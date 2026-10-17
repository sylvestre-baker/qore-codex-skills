# Observed runtime recovery

The original default Docker seccomp profile refused the nested Codex command sandbox before a payload ran. A disposable Linux arm64 environment with a pinned, scoped namespace allowance passed the retained parent and child probes. This qualifies the observed setup for bounded trials; it does not certify trial correctness or every possible escape route.

## What changed

The [recovery record](recovery.json) pins the image, upstream seccomp source, baseline digest, exact added syscall rule and resulting profile digest. The upstream profile is not bundled or relicensed as first-party MIT. All other baseline rules remain in effect. The allowance for `clone`, `unshare`, `mount`, `umount2` and `pivot_root` is an explicit outer security tradeoff needed for nested unprivileged namespaces.

New containers run as UID1000, drop all host capabilities, enable no-new-privileges and have no host mounts or privileged mode. No Docker daemon, host sysctl or user browser setting was changed. This is a different bounded operator procedure from the historical `clean_room.sh` default; that default's failed probe remains valid.

The [effective settings](environment.json) and [actual launch](launch.json) show the named inner permission profile: deny root access, allow minimal runtime reads, read-only task inputs, writable output/scratch and disabled command networking. Root-owned [managed requirements](requirements.toml) constrain apps, plugins, memories, MCP servers, browser use and login shells. Existing model transport remains separate from task-tool networking. See the official [Codex permissions](https://learn.chatgpt.com/docs/permissions), [managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration) and [Docker seccomp](https://docs.docker.com/engine/security/seccomp/) references for the underlying controls.

## What was observed

| Boundary | Retained observation |
|---|---|
| Positive controls | The same outer image/security setup, without the inner command sandbox, could read harmless outside canaries and connect outward. [Actual receipt](positive-controls.json). |
| Inner command sandbox | Approved source bytes were read and hashed; input mutation, outside canary reads and a command socket were denied; output writing worked. [Boundary receipt](boundary.json). |
| Parent tool inventory | Twelve base helpers were reported; actual resource and template listings were empty. [Selected raw events](selected-events.json) and [parent report](parent-probe.json). |
| Delegated child | The returned report retains source bytes/digest, denied canaries/socket, reported fresh context and tool inventory. [Child report](child-probe.json). |
| Runtime versions | [Observed versions](versions.json) identify the immutable image and the context in which they were measured. |
| Independent examination | A separate verifier examined saved artifacts and allowed a bounded pilot with explicit limitations. [Full selected verification](independent-verification.json). |
| UX activation boundary | A separately qualified read-only relay uses the [frozen browser policy](browser-policy.json). Live worker requests and their actual receipts belong to individual UX cells. |

The CLI export omits raw child spawn/fork events. Child freshness is supported by the returned child report and parent consumption, with that provenance limit. Generic MCP helper names remain visible, but the observed listings were empty. Image generation was visible and unused. These observations do not prove that every hidden or service-side route is inaccessible.

The image was already available locally. No new dependency installation, paid service or global security change was used for recovery. This record is not an installer or a claim that an arbitrary machine can run the same campaign without qualification. Every cell retains its own environment, boundary and post-input checks.

## Public evidence identity

The recovery record maps selected public files to original private receipt digests. Most are byte-identical. Only declared private root prefixes are replaced in selected operator receipts; the MCP excerpt preserves original event objects and line identities. Credentials, complete model traces and unrelated private files are excluded. Sanitized evidence has its own digest and does not silently replace the original attempt.
