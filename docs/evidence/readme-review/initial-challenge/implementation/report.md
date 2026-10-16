# README implementation and claims challenge

Candidate: unpublished 0.1.0, qualification explicitly in progress; first challenge wave. Supplied archive SHA-256: `bafd0da80667a00f9e6bd2f9e726eaa64d61ff42d026b9f58eb857df15bf40f8`. The locally rebuilt archive has exactly that SHA-256. This report is a bounded implementation/claims challenge, not final readiness or a complete method qualification.

## Scope and identity

The actual active role is `/root`. `identity.json` records the fresh observed UTC time, container hostname, UID, working directory and evidence-capture process PID. No host conversation/session UUID was exposed through the available facilities; none is invented. No finders, verifier, or other subagents were spawned. These findings have no independent verification verdict labels.

Only candidate public material and standard local shell/Python/Node facilities were used. The bundled generic-review execution summary was inspected as public historical execution evidence; no separate README reader reports, author private inputs, credentials, or unrelated workspace evidence were used. Private logical evidence references were not resolved. No live browser action, publication, external contact, or candidate source edit occurred. Scratch builds, generated derivatives, installation targets and report artifacts are under this report directory. The final source digest comparison found zero changed candidate resources among 177 manifest resources.

## Finding

**RI-001 — Release manifest replaces recorded browser-observation origins with first-party (low).**

`tools/qore.py:58-60` assigns every resource `origin: first-party`; `finalize` at lines 75–78 uses it to generate the top-level manifest. The build rights gate at lines 161–182 accepts explicitly reviewed `Qaizen-public-observation` resources, but this distinction does not survive assembly. The release schema also constrains the origin to `first-party`. `origin-boundary.json` retains all 12 actual mismatches, including the video and three screenshots; the source and artifact digests match for every listed comparison. License remains MIT in both records; the defect concerns origin, not an inferred license violation.

Source → artifact → claim → reader decision: reviewed `release-rights.json` origin → regenerated `manifest.json` origin → the release contract's advertised redistribution information (`docs/contracts.md:10`, `PROVENANCE.md:13`) → a downstream decision about evidence provenance or attribution. A reader consuming the inventory loses an explicit distinction present in the rights source while build/verification report success.

Minimal remedy: carry reviewed origins into the inventory and allow them in the schema, keeping generated metadata separately identified. If the two fields intentionally mean different things, define their meanings and retain the reviewed origin in an unambiguous consumer field. This is a correction proposal; no source change was made.

## Commands and capabilities traced

Actual command stdout/stderr and exit codes are retained in `commands.log`; numbered source excerpts are in `source-traces.log`.

- `qore.py --help` exposes the documented build, verify, derive, install, compare, snapshot and validate-run interfaces. Build succeeded, emitted 178 files, and reproduced the supplied archive hash exactly.
- Derivation from `profiles/qore.json` succeeded; independent verification of the generated output succeeded with 39 files. All three generated folders contain their own copied profile and helper resources. All six direct profile/method checks (Qore and contrast × plan/review/ux) exited zero and retained their actual selected fields in the log.
- Fresh installation into a scratch project succeeded, printed three paths and `replaced: false`; repeating the command exited one and refused the existing first skill. No candidate checkout installation was attempted.
- All 82 bundled unit tests passed. They exercise actual package/validator behavior, not full method reasoning or independent role execution.
- `verify .` failed because the supplied working directory includes installed `.agents/skills` copies outside the release inventory. The separately rebuilt release verified successfully. This environment-specific failure is not treated as a candidate defect.

Profile source IDs, digests, command vectors, invariant applicability and web-surface selection are implemented in `tools/context.py` and copied checkers. Stale applicable sources suppress affected facts and affect coverage. Generated instructions require running those checkers and recording consumed facts before use. The distinction between a checker-selected fact and actual method consumption is documented. No actual plan or UX method execution was performed here, so generated instruction presence is not presented as proof of runtime compliance.

The review skill explicitly requires separate finder contexts, actual mechanical redaction, and a fresh verifier. The run checker compares actor declarations and identity-bound phase evidence; its documented limits acknowledge that actor labels cannot prove isolation. The bundled generic-review record identifies a different earlier candidate archive (`3e0265c6…`), not the challenged archive. It is historical scoped evidence only. README lines 7, 44, 87 and 95 adequately retain qualification/independence limits; this challenge does not demand that unfinished qualification already be complete.

The findings validator separates impact severity from verified blockers; skipped verification retains partial coverage. The UX stop rule accounts for skipped, blocked, missing and stale required gates before SHIP and enforces a ceiling outcome at six iterations. These are declaration/structure consumers; the docs explicitly require observation and separately retained execution evidence. Passing those helpers is not treated as a complete web review, a permission grant, or proof of reasoning quality.

Build checks explicit rights entries and byte freshness before assembling. Missing/stale entries are tested, and build succeeded against the frozen entries. This establishes attestation consistency only; private rights bases and ownership were not independently established. The origin-field discrepancy above is the concrete cross-boundary issue retained from this trace.

First-party prose inspected is English. The limited text scan found only mathematical typography and a proper documentation name outside basic ASCII in the inspected authored Markdown/scripts; no English-consistency defect was identified. Existing-site rendered copy and protocol tokens are explicitly excepted by README line 106.

## Limits and disposition

One low-severity finding is proposed, with no independent confirmation label. No additional actionable candidate is retained. The investigation was bounded by the requested six-minute budget and focused on README command/capability/result promises and their public consumers. It did not run a browser, Docker qualification, a new multi-role method, exhaustive malformed-input testing, or any external guidance retrieval. Public historical evidence and schema validity cannot establish execution on this exact candidate. Lack of those new executions is a limit of this challenge, not a newly invented release requirement.

The retained evidence supports reviewing RI-001 and continuing the already-declared qualification process. It does not support publication approval or a final readiness verdict.
