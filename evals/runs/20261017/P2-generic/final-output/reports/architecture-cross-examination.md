# Architecture — Workflow cross-examination (one pass)

Actual context: `/root/architecture`. Target prepared-input manifest: `e9aeec2eee10b52c3339b53b4e491d3ff69f57c68be2f5ea1d61e70df55acccc`. This is the single assigned Workflow Cross-examine pass after the lead's report barrier. Initial report remains unchanged. Dispatch anchor supplied by lead: `2026-10-17T11:45:46Z`; stop deadline: `2026-10-17T11:47:16Z`. First clock observation this pass: `2026-10-17 11:45:55 UTC`.

## Sources and scope

Read all five complete initial reports at `/workspace/output/reports/{product,architecture,ux,delivery,qa}-analysis.md`. An initial combined read was truncated; complete Product/QA and UX/Delivery reads recovered the relevant full reports, and my own complete Architecture report was authored/inspected during the initial pass. Re-read raw `/workspace/worker/surface-contract.json:1–21`, `checks/check_contract.py:1–54`, `target/verification-protocol.md:1–10`, and `observation-policy.json:1–5` for disputed facts. Previously inspected TASK and qore-plan protocol/roles remain applicable. Also received Delivery's cross-examination message explicitly revising D5 to reject mandatory extra-direction runs and to distinguish procedure completion from literal Tab evidence.

Uninspected: current website, browser/runtime/network evidence, application internals, broader repository consumers, external sources, and other roles' cross-examination files. No browser/network call or input edit occurred. No validator rerun was needed: there is no input change or new validator concern. This pass challenges the documentation plan, not an asserted website defect.

## Material traversal dispute: A3 / Delivery D5 / QA D4 / Product decision 6

**Exact initial divergence.** Architecture A3 and Delivery D5 made the forward Tab route canonical and characterized Shift+Tab as supplemental; QA D4 says one observed permitted sequential path suffices for the current target. Product decision 6 preserves either direction. UX calls for canonical Tab but explicitly asks that the alternative remain valid. All sources must be retained rather than treating a vote or checker pass as authority resolution.

**Direct evidence.** `surface-contract.json:14–15` has literal `traversal: "Tab"` for Close and Back. `target/verification-protocol.md:8,10` expressly permits Tab or Shift+Tab for both. `checks/check_contract.py:35–36` allows either value for Back; it does not impose or validate Close traversal direction. The checker validates the JSON, not the target or a runtime trace (`:42–43`). Thus a passing checker proves neither direction was exercised, and its accepted vocabulary alone does not change the concrete contract's Tab value.

**Concrete counterexample to an overly strict A3.** Suppose a future observation reaches Back with Shift+Tab in 3 steps and all state/focus assertions pass, while forward Tab would require 25 steps. No such runtime behavior was observed; this is a bounded logical counterexample. The maintained target's explicit either-direction/24-step rule can be satisfied by the reverse path. Calling that target run invalid solely because it lacks an additional forward run adds acceptance beyond the supplied procedure and can make retained wording meaningless. Conversely calling that reverse trace an observed successful forward-Tab trace would invent evidence.

**Revised Architecture recommendation (A3-R).** Document Tab as the recommended primary path because it matches the concrete contract. Preserve Shift+Tab as a permitted alternative for both Close and Back; retain the known asymmetry that checker support is explicit only for Back. One permitted sequential path per transition is sufficient for this procedure. Record actual direction/count, activation, resulting state and focus. Do not require both directions or an extra run, do not label a permitted reverse-only run a procedural failure, and do not claim an unexercised direction was observed.

Suggested concise wording: “Use Tab, as declared in the contract; this procedure also permits Shift+Tab for sequential traversal. Record the direction actually used. A passing alternative trace establishes that path, not an untested direction.” The 24-step Back bound applies to whichever permitted Back traversal is used. No new numeric Close bound is introduced.

