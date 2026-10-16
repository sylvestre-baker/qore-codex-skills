# Optional transport: dependency disposition

Agent Mail Rust is optional. Qore does not bundle or automatically install its binary, run its installer, rewrite global configuration or require its server for the three methods.

The bounded local trial pins **v0.3.39**, source commit `a4ec56bc43236693170588dc4fff29654a2f7119`, with the maintainer-signed archive independently verified in the historical trial. Its affected `lru 0.16.4` lock entry has a focused source disposition, not a clean dependency audit.

[RUSTSEC-2026-0253](https://rustsec.org/advisories/RUSTSEC-2026-0253.html), checked on 16 October 2026, concerns panic safety in `LruCache::pop()`. The pinned lock's sole affected consumer is checksum-verified Tantivy 0.26.2. Its private cache uses `usize` keys, has no potentially panicking key destructor and does not call the vulnerable removal operation. The tagged portable release feature chain also excludes hybrid/FrankenSearch. These establish narrow nonapplicability to the reviewed source paths.

The exact distributed binary's resolved features and source correspondence have not been reproduced or established by an SBOM. **Persistent-service recommendation therefore remains PARTIAL.** Bounded cooperative local functional tests retain the signed artifact identity and this limitation. No user risk acceptance, general non-vulnerability or hostile actor authentication is asserted. A signature establishes the release trust relationship, not dependency safety.

Primary references: [pinned lock](https://github.com/Dicklesworthstone/mcp_agent_mail_rust/blob/v0.3.39/Cargo.lock), [release workflow](https://github.com/Dicklesworthstone/mcp_agent_mail_rust/blob/v0.3.39/.github/workflows/dist.yml), [Tantivy source](https://docs.rs/crate/tantivy/0.26.2/source/src/store/reader.rs), [upstream release](https://github.com/Dicklesworthstone/mcp_agent_mail_rust/releases/tag/v0.3.39). The private review retained checksums and fetched sources; it does not claim to have found a supporting advisory note in this release's text.

For a persistent recommendation, obtain binary build/SBOM evidence of the resolved feature path or a corrected upstream pin, then rerun affected transport and recovery tests. Re-evaluate when the binary, source paths or deployment scope changes. Do not use loopback as evidence of advisory nonapplicability or silently substitute another product.
