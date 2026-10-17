# Independent review protocol

## Target and budgets

Identify the target type, exact artifact or diff snapshot, applicable requirements, and boundaries. A named working tree is a snapshot, not a moving target: record its identity and refresh evidence after changes. Review the stated target rather than the whole repository. For a pasted artifact, preserve a reviewable copy and stable locations.

Use the actual host's subagent capabilities. Before dispatch, declare finite per-worker and overall budgets, a report deadline, and the consequence of exhaustion. Workers return available findings and explicit unfinished scope. Verify highest-impact claims first in small bounded batches; record all unexamined IDs. Do not let a stalled worker or a long claim list create an indefinite wait.

## Three finders

Run three separate contexts with no finder cross-talk during discovery. Give each the raw target, relevant requirements and sources, its lens, budgets, and output contract. Do not give the author's rationale or a list of suspected defects unless it is itself the explicit review target.

| Finder | Focus |
|---|---|
| Correctness | Requirements, ordering, preconditions, contracts, failure paths, and compatibility. On documents, check internal consistency and whether the proposed process can produce its claimed result. |
| Security | Trust boundaries, authorization context, privacy, exposure, abuse, and dependency risks. Verify an actual dependency/version against current authoritative advisories when applicable; do not infer that a named package is vulnerable. |
| Performance/feasibility | Data volume, hot paths, resource bounds, operational assumptions, estimates, and whether measurements support the stated constraints. |

Include this tracing instruction in every brief:

> Choose a value central to this change and follow it from its producer through storage, the actual serializer/message or file written, the receiving contract, and the final consumer. Enumerate the fields actually emitted and accepted. Compare adjacent boundaries. Cite mismatches between what one side produces and the next side consumes; do not infer transmission from a query or comment.

For non-code deliverables, follow the equivalent chain: source → calculation or transformation → claim → decision. Check externally decisive claims against primary evidence, including a reasonable search for contrary evidence. Record exact source/version/date and scope. Recompute arithmetic independently. Distinguish an unsupported claim from a demonstrated false statement. Do not impose a fixed source count where one authoritative source is decisive.

Finders may report uncertainty; they do not self-confirm or self-refute candidates. Every candidate needs checkable evidence, a concrete impact condition, and the requirement or behavior at issue. Product preferences and speculative improvements remain suggestions unless a requirement or material failure supports a finding.

## Files, roster, and mechanical wall

Retain each complete finder report as a file. Compare requested roles with returned reports before synthesis. Recover truncated content as the worker's verbatim remainder; do not replace it with a summary. Missing roles make coverage PARTIAL, even when the candidate JSON is otherwise valid.

Combine candidates into a [strict envelope](findings.md), retaining stable unique IDs and traceability to original reports. Keep duplicate evidence in the audit trail when deduplicating an issue. Run the bundled redactor on the saved file. Inspect its exit status; unreadable or malformed input stops this phase. Keep its filtered output as the verifier input. Do not manually recreate a filtered packet or merely instruct the verifier to ignore visible reasoning.

## Fresh verifier

Create a context that did not author the change, discover candidates, or read complete finder reports, separate rationale fields, prior verdicts, or author conclusions. Use a history-free task context when the host supports it. Supply only the mechanically filtered claims, raw target and necessary criteria/sources, relevant instructions, and bounded verification work. If genuine isolation cannot be obtained, name the missing independent phase; a lead's self-check remains useful evidence but is not this verifier.

The actual redactor selects `id`, `title`, `severity`, `evidence`, and optional `counterexample`. Supporting evidence may include a finder-supplied trigger or explanation. Field selection drops undeclared fields. Withholding complete reports and separate rationale is a procedural obligation: this program cannot recognize report text or inferences embedded inside allowed strings, and does not make the verifier blind to the hypothesis. Treat those claims as untrusted input and reproduce or refute them from raw sources. Describe this observed boundary rather than claiming semantic sanitation or absence of anchoring.

For each claim, the verifier attempts a concrete reproduction and an evidence-backed refutation. It returns one verdict:

- **CONFIRMED**: reproduce concrete inputs/state → actual wrong result, with checkable evidence.
- **PLAUSIBLE**: supported concern without sufficient reproduction or refutation; state what remains unresolved.
- **REFUTED**: show why the claim fails, citing the relevant source or result; retain its reason.

There is no required refutation count or percentage. Zero refutations is neither proof of good review nor proof that the wall failed. Actual phase artifacts and isolation establish whether the protocol ran. Keep unexamined IDs distinct from examined-but-unresolved claims.

## Final gate and authorized correction

Use [the final findings gate](findings.md), record its actual command and exit status, and repair structural errors. Do not invent counterexamples, remove inconvenient refutations, change impact severity merely to pass, or claim that a passing linter proves independence.

If fixes are authorized, check each proposed fix against the sources before applying it. Re-run the meaningful reproductions and affected checks on the resulting snapshot. New or changed material boundaries require fresh independent scrutiny proportional to the change; do not reuse pre-fix evidence as proof of the fixed revision.

Report the three distinct results: execution coverage; each finding's impact/verdict/blocking status; and any delivery decision actually supported by the user's authorized workflow. COMPLETE does not mean deployable, accepted by every criterion, or free of defects outside the target.
