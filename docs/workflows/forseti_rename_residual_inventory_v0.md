# Forseti Rename Residual Inventory v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Current-main residual Orca/ORCA/orca_start_preflight census after the Forseti authority rename.
use_when:
  - Planning the Forseti rename compatibility/runtime batches.
  - Checking whether remaining Orca references are likely historical, compatibility, alias, scratch, or defect candidates.
  - Preparing the final stale-reference audit after compatibility-scoped edits.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_rename_migration_policy_v0.md
  - docs/decisions/forseti_compatibility_migration_boundary_v0.md
  - docs/prompts/handoffs/forseti_compatibility_batches_fused_handoff_v0.md
```

## Start Preflight

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write
  target_scope: residual inventory for rename Steps 2 and 3, plus fused preparation for Steps 4 and 5
  dirty_state_checked: yes
  blocked_if_missing: docs/decisions/forseti_rename_migration_policy_v0.md
workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\forseti-compat-scope
branch: codex/forseti-compat-scope
base_commit_observed: 351fe2ac Rename live project authority to Forseti (#646)
output_mode: file-write
```

## Router Summary

Smallest complete outcome: produce a current-main residual inventory, a compatibility migration boundary decision, and a fused-ready handoff for the next runtime/tooling and audit batches.

Regime: Mixed / complicated.

Why: the rename policy is clear, but the remaining references span live compatibility paths, historical provenance, scratch, runtime tooling, and package/CI identifiers with different lock-in costs.

Decomposition: layer-based with a risk-first boundary probe before any compatibility rename.

Current bottleneck: prevent a broad word-match rename from silently migrating paths, packages, skill IDs, CI check IDs, or historical records.

Riskiest assumption: that remaining lowercase `orca` identifiers should be renamed now because the product name is Forseti.

Stop or pivot condition: a proposed edit requires moving top-level roots, changing import/package names, changing CI check IDs, or rewriting historical provenance without a moved-path index, rollback note, and owner-accepted migration plan.

Allowed next move: prepare bounded compatibility/runtime instructions and run a classified stale-reference audit.

Disallowed next move: bulk replacement of `Orca`, `orca`, paths, package names, skill IDs, or CI identifiers.

## Assumption Gate Ledger

Accepted direction: proceed with Steps 2 and 3 now, then prepare a fused handoff for Steps 4 and 5.

Readiness state: `READY_WITH_VERIFIED_LEDGER` for documentation-only inventory, boundary, and handoff authoring.

Verified assumptions:

| Assumption | Evidence | Result |
| --- | --- | --- |
| PR #646 is merged into current main. | `git log --oneline -5 --decorate` in this worktree shows `351fe2ac (HEAD -> codex/forseti-compat-scope, origin/main, origin/HEAD) Rename live project authority to Forseti (#646)`. | Verified. |
| Remaining Orca hits are not automatically defects. | `docs/decisions/forseti_rename_migration_policy_v0.md` classifies compatibility names, historical provenance, and scratch/inbox material as preserved by default. | Verified. |
| Steps 4 and 5 need a boundary before edits. | The policy places lowercase paths, packages, filenames, skill IDs, hooks, and runtime code in later compatibility/runtime batches requiring validation and rollback notes. | Verified. |
| A fused lane must not re-run the previously stalled integrity selftest. | Prior delegated review return reported `registration_integrity.py --selftest` as blocked by an unrelated `tempfile.TemporaryDirectory` root cause and not re-attempted per commission. | Treat as a forbidden validation retry for the next handoff unless separately reauthorized. |

## Census

Commands were run from `C:\Users\vmon7\Desktop\projects\orca\worktrees\forseti-compat-scope`.

| Question | Command | Observed count |
| --- | --- | --- |
| Files with content hits in explicit project roots | `rg -l -i "\bOrca\b|\bORCA\b|orca_start_preflight" AGENTS.md README.md CLAUDE.md .agents .github docs orca orca-harness repo-structure.yaml \| Measure-Object` | 2,020 files |
| Matched content lines in explicit project roots | `rg -n -i "\bOrca\b|\bORCA\b|orca_start_preflight" AGENTS.md README.md CLAUDE.md .agents .github docs orca orca-harness repo-structure.yaml \| Measure-Object` | 28,806 lines |
| Path/name hits | `rg --files \| rg -i "(^|[\\/])(orca|orca-|orca_)|orca-harness|orca-product-lead|orca_repo_map" \| Measure-Object` | 1,828 paths |

Content hits by top-level root:

| Root | Files |
| --- | ---: |
| `docs` | 1,469 |
| `orca` | 285 |
| `orca-harness` | 223 |
| `.agents` | 37 |
| `.github` | 4 |
| `README.md` | 1 |
| `repo-structure.yaml` | 1 |

Docs hits by second-level folder:

| Folder | Files |
| --- | ---: |
| `docs/review-inputs` | 535 |
| `docs/prompts` | 321 |
| `docs/review-outputs` | 258 |
| `docs/research` | 111 |
| `docs/decisions` | 105 |
| `docs/workflows` | 77 |
| `docs/migration` | 35 |
| `docs/hygiene` | 24 |
| `docs/README.md` | 1 |
| `docs/STRUCTURE.md` | 1 |

