# Independent correctness finder — PARTIAL method coverage

Role requested/returned: correctness only / correctness. This is an actual invocation of the installed project derivative, restricted by the user to one finder. No agents were spawned, sibling reports or author chat read, redaction performed, or verifier phase run. Candidate findings remain unverified (PLAUSIBLE for handoff); no independent confirmation or final COMPLETE is claimed.

The initial available-skills catalog exposed these Qore names: `qore-plan`, `qore-plan-qaizen-labs`, `qore-review`, `qore-review-qaizen-labs`, `qore-ux-review`, `qore-ux-review-qaizen-labs`. This catalog came from the session's initial skill list, not discovery inferred from the user prompt. Loaded entry: `/workspace/project/examples/qaizen-labs/.agents/skills/qore-review-qaizen-labs/SKILL.md`. Read its profile, project preflight instructions, protocol, findings contract and run-evidence instructions. The user's explicit finder-only assignment overrides the derivative's orchestration steps for this worker.

Scope is the named public example specification, contract/checker/actions/policy, four root tools, relevant tests and coordination documentation. Public planning statements were target claims, not independent quality evidence. No live site, services, auth files, home profiles, private sources or old unrelated evidence were accessed. No repository source was modified.

## C01 — medium — Failed or incomplete review has no supported recovery transition

Evidence: `tools/coordination.py:79` accepts a delivery only in IN_PROGRESS/awaiting=delivery. Lines 92–95 move FAIL to CHANGES_REQUIRED and PARTIAL/BLOCKED to BLOCKED, with awaiting=None. Line 107 accepts review requests only in REVIEW_REQUIRED/awaiting=None. `docs/coordination.md:71` tells the operator to prepare a corrected artifact as a new delivery/request after failed review; new task revisions are described for changed criteria and reopening DONE.

Trigger: a current review returns FAIL/PARTIAL/BLOCKED, followed by a corrected artifact under unchanged criteria. Consequence: no exposed command returns the task to delivery/review readiness. The corrected delivery is recorded as REJECT/not awaiting delivery and its ID is consumed; a fresh request raises not ready for a fresh review request. A manual edit or newly assigned revision becomes necessary outside the documented correction loop. This is a bounded cooperative workflow recovery failure, not a claim about a service or website.

Reproduction: `python3 -B /workspace/qualification/finders/correctness/reproduce.py`, exit 0. `reproduction.json` C01 shows all three verdict variants reject delivery a2 and request q2. The script supplies current identities and designated fresh review session, without any transport. Suggested correction: provide an explicit recovery transition preserving history, invalidating the previous artifact/request/verdict and allowing corrected delivery or renewed incomplete review. Retain current criteria unless their meaning changes.

## C02 — medium — Wrong review session or run can apply a terminal failure verdict

Evidence: `tools/coordination.py:88` compares REVIEW_KEYS, which omit reviewer session/run (`tools/task_gate.py:12`); lines 89–95 then store the verdict and apply terminal failure/incomplete states. The later gate checks session/run at `tools/task_gate.py:102`. `docs/coordination.md:21` requires the verdict to carry the same review identity, and line 73 promises stale verdict rejection.

Trigger: a current task/artifact/request envelope declares FAIL but carries a different or missing review session/run. Consequence: the coordinator records RECEIVE_VERDICT and enters CHANGES_REQUIRED. The real current reviewer's later verdict is rejected as not awaiting review. This can result from an incorrectly formed cooperative message; no attacker assumption is needed. The completion gate protects DONE but does not protect this earlier state transition.

Reproduction: the same script, `reproduction.json` C02. Request q1 names s1/run1. Verdict 6 names old-session/old-run and is accepted with FAIL. Current s1/run1 verdict 7 is then rejected. Suggested correction: check the current session/run before storing any verdict or changing state, including FAIL/PARTIAL/BLOCKED. This has a distinct validation fix from C01's missing recovery transition. It does not establish false DONE.

## Execution and profile effects

Preflight ran before consuming project facts:

`python3 .agents/skills/qore-review-qaizen-labs/scripts/project-check.py .agents/skills/qore-review-qaizen-labs/references/project.json --root /workspace/project/examples/qaizen-labs --method review`

