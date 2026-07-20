# Capture Source Family: Retail PDP

```yaml
retrieval_header_version: 1
artifact_role: Forseti Capture source-family README
scope: >
  Directory entrypoint for Retail/PDP source-family artifacts under the Capture
  core acquisition layer.
use_when:
  - Starting Retail/PDP capture source-family work.
  - Checking the Capture-vs-Scanning phase placement for Retail/PDP artifacts.
  - Finding the first Retail/PDP capture contracts, probes, or playbooks to open.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/README.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/amazon_demand_signal_route_candidates_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_content_cleaning_contract_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_silver_producer_contract_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_typed_envelope_probe_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_storefront_pin_registry_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/amazon_us_vpn_regression_recovery_playbook_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_site_registry_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_contract_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_capture_pilot_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_widget_expansion_probe_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_rendered_companion_probe_v0.md
  - forseti/product/spines/data_lake/README.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
```

This directory is the current Capture home for Retail/PDP source-family
artifacts. It does not imply a Scanning sibling exists.

Phase sibling status: no accepted
`forseti/product/spines/scanning/source_families/retail_pdp/` directory exists in
this worktree. If a Scanning Retail/PDP source family is later created, add the
cross-pointer here and in the Scanning family entrypoint.

## Capture-To-Lake Route Map

| Layer | Current home | What to confirm |
| --- | --- | --- |
| Access / method | `retailer_information_extraction_standard_v0.md`; `retail_pdp_content_cleaning_contract_v0.md` | Cross-retailer evidence categories and discovery behavior; retailer-owned extraction, retention, target binding, residuals, Cleaning, and Silver handoff. |
| Storefront pins | `retail_storefront_pin_registry_v0.md`; `amazon_us_vpn_regression_recovery_playbook_v0.md`; supporting recon and live receipts linked there | Session, storefront-country, currency, and delivery-location state independently; a working route, VPN geography, or observed context is not a confirmed pin. |
| Retail/PDP packet/content | `run_source_capture_cloakbrowser_packet.py`; `source_capture/retail_pdp_content.py`; `cleaning/retail_pdp.py` | The three admitted profiles default to canonical content after retailer-owned pin/access/sufficiency/extraction gates. Raw remains the failure and unflipped-route posture. |
| Retail/PDP Silver | `retail_pdp_silver_producer_contract_v0.md`; `run_retail_pdp_silver_producer.py`; `source_capture/retail_pdp_silver.py` | Cleaning-owned source anchors, retailer-local identity, and source-visible offer/review observations only. |
| Fragrance purchase-review row capture | `fragrance_purchase_review_*` docs in this folder; `run_fragrance_review_coverage.py`; `run_fragrance_review_discovery.py`; `run_fragrance_review_lake_packet.py`; `forseti-harness/source_capture/fragrance_review_lake.py` | Retailer review-positive PDP discovery, rendered/widget companion preservation, focused coverage, and preserved-body lake tee boundaries. |
| Data Lake authority | `forseti/product/spines/data_lake/README.md` -> `authority/` | Raw admission, path grammar, derived layout, and Silver semantics. The family index does not own them. |

## Non-Claims

This entrypoint is not live capture authorization, validation, readiness,
source completeness, ECR, Cleaning, Judgment, buyer proof, demand proof, or
commercial-readiness evidence.
