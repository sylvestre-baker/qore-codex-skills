# UX cross-examination

Status: COMPLETE — one bounded UX cross pass after the five-report barrier. This is a fresh UX cross-examination context; the initial UX analyst's context was retired by runtime. No identity continuity or fresh independent initial analysis is claimed. Initial report and original claims are preserved. No lead proposed procedure or peer cross report was read. No browser, network, application edit, or input change occurred.

## Evidence inspected and limits

Read the full Product, Architecture, UX, Delivery and QA initial reports at `/workspace/output/reports/{product,architecture,ux,delivery,qa}-analysis.md`, plus the cross brief and original UX claims. Raw sources rechecked: `surface-contract.json` in full, `target/verification-protocol.md` in full, `checks/check_contract.py` in full, `observation-policy.json` in full, and current project profile and `/workspace/output/evidence/profile-check.json`. The profile check reports current source hashes; I did not independently rerun its check. Read the planning skill. The original UX report supplies the original task scope; this pass rechecked the material disputed facts directly.

The runtime replacement is an execution limitation, not missing cross coverage. Actual UI, tab order, focused elements, unanswered-state representation and request enforcement remain unknown. No observed website defect follows from a procedure omission or bound exhaustion.

## Mandatory Architecture complexity challenge

Exact decision challenged: Architecture A4 says to ensure guards before entry and across new main frames/popups, “otherwise stop as unable to verify under policy.” Architecture A1/A5 also say documentation-only, no guard implementation and no browser pass required. These are compatible only if the stop is a future execution prerequisite, not a prerequisite to completing this plan. Concrete failure case: a maintainer sees A4 during documentation review, discovers no supplied observer, and starts building a harness or refuses documentation acceptance. That adds work despite TASK's documentation-only boundary and A1.

Source evidence: the existing checker consumes only contract JSON (`checks/check_contract.py:46-51`) and returns consistency-only (`:42-43`); it contains no request interception or browser runtime. `observation-policy.json:2-4` supplies an origin value, not enforcement. `surface-contract.json:6,20` supplies method restrictions and blocked analytics retention. The current project profile's `unanswered-scope` invariant supplies the precise main-frame/popup policy wording; this implementation-scope detail is profile-supported and must not be attributed solely to the raw contract's `allowed_origins` field.

Smallest investigation: compare proposed prerequisite wording to these four source locations and verify it names no runtime API, schema, new executable or required deployment result. No browser investigation is needed for this planning choice. Selected correction: a short setup paragraph states future observer requirements and marks enforcement unknown until a separate authorized run; unavailable enforcement stops that future run. Documentation readiness remains source review plus existing offline check. Accept Architecture's reuse/no-new-component design with that wording restriction.

UX explicitly revises its initial preference that “one short setup paragraph and a single expanded help sequence” necessarily suffice: brevity is a preference, not a coverage criterion. Keep a small evidence note wherever necessary to distinguish policy prerequisites, actual observations and outcomes. No new storage schema or fixed form is needed.

## Mandatory QA observable-state challenge

Exact decisions challenged: QA decision 1 and the `close-focus` matrix row merge “Tab/Shift+Tab” for Close; QA notes the checker accepts either “even though this instance declares Tab.” That checker condition actually tests only `back` (`checks/check_contract.py:35-36`). Its close test checks the focus destination (`:32-34`), not either traversal direction. The canonical Close contract is explicitly Tab (`surface-contract.json:14`), while the existing target allows Tab or Shift+Tab (`target/verification-protocol.md:8`). QA's combined row could permit a Shift+Tab-only trace to be reported as observed canonical Tab coverage.

Concrete failure: an observer reaches Close with Shift+Tab, activates Enter and observes summary focus, then marks every contract transition observed. The target alternative was exercised, but canonical Tab traversal was never observed. Neither checker success nor correct final focus fills that evidence gap.

Smallest investigation: compare contract line 14, target line 8 and checker lines 32-36; no website inspection needed. Selected correction: preserve the target's Tab/Shift+Tab alternative, recommend Tab for the canonical contract run, record the actual direction, and label Shift+Tab Close as alternative-path evidence. If only Shift+Tab is exercised, canonical Tab traversal remains not observed; do not silently remove the valid target alternative, alter JSON, or require an immediate second live run. This is a distinction in evidence claims, not a new product interaction.

