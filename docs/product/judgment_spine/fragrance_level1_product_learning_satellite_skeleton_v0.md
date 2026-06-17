# Fragrance Level 1 Product-Learning Satellite Skeleton v0

```yaml
retrieval_header_version: 1
artifact_role: Judgment Spine product artifact (fragrance Level 1 product-learning satellite skeleton)
scope: >
  Defines the slot skeleton for a fragrance-specific Level 1 Judgment satellite
  that imports core Judgment boundaries by pointer and reserves, but does not
  complete, the casebook, source, evidence, weighting, forecast, decision,
  utility/action, decision-log, reveal/evaluation, lesson, and receipt surfaces.
use_when:
  - Authoring or reviewing the first fragrance Level 1 product-learning pack.
  - Deciding where fragrance casebook, source, weighting, forecast, decision, reveal, and lesson fields belong.
  - Checking whether fragrance work consumes the Level 1 core-minimum backtest contract before filling domain detail.
  - Checking the non-claims before any fragrance prompt, source-capture, run, scoring, or proof work.
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine/judgment_current_state_and_decomposition_v0.md
  - docs/product/judgment_spine/judgment_level1_product_learning_core_minimum_v0.md
  - docs/product/judgment_spine/fragrance_level1_product_learning_reconciliation_v0.md
  - docs/product/judgment_spine/fragrance_level1_casebook_admission_frame_v0.md
  - docs/product/judgment_spine/fragrance_level1_named_case_candidate_screen_v0.md
  - docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md
  - docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md
  - docs/product/judgment_spine/judgment_spine_demand_read_machinery_architecture_v0.md
  - docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md
  - docs/product/judgment_spine/judgment_spine_c3_verdict_action_ceiling_contract_v0.md
  - docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md
  - docs/product/judgment_spine/near_half_backtest_learning_architecture_v0.md
  - docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md
  - docs/product/core_spine/beauty_venue_card_set_v0.md
stale_if:
  - The evidence ladder changes claim tiers, closeout states, receipt minima, or promotion gates.
  - The conductor changes its no-authority invariant, by-hand cap, JSG routing, or run-authorization boundary.
  - The Level 1 product-learning core minimum changes its default mode, SCV loop, 25-case success condition, source registry, outcome labels, commission gate, forecast/action/log/evaluation contract, or live/client readiness gates.
  - The demand-read core, C2, C3, near-half, far-half, or signal-ledger surfaces are accepted, rejected, or materially amended.
  - The fragrance casebook admission frame accepts, rejects, or materially changes the first Level 1 case slots or named cases.
  - An owning source-capture artifact admits fragrance venue/source families or authorizes capture.
  - A completed fragrance product_learning_receipt exists.
  - The beauty venue card set changes its access-route observations for Basenotes, Fragrantica, or the specialist fragrance blog cluster.
```

## Status

This is a docs-only skeleton for the first fragrance satellite. It is useful
because it names the slots a real fragrance pack must fill without forcing those
slots to be filled now.

Claim cap: product-learning context only. The current closeout state for this
artifact's own claim is `unreceipted_product_learning_context`: durable context
and a skeleton exist, but there is no admitted casebook, no source-capture
authority, no completed evidence packet, no run, no scoring receipt, no
product-learning receipt, no buyer-proof receipt, and no judgment-quality
receipt.

## Operating Rule

Core owns the judgment machinery. Fragrance owns the domain instances.

This skeleton must import core Judgment boundaries by pointer instead of
restating or replacing them:

- The Level 1 core minimum owns the default `mode: backtest`, frozen evidence
  cutoff, future-information exclusion, commission intake/gate, source registry,
  outcome-label, graph/evidence, forecast, utility/action, decision-log,
  reveal/evaluation, benchmark, and readiness-gate contracts.
- Claim tiers, closeout states, receipt minima, and promotion gates come from the
  evidence ladder.
- JSG routing, no-authority discipline, run authorization, and the by-hand cap
  come from the conductor.
- C0-C4 demand-read shape comes from the demand-read core.
- Qualitative weighting comes from C2; no numeric weight, score, formula, or
  deterministic apply-rule belongs here.
- Verdict and action ceiling come from C3; fragrance may map examples onto
  `act`, `phase`, `narrow`, `hold`, or `defend`, but it must not mint new action
  vocabulary.
- Forecast, utility/action, decision-log, reveal/evaluation, and lesson fields
  are product-learning inputs unless later owner gates promote them.

## Current Claim Classification

