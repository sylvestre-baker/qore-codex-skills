# Focused independent documentation supplement

The five requested local completion checks are now observed or checked. **No required work remains unfinished within this focused supplement.** Original `REPORT.md`, `verified.json` and `resolution.json` are preserved. The original two medium findings remain CONFIRMED and their shared staged-link correction remains RESOLVED; this supplement makes no broader release/readiness, conformance or human-testing claim.

## Fresh build and identity

Built the same corrected public candidate into new owned staging `/private/var/folders/4r/1cnctlhj0457b5kgw29hzr4h0000gn/T/qore-doc-supplement-eivt1y_e/qore-codex-skills`, then ran its checker. Both commands exited 0: build selected 240 files and 15,695,781 bytes; checker examined 88 references and 15,783,582 staged bytes. Manifest SHA-256 is `17d71bdc1b8479ff8490218c087bedc90f53ed4edcaf09276d55b4711bee3544`, identical to the preceding verifier's fresh manifest. `SUPPLEMENT.json` retains commands, stdout/stderr, content hashes and raw results; `supplement.py` and `supplement-browser.mjs` reproduce the checks.

## Real 200% browser zoom

Followed the official [Playwright Chromium extension procedure](https://playwright.dev/docs/chrome-extensions): bundled Chromium, isolated temporary persistent context, temporary MV3 extension, and `viewport:null`. The extension invoked `chrome.tabs.setZoom(tab.id, 2)`; `getZoom` returned **2**.

| Measurement | Before | After |
|---|---:|---:|
| Outer window width | 1280 | 1280 |
| CSS inner viewport width | 1280 | 640 |
| Document scroll width | 1280 | 640 |
| Device pixel ratio | 1 | 2 |
| Root CSS zoom | 1 | 1 |

This is actual browser zoom with a changed CSS viewport, rather than CSS zoom or viewport-size substitution. The heading's right edge was 622.40625 within the 640px CSS viewport. The current browser surface screenshot `supplement-actual-zoom-viewport.png` was visually inspected and shows the reflowed header and enlarged hero without horizontal clipping in that viewport. Playwright's separate full-page screenshot at non-default zoom clipped its capture; it is retained as a capture limitation, not treated as a page defect or full-page visual pass. The CDP current-surface screenshot and measured layout are the zoom evidence.

## Confirmed failed media with surviving alternatives

In owned staging, fulfilled the MP4 request with an intentional HTTP **404**. Two observed responses had status 404; captured `SOURCE` **error** events name the exact MP4 URL. The video reached `networkState=3` (no available source), `readyState=0`. The case heading and complete-transcript link remained present and readable. Following that link loaded the transcript page with **2,153 characters** and its expected title. The screenshot `supplement-confirmed-video-404.png` was visually inspected: ordinary case/evidence text and transcript access remain available despite absent playback. This closes the earlier uncertainty about whether an actual failed source had occurred.

## Actual media probe, decode and captions

Executed `/opt/homebrew/bin/ffprobe -v error -show_format -show_streams -of json <fresh media/demo.mp4>`: exit 0, one **H.264 video stream**, **1280×720**, **104.88 seconds**, **2,622 frames**, **1,381,294 bytes**; there is no audio stream, consistent with the silent-video description.

Executed `/opt/homebrew/bin/ffmpeg -nostdin -v error -i <fresh media/demo.mp4> -f null -`: exit **0**, empty stderr after full decoding. This independently checks decodability rather than relying on the supplied probe JSON.

Parsed all **10 caption cues**: every cue has a positive in-range duration, boundaries are contiguous, coverage begins at 0 and ends at **104.88**, matching the actual probed duration. Cues 1–5 and 10 align with the public transcript/provenance timeline boundaries. Cues 6–9 consistently subdivide the declared 56–96.88 browser segment. Every cue's content was compared directly with the supplied public transcript and provenance: separate-run montage, derivatives, five planning perspectives, three finders/fresh verifier/four defects, manual coordination with work already in progress, keyboard help/Close/Back/unanswered state, and final narrow desktop scope are consistent. No contradiction was found in these supplied public sources. Private raw-video correspondence and human caption comprehension remain untested and unclaimed.

## Explanation of the 22 snapshot differences

All **22** previously unmatched files are **new additions under `evidence/render/`**. There are **zero changed existing files**, **zero files removed from the fresh build**, and **219 existing identical files including `.nojekyll`** (218 selected source files plus `.nojekyll`). Existing entry HTML, stylesheet, link-rebased evidence index, media and transcript bytes match the supplied site-corrected snapshot. The generated manifest changes because it inventories the added render evidence. Thus actual existing source/render/media bytes did not change; evidence files were added.

- `evidence/render/README.md` (1537 bytes; SHA-256 `9e4fdeb39b7fc2c4590dad3ae3f1be1aad2b7f3862d69c257d9fde652ff5cae4`)
- `evidence/render/current-actual-browser-zoom-200.png` (436783 bytes; SHA-256 `4c60921e0ac2ed27d081cb36a364e95ea7d294ba3136a9ecd477a717bc0cd675`)
- `evidence/render/current-keyboard-video.png` (156267 bytes; SHA-256 `8eda37ac81c8494de03bc0d80e21ca65e6ec551068c409d9e6bd97979dfcf1f7`)
- `evidence/render/current-observations.json` (2335 bytes; SHA-256 `45815eeeb2fd8e392460405a9b0f6fde8dcb7c606569e3b8b3ba72b4caa79125`)
- `evidence/render/current-video-unavailable.png` (639853 bytes; SHA-256 `1c83e2e0ebdffc970c5bf5fb1741400f8265d5389251a10a744d57807e30c218`)
- `evidence/render/inventory.json` (3070 bytes; SHA-256 `40ccfdfef2f964985acc49764ad71710aa8f85bfa625cf4a3fdedca6f07717f4`)
- `evidence/render/reader-desktop-1280.png` (653761 bytes; SHA-256 `46bb73e21d32ba3ba98357e05e91fd879fb0adba331d955e7f66c714f09d3673`)
- `evidence/render/reader-followup-observations.json` (5231 bytes; SHA-256 `22b6399588f38b97c742dc6c38128a504434ab28a3c38b909d5da0d217de72f3`)
- `evidence/render/reader-narrow-320.png` (512810 bytes; SHA-256 `4bcd07d1a2b91e37381490bf2314f0c9f69d8ebed89fe79c6c155fa7e7093027`)
- `evidence/render/reader-no-javascript.png` (654148 bytes; SHA-256 `87086f1f2f34cb1de4aaada80ef49f74a355b1b20faf746b2827c9e6945538e5`)
- `evidence/render/reader-observations.json` (10589 bytes; SHA-256 `b0a4ff0f166ae52676440eafad80e2629b77f57757f492c75d5c58ae507b9871`)
- `evidence/render/reader-transcript.png` (238413 bytes; SHA-256 `5f941c56f7eaee5350e4e0d9cb62c98e8095630c40d8edc65fafb413c57389ba`)
- `evidence/render/reader-video-playing-captions.png` (124312 bytes; SHA-256 `8a074c2505dcca7570b6bfbb5e945fe7d0284d8a0898017433929bfcae0bcdc4`)
- `evidence/render/readme-caption-playback.png` (113040 bytes; SHA-256 `bc083dab2b675a75e183e0df2c0c3602558f557b96833fd6c9d7296a446b6354`)
- `evidence/render/readme-narrow-entry.png` (90879 bytes; SHA-256 `aa1d39eb805d6eaa50db0260da3a1396c98de9d990423146ad516935a5c2c3e1`)
- `evidence/render/readme-narrow-evidence.png` (89676 bytes; SHA-256 `b04ff17dea5b8f37fb79b82a4431e4e6848a0526f1cece328b50f199bb1b0fd7`)
- `evidence/render/readme-narrow.png` (1018475 bytes; SHA-256 `d44b9234317562e6c91229a68693d78190dd4a3c69bc318dc9d799faa511068c`)
- `evidence/render/readme-observations.json` (11802 bytes; SHA-256 `628ac57bb6e203094bb16930ceef18c733b1b607ccd97349a89d4a0d2327b230`)
- `evidence/render/readme-playback.json` (248 bytes; SHA-256 `62fe2176e29966d6ff439d905f360120b77281819e915f5d2cd5052148828042`)
- `evidence/render/readme-wide-entry.png` (216305 bytes; SHA-256 `e04c1c01c0a30a6b6288c5f5bc9f7df7ef44e7eb773f44e0227524a443ab9bb9`)
- `evidence/render/readme-wide-evidence.png` (220750 bytes; SHA-256 `d95423bf5648395714d9c5ebfac10a1136b3a667c3b66b14e858e051aee185b2`)
- `evidence/render/readme-wide.png` (1202957 bytes; SHA-256 `416e1f9225ae212c42a6021c019c74d167445a1d0537e248d5ea740fb96401c9`)

## Scope retained

No new complete-native-controls requirement was introduced. Sequential video reachability and Space play/pause were already measured in the preceding pass; seeking/full control coverage remains unsupported and unclaimed. This supplement uses local staged files, fresh browser state and public documentation only. It does not inspect private source recordings, author profiles, authentication, finder reasoning or peer reports; it does not publish or access a live product service. The owned browser context and HTTP server were closed.

Hosted publication/default-branch checks, external human first use and accessibility conformance remain outside this local verification. Those are retained boundaries, not newly unresolved requirements of this focused pass.

## Bound page/media identities

- `site-manifest.json`: `17d71bdc1b8479ff8490218c087bedc90f53ed4edcaf09276d55b4711bee3544`
- `index.html`: `1154fd0d7b77da6f0a1c3ead0ef45b2e62231f9c46418273c2bf6b6d179c7337`
- `styles.css`: `1bdc47446d2b60e8d5544ea2eb3e4b666b0728263b18d6ab9bf1d2ace4d616a6`
- `media/demo.mp4`: `988e81758ef725addf9c4da2b0b4e28f01189aaa069a28136f96af582c855973`
- `media/demo.en.vtt`: `2483382e483d1d455aa8cac831e00ba72d03e6e94056fd5f82d4509201c753b8`
- `media/poster.jpg`: `f961fd834dff3425a328c33c57fb68491d5a8e3c38bbb9bc77690cc924fee9fc`
- `media/transcript.html`: `4433ad0b3a4fb9c65970ad3089f2b9e783936ece83eaf0dd62a025f0ce1f7a3f`
- `media/transcript.md`: `c3b42901855bb2a04760a215a007946ead768a5f13d5924c04686db130e748e4`
- `media/provenance.json`: `3cd60f1a0c2764defc388958c87bb859a6bee6ea37133ece4e11e4e041d7601c`
- `evidence/README.md`: `1854eea3166b89540d8621e2822a82a8bef724a23ff75a6b9f00b1dab40a2401`
