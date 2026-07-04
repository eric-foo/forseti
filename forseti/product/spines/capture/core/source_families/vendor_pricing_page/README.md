# Capture Source Family: Vendor Pricing Page

```yaml
retrieval_header_version: 1
artifact_role: Capture source-family lane index
scope: >
  Cold-start lane index for vendor pricing pages whose source-visible price
  facts are recovered from embedded structured payloads and written as source
  capture packets under source_family=vendor_pricing_page.
use_when:
  - Starting or reviewing vendor pricing-page capture-to-lake work.
  - Routing a "capture pricing page" or "land vendor pricing page in the lake" request from the Source Capture Playbook.
  - Checking the current SPA/JS-payload price route versus broader price time-series capture profiles.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/README.md
  - forseti/product/spines/capture/core/source_capture_toolbox/weapon_rung15_embedded_payload_extraction_v0.md
  - forseti/product/spines/capture/core/demand_durability_indicators/price_timeseries/demand_durability_indicator_price_timeseries_capture_profile_v0.md
  - forseti/product/spines/data_lake/README.md
  - orca-harness/docs/source_capture_packet.md
stale_if:
  - run_source_capture_price_payload_packet.py changes source_family, source_surface, access route, or lake-write behavior.
  - price_payload_extraction.py is generalized beyond the current embedded-payload pricing adapter shape.
  - The price time-series capture profile, Source Capture Playbook, or Data Lake raw/derived contracts move or change the route boundary.
```

## Canonical Route Home

Open this README after the Source Capture Playbook has determined that the
target is a public vendor pricing page and the signal lives in embedded
structured payloads rather than rendered-only DOM or an access-controlled API.

Current landed code is a narrow SPA/JS-payload route, not a universal price
checker. Other vendor pricing-page shapes still route through the playbook as
new-source probes unless their source-specific adapter is present and verified.

## Route Map

| Layer | Current home | What to confirm |
| --- | --- | --- |
| Access / method | Source Capture Playbook; `weapon_rung15_embedded_payload_extraction_v0.md` | Rung-1 anti-block HTTP plus rung-1.5 embedded-payload extraction is appropriate for the substrate; a 200 is not trusted without `block_shell` and payload checks. |
| Pricing packet write | `orca-harness/runners/run_source_capture_price_payload_packet.py` | The runner writes `source_family="vendor_pricing_page"` through `stage_and_write_packet`, with local output or `DataLakeRoot` mode selected explicitly. |
| Embedded payload parser | `orca-harness/source_capture/price_payload_extraction.py` | The current implementation recovers tier structure and amounts from React Router hydration plus a linked JS prices object; loud miss, no fake-empty success. |
| Price time-series deconfliction | `forseti/product/spines/capture/core/demand_durability_indicators/price_timeseries/demand_durability_indicator_price_timeseries_capture_profile_v0.md` | This route covers narrow SPA/JS-payload price recovery; rendered retail/beauty price, promo, cadence, and standing-capture profiles remain separate. |
| Data Lake authority | `forseti/product/spines/data_lake/README.md` -> `authority/` | Raw admission, path grammar, derived layout, and Silver semantics stay Data Lake-owned. |

## Current Posture

The landed source-family key is `vendor_pricing_page`. The route is source-family
specific because the packet writer emits that family literally; it should not be
hidden under Retail/PDP, whose current route map is PDP/storefront oriented.

The current adapter surface is the OpenAI/ChatGPT pricing-page payload
shape described by the rung-1.5 weapon doc and runner defaults. Treat new vendor
pricing pages as new-source probes until their payload anchors, schema parse,
and domain checks are verified.

## Non-Claims

Not live capture authorization, validation, readiness, price truth, source
freshness, completeness, standing scheduler authority, rendered retail price
coverage, ECR, Cleaning, Judgment, buyer proof, or commercial-readiness
evidence.
