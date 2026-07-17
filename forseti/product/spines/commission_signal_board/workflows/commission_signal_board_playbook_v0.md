# Commission Signal Board Playbook v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow playbook
scope: >
  Operating sequence for standard signal-board and one-company competitive-
  intelligence commissions, including conditional local validation without
  confusing CSB profiling with retrieval, capture, classification, or proof.
use_when:
  - Dispatching or rerunning the Commission Signal Board prompt.
  - Deciding whether a standard board is ready for classifier-handoff routing or a company report is mechanically complete.
  - Diagnosing validator failures on Commission Signal Board outputs.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
  - .agents/hooks/check_commission_signal_board_output.py
  - forseti-harness/tests/fixtures/commission_signal_board_outputs/
stale_if:
  - The Commission Signal Board prompt output contract changes.
  - The Commission Signal Board validator changes its required sections, fields, or finding codes.
  - Commission boards gain a durable artifact location or CI enforcement path.
```

- Playbook path: `forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md`.
- Prompt Structure path: `forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md`.
- Prompt Structure Rules path: `forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md`.
- Validator path: `.agents/hooks/check_commission_signal_board_output.py`.
- Validator fixture path: `forseti-harness/tests/fixtures/commission_signal_board_outputs/`.
- Current enforcement posture: manual/local checker. Not CI, not pre-commit, not a write hook.

## Purpose

This playbook keeps four objects distinct:

| Object | What it is | Validator applies? |
| --- | --- | --- |
| Intake scaffold | A request for missing commission inputs | No |
| Standard signal board | Existing standard Sections 1-10 with classifier handoff | Yes |
| Commission-stage company board | Conditional company Sections 1-10 sealed before scanning: `run_boundary: COMMISSION_SEALED_PRE_SCAN`, `not_checked` coverage rows as the commissioned scan routes, scout statuses may be `commissioned_not_yet_run` | Yes |
| Company competitive-intelligence report | Conditional company Sections 1-10 with typed ledgers, earned scout statuses, and no classifier handoff | Yes |
| Scanning, Capture, or classifier work | Downstream execution under its owning spine | No |

CSB owns the commission profile, source-family requirements, time posture, and
typed gaps/requests. Scanning owns the intelligent walk. Capture owns venue
access and preservation adapters. This playbook does not authorize downstream
runtime. CSB defines decision-material information jobs and candidate routes; it
does not freeze the participant packet, decide final inclusion, or declare
acquisition complete.

## Operating Sequence

1. Read the prompt and this playbook.
2. Preserve `mode: backtest | forward`. Determine `commission_profile`:
   - default a one-company Brand or Org subject, including unresolved Brand/Org
     identity, to `company_competitive_intelligence`;
   - otherwise use `standard_signal_board` unless explicitly overridden.
3. Default `time_posture` to `recency_first`. Use `longitudinal` only when the
   commission explicitly asks about change, recurrence, or trajectory and
   declares both a period and rationale.
4. Check profile-specific required inputs. Return the prompt's intake scaffold
   if any are missing; intake-only output is not a validator target.
5. Include an item only when its named job can materially change the action,
   action ceiling, rival assessment, or hold condition and no equal-or-better
   included item performs that job. Use exclusion or `not_applicable` records
   for dominated routes.
6. For a recurring or actively radarred source family, put a lake-first
   preflight in the downstream request: relevant Silver/current view, then
   packet or catalog inventory, then raw material when necessary. Treat the
   result as reuse/freshness/coverage context, not current-world proof.
7. Generate exactly the selected profile's Sections 1-10.
8. Save the exact output to a temporary file or bound durable artifact.
9. Run the validator. If it fails, repair the output or report its finding
   codes. Do not run downstream work from a failing report.
10. Route typed source requests to Scanning or Capture under their own
    authority. Do not execute retrieval from this playbook. Scanning decides
    marginal acquisition, dominance, and closure; Capture fulfills the bounded
    request or returns typed failure/route exhaustion.

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
cd forseti-harness
python -B -m pytest -q -p no:cacheprovider tests\unit\test_commission_signal_board_output_validator.py
```

## Validator Applicability

Run the validator only against a full output with profile-specific Sections
1-10 in canonical order.

- `standard_signal_board` requires the existing `Signal Board Rows`,
  `Demand-Classifier Handoff Packet`, and `Board Status And Run Boundary`.
