# QA and security — one Workflow Cross-examine pass

Role/context: QA and security, `/root/qa`. Snapshot remains `e9aeec2eee10b52c3339b53b4e491d3ff69f57c68be2f5ea1d61e70df55acccc` (entire prepared-input manifest, lead-provided; not independently recomputed). Initial report remains intact at `/workspace/output/reports/qa-analysis.md`. This separate report records corrections and challenges after the lead's report barrier; it supersedes the identified ambiguous portions, not the preserved initial evidence.

## Inputs and procedure

Read all five returned initial reports: `/workspace/output/reports/product-analysis.md`, `architecture-analysis.md`, `ux-analysis.md`, `delivery-analysis.md`, `qa-analysis.md`. The initial bulk retrieval was truncated, so Architecture/UX/Delivery were retrieved again and UX was retrieved separately in full; Product was visible in full in the first retrieval, and QA is my complete authored initial report. Re-read all disputed raw sources: `surface-contract.json:1-21`, `checks/check_contract.py:1-54`, `observation-policy.json:1-5`, `target/verification-protocol.md:1-10`. No browser/network/input edits, new tests, child agents, deployment claims, or source redistribution occurred. No peer cross-examination files were read: this is the single authorized challenge pass, not an iterative extra debate.

## Material challenge and correction: traversal evidence

Exact disagreement: my initial D4 says one permitted sequential path suffices for the current target; Product decision 6 similarly preserves either direction. Architecture A3 and Delivery D5 require canonical Tab for the concrete contract trace and retain Shift+Tab as supplementary. UX's state requirements also distinguish canonical Tab and the retained alternative.

Counterevidence to a broad reading of my D4: `surface-contract.json:14-15` declares Tab for BOTH Close and Back. `checks/check_contract.py:35-36` permits Tab or Shift+Tab for Back, but this validates the admissibility of a contract field rather than establishing that a reverse traversal executes the actual supplied contract's Tab value. Close's direction is not explicitly checked there at all. The current target `:8,10` independently permits both directions. Therefore the supplied target is not defective merely for permitting Shift+Tab, but an observation using Shift+Tab alone must not be labeled literal Tab evidence.

Resolution recommended: accept Architecture A3/Delivery D5 with narrow wording. Document Tab as the canonical trace for matching the actual declared transitions; explicitly preserve Shift+Tab as a permitted existing procedural alternative and record the direction actually used. A reverse-only run can establish the target's broader sequential-route observation, but leaves the literal forward-Tab trace not observed. Do not demand BOTH directions for acceptance, mark reverse traversal invalid, remove the alternative, change JSON/checker, or claim reverse evidence proves forward reachability. This is evidence labeling and contract correspondence, not a new website behavior requirement.

Smallest useful investigation: compare only target `:8,10`, contract `:14-15`, checker `:32-36`; done in this pass. No browser or source change is needed to resolve the logical distinction. I revise initial D4/P6/P7 accordingly. Product's alternative can be retained with an explicit distinction between satisfying the existing protocol route and proving the literal declaration. The point of divergence is now resolved in this role's recommendation; lead adjudicates it.

Concrete failure case: Tab moves from summary through many controls, while Shift+Tab reaches Back quickly. A reverse-only success proves neither that forward Back was reachable within the bound nor that forward focus order behaved correctly. Conversely, a reverse-only observation remains real sequential-keyboard evidence under the existing target and must not be erased as invalid.

## Challenges to each role

### Product — decisions 6 and 7, bound and outcomes

Challenge: decision 6 correctly says exhaustion means the protocol cannot complete its proof; decision 7 uses pass/fail/not-observed. Without linking these, an executor can record a failed 24-step run as a proven website accessibility/contract defect or can call the whole journey passed from its completed earlier steps. Counterevidence: target `:10` alone supplies the numeric bound; contract `:15,18` supplies reachability/focus obligations without a numeric maximum; contract `:20` disclaims certification.

Smallest investigation: map the exhausted guard separately to a procedural outcome, actual keyboard reachability evidence, and unperformed return/focus checks. Proposed answer: record `bound exhausted` as failure to demonstrate the bounded procedural check; mark unperformed Back activation and return/focus NOT OBSERVED; do not infer a product numerical-limit violation. If a focus trap or missing Back is actually observed, record that exact mismatch independently. No generic website diagnosis follows from the count alone.

Product decision 5 and scope: preservation of repeated unanswered checkpoints and absence assertions is correct. No counterevidence supports deleting them. The report's High help-coverage severity is a judgment about evidence consequence, not measured user harm; retain its qualifier rather than importing it as a confirmed high-severity application defect.

