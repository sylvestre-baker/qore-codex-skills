# COV-C01 independent verification

**CONFIRMED, medium severity.** The frozen N16 record declares COMPLETE coverage while an applicable G1 observation remains missing. The original worker result remains unchanged. The independently justified assessed observation coverage is **PARTIAL**. This finding concerns the coverage claim, not a demonstrated website failure.

## Requirement and initial scope

The frozen UX method requires declaring scope before capability gaps and forbids shrinking it to conceal a missing tool (`N16/input/.agents/skills/qore-ux-review/SKILL.md:11-12`; `references/protocol.md:25`). Entry and state scopes include G1 (`protocol.md:10-11`). G1 says to navigate directly to applicable stateful URLs **and** reload, with relevant history checks (`references/gates.md:20-22`). Missing tools are SKIPPED/BLOCKED rather than non-applicability (`gates.md:3`; `run-evidence.md:36,48`).

The worker's initial `output/scope-plan.json:28-35` explicitly includes G1. Its line 112 says: “Reload and relevant history in observed route; deep navigation action not offered by relay, retain limitation if unproved. Invalid URL permutations outside explicit journey.” This is not a source-based exclusion of applicable direct URL entry. It cites the missing relay action and says to retain the limitation if unproved. Invalid URL permutations may remain outside the explicit journey; they are not added to this finding.

The task itself asks for the application's Back journey from its public entry (`input/TASK.md:3,7`). The frozen method explicitly orders real entry before deep URL checks (`SKILL.md:13`; `protocol.md:37`). Requiring the already-applicable G1 direct-entry subcheck therefore does not replace the requested entry journey or add a new arbitrary URL exploration task. “Cold” in the candidate title is interpreted narrowly as the missing direct URL entry, not a new requirement to purge caches, prove a new user profile, or explore unrelated routes.

## Actual observation chain and counterexample

I inspected the original N16 commands, action arrays, and raw navigation events for all three observations. Each command supplies `--url https://qaizen.io/labs`. The frozen operator creates a fresh context and performs `page.goto(target.href)` (`operator/browser_probe.mjs:184,249`). Each recorded readiness-route entry follows the public entry link click; none starts by directly loading the readiness URL or submits a direct-navigation action.

Observation 3 is decisive: `observation-3/actions.json:3-7` clicks the readiness link and then reloads. The driver implements reload with `page.reload`, and history actions with `page.goBack`/`page.goForward` (`operator/browser_probe.mjs:314-316`). The raw navigation events agree: Labs first, readiness after click, readiness reload, then history. The observations are real useful evidence for the entry, valid-route document reload and history behavior. They do not show the separate direct URL entry requested by G1.

The output nevertheless gives G1 4/PASS (`output/REPORT.md:41`; `output/gate-results.json`, G1) and declares both `coverage` and `observation_coverage` COMPLETE (`output/execution.json:607-608`). The report also explicitly acknowledges arbitrary address-bar entry was not separately exercised (`REPORT.md:57`), and the execution limitations acknowledge the missing arbitrary navigation action. This is the actual counterexample: a still-required, unobserved check coexists with COMPLETE. It does not depend on inventing a browser failure or disputing the recorded HTTP200 reload.

## Refutation attempts

1. **Direct entry was initially out of scope.** Not supported. The initial entry/state scope requires G1; the only relevant exclusion rationale is the relay's missing action. The frozen contracts explicitly reject that as a non-applicability reason. The separately excluded invalid URL permutations are not used to manufacture this finding.
2. **Reload establishes the full direct-navigation requirement.** The actual HTTP200 reload establishes document handling after real entry, and that pass should be retained. It does not show the separately named direct URL action. No raw command/action indicates such an action; all initial destinations are Labs.
3. **An established DO-NOT-SHIP can have COMPLETE coverage.** True in general, and not contradicted here. A defect discovered during fully executed work can coexist with COMPLETE. Here a required observation remains missing, which is a distinct coverage gap. The declared DO-NOT-SHIP does not fill it.
4. **The worker disclosed the limitation.** True and useful. Disclosure prevents concealment, but does not make COMPLETE accurate under the frozen coverage contract. The consumer should preserve the disclosure and adjust its assessment.

## Minimal consumer remedy

Keep the original worker files and COMPLETE declaration exactly as recorded. In the downstream assessment, record **worker_declared_coverage=COMPLETE**, **assessed_observation_coverage=PARTIAL**, and the reason: applicable G1 direct URL entry unobserved because the supplied relay lacks that action. Mark that subcheck BLOCKED/unobserved, while retaining the real entry/reload/history observations as observed passes. Do not assign a zero product score to a missing capability, relabel it non-applicable, fabricate a phase, or rerun a trial to improve its historical result.

This qualification neither invalidates the retained keyboard Back/focus observations nor turns the original DO-NOT-SHIP into SHIP. The separate visibility finding was not re-reviewed in this batch. If a later authorized observation supplies direct navigation, retain it as separately identified new evidence; it does not rewrite this trial.

## Execution, integrity and limits

The bounded batch began with observed UTC time **2026-10-17 11:17:50**. The local reproduction ran from the timestamps in `checks/commands.json`; its structured results are in `checks/results.json`. The executed harness is `checks/reproduce.py`. It independently parses required gates, original scope, all three original command URLs/action arrays/navigation events, and unchanged coverage fields. It asserts that no direct-navigation action occurred, that observation 3 is click then reload, and that the scope limitation cites relay capability absence.

All 19 inspected N16 source/input/output/operator/observation files matched their before/after SHA-256 values. Original `REPORT.md`, `execution.json`, and scope/action files were not edited. The verified finding is a strict findings envelope preserving ID COV-C01 and medium severity. This batch examined **1/1 claims: 1 CONFIRMED, 0 PLAUSIBLE, 0 REFUTED; none unexamined**. Verification coverage for this bounded claim is complete; assessed N16 observation coverage remains partial.

Only the supplied mechanical claim, neutral N16 materials, and necessary frozen UX contracts were read. No baseline, other case, investigator assessment, author fix, private website source, live browser, model call, network call, installation, repository source edit or subagent was used. The UTC command log accounts for this batch only; no unsupported cumulative telemetry is invented. This batch stays within its three-minute limit and the supplied cumulative independent-verifier budget. No browser behavior was newly executed.
