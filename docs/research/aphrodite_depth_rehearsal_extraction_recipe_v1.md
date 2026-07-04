# Aphrodite Depth Rehearsal - Extraction Recipe v1

```yaml
retrieval_header_version: 1
artifact_role: Research record (versioned rehearsal extraction recipe for the D-1 GentsScents dress rehearsal; not a runner, storage schema, or display doctrine)
scope: >
  Defines `aphrodite-rehearsal-extraction-v1`: the hand-run claim vocabulary,
  provenance fields, abstention rules, and forbidden moves for projecting a
  single GentsScents YouTube corpus into the Aphrodite five-panel depth layer.
use_when:
  - Reading or reviewing the D-1 GentsScents rehearsal claim set.
  - Re-running the bounded hand extraction without creating a durable runner.
authority_boundary: retrieval_only
open_next:
  - docs/research/aphrodite_recipe_v1_second_opinion_adjudication_v0.md
  - docs/research/aphrodite_depth_rehearsal_d1_gentsscents_corpus_v0.md
  - forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml
stale_if:
  - A later Aphrodite extraction recipe supersedes v1.
  - The fragrance reference ontology changes the product, tier, note-family, or dupe vocabulary used here.
```

## Recipe identity

- `extraction_recipe_version`: `aphrodite-rehearsal-extraction-v1`
- `extraction_model`: `gpt-5-codex operator-run in-session`
- Bound run: GentsScents YouTube corpus, 15 videos, newest available packet per video, captured from existing raw lake records only.
- Status: hand-run rehearsal recipe. It is not an extractor build, storage schema, standing crawler, API runner, or readiness claim.

This recipe applies the accepted recipe-v1 adjudication in `docs/research/aphrodite_recipe_v1_second_opinion_adjudication_v0.md`: tier facts rendered under the local rubric may `show`; engagement support keeps raw count and `sum(like_count)` separate; the recipe emits evidence and posture, not final display copy; within-corpus baselines are allowed when the denominator and allocation are disclosed.

## Inputs

1. Existing GentsScents watch packets and caption packets in `F:/orca-data-lake/raw`, selected newest per video.
2. Existing round-2 grading and share-of-voice research records:
   - `docs/research/aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`
   - `docs/research/aphrodite_depth_rehearsal_round2_share_of_voice_v0.md`
3. Ontology reference coordinates in `forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml`.
4. The synthetic but skeptical buyer profile locked by owner choice for this fused run:
   - dupe-first or clone-house operator;
   - cares about Dior Sauvage and Creed Aventus demand adjacency;
   - skeptical by default and needs more proof before spend.

The recipe does not use new capture, roster-scale crawling, API calls, durable silver-lane mutation, buyer contact, or lake schema changes.

## Claim Types

The accepted adjudication text says the recipe has 29 claim types, while its appendix table enumerates 30 when `fit.unresolved_product_mentions` is included. This run preserves the discrepancy visibly and emits all 30 appendix rows rather than hiding the unresolved-tail requirement.

Fit panel:

| Claim type | Definition | Required reference posture |
|---|---|---|
| `fit.video_segment_share` | Share of selected videos whose subject matter is fragrance topical and relevant to buyer discovery. | Source corpus only. |
| `fit.product_segment_presence` | Product mentions and attention from the round-2 SoV pass, with low-confidence tail disclosed. | Resolved products cite ontology coordinates or downgrade. |
| `fit.presence_attention_stance` | Presence x attention x stance rows for buyer-relevant products and top corpus products. | Product IDs and tier/note coordinates when shown. |
| `fit.note_family_overlap` | Overlap between buyer target originals and creator-attended products. | Must derive from ontology `note_families`; no operator-asserted notes. |
| `fit.tier_alignment` | Tier fit against the accepted rubric. | Tier values from ontology; M1 allows `show` under the rubric. |
| `fit.dupe_direct_original_attention` | Attention to the originals the buyer cares about, independent of clone-tail inference. | Product IDs required. |
| `fit.dupe_clone_tail_attention` | Citable clone/dupe roll-up. | Withhold if ontology has no citable `dupe_relationships`. |
| `fit.comparable_brand_baseline` | Within-corpus comparable-product baseline. | Denominator and fractional allocation disclosed. |
| `fit.attention_concentration` | Whether attention is concentrated or diffuse across products. | SoV denominator required. |
| `fit.niche_share_trajectory` | Movement over capture cycles. | Requires at least two cycles; otherwise withhold. |
| `fit.unresolved_product_mentions` | Low-confidence or unresolved product/entity tail. | Required disclosure; cannot silently drop. |

