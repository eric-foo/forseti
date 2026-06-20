```yaml
retrieval_header_version: 1
artifact_role: Orca migration note
scope: >
  Phase-2 W3a deletion + ontology proposal for orca/product/spines/foundation/ (~19 files).
  Covers product_contract/, demand_read_taxonomy/, ontology/ (SSOT -- never deletion target),
  and vertical_exploration/ sub-areas. Read-only scan; adjudication is owner-gated.
use_when:
  - Adjudicating deletion candidates identified in the foundation spine area.
  - Reviewing ontology / doc-term findings before Phase-3 ratchet.
authority_boundary: retrieval_only
open_next:
  - docs/migration/orca_second_pass_consolidation_plan_v0.md
stale_if:
  - Any listed file is deleted, renamed, or substantially rewritten after this scan date (2026-06-19).
  - The deletion-evidence register gains records covering the listed targets.
```

# Phase-2 W3a Proposal — foundation

## Summary

21 files scanned (19 in scope + ontology SSOT + expansion backlog + cards README — included in full scan).
Area is lean and heavily load-bearing. Every file carries active inbound refs from multiple consumers
across `orca/product/`, `docs/`, and `.agents/`. No file qualifies as pure bloat. The `demand_read_taxonomy_adjudication_v0.md` file is a close call: its Q0–Q3 decisions are folded into the taxonomy and thesis, but the prep companion is still actively cited as an adjudication-record source. Verdict: keep.

**Deletion candidates: 0 high / 0 medium / 0 low.**
**Ontology / doc-term findings: 2 (both outside foundation/; foundation itself is clean).**

---

## A. Deletion candidates

None — area is lean.

Rationale by sub-area:

### product_contract/ (7 files)

**`core_spine_v0_product_contract.md`**
- reverse_ref_check: active refs in `orca_repo_map_v0.md:541`, `source-loading.md:305`, ontology backbone §0, proof protocol, information-production foundation, proof-packet preflight, proof input selection, data-and-cleaning boundary, and downstream case-family charters. 10+ consumers across lanes.
- verdict: keep; foundational anchor; no successor.

**`core_spine_v0_information_production_foundation_v0.md`**
- reverse_ref_check: active refs in `source-loading.md:307`, `orca_repo_map_v0.md:536`, `jsg01_source_side_receipt_translator_v0.md:18` (stale-if trigger), ECR plan cross-check, harness `ecr/__init__.py`, offer hypothesis, icp wedge, 20+ prompt and review-output files. IPF is the canonical Evidence Unit semantic home cited by runtime code.
- verdict: keep; load-bearing runtime-adjacent doc; no successor.

**`core_spine_v0_data_and_cleaning_spine_boundary_v0.md`**
- reverse_ref_check: active refs in `source-loading.md:303`, `orca_repo_map_v0.md:458,537`, `orca-harness/evidence_binding/models.py:5`, `orca-harness/ecr/__init__.py:4`, `orca-harness/ecr/models.py:4`, `core_spine_v0_projection_doctrine_v0.md:18`, JSG-01 receipt translator, multiple judgment-spine files. Cited in production harness code.
- verdict: keep; harness-referenced boundary doc; ECR ratification records live here; no successor.

**`core_spine_v0_proof_protocol_v0.md`**
- reverse_ref_check: active refs in `orca_repo_map_v0.md:542`, `distillation_binding_core_spine_proof_v0.md:13`, 6 case-family charters in `orca/product/case_families/`, multiple prompts and review outputs. Proof gates derive from this.
- verdict: keep; proof method gate document; no successor.

**`core_spine_v0_proof_input_selection_v0.md`**
- reverse_ref_check: active refs in `orca_repo_map_v0.md:543`, `core_spine_v0_information_production_foundation_v0.md:6`, `core_spine_v0_proof_packet_preflight_v0.md:13`, 8 case-family charter files, 2 prompt files.
- verdict: keep; active proof-chain document; no successor.

