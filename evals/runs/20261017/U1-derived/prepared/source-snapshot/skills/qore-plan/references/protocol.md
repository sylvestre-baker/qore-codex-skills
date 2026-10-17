# Planning protocol

## Intake and mode

Identify the user's requested outcome, constraints, target, current revision or named working snapshot, and authoritative inputs. Distinguish requirements, measured facts, proposals, and unknowns. Read applicable project instructions and any current specification before proposing a new one. A similarly named file is not automatically applicable: check its scope and freshness.

Use **Workflow** when an applicable specification already exists: independent Analyze, a report barrier, one Cross-examine pass per role, then lead adjudication. Use **Debate** when there is no applicable specification: initial independent analysis, a challenge pass, and at most one additional pass for unresolved questions. The maximum is three rounds in total. Do not restart the round count when a disagreement persists.

Before dispatch, state a finite task budget appropriate to the scope, worker deadlines, and the consequence of exhaustion. A worker returns its complete available report and names unfinished items when its budget ends. Use the host's real subagent tools and observed concurrency; schedule waves rather than assuming five simultaneous workers. Do not depend on a particular model, undocumented tool name, or external shared skill.

## Independent analysis

Create one fresh context per [role](roles.md). Give each the same raw target and relevant requirements, plus its own role brief. Do not provide another role's conclusions during initial analysis. The lead routes and adjudicates rather than masquerading as a sixth independent role.

Each report contains:

- Role, target snapshot, sources inspected, and uninspected scope.
- Proposed decisions and deliverables, with source locations for material facts.
- Risks with triggering conditions, affected behavior, and a checkable source or explicit hypothesis.
- Questions for named peer roles and potential alternatives.
- Unfinished work and evidence that would resolve it.

For external facts, use current primary sources where accuracy or freshness requires it. A project claim cites the actual current file and location. A measurement records its command or procedure, environment, result, and artifact. Unsupported assertions remain questions or proposals; do not adjudicate them as facts.

Save full report files. Before synthesis, compare requested roles with returned complete reports. Recover truncated output from the worker as the remainder of its report, not a lead-written summary. A missing role remains named even when another worker covers part of its topic.

## Challenge and correction

After the report barrier, give each role all returned reports. Assign the challenge links in [roles](roles.md), adding a challenger for any major decision otherwise untouched. A challenge identifies the exact decision, contradicting evidence or concrete failure case, and the smallest useful investigation. A challenge need not produce a defect.

In Workflow, each role performs one cross-examination pass and revises its own report when the evidence warrants it. In Debate, round two does the same; use round three only for a genuine unresolved question with a bounded investigation. The lead explicitly supplies the relevant messages or files for each pass. Workers send their results and end their turn rather than waiting indefinitely for peers.

Stop at resolved decisions, repeated disagreement without new evidence, the declared budget, or the third round. Preserve open questions on stalemate or exhaustion. Do not invent consensus to finish.

## Adjudication

Resolve each material conflict at its point of divergence. Record the alternatives, evidence, selected decision, consequence, and remaining uncertainty. Weight direct current evidence and valid counterexamples over vote counts or confidence. Preserve a sourced minority position even when another approach is selected. Reject a challenger's proposed fix when its own assumptions fail.

Check cross-boundary consistency before consolidating: requirements → design → actual producer → storage → serialization or message → consumer → visible outcome. Enumerate the fields that cross a material interface. Verify reuse against existing implementations, documented contracts, callers, readers, and writers. Record ambiguous searches as open items rather than declaring no impact.

Separate protocol coverage from decision readiness. All five perspectives can complete while a provider decision remains unresolved. Conversely, a useful draft with a missing role is still PARTIAL. Finish with the [specification contract](specification.md) and [run evidence](run-evidence.md).
