# Fragrance Level 1 Product-Learning Reconciliation v0

```yaml
retrieval_header_version: 1
artifact_role: Judgment Spine product-learning reconciliation artifact
scope: >
  Maps the 2026-06-17 user-supplied fragrance (Vertical) Level 1 backtest pack onto
  current Orca Judgment Spine and demand-read surfaces while preserving the
  product-learning cap and non-claims.
use_when:
  - Aligning the fragrance Level 1 backtest pack with current Judgment Spine owners.
  - Deciding what may be authored next without replacing the JSG conductor.
  - Checking why this lane stays product-learning before any build or prompt promotion.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/judgment/judgment_current_state_and_decomposition_v0.md
  - orca/product/satellites/fragrance/judgment_level1/satellite_skeleton/fragrance_level1_product_learning_satellite_skeleton_v0.md
  - orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md
  - orca/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md
  - orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md
  - orca/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md
  - orca/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md
stale_if:
  - The current-state/decomposition map or fragrance Level 1 organizers change their MGT/SCV target, default mode, SCV loop, or live/client readiness gates.
  - The evidence ladder changes product_learning, buyer_proof, judgment_quality, or promotion gates.
  - The demand-read C0-C4 core is accepted, rejected, or materially amended.
  - A fragrance Level 1 pack is promoted into an accepted Orca docs path.
  - A blind-judgment live-execution runner or authorized real-case run changes the by-hand cap.
```

## Status

This is a docs-only reconciliation artifact. The separate Level 1 core artifact
has been retired by owner request; the current-state/decomposition map and
fragrance Level 1 organizers now route to the repo-local backtesting-first
product-learning context by pointer. This artifact still does not authorize a
run, authorize scoring, admit a named case (Case), or promote any prompt. The owner
confirmed in-thread on 2026-06-17 that this lane should stay product-learning.

## ELI5 Read

We found a strong draft plan for testing fragrance judgment. The repo already
has rules for what counts as learning, proof, and real judgment quality. The
safe move is to treat the fragrance plan like a practice notebook for learning,
not like a trophy that proves Orca is good yet.

So this artifact says where each draft piece fits in the existing system, and
where it must not be overstated.

## Fit Judgment

The fragrance Level 1 pack fits as a product-learning demand-read satellite:
a domain-specific backtest pack around source selection, evidence extraction,
forecasting, utility/action judgment, and learning-loop closeout.

It does not fit as a replacement for the Judgment Spine conductor. The
conductor routes, assembles, and verifies receipts; it must not compute
judgment quality, mint tiers, author missing receipts, or authorize runs.

It also does not fit as completed product-learning evidence yet. The
backtesting-first route is product-learning context only: there is no admitted
named fragrance case, no source registry, no case run, no
product_learning_receipt, no blind contestant execution, and no completed
evaluation ledger.

## Current Claim Classification

```yaml
evaluated_surface: fragrance_level1_product_learning_reconciliation_v0
source_quality_state: temp input pack reconciled against current repo owner sources
execution_quality_state: no case run, no prompt promotion, no scoring, no eval receipt
closeout_state: unreceipted_product_learning_context
claim_cap: product-learning context only
weakest_missing_or_failed_gate:
  - no admitted named fragrance Level 1 case
  - no source registry, forecast record, decision log, or evaluation sheet
  - no durable prompt artifact authored through workflow-prompt-orchestrator
  - no authorized real or backtest case run
  - no product_learning_receipt
  - no buyer_proof_receipt
  - no judgment_quality_receipt
receipt_artifact_or_gap: this artifact is reconciliation input; future per-case artifacts and run receipts remain required
```

## Mapping

| Temp pack component | Current Orca owner or surface | Use now | Do not claim |
| --- | --- | --- | --- |
| MGT / SCV target | `judgment_current_state_and_decomposition_v0.md` plus fragrance Level 1 organizers | Use as Level 1 product-learning context: backtesting-first, tight fragrance wedge, full loop through evaluation | Validation, readiness, or permission to expand scope |
| Fragrance Level 1 MGT goal | Demand-read product-learning satellite consuming current Judgment boundaries by pointer | Use as the domain target for a bounded public-fragrance backtest-learning pack | Buyer proof, client-facing authority, or judgment-quality claim |
| Commission intake and gate | Current-state/decomposition route plus future prompt-orchestrated gate artifact | Shape case intake, cutoff, decision type, playbook, source priorities, creator slices, confirmation/counterevidence, and forecast targets | Run authorization, final recommendation, prompt approval, or source authority |
| Source registry and public venues (Venue) | Source-capture satellite / source registry candidate material | Identify candidate source families and provenance requirements for fragrance backtests | Durable source-capture authority without separate adoption |
| Graph-family artifact and evidence object | Case packet / evidence packet preparation upstream of JSG-06 | Organize source facts, contradictions, timelines, evidence IDs, and provenance for later sealed judgment | Conductor edit, scoring schema change, ECR clearance, or JSG gate rewrite |
| Evidence weighting rubric | C2 ledger read contract | Keep as qualitative weighting and reasoning trace over relevance, strength, independence, recency, costliness, direction, and risks | Numeric scoring engine, weighted model, or precise calibration |
| Forecast record and Brier-style eval | Current-state/decomposition forecast boundary plus near-half product-learning evaluation surface | Store raw probabilities, probability buckets, horizons, due dates, later outcome labels (Outcome), and Brier hooks as learning material | JSG-08 calibration, buyer proof, or judgment-quality evidence |
| Utility and action recommendation | C3 verdict/action ceiling contract plus current-state/decomposition utility/action boundary | Bind recommendations to bounded action family, magnitude, timing, trigger, stop condition, next action, and crux | Passive monitor, new action vocabulary, or unconstrained live action |
| Decision log and eval spreadsheet | Product-learning receipt candidate plus future lesson ledger | Preserve what was decided, when, from what evidence, what forecasts/actions were sealed, and how it later scored | Completed product-learning evidence until receipt fields are complete |
| Twenty-five-case fragrance casebook (Case) | Case-finder / casebook admission candidate | Use as the first success condition for a repeatable backtest-learning pack | Accepted batch, benchmark, calibration, readiness screen, or proof |

