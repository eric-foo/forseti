# Clinique Moisture Surge — Sephora-primary override dogfood v0

```yaml
retrieval_header_version: 1
artifact_role: Product-learning dogfood receipt
scope: Test whether authorized Sephora should supersede the otherwise likely retail-primary choice during Understanding and define the smallest complete surrounding retailer capture.
use_when:
  - Adjudicating the proposed retailer-primary and review-corpus rules before changing the Understanding cycle.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md
branch_or_commit: bbb2bd8d3da006f7c6c54f831cdd9ebab377d213
stale_if: Retailer authorization, assortment, providers, page routes, or the selected target market changes; or the owner rejects the proposed rule.
```

**Dogfood status:** DOGFOOD_COMPLETE_SUPPORTED_WITH_GUARDS
**Case:** Clinique Moisture Surge 100H Auto-Replenishing Hydrator, United States
**Authority boundary:** This receipt does not amend Understanding doctrine, authorize acquisition, prove complete assortment coverage, estimate sales, or rank products.

## 1. Bound test

> When a beauty company is authorized at Sephora, should Sephora become the default primary retailer even when another retailer would otherwise be selected, because Sephora exposes unusually unified product, attribute, variant, review, and demographic information?

The case is Clinique’s Moisture Surge franchise, narrowed to the Moisture Surge 100H core product. Forseti’s current company-selection record discovers Clinique through Ulta and Nordstrom rather than Sephora. Sephora nevertheless carries the product. This directly tests the proposed supersession rule rather than selecting a case where Sephora was already primary.

The rule succeeds only if:

1. Sephora is authorized, target-market relevant, route-admissible, and materially complete for the selected product;
2. making it the default primary improves cross-company comparability without silently losing material product or commercial facts; and
3. the surrounding retailer capture can remain bounded rather than recapturing every retailer in full.

The falsifier was evidence that Sephora’s standardization could not compensate for a missing product, material variant, market state, or decision-material fact and that no bounded secondary capture could preserve the loss.

## 2. Confirm-don’t-trust load receipt

These load-bearing repository sources were re-read from the isolated dogfood worktree at base bbb2bd8d3da006f7c6c54f831cdd9ebab377d213:

| Source | Blob verified in this worktree | Load-bearing use |
|---|---:|---|
| commission_signal_board_prompt_structure_rules_v0.md | 5c81a99a977c71e894d31a884b28afb0835e8e18 | Current portfolio-first sequence and primary/secondary retailer rule |
| forseti_commission_signal_board_prompt_structure_v0.md | 8c3b676632d36392d4a6297ada1772417e15ccd6 | Current CSB prompt structure |
| retailer_information_extraction_standard_v0.md | df63fb8cc846208ba9305e20d71068e1e95e6e32 | Retail information inventory and Sephora reference profile |
| retail_pdp_review_record_capture_recon_v0.md | e22ce684a9fdbea7472dfdf426e685a3228a1b27 | Review-provider and route limitations |
| forseti_beauty_retailer_surface_probe_results_v0.md | ff3f8e922fda6e5809bdfe7683fcf6102aa725dd | Direct-public Bazaarvoice route capabilities |
| retail_capture_profiles.py | 0f74cd61e30804639c4006c5b37b8af9b26855af | Existing retailer capture-profile support |

The current authority already requires portfolio-first capture, reconciliation across franchise/product/variant/SKU/listing, one primary retailer chosen by authorization, target market, assortment breadth, structured depth and route admissibility, and at most one secondary retailer with a named non-duplicative job. This dogfood tests a refinement; it does not presume that refinement is already authoritative.

## 3. Evidence boundary and method

This was a product-learning retrieval pass, not an archival acquisition run. Pages were inspected as currently rendered or indexed on 2026-07-21. Price, count, stock and promotion observations are dated observations, not durable company facts.

The product was checked through five roles:

1. owned Clinique PDP and franchise/routine links;
2. Sephora as the proposed deep primary;
3. Ulta as a second specialty retailer and independent review ecosystem;
4. Target as mass retail, specifically Ulta Beauty at Target; and
5. Amazon as marketplace/official-store coverage.

No page was treated as proof of the company’s complete global SKU set. No review count was converted into unit sales. No shared review provider was treated as proof of identical review corpora.

## 4. Owned source remains canonical

