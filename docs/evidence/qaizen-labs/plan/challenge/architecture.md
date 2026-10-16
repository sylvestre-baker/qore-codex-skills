# Architecture — Workflow Cross-examine

Read all five complete Analyze reports: Product, Architecture, UX, Delivery and QA. Snapshot remains `1461fc149209fa29adc067a2b8f3c644055228aa0a2f45485779e3a418f47fd6`. Source paths below are relative to `methods/planning-input/`; report paths are relative to `methods/plan/`. This is the single bounded Cross-examine pass. No browser, service, source edit or new runtime measurement occurred. The Analyze preflight/check results still establish freshness/consistency only.

## Product challenge: define acceptance without expanding invariants

Product acceptance items 3–4 correctly distinguish state from generic h1 focus and identify vacuous unanswered checking after controls unmount. Adopt a returned-introduction predicate plus an unanswered assertion before Back, using existing primitives (`browser-actions.json:99-108`; `tools/browser_probe.mjs:115-125`). Concrete counterexample: Back focuses a stale h1 but leaves the question visible; existing final actions can pass. The fixture positive test already checks intro visible/question hidden (`tests/test_browser_probe.py:50-52`). Actual public selectors/content remain an implementation dependency, not something this planning pass can invent.

Challenge the phrase “never selects an answer” if interpreted as continuous monitoring of all application behavior. Endpoint assertions plus action review do not prove the absence of an arbitrary transient selection between samples. Smallest supported invariant: no action deliberately selects an answer; assert the question remains unanswered at entry, after help closure/immediately before Back, and after return. Preserve a limit on unobserved intermediate moments. Product must distinguish this measurable protocol obligation from a stronger continuous-state guarantee; no current website violation is established.

Product and Delivery support my A2: generic COMPLETE remains execution status. Full Labs acceptance requires the required-check/evidence map, and local tooling acceptance remains separate from live observation completion. No required criterion is silently deferred; its unperformed evidence is named.

## UX challenge: readiness and evidence with bounded complexity

UX requirements 2–3 and 6 are useful minimal action changes: explicit returned state, reopened-help `open` assertion, and unanswered check while answers still exist. Help-open capture is optional when retained assertion/event evidence unambiguously proves the state; avoid making another screenshot a proxy acceptance condition. Final returned state/focus and independent Close proof remain required.

Timing needs precise wording. Product describes focus assertions as immediate, but the preceding action already receives 900 ms before the next assertion (`browser_probe.mjs:143`). UX identifies the actual counterexample: valid restoration later than that pause. Adopt bounded predicate waiting only after a delayed-positive/never-correct control demonstrates the desired semantics. Prefer existing assertion names with preserved input formats and bounded eventual evaluation if agreed, rather than a parallel action vocabulary. Waits must not re-press Enter, re-click, force focus, or restart traversal. The chosen finite focus/attribute timeout is a proposal until Product/UX agree it; it is not a sourced product SLA.

Challenge unnecessary expansion of global answer predicates: no current source proves unrelated selected UI causes a real failure. Keep legacy `assert-none-checked` behavior. An additive scoped selector is justified only when the questionnaire boundary is identified and a discriminating control shows global selection is too broad (`browser_probe.mjs:124-125`). Do not narrow it merely to obtain a pass.

Traversal limits describe the observed path: failure to reach Back in 24 forward steps is a bounded reachability failure, not global inaccessibility. No automatic reverse-direction fallback should hide that failure. A deliberately chosen Shift+Tab protocol must retain its identity and starting focus.

## Answers and minimal architecture decisions

**Product:** no new keyboard abstraction is needed. Existing `traverse-focus` records actual step events and fails before later actions; compose it with Back focus assertion, Enter, state/focus assertions. The excluded-control test verifies the later mouse click never executes (`tests/test_browser_probe.py:58-66`).

**QA/Delivery:** put a compact run manifest and required-check/evidence table beside the Labs report, outside the generic interpreter. Record profile/contract/actions/policy/probe digests, fixture or live target identity, driver/time, artifacts and check statuses. Existing result/event schema and legacy callers remain compatible. A missing required observation prevents Labs success even when generic COMPLETE is legitimate. No runtime registry or Labs-aware mandatory harness is warranted.

**Delivery:** fixture/helper and installed-driver availability are unverified here. Frozen tests name `tests/fixtures/keyboard-journey.html`, `tools/context.py`, and `QORE_PLAYWRIGHT_MODULE` (`test_browser_probe.py:13,25,37`; `test_labs_contract.py:11-15`). Bind those actual implementation-checkout dependencies and their digests before execution; do not fabricate them or silently import an unrelated runtime.

**UX:** failure capture can reuse the existing snapshot helper in a best-effort inner try after preserving the original error, only when a page exists. Cleanup must independently attempt trace/context/video/browser finalization and still write result/events; a capture/cleanup failure must not replace the originating failure. This is a bounded robustness proposal, with fault-injection evidence needed before claiming it works.

## Revisions, privacy and warnings to QA

I revise my initial A4 description: ordinary action exceptions receive structured status, but unguarded cleanup exceptions can prevent writes (`browser_probe.mjs:153-167`). Test capture failure and context/browser-close failure; require original error preservation and whatever artifacts remain writable. This is a concrete local failure path, not a claimed observed defect.

Adopt QA's trace-canary investigation. The events projection omits request headers/bodies, but tracing and DOM/video captures are separate sinks (`browser_probe.mjs:37,67,79-89,155`). The current unqualified retention wording is stronger than the inspected guarantee. State the narrow events guarantee until a synthetic canary proves what trace, DOM and video retain; keep evidence local. An enclosing manifest cannot sanitize traces. If unwanted content is demonstrated, reduce capture scope or sanitize the affected artifact with an explicit tradeoff rather than silently exporting it.

Warn QA to discriminate wrong Close focus from correct Back, delayed focus from never-correct focus, wrong-heading focus from true introduction state, pre-Back selection from vacuous final checking, popup/redirect attempts from main-frame-only coverage, and cleanup failure from successful evidence retention. These controls test identified boundaries; none constitutes current website evidence.

No material architectural dissent remains on reuse or scoped evidence mapping. Unresolved decisions: stable public state/question selectors, eventual-focus timeout, necessary capture artifacts, actual trace retention and runtime dependencies. Preserve those limits in adjudication; a planning protocol can finish while their execution evidence remains pending.
