# Judgment Spine Reveal Calibration Owner Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Case-agnostic owner contract for the JSG-08 outcome reveal/calibration receipt shape.
use_when:
  - Deciding whether a Judgment Spine case has satisfied the reveal/calibration gate.
  - Authoring or reviewing reveal readouts, outcome calibration records, scoring handoffs, or claim classifications.
  - Checking whether reveal/calibration material is being overclaimed as judgment-quality evidence.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md
  - orca/product/spines/judgment/conductor/judgment_spine_gate_ownership_map_v0.md
  - .agents/workflow-overlay/product-proof.md
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
input_hashes:
  docs/product/judgment_spine_evidence_ladder_architecture_v0.md: 79F6696DD50BE3FDCB574FD6AED4FE0761C6335029BFDBE39B51F104F4AD16CF
  .agents/workflow-overlay/product-proof.md: AD1724202841D616F74494B22E3659D7987CC875BD36BF0F23B12C210E4B19C4
  docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md: 3301224649991811D91B8B5932F0DFF18D3E356CB51979619BDBE3494BC9193C
  docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_reveal_readout_calibration_gate_adversarial_artifact_review_v0.md: 31362147A8557C0698A23A9D902AA5FFC71D8B973813F89DF9157D38ED0980EE
  docs/research/judgment-spine/cases/canoo-walmart/outcome_calibration_v0.md: 8E5766B11F80D716ACFB376E8227A9C610BBB906949AF65C9C1791A070C0A2F0
branch_or_commit: main @ dce7537
downstream_consumers:
  - docs/product/judgment_spine_gate_ownership_map_v0.md
  - .agents/workflow-overlay/source-loading.md
  - docs/workflows/orca_repo_map_v0.md
  - future Judgment Spine case outcome calibration records
  - future Judgment Spine claim classification and closeout records
stale_if:
  - docs/product/judgment_spine_evidence_ladder_architecture_v0.md changes judgment-quality receipt minima, claim tiers, or closeout states.
  - docs/product/judgment_spine_gate_ownership_map_v0.md changes JSG-08 ownership status or gate dependencies.
  - .agents/workflow-overlay/product-proof.md changes zero-spoiler, blind-judgment, or outcome-calibration lane boundaries.
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md changes clean execution, sealed output, or blind judgment gate semantics.
  - A later accepted scoring, fixture-admission, or operating-model artifact supersedes this contract.
```

## Source-Loading Surface

Purpose: define the case-agnostic owner surface and required receipt fields for
`JSG-08` before stronger Judgment Spine claims rely on outcome reveal or
calibration material.

Use when: a case, run, scoring artifact, fixture candidate, closeout record, or
review needs to know whether reveal/calibration evidence is absent,
reveal-only, qualitative calibration, score-linked calibration, or contaminated.

Do not use for: executing a model, revealing a live case, scoring a case,
admitting a fixture, validating Judgment Spine, creating buyer proof, or claiming
completed judgment-quality evidence.

Authority boundary: this contract owns the `JSG-08` receipt shape. It does not
own case-specific facts, source custody, no-tools isolation, sealed output,
scoring results, claim-tier vocabulary, or closeout-state vocabulary.

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_jsg_08_reveal_calibration_owner_contract
  edit_permission: docs-write
  target_scope:
    - docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md
    - docs/product/judgment_spine_gate_ownership_map_v0.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/workflows/orca_repo_map_v0.md
  dirty_state_checked: yes
  blocked_if_missing: no
  path_collision_checked:
    path: docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md
    existed_before_write: no
```

## Owner Decision

```yaml
jsg_08_owner_decision:
  gate_id: JSG-08
  gate_name: outcome_reveal_or_calibration_record
  owner_status_after_this_contract: owned
  owner_surface: docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md
  case_specific_receipt_owner: >
    The case artifact that records the reveal readout, outcome calibration, or
    combined reveal/calibration receipt owns the case-specific facts.
  required_for_completed_judgment_quality_evidence: yes
  reveal_readout_alone_clears_completed_judgment_quality_gate: no
  qualitative_calibration_alone_creates_scoring_or_fixture_claim: no
  score_linked_calibration_requires_jsg_07: yes
```

This contract closes the owner-surface question for `JSG-08`. It does not clear
`JSG-08` for any specific case. A case clears the gate only when its own durable
receipt satisfies the fields and claim boundaries below.

## Satisfaction States

