# A maintainer-operated review outside Qore

On 22 October 2026, the Qore maintainer used the generic review skill on the existing Swagger source specification for **POST `/user/find/userId`** in a separate repository under the same owner's administration: [sample.typescript.swagger.api at `ff222188`](https://github.com/sylvestre-baker/sample.typescript.swagger.api/tree/ff2221880142c0b085c0b858b22fe39e45a3be80).

This is an old sample project, not a newly recruited user or a current production service. The target was an existing API contract, not a seeded defect or a new specification written for this case. Qore's skill snapshot is from [`4a6ae96`](https://github.com/sylvestre-baker/qore-codex-skills/tree/4a6ae96a6f80618ac7bc6199e61b4e43f9a6b7bc/skills/qore-review); no project profile was used. [Snapshot manifests](review/snapshot.json) retain both identities and digest procedures: sorted relative paths and SHA-256 file digests, serialized as compact JSON with sorted keys, then hashed.

## Result and decision

**One medium source-level contract mismatch confirmed; zero plausible and zero refuted candidates after deduplication.** Correctness and feasibility independently proposed the same issue; their original reports remain available. Security returned no candidate within the bounded route scope. Zero refutations is a result, not a quality score.

The [declared 500 response](https://github.com/sylvestre-baker/sample.typescript.swagger.api/blob/ff2221880142c0b085c0b858b22fe39e45a3be80/src/modules/users/models/user.ts#L27) allows an optional string `message`. The database error travels unchanged through the store and service into `ResponseFailure`, then the controller passes that object to `send`. In an isolated execution of those actual method spans, injecting a native `Error` preserved the Error object as `message`. A separate `JSON.stringify` experiment produced:

```json
{"code":500,"error":"Internal Server Error","message":{}}
```

The string control conformed. The [fresh verifier's report](review/verifier.json), [first-party harness](review/verifier-reproduction.mjs), and [observations with hashes and extraction spans](review/verifier-reproduction.json) distinguish the source-level mismatch from unobserved HTTP behavior. The harness checks seven target file hashes before evaluating isolated methods. It loads no application constructors or configuration.

**Disposition:** map internal failures to a stable public string consistent with the contract; retain internal diagnostics privately. This case records a review decision, not a completed correction. No source patch, production incident, security exploit, or client failure is claimed.

## Actual phases

| Phase | Actual context and retained output |
|---|---|
| Correctness finder | Fresh `reuse_correctness` context; [complete report](review/finder-correctness.json) |
| Security finder | Fresh `reuse_security` context; [complete report and empty candidates](review/finder-security.json) |
| Feasibility finder | Fresh `reuse_feasibility` context; [complete report](review/finder-feasibility.json) |
| Mechanical redaction | Lead ran the bundled redactor on the saved [candidate envelope](review/findings.json); [filtered claims](review/claims.json) and [diagnostic](review/redaction.log) retained |
| Independent verification | Fresh `reuse_verifier` context received filtered claims and raw target; examined C1, no unexamined IDs; original full finder reports withheld |
| Findings validation | Bundled linter executed with `--verifier=ran --json`; [output](review/findings-lint.json) |

All three requested finders returned; [roster and duplicate mapping](review/roster.json) are retained. Contexts were started without parent conversation history. Filtering removed separate rationale fields; the claim hypothesis remained visible in allowed evidence text. [Execution record](execution.json) and identity-bound phase artifacts record **COMPLETE coverage of these six bounded review phases**. The structural checker verifies declared identities and evidence, not the truth of conclusions or actual independence by actor labels alone.

## Reproduce the observation

Requirements: Git, Node.js, and a local checkout of this evidence directory. No dependency installation, Qore account, server, database, token or network request to an application is required. The initial clone fetches public source; use a new temporary directory:

```sh
qore_case_root="$(mktemp -d "${TMPDIR:-/tmp}/qore-contract.XXXXXX")"
git clone https://github.com/sylvestre-baker/sample.typescript.swagger.api.git "$qore_case_root/target"
git -C "$qore_case_root/target" checkout --detach ff2221880142c0b085c0b858b22fe39e45a3be80
node docs/evidence/maintainer-reuse/review/verifier-reproduction.mjs "$qore_case_root/target"
```

Run the last command from Qore's repository root. It rejects changed pinned source files and writes observations to standard output. It evaluates selected method spans after removing TypeScript type syntax, with offline DB/JWT/telemetry/response stubs. This is not a compiled integration test or an execution of the complete application.

To check the retained review structure from Qore's repository root:

```sh
node skills/qore-review/scripts/finding-lint.mjs docs/evidence/maintainer-reuse/review/verifier.json --verifier=ran --json
python3 skills/qore-review/scripts/run-check.py docs/evidence/maintainer-reuse/execution.json --evidence-root docs/evidence/maintainer-reuse
```

## Limits and provenance

Actual Express HTTP bytes, generated Swagger JSON, installed dependency versions, real MongoDB behavior, runtime performance and a final client consumer were not verified. The verifier confirmed the Error/send-argument boundary and local ECMAScript serialization only. A schema-consuming client could be affected; no actual client rejection was observed. The scope excludes the other endpoints and any repository-wide security assessment.

This demonstrates one bounded reuse beyond Qore. It does not establish independent adoption, current ecosystem demand, measured productivity gain, or superiority to a simpler review. The operator remains Qore's maintainer; the four agent contexts are not four independent human users. A maintainer-led external trial remains future work, conditional on participation and publication permission.

Public files are selected first-party reports, a first-party reproduction harness and manifests; the target implementation and private conversation/tool transcripts are not copied into this case. Source links are pinned. Full finder files and the verifier are retained without substantive edits; phase wrappers add identity metadata after the actual work. The Qore repository's MIT license covers these first-party artifacts, without asserting new licensing rights over the target repository.
