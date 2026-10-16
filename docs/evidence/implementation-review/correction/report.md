# Independent correction verification

All six supplied claims are CONFIRMED against the original source and FIXED on the exercised boundaries of the proposed revision. Original severity is preserved. C-001 and F-1 intentionally remain separate IDs for the same underlying defect. There are five distinct defects. A correction does not refute the original finding.

| ID | Original severity | Original verdict | Proposed disposition |
|---|---|---|---|
| C-001 | medium | CONFIRMED | FIXED |
| C-002 | low | CONFIRMED | FIXED |
| C-003 | medium | CONFIRMED | FIXED |
| S-1 | medium | CONFIRMED | FIXED |
| F-1 | medium | CONFIRMED | FIXED |
| F-2 | medium | CONFIRMED | FIXED |

## Evidence per claim

### C-001: Derivation records the input profile digest but rewrites the bundled profile bytes

Severity: medium. Original verdict: CONFIRMED. Proposed disposition: FIXED.

Using cases/old-compact-profile.json, original derive and verify exit 0, but release profile SHA-256 is 63c9157e3dd4d6eb2c33c899820422e8ce1d1bee9cc4e22c1df96d814e50a83f while all three bundled profiles and checker identities are da03026c9f73a7771cc35aaaff898a3b970fed75362ebfd0c670068d6b23b3d9. Expected released identity to match consumed bytes. Fixed compact derivation preserves the input bytes and all identities agree. Pretty-profile control agrees on both targets.

Evidence: tools/qore.py:215,235; profile-identities.json; commands.json old-compact-derive and old-compact-check-review.

### C-003: Spec validation counts literal docstring text as executable acceptance steps

Severity: medium. Original verdict: CONFIRMED. Proposed disposition: FIXED.

cases/spec-docstring-quote.md has one executable Given; its only When/Then are docstring payload. Original public shell entry exits 0 valid:true; expected rejection under specification.md. Fixed exits 1 with missing when/then. Backtick docstrings reproduce too. Original accepts outline-missing and outline-header; fixed rejects both. Executable scenarios and populated/empty-value Examples controls pass.

Evidence: skills/qore-plan/scripts/spec-lint.mjs:35-89; commands.json *-spec-docstring-* and *-spec-outline-*.

### S-1: Inherited object properties can satisfy missing UX measurements

Severity: medium. Original verdict: CONFIRMED. Proposed disposition: FIXED.

cases/stop-missing-toString.json declares toString and no scores or measurements. Original exits 0 SHIP / COMPLETE with missing_gates:[]; expected rejection or missing observation, never SHIP. Fixed exits 2 for unsupported gate. constructor, __proto__, and hasOwnProperty are also rejected. All eight supported gates are PARTIAL when missing and SHIP with measured score 5.

Evidence: skills/qore-ux-review/scripts/stop-rule.mjs:11-24,61-64; commands.json *-stop-missing-toString.

### F-1: Derived release profile identity hashes the input bytes rather than the bundled profile

Severity: medium. Original verdict: CONFIRMED. Proposed disposition: FIXED.

Same independently reproduced defect as C-001: compact input digest 63c9157e3dd4d6eb2c33c899820422e8ce1d1bee9cc4e22c1df96d814e50a83f differs from original bundled/checker digest da03026c9f73a7771cc35aaaff898a3b970fed75362ebfd0c670068d6b23b3d9 despite successful derive and verify. Expected identical released/consumed identity; fixed input, top manifest, three local manifests, three bundles, and checkers agree.

Evidence: tools/qore.py:215,235; profile-identities.json; commands.json *-compact-*.

### F-2: Findings gate accepts CONFIRMED lower-severity findings without the required counterexample

Severity: medium. Original verdict: CONFIRMED. Proposed disposition: FIXED.

cases/finding-medium-missing.json declares medium CONFIRMED without counterexample. Original exits 0 valid:true / COMPLETE / SHIP; expected invalid because every CONFIRMED finding needs concrete counterexample support. Fixed exits 1 INVALID. Original also accepts low/info missing, blank, and whitespace proof; fixed rejects all five severities without nonblank proof. Nonblank concrete proof passes at all severities; critical/high remain DO-NOT-SHIP and medium/low/info SHIP.

Evidence: skills/qore-review/scripts/finding-lint.mjs:40; references/findings.md:18; commands.json *-finding-*.

### C-002: Unchanged failing gates bypass the promised three-comparison plateau stop

Severity: low. Original verdict: CONFIRMED. Proposed disposition: FIXED.

cases/stop-constant3-4.json measures G1=3 at n=1..4. Original exits 0 with CHANGE_APPROACH and no_improve_count=3; expected STOP_PLATEAU after three non-improving comparisons under protocol.md. Fixed returns STOP_PLATEAU / DO-NOT-SHIP. At n=3 CHANGE_APPROACH remains correct; zeros stop at plateau and n=6/7 stop at ceiling.

Evidence: skills/qore-ux-review/scripts/stop-rule.mjs:84-87; commands.json old-stop-constant3-4 and fixed-stop-constant3-4.

## Controls and attempted refutations

Profile identity: used the real maintained profiles/qore.json, serialized compactly without changing facts, plus a pretty serialization control. Both originals derive successfully, and every derived release verifies. The mismatch exists only when the original rewrites different source bytes; pretty bytes agree. In the fixed derivative, source input, returned profile metadata, top-level manifest, all three standalone release manifests, all bundled project.json files, and all three runtime checker identities agree. All checkers report COMPLETE. This rules out an obsolete profile or stale source as the explanation. The original compact input exactly reproduces the two hashes in the claims. See profile-identities.json and derived-* artifacts.

