# Judgment Level 1 Product-Learning Core Minimum v0

```yaml
retrieval_header_version: 1
artifact_role: Judgment Spine product artifact (Level 1 product-learning core minimum)
scope: >
  Defines the reusable market-agnostic Level 1 product-learning minimum that
  satellites must consume before they fill domain-specific backtest case,
  source, evidence, weighting, forecast, utility/action, decision-log,
  reveal/evaluation, lesson, or receipt slots.
use_when:
  - Deciding what core Judgment pieces a Level 1 satellite may rely on.
  - Checking which Level 1 pieces are still missing or blocked before case admission or run planning.
  - Applying the accepted backtesting-first MGT/SCV target from the uploaded 2026-06-17 docs.
  - Preventing fragrance or another satellite from owning claim tiers, gate semantics, run authorization, scoring, or proof claims.
open_next:
  - docs/product/judgment_spine/judgment_current_state_and_decomposition_v0.md
  - docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md
  - docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md
  - docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md
  - docs/research/judgment-spine/judgment_spine_machinery_build_state_gap_map_v0.md
  - docs/product/judgment_spine/fragrance_level1_product_learning_satellite_skeleton_v0.md
  - docs/product/judgment_spine/fragrance_level1_casebook_admission_frame_v0.md
  - docs/product/judgment_spine/fragrance_level1_product_learning_reconciliation_v0.md
branch_or_commit: >
  Authored on dependent branch codex/judgment-level1-core-minimum based on
  PR #230 head dec37f13cd63a8e683aafeca7851f700e1f0c064.
stale_if:
  - PR #230 changes before landing and this dependent branch is not rebased and reread.
  - The evidence ladder changes claim tiers, closeout states, receipt minima, or promotion gates.
  - The conductor changes its no-authority invariant, by-hand cap, JSG routing, or run authorization boundary.
  - The gate ownership map changes JSG ownership, receipt ownership, or blocked-claim boundaries.
  - The build-state gap map changes blind-execution, real-run, JSG-01 binding, source/evidence binding, or case-finder status.
  - The accepted MGT/SCV target, default operating mode, 25-case backtest bar, outcome labels, source-registry governance, commission-gate playbooks, forecast/action/log/evaluation contracts, or live/client readiness gates are materially amended.
  - A Level 1 satellite admits a named case, completes a product-learning receipt, or receives source-capture/run/scoring authorization.
authority_boundary: retrieval_only
```

## Status

This is a docs-only product-learning core-minimum artifact. It names the
minimum reusable Level 1 surface that satellites should consume by pointer and
propagates the accepted shape of the uploaded 2026-06-17 MGT/SCV pack into the
repo: **backtesting-first**, tight-fragrance wedge first, live/internal later,
client-facing last.

It does not run a case, admit a case, authorize source capture, authorize model
execution, authorize scoring, publish a prompt artifact, or promote any claim.

Claim cap for this artifact: `unreceipted_product_learning_context`.

This artifact depends on PR #230 landing first. If PR #230 changes before this
dependent lane lands, rebase or recreate the dependency, then rerun the source
load against the new PR head before using this artifact.

## Source-Loading Surface

Purpose: give future Level 1 satellites a compact market-agnostic checklist for
what must live in Judgment core and what may be filled by a domain satellite.

Use when:

- starting a Level 1 satellite after current-state/decomposition;
- checking whether a satellite can move from organizer slots toward case
  admission or product-learning receipt work;
- checking whether a Level 1 artifact honors the default backtest mode, cutoff
  discipline, source registry, outcome labels, forecast/action/log/evaluation
  loop, and live/client readiness gates;
- reviewing whether a satellite is trying to own core Judgment semantics.

Do not use for:

- claim-tier definitions or closeout vocabulary;
- JSG gate semantics, predicate changes, or run lifecycle changes;
- source-capture authority, packet-grade evidence capture, or ECR/Cleaning work;
- durable prompt authoring; commission-gate or judgment prompt artifacts still
  require `workflow-prompt-orchestrator`;
