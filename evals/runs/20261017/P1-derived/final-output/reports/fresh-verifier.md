# Independent source verification

Started: 2026-10-17 10:47:39 UTC. Ended: 2026-10-17 10:48:31 UTC.

Independent offline claim verification; inspected only the mechanically whitelisted claim set and cited original raw sources. No role reports, raw claims, adjudication, lead draft, prior answers, network, browser, or source edits.

Enclosing snapshot identity: `ed6c0fb8d8737cb4b8fc9e6b3485e0e618bf332d15725a557cf30d17b127e394`. This supplied enclosing identity was not recomputed and is not a per-file hash.

Coverage: all 12 supplied claims, one bounded pass, no retries; missing claim coverage: none. Eleven supported and one partially supported. Verdicts concern source support only; no live website behavior is certified. Supplied severities are retained, not independently re-ranked. No explicit refutation fields were supplied.

## Sources inspected

- /workspace/worker/target/verification-protocol.md
- /workspace/worker/surface-contract.json
- /workspace/worker/checks/check_contract.py
- /workspace/worker/observation-policy.json
- /workspace/worker/.agents/skills/qore-plan-qaizen-labs/references/project.json
- /workspace/worker/TASK.md

## C01: supported

Severity (as supplied): High. Kind: source_fact.

The target prescribes clicking Back; this does not prove the contracted sequential keyboard traversal and Enter activation.

Source references: target/verification-protocol.md:10; surface-contract.json#/transitions/6; checks/check_contract.py:35-36.

Evidence: Target line 10 says “Click Back”. Contract transitions[6] instead specifies traversal Tab and activation Enter; checker lines 35–36 requires sequential keyboard traversal and Enter. The project back-focus invariant expressly says a click or programmatic focus does not prove keyboard reachability.

Qualification and limits: This establishes an instruction/evidence gap in the fixture, not a deployed keyboard defect. The project invariant is corroboration from an inspected original source.

## C02: supported

Severity (as supplied): Medium. Kind: source_fact.

The target omits the summary Space-close and Enter-reopen steps present in the contract.

Source references: target/verification-protocol.md:7-8; surface-contract.json#/transitions/3; surface-contract.json#/transitions/4.

Evidence: Target lines 7–8 proceed directly from opening help to reaching Close. Contract transitions[3] and [4] prescribe summary Space to close, then summary Enter to reopen.

Qualification and limits: The target also leaves the initial summary activation unspecified, while contract transitions[2] specifies Enter. This corroborating omission does not change the supplied severity or scope of this claim.

## C03: supported

Severity (as supplied): High conditional impact; omission Medium in QA report. Kind: source_fact.

The target has no pre-navigation read-only/origin guard or blocked-analytics evidence instructions; no actual policy violation has been observed.

Source references: target/verification-protocol.md:5-10; surface-contract.json#/scope; surface-contract.json#/limits/2; .agents/skills/qore-plan-qaizen-labs/references/project.json#/invariants/2.

Evidence: The complete target lines 5–10 contains no request-method guard, navigation-origin guard, or blocked-analytics recording instruction. Contract scope permits GET/HEAD/OPTIONS, limits[2] requires retaining blocked analytics effects, and project invariants[2] explicitly requires blocking other methods and off-origin main-frame/popup navigation.

Qualification and limits: “Pre-navigation” is an operational ordering inference needed to protect initial navigation, not a quoted timing requirement. No live observation was performed, so the absence of an observed incident is an evidence limit, not proof that no incident exists.

## C04: supported

Severity (as supplied): Medium. Kind: source_fact.

Close restores summary focus while Back restores introduction-heading focus; these are separate obligations.

Source references: surface-contract.json#/transitions/5; surface-contract.json#/transitions/6; checks/check_contract.py:32-34.

Evidence: Contract transitions[5].focus_after is summary, while transitions[6].focus_after is introduction-heading. Checker lines 32–34 enforces these distinct destinations. Project close-focus invariant explicitly requires separate verification.

Qualification and limits: These are acceptance obligations. Neither the contract nor checker establishes current focus behavior in a browser.

## C05: supported

Severity (as supplied): Low source precision. Kind: sourced_decision.

Use forward sequential Tab then Enter for canonical Close and Back. Checker tolerance of Shift+Tab for Back does not amend the literal Tab transition or validate Close traversal.

Source references: surface-contract.json#/transitions/5; surface-contract.json#/transitions/6; checks/check_contract.py:32-36.

Evidence: Both literal contract transitions[5] and [6] use traversal Tab and activation Enter. Checker lines 35–36 accepts either Tab or Shift+Tab only for Back; it does not inspect Close traversal or Close activation.

Qualification and limits: Forward Tab as the canonical test is a sourced planning decision matching the literal contract. It is not a claim that Shift+Tab is forbidden: the project Back invariant expressly permits Tab or Shift+Tab. Checker tolerance does not rewrite the JSON transition.

## C06: supported

Severity (as supplied): High if guard weakened; no observed incident. Kind: source_fact.

Scope permits only GET, HEAD, OPTIONS and no answers; expected blocked analytics must retain observed effects.

Source references: surface-contract.json#/scope; surface-contract.json#/limits.

