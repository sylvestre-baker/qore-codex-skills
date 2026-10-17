# Product analysis — independent Analyze pass

Role: Product. Target: `/workspace/worker/target/verification-protocol.md`. Supplied immutable snapshot: `0aa277436d8dcda4d6c2412c6ad4307dd0192b0f6230fa96c8b16d99c8bac194` (identifier supplied by lead; independently recomputing it was not part of this pass). Status: complete independent analysis; cross-examination awaits the report barrier. No implementation, source edits, network retrieval, or browser observation performed.

## Sources and evidence boundary

Inspected all lines of `TASK.md:1-5`, `surface-contract.json:1-21`, `checks/check_contract.py:1-54`, `observation-policy.json:1-5`, `target/verification-protocol.md:1-10`, `.agents/skills/qore-plan/references/protocol.md:1-41`, and `.agents/skills/qore-plan/references/roles.md:1-22`. `find .. -name AGENTS.md -print` returned no files. `rg` was unavailable; ordinary file reads supplied the complete documents.

Authority: the task asks for a plan, and expressly identifies the original project files as authority and the tutorial as the target (`TASK.md:3-5`). The surface contract defines the desired journey. The checker establishes limited consistency invariants; its permissiveness does not waive stricter concrete values in the contract. The observation policy independently restricts origins to `https://qaizen.io` (`observation-policy.json:2-4`).

Uninspected: website/current deployment, private source and commit history, browser tooling, any non-supplied implementation, and other roles' conclusions. These are not facts available to this independent pass. Current website conformance remains unknown by design (`surface-contract.json:19`; `checks/check_contract.py:42-43`).

Local measurement: in `/workspace/worker`, `python3 -B checks/check_contract.py surface-contract.json` exited 0 and returned `valid: true`, all eight declared checks, and the limit “Contract consistency only; browser observations establish current behavior.” This is a local consistency observation, not browser proof. Command output was observed in this role's tool result; no standalone output artifact was created.

## Outcome, users, and smallest useful version

Desired outcome: a reader can execute a bounded, unanswered journey and obtain evidence that each declared transition, including keyboard Back and distinct focus destinations, met or failed its acceptance obligation. Counting checklist rows or obtaining a green contract checker is a proxy, not that outcome. The planning deliverable should enable a later protocol edit; this task does not authorize conducting live observation or repairing the website (`TASK.md:3-5`; supplied lead scope).

User stories:

- As an observer, I can follow the declared entry and state journey without selecting an answer, submitting a form, producing results, or leaving the permitted origin/method boundary (`surface-contract.json:4-6,9-15,20`; `observation-policy.json:2-4`).
- As a keyboard user, I can open, toggle, reopen, and close help, then return to the introduction through the declared keys and traversal, with focus observed at the two distinct destinations (`surface-contract.json:11-17`).
- As a reviewer, I can distinguish a documented acceptance obligation from an actual observation and know exactly which checks have evidence, failed, or could not be observed (`surface-contract.json:18-20`; `checks/check_contract.py:42-43`).

Smallest useful version: change the single protocol document to include scope and policy setup, the seven contract transitions in order, observable state and focus checks, evidence/outcome fields, and explicit limits. Reuse the supplied validator as a local prerequisite. A new runner, schema, test framework, browser integration, deployment, broad accessibility audit, or website change is not necessary to make this document plan useful. Such work would require a separately demonstrated need.

## Proposed decisions and deliverables

P1 — Preserve the tutorial disclaimer and identify the authority. `target/verification-protocol.md:3` already correctly disclaims historical authenticity and defect proof. Add references to the three original project sources and distinguish declared acceptance from measured behavior (`TASK.md:5`; `surface-contract.json:19`). Deliverable: provenance/scope paragraph in the proposed replacement outline.

P2 — Make the whole declared transition sequence executable. Replace the underspecified help opening at target line 7 with summary + Enter; insert summary + Space to close and summary + Enter to reopen; close by Tab traversal then Enter; replace the mouse Back at line 10 with Tab traversal then Enter. Preserve clicks for entry and Start because those are the declared activations (`surface-contract.json:9-15`). Deliverable: transition-by-transition procedure with before state, target, action, resulting state, and focus assertion where specified.

