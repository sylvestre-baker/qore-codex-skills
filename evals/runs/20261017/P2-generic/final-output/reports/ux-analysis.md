# UX independent analysis — Workflow initial pass

Role: UX. Actual context name: `/root/ux`. Target snapshot supplied by lead: `e9aeec2eee10b52c3339b53b4e491d3ff69f57c68be2f5ea1d61e70df55acccc`. This report plans a documentation-only clarification; it does not modify inputs or assert deployment behavior.

Identity clarification: the supplied identifier is the enclosing entire frozen prepared-input manifest, not a standalone target-file digest. First clock observation: `2026-10-17 11:42:38 UTC`. Report completed: `2026-10-17 11:43:31 UTC`; administrative identity/timing addendum recorded immediately afterward, before return.

## Inspected sources and limits

- `TASK.md:3-5`: maintainers are the audience; clarify only the supplied procedure; preserve valid obligations; source project requirements from the three specified project inputs; output outside input folder.
- `target/verification-protocol.md:1-10`: actual existing procedure, including tutorial provenance at line 3, keyboard Close/focus at line 8, unanswered check at line 9, and an already explicit sequential-keyboard Back action, 24-step bound, return visibility, absence and heading-focus assertions at line 10.
- `surface-contract.json:4-20`: origin, scope, states, all seven transitions, focus destinations, checks, provenance and limits.
- `checks/check_contract.py:9-43`: validation boundary; particularly distinct Close/Back focus at lines 32-36 and the explicit distinction between consistency and browser proof at lines 42-43.
- `observation-policy.json:2-4`: permitted origin.
- `.agents/skills/qore-plan/references/protocol.md`: independent analysis, report barrier, bounded challenge and evidence discipline.
- `.agents/skills/qore-plan/references/roles.md`: UX lens and required Architecture/QA challenge links.

Uninspected: website, browser behavior, private code, history, other projects, other role reports, deployment identity and broader skill resources. No network used. No accessibility certification or actual website defect inferred. The provided snapshot identifier is a task identifier, not a claim about a website deployment.

## Evidence and expectations

Observed document fact: the supplied target already tests Back with Tab or Shift+Tab and Enter, and already asserts introduction-heading focus (`target/verification-protocol.md:10`). There is no basis to describe the current supplied target as lacking keyboard Back or to replace it with a direct-focus shortcut. Its description as a newly authored fixture must remain (line 3).

Observed documentation omission: target line 7 leaves the help opening activation unspecified and contains no Space close/reopen sequence. The contract explicitly requires Enter → Space → Enter for open-help, toggle-help and reopen-help (`surface-contract.json:11-13`). This is a coverage gap in text, not evidence of broken help behavior.

Observed documentation omission: the target does not spell out scope, origin and method controls. These are valid project obligations (`surface-contract.json:4-6,18,20`; `observation-policy.json:2-4`).

Measurement: from `/workspace/worker`, ran `python3 -B checks/check_contract.py surface-contract.json`; exit 0, `valid: true`, eight listed checks, result explicitly limited to contract consistency. Environment: supplied local shell, no network; stdout captured in tool result for this analysis. This validates the input contract, not the target procedure or current site.

## State and interaction requirements

| Phase/state | Maintainer action and expected evidence | Authority |
|---|---|---|
| Labs → introduction | At the allowed entry URL, click the readiness-check link; observe introduction. | contract lines 4,9 |
| introduction → first-question | Click “Start the check”; record question visible and no answer selected. | contract lines 6,10,18; existing target lines 6,9 |
| first-question → help-open | Reach summary without choosing an answer, activate Enter, observe help open. | contract line 11 |
| help-open → help-closed | Activate the summary with Space; observe help closed. | contract line 12 |
| help-closed → help-open | Activate summary with Enter; observe reopened help. | contract line 13 |
| help-open → help-closed | Sequential keyboard traversal to Close, Enter; help closed and actual focus on summary. | contract lines 14,17; target line 8 |
| help-closed → returned-introduction | Check unanswered immediately before departure; sequential traversal to Back within the existing 24-step guard, Enter; introduction visible, question/help absent, focus on introduction h1. | contract lines 15,17; target line 10 |

The unanswered invariant applies throughout this bounded journey, including immediately before Back. Do not answer to reach a later state. Preserve the valid distinct focus expectations: Close returns to summary; Back returns to introduction heading. Assertions about visibility must not substitute for observing actual focus.

Use Tab for the canonical contract route for Close and Back (`surface-contract.json:14-15`). The existing procedure's Shift+Tab alternative is sequential keyboard traversal; the checker explicitly permits it for Back (`checks/check_contract.py:35-36`). Retain that existing Back alternative with transparent wording, rather than label it invalid. Architecture/QA should adjudicate whether Close's existing Shift+Tab wording remains an explicitly labeled supplemental route or needs exact canonical wording; do not silently weaken Tab coverage.

## Proposed documentation decisions and deliverables

