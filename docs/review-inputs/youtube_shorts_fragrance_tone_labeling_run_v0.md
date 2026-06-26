# YouTube Shorts fragrance tone labeling run v0

```yaml
retrieval_header_version: 1
artifact_role: Review input / single-pass label run
scope: First single-pass transcript-only tone labels for the hard-30 YouTube Shorts fragrance fixture.
use_when:
  - Comparing first-pass labels against the second-pass or adjudication artifacts.
  - Inspecting early label-space viability before benchmark claims.
authority_boundary: retrieval_only
open_next:
  - docs/review-inputs/youtube_shorts_fragrance_tone_labeling_run_v0.json
  - docs/review-inputs/youtube_shorts_fragrance_tone_fixture_hard30_v0.md
```

Generated: `2026-06-26T09:37:24Z`

Input fixture: `docs/review-inputs/youtube_shorts_fragrance_tone_fixture_hard30_v0.json`

This is a single-pass transcript-only labeling run. It is useful for viability, not for benchmark claims.

Revision note: top-level `primary_rhetorical_mode` is intentionally coarse; specific nuance is retained in `mode_detail`.

## Viability Read

- Label space looks separable: yes, at the coarse-mode level.
- Commercial posture is highly salient: yes.
- Recommendation/review modes dominate the fixture.
- Energy remains out of scope; it needs audio-feature capture.
- Next step before scaling: second independent label pass or prompt-based adjudication to measure disagreement.

## Counts

- Rows labeled: 30
- Rows with residual flags: 9

Primary rhetorical modes:

- `contrarian_or_comedic_critique`: 2
- `direct_audience_persuasion`: 1
- `direct_product_pitch_or_cta`: 4
- `personal_or_event_story`: 2
- `ranked_or_segmented_recommendation`: 5
- `scent_of_day_or_wear_diary`: 4
- `single_product_review`: 10
- `sponsored_or_partner_demo`: 2

Commercial directness:

- `direct_pitch_or_cta`: 4
- `explicit_sponsored_or_ad`: 3
- `negative_or_anti_purchase`: 1
- `non_commercial_update`: 1
- `recommendation_or_review`: 19
- `soft_personal_or_experience`: 2

Label confidence:

- `high`: 26
- `low`: 1
- `medium`: 3

## Labels

