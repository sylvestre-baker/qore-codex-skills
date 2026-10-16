# Fresh skeptical newcomer README challenge — QORE-002

Result: no concrete reader failure reproduced in the tested local setup path. The strict packet is `findings.json` with an explicit empty findings array. This is a bounded agent walkthrough, not an independent human usability trial, a completed Qore review, or a readiness certification.

## Scope and independence

Read only the supplied public candidate at `docs-build/qore-skills-0.2.0` and the supplied sibling `site-draft`. No author chat, private reports, personal skill instructions, credentials, peer outputs, external website, or live site was read. No subagents or model calls were launched. No candidate content was changed and nothing was published. The initially assumed `docs-build/site-draft` path did not exist; the authorized sibling was at the task root `site-draft`. This was task-location recovery, not a documented product defect.

The complete candidate file SHA-256 inventory is `source-hashes.json`; the staged showcase inventory is `showcase-source-hashes.json`. Exact subprocess argument vectors, working directories, exit codes, stdout, stderr and elapsed times are in `commands.json`. The private staging path is recorded there. Copies and generated artifacts remain in that unused staging area for reproduction.

## First-time maintainer route

README.md:5 identifies developers and maintainers already using Codex on an existing project. README.md:17–23 lets me select by task and target, rather than requiring a three-method pipeline. As a maintainer challenging a specification I selected qore-review, not planning or rendered web inspection. README.md:25–29 then provides a concrete bundled validator-hardening target, states the independent-subagent and shell/runtime prerequisites, and allows a legitimate zero-finding outcome. I used the supplied candidate as the existing checkout, as permitted at README.md:31; cloning was neither necessary nor attempted.

I followed README.md:38–46 in a private copy: build a new candidate and install its three generic skills. The build returned valid=true, version 0.2.0, 1205 files. Installation returned all three `.agents/skills/` paths and replaced=false. Repeating installation returned exit 1 and the documented existing-destination refusal. I followed README.md:89–96 with a fresh staging substitution for the example output: derive the Qore profile and verify it. Both returned exit 0 and valid=true, kind=derived, 39 files. There was no need for a persistent profile for the first generic review; the adaptation section explained why one might be useful later.

I read the bundled target and its stated local check (examples/validator-hardening.md:68–70 and qore.json). Running `python3 -B -m unittest discover -s tests -v` returned exit 0: 154 tests ran in 4.391 seconds, 11 browser-dependent tests skipped. Those skips are explicit unavailable optional browser coverage; they are not passes. The review context preview returned matching qore.json digests, no problems and COMPLETE context coverage. As docs/profiles.md:31 explains, that means current context, not completed method execution.

## Activation boundary

README.md:48–57 instructs a new Codex chat and supplies the actual activation prompt, then names the three returned finder reports, mechanical redaction, separate verifier and phase evidence required for completion. README.md:29,57 and skills/qore-review/SKILL.md:11–15 explicitly prevent treating successful installation, valid JSON or a lead self-check as a complete review. This task forbade model calls: I did not open that new chat, test automatic discovery, execute the three finders, perform the fresh verifier phase, or claim COMPLETE review coverage. Local setup and derivation succeeded; review activation and independent phases remain UNEXECUTED in this walkthrough. The README provides the next action without representing it as already completed.

## Showcase cross-check

Read `site-draft/index.html` and the candidate's showcase instructions. The staged page states candidate/local-preparation/publication limits and discloses that no external human first-use trial was observed. Its selected case distinguishes a protocol keyboard-verification gap from an asserted website bug. The local checker returned valid=true, 25 references, 9,364,987 bytes. I also executed the showcase's Qaizen Labs derivation and verification commands with a fresh output substitution; both succeeded. This confirms only local command viability and static closure. I did not render layouts, play media, assess captions, navigate external GitHub links, verify an anonymous published release, or inspect a live web flow.

## Findings and limits

Findings: none established with a reproducible reader failure in the stated scope. There is no severity or minimal-remedy entry to invent for an unreproduced issue. Successful local setup is narrower than review activation and much narrower than human testing. The bounded time budget did not include an exhaustive documentation audit or platform portability matrix. A later first-use activation trial should use a clean Codex chat with only these installed candidate skills and retain actual discovery, worker, redaction and verifier evidence. An external human trial remains separate.
