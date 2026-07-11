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

## Recurrence observation — 2026-07-11

A fresh fetched-main/live-PR run at `2026-07-11T08:03:52.4552234Z`
observed:

```text
origin_main_ref=fetched
worktrees_total=55
linked_worktrees=54
local_branches=132
branches_merged_into_origin_main=18
stale_over_48h=11
unknown_age=0
unknown_guards=3
classifications=ahead_or_unpushed:5, merged_or_gone_dirty:1, closed_unmerged:2, unknown:3
commands_started=29
commands_completed=29
commands_timed_out=0
commands_failed=0
commands_not_started=0
termination_failures=0
containment_complete=true
wall_seconds=31.337
```

The run used the detector's measured default budgets:

```powershell
pwsh -NoProfile -File .github/scripts/lane-health-check.ps1 -Json `
  -Fetch -QueryPullRequests
```

The 45-second monotonic whole-run budget and four-second worker budget returned
in 31.337 seconds. All 29 requested commands completed, with no timeout,
not-started command, failure, or termination failure.

GitHub PR evidence was available and complete, and `origin/main` was freshly
fetched. No lane retained unknown age evidence. Three stale records retained
incomplete guard evidence, so the command exited 1: incomplete guards remain a
warning and never become cleanup authorization.

The self-test proved timeout classification and two previously missed process
shapes on the current Windows PowerShell 7.6.3 runtime: an early-exiting parent
with a live child, and a child holding inherited output pipes. The coordinator
assigns a blocked supervisor to a kill-on-close Windows Job Object before release,
terminates residual job members on timeout or normal root exit, and confirms the
active job-process count reaches zero before closing the handle. A post-run
command-line census found no live `lane-health-check.ps1`,
`InternalWorktreeProbe`, or lane `status --porcelain` process. Unrelated Codex
background Git reads were not touched.

This is an **observed, volatile recurrence snapshot**. Concurrent lanes can
change every count. It does not attribute the difference from the intake baseline
to cleanup or prove that a stale classification is safe to act on.

## Current bounded read-only route

`.github/scripts/lane-health-check.ps1` now emits the classification above. On
Windows it uses one coordinator, one sequential owned worker per old lane, a
45-second monotonic subprocess budget, a four-second worker execution budget, and
bounded containment/drain inside the whole-run budget. Every internal worker
proves membership in the coordinator's named Job Object before Git or filesystem
work. A timeout, process failure, future timestamp beyond tolerance, missing path,
failed parse, unavailable PR snapshot, or exhausted budget remains explicitly
unknown. Non-Windows execution aborts before the first telemetry subprocess. The
output never names cleanup candidates or grants cleanup authority.

Any later cleanup lane must re-derive live state, use non-force removal, and
preserve every doctrine item 10 guard. This audit grants no cleanup authority.
