# Forseti Product-Root Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: >
  Binds the live product authority tree successor from orca/product/ to
  forseti/product/, with moved-path compatibility for historical Orca product
  paths and no runtime/package/CI rename.
use_when:
  - Resolving the live product tree root.
  - Reviewing the product-root migration lane.
  - Deciding whether an old orca/product path should be rewritten or resolved.
authority_boundary: retrieval_only
open_next:
  - docs/migration/forseti_product_root_migration_v0/runbook.md
  - docs/migration/forseti_product_root_migration_v0/moves_manifest.csv
  - docs/migration/forseti_product_root_migration_v0/moved_paths_index.md
  - docs/workflows/forseti_repo_map_v0.md
stale_if:
  - A later accepted migration relocates the product tree again.
  - The manifest or moved-path index changes without this decision being updated.
```

## Decision

The live product authority tree root is now `forseti/product/`.

`orca/product/` is no longer a live tree root. It is a historical compatibility
predecessor whose old paths resolve through
`docs/migration/forseti_product_root_migration_v0/moved_paths_index.md`.

This is a path-authority migration only. It does not rename `orca-harness/`, the
`orca-harness` package, `orca-harness-tests`, `orca-product-lead`,
`orca_start_preflight`, the GitHub repository slug, local checkout folder, or
historical prompt/review/provenance records.

## Why

Leaving the main product tree under `orca/product/` after the authority and repo
map have moved to Forseti creates durable operator and agent confusion. The path
is not merely prose: it is embedded in repo navigation, source-loading packs,
placement checks, ontology checks, deletion-evidence governance, and product
records. The migration therefore has to be manifest-backed and gate-backed, not a
word-match rename.

## Execution Shape

- Moved 298 tracked product-tree paths from `orca/product/**` to
  `forseti/product/**` according to
  `docs/migration/forseti_product_root_migration_v0/moves_manifest.csv`.
- Added a generated moved-path index with a root-prefix row plus file-level rows.
- Repointed live authority/navigation/checker surfaces to `forseti/product/`.
- Updated link checking so indexed historical paths can resolve to current
  successors without mass-rewriting historical artifacts.
- Updated deletion-evidence governance so the old-root to new-root rename is
  governed-to-governed for this migration diff; future product deletions remain
  governed under `forseti/product/`.

## Historical Compatibility Rule

Do not mechanically rewrite old prompts, reviews, review inputs, DCP receipts,
hygiene packets, or prior migration records just because they contain
`orca/product/`. Those references are point-in-time provenance unless the artifact
is reactivated as a live route. Use the moved-path index to resolve them.

Current live authority and navigation surfaces should use `forseti/product/`.

## Stacked-Lane Dependency

This lane is stacked on `codex/forseti-repo-map-successor` at commit `189f8938`
because PR #655 was observed open and unmerged when this lane began. The product
root branch should target the repo-map-successor branch or be rebased onto
`main` after #655 lands.

## Validation Plan

Do not run `registration_integrity.py --selftest` for this migration.

Required gates before PR-ready claim:

```text
python docs/migration/forseti_product_root_migration_v0/apply_moves.py --dry-run
python .agents/hooks/check_map_links.py --selftest
python .agents/hooks/check_map_links.py --strict
python .agents/hooks/check_map_links.py --report-forseti
python .agents/hooks/check_placement.py --strict
python .agents/hooks/check_deletion_evidence.py --selftest
python .agents/hooks/check_deletion_evidence.py --strict
python .agents/hooks/header_index.py --strict
python .agents/hooks/check_dcp_receipt.py --strict
python .agents/hooks/check_repo_map_freshness.py --strict
python .agents/hooks/check_full_gt_claims.py --changed --strict
python .agents/hooks/check_review_routing.py --strict
```

If a gate fails because it discovers a real stale live path, patch the live path.
If a gate fails only because it reads historical `orca/product/` provenance as a
live path, prefer moved-path resolution or a narrow nonresolving annotation over
rewriting history.

## Observed Validation Evidence

Observed on this lane after the move and live-surface rewrites:

```text
python docs/migration/forseti_product_root_migration_v0/apply_moves.py --dry-run
DRY RUN: 0 pending, 298 already applied, 0 problem row(s)

python .agents/hooks/check_map_links.py --strict
check_map_links --strict: OK (0 findings)
annotated nonresolving: 33 (debt, not failures)

python .agents/hooks/check_map_links.py --report-forseti
open_next unresolved (C2): 0
inline links unresolved (C4): 0
folders w/ >=1 .md not map-covered (COV>C3): 0
total report findings: 0

python .agents/hooks/check_placement.py --strict
summary: 0 violation(s), 0 freshness, 1167 legacy-tolerated (warn-only), 68 scratch-excluded file(s)

python .agents/hooks/check_deletion_evidence.py --strict
check_deletion_evidence --strict: OK -- every governed deletion in this diff carries a complete evidence record

python .agents/hooks/header_index.py --strict
header_index --strict: OK -- 10 changed durable .md file(s) all have headers and are map-reachable (base: origin/main)

python .agents/hooks/check_dcp_receipt.py --strict
check_dcp_receipt --strict: OK -- every real receipt in the changed .md files is shape-valid (base: origin/main)

python .agents/hooks/check_full_gt_claims.py --changed --strict
check_full_gt_claims: OK -- no unballasted full-GT claim language in scope

python .agents/hooks/check_review_routing.py --strict
check_review_routing --strict: OK (base: origin/main)

python .agents/hooks/check_doc_terms.py --selftest
SELFTEST OK

python .agents/hooks/check_doc_terms.py --report-forseti
files scanned: 274
total report findings (candidates): 4
```

Additional clean checks: `python .agents/hooks/check_repo_map_freshness.py --strict`,
`git diff --check`, and `python -m py_compile` over the modified hooks all
returned exit code 0. `registration_integrity.py --selftest` was deliberately
not run.

## Direction Change Propagation

```yaml
direction_change_propagation:
  trigger: lifecycle_boundary
  doctrine_changed: >
    The live product authority tree successor is bound from orca/product/ to
    forseti/product/ with a manifest-backed moved-path resolver for historical
    Orca product paths. Runtime, package, CI, skill, repo slug, local checkout,
    prompt/review provenance, and other compatibility identifiers remain
    preserved until their own accepted migration units.
  previous_live_root: orca/product/
  new_live_root: forseti/product/
  compatibility_resolver: docs/migration/forseti_product_root_migration_v0/moved_paths_index.md
  controlling_sources_updated:
    - docs/decisions/forseti_product_root_migration_decision_v0.md
    - docs/migration/forseti_product_root_migration_v0/runbook.md
    - docs/migration/forseti_product_root_migration_v0/moves_manifest.csv
    - docs/migration/forseti_product_root_migration_v0/moved_paths_index.md
  downstream_surfaces_checked:
    - README.md
    - docs/STRUCTURE.md
    - repo-structure.yaml
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/workflows/ecr_spine_submap_v0.md
    - .agents/workflow-overlay/
    - .agents/hooks/
    - .agents/skills/orca-product-lead/SKILL.md
  deliberately_preserved:
    - historical prompts
    - review inputs and review outputs
    - hygiene handoffs
    - old migration records
    - runtime root orca-harness/
    - skill command orca-product-lead
    - start-preflight alias orca_start_preflight
  non_claims:
    - not product proof
    - not runtime/package migration
    - not CI check-name migration
    - not repository slug rename
    - not local checkout rename
    - not approval to rewrite historical evidence
```

## Non-Claims

This decision is not product proof, validation of product content, repository
slug rename, local checkout rename, runtime/package migration, CI check-name
migration, skill resolver migration, or approval to rewrite historical evidence.
