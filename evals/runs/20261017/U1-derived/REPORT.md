# Navigable copy of the original trial report

The [original report](final-output/REPORT.md) is preserved byte-for-byte with the original method record. This copy adjusts only links for this public layout. It does not revise findings, coverage or observations. Later independent qualification is recorded separately in `evaluation.json`.

The required keyboard Back transition passed. The scoped review result is **DO-NOT-SHIP**, with **PARTIAL coverage**: a repeated captured state shows the cookie banner concealing the focused Back control, and cold deep-link initialization remains untested.

This was actual operator-mediated browser execution using the supplied `qore-ux-review-qaizen-labs` skill. Input files remained unchanged; no answers, submissions, result generation or shared-data mutations were executed. Proposed corrections were not applied.

The reviewed surface was the anonymous public journey from `https://qaizen.io/labs` to the readiness introduction, unanswered first question, help open/closed, and returned introduction. Depth was `entry`, including neighboring states, with required G0–G6. The observed CSS viewport was 1280×800, DPR 1, English content, and the deployed default dark appearance with the cookie banner undismissed. Playwright 1.62.1 / Chromium 151.0.7922.34 ran through the neutral relay. Screenshots were actually opened and inspected.

The supplied run identity is `qore003-20261017-u1-derived-1`. Candidate SHA-256 is `8b26119f383a7d5853c1bd2ab5f678e08966300846c0d6f2784351c1f5a59e8d`; target SHA-256 is `b269181f3e44e5b4d84fe94ae1d683f85d2b8bde69f389d32d030b1e0909ef36`. The latter identifies the enclosing frozen prepared-input manifest, not a website deployment or one target file. The enclosing manifest serialization was not supplied, so that aggregate digest was retained as supplied. Independent per-file hashes and final unchanged comparisons are in [input-manifest.json](final-output/evidence/input-manifest.json) and [freshness-report.json](final-output/evidence/freshness-report.json). The live deployment commit is unknown.

The source-defined acceptance checks produced these observations:

| Check | Actual evidence and conclusion |
|---|---|
| Entry | Request 2 clicked the public card at 10:55:23 UTC and reached the distinct readiness introduction and Start control. |
| Unanswered | None-checked assertions passed at the first question, after Close, after Back, on restart, after reload and after history navigation. NEXT was disabled in question DOM captures. |
| Help toggle | Tab reached the summary; Enter opened help, Space closed it, and Enter reopened it. Each `open` attribute state was asserted. |
| Close focus | One Tab reached Close; Enter closed help and restored focus to the summary. Repeated in request 4. |
| Keyboard Back | One Tab from the restored summary reached Back at 10:55:45.798 UTC. Enter activated it. Back was neither clicked nor programmatically focused. |
| Introduction focus | At 10:55:53.390 UTC, the introduction was restored and the active element was its h1. Request 4 repeated the separate h1 assertion. |
| Read-only policy | Four analytics POST attempts to `/api/labs/readiness/event` were blocked. Every emitted console error correlated with those blocks; there were no page exceptions. The journey still completed. |
| Origin policy | The allowed-origin guard remained enabled. Recorded navigation and response events stayed on `qaizen.io`; no blocked navigation or route errors occurred. No deliberate off-origin activation was attempted. |

See [transition-report.json](final-output/evidence/transition-report.json), [network-console-review.json](final-output/evidence/network-console-review.json), and the complete raw [request 2 events](final-output/evidence/response-2/events.json).

**UX-1 — P2 / moderate: the cookie banner conceals focused Back in the captured keyboard state.** After closing help and pressing Tab, DOM evidence identifies Back as the active element, while its label and most of its gold focus ring sit behind the banner in the inspected [first capture](final-output/evidence/response-2/06-back-keyboard-focus.png). A fresh replay produced a [byte-identical capture](final-output/evidence/response-4/03-back-focus-obscuration-challenge.png). This reduces a sighted keyboard user's ability to identify the focused control.

The functional refutation matters: Back is reachable, Enter works, and introduction heading focus is restored. This finding does not establish a keyboard trap or failed Back transition. Evidence is limited to repeated full-page captures; fixed/sticky chrome appears at the captured scroll position. The relay exposes neither viewport-only captures nor overlap geometry/hit testing, so precise runtime overlap dimensions remain unmeasured. Cookie dismissal was outside the activation whitelist and was not used to hide the issue. A proposed correction is to reserve banner space and scroll sequentially focused controls into the unobscured viewport, then renew the journey evidence. Full severity, evidence and refutations are preserved in [findings.json](final-output/evidence/findings.json).

Reload and browser history were also observed. Reloading the introduction rendered it successfully. Reloading an unanswered question preserved that question with h2 focus. Browser Back returned to Labs; Forward restored the unanswered first question. Application Back instead stayed on the readiness URL and returned to its introduction. No supplied acceptance rule requires question reload to reset the introduction.

