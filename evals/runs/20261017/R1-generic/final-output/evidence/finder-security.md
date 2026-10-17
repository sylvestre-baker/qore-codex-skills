# Independent finder report: security

Execution coverage: COMPLETE for the assigned security review of the supplied immutable protocol against the three named criteria files. No verifier verdict is assigned here. No website observation was performed, and no website defect is asserted.

## Scope and snapshot

Target: `/workspace/worker/target/verification-protocol.md`, entire 10-line reconstructed fixture. Criteria: `/workspace/worker/surface-contract.json`, `/workspace/worker/checks/check_contract.py`, `/workspace/worker/observation-policy.json`. Instructions read: `.agents/skills/qore-review/references/protocol.md` and `findings.md`. No other finder report was accessed. No subagents, networking, browser use, or shared input mutations.

SHA-256:

- Target: `b8d1f4ad7bd691dbf8f019cd3b87a7644a21899e6317edebac545fd3b245136e`
- Surface contract: `3728739a119a53272541f83d451e40addb6939304f9d9ec060a477a87170a4a3`
- Checker: `9ef2a0acf51f078ce290ec723ca550b8b73597e68304179fe4d0625c5757963b`
- Observation policy: `15f4e5b4960b5011684be265f027e42b8637a3b8aae96b24bba1ba3a4d0f0202`

## Candidate S-1 — medium — missing read-only request-policy procedure

Evidence: protocol lines 5–10 list navigation, help manipulation, answer state and focus assertions, without request-method setup or observation. Contract line 6 allows GET, HEAD, OPTIONS only; line 18 requires `read-only-policy`; line 20 says an analytics POST is expected to be blocked and its effects retained. A UI-only sequence does not specify those actions.

Trigger: the journey attempts the anticipated analytics POST or another prohibited method, with no external guard already present. Requirement and practical consequence: the operator must keep observation within the read-only boundary and retain blocked-request effects, but can complete all listed steps without that evidence and, absent external guarding, without preventing the request. No inference is made that a real deployment currently attempts such a request.

Contrary-evidence search within all supplied sources: protocol lines 6 and 9 explicitly preserve unanswered state; this is useful evidence for answer policy but does not enumerate or block request methods. The contract and checker declare method requirements. Checker lines 17–18 validate only JSON declarations, and lines 42–43 explicitly disclaim runtime observation. None of the supplied sources establishes that a browser guard is already installed for this procedure. This limitation is retained in the candidate condition rather than treated as a proven website behavior.

Suggested disposition for independent verification: inspect whether a procedure executed exactly as written could establish the method policy or preserve the expected blocked-POST effects. If correction is authorized, add guard setup before the first navigation and evidence collection for attempted blocked requests and effects.

## Candidate S-2 — medium — missing authorized-origin procedure

Evidence: protocol line 5 opens a public entry and follows a link; lines 5–10 never check actual origins or invoke observation-policy.json. The latter permits only `https://qaizen.io` at lines 2–4; contract lines 5 and 18 specify that origin and require `origin-policy`. Checker lines 12–15 validate the declared entry URL only.

Trigger: a selected link, redirect, or observed request crosses to a different origin without a separate externally configured guard. Requirement and practical consequence: the sole-authorized-origin boundary needs verification, but every stated assertion could finish without establishing it. A crossing is conditional; no actual external request or navigation is alleged.

Contrary-evidence search: the contract entry URL is correctly on the allowed HTTPS origin and the provenance URLs are also on that origin. Those declarations do not establish the runtime destination of navigation or requests. The entry selector is a suffix selector at contract line 9, which itself does not prove an absolute origin; no inference is made that any particular off-origin link exists. The observation policy contains the right allowlist but supplies no automatic enforcement mechanism. The checker explicitly reports contract consistency only.

Suggested disposition for independent verification: inspect the actual listed operations for an origin-policy assertion or guard. If correction is authorized, require loading/enforcing the sole origin policy before navigation and recording policy observations.

## Required producer-to-consumer trace

Central values: `scope.allowed_methods` and `allowed_origins`.

1. Primary source/storage: contract JSON actually contains `allowed_origins: [https://qaizen.io]` and `scope.allowed_methods: [GET, HEAD, OPTIONS]` (lines 5–6). The separate observation-policy JSON actually contains only `allowed_origins: [https://qaizen.io]` (lines 2–4). This is file content, not inferred network transmission.
2. Contract file fields actually emitted: `schema`, `version`, `entry_url`, `allowed_origins`, `scope`, `states`, `transitions`, `focus_targets`, `required_checks`, `provenance`, `limits`. Scope emits `locale`, `viewport` (width, height), `depth`, `answer_policy`, `allowed_methods`. Transitions emit `id`, `from`, `to`, `control`, `activation`, and optionally `traversal` and `focus_after`.
3. Receiving code: checker main reads the requested file and parses JSON (line 50). `validate` consumes `schema`, `entry_url`, `allowed_origins`, `scope.answer_policy`, `scope.allowed_methods`, `states`, transition `id/from/to/control/activation/focus_after`, Back `traversal`, `focus_targets`, `required_checks`, and `provenance.kind/urls`. It verifies the declared allowed-method set and entry origin but does not receive browser request events or the procedure text. Extra keys are not rejected. It does not read observation-policy.json.
4. Actual serializer/output: lines 42–43 and 51 emit precisely `valid`, `schema`, `checks`, `limit`. The successful run emitted the eight required check names and the literal limitation `Contract consistency only; browser observations establish current behavior.` It emitted neither `allowed_origins` nor `allowed_methods`, request logs, blocked-request evidence, or performed browser checks.
5. Final consumer/decision: the target is a prose procedure; its complete emitted steps are opening entry/following link, starting unanswered, opening help, keyboard Close/focus assertion, unanswered assertion, and clicking Back/introduction/focus assertion. It does not explicitly receive the checker output or either policy value. There is no evidence that the checker output is transmitted into the procedure, and this report does not invent such a link. Comparing the criteria-to-procedure boundary directly shows both required network-policy checks have no corresponding procedural operation. A passing checker result cannot supply missing runtime evidence.

## Commands, results, and artifacts

1. Read only the four named inputs and two skill references using `cat`; exit 0.
2. Read numbered lines of the four inputs with `nl -ba`; exit 0.
3. Ran `python3 -B checks/check_contract.py surface-contract.json`; exit 0, JSON `valid: true`, all eight check labels listed, and explicit contract-consistency limitation. No website was contacted by this checker.
4. Ran `sha256sum` on all four inputs; exit 0; identities recorded above.
5. Wrote this report and strict candidate envelope under `/workspace/output/evidence` only.

Candidate output: `/workspace/output/evidence/candidates-security.json`; complete role report: `/workspace/output/evidence/finder-security.md`.

Limits: two documentary security candidates, no assigned confirmation/refutation, no runtime exploit demonstration, no source beyond the expressly supplied local artifacts. No unfinished assigned scope. Live enforcement may exist externally, but the supplied procedure does not establish it. Final independent verification and delivery decisions belong to subsequent phases.
