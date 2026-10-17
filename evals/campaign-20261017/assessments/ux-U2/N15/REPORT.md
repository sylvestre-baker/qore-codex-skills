# N15 / U2 independent criterion assessment

Actor: `/root/campaign_ux_last_assessor`. UTC start: 2026-10-17T12:13:43Z; end: 2026-10-17T12:15:47.230988+00:00. The 180-second cap was respected. Only the closed N15 case and frozen criteria were inspected. This is not blinded: the report and relay labels reveal the direct-task baseline.

K1, K3, K4 and K8 are **MET at the requested observation scope**. No material criterion failure is established. The baseline needs no Qore finder/verifier roles, gates or repair loop.

| Criterion | Assessment | Evidence and implication |
|---|---|---|
| K1 | MET | Original contract distinguishes Close → summary from Back → introduction H1. N15 reports both accurately. Observation 2 actions 21–27 and `04-after-keyboard-close.dom.json` establish Close/Enter and SUMMARY focus; actions 29–34 and `05-returned-introduction.dom.json` establish Back/Enter and H1 focus. |
| K3 | MET | Observation 2 actions 4 and 28 passed none-checked assertions. Five viewed captures show empty answer circles where present; Next remains disabled in the DOM. Activation checks 8–19 identify actual summary/Close Enter/Space activations. Live policy and harness enforce approved native controls and state, reject mutation methods and unauthorized document/link navigation. Both event logs show successful same-origin GETs only and one blocked analytics POST each. |
| K4 | MET | Raw action outcomes, active-element DOM and viewed PNGs support the conclusion. Report explicitly limits full-page visual completeness and broader certification/deployment claims, and correctly separates the anticipated blocked POST and historical protocol proof gap from a website defect. |
| K8 | MET | Observation 2 contains the complete requested public-entry help sequence: Enter opens, Space closes, Enter reopens, Tab reaches Close and Enter closes it with summary focus restored. The report limits its pass to the recorded desktop session. Extra Back coverage is supported; whole-website inspection and causal improvement are not required. |

The task is complete at U2 scope. Two fresh operator sessions executed the submitted 6- and 33-action arrays verbatim, each with the automatic Tab probe and COMPLETE result. The meaningful focus traversal is also recorded beyond that generic probe: two Tabs reached summary, one reached Close, and one subsequently reached Back. Raw observation 2 events at 12:05:27.315, 12:05:31.203, 12:05:34.264 and 12:05:39.116 UTC record Enter/Space/Enter/Enter, and active element SUMMARY is captured after Close. No answer activation is recorded.

I actually viewed `observation-2/raw/01-help-open-enter.png`, `02-help-closed-space.png`, `03-help-reopened-enter.png`, `04-after-keyboard-close.png` and `05-returned-introduction.png`. Open/reopened captures show help text and Close; collapsed captures show the focused summary; the returned introduction is visibly present and its DOM identifies H1 focus. These PNGs are full-page images (`operator/browser_probe.mjs:244`), not viewport-only captures. The viewport was 1280×800, but image document coordinates do not identify the actual scroll framing at every keypress.

Two material interpretation candidates are retained separately from criterion completion:

1. **Conditional product concern:** the cookie banner crosses help text in the open/reopened full-page PNGs. Actual viewport obstruction is UNKNOWN. Counterexample to treating this as an established journey failure: raw events show keyboard Close succeeds, and full-page capture can combine fixed elements with document-wide content. N15 already discloses the visual limitation; no criterion failure follows.
2. **Rejected defect interpretation:** the console error at `/api/labs/readiness/event` is the rejected POST (`events.json#/blocked_mutations/0` and `#/console/0`). Counterexample to a website-failure claim: the source contract explicitly anticipates this block, page-errors are empty, and the requested help sequence completes.

Method coverage and product quality remain distinct. This is a direct-task baseline with adequate observation evidence, not proof of broader UX quality, repeatability, accessibility, performance or any benefit caused by a workflow. Origin enforcement is specifically approved-link and main-frame/popup navigation enforcement; the harness is not a universal off-origin subresource sandbox. Every observed successful request was nevertheless same-origin. No deployment revision is identified, so deployment comparability remains UNKNOWN beyond the recorded URL and session times. No comparison, score or winner is assigned.

No live/browser/model rerun, fixes, installs, external retrieval, other cases, other evaluators/verifiers, private source or additional agents were used. Videos, traces, request-1 PNGs and unlisted DOM/PNG files were not inspected. Full criterion evidence pointers and the actual inspection inventory are saved alongside this report.
