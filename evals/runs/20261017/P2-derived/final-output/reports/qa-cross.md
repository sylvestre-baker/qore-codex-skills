# QA and security cross-examination

Status: COMPLETE one Workflow cross-examination pass. Role: QA and security. Same supplied candidate 8b26119f383a7d5853c1bd2ab5f678e08966300846c0d6f2784351c1f5a59e8d and enclosing manifest 92981d42bbb636d2809b22af476c7974c1a1f54b539b8e5a7d6c9767b0d53b1d. Initial report remains unchanged; corrections below supersede ambiguous portions only.

## Evidence inspected and limits

Read cross-brief.md and ALL five complete initial reports: product-analysis.md, architecture-analysis.md, ux-analysis.md, delivery-analysis.md and qa-analysis.md. Initial combined output truncated; recovered full Architecture, UX and Delivery reports in separate reads before this conclusion. Reused the full raw-source inspection from initial analysis: target lines 3, 7–10; surface-contract lines 4–20; checker lines 12–18, 32–43; observation-policy in full; original project.json unanswered-scope invariant. No network, browser, input or peer-report edits. No new runtime measurements. Actual DOM, state, focus and guard operation remain unknown.

## Explicit challenges to all four peers

### Product — P1/P4 and measurable acceptance story 3

Exact decision challenged: story 3 treats Tab or Shift+Tab Close traversal as one sufficient instruction while the overall coverage criterion requires all contract items. Failure case: a future record contains only Shift+Tab Close traversal and calls the literal contract Tab transition observed. Surface line 14 specifically declares Tab; target line 8 allows either, and checker lines 35–36 accept either only for Back, not Close. The target alternative is valid procedure scope but does not erase path specificity.

Smallest investigation: compare those three source locations and require the observation record to name the actual traversal direction. Selected recommendation: retain “Tab or Shift+Tab” as the target's alternative; identify Tab as the canonical contract path for Close. A Shift+Tab-only Close run establishes that target alternative and the observed Close/focus outcome; it leaves the canonical Tab traversal unobserved. Do not remove the alternative or infer Tab proof. Same path labeling applies when describing literal Back contract traversal, though the checker explicitly permits Back either way. This is an evidence-label correction, not authorization for extra runs now.

Product P4 properly asks Architecture/QA to settle scope, but citations to the raw contract/policy alone cannot substantiate main-frame/popup semantics: those files declare an allowed-origin value without the profile's finer granularity. Accept pre-navigation wording when it separately attributes that granularity to the fresh original project invariant. Reject a ban on all cross-origin resources.

### Architecture — A3/A4 and future runtime sequence

Exact decision challenged: A3 leaves Close alternative classification for adjudication; A4 says guards across new main frames/popups but cites raw files that do not themselves name those boundaries. Concrete failure: a maintainer could interpret that as all-resource same-origin enforcement, disrupt an allowed read-only resource, and call it original project acceptance; alternatively, they could start initial navigation before the guard is active.

Smallest investigation: compare raw policy/contract origin declarations with original project.json invariants/unanswered-scope, already read. Selected recommendation: methods apply to all requests; the profile-supported origin restriction applies to main-frame/popup navigations, with redirects checked before unauthorized arrival. Explicitly identify the profile contribution; do not call the tiny policy file a runtime guard or proof. If the observer cannot establish these preconditions, stop before navigation as unable to execute under policy, not as a failed website journey. No implementation needs selection for this documentation plan.

Architecture A2 adds ordinary keyboard focus of summary, a reasonable procedure instruction for Enter/Space activation. It must remain tool-independent and avoid a new exact Tab sequence/count unsupported by evidence. No new architecture component is justified. Accept A1/A5 and bounded impact sweep.

### UX — decision 5, decision 7 and minimum unanswered evidence

Exact decision challenged: decision 5 asks preservation of both traversal alternatives but could allow a single combined pass label to hide canonical Tab coverage; decision 7 says “failed or unverified as appropriate” without a decision rule. Concrete cases: the heading visibly returns but actual focus remains elsewhere; Back is not found within 24 real sequential steps; no usable focus observation was captured. These need three distinct descriptions, not one generic failure.

Smallest investigation: source comparison above plus apply a result table to those three cases. Selected rule: (a) actual observed wrong focus means that focus assertion failed for that run; (b) actual 24-step exhaustion means the bounded procedure requirement was not met, while universal keyboard reachability and downstream return/focus remain unestablished; (c) absent/incomplete observation means unobserved, not observed assertion failure. None alone warrants an unqualified website-defect claim. Report an interrupted journey as incomplete even if some sub-obligations passed.

