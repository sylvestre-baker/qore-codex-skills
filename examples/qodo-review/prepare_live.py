#!/usr/bin/env python3
"""Prepare the exact public historical review tree without contacting Qodo."""
import argparse
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
BASE = "a4fef83aadd6610435da5ac0cc7e53b34fe1dd4f"
FIX = "d67673097e41d5e4c4fd02241c9f0c392cdac1f5"
TREE = "c10015840a872caf200164d69aa650b6d0bda8b5"
ORIGIN = "https://github.com/sylvestre-baker/qore-codex-skills"


def git(*argv, cwd):
    result = subprocess.run(["git", *map(str, argv)], cwd=cwd, capture_output=True, text=True, timeout=60)
    if result.returncode:
        raise ValueError("Git prerequisite or preparation failed: " + result.stderr.strip())
    return result.stdout.strip()


def prepare(output):
    for ref in [BASE, FIX]:
        git("cat-file", "-e", ref + "^{commit}", cwd=REPO)
    if git("rev-parse", FIX + "^{tree}", cwd=REPO) != TREE:
        raise ValueError("Historical source tree does not match")
    if output.exists() or output.is_symlink():
        raise ValueError("Output exists; choose an unused directory")
    output.mkdir(parents=True)
    output = output.resolve()
    target = output / "target"
    target.mkdir()
    git("init", "--quiet", cwd=target)
    # A local Git transport copies objects. No alternates or author-only path is retained.
    git("fetch", "--quiet", "--no-tags", "--no-write-fetch-head", REPO, BASE, FIX, cwd=target)
    git("checkout", "--quiet", "--detach", BASE, cwd=target)
    git("read-tree", "--reset", "-u", FIX, cwd=target)
    git("remote", "add", "origin", ORIGIN, cwd=target)
    if git("write-tree", cwd=target) != TREE or git("diff", "--name-only", cwd=target):
        raise ValueError("Prepared index/worktree does not match the recorded correction")
    (output / "review-context.json").write_bytes((HERE / "review-context.json").read_bytes())
    record = {"schema": "qore-qodo-live-preparation/1", "base_commit": BASE, "source_fix_commit": FIX,
              "source_fix_tree": TREE, "changed_files": len(git("diff", "--name-only", BASE, cwd=target).splitlines()),
              "origin": ORIGIN, "qodo_submitted": False,
              "effects": "New isolated public-code Git tree and context only; source checkout unchanged; no network request or Qodo call.",
              "limit": "A shallow or source-archive checkout may lack historical Git objects. Use a full clone; this script never fetches a remote automatically."}
    (output / "preparation.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({**record, "target": str(target), "context": str(output / "review-context.json")}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        prepare(args.output)
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        parser.exit(2, "Preparation refused: " + str(error) + "\n")
