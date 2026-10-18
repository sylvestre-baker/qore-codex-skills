# Journey verification procedure — proposed replacement

Reconstructed tutorial fixture, newly authored for QORE-003; not an authentic historical protocol or evidence of a website defect. This procedure defines acceptance obligations from `surface-contract.json`, `checks/check_contract.py` and `observation-policy.json`. It is not a report of a successful website run.

## Setup and observation boundary

Use en-US and a 1280×800 viewport. Observe only the entry and declared states. Do not select answers, generate results, submit forms or redistribute website source.

Before navigation, install and verify request guards. Permit only GET, HEAD and OPTIONS and only the parsed exact origin `https://qaizen.io`, as authorized by both the contract and observation policy. Apply these restrictions to navigation, redirects and subordinate requests. Ensure uninspectable request paths cannot bypass the guards; if enforcement is unavailable, stop and mark policy checks blocked. Do not send probes to prohibited destinations to test the guard; test its decisions offline.

Log attempted/blocked requests and their observed effects. An analytics POST is expected to be blocked if attempted. Do not unblock it to make the journey work or silently discard effects of blocking. Record any resulting behavior limitation. GET/HEAD/OPTIONS permission does not authorize excluded user actions.

Prepare a trace containing UTC timestamps, step/transition ID, control identity, traversal and activation, expected/observed state, actual focus where required, answer state, evidence references, and pass/fail/not-run/blocked status. Record browser version, URL and any available public deployment identifier without inferring deployment from private source commits. Set and record bounded waits and a finite Tab traversal limit before the run.

## Journey

1. **entry:** Open `https://qaizen.io/labs`. Click `a[href$='/labs/readiness-check']` and observe the introduction on the authorized origin. Record URL, control and state evidence.
2. **start / unanswered:** Click “Start the check” and observe the first question. Inspect selection state without selecting an answer. Keep it unanswered throughout the remaining steps.
3. **open-help:** Reach the relevant `summary` control without selecting an answer; using Tab is a procedural choice here. Press Enter and observe help open.
4. **toggle-help:** With the summary focused, press Space and observe help closed. Record this separately from the later Close action.
5. **reopen-help:** With the summary focused, press Enter and observe help open again.
6. **close-help / close-focus:** Use Tab to reach Close. Record that Close is the active element, press Enter, and observe help closed and the summary focused. Capture actual focus before moving it again. Inspect and record that the question remains unanswered.
7. **back / keyboard-back:** Starting from the summary after Close, traverse sequentially with Tab until the intended Back control is focused. Record the traversal and active Back control before pressing Enter. Do not substitute a mouse click, direct focus call or handler invocation. Press Enter and observe the returned introduction.
8. **introduction-focus:** After the Back transition settles, and before any further input or focus adjustment, assert that the introduction is visible and its heading (`h1`) is the actual active element. Separately record whether the question and help are absent from the visible journey, preserving the prior protocol's assertions. Distinguish visibility from DOM removal in the evidence; the contract does not mandate removal.

If a prerequisite transition fails, preserve the failure and mark dependent observations not run or blocked. Never force a desired focus or state and report it as the application's outcome.

## Completion and limits

Report a result and evidence reference for each required check: `entry`, `unanswered`, `help-toggle`, `close-focus`, `keyboard-back`, `introduction-focus`, `read-only-policy`, and `origin-policy`. Keep Close → summary focus distinct from Back → introduction-heading focus. Preserve unexpected states, request blocks and refutations; do not turn missing evidence into a pass.

Run `python3 -B checks/check_contract.py surface-contract.json` locally. Its success establishes contract consistency only, not protocol correctness or current browser behavior. Inspect all seven transitions and the separate observation policy explicitly when reviewing this procedure.

Public provenance URLs are `https://qaizen.io/labs` and `https://qaizen.io/labs/readiness-check`. The supplied baseline observation date is 2026-10-15. The keyboard proof gap was found in the protocol on 2026-10-16, not on the website. Record a new observation timestamp if this procedure is later executed and separate expectations from observed results.

This procedure covers no mobile journey, complete questionnaire, performance claim or accessibility certification. Private source commits do not identify the current deployment. Effects of blocked analytics restrict what can be inferred about behavior without those blocks.
