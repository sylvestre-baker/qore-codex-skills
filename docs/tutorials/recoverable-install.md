# Recover an interrupted Qore installation

Qore provides three independent Codex methods: prepare a sourced plan, challenge a deliverable, and inspect a rendered web interface. A project can derive specialized versions from one sourced profile. Before using those methods, a developer needs all three skill folders installed reliably.

[Watch the 3:30 lesson and run its pinned offline replay](../evidence/install-recovery/README.md). The public case keeps Qodo advice, independent verification and author corrections distinct.

## The problem and observed outcome

On public main `e9d74cfeadd299a52f66919598b8330d6225e947`, a controlled error before the second skill copy leaves the first skill installed. Repeating the same command is refused because that folder already exists. The ordinary control installs all three skills correctly. This is an injected filesystem failure, not a reported customer incident.

The corrected installer prepares and verifies private staging before creating final destinations exclusively. A handled failure cleans up unchanged content owned by that attempt. If cleanup is unsafe or fails, recovery output identifies retained paths and the next action. It preserves the no-overwrite policy and local adaptations. See [installation and recovery](../../INSTALL.md).

The demonstrated user benefit is a recoverable installation: after resolving the original cause, the same command can install all three skills without manually deleting partial skill folders. There is no measured time saving, incident-prevention claim, crash recovery or atomic three-folder guarantee.

## What Qodo contributed

The maintainer discovered and reproduced the issue first. Commit `f92d9c200893b023c523011b00d74cabd4c1170e` adds the red regression and recovery requirement while leaving production installer bytes unchanged. A native Qodo Agentic Toolbox 1.6.0 deep review then examined that complete test/documentation change against the frozen public main, with the unchanged installer available in repository context.

Qodo identified the direct-copy loop and absence of recovery, recommended staging and attempt-owned cleanup, pointed out missing partial-copy/preservation tests, and requested actionable user recovery guidance. These are targeted recommendations for a known defect, not blind discovery. Staging and broader recovery tests had already been considered in planning; Qodo corroborated those directions rather than inventing them.

A separate fresh Codex verifier reproduced all three diagnoses, with a documentation qualification: the existing guide already said tests were omitted from the compact archive. It also rejected an unsafe detail in the proposed remedy. On the tested macOS filesystem, plain `os.rename()` replaced an existing empty destination. The final implementation instead acquires each root exclusively and preserves observed conflicts or modified content. The maintainer authored the correction and tests.

The initial provider metadata reports the issue review executed. Compliance, skills, spec, UI, persona and cross-repository reviewers were skipped; spec reported no spec content. Its completed operation does not establish whole-product coverage or the full three-finder Qore method.

The final native issue review examined corrective snapshot `d5a66ce2fbb4328fd279166f3a8f1ab8d636c3f3` and returned three further remarks. Separate verification confirmed a remaining diagnostic defect: an error while scanning staged directories could mask the original copy error. A user-authorized focused follow-up protects that bookkeeping and adds a CLI regression. The staging-location assertions were also strengthened. The exception-wrapper metadata observation remains a nonblocking refinement: the original cause is chained, the supported CLI JSON remains compatible, and this project does not establish a stable Python SDK contract. These distinctions retain the native findings rather than implying a clean provider verdict. The final follow-up receives affected independent checks; no additional Qodo run is claimed for it.

## Reproduce the controlled observation locally

From a full source checkout of this candidate, with Python 3, choose a new output directory:

```sh
python3 -B examples/install-recovery/reproduce.py --output /tmp/qore-recovery-new
```

The [replay helper](../../examples/install-recovery/reproduce.py) builds a verified compact bundle in temporary storage, injects the same second-skill copy failure, attempts an unchanged retry, and runs a normal installation control. It preserves an unrelated policy and records source/installer identities. Temporary installations are removed; only the selected new output directory and its `result.json` persist. It makes no Qodo call and requires no Qodo account.

Expected corrected result: `safe_to_retry: true`, no retained skill paths, a successful retry with three installed skills, no content differences, and the unrelated policy preserved. The earlier source produces a blocked retry. To examine that source, prepare a separate checkout of the frozen base and pass it with `--source`; never replace your current working tree for this replay.

Run the broader local regressions with:

```sh
python3 -B -m unittest discover -s tests -p test_package.py -k install -v
```

Tests include partial file copying, each staging/publication position, final verification, cleanup errors, empty and nonempty destination conflicts, observed edits, generic/derived installation and CLI diagnostics. The full suite includes separately identified browser-dependent skips. These are automated checks and agent verification, not an external human usability trial.

## Attribution and release boundary

Keep the known problem, original Qodo recommendations, independent verdicts, maintainer correction and post-fix observations distinct. Raw provider traces and account identifiers are private and are not bundled here. This candidate, its new presentation and its application text require their own review; no merge, release, endorsement or Ambassador acceptance follows from these tests.
