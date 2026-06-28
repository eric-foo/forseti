# ChatGPT Pro Consumer Category Online Food vs Fragrance Prompt v1

```yaml
retrieval_header_version: 1
artifact_role: Product planning prompt artifact
scope: >
  Portable prompt and source pack manifest for asking ChatGPT Pro to compare
  whether Orca should keep the current fragrance opening or run an online-first
  / ecommerce-led food CPG category screen while staying inside the
  consumer-demand decision-intelligence thesis.
use_when:
  - Asking ChatGPT Pro for current web research on online-first food CPG versus
    fragrance as an Orca consumer-demand first opening.
  - Testing whether Feastables is a useful positive exemplar of online food
    demand mechanics, not a celebrity-brand target and not broad food.
  - Preparing a no-contact category-screen decision before outreach, capture, or
    implementation.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_product_thesis_consumer_demand_v0.md
  - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
  - orca/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md
  - orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
  - orca/product/spines/product_lead/proof_charter/orca_product_proof_lead_charter_v0.md
  - docs/research/orca_discovery_candidate_scan_beauty_neutral_chatgptpro_v0.md
  - docs/research/orca_discovery_candidate_scan_beauty_subniche_chatgptpro_v0.md
  - docs/research/orca_discovery_candidate_scan_food_vs_fragrance_chatgptpro_v0.md
  - orca/product/satellites/fragrance/judgment_level1/reconciliation/fragrance_level1_product_learning_reconciliation_v0.md
  - orca/product/satellites/fragrance/judgment_level1/satellite_skeleton/fragrance_level1_product_learning_satellite_skeleton_v0.md
stale_if:
  - Orca's product thesis, first-proof wedge, buyer-proof gate, or current
    fragrance advisory intake changes.
  - A verified no-contact category scan supersedes this prompt.
  - Online-first food, ecommerce-led CPG, social commerce, DTC food, or
    fragrance source access changes materially enough to alter candidate-slot
    density or public-signal availability.
```

## Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: S2 product anchor + targeted prior ChatGPT Pro fragrance/beauty advisory intakes + food-vs-fragrance v0 intake caveat + fragrance satellite boundary
  edit_permission: docs-write
  target_scope: create a v1 product-planning prompt artifact for corrected online-first food vs fragrance comparison; no product doctrine change
  dirty_state_checked: yes
  blocked_if_missing: clean isolated worktree, controlling product thesis/wedge/proof sources, prior fragrance advisory intake, owner clarification
```

## Prompt Preflight

```text
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below.

