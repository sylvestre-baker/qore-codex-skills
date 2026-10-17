# Product cross-examination

Status: COMPLETE for one Product Workflow cross-examination. This is a fresh Product cross-examination context; it does not claim continuity with the retired initial Product agent. The initial report remains intact. No lead proposed protocol, peer cross report, browser, network or supplied-input edits were used.

## Sources and coverage

Read all five full initial reports: product-analysis.md, architecture-analysis.md, ux-analysis.md, delivery-analysis.md, qa-analysis.md. Initial combined output was truncated; separately reread Architecture, UX and Delivery in full to close that gap. Read raw TASK.md, target/verification-protocol.md, surface-contract.json, observation-policy.json, checks/check_contract.py, skill SKILL.md, original references/project.json, fresh profile-check.json and cross-brief.md. The current preflight marks the profile's two raw sources current. Original raw contract facts and profile interpretations are distinguished below. No website behavior was observed.

## Mandatory Architecture complexity challenge

Exact decision challenged: Architecture A4 says “Ensure the chosen observer can enforce guards before entry and across new main frames/popups; otherwise stop as unable to verify under policy.” Architecture A1 simultaneously rejects a runner and correctly keeps this documentation-only.

Concrete failure case: interpreting A4 as a dependency for approving this plan would require selecting or constructing interception tooling despite there being no supplied observer. It could prevent a complete, reviewable documentation plan until a new implementation exists. This contradicts TASK.md:3-5 and A1, and is unnecessary complexity. Architecture's unfinished section already says actual observer selection must not block this documentation plan; retain that qualification next to A4.

Evidence and smallest investigation: compare A4 with TASK.md and the actual five-line observation-policy.json. That file supplies only allowed_origins; it installs no guard. Inspect original project.json invariant unanswered-scope: its current profile wording explicitly covers all non-GET/HEAD/OPTIONS requests and main-frame/popup outside-origin navigation. Raw contract line 6 supplies methods; line 5 plus observation-policy supplies the origin. Main-frame/popup specificity is profile-supported interpretation, not literally present in raw JSON fields. This inspection resolves the documentation wording without any implementation investigation.

Selected correction: make enforceable pre-entry guards a future execution precondition, never a planning-completion dependency. State all-request method filtering and navigation-origin restrictions separately. Do not ban every cross-origin resource. Keep tooling choice, interceptor APIs, schema changes and runtime demonstration outside this change. Product's earlier P4 delegated exact wording; this pass resolves it and makes the source distinction explicit. Severity remains high for a future boundary violation; risk of unnecessary infrastructure is medium. They are different risks, not averaged.

## Mandatory Delivery scope challenge

Exact decisions challenged: Delivery D4 calls bound exhaustion “incomplete/failed reachability evidence,” and its later documentation definition of done permits the 24-step guard to remain “or any change [be] explicitly justified.”

Concrete failure case: a maintainer writes a single failed keyboard-back label after 24 steps, then infers the website cannot be reached by keyboard. Another trims the apparently redundant unanswered assertion or removes the bound under a generic scope rationale. Both weaken or overstate the supplied procedure. Target lines 9-10 separately require an unanswered observation after Close and immediately before leaving, plus traversal within 24 steps. The raw contract contains no numeric accessibility bound; provenance line 19 and target line 3 prevent this fixture becoming deployment-defect evidence.

Smallest investigation: clause-by-clause comparison of target lines 8-10 with the acceptance map; no browser run. This establishes exactly what must survive and what the bound means.

Selected correction: retain 24 and both unanswered checkpoints for this proposed clarification; there is no source-backed reason to change them. Distinguish (a) observed exhaustion of the local bounded traversal, (b) observed unmet focus assertion after a successfully activated transition, and (c) a missing observation, including downstream states not reached. Only (b) establishes an unmet focus obligation in that run; none independently proves a website defect. Record actual starting focus, traversal directions/count, last focus and activation/outcome. Delivery's 50–85 minute estimate stays an unmeasured later-work hypothesis, not a commitment or a dependency on a live run. Scope remains one proposed document plus rationale/coverage review; no harness, production verification or application repair.

