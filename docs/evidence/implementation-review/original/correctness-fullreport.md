# Correctness finder raw report

Role: independent correctness finder, no peer findings read. Target: complete current source at /workspace/implementation-target/qore-skills-0.1.0; supplied candidate archive identity 17888fa30f1024707fc3ee6efda856ca330bc6365e09737007096f5d7db62da8. Source was not edited. All findings are candidates for fresh independent verification, not self-confirmed or self-refuted.

## Reviewed scope

Read README.md; docs/contracts.md, profiles.md, architecture.md; all three schemas; tools/qore.py, context.py, run_contract.py; method protocols; review findings/project-profile/run-evidence; plan specification; all five JavaScript validators/redactor/stop scripts; tests/test_run_contract.py in full and relevant test_package.py/test_validators.py cases. Enumerated all methods, scripts, references and fixtures. Executed complete 90-test suite and external-temp counterexamples. Reviewed build/derive/install/compare control paths, source freshness filtering, rights inventory assembly, contained paths, phase identity envelopes, method independence declarations, stop precedence, real scenario parsing, and output contracts.

## Boundary trace: profile identity

Producer derive() reads input bytes via read_json(profile_path), yielding fields schema,id,version,sources,commands,invariants,surfaces and any preserved extras. validate_profile accepts sourced facts and emits schema,profile{id,version},method,coverage,sources{id,path,expected_sha256,actual_sha256,current},commands,invariants,surfaces,consumed_source_ids,problems. CLI/checker adds profile.sha256 from the actual checked file.

Storage/serialization: derive constructs profile_info{id,version,sha256=digest(original file)}; write_json serializes parsed profile with indent=2, ensure_ascii=False and newline into each references/project.json. finalize writes the original profile_info into root manifest and standalone release metadata; inventory separately hashes the normalized bundled profile. verify checks resource inventory hashes but does not compare profile_info.sha256 to bundled project.json. The receiver is bundled project-check.py, which hashes its normalized file and reports that hash. Final consumer is method preflight/run evidence, which requires the exact consumed bundled profile digest. Adjacent producer/serializer/consumer identities differ for perfectly valid differently formatted profiles (C-001). This is an observed byte-level mismatch, not an assumption that a query transmits a value.

## Candidates

### C-001 — Derivation records the input profile digest but rewrites the bundled profile bytes

Impact: medium.

tools/qore.py:215 records profile_info.sha256 = digest(profile_path), but tools/qore.py:235 writes references/project.json through write_json (indent=2, ensure_ascii=False, trailing newline). With compact JSON of profiles/qore.json, derive succeeds and manifest profile.sha256 is 63c9157e3dd4d6eb2c33c899820422e8ce1d1bee9cc4e22c1df96d814e50a83f, while bundled references/project.json and its successful bundled project-check.py report da03026c9f73a7771cc35aaaff898a3b970fed75362ebfd0c670068d6b23b3d9. /workspace/implementation-review/evidence/correctness-probes.txt retains output; /tmp/qore-correctness-zihl6vcs contains inputs/derivative.

Trigger: A valid maintained profile uses different JSON whitespace, Unicode escaping, or trailing newline from write_json.

Consequence: Release/profile identity and runtime preflight identify different byte snapshots; consumers cannot use release profile.sha256 to attest the exact consumed profile required by run-evidence.md.

Counterexample: Serialize profiles/qore.json with json.dumps(profile,separators=(comma,colon)); derive using current root into unused external temp; compare returned profile.sha256 and SHA-256 of qore-review-qore/references/project.json. Actual different hashes despite verify success. Expected released profile identity to identify the actual consumed bundled bytes or explicitly distinguish source_profile_sha256 from bundled profile sha256.

Uncertainty: Independent verification has not yet run; semantic profile facts remain unchanged.

### C-002 — Unchanged failing gates bypass the promised three-comparison plateau stop

Impact: low.

skills/qore-ux-review/scripts/stop-rule.mjs:84 checks stuck >= 2 before plateau >= 3 at line 85. Four measured iterations n=1..4 with G1=3 return decision CHANGE_APPROACH, stuck_count=3, no_improve_count=3 rather than STOP_PLATEAU. skills/qore-ux-review/references/protocol.md says after three comparisons without improvement the loop stops at plateau. Input /tmp/qore-correctness-zihl6vcs/plateau.json; output correctness-probes.txt.

Trigger: A nonzero failing gate stays unchanged through four or five measured iterations.

