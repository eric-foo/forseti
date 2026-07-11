# Retail/PDP Silver Producer Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product contract / generic Retail/PDP Silver producer
scope: >
  Binds the first semantic Silver read path over projection_retail_pdp: one
  retailer-generic Silver-envelope lane, exact projection-record input,
  retailer-local product identity, source-visible offer/review observations,
  and fail-closed raw plus derived lineage. Amazon is the first proof source,
  not a lane or schema boundary.
use_when:
  - Implementing or reviewing the Retail/PDP Silver producer.
  - Checking which projection rows and fields may enter Retail/PDP Silver.
  - Reusing the Amazon-first proof without creating an Amazon-specific lane.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - forseti-harness/source_capture/retail_pdp_silver.py
  - forseti-harness/runners/run_retail_pdp_silver_producer.py
  - forseti-harness/data_lake/lane_registry.py
stale_if:
  - Retail/PDP projection row kinds or raw-ref shapes change.
  - Silver Vault envelope, lineage, or Bronze-intake contracts change.
  - A consumer requires a current-record selection policy rather than an exact pinned projection id.
```

## Status

`CONTRACT_V0`. This contract binds a producer implementation surface. It is not
Cleaning, Gold/Judgment, live-capture authorization, current-record selection,
deployment readiness, or product proof.

## Decision In One Screen

- Lane: `retail_pdp_silver`, registered as `silver_envelope` and written only
  through `append_silver_record`.
- Boundary: retailer-generic. Amazon is the first proof source; no
  `amazon_silver` lane or Amazon-only payload grammar is allowed.
- Input: caller-pinned `(packet_id, projection_record_id)` naming one exact
  committed `projection_retail_pdp` record. The producer never walks or guesses
  among append-only siblings.
- Identity: a `retail_variant_offer` must expose a retailer-local `product_id`
  or `sku`; the entity key is
  `(namespace=retail_pdp:<retailer>, kind=retailer_product, native_id=<id>)`.
- Payload split: `ProductEntity`, `RetailOfferObservation`, and
  `RetailReviewAggregateObservation`.
- Evidence: selected rows carry hash-checkable raw file refs and exact derived
  refs to the projection record with `row_id` plus `row_kind` locators.

The lane deliberately does not use the packet's suggested
`cleaning_retail_pdp_silver` name. The input projection certifies itself as
`not_cleaned`; a Cleaning namespace would encode a transform that did not
occur.

## Input And Binding Contract

The producer reloads the committed raw packet by key and validates the exact
projection JSON against `RetailPdpProjectionPacket`. Before any Silver append,
every selected row must match the raw packet's packet id, slice id, file id,
relative packet path, SHA-256, and hash basis.

Selected row behavior:

| Projection row | Silver use |
| --- | --- |
| `retail_pdp_product` | Required context for the matching slice and retailer; supplies a projection-row lineage edge. |
| `retail_variant_offer` | Required retailer-local identity; emits `ProductEntity` and `RetailOfferObservation`. |
| `retail_review_substrate` | Optional; emits `RetailReviewAggregateObservation` only when a matching variant identity exists. |
| `retail_embedded_structured_json` | Not emitted; remains raw/projection evidence. |
| `retail_carried_module` | Not emitted; remains frame-sensitive context. |

Multiple product, variant, or review rows for the same `(slice_id, retailer)`
are an identity-binding ambiguity and fail closed. No variant row means failure,
not an empty successful run.

## Record Contract

All records use `schema_version=silver_vault_record_v0`,
`producer_schema_version=retail_pdp_silver_v0`, explicit canonical content
hashes, raw/captured times from the committed source slice, and the generic
Silver lineage builder.

- `ProductEntity` contains stable retailer-local identity only. Mutable name,
  price, availability, review, rank, and text fields do not enter the entity.
- `RetailOfferObservation` preserves the selected variant row's
  `source_visible_fields` and residuals without normalization or inference.
- `RetailReviewAggregateObservation` preserves the selected review row's
  `source_visible_fields` and residuals without adjudicating disagreement.
- Every observation subject points to the emitted retailer-local entity key.

Rendered DOM and visible-text files are direct raw packet material, so packet
file refs are the allowed Bronze intake. The producer does not consume a
source-family payload body and therefore does not require an Attachment Record.
If the input later moves behind an Attachment Record body, this contract becomes
stale and must be revised before reuse.

## Unknown And Residual Behavior

The producer never converts absence into zero or an estimate. Exact inventory
quantity and exact sold units remain absent unless a future projection row
contains a source-backed value or explicit posture under a revised contract.
Current row residuals and explicit posture fields are preserved verbatim.

Bought-in-past-month, customer-insight counts, and any other Amazon field not
bound by the current generic projection are outside v0. Their omission is not a
claim that the source lacks them, and it is not permission to read absence as
zero.

## Operator Surface

The bounded runner requires:

```text
run_retail_pdp_silver_producer.py
  --data-root <lake>
  --packet-id <raw packet id>
  --projection-record-id <exact projection record filename>
```

No scheduler, cadence integration, sibling scan, capture action, session state,
or generated read model is introduced by this contract.

## Failure And Validation Contract

Fail before the first append on an absent/malformed projection, packet mismatch,
unverifiable raw ref, unknown retailer, missing stable identity, missing capture
time, ambiguous same-slice identity, orphan review substrate, invalid Silver
envelope, or incomplete source lineage.

Validation must include focused producer tests, the strict Silver lane registry
guard, Silver envelope and lineage tests, reader-selection and lake-seam
contracts after the new files are tracked, `git diff --check`, and the full
harness suite. A passing test suite is not deployment, acceptance, or product
proof.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Added the first generic Retail/PDP Silver producer contract: exact
    projection-record consumption, retailer-local ProductEntity identity,
    source-visible offer/review observations, and fail-closed raw plus derived
    lineage, with Amazon as proof rather than schema boundary.
  trigger: product_doctrine
  related_triggers:
    - architecture_doctrine
    - output_authority
  controlling_sources_updated:
    - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_silver_producer_contract_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - forseti/product/spines/capture/core/source_families/retail_pdp/README.md
    - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
    - forseti-harness/data_lake/silver_record.py
    - forseti-harness/data_lake/silver_lineage.py
    - forseti-harness/data_lake/lane_registry.py
  intentionally_not_updated:
    - path: AGENTS.md
      reason: The project kernel already routes product and implementation authority to owning contracts and the overlay.
    - path: .agents/workflow-overlay/source-loading.md
      reason: Source-pack mechanics are unchanged; the Retail/PDP README and projection contract point to the new producer contract.
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
      reason: The generic Silver envelope and Bronze-intake grammar already permit this domain producer; no lake-wide rule changed.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: The existing Retail/PDP source-family route remains correct and the nearest README now owns discovery of this artifact.
  stale_language_search: >
    rg -n "amazon_silver|cleaning_retail_pdp_silver|retail_pdp_silver|RetailOfferObservation|RetailReviewAggregateObservation"
    AGENTS.md .agents forseti docs forseti-harness
  stale_language_search_result: >
    Executed 2026-07-11. Live hits are the new contract, implementation,
    registry/inventory, focused tests, proof receipt, and nearest discovery
    routes. The retrieval-only handoff was retired after consumption. No live
    authority carries a conflicting lane, payload, or retailer-specific
    instruction.
  non_claims:
    - not validation
    - not readiness
    - not owner acceptance
    - not live capture authorization
    - not Gold or Judgment
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
