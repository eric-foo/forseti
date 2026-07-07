# Forseti Product-Spine Binding Filename Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Bounded filename migration for the search product-lane, Data Lake spine-promotion, and Creator Signal spine-promotion binding records.
use_when:
  - Resolving whether live product/spine binding records still use lowercase `orca_*` filenames.
  - Auditing the family-by-family lowercase filename migration queue.
  - Updating live references to the Forseti product/spine binding records.
authority_boundary: retrieval_only
open_next:
  - docs/migration/forseti_product_spine_binding_filename_migration_v0/moved_paths_index.md
  - docs/workflows/forseti_post_harness_migration_status_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Decision

Migrate the live search product-lane binding, Data Lake spine-promotion binding,
and Creator Signal spine-promotion binding filenames from lowercase `orca_*` to
Forseti filenames, without changing their product/spine semantics, ownership
boundaries, or migration-execution authority.

This batch is re-derived from current `origin/main` after PR #775 (`0af842e5`,
including #753, #755, #756, #757, #758, #759, #760, #763, #765, #767, #768,
#769, #770, #771, #772, #773, #774, and #775). Older migration PRs or worktrees
are reference material only, not merge targets for this filename family.

| Old path | New path | Rule |
| --- | --- | --- |
| `docs/decisions/orca_search_product_lane_binding_v0.md` | `docs/decisions/forseti_search_product_lane_binding_v0.md` | Live search product-lane binding; rename and update live references. |
| `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md` | `docs/decisions/forseti_data_lake_spine_promotion_binding_v0.md` | Live Data Lake spine-promotion binding; rename and update live references. |
| `docs/decisions/orca_creator_signal_spine_promotion_binding_v0.md` | `docs/decisions/forseti_creator_signal_spine_promotion_binding_v0.md` | Live Creator Signal spine-promotion binding; rename and update live references. |

## Compatibility Rule

Historical references to the old filenames remain valid provenance and resolve
through `docs/migration/forseti_product_spine_binding_filename_migration_v0/moved_paths_index.md`.
This lane does not authorize a broad word-match rewrite of remaining `orca_*`
filenames, archived DCP receipt bodies, prior migration evidence, or unrelated
product strategy decision records.

## Non-Claims

- Not validation, readiness, buyer proof, product proof, scan authorization, capture authorization, or feature/build authorization.
- Not a semantic amendment to search-lane scope, Data Lake ownership, Creator Signal ownership, placement doctrine, repo-structure parameters, or artifact-folder authority.
- Not product-root migration, migration execution, package/import/runtime migration, or historical provenance rewrite.
- Not migration of audience, ICP/wedge, consumer-demand, moat, venue, Data Lake derived-retrieval, product-learning specimen, or workflow-discussion filename families.
- Not retirement of `docs/workflows/orca_repo_map_v0.md`, `orca_start_preflight`, `/orca-product-lead`, or other legacy compatibility aliases.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The search product-lane, Data Lake spine-promotion, and Creator Signal
    spine-promotion binding records now use Forseti filenames for the live
    sources, with old paths resolved by a moved-path index; remaining lowercase
    filename families stay separate migration units.
  trigger: lifecycle_boundary
  related_triggers:
    - workflow_authority
    - product_doctrine
    - architecture_doctrine
  controlling_sources_updated:
    - docs/decisions/forseti_product_spine_binding_filename_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/migration/forseti_product_spine_binding_filename_migration_v0/moved_paths_index.md
    - docs/decisions/forseti_search_product_lane_binding_v0.md
    - docs/decisions/forseti_data_lake_spine_promotion_binding_v0.md
    - docs/decisions/forseti_creator_signal_spine_promotion_binding_v0.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/artifact-folders.md
    - docs/decisions/forseti_repo_structure_binding_v0.md
    - docs/decisions/forseti_spine_first_target_structure_binding_v0.md
    - docs/decisions/forseti_spine_first_blocker_authorization_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - forseti/product/README.md
    - forseti/product/spines/data_lake/README.md
    - forseti/product/spines/creator_signal/README.md
    - forseti/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
    - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
    - forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md
  intentionally_not_updated:
    - path: historical prompts, review outputs, review inputs, research snapshots, hygiene handoffs, old migration records, archived DCP receipt bodies, source-pin rows, and source-hash rows
      reason: >
        Those artifacts are provenance, prior migration evidence, or pinned
        source context; old filenames resolve through the moved-path index
        instead of being rewritten.
    - path: docs/decisions/forseti_spine_first_structure_filename_migration_decision_v0.md
      reason: >
        Its old product/spine binding filenames are point-in-time prior-lane
        evidence about what that lane intentionally did not update.
    - path: remaining product strategy and workflow filename families
      reason: >
        Audience, ICP/wedge, consumer-demand, moat, venue, Data Lake
        derived-retrieval, product-learning specimen, and workflow-discussion
        filenames each need their own family-by-family classification.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The legacy repo-map compatibility pointer remains intentionally tracked.
    - path: remaining lowercase `orca_*` filename families
      reason: >
        The migration policy requires family-by-family batches with moved-path
        coverage, not a broad word-match rewrite.
  stale_language_search: >
    rg -n "docs/decisions/orca_(search_product_lane_binding|data_lake_spine_promotion_binding|creator_signal_spine_promotion_binding)_v0.md|orca_(search_product_lane_binding|data_lake_spine_promotion_binding|creator_signal_spine_promotion_binding)_v0.md|orca_(search_product_lane_binding|data_lake_spine_promotion_binding|creator_signal_spine_promotion_binding)_v0"
    .agents docs repo-structure.yaml forseti --glob '!docs/prompts/**'
    --glob '!docs/review-inputs/**' --glob '!docs/review-outputs/**'
    --glob '!docs/research/**' --glob '!docs/hygiene/**'
  non_claims:
    - not validation
    - not readiness
    - not product/spine semantic amendment
    - not broad filename migration
    - not historical artifact rewrite
```