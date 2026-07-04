# Forseti Repo Map Successor Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Repo-map path successor migration from the legacy Orca map path to the live Forseti map path.
use_when:
  - Choosing the live repo map after the Forseti rename.
  - Deciding whether docs/workflows/orca_repo_map_v0.md is current authority or a compatibility pointer.
  - Continuing the broader Forseti path/package migration after the external identity collision.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/forseti_repo_map_v0.md
  - docs/workflows/orca_repo_map_v0.md
  - docs/decisions/forseti_external_identity_path_migration_decision_v0.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/source-of-truth.md
```

## Start Preflight

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write plus bounded checker/reference patch
  target_scope: Forseti repo-map successor migration
  dirty_state_checked: yes
  blocked_if_missing: docs/decisions/forseti_external_identity_path_migration_decision_v0.md
workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\forseti-repo-map-successor
branch: codex/forseti-repo-map-successor
base_commit_observed: 8edc4ac1 docs: plan Forseti external identity migration (#652)
output_mode: file-write
```

## Decision

`docs/workflows/forseti_repo_map_v0.md` is now the live repo map for current source-pack selection and prompt setup.

`docs/workflows/orca_repo_map_v0.md` remains only as a compatibility pointer so older links, historical receipts, prompts, and review artifacts keep resolving. New live routing, source-loading, checker defaults, and repo-structure entry points should use the Forseti map path.

This lane does not migrate `forseti/product/`, `orca-harness/`, package names, CI check names, skill IDs, or the start-preflight alias.

## External Identity Gate

Before this lane, the external identity cutover was checked first as planned. Current GitHub evidence showed `eric-foo/orca` still exists and `eric-foo/Forseti` already exists as a separate repository with a different GitHub repository id. Therefore the repo slug cutover cannot safely proceed by patching live defaults to `eric-foo/forseti` or by renaming `eric-foo/orca` into an occupied slug.

The external repo identity lane remains owner-gated until the owner chooses what to do with the existing `eric-foo/Forseti` repository.

## What Changed

| Surface | Change |
| --- | --- |
| `docs/workflows/forseti_repo_map_v0.md` | Full live repo map successor. |
| `docs/workflows/orca_repo_map_v0.md` | Compatibility pointer to the live Forseti map. |
| `.agents/hooks/check_map_links.py` | Loads the Forseti map for map/submap coverage checks. |
| `.agents/hooks/check_repo_map_freshness.py` | Treats the Forseti map as the map freshness authority. |
| `.agents/hooks/check_shared_files_dirty.py` | Treats the Forseti map as the commit-once-whole shared map file. |
| `.agents/hooks/header_index.py` | Uses the Forseti map for map-reachability checks. |
| `.agents/hooks/session_context_capsule.py` | Emits the Forseti map as the repo-map entry pointer. |
| `repo-structure.yaml` | Routes docs/workflows entry points to the Forseti map. |
| `.agents/workflow-overlay/source-loading.md` | Uses the Forseti map in the default read order and S1 map pack. |
| `.agents/workflow-overlay/source-of-truth.md` | Names the Forseti map as the bounded source-pack navigation map. |

## Compatibility Boundary

The old map path is intentionally not deleted. Removing it would convert historical and provenance references into broken links while adding no operational value. The compatibility pointer is the rollback surface for older artifacts; the live map path is the forward surface for new work.

Remaining `docs/workflows/orca_repo_map_v0.md` references are valid only when they are historical/provenance references, old-link compatibility, or references to the pointer itself. New live instructions should use `docs/workflows/forseti_repo_map_v0.md`.

## Non-Claims

- This decision is not validation, readiness, source-of-truth promotion, implementation authorization, or proof that the repo map is complete.
- This decision does not migrate product roots, harness roots, package/import names, CI check names, skill IDs, or historical prompt/review artifacts.
- This decision does not perform the GitHub repo rename, local checkout rename, or remote URL change.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The live repo map path moved from docs/workflows/orca_repo_map_v0.md to
    docs/workflows/forseti_repo_map_v0.md; the old Orca path remains only as a
    compatibility pointer for older links and historical references.
  trigger: lifecycle_boundary
  related_triggers:
    - workflow_authority
    - validation_philosophy
  controlling_sources_updated:
    - docs/decisions/forseti_repo_map_successor_migration_decision_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
  downstream_surfaces_checked:
    - AGENTS.md
    - README.md
    - repo-structure.yaml
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/hooks/check_map_links.py
    - .agents/hooks/check_repo_map_freshness.py
    - .agents/hooks/check_shared_files_dirty.py
    - .agents/hooks/header_index.py
    - .agents/hooks/session_context_capsule.py
    - .agents/hooks/check_full_gt_claims.py
    - .agents/hooks/check_handoff_pointers.py
    - docs/workflows/artifact_retrievability_guide.md
    - docs/workflows/repo_map_recent_changes/README.md
    - docs/decisions/forseti_rename_migration_policy_v0.md
    - docs/decisions/forseti_compatibility_migration_boundary_v0.md
    - docs/decisions/forseti_external_identity_path_migration_decision_v0.md
  intentionally_not_updated:
    - path: historical DCP receipt bodies, prompts, review outputs, and dated migration reports
      reason: >
        They are point-in-time provenance. The compatibility pointer keeps their
        links resolvable without rewriting history.
    - path: forseti/product/ and orca-harness/
      reason: >
        Product and harness root migration remain separate high-lock-in lanes.
    - path: eric-foo/orca hard-coded repo slug surfaces
      reason: >
        The target Forseti slug is occupied by a separate repository, so the
        external identity cutover remains owner-gated.
  stale_language_search: >
    rg -n -F "docs/workflows/orca_repo_map_v0.md" AGENTS.md README.md
    repo-structure.yaml .agents/hooks .agents/workflow-overlay docs/workflows/forseti_repo_map_v0.md
    docs/workflows/orca_repo_map_v0.md docs/decisions/forseti_rename_migration_policy_v0.md
    docs/decisions/forseti_compatibility_migration_boundary_v0.md
    docs/decisions/forseti_external_identity_path_migration_decision_v0.md
  non_claims:
    - not validation
    - not readiness
    - not source-of-truth promotion
    - not implementation authorization
```