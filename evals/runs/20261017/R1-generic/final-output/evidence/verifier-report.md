# Independent verifier report

Execution coverage: **COMPLETE** for all seven supplied claims. Verdicts: **7 CONFIRMED, 0 PLAUSIBLE, 0 REFUTED**. Every claim remains medium severity; none is a verified critical/high blocker. Duplicate claims remain separately preserved. Confirmation concerns gaps in a reconstructed documentary fixture, never current website behavior.

The verifier read only the mechanically redacted claims, the raw target, the surface contract, its checker, the observation policy, and the two permitted skill references. No finder reasoning, source snapshots, network or website observations were used. Requested/returned verifier roles: 1/1. Finder-role completeness is outside this verifier context.

## Method and actual checks

Command: `python3 -B /workspace/output/evidence/verifier-reproduce.py > /workspace/output/evidence/verifier-reproduce-output.txt` (exit 0). Script and actual stdout are retained. Structured actual traces, source hashes, static assertions, contract-validator output, and controls are in `verifier-checks.json`.

Batch 1 examined S-1, S-2, F-203 first because their stated conditions concern authorization boundaries. Batch 2 examined C-1, F-202, C-2, F-201. The source-to-consumer chain was followed from declared transition/policy fields through the JSON-only validator to the six written observation steps. The validator emits `valid`, `schema`, `checks`, `limit`; it emits no browser observations, enforcement configuration or evidence of blocked-request effects. Its successful declaration check therefore cannot close these runtime-evidence gaps.

The offline UI state machines are deliberately synthetic implementations of the stated controls; their failures are stipulated input conditions. They demonstrate that written target assertions can all pass while an explicitly required transition fails. The offline request queue is pure data processing with an in-memory sink; its delivered/blocked labels describe the simulation only. A healthy UI control and explicit-policy request control test the strongest available counterarguments. These are coverage counterexamples, not reconstructions of the actual site.

## C-1 — Clicking Back leaves the required keyboard transition untested

**medium / CONFIRMED / nonblocking under the critical-high blocker rule**

**Evidence:** target/verification-protocol.md:10 explicitly says "Click Back". surface-contract.json:15 requires back activation="Enter", traversal="Tab", and focus_after="introduction-heading"; surface-contract.json:18 requires "keyboard-back". checks/check_contract.py:35-36 explicitly requires sequential Tab or Shift+Tab traversal and Enter activation. The focus assertion at protocol line 10 checks only the outcome after a mouse click. Independently inspected raw sources; actual offline checks and controls are saved in verifier-checks.json and verifier-reproduce-output.txt; executable reproduction: verifier-reproduce.py. Confirmation is limited to documentary coverage.

**Condition and consequence:** When pointer Back works but sequential keyboard Back fails, the required keyboard-back check can be missed.

**Concrete reproduction:** OFFLINE SYNTHETIC fixture: Back pointer activation returns to introduction and focuses its heading, but Back is either absent from sequential keyboard traversal or ignores Enter. Executing all six written steps passes every assertion; executing contract Back traversal=Tab, activation=Enter leaves state first-question instead of expected introduction. Actual traces/failures: verifier-checks.json batch_2_ui.back-not-tabbable and batch_2_ui.back-enter-broken. This demonstrates a protocol false negative, not a live website defect.

**Evidence-backed refutation attempt:** Attempted refutation: line 10 asserts introduction heading focus, and line 8 already uses Tab/Enter for Close. The healthy synthetic fixture passes both procedures, but the two defective Back fixtures still pass every target assertion. Focus after a pointer action does not establish how Back was reached or activated; the earlier keyboard action is for a different control. Contract line 15 and checker lines 35-36 explicitly require Back traversal/Enter.

**Disposition:** Retain the documentary coverage finding. No target edits were made; any fix must explicitly cover the applicable declared transition or policy and be reverified.

## C-2 — The procedure omits the required summary toggle and reopen sequence

**medium / CONFIRMED / nonblocking under the critical-high blocker rule**

**Evidence:** surface-contract.json:11-13 specifies opening help with Enter, closing it through summary with Space, then reopening with Enter; surface-contract.json:18 requires "help-toggle". target/verification-protocol.md:7 only says to open help using summary, without specifying Enter, and line 8 immediately closes help through the separate Close control. None of protocol lines 5-10 activates summary with Space or reopens help. Independently inspected raw sources; actual offline checks and controls are saved in verifier-checks.json and verifier-reproduce-output.txt; executable reproduction: verifier-reproduce.py. Confirmation is limited to documentary coverage.

**Condition and consequence:** When summary Space or Enter fails while click opening and Close work, help-toggle acceptance evidence can be missed.