Exit 0; checker returned current sources, no problems and COMPLETE profile freshness coverage only. Profile `qaizen-labs` 0.1.0 SHA-256: `f76afdd45cb6352e5044a06affc4182ea6cd40aa9c012fb216636a61faa428f0`. Complete rerun output is in `preflight.json`; the initial invocation used relative paths from the example root, and the saved invocation uses equivalent absolute script/profile paths. Surface source digest: `3728739a119a53272541f83d451e40addb6939304f9d9ec060a477a87170a4a3`; checker digest: `9ef2a0acf51f078ce290ec723ca550b8b73597e68304179fe4d0625c5757963b`.

Consumed facts and effects (also `profile-use.json`): surface-contract/checker selected the inspected offline command; close-focus/surface required separate summary focus and closed-help assertions; back-focus/surface required actual sequential traversal evidence before Enter and introduction heading focus; unanswered-scope/surface required intermediate unanswered samples and pre-entry method/origin guards. No web surface was returned for method review. Profile freshness is not behavior qualification.

Inspected the declared checker before executing `python3 -B checks/check_contract.py surface-contract.json` from the example root. Exit 0, valid=true; explicitly contract consistency only. Commands below ran from `/workspace/project`; complete stdout/stderr/argv/status are retained in individual command JSON files and indexed by `commands.json`:

- `python3 -B -m unittest discover -s tests -p 'test_coordination.py' -v`: 7 passed.
- Same command with `test_agent_mail.py`: 4 passed, fake transport only.
- Same command with `test_task_gate.py`: 18 passed.
- Same command with `test_labs_contract.py`: 3 passed.
- Same command with `test_browser_probe.py`: all 11 skipped, 0 browser checks executed. This is not a browser pass.
- `node --check tools/browser_probe.mjs`: exit 0, syntax only.
- Saved `reproduce.py`: exit 0, local measured outputs in `reproduction.json`.

Tests were rerun solely to retain full machine-readable command output. Initial `rg` inventory failed (exit 127: unavailable); used find/sed/cat instead. `git rev-parse HEAD` failed (exit 128: no HEAD); git status showed untracked project files. No Git base diff can identify this candidate, so a content snapshot was retained.

Boundary trace: server message ID → adapter-normalized id → consume's delivery_message_id → persisted register → request REVIEW_KEYS → verdict → completion gate → required proof file bytes. Delivery identity and actual artifact/proof hashes have positive and negative unit controls. C02 locates a mismatch between accepted verdict fields and terminal consumers; C01 follows a valid negative verdict to its missing correction consumer. Browser actions → traversal/focus events → result COMPLETE were inspected as a generic supplied-actions consumer. The specification explicitly requires additional Labs check-to-evidence mapping and input identity; generic COMPLETE alone was not treated as Labs acceptance. The checker, delayed predicate loop and separate state/focus assertions do not themselves establish current website behavior.

## Snapshot and remaining work

Target manifest digest: `b2a8222378dcceccf3a3e7422fd12919d870b44b80f5a386d0b49b60147cd688`. Installed derivative manifest digest: `bbe9e705eaf09beb556b0d5298d74778db2a2ba01e205c1e24389f707ac2ae0a`. `identity.json` records procedure and last relevant source mtime; `snapshot-manifest.json` records exact file hashes and mtimes, with scoped source bytes copied under `snapshot/`. Candidate manifest hashes the actual installed skill package. This is a working-tree artifact review, not a commit-diff review. Evidence was collected on 2026-10-16 UTC within the 150-second worker budget.

Totals: 2 unverified candidates, both medium; 0 independently confirmed, 0 independently refuted. No forced finding/refutation quota. No false DONE demonstrated. C01/C02 await fresh verification. The other required method roles, mechanical redaction, fresh verifier and final findings validation are the lead's unfinished work. Browser execution, actual wire exchanges, live scope acceptance, exhaustive malformed-input and cleanup fault injection were not performed. Dependency advisory assertions in coordination-dependencies.md were read as target limitations, not independently checked or endorsed. No public planning/UX evidence was used to certify quality. Overall method coverage remains PARTIAL; this worker supplies correctness evidence only.
