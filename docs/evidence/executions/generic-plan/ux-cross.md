# UX Cross-examine — one Workflow pass

Observed 2026-10-15T19:55:51Z. Frozen candidate b, supplied snapshot `dec34e19b7b3036c213299a1f98b05fec1709212fb156eabf9928682024ae2cb`. Read all five complete Analyze reports; recovered the initially truncated Architecture report in full. No implementation, new probes, peer waiting or external observations.

## Decision revision

Revise UX-D1's priority: recommend exact verifier-token rejection first, as proposed in Delivery D4 (`delivery-analysis.md:9`) and QA-D1 (`qa-analysis.md:7`). Their concrete counterexample, `--verifier=ran=skipped`, is accepted as ran despite the usage grammar. Frozen `skills/qore-review/scripts/finding-lint.mjs:6–10` independently explains this through prefix selection and split extraction. This is stronger evidence for the next bounded improvement than my unmeasured readability hypothesis. Retain UX-D2 recovery documentation; defer broader text-summary changes unless an actual consumer requirement emerges. Do not claim this grammar fix proves independent execution.

## Challenge Architecture: AR1 complexity and state ambiguity

AR1 adds a third declaration plus required nonempty `unexamined_ids` (`architecture-analysis.md:15`). Its mixed-batch use case is sourced and useful; Product PD4–PD7 correctly distinguish examined uncertainty from unexamined work (`product-analysis.md:39–42`). However, AR1's empty-partial rejection (`architecture-analysis.md:92`) conflicts with Product's explicit empty-incomplete requirement (`product-analysis.md:90`). Concrete counterexample: zero candidate findings, a verifier starts, but required phase work remains unfinished. AR1 cannot express that state as partial; telling the maintainer “skipped” misdescribes work that ran. This is a proposal-level contradiction, not a current production defect.

Architecture: either narrow the new label explicitly to partial claim examination and document the separate incomplete-phase state, or resolve zero-claim execution metadata before locking AR1. The unresolved FAIL-versus-SKIPPED mapping (`architecture-analysis.md:114`) also prevents a single clear recovery instruction. Preserve this design as a separate next increment rather than combining it with grammar hardening.

## Challenge QA: observable output

QA03/QA06 distinguish exit categories (`qa-analysis.md:19,22`); add explicit stdout/stderr expectations for both default and --json invocations. For malformed declarations: exit 2, usage on stderr, no successful result JSON. Preserve legitimate exact-token behavior, especially exit 0 with DO-NOT-SHIP: my recorded existing-fixture probe demonstrates that process success is not delivery approval. For invalid envelopes, assert refusal rather than interpreting the printed zero blocker count as reassurance (`finding-lint.mjs:43–58`).

Retain dissent: Product/Architecture prioritize a documented representational gap; my preference is the smaller measured grammar mismatch first. Unfinished: external caller compatibility, comprehension testing, and adjudication of the zero-finding partial state. No independent reproduction of peer probes was performed in this pass.
