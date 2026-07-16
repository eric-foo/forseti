# Reddit Beauty / Fragrance Subreddit Inventory v0

```yaml
retrieval_header_version: 1
artifact_role: Advisory venue-routing inventory (Reddit source family; GTM/radar planning input)
scope: >
  Owner-commissioned inventory of the Reddit subreddits where consumer-demand
  beauty audiences and (at depth) fragrance audiences concentrate, so radar
  scans and GTM work know where the client's clients are. Seeds CSB
  forums_community rows, aphrodite GTM target-discovery/SEO-topic commissions,
  and future beauty-lane scans. Advisory routing input only.
use_when:
  - Commissioning or scoping a CSB board whose forums_community rows need concrete Reddit venues for a beauty or fragrance decision.
  - Selecting Reddit venues for aphrodite GTM Play A (target discovery) or Play B (SEO topic mining) research.
  - Routing a bounded Reddit scan, candidate-intake seed, or exact-query walk toward the highest-yield beauty/fragrance venues.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/scanning/README.md
  - forseti/product/spines/scanning/source_families/reddit/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/reddit/README.md
  - forseti/product/spines/creator_signal/aphrodite_research_engine_gtm_design_v0.md
stale_if:
  - A verification pass finds a listed subreddit banned, private, renamed, or materially changed in size band or posture.
  - The aphrodite lead lane or the beauty-lane scope changes which audience segments matter.
  - A CSB-first scan's venue evaluation contradicts a load-bearing radar/GTM rating here.
  - Reddit source-access or commercial-policy posture changes what any consumer of this inventory may do with these venues.
```

## Status and non-claims

`ADVISORY_PLANNING_INPUT`. This is a market map, not a scan result, capture
authorization, or coverage claim.

- **Not a standing source map for the scanning spine.** CSB-first scans still
  run their own venue evaluation and mandatory broad-scout miss-check; this
  inventory seeds boards and saves rediscovery passes, it never substitutes for
  them and never clears a gate.
- **Not capture, monitoring, or engagement authorization.** Any live Reddit
  fetch routes through the Reddit candidate-intake/capture lanes and their
  robots/ToS posture; commercial Reddit use still requires a sanctioned API or
  licensing path; posting or outreach in any listed venue is a separately gated
  GTM act (most listed venues ban self-promotion — noted per entry because it
  bounds GTM to listening, not because posting is planned).
- **Sizes are approximate bands.** Provenance per entry is `web_verified`
  (verification pass 2026-07-16: member counts visible in web-search snippets,
  mostly cached third-party stat sites whose data vintage is roughly 2025 —
  directionally correct, several months stale), `exists_unverified_count`
  (existence confirmed, no reliable count surfaced), or `model_knowledge`
  (assistant training knowledge, early-2026 horizon, unverified). Bands are
  for prioritization only; they are not demand proof, audience-quality proof,
  or reach estimates.
- **Not coverage-complete.** Reddit venue discovery is open-ended; the
  discovery ledger at the end records what was deliberately left out.

## What this inventory is for

Forseti's buyers are beauty/fragrance brands; **their customers — the demand
pool Forseti reads — concentrate in a knowable set of subreddits.** Two
consumers use this map:

1. **Radar (demand read).** These venues carry the `forums_community` signal
   the product reads: recommendation asks, dupe requests, purchase reports,
   hype waves and their counter-waves. Knowing which venue carries which signal
   type routes bounded scans instead of rediscovering venues per commission.
2. **GTM (aphrodite first).** Play A target discovery (which clone/dupe/indie
   houses the dupe-seeking audience is talking about right now) and Play B SEO
   topic mining (repeat and unanswered questions = content demand) both need
   the concrete venue list. The fragrance tiers are deep
   (exhaustive-within-niche is the moat); the beauty tiers are hub-level for
   the broader consumer-demand lane.

Per-entry signal vocabulary: `rec_ask` (recommendation requests),
`dupe_ask` (dupe/clone requests — the aphrodite lead-lane audience),
`review` (owned-purchase reports), `haul` (purchase display),
`deal` (price-driven purchase intent), `swap` (secondary-market liquidity),
`creator_talk` (creator commentary/drama — creator_signal radar),
`anti_haul` (counterevidence: fatigue, regret, de-influencing).

## Tier 1 — Fragrance core (aphrodite depth)

