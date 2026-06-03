# Judgment Spine Gate Ownership Map v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Case-agnostic ownership map for Judgment Spine gates needed before stronger proof, scoring, blind-use, fixture, or judgment-quality claims.
use_when:
  - Checking which source owns a Judgment Spine gate before a case tries to claim a stronger tier.
  - Routing a case from source custody and packet construction toward sealed execution, scoring, reveal, calibration, and closeout.
  - Identifying unowned or blocked gates before a future operating-model or case-specific run path.
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine_evidence_ladder_architecture_v0.md
  - docs/product/judgment_quality_promotion_operating_model_v0.md
  - docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md
  - docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - .agents/workflow-overlay/validation-gates.md
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
  - docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md
  - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md
  - docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md
  - docs/research/judgment-spine/harness/v0_14/phase_1_infrastructure_architecture.md
input_hashes:
  AGENTS.md: 5800D6EC863102DC680A6FDB91199337BC8CAC65A4C820FE3F94610B0AFA82A1
  .agents/workflow-overlay/README.md: 40E28238868A423CD43559C1BE5C312E088439E596ECE8AFD25E73835A62A27F
  .agents/workflow-overlay/source-of-truth.md: 7DFBF052A098C0AD77A5598BB6EA4738DA9AD6943D391852DC2E032A173182EF
  .agents/workflow-overlay/source-loading.md: 5CE8772563021F02968C76B9FE34D5E136459EFDF9DC92CF9F74077C59932560
  docs/product/judgment_spine_evidence_ladder_architecture_v0.md: 79F6696DD50BE3FDCB574FD6AED4FE0761C6335029BFDBE39B51F104F4AD16CF
  docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md: ED146BEB5767EFDDA3E979AA798CA5CB044A896421872B02FBDF03615E4E6E07
  docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md: 94988650A7A9DF8AA051BBF0E5526FD6022721440219E7FDE29DBD80F60755F3
  docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md: B06BD6722F76D223E7A122B7F97B967431BDEEE5D4E41AD6DCCEF81903DAC8C5
  .agents/workflow-overlay/validation-gates.md: FD7AE96F481733ED7FA5F1DDE252B7CF6A7C5A9053DAC7317795353F003F520F
  .agents/workflow-overlay/product-proof.md: AD1724202841D616F74494B22E3659D7987CC875BD36BF0F23B12C210E4B19C4
  docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md: 3301224649991811D91B8B5932F0DFF18D3E356CB51979619BDBE3494BC9193C
  docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md: 7862F03D0DA8DB6D845DF47FAA7940D89C2B27C8A27204C41744ECD3AC7B4C61
  docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md: 7291EF5E7C19A3514AE2B0E91D9FDD8917D7C4BFF039726FCD6075E55F73C1A4
  docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md: 0CE6E9584F4F1C4716559A654870AF43EBED3E5D53D3279AB658993B7DE1C2AE
  docs/research/judgment-spine/harness/v0_14/phase_1_infrastructure_architecture.md: 0459C21E7083CD9295290170692BE47A85CBCD24B42B9B0C6E9D7ACF29AC850A
  docs/workflows/orca_repo_map_v0.md: BF5559164431C98C1C6A1DB614B854A99E70FF2C0E63E33D26DDDA5AD3E6802E
branch_or_commit: main @ dd2d06553b4412416b1e37a28b2faaf2b7683d33
input_hash_baseline_note: >
  These input_hashes pin the scoped bundle bytes recomputed during the
  2026-06-03 Judgment authority closeout. Recompute before strict reliance if
  any scoped source changes after that closeout.
downstream_consumers:
  - .agents/workflow-overlay/source-loading.md
  - docs/workflows/orca_repo_map_v0.md
  - docs/product/judgment_quality_promotion_operating_model_v0.md
  - future Judgment Spine case-run planning
