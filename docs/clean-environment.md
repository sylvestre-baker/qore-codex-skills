# Independent Linux qualification

The clean-room helper prepares a separate Linux container using only a pinned public Node image, declared Linux packages and `@openai/codex@0.162.0`. It uses no host mounts, author home directories, installed personal skills, client images or Docker socket. The process runs as the unprivileged `node` user, with all capabilities dropped and no-new-privileges enabled. Container networking permits the normal authenticated Codex service; no live call happens during preparation.

```sh
bash tools/clean_room.sh prepare qore-qualification-20261015-example /tmp/qore-clean-audit-new
bash tools/clean_room.sh inspect qore-qualification-20261015-example
bash tools/clean_room.sh stage qore-qualification-20261015-example /path/to/candidate.zip
```

Preparation prints image/container identities and records build and version logs. The audit directory must be new. Staging streams the ZIP into an owner-only file created by the container user. It rejects traversal, absolute paths, symlinks, duplicate paths, unsupported JSON/release metadata, extra or altered resources, and archives exceeding 20,000 entries or 1 GB of expanded data before extracting or running candidate code. The single archive root must match the version in its `qore-release/1` manifest; no release version is hardcoded in staging or execution. Digests verify consistency with the operator-supplied archive, not publisher authenticity.

Candidate verification runs as the unprivileged worker. Only after successful verification does a root process create `/var/lib/qore-qualification/stage.json` outside the candidate. This record contains the selected root, release version, archive and manifest digests, and verification result. Its directory is root-owned and not group/world writable; the record is root-owned and read-only. Workers cannot change the selected root through candidate files. Before each run, the helper reads only this fixed record, accepts its explicit schema/fields, checks the root/version, and rechecks all recorded resource digests. Re-staging or an existing destination is refused. No author source directory is mounted.

An authorized operator supplies a temporary, standard Codex `auth.json` to `/home/node/.codex/auth.json` by streaming it over `docker exec -i` into an owner-only file created by UID 1000. Never print its contents or record the stream. Never copy personal `config.toml`, user skills, plugins or rules, and never include credentials in build contexts, logs or artifacts. The helper only checks that the auth file exists; it does not display its contents. Delete the container after extracting the intended evidence to remove its credential copy.

After the candidate is frozen and the explicit qualification prompt has been reviewed:

```sh
bash tools/clean_room.sh run qore-qualification-20261015-example qualification-prompt.txt > execution.jsonl
```

An optional fourth argument selects an explicitly chosen available model. The invocation uses `--ignore-user-config --ignore-rules --ephemeral --json`, `--sandbox workspace-write`, `sandbox_workspace_write.network_access=false`, and `web_search="disabled"`. It never falls back to full access. The container permits the authenticated model transport; command networking and hosted web search are separate controls. See the [official security reference](https://learn.chatgpt.com/docs/agent-approvals-security). Disabling user config and rules does not itself prove that no project configuration, app, MCP server, hook or alternative tool is available: inspect the actual fresh environment before comparison.

Before checking credentials or starting a model invocation, `run` executes a local `codex sandbox` startup canary with workspace-write and command networking disabled. If the sandbox cannot start, `run` exits with that failure. A startup canary is a feasibility check, not full proof of filesystem or network denial behavior. Successful qualification still requires positive and negative canaries for the intended boundaries, actual candidate-only `.agents/skills` discovery, and all required finder/verifier phases. A prepared image, an integrity check or a model response alone does not complete qualification.

On 17 October 2026, the declared unprivileged Docker configuration and an existing public Codex 0.162.0 image failed the no-auth sandbox canary before executing the payload: Bubblewrap could not create a new namespace. No authenticated model call was made. The [recorded probe](evidence/specialization/isolation-probe.json) establishes **BLOCKED** feasibility for that exact environment, not that every Linux host is unsupported. Keep the affected campaign blocked until an authorized compatible environment passes the intended canaries. Do not enable privileged mode, add capabilities, change host sysctls or use full access to make a trial appear complete.

## Full-archive qualification and evaluation workers

This helper stages the complete approved archive for package portability qualification. That archive contains documentation and earlier evidence, so it must **not** be supplied wholesale to a specialization-evaluation worker. Package qualification and experimental isolation are separate operations.

For a comparative trial, first verify the full candidate outside the worker, then prepare a new reduced evaluation bundle from the experiment's explicit allowlist. Supply only the common target sources, the condition's complete autonomous skill resources, and its prompt. Exclude history, previous reports, answer keys, corrected comparators for incomplete-protocol scenarios, personal configurations and other conditions' resources. Do not mount the full repository, original candidate or control metadata into the worker. An evaluation worker is not isolated merely because it has a new chat or output directory. The baseline must not receive Qore resources; generic and derived conditions must each receive only their declared variant.

Use `docker cp` for approved inputs and evidence extraction. Start any fixture server inside the container; host `127.0.0.1` is a different environment. Initial review qualification does not require Playwright. Browser qualification performed elsewhere retains its separate environment identity.

```sh
bash tools/clean_room.sh cleanup qore-qualification-20261015-example
```

Cleanup removes only the named qualification container and retains its image. It does not prune images or stop unrelated containers. An independent container run is portability evidence, not external human first-use evidence.
