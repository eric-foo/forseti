# Forseti Ulta PowerReviews Review Capture Proof v0

```yaml
retrieval_header_version: 1
artifact_role: Capability proof report (research family)
scope: >
  Records the Gate 1 native review-ID semantics proof, the found/missing
  information matrix against the Sephora extraction target, and the landed
  Ulta-specific PowerReviews adapter for the commissioned Night Shift PDP
  route. One bounded onboarding lane only: no volume capture, monitoring runs,
  other retailers, or Bazaarvoice work.
use_when:
  - Deciding whether Ulta structured review capture is a proven, truthful route.
  - Consuming the Ulta PowerReviews adapter, its packets, or its loss ledger.
  - Reconciling the retailer capability set's Ulta row with landed evidence.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md
  - docs/research/retail_pdp_review_record_capture_recon_v0.md
  - docs/research/forseti_beauty_retailer_surface_probe_results_v0.md
stale_if:
  - Ulta materially changes its review platform, PowerReviews display route, or
    page-declared render configuration.
  - A later accepted capture supersedes the bounded onboarding packets below.
  - The retailer capability set is changed by a later accepted study.
```

## 1. Receipt and Load Outcome

- Workspace: isolated worktree
  `C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\ulta-powerreviews-adapter-9c4df6`,
  branch `claude/ulta-powerreviews-adapter-9c4df6`, started clean at
  `HEAD bbb2bd8d` (equal to `origin/main` at start).
- Commission prompt: `docs/prompts/handoffs/ulta_powerreviews_review_capture_commission_prompt_v0.md` — does not exist yet on any branch (untracked authoring copy in the sibling research worktree `beauty-retailer-corpus-research-2a49fa`; blob `530bb2ca`).
  This report is its commissioned output; no collision — this report did not
  exist at start.
- Source load (`REUSE`/`REFRESH` from current bytes; blob prefixes recorded):
  `AGENTS.md` `be4aa889`; `.agents/workflow-overlay/README.md` `e05f8e6f`;
  preflight defaults `b2f8c5a7`; extraction standard `df63fb8c`; recon report
  `e22ce684`; surface-probe results `ff3f8e92`; Bazaarvoice handoff (bounded
  sections) `039fd0fd`; `retail_capture_profiles.py` `0f74cd61`;
  `sephora_onboarding_capture.py` `4376bb4b`; `sephora_bazaarvoice.py`
  `65080d1f`; corpus research (untracked sibling-worktree copy, bounded
  sections 6/9/12/18) `c8158b73`. `SOURCE_CONTEXT_READY` was declared before
  route work; historical packets were treated as route evidence only and all
  Ulta page state was freshly verified live.

## 2. Gate 1 — Native Review-ID Semantics: PROVEN

The recon's typed risk (`GO_WITH_ID_SEMANTICS_RISK`; `FIELD_RISK` item 3) is
resolved with preserved evidence on the commissioned pin-proven PDP
(`pimprod2046225`, SKU `2645443`; one PDP sufficed — no second product was
needed):

| Evidence | Packet | Content |
| --- | --- | --- |
| Fresh admitted rendered DOM | `01KY1ZR7NTR633VE4HQ8TKAM97` (`F:\forseti-data-lake\raw\b3e\...`) | `--ulta-market US` assertion route, `pin_confirmed=true`, `access_blocked=false`, no proxy/profile/geoip; DOM contains the `PowerReviewsRender` config block and five rendered `pr-rd-review-headline-<id>` rows |
| Display-route fixture + cross-check receipt | `01KY1ZWAZFJ3CR34WDB617Y6RA` (`F:\forseti-data-lake\raw\16e\...`) | Exact reviews and questions display-response bytes (SHA-256 in manifest), token-free request manifest, and the per-row cross-check receipt |

Cross-check result: **all five** rendered headline suffixes
(`584192247`, `580013849`, `579948269`, `578859756`, `576140820`) are present
as structured `review_id` values with byte-identical headline text, and
`review_id == ugc_id` on every captured row (a distinct
`internal_review_id` also exists and is preserved but is not the native
display identity). Verdict: `NATIVE_REVIEW_ID_MAPPING_PROVEN`. The numeric
DOM-headline suffix **is** the native PowerReviews review ID, so it is a
truthful monitoring-anchor identity.

