# Independent Linux qualification

The clean-room helper prepares a separate Linux container using only a pinned public Node image, declared Linux packages and `@openai/codex@0.162.0`. It uses no host mounts, author home directories, installed personal skills, client images or Docker socket. The process runs as the unprivileged `node` user, with all capabilities dropped and no-new-privileges enabled. Container networking permits the normal authenticated Codex service; no live call happens during preparation.

```sh
bash tools/clean_room.sh prepare qore-qualification-20261015-example /tmp/qore-clean-audit-new
bash tools/clean_room.sh inspect qore-qualification-20261015-example
bash tools/clean_room.sh stage qore-qualification-20261015-example /path/to/qore-skills-0.1.0.zip
```

Preparation prints image/container identities and records build and version logs. The audit directory must be new. Staging streams the ZIP into an owner-only file created by the container user, rejects traversal, absolute paths, symlinks, duplicates and unexpected archive structure, then runs the candidate's integrity verification. No author source directory is mounted.

An authorized operator supplies a temporary, standard Codex `auth.json` to `/home/node/.codex/auth.json` by streaming it over `docker exec -i` into an owner-only file created by UID 1000. Never print its contents or record the stream. Never copy personal `config.toml`, user skills, plugins or rules, and never include credentials in build contexts, logs or artifacts. The helper only checks that the auth file exists; it does not display its contents. Delete the container after extracting the intended evidence to remove its credential copy.

After the candidate is frozen and the explicit qualification prompt has been reviewed:

```sh
bash tools/clean_room.sh run qore-qualification-20261015-example qualification-prompt.txt > execution.jsonl
```

An optional fourth argument selects an explicitly chosen available model. The invocation uses `--ignore-user-config --ignore-rules --ephemeral --json` and the candidate directory. The container provides the outer isolation; the CLI can execute the authorized public-code checks there without nested sandbox requirements. Candidate-only `.agents/skills` discovery and all required finder/verifier phases still need actual observation and identity-bound evidence. A prepared image, an integrity check or a model response alone does not complete qualification.

Use `docker cp` for approved inputs and evidence extraction. Start any fixture server inside the container; host `127.0.0.1` is a different environment. Initial review qualification does not require Playwright. Browser qualification performed elsewhere retains its separate environment identity.

```sh
bash tools/clean_room.sh cleanup qore-qualification-20261015-example
```

Cleanup removes only the named qualification container and retains its image. It does not prune images or stop unrelated containers. An independent container run is portability evidence, not external human first-use evidence.
