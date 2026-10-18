# Independent QA and security analysis

Status: COMPLETE initial analysis; cross-examination not yet performed. Role: QA and security. Workflow deciding artifact: target/verification-protocol.md, an existing applicable procedure. Snapshot: enclosing manifest 92981d42bbb636d2809b22af476c7974c1a1f54b539b8e5a7d6c9767b0d53b1d; candidate 8b26119f383a7d5853c1bd2ab5f678e08966300846c0d6f2784351c1f5a59e8d, as supplied in the assignment. These identifiers are not deployment identifiers.

## Inspected sources and limits

Read TASK.md in full; surface-contract.json lines 1–21; observation-policy.json in full (allowed_origins); target/verification-protocol.md lines 1–10; checks/check_contract.py lines 1–54; skill SKILL.md, references/roles.md and protocol.md in full; fresh /workspace/output/evidence/profile-check.json and original references/project.json. No peer reports inspected. No network/browser or input modification performed. Did not inspect application implementation, deployment, private commits, or actual browser behavior; those are outside the authorized task. No assertion below describes an observed website defect.

Measurement: from /workspace/worker, ran `python3 -B checks/check_contract.py surface-contract.json`; exit 0, valid true, all eight named required_checks returned, explicit limit “Contract consistency only; browser observations establish current behavior.” This independently confirms only the current contract consistency. The checker checks declared method names, entry origin, selected focus/traversal fields and check IDs; it neither intercepts requests nor exercises any control (checker lines 12–18, 32–43).

## Proposed decisions and deliverables

1. Preserve fixture steps 4–6: Close sequential traversal and Enter, closed help and summary focus, unanswered assertions including immediately before leaving, and Back sequential traversal within 24 steps with Enter, introduction visible, question/help absent, introduction heading focused (target lines 8–10). These already express valid obligations. Do not call Back keyboard proof missing or substitute click/programmatic focus. Retain the fixture’s 24-step bound as a procedure limit, not a new universal accessibility claim. Contract allows Tab or Shift+Tab via checker lines 35–36 even though this instance declares Tab.
2. Clarify step 3 into the declared Enter → Space → Enter help sequence with observed open → closed → open states (contract lines 11–13). This exposes all help-toggle transitions before Close. Existing “Open help using its summary control” does not specify its activation or exercise Space/reopen. This is a procedure coverage gap, not a current deployment defect.
3. Add a compact preconditions/policy paragraph before opening the entry: en-US, 1280×800, exact entry URL and approved origin; remain unanswered; permit only GET/HEAD/OPTIONS requests; enforce navigation boundaries before the initial navigation, including popup/main-frame destinations and redirects; record blocked analytics and their effects without relaxing policy. Sources: contract lines 4–6, 18–20; observation-policy.json; fresh original project invariant unanswered-scope. Clarify policy at the request/navigation boundary without prescribing an unverified browser implementation. Do not expand the navigation-only origin invariant into a categorical ban on every third-party subresource without evidence.
4. Add evidence and verdict requirements: record transition/action, relevant before/after visible state and actual active element, traversal direction/count for Back, unanswered state immediately before Back, request block record, permitted navigation destinations and any blocked analytics effects. A screenshot of an introduction or a successful contract check cannot prove keyboard reachability/focus. Keep “expected,” “observed,” “failed” and “not observed/blocked” distinct. Record interrupted execution as incomplete observation, not a pass. Runtime evidence is a future execution deliverable, not a requirement to browse for this planning task.
5. Preserve fixture provenance and bounded scope: target line 3 and contract lines 19–20 explicitly distinguish acceptance from deployment proof. Do not claim source-code provenance identifies deployment, mobile coverage, full questionnaire coverage, performance or accessibility certification. No new harness, checker change, application change or website-source capture is needed for this documentation-only clarification.

## Test matrix for a future authorized observation

| ID / source | Action or boundary | Expected observable proof | Current evidence / clarification |
|---|---|---|---|
| entry; contract 4,9 | Open https://qaizen.io/labs and click journey link | Labs then introduction; each main-frame destination has allowed origin | Written instruction exists; exact URL/policy absent in fixture |
| start/unanswered; contract 6,10; fixture 6 | Click Start the check without answering | First question visible; no selected answer | Written instruction exists; deployment unobserved |
| help-toggle; contract 11–13 | Summary Enter, Space, Enter | Help open, closed, open in order; no answer selected | Enter/Space/reopen sequence absent in fixture |
| close-focus; contract 14,17; fixture 8 | Sequential Tab/Shift+Tab to Close, Enter | Help closed and document active element is summary | Already required; preserve separately from Back |
| unanswered; fixture 9–10 | Inspect first question after Close and before Back | Remains unanswered both times | Already required; preserve both checkpoints |
| keyboard-back; contract 15; fixture 10 | Sequentially reach Back within 24 steps, Enter | Record actual traversal and activation; no forced focus/click substitute | Already explicit; add evidence fields only |
| introduction-focus; contract 15,17; fixture 10 | Observe immediately after Back | Introduction visible, question/help absent, active element introduction h1 | Already explicit; preserve full conjunction |
| read-only-policy; contract 6,18,20 | Inspect boundary policy and blocked requests across all steps | No non-GET/HEAD/OPTIONS request sent; analytics POST blocked, effects retained | Declaration/checker is not enforcement; add preconditions/evidence |
| origin-policy; contract 5,18; observation-policy | Check initial, redirected and popup main-frame navigation | Only https://qaizen.io permitted; outside destinations blocked before navigation | Current fixture omits policy; add boundary statement |
| partial observation; checker 43; contract 19 | A step cannot execute or effects interrupt journey | Mark unobserved requirements/incomplete run, retain context | Proposed verdict clarification, not assertion of failure |

