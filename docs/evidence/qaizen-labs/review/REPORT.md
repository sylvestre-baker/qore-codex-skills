# Derived review: actual phases and corrections

**COMPLETE execution coverage for the declared source review.** Three independent finders, actual mechanical filtering, a fresh verifier and the findings validator ran in a clean Linux container. All six generic/derived entries were exposed in the fresh catalog; each finder loaded the specialized review and checked its current profile before using project facts.

Five medium claim IDs describe four distinct defects: unavailable correction after negative review (two overlapping IDs), mismatched reviewer session/run accepted for a negative verdict, environment proxy routing of the local bearer, and ACK work scheduled after its receive deadline. All five were independently reproduced. Zero claims were refuted; there was no refutation quota. These findings concern the Qore helpers, not a newly discovered defect in the Qaizen website.

The focused correction adds an explicit PM correction turn preserving prior reviews, checks session/run before any verdict transition, disables environment proxies, and recomputes remaining budget before each ACK. A separate fresh post-fix verifier checked all four behaviors and relevant refusal/replay paths: all are resolved within the documented scope. A receive scheduling budget is not an OS process deadline against a slow-drip HTTP peer. Original findings remain CONFIRMED with their medium severity; corrections do not rewrite history.

Read [original findings](verified.json), [fresh verification](verifier/REPORT.md), [post-fix checks](fix-verifier/REPORT.md), [execution receipt](run.json), [snapshot](target-snapshot.json) and [transformation provenance](provenance.json).

The original clean archive is identified separately from later corrected bytes. The Linux suite collected 149 tests: 138 passed, 11 browser tests skipped because no optional driver was installed. MacOS browser observations have separate dated evidence. No general security, compatibility, efficiency, external human usability or release readiness follows from this source review.

[Attribution correction](attribution-correction.json) identifies the root lead as the mechanical-redaction operator and preserves the earlier public-wrapper digest. The originally accepted PM delivery remains historical; no new execution is implied.
