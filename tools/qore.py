#!/usr/bin/env python3
"""Build, verify and derive local Qore skill packages without overwriting installations."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import tempfile
import zipfile

sys.dont_write_bytecode = True
from context import contained, digest, read_json, validate_profile
from run_contract import validate_run

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ("qore-plan", "qore-review", "qore-ux-review")
METHODS = dict(zip(SKILLS, ("plan", "review", "ux")))
VERSION = "0.2.1"


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def files_under(root):
    files = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError("Symlinks are not permitted in a release: " + str(path.relative_to(root)))
        if path.is_file():
            files.append(path)
    return files


def check_references(skill):
    for path in files_under(skill):
        if path.suffix not in (".md", ".yaml", ".json", ".py", ".mjs", ".sh"):
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"/Users/[A-Za-z0-9_.-]+/|/home/(?!node/)[A-Za-z0-9_.-]+/|~/(?:\.claude|\.codex)/", text):
            raise ValueError("Personal path in skill: " + str(path.relative_to(skill)))
        if path.suffix == ".mjs":
            imports = re.findall(r"(?:\bfrom\s*|\bimport\s*|\b(?:import|require|fetch)\s*\(\s*)['\"]([^'\"]+)['\"]", text)
            for ref in imports:
                if ref.startswith("node:"):
                    continue
                if ref.startswith(("./", "../")):
                    target = (path.parent / ref).resolve()
                    if not target.is_relative_to(skill.resolve()) or not target.is_file():
                        raise ValueError("Missing or escaping runtime import: " + ref)
                elif "://" in ref:
                    raise ValueError("Undeclared remote runtime resource: " + ref)
        if path.suffix != ".md":
            continue
        for ref in re.findall(r"\]\(([^)]+)\)", text):
            if ref.startswith(("https://", "#")):
                continue
            if "://" in ref:
                raise ValueError("Only informational HTTPS links are permitted: " + ref)
            target = (path.parent / ref.split("#")[0]).resolve()
            if not target.is_relative_to(skill.resolve()) or not target.is_file():
                raise ValueError("Unresolved or escaping local skill reference: " + ref)


def inventory(root, exclude=()):
    rights_path = root / "release-rights.json"
    rights = {r["path"]: r for r in read_json(rights_path)["resources"]} if rights_path.is_file() else {}
    return [{"path": str(path.relative_to(root)), "sha256": digest(path),
             "origin": rights.get(str(path.relative_to(root)), {}).get("origin", "first-party"), "license": "MIT"}
            for path in files_under(root) if str(path.relative_to(root)) not in exclude]


def make_skill_manifest(skill, profile=None):
    check_references(skill)
    write_json(skill / "references/release.json", {"schema": "qore-release/1", "version": VERSION,
               "host": "codex", "profile": profile, "redistribution": "MIT-first-party",
               "resources": inventory(skill, ("references/release.json",))})


def finalize(root, kind, profile=None):
    skill_root = root / "skills" if kind == "generic" else root
    for folder in sorted(skill_root.iterdir()):
        if folder.is_dir() and folder.name.startswith("qore-"):
            make_skill_manifest(folder, profile)
    manifest = {"schema": "qore-release/1", "version": VERSION, "kind": kind,
                "host": "codex", "profile": profile, "redistribution": "MIT-first-party",
                "resources": inventory(root, ("manifest.json",))}
    write_json(root / "manifest.json", manifest)
    return manifest


def verify(root):
    root = root.resolve()
    manifest = read_json(root / "manifest.json")
    if not isinstance(manifest, dict) or manifest.get("schema") != "qore-release/1":
        raise ValueError("Unknown release schema")
    if manifest.get("kind") not in ("generic", "derived") or manifest.get("host") != "codex" or manifest.get("version") != VERSION:
        raise ValueError("Unsupported release kind, host or version")
    if manifest.get("redistribution") != "MIT-first-party":
        raise ValueError("Unknown release redistribution right")
    records = manifest.get("resources")
    if not isinstance(records, list) or not records:
        raise ValueError("Release needs an explicit resource inventory")
    expected = {"manifest.json"}
    for item in records:
        if not isinstance(item, dict) or item.get("origin") not in ("first-party", "Qaizen-public-observation") or item.get("license") != "MIT":
            raise ValueError("Unknown resource redistribution right: " + str(item.get("path") if isinstance(item, dict) else item))
        relative = item.get("path")
        if relative in expected:
            raise ValueError("Duplicate release resource: " + str(relative))
        expected.add(relative)
        path = contained(root, relative)
        if path.is_symlink() or digest(path) != item.get("sha256"):
            raise ValueError("Resource changed: " + relative)
    actual = {str(p.relative_to(root)) for p in files_under(root)}
    if expected != actual:
        raise ValueError("Release inventory differs: " + ", ".join(sorted(expected ^ actual)))
    skill_root = root / "skills" if manifest.get("kind") == "generic" else root
    for folder in skill_root.iterdir():
        if folder.is_dir() and folder.name.startswith("qore-"):
            check_references(folder)
            local = read_json(folder / "references/release.json")
            if not isinstance(local, dict) or local.get("schema") != "qore-release/1":
                raise ValueError("Unknown standalone skill schema")
            if local.get("host") != "codex" or local.get("version") != VERSION or local.get("redistribution") != "MIT-first-party":
                raise ValueError("Unsupported standalone metadata")
            for item in local["resources"]:
                if digest(contained(folder, item["path"])) != item["sha256"]:
                    raise ValueError("Standalone resource changed")
            local_expected = {item["path"] for item in local["resources"]}
            if len(local_expected) != len(local["resources"]):
                raise ValueError("Duplicate standalone resource")
            local_expected.add("references/release.json")
            if local_expected != {str(p.relative_to(folder)) for p in files_under(folder)}:
                raise ValueError("Standalone inventory is incomplete")
    return {"valid": True, "schema": "qore-release/1", "version": manifest["version"],
            "kind": manifest["kind"], "files": len(actual), "manifest_sha256": digest(root / "manifest.json")}


def build(output, scope="full"):
    if scope not in ("full", "skills"):
        raise ValueError("Unknown build scope: " + scope)
    allowlist = read_json(ROOT / "release-files.json")
    if not isinstance(allowlist, list) or not allowlist or len(allowlist) != len(set(allowlist)):
        raise ValueError("release-files.json must be an explicit unique list")
    selected = [contained(ROOT, name) for name in allowlist]
    if any(p.is_symlink() for p in selected):
        raise ValueError("Allowlisted files may not be symlinks")
    check_redistribution(ROOT, allowlist)
    if scope == "skills":
        required = {"LICENSE", "INSTALL.md", "plugin.json", "tools/qore.py", "tools/context.py", "tools/run_contract.py"}
        if not required.issubset(allowlist):
            raise ValueError("Skills-only export is missing an allowlisted installation resource")
        allowlist = [name for name in allowlist if name.startswith("skills/") or name in required]
        selected = [contained(ROOT, name) for name in allowlist]
    output.mkdir(parents=True, exist_ok=True)
    destination = output / ("qore-skills-" + VERSION + ("-skills" if scope == "skills" else ""))
    archive = output / (destination.name + ".zip")
    if destination.exists() or archive.exists():
        raise ValueError("Release destination exists; choose new staging")
    temporary = Path(tempfile.mkdtemp(prefix=".qore-build-", dir=output))
    try:
        tree = temporary / destination.name
        tree.mkdir()
        for relative, source in zip(allowlist, selected):
            target = tree / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        check_references(tree)
        finalize(tree, "generic")
        verify(tree)
        zip_path = temporary / archive.name
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for path in files_under(tree):
                item = zipfile.ZipInfo(str(Path(tree.name) / path.relative_to(tree)), date_time=(2026, 10, 15, 0, 0, 0))
                item.create_system = 3
                item.external_attr = 0o100644 << 16
                item.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(item, path.read_bytes())
        tree.rename(destination)
        zip_path.rename(archive)
    finally:
        shutil.rmtree(temporary)
    return {"bundle": str(destination), "archive": str(archive), "sha256": digest(archive), "scope": scope, **verify(destination)}


def check_redistribution(root, allowlist):
    """Check explicit maintainer attestations, not infer rights from file contents."""
    packet = read_json(root / "release-rights.json")
    if not isinstance(packet, dict) or packet.get("schema") != "qore-rights/1":
        raise ValueError("Expected explicit redistribution record qore-rights/1")
    records = packet.get("resources")
    if not isinstance(records, list):
        raise ValueError("Redistribution resources must be a list")
    expected = set(allowlist) - {"release-rights.json", "release-files.json"}
    seen = set()
    for record in records:
        if not isinstance(record, dict) or record.get("path") not in expected or record["path"] in seen:
            raise ValueError("Unexpected or duplicate redistribution resource: " + str(record.get("path") if isinstance(record, dict) else record))
        name = record["path"]
        seen.add(name)
        if record.get("status") != "approved" or record.get("license") != "MIT" or record.get("origin") not in ("first-party", "Qaizen-public-observation") or not record.get("basis"):
            raise ValueError("Unknown or unauthorized redistribution right: " + name)
        if digest(contained(root, name)) != record.get("sha256"):
            raise ValueError("Redistribution review is stale: " + name)
    if expected != seen:
        raise ValueError("Missing redistribution review: " + ", ".join(sorted(expected - seen)))
    return {"valid": True, "resources": len(seen), "limit": "Maintainer attestations require truthful rights review; hashes do not determine ownership."}


def derive(profile_path, project_root, output):
    profile = read_json(profile_path)
    for method in METHODS.values():
        result = validate_profile(profile, project_root, method)
        if result["coverage"] != "COMPLETE":
            raise ValueError("Profile is not current for " + method + ": " + "; ".join(result["problems"]))
    if output.exists():
        raise ValueError("Derived destination exists; choose new staging")
    profile_info = {"id": profile["id"], "version": profile["version"], "sha256": digest(profile_path)}
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".qore-derive-", dir=output.parent))
    tree = temporary / "candidate"
    tree.mkdir()
    try:
        for name in SKILLS:
            derived = name + "-" + profile["id"]
            target = tree / derived
            shutil.copytree(ROOT / "skills" / name, target, symlinks=True)
            for path in files_under(target):
                if path.suffix in (".md", ".yaml"):
                    text = path.read_text(encoding="utf-8").replace("$" + name, "$" + derived)
                    if path.name == "SKILL.md":
                        text = re.sub(r"(?m)^name:.*$", "name: " + derived, text, count=1)
                        text = re.sub(r"(?m)^(description:.*)$", lambda match: match[1] + " Scoped to project " + profile["id"] + ".", text, count=1)
                        text += ("\n## Generated project binding\n\nThis derivative must load [its project profile](references/project.json) before selecting project facts. "
                                 "Run its bundled project-check.py against the supplied project root with --method " + METHODS[name] +
                                 ". Consume only current returned facts; stale required context is PARTIAL or BLOCKED. "
                                 "The profile grants no action permission. Edit the maintained profile, not this generated copy.\n")
                    path.write_text(text, encoding="utf-8")
            shutil.copyfile(profile_path, target / "references/project.json")
        finalize(tree, "derived", profile_info)
        verify(tree)
        tree.rename(output)
    finally:
        shutil.rmtree(temporary)
    return {"output": str(output), "profile": profile_info, **verify(output)}


class InstallRecoveryError(OSError):
    """A handled install failure with a separate, conservative recovery result."""

    def __init__(self, error, recovery):
        super().__init__(str(error))
        self.recovery = recovery


def _install_present(path):
    """Only ENOENT means absent; permission errors must remain uncertainty."""
    try:
        path.lstat()
        return True
    except FileNotFoundError:
        return False


def _install_tree_state(root):
    """Record identities and bytes without accepting links or special files."""
    state = {}
    pending = [root]
    while pending:
        path = pending.pop()
        info = path.lstat()
        key = path.relative_to(root).as_posix()
        if stat.S_ISDIR(info.st_mode):
            state[key] = (info.st_dev, info.st_ino, "directory", stat.S_IMODE(info.st_mode))
            pending.extend(path.iterdir())
        elif stat.S_ISREG(info.st_mode):
            state[key] = (info.st_dev, info.st_ino, "file", digest(path), stat.S_IMODE(info.st_mode))
        else:
            raise ValueError("Unexpected link or special file during installation: " + str(path))
    return state


def _check_install_bytes(root, expected):
    actual = {name: row[3] for name, row in _install_tree_state(root).items() if row[2] == "file"}
    if actual != expected:
        raise ValueError("Installed or staged files differ from the verified bundle: " + root.name)


def _remove_install_tree(path, expected, *, subset=False):
    if not _install_present(path):
        return
    actual = _install_tree_state(path)
    if (not subset and actual != expected) or any(expected.get(key) != row for key, row in actual.items()):
        raise ValueError("Content or identity changed; preserve this path for manual inspection")
    shutil.rmtree(path)


def install(source, project_root):
    # Normalize lexical paths without resolving away symlink guards.
    source = Path(os.path.abspath(source))
    project_root = Path(os.path.abspath(project_root))
    verify(source)
    manifest = read_json(source / "manifest.json")
    base = source / "skills" if manifest["kind"] == "generic" else source
    candidates = [p for p in sorted(base.iterdir()) if p.is_dir() and p.name.startswith("qore-")]
    if len(candidates) != 3:
        raise ValueError("Expected exactly three skill directories")
    target = project_root / ".agents/skills"
    warnings = []
    user_skills = Path.home() / ".agents/skills"
    if user_skills.resolve() != target.resolve():
        for folder in candidates:
            existing = user_skills / folder.name
            if existing.exists() or existing.is_symlink():
                warnings.append({"code": "same-name-user-skill", "skill": folder.name, "path": str(existing),
                                 "message": "Another same-name user installation exists. Inspect the selected skill path in a fresh chat; this installer leaves it unchanged."})
    for folder in candidates:
        if _install_present(target / folder.name):
            raise ValueError("Installed destination exists; preserve it and compare a new candidate: " + folder.name)
    # Reject symlinked installation ancestors rather than writing through them.
    for ancestor in (project_root, project_root / ".agents", target):
        if ancestor.is_symlink():
            raise ValueError("Installation ancestors must not be symlinks")
    target.mkdir(parents=True, exist_ok=True)
    prefix = "skills/" if manifest["kind"] == "generic" else ""
    expected = {}
    for folder in candidates:
        start = prefix + folder.name + "/"
        expected[folder.name] = {row["path"][len(start):]: row["sha256"] for row in manifest["resources"] if row["path"].startswith(start)}
    staging = None
    staged_state = {}
    owned = []
    bookkeeping_errors = []

    def recovery_path(path):
        # Fallback staging can be outside a read-only project; report its actual
        # location relative to the supplied project rather than losing recovery.
        return os.path.relpath(path, project_root)

    def copy_owned_file(src, dst):
        destination = Path(dst)
        # Exclusive creation establishes ownership even when copying fails midway.
        descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        identity = os.fstat(descriptor)
        try:
            with os.fdopen(descriptor, "wb") as output:
                with open(src, "rb") as input_file:
                    shutil.copyfileobj(input_file, output)
            shutil.copystat(src, destination)
        finally:
            primary_active = sys.exc_info()[0] is not None
            try:
                current = destination.lstat()
                if (current.st_dev, current.st_ino) == (identity.st_dev, identity.st_ino) and stat.S_ISREG(current.st_mode):
                    staged_state[destination.relative_to(staging).as_posix()] = _install_tree_state(destination)["."]
            except (OSError, ValueError) as bookkeeping_error:
                bookkeeping_errors.append({"path": recovery_path(destination), "error": str(bookkeeping_error)})
                if not primary_active:
                    raise
        return str(destination)

    def cleanup_staging():
        if staging is not None:
            _remove_install_tree(staging, staged_state, subset=True)

    try:
        # Prefer .agents, with same-filesystem fallbacks for read-only parents.
        # Never stage inside the directory scanned for installed skills.
        allocation_error = None
        device = target.stat().st_dev
        for parent in dict.fromkeys((target.parent, project_root, Path(tempfile.gettempdir()))):
            try:
                if parent.stat().st_dev != device:
                    continue
                staging = Path(tempfile.mkdtemp(prefix=".qore-install-", dir=parent))
                break
            except PermissionError as error:
                allocation_error = error
        if staging is None:
            if allocation_error is not None:
                raise allocation_error
            raise ValueError("Staging and skill destinations must share a filesystem")
        staged_state["."] = _install_tree_state(staging)["."]
        if staging.stat().st_dev != target.stat().st_dev:
            raise ValueError("Staging and skill destinations must share a filesystem")
        for folder in candidates:
            staged = staging / folder.name
            staged.mkdir()
            staged_state[folder.name] = _install_tree_state(staged)["."]
            allowed_directories = {"."} | {p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_dir()}
            try:
                shutil.copytree(folder, staged, copy_function=copy_owned_file, dirs_exist_ok=True)
            finally:
                # copytree creates directories; only source-declared directory names
                # can become cleanup candidates inside our private staging root.
                primary_active = sys.exc_info()[0] is not None
                try:
                    for path in [staged, *staged.rglob("*")]:
                        info = path.lstat()
                        if stat.S_ISDIR(info.st_mode) and path.relative_to(staged).as_posix() in allowed_directories:
                            key = path.relative_to(staging).as_posix()
                            previous = staged_state.get(key)
                            if previous is None or previous[:2] == (info.st_dev, info.st_ino):
                                staged_state[key] = (info.st_dev, info.st_ino, "directory", stat.S_IMODE(info.st_mode))
                except (OSError, ValueError) as bookkeeping_error:
                    bookkeeping_errors.append({"path": recovery_path(staged), "error": str(bookkeeping_error)})
                    if not primary_active:
                        raise
        for folder in candidates:
            _check_install_bytes(staging / folder.name, expected[folder.name])
        # Do not rename a tree over an existing empty directory: POSIX allows it.
        for folder in candidates:
            for ancestor in (project_root, project_root / ".agents", target):
                if ancestor.is_symlink():
                    raise ValueError("Installation ancestors must not be symlinks")
            destination = target / folder.name
            destination.mkdir()  # exclusive; never merge or replace an existing root
            identity = destination.lstat()
            state = {".": (identity.st_dev, identity.st_ino, "directory", stat.S_IMODE(identity.st_mode))}
            owned.append((destination, state))
            for entry in sorted((staging / folder.name).iterdir()):
                if _install_present(destination / entry.name):
                    raise ValueError("Publication entry appeared; preserve it: " + entry.name)
                entry_state = _install_tree_state(entry)
                entry.rename(destination / entry.name)
                for relative, row in entry_state.items():
                    state[entry.name if relative == "." else entry.name + "/" + relative] = row
            _check_install_bytes(destination, expected[folder.name])
        for destination, state in owned:
            if _install_tree_state(destination) != state:
                raise ValueError("Installed content changed before completion: " + destination.name)
            _check_install_bytes(destination, expected[destination.name])
    except (OSError, ValueError) as error:
        cleanup_errors = list(bookkeeping_errors)
        for destination, state in reversed(owned):
            try:
                _remove_install_tree(destination, state)
            except (OSError, ValueError) as cleanup_error:
                cleanup_errors.append({"path": recovery_path(destination), "error": str(cleanup_error)})
        try:
            cleanup_staging()
        except (OSError, ValueError) as cleanup_error:
            cleanup_errors.append({"path": recovery_path(staging), "error": str(cleanup_error)})
        retained = []
        for path in [*(target / folder.name for folder in candidates), *([staging] if staging else [])]:
            try:
                present = _install_present(path)
            except OSError as inspection_error:
                present = True  # Unknown is retained, never an empty destination.
                cleanup_errors.append({"path": recovery_path(path), "error": str(inspection_error)})
            if present:
                retained.append(recovery_path(path))
        safe = not retained and not cleanup_errors
        recovery = {"safe_to_retry": safe, "retained_paths": retained, "cleanup_errors": cleanup_errors,
                    "next_action": "Correct the reported cause, then rerun the same install command." if safe else "Inspect the retained paths and preserve any local edits. Compare against the verified source; remove or relocate only confirmed attempt-owned content before retrying."}
        raise InstallRecoveryError(error, recovery) from error
    try:
        cleanup_staging()
    except (OSError, ValueError) as error:
        warnings.append({"code": "install-staging-retained", "path": recovery_path(staging),
                         "message": "All three skills are installed. Inspect retained private staging before manual cleanup: " + str(error)})
    return {"installed": [str(target / p.name) for p in candidates], "replaced": False, "warnings": warnings}


def snapshot(root):
    root = root.resolve()
    rows = []
    for path in sorted(root.rglob("*")):
        if any(p in (".git", "__pycache__", "dist", ".agents", ".venv") for p in path.relative_to(root).parts):
            continue
        if path.is_symlink():
            raise ValueError("Snapshot source is a symlink: " + str(path.relative_to(root)))
        if path.is_file():
            rows.append({"path": str(path.relative_to(root)), "sha256": digest(path)})
    value = hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"snapshot_sha256": value, "files": rows}


def compare(source, project_root):
    """Show candidate divergence without replacing or merging installed files."""
    verify(source)
    for ancestor in (project_root, project_root / ".agents", project_root / ".agents/skills"):
        if ancestor.is_symlink():
            raise ValueError("Installation ancestors must not be symlinks")
    manifest = read_json(source / "manifest.json")
    base = source / "skills" if manifest["kind"] == "generic" else source
    changes = []
    for folder in sorted(base.iterdir()):
        if not folder.is_dir() or not folder.name.startswith("qore-"):
            continue
        current = project_root / ".agents/skills" / folder.name
        if current.is_symlink():
            raise ValueError("Installed skill must not be a symlink: " + folder.name)
        old_files = {str(p.relative_to(current)): p for p in files_under(current)} if current.is_dir() else {}
        new_files = {str(p.relative_to(folder)): p for p in files_under(folder)}
        baseline = {}
        if "references/release.json" in old_files:
            local = read_json(old_files["references/release.json"])
            baseline = {r["path"]: r["sha256"] for r in local.get("resources", [])}
        for name in sorted(old_files.keys() | new_files.keys()):
            before = digest(old_files[name]) if name in old_files else None
            after = digest(new_files[name]) if name in new_files else None
            if before != after:
                changes.append({"skill": folder.name, "path": name, "installed_sha256": before,
                                "candidate_sha256": after, "local_adaptation": before is not None and (name not in baseline or before != baseline[name])})
    return {"changes": changes, "changed": bool(changes), "replaced": False,
            "limit": "This comparison does not merge content or authorize migration."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("build"); p.add_argument("--output", type=Path, required=True)
    p.add_argument("--scope", choices=("full", "skills"), default="full")
    p = sub.add_parser("verify"); p.add_argument("bundle", type=Path)
    p = sub.add_parser("derive")
    p.add_argument("--profile", type=Path, required=True); p.add_argument("--project-root", type=Path, required=True); p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("install")
    p.add_argument("--source", type=Path, required=True); p.add_argument("--project-root", type=Path, required=True)
    p = sub.add_parser("compare")
    p.add_argument("--source", type=Path, required=True); p.add_argument("--project-root", type=Path, required=True)
    p = sub.add_parser("snapshot"); p.add_argument("--root", type=Path, required=True)
    p = sub.add_parser("validate-run"); p.add_argument("run", type=Path); p.add_argument("--evidence-root", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "build": result = build(args.output, args.scope)
        elif args.command == "verify": result = verify(args.bundle)
        elif args.command == "derive": result = derive(args.profile, args.project_root, args.output)
        elif args.command == "install": result = install(args.source, args.project_root)
        elif args.command == "compare": result = compare(args.source, args.project_root)
        elif args.command == "snapshot": result = snapshot(args.root)
        else: result = validate_run(read_json(args.run), args.evidence_root or args.run.parent)
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, TypeError, KeyError) as exc:
        failure = {"valid": False, "error": str(exc)}
        if isinstance(exc, InstallRecoveryError):
            failure["recovery"] = exc.recovery
        print(json.dumps(failure), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
