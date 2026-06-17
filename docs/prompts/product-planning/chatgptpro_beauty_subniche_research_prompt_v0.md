# ChatGPT Pro Beauty Sub-Niche Research Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Product planning prompt artifact
scope: >
  Portable prompt and source pack manifest for asking ChatGPT Pro to research
  which beauty/personal-care niche or sub-niche Orca should open first for the
  consumer-demand operator wedge.
use_when:
  - Commissioning external web research on Orca's first beauty niche or sub-niche.
  - Comparing skincare, fragrance, hair/scalp, makeup, body care, SPF/sun-makeup,
    and any stronger surfaced alternatives against Orca's buyer-proof gates.
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
  - A completed niche/sub-niche scan supersedes this prompt's evaluated scope or
    scoring method.
```

## Operator Context

You are helping Orca choose the first beauty/personal-care niche or sub-niche
to open. Use the uploaded source documents as Orca's internal constraints, then
use current public web research to evaluate the market. Cite every load-bearing
external claim with a URL and publication date when available.

This is **research and decision preparation only**. Do not contact brands,
scrape behind logins, recommend outreach copy, propose paid data acquisition,
or treat candidate companies as leads. Do not claim buyer validation,
willingness to pay, product readiness, or commercial readiness.

## Orca Buyer And Product Frame

Orca's current first commercial target is:

> US-market tractioned indie/DTC beauty or personal-care operators with a named
> founder, head of brand, growth, insights, strategy, or equivalent decision
> owner facing a live 30-90 day consumer-demand allocation decision where
> internal data is not conclusive and public creator/social/review/search/retail
> evidence includes at least one gradeable costly-behavior instance in a
> qualifying demand-origin family. Two or more effectively independent origins
> are required for material or irreversible recommendations; one clean origin
> caps the action ceiling at hold / low-commitment.

Orca's product promise for this first proof is not "trend reports" or social
listening. Orca should produce a decision memo/evidence appendix, and later an
executive decision deck only if proof gates pass, that helps the operator decide
whether demand is:

- durable: commit;
- real but transient: move in-window / time-box;
- manufactured or coordinated: discount, avoid, or defend.

The output is a calibrated decision with an action ceiling, never a feed.

## Neutral Niche Exploration

Start from a neutral prior. Do not treat any parent niche or sub-niche as
pre-selected, incumbent, default, runner-up, or category to defend. The task is
to rank the best first opening for Orca from evidence and fit, not to confirm or
reject a pre-existing category answer.

Explore parent niches and their sub-niches before scoring anything. Do not score
"skincare," "makeup," "fragrance," "body care," "hair/scalp," or "SPF" as a
whole until you have broken each into the most relevant sub-niches and judged
whether those sub-niche pockets can produce Orca-qualified candidate slots.

Evaluate at least these parent niches and likely sub-niche families:

1. Skincare, including barrier-first / clinical-masstige skincare,
   acne/blemish-adjacent non-medical routines, gentle derm-developed routines,
   K-beauty US breakout skincare, and other visibly stronger sub-niches you find.
2. Fragrance, including indie fragrance, scent-layering, body/hair mists,
   discovery/travel formats, skin scents, milk/gourmand shifts, and scent-family
   extensions.
3. Hair and scalp, including scalp-as-skincare, hair-wellness routines, hard
   water/buildup, textured-hair prestige, and non-medical treatment formats.
4. Makeup, including skinification of makeup, complexion/base, lip, blush,
   hybrid SPF/makeup only where the decision can be market-demand-led, and any
   stronger sub-niche you find.
5. Body care, including advanced body care, deodorant/body fragrance crossover,
   body acne/texture routines, and body mists.
6. SPF / sun-care / sunscreen-adjacent beauty.

You may add up to two stronger alternatives if current research shows a better
fit, but do not widen into generic "beauty" or trend lists.

Neutrality requirements:

- Do not use pass/fail framing for one special category.
- Do not give any parent niche a special attack section.
- Do not anchor on prior answers, prior rankings, or any uploaded research memo
  unless the user explicitly supplies one as evidence for this run.
- If a category wins, explain why it beat the other scored options under the
  rubric. If a category loses, explain the decision-relevant weakness without
  treating that loss as a reversal from a prior answer.

## Decision Criteria

Score sub-niches by whether they can produce memo-grade, no-contact candidate
slots. Parent niches should be rolled up only after their sub-niches are scored.
A slot means a public, researchable brand context that appears to have:

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

Use this 100-point rubric for every sub-niche:

| Criterion | Weight | What to score |
| --- | ---: | --- |
| Candidate-slot density | 25 | How many plausible no-contact candidate contexts can be found; more is better, do not impose a fixed minimum. |
| Public signal quality | 25 | Independent, source-visible, non-PR-derived signals usable for a manual memo. |
| Live decision pressure | 20 | Visible 30-90 day allocation decisions. |
| Costly-behavior visibility | 15 | Sellouts, waitlists, review depth, restocks, repeat purchase, retail expansion, switching/dupe behavior, or other buyer action. |
| Named operator visibility | 10 | Publicly identifiable founders/operators/decision owners. |
| Repeatability | 5 | Multiple brands face the same kind of decision pattern. |

Use these hard reject filters:

- No named decision owner.
- No live allocation consequence.
- Only engagement volume or generic trend coverage.
- Signals all derive from one origin or PR event.
- The useful evidence requires proprietary/internal data.
- Useful evidence requires absurd-risk source access, paid data, hidden pages,
  or a per-candidate route expansion.

Use these penalty flags rather than automatic rejections:

- `claims_drag`: penalize only when the candidate decision depends on clinical,
  regulatory, efficacy, or compliance proof rather than market-demand evidence.
- `private_data_dependency`: penalize when public evidence may not be enough
  without sell-through, CRM, cohort, panel, or other internal data.
- `feed_or_dashboard_pull`: penalize when the likely first buyer need is
  continuous monitoring instead of a discrete decision memo/deck.
- `one_origin_hype`: penalize when public signal mostly traces to one PR,
  creator, launch, or trade story.
- `operator_not_visible`: severe penalty or reject if no real operator can be
  identified.

## Roster Coverage Lens

Orca's current beauty creator roster path plans toward 1,000 creator accounts.
Use that only as a coverage lens, not as proof or capture authorization.

For each top parent niche, say whether a 1,000-account creator/source roster
could plausibly cover the whole niche across meaningful sub-niches, or whether
the niche is too broad and should be opened through one or two tighter
sub-niche wedges first. A good answer should distinguish:

- whole-niche coverage at scout/heartbeat level;
- deeper monitoring for the top sub-niche pockets;
- whether 1,000 accounts is likely enough for breadth, depth, or both.

## Required Research Method

1. Start from the uploaded Orca docs. State `SOURCE_CONTEXT_READY` only after
   you have read enough to apply the buyer/product gates.
2. Use current web research. Prefer primary and high-quality sources:
   brand announcements, retailer listings, executive/founder interviews, trade
   press, reputable industry analysis, retail/search/category data, review/forum
   evidence, and credible trend reports.
3. Decompose parent niches into sub-niches before scoring. If a parent niche
   wins, explain which sub-niche pockets made it win.
4. Do not over-rely on one article or one trend report. Separate:
   category growth, consumer behavior, creator/social momentum, retail movement,
   review/forum demand, and brand/operator accessibility.
5. Treat public examples as candidate contexts, not buyers or leads.
6. Flag uncertainty. If a signal is unavailable, paywalled, derived from a
   shared PR event, or only social attention, say so.

## Required Output

Return a concise research memo with these sections:

1. **Recommendation**
   - Top 3 openings for Orca, naming parent niche plus the specific sub-niche
     wedge to open first.
   - Runner-up parent niche or sub-niche.
   - One niche/sub-niche to avoid for the first pass.
   - Confidence: high / medium / low, with one sentence why.

2. **Parent Niche Decomposition**
   For each evaluated parent niche, list the main sub-niches you considered,
   which ones were scored, and which were dropped before scoring with the reason.

3. **Ranked Sub-Niche Table**
   Columns:
   - parent niche;
   - sub-niche;
   - candidate-slot density score /25;
   - public signal quality score /25;
   - live decision pressure score /20;
   - costly-behavior visibility score /15;
   - named operator visibility score /10;
   - repeatability score /5;
   - total score /100;
   - penalty flags;
   - short rationale.

4. **Top 3 Opening Rationale**
   For each of the top 3, explain whether the parent niche should be opened as
   a whole niche or through a tighter sub-niche wedge first. Include the 1,000
   account roster coverage lens: breadth, depth, or both.

5. **Candidate Slot Examples**
   For the top three openings, list the strongest public candidate contexts.
   More is better; do not stop at a minimum if strong contexts are available.
   For each:
   - brand/context;
   - public decision trigger;
   - decision family;
   - named decision owner or public role;
   - independent venue origins visible;
   - costly-behavior evidence;
   - sources;
   - qualification status: strong / tentative / reject / needs follow-up.

6. **Neutral Stress Test**
   Stress-test the top-ranked opening against the next two strongest
   alternatives. Explain what evidence would make the winner lose, what would
   make each runner-up win, and which public-signal gaps are most likely to
   change the ranking. Do not frame this as defending or attacking any prior
   category bet.

7. **No-Contact Scan Plan**
   A 1-week no-contact research plan to validate the recommendation before any
   outreach. Include what to look for, what counts as a pass, and what would
   kill or downgrade the niche or sub-niche.

8. **Non-Claims**
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