output_mode: file-write
prompt_artifact_path: docs/prompts/product-planning/chatgptpro_consumer_category_online_food_vs_fragrance_prompt_v1.md
downstream_response_destination: ChatGPT Pro chat response; later filing as docs/research intake requires a separate docs-write pass.
template_kind: none
template_source: adjacent product-planning precedent docs/prompts/product-planning/chatgptpro_beauty_subniche_research_prompt_v0.md, used as pattern only.
edit_permission: docs-write for this artifact; read-only for the ChatGPT Pro recipient.
target_files_or_dirs: docs/prompts/product-planning/
branch_or_commit_reference: codex/consumer-demand-category-prompt at main-derived HEAD 666c4f14 plus later prompt/intake commits on the same branch.
dirty_state_allowance: isolated worktree clean at start; do not consume dirty root-lane changes.
doctrine_change_decision: no doctrine change intended; this is decision preparation only.
reviews: not a review prompt; require blunt stress-test output but no formal verdict lane.
destinations: this file is the durable prompt artifact; recipient writes no repo artifact.
thread_operating_target_continuity: no visible active thread_operating_target carried.
```

## Cynefin Routing

Smallest complete outcome: a paste-ready, source-bound ChatGPT Pro prompt that tests online-first food CPG versus the current fragrance opening under Orca's buyer-proof criteria.

Regime: Mixed - complicated product authority plus complex market uncertainty.

Why: Orca has a locked consumer-demand/beauty first-proof direction and an advisory fragrance queue, but the owner's intended comparator is not broad food. It is online selling of food: online-first, ecommerce-led, social-commerce-visible, DTC/Amazon/TikTok Shop/retailer-PDP food CPG where public demand may show before internal data is conclusive.

Decomposition: Risk-first probe through a corrected no-contact research prompt.

Current bottleneck: Whether online-first food CPG can produce enough memo-grade, public-signal candidate slots without collapsing into private conversion data, retailer sell-through, supply-chain/logistics, sensory/R&D, margin/trade-spend, or claims/regulatory questions.

Riskiest assumption: Feastables is only celebrity hype. The owner's intended use is different: Feastables is the best-known positive exemplar of online attention converting into trial, visible purchase behavior, retail/distribution decisions, and imitation pressure. The question is whether that mechanism appears in other online-first food sub-wedges in an Orca-usable way.

Stop or pivot condition: Online-first food wins only on audience size, celebrity, social engagement, retail scale, or broad category TAM, without named operators, live allocation decisions, independent public demand origins, and costly-behavior evidence.

Allowed next move: Ask ChatGPT Pro for current web research and a category-screen recommendation with citations and explicit non-claims.

Disallowed next move: Treat online-first food as selected, outreach-ready, or superior to fragrance before a no-contact scan clears Orca's buyer-proof gates.

## Source Capsule

Use this capsule if the full source pack is not uploaded. If the source files are uploaded, read them first and treat this capsule as orientation only.

- Orca's current product thesis: evidence-backed strategic decisions for consumer-market leaders before internal data is conclusive. The first reads are demand integrity, durability, and related consumer-demand evidence, with action ceilings such as monitor, probe, commit, hold, scale, avoid, or reduce.
- Current first-proof wedge: US-market tractioned indie/DTC beauty or personal-care operators with a named decision owner and a live 30-90 day demand-allocation decision. Priority decision families are retail/channel expansion, launch/reposition, inventory or purchase-depth commitment, with tier/price, taste-shift, and defend/hold decisions eligible if they pass the same gates.
- Orca sells a decided answer for one named decision, not a trend feed, social-listening dashboard, source dump, generic research report, or deck shop. The minimum proof artifact is a manual decision memo plus evidence appendix; the buyer-facing premium surface is an executive decision deck derived from that substrate.
- Buyer-proof gate: public signals must be relevant to a live decision, include at least one gradeable costly-behavior instance in a qualifying demand-origin family, and use integrity labels. A material or irreversible action needs at least two converging effectively independent origins. Engagement volume alone is not enough.
- Pull means decision or budget-adjacent behavior, not praise. Generic interest, free research asks, and dashboard/feed requests are not buyer pull.
- Current advisory incumbent: neutral ChatGPT Pro research ranked fragrance first for verification, specifically minis/discovery/travel formats plus scent-layering/body/hair mists, with hair/scalp and skincare as live comparators. This is advisory only, not verified Orca evidence.
- Fragrance boundary: Orca has repo-local fragrance product-learning skeleton/reconciliation artifacts, but no admitted fragrance casebook, no completed product-learning receipt, no buyer proof, no source-capture authority, and no judgment-quality evidence.
- Prior food-vs-fragrance v0 answer caveat: the v0 answer is useful but overbroad for food because the owner clarified that Feastables was meant as the strongest positive exemplar of online food demand mechanics, not as a broad food or celebrity-brand shortcut.
- Food is not currently selected in Orca sources. Treat online-first food CPG as a candidate vertical that must earn a no-contact category screen.

## Paste-Ready ChatGPT Pro Prompt

```text
You are helping Orca decide whether to keep its current fragrance opening or run an online-first / ecommerce-led food CPG category screen while staying inside Orca's consumer-demand decision-intelligence thesis.

Important correction: when I mention Feastables, I do not mean "this looks impressive" or "copy MrBeast." I mean Feastables is the best-known positive example of a possible online food demand pattern: online attention converts into trial, public purchase/review/restock signals, retail or distribution allocation decisions, and imitation pressure. Abstract the mechanism before judging the category.

