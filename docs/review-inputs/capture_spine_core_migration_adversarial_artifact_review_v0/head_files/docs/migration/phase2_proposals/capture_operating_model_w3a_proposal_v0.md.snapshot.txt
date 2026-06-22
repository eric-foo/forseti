```yaml
retrieval_header_version: 1
artifact_role: Orca migration note
scope: >
  Phase-2 W3a proposal for the capture/operating_model area (orca/product/spines/capture/core/operating_model/):
  bloat/deletion candidates with full deletion-evidence records and ontology/doc-term findings against the SSOT.
use_when:
  - Owner adjudicating Phase-2 deletion candidates for the capture operating-model sub-directory.
  - Reviewing ontology/doc-term drift findings for capture/operating_model files before a Phase-3 ratchet.
authority_boundary: retrieval_only
open_next:
  - docs/migration/orca_second_pass_consolidation_plan_v0.md
stale_if:
  - Any capture/operating_model file is moved, renamed, or deleted after this proposal is written (inbound ref counts change).
  - v2 or later supersedes the deletion-evidence doctrine or check_deletion_evidence.py GOVERNED_ROOTS.
```

# Phase-2 W3a Proposal — capture/operating_model

## Summary

Files scanned: 35 (all `.md`)
Deletion candidates: 2 high / 0 medium / 0 low
Ontology findings: 4

---

## A. Deletion candidates

### Candidate 1 — `data_capture_harness_operating_model_architecture_v0.md`

```yaml
targets:
  - orca/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v0.md
evidence:
  reverse_ref_check: |
    Inbound refs found (grep over orca/product/, docs/, .agents/):

    LIVE architectural inbound refs that still name this path (not migration-record-only):
      orca/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v1.md:15
        open_next lists v0 path
      orca/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v1.md:37,91,413
        prose references comparing v0 evidence-mode to v1; documents divergence; still says "prior proposed architecture"
      orca/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v2.md:17,61,82
        open_next lists v0; source ledger entry cites v0 as "Safer framing to import"; prose names v0 v-delta
      docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_v0.md:15,82,116
        open_next lists v0; source ledger hash-matches v0; this review directly reviewed v0
      docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_independent_adversarial_review_v0.md:75,121
        source ledger hash-matches v0 for targeted comparison
      docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_narrow_adversarial_review_v0.md:78
        source ledger cites v0 as "Imported safer framing — confirms v2 preserves second-operator-as-control-surface"
      docs/prompts/reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_prompt_v0.md:14,32,51,97,136,226,246
        review prompt loads v0 as review target; hashes recorded
      docs/prompts/reviews/data_capture_harness_operating_model_architecture_v2_independent_adversarial_review_prompt_v0.md:104,147,155
        source hash table captures v0; prompt loads it as a comparison artifact
      docs/prompts/product-planning/data_capture_harness_operating_model_architecture_prompt_v0.md:29,208,216,488
        planning prompt names v0 as output destination and collision check target
      docs/prompts/wrappers/data_capture_harness_operating_model_architecture_gpt55_wrapper_v0.md:34,93
        wrapper names v0 as target durable artifact
      docs/prompts/reviews/data_capture_harness_operating_model_architecture_prompt_adversarial_review_v0.md:209
        closeout contract names v0 as write path
      docs/migration/capture_spine_source_capture_migration_inventory_v0.md:62
        inventory entry references v0
      docs/migration/spine_first_target_move_table_v0.md:146
        move-table entry: "v0/v1 superseded — archive disposition is an owner question"
      docs/migration/repo_structure_spine_first_v0/moved_paths_index.md:91
        path mapping record (migration provenance)
      docs/migration/repo_structure_phase2_consolidation_v0/reference_inventory.md:648
        inventory entry; docs/migration/repo_structure_phase2_consolidation_v0/moved_paths_index.md:47

    STATUS: NOT safe to remove without handling the live review artifacts, prompts, and v1/v2 cross-refs.
    The spine_first_target_move_table_v0.md already flags "archive disposition is an owner question" for
    this file. The live refs are primarily historical cross-comparison and evidence-chain artifacts
    (review prompts, review outputs, v1/v2 prose), not active routing surfaces. The v0 text is entirely
    subsumed by v2 (which documents what it kept from v0 and why). None of the live refs would break
    functionally if v0 were deleted — they record historical provenance. However, the review outputs and
    prompts carry hashes to v0 content; deletion severs those hash anchors. Owner must decide whether
    provenance-by-hash is considered a "ref to handle" or a resolved historical trace.

    Conservative call: 9+ live refs across review artifacts and prompts. Refs are historical/comparative,
    not operational routing. Owner adjudication required before deletion.

  successor: orca/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v2.md

  semantic_delta: |
    v0 proposed a "Contract-pinned obligation-discharge operating envelope" (AO-2) under plain_model_local_fallback
    evidence mode. v2 is a v0/v1 hybrid: it inherits v0's safer second-operator-as-control-surface framing
    (the primary unique contribution of v0), absorbs all v0 session-lifecycle and obligation-state content,
    and explicitly documents what it kept from v0 vs v1. The adversarial review of v0+v1 found v0's safer
    second-operator framing superior to v1's refusal-authority charter (AR-01); v2 absorbed that fix. v2's
    source ledger and hybridization-decision table record every v0 element retained. Nothing is lost
    uniquely from v0 that is not already in v2, but the historical "proposed, then superseded" trail is
    the sole remaining value. v0 does not contain unique content not preserved in v2.

  rollback: git revert <executing merge sha>
```

