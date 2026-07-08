# Precompact Working Packet

## Restore Contract

- packet_version: workflow-precompact-max-v0
- mode: max
- created_at: 2026-06-27T17:48:16.0863556Z (UTC); 2026-06-28T01:48:16.0862271+08:00 (local)
- workspace: C:\Users\vmon7\Desktop\projects\orca
- checkpoint_path: C:\Users\vmon7\Desktop\projects\orca\docs\hygiene\data_lake_v4_1_silver_vault_precompact_v0.md
- expected_branch: codex/ig-reels-capture-spine
- expected_head: f95c33ae4162464354a33cd07be557d2eedc6c89
- expected_dirty_state_after_checkpoint: dirty state before checkpoint plus `?? docs/hygiene/data_lake_v4_1_silver_vault_precompact_v0.md`; exact observed after-state is recorded in Workspace State.
- recovery_rule: On resume, compare workspace, branch, HEAD, dirty state, target-file hashes, and decisive source files. Use `REUSE` only if material facts match. Use `STALE_REREAD_REQUIRED` if docs changed but can be reread. Use `BLOCKED_DRIFT` if target files contain unknown conflicting edits.

## Active Objective

Lock the Orca Data Lake v4.1 forward foundation after the owner corrected that medallion names must stay semantic labels, not physical `bronze/`, `silver/`, or `gold/` folders. The immediate work completed before this packet was a source-backed spec consistency check and wording patch; no implementation/runtime migration was attempted.

## Exact Next Authorized Action

1. After `/compact`, read this packet and run the recovery checks before using it.
2. If recovery is `REUSE`, continue from the verified v4.1 docs state: no more spec edits are known needed; next owner-facing move is either scoped commit/PR preparation for the docs or launching the separate runner data-lake dump audit from its handoff.
3. Stop and reread the binding contracts before any implementation, live lake archive/delete, or runner patch. Do not write to `F:\orca-data-lake` from this packet.

## Authority And Source Ledger

- source-loading mode: repo-overlay-bound
- output mode: temporary-output precompact checkpoint under `docs/hygiene/`; this file itself is dirty/untracked workflow state.
- Repository instructions:
  - `AGENTS.md`: Orca project instructions; push back on wrong assumptions; preserve failure visibility; default docs/prompts/reviews/migration notes allowed; implementation/runtime requires explicit bounded authorization.
- Overlay or equivalent authority:
  - `.agents/workflow-overlay/README.md`: read before project work; overlay is binding.
  - `.agents/workflow-overlay/artifact-folders.md`: workflow/checkpoint artifacts may live under `docs/hygiene` when not source of truth.
  - `.agents/workflow-overlay/decision-routing.md`: substantial/doctrine-changing work uses routing; this lane was architecture/spec-doc work, not implementation.
- User constraints:
  - Current small lake may be archived/abandoned; long-term compounding shape matters more than preserving weak data.
  - Do not add generic physical `bronze/`, `silver/`, `gold/` storage tiers; use canonical raw/derived/indexes shape with medallion labels only.
  - v4.1 is clean forward contract; runner audit should happen separately and should not collide with Silver Vault schema work.
