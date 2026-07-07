# Forseti Audience Taxonomy Filename Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Bounded filename migration for the audience ballot taxonomy and Tier-2-A prior table authority records.
use_when:
  - Resolving whether live audience taxonomy authority records still use lowercase `orca_*` filenames.
  - Auditing the family-by-family lowercase filename migration queue.
  - Updating live references to the Forseti audience taxonomy and Tier-2-A prior records.
authority_boundary: retrieval_only
open_next:
  - docs/migration/forseti_audience_taxonomy_filename_migration_v0/moved_paths_index.md
  - docs/workflows/forseti_post_harness_migration_status_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Decision

Migrate the live audience-inference ballot taxonomy and Tier-2-A base-rate
prior table filenames from lowercase `orca_*` to Forseti filenames, without
changing their audience-inference semantics, Tier-1/Tier-2-A boundary, source
verification posture, or implementation authority.

This batch is re-derived from current `origin/main` after PR #776 (`45b5888a`,
including #753, #755, #756, #757, #758, #759, #760, #763, #765, #767, #768,
#769, #770, #771, #772, #773, #774, #775, and #776). Older migration PRs or
worktrees are reference material only, not merge targets for this filename
family.

| Old path | New path | Rule |
| --- | --- | --- |
| `docs/decisions/orca_audience_ballot_taxonomy_v0.md` | `docs/decisions/forseti_audience_ballot_taxonomy_v0.md` | Live audience-inference ballot taxonomy authority; rename and update live references. |
| `docs/decisions/orca_audience_tier2a_base_rate_prior_table_v0.md` | `docs/decisions/forseti_audience_tier2a_base_rate_prior_table_v0.md` | Live Tier-2-A base-rate prior table authority; rename and update live references. |

The Tier-2-A table's local live version label changes from
`orca-tier2a-beauty-prior-us-0.1.0` to
`forseti-tier2a-beauty-prior-us-0.1.0`; no other dependency on the old label was
observed in this branch. The audience taxonomy record's live `open_next`
harness paths are also refreshed to the already-migrated `forseti-harness/`
root.

## Compatibility Rule

Historical references to the old filenames remain valid provenance and resolve
through `docs/migration/forseti_audience_taxonomy_filename_migration_v0/moved_paths_index.md`.
This lane does not authorize a broad word-match rewrite of remaining `orca_*`
filenames, archived DCP receipt bodies, prompt provenance, research snapshots,
or unrelated product strategy decision records.

## Non-Claims

- Not validation, readiness, buyer proof, product proof, scan authorization, capture authorization, or feature/build authorization.
- Not a semantic amendment to the Tier-1 ballot taxonomy, canonical labels, Tier-2-A carve-out, demographic-prior posture, source verification, or audience-inference implementation.
- Not product-root migration, migration execution, package/import/runtime migration, or historical provenance rewrite.
- Not migration of ICP/wedge, consumer-demand, moat, venue, Data Lake derived-retrieval, product-learning specimen, workflow-discussion, or remaining filename families.
- Not retirement of `docs/workflows/orca_repo_map_v0.md`, `orca_start_preflight`, `/orca-product-lead`, or other legacy compatibility aliases.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The live audience-inference ballot taxonomy and Tier-2-A prior table records
    now use Forseti filenames, with old paths resolved by a moved-path index;
    remaining lowercase filename families stay separate migration units.
  trigger: lifecycle_boundary
  related_triggers:
    - workflow_authority
    - product_doctrine
    - architecture_doctrine
  controlling_sources_updated:
    - docs/decisions/forseti_audience_taxonomy_filename_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/migration/forseti_audience_taxonomy_filename_migration_v0/moved_paths_index.md
    - docs/decisions/forseti_audience_ballot_taxonomy_v0.md
    - docs/decisions/forseti_audience_tier2a_base_rate_prior_table_v0.md
    - forseti-harness/schemas/audience_label_ontology.py
    - forseti/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
  downstream_surfaces_checked:
    - docs/decisions/forseti_creator_signal_spine_promotion_binding_v0.md
    - forseti-harness/schemas/audience_label_ontology.py
    - forseti/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
  intentionally_not_updated:
    - path: historical prompts, review outputs, review inputs, research snapshots, hygiene handoffs, old migration records, archived DCP receipt bodies, source-pin rows, and source-hash rows
      reason: >
        Those artifacts are provenance, prior migration evidence, or pinned
        source context; old filenames resolve through the moved-path index
        instead of being rewritten.
    - path: docs/decisions/forseti_creator_signal_spine_promotion_binding_v0.md
      reason: >
        Its old audience-taxonomy filename appears inside a dated DCP receipt
        body for the Creator Signal promotion lane, not as a live route.
    - path: docs/prompts/deep-thinking/orca_audience_ballot_bucket_taxonomy_prompt_v0.md and docs/prompts/deep-thinking/orca_audience_tier2a_*.md
      reason: >
        Prompt artifacts are historical provenance by default and remain under
        their original Orca filenames unless a later prompt-authority batch
        explicitly migrates them.
    - path: remaining product strategy and workflow filename families
      reason: >
        ICP/wedge, consumer-demand, moat, venue, Data Lake derived-retrieval,
        product-learning specimen, and workflow-discussion filenames each need
        their own family-by-family classification.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The legacy repo-map compatibility pointer remains intentionally tracked.
    - path: remaining lowercase `orca_*` filename families
      reason: >
        The migration policy requires family-by-family batches with moved-path
        coverage, not a broad word-match rewrite.
  stale_language_search: >
    rg -n "docs/decisions/orca_audience_(ballot_taxonomy|tier2a_base_rate_prior_table)_v0.md|orca_audience_(ballot_taxonomy|tier2a_base_rate_prior_table)_v0|orca-tier2a-beauty-prior-us-0.1.0"
    .agents docs repo-structure.yaml forseti forseti-harness --glob '!docs/prompts/**'
    --glob '!docs/review-inputs/**' --glob '!docs/review-outputs/**'
    --glob '!docs/research/**' --glob '!docs/hygiene/**'
  non_claims:
    - not validation
    - not readiness
    - not audience-inference semantic amendment
    - not broad filename migration
    - not historical artifact rewrite
```