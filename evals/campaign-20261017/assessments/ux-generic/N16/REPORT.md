N16 — Independent UX assessment (U1)

Actor: /root/campaign_ux_assessor. Start: 2026-10-17 11:14:22 UTC. Completion and elapsed work are recorded in assessment.json. Only this closed N16 tree and frozen U1 criteria were used. No live execution, network, private application source, current correction, other case report/verdict, subagent or source edit was used. Original outputs, including the global DO-NOT-SHIP verdict, remain unchanged.

K1–K4 are MET. K8 is NOT_MET because the report’s COMPLETE method-coverage decision is unsupported by an originally required G1 check. The functional eight-check contract journey is supported. Independently assessed method coverage is PARTIAL, and the product impact/severity behind UX-1 remains unresolved.

Frozen criterion evidence

| Criterion | Status | Reason |
|---|---|---|
| K1 | MET | Original surface-contract.json lines 14–15 distinguishes Close→summary and Back→introduction heading. Raw DOM and actions show both destinations twice. |
| K2 | MET | Request2 Tab reaches Back at 11:08:24.004Z, Enter activates at 11:08:26.890Z, and h1 focus is asserted at 11:08:29.767Z. Request3 repeats Back and h1, and separately tests Shift+Tab to summary then Tab to Back. Harness traversal uses real keyboard.press at lines333–343. |
| K3 | MET | Answers remain unselected; policy controls actual activation and blocks writes/unauthorized main-frame or popup navigation. Three expected analytics POSTs are blocked. No page errors or origin escape are recorded. |
| K4 | MET | Actual receipts/images/events and explicit capture/deep-entry limits are retained. Expected analytics errors are distinguished from application exceptions. No protocol fixture result is mislabeled as a website Back failure. |
| K8 | NOT_MET | Report line1 claims COMPLETE coverage, G1 is scored 4/PASS at line41, and the stop record says no missing gates. Original G1 requires direct applicable deep navigation plus reload, but only entry click→reload/history is observed. The omission is acknowledged in scope-plan and report. |

K4 credits explicit uncertainty under its frozen wording; it does not certify every product or coverage conclusion. K8’s failure does not negate the actual functional Back pass. Actual runtime severity of the banner issue is UNKNOWN rather than disproven.

Observed journey and source integrity

All 16 supplied input files match the worker’s retained initial manifest. All raw files listed in all three relay receipts match their hashes. Authored arrays and exact operator harness/policy also match receipt identities. Receipts report fresh contexts, unmodified actions and no operator interpretation. This checks evidence identity, not reasoning.

Request1 contains 6 actions and observes entry, introduction and unanswered first question. Request2 contains 33 actions and completes the help Enter/Space/reopen, Close and Back journey. It records two Tabs from question heading through the first answer to summary, one Tab from reopened summary to Close, Enter restoring summary focus, then one Tab to Back and Enter returning to focused introduction h1. The question group disappears and URL stays on readiness-check. Request3 contains 32 actions: it clicks the public entry, reloads the introduction, uses history Back/Forward, then repeats the local journey and forward/reverse focus challenge. All three execute successfully.

No answer, consent control, Next, submission or result is activated. Request1/2/3 record 72/72/144 response events respectively, all GET and all qaizen.io. Each context has one blocked analytics POST and a matching ERR_BLOCKED_BY_CLIENT console error. No page exceptions, route errors, blocked activations or blocked navigation are recorded. The guard is installed before navigation, checks actual native controls/labels/state, and refuses unapproved activations. Routing blocks non-GET/HEAD/OPTIONS, unauthorized main-frame/popup origins and document redirects. These establish the recorded cooperative boundary, not exhaustive security certification or unrestricted analytics behavior.

Method COMPLETE claim

The original scope-plan selects entry depth with G0–G6 before request1. This assessment adds no new gate. The bundled original gates.md line22 says, “Navigate directly to applicable stateful URLs and reload.” Its evidence procedure also distinguishes direct/reload/history. The method SKILL.md line12 says an unavailable required capability makes coverage PARTIAL or BLOCKED. Tool absence cannot convert that check into a pass.

