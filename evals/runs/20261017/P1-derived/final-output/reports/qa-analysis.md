# QA and security independent analysis

- Actor/context: `/root/qa`; independent QA and security perspective in Workflow Analyze. No peer report was read during this analysis.
- Actual start UTC: 2026-10-17T10:41:48Z (first clock observation after dispatch). Report end UTC recorded below.
- Environment: supplied frozen files under `/workspace/worker`, shell `sh`, no network or browser execution. Output written outside input root.
- Target: `target/verification-protocol.md`; named snapshot SHA-256 supplied by lead: `ed6c0fb8d8737cb4b8fc9e6b3485e0e618bf332d15725a557cf30d17b127e394`. I read the target bytes but did not independently recompute this lead-owned snapshot procedure.
- Scope: plan a correction to the tutorial verification procedure; do not change the website, original inputs, policy, contract, checker, or skill. The target explicitly calls itself a reconstructed fixture, not evidence of a website defect (target lines 1–3).

## Sources inspected and authority

1. `TASK.md:1–5`: planning request; original sources authoritative; outputs outside input; no historical reports/network retrieval.
2. `target/verification-protocol.md:1–10`: current six-step fixture. Material gaps: Back is clicked (line 10), help lacks Space-toggle/reopen (lines 7–8), no policy setup or evidence procedure, and Close traversal permits either direction (line 8).
3. `surface-contract.json`: `/scope` (line 6), `/states` (7), all `/transitions/0` through `/transitions/6` (9–15), `/focus_targets` (17), `/required_checks` (18), `/provenance` (19), `/limits` (20). Contract digest returned by current preflight: `3728739a119a53272541f83d451e40addb6939304f9d9ec060a477a87170a4a3`.
4. `checks/check_contract.py:9–43`: read actual validation logic; command is offline, but I did not execute it in this role. Digest returned by current preflight: `9ef2a0acf51f078ce290ec723ca550b8b73597e68304179fe4d0625c5757963b`.
5. `observation-policy.json:/allowed_origins/0` (lines 2–4): sole allowed origin `https://qaizen.io`.
6. Current lead-generated `/workspace/output/profile-check.json`: coverage COMPLETE; fresh source comparisons; consumed facts `surface-contract`, `close-focus`, `back-focus`, `unanswered-scope`. This is current-session preflight feedback, not a peer role report. Its `/surfaces` is empty for method plan; I do not claim it selected a browser surface. Direct surface-contract authority supplies entry URL.
7. Skill `SKILL.md`, `references/protocol.md`, `roles.md`, `specification.md`, `project-profile.md`, `project.json`, and `run-evidence.md`. Profile original was inspected after the supplied current preflight result; profile is context, not higher authority (`project-profile.md:22–28`). Actual planning scope does not authorize website execution (`SKILL.md:17`).

## Proposed decisions and deliverables

