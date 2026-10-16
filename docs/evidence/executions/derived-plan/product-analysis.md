# Product independent Analyze

Timestamp: 2026-10-15T20:01:05.854828+00:00. Role: Product; phase: fresh Analyze only. Workflow selected by existing applicable `examples/validator-hardening.md` (lines 4–8, 70). Target: `<CANDIDATE_B>`, supplied frozen snapshot `dec34e19b7b3036c213299a1f98b05fec1709212fb156eabf9928682024ae2cb` (identity supplied by lead; not independently reconstructed). No peer reports consumed; no implementation or package writes.

## Outcome and smallest useful scope

Propose **D4: reject malformed verifier declarations before deriving a review result**. Preserve existing D1–D3 and US1–US2 (`examples/validator-hardening.md:14–23`). A maintainer should not receive COMPLETE/SHIP because a malformed declaration was silently truncated. This is a concrete extension of the existing goal of distinguishing malformed packets and missing verification (`examples/validator-hardening.md:8`), not a replacement workflow.

Measured counterexample: an empty explicit findings envelope with `--verifier=ran=skipped --json` currently exits 0 and emits `verifier: ran`, COMPLETE, SHIP. Controls with exact `--verifier=ran` emit COMPLETE/SHIP and exact `--verifier=skipped` emit PARTIAL/PENDING. Full argv, cwd, input, stdout/stderr, exits and timestamps are retained in `product-commands.json`. Cause: `finding-lint.mjs:6–9` selects prefix declarations and extracts only `split('=')[1]`; lines 44–47 then derive coverage/verdict. This demonstrates malformed-input acceptance, not proof that any real independent verification was skipped.

**US3:** As a maintainer invoking the CLI manually or through automation, I need an invalid verification declaration rejected so a typing/assembly error cannot create a success result.

Acceptance proposals:
- **A04:** Given a valid empty envelope, when supplied `--verifier=ran=skipped` or `--verifier=ran=`, then exit 2 with usage diagnosis and no successful review JSON. Map US3/D4.
- **A05:** Given exact `--verifier=ran` or `--verifier=skipped`, when validation runs, then preserve existing result fields, exits, empty-envelope behavior and skipped severity handling. Map US1–US3/D1–D4.
- **A06:** Given missing, unknown or duplicate verifier declarations, when CLI validation runs, then retain refusal. Map US3/D4.

## Current evidence and constraints

Read complete derivative planning references: project-profile, protocol, roles, specification, run-evidence. Preflight ran before project fact consumption: exit 0, COMPLETE, no problems. Profile qore/0.1.0 digest `da03026c9f73a7771cc35aaaff898a3b970fed75362ebfd0c670068d6b23b3d9`. Source `project` is current `qore.json`, digest `948b2784fa7970cf90a25c338a29067b13d8b4476f666d712a5eb95fc6f641c8`.

Consumed returned fact **check** (`qore.json:4`): used exact declared argv `python3 -B -m unittest discover -s tests -v`, exit 0, 82 tests passed in 2.654s. Effect: regression gate for the proposed change; current green tests do not cover the measured malformed flag. Consumed **preserve-adaptations** (`qore.json:6`): staging/refusal invariant; effect: Delivery must plan new staging output and an existing-destination refusal gate, with no overwrite of installed adaptations. Review/UX facts and fixture were not selected by plan preflight and are not consumed as profile facts.

Inspected full finding-lint, redactor and validator tests. Existing coverage preserves empty results, malformed envelopes and skipped severity (`tests/test_validators.py:64–113`). Redactor allowlisting is already bounded (`redact-for-verifier.mjs:13–31`); no redactor redesign is necessary for D4. CLI documentation requires exact declared values (`skills/qore-review/SKILL.md:14`). The retained declaration limitation (`finding-lint.mjs:51`) must remain visible.

## Named peer questions and risks

**Architecture:** Can D4 use exact accepted-token membership at the existing parser boundary without a general CLI framework? What caller relies on suffix acceptance? Inspect actual callers before asserting no compatibility impact.

**Delivery:** Can the first increment stay within parser, focused CLI regressions and documentation, using fresh staging? Do not bundle execution-proof attestation, schema migration or UX tooling into this fix.

**QA/security:** Test malformed suffixes, duplicate flags, both exact controls and invalid-envelope interaction. Trigger: any malformed declaration still reaches result derivation; affected outcome is erroneous COMPLETE/SHIP.

Risk trigger: automation currently appends extra `=` segments; strict rejection changes that caller's outcome. Unknown prevalence; resolve with caller sweep, not assumed backward-compatibility. Another trigger is presenting exact `ran` as phase proof; preserve the existing limitation rather than expanding D4 into unverifiable attestation.

## Limits and unfinished scope

No exhaustive argument fuzzing, caller sweep, release manifest impact inspection or staging-refusal execution; no browser observation required for this local CLI proposal. No AGENTS.md returned by scoped file inventory. Parent instructions not exhaustively searched. Cross-examination/adjudication not yet performed. Product Analyze complete within budget; overall planning coverage remains pending the other roles and required phases.
