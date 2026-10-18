#!/usr/bin/env python3
"""Replay recorded installation and diagnostic cases using only bundled Python sources."""
import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path, PurePosixPath
import stat
import sys
import tempfile
from unittest.mock import patch
import zipfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def extract_checked(archive, destination):
    with zipfile.ZipFile(archive) as source:
        for item in source.infolist():
            name = PurePosixPath(item.filename)
            if name.is_absolute() or ".." in name.parts or "\\" in item.filename:
                raise ValueError("Unsafe archive member: " + item.filename)
            if stat.S_ISLNK(item.external_attr >> 16):
                raise ValueError("Archive symlinks are refused")
        source.extractall(destination)


def installation_case(qore, bundle, base):
    base.mkdir()
    project = base / "project"
    project.mkdir()
    policy = project / ".agents/skills/local-policy/SKILL.md"
    policy.parent.mkdir(parents=True)
    policy.write_text("Preserve this local policy.\n")
    original = qore.shutil.copytree

    def fail_second(source, destination, *args, **kwargs):
        if Path(source).name == "qore-review":
            raise PermissionError("Controlled second-skill copy failure")
        return original(source, destination, *args, **kwargs)

    with patch.object(qore.shutil, "copytree", side_effect=fail_second):
        try:
            qore.install(bundle, project)
            raise AssertionError("The injected failure did not execute")
        except (OSError, ValueError) as error:
            failure = {"error": str(error), "recovery": getattr(error, "recovery", None)}
    folders = sorted(path.name for path in (project / ".agents/skills").iterdir())
    try:
        installed = qore.install(bundle, project)
        retry = {"success": True, "installed": [Path(p).name for p in installed["installed"]],
                 "differences": qore.compare(bundle, project)["changes"]}
    except (OSError, ValueError) as error:
        retry = {"success": False, "error": str(error)}
    control = base / "control"
    control.mkdir()
    installed = qore.install(bundle, control)
    return {"failure": failure, "folders_after_failure": folders, "retry": retry,
            "normal_control": {"installed": [Path(p).name for p in installed["installed"]],
                               "differences": qore.compare(bundle, control)["changes"]},
            "unrelated_policy_preserved": policy.read_text() == "Preserve this local policy.\n"}


def diagnostic_case(qore, bundle, project):
    project.mkdir()
    original_rglob = Path.rglob

    def copy_failure(*args, **kwargs):
        raise PermissionError("PRIMARY_COPY_DENIED")

    def scan_failure(path, pattern, *args, **kwargs):
        if path.name.startswith("qore-") and path.parent.name.startswith(".qore-install-"):
            raise PermissionError("SECONDARY_SCAN_DENIED")
        return original_rglob(path, pattern, *args, **kwargs)

    output = io.StringIO()
    argv = ["qore", "install", "--source", str(bundle), "--project-root", str(project)]
    with patch.object(qore.shutil, "copytree", side_effect=copy_failure), \
         patch.object(Path, "rglob", scan_failure), patch.object(sys, "argv", argv), \
         contextlib.redirect_stderr(output):
        exit_code = qore.main()
    return {"exit_code": exit_code, "packet": json.loads(output.getvalue())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New results directory; never overwritten")
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Output already exists; preserve it and choose a new directory")
    provenance = json.loads((HERE / "provenance.json").read_text())
    for item in provenance["runtime_files"]:
        file = HERE / item["path"]
        if sha256(file) != item["sha256"]:
            raise ValueError("Bundled input digest differs: " + item["path"])
    args.output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="qore-review-replay-") as temporary:
        base = Path(temporary)
        extract_checked(HERE / "qore-source-c3ce75c.zip", base / "source")
        source = base / "source/qore-skills-0.2.1"
        sys.path.insert(0, str(source / "tools"))
        final = module("qore_candidate", source / "tools/qore.py")
        final.verify(source)
        package = final.build(base / "build", scope="skills")
        bundle = Path(package["bundle"])
        before = module("qore_baseline", HERE / "historical/baseline-qore.py")
        reviewed = module("qore_reviewed", HERE / "historical/reviewed-qore.py")
        cases = {
            "installation_before": installation_case(before, bundle, base / "before"),
            "installation_after": installation_case(final, bundle, base / "after"),
            "diagnostic_before": diagnostic_case(reviewed, bundle, base / "diagnostic-before"),
            "diagnostic_after": diagnostic_case(final, bundle, base / "diagnostic-after"),
        }
        assert cases["installation_before"]["retry"]["success"] is False
        after = cases["installation_after"]
        assert after["retry"]["success"] and len(after["retry"]["installed"]) == 3
        assert after["retry"]["differences"] == []
        assert after["failure"]["recovery"]["safe_to_retry"] is True
        assert after["failure"]["recovery"]["retained_paths"] == []
        for key in ["installation_before", "installation_after"]:
            assert cases[key]["unrelated_policy_preserved"]
            assert len(cases[key]["normal_control"]["installed"]) == 3
            assert cases[key]["normal_control"]["differences"] == []
        assert cases["diagnostic_before"]["packet"]["error"] == "SECONDARY_SCAN_DENIED"
        diagnostic = cases["diagnostic_after"]["packet"]
        assert diagnostic["error"] == "PRIMARY_COPY_DENIED"
        assert any("SECONDARY_SCAN_DENIED" in entry["error"] for entry in diagnostic["recovery"]["cleanup_errors"])
        record = {"schema": "qore-offline-review-replay/1", "status": "PASS", "cases": cases,
                  "source_identities": provenance["source_identities"],
                  "candidate_installer_sha256": sha256(source / "tools/qore.py"),
                  "bundle_manifest_sha256": package["manifest_sha256"],
                  "python": sys.version.split()[0],
                  "limits": ["Controlled injected failures, not a customer incident.",
                             "Historical code is executed only in temporary projects.",
                             "No Qodo call, network access, personal installation or source checkout is needed.",
                             "No crash, power-loss, hostile-concurrency or whole-product guarantee."]}
        # Replace only ephemeral execution locations; no account paths are emitted.
        encoded = json.dumps(record, indent=2).replace(str(base), "<TEMP>") + "\n"
        (args.output / "result.json").write_text(encoded)
        print(encoded)


if __name__ == "__main__":
    main()