- **Q-D1 (required correction):** replace the target Back click with real sequential **Tab**, then **Enter**, and separately assert the returned introduction heading is the active element. A click or programmatic `.focus()` cannot establish this property. Source: `/transitions/6`, `/focus_targets/introduction-heading`, current profile invariant `back-focus`; checker lines 32–36. Assert introduction visible and first-question/help absent as the fixture already requires.
- **Q-D2 (required correction):** preserve Close as a different action and assertion: after reopened help, reach Close with **Tab**, activate **Enter**, assert help closed and the summary active. Source `/transitions/5`, `/focus_targets/summary`. Use Tab in the canonical procedure because the literal contract specifies Tab for both Close and Back. Profile/checker accept Tab or Shift+Tab for Back; this broader allowance need not create a contradiction when Tab satisfies both. Keep reverse traversal as a deferred optional variant rather than replacing the canonical exact-contract step.
- **Q-D3 (required correction):** explicitly cover the complete ordered chain: entry click → Start click → summary Enter → summary Space (closed) → summary Enter (reopened) → Close Tab/Enter → Back Tab/Enter. Source `/transitions/0–6`; target lacks toggle/reopen. Do not substitute an Escape key or mouse click for a specified activation.
- **Q-D4 (required boundary):** leave first question unanswered throughout. Observe selected/checked response state before help, after each help transition, immediately before Back, and after return where controls remain available. Do not choose an answer to make the path progress. Source `/scope/answer_policy`, `/limits/0`, `/required_checks`.
- **Q-D5 (required planning boundary):** a future browser run installs read-only interception before opening the entry: allow only GET/HEAD/OPTIONS for every request; block main-frame/popup navigations whose parsed origin is not in the source allowlist. Record blocked analytics and effects without relaxing policy. Source `/scope/allowed_methods`, `/allowed_origins`, `observation-policy.json`, current fresh `unanswered-scope` invariant, `/limits/2`. This is a plan, not evidence that interception or browser observations occurred.
- **Q-D6 (proposed evidence design):** retain separate results for static contract validation, observed transitions, keyboard reachability, observed active element, and policy enforcement. Record current URL/origin, state before/after, actual input sequence, active-element role/name/selector, unanswered state, blocked request method/destination/reason, resulting visible effects, and actual timestamps/environment. A screenshot alone cannot prove the input modality or active element. Avoid collecting page source or unnecessary query/body data; no website source redistribution (`/limits/0`). Do not assert a mandated retention period or privacy incident absent evidence.
- **Q-D7 (required honest outcomes):** failed reachability, wrong focus, policy interception failure, unexpected navigation, or unanswered invariant failure prevents a pass for the affected check. If policy blocks an analytics POST, retain its effect; do not label this expected blocking alone a website defect. A failed guard means stop the future observation rather than continue outside scope. Static success never upgrades unobserved behavior to pass.

Deliverables for lead consolidation: revised protocol plan using Q-D1–7; matrix below; meaningful Gherkin and coverage links; evidence schema/procedure; explicit distinction between plan readiness and deployment behavior; named unknowns below. These IDs are role-local and may be mapped to stable final specification IDs.

## Measurable acceptance matrix

| ID | Obligation / trigger | Planned procedure and observable oracle | Evidence / failure interpretation | Source |
|---|---|---|---|---|
| Q-AC01 | Authorized entry | At en-US, 1280×800, start at `https://qaizen.io/labs`; activate `a[href$='/labs/readiness-check']` by click; observe introduction and allowed origin | URL/origin plus transition observation; missing/ambiguous control is unresolved, not guessed | `/entry_url`, `/scope`, `/transitions/0`, observation-policy `/allowed_origins` |
| Q-AC02 | Start unanswered | Click “Start the check”; first question visible, all answer controls unselected | State record plus checked/selected values without choosing an answer | `/transitions/1`, `/scope/answer_policy` |
| Q-AC03 | Full help-toggle coverage | Focus actual summary, Enter opens help; Space closes it; Enter reopens it; answer state remains empty | Actual keys and open/closed semantic/visible states at each transition; no extra focus-after obligation invented for toggle | `/transitions/2–4`, `/required_checks` |
| Q-AC04 | Close keyboard proof | From reopened help, sequential Tab reaches actual Close; Enter closes; active element equals associated summary | Ordered key/focus trace and separate final active-element assertion | `/transitions/5`, `/focus_targets/summary` |
| Q-AC05 | Back keyboard proof | From closed-help state, sequential Tab reaches application Back; Enter returns | Trace begins at actual prior focus; no synthetic target focus or click; record actual reached control | `/transitions/6`; checker 35–36 |
| Q-AC06 | Introduction focus/state | After Q-AC05, introduction visible, first-question/help absent, actual focused element is introduction h1 | Active element and state observation; visibility alone insufficient; ensure the intended h1 is uniquely identified | `/focus_targets/introduction-heading`; target 10 |
| Q-AC07 | Read-only transport | Guard active before first request; permit exactly GET/HEAD/OPTIONS, block every other method; no answers/result/form submission | Guard setup evidence and blocked-request record; no mutation request deliberately sent to live site for testing | `/scope`, `/limits/0`, fresh `unanswered-scope` |
| Q-AC08 | Origin containment | Exact parsed origin allowlist for main frame and popup, including redirected destinations; do not follow an off-origin destination | Navigation decision evidence; matching host substrings or a URL suffix alone cannot authorize origin | `/allowed_origins`, observation-policy; fresh `unanswered-scope` |
| Q-AC09 | Analytics block effects | When analytics POST is attempted, guard blocks it; retain downstream visible/console/navigation effects if any | Expected block distinct from observed application failure; never relax method policy to obtain a clean recording | `/limits/2`; fresh `unanswered-scope` |
| Q-AC10 | Source/evidence distinction | Run offline contract checker within authorized local scope; retain argv/exit/output; independently map every required check and transition to future browser oracle | Checker says “Contract consistency only”; its pass cannot prove keyboard behavior or current deployment | checker 42–43; `/provenance`; `/required_checks` |

