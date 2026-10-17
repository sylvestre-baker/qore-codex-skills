# Protocol review

The supplied procedure has **three Medium-severity verification gaps**. It cannot establish all acceptance obligations in `surface-contract.json`. These findings concern the procedure, not defects in the deployed website. No website requests, browser interactions, answers, submissions, or shared-data mutations were performed.

Authority: `TASK.md` directs review against `surface-contract.json`, `checks/check_contract.py`, and `observation-policy.json`. All three were read in full, along with the target. The tutorial's reference to QORE-003 does not invoke a Qore skill or create project authority.

1. **Medium — Clicking Back leaves required keyboard behavior unverified.**

   Evidence: `target/verification-protocol.md:10` says “Click Back” and then checks visibility and introduction-heading focus. `surface-contract.json:15` requires reaching Back using Tab, activating it with Enter, and moving focus to the introduction heading. The required checks include `keyboard-back` (`surface-contract.json:18`). `checks/check_contract.py:35–36` explicitly requires sequential keyboard traversal and observed Enter activation; its validator permits Tab or Shift+Tab, while this particular contract specifies Tab.

   Impact: A run could satisfy every listed assertion even when Back is unreachable by keyboard or Enter fails to activate it. A mouse click followed by a correct focus destination establishes neither prerequisite. This is a gap in proof, not evidence that Back currently fails.

   Proposed correction: After Close returns focus to the summary, use Tab to reach Back, observe that Back is focused, press Enter, and retain the existing visibility and introduction-heading-focus assertions. Record the actual traversal and activation outcome. Do not replace sequential traversal with direct scripted focus.

   Counterpoint considered: The final heading-focus assertion is useful and matches the contract. It does not establish how Back was reached or activated, so it does not refute the finding.

2. **Medium — Required help keyboard transitions are missing or underspecified.**

   Evidence: `target/verification-protocol.md:7` only says to open help using its summary control. It does not specify Enter. The next instruction immediately reaches Close (`:8`), omitting the summary's Space-to-close and Enter-to-reopen transitions. Those three activations are explicit in `surface-contract.json:11–13`, and `help-toggle` is a required check (`:18`). The contract also specifies Tab for reaching Close (`:14`), whereas the procedure allows Tab or Shift+Tab.

   Impact: The procedure could pass after a mouse-only opening even if Enter opening, Space toggling, or Enter reopening is broken. Correct Close behavior cannot establish summary-toggle behavior. Allowing either traversal direction also leaves the contract's specified forward Close traversal unproven when a runner chooses Shift+Tab.

   Proposed correction: Reach the summary and press Enter; observe help open. Press Space on the summary and observe help closed. Press Enter and observe help open again. Then reach Close using Tab, press Enter, and retain both existing assertions: help is closed and the summary is focused.

   Counterpoint considered: “Using its summary control” identifies the correct control, and the Close step already includes keyboard activation and focus verification. Neither supplies the missing summary activations or intermediate observations. The Python checker does not validate protocol text and cannot fill this gap.

3. **Medium — Origin and read-only policy checks are absent.**

   Evidence: The entire procedure (`target/verification-protocol.md:5–10`) contains no origin or request-method guard, policy verification, or instruction to preserve blocked-request effects. `surface-contract.json:5–6` permits only `https://qaizen.io` and GET, HEAD, OPTIONS. `observation-policy.json:2–4` independently supplies that origin allowlist. `surface-contract.json:18` explicitly requires `read-only-policy` and `origin-policy`; `:20` expects an analytics POST to be blocked and its observed effects retained. `checks/check_contract.py:12–18` checks declared origin and read-only scope, not runtime requests.

   Impact: A literal execution of the procedure would not establish compliance with these required checks. Navigation or page scripts could attempt disallowed requests without the procedure detecting or blocking them. This review establishes missing instructions, not an actual unauthorized request or mutation.

   Proposed correction: Before navigation in any subsequently authorized browser run, enforce the supplied origin and method allowlists for requests and redirects. Record policy enforcement and blocked attempts, including any expected analytics POST and its observed effects. Do not permit the POST merely to make the page appear normal, and do not infer that it occurred without observation. Retain the unanswered requirement and prohibit form submission and result generation.

   Counterpoint considered: An external browser harness could enforce these policies. No such harness or recorded enforcement is supplied, and the procedure neither references one nor asks the runner to verify it. Starting at the public Labs entry and leaving the question unanswered do not alone establish request-policy compliance.

The Medium ratings reflect material acceptance-proof gaps with no demonstrated production defect or observed shared-data impact. No High or Critical impact is supported by the supplied evidence.

Coverage of the eight required checks:

| Required check | Supplied procedure coverage |
| --- | --- |
| entry | Steps 1–2 cover entry and start at a high level. |
| unanswered | Steps 2 and 5 explicitly preserve and assert it. |
| help-toggle | Incomplete: missing Space close and Enter reopen; opening activation unspecified. |
| close-focus | Step 4 checks help closure and summary focus; its traversal alternative is broader than the contract. |
| keyboard-back | Missing: step 6 explicitly clicks. |
| introduction-focus | Step 6 explicitly checks the introduction heading's focus. |
| read-only-policy | No enforcement or verification instruction. |
| origin-policy | No enforcement or verification instruction. |

The protocol correctly keeps Close's summary-focus assertion separate from Back's introduction-heading-focus assertion. No conflation of those destinations was found. Its fixture disclaimer (`target/verification-protocol.md:3`) also correctly avoids claiming an authentic historical record or a website defect.

For reproducibility, a revised procedure should explicitly use the contract's en-US locale, 1280×800 viewport, entry URL and journey selector (`surface-contract.json:4–9`). These are additional underspecified settings, not a separate finding with demonstrated behavioral impact. Restrict any eventual conclusions to the supplied entry/state journey; the contract excludes full questionnaire, mobile, performance, and accessibility certification (`:20`).

Validation actually executed: `python3 -B checks/check_contract.py surface-contract.json` from `/workspace/worker`, exit code 0, returned `valid: true`. Its full stdout and command record are saved in `contract-check.json`. The returned limit is “Contract consistency only; browser observations establish current behavior.” This result checks the JSON contract, not the tutorial protocol or website.

Execution and limits: This was one baseline review by the actual primary context `/root`, with no children or independent verifier. No method requiring independent phases was invoked; no Qore phases, Qore execution contract, profile consumption, or skill structural validator was invented. All five supplied files are accounted for in `input-hashes.json`; line-numbered evidence is retained in `source-evidence.txt`. The supplied enclosing manifest digest is recorded as metadata and was not independently reconstructed. `run-record.json` records identity, timestamps, commands, and unavailable usage. Inputs were not edited.

Actual outcome: three supported procedure findings, plus the bounded reproducibility observation above. Current deployment behavior, actual blocked-request effects, and runtime policy enforcement remain unobserved. There was no independent verification of this review's reasoning. No additional task resources or live observations were available or used.
