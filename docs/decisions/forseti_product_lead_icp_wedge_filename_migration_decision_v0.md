# Forseti Product-Lead ICP/Wedge Filename Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Bounded filename migration for the live product-lead ICP/wedge product artifacts under `forseti/product/spines/product_lead/icp_wedge/orca_*_v0.md`.
use_when:
  - Resolving whether product-lead ICP/wedge artifacts still use lowercase `orca_*` filenames.
  - Auditing the family-by-family lowercase filename migration queue.
  - Updating live references to the Forseti product-lead ICP/wedge product artifacts.
authority_boundary: retrieval_only
open_next:
  - docs/migration/forseti_product_lead_icp_wedge_filename_migration_v0/moved_paths_index.md
  - docs/workflows/forseti_post_harness_migration_status_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Decision

Migrate the live product-lead ICP/wedge product artifact filenames from
lowercase `orca_*` to Forseti filenames, without changing their product
outcomes, supersession semantics, ratification status, discovery authority,
source pins, prompt provenance, or implementation authority.

This batch is re-derived from current `origin/main` after PR #780 (`2a684620`,
including #753, #755, #756, #757, #758, #759, #760, #763, #765, #767, #768,
#769, #770, #771, #772, #773, #774, #775, #776, #778, #779, and #780). Older
migration PRs or worktrees are reference material only, not merge targets for
this filename family.

| Old path | New path | Rule |
| --- | --- | --- |
| `forseti/product/spines/product_lead/icp_wedge/orca_discovery_batch_0_candidate_context_scan_v0.md` | `forseti/product/spines/product_lead/icp_wedge/forseti_discovery_batch_0_candidate_context_scan_v0.md` | Superseded candidate-context scan retained as historical product artifact; rename and update live references. |
| `forseti/product/spines/product_lead/icp_wedge/orca_discovery_batch_0_qualification_prep_sentry_clerk_v0.md` | `forseti/product/spines/product_lead/icp_wedge/forseti_discovery_batch_0_qualification_prep_sentry_clerk_v0.md` | Superseded qualification-prep artifact retained as historical product artifact; rename and update live references. |
| `forseti/product/spines/product_lead/icp_wedge/orca_discovery_batch_0_target_selection_brief_v0.md` | `forseti/product/spines/product_lead/icp_wedge/forseti_discovery_batch_0_target_selection_brief_v0.md` | Superseded target-selection brief retained as historical product artifact; rename and update live references. |
| `forseti/product/spines/product_lead/icp_wedge/orca_discovery_consumer_demand_target_selection_brief_v0.md` | `forseti/product/spines/product_lead/icp_wedge/forseti_discovery_consumer_demand_target_selection_brief_v0.md` | Live consumer-demand target-selection instrument; rename and update live references. |
| `forseti/product/spines/product_lead/icp_wedge/orca_icp_ratification_readiness_report_v0.md` | `forseti/product/spines/product_lead/icp_wedge/forseti_icp_ratification_readiness_report_v0.md` | Ratification-readiness report retained as advisory product-planning artifact; rename and update live references. |
| `forseti/product/spines/product_lead/icp_wedge/orca_product_lead_first_icp_wedge_decision_v0.md` | `forseti/product/spines/product_lead/icp_wedge/forseti_product_lead_first_icp_wedge_decision_v0.md` | Superseded first ICP/wedge product artifact retained as historical product artifact; rename and update live references. |
| `forseti/product/spines/product_lead/icp_wedge/orca_ratification_day_runbook_v0.md` | `forseti/product/spines/product_lead/icp_wedge/forseti_ratification_day_runbook_v0.md` | Executed ratification-day runbook retained as product-planning artifact; rename and update live references. |

## Compatibility Rule

Historical references to the old filenames remain valid provenance and resolve
through `docs/migration/forseti_product_lead_icp_wedge_filename_migration_v0/moved_paths_index.md`.
This lane does not authorize a broad word-match rewrite of prompts, review
artifacts, research snapshots, archived DCP receipt bodies, source-pin/hash
rows, legacy `docs/product/` source keys, or unrelated lowercase `orca_*`
filenames.

## Non-Claims