**Retained strict interpretation/dissent.** If a later reviewer wants to claim exact literal conformity to every JSON transition field, a reverse-only trace leaves literal forward-Tab behavior unobserved. That is a sourced limitation of the claim, grounded in contract `:14–15`, not a reason to erase the target's permitted alternative or mandate both paths in this documentation clarification. The lead should state this distinction in adjudication; it should not describe all source texts as identical. This revises A3's implication that reverse is valid only as a supplementary run while preserving its direction-specific evidence concern. Delivery independently supplied the same distinction during this pass.

Smallest investigation completed: compare only raw transition rows 14–15, checker 32–36 and target 8–10. No website probe, JSON change, new validator, or user confirmation is needed to settle the documentation choice.

Severity: Medium for evidence fidelity if a reverse-only trace is labeled literal forward-Tab proof; Medium for unjustified scope/acceptance expansion if an extra run becomes mandatory. Neither is a measured runtime defect.

## Product challenge: ambiguous “every declared transition” invariant

**Decision challenged.** Product's measurable acceptance says every declared transition has an explicit corresponding instruction and maps Close/Back to contract lines 14–15, while decision 6 preserves either direction.

**Failure case.** A matrix can mark “literal contract trace observed” after only a Shift+Tab run if “mapped” is silently treated as “all exact fields observed.” The reverse logical counterexample above makes the ambiguity concrete. This would overstate evidence even while satisfying the procedure's explicit alternatives.

**Smallest correction.** Keep the seven-transition documentation mapping, but distinguish “expected declared field,” “permitted procedural alternative,” and “actual observed input.” Coverage mapping is a static review result, not a runtime conformance claim. The maintainer needs only one chosen route and an honest direction record, not a new runtime matrix in the body of the procedure. Proposed decision: accept Product's small document-plus-review-map outcome and clarify this one invariant, rather than expanding the checklist into a testing product.

**Refutation preserved.** Product does not propose a Back-only fix, an application change, or mandatory browser execution. Any Architecture/Delivery challenge premised on those proposals would fail against Product decisions 1,4,8 and unfinished-work statements. Those challenges are resolved by the actual report; no scope defect is established.

Severity: Medium if declaration/observation distinction is lost; otherwise documentation is sufficient. Existing unanswered-after-Close and unanswered-immediately-before-Back checkpoints remain separate even when adjacent in prose; neither is deleted for brevity.

## UX challenge: complexity and implied focus guarantees

**Decision challenged.** UX interaction table and decision 5 require distinct observed states and focus outcomes; my initial A4 requested a resulting focus sequence, and UX discusses recording last focus at exhaustion.

**Concrete failure/complexity case.** An instruction to inventory every focus movement and require a second canonical route could turn the short maintained procedure into an instrumentation specification, despite the task requesting documentation only. It could also imply summary focus is a declared postcondition after Space/Enter help toggles, whereas the contract supplies `focus_after` only for Close and Back (`surface-contract.json:11–17`). The focus required to activate a control is not an extra post-action focus acceptance obligation.

**Smallest correction.** Keep Enter-open → Space-close → Enter-reopen as explicit state checks, then separate Close and Back active-focus assertions. Require enough traversal evidence to establish actual sequential movement and count Back steps; a compact key/direction/count record plus relevant focused controls suffices. An exhaustive focus log or screenshot set can be optional; do not introduce mandatory storage or tooling. After a toggle, ensure summary is the active control before its next prescribed key by ordinary navigation if needed; do not invent an obligation that focus remained there unless observed and separately reported. Read-only active-element inspection is evidence; programmatically moving focus to skip required traversal is not.

**Refutation preserved.** UX already explicitly avoids a full accessibility audit, unsupported loading/error screens, source changes and focus-forcing shortcuts. No actual UX complexity defect is proved in that report. The correction primarily narrows my own evidence prescription and guards final drafting against adding unsourced focus invariants.

Severity: Low for verbosity/maintenance burden; Medium if invented post-toggle focus expectations become a false acceptance failure. Smallest investigation completed: compare the actual focus fields in contract `:11–17`; no DOM inspection is needed for this planning distinction.

## QA warnings: failure paths and outcome classification

