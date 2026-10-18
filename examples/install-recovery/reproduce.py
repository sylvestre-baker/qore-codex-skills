"""Replay the same controlled second-skill copy failure and normal control."""
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

import argparse
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[2])
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
repo = args.source.resolve()
args.output.mkdir(parents=True, exist_ok=False)
sys.path.insert(0, str(repo / "tools"))
qore = importlib.import_module("qore")
with tempfile.TemporaryDirectory() as temporary:
    base = Path(temporary)
    package = qore.build(base / "build", scope="skills")
    bundle = Path(package["bundle"])
    project = base / "project"
    project.mkdir()
    unrelated = project / ".agents/skills/local-policy/SKILL.md"
    unrelated.parent.mkdir(parents=True)
    unrelated.write_text("Preserve this local policy.\n")
    real_copy = qore.shutil.copytree

    def fail_second(source, destination, *args, **kwargs):
        if Path(source).name == "qore-review":
            raise PermissionError("Controlled second-skill copy failure")
        return real_copy(source, destination, *args, **kwargs)

    failure = None
    with patch.object(qore.shutil, "copytree", side_effect=fail_second):
        try:
            qore.install(bundle, project)
        except (OSError, ValueError) as error:
            failure = {"type": type(error).__name__, "message": str(error), "recovery": getattr(error, "recovery", None)}
    leftovers = sorted(p.name for p in (project / ".agents/skills").iterdir())
    retry = None
    try:
        result = qore.install(bundle, project)
        retry = {"success": True, "installed": [Path(p).name for p in result["installed"]], "differences": qore.compare(bundle, project)["changes"]}
    except (OSError, ValueError) as error:
        retry = {"success": False, "error": str(error)}
    control = base / "control"
    control.mkdir()
    result = qore.install(bundle, control)
    record = {"source_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True).stdout.strip() or None, "installer_sha256": hashlib.sha256((repo / "tools/qore.py").read_bytes()).hexdigest(), "bundle_manifest_sha256": package["manifest_sha256"], "failure": failure, "folders_after_failure": leftovers, "retry": retry, "normal_control": {"installed": [Path(p).name for p in result["installed"]], "differences": qore.compare(bundle, control)["changes"]}, "unrelated_policy_preserved": unrelated.read_text() == "Preserve this local policy.\n", "limit": "Controlled failure injection, not an observed customer incident."}
    (args.output / "result.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))
