# Independent correctness finder report

Requested role: correctness finder. Returned role: correctness finder. Actual actor ID: /root/correctness.

Scope: examples/validator-hardening.md against skills/qore-review/scripts/{finding-lint,redact-for-verifier}.mjs, their .agents copies, tests/test_validators.py, qore.json, and the assigned protocol/findings references. No peer reasoning was supplied or read. No source files were edited. No authentication files were read.

Target snapshot: examples/validator-hardening.md SHA-256 6f25b2edcd6d0826b12fbb47a99fc4162a1089eef71eaf7f16ea2cb7a8239a87. The directory has no Git metadata; git rev-parse HEAD and git status --short returned 128, so content hashes identify this snapshot. Both script pairs compare byte-identical (cmp exit 0).

## Candidate findings

Zero candidates. The scoped acceptance scenarios are supported by implementation and bounded executions. This is a discovery result, not an independent verifier verdict or a declaration that the whole review is complete.

A01: actual file containing {} yielded exit 1, valid false, coverage PARTIAL, verdict INVALID in both validator copies. Envelope failure cannot become an empty complete review.

A02: actual file containing one high PLAUSIBLE candidate, evidence src/input.ts:12, and --verifier=skipped yielded exit 0, retained high severity and PLAUSIBLE verdict, coverage PARTIAL, verdict PENDING, and no blocking findings in both copies. The supplied regressions separately cover critical severity and rejection of CONFIRMED/REFUTED with skipped verification.

A03: actual file containing {"findings": []} with --verifier=ran yielded exit 0, coverage COMPLETE, verdict SHIP in both copies. This is consistent with the document's express limitation: the declaration alone does not prove phase execution. The validator emits that limitation in its result, and the document directs the maintainer to inspect run evidence separately. I did not treat a CLI declaration as observed independent verification.

## Mandatory boundary trace

Central value: severity high on trace-1. Producer: an external Python test harness writes a JSON file using json.dumps with fields id, title, severity, evidence, verdict, rationale. Storage is an external /tmp/qore-correctness-* directory; tests use the real Node public entry points, with no repository fixture mutation.

First receiving contract: redactor JSON.parse reads the object with findings array, checks object elements, requires unique nonempty id, nonempty title/evidence and known severity. Its emitted envelope has only findings; each emitted finding contains id, title, severity, evidence, and optional counterexample when present. For this actual case the emitted fields were exactly id, title, severity, evidence. It dropped verdict and rationale, recorded the dropped field names on stderr, and retained high unchanged. The harness wrote the actual stdout to claims.json and re-read it; it did not reconstruct the claim from a comment or source query.

The verifier-stage surrogate adds verdict PLAUSIBLE to that deserialized claim and writes final.json via json.dumps. This exercise checks serialization and receiving behavior; the surrogate is not an independent verifier. The final linter requires id/title/severity/verdict/evidence for this non-refuted case, accepts known severities and the three known verdicts, and with --verifier=skipped permits only PLAUSIBLE. REFUTED instead requires refuted_because; confirmed high/critical also require counterexample. Optional/extra properties are retained rather than stripped by this linter.

The final stdout JSON fields actually emitted are valid, coverage, verdict, verifier, total, counts, blocking_findings, findings, problems, limit. The harness parses the actual stdout; final consumers see severity high within findings, coverage PARTIAL, verifier skipped, verdict PENDING, and empty blocking_findings. The adjacent boundaries match the documented two-stage workflow: redactor intentionally removes verdict, and a later stage supplies it before final validation. No mismatch affecting A01–A03 was observed. Counterexample is optional in the redactor and required by the final linter for confirmed high/critical claims, consistent with this target's verified-blocker behavior.

## Executed checks and limits

The exact qore.json check, python3 -B -m unittest discover -s tests -v, returned 0: 85 tests, OK. It was run twice; the fully recorded invocation and all dedicated CLI invocations, exit statuses, stdout, and stderr are in correctness-commands.json. Dedicated packets and intermediate files were written only to an external temporary directory and removed after execution. cmp checks returned 0 for both packaged/local script pairs.

Unfinished scope: none within the assigned correctness check of this document's three scenarios. No exhaustive fuzzing, external research, browser work, security assessment, or independent claim-verification phase was performed by this finder. Other repository behavior is outside this report even though the declared check runs the complete suite. The candidate envelope contains zero findings and no self-assigned verdicts. Requested/returned role coverage for this worker is correctness/correctness only; overall three-finder and fresh-verifier execution coverage belongs to the lead's run record.
