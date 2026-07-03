# Commission Signal Board Moved Paths Index v0

```yaml
retrieval_header_version: 1
artifact_role: Moved-path index
scope: Canonical old-path to new-path resolver for the Commission Signal Board pilot spine.
use_when:
  - Resolving old Commission Signal Board paths under docs/.
  - Updating prompts, wrappers, handoffs, or repo-map entries after the CSB spine migration.
  - Checking which CSB-adjacent executable surfaces intentionally did not move.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/commission_signal_board/README.md
  - docs/decisions/orca_repo_structure_binding_v0.md
stale_if:
  - Another Commission Signal Board artifact moves.
  - Global Orca docs move to orca/docs/.
  - The CSB validator or tests move out of their current homes.
```

- Status: ACTIVE_MOVED_PATH_INDEX.
- Scope: Commission Signal Board pilot only.
- Global docs move: staged, not executed.
- Current-main reconciliation: `orca/product/spines/commission_signal_board/migrations/commission_signal_board_current_main_reconciliation_v0.md`.

## Moved Canonical Docs

| Old path | Canonical path | Resolution |
| --- | --- | --- |
| `docs/product/product_lead/orca_commission_signal_board_prompt_adjudication_packet_v0.md` | `orca/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_structure_rules_v0.md` | Old path is absent on current `main`; use the canonical spine path. |
| `docs/prompts/product-planning/orca_commission_signal_board_prompt_v0.md` | `orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_structure_v0.md` | Old path is absent on current `main`; use the canonical spine path. |
| `docs/workflows/commission_signal_board_playbook_v0.md` | `orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md` | Old path is absent on current `main`; use the canonical spine path. |

## Indexed But Not Moved

| Current path | Spine pointer | Reason not moved |
| --- | --- | --- |
| `.agents/hooks/check_commission_signal_board_output.py` | `orca/product/spines/commission_signal_board/harness/validator.md` | Shared manual/local hook substrate stays global during the pilot. |
| `orca-harness/tests/unit/test_commission_signal_board_output_validator.py` | `orca/product/spines/commission_signal_board/tests/validator_tests.md` | Executable tests stay with the harness until separate code-root migration authority exists. |
| `orca-harness/tests/fixtures/commission_signal_board_outputs/` | `orca/product/spines/commission_signal_board/tests/validator_tests.md` | Fixtures remain bound to the executable harness test suite. |

## Historical Records Absent On Current Main

These paths are historical CSB lane names that older handoffs or packets may
mention, but they are not present on current `main`. Do not route live CSB work
through them unless a later branch restores or explicitly imports them. Recheck
with `git cat-file -e HEAD:<path>` before relying on any older packet that names
one of these files.

| Historical path | Current resolution |
| --- | --- |
| `docs/prompts/handoffs/commission_signal_board_spine_pilot_reconciliation_handoff_prompt_v0.md` | No current-main artifact observed; historical copy on branch `origin/codex/commission-spine-structure` (PR #239, closed unmerged); use the live CSB spine entry points instead. |
| `docs/migration/commission_signal_board_migration_inventory_v0.md` | No current-main artifact observed; use this moved-path index and the Phase-2 CSB proposal for current structure context. |
| `docs/migration/commission_signal_board_spine_pilot_migration_plan_v0.md` | No current-main artifact observed; use this moved-path index and the live CSB spine entry points instead. |

## Reverse Plan

If the pilot spine is reverted before global docs migration, restore the three
canonical docs to their old paths and delete the three stubs. Do not move the
validator, tests, fixtures, repo map, structure binding, or overlay files as
part of that reverse unless a later decision explicitly authorizes it.
