# Forseti Mini God Tier Doctrine Filename Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Bounded filename migration for the Mini God Tier doctrine record.
use_when:
  - Resolving whether the live Mini God Tier doctrine still uses a lowercase `orca_*` filename.
  - Auditing the family-by-family lowercase filename migration queue.
  - Updating live references to the owner-adopted Mini God Tier doctrine lens.
authority_boundary: retrieval_only
open_next:
  - docs/migration/forseti_mini_god_tier_doctrine_filename_migration_v0/moved_paths_index.md
  - docs/workflows/forseti_post_harness_migration_status_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Decision

Migrate the live Mini God Tier doctrine filename from lowercase `orca_*` to a
Forseti filename, without touching historical prompts, review outputs, research
snapshots, old migration evidence, archived DCP receipt bodies, source-pin
rows, source-hash rows, or unrelated remaining `orca_*` filename families.

This batch is re-derived from current `origin/main` after PR #770 (`8564befe`,
including #753, #755, #756, #757, #758, #759, #760, #763, #765, #767, #768,
#769, and #770). Older migration PRs or worktrees are reference material only,
not merge targets for this filename family.

| Old path | New path | Rule |
| --- | --- | --- |
| `docs/decisions/orca_mini_god_tier_doctrine_v0.md` | `docs/decisions/forseti_mini_god_tier_doctrine_v0.md` | Live owner-adopted Mini God Tier doctrine lens; rename and update live references. |

## Compatibility Rule

Historical references to the old filename remain valid provenance and resolve
through `docs/migration/forseti_mini_god_tier_doctrine_filename_migration_v0/moved_paths_index.md`.
This lane does not authorize a broad word-match rewrite of remaining `orca_*`
filenames or the broader `docs/decisions/orca_*` decision-record family.

## Non-Claims

- Not validation, readiness, buyer proof, product proof, scan authorization, capture authorization, or feature/build authorization.
- Not a semantic amendment to the Mini God Tier doctrine lens.
- Not retirement of `orca_start_preflight`, `/orca-product-lead`, or other legacy compatibility aliases.
- Not a rewrite of historical prompts, review outputs, research snapshots, old migration evidence, archived DCP receipt bodies, source-pin rows, source-hash rows, or unrelated lowercase filename families.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The Mini God Tier doctrine record now uses a Forseti filename for the live
    doctrine source, with the old path resolved by a moved-path index; remaining
    lowercase filename families stay separate migration units.
  trigger: lifecycle_boundary
  related_triggers:
    - product_doctrine
    - workflow_authority
    - output_authority
  controlling_sources_updated:
    - docs/decisions/forseti_mini_god_tier_doctrine_filename_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/migration/forseti_mini_god_tier_doctrine_filename_migration_v0/moved_paths_index.md
    - docs/decisions/forseti_mini_god_tier_doctrine_v0.md
    - docs/decisions/orca_doctrine_index_v0.md
    - AGENTS.md
  downstream_surfaces_checked:
    - AGENTS.md
    - docs/decisions/
    - forseti/product/
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
  intentionally_not_updated:
    - path: historical prompts, review outputs, review inputs, research snapshots, hygiene handoffs, old migration records, archived DCP receipt bodies, source-pin rows, source-hash rows, and older DCP receipt bodies
      reason: >
        Those artifacts are provenance, prior migration evidence, or pinned
        source context; old filenames resolve through the moved-path index
        instead of being rewritten.
    - path: remaining older Orca-named decision records
      reason: >
        Existing `docs/decisions/orca_*` settlement records require their own
        family-by-family classification. This lane updates the Mini God Tier
        doctrine successor and live references only.
    - path: orca_start_preflight
      reason: >
        Start-preflight alias retirement is a separate compatibility lane; this
        filename migration does not change accepted prompt preflight aliases.
    - path: remaining lowercase `orca_*` filename families
      reason: >
        The migration policy requires family-by-family batches with moved-path
        coverage, not a broad word-match rewrite.
  stale_language_search: >
    rg -n "docs/decisions/orca_mini_god_tier_doctrine_v0.md|orca_mini_god_tier_doctrine_v0.md"
    AGENTS.md docs/decisions docs/workflows docs/migration forseti/product
    forseti-harness/docs --glob '!docs/prompts/**' --glob '!docs/review-inputs/**'
    --glob '!docs/review-outputs/**' --glob '!docs/research/**'
    --glob '!docs/hygiene/**'
  non_claims:
    - not validation
    - not readiness
    - not doctrine amendment
    - not broad filename migration
    - not historical artifact rewrite
```