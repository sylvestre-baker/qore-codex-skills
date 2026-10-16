# Independent security finder — PARTIAL review coverage

One candidate, S1 (medium), awaits the lead's mechanical redaction and fresh verifier. This is a finder report, not independent verification or a final COMPLETE decision. Requested role: security; returned role: security, in this context only. No agents spawned, sibling reports read, redactor run, verifier phase performed, or repository source changed.

## S1 — Loopback Agent Mail bearer can be sent through an environment HTTP proxy

**Severity: medium.** `tools/agent_mail.py:25` checks the input URL hostname, `:34` adds the bearer, and `:35` builds an opener with the default environment ProxyHandler. The documented loopback-only transport (`docs/coordination.md`, Trust and evidence) therefore does not guarantee direct loopback dispatch.

Trigger: an ordinary cooperative executor has `http_proxy` set without a matching `no_proxy` exclusion. This does not require hostile cooperative users, concurrent writers or forged identities. Consequence: a remote HTTP proxy receives the bearer and RPC task metadata and mediates inbox responses. Actual exposure depends on that executor configuration; no real credentials or environment proxy settings were inspected.

Reproduction: `python3 -B /workspace/qualification/finders/security/repro_proxy.py` exits 0. It uses a synthetic token, synthetic proxy variables and a patched HTTP dispatch; no sockets or services. `repro_proxy.json` records `host: proxy.invalid:8080`, full loopback URL as selector, the synthetic Authorization header, and `fetch_inbox` arguments. Expected: direct loopback HTTP dispatch. Actual: proxy dispatch with the bearer retained. An initial attempt reached the same mocked dispatch but failed because the synthetic response lacked `.msg`; the saved corrected reproduction adds that fixture property. No target changes were made.

Concrete correction: explicitly disable proxies with `ProxyHandler({})` in the opener, retain NoRedirect, and add the environment-proxy regression. Unresolved: this finder has not performed a real proxy exchange or obtained fresh independent verification. Preserve medium impact severity during verification.

## Scope, identity and method

Initial available-skills catalog exposed these Qore entries: `qore-plan`, `qore-plan-qaizen-labs`, `qore-review`, `qore-review-qaizen-labs`, `qore-ux-review`, `qore-ux-review-qaizen-labs`. These came from the initial catalog, not discovery inferred from the user's pasted skill. Loaded installed entry: `/workspace/project/examples/qaizen-labs/.agents/skills/qore-review-qaizen-labs/SKILL.md`, including project profile/preflight, protocol, findings and execution-evidence references.

Target: public working-tree artifacts, not a diff or service security certification: example verification specification, contract/checker/actions/policy; four named repository tools; their five test modules and browser fixture; coordination documentation. Direct helper `tools/context.py` was inspected for JSON/profile parsing. No applicable AGENTS.md was found by the local repository filename search. `rg` is unavailable, so filename discovery used `find`. `git rev-parse HEAD` failed (no HEAD commit); `git status --short` showed an untracked initial working tree. Consequently source identity uses file hashes, not a fabricated commit.

`target-manifest.json` contains sorted relative file paths and SHA-256 per file; its canonical compact sorted-key JSON plus final LF hashes to `1f777e6490ab72f20dd247ea8ea2e9470be024d9d021c728aa8e49c9aa8d1d32`. Installed skill manifest, collected the same way, hashes to `9860886ee24c30b03a928c81489fc79875dedd35e4fc0242ae698b25f7123b9d`. `collect.py` retains the exact digest procedure. Snapshot captured after inspection; no source editing occurred. The README is included for source identity but was not substantively reviewed. Planning statements in verification-spec.md were treated as candidate claims, not independent quality evidence; no old unrelated evidence or author chat was read.

## Actual preflight, profile consumption and commands

Before project facts were consumed, ran from the installed derivative directory:

`python3 scripts/project-check.py references/project.json --root /workspace/project/examples/qaizen-labs --method review`

Exit 0, context coverage COMPLETE, no problems; surface/checker source digests both current. This is profile freshness only. Full retained result: `preflight.json`; repeated execution for retained command output is recorded in `commands.json`.

