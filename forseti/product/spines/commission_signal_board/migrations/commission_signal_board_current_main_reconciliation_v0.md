# Commission Signal Board Current-Main Reconciliation v0

```yaml
retrieval_header_version: 1
artifact_role: Orca migration note
scope: >
  Current-main reconciliation for the Commission Signal Board spine after the
  stale-path correction in PR #307.
use_when:
  - Restarting CSB work after an older handoff names pre-spine or absent paths.
  - Checking whether old CSB inventory, migration-plan, or handoff artifacts are live on current main.
  - Deciding which current CSB sources to open before prompt, playbook, validator, or migration work.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/commission_signal_board/README.md
  - forseti/product/spines/commission_signal_board/migrations/moved_paths_index.md
  - docs/migration/phase2_proposals/commission_signal_board_w3a_proposal_v0.md
branch_or_commit: origin/main @ bc950cdfeeb3a02f33bf52217d71e049aa9093f2
stale_if:
  - The Commission Signal Board spine is renamed, retired, or moved.
  - Any historical CSB path listed below is restored or imported on main.
  - A Phase-2 execute PR changes the commission_signal_board spine area.
  - Global Orca docs move to orca/docs/.
```

## Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3 CSB current-main reconciliation
  edit_permission: docs-write
  target_scope: CSB migration/restart reconciliation note; no prompt, runtime, validator, or readiness change
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md, overlay README, source-loading, artifact-folders, retrieval-metadata, CSB README, spine.yaml, moved-path index, Phase-2 CSB proposal
```

## Current-Main State

Observed authoring baseline: `origin/main` at
`bc950cdfeeb3a02f33bf52217d71e049aa9093f2`, the merge commit for PR #307.
Current landed baseline after PR #310: `origin/main` at
`780091959c778562a19984596b9d45645c8c1edf`, the merge commit for PR #310.

Branch-local note: the later `codex/search-surface-mgt-p0-captures-ws`
rename to Prompt Structure / Prompt Structure Rules has not landed on
`origin/main` at these pins. This section intentionally records the filenames
present on the pinned main commits; re-pin and update it after that rename
lands.

The live CSB spine path remains:

```text
forseti/product/spines/commission_signal_board/
```

The pinned current-main tree contains these CSB spine files:

```text
forseti/product/spines/commission_signal_board/README.md
forseti/product/spines/commission_signal_board/spine.yaml
forseti/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_adjudication_packet_v0.md
forseti/product/spines/commission_signal_board/dispatch_rules/orca_demand_gate_run_commission_criteria_v0.md
forseti/product/spines/commission_signal_board/harness/validator.md
forseti/product/spines/commission_signal_board/migrations/commission_signal_board_current_main_reconciliation_v0.md
forseti/product/spines/commission_signal_board/migrations/moved_paths_index.md
forseti/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md
forseti/product/spines/commission_signal_board/tests/validator_tests.md
forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
```

At those pinned main baselines, the old canonical doc paths under `docs/` are
absent; resolution from `docs/` paths went to the then-current spine filenames
listed above. This branch's later rename is a forward branch-local change until
merged.

## Historical Paths Not Live

Fresh `git cat-file -e HEAD:<path>` checks failed for these historical paths on
the observed baseline:

```text
docs/product/product_lead/orca_commission_signal_board_prompt_adjudication_packet_v0.md
docs/prompts/product-planning/orca_commission_signal_board_prompt_v0.md
docs/workflows/commission_signal_board_playbook_v0.md
docs/prompts/handoffs/commission_signal_board_spine_pilot_reconciliation_handoff_prompt_v0.md  (historical copy on branch origin/codex/commission-spine-structure, PR #239 closed unmerged)
docs/migration/commission_signal_board_migration_inventory_v0.md
docs/migration/commission_signal_board_spine_pilot_migration_plan_v0.md
```

Do not route live CSB work through those paths unless a later branch restores or
explicitly imports them.

## Phase-2 Proposal Relationship

`docs/migration/phase2_proposals/commission_signal_board_w3a_proposal_v0.md`
is an owner-adjudication input for deletion and ontology/doc-term health in the
CSB spine area. It reports no deletion candidates for the CSB spine area and a
clean ontology/doc-term scan. It does not validate CSB readiness, recover absent
historical records, or authorize runtime work.

## Next Safe CSB Entry

For any future CSB prompt, playbook, validator, or migration work, start from:

```text
forseti/product/spines/commission_signal_board/README.md
forseti/product/spines/commission_signal_board/spine.yaml
forseti/product/spines/commission_signal_board/migrations/moved_paths_index.md
```

Use this note only to avoid stale restart assumptions; use the live spine
artifacts for CSB behavior.

## Non-Claims

- Not CSB readiness, validation, proof, or owner acceptance.
- Not a migration execution or file recovery.
- Not a prompt, wrapper, handoff, validator change, CI change, or runtime authorization.
- Not authorization for retrieval, scraping, capture, graph construction,
  demand classification, forecasting, Judgment, buyer proof, or client-facing use.
