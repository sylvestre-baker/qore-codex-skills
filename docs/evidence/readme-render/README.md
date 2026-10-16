# Rendered README and caption checks

The exact [README source snapshot](source-readme.txt) was rendered at 1440×1000 and 390×844 using the declared local GFM renderer. There was no document-wide horizontal overflow, both linked images loaded with descriptive alternative text, the first keyboard-focused link had a visible outline, and all three code blocks remained text. Tables/code may scroll inside their own containers.

[Wide entry](wide-entry.png), [narrow entry](narrow-entry.png), [wide evidence](wide-evidence.png), [narrow evidence](narrow-evidence.png), and [observations](observations.json) retain the actual views. The maintainer opened the original wide/narrow captures. A separate verifier checks these artifacts; this record is not that independent review.

[Caption playback](caption-playback.png) and [player observations](playback.json) show the actual 78.16-second MP4 advancing without player error, with the supplied English WebVTT cue active and caption mode showing. The presentation remains silent with a separate transcript.

[Provenance](provenance.json) identifies source/tool/dependency revisions. The optional docs_preview.mjs tool requires explicitly supplied local marked and Playwright packages with a matching browser; it neither installs dependencies nor contacts a hosted renderer. This is local GitHub-compatible GFM rendering with similar CSS, not an actual GitHub-hosted or instrumented accessibility certification.
