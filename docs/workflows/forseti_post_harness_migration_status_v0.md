# Forseti Post-Harness Migration Status v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Current post-PR-675 Forseti rename migration status and residual queue.
use_when:
  - Checking what changed after the product-root, repo-map, and harness-root migrations landed.
  - Deciding whether a remaining Orca/orca reference is a live defect, historical record, explicit legacy alias, or deferred compatibility surface.
  - Choosing the next Forseti migration lane after the harness identity migration.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_rename_migration_policy_v0.md
  - docs/decisions/forseti_harness_identity_migration_plan_v0.md
  - docs/decisions/forseti_external_identity_path_migration_decision_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Current State

Observed from `origin/main` after PR #675 merged as `c10f1d7f` on 2026-07-05:

| Check | Observed result |
| --- | --- |
| Open `codex/forseti*` PRs | none |
| Tracked `orca/` or `orca-harness/` roots | none |
| Tracked `forseti/` files | 312 |
| Tracked `forseti-harness/` files | 1214 |
| Path/name hits for retained Orca identifiers | 375 |
| Residual content-hit files in explicit project roots | 1920 |
| Residual content-hit lines in explicit project roots | 27273 |

## Status Ledger

| Migration unit | Current status | Current rule |
| --- | --- | --- |
| Product tree root | Executed: live product tree is `forseti/product/`. | Historical `orca/product/` references resolve through `docs/migration/forseti_product_root_migration_v0/moved_paths_index.md`. |
| Repo-map path | Executed: live map is `docs/workflows/forseti_repo_map_v0.md`. | `docs/workflows/orca_repo_map_v0.md` is a compatibility pointer only. |
| Harness root | Executed by PR #675: live runtime root is `forseti-harness/`. | Remaining `orca-harness/` hits must be historical, residual-audit text, or moved-path source terms unless a fresh scan proves a live missed surface. |
| Harness distribution label | Executed by PR #675: package distribution label is `forseti-harness`. | Python import namespaces remain unchanged. |
| CI check identity | Executed by PR #675: required check is `forseti-harness-tests`. | Do not revive `orca-harness-tests` in live automation. |
| GitHub repository slug | Executed on 2026-07-05: live repo is `eric-foo/forseti`; the former web repo moved from `eric-foo/Forseti` to `eric-foo/ForsetiWeb`. | Local `origin` was updated to `https://github.com/eric-foo/forseti.git`; keep historical repo links as provenance. |
| Local parent checkout folder | Not migrated: active workspace path remains under `projects/orca`. | Use a fresh clone or controlled shutdown/move; do not rename the active workspace in-place. |
| Skill command/path | Deferred: `orca-product-lead` remains the accepted compatibility skill command/path. | Requires source/deployment copy, invocation alias, resolver, hash-pin, rollback, and collision handling before migration. |
| Start-preflight alias | Deferred: `orca_start_preflight` remains a legacy alias. | New live prompts and reports prefer `forseti_start_preflight`; alias retirement is last-mile compatibility work. |
| Lowercase `orca_*` filenames | Deferred by default. | Migrate only by family with moved-path/index coverage; do not word-match historical prompts, reviews, receipts, or snapshots. |

## Supersession Notes

The pre-harness records `docs/decisions/forseti_compatibility_migration_boundary_v0.md`,
`docs/decisions/forseti_external_identity_path_migration_decision_v0.md`,
`docs/workflows/forseti_rename_residual_inventory_v0.md`, and
`docs/workflows/forseti_rename_stale_reference_audit_v0.md` remain useful for
their original evidence, but their statements that `orca-harness/`,
`orca-harness`, or `orca-harness-tests` are preserved/deferred are superseded
by PR #675 and `docs/decisions/forseti_harness_identity_migration_plan_v0.md`.

## Next Material Lane

The next high-leverage migration is not another word-match cleanup. It is one
of:

1. Owner-gated external identity cutover after the target GitHub slug is freed
   or replaced.
2. Skill migration from `orca-product-lead` to `forseti-product-lead` with a
   compatibility alias and deployment-copy plan.
3. Family-by-family live filename migration for current product sources whose
   `orca_*` filenames are still operator-facing, each with moved-path coverage.

## Non-Claims

- This status record is not validation, readiness, product proof, package publication, GitHub repo rename execution, local checkout rename execution, or skill migration.
- This status record does not classify every residual content line.
- This status record does not make historical prompts, review outputs, DCP receipts, or snapshots stale merely because they contain Orca.
