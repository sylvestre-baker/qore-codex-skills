"""Validate execution evidence identity and required phase coverage, not report quality."""
import hashlib
import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest


TOOLS = Path(__file__).resolve().parents[1] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
contracts = importlib.import_module("run_contract")
published = importlib.import_module("check_execution_records")


class RunContractTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "evidence"
        self.root.mkdir()

    def artifact_bytes(self, path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def packet(self, method="review"):
        packet = {
            "schema": "qore-run/1", "id": "fixture-run", "skill": "qore-" + method,
            "method": method, "candidate_sha256": "a" * 64,
            "target": {"label": "Isolated fixture target", "snapshot_sha256": "b" * 64},
            "environment": {"id": "test-environment", "operator": "automated-fixture", "host": "test-host"},
            "last_relevant_change": "2026-10-15T10:00:00+00:00",
            "required_phases": sorted(contracts.PHASES[method]),
            "phases": [], "artifacts": [], "coverage": "COMPLETE", "limitations": ["Synthetic structural fixture; no quality claim."], "commands": [],
        }
        if method == "ux":
            packet["scope"] = {"depth": "full", "state_transition_applicable": True}
        for phase_id in packet["required_phases"]:
            relative = method + "-" + phase_id.replace(".", "-") + ".json"
            header = {"candidate_sha256": packet["candidate_sha256"], "target_snapshot_sha256": packet["target"]["snapshot_sha256"], "observed_at": "2026-10-15T11:00:00+00:00", "phase_id": phase_id}
            path = self.root / relative
            path.write_text(json.dumps({"qore_evidence": header, "payload": {"result": "Fixture output for " + phase_id}}), encoding="utf-8")
            packet["artifacts"].append({"path": relative, "sha256": self.artifact_bytes(path), "kind": "execution", "candidate_sha256": header["candidate_sha256"], "target_snapshot_sha256": header["target_snapshot_sha256"], "observed_at": header["observed_at"]})
            packet["phases"].append({"id": phase_id, "status": "PASS", "actor_id": "actor-" + phase_id, "artifacts": [relative]})
        return packet

    def phase(self, packet, phase_id):
        return next(phase for phase in packet["phases"] if phase["id"] == phase_id)

    def descriptor(self, packet, phase_id):
        ref = self.phase(packet, phase_id)["artifacts"][0]
        return next(row for row in packet["artifacts"] if row["path"] == ref)

    def rewrite_header(self, packet, selected_phase, **changes):
        descriptor = self.descriptor(packet, selected_phase)
        path = self.root / descriptor["path"]
        body = json.loads(path.read_text())
        body["qore_evidence"].update(changes)
        path.write_text(json.dumps(body), encoding="utf-8")
        descriptor["sha256"] = self.artifact_bytes(path)

    def validate(self, packet):
        return contracts.validate_run(packet, self.root)

    def test_positive_complete_plan_review_and_ux_runs(self):
        for method in ("plan", "review", "ux"):
            with self.subTest(method=method):
                result = self.validate(self.packet(method))
                self.assertEqual((result["valid"], result["coverage"], result["missing_phases"]), (True, "COMPLETE", []))

    def cache_record(self):
        packet = self.packet()
        item = {"path": "snapshot/__pycache__/source.pyc", "sha256": "c" * 64}
        packet["artifacts"].append({**item, "kind": "source"})
        path = self.root / "execution.json"
        path.write_text(json.dumps(packet))
        exception = {"execution_sha256": self.artifact_bytes(path), "reason": "Keep source caches out of redistribution.",
                     "excluded_source_artifacts": [item]}
        return path, exception

    def test_exact_missing_source_cache_is_an_explicit_partial_exception(self):
        path, exception = self.cache_record()
        before = path.read_bytes()
        result = published.check_record(path, exception)
        self.assertEqual((result["status"], result["coverage"], result["strict_validation"]), ("KNOWN_EXCEPTION", "PARTIAL", "BLOCKED"))
        self.assertEqual(path.read_bytes(), before)
        with self.assertRaisesRegex(ValueError, "Artifact is missing"):
            published.check_record(path)

    def test_cache_exception_cannot_hide_missing_execution_or_changed_identity(self):
        path, exception = self.cache_record()
        (self.root / "review-verifier.json").unlink()
        with self.assertRaisesRegex(ValueError, "review-verifier.json"):
            published.check_record(path, exception)
        path.write_text(path.read_text() + "\n")
        with self.assertRaisesRegex(ValueError, "unchanged execution"):
            published.check_record(path, exception)

    def test_noncache_source_cannot_be_excluded(self):
        path, exception = self.cache_record()
        packet = json.loads(path.read_text())
        packet["artifacts"][-1]["path"] = "source.py"
        path.write_text(json.dumps(packet))
        exception["execution_sha256"] = self.artifact_bytes(path)
        exception["excluded_source_artifacts"][0]["path"] = "source.py"
        with self.assertRaisesRegex(ValueError, "Only exact unreferenced source caches"):
            published.check_record(path, exception)

    def test_unknown_schema_major_and_method_are_refused(self):
        packet = self.packet()
        packet["schema"] = "qore-run/2"
        with self.assertRaises(ValueError):
            self.validate(packet)
        packet["schema"] = "qore-run/1"
        packet["method"] = "unknown"
        with self.assertRaises(ValueError):
            self.validate(packet)

    def test_wrong_candidate_or_target_digest_formats_are_refused(self):
        for field in ("candidate", "target"):
            packet = self.packet()
            if field == "candidate":
                packet["candidate_sha256"] = "not-a-digest"
            else:
                packet["target"]["snapshot_sha256"] = "1234"
            with self.assertRaises(ValueError):
                self.validate(packet)

    def test_artifact_byte_changes_cannot_keep_a_recorded_digest(self):
        packet = self.packet()
        descriptor = packet["artifacts"][0]
        (self.root / descriptor["path"]).write_text("Changed output after recording.", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.validate(packet)

    def test_execution_descriptor_cannot_name_another_candidate_or_target(self):
        for field in ("candidate_sha256", "target_snapshot_sha256"):
            packet = self.packet()
            self.descriptor(packet, "verifier")[field] = "c" * 64
            with self.assertRaises(ValueError):
                self.validate(packet)

    def test_execution_header_must_match_the_recorded_identity(self):
        for field in ("candidate_sha256", "target_snapshot_sha256", "observed_at"):
            packet = self.packet()
            value = "2026-10-15T11:30:00+00:00" if field == "observed_at" else "d" * 64
            self.rewrite_header(packet, "verifier", **{field: value})
            with self.assertRaises(ValueError):
                self.validate(packet)

    def test_self_consistent_proof_from_another_candidate_or_target_is_refused(self):
        for field in ("candidate_sha256", "target_snapshot_sha256"):
            packet = self.packet()
            descriptor = self.descriptor(packet, "verifier")
            descriptor[field] = "c" * 64
            self.rewrite_header(packet, "verifier", **{field: "c" * 64})
            with self.assertRaises(ValueError):
                self.validate(packet)

    def test_proof_must_be_strictly_after_the_last_relevant_change(self):
        for observed in ("2026-10-15T09:59:59+00:00", "2026-10-15T10:00:00+00:00"):
            packet = self.packet()
            descriptor = self.descriptor(packet, "verifier")
            descriptor["observed_at"] = observed
            self.rewrite_header(packet, "verifier", observed_at=observed)
            with self.assertRaises(ValueError):
                self.validate(packet)

    def test_timestamps_require_timezone_and_actual_parseable_values(self):
        for field, value in (("last_relevant_change", "2026-10-15T10:00:00"), ("last_relevant_change", "yesterday"), ("observed_at", "2026-10-15T11:00:00")):
            packet = self.packet()
            if field == "observed_at":
                self.descriptor(packet, "verifier")[field] = value
                self.rewrite_header(packet, "verifier", **{field: value})
            else:
                packet[field] = value
            with self.assertRaises(ValueError):
                self.validate(packet)

    def test_old_source_or_presentation_artifacts_cannot_alone_prove_a_pass(self):
        for kind in ("source", "presentation"):
            packet = self.packet()
            self.descriptor(packet, "verifier")["kind"] = kind
            with self.assertRaises(ValueError):
                self.validate(packet)

    def test_an_execution_artifact_cannot_prove_a_different_phase(self):
        packet = self.packet()
        self.rewrite_header(packet, "verifier", phase_id="redaction")
        with self.assertRaises(ValueError):
            self.validate(packet)

    def test_required_phase_lists_cannot_omit_or_repeat_method_phases(self):
        for mutation in ("omit", "repeat"):
            packet = self.packet()
            if mutation == "omit":
                packet["required_phases"].remove("verifier")
            else:
                packet["required_phases"].append("verifier")
            with self.assertRaises(ValueError):
                self.validate(packet)

    def test_missing_or_skipped_required_phases_limit_coverage(self):
        packet = self.packet()
        packet["phases"] = [phase for phase in packet["phases"] if phase["id"] != "verifier"]
        with self.assertRaises(ValueError):
            self.validate(packet)
        packet["coverage"] = "PARTIAL"
        result = self.validate(packet)
        self.assertEqual(result["missing_phases"], ["verifier"])
        packet = self.packet()
        self.phase(packet, "verifier").update(status="SKIPPED", reason="No independent execution context available")
        packet["coverage"] = "PARTIAL"
        self.assertEqual(self.validate(packet)["coverage"], "PARTIAL")

    def test_all_blocked_phases_report_blocked_coverage(self):
        packet = self.packet()
        for phase in packet["phases"]:
            phase.update(status="BLOCKED", reason="Required capability unavailable", artifacts=[])
        packet["coverage"] = "BLOCKED"
        self.assertEqual(self.validate(packet)["coverage"], "BLOCKED")

    def test_verifier_must_be_independent_of_every_finder(self):
        packet = self.packet()
        self.phase(packet, "verifier")["actor_id"] = self.phase(packet, "finder.correctness")["actor_id"]
        with self.assertRaises(ValueError):
            self.validate(packet)

    def test_named_finders_require_distinct_contexts(self):
        packet = self.packet()
        self.phase(packet, "finder.security")["actor_id"] = self.phase(packet, "finder.correctness")["actor_id"]
        with self.assertRaises(ValueError):
            self.validate(packet)

    def test_finder_independence_is_required_even_when_verifier_is_skipped(self):
        packet = self.packet()
        self.phase(packet, "finder.security")["actor_id"] = self.phase(packet, "finder.correctness")["actor_id"]
        self.phase(packet, "verifier").update(status="SKIPPED", reason="No verifier context available")
        packet["coverage"] = "PARTIAL"
        with self.assertRaises(ValueError):
            self.validate(packet)

    def test_profiled_runs_require_a_profile_preflight_phase(self):
        packet = self.packet()
        packet["profile"] = {"id": "fixture", "version": "1.0.0", "sha256": "e" * 64}
        with self.assertRaises(ValueError):
            self.validate(packet)
        packet["required_phases"].append("profile_preflight")
        packet["coverage"] = "PARTIAL"
        result = self.validate(packet)
        self.assertEqual(result["missing_phases"], ["profile_preflight"])
        packet["profile"]["sha256"] = "invalid-profile-digest"
        with self.assertRaises(ValueError):
            self.validate(packet)

    def test_profile_preflight_is_mandatory_for_profiled_runs(self):
        packet = self.packet()
        packet["profile"] = {"id": "fixture", "version": "1.0.0", "sha256": "e" * 64}
        packet["required_phases"].append("profile_preflight")
        packet["phases"].append({"id": "profile_preflight", "actor_id": "operator", "status": "NOT_APPLICABLE", "reason": "Current source check omitted", "artifacts": []})
        with self.assertRaises(ValueError):
            self.validate(packet)

    def test_recorded_commands_require_typed_arguments_exit_status_and_artifact(self):
        packet = self.packet()
        ref = self.phase(packet, "findings_validation")["artifacts"][0]
        packet["commands"] = [{"argv": ["node", "finding-lint.mjs", "packet.json"], "exit_code": 0, "artifact": ref}]
        self.assertEqual(self.validate(packet)["coverage"], "COMPLETE")
        for command in ({"argv": [], "exit_code": 0, "artifact": ref}, {"argv": [1], "exit_code": 0, "artifact": ref}, {"argv": ["node"], "exit_code": True, "artifact": ref}, {"argv": ["node"], "exit_code": 0, "artifact": "undeclared.json"}):
            packet["commands"] = [command]
            with self.assertRaises(ValueError):
                self.validate(packet)

    def test_all_five_planning_perspectives_require_distinct_contexts(self):
        packet = self.packet("plan")
        self.phase(packet, "qa")["actor_id"] = self.phase(packet, "product")["actor_id"]
        with self.assertRaises(ValueError):
            self.validate(packet)

    def test_pass_needs_declared_evidence_and_cannot_borrow_another_phase(self):
        for refs in ([], ["undeclared.json"]):
            packet = self.packet()
            self.phase(packet, "verifier")["artifacts"] = refs
            with self.assertRaises(ValueError):
                self.validate(packet)

    def test_artifact_paths_cannot_escape_by_traversal_symlink_or_prefix(self):
        for kind in ("traversal", "symlink", "prefix"):
            packet = self.packet()
            descriptor = self.descriptor(packet, "verifier")
            old = descriptor["path"]
            sibling = self.root.with_name(self.root.name + "-other")
            sibling.mkdir(exist_ok=True)
            outside = sibling / "proof.json"
            outside.write_bytes((self.root / old).read_bytes())
            if kind == "symlink":
                (self.root / old).unlink()
                (self.root / old).symlink_to(outside)
            else:
                descriptor["path"] = "../" + ("evidence-other/" if kind == "prefix" else "evidence-other/../evidence-other/") + "proof.json"
                self.phase(packet, "verifier")["artifacts"] = [descriptor["path"]]
            with self.assertRaises(ValueError):
                self.validate(packet)

    def test_entry_state_and_full_scopes_require_real_transition_evidence(self):
        for depth in ("entry", "state", "full"):
            packet = self.packet("ux")
            packet["scope"] = {"depth": depth, "state_transition_applicable": False}
            self.phase(packet, "state_transition").update(status="NOT_APPLICABLE", reason="No transition attempted")
            with self.assertRaises(ValueError):
                self.validate(packet)

    def test_copy_visual_and_perf_allow_explicit_supported_non_applicability(self):
        for depth in ("copy", "visual", "perf"):
            packet = self.packet("ux")
            packet["scope"] = {"depth": depth, "state_transition_applicable": False}
            self.phase(packet, "state_transition").update(status="NOT_APPLICABLE", reason="The scoped correction changes no state transition")
            self.assertEqual(self.validate(packet)["coverage"], "COMPLETE")

    def test_non_applicability_requires_explicit_scope_reason_and_artifact(self):
        for mutation in ("scope", "reason", "artifact"):
            packet = self.packet("ux")
            packet["scope"] = {"depth": "copy", "state_transition_applicable": False}
            phase = self.phase(packet, "state_transition")
            phase.update(status="NOT_APPLICABLE", reason="The copy-only scope changes no state transition")
            if mutation == "scope":
                del packet["scope"]
            elif mutation == "reason":
                del phase["reason"]
            else:
                phase["artifacts"] = []
            with self.assertRaises(ValueError):
                self.validate(packet)

    def test_other_mandatory_method_phases_cannot_be_declared_non_applicable(self):
        packet = self.packet()
        self.phase(packet, "verifier").update(status="NOT_APPLICABLE", reason="Verifier omitted")
        with self.assertRaises(ValueError):
            self.validate(packet)


if __name__ == "__main__":
    unittest.main()
