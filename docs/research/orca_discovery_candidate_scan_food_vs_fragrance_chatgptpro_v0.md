# Orca Discovery Candidate Scan - Food vs Fragrance ChatGPT Pro Intake v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: >
  Advisory intake of a ChatGPT Pro web-research response comparing food /
  creator-led CPG snacks against the current fragrance opening for Orca's
  consumer-demand first proof lane.
use_when:
  - Reviewing the external ChatGPT Pro food-vs-fragrance recommendation before
    deciding the next no-contact verification scan.
  - Checking why fragrance remains the recommended first scan despite food's
    larger category size.
  - Separating Feastables-like category pattern evidence from buyer proof,
    outreach authorization, capture authorization, or final category selection.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/product-planning/chatgptpro_consumer_category_food_vs_fragrance_prompt_v0.md
  - docs/research/orca_discovery_candidate_scan_beauty_neutral_chatgptpro_v0.md
  - docs/research/orca_discovery_candidate_scan_beauty_subniche_chatgptpro_v0.md
  - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
  - orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
  - .agents/workflow-overlay/product-proof.md
stale_if:
  - A verified no-contact fragrance scan supersedes this advisory intake.
  - A verified food-category scan produces stronger source-visible candidate
    slots than the advisory answer found.
  - The buyer-proof gate, first commercial target, or current fragrance advisory
    intake changes.
```

## Status

Status: `ADVISORY_EXTERNAL_RESEARCH_INTAKE_FOOD_VS_FRAGRANCE_V0`.

This artifact preserves the owner's pasted ChatGPT Pro answer as decision
preparation only. It is not an independent Codex web verification pass, not
buyer proof, not outreach authorization, not capture authorization, not product
readiness, not commercial readiness, and not a filled target-slot instrument.

Source attachment:

`C:\Users\vmon7\.codex\attachments\f0b6bc9a-52ec-495e-8442-ade776b0c246\pasted-text.txt`

Claim cap: `product_learning` / advisory intake only. Every ranking, score,
candidate context, external market number, and source citation below remains
`not_verified_by_orca` until direct no-contact source checks confirm the public
evidence, named operator, live decision trigger, costly-behavior floor, and
origination independence.

## Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom attachment intake + existing food-vs-fragrance prompt + product-proof/buyer-proof context
  edit_permission: docs-write
  target_scope: create one clean ChatGPT Pro advisory intake under docs/research/; no product doctrine change
  dirty_state_checked: yes
  blocked_if_missing: clean continuation worktree, pasted ChatGPT Pro answer, prompt artifact, proof-boundary sources
```

## Prompt-Fit Check

The attached answer appears fit for advisory intake:

- It answers the filed prompt's decision question directly.
- It decomposes both food and fragrance before scoring.
- It treats Feastables as a pattern test, not as proof or a selected target.
- It returns the required recommendation, ranking table, Feastables pattern
  test, fragrance stress test, candidate contexts, no-contact scan plan, final
  next action, and non-claims.
- It preserves the core non-claims: not buyer validation, not
  willingness-to-pay proof, not outreach authorization, not capture
  authorization, not product readiness, and not commercial readiness.

Important caveat: the answer's external sources and scores have not been
independently verified in this Codex lane. Use the answer as verification
ordering, not as source-truth.

## External Recommendation Captured

Treat this as the working next scan direction:

**Run fragrance no-contact scan first.**

Confidence from the answer: `medium`.

The answer's blunt read: the Feastables instinct is useful as a pattern test
but wrong as a category-selection shortcut. Feastables demonstrates a visible
creator-led demand pattern, but its audience, content engine, giveaway loop,
retailer leverage, and scale are not reusable Orca assumptions. Food is larger
but often pushes the decision into retailer velocity, trade spend, margin,
production, freshness, taste, claims, or supply-chain data. Fragrance is
narrower but cleaner for public-first decision memos.

## Advisory Ranking Captured

| Rank | Category | Opening | Score | Intake interpretation |
| ---: | --- | --- | ---: | --- |
| 1 | Fragrance | Minis, discovery sets, and travel formats | 88 | Strongest first verification target; maps cleanly to sample-to-full-size, travel assortment, price ladder, retail-depth, and launch-depth decisions. |
| 2 | Fragrance | Layering systems, body mists, and hair mists | 86 | Strong adjacent target; repeatable format-extension and lower-price-entry decisions. |
| 3 | Food | Better-for-you, protein, and functional snacks | 78 | Best food option, but still materially dragged by private data, retailer velocity, manufacturing, sensory, and claims questions. |
| 4 | Fragrance | Broad indie/DTC fine fragrance | 76 | Useful only when narrowed to a live format, launch, or retailer allocation decision. |
| 5 | Food | Premium chocolate and confectionery challengers | 71 | Visible launches, but pricing, commodity inputs, retailer economics, and creator reach often dominate. |
| 6 | Food | Functional beverages, hydration, and energy | 69 | Dense candidate space, but efficacy, formulation, distribution economics, and repeat-purchase data drag public-first conclusions. |
| 7 | Food | Creator-led snacks and confectionery | 65 | Visible triggers, but often one-origin hype or creator dependency. |
| 8 | Food | Limited-drop, fandom, and collaboration foods | 60 | Strong launch windows, weak repeatability, high novelty distortion. |
| 9 | Food | Ingestible beauty, gummies, and functional nutrition | 54 | Heavy claims/regulatory and formulation drag. |

