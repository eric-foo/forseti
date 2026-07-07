# Forseti Commission Signal Board Filename Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Bounded filename migration for the Commission Signal Board source family.
use_when:
  - Resolving whether live Commission Signal Board source files still use lowercase `orca_*` filenames.
  - Auditing the family-by-family lowercase filename migration queue.
  - Updating live references to the CSB Prompt Structure, Prompt Structure Rules, or legacy non-controlling gate-run criteria surfaces.
authority_boundary: retrieval_only
open_next:
  - docs/migration/forseti_commission_signal_board_filename_migration_v0/moved_paths_index.md
  - docs/workflows/forseti_post_harness_migration_status_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Decision

Migrate the live Commission Signal Board filename family from lowercase
`orca_*` to Forseti filenames, without touching historical prompts, review
outputs, research snapshots, old migration evidence, archived DCP receipt
bodies, source-pin rows, source-hash rows, or unrelated remaining `orca_*`
filename families.

This batch is re-derived from current `origin/main` after PR #767 (`f6346932`,
including #753, #755, #756, #757, #758, #759, #760, #763, #765, and #767).
Older migration PRs or worktrees are reference material only, not merge targets
for this filename family.

| Old path | New path | Rule |
| --- | --- | --- |
| `forseti/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_structure_rules_v0.md` | `forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md` | Live CSB Prompt Structure Rules authority surface; rename and update live references. |
| `forseti/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_structure_v0.md` | `forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md` | Live reusable CSB Prompt Structure surface; rename and update live references. |
| `forseti/product/spines/commission_signal_board/dispatch_rules/orca_demand_gate_run_commission_criteria_v0.md` | `forseti/product/spines/commission_signal_board/dispatch_rules/forseti_demand_gate_run_commission_criteria_v0.md` | Legacy non-controlling CSB-adjacent gate-run criteria retained in the live CSB spine; rename the operator-facing file while preserving its historical content boundary. |

## Compatibility Rule

Historical references to the old filenames remain valid provenance and resolve
through `docs/migration/forseti_commission_signal_board_filename_migration_v0/moved_paths_index.md`.
For older `orca/product/...` or `docs/product/...` paths, first resolve through
the relevant product-root and repo-structure migration indexes, then apply this
filename successor where applicable. This lane does not authorize a broad
word-match rewrite of remaining `orca_*` filenames.

## Non-Claims

- Not validation, readiness, buyer proof, product proof, scan authorization, capture authorization, or feature/build authorization.
- Not owner adoption of the CSB Prompt Structure or any demand-gate run criteria.
- Not retirement of `orca_start_preflight`, `/orca-product-lead`, or other legacy compatibility aliases.
- Not a rewrite of historical prompts, review outputs, research snapshots, old migration evidence, archived DCP receipt bodies, source-pin rows, source-hash rows, or unrelated lowercase filename families.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The Commission Signal Board filename family now uses Forseti filenames for
    live CSB source files, with old paths resolved by a moved-path index;
    remaining lowercase filename families stay separate migration units.
  trigger: lifecycle_boundary
  related_triggers:
    - product_doctrine
    - output_authority
  controlling_sources_updated:
    - docs/decisions/forseti_commission_signal_board_filename_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/migration/forseti_commission_signal_board_filename_migration_v0/moved_paths_index.md
    - forseti/product/spines/commission_signal_board/README.md
    - forseti/product/spines/commission_signal_board/spine.yaml
    - forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md
    - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
    - forseti/product/spines/commission_signal_board/dispatch_rules/forseti_demand_gate_run_commission_criteria_v0.md
    - .agents/hooks/check_commission_signal_board_output.py
  downstream_surfaces_checked:
    - docs/decisions/
    - docs/workflows/forseti_repo_map_v0.md
    - forseti/product/spines/commission_signal_board/
    - forseti/product/spines/scanning/admissibility_checkability/forseti_demand_scan_gate_adjudication_packet_v0.md
    - forseti/product/spines/judgment/demand_read/
    - forseti/product/shared/engagement_registry/
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
    rg -n "orca_commission_signal_board_prompt_structure_rules_v0|orca_commission_signal_board_prompt_structure_v0|orca_demand_gate_run_commission_criteria_v0"
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