- named-case admission, run authorization, model execution, scoring, buyer
  proof, validation, fixture admission, readiness, live/client readiness, or
  judgment-quality claims.

Authority boundary: this artifact routes to the owner sources. If it disagrees
with the evidence ladder, conductor, gate ownership map, build-state gap map,
source-capture owners, or a case-specific accepted artifact, the owner source
wins and this artifact is stale for that point.

Recheck recipe:

1. Confirm the branch still descends from the intended PR #230 head or a landed
   descendant.
2. Open the Judgment consolidation map first.
3. Open the evidence ladder for claim caps and receipt minima.
4. Open the conductor for routing, no-authority discipline, by-hand cap, and run
   lifecycle.
5. Open the gate ownership map for gate owners and blocked-claim boundaries.
6. Open the build-state gap map before any built-vs-gap or run-executability
   claim.
7. Open the relevant satellite artifact before saying what a satellite has
   already filled.

## Core Minimum

The Level 1 product-learning core minimum is the smallest reusable Judgment
surface a satellite must be able to point at before it treats its domain fields
as more than organizer slots.

It is not the entire Judgment core. It is not a harness build plan. It is not a
case runner. It is the minimum reusable contract that keeps a Level 1 satellite
from inflating its case, source, forecast, decision, reveal, lesson, or receipt
fields into stronger claims.

## Backtesting-First MGT / SCV Contract

The accepted Level 1 target from the uploaded MGT/SCV pack is:

```text
historical public fragrance case
-> frozen evidence cutoff
-> commission intake
-> commission gate / value-of-information brief
-> graph-family evidence plan
-> provenance-preserving evidence extraction
-> qualitative evidence weighting
-> simple forecasts
-> utility-scored bounded action recommendation
-> decision log
-> outcome reveal
-> evaluation, benchmark comparison, regret/error labeling, and calibration notes
```

Default operating mode:

```json
{
  "mode": "backtest",
  "evidence_cutoff_at": "YYYY-MM-DD",
  "future_information_policy": "exclude all information after cutoff"
}
```

`live_internal` and `client_facing` are later modes. They are not default
Level 1 work and this artifact does not authorize either.

MGT is the capability bar: most of the maximal system's useful decision value
from source-backed evidence, forecasts, utility/action, decision log, and
evaluation. SCV is the build boundary: the smallest loop that completes
backtest evidence cutoff through evaluation without fragile gaps.

Level 1 is not complete if it only produces trend summaries, creator
monitoring, research memos, passive "monitor" answers, unscoreable actions, or
case organizer slots. It is also not smallest if it adds causal inference,
off-policy evaluation, contextual bandits, Bayesian hierarchy, private-data
integrations beyond placeholders, fine-tuning, automated policy learning,
enterprise workflow tooling, full beauty-wide coverage, live/client default
deployment, or calibration claims before enough completed backtests exist.

The first success condition is a repeatable 25-case public fragrance backtest
pack: cases have cutoff dates, evidence versions, forecast records,
utility/action assumptions, decision logs, outcome labels, benchmark policy
comparisons, and error labels. Passing that pack would permit only a later
shadow/live-readiness discussion; it would not prove validation, buyer proof,
readiness, or judgment quality.

## Level 1 SCV Components

The reusable Level 1 core minimum includes these backtesting components:

| Component | Minimum role | Boundary |
| --- | --- | --- |
| Backtest mode contract | Require `mode`, cutoff date, and future-information exclusion before any evidence plan or judgment output | Not live or client-facing mode |
| Commission intake | Capture decision question, buyer type, decision deadline, constraints, risk tolerance, unacceptable actions, and decision authority | Not generic research |
| Commission gate / value-of-information brief | Route evidence before retrieval: decision type, playbook, source priorities, creator slices, mandatory confirmation/counterevidence, forecast targets, redirect/stop rules | Not final recommendation, run authorization, or source authority |
| Source registry governance | Use public, repeatable, provenance-preserving source families; preserve source/date/SKU/access/snippet or URL where material | Venue hints are not source-capture authority |
| Graph-family evidence plan | Return evidence neighborhoods, contradictions, timelines, and evidence IDs rather than isolated facts | Not ECR clearance or packet validity by itself |
| Evidence object schema | Preserve entity, source type, source date, access date, claim, snippet/URL, direction, behavior type, independence, and risk flags | Not captured evidence unless owned source route admits it |
| Qualitative evidence weighting | Read relevance, strength, independence, recency, costliness, direction, and risk flags before judgment | No numeric scoring engine or formula |
| Forecast records | Store target, horizon, cutoff, included evidence, raw probability bucket, due date, outcome label, and Brier hook | No calibration claim until enough completed backtests exist |
| Utility/action schema | Produce one bounded action family with magnitude, timing, trigger, stop condition, next action, crux, confidence bucket, and limitations | Passive "monitor" is disallowed |
| Decision log | Preserve evidence version, forecasts, utility assumptions, action, limitations, and outcome due dates | Not a product-learning receipt unless receipt minima are satisfied |
| Evaluation record | Reveal outcomes only after freeze; score Brier, public proxy utility, regret, benchmarks, and error labels | Evaluation is learning input, not proof |
| Readiness gates | Keep backtest -> `live_internal` -> `client_facing` ordered; require completed cases, provenance learning, benchmarks, calibration review, and decision-rights language before later modes | No readiness claim from setup docs |

Core owns the market-agnostic component contract above. A satellite may fill
domain instances only after the component's owner boundary is respected.

| Core piece | Owner source | Minimum Level 1 role | Satellite may fill | Satellite must not own |
| --- | --- | --- | --- | --- |
| Claim cap and closeout vocabulary | Evidence ladder | Classify the surface as product-learning context, completed product-learning evidence, or a lower/blocked state by owner vocabulary | A case-specific classification or receipt pointer | Claim tiers, closeout states, promotion gates |
| Product-learning receipt minimum | Evidence ladder | Provide the minimum fields for completed product-learning evidence | Case ID, prompt/answer handle, owner readback, product/friction signals, non-claims | Buyer-proof or judgment-quality receipt fields |
| Gate route and no-authority discipline | Conductor | Keep JSG-01 through JSG-10 as owner-routed gates and prevent the conductor or satellite from self-clearing gates | Pointers to case-specific receipts when they exist | Gate predicates, run lifecycle semantics, model/run/scoring authorization |
| Gate ownership and blocked-claim boundaries | Gate ownership map | Identify who owns each JSG receipt and which stronger claims are blocked if missing | Case-specific missing-gate notes | Gate ownership or receipt semantics |
| Build/run executability state | Build-state gap map | Separate built plumbing from missing execution/case-finder/run surfaces | A case-specific gap note after reread | Readiness, validation, or run-executability claims |
| Case admission boundary | Current-state/decomposition plus satellite casebook frame | Require a separate named-case admission record before a candidate becomes admitted | Domain case ID, cutoff, source families, outcome label plan, benchmark policy | Fixture admission, run authorization, or source-capture authority |
| Source/evidence boundary | Source-capture owners plus JSG-01 owners by pointer | Keep source family hints and evidence packet plans separate from source authority | Candidate venues, source-family notes, provenance plan, held/prohibited sources | Capture authority, source-family admission, ECR clearance, packet validity |
| Qualitative demand read | Current-state C0-C4 pointers, especially C1/C2/C3 owner surfaces | Keep allow, qualitative weighting, and verdict/action ceiling market-agnostic | Domain signal IDs, qualitative direction, caveats, no-row handling, action examples mapped onto owner vocabulary | Numeric weights, formulas, scores, new action vocabulary |
| Forecast/reveal/lesson loop | Current-state decomposition, JSG-08 owner contract, near/far learning surfaces by pointer | Treat forecasts and reveals as learning inputs, not proof of judgment quality | Forecast field, measurement window, reveal comparison, candidate lessons | Calibration, proof, validated lessons, or outcome-as-score claims |
| Non-claims and promotion guard | Evidence ladder, conductor, gate map | Keep every Level 1 artifact capped until receipts and gates exist | Domain-specific non-claims and blocker notes | Buyer proof, product proof, readiness, scoring authorization, judgment-quality evidence |