The [owned Clinique PDP](https://www.clinique.com/product/1687/83690/skincare/moisturizers/moisture-surgetm-100h-auto-replenishing-hydrator) exposed the five-size ladder, product claims and test denominators, ingredients, FAQ, and an explicit Moisture Surge routine spanning serum, SPF moisturizer, the 100H hydrator, and body hydrator.

That is not a reason to make the owned PDP the retail primary. It is a reason not to let any retailer supersede the owned source for portfolio and franchise architecture.

**Dogfood implication:** “Sephora primary” means retail-evidence primary, not company or portfolio authority.

## 5. Four-retailer product census

| Surface | Current observed job | Material observations | Review consequence |
|---|---|---|---|
| [Sephora PDP](https://www.sephora.com/product/clinique-moisture-surge-trade-100-hour-auto-replenishing-hydrator-P468351?country_switch=us&lang=en) | Proposed deep retail primary | Five sizes; standardized skin types and concern; highlighted ingredients, callouts and full list; claim/test denominators; review-derived “Highly rated for” chips; Q&A; price/subscription state | Bazaarvoice-backed Sephora surface. Deep capture is justified by normalized attributes, reviewer controls/demographics and sentiment affordances—not by a claim that every field is unique. |
| [Ulta PDP](https://www.ulta.com/p/moisture-surge-100h-auto-replenishing-hydrator-gel-moisturizer-with-hyaluronic-acid-pimprod2021615?sku=2576544) | Specialty secondary and independent review corpus | Same five-size coverage; ingredients and test denominators; sustainability/dermatologist badges; price, promotion, fulfillment and stock state; Q&A | PowerReviews. This is not “reviews only”: retain its separate corpus plus commercial and fulfillment deltas. |
| [Target PDP](https://www.target.com/p/-/A-82550484) | Mass-retail/access and merchandising delta | Ulta Beauty at Target listing; smaller observed size set; standardized “At a glance” attributes; price/stock/fulfillment; Q&A | Bazaarvoice family. Fingerprint overlap against Sephora before admitting another full review corpus; retain Target-native merchandising, access, availability, and Q&A deltas even if reviews overlap. |
| Amazon Premium Beauty | Marketplace authorization, seller/diversion and reach job | Clinique’s official US Amazon Premium Beauty launch is evidenced, and launch coverage included Moisture Surge 100H. A current product PDP/seller state was not reliably observed in this run. | Native Amazon ecosystem in principle, but current product-level capture is ROUTE_BLOCKED_CURRENT_STATE_UNVERIFIED. Do not manufacture a current listing, seller, or review claim. |

Clinique’s official Amazon-store launch is supported by contemporaneous reporting quoting the company and Estée Lauder Companies: [Retail Dive, 2024-03-29](https://www.retaildive.com/news/clinique-launch-amazon-storefront/711769/). That historical authorization signal does not substitute for a current seller/PDP observation.

The Target surface is time-sensitive: Target and Ulta announced that their shop-in-shop partnership would conclude in August 2026. This increases the value of typed dates and retailer-state provenance. See the [official Target announcement](https://corporate.target.com/press/release/2025/08/ulta-beauty-and-target-announce-plans-to-conclude-partnership-in-2026).

## 6. Did Sephora dominate?

No. It won the proposed primary role, but not because it contained every useful fact.

### Where Sephora was strongest

- Unified cross-brand product fields for skin types, concerns, ingredients, and callouts.
- Stable five-size presentation for the core product.
- Review-derived sentiment chips and the richer Sephora review-control/demographic model named in Forseti’s extraction standard.
- A brand/category browsing surface suitable for normalized assortment comparison. The [Clinique moisturizer grid](https://www.sephora.com/brand/clinique/moisturizing-cream-oils-mists) presented a standardized category view rather than only a single PDP.

### Where Sephora did not dominate

- Ulta matched the observed five-size ladder and exposed detailed ingredients and claim/test denominators.
- Ulta added fulfillment, promotion, badge and stock context and a separate PowerReviews corpus.
- Target added mass-retail merchandising and access context that neither specialty retailer represents.
- The owned source more clearly expressed the Moisture Surge franchise/routine architecture.
- Amazon’s marketplace role is structurally different, although current product state could not be verified.

The value of Sephora is **standardization plus distinctive review/metadata controls**, not universal completeness. An unconditional override would encode a false premise and could silently drop products or variants Sephora does not list.

## 7. Review-corpus deduplication rule

The “capture all four per product” instinct is right at the census layer. Four full review corpora are not automatically four independent bodies of customer evidence.

For this case:

- Sephora and Target are in the Bazaarvoice family. Provider identity alone does not prove duplicated rows, and differing review totals do not prove independence.
- Ulta’s PowerReviews corpus is structurally independent enough to justify a second deep review capture.
- Amazon would be a distinct native ecosystem, but only after current PDP/seller state is observed through an admissible route.

The bounded rule that survived is:

1. capture a shallow product/listing census at every supported retailer in scope;
2. fingerprint review overlap using stable IDs where trustworthy and normalized text/date/rating/syndication markers otherwise;
3. admit one principal corpus per substantially overlapping syndication cluster;
4. preserve retailer-native deltas—Q&A, badges, verified-purchase/media/helpfulness fields, fulfillment, availability, and merchandising—even when review text overlaps; and
5. record an explicit route failure or unverified state rather than replacing it with an inferred corpus.

This gives breadth without paying four times for the same syndicated evidence.

## 8. Simulated Understanding capture order

1. **Owned architecture:** establish company portfolio, franchises, products, and variant/SKU relationships; preserve owned routine/collection context.
2. **Sephora shallow assortment/grid:** if authorized and US-pinned, reconcile its listed franchise/product/variant set against owned architecture and expose missing or retailer-exclusive nodes.
3. **Hero/franchise selection:** select the evidence-bounded franchises only after the architecture and grid exist; do not start from one famous product.
4. **Sephora deep PDP:** acquire the standardized product-information and review-control surface for each selected product where materially complete.
5. **Other supported retailers shallow:** for Ulta, Target and Amazon, capture listing presence/absence, identity, size/SKU, price/promotion, availability, aggregate review state, provider fingerprint, and retailer-specific metadata.
6. **Conditional depth:** deepen only for a named non-duplicative job—here, Ulta’s PowerReviews and commercial deltas; Target’s access/merchandising/Q&A deltas; Amazon’s seller/diversion and native review evidence if its route succeeds.
7. **Failure visibility:** emit typed NOT_LISTED, ROUTE_BLOCKED, MARKET_UNPINNED, or MATERIAL_VARIANT_MISSING states. A failed route is a finding, not permission to claim coverage.

## 9. Verdict

**DOGFOOD_SUPPORTS_DEFAULT_NOT_UNCONDITIONAL_OVERRIDE**

The dogfood supports this exact proposed rule:

> Keep the authorized owned source canonical for portfolio and franchise architecture. When Sephora is authorized for the target market, route-admissible, and materially complete for the selected product or franchise, use Sephora as the default retail primary because its standardized product schema, assortment presentation, and review controls improve cross-company comparability. Override at product level when Sephora omits the product or a material variant, cannot be market-pinned or captured, or another authorized retailer is necessary for the bound evidence job. Capture every supported retailer shallowly; deepen only for non-duplicative product, commercial, seller, access, or review-ecosystem evidence.

This is better than both alternatives:

- **Choose the richest retailer case by case:** loses cross-company consistency and repeatedly reopens primary-selection judgment.
- **Always use Sephora when present:** falsely assumes completeness and can hide assortment or market gaps.

The guarded default captures Sephora’s normalization advantage while keeping real failures and product-level exceptions visible.

## 10. Phase-2 positioning, without performing Phase 2

This capture shape improves downstream inputs:

- owned-plus-grid reconciliation gives a defensible franchise/product denominator before hero selection;
- normalized Sephora attributes support cross-product and cross-company comparison;
- retailer-specific price, promotion, availability, fulfillment, and seller states preserve commercial signals Sephora alone cannot supply;
- deduplicated but independent review ecosystems reduce false confidence from syndicated repetition; and
- typed retailer gaps make weak distribution, missing variants, access gaps, and route uncertainty distinguishable.

It does **not** prove demand, sales, commercial importance, whitespace, economics, supply-chain exposure, or vulnerability. Those remain downstream analyses with their own evidence and claim discipline.

## 11. Accepted residuals and non-claims

- This is one adversarial product/franchise case, not cross-brand validation.
- The Sephora/Target review-overlap fingerprint was specified but not executed against archived review rows in this retrieval-only pass.
- Amazon’s current Clinique PDP, seller, and review state remains unverified; the failure is preserved rather than repaired by inference.
- Retail counts, prices, promotions, stock, and partnerships are volatile and require acquisition timestamps in admitted packets.
- The product tests retailer roles; it does not establish that Moisture Surge is Clinique’s sole or top hero franchise.
- No sales-ranking model may treat review volume as units sold without correcting for coverage, syndication, product age, sampling, and review-rate differences.
- Understanding authority remains unchanged.

## 12. Owner adjudication point

The next authorized decision is whether this guarded rule is strong enough to commission the smallest complete Understanding-cycle patch. Until then, current Understanding authority remains unchanged.
