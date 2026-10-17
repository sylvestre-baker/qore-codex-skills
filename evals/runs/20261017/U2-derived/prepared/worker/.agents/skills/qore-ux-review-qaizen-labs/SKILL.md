---
name: qore-ux-review-qaizen-labs
description: Inspect rendered web behavior through a scoped observe, fix, and re-verify loop with fresh evidence and a six-iteration limit. Use to verify web pages or frontend changes; source inspection alone and native app interfaces are outside this method's qualified scope. Scoped to project qaizen-labs.
---

# Qore UX Review

Observe the actual web experience and report what the evidence supports. Browser preflight alone, screenshots without inspection, and type or unit checks cannot establish rendered behavior.

1. Resolve the authorized target, change snapshot, entry path, personas/account contexts, and required state. If `references/project.json` exists, complete [project preflight](references/project-profile.md) before selecting targets or checks from it. Generic first use needs no persistent profile or Qore account.
2. Read [scope and loop](references/protocol.md), [gates and scoring](references/gates.md), and [evidence procedures](references/evidence.md). Declare depth, required gates, state/theme/viewport matrix, and finite budget before discovering tool gaps. Run `node scripts/depth-lint.mjs /absolute/path/to/depth.json` from this skill's directory. Do not shrink scope to conceal a missing capability.
3. Probe the actual browser driver: navigation, screenshot capture, DOM/semantic inspection, keyboard interaction, console, and network observation. Record driver × depth × capability × required check × evidence. Prove instrumented accessibility/performance capabilities separately when required. An unavailable required capability makes coverage PARTIAL or BLOCKED; no browser check becomes PASS from source inspection.
4. Drive the real entry control before deep URLs when G0 applies. Observe applicable states and resolved transitions, inspect screenshots, and collect console/network/DOM evidence. Exercise authorized controls as the actual persona and account context, including their outcomes. Authentication or a profile never grants new mutation permission.
5. Score and challenge the required gates. If fixes are authorized, correct established in-scope defects, then renew evidence. Keep a loop file and run `node scripts/stop-rule.mjs /absolute/path/to/loop.json` after each iteration. **Stop by six iterations**, including persistent zero gates. A fix invalidates prior measurements; success requires fresh observations after the last fix.
6. Report gate evidence, defects, omitted checks, stopping reason, and **COMPLETE / PARTIAL / BLOCKED coverage**, separately from the scoped SHIP / DO-NOT-SHIP / PENDING result. A skipped required check prevents global SHIP. Record [execution evidence](references/run-evidence.md); SHIP is a review result, not deployment authorization.

Use one non-destructive retry for transient driver failures, then retain the diagnostic. Do not silently install software, terminate user browsers, remove locks, seed shared data, publish, or deploy. Native apps are unqualified; report the boundary without substituting web observations for native testing.

## Generated project binding

This derivative must load [its project profile](references/project.json) before selecting project facts. Run its bundled project-check.py against the supplied project root with --method ux. Consume only current returned facts; stale required context is PARTIAL or BLOCKED. The profile grants no action permission. Edit the maintained profile, not this generated copy.
