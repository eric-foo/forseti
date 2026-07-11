# Retail/PDP Amazon-First Silver Live Proof v0

```yaml
retrieval_header_version: 1
artifact_role: Research / implementation validation receipt
scope: >
  Records the bounded 2026-07-11 live proof that a fresh anonymous Amazon US
  PDP packet can be mechanically projected and consumed by the generic
  retail_pdp_silver producer without inventing exact stock or sold quantities.
use_when:
  - Reviewing the first real-source proof for the Retail/PDP Silver producer.
  - Rechecking the observed Amazon values and lineage outcome from this run.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_silver_producer_contract_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/amazon_demand_signal_route_candidates_v0.md
stale_if:
  - The Amazon capture profile, projection contract, or Silver producer contract changes.
  - This receipt is cited as current capture evidence rather than a dated run.
```

## Run Boundary

- Captured at: `2026-07-11T07:14:19Z`.
- Source: public logged-out Amazon PDP for ASIN `B07XXPHQZK`.
- Profile: `amazon_pdp_distribution`.
- Delivery posture: ZIP `10001` applied and independently confirmed by rendered
  `currencyOfPreference="USD"` evidence.
- Session: anonymous and ephemeral; no browser user-data profile, storage state,
  cookie export, credentials, proxy, or persisted session was supplied.
- Storage: isolated initialized lake under `C:\tmp`; scratch evidence only, not
  repository or production-lake authority.

## Exact Evidence Chain

- Raw packet: `01KX80DVHN1SCARF56G9MRKDVC`.
- Exact projection record:
  `projection_retail_pdp/01KX80EHP2X9ZRGH40BX9EMV3F.json`.
- Projection SHA-256:
  `f5747276cf46e2d84b130d118a98da717650d386c0dad61ee1dbce8e8f834eb5`.
- Generic Silver records:
  - `01KX80EXDZ7B6N8V0ERZMN6ZT1.json`
  - `01KX80EXDZQMARCH4R55TZ8A2G.json`
  - `01KX80EXDZPA0J75NF6VJ0BT4K.json`

The local sidecar and by-key lake projection parsed to identical JSON. Their
raw bytes differed only because the Windows sidecar used CRLF while the lake
record used canonical LF.

## Observed Source-Visible Values

| Field | Observed value |
| --- | --- |
| Product id / SKU | `B07XXPHQZK` |
| Price | `24.0` |
| Currency | `USD` |
| Availability | `In Stock` |
| Rating | `4.6` |
| Review/rating count | `36,963` |
| Best-seller rank | `#218 in Beauty & Personal Care`; `#4 in Lip Balms & Moisturizers` |

The generic projection emitted product, variant-offer, review-substrate, and
carried-module rows with no projection residual. The Silver producer selected
only product context, variant offer, and review substrate.

## Silver Outcome

- Emitted payloads: `ProductEntity`, `RetailOfferObservation`, and
  `RetailReviewAggregateObservation`.
- All three records passed the Silver envelope validator.
- All three records returned `source_backed_complete` from the Silver lineage
  read-side gate.
- Every derived ref named the exact projection record above and carried a row
  locator.
- `exact_inventory_quantity`, `exact_stock_quantity`, and `sold_units` were not
  present in the offer observation. No zero, estimate, or inferred value was
  emitted.

## Non-Claims

This receipt is not current Amazon evidence, route authority, capture
authorization, a reusable batch-session proof, Cleaning, Gold/Judgment,
acceptance, deployment readiness, exact inventory, exact sold units, demand
proof, or product proof. Re-run the pinned profile and the exact-record producer
for any claim that depends on current source state.
