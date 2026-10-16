#!/usr/bin/env python3
"""Check every published execution, retaining narrowly pinned cache exclusions."""
import argparse
from copy import deepcopy
import json
from pathlib import Path, PurePosixPath
import sys

sys.dont_write_bytecode = True
from context import digest, read_json
from run_contract import validate_run


def check_record(path, exception=None):
    run = read_json(path)
    excluded = []
    if exception is not None:
        if digest(path) != exception.get("execution_sha256") or not exception.get("reason"):
            raise ValueError("Cache exception does not match the unchanged execution record")
        exclusions = exception.get("excluded_source_artifacts")
        if not isinstance(exclusions, list) or not exclusions:
            raise ValueError("Cache exception needs an explicit nonempty artifact list")
        by_path = {a["path"]: a for a in run["artifacts"]}
        referenced = {ref for phase in run["phases"] for ref in phase["artifacts"]}
        seen = set()
        for item in exclusions:
            name = item["path"]
            pure = PurePosixPath(name)
            if (name in seen or pure.is_absolute() or ".." in pure.parts or "\\" in name
                    or "__pycache__" not in pure.parts or pure.suffix != ".pyc"
                    or name in referenced or by_path.get(name) != {**item, "kind": "source"}):
                raise ValueError("Only exact unreferenced source caches may be excluded: " + name)
            seen.add(name)
            if not (path.parent / name).is_file():
                excluded.append(item)
    if not excluded:
        result = validate_run(run, path.parent)
        return {"record": path.parent.name, "status": "PASS", **result}
    # Never modify or relabel the historical record. Check all remaining obligations
    # on an in-memory view and report this record as incomplete, not a strict pass.
    remaining = deepcopy(run)
    absent = {item["path"] for item in excluded}
    remaining["artifacts"] = [a for a in remaining["artifacts"] if a["path"] not in absent]
    checked = validate_run(remaining, path.parent)
    return {"record": path.parent.name, "status": "KNOWN_EXCEPTION", "coverage": "PARTIAL",
            "strict_validation": "BLOCKED", "remaining_phase_coverage": checked["coverage"],
            "checked_artifact_count": checked["artifact_count"], "excluded_source_artifacts": excluded,
            "reason": exception["reason"]}


def check_records(directory, policy):
    if not isinstance(policy, dict) or policy.get("schema") != "qore-execution-exceptions/1" or not isinstance(policy.get("records"), dict):
        raise ValueError("Expected qore-execution-exceptions/1 policy")
    paths = sorted(directory.glob("*/execution.json"))
    if not paths:
        raise ValueError("No published execution records found")
    if set(policy["records"]) - {path.parent.name for path in paths}:
        raise ValueError("Exception names an unknown execution record")
    results = [check_record(path, policy["records"].get(path.parent.name)) for path in paths]
    return {"policy_check_passed": True, "records": results,
            "strict_passes": sum(row["status"] == "PASS" for row in results),
            "known_exceptions": sum(row["status"] == "KNOWN_EXCEPTION" for row in results),
            "limit": "An accepted cache exception is PARTIAL historical evidence, never a complete strict validation."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    try:
        root = args.root / "docs/evidence"
        print(json.dumps(check_records(root / "executions", read_json(root / "execution-exceptions.json")), indent=2))
        return 0
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(json.dumps({"policy_check_passed": False, "error": str(error)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
