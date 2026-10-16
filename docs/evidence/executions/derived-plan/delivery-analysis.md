# Delivery independent analysis

Observed: 2026-10-15T20:05:37.754569+00:00. Role: Delivery, independent initial Analyze; target frozen snapshot `dec34e19b7b3036c213299a1f98b05fec1709212fb156eabf9928682024ae2cb`, root `<CANDIDATE_B>`. Workflow is selected because `examples/validator-hardening.md:1–8` is an applicable existing specification. This is planning only; no source or package modifications.

## Current evidence and profile consumption

The bundled derivative preflight returned COMPLETE, no problems, profile `qore@0.1.0`, SHA-256 `da03026c9f73a7771cc35aaaff898a3b970fed75362ebfd0c670068d6b23b3d9`. Consumed facts: `check` and `preserve-adaptations`, both source `project`, current `qore.json` SHA-256 `948b2784fa7970cf90a25c338a29067b13d8b4476f666d712a5eb95fc6f641c8`. I inspected `qore.json:4–6`. `check` selects the exact final regression argv, rather than an invented Node-only gate. `preserve-adaptations` requires new staging, comparison and preserved installed adaptations for rollout; no in-place derivative replacement. Other returned facts: none. Preflight/probe/check argv, cwd, full stdout/stderr and exits are retained in `delivery-commands.json`.

## Proposed next safe increment

D-D1: tighten the finding validator CLI to accept exactly `--verifier=ran` or `--verifier=skipped`, and reject suffixes. Current `skills/qore-review/scripts/finding-lint.mjs:6–10` takes only `split('=')[1]`; the actual temporary empty-packet probe with `--verifier=ran=unexpected --json` exits 0 and emits COMPLETE/SHIP. This is a bounded input-contract inconsistency with its own usage line, not proof that verification occurred or that production consumers are affected. The current test helper always constructs canonical flags (`tests/test_validators.py:25–26`), leaving this parsing boundary untested. Keep original D1–D3 and A01–A03 (`examples/validator-hardening.md:14–48`) unchanged.

## Tasks, dependencies and sizes

1. T-D1, XS: agree exact CLI grammar and acceptance cases: canonical ran/skipped, missing/duplicate declaration, unknown value, extra equals/trailing text. Basis: one existing CLI, two canonical values, no file-format change. Depends on Product and Architecture accepting this bounded contract.
2. T-D2, S: add public-entry regression cases and minimally tighten parsing. Basis: `finding-lint.mjs:4–11` plus existing subprocess harness (`tests/test_validators.py:15–26`); no new library or shared abstraction needed. Depends on T-D1.
3. T-D3, XS: update applicable specification and findings guidance with exact-token rejection and exit-2/no-result expectations; retain the phase-evidence limitation (`finding-lint.mjs:51`; `references/findings.md:26`). Depends on T-D1; parallel with T-D2.
4. T-D4, S: run focused boundary regressions, then exact profile check; stage a fresh package/derivative and compare affected files before any installation. Basis: packaging preservation tests at `tests/test_package.py:183–219`, and README safe-update guidance at lines 33, 79–81. Depends on T-D2/T-D3. Critical path T-D1→T-D2→T-D4. These are relative effort units, not calendar promises.

## DoD, risks and rollout

DoD: malformed tokens return usage exit 2 without JSON success; canonical empty review and skipped high candidate behavior remain as tested (`tests/test_validators.py:77–104`); exact full check passes; source/spec/tests agree; fresh staging retains older installed adaptations. Risk: an undocumented caller relies on permissive suffixes; search callers before accepting the change and document rejection. Risk: widening into per-finding verifier attestations changes report semantics and dependency scope—defer to a separate decision.

Rollout boundary is local script/package generation and optional local skill installation, not a service or database. Keep this frozen target intact; implement in a separate candidate, generate to an unused directory, compare, and run checks before selecting installation. Rollback selects the preserved previous package/skill in a new local staging location; never overwrite adaptations. No remote deployment, migration, browser verification or release authorization is implied.

## Alternatives and peer questions

Product: is strict CLI grammar valuable enough as the smallest useful improvement, and can broader evidence-proof ambitions be deferred? Architecture: confirm existing callers and release manifests permit a single-parser change without copied validators or a shared schema prerequisite. QA: exercise both canonical values and every malformed-token class, checking stdout as well as exit. Alternative: test-only hardening; useful but leaves observed acceptance. Alternative: broad verifier-evidence binding; higher value potentially, but requires separate packet/run identity design.

Uninspected: full packaging implementation, external callers, installed adaptations, exhaustive parser fuzzing. No claim of deployment readiness. Initial role report complete within the bounded analysis; cross-examination remains for the next Workflow phase. The exact profile check passed: 82 tests, 2.530s, exit 0; full output is retained in the command artifact.
