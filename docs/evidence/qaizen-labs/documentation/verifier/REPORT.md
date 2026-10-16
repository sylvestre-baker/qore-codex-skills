# Independent documentation verification

Both original filtered claims are **CONFIRMED**, severity **medium**, and their current correction is **RESOLVED** within this local public-candidate scope. They describe the same original four-link defect, not two distinct defects. `verified.json` preserves the historical verdict; `resolution.json` records the correction separately. No refutation quota was applied.

## Independence and permitted inputs

This fresh verifier used only the filtered claims, original public candidate and site-draft, corrected public candidate and site-corrected, declared local Python/Node and Playwright, and its own temporary staging/output. No private source/authentication, author reasoning, finder folders or peer reports were consulted. The recursive reference scanner necessarily parsed local reference syntax from all staged HTML/Markdown, without using those documents as review reasoning. No live website was accessed or content published.

## Original reproduction

Original `site-draft/evidence/README.md:3,20` links `../../../profiles/qaizen-labs.json`, `../../demo/qaizen-labs/README.md`, `../../showcase.md`, and `../../coordination-dependencies.md`. All four resolve beyond the staged project root; all four normalized URLs returned HTTP 404 under `/qore-codex-skills/`. `audit.json` retains exact resolved paths and URL/status measurements. The original checker returned exit 0, `valid=true`, **25 references**, **9,364,987 bytes**. This reproduces both CLAIMS-001 and A11Y-DOC-001 against original bytes, including the false-negative checker behavior.

## Current correction and refusal check

Executed from the corrected candidate:

```sh
python3 -B tools/build_site.py --output /var/folders/4r/1cnctlhj0457b5kgw29hzr4h0000gn/T/qore-doc-fresh-kabpnytk/qore-codex-skills
python3 -B tools/check_site.py /var/folders/4r/1cnctlhj0457b5kgw29hzr4h0000gn/T/qore-doc-fresh-kabpnytk/qore-codex-skills
```

Build exited 0: **240 selected files**, **15,695,781 source bytes**, `deployed=false`. Corrected checker exited 0: **88 references**, **15,783,582 staged bytes**. An independently implemented recursive HTML/Markdown reference scan found **76 local references**, **zero missing/escaping targets**; external references account for the different totals. The scanner normalized macOS `/var` to `/private/var` before containment checks; initial false positives were corrected and are not findings.

The four repaired links are `../profiles/qaizen-labs.json`, `../media/README.md`, `../reference/showcase.md`, and `../reference/coordination-dependencies.md`. Each returned HTTP **200** while served from the intended project prefix. Temporarily renaming `profiles/qaizen-labs.json` in owned staging made the checker exit **1**, reporting `Missing or escaping reference: evidence/README.md: ../profiles/qaizen-labs.json`; restoring it preserved the source candidate. This is a meaningful linked-target refusal test. Build/check commands and raw outputs are retained in `audit.json`; reproducible driver is `verify.py`.

Fresh manifest SHA-256: `17d71bdc1b8479ff8490218c087bedc90f53ed4edcaf09276d55b4711bee3544`. The supplied site-corrected snapshot shares 218/240 selected file bytes with this fresh build. This report qualifies the rebuilt corrected candidate; it does not assert byte identity of the two staged snapshots.

## Documentation and media scope

Corrected `README.md` explicitly labels 0.2.0 as a candidate in qualification, explains the public clone recipe obtains the previously published default branch until separate publication, and allows using an existing candidate checkout. The page similarly says local preparation and separate publication, and calls its repository CTA the published review example. No fresh clone or hosted default-branch version was independently tested.

All **39 command inventory entries** have matching command-text digests and matching declared implementation digests; every command text appears in its declared document. Indexed fenced blocks also match when Markdown indentation is respected. This is identity/inventory checking, not execution of all recipes. Inventory statuses distinguish actual historical execution, maintainer reports, substitutions/templates and unexecuted exact invocations. No template was promoted to current execution success.

New media provenance output digest matches the actual MP4: `988e81758ef725addf9c4da2b0b4e28f01189aaa069a28136f96af582c855973`. Public media probe declares H.264, 1280×720, **104.88 seconds**, **1,381,294 bytes**. The provenance declares a silent montage of separate executions, original-speed browser segment, source-video digest, timeline and limits. This verifier checked the public output identity, track loading and brief playback; it did not access the private source recording or independently establish every frame's correspondence to source. First-party MIT and maintainer-attested redistribution scope remain explicit, without treating the attestation as automated ownership proof.

## Browser and public observation evidence

Owned Chromium was launched using declared Playwright against the temporary loopback site. JavaScript was disabled throughout. `browser.json`, `browser-command.json`, `browser.mjs`, and screenshots retain actual observations.

