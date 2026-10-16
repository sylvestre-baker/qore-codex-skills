# UX — independent Analyze

## Snapshot and limits

Role: UX. Mode: Workflow because the applicable existing specification is the frozen `examples/qaizen-labs/verification-spec.md:2-18`. This report strengthens its verification protocol; it does not diagnose a website defect. The requested snapshot is `methods/planning-input.json`, snapshot SHA-256 `1461fc149209fa29adc067a2b8f3c644055228aa0a2f45485779e3a418f47fd6`, recorded 2026-10-16. Source paths below are relative to `research/qore002-implementation-20261016/methods/planning-input/` unless explicitly prefixed otherwise.

Independence: only role instructions, generated protocol/profile and frozen raw target inputs were read. No peer reports, private repositories, website requests or services were used. No source modifications were made. The actual public example root was used only for freshness and its declared offline check. The budget is 180 seconds for this initial analysis. No browser/fixture execution or screen-reader assessment was attempted.

## Preflight, actual commands and facts consumed

Read the generated `qore-plan-qaizen-labs/SKILL.md`, `references/project-profile.md`, `references/protocol.md` and `references/roles.md` before planning. Its preflight requires current returned facts before use. From `research/qore002-implementation-20261016/derived-initial/qore-plan-qaizen-labs`, executed `python3 scripts/project-check.py references/project.json --root ../../../../qore-skills/examples/qaizen-labs --method plan`; exit 0, coverage COMPLETE, no problems. A first equivalent invocation used a resolved target-root path; a portable rerun retained the complete JSON in `methods/plan/analyze/ux-preflight.json`.

Profile `qaizen-labs` version `0.1.0`, SHA-256 `f76afdd45cb6352e5044a06affc4182ea6cd40aa9c012fb216636a61faa428f0`. Both checked sources current: `surface` SHA-256 `3728739a119a53272541f83d451e40addb6939304f9d9ec060a477a87170a4a3`; `checker` SHA-256 `9ef2a0acf51f078ce290ec723ca550b8b73597e68304179fe4d0625c5757963b`. Returned `surfaces` is empty for method plan; no UX web-surface fact was imported from another method.

| Consumed fact | Source and current digest | Identifiable effect |
| --- | --- | --- |
| `surface-contract` command | `checker`, digest above | Read the frozen checker before executing its actual argument vector in the public example root. |
| `close-focus` | `surface`, digest above | Require a separate Close transition returning focus to summary; Back success cannot stand in for it. |
| `back-focus` | `surface`, digest above | Preserve sequential Tab/Shift+Tab evidence and Enter activation, rejecting mouse/programmatic-focus substitution. |
| `unanswered-scope` | `surface`, digest above | Keep every planned state unanswered and preserve mutation/origin blockers plus blocked analytics evidence. |

Executed from `qore-skills/examples/qaizen-labs`: `python3 -B checks/check_contract.py surface-contract.json`; exit 0. Result: `valid: true`, schema `qaizen-labs-surface/1`, checks `entry`, `unanswered`, `help-toggle`, `close-focus`, `keyboard-back`, `introduction-focus`, `read-only-policy`, `origin-policy`. Reported limit: contract consistency only; browser observations establish current behavior. No other executable project checks were declared for plan. Browser tests were inspected, not run: they start a local HTTP service and need a separately installed optional driver (`tests/test_browser_probe.py:13-39`), outside this analysis pass.

## Sources and current behavior of the protocol

