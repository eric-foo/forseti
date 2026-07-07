# Forseti Product-Lead Authority Filename Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Bounded filename migration for the product-lead authority family.
use_when:
  - Resolving whether the core product-lead authority files still use lowercase `orca_*` filenames.
  - Auditing the remaining family-by-family lowercase filename migration queue.
  - Updating live references to the product thesis, offer, buyer proof, proof charter, or claim-defense doctrine.
authority_boundary: retrieval_only
open_next:
  - docs/migration/forseti_product_lead_authority_filename_migration_v0/moved_paths_index.md
  - docs/workflows/forseti_post_harness_migration_status_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Decision

Migrate the live product-lead authority filename family from lowercase `orca_*`
to Forseti filenames, without touching historical prompts, review outputs,
research snapshots, old migration evidence, or legacy `docs/product/...` source
hash/source-pin rows.

This batch is re-derived from current `origin/main` after PR #758 (`650e0e81`,
including #753, #755, #756, #757, and #758). Older migration PRs or worktrees are
reference material only, not merge targets for this filename family.

| Old path | New path | Rule |
| --- | --- | --- |
| `docs/decisions/orca_product_thesis_consumer_demand_v0.md` | `docs/decisions/forseti_product_thesis_consumer_demand_v0.md` | Live owner-ratified product thesis; rename and update live references. |
| `forseti/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md` | `forseti/product/spines/product_lead/offer/forseti_offer_hypothesis_v0.md` | Live offer hypothesis; rename and update live references. |
| `forseti/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md` | `forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md` | Live buyer-proof packet; rename and update live references. |
| `forseti/product/spines/product_lead/proof_charter/orca_product_proof_lead_charter_v0.md` | `forseti/product/spines/product_lead/proof_charter/forseti_product_proof_lead_charter_v0.md` | Live product-proof charter; rename and update live references. |
| `forseti/product/spines/product_lead/proof_charter/orca_claim_defense_doctrine_v0.md` | `forseti/product/spines/product_lead/proof_charter/forseti_claim_defense_doctrine_v0.md` | Live external-claims policy; rename and update live references. |

## Compatibility Rule

Historical references to the old filenames remain valid provenance and resolve
through `docs/migration/forseti_product_lead_authority_filename_migration_v0/moved_paths_index.md`.
For older `orca/product/...` paths, first resolve through
`docs/migration/forseti_product_root_migration_v0/moved_paths_index.md`, then
apply this filename successor where applicable. This lane does not authorize a
broad word-match rewrite of remaining `orca_*` filenames.

## Non-Claims

- Not validation, readiness, buyer proof, product proof, or feature/build authorization.
- Not a broad product-lead filename migration.
- Not retirement of `orca_start_preflight` or `/orca-product-lead` compatibility.
- Not a rewrite of historical prompts, review outputs, research snapshots, old migration evidence, or legacy source-hash/source-pin rows.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The product-lead authority filename family now uses Forseti filenames for the
    live product thesis, offer hypothesis, buyer-proof packet, product-proof
    charter, and claim-defense doctrine, with old paths resolved by a moved-path
    index; remaining lowercase filename families stay separate migration units.
  trigger: lifecycle_boundary
  related_triggers:
    - product_doctrine
    - output_authority
  controlling_sources_updated:
    - docs/decisions/forseti_product_lead_authority_filename_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/migration/forseti_product_lead_authority_filename_migration_v0/moved_paths_index.md
    - docs/decisions/forseti_product_thesis_consumer_demand_v0.md
    - forseti/product/spines/product_lead/offer/forseti_offer_hypothesis_v0.md
    - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md
    - forseti/product/spines/product_lead/proof_charter/forseti_product_proof_lead_charter_v0.md
    - forseti/product/spines/product_lead/proof_charter/forseti_claim_defense_doctrine_v0.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/project-authority.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/artifact-roles.md
    - .agents/skills/forseti-product-lead/SKILL.md
    - forseti/product/spines/product_lead/
    - forseti/product/spines/commission_signal_board/
    - forseti/product/spines/scanning/
    - forseti/product/spines/judgment/
    - forseti/product/
    - docs/workflows/forseti_repo_map_v0.md
  intentionally_not_updated:
    - path: historical prompts, review outputs, review inputs, research snapshots, hygiene handoffs, old migration records, source-hash/source-pin rows, and older DCP receipt bodies
      reason: >
        Those artifacts are provenance, prior migration evidence, or pinned
        source-hash/source-pin context; old filenames resolve through the moved-path index
        instead of being rewritten.
    - path: remaining lowercase `orca_*` filename families
      reason: >
        The migration policy requires family-by-family batches with moved-path
        coverage, not a broad word-match rewrite.
  stale_language_search: >
    rg -n "orca_product_thesis_consumer_demand_v0|orca_offer_hypothesis_v0|orca_buyer_proof_packet_v0|orca_product_proof_lead_charter_v0|orca_claim_defense_doctrine_v0"
    .agents docs/decisions docs/workflows docs/migration forseti/product forseti-harness/docs --glob
    '!docs/prompts/**' --glob '!docs/review-inputs/**' --glob '!docs/review-outputs/**' --glob
    '!docs/research/**' --glob '!docs/hygiene/**'
  non_claims:
    - not validation
    - not readiness
    - not broad filename migration
    - not historical artifact rewrite
```