Be blunt. If my framing is wrong, say so. The question is NOT "which category is more exciting?" The question is: which opening can produce Orca-qualified, memo-grade no-contact candidate slots fastest, without becoming generic trend research, social listening, supply-chain consulting, sensory product development, or internal-data analytics?

Source context:

Orca helps consumer-market leaders make evidence-backed strategic decisions before internal data is conclusive. The first proof lane is consumer-demand decision intelligence: demand integrity, durability, and related public-signal reads that support action ceilings such as monitor, probe, commit, hold, scale, avoid, or reduce.

Current first-proof wedge: US-market tractioned indie/DTC beauty or personal-care operators with a named decision owner and a live 30-90 day demand-allocation decision. Priority decision families: retail/channel expansion, launch/reposition, inventory or purchase-depth commitment. Tier/price, taste-shift, and defend/hold decisions are eligible only if they pass the same public-signal gates.

Current advisory incumbent: prior neutral ChatGPT Pro research ranked fragrance first for verification, specifically indie fragrance / minis / discovery / travel formats / scent-layering / body and hair mists. Hair/scalp and skincare stayed live comparators. This fragrance result is advisory only, not verified buyer proof.

Buyer-proof criteria to use:
- named operator or accountable decision owner visible in public sources;
- live 30-90 day allocation decision or a tightly plausible decision trigger;
- public demand signal from effectively independent origins, not one PR or creator hype chain;
- at least one gradeable costly-behavior instance such as DTC sellouts, waitlists, subscription/repeat-purchase signals, marketplace/PDP review depth, restocks, retail door expansion, switching/dupe behavior, durable buyer pressure, or other buyer action;
- material action needs at least two converging independent origins;
- engagement volume alone is not enough;
- no dependency on proprietary sell-through, CRM, cohort, panel, retailer internal data, hidden pages, paid data, or absurd-risk source access;
- the output should be a decision memo / evidence appendix / decision deck, not a feed or dashboard.

Decision to prepare:

Assuming Orca remains in consumer demand, should Orca:
A. continue with the current fragrance opening;
B. switch the next no-contact category screen to online-first / ecommerce-led food CPG, using Feastables as the best-known positive exemplar of the demand mechanics;
C. run a side-by-side no-contact screen between fragrance and one online-food sub-wedge; or
D. reject both and name a stronger consumer-demand opening?

Important: "online-first food CPG" is still too broad. Decompose it before scoring. At minimum evaluate:
- ecommerce-first shelf-stable snacks or confectionery with DTC, Amazon, TikTok Shop, social-commerce, or retailer-PDP visibility;
- creator-led / entertainment-led food brands where online demand visibly precedes or shapes retail expansion, Feastables-like but not Feastables-anchored;
- premium chocolate / candy / confectionery challenger brands selling online with public restock, waitlist, review, or marketplace evidence;
- better-for-you snacks, protein bars, functional snacks, or clean-label snacking with online subscription/repeat-purchase/review surfaces;
- limited-drop / fandom / collab food products with online sellouts, restocks, and resale/dupe/imitation pressure;
- shelf-stable beverage, hydration, energy, powders, sachets, or functional drink challengers only where online selling is visible and logistics do not dominate;
- ingestible beauty, collagen, gummies, wellness food, or functional nutrition only if you clearly flag claims/regulatory drag.

Do not evaluate broad restaurants, meal delivery, fresh grocery, cold-chain foods, commodity grocery, or food-service channels unless you explain why they fit the online-first public-signal question.

For fragrance, evaluate the incumbent tightly:
- indie/DTC fragrance;
- minis / discovery / travel formats;
- scent-layering systems;
- body mists / hair mists / fragrance-adjacent body care;
- retail-door, inventory-depth, format-extension, and launch/reposition decisions.

