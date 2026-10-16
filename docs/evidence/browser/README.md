# Browser evidence — 15 October 2026

Playwright Chromium successfully observed an isolated synthetic fixture first, then the existing [QAIZEN Labs](https://qaizen.io/labs) entry and readiness UI. The earlier failed launch remains part of the private history; this later success qualifies only the tested driver and environment.

The real question was whether a visitor could reach the existing check from Labs and enter and leave its first-question state without submitting answers. The observed path completed: entry → readiness introduction → first question → explanation open/closed by keyboard → restored introduction with heading focus. This supports using that existing path for a scoped demonstration. It does not establish whole-site readiness.

Inspect [timestamped observations](observations.json), the [capability/depth matrix](capability-matrix.json), [transformation provenance](provenance.json), the [captioned recording](qaizen-demo-captioned.mp4), [English captions](qaizen-demo.en.vtt) and [transcript](qaizen-transcript.md). Selected unchanged screenshots show the [real entry](qaizen-entry.png), [first question](qaizen-question.png) and [restored introduction](qaizen-returned.png).

## Observed driver and scope

Node v24.19.0, Playwright 1.62.1 and Chromium 151.0.7922.34 ran at a 1280 × 800 viewport. Navigation, screenshot capture, DOM inspection, keyboard interaction, console listening and network observation worked. The synthetic fixture emitted explicit console and fetch events; its label prevents confusion with existing-product evidence.

The real path produced 73 response records, no page exceptions and one blocked anonymous-event POST. The harness deliberately blocks non-GET/HEAD/OPTIONS traffic. Its resulting console error is retained and attributed to the observation policy. No answer, email, booking or contact form was submitted. No user browser session was accessed.

Entry and the declared local state transitions are **COMPLETE within the observation scope**. Full UX review remains **PARTIAL**: instrumented accessibility, performance, alternate viewports, all quiz questions/results and error-state coverage were not executed. No global SHIP verdict is claimed.

## Reproduce with a declared optional driver

The browser helper does not install dependencies, stop browser processes or remove locks. Supply a locally installed `playwright` package and its matching browser. Output must be a new directory. The actions file is explicit and must be reviewed against the authorized scope.

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory tests/fixtures/web
```

In a second terminal:

```sh
node tools/browser_probe.mjs \
  --url http://127.0.0.1:8765/index.html \
  --output /tmp/qore-browser-fixture-new \
  --actions tests/fixtures/web/primary-actions.json \
  --playwright-module "$PLAYWRIGHT_MODULE" \
  --label 'Synthetic driver qualification only'
```

`PLAYWRIGHT_MODULE` identifies the already installed optional Playwright package. A missing package or unusable browser produces a diagnostic and BLOCKED/PARTIAL evidence; it never becomes a passing browser check. The action vocabulary is `click` (role/name or selector), `keyboard`, `assert-text`, `assert-url` and `snapshot`, with at most 40 steps. The helper's COMPLETE status describes its stated action scope only.

For the observed existing-site path, the same helper used `--url https://qaizen.io/en/labs` and [the explicit action sequence](qaizen-actions.json). Live-site content and routes can change; inspect the current result and do not inherit this run's outcome.
