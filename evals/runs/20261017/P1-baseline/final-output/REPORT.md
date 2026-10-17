# Plan for the journey verification protocol

The protocol needs a demonstrated keyboard return journey, the complete help toggle sequence, and explicit observation safeguards. This is a documentation plan: no supplied file was changed and no website was contacted. The local contract consistency check passed; current website behavior remains untested.

## Authority and evidence

The project authorities are [surface-contract.json](/workspace/worker/surface-contract.json:1), [check_contract.py](/workspace/worker/checks/check_contract.py:9), and [observation-policy.json](/workspace/worker/observation-policy.json:1), as directed by [TASK.md](/workspace/worker/TASK.md:3). The [existing protocol](/workspace/worker/target/verification-protocol.md:3) is a reconstructed task fixture, not historical evidence or project authority.

Source references used below:

| Reference | Location and obligation |
| --- | --- |
| S1 | Contract lines 4–6: entry URL, authorized origin, en-US, 1280×800, entry/state depth, unanswered policy, GET/HEAD/OPTIONS only. |
| S2 | Contract lines 7–15: six state IDs and seven exact transitions, controls, activations, and specified Tab traversal. |
| S3 | Contract lines 14–18: Close → summary focus; Back → introduction heading (`h1`) focus; all eight required checks. |
| S4 | Contract lines 19–20: public provenance, dated baseline, expectations versus observations, excluded scope, blocked analytics POST effects, and deployment identity limits. |
| S5 | Checker lines 12–18, 23–43: HTTPS entry authorization, read-only scope, transition consistency, distinct focus destinations, sequential Back activation, required checks, and validation limits. |
| S6 | Observation policy lines 2–4: only `https://qaizen.io` is authorized. |

## Proposed changes and priorities

Priority describes the effect on verification assurance, not website defect severity. No deployment defect is established by these inputs.

| Decision | Evidence and change | Acceptance criterion |
| --- | --- | --- |
| D1 — High priority: repair Back proof | Target line 10 clicks Back. S2/S3 require Tab traversal and Enter. Replace that action with sequential Tab from the summary after Close, record Back as the focused element, press Enter, and observe the result without further focus changes. | A trace shows Tab reaching the intended Back control, its focus immediately before Enter, Enter dispatch, returned introduction, and actual focus on the introduction `h1`. A click, scripted `.focus()`, or direct handler invocation does not satisfy keyboard-back. |
| D2 — Medium priority: complete help behavior | Target line 7 leaves activation unspecified and omits two transitions. Under S2, use Enter to open, Space on summary to close, Enter on summary to reopen, then Tab to Close and Enter to close. Change target line 8's “Tab or Shift+Tab” to the supplied contract's Tab. | Every help transition has its own observed before/after state and activation. Close leaves help closed and focus on the summary; this is distinct from the heading focus required after Back. |
| D3 — High priority before future observation: state safeguards | The target has no request enforcement procedure. Add a guard before any navigation using the exact origin shared by S1 and S6 and the method set in S1. | All actual requests and redirects are subject to origin and method checks. Unauthorized origins and methods are blocked before transmission. Expected analytics POST attempts remain blocked, and their observed effects are retained. No answers, submissions, or result generation occur. |
| D4 — Medium priority: make setup and entry repeatable | Target lines 5–6 omit the specified locale, viewport, link selector and exact start control. Add these from S1/S2, plus an unanswered invariant throughout the journey. | At en-US and 1280×800, start at the declared Labs URL, click `a[href$='/labs/readiness-check']` to introduction, click “Start the check” to first-question, and never select an answer. Record state and selected-answer evidence before help, after Close and before Back. |
| D5 — Medium priority: distinguish outcomes from expectations | The fixture contains assertions but no evidence/result convention. Add a per-transition record and final check matrix under S3–S5. | Record expected/observed values, pass/fail/not-run/blocked status, evidence references, timestamps, and limitations. The contract check's success is never substituted for browser proof. Preserve failures and intervention effects. |
| D6 — Medium priority: scope and provenance | Preserve the fixture disclaimer and add S4's public URLs, dates, and limitations. | Describe 2026-10-15 as the supplied baseline observation date and 2026-10-16 as the protocol proof-gap date. Do not claim either establishes current deployment behavior. Private source commits do not identify deployment. |

Implementation order: add setup/guard and evidence conventions; replace the journey steps; map the eight checks to evidence; review locally. The only proposed project edit is to `target/verification-protocol.md`. No website code change is supported by the supplied evidence. A complete proposed replacement is saved as [verification-protocol.proposed.md](/workspace/output/verification-protocol.proposed.md).

## Acceptance and future browser checks

This table is a future verification specification, **not a record of executed browser checks**. Every row is currently not run. Live execution is prohibited in this recorded task.

