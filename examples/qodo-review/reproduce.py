#!/usr/bin/env python3
"""Replay three scoped Qodo observations locally; never call a remote service."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
EXPECTED_SOURCES = {
    "snapshots/base-project-check.py", "snapshots/historical-project-check.py",
    "snapshots/current-project-check.py", "snapshots/finding-lint.mjs",
    "snapshots/findings.md.txt",
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_sources():
    sources = read(HERE / "sources.json")
    rows = sources.get("resources", [])
    if len(rows) != len(EXPECTED_SOURCES) or {r.get("path") for r in rows} != EXPECTED_SOURCES:
        raise ValueError("The replay needs exactly the five declared public sources")
    for row in rows:
        path = HERE / row["path"]
        if path.is_symlink() or not path.resolve().is_relative_to(HERE) or not path.is_file():
            raise ValueError("Missing or escaping source: " + row["path"])
        if digest(path) != row.get("sha256"):
            raise ValueError("Changed source: " + row["path"])
    return sources


def replay(output):
    sources = verify_sources()
    node = shutil.which("node")
    if node is None:
        raise ValueError("Node.js is required; the replay does not install it")
    if output.exists() or output.is_symlink():
        raise ValueError("Output exists; choose an unused directory")
    output.mkdir(parents=True)
    output = output.resolve()
    commands = []
    checks = []

    def normalize(value):
        return str(value).replace(str(output), "OUTPUT").replace(str(HERE), "EXAMPLE")

    def run(argv):
        completed = subprocess.run([str(arg) for arg in argv], cwd=HERE,
                                   capture_output=True, text=True, timeout=30)
        display_args = [normalize(arg) for arg in argv]
        display_args[0] = "python3" if str(argv[0]) == sys.executable else "node" if str(argv[0]) == node else display_args[0]
        row = {"argv": display_args, "exit_code": completed.returncode,
               "stdout": normalize(completed.stdout), "stderr": normalize(completed.stderr)}
        commands.append(row)
        return row

    project = output / "project"
    project.mkdir()
    policy = b"Tutorial fixture: project facts must be current before use.\n"
    (project / "policy.txt").write_bytes(policy)
    profile = {
        "schema": "qore-project/1", "id": "tutorial", "version": "1.0.0",
        "sources": [{"id": "policy", "path": "policy.txt", "sha256": hashlib.sha256(policy).hexdigest()}],
        "commands": [], "invariants": [{"id": "current-facts", "source": "policy",
                                          "statement": "Project facts must be current before use."}],
        "surfaces": {},
    }
    write(project / "profile.json", profile)
    profile_rows = []
    for label in ["base", "historical", "current"]:
        references = output / label / "references"
        write(references / "project.json", profile)
        # Labeled fixture for the generic-manifest condition, not a rebuilt package.
        write(references / "release.json", {"schema": "qore-release/1", "profile": None, "resources": []})
        helper = HERE / "snapshots" / (label + "-project-check.py")
        direct = run([sys.executable, "-B", helper, project / "profile.json", "--root", project, "--method", "review"])
        bundled = run([sys.executable, "-B", helper, references / "project.json", "--root", project, "--method", "review"])
        try:
            direct_packet = json.loads(direct["stdout"])
            packet = json.loads(bundled["stdout"] or bundled["stderr"])
        except (ValueError, TypeError):
            direct_packet, packet = {}, {}
        expected_exit = 2 if label == "historical" else 0
        expected_coverage = "BLOCKED" if label == "historical" else "COMPLETE"
        ok = direct["exit_code"] == 0 and direct_packet.get("coverage") == "COMPLETE"
        ok = ok and bundled["exit_code"] == expected_exit and packet.get("coverage") == expected_coverage
        checks.append({"id": "profile-" + label, "matches_expected_observation": ok})
        profile_rows.append({"snapshot": label, "exit_code": bundled["exit_code"], "coverage": packet.get("coverage"),
                             "direct_profile_control_exit": direct["exit_code"], "problems": packet.get("problems", [])})

    packet = HERE / "unresolved-finding.json"
    helper = HERE / "snapshots/finding-lint.mjs"
    text = run([node, helper, packet, "--verifier=ran"])
    machine = run([node, helper, packet, "--verifier=ran", "--json"])
    try:
        machine_packet = json.loads(machine["stdout"])
    except ValueError:
        machine_packet = {}
    text_ok = text["exit_code"] == machine["exit_code"] == 0 and "F1" not in text["stdout"]
    text_ok = text_ok and "PENDING" in text["stdout"] and machine_packet.get("verdict") == "PENDING"
    text_ok = text_ok and machine_packet.get("coverage") == "PARTIAL" and machine_packet.get("unresolved_findings") == ["F1"]
    checks.append({"id": "text-summary", "matches_expected_observation": text_ok})

    hash_rows = []
    for row in sources["hash_boundary"]:
        path = row.get("replay_path")
        if path not in EXPECTED_SOURCES:
            raise ValueError("Unexpected hash-boundary source")
        actual = digest(HERE / path)
        slice_matches = actual == row["slice_retained_base_approved_sha256"]
        complete_matches = actual == row["complete_fix_approved_sha256"]
        hash_rows.append({"path": row["source_path"], "actual_sha256": actual,
                          "slice_approval_matches": slice_matches, "complete_fix_approval_matches": complete_matches})
    hashes_ok = len(hash_rows) == 2 and all(not r["slice_approval_matches"] and r["complete_fix_approval_matches"] for r in hash_rows)
    checks.append({"id": "selection-hash-boundary", "matches_expected_observation": hashes_ok})

    matched = all(row["matches_expected_observation"] for row in checks)
    observations = {
        "schema": "qore-qodo-focused-replay/1", "observed_at": datetime.now(timezone.utc).isoformat(),
        "sources_sha256": digest(HERE / "sources.json"), "runner_sha256": digest(Path(__file__)),
        "fixture_findings_sha256": digest(packet), "snapshots": sources["snapshots"],
        "environment": {"python": sys.version.split()[0], "node": run([node, "--version"])["stdout"].strip(), "platform": sys.platform},
        "profile_preflight": profile_rows,
        "text_summary": {"stdout": text["stdout"], "json_verdict": machine_packet.get("verdict"),
                         "json_coverage": machine_packet.get("coverage"), "json_unresolved_findings": machine_packet.get("unresolved_findings")},
        "hash_boundary": hash_rows, "checks": checks, "matches_recorded_observations": matched,
        "commands": commands,
        "limits": ["New focused local replay, not a new Qodo run or the original private execution.",
                   "Synthetic current policy/profile and a minimal generic-manifest fixture, not a full release integrity check or installed derivative.",
                   "The --verifier=ran token is test input to a structural helper, not evidence of a fresh independent review in this replay.",
                   "Hash comparisons are narrower than executing the package builder.",
                   "Recorded executable paths are normalized to python3/node; EXAMPLE/OUTPUT are local path labels, not replayable absolute paths.",
                   "No network, login, commands supplied by a project profile, source edit or external publication."],
    }
    write(output / "observations.json", observations)
    for row in profile_rows:
        print("Profile " + row["snapshot"] + ": " + str(row["coverage"]) + ", exit " + str(row["exit_code"]))
    print("Text: " + str(machine_packet.get("verdict")) + "; unresolved ID F1 appears in JSON")
    print("Hashes: " + str(sum(not r["slice_approval_matches"] for r in hash_rows)) + " slice mismatches; " +
          str(sum(not r["complete_fix_approval_matches"] for r in hash_rows)) + " complete-fix mismatches")
    print("Recorded observations match: " + str(matched).lower())
    print("Evidence: " + str(output / "observations.json"))
    return 0 if matched else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="An unused local directory")
    args = parser.parse_args()
    try:
        raise SystemExit(replay(args.output))
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        parser.exit(2, "Replay refused: " + str(error) + "\n")
