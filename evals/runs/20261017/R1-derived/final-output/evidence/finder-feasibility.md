# Finder: performance / feasibility

Target: `/workspace/worker/target/verification-protocol.md`, against only `surface-contract.json`, `checks/check_contract.py`, and `observation-policy.json`. No network, browser, source changes, or peer reports. Method references read: `protocol.md` and `findings.md` from the supplied skill. Profile preflight result is supplied context; not independently rerun.

## Candidate findings

### F-1 — medium — Back procedure cannot establish the required sequential keyboard transition

/workspace/worker/target/verification-protocol.md:10 directs "Click Back". /workspace/worker/surface-contract.json:15 requires Back traversal="Tab", activation="Enter", and focus_after="introduction-heading"; :18 lists keyboard-back as required. /workspace/worker/checks/check_contract.py:35-36 expressly requires sequential keyboard traversal and observed activation. When a reviewer follows the written procedure, a successful click and heading-focus assertion provide no observation that Back can be reached sequentially and activated with Enter. A deployment with a working mouse Back path but a broken keyboard path can therefore satisfy all written Back assertions without supplying required keyboard-back evidence.

### F-2 — medium — Help toggle acceptance has no corresponding operation in the procedure

/workspace/worker/surface-contract.json:11-13 defines summary Enter to open, Space to close, and Enter to reopen; :18 requires help-toggle. /workspace/worker/target/verification-protocol.md:7-8 opens help using the summary and immediately uses Close; no step activates the open summary with Space or reopens via Enter. When Close works but summary Space toggling or Enter reopening fails, the written procedure can still complete without observing those declared transitions. This leaves the required help-toggle acceptance unsupported.

These are protocol evidence gaps, not claims of actual deployed website defects. They are candidates for a fresh verifier; this finder assigns no verification verdict.

## Mandatory boundary trace

Central value: the Back transition's keyboard activation requirement.

1. Producer/source: `surface-contract.json:15` writes the `back` transition as actual JSON fields `id`, `from`, `to`, `control`, `activation`, `traversal`, `focus_after`. Their actual values are `back`, `help-closed`, `returned-introduction`, `Back`, `Enter`, `Tab`, `introduction-heading`.
2. Storage / receiver: the CLI reads the actual JSON file using `json.loads(Path(...).read_text(...))` at `checks/check_contract.py:50`. `validate` consumes transition fields at :23-36. For Back it requires sequential traversal in (`Tab`, `Shift+Tab`), activation `Enter`, and `focus_after` equal to `introduction-heading`.
3. Actual serializer: `json.dumps(result, indent=2)` at :51 emits exactly `valid`, `schema`, `checks`, `limit` from :42-43. In this run, `valid=true`, schema `qaizen-labs-surface/1`, `checks` is the eight declared check names, and `limit` explicitly states consistency-only. It emits no browser event, traversal, activation, focus observation, timestamp of website behavior, or result per check. Raw stdout and exit 0 are saved in `finder-feasibility-checker-output.json`.
4. Human procedure / transformation: target :10 replaces the declared keyboard Back action with `Click Back`. It preserves the postcondition of introduction visibility and focus, but not traversal or Enter activation.
5. Final consumer / decision: a reviewer following the target can obtain mouse activation plus focus observations. That evidence cannot establish the contract's named `keyboard-back` check. No observation report serializer or actual review decision is supplied; no transmission of observations or deployment pass is inferred.

Additional mismatch: the contract's `help-toggle` requirement and summary Space / Enter transitions do not have corresponding target operations. The target opens help and then closes using Close.

## Contrary-evidence search and limits

Read all six target steps and all supplied sources. Target :8 does specify Tab/Shift+Tab then Enter for Close, so keyboard instructions exist but apply to a different control and transition. Target :10 asserts the correct heading focus, but focus after mouse activation does not show sequential reachability or Enter activation. Target :7 uses the summary but does not specify its activation and contains no Space close / Enter reopen. The checker explicitly limits its pass to consistency and does not read the target; its pass therefore does not provide missing observations. Provenance at surface :19 calls focus and transitions acceptance obligations, not current deployment results.

No runtime budget, throughput, latency, data-volume requirement, or performance measurement is supplied. Surface :20 explicitly excludes performance certification. I raise no invented performance or resource finding. The procedure is finite; the material feasibility concern is whether its operations can produce required acceptance evidence.

## Execution coverage

All four supplied raw inputs and complete target reviewed. No incomplete file coverage within this lens. Browser behavior remains intentionally unexamined; no browser was authorized in this finder brief. Findings are candidates only. No child agents spawned. Actual captured source read outputs and hashes are in `finder-feasibility-source-output.json`; checker command/stdout/stderr/exit are in `finder-feasibility-checker-output.json`.

Context: `/root/finder_feasibility`.
First execution UTC: not directly captured; first clock observation was 2026-10-17 10:16:30 UTC, after initial reads in that tool call. Parent dispatch bracket: 10:16:00–10:16:45 UTC; exact API dispatch timestamp unavailable.
Actual finish UTC: 2026-10-17T10:17:14.981265+00:00.
Usage: null — no token or aggregate agent-second accounting tool is exposed to this finder; wall-clock timestamps retained. Deadline was not exhausted.

Bookkeeping completion UTC: 2026-10-17T10:17:21.361575+00:00. Observed interval since first clock reading: 51.362 seconds; this is not CPU or total execution accounting. Token/CPU usage is unavailable, not zero.
