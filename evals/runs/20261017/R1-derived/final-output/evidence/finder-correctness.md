# Correctness finder report

Context: /root/finder_correctness.
First execution observed UTC: 2026-10-17 10:16:15 UTC; first source-read call preceded this clock measurement in the same exec.
Completion UTC: 2026-10-17 10:17:42 UTC.
Observed duration from first clock measurement: 87.087 seconds.
Parent dispatch timestamp unavailable; parent reports dispatch in 10:16:00–10:16:45 UTC.
Token/CPU usage: null (not exposed by host).

Reviewed only target/verification-protocol.md against surface-contract.json, checks/check_contract.py and observation-policy.json, plus permitted method references. No network, peer reports, shared-data mutations or child agents. The source snapshots and actual source byte hashes are retained in finder-correctness-source-audit.json. Parent supplied profile preflight: qaizen-labs 0.1.0, f76afdd45cb6352e5044a06affc4182ea6cd40aa9c012fb216636a61faa428f0.

## Findings

### C-1: Clicking Back does not exercise the required keyboard transition (medium)

Target target/verification-protocol.md:10 directs “Click Back” followed by content and heading-focus assertions. Source surface-contract.json:15 requires Back traversal with Tab and activation with Enter; :18 requires keyboard-back. checks/check_contract.py:35-36 explicitly requires sequential keyboard traversal and Enter. Trigger: Back works on click and places focus correctly but cannot be reached with Tab or activated with Enter. The target can pass all its assertions without encountering either keyboard failure, leaving keyboard-back unverified.

### C-2: The procedure omits the required help toggle and reopen sequence (medium)

Target target/verification-protocol.md:7-8 opens help once with summary and immediately closes it through Close. Source surface-contract.json:11-14 separately specifies summary Enter to open, summary Space to toggle closed, summary Enter to reopen, and Close Enter to close; :18 requires help-toggle. No target instruction exercises Space on summary or the help-closed to help-open transition. Trigger: initial opening and Close work but Space toggling or reopening fails. The prescribed run still completes, leaving required help-toggle behavior unverified.

### C-3: The browser procedure starts without establishing required request restrictions (medium)

Target target/verification-protocol.md:5 starts by opening the public page; the entire procedure (:5-10) contains no request interception, method allowlist, origin validation, or blocked-request observation. Source surface-contract.json:6 allows only GET/HEAD/OPTIONS; :18 requires read-only-policy and origin-policy; :20 says an analytics POST is expected to be blocked and its effects retained. observation-policy.json:2-4 allows only https://qaizen.io. checks/check_contract.py:2,42-43 says it never contacts the site and proves only consistency. Trigger: the page emits the anticipated analytics POST in a browser without a preinstalled restriction. The target supplies no step to block it or retain its observed effects, so the run cannot establish required policy compliance.

These are finder candidates without independent verification verdicts. They identify what the procedure cannot establish, not live website defects.

## Mandatory boundary trace

Central value: the Back transition's keyboard activation requirement.

Source → storage: surface-contract.json:15 actually stores id=back, from=help-closed, to=returned-introduction, control=Back, activation=Enter, traversal=Tab, focus_after=introduction-heading. The focus target resolves through :17 to h1. Required_checks at :18 separately stores keyboard-back and introduction-focus; focus does not subsume keyboard reachability or activation.

Storage → actual serializer: checks/check_contract.py:23-31 reads transition id/from/to/control/activation/focus_after. Lines 32-36 read Back traversal/activation and Close/Back focus destinations. Lines 42-43 return exactly valid, schema, checks, limit; line 51 serializes them with json.dumps. The actually observed successful CLI stdout retained in finder-correctness-source-audit.json contains precisely those four fields. It emits no executed browser events, focus measurements or request restrictions. Its limit explicitly says browser observations establish current behavior.

Source → transformation → claim → decision: target line 10 transforms the Back requirement into click plus visibility, absence and heading-focus assertions. It retains the final state/focus assertions, replaces Enter with click, and drops traversal. A user can decide those assertions pass without obtaining evidence of keyboard-back. The target is a manual procedure, not a programmatic receiver of the checker JSON; no transmission from checker output into the document is inferred.

Adjacent help boundary: the source emits separate initial Enter/open, Space/close, Enter/reopen, and Close/Enter events. Target lines 7-8 prescribe an unspecified summary open followed by Close/Enter. The middle events have no prescribed action; C-2 identifies the resulting coverage gap.

Policy boundary: the source stores allowed_methods=[GET, HEAD, OPTIONS], allowed_origins=[https://qaizen.io], plus expected analytics POST blocking with effects retained. The target specifies navigation without a restriction setup or policy observation. C-3 is conditional on the anticipated request being emitted; no network behavior was measured.

The whole target and supplied sources were searched for contrary evidence. The target does require Close keyboard traversal/Enter and returned heading focus for Back, but neither addresses Back keyboard activation. The target does retain unanswered-state checks and accurately identifies itself as a reconstructed fixture; neither was reported as defective. No supplied source states that the browser already has a blocker installed. Exact fallback search and its matches are retained in finder-correctness-contrary-search.json.

## Commands and outcomes

Initial cat of target and three raw sources: exit 0. Cat of permitted protocol/findings references plus nl -ba of raw sources: exit 0. Raw source contents are preserved as numbered text in finder-correctness-source-audit.json.

Python source-audit creation: exit 0. Its actual subprocess command was `python3 -B /workspace/worker/checks/check_contract.py /workspace/worker/surface-contract.json`; subprocess exit 0, complete stdout/stderr saved in finder-correctness-source-audit.json. This establishes consistency only.

Attempted rg search/report generation: exit 1, FileNotFoundError for rg; no candidate/report files were written by that failed command. The failure and requested pattern are recorded in finder-correctness-contrary-search.json. Current recovery uses Python re.search over every line of all four files; successful search result is saved there. Report and envelope writing occurs in this recovery command.

Reproduction limits: local exact-source comparison only; no live browser or synthetic website was run. Trigger scenarios show observations that the prescribed procedure cannot distinguish, and are not attributed to the deployment.

## Coverage

All six target steps and all supplied source files were examined for requirements, ordering, preconditions, failure paths, focus destinations and observation restrictions. Incomplete target coverage: none. Live deployment behavior, browser traces, mobile, complete questionnaire and accessibility certification are outside scope. No independent verifier ran in this worker.

Saved complete report: /workspace/output/evidence/finder-correctness.md. Strict candidate envelope: /workspace/output/evidence/finder-correctness.json. Evidence: finder-correctness-source-audit.json and finder-correctness-contrary-search.json in the same directory.