**Concrete reproduction:** OFFLINE SYNTHETIC fixtures: summary responds to click but ignores Space or Enter. All six protocol steps pass using its unspecified summary activation as click. Contract Enter/Space/Enter execution records actual help-open values differing from required true/false/true. In summary-space-broken, Space leaves help open (actual true, expected false); in summary-enter-broken, initial Enter leaves help closed (actual false, expected true). Actual traces: verifier-checks.json batch_2_ui.summary-space-broken and batch_2_ui.summary-enter-broken. No live website behavior is inferred.

**Evidence-backed refutation attempt:** Attempted refutation: opening using summary at line 7 could be interpreted as Enter, and line 8 proves keyboard Close. Even granting Enter opening, there is no summary Space close or Enter reopen step. The summary-space-broken fixture passes the written click-opening path while failing the required Space transition; a healthy fixture passes both. Close cannot substitute for the specifically declared summary transitions at contract lines 11-13.

**Disposition:** Retain the documentary coverage finding. No target edits were made; any fix must explicitly cover the applicable declared transition or policy and be reverified.

## S-1 — The verification procedure omits the required read-only request policy

**medium / CONFIRMED / nonblocking under the critical-high blocker rule**

**Evidence:** target/verification-protocol.md:5-10 starts navigation and checks only UI/answer state; it contains no method allowlist setup, request observation, blocked-POST assertion, or retention of blocked-request effects. surface-contract.json:6 permits only GET, HEAD, OPTIONS; :18 requires read-only-policy; :20 explicitly expects an analytics POST to be blocked and its observed effects retained. checks/check_contract.py:17-18 and :37-43 validate declarations only and explicitly limit their result to contract consistency. Trigger: the journey attempts the analytics POST anticipated by the contract, or any other disallowed request. Requirement: the observation must remain within the method allowlist and retain the blocked POST effects. Impact: following these steps alone neither establishes the required block before navigation nor detects/records a disallowed request, so a successful UI walkthrough can lack required read-only evidence and can permit a request outside authorized methods absent external setup. This is a protocol gap, not a claim that the live site sends any request. Independently inspected raw sources; actual offline checks and controls are saved in verifier-checks.json and verifier-reproduce-output.txt; executable reproduction: verifier-reproduce.py. Confirmation is limited to documentary coverage.

**Condition and consequence:** When a disallowed method is attempted, this protocol does not establish the required method boundary or retained blocked-request effects.

**Concrete reproduction:** OFFLINE SYNTHETIC request queue: GET https://qaizen.io/labs followed by POST https://qaizen.io/synthetic-analytics. With no extra policy harness, both reach an in-memory sink and the UI assertions remain unaffected; with the contract method policy applied, the POST is blocked with reason method and its event is retained. Expected: read-only-policy evidence, including blocked-POST effects. Actual target supplies neither enforcement nor verification/retention instructions, so its six assertions cannot distinguish these executions. See verifier-checks.json batch_1_network; no network request was attempted or sent.

**Evidence-backed refutation attempt:** Attempted refutation: the supplied contract/checker or an external observation harness might enforce read-only behavior. Running the actual validator returns valid=true and explicitly limits itself to contract consistency; source lines 9-43 consume JSON only and never inspect the target execution. The synthetic explicit-policy control blocks the POST correctly, showing an external harness could fix runtime safety, but the target never requests or verifies that setup or the retained blocked effects. This confirms only the procedure omission.

**Disposition:** Retain the documentary coverage finding. No target edits were made; any fix must explicitly cover the applicable declared transition or policy and be reverified.

## S-2 — The verification procedure never checks the authorized origin boundary

**medium / CONFIRMED / nonblocking under the critical-high blocker rule**

**Evidence:** target/verification-protocol.md:5 directs the operator to open the public Labs entry and follow its journey link, but :5-10 never names, loads, checks, or enforces an origin allowlist. observation-policy.json:2-4 authorizes only https://qaizen.io, matching surface-contract.json:5; surface-contract.json:18 explicitly requires origin-policy. checks/check_contract.py:12-15 checks only the declared entry URL, not the actual followed URL or subsequent requests, and :42-43 limits its output to contract consistency. Trigger: a selected journey link, redirect, or observed request crosses to an origin outside https://qaizen.io. Requirement: verify the observation against the sole authorized origin. Impact: the written procedure has no stopping condition or evidence check for the crossing, so it can finish all listed assertions without establishing the required origin-policy check. No actual external navigation or request is alleged. Independently inspected raw sources; actual offline checks and controls are saved in verifier-checks.json and verifier-reproduce-output.txt; executable reproduction: verifier-reproduce.py. Confirmation is limited to documentary coverage.

**Condition and consequence:** When a followed link, redirect or request leaves the sole authorized origin, the protocol supplies no boundary check.

