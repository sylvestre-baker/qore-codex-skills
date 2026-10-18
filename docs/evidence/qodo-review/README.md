# Qodo review case: evidence and limits

On 18 October 2026, two Qodo Agentic Toolbox CLI 1.6.0 issue reviews returned findings on a known public Qore correction. Two separate fresh Codex contexts examined all three returned native claim IDs after mechanical filtering. This is retrospective, agent-driven evidence on the maintainer's computer.

Start with the [reproducible tutorial](../../tutorials/qodo-review.md), rather than reading raw metadata first.

| Artifact | What it supports |
|---|---|
| [Provider excerpts](provider-excerpts.json) | Selected native claims, exact source snapshots, returned roles, warnings and coverage |
| [Verification summary](verification.json) | Scope-specific reproductions/refutations, native classifications and interpretation |
| [Selected original terminal probes](recorded-probes.json) | Actual normalized commands, exit codes and output for historical builds, profile checks, derivation and validator controls |
| [New focused replay](focused-replay.json) | New local execution of the bundled helper snapshots with labeled fixtures |
| [New live preparation](live-preparation.json) | A local target matching the complete 77-file historical change; no Qodo submission |
| [Provenance](provenance.json) | Private input identities, selection rules, rights scope and authentication limits |
| [Exact public source inventory](../../../examples/qodo-review/sources.json) | Pinned commits and digests of the helper sources used by the focused replay |

The profile-check regression is historical and already corrected on checked main `e9d74cf`. The text-summary observation is informational: JSON retains the unresolved finding and verdict stays PENDING. The stale-hash failure belongs to our initial incomplete slice, not the complete published correction.

The full Qodo result's issue reviewer completed, but its explicit spec reference was unresolved and its previous finding inventory was incomplete. Overall coverage remains PARTIAL. All three returned claims were examined; this does not establish that every possible defect was found.

Raw account/session information, authentication screens, full terminal traces and the proprietary CLI bundle remain private. Public excerpts carry a recorded transformation identity. A private-input hash cannot authenticate the original provider response by itself. Readers can reproduce the public code observations without a Qodo account; a new live Qodo run is optional and may return different findings.

No human usability trial, production adoption, new vulnerability disclosure, performance comparison, Qodo endorsement or programme appointment is claimed. Existing Qore method-execution evidence keeps its original identity; this cross-tool example is not a replacement for it.
