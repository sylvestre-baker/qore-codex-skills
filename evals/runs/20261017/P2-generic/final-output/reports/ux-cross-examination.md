# UX cross-examination — one Workflow challenge pass

Actual context: `/root/ux_cross`. This is a fresh successor context for the UX role's single Cross-examine pass, not a new initial Analyze report or an extra verification round. The host retired `/root/ux`; its complete independent report remains `/workspace/output/reports/ux-analysis.md`. This successor read that report and challenges the original Architecture and QA reports after the report barrier; it has not read other cross-examination outputs. All five original analyses were returned before the lead's report barrier. Snapshot supplied by lead: `e9aeec2eee10b52c3339b53b4e491d3ff69f57c68be2f5ea1d61e70df55acccc`, identifying the prepared-input manifest, not a website deployment or standalone target digest.

Budget: 90 seconds from supplied predispatch `2026-10-17T11:47:33Z`, deadline `2026-10-17T11:49:03Z`. At exhaustion this report must retain available findings and name unfinished items. No children, website calls, input changes, or network retrieval were performed.

## Inspected sources and scope

Read complete raw `TASK.md`, `surface-contract.json`, `checks/check_contract.py`, `observation-policy.json`, and `target/verification-protocol.md` under `/workspace/worker`. Also read complete planning references `.agents/skills/qore-plan/references/protocol.md` and `roles.md`, and all five original `/workspace/output/reports/{product,architecture,ux,delivery,qa}-analysis.md`. An initial combined tool response was truncated; subsequent bounded reads recovered complete Architecture, UX, Delivery, and Product reports. QA and the raw supplied sources were fully present in the initial response. No peer cross report was read. No local checker was rerun: initial workers' measurements remain attributed to their reports, not this successor's own runtime observations.

Uninspected: deployed website, browser/DOM/focus behavior, private source, real request effects, current deployment identity and external resources. All failure cases below are hypotheses or documentary risks, not observed website defects.

## Challenge 1 — Architecture user-facing complexity

**Exact decisions challenged:** Architecture A3, its runtime sequence step 4, and its risk mitigation requiring canonical Tab plus separately labeled supplemental Shift+Tab evidence. The original UX report made a similar canonical-route recommendation; this pass revises that position rather than silently presenting it as original consensus.

**Contradicting evidence:** The supplied target already permits either Tab or Shift+Tab for Close and Back (`target/verification-protocol.md:8,10`). The checker explicitly accepts either for Back (`checks/check_contract.py:35-36`). The concrete contract fields declare Tab for both (`surface-contract.json:14-15`); the checker neither resolves that literal discrepancy nor validates Close traversal at all. TASK requires preserving valid obligations and documentation-only clarification (`TASK.md:3-5`). None of these sources requires both directions or two successful runs.

**Concrete failure case:** A maintainer reaches Back via Shift+Tab from the correctly restored summary focus, within 24 steps, presses Enter, and records all expected state/focus outcomes. A canonical-plus-supplemental explanation might make the maintainer believe this valid target route must be repeated forward before any procedural keyboard result can be recorded. That would add work and acceptance complexity without an explicit two-route requirement. Conversely, silently labeling that observation a demonstrated forward-Tab route would overstate evidence. Both errors can be prevented without a new schema or harness.

**Smallest investigation:** Side-by-side compare only contract transitions `close-help`/`back`, checker lines 32-36, and target steps 4/6. This textual investigation is complete here; there is no website measurement that could decide the ownership of the wording. Lead must state the acceptance interpretation, retaining the narrow-source caveat.

**Revised UX recommendation:** Keep one sequential route per Close and Back demonstration. Default the instruction to Tab because it matches the literal declared transitions; preserve the target's Shift+Tab permission and record the actual direction. An observed permitted route suffices to demonstrate the supplied procedure's sequential-keyboard path; it never proves an unexercised direction. For exact literal forward-Tab contract coverage, mark that direction unobserved if only Shift+Tab was used. Explain that distinction once in the evidence note, not as a mandatory second journey. Do not require both directions. Close's Shift+Tab permission comes from the target, while Back additionally has checker support; neither source should be cited as if the checker validates both controls. Lead can choose stricter literal Tab evidence for a claim of full contract trace conformance, but must not describe two mandatory routes as an existing requirement.

