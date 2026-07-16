# Batch 0 Worktree Lifecycle Audit v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow validation note
scope: Read-only baseline and failure classification for branch/worktree lifecycle accumulation.
use_when:
  - Interpreting the retired Batch 0 lifecycle probe and its read-only classifier evidence.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  - .github/scripts/lane-health-check.ps1
  - .github/scripts/spin-up-lane.ps1
```

## Baseline — 2026-07-11

Fresh read after creating the isolated Batch 0 lane:

```text
worktrees_total=214
linked_worktrees=213
local_branches=376
branches_merged_into_main=110
```

A second fresh read later in the same turn observed concurrent lifecycle change:

```text
worktrees_total=211
linked_worktrees=210
local_branches=376
branches_merged_into_main=108
```

Commands used: `git worktree list --porcelain`, `git for-each-ref refs/heads`,
and `git branch --merged main`. Counts are volatile and must be freshly derived
before any cleanup decision.

At task intake, a combined whole-repository status/count command emitted its
counts but timed out after 40 seconds while traversing the dirty shared tree.
This is an observed operating-cost signal, not proof of the cause.

## Initial failure classification

| Signal | Classification | Evidence | Current implication |
| --- | --- | --- | --- |
| More than 200 linked worktrees versus detector default threshold 4 | consequential accumulation | `.github/scripts/lane-health-check.ps1` | Containment is not working at the intended bound. |
| Lane-start helper prints `git worktree remove --force` | safety-contract conflict candidate | `.github/scripts/spin-up-lane.ps1` versus non-force rule in `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md` | Do not execute the printed cleanup command; route a separate fix. |
| Cleanup is actor/instruction carried | firing unknown | doctrine item 10 and current counts | Audit invocation and refusal reasons before adding automation. |
| Dirty/open/unpushed/sealed lanes may legitimately resist cleanup | mixed legitimate residue | doctrine item 10 guards | Classify before removing; count alone cannot authorize deletion. |

## Next bounded read-only step

Classify every linked worktree into: open PR, merged/gone and clean, merged/gone
but dirty, closed-unmerged, ahead/unpushed, sealed/protected, or unknown. Do not
remove anything in this audit. A later cleanup lane must re-derive live state,
use non-force removal, and preserve all doctrine guards.

## Read-only classification — 2026-07-12

The bounded lifecycle-latency lane extended
`.github/scripts/lane-health-check.ps1` with a read-only classifier and ran it
from an isolated clean worktree after `git fetch --prune origin` plus one
repository-wide GitHub PR-state read. The run classified all linked worktrees
without deleting, moving, staging, committing, pushing, or changing a branch.

Fresh observed summary (`2026-07-11T16:56:56.4081582Z`):

```text
linked_worktrees=71
elapsed_seconds=7.356
open_pr=14
merged_gone_clean=8
merged_gone_dirty=6
closed_unmerged=3
ahead_unpushed=6
unknown=34
cleanup_candidates=8
```

The earlier 211-linked-worktree baseline and this 71-linked-worktree observation
were taken at different times while other lanes were active. This lane performed
no cleanup, so it does not claim to have caused the reduction.

A first classifier run identified 12 candidates. Fresh inspection exposed a
missing safety condition: `[gone]` alone cannot prove that the local branch did
not move after its PR. Requiring the local worktree HEAD to equal the latest
merged PR head reduced the candidate set to eight and reclassified the mismatches
as `ahead_unpushed`. The guard is now covered by the script selftest.

Independent review added two further fail-closed conditions: a gone upstream
must be exactly `origin/<branch>`, and only PRs whose head belongs to the
origin repository participate in classification. Any open or closed-unmerged PR
history takes precedence over merged history, and classification refuses when the
2,000-row query boundary makes completeness unproven.

Fresh guarded candidate set from that observation:

| Branch | Worktree | Merged PR |
| --- | --- | --- |
| `claude/repo-map-assessment-a24aa2` | `C:/Users/vmon7/Desktop/projects/orca/.claude/worktrees/repo-map-assessment-a24aa2` | #856 |
| `codex/amazon-capture-latency-session` | `C:/tmp/orca-amazon-capture-latency-session` | #865 |
| `codex/batch0-pr860-receipt` | `C:/Users/vmon7/Desktop/projects/orca/worktrees/batch0-pr860-receipt` | #863 |
| `codex/behavioral-ceremony-reduction` | `C:/Users/vmon7/Desktop/projects/orca/worktrees/behavioral-ceremony-reduction` | #871 |
| `codex/forseti-data-root-default` | `C:/Users/vmon7/Desktop/projects/orca/worktrees/forseti-data-root-default` | #860 |
| `codex/problem-integrity-compression` | `C:/Users/vmon7/Desktop/projects/orca/worktrees/problem-integrity-compression` | #861 |
| `codex/retail-walmart-target-projection-ecr-cleaning-reroot` | `C:/Users/vmon7/.codex/worktrees/2d1c/orca` | #859 |
| `codex/tiktok-grid-video-selection` | `C:/Users/vmon7/Desktop/projects/orca/orca-worktrees/tiktok-grid-video-selection` | #867 |

This table is volatile evidence, not cleanup authority. Any later cleanup must
re-run the classifier, use non-force `git worktree remove`, and preserve every
doctrine guard. This patch does not execute doctrine item 10's lane-start sweep
or branch-only cleanup; those remain actor-carried behavioral rules. The
classifier only prepares live evidence for a separately guarded action. The
same patch removes the unsafe `--force` instruction from
`.github/scripts/spin-up-lane.ps1`; that implementation is not durable on
`main` until its lane PR lands.

## Closeout — 2026-07-17

`closed`.

Keep the read-only, fail-closed classifier in
`.github/scripts/lane-health-check.ps1`. Retire this probe without installing an
automatic cleanup schedule, an age or count deletion rule, or a standing audit.
Every candidate table above is volatile historical evidence, not current state
or cleanup authority. Future cleanup remains a separately authorized guarded
action that must re-derive live state and preserve untracked and dirty work.
