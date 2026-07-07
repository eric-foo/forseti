# Forseti Data Lake Derived-Retrieval Filename Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Bounded filename migration for the Data Lake derived_retrieval activation proposal authority record.
use_when:
  - Resolving whether the live Data Lake derived_retrieval activation proposal still uses a lowercase `orca_*` filename.
  - Auditing the family-by-family lowercase filename migration queue.
  - Updating live references to the Forseti Data Lake derived_retrieval activation proposal.
authority_boundary: retrieval_only
open_next:
  - docs/migration/forseti_data_lake_derived_retrieval_filename_migration_v0/moved_paths_index.md
  - docs/workflows/forseti_post_harness_migration_status_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Decision

Migrate the live Data Lake derived_retrieval activation proposal filename from
lowercase `orca_*` to a Forseti filename, without changing its proposal status,
derived_retrieval gate semantics, Data Lake architecture posture, or
implementation authority.

This batch is re-derived from current `origin/main` after PR #778 (`8a2a5c18`,
including #753, #755, #756, #757, #758, #759, #760, #763, #765, #767, #768,
#769, #770, #771, #772, #773, #774, #775, #776, and #778). Older migration PRs
or worktrees are reference material only, not merge targets for this filename
family.

| Old path | New path | Rule |
| --- | --- | --- |
| `docs/decisions/orca_data_lake_derived_retrieval_activation_proposal_v0.md` | `docs/decisions/forseti_data_lake_derived_retrieval_activation_proposal_v0.md` | Live Data Lake derived_retrieval activation proposal; rename and update live references. |

The renamed proposal's live `open_next` product-spine paths are also refreshed
from the old `orca/product/` root to the already-migrated `forseti/product/`
root.

## Compatibility Rule

Historical references to the old filename remain valid provenance and resolve
through `docs/migration/forseti_data_lake_derived_retrieval_filename_migration_v0/moved_paths_index.md`.
This lane does not authorize a broad word-match rewrite of remaining `orca_*`
filenames, archived DCP receipt bodies, prompt provenance, research snapshots,
or unrelated product strategy decision records.

## Non-Claims

- Not validation, readiness, buyer proof, product proof, scan authorization, capture authorization, or feature/build authorization.
- Not a semantic amendment to derived_retrieval gate status, Data Lake storage/derived-layout/medallion contracts, query-engine timing, cross-platform identity scope, or implementation authority.
- Not product-root migration, migration execution, package/import/runtime migration, or historical provenance rewrite.
- Not migration of ICP/wedge, consumer-demand, moat, venue, product-learning specimen, workflow-discussion, or remaining filename families.
- Not retirement of `docs/workflows/orca_repo_map_v0.md`, `orca_start_preflight`, `/orca-product-lead`, or other legacy compatibility aliases.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The live Data Lake derived_retrieval activation proposal now uses a Forseti
    filename, with the old path resolved by a moved-path index; remaining
    lowercase filename families stay separate migration units.
  trigger: lifecycle_boundary
  related_triggers:
    - workflow_authority
    - architecture_doctrine
  controlling_sources_updated:
    - docs/decisions/forseti_data_lake_derived_retrieval_filename_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/migration/forseti_data_lake_derived_retrieval_filename_migration_v0/moved_paths_index.md
    - docs/decisions/forseti_data_lake_derived_retrieval_activation_proposal_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
  intentionally_not_updated:
    - path: historical prompts, review outputs, review inputs, research snapshots, hygiene handoffs, old migration records, archived DCP receipt bodies, source-pin rows, and source-hash rows
      reason: >
        Those artifacts are provenance, prior migration evidence, or pinned
        source context; old filenames resolve through the moved-path index
        instead of being rewritten.
    - path: DCP receipt bodies inside forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
      reason: >
        Their old Data Lake proposal filename entries are dated adoption
        provenance from the gate-opening amendment, not live route pointers.
    - path: remaining product strategy and workflow filename families
      reason: >
        ICP/wedge, consumer-demand, moat, venue, product-learning specimen, and
        workflow-discussion filenames each need their own family-by-family
        classification.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The legacy repo-map compatibility pointer remains intentionally tracked.
    - path: remaining lowercase `orca_*` filename families
      reason: >
        The migration policy requires family-by-family batches with moved-path
        coverage, not a broad word-match rewrite.
  stale_language_search: >
    rg -n "docs/decisions/orca_data_lake_derived_retrieval_activation_proposal_v0.md|orca_data_lake_derived_retrieval_activation_proposal_v0"
    .agents docs repo-structure.yaml forseti forseti-harness --glob '!docs/prompts/**'
    --glob '!docs/review-inputs/**' --glob '!docs/review-outputs/**'
    --glob '!docs/research/**' --glob '!docs/hygiene/**'
  non_claims:
    - not validation
    - not readiness
    - not Data Lake semantic amendment
    - not broad filename migration
    - not historical artifact rewrite
```