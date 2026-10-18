#!/usr/bin/env python3
"""Validate sourced project facts without executing project commands."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import urlsplit

METHODS = {"plan", "review", "ux"}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def contained(root, relative, *, must_exist=True):
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ValueError("Expected a nonempty POSIX relative path")
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or ":" in pure.parts[0]:
        raise ValueError("Path escapes its declared root: " + relative)
    base = Path(root).resolve()
    candidate = base.joinpath(*pure.parts)
    if not candidate.resolve().is_relative_to(base):
        raise ValueError("Resolved path escapes its declared root: " + relative)
    if must_exist and not candidate.is_file():
        raise ValueError("Required file is missing: " + relative)
    return candidate


def validate_profile(profile, root, method):
    if method not in METHODS:
        raise ValueError("Unknown method: " + method)
    if not isinstance(profile, dict) or profile.get("schema") != "qore-project/1":
        raise ValueError("Expected schema qore-project/1")
    if not re.fullmatch(r"[a-z][a-z0-9-]{0,39}", profile.get("id", "")):
        raise ValueError("Invalid project id")
    if not re.fullmatch(r"\d+\.\d+\.\d+", profile.get("version", "")):
        raise ValueError("Project version must use three numeric components")
    sources = profile.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("Profile needs an explicit nonempty sources list")
    records, by_id = [], {}
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("Each source must be an object")
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id or source_id in by_id:
            raise ValueError("Source identifiers must be unique nonempty strings")
        expected = source.get("sha256", "")
        if not isinstance(expected, str) or not re.fullmatch(r"[a-f0-9]{64}", expected):
            raise ValueError("Source needs a SHA-256 digest: " + source_id)
        relative = source.get("path")
        path = contained(root, relative, must_exist=False)
        actual = digest(path) if path.is_file() else None
        record = {"id": source_id, "path": relative, "expected_sha256": expected,
                  "actual_sha256": actual, "current": actual == expected}
        by_id[source_id] = record
        records.append(record)
    commands, invariants, selected_sources = [], [], set()

    def applicable(fact):
        if not isinstance(fact, dict) or fact.get("source") not in by_id:
            raise ValueError("Every project fact needs a declared source")
        applies = fact.get("applies_to", sorted(METHODS))
        if not isinstance(applies, list) or not applies or set(applies) - METHODS:
            raise ValueError("Invalid applies_to methods")
        if method not in applies:
            return False
        selected_sources.add(fact["source"])
        return by_id[fact["source"]]["current"]

    for field in ("commands", "invariants"):
        if not isinstance(profile.get(field), list):
            raise ValueError(field + " must be a list")
        ids = set()
        for fact in profile[field]:
            fact_id = fact.get("id") if isinstance(fact, dict) else None
            if not isinstance(fact_id, str) or not fact_id or fact_id in ids:
                raise ValueError(field + " identifiers must be unique")
            ids.add(fact_id)
            if field == "commands":
                argv = fact.get("argv")
                if not isinstance(argv, list) or not argv or any(not isinstance(v, str) or not v or "\x00" in v for v in argv):
                    raise ValueError("Commands require an explicit nonempty argv list")
            elif not isinstance(fact.get("statement"), str) or not fact["statement"].strip():
                raise ValueError("Invariants require a statement")
            if applicable(fact):
                (commands if field == "commands" else invariants).append(fact)
    surfaces = profile.get("surfaces")
    if not isinstance(surfaces, dict):
        raise ValueError("surfaces must be an object")
    selected_surfaces = {}
    if "web" in surfaces:
        web = surfaces["web"]
        if not isinstance(web, dict):
            raise ValueError("web surface must be an object")
        url = urlsplit(web.get("entry_url", ""))
        if url.scheme not in ("http", "https") or not url.hostname or url.username or url.password:
            raise ValueError("Web entry must be an HTTP(S) URL without credentials")
        origin = url.scheme + "://" + url.netloc
        allowed = web.get("allowed_origins")
        if not isinstance(allowed, list) or origin not in allowed:
            raise ValueError("Web entry origin must be explicitly allowed")
        if not isinstance(web.get("required_state"), str) or not web["required_state"]:
            raise ValueError("Web surface needs an observable required_state")
        if web.get("kind") not in ("fixture", "application", "documentation"):
            raise ValueError("Web surface needs an explicit kind")
        if method == "ux" and applicable(web):
            selected_surfaces["web"] = web
    problems = ["Changed or missing source: " + s for s in sorted(selected_sources) if not by_id[s]["current"]]
    if method == "ux" and "web" not in selected_surfaces:
        problems.append("No current web surface is available for this profile")
    has_facts = bool(commands or invariants or selected_surfaces)
    coverage = "COMPLETE" if not problems else ("PARTIAL" if has_facts else "BLOCKED")
    return {"schema": "qore-context-check/1", "profile": {"id": profile["id"], "version": profile["version"]},
            "method": method, "coverage": coverage, "sources": records, "commands": commands,
            "invariants": invariants, "surfaces": selected_surfaces,
            "consumed_source_ids": sorted(selected_sources), "problems": problems}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--method", choices=sorted(METHODS), required=True)
    args = parser.parse_args()
    try:
        result = validate_profile(read_json(args.profile), args.root, args.method)
        result["profile"]["sha256"] = digest(args.profile)
        print(json.dumps(result, indent=2))
        return 0 if result["coverage"] == "COMPLETE" else 1
    except (ValueError, OSError, TypeError) as exc:
        print(json.dumps({"coverage": "BLOCKED", "problems": [str(exc)]}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