Accept UX's counting proposal as a clearly labeled procedure convention: one Tab or Shift+Tab press is one traversal step, count across both directions, start from the recorded focus after Close. It clarifies the existing 24-step limit without inventing site behavior. Exact unanswered DOM representation remains unknown; minimum evidence is a timestamped/ordered assertion of no selected answer after Close and again immediately before starting Back traversal, without selecting anything or collecting answer payloads. Do not mandate a specific selector implementation.

### Delivery — D4, D5 and later definition of done

Exact decision challenged: D4's “incomplete/failed reachability evidence” conflates a measured bounded failure with absent proof; later done requires each transition mapped but does not explicitly prevent a Shift+Tab-only record becoming canonical Tab proof. Failure case: a reviewer signs off the whole website based on a prose coverage table, an exit-zero checker and an interrupted future run.

Smallest investigation: apply the three-case result table above to D4 and add canonical-path labeling to T3's review checklist. Selected recommendation: planning done is a sourced reviewable proposed document, source map and limitations; later documentation done requires prose coverage/preservation and offline checker only. Future runtime status is separately per obligation/path. Keep all seven transitions/eight required checks mapped, both unanswered checkpoints and the 24-step limit explicit; never substitute checker results for document review or browser evidence. Estimates 50–85 minutes are already labeled hypotheses and need no new measurement. No browser/harness prerequisite belongs on this critical path.

## Corrections to my initial QA report and claims

- My initial decision 1 said “Contract allows Tab or Shift+Tab via checker” in a paragraph discussing both Close and Back. Narrow that statement: checker lines 35–36 explicitly validate either traversal for Back only. The literal current contract declares Tab for both. Target alternatives remain valid to preserve, but observation must report which path was actually used. QA-1 is retained with this refutation/correction appended, not deleted.
- My initial matrix and Gherkin remain useful procedure tests, but “sequentially” alone must not be read as evidence for the canonical Tab path when only Shift+Tab occurred. The canonical/alternative result rule above qualifies all such rows/scenarios.
- My initial “not observed/blocked” shorthand must not merge actual observed assertion failure, traversal-bound exhaustion and unavailable evidence. The result table above replaces that ambiguity; QA-4 now includes it.
- My initial QA boundary wording already separated method and navigation scope. Retain that decision and clarify provenance: raw sources provide methods/origin value; original fresh project invariant supplies main-frame/popup detail. The report did read that original.

## Minimum evidence and outcome table

| Situation | Record | Conclusion allowed |
|---|---|---|
| Canonical Close path completed | Start focus, actual Tab trace to Close, Enter, closed help, actual summary focus | Canonical Close traversal and observed outcomes, plus separate unanswered assertion |
| Only Shift+Tab Close completed | Actual alternative trace and same state/focus assertions | Target alternative observed; canonical Tab traversal unobserved |
| Back reached at/before traversal 24 | Start focus, ordered keys/count, control and Enter, actual visible state/absence/focus | Each observed obligation judged independently; no global website claim |
| 24 traversals without Back | Count/keys, starting and last focus, no activation | Local bound unmet; dependent Back/return/focus unobserved; no universal inaccessibility conclusion |
| Correct page, wrong focus observed | Actual active element and visible-state result | Visibility may pass; focus assertion fails for this run |
| No usable focus record | Available state/action record and missing evidence | Focus unobserved, no invented failure or pass |
| Guard unavailable before entry | Missing precondition | Do not navigate; unable to perform compliant observation |
| Expected analytics POST blocked | Method/destination block and observed effects | Policy behavior recorded; dependent interrupted checks unobserved; no policy relaxation |

Unanswered checkpoints remain separate ordered records even when adjacent: after Close, and immediately before leaving the question/starting Back traversal. An active-element trace and ordinary state observations suffice as evidence requirements; no new storage schema, recording tool or website-source redistribution is necessary.

## Severity, dissent and unresolved scope

Retain QA's MEDIUM help-sequence coverage rating versus UX's HIGH acceptance-reliability rating. Both are consequence assessments, not measured incident severity; there is no evidence requiring an averaged score. Preserve QA HIGH boundary/evidence-integrity risk and MEDIUM assertion-preservation risk, even where Product/Delivery rank preservation HIGH. This does not change required acceptance coverage.

Selected recommendation resolves the source tension by preserving target alternatives and requiring path-specific evidence, with canonical Tab called out. A candidate wording that silently removes Shift+Tab or treats its sole observation as canonical Tab proof remains unacceptable to QA. The lead must adjudicate exact wording rather than invent role unanimity. No additional analysis round is requested.

Unfinished: lead adjudication, final candidate-wording review against the preservation matrix, and structural validation of the final planning artifact. Deployment behavior, actual policy tooling, exact unanswered DOM representation and tab order remain deliberately unobserved; future authorized observation would resolve those empirical unknowns. No supplied-input changes or runtime work are required to complete this plan.
