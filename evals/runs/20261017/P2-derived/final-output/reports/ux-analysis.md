# UX initial independent analysis

Status: COMPLETE for the bounded documentation analysis. No rendered observation performed or claimed.

Role: UX. Target: documentation-only clarification of `target/verification-protocol.md`. Enclosing snapshot `92981d42bbb636d2809b22af476c7974c1a1f54b539b8e5a7d6c9767b0d53b1d`; candidate snapshot `8b26119f383a7d5853c1bd2ab5f678e08966300846c0d6f2784351c1f5a59e8d` (identifiers supplied in task brief, not independently recomputed).

## Inspected sources and scope

Read all of `TASK.md`, `surface-contract.json`, `checks/check_contract.py`, `observation-policy.json`, and `target/verification-protocol.md`; inspected numbered source locations. Read the current `/workspace/output/evidence/profile-check.json` and planning method `references/roles.md` and `references/protocol.md`. No peer report or conclusion was consulted.

Uninspected: deployed website, DOM, browser focus behavior, network requests, private source, other locales/viewports, assistive technology behavior, loading/error screens, complete questionnaire. These are outside this documentation-only task; no browser or network was used. The tutorial's authorship disclaimer is explicit (`target/verification-protocol.md:3`). Source expectations cannot establish an observed website failure (`surface-contract.json:19`; `checks/check_contract.py:42-43`).

## Findings and proposed decisions

1. Preserve the existing journey and its strongest assertions. The target already requires sequential Close activation, summary focus after Close, an unanswered first question after closing help and immediately before departure, sequential Back within 24 steps, Enter activation, introduction visibility, absence of question/help, and introduction-heading focus (`target/verification-protocol.md:8-10`). These are valid existing obligations, not defects to rewrite. Preserve the fixture disclaimer. The 24-step bound belongs to the target, not the contract; retain it as a procedure bound without claiming the contract requires it.

2. Clarify the missing keyboard help sequence using the existing contract. Current step 3 says only “Open help using its summary control” (`target/verification-protocol.md:7`), which leaves activation ambiguous and omits the Space-close / Enter-reopen sequence. Required sequence is summary Enter -> help open, summary Space -> help closed, summary Enter -> help open (`surface-contract.json:11-13`), followed by the existing Close path. Add each activation and its immediate observable help state, preserving the separate Close action. This fulfills the `help-toggle` required check (`surface-contract.json:18`) while preserving all existing target assertions.

3. Keep the entry and Start controls concrete. Start from `https://qaizen.io/labs`, follow the journey anchor ending `/labs/readiness-check` with click, verify introduction, click “Start the check,” and verify the first question is present without selecting an answer (`surface-contract.json:4,9-10`). Do not replace this entry journey with direct navigation to the questionnaire: that would omit the entry transition. Keyboard-only navigation throughout the entire journey is not an existing requirement: entry and Start are explicitly click transitions. Avoid creating such a new obligation.

4. Preserve distinct focus destinations. After Close, verify help is closed and the question's summary is the focused element. After application Back, verify the introduction heading is focused and introduction is visible while question/help are absent. The destinations are separately declared (`surface-contract.json:14-17`) and separately guarded by the checker (`checks/check_contract.py:32-36`). Never treat focus on summary as a substitute for heading focus on return. Identify the heading in the returned introduction context, rather than treating any `h1` anywhere as sufficient.

5. Make keyboard evidence reviewable without changing the interaction. For Close and Back, record the starting focused element, each sequential Tab/Shift+Tab traversal (or an equivalent ordered event trace), the resolved application control, Enter activation, and the focused destination plus visible state afterward. Preserve the Back 24-step limit; define a step as one sequential Tab or Shift+Tab traversal, counting across both directions. Do not claim keyboard reachability from a screenshot, click, selector-only lookup, or programmatic focus. This is evidence guidance, not a proposal for new application behavior. The checker explicitly requires sequential Back traversal and observed activation (`checks/check_contract.py:35-36`). The target allows Tab or Shift+Tab for Close and Back; retain those valid target alternatives. The contract lists Tab for both transitions, and the checker explicitly accepts either for Back. Flag this precision difference for adjudication rather than silently tightening Close or removing Shift+Tab.

6. Add a short setup/evidence scope paragraph: en-US, 1280 x 800, unanswered, entry/state depth; allow only GET/HEAD/OPTIONS, keep allowed origin `https://qaizen.io`, and retain blocked analytics and their observed effects (`surface-contract.json:4-6,18,20`; `observation-policy.json:2-4`). The current profile also specifies blocking main-frame/popup navigation outside authorized origins. Do not invent a new all-resource same-origin requirement from that phrasing. This task documents the future procedure; it does not execute a journey or relax the policy to obtain a successful recording.

