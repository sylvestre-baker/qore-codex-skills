"""Real optional-driver regressions against a synthetic local journey, never the live site."""
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parents[1]
DRIVER = os.environ.get("QORE_PLAYWRIGHT_MODULE")


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_GET(self):
        if self.headers.get("Host", "").startswith("localhost:"):
            self.server.outside_requests += 1
        if self.path == "/redirect-outside":
            self.send_response(302)
            self.send_header("Location", "http://localhost:" + str(self.server.server_port) + "/keyboard-journey.html")
            self.end_headers()
        else:
            super().do_GET()


@unittest.skipUnless(DRIVER, "Set QORE_PLAYWRIGHT_MODULE to an existing optional Playwright installation")
class BrowserProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(ROOT / "tests/fixtures")))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True); cls.thread.start()
        cls.origin = "http://127.0.0.1:" + str(cls.server.server_port)
        cls.server.outside_requests = 0

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join()

    def probe(self, actions, query=""):
        self.server.outside_requests = 0
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        base = Path(temporary.name); instructions = base / "actions.json"
        instructions.write_text(json.dumps(actions))
        command = ["node", str(ROOT / "tools/browser_probe.mjs"), "--url", self.origin + "/keyboard-journey.html" + query,
                   "--output", str(base / "output"), "--actions", str(instructions), "--playwright-module", DRIVER]
        run = subprocess.run(command, capture_output=True, text=True, timeout=75)
        self.last_outside_requests = self.server.outside_requests
        result = json.loads((base / "output/result.json").read_text()); events = json.loads((base / "output/events.json").read_text())
        return run, result, events

    def test_keyboard_reachable_back_and_legacy_actions_complete(self):
        run, result, events = self.probe([
            {"type": "click", "selector": "#start"},
            {"type": "assert-text", "text": "First question (unanswered)"},
            {"type": "traverse-focus", "selector": "#back", "max_steps": 12},
            {"type": "assert-focused", "selector": "#back"},
            {"type": "keyboard", "key": "Enter"},
            {"type": "assert-focused", "selector": "h1"},
            {"type": "assert-visible", "selector": "#intro"},
            {"type": "assert-hidden", "selector": "#question"},
            {"type": "assert-none-checked"}, {"type": "snapshot", "label": "returned"}])
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(result["status"], "COMPLETE")
        self.assertTrue(any(event["type"] == "focus-step" and event["reached"] for event in events["actions"]))
        back = next(index for index, event in enumerate(events["actions"]) if event["type"] == "focus-step" and event["reached"] and event["active_element"]["id"] == "back")
        self.assertTrue(any(event["type"] == "keyboard" and event.get("key") == "Enter" for event in events["actions"][back + 1:]))

    def test_mouse_success_cannot_hide_back_outside_tab_order(self):
        run, result, events = self.probe([
            {"type": "click", "selector": "#start"},
            {"type": "traverse-focus", "selector": "#back", "max_steps": 6},
            {"type": "click", "selector": "#back"}], "?excluded=1")
        self.assertNotEqual(run.returncode, 0)
        self.assertEqual(result["status"], "PARTIAL")
        self.assertIn("not reached", result["error"])
        self.assertFalse(any(event.get("selector") == "#back" and event["type"] == "click" for event in events["actions"]))

    def test_read_only_policy_blocks_post_without_hiding_observation(self):
        run, result, events = self.probe([{"type": "click", "selector": "#start"}, {"type": "click", "selector": "#post"}])
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(result["policy"]["service_workers"], "block")
        self.assertEqual(events["blocked_mutations"][0]["method"], "POST")

    def test_outside_origin_navigation_is_blocked_and_reported(self):
        run, result, events = self.probe([{"type": "click", "selector": "#start"}, {"type": "click", "selector": "#escape"}])
        self.assertTrue(events["blocked_navigation"])
        self.assertNotEqual(result["status"], "COMPLETE")

    def test_false_focus_assertion_fails(self):
        run, result, _ = self.probe([{"type": "assert-focused", "selector": "h1"}])
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("Expected focused control", result["error"])

    def test_focus_can_settle_after_the_old_fixed_pause(self):
        run, result, _ = self.probe([{"type": "click", "selector": "#start"}, {"type": "traverse-focus", "selector": "#back"},
                                     {"type": "keyboard", "key": "Enter"}, {"type": "assert-focused", "selector": "h1"}], "?delay=2200")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(result["status"], "COMPLETE")

    def test_correct_heading_focus_cannot_hide_retained_question(self):
        run, result, _ = self.probe([{"type": "click", "selector": "#start"}, {"type": "traverse-focus", "selector": "#back"},
                                     {"type": "keyboard", "key": "Enter"}, {"type": "assert-focused", "selector": "h1"},
                                     {"type": "assert-hidden", "selector": "#question"}], "?retained-question=1")
        self.assertNotEqual(run.returncode, 0)
        self.assertEqual(result["status"], "PARTIAL")

    def test_close_focus_is_independent_of_correct_back(self):
        actions = [{"type": "click", "selector": "#start"}, {"type": "keyboard", "key": "Enter"},
                   {"type": "assert-attribute", "selector": "details", "attribute": "open", "value": ""},
                   {"type": "traverse-focus", "selector": "#close"}, {"type": "keyboard", "key": "Enter"},
                   {"type": "assert-focused", "selector": "summary"}]
        positive, _, _ = self.probe(actions)
        self.assertEqual(positive.returncode, 0, positive.stderr)
        negative, result, _ = self.probe(actions, "?wrong-close=1")
        self.assertNotEqual(negative.returncode, 0)
        self.assertIn("Expected focused control", result["error"])

    def test_pre_back_unanswered_check_catches_selection_before_unmount(self):
        run, result, _ = self.probe([{"type": "click", "selector": "#start"}, {"type": "keyboard", "key": "Enter"},
                                     {"type": "traverse-focus", "selector": "#close"}, {"type": "keyboard", "key": "Enter"},
                                     {"type": "assert-none-checked"}], "?select-on-close=1")
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("selection is checked", result["error"])

    def test_delayed_url_succeeds_and_missing_url_fails(self):
        run, _, _ = self.probe([{"type": "click", "selector": "#start"}, {"type": "click", "selector": "#delayed-url"},
                                {"type": "assert-url", "url": self.origin + "/keyboard-journey.html#resolved"}])
        self.assertEqual(run.returncode, 0, run.stderr)
        missing, result, _ = self.probe([{"type": "assert-url", "url": self.origin + "/missing"}])
        self.assertNotEqual(missing.returncode, 0)
        self.assertEqual(result["status"], "PARTIAL")

    def test_popup_and_redirect_to_outside_origin_are_blocked(self):
        for selector in ("#popup", "#redirect"):
            with self.subTest(selector=selector):
                run, result, events = self.probe([{"type": "click", "selector": "#start"}, {"type": "click", "selector": selector}])
                self.assertTrue(events["blocked_navigation"])
                self.assertNotEqual(result["status"], "COMPLETE")
                self.assertEqual(self.last_outside_requests, 0, "The forbidden document reached the server")
