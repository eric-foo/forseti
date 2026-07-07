# Forseti Backtest Specimen Filename Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Bounded filename migration for the Unity runtime-fee backtest specimen product artifacts.
use_when:
  - Resolving whether the Unity backtest specimen files still use lowercase Orca filenames.
  - Auditing remaining family-by-family lowercase filename migration work.
  - Updating live references to the retained Unity backtest specimen artifacts.
authority_boundary: retrieval_only
open_next:
  - docs/migration/forseti_backtest_specimen_filename_migration_v0/moved_paths_index.md
  - docs/workflows/forseti_post_harness_migration_status_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Decision

Migrate the retained Unity runtime-fee backtest specimen filenames from
lowercase Orca filenames to Forseti filenames, without changing the sealed
source-packet, memo, or outcome-calibration semantics.

This batch is re-derived from current `origin/main` after PR #781 (`02481922`,
including #753, #755, #756, #757, #758, #759, #760, #763, #765, #767, #768,
#769, #770, #771, #772, #773, #774, #775, #776, #778, #779, #780, and #781).
Older migration PRs or worktrees are reference material only, not merge targets
for this filename family.

| Old path | New path | Rule |
| --- | --- | --- |
| `forseti/product/case_families/product_learning/other_verticals/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md` | `forseti/product/case_families/product_learning/other_verticals/forseti_backtest_specimen_unity_runtime_fee_source_packet_v0.md` | Retained pre-cutoff source-packet specimen; rename file and update live route references while preserving sealed body content. |
| `forseti/product/case_families/product_learning/other_verticals/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md` | `forseti/product/case_families/product_learning/other_verticals/forseti_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md` | Retained sealed at-cutoff memo specimen; rename file and update live route references while preserving sealed body content. |
| `forseti/product/case_families/product_learning/other_verticals/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md` | `forseti/product/case_families/product_learning/other_verticals/forseti_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md` | Retained post-seal outcome-calibration specimen; rename file and update live route references while preserving calibration body content. |

## Compatibility Rule

Historical references to the old filenames remain valid provenance and resolve
through `docs/migration/forseti_backtest_specimen_filename_migration_v0/moved_paths_index.md`.
For older `docs/product/...` paths, first resolve through
`docs/migration/forseti_product_root_migration_v0/moved_paths_index.md`, then
apply this filename successor where applicable.

The artifact bodies intentionally still contain old source-pin paths, source
hashes, sealed-memo references, and pre-rename Orca wording where changing the
text would alter the sealed artifact body or invalidate the point-in-time hash
relationship. This lane updates current navigation and operator-facing file
names; it does not restate the sealed specimen content as newly authored Forseti
analysis.

## Non-Claims

- Not validation, readiness, product proof, method validation, buyer proof, feature/build authorization, or case acceptance.
- Not a semantic amendment to the Unity runtime-fee specimen, sealed memo, outcome calibration, or source packet.
- Not a rewrite of historical prompts, review outputs, research snapshots, old workflow discussions, source-hash rows, source-pin rows, or sealed specimen body text.
- Not migration of unrelated lowercase Orca filenames in prompts, reviews, research, workflows, source-capture records, runtime code, or compatibility wrappers.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The retained Unity runtime-fee backtest specimen files now use Forseti
    filenames, with old paths resolved by a moved-path index. Sealed specimen
    body content, source-pin rows, and source-hash rows remain point-in-time
    provenance rather than newly rewritten Forseti text.
  trigger: lifecycle_boundary
  related_triggers:
    - product_doctrine
    - output_authority
  controlling_sources_updated:
    - docs/decisions/forseti_backtest_specimen_filename_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/migration/forseti_backtest_specimen_filename_migration_v0/moved_paths_index.md
    - forseti/product/case_families/product_learning/other_verticals/forseti_backtest_specimen_unity_runtime_fee_source_packet_v0.md
    - forseti/product/case_families/product_learning/other_verticals/forseti_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md
    - forseti/product/case_families/product_learning/other_verticals/forseti_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md
  downstream_surfaces_checked:
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - forseti-harness/cases/product_learning/cocokind_holdprice_2025_v0/source_provenance_notes_v0.md
    - forseti-harness/cases/product_learning/joahbeauty_cvs_kill_2024_v0/source_provenance_notes_v0.md
    - forseti-harness/cases/product_learning/kinderbeauty_box_pivot_2023_v0/source_provenance_notes_v0.md
    - forseti-harness/cases/product_learning/nueco_fragrance_pivot_v0/source_provenance_notes_v0.md
    - forseti-harness/cases/product_learning/privatepacks_retail_retreat_v0/source_provenance_notes_v0.md
  intentionally_not_updated:
    - path: sealed specimen body text and headings inside the renamed specimen files
      reason: >
        These are point-in-time sealed specimen artifacts with source-packet and
        memo hashes. Rewording the body would create a stronger integrity risk
        than leaving pre-rename wording inside the sealed artifact content.
    - path: legacy docs/product source-pin and source-hash rows
      reason: >
        The rows preserve the original pinned artifact identity and resolve via
        the product-root and backtest-specimen moved-path indexes instead of
        being silently reauthored.
    - path: historical prompts, review outputs, review inputs, research snapshots, hygiene handoffs, old migration records, and workflow discussions
      reason: >
        Those artifacts are provenance or prior discussion records, not live
        route surfaces for this filename family.
    - path: remaining lowercase Orca compatibility names outside this backtest specimen filename family
      reason: >
        The migration policy requires family-by-family batches with moved-path
        coverage, not a broad word-match rewrite.
  stale_language_search: >
    rg -n "orca_backtest_specimen_(unity_runtime_fee_source_packet|memo_unity_runtime_fee_at_cutoff|unity_runtime_fee_outcome_calibration)_v0|forseti/product/case_families/product_learning/other_verticals/orca_backtest_specimen"
    .agents docs repo-structure.yaml forseti forseti-harness --glob '!docs/prompts/**'
    --glob '!docs/review-inputs/**' --glob '!docs/review-outputs/**'
    --glob '!docs/research/**' --glob '!docs/hygiene/**' --glob '!docs/migration/**'
  non_claims:
    - not validation
    - not readiness
    - not semantic amendment
    - not broad filename migration
    - not sealed body rewrite
```