```yaml
evaluated_surface: fragrance_level1_product_learning_satellite_skeleton_v0
source_quality_state: >
  repo-local skeleton reconciled to current Judgment owner sources and the
  fragrance reconciliation artifact
execution_quality_state: >
  no admitted fragrance casebook, no captured source packet, no sealed answer,
  no run, no scoring, no reveal comparison, no completed receipt
closeout_state: unreceipted_product_learning_context
claim_cap: product-learning context only
weakest_missing_or_failed_gate:
  - no admitted fragrance Level 1 casebook
  - no durable commission-gate or Level 1 judgment prompt artifact
  - no source registry, outcome-label sheet, forecast record, decision log, or evaluation sheet
  - no source-capture authority or captured evidence packet
  - no sealed pre-reveal answer or run
  - no product_learning_receipt
  - no buyer_proof_receipt
  - no judgment_quality_receipt
receipt_artifact_or_gap: this skeleton is setup context; future per-case receipts remain required
```

## Skeleton Slots

| Slot | Fragrance satellite field | Core owner or pointer | Completion prerequisite | Do not claim |
| --- | --- | --- | --- | --- |
| Satellite identity | `decision_family`, Level 1 purpose, target product-learning question | Current-state/decomposition map; C0 frame | Owner accepts the first pack's purpose and case family | Judgment doctrine, proof, or readiness |
| Backtest mode and commission gate | `mode`, cutoff, future-information policy, decision type, playbook, source priorities, confirmation/counterevidence, forecast targets | Level 1 core minimum; future prompt-orchestrated gate artifact | Durable gate brief and case intake artifact | Live/client mode, final recommendation, prompt approval, or run authorization |
| Casebook queue | Candidate cases, cutoff dates, outcome labels, exclusion reasons | Level 1 core minimum; C0 frame, case-finder gap, conductor run authorization boundary | Separate casebook admission artifact | Accepted benchmark, fixture, run authorization, readiness, or scoreable case |
| Source-family registry | Candidate fragrance venues, source-family notes, provenance requirements, cutoff/date/SKU limits | Beauty venue card-set; source-capture owners by pointer; Level 1 source-registry contract | Owning source-capture artifact admits or authorizes source work | Capture authority, monitoring, or current-state source proof |
| Evidence object | Source references, provenance notes, contradiction/timeline links, pre/post-cutoff separation, packet IDs | JSG-01, ECR, packing/finalization owners; Level 1 graph-family plan | Captured evidence packet and authorized packet construction | JSG clearance or gate-bearing execution |
| C1 allow read | Why the demand signal is allowed into the read, or why it is held | Demand-read core C1 | Case-specific source plan and allowed-evidence rationale | Source truth or source-family admission |
| C2 weighting trace | `signal_id`, direction, reasoning, caveats, no-row handling | C2 ledger read contract; signal-reliability ledger | Qualitative read over in-case evidence plus any valid ledger row | Numeric weight, formula, ranking, or score |
| Forecast records | Target, horizon, cutoff, evidence refs, probability bucket, due date, outcome label, Brier hook | Level 1 forecast-record contract; far-half decision object; near-half eval surfaces | Pre-reveal seal before outcome lookup | Judgment-quality evidence, calibration, or buyer proof |
| C3 utility/action | Bounded action family, magnitude, timing, trigger, stop condition, next action, crux, confidence bucket | Level 1 utility/action schema; C3 verdict/action ceiling contract | C2 trace and fixed action vocabulary | Passive monitor, new action vocabulary, or unconstrained live action |
| Decision log | Evidence version, forecasts, utility assumptions, action object, limitations, due dates | Level 1 decision-log contract; evidence ladder receipt boundary | Sealed log before reveal | Completed product-learning evidence by itself |
| Reveal/eval | Outcome record, outcome labels, benchmark comparison, regret/error labels, Brier-style note if used | JSG-08 owner contract; near-half learning shell; Level 1 evaluation record | Sealed pre-reveal call plus outcome record | JSG-08 clearance, calibration, readiness, or proof by outcome |
| Lesson/signal rows | Candidate lesson, signal row candidate, discriminator tell | Near-half lesson architecture; signal-reliability ledger | Promotion gate and report-all K-of-N discipline | Validated lesson, source-family promotion, or causation |
| Product-learning receipt | Case/packet ID, surface, prompt or answer handle, owner readback, friction/product signals, non-claims | Evidence ladder `product_learning_receipt` | All minimum receipt fields complete | Buyer proof, judgment quality, run readiness, or scoring authorization |

## Per-Case Record Shape

Use this as a slot checklist, not as a completed schema. Empty or unknown fields
must stay empty or `unknown`; do not backfill with guesses. Any field that looks
like an achieved state must carry the artifact or receipt pointer that makes it
true; without that pointer, keep the field at the weaker candidate, incomplete,
or unknown state.

