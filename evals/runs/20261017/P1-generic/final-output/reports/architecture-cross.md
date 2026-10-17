# Architecture — one Workflow cross-examination pass

Role: Architecture. Target: `/workspace/worker/target/verification-protocol.md`. Supplied snapshot: `0aa277436d8dcda4d6c2412c6ad4307dd0192b0f6230fa96c8b16d99c8bac194`; supplied identifier, not recomputed or treated as deployment identity.

## Execution and context substitution

This is a fresh Architecture-role continuation context, substituted because the original Architecture context was no longer listed by the host. I am not the original actor and have not repeated independent Analyze. I read the complete original Architecture proposal and all four peer Analyze reports after the lead-supplied barrier at `2026-10-17T10:28:02.060147Z`, then performed this single cross-examination pass. Original reports remain preserved without edits. Substitution limits actor continuity; the lead must report it rather than describe the original worker as returning. No second independent Architecture report, additional quality round, implementation, network retrieval, browser observation, or subagent work occurred.

Read complete supplied originals: `TASK.md:1-5`, `surface-contract.json:1-21`, `checks/check_contract.py:1-54`, `observation-policy.json:1-5`, `target/verification-protocol.md:1-10`. Read complete `/workspace/output/reports/product-analysis.md`, `architecture-analysis.md`, `ux-analysis.md`, `delivery-analysis.md`, `qa-analysis.md`; oversized combined tool output was recovered by smaller reads, including a full standalone Delivery report. Also read qore-plan SKILL, protocol and roles instructions. Browser/tool enforcement capabilities and DOM remain uninspected. Peer reports are challenge inputs supplied by the lead, not replacement project authority.

## Challenge C-A1 — Product's unanswered invariant needs an observable baseline

Peer decision: Product P2/AC6 requires no answer at any point and checks after entering first question and before leaving; P6 adds an unanswered-observation field. Architecture A7 and UX observable check 4 likewise carry the invariant; QA's unanswered row proposes visible/model-exposed state inspection.

Counterexample: a prior browser session restores a selected answer automatically on Start. The observer never clicks an answer, records only that fact, traverses help and Back, and incorrectly reports unanswered throughout. Conversely, inspecting an undocumented internal model or forcing a reset would introduce implementation assumptions or alter the state being observed. Merely reaching returned introduction cannot prove stored answer state after the question is no longer presented.

Smallest investigation performed: inspected complete contract scope/transitions/limits and peer acceptance rows; local JSON inspection confirmed scope has `answer_policy` but no explicit unanswered-indicator field. Contract `:6,18,20` establishes the obligation without supplying the indicator. No browser was used to invent it.

Outcome/revision: strengthen A7 and architecture acceptance: the future observer must identify a nonmutating, browser-observable selected/unselected state of the actual first-question answer controls, record the observed baseline after Start and its persistence through disclosure/Close immediately before Back, plus the action trace showing no answer/submission. An identifiable rendered or accessibility/control state is sufficient; a new internal-state API is not required. If no reliable indicator is available, classify unanswered as not observed/inconclusive and do not claim overall conformance. Do not infer hidden storage state after Back, and do not choose/reset an answer to manufacture a baseline. This resolves the protocol wording ambiguity; exact runtime indicators remain unresolved pending a separately authorized run.

Severity preserved: original Architecture Medium risk that a default/persisted answer goes unnoticed; QA/Product High scope impact if an answer/submission actually occurs. Lack of proof is not itself a measured scope breach. No runtime likelihood is claimed.

## Challenge C-A2 — UX's retained absence check risks becoming a new DOM contract

Peer decision: UX D-UX-2 Back row says preserve terminal question/help absence checks; UX observable check 4 says record final absence. Product P4 instead makes this optional and says “not presented”; Delivery D6 permits supplemental treatment or replacement; QA introduction-focus row calls it useful target-preserved evidence rather than a source requirement. Architecture A8 previously left the interpretation for Product/UX adjudication.

Counterexample: the returned introduction is displayed and its h1 receives focus, while question/help nodes remain in DOM but are hidden. A DOM-count-zero assertion would fail this implementation without a source requirement. Another case displays an introduction but leaves the previous question visible; that is potentially contradictory state evidence, but still does not establish a mandatory node-removal mechanism.

Smallest investigation performed: compared target `:10` with contract states/transitions/focus `:7,15,17` and full peer positions. Local contract inspection found no explicit DOM-removal field; complete source inspection, rather than that field-name test alone, establishes the absence of a supplied DOM-removal requirement.

Outcome/revision: resolve Architecture A8 in favor of Product P4 and Delivery D6: require returned introduction visibility and actual introduction h1 focus; retain a separately labeled optional observation that question/help are “not presented.” Do not require nodes to be detached, empty DOM matches, inaccessible storage, or any inferred visibility mechanism. Optional-check failure is not automatically a contract failure. If observed prior content makes the expected returned-introduction state ambiguous, record that ambiguity and withhold that state pass on the actual evidence. UX's broader retention can be preserved as supplementary evidence, without a new release gate. This is this role's recommended resolution; lead adjudication remains required, and no peer agreement is invented.