**`core_spine_v0_proof_packet_preflight_v0.md`**
- reverse_ref_check: active refs in `orca_repo_map_v0.md:544`, adversarial review prompt (sha-pinned at `557CF083…`), 5 case-family charter files.
- verdict: keep; proof readiness gate; no successor.

**`core_spine_v0_method_validation_rubric_v0.md`**
- reverse_ref_check: active refs in `orca_repo_map_v0.md:570`, `core_spine_v0_method_validation_case_locks_v0.md:7`, `core_spine_v0_method_validation_case_frame_lock_contract_v0.md:7`, adversarial review prompt, case-hunting prompt, method-validation replay packet prompt. 10+ downstream consumers.
- verdict: keep; method-validation design document; no successor.

### demand_read_taxonomy/ (2 files)

**`orca_demand_read_taxonomy_v0.md`**
- reverse_ref_check: active refs in `orca_ontology_backbone_architecture_v0.md:49` (source-read ledger), `orca_product_thesis_consumer_demand_v0.md` (dated-pointer amendment), `buyer_proof_packet_v0.md:669` (stale-if trigger), ontology backbone architecture §0, scan-spec, search migration inventory. The PROPOSED status is retained; Q0–Q3 decisions are folded in via dated amendment, but the taxonomy itself is the operative read-grammar cited by downstream consumers.
- verdict: keep; operative read grammar; no successor.

**`orca_demand_read_taxonomy_adjudication_v0.md`**
- reverse_ref_check: active refs in `orca_product_thesis_consumer_demand_v0.md:123,142`, `orca_demand_read_taxonomy_v0.md:47`, `buyer_proof_packet_v0.md:669,694`, `wind_caller_calibration_carveout_v0.md:390`, ontology backbone §0 source-read ledger, ontology commission refresh delegated review (3 refs), `chatgptpro_beauty_subniche_research_prompt_v0.md:264`.
- semantic note: Q0–Q3 are all decided and folded into the taxonomy and thesis. This file's primary current value is as the adjudication audit record and the source for Q1–Q3 operative definitions (what-counts / anti-trigger / boundary per layer). The ontology commission prompt explicitly cites it as "the firmest source for Read / WindCaller / Call definitions."
- verdict: keep; active adjudication record and operative-definition source; no successor.

### ontology/ (protected SSOT)

`ontology.yaml`, `orca_ontology_backbone_architecture_v0.md`, `ontology_expansion_backlog_v0.json`, all `ontology_cards/`: SSOT and its satellite cards — explicitly excluded from deletion candidates per task scope. All are referenced by `check_ontology_ssot.py`, `check_ontology_expansion.py`, harness runtime, and multiple lanes.

### vertical_exploration/ (2 files)

**`orca_vertical_exploration_guide_v0.md`**
- reverse_ref_check: active refs in `orca_repo_map_v0.md:546`, `source-loading.md:380,614`, `orca_demand_scan_core_spec_v0.md:22,46`, `source_capture_playbook_v0.md:117`, `orca_memorization_resistant_case_finder_frame_v0.md:22`, `beauty_venue_card_set_v0.md:19`, 10+ decision records (`beauty_subtle_decision_screen3_ledger_v0.md`, `ingestible_beauty_screen1_ledger_v0.md`, `orca_mini_god_tier_doctrine_v0.md`, `orca_venue_registry_rejection_decision_v0.md`, `pre_capture_discovery_spine_charter_recommendation_v0.md`, `screening_reddit_read_route_decision_v0.md`, `venue_procedure_proving_screen_beauty_ledger_v0.md`). Walker Equipment Kit block is pasted into every scan/walk prompt.
- verdict: keep; operative discovery procedure; no successor.