## Close traversal conflict and Product revision

Exact decisions challenged: UX decision 5 calls the target alternatives “valid” and describes the contract's Tab as a precision difference; QA decision 1 says “Contract allows Tab or Shift+Tab via checker lines 35–36.” Architecture A3 correctly flags unresolved Close semantics. Product P1 originally preserved sequential Close without stating the canonical/alternative evidence distinction.

Raw evidence: surface-contract.json:14 declares close-help traversal Tab and Enter with summary focus. Line 15 declares Back traversal Tab. Checker lines 35–36 accept Tab or Shift+Tab only for Back; they do not check Close traversal. Target line 8 allows Tab or Shift+Tab for Close, and line 10 allows both for Back. Profile back-focus likewise explicitly permits both for Back. There is no equivalent supplied Close profile invariant that broadens its traversal.

Counterexample: a run reaches Close only with Shift+Tab and returns focus to summary. It proves that target-permitted alternative and the resulting focus observation; it does not observe the raw contract's canonical Tab traversal. A checker pass cannot fill that missing observation. Calling that canonical Close path passed silently erases a source-defined distinction.

Selected recommendation: preserve target's Tab/Shift+Tab alternative, name Tab as the canonical raw-contract Close path, record actual direction, and mark canonical Tab traversal not observed when only Shift+Tab was exercised. Do not force an extra reset or second run into this small journey. A separate future canonical run may supply the missing evidence; this plan need only state the limitation. Keep Close state/focus evidence distinct so valid observations are not discarded with the missing canonical path. Back remains sequential Tab/Shift+Tab under the target and explicit checker/profile support, with 24 total traversal steps across directions. This refutes QA's broad reading of the checker for Close and qualifies UX's unannotated validity language. Product revises P1 accordingly; the original claim is preserved in the claims ledger with this qualification.

## Remaining peer challenge and verdict discipline

QA evidence fields and UX actual-focus guidance strengthen Product P5: screenshots of a visible introduction cannot prove heading focus, and the help Enter-open, Space-close, Enter-reopen observations cannot collapse into “help works.” Keep focus results and visible-state results separate, including summary after Close and heading after Back. Preserve entry and Start clicks; converting the entire journey to keyboard-only is unsupported by surface lines 9-10. Stop dependent evidence claims when a required step cannot be observed; do not use clicking or programmatic focus to rescue the keyboard proof.

Product's original help-gap severity is medium. UX rates the same omission high for acceptance reliability. This pass retains both assessments and the common concrete mitigation; there is no evidence of deployed harm to adjudicate an incident severity. Architecture's high policy/evidence risks and QA's low overreach risk describe distinct triggers and remain explicit.

## Selected Product position and dissent

The smallest useful deliverable is a concrete proposed replacement passage outside the supplied input, a preservation/source map, and offline validation limits. Add only scope/guard preconditions, exact Enter–Space–Enter sequence, and concise evidence/outcome guidance. Preserve the fixture disclaimer, entry/Start actions, separate Close/Back focus outcomes, absence assertions, both unanswered checkpoints and the 24-step bound. Existing checker success is contract consistency only; human prose coverage review is separately necessary. All eight required checks and seven transitions require an instruction/evidence location, not a fabricated deployment result.

Material dissent retained: unqualified Shift+Tab Close equivalence is rejected for canonical raw-contract evidence, while the target alternative remains available. A universal all-resource same-origin ban is unsupported. Future guard enforceability is required before observation but not before completing this plan. Delivery's broad “incomplete/failed” bound wording is replaced with the three outcome distinctions above. Initial Product assertions remain preserved; P1/P4/P5 are qualified rather than erased.

## Unfinished coverage

No Product cross-examination investigation remains for this bounded pass. Lead adjudication and final candidate review remain outstanding. Current deployment behavior, interception implementation, actual tab order, unanswered representation and blocked analytics effects remain unobserved and are intentionally outside this planning task. This report claims complete Product challenge coverage, not independent live verification or complete team adjudication.
