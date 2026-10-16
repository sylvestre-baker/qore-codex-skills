# Product analysis — validator hardening

- Role: Product; initial independent Analyze phase of qore-plan Workflow.
- Report timestamp: 2026-10-15T19:45:06Z (UTC timestamp observed from the host during analysis).
- Frozen target: `<CANDIDATE_B>`.
- Target snapshot supplied by dispatch: `dec34e19b7b3036c213299a1f98b05fec1709212fb156eabf9928682024ae2cb`. This role did not independently recompute the snapshot digest.
- Budget: 120 seconds. This report contains the available initial analysis; no peer conclusions, evaluation reports, or project profiles were read. No source or package files were changed.

## Outcome and recommendation

The next useful improvement is to make **partial independent verification explicitly expressible in the findings validator's declared result**, preserving completed verification work and identifying the remaining claims. Extend the existing specification rather than replacing its outcome or redesigning the review pipeline. This is a proposed priority, not an adjudicated implementation decision.

The maintainer's outcome remains the one already stated: distinguish malformed input, a complete review, and useful review work with missing independent verification, without severity downgrades or false success (`examples/validator-hardening.md:6-16`). A bounded verifier can finish some batches and leave others unfinished; the current findings contract already requires unexamined IDs, PLAUSIBLE verdicts for those claims, and PARTIAL overall coverage (`skills/qore-review/references/findings.md:22`). The smallest useful increment would let the machine-readable findings result carry this declared situation directly. It would not certify that the independent work actually happened: that remains an execution-evidence obligation (`skills/qore-review/scripts/finding-lint.mjs:51`; `skills/qore-review/references/run-evidence.md:28-34`).

The product outcome is that a maintainer can retain a partially completed review and determine what to resume without seeing SHIP for that declared state. Test count and lint passage are supporting proxies, not the outcome.

## Current evidence

All source citations below are relative to the frozen target root above.

1. The existing specification is directly applicable: it names the actual validator-hardening work, calls for inspection of these validators/tests, and expressly permits a legitimate zero-finding result (`examples/validator-hardening.md:4`, `examples/validator-hardening.md:68-70`). This selects Workflow, as required by `skills/qore-plan/SKILL.md:10-13` and `skills/qore-plan/references/protocol.md:5-7`.
2. The original scope is already substantially implemented. Envelope rejection is at `skills/qore-review/scripts/finding-lint.mjs:15-19`; skipped verification restricts candidates to PLAUSIBLE at line 35; blocking findings are derived from CONFIRMED critical/high claims at line 44. Tests cover malformed envelopes, explicit empty findings, skipped severity preservation, missing-verifier verdict restrictions, evidence/counterexamples, and redaction (`tests/test_validators.py:64-124`). I found no reason to invent a new product or assert that these original cases are broken.
3. The CLI accepts only `ran` and `skipped` (`skills/qore-review/scripts/finding-lint.mjs:6-10`). Every valid `ran` packet receives COMPLETE coverage, and one without confirmed high/critical blockers receives SHIP (`skills/qore-review/scripts/finding-lint.mjs:43-51`). A PLAUSIBLE verdict alone does not reveal whether a verifier examined the claim and remained uncertain, or never examined it. The findings contract distinguishes unresolved observation from confirmation (`skills/qore-review/references/findings.md:18-22`). Do not infer incompleteness from PLAUSIBLE alone.
4. Partial verification is already a documented scenario; it is not a hypothetical new workflow (`skills/qore-review/references/findings.md:22`; `skills/qore-review/references/run-evidence.md:28-34`). The existing user-facing contract separately distinguishes validation, actual execution coverage, and delivery authority (`docs/contracts.md:49-55`).
5. The redactor already performs the independence-related mechanical filtering. Its scalar allowlist and rejection behavior are implemented (`skills/qore-review/scripts/redact-for-verifier.mjs:13-31`) and have regression coverage (`tests/test_validators.py:115-124`). No product evidence here justifies changing its allowlist or merging the two scripts.

### Measurements performed

