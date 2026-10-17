# UX independent analysis — Workflow Analyze

Role: UX. Target: `/workspace/worker/target/verification-protocol.md`. Frozen target snapshot supplied by lead: `ed6c0fb8d8737cb4b8fc9e6b3485e0e618bf332d15725a557cf30d17b127e394`.

Context: fresh independent role dispatched by lead; no peer report read. Working root `/workspace/worker`; report is outside the supplied inputs. Actual analysis start: **2026-10-17 10:39:59 UTC**. End timestamp is recorded below. Deadline: 150 seconds from dispatch; complete available report returned within that budget. This is document planning, with no browser, network, native interface, rendered accessibility tree, or deployment observation.

## Sources inspected and authority

- `TASK.md:1-5`: plan changes to the existing target against original project sources, preserve input and skill resources, use only supplied resources.
- `target/verification-protocol.md:1-10`: existing six-step fixture procedure; establishes Workflow applicability and supplies the change target, not authoritative acceptance. Its explicit reconstructed-fixture provenance at line 3 must remain.
- `surface-contract.json:4-20`: authorized entry, origin, locale, viewport, unanswered/read-only scope; named states and transitions; distinct Close and Back focus destinations; required checks; public observation versus declared acceptance distinction and exclusions.
- `checks/check_contract.py:9-43`: schema and consistency checks; Back traversal and Enter requirements; validator explicitly limits itself to contract consistency. It does not inspect the target procedure or prove browser behavior.
- `observation-policy.json:1-5`: supplied navigation origin allowlist `https://qaizen.io`.
- `.agents/skills/qore-plan-qaizen-labs/SKILL.md:10-21`, `references/protocol.md:5-41`, `references/roles.md:9,20-22`, `references/specification.md:7-17`: Workflow, independent reports, cross-examination, actual file boundaries, state/accessibility requirements, evidence limits.
- `references/project-profile.md:5-28` and `references/project.json:5-77`: source-bound preflight consumption and project facts. Lead already ran current preflight; inspected `/workspace/output/profile-check.json:9-24,26-81`: COMPLETE, matching source digests, current selected plan facts. All cited original project sources were read directly; checker output is not treated as source authority.

Profile facts consumed: `close-focus`, `back-focus`, `unanswered-scope` from source `surface` digest `3728739a119a53272541f83d451e40addb6939304f9d9ec060a477a87170a4a3`; these shape UX decisions UX-D2, UX-D3, UX-D5 below. `surface-contract` command, source `checker` digest `9ef2a0acf51f078ce290ec723ca550b8b73597e68304179fe4d0625c5757963b`, is consumed as a proposed consistency gate, not an independently executed measurement in this role. The current plan checker returned no web surface (`profile-check.json:74`), so no profile-derived browser surface is claimed; the entry is independently present in `surface-contract.json:4`.

## Finding and proposed decisions

The present document reaches the expected final introduction and asserts its focus, but **clicking Back does not establish keyboard access to Back** (`target/verification-protocol.md:10`; contract `surface-contract.json:15`; explicit invariant `profile-check.json:53-55`). This is a procedure proof gap, not an observed website defect. In addition, the current procedure does not explicitly exercise the required summary Space toggle and Enter reopen transitions (`surface-contract.json:12-13`) or define observation policy setup before navigation (`surface-contract.json:6,18,20`).

**UX-D1 — Preserve and expand the single existing journey.** Revise the six-step procedure in place in its eventual implementation, preserving entry, unanswered scope, Close focus, final absence assertions, and fixture/provenance wording. Do not introduce a second journey that could drift or a website implementation change without runtime evidence. Sources: `TASK.md:3-5`, target lines 3-10, contract lines 7-20.

**UX-D2 — Exercise the complete help interaction chain before Back.** From first question, focus the summary and activate Enter; assert help open. With summary focused, activate Space; assert help closed. Activate Enter again; assert help reopened. Reach Close by sequential Tab, assert Close holds focus before activation, press Enter, then assert help closed and the same summary holds focus. Use literal Tab for this planned main path, satisfying the contract's Close traversal (`surface-contract.json:11-14`). The existing target's Tab-or-Shift+Tab Close wording is broader than the declared Close transition; literal Tab removes that ambiguity without imposing additional UI behavior. Never force focus onto Close to claim this reachability proof. Focus assertions may inspect the active element; they must not change it.

**UX-D3 — Prove Back traversal separately from return focus.** Starting from the summary after Close, press sequential Tab until the application Back control has focus; record the actual key sequence and focused control identity, press Enter, then assert the introduction is visible, the first-question and help are absent from the presented interactive state, and the introduction's heading holds focus. This is application Back, not browser history Back. Contract declares Tab (`surface-contract.json:15`); the checker permits Tab or Shift+Tab (`checks/check_contract.py:35-36`) and current profile invariant permits either, but the proposed main path uses Tab to satisfy all without policy ambiguity. A separate Shift+Tab exploration is optional and must not replace the declared Tab proof. No click, locator focus(), or equivalent focus assignment may substitute for traversal.

