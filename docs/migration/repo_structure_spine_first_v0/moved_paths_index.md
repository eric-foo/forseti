# Moved Paths Index - Spine-first migration (generated)

```yaml
retrieval_header_version: 1
artifact_role: Orca migration index (generated path-resolution artifact)
scope: >
  Generated old-path -> new-path lookup for the spine-first product
  reorganization (former docs/product lanes -> orca/product spine tree).
  Resolves historical and residual records that keep their point-in-time
  docs/product paths by design. Lookup table only; not authority, validation,
  or migration proof.
use_when:
  - Resolving a historical docs/product path to its orca/product successor.
  - Auditing or re-running the spine-first move or the open_next repointing.
authority_boundary: retrieval_only
open_next:
  - docs/migration/spine_first_execution_route_v0.md
  - docs/decisions/orca_spine_first_target_structure_binding_v0.md
  - docs/migration/spine_first_target_move_table_v0.md
stale_if:
  - The spine-first manifest (moves_manifest.csv) changes and this index is not regenerated.
  - A later accepted migration relocates these artifacts again.
```

Historical + residual records reference old docs/product paths by design;
resolve them here.

| Old path | New path |
| --- | --- |
| `docs/product/README.md` | `orca/product/README.md` |
| `docs/product/core_spine/beauty_venue_card_set_v0.md` | `orca/product/satellites/beauty/beauty_venue_card_set_v0.md` |
| `docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md` | `orca/product/case_families/product_learning/fragrance/consumer_demand_candidate_pool_handoff_v0.md` |
| `docs/product/core_spine/core_spine_v0_cleaning_spine_foundation_v0.md` | `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md` |
| `docs/product/core_spine/core_spine_v0_cleaning_spine_readme_v0.md` | `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md` |
| `docs/product/core_spine/core_spine_v0_corroboration_vs_amplification_discipline_v0.md` | `orca/product/spines/cleaning/contracts/core_spine_v0_corroboration_vs_amplification_discipline_v0.md` |
| `docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` |
| `docs/product/core_spine/core_spine_v0_data_lake_mechanics_map_v0.md` | `orca/product/shared/data_lake_mechanics/core_spine_v0_data_lake_mechanics_map_v0.md` |
| `docs/product/core_spine/core_spine_v0_first_proof_packet_preparation_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_first_proof_packet_preparation_v0.md` |
| `docs/product/core_spine/core_spine_v0_first_proof_run_bt204_backtest_slice_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_first_proof_run_bt204_backtest_slice_v0.md` |
| `docs/product/core_spine/core_spine_v0_first_proof_run_charter_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_first_proof_run_charter_v0.md` |
| `docs/product/core_spine/core_spine_v0_first_proof_run_jb_client0_slice_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_first_proof_run_jb_client0_slice_v0.md` |
| `docs/product/core_spine/core_spine_v0_first_proof_run_locks_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_first_proof_run_locks_v0.md` |
| `docs/product/core_spine/core_spine_v0_first_proof_run_packet_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_first_proof_run_packet_v0.md` |
| `docs/product/core_spine/core_spine_v0_first_proof_run_sh01_shadow_slice_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_first_proof_run_sh01_shadow_slice_v0.md` |
| `docs/product/core_spine/core_spine_v0_heavyweight_proof_case_discovery_charter_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_heavyweight_proof_case_discovery_charter_v0.md` |
| `docs/product/core_spine/core_spine_v0_heavyweight_proof_case_discovery_results_part_2_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_heavyweight_proof_case_discovery_results_part_2_v0.md` |
| `docs/product/core_spine/core_spine_v0_heavyweight_proof_case_discovery_results_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_heavyweight_proof_case_discovery_results_v0.md` |
| `docs/product/core_spine/core_spine_v0_information_production_foundation_v0.md` | `orca/product/spines/foundation/product_contract/core_spine_v0_information_production_foundation_v0.md` |
| `docs/product/core_spine/core_spine_v0_method_validation_case_frame_lock_contract_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_case_frame_lock_contract_v0.md` |
| `docs/product/core_spine/core_spine_v0_method_validation_case_frame_locks_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_case_frame_locks_v0.md` |
| `docs/product/core_spine/core_spine_v0_method_validation_case_locks_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_case_locks_v0.md` |
| `docs/product/core_spine/core_spine_v0_method_validation_mv01_intercom_zendesk_replay_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_mv01_intercom_zendesk_replay_v0.md` |
| `docs/product/core_spine/core_spine_v0_method_validation_mv03_stack_overflow_chatgpt_replay_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_mv03_stack_overflow_chatgpt_replay_v0.md` |
| `docs/product/core_spine/core_spine_v0_method_validation_mv04_unity_runtime_fee_replay_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_mv04_unity_runtime_fee_replay_v0.md` |
| `docs/product/core_spine/core_spine_v0_method_validation_mv05_reddit_api_pricing_replay_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_mv05_reddit_api_pricing_replay_v0.md` |
| `docs/product/core_spine/core_spine_v0_method_validation_mv09_thomson_reuters_casetext_replay_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_mv09_thomson_reuters_casetext_replay_v0.md` |
| `docs/product/core_spine/core_spine_v0_method_validation_replay_packet_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_replay_packet_v0.md` |
| `docs/product/core_spine/core_spine_v0_method_validation_rubric_v0.md` | `orca/product/spines/foundation/product_contract/core_spine_v0_method_validation_rubric_v0.md` |
| `docs/product/core_spine/core_spine_v0_product_contract.md` | `orca/product/spines/foundation/product_contract/core_spine_v0_product_contract.md` |
| `docs/product/core_spine/core_spine_v0_proof_case_selection_brief_v0.md` | `orca/product/case_families/product_learning/other_verticals/core_spine_v0_proof_case_selection_brief_v0.md` |
| `docs/product/core_spine/core_spine_v0_proof_input_selection_v0.md` | `orca/product/spines/foundation/product_contract/core_spine_v0_proof_input_selection_v0.md` |
| `docs/product/core_spine/core_spine_v0_proof_packet_preflight_v0.md` | `orca/product/spines/foundation/product_contract/core_spine_v0_proof_packet_preflight_v0.md` |
| `docs/product/core_spine/core_spine_v0_proof_protocol_v0.md` | `orca/product/spines/foundation/product_contract/core_spine_v0_proof_protocol_v0.md` |
| `docs/product/core_spine/ontology_cards/README.md` | `orca/product/spines/foundation/ontology/ontology_cards/README.md` |
| `docs/product/core_spine/ontology_cards/brand_beautypie_v0.md` | `orca/product/spines/foundation/ontology/ontology_cards/brand_beautypie_v0.md` |
| `docs/product/core_spine/ontology_cards/case_beautypie_repricing_2023_v0.md` | `orca/product/spines/foundation/ontology/ontology_cards/case_beautypie_repricing_2023_v0.md` |
| `docs/product/core_spine/ontology_cards/decision_beautypie_repricing_2023_v0.md` | `orca/product/spines/foundation/ontology/ontology_cards/decision_beautypie_repricing_2023_v0.md` |
| `docs/product/core_spine/ontology_cards/outcome_beautypie_repricing_2023_v0.md` | `orca/product/spines/foundation/ontology/ontology_cards/outcome_beautypie_repricing_2023_v0.md` |
| `docs/product/core_spine/ontology_cards/venue_basenotes_v0.md` | `orca/product/spines/foundation/ontology/ontology_cards/venue_basenotes_v0.md` |
| `docs/product/core_spine/ontology_cards/vertical_beauty_v0.md` | `orca/product/spines/foundation/ontology/ontology_cards/vertical_beauty_v0.md` |
| `docs/product/core_spine/ontology_expansion_backlog_v0.json` | `orca/product/spines/foundation/ontology/ontology_expansion_backlog_v0.json` |
| `docs/product/core_spine/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md` | `orca/product/case_families/product_learning/other_verticals/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md` |
| `docs/product/core_spine/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md` | `orca/product/case_families/product_learning/other_verticals/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md` |
| `docs/product/core_spine/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md` | `orca/product/case_families/product_learning/other_verticals/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md` |
| `docs/product/core_spine/orca_memorization_resistant_case_finder_frame_v0.md` | `orca/product/spines/foundation/vertical_exploration/orca_memorization_resistant_case_finder_frame_v0.md` |
| `docs/product/core_spine/orca_ontology_backbone_architecture_v0.md` | `orca/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md` |
| `docs/product/core_spine/orca_vertical_exploration_guide_v0.md` | `orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md` |
| `docs/product/core_spine_v0_projection_doctrine_v0.md` | `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md` |
| `docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md` | `orca/product/spines/capture/core/demand_durability_indicators/capture_envelope_durability_delta_spec_v0.md` |
| `docs/product/data_capture_spine/core_spine_v0_data_capture_context_preservation_note_v0.md` | `orca/product/spines/capture/core/operating_model/core_spine_v0_data_capture_context_preservation_note_v0.md` |
| `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md` | `orca/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md` |
| `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md` | `orca/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md` |
| `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | `orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md` |
| `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_pressure_test_archive_history_recapture_v0.md` | `orca/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_pressure_test_archive_history_recapture_v0.md` |
| `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_pressure_test_docs_changelog_versioned_page_v0.md` | `orca/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_pressure_test_docs_changelog_versioned_page_v0.md` |
| `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_pressure_test_public_sector_package_milwaukee_fiscal_crossroads_v0.md` | `orca/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_pressure_test_public_sector_package_milwaukee_fiscal_crossroads_v0.md` |
| `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_pressure_test_review_surface_v0.md` | `orca/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_pressure_test_review_surface_v0.md` |
| `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_pressure_test_synthesis_usage_note_v0.md` | `orca/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_pressure_test_synthesis_usage_note_v0.md` |
| `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_pressure_test_threaded_forum_reddit_api_pricing_v0.md` | `orca/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_pressure_test_threaded_forum_reddit_api_pricing_v0.md` |
| `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_remaining_fixture_plan_v0.md` | `orca/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_remaining_fixture_plan_v0.md` |
| `docs/product/data_capture_spine/data_capture_harness_operating_model_architecture_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v0.md` |
| `docs/product/data_capture_spine/data_capture_harness_operating_model_architecture_v1.md` | `orca/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v1.md` |
| `docs/product/data_capture_spine/data_capture_harness_operating_model_architecture_v2.md` | `orca/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v2.md` |
| `docs/product/data_capture_spine/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md` |
| `docs/product/data_capture_spine/data_capture_harness_product_goal_direction_signal_decision_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_harness_product_goal_direction_signal_decision_v0.md` |
| `docs/product/data_capture_spine/data_capture_obligation_baseline_decision_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_obligation_baseline_decision_v0.md` |
| `docs/product/data_capture_spine/data_capture_source_access_boundary_decision_v0.md` | `orca/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md` |
| `docs/product/data_capture_spine/data_capture_source_access_method_plan_v0.md` | `orca/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_method_plan_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_candidate_url_intake_contract_v0.md` | `orca/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_candidate_url_intake_contract_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md` | `orca/product/spines/capture/core/contracts/corpus_intake/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_future_exploration_lanes_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_spine_future_exploration_lanes_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_intake_surface_consolidation_v0.md` | `orca/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_intake_surface_consolidation_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_lane_product_thesis_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_spine_lane_product_thesis_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md` | `orca/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_linkedin_influence_trajectory_watch_spec_v0.md` | `orca/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_influence_trajectory_watch_spec_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_linkedin_lane_index_v0.md` | `orca/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_lane_index_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_linkedin_live_layer_architecture_v0.md` | `orca/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_live_layer_architecture_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_obligation_contract_patch_proposal_v0.md` | `orca/product/spines/capture/core/contracts/obligation_contracts/data_capture_spine_obligation_contract_patch_proposal_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_post_batch_patch_plan_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_spine_post_batch_patch_plan_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md` | `orca/product/spines/capture/core/contracts/obligation_contracts/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_pressure_test_all_slot_synthesis_post_slot3_recapture_delta_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_all_slot_synthesis_post_slot3_recapture_delta_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_pressure_test_all_slot_synthesis_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_all_slot_synthesis_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_pressure_test_closeout_synthesis_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_closeout_synthesis_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_pressure_test_commissioning_plan_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_commissioning_plan_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_pressure_test_execution_authorization_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_execution_authorization_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_pressure_test_slot1_mi_biws_capture_session_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot1_mi_biws_capture_session_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_pressure_test_slot2_teal_capture_session_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot2_teal_capture_session_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_pressure_test_slot3_combined_handoff_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot3_combined_handoff_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_pressure_test_slot3_interim_evidence_synthesis_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot3_interim_evidence_synthesis_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_pressure_test_slot3_reddit_capture_session_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot3_reddit_capture_session_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_pressure_test_slot3_reddit_subbatch_control_note_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot3_reddit_subbatch_control_note_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_pressure_test_slot3_wso_capture_session_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot3_wso_capture_session_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_pressure_test_slot_3_reddit_batch_1of2_reddit_financialcareers_threads_batch_1of2_capture_session_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot_3_reddit_batch_1of2_reddit_financialcareers_threads_batch_1of2_capture_session_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_pressure_test_slot_3_reddit_batch_2of2_reddit_financialcareers_threads_batch_2of2_capture_session_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot_3_reddit_batch_2of2_reddit_financialcareers_threads_batch_2of2_capture_session_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md` | `orca/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md` | `orca/product/spines/scanning/source_families/reddit/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md` |
| `docs/product/data_capture_spine/data_capture_spine_source_observability_requirements_scoping_v0.md` | `orca/product/spines/capture/core/operating_model/data_capture_spine_source_observability_requirements_scoping_v0.md` |
| `docs/product/data_capture_spine/demand_durability_capture_pilot_v0.md` | `orca/product/spines/capture/core/demand_durability_indicators/demand_durability_capture_pilot_v0.md` |
| `docs/product/data_capture_spine/demand_durability_indicator_availability_restock_capture_profile_v0.md` | `orca/product/spines/capture/core/demand_durability_indicators/availability_restock/demand_durability_indicator_availability_restock_capture_profile_v0.md` |
| `docs/product/data_capture_spine/demand_durability_indicator_capture_deconfliction_note_v0.md` | `orca/product/spines/capture/core/demand_durability_indicators/demand_durability_indicator_capture_deconfliction_note_v0.md` |
| `docs/product/data_capture_spine/demand_durability_indicator_price_timeseries_capture_profile_v0.md` | `orca/product/spines/capture/core/demand_durability_indicators/price_timeseries/demand_durability_indicator_price_timeseries_capture_profile_v0.md` |
| `docs/product/data_capture_spine/demand_durability_indicator_review_velocity_corpus_capture_profile_v0.md` | `orca/product/spines/capture/core/demand_durability_indicators/review_velocity/demand_durability_indicator_review_velocity_corpus_capture_profile_v0.md` |
| `docs/product/data_capture_spine/demand_durability_indicator_standing_capture_obligation_home_decision_framing_v0.md` | `orca/product/spines/capture/core/demand_durability_indicators/demand_durability_indicator_standing_capture_obligation_home_decision_framing_v0.md` |
| `docs/product/data_capture_spine/demand_durability_multi_retailer_rendered_capture_spec_v0.md` | `orca/product/spines/capture/core/source_families/retail_pdp/demand_durability_multi_retailer_rendered_capture_spec_v0.md` |
| `docs/product/data_capture_spine/demand_durability_us_storefront_pin_recon_verdict_v0.md` | `orca/product/spines/capture/core/source_families/retail_pdp/demand_durability_us_storefront_pin_recon_verdict_v0.md` |
| `docs/product/data_capture_spine/orca_capture_projection_storage_spine_architecture_v0.md` | `orca/product/spines/capture/core/operating_model/orca_capture_projection_storage_spine_architecture_v0.md` |
| `docs/product/data_capture_spine/orca_creator_momentum_pipeline_architecture_v0.md` | `orca/product/spines/capture/core/source_families/social_media/instagram/orca_creator_momentum_pipeline_architecture_v0.md` |
| `docs/product/data_capture_spine/orca_creator_monitoring_policy_architecture_v0.md` | `orca/product/spines/capture/core/source_families/social_media/instagram/orca_creator_monitoring_policy_architecture_v0.md` |
| `docs/product/data_capture_spine/retail_pdp_typed_envelope_probe_v0.md` | `orca/product/spines/capture/core/source_families/retail_pdp/retail_pdp_typed_envelope_probe_v0.md` |
| `docs/product/data_capture_spine/source_capture_core_payload_split_explainer_v0.md` | `orca/product/spines/capture/core/packet_schema/source_capture_core_payload_split_explainer_v0.md` |
| `docs/product/data_capture_spine/source_capture_packet_schema_evolution_architecture_v0.md` | `orca/product/spines/capture/core/packet_schema/source_capture_packet_schema_evolution_architecture_v0.md` |
| `docs/product/data_capture_spine/source_capture_tenant_payload_attachment_boundary_v0.md` | `orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md` |
| `docs/product/ecr/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md` | `orca/product/spines/ecr/evidence_candidate_record/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md` |
| `docs/product/ecr/ecr_consolidation_v0_jsg01_evidence_unit_binding_slice_plan_v0.md` | `orca/product/spines/ecr/evidence_candidate_record/ecr_consolidation_v0_jsg01_evidence_unit_binding_slice_plan_v0.md` |
| `docs/product/ecr/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md` | `orca/product/spines/ecr/evidence_candidate_record/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md` |
| `docs/product/engagement_logic_registry_v0.md` | `orca/product/shared/engagement_registry/engagement_logic_registry_v0.md` |
| `docs/product/judgment_spine/conductor_construction_integrity_probe_addendum_proposal_v0.md` | `orca/product/spines/judgment/conductor/conductor_construction_integrity_probe_addendum_proposal_v0.md` |
| `docs/product/judgment_spine/conductor_construction_integrity_probe_addendum_v1.md` | `orca/product/spines/judgment/conductor/conductor_construction_integrity_probe_addendum_v1.md` |
| `docs/product/judgment_spine/demand_read_core_adoption_and_ledger_first_direction_v0.md` | `orca/product/spines/judgment/demand_read/core/demand_read_core_adoption_and_ledger_first_direction_v0.md` |
| `docs/product/judgment_spine/fragrance_level1_casebook_admission_frame_v0.md` | `orca/product/satellites/fragrance/judgment_level1/casebook_admission/fragrance_level1_casebook_admission_frame_v0.md` |
| `docs/product/judgment_spine/fragrance_level1_named_case_candidate_screen_v0.md` | `orca/product/satellites/fragrance/judgment_level1/named_case_screens/fragrance_level1_named_case_candidate_screen_v0.md` |
| `docs/product/judgment_spine/fragrance_level1_product_learning_reconciliation_v0.md` | `orca/product/satellites/fragrance/judgment_level1/reconciliation/fragrance_level1_product_learning_reconciliation_v0.md` |
| `docs/product/judgment_spine/fragrance_level1_product_learning_satellite_skeleton_v0.md` | `orca/product/satellites/fragrance/judgment_level1/satellite_skeleton/fragrance_level1_product_learning_satellite_skeleton_v0.md` |
| `docs/product/judgment_spine/jsg01_source_side_receipt_translator_v0.md` | `orca/product/spines/judgment/source_side_receipts/jsg01_source_side_receipt_translator_v0.md` |
| `docs/product/judgment_spine/jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md` | `orca/product/spines/judgment/source_side_receipts/jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md` |
| `docs/product/judgment_spine/jsg01_sp6_source_visibility_derivation_architecture_routing_v0.md` | `orca/product/spines/judgment/source_side_receipts/jsg01_sp6_source_visibility_derivation_architecture_routing_v0.md` |
| `docs/product/judgment_spine/judgment_current_state_and_decomposition_v0.md` | `orca/product/spines/judgment/judgment_current_state_and_decomposition_v0.md` |
| `docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md` | `orca/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md` |
| `docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md` | `orca/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md` |
| `docs/product/judgment_spine/judgment_spine_c2_qualitative_read_feasibility_probe_v0.md` | `orca/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_qualitative_read_feasibility_probe_v0.md` |
| `docs/product/judgment_spine/judgment_spine_c2_qualitative_read_feasibility_probe_v1.md` | `orca/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_qualitative_read_feasibility_probe_v1.md` |
| `docs/product/judgment_spine/judgment_spine_c2_qualitative_read_feasibility_probe_v2.md` | `orca/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_qualitative_read_feasibility_probe_v2.md` |
| `docs/product/judgment_spine/judgment_spine_c2_rule3_reground_phase_a_classification_finding_v0.md` | `orca/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_rule3_reground_phase_a_classification_finding_v0.md` |
| `docs/product/judgment_spine/judgment_spine_c3_verdict_action_ceiling_contract_v0.md` | `orca/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md` |
| `docs/product/judgment_spine/judgment_spine_demand_read_grading_rubric_v0.md` | `orca/product/spines/judgment/demand_read/grading/judgment_spine_demand_read_grading_rubric_v0.md` |
| `docs/product/judgment_spine/judgment_spine_demand_read_machinery_architecture_v0.md` | `orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md` |
| `docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md` | `orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md` |
| `docs/product/judgment_spine/judgment_spine_first_demand_read_scope_v0.md` | `orca/product/spines/judgment/demand_read/core/judgment_spine_first_demand_read_scope_v0.md` |
| `docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md` | `orca/product/spines/judgment/conductor/judgment_spine_gate_ownership_map_v0.md` |
| `docs/product/judgment_spine/judgment_spine_reveal_calibration_owner_contract_v0.md` | `orca/product/spines/judgment/conductor/judgment_spine_reveal_calibration_owner_contract_v0.md` |
| `docs/product/judgment_spine/judgment_spine_toolkit_blocker_specs_from_daimler_source_fanout_v0.md` | `orca/product/spines/judgment/toolkit_gaps/judgment_spine_toolkit_blocker_specs_from_daimler_source_fanout_v0.md` |
| `docs/product/judgment_spine/near_half_backtest_learning_architecture_v0.md` | `orca/product/spines/judgment/learning_loops/near_half/near_half_backtest_learning_architecture_v0.md` |
| `docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md` | `orca/product/spines/judgment/learning_loops/near_half/near_half_signal_reliability_ledger_v0.md` |
| `docs/product/judgment_spine/prospective_decision_loop_phase0_semantics_spec_v0.md` | `orca/product/spines/judgment/learning_loops/far_half/prospective_decision_loop_phase0_semantics_spec_v0.md` |
| `docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md` | `orca/product/spines/judgment/learning_loops/far_half/prospective_decision_loop_target_architecture_v0.md` |
| `docs/product/product_lead/orca_buyer_proof_packet_consumer_demand_revision_v0.md` | `orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_consumer_demand_revision_v0.md` |
| `docs/product/product_lead/orca_buyer_proof_packet_v0.md` | `orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md` |
| `docs/product/product_lead/orca_claim_defense_doctrine_v0.md` | `orca/product/spines/product_lead/proof_charter/orca_claim_defense_doctrine_v0.md` |
| `docs/product/product_lead/orca_discovery_batch_0_candidate_context_scan_v0.md` | `orca/product/spines/product_lead/icp_wedge/orca_discovery_batch_0_candidate_context_scan_v0.md` |
| `docs/product/product_lead/orca_discovery_batch_0_qualification_prep_sentry_clerk_v0.md` | `orca/product/spines/product_lead/icp_wedge/orca_discovery_batch_0_qualification_prep_sentry_clerk_v0.md` |
| `docs/product/product_lead/orca_discovery_batch_0_target_selection_brief_v0.md` | `orca/product/spines/product_lead/icp_wedge/orca_discovery_batch_0_target_selection_brief_v0.md` |
| `docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md` | `orca/product/spines/product_lead/icp_wedge/orca_discovery_consumer_demand_target_selection_brief_v0.md` |
| `docs/product/product_lead/orca_icp_ratification_readiness_report_v0.md` | `orca/product/spines/product_lead/icp_wedge/orca_icp_ratification_readiness_report_v0.md` |
| `docs/product/product_lead/orca_offer_hypothesis_consumer_demand_revision_v0.md` | `orca/product/spines/product_lead/offer/orca_offer_hypothesis_consumer_demand_revision_v0.md` |
| `docs/product/product_lead/orca_offer_hypothesis_v0.md` | `orca/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md` |
| `docs/product/product_lead/orca_product_lead_first_icp_wedge_decision_v0.md` | `orca/product/spines/product_lead/icp_wedge/orca_product_lead_first_icp_wedge_decision_v0.md` |
| `docs/product/product_lead/orca_product_proof_lead_charter_consumer_demand_revision_v0.md` | `orca/product/spines/product_lead/proof_charter/orca_product_proof_lead_charter_consumer_demand_revision_v0.md` |
| `docs/product/product_lead/orca_product_proof_lead_charter_v0.md` | `orca/product/spines/product_lead/proof_charter/orca_product_proof_lead_charter_v0.md` |
| `docs/product/product_lead/orca_ratification_day_runbook_v0.md` | `orca/product/spines/product_lead/icp_wedge/orca_ratification_day_runbook_v0.md` |
| `docs/product/search/aeo_capture_feasibility_probe_phase0_v0.md` | `docs/research/answer_engine/aeo_capture_feasibility_probe_phase0_v0.md` |
| `docs/product/search/aeo_capture_feasibility_probe_phase0_v0_evidence.json` | `docs/research/answer_engine/aeo_capture_feasibility_probe_phase0_v0_evidence.json` |
| `docs/product/search/demand_durability_indicator_search_interest_capture_profile_v0.md` | `orca/product/spines/capture/core/demand_durability_indicators/search_interest/demand_durability_indicator_search_interest_capture_profile_v0.md` |
| `docs/product/search/demand_search_interest_sourcing_and_gate_delta_spec_v0.md` | `orca/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md` |
| `docs/product/search/orca_demand_gate_definition_closures_proposal_v0.md` | `orca/product/spines/scanning/admissibility_checkability/orca_demand_gate_definition_closures_proposal_v0.md` |
| `docs/product/search/orca_demand_gate_run_commission_criteria_v0.md` | `orca/product/spines/commission_signal_board/dispatch_rules/orca_demand_gate_run_commission_criteria_v0.md` |
| `docs/product/search/orca_demand_read_taxonomy_adjudication_v0.md` | `orca/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_adjudication_v0.md` |
| `docs/product/search/orca_demand_read_taxonomy_v0.md` | `orca/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md` |
| `docs/product/search/orca_demand_scan_core_spec_v0.md` | `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md` |
| `docs/product/search/orca_demand_scan_gate_adjudication_packet_v0.md` | `orca/product/spines/scanning/admissibility_checkability/orca_demand_scan_gate_adjudication_packet_v0.md` |
| `docs/product/signal_content/core_spine_v0_signal_content_record_architecture_v0.md` | `orca/product/spines/ecr/signal_content/core_spine_v0_signal_content_record_architecture_v0.md` |
| `docs/product/signal_content/signal_content_record_deriver_architecture_plan_v0.md` | `orca/product/spines/ecr/signal_content/signal_content_record_deriver_architecture_plan_v0.md` |
| `docs/product/source_capture_toolbox/README.md` | `orca/product/spines/capture/core/source_capture_toolbox/README.md` |
| `docs/product/source_capture_toolbox/archive_org_capture_runner_resilience_learnings_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/archive_org_capture_runner_resilience_learnings_v0.md` |
| `docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md` |
| `docs/product/source_capture_toolbox/armory_weapon_and_pipe_readme_templates_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/armory_weapon_and_pipe_readme_templates_v0.md` |
| `docs/product/source_capture_toolbox/capture_recon_index_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md` |
| `docs/product/source_capture_toolbox/cloakbrowser_local_setup_probe_receipt_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/cloakbrowser_local_setup_probe_receipt_v0.md` |
| `docs/product/source_capture_toolbox/cloakbrowser_packet_runner_architecture_independent_pass_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/cloakbrowser_packet_runner_architecture_independent_pass_v0.md` |
| `docs/product/source_capture_toolbox/cloakbrowser_packet_runner_architecture_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/cloakbrowser_packet_runner_architecture_v0.md` |
| `docs/product/source_capture_toolbox/ig_at_scale_operating_envelope_v0.md` | `orca/product/spines/capture/core/source_families/social_media/instagram/ig_at_scale_operating_envelope_v0.md` |
| `docs/product/source_capture_toolbox/ig_capture_findings_consolidated_v0.md` | `orca/product/spines/capture/core/source_families/social_media/instagram/ig_capture_findings_consolidated_v0.md` |
| `docs/product/source_capture_toolbox/ig_capture_rate_findings_report_v0.md` | `orca/product/spines/capture/core/source_families/social_media/instagram/ig_capture_rate_findings_report_v0.md` |
| `docs/product/source_capture_toolbox/ig_capture_shape_contract_spec_v0.md` | `orca/product/spines/capture/core/source_families/social_media/instagram/ig_capture_shape_contract_spec_v0.md` |
| `docs/product/source_capture_toolbox/ig_creator_discovery_spec_v0.md` | `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_discovery_spec_v0.md` |
| `docs/product/source_capture_toolbox/ig_creator_discovery_suggested_accounts_recon_v0.md` | `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_discovery_suggested_accounts_recon_v0.md` |
| `docs/product/source_capture_toolbox/ig_creator_roster_frontier_ledger_spec_v0.md` | `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md` |
| `docs/product/source_capture_toolbox/ig_logged_out_sustainability_probe_plan_v0.md` | `orca/product/spines/capture/core/source_families/social_media/instagram/ig_logged_out_sustainability_probe_plan_v0.md` |
| `docs/product/source_capture_toolbox/ig_r_probe_results_v0.md` | `orca/product/spines/capture/core/source_families/social_media/instagram/ig_r_probe_results_v0.md` |
| `docs/product/source_capture_toolbox/ig_reel_viewcount_capture_feasibility_recon_v0.md` | `orca/product/spines/capture/core/source_families/social_media/instagram/ig_reel_viewcount_capture_feasibility_recon_v0.md` |
| `docs/product/source_capture_toolbox/ig_sustained_cadence_r_probe_design_v0.md` | `orca/product/spines/capture/core/source_families/social_media/instagram/ig_sustained_cadence_r_probe_design_v0.md` |
| `docs/product/source_capture_toolbox/ig_wind_caller_calls_capture_build_architecture_v0.md` | `orca/product/spines/capture/core/source_families/social_media/instagram/ig_wind_caller_calls_capture_build_architecture_v0.md` |
| `docs/product/source_capture_toolbox/ig_wind_caller_capture_feasibility_recon_v0.md` | `orca/product/spines/capture/core/source_families/social_media/instagram/ig_wind_caller_capture_feasibility_recon_v0.md` |
| `docs/product/source_capture_toolbox/linkedin_reddit_source_capture_armory_concurrent_structure_architecture_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/linkedin_reddit_source_capture_armory_concurrent_structure_architecture_v0.md` |
| `docs/product/source_capture_toolbox/pipe_block_wall_escalation_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/pipe_block_wall_escalation_v0.md` |
| `docs/product/source_capture_toolbox/reddit_capture_operator_playbook_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/reddit_capture_operator_playbook_v0.md` |
| `docs/product/source_capture_toolbox/reddit_packet_consolidation_runner_structural_spec_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/reddit_packet_consolidation_runner_structural_spec_v0.md` |
| `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md` |
| `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md` |
| `docs/product/source_capture_toolbox/retail_pdp_projection_contract_v0.md` | `orca/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_contract_v0.md` |
| `docs/product/source_capture_toolbox/retail_pdp_projection_playbook_v0.md` | `orca/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_playbook_v0.md` |
| `docs/product/source_capture_toolbox/retail_pdp_sidecar_operator_playbook_v0.md` | `orca/product/spines/capture/core/source_families/retail_pdp/retail_pdp_sidecar_operator_playbook_v0.md` |
| `docs/product/source_capture_toolbox/source_capture_anti_block_ladder_usage_guide_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/source_capture_anti_block_ladder_usage_guide_v0.md` |
| `docs/product/source_capture_toolbox/source_capture_anti_blocking_http_ladder_daimler_rung_resolution_closeout_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/source_capture_anti_blocking_http_ladder_daimler_rung_resolution_closeout_v0.md` |
| `docs/product/source_capture_toolbox/source_capture_packet_fixture_admission_criteria_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/source_capture_packet_fixture_admission_criteria_v0.md` |
| `docs/product/source_capture_toolbox/source_capture_playbook_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md` |
| `docs/product/source_capture_toolbox/source_capture_toolbox_agent_usability_dry_run_closeout_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/source_capture_toolbox_agent_usability_dry_run_closeout_v0.md` |
| `docs/product/source_capture_toolbox/source_quality_cw_p1_end_to_end_pass_closeout_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/source_quality_cw_p1_end_to_end_pass_closeout_v0.md` |
| `docs/product/source_capture_toolbox/source_quality_cw_p4_end_to_end_pass_closeout_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/source_quality_cw_p4_end_to_end_pass_closeout_v0.md` |
| `docs/product/source_capture_toolbox/source_quality_cw_p6_end_to_end_pass_closeout_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/source_quality_cw_p6_end_to_end_pass_closeout_v0.md` |
| `docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md` |
| `docs/product/source_capture_toolbox/source_quality_mixed_source_trial_closeout_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/source_quality_mixed_source_trial_closeout_v0.md` |
| `docs/product/source_capture_toolbox/source_quality_slot3_post_recapture_closeout_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/source_quality_slot3_post_recapture_closeout_v0.md` |
| `docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md` |
| `docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/source_quality_state_assembler_v0.md` |
| `docs/product/source_capture_toolbox/weapon_anti_block_http_ladder_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/weapon_anti_block_http_ladder_v0.md` |
| `docs/product/source_capture_toolbox/weapon_rung15_embedded_payload_extraction_v0.md` | `orca/product/spines/capture/core/source_capture_toolbox/weapon_rung15_embedded_payload_extraction_v0.md` |

docs/product/search/README.md -> RETIRED_NO_SUCCESSOR
