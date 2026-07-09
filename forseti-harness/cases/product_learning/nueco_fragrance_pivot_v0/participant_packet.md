---
case_id: b2_holdout_h7_v0
decision_question: >
  At the start of 2020, should The Nue Co. prioritise deepening its direct-to-consumer
  subscription model — building recurring revenue and a personalized-plan experience on
  its own DTC channel — or redirect capital and attention toward broadening the product
  range and/or expanding into new channels or geographies, or some combination of
  both paths?
decision_date_or_cutoff: "2020-01-01"
role_frame: >
  You are the founder/CEO of The Nue Co., a direct-to-consumer wellness supplement brand
  founded in 2017 and operating primarily through thenueco.com. You hold full authority
  over product strategy, channel strategy, and investment prioritization. You have just
  closed out 2019 and are setting priorities for 2020.
authority_constraints: >
  Full executive authority over DTC product, pricing, subscription mechanics, and site
  experience. Channel partnerships (retail, wholesale) and geographic expansion would
  require external negotiations not fully within unilateral control. Regulatory constraints
  on supplement claims apply in all markets. Lab and manufacturing are based in England
  under an existing supplier relationship.
capability_constraints: >
  The brand operates on Shopify with ReCharge for subscriptions. Product development
  relies on an England-based lab. The team size and internal capability depth are not
  directly observable from the evidence provided. Marketing infrastructure includes
  Google Ads, Facebook Pixel, AdRoll retargeting, Klaviyo email, Seguno, HubSpot, and
  affiliate/partnership programs (PepperJam, Friendbuy referral). Customer consultation
  is supported by a 5-minute online survey tool.
permitted_assumptions:
  - The evidence captures represent the public-facing DTC site as it appeared in 2019;
    internal operational data (unit economics, margin, CAC, LTV) are not available.
  - Product prices shown in the captures are in USD; the brand may also serve other
    markets, but the observed checkout currency is USD.
  - The brand description "born in 2017" places the company at approximately 2-3 years
    of operation at the decision date.
  - The Shopify shop ID (16732809) and theme revision history are consistent across
    captures and can be treated as referring to the same continuous commercial entity.
forbidden_information_notice: >
  Use only the evidence units provided in this packet. Do not draw on any knowledge,
  recall, research, or information about The Nue Co. or the supplement industry from
  any source outside this packet. If you recall anything about this brand or its later
  history, set that aside entirely — only the bytes in the evidence units count.
source_manifest:
  - source_id: E1
    source: Wayback capture of thenueco.com homepage, snapshot 2019-12-21 (served from 2019-12-14 capture)
    retrieval_timestamp: "2026-06-15T14:18:00Z"
    hash: 7a6204b583312a71488aaf397b4706079fbcec70cae5475a430d3093129174ec
  - source_id: E2
    source: Wayback capture of thenueco.com homepage, snapshot 2019-06-26
    retrieval_timestamp: "2026-06-15T14:18:00Z"
    hash: 872af5a24398ec2a4222c51a6034c7f2ce0e42282da2d92bb0554cab1a3d67da
  - source_id: E3
    source: Wayback capture of thenueco.com homepage, snapshot 2019-02-27
    retrieval_timestamp: "2026-06-15T14:18:00Z"
    hash: 03970d2fabd5f38c5f6b7f4319b12a6e3acdce174397d557a31bed475e7803c9
  - source_id: E4
    source: Wayback capture of thenueco.com/collections/all, snapshot 2019-11-17
    retrieval_timestamp: "2026-06-15T14:18:00Z"
    hash: 20c3e364e0fe6a040c2a17f70506fc7018051f83c95d2465125775b588f8240d
  - source_id: E5
    source: Wayback capture of thenueco.com/collections/best-sellers, snapshot 2019-11-17
    retrieval_timestamp: "2026-06-15T14:18:00Z"
    hash: abc8d24811b108f055fba0c9fc2cf9098d524cde87b5d565a0b66bea8de064eb
  - source_id: E6
    source: Wayback capture of thenueco.com/pages/about, snapshot 2019-02-19
    retrieval_timestamp: "2026-06-15T14:18:00Z"
    hash: d2bdc3133e9da336fefe774442289e24a743c698b734d92cf13a18ecd0a7dbec
  - source_id: E7
    source: Wayback capture of thenueco.com product page for DEBLOAT FOOD + PREBIOTIC, snapshot 2019-12-19
    retrieval_timestamp: "2026-06-15T14:18:00Z"
    hash: 3c6dcc777557884808dc4e20999979b1a778875c17ed069629458083c01a4ffd
---

# Participant Packet

