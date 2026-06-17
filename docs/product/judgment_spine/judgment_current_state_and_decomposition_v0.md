# Judgment Current State And Decomposition v0

```yaml
retrieval_header_version: 1
artifact_role: Judgment Spine current-state and decomposition map
scope: >
  Source-backed product-learning frame for where Orca Judgment stands now and
  how the next work should split into core Judgment portions and a fragrance
  Level 1 satellite without promoting the lane into proof, scoring, readiness,
  or judgment-quality evidence.
use_when:
  - Orienting after the fragrance Level 1 product-learning reconciliation.
  - Deciding where forecasting, weighting, decision, reveal, and lesson work belong.
  - Separating market-agnostic Judgment core work from fragrance-specific satellite work.
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md
  - docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md
  - docs/research/judgment-spine/judgment_spine_machinery_build_state_gap_map_v0.md
  - docs/product/judgment_spine/judgment_spine_demand_read_machinery_architecture_v0.md
  - docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md
  - docs/product/judgment_spine/judgment_spine_c3_verdict_action_ceiling_contract_v0.md
  - docs/product/judgment_spine/fragrance_level1_product_learning_reconciliation_v0.md
  - docs/product/judgment_spine/fragrance_level1_product_learning_satellite_skeleton_v0.md
  - docs/product/judgment_spine/fragrance_level1_casebook_admission_frame_v0.md
  - docs/product/judgment_spine/fragrance_level1_named_case_candidate_screen_v0.md
  - docs/product/judgment_spine/judgment_level1_product_learning_core_minimum_v0.md
stale_if:
  - The evidence ladder changes claim tiers, closeout states, receipt minima, or promotion gates.
  - The conductor changes its no-authority invariant, by-hand cap, or JSG routing.
  - The build-state gap map changes blind-execution, real-run, JSG-01 binding, or case-finder status.
  - The demand-read core, C2, C3, near-half, far-half, or signal-ledger surfaces are accepted, rejected, or materially amended.
  - The fragrance Level 1 satellite skeleton is materially amended, retired, or superseded.
  - The fragrance Level 1 casebook admission frame is materially amended, retired, or superseded.
```

## Status

This is a docs-only decomposition aid. It does not change Judgment Spine
doctrine, adopt the fragrance pack, authorize prompts, authorize a run, authorize
scoring, or update any runtime.

Claim cap: product-learning context only. The current closeout state for this
artifact's own claim is `unreceipted_product_learning_context`: durable context
exists, but no case run, product-learning receipt, buyer-proof receipt, or
judgment-quality receipt exists for the fragrance Level 1 lane.

## Operating Frame

The next Judgment work should use a core-plus-satellite shape:

- **Core:** market-agnostic Judgment surfaces that future verticals can reuse.
- **Satellite:** fragrance-specific source families, casebook choices,
  discriminator tells, utility/action examples, and evidence instances.

For Level 1, the core-plus-satellite shape is now **backtesting-first** by
default. The reusable core must carry the mode contract, commission intake/gate,
source registry governance, outcome labels, graph/evidence shape, qualitative
weighting, forecasts, utility/action object, decision log, reveal/evaluation,
benchmark comparison, and readiness gates. The fragrance satellite fills the
domain instances for a tight public fragrance wedge.

This is the right shape because it keeps Judgment scalable without baking
fragrance assumptions into the core. It also keeps the current move reversible:
fragrance can be the first satellite example while the core remains
market-agnostic.

## Current State

