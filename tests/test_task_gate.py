"""Synthetic local fixtures, not Agent Mail wire evidence or independent review."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from task_gate import Rejected, REVIEW_KEYS, DELIVERY_KEYS, canonical_bytes, digest, evaluate, atomic_write


class GateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.artifact = b'def normalize_label(value):\n    return value.lower()\n'
        (self.root / "artifact.py").write_bytes(self.artifact)
        self.snapshot = {"task_id": "private-probe", "task_revision": 1,
                         "objective": "Normalize Unicode labels", "authorized_scope": "one local file",
                         "criteria": ["Unicode labels are lowercased"],
                         "required_check_ids": ["unicode"], "expected_results": {"unicode": "PASS"}}
        self.register = {"task_id": "private-probe", "task_revision": 1,
                         "criteria_sha256": digest(canonical_bytes(self.snapshot)),
                         "artifact_revision": "artifact-1", "artifact_sha256": digest(self.artifact),
                         "artifact_path": "artifact.py", "delivery_message_id": "delivery-1",
                         "review_request_id": "request-1", "review_session_id": "fresh-reviewer-1",
                         "review_run_id": "run-1", "review_session_fresh": True,
                         "dependencies_satisfied": True, "authorization_satisfied": True,
                         "state": "REVIEW_REQUIRED", "awaiting": "review_verdict",
                         "next_action_owner": "PM", "accepted_identity": None,
                         "processed_message_ids": []}
        self.delivery = {key: self.register[key] for key in DELIVERY_KEYS}
        self.delivery["artifact_path"] = "artifact.py"
        self.request = {key: self.register[key] for key in REVIEW_KEYS}
        self.request.update(review_session_id="fresh-reviewer-1", review_run_id="run-1")
        self.verdict = dict(self.request, verdict="PASS", message_id="verdict-1")
        self.proof = dict(self.request, check_id="unicode", result="PASS")
        self.write_proof()

    def write_proof(self):
        raw = canonical_bytes(self.proof)
        (self.root / "proof.json").write_bytes(raw)
        self.verdict["proofs"] = [{"check_id": "unicode", "path": "proof.json", "sha256": digest(raw)}]

    def run_gate(self):
        return evaluate(self.register, self.snapshot, self.delivery, self.request, self.verdict, self.root)

    def rejected(self, fragment):
        original = deepcopy(self.register)
        with self.assertRaisesRegex(Rejected, fragment):
            self.run_gate()
        self.assertEqual(self.register, original)

    def test_current_identity_accepts_and_atomically_records(self):
        decision, replacement = self.run_gate()
        self.assertEqual(decision["action"], "DONE")
        self.assertEqual(replacement["processed_message_ids"], ["delivery-1", "request-1", "verdict-1"])
        target = self.root / "register.json"
        atomic_write(target, replacement)
        self.assertEqual(json.loads(target.read_bytes()), replacement)
        self.assertEqual(replacement["accepted_proofs"], self.verdict["proofs"])

    def test_exact_canonical_rule_unicode_order_lf_and_no_nan(self):
        self.assertEqual(canonical_bytes({"z": "É", "a": 1}), '{"a":1,"z":"É"}\n'.encode())
        with self.assertRaises(ValueError):
            canonical_bytes({"bad": float("nan")})

    def test_same_artifact_new_criteria_rejects_late_old_pass(self):
        self.snapshot.update(task_revision=2, criteria=["Non-ASCII input must raise ValueError"])
        self.register.update(task_revision=2, criteria_sha256=digest(canonical_bytes(self.snapshot)),
                             delivery_message_id="delivery-2", review_request_id="request-2")
        self.assertEqual(digest((self.root / "artifact.py").read_bytes()), self.register["artifact_sha256"])
        # Old delivery, request, verdict and proof remain immutable local fixtures.
        self.rejected("delivery identity differs")

    def test_new_criteria_current_delivery_still_rejects_old_review(self):
        self.snapshot.update(task_revision=2, criteria=["Non-ASCII input must raise ValueError"])
        self.register.update(task_revision=2, criteria_sha256=digest(canonical_bytes(self.snapshot)))
        self.delivery.update({key: self.register[key] for key in DELIVERY_KEYS})
        self.request.update({key: self.register[key] for key in REVIEW_KEYS})
        self.rejected("review identity differs")

    def test_criteria_modified_without_rehash_rejected(self):
        self.snapshot["criteria"] = ["Reject non-ASCII"]
        self.rejected("current criteria bytes changed")

    def test_actual_artifact_tamper_rejected(self):
        (self.root / "artifact.py").write_bytes(b"changed\n")
        self.rejected("actual artifact bytes differ")

    def test_wrong_artifact_identity_rejected(self):
        self.verdict["artifact_sha256"] = "0" * 64
        self.rejected("review identity differs")

    def test_wrong_request_rejected(self):
        self.verdict["review_request_id"] = "request-old"
        self.rejected("review identity differs")

    def test_new_artifact_rejects_old_review(self):
        new = b"new artifact\n"
        (self.root / "artifact.py").write_bytes(new)
        self.register.update(artifact_revision="artifact-2", artifact_sha256=digest(new),
                             delivery_message_id="delivery-2", review_request_id="request-2")
        self.delivery.update({key: self.register[key] for key in DELIVERY_KEYS})
        self.request.update({key: self.register[key] for key in REVIEW_KEYS})
        self.rejected("review identity differs")

    def test_missing_check_rejected(self):
        self.verdict["proofs"] = []
        self.rejected("required proof missing")

    def test_wrong_check_rejected(self):
        self.verdict["proofs"][0]["check_id"] = "different"
        self.rejected("proof check IDs differ")

    def test_actual_proof_tamper_rejected(self):
        (self.root / "proof.json").write_bytes(b"{}\n")
        self.rejected("actual evidence bytes differ")

    def test_proof_current_hash_but_old_identity_rejected(self):
        self.proof["task_revision"] = 0
        self.write_proof()
        self.rejected("proof identity differs")

    def test_blocked_partial_failed_proof_rejected(self):
        for result in ("PARTIAL", "BLOCKED", "FAIL"):
            with self.subTest(result=result):
                self.proof["result"] = result
                self.write_proof()
                self.rejected("proof result differs")

    def test_wrong_review_session_and_run_rejected(self):
        for field in ("review_session_id", "review_run_id"):
            with self.subTest(field=field):
                original = self.verdict[field]
                self.verdict[field] = "different"
                self.rejected("review (session|run) differs")
                self.verdict[field] = original

    def test_dependencies_authorization_and_wait_are_required(self):
        for field, value, reason in (("dependencies_satisfied", False, "dependencies"),
                                     ("authorization_satisfied", False, "authorization"),
                                     ("awaiting", "delivery", "does not await"),
                                     ("review_session_fresh", False, "not designated fresh")):
            with self.subTest(field=field):
                original = self.register[field]
                self.register[field] = value
                self.rejected(reason)
                self.register[field] = original

    def test_replayed_done_is_traceable_noop_without_state_change(self):
        _, self.register = self.run_gate()
        original = deepcopy(self.register)
        decision, replacement = self.run_gate()
        self.assertEqual(decision["action"], "NOOP")
        self.assertEqual(decision["reason"], "already consumed")
        self.assertEqual(replacement, original)
        self.assertEqual(replacement["processed_message_ids"].count("verdict-1"), 1)

    def test_proof_cannot_escape_root(self):
        self.verdict["proofs"][0]["path"] = "../outside.json"
        self.rejected("contained relative path")


if __name__ == "__main__":
    unittest.main(verbosity=2)
