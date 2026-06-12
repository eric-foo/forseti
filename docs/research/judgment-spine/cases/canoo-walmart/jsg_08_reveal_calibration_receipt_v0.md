# Canoo/Walmart JSG-08 Reveal Calibration Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Case-specific JSG-08 companion receipt for Canoo/Walmart reveal and calibration state.
use_when:
  - Checking whether the Canoo/Walmart case has a durable JSG-08 reveal/calibration receipt.
  - Classifying the case before any later claim-tier, closeout, fixture, scoring, or proof work.
  - Preserving why current Canoo/Walmart material remains qualitative case-learning or product-learning context only.
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine/judgment_spine_reveal_calibration_owner_contract_v0.md
  - docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md
  - docs/research/judgment-spine/cases/canoo-walmart/case_index.md
  - docs/research/judgment-spine/cases/canoo-walmart/outcome_calibration_v0.md
input_hashes:
  docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md: ED146BEB5767EFDDA3E979AA798CA5CB044A896421872B02FBDF03615E4E6E07
  docs/research/judgment-spine/cases/canoo-walmart/blind_judgments_v0.md: 2DF41433DCFACB31832CD51E65EC424888B7EB8955115D6949A35E8C7F2E8225
  docs/research/judgment-spine/cases/canoo-walmart/owner_context_judgments_v0.md: A12BDC0416FC41502AB0B46B70338FF40FF118008D5D808C5E91BDD265E3B2E8
  docs/research/judgment-spine/cases/canoo-walmart/pre_reveal_judgment_comparison_v0.md: 2AD850D94A29438D54491AA5EE72D8D79332E04F6C78E03BF960CF28BEEAEE80
  docs/research/judgment-spine/cases/canoo-walmart/facilitator_ledger_v0.md: 6356C45D8E9B75732DB3D146EABFFCE4AD2775BCDD23D0205E26A46222FCE739
  docs/research/judgment-spine/cases/canoo-walmart/reveal_readout_v0.md: 927DB2F16D3D9DF9EBB9DF20F6A35F00659C7C671EEC8ADAF4104BD7535C3A7E
  docs/research/judgment-spine/cases/canoo-walmart/outcome_calibration_v0.md: 8E5766B11F80D716ACFB376E8227A9C610BBB906949AF65C9C1791A070C0A2F0
  docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_reveal_readout_calibration_gate_adversarial_artifact_review_v0.md: 31362147A8557C0698A23A9D902AA5FFC71D8B973813F89DF9157D38ED0980EE
stale_if:
  - Any input hash changes.
  - Any cited input artifact remains untracked when a future route needs strict provenance or gate-clearance evidence.
  - A later JSG-07 scoring result, clean harness-format model run, fixture-admission decision, or claim classification supersedes this receipt.
  - New evidence establishes Walmart delivery performance, unit acceptance volume, route uptime, operational harm or gain, termination-right exercise, financial exposure at bankruptcy, or protective-term effectiveness.
  - The JSG-08 owner contract changes receipt fields, satisfaction states, scoring relationship, or claim caps.
```

## Source-Loading Surface

Purpose: apply the case-agnostic JSG-08 owner contract to the current
Canoo/Walmart case artifacts without changing their historical lifecycle.

Use when: a future route needs to know whether Canoo/Walmart has no durable
reveal/calibration evidence, reveal-only material, qualitative outcome
calibration, score-linked outcome calibration, or a contaminated/invalid state.

Do not use for: model execution, scoring, fixture admission, validation,
readiness, buyer proof, or completed judgment-quality evidence.

Authority boundary: this receipt classifies the current case-specific JSG-08
state from existing artifacts. It does not own JSG-07 scoring, JSG-09 claim
classification, JSG-10 closeout state, source custody, or clean execution proof.

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_canoo_walmart_jsg_08_receipt
  edit_permission: docs-write
  target_scope:
    - docs/research/judgment-spine/cases/canoo-walmart/jsg_08_reveal_calibration_receipt_v0.md
    - docs/research/judgment-spine/cases/canoo-walmart/case_index.md
    - docs/research/judgment-spine/manifest_v0.md
  dirty_state_checked: yes
  blocked_if_missing: no
  path_collision_checked:
    path: docs/research/judgment-spine/cases/canoo-walmart/jsg_08_reveal_calibration_receipt_v0.md
    existed_before_write: no
  observed_case_state: qualitative_outcome_calibration_exists
  implementation_lock:
    receipt_status: qualitative_outcome_calibration
    historical_artifact_patch: no
    scoring_or_validation_claim: no
    provenance_anchor_status: filesystem_hashes_only_until_git_commit
```

