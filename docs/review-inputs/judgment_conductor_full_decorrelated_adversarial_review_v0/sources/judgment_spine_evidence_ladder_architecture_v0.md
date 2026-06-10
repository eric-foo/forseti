# Judgment Spine Evidence Ladder Architecture v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Claim-tier and closeout-state architecture for separating Judgment Spine product-learning, buyer-proof, and judgment-quality evidence.
use_when:
  - Classifying what a Judgment Spine run, case, model answer, memo, or proof artifact can claim.
  - Naming the closeout state for partial, missing, contaminated, or fully receipted evidence.
  - Preventing manual advisory output from being reused as buyer proof or judgment-quality evidence.
  - Deciding which promotion gates are required before a stronger Judgment Spine claim.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/product-proof.md
  - .agents/workflow-overlay/validation-gates.md
  - docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
input_hashes:
  AGENTS.md: 5800D6EC863102DC680A6FDB91199337BC8CAC65A4C820FE3F94610B0AFA82A1
  .agents/workflow-overlay/README.md: 40E28238868A423CD43559C1BE5C312E088439E596ECE8AFD25E73835A62A27F
  .agents/workflow-overlay/source-of-truth.md: CB03B26D6140D418FA3E91DE9B2F14141030E7682227E73167E999B6D207CD27
  .agents/workflow-overlay/source-loading.md: 835BD6A1D8B65657C700878053DFAA71FC76C302613925270986419E847FB7B9
  .agents/workflow-overlay/product-proof.md: AD1724202841D616F74494B22E3659D7987CC875BD36BF0F23B12C210E4B19C4
  .agents/workflow-overlay/validation-gates.md: F43041E2E501D9F29632E1BB69A1F19A54F4B0FAD7FED5073F4F95731024C3C7
  docs/workflows/orca_repo_map_v0.md: 5EA74405AD8A912EEB4C54F3526743F5614C6298F8040253C61951D077A58884
  docs/product/README.md: D0B1C53CCB8B7DA9C2CCEBDF511CD41B4C1614B59D912471AB4B09D610516377
  docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md: 94988650A7A9DF8AA051BBF0E5526FD6022721440219E7FDE29DBD80F60755F3
  docs/product/orca_buyer_proof_packet_v0.md: ECDCD4BFC626295D486189F063CA8429EA2F324BD71151C9D28A52683927A224
  docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md: A257AE82D36216EB9099D269C2EAD0587E9063764B9011C4F45229852678D344
  docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md: 3301224649991811D91B8B5932F0DFF18D3E356CB51979619BDBE3494BC9193C
  docs/decisions/daimler_advisory_run_001_authorization_record_v0.md: 2BA36EDEACF80D8B0E979EC922D1E66947EDEA42B372921727AC9F69A20F43AC
  docs/prompts/handoffs/daimler_advisory_run_001_manual_execution_handoff_v0.md: 7218E35191702429A40EFD38404BDE2F7ECC9AD7091617900F35FA27FCF42DFF
  docs/prompts/wrappers/daimler_advisory_run_001_manual_execution_handoff_wrapper_v0.md: 7F5F3AAEF4D4777E4EF79FC4451098552A9566041DAD282492DB227B78802CED
branch_or_commit: main @ c939ba3d234980c99b49bbbe9ba8325b5933cab4
downstream_consumers:
  - .agents/workflow-overlay/product-proof.md
  - .agents/workflow-overlay/validation-gates.md
  - .agents/workflow-overlay/source-loading.md
  - docs/workflows/orca_repo_map_v0.md
stale_if:
  - Judgment Spine claim tiers are renamed, merged, split, or retired.
  - Judgment Spine closeout-state vocabulary is renamed, merged, split, or retired.
  - Buyer-proof semantics change in .agents/workflow-overlay/product-proof.md.
  - Gate-bearing execution requirements change in contestant_no_tools_execution_contract_v0.md.
  - A later accepted artifact supersedes this claim-tier architecture.
