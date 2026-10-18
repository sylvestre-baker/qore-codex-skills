# Gates and evidence-based scoring

Use the requirements of the actual surface. Record each required check and its artifact; a gate score must not conceal a missing check. Gates excluded by depth remain visible with their scope reason. A missing tool is SKIPPED/BLOCKED, never a product defect or non-applicability justification.

| Score | Observable interpretation |
|---|---|
| 0 | Established severe failure of the gate: unreachable path, invalid render, unusable interaction, or equivalent demonstrated failure. |
| 1 | Major defect in a principal path. |
| 2 | Material defect in a secondary state or required context. |
| 3 | Functional behavior with a concrete acceptance or usability defect still open. |
| 4 | Required checks pass; any remaining issue is documented and non-blocking within scope. |
| 5 | Required checks and focused challenge pass with no observed issue. |

No artifact means unobserved, not a fabricated score. A 5 is not proof of perfection or a claim of industry superiority. State the observed issue behind any score below 4.

## G0 — Entry reachability

Start from the real entry page and click the specified control. Assert the intended surface using its heading and distinguishing content, not just its URL. Check for stale controls that still open a superseded flow. Repeat for every relevant persona/account context. Source-search inbound route/navigation wiring where available, but do not call a route orphaned from a search that misses dynamic navigation. A source search cannot replace the actual click.

## G1 — Direct navigation and rendering

Navigate directly to applicable stateful URLs and reload. Observe document outcome, console exceptions, hydration/render errors, authentication context and visible result. Check valid and principal invalid permutations. For same-document navigation, exercise hash/query changes and Back/Forward; a fresh page load alone can miss stale views. Distinguish expected application rejection from a broken valid document.

## G2 — Data and state transitions

Map applicable loading, empty, zero-results, single, typical/representative, overflow, error, and partial-data states. Identify those not applicable and why. Use actual authorized representative data and label fixtures or simulated responses; never describe empty-only or mocked observations as real-data coverage.

For each relevant loader, pending save, or optimistic update, observe its terminal state. Correlate the network outcome with loader removal and content/empty/error rendering. A successful request with a permanently pending interface is a demonstrated failure. A screenshot of a loader alone does not establish a transition. Exercise authorized write/toggle/submit controls in the actual account context, inspect the response and final state, and verify persistence where required. Do not infer that a visible control works without activating it.

## G3 — Visual behavior

Inspect the rendered images at declared viewports/themes: alignment, rhythm, hierarchy, readable text, clipping, overlap, overflow, component consistency, and responsive behavior. Check applicable reduced-motion behavior and content visibility before/after hydration. DOM geometry can support the check; a semantic tree cannot establish visual layout. Avoid imposing equal heights or a fixed viewport on layouts that intentionally differ; use the surface's actual design requirements.

## G4 — Content integrity

Inspect every affected interpolated state for grammar, labels, units, dates/numbers, localization, accessible instructions, and actionable errors. Detect exposed internal identifiers/enums, `null`, `undefined`, `NaN`, stack traces, or implementation jargon, then confirm whether the text is actually inappropriate for the audience. Check duplicate IDs where they affect semantics/behavior. A broad text scanner generates candidates, not automatic defects; documentation may intentionally discuss such tokens.

## G5 — Accessibility

Use live semantic inspection and keyboard interaction: meaningful names, appropriate heading structure, reading order, visible focus, focus restoration, overlay close behavior, absence of traps, labels/instructions, and state announcements where needed. Verify risky contrast pairs with actual measurements. Include instrumented accessibility checks required by scope and record their tool/version/results. A screenshot alone cannot establish accessibility, and a high automated score cannot establish keyboard or screen-reader usability. If a required instrument is unavailable, retain partial coverage.

## G6 — Adversarial challenge

Recast each PASS as a claim that could fail. Test the highest-impact applicable risks harder, prioritizing unreachable paths, invalid render, wrong data/account context, accessibility, then polish. Challenge scope exclusions as well as in-scope results. Use authoritative current guidance when an external standard affects the decision. Do not invent a fixed number of defects to find. When a challenge exposes an issue, correct the underlying gate and reopen the loop; do not average it away.

## GP — Performance

Record actual tool, environment, device/network settings, metric, sample method, and trace/report. Use relevant metric budgets from the project's current acceptance criteria or explicitly declared review targets. Inspect the critical render/interaction path and trace bottlenecks rather than treating a composite audit score as an outcome. Distinguish lab observations from field population data and do not label a lab pass as a real-user percentile result. Verify current metric definitions/thresholds from authoritative sources when they drive a decision. Required unavailable measurements make coverage PARTIAL; they cannot be estimated from a fast screenshot.
