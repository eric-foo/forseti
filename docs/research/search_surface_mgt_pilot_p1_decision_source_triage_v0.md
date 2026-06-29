# Search-Surface MGT P1 Decision-Source Triage v0

```yaml
retrieval_header_version: 1
artifact_role: Research synthesis artifact
scope: Prioritizes P1 direct-source reads from the Search-Surface MGT P0 fragrance SERP set by whether a search result can affect a Scanning or Capture decision.
use_when:
  - Choosing which P0-derived search results deserve P1 direct-source capture.
  - Keeping Search-Surface MGT focused on decision leverage instead of broad keyword research.
  - Explaining why AI Overview presence is not currently a primary prioritization input.
open_next:
  - docs/research/search_surface_mgt_pilot_p0_receipts_v0/search_surface_mgt_pilot_p0_capture_receipt_v0.md
  - docs/research/search_surface_mgt_pilot_p0_receipts_v0/search_surface_mgt_pilot_p0_capture_efficacy_review_v0.md
  - docs/research/search_surface_mgt_pilot_p0_live_trends_probe_v0.md
  - docs/research/search_surface_mgt_pilot_p0_receipts_v0/capture_manifest.json
stale_if:
  - P1 direct-source capture is completed and supersedes this triage.
  - The P0 SERP result set is recaptured or materially changes.
  - Orca changes the Search-Surface MGT boundary, Capture request contract, or Scanning frontier rules.
authority_boundary: retrieval_only
```

## Boundary

This is decision-source triage, not judgment. It does not prove durable demand, buyer proof, willingness to pay, product readiness, market size, or Google AI Overview causality.

Prioritization rule from owner direction: prefer results that can affect a decision, even if they only provide light support. Ignore or defer results that merely decorate the search landscape.

AI Overview presence is carried as an annotation only. For this P1 triage, source decision effect beats AI-box state.

## Triage Read

| Priority | Cluster | P0 source result | Why it can affect a decision | Next action |
| --- | --- | --- | --- | --- |
| A | Discovery / sampling | Reddit thread: `How do you test a fragrance before buying?` | Direct buyer-language about decants, skin testing, repeated wears, 2ml/5ml/10ml sizes, avoiding expensive blind buys, and when samples convert to full-size or travel-size purchase. This can shape Capture questions and Scanning frontiers around trial-to-bottle behavior. | Capture now. Preserve thread and extract buyer decision grammar. |
| A | Discovery / sampling | Ministry of Scent `Perfume Sample Sets` | Live retailer shelf exposes sample-set category structure, shipping distinction for sample-only orders, brand/note filters, 97 products, product prices, reviews, and sold-out states. This can shape concrete Capture asks around sample-set retail mechanics. | Capture now. Preserve category page and a small product spread. |
| A | Discovery / sampling | Twisted Lily `Discovery Sets` | Live retailer shelf exposes niche/indie discovery sets, 59 products, sample/travel navigation, prices, review counts, and curated house sets. This can shape direct Capture asks around discovery-set selection and retail depth. | Capture now. Preserve category page and a small product spread. |
| A | Dupe / comparison | Reddit thread: `What is the best alternative to Santal 33 by Le Labo?` | Direct substitution language, price-pressure motive, use-case split between original and cheaper everyday dupe, and repeated alternatives such as Maison Louis Marie Bois de Balincourt, Cremo Palo Santal, Fine'ry Jungle Santal, Dossier, and Dime. This can shape a comparison-frontier and product-substitute Capture request. | Capture now. Preserve thread and extract repeated substitutes, price anchors, and "closest / not close enough" language. |
| A | Dupe / comparison | Reddit thread: `I'm looking for close dupes of Baccarat Rouge 540` | Direct buyer-origin comparison behavior with repeated alternatives such as Lattafa Ana Abiyedh Rouge, Maison Alhambra Baroque Rouge 540, Ariana Grande Cloud, Al Haramain Amber Oud Ruby, Club de Nuit Untold, Zara Red Temptation, and Montagne Le Bon Bon. This can shape competitor/substitution capture. | Capture now. Preserve thread and extract repeated alternatives plus performance/price language. |
| B | Discovery / sampling | Sephora Favorites sampler/voucher search result | Search result snippets and prior P0 SERP text point to voucher mechanics: sampler purchase that can convert into a full-size or travel-size fragrance. This can affect the trial-to-purchase offer map, but direct page access was not observed in the browser pass. | Capture if accessible. Prefer official Sephora page or a reliable archived/product page; otherwise preserve an editorial explainer only as support. |
| B | Trend-note control | Reddit thread: `Best pistachio scent?` | Direct scent-note frontier: users compare pistachio products by maturity, gourmand sweetness, nuttiness, powderiness, performance, seasonality, and decant/blind-buy behavior. This can support a Scanning frontier if Orca chooses note-trend work. | Capture if P1 includes note-trend control. Not needed before discovery/sample and dupe clusters. |
| B | Trend-note control | Reddit thread: `How do y'all feel about Phlur Vanilla Skin?` | Direct product-specific language around projection, longevity, layering, synthetic/play-doh objection, body chemistry, and vanilla alternatives. This can support a Scanning frontier if Orca chooses note/product trend work. | Capture if P1 includes note-trend control. Not needed before discovery/sample and dupe clusters. |
| C | Editorial listicles | Cosmopolitan / Byrdie / Allure / Esquire-style result pages | Can expose product lists, fresh dates, voucher explanations, and SEO-visible alternatives, but usually weaker than buyer-origin/community or retailer surfaces. | Defer unless needed to triangulate named substitutes or voucher mechanics. |
| C | AI answer-surface state | AI Overview shown / not shown | Useful surface annotation, but the live Trends probe showed AI-box presence does not materially decide which P1 sources are worth reading. | Preserve as metadata only. Do not prioritize P1 by AI-box state. |

