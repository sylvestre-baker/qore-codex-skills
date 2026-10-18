# Execution evidence

Record actual execution separately from the plan, findings, or UX score. A `qore-run/1` record supports evidence identity and declared coverage; it does not certify factual quality, independence merely from actor names, or permission to deliver.

## Run record

Write JSON with these explicit fields:

- `schema`: `qore-run/1`; unique `id`; `method`: `ux`; and the actual installed `skill` name.
- `candidate_sha256`: SHA-256 identifying the exact candidate/skill snapshot; retain the digest procedure and manifest or snapshot artifact. Do not substitute a different package revision.
- `target`: `{label, snapshot_sha256}` identifying the actual target revision or named file/working-tree snapshot. Retain the snapshot/digest procedure.
- `last_relevant_change`: a timezone-aware ISO timestamp for the last relevant target/candidate correction. Never invent an earlier change time to make existing evidence appear fresh.
- `environment`: `{id, operator, host}` describing the actual environment and operator category, such as maintainer, agent, or external human. An agent walkthrough is not external human first-use evidence.
- `profile`: `null` for generic use, otherwise `{id, version, sha256}` for the exact consumed bundled profile.
- `required_phases`: the method phase IDs below, plus `profile_preflight` when a profile is used and any additional phases required by scope.
- `phases`: `{id, actor_id, status, artifacts, reason?}` records. Status is `PASS`, `FAIL`, `SKIPPED`, `BLOCKED`, or `NOT_APPLICABLE`. Artifacts are paths declared below. A PASS needs actual evidence; any other status needs a reason.
- `artifacts`: `{path, sha256, kind}` records for files under the evidence root; `kind` is `execution`, `source`, or `presentation`. Paths are unique contained relative paths; no `..`, absolute paths, or escaping symlinks. Digests match current bytes. Execution artifacts additionally bind `candidate_sha256`, `target_snapshot_sha256`, and timezone-aware `observed_at` strictly after the last relevant change.
- `commands`: `{argv, exit_code, artifact}` for actual commands and their declared output artifact. Preserve failed commands as well as successful ones.
- `limitations`: an explicit list, including missing roles/checks, unexamined claims, assistance, freshness limits, and relevant capability gaps.
- `coverage`: `COMPLETE`, `PARTIAL`, or `BLOCKED`, computed from the actual required phase outcomes.

When a copy, visual, or performance scope has no applicable state transition, also record `scope: {"depth": "copy|visual|perf", "state_transition_applicable": false}` with the actual one depth value. Only then may `state_transition` be NOT_APPLICABLE, with a specific scope reason and evidence artifact. Tool absence is not a reason; entry/state/full scopes require an actual applicable transition. A qualification demonstration separately requires the real entry and a resolved-state transition.

Each executed phase retains a JSON artifact with `qore_evidence` metadata (`candidate_sha256`, `target_snapshot_sha256`, `observed_at`, and matching `phase_id`) and `payload` containing its actual output. Its declared row and embedded metadata must agree. Create the wrapper only after the real phase; copying old proof into a new wrapper does not renew its observation time. A phase PASS references its matching execution artifact; source or presentation artifacts alone cannot prove execution.

Include instruction/README revision, capability probes, requested/returned role roster, profile fact consumption, per-phase timestamps and target/candidate changes in declared companion artifacts. Evidence captured before a relevant correction, for another target, or from another candidate cannot silently establish the present result. A sanitized public artifact has its own identity and a recorded transformation relationship to raw proof; verify it still supports the linked claim.

## Required phases

Use `scope`, `browser`, `state_transition`, `freshness`, and `verdict`. Retain depth input/lint, the initial required-check matrix and driver probe, real entry/state/transition observations, per-gate artifacts/timestamps, correction snapshots, loop history, and actual stop-rule output. Scope assessment must explicitly identify applicable transitions; no preflight or source inspection substitutes for an actual transition when one is required.

When a profile is present, `profile_preflight` retains the checker output, source digests, and profile-use artifact. The profile's freshness does not establish the other phases.

A phase PASS means the required work actually ran and its evidence was retained; it does not mean the target contained no defects. A finding of a defect can be a successful review phase. FAIL means the phase itself did not complete successfully. Use SKIPPED/BLOCKED for work not executed and state the cause. Only the documented scope-bound transition exception permits a mandatory UX phase to be NOT_APPLICABLE; it cannot conceal missing execution.

Preserve the original required scope. Missing required tools, data, or fresh measurements prevent global SHIP. Complete observations can establish DO-NOT-SHIP; report that separately from execution coverage. A justified check exclusion needs its scope/source reason and cannot be based on tool absence.

## Check the record

From the skill directory run:

```bash
python3 scripts/run-check.py /absolute/path/to/execution.json --evidence-root /absolute/path/to/evidence
```

Retain output and exit status. The checker validates declared identities, artifact digests, role separation constraints, and phase coverage. It cannot prove the sources support conclusions or that a person actually interacted with the target. A passing checker does not replace full phase reports and raw observations.

Coverage is COMPLETE only when all applicable required phases ran with evidence and any permitted non-applicability is justified. With useful completed work and a required gap, use PARTIAL; if no required work can execute, use BLOCKED. If a method is outside the task (for example justified no web effect), state that boundary rather than manufacturing a completed method run. Keep execution coverage separate from product readiness and deployment authorization.