- Ran the exact project check from `qore.json:4`, with frozen target root as working directory: `python3 -B -m unittest discover -s tests -v`. Result: exit 0; 82 tests, 2.784 seconds, OK. Environment observed: Node v22.23.3, Python 3.14.7, local macOS host. This is baseline regression evidence, not proof of all product requirements.
- Read-only interface probe: used Python `subprocess.run` to supply JSON through `/dev/stdin` to `node skills/qore-review/scripts/finding-lint.mjs /dev/stdin --verifier=ran --json`. Input was an explicit findings envelope with one high PLAUSIBLE claim, ID F1, evidence `src/input.ts:12`. Observed exit 0, valid true, COMPLETE, SHIP, no blockers, and the existing limitation text. This constructed input demonstrates current flag semantics only; its title does not establish real unexamined work, and no defect was planted in the target. Source control flow independently supports the result at `finding-lint.mjs:44-51`.
- Searches/read checks found no applicable AGENTS.md at the checked target and ancestor paths. A broader reference search included a nonexistent top-level `scripts` path and returned exit 2; relevant hits were still read directly. No absence-of-impact conclusion relies on that search.

## Proposed product decisions and scope

Retain existing D1–D3 and US1–US2 from `examples/validator-hardening.md:12-23`.

| Proposed ID | Decision and reason | Observable deliverable |
|---|---|---|
| PD4 | Add an explicit declaration of partial verifier completion. Preserve the existing absent-verifier and completed-verifier paths. | A valid packet declared partially verified yields PARTIAL coverage and cannot yield SHIP. Architecture should choose the smallest compatible CLI/packet representation; no syntax is locked by this role. |
| PD5 | Distinguish unfinished claims from examined-but-unresolved PLAUSIBLE claims through declared IDs. Do not overload severity or verdict for this purpose. | Output identifies the unexamined finding IDs; existing IDs, severity, verdicts, evidence and refutations remain intact. |
| PD6 | Preserve verified blockers even when some other claims remain unexamined. | A partially verified packet containing a supported CONFIRMED critical/high claim remains PARTIAL with DO-NOT-SHIP and that blocking ID. Without a verified blocker, the scoped result is PENDING. |
| PD7 | Keep the result a structural/declaration check, with actual execution coverage checked separately. | Documentation and output retain the limitation that flags/IDs do not prove actual independence or execution. No new overall review certification is claimed. |

New story US3: “As a maintainer whose verifier stopped before all batches finished, I can retain the examined results and see the exact remaining claims, so I can resume review without representing it as complete.” This refines the existing US2 rather than adding an unrelated capability.

In scope: the existing example specification, findings validation behavior, focused public-entry-point regression tests, and the directly affected CLI/contract documentation. A protocol update is needed wherever existing instructions teach the two-state invocation (`skills/qore-review/SKILL.md:14`; `skills/qore-review/references/findings.md:7-11`; `docs/contracts.md:38`). Exact packaging/release-file consequences remain Delivery's investigation.

Out of scope for this increment: a general JSON schema platform, evidence provenance service, new persistent project profile, browser/native interface, database, API, new independent-agent scheduler, changes to UX scoring, severity downgrades, and automatic publication/merge permission. None is needed to express the documented partial-batch outcome. Actual independent context identity remains an execution-evidence concern.

## Measurable acceptance proposal

Preserve A01–A03 from the existing example (`examples/validator-hardening.md:30-48`). Add the following to its next version with real Gherkin steps and a coverage mapping, following `skills/qore-plan/references/specification.md:9-17`.

```gherkin
Feature: Preserve useful partial verification
  Scenario: A04 Retain mixed completed and unfinished claims
    Given F1 is a supported CONFIRMED medium finding
    And F2 is a high PLAUSIBLE finding declared unexamined
    When the findings validator receives an explicit partial-verification declaration
    Then the packet is structurally valid with PARTIAL coverage and PENDING verdict
    And F2 is identified as unexamined
    And both finding IDs, severities and verdicts are preserved

  Scenario: A05 Preserve a verified blocker during partial verification
    Given F1 is a CONFIRMED high finding with checkable evidence and a counterexample
    And F2 is PLAUSIBLE and declared unexamined
    When the findings validator receives an explicit partial-verification declaration
    Then coverage is PARTIAL and the verdict is DO-NOT-SHIP
    And F1 remains in blocking_findings
    And F2 remains unexamined and non-blocking

  Scenario: A06 Reject contradictory unfinished-claim declarations
    Given the declared unexamined IDs include a missing finding ID
    When the findings validator validates the packet
    Then the declaration is rejected and SHIP is unavailable

  Scenario: A07 Reject a verification verdict for an unexamined claim
    Given F1 is declared unexamined and has a CONFIRMED verdict
    When the findings validator validates the packet
    Then the declaration is rejected and SHIP is unavailable

  Scenario: A08 Keep examined uncertainty distinct from unfinished work
    Given every claim was declared examined
    And one claim remains PLAUSIBLE after examination
    When the validator receives a completed-verifier declaration
    Then the claim is not automatically relabeled unexamined
    And its severity and PLAUSIBLE verdict are preserved
```