Method order followed the commissioned sequence: (1) preserved packets and
embedded state (pin packet `01KXWQW45J2C17RX4397Z27KYJ` page-declares the full
`POWERREVIEWS.display.render` configuration; JSON-LD carries 5 `Review`
objects and the 671/4.3 aggregate), (2) an ordinary live PDP load with
rendered-row observation, (3) the page-declared public display route
(`display.powerreviews.com`, page-declared public display key used in memory
only and never persisted), (4) rendered DOM cross-check. A retailer-owned
endpoint (step 5) was not needed. No auth, CAPTCHA, proxy, gate defeat, or
full-corpus pagination was used.

## 3. Found/Missing Matrix vs the Sephora Extraction Target

Source vocabulary observed live on the reference PDP: source filter
`Filter Reviews By Source` = `Reviewed at Ulta.com` (default) / `All reviews`;
sorts `Most Recent` (default), `Most Helpful`, `Lowest Rated`,
`Highest Rated`, `Oldest`, `Images`; a variant filter; review search; Q&A
sorts `Newest` / `Oldest` / `Most Answers`.

| Information class (Sephora target) | Ulta status | Evidence |
| --- | --- | --- |
| Product identity, variant/SKU state, price, availability | `observed` | Carried by the existing admitted `ulta_pdp_aggregate`/pin route (9 projection rows, 0 residuals); not rebuilt |
| Source-labelled helpful/top-ranked response, exact order, every row field | `observed` | `sort=MostHelpful` (rendered label `Most Helpful`), helpful_votes descending 23→…; 100 rows preserved |
| Source-labelled most-recent response + native last-seen anchor | `observed` | `sort=Newest` (rendered label `Most Recent`), created_date descending; anchor `584192247` |
| Aggregates: rating, exact count, histogram, recommendation % | `observed` | Rollup: `average_rating 4.31`, `review_count 672`, `rating_histogram`, `recommended_ratio 0.85`; rendered page showed 671 vs structured 672 — an in-flight count drift class the adapter records rather than reconciles |
| Per-row: native ID, title, body, date, author, verified state, votes, media | `observed` | Row fields: `review_id`/`ugc_id`/`internal_review_id`/`legacy_id`, headline, comments, created/updated dates, nickname, location, `badges.is_verified_buyer` / `is_verified_reviewer` / `is_staff_reviewer`, helpful/not-helpful votes + `helpful_score`, media, `product_variant`, gtin/upc |
| Incentive/sampling disclosure | `observed` (per-row + aggregate) | `details.disclosure_code: "sampling"` on disclosed rows; rollup `native_sampling_review_count 460` of 672 (~68%), `native_sweepstakes_review_count 0` |
| Source-proven non-incentivized filter | `not_exposed` | No display-route incentive filter proven; unfiltered baseline preserved; no Sephora filter parity fabricated |
| Syndication markers | `observed` (aggregate) | Rollup `syndicated_review_count 0` on an all-native corpus; the widget's `Reviewed at Ulta.com`/`All reviews` source filter exists, but its display-route parameter is unverifiable on this all-native product |
| Reviewer-attribute facets | partially `observed` / `not_exposed` (aggregate) | Per-row `properties` facets with exact labels `Pros`, `Cons`, `Best Uses`, `Describe Yourself`, `Was this a gift?`, `Skin Type` when reviewers supplied them; no aggregate age/skin distributions with denominators |
| AI sentiment chips | `observed` (provider form) | Rollup `faceoff_positive` / `faceoff_negative`; rendered pros/cons chips with counts (e.g. `Hydrating 35`, `Sticky 26`) |
| Q&A | `observed` | 3 questions, 3 declared = 3 included answers, with `author_type: EXPERT` brand-engage answer metadata, votes, and `is_seeded` |

## 4. Adapter Implementation and Test Evidence

