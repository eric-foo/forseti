# Safety Rules

```yaml
retrieval_header_version: 1
artifact_role: Forseti overlay authority
scope: Project-specific safety rules, forbidden drift, authorization boundaries, and rollback limits for Forseti work.
use_when:
  - Checking whether an action is forbidden drift or needs explicit authorization (implementation, runtime, commit, push, external-folder, or skill edits).
  - Confirming fail-visible behavior, scope discipline, or rollback boundaries before acting.
authority_boundary: retrieval_only
```

## Project-Specific Safety

- Fail visibly when required Forseti authority is missing.
- Do not substitute `jb` paths, product facts, lifecycle rules, or validation gates.
- Do not create software implementation, runtime systems, packages, tests, deployed automation, or source-system buildout unless the current turn or an accepted Forseti decision explicitly authorizes a bounded implementation scope.
- Bounded implementation authorization is not blanket runtime authority. Stay inside the named scope, preserve the bounded third-tranche scope for anti-detect/proxy/JS-challenge work, and preserve separate gates for commercial fetch services, storage, dashboards, deployment, ECR, Cleaning, Judgment, commits, pushes, and PRs.
- Do not mutate external reference folders during import planning.
- Do not edit installed global skills, user-level skills, plugin cache files, or external workflow source unless a later turn explicitly authorizes it.
- For current data-lake work, resolve the operational root through the canonical
  Forseti locator (`FORSETI_DATA_ROOT`, or an explicit root verified by the
  current Forseti root contract). `F:\orca-data-lake`, `ORCA_DATA_ROOT`,
  `.orca-*` markers, and `orca-harness` commands found in dated prompts,
  handoffs, reviews, or receipts are legacy provenance or compatibility
  vocabulary, not executable current-root instructions. If a routed artifact
  supplies only a legacy locator, stop before any lake read or write and reload
  `docs/workflows/forseti_data_lake_rename_execution_closeout_handoff_v0.md`
  plus `forseti-harness/data_lake/root.py`; do not silently target or recreate
  the old physical root. Compatibility handling inside current Forseti code is
  unchanged by this agent-facing rule.
- Forseti-local candidate skill drafting or iteration may proceed only through the
  controlled lane in `.agents/workflow-overlay/skill-adoption.md`. That lane
  does not authorize global, user-level, plugin, installed, or external workflow
  source mutation.
- Treat credential failure and sandbox or network denial as different claims.
  Before asking the owner to reauthenticate, repeat the smallest read-only
  authentication check through the approved GitHub-action route. Ask only when
  that independent check reports missing or invalid credentials; never print
  credentials or tokens.
- Do not configure remotes or perform destructive cleanup unless explicitly authorized. Commit, push, pull-request preparation, and merge follow `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`: at verified completion of a repo-changing work unit on the lane's own branch or worktree they proceed without a typed instruction, owner-gated by the harness permission prompts. The lane author self-merges only its own PR after all required validation, review return, and adjudication are complete; an explicit owner hold, unverifiable completion, foreign authorship, or any guard/server refusal fails closed to a human landing. The guard (`.agents/hooks/guard_protected_actions.py`) is the enforcement.
- **Online/external source-data capture routes through the Source Capture Armory Runner Ladder.** Any capture of online or external source data for evidence or learning goes through the armory runners + Mini God-Tier source-quality discipline (the "Runner Ladder"), not ad-hoc web fetches; captures emit inspectable Source Capture Packets that also serve as Capture-lane data. Route via the repo map (`docs/workflows/forseti_repo_map_v0.md` -> Data Capture / Source Capture Armory submap) -> `forseti-harness/docs/source_capture_agent_runbook.md` + `forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md`. Uncaptured scouting/diagnostic web reads (not entered as evidence) are exempt.

## Scope Discipline

**Smallest complete intervention** -- and the interpretation of any "smallest
complete X" phrasing (fix, patch, edit, rewrite, refactor, review, answer) -- is
defined canonically in `AGENTS.md` § "Smallest Complete Intervention". That
definition is repo-wide and all-agent; this overlay defers to it and does not
restate it. The overlay's only role here is to apply that rule to Forseti scope
discipline: bounded intervention, justified adjacency, and no speculative
extras.

## Rollback Boundary

Rollback for this bootstrap is additive: remove the newly created Forseti directory only with explicit user approval. No rollback step may edit `jb`, installed skills, user-level skills, plugin skills, or external reference folders.
