# Orca Search Lane

```yaml
retrieval_header_version: 1
artifact_role: Orca product lane index
scope: >
  Front-door index for docs/product/search/ - Orca's search / answer-engine
  surfaces PLUS the demand-signal discovery method (scan, read-grammar, gates)
  those surfaces feed. Lists the co-located docs and notes the cross-spine
  consumers of the method docs.
use_when:
  - Looking for Orca's search / answer-engine work (capture, source-class, AEO).
  - Looking for the demand-signal discovery method (scan core, read taxonomy, demand gates).
  - Deciding whether a new doc belongs in this lane.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_search_product_lane_binding_v0.md
```

The search lane is Orca's **demand-signal intelligence (search-led)** vertical. It
holds two things: (1) the **search / answer-engine surfaces** Orca captures (web
search / SERP, Google AI Overviews and other answer engines, zero-click, AEO/GEO,
search-interest / "trends"); and (2) the **demand-signal discovery method** those
surfaces feed - the scan method, the read grammar/taxonomy, and the demand gates
that adjudicate discovered signal. The lane is **bound by**
`docs/decisions/orca_search_product_lane_binding_v0.md`; that record holds the
inclusion test and precedence rule that decide membership.

> Scope note: the demand-signal **method** docs in this lane (scan core, read
> taxonomy, demand gates) are **search-led but venue-spanning** - they govern
> demand reads across all venues (forums, retail, reviews, search) and are
> consumed by the judgment, data-capture, and core spines. They live here
> because search/trends is the lane that owns demand-signal discovery, not
> because they are search-only; their cross-spine references resolve into
> `docs/product/search/`.

> Migration status: the search/answer-engine surfaces (the first 4 below) are
> already in this lane. The demand-signal method docs (the 6) are relocated here
> by the expanded `docs/migration/repo_structure_search_lane_v0/` move; until
> that apply runs, their relative links resolve only after the move.

## In this lane

### Search / answer-engine surfaces
- [`aeo_capture_feasibility_probe_phase0_v0.md`](aeo_capture_feasibility_probe_phase0_v0.md) - Phase-0 feasibility probe: can AI answer engines' output (brands + cited sources + issued queries) be reliably and automatably captured? ChatGPT + Google AI Overviews. GO verdict, extraction patterns, failure taxonomy.
- [`aeo_capture_feasibility_probe_phase0_v0_evidence.json`](aeo_capture_feasibility_probe_phase0_v0_evidence.json) - Machine-readable per-run evidence for the probe.
- [`demand_search_interest_sourcing_and_gate_delta_spec_v0.md`](demand_search_interest_sourcing_and_gate_delta_spec_v0.md) - Source classes + gate-read placement for search-interest and AEO (which surface feeds which demand gate).
- [`demand_durability_indicator_search_interest_capture_profile_v0.md`](demand_durability_indicator_search_interest_capture_profile_v0.md) - Capture obligations for search-interest signals: temporal regime, cold-start, comparability.

### Demand-signal discovery method (search-led, venue-spanning)
- [`orca_demand_scan_core_spec_v0.md`](orca_demand_scan_core_spec_v0.md) - Method spec for the scanning function: how an authorized scan walks venues, recognizes demand situations, and emits candidate observations.
- [`orca_demand_read_taxonomy_v0.md`](orca_demand_read_taxonomy_v0.md) - The demand-read grammar: signal layers, read types, wind-caller machinery, durable/transient/manufactured demand-state model. Consumed across judgment/capture/core spines.
- [`orca_demand_read_taxonomy_adjudication_v0.md`](orca_demand_read_taxonomy_adjudication_v0.md) - Adjudication-prep companion to the taxonomy (operative definitions, named tensions, owner decision queue).
- [`orca_demand_scan_gate_adjudication_packet_v0.md`](orca_demand_scan_gate_adjudication_packet_v0.md) - Owner decision packet for the first live demand scan (scan-core adoption, gate-run criteria, gate architecture, sourcing gap).
- [`orca_demand_gate_definition_closures_proposal_v0.md`](orca_demand_gate_definition_closures_proposal_v0.md) - Ratified Demand-Substrate Hard Gate definitions (G1 independence, G2 costly-behavior floor, G4 org-motion).
- [`orca_demand_gate_run_commission_criteria_v0.md`](orca_demand_gate_run_commission_criteria_v0.md) - Criteria/shape for commissioning one candidate through the demand gate to an admit/hold/fail verdict.

## Consumed by (cross-spine, stay external)

The method docs above are referenced by, but do not move with, their consumers -
e.g. the `judgment_spine/` read-machinery, grading rubric, and verdict
contracts; `product_lead/orca_buyer_proof_packet_v0.md`;
`core_spine/orca_ontology_backbone_architecture_v0.md`; and the
`data_capture_spine/` durability capture profiles. Those references now resolve
into `docs/product/search/`.

## Not in this lane

Different venue, or not demand-signal-discovery method, so they stay where they are:
- Retail availability/restock, price-timeseries, and review-velocity durability capture profiles (`data_capture_spine/`) - retail/price/review venues, not search.
- `reddit_candidate_intake_old_reddit_search_surface_handling_v0.md` (`workflows/`) - old-Reddit HTML listing parsing, a capture concern (its "search" is not search-interest).
- `consumer_demand_candidate_pool_handoff_v0.md` (`core_spine/`) - a one-shot candidate roster, not method.
- `orca_discovery_candidate_scan_beauty_neutral_chatgptpro_v0.md` (`research/`) - a discovery research artifact.