Stop behavior: constant scores 3 and 0 were checked at each length 1–7. At three iterations the nonzero failing case correctly asks for CHANGE_APPROACH; at four the fixed version stops at plateau and retains DO-NOT-SHIP. Zero remains DO-NOT-SHIP and cannot prolong plateau or ceiling. Six iterations stop without success; a fresh complete passing sixth iteration can SHIP; a passing seventh iteration still returns STOP_CEILING. Improving scores reach SHIP. Missing or unmeasured scores cannot SHIP, a fix invalidates same-iteration observations, and remeasurement restores eligibility. Supported G0–G6 and GP each pass with measured 5 and are PARTIAL when unmeasured. Unknown and inherited names are rejected in the fix. Prototype controls show the original issue is inherited lookup, rather than all arbitrary names manufacturing success.

Spec behavior: tests use the documented Bash public entrypoint, both quote and backtick docstrings, executable controls, literal Scenario/Examples text, unclosed strings, outlines without Examples, header-only Examples, and populated Examples including intentionally empty cell values. The original accepts literal step payload and missing Examples; the fix rejects those cases without rejecting the valid controls. The exact raw Markdown files are retained under cases/. No external Gherkin parser was installed or used.

Findings behavior: CONFIRMED packets at critical, high, medium, low, and info were each tested with missing, empty, whitespace-only, and concrete nonblank counterexamples. Original critical/high enforcement already worked; medium/low/info missing proof reproduces the defect. The fix enforces nonblank proof at every severity. Valid proof does not make medium/low/info blocking: only critical/high produce DO-NOT-SHIP. Structural acceptance cannot establish the truth of arbitrary nonblank proof.

## Producer, serialization, and consumer tracing

No new public JSON fields are introduced by the changed implementation. In particular source_profile_sha256 is not introduced. The identity repair keeps the existing profile.sha256 producer in tools/qore.py and copies the input bytes at derive line 235. finalize and make_skill_manifest serialize that metadata to the top-level and per-skill manifests. Each unchanged bundled project-check.py computes profile.sha256 from its actual consumed file. Those identities were compared through real executions, not inferred from new tests. The release resource inventories also hash bundled bytes, and derive/verify succeed. verify still checks resource inventories rather than independently enforcing semantic profile metadata equality; this wave establishes generator/checker agreement for the tested immutable inputs, not tamper resistance for manually rewritten metadata. The release schema permits an object profile without enforcing its inner identity fields.

The stop-rule continues to emit the existing decision/verdict/coverage/count fields; its internal maps now have null prototypes and scope names are checked against published gates. The Gherkin parser adds internal docstring/outline/Examples state; these are not exported scenario fields. The finding counterexample field already existed in the public contract and is now required structurally for every CONFIRMED severity. The final verified.json itself passes the fixed findings gate.

## Tests, identities, and execution evidence

The full current public suite ran with argv ["python3", "-B", "-m", "unittest", "discover", "-s", "tests", "-v"] in the fixed target: exit 0, 105 tests, OK. Its captured stdout/stderr are in commands.json under full-current-tests; current-tests.stdout and current-tests.stderr retain the initial identical suite run. No failing tests were omitted.

commands.json records 176 reproduction/check invocations with exact argv, cwd, exit code, stdout, and stderr. cases/ retains the exact raw JSON/Markdown boundary inputs. reproduce.py and finish.py preserve the procedures. Re-running derivation requires fresh output paths because the public CLI correctly refuses existing destinations. source-context/ contains numbered copies of only relevant implementation and public contracts. target-manifests/ retains the supplied release manifests. old-source-manifest.json and fixed-source-manifest.json enumerate all supplied files by relative path, byte count, and SHA-256; their aggregate identities are calculated over sorted JSON records. Inventory hashing did not inspect historical report conclusions. target-unchanged.json confirms both complete file inventories remain unchanged after this wave.

Raw original release verification exits 1 because its supplied tree includes extra installed .agents and cache files outside its inventory; raw proposed release verification succeeds with 487 files. This is a supplied-tree identity distinction, not a newly introduced regression. The original derivation reproductions and their generated release verification still succeed. No installed copies or historical snapshots were treated as the active original implementation.

## Regressions and limits

No new regression was established by these controls. Existing spec-linter gaps remain: spec-outline-ragged.md and spec-outline-mismatched-columns.md are accepted on both versions. Thus the revision enforces presence of populated Examples and excludes docstring payload, but does not establish full executable Gherkin grammar or placeholder binding. This limitation is retained explicitly; the two demonstrated C-003 boundaries are fixed. Concurrency changes to the profile while derive executes, arbitrary malformed Gherkin grammar, and independently re-signed metadata tampering were not examined.

This is one independent correction verification wave. Requested/returned verifier roles: 1/1; no subagents were spawned. Supplied claim verification coverage: COMPLETE, six examined IDs, zero unexamined IDs. Totals: 6 CONFIRMED, 0 PLAUSIBLE, 0 REFUTED; fixed dispositions 6, open dispositions 0 for the supplied defect boundaries. A complete finder campaign was neither requested nor executed, so broader method execution coverage remains PARTIAL and this is not universal safety certification. No credentials, installation, live browser/app activity, publication, external contact, or target edits occurred. Public historical evidence and author reasoning were not used as verification authority.
