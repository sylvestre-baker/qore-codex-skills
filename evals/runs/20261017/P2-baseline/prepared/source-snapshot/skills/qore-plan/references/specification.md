# Specification artifact contract

Use the user's established destination and naming convention. Otherwise choose a focused file under `docs/specs/` and state its path. Preserve applicable existing content and version the result. Do not silently split a user's change into unrelated replacement specifications.

Every new or edited specification produced by this method has:

- First line `<!-- qore-spec/1 -->`.
- Outcome, scope, authoritative inputs and their revisions, constraints, and explicit non-applicable surfaces.
- User stories and decisions with stable IDs. Distinguish sourced facts from proposed decisions and unresolved authority.
- Architecture and reuse/impact evidence where applicable; contracts, compatibility, rejection behavior, and configuration/data effects.
- A Mermaid `flowchart` for the relevant components or information flow and a fenced Mermaid `sequenceDiagram` for the actual runtime or execution flow, including its main rejection path. Show real boundaries; do not invent transactions or services.
- For interface changes, entry paths, state transitions, content and accessibility requirements. A planned check is not a native or browser observation.
- Tasks with size and rationale, risk, dependencies, critical order, coupling, acceptance gates, and applicable documentation/test/rollout tasks.
- Real acceptance scenarios inside `gherkin` fences. Each scenario has `Given`, `When`, and `Then` steps; `And`/`But` add conditions. A `Scenario Outline` has populated `Examples`. Empty fences and arrow shorthand do not satisfy acceptance coverage.
- A `Coverage:` mapping from scenario IDs to user stories and locked decisions. Cover meaningful failure and boundary paths, not just nominal behavior. Map every applicable supplied acceptance criterion and QA feedback item; name missing coverage.
- Adjudicated decisions, rejected alternatives, material dissent, dependencies, and open questions.
- Mode, actual role/phase coverage, rounds and stopping reason, artifacts, limits, and structural validation result.

Minimal scenario shape:

```gherkin
Feature: Preserve a user's working files
  Scenario: AC01 Existing destination is preserved
    Given the requested output directory already contains a working file
    When generation is attempted for that directory
    Then generation refuses that destination
    And the existing working file is unchanged
```

`Coverage: AC01 → US1 / D1` must use the actual IDs in the specification. Ensure the mapping covers the declared stories and decisions; a linter cannot establish whether a missing requirement should have been declared.

From the skill directory run:

```bash
bash scripts/spec-lint.sh /absolute/path/to/spec.md
```

Retain the exit status and output. Repair missing required structure without changing requirements merely to satisfy the checker. If the checker is unavailable or fails for an unresolved reason, report the failure and PARTIAL/BLOCKED validation coverage. A valid document can still contain unresolved decisions; structural validity does not approve implementation or establish overall quality.
