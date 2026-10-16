# Independent feasibility finder — PARTIAL review coverage

Requested and returned role: independent performance/feasibility finder only. No agents spawned, peer reports read, mechanical redaction, verifier, or final findings gate performed. These are two medium-severity candidates, not independently verified findings or delivery blockers. The lead owns remaining phases.

## Discovery and binding

The initial available-skills catalog actually exposed these Qore entries: `qore-plan`, `qore-plan-qaizen-labs`, `qore-review`, `qore-review-qaizen-labs`, `qore-ux-review`, `qore-ux-review-qaizen-labs`. Loaded `/workspace/project/examples/qaizen-labs/.agents/skills/qore-review-qaizen-labs/SKILL.md`, its bundled project profile, project-profile instructions, protocol, findings contract and execution-evidence instructions. This catalog statement comes from the initial tool/skill catalog, not inferred discovery from the user-supplied skill text.

Before consuming project facts, ran the bundled `python3 …/scripts/project-check.py …/references/project.json --root /workspace/project/examples/qaizen-labs --method review`. Exit 0; complete JSON in commands.json. Its coverage COMPLETE refers only to profile freshness. Profile qaizen-labs 0.1.0 SHA-256 `f76afdd45cb6352e5044a06affc4182ea6cd40aa9c012fb216636a61faa428f0`; both source digests matched. Checker source `9ef2a0acf51f078ce290ec723ca550b8b73597e68304179fe4d0625c5757963b`; surface source `3728739a119a53272541f83d451e40addb6939304f9d9ec060a477a87170a4a3`.

Consumed `surface-contract` by inspecting checks/check_contract.py and then executing its exact declared command. Consumed `close-focus`, `back-focus`, `unanswered-scope` to inspect separate Close/Back assertions, sequential keyboard traversal and intermediate unanswered checks plus observation guards. They shape source review only; unavailable rendered checks remain uncovered. No web surfaces were returned for method review. See profile-use.json for fact/source/effect mapping.

## F-FEAS-01 — medium — Failed review cannot accept corrected delivery

Evidence: tools/coordination.py:79 permits deliveries only from IN_PROGRESS/awaiting=delivery; :92-93 puts FAIL in CHANGES_REQUIRED/awaiting=None. The request operation at :106-107 requires REVIEW_REQUIRED. docs/coordination.md:71 directs production to prepare a corrected artifact as a new delivery/request after failed review, reserving new criteria revisions for changed criteria/reopening DONE.

Trigger: unchanged criteria, first delivery independently fails, production supplies corrected artifact a2. Saved reproduction executes initialize → production_ack → delivery → request_review → FAIL → corrected delivery. Actual output: state CHANGES_REQUIRED both before and after correction; final decision REJECT, reason `not awaiting delivery`. The CLI exposes no restart/correction transition. The documented loop therefore stalls unless an operator edits private state manually or performs a new revision/assignment beyond the prescribed unchanged-criteria flow.

Concrete reproduction: `python3 -B /workspace/qualification/finders/feasibility/reproduce.py`, first case. A supported guarded resubmission transition should clear the old request/verdict, accept the new delivery, and retain stale identity rejection. Independent verifier disposition remains pending.

## F-FEAS-02 — medium — ACK batch exceeds receive window

Evidence: docs/coordination.md:13 promises at most 120 seconds. tools/agent_mail.py:58-59 sets a per-call timeout before fetch, but :84-89 performs all ACKs without recalculating remaining budget; its RECEIVED return precedes the deadline check at :103.

Trigger: multiple ACK-required messages and slow successful acknowledgements. Deterministic local simulation of the actual receive function uses a Client subclass and patched monotonic clock, with a 1-second fetch and six 25-second ACKs. No HTTP or real waiting occurs. For seconds=120 the function returns RECEIVED at simulated t=151; every call retains a 30-second timeout and the last ACK starts at t=126. This measures scheduling behavior under explicit latency inputs, not actual Agent Mail performance. A 999-message permitted batch could schedule 29,970 seconds of 30-second calls before deadline handling; that is conditional arithmetic, not an observed service run.

