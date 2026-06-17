# Spine-First Target Move Table v0

```yaml
retrieval_header_version: 1
artifact_role: Orca migration inventory record (move-table marking artifact)
scope: >
  Reconciled move-table package for the spine-first product reorganization. One
  row per candidate file or file family: current path -> target path, move class,
  owner/role, rationale, required reference rewrites, blockers, confidence, and
  file:line citation. Reconciles the two committed per-lane inventories (capture,
  search) with three fresh controller inventory passes (foundation/core-spine,
  judgment, product-lead/ecr/signal-content). Inventory only: move_now = no for
  every row; no file moved, renamed, created, or deleted; no code/tests/imports
  touched.
use_when:
  - Sequencing the spine-first migration execution.
  - Looking up the proposed target home of a current product file.
  - Reconciling a sibling per-lane inventory against the bound target tree.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_spine_first_target_structure_binding_v0.md
  - docs/migration/spine_first_untagged_file_inventory_v0.md
  - docs/migration/capture_spine_source_capture_migration_inventory_v0.md
  - docs/migration/search_demand_signal_migration_inventory_v0.md
stale_if:
  - The bound target tree or a convention in the spine-first binding changes.
  - A sibling per-lane inventory lands on main and re-classifies a shared surface.
  - docs/product/ membership changes (a doc is added, removed, or re-homed).
```

## Status & base

- Status: `INVENTORY_ONLY_V0` — proposals; `move_now: no` for every row.
- Base: read against `origin/main @ 8f19b460` (controller HEAD == origin/main,
  clean). Pending sibling-branch inventories are **not** assumed merged.
- Authority: the target homes are bound by
  `docs/decisions/orca_spine_first_target_structure_binding_v0.md`. On conflict
  that binding (and the owner) govern; this table is the reconciled reading.
- Move classes: `direct_move` | `split_needed` | `historical_keep` |
  `process_keep` | `runtime_defer` | `needs_main_ca_tag` | `reject_false_positive`.
- `historical_keep` / `process_keep` = stays at a current by-type home (decisions,
  prompts, reviews, research, workflows, migration); it does **not** move into
  `orca/product/`. `runtime_defer` = `orca-harness/` code, left in place.
- Counts reconciled: 218 `docs/product/` files (capture 109 + search 11 via
  committed inventories; core_spine 47 + judgment 29 + product_lead 14 + ecr 3 +
  signal_content 2 + 2 root + README via fresh passes) + the `docs/` top-level
  reshape + the `orca-harness/` runtime defer.

## Section 0 — Root layout & docs/ reshape (highest-salience blockers)

| Current | Target | Class | Conf | Cite | Rationale / refs / blockers |
| --- | --- | --- | --- | --- | --- |
| *(new top-level dir)* `orca/` | `orca/` | `needs_main_ca_tag` | high | `repo-structure.yaml:23-30` | **B1.** `known_top_level.dirs` lacks `orca`; absent on origin/main. Execution blocked until the machine map authorizes the root. Ref rewrite: `repo-structure.yaml` + `artifact-folders.md`. |
| `docs/product/` (whole tree) | `orca/product/` | `split_needed` | high | `.agents/workflow-overlay/artifact-folders.md:34` | The by-lane `docs/product/` axis is replaced by the `orca/product/` spine axis. Massive ref rewrites across repo map, submaps, harness docs. |
| *(new)* `docs/doctrine/` | `docs/doctrine/` | `needs_main_ca_tag` | low | `docs/decisions/orca_doctrine_index_v0.md` exists | **B3.** Target adds `doctrine/` while keeping `decisions/`; no source defines the boundary. Doctrine index already in `decisions/`. |
| `docs/decisions/`, `docs/workflows/`, `docs/prompts/`, `docs/review-inputs/`, `docs/review-outputs/`, `docs/research/`, `docs/migration/`, `docs/hygiene/`, `docs/_inbox/`, `docs/README.md`, `docs/STRUCTURE.md` | unchanged | `process_keep` | high | `repo-structure.yaml:39-49` | By-type docs roles persist in the target tree; only `docs/product/` is dropped. |
| `orca-harness/**` (all runtime, tests, schemas, runners, adapters) | `orca-harness/**` (unchanged) | `runtime_defer` | high | capture inv §4 (`docs/migration/capture_spine_source_capture_migration_inventory_v0.md:96-107`) | Foregone limitation: runtime stays until a global runtime-mapping decision. Spine names under `orca/product/spines/` mirror but do not relocate harness subtrees. |

