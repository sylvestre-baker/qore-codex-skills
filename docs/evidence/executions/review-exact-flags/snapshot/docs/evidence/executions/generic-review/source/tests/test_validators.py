"""Exercise validator decisions through their public Node/shell entry points."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/validators"


class ValidatorTests(unittest.TestCase):
    def invoke(self, method, script, value, *flags, raw=False):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input"
            path.write_text(value if raw else json.dumps(value), encoding="utf-8")
            entry = ROOT / "skills" / method / "scripts" / script
            command = ["bash" if script.endswith(".sh") else "node", str(entry), str(path), *flags]
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            output = json.loads(result.stdout) if result.stdout.strip() else None
            return result.returncode, output, result.stderr

    def review(self, value, verifier="ran", raw=False):
        return self.invoke("qore-review", "finding-lint.mjs", value, f"--verifier={verifier}", "--json", raw=raw)

    def candidate(self, **changes):
        finding = {"id": "F1", "title": "Candidate", "severity": "high", "verdict": "PLAUSIBLE", "evidence": "src/input.ts:12"}
        finding.update(changes)
        return {"findings": [finding]}

    def ux(self, value):
        return self.invoke("qore-ux-review", "stop-rule.mjs", value)

    def ux_packet(self):
        return json.loads((FIXTURES / "valid-ux.json").read_text())

    def spec(self, value):
        return self.invoke("qore-plan", "spec-lint.sh", value, "--json", raw=True)

    def spec_text(self):
        return (FIXTURES / "valid-spec.md").read_text()

    def depth(self, depth, files, **extra):
        return self.invoke("qore-ux-review", "depth-lint.mjs", {"depth": depth, "changed_files": files, **extra})

    def test_positive_spec(self):
        code, result, _ = self.spec(self.spec_text())
        self.assertEqual(code, 0)
        self.assertEqual([item["id"] for item in result["scenarios"]], ["A01"])

    def test_positive_review_retains_refutations_and_blocks_confirmed_high(self):
        code, result, _ = self.review((FIXTURES / "valid-findings.json").read_text(), raw=True)
        self.assertEqual(code, 0)
        self.assertEqual(result["blocking_findings"], ["F1"])
        self.assertEqual(result["verdict"], "DO-NOT-SHIP")
        self.assertIn("refuted_because", result["findings"][1])

    def test_positive_ux(self):
        code, result, _ = self.ux(self.ux_packet())
        self.assertEqual((code, result["coverage"], result["verdict"]), (0, "COMPLETE", "SHIP"))

    def test_empty_null_array_and_missing_envelope_are_refused(self):
        for value in [{}, None, [], {"findings": None}, {"findings": {}}]:
            with self.subTest(value=value):
                code, result, _ = self.review(value)
                self.assertEqual(code, 1)
                self.assertFalse(result["valid"])
                self.assertNotEqual(result["verdict"], "SHIP")

    def test_truncated_json_is_not_an_empty_review(self):
        code, result, _ = self.review((FIXTURES / "truncated.json").read_text(), raw=True)
        self.assertEqual(code, 2)
        self.assertIsNone(result)

    def test_empty_findings_is_a_valid_complete_packet(self):
        code, result, _ = self.review({"findings": []})
        self.assertEqual((code, result["total"], result["coverage"]), (0, 0, "COMPLETE"))

    def test_duplicate_ids_and_non_object_findings_are_refused(self):
        packet = self.candidate()
        packet["findings"].append(copy.deepcopy(packet["findings"][0]))
        self.assertEqual(self.review(packet)[0], 1)
        self.assertEqual(self.review({"findings": [None]})[0], 1)

    def test_unknown_verdict_and_severity_are_refused(self):
        self.assertEqual(self.review(self.candidate(verdict="MAYBE"))[0], 1)
        self.assertEqual(self.review(self.candidate(severity="urgent"))[0], 1)

    def test_skipped_verifier_preserves_high_and_critical_severity(self):
        for severity in ["high", "critical"]:
            code, result, _ = self.review(self.candidate(severity=severity), "skipped")
            self.assertEqual(code, 0)
            self.assertEqual(result["findings"][0]["severity"], severity)
            self.assertEqual(result["coverage"], "PARTIAL")
            self.assertEqual(result["blocking_findings"], [])
            self.assertNotEqual(result["verdict"], "SHIP")

    def test_missing_verifier_never_proves_or_refutes(self):
        for verdict in ["CONFIRMED", "REFUTED"]:
            code, result, _ = self.review(self.candidate(verdict=verdict, counterexample="zero produces Infinity", refuted_because="handled at src/a.ts:2"), "skipped")
            self.assertEqual(code, 1)
            self.assertFalse(result["valid"])

    def test_blocking_findings_need_counterexample_and_checkable_evidence(self):
        self.assertEqual(self.review(self.candidate(verdict="CONFIRMED"))[0], 1)
        self.assertEqual(self.review(self.candidate(evidence="This might be slow"))[0], 1)
        self.assertEqual(self.review(self.candidate(verdict="REFUTED"))[0], 1)

    def test_measurements_and_source_identifiers_remain_accepted(self):
        for evidence in ["340 requests for 20 rows", "git show 3427dcc lists docs/spec.md", "jsdom 29.1.1 behavior"]:
            self.assertEqual(self.review(self.candidate(evidence=evidence))[0], 0)

    def test_redactor_allowlist_drops_unanticipated_rationale(self):
        packet = self.candidate(rationale="Private rationale", novel_field={"analysis": "More rationale"}, counterexample="zero -> Infinity")
        code, result, _ = self.invoke("qore-review", "redact-for-verifier.mjs", packet, "--json")
        self.assertEqual(code, 0)
        self.assertEqual(set(result["findings"][0]), {"id", "title", "severity", "evidence", "counterexample"})
        self.assertEqual(result["findings"][0]["evidence"], "src/input.ts:12")

    def test_redactor_refuses_bad_envelope_and_nested_allowed_field(self):
        for packet in [{}, None, [], {"findings": [{"id": "x"}]}, self.candidate(title=""), self.candidate(severity="urgent"), self.candidate(evidence={"rationale": "Hidden"})]:
            self.assertEqual(self.invoke("qore-review", "redact-for-verifier.mjs", packet)[0], 2)

    def test_spec_version_must_be_first_and_known(self):
        source = self.spec_text()
        self.assertEqual(self.spec("\n" + source)[0], 1)
        self.assertEqual(self.spec(source.replace("qore-spec/1", "qore-spec/2"))[0], 1)

    def test_empty_fence_cannot_borrow_steps_outside(self):
        source = self.spec_text().replace("```gherkin\n", "```gherkin\n```\n", 1)
        self.assertEqual(self.spec(source)[0], 1)

    def test_each_scenario_requires_its_own_three_step_types(self):
        source = self.spec_text().replace("```\n\nCoverage:", "  Scenario: A02 Missing action\n    Given another input\n    Then a result\n```\n\nCoverage:", 1).replace("A01 -> US1", "A01 A02 -> US1")
        code, result, _ = self.spec(source)
        self.assertEqual(code, 1)
        self.assertTrue(any(problem["code"] == "step" for problem in result["problems"]))
        self.assertEqual(self.spec(self.spec_text().replace("When independent", "And independent"))[0], 1)

    def test_spec_duplicate_ids_and_orphan_coverage_fail(self):
        source = self.spec_text()
        scenario = "  Scenario: A01 Duplicate\n    Given input\n    When checked\n    Then done\n"
        self.assertEqual(self.spec(source.replace("```\n\nCoverage:", scenario + "```\n\nCoverage:", 1))[0], 1)
        self.assertEqual(self.spec(source.replace("A01 -> US1", "A01 A99 -> US1"))[0], 1)

    def test_spec_requires_coverage_and_fenced_sequence(self):
        self.assertEqual(self.spec(self.spec_text().replace("Coverage:", "Trace:"))[0], 1)
        self.assertEqual(self.spec(self.spec_text().replace("sequenceDiagram", "flowchart LR"))[0], 1)
        self.assertEqual(self.spec(self.spec_text().replace("A01 -> US1 / D1.", "A01."))[0], 1)

    def test_spec_supports_named_scenarios_and_bold_coverage(self):
        source = self.spec_text().replace("A01 Preserve", "Preserve").replace("Coverage: A01", "**Coverage:** Scenario 1")
        self.assertEqual(self.spec(source)[0], 0)

    def test_required_skipped_gate_prevents_ship_despite_passing_score(self):
        packet = self.ux_packet()
        packet["iterations"][0]["measured"].remove("GP")
        packet["iterations"][0]["skipped"] = {"GP": "Measurement unavailable"}
        code, result, _ = self.ux(packet)
        self.assertEqual((code, result["coverage"]), (0, "PARTIAL"))
        self.assertNotEqual(result["verdict"], "SHIP")
        self.assertIn("GP", result["missing_gates"])

    def test_all_required_skipped_never_ship(self):
        packet = self.ux_packet()
        packet["iterations"][0].update(measured=[], skipped={gate: "Not observed" for gate in packet["in_scope"]})
        result = self.ux(packet)[1]
        self.assertEqual(result["coverage"], "PARTIAL")
        self.assertNotEqual(result["decision"], "SHIP")

    def test_missing_required_gate_is_not_treated_as_pass(self):
        packet = self.ux_packet()
        del packet["iterations"][0]["scores"]["G1"]
        packet["iterations"][0]["measured"].remove("G1")
        result = self.ux(packet)[1]
        self.assertIn("G1", result["missing_gates"])
        self.assertNotEqual(result["verdict"], "SHIP")

    def test_fixes_invalidate_same_iteration_and_carried_scores(self):
        packet = self.ux_packet()
        packet["iterations"][0]["fix_applied"] = True
        self.assertEqual(set(self.ux(packet)[1]["stale_gates"]), set(packet["in_scope"]))
        packet["iterations"].append({"n": 2, "scores": {"G0": 5, "G1": 4, "GP": 4}, "measured": ["G0", "G1"]})
        result = self.ux(packet)[1]
        self.assertEqual(result["stale_gates"], ["GP"])
        self.assertNotEqual(result["verdict"], "SHIP")
        packet["iterations"][-1]["measured"].append("GP")
        self.assertEqual(self.ux(packet)[1]["verdict"], "SHIP")

    def test_zero_gate_cannot_extend_six_iteration_budget(self):
        packet = {"in_scope": ["G1"], "iterations": [{"n": n, "scores": {"G1": 0}, "measured": ["G1"]} for n in range(1, 7)]}
        result = self.ux(packet)[1]
        self.assertEqual((result["decision"], result["verdict"], result["surface_score"]), ("STOP_CEILING", "DO-NOT-SHIP", 0))

    def test_sixth_fresh_pass_can_ship_but_seventh_cannot(self):
        packet = self.ux_packet()
        packet["iterations"][0]["n"] = 6
        self.assertEqual(self.ux(packet)[1]["verdict"], "SHIP")
        packet["iterations"][0]["n"] = 7
        self.assertEqual(self.ux(packet)[1]["decision"], "STOP_CEILING")

    def test_justified_non_applicability_is_distinct_from_tool_absence(self):
        packet = self.ux_packet()
        packet["iterations"][0]["measured"].remove("GP")
        packet["not_applicable"] = {"GP": "The static copy correction has no timing-sensitive behavior"}
        result = self.ux(packet)[1]
        self.assertEqual(result["verdict"], "SHIP")
        self.assertIn("GP", result["not_applicable"])
        packet["not_applicable"]["GP"] = "Tool unavailable"
        self.assertEqual(self.ux(packet)[0], 2)

    def test_infra_blockage_affects_coverage_without_failing_observed_gates(self):
        packet = self.ux_packet()
        packet["iterations"][0]["measured"].remove("GP")
        packet["iterations"][0]["infra_blocked"] = ["GP"]
        result = self.ux(packet)[1]
        self.assertEqual(result["coverage"], "PARTIAL")
        self.assertEqual(result["failing_gates"], [])
        self.assertNotEqual(result["verdict"], "SHIP")

    def test_ux_rejects_invalid_scores_iteration_order_and_unmeasured_change(self):
        for score in [True, "4", 6, -1, 4.5]:
            packet = self.ux_packet()
            packet["iterations"][0]["scores"]["G1"] = score
            self.assertEqual(self.ux(packet)[0], 2)
        packet = self.ux_packet()
        packet["iterations"].append({"n": 1, "scores": {}, "measured": []})
        self.assertEqual(self.ux(packet)[0], 2)
        packet["iterations"][-1].update(n=2, scores={"G1": 5})
        self.assertEqual(self.ux(packet)[0], 2)

    def test_optional_coverage_fields_do_not_silently_coerce_bad_types(self):
        for field in ["skipped", "infra_blocked", "not_applicable"]:
            for value in [None, False, ""]:
                packet = self.ux_packet()
                packet["iterations"][0][field] = value
                self.assertEqual(self.ux(packet)[0], 2)

    def test_depth_positive_source_families(self):
        for depth, files, extra in [("copy", ["src/locales/en.json"], {}), ("visual", ["src/theme.css"], {}), ("entry", ["src/routes.ts"], {}), ("full", ["src/api/service.ts"], {}), ("none", ["src/utils/parse.ts"], {"justification": "Pure calculation with no rendered output"})]:
            with self.subTest(depth=depth):
                self.assertEqual(self.depth(depth, files, **extra)[0], 0)

    def test_depth_rejects_data_as_visual_and_render_as_none(self):
        self.assertEqual(self.depth("visual", ["api/users.ts"])[0], 1)
        self.assertEqual(self.depth("copy", ["src/serializer.ts"])[0], 1)
        self.assertEqual(self.depth("none", ["src/Button.tsx"], justification="Helper")[0], 1)
        self.assertEqual(self.depth("none", ["src/utils/a.ts"])[0], 1)

    def test_route_reachability_applies_to_modern_app_and_root_paths(self):
        for file in ["pages/index.tsx", "src/routes.ts", "app/accounts/page.tsx"]:
            self.assertEqual(self.depth("state", [file])[0], 1)
            self.assertEqual(self.depth("entry", [file])[0], 0)

    def test_depth_missing_files_unknown_depth_and_bad_shape(self):
        self.assertEqual(self.depth("full", [])[0], 1)
        self.assertEqual(self.depth("unknown", ["src/a.ts"])[0], 1)
        self.assertEqual(self.invoke("qore-ux-review", "depth-lint.mjs", None)[0], 2)


if __name__ == "__main__":
    unittest.main()