Canonical Back/Close traversal uses forward Tab. An explicitly authorized future variant can add Shift+Tab, but it cannot erase proof of the canonical surface contract. Configure and record bounded locator/state waits and maximum traversal attempts in the future harness; exact numerical values are implementation proposals pending actual DOM behavior, not supplied acceptance requirements. A timeout is a failed/incomplete check, not permission for scripted focus recovery.

## Trust boundaries, privacy and integrity

| Boundary | Relevant data / action | Required guard or evidence | Limit / open point |
|---|---|---|---|
| Frozen project input → planning output | Contract, policy, target bytes, source digests | Read originals; output outside input; version and bind plan to snapshot | No input edits authorized |
| Plan → future observer | URL, viewport, locale, exact key sequence, selected-state invariant | A plan is not observed success; observer must retain actual run evidence | No browser executed here |
| Browser → network | Request method; navigation parsed origin; redirect/popup destination | Method allowlist globally; origin boundary for main frame/popups installed before entry | Contract lists allowed origins broadly; current profile specifically names main frame/popups. It does not explicitly resolve third-party subresource policy. Do not silently invent its authorization or claim all resource-origin enforcement proven |
| User interaction → application state | Answer controls, details/help state, application Back, focus | No answer selection or result generation; inspect state without mutating it | Current implementation/DOM unknown; hypothesis of stale answer state is a negative-path consideration, not an observed defect |
| Observation → evidence artifact | URLs, control identifiers, active element, blocked effects | Minimum relevant metadata; avoid request bodies/page-source redistribution; bind timestamps/environment | No accounts or personal data are requested. Do not invent authentication, storage or database changes |
| Static checker → readiness claim | Validator success and required-check list | Explicit consistency-only result and independent semantic coverage matrix | Checker does not drive a browser, inspect target prose, or prove comprehensive coverage |

Authorization here is source-limited public observation planning. An allowed origin grants no authentication, account/data access, submission, answer entry, source redistribution, publication or deployment authority. All are unnecessary to this document task. No invented backend API, transaction, credential or database is part of this plan.

## Findings and bounded risks

Severity is planning significance, not an observed website vulnerability.