| Required check | Future action and required evidence | Pass condition |
| --- | --- | --- |
| entry | Record locale/viewport and initial URL; click the contract link from Labs, observe introduction; click “Start the check,” observe first-question. | Expected states and controls are observed in order on the authorized origin. |
| unanswered | Inspect answer selection state without selecting any option, before help and after Close; retain the invariant for the entire trace. | No answer is selected or submitted and no result is generated. A screenshot alone is insufficient if it cannot establish selection state. |
| help-toggle | On the relevant summary press Enter, Space, Enter, observing each transition. | `first-question → help-open → help-closed → help-open` occurs with the specified keys. |
| close-focus | Traverse with Tab to Close; capture its focus; press Enter; capture help state and actual focused element before any further navigation. | Help is closed and the relevant summary is focused. |
| keyboard-back | From summary after Close, use Tab to Back, recording the actual traversal, focused Back and Enter activation. | Back is reachable sequentially and Enter causes `help-closed → returned-introduction`. Seeing the introduction after a click cannot pass this check. |
| introduction-focus | Immediately after the Back transition settles, inspect active element and introduction identity without correcting focus. | Introduction is visible and its `h1` is focused. Preserve the target's question/help absence assertions as supplementary observations; distinguish hidden versus removed if relevant. |
| read-only-policy | Install method interception before navigation, verify guard operation offline, retain allowed/blocked request metadata and effects. | Only GET, HEAD and OPTIONS can be sent, no prohibited user actions occur, and analytics POST is blocked if attempted. Its absence is not a failure; its presence is not permission to send it. |
| origin-policy | Compare parsed exact origins against both sources, enforce redirects and subordinate requests as well as top-level navigation. | Every transmitted request is to `https://qaizen.io`; all other origins are blocked. If coverage cannot be established, mark the check blocked/unproven. |

Record enough identity to disambiguate the journey controls and introduction heading without redistributing website source. Capture actual focus, not just visual highlighting or the existence of a heading. Use bounded, recorded waits for state changes and a declared finite traversal limit; failure to reach a control remains failure/blocked evidence, never a reason to switch to a click. Do not guess the tab count, DOM details, help implementation, or current deployment identity from this fixture.

## Local checks actually performed

1. Read all five supplied files, including the three original project sources. Compared the target's steps with every declared transition, focus destination, required check, provenance statement and limit.
2. Executed `python3 -B checks/check_contract.py surface-contract.json` from `/workspace/worker`: exit 0, `valid: true`, schema `qaizen-labs-surface/1`, all eight required check IDs returned. Full stdout/stderr, command and execution timestamps are in [checks.json](/workspace/output/checks.json).
3. Compared the observation-policy origin list with the contract's list: they agree exactly. This is an offline source check, not proof of request enforcement.
4. Hashed all supplied files before output generation and compared them again at completion. The comparison is recorded in [input-integrity.json](/workspace/output/input-integrity.json). No input was modified.

The checker validates the contract data. It neither reads this protocol nor runs a browser, and it does not fully enforce every transition's specific key/traversal or the separate observation-policy file. Passing it is necessary local evidence, not sufficient evidence that the proposed procedure or deployment passes.

## Interpretations tested and rejected

| Interpretation | Disposition and source |
| --- | --- |
| A successful mouse Back plus heading-focus assertion proves keyboard Back. | Rejected: focus after navigation does not establish sequential reachability or Enter activation. S2/S5 require both. |
| Since the checker permits Shift+Tab for Back, the plan can freely substitute it for Tab. | Rejected for this supplied contract: S5 accepts either direction generically, but S2 specifically declares Tab for both Close and Back. Use Tab here. |
| The contract's successful local validation proves the website passes. | Rejected explicitly by checker line 43 and S4. |
| The keyboard proof gap is a known website bug. | Rejected by S4 and the target's fixture disclaimer. The proven issue is protocol coverage. |
| Expected analytics traffic may be sent, or its effects discarded as irrelevant. | Rejected: S4 expects a blocked POST and requires retaining observed effects. Blocking may influence behavior and must be disclosed. |
| Introduction focus implies the question/help absence assertions are automatically established. | Rejected: focus and visibility are separate observations. Retain those target assertions, but do not invent additional contract obligations about DOM removal. |

## Limits and actual outcome

The sourced plan and proposed replacement are complete. The original protocol remains unchanged. No browser, network, search, connector, website source, private commit, or external resource was used. Missing coverage is all current-deployment behavior, actual keyboard reachability, actual focus outcomes, and runtime origin/method enforcement. Those require a later separately authorized observation environment; this plan does not report them as passed.

Scope excludes answers, result generation, form submission, website source redistribution, mobile coverage, the complete questionnaire, performance testing, and accessibility certification. Record the effects of any blocked analytics request rather than generalizing observations to an unrestricted deployment.

This is a baseline task. It invokes no Qore skill and no independent role method. There were no child contexts, finder/verifier phases, role barriers or cross-examinations to execute. No Qore execution contract or structural validator is applicable, and no Qore phases have been invented. Operational identity, timing, resource availability and an empty requested/returned/missing child roster are recorded in [run-record.json](/workspace/output/run-record.json). The supplied target snapshot digest identifies the whole prepared input manifest; individual file hashes are recorded separately and do not purport to reproduce that digest.
