# QA and security — independent Analyze report

Role: QA and security planning perspective; actual context: fresh worker context supplied raw project documents and this role brief only. No peer reports, browser, network, external projects, prior reports, or application sources inspected. This is documentation planning, not a current deployment assessment or certification.

Target snapshot: `e9aeec2eee10b52c3339b53b4e491d3ff69f57c68be2f5ea1d61e70df55acccc`, identified by lead as the entire prepared manifest. I did not independently recompute the manifest digest. Applicable existing specification is `target/verification-protocol.md`, which determines Workflow selection but is not the project authority for expected behavior. Authoritative requirements come from the original project sources and TASK.

## Inspected evidence and limits

- `TASK.md:1-5`: qore-plan; documentation-only clarification; preserve valid obligations; original sources; no input mutation or external answer retrieval.
- `surface-contract.json:2-20`: complete file, schema/version, authorized entry/origin, scope, six states, seven transitions, focus targets, eight required checks, provenance and limits.
- `checks/check_contract.py:1-54`: complete file; static validation and its explicit browser-evidence limit at lines 42-43. Lines 32-36 require distinct Close/Back focus destinations and keyboard Back traversal plus Enter. Its required-check subset at lines 37-39 does not itself prove all transition or prose coverage.
- `observation-policy.json:1-5`: complete file; sole allowed origin `https://qaizen.io`.
- `target/verification-protocol.md:1-10`: complete target. Crucial current fact: line 10 ALREADY requires sequential keyboard Back traversal within 24 steps, Enter activation, visible introduction, absent question/help, and heading focus. Line 8 already requires keyboard Close and summary focus. These are not missing requirements.
- `.agents/skills/qore-plan/references/protocol.md`: complete supplied planning protocol, sections Intake and mode, Independent analysis, Challenge and correction, Adjudication.
- `.agents/skills/qore-plan/references/roles.md`: complete five-perspective briefs, challenge links and Architecture reuse boundary guidance.

Uninspected: all other resources, application/runtime/browser behavior, deployment revision and DOM, peers' reports, specification/run-evidence templates (lead responsibility). No claim of website defect or success follows from this report. Input files and skill resources were not modified.

Measurement: ran `python3 -B checks/check_contract.py surface-contract.json` in `/workspace/worker` under supplied shell/container; exit 0, `valid: true`, all eight declared check IDs returned, limit `Contract consistency only; browser observations establish current behavior.` This checks the JSON contract, not target prose or the public deployment. No site contact occurred. Raw supplied command/result are captured in this report; lead may retain separate run evidence.

## Proposed decisions and deliverables

D1. Preserve the complete existing Back paragraph's valid obligations, including unanswered assertion before leaving, 24-step bound, Enter activation, visible introduction, absent question/help and heading focus. Preserve Close's independent closed-state and summary-focus assertions. This requires clarification around existing text, not introducing keyboard Back as a purported newly missing fix. Sources: target lines 8-10; contract lines 14-19. The specific bound and absence assertions are existing target obligations even though the contract does not repeat them. No supplied evidence contradicts them.

D2. Make the full help sequence explicit: focus summary, Enter opens help, Space closes it, Enter reopens it, then Tab to Close, Enter closes it and restores focus to summary. Assert help state after each activation. Current target line 7 leaves the activation unspecified and does not expressly cover Space toggle or reopening, while contract lines 11-14 explicitly require them. Add steps rather than collapsing toggle and Close into one test. This is a documentation coverage correction, not evidence of a site defect.

D3. Add preconditions covering URL/origin, en-US, 1280×800, entry/state-only depth, unanswered policy, allowed methods, and no results or submissions. Configure policy before navigation, enforce on requests/redirect destinations throughout the journey, record the disposition and observable effect of blocked analytics POST. Exact origin matching must use parsed origin rather than string-prefix matching. These are practical procedure requirements derived from contract lines 4-6, 18-20 and observation-policy lines 2-4. They do not authorize a browser run in this planning task.

D4. Use contract Tab traversal as the primary documented path for Close and Back, retaining the target's already permitted Shift+Tab wording as reverse sequential navigation, with the actual direction and count recorded. Do not introduce programmatic focus, selector click, JavaScript activation or pointer Back as substitutes. The checker explicitly accepts Tab or Shift+Tab for Back (lines 35-36); the exact supplied transition declares Tab (contract lines 14-15). If lead wants both directions to be mandatory, that expands acceptance and needs justification; one observed permitted sequential path suffices for the current target.

D5. Explain outcomes and evidence: static-contract pass; procedure coverage reviewed; browser observation PASS, FAIL, or NOT OBSERVED/BLOCKED per obligation. A denied POST expected by policy is not automatically a functional journey failure; retain any resulting errors, missing content or changed navigation, and mark affected assertions unresolved/failed on their observed facts. A runtime failure must not silently weaken the document's expected behavior. Contract lines 19-20 expressly separate expectations from observations and demand retention of blocked-request effects.