- Not validation, readiness, buyer proof, product proof, scan authorization, capture authorization, outreach authorization, prompt retirement, or feature/build authorization.
- Not a semantic amendment to the consumer-demand ratification, ICP/wedge order, discovery status, pricing-first supersession, or owner-decision effects.
- Not product-root migration, package/import/runtime migration, historical provenance rewrite, or compatibility-wrapper retirement.
- Not migration of prompt files, review outputs, research files, source-hash keys, DCP receipt bodies, `.agents/skills/orca-product-lead`, `.claude/skills/orca-product-lead`, or `orca_start_preflight`.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The live product-lead ICP/wedge product artifacts under
    `forseti/product/spines/product_lead/icp_wedge/orca_*_v0.md` now use
    Forseti filenames, with old paths resolved by a moved-path index; prompts,
    wrappers, source-hash rows, and unrelated lowercase filenames remain
    separate migration units.
  trigger: lifecycle_boundary
  related_triggers:
    - workflow_authority
    - product_doctrine
  controlling_sources_updated:
    - docs/decisions/forseti_product_lead_icp_wedge_filename_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/migration/forseti_product_lead_icp_wedge_filename_migration_v0/moved_paths_index.md
    - forseti/product/spines/product_lead/icp_wedge/forseti_discovery_batch_0_candidate_context_scan_v0.md
    - forseti/product/spines/product_lead/icp_wedge/forseti_discovery_batch_0_qualification_prep_sentry_clerk_v0.md
    - forseti/product/spines/product_lead/icp_wedge/forseti_discovery_batch_0_target_selection_brief_v0.md
    - forseti/product/spines/product_lead/icp_wedge/forseti_discovery_consumer_demand_target_selection_brief_v0.md
    - forseti/product/spines/product_lead/icp_wedge/forseti_icp_ratification_readiness_report_v0.md
    - forseti/product/spines/product_lead/icp_wedge/forseti_product_lead_first_icp_wedge_decision_v0.md
    - forseti/product/spines/product_lead/icp_wedge/forseti_ratification_day_runbook_v0.md
  downstream_surfaces_checked:
    - .agents/skills/forseti-product-lead/SKILL.md
    - .claude/skills/forseti-product-lead/SKILL.md
    - docs/decisions/forseti_consumer_demand_ratification_decision_memo_v0.md
    - docs/decisions/forseti_icp_wedge_consumer_demand_first_v0.md
    - docs/decisions/forseti_icp_wedge_convergence_break_in_first_v0.md
    - docs/decisions/forseti_icp_wedge_pricing_first_v0.md
    - docs/decisions/forseti_product_thesis_consumer_demand_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md
    - forseti/product/spines/foundation/ontology/forseti_ontology_backbone_architecture_v0.md
    - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md
    - forseti/product/spines/product_lead/offer/forseti_offer_hypothesis_v0.md
    - forseti/product/spines/product_lead/proof_charter/forseti_product_proof_lead_charter_v0.md
    - forseti/product/spines/scanning/admissibility_checkability/forseti_demand_gate_definition_closures_proposal_v0.md
    - forseti/product/spines/scanning/admissibility_checkability/forseti_demand_scan_gate_adjudication_packet_v0.md
    - forseti/product/spines/scanning/scan_core/forseti_demand_scan_core_spec_v0.md
  intentionally_not_updated:
    - path: historical prompts, review outputs, review inputs, research snapshots, hygiene handoffs, old migration records, archived DCP receipt bodies, source-pin rows, and source-hash rows
      reason: >
        Those artifacts are provenance, prior migration evidence, or pinned
        source context; old filenames resolve through the moved-path index
        instead of being rewritten.
    - path: compatibility product-lead skill wrapper directories
      reason: >
        Compatibility wrappers remain a separate transition-window decision.
    - path: remaining lowercase orca-star compatibility names outside this product-lead ICP/wedge filename family
      reason: >
        The migration policy requires family-by-family batches with moved-path
        coverage, not a broad word-match rewrite.
  stale_language_search: >
    rg -n "forseti/product/spines/product_lead/icp_wedge/orca_(discovery_batch_0_candidate_context_scan|discovery_batch_0_qualification_prep_sentry_clerk|discovery_batch_0_target_selection_brief|discovery_consumer_demand_target_selection_brief|icp_ratification_readiness_report|product_lead_first_icp_wedge_decision|ratification_day_runbook)_v0.md|orca_(discovery_batch_0_candidate_context_scan|discovery_batch_0_qualification_prep_sentry_clerk|discovery_batch_0_target_selection_brief|discovery_consumer_demand_target_selection_brief|icp_ratification_readiness_report|product_lead_first_icp_wedge_decision|ratification_day_runbook)_v0"
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