"""Check durable single-PM recovery and manifest integrity using actual local bytes."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from coordination import initialize, consume, request_review, resume_production, load_register, save_register
from task_gate import DELIVERY_KEYS, canonical_bytes, digest, artifact_bytes, Rejected


class CoordinationTests(unittest.TestCase):
    def setUp(self):
        self.criteria = {"task_id": "journey", "task_revision": 1, "objective": "Verify the declared journey",
                         "authorized_scope": "local test files", "criteria": ["Use current criteria"],
                         "required_check_ids": ["journey"], "expected_results": {"journey": "PASS"}}
        self.register = initialize(self.criteria, "assignment-1", True, True)
        self.common = {key: self.register[key] for key in ("task_id", "task_revision", "criteria_sha256")}
        self.ack = {"id": "ack-1", "body": {**self.common, "kind": "production_ack", "assignment_message_id": "assignment-1"}}
        self.delivery = {"id": "delivery-1", "body": {**self.common, "kind": "delivery", "artifact_revision": "revision-1", "artifact_sha256": "a" * 64, "artifact_path": "artifact.txt"}}

    def test_receive_window_timeout_keeps_task_open_without_resend(self):
        self.assertEqual(consume(self.register, []), self.register)

    def test_newest_first_numeric_window_retains_delivery_and_replay_is_idempotent(self):
        ack = {**self.ack, "id": "2"}
        delivery = {**self.delivery, "id": 10}
        before = deepcopy(self.register)
        for window in ([delivery, ack], [ack, delivery]):
            with self.subTest(ids=[message["id"] for message in window]):
                current = consume(self.register, window)
                self.assertEqual(current["state"], "REVIEW_REQUIRED")
                self.assertEqual(current["delivery_message_id"], "10")
                self.assertEqual([d["action"] for d in current["decisions"]], ["ACCEPT_ACK", "RECEIVE_DELIVERY"])
                self.assertEqual(consume(current, window), current)
                self.assertEqual(self.register, before)

    def test_invalid_or_mixed_window_is_refused_before_any_decision(self):
        for window in ([{**self.ack, "id": 2}, self.delivery], [self.ack, {"body": {}}],
                       [self.ack, {"id": True}], {"messages": [self.ack]}):
            before = deepcopy(self.register)
            with self.assertRaises(Rejected):
                consume(self.register, window)
            self.assertEqual(self.register, before)

    def test_late_current_delivery_is_consumed_on_manual_resume(self):
        current = consume(self.register, [self.ack])
        self.assertEqual(current["awaiting"], "delivery")
        self.assertEqual(consume(current, []), current)
        current = consume(current, [self.delivery])
        self.assertEqual(current["state"], "REVIEW_REQUIRED")
        self.assertIsNone(current["awaiting"])
        self.assertEqual(current["next_action_owner"], "pm")

    def test_read_message_replay_after_saved_decision_before_transport_ack(self):
        current = consume(self.register, [self.ack, self.delivery])
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "tasks.md"
            text = "# Tasks\n\nHuman notes remain.\n\n```qore-task\n{}\n```\n"
            save_register(path, text, current)
            saved_text, recovered = load_register(path)
            self.assertIn("Human notes remain.", saved_text)
            self.assertEqual(consume(recovered, [self.ack, self.delivery]), current)
            self.assertEqual(len(recovered["decisions"]), 2)

    def test_old_criteria_and_premature_delivery_do_not_advance(self):
        stale = deepcopy(self.ack); stale["body"]["task_revision"] = 0
        for message in (stale, self.delivery):
            current = consume(self.register, [message])
            self.assertEqual(current["state"], "ASSIGNED")
            self.assertEqual(current["decisions"][-1]["action"], "REJECT")

    def test_fresh_request_required_no_second_reviewer_on_timeout(self):
        current = consume(self.register, [self.ack, self.delivery])
        request = {key: current[key] for key in DELIVERY_KEYS}
        request.update(review_request_id="request-1", review_session_id="session-1", review_run_id="run-1", review_session_fresh=True)
        current = request_review(current, request)
        self.assertEqual(consume(current, []), current)
        with self.assertRaisesRegex(Rejected, "not ready"):
            request_review(current, request)
        old = {"id": "verdict-1", "body": {**request, "kind": "review_verdict", "review_request_id": "old", "verdict": "PASS"}}
        stale = consume(current, [old])
        self.assertEqual(stale["state"], "REVIEW_REQUIRED")
        self.assertNotIn("pending_verdict", stale)
        verdict = deepcopy(old); verdict["id"] = "verdict-2"; verdict["body"]["review_request_id"] = "request-1"
        received = consume(stale, [verdict])
        self.assertEqual(received["state"], "REVIEW_REQUIRED")
        self.assertEqual(received["pending_verdict"]["message_id"], "verdict-2")

    def test_manifest_hash_does_not_hide_changed_missing_or_escaping_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); data = b"Actual artifact bytes\n"; (root / "artifact.txt").write_bytes(data)
            manifest = {"schema": "qore-task-files/1", "files": [{"path": "artifact.txt", "sha256": digest(data)}]}
            (root / "manifest.json").write_bytes(canonical_bytes(manifest))
            register = {"artifact_kind": "manifest", "artifact_path": "manifest.json"}
            self.assertEqual(artifact_bytes(root, register), canonical_bytes(manifest))
            (root / "artifact.txt").write_bytes(b"Changed\n")
            with self.assertRaisesRegex(Rejected, "actual manifest file bytes differ"): artifact_bytes(root, register)
            (root / "artifact.txt").unlink()
            with self.assertRaisesRegex(Rejected, "unavailable"): artifact_bytes(root, register)
            manifest["files"][0]["path"] = "../escape"
            (root / "manifest.json").write_bytes(canonical_bytes(manifest))
            with self.assertRaisesRegex(Rejected, "contained relative"): artifact_bytes(root, register)

    def review_pending(self):
        current = consume(self.register, [self.ack, self.delivery])
        request = {key: current[key] for key in DELIVERY_KEYS}
        request.update(review_request_id="request-1", review_session_id="session-1", review_run_id="run-1", review_session_fresh=True)
        return request_review(current, request), request

    def test_wrong_session_or_run_cannot_apply_any_verdict(self):
        for field in ("review_session_id", "review_run_id"):
            for verdict in ("FAIL", "PARTIAL", "BLOCKED", "PASS"):
                current, request = self.review_pending()
                message = {"id": "wrong", "body": {**request, "kind": "review_verdict", field: "old", "verdict": verdict}}
                received = consume(current, [message])
                self.assertEqual(received["state"], "REVIEW_REQUIRED")
                self.assertEqual(received["awaiting"], "review_verdict")
                self.assertNotIn("pending_verdict", received)
                self.assertEqual(received["decisions"][-1]["action"], "REJECT")

    def test_failed_or_partial_review_can_resume_with_new_delivery(self):
        for verdict in ("FAIL", "PARTIAL", "BLOCKED"):
            current, request = self.review_pending()
            failed = {"id": "review-1", "body": {**request, "kind": "review_verdict", "verdict": verdict}}
            current = consume(current, [failed])
            current = resume_production(current)
            self.assertEqual(current["review_history"][0]["pending_verdict"]["verdict"], verdict)
            self.assertEqual(current["criteria_sha256"], self.register["criteria_sha256"])
            old = deepcopy(failed); old["id"] = "late-review"
            current = consume(current, [old])
            self.assertEqual(current["state"], "IN_PROGRESS")
            same = deepcopy(self.delivery); same["id"] = "same-revision"
            self.assertEqual(consume(current, [same])["decisions"][-1]["action"], "REJECT")
            changed = deepcopy(self.delivery); changed["id"] = "delivery-2"; changed["body"]["artifact_revision"] = "revision-2"
            current = consume(current, [changed])
            self.assertEqual(current["state"], "REVIEW_REQUIRED")
            second = {key: current[key] for key in DELIVERY_KEYS}
            second.update(review_request_id="request-2", review_session_id="session-2", review_run_id="run-2", review_session_fresh=True)
            current = request_review(current, second)
            self.assertEqual(current["review_request_id"], "request-2")

    def test_resume_cannot_interrupt_active_or_completed_work(self):
        for current in (self.register, self.review_pending()[0], {**self.register, "state": "DONE"}):
            with self.assertRaises(Rejected): resume_production(current)

    def test_multiple_editable_task_blocks_are_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "tasks.md"
            path.write_text('```qore-task\n{}\n```\n' * 2)
            with self.assertRaisesRegex(Rejected, "exactly one"): load_register(path)
