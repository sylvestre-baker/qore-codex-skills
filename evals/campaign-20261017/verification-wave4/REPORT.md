# Independent wave 4 verification

Start: 2026-10-17T11:42:57+00:00. End: 2026-10-17T11:46:34.343754+00:00. Continuous active verification wall time: **217.344 seconds**, within the 360-second cap. No intentional idle intervals. This is active elapsed wall time including local tools, not unavailable CPU/token telemetry. Charge this window to the campaign's shared verification budget; prior windows are not re-estimated here.

First intake was only `verification-wave4/claims.json`. Subsequently read the exact referenced original N01/N10 skills, full method protocol and findings contracts, redactors, raw candidate envelopes, retained filtered packets, all six complete returned finder reports, verifier reports/intake records, relevant original source/profile, actual command receipts and returned report. No first-evaluator assessment, other verification wave, author correction, comparison narrative or broad conversation was read before these verdicts. No website/model rerun, network, install, outreach, source correction or original artifact mutation occurred. New files are confined to this verification directory.

## Verdicts

**R2-C02 — CONFIRMED, medium: source-bound traversal criterion was broadened and consumed.**

The actual source hash matches the profile's bound surface source. `N01/input/surface-contract.json:15` selects the single value `back.traversal="Tab"`. The derivative's `references/project.json:45-47` instead says sequential Tab **or** Shift+Tab. `N01/output/evidence/profile-use.json:25-29` records that broader fact as a consumed review criterion, and `N01/output/REPORT.md:9,22` accepts the target's alternative traversal and reports the profile preflight complete without exposing this contradiction.

Independent reproduction extracted the exact values and verified their hashes. The attempted refutation is real but insufficient: `checks/check_contract.py:35-36` permits either value across its input domain. Running the existing validator against the original source and an in-memory-only copy changed to Shift+Tab passes both. That shows two different valid contracts; it does not change the selected source's Tab value. `references/project-profile.md:22,24,36` requires source support and exposing contradictions, and explicitly warns structural consistency cannot prove semantic support.

Concrete counterexample is the actual source-to-profile-to-consumption mapping: expected selected criterion requires the forward Tab traversal; actual consumed criterion also accepts backward Shift+Tab. A backward-only trace could meet the broader criterion without establishing the selected forward traversal. No actual browser path or deployed keyboard failure was observed. Severity stays medium; this is criterion/source fidelity, not a verified critical/high blocker.

**R2-C01 — REFUTED, medium preserved: forbidden verifier exposure is not established.**

The complete pinned method contract is read together with its actual allowlist. `SKILL.md:12-13` and `protocol.md:31,35` require the mechanical wall and exclude finder reports/reasoning; the bundled redactor at lines 13,17-19,28-34 explicitly retains scalar `id`, `title`, `severity`, `evidence`, `counterexample`. `findings.md:5` requires enough checkable source context to reproduce the claim. It does not promise removal of every explanatory or conditional sentence inside evidence.

Both retained packets contain only `id`, `title`, `severity`, `evidence`. Actual reruns of the supplied redactors reproduce their retained packets **byte-for-byte**. N01's raw `finder_report` fields are report filenames and are dropped. N10's separate `rationale`, `uncertainty`, `proposed_correction` fields are dropped. Manually compared the complete returned finder reports against retained evidence: the packets contain claim support, conditions, consequences and limits, not full returned reports repackaged into evidence. They contain no prior finder confirmation/refutation verdict. Checker `valid=true` statements are source-check results, not earlier candidate verdicts.

The actual verifier reports identify only the filtered packet and original criteria as intake (`N01/output/evidence/verifier-report.md:3,17`; `N10/output/roles/verifier/report.md:7`; N10 isolation record lines 15-24). N01's verifier audit records the retained packet's digest. These records corroborate the mechanical result. They do not provide omniscient proof of an inaccessible/unrecorded context. No prohibited full-report, separate rationale-field or earlier-verdict exposure is reproduced on the referenced evidence. Claim context inside the explicitly permitted evidence field alone cannot establish the alleged failure.

## Coverage implication, criterion quality and activity inventory

- **This diagnostic:** both supplied IDs examined with reproductions and refutation attempts; no unexamined/unfinished IDs. One CONFIRMED, zero PLAUSIBLE, one REFUTED. Original medium severities preserved. No confirmed critical/high blocker.
- **Original N01 full-method coverage:** **affected PARTIAL** for profile-backed source fidelity. The source contradiction was consumed without being exposed, so an unqualified full-method COMPLETE conclusion is unsupported for that affected obligation. This is separate from the original report's narrower claim that the named document-review phases ran.
- **Original N10:** R2-C01 supplies no basis to downgrade its bounded COMPLETE claim. COMPLETE remains supported against this tested exposure challenge; this two-candidate diagnostic does not independently certify every other method criterion or deployment property.
- **Criterion quality:** N01's broadened traversal fact is a demonstrated medium source-fidelity defect. No semantic-blinding defect is demonstrated for the R2 filter under the pinned full method plus explicit field allowlist. Both points concern the specified diagnostic, not a claim of general method fitness.
- **Narrower activity inventory:** retained reports and receipts still support three returned finder roles, mechanical redaction, a returned fresh verifier report and findings validation for the original runs. The profile mismatch does not erase those observed activities. A phase inventory alone cannot establish correct source fidelity or full-method completion.

## Read-only checks and final gate

`python3 -B verification-wave4/read-only-checks.py` exited 0. It ran both original redactors, compared actual output bytes and field sets, compared complete-report containment, hashed bound sources, extracted actual consumption, and executed the original local contract validator for the selected and alternate in-memory contracts. Results are in `read-only-checks.json`. Mechanical containment is supplementary; the rationale verdict rests on manual reading of the full reports and allowed packet content.

Actually ran the existing pinned `N01/input/.agents/skills/qore-review-qaizen-labs/scripts/finding-lint.mjs` with the absolute `verification-wave4/verified.json` path and `--verifier=ran --json`. Exit **0**, valid=true, counts **1 CONFIRMED / 0 PLAUSIBLE / 1 REFUTED**, no blocking findings or structural problems. Exact argv, times, stdout and stderr are retained in `finding-lint.json`. Its COMPLETE/SHIP labels are mechanical packet gate outputs, not a requalification of original N01 coverage or a delivery decision. The REFUTED record retains `refuted_because` as required by the pinned findings contract.

`timing-and-integrity.json` records this active window and confirms all original input hashes recorded by the read-only checks still match. No original corrections were applied. Verification stops after these deliverables.
