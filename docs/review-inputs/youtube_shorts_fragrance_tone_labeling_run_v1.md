# YouTube Shorts fragrance tone labeling run v1

```yaml
retrieval_header_version: 1
artifact_role: Review input / second-pass labeling run
scope: Second-pass transcript-only labels for the hard-30 YouTube Shorts fragrance fixture under the adjudicated rubric.
use_when:
  - Inspecting same-row label disagreement before scaling labels beyond hard-30.
  - Deciding whether the stable transcript-rhetorical fields are ready for broader labeling.
authority_boundary: retrieval_only
open_next:
  - docs/review-inputs/youtube_shorts_fragrance_tone_labeling_run_v1.json
  - docs/review-inputs/youtube_shorts_fragrance_tone_labeling_run_v0.json
  - docs/review-inputs/youtube_shorts_fragrance_transcript_tone_rubric_v0.md
  - docs/review-inputs/youtube_shorts_fragrance_tone_expansion100_capture_v0.json
```

Generated: `2026-06-26T11:07:02Z`

Input fixture: `docs\review-inputs\youtube_shorts_fragrance_tone_fixture_hard30_v0.json`
Rubric: `docs\review-inputs\youtube_shorts_fragrance_transcript_tone_rubric_v0.md`
First-pass comparison reference: `docs\review-inputs\youtube_shorts_fragrance_tone_labeling_run_v0.json`
Expansion pool context: `docs\review-inputs\youtube_shorts_fragrance_tone_expansion100_capture_v0.json`

## Scope

This is a second-pass transcript-only labeling run over the original hard-30 fixture. It compares only the two adjudicated stable fields: `primary_rhetorical_mode` and `commercial_directness`. Diagnostic fields are retained as review notes, not repeatable labels.

Important caveat: this is not a blind independent-rater result. The v0 artifact was inspected for format before this pass, so the comparison is a raw disagreement surface, not inter-rater reliability.

The 100-row pool is used as context only. This artifact does not label the additional 70 Shorts.

## Counts

- Rows labeled: 30
- Rows abstained: 0
- Rows with residual flags: 16

Primary rhetorical modes:

- `contrarian_or_comedic_critique`: 2
- `direct_product_pitch_or_cta`: 3
- `personal_or_event_story`: 3
- `ranked_or_segmented_recommendation`: 8
- `scent_of_day_or_wear_diary`: 3
- `single_product_review`: 9
- `sponsored_or_partner_demo`: 2

Commercial directness:

- `direct_pitch_or_cta`: 4
- `explicit_sponsored_or_ad`: 2
- `negative_or_anti_purchase`: 2
- `non_commercial_update`: 1
- `recommendation_or_review`: 19
- `soft_personal_or_experience`: 2

Label confidence:

- `high`: 20
- `low`: 3
- `medium`: 7

## Raw Agreement With v0

- Comparable rows: 30
- `primary_rhetorical_mode` matches: 25 / 30
- `commercial_directness` matches: 25 / 30
- Stable pair matches: 22 / 30

Mismatch rows:

| Fixture | Creator | Video | v0 Mode | v1 Mode | v0 Commercial | v1 Commercial |
| --- | --- | --- | --- | --- | --- | --- |
| `ytshorts-fragrance-tone-hard30-v0-001` | `JeremyFragrance` | `as7hye0qgYc` | `scent_of_day_or_wear_diary` | `scent_of_day_or_wear_diary` | `direct_pitch_or_cta` | `recommendation_or_review` |
| `ytshorts-fragrance-tone-hard30-v0-010` | `SchoolofScent` | `uaCSynFfPpc` | `single_product_review` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `direct_pitch_or_cta` |
| `ytshorts-fragrance-tone-hard30-v0-011` | `CurlyScents` | `MN3AI-mrPWk` | `direct_audience_persuasion` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `recommendation_or_review` |
| `ytshorts-fragrance-tone-hard30-v0-015` | `SokiLondon` | `XDscn2sgW3w` | `single_product_review` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `recommendation_or_review` |
| `ytshorts-fragrance-tone-hard30-v0-018` | `TLTGReviews` | `-V7MN2IWMpA` | `scent_of_day_or_wear_diary` | `personal_or_event_story` | `soft_personal_or_experience` | `soft_personal_or_experience` |
| `ytshorts-fragrance-tone-hard30-v0-027` | `JeremyFragrance` | `DUafgG-TLms` | `direct_product_pitch_or_cta` | `single_product_review` | `direct_pitch_or_cta` | `recommendation_or_review` |
| `ytshorts-fragrance-tone-hard30-v0-028` | `CurlyScents` | `oFSnzMS8yxA` | `direct_product_pitch_or_cta` | `direct_product_pitch_or_cta` | `explicit_sponsored_or_ad` | `direct_pitch_or_cta` |
| `ytshorts-fragrance-tone-hard30-v0-030` | `SokiLondon` | `XTgiBsIaokI` | `single_product_review` | `single_product_review` | `recommendation_or_review` | `negative_or_anti_purchase` |

## Labels

