# Product Analyze — Labs verification protocol correction

Phase: independent Analyze only. Workflow is selected by the existing applicable `examples/qaizen-labs/verification-spec.md`; its scope and revision warning apply (lines 8–18, 109). No peer report was read. This report does not establish human acceptance or live website behavior.

## Snapshot and sources

Frozen target: `research/qore002-implementation-20261016/methods/planning-input/`; target identity is `1461fc149209fa29adc067a2b8f3c644055228aa0a2f45485779e3a418f47fd6`, recorded in `methods/planning-input.json`. Candidate manifest: `0540496cea29da71f72046f36a12c3a23b4d71900c97f7193f4dba699836b036`. All code references below are relative to that frozen target, not the working public tree.

Inspected: `examples/qaizen-labs/verification-spec.md:1–109`, `surface-contract.json:1–21`, `browser-actions.json:1–110`, `observation-policy.json:1–5`, `checks/check_contract.py:1–54`, `tools/browser_probe.mjs:1–169`, `tests/test_browser_probe.py:1–82`, `tests/test_labs_contract.py:1–51`. Also read the derivative skill, protocol, roles, project-preflight instructions and bundled profile. The actual public example was used only for freshness validation and the declared offline check. No website request, service, source modification, unrelated research or private repository inspection occurred.

## Maintainer outcome and smallest useful change

The useful outcome is a maintainer decision about this exact declared journey, supported by evidence that distinguishes a keyboard failure from a mouse-success false positive. A green command or existence of a recording is a proxy, not that outcome. The specification explicitly describes a verification coverage gap, not an established website defect (`verification-spec.md:8`).

Preserve the existing harness, action formats and optional driver. The frozen implementation already includes bounded sequential traversal, focus assertions, request blocking and URL waits (`tools/browser_probe.mjs:54–65, 116–144`). Do not replace them or invent a new service. The smallest useful revision is to close any remaining mismatch between the acceptance contract, the action sequence and the evidence a maintainer receives, adding only discriminating checks or reporting needed to make that decision. A no-new-defect conclusion remains valid (`verification-spec.md:18`).

Scope stays desktop English, 1280×800, entry/state only, first question unanswered (`surface-contract.json:6`); there is no questionnaire completion, mobile expansion, performance/accessibility certification, deployment or website implementation work (`verification-spec.md:16,109`). Existing browser output status is a harness execution status: reaching the end sets COMPLETE (`tools/browser_probe.mjs:147–152`). It must not automatically become a claim that every required Labs check passed.

## User stories and measurable acceptance

1. **Maintainer: distinguish reachability from final state.** Starting on the unanswered first question after help closure, Back is reached using actual sequential Tab or Shift+Tab events, followed by Enter. Each traversal event records direction, ordinal and active element, and a bounded failure prevents later mouse success from rescuing the result. The reachable control passes; a control excluded from the sequential order fails. Existing basis: `surface-contract.json:14–18`; harness `127–139`; declared controls `tests/test_browser_probe.py:43–66`.
2. **Reviewer: verify separate transitions.** Help opening, Space toggling, reopening and keyboard Close are observed; Close leaves help closed and summary focused. Independently, Back returns to the introduction with heading focus. The acceptance result links each transition to its action/evidence location rather than treating the two focus destinations as interchangeable. Basis: `surface-contract.json:11–18`, `browser-actions.json:32–108`, checker `32–36`.
3. **Maintainer: know the returned state.** The Back result must establish that the introduction is visible and the question view is left, as well as heading focus. `browser-actions.json:99–108` currently checks generic `h1` focus and absence of checked inputs but does not explicitly assert introduction visibility or question disappearance. This is a source-backed evidence-gap hypothesis, not a demonstrated site failure: a hypothetical page retaining a question while focusing an unrelated `h1` could satisfy those two assertions. The smallest investigation is a synthetic state/focus counterexample and reuse of existing `assert-visible`/`assert-hidden` actions (`tools/browser_probe.mjs:117`, positive test `test_browser_probe.py:50–53`) if the actual state contract needs those predicates.
4. **User: remain unanswered.** Evidence identifies the first-question state with no selected answers before traversal and verifies the declared observation never selects an answer. The existing no-selection checks at `browser-actions.json:25,104` are useful snapshots, but the latter occurs after leaving the question and may be vacuous when question controls are removed. Do not overstate those snapshots as proof of every intervening moment; use action review and, if necessary, a pre-Back check as the smallest strengthening. Basis: contract `6,20`, harness `124–125`.
5. **User: preserve observation boundaries.** Before entry, block service workers, non-GET/HEAD/OPTIONS requests and outside-origin top-level/popup navigation. Retain blocked events; expected blocked analytics do not justify relaxing the policy or declaring site failure. A forbidden navigation attempt prevents scoped success. Basis: contract `6,20`; harness `54–65,144`; policy tests `68–77`.
6. **Reviewer: distinguish evidence classes.** Report separately (a) fresh profile and offline consistency, (b) actual positive/negative harness controls and (c) fresh authorized website observations. Missing (c) leaves current site behavior unestablished even if (a) and (b) pass. Required observations missing from an action list prevent complete Labs acceptance, regardless of generic harness COMPLETE. Basis: `verification-spec.md:60–100`, checker `42–43`, harness `147–152`.

