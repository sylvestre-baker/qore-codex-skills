# Consumed project facts and review effect

Only qore-review-qore-contrast's bundled profile was used. Its project preflight completed before project commands or invariants were selected. The raw profile was read as data first; current checker output then supplied the facts. No neighboring profile, previous public execution result, credential or web state was consumed.

| Fact | Selected by current checker | Actually consumed | Current supporting source | Effect |
|---|---|---|---|---|
| command `check` | Yes | Yes | source `project`, `tests/fixtures/project-alternate.json`, key `check` | Executed the exact unittest argv, rather than selecting a command from memory or another profile. All 35 tests passed, exit 0. |
| invariant `contrast-review` | Yes | Yes | source `project`, same file, `invariants.contrast-review` | Tested retention of high severity and PLAUSIBLE verdict with verification skipped; required no verified blocker and partial coverage. |

The current supporting source digest is `830dc3c50369c21f523a1c68b188f3013b40c439ea362a1e97c45a38a89a79c5`; expected and actual match. The source explicitly supports both facts, not merely the profile's structural shape. The checker lists `project` as consumed_source_ids; this table records the lead's actual consumption separately.

The invariant states: “A high-severity candidate without independent verification stays PLAUSIBLE and does not become a verified blocker.” Plan/UX facts were not returned for review and were not used. No web surface was selected or visited. Public tutorial and implementation facts are retained separately in the source snapshots and are not attributed to any other project profile.

The tutorial `examples/validator-hardening.md:35-41` supplies acceptance scenario A02, with D2/D3 at lines 15-16. The current derivative validator checks skipped verification at line 35, derives blockers only for CONFIRMED high/critical findings with verifier ran at line 44, and emits PARTIAL/PENDING for skipped verification at lines 45-47. It passes findings through without rewriting severity at line 50. Its bytes match the canonical `skills/qore-review/scripts/finding-lint.mjs` inspected in this run (see scoped manifest). Regression tests `test_skipped_verifier_preserves_high_and_critical_severity` and `test_missing_verifier_never_proves_or_refutes` exercised the canonical implementation in the selected project validation.

Direct reproduction used a clearly synthetic high/PLAUSIBLE input, not an allegation of an actual defect. The derivative returned valid=true, high severity unchanged, PLAUSIBLE=1, blocking_findings=[], coverage=PARTIAL and verdict=PENDING, exit 0. This agrees with the relevant invariant and A02. Review effect: no violation observed in this focused case; no verified blocker or release approval is inferred. No independent verifier ran, so this lead observation is not an independently CONFIRMED or REFUTED finding.

The example's general verification paragraph references qore.json. For this consumer probe the user requested the current profile-selected command; only that command was selected and executed. No facts from another profile were imported to replace it. The selected test suite invokes canonical review/plan/UX validation scripts; these are tests within the authorized project command, not execution of other generated derivatives or other review campaigns.
