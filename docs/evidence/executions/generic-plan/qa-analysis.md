# QA and security independent analysis

Timestamp: 2026-10-15T19:53:34.486966+00:00. Mode: Workflow, initial independent Analyze. Frozen target: `dec34e19b7b3036c213299a1f98b05fec1709212fb156eabf9928682024ae2cb`. Candidate root: `<CANDIDATE_B>`. This report concerns the supplied tutorial and actual local tooling, not a claimed production incident.

## Decision proposal

**QA-D1: Next implement exact verifier-declaration parsing with regression coverage.** `skills/qore-review/scripts/finding-lint.mjs:6-10` accepts one declaration but extracts only `split('=')[1]`. Actual public-entry-point probe: an explicit empty packet with `--verifier=ran=skipped --json` exits 0 and returns `valid:true`, `coverage:COMPLETE`, `verdict:SHIP`, `verifier:ran`. The declared usage permits `ran|skipped` (line 10); this malformed value should exit 2 with a usage diagnostic, without returning a successful packet. `--verifier=skipped=ran` similarly exits 0/PARTIAL. This is a concrete parser boundary mismatch; it does not prove independent verification was bypassed in a real workflow.

Reject the complete declaration unless it is exactly one supported token, preserving the existing public spelling and exit-code categories. Do not infer execution from a token: retain the explicit limitation at `finding-lint.mjs:51` and separate evidence requirement in `docs/contracts.md:45-55`. Update the tutorial with a malformed-declaration scenario mapped to US1/D1 and, if needed, an explicit decision ID describing strict CLI input. The existing goal already distinguishes malformed packets from honest uncertainty (`examples/validator-hardening.md:6-16`); do not replace it with an invented product.

**QA-D2: Preserve established packet semantics.** Keep explicit empty findings valid; keep skipped high/critical PLAUSIBLE findings unchanged, PARTIAL, nonblocking and without SHIP. Those behaviors are intentional (`examples/validator-hardening.md:30-48`; `tests/test_validators.py:64-104`). Exact parsing must not become an excuse to require findings or downgrade severity. Keep mechanical claim allowlisting and scalar constraints (`redact-for-verifier.mjs:13-31`) separate from verdict adjudication.

## Acceptance matrix

| ID | Input/condition | Observable result | Existing evidence / needed work |
|---|---|---|---|
| QA01 | Empty envelope, exact `ran` | 0; valid; COMPLETE; SHIP, with declaration limitation | Probe; preserve `test_validators.py:77-79` |
| QA02 | Empty envelope, `ran=skipped` or `skipped=ran` | 2; usage diagnostic; no success JSON | Probe currently contradicts; add regression |
| QA03 | Missing, duplicate, unknown, whitespace/suffixed verifier declaration | 2; deterministic usage failure | Parser `finding-lint.mjs:6-10`; add table cases |
| QA04 | Exact skipped; high/critical PLAUSIBLE with source | 0; original severity; PARTIAL; PENDING; no blockers | Existing `test_validators.py:91-98` |
| QA05 | Exact skipped; CONFIRMED or REFUTED | 1; invalid; no SHIP | Existing `test_validators.py:100-104` |
| QA06 | {}, null, bare array; truncated JSON | 1 for invalid envelope; 2 for parse failure | Existing `test_validators.py:64-75` |
| QA07 | Redactor receives nested allowlisted value or unknown rationale | Nested value refused; unknown rationale excluded from stdout | Existing `test_validators.py:115-124` |

```gherkin
Feature: Exact verification declaration
  Scenario: QA02 Refuse an ambiguous verifier value
    Given an explicit empty findings envelope
    And the declaration is --verifier=ran=skipped
    When the findings validator executes
    Then it exits with usage status 2
    And no successful review JSON is emitted
```
Coverage: QA02→US1/D1/proposed QA-D1; QA01/QA04/QA05→US2/D2/D3/proposed QA-D2; QA06/QA07→US1/D1.

## Boundaries and risks

Trigger: malformed CLI arguments reach the validator. Affected behavior: a declaration outside the documented grammar becomes COMPLETE/SHIP. Confidence is limited to observed structural output; external publication remains unauthorized (`qore-plan/SKILL.md:17`; `docs/contracts.md:55`). No server, database, account authorization, or network boundary is present in these inspected scripts. Files are read from supplied paths and diagnostics go to stderr (`finding-lint.mjs:12-14`; `redact-for-verifier.mjs:9-11,33-34`). Privacy hypothesis: stdout filtering does not sanitize secrets already embedded in allowed claim strings; the scope must not promise universal secret removal. No secret-bearing probe was needed.

## Named peer questions

Product: Is malformed CLI refusal accepted within US1, or should its scope be stated explicitly? Architecture: Can exact-token validation retain exit 2 and avoid duplicating existing envelope checks? UX: Is stderr usage plus absent JSON the intended caller recovery contract? Delivery: Will the gate include the whole existing suite and preserve unrelated redactor semantics? All: What observable requirement justifies any larger change beyond this reproducible edge?

## Evidence and limits

Read the tutorial; the four requested planning references; findings/run-evidence contracts; both review scripts; validator tests; qore.json; relevant run-checker/test searches. No evaluation reports, project profiles, or peer conclusions were consumed. Actual `qore.json:4` check passed: 82 tests, exit 0. Raw argv, cwd, stdout, stderr and status for five CLI probes and the full suite are in `qa-commands.json`. Candidate files were not edited; inputs used a temporary directory. Unfinished: peer cross-examination/adjudication; no exhaustive parser fuzzing, package-derivative impact audit, or independent-context proof. No implementation approval is claimed.