Consequence: The consumer is instructed to continue investigation instead of stopping at its declared plateau budget; the six-iteration ceiling still bounds eventual execution.

Counterexample: node skills/qore-ux-review/scripts/stop-rule.mjs /tmp/qore-correctness-zihl6vcs/plateau.json returns CHANGE_APPROACH at iteration 4, although three unchanged comparisons have completed.

Uncertainty: Independent verification has not yet run; severity limited by functioning six-iteration ceiling.

### C-003 — Spec validation counts literal docstring text as executable acceptance steps

Impact: medium.

skills/qore-plan/scripts/spec-lint.mjs:44-48 scans every Gherkin line for Given/When/Then without tracking docstrings. /tmp/qore-correctness-zihl6vcs/docstring-spec.md has one real Given step and When/Then solely inside its triple-quoted argument. node spec-lint.mjs FILE --json exits 0 with valid:true and no problems. The artifact contract requires real acceptance scenarios with their own Given, When, Then. An additional Scenario Outline using placeholders without Examples also exits 0 (/tmp/qore-correctness-zihl6vcs/outline-spec.md).

Trigger: An acceptance scenario contains step-looking multiline input or an outline lacks Examples.

Consequence: The mandatory structural validation phase can pass a specification with no actual action/assertion acceptance steps, undercutting the documented real-Gherkin boundary.

Counterexample: Run node skills/qore-plan/scripts/spec-lint.mjs /tmp/qore-correctness-zihl6vcs/docstring-spec.md --json. Actual valid:true; expected rejection because literal argument text contains the only When and Then.

Uncertainty: Independent verification has not yet run; no external Gherkin package was installed, grammar distinction follows standard docstring syntax and repository real-step requirement.

## Actual commands/results

- Initial `rg` unavailable; used find, cat, sed, nl. This did not block source reads.
- `python3 -m unittest discover -s tests`: exit 0; Ran 90 tests in 1.818s; OK. These tests do not cover the reproduced profile serialization identity mismatch, plateau precedence or Gherkin literal-text cases.
- External probe imported tools/qore.py with sys.dont_write_bytecode=True; created /tmp/qore-correctness-zihl6vcs; wrote compact profile via json.dumps(json.loads(Path("profiles/qore.json").read_text()), separators=(",",":")); qore.derive(source,Path.cwd(),temp/"derived") succeeded; ran generated qore-review-qore/scripts/project-check.py references/project.json --root current-root --method review; exit 0, exact digest mismatch retained in correctness-probes.txt.
- `node skills/qore-ux-review/scripts/stop-rule.mjs /tmp/qore-correctness-zihl6vcs/plateau.json`: exit 0; CHANGE_APPROACH, DO-NOT-SHIP, COMPLETE, stuck_count=3, no_improve_count=3. Input contains in_scope=[G1], four measured G1=3 iterations n=1..4.
- `node skills/qore-plan/scripts/spec-lint.mjs /tmp/qore-correctness-zihl6vcs/docstring-spec.md --json`: exit 0, valid:true, A01, problems:[] despite only one actual Given step and When/Then in triple-quoted argument. Minimal artifact contains required schema marker, Gherkin fence, coverage A01 -> US1 / D1 and Mermaid sequenceDiagram.
- Same command for outline-spec.md: exit 0, valid:true despite placeholder Scenario Outline lacking Examples. Raw input files remain available in the named temp directory; complete actual outputs in correctness-probes.txt.

## Limits and unfinished scope

No external service, credentials, installation, messages, live writes or native apps used. Private historical inputs and external-program acceptance excluded. No browser execution or claims about browser behavior. Did not independently rebuild supplied archive in this finder; target identity supplied by lead. Did not exhaustively test filesystem races, interruption rollback, malformed types, profile semantic fidelity, all resource provenance statements, Python/shell dynamic runtime import closure, full bundled scripts copy equality or all documentation command examples. Did not inspect every evidence media artifact. Run checker structurally validates declarations and explicitly does not prove real independent execution; opaque payload acceptance alone was not promoted into a candidate because this limitation is documented. Resource inventories/rights attestations were inspected structurally, not treated as ownership proof.

Finder coverage PARTIAL due bounded four-minute budget. Three candidate findings returned; no confirmation/refutation attributed to this finder. Fresh verifier must examine IDs C-001,C-002,C-003. Final method coverage, role roster and verifier execution belong to lead's run record.