1. **High, confirmed protocol gap:** triggering condition is using existing target step 6. It clicks Back (`target:10`), so keyboard reachability is unproven even if focus passes. Affected requirement `/transitions/6`; fix Q-D1. Evidence is target text, not live UI.
2. **Medium, confirmed protocol omission:** existing step 3–4 jumps open→Close without Space close/reopen (`target:7–8`), leaving `/transitions/3–4` and `help-toggle` incomplete. Add Q-D3.
3. **Medium, confirmed guard/evidence omission:** target lacks method/origin setup and blocked-analytics evidence, despite `/scope`, `/required_checks`, `/limits/2` and fresh profile invariant. A future recorder following it literally cannot establish authorized observation. Add Q-D5–6. No unauthorized request is claimed to have occurred.
4. **Medium, conditional false-confidence risk:** if only checker success is used for sign-off, prose/behavior gaps survive. Validator checks Back traversal/Enter but does not verify actual traversal; it does not enforce Close traversal/activation or every required-check ID, and cannot inspect target prose (checker 23–43). Existing validator may remain unchanged; mapping and independent review close the document assurance gap. Do not expand scope to rewriting it absent need.
5. **Medium, conditional origin bypass risk (hypothesis):** a future harness allowing navigation by host substring, href suffix or initial URL only could permit an off-origin/redirected/popup destination. Negative local guard tests resolve this. The entry suffix selector in the source is a control locator, not an authorization predicate.
6. **Medium, conditional policy interference (declared expectation plus unknown effect):** source expects blocked analytics POST, but its actual UI effect is unknown (`/limits/2`). Record and report; do not promise it is harmless or blame it for any behavior without evidence.
7. **Low, authority precision:** checker and current profile allow Shift+Tab for Back while literal transition declares Tab; target permits either for Close. Canonical Tab satisfies all sources, eliminating need for a policy exception. A reverse-only proof would require explicit adjudication rather than treating validator tolerance as source amendment.
8. **Unscored implementation unknowns:** duplicate h1/summary, inaccessible/disabled Back, focus delayed/lost, keyboard trap, stale selected answer, or navigation instability are possible failure cases to observe, not established defects. Do not assert their probability, product impact beyond this journey, or accessibility certification.

## Edge-case Gherkin for final specification

```gherkin
Feature: Observe the unanswered journey within the declared boundaries
  Scenario: Q-S01 Complete help sequence preserves unanswered state
    Given the first question is visible and all answer controls are unselected
    And the actual question help summary has keyboard focus
    When Enter opens help
    And Space closes help through the summary
    And Enter reopens help through the summary
    Then help is open
    And all answer controls remain unselected at each observed transition

  Scenario: Q-S02 Close and Back have distinct keyboard focus destinations
    Given help has been reopened and the first question remains unanswered
    When sequential Tab reaches Close and Enter activates it
    Then help is closed and the actual active element is its summary
    When sequential Tab reaches the application Back control and Enter activates it
    Then the introduction is visible and its heading is the actual active element
    And the first question and its help are absent

  Scenario: Q-S03 A visible returned introduction does not pass wrong focus
    Given sequential Tab and Enter activated the application Back control
    When the introduction is visible but its heading is not the active element
    Then introduction focus is reported failed
    And a screenshot of the visible introduction does not substitute for focus evidence

  Scenario: Q-S04 Unreachable Back is preserved as a failure
    Given help is closed and the summary has actual focus
    When the declared bounded sequential Tab traversal does not reach Back
    Then keyboard Back is failed or incomplete with the traversal trace retained
    And no click or programmatic target focus is used to claim that check passed

  Scenario: Q-S05 Expected analytics blocking retains observed effects
    Given the read-only request guard was active before entry
    When the application attempts an analytics POST
    Then the POST is blocked before transmission
    And its destination, method, block reason and observed application effects are retained
    And the allowed methods remain GET, HEAD and OPTIONS

  Scenario: Q-S06 Local policy test rejects an off-origin redirected popup
    Given a local policy test double supplies a popup redirect destination outside https://qaizen.io
    When the planned navigation guard evaluates that destination
    Then the destination is blocked
    And the rejection record identifies the actual parsed origin
    And no live off-origin navigation is performed for this test

  Scenario: Q-S07 An answer becoming selected prevents unanswered acceptance
    Given all answer controls were unselected before opening help
    When an observation after a help transition finds an answer selected
    Then unanswered acceptance is failed
    And the observer does not continue by submitting or generating results

  Scenario: Q-S08 Offline validity does not claim browser success
    Given the supplied offline contract checker returns valid
    When no future browser journey has been observed
    Then the report records contract consistency only
    And keyboard reachability, active-element behavior and deployment success remain unobserved
```