QA decision 4 and its focus-failure Gherkin are otherwise strong: introduction visible does not prove introduction heading focused. Retain per-transition observations for Enter-open, Space-close, Enter-reopen; separate actual summary focus after Close from actual returned-introduction h1 focus after Back. A photograph of a heading alone cannot show the active element. Raw contract declares summary/h1 targets, not any deployed DOM shape; use the actual focused element within the correct state rather than inventing selectors or visibility machinery.

Minimal unanswered evidence: record no answer selected at the first-question checkpoint after Close and again immediately before Back traversal. An observation at Start alone cannot fill either later checkpoint. Do not invent a state detector or select an answer to check it. The deployed representation remains future observation work.

## Additional peer decisions and verdict precision

Product P1 and P5 correctly preserve the bound and separate obligations from current behavior. Challenge their broad “pass/fail/not observed” wording only insofar as it could collapse three different cases: (1) Back not reached in 24 traversal steps is a failed bounded procedure condition; (2) Back is reached/activated and actual focus is on another element is an observed unmet focus assertion; (3) observation is unavailable or blocked before activation leaves downstream transition/focus unobserved. None alone supports a website-defect assertion in this fixture task. Keep actual observations and procedural verdicts together.

Delivery D4's “incomplete/failed reachability evidence” needs the same split. Its D2 and preservation checklist already support retaining the full 24-step condition. Selected wording: retain starting focus, actual sequential key directions/count, last reached control, whether Back was reached, whether Enter occurred, and observed postconditions. Count each Tab or Shift+Tab as one traversal step, including changes of direction; never silently restart the budget. Preserve the separate unanswered checkpoint after Close and before leaving. Do not click or inject focus to rescue a passing trace. If the bound expires, preserve earlier observations and leave dependent return/focus obligations unobserved. No new retry product behavior is implied.

Policy precision: accept QA decision 3's distinction. All requests are subject to GET/HEAD/OPTIONS methods; the project profile explicitly scopes the origin navigation guard to main frames/popups. Do not turn this into a categorical ban on all cross-origin subresources. Original contract/policy establish the allowed origin and methods; profile establishes explicit navigation categories. Blocked analytics and visible effects must remain recorded; never relax guards to obtain a successful journey.

Entry and Start remain click transitions (`surface-contract.json:9-10`). Architecture A2 and QA help sequence support keeping summary keyboard actions local to their specified part of the journey. No keyboard-only entry rewrite, artificial reset, full questionnaire, mobile run or general accessibility certification is warranted.

## Explicit revisions, retained dissent and recommendation

UX initial report/claims remain untouched as historical analysis. This pass revises the interpretation of `ux-traversal-nuance` and `ux-preserve-existing`: preserving the target alternative does not authorize marking the canonical Close Tab path observed from Shift+Tab evidence. The old recommendation to flag this for adjudication is now replaced by the direction-labeled recommendation above. The alternative remains valid target coverage; canonical coverage remains evidence-specific.

UX `ux-focus-evidence` needs a wording correction: the checker validates declared Back traversal/Enter values; it does not require or inspect actual browser observations despite its error message mentioning observed activation. The procedure and future trace must establish those observations. No initial claim is deleted.

Severity dissent is preserved: UX rates omitted explicit help sequence HIGH for acceptance reliability; Product, Architecture, Delivery and QA rate it MEDIUM. Both agree on the factual omission and corrective sequence. This pass retains UX HIGH rather than averaging severity; no observed deployment impact is asserted. UX accepts QA's emphasis on separate visible-state and focus evidence and Architecture's documentation-only design subject to future-run wording.

Selected minimal solution: preserve fixture disclaimer and every existing target assertion; add exact source-backed setup/policy requirements, Enter/Space/Enter help state assertions, direction-labeled Close evidence and concise per-obligation outcome guidance. Retain pointer entry/Start, both unanswered checkpoints, Back's 24-step bound and full postcondition conjunction. Keep all runtime implementation and empirical claims outside this plan.

Unfinished evidence: current site behavior, actual guard coverage, tab order, answer-state representation and analytics effects are deliberately unobserved. Lead adjudication and candidate wording are pending. No material UX cross investigation remains within this documentation-only scope; no peer cross reports or proposed final procedure were used.