- Source-read ledger:
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md` | lines=422 | sha256=ABB8B54E1A0140278CED782D096A8F889690F74F53CE8A57B65D953E5F04E748
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md` | lines=541 | sha256=83DA3A6ECD5EDD87DD67AC26BBFBC7946591A0544483261ED29C8776B2052EDA
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md` | lines=313 | sha256=16FAB2019CC4B151FA2C2FDD502DFED6279582BB77526CEA9B6FFAE6685E1C9A
- `docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md` | lines=427 | sha256=F2F69D8577549C603007F043F14C9D07E1CFF67C1EAD91A44D3FA14305D5E576
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md` | lines=344 | sha256=5664051651B348959254AE6913F9274EAF67280022B42BBC618BC5A375D4D5EE
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md` | lines=201 | sha256=4587AAC7D44DC4FB12E0C5C4A7FCDFC96432FECBD42062A9706054EF3A2B6391
- `.agents/workflow-overlay/README.md` | lines=38 | sha256=7A30709D6011BD3F6458E926570B7164B91C7F3BF8BAE7DBD5A612A08DE81FDA
- `.agents/workflow-overlay/artifact-folders.md` | lines=420 | sha256=42D4F554DAF4BE6F0A4A9BCBE3C67FD74EEFCC063FC72B03E53E11242EDC7AE9
- `.agents/workflow-overlay/decision-routing.md` | lines=189 | sha256=8CA8069E20C5803A1B645921ABBD986656739C943ED0996572E26A4B9430092E
- `AGENTS.md` | lines=95 | sha256=4296E7617D8B2675881780CD7BE0704A00DCB17ADF7758243008DE956070940B
- Source gaps:
  - Current code implementation was not patched. `orca-harness/data_lake/root.py` and packet writers still need the separate runner audit/implementation pass.
  - Live external lake was inspected earlier in this lane; reread before any operator action. No external root write/rename/delete happened.
- Strict-only blockers:
  - Live lake archive/delete requires explicit operator action and likely escalation.
  - Runtime implementation requires explicit bounded authorization.
- Not-proven boundaries:
  - No tests prove v4.1 writer behavior yet.
  - No SQL/query table implementation exists from this work.
  - No Creator Vault UI/API/client replica was built.

## Current Task State

- Completed:
  - Back-checked v4.1 docs against binding medallion, physicality, and derived-layout contracts.
  - Confirmed no stale `bronze/raw`, `silver/authority`, `silver/retrieval`, or `gold/judgment` physical-folder scheme remains.
  - Patched wording-level misses so v4.1 sharding is the forward target and medallion names are semantic labels only.
  - Verified `git diff --check` on the tracked physicality edit; only Git LF-to-CRLF warning remains.
- Partially completed:
  - Silver Vault record contract and v4.1 forward epoch contract are authored but untracked.
  - Runner data-lake dump audit handoff is authored but untracked; it is read-only audit scope unless separately authorized.
- Broken or uncertain:
  - Runtime code still likely disagrees with v4.1 sharded pathing.
  - Existing live root has small useful samples but no Creator/Silver Vault retrieval layer; it is not migrated.

## Workspace State

- Branch: codex/ig-reels-capture-spine
- Head: f95c33ae4162464354a33cd07be557d2eedc6c89
- Dirty or untracked state before checkpoint:

```text
 M orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
