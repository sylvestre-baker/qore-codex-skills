# Historical review and export limitation

[REPORT.md](REPORT.md) and `execution.json` retain the original execution identity and bytes. This note describes a later export correction, not a new review execution.

The public 0.2.0 export omitted 37 referenced source artifacts through ignored directories. The 35 original `.agents/` files are now selected for export with their recorded SHA-256 digests. Two original, unreferenced `__pycache__/*.pyc` files remain excluded under the repository's contribution policy.

Strict `validate-run` therefore cannot validate the complete historical record from the cache-free public export. The [pinned exception policy](../../execution-exceptions.json) identifies the exact unchanged execution and both excluded cache digests. `tools/check_execution_records.py` checks the remaining 251 artifacts and all phase obligations without editing the original record, then reports `KNOWN_EXCEPTION`, PARTIAL coverage and BLOCKED strict validation. This is not a strict COMPLETE pass.

No missing source is reconstructed, no old evidence is retimestamped and no new model execution is inferred from the correction. If the maintainer later chooses to include the original caches after a content and rights review, strict validation can be checked separately and the exception removed. The full archive remains subject to the current redistribution review.