## What Current Judgment Already Provides

The current source-loaded Judgment surface provides these reusable core pieces:

- The evidence ladder owns claim tiers, closeout states, weakest-cleared-gate
  discipline, and minimum receipt fields.
- The conductor owns routing through JSG-01 to JSG-10, the no-authority
  invariant, the route-don't-restate rule, run lifecycle labels, and the
  by-hand cap.
- The gate ownership map owns gate-owner routing and names which stronger
  claims are blocked when required gate receipts are missing.
- The build-state gap map records the current built-vs-gap inventory: scoring,
  memorization probe, schemas/reports/tests, ECR derivers, SP-5 finalizer, and
  JSG-01 binding are recorded there as built; blind-judgment contestant
  execution under proven isolation, an authorized real non-synthetic run, and
  the case-finder remain recorded gaps.
- The current-state/decomposition artifact owns the core/satellite split and
  keeps fragrance as a satellite, not the core.
- The fragrance satellite skeleton and casebook frame reserve domain slots but
  do not admit named cases or authorize execution.
- The uploaded MGT/SCV pack has now been reduced into the backtesting-first
  Level 1 SCV contract above: default `backtest` mode, 25 public fragrance
  cases, source registry governance, outcome labels, commission-gate playbooks,
  graph/evidence artifacts, forecast/action/log/evaluation records, and
  live/client readiness gates.

## What Remains Missing Or Blocked

These are blockers for treating any Level 1 satellite case as run-ready or
proof-bearing:

- No named Level 1 fragrance case is admitted by the current fragrance artifacts.
- Durable Orca prompt artifacts now exist for the commission gate and Level 1
  judgment output:
  `docs/prompts/product-planning/judgment_level1_commission_gate_prompt_v0.md`
  and
  `docs/prompts/product-planning/judgment_level1_judgment_prompt_v0.md`.
  They are prompt surfaces only, not case-specific gate briefs, judgment
  outputs, prompt approval, source-capture authority, run authorization, scoring,
  proof, or readiness.
- No backtest case intake form, source registry sheet, outcome-label sheet,
  graph-family template, forecast record sheet, decision log sheet, benchmark
  policy sheet, or evaluation spreadsheet exists by this artifact.
- No satellite has a case-specific captured evidence packet or source-capture
  authority by this artifact.
- No authorized real non-synthetic run is recorded by this artifact.
- Blind-judgment contestant execution under proven isolation remains a recorded
  gap in the build-state gap map.
- No completed Level 1 `product_learning_receipt` exists for any fragrance case
  in this lane.
- No buyer-proof receipt or judgment-quality receipt exists for this Level 1
  slice.
- PR #230 must land or be otherwise incorporated before this dependent branch is
  treated as mainline-reachable.

Missing evidence is a cap, not a pass. A satellite may use the gaps to plan the
next docs-only slice, but it must not convert them into readiness, validation,
proof, or run authority.

## Satellite Fill Contract

A Level 1 satellite may fill only domain-specific instances:

- casebook candidates and later named-case admission records;
- domain source-family notes, registry rows, source-plan fields, and provenance
  notes that preserve cutoff/date/SKU limits;
- case-specific evidence references and provenance notes;
- C1/C2/C3 domain reads that preserve owner vocabulary and caveats;
- commission-gate brief fields, graph-family plan fields, forecast records,
  utility/action records, decision-log fields, reveal/evaluation hooks, and
  lesson fields as learning inputs;
- product-learning receipt fields when the minimum receipt can be satisfied;
- domain-specific non-claims and blocker notes.

A Level 1 satellite must not fill or redefine:

- claim tiers, closeout states, promotion gates, or receipt minima;
- JSG gate semantics, predicates, ownership, or run lifecycle states;
- no-tools, memorization-probe, sealed-output, scoring, or reveal/calibration
  gate-clearance rules;
- source-capture authority or ECR/Cleaning handoff obligations;
- numeric weighting, scoring, formulas, or deterministic apply rules;
- C3 action vocabulary beyond mapping domain examples onto the owner vocabulary;
- passive "monitor" recommendations without target, trigger, stop condition,
  timebox, and next action;