**confidence:** high

**rationale:** superseded-by-v2. v0 is status `PROPOSED_ARCHITECTURE_V0`; v2 is status `PROPOSED_ARCHITECTURE_V2` with owner acceptance recorded at `data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md`. v2 explicitly absorbs v0's unique framing contribution. All live refs are historical/comparative provenance, not active routing surfaces. The move-table already classified this as "owner question" pending disposition.

---

### Candidate 2 — `data_capture_harness_operating_model_architecture_v1.md`

```yaml
targets:
  - orca/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v1.md
evidence:
  reverse_ref_check: |
    Inbound refs found (grep over orca/product/, docs/, .agents/):

    LIVE architectural inbound refs that still name this path (not migration-record-only):
      orca/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v2.md:16,62,81
        open_next lists v1; source ledger cites v1 as "Hybrid base — v1 strengths"; prose names v1 as base
      docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_v0.md:14,83,117
        open_next lists v1; source ledger hash-matches v1; this review directly reviewed v1
      docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_independent_adversarial_review_v0.md:76,122
        source ledger hash-matches v1 for targeted comparison (CPOE-ARC reviewer charter; refusal verbs; "locked now")
      docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_narrow_adversarial_review_v0.md:77
        source ledger cites v1 as "Base artifact for comparison — confirms v2 removed v1's review-first/refusal-heavy terms"
      docs/prompts/reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_prompt_v0.md:13,34,52,137
        review prompt loads v1 as primary review target; hashes recorded
      docs/prompts/reviews/data_capture_harness_operating_model_architecture_v2_independent_adversarial_review_prompt_v0.md:105,156
        source hash table captures v1; prompt loads it as a comparison artifact
      docs/migration/repo_structure_spine_first_v0/moved_paths_index.md:92
        path mapping record (migration provenance)
      docs/migration/repo_structure_phase2_consolidation_v0/reference_inventory.md:649
        inventory entry; docs/migration/repo_structure_phase2_consolidation_v0/moved_paths_index.md:48
      docs/migration/spine_first_target_move_table_v0.md:146
        move-table entry: "v0/v1 superseded — archive disposition is an owner question"

    STATUS: Same pattern as v0. NOT safe to remove without handling the live review artifacts and prompts.
    All live non-migration refs are historical/comparative provenance in review outputs and prompts.
    v2 explicitly documents what it took from v1 (the hybrid base) and what it rejected (CPOE-ARC
    reviewer-checkpoint framing, "locked now" wording). Deletion severs hash anchors in review
    artifacts but does not break any active routing surface.

    Conservative call: 8+ live refs across review artifacts and prompts. Same owner-question status
    as v0 per spine_first_target_move_table_v0.md:146.

  successor: orca/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v2.md

  semantic_delta: |
    v1 proposed "Contract-Pinned Operating Envelope with Adversarial Reviewer Checkpoint (CPOE-ARC)"
    under delegated_three_subagents evidence mode. v2 uses v1 as its explicit hybrid base and absorbs:
    all per-slice safeguards (Obligations 10/11/12/15), the known failure-mode counterweights (20 named
    failure modes including F-STATE-COLLAPSE, F-LEAK-ECR, F-PER-SLICE-FLATTEN), and the obligation-discharge
    visibility commitment. v2 rejects v1's CPOE-ARC label, refusal-authority charter, and "locked now"
    wording (AR-01/AR-02/AR-03 from the adversarial review). The hybridization-decision table in v2
    documents each v1 element retained or replaced. v1 does not contain unique content not already
    captured in v2's hybridization record. The sole remaining value of v1 is the historical
    evidence-mode trail (delegated_three_subagents receipt and subagent source-readiness receipts).

  rollback: git revert <executing merge sha>
```

