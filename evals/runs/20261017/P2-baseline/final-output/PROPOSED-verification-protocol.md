# Journey verification procedure

Reconstructed tutorial fixture. Newly authored for QORE-003; not an authentic historical protocol or evidence of a website defect.

This procedure verifies the declared acceptance obligations in `surface-contract.json`. Read it with `observation-policy.json` and `checks/check_contract.py`. Expected transitions and focus destinations are requirements, not evidence that the current deployment satisfies them. The recorded keyboard proof gap concerns the protocol, not a demonstrated website defect.

## Scope and setup

Use locale `en-US` and a 1280 × 800 viewport. Cover only the declared entry and states, leaving the first question unanswered. Do not select answers, generate results, submit forms, or redistribute website source. This procedure makes no claim about mobile behavior, the complete questionnaire, performance, or accessibility certification.

For a separately authorized public observation, restrict requests to origin `https://qaizen.io` and methods `GET`, `HEAD`, and `OPTIONS` before opening the entry. Apply the origin restriction to navigation, redirects, and other requests. Block all other origins and methods. An analytics POST is expected to be blocked: record its occurrence and any observed effects on the journey, without allowing or replaying it. Record any policy violation or resulting coverage limit; a blocked attempt is not itself proof that an application transition failed.

Run `python3 -B checks/check_contract.py surface-contract.json` locally. A successful result establishes contract consistency only. It neither checks this document's completeness nor proves current browser behavior. Do not perform public observation when the execution environment prohibits network access.

## Journey and assertions

Use actual keyboard input for the specified keyboard transitions. Before activating a keyboard control, establish that it has focus. For Close and Back, record the sequential traversal and focus reached before Enter, then the observed state and focus afterward. Directly assigning focus to Close or Back does not demonstrate sequential reachability.

Use Tab for the main run, matching the supplied contract's traversal for Close and Back. Retain Shift+Tab as optional additional protocol coverage and label it separately; it does not substitute for the declared Tab trace. Preserve the existing 24-step bound for reaching Back as a local protocol guard, not a contract-wide maximum or website requirement. If Back is not reached within that bound, record the incomplete bounded attempt and do not claim the transition passed.

1. **Entry (`entry`):** Open `https://qaizen.io/labs` and click the journey link matching `a[href$='/labs/readiness-check']`. Assert the introduction is visible. Observe and record the resulting URL subject to the origin policy.
2. **Start (`start`):** Click **Start the check**. Assert the first question is visible and unanswered. Do not select an answer at any later step.
3. **Open help (`open-help`):** Focus the question's `summary` control, press Enter, and assert help is open. Record how focus was reached; the contract does not prescribe traversal for this initial step.
4. **Toggle help (`toggle-help`):** With the summary focused, press Space and assert help is closed. Do not substitute the Close control for this summary toggle.
5. **Reopen help (`reopen-help`):** With the summary focused, press Enter and assert help is open again.
6. **Close (`close-help`):** From the open-help state, reach **Close** with Tab and activate it with Enter. Assert help is closed and the actual focused element is the summary (`summary`).
7. **Unanswered (`unanswered`):** Assert the first question remains unanswered after the help sequence.
8. **Back (`back`):** Assert the question remains unanswered immediately before leaving it. From the closed-help state, reach **Back** with Tab within 24 traversal steps and activate it with Enter. Assert the introduction is visible, the question and help are absent, and the actual focused element is the introduction heading (`h1`). Treat the absence checks as retained assertions from this protocol. The required Back focus destination is distinct from Close's summary destination.

## Evidence and reporting

Record observation date/time, entry and resulting URLs, locale, viewport, request restrictions, each actual control/input, relevant pre/post state, focus observations, and any blocked requests and observed effects. Keep expected and observed results separate. Record each required check as passed, failed, or not observed, with supporting evidence or the reason coverage is missing:

| Required check | Evidence location in this procedure |
| --- | --- |
| `entry` | Step 1: link, click, and introduction |
| `unanswered` | Steps 2, 7, and immediately before Back in step 8 |
| `help-toggle` | Steps 3–5: summary Enter, Space, Enter and resulting states |
| `close-focus` | Step 6: sequential traversal, Enter, closed help, summary focus |
| `keyboard-back` | Step 8: sequential traversal within the local guard, Enter, returned introduction |
| `introduction-focus` | Step 8: actual heading focus after Back |
| `read-only-policy` | Request restrictions and observation log; no answers or submission |
| `origin-policy` | Authorized origin restriction and observed request/navigation log |

Retain the contract's public provenance and its distinction between observation and declared acceptance. Its baseline observation date is 2026-10-15; its note dates the protocol keyboard proof gap to 2026-10-16. Neither date proves a current deployment pass. Private source commits do not identify the current deployment. A failed or unobserved obligation must remain visible in the report rather than being replaced by an expected result.
