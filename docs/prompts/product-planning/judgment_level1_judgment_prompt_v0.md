# Judgment Level 1 Judgment Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (Level 1 product-learning judgment output)
scope: >
  Durable Orca prompt for producing backtesting-first Level 1 forecast,
  utility/action, decision-log, and evaluation-hook output after a commission
  gate brief and evidence artifacts exist.
use_when:
  - Producing a Level 1 backtest judgment output after commission gate, retrieval/extraction, and qualitative evidence weighting are complete.
  - Converting source-backed evidence into coarse forecast records, one bounded action, a decision-log entry, and reveal/evaluation hooks.
  - Preventing Level 1 judgment output from claiming source capture, scoring authorization, readiness, buyer proof, or judgment-quality evidence.
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine/judgment_level1_product_learning_core_minimum_v0.md
  - docs/product/judgment_spine/fragrance_level1_casebook_admission_frame_v0.md
  - docs/product/judgment_spine/judgment_spine_reveal_calibration_owner_contract_v0.md
  - .agents/workflow-overlay/prompt-orchestration.md
input_hashes:
  uploaded_judgment_prompt_draft_sha256: 841760B716F26FEECB3576A6B79DDAC1BD66183284A1583D371B676FBAC3D506
branch_or_commit: codex/judgment-level1-prompt-artifacts at c974e49c1828e1217cd1b1a88eeec036c0c9265e
stale_if:
  - The Level 1 core-minimum doc changes its default mode, forecast/action/log/evaluation contract, outcome labels, or live/client readiness gates.
  - The fragrance casebook admission frame changes its canonical outcome-label families.
  - The JSG-08 reveal/calibration owner contract changes reveal/evaluation satisfaction states or claim caps.
  - Prompt-orchestration rules change output modes, preflight fields, source-gated method sequencing, or durable prompt artifact requirements.
  - A later prompt artifact supersedes this judgment prompt.
```

## Status

This is a durable prompt artifact authored through `workflow-prompt-orchestrator`
mechanics. It promotes the uploaded temporary Level 1 judgment draft into an
Orca-bound prompt surface.

It is not a case intake, not a named-case admission, not raw retrieval, not
source extraction, not evidence weighting, not a decision log sheet, not an
evaluation spreadsheet, not scoring authorization, not validation, not
readiness, not buyer proof, and not judgment-quality evidence.

Default downstream output mode: `chat-only`. A later wrapper may bind
`file-write` for a case-specific judgment output only when it also binds the
destination path, source pack, dirty-state allowance, and validation gates.

## Prompt-Orchestrator Receipt

```yaml
prompt_orchestrator_receipt:
  skill: workflow-prompt-orchestrator
  template_kind: full-prompt
  output_mode: file-write
  template_source: >
    Orca overlay contract plus generic workflow-prompt-orchestrator full-prompt
    and product template guidance; no project-local product/full-prompt template
    was registered for this exact artifact.
  workflow_sequence_policy: overlay_owned
  workflow_sequence_source: accepted_project_artifact
  workflow_sequence_status: bound
  accepted_project_artifacts:
    - docs/product/judgment_spine/judgment_level1_product_learning_core_minimum_v0.md
    - docs/product/judgment_spine/fragrance_level1_casebook_admission_frame_v0.md
  non_claims:
    - not prompt execution
    - not raw retrieval
    - not source capture
    - not scoring authorization
    - not validation
    - not readiness
```

## Authoring Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_judgment_level1_prompt_artifact_pack
  edit_permission: docs-write
  target_scope: >
    Create durable Level 1 commission-gate and judgment prompt artifacts and
    update narrow live route mentions that previously recorded the prompt gap.
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - docs/product/judgment_spine/judgment_level1_product_learning_core_minimum_v0.md
    - docs/product/judgment_spine/fragrance_level1_casebook_admission_frame_v0.md
    - C:/Users/vmon7/AppData/Local/Temp/orca_judgement_prompt_level1.md
```

Preflight defaults:
`docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0` - constants
bound; deltas stated here.

Required deltas:

- authorization_basis: current user instruction to continue the post-PR
  Judgment Level 1 product-learning lane, plus the packet active objective that
  names prompt-orchestrated commission-gate and Level 1 judgment prompt
  artifacts as the next authorized docs-only move.
- objective / intended_decision: bind a durable prompt that turns gated
  evidence into coarse forecast records, one bounded action, a decision-log
  entry, and evaluation hooks without claiming proof or readiness.
- target_files_or_dirs: this prompt artifact; later case-specific users must
  supply the commission gate brief, graph-family artifact, evidence objects,
  weighted evidence stack, and output destination if any.
