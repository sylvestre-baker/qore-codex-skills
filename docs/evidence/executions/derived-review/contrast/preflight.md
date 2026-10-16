# Freshness preflight

Observed at: 2026-10-15T20:05:41.559235+00:00.

Working directory: `/workspace/implementation-target/qore-skills-0.1.0/.agents/skills/qore-review-qore-contrast`.

Actual argv (executed as an argument vector, without shell interpolation):

```json
[
  "python3",
  "scripts/project-check.py",
  "references/project.json",
  "--root",
  "/workspace/implementation-target/qore-skills-0.1.0",
  "--method",
  "review"
]
```

Exit status: 0.

Complete stdout:

```text
{
  "schema": "qore-context-check/1",
  "profile": {
    "id": "qore-contrast",
    "version": "0.1.0",
    "sha256": "f72394c2ebb80cb6da41b33a088d56fbd24b4577f71bc2b022d0ef4bb36bfb88"
  },
  "method": "review",
  "coverage": "COMPLETE",
  "sources": [
    {
      "id": "project",
      "path": "tests/fixtures/project-alternate.json",
      "expected_sha256": "830dc3c50369c21f523a1c68b188f3013b40c439ea362a1e97c45a38a89a79c5",
      "actual_sha256": "830dc3c50369c21f523a1c68b188f3013b40c439ea362a1e97c45a38a89a79c5",
      "current": true
    }
  ],
  "commands": [
    {
      "id": "check",
      "argv": [
        "python3",
        "-B",
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests",
        "-p",
        "test_validators.py",
        "-v"
      ],
      "source": "project",
      "applies_to": [
        "plan",
        "review"
      ]
    }
  ],
  "invariants": [
    {
      "id": "contrast-review",
      "statement": "A high-severity candidate without independent verification stays PLAUSIBLE and does not become a verified blocker.",
      "source": "project",
      "applies_to": [
        "review"
      ]
    }
  ],
  "surfaces": {},
  "consumed_source_ids": [
    "project"
  ],
  "problems": []
}
```

Complete stderr:

```text
```