?? .codex/hooks/run_orca_guard.py
?? _scratch/aeo_spec_review_source_pack_v0.zip
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0.zip
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/SOURCE_MANIFEST.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/START_HERE_CHATGPTPRO_PROMPT.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/.agents/workflow-overlay/README.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/.agents/workflow-overlay/source-loading.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/AGENTS.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/docs/decisions/orca_data_lake_spine_promotion_binding_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/docs/decisions/orca_product_thesis_consumer_demand_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/docs/workflows/ig_reels_capture_to_projection_ecr_cleaning_handoff_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/docs/workflows/ig_reels_projection_to_ecr_consumption_decision_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/docs/workflows/social_dom_json_capture_to_youtube_tiktok_handoff_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/cleaning/models.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/cleaning/projection.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/data_lake/root.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/ecr/lake.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/runners/run_source_capture_ig_reels_grid_packet.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/signal_content/lake.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/source_capture/ig_projection.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/source_capture/ig_reels_grid.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/source_capture/ig_reels_grid_capture.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/source_capture/ig_reels_grid_projection.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/source_capture/models.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/source_capture/packet_assembly.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/source_capture/writer.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/youtube_capture/README.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/youtube_capture/capture_youtube_v0.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/youtube_capture/enrich_ryd_v0.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/youtube_capture/shorts_scroll_capture_v0.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/capture/core/source_families/social_media/instagram/ig_capture_shape_contract_spec_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/capture/core/source_families/social_media/instagram/orca_creator_momentum_pipeline_architecture_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/capture/core/source_families/social_media/instagram/orca_creator_monitoring_policy_architecture_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_agent_playbook_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_recon_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/README.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0.zip
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/SOURCE_MANIFEST.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/START_HERE_CHATGPTPRO_PROMPT.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/.agents/workflow-overlay/README.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/.agents/workflow-overlay/source-loading.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/AGENTS.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/core_spine/core_spine_v0_cleaning_spine_foundation_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/core_spine_v0_projection_doctrine_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/data_capture_spine/data_capture_spine_intake_surface_consolidation_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/data_capture_spine/demand_durability_indicator_availability_restock_capture_profile_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/data_capture_spine/demand_durability_indicator_price_timeseries_capture_profile_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/data_capture_spine/demand_durability_indicator_review_velocity_corpus_capture_profile_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/data_capture_spine/orca_capture_projection_storage_spine_architecture_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/data_capture_spine/orca_creator_monitoring_policy_architecture_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/data_capture_spine/source_capture_packet_schema_evolution_architecture_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/ecr/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/ecr/ecr_consolidation_v0_jsg01_evidence_unit_binding_slice_plan_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/ecr/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/signal_content/core_spine_v0_signal_content_record_architecture_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/signal_content/signal_content_record_deriver_architecture_plan_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/source_capture_toolbox/ig_capture_shape_contract_spec_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/source_capture_toolbox/ig_creator_roster_frontier_ledger_spec_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/source_capture_toolbox/reddit_packet_consolidation_runner_structural_spec_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/source_capture_toolbox/retail_pdp_projection_playbook_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/workflows/data_capture_spine_consolidation_map_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/workflows/ecr_spine_submap_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/ecr/deriver.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/ecr/models.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/evidence_binding/composer.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/evidence_binding/models.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/evidence_binding/verifier.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/runners/run_source_capture_ig_calls_packet.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/signal_content/deriver.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/signal_content/models.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/source_capture/ig_momentum_harvest.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/source_capture/models.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/source_capture/reddit_projection.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/source_capture/retail_pdp_projection.py
?? _scratch/ig_reels_diag_esthertakumi/manifest.json
?? _scratch/ig_reels_diag_esthertakumi/raw/01_ig_reels_grid_capture.json
?? _scratch/ig_reels_diag_esthertakumi/receipt.md
?? _scratch/ig_reels_pinprobe_jeremyfragrance/manifest.json
?? _scratch/ig_reels_pinprobe_jeremyfragrance/raw/01_ig_reels_grid_capture.json
?? _scratch/ig_reels_pinprobe_jeremyfragrance/receipt.md
?? _scratch/manual_lake_root_probe/.orca-data-root
?? _scratch/manual_lake_root_probe/.staging/01KVQGPGY4WWNYEHQDJRMSVEX0/probe.txt
?? _scratch/manual_lake_write_probe/stage_plain/probe.txt
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0.zip
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0/README_FOR_CHATGPT_PRO.md
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0/sources/.agents/workflow-overlay/product-proof.md
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0/sources/docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0/sources/docs/decisions/orca_product_thesis_consumer_demand_v0.md
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0/sources/orca/product/spines/foundation/product_contract/core_spine_v0_product_contract.md
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0/sources/orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0/sources/orca/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0/sources/orca/product/spines/product_lead/proof_charter/orca_claim_defense_doctrine_v0.md
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0/sources/orca/product/spines/product_lead/proof_charter/orca_product_proof_lead_charter_v0.md
?? _scratch/precompact_creator_signal_data_lake_v0.md
?? _scratch/precompact_ig_reels_capture_v0.md
?? docs/hygiene/cleaning_spine_lane_handoff_v0.md
?? docs/hygiene/commission_signal_board_lane_handoff_v0.md
?? docs/hygiene/creator_ledger_placement_eli5_handoff_v0.md
?? docs/hygiene/orca_creator_signal_idea_viability_lane_handoff_v0.md
?? docs/hygiene/orca_signal_naming_brand_architecture_handoff_v0.md
?? docs/hygiene/social_capture_browser_calibration_lane_handoff_v0.md
?? docs/prompts/deep-thinking/creator_intelligence_sync_foundation_chatgptpro_prompt_v0.md
?? docs/prompts/deep-thinking/creator_ledger_cross_platform_identity_architecture_prompt_v0.md
?? docs/prompts/deep-thinking/full_system_name_aura_review_prompt_v0.md
?? docs/prompts/patches/fused_delegated_review_gate_tightening_patch_prompt_v0.md
?? docs/prompts/product-planning/orca_spine_first_target_structure_controller_prompt_v0.md
?? docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md
?? docs/workflows/data_lake_r2_continuation_handoff_v0.md
?? docs/workflows/ig_reels_projection_to_ecr_consumption_decision_v0.md
?? orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
?? orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md
?? worktrees/creator-ledger-static-fixture/
?? worktrees/ecr-loader-review/
?? worktrees/ig-reel-deep-capture-codex/
?? worktrees/ig-reels-extract-routine/
?? worktrees/ig-reels-projection-residuals-pr/
?? worktrees/pr380-ci-fix/
?? worktrees/pr380-updated-merge-test/
?? worktrees/scanning-fragrance-commission/
?? worktrees/search-surface-mgt-p0-captures/
?? worktrees/youtube-downstream-ecr-cleaning/
```

- Dirty or untracked state after checkpoint:

```text
 M orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
