# Lead command record

Working directory: /workspace/qore-skills-0.1.0 unless stated.

- `pwd; rg --files -g AGENTS.md ...`: exit 127; pwd returned source root; rg absent. Subsequent discovery used `find . -name AGENTS.md -o -name project.json`: exit 0, no matching files.
- `cat .agents/skills/qore-review/SKILL.md .agents/skills/qore-review/references/protocol.md .agents/skills/qore-review/references/findings.md .agents/skills/qore-review/references/run-evidence.md`: exit 0; current copies retained in source/.
- `cat examples/validator-hardening.md`, `cat qore.json`, `cat README.md`, validator and test reads: exit 0; copies retained.
- `sha256sum /workspace/candidate.zip`: exit 0; 3e0265c6d33fc0340fd8df0f0c1c4074a7495a8744365b6d388c747e4daf60da.
- `python3 -B -m unittest discover -s tests -v`: exit 0; actual combined output in project-tests.log (82 tests, 1.854 seconds).
- Snapshot procedure executed via Python standard library: copy named source paths, SHA256 each, preserve actual mtimes in source-manifest.json; SHA256 manifest bytes as snapshot identity. Compare each against candidate.zip using zipfile, mapping .agents/skills/ to skills/. All scoped bytes match. identity.json records the result.

No profile was found under the local skill references, so this is generic use. No source mutation or auth-file read was requested or performed. Tests use their own temporary directories.
