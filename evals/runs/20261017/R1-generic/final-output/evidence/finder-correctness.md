# Correctness finder report

Role: independent correctness finder. Target: `/workspace/worker/target/verification-protocol.md` only, checked against the supplied original contract, validator, and observation policy. Discovery was independent: no other finder reports were read and no coordination was performed. No network or website observation was used. Inputs were treated as immutable. This report is a finder report, not a verifier verdict or delivery decision.

## Scope and result

Completed the assigned source review, including all six protocol steps, the contract states/transitions/checks, validator behavior, and the observation-policy origin list. Two candidate findings are recorded below. Finder execution coverage: COMPLETE for this supplied correctness scope. Overall Qore execution coverage is for the lead to determine after the other roles and independent verifier. No unfinished assigned scope. Current website behavior, actual browser state/focus, deployment identity, and implementation defects were not examined and are not claimed.

## C-1 — Clicking Back leaves the required keyboard transition untested (medium)

Evidence: `target/verification-protocol.md:10` explicitly instructs “Click Back.” The receiving acceptance requirement in `surface-contract.json:15` is a Back transition with `activation: Enter`, `traversal: Tab`, and `focus_after: introduction-heading`; line 18 lists `keyboard-back`. `checks/check_contract.py:35-36` requires Tab or Shift+Tab traversal and Enter activation. The protocol has a keyboard traversal instruction for Close (line 8), but it does not extend that instruction to Back.

Triggering condition: Back works on pointer clicks and performs the specified visual and focus updates, but fails sequential keyboard reachability or Enter activation. Practical consequence: all six written steps can be followed without exercising the keyboard-back acceptance obligation. A keyboard navigation failure can escape this procedure. No observed website failure is asserted.

Correction direction: replace the Back click instruction with sequential Tab or Shift+Tab traversal to Back and Enter activation, retaining the existing state and focus assertions. This report does not apply changes.

## C-2 — The procedure omits the required summary toggle and reopen sequence (medium)

Evidence: `surface-contract.json:11-13` declares summary Enter to open help, summary Space to close it, and summary Enter to reopen it; line 18 requires `help-toggle`. `target/verification-protocol.md:7` opens help through summary without naming the input, then line 8 directly activates the separate Close control. Lines 5-10 contain no Space activation or reopen step.

Triggering condition: Close works but summary Space closing or Enter reopening fails, or summary is pointer-operable but keyboard activation fails. Practical consequence: every stated assertion can succeed while the help-toggle obligation and declared summary keyboard path remain untested. No observed website failure is asserted.

Correction direction: make Enter explicit when opening help, insert a summary Space toggle with a closed-state assertion, then summary Enter with an open-state assertion before exercising Close. This report does not apply changes.

## Required value trace and adjacent boundary comparison

Central value: the Back activation and traversal obligation.

1. Producer/source and storage: the original on-disk `surface-contract.json:15` stores the transition object `{id: back, from: help-closed, to: returned-introduction, control: Back, activation: Enter, traversal: Tab, focus_after: introduction-heading}`. These are actual JSON fields, not a comment or inferred network transmission. `focus_targets` at line 17 resolves the focus name to `h1`.
2. Actual deserializer/consumer: `checks/check_contract.py:50` reads the named file as UTF-8, applies `json.loads`, and passes the object to `validate`. For each transition, lines 23-31 consume `id`, `from`, `to`, `control`, `activation`, and optional `focus_after`; for Back, lines 32-36 additionally consume `traversal` and require Tab or Shift+Tab and Enter. This matches the stored original Back fields.
3. Fields emitted and accepted at the contract/checker boundary: the actual contract top-level keys are `schema`, `version`, `entry_url`, `allowed_origins`, `scope`, `states`, `transitions`, `focus_targets`, `required_checks`, `provenance`, and `limits`. Scope emits `locale`, `viewport` (width/height), `depth`, `answer_policy`, and `allowed_methods`. The validator reads schema, entry URL, origins, answer policy, allowed methods, states, transitions, focus targets, required checks, provenance kind, and provenance URLs. It does not evaluate version, locale, viewport, depth, provenance date/note, or limits. Transition records emit `id`, `from`, `to`, `control`, `activation`, with `traversal` and `focus_after` only for the applicable entries; the checker reads the fields described above rather than rejecting unknown fields.
4. Actual serializer/output: `checks/check_contract.py:42-43` returns exactly `valid`, `schema`, `checks`, and `limit`; line 51 serializes that result using `json.dumps(..., indent=2)` to stdout. The executed command emitted `valid: true`, the schema, the eight required-check names, and the limitation “Contract consistency only; browser observations establish current behavior.” Transition activation/traversal fields and observed browser results are absent from that output.
5. Claim and final decision boundary: the human-readable protocol's actual final consumer is a tester following line 10, which requests a mouse click and final state/focus assertions. This differs from the original contract's Enter/traversal obligation. No supplied source demonstrates that this Markdown is generated from checker stdout; this report makes no such transmission claim. The checker output explicitly cannot establish protocol/browser coverage, and its passing result does not fill this gap.

