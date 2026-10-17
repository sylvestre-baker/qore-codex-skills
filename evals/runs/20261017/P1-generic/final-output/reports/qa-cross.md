# QA and security — Workflow Cross-examine pass

Role: QA and security. One cross-examination pass after the lead's report barrier at `2026-10-17T10:28:02.060147Z`. Supplied snapshot: `0aa277436d8dcda4d6c2412c6ad4307dd0192b0f6230fa96c8b16d99c8bac194`. Initial report preserved at `/workspace/output/reports/qa-analysis.md`. No network, website execution, source edits or subagents.

## Inspected inputs and actual checks

Read all five complete initial reports: `/workspace/output/reports/product-analysis.md`, `architecture-analysis.md`, `ux-analysis.md`, `delivery-analysis.md`, and `qa-analysis.md`. The combined read was truncated by tool output; recovered Architecture, UX and Delivery with separate numbered reads, including Architecture's final unfinished-work paragraph. Product and QA were present completely in the first read. Reused inspected original source locations: `TASK.md:3-5`; `surface-contract.json:4-20`; `checks/check_contract.py:9-43,46-54`; `observation-policy.json:2-4`; `target/verification-protocol.md:3-10`. No report conclusion is treated as a new project authority.

Actual commands in this pass: `cat` of the five reports; `nl -ba` of Architecture, UX and Delivery; `tail -n 4` of Architecture to recover its end; and the following local in-memory validator experiment in `/workspace/worker`. No experiment file was written and `-B` suppressed bytecode:

```python
import copy, json, runpy
from pathlib import Path
validate = runpy.run_path('checks/check_contract.py')['validate']
base = json.loads(Path('surface-contract.json').read_text())
for name, key, value in [('close traversal mismatch', 'traversal', 'Shift+Tab'),
                         ('close activation mismatch', 'activation', 'click')]:
    data = copy.deepcopy(base)
    next(t for t in data['transitions'] if t['id'] == 'close-help')[key] = value
    print(name + ': ' + str(validate(data)['valid']))
data = copy.deepcopy(base)
next(t for t in data['transitions'] if t['id'] == 'back')['activation'] = 'click'
try:
    validate(data)
except ValueError as error:
    print('back click: rejected: ' + str(error))
```

Command `python3 -B -` exited 0. Actual stdout:

```text
close traversal mismatch: True
close activation mismatch: True
back click: rejected: Back requires sequential keyboard traversal and observed activation
```

This demonstrates, without modifying project files, that the checker is not a complete action/traversal oracle. It reinforces the peers' source-review requirement; it reveals no checker bug that this task authorizes fixing. No browser behavior was measured.

## Challenges to each peer, smallest investigations and outcomes

### Product — P6 / AC6 / question to QA

Exact decision challenged: P6's pass/fail/not-observed evidence ledger and AC6's instruction to check unanswered state initially and before leaving. Concrete failure cases: a persisted/default selection exists despite no answer click; or a guard denies a required script and the observer cannot establish the unanswered state. Counting absence of deliberate input as proof would give a false pass; collapsing unavailable observation into website failure would overclaim. Source: `surface-contract.json:6,18,20`; Architecture's risk at `architecture-analysis.md:76` explicitly identifies defaults/persistence.

Smallest investigation: compare P6/AC6 against Architecture A7 and its unanswered acceptance at `:62`, and QA's invariant row. Outcome: Product already requires explicit observation and separates source consistency, document coverage and browser results in P7; this is not a defect in the selected scope. Strengthen the proposed ledger with **blocked/inconclusive + reason** alongside pass/fail/not observed, and record the public observable indicator that establishes no selected answer. Exact DOM/accessibility indicators remain unknown. A visible question alone does not prove unanswered. Missing indicator means no unanswered pass. Severity remains High for a false acceptance claim; lack of a named runtime selector is a bounded future-evidence dependency, not a current document blocker.

