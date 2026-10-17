#!/usr/bin/env python3
"""Check declared execution coverage and evidence identity, not decision quality."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

PHASES = {
    "plan": {"product", "architecture", "ux", "delivery", "qa", "adjudication", "spec_validation"},
    "review": {"finder.correctness", "finder.security", "finder.feasibility", "redaction", "verifier", "findings_validation"},
    "ux": {"scope", "browser", "state_transition", "freshness", "verdict"},
}
HEX = re.compile(r"[a-f0-9]{64}")


def instant(value):
    if not isinstance(value, str):
        raise ValueError("Evidence timestamps must be ISO 8601 strings")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Evidence timestamps must include a timezone")
    return parsed


def validate_run(run, evidence_root):
    if not isinstance(run, dict) or run.get("schema") != "qore-run/1":
        raise ValueError("Expected schema qore-run/1")
    for field in ("id", "skill", "candidate_sha256"):
        if not isinstance(run.get(field), str) or not run[field]:
            raise ValueError("Missing run field: " + field)
    if not HEX.fullmatch(run["candidate_sha256"]):
        raise ValueError("candidate_sha256 must be a SHA-256 digest")
    last_change = instant(run.get("last_relevant_change"))
    method = run.get("method")
    if method not in PHASES:
        raise ValueError("Unknown run method")
    target, environment = run.get("target"), run.get("environment")
    if not isinstance(target, dict) or not target.get("label") or not HEX.fullmatch(str(target.get("snapshot_sha256", ""))):
        raise ValueError("Target needs a label and snapshot_sha256")
    if not isinstance(environment, dict) or any(not environment.get(f) for f in ("id", "operator", "host")):
        raise ValueError("Environment needs id, operator and host")
    required = set(PHASES[method])
    profile = run.get("profile")
    if profile is not None:
        if not isinstance(profile, dict) or not profile.get("id") or not profile.get("version") or not HEX.fullmatch(str(profile.get("sha256", ""))):
            raise ValueError("Profile needs id, version and SHA-256")
        required.add("profile_preflight")
    supplied = run.get("required_phases")
    if not isinstance(supplied, list) or len(supplied) != len(set(supplied)) or not required.issubset(supplied):
        raise ValueError("required_phases omits a required method phase or repeats one")
    required.update(supplied)
    artifacts = run.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError("artifacts must be a list")
    available = {}
    base = Path(evidence_root).resolve()
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            raise ValueError("Artifact must be an object")
        relative = artifact.get("path", "")
        pure = PurePosixPath(relative)
        if not relative or pure.is_absolute() or ".." in pure.parts or "\\" in relative or relative in available:
            raise ValueError("Artifact path must be unique and contained")
        path = base.joinpath(*pure.parts)
        if not path.resolve().is_relative_to(base) or not path.is_file():
            raise ValueError("Artifact is missing or escapes evidence root: " + relative)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != artifact.get("sha256"):
            raise ValueError("Artifact digest mismatch: " + relative)
        if artifact.get("kind") not in ("execution", "source", "presentation"):
            raise ValueError("Artifact kind must be execution, source or presentation")
        if artifact["kind"] == "execution":
            if artifact.get("candidate_sha256") != run["candidate_sha256"] or artifact.get("target_snapshot_sha256") != target["snapshot_sha256"]:
                raise ValueError("Execution evidence belongs to another candidate or target")
            if instant(artifact.get("observed_at")) <= last_change:
                raise ValueError("Execution evidence predates the last relevant change")
            envelope = json.loads(path.read_text(encoding="utf-8"))
            identity = envelope.get("qore_evidence") if isinstance(envelope, dict) else None
            if not isinstance(identity, dict) or "payload" not in envelope:
                raise ValueError("Execution artifact needs an identity-bound JSON envelope")
            for field in ("candidate_sha256", "target_snapshot_sha256", "observed_at"):
                if identity.get(field) != artifact.get(field):
                    raise ValueError("Execution artifact identity disagrees with its descriptor")
            if not isinstance(identity.get("phase_id"), str):
                raise ValueError("Execution artifact needs phase_id")
            artifact = {**artifact, "phase_id": identity["phase_id"]}
        available[relative] = artifact
    phases = run.get("phases")
    if not isinstance(phases, list):
        raise ValueError("phases must be a list")
    by_id = {}
    for phase in phases:
        if not isinstance(phase, dict) or not phase.get("id") or phase["id"] in by_id:
            raise ValueError("Phase ids must be unique")
        if phase.get("status") not in ("PASS", "FAIL", "SKIPPED", "BLOCKED", "NOT_APPLICABLE"):
            raise ValueError("Unknown phase status")
        if not phase.get("actor_id"):
            raise ValueError("Phase needs actor_id")
        refs = phase.get("artifacts")
        if not isinstance(refs, list) or any(ref not in available for ref in refs):
            raise ValueError("Phase references an undeclared artifact")
        if phase["status"] == "PASS" and not refs:
            raise ValueError("PASS phase requires evidence")
        if phase["status"] == "PASS" and not any(available[p].get("kind") == "execution" and available[p].get("phase_id") == phase["id"] for p in refs):
            raise ValueError("PASS phase requires matching execution evidence")
        if phase["status"] != "PASS" and not phase.get("reason"):
            raise ValueError("Non-PASS phase needs an explicit reason")
        by_id[phase["id"]] = phase
    for phase_id in required:
        if by_id.get(phase_id, {}).get("status") == "NOT_APPLICABLE":
            scope = run.get("scope", {})
            phase = by_id[phase_id]
            if not (method == "ux" and phase_id == "state_transition" and
                    scope.get("depth") in ("copy", "visual", "perf") and
                    scope.get("state_transition_applicable") is False and phase["artifacts"]):
                raise ValueError("A method's mandatory phase cannot be declared non-applicable")
    if method == "review":
        finders = [p["actor_id"] for name, p in by_id.items() if name.startswith("finder.")]
        if len(finders) != len(set(finders)):
            raise ValueError("Finders require independent contexts")
        verifier = by_id.get("verifier", {}).get("actor_id")
        if verifier is not None and verifier in finders:
            raise ValueError("The verifier must be independent of the finders")
    if method == "plan":
        actors = [by_id[p]["actor_id"] for p in ("product", "architecture", "ux", "delivery", "qa") if p in by_id and by_id[p]["status"] == "PASS"]
        if len(actors) != len(set(actors)):
            raise ValueError("The five planning perspectives require distinct contexts")
    completed = [p for p in required if by_id.get(p, {}).get("status") == "PASS"]
    missing = sorted(p for p in required if by_id.get(p, {}).get("status") not in ("PASS", "NOT_APPLICABLE"))
    coverage = "COMPLETE" if not missing else ("PARTIAL" if completed else "BLOCKED")
    if run.get("coverage") != coverage:
        raise ValueError("Declared coverage differs from observed phase coverage: " + coverage)
    if not isinstance(run.get("limitations"), list) or not isinstance(run.get("commands"), list):
        raise ValueError("limitations and commands must be explicit lists")
    for command in run["commands"]:
        if not isinstance(command, dict) or not isinstance(command.get("argv"), list) or not command["argv"] or any(not isinstance(v, str) for v in command["argv"]) or type(command.get("exit_code")) is not int or command.get("artifact") not in available:
            raise ValueError("Each command needs argv, exit_code and declared artifact")
    return {"valid": True, "coverage": coverage, "missing_phases": missing,
            "artifact_count": len(available), "note": "Evidence identity and declared phase coverage checked; factual quality is not certified."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("--evidence-root", type=Path)
    args = parser.parse_args()
    try:
        result = validate_run(json.loads(args.run.read_text()), args.evidence_root or args.run.parent)
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({"valid": False, "problems": [str(exc)]}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
