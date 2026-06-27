# YouTube Shorts Fragrance Tone Labeling Pool200 v0

```yaml
retrieval_header_version: 1
artifact_role: Review input / transcript-only tone labeling run
scope: Transcript-only stable-field labels and abstains for the YouTube Shorts fragrance tone pool.
use_when:
  - Inspecting transcript-only tone distributions.
  - Joining stable tone labels to the Shorts pool and creator ledger.
authority_boundary: retrieval_only
open_next:
  - docs/review-inputs/youtube_shorts_fragrance_tone_labeling_pool200_v0.json
  - docs/review-inputs/youtube_shorts_fragrance_transcript_tone_rubric_v0.md
```

## Summary

- Generated at: `2026-06-26T19:24:16Z`
- Rows total: 200
- Rows labeled: 187
- Rows abstained: 13
- Labeler: `composite_pool200_readout_existing_labels_plus_new100_rule_assisted_pass`

Stable fields only: `primary_rhetorical_mode` and `commercial_directness`. Diagnostic fields and energy/prosody remain out of scope.

## Primary Rhetorical Mode

| Mode | Count |
| --- | ---: |
| `contrarian_or_comedic_critique` | 9 |
| `direct_audience_persuasion` | 6 |
| `direct_product_pitch_or_cta` | 26 |
| `personal_or_event_story` | 15 |
| `ranked_or_segmented_recommendation` | 72 |
| `scent_of_day_or_wear_diary` | 8 |
| `single_product_review` | 49 |
| `sponsored_or_partner_demo` | 2 |

## Commercial Directness

| Commercial Directness | Count |
| --- | ---: |
| `direct_pitch_or_cta` | 38 |
| `explicit_sponsored_or_ad` | 2 |
| `negative_or_anti_purchase` | 8 |
| `non_commercial_update` | 4 |
| `recommendation_or_review` | 120 |
| `soft_personal_or_experience` | 15 |

## Confidence

| Confidence | Count |
| --- | ---: |
| `high` | 127 |
| `low` | 12 |
| `medium` | 48 |

## Residual Flags

| Flag | Count |
| --- | ---: |
| `ad_context_in_title_non_transcript` | 1 |
| `asr_derived_text` | 1 |
| `auto_caption_text` | 99 |
| `blind_reaction_format` | 1 |
| `bodybuilding_update` | 1 |
| `brand_sent_products` | 2 |
| `channel_cta` | 1 |
| `comedic_context` | 4 |
| `comedic_persona` | 1 |
| `community_cta_secondary` | 1 |
| `creator_brand_context` | 2 |
| `creator_interview` | 1 |
| `creator_own_brand` | 2 |
| `creator_product_development` | 1 |
| `cta_inside_recommendation_structure` | 9 |
| `deal_context` | 1 |
| `direct_address_inside_list_structure` | 6 |
| `discount_code_cta` | 1 |
| `duplicate_product_context` | 2 |
| `explicit_check_out_cta` | 3 |
| `fragrance_not_primary` | 2 |
| `future_drop_cta` | 1 |
| `insufficient_transcript_substance` | 3 |
| `interrupted_transcript` | 1 |
| `interview_context` | 2 |
| `layering_combo` | 1 |
| `long_personal_update` | 1 |
| `multi_product_collection_review` | 1 |
| `multi_product_list` | 1 |
| `multiple_check_out_ctas` | 1 |
| `music_or_dialogue_fragment` | 1 |
| `near_minimum_word_count` | 9 |
| `no_product_named` | 1 |
| `no_transcript_fragrance_signal` | 4 |
| `non_fragrance_dialogue_fragment` | 1 |
| `non_fragrance_transcript` | 4 |
| `not_explicit_sponsored` | 1 |
| `not_fragrance_primary` | 1 |
| `not_product_review_primary` | 5 |
| `own_brand_or_brand_affinity_ambiguous` | 1 |
| `possible_creator_brand_context` | 1 |
| `profanity_in_auto_caption` | 1 |
| `purchase_link_context` | 1 |
| `rapid_list_sparse_detail` | 2 |
| `retail_cta` | 1 |
| `retail_shop_context` | 1 |
| `sale_context` | 1 |
| `sarcasm` | 1 |
| `scarcity_context` | 1 |
| `self_promotional_context` | 1 |
| `short_transcript` | 15 |
| `skincare_primary` | 2 |
| `sponsor_ambiguity` | 2 |
| `sponsored_ambiguity` | 1 |
| `sponsored_context_explicit` | 2 |
| `stage_awards_audio` | 2 |
| `stock_level_claim` | 1 |
| `street_interview` | 1 |
| `teaser_context` | 1 |
| `unscoreable_caption_text` | 2 |
| `utility_test_not_scent_review_primary` | 1 |

## Non-Claims

- not benchmark validation
- not inter-rater reliability
- not buyer proof
- not an energy/prosody measure
- not creator-level generalization
- not a claim that every admitted row is fragrance-relevant after human review

Machine-readable labels are in `docs/review-inputs/youtube_shorts_fragrance_tone_labeling_pool200_v0.json`.