Severity preserved: Architecture's original Medium risk of silently broadening source obligations remains Medium; Product classifies the unsupported DOM interpretation Low, Delivery the extra acceptance gate Medium. The disagreement in scale is retained because the consequences differ, not averaged down.

## Challenge C-A3 — UX evidence and recovery must stay usable and must not repair focus proof

Peer decision: UX D-UX-2 requests a numbered procedure plus state/action/evidence table; D-UX-3 asks for precontrol focus, action, poststate, active element, unanswered and deviations; D-UX-5 proposes bounded timeout and fresh-run recovery. Architecture A7 proposes a long evidence-field list. Product P6 and Delivery D1 call for a small ledger.

Counterexample: duplicating the seven-transition procedure and the same full metadata in every evidence row makes an operator skip entries or conflate expected with observed. A second failure case occurs when Close visually closes help but focuses body: an operator Tabs back to summary to continue and later reports an unbroken successful canonical journey. A third case loses focus between Enter/Space; restoring it by direct focus can conceal real behavior if reported as original focus retention.

Smallest investigation performed: compared UX table/fields/recovery with Architecture A4/A7/runtime steps and all seven contract transition records `:9-15`. No supplied source requires an extra backend, schema, fixed Tab count, duplicated full metadata, mandatory screenshot set, timeout value, or posttoggle focus destination.

Outcome/revision: keep one compact ordered action/evidence table, shared run metadata once, and expectation separate from observation; IDs can map seven transitions onto the eight check labels. Record actual key/traversal path and relevant control identity, observed result, required focus checkpoint, unanswered observation and evidence/deviation reference. Shared metadata includes environment, policy and source identity. Do not demand a duplicate narrative or executable evidence schema. Ordinary navigation to summary before its specified activation remains a procedure detail, recorded without creating a new contract traversal obligation. Unexpected focus between summary actions may be recorded with ordinary navigation as a deviation; the source has no posttoggle focus assertion. Close-to-summary failure remains failed: recovery must not replace its evidence, and any later observation under altered prerequisites is separate rather than proof of the canonical chain. No direct focus correction can satisfy Close/Back focus assertions.

A runner may declare an operational timeout later, clearly distinguished from source acceptance/performance thresholds. No specific timeout or Tab count is justified here.

Severity preserved: High original Architecture risk of assembling a false success chain; Medium operator/evidence ambiguity is a prospective usability impact, not measured user behavior. Simpler record presentation must not erase distinct focus facts.

## Challenge C-A4 — Product and Delivery guard prerequisites must not become a harness build gate

Peer decisions: Product P5 requires enforcement before navigation, P7 separates document/browser acceptance; Delivery D4 requires an enforceable pre-navigation gate but D1 excludes harness implementation. QA QA-4 asks for fail-closed checks on every attempted request, navigation and redirect before dispatch. Architecture A5 contains the same prevention proposal.

Concrete failure: navigating first and installing filters afterward can already dispatch an external asset or analytics POST. Top-level-only filtering can miss subresources; a GET submission remains forbidden despite allowed method. Conversely, requiring a new framework or proof from the live site before completing the requested document plan exceeds `TASK.md:3-5` and turns unavailable runtime tooling into a false documentation blocker.

Smallest investigation performed: checked actual supplied file/reader boundaries and checker read path; JSON inspection confirms contract/policy origin arrays equal exactly `https://qaizen.io`. Checker reads only its JSON argument (`checks/check_contract.py:46-51`), not policy or Markdown. There is no supplied executable browser guard to reuse or establish as working. No browser inventory or host capability was inferred.

Outcome/refinement: preserve pre-request prevention as a future execution prerequisite covering methods and origins of navigation, redirects and page-initiated requests. Do not name an interception API, assert service-worker/background coverage, add origin exceptions, or claim the guard already exists. The future operator must establish that chosen environment can enforce the stated request boundary before first navigation; unresolved coverage means run blocked/not run. Contract/policy disagreement also blocks execution until explicitly resolved, without editing authority to pass.

The document plan and later document edit remain deliverable using source review and the existing checker. They need only specify the guard invariant, readiness evidence, boundary limitations and no-run behavior. No harness build, guard test suite, browser run or website repair is a prerequisite for this plan. Optional future guard evaluation may use safe offline fixtures rather than intentionally transmitting forbidden requests. This answers Product, Delivery and QA's Architecture questions at the level warranted by supplied evidence; actual host mechanism remains unresolved.

Severity preserved: High authorization impact if a forbidden request escapes; Medium overbuild/scope impact if tooling is made a documentation prerequisite. No hypothetical browser mechanism is promoted to a project fact.

## Challenge C-A5 — QA warnings: separate denied requests, failed acceptance and dependent unobserved checks

