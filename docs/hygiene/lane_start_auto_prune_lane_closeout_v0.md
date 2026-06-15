---
retrieval_header_version: 1
artifact_role: Hygiene closeout log (durable record of the lane-start auto-prune lane and the cascade it surfaced)
scope: >
  One-page record of what the lane-start auto-prune lane shipped, the dev-workflow
  cascade it surfaced while closing out (red main, broken auto-merge bot), and the
  worktree/branch sweeps performed. Provenance only; not validation or readiness.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  - docs/hygiene/lane_start_auto_prune_rule_handoff_v0.md
---

# Lane-Start Auto-Prune Lane — Closeout Log v0

Durable record of the lane that adopted the lane-start auto-prune rule and the
follow-on work it surfaced. Provenance only.

## What shipped (all merged to main)

- **Decision item 10 — lane-start auto-prune rule** (PR #104). Agent-instruction-only
  standing rule: at each new lane's start, `git fetch --prune origin`, then non-force
  `git worktree remove` of `[gone]`-branch worktrees with no open PR, then `git branch -D`
  those `[gone]` branches (worktree-bound and branch-only). Load-bearing guards inline:
  non-force only; exclude open-PR worktrees; never the seal or any `[ahead]`-unpushed
  worktree; glance for closed-unmerged before `-D`; re-derive live every time.
- **Decision item 11 — standing self-label policy** (PR #109). The lane author applies
  the existing opt-in `agent-automerge` marker by default for routine low-risk changes
  it judges safe to land unattended, and withholds it (owner review) for enforcement/
  safety surfaces, contested doctrine, high lock-in, or uncertainty. No new merge
  authority; author judgment, not a path Action.
- **Cold handoff packet** (PR #103) — `docs/hygiene/lane_start_auto_prune_rule_handoff_v0.md`,
  the intake artifact this lane continued from.

## Cascade surfaced while closing out (not the auto-prune lane's own content)

- **Red main fixed** (PR #116). `demand_durability_capture_pilot_v0.md` `open_next`
  pointed to non-existent `demand_proxy_*` files (the profiles were named
  `demand_durability_indicator_*`); `check_map_links.py --strict` failed, turning
  `push:main` CI red. Repointed the two paths. Red-green proven (2 findings/exit 1 ->
  0 findings/exit 0). A parallel lane (PR #117) fixed the same drift independently.
- **Auto-merge bot fixed** (PR #118). The bot (item 9) failed every evaluation with
  `GraphQL: Resource not accessible by integration` on `statusCheckRollup ->
  checkSuite.workflowRun`; its `permissions:` block lacked `actions: read`. Added it
  (least-privilege). Before this, the bot had never completed an unattended merge.

## Hygiene

- Worktree/branch sweeps removed merged `[gone]` residue under the item-10 guards
  (non-force; seal, `[ahead]`, open-PR, and dirty worktrees excluded).
- `orca-r6-rescan-commission-wt` was held (non-force remove refused it — untracked
  content), which is the safety guard behaving as designed.

## Non-claims

- Provenance/record only — not validation, readiness, or acceptance of any content.
- Items 10/11 are behavioral rules, "live" only insofar as agents follow them; no
  proven long-run bound on worktree/branch count is asserted.