- `company_competitive_intelligence` requires `Company Commission And Identity
  Receipt` through `Completion Ledger And Run Boundary` and must not contain a
  classifier handoff. This includes commission-stage company boards
  (`run_boundary: COMMISSION_SEALED_PRE_SCAN`): they are full ten-section
  outputs and are validated; the validator enforces that the commission-stage
  boundary coexists with `not_checked` coverage rows and that
  `commissioned_not_yet_run` scout statuses appear only at that stage. It also
  cross-checks each Reddit/Quora scout status against the corresponding
  coverage-row status and yield so the completion ledger cannot claim a result
  the route ledger did not earn.

Do not run it against `NEEDS_COMMISSION_INTAKE` or `NEEDS_CUTOFF_DATE`.

## What The Validator Checks

For `standard_signal_board`, the established structure, row vocabulary,
backtest cutoff, engagement-overclaim, and classifier-handoff checks remain
unchanged.

For `company_competitive_intelligence`, the validator checks:

- one-company identity and default profile routing;
- `mode` and orthogonal `time_posture`;
- deterministic recency tiers and age-use rules;
- declared period and rationale for `longitudinal`;
- source-family coverage, the Reddit `mandatory_bounded_scout` compatibility
  row, the initial-proving Quora compatibility row, category-aware forum
  discovery, typed gaps, and justified `not_applicable`. The Reddit/Quora rows
  are search-hygiene considerations: they may document non-selection and do not
  authorize acquisition or earn completion credit without a named
  non-dominated information job;
- observation-level URL, publisher, publication/event/access dates, evidence
  status, source class, fact domain, and syndication group;
- shared source-family vocabulary, typed `effective_time_precision` and
  `age_anchor_basis`, current-page versus dated-event separation, and no old
  evidence relabeled current;
- community evidence as external/customer evidence only;
- decision-neutral company lenses and prohibited GTM keys;
- Company Surface rows as `candidate_only` and `not_imported`;
- completion ledger, explicit gaps/requests, no arbitrary caps, typed
  `run_boundary` and `next_authorized_step`, Reddit/Quora scout-status
  consistency with their coverage rows, and no classifier handoff;
- document-wide `OBS-###` references resolve to observation-ledger rows
  (`dangling_observation_reference`);
- the shared engagement/resonance overclaim ban, which applies to both profiles.

## What A Pass Means

A standard pass means its classifier-handoff rows are mechanically eligible
under the board's own row table. A company pass means the report is mechanically
complete under the conditional company planning contract. Neither pass means:

- evidence is true;
- evidence was retrieved;
- demand exists;
- the board is exhaustive;
- graph construction is complete;
- acquisition is complete or the participant packet is frozen;
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
    Commission Signal Board operation now routes two conditional profiles while
    preserving mode backtest|forward. Agents default one-company Brand/Org work
    to company_competitive_intelligence, default time posture to recency_first,
    use longitudinal only with period and rationale, and validate only a complete
    profile-specific output. Company reports have no classifier handoff.
  trigger: workflow_authority
  related_triggers:
    - validation_philosophy
  controlling_sources_updated:
    - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
    - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
    - forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md
    - .agents/hooks/check_commission_signal_board_output.py
    - forseti-harness/tests/unit/test_commission_signal_board_output_validator.py
    - forseti-harness/tests/fixtures/commission_signal_board_outputs/
    - docs/workflows/forseti_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/hooks/check_commission_signal_board_output.py
    - forseti-harness/tests/fixtures/commission_signal_board_outputs/
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        AGENTS.md already routes Forseti project rules to the overlay and durable
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
        Prompt-orchestration mechanics are unchanged; the canonical prompt
        applies the full contract without forking prompt-policy.
  stale_language_search: >
    rg -n "Commission Signal Board|commission_signal_board|check_commission_signal_board|NEEDS_COMMISSION_INTAKE|validator target|classifier handoff"
    docs .agents forseti-harness -S
    and
    rg -n "run the validator|validator applies|manual/local|NOT hook-wired|intake-only"
    docs .agents forseti-harness -S
    (refresh during implementation validation)
  stale_language_search_result: >
    Executed 2026-07-16. The scoped profile/posture/venue/classifier search
    returned expected live-contract and non-claim hits; the exact forbidden
    posture search returned only quoted receipt literals, not live contract
    usage. Live instructions preserve the standard classifier handoff, omit it
    from company reports, and do not treat validator pass as truth, demand
    classification, proof, graph weight, recency proof, or readiness.
  non_claims:
    - not validation
    - not readiness
    - not CI enforcement
    - not pre-commit enforcement
    - not demand classification
    - not evidence retrieval
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