Treat Feastables as a positive exemplar of a possible mechanism: online attention, product trial, public purchase/review/restock evidence, retail expansion, distribution/inventory decisions, and competitive imitation risk. Do not assume Feastables itself is an Orca target, and do not assume MrBeast's audience generalizes. The test is whether other online-first food sub-wedges expose the same kind of public demand mechanics without depending mainly on celebrity distribution, retailer internal sell-through, supply chain, taste testing, margin structure, trade spend, paid panels, or private data.

Use current public web research. Cite every load-bearing external claim with a URL and publication date when available. Prefer primary sources, brand sites, DTC stock/restock/waitlist surfaces, retailer/PDP evidence, Amazon/TikTok Shop/marketplace evidence where accessible without login, founder/operator interviews, trade press, category data, review/forum evidence, and public demand surfaces. Do not contact brands. Do not scrape behind logins. Do not recommend outreach copy. Do not claim buyer validation, willingness to pay, product readiness, commercial readiness, or outreach authorization.

Scoring rubric, 100 points:
- Candidate-slot density /15: how many plausible no-contact candidate contexts exist.
- Online public demand visibility /15: DTC, marketplace, PDP, social commerce, restock, waitlist, review, subscription, or repeat-purchase signals visible without private access.
- Public signal quality and independence /15: source-visible, non-PR-derived, independently originated signals.
- Live decision pressure /15: visible 30-90 day allocation decisions.
- Costly-behavior visibility /15: sellouts, waitlists, restocks, repeat purchase, review depth, retail expansion, switching/dupe behavior, or durable buyer action.
- Named operator visibility /10: founder, CEO, head of brand/growth/insights/strategy, or equivalent operator visible enough for a decision-owner hypothesis.
- Decision-artifact fit /5: can Orca produce a decision memo/deck from public evidence, not a feed/dashboard or generic trend report?
- Proprietary-data independence /5: lower dependency on internal sell-through, retailer data, supply-chain, panel, cohort, sensory, or paid data.
- Claims/regulatory/logistics/sensory drag /3: lower risk is better; penalize FDA/FTC/health/efficacy/nutrition, cold-chain, freshness, taste, and logistics-heavy contexts where they dominate market-demand evidence.
- Repeatability /2: multiple brands face similar decision patterns.

Penalty flags:
- one_origin_hype
- celebrity_or_creator_dependency
- private_data_dependency
- retailer_internal_data_dependency
- supply_chain_or_margin_dependency
- sensory_or_product_R&D_dependency
- claims_or_regulatory_drag
- logistics_or_freshness_drag
- feed_or_dashboard_pull
- operator_not_visible
- too_scaled_or_acquired_for_first_proof
- no_live_decision
- not_online_first

Required output:

1. Recommendation
- Choose one: continue fragrance, switch to a named online-food sub-wedge, run side-by-side fragrance vs online-food screen, or reject both for a better opening.
- Confidence: high / medium / low.
- One blunt paragraph explaining whether my online-food / Feastables-as-positive-exemplar instinct is good, overnarrow, or still weaker than fragrance.

2. Category Decomposition
- Break online-first food CPG into sub-wedges before scoring.
- Break fragrance into sub-wedges before scoring.
- State which sub-wedges you dropped before scoring and why.

3. Ranked Sub-Wedge Table
Columns:
- category;
- sub-wedge;
- score by criterion;
- total /100;
- penalty flags;
- short rationale;
- sources.

4. Online Food / Feastables Mechanism Test
Answer directly:
- What is the actual reusable mechanism, if any?
- Which online-food sub-wedges share it?
- Which parts of Feastables are not reusable for Orca?
- Would a Feastables-like online-food pattern likely need internal retailer/sell-through/supply-chain data before Orca's public-signal memo is useful?

5. Fragrance Incumbent Stress Test
Answer directly:
- Why might fragrance still be the better first opening even if online food has a stronger exemplar?
- What evidence would make fragrance lose?
- What evidence would make online-first food beat fragrance?
- Is fragrance smaller but cleaner, or actually weaker once the corrected online-food comparator is checked?

