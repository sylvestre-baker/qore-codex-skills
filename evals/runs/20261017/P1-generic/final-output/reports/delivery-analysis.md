# Delivery independent analysis

Role: Delivery. Phase: Workflow Analyze (independent; no peer reports read).
Target: `/workspace/worker/target/verification-protocol.md`.
Supplied snapshot: `0aa277436d8dcda4d6c2412c6ad4307dd0192b0f6230fa96c8b16d99c8bac194` (provided identifier; not independently recomputed).

## Sources and boundaries

Inspected in full: `TASK.md:1-5`; `surface-contract.json:1-21`; `checks/check_contract.py:1-54`; `observation-policy.json:1-5`; `target/verification-protocol.md:1-10`; `.agents/skills/qore-plan/SKILL.md`; `.agents/skills/qore-plan/references/protocol.md`; `.agents/skills/qore-plan/references/roles.md`. A local file search found no `AGENTS.md`.

Uninspected: no live site, deployment, browser state, private website source, peer reports, or external resources. No browser harness, automation package, or installed-browser inventory was supplied or inspected. Other skill references are for the lead's synthesis and were not independently audited here. No claim is made about deployment behavior.

Authority: the three original project sources govern the change (`TASK.md:3-5`). The target is a reconstructed fixture (`target/verification-protocol.md:3`), not evidence of a historical defect. Expected transitions are declared obligations, not deployment observations (`surface-contract.json:19`). This task authorizes a plan only; source files stay immutable and reports go outside the input (`TASK.md:5`).

## Decisions and initial deliverables

D1 — Plan one bounded document change, with a traceability/evidence checklist in that document. Do not add a browser harness, modify the contract/checker, fix the website, or add CI as a prerequisite. These are proposals for scope control, supported by the requested target and planning-only outcome (`TASK.md:3-5`), not prohibitions on future separately authorized work.

D2 — Replace the incomplete interaction procedure with the exact seven-transition sequence. Entry and Start use click; summary opens with Enter, closes with Space, reopens with Enter; Close is reached with Tab and activated with Enter; Back is reached with Tab and activated with Enter (`surface-contract.json:9-15`). Explicitly establish focus on summary by sequential keyboard navigation before activating it. The target currently omits the Space/reopen sequence, leaves summary activation unspecified, and clicks Back (`target/verification-protocol.md:7-10`). The required keyboard proof must record genuine traversal and activation, not just a final URL/state or programmatic focus. Keep the distinct focus assertions after Close and Back (`surface-contract.json:14-17`; `checks/check_contract.py:32-36`).

D3 — Use Tab for Close and Back in the primary procedure. Although the checker accepts Tab or Shift+Tab for Back (`checks/check_contract.py:35`), the supplied transition specifies Tab (`surface-contract.json:15`), so the broader checker must not weaken this target. The target's existing Tab-or-Shift+Tab Close wording (`target/verification-protocol.md:8`) should become the exact contract traversal. Alternative reverse traversal can be supplemental, not a substitute for the declared sequence.

D4 — Put observation constraints before any future navigation: en-US, 1280×800, entry/state depth, unanswered state, exact permitted origin, and GET/HEAD/OPTIONS only (`surface-contract.json:4-6`; `observation-policy.json:2-4`). Propose a pre-navigation gate demonstrating enforceable origin and method restrictions for all browser requests/redirects and recording denied requests. Tool-specific enforcement is unresolved because no harness was supplied. Inability to enforce a required boundary blocks live execution; it does not authorize widening the boundary. Analytics POST remains blocked and observed effects retained (`surface-contract.json:20`). This is a future execution prerequisite, not permission to navigate now.

D5 — Separate evidence levels and pass criteria. A local checker pass establishes JSON consistency only (`checks/check_contract.py:42-43`). A source review establishes coverage of the revised protocol. Neither establishes current website conformance. Future browser evidence must identify action, state before/after, active element at the two focus checkpoints, unanswered assertion, and blocked-request effects. This evidence schema is proposed implementation detail, derived from required checks (`surface-contract.json:18`) rather than a claim that it already exists.

D6 — Preserve the fixture/provenance distinction and explicit exclusions. No answers, results, submissions, website source redistribution, mobile/full-questionnaire/performance/accessibility certification, or deployment identification from private commits (`surface-contract.json:19-20`). The existing target assertion that question/help are absent after Back (`target/verification-protocol.md:10`) is not explicitly required by the original contract. Treat that assertion as a proposed supplemental check, or replace it with the required returned-introduction state and heading focus. Do not silently elevate it to project authority.

## Work breakdown and size basis