| Surface | Current state | What it owns | Claim cap now |
| --- | --- | --- | --- |
| Evidence ladder | Controlling product artifact | Claim tiers, closeout states, receipt minima, weakest-cleared-gate and promotion rules | Lower-tier work cannot support stronger claims without explicit gates |
| Conductor | Working operating model; path toward judgment-quality evidence, not proof | JSG-01 through JSG-10 sequencing, mechanical predicate reads, lifecycle states, by-hand cap | By-hand JSG-04/05/06 caps no stronger than product-learning |
| Machinery build-state map | Verified built-vs-gap inventory | What is built vs missing across harness/scoring/probe/ECR/finalizer/binding/run/case-finder | Product-learning; authorizes no run |
| JSG-01 binding | Built and unfrozen/evaluable over a bound case packet | EvidenceUnit binding plus receipt-consuming path | Clears no case until a separately authorized run evaluates one |
| Blind contestant execution | Gap | Live blind-judgment execution under proven isolation | Missing runner keeps JSG-04/05/06 by-hand/product-learning |
| Authorized real run | None | Actual non-synthetic case execution | No judgment-quality or buyer-proof claim |
| Case-finder | Gap | Post-cutoff/prospective case sourcing | Fragrance casebook remains proposed until admitted |
| Demand-read core C0-C4 | Product-learning design/input surface | Frame, allow, qualitative weight, verdict/action ceiling, counterfactual | Design input/product-learning; no scoring engine, no conductor edit |
| C2 ledger read contract | Proposed consumer-side contract | Qualitative ledger read, caveat travel, direction plus reasoning, no numeric weight | Product-learning; no row/query/build |
| C3 verdict/action ceiling contract | Proposed binding-side contract | Two-axis demand-state verdict and action ceiling vocabulary | Product-learning; no numeric ceiling or live loop |
| Near-half backtest shell | Proposed target architecture | Adversarial postmortem, validated-lesson cell, promotion gate, ledger emission | Product-learning; validates no lesson yet |
| Signal-reliability ledger | Proposed schema and discipline | K-of-N report-all signal reliability record, product-learning cap, staleness/provenance | No real rows or source-family admission |
| Far-half live decision shell | Proposed target architecture | Decision object, shadow/assisted modes, seal-before-disclose, decision memory | Product-learning; no live runtime |
| Fragrance Level 1 reconciliation | Durable product-learning context | Maps the temp fragrance draft onto current Judgment/demand-read surfaces | Unreceipted product-learning context |
| Fragrance Level 1 satellite skeleton | Repo-local product-learning skeleton | Reserves fragrance casebook/source/evidence/weighting/forecast/decision/reveal/lesson/receipt slots | No admitted cases, source authority, run, score, or proof |
| Fragrance Level 1 casebook admission frame | Repo-local product-learning casebook organizer | Admits the 25-slot casebook shape, bucket allocation, selection rules, and outcome-label families | No named cases admitted, no source authority, run, score, or proof |
| Fragrance Level 1 named-case candidate screen | Repo-local product-learning candidate screen | Ranks first admission attempts against the case-selection doctrine without selecting a case | No named cases admitted, no source authority, run, score, or proof |
| Level 1 product-learning core minimum | Repo-local product-learning core minimum | Names the reusable market-agnostic backtesting-first SCV pieces satellites must consume before filling domain-specific cases | Product-learning context only; no case run, source authority, prompt artifact, score, proof, live/client readiness, or judgment-quality claim |

## Core Ownership

Core Judgment owns the reusable structures future satellites must consume by
pointer:

- Claim-tier and closeout vocabulary.
- Receipt minima and promotion gates.
- Backtesting-first operating contract: `mode: backtest`, frozen evidence
  cutoff, future-information exclusion, and later-gated `live_internal` /
  `client_facing` modes.
- SCV loop contract: commission intake/gate, graph-family evidence plan,
  provenance-preserving extraction, qualitative weighting, forecast records,
  utility-bounded action, decision log, reveal, evaluation, benchmark
  comparison, and error labels.
- JSG conductor routing and no-authority discipline.
- The by-hand cap and no-tools/proven-isolation boundary.
- The market-agnostic demand-read core shape: C0 frame, C1 allow, C2 qualitative
  weighting, C3 verdict/action ceiling, C4 counterfactual.
- Qualitative weighting constraints: no numeric weight, score, formula, or
  deterministic apply-rule.
- Qualitative decision constraints: verdict/action ceiling vocabulary, weakest
  load-bearing evidence cap, fixed non-claims.
- Near-half/far-half/ledger interfaces, when and only when those proposed
  surfaces are accepted or otherwise explicitly consumed.

Core must not absorb fragrance facts. It should name the slot a satellite fills,
not the fragrance-specific content of that slot.

## Fragrance Satellite Ownership

The fragrance satellite may own:

- The first admitted fragrance casebook, after an explicit case-admission step.
- Fragrance source families and venue-specific access notes, consuming the
  promoted beauty venue card-set where applicable.
- Fragrance-specific evidence objects, source registries, and provenance notes.
- Fragrance signal IDs and discriminator tells, including Basenotes,
  Fragrantica, specialist fragrance blogs, and other adopted venue surfaces.
- Fragrance-specific utility/action examples that map into the C3 action
  ceiling without minting new action vocabulary.
- Product-learning receipts, decision logs, outcome labels, and evaluation
  spreadsheets for admitted cases.

The fragrance satellite must not own:

- Claim tiers or closeout states.
- JSG gate semantics or conductor predicates.
- Scoring authorization or scoring vocabulary.
- Numeric weighting models.
- Buyer-proof, validation, readiness, or judgment-quality claims.
- A source-capture authority claim unless an owning source-capture artifact
  separately adopts it.

## Decomposition Map