| State | Use when | Claim effect |
| --- | --- | --- |
| `absent` | No durable reveal readout, outcome calibration, or combined receipt exists for the case. | The case must name `JSG-08` as missing or use `no_durable_evidence` for reveal/calibration claims. |
| `reveal_readout_only` | A durable artifact records revealed facts or post-reveal learning, but no calibration frame and comparison record has been declared. | Case-learning only. It cannot support `completed_judgment_quality_evidence`, buyer proof, scoring readiness, fixture admission, or validation. |
| `qualitative_outcome_calibration` | A durable calibration record compares sealed judgment output with reveal/outcome material under a declared frame, without using a scoring result. | May support qualitative product learning or case learning. It does not create a scoring result and does not by itself support fixture admission or judgment-quality evidence. |
| `score_linked_outcome_calibration` | A durable calibration record declares its frame and explicitly references the existing `JSG-07` scoring result or score artifact without changing it. | Satisfies the `JSG-08` owner-contract shape for stronger claims only if every other required gate also clears. It is not validation or proof by itself. |
| `contaminated_or_invalid` | Reveal, calibration, or scoring material entered the wrong lane, relied on unsealed output, inherited a biased frame without declaration, or cannot identify the revealed material. | Blocks stronger claims; use `blocked_or_contaminated` or the weakest unaffected lower state. |

## Required Receipt Fields

A case-specific `JSG-08` receipt must record the following fields or name the
field as missing:

```yaml
jsg_08_reveal_calibration_receipt:
  receipt_status: absent | reveal_readout_only | qualitative_outcome_calibration | score_linked_outcome_calibration | contaminated_or_invalid
  case_id:
  receipt_artifact:
  sealed_blind_output:
    artifact:
    hash_or_seal_reference:
    sealed_before_reveal: yes | no | unknown
  reveal_event:
    reveal_sequence_or_timestamp:
    reveal_operator_or_source:
    material_revealed:
    reveal_source_refs:
  calibration_frame:
    selected_frame:
    frame_declared_before_interpretive_reveal_use: yes | no | unknown
    axes:
    rejected_frames:
  comparison_inputs:
    contestant_output_refs:
    owner_or_baseline_judgment_refs:
    outcome_or_reference_refs:
  scoring_relationship:
    jsg_07_scoring_result: path_hash | not_scored | missing
    score_use: none_qualitative_only | references_existing_score | score_relationship_missing
    calibration_changes_score: no
  missing_evidence:
  failure_events:
  claim_cap:
  non_claims:
```

The receipt may live in a dedicated `outcome_calibration_vN.md`, a combined
case closeout artifact, or another accepted case artifact. The filename is not
the gate. The field contract is the gate.

## Reveal Readout Boundary

A reveal readout may preserve revealed facts, post-reveal context, tactical
lessons, and qualitative first-pass comparison. It is useful parent-side
material, but it is not enough to clear `JSG-08` for completed
judgment-quality evidence unless it also contains the required calibration
frame, comparison inputs, scoring relationship, missing-evidence labels, claim
cap, and non-claims.

If a reveal readout contains interpretive language before a calibration frame is
declared, the later calibration artifact must either declare an independent
frame before using that language or mark the frame relationship as missing or
contaminated.

## Calibration Frame Boundary

Outcome calibration must declare its comparison frame before inheriting
interpretive reveal-readout framing. Allowed examples include:

- `actual_action_alignment`;
- `later_outcome_alignment`;
- `combined_decision_quality_alignment`;
- a custom named frame with explicit axes.

The calibration record may reject frames. It must not silently let a reveal
readout decide whether the case evaluates action matching, outcome matching,
decision quality under uncertainty, or a combined axis.

Reveal readouts may contain interpretive sections that pre-select a calibration
frame before the calibration artifact exists. A calibration record must treat
that framing as a possible bias source and preserve its own declared frame
independently before using those interpretive sections.

## Scoring Relationship Boundary

`JSG-08` does not own scoring. `JSG-07` owns the scoring result and scoring
artifact relationship.

For qualitative calibration, record:

```yaml
scoring_relationship:
  jsg_07_scoring_result: not_scored
  score_use: none_qualitative_only
  calibration_changes_score: no
```

For score-linked calibration, record the existing scoring result path and hash.
The calibration artifact may interpret a score, but it must not create, revise,
or repair the score unless a separate scoring route authorizes that work.

## Claim Cap Rules

