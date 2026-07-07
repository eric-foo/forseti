# Forseti Repo-Map Architecture MGT Filename Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Bounded filename migration for the Repo-Map Architecture MGT authority record.
use_when:
  - Resolving whether the live repo-map architecture authority still uses a lowercase `orca_*` filename.
  - Auditing the family-by-family lowercase filename migration queue.
  - Updating live references to the Forseti repo-map architecture authority.
authority_boundary: retrieval_only
open_next:
  - docs/migration/forseti_repo_map_architecture_mgt_filename_migration_v0/moved_paths_index.md
  - docs/workflows/forseti_post_harness_migration_status_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Decision

Migrate the live Repo-Map Architecture MGT authority filename from lowercase
`orca_*` to a Forseti filename, without changing the architecture semantics and
without touching historical prompts, review outputs, research snapshots, old
migration evidence, archived DCP receipt bodies, source-pin rows,
source-hash rows, or unrelated remaining `orca_*` filename families.

This batch is re-derived from current `origin/main` after PR #772 (`16ce9026`,
including #753, #755, #756, #757, #758, #759, #760, #763, #765, #767, #768,
#769, #770, #771, and #772). Older migration PRs or worktrees are reference
material only, not merge targets for this filename family.

| Old path | New path | Rule |
| --- | --- | --- |
| `docs/decisions/orca_repo_map_architecture_mgt_v0.md` | `docs/decisions/forseti_repo_map_architecture_mgt_v0.md` | Live repo-map retrieval architecture authority; rename and update live references. |

## Compatibility Rule

Historical references to the old filename remain valid provenance and resolve
through `docs/migration/forseti_repo_map_architecture_mgt_filename_migration_v0/moved_paths_index.md`.
This lane does not authorize a broad word-match rewrite of remaining `orca_*`
filenames or the broader `docs/decisions/orca_*` decision-record family.

## Non-Claims

- Not validation, readiness, buyer proof, product proof, scan authorization, capture authorization, or feature/build authorization.
- Not a semantic amendment to the repo-map architecture, coverage invariant, generated index/health role, recent-change satellite role, or promotion-on-touch boundary.
- Not creation or deletion of any repo-map, submap, generated inventory, or standing gardener artifact.
- Not retirement of `docs/workflows/orca_repo_map_v0.md` as a compatibility pointer.
- Not retirement of `orca_start_preflight`, `/orca-product-lead`, or other legacy compatibility aliases.
- Not a rewrite of historical prompts, review outputs, research snapshots, old migration evidence, archived DCP receipt bodies, source-pin rows, source-hash rows, or unrelated lowercase filename families.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The Repo-Map Architecture MGT authority now uses a Forseti filename for the
    live source, with the old path resolved by a moved-path index; remaining
    lowercase filename families stay separate migration units.
  trigger: lifecycle_boundary
  related_triggers:
    - workflow_authority
    - validation_philosophy
    - output_authority
  controlling_sources_updated:
    - docs/decisions/forseti_repo_map_architecture_mgt_filename_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/migration/forseti_repo_map_architecture_mgt_filename_migration_v0/moved_paths_index.md
    - docs/decisions/forseti_repo_map_architecture_mgt_v0.md
  downstream_surfaces_checked:
    - .agents/hooks/check_map_links.py
    - docs/decisions/forseti_doctrine_index_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/repo_map_header_backlog_prompt_batch_v0.md
    - docs/workflows/repo_map_header_backlog_review_outputs_batch_1_v0.md
    - docs/workflows/repo_map_retrieval_batches_3_5_v0.md
    - docs/workflows/repo_map_retrieval_probe_batch_2_v0.md
  intentionally_not_updated:
    - path: historical prompts, review outputs, review inputs, research snapshots, hygiene handoffs, old migration records, archived DCP receipt bodies, source-pin rows, source-hash rows
      reason: >
        Those artifacts are provenance, prior migration evidence, or pinned
        source context; old filenames resolve through the moved-path index
        instead of being rewritten.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The legacy repo-map compatibility pointer remains intentionally tracked;
        this lane migrates the architecture decision filename, not the existing
        repo-map pointer compatibility surface.
    - path: remaining older Orca-named decision records
      reason: >
        Existing `docs/decisions/orca_*` settlement records require their own
        family-by-family classification. This lane updates the repo-map
        architecture successor and live references only.
    - path: orca_start_preflight
      reason: >
        Start-preflight alias retirement is a separate compatibility lane; this
        filename migration does not change accepted prompt preflight aliases.
    - path: remaining lowercase `orca_*` filename families
      reason: >
        The migration policy requires family-by-family batches with moved-path
        coverage, not a broad word-match rewrite.
  stale_language_search: >
    rg -n "docs/decisions/orca_repo_map_architecture_mgt_v0.md|orca_repo_map_architecture_mgt_v0.md"
    .agents docs --glob '!docs/prompts/**' --glob '!docs/review-inputs/**'
    --glob '!docs/review-outputs/**' --glob '!docs/research/**'
    --glob '!docs/hygiene/**'
  non_claims:
    - not validation
    - not readiness
    - not architecture amendment
    - not repo-map compatibility pointer retirement
    - not broad filename migration
    - not historical artifact rewrite
```