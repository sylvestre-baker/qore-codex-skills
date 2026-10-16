# Focused project-profile consumer probe

The requested consumer probe completed. Fresh preflight passed, the profile-selected current validation command passed all 90 tests (exit 0), and direct executions support the relevant verified-blockers invariant for the tested states. No source changes, credential access or publication occurred. No other installed derivative was invoked. The project suite does exercise generic plan/review/UX helpers and temporary generated fixtures as part of its declared validation.

The exact command was python3 -B -m unittest discover -s tests -v, selected only after preflight and inspection of the current test code. Complete actual argv, stdout, stderr and status are retained in commands.md and the execution JSON files.

| Synthetic case | Exit | Coverage | Decision | Verified blockers |
| --- | --- | --- | --- | --- |
| Missing envelope | 1 | PARTIAL | INVALID | None |
| High PLAUSIBLE, verifier skipped | 0 | PARTIAL | PENDING | None |
| Critical PLAUSIBLE, verifier skipped | 0 | PARTIAL | PENDING | None |
| CONFIRMED, verifier skipped | 1 | PARTIAL | INVALID | None |
| High CONFIRMED, verifier declared ran | 0 | COMPLETE | DO-NOT-SHIP | Synthetic PROBE-HIGH |
| Explicit empty findings, verifier declared ran | 0 | COMPLETE | SHIP | None |

Both skipped-verifier severity values remain unchanged in actual output. The implementation refuses CONFIRMED status with verification skipped, and derives blockers only from valid critical/high CONFIRMED findings with verifier declared ran. Thus A02 and the invariant affect the review decision: an unverified high concern cannot be downgraded to clear a gate or treated as a verified blocker. A01 rejects malformed input. A03 permits a structurally valid empty packet, but its COMPLETE/SHIP is conditional on actual phase evidence, as the example and validator limit explicitly state. The synthetic declared-ran cases demonstrate schema decisions only; no independent finding confirmation occurred.

No defect was demonstrated in this bounded probe. This is not a zero-defect certification, shipping approval, or complete three-finder review. Full review campaign coverage is PARTIAL: correctness/security/feasibility finder contexts, mechanical claim redaction, fresh independent verification and a campaign findings gate were deliberately not run because the user requested a focused consumer probe. Requested/returned finder roles: zero/zero. No actual candidate findings or unexamined finding IDs were generated; PROBE-HIGH is only synthetic test data. Lead checking does not substitute for an independent verifier. No qore-run/1 full-campaign completion is claimed.

Identity and limits: identities.json retains the user-supplied source archive identity separately from recomputed derivative and consumed-target snapshot identities. The original archive bytes were not available to rehash. The working directory has no Git metadata. The scoped digest manifest does not claim to identify every repository byte. No prior public execution results supported this result. Only current qore profile facts were consumed; plan/UX and neighboring profile facts were not used. Five-minute budget; bounded current-source probe only.

Evidence: preflight.md/preflight.json; project-validation.json; invariant-probes.json and six retained synthetic inputs; commands.md; profile-use.md; identities.json; consumed-snapshot-manifest.json; current source copies under source/.
