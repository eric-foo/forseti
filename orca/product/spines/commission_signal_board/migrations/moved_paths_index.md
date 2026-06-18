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

## Moved Canonical Docs

| Old path | Canonical path | Resolution |
| --- | --- | --- |
| `docs/product/product_lead/orca_commission_signal_board_prompt_adjudication_packet_v0.md` | `orca/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_adjudication_packet_v0.md` | Old path is a resolver stub. |
| `docs/prompts/product-planning/orca_commission_signal_board_prompt_v0.md` | `orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md` | Old path is a resolver stub. |
| `docs/workflows/commission_signal_board_playbook_v0.md` | `orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md` | Old path is a resolver stub. |

## Indexed But Not Moved

| Current path | Spine pointer | Reason not moved |
| --- | --- | --- |
| `.agents/hooks/check_commission_signal_board_output.py` | `orca/product/spines/commission_signal_board/harness/validator.md` | Shared manual/local hook substrate stays global during the pilot. |
| `orca-harness/tests/unit/test_commission_signal_board_output_validator.py` | `orca/product/spines/commission_signal_board/tests/validator_tests.md` | Executable tests stay with the harness until separate code-root migration authority exists. |
| `orca-harness/tests/fixtures/commission_signal_board_outputs/` | `orca/product/spines/commission_signal_board/tests/validator_tests.md` | Fixtures remain bound to the executable harness test suite. |
| `docs/prompts/handoffs/commission_signal_board_spine_pilot_reconciliation_handoff_prompt_v0.md` | none | Historical handoff prompt remains in the global handoff prompt archive. |
| `docs/migration/commission_signal_board_spine_pilot_migration_plan_v0.md` | this index | Global migration planning record remains under `docs/migration/`. |

## Reverse Plan

If the pilot spine is reverted before global docs migration, restore the three
canonical docs to their old paths and delete the three stubs. Do not move the
validator, tests, fixtures, repo map, structure binding, or overlay files as
part of that reverse unless a later decision explicitly authorizes it.