Landed, retailer-native (never labelled Bazaarvoice):

- `forseti-harness/source_capture/adapters/ulta_powerreviews.py` — resolves
  the page-declared `script#PowerReviewsRender` →
  `POWERREVIEWS.display.render({...})` configuration (api key in flight only;
  merchant `6406`, group `11984`, locale `en_US`) and carries the no-proxy
  display transport. The display route's observed 25-row page cap is encoded
  as a route boundary.
- `forseti-harness/source_capture/ulta_onboarding_capture.py` — three-role
  companion from a hash-verified, pin-admitted parent packet: bounded
  `MostHelpful` and `Newest` offset pages (default 4×25 = 100 rows per role)
  plus one Q&A response; exact raw bytes with hashes; token-free request
  manifest; compact body-free summary rows carrying IDs/ranks/dates/counts/
  raw-file references; explicit loss ledger; fail-loud nonzero raw fallback
  (exit 4 acquisition / exit 5 adaptation, partial bytes always preserved);
  append-only retention. Hard gates: parent `ulta_us_market_assertion` with
  `pin_confirmed=true` and no access block; URL product id ==
  page-declared `page_id`; every row bound to that `page_id`;
  `review_id == ugc_id` on every row (Gate 1 invariant); unique IDs;
  order verification per role; key-echo refusal; zero-rows-with-declared-total
  refusal.
- `forseti-harness/runners/run_source_capture_ulta_onboarding.py` — CLI on
  the existing packet seam, with lake-seam wiring reconciled in
  `data_lake/inventory.py` (explicit data-root reason + identity binding),
  `source_capture/source_classification.py`
  (`ulta_powerreviews_onboarding`), the seam-coverage contract list, and the
  regenerated `lake_touchpoint_inventory_v0.json`.
- `forseti-harness/tests/unit/test_ulta_onboarding_capture.py` — 13 focused
  tests mirroring the Sephora/Target coverage classes: success without
  body/key duplication, acquisition fail-loud with partial preservation,
  adaptation fail-loud raw fallback (native-ID invariant break and foreign
  product row), identity-mapping and pin/sufficiency refusals before any
  network read, key-echo refusal, route page-cap rejection, corrupt-response
  preservation, and config-resolution failure shapes. All pass, plus the
  lake-seam and inventory contract gates.

Live proof packet: `01KY20GH02FH8CCSAV2D6M9NKR`
(`F:\forseti-data-lake\raw\c38\...`), exit code 0 — 100 Most Helpful rows +
100 Most Recent rows of 672 declared, 3 questions with all declared answers,
anchor `584192247`, aggregates and sampling counts preserved, request manifest
verified key-free, `content_qualification.status = passed`.

Monitoring-anchor semantics only: the packet records the native last-seen
review ID; no scheduler, monitoring run, or universal review abstraction was
built. PowerReviews mechanics remain provider-specific to Ulta until a second
PowerReviews retailer proves identical public mechanics.

## 5. Loss Ledger and Non-Claims

- Bounded window: 100 + 100 of 672 declared reviews; the display route caps
  each response at 25 rows; not the complete historical corpus.
- Incentive semantics: no source-proven non-incentivized filter; the
  unfiltered baseline is preserved with per-row `disclosure_code` and rollup
  sampling counts (460 of 672 sampling); no incentive filter applied or
  claimed.
- Syndication filter parameter unverified (all-native product); rollup
  `syndicated_review_count` preserved; no syndication filter claimed.
- No aggregate reviewer demographic distributions with denominators; per-row
  `Describe Yourself` / `Skin Type` properties remain raw-only.
- Linked review/answer media bytes not fetched (references preserved).
- Rendered 671 vs structured 672 review-count drift preserved as a
  disagreement, not reconciled.
- Non-claims: no volume capture; no monitoring readiness or runs; no
  demographic representativeness; no sales, velocity, or revenue inference;
  no Bazaarvoice-sequence (Kohl's/Nordstrom) or Sephora/Target runtime
  contact; no production readiness.

## 6. Completion Status

`ROUTE_PROVEN_ADAPTER_LANDED`
