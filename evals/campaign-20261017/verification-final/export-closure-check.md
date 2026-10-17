# Separate export closure verification

Verifier `/root/campaign_final_verifier`; status VERIFIED. Start 2026-10-17T12:25:52Z; end 2026-10-17T12:26:39.389719+00:00; active wall time 47.39 seconds, within 60 seconds; no intentional idle.

Verified all **19 export companions** (12 U2-derived, 7 U2-generic) byte-for-byte against both the same trial's private frozen prepared inputs and public prepared copies. Every companion was absent from the original worker output, and each added outer artifact is explicitly `presentation`. The separate export manifest discloses export-only closure and states that these files do not prove worker consumption.

Compared every original raw final-output file against its corresponding public file: no mismatches. Compared original extracted output against every file in the original final-output.tar: no mismatches. Both native qore-run files and their original/evaluation digests remain identical. Actual read-only `evaluate.check_record` returned valid=true for both outer evaluations, retaining PARTIAL qualified coverage and UNVERIFIED comparability. Full counts, hashes, per-file companion paths and actual checker outputs are in export-closure-check.json.

Original qualification-decisions.json and verification-final/REPORT.md hashes are unchanged. No original report, trial, code, browser or runtime was rerun or modified. This check establishes export companion identity/disclosure and archive integrity only. It grants no broader historical/runtime exemption, does not establish which references the worker read, does not close missing original observations, and makes no deployment/release or historical-compliance claim. Existing coverage, quality, telemetry and runtime unknowns remain.