- source_pack / bounded_reads: AGENTS, overlay README, source-of-truth,
  source-loading, prompt-orchestration, template registry, artifact folders,
  retrieval metadata, validation gates, Judgment consolidation map, Level 1 core
  minimum, current-state/decomposition, fragrance casebook frame, JSG-08 owner
  contract when reveal/evaluation claims matter, and uploaded judgment draft.
- output_mode: file-write for this durable artifact; downstream default
  `chat-only`.
- edit_permission: docs-write for this authoring pass; downstream receiver is
  read-only unless a later wrapper binds write authority.
- dirty_state_allowance: authoring worktree was clean before edits; downstream
  receiver must report dirty state if repo sources are read.
- controlling_source_state: clean at authoring preflight before these edits.
- branch_or_commit_reference: `codex/judgment-level1-prompt-artifacts` at
  `c974e49c1828e1217cd1b1a88eeec036c0c9265e`.
- doctrine_change_decision: no intended doctrine change; if a receiver needs to
  change product doctrine, prompt policy, claim tiers, gate ownership, source
  authority, or lifecycle boundaries, stop and route through the owning source.
- isolation_decision: fresh dependent worktree/branch from PR #230 head because
  current `main` did not yet contain the Judgment Level 1 stack at authoring.
- validation_gates: retrieval-header check, repo-map freshness check,
  placement changed-file check, header index, and diff whitespace check.
- thread_operating_target_continuity: no structured `goal_handoff` or active
  `thread_operating_target` was supplied; this prompt carries the active
  objective in plain prose only.

## Downstream Receiver Contract

Use this prompt only after these inputs exist:

- a case intake or named-case admission artifact;
- a commission-gate brief;
- graph-family artifact or equivalent bounded evidence plan output;
- evidence objects with source/date/provenance boundaries;
- qualitative evidence weighting stack;
- buyer constraints or utility template;
- explicit cutoff and future-information policy.

If any required input is missing, return `BLOCKED_LEVEL1_JUDGMENT_INPUT_MISSING`
with the missing fields. Do not invent source evidence and do not do raw
retrieval.

Before applying the prompt:

1. Read `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md`.
3. Read `.agents/workflow-overlay/source-of-truth.md`.
4. Read `.agents/workflow-overlay/source-loading.md`.
5. Read `.agents/workflow-overlay/prompt-orchestration.md`.
6. Read `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md`.
7. Read `docs/product/judgment_spine/judgment_level1_product_learning_core_minimum_v0.md`.
8. Read `docs/product/judgment_spine/fragrance_level1_casebook_admission_frame_v0.md` for canonical outcome-label families when the case is fragrance.
9. Read `docs/product/judgment_spine/judgment_spine_reveal_calibration_owner_contract_v0.md` before any reveal/evaluation satisfaction or calibration claim.
10. Read the case-specific intake/admission, commission-gate brief, evidence artifacts, and evidence-weighting record supplied for the case.

Declare `SOURCE_CONTEXT_READY` before producing judgment output. If any required
source is missing, declare `SOURCE_CONTEXT_INCOMPLETE` and return the smallest
specific blocker.

## Prompt

You are the Orca Level 1 judgment harness.

Given the commission gate brief, graph-family artifact, evidence objects,
weighted evidence stack, and utility constraints, produce forecasts, choose one
bounded action, log the decision, and prepare the case for later evaluation.

Default mode is `backtest`. `live_internal` and `client_facing` are later-gated
modes. If either is requested without explicit current source authority, return
`BLOCKED_MODE_NOT_AUTHORIZED`.

## Mode Contract

Every run must include:

```json
{
  "mode": "backtest",
  "case_id": "...",
  "evidence_cutoff_at": "YYYY-MM-DD",
  "future_information_policy": "exclude all information after cutoff"
}
```

If `mode = backtest`, judge only from evidence available at the cutoff date. Do
not use later outcomes to adjust forecasts or action.

## Required Inputs

```json
{
  "commission_gate_brief": {},
  "graph_family_artifact": {},
  "evidence_objects": [],
  "weighted_evidence_stack": {},
  "buyer_constraints": {},
  "utility_template": {},
  "forecast_history_or_calibration": null,
  "evidence_cutoff_at": "YYYY-MM-DD"
}
```

If a required input is missing, state how that limits confidence and stop when
the missing input is load-bearing.

## Output Contract

Return:

```json
{
  "source_context_status": "SOURCE_CONTEXT_READY / SOURCE_CONTEXT_INCOMPLETE",
  "case_id": "...",
  "mode": "backtest",
  "forecast_records": [],
  "utility_assessment": {},
  "action_recommendation": {},
  "decision_log_entry": {},
  "evaluation_hooks": {},
  "visible_limitations": []
}
```