?? .codex/hooks/run_orca_guard.py
?? _scratch/aeo_spec_review_source_pack_v0.zip
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0.zip
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/SOURCE_MANIFEST.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/START_HERE_CHATGPTPRO_PROMPT.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/.agents/workflow-overlay/README.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/.agents/workflow-overlay/source-loading.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/AGENTS.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/docs/decisions/orca_data_lake_spine_promotion_binding_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/docs/decisions/orca_product_thesis_consumer_demand_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/docs/workflows/ig_reels_capture_to_projection_ecr_cleaning_handoff_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/docs/workflows/ig_reels_projection_to_ecr_consumption_decision_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/docs/workflows/social_dom_json_capture_to_youtube_tiktok_handoff_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/cleaning/models.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/cleaning/projection.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/data_lake/root.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/ecr/lake.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/runners/run_source_capture_ig_reels_grid_packet.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/signal_content/lake.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/source_capture/ig_projection.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/source_capture/ig_reels_grid.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/source_capture/ig_reels_grid_capture.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/source_capture/ig_reels_grid_projection.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/source_capture/models.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/source_capture/packet_assembly.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/source_capture/writer.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/youtube_capture/README.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/youtube_capture/capture_youtube_v0.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/youtube_capture/enrich_ryd_v0.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca-harness/youtube_capture/shorts_scroll_capture_v0.py
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/capture/core/source_families/social_media/instagram/ig_capture_shape_contract_spec_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/capture/core/source_families/social_media/instagram/orca_creator_momentum_pipeline_architecture_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/capture/core/source_families/social_media/instagram/orca_creator_monitoring_policy_architecture_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_agent_playbook_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_recon_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/README.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
?? _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/sources/orca/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0.zip
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/SOURCE_MANIFEST.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/START_HERE_CHATGPTPRO_PROMPT.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/.agents/workflow-overlay/README.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/.agents/workflow-overlay/source-loading.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/AGENTS.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/core_spine/core_spine_v0_cleaning_spine_foundation_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/core_spine_v0_projection_doctrine_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/data_capture_spine/data_capture_spine_intake_surface_consolidation_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/data_capture_spine/demand_durability_indicator_availability_restock_capture_profile_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/data_capture_spine/demand_durability_indicator_price_timeseries_capture_profile_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/data_capture_spine/demand_durability_indicator_review_velocity_corpus_capture_profile_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/data_capture_spine/orca_capture_projection_storage_spine_architecture_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/data_capture_spine/orca_creator_monitoring_policy_architecture_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/data_capture_spine/source_capture_packet_schema_evolution_architecture_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/ecr/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/ecr/ecr_consolidation_v0_jsg01_evidence_unit_binding_slice_plan_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/ecr/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/signal_content/core_spine_v0_signal_content_record_architecture_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/signal_content/signal_content_record_deriver_architecture_plan_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/source_capture_toolbox/ig_capture_shape_contract_spec_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/source_capture_toolbox/ig_creator_roster_frontier_ledger_spec_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/source_capture_toolbox/reddit_packet_consolidation_runner_structural_spec_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/product/source_capture_toolbox/retail_pdp_projection_playbook_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/workflows/data_capture_spine_consolidation_map_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/docs/workflows/ecr_spine_submap_v0.md
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/ecr/deriver.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/ecr/models.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/evidence_binding/composer.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/evidence_binding/models.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/evidence_binding/verifier.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/runners/run_source_capture_ig_calls_packet.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/signal_content/deriver.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/signal_content/models.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/source_capture/ig_momentum_harvest.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/source_capture/models.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/source_capture/reddit_projection.py
?? _scratch/chatgptpro_data_lake_architecture_pass_v0/sources/orca-harness/source_capture/retail_pdp_projection.py
?? _scratch/ig_reels_diag_esthertakumi/manifest.json
?? _scratch/ig_reels_diag_esthertakumi/raw/01_ig_reels_grid_capture.json
?? _scratch/ig_reels_diag_esthertakumi/receipt.md
?? _scratch/ig_reels_pinprobe_jeremyfragrance/manifest.json
?? _scratch/ig_reels_pinprobe_jeremyfragrance/raw/01_ig_reels_grid_capture.json
?? _scratch/ig_reels_pinprobe_jeremyfragrance/receipt.md
?? _scratch/manual_lake_root_probe/.orca-data-root
?? _scratch/manual_lake_root_probe/.staging/01KVQGPGY4WWNYEHQDJRMSVEX0/probe.txt
?? _scratch/manual_lake_write_probe/stage_plain/probe.txt
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0.zip
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0/README_FOR_CHATGPT_PRO.md
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0/sources/.agents/workflow-overlay/product-proof.md
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0/sources/docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0/sources/docs/decisions/orca_product_thesis_consumer_demand_v0.md
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0/sources/orca/product/spines/foundation/product_contract/core_spine_v0_product_contract.md
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0/sources/orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0/sources/orca/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0/sources/orca/product/spines/product_lead/proof_charter/orca_claim_defense_doctrine_v0.md
?? _scratch/orca_vc_positioning_chatgpt_pro_pack_v0/sources/orca/product/spines/product_lead/proof_charter/orca_product_proof_lead_charter_v0.md
?? _scratch/precompact_creator_signal_data_lake_v0.md
?? _scratch/precompact_ig_reels_capture_v0.md
?? docs/hygiene/cleaning_spine_lane_handoff_v0.md
?? docs/hygiene/commission_signal_board_lane_handoff_v0.md
?? docs/hygiene/creator_ledger_placement_eli5_handoff_v0.md
?? docs/hygiene/data_lake_v4_1_silver_vault_precompact_v0.md
?? docs/hygiene/orca_creator_signal_idea_viability_lane_handoff_v0.md
?? docs/hygiene/orca_signal_naming_brand_architecture_handoff_v0.md
?? docs/hygiene/social_capture_browser_calibration_lane_handoff_v0.md
?? docs/prompts/deep-thinking/creator_intelligence_sync_foundation_chatgptpro_prompt_v0.md
?? docs/prompts/deep-thinking/creator_ledger_cross_platform_identity_architecture_prompt_v0.md
?? docs/prompts/deep-thinking/full_system_name_aura_review_prompt_v0.md
?? docs/prompts/patches/fused_delegated_review_gate_tightening_patch_prompt_v0.md
?? docs/prompts/product-planning/orca_spine_first_target_structure_controller_prompt_v0.md
?? docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md
?? docs/workflows/data_lake_r2_continuation_handoff_v0.md
?? docs/workflows/ig_reels_projection_to_ecr_consumption_decision_v0.md
?? orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
?? orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md
?? worktrees/creator-ledger-static-fixture/
?? worktrees/ecr-loader-review/
?? worktrees/ig-reel-deep-capture-codex/
?? worktrees/ig-reels-extract-routine/
?? worktrees/ig-reels-projection-residuals-pr/
?? worktrees/pr380-ci-fix/
?? worktrees/pr380-updated-merge-test/
?? worktrees/scanning-fragrance-commission/
?? worktrees/search-surface-mgt-p0-captures/
?? worktrees/youtube-downstream-ecr-cleaning/
```

- Target files or artifacts:
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md`
  - `docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md`
  - `docs/hygiene/data_lake_v4_1_silver_vault_precompact_v0.md`