```

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_judgment_spine_closeout_state_patch
  edit_permission: docs-write
  target_scope:
    - docs/product/judgment_spine_evidence_ladder_architecture_v0.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/workflows/orca_repo_map_v0.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
  dirty_state_checked: yes
  blocked_if_missing: no
  dirty_or_untracked_notes:
    - docs/product/judgment_spine_evidence_ladder_architecture_v0.md was untracked before this patch.
    - .agents/workflow-overlay/validation-gates.md was modified before this patch.
```

## Purpose

This artifact establishes the Judgment Spine evidence ladder so future Orca work
can classify a run or artifact by what it actually supports.

The ladder prevents a lower-tier signal from being reused as a stronger claim.
A usable manual advisory answer can be valuable product-learning evidence, but
it does not become buyer proof or judgment-quality evidence unless the separate
promotion gates for those tiers are satisfied.

## Claim Tiers

```yaml
judgment_spine_claim_tiers:
  product_learning:
    purpose: Internal learning about packet usability, operator friction, narrative clarity, and product experience.
    typical_surfaces:
      - manual subscription/chat advisory answer
      - owner readback
      - packet-friction note
      - non-gate-bearing model comparison
    may_support:
      - package-usability learning
      - product-narration learning
      - operator-friction discovery
      - candidate packet patch priorities
    cannot_support_by_itself:
      - buyer proof
      - product proof
      - fixture validation or admission
      - scoring readiness
      - clean no-tools evidence
      - blind-use readiness
      - judgment-quality claim

  buyer_proof:
    purpose: Evidence that a qualified decision owner can use Orca's memo/evidence artifact for a live allocation decision.
    typical_surfaces:
      - buyer-qualified manual memo
      - evidence appendix
      - buyer readback tied to a live decision
      - internal buyer circulation or budget-adjacent pull signal
    may_support:
      - buyer usefulness signal
      - proof-memo fit signal
      - decision-owner pull grading
      - commercial-next-step hypothesis evidence
    cannot_support_by_itself:
      - clean no-tools evidence
      - fixture validation or admission
      - judgment-quality claim
      - model-family blind-use authorization

  judgment_quality:
    purpose: Controlled evidence about whether a sealed Judgment Spine run produced a clean, scoreable, calibrated judgment under harness-grade constraints.
    typical_surfaces:
      - frozen participant packet
      - frozen facilitator ledger
      - structural no-tools execution receipt
      - clean memorization-probe gate result
      - sealed blind judgment output
      - scoring result
      - outcome reveal and calibration record
      - repeatability or failure analysis across preselected cases
    may_support_when_all_gates_are_met:
      - clean blind contestant output
      - scoring and calibration analysis
      - fixture admission consideration
      - judgment-quality evidence
    cannot_support_by_itself:
      - buyer validation
      - willingness-to-pay proof
      - product readiness
      - commercial readiness
```

## Closeout States

`closeout_state` is required whenever a Judgment Spine artifact classifies
proof, readiness, validation, fixture admission, scoring, blind use, or
judgment-quality status.

The state records where the evaluated claim actually closed after both source
quality and execution quality were checked. It is not a fourth evidence tier,
and it does not rename Product-Learning, Buyer-Proof, or Judgment-Quality.