| Subreddit | Size band | Audience shape | Dominant signals | Radar / GTM note | Posture | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| r/fragrance | ~2.4M | General hub; all genders per its own tagline; enthusiast-to-beginner mix | rec_ask, review, dupe_ask | Highest-volume general fragrance demand pool; SEO topic goldmine (repeat questions) | Strict no-self-promo (rules text not snippet-retrievable; verify on first commission) | web_verified |
| r/Perfumes | count unverified | Feminine-leaning, recommendation-dense, beginner-friendly | rec_ask, review, haul | Fast-moving rec-ask venue; strong for note-family demand reads. CAUTION: web search conflates it with the unrelated K-pop r/Perfume (singular, ~10K) — verify count directly before load-bearing use | No self-promo (model_knowledge) | exists_unverified_count |
| r/Colognes | ~210K | Masculine-leaning, collection-showcase culture, value-conscious | rec_ask, review, dupe_ask | Male demand pool; heavy clone-house awareness (Lattafa et al.) | Sidebar rules verified: no swap/sell (routes to r/FragranceSwap); fake-checks route to r/colognecheck | web_verified |
| r/FemFragLab | count unverified | Women's fragrance lab culture; layering, skin-scent discourse | rec_ask, review, haul | High-signal for feminine niche/indie demand and layering trends; existence confirmed via cross-sub aggregation citations | Community-strict moderation (model_knowledge) | exists_unverified_count |

## Tier 2 — Fragrance dupe / clone / value (aphrodite lead-lane audience)

The aphrodite first cohort is dupe/clone/affordable creator-commerce houses;
**these venues are literally their customers.**

| Subreddit | Size band | Audience shape | Dominant signals | Radar / GTM note | Posture | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| r/fragranceclones | ~270K | Dupe-seekers; clone-house comparison culture (verified sample discourse: "Lattafa The Kingdom as a clone of Le Male Elixir") | dupe_ask, review | The single most GTM-relevant fragrance venue: live which-clone-wins discourse maps directly to Play A target discovery | No self-promo (model_knowledge) | web_verified |
| r/DesiFragranceAddicts | ~256K | South Asian/desi fragrance community: perfumes, attars, incense, gourmands | rec_ask, review, dupe_ask | Major discovery-pass find: clone-house/attar demand pool at scale; strong Lattafa-class-relevant audience | — | web_verified |
| r/DIYfragrance | ~39K | Hobbyist perfumers; materials-literate | — | Low direct GTM value; occasional early note-trend signal | — | web_verified |
| r/PerfumeOils | ~9K | Oil-based/attar-style (alcohol-free) perfume niche | rec_ask, review | Small; overlaps indie and Middle-Eastern-style interest | — | web_verified |

An **Arab-specific fragrance sub was not confirmed to exist** (searched under
several plausible names). r/DesiFragranceAddicts is the closest verified
regional community; a direct single-page Reddit check for Arab/khaleeji/oud
subs is an open verification item, not a confirmed absence.

## Tier 3 — Fragrance exchange / purchase intent

| Subreddit | Size band | Audience shape | Dominant signals | Radar / GTM note | Posture | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| r/FragranceSwap | ~121K | Secondary-market traders; wts/wtb/wtt + decant culture | swap | Liquidity signal: what trades fast = revealed demand | Trade-rule heavy | web_verified |
| r/Indiemakeupandmore | ~147K | Indie perfume-oil + indie beauty buyers; consumers, creators, AND shop owners | review, haul, rec_ask | Indie-house demand pool; overlaps fragrance and beauty lanes. Posture is the outlier: shop owners are welcome, so indie-brand self-promo is tolerated — the one listed venue where brand presence is native | Disclosure rules; self-promo tolerated for indie shops | web_verified |

## Tier 4 — Beauty core hubs (consumer-demand lane, hub level)

