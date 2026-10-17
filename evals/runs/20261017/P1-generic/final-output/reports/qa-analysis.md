# QA and security — independent Analyze report

Role: QA and security. Mode assigned: Workflow, Analyze phase only. Supplied immutable target snapshot: `0aa277436d8dcda4d6c2412c6ad4307dd0192b0f6230fa96c8b16d99c8bac194`. This identifier is supplied by the lead; I have not independently established a repository revision or deployment identity. Target: `/workspace/worker/target/verification-protocol.md`. All source paths below are relative to `/workspace/worker`.

## Sources and measurements

Inspected: `TASK.md:1-5`; `surface-contract.json:1-21`; `checks/check_contract.py:1-54`; `observation-policy.json:1-5`; `target/verification-protocol.md:1-10`; `.agents/skills/qore-plan/SKILL.md`; `.agents/skills/qore-plan/references/protocol.md`; `.agents/skills/qore-plan/references/roles.md`. Searched for `AGENTS.md` with `find . -name AGENTS.md -print`: none returned. `rg` is unavailable in this environment, so this fallback was used. No peer reports were read. Uninspected: website, browser behavior, historical deployment, private implementation, all resources outside supplied sources and relevant skill instructions. No network calls or input modifications were made.

Local measurement: ran `python3 -B checks/check_contract.py surface-contract.json` in `/workspace/worker`, Python environment supplied by host. Exit 0; output `valid: true`, schema `qaizen-labs-surface/1`, all eight contract check IDs, and limit `Contract consistency only; browser observations establish current behavior.` This checks the supplied contract's consistency, not the target prose and not the website (`checks/check_contract.py:42-43`). No browser acceptance result exists from this task.

## Decisions and proposed deliverables

**QA-1: The project sources govern the document.** `TASK.md:3-5` expressly makes the tutorial protocol a target, not authority. Preserve its fixture provenance (`target/verification-protocol.md:3`), distinguish acceptance obligations from observed results, and do not infer a deployed bug from a protocol gap (`surface-contract.json:19`). Deliverable: revised protocol specification, not website changes or browser execution in this planning task.

**QA-2: Specify and trace every declared transition, not merely required-check labels.** The target omits explicit Enter for opening help, the Space close / Enter reopen sequence, and keyboard Back; it also permits Shift+Tab for Close where the supplied transition says Tab (`target/verification-protocol.md:7-10`; `surface-contract.json:11-15`). Proposed replacement execution order: click entry; click Start; focus summary and Enter; Space on summary; Enter on summary; Tab to Close and Enter; from restored summary focus, Tab to Back and Enter. Assert each declared state and distinct final focus destination. Use actual keyboard traversal/activation, not a scripted DOM click, direct focus call, or post-hoc focus correction. The latter exclusions are proposals needed to make keyboard proof meaningful, not quoted contract text.

**QA-3: Choose Tab for both Close and Back in the planned protocol.** `surface-contract.json:14-15` specifies Tab. The checker permits Tab or Shift+Tab for Back (`checks/check_contract.py:35-36`) but does not override the concrete supplied contract; it does not validate Close traversal at all. Shift+Tab may be a separately labeled exploratory variant, never a substitute for proving the declared Tab transitions. Do not weaken or edit the supplied contract/checker to make the target pass.

**QA-4: Put the observation envelope before navigation.** Exact entry URL, `en-US`, 1280×800 viewport, entry/state depth, unanswered state and methods are obligations (`surface-contract.json:4-6`). Origin allowlist is exactly `https://qaizen.io` in both sources (`surface-contract.json:5`; `observation-policy.json:2-4`). Proposal for future execution: install fail-closed origin and method guards before opening the entry URL; check every attempted request, navigation and redirect destination before dispatch; block methods outside GET/HEAD/OPTIONS and origins outside the exact allowlist. Record blocked attempts and UI consequences. These guard mechanics are a proposed way to implement the obligations; the files do not name a browser interception API.

