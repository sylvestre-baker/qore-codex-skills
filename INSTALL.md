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
