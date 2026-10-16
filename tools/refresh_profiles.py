#!/usr/bin/env python3
"""Refresh the two maintained example profiles from their explicit local sources."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def refresh(name, source, project_id):
    path = ROOT / source
    config = json.loads(path.read_text())
    profile = {
        "schema": "qore-project/1", "id": project_id, "version": "0.1.0",
        "sources": [{"id": "project", "path": source, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}],
        "commands": [{"id": "check", "argv": config["check"], "source": "project", "applies_to": ["plan", "review"]}],
        "invariants": [{"id": key, "statement": text, "source": "project", "applies_to": [method]}
                       for (key, text), method in zip(config["invariants"].items(), ("plan", "review", "ux"))],
        "surfaces": {"web": {**config["fixture"], "source": "project", "applies_to": ["ux"]}},
    }
    output = ROOT / "profiles" / name
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(profile, indent=2) + "\n")
    return str(output.relative_to(ROOT))


if __name__ == "__main__":
    print(json.dumps({"refreshed": [refresh("qore.json", "qore.json", "qore"),
          refresh("contrast.json", "tests/fixtures/project-alternate.json", "qore-contrast")]}))