**Case:** `b2_holdout_h7_v0` | **Decision date:** 2020-01-01

---

## Decision Context

The Nue Co. is a direct-to-consumer supplement brand, founded in 2017, operating primarily through its own Shopify storefront at thenueco.com. Its stated founding proposition — observed consistently across captures from February 2019 through December 2019 — is that conventional supplements are laden with chemical preservatives and fillers; the brand positions itself around food-based, organically sourced ingredients that are scientifically validated, free from toxins, and more bioavailable than conventional supplements. Formulas are produced by a laboratory based in England with over 20 years of operating history, blended in FDA-approved facilities, and packaged in recyclable glass. The brand stated a commitment to becoming zero-waste by 2020.

By late 2019 the observable product catalog had grown substantially from the brand's initial food-based powder range. The November 2019 collection captures (E4, E5) show at least 15 distinct product SKUs covering categories the brand explicitly tags as: gut health, skin, stress, sleep, energy, and immunity. Formats had expanded to include powders, tinctures (alcohol-free, glycerin-extracted), time-delay capsules, a topical spray, and, as of December 2019, a new encapsulated product (DEBLOAT+) promoted prominently on the homepage as a capsule version of its bestselling powder. The December 2019 homepage (E1) also introduced a fragrance product ("Functional Fragrance"), indicating the brand had extended beyond ingestible supplements into adjacent wellness product types. The best-sellers page (E5) confirms a distinct curated collection separate from the full catalog, with DEBLOAT FOOD + PREBIOTIC, PREBIOTIC + PROBIOTIC, SKIN FOOD + PREBIOTIC, ENERGY FOOD + PREBIOTIC, MAGNESIUM EASE, FUNCTIONAL FRAGRANCE, SLEEP DROPS, and NOOTRO-FOCUS among the items positioned there.

A subscription model ("Plans") was active and promoted throughout the observation window. The ReCharge Payments integration powered monthly subscriptions at a 20% discount to one-time prices, with a two-month minimum commitment and cancellation by email request. Cart UX prominently separated "Your Plan" items from "One-Time Purchases," and the homepage carried a consultation-survey tool ("Tell us your concerns + we'll tell you what to take") allowing customers to receive personalized product recommendations across six concern categories: Energy, Gut Health, Immunity, Skin, Sleep, Focus, and Stress. A referral program (Friendbuy, offering $15 referral credit) was present in the December 2019 homepage. Marketing integrations visible in the page source across captures include Google Ads, Facebook Pixel, AdRoll retargeting, Klaviyo email, Mailchimp, HubSpot, Seguno, and an affiliate program via PepperJam. A footer link labeled "NYC Flagship" appears in the early 2019 about-page capture (E6), suggesting a physical retail presence in New York at that time. The product detail page for DEBLOAT FOOD + PREBIOTIC (E7, December 2019) shows an in-stock inventory of 2,579 units, a one-time price of $55, and a subscription price of $44, with 83 product reviews averaging 4.53 stars at snapshot time.

Entering 2020, the brand faced a recognizable strategic choice that growing DTC wellness brands commonly encounter: whether to lean further into the direct subscription relationship — deepening personalization, improving plan retention, and building recurring revenue density on its owned channel — or to broaden reach through product range expansion, channel diversification, and potentially geographic scale, or some combination of both. The evidence does not establish which path the leadership chose or what the outcomes were; the evidence only establishes the observable state of the business at the decision point.

---

## Evidence Units

- **E1** — Homepage snapshot, 2019-12-21 (Wayback redirect to 2019-12-14 capture): Shows a redesigned homepage (theme "Dev - Homepage Redesign - Nov 2019") featuring a hero promoting "Functional Fragrance," a spotlight module for the new DEBLOAT+ capsule product with clinical trial language (51% reduction in bloating in 30 days), a "Tell us your concerns" consultation section with six concern categories, product-type differentiator sections (powders / tinctures / time-delay capsules), a journal/blog article carousel, and a rotating press-quote slider. Referral program (Friendbuy, $15) present in navigation.

- **E2** — Homepage snapshot, 2019-06-26: Shows the mid-2019 site state (theme "The Nue Co 2018 - Barrel Updates") with navigation limited to "Build a Plan" (survey) and "Shop." Marketing integrations at this point include ReCharge, Judge.me reviews, AdRoll, free-gift program (SECOMAPP), HubSpot, Mailchimp, and Seguno. No referral program visible. The cart experience already prominently separates subscription ("Plan") and one-time items.

