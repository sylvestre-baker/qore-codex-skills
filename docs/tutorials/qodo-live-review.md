# Run a new Qodo review of the historical change

This is an optional live how-to after the [local replay tutorial](qodo-review.md). It contacts Qodo and sends the public-code change for review. It is separate from reproducing the recorded code observations offline.

## Prerequisites

Use a full Git checkout of this public repository, `python3`, Git, Node.js, and a reviewed official Qodo Agentic Toolbox CLI. The original run used **CLI 1.6.0**, not the deprecated Qodo Command or Qodo Gen CLIs. Check the [official installation documentation](https://docs.qodo.ai/agentic-toolbox/cli) for current installation and account requirements; no installer or CLI binary is bundled here.

The CLI requires authentication and access to the public base repository. Connect only repositories you intend to authorize, inspect any displayed permissions, and follow your workspace's usage terms. Local preparation does not log in, install a GitHub app, buy a plan or submit a review.

The [official Reviewer documentation](https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-codebase-review-skill) explains local diffs, review context and the requirement for the base commit to exist at the provider. The instructions below use the observed 1.6.0 command interface. Future versions or account configuration may differ.

## Prepare the exact complete public change

From this repository root:

```sh
qodo_live_root="$(mktemp -d "${TMPDIR:-/tmp}/qore-qodo-live.XXXXXX")"
python3 -B examples/qodo-review/prepare_live.py --output "$qodo_live_root/run"
```

Expect `qodo_submitted: false`, `changed_files: 77`, base `a4fef83aadd6610435da5ac0cc7e53b34fe1dd4f` and tree `c10015840a872caf200164d69aa650b6d0bda8b5`. The script copies Git objects locally into an independent new target; it does not retain an alternate-object dependency on the source checkout. The target's origin is the public Qore repository.

The source checkout is unchanged. An existing destination is refused. A shallow clone or extracted source ZIP may lack the historical Git objects; use a full clone. The script does not automatically fetch from a network or modify the source repository to repair missing history.

## Submit and retain the new result

The next commands are **reference templates with user-supplied paths and operation IDs**. The historical run used the same CLI arguments against the same prepared tree; these exact substitutions are not claimed as a new executed review.

Set `qodo_cli` to your locally reviewed 1.6.0 `qodo.mjs`. Its recorded official bundle digest is `cc4171611b9016386fc7d7bbd5d4e94a3d3a5f079b86c7ebc425a8d171efd4e7`. The official source URL observed for that version was `https://get.qodo.ai/releases/1.6.0/qodo.mjs`; the file is not redistributed by Qore.

```sh
qodo_cli=/absolute/path/to/your/reviewed/qodo.mjs
cd "$qodo_live_root/run/target"
node "$qodo_cli" --no-onboarding --json review \
  --base a4fef83aadd6610435da5ac0cc7e53b34fe1dd4f \
  --context-file ../review-context.json --full --deep --async \
  > ../submission.json 2> ../submission.stderr
```

An accepted operation is not a completed review. Read the submission exit status and JSON; retain both streams. The 1.6.0 CLI can return exit 0 with an operation ID while the analysis is still working.

Use the returned actual ID in the following template, retaining each collection separately:

```sh
node "$qodo_cli" --no-onboarding --json review status ACTUAL_OPERATION_ID \
  > ../collection-01.json 2> ../collection-01.stderr
```

In the tested 1.6.0 interface, status exit 2 means still working. Exit 1 can report failure; it does not mean zero findings. A terminal successful response contains findings and metadata. Inspect both, including skipped reviewers, unresolved context and finding-inventory warnings. Do not repeatedly submit the same review while an operation is already running.

The recipe intentionally uses standard repository autodetection from the configured public origin. Our earlier wrapper passed a full HTTPS URL through `--repo`; that explicit option was forwarded verbatim as a repository name. A run with that override still failed after repository access was connected, while autodetection subsequently succeeded. This sequence did not isolate a unique internal failure cause, so it is an integration observation rather than a general service-failure claim.

The bundled context keeps the historical public spec reference. It was unresolved in the original run. Passing a URL does not establish that Qodo consumed the specification; inspect the returned metadata before claiming that phase completed.

## Verify the findings separately

Retain the original response locally. Select native finding IDs, action levels, descriptions and evidence into a separate file before handing it to a fresh verifier. Withhold proposed fixes, confidence labels and the author's conclusions. Preserve `action_level`; it is not the Qore severity enum.

Reproduce or refute the returned claims on their exact target, then check the intended delivery version. Keep unexamined IDs visible. The [decision record in the tutorial](qodo-review.md#apply-the-lesson-to-your-own-change) provides the fields to retain.

The current repository's ordinary diff-review workflow remains appropriate for routine changes. The [Qore review method](../../skills/qore-review/SKILL.md) describes a different, full three-finder protocol; using an external Qodo finder and a separate verifier does not silently count as that protocol.

## Troubleshoot the observed gaps

| Observation | Next action |
|---|---|
| Authentication refused | Use the official login flow for the intended account; never put a credential in a public log |
| No authorized repositories | Check the intended workspace and repository connection before submitting another review |
| Operation accepted, then failed | Keep the operation and error privately; inspect access and input format rather than treating it as an empty review |
| Spec reference unresolved | Record the missing phase; do not equate a supplied reference with consumed content |
| Previous finding inventory incomplete | Check earlier open findings separately; a new result is not automatic closure |
| Different findings on a fresh run | Retain the new source, context and result identities; do not relabel the new run as the historical one |

These are observations and recovery paths from this bounded trial, not a promise that they diagnose every account or service problem.