Evidence: Contract scope.answer_policy is unanswered and allowed_methods is GET/HEAD/OPTIONS. Limits[0] prohibits answers, results, and submission; limits[2] says “An analytics POST is expected to be blocked; retain its observed effects.” Project invariants[2] requires blocking all other methods and recording blocked analytics without relaxing policy.

Qualification and limits: Expected analytics is a declared expectation; no request, blocking event, or user-visible effect was observed in this offline pass. “Retain” applies to observed effects, which must not be invented.

## C07: supported

Severity (as supplied): Medium conditional. Kind: source_fact.

Contract and observation policy currently agree on https://qaizen.io as their sole allowed origin.

Source references: surface-contract.json#/allowed_origins; observation-policy.json#/allowed_origins.

Evidence: surface-contract.json.allowed_origins and observation-policy.json.allowed_origins each contain exactly one identical value: https://qaizen.io.

Qualification and limits: “Currently” refers to the supplied snapshot only; no remote policy or deployed origin behavior was checked.

## C08: supported

Severity (as supplied): Medium false-confidence risk. Kind: source_fact.

The checker reads contract JSON only, cannot validate Markdown or deployed keyboard behavior, and expressly limits its result to contract consistency.

Source references: checks/check_contract.py:42-50.

Evidence: The checker main routine parses json.loads(Path(sys.argv[1]).read_text(...)) and passes that object to validate. Its return explicitly states “Contract consistency only; browser observations establish current behavior.” There is no Markdown or browser processing.

Qualification and limits: This conclusion follows from reading the entire checker, not just the cited return/main lines. No checker execution was needed for this source-code claim, and no exit result is asserted.

## C09: supported

Severity (as supplied): Low in Delivery; Medium in Architecture. Kind: source_fact.

The target is a reconstructed fixture; acceptance expectations and historical baseline are not evidence of current website pass or defect, and private commits do not identify deployment.

Source references: target/verification-protocol.md:3; surface-contract.json#/provenance; surface-contract.json#/limits/3.

Evidence: Target line 3 explicitly identifies a newly authored reconstructed tutorial fixture and disclaims website-defect evidence. Contract provenance says expectations are acceptance obligations, not evidence that current deployment passed, and locates the proof gap in the protocol rather than the website. Limits[3] states private commits do not identify deployment.

Qualification and limits: The baseline date is a supplied provenance field, not independently verified historical browser evidence. Nothing here certifies a present website pass or defect.

## C10: supported

Severity (as supplied): scope constraint. Kind: source_fact.

TASK requests a plan for the target using original project sources, with outputs outside inputs and no supplied input or skill edits.

Source references: TASK.md.

Evidence: TASK.md requests planning changes to target/verification-protocol.md using the three original project sources; calls the tutorial a target rather than authority; requires outputs outside inputs; prohibits editing supplied input or skill resources and using prior reports or network answers.

Qualification and limits: This verifies the supplied task scope. This verifier only wrote the two requested output artifacts and did not execute the broader planning task.

## C11: supported

Severity (as supplied): Medium ambiguity; High potential guard violation. Kind: open_boundary.

Current profile requires origin guards for main-frame/popup navigation and method guards for all requests. Original allowlists do not explicitly resolve comprehensive third-party subresource authorization; no permission is inferred.

Source references: surface-contract.json#/allowed_origins; surface-contract.json#/scope; observation-policy.json; .agents/skills/qore-plan-qaizen-labs/references/project.json#/invariants/2.

Evidence: Project invariants[2] explicitly covers all non-GET/HEAD/OPTIONS requests and off-origin main-frame/popup navigation. Contract and observation policy provide origin lists but no explicit comprehensive third-party subresource authorization rule.

Qualification and limits: This is an open boundary, not a new permission or a finding that third-party requests are permitted. Method restrictions apply to all requests. The sources do not settle whether additional origin restrictions should cover every subresource.

## C12: partially supported

Severity (as supplied): Medium interpretation. Kind: proposal.

Interpret returned question/help absence at the visible, accessible and interactive presentation boundary, without requiring DOM deletion or questionnaire re-entry. Actual markup remains unknown.

Source references: target/verification-protocol.md:10; surface-contract.json#/states; surface-contract.json#/focus_targets.

Evidence: Target line 10 requires the introduction visible and question/help absent. Contract names returned-introduction as the destination and maps introduction-heading to h1. Neither source requires DOM deletion or questionnaire re-entry.

Qualification and limits: The proposed visible, accessible, and interactive presentation boundary is an interpretation, not an explicit source requirement. Sources do not define “absent” or supply markup. Avoid claiming accessibility-tree removal, hidden-control inertness, DOM removal, or re-entry behavior as verified facts. The proposal can be adopted as a planning decision with that qualification.

## Scope and completion

All supplied claims received an evidence-based verdict. C05 remains a sourced planning decision, C11 remains an open authorization boundary, and C12 remains an interpretive proposal with partial source support. Requirements and declared expectations have not been converted into observations. No comparative assessment or further verification cycle was performed.

The first recorded clock observation establishes the reported start; the dispatch timestamp was not separately available. The reported end is when the completed verification results were frozen for output.
