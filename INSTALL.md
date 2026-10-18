# Install the skills-only archive

This archive contains the three generic skills, their local resources, the plugin descriptor, the MIT license and the standalone installer. The full source and historical evidence remain in the main archive and [public repository](https://github.com/sylvestre-baker/qore-codex-skills).

You need Python 3 for installation. Actual method execution also needs Codex with the required independent worker capabilities, Node and Bash; web UX requires the browser capabilities for your declared scope.

From the extracted archive directory, verify it and install into your chosen project:

```sh
python3 tools/qore.py verify .
python3 tools/qore.py install --source . --project-root /absolute/path/to/your/project
```

Replace the project path. The installer copies three folders into that project's `.agents/skills/`, refuses existing destinations and reports any same-name personal installation without changing it. Open a fresh Codex chat in the target project and inspect the selected skill path.

Use `$qore-plan`, `$qore-review` or `$qore-ux-review` with a concrete authorized target. Their protocols and local helpers are bundled inside each skill. This download omits the tutorial target, tests, profiles and historical evidence. Use the full source checkout for the README tutorial, development checks or rebuilding archives.

Installation and a valid inventory do not establish a completed method execution. The [MIT license](LICENSE) covers the selected first-party content.

## Recovery requirement under development

The installer must recover from a handled copy or publication error without leaving newly installed skill folders that block an immediate retry. Existing skills, unrelated files and local adaptations must remain unchanged. If cleanup cannot be completed safely, the installer must preserve uncertain content and report the retained paths and manual recovery action, rather than claim that retry is safe.

The regression test `test_install_copy_failure_can_be_retried_without_manual_skill_removal` documents a known gap in the current implementation. It deliberately fails before the correction: a controlled error while copying the second skill leaves the first skill installed, so an unchanged retry is refused. This is an injected failure test, not an observed customer incident. The test and this requirement are being reviewed before production code is changed.

This requirement does not promise an atomic three-folder update, recovery after process termination or power loss, or protection against hostile concurrent filesystem changes.