## JSG-08 Receipt

```yaml
jsg_08_reveal_calibration_receipt:
  receipt_status: qualitative_outcome_calibration
  case_id: canoo-walmart
  receipt_artifact: docs/research/judgment-spine/cases/canoo-walmart/jsg_08_reveal_calibration_receipt_v0.md
  prior_calibration_artifact: docs/research/judgment-spine/cases/canoo-walmart/outcome_calibration_v0.md
  provenance_anchor_status: filesystem_hashes_only_until_git_commit
  sealed_blind_output:
    artifact: docs/research/judgment-spine/cases/canoo-walmart/blind_judgments_v0.md
    hash_or_seal_reference: 2DF41433DCFACB31832CD51E65EC424888B7EB8955115D6949A35E8C7F2E8225
    sealed_before_reveal: yes
    cleanliness_caveat: user_supplied_not_independently_verified
    execution_quality_gap: jsg_04_and_jsg_06_not_cleared_no_independent_clean_isolation_or_harness_run_proof
  reveal_event:
    reveal_sequence_or_timestamp: >
      After the blind judgment and pre-reveal comparison were recorded, the
      facilitator ledger preserved actual public action, agreement terms, and
      later supplier outcome for reveal use.
    reveal_operator_or_source: docs/research/judgment-spine/cases/canoo-walmart/facilitator_ledger_v0.md
    material_revealed:
      - Walmart publicly announced a definitive agreement to purchase 4,500 Canoo electric delivery vehicles, with an option to purchase up to 10,000 units.
      - Canoo's Form 8-K described acceptance and performance criteria, termination rights, Amazon-related restrictions, and a warrant issued to Walmart.
      - Canoo later announced a voluntary Chapter 7 bankruptcy filing and immediate cessation of operations.
    reveal_source_refs:
      - docs/research/judgment-spine/cases/canoo-walmart/facilitator_ledger_v0.md: 6356C45D8E9B75732DB3D146EABFFCE4AD2775BCDD23D0205E26A46222FCE739
      - docs/research/judgment-spine/cases/canoo-walmart/reveal_readout_v0.md: 927DB2F16D3D9DF9EBB9DF20F6A35F00659C7C671EEC8ADAF4104BD7535C3A7E
  calibration_frame:
    selected_frame: combined_decision_quality_alignment
    frame_declared_before_interpretive_reveal_use: yes
    axes:
      - actual_action_alignment
      - later_outcome_alignment
      - decision_quality_under_uncertainty
    rejected_frames:
      - actual_action_alignment_only
      - later_outcome_alignment_only
      - single_winner_score
  comparison_inputs:
    contestant_output_refs:
      - docs/research/judgment-spine/cases/canoo-walmart/blind_judgments_v0.md: 2DF41433DCFACB31832CD51E65EC424888B7EB8955115D6949A35E8C7F2E8225
    owner_or_baseline_judgment_refs:
      - docs/research/judgment-spine/cases/canoo-walmart/owner_context_judgments_v0.md: A12BDC0416FC41502AB0B46B70338FF40FF118008D5D808C5E91BDD265E3B2E8
      - docs/research/judgment-spine/cases/canoo-walmart/pre_reveal_judgment_comparison_v0.md: 2AD850D94A29438D54491AA5EE72D8D79332E04F6C78E03BF960CF28BEEAEE80
    outcome_or_reference_refs:
      - docs/research/judgment-spine/cases/canoo-walmart/facilitator_ledger_v0.md: 6356C45D8E9B75732DB3D146EABFFCE4AD2775BCDD23D0205E26A46222FCE739
      - docs/research/judgment-spine/cases/canoo-walmart/reveal_readout_v0.md: 927DB2F16D3D9DF9EBB9DF20F6A35F00659C7C671EEC8ADAF4104BD7535C3A7E
      - docs/research/judgment-spine/cases/canoo-walmart/outcome_calibration_v0.md: 8E5766B11F80D716ACFB376E8227A9C610BBB906949AF65C9C1791A070C0A2F0
      - docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_reveal_readout_calibration_gate_adversarial_artifact_review_v0.md: 31362147A8557C0698A23A9D902AA5FFC71D8B973813F89DF9157D38ED0980EE
  scoring_relationship:
    jsg_07_scoring_result: not_scored
    score_use: none_qualitative_only
    calibration_changes_score: no
  missing_evidence:
    - "JSG-04 not cleared: no independent clean-execution proof for the user-supplied blind LLM judgment"
    - "JSG-06 not cleared: no clean isolation result alongside the sealed blind judgment hash"
    - clean harness-format model run receipt
    - JSG-07 scoring result
    - score-ready fixture admission
    - Walmart fleet deployment volume
    - Walmart unit acceptance volume
    - route uptime or route-level performance
    - operational harm, operational gain, or delivered-unit economics
    - whether Walmart exercised termination rights
    - whether Walmart had deposits, prepayments, or other financial exposure outstanding at bankruptcy
    - whether the protective terms worked in practice
  failure_events:
    - none recorded as reveal/calibration contamination in the loaded artifacts
    - "JSG-04 not cleared: no clean isolation proof for the user-supplied blind judgment"
    - "JSG-06 not cleared: no clean isolation result alongside the sealed blind judgment hash"
    - stronger claims remain blocked by the missing evidence above
  ladder_closeout_note: >
    This receipt does not set a JSG-09 claim classification or JSG-10 closeout
    state. A later classification route must map this qualitative-only receipt
    to the evidence ladder vocabulary before making any closeout claim.
  claim_cap: qualitative_case_learning_or_product_learning_context_only
  non_claims:
    - not validation
    - not readiness
    - not blind-use readiness
    - not buyer proof
    - not fixture admission
    - not scoring authorization
    - not model execution
    - not model performance proof
    - not completed judgment-quality evidence
    - not JSG-09 claim classification clearance
    - not JSG-10 closeout clearance
```