Answer to Product's direct question: policy denial and assertion failure are separate observations. A blocked analytics POST is not automatically pass/fail for the journey. If the guard blocks and a required state remains visible, evaluate its state normally; if the state is unobservable, mark affected checks blocked/not observed. If an observable state directly contradicts an acceptance obligation, record failed criterion and blocking context without claiming a website defect independent of the enforced policy. Minimum evidence: guard configuration/capability evidence; destination origin + method + decision for attempted requests, with transition/time association and visible effects; focused control before Enter and active-element identity after Close/Back; no page source, bodies, answer payloads or full screenshots required merely for this ledger.

### Architecture — A5 / A6 / A7 and warning to QA

Exact decision challenged: A5's before-dispatch prevention for redirects and page-initiated requests and A6's choice of observed failure or blocked observation. Concrete failure cases: a top-level-only guard misses a third-party image/script or redirect hop; an allowed GET submits a form; an analytics block prevents a downstream state and the record still combines later checkpoints into a single passing journey. Source boundaries: `surface-contract.json:5-6,9-15,20`; `observation-policy.json:2-4`.

Smallest investigation: inspect A5/A6 and runtime sequence `architecture-analysis.md:49-54`, plus acceptance `:62-65`. Outcome: the before-dispatch/page-initiated/redirect requirement and dependent-step rule are already present, so the proposed omission is **refuted**. Keep explicit subresources in the final wording, because “page-initiated” must not be interpreted as top-level navigation only. Add/retain an action-layer no-form-submission rule independent of methods; A62 already says no form submission, so there is no GET-form permission in Architecture's full proposal. No new harness is justified. Guard capability is an unresolved future execution prerequisite. Severity stays High if an unsupported request surface bypasses enforcement; the likelihood and actual host behavior are unknown, not established security findings.

Answer to Architecture's warning: the QA matrix covers analytics effects, guards before navigation, redirect/subresource origin checks, distinct preactivation versus postactivation focus and unanswered indicators. Add the explicit dependent-step rule from A54 to the final QA matrix: an unestablished intermediate state cannot supply evidence for the next transition; do not jump ahead with direct focus/click or stitch checkpoints across runs. A separate restarted run is labeled separately, with no assumption a reload resets persistent answers. Prohibited actions/requests are tested through design review or offline guard fixtures, never deliberately sent to the live site.

### UX — D-UX-2 terminal row / D-UX-3 / acceptance 4

Exact decision challenged: D-UX-2's retained assertion that question/help are “absent” and acceptance 4's final absence observation (`ux-analysis.md:37,54`). Concrete failure case: a valid returned introduction hides question/help but retains their DOM nodes; a node-removal assertion fails the run despite satisfying the source state/focus contract. Source: target `:10` versus `surface-contract.json:15,17`, which require returned-introduction and h1 focus but do not prescribe removal.

Smallest investigation: compare the terminal row to Product P4, Architecture A8 and Delivery D6. Outcome: there is no source evidence for mandatory DOM detachment. **Resolved by correction:** UX sent an explicit cross-examination message revising this to optional supplemental “not visibly presented,” never DOM removal. Adopt that wording in the consolidated plan and downgrade its authority, not the observed failure severity of any actual focus obligation. Do not require a particular DOM mechanism.

Answer to UX's direct questions: QA distinguishes Enter-open, Space-close, Enter-reopen and explicit Close; each action has its own expected state, even though the initial matrix placed toggle/reopen in one row. For clearer acceptance bookkeeping split that row into distinct transition records. Close restores the relevant journey summary; Back reaches the returned introduction h1. Record focused Close/Back before Enter and active-element identity afterward. UX's message correctly says ambiguous multiple candidates yield inconclusive/unobserved, not an invented locator or focus correction. Severity of false keyboard/focus acceptance remains High; multiple matching DOM elements remain a Medium hypothesis until observed.

### Delivery — D2 / D5 / T5 / definition of done

Exact decisions challenged: D5's evidence summary emphasizes active element at the two destination checkpoints, while D2 calls for genuine traversal; T5 asks for source comparison/local validator. Concrete failure cases: final summary/h1 focus is logged but preactivation Back was directly focused rather than reached with Tab; or a checker pass hides a Close click/Shift+Tab mismatch. Source: contract `:14-15`; checker `:32-36,42-43` and the in-memory results above.