## Section 1 — Foundation (`orca/product/spines/foundation/`)

Source: fresh foundation/core-spine pass. All paths under `docs/product/core_spine/`
unless noted.

| Current | Target | Class | Conf | Cite | Rationale / blockers |
| --- | --- | --- | --- | --- | --- |
| `core_spine_v0_product_contract.md` | `foundation/product_contract/` | `direct_move` | high | `…product_contract.md:1-6` | Canonical market-agnostic product contract. |
| `core_spine_v0_information_production_foundation_v0.md` | `foundation/product_contract/` | `direct_move` | high | `…information_production_foundation_v0.md:16-18` | IPF/Evidence-Unit standard; the "evidence_standard" concept (target `foundation/evidence_standard/` slot is otherwise empty — see note). |
| `core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | `foundation/product_contract/` | `direct_move` | high | `…data_and_cleaning_spine_boundary_v0.md:12-13` | Multi-spine boundary note governing all spines from foundation. |
| `core_spine_v0_proof_protocol_v0.md` | `foundation/product_contract/` | `direct_move` | high | `…proof_protocol_v0.md:18-20` | Proof METHOD (gates for all runs), not a corpus. |
| `core_spine_v0_proof_input_selection_v0.md` | `foundation/product_contract/` | `needs_main_ca_tag` | medium | `…proof_input_selection_v0.md:13-30` | Protocol-definition vs proof-setup; see untagged U-F1. |
| `core_spine_v0_proof_packet_preflight_v0.md` | `foundation/product_contract/` | `needs_main_ca_tag` | medium | `…proof_packet_preflight_v0.md:28` | Readiness-gate machinery vs corpus; U-F1. |
| `core_spine_v0_method_validation_rubric_v0.md` | `foundation/product_contract/` | `needs_main_ca_tag` | medium | `…method_validation_rubric_v0.md:18` | Method-definition vs validation-machinery; U-F1. |
| `orca_ontology_backbone_architecture_v0.md` | `foundation/ontology/` | `direct_move` | high | `…orca_ontology_backbone_architecture_v0.md:16` | Naming-normative ontology backbone (ADOPTED). |
| `ontology_expansion_backlog_v0.json` | `foundation/ontology/` | `needs_main_ca_tag` | high | `…ontology_expansion_backlog_v0.json:3` | **B4.** Read by `.agents/hooks/check_ontology_expansion.py`; move requires a paired hook-path rewrite (runtime-adjacent). |
| `ontology_cards/` (README + brand_beautypie, case/decision/outcome_beautypie_repricing_2023, venue_basenotes, vertical_beauty) | `foundation/ontology/ontology_cards/` | `needs_main_ca_tag` | medium | `ontology_cards/README.md:12` | Beauty/fragrance instance cards: foundation/ontology vs `satellites/beauty/`. See untagged U-F2. |
| `orca_vertical_exploration_guide_v0.md` | `foundation/vertical_exploration/` | `direct_move` | high | `…orca_vertical_exploration_guide_v0.md:5-6` | Market-agnostic WHERE-side procedure. |
| `orca_memorization_resistant_case_finder_frame_v0.md` | `foundation/vertical_exploration/` | `direct_move` | high | `…orca_memorization_resistant_case_finder_frame_v0.md:8-9` | Vertical-agnostic case-finder doctrine. |
| *(from search lane)* `orca_demand_read_taxonomy_v0.md`, `orca_demand_read_taxonomy_adjudication_v0.md` | `foundation/demand_read_taxonomy/` | `direct_move` | high | search binding `…orca_search_product_lane_binding_v0.md:99-104` | Search dissolution: the demand-read grammar (see Section 3a). |

Empty/under-populated target slots: `foundation/evidence_standard/` (IPF covers
the standard but no separate doc), `foundation/shared_primitives/` (no current
doc maps cleanly) — flagged for owner as structure-ahead-of-content.

## Section 2 — Cleaning (`orca/product/spines/cleaning/`)

| Current (`docs/product/core_spine/`) | Target | Class | Conf | Cite | Rationale |
| --- | --- | --- | --- | --- | --- |
| `core_spine_v0_cleaning_spine_foundation_v0.md` | `cleaning/contracts/` | `direct_move` | high | `…cleaning_spine_foundation_v0.md:4-9` | Cleaning layer contract. |
| `core_spine_v0_cleaning_spine_readme_v0.md` | `cleaning/contracts/` | `direct_move` | high | `…cleaning_spine_readme_v0.md:5` | Cleaning entrypoint, pairs with foundation. |
| `core_spine_v0_corroboration_vs_amplification_discipline_v0.md` | `cleaning/contracts/` | `direct_move` | high | `…corroboration_vs_amplification_discipline_v0.md:8` | Cleaning/Judgment dedup-vs-independence discipline. |

`cleaning/{transformations,integrity_labels,normalization}/` are empty target
slots (no current doc); structure-ahead-of-content. The cleaning runtime
(`orca-harness/cleaning/`) is `runtime_defer`.

## Section 3 — Scanning (`orca/product/spines/scanning/`)

### 3a — Search-lane dissolution (high-salience; reverses #236/#241)

All currently under `docs/product/search/`. See binding §"Search-dissolution
policy" and Blocker B2.

| Current (`docs/product/search/`) | Target | Class | Conf | Cite | Rationale / blockers |
| --- | --- | --- | --- | --- | --- |
| `orca_demand_scan_core_spec_v0.md` | `scanning/scan_core/` | `direct_move` | high | `…orca_demand_scan_core_spec_v0.md:614` | The scan method ("makes the gate's columns fillable"). |
| `orca_demand_read_taxonomy_v0.md` | `foundation/demand_read_taxonomy/` | `direct_move` | high | search inv §3 (`…search_demand_signal_migration_inventory_v0.md:168`) | Demand-read grammar (venue-spanning; authority preserved). |
| `orca_demand_read_taxonomy_adjudication_v0.md` | `foundation/demand_read_taxonomy/` | `direct_move` | high | same | Adjudication companion to the taxonomy. |
| `orca_demand_scan_gate_adjudication_packet_v0.md` | `scanning/admissibility_checkability/` | `direct_move` | medium | `…orca_demand_scan_gate_adjudication_packet_v0.md:192-193` | Gate packaging/location (consumes the ratified gate). |
| `orca_demand_gate_definition_closures_proposal_v0.md` | `scanning/admissibility_checkability/` | `split_needed` | medium | `…orca_demand_gate_definition_closures_proposal_v0.md:27-28` | Gate definitions align with the buyer-proof Hard Gate (`product_lead/buyer_proof/`); admissibility columns side -> scanning. Convention 3. |
| `orca_demand_gate_run_commission_criteria_v0.md` | `commission_signal_board/` (or `scanning/admissibility_checkability/`) | `needs_main_ca_tag` | low | `…orca_demand_gate_run_commission_criteria_v0.md:35` | **B5.** Functional CSB precursor; only artifact approximating CSB. See Section 11. |
| `aeo_capture_feasibility_probe_phase0_v0.md` | `scanning/source_families/answer_engine/` | `direct_move` | medium | search inv §1 (`…search_demand_signal_migration_inventory_v0.md:77`) | Answer-engine surface feasibility probe. |
| `aeo_capture_feasibility_probe_phase0_v0_evidence.json` | `scanning/source_families/answer_engine/` | `direct_move` | medium | same | Evidence sidecar to the AEO probe (moves with it). |
| `demand_search_interest_sourcing_and_gate_delta_spec_v0.md` | `scanning/source_families/answer_engine/` | `split_needed` | medium | `…orca_search_product_lane_binding_v0.md:94` | Search-interest/AEO source-classes + gate-read placement; touches capture search_interest profile. |
| `demand_durability_indicator_search_interest_capture_profile_v0.md` | `capture/demand_durability_indicators/search_interest/` | `direct_move` | high | `…orca_search_product_lane_binding_v0.md:95` | Convention 2 — capture owns the search-interest indicator. |
| `README.md` | *(dissolved)* | `needs_main_ca_tag` | medium | search inv §1 (`…:75`) | The `search/` lane README has no target home (lane dissolves); content may seed scanning/ + foundation READMEs or be retired. |

### 3b — Scanning source-families (discovery side)

| Current | Target | Class | Conf | Cite | Rationale |
| --- | --- | --- | --- | --- | --- |
| `data_capture_spine/data_capture_spine_linkedin_*` (4: discovery_planning_lane, lane_index, influence_trajectory_watch_spec, live_layer_architecture) | `scanning/source_families/linkedin/` | `split_needed` | medium | capture inv §3,§8 (`…capture_spine_source_capture_migration_inventory_v0.md:90,137`) | LinkedIn is no-live, planning-only, **upstream discovery** -> scanning, NOT capture. live_layer_architecture may straddle capture; tag. |
| `data_capture_spine/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md` | `scanning/source_families/reddit/` (discovery) | `split_needed` | medium | capture inv §8 (`…:136`) | Graph-frontier = bounded discovery/planning; the candidate-intake/capture side stays capture (Section 4). |

## Section 4 — Capture (`orca/product/spines/capture/`)

Family-level rows; per-file detail is in the committed capture inventory
(`docs/migration/capture_spine_source_capture_migration_inventory_v0.md`). All
`move_now: no`. Runtime stays in `orca-harness/` (`runtime_defer`).

| Current family | Target | Class | Conf | Cite | Rationale / blockers |
| --- | --- | --- | --- | --- | --- |
| `data_capture_spine/` source-access (`data_capture_source_access_boundary_decision`, `…method_plan`) | `capture/contracts/source_access_boundary/` | `direct_move` | high | capture inv §1 (`…:62`) | Access boundary. |
| `data_capture_spine/` intake (`…candidate_url_intake_contract`, `…reddit_candidate_url_intake_crawler_architecture`, `…intake_surface_consolidation`) | `capture/contracts/candidate_intake/` | `direct_move` | high | capture inv §1,§8 (`…:62,135`) | Candidate URL intake. |
| `data_capture_spine/` corpus (`…corpus_intake_obligation_contract_proposal`) | `capture/contracts/corpus_intake/` | `direct_move` | high | capture inv §1 (`…:62`) | Standing/corpus capture. |
| `data_capture_spine/` obligations (`core_spine_v0_data_capture_spine_obligation_contract`, `…obligation_contract_patch_proposal`, `…posture_vocabulary_enforcement_proposal`) | `capture/contracts/obligation_contracts/` | `direct_move` | high | capture inv §1 (`…:62`) | Obligation contracts. |
| `data_capture_spine/` operating-model (`data_capture_harness_operating_model_architecture_v0/v1/v2` + `…v2_acceptance_decision` + `…product_goal_direction_signal_decision` + `data_capture_obligation_baseline_decision` + `…lane_product_thesis`) | `capture/operating_model/` | `split_needed` | medium | capture inv §1,§11.3 (`…:62,160`) | v2 current; v0/v1 superseded — archive disposition is an owner question. |
| `data_capture_spine/` payload/schema (`source_capture_packet_schema_evolution_architecture`, `source_capture_tenant_payload_attachment_boundary`, `source_capture_core_payload_split_explainer`) | `capture/packet_schema/` | `direct_move` | high | capture inv §1 (`…:62`) | Packet schema. |
| `data_capture_spine/` architecture/fixtures (`core_spine_v0_data_capture_spine_architecture_blueprint`, `…full_fixture_synthesis`, `…remaining_fixture_plan`, `…context_preservation_note`, 6 `…pressure_test_*` fixtures) | `capture/operating_model/` | `direct_move` | medium | capture inv §1 (`…:54`) | Core capture architecture. |
| `data_capture_spine/` pressure-test slot sessions (~12: slot1_mi_biws, slot2_teal, slot3 reddit/wso batches, all_slot_synthesis, closeout_synthesis, commissioning_plan, execution_authorization) | `capture/operating_model/` **or** `case_families/` | `needs_main_ca_tag` | low | capture inv §11.6 (`…:163`) | Borderline capture-evidence vs case-family. See untagged U-C1. |
| `data_capture_spine/` demand-durability venues (`demand_durability_indicator_{price_timeseries,availability_restock,review_velocity_corpus}_capture_profile`, `…capture_deconfliction_note`, `…standing_capture_obligation_home_decision_framing`, `demand_durability_multi_retailer_rendered_capture_spec`, `demand_durability_us_storefront_pin_recon_verdict`, `demand_durability_capture_pilot`, `capture_envelope_durability_delta_spec`) | `capture/demand_durability_indicators/{price_timeseries,availability_restock,review_velocity}/` | `direct_move` | high | capture inv §5,§7 (`…:115,131`) | Convention 2. search-interest excluded (Section 3a). |
| `data_capture_spine/` retail/PDP (`retail_pdp_typed_envelope_probe`) + `source_capture_toolbox/retail_pdp_*` (3) | `capture/source_families/retail_pdp/` | `direct_move` | high | capture inv §7 (`…:131`) | Retail/PDP cleanly capture-owned. |
| `data_capture_spine/` creator (`orca_creator_momentum_pipeline_architecture`, `orca_creator_monitoring_policy_architecture`) + `source_capture_toolbox/ig_*` (13) | `capture/source_families/instagram/` | `needs_main_ca_tag` | low | capture inv §6 (`…:121-127`) | **B6.** IG unmarked (no lane binding); held under Capture/Toolbox today. See untagged U-C2. |
| `source_capture_toolbox/` (45 docs, the Armory subsystem incl. README, playbook, recon-index, anti-block ladder, CloakBrowser, reddit ×4, archive ×3, source-quality ×7) | `capture/source_capture_toolbox/` | `direct_move` (as a unit) | high | capture inv §2 (`…:70-82`) | Adopt as a named subsystem. **B6** Toolbox-vs-Armory canonical name = owner decision. |
| `data_capture_spine/data_capture_spine_future_exploration_lanes_v0.md` | `capture/` (spine root) | `direct_move` | medium | capture inv §1 (`…:62`) | Capture-spine backlog. |

ECR/Cleaning/Judgment downstream interfaces named in the capture inventory (§9)
migrate with **their** spines, not capture.

## Section 5 — ECR + Signal Content (`orca/product/spines/ecr/`)

Source: fresh product-lead/ecr/signal-content pass.

| Current | Target | Class | Conf | Cite | Rationale |
| --- | --- | --- | --- | --- | --- |
| `docs/product/ecr/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md` | `ecr/evidence_candidate_record/` | `direct_move` | high | `…frame_source_visibility_slice_architecture_plan_v0.md:4` | ECR frame + SP-6 slice. |
| `docs/product/ecr/ecr_consolidation_v0_jsg01_evidence_unit_binding_slice_plan_v0.md` | `ecr/evidence_candidate_record/` | `direct_move` | high | `…jsg01_evidence_unit_binding_slice_plan_v0.md:4` | JSG-01 EvidenceUnit binding slice. |
| `docs/product/ecr/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md` | `ecr/evidence_candidate_record/` | `direct_move` | high | `…sp1_sp2_sp3_source_side_slice_plan_v0.md:4` | SP-1/2/3 source-side reconcile. |
| `docs/product/signal_content/core_spine_v0_signal_content_record_architecture_v0.md` | `ecr/signal_content/` | `direct_move` | high | `…signal_content_record_architecture_v0.md:3` | SCR direction (under ECR per foregone-limitations). |
| `docs/product/signal_content/signal_content_record_deriver_architecture_plan_v0.md` | `ecr/signal_content/` | `direct_move` | high | `…signal_content_record_deriver_architecture_plan_v0.md:4` | SCR deriver plan. |

## Section 6 — Judgment (`orca/product/spines/judgment/`)

Source: fresh judgment pass. All under `docs/product/judgment_spine/`. All 29
classified; none untagged.

| Current | Target | Class | Conf | Cite |
| --- | --- | --- | --- | --- |
| `judgment_quality_promotion_operating_model_v0.md` | `judgment/conductor/` | `direct_move` | high | `…:6` |
| `conductor_construction_integrity_probe_addendum_v1.md` | `judgment/conductor/` | `direct_move` | high | `…:3` |
| `conductor_construction_integrity_probe_addendum_proposal_v0.md` | `judgment/conductor/` (or archive) | `needs_main_ca_tag` | medium | `…proposal_v0.md:30-33` |
| `judgment_spine_gate_ownership_map_v0.md` | `judgment/conductor/` | `direct_move` | high | `…:6` |
| `judgment_spine_reveal_calibration_owner_contract_v0.md` | `judgment/conductor/` (vs `…/product_learning/reveal_evaluation/`) | `needs_main_ca_tag` | medium | `…:6` |
| `judgment_current_state_and_decomposition_v0.md` | `judgment/conductor/` (vs judgment root) | `needs_main_ca_tag` | medium | `…:5-6` |
| `judgment_spine_evidence_ladder_architecture_v0.md` | `judgment/claim_ladder/` | `direct_move` | high | `…:6` |
| `judgment_spine_demand_read_machinery_architecture_v0.md` | `judgment/demand_read/core/` | `direct_move` | high | `…:6` |
| `demand_read_core_adoption_and_ledger_first_direction_v0.md` | `judgment/demand_read/core/` | `direct_move` | high | `…:5,17` |
| `judgment_spine_first_demand_read_scope_v0.md` | `judgment/demand_read/core/` | `direct_move` | medium | `…:5` |
| `judgment_spine_c2_ledger_read_contract_v0.md` | `judgment/demand_read/c2_weighting/` | `direct_move` | high | `…:5` |
| `judgment_spine_c2_qualitative_read_feasibility_probe_v0.md` / `_v1.md` / `_v2.md` | `judgment/demand_read/c2_weighting/` | `direct_move` | high | `…v2.md:5` |
| `judgment_spine_c2_rule3_reground_phase_a_classification_finding_v0.md` | `judgment/demand_read/c2_weighting/` | `direct_move` | high | `…:5` |
| `judgment_spine_c3_verdict_action_ceiling_contract_v0.md` | `judgment/demand_read/c3_verdict_action/` | `direct_move` | high | `…:5` |
| `judgment_spine_demand_read_grading_rubric_v0.md` | `judgment/demand_read/grading/` | `direct_move` | high | `…:5` |
| `judgment_spine_toolkit_blocker_specs_from_daimler_source_fanout_v0.md` | `judgment/toolkit_gaps/` | `direct_move` | high | `…:6` |
| `jsg01_source_side_receipt_translator_v0.md` | `judgment/source_side_receipts/` | `direct_move` | high | `…:6` |
| `jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md` | `judgment/source_side_receipts/` | `direct_move` | high | `…:6` |
| `jsg01_sp6_source_visibility_derivation_architecture_routing_v0.md` | `judgment/source_side_receipts/` | `direct_move` | high | `…:6` |
| `near_half_signal_reliability_ledger_v0.md` | `judgment/learning_loops/near_half/` | `direct_move` | high | `…:6,24` |
| `near_half_backtest_learning_architecture_v0.md` | `judgment/learning_loops/near_half/` | `direct_move` | high | `…:6,23` |
| `prospective_decision_loop_target_architecture_v0.md` | `judgment/learning_loops/far_half/` | `direct_move` | high | `…:6,22` |
| `prospective_decision_loop_phase0_semantics_spec_v0.md` | `judgment/learning_loops/far_half/` | `direct_move` | high | `…:6,18` |
| `fragrance_level1_product_learning_reconciliation_v0.md` | `judgment/product_learning/` (vs `satellites/fragrance/judgment_level1/reconciliation/`) | `needs_main_ca_tag` | medium | `…:5,52-58` |
| `fragrance_level1_product_learning_satellite_skeleton_v0.md` | `satellites/fragrance/judgment_level1/satellite_skeleton/` | `direct_move` | high | `…:5,57` |
| `fragrance_level1_casebook_admission_frame_v0.md` | `satellites/fragrance/judgment_level1/casebook_admission/` | `direct_move` | high | `…:5,8` |
| `fragrance_level1_named_case_candidate_screen_v0.md` | `satellites/fragrance/judgment_level1/named_case_screens/` | `direct_move` | high | `…:5` |

Empty target slots (structure-ahead-of-content): `judgment/product_learning/{forecast_records,decision_logs,receipts}`, `satellites/fragrance/judgment_level1/{source_registry,evaluation_artifacts}`.

## Section 7 — Product Lead (`orca/product/spines/product_lead/`)

Source: fresh product-lead pass. All under `docs/product/product_lead/`.

| Current | Target | Class | Conf | Cite |
| --- | --- | --- | --- | --- |
| `orca_offer_hypothesis_v0.md` | `product_lead/offer/` | `direct_move` | high | `…:1` |
| `orca_offer_hypothesis_consumer_demand_revision_v0.md` | `product_lead/offer/` | `direct_move` | high | `…:1` |
| `orca_buyer_proof_packet_v0.md` | `product_lead/buyer_proof/` | `direct_move` | high | `…:138` |
| `orca_buyer_proof_packet_consumer_demand_revision_v0.md` | `product_lead/buyer_proof/` | `direct_move` | high | `…:1` |
| `orca_product_proof_lead_charter_v0.md` | `product_lead/proof_charter/` | `direct_move` | high | `…:5` |
| `orca_product_proof_lead_charter_consumer_demand_revision_v0.md` | `product_lead/proof_charter/` | `direct_move` | high | `…:1` |
| `orca_product_lead_first_icp_wedge_decision_v0.md` | `product_lead/icp_wedge/` | `direct_move` | high | `…:4` |
| `orca_icp_ratification_readiness_report_v0.md` | `product_lead/icp_wedge/` | `needs_main_ca_tag` | medium | `…:4` |
| `orca_discovery_consumer_demand_target_selection_brief_v0.md` | `product_lead/icp_wedge/` | `needs_main_ca_tag` | medium | `…:4` |
| `orca_ratification_day_runbook_v0.md` | `product_lead/icp_wedge/` | `needs_main_ca_tag` | medium | `…:4` |
| `orca_claim_defense_doctrine_v0.md` | `product_lead/proof_charter/` (vs judgment) | `needs_main_ca_tag` | medium | `…:3,11` |
| `orca_discovery_batch_0_candidate_context_scan_v0.md` | `product_lead/icp_wedge/` (or archive) | `needs_main_ca_tag` | low | `…:3 (SUPERSEDED)` |
| `orca_discovery_batch_0_qualification_prep_sentry_clerk_v0.md` | `product_lead/icp_wedge/` (or archive) | `needs_main_ca_tag` | low | `…:1 (SUPERSEDED)` |
| `orca_discovery_batch_0_target_selection_brief_v0.md` | `product_lead/icp_wedge/` (or archive) | `needs_main_ca_tag` | low | `…:3 (SUPERSEDED)` |

## Section 8 — Satellites (`orca/product/satellites/`)

| Current | Target | Class | Conf | Cite | Rationale |
| --- | --- | --- | --- | --- | --- |
| `core_spine/beauty_venue_card_set_v0.md` | `satellites/beauty/` | `direct_move` | high | `…beauty_venue_card_set_v0.md:5-6,11` | Beauty-specific maintained venue asset. |
| `judgment_spine/fragrance_level1_product_learning_satellite_skeleton_v0.md` | `satellites/fragrance/judgment_level1/satellite_skeleton/` | `direct_move` | high | (Section 6) | Domain frame/skeleton. |
| `judgment_spine/fragrance_level1_casebook_admission_frame_v0.md` | `satellites/fragrance/judgment_level1/casebook_admission/` | `direct_move` | high | (Section 6) | |
| `judgment_spine/fragrance_level1_named_case_candidate_screen_v0.md` | `satellites/fragrance/judgment_level1/named_case_screens/` | `direct_move` | high | (Section 6) | |

## Section 9 — Case families (`orca/product/case_families/product_learning/`)

Source: fresh foundation/core-spine pass (corpora) + judgment pass (fragrance) +
capture inventory (case-family note).

| Current family (`docs/product/core_spine/`) | Target | Class | Conf | Cite | Rationale / blockers |
| --- | --- | --- | --- | --- | --- |
| method-validation corpus (`…method_validation_case_locks`, `…case_frame_lock_contract`, `…case_frame_locks`, `…mv01_intercom_zendesk_replay`, `…mv03_stack_overflow_chatgpt_replay`, `…mv04_unity_runtime_fee_replay`, `…mv05_reddit_api_pricing_replay`, `…mv09_thomson_reuters_casetext_replay`, `…replay_packet`) | `case_families/product_learning/other_verticals/` | `direct_move` | high | `…method_validation_case_locks_v0.md:17-21` | All SaaS/tech cases; corpus. **`other_verticals` is the catch-all** — confirm naming (U-CF1). |
| first-proof-run corpus (`…first_proof_run_locks`, `…first_proof_run_packet`, `…first_proof_run_jb_client0_slice`, `…first_proof_run_sh01_shadow_slice`, `…first_proof_run_bt204_backtest_slice`, `…first_proof_packet_preparation`) | `case_families/product_learning/other_verticals/` | `direct_move` | medium | A return | jb-slice -> `retail_pdp`? is a poor fit (finance/job board); U-CF2. |
| `…first_proof_run_charter_v0.md` | `case_families/product_learning/` (vs `foundation/product_contract/`) | `needs_main_ca_tag` | low | `…first_proof_run_charter_v0.md:1-5` | Proof-method vs corpus; U-F3. |
| heavyweight discovery (`…heavyweight_proof_case_discovery_charter`, `…results`, `…results_part_2`, `…proof_case_selection_brief`) | `case_families/product_learning/other_verticals/` | `direct_move` | medium | A return | Cross-domain candidate corpus. |
| Unity backtest specimens (`orca_backtest_specimen_unity_runtime_fee_source_packet`, `…memo_unity_runtime_fee_at_cutoff`, `…outcome_calibration`) | `case_families/product_learning/other_verticals/` | `direct_move` | high | `…outcome_calibration_v0.md:14-19` | Tight family (move together); SHA256 cross-refs need post-move rewrite. |
| `consumer_demand_candidate_pool_handoff_v0.md` | `case_families/product_learning/fragrance/` (vs `satellites/beauty/`) | `needs_main_ca_tag` | medium | `…consumer_demand_candidate_pool_handoff_v0.md:7-13` | One-shot beauty discovery handoff; U-CF3. |
| `orca-harness/cases/product_learning/` (~14 case families) + `cases/plumbing/` | *(case-family inventory owns)* | `needs_main_ca_tag` | medium | capture inv §10 (`…:151-154`) | Runtime case corpora; `runtime_defer` for the harness, but the case-family mapping is owned by a (pending) case-family inventory. |

## Section 10 — Shared (`orca/product/shared/`)

| Current | Target | Class | Conf | Cite |
| --- | --- | --- | --- | --- |
| `core_spine/core_spine_v0_data_lake_mechanics_map_v0.md` | `shared/data_lake_mechanics/` | `direct_move` | high | `…data_lake_mechanics_map_v0.md:4-8` |
| `core_spine_v0_projection_doctrine_v0.md` (root) | `shared/projection_doctrine/` | `direct_move` | high | `…core_spine_v0_projection_doctrine_v0.md:4-7` |
| `engagement_logic_registry_v0.md` (root) | `shared/engagement_registry/` | `direct_move` | high | `…engagement_logic_registry_v0.md:5` |

## Section 11 — Commission Signal Board (`orca/product/spines/commission_signal_board/`)

| Current | Target | Class | Conf | Cite | Rationale / blockers |
| --- | --- | --- | --- | --- | --- |
| *(none found)* | `commission_signal_board/{commission_contract,signal_board,dispatch_rules,work_orders}/` | `needs_main_ca_tag` | high | C gate-verification (`…orca_demand_gate_run_commission_criteria_v0.md:4`) | **B5.** No CSB doc exists; CSB is structure-not-built. Only precursor is the gate-run commission criteria (Section 3a). First CSB artifact may need authoring, or that doc relocates here. |

## Section 12 — `docs/` by-type homes (no move into `orca/product/`)

| Current | Class | Cite | Rationale |
| --- | --- | --- | --- |
| `docs/decisions/` capture/search/judgment decisions (~25+ capture-relevant) | `process_keep` | capture inv §1 (`…:58`) | Decision records stay by-type; do not move to `orca/product/`. |
| `docs/prompts/**`, `docs/review-outputs/**`, `docs/review-inputs/**` (incl. demand/scan/gate review history) | `historical_keep` | search inv §1 (`…:97-114`) | Type-filed; reference-model-B (keep + resolve via moved-paths index). |
| `docs/research/**` (org-motion, ChatGPT-Pro discovery, daimler source registry) | `historical_keep` | search inv §1 (`…:106-110`) | Research-by-type. The ChatGPT-Pro discovery artifact is the search binding's explicit exclusion. |
| `docs/workflows/**` (repo map, consolidation maps, submaps) | `process_keep` (+ heavy ref rewrites) | `repo-structure.yaml:46` | Stay; but `docs/product -> orca/product` references rewrite at execution. |
| `docs/migration/**` (incl. moved-path indexes, this table) | `process_keep` | binding Convention 5 | Convention 5 — never under `orca/product/shared/`. |

## Required reference rewrites (execution-time, summary)

- `repo-structure.yaml`: add `orca/` to `known_top_level`; add `orca/product/`
  axis; add `docs/doctrine/`; drop `docs/product/` role.
- `.agents/workflow-overlay/artifact-folders.md`: replace `docs/product/` lane
  axis with the `orca/product/` spine axis.
- `docs/workflows/orca_repo_map_v0.md` + `data_capture_spine_consolidation_map_v0.md`
  + `ecr_spine_submap_v0.md` + `judgment_spine_consolidation_map_v0.md`: bulk
  `docs/product/... -> orca/product/...` rewrites.
- `.agents/hooks/check_ontology_expansion.py`: backlog JSON path (B4).
- Unity backtest specimen trio: internal SHA256 path pointers.
- Moved docs' `open_next` / `branch_or_commit` lines; the search-lane moved-paths
  index residual (search inv §7).

## Highest-risk blockers (see binding for full text)

B1 `orca/` root unauthorized · B2 search-lane physical reversal · B3 `docs/doctrine/`
boundary · B4 ontology hook coupling · B5 CSB has no doc home · B6 Toolbox-vs-Armory
name + IG-lane status · B7 sibling inventories not on main.

## Non-claims

- Inventory only. No file moved/renamed/created/deleted; no code/tests/imports
  touched; no `orca/` tree created. Allocations are proposals (`move_now: no`).
- Not validation, readiness, proof, or migration completion.
- Does not re-decide ownership where a committed inventory or owner doc governs;
  on conflict they (and the spine-first binding) win.
- `historical_keep` / `process_keep` reflect by-type homes that persist; they are
  not claims that those files are correct, current, or accepted.
- Sibling per-lane inventories (cleaning, ecr, foundation, ontology, product-lead,
  global-prompt-review) are in-flight, not merged; re-reconcile on landing.
