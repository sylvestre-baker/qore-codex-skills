# Contracts and validators

Qore separates context, package integrity, method artifacts, and execution evidence. A structural check is useful evidence for its stated contract; it does not prove factual quality or grant delivery permission.

## Versioned records

| Contract | Purpose | Reference |
|---|---|---|
| `qore-project/1` | Bind project commands, invariants, and surfaces to source IDs and digests. | [Schema](../schemas/qore-project.schema.json), [profile guide](profiles.md) |
| `qore-release/1` | Identify candidate/core/profile/host metadata and the explicit resource inventory with digests and redistribution information. | [Schema](../schemas/qore-release.schema.json), [assembler](../tools/qore.py) |
| `qore-run/1` | Record candidate/target identity, environment, actual phases, artifacts, commands, freshness, coverage, and limitations. | [Schema](../schemas/qore-run.schema.json), [run checker](../tools/run_contract.py) |

The implemented validators are the operational checks. Use them alongside the schemas rather than inferring successful execution from a JSON shape.

## Local command reference

Run these from the repository root. Paths below identify your actual inputs; generated output destinations must be unused.

| Command | Effect |
|---|---|
| `python3 tools/qore.py build --output STAGING` | Copy the release allowlist, create and verify a versioned candidate folder, and write its ZIP. |
| `python3 tools/qore.py verify BUNDLE` | Compare declared resources, contained paths, and current file digests, including standalone skill inventories. |
| `python3 tools/qore.py derive --profile PROFILE --project-root ROOT --output STAGING` | Validate current sourced facts for all three methods and generate project-bound skill folders. It does not execute profile commands. |
| `python3 tools/qore.py install --source BUNDLE --project-root ROOT` | Verify the candidate and copy three skills into the project's `.agents/skills/`; refuse existing destinations. |
| `python3 tools/qore.py compare --source BUNDLE --project-root ROOT` | Report installed/candidate divergence and local adaptations without writes. |
| `python3 tools/qore.py snapshot --root ROOT` | Produce a file inventory and aggregate SHA-256 for the selected snapshot, excluding the tool's declared generated/runtime directories. |
| `python3 tools/qore.py validate-run RUN --evidence-root EVIDENCE` | Validate declared phase coverage and identity-bound evidence files. |
| `python3 tools/context.py PROFILE --root ROOT --method plan` | Return fresh facts applicable to one method; `review` and `ux` are the other method values. |

An exit status of zero establishes that the command's structural check passed. Inspect the returned coverage and limitations as well. A nonzero result retains a diagnostic; it never means an empty successful review. `verify` accepts the extracted candidate directory, not the ZIP path.

## Method artifacts

These commands run from the corresponding skill directory; installed derivatives contain their own copies. Use absolute artifact paths so the skill directory and target project cannot be confused.

| Method | Validator | Contract |
|---|---|---|
| Plan | `bash scripts/spec-lint.sh SPEC.md` | First-line `qore-spec/1`, actual fenced Gherkin scenarios and steps, coverage IDs, and a runtime sequence diagram. [Detailed format](../skills/qore-plan/references/specification.md). |
| Review | `node scripts/redact-for-verifier.mjs FINDINGS.json` then `node scripts/finding-lint.mjs VERIFIED.json --verifier=ran --json` | Strict findings envelope, mechanical claim filtering, evidence and verdict obligations. Use `--verifier=skipped` when the separate verifier did not run. [Detailed format](../skills/qore-review/references/findings.md). |
| Web UX | `node scripts/depth-lint.mjs DEPTH.json` and `node scripts/stop-rule.mjs LOOP.json` | Declared depth, required gates, actual measurements, omissions, correction freshness, and bounded stopping. [Detailed format](../skills/qore-ux-review/references/evidence.md). |

The review filter's standard output is the verifier's claims file. Save it as a file before starting the fresh verifier; an intention to redact is not mechanical filtering. A valid unverified high-severity concern stays PLAUSIBLE and non-blocking, with PARTIAL review coverage. Do not downgrade its impact to clear a validator.

## Execution evidence and coverage

A run identifies the exact candidate, target snapshot, environment/operator category, optional profile, required phases, actual actors, commands, and limitations. Artifacts have contained relative paths and SHA-256 digests. Executed phase artifacts carry matching `qore_evidence` identity metadata and their actual output payload. Their observation times must be after the last relevant change; rewrapping older proof does not make it fresh.

Every PASS phase references matching execution evidence. A source file or presentation alone cannot prove a finder, verifier, browser action, or other phase ran. Actor labels constrain declarations but do not themselves prove context isolation. Compare requested roles with returned complete reports.

| Coverage | Meaning |
|---|---|
| COMPLETE | Required phases have current evidence, with only explicitly permitted and justified non-applicability. |
| PARTIAL | Useful work completed, but a required phase/check is missing, skipped, unfinished, or stale. |
| BLOCKED | Required execution could not proceed; the cause and resumption path are recorded. |

Coverage differs from the target verdict. A review can complete and find a blocker. A web check can establish DO-NOT-SHIP. A passing findings structure can coexist with missing independent verification. A SHIP label never authorizes publication, merge, or deployment.

For method-specific phase IDs and exact run fields, read the bundled execution reference for [plan](../skills/qore-plan/references/run-evidence.md), [review](../skills/qore-review/references/run-evidence.md), or [UX](../skills/qore-ux-review/references/run-evidence.md). Qualification evidence must also match the instruction revision and actual claimed scope.

Resource closure checks cover inventories, contained Markdown references and literal JavaScript runtime imports or remote fetches. They are combined with source review and actual helper execution; they are not a universal analyzer of dynamic code. Python/Node/Bash and observed Codex facilities remain documented host prerequisites. Explicit project inputs and authorized web targets remain outside each autonomous skill. The 0.1.0 package version pins the first-party core and Codex adaptation together; actual host runtime versions belong to the execution record.