stale_if:
  - docs/product/judgment_spine_evidence_ladder_architecture_v0.md changes claim tiers, closeout states, or required receipts.
  - docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md changes Data Capture, Evidence Candidate Record, source identity, captured-signal receipt, or handoff boundary semantics.
  - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md changes source identity, raw-observable fidelity, inspectability, actor/timing/cutoff posture, or categorical handoff obligations.
  - .agents/workflow-overlay/validation-gates.md changes Judgment Spine claim-tier gate requirements.
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md changes clean execution or blind judgment gate semantics.
  - docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md changes probe gate semantics.
  - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md changes packet, admission, source-bytes or inspectable-reference handoff, final pre-decision status, freeze-input, scoring-boundary, or block-don't-repair semantics.
  - docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md changes facilitator-ledger labeling, authorship, disagreement, version-pin, or freeze-hash workflow.
  - docs/research/judgment-spine/harness/v0_14/phase_1_infrastructure_architecture.md changes scoring, mapping-table version, ledger-freeze, evidence-ID, no-LLM-import, report, or deterministic harness requirements.
  - A later accepted operating-model artifact supersedes this gate ownership map.
```

## Source-Loading Surface

Purpose: name the owner status and handoff boundary for each case-agnostic
Judgment Spine gate needed before stronger proof, scoring, blind-use, fixture,
or judgment-quality claims.

Use when: a future case, run, memo, deck, fixture, scoring artifact, or review
needs to know which gate is owned, candidate-owned, unowned, or blocked before
claim promotion.

Do not use for: authorizing a model run, scoring a case, admitting a fixture,
validating Judgment Spine, creating buyer proof, or claiming judgment-quality
evidence.

Authority boundary: if this map conflicts with the evidence ladder, Orca
overlay, harness contract, or a case-specific accepted decision, open the
controlling source and treat this map as stale for that gate.

Recheck recipe: recompute the input hashes above and rerun the source-loading
read pack in `.agents/workflow-overlay/source-loading.md` before strict gate
ownership, readiness, validation, proof, fixture, scoring, or judgment-quality
claims.

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_judgment_spine_gate_ownership_map
  edit_permission: docs-write
  target_scope:
    - docs/product/judgment_spine_gate_ownership_map_v0.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
  dirty_state_checked: yes
  blocked_if_missing: no
  dirty_or_untracked_notes:
    - docs/product/judgment_spine_evidence_ladder_architecture_v0.md is untracked in this worktree.
    - .agents/workflow-overlay/product-proof.md is untracked in this worktree.
    - .agents/workflow-overlay/source-loading.md, .agents/workflow-overlay/validation-gates.md, and docs/workflows/orca_repo_map_v0.md were modified before this map was written.
```

## Owner Status Vocabulary

```yaml
owner_status_values:
  owned:
    meaning: A source-backed owner surface defines the gate, required receipt, and failure effect well enough for a future case to route without inventing ownership.
  candidate_owner:
    meaning: A source-backed surface names the concept, but the exact gate contract or receipt ownership is incomplete.
  unowned:
    meaning: No source-backed owner surface was found in the loaded source pack.
  blocked_owner_decision_required:
    meaning: The gate is required for stronger claims, but current sources do not define a complete owner contract; an owner decision or accepted source patch is required before treating it as owned.
```

## Gate Ownership Map

