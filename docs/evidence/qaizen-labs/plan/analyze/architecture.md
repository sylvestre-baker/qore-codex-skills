# Architecture — independent Analyze

Scope: strengthen the existing Labs verification protocol and optional local browser harness. Workflow mode applies because `examples/qaizen-labs/verification-spec.md` already specifies this correction. This is one bounded independent Analyze perspective, not adjudication or human evidence. No website request, local server, source modification, peer report consumption or subagent execution occurred.

## Snapshot and inspected sources

Frozen target: `methods/planning-input.json`, label `Labs protocol correction planning input`, snapshot SHA-256 `1461fc149209fa29adc067a2b8f3c644055228aa0a2f45485779e3a418f47fd6`, recorded `2026-10-16T06:37:50.981528+00:00`. Paths below are relative to `research/qore002-implementation-20261016/methods/planning-input/` unless explicitly prefixed otherwise. All implementation citations refer to that frozen copy. The public example root was used only for profile freshness and its declared offline check.

Inspected: `examples/qaizen-labs/verification-spec.md:6-18,56-109`; `surface-contract.json:2-20`; `browser-actions.json:1-110`; `observation-policy.json:1-5`; `checks/check_contract.py:1-54`; `tools/browser_probe.mjs:1-169`; `tests/test_browser_probe.py:1-82`; `tests/test_labs_contract.py:1-51`; `profiles/qaizen-labs.json:1-79`. Also read the generated derivative's SKILL, project-preflight, protocol and roles references. Uninspected: fixture HTML and `tools/context` implementation are absent from this frozen target; website behavior, optional-driver installation and rendered artifacts are not observed in this role.

## Commands, current facts and their effects

Commands are shown using workspace-relative paths; the preflight's `--root` was resolved to that absolute directory at execution. No personal path is needed to reproduce the invocation from the workspace root.

1. From `research/qore002-implementation-20261016/derived-initial/qore-plan-qaizen-labs`, ran `python3 scripts/project-check.py references/project.json --root <workspace>/qore-skills/examples/qaizen-labs --method plan`. Exit 0; `qore-context-check/1`, coverage COMPLETE, no problems, both sources current. Complete JSON is retained below. This is profile freshness, not protocol completeness.
2. Inspected `checks/check_contract.py` before running its selected argument vector. From `qore-skills/examples/qaizen-labs`, ran `python3 -B checks/check_contract.py surface-contract.json`. Exit 0; `valid: true`, schema `qaizen-labs-surface/1`, all eight declared checks returned; limit explicitly says contract consistency only.
3. Ran `node --check research/qore002-implementation-20261016/methods/planning-input/tools/browser_probe.mjs`. Exit 0, no output. Syntax only; no runtime or browser claim.

Profile SHA-256: `f76afdd45cb6352e5044a06affc4182ea6cd40aa9c012fb216636a61faa428f0`. Facts selected and actually consumed:

| Fact | Source ID / current SHA-256 | Identifiable effect |
|---|---|---|
| `surface-contract` command | `checker` / `9ef2a0acf51f078ce290ec723ca550b8b73597e68304179fe4d0625c5757963b` | Executed offline check; contract validation remains a separate component and result from browser evidence. |
| `close-focus` | `surface` / `3728739a119a53272541f83d451e40addb6939304f9d9ec060a477a87170a4a3` | Preserve dedicated Close → summary assertion; it cannot substitute for Back. |
| `back-focus` | same `surface` digest | Require recorded sequential traversal, Enter, then introduction focus; reject any mouse-success substitution. |
| `unanswered-scope` | same `surface` digest | Install context routing before entry, block service workers, keep answers unselected, retain analytics blocking as evidence. |

The plan preflight selects no `surfaces` fact (`{}`); the website URL is not treated as a selected plan execution target. No unselected profile surface fact was consumed for a website run.

## Reuse and impact sweep

The required extension already exists in this snapshot: `traverse-focus` bounds Tab/Shift+Tab to 1..50 steps, records every actual focus step and throws before subsequent actions when the target is unreachable (`tools/browser_probe.mjs:127-140`). `assert-focused`, actual `keyboard` actions and URL waiting also exist (`:114-120`). The actual Labs consumer already composes these: Back traversal, Back focus assertion, Enter, h1 focus assertion and unanswered assertion (`browser-actions.json:84-105`). Do not add another keyboard engine, API, database, mandatory driver or duplicated Labs harness. The smallest correction is to verify and strengthen the existing protocol, evidence mapping and missing discriminating controls where justified.

Known consumers and contracts:

| Producer / stored artifact | Reader | Compatibility decision |
|---|---|---|
| `surface-contract.json` transitions, scope, checks | offline checker; profile source binding; maintainers | Keep `qaizen-labs-surface/1`; preserve separate Close and Back obligations (`check_contract.py:32-39`). |
| `profiles/qaizen-labs.json` source records and facts | derivative preflight for plan/review/UX | Regenerate maintained profile derivatives if a bound source changes; do not alter bundled digest to silence staleness (`tests/test_labs_contract.py:36-51` documents expected stale exclusion). |
| `browser-actions.json` ordered `{type, selector|role/name, key, max_steps, ...}` | browser probe loop | Preserve legacy `click`, `click-if-visible`, `keyboard`, text/URL assertions and snapshot behavior; additive actions are sufficient (`browser_probe.mjs:105-145`). |
| `observation-policy.json` exact `allowed_origins` | context request route | No new policy service; local JSON checked before Chromium execution (`:24-26,55-66`). |
| probe `events.json`, `result.json`, snapshots, trace/video paths | tests and evidence reviewer | Keep `qore-browser-probe/1`, existing status semantics and event names unless a demonstrable incompatibility requires versioning (`:29-40,149-168`; tests `:40-77`). Additive evidence fields must not redefine COMPLETE as product approval. |

No transaction or shared data store exists here. The process owns its isolated context, new output directory, routing, sequential actions and artifact finalization. Local JSON files are stored inputs; DOM/focus are current derived reads; event/snapshot files are stored observation snapshots. Re-running against a website must create a new evidence directory, not reuse a prior observation (`browser_probe.mjs:27-28`).

## Proposed decisions and deliverables

A1 — Retain the optional driver boundary and existing interpreter. No automatic driver installation; unavailable driver remains BLOCKED (`browser_probe.mjs:47-50,149-152`). Legacy action regression coverage is already declared (`tests/test_browser_probe.py:43-56`); implementation work should preserve it.

A2 — Make scoped acceptance a mapping from sourced check IDs to concrete action/event evidence, rather than equating generic process completion with Labs acceptance. The generic harness currently completes whatever supplied action list finishes, including an empty list (`browser_probe.mjs:22-23,105,147-148`); that is valid generic behavior. The Labs evidence consumer should require `keyboard-back`, `close-focus`, `introduction-focus`, unanswered and policy proof before a scoped success claim. Deliverable: a concise check-to-action/evidence table in the revised spec/report, with missing observations marked PARTIAL/BLOCKED. Do not introduce a workflow registry merely to enforce one example.

A3 — Prove Back by chain: `focus-step(reached=true)` for the declared Back target → Enter action → focus on introduction h1 and visible introduction state → no selected answers. The negative control excludes Back from tab order, then includes a later mouse click that must never execute (`tests/test_browser_probe.py:58-66`). This rejects the concrete false positive without any new abstraction. Existing events contain intermediate active-element identity; preserve that evidence, not just final screenshots.

A4 — Keep failures fail-closed and attributable. Invalid input/driver launch precedes successful observation; runtime exceptions produce BLOCKED before snapshots or PARTIAL after snapshots with nonzero exit (`browser_probe.mjs:149-152`). Do not retry by clicking or programmatically focusing Back. Retain blocked mutation events without failing solely because expected analytics POSTs were prevented (`:61-63`; `surface-contract.json:20`). An outside-origin navigation attempt prevents COMPLETE (`:144`).

A5 — Retain the current routing ownership: isolated context, `serviceWorkers: 'block'`, `context.route` before `newPage`/`goto` (`browser_probe.mjs:54-69,94`). Origin enforcement concerns main-frame and popup navigation, while the read-only method filter applies to all routed requests. No broadened origin access or questionnaire completion is proposed. Deliverable: concrete negative policy controls and preserved attempted-request records, separate from journey assertions.

Component flow: maintained contract/checker → current profile preflight → selected offline check plus sourced plan assertions → ordered Labs actions + exact-origin policy → optional existing probe → isolated Chromium context → events/snapshots/result → reviewer check-to-evidence mapping. Controls and live runs have separate identities and evidence directories; controls establish probe discrimination, never current website success.

Runtime sequence: validate URL/actions/policy; reserve new output directory; load optional driver; create isolated context; install method/origin guards; begin tracing and attach listeners; navigate entry; wait for URL assertions; preserve unanswered first-question state; traverse/open/toggle/reopen/close help; assert summary focus; traverse to Back and record each step; press Enter; assert introduction focus/state and unanswered condition; capture final artifacts; close context/browser; write result and events even on ordinary action failure. No database commit, API transaction or outbox is needed.

## Concrete risks and explicit hypotheses

R1 — Scope overclaim: a consumer reports `result.status=COMPLETE` as full Labs acceptance without checking required observations. Counterexample: `--actions` omitted still executes the generic entry/Tab/final path and may complete (`browser_probe.mjs:22,100-105,147-148`). Proposed response is evidence mapping, not claiming the generic probe is defective.

