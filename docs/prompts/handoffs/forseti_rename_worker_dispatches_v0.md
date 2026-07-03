# Forseti Rename Worker Dispatches v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti prompt artifact
scope: Cross-recipient worker dispatches for Forseti rename batches after authority/doctrine rename.
use_when:
  - Spawning subagents to continue the Forseti rename migration.
  - Checking worker scope, write boundaries, and return shape for rename batches.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_rename_migration_policy_v0.md
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/prompt-orchestration.md
```

## Prompt Preflight

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write for workers A and B; read-only for worker C
  target_scope: Forseti rename continuation after authority/doctrine batch commit 81a8a7f6
  dirty_state_checked: yes
  blocked_if_missing: docs/decisions/forseti_rename_migration_policy_v0.md
output_mode: file-write
prompt_artifact_path: docs/prompts/handoffs/forseti_rename_worker_dispatches_v0.md
template_kind: handoff
branch: codex/forseti-rename-authority
base_commit: 81a8a7f6
repo_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\forseti-rename
reviews: findings-first if worker identifies defects; no runtime-model recommendation
Doctrine change: yes; governed by docs/decisions/forseti_rename_migration_policy_v0.md
```

## Shared Worker Rules

- You are not alone in the codebase. Do not revert or overwrite changes made by other workers.
- Start from the current branch after authority/doctrine commit `81a8a7f6`.
- Read `AGENTS.md`, `.agents/workflow-overlay/README.md`, `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/source-of-truth.md`, and `docs/decisions/forseti_rename_migration_policy_v0.md` before editing.
- Follow the rename classes in the policy: live authority/current sources should say Forseti; historical prompts, reviews, old DCP receipts, and scratch/inbox material remain Orca by default; lowercase compatibility paths remain until explicitly migrated.
- Do not rename directories, packages, imports, hooks, or skill IDs unless your worker task explicitly authorizes that exact write scope.
- Do not edit `AGENTS.md`, `.agents/workflow-overlay/**`, `README.md`, `CLAUDE.md`, `repo-structure.yaml`, or `docs/workflows/orca_repo_map_v0.md`; those were handled in Batch 0/1.
- Do not touch `docs/prompts/**` or `docs/review-outputs/**` unless your worker task explicitly names them; most prompt/review artifacts are historical.
- Preserve historical provenance. Add transition notes only to currently-live route surfaces.

Return exactly this schema:

```text
worker_id:
branch:
base_commit:
head_commit_or_uncommitted: <commit sha, uncommitted, or none>
push_pr_state: <not_pushed | pushed | pr_open | not_applicable>
merged: no
scope_completed: yes/no
files_changed:
  - path:line - one-line change summary
validation:
  - command - PASS/FAIL/NOT_RUN and reason
remaining_orca_hits:
  - category: <historical | compatibility | alias | defect | none> path:line summary
blockers:
  - none | blocker text
```

## Worker A: Product And Architecture Live Docs

Task: Patch current product and architecture source prose so live, controlling docs say Forseti where they refer to the project/product, while preserving historical paths and historical provenance.

Write scope:
- `docs/decisions/orca_product_thesis_consumer_demand_v0.md`
- `docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md`
- `orca/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md`
- `orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md`
- `orca/product/spines/product_lead/proof_charter/orca_product_proof_lead_charter_v0.md`
- `orca/product/spines/product_lead/proof_charter/orca_claim_defense_doctrine_v0.md`
- `orca/product/spines/foundation/product_contract/core_spine_v0_product_contract.md`
- `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `orca/product/spines/foundation/product_contract/core_spine_v0_information_production_foundation_v0.md`

Do not move or rename files. Do not patch old prompts/reviews. If a listed file is clearly historical/superseded, leave its body unchanged and report it.

Validation: run `rg -n "\bOrca\b|\bORCA\b" <your write scope>` and classify remaining hits.

## Worker B: Active Prompt Templates And Shared Prompt Defaults

Task: Patch active, reusable prompt-template/default surfaces so future generated prompts say Forseti. Leave historical one-off prompts alone.

Write scope:
- `docs/prompts/templates/**`
- only active shared/default prompt surfaces under `docs/prompts/**` that are templates or reusable wrappers; do not edit historical one-off prompt artifacts.

Do not edit `.agents/workflow-overlay/**`; Batch 0/1 already did. Do not edit review outputs.

Validation: run `rg -n "\bOrca\b|\bORCA\b|orca_start_preflight" docs/prompts/templates docs/prompts -g "*.md"` and classify hits as updated, historical, compatibility alias, or defect. If the scope is too broad or ambiguous, stop after the template subtree and report the boundary.

## Worker C: Compatibility Migration Inventory Only

Task: Produce a read-only inventory for the later compatibility/path migration. Do not edit files.

Read scope:
- `repo-structure.yaml`
- `docs/workflows/orca_repo_map_v0.md`
- `.agents/hooks/**`
- `.github/**`
- `orca-harness/**` metadata/config/import surfaces only; do not read all fixtures/data
- `.agents/skills/orca-product-lead/SKILL.md`
- `.claude/skills/orca-product-lead/SKILL.md` if present in this worktree

Inventory these migration units:
- `orca/product/` to a future `forseti/product/` or alternative;
- `orca-harness/` to a future `forseti-harness/` or alternative;
- `orca-product-lead` to a future `forseti-product-lead` or alias strategy;
- `orca_*` filenames that are live route/authority surfaces rather than historical records;
- hook/checker messages that still say Orca in live runtime output.

Return: a concise file-by-file plan with risk, dependencies, validation commands, and whether the unit should be moved, aliased, or deferred. No edits.