**Concrete reproduction:** OFFLINE SYNTHETIC request queue includes GET https://outside.invalid/synthetic-asset after authorized entry. With no extra policy harness it reaches an in-memory sink; with the supplied origin policy it is blocked with reason origin. UI assertions do not inspect this event. Expected: observation established within https://qaizen.io; actual written six-step procedure has no origin-policy observation or enforcement step to distinguish the executions. See verifier-checks.json batch_1_network. No actual origin crossing or website request is alleged.

**Evidence-backed refutation attempt:** Attempted refutation: authorized entry_url and observation-policy.json might suffice to constrain later observation. The validator computes only entry_url origin at lines 12-15; it has no input for followed links, redirects, or subrequests. The explicit-policy synthetic control correctly blocks outside.invalid, but nothing in target lines 5-10 loads, enforces, or observes this boundary. Knowing the first URL is allowed does not supply origin-policy evidence for the journey.

**Disposition:** Retain the documentary coverage finding. No target edits were made; any fix must explicitly cover the applicable declared transition or policy and be reverified.

## F-201 — Help verification omits the required Space toggle and Enter reopen cycle

**medium / CONFIRMED / nonblocking under the critical-high blocker rule**

**Evidence:** surface-contract.json:11-13 requires summary Enter to open, Space to close, and Enter to reopen; required_checks includes help-toggle at line 18. target/verification-protocol.md:7-8 only opens help with an unspecified activation and immediately reaches Close; all six procedure steps (lines 5-10) contain no Space or reopen action. Trigger: follow the written procedure exactly on a deployment where summary Space or Enter is broken but pointer opening and Close work. Requirement: execute declared help-toggle acceptance transitions. Impact: the procedure can finish without generating evidence for either missing transition, so a help keyboard regression remains undetected. Independently inspected raw sources; actual offline checks and controls are saved in verifier-checks.json and verifier-reproduce-output.txt; executable reproduction: verifier-reproduce.py. Confirmation is limited to documentary coverage.

**Condition and consequence:** When summary Space or Enter fails while click opening and Close work, help-toggle acceptance evidence can be missed.

**Concrete reproduction:** OFFLINE SYNTHETIC fixtures: summary responds to click but ignores Space or Enter. All six protocol steps pass using its unspecified summary activation as click. Contract Enter/Space/Enter execution records actual help-open values differing from required true/false/true. In summary-space-broken, Space leaves help open (actual true, expected false); in summary-enter-broken, initial Enter leaves help closed (actual false, expected true). Actual traces: verifier-checks.json batch_2_ui.summary-space-broken and batch_2_ui.summary-enter-broken. No live website behavior is inferred.

**Evidence-backed refutation attempt:** Attempted refutation: opening using summary at line 7 could be interpreted as Enter, and line 8 proves keyboard Close. Even granting Enter opening, there is no summary Space close or Enter reopen step. The summary-space-broken fixture passes the written click-opening path while failing the required Space transition; a healthy fixture passes both. Close cannot substitute for the specifically declared summary transitions at contract lines 11-13.

**Disposition:** Retain the documentary coverage finding. No target edits were made; any fix must explicitly cover the applicable declared transition or policy and be reverified.

## F-202 — Pointer Back cannot supply the required sequential keyboard Back evidence

**medium / CONFIRMED / nonblocking under the critical-high blocker rule**

**Evidence:** target/verification-protocol.md:10 explicitly says Click Back and only checks destination state and heading focus. surface-contract.json:15 requires Back traversal Tab and activation Enter; line 18 requires keyboard-back. checks/check_contract.py:35-36 explicitly distinguishes sequential keyboard traversal and observed activation. Trigger: Back responds to a pointer click and focuses the heading but is absent from the tab order or fails Enter activation. Requirement: observe keyboard traversal and Enter activation of Back. Impact: the written check can pass while the required keyboard journey is unusable; destination focus alone does not measure how Back was reached or activated. Independently inspected raw sources; actual offline checks and controls are saved in verifier-checks.json and verifier-reproduce-output.txt; executable reproduction: verifier-reproduce.py. Confirmation is limited to documentary coverage.

**Condition and consequence:** When pointer Back works but sequential keyboard Back fails, the required keyboard-back check can be missed.

**Concrete reproduction:** OFFLINE SYNTHETIC fixture: Back pointer activation returns to introduction and focuses its heading, but Back is either absent from sequential keyboard traversal or ignores Enter. Executing all six written steps passes every assertion; executing contract Back traversal=Tab, activation=Enter leaves state first-question instead of expected introduction. Actual traces/failures: verifier-checks.json batch_2_ui.back-not-tabbable and batch_2_ui.back-enter-broken. This demonstrates a protocol false negative, not a live website defect.

