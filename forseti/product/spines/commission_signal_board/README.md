# Commission Signal Board Spine

```yaml
retrieval_header_version: 1
artifact_role: Spine README
scope: Entry point for the live Commission Signal Board spine, including standard and one-company competitive-intelligence profiles.
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

## Commission Profiles And Time Postures

CSB keeps the existing `mode: backtest | forward` axis unchanged and adds two
orthogonal fields:

- `commission_profile: standard_signal_board | company_competitive_intelligence`;
- `time_posture: recency_first | longitudinal`.

`recency_first` is the universal default and uses the canonical prompt's
deterministic 0-30, 31-90, 91-180, and over-180-day ladder. `longitudinal` is an
explicit override only for change, recurrence, or trajectory across a declared
period and requires both the period and rationale. A named event is a route or
query inside one of these two postures, not another posture.

A commission for one company subject defaults to
`company_competitive_intelligence` when the subject is a Brand or Org, including
an unresolved Brand/Org identity. That profile produces the conditional
ten-section company report and no demand-classifier handoff. Other commissions
continue to use the existing standard Sections 1-10 and classifier handoff.

## Legacy Non-Controlling Artifacts

| Artifact | Status | Current authority |
| --- | --- | --- |
| `forseti/product/spines/commission_signal_board/dispatch_rules/forseti_demand_gate_run_commission_criteria_v0.md` | Historical only; not a live CSB dispatch rule | Use the CSB prompt and playbook. CSB is an evidence/signals-only board and must not emit admit/hold/fail gate verdicts. |

## Boundaries

CSB owns commission profiles, source-family requirements, time posture, and
typed gaps/requests. Scanning owns the intelligent walk, exact-query and
category-aware hidden-venue discovery, negatives, access notes, and frontier
closeout. Capture owns lawful source access and preservation adapters. CSB does
not contain venue or research modules and does not fake either downstream act.

This spine does not authorize retrieval, scraping, capture, graph construction,
demand classification, forecasting, judgment, buyer proof, validation,
readiness, CI, hook wiring, or runtime work. Public-reaction engagement belongs
in CSB as resonance/routing context only; the authority and prompt artifacts keep
it separate from proof, Commit/Scale support, graph weight, classifier mapping,
final resonance weight, and Action Ceiling.

The executable validator remains at
`.agents/hooks/check_commission_signal_board_output.py`. The executable tests
and fixtures remain under `forseti-harness/tests/`.

Company reports remain one-company-at-a-time and decision-neutral. They may use
bounded comparator pointers to interpret the subject, but deep competitor
treatment requires a separately named follow-up commission. Their Company
Surface ledger is candidate-only: no import, identity resolution, stored
corpus, or Company Surface mutation occurs in CSB.

## Old Paths

The old CSB doc paths under `docs/` are absent on current `main`. Use the
moved-path index before following historical links or older handoff packets:

```text
forseti/product/spines/commission_signal_board/migrations/moved_paths_index.md
```
