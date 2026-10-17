# Performance / feasibility finder report

Role coverage: COMPLETE for the supplied six-step protocol and the four authorized substantive sources. No website observation, network requests, other finder reports, or shared-data mutations were used. Candidate findings are submitted for fresh verification; this role assigns no confirmation/refutation verdicts. No performance certification is claimed: surface-contract.json:20 expressly excludes it and no runtime/resource service objective is specified.

## Snapshot and sources

Review target: /workspace/worker/target/verification-protocol.md, reconstructed tutorial fixture, QORE-003 (line 3). Requirements: original surface-contract.json, original observation-policy.json, original checks/check_contract.py. Skill references protocol.md and findings.md were read. SHA-256 identities:

- target/verification-protocol.md: b8d1f4ad7bd691dbf8f019cd3b87a7644a21899e6317edebac545fd3b245136e
- surface-contract.json: 3728739a119a53272541f83d451e40addb6939304f9d9ec060a477a87170a4a3
- checks/check_contract.py: 9ef2a0acf51f078ce290ec723ca550b8b73597e68304179fe4d0625c5757963b
- observation-policy.json: 15f4e5b4960b5011684be265f027e42b8637a3b8aae96b24bba1ba3a4d0f0202
- .agents/skills/qore-review/references/protocol.md: e27e0050fdf4d75d2840dd257b9a759f1f48d459ef540990cd3aed5528c5f340
- .agents/skills/qore-review/references/findings.md: f9f9035e471c9832c6546e80e4fe857777fefceba781bd5801ee8f97bdeaa409

## Required value trace: help-toggle acceptance evidence

Producer/storage: surface-contract.json:18 stores required_checks including help-toggle. Its operational definition is the transition cycle in lines 11-13: open-help (summary, Enter, first-question→help-open), toggle-help (summary, Space, help-open→help-closed), reopen-help (summary, Enter, help-closed→help-open). All transition objects emit id/from/to/control/activation; close-help and back additionally emit traversal/focus_after. Top-level stored fields are schema, version, entry_url, allowed_origins, scope, states, transitions, focus_targets, required_checks, provenance, limits. scope emits locale, viewport {width,height}, depth, answer_policy, allowed_methods. provenance emits kind, urls, baseline_observed_on, note.

Transformation/actual serialized output: checks/check_contract.py:50 parses that exact file with json.loads, validate checks selected fields, and lines 42-43 return only valid/schema/checks/limit. Line 51 actually serializes those four fields to stdout with json.dumps. The executed command exited 0 and emitted valid=true, schema=qaizen-labs-surface/1, checks=[entry, unanswered, help-toggle, close-focus, keyboard-back, introduction-focus, read-only-policy, origin-policy], and limit=Contract consistency only; browser observations establish current behavior. Complete stdout is saved in feasibility-check-output.txt.

Receiving contract: validator accepts schema, entry_url, allowed_origins, scope.answer_policy/allowed_methods, states, transition id/from/to/control/activation and optional focus_after, focus_targets keys, back traversal/activation, close/back focus_after, required_checks, provenance.kind/urls. It does not compare protocol text, execute transitions, or emit observed states, executed actions, actual focus, network records, viewport, or locale. It does not itself enforce runtime policy. This is consistent with its explicit limit, so the checker is not itself reported defective.

Final consumer/decision: the human executing target/verification-protocol.md has six numbered imperative steps and visual/focus assertions as the observable output; no structured results serializer, output schema, input file reference, or rule consuming checker stdout is specified. There is no evidence that checker success is transmitted into or consumed by this procedure. Comparing the source requirement directly with the procedure shows no Space/reopen actions, pointer Back in place of sequential keyboard Back, and no runtime policy setup/check. Thus the procedure does not necessarily produce the evidence its declared checks require. Findings concern missing proof in this protocol, not false statements about the deployed website.

## Candidates

### F-201 — Help verification omits the required Space toggle and Enter reopen cycle

Severity: medium.

surface-contract.json:11-13 requires summary Enter to open, Space to close, and Enter to reopen; required_checks includes help-toggle at line 18. target/verification-protocol.md:7-8 only opens help with an unspecified activation and immediately reaches Close; all six procedure steps (lines 5-10) contain no Space or reopen action. Trigger: follow the written procedure exactly on a deployment where summary Space or Enter is broken but pointer opening and Close work. Requirement: execute declared help-toggle acceptance transitions. Impact: the procedure can finish without generating evidence for either missing transition, so a help keyboard regression remains undetected.

