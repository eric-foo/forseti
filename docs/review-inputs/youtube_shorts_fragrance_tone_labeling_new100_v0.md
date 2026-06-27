# YouTube Shorts Fragrance Tone Labeling New100 v0

```yaml
retrieval_header_version: 1
artifact_role: Review input / transcript-only tone labeling run
scope: Transcript-only stable-field labels and abstains for the YouTube Shorts fragrance tone pool.
use_when:
  - Inspecting transcript-only tone distributions.
  - Joining stable tone labels to the Shorts pool and creator ledger.
authority_boundary: retrieval_only
open_next:
  - docs/review-inputs/youtube_shorts_fragrance_tone_labeling_new100_v0.json
  - docs/review-inputs/youtube_shorts_fragrance_transcript_tone_rubric_v0.md
```

## Summary

- Generated at: `2026-06-26T19:24:16Z`
- Rows total: 100
- Rows labeled: 94
- Rows abstained: 6
- Labeler: `codex_rule_assisted_transcript_only_labeling_pass`

Stable fields only: `primary_rhetorical_mode` and `commercial_directness`. Diagnostic fields and energy/prosody remain out of scope.

## Primary Rhetorical Mode

| Mode | Count |
| --- | ---: |
| `contrarian_or_comedic_critique` | 4 |
| `direct_audience_persuasion` | 5 |
| `direct_product_pitch_or_cta` | 11 |
| `personal_or_event_story` | 7 |
| `ranked_or_segmented_recommendation` | 42 |
| `scent_of_day_or_wear_diary` | 2 |
| `single_product_review` | 23 |

## Commercial Directness

| Commercial Directness | Count |
| --- | ---: |
| `direct_pitch_or_cta` | 20 |
| `negative_or_anti_purchase` | 4 |
| `recommendation_or_review` | 61 |
| `soft_personal_or_experience` | 9 |

## Confidence

| Confidence | Count |
| --- | ---: |
| `high` | 67 |
| `low` | 7 |
| `medium` | 20 |

## Residual Flags

| Flag | Count |
| --- | ---: |
| `auto_caption_text` | 99 |
| `cta_inside_recommendation_structure` | 9 |
| `direct_address_inside_list_structure` | 6 |
| `insufficient_transcript_substance` | 2 |
| `near_minimum_word_count` | 3 |
| `no_transcript_fragrance_signal` | 4 |
| `short_transcript` | 3 |

## Non-Claims

- not benchmark validation
- not inter-rater reliability
- not buyer proof
- not an energy/prosody measure
- not creator-level generalization
- not a claim that every admitted row is fragrance-relevant after human review

Machine-readable labels are in `docs/review-inputs/youtube_shorts_fragrance_tone_labeling_new100_v0.json`.
