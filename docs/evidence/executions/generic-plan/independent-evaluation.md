# Independent planning evaluation

Evaluator: `/root/impl_validators/plan_value_evaluator`. Observed: 2026-10-15T20:14:49Z. This evaluator was neither a planning role nor the lead. Scope: two frozen-b planning runs; no source changes or external research.

Both runs support a useful, bounded next decision: lock exact verifier-token recognition, add a regression that fails on frozen b, and implement the parser correction only when implementation is authorized. Neither establishes a corrected release, clean-environment qualification, or human usability.

## Generic run

The initial problem is concrete: select the next safe improvement after existing envelope, severity and missing-verification acceptance already passes (`generic-plan/intake.json`; `proposed-spec.md:72–89`). This avoids presenting existing behavior as an unmet requirement.

Evidence connects that question to the selected decision. Delivery's raw record 0 uses the nonempty existing fixture: malformed `--verifier=ran=skipped` returns COMPLETE with DO-NOT-SHIP and a retained blocker. QA's `commands[0]` uses an empty packet and returns COMPLETE/SHIP. These are complementary measurements; Delivery did not independently measure the empty-packet SHIP branch. Frozen `finding-lint.mjs:6–10` explains both: prefix selection plus `split('=')[1]` discards the suffix. I independently reproduced the empty-packet behavior through `/dev/stdin`, including canonical and inverse-suffix controls.

The resulting D4–D7, A04–A09 and T1–T4 specify refusal categories, preserved semantics, dependencies and fresh-candidate qualification (`generic-plan/proposed-spec.md:84–197`). Cross-examination adds decision value: Product and Architecture move partial-batch proposals to follow-up after the measured grammar mismatch; their empty-partial ambiguity remains visible (`product-cross.md:7–15`; `architecture-cross.md:5–13`; `qa-cross.md:7–13`). This is justified prioritization, although no evidence ranks its commercial value or frequency against other work.

## Derived run

This run independently has the same problem-to-evidence-to-decision chain (`derived-plan/intake.json`; `delivery-commands.json[1]`; `qa-commands.json.records[2]`; `proposed-spec.md:74–101`). Its strongest additional contribution is a falsifiable test-quality correction. UX's cross probes and QA's independent `qa-cross-commands.json.records[0–2]` show malformed syntax plus a nonexistent file currently yields exit 2 and empty stdout because of ENOENT. Testing those two signals alone would falsely pass. The adopted A07 requires usage rather than a read error (`proposed-spec.md:175–180`); I reproduced the distinction between malformed suffix and unknown-value usage. This proves diagnostic precedence, not syscall-level absence of file access.

Profile use has actual effects. Preflight selects only `check` and `preserve-adaptations` from current `qore.json`; my source hash matches `948b2784…641c8`. `profile-selected-check.json` records executing the selected unittest argv and 82 passing tests. Preservation constrains D5/A08/T4 to unused staging, refusal and unchanged bytes (`proposed-spec.md:80–100,182–208`); existing `tests/test_package.py:183–217` genuinely tests those properties. This supports consumption beyond fact listing. It does not prove the profile improved the decision compared with generic planning, which also selected the same command and staging constraints.

## Completion, limits and usability

Both `run-validation.json` files report valid COMPLETE coverage while expressly excluding factual-quality certification. Both final spec hashes match their lint records. Rosters and artifacts support documented protocol completion; actor names alone do not establish isolation. The current collaboration listing exposes only the lead and this evaluator, so I cannot retrospectively certify the ten historical role contexts or absence of shared context.

The plans give a maintainer an identifiable next action and acceptance gates. Their 208/223-line specifications plus supporting reports have not undergone human comprehension testing. Reject any inference that agreement, nine linted scenarios or 82 baseline tests proves reasoning quality, post-fix correctness, production harm, clean-host independence or general method superiority. External callers, partial-batch semantics and corrected-candidate qualification remain open. These limits are largely acknowledged by the runs themselves.
