---
name: qore-review
description: Challenge a plan, specification, architecture document, or deliverable using three independent finders and a fresh verifier. Use for evidence-backed adversarial review; prefer an available routine code-review workflow for ordinary Git diffs, and rendered UX review for web behavior.
---

# Qore Review

Produce checkable findings while preserving uncertainty and the work that refuted false alerts. This method needs no Qore account, browser, or persistent project profile.

1. Resolve the target type and exact scope: artifact/version, repository diff with base and current snapshot, or supplied material. For an ordinary Git diff, prefer the host's available code-review workflow. Use this method when explicitly requested or that workflow cannot read the target. Do not broaden to the whole repository. If `references/project.json` exists, complete [project preflight](references/project-profile.md) before using its facts.
2. Read [the review protocol](references/protocol.md) and [findings contract](references/findings.md). Run three independent finders: **correctness**, **security**, and **performance/feasibility**. Use separate contexts without peer findings; schedule waves within real concurrency limits. Save complete files and requested/returned roles.
3. Collect a strict `{ "findings": [...] }` envelope with unique IDs. Actually run `node scripts/redact-for-verifier.mjs /absolute/path/to/findings.json > /absolute/path/to/claims.json` from the skill directory. Malformed output is a failure, never zero defects. Mechanical filtering must precede the verifier.
4. Give the filtered claims and raw target/criteria to a **fresh independent verifier**, without full finder reports, separate rationale fields, prior verdicts, or author conclusions. The filtered evidence still carries claim context; it is not semantic blinding. It attempts reproduction or refutation in bounded batches. Preserve CONFIRMED, PLAUSIBLE, REFUTED, and unfinished IDs. The lead's own checking cannot substitute for this phase.
5. Run `node scripts/finding-lint.mjs /absolute/path/to/verified.json --verifier=ran --json` only when verification actually ran; otherwise use `--verifier=skipped`. Preserve impact severity. Any critical/high PLAUSIBLE concern requires PARTIAL/PENDING even after verification ran; it is not a verified blocker. A separate confirmed blocker still requires DO-NOT-SHIP. Never downgrade severity to obtain a passing checker.
6. Report findings, counterexamples, refutations, actual phases, uncovered scope, and **COMPLETE / PARTIAL / BLOCKED coverage**. Record [execution evidence](references/run-evidence.md). A valid empty findings list does not prove the required phases ran or certify defect absence.

Apply in-scope fixes only when already authorized. Reproduce affected checks on the resulting snapshot. Review does not authorize publication, messages, shared-data writes, merge, or deployment. It does not qualify native interfaces or substitute for observing rendered web behavior.
