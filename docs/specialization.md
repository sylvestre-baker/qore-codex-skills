# Evaluate a project adaptation

**All 18 original cells executed, including the retained pilot; 14 COMPLETE and 4 PARTIAL after independent coverage qualification. Comparative benefit remains UNKNOWN.**

Use this optional protocol to decide whether to retain, simplify or fix an adaptation for the obligations tested on Qaizen Labs. For your first Qore result, use the [published review quickstart](../README.md#try-one-review). The [recorded Labs case](evidence/qaizen-labs/README.md) remains separate from this experiment.

## What the comparison can establish

The primary comparison is **generic Qore versus derived Qore**. They receive the same task and may consult the same original project sources. The derived skill organizes those facts through the existing sourced profile. It receives no exclusive project information and the invocation does not repeat the expected rule.

| Condition | Instructions and project context |
|---|---|
| Baseline | The task and original project sources, without Qore. This also changes the method and organization of work. |
| Generic | The same task and sources, with the selected generic method. |
| Derived | The same task and sources, with its generated Qaizen Labs derivative. |

Each cell uses a fresh context. The candidate, source digests, model configuration, tools and declared budget identify the execution. A valid baseline need not perform Qore phases. Generic and derived reports retain their methods’ required phases and execution records.

One observation in each of eighteen cells is a bounded diagnostic. Six related scenarios on one project do not demonstrate general superiority, statistical reliability, cost savings or robustness to future models. Observed time and resource use are reported with their limits rather than converted into a productivity claim.

## Six related scenarios

The [scenario registry](../evals/scenarios.json) is the machine-readable authority for the inputs and criteria. The [series registry](../evals/series.json) accounts for the three conditions in every scenario, including cells not launched.

| Scenario | Task | Expected evidence |
|---|---|---|
| P1 | Plan correction of an incomplete protocol. | Separate criteria for keyboard traversal, returned state and focus, with source-backed checks. |
| P2 | Plan a documentation clarification of a correct protocol. | Preserve valid obligations without inventing an application change. |
| R1 | Review the incomplete protocol. | Identify missing evidence without claiming a proven website defect. |
| R2 | Review its corrected comparator. | An empty review is valid; any additional finding needs support. |
| U1 | Observe the actual Back journey from the public entry. | Keyboard traversal, return state, heading focus and unanswered state. |
| U2 | Observe help opening and closing. | Closure, focus on the help summary and an unchanged unanswered question. |

The protocol documents are **reconstructed tutorial fixtures**, newly authored for this evaluation. They are not historical public revisions or newly discovered website defects. The corrected comparator is unavailable to P1 and R1 workers. Synthetic controls qualify the protocol; they do not replace real browser observations.

The criteria examine relevant project rules, evidence, omissions, unsupported assertions, valid empty findings, unnecessary changes and justified decisions. Reading a profile is not proof of using it: the result must identify its effect on an action or conclusion.

## Prepare the environment before trials

**Observed recovery:** the original [no-model probe](evidence/specialization/isolation-probe.json) failed before command execution. A separately qualified [disposable Linux runtime](evidence/specialization/runtime/README.md) then ran the pilot and all remaining cells. It used an explicit scoped seccomp syscall allowance, UID 1000, dropped capabilities, no new privileges, no host mounts, a named inner filesystem sandbox, disabled connectors and observed parent/child boundary controls. Model transport remained available; command networking did not. This qualifies the recorded environment, not arbitrary Docker installations or the historical clean-room default.

Workers must not reach old answers, reports, evaluator keys, neighboring cell results, private sources, personal skill directories or the full repository history. A new chat alone does not establish that isolation. The common input bundle contains the selected sources and the target document; each Qore condition also receives its complete autonomous skill resources.

Before a cell starts, record actual model and tool availability, test the source boundary, and check that tools cannot reach alternate search or network paths. Keep model transport separate from tool-network permissions. Recheck input digests after the trial. A violated boundary invalidates comparability; an unavailable required capability leaves the cell incomplete or blocked. Do not substitute the author’s main conversation.

Use the declared budgets and order in the series. The first balanced R1 group checks capture, isolation and feasibility. Its outcome does not determine whether the experiment proceeds. A material protocol correction preserves the pilot separately and restarts the balanced series; only one pilot correction is permitted. This means at most twenty-one attempted cells, rather than silently replacing unfavorable results.

## Browser observations use a declared operator relay

The agent requests a complete sequence of at most forty actions. An operator executes it in the existing observation harness and returns actual screenshots, DOM, events and diagnostics. The operator does not fix selectors, repair the route, suggest a missing check or continue the agent’s reasoning.

Each request starts again at the real entry. At most six complete observations are permitted. The initial Tab used by the harness probe is documented. Refusals, interruptions, assistance and scope limits remain part of the evidence.

Only the declared entry, Start, help summary, Close and Back controls are authorized. No questionnaire answer or submission may be activated. The harness must check the actual click target or focused keyboard control before activation; a matching label alone is insufficient. If that guard cannot be qualified, live cells remain blocked. Existing origin and network protections remain active.

The live deployment may change independently of the local surface contract. Matching local digests do not prove that the three conditions observed the same website state. Unverified live comparability allows an observation report, not a conclusion that one condition helped.

## Local helper interface

The implementation is `tools/evaluate.py`. Its three operations prepare local files, check recorded evidence and summarize entered evaluations. They do not run agents, models, browsers or paid services, and they do not judge reasoning quality.

**Command status:** all eighteen preparations and original agent executions are retained. The checker validates their exported records and the generated summary consumes later independent qualification without rewriting original method declarations. Candidate and correction checks are linked in the result inventory. These helpers still do not execute or grade agents themselves.

Run from the repository root with Python 3. Substitute a scenario ID and condition listed in the registries; use a new, unused output directory:

```sh
python3 tools/evaluate.py prepare --scenario R1 --condition generic --output /tmp/qore-eval-r1-generic-new
```

The expected output is a contained `worker/` input bundle, its manifest, and an evaluator-only frozen `source-snapshot/`. Stage **only `worker/`** in the trial environment. The source snapshot includes fixtures and evaluation definitions needed to reconstruct the expected inputs; it must remain outside every worker. Preparation is not an executed trial and must not create a completed run record.

Once an actual run and reviewed evidence exist, substitute their paths:

```sh
python3 tools/evaluate.py check RECORD --evidence-root ROOT
python3 tools/evaluate.py summarize SERIES --output NEW_DIR
```

`RECORD` is an actual evaluation record, `ROOT` is its evidence root, and `SERIES` is the actual series registry. `NEW_DIR` is an unused directory for generated summaries. These are substitutions, not existing evidence files. Validation checks the record’s identities and referenced bytes. A passing structure does not establish a completed phase or correct conclusion.

A later independent qualification can restrict the effective coverage while preserving the original method record and declared coverage; see the [qualification contract](contracts.md#independent-diagnostic-qualification). Summaries report both declarations and effective states and disclose unqualified cells. A valid metadata packet never proves independent work occurred.

The evaluation record references existing Qore execution records where applicable. Baseline records have no Qore run reference. Applicable criterion states are **MET / NOT_MET / UNKNOWN**. Applicability is frozen per scenario; an applicable criterion cannot be skipped as NOT_APPLICABLE. Comparability is **COMPARABLE / UNVERIFIED / INVALID**. These are separate from execution coverage and finding severity. Cells without execution remain **NOT_RUN** in the series.

The [record schema](../schemas/qore-eval-run.schema.json) describes the minimum envelope. `environment.actor_id` identifies the parent context; each child has its own identity and a start/end interval within the trial. Measured aggregate agent time includes those intervals. A linked Qore record uses the same trial ID, host/operator, prepared-input digest and observed time window; its actors must appear in the trial's accounting. Missing measurements retain their reason rather than becoming zero.

The checker reconstructs the exact allowed worker tree from the frozen source snapshot, without executing snapshot code. Rewriting the input manifest cannot authorize an extra answer file, a different prompt or another skill. It rejects symlinked input/evidence roots and ancestors inside the declared boundary. Keep the source snapshot with the evidence, outside workers, and use the matching versioned checker for later historical validation.

An excluded pilot is a balanced R1 triad with actual hashed records and hashed `qore-eval-change/1` evidence. Only `SETUP_CHANGED` or `PROTOCOL_CHANGED` is accepted. The change names distinct before/after identities; protocol changes must match the frozen scenario revisions, and setup changes identify both environments. Summaries retain the pilot records, status and reasons. Validation establishes byte relationships; it cannot prove that a stated exclusion motive is unbiased.

## Read results without manufacturing a winner

A distinct evaluator applies criteria fixed before the trials to neutral run identifiers. Identifiable condition clues are disclosed. A separate verifier examines material comparative conclusions and evidence. Neither role’s name nor a valid JSON file proves substantive independence.

| Decision | Meaning for the tested obligations |
|---|---|
| Retain | Evidence supports keeping the adaptation at the tested revision. |
| Simplify | Evidence supports proposing a smaller adaptation. That change needs its own check. |
| Fix | A supported failure requires correction and fresh affected evidence. |
| Unknown | Missing, invalid or inconclusive evidence does not support a decision. |

A tie, valid empty review or absent demonstrated benefit is an acceptable outcome. Corrections produce new identities; original attempts and failures remain visible. The [result inventory](evidence/specialization/README.md) distinguishes helper qualification, campaign completion and conclusions that can actually be interpreted.

Qodo may review the frozen implementation diff separately if access and capabilities are available. Its actual output is retained and independently checked. An unobserved Qodo review stays NOT_OBSERVED and is not part of the three-condition comparison.

No trial or helper grants publication, merge, deployment, outreach or spending permission. Public evidence requires a provenance and disclosure review. Private sources, credentials, raw traces and client code are not automatically exported.

## Recorded execution limits

The frozen candidate remains bound to the original eighteen attempts. Later profile 0.1.1, browser-harness, planning-deadline and reporting corrections are separately identified. There were no excluded pilots or replacement quality trials. Neutral filenames did not blind evaluators to method content. Predeclared criteria were applied qualitatively after outputs; the operational interpretation was not a validated standardized rubric.

Child context wall intervals are conservative bounds, not exact compute or billing telemetry. Some role returns and one evaluator exceeded their smaller declared budgets; missed expiry requests and actual times remain in evidence. No universal budget-compliance claim is made. A required deep-entry observation unavailable through the frozen relay remains missing; warm navigation, reload and history do not silently replace it.
