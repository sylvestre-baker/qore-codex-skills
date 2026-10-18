"""Exercise observable tutorial outcomes and preservation/refusal paths."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/qodo-review"


class QodoTutorialTests(unittest.TestCase):
    def invoke(self, example, output, env=None):
        return subprocess.run([sys.executable, "-B", str(example / "reproduce.py"), "--output", str(output)],
                              capture_output=True, text=True, env=env, timeout=30)

    def test_focused_replay_distinguishes_historical_current_and_input_artifact(self):
        if not shutil.which("node"):
            self.skipTest("Node.js is required for the actual validator replay")
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "run"
            result = self.invoke(EXAMPLE, output)
            self.assertEqual(result.returncode, 0, result.stderr)
            evidence = json.loads((output / "observations.json").read_text())
            self.assertTrue(evidence["matches_recorded_observations"])
            self.assertNotIn(str(Path.home()) + "/", (output / "observations.json").read_text())
            self.assertEqual({r["argv"][0] for r in evidence["commands"]}, {"python3", "node"})
            self.assertEqual([(r["snapshot"], r["coverage"], r["exit_code"]) for r in evidence["profile_preflight"]],
                             [("base", "COMPLETE", 0), ("historical", "BLOCKED", 2), ("current", "COMPLETE", 0)])
            self.assertEqual(evidence["text_summary"]["json_verdict"], "PENDING")
            self.assertEqual(evidence["text_summary"]["json_unresolved_findings"], ["F1"])
            self.assertTrue(all(not r["slice_approval_matches"] and r["complete_fix_approval_matches"] for r in evidence["hash_boundary"]))

    def test_existing_output_is_preserved(self):
        if not shutil.which("node"):
            self.skipTest("Node.js is a prerequisite")
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "run"
            output.mkdir()
            marker = output / "local-adaptation.txt"
            marker.write_bytes(b"Keep my work.\n")
            result = self.invoke(EXAMPLE, output)
            self.assertEqual(result.returncode, 2)
            self.assertIn("Output exists", result.stderr)
            self.assertEqual(marker.read_bytes(), b"Keep my work.\n")
            self.assertEqual(list(output.iterdir()), [marker])

    def test_changed_snapshot_is_refused_before_output_creation(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            copied = root / "example"
            shutil.copytree(EXAMPLE, copied)
            with (copied / "snapshots/historical-project-check.py").open("a") as stream:
                stream.write("\nraise RuntimeError('Changed source must never execute')\n")
            result = self.invoke(copied, root / "run")
            self.assertEqual(result.returncode, 2)
            self.assertIn("Changed source", result.stderr)
            self.assertFalse((root / "run").exists())

    def test_unlisted_or_escaping_source_is_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            copied = root / "example"
            shutil.copytree(EXAMPLE, copied)
            sources = json.loads((copied / "sources.json").read_text())
            sources["resources"][0]["path"] = "../outside.py"
            (copied / "sources.json").write_text(json.dumps(sources))
            result = self.invoke(copied, root / "run")
            self.assertEqual(result.returncode, 2)
            self.assertIn("five declared public sources", result.stderr)
            self.assertFalse((root / "run").exists())

    def test_missing_node_is_an_explicit_prerequisite_gap(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "run"
            result = self.invoke(EXAMPLE, output, env={**os.environ, "PATH": folder})
            self.assertEqual(result.returncode, 2)
            self.assertIn("Node.js is required", result.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
