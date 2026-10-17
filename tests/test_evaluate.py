"""Counterexamples for source isolation, evidence identity and honest comparisons."""
import copy
import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
evaluate = importlib.import_module("evaluate")


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def empty_series(self):
        """Keep synthetic refusal controls independent of published campaign results."""
        config, _, config_sha = evaluate.configuration()
        return {"schema": "qore-eval-series/1", "id": "synthetic-unit-series",
                "scenarios_sha256": config_sha, "status": "BLOCKED", "excluded_pilot": [],
                "cells": [{"scenario_id": sid, "condition": condition, "status": "NOT_RUN",
                           "records": [], "reason": "Synthetic not-run control; no model invocation."}
                          for sid, condition in config["order"]]}

    def prepared(self, condition="baseline", scenario="R2"):
        path = self.root / (scenario + "-" + condition)
        evaluate.prepare(scenario, condition, path)
        return path

    def baseline(self, condition="baseline", scenario="R2"):
        prepared = self.prepared(condition, scenario)
        manifest = evaluate.read_json(prepared / "input-manifest.json")
        config, scenarios, _ = evaluate.configuration()
        run = {
            "schema": "qore-eval-run/1", "id": "synthetic-unit-" + scenario + "-" + condition, "series_id": "synthetic-unit-series",
            "scenario_id": scenario, "condition": condition, "trial": 1,
            "candidate_sha256": manifest["candidate_sha256"], "input_manifest": prepared.name + "/input-manifest.json",
            "input_manifest_sha256": evaluate.digest(prepared / "input-manifest.json"),
            "condition_resources_sha256": manifest["condition_resources_sha256"],
            "environment": {"operator": "synthetic automated unit fixture", "host": "unit-test", "model": "not-a-real-model", "actor_id": "unit-parent",
                            "tools": {}, "settings": {}, "isolation": {"status": "PASS", "evidence": ["observation.json"]}},
            "resources": {"caps": config["budgets"], "started_at": "2026-10-17T06:00:00Z", "ended_at": "2026-10-17T06:01:00Z",
                          "tokens": None, "aggregate_agent_seconds": None, "children": [],
                          "unavailable": {"tokens": "Synthetic test, no model call", "aggregate_agent_seconds": "Synthetic test"}},
            "execution": {"coverage": "COMPLETE", "evidence": ["observation.json"]},
            "assessment": [{"criterion": k, "status": "UNKNOWN", "evidence": [], "reason": "No real assessment in a unit fixture"}
                           for k in scenarios[scenario]["criteria"]],
            "comparison": {"comparability": "COMPARABLE", "decision": "Unknown", "verification": [], "reason": "Unit fixture only"},
            "limitations": ["Synthetic fixture, never empirical evidence."], "qore_run": None,
        }
        self.observation(run)
        return run

    def observation(self, run):
        at = "2026-10-17T06:00:30Z"
        packet = {"schema": "qore-eval-evidence/1", "run_id": run["id"], "candidate_sha256": run["candidate_sha256"],
                  "input_manifest_sha256": run["input_manifest_sha256"], "observed_at": at,
                  "payload": {"synthetic": True, "no_real_execution": True}}
        evaluate.write(self.root / "observation.json", packet)
        run["artifacts"] = [{"path": "observation.json", "sha256": evaluate.digest(self.root / "observation.json"),
                             "kind": "execution", "observed_at": at}]

    def check(self, run):
        evaluate.write(self.root / "record.json", run)
        return evaluate.check_record(self.root / "record.json", self.root)

    def test_baseline_does_not_need_qore_phases(self):
        result = self.check(self.baseline())
        self.assertTrue(result["valid"])
        self.assertEqual(result["coverage"], "COMPLETE")

    def qualification(self, run, coverage="PARTIAL"):
        packet = {"schema": "qore-eval-qualification/1", "run_id": run["id"],
                  "candidate_sha256": run["candidate_sha256"],
                  "input_manifest_sha256": run["input_manifest_sha256"],
                  "qore_run_sha256": None, "declared_coverage": run["execution"]["coverage"],
                  "coverage": coverage, "assessor": "unit-assessor", "verifier": "unit-verifier",
                  "assessed_at": "2026-10-17T06:02:00Z", "reason": "Synthetic missing required observation",
                  "evidence": ["observation.json"]}
        self.save_qualification(run, packet)
        run["comparison"]["comparability"] = "UNVERIFIED"
        return packet

    def save_qualification(self, run, packet):
        evaluate.write(self.root / "qualification.json", packet)
        descriptor = {"path": "qualification.json", "sha256": evaluate.digest(self.root / "qualification.json"), "kind": "presentation"}
        run["artifacts"] = [a for a in run["artifacts"] if a["path"] != "qualification.json"] + [descriptor]
        run["qualification"] = {k: descriptor[k] for k in ("path", "sha256")}

    def test_independent_restriction_preserves_original_declaration(self):
        run = self.baseline()
        before = copy.deepcopy(run["execution"])
        self.qualification(run)
        checked = self.check(run)
        self.assertEqual(checked["coverage"], "PARTIAL")
        self.assertEqual(checked["declared_coverage"], "COMPLETE")
        self.assertTrue(checked["qualification_supplied"])
        self.assertEqual(run["execution"], before)

    def test_qualification_rejects_other_identity_or_promotion(self):
        run = self.baseline()
        run["execution"].update(coverage="PARTIAL", reason="Synthetic missing phase")
        packet = self.qualification(run, "COMPLETE")
        with self.assertRaisesRegex(ValueError, "cannot promote"):
            self.check(run)
        packet.update(coverage="PARTIAL", run_id="other-trial")
        self.save_qualification(run, packet)
        with self.assertRaisesRegex(ValueError, "another trial"):
            self.check(run)

    def test_qualification_requires_separate_actors_and_existing_evidence(self):
        run = self.baseline()
        packet = self.qualification(run)
        packet["verifier"] = packet["assessor"]
        self.save_qualification(run, packet)
        with self.assertRaisesRegex(ValueError, "separate non-execution"):
            self.check(run)
        packet.update(verifier="unit-verifier", evidence=["missing.json"])
        self.save_qualification(run, packet)
        with self.assertRaisesRegex(ValueError, "undeclared evidence"):
            self.check(run)

    def test_restricted_execution_cannot_keep_success_or_comparability(self):
        run = self.baseline()
        self.qualification(run)
        run["assessment"][0].update(status="MET", evidence=["observation.json"])
        with self.assertRaisesRegex(ValueError, "Incomplete method"):
            self.check(run)
        run["assessment"][0]["status"] = "UNKNOWN"
        run["comparison"]["comparability"] = "COMPARABLE"
        with self.assertRaisesRegex(ValueError, "Missing phases"):
            self.check(run)

    def test_summary_uses_restricted_coverage_and_retains_declared_count(self):
        run = self.baseline()
        self.qualification(run)
        self.check(run)
        series = self.empty_series()
        cell = next(c for c in series["cells"] if (c["scenario_id"], c["condition"]) == ("R2", "baseline"))
        cell.update(status="PARTIAL", records=["record.json"])
        path = self.root / "series.json"
        evaluate.write(path, series)
        result = evaluate.summarize(path, self.root / "summary")
        self.assertEqual(result["attempted_cells"], 1)
        self.assertEqual(result["completed_cells"], 0)
        self.assertEqual(result["declared_complete_cells"], 1)
        self.assertEqual(result["qualified_cells"], 1)

    def test_all_conditions_have_equal_authoritative_facts_without_answers(self):
        bundles = [self.prepared(c, "R1") for c in evaluate.CONDITIONS]
        for relative in ("surface-contract.json", "checks/check_contract.py", "observation-policy.json", "target/verification-protocol.md"):
            self.assertEqual(len({evaluate.digest(p / "worker" / relative) for p in bundles}), 1)
        for bundle in bundles:
            names = [p.relative_to(bundle / "worker").as_posix() for p in (bundle / "worker").rglob("*") if p.is_file()]
            self.assertFalse(any(n.startswith(("docs/", ".git/", "evals/", "profiles/")) for n in names))
            self.assertFalse(any("protocol-corrected" in n for n in names))
        self.assertFalse((bundles[0] / "worker/.agents").exists())
        profile = next((bundles[2] / "worker/.agents/skills").glob("*/references/project.json"))
        self.assertEqual(evaluate.read_json(profile)["id"], "qaizen-labs")

    def test_derivative_is_autonomous_and_sourced_to_staged_files(self):
        bundle = self.prepared("derived", "U1")
        profile = next((bundle / "worker/.agents/skills").glob("*/references/project.json"))
        context = importlib.import_module("context")
        checked = context.validate_profile(evaluate.read_json(profile), bundle / "worker", "ux")
        self.assertEqual(checked["coverage"], "COMPLETE")
        self.assertTrue(any(f["id"] == "back-focus" for f in checked["invariants"]))

    def test_existing_output_is_preserved(self):
        path = self.prepared()
        original = (path / "input-manifest.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "Output exists"):
            evaluate.prepare("R2", "baseline", path)
        self.assertEqual((path / "input-manifest.json").read_bytes(), original)

    def test_mutated_input_invalidates_comparison_without_erasing_evidence(self):
        run = self.baseline()
        changed = self.root / "R2-baseline/worker/surface-contract.json"
        changed.write_text("{}")
        with self.assertRaisesRegex(ValueError, "Changed inputs require INVALID"):
            self.check(run)
        run["comparison"]["comparability"] = "INVALID"
        self.assertIn("surface-contract.json", self.check(run)["changed_inputs"])
        self.assertEqual(changed.read_text(), "{}")

    def test_unlisted_worker_file_is_not_silently_accepted(self):
        run = self.baseline()
        (self.root / "R2-baseline/worker/previous-answer.md").write_text("Leaked solution")
        with self.assertRaisesRegex(ValueError, "Changed inputs require INVALID"):
            self.check(run)

    def test_evidence_from_another_trial_is_rejected(self):
        run = self.baseline()
        p = self.root / "observation.json"
        packet = evaluate.read_json(p); packet["run_id"] = "different-run"
        evaluate.write(p, packet); run["artifacts"][0]["sha256"] = evaluate.digest(p)
        with self.assertRaisesRegex(ValueError, "belongs to another trial"):
            self.check(run)

    def test_old_evidence_and_altered_evidence_are_rejected(self):
        run = self.baseline()
        run["artifacts"][0]["observed_at"] = "2026-10-16T00:00:00Z"
        with self.assertRaisesRegex(ValueError, "outside this trial"):
            self.check(run)
        run["artifacts"][0]["observed_at"] = "2026-10-17T06:00:30Z"
        (self.root / "observation.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "Altered evidence"):
            self.check(run)

    def test_escape_and_symlink_evidence_are_rejected(self):
        run = self.baseline()
        run["artifacts"][0]["path"] = "../outside.json"
        with self.assertRaisesRegex(ValueError, "escapes"):
            self.check(run)
        run["artifacts"][0]["path"] = "linked.json"
        (self.root / "linked.json").symlink_to(self.root / "observation.json")
        with self.assertRaisesRegex(ValueError, "Symlinked"):
            self.check(run)

    def rebind_manifest(self, run):
        manifest_path = self.root / run["input_manifest"]
        run["input_manifest_sha256"] = evaluate.digest(manifest_path)
        self.observation(run)

    def test_updated_manifest_cannot_whitelist_an_old_answer(self):
        run = self.baseline()
        folder = self.root / "R2-baseline"
        answer = folder / "worker/previous-answer.md"
        answer.write_text("Old evaluator answer: claim success")
        manifest = evaluate.read_json(folder / "input-manifest.json")
        manifest["resources"].append({"path": "previous-answer.md", "sha256": evaluate.digest(answer)})
        evaluate.write(folder / "input-manifest.json", manifest)
        self.rebind_manifest(run)
        with self.assertRaisesRegex(ValueError, "Frozen worker resource closure"):
            self.check(run)

    def test_updated_manifest_cannot_replace_the_frozen_task(self):
        run = self.baseline()
        folder = self.root / "R2-baseline"
        task = folder / "worker/TASK.md"
        task.write_text("Previous evaluator answer: report every criterion MET")
        manifest = evaluate.read_json(folder / "input-manifest.json")
        next(r for r in manifest["resources"] if r["path"] == "TASK.md")["sha256"] = evaluate.digest(task)
        evaluate.write(folder / "input-manifest.json", manifest)
        self.rebind_manifest(run)
        with self.assertRaisesRegex(ValueError, "Frozen worker resource closure"):
            self.check(run)

    def test_contained_symlink_roots_and_ancestors_are_refused(self):
        run = self.baseline()
        folder = self.root / "R2-baseline"
        (folder / "worker").rename(folder / "actual-worker")
        (folder / "worker").symlink_to(folder / "actual-worker", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "Symlinked"):
            self.check(run)
        (folder / "worker").unlink()
        (folder / "actual-worker").rename(folder / "worker")
        (self.root / "evidence").mkdir()
        (self.root / "observation.json").rename(self.root / "evidence/observation.json")
        (self.root / "alias").symlink_to(self.root / "evidence", target_is_directory=True)
        run["artifacts"][0]["path"] = "alias/observation.json"
        run["execution"]["evidence"] = ["alias/observation.json"]
        run["environment"]["isolation"]["evidence"] = ["alias/observation.json"]
        with self.assertRaisesRegex(ValueError, "Symlinked"):
            self.check(run)

    def test_children_must_be_inside_the_trial_and_counted(self):
        run = self.baseline()
        run["resources"]["children"] = [{"actor_id": "child", "started_at": "2026-10-17T05:00:00Z", "ended_at": "2026-10-17T07:00:00Z"}]
        run["resources"]["aggregate_agent_seconds"] = 0
        with self.assertRaisesRegex(ValueError, "outside the trial"):
            self.check(run)
        run["resources"]["children"][0].update(started_at="2026-10-17T06:00:00Z", ended_at="2026-10-17T06:00:30Z")
        with self.assertRaisesRegex(ValueError, "omits measured child"):
            self.check(run)
        run["resources"]["aggregate_agent_seconds"] = 30
        self.assertTrue(self.check(run)["valid"])

    def generic_qore_record(self, scenario="R2", condition="generic"):
        run = self.baseline(condition, scenario)
        module = importlib.import_module("run_contract")
        phases = sorted(module.PHASES["review"])
        profile = None
        if condition == "derived":
            profile_path = next((self.root / (scenario + "-derived/worker/.agents/skills")).glob("*/references/project.json"))
            p = evaluate.read_json(profile_path)
            profile = {"id": p["id"], "version": p["version"], "sha256": evaluate.digest(profile_path)}
            phases.append("profile_preflight")
        qroot = self.root / "qore"
        qroot.mkdir()
        qrun = {"schema": "qore-run/1", "id": run["id"], "method": "review", "skill": "qore-review" + ("-qaizen-labs" if condition == "derived" else ""),
                "candidate_sha256": run["candidate_sha256"], "target": {"label": "Synthetic unit fixture", "snapshot_sha256": run["input_manifest_sha256"]},
                "last_relevant_change": "2026-10-16T00:00:00Z", "environment": {"id": "unit", "host": run["environment"]["host"], "operator": run["environment"]["operator"]},
                "profile": profile, "required_phases": phases, "phases": [], "artifacts": [], "commands": [], "limitations": ["Synthetic, no real Qore execution"], "coverage": "COMPLETE"}
        for name in phases:
            actor = "unit-" + name if name.startswith("finder.") or name == "verifier" else "unit-parent"
            if actor != "unit-parent":
                run["resources"]["children"].append({"actor_id": actor, "started_at": run["resources"]["started_at"], "ended_at": run["resources"]["ended_at"]})
            at = "2026-10-17T06:00:30Z"
            packet = {"qore_evidence": {"candidate_sha256": run["candidate_sha256"], "target_snapshot_sha256": run["input_manifest_sha256"], "observed_at": at, "phase_id": name}, "payload": {"synthetic": True}}
            path = name + ".json"
            evaluate.write(qroot / path, packet)
            qrun["phases"].append({"id": name, "actor_id": actor, "status": "PASS", "artifacts": [path]})
            qrun["artifacts"].append({"path": path, "sha256": evaluate.digest(qroot / path), "kind": "execution", **{k: packet["qore_evidence"][k] for k in ("candidate_sha256", "target_snapshot_sha256", "observed_at")}})
        run["resources"]["aggregate_agent_seconds"] = 240
        evaluate.write(qroot / "execution.json", qrun)
        run["qore_run"] = {"path": "qore/execution.json", "sha256": evaluate.digest(qroot / "execution.json")}
        return run, qrun

    def test_actual_qore_trial_binding_has_positive_and_old_phase_controls(self):
        run, qrun = self.generic_qore_record()
        self.assertTrue(self.check(run)["valid"])
        for artifact in qrun["artifacts"]:
            artifact["observed_at"] = "2026-10-16T06:00:30Z"
            path = self.root / "qore" / artifact["path"]
            packet = evaluate.read_json(path)
            packet["qore_evidence"]["observed_at"] = artifact["observed_at"]
            evaluate.write(path, packet); artifact["sha256"] = evaluate.digest(path)
        evaluate.write(self.root / "qore/execution.json", qrun)
        run["qore_run"]["sha256"] = evaluate.digest(self.root / "qore/execution.json")
        with self.assertRaisesRegex(ValueError, "outside the current trial"):
            self.check(run)

    def test_qore_identity_and_actors_belong_to_current_trial(self):
        run, qrun = self.generic_qore_record()
        qrun["id"] = "old-trial"
        evaluate.write(self.root / "qore/execution.json", qrun)
        run["qore_run"]["sha256"] = evaluate.digest(self.root / "qore/execution.json")
        with self.assertRaisesRegex(ValueError, "another trial"):
            self.check(run)

    def test_excluded_missing_pilot_or_outcome_selection_is_rejected(self):
        packet = self.empty_series()
        packet["excluded_pilot"] = [{"scenario_id": "R1", "condition": c, "reason": "Unfavorable result", "record": "missing-" + c + ".json"} for c in evaluate.CONDITIONS]
        evaluate.write(self.root / "series.json", packet)
        with self.assertRaisesRegex(ValueError, "never outcome selection"):
            evaluate.summarize(self.root / "series.json", self.root / "summary")
        for item in packet["excluded_pilot"]:
            item["exclusion_basis"] = "PROTOCOL_CHANGED"
        evaluate.write(self.root / "series.json", packet)
        with self.assertRaisesRegex(ValueError, "Required file is missing"):
            evaluate.summarize(self.root / "series.json", self.root / "summary")

    def test_valid_excluded_pilot_is_checked_and_retained_in_both_outputs(self):
        import shutil
        packet = self.empty_series()
        packet["excluded_pilot"] = []
        for condition in evaluate.CONDITIONS:
            case = EvaluationTests(); case.setUp(); self.addCleanup(case.doCleanups)
            run = case.baseline(condition, "R1") if condition == "baseline" else case.generic_qore_record("R1", condition)[0]
            self.assertTrue(case.check(run)["valid"])
            folder = self.root / ("pilot-" + condition)
            shutil.copytree(case.root, folder)
            replacement = {**run["environment"], "host": "synthetic-replacement-host"}
            change = {"schema": "qore-eval-change/1", "kind": "SETUP_CHANGED", "before_sha256": evaluate.identity(run["environment"]),
                      "after_sha256": evaluate.identity(replacement), "after_environment": replacement, "reason": "Synthetic setup replacement control"}
            evaluate.write(folder / "change.json", change)
            packet["excluded_pilot"].append({"scenario_id": "R1", "condition": condition, "record": folder.name + "/record.json",
                "sha256": evaluate.digest(folder / "record.json"), "reason": "Synthetic setup replacement control", "exclusion_basis": "SETUP_CHANGED",
                "change_evidence": {"path": folder.name + "/change.json", "sha256": evaluate.digest(folder / "change.json")}})
        evaluate.write(self.root / "series.json", packet)
        result = evaluate.summarize(self.root / "series.json", self.root / "summary")
        self.assertEqual(len(result["excluded_pilot"]), 3)
        self.assertEqual(result["coverage"], "BLOCKED")
        markdown = (self.root / "summary/summary.md").read_text()
        for condition in evaluate.CONDITIONS:
            self.assertIn("pilot-" + condition + "/record.json", markdown)
        self.assertIn("Synthetic setup replacement control", markdown)

    def test_missing_independence_or_phase_cannot_be_comparable(self):
        run = self.baseline()
        run["environment"]["isolation"] = {"status": "UNVERIFIED", "evidence": []}
        with self.assertRaisesRegex(ValueError, "Missing isolation"):
            self.check(run)
        run["execution"] = {"coverage": "PARTIAL", "evidence": [], "reason": "No qualified isolation"}
        with self.assertRaisesRegex(ValueError, "prevent comparability"):
            self.check(run)
        run["comparison"]["comparability"] = "UNVERIFIED"
        self.assertEqual(self.check(run)["coverage"], "PARTIAL")

    def test_missing_usage_is_not_zero_and_requires_explanation(self):
        run = self.baseline()
        del run["resources"]["unavailable"]["tokens"]
        with self.assertRaisesRegex(ValueError, "Unavailable usage reason"):
            self.check(run)

    def test_qore_record_is_required_only_in_qore_conditions(self):
        run = self.baseline()
        run["qore_run"] = {"path": "invented.json", "sha256": "0" * 64}
        with self.assertRaisesRegex(ValueError, "Baseline must not invent"):
            self.check(run)

    def test_malformed_packets_unknown_schema_and_duplicate_keys_fail(self):
        path = self.root / "bad.json"
        for body in ("{}", "null", '{"schema":"qore-eval-run/2"}', '{"schema":"qore-eval-run/1","schema":"other"}'):
            path.write_text(body)
            with self.assertRaises((ValueError, TypeError)):
                evaluate.check_record(path, self.root)

    def test_not_run_series_has_no_fake_results_or_winner(self):
        packet = self.empty_series()
        packet["scenarios_sha256"] = evaluate.configuration()[2]
        evaluate.write(self.root / "series.json", packet)
        result = evaluate.summarize(self.root / "series.json", self.root / "summary")
        self.assertEqual(result["coverage"], "BLOCKED")
        self.assertEqual(result["completed_cells"], 0)
        self.assertEqual(len(result["cells"]), 18)
        self.assertFalse(any("assessment" in row for row in result["cells"]))
        with self.assertRaisesRegex(ValueError, "Output exists"):
            evaluate.summarize(self.root / "series.json", self.root / "summary")

    def test_missing_or_duplicate_series_cells_are_rejected(self):
        packet = self.empty_series()
        packet["scenarios_sha256"] = evaluate.configuration()[2]
        packet["cells"][1] = copy.deepcopy(packet["cells"][0])
        evaluate.write(self.root / "series.json", packet)
        with self.assertRaisesRegex(ValueError, "duplicate series cell"):
            evaluate.summarize(self.root / "series.json", self.root / "summary")


if __name__ == "__main__":
    unittest.main()