- `examples/qaizen-labs/verification-spec.md:8-18,56-109`: old proof gap, existing reuse decision, scope, acceptance and excluded claims.
- `examples/qaizen-labs/surface-contract.json:4-20`: desktop English, 1280×800, unanswered journey, named transitions and distinct focus targets; acceptance is explicitly separate from current deployment status.
- `examples/qaizen-labs/browser-actions.json:1-109`: optional Reject, Labs entry click and URL wait, Start, initial unchecked assertion, sequential summary traversal, Enter/Space/Enter help toggle, sequential Close, summary focus, sequential Back, h1 focus and final unchecked assertion.
- `examples/qaizen-labs/observation-policy.json:1-5`: sole allowed origin.
- `examples/qaizen-labs/checks/check_contract.py:9-43`: consistency validation and its stated observation limit.
- `tools/browser_probe.mjs:54-76,77-104,105-168`: pre-entry read-only policy, captures, action execution, sequential focus events and failure retention.
- `tests/test_browser_probe.py:43-82`: existing positive/negative Back controls, legacy action coverage, blocked POST, outside-origin navigation and false-focus controls.
- `tests/test_labs_contract.py:22-51`: contract mutation and stale-profile checks.

The correction is already partly implemented: `traverse-focus` uses actual keyboard presses, records each active element and fails at a finite bound (`tools/browser_probe.mjs:127-139`); the Back action already traverses, checks focus and presses Enter (`browser-actions.json:84-101`). This must be retained and exercised, not described as missing implementation or replaced by a duplicate harness.

## Proposed interaction requirements and deliverables

1. Preserve the scoped state sequence: Labs → introduction → unanswered first question → help open → help closed by Space → help reopened → help closed by Close → returned introduction. Entry/Start are mouse-operated in this declared journey; only help and Back carry keyboard proof. Do not claim full keyboard entry coverage from this test (`surface-contract.json:9-15`). Record stable visible state and URL where applicable, not just a capture label.
2. Make state proof discriminate the returned introduction from any focused `h1`. Keep heading focus assertion, and pair it with an observable introduction identity/visibility and question absence. The contract names an introduction-heading target, but maps it only to `h1` (`surface-contract.json:15-17`); the current action list does not assert introduction content or question absence (`browser-actions.json:99-109`). Architecture should choose selectors from the actual observable interface without inventing new product text. Existing harness already supports visible/hidden/text assertions (`browser_probe.mjs:115-117`).
3. Keep three distinct help checks: Enter opens summary, Space closes summary, Close closes help and restores summary focus. Capture a help-open state, or equivalent explicit retained state evidence, alongside existing help-closed capture. Reopening currently has no explicit open assertion before traversing to Close (`browser-actions.json:56-78`); add that assertion so failure points identify the transition.
4. Retain traversal start context, each Tab/Shift+Tab step, target reached, Enter activation and resulting visible state/focus as one traceable chain. A later mouse action cannot recover a failed keyboard obligation. Finite bounds are an evidence limit, not proof of global keyboard inaccessibility; a failure report should identify bound, starting focus and observed sequence (`browser_probe.mjs:128-142`). Existing negative control already stops before its fallback click (`test_browser_probe.py:58-66`).
5. Specify bounded readiness for asynchronous UI state/focus. URL already waits 15 seconds (`browser_probe.mjs:116`). Attribute/focus checks are immediate and each preceding action gets a fixed 900 ms pause (`118-122,143`). Proposed requirement: wait for expected focus/open/visible state within a declared timeout, preserving the final observed state on timeout. This avoids classifying a merely delayed transition as a keyboard defect and makes missing transitions reproducible. Retain controls where the transition never occurs; do not turn timeouts into retries that re-activate controls.
6. Demonstrate unanswered state at question entry, after help Close and immediately before Back; retain final assertion too. Current checks are at first question and returned introduction only (`browser-actions.json:24-25,103-105`). Returning to an intro with no answer controls can make the final unchecked check vacuous. The additional middle check tests the invariant where answers exist without selecting any answer.
7. Keep read-only policy failures and product failures distinguishable in the report. Blocked analytics is expected and retained (`surface-contract.json:20`), while outside-origin navigation makes the run incomplete (`browser_probe.mjs:144`). A mutation event does not itself show the journey failed: record whether visible state/focus was still observable. A blocked request that prevents required UI readiness should produce a scoped missing observation, with request/event identity and final available capture.

