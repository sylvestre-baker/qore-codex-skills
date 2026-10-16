# Qaizen Labs: a project-specific verification case

This public workspace describes one existing journey. It contains no website source, private rules or questionnaire answers. The maintained profile is `profiles/qaizen-labs.json` at the Qore repository root; use this directory as its project root.

The useful change is a correction to a verification protocol: a successful mouse click on Back must not establish that Back is reachable and usable by keyboard. That coverage gap was independently reproduced against the private planning specification on 16 October 2026. It was not a defect observed on the Qaizen website, nor a discovery by the later derived review.

The [surface contract](surface-contract.json) separates declared acceptance from dated public observations. Close must restore focus to the help summary; Back must restore focus to the introduction heading. These are distinct project facts that each method must consume from its generated profile, without repeating them in the invocation.

Run the offline contract check from this directory:

```sh
python3 -B checks/check_contract.py surface-contract.json
```

The check establishes internal consistency. A fresh real browser run is required for website behavior. The scoped observation must leave the first question unanswered, block non-read requests and stay within the authorized origin. Keyboard traversal and its focused target must be recorded before Back activation. Direct focus, a locator's automatic focus or a mouse click cannot prove that traversal.

Plan the known correction, independently challenge its assertions, then observe the real entry/state journey. Synthetic reachable/unreachable controls qualify the test itself and remain separate from the live site result. A review with no new confirmed defect is valid. No performance, general accessibility, productivity or Ambassador acceptance claim follows.

The current optional harness refuses HTTP document redirects before following them, including same-origin redirects. Top-level documents use a guarded fetch with no automatic redirect following, then fulfill the actual response into the browser. This is a declared observation constraint; a target requiring such a redirect remains incomplete. Client-side navigation inside the allowed origin is exercised separately. This guard is necessary because [Playwright routes do not intercept later HTTP redirect hops](https://playwright.dev/docs/network#redirects). Raw traces may contain network/page data; only selected reviewed evidence is shareable.

Actual outcomes and identities: [three-method case evidence](../../docs/evidence/qaizen-labs/README.md). The plan, source review and browser observation remain separate executions.