Consumed profile `qaizen-labs` 0.1.0, SHA-256 `f76afdd45cb6352e5044a06affc4182ea6cd40aa9c012fb216636a61faa428f0`. `checker` digest `9ef2a0acf51f078ce290ec723ca550b8b73597e68304179fe4d0625c5757963b`; `surface` digest `3728739a119a53272541f83d451e40addb6939304f9d9ec060a477a87170a4a3`. Exact per-fact sources and effects are in `profile-use.json`:

- `surface-contract` selected the declared command, inspected before execution.
- `close-focus` and `back-focus` selected separate source assertions and traversal inspection; no rendered focus claim.
- `unanswered-scope` selected method/navigation guard and sampled unanswered-state inspection.
- Review preflight returned no web surfaces; none were consumed or visited. Profile context never supplied permission.

From current example root, `python3 -B checks/check_contract.py surface-contract.json` exited 0: valid contract, explicitly consistency only.

From repository root, `python3 -B -m unittest discover -s tests -p NAME -v` exited 0 for each: `test_task_gate.py` 18 passed; `test_coordination.py` 7 passed; `test_agent_mail.py` 4 passed; `test_labs_contract.py` 3 passed. `test_browser_probe.py`: all 11 skipped for missing optional driver; zero browser passes. `node --check tools/browser_probe.mjs` exited 0 (syntax only). Full argv, cwd, stdout/stderr, exit codes and UTC capture times are retained in `commands.json`.

## Boundary trace and observations

Followed criteria from `initialize()` canonical sorted-key UTF-8 JSON with final LF → `criteria_sha256` stored in the Markdown qore-task block → task identity in normalized messages → delivery transport ID added from the actual envelope → request/verdict/proofs → `evaluate()` and DONE. Task fields are task_id/task_revision/criteria_sha256; delivery adds artifact_revision/artifact_sha256/delivery_message_id; review adds review_request_id, with session/run separately compared at the gate. Proofs emit/accept check_id, path and sha256; proof JSON must carry matching review identity, session/run, check_id and expected result. Actual artifact/manifest child/proof bytes are recomputed. No additional identity mismatch candidate was established.

Authorization/dependency booleans remain trusted PM inputs; received text does not set them. Reviewer freshness is a cooperative designation, explicitly not authentication. Missing hostile actor isolation or multi-writer locking is outside declared scope. Tests exercised rejection of stale identities, changed proof/artifact bytes and escaping relative paths. Path resolution also checks containment after resolving symlinks; no adversarial concurrent-filesystem guarantee was assumed.

Browser source places method and top-level/popup origin guards before navigation, blocks service workers and refuses document redirects before following. Outside-origin subresources are not prohibited by this declared top-level policy. Structured network records omit request headers/bodies; raw traces/DOM/screenshots/video and URLs are explicitly retained privately pending export review. No universal sanitization claim was inferred. Harness inputs/outputs were compared to acceptance: generic COMPLETE means supplied actions finished; enclosing Labs qualification still requires mapped proof and input identity. No live deployment claim was accepted from public planning/UX evidence.

## Limits and unfinished work

32 unit/structural tests passed and 11 browser tests skipped. Source review and socket-free reproduction cannot establish live network or browser behavior. No website, services, auth files, home profiles, private source or dependency binary was accessed. Coordination dependency documentation explicitly leaves binary feature/source correspondence and persistent recommendation PARTIAL; its linked advisory, signed archive and historical source-disposition claims were not independently fetched/revalidated during this bounded local-only finder run. No dependency vulnerability finding is asserted.

Unfinished: independent verification of S1, real driver-backed browser policy/keyboard controls, deployment observations, dependency/binary corroboration, and the lead's remaining method phases. Correctness and feasibility are other contexts' work and were neither read nor represented as returned here. No refutation quota was imposed. Finder totals: 1 candidate; independently confirmed 0, independently refuted 0; S1 unexamined by a fresh verifier. Overall method coverage remains PARTIAL. Available work and all artifacts were saved within the 150-second budget.
