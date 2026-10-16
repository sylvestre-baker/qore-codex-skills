"""Verify adapter recovery ordering with a fake transport; real wire receipts are separate."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
import urllib.request
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from agent_mail import Client, receive
from coordination import initialize, save_register, load_register


class ReceiveTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        self.path = Path(temporary.name) / "tasks.md"
        self.criteria = {"task_id": "resume", "task_revision": 1, "objective": "Resume", "authorized_scope": "local",
                         "criteria": ["Preserve decisions"], "required_check_ids": ["check"], "expected_results": {"check": "PASS"}}
        self.register = initialize(self.criteria, "1", True, True)
        save_register(self.path, "# Private\n```qore-task\n{}\n```\n", self.register)
        common = {key: self.register[key] for key in ("task_id", "task_revision", "criteria_sha256")}
        self.entries = [{"id": 2, "thread_id": "resume", "ack_required": True, "body_md": json.dumps({**common, "kind": "production_ack", "assignment_message_id": "1"})}]

    def test_saved_decision_precedes_transport_ack_and_replay_is_safe(self):
        outer = self
        class Transport:
            def call(self, name, arguments):
                if name == "fetch_inbox":
                    outer.assertIs(arguments["unread_only"], False)
                    return outer.entries
                _, saved = load_register(outer.path)
                outer.assertIn("2", saved["processed_message_ids"])
                outer.assertEqual(saved["state"], "IN_PROGRESS")
                return {"acknowledged": True}
        first = receive(Transport(), self.path, "project", "pm", "resume", seconds=0)
        before = self.path.read_bytes()
        second = receive(Transport(), self.path, "project", "pm", "resume", seconds=0)
        self.assertEqual(first["status"], "RECEIVED"); self.assertEqual(second["status"], "WAITING")
        self.assertEqual(before, self.path.read_bytes())

    def test_no_messages_timeout_retains_open_assignment(self):
        class Transport:
            def call(self, *_): return []
        result = receive(Transport(), self.path, "project", "pm", "resume", seconds=0)
        self.assertEqual(result["status"], "WAITING")
        self.assertEqual(load_register(self.path)[1], self.register)

    def test_two_receive_failures_block_then_recovery_uses_same_assignment(self):
        outer = self
        class Broken:
            def call(self, *_): raise OSError("Synthetic transport failure")
        with patch("agent_mail.time.sleep", return_value=None):
            result = receive(Broken(), self.path, "project", "pm", "resume", seconds=10)
        self.assertEqual(result["status"], "BLOCKED")
        class Recovered:
            def call(self, name, _): return outer.entries if name == "fetch_inbox" else {}
        result = receive(Recovered(), self.path, "project", "pm", "resume", seconds=0)
        saved = load_register(self.path)[1]
        self.assertEqual(result["state"], "IN_PROGRESS")
        self.assertEqual(saved["assignment_message_id"], "1")
        self.assertEqual(saved["next_action_owner"], "production")

    def test_remote_endpoint_and_missing_token_are_refused(self):
        for url, token in [("https://example.com/mcp/", "test"), ("http://127.0.0.1:1/mcp/", "")]:
            with self.assertRaises(ValueError): Client(url, token)

    def test_environment_proxy_is_disabled_for_loopback_bearer(self):
        class Captured(Exception): pass
        class Dispatch(urllib.request.HTTPHandler):
            def http_open(inner, request):
                self.assertEqual(request.host, "127.0.0.1:8765")
                self.assertEqual(request.selector, "/mcp/")
                self.assertEqual(request.get_header("Authorization"), "Bearer synthetic")
                raise Captured()
        build = urllib.request.build_opener
        def opener(*handlers): return build(*handlers, Dispatch())
        with patch.dict("os.environ", {"http_proxy": "http://synthetic-proxy.invalid:8123", "no_proxy": ""}, clear=True), patch("agent_mail.urllib.request.build_opener", side_effect=opener):
            with self.assertRaises(Captured): Client("http://127.0.0.1:8765/mcp/", "synthetic").call("fetch_inbox", {})

    def test_slow_ack_batch_recomputes_deadline_and_replays_pending_ack(self):
        outer = self; clock = [0.0]; calls = []
        entries = [{**self.entries[0], "id": i} for i in range(2, 9)]
        class Transport(Client):
            def __init__(inner): inner.timeout = 30
            def call(inner, name, arguments):
                calls.append((name, clock[0], inner.timeout))
                clock[0] += min(2 if name == "fetch_inbox" else 25, inner.timeout)
                return entries if name == "fetch_inbox" else {}
        with patch("agent_mail.time.monotonic", side_effect=lambda: clock[0]):
            result = receive(Transport(), self.path, "project", "pm", "resume", seconds=120)
        self.assertEqual(result["status"], "RECEIVED")
        self.assertEqual(clock[0], 120)
        self.assertTrue(all(start < 120 and timeout <= 120-start for _, start, timeout in calls))
        self.assertEqual(len(load_register(self.path)[1]["processed_message_ids"]), 7)
        self.assertLess(len(result["acknowledged"]), 7)
