# Findings contract and validation

Both candidate and final packets are JSON objects containing `findings`, an array. An explicit empty array is valid; `{}`, a bare array, malformed/truncated JSON, missing fields, and duplicate IDs are not substitutes. A finding has nonempty string fields `id`, `title`, `severity`, and `evidence`. Severity is `critical`, `high`, `medium`, `low`, or `info` and describes impact if the stated condition holds.

Evidence must identify a checkable file/location, source, or measured result. A number without its procedure and context is insufficient reasoning even if it passes a structural check. The final report also gives the triggering condition, violated behavior or requirement, and practical consequence. Include enough raw target context for a reader to reproduce the claim without trusting the finder.

From this skill's directory:

```bash
node scripts/redact-for-verifier.mjs /absolute/path/to/findings.json > /absolute/path/to/claims.json
node scripts/finding-lint.mjs /absolute/path/to/verified.json --verifier=ran --json
```

The redactor validates shape before mechanically selecting `id`, `title`, `severity`, `evidence`, and optional `counterexample`. It removes other fields, not the meaning of prose inside allowed strings. Finder-supplied claim context remains visible; this is a field/report boundary, not semantic blinding. Use its actual output, not finder prose, as verifier input. The verifier writes a final strict findings envelope preserving IDs and original candidate severity. Add `verdict`:

| Verdict | Required support |
|---|---|
| `CONFIRMED` | `counterexample`: concrete inputs/state, actual result, and expected result, supported by reproduction evidence. |
| `PLAUSIBLE` | Evidence plus the unresolved condition or missing observation; no claim of independent confirmation. |
| `REFUTED` | `refuted_because`: an evidence-backed explanation of why the candidate fails. Keep the finding in the final packet. |

If no independent verifier ran, use `--verifier=skipped`; every candidate remains PLAUSIBLE, coverage is PARTIAL or BLOCKED, and neither confirmation nor refutation is attributed to the missing pass. If only some batches ran, label the unexamined IDs, retain their PLAUSIBLE verdicts, and keep overall coverage PARTIAL. Report which verified claims were actually examined rather than treating the flag as phase proof.

Only independently CONFIRMED `critical`/`high` findings are verified blockers under this contract. Blocking is derived separately from impact severity. Any critical/high PLAUSIBLE finding may pass structural validation but requires PARTIAL coverage and PENDING, even with `--verifier=ran`. If a separate confirmed blocker exists, the verdict remains DO-NOT-SHIP with PARTIAL coverage. `unresolved_findings` names these unresolved critical/high IDs; retain their severity and uncertainty. A REFUTED high candidate remains in the audit record without blocking. Explain any genuine evidence-based severity reassessment instead of lowering impact to clear a gate.

Validation checks report structure and verdict obligations. It cannot establish that a location supports the claim, that a counterexample really ran, or that contexts were independent. Retain phase evidence, checker output, and the [run record](run-evidence.md).

Order the readable report by impact, with confirmed findings first within an impact level. For each, show location/evidence, condition and consequence, counterexample or uncertainty/refutation, and correction/disposition where applicable. End with confirmed/plausible/refuted totals, requested/returned roles, verification coverage, unexamined IDs, target snapshot, limits, and the separate execution coverage result. Never label a valid empty packet a complete defect-free review without the required executed phases.
