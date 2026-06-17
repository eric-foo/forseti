# Search-lane Reference Inventory

Covers the full lane migration (two waves, applied on the lane branch). Verified
by worker sweeps this session and re-scanned by `apply_moves.py --dry-run` at
apply. Classes: `live` = rewritten by `--apply`; `historical` = kept, resolved
via `moved_paths_index.md`; `moved_set` = inside a moved file (rewritten where
the reference is a full old path).

Move-set (10): see `moves_manifest.csv`. Wave 1 = the 4 search/answer-engine
surface docs. Wave 2 = the 6 demand-signal method docs.

## Wave 1 (search / answer-engine surfaces) - live rewrites

| Referencing file | References | Lines |
| --- | --- | --- |
| `docs/product/data_capture_spine/demand_durability_indicator_capture_deconfliction_note_v0.md` | search-interest capture profile | 21, 134 |
| the moved search-interest source-class spec | search-interest capture profile (`open_next`) | internal |

(AEO report <-> evidence JSON use a bare "same folder" note - not rewritten; both move together.)

## Wave 2 (demand-signal method, 6 docs) - live rewrites

~19 distinct LIVE referencing files across the 6 (worker sweep). The apply
engine scans and rewrites every full-path occurrence. Largest fan-out:
`orca_demand_read_taxonomy_v0.md` (judgment_spine read-machinery / grading
rubric / verdict + ledger contracts, the buyer-proof packet, the ontology
backbone, and the data_capture_spine durability profiles). 5 of the 6 also
cross-reference each other; those intra-set full paths are rewritten too.

LIVE referencing files (rewritten by `--apply`):
- `docs/product/search/demand_search_interest_sourcing_and_gate_delta_spec_v0.md`
- `docs/product/search/demand_durability_indicator_search_interest_capture_profile_v0.md`
- `docs/product/core_spine/orca_ontology_backbone_architecture_v0.md`
- `docs/product/product_lead/orca_buyer_proof_packet_v0.md`
- `docs/product/judgment_spine/judgment_spine_demand_read_machinery_architecture_v0.md`
- `docs/product/judgment_spine/judgment_spine_c3_verdict_action_ceiling_contract_v0.md`
- `docs/product/judgment_spine/judgment_spine_demand_read_grading_rubric_v0.md`
- `docs/product/judgment_spine/judgment_spine_c2_rule3_reground_phase_a_classification_finding_v0.md`
- `docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md`
- `docs/product/data_capture_spine/demand_durability_indicator_review_velocity_corpus_capture_profile_v0.md`
- `docs/product/data_capture_spine/demand_durability_indicator_price_timeseries_capture_profile_v0.md`
- `docs/product/data_capture_spine/demand_durability_indicator_capture_deconfliction_note_v0.md`
- `docs/product/data_capture_spine/demand_durability_indicator_availability_restock_capture_profile_v0.md`
- the 6 moved docs (intra-set references to each other)

NOTE: `docs/product/search/README.md` was hand-restructured (the 6 become
in-lane) and no longer holds the old paths, so the engine does not rewrite it.

## Not rewritten (by design)

- Historical records (decisions / reviews / prompts / research / hygiene): keep
  old paths; resolve via `moved_paths_index.md`. Notable: the wind_caller
  carveout decision, the consumer-demand ratification memo, the consumer-demand
  thesis, several product-planning / review prompts, and adversarial review
  outputs.
- Bare-filename mentions (no full path) - resolve regardless of folder.
  Pre-existing-stale note: `orca_ontology_backbone_architecture_v0.md` calls the
  scan-core spec "in-flight / not on main" by bare name (lines 63 / 306 / 328) -
  stale independent of this move (the spec is already on main); left as-is (out
  of scope for this migration).

## Integrity

- search/README.md's "Related, but living in their function lanes" section was
  structurally false after the move (it claimed the 6 stay in their spine
  lanes); hand-rewritten so the 6 are in-lane with a venue-spanning scope note
  (worker FLAG 1).
- No inbound content-hash pin covers the moved docs (references are by path, not
  hash), so the intra-set rewrites are hash-safe.
- `apply_moves.py --dry-run` re-scans the live tree at apply; any new full-path
  reference added by a concurrent lane is reported and rewritten; anything
  outside this inventory is surfaced for reconciliation rather than auto-trusted.