**`orca_memorization_resistant_case_finder_frame_v0.md`**
- reverse_ref_check: active refs in `orca_demand_scan_core_spec_v0.md:49`, `orca_vertical_exploration_guide_v0.md:19`, `judgment_spine_backtest_batch1_ledger_declaration_v0.md:18`, `pre_capture_discovery_spine_charter_recommendation_v0.md:23,181`, `r5_whitelist_decision_framing_propagation_v0.md:67`, `fragrance_level1_named_case_candidate_screen_v0.md:345`, `consumer_demand_candidate_pool_handoff_v0.md:21`, `conductor_construction_integrity_probe_addendum_adversarial_review_v0.md:96`, `decide_vs_confirm_case_discovery_results_v0.md:18`, `research/source_registry_practices_deep_research_report_v0.md:20`, multiple commission prompts.
- verdict: keep; active case-finder doctrine frame; no successor.

---

## B. Ontology / doc-term findings

The foundation area itself (`orca/product/spines/foundation/`) is **clean** — the `check_doc_terms.py --check` run (run 2026-06-19) excludes `foundation/ontology/` (the term home) and finds no new-term candidates or deprecated/aliased term usage originating in the remaining foundation files.

The tool scan over all of `orca/product/` (218 files) surfaced **2 new-term candidates** in files **outside** this area:

### Finding B-1: `FailureEvent` — ontology head-noun drift

- term: `FailureEvent`
- head-noun: `Event` (matches SSOT head-noun set; canonical type is `DecisionEvent`)
- files:
  - `orca/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md` — 12 refs
  - `orca/product/spines/judgment/conductor/judgment_spine_gate_ownership_map_v0.md` — 1 ref
- status: `FailureEvent` is not in `ontology.yaml` as a type, alias, or dimension. It is a harness/engineering term (a gate-failure event in the judgment conductor), not a demand-world object type candidate. It does not represent a candidate for ontology addition under the 18-type cap.
- proposed fix (read-only): No source edit — this is an engineering identifier in a conductor that is currently FROZEN; the term is appropriately scoped to the judgment-spine conductor and does not require ontology registration. Flag for the judgment-spine lane to note the head-noun collision during the next conductor unfreeze pass. No action in this area.

### Finding B-2: `RetailPdpProjectionPacket` — ontology head-noun drift

- term: `RetailPdpProjectionPacket`
- head-noun: `Packet` (matches SSOT head-noun set; canonical alias is `SourceCapturePacket` → `CapturePacket`)
- file: `orca/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_playbook_v0.md` — 1 ref
- status: This is a capture-lane projection artifact name, not a new ontology type candidate. It follows the `CapturePacket` head-noun but is a scoped implementation label for a projection playbook's output object, not a distinct demand-world type.
- proposed fix (read-only): No source edit — this is a capture-lane engineering label that is not in scope for ontology adoption (no backing landed, no demand-world semantic gap filled). Flag for the capture lane to clarify in the playbook whether this is an alias for `SourceCapturePacket` or a distinct construct; if distinct, surface to the ontology owner under the one-in-one-out rule before the 18-cap is approached.

### Foundation ontology files: clean against SSOT

Spot-checked the foundation product_contract/ and demand_read_taxonomy/ files for non-SSOT CamelCase usage:
- `EvidenceUnit`, `CapturePacket`, `DecisionEvent`, `TrendVector`, `WindCaller` usage all matches SSOT types or known aliases.
- `SourceCapturePacket` used correctly as the recorded storage alias → `CapturePacket`.
- `FacilitatorLedger` used correctly as runtime alias → `Case`.
- No deprecated/retired terms (`Hollow`, `Slot`, `DataSpine`) found in active use in the foundation files.
- "Durable vs hollow" framing: not present in current form of `orca_demand_read_taxonomy_v0.md` (retired per Q0 2026-06-14; taxonomy correctly reflects `durable vs transient × real vs manufactured`).
- `orca_demand_read_taxonomy_adjudication_v0.md` retains the "durable vs hollow" phrasing in its historical Q0 status block (dated audit record). This is correct — it is a dated adjudication record of the retired framing, not a live assertion.