- buyer-proof, product-proof, readiness, validation, fixture-admission,
  scoring, blind-use, run authorization, `live_internal`, `client_facing`, or
  judgment-quality claims.

## Minimum Per-Case Progression

Use this as a Level 1 progression checklist, not as execution authorization.

| State | Minimum durable artifact | Strongest claim before next state |
| --- | --- | --- |
| Candidate | Candidate screen, queue, or casebook row | Product-learning context only |
| Admitted for Level 1 attempt | Named-case admission record with all admission-minimum fields and `mode: backtest` unless explicitly overridden | Case admitted for learning setup only; no capture/run authority |
| Commission gate bounded | Commission intake plus gate/value-of-information brief naming playbook, source priorities, confirmation/counterevidence, forecast targets, redirect rules, and stop conditions | Evidence-plan context only; not recommendation or run authority |
| Source registry and outcome labels bounded | Source-family governance plus case-relevant outcome-label plan | Product-learning planning context only |
| Source/evidence plan bounded | Source/evidence plan that points to source-capture owners and names prohibited/held sources | Product-learning planning context only |
| Evidence packet available | Captured packet or evidence object admitted by the owning source/capture/JSG-01 route | At most the owner-cleared source/evidence state; no run claim by itself |
| Qualitative read and decision sealed | C1/C2/C3 trace, forecast records, utility/action object, and decision log sealed before reveal when evaluation is intended | Product-learning process context unless receipt completed |
| Reveal/eval recorded | Outcome labels, benchmark comparisons, regret/error labels, and reveal comparison under the JSG-08 owner boundary | Learning input; not calibration or judgment-quality by itself |
| Product-learning receipt complete | Evidence-ladder `product_learning_receipt` minimum fields complete | Completed product-learning evidence only |

Any state that lacks its named durable artifact remains at the weaker prior
state or `unknown`.

## Claim Classification

```yaml
judgment_spine_claim_classification:
  evaluated_claim_surface: judgment_level1_product_learning_core_minimum_v0
  source_quality_state: >
    docs-only market-agnostic core-minimum artifact derived from the current
    Judgment source pack and dependent on PR #230 head dec37f13.
  execution_quality_state: >
    no admitted case, no captured case-specific evidence packet, no sealed
    answer, no model execution, no scoring, no reveal comparison, and no
    completed product-learning receipt.
  closeout_state: unreceipted_product_learning_context
  claim_cap: product-learning context only
  weakest_missing_or_failed_gate:
    - no case-specific product_learning_receipt
    - no admitted named Level 1 case by this artifact
    - no case-specific commission-gate brief or Level 1 judgment output by this artifact
    - no source registry, outcome-label sheet, forecast record, decision log, or evaluation sheet by this artifact
    - no source-capture authority or captured evidence packet by this artifact
    - no authorized real run by this artifact
    - no buyer_proof_receipt
    - no judgment_quality_receipt
  receipt_artifact_or_gap: >
    This artifact is setup context. Future per-case product-learning receipts
    remain required before completed product-learning evidence can be claimed.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not product proof
    - not source-capture authority
    - not run authorization
    - not scoring authorization
    - not live_internal readiness
    - not client_facing readiness
    - not fixture admission
    - not judgment-quality evidence
```

## Next Docs-Only Moves

After this core minimum is map-reachable and PR #230 is accounted for, the next
useful docs-only moves are:

1. Use the durable prompt artifacts at
   `docs/prompts/product-planning/judgment_level1_commission_gate_prompt_v0.md`
   and
   `docs/prompts/product-planning/judgment_level1_judgment_prompt_v0.md` only
   after the relevant case intake/admission and source boundaries are supplied.
2. Create the backtest case intake, outcome-label sheet, source registry sheet,
   graph-family template, forecast record sheet, decision log sheet, benchmark
   policy sheet, and evaluation spreadsheet as docs/planning artifacts before
   any first-case run.
3. Admit-attempt packet for the first named fragrance case, still with no source
   capture or run authorization.
