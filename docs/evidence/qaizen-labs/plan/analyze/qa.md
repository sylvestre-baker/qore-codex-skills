# QA and security — independent Analyze report

## Snapshot and scope

Workflow mode applies because the frozen `examples/qaizen-labs/verification-spec.md:1-18` is an applicable existing specification for correcting the public verification protocol. Its own status is provisional. The known issue is insufficient keyboard proof, not a measured website defect (`verification-spec.md:8,109`). This report strengthens that correction and does not propose a replacement product.

Target snapshot: `qore-target-snapshot/1`, SHA-256 `1461fc149209fa29adc067a2b8f3c644055228aa0a2f45485779e3a418f47fd6`; candidate manifest `0540496cea29da71f72046f36a12c3a23b4d71900c97f7193f4dba699836b036`. I recomputed each of the nine recorded file digests and all matched `methods/planning-input.json`. Paths below are relative to `research/qore002-implementation-20261016/methods/planning-input/` unless explicitly prefixed otherwise. No peer report, private repository, trial trace, unrelated research, website, or network service was read. No source file was modified. This is agent analysis, not human evidence or a live-site verdict.

Read the generated skill, project-preflight instructions, protocol and role definitions. This is the independent Analyze phase only; cross-examination and adjudication have not occurred.

## Actual commands and results

Commands ran from the workspace unless a working directory is stated. Root paths were resolved at runtime; no user-specific path is needed to reproduce them.

1. From `derived-initial/qore-plan-qaizen-labs`, ran `python3 scripts/project-check.py references/project.json --root <resolved qore-skills/examples/qaizen-labs> --method plan`. Exit 0, coverage COMPLETE, no problems. Both current source digests matched. The complete JSON result is preserved as sibling artifact `qa-preflight.json`; the preflight was repeated only to preserve that complete machine result.
2. From the actual public example root `qore-skills/examples/qaizen-labs`, inspected the frozen checker, then ran the returned argument vector `python3 -B checks/check_contract.py surface-contract.json`. Exit 0, `valid: true`; output explicitly limits the result to contract consistency.
3. Ran a local `python3 -B -` script using `hashlib.sha256` on every frozen file listed in `planning-input.json`, then imported the frozen `checks/check_contract.py` with `importlib.util.spec_from_file_location` and called `validate` on a deep copy of the contract for each mutation. Exit 0. Positive contract passed. Six negative controls were rejected: unknown transition state; Back focus changed to summary; Back traversal changed to click; unauthorized entry origin; answer policy changed to submit; allowed methods changed to GET/POST. These are actual offline checker observations, not browser tests.

Browser test execution was deliberately excluded by the role brief's prohibition on network services: `tests/test_browser_probe.py:24-31` starts a local HTTP service. The frozen input also does not include its referenced fixture or `tools/context.py` dependency (`tests/test_browser_probe.py:25`; `tests/test_labs_contract.py:11-15`). I therefore do not claim the supplied unittest suites ran or passed. The relevant declared project check did run.

## Profile facts consumed and identifiable effects

Profile identity: `qaizen-labs` version `0.1.0`, SHA-256 `f76afdd45cb6352e5044a06affc4182ea6cd40aa9c012fb216636a61faa428f0`.

| Fact consumed | Source ID / current source SHA-256 | Effect on this plan |
|---|---|---|
| `surface-contract` command | checker / `9ef2a0acf51f078ce290ec723ca550b8b73597e68304179fe4d0625c5757963b` | Executed the actual offline checker; kept its result distinct from browser evidence. |
| `close-focus` invariant | surface / `3728739a119a53272541f83d451e40addb6939304f9d9ec060a477a87170a4a3` | Requires its own help-close assertion and a negative control that distinguishes it from Back. |
| `back-focus` invariant | surface / same digest | Requires recorded sequential Tab/Shift+Tab steps and Enter activation; mouse or programmatic focus cannot repair a failed traversal. |
| `unanswered-scope` invariant | surface / same digest | Adds answer-preservation checks and attempted-blocking tests; expected blocked analytics are retained without weakening policy. |

The plan preflight returned no web surface. I did not consume a profile web entry as a current browser authorization. Current declared surface expectations are read from the frozen contract as requirements, not observations of deployment behavior.

