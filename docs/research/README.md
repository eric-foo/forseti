# Forseti Research

This folder holds docs-first public and source-backed research artifacts that support Forseti product, proof, and decision work.

Research artifacts are not product authority by default. They may gather evidence, preserve raw lane outputs, screen candidates, map rejected sources, or synthesize source-backed findings. Product claims, accepted decisions, and proof locks belong in `forseti/product/` or `docs/decisions/` after a later explicit promotion step.

Use this folder when the main artifact is:

- evidence gathering from public sources;
- corpus qualification;
- candidate screening;
- source-query and source-quality notes;
- reject-pattern mapping;
- synthesis of previously gathered evidence;
- decision-packet construction boundaries between cleaned evidence and judgment or harness use.

Do not use this folder for implementation, automation, scraping tools, datasets, packages, tests, runtime artifacts, or generated source systems.

## Research Areas

- `docs/research/consulting-judgment-corpus/`: consulting-judgment corpus material.
- `docs/research/judgment-spine/`: Judgment Spine parent contract, harness specs, case indexes, and case-learning artifacts.
- `docs/research/packing-phase/`: initial boundary note for turning cleaned evidence into judgment-ready packet artifacts without absorbing Cleaning or Judgment Harness responsibilities.
- `docs/research/daimler_advisory_001/` (plus the loose `daimler_advisory_001_*.md` files): Daimler advisory-run 001 source-capture research — source registry, official/legal provenance core, source-fanout consolidation, and source-body capture receipts.
- Loose `data_capture_spine_pressure_test_batch_synthesis_n2of3_v0.md` and `..._n3of3_v0.md`: Data Capture Spine pressure-test batch-synthesis outputs (loose files pending folder triage).
- Loose `aphrodite_*` files: Aphrodite creator-capture research — the capture strategy (`aphrodite_creator_capture_strategy_v0.md`), the Silver metric monitoring inventory (`aphrodite_silver_metric_monitoring_inventory_v0.md`), and the creator-capture field map (`aphrodite_creator_capture_field_map_v0.md` — what data/stats we can track/harvest per grid/deep/derived layer).