4. Fragrance source/evidence plan that points to source-capture owners rather
   than claiming source authority.
5. Per-case product-learning receipt template or first receipt only after a
   named case and evidence plan are bounded.

Do not broaden the fragrance skeleton into run execution before the backtest
mode contract, commission gate, source registry, outcome labels,
forecast/action/log/evaluation artifacts, case admission, and source boundary
blockers are resolved.

## Non-Claims

This artifact is not validation, readiness, buyer proof, product proof,
judgment-quality evidence, source-capture authority, prompt approval, prompt
artifact, run authorization, scoring authorization, fixture admission, accepted
benchmark, completed product-learning evidence, `live_internal` readiness,
`client_facing` readiness, owner adoption of any fragrance case, or proof that a
Level 1 satellite works.

It does not change the evidence ladder, conductor, gate ownership map,
build-state gap map, source-capture owners, or fragrance satellite artifacts. It
only names the minimum core surface a satellite must consume without claim
inflation.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Level 1 product-learning now adopts the backtesting-first MGT/SCV target
    from the 2026-06-17 uploaded docs as repo-local product doctrine: default
    mode is historical public-fragrance `backtest` with a frozen evidence cutoff
    and future-information exclusion; the SCV loop runs commission intake/gate,
    graph-family evidence plan, provenance-preserving extraction, qualitative
    weighting, forecasts, utility-bounded action, decision log, reveal, and
    evaluation; live/internal and client-facing modes remain later gated modes.
    This changes Level 1 product-learning routing and satellite-fill contract
    only; it does not change claim tiers, closeout states, conductor routing,
    JSG gate ownership, source-capture authority, scoring, run authorization,
    buyer proof, readiness, or judgment-quality evidence.
  trigger: product_doctrine
  related_triggers:
    - architecture_doctrine
  controlling_sources_updated:
    - docs/product/judgment_spine/judgment_level1_product_learning_core_minimum_v0.md
    - docs/product/judgment_spine/judgment_current_state_and_decomposition_v0.md
    - docs/product/judgment_spine/fragrance_level1_product_learning_reconciliation_v0.md
    - docs/product/judgment_spine/fragrance_level1_product_learning_satellite_skeleton_v0.md
    - docs/product/judgment_spine/fragrance_level1_casebook_admission_frame_v0.md
    - docs/product/judgment_spine/fragrance_level1_named_case_candidate_screen_v0.md
    - docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md
    - docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md
    - docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md
    - docs/product/judgment_spine/judgment_spine_reveal_calibration_owner_contract_v0.md
    - docs/product/judgment_spine/judgment_spine_demand_read_grading_rubric_v0.md
    - docs/product/judgment_spine/judgment_spine_demand_read_machinery_architecture_v0.md
    - docs/research/judgment-spine/judgment_spine_machinery_build_state_gap_map_v0.md
    - docs/prompts/handoffs/judgment_spine_harness_product_first_proof_relevance_handoff_prompt_v0.md
    - docs/prompts/handoffs/judgment_spine_read_machinery_architecture_handoff_v0.md
  intentionally_not_updated:
    - path: docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md
      reason: >
        Claim tiers, closeout states, promotion gates, and receipt minima are
        unchanged and are consumed by pointer.
    - path: docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md
      reason: >
        Conductor routing, no-authority discipline, by-hand cap, and run
        lifecycle states are unchanged and are consumed by pointer.
    - path: docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md
      reason: >
        JSG gate ownership and blocked-claim boundaries are unchanged and are
        consumed by pointer.
    - path: docs/research/judgment-spine/judgment_spine_machinery_build_state_gap_map_v0.md
      reason: >
        Built-vs-gap state is unchanged; this artifact only points to that map
        before any run-executability claim.
    - path: docs/product/judgment_spine/judgment_spine_reveal_calibration_owner_contract_v0.md
      reason: >
        JSG-08 reveal/calibration satisfaction states and caps are unchanged.
        This patch only routes Level 1 backtest evaluation toward that owner.
    - path: docs/product/judgment_spine/judgment_spine_demand_read_grading_rubric_v0.md
      reason: >
        Backtest-only grading and monitoring-window limits already exist there;
        this patch does not amend grading semantics.
    - path: docs/prompts/handoffs/judgment_spine_harness_product_first_proof_relevance_handoff_prompt_v0.md
      reason: >
        Prompt artifacts require a `workflow-prompt-orchestrator` pass. This
        product-doctrine patch records the stale route risk but does not
        hand-edit prompt artifacts.
    - path: docs/prompts/handoffs/judgment_spine_read_machinery_architecture_handoff_v0.md
      reason: >
        Prompt artifacts require a `workflow-prompt-orchestrator` pass. This
        product-doctrine patch records the stale route risk but does not
        hand-edit prompt artifacts.
  stale_language_search: >
    rg -n --glob '!judgment_level1_product_learning_core_minimum_v0.md'
    "review_velocity_sustains|creator_momentum_persists|search_interest_persists|learning_only \| blind_backtest_candidate|owner adoption of the temp pack|no accepted fragrance pack|If the owner accepts this reconciliation|Whether to promote any temp-pack component"
    docs/product/judgment_spine docs/research/judgment-spine docs/workflows/orca_repo_map_v0.md
    docs/prompts/handoffs/judgment_spine_harness_product_first_proof_relevance_handoff_prompt_v0.md
    docs/prompts/handoffs/judgment_spine_read_machinery_architecture_handoff_v0.md
  stale_language_search_result: >
    Executed 2026-06-17 after this propagation patch, excluding this receipt
    file from its own literal-pattern scan. The checked product, research,
    repo-map, and two prompt-handoff surfaces had no hits for the old
    outcome-label spellings, old admission-mode enum, or old "temp pack not
    accepted" route phrases. Prompt handoff artifacts remain intentionally
    unedited because durable prompt artifacts require a
    `workflow-prompt-orchestrator` pass.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not product proof
    - not source-capture authority
    - not implementation authorization
    - not run authorization
    - not scoring authorization
    - not prompt artifact authorization
    - not live_internal readiness
    - not client_facing readiness
    - not fixture admission
    - not judgment-quality evidence
