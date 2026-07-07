# Forseti Vertical Exploration Filename Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Bounded filename migration for the vertical-exploration and case-finder frame family.
use_when:
  - Resolving whether the live vertical-exploration procedure files still use lowercase `orca_*` filenames.
  - Auditing the family-by-family lowercase filename migration queue.
  - Updating live references to the vertical-exploration guide or memorization-resistant case-finder frame.
authority_boundary: retrieval_only
open_next:
  - docs/migration/forseti_vertical_exploration_filename_migration_v0/moved_paths_index.md
  - docs/workflows/forseti_post_harness_migration_status_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Decision

Migrate the live vertical-exploration filename family from lowercase `orca_*`
to Forseti filenames, without touching historical prompts, review outputs,
research snapshots, old migration evidence, source-pin rows, source-hash rows,
older DCP receipt bodies, or unrelated remaining `orca_*` filename families.

This batch is re-derived from current `origin/main` after PR #763 (`f0ce5b14`,
including #753, #755, #756, #757, #758, #759, #760, and #763). Older migration
PRs or worktrees are reference material only, not merge targets for this
filename family.

| Old path | New path | Rule |
| --- | --- | --- |
| `forseti/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md` | `forseti/product/spines/foundation/vertical_exploration/forseti_vertical_exploration_guide_v0.md` | Live WHERE-side vertical-exploration procedure; rename and update live references. |
| `forseti/product/spines/foundation/vertical_exploration/orca_memorization_resistant_case_finder_frame_v0.md` | `forseti/product/spines/foundation/vertical_exploration/forseti_memorization_resistant_case_finder_frame_v0.md` | Live memorization-resistant case-finder doctrine frame; rename and update live references. |

## Compatibility Rule

Historical references to the old filenames remain valid provenance and resolve
through `docs/migration/forseti_vertical_exploration_filename_migration_v0/moved_paths_index.md`.
For older `orca/product/...` or `docs/product/core_spine/...` paths, first
resolve through the relevant product-root and repo-structure migration indexes,
then apply this filename successor where applicable. This lane does not
authorize a broad word-match rewrite of remaining `orca_*` filenames.

## Non-Claims

- Not validation, readiness, buyer proof, product proof, scan authorization, capture authorization, or feature/build authorization.
- Not owner sign-off of the proposed case-finder doctrine frame.
- Not retirement of `orca_start_preflight` or `/orca-product-lead` compatibility.
- Not a rewrite of historical prompts, review outputs, research snapshots, old migration evidence, source-pin rows, source-hash rows, older DCP receipt bodies, or unrelated lowercase filename families.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The vertical-exploration filename family now uses Forseti filenames for the
    live WHERE-side procedure and memorization-resistant case-finder frame, with
    old paths resolved by a moved-path index; remaining lowercase filename
    families stay separate migration units.
  trigger: lifecycle_boundary
  related_triggers:
    - product_doctrine
    - output_authority
  controlling_sources_updated:
    - docs/decisions/forseti_vertical_exploration_filename_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/migration/forseti_vertical_exploration_filename_migration_v0/moved_paths_index.md
    - forseti/product/spines/foundation/vertical_exploration/forseti_vertical_exploration_guide_v0.md
    - forseti/product/spines/foundation/vertical_exploration/forseti_memorization_resistant_case_finder_frame_v0.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/source-loading.md
    - docs/decisions/
    - docs/workflows/forseti_repo_map_v0.md
    - forseti/product/spines/scanning/
    - forseti/product/spines/capture/core/source_capture_toolbox/
    - forseti/product/satellites/
    - forseti/product/case_families/
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
    rg -n "orca_vertical_exploration_guide_v0|orca_memorization_resistant_case_finder_frame_v0"
    .agents docs/decisions docs/workflows docs/migration forseti/product
    forseti-harness/docs --glob '!docs/prompts/**' --glob '!docs/review-inputs/**'
    --glob '!docs/review-outputs/**' --glob '!docs/research/**'
    --glob '!docs/hygiene/**'
  non_claims:
    - not validation
    - not readiness
    - not case-finder sign-off
    - not broad filename migration
    - not historical artifact rewrite
```