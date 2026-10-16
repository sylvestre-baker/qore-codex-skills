# Existing QAIZEN Labs observation

The silent recording shows an actual isolated Playwright browser session on 15 October 2026. English captions are supplied in [WebVTT](qaizen-demo.en.vtt) and as an English subtitle track in [the MP4](qaizen-demo-captioned.mp4). It contains no narration, synthetic frames, simulated timing comparison or claimed gain.

| Approximate time | Observed action |
| --- | --- |
| 00:00–00:05 | Open the existing QAIZEN Labs entry. The `/en/labs` request resolves to `/labs`. Tab focuses the skip link. Reject analytics consent in this new context. |
| 00:05–00:09 | Click the existing readiness card and observe the readiness introduction at `/labs/readiness-check`. |
| 00:09–00:12 | Click “Start the check” and observe the actual first question. No answer is selected. |
| 00:12–00:14 | Expand “What does this mean?” and capture its explanation. |
| 00:14–00:16 | Press Space on the focused disclosure summary. Its explanation closes. |
| 00:16–00:21 | Click Back. The introduction returns and its heading receives focus. |

The harness blocks non-GET/HEAD/OPTIONS requests. One `POST /api/labs/readiness/event` was blocked, producing one expected network/console error. That error is an instrumentation consequence; it is not presented as a website defect. No page exception was observed. The request's application behavior was not tested.

The browser video starts shortly before entry navigation. Caption times are approximate descriptions of the visible actions; exact UTC timestamps are in [the observations](observations.json). This recording does not establish full-site quality, instrumented accessibility, mobile coverage, native-app support or Core Web Vitals.