## Forecasting

Do not forecast every target mechanically. Forecast targets that would
materially change the action. Keep the core targets where applicable for
comparability.

Canonical outcome labels:

| Target | Outcome = true when |
| --- | --- |
| `review_velocity_sustained_60d` | Review count increases by the greater of 5 relevant reviews or 20% of cutoff review count within the window, excluding obvious launch-dump, duplicated, old-SKU, or wrong-SKU reviews. Use a peer baseline when pre-cutoff reviews are very low. |
| `creator_momentum_persisted_30d` | Post-cutoff mentions continue for 30 days with evidence of non-duplicated creators or cross-segment spread. |
| `creator_decay_after_launch_30d` | Days 31-60 show less than 25% of independent creator activity from days 0-30 and no new non-creator confirmation emerges. |
| `community_confirmation_30d` | At least 3 independent community/review items after cutoff include usage or purchase-proxy language, not just awareness. |
| `restock_or_sellout_repeats_60d` | At least one post-cutoff public restock/sellout/out-of-stock event is observed and tied to the correct SKU or format. |
| `discounting_or_overstock_appears_90d` | Target SKU/product receives a 20%+ discount or repeated SKU-specific promotion not explained by ordinary sitewide sale. |
| `complaint_cluster_grows_60d` | At least 3 independent post-cutoff complaints share the same issue and appear in more than one source family or review cluster. |
| `retail_expansion_or_sku_followthrough_180d` | New retailer, format, SKU, restock expansion, discovery set, travel size, or adjacent product follow-through appears within the horizon. |
| `search_interest_persisted_60d` | Autocomplete, trend tool, search result ranking, marketplace search, or AEO answer visibility persists across at least two checks after cutoff. |

Migration aliases from earlier drafts may be accepted as input only. Emit the
canonical label in the output:

| Alias | Emit |
| --- | --- |
| `restock_or_sellout_60d` | `restock_or_sellout_repeats_60d` |
| `discounting_or_overstock_90d` | `discounting_or_overstock_appears_90d` |
| `complaint_cluster_growth_60d` | `complaint_cluster_grows_60d` |
| `search_persistence_60d` | `search_interest_persisted_60d` |
| `creator_decay_30d` | `creator_decay_after_launch_30d` |

Use coarse probabilities. Avoid fake precision. Allowed probability buckets:

```text
50-60
60-70
70-80
80-90
```

Use raw probabilities now. Add calibrated probabilities only when the matching
target/horizon has enough completed backtests and an owning source authorizes
the calibration claim.

Forecast record schema:

```json
{
  "forecast_id": "...",
  "case_id": "...",
  "target": "...",
  "horizon_days": 60,
  "evidence_cutoff_at": "YYYY-MM-DD",
  "included_evidence_ids": [],
  "excluded_future_evidence_policy": "exclude all source dates after cutoff",
  "raw_probability": 0.65,
  "calibrated_probability": null,
  "probability_bucket": "60-70",
  "main_evidence_drivers": [],
  "main_uncertainty": "...",
  "outcome_due_at": "YYYY-MM-DD",
  "outcome_label": null,
  "brier_score": null
}
```

## Utility

Use coarse public proxy utility for backtesting only. This is not ROI,
calibration, or scoring authorization.

| Buyer type | Upside weighted most | Downside weighted most | Default action bias |
| --- | --- | --- | --- |
| operator | capturing demand, cash efficiency, brand fit | overstock, cash drag, brand dilution | controlled test unless costly behavior is strong |
| retailer | sell-through, relevance, category leadership | dead inventory, returns, shelf opportunity cost | add/test/deepen based on confirmation |
| investor | durability, channel quality, repeat proxy | hype, margin risk, weak retention proxy | diligence deeper unless durability is strong |
| platform | scalable category signal, acquisition/incubation fit | false positives, execution distraction | option-building and evidence collection |
| strategy | timing, category direction, option value | acting too early, acting on noise | bounded wait or controlled test |

Proxy points may be used for internal comparison only:

| Outcome | Proxy points |
| --- | ---: |
| Review velocity sustains | +20 |
| Restock or sellout repeats | +20 |
| Retail expansion / SKU follow-through | +20 |
| Community confirmation | +15 |
| Search interest persists | +10 |
| Discounting / overstock appears | -20 |
| Complaint cluster grows | -15 |
| Creator momentum collapses | -15 |
| One-origin hype confirmed | -15 |

Adjust points qualitatively by buyer type. Do not claim precise ROI.

Utility assessment output:

```json
{
  "buyer_type": "...",
  "utility_template": "...",
  "key_upside_outcomes": [],
  "key_downside_outcomes": [],
  "risk_constraints": [],
  "public_proxy_utility_notes": [],
  "expected_value_summary": "coarse, not precise",
  "highest_regret_failure_mode": "..."
}
```

## Action Recommendation

Use exactly one primary action family:

```text
commit_or_deepen
controlled_test
bounded_wait_with_trigger
avoid_kill_or_discount
reposition_or_change_offer
collect_specific_evidence
```

Never output passive monitor.

Bad:

```text
Monitor the trend.
```

Required:

```text
bounded wait + evidence target + timebox + go trigger + stop condition + next action
```

Action object:

```json
{
  "action_family": "controlled_test",
  "specific_action": "...",
  "magnitude": "range or bucket",
  "timing": "start date / decision window",
  "duration": "days/weeks",
  "do_not_do": "...",
  "evidence_target": "...",
  "go_trigger": "...",
  "stop_condition": "...",
  "next_action_if_trigger_hits": "...",
  "main_crux": "...",
  "confidence_bucket": "low / medium / high",
  "utility_rationale": "...",
  "visible_limitations": []
}
```

`collect_specific_evidence` is valid only when framed as value-of-information:
the missing evidence, source family, timebox, action unlocked, and stop
condition must all be named.

## Decision Log

Every recommendation must produce a decision log entry:

```json
{
  "case_id": "...",
  "mode": "backtest",
  "evidence_cutoff_at": "YYYY-MM-DD",
  "intake_version": "...",
  "gate_version": "...",
  "evidence_version": "...",
  "weighted_evidence_stack_id": "...",
  "forecast_ids": [],
  "utility_template": "...",
  "action_recommendation": {},
  "main_crux": "...",
  "what_would_change_the_call": [],
  "visible_limitations": [],
  "outcome_due_dates": [],
  "future_information_policy": "exclude all after cutoff"
}
```

This output is a decision-log entry candidate. It is not a durable decision log
sheet unless a later wrapper binds a file destination and write authority.

## Evaluation Hooks

Include fields that later evaluation can score after reveal. Do not reveal,
score, calibrate, or claim learning completion inside this prompt.

```json
{
  "evaluation_hooks": {
    "benchmark_policies_to_compare": [
      "creator_only",
      "retail_only",
      "conservative_controlled_test",
      "aggressive_commit",
      "always_wait",
      "raw_LLM_without_harness",
      "human_manual_if_available",
      "orca_structured_policy"
    ],
    "forecast_targets_to_score": [],
    "utility_outcomes_to_label": [],
    "likely_error_modes_to_watch": [],
    "disagreement_case_tag": true,
    "outcome_label_due_dates": []
  }
}
```

Use these error labels after outcome reveal only:

```text
data_miss
extraction_error
weighting_error
forecasting_error
utility_error
judgment_error
uncertainty_error
provenance_error
future_information_leak
```

For each completed case, later evaluation may compare Brier score for each
forecast, realized public proxy utility, regret versus best benchmark action,
benchmark comparison, primary error label, missing crux, and schema/rubric
updates. This prompt only creates hooks for that later step.

## Backtesting Procedure

The intended sequence is:

```text
1. Freeze historical case and cutoff date.
2. Run commission gate without future evidence.
3. Retrieve/extract evidence available before cutoff.
4. Weight evidence.
5. Run this judgment prompt.
6. Freeze decision log.
7. Reveal outcome window.
8. Label outcomes.
9. Score forecasts and action.
10. Update notes/rubrics only after scoring.
```

This prompt covers step 5 only and produces step-6-ready output. It does not
authorize steps 2-4, 6-10, or any case run by itself.

## Named Limitations

Always name limitations relevant to the case:

```text
No causal attribution.
No private sell-through unless provided.
No validated calibration until enough backtests exist.
No automated policy learning.
No client-facing authority in backtest mode.
Potential public-signal incompleteness.
Possible source-date/provenance gaps.
```

## Blockers

Return a blocker instead of partial judgment output when:

- the required input stack is missing;
- the case has no `mode`, `case_id`, `evidence_cutoff_at`, or
  `future_information_policy`;
- a requested `live_internal` or `client_facing` mode lacks explicit current
  authorization;
- source context is incomplete for the claim being made;
- producing output would require raw retrieval, private data, live capture,
  source-capture authority, run authorization, scoring, or post-cutoff evidence;
- the only possible action would be passive monitoring.

## Non-Claims

This prompt and any output from it are not validation, readiness, buyer proof,
product proof, source-capture authority, captured evidence, run authorization,
scoring authorization, fixture admission, prompt approval, completed
product-learning evidence, `live_internal` readiness, `client_facing`
readiness, calibration evidence, or judgment-quality evidence.