- Related worktrees or branches:
  - Many untracked `worktrees/` folders exist in this workspace. Treat as unrelated unless owner redirects.

## Changed / Inspected / Tested Files

- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md`
  - Status: tracked modified.
  - Role: Binding physicality contract with v4.1 note.
  - Important observations: v4.1 keeps committed slots `raw/ attachments/ derived/ acknowledgements/ indexes/`; `.staging/` and markers live in the v4.1 forward-epoch contract; generic medallion storage folders are forbidden.
  - Sections: `v4.1 Forward Epoch Note`, `Directory Slot Contract`.
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
  - Status: untracked new.
  - Role: v4.1 Silver Vault record contract and Creator Vault generated-read-layer contract.
  - Important observations: authoritative records live under `derived/<anchor_shard>/<raw_anchor>/<lane_namespace>/<record_id>.json`; generated read models live under `indexes/derived_retrieval/silver_vault/...`; record meaning lives inside record header/payload, not path.
  - Sections: `Decision In One Screen`, `Derived Record Placement`, `Common Record Header`, `Observation Payloads`, `Creator Vault Envelope Guardrails`, `Acceptance Criteria`.
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md`
  - Status: untracked new.
  - Role: clean forward epoch contract.
  - Important observations: do not compatibility-migrate old small lake by default; initialize clean v4.1 root; no physical `bronze/`, `silver/`, `gold/` tiers.
  - Sections: `v4.1 Physical Folder Grammar`, `Forward Writer Obligations`, `Old Lake Handling`, `Relationship To Existing Contracts`.