```yaml
judgment_spine_closeout_states:
  no_durable_evidence:
    use_when: >
      The evaluated claim has no durable raw output, run receipt, source
      custody receipt, or other artifact that can carry that claim. Adjacent
      specs, prompts, wrappers, runbooks, source lists, or prior-thread memory
      do not count as durable evidence for a run, answer, proof, or judgment.
    claim_cap: none
    may_support:
      - route planning
      - gap identification
      - tooling backlog discovery
    blocked_claims:
      - completed product-learning evidence
      - buyer proof
      - judgment-quality evidence

  unreceipted_product_learning_context:
    use_when: >
      Some durable material exists for the evaluated product-learning surface,
      but the minimum product-learning receipt is incomplete or the material is
      limited to design context, source-custody context, a durable owner-note
      artifact, or unsealed-answer context. A durable owner-note must have a
      path, hash, timestamp, or equivalent retrieval handle; prior-thread
      memory or owner recollection alone does not qualify.
    claim_cap: product-learning context only
    may_support:
      - product narration questions
      - packet patch hypotheses
      - operator-friction discovery
      - source/tooling blocker discovery
    blocked_claims:
      - completed product-learning evidence
      - buyer proof
      - judgment-quality evidence

  completed_product_learning_evidence:
    use_when: >
      The minimum product-learning receipt is complete, and stronger
      buyer-proof and judgment-quality receipts are absent.
    claim_cap: product_learning
    blocked_claims:
      - buyer proof
      - judgment-quality evidence

  completed_buyer_proof_evidence:
    use_when: >
      The minimum buyer-proof receipt is complete, and a separate
      judgment-quality receipt is absent.
    claim_cap: buyer_proof
    blocked_claims:
      - judgment-quality evidence

  completed_judgment_quality_evidence:
    use_when: >
      The minimum judgment-quality receipt is complete under the controlling
      harness contract.
    claim_cap: judgment_quality
    blocked_claims:
      - buyer validation by itself
      - willingness-to-pay proof by itself
      - product readiness by itself

  blocked_or_contaminated:
    use_when: >
      Leakage, post-cutoff contamination, tool-use breach, missing isolation,
      missing source identity, unreconciled scoring failure, or another
      material defect breaks the evaluated gate.
    claim_cap: weakest unaffected gate, often none
    required_note: name the failed or contaminated gate before any reuse.
```

## Source-Quality x Execution-Quality Matrix

The matrix is a cap table for the evaluated claim, not a checklist that grants
success. The fourth column states the ceiling after the named receipts and
gates are independently satisfied; it is not permission to claim the ceiling.
If a row does not fit, use the weakest-cleared-gate rule below and record the
missing evidence.

| Source-quality state | Execution-quality state | Default `closeout_state` | Claim cap, not success grant |
| --- | --- | --- | --- |
| No durable artifact for the evaluated claim | Any | `no_durable_evidence` | No evidence claim; routing/gap discovery only. |
| Design/control artifacts only | No run, answer, buyer use, or sealed output | `no_durable_evidence` for run/proof/judgment claims | Design input only. |
| Durable source custody or packet context, but incomplete product-learning receipt | No sealed or gate-bearing execution | `unreceipted_product_learning_context` | Product-learning context only. |
| Complete product-learning receipt | Manual or non-gate-bearing execution | `completed_product_learning_evidence` | Product-Learning. |
| Complete buyer-proof receipt | Buyer-qualified use/readback under proof gates | `completed_buyer_proof_evidence` | Buyer-Proof. |
| Complete judgment-quality receipt | Clean isolated execution, sealed output, scoring, reveal/calibration record | `completed_judgment_quality_evidence` | Judgment-Quality. |
| Any material source or execution contamination | Any affected execution | `blocked_or_contaminated` | Weakest unaffected gate; often none. |

## Promotion Rules

Evidence may move upward only through an explicit promotion gate. A lower-tier
artifact can inform the next tier's design, but it cannot carry its claim
forward.

Weakest-cleared-gate rule: a Judgment Spine classification must cap the claim
at the weakest required source-quality or execution-quality gate actually
cleared. If source quality and execution quality point to different caps, use
the lower cap. Missing evidence is a cap, not a pass.

Sub-floor rule: when the evaluated run, answer, buyer-proof artifact, scoring
artifact, or judgment-quality claim has no durable evidence of its own, the
state is `no_durable_evidence`. Specs, prompts, wrappers, runbooks, source
capture receipts, architecture documents, prior-thread memory, or owner
recollection may explain what should happen next, but they do not fill the
missing run/proof/judgment receipt.

| From | To | Required promotion gate |
| --- | --- | --- |
| Product Learning | Buyer Proof | Qualified buyer, live decision context, memo plus evidence appendix, buyer readback, and pull-versus-praise classification under `.agents/workflow-overlay/product-proof.md`. |
| Product Learning | Judgment Quality | New gate-bearing authorization, frozen packet boundary, structural no-tools evidence, memorization-probe routing, sealed blind judgment, and scoring path under `contestant_no_tools_execution_contract_v0.md`. |
| Buyer Proof | Judgment Quality | Separate harness-grade run. Buyer usefulness, memo circulation, deck interest, or paid-sprint pull does not prove clean model judgment. |
| Judgment Quality | Buyer Proof | Separate buyer-facing proof. A clean scored run can support product narration, but buyer proof still requires a qualified decision owner and live decision use. |