## Decision Implication

Proceed with P1 direct-source capture in this order:

1. Discovery/sample buyer thread.
2. Discovery/sample retailer shelves.
3. Santal 33 dupe buyer thread.
4. Baccarat Rouge 540 dupe buyer thread.
5. Sephora sampler/voucher only if directly accessible or needed to complete offer mechanics.
6. Pistachio / Vanilla Skin note-trend threads only if Scanning wants a trend-note control cluster.

This sequence honors the new prioritization rule: capture the result if it can change or lightly support a decision. For P1, a source can affect a decision if it can produce any of:

- a concrete Capture request with URL, surface, acquisition route, and verification question;
- a Scanning frontier with buyer language, competitor/substitute set, or offer mechanics;
- a negative that cheaply closes a tempting but weak path.

## Capture Requests Implied

### Capture Request 1 - Trial / Discovery Behavior

Preserve:

- `https://www.reddit.com/r/FragranceStories/comments/1mydzqk/how_do_you_test_a_fragrance_before_buying/`
- `https://ministryofscent.com/collections/sample-sets-1`
- `https://twistedlily.com/collections/samples-discovery-sets`

Verification questions:

- What phrases do buyers use for trial before full-bottle commitment?
- Which sample sizes appear in buyer-language: 1ml, 2ml, 3ml, 5ml, 10ml, travel size, full bottle?
- Which retailer mechanics matter: discovery set, sample-only shipping, voucher, travel spray, reviews, sold-out states, price ladder?
- Does the source expose enough buyer-origin or retail-depth language to become a Scanning frontier?

### Capture Request 2 - Dupe / Substitution Behavior

Preserve:

- `https://www.reddit.com/r/fragrance/comments/15fp22s/what_is_the_best_alternative_to_santal_33_by_le/`
- `https://www.reddit.com/r/Colognes/comments/1nwmudi/im_looking_for_close_dupes_of_baccarat_rouge_540/`

Verification questions:

- Which substitutes repeat across independent comments?
- What language distinguishes "close enough" from "not satisfying after the original"?
- What price anchors and use-cases appear: everyday wear, grocery/walk use, cheaper clone, sample first, performance/longevity?
- Which product pages should Capture inspect next because they recur in buyer-origin comparison language?

### Optional Capture Request 3 - Note-Trend Control

Preserve only if needed:

- `https://www.reddit.com/r/Perfumes/comments/1ds4mtk/best_pistachio_scent/`
- `https://www.reddit.com/r/Perfumes/comments/1igxp3x/how_do_yall_feel_about_phlur_vanilla_skin_i/`

Verification questions:

- Does the note trend produce buyer-origin language beyond generic enthusiasm?
- Are repeated products and objections stable enough to form a Scanning frontier?
- Does product-specific language reveal actionable preference axes: sweetness, maturity, projection, layering, body chemistry, seasonality?

## Observed Support

- P0 Trends showed Q03/Q04 note terms were high-interest despite no AI Overview; that prevents interpreting no-AI-box as weak attention.
- The fragrance-testing Reddit thread shows multiple buyer paths around decants, samples, skin testing, multi-wear testing, and travel-size / full-bottle upgrade decisions.
- Twisted Lily and Ministry of Scent show live retail shelves for discovery/sample sets with prices, product counts, review counts, filters, sold-out states, and sample-set language.
- Santal 33 and Baccarat Rouge 540 dupe Reddit threads expose direct substitution maps, price sensitivity, closest-match language, and competing alternatives.
- Pistachio and Vanilla Skin threads expose note/product preference axes, but they are lower-priority until Scanning decides note-trend work matters.

## Non-Claims

- Not judgment evidence.
- Not durable-demand proof.
- Not buyer-proof clearance.
- Not source exhaustiveness.
- Not a recommendation to build a Search branch.
- Not a claim that AI Overview presence or absence determines source priority.
- Not a claim that editorial/listicle results are useless; they are simply lower-priority than buyer-origin or direct-retailer sources for this P1 purpose.
