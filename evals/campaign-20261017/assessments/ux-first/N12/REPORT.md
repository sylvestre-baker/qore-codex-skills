N12 — Independent UX assessment (U1)

Actor: /root/campaign_ux_assessor. Assessment began 2026-10-17 11:03:39 UTC. Completion time and elapsed wall time are recorded in assessment.json. This assessment reads only N12 and the frozen criteria.json in its parent. Original frozen worker inputs and operator harness/policy copies were added to N12 during the assessment; all supplied source hashes and operator identities were independently checked. No new browser/model/network request, source edit, outreach, or subagent was used.

The required functional Back journey is supported. Method execution remains PARTIAL. The banner finding is a plausible product candidate whose actual viewport impact remains unresolved; I do not independently endorse its P2 severity or treat the worker’s DO-NOT-SHIP as a proven website defect.

Frozen criterion results

| Criterion | Result | Evidence and interpretation |
|---|---|---|
| K1 | MET | Original surface-contract.json lines 14–15 requires Close→summary and Back→introduction heading separately. Request2 snapshots show SUMMARY after Close and H1 after Back; the report retains that distinction and source provenance. |
| K2 | MET | Request2 events at 10:55:45.798Z record one sequential Tab reaching Back; Enter at 10:55:48.698Z; h1 focus assertion at 10:55:50.515Z. Request4 repeats at 10:57:47.674Z,10:57:50.576Z,10:57:51.488Z. Harness lines333–343 implement real keyboard presses; no programmatic focus or authored Back click is used. Native click events following Enter are expected keyboard activation evidence. |
| K3 | MET | Unanswered assertions succeed. Matching operator harness/policy enforce approved controls, block non-GET/HEAD/OPTIONS requests and unauthorized main-frame/popup navigation, and block service workers. Four analytics POSTs are blocked, with four correlated console errors and no page exceptions. All recorded response/navigation origins are qaizen.io. |
| K4 | MET | Actual evidence and explicit uncertainty are retained. REPORT line26 limits the visual claim to full-page captures and admits missing geometry; G1 is partial. The two assertion errors are recognized as authored-check errors. The original protocol proof gap is not called an application Back failure. This criterion credits explicit uncertainty; it does not certify UX-1. |
| K8 | UNKNOWN | Back-pass and PARTIAL coverage conclusions are supported. The whole product verdict additionally relies on a P2 visual finding whose actual viewport impact cannot be resolved from retained captures. The evidence supports a captured concealment candidate; whether it supports a product-blocking DO-NOT-SHIP remains unknown. |

Evidence integrity and actual execution

All 17 files listed in the worker’s input-manifest have matching hashes in the supplied original input copy. Every raw file listed in all five operator relay receipts matches its recorded hash. The retained browser_probe.mjs and live-policy.json match the exact harness/policy hashes used by all receipts. Receipts report fresh contexts and unmodified action arrays. This is evidence identity verification, not independent proof that every interpretation is correct.

The authored arrays contain 0,31,38,38,11 actions respectively. Request2 executes the complete required public-entry, Start, help Enter/Space/reopen, Close and Back sequence. Request4 repeats the Close/Back focus challenge, then fails later on an unsupported reload assertion. Request3 stops after entry when the uppercase exact locator fails; its long unexecuted tail is not observation. Request5 observes reload and browser history without assuming a reset. No sixth request is present.

The worker’s report is treatment-revealing: its run ID contains “u1-derived”, it invokes a project derivative skill, and operator paths identify that condition. Neutral naming is not true blinding. This assessment makes no comparative, winner, quality or efficiency inference.

Actual image and measurement inspection

I actually opened 11 original PNGs with view_image: entry; introduction; first question; help open; Close-summary focus; Back focus; returned introduction; fresh Close-focus and Back-focus challenge; and question-reload/history-forward states. The complete viewed-versus-metadata-only inventory is in inspection-inventory.json. All 23 raw PNG dimensions/hashes were measured from bytes. Metadata-only images are explicitly not marked viewed.

The actual CSS viewport in DOM is 1280×800 at DPR1. The two Back-focus PNGs are 1280×1033 and byte-identical (SHA256 57673acee0c4875835c892ce68bfe1efd2182ec2cbb4c6904ecaad0f4004aa31). Both paired DOM snapshots identify BUTTON Back as active. In both images I see only the top of the gold Back outline above the cookie banner; the Back label is concealed in these full-page capture pixels. Close-summary focus has a clear visible outline, the expanded Close challenge has its own outline, and the returned introduction is visually distinct.

The harness records DOM before calling page.screenshot({fullPage:true}) at lines231–246. It does not record scroll offsets, bounding rectangles, visual viewport, overlap area or hit testing, and exposes no viewport-only snapshot action. The captures also place fixed/sticky navigation at different document positions across focus states. Full-page pixels therefore cannot be treated as a measured 1280×800 viewport screenshot. A repeatable capture procedure may repeat a sticky-overlay artifact. Conversely, these limitations do not prove that the real overlap is an artifact. Runtime overlap is unresolved, with a plausible product risk.

Product finding and concrete corrections

UX-1 remains an UNRESOLVED_PRODUCT_CANDIDATE. The captured concealment and Back active element are supported. The assertion that a sighted keyboard user cannot identify Back in the actual viewport, the P2 severity and a product blocker require stronger evidence. The functional counterexample is decisive against broader failure claims: Tab reaches Back and Enter restores introduction h1 focus twice. There is no evidence of a keyboard trap, broken Back transition, standard violation or application implementation cause.

The proposal to reserve cookie-banner space or add scroll padding is a suggestion until actual viewport geometry confirms the problem. A future authorized observation should capture the viewport and Back/banner rectangles simultaneously with scroll offsets, then decide whether an application correction is warranted. Cookie acceptance/rejection is outside this run’s approved activation descriptors; its absence is an expected scope limitation and should not be repaired by unauthorized consent activation.

Two worker failures are established and corrected: request3 uses an exact uppercase locator for underlying mixed-case heading text; request4 assumes unanswered-question reload must return to h1 despite no such contract requirement. The later checks correct both assumptions. These are not product issues. Missing cold direct navigation and geometry are expected relay limitations. No application implementation issue is established here.

Method coverage, separately

The supplied original method selects entry depth and requires G0–G6. G1 includes direct stateful navigation as well as reload/history. The exposed action API supports reload/history but no new navigate action; every relay call starts at /labs. Introduction reload and question reload/history do not establish cold deep-link initialization. PARTIAL coverage is therefore supported. GP, full questionnaire, answers/results, mobile and certification are excluded by the actual source scope; this assessment adds no later baseline obligations.

Original profile/checker reports are retained and bind current sources; separate focus and unanswered checks demonstrate fact consumption. The structural run-check accepts the declared PARTIAL record and explicitly does not certify reasoning. The stop-rule returns STOP_PLATEAU with G1 missing and G3/G5 below 4; that reflects submitted scores and cannot independently validate the visual product finding. Request5 is a reload/history observation, not a third Back-focus challenge, so future summaries should keep the Back evidence attached to requests2/4.

The independently defensible outcome is: functional Back journey supported; method PARTIAL; visual product candidate unresolved; product readiness PENDING. No general benefit, quality, efficiency, cost or winner conclusion follows from this single closed case.