**QA-5: Method allowlisting alone is insufficient authorization.** No answer selection, result generation, form submission or website source redistribution is allowed (`surface-contract.json:20`). A GET form submission is still outside scope. No destructive or submitting control may be activated to test a guard live. No external origin can be added merely because an asset or redirect is blocked. The expected analytics POST must remain blocked and its observed effects retained (`surface-contract.json:20`); a blocked request alone is not a journey failure, and a resulting inaccessible required state must not be hidden.

**QA-6: Separate three acceptance layers.** (a) source consistency: existing validator pass; (b) document readiness: trace matrix demonstrates the protocol covers all supplied transitions, policies, evidence and limits; (c) future browser outcome: actual state, key, focus and network observations. A validator pass cannot establish (b) or (c). A complete document plan may coexist with unknown website behavior. Protocol failures, deployment acceptance failures, and blocked-observation/inconclusive outcomes must be reported separately.

**QA-7: Add a compact evidence record and explicit limits.** Proposed fields: contract snapshot, protocol revision, browser/version, execution timestamp, locale, viewport, effective origin/method policy, each transition ID and observed result, actual key sequence/focused control, resulting active element, unanswered observations, request allow/block decisions and blocked analytics effects. Record expected versus observed separately; screenshots alone cannot prove Enter, Tab, absence of forbidden requests, or active focus. Do not attach website source or raw response bodies. Whether incidental session storage is necessary/used is unknown; do not claim the browser changes no state. Public URLs and dated observation provenance may be retained; private commit hashes do not prove deployment identity (`surface-contract.json:19-20`).

## Acceptance and evidence matrix

All “browser” rows are requirements for the planned future protocol, not tests executed here.

| ID | Source obligation | Observable acceptance / evidence | Negative or boundary case |
|---|---|---|---|
| ENV | `surface-contract.json:4-6` | Before entry, record exact URL, en-US, 1280×800, entry/state scope and active guards. | Missing environment or guards: execution not ready; do not navigate. |
| entry | `surface-contract.json:9,18` | Start at Labs and click the declared journey anchor; record resolved destination and visible introduction. | Selector mismatch or unexpected destination: record blocked/missing transition, no alternative external navigation. |
| start | `surface-contract.json:10` | Click Start the check; identify first-question state without selecting an answer. | Starting selects a value automatically: record observed violation/inconclusive cause; never repair by selecting a value. |
| open-help | `surface-contract.json:11` | Record summary focus, actual Enter activation, then help-open. | Calling click or setting an open attribute supplies no keyboard proof. |
| help-toggle | `surface-contract.json:12-13,18` | While summary is focused, Space produces help-closed, then Enter produces help-open; log each state. | Space scrolls only, help stays open, or Enter fails to reopen: fail this transition; retain actual outcome. |
| close-focus | `surface-contract.json:14,17-18` | From open help, traverse using Tab to Close; Enter; help closes and active element is the journey summary. | Help closes but focus goes to body/Close/Back: close-focus fails. An assertion or screenshot of summary presence is insufficient. |
| unanswered | `surface-contract.json:6,18,20` | No answer control activated; inspect visible/model-exposed answer state initially and after help actions and before Back. | Existing answer, an action selecting an answer, submission, results: do not proceed deeper. Preserve the observed deviation. Continuous invariant checks are a proposal stronger than target's single check. |
| keyboard-back | `surface-contract.json:15,18`; `checks/check_contract.py:35-36` | Starting in help-closed after Close, use Tab to reach actual Back, record its focus, then Enter. | Clicking Back, invoking its handler, using browser history, or directly focusing Back does not prove sequential keyboard reachability. |
| introduction-focus | `surface-contract.json:15,17-18` | After Back, returned introduction is visible and active element is its h1, distinct from summary focus after Close. | Introduction visibility with body/summary focus fails focus obligation. Question/help absence is useful target-preserved state evidence (`target/verification-protocol.md:10`), not a separately asserted source requirement. |
| read-only-policy | `surface-contract.json:6,18,20` | Log attempted method and allow/block outcome before request dispatch; no forbidden method sent, no answers/results/submission. Retain expected analytics POST attempt and visible effects if observed. | POST, PUT, PATCH, DELETE or any other unlisted method blocked. An unobserved analytics POST is not invented or mandatory to generate. |
| origin-policy | `surface-contract.json:5,18`; `observation-policy.json:2-4` | Each actual destination origin exactly matches allowlist before dispatch, including redirects/subresources; retain denied destination and its effect. | HTTP, sibling subdomain, userinfo trick, different port, external redirect or popup does not gain authorization from similar text. Test guards offline rather than creating forbidden live journeys. |
| provenance/limits | `surface-contract.json:19-20`; target `:3` | Document expected versus observed, fixture status, snapshot scope, blocked effects and all listed exclusions. | No mobile/full-questionnaire/performance/accessibility certification or deployed defect claim from local checks. |

