# Browser and loop evidence

Use the driver's documented APIs, discovered in this session. Do not copy an unsupported tool name from a historical setup or infer capabilities from a connector's presence. Operate a shared browser sequentially so navigation/state changes cannot race each other.

## Observation procedures

| Check | Procedure and artifact |
|---|---|
| Entry | Capture entry page/control, activate it, capture intended surface and distinguishing content, and repeat per relevant context. |
| Direct/reload/history | Navigate directly, reload, then exercise relevant same-document state and Back/Forward. Save URL, visible state, console and document/network outcomes. |
| Loading → resolved | Capture pending state, observe the corresponding response, then capture loader removal and terminal content/error/empty state. Use bounded waits tied to an observed condition. |
| Authorized action | Establish persona/account, activate the control, observe request/result and resulting UI/persistence. Record the actual action, not merely the availability of a button. |
| Visual | Set the intended viewport and verify its actual CSS width/height before trusting the screenshot; window size is not viewport size. Capture and actually view screenshots at declared themes and relevant transitions. Use DOM geometry to investigate candidates; preserve the rendered proof. |
| Content | Inspect visible text/DOM across interpolations and states. Treat scanner matches as candidates requiring context. |
| Accessibility | Inspect semantic names/structure, perform keyboard navigation, capture focus, measure risky contrast, and retain required instrumented audit output. |
| Performance | Capture a real trace/audit for the scoped navigation/interaction, retain settings and metrics, inspect summaries rather than loading a large raw trace into context. |

Use a gitignored project evidence directory or an explicit temporary directory. Do not commit screenshots or traces by default. Artifact names identify gate, state/context, viewport/theme, and iteration. Record timestamp, candidate/target revision, and procedure. Preserve raw evidence privately when it may contain credentials or user data; public redactions need their own identity and a traceable relationship to the raw proof. Do not publish an artifact automatically.

Screenshots must be opened/viewed before a visual PASS. A DOM or semantic snapshot cannot stand in for pixels. Console/network artifacts must identify the observed time/window and requests rather than a generic claim that they were checked.

For local static artifacts, use an authorized local HTTP origin when the required driver/audit cannot inspect file URLs. Correlate console failures with exact requests and behavior: a missing optional asset, an origin restriction, and an application exception have different consequences. Treat apparent instrumentation/contrast false positives as hypotheses to investigate against rendered colors/backgrounds; do not suppress a class of warnings automatically.

## Loop file

The loop file consumed by `scripts/stop-rule.mjs` is separate from the `qore-run/1` execution record. Maintain an immutable initial `in_scope` list and append real iterations. A minimal illustrative shape is:

```json
{
  "in_scope": ["G4", "G6"],
  "iterations": [
    {
      "n": 1,
      "scores": {"G4": 4, "G6": 5},
      "measured": ["G4", "G6"],
      "fix_applied": false
    }
  ]
}
```

This example represents copy scope only and is not evidence that any check ran. Use the actual required gates and observations. Fields:

- `n`: strictly increasing positive iteration number, maximum six performed iterations.
- `scores`: integer 0–5 values for observed gates; never change a score without remeasurement.
- `measured`: gates actually measured in this iteration. Carrying a previous score does not make it fresh.
- `fix_applied`: true when a correction lands at the end of that iteration; same-iteration observations predate it.
- `skipped`: map required gate IDs to the reason their observations were skipped.
- `infra_blocked`: required gates blocked by an observed infrastructure failure; retain diagnostic artifacts separately.
- `not_applicable`: map gate IDs to justified product/scope reasons, either at top level or per iteration. Tool absence is not a reason. The declared scope cannot silently shrink.
- Optional `g6_passed`: boolean challenge result; include G6 in `measured` when using it. Otherwise score G6 numerically.

Run from the skill directory:

```bash
node scripts/stop-rule.mjs /absolute/path/to/loop.json
```

Keep its output and exit status per iteration. Missing, skipped, blocked, or stale required checks prevent SHIP. A complete failing observation may still yield COMPLETE execution coverage with DO-NOT-SHIP. At the ceiling, record remaining defects/gaps and stop; do not use a zero score as a reason to continue.

If no web behavior is applicable (`none`), explain that boundary rather than claiming a completed browser run; do not feed an empty scope to the stop-rule or invent browser checks. For actual web review, include an observed transition when applicable. A copy/visual/performance run may declare the transition non-applicable only under the explicit [run-record condition](run-evidence.md); a qualification demonstration of a data-driven surface must navigate from its real entry and reach a resolved state.

## Readable result

State surface/snapshot, depth, contexts, data provenance, themes/viewports, driver and capability matrix, and completed iterations. For each gate show score or omission status, required checks, evidence/timestamps, finding, and freshness. Keep blockers, uncertain observations, and justified non-applicability distinct. Give stopping reason, scope-limited verdict, coverage, and concrete resumption path. A broader delivery decision remains separate from the review's evidence.
