# Foundation Layer Migration Inventory v0

```yaml
retrieval_header_version: 1
artifact_role: Migration record
scope: Inventory-only marking artifact for the Foundation Layer, formerly named Core Spine, before any spine-first repository migration.
use_when:
  - Deciding what belongs to Foundation before moving or renaming Core Spine surfaces.
  - Checking which legacy core_spine names and pending branch changes must be accounted for.
  - Preventing generated, historical, runtime, or downstream-spine surfaces from being moved too early.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/artifact-folders.md
  - docs/workflows/orca_repo_map_v0.md
  - docs/product/core_spine/core_spine_v0_product_contract.md
  - docs/product/core_spine/core_spine_v0_information_production_foundation_v0.md
  - docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
stale_if:
  - PR #242 or branch codex/foundation-rename lands, is closed, or is superseded.
  - docs/product/foundation/ appears on the current branch.
  - docs/product/core_spine/ is moved, deleted, or partially migrated.
  - core_spine_v0_* artifact IDs are renamed.
  - repo-structure.yaml changes product_lanes or docs/product lane placement.
```

## Purpose

This is an inventory-only migration marking artifact. It identifies the current Foundation/Core surfaces and migration dependencies that must be accounted for before any spine-first repository migration.

It treats Foundation as a shared judgment/product substrate, not as a normal downstream spine. The current repository still uses `Core Spine`, `core_spine`, and `core_spine_v0_*` naming in many places. This artifact marks those surfaces; it does not move, rename, validate, approve, or promote them.

## Start Preflight Receipt

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus targeted Foundation/Core scans
  edit_permission: docs-write
  target_scope: inventory-only migration record under docs/migration/
  dirty_state_checked: yes
  blocked_if_missing: none for inventory; PR #242 verified by gh pr view during this run
```

Observed branch/worktree state:

- Inventory branch/worktree: `codex/foundation-layer-migration-inventory`.
- Current base commit observed before writing: `b139fa9f`.
- Current branch check found `docs/product/foundation/` absent.
- Current branch check found `docs/product/core_spine/` present.
- Current branch check found local branch `codex/foundation-rename` at `56a832c0`.
- `git merge-base --is-ancestor codex/foundation-rename HEAD` exited `1`, so the current inventory branch does not contain the pending rename branch.
- `git merge-base --is-ancestor HEAD codex/foundation-rename` exited `0`, so the pending rename branch appears to include this branch's starting base.
- Repository text search found no local `PR #242`, `#242`, or `foundation-rename` mention under `docs`, `.agents`, or `repo-structure.yaml`.
- `gh pr view 242` verified PR #242 as open, draft, base `main`, head `codex/foundation-rename`, merge state `UNSTABLE`, not merged (`mergedAt: null`), URL `https://github.com/eric-foo/orca/pull/242`.

## Current Surfaces Found

### Current Foundation Home

Current branch:

- `docs/product/core_spine/` exists.
- `docs/product/foundation/` does not exist.
- `docs/product/core_spine_v0_projection_doctrine_v0.md` exists at the `docs/product/` root, not under `docs/product/core_spine/`.

Pending branch dependency:

- `codex/foundation-rename` contains `docs/migration/foundation_layer_rename_v0.md`.
- That branch records `docs/product/core_spine/** -> docs/product/foundation/**`.
- That branch preserves `core_spine_v0_*` artifact IDs in the rename pass.
- That branch diff observed locally changes 161 files and renames the current `docs/product/core_spine/**` product-lane files to `docs/product/foundation/**`.

### Owned Product Surfaces In `docs/product/core_spine/`

These currently live under the legacy Core Spine product lane and must be accounted for before a Foundation migration. The pending rename branch moves these paths to `docs/product/foundation/` while preserving filenames.

Core contracts, standards, and boundaries:

