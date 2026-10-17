# UX independent analysis — Workflow round 1

Role: UX. Target: `/workspace/worker/target/verification-protocol.md`. Supplied immutable snapshot: `0aa277436d8dcda4d6c2412c6ad4307dd0192b0f6230fa96c8b16d99c8bac194` (identity supplied by lead; not independently recomputed).

Status: complete independent analysis within the 150-second worker budget. No peer reports or conclusions were supplied or read. No network, browser observation, source changes, or implementation occurred. This report is an output artifact, not a change to the target.

## Inspected sources and evidence

All source paths below are relative to `/workspace/worker/`.

- `TASK.md:1-5`: requests qore-plan, a plan to change the target, sourced decisions/acceptance/checks/limits, original project sources as authority, no source mutation or external retrieval.
- `surface-contract.json:4-20`: entire declared public journey, scope, exact transitions, focus obligations, required checks, provenance and limits.
- `checks/check_contract.py:9-43`: validator requirements and explicit boundary that browser observations establish current behavior. Especially `:32-36` distinguishes Close/Back focus and demands keyboard traversal/activation for Back.
- `observation-policy.json:2-4`: sole allowed origin `https://qaizen.io`.
- `target/verification-protocol.md:1-10`: entire existing tutorial target. Its own `:3` denies historical/defect provenance. Its `:6-8` underspecifies Start/help activations and misses the Space/reopen loop; `:10` uses click for Back, conflicting with the declared keyboard journey.
- `.agents/skills/qore-plan/references/protocol.md:5-41`: independent roles, evidence discipline, challenge and adjudication.
- `.agents/skills/qore-plan/references/roles.md:7-11,20`: UX lens and challenge partners, bounded to actual document/host surfaces.

Local measurement: ran `python3 -B checks/check_contract.py surface-contract.json` from `/workspace/worker`; exit 0; result `valid: true`, schema `qaizen-labs-surface/1`, eight required checks listed. This validates contract consistency only. It proves neither the target's coverage nor any website behavior.

Uninspected: deployed HTML, DOM/accessibility tree, screenshots, network behavior, actual focus movement, error/loading messages, mobile layouts, full questionnaire, private website source/commits. These remain unknown; no access was attempted. No prior reports were read.

## Decisions and planned deliverables

D-UX-1 — Preserve the original source hierarchy. The contract and original checker/policy govern the target; the tutorial is the editable subject. Describe the keyboard defect as a protocol coverage gap, not an observed deployment defect (`surface-contract.json:19`; target `:3`). Deliverable: purpose/provenance paragraph separating acceptance obligations, observations to collect later, and unmeasured behavior.

D-UX-2 — Replace vague actions with the exact seven-transition journey below. The single uninterrupted journey must remain unanswered throughout (`surface-contract.json:6,8-18`). Deliverable: numbered procedure plus a state/action/evidence table. Reuse the current target's entry, Start, Close and terminal observations; strengthen their missing details. No website UI change or new automation framework is required by this planning task.

| ID | From → to | Required user action | Observable acceptance / evidence |
|---|---|---|---|
| entry | labs → introduction | At `https://qaizen.io/labs`, click `a[href$='/labs/readiness-check']` | Identify the matching journey link and record arrival at introduction. Record actual final URL/origin without assuming undocumented URL changes. Source `surface-contract.json:4,9`. |
| start | introduction → first-question | Click `Start the check` | First question shown and no answer selected. Preserve an unanswered baseline for later comparison. Source `:6,10,18`. |
| open-help | first-question → help-open | Focus the identified `summary` using ordinary navigation as needed, press Enter | Help visibly opens; record the action and actual state. Source `:11`. No specific post-open focus assertion is declared. |
| toggle-help | help-open → help-closed | On that summary press Space | Help visibly closes while the question remains unanswered. Source `:12`. |
| reopen-help | help-closed → help-open | On that summary press Enter | Help visibly reopens. Source `:13`. This prepares the explicit Close transition; collapsing with Space alone does not cover Close. |
| close-help | help-open → help-closed | Reach Close by Tab; activate with Enter | Help closed and actual active element is the summary. Source `:14,17`. Target `:8` currently permits Shift+Tab; the revised canonical path should say Tab because the supplied transition says Tab. |
| back | help-closed → returned-introduction | Reach Back by Tab; activate with Enter | Introduction visible; active element is the introduction `h1`. Preserve existing terminal checks that question and help are absent (`target:10`); distinguish these retained tutorial checks from the contract's explicit heading-focus obligation (`surface-contract.json:15,17`). |