## Classification Rationale

The Canoo/Walmart case has more than a reveal readout because
`outcome_calibration_v0.md` declares a calibration frame, compares the sealed
blind LLM and owner-assisted judgments against reveal/outcome material, names
missing evidence, and caps the result as qualitative-only.

The case does not reach `score_linked_outcome_calibration` because no JSG-07
scoring result is present and the outcome calibration explicitly records
`score_status: not_scored`.

The case does not reach completed judgment-quality evidence because current
materials do not prove independent blind cleanliness, clean no-tools execution,
a clean harness-format model run, a JSG-07 score, score-ready fixture admission,
JSG-09 claim classification clearance, JSG-10 closeout clearance, or the
Walmart-specific operational evidence needed to test protective-term
effectiveness.

The exact evidence-ladder closeout state is intentionally not set here. This
receipt is a JSG-08 case-specific receipt, not a JSG-09 claim classification or
JSG-10 closeout artifact. A later classification must name the closeout state
from the ladder and preserve this receipt's qualitative-only cap.

## Claim Cap

Use this receipt as qualitative case-learning or product-learning context only.
It can help a future operator avoid confusing action alignment, later-outcome
alignment, and decision quality under uncertainty. It cannot be used to promote
the case into proof, readiness, scoring, fixture admission, or judgment-quality
evidence.

## Non-Claims

- This receipt does not validate Judgment Spine.
- This receipt does not create judgment-quality evidence.
- This receipt does not prove a clean blind model run.
- This receipt does not prove clean no-tools isolation.
- This receipt does not prove model performance.
- This receipt does not authorize model execution.
- This receipt does not authorize scoring.
- This receipt does not admit a fixture.
- This receipt does not prove blind-use readiness.
- This receipt does not create buyer proof.
- This receipt does not create product readiness.
- This receipt does not clear JSG-09 or JSG-10.
- This receipt does not change any sealed output, score, case artifact, source
  receipt, or product doctrine.