Coverage proposal: A04 → US2/US3/D2/D3/PD4/PD5; A05 → US2/US3/D2/D3/PD6; A06/A07 → US1/US3/D1/PD5; A08 → US2/D2/PD5. QA should add the corresponding REFUTED-unexamined and duplicate/non-string ID boundaries once the declaration shape is chosen. Existing A03 must continue to permit an explicit valid empty review when the required phases actually completed. A truthful empty packet must not be forced into an invented finding to express a missing phase; PD4 must also represent partial execution without relying exclusively on a nonempty unexamined-ID list.

## Risks, triggers and evidence

| Risk | Trigger and affected behavior | Checkable basis / required check |
|---|---|---|
| Representation cannot distinguish unresolved from unexamined | Treating all PLAUSIBLE claims as unfinished would misstate a completed verifier's work. | `skills/qore-review/references/findings.md:19-22`; A08 checks the distinction. |
| Partial work loses an established blocker | Implementation assigns a blanket PENDING result to every partial packet. | Existing blocker invariant at `qore.json:7` and derivation at `finding-lint.mjs:44`; A05 must keep the blocker. |
| New declaration is mistaken for independent proof | A caller supplies completion metadata without corresponding phase evidence and reports global success. | Existing limit at `finding-lint.mjs:51` and evidence contract at `run-evidence.md:28-34`; preserve warning and separate coverage reporting. This increment cannot eliminate dishonest declarations. |
| Inconsistent callers/documentation | The validator grows a third state while skill instructions still expose only ran/skipped. | `skills/qore-review/SKILL.md:14`, `docs/contracts.md:38`; Delivery must sweep actual references. |
| Scope expands beyond the useful increment | The work adds a new proof subsystem before partial batches can be expressed. | Explicit hypothesis about implementation risk; Architecture must show an existing interface requirement before adding a component. |
| Acceptance gets optimized for lint alone | Spec passes structural checks while unresolved behavior has no acceptance scenario. | `skills/qore-plan/references/specification.md:38`; require the observable matrix above plus the existing regression suite. |

## Named peer questions and challenges

- **Architecture:** Which smallest existing boundary can accept a partial declaration and expose unexamined IDs while preserving both current invocations? Show why a new schema/module would be necessary before proposing one. How will an examined PLAUSIBLE claim stay distinct from an unexamined one? How can a zero-finding packet still declare incomplete execution?
- **Delivery:** What concrete consumer requires more than findings-lint, its contract instructions, tests and example-spec update? Do not assume full run-record integration or changes to all validators are prerequisites. Identify packaging/release metadata that genuinely requires regeneration from source evidence; do not estimate unsupported migration effort.
- **QA and security:** Can you validate A04–A08 and identify contradictions/unknown IDs without relying on real phase execution being inferable from JSON? What existing test ensures compatibility of the two old modes and the explicit-empty review?
- **UX:** What concise CLI summary lets a maintainer distinguish “valid but unfinished” from “rejected input” and “verified blocker remains”? Should pending counts and IDs appear in plain output as well as JSON? Keep this within the local command/report interface.

## Uninspected scope and unfinished work

The role read the example specification; all four dispatched qore-plan files; both review scripts; `tests/test_validators.py`; qore.json; findings/run-evidence review references; qore-review SKILL.md; and directly cited contracts excerpts. It ran the complete project suite but did not inspect every test implementation, generated adaptation, release manifest, run-check implementation, or run schema. No project profile, peer report, other evaluation report, external source, native UI or browser was consumed.

Unfinished: Architecture's minimal representation and compatibility sweep; QA's boundary matrix; Delivery's actual packaging effects; UX's wording requirements; independent Cross-examine and lead adjudication. The chosen PD4–PD7 are proposals until those phases. The report itself is complete for initial Product Analyze, while the overall Workflow is still in progress. This role did not produce a final specification, perform spec-lint on a new specification, implement changes, or claim complete five-role coverage. No evidence establishes an actual missed production finding; the proposal improves how an already documented partial execution is represented.