Secondary adjacent-boundary mismatch: the contract's `help-toggle` check plus Space/Enter transition inputs (lines 11-13, 18) become no equivalent instructions in protocol lines 7-8; Close/Enter is a different transition.

## Reasonable contrary-evidence search

Read all four supplied files and searched their full contents for Back/back, toggle, Space, Enter, Tab, help, keyboard, checks, and the consistency limitation. The only protocol keyboard instruction is the Close step at line 8. The final heading focus assertion at line 10 is evidence of an intended focus outcome, but does not supply the missing keyboard trigger. Contract provenance at line 19 expressly distinguishes acceptance obligations from observed deployment behavior and says the proof gap was in the protocol, not the website. The successful validator result expressly disclaims browser proof. `observation-policy.json:2-4` contains only the authorized origin `https://qaizen.io` and provides no alternative keyboard procedure. These observations constrain the claims to missing protocol coverage. They are not independent verifier verdicts on the candidates.

## Commands and results

- `cat /workspace/worker/.agents/skills/qore-review/references/protocol.md /workspace/worker/.agents/skills/qore-review/references/findings.md`: exit 0; read role protocol and findings schema.
- `nl -ba /workspace/worker/target/verification-protocol.md`, `nl -ba /workspace/worker/surface-contract.json`, `nl -ba /workspace/worker/checks/check_contract.py`, `nl -ba /workspace/worker/observation-policy.json`: each exit 0; obtained complete source and checkable line numbers.
- `python3 -B /workspace/worker/checks/check_contract.py /workspace/worker/surface-contract.json`: exit 0; stdout is preserved in `correctness-check-output.json`. It reports contract consistency, not protocol or browser success.
- `sha256sum /workspace/worker/target/verification-protocol.md /workspace/worker/surface-contract.json /workspace/worker/checks/check_contract.py /workspace/worker/observation-policy.json`: exit 0; identities below.
- `rg -n 'Back|back|toggle|Space|Enter|Tab|help|keyboard|checks|Contract consistency'` over the four supplied files: exit 127 (`rg: not found`). Used a Python line scan over those four files with exactly those search terms instead: exit 0; results match the cited locations. No network fallback.
- Output creation used Python standard-library JSON serialization and UTF-8 file writes under `/workspace/output/evidence`; no source changes.

Executed contract-check output:

```json
{
  "valid": true,
  "schema": "qaizen-labs-surface/1",
  "checks": ["entry", "unanswered", "help-toggle", "close-focus", "keyboard-back", "introduction-focus", "read-only-policy", "origin-policy"],
  "limit": "Contract consistency only; browser observations establish current behavior."
}
```

## Snapshot and artifacts

SHA-256:

- `target/verification-protocol.md`: `b8d1f4ad7bd691dbf8f019cd3b87a7644a21899e6317edebac545fd3b245136e`
- `surface-contract.json`: `3728739a119a53272541f83d451e40addb6939304f9d9ec060a477a87170a4a3`
- `checks/check_contract.py`: `9ef2a0acf51f078ce290ec723ca550b8b73597e68304179fe4d0625c5757963b`
- `observation-policy.json`: `15f4e5b4960b5011684be265f027e42b8637a3b8aae96b24bba1ba3a4d0f0202`

Saved artifacts: `/workspace/output/evidence/finder-correctness.md` (complete role report), `/workspace/output/evidence/candidates-correctness.json` (strict candidate envelope), and `/workspace/output/evidence/correctness-check-output.json` (actual checker stdout).

Candidates: 2; independently confirmed/plausible/refuted counts: not assigned at finder phase. No self-verification verdicts. No unfinished source-review scope or unexamined candidate IDs in this role. Required independent verification remains a separate phase.

Final artifact check: a Python JSON parse/assertion checked the candidate envelope, required nonempty string fields, allowed severities, and unique IDs (exit 0; "Candidate envelope: valid; 2 findings; no duplicate IDs."). This is structural validation only, not claim verification.
