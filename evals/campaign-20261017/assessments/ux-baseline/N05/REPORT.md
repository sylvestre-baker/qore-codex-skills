N05 — Independent UX assessment (U1)

Actor: /root/campaign_ux_assessor. Start: 2026-10-17 11:08:08 UTC. Completion and elapsed time are recorded in assessment.json. Scope is this closed neutral N05 tree and the frozen U1 criteria. I did not read another case’s report/verdict, change original outputs or sources, make new live/network observations, or delegate. No Qore method is invoked in the original TASK, so no Qore phases are required here.

All five applicable frozen criteria are MET. The required functional Back journey is supported by actual actions, DOM and viewed images. The visual banner concern remains conditional; its actual viewport impact and severity are not independently confirmed. The report’s limited conclusion is appropriate and does not claim a SHIP/DO-NOT-SHIP product decision.

Frozen criterion evaluation

| Criterion | Result | Evidence |
|---|---|---|
| K1 | MET | Original surface-contract.json lines 14–15 defines distinct destinations. The Close-result DOM has SUMMARY “What does this mean?” active; the Back-result DOM has the introduction H1 active. The report preserves this distinction. |
| K2 | MET | Request2 events record sequential Tab reaching Back at 11:04:02.890Z, focus assertion at 11:04:03.794Z, Enter at 11:04:05.787Z, and introduction h1 focus assertion at 11:04:09.570Z. Harness lines333–343 use actual keyboard presses and compare activeElement; there is no programmatic focus or authored Back click. |
| K3 | MET | No-checked assertions pass before help and after Close while the question exists. NEXT is disabled. Hash-matched harness and policy enforce approved control activation, block writes and unauthorized main-frame/popup navigation. The expected analytics POST is blocked. |
| K4 | MET | Evidence and explicit limits are retained. Script failure, blocked analytics, full-page uncertainty, unavailable trace/video and deployment identity limits are not turned into a website Back defect. One precise diagnostic correction is noted below. |
| K8 | MET | The scoped decision is a functional contract pass in one replay plus a conditional visual concern. The report requests viewport confirmation before a possible banner/scroll correction and avoids a product-blocking or certification claim. |

Actual execution and integrity

Request1 authored five actions. Entry and introduction are observed, but the Start activation is refused. Request2 authors 34 actions and completes the entire journey with 17 successful assertions. It reaches the help summary using two Tabs from the question heading, Enter opens help, Space closes it, Enter reopens it, one Tab reaches Close, and Enter restores summary focus. One subsequent Tab reaches Back; Enter restores the introduction with focused h1. The URL stays on readiness-check. These transitions exceed the automatic Tab capability probe and directly prove the required journey.

I independently checked all four supplied source hashes against input-sha256.json. Both action-array hashes, all relay-listed raw file hashes, and exact operator harness/policy hashes match their receipts. Both receipts state fresh contexts and unmodified actions. Each request records 72 response events, all GET and all qaizen.io. Request2 records one POST attempt to /api/labs/readiness/event at 11:03:41.969Z, blocked by read-only policy, and a matching console error at 11:03:41.973Z. No page exceptions, route errors or blocked navigation occur. Request1 has a guard refusal for the malformed locator; request2 has no blocked activations.

The operator harness installs the activation guard before navigation. It checks actual native controls, labels, attributes and required state; only approved entry, Start, summary, Close and Back descriptors exist. Tab traversal does not select answers. The route handler blocks non-GET/HEAD/OPTIONS requests, unauthorized main-frame/popup navigation and redirect following. This supports the observed guarded run. It is not exhaustive security isolation or an adversarial off-origin test. No answers, consent actions, Next, result generation or submissions are present.

Actual screenshot inspection and viewport limits

I actually opened eight original PNGs using view_image at the tool call clock 11:08:19 UTC: public entry, introduction, first unanswered question, open help, Space-closed help, Close result, Back focused, and Back result. The complete inventory records which remaining PNGs were metadata-only. All 12 retained raw PNG dimensions and hashes were independently measured from bytes.

The DOM reports actual CSS viewport 1280×800 DPR1. The Back-focused PNG is 1280×1033, and the source explicitly requests fullPage:true at harness line244. The image shows only a narrow gold edge of Back’s outline above the cookie banner; the label is concealed in these captured pixels. The paired DOM establishes that Back is focused. The summary has a clearly visible outline after Close; the returned introduction is visually distinct and its h1 focus is established in DOM.

No scroll offsets, bounding rectangles, visual viewport, overlap area or hit testing are retained. The full-page images also place sticky navigation at different document positions across states. Therefore the image is not a measured 1280×800 viewport capture. The evidence cannot establish whether ordinary runtime overlap is the same or whether capture behavior contributes. There is only one Back-focused capture in this case, so no repeated reliability or visual reproduction is established.

The worker’s description of “medium potential impact” and “medium confidence” is a qualified judgment, not measured severity. Its conditional follow-up is appropriate: obtain viewport-only confirmation with the banner present and then consider banner-space/focus-scroll changes if confirmed. I classify that code-change proposal as a suggestion and the visual concern as an unresolved product candidate. Keyboard reachability and activation succeed, countering any broader claim of inability to return, trap or formal accessibility failure. No application implementation defect is established from the retained evidence.

Concrete report correction

REPORT line22 attributes request1’s Start failure to exact text case. The actual action is {type:click,text:Start the check,exact:true}, with no role or selector. At harness line297, click locators resolve only role/name or selector; action.text is not used for click. Thus the supported cause is an unsupported locator shape, irrespective of capitalization. The generic refusal does not prove a case-sensitive text match failed. This is a worker diagnostic error, correctly categorized as an observation-script failure overall, repaired by request2’s supported selector. It is not a product defect and does not invalidate the final successful journey. The original report remains unchanged.

Coverage and limits

All eight checks selected by the actual source contract have evidence within the requested task. The baseline invokes no Qore profile, gates, loop, independent roles or execution.json workflow; their absence is not missing coverage. Cold direct deep navigation and browser history are not added as later obligations. The structural contract/evidence checkers are retained as mechanical checks, not proof of reasoning.

The broader product evaluation remains limited to one desktop replay, unanswered first question, deployed default appearance and blocked analytics. Actual viewport focus visibility, banner-dismissed behavior, screen-reader usability, contrast, cross-browser/mobile, full questionnaire/results, performance and certification are unobserved. The exact harness config sets en-US; DOM reports en. No deployment commit is independently identified.

The run identity and result labels reveal “u1-baseline”, and the report explicitly states that no Qore skill was invoked. Neutral filenames are not true blinding. No comparison, winner, general quality, cost, feasibility or efficiency inference is made.