Focus assertions must identify the relevant journey control, not an arbitrary matching element when multiple `summary`/`h1` nodes exist. This is a proposed disambiguation rule; source selectors alone do not guarantee uniqueness. If uniqueness or visibility cannot be established, record the ambiguity and do not fabricate a pass. Exact DOM structure and a supported browser observation mechanism remain unknown.

## Edge-case Gherkin for inclusion or derivation

```gherkin
Feature: Preserve declared keyboard and observation boundaries
  Background:
    Given the run is scoped to en-US and a 1280 by 800 viewport
    And guards authorize only https://qaizen.io and GET, HEAD, OPTIONS
    And no answer has been selected

  Scenario: Summary toggles twice before Close restores focus
    Given the first question is visible and its summary has focus
    When I press Enter
    Then help is open
    When I press Space on the summary
    Then help is closed
    When I press Enter on the summary
    Then help is open
    When I use Tab to reach Close and press Enter
    Then help is closed
    And the journey summary is the active element
    And the first question remains unanswered

  Scenario: Visible introduction cannot conceal failed Back focus
    Given help is closed and Close has restored summary focus
    When I use Tab to reach Back and press Enter
    And the introduction becomes visible
    But the active element is not its heading
    Then keyboard Back activation is recorded separately from failed introduction-focus
    And I do not set focus to manufacture a passing observation

  Scenario: A blocked analytics request has a visible consequence
    Given an in-scope action attempts an analytics POST
    When the method guard intercepts it before dispatch
    Then the POST is blocked
    And the attempted destination and method are recorded
    And any observed UI consequence is retained
    And required transition outcomes are evaluated against their actual state

  Scenario: A redirect does not inherit the entry origin authorization
    Given an authorized GET receives a redirect to another origin
    When the guard evaluates the redirect destination before dispatch
    Then it blocks the out-of-scope request
    And the affected transition is marked blocked or inconclusive with evidence
    And the allowlist is not expanded

  Scenario: Read-only HTTP method does not authorize form submission
    Given a control would submit a form using GET
    When planning the observation actions
    Then that control is excluded from the executable journey
    And no form submission is performed to test this exclusion

  Scenario: A mouse Back observation cannot complete keyboard proof
    Given an earlier observation clicked Back and saw the introduction
    When assessing keyboard-back coverage
    Then that observation is insufficient
    And a separate declared Tab and Enter observation is required
```

The redirect, forbidden-method and GET-form cases describe guard design or offline fixture checks; this task does not authorize sending those requests or performing those actions on the live website. Browser failures are unknown until separately authorized observation. No fixed Tab count or timing threshold is asserted because the supplied sources do not establish one.

## Risks, concrete triggers, severity and response

Severity is this role's proposed planning scale, not a measured deployment finding.

