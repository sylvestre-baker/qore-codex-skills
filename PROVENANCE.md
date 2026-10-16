# Provenance and license

This repository is a new first-party implementation of the three Qore methods maintained by Sylvestre Franceschi. Its original code and authored documentation are offered under the MIT license in LICENSE.

The methods were reconciled against existing Qore planning, review and UX workflows. The public implementation is re-authored around the accepted behavioral contracts. Private client bundles, client notices, personal installations and their Git histories are not redistributed. An internal distribution notice is not used as a public license grant.

The private implementation audit retains source digests and reconciliation decisions. Those private source paths and reports are deliberately excluded from this repository's release allowlist.

Public browser observations concern the existing Qaizen Labs surface. The selected observations and screenshots retain their source identity, and the video presentation has a documented captioning transformation. See docs/evidence/browser/provenance.json. No private raw trace is published automatically.

External documentation links are informational sources, not downloaded runtime instructions. The optional Playwright driver is not vendored and has its own upstream license. The core assembly and contract checks use Python's standard library plus the declared shell and Node runtimes.

The explicit `release-rights.json` record binds each reviewed export resource to its digest, origin, license and approval basis. Build refuses missing, stale or unknown redistribution entries. This is a maintainer attestation, not an automated determination of ownership. Changes require reviewing the affected content before renewing its entry. The rights record and export allowlist are first-party metadata and are included in the final manifest.