Ad reception panel:

| Claim type | Definition |
|---|---|
| `ad.video_disclosure_class` | Per-corpus commercial class available from caption/watch metadata and affiliate link presence. |
| `ad.affiliate_link_inventory` | Link-bearing video count and affiliate-link inventory. |
| `ad.load_mix` | Commercial density and class mix. |
| `ad.matched_reception_pair` | Matched sponsored/affiliate vs organic comparator. |
| `ad.reception_delta` | Engagement difference by commercial class, downgraded if comparator is confounded. |
| `ad.comment_texture_by_class` | Comment texture by commercial class, with page/top-sort limitations. |

Purchase intent panel:

| Claim type | Definition |
|---|---|
| `intent.product_resolved_counts` | Product-resolved intent counts when product binding is available. |
| `intent.engagement_weighted_support` | Raw intent comment counts and `sum(like_count)` kept separate; no blended scalar. |
| `intent.aggregate_texture_unresolved` | Purchase/dupe/comparison texture that is real but not safely product-resolved. |
| `intent.sample_limitation` | Required sample limitation and denominator disclosure. |

Brand adjacency panel:

| Claim type | Definition |
|---|---|
| `adj.organic_brand_product_presence` | Organic presence of buyer-adjacent brands/products. |
| `adj.similarity_to_buyer_coordinates` | Similarity to buyer coordinates from tier and note-family reference data. |
| `adj.organic_attention_stance` | Attention and stance for unpaid adjacent content. |
| `adj.comparable_brand_baseline` | Within-corpus adjacent product baseline. |

Momentum panel:

| Claim type | Definition |
|---|---|
| `momentum.capture_window_state` | Captured-window and publish-window state. |
| `momentum.view_engagement_moving_average` | Moving average over cycles. |
| `momentum.follower_delta` | Follower movement over cycles. |
| `momentum.breakout_frequency` | Breakout frequency against prior baseline. |
| `momentum.fit_relevant_participation` | Repeated fit-relevant participation over time. |

## Provenance Fields

Every emitted claim carries:

- `source_refs`
- `extraction_model`
- `extraction_recipe_version`
- `input_content_hash`
- `extraction_timestamp`
- `receipt`
- `confidence_or_abstention`
- `provenance_state: show | downgrade | withhold`

Fit claims that render product-coordinate conclusions also carry `reference_coords` against `fragrance_reference_v0.yaml`. A missing coordinate is a defect unless the claim is explicitly withheld or downgraded because the coordinate is absent.

## Abstention Rules

- Missing evidence emits a claim with `value: null`, `provenance_state: withhold`, and a receipt naming what is missing. It is never zero-filled and never dropped.
- The empty dupe-graph text is exact:
  - `Dupe-space roll-up withheld: the ontology contains no citable dupe relationships for this capture/version. Direct original mentions are shown where available. This is not evidence of zero clone demand.`
- Single-cycle momentum claims withhold or downgrade. They cannot infer trend.
- Buyer profile assertions are synthetic intake coordinates only; they are not market proof.
- Page/top-sort comments may support texture, but not full-audience prevalence.

## Forbidden Moves

No scores; no unstamped claims; no API calls; no durable data-lake mutation; no roster-scale expansion; no buyer outreach; no new dupe graph; no FLAG-1 or commercial-use resolution; no demographic or person-level inference; no substituting same-vendor review for the D-1 cross-vendor adversarial review criterion.

## Non-Claims

- Not validation, readiness, buyer proof, or D-1 passage.
- Not a runner or build spec.
- Not a display doctrine replacement.
- Not evidence-grade for a sold report.
