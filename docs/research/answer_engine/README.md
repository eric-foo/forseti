# Answer Engine Research

```yaml
retrieval_header_version: 1
artifact_role: Research front-door
scope: Retrieval-only entry point for answer-engine and AEO research artifacts.
use_when:
  - Starting answer-engine, AEO, or search-surface research.
  - Finding the Phase-0 feasibility probe and evidence bundle.
  - Routing from research evidence to the scanning source-family spec.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/forseti_repo_map_v0.md
  - docs/research/answer_engine/aeo_capture_feasibility_probe_phase0_v0.md
  - docs/research/answer_engine/aeo_capture_feasibility_probe_phase0_v0_evidence.json
  - orca/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md
stale_if:
  - The AEO Phase-0 probe is superseded by a later accepted answer-engine research record.
  - The scanning answer-engine/source-family spec is superseded.
```

## Load Order

1. Open the Phase-0 probe report for the research verdict, observed surfaces,
   limitations, and non-claims.
2. Open the evidence JSON only when raw observed probe evidence is needed.
3. Open the scanning source-family spec when the work moves from research
   evidence to scanning/product routing.

## Boundary

This folder is research evidence, not product authority by location. It does
not authorize live capture, monitoring, browser automation, source-access
tooling, buyer proof, validation, readiness, or answer-engine product claims.