R2 — State aliasing: `h1` focus alone can pass on an unintended heading while introduction content is absent. The Labs actions currently assert h1 focus but do not separately assert intro visible/question hidden (`browser-actions.json:99-109`); the positive fixture test does check both (`tests/test_browser_probe.py:50-52`). Hypothesis to resolve with UX: add an unambiguous introduction marker/state assertion, using public selectors and observed content. No current website failure is established.

R3 — Freshness coverage is deliberately narrower than all runtime inputs: the profile binds contract and checker, not actions/policy/probe (`profiles/qaizen-labs.json:5-15`). If any of those change, successful profile preflight alone does not identify the executed runtime version. Preserve their snapshot hashes in run evidence; do not imply the preflight covers them all.

R4 — Browser controls are optional-driver gated and their fixture HTML is absent from this frozen package (`tests/test_browser_probe.py:13,21-25`). Their source demonstrates intended discrimination but is not a passing execution measurement. No local service was started under this role's no-network-services constraint. Missing real control results remain unfinished.

R5 — Artifact finalization has unguarded `context.close()`/`browser.close()` before result writes (`browser_probe.mjs:153-167`). Hypothesis: a cleanup exception could suppress the structured failure record. QA should decide whether a bounded injected cleanup failure merits a regression and best-effort cleanup in this correction, rather than silently expanding scope.

## Questions for required peer roles

Product: confirm that desktop English entry/state evidence is the smallest useful outcome; should scoped acceptance explicitly reject a generic COMPLETE run missing one required check? The current spec supports that distinction (`verification-spec.md:96-100`). No new abstraction is needed to demonstrate keyboard reachability.

UX: what uniquely identifies returned introduction state in the public observation, beyond a focused h1? Should the action contract assert the question is hidden as the fixture test already does? Is 24 forward Tab presses an accepted bounded failure threshold for the declared desktop state, with Shift+Tab reserved for an explicitly chosen alternative rather than fallback that hides an unwanted path?

QA/security: can the controls prove failure occurs before the later mouse click, prove Enter activation, distinguish blocked expected analytics from forbidden navigation, and cover delayed URL success plus finite-timeout failure? Should finalization failure be required now or documented as a limitation? Warn that no optional-driver tests were executed in this Analyze turn.

## Unfinished work

Await one authorized Cross-examine pass, then lead adjudication. Required later evidence: optional-driver positive/negative control executions with available fixture source, distinct Close/Back observations, policy/navigation negative controls, delayed URL control, current live run only when separately permitted, and inspection of captured state. This report does not adjudicate Product/UX/QA, certify the website or claim complete planning protocol coverage.

## Complete preflight JSON

```json
{
  "schema": "qore-context-check/1",
  "profile": {
    "id": "qaizen-labs",
    "version": "0.1.0",
    "sha256": "f76afdd45cb6352e5044a06affc4182ea6cd40aa9c012fb216636a61faa428f0"
  },
  "method": "plan",
  "coverage": "COMPLETE",
  "sources": [
    {
      "id": "surface",
      "path": "surface-contract.json",
      "expected_sha256": "3728739a119a53272541f83d451e40addb6939304f9d9ec060a477a87170a4a3",
      "actual_sha256": "3728739a119a53272541f83d451e40addb6939304f9d9ec060a477a87170a4a3",
      "current": true
    },
    {
      "id": "checker",
      "path": "checks/check_contract.py",
      "expected_sha256": "9ef2a0acf51f078ce290ec723ca550b8b73597e68304179fe4d0625c5757963b",
      "actual_sha256": "9ef2a0acf51f078ce290ec723ca550b8b73597e68304179fe4d0625c5757963b",
      "current": true
    }
  ],
  "commands": [
    {
      "id": "surface-contract",
      "argv": ["python3", "-B", "checks/check_contract.py", "surface-contract.json"],
      "source": "checker",
      "applies_to": ["plan", "review"]
    }
  ],
  "invariants": [
    {
      "id": "close-focus",
      "statement": "Closing question help restores focus to its summary; verify this separately from the application Back transition.",
      "source": "surface",
      "applies_to": ["plan", "review", "ux"]
    },
    {
      "id": "back-focus",
      "statement": "Reach the application Back control using sequential Tab or Shift+Tab; activate with Enter and verify introduction heading focus. A click or programmatic focus does not prove keyboard reachability.",
      "source": "surface",
      "applies_to": ["plan", "review", "ux"]
    },
    {
      "id": "unanswered-scope",
      "statement": "Leave the first question unanswered, block all non-GET/HEAD/OPTIONS requests and main-frame/popup navigation outside the allowed origins. Record blocked analytics; do not relax policy for a successful recording.",
      "source": "surface",
      "applies_to": ["plan", "review", "ux"]
    }
  ],
  "surfaces": {},
  "consumed_source_ids": ["checker", "surface"],
  "problems": []
}
```
