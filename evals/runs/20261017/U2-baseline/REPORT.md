# Navigable copy of the original trial report

The [original report](final-output/REPORT.md) is preserved byte-for-byte with the original method record. This copy adjusts only links for this public layout. It does not revise findings, coverage or observations. Later independent qualification is recorded separately in `evaluation.json`.

# Observed help journey

The declared help journey passed in the observed desktop browser session: help opened with Enter, closed with Space, reopened with Enter, and closed through the keyboard-operated Close button. Close restored focus to the help summary. Tab then reached Back; Enter returned to the introduction and focused its H1. No failure of the eight required checks was observed. This conclusion applies to the recorded session, not to the entire application.

The task used the original `TASK.md`, `surface-contract.json`, `checks/check_contract.py`, and `observation-policy.json`. The contract selected the observations and acceptance criteria. No tutorial protocol or Qore skill was supplied or invoked. The baseline required no independent finder/verifier roles; only the primary context `/root` performed this task. No subagents ran, so no child roster or Qore execution contract is applicable.

## Actual execution and evidence

Two fresh, isolated operator-mediated Playwright Chromium sessions started at the declared public entry, `https://qaizen.io/labs`. Each included the automatic Tab capability probe. Request 1 established the entry, introduction and first question; request 2 replayed entry and exercised the complete keyboard journey. Arrays were executed verbatim, with no operator interpretation or repair. Both receipts report exit code 0, `fresh_context: true`, and `input_actions_modified: false`.

| Request | Submitted actions | Relay start UTC | Relay return UTC | Result |
| --- | ---: | --- | --- | --- |
| [1](final-output/browser-request-1.json) | 6 | 2026-10-17 12:04:33.305885 | 2026-10-17 12:04:48.433643 | COMPLETE |
| [2](final-output/browser-request-2.json) | 33 | 2026-10-17 12:05:14.086654 | 2026-10-17 12:06:02.191746 | COMPLETE |

Request files were written at 12:04:31.496722 UTC and 12:05:12.761629 UTC respectively. These are browser dispatches, not independent agent roles. Full returned reports and evidence are saved in [response-1](final-output/response-1/relay.json) and [response-2](final-output/response-2/relay.json), including `result.json`, complete `events.json`, DOM captures and PNG captures. Requested browser roster: 1 and 2; returned: 1 and 2; missing: none. Four of the six available requests were unused because the required sequence completed.

Browser: Playwright 1.62.1, Chromium 151.0.7922.34, Node v22.23.3. Captured viewport: 1280 × 800, device pixel ratio 1; document language `en`, with English content. The contract declares en-US; regional locale was not independently measured.

## Acceptance results

All action times below are UTC on 2026-10-17. The authoritative action and activation records are [request 2 events](final-output/response-2/events.json). Timestamps on action entries mark their recorded initiation; completion is recorded by the outcome field.

