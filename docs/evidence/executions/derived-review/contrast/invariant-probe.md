# Direct relevant invariant probe

Observed at: 2026-10-15T20:06:10.138496+00:00.

Working directory: `/workspace/implementation-target/qore-skills-0.1.0/.agents/skills/qore-review-qore-contrast`.

Actual argv (executed as an argument vector, without shell interpolation):

```json
[
  "node",
  "scripts/finding-lint.mjs",
  "/workspace/current-profile-contrast-review/synthetic-input.json",
  "--verifier=skipped",
  "--json"
]
```

Exit status: 0.

Complete stdout:

```text
{
  "valid": true,
  "coverage": "PARTIAL",
  "verdict": "PENDING",
  "verifier": "skipped",
  "total": 1,
  "counts": {
    "CONFIRMED": 0,
    "PLAUSIBLE": 1,
    "REFUTED": 0
  },
  "blocking_findings": [],
  "findings": [
    {
      "id": "PROBE-HIGH",
      "title": "Synthetic unverified high candidate for consumer probe",
      "severity": "high",
      "verdict": "PLAUSIBLE",
      "evidence": "examples/validator-hardening.md:41",
      "unresolved": "Independent verification intentionally outside this focused probe."
    }
  ],
  "problems": [],
  "limit": "The verifier flag records an execution declaration; validate actual independent phase evidence separately."
}
```

Complete stderr:

```text
```