### F-202 — Pointer Back cannot supply the required sequential keyboard Back evidence

Severity: medium.

target/verification-protocol.md:10 explicitly says Click Back and only checks destination state and heading focus. surface-contract.json:15 requires Back traversal Tab and activation Enter; line 18 requires keyboard-back. checks/check_contract.py:35-36 explicitly distinguishes sequential keyboard traversal and observed activation. Trigger: Back responds to a pointer click and focuses the heading but is absent from the tab order or fails Enter activation. Requirement: observe keyboard traversal and Enter activation of Back. Impact: the written check can pass while the required keyboard journey is unusable; destination focus alone does not measure how Back was reached or activated.

### F-203 — Procedure has no operational step to enforce or observe the declared network boundary

Severity: medium.

surface-contract.json:5-6 restricts origins and permits only GET/HEAD/OPTIONS; line 18 requires read-only-policy and origin-policy, and line 20 expects an analytics POST to be blocked and its observed effects retained. observation-policy.json:2-3 supplies the single allowed origin. target/verification-protocol.md:5-10 gives six UI-only steps with no setup/import of either policy, network interception, method/origin verification, or retention of blocked-request effects. checks/check_contract.py:14-18 validates declared data only and its returned limit at lines 42-43 is explicitly contract consistency only. Trigger: a normal browser session follows the procedure and navigation/help actions emit analytics POST or cross-origin subrequests. Requirement: constrain actual observation to the allowed origins/methods and retain blocked effects. Impact: an operator can complete every written assertion without establishing the required read-only/origin checks, and an expected POST has no specified mechanism to be blocked.

## Contrary-evidence search and limits

Read every protocol step and all contract fields. The protocol does explicitly preserve unanswered state (steps 2/5), verifies Close Enter activation and summary focus (step 4), and verifies introduction focus after Back (step 6). These observations cover some adjacent obligations but cannot establish the missing action paths. The presence of Enter/Tab in step 4 is specific to Close; no instruction carries it to Back in step 6. The source contract explicitly labels expected transitions acceptance obligations rather than website observations (line 19); no website defect is inferred. The policy JSON is a declaration and the checker validates declared scope; neither supplied source shows automatic attachment of network enforcement to these six manual steps. Network finding is therefore a protocol enforcement/evidence omission, not an observed unauthorized request. Locale/viewport setup is also absent, but this report does not elevate that alone to a separate finding because no rendering or reproducibility failure was observed.

## Commands and results

1. pwd && rg --files target checks .agents/skills/qore-review/references | head -60: pwd=/workspace/worker; rg unavailable (/bin/sh: rg: not found). Switched to direct reads.
2. cat surface-contract.json observation-policy.json checks/check_contract.py target/verification-protocol.md .agents/skills/qore-review/references/protocol.md .agents/skills/qore-review/references/findings.md: exit 0; all authorized sources read completely.
3. nl -ba on target/verification-protocol.md, surface-contract.json, checks/check_contract.py, observation-policy.json: exit 0; locations cited above.
4. python3 -B checks/check_contract.py surface-contract.json: exit 0; valid=true and only contract-consistency output. Repeated once solely to retain exact stdout in feasibility-check-output.txt.
5. Read-only Python transition enumeration/text-presence probe: exit 0; enumerated all seven transition objects; Space/reopen absent from protocol. Simple substring HEAD appeared because heading contains that substring, so this probe is not treated as evidence for a network method instruction; full source read resolves that ambiguity.
6. Python SHA-256 and report artifact write: input files read only; output restricted to /workspace/output/evidence.

## Deliverables and unfinished scope

Saved complete role report: /workspace/output/evidence/finder-feasibility.md.
Saved strict candidate envelope: /workspace/output/evidence/candidates-feasibility.json.
Saved checker transcript: /workspace/output/evidence/feasibility-check-output.txt.

Three medium-severity candidates. No candidate was self-confirmed or self-refuted. All supplied target steps reviewed; no unfinished assigned scope. Browser execution and website observation deliberately excluded. No measurement supports a website performance or accessibility conclusion; neither is asserted. Fresh verifier and parent aggregation remain outside this role.
