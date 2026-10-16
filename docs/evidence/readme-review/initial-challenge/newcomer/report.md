# Independent README newcomer challenge

Candidate: unpublished 0.1.0, qualification explicitly in progress. User-supplied archive SHA-256: `bafd0da80667a00f9e6bd2f9e726eaa64d61ff42d026b9f58eb857df15bf40f8`.

This report contains two low-severity candidate findings, without independent-verifier verdicts. It is the first challenge wave and makes no final readiness decision. Exact findings and minimal remedies are in `findings.json`.

## Context and boundaries

I operated as `/root` in the actual provided task context. `identity.json` records the actual exposed host, UID, process identity and session ID where available. The recorded PID belongs to the identity-recording Python command, not a fabricated agent process. This was not a newly launched Codex chat or a clean Linux qualification container. Tools actually used were the provided local command executor and UTC clock, orchestrated through functions.exec. No subagents were spawned. No credentials, private author inputs, other reader reports, live websites, or browser sessions were used. Public documentation inventory entries were inspected as candidate text, not accepted as proof of prior execution.

The initial source copy and each method-specific source copy excluded `.agents`, `.git`, and Python caches. Commands ran only in disposable copies. The final public-file comparison found 178 unchanged files, zero additions, zero removals and zero changed bytes relative to the initial copy; see `source-preservation.json`. Frozen source was not edited. `rg` was unavailable (exit 127), so subsequent searches used standard grep/find and Python.

## What actually ran

The literal README shell setup (README.md:28-30) ran in `fresh-source`, then independently in `source-plan`, `source-review`, and `source-ux`. Separate retained build staging directories are under this report directory. Every build and installation exited zero, produced three installed skill paths, and reported `replaced: false`. Every build reproduced the supplied archive SHA exactly. Logs retain shell tracing, stdout, stderr, paths and exit status.

The literal derive/verify block (README.md:75-76) ran with its documented unused `/tmp/qore-derived-first` destination. Both commands exited zero. A copy of the resulting artifact is retained as `derived-artifact`. Its manifest contains kind `derived`, 39 files, and SHA-256 `050f23866c5b274b0b22d788d3113477da9020f1c59172992857fc131dfed9b4`. Each derived method's actual bundled project checker ran against the fresh project and exited zero. This establishes current profile context only, not method execution.

Method choices and execution limits:

- Plan: strengthen the bundled validator-hardening specification. The existing specification selects Workflow mode. The installed protocol requires five independent perspectives, challenge/adjudication and a specification validator. Setup and derived context checking ran; those independent phases did not run because this challenge prohibits subagents. No planning completion is claimed.
- Review: the README's bundled validator-hardening target and its validators/tests. Setup and derived context checking ran. The 35 validator regressions passed on the normal host. Three finders, mechanical phase redaction and a fresh verifier did not run. This is a single newcomer challenge, not the advertised complete review example.
- UX: the Qore profile's explicitly synthetic localhost fixture, not the QAIZEN production site. Setup and derived UX context checking ran. The selected web surface retained its fixture kind, URL, allowed origins and required state. No server/browser interaction or rendered gate execution occurred. No UX outcome is claimed.

Automatic discovery in a new Codex chat was not observed. Reading installed SKILL.md files does not establish discovery.

## Candidate findings

### RN-001 — First-review prerequisites omit Bash (low)

README.md:23 asks for Python, Node and a POSIX shell. The advertised review's regression tests launch Bash at tests/test_validators.py:20-21; planning also prescribes it at skills/qore-plan/SKILL.md:14. In a controlled PATH exposing Python, Node, POSIX sh and mktemp but no Bash, the exact setup still succeeded. Running the validator regression subset then produced seven errors out of 35 tests, all from missing Bash. On the normal host the same 35 tests passed. See `setup-posix-without-bash.log`, `posix-without-bash.log`, and `normal-validator-regressions.log`.

The reader failure is delayed: stated setup prerequisites suffice for installation, then the first-use test path needs an undeclared executable. This is a portability/precondition gap, not evidence that the validators fail on the tested normal host. Minimal remedy: list Bash for the first review/planning paths, or eliminate that dependency by invoking Node directly and adjusting the tests.

### RN-002 — Comparison excludes local additions from adaptation flag (low)

The documented update path directs readers to inspect differences and preserve local adaptations (docs/profiles.md:53-60). I added one policy file only to the disposable installed planning skill and compared it against the unchanged verified candidate. The serializer emitted the correct path and installed digest, a null candidate digest, but `local_adaptation: false`. tools/qore.py:278-283 only recognizes adaptations of paths already present in the baseline. See `compare-added-file.log`.

Source → storage → serializer → claim → decision: the installed-only policy file exists outside the recorded release baseline; comparison sees it in the installed file set and emits it in `changes`; the adaptation boolean nevertheless excludes it; a newcomer selecting preservation work from that boolean can overlook locally authored additions. The file remains visible in the full diff. No automatic migration, deletion or loss occurred. Minimal remedy: explicitly classify baseline-absent installed additions as local additions/adaptations and document their preservation.

## Boundary comparisons and non-findings

`boundary-trace.json` compares actual source SKILL.md hashes with installed bytes: all three match. Generic skills contain no project profile. Each derived skill has the expected renamed frontmatter and a profile equal to the maintained source profile. The derived checker selects method-specific facts rather than importing all facts into every method. These boundaries supported the narrow README setup/adaptation claims in this environment.

README.md:7,44,66,87-95 already limits method completion, host qualification, browser scope and human-first-use claims. Those honest gaps are not defects merely because this challenge did not complete them. The public browser artifacts were inspected as recorded material only; their historical observation was not reproduced. No external-human first-use promise was found. Requiring a working browser driver is explicit for UX.

Possible improvements, not findings: a runtime version table and a short post-install checklist could reduce assumptions; older Python/Node runtimes were not actually tested. A fail-fast shell recipe could make failed-command recovery clearer, but the documented unused-output condition was satisfied here, and no canonical-command failure was observed. No claims of general quality, speed, native support, live-site readiness or completed independent qualification are inferred.

## Retained evidence

`findings.json` is a strict object with a `findings` array, unique IDs and no self-confirmed verdict labels. `citations/` retains numbered public source excerpts. `setup-*.log`, `canonical-*.log`, `preflight-*.log`, the comparison/test logs and retained source/staging trees contain the actual commands and artifacts. `evidence-index.json` lists evidence file digests. Remedies above are proposals; candidate source was not changed.