```yaml
fragrance_level1_case:
  case_id:
  case_status: candidate | admitted | excluded
  case_admission_artifact_ref:
  mode_contract:
    mode: backtest
    evidence_cutoff_at:
    future_information_policy: exclude_all_information_after_cutoff
  decision_family: fragrance_level1
  decision_frame:
    product_learning_question:
    cutoff_datetime_utc:
    outcome_label_plan:
    exclusion_reason_if_any:
  commission_gate:
    gate_brief_ref:
    decision_type:
    playbook:
    source_priorities: []
    creator_slices: []
    mandatory_confirmation_or_counterevidence: []
    forecast_targets: []
    redirect_or_stop_rules: []
  source_registry:
    registry_ref:
    provenance_rules_ref:
    source_mix_policy:
  source_plan:
    candidate_venues:
      - venue_name:
        source_family:
        basis:
        access_note:
        capture_authority: not_authorized | authorized_by_pointer
        authority_pointer:
    prohibited_or_held_sources:
      - source_or_family:
        reason:
  evidence_packet:
    packet_id:
    packet_construction_authority_ref:
    evidence_object_refs: []
    provenance_notes:
    post_cutoff_exclusion_notes:
  c1_allow:
    allow_state: allowed | held | excluded | unknown
    allow_artifact_or_rationale_ref:
    rationale:
  c2_weighting:
    decision_family_query:
    signals:
      - signal_id:
        direction: supports | opposes | hedges | unknown
        qualitative_read:
        direction_reasoning:
        caveats:
        n_scoreable:
        small_n_or_staleness_caveat:
        ledger_row_ref:
        no_row_handling:
        ambiguity_or_absence_classification:
    reasoning_trace:
  forecast_records:
    - target:
      horizon:
      cutoff_datetime_utc:
      included_evidence_refs: []
      raw_probability_bucket:
      due_date:
      outcome_label:
      brier_hook:
      sealed_before_reveal: yes | no | unknown
      seal_artifact_or_process_ref:
  utility_action:
    action_family: act | phase | narrow | hold | defend | unknown
    magnitude:
    timing:
    trigger:
    stop_condition:
    next_action:
    crux:
    confidence_bucket:
    limitations:
  decision_log:
    decision_log_ref:
    evidence_version:
    forecasts_ref:
    utility_assumptions:
    action_ref:
    limitations:
    outcome_due_dates: []
  c3_decision:
    demand_state: durable | transient | unknown
    persistence_basis:
    action_ceiling: act | phase | narrow | hold | defend | unknown
    horizon: commit | move | unknown
    confidence_band:
    confidence_band_basis:
    recommendation:
    signals_used: []
    cap_reasons:
    reasoning_trace:
  reveal_eval:
    outcome_record_ref:
    outcome_labels_observed: []
    benchmark_comparison:
    regret_label:
    error_label:
    reveal_comparison:
    brier_or_forecast_note:
    product_learning_signal:
  lesson_capture:
    candidate_lessons: []
    candidate_signal_rows: []
    promotion_status: not_attempted | candidate | promotion_validated_by_artifact
    promotion_artifact_ref:
    promoted_signal_row_refs: []
  product_learning_receipt:
    receipt_status: incomplete | complete_by_artifact
    receipt_artifact_ref:
    raw_answer_location:
    owner_readback:
    product_or_friction_signals:
    non_claims:
      - not buyer proof
      - not judgment-quality evidence
      - not run authorization
      - not scoring authorization
```

### Per-Case Guardrails

- `admitted`, `excluded`, `authorized_by_pointer`,
  `promotion_validated_by_artifact`, and `complete_by_artifact` are not
  self-certifying values; each requires the adjacent artifact or receipt pointer.
- `capture_authority: authorized_by_pointer` must point to an owning
  source-capture artifact that is external to this skeleton; a pointer to this
  skeleton, the reconciliation artifact, or any other non-authorizing source
  does not satisfy the authorization requirement.
- `sealed_before_reveal: yes` is an achieved-state value under the general
  guardrail above; use `unknown` unless the sealing method or process record
  can be named in `seal_artifact_or_process_ref`.
- `mode_contract.mode` defaults to `backtest`; any `live_internal` or
  `client_facing` value requires a later owner-gated readiness decision, not
  this skeleton.
- `raw_probability_bucket` and forecast confidence fields are
  forecast/evaluation fields. They are not the C3 sealed-call
  `confidence_band`.
- C2 trace fields must make caveats travel: direction reasoning, N/small-N or
  staleness, ledger row or no-row handling, and absence/ambiguity
  classification.
- C3 trace fields must preserve the transient-default and action-ceiling logic:
  persistence basis, C3 `confidence_band`, tagged `signals_used`, and cap
  reasons.
- `utility_action` must not be a passive "monitor" answer. A hold/defend/narrow
  action still needs a target, trigger, stop condition, timebox or due date, and
  next action.
- The `product_learning_receipt` sub-object is a pointer/status slot, not a
  full receipt. A `complete_by_artifact` status requires the referenced artifact
  to satisfy all minimum receipt fields owned by the evidence ladder; the
  inline sub-object fields are supplements, not substitutes for the evidence
  ladder's minimum receipt field set.

