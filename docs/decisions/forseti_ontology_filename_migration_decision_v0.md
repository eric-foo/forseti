# Forseti Ontology Filename Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Bounded filename migration for the ontology foundation family.
use_when:
  - Resolving whether the ontology backbone and ontology GT ladder still use lowercase `orca_*` filenames.
  - Auditing the remaining family-by-family lowercase filename migration queue.
  - Updating live references to the ontology backbone naming authority.
authority_boundary: retrieval_only
open_next:
  - docs/migration/forseti_ontology_filename_migration_v0/moved_paths_index.md
  - docs/workflows/forseti_post_harness_migration_status_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Decision

Migrate the live ontology foundation filename family from lowercase `orca_*` to
Forseti names, without touching historical prompts, review outputs, snapshots, or
old migration evidence.

This batch is re-derived from current `origin/main` after PR #757 (`2141a2ab`,
including #753, #755, and #756). Older migration PRs or worktrees are
reference material only, not merge targets for this filename family.

| Old path | New path | Rule |
| --- | --- | --- |
| `docs/decisions/orca_ontology_gt_foundation_ladder_v0.md` | `docs/decisions/forseti_ontology_gt_foundation_ladder_v0.md` | Live decision/roadmap record; rename and update live references. |
| `forseti/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md` | `forseti/product/spines/foundation/ontology/forseti_ontology_backbone_architecture_v0.md` | Live ontology naming/rationale authority; rename and update live validators, SSOT metadata, cards, and current route references. |

## Compatibility Rule

Historical references to the old filenames remain valid provenance and resolve
through `docs/migration/forseti_ontology_filename_migration_v0/moved_paths_index.md`.
This lane does not authorize a broad word-match rewrite of remaining `orca_*`
filenames. Remaining product-source filename families stay queued for separate
moved-path batches.

## Non-Claims

- Not validation, readiness, buyer proof, product proof, or ontology build authorization.
- Not a broad product-spine filename migration.
- Not retirement of `orca_start_preflight` or `/orca-product-lead` compatibility.
- Not a rewrite of historical prompts, review outputs, snapshots, or old migration evidence.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The ontology foundation filename family now uses Forseti filenames for the
    live ontology GT ladder and ontology backbone authority, with old paths
    resolved by a moved-path index; remaining lowercase filename families stay
    separate migration units.
  trigger: lifecycle_boundary
  related_triggers:
    - architecture_doctrine
    - output_authority
  controlling_sources_updated:
    - docs/decisions/forseti_ontology_filename_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/migration/forseti_ontology_filename_migration_v0/moved_paths_index.md
  downstream_surfaces_checked:
    - .agents/hooks/check_ontology_ssot.py
    - .agents/hooks/check_ontology_expansion.py
    - forseti/product/spines/foundation/ontology/ontology.yaml
    - forseti/product/spines/foundation/ontology/ontology_expansion_backlog_v0.json
    - forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml
    - forseti/product/spines/foundation/ontology/ontology_cards/
    - forseti/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md
  intentionally_not_updated:
    - path: historical prompts, review outputs, review inputs, snapshots, old migration records, and older DCP receipt bodies
      reason: >
        Those artifacts are provenance or prior migration evidence; old filenames
        resolve through the moved-path index instead of being rewritten. The old
        backbone filename also remains in a historical DCP receipt body inside
        `.agents/workflow-overlay/artifact-folders.md`; that receipt is not a live
        route surface.
    - path: remaining lowercase `orca_*` filename families
      reason: >
        The migration policy requires family-by-family batches with moved-path
        coverage, not a broad word-match rewrite.
  stale_language_search: >
    rg -n "orca_ontology_backbone_architecture_v0|orca_ontology_gt_foundation_ladder_v0"
    .agents docs/decisions docs/workflows docs/migration forseti/product --glob
    '!docs/prompts/**' --glob '!docs/review-inputs/**' --glob '!docs/review-outputs/**'
  non_claims:
    - not validation
    - not readiness
    - not broad filename migration
    - not historical artifact rewrite
```
