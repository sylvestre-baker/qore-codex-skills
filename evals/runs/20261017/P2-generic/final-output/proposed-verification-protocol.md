# Journey verification procedure

Reconstructed tutorial fixture. Newly authored for QORE-003; not an authentic historical protocol or evidence of a website defect.

## Scope and preparation

Use `surface-contract.json` (schema `qaizen-labs-surface/1`, version `0.1.0`), `observation-policy.json`, and `checks/check_contract.py` as the project sources. Expected transitions and focus destinations are acceptance obligations; they are not evidence that the current deployment passes them. The historical protocol-gap note does not establish a gap in this current procedure. Private source commits do not identify the current deployment.

Before any future observation, confirm the contract and policy agree and prepare `en-US`, a 1280×800 viewport, and entry/state-only coverage. Enforce the sole allowed origin, exactly `https://qaizen.io`, and only GET, HEAD, OPTIONS before navigation and throughout requests, subrequests and redirect destinations. Do not start if enforcement cannot be confirmed; do not broaden the policy to complete the journey. An analytics POST is expected to be blocked: keep it blocked and retain its observed effects, including any effect on loading, errors or navigation. No such effects are presumed here.

Keep the journey unanswered. Do not select answers, submit forms, generate results or redistribute website source. This procedure does not cover mobile, the complete questionnaire, performance or accessibility certification.

Run `python3 -B checks/check_contract.py surface-contract.json` locally and retain its result. A pass establishes contract consistency only; the checker does not inspect this Markdown, enforce browser policy or establish current website behavior. Resolve/report a failed consistency check before claiming verification.

## Journey

1. Open `https://qaizen.io/labs`. Click the journey link `a[href$='/labs/readiness-check']` and observe the introduction (`entry`).
2. Click **Start the check**. Observe the first question without selecting an answer (`start`).
3. Reach the help **summary** control without answering and activate it with **Enter**. Assert help is open (`open-help`).
4. With summary as the active control, press **Space**. Assert help is closed (`toggle-help`).
5. With summary as the active control, press **Enter**. Assert help is open again (`reopen-help`). If needed, reach summary through ordinary navigation; these toggles do not add an unspecified post-toggle focus requirement.
6. Reach **Close** by sequential keyboard traversal, activate with **Enter**, and assert help is closed and actual focus is on **summary** (`close-help`). Use **Tab**, the direction declared in the contract; **Shift+Tab** remains a permitted procedural alternative. Record the direction used. Do not substitute a click or forced focus for traversal or for the focus assertion.
7. Assert that the first question remains unanswered after Close.
8. Assert again that the question remains unanswered immediately before leaving it. From the observed summary focus restored by Close, reach **Back** with **Tab or Shift+Tab** within **24 traversal actions** and activate it with **Enter** (`back`). Tab is the declared/default direction; record the actual direction or sequence. Count initial summary focus as zero and each Tab/Shift+Tab action once, without resetting the count. If action 24 focuses Back, Enter may activate it; Enter is not a traversal action. If Back is not focused after action 24, stop before action 25, record the final focus/count and failed bounded proof, and leave unperformed activation/return checks not observed. Do not click Back or force focus to manufacture a pass. After actual Enter activation, assert the introduction is visible, the question and help are absent, and actual focus is on the introduction heading (`h1`).

One permitted sequential route suffices for the procedure; a second directional run is not required. A Shift+Tab or mixed-direction observation does not establish an unexercised literal forward-Tab trace. The 24-action Back guard is retained from this procedure; it is not a contract-level product maximum, a Close limit or an accessibility certification criterion.

## Record and interpret evidence

Record the observation time/environment and, for each obligation, expected and observed state, actual control/input, relevant focus, Back count and PASS, FAIL or NOT OBSERVED with its reason. A visible-state pass cannot substitute for a focus pass. Record blocked requests and their observed effects with only necessary sanitized metadata; omit credentials, cookies, sensitive query values and source payloads. This compact recording convention does not require a new tool or capture system.

PASS requires observation of the relevant condition; FAIL records an observed mismatch; NOT OBSERVED records missing or unperformed evidence. At bound exhaustion, the bounded procedural reachability proof fails; Back activation and return assertions not performed remain NOT OBSERVED. The count alone establishes no website defect or universal tab-order limit. If Close fails to restore actual summary focus, record that failure and do not reset focus to claim a complete prescribed Back trace.

A correctly blocked analytics POST alone does not require aborting otherwise observable checks. If blocking prevents an observation, retain the effect and mark that assertion NOT OBSERVED; record any directly observed mismatch separately. Stop on an actual policy breach, loss of the unanswered invariant or inability to establish a required predecessor state. Record the last supported result and unperformed checks without weakening expectations or bypassing guards. A procedure completion, a local checker pass and current deployment conformance are distinct claims; claim only the evidence actually obtained.