- At **320px**, document scroll width was **320px**; at **1280px**, it was **1280px**. Full-page screenshots were visually inspected: responsive reading order, stacked narrow content, contained code scroll, and no visible overlapping major sections.
- Sequential Tab reached the video after the documented links. The initial Skip link had a visible **3px** outline and an on-screen bounding box. Space started playback (time advanced to **0.494664s**); second Space paused (**0.496033s**). Full native-media control and seek-key coverage were not claimed.
- The English caption track was showing with **10 loaded cues**. Brief playback worked without JavaScript. No full-length caption timing/content evaluation or human comprehension evaluation was performed.
- Reduced-motion emulation matched with **zero active animations**. This is a scoped observation, not a broad motion audit.
- After an MP4 abort route and reload, the case heading and complete-transcript link remained readable; the direct transcript loaded without JavaScript and contained **2,153 text characters**. A concrete media error event/code was not captured, so this establishes surviving text alternatives rather than complete error-state behavior.
- Public current-observations.json records actual extension `tabs.setZoom(2.0)`: outer width 1280, inner width 640, DPR 2, scroll width 640, CSS zoom 1. Its accompanying README explicitly separates historical CSS zoom from actual browser zoom and limits keyboard seeking claims. This verifier inspected those public measurements but did **not** independently rerun actual 200% browser zoom. Its `site_manifest_sha256` is null; exact current-snapshot binding is therefore incomplete. Fresh observations here are bound to this report's manifest hash.

Public render documentation distinguishes historical original-page measurements, corrected/current observations and local README preview. The original four broken links remain visible as historical evidence. README/site statements do not claim external human first-use, accessibility certification, universal compatibility, benchmark superiority or successful deployment. No subjective score or conformance result is issued here.

## Unfinished work and limits

1. Independently rerun actual 200% browser zoom on this exact fresh manifest and retain source binding.
2. Capture a confirmed video-failure error/event, test complete native media controls, and evaluate full caption/timeline correspondence if those claims are required.
3. Independently probe the actual media file with a decoder rather than relying on the public codec/duration probe and brief browser playback.
4. Investigate the 22 byte differences between supplied site-corrected and the fresh build before treating them as interchangeable publication artifacts.
5. Hosted GitHub rendering, anonymous published URLs, release/default-branch version and external human first use remain outside this local verification. No accessibility conformance or screen-reader testing was performed.

These limits do not reopen the resolved original four-link behavior. They prevent broader readiness claims. Work stopped after the bounded verifier pass; complete available artifacts were preserved.

## Source identity

- `doc-readers/claims.json`: `dce3853efabb85b08349e8fd96db4cb4a987fca3e0f5e14cd97eab4530f90397`
- `docs-build/qore-skills-0.2.0/tools/build_site.py`: `6ec74fc2b5c5a384ff1a668d1c323d38a0d95de98e16afc576aaf9f77448e14e`
- `docs-build/qore-skills-0.2.0/tools/check_site.py`: `eb11f85ae9c410a0615f2991389c4e7120ec6090147845ba1bd8be9a4af9d3a2`
- `site-draft/evidence/README.md`: `3f70dcf9ab7c0ff071b19bb0e129e9553ada15ef266b483912f0e27a4fe28b42`
- `doc-verification-build/qore-skills-0.2.0/README.md`: `5fdd44f7b53eab42ab62a72d26530bcc7935df7ce138992e4f778dd7183b0ef2`
- `doc-verification-build/qore-skills-0.2.0/tools/build_site.py`: `26d56e56b24d8b17c03d9a565e64a052e9ae3ca39d785a1813a99504ff2a85ea`
- `doc-verification-build/qore-skills-0.2.0/tools/check_site.py`: `8e681363103d163154b2a50b97b1bf0441774ab3d82eeca81622479696a5daff`
- `doc-verification-build/qore-skills-0.2.0/docs/command-inventory.json`: `d8ccdbf5a6f47000a55fdc32690e4610c78efad941010c20c33f5cd4f95b2ec9`
- `doc-verification-build/qore-skills-0.2.0/showcase/index.html`: `1154fd0d7b77da6f0a1c3ead0ef45b2e62231f9c46418273c2bf6b6d179c7337`
- `doc-verification-build/qore-skills-0.2.0/showcase/styles.css`: `1bdc47446d2b60e8d5544ea2eb3e4b666b0728263b18d6ab9bf1d2ace4d616a6`
- `doc-verification-build/qore-skills-0.2.0/docs/demo/qaizen-labs/provenance.json`: `3cd60f1a0c2764defc388958c87bb859a6bee6ea37133ece4e11e4e041d7601c`
- `doc-verification-build/qore-skills-0.2.0/docs/evidence/qaizen-labs/render/current-observations.json`: `45815eeeb2fd8e392460405a9b0f6fde8dcb7c606569e3b8b3ba72b4caa79125`
- `fresh-staging/site-manifest.json`: `17d71bdc1b8479ff8490218c087bedc90f53ed4edcaf09276d55b4711bee3544`
- `fresh-staging/evidence/README.md`: `1854eea3166b89540d8621e2822a82a8bef724a23ff75a6b9f00b1dab40a2401`
- `fresh-staging/profiles/qaizen-labs.json`: `f76afdd45cb6352e5044a06affc4182ea6cd40aa9c012fb216636a61faa428f0`
- `fresh-staging/reference/showcase.md`: `b2d702c38c1a8f408c8516be5819aadc21cad0fa00053e95bbf2f3278f14035e`
- `fresh-staging/reference/coordination-dependencies.md`: `8914f0047061092ba617d39aa50afff8b24848cf637839764c81fa18bbea4f0d`
- `fresh-staging/media/README.md`: `92d50b86967acb91d6e9dd94a98e4058b8776b2aa529ce2431cbdf3ca565e0b4`
