# QORE-002 public documentation accessibility reader

Scope: fresh bounded technical read of the public candidate `docs-build/qore-skills-0.2.0` and sibling `site-draft`, on 16 October 2026. No live website, authenticated service, private author materials, peer reports, source changes or subagents were used. This is an automated browser observation with visual inspection of screenshots, not accessibility-conformance certification or a human usability trial.

## Result

One medium documentation finding, A11Y-DOC-001, is recorded in `findings.json`: the showcase evidence index retains four relative links that resolve outside the project prefix and return HTTP 404. The eleven links directly on the HTML showcase return HTTP 200. All 42 local README link occurrences have corresponding candidate files (fragment anchors were not checked).

## Actual observations

The reader started its own temporary loopback static server, mounting only `site-draft` at `/qore-codex-skills/`, and used the documented Node and Playwright facilities. Both browser sessions and servers were closed by `finally` blocks. Test code and raw values are retained in `check.mjs`, `followup.mjs`, `observations.json` and `followup-observations.json`.

- **1280 × 900:** document scrollWidth 1280. The visual review of `desktop-1280.png` showed readable hierarchy, three columns, clear links, no apparent collision and evidence/limits outside the video.
- **320 × 800:** document scrollWidth 320. `narrow-320.png` showed the columns stacked and readable text. The command block intentionally scrolls internally: clientWidth 285, scrollWidth 393. Chromium sequential Tab reached PRE, which had a native visible outline; ArrowRight changed scrollLeft from 0 to 40. The full command was selectable with its line breaks and backslashes retained. The `narrow-pre-keyboard.png` capture was taken during smooth scrolling and does not visually establish the PRE focus state; the raw DOM/keyboard measurements do.
- **Keyboard/focus:** first nine sequential targets had the configured 3px brown outline. `keyboard-first-focus.png` records the first skip-link focus. Activating Skip to content moved sequential navigation past the header to the hero CTA; document.activeElement remained BODY after fragment activation, so this does not establish screen-reader focus. A subsequent 40-Tab traversal reached native video controls, transcript/download links, the scrollable code block and the final CTAs without an observed keyboard trap.
- **200% approximation:** `css-zoom-200-approximation.png` was captured after applying CSS `zoom:2` at a 1280px viewport; document scrollWidth remained 1280, and the visual image had no apparent lost text. This is explicitly **not real browser zoom**; media-query behavior can differ (the three-column cards remained three columns). Real 200% browser-zoom verification remains unfinished.
- **Reduced motion:** emulating `prefers-reduced-motion: reduce` produced a matching media query and computed `scroll-behavior:auto`. No scripted animation or autoplay is present.
- **No JavaScript/video dependence:** a JavaScript-disabled browser rendered the H1 and 4,676 body-text characters, with the transcript link present (`no-javascript.png`). A separate browser blocked the MP4 request; the caption, transcript/download links and full case text remained present (`failed-video.png`). The script did not await an explicit terminal media error, so it demonstrates a blocked video request with readable alternatives, not a fully adjudicated browser error-state UI.
- **Media:** metadata reported 104.88 seconds. Programmatic play advanced to 0.352s, then pause succeeded. The English captions track was showing, with ten cues and one active cue; `video-playing-captions.png` visibly shows the first cue. The HTML transcript returned HTTP 200 and has a title, H1 and seven timed sections (`transcript.png`). Caption source timings cover 0:00–1:44.88. Complete video-frame/caption accuracy and keyboard playback operation were not verified.
- **English copy/source linkage:** the README, showcase, transcript, captions, showcase preparation instructions and public evidence index were read. The copy clearly identifies candidate status, the protocol gap versus website behavior, assembled separate executions and the limits of evidence. No additional material copy defect was established. Repository links were not opened externally.

## Finding detail

**A11Y-DOC-001 — Medium — staged evidence navigation escapes the project prefix.** `site-draft/evidence/README.md:3` references `../../../profiles/qaizen-labs.json`; line 20 references `../../demo/qaizen-labs/README.md`, `../../showcase.md`, and `../../coordination-dependencies.md`. From the staged evidence URL, all four resolve at the server root outside `/qore-codex-skills/` and return 404. A reader following the case index cannot reach its maintained profile, demo explanation, preparation guide or dependency limits through these references. This is a source-link failure in a linked Markdown document; the local server served Markdown as plain text, so no clickable Markdown renderer behavior is claimed. Rewrite staged links to valid in-prefix files, copy their selected public targets, or use exact public repository URLs for the candidate identity, then check links recursively from linked Markdown as well as HTML.

## Unfinished required observations and limits

Real browser 200% zoom remains unobserved. Native video controls were reached by keyboard, but keyboard play/pause/caption-toggle behavior was not exercised. A blocked-video request was exercised without waiting for a terminal media error. Screen-reader behavior, touch targets, all contrast combinations, every video frame, all downstream evidence links, README fragment anchors and live hosted deployment were not assessed. No measured accessibility score, WCAG conformance claim, comparative quality claim or external human-first-use conclusion is made.

## Source identities

See `source-hashes.json` for SHA-256 of the sources used by this reader. `site-draft/index.html` and candidate `showcase/index.html` share SHA-256 `1154fd0d7b77da6f0a1c3ead0ef45b2e62231f9c46418273c2bf6b6d179c7337`.