## Product-Learning Cap

The evidence ladder says lower-tier learning must not be reused as a stronger
claim without explicit promotion gates. Product-learning can inform next
experiments, but it does not by itself support buyer proof, product proof,
clean no-tools validation, blind-use validation, or judgment-quality evidence.

The conductor separately caps by-hand JSG-04/05/06 work at product-learning.
That matters here because the fragrance pack currently describes docs,
prompts, source plans, manual extraction, and evaluation surfaces. It does not
provide a proven isolated contestant execution path.

## Assumption Gate Ledger

```yaml
gate: workflow-assumption-gate
status: READY_WITH_VERIFIED_LEDGER
applies_to: docs-only reconciliation artifact for fragrance Level 1 product-learning
verified_assumptions:
  - assumption: The temp pack is draft input, not current Orca authority.
    verification: temp files live outside repo docs; the MGT/SCV target is now repo-local only as product-learning context through the current-state/decomposition map and fragrance Level 1 organizers.
  - assumption: Product-learning is the correct claim boundary.
    verification: owner confirmed "stay product learning"; evidence ladder and conductor cap lower-tier and by-hand work.
  - assumption: Demand-read C0-C4 is the closest current fit.
    verification: current demand-read sources define C0 frame, C1 allow, C2 qualitative ledger read, and C3 verdict/action ceiling.
blocker_agents:
  - Any future artifact that claims validation, readiness, buyer proof, judgment quality, run authorization, scoring authorization, or prompt adoption.
deferrable_owner_decisions:
  - Which exact fragrance cases form the first admitted casebook.
  - Whether any prompt artifact should be authored through workflow-prompt-orchestrator.
```

## Mini God Tier Handling

The temp pack's MGT language is now repo-local only as product-learning context
through the current-state/decomposition map and fragrance Level 1 organizers.
It is not a claim tier. For this product-learning reconciliation, the visible
limitations are:

- No live/client workflow or readiness gate clearance.
- No admitted named fragrance case.
- No completed 25-case backtest pack.
- No source registry, forecast record, decision log, or evaluation sheet.
- No autonomous retrieval runner.
- No new scoring engine or scoring authorization.
- No numeric weighting model.
- No buyer proof.
- No judgment-quality evidence.
- No conductor rewrite.
- No prompt promotion.

These limitations are the price of keeping the first move small and reversible.

## Next Docs-Only Moves

1. If prompts are needed, author the commission-gate and Level 1 judgment prompt
   artifacts through `workflow-prompt-orchestrator`.
2. Create or point to the source registry, outcome-label sheet, forecast record,
   decision log, benchmark policy, and evaluation sheet required by the
   Level 1 route.
3. If case selection is next, make a named-case admission artifact before any
   run, score, or lesson-ledger claim.
4. If evidence capture is next, keep source families and provenance as a
   satellite input until an owning source-capture artifact adopts them.

## Non-Claims

This artifact is not validation, readiness, buyer proof, product proof,
judgment-quality evidence, prompt approval, run authorization, scoring
authorization, source-capture authority, conductor amendment, prompt artifact,
`live_internal` readiness, `client_facing` readiness, or proof that the
fragrance backtest route works.

It does not assert that the fragrance Level 1 plan works. It only reconciles
the plan to current Orca boundaries so the next document can be authored
without accidentally overstating the claim.

## Source-Read Ledger

User-supplied temp pack:

- `orca_mgt_goal_v1.md`
- `orca_build_action_doc.md`
- `orca_judgement_mgt.md`
- `orca_commission_gate_prompt.md`
- `orca_judgement_prompt_level1.md`
- `orca_open_questions_working_doc.md`
- `orca_docs_split_manifest.md`

Repo owner and routing sources:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `docs/decisions/orca_mini_god_tier_doctrine_v0.md`

Judgment Spine sources:

- `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md`
- `docs/research/judgment-spine/judgment_spine_machinery_build_state_gap_map_v0.md`
- `orca/product/spines/judgment/judgment_current_state_and_decomposition_v0.md`
- `orca/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md`
- `orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md`
- `orca/product/spines/judgment/conductor/judgment_spine_gate_ownership_map_v0.md`
- `orca/product/spines/judgment/conductor/judgment_spine_reveal_calibration_owner_contract_v0.md`
- `orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md`
- `orca/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md`
- `orca/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md`
- `orca/product/spines/judgment/learning_loops/near_half/near_half_backtest_learning_architecture_v0.md`
