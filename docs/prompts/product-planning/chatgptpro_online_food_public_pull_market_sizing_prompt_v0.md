# ChatGPT Pro Online Food Public Pull And Market Sizing Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Product planning prompt artifact
scope: Standalone ChatGPT Pro prompt for finding the strongest online-first food CPG public-pull subniche for Orca, including active-company density, influencer-demand quality, public pull, memo convertibility, and TAM/SAM/SOM.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_product_thesis_consumer_demand_v0.md
  - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
  - orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
  - .agents/workflow-overlay/product-proof.md
stale_if:
  - Orca's product thesis, first-proof wedge, or buyer-proof gate changes.
  - A verified online-food no-contact scan supersedes this prompt.
```

## Prompt Preflight

```text
output_mode: file-write
prompt_artifact_path: docs/prompts/product-planning/chatgptpro_online_food_public_pull_market_sizing_prompt_v0.md
downstream_response_destination: ChatGPT Pro chat response; later filing as docs/research intake requires a separate docs-write pass.
template_kind: none
edit_permission: docs-write for this artifact; read-only for the ChatGPT Pro recipient.
doctrine_change_decision: no doctrine change intended; this is decision preparation only.
```

## Paste-Ready ChatGPT Pro Prompt

```text
You are helping Orca research the ONLINE-FIRST FOOD CPG lane independently.

Do NOT frame this as food versus beauty or food versus fragrance. Do NOT choose whether food is better than beauty. Your job is to find the strongest online-first food CPG subniche for Orca's consumer-demand decision-intelligence proof lane.

Core question:

Within online-first / ecommerce-led food CPG, which subniche has the strongest combination of:
1. qualified active-company density;
2. influencer quantity AND influencer-originated demand quality;
3. other public pull signals that indicate costly behavior, not just attention;
4. live decision pressure that can convert into a useful Orca memo; and
5. credible TAM/SAM/SOM at both the broad category and selected subniche levels?

Feastables is a positive exemplar of possible online-food demand mechanics, not a target and not a celebrity shortcut. Use it only to abstract the mechanism: online attention converts into trial, public purchase/review/restock signals, retail/distribution decisions, and imitation pressure. Then test whether other online-food subniches show the same mechanism without depending mainly on celebrity distribution or private data.

Source context:

Orca helps consumer-market leaders make evidence-backed strategic decisions before internal data is conclusive. The first proof lane is consumer-demand decision intelligence: demand integrity, durability, and related public-signal reads that support action ceilings such as monitor, probe, commit, hold, scale, avoid, or reduce.

Current first-proof wedge in Orca sources is beauty-first, but this prompt is deliberately exploring online-first food as a possible consumer-demand lane. Do not decide against beauty; assess food on its own merits and weaknesses.

Orca sells a decided answer for one named decision, not a trend feed, social-listening dashboard, source dump, generic research report, or deck shop. The proof artifact is a manual decision memo plus evidence appendix.

Buyer-proof criteria to use:
- named operator or accountable decision owner visible in public sources;
- live 30-90 day allocation decision or a tightly plausible decision trigger;
- public demand signal from effectively independent origins, not one PR or creator hype chain;
- at least one gradeable costly-behavior instance such as DTC sellouts, waitlists, subscription/reorder signals, marketplace/PDP review depth, restocks, retail door expansion, switching/dupe behavior, durable buyer pressure, or other buyer action;
- material action needs at least two converging independent origins;
- engagement volume alone is not enough;
- no dependency on proprietary sell-through, CRM, cohort, panel, retailer internal data, hidden pages, paid data, or absurd-risk source access;
- the output should support a decision memo / evidence appendix / decision deck, not a feed or dashboard.

Definitions:

"Online-first food CPG" means packaged food or beverage brands where online discovery, DTC, social commerce, marketplace, creator content, community demand, or public PDP/review surfaces materially precede, shape, or reveal retail/channel decisions. Prioritize shelf-stable categories. Exclude restaurants, meal delivery, fresh grocery, commodity grocery, food service, cold-chain-heavy products, and pure nutrition/medical claims unless they clearly pass the public-pull and memo-convertibility test.

"Active company" means a brand/operator with current launches, retail/channel movement, format expansion, SKU decisions, or visible public demand surfaces in the last 12 months. Do not count dead brands, purely legacy brands, or companies too scaled/acquired for Orca's first proof unless you mark them as benchmarks only.

"Influencer quantity" means observable creator breadth around a subniche or company. "Influencer demand quality" means evidence that creator activity produced or coincided with purchase intent or costly behavior: comments asking where to buy, stockout/restock pressure, retailer/PDP review growth, waitlists, subscription/reorder behavior, dupe/switching behavior, marketplace demand, or repeated unpaid creator coverage. Discount paid seeding, affiliate floods, creator-owned audience concentration, and launch PR.

"Public pull" is broader than influencer demand: retailer/PDP reviews, DTC stock status, waitlists, restocks, subscription/reorder surfaces, marketplace rank/reviews where visible without login, TikTok Shop/Amazon/Target/Walmart/retailer PDP activity, community/forum demand, dupe/switching behavior, retail expansion, assortment changes, launch depth, and public operator commentary.

TAM/SAM/SOM must be split into two layers:

Layer A - End-market sizing:
- TAM: broad consumer spend for online-relevant packaged food/snack/confectionery/food CPG, preferably US-first with global noted separately if useful.
- SAM: online-visible / digitally influenced / DTC-retail / ecommerce-relevant portion Orca can observe through public signals.
- SOM: selected online-food subniche's realistic public-signal arena for the first proof lane, not a fake revenue capture claim.

Layer B - Orca decision-opportunity sizing:
- TAM: approximate universe of active US online-first food CPG companies where consumer-demand decisions could matter.
- SAM: companies in online-visible subniches with public demand surfaces, named operators, and live allocation decisions.
- SOM: first-proof reachable candidate-slot count over the next 30 days, not outreach conversion, not revenue, and not willingness-to-pay proof.

Use current public web research. Cite every load-bearing claim with a URL and publication date when available. Prefer primary sources, brand/DTC stock/restock/waitlist surfaces, retailer/PDP evidence, marketplace evidence accessible without login, founder/operator interviews, trade press, market data, review/forum evidence, creator/social surfaces accessible without login, and public demand surfaces. Do not contact brands. Do not scrape behind logins. Do not recommend outreach copy. Do not claim buyer validation, willingness to pay, product readiness, commercial readiness, or outreach authorization.

Subniches to evaluate before selecting the strongest online-food lane:
- shelf-stable DTC-to-retail better-for-you snacks;
- ecommerce-first crackers, chips, puffs, candy, or confectionery;
- creator-led / entertainment-led candy or snacks, Feastables-like but not Feastables-anchored;
- premium or functional chocolate challenger brands;
- protein bars, protein snacks, or functional snacks with online subscription/reorder/review surfaces;
- kids/family better-for-you snacks if public pull and operator visibility are strong;
- limited-drop / fandom / collab food products where scarcity can be audited;
- shelf-stable powders, hydration, energy, sachets, or functional drinks where claims/logistics do not dominate;
- ingestible wellness, collagen, gummies, or functional nutrition only if you clearly flag claims/regulatory drag.

Scoring rubric, 100 points:
- Qualified active-company density /15
- Online public-pull surface quality /15
- Influencer demand quality /12
- Public signal independence /10
- Live decision pressure /12
- Costly-behavior visibility /12
- Named operator visibility /8
- Decision memo convertibility /8
- Proprietary-data independence /4
- Low claims/logistics/sensory/margin drag /4

Blindspot audit:
- paid seeding / affiliate flood mistaken for demand;
- creator-owned audience concentration mistaken for category pull;
- one-origin launch hype;
- engineered scarcity mistaken for durable demand;
- platform algorithm spike mistaken for durable pull;
- category size mistaken for Orca buyer opportunity;
- private retailer/sell-through dependency;
- margin/trade-spend/COGS/supply capacity dominating the decision;
- taste/sensory testing dominating the decision;
- claims/regulatory/compliance questions dominating the decision;
- no named accountable operator;
- no live decision in the next 30-90 days;
- too scaled/acquired for first proof;
- too fragmented or too tiny to produce repeatable slots;
- generic dashboard/feed pull rather than memo-convertible decisions.

Required output:

1. Executive Recommendation
- Name the strongest online-first food CPG subniche for Orca's next no-contact scan.
- Confidence: high / medium / low.
- One blunt paragraph explaining why this subniche wins inside online-food.
- State whether Feastables-like mechanics are actually reusable here or just a benchmark.

2. TAM/SAM/SOM
Return two sizing tables:
- End-market sizing: overarching TAM, online-visible SAM, selected-subniche SOM/public-signal arena, geography/year, sources, confidence/caveats.
- Orca decision-opportunity sizing: active-company TAM, qualified public-pull company SAM, 30-day first-proof candidate-slot SOM, method, sources, confidence/caveats.

Do not inflate precision. Ranges are better than fake exactness.

3. Subniche Comparison Table
For every evaluated subniche: score by criterion, total /100, active-company count estimate, public-pull surfaces, influencer demand quality, memo-convertible decision families, penalty flags, rationale, sources.

4. Top Company Roster
For the winning subniche, list at least 20 active companies if possible. If fewer than 20 qualify, say so. For each: brand/company, current trigger, decision family, named operator or role, public pull surfaces, influencer-demand evidence, costly-behavior evidence, likely highest action ceiling, qualification status, and source links.

5. Public Pull Map
Separate influencer-originated demand, retailer/PDP demand, DTC/stock/restock/waitlist demand, marketplace/social-commerce demand, review/forum/community demand, operator/retailer commentary, and weak or misleading signals.

6. Memo Convertibility
State the strongest memo shapes Orca could produce in this lane and what public evidence would support each: first retail rollout depth, DTC-to-retail channel mix, SKU/flavor depth, pack-size or variety-pack decision, inventory/restock depth, limited-drop repeatability, price/tier, hold/avoid.

7. Kill / Downgrade Conditions
State exactly what would make this online-food lane fail the first no-contact scan.

8. One-Week No-Contact Scan Plan
Give a day-by-day scan plan for this online-food lane only.

9. Non-Claims
State explicitly that this is not buyer validation, not willingness-to-pay proof, not outreach authorization, not capture authorization, not product readiness, not commercial readiness, and not proof that any named company is a buyer or lead.
```

## Non-Claims

This prompt is decision preparation only. It does not select online-first food, create buyer proof, authorize outreach, authorize capture, authorize implementation, prove willingness to pay, prove product readiness, or establish commercial readiness.