**Disposition:** Architecture's source distinction is sound; its supplemental-route presentation needs simplification so it does not accidentally become a new required run. A3 is narrowed, not refuted wholesale. The minimum document remains setup + explicit steps + one short evidence note. Keep the comprehensive mapping outside the maintainer procedure. Architecture A1/A2/A4-A7 support that scope and need no new subsystem.

## Challenge 2 — QA observable-state coverage and outcome wording

**Exact decisions challenged:** QA D2/D5, matrix P4-P8/N4/N6, and its traversal-exhaustion Gherkin. This is a precision challenge: QA already covers the main states and distinct focus assertions, so no missing-focus defect is alleged.

**Supporting and contradicting evidence:** QA P4/P5 explicitly checks Enter-open, Space-close, Enter-reopen; P6 independently asserts closed help and summary focus; P8 independently asserts visible introduction, absent question/help and h1 focus. This correctly covers the contract (`surface-contract.json:11-17`) and stronger target postconditions (`target:8-10`). QA N4 and its Gherkin call bounded proof failure after 24 traversals, while D5 allows FAIL or NOT OBSERVED/BLOCKED. Architecture A4 and Product decision 6 instead emphasize inability to complete the bounded observation. The numerical bound exists only in the target; no supplied source makes it a universal product tab-order rule.

**Concrete failure cases:** (a) On the 24th traversal Back receives focus: interpreting “after 24” as exhaustion before inspecting the resulting focus incorrectly fails an in-bound run. (b) Back is still not reached after 24 actions: treating the unperformed Enter and return assertions as failed website behaviors invents observations. (c) An allowed resource stalls or a denied request impedes help rendering: a maintainer cannot infer help-open or help-closed from the requested key. (d) Help visibly closes while focus remains on an unrelated element: a whole-step pass hides the focus mismatch; QA already correctly rejects this.

**Smallest investigation:** Compare the Back line's “within 24 steps” with QA P7/N4 and the Gherkin; inspect per-assertion evidence labels. No browser access is needed for this wording check. Use one traversal keystroke as one step; start from the observed summary focus restored by Close, excluding the prior Close traversal and Back's Enter activation. This counting rule is a proposed operational clarification, not text already stated by the JSON.

**Required precision:** Inspect focus after every traversal, including action 24; if Back is then focused, activate Enter and assess the return assertions. If Back is not reached after action 24, record bounded keyboard reachability not demonstrated, terminal focus, actual key sequence, unanswered state if still observable, and mark Back activation/returned-state/heading-focus not observed. Do not reset focus, click, or use a direct-focus shortcut to manufacture that proof. If a visible or focus assertion actually contradicts its expectation, mark that assertion failed. Keep blocking context separate so policy denial itself is not automatically a functional defect.

**Disposition:** QA's matrix already has strong observable-state coverage. Retain P4-P8 and N3 separation. Clarify the exhaustion scenario and result vocabulary to avoid implying that all downstream behaviors failed. No new loading, empty or error screen is specified because none is supplied or observed. A single instruction to record unavailable state and affected checks is sufficient; no separate recovery subsystem or UI copy is justified.

## Revised UX requirements for the final specification

