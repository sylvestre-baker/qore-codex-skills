# Navigable copy of the original trial report

The [original report](final-output/REPORT.md) is preserved byte-for-byte with the original method record. This copy adjusts only links for this public layout. It does not revise findings, coverage or observations. Later independent qualification is recorded separately in `evaluation.json`.

# Recorded UX review

**DO-NOT-SHIP.** Help and keyboard Back work, but the cookie banner obscures the focused Back button in the observed first-visit state. UX loop coverage is **PARTIAL** under the actual stop-rule; scoped observation coverage is **COMPLETE**. No inputs or shared data were changed.

## Finding and evidence

**F1 — medium severity: focused Back is obscured.** At 1280×800 with the cookie banner present, Tab after closing help focuses Back, but the banner covers its label and nearly all its gold focus outline. Inspect [the focused screenshot](final-output/evidence/response-5/07-back-focused.png) and [DOM](final-output/evidence/response-5/07-back-focused.dom.json), captured at 12:00:05.317Z. Keyboard users can lose track of their current control. Exact overlap geometry and formal standards conformance were not measured.

The stronger claim that Back is unreachable or focus restoration is broken is **refuted**: [actual events](final-output/evidence/response-5/events.json) show sequential Tab reaching Back, Enter returning to the introduction, and h1 focus passing. Close separately restores focus to the help summary. The [Close-focused screenshot](final-output/evidence/response-5/05-close-focused.png) shows its focus outline clearly. Full-page captures show sticky elements at their captured scroll positions; this limits geometric interpretation, but does not erase the observed Back obscuration.

Propose reserving space for the consent banner or scrolling focused controls above it. No fix was executed. After an authorized correction, repeat the full entry/help/Close/Back journey and renew every required gate.

## Observed journey

The real Labs anchor opened the intended readiness-check introduction. Start reached the unanswered first question. Summary Enter opened help, Space closed it, and Enter reopened it. Tab/Enter on Close closed help and restored summary focus. Tab/Enter on Back restored the introduction and focused h1. No answer was selected; Next remained disabled. [Request 3](final-output/evidence/response-3/result.json) and its [events](final-output/evidence/response-3/events.json) retain every transition. URL alone was not treated as proof of these local states.

[Request 5](final-output/evidence/response-5/result.json) additionally observed direct document reload (GET 200), browser history Back to Labs and Forward to the introduction, closed Close-control invisibility, unanswered preservation and the focused-state challenge. All relevant state images cited in the phase reports were actually opened and inspected.

| Gate | Score | Conclusion |
|---|---:|---|
| G0 Entry | 4 | Real anchor reaches intended heading/content |
| G1 Rendering/navigation | 4 | Reload and history states resolve; no page exception |
| G2 State/data | 4 | Required transitions and unanswered assertions pass |
| G3 Visual | 3 | Focused Back obscured by cookie banner |
| G4 Content | 4 | Affected introduction/question/help copy coherent |
| G5 Accessibility | 3 | Activation/focus destinations pass; visual focus obscured |
| G6 Challenge | 4 | Fresh replay exposed F1 and corrected prior scores |

Scores use the supplied skill scale; 4 is a scoped pass, not certification. GP is excluded because performance is explicitly outside the project contract. [Gate evidence](final-output/evidence/gate-results.json) preserves severity, refutations and unexamined claims.

## Execution and limits

Used the supplied [qore-ux-review skill](final-output/evidence/source/.agents/skills/qore-ux-review/SKILL.md), original contract/checker/policy, and neutral relay only. Context: anonymous public visitor, en-US scope (page language en), actual default dark appearance, CSS viewport 1280×800/DPR1. Driver: Playwright 1.62.1, Chromium 151.0.7922.34, Node v22.23.3. Navigation, screenshots, DOM, keyboard, console and network capabilities were actually probed; [matrix](final-output/required-check-matrix.json) links them to checks. Profile is null.

Five fresh browser requests, four UX iterations, no child agents. UX does not require independent finder/planning/verifier roles. Complete root phase and iteration reports are in `evidence/*-report.md`; [roster](final-output/roster.json) records actual context names and operator dispatch/return timestamps. Aggregate agent-seconds telemetry is unavailable, not zero. First recorded clock: 11:53:34Z; final browser return: 12:00:19.824660Z, within 900 seconds. Requests contained 0/29/29/36/36 actions; larger event counts include automatic Tab/focus substeps.

Requests 2 and 4 stopped at exact-name/text locators. Their raw diagnostics and missing actions remain retained; they are observation failures, not site defects. Corrected replays completed the journey. The final [stop-rule output](final-output/evidence/stop-rule-4.json) is STOP_PLATEAU / DO-NOT-SHIP / PARTIAL, with COMPLETE observations and no missing/stale gates. Its no-improvement count includes earlier incomplete attempts. No fifth iteration or sixth request was dispatched.

The qore-run record separately reports COMPLETE **phase execution**, because all five required phases ran and saved reports. This structural metric does not override PARTIAL **loop completion** or the failed G3/G5 gates. No corrected-state evidence exists. The structural validator result is retained in [validation.json](final-output/validation.json); structural validity does not establish reasoning correctness.

Each complete journey attempted one analytics POST to `/api/labs/readiness/event`; policy blocked it and the matching resource console error was retained. No page exceptions or blocked external navigation were observed. The journey resolved despite that expected block. Completed network responses were same-origin GETs; no answer/submission or consent mutation was activated. Unrestricted analytics and redirect behavior are unqualified.

No mobile, other themes/browsers/accounts, results, full questionnaire, screen-reader/contrast certification or performance conclusions. Consent dismissal, manual scrolling alternatives and exact overlay geometry remain unexamined. Trace/video names occur in relay results but those files were not supplied. The enclosing target digest identifies the frozen prepared-input manifest, **not the deployed website**. Live source revision and the original enclosing digest serialization are unavailable; supplied identities and individual file hashes are retained. [Integrity checks](final-output/evidence/receipt-integrity.json) matched every receipt/request digest, and [input checks](final-output/evidence/input-immutability.json) found no changes.