| Fixture | Creator | Video | Status | Mode | Commercial | Confidence | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ytshorts-fragrance-tone-hard30-v0-001` | `JeremyFragrance` | `as7hye0qgYc` | `labeled` | `scent_of_day_or_wear_diary` | `recommendation_or_review` | `low` | asr_derived_text, short_transcript, near_minimum_word_count |
| `ytshorts-fragrance-tone-hard30-v0-002` | `GentsScents` | `ljZ7_JHXNdw` | `labeled` | `single_product_review` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-003` | `GentsScents` | `VOGZUccarFc` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-004` | `GentsScents` | `sy-rczzFrYg` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-005` | `ThePerfumeGuy` | `rmDwkTrzNxo` | `labeled` | `single_product_review` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-006` | `ThePerfumeGuy` | `5QDcTenklxg` | `labeled` | `single_product_review` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-007` | `ThePerfumeGuy` | `hfyoVdOAYt4` | `labeled` | `single_product_review` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-008` | `SchoolofScent` | `vl-QUTwtneY` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-009` | `SchoolofScent` | `WEqUWKA4FUI` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-010` | `SchoolofScent` | `uaCSynFfPpc` | `labeled` | `ranked_or_segmented_recommendation` | `direct_pitch_or_cta` | `medium` | brand_sent_products, discount_code_cta, sponsored_ambiguity |
| `ytshorts-fragrance-tone-hard30-v0-011` | `CurlyScents` | `MN3AI-mrPWk` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `medium` | rapid_list_sparse_detail |
| `ytshorts-fragrance-tone-hard30-v0-012` | `CurlyScents` | `FqTrOZbh_DE` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `medium` | rapid_list_sparse_detail |
| `ytshorts-fragrance-tone-hard30-v0-013` | `funmimonet` | `bPJCH9iQUhI` | `labeled` | `sponsored_or_partner_demo` | `explicit_sponsored_or_ad` | `high` | sponsored_context_explicit |
| `ytshorts-fragrance-tone-hard30-v0-014` | `funmimonet` | `Uj4bVTM6dm8` | `labeled` | `personal_or_event_story` | `soft_personal_or_experience` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-015` | `SokiLondon` | `XDscn2sgW3w` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `medium` | multi_product_collection_review |
| `ytshorts-fragrance-tone-hard30-v0-016` | `SokiLondon` | `Fd-aChpt_Ss` | `labeled` | `single_product_review` | `recommendation_or_review` | `medium` | possible_creator_brand_context |
| `ytshorts-fragrance-tone-hard30-v0-017` | `TLTGReviews` | `7S40eU8FDCY` | `labeled` | `scent_of_day_or_wear_diary` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-018` | `TLTGReviews` | `-V7MN2IWMpA` | `labeled` | `personal_or_event_story` | `soft_personal_or_experience` | `medium` | fragrance_not_primary, long_personal_update |
| `ytshorts-fragrance-tone-hard30-v0-019` | `TLTGReviews` | `Ln1LUflj8d0` | `labeled` | `scent_of_day_or_wear_diary` | `recommendation_or_review` | `high` | profanity_in_auto_caption |
| `ytshorts-fragrance-tone-hard30-v0-020` | `Redolessence` | `JMmEIv_oG4o` | `labeled` | `single_product_review` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-021` | `Redolessence` | `_Gp2AmN74E8` | `labeled` | `direct_product_pitch_or_cta` | `direct_pitch_or_cta` | `high` | purchase_link_context |
| `ytshorts-fragrance-tone-hard30-v0-022` | `Redolessence` | `Tb-_V-JVNfk` | `labeled` | `single_product_review` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-023` | `TheFragranceApprentice` | `6k8ebJw50tU` | `labeled` | `personal_or_event_story` | `non_commercial_update` | `high` | not_product_review_primary |
| `ytshorts-fragrance-tone-hard30-v0-024` | `TheFragranceApprentice` | `5e4y5yNagRI` | `labeled` | `contrarian_or_comedic_critique` | `negative_or_anti_purchase` | `low` | short_transcript, comedic_context, near_minimum_word_count |
| `ytshorts-fragrance-tone-hard30-v0-025` | `TheFragranceApprentice` | `WcSRnnwSAJM` | `labeled` | `contrarian_or_comedic_critique` | `recommendation_or_review` | `high` | comedic_context |
| `ytshorts-fragrance-tone-hard30-v0-026` | `JeremyFragrance` | `doNVRDk0X_Y` | `labeled` | `direct_product_pitch_or_cta` | `direct_pitch_or_cta` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-027` | `JeremyFragrance` | `DUafgG-TLms` | `labeled` | `single_product_review` | `recommendation_or_review` | `medium` | duplicate_product_context |
| `ytshorts-fragrance-tone-hard30-v0-028` | `CurlyScents` | `oFSnzMS8yxA` | `labeled` | `direct_product_pitch_or_cta` | `direct_pitch_or_cta` | `low` | short_transcript, ad_context_in_title_non_transcript, near_minimum_word_count |
| `ytshorts-fragrance-tone-hard30-v0-029` | `funmimonet` | `zJVS5UnoHIY` | `labeled` | `sponsored_or_partner_demo` | `explicit_sponsored_or_ad` | `high` | sponsored_context_explicit |
| `ytshorts-fragrance-tone-hard30-v0-030` | `SokiLondon` | `XTgiBsIaokI` | `labeled` | `single_product_review` | `negative_or_anti_purchase` | `high` | none |

## Interpretation

- The coarse rhetorical mode mostly survives a second pass, but multi-product comparison rows are the main instability source.
- Commercial directness needs tighter treatment for transcript-visible CTAs, title-only ad markers, and negative reviews with partial price praise.
- The added 70 rows should not be labeled at scale until these disagreement cases are either adjudicated or explicitly accepted as residual ambiguity.

## Non-Claims

- not blind independent labeling
- not adjudicated labels
- not inter-rater reliability
- not benchmark validation
- not labels for the full 100-row pool
- not energy, prosody, audio, visual, comment, or engagement scoring
- diagnostic note fields are not repeatable closed labels
- full transcript bodies are not stored in this artifact

Machine-readable labels are in `docs/review-inputs/youtube_shorts_fragrance_tone_labeling_run_v1.json`.