1. Preserve the reconstructed-fixture disclaimer (`target:3`), public-observation versus declared-acceptance distinction, baseline/history distinction, and private-commit/deployment limitation (`contract:19-20`). This supplied target already includes keyboard Back proof; do not characterize that as missing.
2. Put origin/method guards and the fixed en-US, 1280×800, entry/state, unanswered envelope before navigation. Retain sole origin `https://qaizen.io`, GET/HEAD/OPTIONS, expected blocked analytics POST and its observed effects, plus no answers/results/submissions/source redistribution. Describe guard obligations without inventing implementation tooling.
3. Preserve entry-link click and Start click (`contract:9-10`); this is not an all-keyboard entry requirement. Observe introduction, then the first question unanswered.
4. Spell out summary Enter/open, Space/closed, Enter/reopened as separate observable transitions before Close (`contract:11-13`). A generic help-open action does not cover this cycle.
5. Reach Close by a recorded permitted sequential route, Enter, then independently observe help closed and summary actually focused. Preserve the post-Close unanswered check (`target:8-9`). No 24-step Close cap is supplied.
6. Preserve the immediate pre-departure unanswered check, Back sequential traversal within the existing 24-step bound, Enter activation, introduction visible, question/help absent and actual introduction-heading/h1 focus (`target:10`). Close summary focus cannot substitute for Back heading focus. Treat counting and evidence labels as operational proposals.
7. Record the exercised direction and never claim the other direction passed. One target-permitted route can suffice for procedural keyboard demonstration; literal Tab trace coverage remains direction-specific. Do not add a requirement for both routes without new authority.
8. Use per-assertion expected/observed results with pass, observed mismatch, or not observed/blocked; no global runtime pass from the JSON checker. Keep future runtime evidence distinct from this documentation plan and attributed initial local checker results.

## Risks, severity, refutations and dissent

| Severity | Trigger and consequence | Evidence / handling |
| --- | --- | --- |
| Medium | Canonical/supplemental language becomes two mandatory journeys, expanding maintainer work | Target permits either; no source mandates both. Prefer one recorded route with exact directional claim. |
| Medium | Shift+Tab observation is claimed as a tested literal Tab transition | Contract declares Tab, target broader, Back checker broader. Retain discrepancy and unobserved-direction label. |
| Medium | Exhaustion is applied before inspecting action 24, or downstream unperformed assertions are marked observed failures | “Within 24” in target; hypothetical counterexample above. Count actions precisely and separate evidence status. |
| Medium | Visible closed/returned state is accepted despite wrong focus | Contract distinct focus destinations; QA N3 already addresses. Retain separate assertions. |
| High for policy compliance | Future observer relaxes methods/origin to obtain an apparent pass, omitting blocked-request effects | Contract scope/limits and policy allowlist. Retain guards/effects; no bypass. |
| Medium | A rewrite removes existing unanswered, absence, bound or focus obligations | Target 8-10. Preservation mapping must retain every one. |

Refuted proposals: mandatory testing of both traversal directions; using static checker output as website success; adding a 24-step Close cap; treating 24-step exhaustion alone as a proven universal accessibility defect; deleting stronger target postconditions because the JSON is shorter; inventing loading/error screens or recovery actions.

Preserved dissent: Architecture A3, Delivery D5 and original UX favor canonical Tab proof with Shift+Tab supplementary. This has a valid literal-contract rationale and must remain visible if the lead chooses the smaller one-permitted-route procedural interpretation. Product decision 6 and QA D4 support retaining either route while accurately describing literal coverage. These are original-report positions, not claims of peer agreement with this successor. Lead adjudication remains necessary on the exact claim permitted for a Shift+Tab-only run; this report does not invent consensus.

## Completion and unfinished work

The assigned single cross-examination pass is complete. No further peer round or website observation is needed to finish this report. Lead work remains: adjudicate traversal claim scope; choose concise result/count wording; draft final replacement/proposed diff and preservation map; package final specification and run evidence. Actual deployed behavior remains unknown. No assigned investigation is unfinished except final completion timestamp recording immediately below.

Actual full report save completed UTC: `2026-10-17T11:49:18Z`. This is 15 seconds beyond the supplied deadline; report generation did not yield before that point. No additional investigation was undertaken after expiry. The complete available work is preserved above; unfinished lead items remain explicitly named. Administrative completion timing recorded immediately after the observed clock result.
