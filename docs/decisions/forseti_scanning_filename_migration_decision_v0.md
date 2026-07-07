# Forseti Scanning Filename Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Bounded filename migration for the scanning core and admissibility/checkability source family.
use_when:
  - Resolving whether the live scanning core and admissibility/checkability files still use lowercase `orca_*` filenames.
  - Auditing the family-by-family lowercase filename migration queue.
  - Updating live references to scan-core, intelligent-walk MGT, demand-gate closures, or scan-gate adjudication surfaces.
authority_boundary: retrieval_only
open_next:
  - docs/migration/forseti_scanning_filename_migration_v0/moved_paths_index.md
  - docs/workflows/forseti_post_harness_migration_status_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Decision

Migrate the live scanning core and admissibility/checkability filename family
from lowercase `orca_*` to Forseti filenames, without touching historical
prompts, review outputs, research snapshots, old migration evidence, archived
DCP receipt bodies, source-pin rows, source-hash rows, or unrelated remaining
`orca_*` filename families.

This batch is re-derived from current `origin/main` after PR #765 (`031eb31d`,
including #753, #755, #756, #757, #758, #759, #760, #763, and #765). Older
migration PRs or worktrees are reference material only, not merge targets for
this filename family.

| Old path | New path | Rule |
| --- | --- | --- |
| `forseti/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md` | `forseti/product/spines/scanning/scan_core/forseti_demand_scan_core_spec_v0.md` | Live proposed scan-core method spec; rename and update live references. |
| `forseti/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md` | `forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md` | Live MGT intelligent-walk operating model; rename and update live references. |
| `forseti/product/spines/scanning/admissibility_checkability/orca_demand_gate_definition_closures_proposal_v0.md` | `forseti/product/spines/scanning/admissibility_checkability/forseti_demand_gate_definition_closures_proposal_v0.md` | Live applied demand-gate definition closures artifact; rename and update live references. |
| `forseti/product/spines/scanning/admissibility_checkability/orca_demand_scan_gate_adjudication_packet_v0.md` | `forseti/product/spines/scanning/admissibility_checkability/forseti_demand_scan_gate_adjudication_packet_v0.md` | Live scan-core/gate-run adjudication packet; rename and update live references. |

## Compatibility Rule

Historical references to the old filenames remain valid provenance and resolve
through `docs/migration/forseti_scanning_filename_migration_v0/moved_paths_index.md`.
For older `orca/product/...` or `docs/product/...` paths, first resolve through
the relevant product-root and repo-structure migration indexes, then apply this
filename successor where applicable. This lane does not authorize a broad
word-match rewrite of remaining `orca_*` filenames.

## Non-Claims

- Not validation, readiness, buyer proof, product proof, scan authorization, capture authorization, or feature/build authorization.
- Not owner adoption of the proposed scan-core method spec or scan-gate adjudication packet.
- Not retirement of `orca_start_preflight` or `/orca-product-lead` compatibility.
- Not a rewrite of historical prompts, review outputs, research snapshots, old migration evidence, archived DCP receipt bodies, source-pin rows, source-hash rows, or unrelated lowercase filename families.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The scanning core and admissibility/checkability filename family now uses
    Forseti filenames for live scanning source files, with old paths resolved by
    a moved-path index; remaining lowercase filename families stay separate
    migration units.
  trigger: lifecycle_boundary
  related_triggers:
    - product_doctrine
    - output_authority
  controlling_sources_updated:
    - docs/decisions/forseti_scanning_filename_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/migration/forseti_scanning_filename_migration_v0/moved_paths_index.md
    - forseti/product/spines/scanning/scan_core/forseti_demand_scan_core_spec_v0.md
    - forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md
    - forseti/product/spines/scanning/admissibility_checkability/forseti_demand_gate_definition_closures_proposal_v0.md
    - forseti/product/spines/scanning/admissibility_checkability/forseti_demand_scan_gate_adjudication_packet_v0.md
  downstream_surfaces_checked:
    - docs/decisions/
    - docs/workflows/forseti_repo_map_v0.md
    - forseti/product/spines/scanning/
    - forseti/product/spines/foundation/
    - forseti/product/spines/judgment/demand_read/
    - forseti/product/spines/capture/core/
    - forseti/product/spines/commission_signal_board/
    - forseti/product/shared/engagement_registry/
  intentionally_not_updated:
    - path: historical prompts, review outputs, review inputs, research snapshots, hygiene handoffs, old migration records, archived DCP receipt bodies, source-pin rows, source-hash rows, and older DCP receipt bodies
      reason: >
        Those artifacts are provenance, prior migration evidence, or pinned
        source context; old filenames resolve through the moved-path index
        instead of being rewritten.
    - path: remaining lowercase `orca_*` filename families
      reason: >
        The migration policy requires family-by-family batches with moved-path
        coverage, not a broad word-match rewrite.
  stale_language_search: >
    rg -n "orca_demand_scan_core_spec_v0|orca_scanning_intelligent_walk_mgt_operating_model_v0|orca_demand_gate_definition_closures_proposal_v0|orca_demand_scan_gate_adjudication_packet_v0"
    .agents docs/decisions docs/workflows docs/migration forseti/product
    forseti-harness/docs --glob '!docs/prompts/**' --glob '!docs/review-inputs/**'
    --glob '!docs/review-outputs/**' --glob '!docs/research/**'
    --glob '!docs/hygiene/**'
  non_claims:
    - not validation
    - not readiness
    - not scan authorization
    - not broad filename migration
    - not historical artifact rewrite
```