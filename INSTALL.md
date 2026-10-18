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

## Recover from a handled installation error

The installer prepares and checks all three skills in private staging outside `.agents/skills/`, then creates each destination exclusively. A handled copy, publication or final verification error triggers cleanup of unchanged content owned by that attempt. Existing skills, unrelated files and observed local adaptations are preserved.

On failure, the command exits nonzero and writes JSON to stderr. The original failure remains in `error`. When recovery was attempted, `recovery` reports `safe_to_retry`, project-relative `retained_paths`, separate `cleanup_errors`, and `next_action`.

Staging prefers `.agents/`, with same-filesystem fallbacks for read-only project parents. A retained fallback outside the project is reported relative to the project, potentially using `..`; inspect the exact reported path. Inaccessible paths are conservatively retained in the report with inspection errors; inability to inspect never establishes safe retry. Observed permission changes also prevent automatic removal of the affected content.

If `safe_to_retry` is true, correct the original cause and rerun the same command. If it is false, inspect the retained paths, preserve local edits, and compare against the verified candidate before manually removing or relocating only content confirmed to belong to that attempt. Do not delete all `qore-*` folders or shared parent directories. An existing destination is still refused, even when empty.

Successful output retains `installed`, `replaced: false` and `warnings`. If all three skills are installed but private staging cannot be removed, an `install-staging-retained` warning identifies it for inspection. Empty parent directories may remain after recovery.

These guarantees cover handled errors without hostile concurrent filesystem changes. They do not promise an atomic three-folder update or automatic recovery after process termination or power loss. The installer never silently removes leftovers from an earlier interrupted process.

The full source checkout includes failure-injection regressions for partial copies, each skill's staging/publication, final checks, cleanup failures, conflicting destinations and changed content. This compact archive omits those development tests. Failure-injection evidence is not a customer-incident report.