Consequence: a bounded operator receive turn can continue well after the promised window. Already processed entries with ack_required still set are acknowledged again on replay, so the issue is not limited to new deliveries. Recompute the remaining budget before every ACK and return at deadline with durable state and replayable pending ACKs.

Concrete reproduction: same command, second case; complete call timeline in reproduction.json.txt. Real transport behavior and independent verification remain unresolved.

## Checks and boundary tracing

commands.json preserves exact argv, cwd, exit code, stdout and stderr for preflight, declared checker and all five test runs. `python3 -B checks/check_contract.py surface-contract.json` from the example root: exit 0, valid=true, explicitly contract consistency only.

From repository root, `python3 -B -m unittest discover -s tests -p NAME`: test_coordination.py 7 passed; test_agent_mail.py 4 passed; test_task_gate.py 18 passed; test_labs_contract.py 3 passed. test_browser_probe.py collected 11 and skipped all 11 because the optional driver is absent: no browser pass. `node --check tools/browser_probe.mjs`: exit 0. Runtime: Python 3.14.8 and Node v22.23.2. These checks do not establish support for older runtimes. `rg` is unavailable (exit 127); used find/grep and direct reads instead. The initial brace-expansion wc command failed under sh and supplied no evidence.

Central identity trace: criteria producer initialize hashes sorted compact UTF-8 JSON plus final LF; Markdown save_register serializes it in one qore-task fence. Agent Mail body_md JSON becomes a normalized body with transport envelope id; consume supplies delivery_message_id from that envelope. Delivery identity fields are task_id, task_revision, criteria_sha256, artifact_revision, artifact_sha256, delivery_message_id; review adds review_request_id plus session/run/freshness fields. Completion evaluate compares those identities and actual artifact/manifest/proof bytes, proof check_id/result against the criteria inventory, then emits DONE and accepted_identity. No field transmission mismatch was established in this trace; F-FEAS-01 concerns the state transition around a new artifact, not invented service behavior.

The contract/actions/policy remain a desktop English unanswered entry/state scope. Source inspection supports separate focus checks and finite observation assertions; it cannot establish current browser behavior. Optional browser and Agent Mail prerequisites are documented rather than assumed installed. The 1,000-entry refusal is a stated small-project bound, not a missing unbounded-service feature. Same-origin HTTP redirect refusal is expressly declared and is not treated as a new defect. The dependency document retains its partial persistent-service disposition; advisory/binary claims were not independently researched in this feasibility pass. Public planning/UX assertions were treated as candidate source, not independent proof.

## Snapshot, limits and unfinished work

Working tree artifact review, not a Git-base diff: `git -C /workspace/project rev-parse HEAD` failed because there is no HEAD commit; git status showed untracked candidate files. snapshot.json records SHA-256 for 18 scoped target files (spec/contract/checker/actions/policy, harness/helpers, tests/fixture and coordination docs); its exact-byte manifest digest is `5ceb645436a510909424e7e7adbe0608d43c6c9dab15fad91556957ad65b85e2`. skill-snapshot.json identifies installed derivative files; exact-byte manifest digest `bbe9e705eaf09beb556b0d5298d74778db2a2ba01e205c1e24389f707ac2ae0a`. No repository source was modified. Local reproduction and receipts are outside the repository. No AGENTS.md was found under the repository.

No live website, browser, service, auth file, home profile, private source, sibling report, old unrelated evidence or author chat was accessed. Synthetic transport scheduling is not a wire receipt or browser qualification. Remaining work: independent verifier examination of F-FEAS-01 and F-FEAS-02, actual browser positive/negative controls and live authorized journey, real slow-ACK/recovery qualification, older-runtime compatibility and exhaustive failure-path testing. These remain named gaps, not implied passes.

Totals: 2 candidates (medium); 0 independently confirmed, 0 independently refuted. Both candidate IDs await the lead's redaction and fresh verifier. Finder scope has useful executed evidence; overall review coverage is PARTIAL, with no final COMPLETE or product readiness claim.
