# Forseti Capture Core Filename Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Bounded filename migration for the Capture-core architecture filename family.
use_when:
  - Resolving whether live Capture-core architecture source files still use lowercase `orca_*` filenames.
  - Auditing the family-by-family lowercase filename migration queue.
  - Updating live references to the Capture projection storage spine, creator momentum pipeline, or creator monitoring policy surfaces.
authority_boundary: retrieval_only
open_next:
  - docs/migration/forseti_capture_core_filename_migration_v0/moved_paths_index.md
  - docs/workflows/forseti_post_harness_migration_status_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Decision

Migrate the live Capture-core architecture filename family from lowercase
`orca_*` to Forseti filenames, without touching historical prompts, review
outputs, research snapshots, old migration evidence, archived DCP receipt
bodies, source-pin rows, source-hash rows, or unrelated remaining `orca_*`
filename families.

This batch is re-derived from current `origin/main` after PR #769 (`89d15cbd`,
including #753, #755, #756, #757, #758, #759, #760, #763, #765, #767, #768,
and #769). Older migration PRs or worktrees are reference material only, not
merge targets for this filename family.

| Old path | New path | Rule |
| --- | --- | --- |
| `forseti/product/spines/capture/core/operating_model/orca_capture_projection_storage_spine_architecture_v0.md` | `forseti/product/spines/capture/core/operating_model/forseti_capture_projection_storage_spine_architecture_v0.md` | Live Capture projection storage spine architecture surface; rename and update live references. |
| `forseti/product/spines/capture/core/source_families/social_media/instagram/orca_creator_momentum_pipeline_architecture_v0.md` | `forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_momentum_pipeline_architecture_v0.md` | Live IG creator-momentum pipeline architecture surface; rename and update live references. |
| `forseti/product/spines/capture/core/source_families/social_media/instagram/orca_creator_monitoring_policy_architecture_v0.md` | `forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_monitoring_policy_architecture_v0.md` | Live creator monitoring policy architecture surface; rename and update live references. |

## Compatibility Rule

Historical references to the old filenames remain valid provenance and resolve
through `docs/migration/forseti_capture_core_filename_migration_v0/moved_paths_index.md`.
For older `orca/product/...` or `docs/product/...` paths, first resolve through
the relevant product-root and repo-structure migration indexes, then apply this
filename successor where applicable. This lane does not authorize a broad
word-match rewrite of remaining `orca_*` filenames.

## Non-Claims

- Not validation, readiness, buyer proof, product proof, scan authorization, capture authorization, or feature/build authorization.
- Not owner adoption of the Capture projection storage spine, creator-momentum pipeline, or creator monitoring policy.
- Not retirement of `orca_start_preflight`, `/orca-product-lead`, or other legacy compatibility aliases.
- Not a rewrite of historical prompts, review outputs, research snapshots, old migration evidence, archived DCP receipt bodies, source-pin rows, source-hash rows, or unrelated lowercase filename families.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The Capture-core architecture filename family now uses Forseti filenames for
    live source files, with old paths resolved by a moved-path index; remaining
    lowercase filename families stay separate migration units.
  trigger: lifecycle_boundary
  related_triggers:
    - product_doctrine
    - output_authority
  controlling_sources_updated:
    - docs/decisions/forseti_capture_core_filename_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/migration/forseti_capture_core_filename_migration_v0/moved_paths_index.md
    - forseti/product/spines/capture/core/operating_model/forseti_capture_projection_storage_spine_architecture_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_momentum_pipeline_architecture_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_monitoring_policy_architecture_v0.md
    - forseti/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/instagram/README.md
  downstream_surfaces_checked:
    - forseti/product/spines/capture/core/
    - forseti/product/spines/creator_signal/
    - forseti/product/spines/commission_signal_board/
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
  intentionally_not_updated:
    - path: historical prompts, review outputs, review inputs, research snapshots, hygiene handoffs, old migration records, archived DCP receipt bodies, source-pin rows, source-hash rows, and older DCP receipt bodies
      reason: >
        Those artifacts are provenance, prior migration evidence, or pinned
        source context; old filenames resolve through the moved-path index
        instead of being rewritten.
    - path: older Orca-named decision records
      reason: >
        Existing `docs/decisions/orca_*` settlement records preserve prior path
        and decision context. This lane updates current live references and adds
        a successor index rather than rewriting old decision provenance.
    - path: orca_start_preflight
      reason: >
        Start-preflight alias retirement is a separate compatibility lane; this
        filename migration does not change accepted prompt preflight aliases.
    - path: remaining lowercase `orca_*` filename families
      reason: >
        The migration policy requires family-by-family batches with moved-path
        coverage, not a broad word-match rewrite.
  stale_language_search: >
    rg -n "orca_capture_projection_storage_spine_architecture_v0|orca_creator_momentum_pipeline_architecture_v0|orca_creator_monitoring_policy_architecture_v0"
    .agents docs/decisions docs/workflows docs/migration forseti/product
    forseti-harness/docs --glob '!docs/prompts/**' --glob '!docs/review-inputs/**'
    --glob '!docs/review-outputs/**' --glob '!docs/research/**'
    --glob '!docs/hygiene/**'
  non_claims:
    - not validation
    - not readiness
    - not capture authorization
    - not broad filename migration
    - not historical artifact rewrite
```
