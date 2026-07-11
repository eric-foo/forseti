# Repo Map Recent Change — Lifecycle Recurrence Telemetry v0

```yaml
retrieval_header_version: 1
artifact_role: Repository-map recent-change note
scope: Routes cold readers to bounded, read-only stale-worktree recurrence telemetry in the existing lane-health detector.
use_when:
  - Comparing worktree and branch recurrence after the 2026-07-11 hygiene closeout.
  - Inspecting stale-over-48-hour lane classifications and their safety guards.
authority_boundary: retrieval_only
open_next:
  - .github/scripts/lane-health-check.ps1
  - docs/workflows/process_improvement_batch0/worktree_lifecycle_audit_v0.md
  - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
```

The existing lane-health detector now emits versioned JSON telemetry for current
worktree and branch counts plus stale-over-48-hour linked-worktree
classifications. Staleness uses the newer of the worktree HEAD commit time and
the mtimes of existing changed or untracked files; ignored files are excluded.
A timestamp more than 300 seconds after observation becomes explicit unknown
evidence.

The expensive lane-local inspection is bounded: one coordinator starts one
sequential owned PowerShell worker for each old lane. On Windows the coordinator
starts a blocked supervisor, assigns it to a kill-on-close Job Object, and only
then releases it to spawn the command. Each internal worker proves membership in
the coordinator's named Job Object before touching Git or the filesystem.
Residual members are terminated on timeout or normal root exit, and the active
job-process count must reach zero before the handle closes. The measured default
monotonic subprocess budget is 45 seconds; worker execution defaults to four
seconds, with containment/drain inside the whole-run budget. Non-Windows
execution aborts before the first telemetry subprocess.

The 2026-07-11 self-test on Windows PowerShell 7.6.3 proved timeout handling,
early-exiting-parent cleanup, inherited-pipe descendant cleanup, exact child-PID
disappearance, and job emptiness. Direct internal-worker invocation failed
closed before Git or filesystem work. A default-budget, freshly fetched-main/
live-PR smoke returned in 31.337 seconds with all 29 commands completed, zero
timeouts, zero failed or unstarted commands, and zero termination failures.
Unknown-age evidence remained empty; three stale records retained incomplete
guard evidence and therefore kept the top-level result incomplete.

Every stale record retains independent open-PR, dirty, ahead/unpushed,
sealed/locked, and unknown evidence. Both network reads are opt-in and read-only:
`-Fetch` refreshes remote refs and `-QueryPullRequests` reads PR state. No
scheduled workflow or cleanup executor was added.

```yaml
direction_change_propagation:
  doctrine_changed: >
    The existing read-only lane-health detector now exposes versioned,
    machine-readable recurrence telemetry for current counts and stale-over-48h
    worktrees. Windows lane-local reads use release-after-assignment Job Object
    supervision with confirmed empty-job closeout, per-worker execution limits,
    and a monotonic whole-run budget. Internal workers prove membership in the
    coordinator's named Job Object before Git or filesystem work; non-Windows
    execution aborts before the first telemetry subprocess. Timeouts, process
    failures, future material timestamps, or missing evidence remain incomplete;
    the detector grants no cleanup authority. Doctrine item 8 now names both
    opt-in network reads: -Fetch and -QueryPullRequests.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
    - validation_philosophy
  controlling_sources_updated:
    - .github/scripts/lane-health-check.ps1
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - docs/workflows/process_improvement_batch0/worktree_lifecycle_audit_v0.md
    - docs/workflows/repo_map_recent_changes/lifecycle_recurrence_telemetry_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/safety-rules.md
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - .github/scripts/spin-up-lane.ps1
  intentionally_not_updated:
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        This remains a local advisory detector, not a commit or CI gate.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: >
        The main map already routes `.github/` to lane health. This low-conflict
        recent-change note records the new comparison surface without appending
        chronology to the main map.
    - path: .github/scripts/spin-up-lane.ps1
      reason: >
        Lane creation and cleanup execution remain outside this read-only
        telemetry outcome; no scheduling, prompt, or cleanup wiring was added.
  stale_language_search: >
    rg -n -i "lane-health|QueryPullRequests|only network action|worktree.*sprawl|worktree.*stale|stale.*worktree|48.?hour"
    AGENTS.md .agents/workflow-overlay docs/decisions
    docs/workflows/process_improvement_batch0 .github/scripts
  stale_language_search_result: >
    Executed after the change. Live authority remains in doctrine items 8 and
    10; the detector, Batch 0 audit, and this route note retain read-only
    classification and independent cleanup guards.
  non_claims:
    - not cleanup, archive, prune, move, or deletion authority
    - not a scheduled workflow or CI gate
    - not validation, readiness, approval, or lifecycle completion
    - a complete classification is not proof that cleanup is safe
    - non-Windows telemetry support; that runtime currently fails closed before subprocess work
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