## Meaningful edge-case Gherkin

These scenarios specify future evidence and unsafe shortcuts to reject. They do not request current browser execution or new application behavior.

```gherkin
Feature: Bounded, evidenced journey verification

  Scenario: Space help closure does not replace Close focus proof
    Given the first question is unanswered and help was opened with summary Enter
    When summary Space closes help
    And summary Enter reopens help
    And the observer reaches Close sequentially and presses Enter
    Then help is closed and the actual focused element is the summary
    And the first question remains unanswered
    And the help toggle sequence and Close focus result are recorded separately

  Scenario: Introduction visibility without heading focus is insufficient
    Given help was closed through Close and summary focus was observed
    And the question is still unanswered immediately before leaving
    When Back is reached by sequential Tab or Shift+Tab within 24 steps and activated with Enter
    And the introduction becomes visible but focus remains elsewhere
    Then introduction visibility is recorded as observed
    And the introduction-focus obligation is recorded as failed
    And the combined Back verification is not recorded as passed

  Scenario: Back is not reached within the procedure bound
    Given the first question is unanswered and help is closed
    When 24 sequential traversal steps do not reach Back
    Then the bound and last focused element are recorded
    And Back keyboard reachability is not recorded as passed
    And a click or forced focus is not substituted to claim that proof
    And the introduction transition and focus remain unobserved in that run

  Scenario: Analytics write is blocked during the journey
    Given the request policy is active before entry navigation
    When analytics attempts a POST
    Then that request is blocked
    And its attempted destination, method and observable journey effects are retained
    And the policy remains active
    And any steps prevented by those effects are recorded as unobserved

  Scenario: An allowed link redirects outside the authorized origin
    Given main-frame and popup navigation allow only https://qaizen.io
    When navigation from an allowed page attempts an outside-origin redirect or popup
    Then the unauthorized navigation is blocked before arrival
    And the attempted destination and affected journey step are recorded
    And a successful contract consistency check does not turn that interrupted run into a journey pass
```

## Risks with triggers and severity

- HIGH, evidence-integrity risk: if a maintainer treats checker success or introduction visibility as proof of the complete keyboard journey, keyboard/focus requirements may be reported passed without observation. Source: checker lines 42–43; fixture line 10. This is a risk hypothesis, not evidence it happened. Mitigate with per-obligation evidence/verdict fields.
- HIGH, boundary risk: if future observation begins before policy enforcement, an analytics POST or outside-origin navigation may proceed. Sources: contract lines 5–6, 20 and profile unanswered-scope invariant. Current fixture omits policy setup. Mitigate with pre-entry guards and retained blocked-effects evidence. Actual interception coverage is unknown.
- MEDIUM, coverage risk: if step 3 is accepted as full help-toggle coverage, Space closure and Enter reopening remain untested. Source: contract lines 11–13 versus fixture line 7. Mitigate with explicit three-transition sequence.
- MEDIUM, scope regression: if a rewrite removes the redundant-looking unanswered checkpoint, Back postconditions, Close focus destination, or 24-step bound, valid fixture obligations are weakened. Source: fixture lines 8–10. Mitigate with a line-by-line preservation checklist.
- LOW, overreach risk: treating origin policy as a ban on all cross-origin resources or requesting a new browser harness grows scope without raw-source support. Source: project.json unanswered-scope specifies main-frame/popup navigation; TASK.md requests documentation only. Keep implementation choices and new boundary claims out of this change.

## Named peer challenges and alternatives

- Product: identify the observable acceptance delta after preserving existing Back and Close requirements. Reject a “fix keyboard Back” story that implies those words are absent. Alternative: clarify proof/evidence and complete the help sequence.
- Architecture: where exactly does proposed origin enforcement apply—requests, redirects, main-frame, popups, or every resource? Supply a raw-source reason for each added boundary. Alternative: state policy requirements without inventing a harness or claiming runtime coverage.
- UX: how is actual focus distinguished from visible heading, and how will Enter/Space/reopen be observed individually? Preserve separate Close/Back destinations. Alternative: record active element and visible state beside each transition.
- Delivery: does done mean a reviewable documentation plan or an observed website pass? Separate offline validation from later authorized browser evidence and do not add new runtime implementation tasks.

## Unfinished work / evidence needed

Cross-examination and lead adjudication remain pending; no peer conclusions have been consumed. The final proposed documentation wording must be checked against this preservation matrix. Actual deployment behavior, request interception coverage, response to blocked analytics and focus results remain unobserved; only a separately authorized controlled browser run could resolve them. Current planning can complete while clearly labeling those facts unknown. No blocker to producing a documentation-only clarification plan is established.
