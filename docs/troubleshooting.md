# Troubleshooting

Keep the original diagnostic and the candidate/target identity when reporting a failure. Retrying with a different target or changing a declaration is not evidence that the original check succeeded.

| What you see | Meaning and next step |
|---|---|
| `Release destination exists; choose new staging` | The versioned build folder or ZIP already exists. Choose a new staging location. Keep the current candidate for comparison. |
| `Derived destination exists; choose new staging` | Derivation preserves its current output. Generate to a different unused path; compare before migration. |
| `Installed destination exists; preserve it and compare a new candidate` | At least one skill destination already exists. Existing content was not replaced. Use a fresh target or review an explicit migration; there is no force option. |
| `Resource changed` or an inventory mismatch | Candidate bytes or the file set differ from its manifest. Keep the altered tree as evidence and build a new candidate from the intended sources. Do not edit hashes to disguise the change. |
| `Changed or missing source` | A profile fact no longer matches its recorded source. Read and reconcile the source/profile, then regenerate. Affected coverage remains PARTIAL or BLOCKED until refreshed. |
| `No current web surface is available for this profile` | The UX consumer has no current source-backed target. Check its source, URL, kind, required state, and applicability. Do not borrow another project's surface. |
| A path/symlink escape is refused | The input crosses a declared local boundary. Use contained real source files and a valid target root; do not disable containment checks. |
| Malformed or truncated findings JSON | Retrieve the full worker report and restore a strict findings envelope before filtering. `{}` cannot mean zero findings. |
| `unresolved_findings` with PARTIAL/PENDING after verification | Critical/high candidates remain PLAUSIBLE. Retain their severity and investigate the missing observation. The verifier having run does not resolve them. |
| `local_adaptations` names `references/project.json` | The bundled profile differs from its recorded base. Review the local customization; current facts remain usable if source checks pass. Preserve the edit and reconcile the maintained profile before regeneration. |
| A required browser capability is unavailable | Record the failed probe and dependent gaps. One non-destructive transient retry is allowed; then retain PARTIAL/BLOCKED coverage. No software installation, process termination, or lock removal is implied. |
| A required UX gate is skipped or stale | Global SHIP is unavailable. Run the missing check or renew observations after the correction. Do not narrow the original scope because a tool is absent. |
| The sixth UX iteration still fails | Stop and report remaining defects/gaps. A persistent zero gate does not extend the ceiling. Resume only as separately scoped work. |

## Codex does not discover the installed skill

Check that the installer printed the intended project's `.agents/skills/` paths, and open a new chat in that project directory. Invoke the exact generic name (`$qore-plan`, `$qore-review`, `$qore-ux-review`) or the generated name including the profile ID. Inspect the installed `SKILL.md` if the name is uncertain.

If discovery still fails, record the Codex version, selected project directory, installed folder paths, and actual discovery result. Treat direct file loading, automatic discovery, and candidate-only clean discovery as different observations. Do not claim portability from an installation on the author's configured host. See the [independent Linux procedure](clean-environment.md).

The installer reports `same-name-user-skill` if a matching folder exists in the personal `.agents/skills/` directory. It leaves that installation unchanged. Inspect the exact selected skill path in a fresh chat; the warning does not prove which version Codex selected. Project-specific descriptions include the profile ID to distinguish derivatives from the generic methods.

## A role or verifier cannot finish

Keep the requested/returned roster and complete available report files. Recover truncated output from its worker; a lead-written summary cannot replace missing evidence. Schedule the required roles in waves if concurrency is limited. Do not relabel one context as several independent workers.

Without a fresh separate verifier, candidates remain PLAUSIBLE and the review is PARTIAL or BLOCKED. Use the findings validator's `--verifier=skipped` declaration. Preserve the original impact severity, including high/critical uncertainty; missing verification is not a reason to downgrade a candidate. A lead's useful self-check does not complete the independent phase.

## A local browser probe fails

The [optional browser helper](evidence/browser/README.md#reproduce-with-a-declared-optional-driver) requires a locally available Playwright package and matching browser. It does not install them. Its action sequence, target origin, and data interactions must fit the user's authorized scope. An unavailable helper does not establish a page defect.

For local fixtures, confirm the server is listening and that the URL belongs to the same environment as the browser. A container's localhost differs from the host's localhost. Inspect exact console/network events rather than ignoring all errors. The recorded QAIZEN demonstration's blocked analytics request is a property of that observation harness; it is not a blanket exception for future failures.

## Report a reproducible issue

For handled installation failures, inspect `recovery.safe_to_retry`, `retained_paths`, `cleanup_errors` and `next_action` in stderr JSON. Preserve uncertain files; do not delete every folder matching `qore-*`. Follow the [recovery instructions](../INSTALL.md#recover-from-a-handled-installation-error) or [controlled recovery tutorial](tutorials/recoverable-install.md).

Provide the method, target/candidate/profile identities, actual command or prompt, expected outcome, observed outcome, relevant evidence, and execution limits. Remove credentials and private data before sharing. Follow [contributing guidance](../CONTRIBUTING.md); no external message or publication happens automatically.
