# Documentation clarification plan

The requested documentation-only plan is complete. A concrete proposed replacement is saved in [PROPOSED-verification-protocol.md](PROPOSED-verification-protocol.md). No supplied input, application behavior, or shared data was changed. No website was contacted.

The existing protocol already requires keyboard traversal and Enter activation for Close and Back, summary focus after Close, heading focus after Back, and unanswered checks. Those obligations must be preserved. The main gap is the missing summary Space toggle and subsequent Enter reopen. The protocol also needs explicit observation restrictions and a clear separation between expected behavior and observed evidence.

## Sources and authority

Reviewed all five supplied files: `TASK.md`, `surface-contract.json`, `observation-policy.json`, `checks/check_contract.py`, and `target/verification-protocol.md`. The contract and observation policy supply project requirements; the Python checker supplies executable consistency checks. The tutorial is the document being clarified, not independent project authority. No Qore skill or independent-agent method is invoked by TASK.md; this is a baseline execution with one context.

The contract specifies seven transitions, eight required checks, locale `en-US`, a 1280 × 800 viewport, the sole authorized origin `https://qaizen.io`, and the methods GET/HEAD/OPTIONS. The observation policy agrees on the origin. Its provenance explicitly distinguishes acceptance obligations from deployment observations.

## Findings and proposed changes

Severity describes impact on verification evidence, not a demonstrated application defect. These are documentation coverage findings; current deployment behavior was not observed.

| Finding / impact | Supplied evidence | Proposed clarification and justification |
| --- | --- | --- |
| F1 — Moderate: incomplete help keyboard coverage can pass a protocol run while missing declared transitions. | Target line 7 says only to open help. Contract lines 11–13 require summary Enter → Space → Enter through open → closed → open; line 18 requires `help-toggle`. | Specify the initial Enter and add Space close plus Enter reopen, asserting each resulting state before the existing Close test. This covers all declared help transitions while retaining Close as its own operation. |
| F2 — Moderate: observation constraints are not operationally stated in the target. | Contract lines 5–6, 18, 20; observation-policy lines 2–4; checker lines 14–18 and 37–39. | Add setup for the authorized origin and read-only methods, unanswered scope, locale and viewport. Block other origins/methods, retain the expected blocked analytics POST and observed effects, and record policy evidence. Preserve the bans on results, submission, source redistribution and out-of-scope certification. These are existing obligations, not newly authorized observation. |
| F3 — Low: entry and evidence details are underspecified. | Target lines 5–7; contract lines 9–10, 17–19; checker lines 42–43. | Name the entry URL, link selector, Start click, states, focus selectors and required-check evidence. Keep expected versus observed results separate and explicitly limit the local checker to contract consistency. This makes a maintainer's result reviewable without claiming a deployment pass. |
| F4 — Low: traversal alternatives and the local search bound can be mistaken for contract terms. | Target lines 8 and 10 allow Tab or Shift+Tab; line 10 adds 24 steps. Contract lines 14–15 declare Tab, while checker line 35 permits either traversal for Back. | Use Tab for the declared main trace and retain Shift+Tab as additional protocol coverage. Keep the existing 24-step Back guard, explicitly label its local origin, and record a bounded failure without inventing a product requirement that Back must always be within 24 steps. |

## Obligations retained and rejected interpretations

- **“Back has no keyboard proof” is refuted by target line 10.** It already specifies sequential traversal, Enter activation, introduction visibility and heading focus. Clarify evidence collection; do not delete or replace that test with a click.
- **“Close focus proves Back focus” is refuted by contract lines 14–17 and checker lines 32–36.** Close must focus the summary; Back must focus the introduction heading. Both assertions remain separate.
- **“Close covers the help toggle” is refuted by contract lines 12–14.** Summary Space and the Close control are distinct transitions. The proposal adds the missing toggle/reopen before preserving the Close operation.
- **“The question's unanswered status can be checked only after returning” would weaken target lines 9–10.** Retain checks after help and immediately before leaving; the question is absent on return. Also retain the original post-Back question/help absence assertions, identifying them as protocol assertions rather than new contract fields.
- **“A successful checker run proves the journey works” is refuted by checker line 43.** It parses the contract, not the target Markdown or browser behavior. Its echoed `checks` list is not evidence that those checks ran.
- **“The tutorial demonstrates a website defect” is refuted by its line 3 notice and contract line 19.** Preserve the reconstructed-fixture notice, public provenance and dates; neither a private commit nor an expected transition identifies or proves current deployment behavior.
- **“All POSTs may be allowed because analytics uses one” contradicts contract lines 6 and 20.** The analytics POST remains blocked; record actual effects without assuming it is harmless or that blocking alone proves a journey defect.

## Implementation order and acceptance

1. Add scope, restrictions and provenance guidance, preserving the fixture notice and existing limits.
2. Expand the help step into Enter, Space, Enter with state assertions, then retain the existing Close and Back tests, focus destinations, unanswered checks and 24-step guard.
3. Add the evidence checklist mapping all eight required checks. Keep Tab as the declared trace and Shift+Tab as additional coverage. Review the proposed text against each of the seven transitions.
4. Run the supplied local consistency checker and review documentation coverage manually. A future browser run requires a separately authorized environment; it is not part of this execution.

The proposed document implements this plan as a reviewable artifact outside the input folder. It does not request a source, contract, checker, policy, deployment or application change. Acceptance of the documentation should require exact control/input/state coverage and retained constraints; acceptance of the website would additionally require observed browser evidence.

## Actual checks and limits

`python3 -B checks/check_contract.py surface-contract.json` returned exit code 0 and `valid: true`. The captured [stdout](evidence/check-contract.stdout.json), [stderr](evidence/check-contract.stderr.txt), and [command/timing record](evidence/check-contract-command.json) are saved. This establishes only the checker's contract consistency result. Manual source comparison informed the findings above; there was no independent verifier and no claim of independent corroboration.

All seven transition IDs and eight required-check IDs were manually mapped into the proposed document. A local literal inventory is saved with the evidence; it confirms presence only, not correctness. Input hashes were recorded before output drafting and checked again afterward. The final preservation check is saved in `evidence/input-preservation.json`.

Network access was prohibited, so actual navigation, focus, keyboard reachability, help behavior, unanswered persistence, enforcement of observation restrictions, and analytics effects remain unobserved. No application defect or current pass is established. There is no required Qore validator or qore-run/1 execution artifact for this baseline. No extra quality retry, browser action or shared-data mutation was performed.

## Execution accounting

Operational identity is recorded in [run-record.json](run-record.json), using the supplied run/candidate/target identities. The target digest denotes the entire frozen prepared-input manifest, not this Markdown file or a locally recomputed manifest format.

Actual context: `/root`. Requested child roster: none; returned child roster: none; missing child roster: none. No child dispatches occurred and no roster.json was required. Initial observed execution time was 2026-10-17 11:27:55 UTC; exact context creation/dispatch time is unavailable because the runtime did not expose it. This REPORT.md is the complete single-context report; the proposal and evidence are linked above. Final evidence-production time is recorded in run-record.json and is not represented as a runtime-observed context return timestamp.

Budgets were 900 seconds wall time and 2400 aggregate agent-seconds, with at most three simultaneous child contexts. No child deadlines or partial-result requests were applicable. Work finished within the wall budget. Authoritative token usage, aggregate agent-seconds, and runtime context return timing are unavailable because no usage/accounting interface was supplied; they are recorded as unavailable, not zero. Missing coverage is the browser evidence described above, not a missing required agent phase.