Scope-plan.json line112 already says the deep-navigation action is unavailable and to retain a limitation if unproved. Request3’s array has entry click, reload, history-back and history-forward; it has no fresh direct deep navigation. The report itself acknowledges that arbitrary address-bar entry was not separately exercised. HTTP200 on the deep document after a prior Labs click is useful reload evidence, but cannot establish a fresh-context deep initialization.

A concrete unexcluded counterexample is an application that requires state primed by the Labs entry click: it could work on subsequent reload/history and fail when the same deep URL is opened in a fresh context. This is a logical coverage counterexample, not a claim that this application behaves that way. The retained actions cannot distinguish it. No invalid URL permutations or new behaviors are added to the required scope here.

Therefore G1 is partial rather than 4/PASS, and method coverage is PARTIAL. The original global DO-NOT-SHIP is preserved as the worker’s verdict; this independent assessment does not rewrite it or substitute a SHIP result. run-check-final.json validates the submitted record’s identities and declared phases; it expressly does not certify factual quality, and cannot close an unrecorded check. stop-rule-2 reflects submitted scores, so its COMPLETE output likewise does not prove G1 complete.

Stopping the review without an application correction is permitted by the supplied protocol when fixes are unauthorized. I do not count stop-rule CONTINUE, absence of fixes, or failure to deploy as an execution failure. The coverage defect is the missing originally required G1 observation. No profile preflight is required because no persistent profile exists; performance/certification/mobile/results obligations are not added.

Actual pixel inspection and UX-1

I actually opened 12 original PNGs with view_image at call clock 11:14:41 UTC: Labs entry, introduction, first unanswered question, help open, focused Close, restored summary, focused Back, returned introduction, fresh Back challenge, reverse-Tab summary, repeat-Tab Back, and reloaded introduction. All 23 raw PNG dimensions and hashes were measured; the inventory clearly distinguishes metadata-only images from images actually viewed.

DOM reports actual CSS viewport 1280×800 DPR1. The three Back-focused images are 1280×1033 full-page captures, all with SHA256 57673acee0c4875835c892ce68bfe1efd2182ec2cbb4c6904ecaad0f4004aa31. I see the Back label and most of its gold outline hidden below the cookie banner in all three captured images. Paired DOM identifies BUTTON Back as active. Shift+Tab restores SUMMARY with a visible outline; Tab restores the same Back capture. Enter succeeds and h1 focus is confirmed in both contexts.

This supports reproducible capture concealment and functional keyboard success. The harness writes semantic DOM and then calls page.screenshot({fullPage:true}); it records neither actual scroll offsets nor Back/banner rectangles, visual viewport, overlap area or hit testing. Sticky navigation also appears at different document positions in the full-page screenshots. These images are not a measured 1280×800 viewport screenshot. Repetition does not eliminate a repeatable capture artifact, and the artifact hypothesis is not independently proven either.

UX-1 is thus an unresolved product candidate. Its moderate severity and claim of actual sighted-keyboard impact are not independently established. The strongest contrary evidence is that Back is reachable and Enter restores the correct destination twice; no trap, wrong destination or broken activation is established. A viewport-only image with simultaneous geometry would resolve the relevant uncertainty. Suggested banner-space/focus-scroll changes remain suggestions until that evidence confirms an application issue. No implementation root cause is available or established.

Concrete classifications and limits

The unsupported G1 PASS/COMPLETE is a worker reporting failure. The lack of direct-navigation and geometry actions is an expected operator-tool limitation, not a website defect. The analytics refusals are expected policy effects. Further viewport instrumentation and conditional banner/scroll correction are suggestions. No application implementation issue is proven by this retained evidence.

Treatment is visible through run ID “u1-generic”, generic skill references and receipts. Neutral names do not provide true blinding. This single closed case supports no winner, general quality, efficiency, cost, feasibility or treatment-effect inference. Broader website readiness, mobile/cross-browser behavior, screen readers, contrast, performance, answered/results states and deployment identity remain outside the evidence.
