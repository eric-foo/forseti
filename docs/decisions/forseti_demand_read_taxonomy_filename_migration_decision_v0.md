# Forseti Demand-Read Taxonomy Filename Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Bounded filename migration for the demand-read taxonomy family.
use_when:
  - Resolving whether the live demand-read taxonomy files still use lowercase `orca_*` filenames.
  - Auditing the family-by-family lowercase filename migration queue.
  - Updating live references to the demand-read taxonomy or its adjudication companion.
authority_boundary: retrieval_only
open_next:
  - docs/migration/forseti_demand_read_taxonomy_filename_migration_v0/moved_paths_index.md
  - docs/workflows/forseti_post_harness_migration_status_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Decision

Migrate the live demand-read taxonomy filename family from lowercase `orca_*`
to Forseti filenames, without touching historical prompts, review outputs,
research snapshots, old migration evidence, source-pin rows, or legacy
source-hash rows.

This batch is re-derived from current `origin/main` after PR #760 (`04330574`,
including #753, #755, #756, #757, #758, #759, and #760). Older migration PRs or
worktrees are reference material only, not merge targets for this filename
family.

| Old path | New path | Rule |
| --- | --- | --- |
| `forseti/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md` | `forseti/product/spines/foundation/demand_read_taxonomy/forseti_demand_read_taxonomy_v0.md` | Live proposed demand-read grammar; rename and update live references. |
| `forseti/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_adjudication_v0.md` | `forseti/product/spines/foundation/demand_read_taxonomy/forseti_demand_read_taxonomy_adjudication_v0.md` | Live adjudication-prep companion; rename and update live references. |

## Compatibility Rule

Historical references to the old filenames remain valid provenance and resolve
through `docs/migration/forseti_demand_read_taxonomy_filename_migration_v0/moved_paths_index.md`.
For older `orca/product/...` paths, first resolve through
`docs/migration/forseti_product_root_migration_v0/moved_paths_index.md`, then
apply this filename successor where applicable. This lane does not authorize a
broad word-match rewrite of remaining `orca_*` filenames.

## Non-Claims

- Not validation, readiness, buyer proof, product proof, scan authorization, capture authorization, or feature/build authorization.
- Not adoption of the PROPOSED demand-read taxonomy.
- Not retirement of `orca_start_preflight` or `/orca-product-lead` compatibility.
- Not a rewrite of historical prompts, review outputs, research snapshots, old migration evidence, source-pin rows, source-hash rows, or older DCP receipt bodies.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The demand-read taxonomy filename family now uses Forseti filenames for the
    live proposed demand-read grammar and adjudication-prep companion, with old
    paths resolved by a moved-path index; remaining lowercase filename families
    stay separate migration units.
  trigger: lifecycle_boundary
  related_triggers:
    - product_doctrine
    - output_authority
  controlling_sources_updated:
    - docs/decisions/forseti_demand_read_taxonomy_filename_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/migration/forseti_demand_read_taxonomy_filename_migration_v0/moved_paths_index.md
    - forseti/product/spines/foundation/demand_read_taxonomy/forseti_demand_read_taxonomy_v0.md
    - forseti/product/spines/foundation/demand_read_taxonomy/forseti_demand_read_taxonomy_adjudication_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/foundation/ontology/
    - forseti/product/spines/scanning/
    - forseti/product/spines/judgment/demand_read/
    - forseti/product/spines/capture/core/demand_durability_indicators/
    - forseti/product/spines/product_lead/buyer_proof/
    - forseti/product/shared/engagement_registry/
    - forseti/product/satellites/beauty/
    - docs/workflows/forseti_repo_map_v0.md
  intentionally_not_updated:
    - path: historical prompts, review outputs, review inputs, research snapshots, hygiene handoffs, old migration records, source-pin rows, source-hash rows, and older DCP receipt bodies
      reason: >
        Those artifacts are provenance, prior migration evidence, or pinned
        source context; old filenames resolve through the moved-path index
        instead of being rewritten.
    - path: remaining lowercase `orca_*` filename families
      reason: >
        The migration policy requires family-by-family batches with moved-path
        coverage, not a broad word-match rewrite.
  stale_language_search: >
    rg -n "orca_demand_read_taxonomy(_adjudication)?_v0" .agents docs/decisions
    docs/workflows docs/migration forseti/product forseti-harness/docs --glob
    '!docs/prompts/**' --glob '!docs/review-inputs/**' --glob '!docs/review-outputs/**'
    --glob '!docs/research/**' --glob '!docs/hygiene/**'
  non_claims:
    - not validation
    - not readiness
    - not taxonomy adoption
    - not broad filename migration
    - not historical artifact rewrite
```
