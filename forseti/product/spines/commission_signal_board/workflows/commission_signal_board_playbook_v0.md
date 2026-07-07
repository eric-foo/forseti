# Commission Signal Board Playbook v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow playbook
scope: >
  Operating sequence for running the Commission Signal Board lane and its local
  handoff-row validator without confusing intake blockers, full board outputs,
  retrieval, demand classification, graph construction, or proof claims.
use_when:
  - Dispatching or rerunning the Commission Signal Board prompt.
  - Deciding whether a Commission Signal Board output is ready for retrieval or classifier handoff routing.
  - Diagnosing validator failures on Commission Signal Board outputs.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
  - .agents/hooks/check_commission_signal_board_output.py
  - orca-harness/tests/fixtures/commission_signal_board_outputs/
stale_if:
  - The Commission Signal Board prompt output contract changes.
  - The Commission Signal Board validator changes its required sections, fields, or finding codes.
  - Commission boards gain a durable artifact location or CI enforcement path.
```

- Playbook path: `forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md`.
- Prompt Structure path: `forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md`.
- Prompt Structure Rules path: `forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md`.
- Validator path: `.agents/hooks/check_commission_signal_board_output.py`.
- Validator fixture path: `orca-harness/tests/fixtures/commission_signal_board_outputs/`.
- Current enforcement posture: manual/local checker. Not CI, not pre-commit, not a write hook.

## Purpose

This playbook tells agents how to run a Commission Signal Board lane without
skipping the intake check or overclaiming the validator.

The lane has three different objects:

| Object | What it is | Validator applies? |
| --- | --- | --- |
| Intake scaffold | A request for missing commission inputs | No |
| Full Commission Signal Board | The Section 1-10 board output | Yes, after it is saved to a file |
| Retrieval/classifier work | Downstream lanes that may consume the board | No, separate authority |

## Operating Sequence

1. Read the prompt and this playbook.
2. Check required inputs:
   - `mode`
   - `candidate_or_subject`
   - `decision_context`
   - `evidence_cutoff_at` when `mode: backtest`
3. If required inputs are missing, return the prompt's intake scaffold and stop.
   Do not run the validator.
4. If inputs are complete, generate the full board with Sections 1-10.
5. Save the exact board output to a temporary file or a bound durable artifact.
6. Run the validator against that saved full board output (see Validator Command section).
7. If the validator passes, the board is mechanically safe for handoff-row
   packaging only.
8. If the validator fails, fix the board output or report the finding codes.
   Do not hand rows to a classifier until the validator passes.

## Validator Command

From the repo root:

```powershell
python -B .agents\hooks\check_commission_signal_board_output.py <board-output-file>
```

Selftest:

```powershell
python -B .agents\hooks\check_commission_signal_board_output.py --selftest
```

Focused pytest suite:

```powershell
cd orca-harness
python -B -m pytest -q -p no:cacheprovider tests\unit\test_commission_signal_board_output_validator.py
```

## Validator Applicability

Run the validator only when the saved output is a full board with Sections 1-10
in the prompt-defined order, including:

- `### 4. Signal Board Rows`;
- `### 8. Demand-Classifier Handoff Packet`;
- `### 10. Board Status And Run Boundary`.

Do not run it against intake-only output. A `NEEDS_COMMISSION_INTAKE` or
`NEEDS_CUTOFF_DATE` response is expected to fail the full-section contract,
because it is not a board.

## What The Validator Checks

The validator first checks full-board structure: Sections 1-10 must appear in
the prompt-defined order, Section 4 must have its Markdown table and required
columns (`row_id`, `source_family`, `signal_role`, `row_purpose`,
`recency_status`, `recency_attention`, `graph_role`, `graph_weight_hint`,
`evidence_status`, `surface_cutoff_status`, `cutoff_status`), Section 8 must
contain a valid YAML
`classifier_handoff_packet`, and Section 10 must contain valid board-status
YAML. It fails malformed Section 4 rows, missing row IDs, duplicate row IDs,
row IDs not matching `SBR-NNN` format, non-monotonic row IDs, invalid Section 4 controlled
vocabulary values including recency/current-state fields, missing Section 8 handoff packet fields, invalid
`classifier_mapping_status`, invalid `prohibited_claims` shape, invalid
`board_status`, invalid `run_boundary`, and missing `next_authorized_step`.