**UX-D4 — Keep transition, reachability, and focus evidence distinct.** Every state transition has a visible/semantic state assertion. For Close and Back, record focused control before Enter and destination focus after Enter. A screenshot showing the introduction, or even an active heading assertion alone, cannot establish how Back was reached. Read activeElement or equivalent semantic focus identity; establish that the heading belongs to the introduction rather than matching an arbitrary `h1`. Do not overfit DOM IDs, styles, component internals, or exact tab counts absent from supplied sources (`surface-contract.json:17`). The target already requires the question and help absent on return; define this as absent from visible, accessible, interactive presentation, with no focus left in the departed question/help. DOM deletion is an unproven implementation requirement, not a necessary acceptance obligation.

**UX-D5 — Set observation boundaries before the first navigation.** Use en-US and 1280×800 (`surface-contract.json:6`), start at `https://qaizen.io/labs`, click the link matching `a[href$='/labs/readiness-check']`, and verify the destination stays on the allowed origin. Before navigation, arrange denial of all non-GET/HEAD/OPTIONS requests and disallowed-origin main-frame/popup navigation; retain attempted method/destination/block/effect observations. Use the intersection of supplied contract and observation-policy allowlists if they ever disagree, stop to report disagreement, and never silently expand access. An expected analytics POST remains blocked and its effects are recorded (`surface-contract.json:20`; current `unanswered-scope` invariant). Do not assert the journey succeeded simply because analytics was blocked.

**UX-D6 — Keep the question unanswered throughout.** Assert the first question is initially unanswered and remains so after help toggling and Close; never select any answer, submit a form, or generate a result. Record that the final return exposes the introduction and removes question/help from interactive presentation. A later question rerender is outside scope; do not claim answer persistence across a re-entry not performed. Source: `surface-contract.json:6,18,20`; target lines 6,9-10.

## State and interaction requirements / deliverable

The planned revised procedure should contain this linear chain, with one evidence record per transition:

| Transition | Action / precondition | Observable outcome |
| --- | --- | --- |
| entry | Public Labs entry; click declared journey link | Introduction visible; allowed origin retained |
| start | Introduction; click Start the check | First question visible and unanswered |
| open-help | Summary focused; Enter | Help open |
| toggle-help | Summary focused; Space | Help closed |
| reopen-help | Summary focused; Enter | Help open again |
| close-help | Reach Close with sequential Tab; record focus; Enter | Help closed; summary focused; question still unanswered |
| back | From post-Close state reach application Back with sequential Tab; record focus; Enter | Introduction visible; question/help absent from presented state; introduction heading focused |

This table reflects `surface-contract.json:9-17`; it is acceptance planning, not a run log. Open/closed may be observed through relevant visible content and the disclosure's semantic state where present; do not invent an ARIA attribute requirement unsupported by current markup. Native summary semantics can supply state. The plan should require sufficient observations to identify controls and states without prescribing a new UI framework.

Content/accessibility: preserve English control names from the contract and record actual accessible control identities during future execution. The contract binds locale and viewport, not translations or responsive behavior. The summary's Enter/Space behavior, focus restoration after Close, sequential access to Back, and introduction heading focus are the applicable narrow accessibility acceptance obligations; this is not an accessibility certification (`surface-contract.json:20`).

Loading/recovery: no rendered loading, empty, or error states are supplied. Propose condition-based bounded waits for the required state and label timeouts or intercepted-navigation failures as blocked/unresolved observations with the last reached state. Do not record a missing state as passed or continue with a forced DOM state. A fresh reset may be used for a new clearly identified attempt after a failed run while preserving the failed attempt's evidence; reruns must retain boundaries and unanswered policy. These are proposed test execution rules, not claims about existing recovery UI. Do not add UI redesign, empty-state copy, spinners, or localization work based on hypotheses.

Deliverables to lead: incorporate UX-D1–D6 into the consolidated specification, a revised-procedure task, Gherkin scenarios mapped to declared stories/decisions, and a future observation evidence template capturing state/action/focus/policy/effect. No website changes or runtime evidence are supplied by this report.

## Proposed acceptance/checks and their limits

- UX-AC1: From the declared entry under the declared locale, viewport, origin and method restrictions, the declared link and Start actions reach the unanswered first question. Inspect state and policy evidence. This remains planned.
- UX-AC2: Enter opens help, Space closes help, and Enter reopens it; each state is observed separately. This catches the help-toggle gap in the target, not just the Back gap.
- UX-AC3: The focused Close control is reached by sequential Tab, activated by Enter, and help closes with summary focus. Preserve unanswered evidence at this checkpoint.
- UX-AC4: Starting after UX-AC3, sequential Tab reaches the application Back control; Enter returns the introduction with heading focus and no question/help in presented interactive state. Retain both the input trace and focus observations; do not collapse this into UX-AC3.
- UX-AC5: Attempts outside allowed methods/origins are denied according to policy; expected blocked analytics and resulting effects are retained. Do not relax the guard if blocking prevents a state.
- UX-AC6: `python3 -B checks/check_contract.py surface-contract.json` may establish unchanged contract consistency only. It cannot pass UX-AC1–5 or detect the target's clicked Back itself (`checks/check_contract.py:42-43`). Specification structural lint likewise cannot establish browser conformance.

