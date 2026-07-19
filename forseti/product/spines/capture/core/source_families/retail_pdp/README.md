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
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_contract_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_silver_producer_contract_v0.md
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
| Access / method | `retail_pdp_projection_contract_v0.md`, `retail_pdp_projection_playbook_v0.md`, `retail_pdp_sidecar_operator_playbook_v0.md` | Retailer-specific capture inputs, residual vocabulary, target DOM price/SKU binding posture, and the no-ECR/Cleaning/Judgment boundary. |
| Storefront pins | `retail_storefront_pin_registry_v0.md`; `amazon_us_vpn_regression_recovery_playbook_v0.md`; supporting recon and live receipts linked there | Session, storefront-country, currency, and delivery-location state independently; a working route, VPN geography, or observed context is not a confirmed pin. |
| Retail/PDP packet/projection | `forseti-harness/runners/run_source_capture_cloakbrowser_packet.py --source-family retail_pdp`; `run_retail_pdp_projection.py`; the Sephora, Luckyscent, and Nordstrom parser-fit runners; `forseti-harness/source_capture/retail_pdp_projection.py` | `sephora_pdp_aggregate`, `luckyscent_pdp_aggregate`, and `nordstrom_pdp_aggregate` default to family-owned content mode only after their retailer-owned US/USD, access, sufficiency, and projection gates pass. Luckyscent retains all three target variants and all eight rendered target reviews. Retailer PDP onboarding uses one coverage rule: capture the complete Most Recent 30-day cohort, and when it contains fewer than 12 reviews continue in that same source order to 30 total rows or proven source exhaustion. Nordstrom implements this rule with `--nordstrom-review-posture recent_window_30d`, retains the retailer's separate most-helpful positive/critical pair, and records each `Load 6 more reviews` activation as one six-row append. A 30-row cap hit inside the recent window is marked truncated. Retailers without proven sort/continuation controls do not inherit generic clicking; their route remains capability-unconfirmed until a retailer-owned adapter implements the same coverage decision. Nordstrom's visible shipping destination stays an unpinned residual, not US-delivery proof. Raw/sample modes and packet-directory projection remain for drift checks and legacy packets. Every other retail profile remains raw. No live broad crawl, scheduler, ECR, Cleaning, or Judgment. |
| Retail/PDP Silver | `retail_pdp_silver_producer_contract_v0.md`; `run_retail_pdp_silver_producer.py`; `forseti-harness/source_capture/retail_pdp_silver.py` | Exact projection record, retailer-local identity, raw plus derived lineage, and source-visible offer/review observations only. |
| Fragrance purchase-review row capture | `fragrance_purchase_review_*` docs in this folder; `run_fragrance_review_coverage.py`; `run_fragrance_review_discovery.py`; `run_fragrance_review_lake_packet.py`; `forseti-harness/source_capture/fragrance_review_lake.py` | Retailer review-positive PDP discovery, rendered/widget companion preservation, focused coverage, and preserved-body lake tee boundaries. |
| Data Lake authority | `forseti/product/spines/data_lake/README.md` -> `authority/` | Raw admission, path grammar, derived layout, and Silver semantics. The family index does not own them. |

## Non-Claims

This entrypoint is not live capture authorization, validation, readiness,
source completeness, ECR, Cleaning, Judgment, buyer proof, demand proof, or
commercial-readiness evidence.
