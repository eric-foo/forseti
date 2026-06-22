# Commission Signal Board Spine

```yaml
retrieval_header_version: 1
artifact_role: Spine README
scope: Entry point for the live Commission Signal Board pilot spine.
use_when:
  - Starting Commission Signal Board prompt, playbook, validator, or migration work.
  - Checking which CSB artifacts are canonical after the spine-first pilot authorization.
  - Distinguishing the live CSB pilot from the staged global docs migration.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/commission_signal_board/spine.yaml
  - orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md
  - orca/product/spines/commission_signal_board/migrations/moved_paths_index.md
stale_if:
  - The Commission Signal Board spine is renamed, retired, or merged into another spine.
  - The executable validator moves out of .agents/hooks.
  - Global Orca docs move to orca/docs/.
```

- Status: LIVE_PILOT_SPINE.
- Owner authorization: current-turn authorization, 2026-06-18.
- Current scope: Commission Signal Board only.
- Global docs migration: accepted in direction, staged, not executed here.

## Canonical Artifacts

| Role | Path |
| --- | --- |
| Spine manifest | `orca/product/spines/commission_signal_board/spine.yaml` |
| Authority packet | `orca/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_adjudication_packet_v0.md` |
| Prompt | `orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md` |
| Playbook | `orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md` |
| Validator pointer | `orca/product/spines/commission_signal_board/harness/validator.md` |
| Test pointer | `orca/product/spines/commission_signal_board/tests/validator_tests.md` |
| Moved-path index | `orca/product/spines/commission_signal_board/migrations/moved_paths_index.md` |

## Boundaries

This spine does not authorize retrieval, scraping, capture, graph construction,
demand classification, forecasting, judgment, buyer proof, validation,
readiness, CI, hook wiring, or runtime work.

The executable validator remains at
`.agents/hooks/check_commission_signal_board_output.py`. The executable tests
and fixtures remain under `orca-harness/tests/`.

## Old Paths

The old CSB doc paths under `docs/` are absent on current `main`. Use the
moved-path index before following historical links or older handoff packets:

```text
orca/product/spines/commission_signal_board/migrations/moved_paths_index.md
```
