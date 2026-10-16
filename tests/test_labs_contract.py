"""Exercise public contract and profile consumers against altered source data."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from context import validate_profile

spec = importlib.util.spec_from_file_location("labs_contract", ROOT / "examples/qaizen-labs/checks/check_contract.py")
checker = importlib.util.module_from_spec(spec); spec.loader.exec_module(checker)


class LabsContractTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "examples/qaizen-labs/surface-contract.json").read_text())

    def test_declared_contract_is_consistent_without_network(self):
        self.assertTrue(checker.validate(self.data)["valid"])

    def test_wrong_states_focus_origin_answer_and_keyboard_fail(self):
        for mutate in (
            lambda d: d["transitions"][0].update(to="missing"),
            lambda d: d["transitions"][-1].update(focus_after="summary"),
            lambda d: d["transitions"][-1].update(traversal="click"),
            lambda d: d.update(allowed_origins=["https://example.com"]),
            lambda d: d["scope"].update(answer_policy="submit"),
        ):
            data = copy.deepcopy(self.data); mutate(data)
            with self.assertRaises(ValueError): checker.validate(data)

    def test_all_three_methods_consume_current_facts_and_detect_staleness(self):
        profile = json.loads((ROOT / "profiles/qaizen-labs.json").read_text())
        example = ROOT / "examples/qaizen-labs"
        for method in ("plan", "review", "ux"):
            result = validate_profile(profile, example, method)
            self.assertEqual(result["coverage"], "COMPLETE")
            self.assertIn("back-focus", {fact["id"] for fact in result["invariants"]})
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp); (target / "checks").mkdir()
            for relative in ("surface-contract.json", "checks/check_contract.py"):
                (target / relative).write_bytes((example / relative).read_bytes())
            (target / "surface-contract.json").write_text('{}')
            for method in ("plan", "review", "ux"):
                result = validate_profile(profile, target, method)
                self.assertNotEqual(result["coverage"], "COMPLETE")
                self.assertNotIn("back-focus", {fact["id"] for fact in result["invariants"]})
