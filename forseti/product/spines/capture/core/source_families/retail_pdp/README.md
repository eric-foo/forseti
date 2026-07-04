# Capture Source Family: Retail PDP

```yaml
retrieval_header_version: 1
artifact_role: Orca Capture source-family README
scope: >
  Directory entrypoint for Retail/PDP source-family artifacts under the Capture
  core acquisition layer.
use_when:
  - Starting Retail/PDP capture source-family work.
  - Checking the Capture-vs-Scanning phase placement for Retail/PDP artifacts.
  - Finding the first Retail/PDP capture contracts, probes, or playbooks to open.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_contract_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_typed_envelope_probe_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_site_registry_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_contract_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_capture_pilot_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_widget_expansion_probe_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_rendered_companion_probe_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
```

This directory is the current Capture home for Retail/PDP source-family
artifacts. It does not imply a Scanning sibling exists.

Phase sibling status: no accepted
`forseti/product/spines/scanning/source_families/retail_pdp/` directory exists in
this worktree. If a Scanning Retail/PDP source family is later created, add the
cross-pointer here and in the Scanning family entrypoint.