## Risks and triggered handling

| ID / severity | Trigger and affected behavior | Evidence or hypothesis; check / response |
| --- | --- | --- |
| UX-R1 High | Back reached by click or direct focus, then heading correctly focused; false keyboard pass | Actual target line 10; contract line 15 and checker lines 35-36. Require sequential input trace plus pre-Enter focus. |
| UX-R2 High | Close focus passes and is substituted for Back evidence | Distinct contract focus targets at lines 14-17; current profile close-focus. Separate acceptance records. |
| UX-R3 Medium | Space toggle/reopen never exercised; incomplete help contract | Actual target lines 7-8 omit contract lines 12-13. Require all three disclosure transitions. |
| UX-R4 High | Observation guard installed late or loosened for analytics; read-only/origin breach | Contract lines 6,18,20; observation-policy lines 2-4; profile invariant. Setup before entry and retain denials/effects. |
| UX-R5 Medium | Generic h1 or screenshot is accepted as introduction focus; focus is elsewhere | Hypothesis grounded in generic focus target `h1`, contract line 17. Identify introduction container/heading semantically in actual future markup; inspect active element. |
| UX-R6 Medium | Loading/interception prevents required state; procedure assumes successful transition | Hypothesis; contract line 20 anticipates blocked analytics effects. Bound waits, retain last state, report blocked/unresolved evidence. |
| UX-R7 Medium | Hidden question/help remains focusable or exposed after return; superficial visibility passes | Hypothesis grounded in target line 10's absence requirement. Check returned interactive presentation and active heading, without prescribing DOM removal. |
| UX-R8 Medium | Validator pass is presented as deployed accessibility or journey pass | Explicit checker limit lines 42-43, contract provenance lines 19-20. Keep static validation, planned checks and observations separate. |

Severity is planning judgement about misleading acceptance or policy violations, not measured website incident severity.

## Named peer questions and alternatives for later challenge

**Architecture:** Does the design remain a change to the existing procedure, using existing contract/validator boundaries, or add a browser framework, app changes, extra contract schema, or duplicate procedure? Please justify each additional surface against a concrete requirement. Smallest useful investigation: trace the target's consumers and the contract check's actual input; avoid inventing application services for a document change (`roles.md:20`). Also confirm that defining absence as no visible/accessible/focusable departed state preserves the target's intent without requiring an unsupported DOM-removal implementation.

**QA and security:** Does the matrix prove every declared help state and the Back transition separately, retaining actual Tab/Enter input, focused control before activation, and correct focus afterward? What concrete evidence prevents a click or focus() followed by a heading assertion from passing? Smallest useful investigation: map contract transitions 9-15 against proposed scenarios and require the clicked-Back counterexample to fail. Confirm that the policy check distinguishes navigation-origin guards from all-request method guards and retains blocked analytics effects without requiring all cross-origin subresources to be blocked.

Alternative A (recommended): literal Tab for both Close and Back in the primary procedure; simplest exact contract alignment. Alternative B: permit Tab or Shift+Tab for Back as checker/profile allow, recording which path was used; acceptable only if lead explicitly resolves that wording against the narrower transition declaration. Rejected alternative: retain clicked Back because returned heading focus is asserted; it proves a different property. Deferred alternative: automate the journey immediately; runtime/tool choice is outside supplied implementation and unnecessary to state the acceptance contract.

## Uninspected scope and unfinished evidence

No peer reports have been inspected; cross-examination is pending the lead's report barrier. No deployed website, website source, browser runtime, network effect, actual DOM/accessibility tree, keyboard order, focus ring, loading/recovery UI, translations, mobile viewport, full questionnaire, result generation, performance, or accessibility certification was inspected. Private source commit identity cannot identify deployment (`surface-contract.json:20`). No supplied source establishes current deployment behavior.

Unfinished evidence: actual future allowed browser observations for UX-AC1–5; control/heading identity and observed state semantics; policy interception effects; execution timestamps and input/focus records. Static validator measurement is owned by lead/QA unless separately delegated; this role inspected its source only. No missing evidence is recast as a measured defect or a passed check. All initial independent-analysis deliverables are present; remaining work is the explicitly scheduled cross-examination and eventual lead adjudication.

Actual analysis end: **2026-10-17 10:41:36 UTC**. Independent Analyze report complete; returned before the 150-second worker deadline. No input edits, network requests, or runtime observations were made.