| Risk | Trigger and impact | Severity | Basis / evidence to resolve |
|---|---|---|---|
| False keyboard pass | Protocol continues to click Back; visible return is mistaken for keyboard reachability. | High acceptance-integrity risk | Target `:10` versus contract `:15`; resolve by actual sequential keyboard and focus record. |
| False all-checks pass | Only validator exit status is used to declare browser success. | High acceptance-integrity risk | Checker `:42-43` explicitly limits output; require separate document/browser status. |
| Out-of-scope request | Guard is installed after navigation, checks only top-level requests, or permits redirects without recheck. | High authorization impact, hypothesis about execution mechanics | Contract `:5-6,18`; policy `:2-4`; resolve by documented before-dispatch guard coverage. No such browser implementation has been inspected. |
| Answer/submission scope breach | Test activates answers, a GET form, or result generation while claiming allowed methods make it read-only. | High scope impact | Contract `:6,20`; resolve by allowed action sequence plus unanswered observations. |
| Lost causal evidence | Analytics POST blocked, related UI effect suppressed or ignored. | Medium observation-integrity impact | Contract `:20`; require blocked-attempt and consequence record. The actual effect is unknown. |
| Focus target ambiguity | Multiple matching headings/summaries lead to a passing assertion on an unrelated element. | Medium acceptance-integrity impact, explicit hypothesis | Contract `:17` selectors; browser DOM unknown. Resolve by identifying active journey elements in runtime evidence. |
| Inflated defect claim | Tutorial/document gap is labeled an existing website regression. | High reporting-integrity impact | Contract `:19`, target `:3`; preserve distinction and label unobserved runtime behavior unknown. |
| Unsupported certification | A single viewport/short journey is called accessible, mobile-ready or performance-certified. | Medium decision impact | Contract `:6,20`; include exclusions next to outcome reporting. |

## Questions and challenges reserved for named peers

These are independent questions, not conclusions about unread peer proposals.

- **Product:** Will acceptance require all seven transition IDs, including Space/Enter toggle/reopen, even if the checker remains green? How will protocol readiness be separated from website acceptance and from the useful but target-only question/help absence assertion?
- **Architecture:** What exact boundary ensures all attempted requests and redirect destinations are checked before dispatch? Does any proposed strategy silently allow external assets or a GET submission? Do not claim a particular interception API works without evidence; a document can specify the invariant and leave the host mechanism open.
- **UX:** How will sequential focus evidence distinguish Close restoring summary from Back moving to h1? What observation establishes the correct summary/h1 when selectors match more than one node? Is any proposed direct focus operation accidentally replacing the keyboard behavior being tested?
- **Delivery:** What explicit review or check catches missing prose transitions that the existing validator cannot catch? Are browser observation and tool/harness development accidentally included in a document-only plan? What remains deliverable when runtime observation is unavailable or policy blocking prevents a state?
- **All roles:** Any claim about deployed behavior, precise request side effects, keyboard order, browser timing or severity likelihood needs a supplied source or explicit unknown/hypothesis. Do not convert the expected analytics POST into a requirement to provoke it.

## Alternatives considered

1. Minimal patch replacing only `Click Back` with `Tab ... Enter`: reject as insufficient because explicit help keyboard toggles, scope guards and policy/evidence limits remain omitted (`surface-contract.json:6,11-13,18-20`).
2. Treat validator as complete acceptance oracle: reject; it validates contract data and intentionally cannot observe browser behavior (`checks/check_contract.py:42-43`). In particular it neither reads the target protocol nor enforces the supplied Close traversal.
3. Build a browser automation suite now: defer; source task requests planning and forbids input mutation/network answer retrieval (`TASK.md:3-5`). A future authorized harness may operationalize the planned checks, but no new implementation is necessary to provide a reviewable document change specification.
4. Permit Shift+Tab wherever convenient: source checker permits it for Back, but choose the stricter concrete Tab transitions in the supplied contract. Separately labeled exploratory variants do not satisfy the declared sequence by themselves.

## Completion and unfinished work

Analyze deliverables complete: sourced decisions, acceptance matrix, real edge cases, authorization boundaries, negative cases, evidence requirements, risks, alternatives and peer questions. Full cross-examination and lead adjudication are not yet performed and require the explicitly supplied complete peer reports after the report barrier. Runtime browser behavior, request-guard feasibility in a chosen host, exact focus order and deployment outcomes remain unmeasured; a separately authorized browser observation record would resolve those unknowns. No source edits, network calls, website execution or output other than this report were made by this role.
