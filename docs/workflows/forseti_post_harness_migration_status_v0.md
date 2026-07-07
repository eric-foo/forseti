# Forseti Post-Harness Migration Status v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Current Forseti rename migration status and residual queue.
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

## Baseline Census

Baseline census observed from `origin/main` after PR #675 merged as `c10f1d7f` on 2026-07-05. Later rows below record subsequent executed migration lanes where explicitly cited. Current convergence planning treats `origin/main` after PR #767 (`f6346932`, including #753, #755, #756, #757, #758, #759, #760, #763, #765, and #767) as the baseline; pre-#753/#755/#756 migration branches are spent unless their remaining value is manually re-derived against current `main`.

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
| Local parent checkout folder | Partially executed on 2026-07-05: a fresh main-repo clone exists at `C:\Users\vmon7\Desktop\projects\forseti` and tracks `eric-foo/forseti`; the local web checkout moved to `C:\Users\vmon7\Desktop\projects\ForsetiWeb`. The legacy active workspace remains under `projects/orca`. | Use `projects/forseti` for new main-repo sessions; do not rename or delete `projects/orca` until its active worktrees/sessions are closed or deliberately migrated. |
| Skill command/path | Executed by the skill identity lane: `forseti-product-lead` is the primary accepted/deployed product-lead skill ID; `/orca-product-lead` remains a thin compatibility wrapper. | Resolver activation in an already-running thread is not claimed; keep wrapper for one transition window. |
| Current-main convergence | Executed through PR #767: #753 recorded the local checkout split, #755 landed ontology GT ladder/A1/A2/R0 SSOT fixes, #756 landed the TikTok packet-grade runner posture on `forseti-harness/`, #757 aligned the migration plan to current `main`, #758 migrated the ontology filename family, #759 migrated the product-lead authority filename family, #760 added the missing-work PR fanout handoff prompt, #763 migrated the demand-read taxonomy filename family, #765 migrated the vertical-exploration filename family, and #767 migrated the scanning/admissibility filename family. | Future migration and conflict-resolution lanes start from current `main`; do not replay stale side-branch trees over #755/#756/#758/#759/#760/#763/#765/#767 files. |
| Ontology filename family | Executed by PR #758: the live ontology GT ladder and ontology backbone filenames now use Forseti names. | Historical old filenames resolve through `docs/migration/forseti_ontology_filename_migration_v0/moved_paths_index.md`; remaining lowercase `orca_*` filename families stay separate queued batches. |
| Product-lead authority filename family | Executed by PR #759: the live product thesis, offer hypothesis, buyer-proof packet, product-proof charter, and claim-defense doctrine filenames now use Forseti names. | Historical old filenames resolve through `docs/migration/forseti_product_lead_authority_filename_migration_v0/moved_paths_index.md`; remaining lowercase `orca_*` filename families stay separate queued batches. |
| Demand-read taxonomy filename family | Executed by PR #763: the live proposed demand-read grammar and adjudication-prep companion filenames now use Forseti names. | Historical old filenames resolve through `docs/migration/forseti_demand_read_taxonomy_filename_migration_v0/moved_paths_index.md`; remaining lowercase `orca_*` filename families stay separate queued batches. |
| Vertical-exploration filename family | Executed by PR #765: the live WHERE-side vertical-exploration procedure and memorization-resistant case-finder frame filenames now use Forseti names. | Historical old filenames resolve through `docs/migration/forseti_vertical_exploration_filename_migration_v0/moved_paths_index.md`; remaining lowercase `orca_*` filename families stay separate queued batches. |
| Scanning/admissibility filename family | Executed by PR #767: the live scan-core method spec, intelligent-walk MGT operating model, demand-gate closures artifact, and scan-gate adjudication packet filenames now use Forseti names. | Historical old filenames resolve through `docs/migration/forseti_scanning_filename_migration_v0/moved_paths_index.md`; remaining lowercase `orca_*` filename families stay separate queued batches. |
| Commission Signal Board filename family | Executed by this bounded Commission Signal Board filename migration lane: the live CSB Prompt Structure Rules, Prompt Structure, and legacy non-controlling gate-run criteria filenames now use Forseti names. | Historical old filenames resolve through `docs/migration/forseti_commission_signal_board_filename_migration_v0/moved_paths_index.md`; remaining lowercase `orca_*` filename families stay separate queued batches. |
| Start-preflight alias | Deferred: `orca_start_preflight` remains a legacy alias. | New live prompts and reports prefer `forseti_start_preflight`; alias retirement is last-mile compatibility work. |
| Lowercase `orca_*` filenames | Partially deferred: the ontology, product-lead authority, demand-read taxonomy, vertical-exploration, scanning/admissibility, and Commission Signal Board filename families have migrated; other families remain queued by default. | Migrate only by family with moved-path/index coverage; do not word-match historical prompts, reviews, receipts, research snapshots, source-pin rows, or source-hash rows. |