- `docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md`
  - Status: untracked new.
  - Role: cold-lane handoff for read-only runner data-lake dump audit.
  - Important observations: audit lane must not edit Silver Vault schema, must not write to `F:\orca-data-lake`, and should prove which runners write v4.1-compatible raw/derived/index refs.
  - Sections: `Goal Handoff`, `Drift Guard`, `Mutable Questions`, `Do Not Forget`.
- Binding docs inspected:
  - `core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md`: says not to collapse layers into generic bronze/silver/gold storage tiers.
  - `core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md`: derived is append-only one-record-per-file; `indexes/derived_retrieval` is rebuildable, non-authoritative.

## Frozen Decisions

- Decision: v4.1 is a clean forward epoch, not a compatibility migration.
  - Evidence: user explicitly accepted archiving/abandoning old small lake; v4.1 forward contract records this.
  - Consequence: old records should not shape the forward schema; recapture under v4.1 is preferred.
- Decision: physical folders remain canonical `raw/`, `attachments/`, `derived/`, `acknowledgements/`, `indexes/`; medallion words are labels only.
  - Evidence: medallion contract lines 81-82 say not to collapse into generic storage tiers; physicality and v4.1 docs now repeat this.
  - Consequence: no `bronze/`, `silver/`, or `gold/` top-level folders.