## Proposed decisions and test deliverables

Retain D1–D5 and reuse the existing harness. Sequential traversal, separate focus obligations and bounded URL waiting are already implemented in this snapshot (`tools/browser_probe.mjs:116-139`); planning must verify and strengthen them instead of presenting them as unimplemented discoveries. Existing browser tests already cover positive traversal, exclusion from tab order, blocked POST, blocked main-frame navigation and a false focus assertion (`tests/test_browser_probe.py:43-82`).

Produce one traceable matrix linking L01–L07, fixture identity, assertion, expected failure, artifacts and actual status. Required browser cases need a real optional driver; missing capability leaves that evidence NOT_TESTED/PARTIAL rather than silently succeeding through mocks. Preserve legacy actions in the positive path (`verification-spec.md:16`; `tests/test_browser_probe.py:43-53`).

| Acceptance | Positive evidence required | Discriminating negative control / current gap |
|---|---|---|
| L01 current sources | Fresh preflight, profile digest, fact/source/effect record | Missing and changed source both prevent affected COMPLETE. Changed source has a test at `test_labs_contract.py:43-51`; missing source should also be demonstrated. |
| L02 offline contract | Actual command and consistent contract | The six offline mutations above fail. Keep this separate from site results. |
| L03 keyboard Back | Actual focus-step sequence reaches Back, then Enter causes state and focus transition | Back excluded from tab order fails before any later click. Existing test establishes that traversal failure prevents the click (`test_browser_probe.py:58-66`). Retain this property. |
| L04 independent focus / unanswered | Help close returns summary focus; Back returns introduction heading focus; answers remain absent/unchecked in question state | Add a close-help fixture with wrong focus while Back remains correct, and the converse. Existing positive browser test omits the help transitions. Returned-introduction-only answer checking can become vacuous after inputs disappear, so retain a check before Back as well. |
| L05 policy | Isolated context, route interception and service-worker blocking before entry; blocked events retained | Actual attempted POST and main-frame escape are covered in test definitions. Add popup/redirect attempts and service-worker attempt as distinct controls; checking the result's configuration string alone does not prove service-worker behavior (`test_browser_probe.py:71`). |
| L06 async navigation | Delayed expected URL succeeds within the declared timeout | Never-changing or wrong URL fails after the finite deadline. Implementation waits at `browser_probe.mjs:116`; no matching browser test exists in the frozen suite. |
| L07 evidence honesty | Offline, synthetic and authorized live evidence have distinct identity, time, target and scope | Missing required journey observations cannot qualify as completed Labs verification even if the generic probe finishes. |

For eventual current-site observation, require observed introduction and returned-introduction state, not merely a generic focused `h1`. The action list asserts heading focus but does not explicitly assert the intended introduction content at return (`examples/qaizen-labs/browser-actions.json:99-108`); the positive fixture already combines focus and state visibility checks (`tests/test_browser_probe.py:49-52`). Ask UX for the narrow, stable state assertion before adding selectors.

## Risks, counterexamples and boundaries

