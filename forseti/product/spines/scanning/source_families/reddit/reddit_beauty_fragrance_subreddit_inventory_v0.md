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
  - forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_subreddit_registry_spec_v0.md
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
- **Sizes are approximate bands; the registry is the authoritative count
  source.** All counts below carry provenance `live_read` (2026-07-16 direct
  same-context page reads; exact values and dated observation series live in
  `reddit_subreddit_registry_v0.json`). Bands are for prioritization only;
  they are not demand proof, audience-quality proof, or reach estimates, and
  future refreshes update the registry first — treat any drift between this
  table and the registry as the registry being right.
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
| r/fragrance | ~2.42M | General hub; "inclusive, adult community" per its own bio; enthusiast-to-beginner mix | rec_ask, review, dupe_ask | Highest-volume general fragrance demand pool; SEO topic goldmine (repeat questions); bio confirms promo/affiliate-free posture | Bio-confirmed: promotion/transaction/influencer-free; rec asks restricted to daily thread | live_read |
| r/Perfumes | ~305K | Feminine-leaning, recommendation-dense, beginner-friendly | rec_ask, review, haul | Fast-moving rec-ask venue; strong for note-family demand reads | No self-promo (model_knowledge) | live_read |
| r/Colognes | ~291K | Masculine-leaning, collection-showcase culture, value-conscious | rec_ask, review, dupe_ask | Male demand pool; heavy clone-house awareness (Lattafa et al.) | Sidebar rules verified: no swap/sell (routes to r/FragranceSwap); fake-checks route to r/colognecheck | live_read |
| r/FemFragLab | ~189K | Women's fragrance lab culture; layering, skin-scent discourse | rec_ask, review, haul | High-signal for feminine niche/indie demand and layering trends | Community-strict moderation (model_knowledge) | live_read |

## Tier 2 — Fragrance dupe / clone / value (aphrodite lead-lane audience)

The aphrodite first cohort is dupe/clone/affordable creator-commerce houses;
**these venues are literally their customers.**

| Subreddit | Size band | Audience shape | Dominant signals | Radar / GTM note | Posture | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| r/fragranceclones | ~295K | Dupe-seekers; clone-house comparison culture (verified sample discourse: "Lattafa The Kingdom as a clone of Le Male Elixir") | dupe_ask, review | The single most GTM-relevant fragrance venue: live which-clone-wins discourse maps directly to Play A target discovery | No self-promo (model_knowledge) | live_read |
| r/DesiFragranceAddicts | ~298K | South Asian/desi fragrance community: perfumes, attars, incense, gourmands | rec_ask, review, dupe_ask | Clone-house/attar demand pool at scale; strong Lattafa-class-relevant audience | — | live_read |
| r/DIYfragrance | ~46K | Hobbyist perfumers; materials-literate | — | Low direct GTM value; occasional early note-trend signal | — | live_read |
| r/PerfumeOils | ~13K | Oil-based/attar-style (alcohol-free) perfume niche | rec_ask, review | Small; overlaps indie and Middle-Eastern-style interest | — | live_read |

Arab-specific check resolved (live read 2026-07-16): **r/arabfragrances
exists but is dead** (1 member, created 2024) — not a venue.
r/DesiFragranceAddicts is the regional community at scale.

## Tier 3 — Fragrance exchange / purchase intent

| Subreddit | Size band | Audience shape | Dominant signals | Radar / GTM note | Posture | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| r/FragranceSwap | ~125K | Secondary-market traders; wts/wtb/wtt + decant culture | swap | Liquidity signal: what trades fast = revealed demand | Trade-rule heavy | live_read |
| r/Indiemakeupandmore | ~148K | Indie perfume-oil + indie beauty buyers; consumers, creators, AND shop owners | review, haul, rec_ask | Indie-house demand pool; overlaps fragrance and beauty lanes. Posture is the outlier: shop owners are welcome, so indie-brand self-promo is tolerated — the one listed venue where brand presence is native | Disclosure rules; self-promo tolerated for indie shops | live_read |