- Decision: Silver Vault authority is append-only derived records; Creator Vault/envelopes/query tables are generated read models.
  - Evidence: Silver Vault contract maps authority to `derived/...` and retrieval to `indexes/derived_retrieval/silver_vault/...`.
  - Consequence: Creator Vault can be carved out/synced as a generated public-evidence read layer, but it is not source of truth and not Gold.
- Decision: corrections/conflicts are records/relations, not rewrites.
  - Evidence: derived-layout supersession model and Silver Vault record contract.
  - Consequence: latest/winner views are generated-only.

## Mutable Questions

- Question: Which exact runner/code path should first implement v4.1 sharded raw/derived/index refs?
  - Why still mutable: separate runner audit has not run.
  - What would resolve it: execute the handoff in `docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md`.
- Question: Should the current external old lake be renamed, left read-only, or deleted later?
  - Why still mutable: no operator action chosen; no live write permitted from this lane.
  - What would resolve it: explicit operator decision after backup/archive policy.
- Question: When should docs be committed/PR'd?
  - Why still mutable: precompact stops work now; worktree has many unrelated untracked files.
  - What would resolve it: post-compact recovery plus scoped staging of only relevant files, or owner redirect.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: physical `bronze/`, `silver/`, and `gold/` folders.
  - Why stale or dangerous: conflicts with binding medallion contract and owner's correction about unnecessary ceremony/latency.
  - Current replacement: canonical physical slots plus medallion labels only.
- Stale instruction, idea, artifact, or finding: unqualified `raw/<packet_id>` as v4.1 physical path.
  - Why stale or dangerous: v4.1 forward root is sharded as `raw/<packet_shard>/<packet_id>/`.
  - Current replacement: say logical slot `raw/`; v4.1 physical raw refs use packet shard.
- Stale instruction, idea, artifact, or finding: treating current small lake as needing compatibility migration.
  - Why stale or dangerous: user accepts old data is small/weak and long-term compounding matters more.
  - Current replacement: archive/abandon old root by explicit operator decision; recapture under v4.1.

## Commands And Validation Evidence

- Command:
  ```powershell
  rg -n "legacy sharded root|legacy `raw/<shard>|repo code/tests as legacy evidence|Forward v4.1 root shape remains|existing derived grammar|bronze/raw|silver/authority|silver/retrieval|gold/judgment|bronze/ ->|silver/ ->|gold/   ->|gold/judgment_outputs" "orca/product/spines/data_lake/authority" "docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md"
  ```
  Result:
  - Passed/failed/not run: passed for the intended check; `rg` exit 1 means no stale-pattern matches.
  - Important output:
    ```text
No matches (rg exit 1).
    ```

- Command:
  ```powershell
  git diff --check -- "orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md"
  ```
  Result:
  - Passed/failed/not run: exit 0.
  - Important output:
    ```text
