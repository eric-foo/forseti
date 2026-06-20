```yaml
retrieval_header_version: 1
artifact_role: Orca migration note
scope: >
  Phase-2 W3a proposal for the shared area (orca/product/shared/): bloat/deletion candidates with full deletion-evidence records and ontology/doc-term findings against the SSOT.
use_when:
  - Owner adjudicating Phase-2 deletion candidates for the shared area (engagement_registry/, projection_doctrine/).
  - Reviewing ontology/doc-term drift findings for shared-area files before a Phase-3 ratchet.
authority_boundary: retrieval_only
open_next:
  - docs/migration/orca_second_pass_consolidation_plan_v0.md
stale_if:
  - Any shared-area file is moved, renamed, or deleted after this proposal is written (inbound ref counts change).
  - The owner makes an R2 re-home decision for projection_doctrine/ or engagement_registry/ (supersedes this proposal's successors).
```

# Phase-2 W3a Proposal — shared

## Summary

Files scanned: 2 (both `.md`)
Deletion candidates: 0 high / 0 medium / 0 low
Ontology findings: 1 known-alias usage (clean; no new-term candidates)

## A. Deletion candidates

None — area is lean.

Both files in `orca/product/shared/` carry deep, active inbound reference webs from multiple governed spines and live surfaces. Neither is bloat; both are explicitly flagged in existing decisions as pending their own R2 re-home decisions (not deletion). Full evidence follows.

---

### File 1: `orca/product/shared/engagement_registry/engagement_logic_registry_v0.md`

**Reverse-ref check (grep of orca/product/, docs/, .agents/ for `engagement_logic_registry`):**

Inbound references found — NOT safe to delete without handling:

- `docs/migration/spine_first_target_move_table_v0.md:259` — migration provenance (historical reference-model-B)
- `docs/migration/repo_structure_spine_first_v0/moved_paths_index.md:146` — migration provenance
- `docs/migration/repo_structure_phase2_consolidation_v0/runbook.md:28` — migration runbook reference
- `docs/workflows/orca_repo_map_v0.md:541` — live repo map entry (surface reference)
- `docs/workflows/orca_repo_map_v0.md:731` — live repo map listing
- `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md:136` — decision record names it as pending its own R2 re-home
- `docs/prompts/reviews/core_spine_v0_proof_packet_preparation_adversarial_review_gpt55_prompt_v0.md:75` — prompt source-pack reference
- `orca/product/spines/foundation/product_contract/core_spine_v0_proof_protocol_v0.md:6,57` — live source-basis and proof protocol dependency
- `orca/product/spines/foundation/product_contract/core_spine_v0_proof_packet_preflight_v0.md:10` — live preflight dependency
- `orca/product/spines/foundation/product_contract/core_spine_v0_proof_input_selection_v0.md:6` — live source-basis
- `orca/product/spines/foundation/product_contract/core_spine_v0_product_contract.md:6,60` — live source-basis and signal-use table entry
- `orca/product/spines/foundation/product_contract/core_spine_v0_information_production_foundation_v0.md:6` — live source-basis
- `orca/product/case_families/product_learning/other_verticals/core_spine_v0_first_proof_packet_preparation_v0.md` — live case-family dependency
- `orca/product/case_families/product_learning/other_verticals/core_spine_v0_first_proof_run_bt204_backtest_slice_v0.md:34` — live proof-run dependency
- `orca/product/case_families/product_learning/other_verticals/core_spine_v0_first_proof_run_charter_v0.md:17` — live charter dependency
- `orca/product/case_families/product_learning/other_verticals/core_spine_v0_first_proof_run_locks_v0.md:46` — live locks dependency
- `orca/product/case_families/product_learning/other_verticals/core_spine_v0_heavyweight_proof_case_discovery_charter_v0.md:39` — live discovery dependency
- `orca/product/case_families/product_learning/other_verticals/core_spine_v0_heavyweight_proof_case_discovery_results_v0.md:43` — live discovery dependency
- `orca/product/case_families/product_learning/other_verticals/core_spine_v0_proof_case_selection_brief_v0.md:38` — live case-selection dependency

