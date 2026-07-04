# Forseti Product-Root Migration Runbook

```yaml
retrieval_header_version: 1
artifact_role: Forseti migration record
scope: >
  Runbook for moving the live product authority tree from orca/product/ to
  forseti/product/ while preserving historical Orca path references through a
  generated moved-path index.
use_when:
  - Executing or reviewing the product-root migration.
  - Resolving why old orca/product references remain in historical artifacts.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_product_root_migration_decision_v0.md
  - docs/migration/forseti_product_root_migration_v0/moves_manifest.csv
  - docs/migration/forseti_product_root_migration_v0/moved_paths_index.md
stale_if:
  - The migration has been superseded by a later product-root move.
```

## What This Applies

298 tracked paths move from `orca/product/` to `forseti/product/`. The
move is a governed rename, not a semantic deletion. Historical prompts, reviews,
receipts, and old migration records are not word-rewritten; they resolve through
`moved_paths_index.md`.

## Apply Shape

1. Start from a clean lane branch/worktree.
2. Verify this manifest against the current tree.
3. Move the tree with `git mv orca forseti` while `orca/` contains only
   `product/`.
4. Repoint live routers, overlays, maps, and checkers to `forseti/product/`.
5. Run the validation gates named in the decision record.

Rollback is ordinary git rollback for tracked files. The generated index is not
a source of authority; it is a resolver for historical path references.

## Non-Claims

This runbook does not rename the GitHub repository, local checkout folder,
`orca-harness/`, package names, CI check names, skill IDs, or historical
provenance records.