The specific contract says Tab for Back (`surface-contract.json:15`), even though the checker allows Tab or Shift+Tab (`checks/check_contract.py:35`). Use Tab in the canonical protocol to satisfy both; do not weaken the concrete contract to the checker's broader accepted set. Similarly, Enter/Space/Enter is an ordered requirement, not three interchangeable examples. Close returning focus to summary is separate evidence from Back returning focus to heading.

D-UX-3 — Capture keyboard evidence that cannot be replaced by visual assertions. For Close and Back, record sequential traversal, focused control immediately before Enter, activation event, resulting visible state and actual active element. A screenshot of an introduction or a direct/programmatic focus call cannot prove Back's keyboard reachability or focus restoration. Do not use click or forced/programmatic focus to satisfy those steps. For the initial summary focus, ordinary sequential navigation is a proposed observation technique; the source specifies its control/activation but no traversal constraint. If focus unexpectedly leaves summary between disclosure actions, record that fact and any ordinary navigation used to recover; do not invent a post-toggle focus obligation. Deliverable: per-transition evidence fields (ID, pre-state, control identity, actual traversal/action, post-state, active-element identity where required, unanswered observation, deviation).

D-UX-4 — Preflight is part of observable validity. State en-US, 1280×800, entry/state depth, unanswered policy, same-origin allowance and allowed request methods GET/HEAD/OPTIONS before navigation (`surface-contract.json:4-6`; `observation-policy.json:2-4`). Proposed future execution control: establish request blocking before navigation and retain blocked-request effects. No observation is authorized during this planning run. The expected analytics POST must be blocked; its observed effects must remain in the record (`surface-contract.json:20`). Do not silently allow POST merely because the page needs analytics, and do not label every blocked analytics request a website defect. Deliverable: execution preconditions and policy/deviation evidence section.

D-UX-5 — Do not invent product behavior at loading/error/recovery boundaries. The inputs specify no loading message, empty state, timing threshold, retry control, focus styling or error content. Proposed future method: wait for the named observable state using a declared bounded runner timeout, record actual error/loading/blocked-request effects, and stop the dependent sequence if the expected control/state cannot be established. Mark affected steps blocked/unobserved, distinguish an observable acceptance failure from inability to run, and preserve evidence. If a retry is attempted later, restart a fresh unanswered journey and record it as a separate run. No auto-answer, submission, result generation or undocumented recovery interaction is allowed. The timeout is an operational bound, not a performance acceptance criterion. Deliverable: exception/reporting paragraph with no fabricated UI text.

D-UX-6 — Scope accessibility and content honestly. The required keyboard actions and focus destinations provide narrow keyboard/focus evidence, not accessibility certification (`surface-contract.json:20`). Record visible controls and actual active-element identity; do not infer accessibility names, heading hierarchy or screen-reader announcements from the contract alone. `Start the check`, Close and Back are supplied action identifiers, `summary` and `h1` are supplied targets; uniqueness and exact runtime accessibility names are unobserved. Use en-US only (`:6`); additional locales, translations, localization quality and mobile behavior remain outside scope. Deliverable: explicit coverage/unknowns statement.

## Observable acceptance and checks

1. The revised document maps all eight required check names (`surface-contract.json:18`) to concrete actions, observations, policy evidence or explicit blocking outcomes: entry; unanswered; help-toggle; close-focus; keyboard-back; introduction-focus; read-only-policy; origin-policy.
2. All seven transition IDs appear with the exact activation and ordered disclosure sequence. Tab/Enter Back replaces target `:10`'s click; Enter/Space/Enter appear before Close.
3. Close evidence ends at summary; Back evidence ends at introduction h1. Each requires actual active-element observation, not just visible-page change.
4. Unanswered is a continuing invariant. Observe baseline and after disclosure/Close and before Back; record final absence of the question without inferring preserved answer state in unseen UI. No answers are supplied at any step.
5. Limits include no results, submission, source redistribution, mobile/full-questionnaire/performance/accessibility certification and no deployment identification by private commit (`surface-contract.json:20`).
6. Local checker remains a source-consistency check; documentary review checks target coverage. Neither grants browser pass status. A future browser run is separately needed to establish current behavior (`checks/check_contract.py:43`).

