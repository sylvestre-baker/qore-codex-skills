"""Exercise archive trust boundaries and fail-closed clean-room execution locally."""
import hashlib
import json
import os
from pathlib import Path
import stat
import struct
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import warnings
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/clean_room.sh"


def embedded_python(marker):
    source = SCRIPT.read_text().split("<<'" + marker + "'\n", 1)[1].split("\n" + marker, 1)[0]
    namespace = {"__name__": "clean_room_test"}
    exec(compile(source, str(SCRIPT) + ":" + marker, "exec"), namespace)
    return namespace


class CleanRoomTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.workspace = self.base / "workspace"
        self.workspace.mkdir()
        self.stage = embedded_python("STAGE_PY")["stage_archive"]
        self.identity = embedded_python("IDENTITY_PY")["read_stage"]

    def archive(self, version="0.2.1", change=None, extra=(), suffix=""):
        root = "qore-skills-" + version + suffix
        resources = {"tools/qore.py": b"# inert qualification fixture\n",
                     "skills/qore-review/SKILL.md": b"# Review fixture\n"}
        manifest = {"schema": "qore-release/1", "version": version, "kind": "generic",
                    "host": "codex", "redistribution": "MIT-first-party",
                    "resources": [{"path": name, "sha256": hashlib.sha256(data).hexdigest(),
                                   "origin": "first-party", "license": "MIT"}
                                  for name, data in resources.items()]}
        if change:
            change(manifest)
        archive = self.base / "candidate.zip"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(archive, "w") as bundle:
                bundle.writestr(root + "/manifest.json", json.dumps(manifest))
                for name, data in resources.items():
                    bundle.writestr(root + "/" + name, data)
                for name, data in extra:
                    bundle.writestr(name.replace("ROOT", root) if isinstance(name, str) else name, data)
        return archive

    def test_staging_discovers_release_versions_without_executing_code(self):
        for version, suffix in (("0.2.1", ""), ("9.7.5-build.1", "-skills")):
            with self.subTest(version=version):
                record = self.stage(self.archive(version, suffix=suffix), self.workspace)
                self.assertEqual(record["version"], version)
                self.assertEqual(Path(record["candidate_root"]).name, "qore-skills-" + version + suffix)
                self.assertEqual(record["manifest_sha256"], hashlib.sha256(
                    (Path(record["candidate_root"]) / "manifest.json").read_bytes()).hexdigest())

    def test_manifest_version_and_archive_root_must_agree(self):
        with self.assertRaisesRegex(ValueError, "root does not match"):
            self.stage(self.archive(change=lambda m: m.update(version="8.0.0")), self.workspace)
        self.assertEqual(list(self.workspace.iterdir()), [])

    def test_unknown_release_schema_and_rights_are_refused(self):
        for key, value in (("schema", "qore-release/2"), ("host", "unknown"),
                           ("redistribution", "unknown")):
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "metadata"):
                self.stage(self.archive(change=lambda m: m.update({key: value})), self.workspace)

    def test_missing_altered_duplicate_and_escaping_resources_are_refused(self):
        changes = (
            lambda m: m["resources"][0].update(sha256="0" * 64),
            lambda m: m["resources"][0].update(path="missing.py"),
            lambda m: m["resources"].append(dict(m["resources"][0])),
            lambda m: m["resources"][0].update(path="../escape.py"),
        )
        for change in changes:
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.stage(self.archive(change=change), self.workspace)
        self.assertEqual(list(self.workspace.iterdir()), [])

    def test_unsafe_and_extra_zip_entries_are_refused_before_extraction(self):
        for entry in ("ROOT/../escape", "/escape", "ROOT/./alias", "ROOT/back\\slash",
                      "ROOT/tools/qore.py", "other/file", "ROOT/unlisted.txt"):
            with self.subTest(entry=entry), self.assertRaises(ValueError):
                self.stage(self.archive(extra=[(entry, b"unexpected")]), self.workspace)
        link = zipfile.ZipInfo("ROOT/link")
        link.filename = "qore-skills-0.2.1/link"
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        with self.assertRaisesRegex(ValueError, "Unsafe"):
            self.stage(self.archive(extra=[(link, b"/outside")]), self.workspace)
        self.assertEqual(list(self.workspace.iterdir()), [])

    def test_staging_refuses_an_existing_destination(self):
        archive = self.archive()
        self.stage(archive, self.workspace)
        marker = self.workspace / "qore-skills-0.2.1/tools/qore.py"
        before = marker.read_bytes()
        with self.assertRaisesRegex(ValueError, "destination exists"):
            self.stage(archive, self.workspace)
        self.assertEqual(marker.read_bytes(), before)

    def test_expanded_size_limit_is_checked_before_reading_members(self):
        archive = self.archive()
        data = bytearray(archive.read_bytes())
        central_header = data.index(b'PK\x01\x02')
        struct.pack_into('<I', data, central_header + 24, 1_000_000_001)
        archive.write_bytes(data)
        with self.assertRaisesRegex(ValueError, 'exceeds qualification limits'):
            self.stage(archive, self.workspace)
        self.assertEqual(list(self.workspace.iterdir()), [])

    def protected_record(self):
        record = self.stage(self.archive(), self.workspace)
        record["verification"] = {"valid": True, "version": record["version"]}
        folder = self.base / "metadata"
        folder.mkdir(mode=0o755)
        metadata = folder / "stage.json"
        metadata.write_text(json.dumps(record))
        metadata.chmod(0o444)
        return metadata, record

    def root_owned(self):
        original = Path.stat
        def stat_with_root_owner(path, *args, **kwargs):
            result = original(path, *args, **kwargs)
            values = list(result)
            values[4] = 0
            return os.stat_result(values)
        return patch.object(Path, "stat", stat_with_root_owner)

    def test_run_identity_is_pinned_and_resource_changes_are_detected(self):
        metadata, record = self.protected_record()
        with self.root_owned():
            self.assertEqual(self.identity(metadata, self.workspace), record["candidate_root"])
            target = Path(record["candidate_root"]) / "tools/qore.py"
            target.write_text("changed\n")
            with self.assertRaisesRegex(ValueError, "resource changed"):
                self.identity(metadata, self.workspace)

    def test_writable_unknown_and_redirected_stage_records_are_refused(self):
        metadata, record = self.protected_record()
        with self.root_owned():
            metadata.chmod(0o666)
            with self.assertRaisesRegex(ValueError, "not protected"):
                self.identity(metadata, self.workspace)
            metadata.chmod(0o644)
            for modification in ({"unexpected": True}, {"candidate_root": str(self.base)},
                                 {"schema": "qore-clean-room-stage/2"}):
                metadata.write_text(json.dumps({**record, **modification}))
                with self.assertRaises(ValueError):
                    self.identity(metadata, self.workspace)

    def test_unlisted_post_staging_files_prevent_execution(self):
        metadata, record = self.protected_record()
        injected = Path(record['candidate_root']) / '.codex/config.toml'
        injected.parent.mkdir()
        injected.write_text('web_search="live"\n')
        with self.root_owned(), self.assertRaisesRegex(ValueError, 'inventory changed'):
            self.identity(metadata, self.workspace)

    def fake_docker(self):
        bindir = self.base / "bin"
        bindir.mkdir()
        docker = bindir / "docker"
        docker.write_text("""#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
with open(os.environ['DOCKER_CALLS'], 'a') as log:
    log.write(json.dumps(args) + '\\n')
if args[0] == 'inspect':
    value = args[-1]
    if 'Labels' in value: print('20261015')
    elif 'HostConfig' in value:
        print(json.dumps({'CapDrop':['ALL'], 'SecurityOpt':['no-new-privileges']}))
    else: print('[]')
elif 'sandbox' in args:
    print('Sandbox startup canary', file=sys.stderr)
    sys.exit(int(os.environ.get('CANARY_EXIT', '0')))
elif 'exec' in args and 'codex' in args and '--json' in args:
    print('{"type":"mock-model-invocation"}')
elif args[0] == 'exec' and 'python3' in args:
    source = sys.stdin.read()
    print('/workspace/qore-skills-9.7.5' if 'def read_stage' in source else '{}')
""")
        docker.chmod(0o755)
        prompt = self.base / "prompt.txt"
        prompt.write_text("Use the supplied public sources.\n")
        log = self.base / "docker-calls.jsonl"
        env = {**os.environ, "PATH": str(bindir) + os.pathsep + os.environ["PATH"],
               "DOCKER_CALLS": str(log)}
        return prompt, log, env

    def test_shell_defaults_disable_command_network_and_web_search(self):
        prompt, log, env = self.fake_docker()
        result = subprocess.run(["bash", str(SCRIPT), "run", "qore-qualification-test", str(prompt)],
                                env=env, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = [json.loads(line) for line in log.read_text().splitlines()]
        invocation = next(call for call in calls if "codex" in call and "--json" in call)
        self.assertEqual(invocation[invocation.index("--workdir") + 1], "/workspace/qore-skills-9.7.5")
        self.assertEqual(invocation[invocation.index("--sandbox") + 1], "workspace-write")
        self.assertIn("sandbox_workspace_write.network_access=false", invocation)
        self.assertIn('web_search="disabled"', invocation)
        for flag in ("--ignore-user-config", "--ignore-rules", "--ephemeral"):
            self.assertIn(flag, invocation)
        self.assertNotIn("danger-full-access", invocation)

    def test_sandbox_failure_stops_before_credentials_or_model_work(self):
        prompt, log, env = self.fake_docker()
        env["CANARY_EXIT"] = "17"
        result = subprocess.run(["bash", str(SCRIPT), "run", "qore-qualification-test", str(prompt)],
                                env=env, text=True, capture_output=True)
        self.assertEqual(result.returncode, 17)
        calls = [json.loads(line) for line in log.read_text().splitlines()]
        self.assertFalse(any("/home/node/.codex/auth.json" in call for call in calls))
        self.assertFalse(any("codex" in call and "--json" in call for call in calls))


if __name__ == "__main__":
    unittest.main()