Deep-thinking judgment: do not read the score gap as "food is bad." Read it as
"food is not yet the first public-signal proof lane unless a named food
sub-wedge clears a much higher no-contact bar."

## Feastables Pattern Test

The reusable pattern, if any:

- concentrated attention can create trial;
- trial can leave public traces through retailer reviews, sellouts, restocks,
  retail expansion, and competitive response;
- operators then face SKU, format, door-count, inventory-depth, or retail-depth
  allocation decisions.

The non-reusable parts:

- MrBeast's audience;
- the content engine and giveaway loop;
- unusual retailer leverage;
- scale;
- the possibility that the creator campaign, audience, launch traffic, and
  brand PR are one underlying demand origin.

Advisory conclusion: a Feastables-like food read can often support `monitor` or
`probe`, but a public-only memo will likely struggle to support `commit` or
`scale` without sell-through, trade-spend, margin, production-capacity, and
ingredient/supply evidence.

## Candidate Context Queue

All contexts below are `not_verified_by_orca`. They are a verification queue,
not target slots, buyers, leads, or proof.

### Fragrance

| Context | Advisory status | Verify next |
| --- | --- | --- |
| DedCool - Milk franchise / Mineral Milk | strong | Confirm operator visibility, current format-extension decision, Sephora sell-through claim, Fragrantica/community independence, and whether sources collapse to one launch chain. |
| Snif - discovery, minis, and layering bundles | tentative | Audit Ulta reviews, DTC sold-out sample set, review incentives/syndication, and whether bundle/mini decisions are live. |
| Ellis Brooklyn - body mists / Amika collaboration | tentative | Confirm current collaboration or mist allocation trigger; separate brand-sourced sellout claims from independent consumer/retailer origins. |
| NOYZ - MYLK, solids, mists, and discovery | tentative | Verify Ulta concentration, influencer seeding, operator visibility, and format-depth decision. |
| Phlur - international Sephora expansion | reject for first proof / benchmark | Too scaled / acquired for the first proof target; useful as benchmark only. |

### Food

| Context | Advisory status | Verify next |
| --- | --- | --- |
| WILDE - protein crackers | tentative | Visible format and Target rollout, but verify whether new-format demand is public enough and not dominated by manufacturing capacity. |
| Mid-Day Squares - No Bread PB&J | tentative | Specific format at Target, but refrigerated logistics, production, taste, and modest new-format review evidence are drag. |
| JOYRIDE - Fruit Chews and Zips | tentative | Real retail expansion, but creator dependency and functional/ingredient claims remain material. |
| BelliWelli - fiber powder and gummies | reject | Viral causal chain plus claims drag and weak independent origination. |
| ALOHA - protein bars | reject for first proof | Too scaled and dependent on internal retail economics. |

The answer found five visible food contexts, but no food context that clearly
clears the strong public-first bar.

## Fragrance Stress Test

Fragrance should lose if a no-contact scan finds:

- fewer than 8-12 qualified contexts after origin deduplication;
- fewer than four strong contexts;
- no named operators or 30-90-day triggers;
- retailer reviews are mostly incentivized, syndicated, or weakly
  decision-relevant;
- recommendations repeatedly require private sell-through, COGS, or sensory
  research.

Food should beat fragrance only if one food sub-wedge yields:

- at least ten qualified contexts;
- at least four strong contexts;
- at least five live allocation triggers;
- two independent public origins plus costly behavior per strong context;
- no majority dependency on creator traffic, claims, retailer velocity,
  manufacturing, supply chain, or margin data.

Current advisory verdict: **fragrance is smaller but cleaner**.

## Recommended Next Step

Run a fragrance-only no-contact verification scan first, with food retained as
a holdout comparator rather than a parallel workstream.

Suggested scan target:

**Fragrance minis / discovery / travel formats plus layering / body-mist /
hair-mist format-extension decisions.**

Pass signal:

- 8-12 qualified fragrance contexts;
- at least four strong contexts;
- at least three mock memos that produce a concrete action beyond generic
  monitoring.

Downgrade or kill signal:

- best contexts collapse into PR, incentivized reviews, or creator/social
  engagement;
- live decisions are absent;
- most answers require private sell-through, COGS, or sensory research.

Food revisit trigger:

- a named food sub-wedge clears at least ten qualified contexts and four strong
  cases without most cases depending on creators, claims, retailer velocity,
  production, supply chain, or margins.

## Non-Claims

This intake does not claim:

- buyer validation;
- buyer proof;
- willingness-to-pay proof;
- product readiness;
- feature readiness;
- implementation readiness;
- commercial readiness;
- outreach authorization;
- capture authorization;
- final category selection;
- that any listed context is a qualified buyer, lead, or filled target slot.

Next authorized action: run the bounded fragrance no-contact verification scan
before selecting fragrance as a proof target or reopening food as a parallel
category screen.