- `absent` or no durable artifact: no reveal/calibration evidence claim.
- `reveal_readout_only`: case-learning or product-learning context only.
- `qualitative_outcome_calibration`: qualitative case-learning or
  product-learning context only unless stronger gates are separately satisfied.
- `score_linked_outcome_calibration`: may satisfy `JSG-08` for stronger
  classification only when `JSG-01` through `JSG-07`, `JSG-09`, and `JSG-10`
  also clear under their controlling sources.
- `contaminated_or_invalid`: block stronger claims and name the affected gate.

No `JSG-08` state independently creates validation, readiness, buyer proof,
fixture admission, scoring authorization, model-execution authorization, or
completed judgment-quality evidence.

## Handoff Boundaries

- Evidence ladder owns claim tiers, closeout states, and the minimum
  judgment-quality receipt vocabulary.
- Gate ownership map records that `JSG-08` is owned by this contract.
- Product-proof owns zero-spoiler lane separation and the sequence:
  participant packet, facilitator ledger, blind judgment, then outcome
  calibration.
- No-tools execution contract owns clean execution and sealed output evidence.
- Case artifacts own case-specific reveal facts, calibration frames, missing
  evidence, and claim caps.

## Non-Claims

- This contract does not validate Judgment Spine.
- This contract does not create judgment-quality evidence.
- This contract does not authorize model execution.
- This contract does not authorize scoring.
- This contract does not admit a fixture.
- This contract does not prove blind-use readiness.
- This contract does not create buyer proof.
- This contract does not create product readiness.
- This contract does not clear `JSG-08` for any case-specific artifact.
- This contract does not perform outcome calibration for any case.
- This contract does not change any sealed output, score, case artifact, or
  source receipt.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Judgment Spine reveal/calibration promotion now has a case-agnostic JSG-08
    owner contract that distinguishes reveal-only material, qualitative
    calibration, score-linked calibration, and contaminated or absent receipts.
  trigger: architecture_doctrine
  controlling_sources_updated:
    - docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md
    - docs/product/judgment_spine_gate_ownership_map_v0.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/artifact-roles.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - docs/product/judgment_spine_evidence_ladder_architecture_v0.md
    - .agents/workflow-overlay/product-proof.md
    - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
    - docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_reveal_readout_calibration_gate_adversarial_artifact_review_v0.md
    - docs/research/judgment-spine/cases/canoo-walmart/outcome_calibration_v0.md
  intentionally_not_updated:
    - path: docs/product/judgment_spine_evidence_ladder_architecture_v0.md
      reason: >
        The ladder already owns claim tiers, closeout states, and the
        judgment-quality receipt minimum. This contract resolves gate ownership
        and receipt shape only.
    - path: .agents/workflow-overlay/product-proof.md
      reason: >
        Zero-spoiler lane sequence already separates blind judgment from
        outcome calibration. This contract binds the Judgment Spine gate
        receipt shape without changing buyer-proof semantics.
    - path: docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
      reason: >
        Clean no-tools execution and sealed blind output semantics did not
        change. JSG-08 consumes those receipts but does not redefine them.
    - path: Daimler-specific case, run, prompt, source, and decision artifacts
      reason: >
        This is case-agnostic owner-contract doctrine. Applying it to Daimler
        requires a separate case-specific reveal/calibration receipt or
        classification decision.
  stale_language_search: >
    rg -n "JSG-08|reveal/calibration|outcome_reveal_or_calibration_record|completed_judgment_quality_evidence|validation|readiness|buyer proof|fixture admission|scoring authorization|model execution"
    docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md
    docs/product/judgment_spine_gate_ownership_map_v0.md
    .agents/workflow-overlay/source-loading.md
    .agents/workflow-overlay/source-of-truth.md
    docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed on 2026-06-03 after the JSG-08 owner-contract patch and AR-01
    through AR-03 minor review patch. Hits in this contract are expected
    owner-contract, receipt-shape, satisfaction-state, claim-cap, non-claim,
    and propagation references. Hits in the gate map are expected owner-status
    rows, the owner-detail section, vocabulary, non-claims, and propagation
    references. Hits in source-loading, source-of-truth, and repo-map are
    expected navigation or source-list references. No hit converted the
    contract or navigation surfaces into validation, readiness, buyer proof,
    fixture admission, scoring authorization, model-execution authorization, or
    judgment-quality evidence.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not fixture admission
    - not scoring authorization
    - not model execution
    - not judgment-quality evidence
```
