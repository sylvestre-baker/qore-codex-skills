"""Check literal Gherkin arguments and outline tables through the public entrypoint."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "skills/qore-plan/scripts/spec-lint.sh"


class SpecBoundaryTests(unittest.TestCase):
    def check_spec(self, body, coverage="AC01 -> US1"):
        # A longer outer fence permits backtick Gherkin docstrings as literal lines.
        source = (
            "<!-- qore-spec/1 -->\n~~~~gherkin\nFeature: Literal boundaries\n"
            + body
            + "\n~~~~\nCoverage: " + coverage
            + "\n```mermaid\nsequenceDiagram\n  Reader->>Checker: Validate\n```\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "spec.md"
            path.write_text(source, encoding="utf-8")
            result = subprocess.run(
                ["bash", str(ENTRY), str(path), "--json"],
                text=True, capture_output=True, timeout=10,
            )
            return result.returncode, json.loads(result.stdout)

    def test_docstring_keywords_cannot_supply_executable_steps(self):
        for marker in ('"""', "```"):
            with self.subTest(marker=marker):
                body = (
                    "  Scenario: AC01 Literal argument\n    Given a message\n"
                    f"      {marker}\n      When this is literal text\n"
                    f"      Then this is literal text\n      {marker}"
                )
                code, report = self.check_spec(body)
                self.assertEqual(code, 1)
                missing = [p["message"] for p in report["problems"] if p["code"] == "step"]
                self.assertTrue(any("when" in message for message in missing))
                self.assertTrue(any("then" in message for message in missing))

    def test_literal_scenarios_and_examples_do_not_change_the_parse(self):
        for marker in ('"""', "```"):
            with self.subTest(marker=marker):
                body = (
                    "  Scenario: AC01 A complete scenario\n    Given a message\n"
                    f"      {marker}text/plain\n      Scenario: AC99 Only literal\n"
                    "      When literal text\n      Then literal text\n      Examples:\n"
                    f"      {marker}\n    When checked\n    Then accepted"
                )
                code, report = self.check_spec(body)
                self.assertEqual(code, 0, report)
                self.assertEqual([s["id"] for s in report["scenarios"]], ["AC01"])

    def test_keyword_substrings_in_literal_text_are_not_steps(self):
        code, report = self.check_spec(
            '  Scenario: AC01 Literal control\n    Given a message\n      """\n'
            '      LiteralWhen is text\n      LiteralThen is text\n      """'
        )
        self.assertEqual(code, 1)
        self.assertEqual(sum(p["code"] == "step" for p in report["problems"]), 2)

    def test_unclosed_docstrings_are_rejected_even_with_real_steps(self):
        for marker in ('"""', "```"):
            with self.subTest(marker=marker):
                code, report = self.check_spec(
                    "  Scenario: AC01 Unclosed argument\n    Given a message\n"
                    f"    When checked\n    Then accepted\n      {marker}\n      payload"
                )
                self.assertEqual(code, 1)
                self.assertTrue(any(p["code"] == "docstring" for p in report["problems"]))

    def test_the_other_docstring_delimiter_does_not_close_an_argument(self):
        code, report = self.check_spec(
            '  Scenario: AC01 Mismatched delimiter\n    Given a message\n'
            '    When checked\n    Then accepted\n      """\n      payload\n      ```'
        )
        self.assertEqual(code, 1)
        self.assertTrue(any(p["code"] == "docstring" for p in report["problems"]))

    def test_outline_without_examples_is_rejected(self):
        for message in ("<message>", "ordinary text"):
            with self.subTest(message=message):
                code, report = self.check_spec(
                    f"  Scenario Outline: AC01 Parameterized\n    Given {message}\n"
                    "    When checked\n    Then accepted"
                )
                self.assertEqual(code, 1)
                self.assertTrue(any(p["code"] == "examples" for p in report["problems"]))

    def test_examples_need_both_header_and_data_row(self):
        for table in ("", "      | message |", "      |   |\n      | value |"):
            with self.subTest(table=table):
                code, report = self.check_spec(
                    "  Scenario Outline: AC01 Missing examples\n    Given <message>\n"
                    "    When checked\n    Then accepted\n    Examples:\n" + table
                )
                self.assertEqual(code, 1)
                self.assertTrue(any(p["code"] == "examples" for p in report["problems"]))

    def test_each_outline_owns_its_examples(self):
        code, report = self.check_spec(
            "  Scenario Outline: AC01 Complete\n    Given <message>\n    When checked\n"
            "    Then accepted\n    Examples:\n      | message |\n      | value |\n"
            "  Scenario Outline: AC02 Missing examples\n    Given <message>\n"
            "    When checked\n    Then accepted", "AC01 AC02 -> US1"
        )
        self.assertEqual(code, 1)
        self.assertTrue(any("AC02" in p["message"] and p["code"] == "examples" for p in report["problems"]))

    def test_populated_outline_preserves_placeholders_and_empty_input_values(self):
        code, report = self.check_spec(
            '  Scenario Outline: AC01 Parameterized\n    Given <message>\n      """\n'
            '      A literal <message> with When and Then\n      """\n'
            "    When checked\n    Then <result>\n    Examples: Normal and empty input\n"
            "      | message | result |\n      | hello | accepted |\n      | | rejected |"
        )
        self.assertEqual(code, 0, report)

    def test_every_examples_section_requires_population(self):
        code, report = self.check_spec(
            "  Scenario Outline: AC01 Two sections\n    Given <message>\n    When checked\n"
            "    Then accepted\n    Examples: Populated\n      | message |\n      | value |\n"
            "    Examples: Empty\n      | message |"
        )
        self.assertEqual(code, 1)
        self.assertTrue(any(p["code"] == "examples" for p in report["problems"]))


if __name__ == "__main__":
    unittest.main()
