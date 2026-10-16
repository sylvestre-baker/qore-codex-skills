# Independent feasibility finder report

Role: performance/feasibility. Target: complete current Qore source, user candidate identity `17888fa30f1024707fc3ee6efda856ca330bc6365e09737007096f5d7db62da8`. No peer findings read. Source remained unedited. All probe writes were external temporary/evidence directories. No installs, credentials, external services, browser/native actions, or live writes.

This is finder evidence, not independent verification. Candidates below are neither self-confirmed nor self-refuted.

## Reviewed scope

Read README.md; docs/contracts.md, profiles.md, architecture.md; schemas/qore-run.schema.json and qore-release.schema.json; tools/qore.py, context.py, run_contract.py; all three SKILL.md entrypoint/protocol material (review under .agents copy); review findings and project-profile contracts; plan run-evidence; UX evidence/stop protocol; spec-lint.mjs, finding-lint.mjs, redact-for-verifier.mjs, depth-lint.mjs and stop-rule.mjs. Inspected test_run_contract.py and test fixtures; executed the full existing test suite. Compared tools/context.py and run_contract.py to review bundled project-check.py/run-check.py with cmp; both comparisons exited 0.

Reviewed immutable destination refusal, source containment, release and skill inventories, rights metadata flow, profile applicability/freshness filtering, evidence descriptors/envelopes, required method phase coverage, and iteration ceiling/freshness logic by source inspection. No large-data benchmark was justified for the small local package; no performance improvement or comparative cost claim is assessed.

## Boundary trace: profile SHA-256

Producer: derive reads profile bytes via read_json (schema/id/version/sources/commands/invariants/surfaces; source facts validated for all three methods). At tools/qore.py:215 it emits `profile_info={id,version,sha256:digest(input_path)}`.

Storage/serialization: line 235 writes each parsed profile through write_json using indent=2, ensure_ascii=False and trailing newline. finalize writes release metadata fields `schema,version,kind,host,profile,redistribution,resources`; standalone metadata emits `schema,version,host,profile,redistribution,resources`. Each profile is thus stored with normalized bytes while metadata retains original-input digest.

Receiving contract: verify checks release schema/kind/host/version/redistribution, resources and digests, standalone metadata and local resource closure. It does not compare profile metadata sha256 to references/project.json bytes. Profile preflight then reads the bundled profile and emits `schema,profile:{id,version,sha256},method,coverage,sources,commands,invariants,surfaces,consumed_source_ids,problems`. The `sha256` is the actual copied file digest in context.py:145.

Final consumer: project-profile.md requires retaining exact checker profile SHA and fact use; run-evidence.md identifies run.profile as the exact consumed bundled profile. That consumer accepts `{id,version,sha256}`, while the assembly producer has used the same field for original differently serialized input bytes. F-1 records the concrete adjacent boundary mismatch. The method facts remain semantically equivalent; identity consistency is the issue.

## Candidate findings

### F-1 — medium: Derived release profile identity hashes the input bytes rather than the bundled profile

Evidence: tools/qore.py:215 records digest(profile_path), but line 235 calls write_json on the parsed profile. With the compact valid profile saved as feasibility-compact-profile.json, derive succeeds and verify returns valid, while manifest profile.sha256 is 63c9157e3dd4d6eb2c33c899820422e8ce1d1bee9cc4e22c1df96d814e50a83f and bundled references/project.json / runtime checker profile.sha256 is da03026c9f73a7771cc35aaaff898a3b970fed75362ebfd0c670068d6b23b3d9. See feasibility-derive-result.json and feasibility-project-check-result.txt.

Trigger: Input profile JSON uses a valid serialization different from write_json(indent=2, ensure_ascii=False) plus newline.

Consequence: A successfully verified derivative advertises a different profile digest from the exact bundled profile consumed at runtime; consumers cannot reconcile release identity with preflight/run evidence using the claimed exact profile digest.

Uncertainty: The verifier must decide whether release profile.sha256 is intended as source-input identity only; current runtime/run docs describe the exact consumed bundled profile and no distinct source-vs-bundled identity fields exist.

### F-2 — medium: Findings gate accepts CONFIRMED lower-severity findings without the required counterexample

Evidence: skills/qore-review/references/findings.md:18 requires counterexample support for CONFIRMED, and :26 says validation checks verdict obligations. scripts/finding-lint.mjs:40 applies that obligation only to critical/high. The saved feasibility-medium-without-counterexample.json has a medium CONFIRMED finding and no counterexample; node finding-lint.mjs INPUT --verifier=ran --json exits 0 and emits valid:true, coverage:COMPLETE, verdict:SHIP. See feasibility-medium-lint-result.txt.

Trigger: A verifier packet labels a medium, low, or info finding CONFIRMED without a counterexample field.

Consequence: The final structural gate reports a contract-invalid confirmed packet as valid, losing required reproducibility support for nonblocking findings.

Uncertainty: This is a structural obligation mismatch; it does not claim the checker can prove that reproduction actually occurred, nor that a medium finding should block delivery.

## Procedures and raw results

1. Ran `python3 -m unittest discover -s tests -v`: 90 tests ran in 1.959 seconds, exit 0, OK. This is regression execution, not independent phase or factual-quality proof.
2. Created external `/tmp/qore-feasibility-wx44k6_1/compact.json` by parsing profiles/qore.json and serializing with `json.dumps(p,separators=(',',':'))`. Called `qore.derive(compact_path, Path('.'), temp/'derived')` through tools/qore.py's actual functions. Success with valid verify result. Saved exact compact input and derive result in evidence.
3. Computed digest of generated review references/project.json: `da03026c9f73a7771cc35aaaff898a3b970fed75362ebfd0c670068d6b23b3d9`, versus returned profile input identity `63c9157e3dd4d6eb2c33c899820422e8ce1d1bee9cc4e22c1df96d814e50a83f`. Actual generated runtime checker command and full output are retained in feasibility-project-check-result.txt.
4. Saved medium CONFIRMED packet without counterexample and ran actual final findings checker. Exact command, exit code and complete output retained in feasibility-medium-lint-result.txt.

## Unreviewed scope and limits

Did not execute full planning/review/UX methods on a second target, install the package into an independent host, benchmark large files or resource exhaustion, or independently validate ownership attestations. No private historical client inputs or external acceptance criteria were considered. Did not inspect every schema field/test branch or every reference in depth; reviewed source/control boundaries above within the worker budget. This finder report is PARTIAL scope coverage and must pass mechanical filtering and a fresh verifier before any confirmed/refuted conclusions. Returned role: feasibility only; requested broader review roles belong to the lead's roster. Unexamined items are explicit rather than interpreted as zero findings.
