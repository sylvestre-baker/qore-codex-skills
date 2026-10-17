# Five planning perspectives

Use these five distinct roles. Role names describe a lens; they do not imply professional certification or grant authority over the project. Each role returns sources, its deliverables, peer challenges, and unfinished work.

| Role | Examine and produce | Challenge |
|---|---|---|
| Product | User outcome, scope, user stories, measurable acceptance criteria, business constraints, and the smallest useful version. Distinguish an outcome from a proxy metric. | Architecture on unnecessary complexity; Delivery on scope and assumptions. |
| Architecture | Reuse, components, data, contracts, trust boundaries, failure behavior, compatibility, and transaction ownership. Produce decision records, a component flow, and a runtime sequence. | Product on ambiguous invariants; UX on complexity; warn QA about failure paths. |
| UX | Entry paths, state transitions, loading/empty/error behavior, content, accessibility, localization, and recovery. Produce state and interaction requirements. | Architecture on user-facing complexity; QA on observable state coverage. |
| Delivery | Tasks, sizes and their basis, risk, dependencies, critical path, rollout/rollback where relevant, and definition of done. Separate initial scope from deferred work. | Product on scope realism; Architecture on implementability and prerequisites. |
| QA and security | Acceptance coverage, boundaries, abuse, authorization, privacy, data integrity, negative paths, and evidence needed for release decisions. Produce a test matrix and edge-case Gherkin. | All roles on testability, omitted conditions, and unsupported risk claims. |

Architecture performs a visible reuse and impact sweep before proposing a duplicate operation:

1. Find existing behavior, services, routes, tables, and shared invariants.
2. Check documented interfaces and reusable schemas; plan documentation updates for affected contracts.
3. Trace shared values through every applicable reader and writer. Distinguish derived reads from stored snapshots; justify no-change classifications with sources.
4. Establish the ownership of transactions, retries, side effects, guards, and authorization context. A helper opening its own transaction may invalidate a caller's intended atomic boundary.

These checks apply only where such surfaces exist. For a document or local tooling change, identify its actual file/host boundaries instead of inventing an API or database. Missing evidence is an open item, not a reason to copy another project's conventions.

The lead owns scheduling, the roster, budgets, source discipline, and adjudication. It retains conflict and minority evidence rather than averaging the roles' opinions.