Peer decision: QA QA-4/5/6/7 and matrix/Gherkin distinguish guard denial, required transition outcomes and evidence layers. Product P6's original ledger lists pass/fail/not observed but not a distinct blocked status. UX D-UX-5 and Delivery D5 require failure versus unavailable-observation distinction. Architecture A6/runtime step 6 warns against a fabricated continuation.

Concrete failure paths:

1. Analytics POST is blocked, help never opens, and a report marks all checks passed because the expected policy denial occurred.
2. Guard blocks an external resource; the record labels a website defect even though the policy-limited environment prevented establishing the state.
3. Space fails to collapse help, but Close works; a single coarse help-toggle row reports success.
4. Close yields body focus; later Tab actions and a successful h1 are spliced into a nominal successful canonical chain.
5. No analytics POST occurs during the run; the observer provokes one or invents its presence to satisfy an expected-blocking item.

Smallest investigation performed: compared QA's per-transition matrix and Gherkin with source limits `:20`, all transition prerequisites `:9-15`, and Product/UX outcome fields. Source says retain observed effects; it does not authorize provoking POST or guarantee occurrence in each execution. No measured UI consequences exist in supplied sources.

Outcome/revision and warning to QA: retain QA's separate layers and per-transition observations; include pass/fail/blocked/not observed with reason, or equally explicit outcome+cause fields. A functioning denial can satisfy the observed policy decision while UI acceptance separately fails or remains unobserved. If expected state is established and a required behavior demonstrably fails, record failure with evidence. If enforcement/environment/control ambiguity prevents establishing prerequisite or observation, record blocked/not observed rather than inventing product causality. Downstream canonical steps with unmet prerequisites remain not observed/blocked; separately restarted or exploratory observations cannot erase the failed original. Record actual blocked method/destination and visible effect without payload/source redistribution. If analytics is not attempted or its effects cannot be determined, explicitly state that limit; never provoke or fabricate it. Policy relaxation cannot be recovery.

Severity preserved: Medium lost-causal-evidence/analytics-effect risk, High false-success-chain and forbidden-request risks, Medium focus-target ambiguity. These are planning consequences, not measured deployment incident findings.

## Revised Architecture proposal and interfaces

A1–A3 remain: authority unchanged; all seven exact transitions; canonical Tab for both Close and Back despite permissive validator. A4 remains with genuine sequential evidence and distinct Close-summary/Back-h1 observations. A5 is clarified as a future-run guard capability gate, not an implementation prerequisite. A6 adds explicit cause/outcome separation and no provocation. A7 is narrowed to shared metadata plus one compact expectation/observation ledger and an identifiable unanswered baseline. A8 is resolved to optional “not presented” evidence without a DOM-removal contract.

Producer/consumer boundary stays: original contract/policy → document expectations → later authorized observer/guard → observed state, focus, unanswered and request outcomes → reviewer classifications. Local checker consumes only contract JSON. Protocol only consumes source fields and names evidence to collect; it does not add a storage/service/transaction API. The website owns actual runtime behavior; observer owns actions; guard owns prevention; reviewer owns interpretation. Unknown host enforcement is explicit rather than hidden in a new helper. Documentation readiness and website acceptance stay separate.

## Actual commands/checks and results in this pass

- `cat /workspace/worker/.agents/skills/qore-plan/SKILL.md` and `cat` of protocol/roles references: complete reads, no changes.
- Batched `cat` commands read all five complete Analyze files and supplied original project files. Truncated combined display was recovered through smaller reads; full Architecture/UX and standalone Delivery were inspected.
- `python3 -B checks/check_contract.py surface-contract.json` in `/workspace/worker`: exit 0, `valid: true`, schema `qaizen-labs-surface/1`, all eight required-check IDs, explicit consistency-only limit. This fresh result supports source consistency only.
- Read-only `python3 -B -` JSON/source inspection: equal origin arrays; exact seven IDs `entry,start,open-help,toggle-help,reopen-help,close-help,back`; scope keys locale/viewport/depth/answer_policy/allowed_methods; focus targets summary→summary and introduction-heading→h1; no explicit unanswered-indicator/DOM-removal fields; checker reads only `Path(sys.argv[1])`. Field-name checks supplement complete reading and do not prove runtime semantics.
- `clock__curr_time`: observed `2026-10-17 10:30:26 UTC` during this pass. This is not browser or deployment evidence.
- Only output mutation: this cross report under `/workspace/output/reports/architecture-cross.md`. No supplied source or prior report was changed.

## Limits and unfinished items

One cross pass complete within the bounded assignment; no assigned source challenge remains unfinished. Lead adjudication remains pending. This context substitution prevents a claim of original-actor continuity; report it in run evidence. No unanimous peer agreement is claimed. Remaining runtime uncertainties: exact selected-state indicators and control disambiguation, actual focus/tab order, state timing, guard implementation and all request-surface coverage, current deployment behavior, occurrence/effects of blocked analytics. A separately authorized policy-enforced observation could resolve these; they do not block a source-grounded document-change specification. No additional cross/quality round is requested.