```

## Source-Read Ledger

- Current user instruction: continue from `codex/judgement-lane` at
  `dec37f13cd63a8e683aafeca7851f700e1f0c064`; create or reset dependent
  branch; rerun confirm-don't-trust; do not merge or close PR #230.
- Current user instruction: the Level 1 core minimum is done but likely reflects
  old documents; propagate the uploaded MGT/SCV docs and use 5.4/5.3 subagents
  if required.
- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/validation-gates.md`
- `docs/workflows/artifact_retrievability_guide.md`
- `docs/workflows/orca_repo_map_v0.md`
- `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md`
- `docs/research/judgment-spine/judgment_spine_machinery_build_state_gap_map_v0.md`
- `docs/product/judgment_spine/judgment_current_state_and_decomposition_v0.md`
- `docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md`
- `docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md`
- `docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md`
- `docs/product/judgment_spine/fragrance_level1_product_learning_satellite_skeleton_v0.md`
- `docs/product/judgment_spine/fragrance_level1_casebook_admission_frame_v0.md`
- `docs/product/judgment_spine/fragrance_level1_named_case_candidate_screen_v0.md`
- `docs/product/judgment_spine/fragrance_level1_product_learning_reconciliation_v0.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_mgt_goal_v1.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_judgement_mgt.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_build_action_doc.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_commission_gate_prompt.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_judgement_prompt_level1.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_open_questions_working_doc.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_docs_split_manifest.md`
- Subagent audit: GPT-5.4 explorer `019ed622-a038-7131-b42a-759d18e87ce7`
  (doctrine delta audit; read-only).
- Subagent audit: GPT-5.3 Codex Spark explorer
  `019ed622-d89a-7c63-8b26-c3d8fb6a4411` (product stale-surface search;
  read-only).
- Subagent audit: GPT-5.3 Codex Spark explorer
  `019ed623-0bc9-76c0-9aa2-fcfa789b09a6` (map/prompt/research stale-surface
  search; read-only).