## Supersession Notes

The pre-harness records `docs/decisions/forseti_compatibility_migration_boundary_v0.md`,
`docs/decisions/forseti_external_identity_path_migration_decision_v0.md`,
`docs/workflows/forseti_rename_residual_inventory_v0.md`, and
`docs/workflows/forseti_rename_stale_reference_audit_v0.md` remain useful for
their original evidence, but their statements that `orca-harness/`,
`orca-harness`, or `orca-harness-tests` are preserved/deferred are superseded
by PR #675 and `docs/decisions/forseti_harness_identity_migration_plan_v0.md`.
Statements that the external repo slug or product-lead skill identity are still
deferred are superseded by `docs/decisions/forseti_external_identity_path_migration_decision_v0.md`
and `docs/decisions/forseti_skill_preflight_identity_migration_plan_v0.md`.
Migration branches or handoffs authored before PR #753, PR #755, PR #756, PR #758, PR #759, PR #760, PR #763, PR #765, or PR #767 are
not convergence targets. Their remaining useful changes must be re-applied from
current `main`, with special care around ontology/A1/A2/R0 sources, product-lead
authority filenames, demand-read taxonomy files, vertical-exploration files, scanning/admissibility files, Commission Signal Board files, and TikTok runner/harness files
that changed in those PRs.

## Next Material Lane

The next high-leverage migration is not another word-match cleanup. After the
external repo identity, product-lead skill identity, checkout split, #755
ontology/source fixes, #756 TikTok runner posture, #757 current-main plan
alignment, #758 ontology filename migration, #759 product-lead authority filename
migration, #760 missing-work PR fanout prompt, #763 demand-read taxonomy filename migration, #765 vertical-exploration filename migration, and #767 scanning/admissibility filename migration have landed, the remaining
material lanes are:

1. Converge from current `main`; treat old stacked migration PRs/worktrees as
   reference material, not merge targets.
2. Close or migrate the legacy active `projects/orca` workspace/worktrees once no
   running sessions depend on them; the fresh `projects/forseti` clone is now
   available for new main-repo sessions.
3. Continue family-by-family live filename migration for current product sources
   whose `orca_*` filenames are still operator-facing; the ontology,
   product-lead authority, demand-read taxonomy, vertical-exploration, and
   scanning/admissibility filename families have landed, this lane handles the Commission Signal Board
   filename family, and remaining families still need moved-path coverage plus
   a fresh read of any #755/#756/#758/#759/#760/#763/#765/#767-touched source before
   editing.
4. Retire `orca_start_preflight` only after durable prompt/history consumers are
   classified; keep `forseti_start_preflight` primary now.
5. Retire compatibility wrappers such as `/orca-product-lead` only after one
   transition window and resolver behavior are verified.

## Non-Claims

- This status record is not validation, readiness, product proof, package publication, GitHub repo rename execution, legacy workspace retirement, or resolver activation proof.
- This status record does not classify every residual content line.
- This status record does not make historical prompts, review outputs, DCP receipts, or snapshots stale merely because they contain Orca.
