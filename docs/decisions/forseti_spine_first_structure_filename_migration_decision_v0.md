# Forseti Spine-First Structure Filename Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Bounded filename migration for the spine-first target-structure binding and blocker-authorization records.
use_when:
  - Resolving whether the live spine-first structure records still use lowercase `orca_*` filenames.
  - Auditing the family-by-family lowercase filename migration queue.
  - Updating live references to the Forseti spine-first structure records.
authority_boundary: retrieval_only
open_next:
  - docs/migration/forseti_spine_first_structure_filename_migration_v0/moved_paths_index.md
  - docs/workflows/forseti_post_harness_migration_status_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Decision

Migrate the live spine-first target-structure binding and blocker-authorization
filenames from lowercase `orca_*` to Forseti filenames, without changing the
spine-first target semantics, placement rules, migration-execution authority, or
historical product-root provenance.

This batch is re-derived from current `origin/main` after PR #774 (`a95d441c`,
including #753, #755, #756, #757, #758, #759, #760, #763, #765, #767, #768,
#769, #770, #771, #772, #773, and #774). Older migration PRs or worktrees are
reference material only, not merge targets for this filename family.

| Old path | New path | Rule |
| --- | --- | --- |
| `docs/decisions/orca_spine_first_target_structure_binding_v0.md` | `docs/decisions/forseti_spine_first_target_structure_binding_v0.md` | Live spine-first target-structure binding; rename and update live references. |
| `docs/decisions/orca_spine_first_blocker_authorization_v0.md` | `docs/decisions/forseti_spine_first_blocker_authorization_v0.md` | Live spine-first blocker authorization; rename and update live references. |

## Compatibility Rule

Historical references to the old filenames remain valid provenance and resolve
through `docs/migration/forseti_spine_first_structure_filename_migration_v0/moved_paths_index.md`.
This lane does not authorize a broad word-match rewrite of remaining `orca_*`
filenames or a root-path content rewrite of historical `orca/product/` evidence.

## Non-Claims

- Not validation, readiness, buyer proof, product proof, scan authorization, capture authorization, or feature/build authorization.
- Not a semantic amendment to the spine-first target tree, blocker settlements, placement doctrine, repo-structure parameters, or artifact-folder authority.
- Not migration execution, product-root migration, or retirement of historical `orca/product/` provenance.
- Not migration of the search-lane, data-lake, creator-signal, ICP/wedge, audience, moat, venue, or workflow-discussion filename families.
- Not retirement of `docs/workflows/orca_repo_map_v0.md`, `orca_start_preflight`, `/orca-product-lead`, or other legacy compatibility aliases.
- Not a rewrite of historical prompts, review outputs, research snapshots, old migration evidence, archived DCP receipt bodies, source-pin rows, source-hash rows, or unrelated lowercase filename families.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The spine-first target-structure binding and blocker-authorization records
    now use Forseti filenames for the live sources, with old paths resolved by a
    moved-path index; remaining lowercase filename families stay separate
    migration units.
  trigger: lifecycle_boundary
  related_triggers:
    - workflow_authority
    - architecture_doctrine
    - output_authority
  controlling_sources_updated:
    - docs/decisions/forseti_spine_first_structure_filename_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/migration/forseti_spine_first_structure_filename_migration_v0/moved_paths_index.md
    - docs/decisions/forseti_spine_first_target_structure_binding_v0.md
    - docs/decisions/forseti_spine_first_blocker_authorization_v0.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/artifact-folders.md
    - forseti/product/README.md
    - forseti/product/spines/data_lake/README.md
    - docs/decisions/forseti_repo_structure_binding_v0.md
    - docs/decisions/orca_search_product_lane_binding_v0.md
    - docs/decisions/orca_data_lake_spine_promotion_binding_v0.md
    - docs/decisions/orca_creator_signal_spine_promotion_binding_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
  intentionally_not_updated:
    - path: historical prompts, review outputs, review inputs, research snapshots, hygiene handoffs, old migration records, archived DCP receipt bodies, source-pin rows, and source-hash rows
      reason: >
        Those artifacts are provenance, prior migration evidence, or pinned
        source context; old filenames resolve through the moved-path index
        instead of being rewritten.
    - path: historical `orca/product/` body evidence inside spine-first records
      reason: >
        This lane migrates filenames and live reference surfaces only. Product
        root compatibility is already covered by the product-root moved-path
        index and should not be rewritten as a side effect of this filename pair.
    - path: remaining product-spine and decision-record filename families
      reason: >
        Search-lane, data-lake, creator-signal, ICP/wedge, audience, moat,
        venue, and workflow-discussion filenames each need their own
        family-by-family classification.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The legacy repo-map compatibility pointer remains intentionally tracked.
    - path: remaining lowercase `orca_*` filename families
      reason: >
        The migration policy requires family-by-family batches with moved-path
        coverage, not a broad word-match rewrite.
  stale_language_search: >
    rg -n "docs/decisions/orca_spine_first_(target_structure_binding|blocker_authorization)_v0.md|orca_spine_first_(target_structure_binding|blocker_authorization)_v0.md|orca_spine_first_(target_structure_binding|blocker_authorization)_v0"
    .agents docs repo-structure.yaml forseti --glob '!docs/prompts/**'
    --glob '!docs/review-inputs/**' --glob '!docs/review-outputs/**'
    --glob '!docs/research/**' --glob '!docs/hygiene/**'
  non_claims:
    - not validation
    - not readiness
    - not target-tree amendment
    - not product-root content rewrite
    - not broad filename migration
    - not historical artifact rewrite
```