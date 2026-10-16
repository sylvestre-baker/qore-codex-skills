# Case: reject a malformed verifier declaration

A real Qore self-application exposed an input boundary the original tutorial acceptance cases did not cover. An empty findings packet passed with the malformed option `--verifier=ran=skipped`: the parser discarded the suffix and interpreted it as `ran`, producing structural COMPLETE/SHIP. Those tokens were never proof that a verifier had actually run.

The [recorded before/after probe](../demo/verifier-flag-probe.json) preserves the explicit input, both helper source digests, real stdout/stderr, exit statuses and observation time. Its source snapshots are retained beside it for independent reproduction. No defect was inserted for the demonstration.

## From problem to decision

The five planning perspectives independently examined the existing validator-hardening specification and implementation. Delivery reproduced the malformed option. Product, Architecture and UX also proposed partial-batch verification support and clearer human output. Cross-examination selected the smaller prerequisite: require the entire raw verifier value to match the documented grammar. The broader features remained deferred, with their dissent retained.

The implementation now validates the complete suffix rather than splitting at the next equals sign. `ran` and `skipped` retain their existing behavior; malformed suffixes are refused with exit 2 and usage text. A regression exercises `ran=skipped`, `ran=`, `skipped=ran` and `unknown`.

The supported decision is to retain this exact-token guard and its regression before considering a broader verification-state interface. This one case does not establish general planning quality, speed, cost or superiority.

## What the earlier review established

The earlier independent review completed its three finder phases, real mechanical filtering and a fresh verifier with zero candidates. It exercised the tutorial's A01–A03: malformed envelopes, preserved unverified severity, and an explicit empty review. It did not find the malformed-option counterexample later observed during planning. [Original review evidence](executions/generic-review/report.md) retains its own candidate and target identities.

A completed protocol can miss a defect. A passing linter and a zero-finding review cannot establish defect absence. The later counterexample remains visible rather than being erased from the story.

## Evidence boundaries

The before/after replay identifies two exact helper snapshots. It is separate from both planning and review executions, with its own time and artifacts. Original candidate identities are not relabelled as the final release. Public presentation uses selected public inputs and recorded transformations; raw private traces are not automatically exported.

The real [web observations](executions/generic-ux/README.md) and [profile route contrasts](executions/derived-ux/README.md) demonstrate different method consumers. They do not prove this parser change, and this parser replay does not replace their browser evidence.