`orca/` hits by product subtree:

| Folder | Files |
| --- | ---: |
| `orca/product/spines` | 263 |
| `orca/product/case_families` | 13 |
| `orca/product/satellites` | 6 |
| `orca/product/shared` | 2 |
| `orca/product/README.md` | 1 |

Path/name hits by top grouping:

| Group | Paths |
| --- | ---: |
| `orca-harness` | 1,186 |
| `docs` | 346 |
| `orca` | 296 |

## Classified Control-Surface Sample

This sample classifies live route/control surfaces only. It is not the final exhaustive stale-reference audit.

| Surface | Observed residual | Classification | Step consequence |
| --- | --- | --- | --- |
| `README.md` | Legacy-name note and compatibility paths | explicit legacy/compatibility | Keep; no batch edit required. |
| `repo-structure.yaml` | `orca/product/`, `orca-harness`, `docs/workflows/orca_repo_map_v0.md` routes | compatibility machine-map identifiers | Keep until explicit path migration. |
| `docs/workflows/orca_repo_map_v0.md` | live map path and `orca/` / `orca-harness/` route rows | compatibility navigation | Keep path; add rows for new artifacts only. |
| `.agents/workflow-overlay/artifact-folders.md` | accepted `orca/product/` product tree and `orca-product-lead` example | compatibility authority | Keep until a moved-path migration changes the owner source. |
| `.agents/workflow-overlay/source-loading.md` | `orca_start_preflight` accepted alias | explicit legacy alias | Keep; new live prompts prefer `forseti_start_preflight`. |
| `.agents/workflow-overlay/skill-adoption.md` | `orca-product-lead` accepted/frozen compatibility command/path | explicit compatibility skill ID | Keep. |
| `.agents/skills/orca-product-lead/SKILL.md` | compatibility skill name/path | compatibility skill surface | Do not rename without skill migration and deployment plan. |
| `.github/workflows/ci.yml` | `orca-harness-tests`, working directory `orca-harness` | runtime/CI compatibility ID | Keep unless a separate CI/check-name migration is owner-accepted. |
| `.github/workflows/auto-merge.yml` | `CI_CHECK: orca-harness-tests` | CI compatibility dependency | Keep; changing this can break auto-merge/branch protection assumptions. |
| `orca-harness/README.md` | `# Orca Harness` | runtime/tooling label candidate | Candidate for a compatibility note, not a directory/package rename. |
| `docs/_inbox/README.md` | `# Orca Inbox`, "Orca authority" | scratch/inbox | Leave by default; triage only if promoted. |

## Residual Classes For Step 5

| Class | Default action | Examples |
| --- | --- | --- |
| Historical provenance | Preserve | old prompts, review outputs, dated DCP receipts, prior migration notes |
| Explicit legacy alias | Preserve with clarity | `Legacy project name: Orca`, `orca_start_preflight` alias |
| Compatibility identifier | Preserve until moved-path/rollback migration | `orca/product/`, `orca-harness/`, `orca-product-lead`, `orca_*` package/file names, `docs/workflows/orca_repo_map_v0.md` |
| Scratch/inbox | Leave unless promoted | `docs/_inbox/**` |
| Live human-facing defect | Patch or queue with owner | current authority/doc/prose that says Orca as the project/product name without legacy/compatibility context |

## Compatibility Units

These are the only plausible later migration units visible from the sampled control surfaces:

| Unit | Current boundary | Required before rename |
| --- | --- | --- |
| `orca/product/` root | accepted product tree and route surface | moved-path index, repo-map/retrieval repoint, import/path search, rollback notes, validation gates |
| `orca-harness/` root | runtime/package/test working directory | packaging/import/test/CI plan, branch-protection/check-name impact analysis, rollback notes |
| `docs/workflows/orca_repo_map_v0.md` | live repo map path | renamed successor plus all inbound references and checker expectations updated |
| `orca-product-lead` skill ID | accepted local skill command/path | resolver/deployment/collision analysis, source/deployment copy plan, rollback notes |
| `orca_*` filenames/import-package paths | compatibility filenames and packages | per-family moved-path index, import/reference rewrite, tests |
| CI and automation IDs | `orca-harness-tests`, risk-router markers | explicit downstream dependency review before changing check IDs |

## Non-Claims

- This inventory is not validation, readiness, source promotion, implementation authorization, or path/package migration.
- This inventory does not classify all 28,806 matched lines.
- A remaining Orca hit is not a defect without classifying it under the rename policy.
- The final stale-reference audit remains Step 5.

## Recheck Recipe

```powershell
rg -l -i "\bOrca\b|\bORCA\b|orca_start_preflight" AGENTS.md README.md CLAUDE.md .agents .github docs orca orca-harness repo-structure.yaml | Measure-Object
rg -n -i "\bOrca\b|\bORCA\b|orca_start_preflight" AGENTS.md README.md CLAUDE.md .agents .github docs orca orca-harness repo-structure.yaml | Measure-Object
rg --files | rg -i "(^|[\\/])(orca|orca-|orca_)|orca-harness|orca-product-lead|orca_repo_map" | Measure-Object
```
