# Forseti Product-Strategy Filename Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Bounded filename migration for the remaining live product-strategy decision records under `docs/decisions/orca_*_v0.md`.
use_when:
  - Resolving whether product-strategy decision records still use lowercase `orca_*` filenames.
  - Auditing the family-by-family lowercase filename migration queue.
  - Updating live references to the Forseti consumer-demand, ICP/wedge, moat proof-path, and venue-registry decision records.
authority_boundary: retrieval_only
open_next:
  - docs/migration/forseti_product_strategy_filename_migration_v0/moved_paths_index.md
  - docs/workflows/forseti_post_harness_migration_status_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Decision

Migrate the remaining live product-strategy decision filenames from lowercase
`orca_*` to Forseti filenames, without changing their owner-decision outcomes,
supersession semantics, ICP/wedge posture, moat proof-path posture,
venue-registry rejection, or implementation authority.

This batch is re-derived from current `origin/main` after PR #779 (`c63dece0`,
including #753, #755, #756, #757, #758, #759, #760, #763, #765, #767, #768,
#769, #770, #771, #772, #773, #774, #775, #776, #778, and #779). Older
migration PRs or worktrees are reference material only, not merge targets for
this filename family.

| Old path | New path | Rule |
| --- | --- | --- |
| `docs/decisions/orca_consumer_demand_ratification_decision_memo_v0.md` | `docs/decisions/forseti_consumer_demand_ratification_decision_memo_v0.md` | Live consumer-demand owner-decision memo; rename and update live references. |
| `docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md` | `docs/decisions/forseti_icp_wedge_consumer_demand_first_v0.md` | Current first-proof ICP/wedge authority; rename and update live references. |
| `docs/decisions/orca_icp_wedge_convergence_break_in_first_v0.md` | `docs/decisions/forseti_icp_wedge_convergence_break_in_first_v0.md` | Historical superseded ICP/wedge predecessor retained as a live decision record; rename and update live references. |
| `docs/decisions/orca_icp_wedge_pricing_first_v0.md` | `docs/decisions/forseti_icp_wedge_pricing_first_v0.md` | Superseded pricing-first wedge authority retained as method/history anchor; rename and update live references. |
| `docs/decisions/orca_moat_judgment_quality_proof_path_decision_chain_v0.md` | `docs/decisions/forseti_moat_judgment_quality_proof_path_decision_chain_v0.md` | Live moat/judgment-quality proof-path decision-chain capture; rename and update live references. |
| `docs/decisions/orca_venue_registry_rejection_decision_v0.md` | `docs/decisions/forseti_venue_registry_rejection_decision_v0.md` | Live venue-registry rejection owner-decision record; rename and update live references. |

## Compatibility Rule

Historical references to the old filenames remain valid provenance and resolve
through `docs/migration/forseti_product_strategy_filename_migration_v0/moved_paths_index.md`.
This lane does not authorize a broad word-match rewrite of remaining `orca_*`
filenames outside this product-strategy decision family, archived DCP receipt
bodies, prompt provenance, source-pin/hash rows, research snapshots, or
unrelated product-tree filenames.

## Non-Claims

- Not validation, readiness, buyer proof, product proof, scan authorization, capture authorization, or feature/build authorization.
- Not a semantic amendment to consumer-demand ratification, ICP/wedge ordering, pricing-first supersession, moat proof-path posture, venue-registry rejection, or owner-decision effects.
- Not product-root migration, migration execution, package/import/runtime migration, or historical provenance rewrite.
- Not migration of product-tree `orca_*` filenames, workflow-discussion filenames, source-hash keys, prompt files, review outputs, research files, or compatibility aliases.
- Not retirement of `docs/workflows/orca_repo_map_v0.md`, `orca_start_preflight`, `/orca-product-lead`, or other legacy compatibility aliases.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The remaining live product-strategy decision records under
    `docs/decisions/orca_*_v0.md` now use Forseti filenames, with old paths
    resolved by a moved-path index; product-tree `orca_*` filenames and other
    compatibility surfaces remain separate migration units.
  trigger: lifecycle_boundary
  related_triggers:
    - workflow_authority
    - product_doctrine
    - architecture_doctrine
  controlling_sources_updated:
    - docs/decisions/forseti_product_strategy_filename_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/migration/forseti_product_strategy_filename_migration_v0/moved_paths_index.md
    - docs/decisions/forseti_consumer_demand_ratification_decision_memo_v0.md
    - docs/decisions/forseti_icp_wedge_consumer_demand_first_v0.md
    - docs/decisions/forseti_icp_wedge_convergence_break_in_first_v0.md
    - docs/decisions/forseti_icp_wedge_pricing_first_v0.md
    - docs/decisions/forseti_moat_judgment_quality_proof_path_decision_chain_v0.md
    - docs/decisions/forseti_venue_registry_rejection_decision_v0.md
  downstream_surfaces_checked:
    - .agents/skills/forseti-product-lead/SKILL.md
    - .agents/workflow-overlay/artifact-folders.md
    - docs/decisions/forseti_product_thesis_consumer_demand_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - forseti/product/spines/product_lead/offer/forseti_offer_hypothesis_v0.md
    - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md
    - forseti/product/spines/product_lead/proof_charter/forseti_product_proof_lead_charter_v0.md
    - forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md
  intentionally_not_updated:
    - path: historical prompts, review outputs, review inputs, research snapshots, hygiene handoffs, old migration records, archived DCP receipt bodies, source-pin rows, and source-hash rows
      reason: >
        Those artifacts are provenance, prior migration evidence, or pinned
        source context; old filenames resolve through the moved-path index
        instead of being rewritten.
    - path: product-tree filenames under forseti/product/spines/product_lead/icp_wedge/orca_*.md
      reason: >
        Those filenames are a separate compatibility family; this lane updates
        their live references to the renamed decision records where safe but
        does not rename the product-tree files themselves.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The legacy repo-map compatibility pointer remains intentionally tracked.
    - path: remaining lowercase `orca_*` compatibility names outside docs/decisions
      reason: >
        The migration policy requires family-by-family batches with moved-path
        coverage, not a broad word-match rewrite.
  stale_language_search: >
    rg -n "docs/decisions/orca_(consumer_demand_ratification_decision_memo|icp_wedge_consumer_demand_first|icp_wedge_convergence_break_in_first|icp_wedge_pricing_first|moat_judgment_quality_proof_path_decision_chain|venue_registry_rejection_decision)_v0.md|orca_(consumer_demand_ratification_decision_memo|icp_wedge_consumer_demand_first|icp_wedge_convergence_break_in_first|icp_wedge_pricing_first|moat_judgment_quality_proof_path_decision_chain|venue_registry_rejection_decision)_v0"
    .agents docs repo-structure.yaml forseti forseti-harness --glob '!docs/prompts/**'
    --glob '!docs/review-inputs/**' --glob '!docs/review-outputs/**'
    --glob '!docs/research/**' --glob '!docs/hygiene/**' --glob '!docs/migration/**'
  non_claims:
    - not validation
    - not readiness
    - not product-strategy semantic amendment
    - not broad filename migration
    - not historical artifact rewrite
```