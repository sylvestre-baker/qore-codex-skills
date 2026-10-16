# QA and security — independent Analyze report

Observed at 2026-10-15T20:07:17.824717+00:00. Workflow is selected by the applicable `examples/validator-hardening.md:4-8,25-51`. Target: `<CANDIDATE_B>`; supplied frozen snapshot `dec34e19b7b3036c213299a1f98b05fec1709212fb156eabf9928682024ae2cb` (not independently rehashed). Source references below are relative to that root.

## Current evidence and profile consumption

Bundled project preflight ran before project facts were consumed: exit 0, COMPLETE; full output/argv/cwd/stdout/stderr/exit in `qa-commands.json`. Profile `qore/0.1.0`, SHA-256 `da03026c9f73a7771cc35aaaff898a3b970fed75362ebfd0c670068d6b23b3d9`. Consumed fact `check`, source ID `project`, current digest `948b2784fa7970cf90a25c338a29067b13d8b4476f666d712a5eb95fc6f641c8`, matches `qore.json:4`: actual declared suite ran, 82 tests passed in 2.585s. Consumed `preserve-adaptations`, same source/digest (`qore.json:6`): acceptance requires new staging and preservation of existing adaptations; no package/source writes performed. Other-method facts were not consumed as profile authority.

Inspected the skill and required planning references, existing spec, `qore.json`, complete `tests/test_validators.py`, `skills/qore-review/scripts/finding-lint.mjs`, and `redact-for-verifier.mjs`. No generic-run or peer reports were read.

## Proposed next improvement

Propose D4: accept only exact verifier tokens `--verifier=ran` and `--verifier=skipped`; reject appended payloads with usage exit 2, empty stdout, before reading a packet. This is a measured CLI-boundary gap, not a seeded production defect or a claim of deployment harm. `finding-lint.mjs:6-10` splits at `=` and consumes only component 1. Against unchanged source and temporary `{"findings":[]}`, `--verifier=ran=skipped` returned exit 0, COMPLETE, SHIP; inverse suffix returned PENDING. Exact canonical tokens retained current behavior, and duplicate declarations already returned exit 2. Full observations are recorded.

D4 preserves D1-D3 (`examples/validator-hardening.md:14-16`), including valid empty review and the declaration/evidence distinction (`finding-lint.mjs:44-51`). It needs a public CLI regression test: existing tests invoke canonical flags through `tests/test_validators.py:15-26`; present declaration cases do not exercise suffixes.

## Acceptance matrix

| Boundary | Falsifiable acceptance / evidence |
|---|---|
| Declaration grammar | Suffix, empty, missing, duplicate, unknown flag: exit 2 and no JSON success. Exact ran/skipped remain accepted. New regressions needed. |
| Envelope/data integrity | Preserve invalid envelope exit 1; malformed JSON exit 2; explicit empty findings valid. Existing tests `:64-85`. |
| Uncertainty | Skipped preserves high/critical, PARTIAL, no verified blockers/SHIP; CONFIRMED/REFUTED rejected. Existing `:91-104`. |
| Evidence/blockers | Confirmed high requires counterexample; uncheckable evidence rejected. Existing `:106-113`. |
| Privacy | Redactor outputs scalar allowlisted fields only; nested values rejected; unknown rationale dropped. Existing `:115-124`; implementation `redact-for-verifier.mjs:13-33`. |
| Authorization | A CLI declaration cannot establish real independent execution (`finding-lint.mjs:51`). No account/service/data authorization surface exists in inspected scripts. |
| Adaptation preservation | Generate future derivative in new staging; existing adaptation unchanged (`qore.json:6`). No generation proposed here. |

```gherkin
Feature: Exact verifier declarations
  Scenario: QA04 Reject a misleading verifier suffix
    Given an explicit empty findings packet
    When validation receives --verifier=ran=skipped
    Then it exits 2 with usage on stderr and empty stdout

  Scenario: QA05 Retain skipped uncertainty
    Given a valid high PLAUSIBLE candidate with src/input.ts:12 evidence
    When validation receives exactly --verifier=skipped
    Then severity stays high and coverage stays PARTIAL with no SHIP
```

Coverage: QA04 → US1 / D4; QA05 → US2 / D2 / D3. Existing A01-A03 remain mandatory.

## Risks, questions, limits

Trigger: malformed declaration containing extra `=` currently selects the first value; outcome is misleading declared coverage. Hypothesis: an external wrapper constructs such flags; no wrapper impact is established. Do not classify this as a verified high blocker.

Product: Should malformed declarations reject uniformly with existing usage exit 2? Architecture: Can exact token matching preserve all supported callers? UX: Should stderr usage remain the recovery instruction? Delivery: Can this remain one parser change plus table-driven CLI regression and spec update, staged separately? Each role must answer from sources; no consensus claimed.

Unfinished: caller inventory, independent challenge, adjudication, final specification/lint, snapshot rehash, other validator implementation review. Complete role analysis; overall protocol coverage remains PARTIAL until required peer/challenge phases complete. No implementation, publication, browser claim, or real-user privacy exposure was attempted.