| Gate | Result | Evidence / limit |
|---|---|---|
| G0 | 4 | Actual public entry click and distinguishing introduction content. |
| G1 | PARTIAL; no aggregate score | Introduction/question reload and history observed. Fresh-context direct deep entry cannot be requested through this API. |
| G2 | 4 | Required help/Back states resolve, answers remain unselected, policy preserved. |
| G3 | 3 | UX-1 overlap in inspected PNGs; otherwise readable scoped layout. |
| G4 | 4 | Introduction, question and help copy inspected in DOM and rendered captures. |
| G5 | 3 | Keyboard reachability and distinct focus restoration pass; UX-1 affects visible identification. |
| G6 | 4 | Fresh focus challenge, restart isolation, reload/history and error correlation checked; refutations retained. |
| GP | NOT_APPLICABLE | Performance explicitly excluded by the supplied contract. |

The initial required set was preserved. G1 requires direct navigation as well as reload/history; the relay forces every fresh context to `/labs` and provides no `navigate` action. Reloading the deep document does not establish cold deep-link initialization. This is a driver coverage gap, not a website defect. The [capability matrix](final-output/evidence/capability-matrix.json) maps observed navigation, screenshot, DOM, keyboard, console and network capabilities to checks. Full questionnaire/results, mobile and accessibility/performance certification are explicitly outside scope. No contrast measurement, automated accessibility audit, screen-reader test or implementation-source review is claimed.

All phases were performed by the actual `/root` context. The invoked UX method requires sequential observation and challenge, not independent finder/planning/verifier roles. No subagents were requested or spawned; required/requested/returned/missing child rosters are empty, with the reason and real operator observation roster retained in [dispatch-roster.json](final-output/evidence/dispatch-roster.json). No independence claim is made for G6.

| Request | Relay start → return, UTC, 2026-10-17 | Outcome |
|---|---|---|
| 1 | 10:54:26.558 → 10:54:31.747 | Capability probe completed. |
| 2 | 10:55:19.742 → 10:55:57.377 | Complete required help/Close/Back journey. |
| 3 | 10:56:28.784 → 10:56:48.579 | Partial: authored exact uppercase text locator timed out. |
| 4 | 10:57:30.493 → 10:58:18.211 | Focus/overlap challenge completed; later authored h1-on-reload assumption timed out. |
| 5 | 10:59:00.136 → 10:59:16.174 | Reload/history outcome observation completed. |

Request 3 used visually uppercased heading text with exact underlying-text matching; a semantic heading assertion passed in request 4. Request 4 assumed question reload resets to the introduction; request 5 refuted that assumption. Both diagnostics and all unexecuted tails remain preserved. Neither assertion error is reported as a product defect. Five fresh contexts were used, with at most 38 requested actions in an array. No sixth request was dispatched.

Four loop iterations followed the separate capability preflight. The bundled stop-rule returned **STOP_PLATEAU** at iteration 4, with G3/G5 failing and G1 missing. No new browser dispatch followed that stop. The final result is neither a budget-exhaustion claim nor a successful completion claim. The immutable-input constraint also prevents applying a fix within this run. See [loop.json](final-output/loop.json), the four complete iteration reports, and [stop-rule-4.json](final-output/evidence/stop-rule-4.json).

The bundled profile preflight returned COMPLETE with both source digests current. Its consumed invariants drove the separate Close/Back assertions, sequential traversal and unanswered/policy checks; consumption is recorded in [profile-use.json](final-output/evidence/profile-use.json). Contract consistency and depth lint passed. The `qore-run/1` record in [execution.json](final-output/execution.json) binds the supplied identities, actual phase reports, command outputs, source revisions, receipts and evidence digests. Structural validation passed with declared PARTIAL coverage and the browser phase incomplete; see [run-check.json](final-output/run-check.json). Structural validity does not certify the reasoning.

The wall budget was 900 seconds and aggregate agent budget 2400 seconds; no child contexts ran. Root elapsed wall accounting is saved in [usage.json](final-output/usage.json). Token and billed agent-second usage are unavailable because this runtime exposes no usage telemetry; unavailable usage is not recorded as zero. The supplied candidate/target change timestamp is 09:53:58.639550 UTC, earlier than every actual observation. No correction invalidated those observations.

Remaining coverage is cold deep-link initialization and stronger viewport/geometry confirmation of the overlap. Trace/video files named by the probe were not exposed in feedback. A separate authorized run should provide those facilities, investigate the banner correction and renew every required gate after any change. This run stops with the demonstrated functional Back pass, open moderate visual/focus finding, and PARTIAL method coverage.
