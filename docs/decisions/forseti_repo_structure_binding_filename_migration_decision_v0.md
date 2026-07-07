# Forseti Repo Structure Binding Filename Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Bounded filename migration for the Repo Structure Binding authority record.
use_when:
  - Resolving whether the live repo structure binding still uses a lowercase `orca_*` filename.
  - Auditing the family-by-family lowercase filename migration queue.
  - Updating live references to the Forseti repo structure binding.
authority_boundary: retrieval_only
open_next:
  - docs/migration/forseti_repo_structure_binding_filename_migration_v0/moved_paths_index.md
  - docs/workflows/forseti_post_harness_migration_status_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Decision

Migrate the live Repo Structure Binding authority filename from lowercase
`orca_*` to a Forseti filename, without changing placement semantics,
repo-structure parameters, or checker behavior, and without touching historical
prompts, review outputs, research snapshots, old migration evidence, archived
DCP receipt bodies, source-pin rows, source-hash rows, or unrelated remaining
`orca_*` filename families.

This batch is re-derived from current `origin/main` after PR #773 (`99f51e1d`,
including #753, #755, #756, #757, #758, #759, #760, #763, #765, #767, #768,
#769, #770, #771, #772, and #773). Older migration PRs or worktrees are
reference material only, not merge targets for this filename family.

| Old path | New path | Rule |
| --- | --- | --- |
| `docs/decisions/orca_repo_structure_binding_v0.md` | `docs/decisions/forseti_repo_structure_binding_v0.md` | Live placement/structure binding authority; rename and update live references. |

## Compatibility Rule

Historical references to the old filename remain valid provenance and resolve
through `docs/migration/forseti_repo_structure_binding_filename_migration_v0/moved_paths_index.md`.
This lane does not authorize a broad word-match rewrite of remaining `orca_*`
filenames or the broader `docs/decisions/orca_*` decision-record family.

## Non-Claims

- Not validation, readiness, buyer proof, product proof, scan authorization, capture authorization, or feature/build authorization.
- Not a semantic amendment to placement doctrine, repo-structure parameters, artifact-folder authority, or `check_placement.py` behavior.
- Not retirement of `docs/workflows/orca_repo_map_v0.md` as a compatibility pointer.
- Not migration of the spine-first target, blocker authorization, search-lane binding, data-lake binding, creator-signal binding, or other remaining filename families.
- Not retirement of `orca_start_preflight`, `/orca-product-lead`, or other legacy compatibility aliases.
- Not a rewrite of historical prompts, review outputs, research snapshots, old migration evidence, archived DCP receipt bodies, source-pin rows, source-hash rows, or unrelated lowercase filename families.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The Repo Structure Binding authority now uses a Forseti filename for the
    live source, with the old path resolved by a moved-path index; remaining
    lowercase filename families stay separate migration units.
  trigger: lifecycle_boundary
  related_triggers:
    - workflow_authority
    - validation_philosophy
    - output_authority
  controlling_sources_updated:
    - docs/decisions/forseti_repo_structure_binding_filename_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/migration/forseti_repo_structure_binding_filename_migration_v0/moved_paths_index.md
    - docs/decisions/forseti_repo_structure_binding_v0.md
    - repo-structure.yaml
    - .agents/workflow-overlay/artifact-folders.md
  downstream_surfaces_checked:
    - .agents/hooks/check_placement.py
    - repo-structure.yaml
    - .agents/workflow-overlay/artifact-folders.md
    - docs/decisions/forseti_doctrine_index_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - forseti/product/spines/foundation/ontology/forseti_ontology_backbone_architecture_v0.md
    - forseti/product/spines/commission_signal_board/spine.yaml
  intentionally_not_updated:
    - path: historical prompts, review outputs, review inputs, research snapshots, hygiene handoffs, old migration records, archived DCP receipt bodies, source-pin rows, and source-hash rows
      reason: >
        Those artifacts are provenance, prior migration evidence, or pinned
        source context; old filenames resolve through the moved-path index
        instead of being rewritten.
    - path: remaining structure-family decision records
      reason: >
        The spine-first target, blocker authorization, search-lane binding,
        data-lake binding, creator-signal binding, and adjacent filenames each
        need their own family-by-family classification. This lane updates the
        repo structure binding successor and live references only.
    - path: orca_start_preflight
      reason: >
        Start-preflight alias retirement is a separate compatibility lane; this
        filename migration does not change accepted prompt preflight aliases.
    - path: remaining lowercase `orca_*` filename families
      reason: >
        The migration policy requires family-by-family batches with moved-path
        coverage, not a broad word-match rewrite.
  stale_language_search: >
    rg -n "docs/decisions/orca_repo_structure_binding_v0.md|orca_repo_structure_binding_v0.md|orca_repo_structure_binding_v0"
    .agents docs repo-structure.yaml forseti --glob '!docs/prompts/**'
    --glob '!docs/review-inputs/**' --glob '!docs/review-outputs/**'
    --glob '!docs/research/**' --glob '!docs/hygiene/**'
  non_claims:
    - not validation
    - not readiness
    - not placement amendment
    - not broad filename migration
    - not historical artifact rewrite
```