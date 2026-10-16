# UX independent analysis — validator hardening

Observed at 2026-10-15T20:04:12.366909+00:00. Target: `<CANDIDATE_B>`, snapshot `dec34e19b7b3036c213299a1f98b05fec1709212fb156eabf9928682024ae2cb` (matches requested snapshot). Role: UX; initial Analyze only. Workflow applies because `examples/validator-hardening.md` already defines this exact scope (lines 4–8). No implementation, browser qualification, external claims, or production defect claim.

## Preflight and facts actually consumed

Read generated SKILL plus project-profile, protocol, roles, specification, and run-evidence references. Bundled checker ran before consuming project facts: exit 0, COMPLETE; profile `qore` version `0.1.0`, SHA-256 `da03026c9f73a7771cc35aaaff898a3b970fed75362ebfd0c670068d6b23b3d9`. Source ID `project`, `qore.json`, current digest `948b2784fa7970cf90a25c338a29067b13d8b4476f666d712a5eb95fc6f641c8`.

Consumed fact `check`: executed its exact argv (`python3 -B -m unittest discover -s tests -v`) at target root after inspecting temporary-file behavior; 82 tests passed. Effect: retain this command as the integration acceptance gate, add observable CLI assertions to the existing test harness instead of introducing another runner.

Consumed fact `preserve-adaptations`: effect on plan is that updated skill bundles/derivatives must go to unused staging destinations; refusal must retain existing bytes and explain selecting a new path. Do not modify generated installed copies in place. `tests/test_package.py:183–217` supplies existing preservation coverage. No mutation probe was needed. Review/UX-only facts and web fixture were not returned for plan and were not consumed.

## Recommended next safe increment

Propose D-UX1: specify recovery guidance and regression coverage for the existing findings CLI boundary, preserving its packet semantics and exit classes. Do not introduce a universal error schema or refactor all validators in this increment. Current `finding-lint.mjs:9–14,53–58` already distinguishes invocation/read failures (2), invalid envelope/content (1), and structurally valid packets (0).

Observed public CLI states (full argv/cwd/stdout/stderr/exit and exact temporary input bytes in `ux-commands.json`):

| State | Actual output | Required recovery |
|---|---|---|
| No arguments | Exit 2, usage on stderr | Supply one absolute packet and explicit verifier declaration. |
| Missing file | Exit 2, empty stdout, ENOENT on stderr | Correct path/readability; rerun unchanged validator. |
| Truncated JSON | Exit 2, empty stdout, parse diagnostic | Repair JSON; no inference of zero findings. |
| Empty object | Exit 1, JSON valid=false, PARTIAL, INVALID | Add explicit findings envelope; preserve diagnostic. |
| Explicit empty findings, verifier ran | Exit 0, COMPLETE, SHIP | Verify phase evidence separately; declaration is not proof. |
| High PLAUSIBLE, verifier skipped | Exit 0, PARTIAL, PENDING, original high retained | Run missing independent verification, retain severity, then validate new packet. |

These are actual observations, not browser evidence. Existing spec A01–A03 (`examples/validator-hardening.md:30–48`) and findings contract (`references/findings.md:22–26`) support preserving those distinctions. Proposal adds actionable stable recovery text/documentation, without interpreting missing stdout as an empty review.

## Named peer challenges

**Architecture:** Can the increment reuse current `problems` and stderr paths instead of adding adapters across every validator? Any proposed schema change must identify actual consumers; `tests/test_validators.py:15–23` currently deliberately permits absent JSON stdout.

**QA:** Add assertions for stderr channel, absence of success output, and successful rerun after correcting the same temporary file. Current truncated test (`test_validators.py:72–75`) checks exit/no JSON but not recovery. Cover valid empty and partial with explicit severity and verdict assertions, not exit 0 alone.

## Risks, triggers, limits

Changing exit classes or emitting JSON on previously empty stdout can break callers; trigger: new error serialization. Gate with unchanged-channel regression assertions and documented compatibility. Runtime parse-message wording varies; test stable prefix/action, not full Node diagnostic. Recovery wording must never recommend lowering severity or fabricating verifier execution.

Uninspected: detailed stop-rule/depth internals, downstream external consumers, localization demand, accessibility beyond plain terminal text. No loading state exists in inspected synchronous CLI. Cross-examination, adjudication, final specification/lint and full protocol coverage remain with lead; this report alone establishes no COMPLETE planning run.
