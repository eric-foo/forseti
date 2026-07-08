# Source Manifest - Orca Data-Lake Architecture Pass v0

Generated from local `origin/main` at commit `ede2dca7`.

This is a bounded source pack for an external, no-repo ChatGPT Pro architecture-planning pass. It is not an Orca source-of-truth artifact, not validation evidence, and not owner adoption of any architecture.

## Authority / Boundary Sources

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`

## Lake / Capture / Projection / Cleaning Sources

- `docs/product/data_capture_spine/orca_capture_projection_storage_spine_architecture_v0.md`
- `docs/product/data_capture_spine/source_capture_packet_schema_evolution_architecture_v0.md`
- `docs/product/data_capture_spine/data_capture_spine_intake_surface_consolidation_v0.md`
- `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `docs/product/core_spine_v0_projection_doctrine_v0.md`
- `docs/product/core_spine/core_spine_v0_cleaning_spine_foundation_v0.md`

## ECR / Signal Content / Evidence Binding Sources

- `docs/workflows/ecr_spine_submap_v0.md`
- `docs/product/ecr/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md`
- `docs/product/ecr/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md`
- `docs/product/ecr/ecr_consolidation_v0_jsg01_evidence_unit_binding_slice_plan_v0.md`
- `docs/product/signal_content/core_spine_v0_signal_content_record_architecture_v0.md`
- `docs/product/signal_content/signal_content_record_deriver_architecture_plan_v0.md`

## Source-Family / Tenant Stress Cases

- `docs/product/source_capture_toolbox/ig_capture_shape_contract_spec_v0.md`
- `docs/product/data_capture_spine/orca_creator_monitoring_policy_architecture_v0.md`
- `docs/product/source_capture_toolbox/ig_creator_roster_frontier_ledger_spec_v0.md`
- `docs/product/source_capture_toolbox/retail_pdp_projection_playbook_v0.md`
- `docs/product/source_capture_toolbox/reddit_packet_consolidation_runner_structural_spec_v0.md`
- `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md`
- `docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md`
- `docs/product/data_capture_spine/demand_durability_indicator_price_timeseries_capture_profile_v0.md`
- `docs/product/data_capture_spine/demand_durability_indicator_review_velocity_corpus_capture_profile_v0.md`
- `docs/product/data_capture_spine/demand_durability_indicator_availability_restock_capture_profile_v0.md`

## Implementation Reality Sources

- `orca-harness/source_capture/models.py`
- `orca-harness/source_capture/ig_momentum_harvest.py`
- `orca-harness/runners/run_source_capture_ig_calls_packet.py`
- `orca-harness/source_capture/retail_pdp_projection.py`
- `orca-harness/source_capture/reddit_projection.py`
- `orca-harness/ecr/models.py`
- `orca-harness/ecr/deriver.py`
- `orca-harness/signal_content/models.py`
- `orca-harness/signal_content/deriver.py`
- `orca-harness/evidence_binding/models.py`
- `orca-harness/evidence_binding/composer.py`
- `orca-harness/evidence_binding/verifier.py`

## Source-Use Notes

- The storage backbone is explicitly `PROPOSED`; do not treat it as adopted.
- `MetricObservation` exists in current code, but it is an IG typed-capture substrate, not a whole-lake schema.
- ECR/SCR/evidence-binding code exists and is useful for current derivation grain and keying reality.
- Cleaning foundation currently points to a raw-keyed input handle with optional projection and ECR references.
- Projection doctrine treats projection as a rebuildable view over raw, not a new source of truth.
- Source-family examples are included to stress tenant neutrality: IG metrics, Reddit thread projection, Retail PDP projection, and demand-durability series profiles.