| Required check | Observed result and evidence |
| --- | --- |
| entry | Public entry responded with HTTP 200. Clicking the declared readiness-check link reached `/labs/readiness-check`; Start reached question 1. [Request 1 events](final-output/response-1/events.json), [introduction DOM](final-output/response-1/02-introduction.dom.json), [question DOM](final-output/response-1/03-first-question.dom.json). |
| unanswered | `assert-none-checked` completed before help at 12:05:22.753 and after Close at 12:05:43.068. No answer activation was requested or recorded. Tab passed through the first answer without activating it. Next remained disabled in question captures. |
| help-toggle | Tab reached the summary in two steps. Enter at 12:05:27.315 opened help; the `open` attribute assertion and visible Close assertion passed. Space at 12:05:31.203 hid Close and removed help text from visible DOM text. Enter at 12:05:34.264 reopened it. [Open DOM](final-output/response-2/01-help-open-enter.dom.json), [closed DOM](final-output/response-2/02-help-closed-space.dom.json), [reopened DOM](final-output/response-2/03-help-reopened-enter.dom.json). |
| close-focus | One Tab reached Close, then its focus assertion passed. Enter at 12:05:39.116 closed help. Close became hidden and the summary focus assertion passed. [After Close DOM](final-output/response-2/04-after-keyboard-close.dom.json) identifies active element `SUMMARY`, “What does this mean?”. |
| keyboard-back | From the refocused summary, one actual Tab reached Back at 12:05:43.994. Focus assertion passed; Enter at 12:05:45.811 activated Back. Guard records identify the actual Back button and allow its activation in the closed-help state. This proves the requested transition, beyond the initial generic Tab probe. |
| introduction-focus | After Back, Start was visible, the radiogroup was hidden, and URL remained `/labs/readiness-check`. The H1 focus assertion passed at 12:05:47.910. [Returned introduction DOM](final-output/response-2/05-returned-introduction.dom.json) identifies active element `H1`, “Could your AI pilot go live? A check in about 3 minutes”. |
| read-only-policy | Both sessions enforced GET/HEAD/OPTIONS. All recorded successful network events were GET. Each session blocked one analytics POST to `/api/labs/readiness/event`. Neither session recorded a page error, route error or blocked activation. [Evidence audit](final-output/evidence-audit.json). |
| origin-policy | Every recorded network and navigation origin was `https://qaizen.io`. No blocked navigation or route errors were recorded. This establishes observed traffic under the relay policy, not a general security guarantee. |

## Visual observations and diagnostic interpretation

I actually inspected the first-question PNG and the request 2 open-help, Space-closed, keyboard-Close and returned-introduction PNGs. Expanded help showed a definition, answer examples, “Who to ask”, “Why it matters”, and Close. Closed captures showed the collapsed summary with a visible focus outline; the returned capture showed the introduction and Start. DOM and focus assertions, rather than pixels alone, establish focus destinations. A persistent analytics-cookie banner overlapped portions of the full-page captures; this limits visual completeness and was not investigated as a separate defect. Cookie controls were not activated.

**Informational / expected policy effect:** each run recorded one blocked analytics POST, one failed-request event and one corresponding `net::ERR_BLOCKED_BY_CLIENT.Inspector` console error. The supplied contract explicitly anticipated a blocked analytics POST. The help and return sequence still completed in that condition. Therefore the console error does not establish a help defect or an uncaught application exception; both `page_errors` arrays were empty. Conversely, this execution does not establish analytics delivery or behavior with analytics enabled. No other defect severity is assigned because no defect was established.

The contract's historical keyboard proof-gap note is provenance, not evidence of a current website failure. The observed Tab-to-Back, Enter activation and H1 focus directly satisfy the current acceptance obligation. The contract validator's success likewise establishes structural consistency only, not browser correctness.

## Checks, integrity and limits

`python3 -B checks/check_contract.py surface-contract.json` exited 0; its full output is [contract-check.json](final-output/contract-check.json). [evidence-audit.json](final-output/evidence-audit.json) records matching request hashes, no mismatches against either relay's evidence-file hashes, completed/observed action outcomes, actual focus steps and keyboard activation targets. [input-hashes.json](final-output/input-hashes.json) and the post-observation audit confirm all four input files remained unchanged. All output writes were outside the input directory. No shared-data mutation was executed; the relay blocked the application's attempted analytics mutations. No command networking, search, fetch, connectors or external sources were used.

The primary context began with its first recorded UTC clock reading at 12:04:14. Wall budget: 900 seconds; aggregate agent budget: 2400 seconds. No child contexts or missing child reports exist. Precise aggregate model actor-seconds and token usage are unavailable because the available tools expose no such usage meter; no zero usage is inferred. [run-record.json](final-output/run-record.json) retains operational identity and timing. No budget exhaustion or quality retry occurred.

Missing coverage: no mobile or other browser testing; no complete questionnaire, answers, results or submissions; no screen-reader, accessibility or performance certification; no accepted-cookie or unblocked-analytics run; no reload/history persistence checks. The full keyboard journey was observed once, with a separate entry observation, so broad repeatability is not established. The supplied target digest identifies the enclosing frozen manifest, not a single file or deployed website revision; private commits cannot identify the deployment observed here. No production source change is supported by these observations.
