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
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DRIVER = os.environ.get("QORE_PLAYWRIGHT_MODULE")


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_GET(self):
        if self.headers.get("Host", "").startswith("localhost:"):
            self.server.outside_requests += 1
        if urlsplit(self.path).path == "/activation-observed":
            self.server.activations.extend(parse_qs(urlsplit(self.path).query).get("event", []))
            self.send_response(204)
            self.end_headers()
        elif self.path == "/redirect-outside":
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
        cls.server.activations = []

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join()

    def probe(self, actions, query="", fixture="keyboard-journey.html", policy=None):
        self.server.outside_requests = 0
        self.server.activations = []
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        base = Path(temporary.name); instructions = base / "actions.json"
        instructions.write_text(json.dumps(actions))
        command = ["node", str(ROOT / "tools/browser_probe.mjs"), "--url", self.origin + "/" + fixture + query,
                   "--output", str(base / "output"), "--actions", str(instructions), "--playwright-module", DRIVER]
        if policy is not None:
            policy_file = base / "policy.json"
            policy_file.write_text(json.dumps(policy))
            command.extend(["--policy", str(policy_file)])
        run = subprocess.run(command, capture_output=True, text=True, timeout=75)
        self.last_outside_requests = self.server.outside_requests
        self.last_activations = list(self.server.activations)
        result = json.loads((base / "output/result.json").read_text()); events = json.loads((base / "output/events.json").read_text())
        return run, result, events

    def activation_policy(self, extra=()):
        question = [{"selector": "#question", "visible": True}]
        descriptors = [
            {"id": "start", "selector": "#start", "role": "button", "name": "Start", "state": [
                {"selector": "#intro", "visible": True}, {"selector": "#question", "visible": False}]},
            {"id": "help", "selector": "#summary", "role": "button", "name": "Help", "state": question},
            {"id": "close", "selector": "#close", "role": "button", "name": "Close", "attributes": {"type": "button"},
             "state": question + [{"selector": "#help", "attributes": {"open": ""}}]},
            {"id": "back", "selector": "#back", "role": "button", "name": "Back", "state": question + [
                {"selector": "#help", "attributes": {"open": None}}]},
        ]
        return {"allowed_origins": [self.origin], "activation_guard": descriptors + list(extra)}

    def guarded_probe(self, actions, policy=None):
        return self.probe(actions, fixture="activation-journey.html", policy=policy or self.activation_policy())

    def assert_activation_blocked(self, run, result, events, target):
        self.assertNotEqual(run.returncode, 0)
        self.assertEqual(result["status"], "PARTIAL")
        self.assertIn("Activation guard blocked", result["error"])
        self.assertTrue(events["blocked_activations"])
        self.assertEqual(events["blocked_activations"][-1]["target"]["id"], target)
        self.assertEqual(events["actions"][-1]["outcome"], "blocked")
        self.assertEqual(self.last_activations, ["start"], "A forbidden page handler ran before the guard refused it")

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

    def test_activation_guard_allows_close_and_back_with_observed_states(self):
        run, result, events = self.guarded_probe([
            {"type": "click", "selector": "#start"},
            {"type": "keyboard", "key": "Return"},
            {"type": "assert-attribute", "selector": "#help", "attribute": "open", "value": ""},
            {"type": "traverse-focus", "selector": "#close"},
            {"type": "keyboard", "key": "Spacebar"},
            {"type": "assert-focused", "selector": "#summary"},
            {"type": "assert-attribute", "selector": "#help", "attribute": "open", "value": None},
            {"type": "assert-none-checked"},
            {"type": "traverse-focus", "selector": "#back"},
            {"type": "keyboard", "key": "NumpadEnter"},
            {"type": "assert-visible", "selector": "#intro"},
            {"type": "assert-hidden", "selector": "#question"},
            {"type": "assert-focused", "selector": "h1"},
            {"type": "assert-none-checked"}])
        self.assertEqual(run.returncode, 0, run.stderr + run.stdout)
        self.assertEqual(result["status"], "COMPLETE")
        self.assertEqual(self.last_activations, ["start", "close", "back"])
        self.assertEqual(events["blocked_activations"], [])
        self.assertEqual(events["actions"][0]["key"], "Tab", "The automatic initial Tab remains part of the probe")
        close = next(check for check in events["activation_checks"] if check["control"] == "close")
        self.assertTrue(close["allowed"])
        self.assertEqual(close["states"][0]["predicates"][-1]["actual"]["attributes"]["open"], "")

    def test_activation_guard_allows_the_actual_same_origin_entry_link(self):
        extra = {"id": "entry", "selector": "#entry", "role": "link", "name": "Open Labs", "attributes": {"href": "#entry-ready"},
                 "state": [{"selector": "#intro", "visible": True}]}
        run, result, events = self.guarded_probe([
            {"type": "click", "selector": "#entry"},
            {"type": "assert-url", "url": self.origin + "/activation-journey.html#entry-ready"}],
            policy=self.activation_policy([extra]))
        self.assertEqual(run.returncode, 0, run.stderr + run.stdout)
        self.assertEqual(result["status"], "COMPLETE")
        self.assertEqual(self.last_activations, ["entry"])
        self.assertTrue(any(check["allowed"] and check["control"] == "entry" for check in events["activation_checks"]))

    def test_activation_guard_blocks_actual_focused_answer_for_enter_and_space_aliases(self):
        for key in ("Enter", "Space", " "):
            with self.subTest(key=repr(key)):
                run, result, events = self.guarded_probe([
                    {"type": "click", "selector": "#start"},
                    {"type": "keyboard", "key": "Tab"},
                    {"type": "assert-focused", "selector": "#answer"},
                    {"type": "keyboard", "key": key},
                    {"type": "click", "selector": "#back"}])
                self.assert_activation_blocked(run, result, events, "answer")
                self.assertFalse(any(event.get("selector") == "#back" for event in events["actions"]))

    def test_activation_guard_blocks_unapproved_clicks_even_when_label_matches(self):
        for action_type in ("click", "click-if-visible"):
            with self.subTest(action_type=action_type):
                run, result, events = self.guarded_probe([
                    {"type": "click", "selector": "#start"}, {"type": action_type, "selector": "#unapproved"}])
                self.assert_activation_blocked(run, result, events, "unapproved")
                self.assertEqual(events["blocked_activations"][-1]["target"]["name"], "Close")

    def test_activation_guard_refuses_mislabeled_nested_and_submission_controls(self):
        for target, name in (("mislabeled", "Close"), ("nested-close", "Close"), ("nested-back", "Back"), ("submit", "Back")):
            with self.subTest(target=target):
                extra = {"id": target, "selector": "#" + target, "role": "button", "name": name,
                         "state": [{"selector": "#question", "visible": True}]}
                run, result, events = self.guarded_probe([
                    {"type": "click", "selector": "#start"}, {"type": "click", "selector": "#" + target}],
                    policy=self.activation_policy([extra]))
                self.assert_activation_blocked(run, result, events, target)

    def test_activation_guard_observes_state_instead_of_trusting_descriptor(self):
        policy = self.activation_policy()
        policy["activation_guard"][-1]["state"][-1]["attributes"]["open"] = ""
        run, result, events = self.guarded_probe([
            {"type": "click", "selector": "#start"}, {"type": "click", "selector": "#back"}], policy=policy)
        self.assert_activation_blocked(run, result, events, "back")
        predicate = events["blocked_activations"][-1]["states"][0]["predicates"][-1]
        self.assertFalse(predicate["passed"])
        self.assertIsNone(predicate["actual"]["attributes"]["open"])

    def test_activation_guard_refuses_modified_activation_and_answer_arrows(self):
        for target, key in (("#summary", "Shift+Enter"), ("#answer", "ArrowRight")):
            with self.subTest(target=target, key=key):
                actions = [{"type": "click", "selector": "#start"}]
                if target == "#answer":
                    actions.append({"type": "keyboard", "key": "Tab"})
                actions.append({"type": "keyboard", "key": key})
                run, result, events = self.guarded_probe(actions)
                self.assert_activation_blocked(run, result, events, target.removeprefix("#"))

    def test_activation_event_capture_rechecks_label_after_pointerdown(self):
        extra = {"id": "late-change", "selector": "#late-change", "role": "button", "name": "Back",
                 "state": [{"selector": "#question", "visible": True}]}
        run, result, events = self.guarded_probe([
            {"type": "click", "selector": "#start"}, {"type": "click", "selector": "#late-change"}],
            policy=self.activation_policy([extra]))
        self.assert_activation_blocked(run, result, events, "late-change")
        checks = [check for check in events["activation_checks"] if check["target"] and check["target"]["id"] == "late-change"]
        self.assertTrue(any(check["source"] == "preflight" and check["allowed"] for check in checks))
        self.assertTrue(any(check["source"] == "event-capture" and not check["allowed"] for check in checks))


class ActivationPolicyValidationTests(unittest.TestCase):
    def test_invalid_guard_schema_is_refused_before_creating_output_or_using_driver(self):
        valid = {"id": "start", "selector": "#start", "role": "button", "name": "Start",
                 "state": [{"selector": "#intro", "visible": True}]}
        invalid = [None, [], {}, [valid | {"unknown": True}], [valid | {"role": "checkbox"}],
                   [valid | {"state": []}], [valid | {"state": [{"selector": "#intro", "visible": "true"}]}],
                   [valid | {"attributes": {}}], [valid, valid]]
        for guard in invalid:
            with self.subTest(guard=guard), tempfile.TemporaryDirectory() as temporary:
                base = Path(temporary); policy = base / "policy.json"
                policy.write_text(json.dumps({"allowed_origins": ["http://127.0.0.1:9"], "activation_guard": guard}))
                run = subprocess.run(["node", str(ROOT / "tools/browser_probe.mjs"), "--url", "http://127.0.0.1:9/",
                                      "--output", str(base / "output"), "--policy", str(policy)], capture_output=True, text=True, timeout=10)
                self.assertNotEqual(run.returncode, 0)
                self.assertIn("activation_guard", run.stderr)
                self.assertFalse((base / "output").exists())
