# ChatGPT Pro Beauty Sub-Niche Research Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Product planning prompt artifact
scope: >
  Portable prompt and source pack manifest for asking ChatGPT Pro to research
  which beauty/personal-care sub-niche Orca should test first for the
  consumer-demand operator wedge.
use_when:
  - Commissioning external web research on Orca's first beauty sub-niche.
  - Comparing fragrance, scalp/haircare, body care, SPF/sun-makeup, and any
    stronger surfaced alternatives against Orca's buyer-proof gates.
  - Preparing a no-contact candidate-scan decision before any outreach,
    capture, or implementation.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_product_thesis_consumer_demand_v0.md
  - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
  - docs/product/product_lead/orca_buyer_proof_packet_v0.md
  - docs/product/source_capture_toolbox/ig_creator_roster_frontier_ledger_spec_v0.md
stale_if:
  - Orca's first commercial target, buyer-proof gate, demand-read taxonomy, or
    beauty creator roster/frontier spec changes.
  - A completed sub-niche scan supersedes this prompt's hypothesis set.
```

## Operator Context

You are helping Orca choose the first beauty/personal-care sub-niche to test.
Use the uploaded source documents as Orca's internal constraints, then use
current public web research to evaluate the market. Cite every load-bearing
external claim with a URL and publication date when available.

This is **research and decision preparation only**. Do not contact brands,
scrape behind logins, recommend outreach copy, propose paid data acquisition,
or treat candidate companies as leads. Do not claim buyer validation,
willingness to pay, product readiness, or commercial readiness.

## Orca's Current Buyer And Product Frame

Orca's current first commercial target is:

> US-market tractioned indie/DTC beauty or personal-care operators with a named
> founder, head of brand, growth, insights, strategy, or equivalent decision
> owner facing a live 30-90 day consumer-demand allocation decision where
> internal data is not conclusive and public creator/social/review/search/retail
> signals can be fused across at least two independent venue families.

Orca's product promise for this first proof is not "trend reports" or social
listening. Orca should produce a decision memo/evidence appendix, and later an
executive decision deck only if proof gates pass, that helps the operator decide
whether demand is:

- durable: commit;
- real but transient: move in-window / time-box;
- manufactured or coordinated: discount, avoid, or defend.

The output is a calibrated decision with an action ceiling, never a feed.

## Current First Bet To Attack

Our current hypothesis is:

> The first sub-niche to test should be indie fragrance / scent-layering /
> fragrance-adjacent body or hair mists.

Attack this hypothesis. Compare it against at least:

1. Indie fragrance / scent-layering / fragrance-adjacent body or hair mists.
2. Scalp and haircare.
3. Advanced body care.
4. SPF / sun-makeup / sunscreen-adjacent beauty.

You may add up to two stronger alternatives if current research shows a better
fit, but do not widen into generic "beauty" or trend lists.

## Decision Criteria

Score sub-niches by whether they can produce memo-grade, no-contact candidate
slots. A slot means a public, researchable brand context that appears to have:

- a US-market tractioned indie/DTC beauty or personal-care brand;
- a named founder or relevant decision owner visible in public sources;
- a plausible live 30-90 day decision in retail/channel expansion,
  launch/reposition, inventory or purchase-depth, tier/price, taste shift, or
  defend/hold against manufactured/transient demand;
- visible public demand signals across at least two effectively independent
  public venue origins;
- at least one gradeable costly-behavior signal, not just likes/views;
- enough public evidence for a manual Orca memo without private sell-through,
  CRM, panel, cohort, dashboard, or internal data;
- no obvious need for absurd-risk source access, paid data, hidden pages, or
  proprietary sources.

Use these negative filters:

- No named decision owner.
- No live allocation consequence.
- Only engagement volume or generic trend coverage.
- Signals all derive from one origin or PR event.
- The useful evidence requires proprietary/internal data.
- The category is attractive but too regulated, scientific, or claims-heavy for
  a first 2-3 month proof.
- The likely buyer would want a feed/dashboard rather than a discrete decision.

## Required Research Method

1. Start from the uploaded Orca docs. State `SOURCE_CONTEXT_READY` only after
   you have read enough to apply the buyer/product gates.
2. Use current web research. Prefer primary and high-quality sources:
   brand announcements, retailer listings, executive/founder interviews, trade
   press, reputable industry analysis, retail/search/category data, review/forum
   evidence, and credible trend reports.
3. Do not over-rely on one article or one trend report. Separate:
   category growth, consumer behavior, creator/social momentum, retail movement,
   review/forum demand, and brand/operator accessibility.
4. Treat public examples as candidate contexts, not buyers or leads.
5. Flag uncertainty. If a signal is unavailable, paywalled, derived from a
   shared PR event, or only social attention, say so.

## Required Output

Return a concise research memo with these sections:

1. **Recommendation**
   - Best first sub-niche.
   - Runner-up.
   - One sub-niche to avoid for the first pass.
   - Confidence: high / medium / low, with one sentence why.

2. **Ranked Sub-Niche Table**
   Columns:
   - sub-niche;
   - why it might fit;
   - strongest public evidence;
   - visible decision triggers;
   - likely decision owner;
   - evidence-source diversity;
   - costly-behavior visibility;
   - first-proof risks;
   - score 1-5.

3. **Candidate Slot Examples**
   For the top two sub-niches, list 3-6 public candidate contexts each.
   For each:
   - brand/context;
   - public decision trigger;
   - decision family;
   - named decision owner or public role;
   - independent venue origins visible;
   - costly-behavior evidence;
   - sources;
   - qualification status: strong / tentative / reject / needs follow-up.

4. **Attack On The Fragrance Bet**
   Explicitly say whether the current first bet survives. If it loses, explain
   what beat it. If it survives, explain the narrow version of fragrance that
   should be tested first and what fragrance-adjacent areas should be excluded.

5. **No-Contact Scan Plan**
   A 1-week no-contact research plan to validate the recommendation before any
   outreach. Include what to look for, what counts as a pass, and what would
   kill or downgrade the sub-niche.

6. **Non-Claims**
   State that the memo is not buyer validation, willingness-to-pay proof,
   outreach authorization, capture authorization, product readiness, commercial
   readiness, or a claim that Orca can support the sub-niche without a later
   proof artifact.

## Uploaded Source Pack

Read the uploaded files in this order:

1. `docs/decisions/orca_product_thesis_consumer_demand_v0.md`
2. `docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md`
3. `docs/product/product_lead/orca_offer_hypothesis_v0.md`
4. `docs/product/product_lead/orca_buyer_proof_packet_v0.md`
5. `docs/product/product_lead/orca_product_proof_lead_charter_v0.md`
6. `docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md`
7. `docs/product/product_lead/orca_demand_read_taxonomy_v0.md`
8. `docs/product/product_lead/orca_demand_read_taxonomy_adjudication_v0.md`
9. `docs/product/source_capture_toolbox/ig_creator_roster_frontier_ledger_spec_v0.md`

If you cannot read a file, name it and continue with a visible source gap.
