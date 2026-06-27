# YouTube Shorts Fragrance Product-Talk Opinion Value Pilot30 v0

```yaml
retrieval_header_version: 1
artifact_role: Review input / product-talk opinion evidence advisory
scope: Row-level product identity, source-visible commercial signal, and independent-opinion evidence tier for the hard30 product-talk pilot.
use_when:
  - Separating organic product opinion from commercially shaped positive mentions.
  - Checking which product-talk rows deserve more weight for demand-learning review.
  - Deciding what belongs in future YouTube transcript product-mention silver rows versus Judgment-prep interpretation.
authority_boundary: retrieval_only
open_next:
  - docs/review-inputs/youtube_shorts_fragrance_product_talk_opinion_value_pilot30_v0.json
  - docs/review-inputs/youtube_shorts_fragrance_product_talk_posture_pilot30_v0.json
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_transcript_product_extraction_spec_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
```

## Summary

- Generated at: `2026-06-26T20:03:03Z`
- Rows total: 30
- Clean independent rows with non-low product identity: 18
- Commercially down-weighted rows: 9
- Negative or qualified rows: 6

This artifact accepts the owner direction: sponsored, brand-sent, direct-CTA, and creator-affinity positives are low-value for independent preference. They are not inverted; they are excluded or heavily down-weighted for the independent-opinion rollup.

## Placement

Canonical durable row data belongs in the data lake derived tree. This repo file is only a transitional review mirror/receipt for the pilot rows.

Admissible lake promotion is split:

- quote/timestamp-backed product mentions and source-visible commercial signals: `derived/<transcript-packet>/silver__cleaning__product_mentions/<id>` or a sibling Cleaning silver lane under the same raw anchor when the row is not itself a product mention
- independent-opinion evidence tier, down-weighting advice, and source-value interpretation: a bounded gold-ready/Judgment-prep assembly or consumption-time computed view with `judgment_status: not_evaluated`, not silver

Do not append this pilot table to silver as-is. It lacks full CE2/CE9 quote/timestamp admission for every row and includes interpretive opinion-value fields.

## Evidence Tiers

| Tier | Count |
| --- | ---: |
| `tier_0_not_product_evaluation` | 1 |
| `tier_1_commercial_positive_low_independent_value` | 9 |
| `tier_2_organic_positive_language` | 14 |
| `tier_3_organic_qualified_tradeoff` | 4 |
| `tier_4_negative_diagnostic` | 2 |

## Commercial Signals

| Signal | Count |
| --- | ---: |
| `brand_sent_plus_discount_or_stock_cta` | 1 |
| `creator_brand_or_affinity_ambiguous` | 2 |
| `creator_directed_product_mentioned` | 1 |
| `creator_own_brand_or_affinity_ambiguous` | 1 |
| `direct_cta_no_sponsor_observed` | 2 |
| `event_discovery_no_sponsor_observed` | 1 |
| `explicit_partner_or_sponsored_transcript` | 1 |
| `explicit_sponsored_transcript` | 1 |
| `non_commercial_update` | 1 |
| `none_observed` | 18 |
| `title_or_metadata_ad_signal_only` | 1 |

## Strong Endorsement vs Good Positive

Use this boundary:

- `strong_endorsement`: action language, superlative/top-tier language, repeated personal-use proof, or multiple concrete benefit frames with no material caveat.
- `positive_recommendation`: favorable inclusion or mild praise, but not enough action, personal proof, or concrete benefit density.
- `qualified_or_mixed`: material praise and material caveat both affect the product read.
- `critical_or_warning`: dominant guidance is negative, anti-buy, disappointment, or caution.

Practical consequence: a sparse top-10 list inclusion is usually `positive_recommendation`, not `strong_endorsement`. A direct try/buy CTA, long-term own-use proof, or best/top-tier claim pushes it into `strong_endorsement`, unless commercial contamination down-weights its independent value.

## Product Identity Residual

| Confidence | Count |
| --- | ---: |
| `high` | 25 |
| `low` | 2 |
| `medium` | 3 |

Rows with unresolved/low-confidence product identity remain useful only after entity recovery. Do not treat unknown-product negative rows as product-level evidence until the product is recovered.

## Non-Claims

- not buyer proof
- not a sponsorship truth label
- not a paid-activity, credibility, or Signal Integrity judgment
- not canonical durable data-lake row storage
- not data-lake silver output despite using silver placement language for future mechanical mentions
- not inter-rater reliability
- not creator-level generalization
- not a final weighting algorithm

Machine-readable rows are in `docs/review-inputs/youtube_shorts_fragrance_product_talk_opinion_value_pilot30_v0.json`.
