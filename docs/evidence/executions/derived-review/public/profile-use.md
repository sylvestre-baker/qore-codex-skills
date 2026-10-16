# Consumed source and fact mapping

Only the bundled qore profile was consumed. Public facts are confined to this output directory; no neighboring profile was used.

Source ID: project. Current path: qore.json. Current SHA-256: 948b2784fa7970cf90a25c338a29067b13d8b4476f666d712a5eb95fc6f641c8. The current file was read after successful preflight and supports both selected facts directly.

| Fact | Selected | Actually consumed | Effect |
| --- | --- | --- | --- |
| check | Yes | Yes | Executed its exact argument vector from the project root; 90 tests passed, exit 0. This replaced any assumed validation command. |
| verified-blockers | Yes | Yes | Evaluated A02 and D2/D3 of examples/validator-hardening.md against current bundled implementation and synthetic executions. Preserved severity, distinguished verified blocking from impact, and kept full review coverage PARTIAL because independent verification was outside this probe. |

The example source is examples/validator-hardening.md, with A01 malformed envelope, A02 unverified high severity, and A03 valid empty packet with actual phase evidence. The implementation consumer is the derivative's scripts/finding-lint.mjs, byte-identical to skills/qore-review/scripts/finding-lint.mjs. Tests in tests/test_validators.py exercise the generic current implementation; direct probes exercise this derivative's bundled implementation. Digests and retained source copies establish the actual bytes.

Trace: qore.json declarations → bundled profile source binding → fresh checker selected facts → exact project command and invariant-specific inputs → validator's findings/severity/verdict, blocking_findings, coverage and decision fields → this report. No assumption that a declaration proves actual independent phases crosses the final boundary.