## Risks, triggering conditions and impact

Severity describes impact on this verification plan, not a measured website security or accessibility severity.

- High — Trigger: Back is clicked, focused directly, or its heading is asserted without recording Tab/Enter and active element. Impact: an inaccessible/unreachable keyboard Back or failed focus restoration can go undetected. Sources `surface-contract.json:15,17`; checker `:32-36`; current target `:10` demonstrates the protocol gap.
- High — Trigger: close-help and back share one generic focus assertion. Impact: the two distinct required destinations can be confused, producing false passes. Sources `surface-contract.json:14-17`; checker `:33-34`.
- Medium — Trigger: only Enter-open/Close is documented, omitting Space-collapse and Enter-reopen. Impact: help-toggle acceptance remains untested even if Close works. Sources `surface-contract.json:11-14`; target `:7-8`.
- High — Trigger: future execution permits answer selection, nonallowed origins/methods, submission, or continues through a policy breach. Impact: run exceeds authorized scope and cannot substantiate read-only acceptance. Sources `surface-contract.json:5-6,18,20`; observation policy `:2-4`. This is a prospective execution risk, not an observed breach.
- Medium — Trigger: blocked analytics causes altered UI, a timeout, or an error and the record omits it. Impact: misleading report of normal behavior under enforced policy. Source `surface-contract.json:20`; exact actual effect unknown.
- Medium — Trigger: source/checker pass or a historical baseline is presented as current browser evidence. Impact: unsupported claims of deployment success/failure. Sources `surface-contract.json:19`; checker `:43`.
- Low — Trigger: the canonical procedure allows Shift+Tab because target/checker allow it, while concrete contract says Tab. Impact: unnecessary source ambiguity; using Tab resolves without expanding scope. Sources contract `:14-15`, checker `:35`, target `:8`.
- Medium hypothesis — Trigger: multiple matching summary/heading/control candidates, delayed state, unexpected focus movement, or ambiguous unavailable controls at runtime. Impact: observers might act on the wrong element or misclassify a blocked observation. Smallest resolution is a permitted future DOM/active-element observation; no uniqueness or timing claim is justified now.

## Questions for named peers and alternatives

Architecture: Can your plan achieve all transitions with one amended document and a compact evidence table, reusing the existing contract and checker? A new harness/schema or forced-focus helper would add operator complexity and may obscure keyboard reachability. Smallest check: map each proposed mechanism to a required check and remove mechanisms with no source obligation. Which host-level boundary enforces origins/methods before future navigation, including redirect destinations? This is an implementation choice to describe only as far as the supplied evidence supports.

QA and security: Will your acceptance matrix distinguish the three summary actions from the explicit Close action and require separate Close/Back focus evidence? Concrete failure case: Enter opens, Space fails, Close works; a coarse help-toggle row could pass falsely. Another: Back returns the right page but leaves focus on removed content. Smallest check: one row per transition plus continuing unanswered/policy invariants, and explicit no-browser-evidence status today.

Product: Does preserving target `:10`'s question/help-absence check add any intended claim beyond visible returned introduction? Keep it as existing observable coverage but label it separately from the exact contract focus requirement. Do not infer stored questionnaire state.

Alternatives: (A) Only replace click Back with Tab/Enter: smallest textual change, rejected as insufficient because the required Enter/Space/Enter sequence remains omitted. (B) Full site/accessibility test campaign: deferred/out of scope; would exceed original limits. (C) One exact ordered journey, policy preflight, compact evidence table and honest reporting limits: selected proposal because it directly covers original sources without inventing site implementation.

## Unfinished work

Cross-examination remains pending until the lead supplies all five independent reports. No browser observations or target implementation are part of this planning-only assignment. Unknown runtime selectors, focus behavior, loading/error content and effects of blocked analytics require a later authorized public observation; none can be resolved by rewriting the protocol or running the local checker. The lead must adjudicate any peer disagreements and produce the consolidated change specification and run evidence.
