# Adapt the methods to a project

Use the generic methods first when you need a single task. A persistent profile is useful when the same project commands, invariants, and surfaces should guide future invocations of all three methods.

## Maintain one sourced profile

The [Qore profile](../profiles/qore.json) is the maintained public example for this repository. Its source is [qore.json](../qore.json). The [contrasting profile](../profiles/contrast.json) uses a clearly labeled synthetic source and an alternate fixture route to check isolation. The Qore profile's web surface is also a **fixture**; it is separate from the [existing-site browser observation](evidence/browser/README.md).

The [project schema](../schemas/qore-project.schema.json) describes `qore-project/1`:

| Field | Meaning |
|---|---|
| `id`, `version` | Project identity and maintained profile version. |
| `sources` | Unique source IDs, contained project-relative paths, and current SHA-256 digests. |
| `commands` | Named argument vectors, each bound to a declared source. Optional `applies_to` narrows methods. |
| `invariants` | Named statements, their source, and applicable `plan`, `review`, or `ux` methods. |
| `surfaces.web` | Entry URL, allowed origins, observable required state, source ID, and `fixture`, `application`, or `documentation` kind. |

Start from actual project instructions and current code/configuration. Record a fact only when the referenced source supports it. Resolve contradictions rather than copying a neighboring project's conventions. Include no credentials, personal paths, permission tokens, or private material intended for public export.

The runtime checker checks structure, source identity, and method applicability. It cannot prove that a sentence is a faithful interpretation of its source. A command's presence does not approve executing it; inspect its effect and follow the user's authorization.

For a bundled `references/project.json`, runtime output also reports `local_adaptations` by comparing its bytes with `references/release.json`. A valid local customization is named without blocking current sourced facts. This is a comparison with the bundled baseline, not an authenticity guarantee; `compare` still checks the wider installed file set against a supplied candidate.

## Check before deriving

From this repository, preview the plan facts:

```sh
python3 tools/context.py profiles/qore.json --root . --method plan
```

Use `--method review` or `--method ux` to inspect those consumers. A current result is `qore-context-check/1` with matching source digests, selected facts, no problems, and COMPLETE context coverage. That result describes context only; it does not mean the method ran. The checker does not execute profile commands.

Generate into a new destination, as in the [README adaptation example](../README.md#adapt-all-three-methods-from-one-profile). Derivation validates all three consumers before writing the new candidate. Install a derived candidate with the same `install --source … --project-root …` interface used for generic skills. The generated names include the profile ID, for example `$qore-review-qore`.

Each derivative explicitly loads `references/project.json`. Before consuming its facts, it runs its bundled checker from its own skill directory:

```sh
python3 scripts/project-check.py references/project.json --root /absolute/path/to/project --method review
```

Select the actual method value for that derivative. The result identifies the exact profile digest and fresh applicable commands, invariants, and web facts. Record the fact IDs actually consumed and how they affected the work; selected facts alone do not prove behavior.

## Update without overwriting

1. Keep the current installed/generated folders intact.
2. Read the changed project source and reconcile the maintained profile's facts and digests. A changed digest is a request to recheck meaning, not permission to suppress a warning.
3. Derive to a different unused staging path. For a later candidate, for example:

   ```sh
   python3 tools/qore.py derive --profile profiles/qore.json --project-root . --output /tmp/qore-derived-next
   ```

4. Compare the current folders with the new candidate. The read-only comparison reports each differing path, both digests, and whether the installed file differs from its recorded base:

   ```sh
   python3 tools/qore.py compare --source /tmp/qore-derived-next --project-root .
   ```

   Preserve local adaptations and expose conflicting changes. There is no automatic merge or rollback command.
5. Use an explicitly chosen migration/install destination. The installer refuses an existing skill folder; it has no overwrite option.

When a source changes or disappears after assembly, affected profile use becomes PARTIAL or BLOCKED. Unaffected current work can continue with visible limits. The derivative cannot silently substitute generic behavior or claim that a stale invariant is current. Refresh and regenerate before claiming the affected work complete.

See [troubleshooting](troubleshooting.md) for source mismatches, missing surfaces, and destination collisions.
