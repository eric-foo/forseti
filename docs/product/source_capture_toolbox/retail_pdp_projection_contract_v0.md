# Retail/PDP Projection Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product contract / playbook for Retail PDP mechanical projection
scope: >
  Retail/PDP raw-packet-to-projection contract for Amazon, Sephora, and Ulta:
  what capture must preserve, what projection may emit, what residuals mean,
  and what remains outside projection until a later owner-authorized lane.
use_when:
  - Stabilizing or reviewing the Retail/PDP projection slice and its bounded capture-to-projection wiring.
  - Checking Amazon, Sephora, or Ulta product/offer/review binding limits.
  - Deciding whether the next move is playbook review, sidecar capture wiring, retailer recon, or ECR sequencing.
authority_boundary: retrieval_only
open_next:
  - docs/product/source_capture_toolbox/retail_pdp_sidecar_operator_playbook_v0.md
  - docs/product/core_spine_v0_projection_doctrine_v0.md
  - docs/product/data_capture_spine/demand_durability_multi_retailer_rendered_capture_spec_v0.md
  - orca-harness/runners/run_source_capture_cloakbrowser_packet.py
  - orca-harness/source_capture/retail_pdp_projection.py
  - orca-harness/tests/unit/test_retail_pdp_projection.py
  - orca-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py
stale_if:
  - Retail PDP projection code changes row kinds, residual vocabulary, required bindings, or retailer parsing posture.
  - Multi-retailer rendered capture posture changes for Amazon, Sephora, or Ulta.
  - Projection doctrine changes raw-canonical, carry-or-residualize, or no-salience-decision rules.