- `docs/product/core_spine/core_spine_v0_product_contract.md`
- `docs/product/core_spine/core_spine_v0_information_production_foundation_v0.md`
- `docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `docs/product/core_spine/core_spine_v0_data_lake_mechanics_map_v0.md`
- `docs/product/core_spine/core_spine_v0_corroboration_vs_amplification_discipline_v0.md`

Cleaning and projection-adjacent Foundation surfaces:

- `docs/product/core_spine/core_spine_v0_cleaning_spine_foundation_v0.md`
- `docs/product/core_spine/core_spine_v0_cleaning_spine_readme_v0.md`

Ontology, exploration, and candidate-pool surfaces:

- `docs/product/core_spine/orca_ontology_backbone_architecture_v0.md`
- `docs/product/core_spine/ontology_expansion_backlog_v0.json`
- `docs/product/core_spine/orca_vertical_exploration_guide_v0.md`
- `docs/product/core_spine/beauty_venue_card_set_v0.md`
- `docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md`
- `docs/product/core_spine/orca_memorization_resistant_case_finder_frame_v0.md`

Ontology cards:

- `docs/product/core_spine/ontology_cards/README.md`
- `docs/product/core_spine/ontology_cards/brand_beautypie_v0.md`
- `docs/product/core_spine/ontology_cards/case_beautypie_repricing_2023_v0.md`
- `docs/product/core_spine/ontology_cards/decision_beautypie_repricing_2023_v0.md`
- `docs/product/core_spine/ontology_cards/outcome_beautypie_repricing_2023_v0.md`
- `docs/product/core_spine/ontology_cards/venue_basenotes_v0.md`
- `docs/product/core_spine/ontology_cards/vertical_beauty_v0.md`

Proof and proof-selection surfaces:

- `docs/product/core_spine/core_spine_v0_proof_protocol_v0.md`
- `docs/product/core_spine/core_spine_v0_proof_input_selection_v0.md`
- `docs/product/core_spine/core_spine_v0_proof_packet_preflight_v0.md`
- `docs/product/core_spine/core_spine_v0_proof_case_selection_brief_v0.md`
- `docs/product/core_spine/core_spine_v0_first_proof_packet_preparation_v0.md`
- `docs/product/core_spine/core_spine_v0_first_proof_run_charter_v0.md`
- `docs/product/core_spine/core_spine_v0_first_proof_run_locks_v0.md`
- `docs/product/core_spine/core_spine_v0_first_proof_run_packet_v0.md`
- `docs/product/core_spine/core_spine_v0_first_proof_run_jb_client0_slice_v0.md`
- `docs/product/core_spine/core_spine_v0_first_proof_run_bt204_backtest_slice_v0.md`
- `docs/product/core_spine/core_spine_v0_first_proof_run_sh01_shadow_slice_v0.md`
- `docs/product/core_spine/core_spine_v0_heavyweight_proof_case_discovery_charter_v0.md`
- `docs/product/core_spine/core_spine_v0_heavyweight_proof_case_discovery_results_v0.md`
- `docs/product/core_spine/core_spine_v0_heavyweight_proof_case_discovery_results_part_2_v0.md`

Backtest specimens:

- `docs/product/core_spine/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md`
- `docs/product/core_spine/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md`
- `docs/product/core_spine/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md`

Method-validation surfaces:

- `docs/product/core_spine/core_spine_v0_method_validation_replay_packet_v0.md`
- `docs/product/core_spine/core_spine_v0_method_validation_rubric_v0.md`
- `docs/product/core_spine/core_spine_v0_method_validation_case_locks_v0.md`
- `docs/product/core_spine/core_spine_v0_method_validation_case_frame_locks_v0.md`
- `docs/product/core_spine/core_spine_v0_method_validation_case_frame_lock_contract_v0.md`
- `docs/product/core_spine/core_spine_v0_method_validation_mv01_intercom_zendesk_replay_v0.md`
- `docs/product/core_spine/core_spine_v0_method_validation_mv03_stack_overflow_chatgpt_replay_v0.md`
- `docs/product/core_spine/core_spine_v0_method_validation_mv04_unity_runtime_fee_replay_v0.md`
- `docs/product/core_spine/core_spine_v0_method_validation_mv05_reddit_api_pricing_replay_v0.md`
- `docs/product/core_spine/core_spine_v0_method_validation_mv09_thomson_reuters_casetext_replay_v0.md`

### Foundation/Core Surfaces Outside `docs/product/core_spine/`

These are not automatically Foundation-home moves. They keep legacy names or consume Foundation semantics, but their allocation needs separate owner confirmation.

Product root:

- `docs/product/core_spine_v0_projection_doctrine_v0.md` - root-level projection doctrine; its header describes a view contract over the Data-Capture-owned Mechanical Source Projection helper.

Data Capture files with legacy `core_spine_v0_` IDs:

- `docs/product/data_capture_spine/core_spine_v0_data_capture_context_preservation_note_v0.md`
- `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`
- `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md`
- `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_remaining_fixture_plan_v0.md`
- `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_pressure_test_archive_history_recapture_v0.md`
- `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_pressure_test_docs_changelog_versioned_page_v0.md`
- `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_pressure_test_public_sector_package_milwaukee_fiscal_crossroads_v0.md`
- `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_pressure_test_review_surface_v0.md`
- `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_pressure_test_synthesis_usage_note_v0.md`
- `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_pressure_test_threaded_forum_reddit_api_pricing_v0.md`

Signal content:

- `docs/product/signal_content/core_spine_v0_signal_content_record_architecture_v0.md`

Review-input source copies that must not be treated as canonical migration targets:

- `docs/review-inputs/judgment_conductor_delegated_review_v0/sources/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/review-inputs/judgment_conductor_delegated_review_v0/sources/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `docs/review-inputs/judgment_conductor_full_decorrelated_adversarial_review_v0/sources/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/review-inputs/judgment_conductor_full_decorrelated_adversarial_review_v0/sources/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `docs/review-inputs/judgment_conductor_post_patch_recheck_v0/sources/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/review-inputs/judgment_conductor_post_patch_recheck_v0/sources/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`

## Legacy Names And Proposed Canonical Names

| Current / legacy string | Proposed canonical handling | Inventory note |
| --- | --- | --- |
| `Core Spine` | `Foundation Layer` | Prose label only until the rename lands or owner confirms. |
| `core_spine` folder/lane | `foundation` folder/lane | Pending branch proposes `docs/product/foundation/`; current branch still uses `docs/product/core_spine/`. |
| `docs/product/core_spine/**` | `docs/product/foundation/**` | Proposed by `codex/foundation-rename`; not applied on current branch. |
| `core_spine_v0_*` artifact IDs | Preserve for this pass | Artifact-ID migration is wider than folder/prose rename and must be separate. |
| `Core Spine v0 Product Contract` | Foundation Layer product contract | Current file/title remain legacy. |
| `Core Spine v0 Information Production Foundation` | Information Production Foundation under Foundation Layer | Already carries "Foundation"; do not rename mechanically. |
| `Core Spine v0 Projection Doctrine` | Foundation/Projection doctrine, allocation owner unresolved | Current file is root-level and tied to Data-Capture-owned projection helper. |
| `core` inside Judgment demand-read core | Not part of Foundation rename | Pending branch rename record says Judgment demand-read core is separate. |

## Owned Foundation Surfaces

Foundation-owned surfaces are the shared product/judgment substrate surfaces that define market-agnostic evidence mechanics, information production, evidence-unit boundaries, ontology, proof/method-validation history, and cross-spine layer contracts.

Primary Foundation-owned surfaces:

- Product contract: `docs/product/core_spine/core_spine_v0_product_contract.md`
- Information Production Foundation: `docs/product/core_spine/core_spine_v0_information_production_foundation_v0.md`
- Data/Cleaning/Judgment boundary: `docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- Data-lake mechanics map: `docs/product/core_spine/core_spine_v0_data_lake_mechanics_map_v0.md`
- Projection doctrine: `docs/product/core_spine_v0_projection_doctrine_v0.md`, allocation pending owner confirmation.
- Corroboration/amplification discipline: `docs/product/core_spine/core_spine_v0_corroboration_vs_amplification_discipline_v0.md`
- Ontology backbone and backlog: `docs/product/core_spine/orca_ontology_backbone_architecture_v0.md`, `docs/product/core_spine/ontology_expansion_backlog_v0.json`, and `docs/product/core_spine/ontology_cards/**`.
- Exploration and source/candidate discovery primitives: `docs/product/core_spine/orca_vertical_exploration_guide_v0.md`, `docs/product/core_spine/beauty_venue_card_set_v0.md`, and `docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md`.
- Proof, backtest, and method-validation family under `docs/product/core_spine/`.

Foundation-owned but possibly future-reallocated surfaces:

- Cleaning Foundation and Cleaning README currently live in `docs/product/core_spine/`; a future `docs/product/cleaning_spine/` lane would need a separate structure decision before moving them.
- Projection doctrine currently lives at `docs/product/` root; moving it into Foundation or Data Capture should wait for owner allocation.
- Signal Content Record architecture has a legacy `core_spine_v0_` ID but lives in `docs/product/signal_content/`; it should remain signal-content-owned unless owner redirects.
- Data Capture obligation/pressure-test files with legacy `core_spine_v0_` IDs live in `docs/product/data_capture_spine/`; they should remain Capture-owned unless owner redirects.

## Shared Surfaces Consumed By Downstream Lanes

### Judgment

Foundation/Core dependencies observed:

- `docs/product/core_spine/core_spine_v0_product_contract.md`
- `docs/product/core_spine/core_spine_v0_information_production_foundation_v0.md`
- `docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `docs/product/core_spine_v0_projection_doctrine_v0.md`
- `docs/product/signal_content/core_spine_v0_signal_content_record_architecture_v0.md`
- `docs/product/judgment_spine/judgment_current_state_and_decomposition_v0.md`
- `docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md`
- `docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md`
- `docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md`
- `docs/product/judgment_spine/jsg01_source_side_receipt_translator_v0.md`
- `docs/product/judgment_spine/jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md`
- `docs/product/judgment_spine/jsg01_sp6_source_visibility_derivation_architecture_routing_v0.md`

Migration note: Judgment can consume Foundation standards, but Judgment's demand-read core is not a Foundation rename target.

### Capture

Foundation/Core dependencies observed:

- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`
- `docs/product/data_capture_spine/core_spine_v0_data_capture_context_preservation_note_v0.md`
- `docs/product/core_spine/core_spine_v0_data_lake_mechanics_map_v0.md`
- `docs/product/core_spine_v0_projection_doctrine_v0.md`
- `docs/product/source_capture_toolbox/source_capture_playbook_v0.md`
- `docs/product/source_capture_toolbox/capture_recon_index_v0.md`

Runtime-facing capture dependency observed:

- `orca-harness/source_capture/models.py` defines `OBLIGATION_CONTRACT_VERSION = "core_spine_v0_data_capture_spine_obligation_contract_v0"`.
- `orca-harness/cases/product_learning/**` has 185 observed files containing either the legacy obligation-contract version or direct `docs/product/core_spine/` provenance links. Treat these as generated/provenance artifacts, not migration move targets.

### ECR / SCR

Foundation/Core dependencies observed:

- `docs/workflows/ecr_spine_submap_v0.md`
- `docs/product/ecr/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md`
- `docs/product/ecr/ecr_consolidation_v0_jsg01_evidence_unit_binding_slice_plan_v0.md`
- `docs/product/signal_content/core_spine_v0_signal_content_record_architecture_v0.md`
- `docs/product/signal_content/signal_content_record_deriver_architecture_plan_v0.md`
- `docs/product/core_spine/core_spine_v0_data_lake_mechanics_map_v0.md`
- `docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`

Runtime-facing ECR/SCR dependency observed:

- `orca-harness/ecr/__init__.py`
- `orca-harness/ecr/models.py`
- `orca-harness/evidence_binding/models.py`
- `orca-harness/signal_content/__init__.py`
- `orca-harness/signal_content/models.py`

### Cleaning

Foundation/Core dependencies observed:

- `docs/product/core_spine/core_spine_v0_cleaning_spine_foundation_v0.md`
- `docs/product/core_spine/core_spine_v0_cleaning_spine_readme_v0.md`
- `docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `docs/product/core_spine_v0_projection_doctrine_v0.md`
- `docs/prompts/handoffs/cleaning_spine_projection_doctrine_handoff_prompt_v0.md`
- `docs/prompts/handoffs/cleaning_spine_foundation_architecture_planning_prompt_v0.md`
- `docs/prompts/handoffs/cleaning_spine_foundation_architecture_planning_prompt_v1.md`

Runtime-facing Cleaning dependency observed:

- `orca-harness/tests/unit/test_cleaning_projection_integration.py`
- `orca-harness/tests/unit/test_reddit_projection.py`
- `orca-harness/tests/unit/test_retail_pdp_projection.py`
- `orca-harness/tests/unit/test_source_capture_ig_projection.py`
- `orca-harness/tests/unit/test_source_capture_packet.py`
- `orca-harness/tests/unit/test_source_quality_report_skeleton.py`

Migration note: these are not move authorization. Cleaning has no accepted `docs/product/cleaning_spine/` lane in the current artifact-folder list.

### Search

Foundation/Core dependencies observed:

- `docs/decisions/orca_search_product_lane_binding_v0.md`
- `docs/product/search/README.md`
- `docs/product/search/orca_demand_scan_core_spec_v0.md`
- `docs/product/search/orca_demand_read_taxonomy_v0.md`
- `docs/product/search/demand_search_interest_sourcing_and_gate_delta_spec_v0.md`
- `docs/product/search/demand_durability_indicator_search_interest_capture_profile_v0.md`

Migration note: search-led demand-signal method docs are venue-spanning consumers of Foundation/Core concepts. The current search lane decision gives topic primacy to `docs/product/search/`; do not pull these into Foundation during a folder rename.

### Product Lead

Foundation/Core dependencies observed:

- `docs/product/product_lead/orca_offer_hypothesis_v0.md`
- `docs/product/product_lead/orca_buyer_proof_packet_v0.md`
- `docs/product/product_lead/orca_buyer_proof_packet_consumer_demand_revision_v0.md`
- `docs/product/product_lead/orca_product_proof_lead_charter_v0.md`
- `docs/product/product_lead/orca_product_lead_first_icp_wedge_decision_v0.md`
- `.agents/skills/orca-product-lead/SKILL.md`

Migration note: Product Lead consumes Foundation as an input layer for buyer-proof/product judgment. It should not own the Foundation home.

### CSB

Search for literal `CSB` did not find a defined Orca surface in the scoped docs and overlay search. Nearby "substrate" hits appear under Product Lead and consumer-demand artifacts, not a canonical CSB lane. Treat CSB allocation as an owner question until the acronym is defined in an accepted Orca source.

## Prompt Surfaces To Account For

Prompt files with direct Core/Foundation dependencies found in the requested search targets:

- `docs/prompts/product-planning/core_spine_v0_method_validation_replay_packet_prompt_v0.md`
- `docs/prompts/product-planning/core_spine_v0_method_validation_cutoff_source_visibility_verification_prompt_v0.md`
- `docs/prompts/product-planning/core_spine_v0_method_validation_case_frame_locks_prompt_v0.md`
- `docs/prompts/deep-thinking/core_spine_v0_method_validation_case_hunting_prompt_v0.md`
- `docs/prompts/wrappers/core_spine_v0_method_validation_fresh_replay_source_loading_wrapper_v0.md`
- `docs/prompts/wrappers/core_spine_v0_method_validation_cutoff_source_visibility_verification_wrapper_v0.md`
- `docs/prompts/reruns/core_spine_v0_method_validation_replay_packet_anti_leakage_rerun_prompt_v0.md`
- `docs/prompts/reviews/core_spine_v0_proof_packet_preparation_adversarial_review_gpt55_prompt_v0.md`
- `docs/prompts/reviews/core_spine_v0_method_validation_case_frame_locks_adversarial_review_gpt54_prompt_v0.md`
- `docs/prompts/reviews/case_to_v0_14_bridge_foundation_adversarial_review_prompt_v0.md`
- `docs/prompts/handoffs/cleaning_spine_projection_doctrine_handoff_prompt_v0.md`
- `docs/prompts/handoffs/cleaning_spine_foundation_architecture_planning_prompt_v0.md`
- `docs/prompts/handoffs/cleaning_spine_foundation_architecture_planning_prompt_v1.md`
- `docs/prompts/deep-thinking/packing_to_harness_foundation_interface_architecture_ca_prompt_v0.md`
- `docs/prompts/architecture/ecr_consolidation_v0_frame_source_visibility_slice_architecture_prompt_v0.md`
- `docs/prompts/architecture/jsg01_sp6_source_visibility_derivation_architecture_prompt_v0.md`
- `docs/prompts/architecture/source_capture_packet_schema_evolution_architecture_prompt_v0.md`
- `docs/prompts/handoffs/ecr_jsg01_source_side_receipt_lane_setup_v0.md`
- `docs/prompts/handoffs/ecr_jsg01_bounded_unfreeze_build_handoff_prompt_v0.md`
- `docs/prompts/handoffs/signal_content_record_deriver_architecture_ecr_lane_handoff_prompt_v0.md`

Migration note: historical prompts and wrappers may retain old names as historical routing records. Do not rewrite prompt titles, artifact IDs, or review output references unless the migration explicitly includes prompt artifact-ID migration.

## Decision And Workflow Surfaces To Account For

Decision records:

- `docs/decisions/orca_repo_structure_binding_v0.md`
- `docs/decisions/orca_search_product_lane_binding_v0.md`
- `docs/decisions/beauty_venue_card_set_promotion_decision_v0.md`
- `docs/decisions/distillation_binding_core_spine_proof_v0.md`
- `docs/decisions/distillation_doctrine_orca_spine_bindings_v0.md`
- `docs/decisions/dcp_receipts_archive_v0.md`
- `docs/decisions/orca_product_thesis_consumer_demand_v0.md`
- `docs/decisions/advisory_proof_slice_definition_v0.md`
- `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`
- `docs/decisions/data_capture_spine_pressure_test_batch_classification_decision_v0.md`
- `docs/decisions/data_capture_spine_obligation_contract_patch_proposal_owner_decision_v0.md`
- `docs/decisions/data_capture_spine_post_batch_patch_plan_owner_decision_v0.md`
- `docs/decisions/jsg01_unfreeze_decision_v0.md`
- `docs/decisions/jsg01_unfreeze_decision_memo_v0.md`
- `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md`
- `docs/decisions/judgment_spine_backtest_batch2_candidate_routing_v0.md`
- `docs/decisions/judgment_spine_backtest_batch2_ledger_declaration_v0.md`

Workflow records and maps:

- `docs/workflows/orca_repo_map_v0.md`
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `docs/workflows/ecr_spine_submap_v0.md`
- `docs/workflows/orca_pricing_first_method_validation_handoff_v0.md`
- `docs/workflows/orca_pricing_first_doc_cascade_proposal_v0.md`
- `docs/workflows/orca_major_move_folder_integrity_ca_discussion_v0.md`
- `docs/workflows/reddit_capture_to_ecr_consumption_probe_finding_v0.md`

Migration note: maps and decisions route future source loading. They should be updated only when the migration itself is accepted; this inventory does not update them.

## Review Surfaces To Account For

Review outputs with direct Core/Foundation dependencies found in the requested search targets:

- `docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v0.md`
- `docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v1.md`
- `docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v2.md`
- `docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_post_patch_confirmation_v0.md`
- `docs/review-outputs/method-validation/core_spine_v0_method_validation_cutoff_source_visibility_verification_report_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_full_fixture_synthesis_adversarial_review_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_manual_harness_bt204_dry_run_adversarial_review_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/case_to_v0_14_bridge_foundation_adversarial_review_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/projection_doctrine_v0_vendor_ca_closeout_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/ecr_consolidation_v0_frame_source_visibility_slice_architecture_prompt_adversarial_review_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/ecr_consolidation_v0_plan_cross_family_review_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/ecr_consolidation_v0_sp1_sp2_sp3_source_side_reconcile_cross_family_review_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/ecr_jsg01_evidence_unit_binding_plan_delegated_adversarial_artifact_review_patch_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/jsg01_source_side_receipt_translator_adversarial_review_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/judgment_spine_gate_ownership_map_adversarial_artifact_review_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/judgment_spine_gate_ownership_map_patch_recheck_adversarial_artifact_review_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/judgment_spine_thesis_operating_contract_adversarial_review_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/source_capture_packet_schema_evolution_architecture_adversarial_artifact_review_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_draft_fixture_pack_adversarial_review_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_fixture_extraction_plan_adversarial_review_v0.md`

Migration note: review outputs are records of reviewed historical state. Do not rewrite them as part of a folder rename unless a separate review-history rewrite policy is accepted.

## Pending PR Or Branch Dependency

Local branch dependency:

- `codex/foundation-rename` at `56a832c0`.
- Commit subject observed: `docs: rename core spine to foundation layer`.
- Diff stat observed: `161 files changed, 765 insertions(+), 632 deletions(-)`.
- Key added artifact: `docs/migration/foundation_layer_rename_v0.md`.
- Key route changes: `.agents/workflow-overlay/artifact-folders.md`, `.agents/workflow-overlay/source-loading.md`, `docs/workflows/orca_repo_map_v0.md`, `repo-structure.yaml`.
- Key product move: all current `docs/product/core_spine/**` files are renamed to `docs/product/foundation/**`.

PR dependency:

- User named PR #242 / `codex/foundation-rename`.
- `gh pr view 242` verified PR #242 as open, draft, base `main`, head `codex/foundation-rename`, merge state `UNSTABLE`, not merged (`mergedAt: null`), URL `https://github.com/eric-foo/orca/pull/242`.
- Local repo text search found no PR #242 record inside `docs`, `.agents`, or `repo-structure.yaml`.
- Current inventory branch does not contain the local `codex/foundation-rename` commit.

Migration implication: before any follow-on migration, first check whether PR #242 has landed or been superseded. Do not duplicate the pending rename branch blindly.

## Future Allocation Proposal

Proposed allocation after owner confirmation:

1. Foundation Layer owns the shared product/judgment substrate: product contract, IPF/Evidence Unit standard, data/cleaning/judgment boundary, data-lake mechanics, ontology, exploration/candidate primitives, proof/method-validation historical family, and any owner-confirmed projection doctrine.
2. Data Capture keeps Data Capture files even when their artifact IDs begin with `core_spine_v0_`.
3. ECR and Signal Content keep their own product-lane homes and runtime packages; Foundation supplies boundary and Evidence Unit semantics, not ownership of ECR/SCR code.
4. Judgment keeps Judgment Spine surfaces and demand-read core; Foundation supplies standards and inputs.
5. Search keeps search-led demand-signal method docs under `docs/product/search/` per the search lane binding.
6. Product Lead consumes Foundation for offer/proof reasoning but does not own the Foundation home.
7. Cleaning remains Foundation-adjacent until a separate Cleaning Spine folder/structure decision exists.
8. Runtime-generated case receipts, manifests, and source-provenance notes keep historical legacy IDs unless a separate provenance migration is explicitly authorized.

## Open Owner Questions

- Is `docs/product/foundation/` the canonical Foundation home, or should the owner alter the pending branch allocation before landing?
- Should `core_spine_v0_*` artifact IDs be preserved indefinitely as stable retrieval handles, or is a later artifact-ID migration desired?
- Should `docs/product/core_spine_v0_projection_doctrine_v0.md` become Foundation-owned, Data Capture-owned, or stay at product root?
- Should Cleaning get a bound `docs/product/cleaning_spine/` lane before any Cleaning Foundation files move?
- What is the canonical expansion and home for CSB?
- Are proof-run and method-validation artifacts active Foundation surfaces, historical Foundation records, or migration-excluded history?
- Should generated case provenance under `orca-harness/cases/product_learning/**` be frozen with old `core_spine_v0_*` IDs?
- Should PR #242 / `codex/foundation-rename` be the migration carrier, or should this inventory supersede or constrain it?

## Suggested Migration Order

1. Verify PR #242 / `codex/foundation-rename` state from the active branch and remote PR before editing.
2. Owner-confirm the concept boundary: Foundation is shared judgment/product substrate, not a downstream spine.
3. Owner-confirm folder allocation: `docs/product/foundation/` versus another Foundation home.
4. Decide whether the migration is folder/prose only or includes artifact-ID renames. Default recommendation: folder/prose only; preserve `core_spine_v0_*` IDs.
5. Apply the pending folder rename only after reconciling with current `main`; update `repo-structure.yaml`, `.agents/workflow-overlay/artifact-folders.md`, `.agents/workflow-overlay/source-loading.md`, and `docs/workflows/orca_repo_map_v0.md` in the same migration.
6. Update live route surfaces and live prompts that must route to the new home. Keep historical prompts/reviews/provenance records unchanged unless explicitly in scope.
7. Review runtime-facing references separately. Code constants, tests, and generated case outputs need a compatibility or versioning decision, not a mechanical docs move.
8. Only after the folder/prose migration is stable, consider a separate artifact-ID migration for `core_spine_v0_*`, with its own inventory and blast-radius review.

## Must Not Move Yet

- Do not move `docs/product/data_capture_spine/core_spine_v0_*` files as part of the Foundation home rename.
- Do not move `docs/product/signal_content/core_spine_v0_signal_content_record_architecture_v0.md` into Foundation without owner allocation.
- Do not move Search lane files into Foundation; search topic primacy is separately bound.
- Do not rewrite historical review outputs, review-input source copies, or prompt titles by default.
- Do not rewrite `orca-harness/cases/product_learning/**` generated case receipts/manifests/provenance as part of this docs inventory.
- Do not alter runtime code constants or tests in an inventory-only migration artifact.

## Explicit Non-Claims

- Not validation.
- Not readiness.
- Not acceptance.
- Not source-of-truth promotion.
- Not implementation authorization.
- Not runtime compatibility proof.
- Not a claim that PR #242 status will remain unchanged after the `gh pr view 242` check in this run.
- Not a completed rename.
- Not a file move.
- Not an artifact-ID migration.
- Not a claim that `docs/product/foundation/` exists on the current branch.
- Not a claim that Foundation naming has landed on `main`.
- Not a claim that generated runtime provenance should be rewritten.