## Source-Family Starting Hints

The beauty venue card-set is the starting pointer for fragrance venue hints. It
does not authorize capture or monitoring.

A later fragrance source registry or source/evidence plan must preserve source
family, source date, access date, SKU/format limits where relevant, and cutoff
eligibility. Venue hints are not enough.

Initial candidate hints:

- Basenotes: fragrance subtle-class tracker; direct HTTP was observed as 403 in
  the card-set, with search snippets as a possible screening route.
- Fragrantica: tracker/aggregator; direct HTTP was observed as 403 in the
  card-set, with snippets only.
- Specialist fragrance blog cluster: outcome gauge; direct fetch was observed
  as workable in the card-set.

These are candidate fields for a future source/evidence slice. They are not
current evidence, not source-family admission, and not permission to run source
capture.

Creator evidence is early radar, not proof. A creator-led case cannot reach a
stronger action posture without non-creator confirmation.

## Forecasting Boundary

Forecasting is a learning input, not the center of the Judgment claim. A
forecast field may help compare sealed expectation to later outcome, but the
evidence ladder frames Judgment as the best move under the evidence available at
the decision point.

For this satellite:

- Forecasts must be sealed before reveal if they will be evaluated.
- Forecast records should name target, horizon, cutoff, included evidence refs,
  raw probability bucket, due date, outcome label, and Brier hook.
- Outcome comparison may produce product-learning notes.
- A correct outcome call does not prove the judgment was good.
- A wrong outcome call does not automatically prove the judgment was bad.
- Calibration, buyer proof, and judgment-quality claims require their own gates.

## Casebook Admission Boundary

This skeleton does not admit the first cases. Before any case is treated as more
than a candidate, a later artifact should record at least:

- `mode: backtest` unless a later owner explicitly authorizes another mode;
- the case ID and decision family;
- cutoff date/time and post-cutoff exclusion rule;
- source families allowed for the pre-cutoff packet;
- outcome label and measurement window;
- commission-gate and source-registry references where available;
- forecast targets and benchmark policy that may disagree;
- exclusion criteria;
- explicit non-claims.

## Prompt Boundary

This artifact is not a prompt, wrapper, handoff, rerun prompt, or patch prompt.
If any fragrance prompt is needed, author it through `workflow-prompt-orchestrator`.

## Next Docs-Only Moves

1. Author durable commission-gate and Level 1 judgment prompt artifacts through
   `workflow-prompt-orchestrator` if prompt artifacts are needed.
2. Create the backtest case intake, source registry, outcome-label, forecast
   record, utility/action, decision-log, benchmark, and evaluation artifacts the
   core minimum names.
3. Use the named-case candidate screen to choose the first case admission
   attempt, then fill the admission-minimum fields in the casebook lane.
4. Author a fragrance source/evidence plan that consumes the beauty venue
   card-set by pointer and routes capture authority to the source-capture owners.
5. Create a first per-case product-learning receipt template or example only
   after the casebook and evidence slots are bounded.

## Non-Claims

This artifact is not validation, readiness, buyer proof, product proof,
judgment-quality evidence, prompt approval, run authorization, scoring
authorization, source-capture authority, conductor amendment, C2/C3 adoption,
casebook admission, source-family admission, prompt artifact, `live_internal`
readiness, `client_facing` readiness, owner adoption of any named fragrance
case, or wholesale temp-pack adoption.

It does not assert that the fragrance Level 1 plan works. It only gives the
first fragrance satellite a repo-local shape that future docs can fill without
claim inflation.

## Source-Read Ledger

Overlay and routing sources:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/validation-gates.md`

Judgment and fragrance sources:

- `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md`
- `docs/research/judgment-spine/judgment_spine_machinery_build_state_gap_map_v0.md`
- `docs/product/judgment_spine/judgment_current_state_and_decomposition_v0.md`
- `docs/product/judgment_spine/judgment_level1_product_learning_core_minimum_v0.md`
- `docs/product/judgment_spine/fragrance_level1_product_learning_reconciliation_v0.md`
- `docs/product/judgment_spine/fragrance_level1_named_case_candidate_screen_v0.md`
- `docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md`
- `docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md`
- `docs/product/judgment_spine/judgment_spine_demand_read_machinery_architecture_v0.md`
- `docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md`
- `docs/product/judgment_spine/judgment_spine_c3_verdict_action_ceiling_contract_v0.md`
- `docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md`
- `docs/product/judgment_spine/near_half_backtest_learning_architecture_v0.md`
- `docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md`
- `docs/product/core_spine/beauty_venue_card_set_v0.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_mgt_goal_v1.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_judgement_mgt.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_build_action_doc.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_commission_gate_prompt.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_judgement_prompt_level1.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_open_questions_working_doc.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_docs_split_manifest.md`