## Tier 4 — Beauty core hubs (consumer-demand lane, hub level)

| Subreddit | Size band | Audience shape | Dominant signals | Radar / GTM note | Posture | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| r/SkincareAddiction | ~5.0M | Largest skincare hub; routine-driven, science-based per its own bio | rec_ask, review | Category-scale demand pool; very high volume (historically 1000+ posts/day) | Verified strict: structured-post/routine-template rules, flair-gating, heavy self-promo restriction | live_read |
| r/MakeupAddiction | ~7.5M | Largest venue in this entire inventory; looks + product talk | review, haul, rec_ask | Category-scale; haul culture = purchase display. Web-cached claims (3–4M) badly undercounted it | Some self-promo limits | live_read |
| r/SkincareAddicts | ~1.2M | Less-strict spinoff/alternative to the flagship; "positive newbie-friendly" per bio | rec_ask, review | Same demand pool, looser posting rules — often easier signal to read | Looser than flagship | live_read |
| r/AsianBeauty | ~3.76M | K/J-beauty; ingredient-forward, import-savvy | rec_ask, review, haul | Trend-leading venue: K-beauty waves surface here before mass market | Strict sourcing rules (model_knowledge) | live_read |
| r/30PlusSkinCare | ~2.42M | Mature-skin demographic; higher spend capacity | rec_ask, review | Demographic wedge with strong purchase intent — far larger than expected | Moderate (model_knowledge) | live_read |
| r/beauty | ~1.85M | General beauty catch-all; beginner-heavy | rec_ask | Lower signal density than the dedicated hubs | — | live_read |
| r/HaircareScience | ~1.05M | Ingredient-literate haircare; active since 2013 | rec_ask, review | Haircare demand pool, evidence-oriented buyer language | Strict | live_read |
| r/curlyhair | ~1.4M | Curly-method community; product-routine-driven | rec_ask, review, haul | Product-dense; routine culture drives repeat purchase talk. Press-noted mixed inclusivity record for Black natural hair — see r/NaturalHair and r/blackhair in Tier 5 | Moderate (model_knowledge) | live_read |
| r/lacqueristas | ~74K | Indie nail-polish/lacquer community (seed name r/RedditLaqueristas appears stale; live community goes by this name) | review, haul | Nail-category hub; review-heavy, indie-brand purchase intent | — | live_read |

## Tier 5 — Beauty demographic / regional hubs

| Subreddit | Size band | Audience shape | Dominant signals | Radar / GTM note | Posture | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| r/IndianSkincareAddicts | ~314K | Indian market; science-forward, mixes international + local brands | rec_ask, review, deal | Regional demand pool; dupe/afford discourse strong | Moderate | live_read |
| r/EuroSkincare | ~119K | EU availability/regulatory-aware buyers | rec_ask, review | Regional routing for EU demand questions | Moderate | live_read |
| r/AusSkincare | ~220K | Australian + NZ market | rec_ask, review | Regional routing | — | live_read |
| r/KoreanBeauty | ~369K | K-beauty-only; industry-cited as higher purchase intent and brand loyalty than the broader hub | rec_ask, review, haul | Higher-intent niche alternative to r/AsianBeauty | — | live_read |
| r/malegrooming | ~1.08M | Men's hair/beard/skincare demographic hub ("number one... community on Reddit for men" per bio) | rec_ask, review | Men's-demographic routing; overlaps the fragrance male demand pool; much larger than expected | — | live_read |
| r/NaturalHair | ~428K | Black natural-hair community | rec_ask, review, haul | Fills the Black-haircare demographic gap; primary venue | — | live_read |
| r/blackhair | ~167K | Black hair care and admiration, all types/techniques | rec_ask, review | Companion Black-haircare venue | — | live_read |
| r/tretinoin | ~287K | Retinoid community (tretinoin, adapalene, tazarotene per bio); high routine adherence | review, rec_ask | Ingredient-level demand depth; adjacent-product asks common | Moderate | live_read |