## Required Receipts By Tier

### Claim Classification Record

Any artifact making or blocking a stronger Judgment Spine claim should name the
classification inline or co-reference a durable classification record:

```yaml
judgment_spine_claim_classification:
  evaluated_claim_surface:
  source_quality_state:
  execution_quality_state:
  closeout_state:
  claim_cap:
  weakest_missing_or_failed_gate:
  receipt_artifact_or_gap:
  non_claims:
    - not validation unless separately proven
    - not readiness unless separately proven
    - not buyer proof unless the buyer-proof receipt is complete
    - not judgment-quality evidence unless the judgment-quality receipt is complete
```

### Product Learning Receipt

Minimum receipt fields:

```yaml
product_learning_receipt:
  case_or_packet_id:
  selected_surface_named_before_run: true | false | unknown
  model_or_chat_surface:
  prompt_artifact:
  prompt_body_only_confirmed: true | false | unknown
  raw_answer_location:
  owner_readback_captured: true | false
  product_signals:
    - <signal>
  friction_signals:
    - <friction>
  non_claims:
    - not buyer proof
    - not product proof
    - not clean no-tools evidence
    - not fixture validation or admission
    - not scoring
    - not judgment-quality evidence
```

Missing pre-run surface selection weakens process hygiene but does not make the
answer useless for product learning. It does block any attempt to call the run
clean, controlled, gate-bearing, or stronger than product-learning evidence.

### Buyer-Proof Receipt

Minimum receipt fields:

```yaml
buyer_proof_receipt:
  buyer_or_decision_owner:
  live_decision_context:
  memo_artifact:
  evidence_appendix_artifact:
  readback_or_use_signal:
  trust_state: trust_open | trust_objection | trust_refusal
  pull_grade: A | B | C | D
  commercial_next_step_signal:
  non_claims:
    - not judgment-quality evidence
    - not clean no-tools evidence
    - not fixture admission
    - not product readiness unless separately accepted
```

### Judgment-Quality Receipt

Minimum receipt fields:

```yaml
judgment_quality_receipt:
  case_id:
  selected_model_family_and_id:
  owner_authorization:
  frozen_participant_packet_hash:
  frozen_facilitator_ledger_hash:
  prompt_hash:
  memorization_probe_result:
  execution_isolation_result: proven
  sealed_blind_judgment_hash:
  scoring_result:
  outcome_reveal_or_calibration_record:
  failure_events:
  non_claims:
    - not buyer validation
    - not willingness-to-pay proof
    - not product readiness by itself
```

## Daimler / GPT-5.4 Boundary

The Daimler GPT-5.4 manual advisory material is not a completed evidence
receipt in this lane.

Current source state:

- `docs/decisions/daimler_advisory_run_001_authorization_record_v0.md` records
  `advisory_run_execution_status: not_run_by_this_record` and leaves execution
  preconditions as `REQUIRED_UNSET`.
- `docs/prompts/handoffs/daimler_advisory_run_001_manual_execution_handoff_v0.md`
  records that no model run has occurred and no advisory output exists yet.
- `docs/prompts/wrappers/daimler_advisory_run_001_manual_execution_handoff_wrapper_v0.md`
  preserves the boundary that wrapper plumbing is not validation, scoring,
  product proof, or judgment quality.

Therefore this artifact does not claim that a Daimler GPT-5.4 answer exists as
a durable Orca evidence artifact. Any owner-stated, prior-thread, or otherwise
unreceipted Daimler advisory output may be used only as candidate
product-learning context until a completed `product_learning_receipt` records a
real `raw_answer_location`.

If a later durable Daimler advisory answer is supplied, the minimum
classification remains `product_learning` unless and until the stronger
promotion gates are satisfied. The completed receipt must record the selected
surface, model or chat surface, prompt artifact, prompt-body-only confirmation,
raw answer location, owner readback, product signals, friction signals, and
non-claims.

Blocked stronger claims:

