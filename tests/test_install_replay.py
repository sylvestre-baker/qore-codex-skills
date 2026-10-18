"""Reject a false success when the diagnostic replay recommends an unsafe retry."""
import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


class InstallReplayTests(unittest.TestCase):
    def test_diagnostic_retry_advice_must_be_checked_before_pass(self):
        source = Path(__file__).resolve().parents[1] / "docs/evidence/install-recovery/replay/reproduce.py"
        spec = importlib.util.spec_from_file_location("qore_install_replay", source)
        replay = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(replay)
        actual_diagnostic = replay.diagnostic_case

        def unsafe_advice(*args, **kwargs):
            result = actual_diagnostic(*args, **kwargs)
            if result["packet"]["error"] == "PRIMARY_COPY_DENIED":
                result["packet"]["recovery"]["safe_to_retry"] = True
            return result

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "result"
            with patch.object(replay, "diagnostic_case", side_effect=unsafe_advice), \
                 patch.object(sys, "argv", ["qore-install-replay", "--output", str(output)]), \
                 contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(AssertionError, "Diagnostic recovery must not be marked safe to retry"):
                    replay.main()
            self.assertFalse((output / "result.json").exists())


if __name__ == "__main__":
    unittest.main()