- **E3** — Homepage snapshot, 2019-02-27: Shows the early 2019 site under the same "The Nue Co 2018 - Barrel Updates" theme. Navigation includes "Build a Plan," "Shop," and "About" in header. Free-gift program (SECOMAPP), ReCharge subscriptions, and Judge.me reviews active. Subscription plan cart UI present with messaging: "Plan ahead, make it monthly — Our tailored programs ensure you get the products you need, when you need them."

- **E4** — Full catalog page (collections/all), snapshot 2019-11-17: Shows 15+ products organized under filter tags: Energy, Gut Health, Immunity, Skin, Sleep, Stress. Products include DEBLOAT+ ($60), REGULARITY RELIEF ($40), DIGEST START ($30), SKIN FILTER ($60), DEBLOAT FOOD + PREBIOTIC ($55), PREBIOTIC + PROBIOTIC ($75), PROBIOTIC PROTEIN – PLANT (from $35), PROBIOTIC PROTEIN (from $35), SKIN FOOD + PREBIOTIC ($55), ENERGY FOOD + PREBIOTIC ($55), SLEEP DROPS (from $35), MAGNESIUM EASE (from $35), DEFENSE DROPS ($55), POWER UP ($40), Topical-C ($70), FUNCTIONAL FRAGRANCE (from $30), NOOTRO-FOCUS ($85).

- **E5** — Best-sellers collection page, snapshot 2019-11-17: Shows the curated best-sellers list with the same filter taxonomy (Energy, Gut Health, Immunity, Skin, Sleep, Stress). Leading positions: DEBLOAT FOOD + PREBIOTIC, PREBIOTIC + PROBIOTIC, SKIN FOOD + PREBIOTIC, ENERGY FOOD + PREBIOTIC, MAGNESIUM EASE, FUNCTIONAL FRAGRANCE, SLEEP DROPS, NOOTRO-FOCUS, PROBIOTIC PROTEIN – PLANT, POWER UP. Gut-health and prebiotic products occupy the first positions.

- **E6** — About page, snapshot 2019-02-19: Contains brand origin story (founded 2017, grandfather-scientist narrative), philosophy ("science and natural innovation," Ayurvedic and Chinese medicine), four-stage manufacturing process (proven formula → remove chemicals → swap for organic foods → natural supplement backed by science), ingredient sourcing examples (Camu Camu for Vitamin C; Baobab for Beta-Carotene; Beetroot for Iron), and commitment language on sustainability and zero-waste-by-2020. Footer links include "NYC Flagship." Subscription plan cart includes benefit messaging: "Delivered / Results / Support."

- **E7** — Product detail page for DEBLOAT FOOD + PREBIOTIC, snapshot 2019-12-19: Price $55 one-time / $44 on subscription (20% discount, 1-month frequency, 2-month minimum). 83 reviews at 4.53 stars. In-stock inventory 2,579 units (SKU PR-DEB-100, barcode 5060506360003, EAN prefix suggesting UK origin). Ingredients: maqui fruit powder, cinnamon powder, ginger root powder, turmeric root powder, inulin. Serving size 1 tsp / 5g; 20 servings per container. Full "Why It Works" section citing clinical studies. Product created 2017-07-14; published to store 2019-10-03. Friendbuy referral script present; product tagged "gut health."

---

## Known Uncertainties

The following cannot be determined from the evidence provided:

- **Financial data**: No revenue, gross margin, customer acquisition cost, lifetime value, or burn rate is observable. Unit pricing and product counts are visible but conversion rates and order volume are not.
- **Subscription metrics**: ReCharge integration and plan pricing are visible, but subscriber count, churn rate, average plan revenue, or subscription attachment rate cannot be inferred from static HTML captures.
- **Channel mix**: The NYC Flagship link suggests some physical retail presence, and the PepperJam affiliate integration suggests an affiliate channel, but the scale, revenue contribution, or strategic priority of non-DTC channels is unknown.
- **Geographic split**: The site operates in USD and the lab is in England; the degree to which UK, European, or other international revenue exists is not determinable from the evidence.
- **Team and organizational capacity**: Headcount, capability depth, and capital position are not observable.
- **Competitive landscape**: No competitor data is present in the evidence; the supplement market context at the decision date is not established by these captures.
- **Evidence scope**: All seven evidence units are captures of The Nue Co.'s own DTC website. They represent how the brand chose to present itself publicly, not independent or financial reporting. Inventory numbers, review counts, and prices are point-in-time observations and may not reflect steady-state conditions.
- **E1 redirect caveat**: The requested Wayback snapshot date of 2019-12-21 was internally redirected by Wayback to a 2019-12-14 capture of the same URL. The capture remains pre-cutoff, but the content reflects December 14, 2019, not December 21, 2019.