```

## Status

Status: `CONTRACT_V0`.

This contract is a docs-first stabilization surface for the current Retail/PDP
projection slice. It is not implementation authorization, not capture execution,
not ECR sequencing, not Cleaning, not Judgment, not validation, and not readiness.

The implemented capture-side wiring is bounded and opt-in: the CloakBrowser
packet runner can write a separate Retail/PDP projection JSON after a successful
packet write when `--source-family retail_pdp --retail-pdp-projection-output`
are supplied.

## Purpose

Retail PDPs are useful to Orca only if the source-visible product, offer, and
review facts remain tied to the raw retailer packet that produced them. The goal
is not to make retailer pages look clean. The goal is to preserve a narrow,
mechanical row view over raw capture bytes so downstream layers can inspect:

- which product/SKU/variant was captured;
- which price, currency, availability, and review substrate were source-visible;
- which retailer-specific fallbacks were unsafe and visibly residualized;
- which facts came from rendered DOM, visible text, embedded structured JSON, or
  carried frame-sensitive modules; and
- which gaps remain visible before ECR, Cleaning, or Judgment acts.

Raw remains canonical. Projection is a re-derivable view.

## Source Read Ledger

| Source | Why read | Supported claim |
| --- | --- | --- |
| `AGENTS.md` and `.agents/workflow-overlay/README.md` | Orca project authority and overlay binding | Docs-write work must stay inside Orca authority and visible boundaries. |
| `.agents/workflow-overlay/source-loading.md` | Source-loading and capture/projection read-pack route | Capture-spine activity starts from the source-capture playbook; raw-to-Judgment projection opens projection doctrine. |
| `.agents/workflow-overlay/source-of-truth.md` | Doctrine-change propagation rule | This new product contract carries an inline propagation receipt. |
| `.agents/workflow-overlay/artifact-folders.md` and `retrieval-metadata.md` | Placement and retrieval-header rules | New durable product artifacts belong under `docs/product/` and need retrieval metadata. |
| `docs/product/source_capture_toolbox/source_capture_playbook_v0.md` | Capture method boundary | Retail capture must locate the signal substrate first and preserve source-native bytes, not paraphrase. |
| `docs/product/source_capture_toolbox/capture_recon_index_v0.md` | Existing recon evidence | Sephora progressive-scroll/Bazaarvoice and Ulta Apollo state are reported as worktree-pending recon; Amazon recon remains open in the rendered-capture spec. |
| `docs/product/source_capture_toolbox/retail_pdp_sidecar_operator_playbook_v0.md` | Operator procedure | Exact Amazon/Sephora/Ulta sidecar smoke commands, output inspection contract, failure taxonomy, merge-conflict posture, and code-enforceable follow-up flags. |
| `docs/product/core_spine_v0_projection_doctrine_v0.md` | Projection doctrine | Raw is canonical; projection is a view; Retail/PDP must preserve SKU/variant/price, availability, review-substrate, per-retailer/locale series, and embedded JSON. |
| `docs/product/data_capture_spine/demand_durability_multi_retailer_rendered_capture_spec_v0.md` | Multi-retailer rendered capture spec | Per-retailer series, substrate-first posture, and Amazon/Sephora/Ulta source-access status. |
| `orca-harness/runners/run_source_capture_cloakbrowser_packet.py` | Current capture-side wiring | `--retail-pdp-projection-output` is an opt-in Retail/PDP-only sidecar after packet write; it does not change packet schema, fetch, clean, judge, or feed ECR. |
| `orca-harness/source_capture/retail_pdp_projection.py` | Current implementation | Row kinds, binding map, residual names, no-Judgment-field guard, and structure-preservation rule. |
| `orca-harness/tests/unit/test_retail_pdp_projection.py` and `orca-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py` | Current behavioral tests | Amazon, Sephora, Ulta, unsafe fallback, no-Judgment-smuggling, structure-preserved behavior, and opt-in capture-runner sidecar gating. |

## Contract

### Capture Input Required

Retail projection consumes an existing `SourceCapturePacket` plus preserved raw
file bytes. It does not fetch, browse, enrich, or choose sources.

For a PDP slice to be projectable, the raw packet should preserve:

- rendered DOM HTML for the PDP slice;
- visible text for fallback and module detection;
- packet and slice identifiers, file hashes, hash basis, source locator,
  `series_id`, locale pin, currency pin, variant pin, capture time, cutoff
  posture, access posture, and archive-history posture;
- embedded structured JSON when the retailer exposes it in the captured HTML;
- enough rendered structure to anchor product, variant, price, availability, and
  review substrate; and
- raw screenshot/media as packet evidence when captured, even when the current
  projection only ledger-collapses hero imagery or cart/notify chrome.

Retailer-specific capture details that now matter to projection:

- Amazon: rendered DOM should preserve ASIN, the target DOM price input,
  availability text, average-customer-review nodes, and any delivery-location
  limitation or ZIP pin used for US storefront comparability.
- Sephora: rendered DOM should preserve the target `ProductPage` root attributes
  such as `data-cnstrc-item-price`, `data-cnstrc-item-id`, and
  `data-cnstrc-item-variation-id` when present; recommendation-card
  `product_list_price` fields are carried only as frame context, not as target
  product price.
- Ulta: rendered DOM should preserve JSON-LD plus `window.__APOLLO_STATE__`,
  including the requested SKU context that can differ from the projected SKU.

If rendered DOM HTML is missing, projection must emit a residual rather than
fabricating rows.

### Projection Output Allowed

The current projection view may emit only these row families:

| Row kind | Meaning |
| --- | --- |
| `retail_pdp_product` | Packet/slice-level product context: retailer, source locator, series, pins, timing, cutoff, and archive posture. |
| `retail_variant_offer` | Source-visible SKU/product/variant/price/currency/availability facts plus source-visible binding provenance such as `price_isolation`, `price_binding_source`, `dom_price`, `apollo_requested_sku`, or `apollo_sku` when the raw packet exposes them. |
| `retail_review_substrate` | Source-visible review-count/rating substrate and how it was located. |
| `retail_embedded_structured_json` | Raw JSON-LD or Apollo-state text preserved verbatim with parse status. |
| `retail_carried_module` | Frame-sensitive modules such as shipping, loyalty, and recommendations carried as visible context, not trusted as target product/review facts. |

Projection may emit these bindings:

- `sku_variant_price`;
- `variant_availability`;
- `review_substrate_for_product`;
- `series_locale_currency`;
- `structured_json_for_product`;
- `module_carried`.

Projection must not emit credibility, integrity, demand, discounting,
inclusion/exclusion, Signal Use, Decision Strength, Action Ceiling, or any
Judgment-facing label. Current code rejects source-visible field names that
smuggle those concepts.

### Structure And Residual Semantics

`structure_preserved` is true only when the required retail bindings are present:

- `sku_variant_price`;
- `variant_availability`;
- `review_substrate_for_product`;
- `series_locale_currency`.

Residuals are not failures by themselves. A residual is a visible gap, fallback
warning, mismatch, or absent substrate that travels with the view so downstream
work cannot mistake a brittle carry for a clean fact.

Known residual classes include:

| Residual | Meaning |
| --- | --- |
| `retail_pdp_rendered_dom_absent` | No rendered PDP HTML was available for the slice. |
| `<slice>:<retailer>:variant_offer_absent` | Projection could not locate a variant/offer binding. |
| `<slice>:<retailer>:review_substrate_absent` | Projection could not locate the review substrate. |
| `amazon_price_from_unanchored_visible_text_fallback` | Amazon price came only from a position-dependent visible-text `$N` fallback, not the target DOM price input. |
| `sephora_price_from_structured_json_without_target_dom_price` | Sephora price came from structured JSON while the target `ProductPage` DOM price binding was absent; carry it as source-visible but residualized. |
| `sephora_review_count_from_unanchored_fallback` | Sephora review count came only from an unanchored visible-text review pattern, not the target `Ratings & Reviews (N)` widget. |
| `sephora_ld_json_review_count_differs_from_target_dom` | Sephora structured JSON review count differs from the target DOM review widget. |
| `ulta_ld_json_apollo_<field>_mismatch` | Ulta JSON-LD and Apollo state disagree for a variant field such as SKU, product ID, price, or availability. |
| `ulta_requested_sku_differs_from_projected_sku` | Ulta requested SKU context differs from the projected variant SKU, even when JSON-LD and Apollo agree with each other. |
| `ulta_ld_json_apollo_review_count_mismatch` / `ulta_ld_json_apollo_rating_mismatch` | Ulta JSON-LD and Apollo state disagree for review substrate values. |
| `<structured_kind>_<index>_malformed_json` | Embedded structured JSON was preserved but could not be parsed. |

`hierarchy_preserved=True` is vacuous for current PDP projection. PDPs do not
have thread parent/reply hierarchy; their structure is the product/variant/price
/availability/review binding map above.

### Retailer Postures

| Retailer | Capture substrate to preserve | Projection posture | Binding limits |
| --- | --- | --- | --- |
| Amazon | Rendered DOM plus visible text; US storefront/locale/currency pins when the capture series requires comparability. | Current projection reads ASIN, DOM target price input, availability text, average customer review nodes, and best-sellers-rank text; it carries shipping, loyalty, and recommendation modules. | If the DOM price input is absent, the visible-text price fallback is residualized because it can pick up store-card or promo amounts. Amazon capture recon remains the open source-access question in the multi-retailer rendered-capture spec. |
| Sephora | Rendered DOM after the review area has actually loaded; Bazaarvoice configuration and target review widget should be preserved when present. | Current projection preserves JSON-LD verbatim, uses the target `ProductPage` DOM root price when present, uses structured product/offer fields otherwise, treats `Ratings & Reviews (N)` as the target review count, and carries recommendation review-count examples separately. | Recommendation prices and counts are not the target substrate. Bare `<token> Reviews` fallback is residualized. JSON-LD disagreement with the target DOM review widget is residualized. Structured JSON price is carried but residualized when the target DOM price binding is absent. |
| Ulta | Rendered DOM carrying JSON-LD and `window.__APOLLO_STATE__`; requested SKU context should remain visible. | Current projection preserves JSON-LD and Apollo state verbatim, prefers/merges Apollo offer fields, carries `apollo_requested_sku`, compares JSON-LD against Apollo for mismatches, and compares requested SKU context against the projected variant SKU. | JSON-LD/Apollo disagreements are residualized. Requested/projected SKU disagreement is residualized even when embedded substrates agree with each other. Apollo state is a source-visible embedded-state substrate, not an authority to normalize away SKU or review mismatches. |

### What Must Stay Out

Projection must not:

- fetch retailer pages, run browsers, retry blocked captures, or decide source
  access posture;
- clean, normalize, dedupe, cluster, translate, summarize, or judge facts;
- decide salience, demand relevance, independence, credibility, or strength;
- convert residuals into exclusion or failure labels;
- treat frame-sensitive shipping, loyalty, or recommendation modules as target
  SKU/price/review facts; or
- sequence ECR before the source-visible projection layer has preserved its
  gaps.

## Next Move Gate

The next safest move is **not** automatic ECR. With bounded opt-in sidecar
wiring available, the next move is one of:

1. **Targeted recapture/reprojection checks** for new retailer edge cases, such
   as Sephora review-count precision, Ulta requested-SKU mismatch variants, or
   Amazon storefront/location posture.
2. **Use or recheck the opt-in sidecar** for already bounded Retail PDP
   CloakBrowser packet outputs:
   `--source-family retail_pdp --retail-pdp-projection-output <path>`, using
   this contract as the behavior surface and preserving residuals unchanged.
   Use `retail_pdp_sidecar_operator_playbook_v0.md` for the current
   Amazon/Sephora/Ulta smoke commands and inspection checklist.
3. **Retailer recon closure** if the immediate bottleneck is source-access
   posture rather than projection behavior.

Auto-project-after-capture behavior is acceptable only as bounded opt-in sidecar
wiring against this contract. It must not become a generic packet writer
responsibility, hide residuals, silently trust fallbacks, or feed ECR facts that
projection could not anchor.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Added a Retail/PDP projection contract/playbook that binds the current
    Amazon, Sephora, and Ulta raw-packet-to-projection slice: raw remains
    canonical, projection is a view, unsafe retailer fallbacks are carried only
    with visible residuals, ECR/Cleaning/Judgment remain downstream, and the
    bounded sidecar operator path is documented without promoting scratch
    packets into fixtures.
  trigger: product_doctrine
  related_triggers:
    - architecture_doctrine
    - output_authority
  controlling_sources_updated:
    - docs/product/source_capture_toolbox/retail_pdp_projection_contract_v0.md
    - docs/product/source_capture_toolbox/retail_pdp_sidecar_operator_playbook_v0.md
    - docs/product/source_capture_toolbox/README.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - orca-harness/docs/source_capture_agent_runbook.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/product/core_spine_v0_projection_doctrine_v0.md
    - docs/product/data_capture_spine/demand_durability_multi_retailer_rendered_capture_spec_v0.md
    - docs/product/source_capture_toolbox/source_capture_playbook_v0.md
    - docs/product/source_capture_toolbox/capture_recon_index_v0.md
    - orca-harness/docs/source_capture_agent_runbook.md
    - orca-harness/source_capture/retail_pdp_projection.py
    - orca-harness/tests/unit/test_retail_pdp_projection.py
  intentionally_not_updated:
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Existing source-loading already routes capture-spine activity to the
        capture playbook and raw-to-Judgment projection work to projection
        doctrine; this artifact is reachable through the Armory README and Data
        Capture submap without changing the read-pack rule.
    - path: docs/product/source_capture_toolbox/capture_recon_index_v0.md
      reason: >
        This branch ran bounded scratch recapture/reprojection checks, but it
        did not produce a durable recon closeout or fixture-admission decision.
        Do not promote ignored `_test_runs/` packets into recon authority here.
  stale_language_search: >
    rg -n "retail_pdp_projection_contract|retail_pdp_sidecar_operator|Retail/PDP projection|Retail PDP projection|ProductPage|requested SKU"
    docs/product/source_capture_toolbox/README.md docs/workflows/data_capture_spine_consolidation_map_v0.md
    .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md orca-harness/docs/source_capture_agent_runbook.md
  stale_language_search_result: >
    Executed 2026-06-17 in this worktree after Sephora target-DOM price and
    Ulta requested-SKU residual hardening. Hits were updated in the intended
    routing surfaces: this contract, the Source Capture Armory README, the Data
    Capture Spine submap, and the repo map runner/source package route. Capture
    recon index language was intentionally not promoted from scratch packets.
  non_claims:
    - not validation
    - not readiness
    - not owner acceptance
    - not implementation authorization
    - not capture execution
    - not ECR, Cleaning, Judgment, buyer proof, or source completeness proof
```