| Subreddit | Size band | Audience shape | Dominant signals | Radar / GTM note | Posture | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| r/SkincareAddiction | multi-M (sources conflict, 1.4M–5M) | Largest skincare hub; routine-driven, ingredient-literate | rec_ask, review | Category-scale demand pool; very high volume (historically 1000+ posts/day) | Verified strict: structured-post/routine-template rules, flair-gating, heavy self-promo restriction | web_verified (band only) |
| r/MakeupAddiction | ~3–4M | Largest makeup hub; looks + product talk | review, haul, rec_ask | Category-scale; haul culture = purchase display | Some self-promo limits | web_verified (band only) |
| r/SkincareAddicts | ~1M (unverified precision) | Less-strict spinoff/alternative to the flagship | rec_ask, review | Same demand pool, looser posting rules — often easier signal to read | Looser than flagship | exists_unverified_count |
| r/AsianBeauty | count unverified (a 3.7M claim looks inflated) | K/J-beauty; ingredient-forward, import-savvy | rec_ask, review, haul | Trend-leading venue: K-beauty waves surface here before mass market | Strict sourcing rules (model_knowledge) | exists_unverified_count |
| r/30PlusSkinCare | count unverified | Mature-skin demographic; higher spend capacity (community notable enough for 2020 Washington Post feature) | rec_ask, review | Demographic wedge with strong purchase intent | Moderate (model_knowledge) | exists_unverified_count |
| r/beauty | count unverified | General beauty catch-all; beginner-heavy | rec_ask | Lower signal density than the dedicated hubs | — | model_knowledge (low confidence) |
| r/HaircareScience | ~1M | Ingredient-literate haircare; active since 2013 | rec_ask, review | Haircare demand pool, evidence-oriented buyer language | Strict | web_verified |
| r/curlyhair | count unverified | Curly-method community; product-routine-driven | rec_ask, review, haul | Product-dense; routine culture drives repeat purchase talk. Press-noted mixed inclusivity record for Black natural hair — see the Black-haircare gap in the discovery ledger | Moderate (model_knowledge) | exists_unverified_count |
| r/lacqueristas | ~68K | Indie nail-polish/lacquer community (seed name r/RedditLaqueristas appears stale; live community goes by this name) | review, haul | Nail-category hub; review-heavy, indie-brand purchase intent | — | web_verified |

## Tier 5 — Beauty demographic / regional hubs

| Subreddit | Size band | Audience shape | Dominant signals | Radar / GTM note | Posture | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| r/IndianSkincareAddicts | ~311K | Indian market; science-forward, mixes international + local brands | rec_ask, review, deal | Regional demand pool; dupe/afford discourse strong | Moderate | web_verified |
| r/EuroSkincare | ~98K | EU availability/regulatory-aware buyers | rec_ask, review | Regional routing for EU demand questions | Moderate | web_verified |
| r/AusSkincare | count unverified | Australian market | rec_ask, review | Regional routing | — | model_knowledge (low confidence) |
| r/KoreanBeauty | count unverified (smaller than r/AsianBeauty) | K-beauty-only; industry-cited as higher purchase intent and brand loyalty than the broader hub | rec_ask, review, haul | Higher-intent niche alternative to r/AsianBeauty | — | exists_unverified_count |
| r/malegrooming | count unverified | Men's grooming/skincare demographic hub | rec_ask, review | Men's-demographic routing; overlaps the fragrance male demand pool | — | exists_unverified_count |
| r/tretinoin | ~275K | Single-ingredient community; high routine adherence | review, rec_ask | Ingredient-level demand depth; adjacent-product asks common | Moderate | web_verified |

## Tier 6 — Retailer / deal / purchase-intent venues

| Subreddit | Size band | Audience shape | Dominant signals | Radar / GTM note | Posture | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| r/Sephora | ~1M | Retailer-anchored; sale-cycle-driven | deal, haul, rec_ask | Purchase-intent-dense; sale threads = live conversion talk | Retailer-specific rules | web_verified |
| r/Ulta | count unverified | Retailer-anchored | deal, haul | Same pattern as r/Sephora, different assortment | — | model_knowledge (low confidence) |
| r/MUAontheCheap | ~1.1M | Deal-hunters across beauty; running since 2017 | deal | Price-elasticity radar; what moves on discount | Actively moderated, deal-format rules | web_verified |
| r/MakeupDupes | count unverified | Dupe-finders (beauty analog of r/fragranceclones) | dupe_ask, review | Comparison-shopping intent; directly relevant if the beauty lane follows the aphrodite dupe-audience wedge | — | exists_unverified_count |
| r/BeautyBoxes | count unverified | Subscription-box buyers | review, haul | Sampling-economy signal; discovery-driven buyers | — | model_knowledge (low confidence) |

## Tier 7 — Creator-watch (creator_signal radar)

