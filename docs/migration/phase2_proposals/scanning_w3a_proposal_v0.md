```yaml
retrieval_header_version: 1
artifact_role: Orca migration note
scope: >
  Phase-2 W3a proposal for the scanning area (orca/product/spines/scanning/): bloat/deletion candidates with full deletion-evidence records and ontology/doc-term findings against the SSOT.
use_when:
  - Owner adjudicating Phase-2 deletion candidates for the scanning spine.
  - Reviewing ontology/doc-term drift findings for scanning-area files before a Phase-3 ratchet.
authority_boundary: retrieval_only
open_next:
  - docs/migration/orca_second_pass_consolidation_plan_v0.md
stale_if:
  - Any scanning-area file is moved, renamed, or deleted after this proposal is written (inbound ref counts change).
```

# Phase-2 W3a Proposal — scanning

## Summary

Files scanned: 11 (10 `.md` + 1 `.json`)
Deletion candidates: 0 high / 0 medium / 0 low
Ontology findings: 5

## A. Deletion candidates

None — area is lean.

Every file in `orca/product/spines/scanning/` carries live, unresolved inbound references from other governed areas (`orca/product/spines/capture/`, `orca/product/spines/commission_signal_board/`, `docs/`, `.agents/`), active PROPOSED status, or functions as the canonical cold-start entry point for its source family. Evidence summary per file:

- `orca_demand_gate_definition_closures_proposal_v0.md`: Status `APPLIED_TO_LIVE_INSTRUMENTS_2026-06-14`. At least 25 inbound references in `orca/product/spines/capture/`, `docs/review-outputs/`, `docs/prompts/`, `orca/product/spines/foundation/ontology/`, `orca/product/spines/product_lead/`. Live applied gate; not a deletion candidate.
- `orca_demand_scan_gate_adjudication_packet_v0.md`: Inbound refs in `orca/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_structure_rules_v0.md:20,113`, `docs/migration/`, `docs/decisions/`. Active decision-prep surface; not bloat.
- `orca_demand_scan_core_spec_v0.md`: Inbound refs in 18 files across `orca/product/spines/`, `docs/review-outputs/`, `docs/prompts/`, `docs/decisions/`. Status `PROPOSED_PENDING_ADJUDICATION`; SSOT for the scan method. Not a deletion candidate.
- `aeo_capture_feasibility_probe_phase0_v0.md` + `_evidence.json`: Inbound refs in `docs/migration/spine_first_target_move_table_v0.md:121-122`, `docs/migration/search_demand_signal_migration_inventory_v0.md:77`, `docs/migration/repo_structure_spine_first_v0/moved_paths_index.md:190-191`, `docs/decisions/orca_search_product_lane_binding_v0.md:113-114`. Status `PROBE_EXECUTED_2026-06-17_AWAITING_LANE_ADJUDICATION`; the probe GO/verdict feeds `demand_search_interest_sourcing_and_gate_delta_spec_v0.md`. Not deletable until adjudication and supersession.
- `demand_search_interest_sourcing_and_gate_delta_spec_v0.md`: Inbound refs in `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md:29`, `orca/product/spines/capture/core/demand_durability_indicators/search_interest/demand_durability_indicator_search_interest_capture_profile_v0.md:23,61`, `docs/migration/`, `docs/decisions/`, `orca/product/spines/commission_signal_board/`. Status `PROPOSED_PENDING_FEASIBILITY_AND_OWNER_ADJUDICATION`. Not a deletion candidate.
- `data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md`: Referenced by 9 files including `orca/product/spines/capture/core/source_capture_toolbox/linkedin_reddit_source_capture_armory_concurrent_structure_architecture_v0.md`, `docs/workflows/linkedin_lane_operator_pilot_plan_v0.md`, `docs/workflows/data_capture_spine_consolidation_map_v0.md`. Status `OWNER_ACCEPTED_LINKEDIN_LANE_DISCOVERY_PLANNING_V0`. Authority doc; not bloat.
- `data_capture_spine_linkedin_lane_index_v0.md`: Referenced by `docs/workflows/orca_repo_map_v0.md:514`, `orca/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_structure_rules_v0.md:136`, `docs/hygiene/repo_cleanup_pass_2026_06_v0.md:175,245,288`. Canonical cold-start index for LinkedIn access; repo map calls it out explicitly. Not a deletion candidate.
- `data_capture_spine_linkedin_live_layer_architecture_v0.md`: Referenced by `orca-harness/capture_spine/linkedin_live_adapter/models.py:4` and 8 review-output files. Status `ACCEPTED (v0.1)`; the live-layer ADR. Not bloat.
- `data_capture_spine_linkedin_influence_trajectory_watch_spec_v0.md`: Referenced by `orca/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_lane_index_v0.md:79`, `orca/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md:191,515`. Deferred capability spec; not abandoned — explicitly pointed to by the lane index as the Bounded Watch next step. Not a deletion candidate.
- `data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md`: Referenced by `docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md`, `docs/workflows/data_capture_spine_consolidation_map_v0.md:49,131,302`, `docs/workflows/orca_repo_map_v0.md:337`, `orca/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md`, `orca/product/spines/capture/core/source_capture_toolbox/reddit_capture_operator_playbook_v0.md`. Status `OWNER_DIRECTION_ACCEPTED`. High-inbound architecture authority. Not a deletion candidate.