**Verdict: NOT a deletion candidate.** 19+ inbound references across live product_contract, case_families, docs surfaces. The file is actively load-bearing as the signal-use classification rubric for the Core Spine proof protocol. `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md:136,152` explicitly states it is "pending its own R2 decision" (re-home to judgment/Core signal-use, not deletion). Status is `PROPOSED_FREEZE` — active, not superseded.

---

### File 2: `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`

**Reverse-ref check (grep of orca/product/, docs/, .agents/ for `projection_doctrine`):**

Inbound references found — NOT safe to delete without handling:

- `.agents/workflow-overlay/artifact-folders.md:374` — live overlay: names path as governed artifact folder
- `.agents/workflow-overlay/source-loading.md:384` — live overlay: names path as a source-loading reference
- `docs/workflows/orca_repo_map_v0.md:397` — live repo map entry
- `docs/workflows/data_capture_spine_consolidation_map_v0.md:60` — live consolidation map dependency
- `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md:135,152` — decision record names it as pending its own R2 re-home
- `docs/decisions/orca_spine_first_target_structure_binding_v0.md:76,220` — structural binding reference
- `docs/migration/spine_first_target_move_table_v0.md:258` — migration provenance
- `docs/migration/repo_structure_spine_first_v0/moved_paths_index.md:78` — migration provenance
- `docs/migration/orca_second_pass_consolidation_plan_v0.md:139` — controller worksheet reference
- `docs/migration/data_lake_spine_first_migration_plan_v0.md:138` — migration plan reference
- `docs/review-outputs/adversarial-artifact-reviews/projection_doctrine_v0_vendor_ca_closeout_v0.md:26` — CA closeout names source path
- `docs/prompts/handoffs/cleaning_spine_projection_doctrine_handoff_prompt_v0.md:135,138,230` — live handoff prompt dependency
- `docs/prompts/handoffs/cleaning_spine_foundation_architecture_planning_prompt_v0.md:17,18,195,196` — live prompt dependency
- `docs/prompts/handoffs/cleaning_spine_foundation_architecture_planning_prompt_v1.md:17,18,27,206,207` — live prompt dependency (v1)
- `orca/product/README.md:23` — live README entry
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md:15` — live cleaning spine dependency
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md:16,29,77,93,396,397` — live cleaning spine foundation (6 refs)
- `orca/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_playbook_v0.md:17,223,235` — live playbook dependency
- `orca/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_contract_v0.md:17,69,244` — live contract dependency
- `orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md:21,70,267,278` — live packet schema dependency
- `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md:22,212` — live data lake map dependency
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md:18` — live lake contract dependency
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md:19` — live lake contract dependency

**Verdict: NOT a deletion candidate.** 23+ inbound references across live overlay files, cleaning spine contracts, capture source-family contracts, data lake contracts, active prompts and handoffs. Status is `CANDIDATE_KEPT_BY_VENDOR_CA_FOR_OWNER_CONFIRMATION` — active candidate awaiting owner confirmation, not superseded. `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md:135,152` explicitly states it is "pending its own R2 decision" (re-home to Capture-owned, not deletion).

---

## B. Ontology / doc-term findings

**Scan summary (check_doc_terms.py predicate applied manually):**

### engagement_logic_registry_v0.md

No multi-hump CamelCase tokens found. The file uses only prose vocabulary (no SSOT-shaped coinages). Clean.

### core_spine_v0_projection_doctrine_v0.md

One multi-hump CamelCase token found:

| Token | File:line | Classification | Notes |
| --- | --- | --- | --- |
| `SourceCapturePacket` | `core_spine_v0_projection_doctrine_v0.md:91` | KNOWN — alias for `CapturePacket` (registered in `ontology.yaml` `runtime_bindings.CapturePacket.name_alias`) | Used correctly in pipeline diagram as the runtime storage alias. No fix needed. |

**New-term candidates:** None. No CamelCase token with an ontology head noun (`Caller`, `Event`, `Packet`, `Unit`, `Vector`) appears outside the SSOT-known set.

**Deprecated/aliased terms used incorrectly:** None.

**Overall:** Clean. Both files are either term-free (engagement registry uses prose only) or use only SSOT-registered tokens correctly (projection doctrine uses `SourceCapturePacket` as the accepted storage alias).