## Tier 6 — Retailer / deal / purchase-intent venues

| Subreddit | Size band | Audience shape | Dominant signals | Radar / GTM note | Posture | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| r/Sephora | ~1.06M | Retailer-anchored; sale-cycle-driven | deal, haul, rec_ask | Purchase-intent-dense; sale threads = live conversion talk | Retailer-specific rules | live_read |
| r/Ulta | ~158K | Retailer-anchored (unofficial, fans + employees per bio) | deal, haul | Same pattern as r/Sephora, different assortment | — | live_read |
| r/MUAontheCheap | ~1.13M | Deal-hunters across beauty incl. fragrance sales (per bio); running since 2017 | deal | Price-elasticity radar; what moves on discount | Actively moderated, deal-format rules | live_read |
| r/MakeupDupes | ~69K | Dupe-finders (beauty analog of r/fragranceclones) | dupe_ask, review | Comparison-shopping intent; directly relevant if the beauty lane follows the aphrodite dupe-audience wedge | — | live_read |
| r/BeautyBoxes | ~523K | Subscription-box buyers | review, haul | Sampling-economy signal; discovery-driven buyers — far larger than expected | — | live_read |

## Tier 7 — Creator-watch (creator_signal radar)

| Subreddit | Size band | Audience shape | Dominant signals | Radar / GTM note | Posture | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| r/BeautyGuruChatter | ~3.08M | Creator-commentary community (influencers, MUAs, brand owners per bio) | creator_talk | Direct creator_signal radar: rising/falling creator credibility, sponsorship fatigue, scandal risk — inputs the product's creator vetting reads care about. The 3.1M web claim was real, not inflated — this venue is category-scale | Strict; no brigading (model_knowledge) | live_read |

## Tier 8 — Counterevidence / anti-consumption venues

CSB boards carry mandatory counterevidence paths; these venues are where the
counter-wave shows first.

| Subreddit | Size band | Audience shape | Dominant signals | Radar / GTM note | Posture | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| r/MakeupRehab | ~189K | Anti-overconsumption; no-buy/low-buy support culture per its own bio; regret and de-influencing talk | anti_haul | Counterevidence venue: hype fatigue, manufactured-demand skepticism. Purchase intent is suppressed by design — that inversion is the signal | Supportive-community rules | live_read |
| r/PanPorn | ~978K | Project-pan (use-it-up) culture; "well-loved makeup" | anti_haul, review | Usage-depth signal: what actually gets used vs shelfware — near-1M scale makes this a serious counterevidence pool | Moderate | live_read |

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

Verification method: two web-search-only passes (2026-07-16), then a live
seeding pass the same day — direct same-context `about.json` reads via the
operator's browser session for all 35 tracked subs (exact counts, bios,
titles, creation dates now in the registry; no Bronze packet exists for
that pass). Every previously open count item is resolved.

Resolutions from the live pass (2026-07-16):

- All counts confirmed at exact values (registry is authoritative). Notable
  corrections vs the web-cached pass: r/MakeupAddiction is ~7.5M (web
  claims of 3–4M badly undercounted); r/AsianBeauty ~3.76M and
  r/BeautyGuruChatter ~3.08M (the "inflated-looking" claims were real);
  r/PanPorn ~978K; r/30PlusSkinCare ~2.42M; r/malegrooming ~1.08M;
  r/BeautyBoxes ~523K.
- r/arabfragrances exists but is dead (1 member, created 2024): no
  Arab-specific venue; r/DesiFragranceAddicts is the regional community.
- Black-haircare gap filled: r/NaturalHair (~428K) and r/blackhair (~167K)
  added to Tier 5 and the registry.
- r/basenotes returns 403 (private/banned): not a venue. The Basenotes
  brand is a standalone non-Reddit forum, worth its own row in any future
  cross-forum inventory.
- `active_user_count` was not exposed to the session's reads; the field
  stays opportunistic in the registry.

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
