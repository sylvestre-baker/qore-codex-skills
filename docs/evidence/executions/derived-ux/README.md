# Focused synthetic UX profile probes

Public bundle ID: `public-focused-derived-ux-20261015-01`. Both probes used derivatives freshly assembled from candidate b, archive SHA-256 `2963c43e98803354932e406627d9e239064fbe2899745a7e093b7d4154fa56d1`.

The focused question was whether current profile facts would actually change browser behavior when the operator supplied only the derivative and project root. Both probes completed. The checker ran before target selection, current source digests matched, and only its returned `surfaces.web` facts selected the actual URL and exact visible-state assertion. The served HTML bytes matched the approved candidate fixtures.

| Profile | Actual route | Actual resolved state | Evidence |
| --- | --- | --- | --- |
| `qore` | `http://127.0.0.1:8765/index.html` | `Resolved synthetic state.` | [Profile check](qore/profile-check.json), [fact consumption](qore/profile-use.json), [DOM](qore/browser/02-final.dom.json), [unchanged screenshot](qore/resolved.png) |
| `qore-contrast` | `http://127.0.0.1:8765/alternate.html` | `Alternate resolved synthetic state.` | [Profile check](contrast/profile-check.json), [fact consumption](contrast/profile-use.json), [DOM](contrast/browser/02-final.dom.json), [unchanged screenshot](contrast/resolved.png) |

The exact neighboring state line was absent in each result. [The comparison](comparison.json), [primary input](qore/invocation.json) and [contrast input](contrast/invocation.json) preserve this distinction. The assertion and route were read from current profile data, rather than supplied as target facts in the operator input.

These are explicitly labelled synthetic fixtures. They establish the focused route/state profile-consumption contrast, not existing-product quality, a complete derivative UX audit or a full-method SHIP verdict. A full `qore-run/1` derivative audit wrapper is deliberately omitted: the probes did not execute a complete gate matrix and stop-rule cycle, and those phases must not be fabricated. The genuine existing-site method execution is recorded separately in [generic UX](../generic-ux/README.md).

[Transformation provenance](provenance.json) supplies new public IDs, original candidate/profile identities, raw/public digests and transformations. Raw traces remain private. [Primary commands](qore/commands.json) and [contrast commands](contrast/commands.json) are redacted display argv with disclosed logical placeholders; those substituted strings were not literally executed. The original UX author prepared this export and does not claim independent evaluation or external human first use.