7. Recovery should describe evidence handling, not invented application UX. If a control is missing, a state cannot be observed, focus lands elsewhere, or the traversal bound is exhausted, retain the actual trace, mark that obligation failed or unverified as appropriate, and stop the dependent journey. Do not focus the destination or click Back to manufacture a passing keyboard result. If policy blocking changes rendering, retain that observation and the blocked request instead of relaxing policy (`surface-contract.json:20`). Distinguish a failed observed assertion from an unavailable observation. No source specifies loading UI, error copy, retry UI, or focus recovery behavior; do not add them as product requirements.

## Proposed interaction and evidence requirements

| Journey point | Required action / state | Evidence needed |
|---|---|---|
| Labs -> introduction | Click declared journey link; introduction visible | Entry/control and resulting introduction |
| Introduction -> question | Click Start; first question visible and unanswered | Start action, question state, no selection |
| Help open | Summary Enter; help open | Focused summary, key, resulting state |
| Help toggle closed | Summary Space; help closed | Key and resulting state |
| Help reopen | Summary Enter; help open | Key and resulting state |
| Close | Sequential traversal to Close; Enter; help closed and summary focused | Traversal and activation, resulting state and actual focused element; unanswered assertion retained |
| Back | Unanswered immediately before leaving; sequential traversal within 24 steps; Enter | Traversal count and activation, introduction visible, question/help absent, introduction heading focused |

For help visibility, describe a state assertion appropriate to the rendered control (for example expanded/collapsed state together with exposed content) without asserting an unobserved DOM implementation. The contract identifies `summary` but no deployed markup was inspected. Do not generalize this narrow focus/key coverage to an accessibility certification (`surface-contract.json:20`).

## Risks

| Trigger | Impact / severity | Basis and proposed mitigation |
|---|---|---|
| Maintainer executes existing ambiguous step 3 with mouse and omits Space/reopen | Required keyboard help-toggle coverage absent; high for acceptance reliability | Target line 7 versus contract lines 11-13,18. Spell out all three activations/states. No deployed defect inferred. |
| Maintainer checks only the returned page screenshot or focuses heading manually | False claim of keyboard reachability/focus behavior; high for acceptance reliability | Contract lines 14-17 and checker lines 32-36. Require sequential traversal, activation, and actual destination evidence. |
| Clarification deletes or merges repeated unanswered assertions | Journey can leave without proving unanswered invariant at required checkpoints; medium | Target lines 9-10. Preserve both checkpoints even if adjacent text seems repetitive. |
| 24-step exhaustion is treated as evidence of a deployed defect regardless of setup | Unsupported conclusion; medium | Bound exists only in target line 10; deployed behavior unobserved. Record setup, trace, count, and inability to complete; classify evidence precisely. |
| Policy blocked analytics causes visible disruption and recorder relaxes policy | Observation crosses scope and loses diagnostic evidence; high for policy compliance | Contract lines 6,20. Preserve blocking and observed effects. |
| New loading, mobile, localization, or accessibility requirements are invented | Scope expansion without authority; medium | Contract lines 6,20. Record unknowns rather than inventing app behavior. |

Severity is this role's assessment of impact on verification reliability and scope, not a measured product risk rating.

## Named peer questions and alternatives

Architecture: Can one short setup paragraph and a single expanded help sequence carry the necessary policy and state detail without adding a framework, new schema, browser harness, or application changes? Please trace the document/checker boundary: the checker validates contract consistency and cannot verify the procedure's keyboard execution. For Close traversal, should we explicitly annotate the contract's Tab example versus the target's Tab-or-Shift+Tab alternative, or preserve target wording and leave contract wording untouched? My preference is preserve the target alternative and avoid unnecessary runtime/schema work.

QA and security: Will the proposed evidence matrix distinguish each of Enter-open, Space-close, Enter-reopen, Close focus return, and Back heading focus instead of allowing a single “help works” result? What minimal observation record proves the question is unanswered at both retained checkpoints without selecting anything? Can we preserve the 24-step bound while making a bounded incomplete trace distinguishable from a current website failure? Please challenge whether event/focus trace guidance needs more precision or can remain tool-independent.

Alternative rejected provisionally: rewrite the whole journey as keyboard-only. It would add unsupported requirements at entry and Start (contract explicitly requests click), while the actual documentation omission is the help keyboard sequence. Alternative rejected: regard a passing contract checker as browser verification; checker itself disclaims that inference.

## Deliverables and unfinished evidence

Deliverable proposed: a small documentation-only patch to the protocol adding setup/scope, explicit help key sequence and observations, and evidence/recovery guidance while preserving every valid target assertion. Supporting acceptance mapping should tie every changed clause to the source locations above; no changes to contract, checker, policy, app, or skill are needed.

This initial report is complete within the assigned scope. Unfinished work: peer cross-examination and lead adjudication, especially Close traversal wording and the smallest useful evidence format; no patch has been authored by this role. Current browser behavior, exact unanswered-state representation, actual tab sequence, DOM heading identity, and analytics effects remain deliberately unmeasured. Only a separately authorized, policy-constrained observation could resolve those empirical unknowns; they do not block planning this documentation clarification.
