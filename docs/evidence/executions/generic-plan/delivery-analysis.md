# Delivery independent analysis

Observed: 2026-10-15T19:51:53.796858+00:00. Target: `<CANDIDATE_B>`; assigned frozen snapshot `dec34e19b7b3036c213299a1f98b05fec1709212fb156eabf9928682024ae2cb` (identity supplied, not independently recomputed). Workflow applies because `examples/validator-hardening.md:6-16` already specifies this change. This is an independent Analyze report; no peer conclusions or evaluation reports consumed.

## Current evidence and bounded proposal

A01–A03 already have matching coverage: malformed envelope, skipped verification preserving high/critical severity, and valid empty findings (`tests/test_validators.py:64-105`). Do not reimplement these achievements. The example expressly warns that declarations alone do not prove phase completion (`examples/validator-hardening.md:43-48`). Current code separates verified blocking severity and preserves a phase-evidence limitation (`skills/qore-review/scripts/finding-lint.mjs:43-51`).

Proposed D4: tighten only the verifier declaration grammar to the two documented exact tokens. The parser takes `split('=')[1]` and accepts any declaration starting `--verifier=` (`skills/qore-review/scripts/finding-lint.mjs:6-10`). A read-only probe with the existing valid fixture and `--verifier=ran=skipped` exited 0, reported verifier `ran` and COMPLETE. This is an observed malformed-token acceptance, not proof that independent execution can be established mechanically. Full argv/results are in `delivery-commands.json`.

This is a small extension of honest declaration handling, subject to Product adjudicating applicability to D3. It does not add an execution attestation service, stronger semantic evidence heuristics, a shared validator framework, UX gates, or package-format changes. Preserve explicit empty reviews and the current valid ran/skipped behavior.

## Tasks, dependencies, and gates

1. **T1 Small, 30–60 minutes:** lock exact CLI grammar and exit/output expectations in the applicable specification; add malformed-suffix, missing/duplicate declaration, unknown flag, and valid-token public-entry tests in `tests/test_validators.py`. Basis: existing invocation helper already calls Node with arbitrary flags (`tests/test_validators.py:15-26`); no fixture redesign needed. First capture regression failing on present code.
2. **T2 Small, 30–60 minutes:** replace the permissive declaration parsing/validation in `skills/qore-review/scripts/finding-lint.mjs:4-11`. Preserve all result fields, exit 1 for structural refusals and exit 2 for CLI/read failures (`:9-14,43-58`). Depends on T1’s settled contract.
3. **T3 Small, 30–60 minutes:** clarify exact declarations in `skills/qore-review/references/findings.md`, retain its explicit phase-proof limit (`:22-28`), and run the project check from `qore.json:4`. Current baseline: 82 tests passed in 2.679 seconds; this does not prove future changes correct.
4. **T4 Medium, 1–2 hours:** rebuild into unused staging, verify the new package, compare changed resources and install into an unused qualification project. Basis: validator and findings documentation are hashed release resources (`skills/qore-review/references/release.json:20-24,44-48`), and existing build tests cover deterministic packaging and verification (`tests/test_package.py:68-85`). Do not patch frozen package manifests manually.

Critical order: T1 → T2 → T3 → T4. Estimates are planning allowances for one maintainer, not measured throughput. Definition of done: new rejection tests fail before/pass after, existing A01–A03 behavior passes, full project check passes, rebuilt candidate verifies, and rollout evidence records distinct old/new identities.

## Risks, rollout, peer questions, and limits

Compatibility risk: undocumented callers using suffix-bearing tokens will now receive CLI failure. **Architecture:** trace actual callers before locking D4; can exact equality preserve intended usage without touching packet semantics? **Product:** confirm this bounded extension is the next valuable increment; the supplied acceptance criteria are already implemented, so do not claim an unmet A01–A03 requirement.

Release risk: editing the frozen bundle invalidates resource digests. Work in source/new staging only; existing installations and adaptations stay intact (`docs/profiles.md:43-54`; `docs/troubleshooting.md:7-10`). Roll back by retaining/reselecting the prior verified candidate and installation location; there is no automatic rollback command (`docs/profiles.md:53`). Publication or overwriting adapted skills is outside this plan.

Uninspected/unfinished: exhaustive caller sweep, packaging implementation, independent phase-evidence validator, and cross-examination. No implementation or package edits performed. Reviewed protocol/roles/specification contracts, example, validator/redactor, tests and cited documentation. This role is complete for Analyze; final protocol coverage belongs to the lead.
