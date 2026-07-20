# Retail PDP Review Record Capture Recon v0

```yaml
retrieval_header_version: 1
artifact_role: Research recon report
scope: Evidence-only capture-spine recon for extending retail PDP capture from aggregate review substrate to individual review_record Attachment Records.
use_when:
  - Deciding whether retail PDP individual review capture is ready for implementation scoping.
  - Comparing Amazon, Sephora, and Ulta source-visible per-review field shape.
  - Preparing the minimal retail_pdp review_record adapter scope after Attachment Record storage binding is locked.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_content_cleaning_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  - orca-harness/source_capture/retail_pdp_projection.py
stale_if:
  - Amazon review-page access posture changes under the measured no-gate-defeat route.
  - Sephora or Ulta review modules materially change their rendered DOM/state shape.
  - Attachment Record physical storage or writer binding is implemented or changed.
  - A later retail_pdp review_record recon supersedes this report.
```

- Status: `RECON_COMPLETE_BUILD_NOT_READY`.
- Lane branch/worktree: `codex/retail-pdp-review-recon` under `.codex/worktrees/retail-pdp-review-recon`.
- Probe date: 2026-06-20.
- This is evidence organization, not a source-family spec, not implementation authorization, not product readiness, and not capture execution at volume.

## Boundary

The lane tested the smallest useful question: whether existing retail PDP packet capture exposes source-visible individual review records for Amazon, Sephora, and Ulta without auth, proxy use, CAPTCHA solving, source discovery, or gate defeat.

It did not build adapters, write `review_record` Attachment Records, add graph/dedup/identity/integrity logic, run volume capture, or land anything to `main`.

## Inputs Read

Controlling and support inputs:

- Commission prompt: `.claude/worktrees/distracted-ishizaka-01eff5/docs/prompts/handoffs/retail_pdp_review_capture_commission_prompt_v0.md`.
- Branch-only review capture spec: `.claude/worktrees/distracted-ishizaka-01eff5/orca/product/spines/capture/source_families/retail_pdp/retail_pdp_review_capture_spec_v0.md`.
- Branch-only manufactured-demand design: `.claude/worktrees/distracted-ishizaka-01eff5/orca/product/spines/judgment/demand_read/integrity/judgment_spine_manufactured_demand_detection_design_v0.md`.
- Established mainline retail substrate: `orca/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_contract_v0.md`.
- Existing operator playbook and toolbox: `orca/product/spines/capture/core/source_families/retail_pdp/retail_pdp_sidecar_operator_playbook_v0.md`, `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`, `orca/product/spines/capture/core/source_capture_toolbox/source_capture_anti_block_ladder_usage_guide_v0.md`, `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`.
- Attachment Record contracts: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md`, `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md`, `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`.
- Existing harness code: `orca-harness/source_capture/retail_pdp_projection.py`, `orca-harness/runners/run_source_capture_cloakbrowser_packet.py`, `orca-harness/runners/run_source_capture_http_packet.py`, `orca-harness/runners/run_source_capture_durability_series.py`, `orca-harness/source_capture/models.py`.

Retrievability note: the commission prompt, the branch-only review capture spec, and the branch-only manufactured-demand design above live only in the `.claude/worktrees/distracted-ishizaka-01eff5` local worktree. They are not tracked on this branch (`codex/retail-pdp-review-recon`) or on `origin/main`, so a fresh reader on this branch cannot open them; treat their content as reported, not retrievable here. By contrast, the retail PDP projection contract, the Attachment Record implementation contract, and `retail_pdp_projection.py` cited above are tracked and retrievable on this branch.

## Reuse Inventory

Existing reusable substrate:

- `run_source_capture_cloakbrowser_packet.py` already writes source-capture packets and can optionally write a retail PDP projection over preserved rendered bytes.
- `run_source_capture_http_packet.py` is useful as a rung-0 direct HTTP control.
- `retail_pdp_projection.py` already emits aggregate row kinds: `retail_pdp_product`, `retail_variant_offer`, `retail_review_substrate`, `retail_embedded_structured_json`, and `retail_carried_module`.
- The current projection explicitly stays capture/projection-only and does not call ECR, Cleaning, or Judgment.

Missing or deferred substrate:

- No `review_record` row kind or Attachment Record writer exists in `orca-harness` on this branch.
- `Attachment Record` implementation authority exists as a contract shape, but exact packet-member versus sidecar body layout, manifest/index serialization, backend binding, and writer seam remain deferred.
- Therefore a source adapter can be scoped, but a durable `review_record` write path cannot be honestly called implementation-ready yet.

## Live Recon Packets

All packet artifacts are local scratch under `orca-harness/_test_runs/retail_pdp_review_recon_20260620/`, which is gitignored and untracked. The byte counts, row counts, and packet IDs in the table below are reported from that local scratch; they are not committed and cannot be independently reproduced or verified from this branch. Treat them as reported evidence, not repo-verifiable fixtures.

The `Verdict` column records source-access verdicts for scoping only — whether per-review fields are source-visible without gate defeat (`GO`/`PARTIAL_GO`/`NO_GO`). They are not build authorization; build readiness is governed by the `RECON_COMPLETE_BUILD_NOT_READY` status above and the Blockers below.

| Target | Packet | Observed access / source shape | Verdict |
| --- | --- | --- | --- |
| Amazon review page, rendered: `https://www.amazon.com/product-reviews/B07XXPHQZK?sortBy=recent` | `amazon_review_page_01`, packet `01KVJ5HTQ8644NCWYQY12762A5` | CloakBrowser preserved an Amazon continue-shopping/interstitial page. Manifest limitation: `access_failed: ... amazon_continue_shopping_interstitial`. Visible text was 149 bytes. | `NO_GO_FOR_REVIEW_PAGE_ROUTE_IN_THIS_ENVIRONMENT`. Do not click/solve/escalate through the challenge under this commission. |
| Amazon review page, direct HTTP control: same URL | `amazon_review_page_direct_http_00`, packet `01KVJ5KB9Z0JQFS32PY991D5VF` | HTTP 200 with 5,125 bytes, but marker scan found `opfcaptcha.amazon.com` and continue-shopping body, not review records. | Confirms the rendered block was not just a browser artifact. |
| Amazon alternate slugged review URL | `amazon_review_page_alt_01`, packet `01KVJ5RZFR0SDTA30VQ2K1JQKB` | Rendered DOM was only 2,343 bytes; title was `Page Not Found`; visible text was 1 byte. | Invalid route, not evidence of review availability. |
| Amazon canonical PDP: `https://www.amazon.com/Laneige-Sleeping-Berry/dp/B07XXPHQZK` | `amazon_pdp_control_01`, packet `01KVJ5V0AGNY7GDGK7BY2Z2JV3` plus projection JSON | PDP reachable with ZIP `10001` confirmed. Projection rows: product 1, variant offer 1, review substrate 1, carried module 2, residuals 0. DOM includes per-review blocks with `data-reviewid`, `data-hook="reviewTitle"`, `data-hook="review-date"`, `data-hook="review-star-rating"`, `data-hook="avp-badge"`, and review text containers. | `PARTIAL_GO`: PDP-embedded top reviews are source-visible; all-review pagination remains blocked in this environment. |
| Sephora PDP: `https://www.sephora.com/product/lip-sleeping-mask-P420652` | `sephora_pdp_review_recon_01`, packet `01KVJ5Z013Q6703N0R1NQW4H64` plus projection JSON | PDP reachable. Projection rows include product 1, variant offer 1, review substrate 1, embedded structured JSON 5, carried module 3. Review substrate sees Bazaarvoice API config, rating `4.3`, and review count `22K`; one expected residual records JSON-LD versus target-DOM review-count disagreement. Visible rendered rows show timestamps, titles, variants, text bodies, helpful counts, reviewer labels, skin/profile labels, verified-purchase flags, incentive/recommendation flags, and image metadata keyed by Bazaarvoice review IDs. Star rating labels are present as `aria-label` values. | `GO_WITH_NATIVE_ID_MAPPING_RISK`: enough per-review source-visible fields for adapter scoping; verify native review ID mapping for non-image rows before code. |
| Ulta PDP: `https://www.ulta.com/p/night-shift-overnight-lip-mask-pimprod2046225?sku=2645443` | `ulta_pdp_review_recon_01`, packet `01KVJ6287Y09XBT4XKS2YEDNQX` plus projection JSON | PDP reachable. Projection rows include product 1, variant offer 1, review substrate 1, embedded structured JSON 3, carried module 3, residuals 0. Review substrate sees Apollo and JSON-LD rating `4.3` and review count `671`. JSON-LD includes 5 `Review` objects with title, body, date, author, location, and rating. Rendered PowerReviews DOM includes numeric headline IDs such as `pr-rd-review-headline-580013849`, review headline classes, helpful controls, recommendation text, and sort/filter state. | `GO_WITH_ID_SEMANTICS_RISK`: enough per-review fields for adapter scoping; confirm whether PowerReviews numeric headline suffix is the native review ID before binding. |

## Field Verdicts

Amazon:

- PDP-embedded top reviews expose source-native-looking review IDs (`data-reviewid`), reviewer display names, ratings, titles, review dates, variant attributes, verified purchase badges, review text, media popover anchors, and action metadata.
- The all-reviews page route is blocked by Amazon interstitial/challenge behavior in both rendered and direct-HTTP probes. Treat pagination and full corpus expansion as blocked unless the owner separately authorizes a commercial/provider route that remains inside the no-gate-defeat boundary.

Sephora:

- Aggregate substrate is already supported by the current projection.
- Rendered review rows expose enough field surface for `review_record` extraction: timestamp, title, variant, text body, helpful counts, reviewer display/profile labels, verified purchase, incentive disclosure, recommendation flag, media presence, and star rating labels.
- Native review IDs are clearly visible for review-image metadata. The mapping from every visible review row to a native Bazaarvoice review ID still needs one selector-level verification pass before code.

Ulta:

- Aggregate substrate is already supported by the current projection through JSON-LD plus Apollo state.
- JSON-LD exposes compact per-review records with title, text, published date, author display, location, and rating.
- Rendered PowerReviews DOM exposes additional review UI, helpful controls, recommendation text, and numeric headline IDs. These IDs are likely the path to native review identity but need one verification pass before code treats them as native review IDs.



## 2026-07-21 Amazon compatibility implementation addendum

Owner-directed work after the historical recon tested Amazon against the proven
Sephora extraction inventory. This supersedes the report's
`RECON_COMPLETE_BUILD_NOT_READY` recommendation for the bounded Amazon PDP
top-review surface only; it does not change the Kohl's-first sequence.

- Parent packet `01KY0PHPN10205MKKCK1GB7YH1` exposes 13 Amazon-native rows:
  8 US and 5 other-country top reviews.
- Corrected companion `01KY0S1ZACF3AG467GV6VA8CJN` preserves IDs, ratings,
  titles, authors, dates/locations, variants, verified-purchase badges,
  helpfulness, incentive badges, media references, and exact raw anchors. It
  records aggregate rating `4.6`, count `37,045`, and five-to-one-star
  percentages `81/11/5/1/2`. Bodies remain only in the immutable parent DOM.
- Packet `01KY0S0MYDZQ2CSTF7HE1DD63S` is retained but superseded because its
  first parser pass misread nested accessibility text as `81%` in every star
  bucket.
- No Bazaarvoice marker was found. The provider is
  `amazon_native_rendered_pdp`. Five brand-authored A+ FAQ questions were
  excluded from customer product Q&A.
- Anonymous Amazon review portal `01KY0PDWK6NXH4H24X74P6BVVV` and direct
  HTTP all-review probe `01KY0PFAXN1SBA86S49JKREBXQ` resolved to sign-in.
  Page-declared fragment probe `01KY0R6YVRHNBWF3DPJ826WFSC` returned 404.
  Stricter PDP attempt `01KY0P6N06XWTYAPWS2DR5JGHQ` preserved raw content but
  failed an unrelated distribution-chip criterion.

Explicit losses: no Most Helpful, Most Recent, last-seen anchor, complete
corpus, reviewer age/skin/concern distributions, customer product Q&A, or
independent linked-media-byte capture.

## Recommended Minimal Next Scope

Do not start a full adapter build yet. The next smallest complete step is a selector-level design patch that:

1. Locks a retailer-specific source map for Amazon PDP top reviews, Sephora rendered/Bazaarvoice rows, and Ulta JSON-LD/PowerReviews rows.
2. Defines `review_record` Attachment Record body fields as raw source-visible fields only, keyed by packet ID, slice ID, retailer, product/SKU key, source URL, and native-or-candidate review ID.
3. Marks per-field residuals for absent or unverified fields instead of inventing normalized values.
4. Keeps the extractor packet-local: consume preserved raw bytes and projection context only; do not fetch, browse, paginate, dedupe, score, identify actors, or call downstream lanes.
5. Blocks implementation until the Attachment Record writer/physical representation is bound enough to preserve compact manifest/index entries plus immutable body files without adding direct lake fields.

## Out Of Scope

- No graph construction, reviewer ego graph expansion, deduplication, entity resolution, credibility scoring, integrity verdicts, Judgment labels, Cleaning labels, or downstream routing.
- No auth, credentials, proxy use, CAPTCHA solving, challenge clicking, stored browser profile use, or gate defeat.
- No Amazon all-reviews pagination claim.
- No volume capture or corpus execution.
- No claim that these packet artifacts are production fixtures.

## Blockers / Escalations

1. `BLOCKER`: Attachment Record storage/writer binding is still deferred. Without that, an adapter can at most produce candidate bodies, not durable `review_record` Attachment Records.
2. `FIELD_RISK`: Sephora visible rows need native Bazaarvoice review ID mapping for non-image rows.
3. `FIELD_RISK`: Ulta PowerReviews numeric DOM IDs need native-review-ID semantics verification.
4. `ACCESS_RISK`: Amazon all-reviews pagination is blocked under the tested no-gate-defeat routes. PDP top reviews remain usable for a bounded first extractor.

## Files Written / Preserved

- Durable report: `docs/research/retail_pdp_review_record_capture_recon_v0.md`.
- Local packet scratch root: `orca-harness/_test_runs/retail_pdp_review_recon_20260620/`.
- No source code, tests, prompts, or product-authority specs were changed by this recon.
