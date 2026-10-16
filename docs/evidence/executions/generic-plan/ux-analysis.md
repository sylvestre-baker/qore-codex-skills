# UX independent analysis — validator hardening

Observed: 2026-10-15T19:49:45Z; diagnostic capture timestamp is retained in ux-commands.json. Target: frozen snapshot `dec34e19b7b3036c213299a1f98b05fec1709212fb156eabf9928682024ae2cb`, `<CANDIDATE_B>`. Existing `examples/validator-hardening.md:1–70` selects Workflow. This is the initial independent Analyze report; no peer conclusions were supplied. No implementation or browser/native qualification was performed.

## Evidence and current interaction

All citations below are relative to the frozen root. Read: the example; qore-plan SKILL.md and protocol/roles/specification references; finding-lint.mjs; findings.md; redact-for-verifier.mjs; tests/test_validators.py. No evaluation report or project-profile facts were read.

The maintainer enters through one packet path plus a required verifier declaration. Bad usage and unreadable/unparseable JSON terminate with exit 2 and stderr; semantic invalidity returns exit 1; structurally valid packets return exit 0 even for DO-NOT-SHIP (`skills/qore-review/scripts/finding-lint.mjs:4–14,43–58`). Thus process success and review readiness are distinct observable states.

JSON contains preserved findings, counts, coverage, verdict, problems and an explicit execution-declaration limitation (`finding-lint.mjs:46–52`). Plain text prints validity, coverage, verdict and blocker count, but omits that limitation and plausible/refuted counts (`finding-lint.mjs:53–56`). An invalid envelope visibly prints “0 blocking findings”; this is derived after validity fails, not evidence that zero defects were established (`finding-lint.mjs:18–19,43–55`). Existing tests exercise JSON through their helper, including truncated input, explicit empty reviews and skipped verification (`tests/test_validators.py:15–26,64–104`).

Three actual CLI probes, including their argv/cwd/exit/stdout/stderr, are saved in ux-commands.json. The invalid envelope prints refusal plus zero blockers; malformed JSON with --json produces no JSON; a confirmed blocker produces exit 0 and DO-NOT-SHIP. These observations confirm current branches, not user misunderstanding.

## Proposed decisions and deliverables

**UX-D1 (proposed):** Make the next increment a bounded plain-text reporting clarification. Retain the existing validity, coverage, verdict, severity and exit semantics; append the existing limitation text and plausible/refuted totals. Label blockers as verified blockers and avoid displaying a numeric blocker assurance for an invalid packet. The original goal expressly distinguishes malformed, complete and verification-missing results (`examples/validator-hardening.md:6–16`); existing reporting guidance already separates execution coverage from delivery decisions (`skills/qore-review/references/findings.md:22–28`). This is a content proposal, not a demonstrated behavioral defect.

**UX-D2 (proposed):** Document recovery alongside the CLI contract: exit 2 → repair invocation/path/JSON; exit 1 → repair the identified packet fields; valid PARTIAL → retain impact and obtain missing independent evidence; valid empty → inspect actual phase evidence. Preserve A01–A03, especially the prohibition on treating a declaration as proof (`examples/validator-hardening.md:30–48`). Do not prescribe changing skipped to ran as a repair.

Deliverables: one CLI state table with stdout/stderr/exit expectations, concise text examples, and public-entry regression coverage. No dashboard, new persistence or phase registry is required for this increment. Text must remain readable without color; identifiers and problem wording must survive piping. Localization is unrequested and remains out of scope.

## Triggered risks, peer questions and acceptance

**Architecture:** Can the existing `result` object drive text formatting without adding a second verdict computation? A duplicated state machine would risk divergence from JSON; this is a hypothesis triggered only by a separate renderer calculation. Is changing a current text line compatible with any actual consumers? Inspect callers before locking exact wording.

**QA and security:** Please cover observable text and JSON together: invalid envelope, parse failure, skipped high PLAUSIBLE, confirmed high blocker, and explicit empty ran/skipped. Assert exit code separately from verdict and retain stderr. Existing review tests mostly assert JSON properties; they do not establish text readability (`tests/test_validators.py:53–113`). For valid partial states, verify unchanged severity and no SHIP. For empty complete states, require the limitation in text without claiming the linter proves phase completion.

**Product/Delivery:** Is reporting clarity the smallest accepted improvement, or is machine-readable invocation-error parity required? The latter changes the error contract and should be separately adjudicated.

Unfinished: actual downstream text consumers, user comprehension, full project check, redactor recovery interaction, and cross-examination. Resolve through caller search, QA matrix and peer reports before lead adjudication. No claim of complete Workflow coverage or implementation readiness is made.