### Architecture — A3, A4 and A7

A3: accepted with the narrow evidence distinction above. Refute any interpretation that supplemental means mandatory second run: neither contract nor target requires both directions. The minimal correction is a canonical-route sentence plus actual-direction evidence field.

A4: the proposed count begins after Close. Concrete failure: Close fails its summary-focus assertion, but an executor force-focuses summary before counting and claims a clean Back run. Sources: contract `:14,17`, target `:8`. Clarify that the start is the OBSERVED restored summary focus; if that precondition fails, record Close-focus FAIL and subsequent sequential proof NOT OBSERVED unless performed as a separately identified diagnostic run, never a repaired pass. No diagnostic run is required by this plan.

A7: wording classifying remaining proof incomplete when a control cannot be reached is useful, but distinguish missing evidence from an observed failing condition. Concrete failure: introduction becomes visible with focus on body; describing all return evidence merely incomplete conceals the directly observed heading-focus mismatch. Smallest investigation: classify each assertion, not just each journey. Visible return can PASS, heading focus FAIL; later unperformed checks NOT OBSERVED. Policy denial alone is not an application defect.

Architecture A5 security wording is supported and within scope. No supplied enforcement implementation exists; reject any inference that documentation changes deploy a guard. If guard installation/enforcement cannot be confirmed, do not start observation. This is a procedural fail-closed rule, not a request to implement interception.

### UX — decisions 4 and 5, recovery and observability

UX decision 4's stop rule and decision 5's actual-focus evidence are supported. Omitted edge condition: Back first receives focus exactly on step 24. A preemptive stop on reaching the count would reject a valid bounded trace. Inspect the focus outcome of action 24; if Back is focused, Enter is permitted; if not, stop before action 25. Enter is activation, not a traversal step. Scope: clarify the existing bound rather than adding a new Close count or timing threshold.

Recovery wording says stop the affected sequence on missing controls, lost unanswered invariant, origin breach etc. Distinguish an actual policy breach from an expected blocked attempt: a correctly denied analytics POST is not a reason by itself to abort an otherwise observable journey. Its effects remain evidence; continue only while guards hold and required state/answer invariants remain observable. Conversely, if an unauthorized request actually escaped rather than being blocked, stop and record the policy breach; do not describe it as normal blocked analytics. Sources: contract `:6,20`, policy `:2-4`.

Smallest investigation: two paper traces (denied POST with intact journey; denied POST prevents state loading) are sufficient to validate classification wording. No runtime experiments or invented error copy are needed.

### Delivery — D4, D5 and definition of done

D5 accepted with the narrowed canonical/alternative distinction. D4 properly keeps exhaustion separate from numerical product defect. Challenge definition-of-done item 4 allowing traversal interpretation to remain merely marked unresolved: this is acceptable for a PARTIAL/decision-unready plan, but a claimed complete, implementation-ready replacement should contain the explicit chosen semantics. Smallest investigation: inspect final replacement and decision record for the canonical Tab/retained alternative sentence and 24-action boundary. If lead chooses otherwise, preserve this role's dissent and the literal-contract evidence limitation rather than manufacturing consensus.

The 55–90-minute delivery estimate is explicitly an assumption-based prospective range, not a measured duration; no adverse finding. Do not turn it into a task completion promise. Definition of done correctly excludes browser/app changes and requires preservation. No supplied source establishes an application deployment/rollout dependency; documentation-only rollout/rollback is adequate.

### QA self-review — D3, D4, D5, matrix N1/N4/E1 and Gherkin

D4 corrected as above. Initial N4 and Gherkin say bounded proof fails; clarify that this is a procedural demonstration failure, not automatically `keyboard-back` product nonconformance. Unperformed activation/return-focus must be NOT OBSERVED.

D3/N1's cross-origin and deceptive-prefix cases are useful NEGATIVE EXAMPLES of policy semantics. They do not authorize initiating hostile requests or adding browser guard tests to this doc-only work. No new runner, attack traffic, fixture suite or scheme expansion is required. The parsed-origin recommendation is a proposed robust interpretation; runtime enforcement remains unknown.

D5's combined NOT OBSERVED/BLOCKED label is underspecified. Use three assertion outcomes PASS, FAIL, NOT OBSERVED, plus a cause/context field such as blocked request, bound exhaustion or unavailable state. This keeps cause separate from observed truth. Overall PASS requires every required obligation's relevant evidence; static checker PASS cannot fill runtime gaps.