P3 — Follow the concrete contract's Tab value. The existing tutorial allows Tab or Shift+Tab for Close (`target/verification-protocol.md:8`), while the contract sets Tab for Close and Back (`surface-contract.json:14-15`). The checker allows Tab or Shift+Tab for Back (`checks/check_contract.py:35-36`), but does not turn that allowance into the selected journey. The plan should use Tab for both. Other traversal directions can only be explicitly labeled additional explorations outside the minimum evidence path. Do not alter the contract to rationalize the target.

P4 — Separate focus proof from destination visibility. Require observation of active/focused summary after Close and focused introduction `h1` after Back, in addition to relevant state visibility (`surface-contract.json:14-17`; `checks/check_contract.py:32-34`). A screenshot showing a heading alone is insufficient to prove focus. The target's extra assertion that question and help are “absent” (`target/verification-protocol.md:10`) is not an express source obligation. Proposal: retain only as an optional visual-state check, worded “not presented,” rather than silently requiring removal of DOM nodes. Actual DOM structure remains unobserved.

P5 — Add bounded preconditions and observation policy. State exact entry URL, `en-US`, 1280×800, entry/state depth, unanswered policy, only GET/HEAD/OPTIONS, and exact permitted origin. Require policy enforcement before navigation and retention of observed blocked analytics POST effects (`surface-contract.json:4-6,20`; `observation-policy.json:2-4`). The concrete guard implementation is a later tooling choice, not a supplied fact. If required enforcement is unavailable, protocol execution must be recorded as not run/blocked rather than silently weakening scope. This stop/report behavior is a Product proposal derived from preserving the source boundary.

P6 — Add a small evidence ledger linked to the eight existing required-check IDs. Proposed fields: run date and browser/environment; contract snapshot/version; transition/check ID; URL/state before and after; actual activation/traversal; observed focus target when relevant; unanswered observation; pass/fail/not observed; evidence reference; policy denials and observed effects. These fields are proposals for reviewability, not pre-existing schema obligations (`surface-contract.json:18-20`; planning protocol reference:23). The ledger can be prose/table inside a run record; no new serialized schema is required.

P7 — Keep acceptance of the document separate from website acceptance. Static source review plus the supplied validator can establish that the planned document covers the declared journey. Only an authorized later browser observation could determine current runtime behavior; do not claim current deployment passes or fails (`checks/check_contract.py:42-43`; `surface-contract.json:19-20`). Deliverable: explicitly separate “protocol coverage complete” from “browser behavior unobserved.”

## Measurable acceptance criteria for the planned protocol

| ID | Observable criterion | Source obligation / proposal |
|---|---|---|
| AC1 | States scope as entry URL `https://qaizen.io/labs`, locale `en-US`, viewport 1280×800, depth entry/state, unanswered; names sole allowed origin and all three allowed methods. | Contract lines 4-6; policy lines 2-4. |
| AC2 | Entry action uses the declared journey link and click, reaches introduction; Start uses “Start the check” and click, reaches first question. | Contract lines 9-10. |
| AC3 | From unanswered first question, summary Enter opens help, summary Space closes it, summary Enter reopens it; observations are recorded for each resulting state. | Contract lines 11-13; required `help-toggle` line 18. |
| AC4 | From help open, sequential Tab reaches Close, Enter closes help, and the focused element is the summary. The procedure does not replace this with a click or synthetic focus assignment. | Contract lines 14,17; checker lines 32-34. No synthetic focus is a proposed proof-integrity rule. |
| AC5 | From help closed after Close, sequential Tab reaches Back, Enter returns to introduction, and the focused element is its `h1`; actual keyboard activation and destination are observed separately. | Contract lines 15,17-18; checker lines 35-36. |
| AC6 | No answer is selected at any point. Explicitly check unanswered state after entering first question and before leaving it; do not submit, generate results, or proceed through the full questionnaire. | Contract lines 6,18,20. Check timing is proposed coverage. |
| AC7 | Origin and method policy applies before navigation and during the whole run; blocked analytics POST and its observed effects are retained as evidence. The protocol does not relax policy to obtain a passing journey. | Contract lines 5-6,18,20; policy lines 2-4. Enforcement detail/stop rule is proposed. |
| AC8 | Each of `entry`, `unanswered`, `help-toggle`, `close-focus`, `keyboard-back`, `introduction-focus`, `read-only-policy`, `origin-policy` has a procedure and a place for evidence/outcome, including an unobserved outcome. | Contract line 18; evidence fields are proposed. |
| AC9 | Includes no current-deployment pass/defect claim, retains fixture disclaimer, distinguishes expected from observed, and states no mobile/full questionnaire/performance/accessibility certification or website source redistribution. | Target line 3; contract lines 19-20. |
| AC10 | Local check is identified as contract consistency only, with command `python3 -B checks/check_contract.py surface-contract.json`; no local result is presented as browser evidence. | Checker lines 46-51,42-43. |