warning: in the working copy of 'orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md', LF will be replaced by CRLF the next time Git touches it
    ```

- Command:
  ```powershell
  Get-FileHash -Algorithm SHA256 <material sources>; (Get-Content <file>).Count
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output:
    ```text
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md` | lines=422 | sha256=ABB8B54E1A0140278CED782D096A8F889690F74F53CE8A57B65D953E5F04E748
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md` | lines=541 | sha256=83DA3A6ECD5EDD87DD67AC26BBFBC7946591A0544483261ED29C8776B2052EDA
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md` | lines=313 | sha256=16FAB2019CC4B151FA2C2FDD502DFED6279582BB77526CEA9B6FFAE6685E1C9A
- `docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md` | lines=427 | sha256=F2F69D8577549C603007F043F14C9D07E1CFF67C1EAD91A44D3FA14305D5E576
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md` | lines=344 | sha256=5664051651B348959254AE6913F9274EAF67280022B42BBC618BC5A375D4D5EE
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md` | lines=201 | sha256=4587AAC7D44DC4FB12E0C5C4A7FCDFC96432FECBD42062A9706054EF3A2B6391
- `.agents/workflow-overlay/README.md` | lines=38 | sha256=7A30709D6011BD3F6458E926570B7164B91C7F3BF8BAE7DBD5A612A08DE81FDA
- `.agents/workflow-overlay/artifact-folders.md` | lines=420 | sha256=42D4F554DAF4BE6F0A4A9BCBE3C67FD74EEFCC063FC72B03E53E11242EDC7AE9
- `.agents/workflow-overlay/decision-routing.md` | lines=189 | sha256=8CA8069E20C5803A1B645921ABBD986656739C943ED0996572E26A4B9430092E
- `AGENTS.md` | lines=95 | sha256=4296E7617D8B2675881780CD7BE0704A00DCB17ADF7758243008DE956070940B
    ```

- Command:
  ```powershell
  git status --porcelain=v1 -uall
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: exact before/after status recorded in Workspace State.

## Blockers And Risks

- Blocker or risk: runtime writers are not yet v4.1-compliant.
  - Evidence: handoff records current `DataLakeRoot` unsharded literals vs v4.1 sharded target.
  - Likely next action: run read-only runner audit, then patch bounded writer paths under explicit implementation authorization.
- Blocker or risk: accidental old-lake mutation.
  - Evidence: v4.1 contract says not a live archive/delete operation; no operator action has been approved.
  - Likely next action: require explicit operator decision/escalation before touching `F:\orca-data-lake`.
- Blocker or risk: unrelated dirty/untracked workspace files could be accidentally staged.
  - Evidence: exact status includes many unrelated `_scratch`, `docs/hygiene`, and `worktrees` files.
  - Likely next action: stage only the four relevant docs plus checkpoint only if intentionally committing checkpoint; otherwise leave checkpoint uncommitted.

## Recovery Instructions

- Required checks:
  - Verify workspace is `C:\Users\vmon7\Desktop\projects\orca`.
  - Verify branch is `codex/ig-reels-capture-spine` and HEAD is `f95c33ae4162464354a33cd07be557d2eedc6c89`, or mark `STALE_REREAD_REQUIRED`.
  - Verify target file hashes from the Source-read ledger, or reread changed target files before reuse.
  - Verify dirty state has not acquired conflicting edits in the four target docs.
  - Rerun stale-pattern search before claiming final spec consistency.
- Recovery outcomes:
  - `REUSE`: branch/head/material target file hashes match, and dirty state drift is only optional/unrelated.
  - `PARTIAL_REUSE`: unrelated scratch/worktree drift exists; reread target docs and continue.
  - `STALE_REREAD_REQUIRED`: any binding source or target doc changed; reread medallion/physicality/derived/v4.1/Silver docs.
  - `BLOCKED_DRIFT`: target docs contain conflicting unknown edits or branch/head drift makes ownership ambiguous.
- Sources that must be reread if drift is detected:
  - `AGENTS.md`
  - `.agents/workflow-overlay/README.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
  - `docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md`

## Do Not Forget

- Do not say v4.1 means `bronze/`, `silver/`, or `gold/` folders. It means canonical `raw/`, `derived/`, `indexes/` with medallion labels.
- Do not let per-reel/detail captures overwrite grid-primary metric observations unless an explicit selection-policy/supersession rule changes.
- Do not turn Creator Vault into a person dossier or Gold/Judgment layer.
- Do not continue work after writing this checkpoint; the user asked for precompact.