**Q1 — 24-step exhaustion.** QA N4 and its Gherkin say the bounded Back proof fails; UX/Product/Architecture often say inability to complete/incomplete. These are compatible if recorded per assertion. When Back is not reached after 24 traversal keystrokes, the procedure's bounded reachability assertion is not met, and the last focused element/count must be recorded. Enter activation, returned introduction, absence of question/help, and heading focus are NOT OBSERVED because they were not exercised. There is no global website defect or contract-level 24-step accessibility limit established by that result. Preserve the old cap; do not reset it midway, add 24 steps per direction, or force-focus/click to fabricate a pass. An additional run would need its own independent record and cannot overwrite the original bounded outcome.

**Q2 — Visibility passes while focus fails.** QA's separate state/focus Gherkin is useful and agrees with contract `:14–17`. Retain per-assertion outcomes: closed help can pass while summary focus fails; visible introduction can pass while introduction-heading focus fails. A broad “Back passed” label must not hide that distinction. No source supports deleting the original return absence assertions.

**Q3 — Blocking versus behavior.** An expected denied analytics POST is policy-compliant (`surface-contract.json:20`). If other assertions remain observable, record them on their facts; if blocked effects prevent observation, those downstream checks are NOT OBSERVED/BLOCKED. A directly observed wrong focus/state is a failed obligation even if a block may have contributed; record the effect/context without removing the expected acceptance obligation or claiming causality without evidence. Never loosen methods/origins to obtain a pass.

**Q4 — Negative-test expansion.** QA N1/N2 mention proposed policy tests for deceptive origins and disallowed methods. They are reasonable review examples, but no supplied task requires active request injection, guard implementation, or browser/security testing to complete this documentation plan. Keep them as hypothetical failure handling/static examples, or explicitly deferred future tests. The procedure must cover actual requests and redirect destinations if later executed, with exact origin matching; it need not prescribe a new interceptor or security test suite.

Severity: Medium for blanket outcome misclassification; High for bypassing request policy, grounded in contract `:5–6,20` and policy `:2–4`. No live occurrence was measured. Smallest useful investigation was the source/evidence cross-check already completed, not a runtime test.

## Reuse, sequence and cross-boundary confirmation

The initial reuse/impact sweep stands: only the Markdown procedure is a proposed change; contract/policy/checker are reused unchanged, and reports/draft/diff remain under `/workspace/output`. No local service/database/transaction machinery is supplied or needed. The actual future trust boundary is observation requests from a browser to the sole allowed origin; policy is configured before navigation, applied throughout to requests/redirects, and effects retained. Its enforcement implementation remains unspecified because none was supplied.

Component flow remains source declarations → maintained procedure → future executor → observation record → reviewer, with a separate JSON → checker → consistency-result path. Runtime order remains guarded entry click → Start click unanswered → summary Enter/Space/Enter with state observations → sequential Close/Enter and summary focus → unanswered checkpoints → bounded sequential Back/Enter → introduction visible, question/help absent, heading focused. This pass does not add a transaction, retry or deployment dependency.

The minimum final maintainer document can therefore be a setup block, concise numbered journey and evidence note, with the full obligation/preservation map in review artifacts. Product's small-scope choice, UX's explicit transitions and QA's separate outcomes fit this architecture without new infrastructure. Delivery's time estimates are proposals, not measurements of current website or implementation complexity, and do not block drafting.

## Decisions retained, revisions and unfinished work

Retain A1/A2/A4–A7 in substance: preserve existing obligations/provenance; add full help sequence and guardrails; keep 24 as the existing Back observation bound; separate checker/prose/runtime evidence; retain failure effects. Revise A3 as A3-R above and narrow A4's focus-log wording to sufficient evidence rather than mandatory exhaustive instrumentation. Reject an extra mandatory direction run and reject any claim that checker latitude alone proves literal Tab behavior. No further round or peer wait is required by this role.

Completed in this pass: all returned initial reports reviewed; direct source conflict checked; named Product and UX challenges made; QA failure paths assessed; the material A3 conflict resolved as this role's recommendation with the exact-field minority concern preserved; no source changes or website claims made. Unfinished: lead adjudication, final replacement/diff and preservation map, actual current-site observations (outside scope). The lead must not call literal forward-Tab behavior observed when the record contains only reverse traversal. This remaining evidence limit does not block the documentation plan.
