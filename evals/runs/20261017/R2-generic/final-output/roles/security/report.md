# Independent security finder report

Target: `/workspace/worker/target/verification-protocol.md` (reconstructed tutorial fixture, explicitly not historical website evidence). Primary sources were limited to `/workspace/worker/surface-contract.json`, `/workspace/worker/checks/check_contract.py`, and `/workspace/worker/observation-policy.json`. Method references read: qore-review `references/protocol.md` and `references/findings.md`. No peer artifacts were read and no subagents were used.

Timing: dispatch-derived start is 2026-10-17T11:20:25Z (parent's 180-second allocation and 11:23:25Z deadline). First directly sampled clock was 2026-10-17T11:21:09Z; earlier reads did not capture a clock timestamp. Completion recorded at 2026-10-17T11:21:51.482255+00:00. Actual token/CPU usage is unavailable from this host.

## Candidate S-1 — medium — Procedure omits the required origin and read-only network controls

Supporting evidence: the complete action list at target lines 5–10 contains no origin or HTTP-method policy setup or verification, nor any blocked-request evidence instruction. Contract lines 5–6 constrain origins to `https://qaizen.io` and methods to `GET`, `HEAD`, `OPTIONS`. Contract line 18 requires `read-only-policy` and `origin-policy`; line 20 anticipates a blocked analytics POST and requires retaining its observed effects. Observation policy lines 2–4 repeats the same sole authorized origin.

Trigger and impact: a reviewer follows only these six steps in a browser without an independently installed request filter, and the page attempts the analytics POST anticipated in contract line 20 (or redirects to an unauthorized origin). All specified visual/focus assertions can pass while request authorization is unestablished. A protocol execution can therefore look successful without satisfying two required acceptance checks, and may permit disallowed request side effects. This is an omission in the protocol; it is not evidence that any actual website request was emitted.

Contrary evidence and limits: unanswered state is explicitly preserved in target lines 6, 9 and 10. Target line 3 disclaims historical and website-defect evidence. The allowed origin lists agree across the two JSON sources. A mandatory external harness could establish these controls, but none is supplied or referenced in the protocol. The checker validates declarations and explicitly limits its result to contract consistency; it cannot supply browser enforcement. No browser runner, actual request log or deployment trace is available in the permitted evidence. No dependency vulnerability or actual privacy exposure is claimed.

Suggested correction: establish the policy-enforcing harness before first navigation; enforce the supplied origin and HTTP-method limits and retain blocked-request/effects evidence. If another harness owns this, make it an explicit prerequisite. Candidate verification and disposition belong to the independent verifier.

## Mandatory source → transformation → claim → decision trace

Central values: `allowed_origins`, `scope.allowed_methods`, and `required_checks` policy entries.

1. Producer/storage: `surface-contract.json` stores top-level fields `schema`, `version`, `entry_url`, `allowed_origins`, `scope`, `states`, `transitions`, `focus_targets`, `required_checks`, `provenance`, and `limits`. Security-relevant values are the sole HTTPS origin at line 5, the three permitted methods and unanswered policy at line 6, the two policy obligations at line 18, and the expected blocked POST at line 20. `observation-policy.json` actually stores only `allowed_origins`; it agrees with the contract and contains no method field.
2. Actual parser/consumer: `check_contract.py:50` reads and JSON-decodes the contract file supplied on the command line. Lines 12–18 consume `entry_url`, `allowed_origins`, `scope.answer_policy` and `scope.allowed_methods`, checking authorized HTTPS entry and the exact method set. Lines 19–41 additionally consume states, transition identifiers/from/to/control/activation/focus_after, focus targets, Back traversal, required-check names, and provenance kind/URLs. It does not read observation-policy.json or the protocol, enforce browser traffic, consume `limits`, or turn required-check names into observed results.
3. Actual emitted serialization: lines 42–43 produce `valid`, `schema`, `checks`, `limit`, and line 51 serializes that object with `json.dumps`. Saved command output has `valid: true`, `checks` containing `read-only-policy` and `origin-policy`, and `limit: Contract consistency only; browser observations establish current behavior.` There are no observed-origin, observed-method, blocked-request, request-effect or browser-result fields. This is not evidence of transmission to a browser; no such transmission exists in the supplied checker.
4. Receiving procedural contract/final consumer: a human/browser executor receives the six natural-language steps at target lines 5–10. They specify unanswered and UI/focus observations, but no policy precondition or evidence field. The adjacent-boundary mismatch is between declared mandatory network-policy observations and a written procedure that does not establish or record them. A success decision from only those written assertions cannot establish the two declared policy checks. The sources do not demonstrate that anyone made such a success decision.

## Executed checks and scope

- Read and numbered all four target/source files; SHA256 snapshot and exact content are in `source-snapshot.txt`.
- Executed `python3 -B /workspace/worker/checks/check_contract.py /workspace/worker/surface-contract.json`; exit 0, `valid=true`. Full actual stdout/stderr and command are in `contract-check.json`.
- Compared the two stored origin lists, read the complete protocol, enumerated checker output fields, and saved raw results in `static-policy-trace.json`.
- The initial attempted file search using `rg` failed because `rg` is absent; continued with explicit supplied paths. This did not limit source access.
- Examined authorization/origin boundaries, read-only method constraints, unanswered state, expected analytics effects, provenance limits, and the absence of actual browser/dependency implementation. No network requests, site interactions, source-input mutations, or website-source redistribution occurred.

Unfinished scope: no static security-source area within the assigned target remains unread. Browser enforcement/actual traffic, external harness behavior, deployment properties and dependency advisories remain unobserved and were outside the authorized supplied-source review. This is a finder report only; no independent verdicts are assigned.

Candidate count: 1. Candidate IDs: S-1. Strict envelope: `findings.json`.