| Fixture | Creator | Video | Mode | Detail | Commercial | Lexical Intensity | Confidence | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ytshorts-fragrance-tone-hard30-v0-001` | JeremyFragrance | `as7hye0qgYc` | `scent_of_day_or_wear_diary` | `scent_of_day_micro_pitch` | `direct_pitch_or_cta` | `medium` | `low` | asr_derived_text, short_transcript |
| `ytshorts-fragrance-tone-hard30-v0-002` | GentsScents | `ljZ7_JHXNdw` | `single_product_review` | `budget_clone_evaluation` | `recommendation_or_review` | `high` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-003` | GentsScents | `VOGZUccarFc` | `ranked_or_segmented_recommendation` | `ranked_list_recommendation` | `recommendation_or_review` | `medium` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-004` | GentsScents | `sy-rczzFrYg` | `ranked_or_segmented_recommendation` | `category_explainer_recommendation` | `recommendation_or_review` | `medium` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-005` | ThePerfumeGuy | `rmDwkTrzNxo` | `single_product_review` | `single_product_discovery_review` | `recommendation_or_review` | `high` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-006` | ThePerfumeGuy | `5QDcTenklxg` | `single_product_review` | `sensory_single_product_review` | `recommendation_or_review` | `medium` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-007` | ThePerfumeGuy | `hfyoVdOAYt4` | `single_product_review` | `budget_classic_recommendation` | `recommendation_or_review` | `high` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-008` | SchoolofScent | `vl-QUTwtneY` | `ranked_or_segmented_recommendation` | `segmented_audience_recommendation` | `recommendation_or_review` | `medium` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-009` | SchoolofScent | `WEqUWKA4FUI` | `ranked_or_segmented_recommendation` | `price_tier_recommendation` | `recommendation_or_review` | `high` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-010` | SchoolofScent | `uaCSynFfPpc` | `single_product_review` | `comparative_replacement_review` | `recommendation_or_review` | `high` | `high` | possible_brand_seeded_context |
| `ytshorts-fragrance-tone-hard30-v0-011` | CurlyScents | `MN3AI-mrPWk` | `direct_audience_persuasion` | `social_effect_persuasion` | `recommendation_or_review` | `high` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-012` | CurlyScents | `FqTrOZbh_DE` | `ranked_or_segmented_recommendation` | `ranked_list_status_play` | `recommendation_or_review` | `high` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-013` | funmimonet | `bPJCH9iQUhI` | `sponsored_or_partner_demo` | `sponsored_routine_demo` | `explicit_sponsored_or_ad` | `high` | `high` | sponsored_context_explicit |
| `ytshorts-fragrance-tone-hard30-v0-014` | funmimonet | `Uj4bVTM6dm8` | `personal_or_event_story` | `event_travel_discovery_story` | `soft_personal_or_experience` | `medium` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-015` | SokiLondon | `XDscn2sgW3w` | `single_product_review` | `comparative_product_review` | `recommendation_or_review` | `medium` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-016` | SokiLondon | `Fd-aChpt_Ss` | `single_product_review` | `guest_single_product_review` | `recommendation_or_review` | `medium` | `medium` | none |
| `ytshorts-fragrance-tone-hard30-v0-017` | TLTGReviews | `7S40eU8FDCY` | `scent_of_day_or_wear_diary` | `scent_of_day_recommendation` | `recommendation_or_review` | `medium` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-018` | TLTGReviews | `-V7MN2IWMpA` | `scent_of_day_or_wear_diary` | `personal_scent_diary` | `soft_personal_or_experience` | `medium` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-019` | TLTGReviews | `Ln1LUflj8d0` | `scent_of_day_or_wear_diary` | `casual_wearability_review` | `recommendation_or_review` | `medium` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-020` | Redolessence | `JMmEIv_oG4o` | `single_product_review` | `luxury_single_product_review` | `recommendation_or_review` | `high` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-021` | Redolessence | `_Gp2AmN74E8` | `direct_product_pitch_or_cta` | `direct_purchase_prompt_review` | `direct_pitch_or_cta` | `high` | `high` | purchase_link_context |
| `ytshorts-fragrance-tone-hard30-v0-022` | Redolessence | `Tb-_V-JVNfk` | `single_product_review` | `sensual_single_product_review` | `recommendation_or_review` | `high` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-023` | TheFragranceApprentice | `6k8ebJw50tU` | `personal_or_event_story` | `personal_channel_update` | `non_commercial_update` | `medium` | `high` | not_product_review_primary |
| `ytshorts-fragrance-tone-hard30-v0-024` | TheFragranceApprentice | `5e4y5yNagRI` | `contrarian_or_comedic_critique` | `contrarian_comedy_warning` | `negative_or_anti_purchase` | `high` | `medium` | short_transcript, comedic_context |
| `ytshorts-fragrance-tone-hard30-v0-025` | TheFragranceApprentice | `WcSRnnwSAJM` | `contrarian_or_comedic_critique` | `absurdist_negative_review` | `recommendation_or_review` | `high` | `high` | comedic_context |
| `ytshorts-fragrance-tone-hard30-v0-026` | JeremyFragrance | `doNVRDk0X_Y` | `direct_product_pitch_or_cta` | `direct_product_demo_pitch` | `direct_pitch_or_cta` | `medium` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-027` | JeremyFragrance | `DUafgG-TLms` | `direct_product_pitch_or_cta` | `direct_product_demo_testimonial` | `direct_pitch_or_cta` | `high` | `high` | none |
| `ytshorts-fragrance-tone-hard30-v0-028` | CurlyScents | `oFSnzMS8yxA` | `direct_product_pitch_or_cta` | `compact_ad_style_product_pitch` | `explicit_sponsored_or_ad` | `high` | `medium` | short_transcript, ad_context_in_title |
| `ytshorts-fragrance-tone-hard30-v0-029` | funmimonet | `zJVS5UnoHIY` | `sponsored_or_partner_demo` | `sponsored_product_family_demo` | `explicit_sponsored_or_ad` | `high` | `high` | sponsored_context_explicit |
| `ytshorts-fragrance-tone-hard30-v0-030` | SokiLondon | `XTgiBsIaokI` | `single_product_review` | `critical_comparative_review` | `recommendation_or_review` | `medium` | `high` | none |

## Non-Claims

- Not adjudicated labels.
- Not benchmark validation.
- Not inter-rater reliability.
- Not energy/prosody/audio scoring.
- Not visual, comment, or engagement scoring.
- Full transcript bodies are not stored in this artifact.

Machine-readable labels are in `docs/review-inputs/youtube_shorts_fragrance_tone_labeling_run_v0.json`.
