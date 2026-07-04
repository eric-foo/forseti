# Forseti Compatibility Migration Boundary v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Boundary for Forseti rename compatibility, runtime/tooling, and stale-reference audit batches.
use_when:
  - Deciding whether a remaining Orca/orca identifier should be renamed now.
  - Preparing fused or implementation-scoped work for the rename compatibility/runtime batches.
  - Reviewing whether a proposed rename touches high-lock-in path, package, skill, hook, or CI identifiers.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_rename_migration_policy_v0.md
  - docs/workflows/forseti_rename_residual_inventory_v0.md
  - docs/prompts/handoffs/forseti_compatibility_batches_fused_handoff_v0.md
```

## Decision

Do not perform a broad compatibility/path/package rename in the next fused pass.

The next fused lane may patch narrow live human-facing defects and compatibility-note gaps, then run the final stale-reference audit. It must not rename top-level roots, package/import names, skill IDs, CI check IDs, or the live repo-map path unless a separate owner-accepted migration plan names the moved-path index, validation commands, rollback notes, and downstream dependency impacts.

Preserved compatibility identifiers are not rename defects:

- historical `orca/product/` paths
- `orca-harness/`
- `docs/workflows/orca_repo_map_v0.md`
- `orca-product-lead`
- `orca_start_preflight`
- lowercase `orca_*` filenames, package/import paths, and external identifiers
- CI/check identifiers such as `orca-harness-tests`

## Why

The rename policy already makes Forseti the canonical project/product name while preserving legacy lowercase paths, package names, filenames, skill IDs, hook names, and historical artifacts until an explicit compatibility batch migrates or retires them. The fresh residual inventory shows most remaining hits are in historical docs, review/prompt artifacts, or compatibility roots. A word-match rename would change route, package, CI, and provenance semantics with no rollback plan.

The right long-term state may still include deeper path/package migration, but it is a high-lock-in migration, not a text cleanup.

## Batch Boundary

| Batch | Allowed now | Not allowed now |
| --- | --- | --- |
| Step 4 runtime/tooling | Patch live human-facing runtime/tooling labels only when they imply Orca remains the current project/product name; add explicit compatibility notes when useful. | Rename `orca-harness/`, package/import names, CI job/check IDs, runner paths, or working directories. |
| Step 5 stale-reference audit | Classify remaining hits as historical provenance, explicit legacy alias, transitional compatibility, scratch/inbox, or defect; patch only live defects. | Rewrite historical prompts/reviews/DCPs, scratch/inbox material, compatibility IDs, or package/path names by word match. |

## Specific Surface Decisions

| Surface | Boundary |
| --- | --- |
| `forseti/product/` | Live product tree root after the product-root successor migration; historical `orca/product/` paths resolve through `docs/migration/forseti_product_root_migration_v0/moved_paths_index.md`. |
| `orca-harness/` | Preserve as the runtime/tooling root. A README label may say "Forseti harness" while noting the legacy path, but the directory remains. |
| `docs/workflows/orca_repo_map_v0.md` | No longer the live repo-map path after the successor migration; retain only as a compatibility pointer to `docs/workflows/forseti_repo_map_v0.md`. |
| `orca-product-lead` | Preserve as the accepted/frozen compatibility skill command/path until a skill migration explicitly handles source copy, deployment copy, invocation, collision, and rollback. |
| `orca_start_preflight` | Preserve as a legacy alias. New live prompts and reports prefer `forseti_start_preflight`. |
| `orca-harness-tests` | Preserve unless branch protection, auto-merge, and CI dependency impacts are checked and accepted. |
| `docs/_inbox/**` | Leave by default. Triage only when promoted or used as source. |

## Assumption Gate Result

```yaml
assumption_gate:
  accepted_direction: Steps 2 and 3 now; prepare fused handoff for Steps 4 and 5.
  state: READY_WITH_VERIFIED_LEDGER
  verified_assumptions:
    - PR #646 is merged into observed current main at 351fe2ac.
    - The rename policy defines compatibility and historical classes that remain valid.
    - Compatibility/path/runtime work is high-lock-in without a boundary decision.
    - The next fused lane must not rerun the previously stalled registration_integrity.py --selftest command.
  blockers_for_docs_boundary: none
  blockers_for_path_package_migration:
    - No moved-path index for root/package/skill migration.
    - No rollback plan for root/package/skill migration.
    - No branch-protection or CI dependency analysis for check-name migration.
```

## Fused Authorization Boundary

This decision does not execute `/fused`, authorize implementation by itself, or open a path/package migration. If the operator invokes `/fused` with `docs/prompts/handoffs/forseti_compatibility_batches_fused_handoff_v0.md`, the receiving lane gets only the bounded Step 4/5 work stated there.

Any deeper move from `orca` paths to `forseti` paths requires a new explicit owner acceptance after a concrete plan names:

- exact moved paths and aliases;
- moved-path index and repo-map update path;
- package/import/reference rewrite method;
- CI/check-name and branch-protection impact;
- rollback notes;
- validation gates and timeouts.

## Non-Claims

- This decision is not validation, readiness, product proof, implementation authorization, or path/package migration.
- This decision does not prove every remaining Orca hit is valid.
- This decision does not block future migration; it blocks implicit word-match migration.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Forseti rename Steps 4 and 5 are bounded to narrow live runtime/tooling label repairs and final classified stale-reference audit; root paths, package/import names, skill IDs, CI check IDs, and the live repo-map path remain compatibility identifiers unless a separate owner-accepted migration plan binds moved-path indexes, validation, rollback, and dependency impacts.
  trigger: lifecycle_boundary
  related_triggers:
    - workflow_authority
    - output_authority
  controlling_sources_updated:
    - docs/decisions/forseti_compatibility_migration_boundary_v0.md
  downstream_surfaces_checked:
    - docs/decisions/forseti_rename_migration_policy_v0.md
    - docs/workflows/forseti_rename_residual_inventory_v0.md
    - docs/prompts/handoffs/forseti_compatibility_batches_fused_handoff_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - repo-structure.yaml
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/skill-adoption.md
    - .github/workflows/ci.yml
    - .github/workflows/auto-merge.yml
  intentionally_not_updated:
    - path: docs/decisions/forseti_rename_migration_policy_v0.md
      reason: >
        The policy already declares compatibility names preserved until explicit migration; this decision applies that policy to the next fused batches instead of changing it.
    - path: repo-structure.yaml
      reason: >
        Its router-only compatibility paths remain correct; changing them would be the deferred path migration this decision forbids for the next fused pass.
    - path: .agents/workflow-overlay/artifact-folders.md
      reason: >
        It now declares `forseti/product/` as the live product root and preserves historical `orca/product/` through a moved-path index; no runtime/package/skill migration happens here.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        It already names forseti_start_preflight as preferred and orca_start_preflight as a legacy alias; no alias change now.
    - path: .agents/workflow-overlay/skill-adoption.md
      reason: >
        It already records orca-product-lead as the retained compatibility command/path; no skill migration now.
    - path: .github/workflows/ci.yml
      reason: >
        CI check IDs and working-directory paths stay compatibility identifiers until a separate check-name and branch-protection migration is accepted.
    - path: .github/workflows/auto-merge.yml
      reason: >
        Its CI_CHECK value depends on the retained orca-harness-tests check name; changing it belongs to a separate CI migration.
  stale_language_search: >
    rg -n -i "\bOrca\b|\bORCA\b|orca_start_preflight" README.md repo-structure.yaml .agents/workflow-overlay docs/workflows/orca_repo_map_v0.md .github/workflows .agents/skills/orca-product-lead orca-harness/README.md docs/_inbox/README.md
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not path/package migration
```
