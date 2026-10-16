# Independent verification

Completed 2026-10-15T20:08:15.666362+00:00. All six filtered claim IDs examined. Six CONFIRMED records represent five unique issues; C-001 and F-1 are duplicates. Original severities retained. No critical/high blockers.

Input boundary: only mechanically filtered claims.json and raw target/criteria were read. No finder reports or finder reproduction outputs were consumed. Fresh probes and controls were created in an external temporary directory.

Evidence: verifier-probe.py records exact reproduction procedure; verifier-results.json records commands, return codes, stdout/stderr and digest comparisons. Temporary artifacts: /tmp/qore-independent-verifier-51y5w0tg.

## C-001 — CONFIRMED (medium)
Derivation records the input profile digest but rewrites the bundled profile bytes

tools/qore.py:215,235; docs/profiles.md (exact profile digest); skills/qore-review/references/run-evidence.md:14; verifier-results.json derive/verify/project-check/profile-hashes.

Compact serialization of profiles/qore.json was derived into /tmp/qore-independent-verifier-51y5w0tg/derived. Derive and verify exit 0. Manifest profile.sha256 is 63c9157e3dd4d6eb2c33c899820422e8ce1d1bee9cc4e22c1df96d814e50a83f; actual bundled profile and runtime checker identity are da03026c9f73a7771cc35aaaff898a3b970fed75362ebfd0c670068d6b23b3d9. Expected one unambiguous consumed-profile identity, or distinct source/bundled identity fields. Parsed content is equal, so this demonstrates byte-identity/provenance inconsistency rather than changed facts.

## C-003 — CONFIRMED (medium)
Spec validation counts literal docstring text as executable acceptance steps

skills/qore-plan/scripts/spec-lint.mjs:44-48; skills/qore-plan/references/specification.md acceptance scenario contract; verifier-results.json docstring/no-steps-control/outline.

Generated /tmp/qore-independent-verifier-51y5w0tg/docstring.md has one actual Given step; the only When and Then occur inside its triple-quoted literal argument. Actual spec-lint exits 0 valid:true with no problems. Expected rejection for missing executable When and Then. Replacing those literal words with LiteralWhen/LiteralThen makes it reject both missing steps. Separately an Outline with <message> and no Examples also passes despite the explicit populated-Examples requirement.

## S-1 — CONFIRMED (medium)
Inherited object properties can satisfy missing UX measurements

skills/qore-ux-review/scripts/stop-rule.mjs:11,22,59-62; skills/qore-ux-review/references/evidence.md missing checks prevent SHIP; verifier-results.json inherited and ordinary-missing.

Input {"in_scope":["toString"],"iterations":[{"n":1,"scores":{},"measured":[]}]} returns exit 0 SHIP and COMPLETE with no missing gates. Expected rejection of an unsupported gate or PARTIAL/PENDING for an unmeasured accepted gate. Same input with G1 returns PARTIAL/PENDING and missing_gates:["G1"]. Inherited Object.prototype values satisfy the measurement-presence checks. Scope requires this accepted nonstandard gate name; normal G1 control is unaffected.

## F-1 — CONFIRMED (medium)
Derived release profile identity hashes the input bytes rather than the bundled profile

tools/qore.py:215,235; verifier-results.json derive/verify/project-check/profile-hashes; same underlying defect as C-001.

Independent compact-profile derivation and verification both exit 0, but manifest/input digest 63c9157e3dd4d6eb2c33c899820422e8ce1d1bee9cc4e22c1df96d814e50a83f differs from bundled/checker profile digest da03026c9f73a7771cc35aaaff898a3b970fed75362ebfd0c670068d6b23b3d9. Expected copied profile identity to align or be explicitly distinguished from source-profile identity. Duplicate of C-001; retain ID without counting as another unique defect.

## F-2 — CONFIRMED (medium)
Findings gate accepts CONFIRMED lower-severity findings without the required counterexample

skills/qore-review/scripts/finding-lint.mjs:40; skills/qore-review/references/findings.md CONFIRMED obligations; verifier-results.json medium-no-counterexample and high-control.

Packet {"findings":[{"id":"probe","title":"Known defect","severity":"medium","evidence":"source.js:1","verdict":"CONFIRMED"}]} has no counterexample. Actual finding-lint --verifier=ran --json exits 0 valid:true COMPLETE SHIP. Expected rejection because every CONFIRMED finding requires concrete counterexample. Changing severity alone to high exits 1 with counterexample problem, confirming the obligation is restricted to blocking severities.

## C-002 — CONFIRMED (low)
Unchanged failing gates bypass the promised three-comparison plateau stop

skills/qore-ux-review/scripts/stop-rule.mjs:84-85; skills/qore-ux-review/references/protocol.md Stop and report; verifier-results.json plateau and nonfailure-plateau.

Four measured iterations n=1..4 each have G1=3. Actual exit 0 decision CHANGE_APPROACH with stuck_count=3 and no_improve_count=3. Expected STOP_PLATEAU after three comparisons without improvement per protocol. Control with four missing-measurement iterations reaches STOP_PLATEAU, demonstrating that unchanged failures mask the plateau branch. Six-iteration ceiling still applies.

## Refutation attempts and limitations
Profile hashes were compared semantically as well as bytewise: JSON content is equal. This narrows the demonstrated consequence to inconsistent byte identity and provenance. It does not establish stale or altered project facts. The release resource inventory still detects byte changes.
The plateau control reaches STOP_PLATEAU without stuck failures, so plateau functionality exists but is shadowed for the claimed case. The ceiling remains effective.
The docstring negative control rejects missing steps when keyword text is removed. The outline probe independently confirms the related missing-Examples case.
The inherited-property control uses ordinary G1 and correctly retains missing coverage; the bypass depends on an accepted Object.prototype property gate name. Missing supported-gate validation does not refute acceptance of the supplied input.
The findings high-severity control rejects the omitted counterexample. The documentation explicitly requires counterexamples for every CONFIRMED severity, making lower-severity acceptance a contract mismatch.

Execution coverage for this verifier: COMPLETE across all six IDs; unexamined IDs: none. This is bounded claim verification, not whole-repository certification. Full role execution and candidate/target snapshot identities belong to the parent run record. Source changes were not authorized or intentionally made. Python derive/check subprocesses initially omitted -B and may have generated bytecode caches; parent was informed.