| Subreddit | Size band | Audience shape | Dominant signals | Radar / GTM note | Posture | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| r/BeautyGuruChatter | count unverified (a 3.1M claim looks inflated; likely mid-hundreds-K) | Creator-commentary community | creator_talk | Direct creator_signal radar: rising/falling creator credibility, sponsorship fatigue, scandal risk — inputs the product's creator vetting reads care about | Strict; no brigading (model_knowledge) | exists_unverified_count |

## Tier 8 — Counterevidence / anti-consumption venues

CSB boards carry mandatory counterevidence paths; these venues are where the
counter-wave shows first.

| Subreddit | Size band | Audience shape | Dominant signals | Radar / GTM note | Posture | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| r/MakeupRehab | count unverified | Anti-overconsumption; no-buy/low-buy support culture; regret and de-influencing talk | anti_haul | Counterevidence venue: hype fatigue, manufactured-demand skepticism. Purchase intent is suppressed by design — that inversion is the signal | Supportive-community rules | exists_unverified_count |
| r/PanPorn | count unverified (a 1M+ claim is unverified precision) | Project-pan (use-it-up) culture | anti_haul, review | Usage-depth signal: what actually gets used vs shelfware | Moderate | exists_unverified_count |

## Relation to the Reddit capture/scanning lanes

This inventory and the existing Reddit lanes feed each other without either
absorbing the other:

- **Graph Frontier Register → inventory.** The capture-spine Reddit Graph
  Frontier lane already persists `subreddit_candidate` nodes (with visible
  subscriber counts when a bounded run saw them) in its Graph Frontier
  Register. Register discoveries are the natural mechanical confirm/extend
  feed for this inventory: when a bounded run surfaces a beauty/fragrance
  subreddit this map missed or contradicts a band here, update the affected
  tier. The register stays the provenance-receipted record; this inventory
  stays the human planning view.
- **Inventory → bounded runs.** Entries here may seed Candidate URL Intake
  run envelopes or frontier selection reasons. Seeding never bypasses the
  lanes' own gates: every run still needs its bounded envelope, caps,
  robots/source-policy posture receipt, and stop condition, and this inventory
  authorizes none of that.

## Discovery ledger

Verification method (2026-07-16): two web-search-only passes (no automated
Reddit fetching). Most verified counts trace to cached third-party stat sites
with roughly-2025 data vintage; treat every count as directional. Several
tool-synthesized numbers with no linked source were discarded rather than
recorded.

Open verification items (each needs one direct single-page Reddit check
before load-bearing use; none blocks advisory routing):

- r/Perfumes exact count (web search conflates it with the unrelated K-pop
  r/Perfume); r/FemFragLab count; r/BeautyGuruChatter, r/AsianBeauty,
  r/PanPorn, r/MakeupRehab counts (inflated or vague claims flagged above);
  r/beauty, r/Ulta, r/BeautyBoxes, r/AusSkincare, r/curlyhair counts.
- Whether an Arab/khaleeji/oud-specific fragrance sub exists (not found under
  several plausible names; r/DesiFragranceAddicts is the closest verified
  regional community).
- A dominant Black-haircare hub (search coverage gap, not a confirmed
  absence; r/curlyhair's press-noted inclusivity record makes this a real
  demographic hole in the map).
- r/basenotes likely does not exist as an active sub (the Basenotes brand is
  a standalone forum, itself a non-Reddit venue worth its own row in any
  future cross-forum inventory).

Deliberately excluded or out of scope for v0:

- r/RepFinds (replica/grey-market fashion; not a legitimate-retail beauty
  venue, noted only because clone-fragrance culture overlaps "rep" culture).
- r/colognecheck and r/Scent_Swap (narrow-purpose satellites; too small or
  too specialized to route scans toward).
- Wellness/supplement subs, fashion subs, general shopping/haul subs,
  body-care-specific subs (none dominant found), non-English-language subs,
  and non-Reddit forums (Basenotes, Fragrantica, MakeupAlley). Each is a
  deferred adjacency; add on a concrete radar or GTM need, not speculatively.
- No distinct 2024–2026 TikTok-trend breakout subreddit surfaced in
  discovery; trend waves appear to flow through the existing hubs.

## Refresh contract

This inventory is refresh-on-trigger, not a standing monitor: refresh a tier
when a commission touching it finds a material mismatch (dead venue, size-band
shift, posture change), or when the lead lane's audience definition changes.
Do not build tooling, dashboards, or scheduled checks around it.