Acceptance deliverables are a revised sourced specification with story/check mapping, the smallest necessary action/harness change, discriminating controls, and a short decision record identifying passed, failed and unobserved obligations. Keep observations linked to their snapshot/run and finite traversal limits (currently 24 steps for summary/Back and 12 for Close, `browser-actions.json:34,64,88`). Do not add a product dashboard, mandatory browser dependency or broad accessibility score.

## Actual commands and outcomes

Commands ran from the workspace unless otherwise stated. No browser tests were executed because this Analyze brief prohibits services/website requests; the optional-driver tests start a local HTTP service (`tests/test_browser_probe.py:21–31`). The frozen `test_labs_contract.py` imports an unfrozen `tools/context.py` dependency (`10–12`), so I did not silently borrow the live repository implementation to execute it.

1. In `research/qore002-implementation-20261016/derived-initial/qore-plan-qaizen-labs`: `python3 scripts/project-check.py references/project.json --root "$WORKSPACE/qore-skills/examples/qaizen-labs" --method plan` (the actual invocation used the resolved workspace root). Exit 0. Complete result:

```json
{
  "schema": "qore-context-check/1",
  "profile": {"id": "qaizen-labs", "version": "0.1.0", "sha256": "f76afdd45cb6352e5044a06affc4182ea6cd40aa9c012fb216636a61faa428f0"},
  "method": "plan",
  "coverage": "COMPLETE",
  "sources": [
    {"id": "surface", "path": "surface-contract.json", "expected_sha256": "3728739a119a53272541f83d451e40addb6939304f9d9ec060a477a87170a4a3", "actual_sha256": "3728739a119a53272541f83d451e40addb6939304f9d9ec060a477a87170a4a3", "current": true},
    {"id": "checker", "path": "checks/check_contract.py", "expected_sha256": "9ef2a0acf51f078ce290ec723ca550b8b73597e68304179fe4d0625c5757963b", "actual_sha256": "9ef2a0acf51f078ce290ec723ca550b8b73597e68304179fe4d0625c5757963b", "current": true}
  ],
  "commands": [{"id": "surface-contract", "argv": ["python3", "-B", "checks/check_contract.py", "surface-contract.json"], "source": "checker", "applies_to": ["plan", "review"]}],
  "invariants": [
    {"id": "close-focus", "statement": "Closing question help restores focus to its summary; verify this separately from the application Back transition.", "source": "surface", "applies_to": ["plan", "review", "ux"]},
    {"id": "back-focus", "statement": "Reach the application Back control using sequential Tab or Shift+Tab; activate with Enter and verify introduction heading focus. A click or programmatic focus does not prove keyboard reachability.", "source": "surface", "applies_to": ["plan", "review", "ux"]},
    {"id": "unanswered-scope", "statement": "Leave the first question unanswered, block all non-GET/HEAD/OPTIONS requests and main-frame/popup navigation outside the allowed origins. Record blocked analytics; do not relax policy for a successful recording.", "source": "surface", "applies_to": ["plan", "review", "ux"]}
  ],
  "surfaces": {},
  "consumed_source_ids": ["checker", "surface"],
  "problems": []
}
```