Before the handoff-row cross-check, it also fails on mechanical
engagement/resonance overclaim language that turns public reaction into proof,
graph weight, Commit/Scale support, credibility, Action Ceiling, or final
resonance weight.

After structure passes far enough to parse rows and the handoff packet, the
validator cross-checks rows listed in Section 8 against the Section 4 table. It
fails when the handoff packet has a missing or invalid `mode` field, or when a
referenced handoff row:

- is unknown;
- is not `source_backed`;
- is `excluded_future_info`;
- is AEO / answer-engine visibility;
- in backtest mode, lacks `surface_cutoff_status: existed_by_cutoff`;
- in backtest mode, lacks `cutoff_status: in_window`.

Valid handoff modes are `backtest` and `forward`; unknown or placeholder modes
fail instead of silently bypassing cutoff enforcement.

## What A Pass Means

A pass means:

```text
Rows listed in the classifier handoff are mechanically eligible under the
board's own row table.
```

A pass does not mean:

- evidence is true;
- evidence was retrieved;
- demand exists;
- the board is exhaustive;
- graph construction is complete;
- classifier mapping is correct;
- buyer proof, validation, readiness, forecast, or client-facing claims are allowed.

## How Agents Discover This Lane

Agents should discover this playbook from:

- the Commission Signal Board prompt `open_next`;
- the repo map Product Anchor Files section;
- the repo map Active Hooks / Manual Checkers section;
- downstream wrappers or handoffs that name this playbook before board generation.

If an agent sees "Commission Signal Board", "commissioning board", or
"commission board output", it should open this playbook before running or
validating the board.

## Current Non-Goals

- Do not add CI or pre-commit enforcement until board artifact paths are
  standardized.
- Do not make the validator run on chat-only intake scaffolds.
- Do not turn the validator into demand classification, graph scoring, evidence
  weighting, retrieval, or proof review.
- Do not treat validator pass as approval or readiness.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Commission Signal Board operation now has a discoverable playbook route:
    agents must check intake first, produce a full board only when required
    inputs are supplied, and run the manual/local validator only against full
    board outputs before making a classifier-handoff mechanical-safety claim.
  trigger: workflow_authority
  related_triggers:
    - validation_philosophy
  controlling_sources_updated:
    - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
    - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
    - forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md
    - .agents/hooks/check_commission_signal_board_output.py
    - orca-harness/tests/unit/test_commission_signal_board_output_validator.py
    - orca-harness/tests/fixtures/commission_signal_board_outputs/
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/hooks/check_commission_signal_board_output.py
    - orca-harness/tests/fixtures/commission_signal_board_outputs/
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        AGENTS.md already routes Orca project rules to the overlay and durable
        docs; adding a Commission Signal Board special case would fork the
        playbook.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The validator remains manual/local, not a CI or hook gate. The
        enforcement-placement principle already lives here; no active validation
        gate is being registered yet.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Source-loading packs are unchanged; this playbook is a run sequence for
        an existing prompt and checker.
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        Prompt-orchestration mechanics are unchanged; the board prompt now
        points to this playbook instead of forking prompt-policy.
  stale_language_search: >
    rg -n "Commission Signal Board|commission_signal_board|check_commission_signal_board|NEEDS_COMMISSION_INTAKE|validator target|classifier handoff"
    docs .agents orca-harness -S
    and
    rg -n "run the validator|validator applies|manual/local|NOT hook-wired|intake-only"
    docs .agents orca-harness -S
    (executed 2026-06-18)
  stale_language_search_result: >
    The old optional-recency validator wording produced only receipt search-string
    hits, not live instructional hits. Scoped validator hits are the updated
    Prompt Structure, playbook, Prompt Structure Rules doc, validator, tests,
    fixtures, adjudication packet, and repo-map discovery entries. No checked
    live surface instructed agents to run the validator on intake-only output,
    skip the playbook for Commission Signal Board work, treat the checker as
    CI/pre-commit/write-hook enforcement, omit required recency row fields, or
    treat validator pass as evidence truth, demand classification, proof, graph
    weight, recency proof, or readiness.
  non_claims:
    - not validation
    - not readiness
    - not CI enforcement
    - not pre-commit enforcement
    - not demand classification
    - not evidence retrieval
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
