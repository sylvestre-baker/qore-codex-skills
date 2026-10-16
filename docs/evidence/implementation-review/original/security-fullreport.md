# Independent security finder — raw report

Target: complete current source at /workspace/implementation-target/qore-skills-0.1.0. Supplied candidate identity: 17888fa30f1024707fc3ee6efda856ca330bc6365e09737007096f5d7db62da8. No peer reports accessed. No source edits, installs, credentials, paid services, external messages, native interfaces, or live application writes.

## Candidate S-1 (medium)

Inherited object properties can satisfy missing UX measurements. See security-candidates.json for the full candidate and security-counterexamples.json for the actual external-temp-file command and complete output. The reproduced packet declares toString required but has empty scores and measured arrays. The script returns SHIP / COMPLETE, with no missing gate. Expected: refuse unknown gate identifiers, or mark the unmeasured required gate missing. The central issue is untrusted dictionary keys crossing into ordinary JavaScript objects and using inherited values as observation state. Impact is scoped to malformed/adversarial gate names; valid ordinary gate names were not shown affected. This is candidate evidence, not independent confirmation.

## Required producer-to-consumer boundary trace

Value traced: required UX gate identity and measurement freshness.

Producer: the method operator writes loop JSON according to skills/qore-ux-review/references/evidence.md. Actual persisted reproduction fields: top-level in_scope and iterations; each iteration emits n, scores, measured. No measurements are emitted. Documented optional fields include fix_applied, skipped, infra_blocked, not_applicable, g6_passed.

Receiving contract: stop-rule.mjs JSON.parse reads that exact file. Lines 11-18 accept arbitrary unique nonempty strings as in_scope entries, measured/blocked lists drawn from that scope, and omission reason maps. It does not restrict required identities to the protocol's G0-G6 and GP domain.

Storage: line 22 allocates measuredAt={} and measuredScores={}. These objects already expose inherited toString. The measurement loop at lines 47-52 runs zero times for the actual packet. No own timestamp or own score is stored.

Next boundary: lines 59-61 consume dictionary reads without own-property tests. The inherited function is unequal to undefined, and numeric comparisons against it are false. Therefore missing=[], stale=[], failing=[]; covered becomes true. This differs from the preceding boundary, which emitted no observed gate records.

Final consumer/output: lines 76-94 serialize decision, verdict, coverage, iteration, ceiling, surface_score, consecutive_fresh_passes, passes_required, lowest_failing_gate, failing_gates, stale_gates, missing_gates, skipped, infra_blocked, not_applicable, stuck_count, no_improve_count, limit. Actual file output says SHIP/COMPLETE. Protocol instructs the operator to use this decision after each iteration and repair conflicts rather than route around it. No further application runtime consumer is established; this report does not infer one.

## Reviewed scope

Read README.md, docs/contracts.md, docs/profiles.md, docs/architecture.md; qore-review findings contract; all three method protocols; tools/qore.py, tools/context.py, tools/run_contract.py; review redaction and finding-lint; UX stop-rule and depth-lint; planning spec-lint; UX evidence format; qore-run schema; tests/test_run_contract.py. Enumerated all skill resource paths. Checked release inventory/rights/verification code, contained source/evidence paths, immutable derivation/install behavior, profile applicability/current-source checks, evidence header/descriptor matching and phase independence declarations. The code explicitly limits factual quality and truthful role declarations, so no candidate is asserted merely because a fabricated payload can be wrapped in matching metadata.

Runtime exercise: one focused Node counterexample, saved in an external /tmp/qore-security-* directory, with command, exit code, input and stdout retained. No external browsing was necessary for this standard-library-only local trust-boundary examination; no third-party dependency vulnerability is claimed.

## Unreviewed scope and limits

Coverage PARTIAL due to bounded finder time. Did not exhaustively read package/validator regression suites, release/project JSON schemas, all duplicated installed helper copies, execution evidence references, rights/provenance record contents, browser assets, or all actual historical consumers. No broad tests run. Did not exercise concurrent TOCTOU updates, filesystem races, platform portability, or native/browser behavior. Private historical client inputs and external-program acceptance excluded as directed. No independent verifier or final adjudication performed by this finder. One candidate returned, no self-confirmed or self-refuted candidates.