| Gate ID | Gate | Owner status | Owner surface | Required receipt or artifact | Claim blocked if missing | Handoff boundary | Open owner decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| JSG-01 | Source identity and pre-decision status | owned | `core_spine_v0_data_and_cleaning_spine_boundary_v0.md` and `core_spine_v0_data_capture_spine_obligation_contract_v0.md` for Data Capture/ECR source identity, raw-observable/inspectability, timing, actor, cutoff/archive, and categorical handoff obligations; `packing_to_harness_foundation_interface_architecture_v3.md` for final Judgment-owned `pre_decision_status` | Source identity, inspectable reference or source bytes when required, timing/cutoff posture, and final pre-decision status | Judgment-quality evidence, fixture admission, scoring, clean blind-use readiness | Data Capture/ECR preserve source identity and categorical handoff posture; Judgment/Harness consumes and blocks if missing | none for ownership; case-specific source gaps remain possible |
| JSG-02 | Participant packet freeze | owned | Evidence ladder receipt; product-proof zero-spoiler participant-packet boundary; `packing_to_harness_foundation_interface_architecture_v3.md` | Frozen `participant_packet_hash` with zero-spoiler participant-visible boundary | Clean blind judgment, scoring, fixture admission, judgment-quality evidence | Packing/case artifact authors packet; Harness consumes frozen hash and blocks rather than repairs | none for ownership |
| JSG-03 | Facilitator ledger freeze | owned | Evidence ladder receipt; `band_input_labeling_rubric.md`; `packing_to_harness_foundation_interface_architecture_v3.md` | Frozen `FacilitatorLedger` with `ledger_freeze_hash`, authors, version pins, band inputs, and disagreement trail | Scoring, fixture admission, judgment-quality evidence | Facilitator ledger owns labels and freeze; Harness consumes and verifies | none for ownership |
| JSG-04 | No-tools isolation | owned | `contestant_no_tools_execution_contract_v0.md` | `contestant_execution_isolation` with `isolation_result: proven` and auditable execution provenance | Clean blind-use readiness, scoring, validation, fixture admission, judgment-quality evidence | Execution surface or runner receipt proves isolation; prompt text alone is insufficient | none for ownership |
| JSG-05 | Memorization probe | owned | `memorization_probe_protocol.md` paired with no-tools execution contract | Memorization probe artifact with raw `probe_result`, isolation evidence, and gate interpretation such as `pass_valid` | Contestant-case pair cannot clear model-family gate; clean blind-use readiness remains blocked | Probe protocol owns recognition semantics; no-tools contract owns isolation layer | none for ownership |
| JSG-06 | Sealed blind judgment output | owned | Evidence ladder receipt; product-proof blind-judgment lane; no-tools execution contract blind judgment section | Sealed blind judgment hash plus clean isolation result before reveal exposure | Scoring, calibration, fixture admission, judgment-quality evidence | Execution receipt proves clean run; case record preserves seal before reveal | none for ownership |
| JSG-07 | Scoring result | owned | Evidence ladder receipt; `phase_1_infrastructure_architecture.md`; `packing_to_harness_foundation_interface_architecture_v3.md` | Scoring result with scorer/mapping/version hashes and required frozen inputs | Fixture admission, judgment-quality evidence, score-based calibration claims | Harness owns deterministic scoring; it must not author labels or repair missing inputs | none for ownership |
| JSG-08 | Reveal or calibration record | owned | `judgment_spine_reveal_calibration_owner_contract_v0.md`, with product-proof zero-spoiler/outcome-calibration lane boundaries and case-specific reveal/calibration artifacts | `jsg_08_reveal_calibration_receipt` with receipt status, sealed output reference, reveal event, calibration frame, comparison inputs, scoring relationship, missing evidence, claim cap, and non-claims | Completed judgment-quality evidence, calibration-based scoring claims, fixture-readiness claims when the case-specific receipt is absent, reveal-only, qualitative-only, or contaminated | Owner contract defines receipt shape; case artifacts own case-specific reveal facts and calibration; JSG-07 still owns scoring results | none for ownership; case-specific receipt gaps remain possible |
| JSG-09 | Claim classification | owned | Evidence ladder `judgment_spine_claim_classification`; validation gate; product-proof boundary | Inline classification or durable co-referenced classification record with source-quality state, execution-quality state, `closeout_state`, claim cap, missing gate, and receipt artifact or gap | Proof, readiness, validation, fixture admission, scoring, blind-use, or judgment-quality claims above the weakest cleared gate | Classified artifact must embed or co-reference the classification | none for ownership |
| JSG-10 | Closeout state | owned | Evidence ladder closeout-state vocabulary; validation gate | Named `closeout_state` from the ladder vocabulary, capped by weakest-cleared gate | Any stronger claim than the named closeout state permits | Evidence ladder owns vocabulary; classified artifact records state | none for ownership |

## JSG-08 Owner Detail

`JSG-08` is promoted to `owned` for owner-surface routing only.

