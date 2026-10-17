# State-transition phase report

Actor/context /root. Primary complete observation: request 3, 2026-10-17T11:56:22.907Z–11:57:13.069Z. Challenge: request 5, 2026-10-17T11:59:29.408031+00:00–2026-10-17T12:00:19.824660+00:00 (relay window).

All seven contract transitions actually executed in request 3: entry anchor click, Start click, summary Enter open, summary Space close, summary Enter reopen, Tab to Close then Enter, Tab to Back then Enter. Focus destinations were separately asserted: summary after Close; h1 after Back. Summary traversal took two Tabs from the question h2; Close took one Tab from summary; Back took one Tab from restored summary. No direct programmatic focus replaced these steps. URLs remain /labs/readiness-check throughout local states, so state identity comes from rendered content/DOM, not URL alone.

Request 5 added reload document 200 and browser history Back/Forward with heading/content snapshots, then repeated open/Close/Back transitions, observed Close hidden when closed, and captured visible focus. Browser Back and the application's Back are different actions, both retained. Unanswered assertions passed before help and after Close/traversal; no radio answer, Next, result or submission control was activated. Next was disabled in first-question snapshots.

Help's visible definition, Strong/Partial/Weak/Missing examples, Who to ask and Why it matters sections were read from DOM and PNGs. No loader remained unresolved on the scoped path. Arbitrary data permutations and questionnaire completion would require prohibited answers and are outside this task. F1 concerns the visibility of focused Back with the cookie banner, while its transition and h1 focus destination succeed.
