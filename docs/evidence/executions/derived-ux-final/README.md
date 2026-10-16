# Fresh final focused UX derivative probes

Both derivatives were newly generated from the final frozen instruction resources and checked again against their current project sources before selecting targets. Identity is instruction-resource SHA-256 `550e45ab0a07a641f8ec6d3cba5677e97a8e5fd86053631a1e75c90a8f8c52d0`, not an invented archive digest. [The comparison](comparison.json) preserves actual profiles, URLs, states and completion times.

| Current profile | Actual selected route | Actual visible state | Evidence |
| --- | --- | --- | --- |
| `qore` | `/index.html` | `Resolved synthetic state.` | [Source check](qore/profile-check.json), [consumption](qore/profile-use.json), [DOM](qore/browser/02-final.dom.json), [opened screenshot](qore/resolved.png) |
| `qore-contrast` | `/alternate.html` | `Alternate resolved synthetic state.` | [Source check](contrast/profile-check.json), [consumption](contrast/profile-use.json), [DOM](contrast/browser/02-final.dom.json), [opened screenshot](contrast/resolved.png) |

The operator input contained no URL or expected-state facts. Each fresh checker returned current source facts, the helper read those returned facts to select navigation and visibility assertions, and the served HTML matched approved source bytes. The exact neighboring state line was absent in each observation.

These are labelled synthetic fixtures and **COMPLETE focused profile-consumption probes**, not complete derivative UX audits. No full gate matrix or stop cycle is fabricated. The actual complete generic method run is [recorded separately](../generic-ux-final/README.md). [Commands](qore/commands.json) and [contrast commands](contrast/commands.json) disclose redacted display placeholders. [Provenance](provenance.json) maps distinct public IDs to raw source digests, derivative manifest identities and unchanged screenshots. Raw traces remain private; no independent-evaluator or external-human-first-use claim is made.