Estimates below are delivery proposals, not measured duration or a promise. One document of ten current lines, seven declared transitions, eight required check labels, two compact policies, and one 54-line local validator bound the work. There is no supplied application implementation to change.

| ID | Task and concrete deliverable | Effort | Dependencies | Completion check |
| --- | --- | --- | --- | --- |
| T1 | Source-to-protocol coverage ledger: authority, all seven transitions, eight required checks, environment, limits, and provenance | 20–30 min | None | Each obligation has a source location and planned protocol section |
| T2 | Draft constraints/setup section and future enforcement gate, including blocked analytics evidence and inability-to-enforce outcome | 20–35 min | T1 | All origin/method/scope requirements precede navigation; unknown harness remains explicit |
| T3 | Rewrite ordered keyboard/state procedure and observable checkpoints | 25–40 min | T1 | Seven transitions in contract order; exact controls/keys, focus destinations, unanswered state |
| T4 | Add evidence template and distinguish local structural validation from future observed browser results | 15–25 min | T2, T3 | Eight checks trace to evidence; no browser-pass claim without observations |
| T5 | Independent source comparison and local validator check; resolve review differences | 15–25 min | T4 | No checker-only inference; no conflicting traversal or missing limits |

Total prospective document implementation/review: approximately 95–155 minutes (about 1.5–2.6 person-hours). This excludes the present multi-role planning process and any browser/tool discovery or live observation. Review availability may add elapsed time; no calendar date is supportable from supplied resources.

Dependency graph: `T1 → {T2, T3} → T4 → T5`. With a single editor all work is sequential; the graph only identifies logically independent drafting sections. With two available contributors the longest estimated path is T1 → T3 → T4 → T5, 75–120 minutes plus handoff. No multi-person staffing is assumed.

Initial scope: all T1–T5 and the revised document are one coherent change. Dropping request boundaries, keyboard traversal proof, help toggle/reopen, focus checks, or evidence limitations would leave the outcome incomplete. Future scope: browser harness selection, browser execution, remediation of actual website failures, CI integration, and any broader accessibility or device work. Future execution is not required for plan completion and must not be represented as completed by this work.

## Acceptance and definition of done

For the proposed document change:

1. A reviewer can map all transition IDs and all eight required checks (`surface-contract.json:9-18`) to explicit steps and evidence fields.
2. The only prescribed primary Back activation is sequential Tab traversal followed by Enter; final heading focus is checked separately. Close similarly restores summary focus. Opening help alone or ending on the right page cannot count as keyboard coverage.
3. Enter/Space/Enter on the summary and the state after each action are explicit. The first question remains unanswered through the bounded journey.
4. Locale, viewport, origin and method gates precede navigation. A blocked analytics POST is expected and its observed effects retained. Cross-origin redirects/requests and unsafe methods cannot be exempted merely to make the journey succeed.
5. Current observed behavior is marked unknown until observed; the 2026-10-15 baseline and 2026-10-16 protocol gap are not recast as a website defect (`surface-contract.json:19`).
6. The checker command and its limited interpretation are stated. Source coverage review—not the checker alone—confirms the Markdown covers obligations. No additional test framework is necessary for a document-only edit.
7. Limits and out-of-scope work are explicit. The fixture notice remains accurate. Any supplemental absent-question/help assertion is identified separately from required returned-introduction/heading-focus checks.
8. The user receives a sourced plan, tasks, unresolved execution dependencies, and verification boundaries. Source implementation remains unperformed under this request.

For a later browser execution, use a separate readiness decision: select a harness capable of enforced request boundaries and genuine keyboard observation; demonstrate restrictions before initial navigation; execute and retain actual evidence. Report unmet criteria as failures or unavailable observations, never as presumed passes. This readiness dependency does not block this documentation plan.

## Risks, triggers, impact, and controls

