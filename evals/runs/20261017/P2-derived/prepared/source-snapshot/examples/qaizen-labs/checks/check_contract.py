#!/usr/bin/env python3
"""Check the public journey contract; never contact the website."""
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit


def validate(data):
    if not isinstance(data, dict) or data.get("schema") != "qaizen-labs-surface/1":
        raise ValueError("Expected qaizen-labs-surface/1")
    entry = urlsplit(data["entry_url"])
    origin = entry.scheme + "://" + entry.netloc
    if entry.scheme != "https" or entry.username or entry.password or origin not in data["allowed_origins"]:
        raise ValueError("Entry must have an explicitly authorized HTTPS origin")
    scope = data["scope"]
    if scope["answer_policy"] != "unanswered" or set(scope["allowed_methods"]) != {"GET", "HEAD", "OPTIONS"}:
        raise ValueError("The observation must remain read-only and unanswered")
    states = data["states"]
    if not isinstance(states, list) or len(states) != len(set(states)) or not states:
        raise ValueError("State IDs must be nonempty and unique")
    by_id = {}
    for transition in data["transitions"]:
        key = transition["id"]
        if key in by_id or transition["from"] not in states or transition["to"] not in states:
            raise ValueError("Duplicate transition or unknown state: " + key)
        if not transition["control"] or not transition["activation"]:
            raise ValueError("Every transition needs a control and activation")
        if transition.get("focus_after") and transition["focus_after"] not in data["focus_targets"]:
            raise ValueError("Unknown focus target: " + key)
        by_id[key] = transition
    close, back = by_id["close-help"], by_id["back"]
    if close.get("focus_after") != "summary" or back.get("focus_after") != "introduction-heading":
        raise ValueError("Close and Back require different focus destinations")
    if back.get("traversal") not in ("Tab", "Shift+Tab") or back["activation"] != "Enter":
        raise ValueError("Back requires sequential keyboard traversal and observed activation")
    required = data["required_checks"]
    if not isinstance(required, list) or len(required) != len(set(required)) or not {"keyboard-back", "unanswered", "close-focus", "introduction-focus", "read-only-policy", "origin-policy"}.issubset(required):
        raise ValueError("Missing or duplicate required checks")
    if data["provenance"]["kind"] != "public-observation-and-declared-acceptance" or not data["provenance"]["urls"]:
        raise ValueError("Public provenance and observation/expectation distinction are required")
    return {"valid": True, "schema": data["schema"], "checks": required,
            "limit": "Contract consistency only; browser observations establish current behavior."}


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("Usage: python3 -B checks/check_contract.py surface-contract.json")
        result = validate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
        print(json.dumps(result, indent=2))
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(json.dumps({"valid": False, "error": str(error)}), file=sys.stderr)
        sys.exit(1)
