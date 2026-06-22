# Demand Read Machinery Settlement Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Product-planning prompt artifact
scope: >
  Commission a bounded Orca lane to settle the demand-read machinery: naming,
  canonical axes, C0-C4 behavior, action ceiling, monitoring/durability boundary,
  proof status, and patch implications.
use_when:
  - Commissioning a focused lane to settle Orca's demand-read machinery.
  - Checking whether "transient" should be renamed or externally reframed.
  - Preventing demand-read settlement from drifting into capture/runtime/build work.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/decisions/orca_product_thesis_consumer_demand_v0.md
  - orca/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md
  - orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md
  - orca/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md
  - orca/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md
stale_if:
  - The owner amends the demand-state model, action vocabulary, buyer-proof hard gate, or demand-read C2/C3 contracts.
  - A later demand-read settlement or owner decision supersedes this prompt.
```

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: required_on_intake
  overlay_read: required_on_intake
  source_pack: custom_S3_demand_read_machinery
  edit_permission: docs-write
  target_scope: product doctrine + architecture doctrine settlement for demand-read machinery only
  dirty_state_checked: required
  blocked_if_missing: AGENTS.md, overlay README, source-loading, decision-routing, source-of-truth, product thesis, demand-read taxonomy, C2 contract, C3 contract
```

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated here.

Output mode: `file-write`.

Template kind: `product` / product-planning commission. No registered Orca product template is currently bound; use this filed prompt body as the durable prompt source.

Authorization basis: owner requested a new lane prompt to settle the demand-read machinery after deprecating PR #260's old historical durability-probe artifact. This prompt authorizes documentation/product-planning output only.

Edit permission: `docs-write` for a settlement artifact and, if necessary, a bounded patch plan. Do not implement runtime, capture, automation, scoring, data-lake, scheduler, dashboard, scraper, browser automation, or API work.

Suggested output artifact: `orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_settlement_v0.md`.

Dirty-state allowance: read repo state before writing. Work on a clean branch or worktree off current `origin/main`; do not mix with unrelated dirty files.

Doctrine change decision: likely yes. If the lane changes naming, canonical action vocabulary, demand-state semantics, proof boundaries, or settlement status, it must include a `direction_change_propagation` receipt or a `direction_change_propagation_blocker` under `.agents/workflow-overlay/source-of-truth.md`.

Validation gates:

- `python .agents/hooks/check_map_links.py --strict`
- `python .agents/hooks/header_index.py --strict`
- `git diff --check`
- targeted stale-language search over the touched demand-read/product-proof surfaces for superseded terms if the lane renames or realigns vocabulary

## Objective

Settle Orca's demand-read machinery enough that downstream capture, ECR, Cleaning, Judgment, product-proof, and satellite lanes can consume one coherent model without relearning or forking it.

The lane must specifically decide whether internal `transient` should remain the canonical term, be renamed, or receive a separate buyer-facing label. The owner floated `trendy`; treat that as a hypothesis to evaluate, not an instruction to adopt.

## Source-Gated Method Contract

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. Read `.agents/workflow-overlay/decision-routing.md`. Run the Cynefin router before planning because this is product/architecture doctrine settlement.
3. REFERENCE-LOAD any workflow methods you use as procedural guidance only. Do not APPLY them yet.
4. SOURCE-LOAD the task sources below.
5. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, conflicts, stale state, and excluded sources.
6. Only after source readiness, APPLY methods and produce the settlement.

## Required Reads

Read these current workspace files before making strict or actionable claims:

- `docs/decisions/orca_product_thesis_consumer_demand_v0.md`
  - sections: 2026-06-14 Demand-State Model amendment; 2026-06-20 headline value proposition; 2026-06-20 action vocabulary amendment; Thesis; Falsifiers; Non-Claims.
- `orca/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md`
  - sections: Status; Function In One Sentence; Signal Layers; Read Types; Calling Sequence; Non-Claims.
- `orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md`
  - sections: Consumer-Demand Refinement; Demand-Substrate Hard Gate; Proof Standard; Target Buyer; Kill Criteria; Graduation Criteria; Not-Proven Boundaries.
- `orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md`
  - sections: Status; Target Architecture; C0-C4 core; Invariants; Non-Claims; Claim Classification.
- `orca/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md`
  - sections: Status; Required Behavior; Rule 3; Acceptance Criteria; Claim Classification.
- `orca/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md`
  - sections: 2026-06-20 amendments; Input Basis; Required Behavior; Interfaces / Contracts; Acceptance Criteria; Claim Classification.

Available if material, but do not bulk-load by default:

- `orca/product/spines/judgment/demand_read/core/judgment_spine_first_demand_read_scope_v0.md`
- `orca/product/spines/judgment/demand_read/grading/judgment_spine_demand_read_grading_rubric_v0.md`
- `orca/product/satellites/fragrance/judgment_level1/satellite_skeleton/fragrance_level1_product_learning_satellite_skeleton_v0.md`
- `orca/product/shared/engagement_registry/engagement_logic_registry_v0.md`
- `orca/product/spines/capture/core/demand_durability_indicators/capture_envelope_durability_delta_spec_v0.md`

Excluded by default:

- closed PR #260's harvested probe spec, unless used only as deprecated history;
- broad review outputs;
- all prompts;
- all proof-run packets;
- runtime/source-capture implementation files.

## Working Context To Verify

Treat this as orientation only; verify against required reads:

- PR #260 was deprecated because the old one-off historical durability probe no longer matches the current stance.
- Current stance: durability is observed through monitored signal behavior over time, not predicted upfront.
- Current demand-state model separates persistence (`durable` / `transient`) from integrity (`real` / `manufactured`).
- The action vocabulary is `monitor`, `probe`, `commit`, `hold`, `scale`, `avoid`, `reduce`.
- Engagement/attention volume alone must not carry a material demand read. Costly behavior and independent converging origins govern the action ceiling.
- Current proof status is not robust/validated. Much of the machinery is design/product-learning until by-hand reads, monitoring outcomes, buyer proof, and/or judgment-quality gates exist.

## Questions To Settle

1. **Naming.** Should internal canonical `transient` remain? Should a buyer-facing label differ? Evaluate `trendy` explicitly.
   - Push hard if `trendy` weakens precision. It may imply fashionability, taste, or category buzz rather than real-but-decaying demand.
   - Consider alternatives such as `short-window demand`, `spike demand`, `in-window demand`, `momentum demand`, or `transient demand`.
   - Decide internal term, buyer-facing term, and forbidden terms.
2. **Demand-state model.** Confirm or amend the two-axis model: persistence (`durable` / `transient`) and integrity (`real` / `manufactured`).
3. **Calling sequence.** Confirm or amend: first call opens conservative; durability is earned by monitored persistence, not predicted.
4. **C0-C4 machinery.** State the minimal operative model from C0 Frame through C4 Counterfactual. Name what belongs to Judgment versus Product Lead, Capture, ECR, Cleaning, Outcome Memory, and satellites.
5. **C2/C3 settlement.** Confirm how C2 qualitative weighting and C3 verdict/action ceiling interact, including Rule 3 and the no-scoring invariant.
6. **Action ceiling.** Confirm whether the seven-verb set remains complete and whether any downstream surface still carries stale old verbs or horizon vocabulary.
7. **Proof boundary.** State exactly what is designed, proposed, owner-adopted, product-learning only, buyer-proof-gated, or judgment-quality-gated. Do not upgrade proof status.
8. **Monitoring boundary.** Define what the first monitoring loop must observe before a read can upgrade from transient to durable. If the threshold is unknown, name it as a blocker and owner decision, not a hidden default.
9. **Robustness path.** Name the smallest path to test whether the demand read is actually strong: by-hand reads, outcome memory, monitored series, buyer readback, or judgment-quality backtest.
10. **Patch implications.** List exact files that should be amended if the settlement is accepted. Separate mandatory coherence patches from optional wording cleanup.

## Output Contract

Write one settlement artifact at the suggested path unless a better accepted product-spine path is justified in the output.

The artifact must include:

- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
- Human summary: the settled model in plain language.
- Naming decision: internal term, buyer-facing term, rejected terms, and rationale.
- Machinery decision: C0-C4 with source-owner boundaries.
- Proof status: what can be claimed now and what cannot.
- Monitoring/durability rule: what earns durable and what remains unknown.
- Patch plan: exact files, mandatory vs optional, with doctrine-change propagation needs.
- Code-enforceable versus judgment-only obligations.
- Next authorized action.
- Non-claims: not validation, not buyer proof, not judgment-quality proof, not implementation authorization, not capture authorization, not a scoring engine.

If the lane writes or patches any product artifact, include retrieval metadata and run the validation gates above. If the lane only returns an advisory recommendation without writing, state that output mode changed to `chat-only` and explain why the filed prompt's requested `file-write` could not be satisfied.

## Hard Stops

Stop and return `BLOCKED_SOURCE_CONTEXT_INCOMPLETE` if any required demand-read owner file is missing, conflicted, or visibly superseded without a clear successor.

Stop and return `BLOCKED_DOCTRINE_CHANGE_UNBOUND` if the lane would change canonical demand-state or action vocabulary but cannot carry a direction-change propagation receipt.

Stop and return `BLOCKED_IMPLEMENTATION_SCOPE` if the work requires runtime, capture, automation, scoring, scheduler, database, dashboard, or source-system implementation.

Stop and return `BLOCKED_OWNER_DECISION_REQUIRED` if the lane cannot choose between internal and buyer-facing naming without owner input after analysis.