E1 says URL metadata but full URLs may contain tokens/query identifiers. Retain only necessary sanitized URL/origin/method/status, omit credentials, cookies, sensitive queries/payloads and page-source redistribution. This is a low-risk data-minimization proposal, not evidence of current leakage or an additional project security policy. Avoid full DOM/network dumps as default. Privacy remains conditional, not a release-blocking invented vulnerability.

## Precise proposed counting and classification conventions

These conventions clarify the target's existing guard and must be labeled procedure conventions, not independent product invariants:

1. Establish actual summary focus after Close and observe unanswered state; do not reset focus to create that precondition.
2. Count each Tab or Shift+Tab traversal action toward Back once. For the canonical literal trace use Tab; a reverse or mixed-direction trace records actual direction and does not claim pure forward-Tab evidence. Count backward/forward oscillations, do not reset the count.
3. Initial summary focus is count zero; Enter is not a traversal action. Inspect focus after each counted action. Back focused on action 24 is within bound; no action 25 is allowed for this bounded proof. Keep actual start, direction sequence and terminal focus; record unexpected early focus or departures.
4. The 24-action bound applies to Back traversal only, not help toggles, Close traversal, total journey actions or elapsed loading time. No supplied timing deadline for page transitions is invented.
5. PASS means the individual expected condition was observed. FAIL means a directly observed condition contradicts it. NOT OBSERVED means missing/unperformed evidence; record the reason. Bound exhaustion is recorded as procedural failure to demonstrate within guard, with no fabricated Back activation or heading-focus result. A blocked request can be recorded alongside either observable PASS/FAIL results or NOT OBSERVED assertions.
6. An unavailable guard before navigation prevents execution. A guard breach during observation stops the run. Correctly blocked attempts remain denied and their effects retained; do not relax policy. Later steps not performed cannot pass. Loss of unanswered state stops the affected journey before any submission/results.

Edge-case additions to original Gherkin:

```gherkin
Scenario: Back receives focus on the last permitted traversal
  Given Close restored actual focus to summary and the question is unanswered
  When canonical forward Tab action 24 focuses Back
  Then the traversal bound is satisfied
  And Enter may activate Back without adding a traversal count
  And returned visibility, absence and heading focus are checked separately

Scenario: A reverse-only success is accurately labeled
  Given the supplied target permits Shift+Tab and the declared transition says Tab
  When Shift+Tab reaches Back within 24 recorded traversal actions and Enter returns
  Then the actual sequential reverse route and return observations may be recorded
  But the literal forward-Tab trace remains not observed
  And a second reverse run is not required to complete a canonical forward run

Scenario: Close focus failed before Back proof begins
  Given Enter on Close closed help but actual focus is not on summary
  Then Close-focus fails
  And I do not force focus to summary and call the complete prescribed trace passed
  And unperformed Back and heading-focus assertions remain not observed
```

## Risk adjudication and preserved boundaries

High conditional risks from the initial report remain: prohibited observation if guards are bypassed, and loss/false proof if existing keyboard obligations are rewritten away. Their triggers are concrete document changes or future execution decisions; no exploit or live defect was measured. Medium risks remain documentary transition omission, false static-to-runtime confidence, focus-state conflation and hidden blocked-request effects. Low privacy/source-retention concern remains explicitly hypothetical. Product/Architecture/UX severity differences do not imply consensus about application defect severity; retain the role-specific evidence and consequence qualifiers.

No peer proposed weakening the already-present Back/Close proof or required unanswered/absence assertions. Those preservation decisions survive challenge. Help Enter/Space/Enter and pre-navigation origin/method/scope clarification are supported independently by all reports and source references. No supplied evidence justifies new APIs, database work, application fixes, live-browser prerequisites, or changing the checker/contract/policy.

## Unfinished work and handoff

This role's one cross-examination pass is complete. Lead must adjudicate precise final wording and publish the consolidated source/preservation map and honest evidence categories. Current deployment behavior, request effects, actual tab order/focus and enforcement implementation remain unobserved, intentionally outside this documentation plan. There is no unresolved QA objection to a concise doc-only proposal incorporating the corrections above. If the lead adopts either-direction-only literal contract acceptance, retain my contrary evidence interpretation as a minority position. No further role round is requested.

Actual completion UTC: 2026-10-17T11:47:21Z. Report completed approximately five seconds after the declared 11:47:16Z worker deadline; no investigation continued afterward. All available cross-examination findings are saved; final synthesis remains with lead.