| Risk | Trigger and evidence | Impact severity | Control/check |
| --- | --- | --- | --- |
| False keyboard pass | Click Back or directly focus the destination and assert the final page; target currently clicks (`target/verification-protocol.md:10`) | High: required keyboard evidence absent | Separate actual sequential traversal, Enter activation, state transition, and final focus evidence |
| Policy breached during observation | Origin/method filtering missing or installed after navigation; boundaries at `surface-contract.json:5-6`, `observation-policy.json:2-4` | High: unauthorized request can occur | Future pre-navigation enforcement gate; no execution if enforcement unavailable |
| Blocked analytics mistaken for irrelevant noise or reason to relax policy | Expected blocked POST has UI effects (`surface-contract.json:20`) | Medium: misleading usability/conformance conclusion, or high if POST allowed | Retain blocked event and observed effects; keep restriction |
| Checker mistaken for website/protocol proof | JSON validation passes but Markdown or site is untested (`checks/check_contract.py:42-43`) | High: unsupported completion assertion | Separate consistency, coverage review, browser evidence statuses |
| Exact contract weakened by permissive checker | Shift+Tab substituted for declared Tab based solely on checker (`surface-contract.json:14-15`; `checks/check_contract.py:35`) | Medium: procedure does not match declared path | Use exact primary sequence; label variants supplemental |
| Scope expands into app/harness implementation | New tool/code/website remediation made necessary for document delivery without authority (`TASK.md:3-5`) | Medium: schedule/authorization failure | Bound initial change to documentation and name future prerequisites |
| Unobserved current UI differs | Current deployment fails expected path, changes controls, or behaves differently from baseline; explicit uncertainty in `surface-contract.json:19` | Medium: later observation cannot complete as planned | Record failure and stop unsupported inference; no claim of a known website defect now |
| Unsupported extra gate | Treat absent question/help after Back as a required contract invariant solely because target said so (`target/verification-protocol.md:10`) | Medium: unnecessary acceptance failure | Separate proposed supplemental assertion from authoritative obligations |

Severity is a planning assessment, not an observed incident classification.

## Rollout and rollback

No website rollout, deployment, migration, or external publication is part of this plan. For a later authorized document edit, review the diff against the source-to-protocol ledger and replace the target through the project's normal version-control process if present (repository workflow is uninspected). Rollback means restoring the previous document revision if the new wording introduces contradictions, while explicitly recording that the old version retains a keyboard evidence gap. Rollback is not evidence of conformance. No live interaction or application rollback is needed for this planning deliverable.

## Questions and challenges for named peers

Product: Is the smallest useful version the complete seven-transition documentation change, or are you proposing to defer any of help Space/reopen, Back keyboard proof, request gates, or focus evidence? Those are already declared obligations (`surface-contract.json:11-18`); dropping them would not satisfy the requested source conformance. Do not turn supplementary absent-question/help assertions into new release gates without distinguishing proposal from source.

Architecture: Does your design require new automation code or a reusable runner before this document can be delivered? Please identify the actual supplied reusable component and interface if so; the available project files expose no application/harness contract. Keep tool-specific enforcement feasibility as a future readiness dependency unless you can supply evidence. How will you prevent requests before interception and account for redirects and secondary requests without inventing current harness capability?

QA and security: Can your coverage matrix keep contract consistency, document coverage, and live browser pass/fail separate? Does the future boundary gate include all requests before initial navigation and retain blocked analytics effects? The local checker validates neither enforcement nor browser behavior.

UX: Does the step sequence preserve the focus starting points necessary for Tab proof after Close, and avoid using programmatic focus as the traversal evidence? Are any absent-state assertions beyond `surface-contract.json:7,15,17` being proposed as supplemental criteria?

## Alternatives considered

A. Minimal edit replacing only Click Back with Tab/Enter: rejected as insufficient because summary Enter/Space/Enter and policy/evidence prerequisites remain unspecified.

B. Full browser harness/CI implementation: defer. It may benefit future repeatable execution, but no tooling source exists here and this request is a plan for one document.

C. Broad keyboard exploration with Tab or Shift+Tab interchangeably: useful supplemental exploratory coverage, but primary protocol should match the supplied transition values.

D. Include a complete proposed replacement document inside the final plan: optional presentation choice, not required by this role. If used, label it a proposed artifact and preserve authority/evidence boundaries.

## Local verification performed

Environment: supplied `/workspace/worker`, shell `sh`, no network access or mutations. Command: `python3 -B checks/check_contract.py surface-contract.json`. Result: exit 0, JSON `valid: true`, schema `qaizen-labs-surface/1`, eight required checks listed, and limit `Contract consistency only; browser observations establish current behavior.` This is an observed local consistency result only. `-B` avoids Python bytecode writes.

`rg` was unavailable; file discovery used `find` and source reads used `cat`/`nl`. No supplied file was edited.

## Unfinished work and resolving evidence

Independent Delivery analysis is complete within the assigned deadline. Cross-examination is intentionally pending the lead's report barrier; no peer conclusions were inspected. Lead adjudication, combined specification, and skill artifact lint are not this report's delegated deliverables. Current browser behavior, harness availability, enforcement feasibility, deployment identity, and actual execution duration remain unknown; only future authorized tool inspection and controlled browser observations can resolve them. These unknowns do not prevent a sourced document-change plan.