- No durable raw answer location is recorded in this lane.
- The current run-control surfaces still say no run or no output exists.
- No selected chat surface is durably recorded as completed before a run.
- No structural no-tools execution occurred.
- GPT-5.4 was not shown to have cleared a memorization probe for Daimler.
- No frozen facilitator ledger, sealed blind judgment artifact, scoring result,
  reveal, calibration record, buyer readback, or buyer pull signal exists from
  this run.

Therefore the current Daimler material may inform packet patch hypotheses,
product narration questions, and architecture planning only as unreceipted
product-learning context. It must not be cited as buyer proof, product proof,
fixture validation or admission, clean no-tools evidence, scoring readiness,
blind-use readiness, or judgment-quality evidence.

## Core / Satellite Boundary

Core owns:

- claim-tier vocabulary;
- closeout-state vocabulary;
- tier promotion gates;
- weakest-cleared-gate cap rules;
- required receipt minima;
- non-claim boundaries;
- evidence-reuse limits across tiers.

Satellites own:

- case facts and packet construction;
- source-family choices;
- model/provider or chat-surface choices;
- case-specific probe status;
- buyer/demo packaging;
- owner readback notes;
- case-specific patch priorities.

Daimler remains satellite. The evidence ladder is case-agnostic.

## Non-Claims

- This artifact does not validate Judgment Spine.
- This artifact does not prove buyer pull.
- This artifact does not constitute buyer-proof evidence.
- This artifact does not prove product readiness.
- This artifact does not prove judgment quality.
- This artifact does not authorize model execution.
- This artifact does not authorize API execution.
- This artifact does not authorize scoring.
- This artifact does not admit any fixture.
- This artifact does not freeze a facilitator ledger.
- This artifact does not resolve reveal/calibration gate ownership.
- This artifact does not authorize implementation, runtime design, tests,
  deployment, commits, pushes, or PRs.

Required boundary: claim architecture only; not validation or readiness.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Judgment Spine evidence classification now must name a ladder-owned
    closeout_state and apply source-quality, execution-quality, and
    weakest-cleared-gate caps before stronger proof, readiness, validation,
    fixture, scoring, blind-use, or judgment-quality claims.
  trigger: architecture_doctrine
  controlling_sources_updated:
    - docs/product/judgment_spine_evidence_ladder_architecture_v0.md
    - .agents/workflow-overlay/product-proof.md
    - .agents/workflow-overlay/validation-gates.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/product-proof.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Existing Judgment Spine Evidence Ladder Read Pack already routes
        claim-tier, proof-tier, buyer-proof-boundary, and judgment-quality
        classification work to this ladder; closeout_state changes the ladder
        vocabulary, not the read-pack route.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Existing repo-map navigation already points Judgment Spine claim-tier
        and judgment-quality boundary work to this ladder; no new artifact or
        navigation destination was created.
    - path: docs/product/judgment_quality_promotion_operating_model_v0.md
      reason: >
        Deferred by owner decision; this patch intentionally adds ladder-owned
        closeout states before any later thin operating-model spine.
    - path: Daimler-specific run, prompt, source, and decision artifacts
      reason: >
        Daimler exposed the blocker, but this patch is case-agnostic doctrine.
        Changing satellite case artifacts would require a separate run receipt
        or case-specific closeout decision.
  stale_language_search: >
    rg -n "closeout_state|closeout state|weakest-cleared-gate|no_durable_evidence|judgment-quality|buyer proof|buyer-proof|claim-tier"
    docs/product/judgment_spine_evidence_ladder_architecture_v0.md
    .agents/workflow-overlay/product-proof.md
    .agents/workflow-overlay/validation-gates.md
    .agents/workflow-overlay/source-loading.md
    docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed on 2026-06-02. The closeout-state search returned expected
    matches in this ladder, the aligned product-proof boundary, the aligned
    validation gate, source-loading read pack, and repo-map navigation.
    Source-loading and repo-map hits already route Judgment Spine claim-tier
    and judgment-quality boundary work to this ladder. A stale-pattern scan for
    observed Daimler/GPT-5.4 answer language, the prior ambiguous owner-note
    wording, the old matrix grant header, and pending validation markers
    returned no matches.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not judgment-quality proof
    - not implementation authorization
```