Deliverables: strengthened actions/acceptance mapping; a state-observation matrix keyed to transition IDs, visible predicates, focus destinations and evidence paths; discriminating local controls for any changed assertions/waits; and a scoped final evidence report separating offline consistency, synthetic control behavior and eventual current website observation. No live observation belongs to this planning artifact.

## Content and accessibility boundaries

Use the current English control labels in the source contract. Optional cookie Reject is a possible entry variation, not a mandatory failure when absent (`browser-actions.json:1-6`). Preserve a recorded not-present outcome and enough entry evidence to distinguish banner absence from an overlay that blocks interaction (`browser_probe.mjs:110-113,142`). An ambiguous/multiple control match should be reported as an observation failure rather than silently selecting one.

Sequential reachability, Enter/Space behavior, focus restoration and captured content are narrow observable accessibility obligations. They do not establish accessible names, contrast, screen-reader announcements, mobile usability, full questionnaire coverage or certification. Desktop English only is declared (`surface-contract.json:6,20`; `verification-spec.md:109`). Empty/result/submission/error-product states and alternate locales are outside the contract and should stay explicitly untested. Recovery here means a successful user Back transition and useful retained diagnostic evidence on probe failure, not an unrequested website redesign.

## Concrete risks and hypotheses

- **State aliasing:** if a different or stale h1 receives focus, current final focus assertion can pass without proving returned introduction. Source: generic h1 mapping and no final state predicate cited above. Resolve with final intro-visible/question-hidden proof and a counterexample control focusing an incorrect heading.
- **Transient selection missed:** if help interaction temporarily selects an answer and Back clears/unmounts it, endpoint-only unchecked assertions miss it. This is an explicit hypothesis, not a current site finding. An unanswered check before Back discriminates it; QA should decide whether per-transition assertions suffice.
- **Timing false failure:** if UI settles later than the fixed 900 ms pause, immediate focus/attribute checks may fail despite eventual correct behavior. Source: `browser_probe.mjs:118-122,143`. Use delayed-positive and never-settling negative controls with finite waits.
- **Wrong failure attribution:** if blocked analytics alters visible loading or focus, reporting a general website defect without policy context is unsupported. Source: expected blocked analytics (`surface-contract.json:20`) and mutation/event retention (`browser_probe.mjs:61-63`). Retain the observation and constraint together.
- **Capture gap:** if the journey fails after the last snapshot, result/events retain failure but no explicit failure-state DOM/screenshot is requested in catch (`browser_probe.mjs:149-167`). Trace/video may help, but depend on successful persistence. Proposal: best-effort failure capture with original error preserved; Architecture/QA should assess minimal implementation and failure controls.

## Required peer questions

**Architecture:** How will final introduction state be distinguished from an arbitrary focused h1 using existing action primitives and current source-bound selectors? Can readiness use bounded predicate waits while preserving legacy actions and avoiding repeated user activation? What is the smallest safe way to retain the failure-state capture without masking the original failure? Is the existing global `[aria-selected="true"]` unchecked predicate too broad for answer-only scope (`browser_probe.mjs:124-125`), and should a scoped selector be additive rather than break legacy use?

**QA and security:** Which retained observations prove each help state independently, including reopened state before Close? Add/identify a delayed-focus positive and never-correct negative control, a focused-wrong-heading control, and an answer-selection-before-Back counterexample. How should a 24-step traversal-bound failure be reported without overclaiming website inaccessibility? Can policy-induced UI interruption remain PARTIAL with blocked event plus final capture, and what exact evidence is required before calling the scoped journey complete?

## Unfinished work

No peer cross-examination or adjudication has occurred; these are initial UX proposals. The actual website and rendered content remain unobserved by instruction. No new product selectors, accessible names or complete accessibility claims are established here. Driver execution and controls require the later authorized implementation/testing pass. A later complete scoped success still needs current rendered-state evidence, actual traversals and activation, observed focus, inspection of captures, and preserved policy effects. Profile preflight COMPLETE establishes freshness only, not completed planning protocol or UX success.