2. In `qore-skills/examples/qaizen-labs`: `python3 -B checks/check_contract.py surface-contract.json`. Exit 0. Complete result:

```json
{"valid": true, "schema": "qaizen-labs-surface/1", "checks": ["entry", "unanswered", "help-toggle", "close-focus", "keyboard-back", "introduction-focus", "read-only-policy", "origin-policy"], "limit": "Contract consistency only; browser observations establish current behavior."}
```

3. Read-only inspection used `rg --files`, `rg -n` and `nl -ba` on the listed frozen inputs and `cat` on the assigned derivative protocol/profile files; all completed successfully. No test output is inferred from reading test code.

## Profile facts consumed and their effect

The preflight selected three invariants and one command; I actually consumed all four. `surface-contract` is bound to source `checker`, current digest `9ef2a0acf51f078ce290ec723ca550b8b73597e68304179fe4d0625c5757963b`; it caused the offline command to run and prevents its success being reported as website success. `close-focus`, `back-focus` and `unanswered-scope` are each bound to source `surface`, current digest `3728739a119a53272541f83d451e40addb6939304f9d9ec060a477a87170a4a3`. They respectively require independent Close/Back proof; forbid click/programmatic focus as keyboard evidence; and restrict the journey plus blocking-policy acceptance. The checker returned no plan-applicable web surface, so no browser entry was selected from this method's profile result.

## Risks, hypotheses and required peer questions

- **Evidence overclaim:** Generic harness COMPLETE after an arbitrary action list could be presented as all Labs obligations satisfied. Trigger: omitted action/required observation. Effect: maintainer gets a false acceptance decision. Evidence: harness `105–148` versus contract `18`; resolve with required-check/evidence mapping or an explicit report distinction, not necessarily a new runtime schema.
- **State ambiguity hypothesis:** Generic heading focus and no remaining checked input could pass without a true introduction return. Concrete hypothetical counterexample and smallest investigation appear in acceptance item 3. No observed deployment defect is claimed.
- **Flakiness hypothesis:** Immediate focus assertion after asynchronous state handling may fail transiently (`tools/browser_probe.mjs:118–119`); the per-action 900 ms wait occurs after the assertion (`143`). Ask Architecture/QA to determine whether a retrying focus assertion is needed from a discriminating async control before changing semantics.

**Architecture question (sent directly):** What is the smallest extension to the existing harness that proves Back was reached through recorded Tab/Shift+Tab and activated with Enter while preserving legacy actions? Which new abstraction is necessary, if any, and which evidence rejects mouse-click false positives? Also consider whether the existing visibility actions suffice for a returned-state predicate.

**Delivery question (routed through the lead because Delivery had not yet been dispatched):** Which artifacts and capability gates are essential for a maintainer to decide the declared desktop-English unanswered journey, and can local contract/harness completion remain useful and explicitly partial when fresh website observation is unavailable? Avoid expanding a protocol correction into site remediation without a demonstrated site failure.

## Unfinished work

No Cross-examine or peer adjudication has occurred. No browser driver availability, synthetic execution, live observation or human acceptance has been established. Resolve the concrete evidence-gap hypotheses using frozen-source-compatible controls; obtain Architecture and Delivery answers at the report barrier; revise the specification from the actual five reports. Product Analyze is complete within its bounded scope; overall Workflow and current website acceptance remain pending.