Smallest investigation: compare D2/D5/T5 with DoD `delivery-analysis.md:51-57` and Architecture A4. Outcome: Delivery already separates actual sequential traversal, Enter, state and focus (`:66`) and requires source coverage independent of validator. Thus no missing task or new automated checker is necessary. Clarify T5's manual review artifact: a seven-transition tuple comparison and eight-check mapping with an evidence field for preactivation focused Close/Back, not merely the two destination active elements. Severity remains High for false keyboard acceptance; no extra implementation scope follows.

Answer to Delivery's direct questions: yes, the QA proposal separates contract consistency, document coverage and future browser outcomes. All request surfaces, redirects and subresources require prevention before first navigation, while observation of expected analytics blocking preserves effects and does not grant journey success. A document can be accepted as covering these conditions while the browser/tool readiness check remains unperformed. Delivery's estimates are explicitly proposals bounded to one document; they are not empirical facts and this cross-pass does not validate their duration.

## Revisions and clarifications to my initial QA report

1. **Initial focus scope:** QA-2's blanket exclusion of direct focus must be read for proving declared traversal or focus outcomes. The source specifies Enter on summary but no initial traversal (`surface-contract.json:11`). Ordinary sequential navigation to summary is a useful proposed method, not an additional contract acceptance gate. Preserve UX's distinction: no invented post-open/post-toggle focus destination. If focus moves, observe it and record any ordinary recovery navigation; do not repair Close/Back focus before checking it.
2. **Unanswered evidence:** “visible/model-exposed” in the initial matrix is too broad. Use relevant publicly observable answer-control state, such as rendered/accessibility/DOM selection state if available, without assuming the website exposes a particular mechanism or accessing private application internals. Record how it was observed; hidden questionnaire state after Back remains unproven and is not needed. No answer interaction is used to test the indicator.
3. **Origin precision:** My “different port” negative case means a different **effective** origin, such as a nondefault port. Use parsed normalized URL origins, not URL text prefix/suffix checks. Explicit default HTTPS port does not by itself establish a different web origin. Userinfo text or a lookalike hostname does not confer authorization; the entry checker independently rejects credentials (`checks/check_contract.py:12-15`). Do not silently invent additional source-mandated URL syntax rules.
4. **Post-Back absence:** Retain only optional supplemental “question/help not visibly presented,” clearly distinguished from required returned-introduction and h1 focus. No DOM-node-removal requirement. This aligns with UX's correction, Product P4, Architecture A8 and Delivery D6.
5. **Split combined help row:** Record toggle-help and reopen-help separately so Space failure cannot hide behind a successful reopen or Close. All seven transition IDs need separate outcomes even if a prose table groups related actions.
6. **Dependency and causal reporting:** Adopt Architecture A54's no-stitching rule and maintain state/focus/policy outcome distinctions. A blocked analytics request need not occur: if absent, record not observed; never generate one to meet a checklist. If observed, block it and retain effects. The existing Gherkin analytics scenario is conditional, not a live-execution requirement.

No risk severity is reduced merely because a peer agrees. High policy/false-acceptance risks retain High impact, with likelihood/current occurrence explicitly unknown. The absence of browser evidence prevents factual claims about deployed defects or security incidents.

## Disposition and unfinished items

This single Workflow Cross-examine pass is complete: all five initial reports inspected, four peer decision groups challenged with concrete failures and smallest investigations, direct questions to QA answered, initial QA proposals revised where evidence warrants. Main selected approach survives: one source-traced document plan; exact seven transitions and Tab/Enter proof; independent unanswered and policy boundaries; compact evidence; separate source/document/browser status; no new harness required here.

Unfinished for the lead: adjudicate the clarified evidence/status wording and produce the consolidated specification/run evidence/lint. Unfinished runtime evidence: actual initial summary route, control uniqueness, public unanswered indicator, request enforcement/tool capability, effects of blocking, focus behavior and current deployment outcomes. Those require a separately authorized bounded observation and are not resolvable by this no-network planning pass. No further cross-examination round or peer waiting is requested.
