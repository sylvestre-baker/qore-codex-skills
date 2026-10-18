"""Verify package safety and sourced context with isolated temporary inputs."""
import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile


TOOLS = Path(__file__).resolve().parents[1] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
qore = importlib.import_module("qore")
context = importlib.import_module("context")


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.source = self.base / "source"
        self.source.mkdir()
        for name in qore.SKILLS:
            skill = self.source / "skills" / name
            (skill / "references").mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                f"---\nname: {name}\ndescription: Isolated package test\n---\n"
                "Read [the local guide](references/guide.md). "
                "See [informational documentation](https://example.com/docs).\n",
                encoding="utf-8",
            )
            (skill / "references/guide.md").write_text("# Guide\nUse the declared project inputs.\n", encoding="utf-8")
        (self.source / "README.md").write_text("# Test package\nThree isolated skills.\n", encoding="utf-8")
        (self.source / "LICENSE").write_text("Fixture license text for packaging tests only.\n", encoding="utf-8")
        (self.source / "plugin.json").write_text(json.dumps({"name": "test-qore", "version": "0.1.0"}), encoding="utf-8")
        self.allowlist = sorted(str(path.relative_to(self.source)) for path in self.source.rglob("*") if path.is_file())
        self.write_allowlist(self.allowlist)
        self.root_patch = patch.object(qore, "ROOT", self.source)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.project = self.base / "project"
        self.project.mkdir()
        self.marker_name = "qore-command-must-not-run-" + self.base.name
        (self.project / "rules.md").write_text("Use the scoped source contract.\n", encoding="utf-8")

    def write_allowlist(self, paths):
        (self.source / "release-files.json").write_text(json.dumps(paths + ["release-rights.json"]), encoding="utf-8")
        resources = [{"path": p, "sha256": context.digest(self.source / p), "origin": "first-party", "license": "MIT", "status": "approved", "basis": "New isolated fixture authored for this test."} for p in paths if (self.source / p).is_file()]
        (self.source / "release-rights.json").write_text(json.dumps({"schema": "qore-rights/1", "resources": resources}), encoding="utf-8")

    def test_unknown_or_unauthorized_redistribution_is_refused_with_resource(self):
        path = self.source / "release-rights.json"
        original = json.loads(path.read_text())
        for status, origin, license_name in (("unknown", "first-party", "MIT"), ("denied", "first-party", "MIT"), ("approved", "unauthorized-client", "MIT"), ("approved", "first-party", "unknown")):
            packet = json.loads(json.dumps(original))
            packet["resources"][0]["status"] = status
            packet["resources"][0]["origin"] = origin
            packet["resources"][0]["license"] = license_name
            path.write_text(json.dumps(packet))
            with self.assertRaisesRegex(ValueError, "redistribution right: " + packet["resources"][0]["path"]):
                self.build(status)

    def test_required_personal_path_is_refused_in_repository_content(self):
        (self.source / "README.md").write_text("Run the helper at " + "/Users/" + "fixture-owner/private/check.py\n")
        self.write_allowlist(self.allowlist)
        with self.assertRaisesRegex(ValueError, "Personal path"):
            self.build()

    def test_remote_runtime_import_is_not_an_informational_citation(self):
        relative = "skills/qore-review/references/remote.mjs"
        (self.source / relative).write_text("import 'https://example.com/required-runtime.mjs';\n")
        self.write_allowlist(self.allowlist + [relative])
        with self.assertRaisesRegex(ValueError, "Undeclared remote runtime resource"):
            self.build()

    def test_missing_and_stale_redistribution_reviews_are_refused(self):
        path = self.source / "release-rights.json"
        original = json.loads(path.read_text())
        packet = json.loads(json.dumps(original))
        packet["resources"].pop()
        path.write_text(json.dumps(packet))
        with self.assertRaisesRegex(ValueError, "Missing redistribution review"):
            self.build("missing-right")
        path.write_text(json.dumps(original))
        (self.source / "README.md").write_text("Changed source after rights review.\n")
        with self.assertRaisesRegex(ValueError, "Redistribution review is stale: README.md"):
            self.build("stale-right")

    def test_release_preserves_the_reviewed_observation_origin(self):
        path = self.source / "release-rights.json"
        packet = json.loads(path.read_text())
        packet["resources"][0]["origin"] = "Qaizen-public-observation"
        path.write_text(json.dumps(packet))
        bundle = Path(self.build()["bundle"])
        manifest = json.loads((bundle / "manifest.json").read_text())
        record = next(r for r in manifest["resources"] if r["path"] == packet["resources"][0]["path"])
        self.assertEqual(record["origin"], "Qaizen-public-observation")

    def profile(self):
        return {
            "schema": "qore-project/1", "id": "fixture", "version": "1.0.0",
            "sources": [{"id": "rules", "path": "rules.md", "sha256": context.digest(self.project / "rules.md")}],
            "commands": [{"id": "check", "source": "rules", "argv": ["python3", "-c", f"open({self.marker_name!r}, 'w').write('unexpected')"], "applies_to": ["plan", "review", "ux"]}],
            "invariants": [{"id": "scoped", "source": "rules", "statement": "Only consume current sourced facts."}],
            "surfaces": {"web": {"source": "rules", "entry_url": "https://example.com/start", "allowed_origins": ["https://example.com"], "required_state": "The detail view is visible", "kind": "fixture"}},
        }

    def write_profile(self, profile=None):
        path = self.base / "profile.json"
        path.write_text(json.dumps(profile or self.profile()), encoding="utf-8")
        return path

    def assert_command_not_executed(self):
        for root in (Path.cwd(), self.base, self.project, self.source):
            self.assertFalse((root / self.marker_name).exists(), "Profile command ran in " + str(root))
        self.assertEqual(list(self.base.rglob(self.marker_name)), [], "Profile command ran in a generated fixture directory")

    def test_no_execution_guard_detects_a_relative_marker_in_the_actual_working_directory(self):
        import subprocess
        marker = self.project / self.marker_name
        subprocess.run(self.profile()["commands"][0]["argv"], cwd=self.project, check=True)
        self.assertTrue(marker.is_file())
        with self.assertRaises(AssertionError):
            self.assert_command_not_executed()

    def test_no_execution_guard_also_checks_nested_derivative_directories(self):
        nested = self.base / "derived/qore-plan-fixture"
        nested.mkdir(parents=True)
        (nested / self.marker_name).write_text("Unexpected execution in a derivative.\n")
        with self.assertRaises(AssertionError):
            self.assert_command_not_executed()

    def build(self, name="output"):
        return qore.build(self.base / name)

    def test_builds_are_byte_identical_with_fixed_archive_metadata(self):
        first, second = self.build("first"), self.build("second")
        self.assertEqual(first["sha256"], second["sha256"])
        self.assertEqual(Path(first["archive"]).read_bytes(), Path(second["archive"]).read_bytes())
        with zipfile.ZipFile(first["archive"]) as archive:
            entries = archive.infolist()
            self.assertTrue(entries)
            self.assertTrue(all(entry.date_time == (2026, 10, 15, 0, 0, 0) for entry in entries))
            self.assertTrue(all((entry.external_attr >> 16) & 0o777 == 0o644 for entry in entries))

    def test_positive_package_has_exactly_three_closed_skills_and_https_citations(self):
        result = self.build()
        bundle = Path(result["bundle"])
        self.assertTrue(qore.verify(bundle)["valid"])
        self.assertEqual({path.name for path in (bundle / "skills").iterdir()}, set(qore.SKILLS))
        for name in qore.SKILLS:
            standalone = json.loads((bundle / "skills" / name / "references/release.json").read_text())
            self.assertEqual(standalone["schema"], "qore-release/1")
            self.assertEqual({row["path"] for row in standalone["resources"]}, {"SKILL.md", "references/guide.md"})

    def test_skills_only_archive_is_closed_installable_and_reproducible(self):
        import shutil
        import subprocess
        (self.source / "tools").mkdir()
        for name in ("qore.py", "context.py", "run_contract.py"):
            shutil.copyfile(TOOLS / name, self.source / "tools" / name)
        (self.source / "INSTALL.md").write_text("# Install\nUse the bundled installer.\n")
        self.write_allowlist(self.allowlist + ["INSTALL.md"] + ["tools/" + name for name in ("qore.py", "context.py", "run_contract.py")])
        first = qore.build(self.base / "slim-first", "skills")
        second = qore.build(self.base / "slim-second", "skills")
        self.assertEqual(first["sha256"], second["sha256"])
        bundle = Path(first["bundle"])
        self.assertTrue(qore.verify(bundle)["valid"])
        self.assertFalse((bundle / "README.md").exists())
        self.assertFalse((bundle / "docs").exists())
        response = subprocess.run([sys.executable, "-B", str(bundle / "tools/qore.py"), "install", "--source", str(bundle), "--project-root", str(self.project)], capture_output=True, text=True, check=True)
        self.assertEqual(len(json.loads(response.stdout)["installed"]), 3)
        with self.assertRaisesRegex(ValueError, "destination exists"):
            qore.build(self.base / "slim-first", "skills")

    def test_missing_runtime_reference_prevents_build_without_partial_destination(self):
        skill = self.source / "skills/qore-plan/SKILL.md"
        skill.write_text(skill.read_text() + "[Required guide](references/missing.md)\n")
        self.write_allowlist(self.allowlist)
        with self.assertRaisesRegex(ValueError, "Unresolved or escaping local skill reference"):
            self.build()
        self.assertFalse((self.base / "output" / f"qore-skills-{qore.VERSION}").exists())

    def test_escaping_runtime_reference_is_refused_even_when_target_exists(self):
        skill = self.source / "skills/qore-plan/SKILL.md"
        skill.write_text(skill.read_text() + "[Escape](../../README.md)\n")
        self.write_allowlist(self.allowlist)
        with self.assertRaisesRegex(ValueError, "Unresolved or escaping local skill reference"):
            self.build()

    def test_release_allowlist_traversal_and_symlink_are_refused(self):
        outside = self.base / "outside.md"
        outside.write_text("External file.\n")
        self.write_allowlist(self.allowlist + ["../outside.md"])
        with self.assertRaises(ValueError):
            self.build()
        link = self.source / "linked.md"
        link.symlink_to(outside)
        self.write_allowlist(self.allowlist + ["linked.md"])
        with self.assertRaises(ValueError):
            self.build("symlink")

    def test_verify_rejects_altered_missing_and_unlisted_files(self):
        for mutation in ("altered", "missing", "unlisted"):
            with self.subTest(mutation=mutation):
                bundle = Path(self.build(mutation)["bundle"])
                path = bundle / "skills/qore-plan/references/guide.md"
                if mutation == "altered":
                    path.write_text("Changed after packaging.\n")
                elif mutation == "missing":
                    path.unlink()
                else:
                    (bundle / "unlisted.txt").write_text("Unexpected content.\n")
                with self.assertRaises(ValueError):
                    qore.verify(bundle)

    def test_verify_rejects_manifest_digest_changes_and_unknown_major(self):
        for mutation in ("digest", "major"):
            bundle = Path(self.build(mutation)["bundle"])
            path = bundle / "manifest.json"
            manifest = json.loads(path.read_text())
            if mutation == "digest":
                manifest["resources"][0]["sha256"] = "0" * 64
            else:
                manifest["schema"] = "qore-release/2"
            path.write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                qore.verify(bundle)

    def test_verify_rejects_unknown_host_kind_version_and_redistribution(self):
        for field, value in (("host", "unqualified"), ("kind", "unknown"), ("version", "2.0.0"), ("redistribution", "unknown")):
            with self.subTest(field=field):
                bundle = Path(self.build("metadata-" + field)["bundle"])
                path = bundle / "manifest.json"
                manifest = json.loads(path.read_text())
                manifest[field] = value
                path.write_text(json.dumps(manifest))
                with self.assertRaises(ValueError):
                    qore.verify(bundle)

    def test_standalone_inventory_cannot_omit_repeat_or_upgrade_resources(self):
        for mutation in ("omit", "repeat", "major"):
            bundle = Path(self.build("standalone-" + mutation)["bundle"])
            local_path = bundle / "skills/qore-plan/references/release.json"
            local = json.loads(local_path.read_text())
            if mutation == "omit":
                local["resources"].pop()
            elif mutation == "repeat":
                local["resources"].append(local["resources"][0].copy())
            else:
                local["schema"] = "qore-release/2"
            local_path.write_text(json.dumps(local))
            manifest_path = bundle / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            for row in manifest["resources"]:
                if row["path"] == str(local_path.relative_to(bundle)):
                    row["sha256"] = context.digest(local_path)
            manifest_path.write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                qore.verify(bundle)

    def test_manifest_path_prefix_collision_does_not_escape_bundle(self):
        bundle = Path(self.build()["bundle"])
        sibling = bundle.with_name(bundle.name + "-other")
        sibling.mkdir()
        (sibling / "proof.txt").write_text("Sibling resource.\n")
        path = bundle / "manifest.json"
        manifest = json.loads(path.read_text())
        manifest["resources"].append({"path": "../" + sibling.name + "/proof.txt", "sha256": context.digest(sibling / "proof.txt")})
        path.write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):
            qore.verify(bundle)

    def test_verify_refuses_release_symlink(self):
        bundle = Path(self.build()["bundle"])
        guide = bundle / "skills/qore-plan/references/guide.md"
        outside = self.base / "external-guide.md"
        outside.write_bytes(guide.read_bytes())
        guide.unlink()
        guide.symlink_to(outside)
        with self.assertRaises(ValueError):
            qore.verify(bundle)

    def test_existing_build_and_derivative_destinations_are_preserved(self):
        result = self.build()
        archive_bytes = Path(result["archive"]).read_bytes()
        with self.assertRaises(ValueError):
            self.build()
        self.assertEqual(Path(result["archive"]).read_bytes(), archive_bytes)
        destination = self.base / "derived"
        qore.derive(self.write_profile(), self.project, destination)
        changed = destination / "qore-plan-fixture/SKILL.md"
        changed.write_text(changed.read_text() + "Local adaptation.\n")
        before = changed.read_bytes()
        with self.assertRaises(ValueError):
            qore.derive(self.write_profile(), self.project, destination)
        self.assertEqual(changed.read_bytes(), before)

    def test_derive_copies_three_profiles_and_does_not_execute_commands(self):
        destination = self.base / "derived"
        result = qore.derive(self.write_profile(), self.project, destination)
        self.assertTrue(result["valid"])
        self.assert_command_not_executed()
        for skill in qore.SKILLS:
            path = destination / (skill + "-fixture")
            self.assertEqual(json.loads((path / "references/project.json").read_text()), self.profile())
            self.assertIn("name: " + skill + "-fixture", (path / "SKILL.md").read_text())
            self.assertIn("Scoped to project fixture.", (path / "SKILL.md").read_text().splitlines()[2])

    def test_local_profile_adaptation_is_named_without_blocking_current_facts(self):
        destination = self.base / "derived"
        qore.derive(self.write_profile(), self.project, destination)
        copied = destination / "qore-review-fixture/references/project.json"
        self.assertEqual(context.local_adaptations(copied), [])
        baseline = context.digest(copied)
        adapted = json.loads(copied.read_text())
        adapted["invariants"][0]["statement"] = "Authorized local rule."
        copied.write_text(json.dumps(adapted))
        result = context.validate_profile(adapted, self.project, "review")
        self.assertEqual(result["coverage"], "COMPLETE")
        self.assertEqual(context.local_adaptations(copied), [{"path": "references/project.json", "expected_sha256": baseline,
                                                           "actual_sha256": context.digest(copied), "kind": "local_adaptation"}])
        self.assertEqual(context.local_adaptations(self.write_profile()), [])

    def test_standalone_profile_is_not_blocked_by_an_unrelated_neighboring_release_file(self):
        import subprocess
        profile = self.base / "project.json"
        profile.write_text(json.dumps(self.profile()))
        for neighbor in ("{", "[" * 200000 + "]" * 200000, '{"version":"3.1.0","channel":"stable"}',
                         '{"schema":"qore-release/1","resources":[]}',
                         '{"schema":"qore-release/1","resources":null}'):
            with self.subTest(neighbor=neighbor):
                (self.base / "release.json").write_text(neighbor)
                response = subprocess.run([sys.executable, "-B", str(TOOLS / "context.py"), str(profile),
                                           "--root", str(self.project), "--method", "review"], capture_output=True, text=True)
                self.assertEqual(response.returncode, 0, response.stderr)
                packet = json.loads(response.stdout)
                self.assertEqual(packet["coverage"], "COMPLETE")
                self.assertEqual(packet["local_adaptations"], [])

    def test_profile_exceeding_json_parser_depth_reports_structured_blocked_result(self):
        import subprocess
        profile = self.base / "deep-profile.json"
        profile.write_text("[" * 200000 + "]" * 200000)
        response = subprocess.run([sys.executable, "-B", str(TOOLS / "context.py"), str(profile),
                                   "--root", str(self.project), "--method", "review"], capture_output=True, text=True)
        self.assertEqual(response.returncode, 2)
        packet = json.loads(response.stderr)
        self.assertEqual(packet["coverage"], "BLOCKED")
        self.assertNotIn("Traceback", response.stderr)

    def test_installer_warns_about_same_name_user_skill_without_changing_it(self):
        bundle = Path(self.build()["bundle"])
        home = self.base / "home"
        existing = home / ".agents/skills/qore-review"
        existing.mkdir(parents=True)
        policy = existing / "SKILL.md"
        policy.write_text("Existing personal skill.\n")
        with patch.object(Path, "home", return_value=home):
            result = qore.install(bundle, self.project)
        self.assertEqual(len(result["installed"]), 3)
        self.assertEqual([row["skill"] for row in result["warnings"]], ["qore-review"])
        self.assertEqual(result["warnings"][0]["code"], "same-name-user-skill")
        self.assertEqual(policy.read_text(), "Existing personal skill.\n")

    def test_compact_profile_identity_matches_copied_bytes_and_runtime_checker(self):
        import subprocess
        profile = self.base / "compact.json"
        profile.write_text(json.dumps(self.profile(), separators=(",", ":")))
        expected = context.digest(profile)
        destination = self.base / "derived-compact"
        result = qore.derive(profile, self.project, destination)
        self.assertEqual(result["profile"]["sha256"], expected)
        for skill in qore.SKILLS:
            copied = destination / (skill + "-fixture") / "references/project.json"
            self.assertEqual(copied.read_bytes(), profile.read_bytes())
            response = subprocess.run([sys.executable, "-B", str(TOOLS / "context.py"), str(copied), "--root", str(self.project), "--method", qore.METHODS[skill]], capture_output=True, text=True, check=True)
            self.assertEqual(json.loads(response.stdout)["profile"]["sha256"], expected)

    def test_install_copy_failure_can_be_retried_without_manual_skill_removal(self):
        bundle = Path(self.build()["bundle"])
        unrelated = self.project / ".agents/skills/local-policy/SKILL.md"
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text("Keep the user's existing policy.\n")
        real_copytree = qore.shutil.copytree

        def fail_second_skill(source, destination, *args, **kwargs):
            if Path(source).name == "qore-review":
                raise PermissionError("Controlled second-skill copy failure")
            return real_copytree(source, destination, *args, **kwargs)

        with patch.object(qore.shutil, "copytree", side_effect=fail_second_skill):
            with self.assertRaises(OSError):
                qore.install(bundle, self.project)
        target = self.project / ".agents/skills"
        self.assertEqual(sorted(path.name for path in target.iterdir()), ["local-policy"])
        self.assertEqual(unrelated.read_text(), "Keep the user's existing policy.\n")
        result = qore.install(bundle, self.project)
        self.assertEqual(len(result["installed"]), 3)
        self.assertFalse(result["replaced"])
        self.assertEqual(qore.compare(bundle, self.project)["changes"], [])

    def test_install_recovers_each_staging_copy_and_publication_failure(self):
        bundle = Path(self.build()["bundle"])
        real_copytree = qore.shutil.copytree
        real_rename = Path.rename
        for phase in ("copy", "publication"):
            for name in qore.SKILLS:
                with self.subTest(phase=phase, skill=name):
                    project = self.base / (phase + name)
                    project.mkdir()
                    target = project / ".agents/skills"
                    other = target / "user-skill/local.md"
                    other.parent.mkdir(parents=True)
                    other.write_text("User content.\n")

                    def copy(src, dst, *args, **kwargs):
                        if phase == "copy" and Path(src).name == name:
                            raise PermissionError("Controlled copy failure: " + name)
                        return real_copytree(src, dst, *args, **kwargs)

                    def rename(src, dst):
                        if phase == "publication" and Path(dst).parent == target / name:
                            raise PermissionError("Controlled publication failure: " + name)
                        return real_rename(src, dst)

                    with patch.object(qore.shutil, "copytree", side_effect=copy), patch.object(Path, "rename", rename):
                        with self.assertRaises(qore.InstallRecoveryError) as caught:
                            qore.install(bundle, project)
                    self.assertTrue(caught.exception.recovery["safe_to_retry"])
                    self.assertEqual(caught.exception.recovery["retained_paths"], [])
                    self.assertEqual(other.read_text(), "User content.\n")
                    self.assertEqual(sorted(p.name for p in target.iterdir()), ["user-skill"])
                    self.assertEqual(list(project.glob(".qore-install-*")), [])
                    self.assertEqual(list((project / ".agents").glob(".qore-install-*")), [])
                    self.assertEqual(len(qore.install(bundle, project)["installed"]), 3)
                    self.assertEqual(qore.compare(bundle, project)["changes"], [])

    def test_install_cleans_partial_file_copy_and_can_retry(self):
        bundle = Path(self.build()["bundle"])

        def fail_mid_file(src, dst, *args):
            dst.write(src.read(7))
            raise PermissionError("Controlled partial file copy")

        with patch.object(qore.shutil, "copyfileobj", side_effect=fail_mid_file):
            with self.assertRaises(qore.InstallRecoveryError) as caught:
                qore.install(bundle, self.project)
        self.assertIn("Controlled partial file copy", str(caught.exception))
        self.assertTrue(caught.exception.recovery["safe_to_retry"])
        self.assertEqual(list((self.project / ".agents/skills").iterdir()), [])
        self.assertEqual(list(self.project.glob(".qore-install-*")), [])
        self.assertEqual(list((self.project / ".agents").glob(".qore-install-*")), [])
        self.assertEqual(len(qore.install(bundle, self.project)["installed"]), 3)

    def test_install_rolls_back_failure_of_final_validation(self):
        bundle = Path(self.build()["bundle"])
        target = self.project / ".agents/skills"
        check = qore._check_install_bytes
        calls = []

        def fail_final(path, expected):
            if path.parent == target:
                calls.append(path)
                if len(calls) == 4:
                    raise ValueError("Controlled final validation failure")
            return check(path, expected)

        with patch.object(qore, "_check_install_bytes", side_effect=fail_final):
            with self.assertRaises(qore.InstallRecoveryError) as caught:
                qore.install(bundle, self.project)
        self.assertTrue(caught.exception.recovery["safe_to_retry"])
        self.assertEqual(list(target.iterdir()), [])
        self.assertEqual(len(qore.install(bundle, self.project)["installed"]), 3)

    def test_install_refuses_modified_staging_before_publication(self):
        bundle = Path(self.build()["bundle"])
        real_copytree = qore.shutil.copytree

        def tamper(src, dst, *args, **kwargs):
            result = real_copytree(src, dst, *args, **kwargs)
            if Path(src).name == "qore-ux-review":
                (Path(dst).parent / "qore-plan/SKILL.md").write_text("Changed after copy.\n")
            return result

        with patch.object(qore.shutil, "copytree", side_effect=tamper):
            with self.assertRaises(qore.InstallRecoveryError) as caught:
                qore.install(bundle, self.project)
        self.assertIn("differ from the verified bundle", str(caught.exception))
        self.assertFalse(caught.exception.recovery["safe_to_retry"])
        self.assertEqual(list((self.project / ".agents/skills").iterdir()), [])
        self.assertEqual(len(caught.exception.recovery["retained_paths"]), 1)
        staging = self.project / caught.exception.recovery["retained_paths"][0]
        self.assertEqual((staging / "qore-plan/SKILL.md").read_text(), "Changed after copy.\n")

    def test_install_preserves_a_destination_created_before_publication(self):
        bundle = Path(self.build()["bundle"])
        target = self.project / ".agents/skills"
        real_mkdir = Path.mkdir
        raced = target / "qore-review"

        def mkdir(path, *args, **kwargs):
            if path == raced and not path.exists():
                real_mkdir(path)
                (path / "local.md").write_text("Concurrent user content.\n")
            return real_mkdir(path, *args, **kwargs)

        with patch.object(Path, "mkdir", mkdir):
            with self.assertRaises(qore.InstallRecoveryError) as caught:
                qore.install(bundle, self.project)
        self.assertFalse(caught.exception.recovery["safe_to_retry"])
        self.assertEqual((raced / "local.md").read_text(), "Concurrent user content.\n")
        self.assertEqual(sorted(p.name for p in target.iterdir()), ["qore-review"])

    def test_install_preserves_foreign_content_and_replaced_roots_during_rollback(self):
        bundle = Path(self.build()["bundle"])
        real_rename = Path.rename
        for change in ("extra-file", "edited-file", "replaced-root", "symlink"):
            with self.subTest(change=change):
                project = self.base / change
                project.mkdir()
                target = project / ".agents/skills"
                first = target / "qore-plan"
                external = self.base / (change + "-external")
                external.mkdir()
                (external / "local.md").write_text("External content.\n")

                def rename(src, dst):
                    if Path(dst).parent == target / "qore-review":
                        if change == "extra-file":
                            (first / "local.md").write_text("New user content.\n")
                        elif change == "edited-file":
                            (first / "SKILL.md").write_text("Edited user content.\n")
                        else:
                            real_rename(first, project / "saved-original")
                            if change == "symlink":
                                first.symlink_to(external, target_is_directory=True)
                            else:
                                first.mkdir()
                                (first / "local.md").write_text("Replacement content.\n")
                        raise PermissionError("Controlled publication failure after observed change")
                    return real_rename(src, dst)

                with patch.object(Path, "rename", rename):
                    with self.assertRaises(qore.InstallRecoveryError) as caught:
                        qore.install(bundle, project)
                self.assertFalse(caught.exception.recovery["safe_to_retry"])
                self.assertIn(".agents/skills/qore-plan", caught.exception.recovery["retained_paths"])
                self.assertTrue(first.exists())
                self.assertEqual((external / "local.md").read_text(), "External content.\n")
                self.assertTrue(caught.exception.recovery["cleanup_errors"])

    def test_install_preserves_an_empty_destination_created_during_publication(self):
        bundle = Path(self.build()["bundle"])
        raced = self.project / ".agents/skills/qore-review"
        real_mkdir = Path.mkdir
        identities = []

        def mkdir(path, *args, **kwargs):
            if path == raced and not path.exists():
                real_mkdir(path, mode=0o700)
                identities.append(path.stat().st_ino)
            return real_mkdir(path, *args, **kwargs)

        with patch.object(Path, "mkdir", mkdir):
            with self.assertRaises(qore.InstallRecoveryError) as caught:
                qore.install(bundle, self.project)
        self.assertFalse(caught.exception.recovery["safe_to_retry"])
        self.assertEqual(raced.stat().st_ino, identities[0])
        self.assertEqual(raced.stat().st_mode & 0o777, 0o700)
        self.assertEqual(list(raced.iterdir()), [])

    def test_install_preserves_a_foreign_entry_inside_a_newly_owned_root(self):
        bundle = Path(self.build()["bundle"])
        destination = self.project / ".agents/skills/qore-plan"
        real_mkdir = Path.mkdir

        def mkdir(path, *args, **kwargs):
            result = real_mkdir(path, *args, **kwargs)
            if path == destination:
                (path / "SKILL.md").write_text("Foreign content appeared.\n")
            return result

        with patch.object(Path, "mkdir", mkdir):
            with self.assertRaises(qore.InstallRecoveryError) as caught:
                qore.install(bundle, self.project)
        self.assertFalse(caught.exception.recovery["safe_to_retry"])
        self.assertEqual((destination / "SKILL.md").read_text(), "Foreign content appeared.\n")

    def test_install_reports_cleanup_failure_without_masking_primary_error(self):
        bundle = Path(self.build()["bundle"])
        target = self.project / ".agents/skills"
        real_rename, real_rmtree = Path.rename, qore.shutil.rmtree

        def rename(src, dst):
            if Path(dst).parent == target / "qore-review":
                raise PermissionError("Primary publication error")
            return real_rename(src, dst)

        def rmtree(path, *args, **kwargs):
            if Path(path) == target / "qore-plan":
                raise PermissionError("Cleanup access denied")
            return real_rmtree(path, *args, **kwargs)

        with patch.object(Path, "rename", rename), patch.object(qore.shutil, "rmtree", side_effect=rmtree):
            with self.assertRaises(qore.InstallRecoveryError) as caught:
                qore.install(bundle, self.project)
        self.assertEqual(str(caught.exception), "Primary publication error")
        recovery = caught.exception.recovery
        self.assertFalse(recovery["safe_to_retry"])
        self.assertEqual(recovery["retained_paths"], [".agents/skills/qore-plan"])
        self.assertIn("Cleanup access denied", recovery["cleanup_errors"][0]["error"])
        self.assertIn("Inspect", recovery["next_action"])

    def test_install_reports_staging_cleanup_failure_after_complete_install(self):
        bundle = Path(self.build()["bundle"])
        real_rmtree = qore.shutil.rmtree

        def rmtree(path, *args, **kwargs):
            if Path(path).name.startswith(".qore-install-"):
                raise PermissionError("Private staging cleanup denied")
            return real_rmtree(path, *args, **kwargs)

        with patch.object(qore.shutil, "rmtree", side_effect=rmtree):
            result = qore.install(bundle, self.project)
        self.assertEqual(len(result["installed"]), 3)
        warning = next(w for w in result["warnings"] if w["code"] == "install-staging-retained")
        self.assertTrue((self.project / warning["path"]).is_dir())
        self.assertEqual(qore.compare(bundle, self.project)["changes"], [])

    def test_install_refuses_cross_device_publication_before_skill_creation(self):
        import os
        bundle = Path(self.build()["bundle"])
        target = self.project / ".agents/skills"
        target.mkdir(parents=True)
        real_stat = Path.stat

        def different_device(path, *args, **kwargs):
            result = real_stat(path, *args, **kwargs)
            if path == target:
                values = list(result)
                values[2] += 1
                return os.stat_result(values)
            return result

        with patch.object(Path, "stat", different_device):
            with self.assertRaises(qore.InstallRecoveryError) as caught:
                qore.install(bundle, self.project)
        self.assertIn("share a filesystem", str(caught.exception))
        self.assertTrue(caught.exception.recovery["safe_to_retry"])
        self.assertEqual(list(target.iterdir()), [])

    def test_install_recovers_derived_skills_and_preserves_cli_failure_contract(self):
        profile = self.write_profile()
        derived = self.base / "derived-install"
        qore.derive(profile, self.project, derived)
        real_copytree = qore.shutil.copytree

        def fail(src, dst, *args, **kwargs):
            if Path(src).name.startswith("qore-review-"):
                raise PermissionError("Derived copy failure")
            return real_copytree(src, dst, *args, **kwargs)

        with patch.object(qore.shutil, "copytree", side_effect=fail):
            with self.assertRaises(qore.InstallRecoveryError) as caught:
                qore.install(derived, self.project)
        self.assertTrue(caught.exception.recovery["safe_to_retry"])
        self.assertEqual(len(qore.install(derived, self.project)["installed"]), 3)
        self.assertEqual(qore.compare(derived, self.project)["changes"], [])

        import io
        error = qore.InstallRecoveryError(PermissionError("Original failure"), caught.exception.recovery)
        stream = io.StringIO()
        with patch.object(sys, "argv", ["qore", "install", "--source", str(derived), "--project-root", str(self.project)]), patch.object(qore, "install", side_effect=error), patch.object(sys, "stderr", stream):
            self.assertEqual(qore.main(), 1)
        packet = json.loads(stream.getvalue())
        self.assertFalse(packet["valid"])
        self.assertEqual(packet["error"], "Original failure")
        self.assertTrue(packet["recovery"]["safe_to_retry"])

    def test_install_relative_project_root_keeps_recovery_and_success_warnings(self):
        import os
        bundle = Path(self.build()["bundle"])
        previous = Path.cwd()
        real_rmtree = qore.shutil.rmtree

        def deny_staging(path, *args, **kwargs):
            if Path(path).name.startswith(".qore-install-"):
                raise PermissionError("Staging cleanup denied")
            return real_rmtree(path, *args, **kwargs)

        try:
            os.chdir(self.base)
            with patch.object(qore.shutil, "rmtree", side_effect=deny_staging):
                result = qore.install(bundle, Path("project"))
            warning = next(row for row in result["warnings"] if row["code"] == "install-staging-retained")
            self.assertFalse(Path(warning["path"]).is_absolute())
            failed = self.base / "relative-failure"
            failed.mkdir()
            with patch.object(qore.shutil, "rmtree", side_effect=deny_staging), patch.object(qore.shutil, "copytree", side_effect=PermissionError("Original copy failure")):
                with self.assertRaises(qore.InstallRecoveryError) as caught:
                    qore.install(bundle, Path("relative-failure"))
            self.assertEqual(str(caught.exception), "Original copy failure")
            self.assertFalse(caught.exception.recovery["safe_to_retry"])
            self.assertTrue(all(not Path(p).is_absolute() for p in caught.exception.recovery["retained_paths"]))
        finally:
            os.chdir(previous)

    @unittest.skipUnless(sys.platform != "win32" and __import__("os").geteuid() != 0, "Requires POSIX permission enforcement for a non-root operator")
    def test_install_keeps_primary_copy_error_when_bookkeeping_cannot_read(self):
        import os
        bundle = Path(self.build()["bundle"])

        def fail_unreadable(src, dst, *args):
            dst.write(src.read(4))
            dst.flush()
            os.fchmod(dst.fileno(), 0)
            raise PermissionError("Original partial write failure")

        try:
            with patch.object(qore.shutil, "copyfileobj", side_effect=fail_unreadable):
                with self.assertRaises(qore.InstallRecoveryError) as caught:
                    qore.install(bundle, self.project)
            self.assertIn("Original partial write failure", str(caught.exception))
            self.assertFalse(caught.exception.recovery["safe_to_retry"])
            self.assertTrue(caught.exception.recovery["cleanup_errors"])
        finally:
            for path in self.project.rglob("*"):
                if path.is_file():
                    path.chmod(0o600)

    @unittest.skipUnless(sys.platform != "win32" and __import__("os").geteuid() != 0, "Requires POSIX permission enforcement for a non-root operator")
    def test_install_never_reports_safe_retry_when_destination_is_inaccessible(self):
        bundle = Path(self.build()["bundle"])
        target = self.project / ".agents/skills"
        real_rename = Path.rename

        def lose_access(src, dst):
            if Path(dst).parent == target / "qore-review":
                target.chmod(0)
                raise PermissionError("Original publication failure with lost access")
            return real_rename(src, dst)

        try:
            with patch.object(Path, "rename", lose_access):
                with self.assertRaises(qore.InstallRecoveryError) as caught:
                    qore.install(bundle, self.project)
            self.assertFalse(caught.exception.recovery["safe_to_retry"])
            self.assertTrue(caught.exception.recovery["retained_paths"])
            self.assertIn("Original publication failure", str(caught.exception))
        finally:
            target.chmod(0o700)
        self.assertTrue((target / "qore-plan").is_dir())
        with self.assertRaises(ValueError):
            qore.install(bundle, self.project)

    def test_install_preserves_mode_only_local_adaptation_during_recovery(self):
        bundle = Path(self.build()["bundle"])
        target = self.project / ".agents/skills"
        real_rename = Path.rename
        changed = target / "qore-plan/SKILL.md"

        def adapt_mode(src, dst):
            if Path(dst).parent == target / "qore-review":
                changed.chmod(0o444)
                raise PermissionError("Publication failure after local permission change")
            return real_rename(src, dst)

        with patch.object(Path, "rename", adapt_mode):
            with self.assertRaises(qore.InstallRecoveryError) as caught:
                qore.install(bundle, self.project)
        self.assertFalse(caught.exception.recovery["safe_to_retry"])
        self.assertEqual(changed.stat().st_mode & 0o777, 0o444)

    @unittest.skipUnless(sys.platform != "win32" and __import__("os").geteuid() != 0, "Requires POSIX permission enforcement for a non-root operator")
    def test_install_supports_readonly_parents_with_writable_skills_directory(self):
        bundle = Path(self.build()["bundle"])
        target = self.project / ".agents/skills"
        target.mkdir(parents=True)
        try:
            self.project.chmod(0o500)
            target.parent.chmod(0o500)
            result = qore.install(bundle, self.project)
            self.assertEqual(len(result["installed"]), 3)
            self.assertEqual(qore.compare(bundle, self.project)["changes"], [])
        finally:
            self.project.chmod(0o700)
            target.parent.chmod(0o700)

    def test_install_cli_preserves_copy_error_when_directory_bookkeeping_fails(self):
        import io
        bundle = Path(self.build()["bundle"])
        real_rglob = Path.rglob

        def fail_scan(path, pattern, *args, **kwargs):
            if path.name == "qore-plan" and path.parent.name.startswith(".qore-install-"):
                raise PermissionError("Secondary staging scan failure")
            return real_rglob(path, pattern, *args, **kwargs)

        stream = io.StringIO()
        with patch.object(sys, "argv", ["qore", "install", "--source", str(bundle), "--project-root", str(self.project)]), patch.object(qore.shutil, "copytree", side_effect=PermissionError("Original installation copy failure")), patch.object(Path, "rglob", fail_scan), patch.object(sys, "stderr", stream):
            self.assertEqual(qore.main(), 1)
        packet = json.loads(stream.getvalue())
        self.assertEqual(packet["error"], "Original installation copy failure")
        self.assertTrue(any("Secondary staging scan failure" in row["error"] for row in packet["recovery"]["cleanup_errors"]))
        self.assertEqual(list((self.project / ".agents/skills").iterdir()), [])
        self.assertEqual(len(qore.install(bundle, self.project)["installed"]), 3)

    def test_install_refuses_to_overwrite_a_modified_existing_skill(self):
        bundle = Path(self.build()["bundle"])
        installed = qore.install(bundle, self.project)
        self.assertFalse(installed["replaced"])
        local = self.project / ".agents/skills/qore-review/SKILL.md"
        local.write_text(local.read_text() + "Project-specific local adaptation.\n")
        before = local.read_bytes()
        comparison = qore.compare(bundle, self.project)
        self.assertEqual(len(comparison["changes"]), 1)
        self.assertEqual(comparison["changes"][0]["path"], "SKILL.md")
        self.assertTrue(comparison["changes"][0]["local_adaptation"])
        self.assertFalse(comparison["replaced"])
        with self.assertRaises(ValueError):
            qore.install(bundle, self.project)
        self.assertEqual(local.read_bytes(), before)

    def test_compare_identifies_locally_added_policy_as_an_adaptation(self):
        bundle = Path(self.build()["bundle"])
        qore.install(bundle, self.project)
        local = self.project / ".agents/skills/qore-review/local-policy.md"
        local.write_text("An authorized local policy.\n")
        comparison = qore.compare(bundle, self.project)
        change = next(c for c in comparison["changes"] if c["path"] == "local-policy.md")
        self.assertTrue(change["local_adaptation"])
        self.assertIsNone(change["candidate_sha256"])
        self.assertEqual(local.read_text(), "An authorized local policy.\n")

    def test_install_refuses_symlinked_ancestor_without_external_writes(self):
        bundle = Path(self.build()["bundle"])
        external = self.base / "external-install"
        external.mkdir()
        (self.project / ".agents").symlink_to(external, target_is_directory=True)
        with self.assertRaises(ValueError):
            qore.install(bundle, self.project)
        self.assertEqual(list(external.iterdir()), [])

    def test_current_profile_returns_scoped_facts_without_execution(self):
        for method in ("plan", "review", "ux"):
            result = context.validate_profile(self.profile(), self.project, method)
            self.assertEqual(result["coverage"], "COMPLETE")
            self.assertEqual(result["commands"][0]["id"], "check")
        self.assert_command_not_executed()

    def test_changed_or_missing_sources_block_only_affected_facts(self):
        for state in ("changed", "missing"):
            with self.subTest(state=state):
                source = self.project / "rules.md"
                source.write_text("Original source.\n")
                profile = self.profile()
                if state == "changed":
                    source.write_text("New source revision.\n")
                else:
                    source.unlink()
                result = context.validate_profile(profile, self.project, "plan")
                self.assertEqual(result["coverage"], "BLOCKED")
                self.assertEqual(result["commands"], [])
                self.assertEqual(result["invariants"], [])
                self.assert_command_not_executed()

    def test_stale_context_is_partial_when_unrelated_current_facts_remain(self):
        stable = self.project / "stable.md"
        stable.write_text("Current independent source.\n")
        profile = self.profile()
        profile["sources"].append({"id": "stable", "path": "stable.md", "sha256": context.digest(stable)})
        profile["invariants"].append({"id": "independent", "source": "stable", "statement": "Retain unrelated valid work."})
        (self.project / "rules.md").write_text("Changed source.\n")
        result = context.validate_profile(profile, self.project, "review")
        self.assertEqual(result["coverage"], "PARTIAL")
        self.assertEqual([fact["id"] for fact in result["invariants"]], ["independent"])
        self.assertEqual(result["commands"], [])

    def test_stale_profile_cannot_be_derived_into_a_new_destination(self):
        profile = self.write_profile()
        (self.project / "rules.md").unlink()
        with self.assertRaises(ValueError):
            qore.derive(profile, self.project, self.base / "derived")
        self.assertFalse((self.base / "derived").exists())

    def test_fact_references_must_name_a_declared_source(self):
        for field in ("commands", "invariants"):
            profile = self.profile()
            profile[field][0]["source"] = "undeclared"
            with self.assertRaises(ValueError):
                context.validate_profile(profile, self.project, "plan")
        profile = self.profile()
        profile["surfaces"]["web"]["source"] = "undeclared"
        with self.assertRaises(ValueError):
            context.validate_profile(profile, self.project, "ux")

    def test_unknown_profile_major_and_source_path_traversal_are_refused(self):
        profile = self.profile()
        profile["schema"] = "qore-project/2"
        with self.assertRaises(ValueError):
            context.validate_profile(profile, self.project, "plan")
        for relative in ("../project-other/rules.md", "/tmp/rules.md", "..\\outside.md"):
            profile = self.profile()
            profile["sources"][0]["path"] = relative
            with self.assertRaises(ValueError):
                context.validate_profile(profile, self.project, "plan")

    def test_escaping_source_symlink_is_refused(self):
        outside = self.base / "outside.md"
        outside.write_text("Outside source.\n")
        source = self.project / "rules.md"
        source.unlink()
        source.symlink_to(outside)
        profile = self.profile()
        with self.assertRaises(ValueError):
            context.validate_profile(profile, self.project, "plan")


if __name__ == "__main__":
    unittest.main()
