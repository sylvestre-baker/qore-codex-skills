# QA Cross-examine

Observed 2026-10-15T20:12:18.331135+00:00. Read all five Analyze reports and `ux-cross.md`; one challenge pass, frozen target `dec34e19b7b3036c213299a1f98b05fec1709212fb156eabf9928682024ae2cb`. Source locations below refer to `<CANDIDATE_B>`.

**Retain D4, revise QA04.** Exact verifier tokens are the smallest measured improvement: `finding-lint.mjs:6-10` truncates additional equals components; the empty-envelope counterexample emits COMPLETE/SHIP (`qa-commands.json`). Broader recovery wording is useful but lacks a comparably concrete acceptance violation. This priority follows evidence, not role agreement.

**Product challenge:** A04's “no successful review JSON” is too weak. Require entirely empty stdout plus stable usage on stderr and exit 2. A06 must include duplicate identical and conflicting declarations, missing/empty value, unknown value and unknown flag. Preserve A01–A03, exact canonical flags and argument-order behavior; no real verification is established by the flag (`finding-lint.mjs:51`).

**Architecture challenge:** AR1's rejection-before-read assertion needs an observable precedence gate. Independently confirmed UX's counterexample: malformed token plus nonexistent file currently returns exit 2, empty stdout, ENOENT; canonical token plus that file does the same. Full new argv/cwd/input state/stdout/stderr/exits are in `qa-cross-commands.json`. A test checking only exit/stdout falsely passes today. Require usage rather than ENOENT for malformed argv; correcting only the token must expose ENOENT. This tests diagnostic precedence, not a syscall-level proof of no file access.

**UX challenge:** Retain revised focused recovery scope. Use stable usage/read prefixes, not complete runtime-specific parse messages (`finding-lint.mjs:10,14`). Correcting malformed syntax must preserve the caller's truthful ran/skipped choice; recovery must never imply choosing ran to clear a gate.

**Delivery challenge:** T-D4 must retain concrete preservation evidence, not just an unused directory name. `tests/test_package.py:183-196` asserts existing build/derivative refusal and unchanged adaptation bytes; `:208-217` does the same for installation. These existing tests were included in my actual 82-test passing declared check. Implementation/release generation still needs a separate candidate and regenerated inventories; this planning run grants no installation authority.

**Profile effect:** returned `check` and `preserve-adaptations`, source `project`, digest `948b2784fa7970cf90a25c338a29067b13d8b4476f666d712a5eb95fc6f641c8`, drive the executed full-suite gate and byte-preservation acceptance. No web fact was consumed.

**Open/dissent:** Architecture's partial-batch issue (`references/findings.md:22`) remains unresolved and outside D4; grammar cannot establish execution completeness. External caller compatibility, exhaustive fuzzing, snapshot rehash, final adjudication/specification/lint remain unfinished. No verified high blocker or production harm is asserted. Cross-examination complete for this role; overall method coverage awaits lead reconciliation.