Coverage: Q-S01 → Q-AC02/Q-AC03 / Q-D3/Q-D4; Q-S02 → Q-AC04/Q-AC05/Q-AC06 / Q-D1/Q-D2; Q-S03/Q-S04 → Q-AC05/Q-AC06 / Q-D1/Q-D6/Q-D7; Q-S05 → Q-AC07/Q-AC09 / Q-D5/Q-D6; Q-S06 → Q-AC08 / Q-D5; Q-S07 → Q-AC02 / Q-D4/Q-D7; Q-S08 → Q-AC10 / Q-D6/Q-D7. Final spec must add explicit entry/setup scenario Q-AC01 and guard setup/nonallowed-method local test coverage Q-AC07 if not covered elsewhere; this role matrix names them rather than claiming these eight scenarios exhaust the final specification.

## Named peer questions and alternatives

- **Product:** Will the final stories lock full `/transitions` coverage and the eight named `/required_checks`, rather than only the most conspicuous Back repair? What outcome differentiates protocol completeness from a passing current deployment? Smallest investigation: map each supplied transition/check to one stable acceptance ID.
- **Architecture:** Where do method interception and main-frame/popup origin decisions occur before entry, and what evidence proves redirects are checked? Do not add APIs/databases or rewrite the checker to address a prose gap. What is the explicit treatment of third-party subresources, which the narrow profile invariant does not fully resolve? Smallest investigation: document exact guard boundary and origin parsing rules; leave unresolved authorization visible.
- **UX:** How will the summary, Close, Back and introduction heading be identified unambiguously, and how will active element be observed separately from visibility? Do not invent Start focus, help-toggle focus outcomes or a keyboard order not in sources. Smallest investigation: specify observation fields and failure reporting without claiming current DOM inspection.
- **Delivery:** Does definition of done distinguish document source/lint checks from future browser checks and include policy-blocked effects? Is browser execution deferred because this task is planning only? Smallest investigation: make per-task prerequisites/gates and pending evidence explicit.
- **All roles:** Will each unsupported security/UX behavior claim be labeled hypothesis? Can any acceptance criterion currently pass from screenshots or checker output alone when it requires input modality or active-element evidence? Can the plan be adopted without changing frozen sources?

Alternatives: minimal Back-only edit is smaller but rejected as incomplete against the full source transitions/policy; a full browser automation implementation is deferred as beyond this planning request; changing the validator to accept target prose is unnecessary and unsupported; using Tab canonically is selected over reverse-only traversal because it satisfies the literal transition and current profile simultaneously; guard-unit tests should use local test doubles rather than deliberate live mutations/off-origin requests.

## Uninspected and unfinished work

- No peer reports inspected and no cross-examination yet: waiting for lead's all-five barrier and explicit challenge assignment. This analysis alone cannot complete QA Workflow phase coverage.
- No browser/website/network execution, DOM measurement, analytics observation, deployment identification, mobile/full questionnaire/performance/accessibility certification, answer/result/submission tests, account access or private source inspection. These are not claims of defects or success.
- No source modification, implementation execution, contract-checker execution or final specification lint by this role. Lead must retain actual offline command/lint results if run.
- Exact future observer capability, selectors, bounded wait/traversal values, request interception coverage (including service worker/WebSocket details if relevant), third-party subresource authorization, and current analytics effects remain unknown. Do not invent them to claim current behavior.
- Need final cross-role coverage mapping for Q-AC01 and guard setup/local method rejection, final stable specification IDs, and adjudication of any peer disagreement. Resolution evidence: complete peer reports, source comparison and final spec coverage audit; browser facts remain deferred.

Report status: independent Analyze complete within the 150-second dispatch budget; cross-examination intentionally pending. Deadline did not require prematurely stopping the available source analysis.

Actual end UTC: 2026-10-17T10:43:43.035074Z