D6. Deliver a proposed maintainer documentation clarification, source-to-step acceptance matrix, preservation/change rationale and verification evidence outside inputs. Do not add browser tooling, application fixes, changed contract/checker/policy, analytics bypasses, broad security scans, tests of full questionnaire, mobile/performance coverage or accessibility certification. Browser execution is not needed to complete the doc-only plan; future browser observations are separate evidence required only to claim current deployment conformance.

## Acceptance and evidence matrix

All browser rows below are planned checks, not performed measurements. The only performed check is S1.

| ID | Boundary/behavior | Required procedure/evidence | Expected outcome and source |
|---|---|---|---|
| S1 | Contract consistency | Run supplied local checker, retain command/environment/exit/result | Pass already measured; never promoted to browser pass. Checker 42-43 |
| S2 | Documentation integrity | Review target proposed diff against all old steps and authoritative fields | Existing valid Close/Back/unanswered/24-step/state assertions preserved; all additions have rationale. TASK 3, target 8-10 |
| P1 | Authorization before navigation | Parse entry and request origins; record effective allowlist/method policy without secrets | Only https://qaizen.io and GET/HEAD/OPTIONS permitted. Contract 4-6; policy 2-4 |
| P2 | Entry | Start /labs; observe journey link click and introduction | URL/visible state consistent with entry transition. Contract 9 |
| P3 | Unanswered start/data integrity | Click Start; observe first question and selected-answer state without setting values | First question visible, unanswered. Contract 6,10,18 |
| P4 | Keyboard help open | Focus summary through ordinary navigation; Enter; record state | Help open. Contract 11 |
| P5 | Toggle and reopen | Space on summary; assert closed; Enter; assert open | Separate observable transitions, no answer mutation. Contract 12-13 |
| P6 | Close focus | Tab/record permitted sequential direction to Close; Enter; inspect focused element and help state | Help closed AND summary focused; question still unanswered. Contract 14,17; target 8-9 |
| P7 | Back proof and bound | Assert unanswered; sequential navigation, record every step/direction from known post-Close focus; Enter only when Back focused | Reach Back within 24 traversal steps; do not bypass exhaustion. Target 10; checker 35-36 |
| P8 | Return state/focus | After keyboard Enter on Back observe visibility and active focus | Introduction visible, question/help absent, introduction h1 focused; no answer/result. Target 10; contract 15,17 |
| N1 | Cross-origin redirect or request | Proposed policy test: request/redirect to other origin, including deceptive prefix/lookalike | Denied and recorded before destination request; affected observations marked blocked if necessary. Policy 2-4 |
| N2 | Non-allowlisted method | Proposed policy test: analytics POST or other disallowed method | Blocked; preserve its effects; never temporarily permit it to obtain a pass. Contract 6,20 |
| N3 | Focus/state mismatch | Observe help closed but summary unfocused, or return with h1 unfocused | Fail corresponding focus obligation separately from visual state, not blanket pass. Contract 14-18 |
| N4 | Traversal exhaustion/control missing | Back absent, unreachable or not focused after 24 steps | Record failing step/focus, stop this proof; do not substitute click or scripted focus. Existing target 10 |
| N5 | Unanswered integrity failure | Answer becomes selected at any checkpoint | Record failure and stop before generating results/submitting; no attempt to complete questionnaire. Contract 6,20; target 6,9-10 |
| N6 | Network/runtime interruption | Allowed resource unavailable or policy denial prevents state assertions | Record environment/time and denied request metadata; affected checks not observed/blocked, no fabricated PASS. Contract 19-20 |
| E1 | Evidence privacy/provenance | Retain only necessary URL/origin/method/status, steps, state/focus, observation time and environment | Avoid cookies/tokens/full response payloads or site source redistribution; distinguish current observations from historical baseline. Contract 19-20; data minimization is a proposal |

Acceptance: documentation maps all seven transitions, eight required checks, distinct focus destinations and all declared limits; nothing claims the static checker validates prose or that documentation repair proves deployment behavior. Existing 24-step bound remains. Lead should mark each row as preserved, clarified, added from contract, or deferred runtime verification.

## Edge-case Gherkin