6. Candidate Slot Examples
For the top three sub-wedges overall, list the strongest public candidate contexts you can find.
For each:
- brand/context;
- public decision trigger;
- decision family;
- named operator or public role;
- independent venue origins visible;
- online public-demand surface visible;
- costly-behavior evidence;
- source links;
- qualification status: strong / tentative / reject / needs follow-up.

Include at least five online-food candidate contexts and five fragrance candidate contexts if available. If not available, say that the category failed slot-density expectations.

7. No-Contact Scan Plan
Give a 1-week no-contact scan plan:
- day-by-day checks;
- what counts as a pass;
- what kills or downgrades online-first food;
- what kills or downgrades fragrance;
- whether the next scan should be online-food-only, fragrance-only, or side-by-side.

8. Final Decision Prep
Return the exact next action Orca should take:
- "run fragrance no-contact scan first";
- "run online-food no-contact scan first on [named sub-wedge]";
- "run side-by-side scan: fragrance [sub-wedge] vs online-food [sub-wedge]";
- or "do not run either yet; first research [specific missing thing]."

9. Non-Claims
State explicitly that this is not buyer validation, not willingness-to-pay proof, not outreach authorization, not capture authorization, not product readiness, not commercial readiness, and not proof that any named brand is a buyer or lead.
```

## Source-Read Ledger

- `AGENTS.md` - project behavior and prompt-artifact rules.
- `.agents/workflow-overlay/README.md` - overlay entrypoint.
- `.agents/workflow-overlay/source-loading.md` - S2 product anchor and prompt source-loading requirements.
- `.agents/workflow-overlay/prompt-orchestration.md` - durable/cross-recipient prompt contract.
- `.agents/workflow-overlay/decision-routing.md` - Cynefin routing layer.
- `.agents/workflow-overlay/source-of-truth.md` - source hierarchy and doctrine-change boundary.
- `.agents/workflow-overlay/artifact-folders.md` - accepted prompt artifact folders.
- `.agents/workflow-overlay/template-registry.md` - no bound product-planning template; adjacent prompt used as precedent only.
- `.agents/workflow-overlay/product-proof.md` - trust, pull, kill, and non-claim semantics.
- `docs/decisions/orca_product_thesis_consumer_demand_v0.md` - controlling product thesis.
- `docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md` - current first-proof wedge.
- `orca/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md` - offer and first-proof fit gates.
- `orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md` - buyer-proof gate and proof standards.
- `orca/product/spines/product_lead/proof_charter/orca_product_proof_lead_charter_v0.md` - proof-lead scope and exclusions.
- `orca/product/spines/foundation/product_contract/core_spine_v0_product_contract.md` - core/satellite and decision-artifact boundary.
- `docs/prompts/product-planning/chatgptpro_beauty_subniche_research_prompt_v0.md` - adjacent ChatGPT Pro prompt precedent.
- `docs/prompts/product-planning/chatgptpro_consumer_category_food_vs_fragrance_prompt_v0.md` - v0 broad-food prompt superseded for the corrected online-food question.
- `docs/research/orca_discovery_candidate_scan_food_vs_fragrance_chatgptpro_v0.md` - v0 answer intake caveat and overbroad-food warning.
- `docs/research/orca_discovery_candidate_scan_beauty_subniche_chatgptpro_v0.md` - prior advisory fragrance intake.
- `docs/research/orca_discovery_candidate_scan_beauty_neutral_chatgptpro_v0.md` - neutral advisory fragrance ranking and verification queue.
- `orca/product/satellites/fragrance/judgment_level1/reconciliation/fragrance_level1_product_learning_reconciliation_v0.md` - fragrance product-learning cap.
- `orca/product/satellites/fragrance/judgment_level1/satellite_skeleton/fragrance_level1_product_learning_satellite_skeleton_v0.md` - fragrance skeleton and non-claims.

## Non-Claims

This prompt is decision preparation only. It does not select online-first food, reject fragrance, create buyer proof, authorize outreach, authorize capture, authorize implementation, prove willingness to pay, prove product readiness, or establish commercial readiness.
