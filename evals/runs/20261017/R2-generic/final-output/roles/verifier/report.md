# Independent verifier report

Observed start: 2026-10-17T11:22:46Z. Allocation: 240 seconds; instructed deadline: 2026-10-17T11:26:30Z. Resource telemetry: unavailable (not zero).

## Scope and isolation

Reviewed the actual static document `/workspace/worker/target/verification-protocol.md` against the original surface contract, checker, and observation policy. The candidate input was exclusively mechanically filtered `/workspace/output/claims.json`. Read only the specifically supplied original files and method criteria, then created/read this verifier's own artifacts. No finder reports, root commentary, unfiltered candidate packet, peer artifacts, external sources, browser, network calls, or input mutations were used. No subagents were used.

All three medium IDs were examined as one bounded batch. Each received a concrete static reproduction and an evidence-backed refutation attempt. The packet preserves all original IDs and severities. Confirmation is confined to actual omissions in this document. Hypothetical deployed failures and traffic are not treated as observations.

## C-1 — CONFIRMED, medium

**Location and requirement.** Document lines 5-10 are the complete procedure; lines 7-8 open help and then use Close + Enter. Contract lines 11-13 explicitly require summary Enter, summary Space, and summary Enter in order, and line 18 requires help-toggle.

**Actual comparison.** The source has one help-opening step with no specified activation, no Space instruction, and no help reopening after closure. Close + Enter is explicitly specified, as is Back + Enter. The concrete input/output comparison and complete original steps are retained in `static-comparison.json`, with numbered original sources in `numbered-sources.txt`. This is a reproducible document coverage mismatch, not a simulation of a faulty website.

**Refutation attempted.** Close might appear to fulfill a general toggle requirement, but the contract separately names Close + Enter and summary + Space transitions. The single summary opening cannot cover a second opening after closure. The supplied checker was also tested: it returned valid=true, but reads only the contract and explicitly limits its result to contract consistency. Neither contrary check establishes coverage.

**Consequence and correction.** Completing the document cannot establish the required summary sequence. Add the specified opening activation, summary Space closure, and summary Enter reopening with the corresponding state checks before the existing Close check.

## C-2 — CONFIRMED, medium

**Location and requirement.** Contract lines 5-6 constrain origin and methods; line 18 requires origin-policy and read-only-policy checks; line 20 requires retaining effects of the expected blocked analytics POST. Observation policy lines 2-4 repeat the allowed origin. The entire target contains no network prerequisites, constraints, request observation, or relevant effects record.

**Actual comparison.** For the concrete supplied policy values, the actual procedure begins navigation and ends after its UI/focus assertions without establishing or checking either network policy or recording blocked-analytics effects. The whole-source comparison is in `static-comparison.json`; whole-word searches supplement manual reading of all ten lines. This confirms the document omission only. No actual POST, unauthorized origin, redirect, or completed browser trace was observed.

**Refutation attempted.** Opening the public entry supplies an initial destination but cannot establish policy for auxiliary requests; unanswered assertions constrain answers but do not specify allowed HTTP methods. The complete target has no prerequisite incorporating external controls. The separate observation-policy JSON declares an allowlist without making the procedure check it. The passing checker does not read the procedure. A preconfigured browser could provide controls externally, but was not observed and would not fix the missing prescribed checks/effects record.

**Consequence and correction.** The procedure cannot produce specified evidence for the required policy checks. Establish or explicitly require the origin/method controls before navigation, verify policy behavior, and retain observed blocked-request effects within the authorized scope.

## S-1 — CONFIRMED, medium; duplicate of C-2

Independently rechecked the complete target and policy requirements for this ID. The same concrete comparison and contrary explanations above apply: no policy setup/precondition, assertion, request observation, or effects record appears in the procedure, and neither the public destination nor unanswered status supplies them. This candidate's core static omission is confirmed. Its examples involving analytics or redirects remain hypothetical and are not claimed as deployment evidence. It duplicates C-2, is retained intact in the audit packet, and does not represent an additional unique defect.

## Commands, outputs, and snapshot

Executed `python3 -B /workspace/worker/checks/check_contract.py /workspace/worker/surface-contract.json`: exit 0; valid=true; required_checks echoed; explicit limit: "Contract consistency only; browser observations establish current behavior." Actual stdout, stderr, command arguments, and exit status are saved in `contract-check.json`.

Executed a local Python static document comparison, saving the exact six procedure steps, required transition objects, policy values, search results, and SHA-256 snapshot identities in `static-comparison.json`. Saved full line-numbered original inputs as `numbered-sources.txt`. A substring search initially matched HEAD inside "heading"; corrected the saved comparison to whole-word matching and independently read the full document. Final network-policy search returns no matching steps. Search absence is supporting evidence; the conclusions rest on the complete document and explicit contract obligations.

Target SHA-256: `0a3452f02e358d8800fb26d591083deb972c5531165473990dc27007a9a9e0d4`. Input hashes are retained in `static-comparison.json`.

## Coverage and limits

Confirmed: 3 IDs (2 unique issues). Plausible: 0. Refuted: 0. Confirmed critical/high blockers: 0. Requested/returned verifier roles: 1/1; no claims about the other review phases. Examined IDs: C-1, C-2, S-1. Unexamined: none. Examined-but-unresolved IDs: none. Static document verification coverage: COMPLETE for the assigned batch. Browser/deployment behavior: unobserved and outside this static task. Unfinished assigned scope: none.

Full per-ID evidence, concrete counterexamples, refutation attempts, conditions, and consequences are in `/workspace/output/verified.json`. Actual completion UTC is recorded in `coverage.json` and below after final save. Resource telemetry remains unavailable.

Observed completion: 2026-10-17T11:24:24Z. The strict envelope, preserved IDs/severity, verdicts, counterexamples, and refutation-attempt presence passed local Python assertions; the parent may run the supplied final finding linter.
