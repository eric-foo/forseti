# YouTube Shorts Fragrance Product-Talk Posture Pilot30 v0

```yaml
retrieval_header_version: 1
artifact_role: Review input / transcript-only product-talk posture pilot
scope: Product-talk posture labels for the hard30 YouTube Shorts fragrance fixture.
use_when:
  - Testing whether product-talk posture adds useful signal beyond rhetorical mode and commercial directness.
  - Inspecting transcript-visible product promise, objection, and recommendation frames.
authority_boundary: retrieval_only
open_next:
  - docs/review-inputs/youtube_shorts_fragrance_product_talk_posture_pilot30_v0.json
  - docs/review-inputs/youtube_shorts_fragrance_tone_fixture_hard30_v0.json
  - docs/review-inputs/youtube_shorts_fragrance_tone_labeling_run_v1.json
  - docs/review-inputs/youtube_shorts_fragrance_transcript_tone_rubric_v0.md
```

## Summary

- Generated at: `2026-06-26T19:43:59Z`
- Rows total: 30
- Rows labeled: 29
- Rows abstained: 1
- Labeler: `codex_transient_transcript_read_product_talk_posture_pilot`

This pilot asks a narrower question than generic tone: when the creator talks about a product, what transcript-visible stance and product promise frame are they using?

Transcript bodies were read transiently from the existing hard30 data-lake pointers and were not copied into this repo artifact.

## Field Contract

Pilot-only fields:

- `dominant_product_posture`: coarse stance toward the product in transcript-visible product talk.
- `recommendation_strength`: how directly the transcript pushes trial, purchase, or avoidance.
- `claim_frames`: provisional multi-label vocabulary for the product promises or objections used.
- `commercial_context`: transcript-visible commercial posture, separated from the product stance.

These fields are not a benchmark, not inter-rater validated, and not audio tone. They are a probe for whether the product-talk layer is worth expanding.

## Dominant Product Posture

| Posture | Count |
| --- | ---: |
| `critical_or_warning` | 2 |
| `positive_recommendation` | 6 |
| `qualified_or_mixed` | 5 |
| `strong_endorsement` | 16 |

## Recommendation Strength

| Strength | Count |
| --- | ---: |
| `anti_purchase_or_warning` | 2 |
| `descriptive_or_observational` | 5 |
| `explicit_purchase_or_try_cta` | 6 |
| `no_scoreable_product_talk` | 1 |
| `soft_recommendation` | 7 |
| `strong_recommendation_no_purchase_cta` | 9 |

## Commercial Context

| Context | Count |
| --- | ---: |
| `brand_sent_or_affiliate_ambiguous` | 1 |
| `creator_brand_or_affinity_ambiguous` | 1 |
| `direct_cta` | 2 |
| `explicit_sponsored_partner` | 2 |
| `metadata_ad_context_only` | 1 |
| `negative_purchase_guidance` | 2 |
| `non_commercial_update` | 1 |
| `organic_review` | 17 |
| `soft_personal_context` | 3 |

## Claim Frames

| Claim frame | Count |
| --- | ---: |
| `age_segment` | 1 |
| `artistic_positioning` | 1 |
| `availability_scarcity` | 1 |
| `brand_sent_products` | 1 |
| `collaboration_new_release` | 1 |
| `collection_ranking` | 3 |
| `collection_variant_comparison` | 1 |
| `collection_worthiness` | 1 |
| `commercial_cta` | 3 |
| `comparison_dupe_alternative` | 9 |
| `controversy_warning` | 1 |
| `creator_personal_use` | 3 |
| `event_discovery` | 1 |
| `format_convenience` | 1 |
| `identity_or_occasion` | 13 |
| `launch_or_new_release` | 1 |
| `narrative_analogy` | 1 |
| `packaging_or_format_drawback` | 1 |
| `performance_longevity_projection` | 12 |
| `price_segment` | 1 |
| `quality_positioning` | 3 |
| `routine_layering` | 2 |
| `seasonal_use_case` | 4 |
| `sensory_description` | 21 |
| `social_compliment_reaction` | 5 |
| `social_proof` | 1 |
| `sponsorship_disclosure` | 2 |
| `value_price` | 11 |

## Confidence

| Confidence | Count |
| --- | ---: |
| `high` | 19 |
| `low` | 3 |
| `medium` | 7 |

## Pilot Read

The pilot appears worth one more bounded pass because it separates product stance from video format. For example, `ranked_or_segmented_recommendation` rows split into sparse list-inclusion recommendations, age/price segment recommendations, and brand-sent buying-guide CTAs. Single-product rows split into strong endorsement, qualified/mixed review, and negative guidance.

Do not expand this as a vague tone score. If expanded, keep it as product-talk posture plus claim frames, and keep audio delivery separate.

## Non-Claims

- not buyer proof
- not a sentiment benchmark
- not inter-rater reliability
- not audio tone, energy, pace, volume, or prosody
- not creator-level generalization
- not proof that product-talk posture is worth full instrumentation
- not a claim that transcript-only labels capture sarcasm or delivery reliably

Machine-readable labels are in `docs/review-inputs/youtube_shorts_fragrance_product_talk_posture_pilot30_v0.json`.