1. Preserve the tutorial provenance statement and existing Close, unanswered, keyboard Back, return-visibility, absence and heading-focus assertions. Any rewrite should map these old obligations to the new procedure. Justification: target lines 3,8-10 already contain valid safeguards.
2. Expand help step into explicit Enter-open, Space-close and Enter-reopen assertions, then perform existing Close sequence. Justification: contract lines 11-14 require distinct transitions; generic “open help” omits observability of two required states.
3. Add a concise setup block: en-US, 1280 × 800, public entry URL, allowed origin exactly https://qaizen.io, read-only GET/HEAD/OPTIONS, no answer selection or submission/results. Explain blocked analytics POST is expected and record its visible effects. Justification: contract lines 4-6,18,20 and observation policy lines 2-4.
4. Preserve the 24-step Back traversal bound as the procedure's operational stopping guard. It is present in the target but not mandated by the project contract; do not misrepresent its provenance as product behavior, a maximum permissible focus order, or proof of accessibility failure. If exhausted, record last focused element/state and inability to complete this run; do not force-focus Back to manufacture a pass. This is a proposed clarification, not an observation of any current failure.
5. Require concise per-transition expected/observed records, actual activated control, activation key, and focus destination at the two focus assertions. Label untested transitions untested. Avoid claiming a site pass from the local checker. Justification: contract provenance line 19 and checker lines 42-43.
6. Keep documentation restricted to this path. Do not add mobile, performance, completed questionnaire, broad accessibility certification, application fixes, or source distribution. Contract line 20 expressly excludes these scopes.

Deliverables for the lead: a proposed documentation change specification, an obligation-preservation map, and acceptance checks covering these seven transition rows. This report does not authorize modifying original input files.

## Content, accessibility, localization, and recovery

Use exact control labels and identify summary and h1 as contract targets, avoiding claims that current wording or markup was observed. Content should clearly separate procedure instructions, expected outcomes and recorded outcomes. English-US and fixed viewport are run conditions, not an instruction to implement localization.

Keyboard observability is specifically required. Do not use programmatic focus or a pointer click as evidence of successful sequential keyboard traversal for Close/Back. Pointer clicks remain the declared activation for entry/start. No screen-reader, contrast or full WCAG claim follows from this limited path.

If a control is missing, cannot receive sequential focus, a state does not appear, an origin boundary would be crossed, or an unanswered invariant is lost, stop the affected sequence and record what happened. These are proposed reporting rules for hypothetical run conditions, not claims that those conditions currently exist. Do not attempt recovery by answering, submitting, navigating outside policy, or changing the application. Loading/empty/error UI is unobserved; document inability to reach an expected state without inventing such screens or expected copy.

## Risks

| Severity | Trigger and affected behavior | Evidence or status |
|---|---|---|
| Medium | Clarification treats existing Back proof as absent and removes return-state/focus assertions. Maintainers would lose valid coverage. | Actual target line 10 already contains these requirements. |
| Medium | Generic help opening remains unchanged. Space-toggle and reopen acceptance remain unexercised by the written procedure. | Target line 7 versus contract lines 11-13. |
| Medium | A later run uses a forced focus jump to satisfy the 24-step guard. The recorded Back success would not prove traversal. | Explicit hypothesis; target line 10 and checker lines 35-36 define the route. |
| Medium | A later run interprets blocked analytics as irrelevant and omits effects. Maintainers lose contextual evidence of the actual observed journey. | Contract line 20 requires retention; no effects observed here. |
| Low | Step limit interpreted as product accessibility criterion. A long focus order may be mislabeled a site defect without evidence. | Explicit hypothesis; bound appears only in target line 10. |
| Medium | Local consistency success is presented as current deployment success. | Checker lines 42-43 explicitly limit its result; no browser run performed. |

## Alternatives

- Minimal edit: add explicit help keys and a setup paragraph, preserving all remaining target text. Smallest useful change, but may leave evidence and 24-step status ambiguous.
- Structured procedure plus compact expected/observed checklist: recommended if still concise; makes state and focus evidence reviewable and preserves old assertions visibly.
- Expand to full accessibility audit or implement runtime fixes: rejected as outside the user's documentation scope and unsupported by current evidence.

## Questions for named peers

Architecture: Can the final document distinguish the canonical contract Tab traversal from the supplied procedure's valid Shift+Tab alternative without creating a new product requirement? Please resolve Close's alternative separately from Back, since the checker only explicitly validates Back traversal.

Architecture: Where should the origin/method guard be stated so maintainers can apply it before interaction, while avoiding an invented browser automation or request-filter implementation? No such implementation is supplied.

QA and security: Does your matrix explicitly exercise Enter-open, Space-close, Enter-reopen, Close-focus and Back-heading-focus separately, including the existing unanswered-before-leave and returned-state absence assertions? Please challenge any claimed equivalence.

QA and security: What minimal recorded evidence distinguishes guard exhaustion or unavailable controls from an observed failed acceptance condition, and prevents unperformed steps being marked passed? Please keep this scoped to documentation, without prescribing unsupported storage machinery.

## Unfinished work

Cross-examination is pending the report barrier. Peer answers may adjust traversal wording and evidence requirements. No website run is required or performed by this planning analysis; actual behavior remains unknown. Final consolidated specification, change acceptance, and adjudication belong to the lead. All assigned independent UX analysis is otherwise complete within the deadline.