| Portion | Core owner/surface | Fragrance satellite first use | Boundary |
| --- | --- | --- | --- |
| Case framing / admission | C0 Decision Frame, case-finder, conductor run authorization boundary | Proposed 25-case fragrance casebook and cutoff plan | Casebook proposal is not run authorization or fixture admission |
| Commission gate / evidence plan | Level 1 core-minimum backtesting contract plus future prompt-orchestrated gate artifact | Fragrance decision type, playbook, source priorities, creator slices, confirmation/counterevidence, forecast targets | Gate brief is not final recommendation, source authority, or run authorization |
| Evidence capture / source plan | Source-capture owners plus C1 allow gate by pointer | Fragrance source registry, public venues, beauty venue card-set consumption | Venue hints are not source authority or captured evidence |
| Evidence object / packet | JSG-01, ECR, packing/finalization, packet construction | Fragrance graph-family artifact, evidence object schema, contradictions, timeline, and provenance plan | No JSG-01 clearance without authorized run evaluation |
| Weighting | C2 ledger read contract and signal-reliability ledger | Qualitative fragrance weighting rubric, caveat travel, signal IDs | No numeric weight, formula, or scoring engine |
| Forecast / expected outcome | Level 1 forecast-record contract plus far-half decision object and product-learning evaluation surfaces | Raw forecast probabilities, probability bucket, horizon, due date, and Brier hook | Outcome prediction is not a Judgment Spine claim; forecast records are learning inputs only |
| Decision / action ceiling | C3 verdict/action ceiling contract and Level 1 utility/action schema | Fragrance utility/action recommendation with target, trigger, stop condition, next action, and crux | No passive monitor, new action vocabulary, or unconstrained live action |
| Reveal / evaluation | JSG-08 reveal/calibration owner contract and near-half learning shell | Fragrance outcome labels, benchmark comparison, regret/error labels, and reveal comparison | Reveal comparison does not by itself create calibration, buyer proof, or judgment quality |
| Lesson capture | Near-half adversarial postmortem, validated-lesson cell, signal ledger | Candidate fragrance lessons and signal rows | Candidate lessons are N=0/unproven until promotion gates clear |
| Decision log / receipt | Evidence ladder product_learning_receipt shape | Per-case decision log, owner readback, friction/product signals | Completed product-learning evidence requires minimum receipt fields |

## Forecasting Boundary

Forecasting is useful, but it is not the center of the Judgment claim. The
evidence ladder states that Judgment Spine measures the best move under the
evidence available at the decision point, not correctness against the later
real-world outcome.

So the forecasting portion should be handled as:

- a decision-object or product-learning evaluation field when useful;
- a reveal/learning input after the outcome is known;
- a source of calibration questions for later loops;
- never a shortcut to judgment-quality evidence.

This prevents a common drift: turning a good or lucky outcome call into proof
that the judgment was good, or turning an unlucky but evidence-right call into a
false failure.

## First Work Slices After This Map

Current slice status:

1. **Done in this lane:** this current-state/decomposition map now bridges the
   reconciliation into a core/satellite split.
2. **Done in this lane:** the fragrance satellite skeleton exists as an
   organizer for casebook, source, evidence, weighting, forecast, decision,
   reveal, lesson, and receipt slots. It is not execution machinery.
3. **Done in this lane:** the casebook admission frame reserves the 25-slot
   shape and selection rules. It admits no named cases.
4. **Done in this lane:** the named-case candidate screen ranks first admission
   attempts. It recommends which case to try admitting first, but still admits
   no named case.
5. **Done in the dependent core-minimum lane:** the reusable **Level 1
   product-learning core minimum** now names the market-agnostic core pieces
   satellites must consume, what current Judgment already provides, what remains
   blocked, which slots satellites may fill, and what claims remain impossible.
6. **Next after the propagated core minimum:** prompt-orchestrated commission
   gate / Level 1 judgment prompts, source registry, outcome-label sheet,
   forecast/action/log/evaluation artifacts, named-case admission attempt,
   source/evidence plan, and per-case product-learning receipt template remain
   separate slices.

Top-level repo-map updates should stay thin. The repo map should route readers
to the Judgment consolidation map; the consolidation map remains the correct
local index for Judgment-specific current-state and core-minimum pointers.

## Non-Claims

This artifact is not validation, readiness, buyer proof, product proof,
judgment-quality evidence, prompt approval, run authorization, scoring
authorization, source-capture authority, conductor amendment, casebook
admission, or owner adoption of the fragrance temp pack.

It does not assert that the fragrance Level 1 plan works. It only states the
current source-backed shape of the work so the next artifacts can split without
claim inflation.

## Source-Read Ledger

- `docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md`
- `docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md`
- `docs/research/judgment-spine/judgment_spine_machinery_build_state_gap_map_v0.md`
- `docs/product/judgment_spine/judgment_spine_demand_read_machinery_architecture_v0.md`
- `docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md`
- `docs/product/judgment_spine/judgment_spine_c3_verdict_action_ceiling_contract_v0.md`
- `docs/product/judgment_spine/near_half_backtest_learning_architecture_v0.md`
- `docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md`
- `docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md`
- `docs/product/core_spine/beauty_venue_card_set_v0.md`
- `docs/product/judgment_spine/fragrance_level1_product_learning_reconciliation_v0.md`
- `docs/product/judgment_spine/fragrance_level1_product_learning_satellite_skeleton_v0.md`
- `docs/product/judgment_spine/fragrance_level1_casebook_admission_frame_v0.md`
- `docs/product/judgment_spine/fragrance_level1_named_case_candidate_screen_v0.md`
- `docs/product/judgment_spine/judgment_level1_product_learning_core_minimum_v0.md`
- `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_mgt_goal_v1.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_judgement_mgt.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_build_action_doc.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_commission_gate_prompt.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_judgement_prompt_level1.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_open_questions_working_doc.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_docs_split_manifest.md`