**confidence:** high

**rationale:** superseded-by-v2. v1 is status `PROPOSED_ARCHITECTURE_V0` (as stated in v1 itself); v2 is the owner-accepted architecture. v2 explicitly documents what it absorbed from v1 and what it rejected. All live refs are historical/comparative provenance, not active routing surfaces. Move-table already classifies v1 as "owner question."

---

### Non-candidates (why the other 33 files are retained)

All other 33 files in `orca/product/spines/capture/core/operating_model/` carry either:

- live inbound refs from active decisions, contracts, or implementation artifacts (confirmed by grep); or
- unique content not preserved in any successor (pressure-test sessions, synthesizing artifacts, scoping records, patch plans, future-exploration backlog, projection-storage architecture); or
- are active decisions with downstream dependents (baseline decision, v2 acceptance decision, lane product thesis, commissioning plan, execution authorization, post-batch patch plan, source-observability scoping).

Notable checks:

- `core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`: 20+ live inbound refs from decisions, contracts, review prompts, and the cleaning-spine foundation. Retained.
- `core_spine_v0_data_capture_context_preservation_note_v0.md`: 20+ live inbound refs including the cleaning-spine foundation, multiple review prompts, and fixture sessions. Retained.
- `core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md`: 14+ live inbound refs including the obligation-baseline decision and adversarial review. Retained.
- `core_spine_v0_data_capture_spine_remaining_fixture_plan_v0.md`: live inbound refs from 5+ fixture sessions and the full-fixture synthesis adversarial review. Retained.
- `orca_capture_projection_storage_spine_architecture_v0.md`: live inbound refs from `orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md`, the IG capture shape contract, and IG monitoring policy. Status PROPOSED/AWAITING owner adoption. Retained as active proposed architecture with downstream consumers.
- `data_capture_spine_post_batch_patch_plan_v0.md`: live inbound refs from decisions and review prompts. Retained.
- `data_capture_spine_source_observability_requirements_scoping_v0.md`: live inbound refs from 3 decisions. Retained.
- `data_capture_spine_future_exploration_lanes_v0.md`: live inbound refs from wind_caller_calibration_carveout_v0.md, orca_repo_map_v0.md, and a deep-thinking prompt. Retained.
- Pressure-test session files (slot1, slot2, slot3 variants, reddit batches, wso, interim evidence, combined handoff, slot3 subbatch control, closeout synthesis, all-slot synthesis, post-slot3 recapture delta): all carry live inbound refs from decisions or synthesizing artifacts. Retained.
- `data_capture_harness_product_goal_direction_signal_decision_v0.md`, `data_capture_obligation_baseline_decision_v0.md`, `data_capture_harness_operating_model_architecture_v2.md`, `data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md`, `data_capture_spine_lane_product_thesis_v0.md`, `data_capture_spine_pressure_test_commissioning_plan_v0.md`, `data_capture_spine_pressure_test_execution_authorization_v0.md`, `data_capture_spine_pressure_test_slot3_reddit_subbatch_control_note_v0.md`: active decisions and session controls. Retained.

---

## B. Ontology / doc-term findings

