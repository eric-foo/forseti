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
  - forseti/product/spines/commission_signal_board/spine.yaml
  - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
  - forseti/product/spines/commission_signal_board/migrations/moved_paths_index.md
stale_if:
  - The Commission Signal Board spine is renamed, retired, or merged into another spine.
  - The executable validator moves out of .agents/hooks.
  - Global Forseti docs move into a product-root docs subtree.
```

- Status: LIVE_PILOT_SPINE.
- Owner authorization: current-turn authorization, 2026-06-18.
- Current scope: Commission Signal Board only.
- Global docs migration: accepted in direction, staged, not executed here.

## Canonical Artifacts

| Role | Path |
| --- | --- |
| Spine manifest | `forseti/product/spines/commission_signal_board/spine.yaml` |
| Prompt Structure Rules | `forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md` |
| Prompt Structure | `forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md` |
| Playbook | `forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md` |
| Validator pointer | `forseti/product/spines/commission_signal_board/harness/validator.md` |
| Test pointer | `forseti/product/spines/commission_signal_board/tests/validator_tests.md` |
| Moved-path index | `forseti/product/spines/commission_signal_board/migrations/moved_paths_index.md` |

Naming note: **Prompt Structure** is the runnable CSB prompt/template. **Prompt Structure Rules** is the durable authority/rules doc for that prompt structure. File paths now use role-aligned names.

## Legacy Non-Controlling Artifacts

| Artifact | Status | Current authority |
| --- | --- | --- |
| `forseti/product/spines/commission_signal_board/dispatch_rules/forseti_demand_gate_run_commission_criteria_v0.md` | Historical only; not a live CSB dispatch rule | Use the CSB prompt and playbook. CSB is an evidence/signals-only board and must not emit admit/hold/fail gate verdicts. |

## Boundaries

This spine does not authorize retrieval, scraping, capture, graph construction,
demand classification, forecasting, judgment, buyer proof, validation,
readiness, CI, hook wiring, or runtime work. Public-reaction engagement belongs
in CSB as resonance/routing context only; the authority and prompt artifacts keep
it separate from proof, Commit/Scale support, graph weight, classifier mapping,
final resonance weight, and Action Ceiling.

The executable validator remains at
`.agents/hooks/check_commission_signal_board_output.py`. The executable tests
and fixtures remain under `orca-harness/tests/`.

## Old Paths

The old CSB doc paths under `docs/` are absent on current `main`. Use the
moved-path index before following historical links or older handoff packets:

```text
forseti/product/spines/commission_signal_board/migrations/moved_paths_index.md
```