## B. Ontology / doc-term findings

Compared scanning-area vocabulary against `orca/product/spines/foundation/ontology/ontology.yaml` (SSOT). The SSOT canonical types and aliases (from `runtime_bindings`) are: `Vertical`, `Brand`, `Product`, `Venue`, `WindCaller`, `Call`, `Observation`, `TrendVector`, `DecisionEvent`, `Reading`, `Memo`, `Case`, `Outcome`, `CapturePacket`, `EvidenceUnit`, `Buyer`, `Org`, plus aliases `SourceCapturePacket`, `FacilitatorLedger`, `CaseReport`.

**Finding 1 — `TrendVector` used as unresolved prose in scan-core schema**

- Term: `TrendVector`
- File:line: `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md:338` (field `trend_vector:` in observation schema), also `orca_demand_scan_core_spec_v0.md:174,184,213` (prose)
- SSOT status: ADOPTED (`trend` namespace, `adopted` status). The scan-core observation schema uses the lowercase `trend_vector` field name (not the CamelCase type name), which is consistent with schema field naming, not a drift issue. Prose references to `TrendVector` are correctly matching the SSOT type.
- Proposed fix: None needed; usage is aligned.

**Finding 2 — `WindCaller` used in scan schema with mixed case/prose forms**

- Term: `wind_caller`, `WindCaller`, `wind-caller`
- File:line: `orca_demand_scan_core_spec_v0.md:245` (`wind_caller_call` as `read_type` enum value), `orca_demand_scan_core_spec_v0.md:248` (`wind_caller` in `signal_layer` enum), `orca_demand_scan_core_spec_v0.md:338` (schema fields)
- SSOT status: `WindCaller` is ADOPTED (`windcaller` namespace). The scan schema uses snake_case field values (`wind_caller_call`, `wind_caller`) which is appropriate for enum values. The prose consistently uses `wind-caller` (hyphenated) in many places.
- Proposed fix: The SSOT canonical noun is `WindCaller`; the hyphenated form `wind-caller` is a prose convenience not in the SSOT. No action needed on enum values (snake_case is correct for schema fields), but new docs should prefer `WindCaller` for type-name references and `wind-caller` or `wind_caller` only in schema/field contexts. Low-priority alignment; no rename required.

**Finding 3 — `DecisionEvent` used in scan schema but abbreviated as `brand_decision_event`**

- Term: `brand_decision_event` vs SSOT `DecisionEvent`
- File:line: `orca_demand_scan_core_spec_v0.md:340` (`read_type` enum value `brand_decision_event`), `orca_demand_scan_core_spec_v0.md:228` (section header "Brand-decision event read")
- SSOT status: `DecisionEvent` is ADOPTED (`decision` namespace). The scan schema uses `brand_decision_event` as a `read_type` enum value — this adds the `brand_` qualifier that the ontology type does not carry. The SSOT type is `DecisionEvent`, not `BrandDecisionEvent`.
- Proposed fix: If/when the scan-core spec is adjudicated and adopted, consider aligning the enum value to `decision_event` (dropping `brand_`) to match the SSOT namespace convention, or formally record `brand_decision_event` as a scan-schema-local qualifier that scopes the SSOT type to brand contexts. Owner adjudication surface; not a bloat finding.

**Finding 4 — `CapturePacket` / `SourceCapturePacket` absent from scanning docs (correct absence)**

- Term: `CapturePacket`, `SourceCapturePacket`
- File:line: not found in scanning-area files
- SSOT status: `CapturePacket` is ADOPTED; `SourceCapturePacket` is the runtime alias. Scanning files correctly do not reference capture-packet types directly — the scan emits screening-grade artifacts, not packets. This is a clean boundary, not a gap.
- Proposed fix: None. The absence is correct.

**Finding 5 — `EvidenceUnit` absent; `evidence` used as a schema field name without SSOT alignment**

- Term: `EvidenceUnit` (SSOT type, `evidence` namespace)
- File:line: `orca_demand_scan_core_spec_v0.md` does not reference `EvidenceUnit`. The word `evidence` appears extensively as a field descriptor and in gate-column prose, not as the SSOT type name.
- SSOT status: `EvidenceUnit` is ADOPTED. Scanning files correctly distinguish between "evidence" as a qualitative term and the `EvidenceUnit` type (which belongs to the capture/proof lane, not the scan lane). The scan-core schema does not emit `EvidenceUnit` records — that is the capture lane's output.
- Proposed fix: None. The absence of `EvidenceUnit` in scanning docs is correct. Authors should be aware that `evidence` in prose is not a reference to the SSOT `EvidenceUnit` type; no renaming is warranted in scanning context.

**Summary of ontology findings: Clean with minor alignment notes.** No SSOT violations found. Five findings examined; all are either correct usage, appropriate schema-field naming conventions, or minor prose-form variations (hyphenated vs CamelCase) that do not constitute drift. The one actionable candidate is Finding 3 (`brand_decision_event` vs `DecisionEvent`) — a naming-alignment note for the adjudication of the scan-core spec, not a bloat or error issue.
