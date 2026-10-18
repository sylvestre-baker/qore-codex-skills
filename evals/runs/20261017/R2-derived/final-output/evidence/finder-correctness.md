# Correctness finder report

Actual context identity: `/root/finder_correctness` (independent finder dispatched by `/root`). Discovery started 2026-10-17 11:13:50 UTC. Discovery ended 2026-10-17 11:14:11 UTC. Report completed 2026-10-17 11:15:01 UTC. No peer or lead output was read; no network access, source mutations, or subagents were used. Findings below are candidates for the fresh verifier, not independent verdicts.

## Scope and snapshot

Target: `/workspace/worker/target/verification-protocol.md`, SHA-256 `0a3452f02e358d8800fb26d591083deb972c5531165473990dc27007a9a9e0d4`.

Criteria examined in full:

- `/workspace/worker/surface-contract.json`, version 0.1.0, SHA-256 `3728739a119a53272541f83d451e40addb6939304f9d9ec060a477a87170a4a3`.
- `/workspace/worker/observation-policy.json`, SHA-256 `15f4e5b4960b5011684be265f027e42b8637a3b8aae96b24bba1ba3a4d0f0202`.
- `/workspace/worker/checks/check_contract.py`, SHA-256 `9ef2a0acf51f078ce290ec723ca550b8b73597e68304179fe4d0625c5757963b`.

Method references read: skill `references/protocol.md` and `references/findings.md`. Scope is the authored verification procedure, not the website or the correctness of the contract checker itself.

## Boundary trace

Central value: the required journey transition sequence and its acceptance result. The source is the contract's `transitions` array and `required_checks`; the transformation is the six numbered prose instructions; the claim is that executing those instructions verifies the journey; the consumer is a tester deciding whether the listed acceptance obligations have been observed. No runtime serializer, evidence file schema, or browser result is supplied, so this is a document trace only.

The source transition fields actually supplied are `id`, `from`, `to`, `control`, `activation`, and, for Close/Back, `traversal` and `focus_after`. The protocol prose explicitly supplies controls, some activation/traversal methods, and assertions; it does not preserve transition IDs or define a results artifact. Mapping adjacent boundaries:

| Source transition | Source control/activation | Target instruction and acceptance observation |
| --- | --- | --- |
| entry | journey anchor/click | line 5: follow journey link; no explicit destination assertion |
| start | Start the check/click | line 6: start without an answer |
| open-help | summary/Enter | line 7: summary, activation unspecified |
| toggle-help | summary/Space | absent |
| reopen-help | summary/Enter | absent |
| close-help | Close/Enter; Tab; focus summary | line 8: Tab or Shift+Tab, Enter, help closed and summary focused |
| back | Back/Enter; Tab; focus introduction heading | line 10: Tab or Shift+Tab, Enter, introduction visible, question/help absent, heading focused |

The unanswered invariant is transmitted: scope.answer_policy is `unanswered` (contract line 6), target line 6 forbids selection, and lines 9-10 assert the unanswered state before Back. The Back precondition is also coherent: line 8 closes help and restores summary focus before line 10 begins sequential traversal. These checks do not supply the omitted summary keyboard transitions or policy observations.

The contract also supplies `entry_url`, `allowed_origins`, `scope.allowed_methods`, `scope.locale`, `scope.viewport`, and `required_checks`. The target neither names nor imports either JSON file. In particular, it provides no network admission rule or read-only/origin-policy observation.

## C-001 — Required keyboard help-toggle sequence is untested

Severity: medium.

Evidence: target `/workspace/worker/target/verification-protocol.md:7-8` goes directly from opening help using the summary to activating Close. Contract `/workspace/worker/surface-contract.json:11-13` requires summary Enter to open, summary Space to close, and summary Enter to reopen; line 18 explicitly lists `help-toggle` as required. The target specifies neither the opening key nor any summary toggle/reopen step.

Triggering condition: a page opens help by pointer and supports Close/Back as specified, but its summary Space activation or subsequent Enter reopening fails. A tester can follow every target instruction and never exercise that failure path.

Consequence: successful execution of the procedure cannot establish the required `help-toggle` behavior and can produce an acceptance decision without coverage of that obligation.

Requirement: the contract's declared help transitions and required `help-toggle` check. This is an omission in the procedure, not a demonstrated defect in the deployed website.

Contrary-evidence search: all six target steps were inspected. Closing help in line 8 uses the separate Close control, so that assertion does not exercise the summary Space handler. The structural checker emits the supplied `help-toggle` check name, but its return explicitly limits the result to contract consistency (`checks/check_contract.py:42-43`); it does not execute target instructions or browser transitions.

Uncertainty: no browser observation exists in this scope; actual website handling of Space/Enter is unknown. An external runner might add missing steps, but no such runner or incorporation instruction is supplied in the target.

Suggested disposition: explicitly execute and assert summary Enter → open, Space → closed, Enter → open before traversing to Close.

## C-002 — Procedure omits the mandatory observation-policy precondition

Severity: medium.

Evidence: `/workspace/worker/surface-contract.json:5-6` restricts origins to `https://qaizen.io` and methods to GET/HEAD/OPTIONS; line 18 requires `read-only-policy` and `origin-policy`; line 20 specifically expects an analytics POST to be blocked and its observed effects retained. `/workspace/worker/observation-policy.json:2-3` independently names the same sole allowed origin. The target's first operation at line 5 is navigation; the complete instructions at lines 5-10 never install a method/origin restriction, instruct the operator to rely on an already installed restriction, inspect blocked traffic, or retain blocked-request effects.

Triggering condition: an ordinary unguarded browser executes the procedure and the expected analytics POST is emitted, or navigation/subresources reach an origin outside the allowlist. All target UI assertions can still be satisfied.

Consequence: completion of the procedure can violate the declared observation boundary while producing no evidence for two required checks. The target also fails to collect the blocked-analytics effects explicitly required by the contract.

Requirement: the read-only and origin-policy checks, the method/origin scope, and the explicit blocked-analytics requirement. Not selecting an answer does not enforce request methods for page-driven analytics.

Contrary-evidence search: the target's unanswered instructions at lines 6 and 9-10 constrain answer state, not network requests. The standalone policy file only contains data; nothing in the target loads or applies it. `checks/check_contract.py:12-18` checks declared origin/method values in JSON, and its line 2 states it never contacts the website; this supplies no browser enforcement. No assertion is made that prohibited requests actually occurred.

Uncertainty: the broader execution environment might install an independent guard. None is specified by the target or supplied criteria, so this candidate concerns a missing precondition in a standalone procedure; actual network behavior remains unobserved.

Suggested disposition: before navigation, require an origin/method request guard, record allowed/blocked request outcomes and visible effects, and assert the policy checks on the resulting observation.

## Checks, limits, and unfinished scope

Executed `python3 -B /workspace/worker/checks/check_contract.py /workspace/worker/surface-contract.json`; exit status 0. Output was `valid: true` with all eight supplied check names and the explicit limit `Contract consistency only; browser observations establish current behavior.` This checks the input contract and cannot establish procedure coverage or deployed behavior.

Two candidate findings returned. No confirmation/refutation verdicts assigned. All assigned document/source scope was examined; no scope remained unfinished at return. No deployed website behavior, network events, source implementation, or historical claim was verified. The target's explicit reconstruction disclaimer at line 3 is preserved in interpretation.