Checks for the later document change: trace every AC to the revised prose and each required-check ID to action plus observation; compare all seven transition tuples `(from,to,control,activation,traversal,focus_after)` against contract lines 9-15; run the existing checker; review provenance and limits for overclaims. A static checker pass alone cannot detect missing keyboard instructions in the Markdown because the script reads only the JSON input (`checks/check_contract.py:46-51`).

## Risks, triggers, severity, and impact

Severity describes consequence to this task's bounded outcome, not a measured website defect.

| Risk | Trigger and affected behavior | Severity | Evidence/check |
|---|---|---|---|
| False keyboard acceptance | Back is clicked, or focus is assigned directly before assertion; a journey can appear correct without proving keyboard access. | High | Target line 10 vs contract line 15. Review action/focus evidence separately. |
| Missing help-cycle coverage | Protocol closes only via Close, leaving Space toggle and Enter reopen unobserved. | Medium | Target lines 7-8 omit contract lines 12-13. Trace all seven transitions. |
| Scope escape | A request uses another origin or disallowed method, or an answer is selected/submitted. | High | Contract lines 5-6,20; policy lines 2-4. Require guards and denials ledger. |
| Misreported website status | Local validator pass or tutorial wording is treated as proof of live behavior. | High | Checker lines 42-43; contract line 19. Audit claims. |
| Guard affects journey | Expected analytics POST block changes observable state or functionality. | Medium, hypothesis until observed | Contract line 20 expects blocking and retention of effects; do not assume harmlessness or bypass. |
| Overbuilt delivery | Tooling or site repairs are made prerequisites for a protocol-only revision without evidence they are necessary. | Medium | Task lines 3-5; roles reference line 20. Keep implementation separate from documentation acceptance. |
| Unsupported DOM absence | Tutorial “absent” is interpreted as node removal rather than observed returned-introduction state. | Low | Target line 10 adds wording not expressed in contract lines 7,15,17. Clarify optional check. |

## Questions for peers and alternatives to challenge

Architecture: Can the existing three authority files plus a Markdown action/evidence table satisfy P2/P6 without adding a new schema, parser, or runner? If proposing new machinery, identify the concrete failure that a document change cannot address and the smallest test proving that need. Alternative: manual procedure plus existing validator. Also locate the actual host boundary that would enforce P5; do not infer a browser tool exists from supplied files.

Delivery: Can a single-document planned change with traceability review and the existing checker be the smallest deliverable, while live observation stays explicitly unperformed here? Challenge any task that broadens this into website remediation, mobile coverage, full questionnaire completion, or a prerequisite automation build. Alternative: stage documentation coverage first and separately authorize execution/tooling if required.

QA/security: Does the evidence ledger distinguish a policy-denied required resource from an assertion failure, and retain the blocked analytics POST effects without treating every expected denial as an automatic pass? Propose the least evidence needed to verify origin/method constraints and actual focus without recording unnecessary page content.

UX: Are “returned introduction visible” and focused introduction `h1` sufficient observations for the declared returned state, with question/help “not presented” as a secondary check? Please avoid assuming DOM removal or current focus behavior without browser evidence.

## Unfinished work and resolving evidence

No assigned independent-analysis item remains unfinished. Cross-examination and adjudication are intentionally pending the lead's report barrier. Browser behavior, suitable enforcement tooling, exact DOM selectors beyond declared control/focus references, and real policy-denial effects remain unknown. They require an authorized future bounded browser run and its evidence, not network retrieval or guesswork in this planning pass. No implementation was requested or performed.
