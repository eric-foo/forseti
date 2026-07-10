# Batch 0 Worktree Lifecycle Audit v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow validation note
scope: Read-only baseline and failure classification for branch/worktree lifecycle accumulation.
use_when:
  - Assessing whether lane-start cleanup and lane closeout contain repository sprawl.
  - Scoping a separately authorized lifecycle cleanup or enforcement fix.
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