Compared `orca/product/spines/capture/core/operating_model/` vocabulary against `orca/product/spines/foundation/ontology/ontology.yaml` (SSOT). Canonical types checked: `Vertical`, `Brand`, `Product`, `Venue`, `WindCaller`, `Call`, `Observation`, `TrendVector`, `DecisionEvent`, `Reading`, `Memo`, `Case`, `Outcome`, `CapturePacket`, `EvidenceUnit`, `Buyer`, `Org`. Runtime/storage aliases checked: `SourceCapturePacket`, `FacilitatorLedger`, `CaseReport`. Distinctive head nouns from multi-hump canonical types: `Caller`, `Event`, `Packet`, `Unit`, `Vector`.

**Finding 1 — `SourceCapturePacket` appears as a CamelCase type token in `orca_capture_projection_storage_spine_architecture_v0.md`**

- Term: `SourceCapturePacket`
- File:line: `orca_capture_projection_storage_spine_architecture_v0.md:153` ("reader → SourceCapturePacket + NEW typed Observation fields")
- SSOT status: KNOWN. `SourceCapturePacket` is the recorded storage alias / name_alias for the `CapturePacket` ontology type (`runtime_bindings.CapturePacket.name_alias: SourceCapturePacket`). Usage here is in a prose architecture diagram naming the runtime model class. This is a correctly-used alias, not drift.
- Proposed fix: None. Usage is correct per the SSOT alias record.

**Finding 2 — `DecisionEvent` appears as an ontology reference in `orca_capture_projection_storage_spine_architecture_v0.md`**

- Term: `DecisionEvent`
- File:line: `orca_capture_projection_storage_spine_architecture_v0.md:162,181` ("only an ACTED-ON decision writes back (ontology DecisionEvent)"; "an acted-on decision → ontology `DecisionEvent` (adapter, not hard type-bind; the ontology is AWAITING_DISPATCH / HIGH lock-in)")
- SSOT status: KNOWN. `DecisionEvent` is ADOPTED in the SSOT (`decision` namespace, status: adopted). The usage correctly qualifies it as an adapter reference with a lock-in caveat ("AWAITING_DISPATCH / HIGH lock-in" — noting the deferred adoption). The architecture explicitly avoids hard type-binding. Usage is appropriately qualified.
- Proposed fix: None. The lock-in caveat is accurate for the current SSOT state; `DecisionEvent` is adopted but the ontology-to-runtime binding for it is not in the `runtime_bindings` block, consistent with it being SSOT-only.

**Finding 3 — `SourceCaptureSlice` appears as an engineering identifier in `orca_capture_projection_storage_spine_architecture_v0.md`**

- Term: `SourceCaptureSlice`
- File:line: `orca_capture_projection_storage_spine_architecture_v0.md:291,343` — naming the runtime class `orca-harness/source_capture/models.py:SourceCaptureSlice`
- SSOT status: NOT in the SSOT as a type or alias. Head noun "Slice" is not an ontology head noun; this is a CamelCase engineering identifier whose head noun falls outside the ontology's distinctive head-noun set (`Caller`, `Event`, `Packet`, `Unit`, `Vector`). The doc-term checker's `ignore` path applies (non-ontology head noun). Not a drift finding by the checker's own rules.
- Proposed fix: None. `SourceCaptureSlice` is a runtime model class identifier, not an ontology-shaped coinage. No action needed.

**Finding 4 — `VisibleFact` appears repeatedly in `orca_capture_projection_storage_spine_architecture_v0.md`**

- Term: `VisibleFact`
- File:line: `orca_capture_projection_storage_spine_architecture_v0.md:64,79,93,109,118,120,122,123,251,288,316,343` — naming the runtime enum `orca-harness/source_capture/models.py:VisibleFact`
- SSOT status: NOT in the SSOT as a type or alias. Head noun "Fact" is not an ontology head noun. The doc-term checker's `ignore` path applies (non-ontology head noun). Not a drift finding by the checker's own rules.
- Proposed fix: None. `VisibleFact` is a runtime enum identifier, not an ontology-shaped coinage. No action needed.

**Overall ontology status:** No SSOT violations, no deprecated/aliased term misuse, no new-term candidates requiring SSOT promotion found in the 35 scanned files. The two live CamelCase ontology references (`SourceCapturePacket`, `DecisionEvent`) are correctly used per the SSOT. The two engineering identifiers (`SourceCaptureSlice`, `VisibleFact`) fall outside the checker's ontology-shaped scope. Area is effectively clean on ontology/doc-term drift.