`judgment_spine_reveal_calibration_owner_contract_v0.md` now defines the
case-agnostic receipt shape, satisfaction states, reveal-readout boundary,
calibration-frame boundary, scoring relationship, and claim caps for
`outcome_reveal_or_calibration_record`.

This does not clear the gate for any case. A case-specific artifact must still
record whether its receipt is `absent`, `reveal_readout_only`,
`qualitative_outcome_calibration`, `score_linked_outcome_calibration`, or
`contaminated_or_invalid`. Reveal-only material remains case-learning or
product-learning context and cannot support completed judgment-quality evidence,
scoring readiness, fixture admission, or validation.

`JSG-09` and `JSG-10` are owned for classification and closeout recording only.
They cannot record `completed_judgment_quality_evidence` unless the
case-specific `JSG-08` receipt has a status strong enough for the claim and all
other required gates also clear. The classification or closeout must name the
missing or insufficient `JSG-08` receipt or use a lower ladder closeout state.

## Non-Claims

- This map does not validate Judgment Spine.
- This map does not create judgment-quality evidence.
- This map does not authorize model execution.
- This map does not authorize scoring.
- This map does not admit a fixture.
- This map does not prove blind-use readiness.
- This map does not create buyer proof.
- This map does not create product readiness.
- This map does not clear `JSG-08` for any case-specific artifact.
- This map does not authorize implementation, runtime design, tests,
  deployment, commits, pushes, or PRs.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Judgment Spine gate promotion now has a case-agnostic ownership map that
    distinguishes owned, candidate-owned, unowned, and blocked-owner-decision
    gates before stronger proof, scoring, fixture, blind-use, or
    judgment-quality claims.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
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
    - docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md
    - docs/product/judgment_spine_evidence_ladder_architecture_v0.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/product-proof.md
    - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
    - docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md
    - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md
    - docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md
    - docs/research/judgment-spine/harness/v0_14/phase_1_infrastructure_architecture.md
    - docs/research/judgment-spine/README.md
    - docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md
  intentionally_not_updated:
    - path: docs/product/judgment_quality_promotion_operating_model_v0.md
      reason: >
        Deferred by owner decision. This checkpoint maps gate ownership and
        leaves the later operating-model spine uncreated.
    - path: docs/product/judgment_spine_evidence_ladder_architecture_v0.md
      reason: >
        The ladder already owns claim tiers, closeout states, and receipt
        minima. Source-loading and repo-map navigation now route ownership
        questions to this map without changing ladder vocabulary.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The existing Judgment Spine claim-tier gate already requires claim tier
        and closeout state before stronger claims. This map adds ownership
        routing, not a new overlay validation rule.
    - path: Daimler-specific case, run, prompt, source, and decision artifacts
      reason: >
        This is a case-agnostic ownership map. Applying it to Daimler requires
        a separate case-specific classification or run receipt.
  stale_language_search: >
    rg -n "blocked_owner_decision_required|owner_status|judgment-quality|fixture admission|scoring readiness|validation|buyer proof|readiness|model execution|Daimler"
    docs/product/judgment_spine_gate_ownership_map_v0.md
    docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md
    .agents/workflow-overlay/source-loading.md
    .agents/workflow-overlay/source-of-truth.md
    docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed on 2026-06-03 after the DCP primary/related trigger grammar patch
    and AR-01 through AR-04 minor review patch. Hits in this map are expected
    gate rows, owner-status vocabulary, the JSG-08 owner-detail section,
    JSG-09/JSG-10 dependency note, related_triggers, non-claims, and
    propagation references. Hits in the owner contract are expected
    receipt-shape, satisfaction-state, claim-cap, non-claim, and propagation
    references. Hits in source-loading, source-of-truth, and repo-map are
    expected navigation, source-list, or DCP grammar references. No hit
    converted the map or navigation surfaces into validation, readiness, buyer
    proof, fixture admission, scoring authorization, model-execution
    authorization, or judgment-quality evidence.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not fixture admission
    - not scoring authorization
    - not judgment-quality proof
    - not implementation authorization
```