```gherkin
Feature: Documentation preserves observable keyboard and read-only evidence

Scenario: Help closes visually but focus does not return to its summary
  Given the question is unanswered and help is open
  When I reach Close by sequential keyboard traversal and press Enter
  And help becomes closed but document focus is elsewhere
  Then the help-closed assertion passes
  And the close-focus obligation fails
  And the observation must not be reported as a complete Close pass

Scenario: Back cannot be reached within the existing bound
  Given Close has returned focus to the summary and the question is unanswered
  When 24 sequential Tab or Shift+Tab traversal steps have not focused Back
  Then the bounded keyboard Back proof fails with the final focus recorded
  And I do not click Back or programmatically focus it to claim that proof passed
  And the required expected return state and heading focus remain in the protocol

Scenario: Return looks correct but heading focus is missing
  Given Back was reached within 24 sequential traversal steps without answering
  When Enter activates Back
  And the introduction is visible and the question and help are absent
  But the introduction heading is not focused
  Then the visible return-state assertion passes
  And the introduction-focus obligation fails

Scenario: Expected blocked analytics request has a visible effect
  Given the origin and GET HEAD OPTIONS restrictions were installed before entry
  When the page attempts an analytics POST
  Then that request is blocked
  And the observed effect on loading or navigation is retained
  And any state assertion that cannot be observed remains unresolved
  And the method restriction is not relaxed to make the journey pass

Scenario: An allowed page redirects outside the authorized origin
  Given only https://qaizen.io is authorized
  When an allowed request proposes a redirect to another origin
  Then the destination request is denied
  And the redirect and affected observation are recorded without credential payloads
  And that unavailable observation is not inferred from the contract

Scenario: Explicit help toggle coverage is preserved before Close
  Given the first question is unanswered and the summary is focused
  When Enter opens help
  And Space closes help
  And Enter reopens help
  Then each help state is asserted independently
  And the next step tests Close and its summary-focus destination separately

Scenario: An answer changes before leaving the question
  Given the journey must remain unanswered
  When an answer is observed selected before Back activation
  Then the unanswered obligation fails
  And the observer does not submit the form or generate results
```

## Risk register

Severity describes planning consequences if the trigger occurs; no current deployment vulnerabilities are asserted.

- High — unauthorized observation/network side effects if procedure omits pre-navigation enforcement or permits POST to resolve an error. Evidence: contract 6,20 and policy 2-4; whether the page currently attempts particular forbidden requests beyond the stated expected analytics POST is unobserved.
- High — false acceptance and loss of a valid obligation if an editor assumes keyboard Back is absent and replaces the current paragraph, deleting bound/unanswered/return-state/focus checks. Evidence: target 10 already contains all these requirements; checker 32-36 distinguishes Back and Close.
- Medium — incomplete transition coverage if summary opening is assumed to cover Space-close and Enter-reopen. Evidence: target 7 versus contract 11-13. This is a proven documentation omission, not a measured runtime bug.
- Medium — false runtime confidence if local checker success is represented as procedure/browser validation. Evidence: checker 42-43; no runtime observations performed.
- Medium — concealed focus defect if visible introduction/help state alone is accepted. Trigger is mismatch between visibility and active focus; evidence of obligation contract 14-18; occurrence remains a hypothesis.
- Medium — loss of faithful evidence if blocked analytics effects are removed or bypassed. Evidence: contract 20; occurrence and severity of any visible effect remain unobserved.
- Low — inadvertent sensitive-data retention or source redistribution if maintainers retain full network payloads/DOM dumps as default proof. No actual leakage identified. Contract 20 forbids source redistribution; minimal metadata policy is a proposal, not an invented existing project rule.

## Named peer questions and alternatives

Product: Do your acceptance criteria preserve the current Back paragraph verbatim in substance, including the target-specific 24-step and absence assertions? Is any proposed expansion beyond eight declared checks required for the maintainer outcome? Alternative: a concise preconditions-plus-step clarification, rather than a broad browser-testing initiative.

Architecture: Where in the proposed documentation does policy enforcement begin, and how does it cover redirects/subrequests without implying new software implementation? Can you distinguish a contract consistency checker from a prose-coverage review and a runtime observation? Alternative: document existing guard requirements and leave implementation unspecified rather than inventing a new interceptor or schema.

UX: Does your journey enumerate Enter-open, Space-close, Enter-reopen, Close-focus and Back-focus as distinct observations? What exactly should be recorded at the 24-step boundary, and is the existing allowance for Shift+Tab retained? Alternative: primary Tab sequence with reverse traversal retained as permitted; do not require both directions without justification.

Delivery: Does definition of done allow the documentation plan to finish without network execution, while explicitly withholding current-site conformance claims? Is each output written outside inputs with no source edits? Alternative: bounded static acceptance mapping now and future authorized browser evidence separately, rather than blocking this doc-only plan on deployment access.

For all roles: identify the exact sourced obligation before proposing deletion, weakening, or expansion. Static coverage is not current behavior evidence. A reconstructed fixture's historical statement is not authentic deployment provenance.

## Unfinished work and resolving evidence

Initial analysis complete within the deadline. Cross-examination, peer comparison, final adjudication and consolidated spec/run-evidence belong to subsequent Workflow stages and were intentionally not attempted. No future browser observations have been executed or are necessary for this plan's completion; current runtime conformance remains unknown until separately observed under the supplied policy. Exact interpretation of a traversal step should be clarified as one recorded Tab/Shift+Tab action, preserving the current 24-step bound; this is a documentation proposal requiring lead adjudication, not a discovered contract requirement.

Completed UTC: pending timestamp appended immediately below by local clock tool.

Actual completion UTC: 2026-10-17T11:45:18Z.
