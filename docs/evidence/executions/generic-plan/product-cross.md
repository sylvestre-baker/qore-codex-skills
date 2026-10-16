# Product Cross-examine

Timestamp: 2026-10-15T19:54:28.102397+00:00. Role: Product. Frozen candidate b; snapshot `dec34e19b7b3036c213299a1f98b05fec1709212fb156eabf9928682024ae2cb`. Read all five complete Analyze reports. One bounded cross-examination pass; no implementation or behavioral probes performed. Source citations below refer to the frozen candidate.

## Revised priority

Revise Product's PD4–PD7 from the immediate increment to a documented follow-up. Prefer Delivery D4 / QA-D1: require the verifier declaration to equal one supported token exactly. Their independently reported `--verifier=ran=skipped` counterexample is directly explained by `skills/qore-review/scripts/finding-lint.mjs:6-10`: splitting and retaining only the first value accepts a suffix outside the documented grammar. Unlike our broader partial-mode proposal, this has a concrete current rejection boundary and needs no new packet representation.

Explicitly extend US1 to malformed invocation, preserving D1–D3 and A01–A03 (`examples/validator-hardening.md:12-48`). Acceptance: both suffix orders, empty values, missing/duplicate declarations and unsupported tokens receive usage exit 2 without success JSON; exact ran/skipped retain current outcomes and severity. Retain the declaration limitation (`finding-lint.mjs:51`).

## Architecture challenge

AR1 adds a third declaration plus mandatory nonempty `unexamined_ids`; this is unnecessary complexity for the immediate parser correction. The source already distinguishes packet validation from actual execution evidence (`skills/qore-review/references/findings.md:22-26`). Defer AR1–AR2 rather than silently combining them with strict parsing.

For the follow-up, challenge the claim that incomplete empty reviews should always use skipped. Counterexample hypothesis: a verifier starts, examines no claims because the packet is empty, then fails a required completion step. The nonempty-list requirement cannot represent that execution faithfully; A03 explicitly separates empty findings from completed required phases (`examples/validator-hardening.md:43-48`). Resolve whether partial means claim-subset coverage only or phase completion before locking syntax. Preserve Architecture's narrower interpretation as dissent; no new run status is justified now.

## Delivery challenge

T4's fresh build and manifest verification are justified if distributing changed hashed resources (`skills/qore-review/references/release.json:44-48`, cited by Delivery). Installing into another qualification project is not yet demonstrated necessary for exact-token rejection. Bound it to an explicit distribution smoke scenario, or defer installation while retaining build verification. The 1–2-hour estimate is an allowance, not measured effort.

## Competing proposals and open work

UX-D1's plain-text limitation and clearer blocker wording improve comprehension but change another observable contract. Defer formatting changes unless a separately accepted requirement demands them; preserve UX's recommendation as useful dissent. Recovery documentation can explain usage failure without changing output semantics.

Retain PD5–PD7 as future acceptance constraints: examined uncertainty differs from unexamined work, and partial progress must preserve confirmed blockers. Unfinished: exhaustive caller compatibility, final packaging gate, malformed-token regression execution and lead adjudication. No consensus or implementation readiness is claimed.