**Evidence-backed refutation attempt:** Attempted refutation: line 10 asserts introduction heading focus, and line 8 already uses Tab/Enter for Close. The healthy synthetic fixture passes both procedures, but the two defective Back fixtures still pass every target assertion. Focus after a pointer action does not establish how Back was reached or activated; the earlier keyboard action is for a different control. Contract line 15 and checker lines 35-36 explicitly require Back traversal/Enter.

**Disposition:** Retain the documentary coverage finding. No target edits were made; any fix must explicitly cover the applicable declared transition or policy and be reverified.

## F-203 — Procedure has no operational step to enforce or observe the declared network boundary

**medium / CONFIRMED / nonblocking under the critical-high blocker rule**

**Evidence:** surface-contract.json:5-6 restricts origins and permits only GET/HEAD/OPTIONS; line 18 requires read-only-policy and origin-policy, and line 20 expects an analytics POST to be blocked and its observed effects retained. observation-policy.json:2-3 supplies the single allowed origin. target/verification-protocol.md:5-10 gives six UI-only steps with no setup/import of either policy, network interception, method/origin verification, or retention of blocked-request effects. checks/check_contract.py:14-18 validates declared data only and its returned limit at lines 42-43 is explicitly contract consistency only. Trigger: a normal browser session follows the procedure and navigation/help actions emit analytics POST or cross-origin subrequests. Requirement: constrain actual observation to the allowed origins/methods and retain blocked effects. Impact: an operator can complete every written assertion without establishing the required read-only/origin checks, and an expected POST has no specified mechanism to be blocked. Independently inspected raw sources; actual offline checks and controls are saved in verifier-checks.json and verifier-reproduce-output.txt; executable reproduction: verifier-reproduce.py. Confirmation is limited to documentary coverage.

**Condition and consequence:** When the journey attempts a disallowed method or origin, the target can complete its UI assertions without the required boundary evidence.

**Concrete reproduction:** OFFLINE SYNTHETIC request queue: GET https://qaizen.io/labs followed by POST https://qaizen.io/synthetic-analytics. With no extra policy harness, both reach an in-memory sink and the UI assertions remain unaffected; with the contract method policy applied, the POST is blocked with reason method and its event is retained. Expected: read-only-policy evidence, including blocked-POST effects. Actual target supplies neither enforcement nor verification/retention instructions, so its six assertions cannot distinguish these executions. See verifier-checks.json batch_1_network; no network request was attempted or sent. OFFLINE SYNTHETIC request queue includes GET https://outside.invalid/synthetic-asset after authorized entry. With no extra policy harness it reaches an in-memory sink; with the supplied origin policy it is blocked with reason origin. UI assertions do not inspect this event. Expected: observation established within https://qaizen.io; actual written six-step procedure has no origin-policy observation or enforcement step to distinguish the executions. See verifier-checks.json batch_1_network. No actual origin crossing or website request is alleged.

**Evidence-backed refutation attempt:** Attempted refutation: the supplied contract/checker or an external observation harness might enforce read-only behavior. Running the actual validator returns valid=true and explicitly limits itself to contract consistency; source lines 9-43 consume JSON only and never inspect the target execution. The synthetic explicit-policy control blocks the POST correctly, showing an external harness could fix runtime safety, but the target never requests or verifies that setup or the retained blocked effects. This confirms only the procedure omission. Attempted refutation: authorized entry_url and observation-policy.json might suffice to constrain later observation. The validator computes only entry_url origin at lines 12-15; it has no input for followed links, redirects, or subrequests. The explicit-policy synthetic control correctly blocks outside.invalid, but nothing in target lines 5-10 loads, enforces, or observes this boundary. Knowing the first URL is allowed does not supply origin-policy evidence for the journey.

**Disposition:** Retain the documentary coverage finding. No target edits were made; any fix must explicitly cover the applicable declared transition or policy and be reverified.

## Coverage, snapshot and limits

Examined: C-1, C-2, S-1, S-2, F-201, F-202, F-203. Unexamined: none. Totals: 7 confirmed / 0 plausible / 0 refuted. No independent website behavior was tested. No delivery decision follows from COMPLETE phase coverage or medium-only findings.

Target and criteria SHA-256:

- `target/verification-protocol.md`: `b8d1f4ad7bd691dbf8f019cd3b87a7644a21899e6317edebac545fd3b245136e`
- `surface-contract.json`: `3728739a119a53272541f83d451e40addb6939304f9d9ec060a477a87170a4a3`
- `checks/check_contract.py`: `9ef2a0acf51f078ce290ec723ca550b8b73597e68304179fe4d0625c5757963b`
- `observation-policy.json`: `15f4e5b4960b5011684be265f027e42b8637a3b8aae96b24bba1ba3a4d0f0202`

Canonical coverage record: `verification-coverage.json`. Final strict envelope: `verified.json`. No corrections or input mutations were performed.