1. **Evidence identity can be lost during handoff.** The result records target, time, driver and policy but no action-file, policy-file, harness or contract content digest (`tools/browser_probe.mjs:31-39`). Counterexample: two executions use different action files against the same target and carry the same label, yet a reviewer cannot bind a detached result to the intended frozen protocol. Proposal: an enclosing run manifest records all those digests and artifacts; do not require the generic probe to understand the Labs schema.
2. **Generic completion can be mistaken for contract completion.** With no `--actions`, the actions array is empty and the generic probe can finish after snapshots (`browser_probe.mjs:22,100-105,147-148`). This is not by itself a generic harness defect. Require the Labs-specific evidence consumer to check required observations rather than interpreting its generic COMPLETE as L01–L07 success. Missing screenshot/video/trace needs an explicit scoped decision (`browser_probe.mjs:154-162`), not a silent certification claim.
3. **Privacy claim needs a realistic trace control.** Events intentionally omit request headers/bodies, but tracing is also enabled with DOM snapshots and screenshots (`browser_probe.mjs:37,67,79-89,155`). Hypothesis requiring investigation: a trace may retain network or page material beyond that events projection. Before stating that no headers/bodies are retained across all artifacts, run a synthetic secret-canary fixture and inspect the trace, video, DOM and event outputs. Keep captures local and unanswered, and label any narrower guarantee precisely. This is not evidence of current live data leakage.
4. **Asynchronous focus can be misclassified.** URL assertion waits, while focused-element and attribute assertions read immediately (`browser_probe.mjs:116-123`). Counterexample hypothesis: a component schedules focus restoration after a frame, and Enter returns before focus arrives. Define a bounded eventual assertion if that is the intended UI contract; use delayed focus positive and never-focus negative controls. Avoid an arbitrary sleep as the proof.
5. **Unanswered selection assertion may be broader than answers.** It checks all `aria-selected=true` and `aria-checked=true` elements in the document (`browser_probe.mjs:124-125`). Hypothesis: a selected navigation tab unrelated to the questionnaire would cause failure. UX/Architecture should identify the correct questionnaire boundary; retain the current conservative check until evidence justifies narrowing it. No unsupported claim that the current site contains that case.
6. **Authorization is separate from origin allowlisting.** Policy controls methods and main-frame/popup navigation, not general permission to operate the app. The maintained contract prohibits result generation, submissions, source redistribution and certification claims (`surface-contract.json:20`). Keep the current isolated context and install policy before entry (`browser_probe.mjs:54-69`); do not use a logged-in browser or relax policy to suppress expected analytics failures. Read-only HTTP methods are a bounded protocol rule, not proof that every possible server operation is side-effect-free.

## Edge-case Gherkin proposals

```gherkin
Scenario: A correct Back transition cannot hide wrong help-close focus
  Given help is open on the unanswered first question
  And Back is reachable and restores the introduction correctly
  When Close is reached sequentially and activated with Enter
  And the help closes but focus moves outside its summary
  Then the close-focus obligation fails independently

Scenario: A detached generic probe result cannot satisfy Labs acceptance
  Given a completed probe result has no bound Labs action-file identity
  When the maintainer evaluates the required Labs checks
  Then contract completion remains unproven
  And the report names the missing observations and identity

Scenario: Delayed navigation is distinguished from missing navigation
  Given entry navigation completes after a controlled delay inside the timeout
  When the URL assertion runs
  Then it succeeds only after the exact expected URL is observed
  But a fixture that never transitions fails within the finite timeout

Scenario: A forbidden popup is blocked without weakening the policy
  Given policy is installed before the isolated context enters the fixture
  When the fixture attempts a popup to an outside origin
  Then no outside-origin top-level document is loaded
  And the attempted navigation is retained as blocked evidence
  And the scoped journey cannot be reported as complete
```

## Required questions for peer roles

- **Product:** Should missing video/trace prevent scoped journey success, or can screenshots plus complete assertions suffice? Define the necessary decision evidence instead of equating every optional artifact with acceptance.
- **Architecture:** Where should the run identity manifest and required-observation completeness check live, so legacy generic probe behavior remains compatible? Can its scope also resolve the trace privacy guarantee without exporting private content?
- **UX:** What stable assertion proves introduction state after Back, and what questionnaire boundary distinguishes answers from unrelated selected UI? Is focus restoration explicitly eventual within a bounded timeout?
- **Delivery:** Will the local optional driver and fixture be available for all discriminating controls, and which gate prevents release claims when those tests are skipped? Preserve separate current-site authorization/capability dependencies after local corrections.
- **All roles:** Which proposed decisions rely on current observations versus declared requirements? Every claimed website pass needs a fresh authorized observation; an agent's judgment or fixture pass cannot substitute.

## Unfinished work and status

Independent analysis is complete within its bounded scope. Browser controls, trace-canary privacy inspection, current-site observation, peer cross-examination and adjudication remain unperformed. No current website defect or pass is asserted. Preflight coverage COMPLETE means the selected profile facts are current; it does not mean the Workflow protocol, implementation or release evidence is complete. The smallest next QA step is to agree the matrix and evidence identities, then execute the missing synthetic controls with the actual driver under the parent task's authorized conditions.
