# YouTube Shorts fragrance tone labeling remaining70 v0

```yaml
retrieval_header_version: 1
artifact_role: Review input / remaining-pool labeling run
scope: Transcript-only labels for the 70 non-hard30 YouTube Shorts rows under the patched rubric.
use_when:
  - Inspecting labels for the expansion30 and expansion100 rows.
  - Checking abstains before deciding whether capture admission needs tightening.
  - Joining remaining-pool labels back to the 100-row Shorts pool.
authority_boundary: retrieval_only
open_next:
  - docs/review-inputs/youtube_shorts_fragrance_tone_labeling_remaining70_v0.json
  - docs/review-outputs/youtube_shorts_fragrance_tone_label_adjudication_v0.md
  - docs/review-inputs/youtube_shorts_fragrance_transcript_tone_rubric_v0.md
```

Generated: `2026-06-26T18:34:11Z`

## Scope

This labels the 70 non-hard30 rows only: the 30-row expansion capture plus the 40-row expansion-to-100 capture. The hard-30 labels remain governed by the v0/v1 comparison and adjudication artifacts.

Stable fields: `primary_rhetorical_mode` and `commercial_directness`. Diagnostic fields remain provisional notes.

## Counts

- Rows total: 70
- Rows labeled: 63
- Rows abstained: 7

Primary rhetorical modes, labeled rows only:

- `contrarian_or_comedic_critique`: 3
- `direct_audience_persuasion`: 1
- `direct_product_pitch_or_cta`: 12
- `personal_or_event_story`: 5
- `ranked_or_segmented_recommendation`: 22
- `scent_of_day_or_wear_diary`: 3
- `single_product_review`: 17

Commercial directness, labeled rows only:

- `direct_pitch_or_cta`: 14
- `negative_or_anti_purchase`: 2
- `non_commercial_update`: 3
- `recommendation_or_review`: 40
- `soft_personal_or_experience`: 4

Label confidence, labeled rows only:

- `high`: 40
- `low`: 2
- `medium`: 21

## Abstains

The abstains are not silent drops. They identify transcript/capture rows where a transcript-only fragrance tone label would be a guess.

| Source Row | Creator | Video | Reason Flags |
| --- | --- | --- | --- |
| `ytshorts-fragrance-tone-expansion30-v0-011` | `TLTGReviews` | `rnJjtCdMZyo` | non_fragrance_transcript, stage_awards_audio |
| `ytshorts-fragrance-tone-expansion30-v0-026` | `TLTGReviews` | `wBzGGKsOdyY` | non_fragrance_transcript, bodybuilding_update |
| `ytshorts-fragrance-tone-expansion100-v0-007` | `TLTGReviews` | `zHTuK2_Ouf0` | non_fragrance_transcript, stage_awards_audio, near_minimum_word_count |
| `ytshorts-fragrance-tone-expansion100-v0-015` | `Scentbird` | `m3Tnv4p7TAg` | unscoreable_caption_text, music_or_dialogue_fragment, near_minimum_word_count |
| `ytshorts-fragrance-tone-expansion100-v0-026` | `funmimonet` | `ieDgm6dPS3s` | non_fragrance_transcript, skincare_primary |
| `ytshorts-fragrance-tone-expansion100-v0-035` | `Scentbird` | `hy443hJNeu8` | unscoreable_caption_text, non_fragrance_dialogue_fragment, near_minimum_word_count |
| `ytshorts-fragrance-tone-expansion100-v0-040` | `TheScentinel` | `fDtI1QsNNqY` | insufficient_transcript_substance, short_transcript, no_product_named |

## Labels

| Source Row | Creator | Video | Status | Mode | Commercial | Confidence | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ytshorts-fragrance-tone-expansion30-v0-001` | `ChaosFragrances` | `xZ6vd9fyBbw` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | multi_product_list |
| `ytshorts-fragrance-tone-expansion30-v0-002` | `FragranceKnowledge` | `xK8bmugSpgQ` | `labeled` | `single_product_review` | `recommendation_or_review` | `medium` | utility_test_not_scent_review_primary |
| `ytshorts-fragrance-tone-expansion30-v0-003` | `ProfessorPerfume` | `vtwo-iaOszA` | `labeled` | `scent_of_day_or_wear_diary` | `recommendation_or_review` | `medium` | layering_combo |
| `ytshorts-fragrance-tone-expansion30-v0-004` | `JeremyFragrance` | `JcwT5rvhXIc` | `labeled` | `direct_product_pitch_or_cta` | `direct_pitch_or_cta` | `high` | own_brand_or_brand_affinity_ambiguous, explicit_check_out_cta |
| `ytshorts-fragrance-tone-expansion30-v0-005` | `GentsScents` | `jo03W7cBwBM` | `labeled` | `single_product_review` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion30-v0-006` | `ThePerfumeGuy` | `17mhHUkRLvg` | `labeled` | `single_product_review` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion30-v0-007` | `SchoolofScent` | `1K9ej-6aP6g` | `labeled` | `direct_audience_persuasion` | `direct_pitch_or_cta` | `medium` | creator_product_development, future_drop_cta |
| `ytshorts-fragrance-tone-expansion30-v0-008` | `CurlyScents` | `ekaQONEC2ys` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion30-v0-009` | `funmimonet` | `DIMlwC1LsHg` | `labeled` | `direct_product_pitch_or_cta` | `direct_pitch_or_cta` | `medium` | sponsor_ambiguity, teaser_context, not_explicit_sponsored |
| `ytshorts-fragrance-tone-expansion30-v0-010` | `SokiLondon` | `frHbes9NwZI` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion30-v0-011` | `TLTGReviews` | `rnJjtCdMZyo` | `abstain` | `none` | `none` | `none` | non_fragrance_transcript, stage_awards_audio |
| `ytshorts-fragrance-tone-expansion30-v0-012` | `Redolessence` | `I_IBUdYJQ6U` | `labeled` | `personal_or_event_story` | `soft_personal_or_experience` | `medium` | interview_context, not_product_review_primary |
| `ytshorts-fragrance-tone-expansion30-v0-013` | `TheFragranceApprentice` | `EPcHN1WaGBY` | `labeled` | `contrarian_or_comedic_critique` | `non_commercial_update` | `medium` | comedic_persona, not_product_review_primary |
| `ytshorts-fragrance-tone-expansion30-v0-014` | `ChaosFragrances` | `54Ue3UL7XU4` | `labeled` | `single_product_review` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion30-v0-015` | `FragranceKnowledge` | `weBLSbBqBbs` | `labeled` | `direct_product_pitch_or_cta` | `direct_pitch_or_cta` | `high` | sale_context, stock_level_claim |
| `ytshorts-fragrance-tone-expansion30-v0-016` | `BowTieFragranceGuy` | `hiAWZwgYwQA` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | channel_cta |
| `ytshorts-fragrance-tone-expansion30-v0-017` | `MilaLeBlanc` | `WLjJ0J4QFBo` | `labeled` | `single_product_review` | `recommendation_or_review` | `medium` | short_transcript |
| `ytshorts-fragrance-tone-expansion30-v0-018` | `ThePerfumeNest` | `vDvnnG2iaGQ` | `labeled` | `ranked_or_segmented_recommendation` | `negative_or_anti_purchase` | `high` | none |
| `ytshorts-fragrance-tone-expansion30-v0-019` | `JeremyFragrance` | `tQ0RKdd1o9g` | `labeled` | `single_product_review` | `recommendation_or_review` | `medium` | duplicate_product_context |
| `ytshorts-fragrance-tone-expansion30-v0-020` | `GentsScents` | `KorM3KkSUrs` | `labeled` | `single_product_review` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion30-v0-021` | `ThePerfumeGuy` | `BhA4y28lmt0` | `labeled` | `direct_product_pitch_or_cta` | `direct_pitch_or_cta` | `high` | scarcity_context |
| `ytshorts-fragrance-tone-expansion30-v0-022` | `SchoolofScent` | `cc7MLqJl9SY` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `medium` | interview_context, blind_reaction_format |
| `ytshorts-fragrance-tone-expansion30-v0-023` | `CurlyScents` | `vLiFRCQhV0s` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion30-v0-024` | `funmimonet` | `GcAIds8HW38` | `labeled` | `direct_product_pitch_or_cta` | `direct_pitch_or_cta` | `high` | retail_cta |
| `ytshorts-fragrance-tone-expansion30-v0-025` | `SokiLondon` | `3Abc0p30r9c` | `labeled` | `single_product_review` | `recommendation_or_review` | `medium` | creator_brand_context |
| `ytshorts-fragrance-tone-expansion30-v0-026` | `TLTGReviews` | `wBzGGKsOdyY` | `abstain` | `none` | `none` | `none` | non_fragrance_transcript, bodybuilding_update |
| `ytshorts-fragrance-tone-expansion30-v0-027` | `Redolessence` | `Az4cCq5L0NE` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion30-v0-028` | `TheFragranceApprentice` | `YWnj7wFOqO0` | `labeled` | `personal_or_event_story` | `non_commercial_update` | `high` | not_product_review_primary |
| `ytshorts-fragrance-tone-expansion30-v0-029` | `MilaLeBlanc` | `hwRSgl1RUL8` | `labeled` | `single_product_review` | `recommendation_or_review` | `medium` | short_transcript |
| `ytshorts-fragrance-tone-expansion30-v0-030` | `ThePerfumeNest` | `W3HTpUsaHiA` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion100-v0-001` | `JeremyFragrance` | `syjxpoKWbRM` | `labeled` | `direct_product_pitch_or_cta` | `direct_pitch_or_cta` | `medium` | creator_own_brand, self_promotional_context |
| `ytshorts-fragrance-tone-expansion100-v0-002` | `GentsScents` | `sNQKEWZ6rTM` | `labeled` | `single_product_review` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion100-v0-003` | `ThePerfumeGuy` | `ESyg9QXm8MU` | `labeled` | `direct_product_pitch_or_cta` | `direct_pitch_or_cta` | `high` | explicit_check_out_cta |
| `ytshorts-fragrance-tone-expansion100-v0-004` | `SchoolofScent` | `ZVU5kePvD2w` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `medium` | brand_sent_products, sponsor_ambiguity |
| `ytshorts-fragrance-tone-expansion100-v0-005` | `funmimonet` | `moiH3xaltg0` | `labeled` | `personal_or_event_story` | `soft_personal_or_experience` | `medium` | not_fragrance_primary, skincare_primary |
| `ytshorts-fragrance-tone-expansion100-v0-006` | `SokiLondon` | `dhFp3M6oMc8` | `labeled` | `direct_product_pitch_or_cta` | `direct_pitch_or_cta` | `high` | creator_own_brand |
| `ytshorts-fragrance-tone-expansion100-v0-007` | `TLTGReviews` | `zHTuK2_Ouf0` | `abstain` | `none` | `none` | `none` | non_fragrance_transcript, stage_awards_audio, near_minimum_word_count |
| `ytshorts-fragrance-tone-expansion100-v0-008` | `Redolessence` | `gvRng8Hkwyw` | `labeled` | `direct_product_pitch_or_cta` | `direct_pitch_or_cta` | `high` | retail_shop_context |
| `ytshorts-fragrance-tone-expansion100-v0-009` | `TheFragranceApprentice` | `fnAGBzFSQnw` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion100-v0-010` | `ChaosFragrances` | `vjzHIMn3b4w` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion100-v0-011` | `FragranceKnowledge` | `9wB39dxIL6M` | `labeled` | `contrarian_or_comedic_critique` | `non_commercial_update` | `low` | comedic_context, not_product_review_primary, short_transcript |
| `ytshorts-fragrance-tone-expansion100-v0-012` | `BowTieFragranceGuy` | `n9U1c-QRSO8` | `labeled` | `direct_product_pitch_or_cta` | `direct_pitch_or_cta` | `high` | short_transcript |
| `ytshorts-fragrance-tone-expansion100-v0-013` | `MilaLeBlanc` | `kgSCH6-SN_A` | `labeled` | `single_product_review` | `recommendation_or_review` | `medium` | short_transcript |
| `ytshorts-fragrance-tone-expansion100-v0-014` | `ThePerfumeNest` | `7EdjxOC-MNI` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion100-v0-015` | `Scentbird` | `m3Tnv4p7TAg` | `abstain` | `none` | `none` | `none` | unscoreable_caption_text, music_or_dialogue_fragment, near_minimum_word_count |
| `ytshorts-fragrance-tone-expansion100-v0-016` | `Scenteno` | `7_kbaCJR_o0` | `labeled` | `single_product_review` | `recommendation_or_review` | `medium` | short_transcript |
| `ytshorts-fragrance-tone-expansion100-v0-017` | `JusDeRose` | `G9fk8bgFv8k` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion100-v0-018` | `OliviaOlfactory` | `8iyV0R5D9B4` | `labeled` | `scent_of_day_or_wear_diary` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion100-v0-019` | `MonikaCioch` | `2tuGZN1vtUw` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion100-v0-020` | `ScentedMoments` | `bGFqsPZ7bWc` | `labeled` | `single_product_review` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion100-v0-021` | `JeremyFragrance` | `iohVc61b9Bk` | `labeled` | `scent_of_day_or_wear_diary` | `recommendation_or_review` | `medium` | interrupted_transcript |
| `ytshorts-fragrance-tone-expansion100-v0-022` | `GentsScents` | `inl7gtQd4EM` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion100-v0-023` | `ThePerfumeGuy` | `-wS9yaoumW8` | `labeled` | `direct_product_pitch_or_cta` | `direct_pitch_or_cta` | `high` | deal_context |
| `ytshorts-fragrance-tone-expansion100-v0-024` | `SchoolofScent` | `3UE8ZN1I8zM` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion100-v0-025` | `CurlyScents` | `usFrt5XnBic` | `labeled` | `personal_or_event_story` | `soft_personal_or_experience` | `medium` | creator_interview, fragrance_not_primary |
| `ytshorts-fragrance-tone-expansion100-v0-026` | `funmimonet` | `ieDgm6dPS3s` | `abstain` | `none` | `none` | `none` | non_fragrance_transcript, skincare_primary |
| `ytshorts-fragrance-tone-expansion100-v0-027` | `SokiLondon` | `wf8wjYjytuI` | `labeled` | `single_product_review` | `recommendation_or_review` | `medium` | creator_brand_context |
| `ytshorts-fragrance-tone-expansion100-v0-028` | `Redolessence` | `Ifa-qYlGEfM` | `labeled` | `single_product_review` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion100-v0-029` | `TheFragranceApprentice` | `mCNfOHwUYt4` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion100-v0-030` | `ChaosFragrances` | `NJmP-Otw57s` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion100-v0-031` | `FragranceKnowledge` | `uRzXOOZeTSE` | `labeled` | `contrarian_or_comedic_critique` | `negative_or_anti_purchase` | `low` | comedic_context, sarcasm, short_transcript |
| `ytshorts-fragrance-tone-expansion100-v0-032` | `BowTieFragranceGuy` | `G74XHCSr_CQ` | `labeled` | `ranked_or_segmented_recommendation` | `direct_pitch_or_cta` | `high` | multiple_check_out_ctas |
| `ytshorts-fragrance-tone-expansion100-v0-033` | `MilaLeBlanc` | `hK8RaqDTqo8` | `labeled` | `single_product_review` | `recommendation_or_review` | `medium` | short_transcript |
| `ytshorts-fragrance-tone-expansion100-v0-034` | `ThePerfumeNest` | `_zQeVk1r3fg` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion100-v0-035` | `Scentbird` | `hy443hJNeu8` | `abstain` | `none` | `none` | `none` | unscoreable_caption_text, non_fragrance_dialogue_fragment, near_minimum_word_count |
| `ytshorts-fragrance-tone-expansion100-v0-036` | `Scenteno` | `ZUnhHKu-cgk` | `labeled` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `high` | community_cta_secondary |
| `ytshorts-fragrance-tone-expansion100-v0-037` | `DemiRawling` | `qP0WyLE4Brc` | `labeled` | `personal_or_event_story` | `soft_personal_or_experience` | `medium` | street_interview |
| `ytshorts-fragrance-tone-expansion100-v0-038` | `JusDeRose` | `mxS8HENWII8` | `labeled` | `single_product_review` | `recommendation_or_review` | `high` | none |
| `ytshorts-fragrance-tone-expansion100-v0-039` | `ScentedMoments` | `QGh0xaigTvo` | `labeled` | `direct_product_pitch_or_cta` | `direct_pitch_or_cta` | `high` | explicit_check_out_cta |
| `ytshorts-fragrance-tone-expansion100-v0-040` | `TheScentinel` | `fDtI1QsNNqY` | `abstain` | `none` | `none` | `none` | insufficient_transcript_substance, short_transcript, no_product_named |

## Viability Read

- The patched stable fields were operational for 63 of the 70 remaining rows.
- The 7 abstains are mostly off-topic/stage-audio/skincare-primary/incoherent-caption captures; this is a capture/admission precision signal, not a transcript-tone success claim.
- Energy, pace, volume, and prosodic excitement remain out of scope for transcript labels.

## Non-Claims

- not blind independent labeling
- not inter-rater reliability
- not benchmark validation
- not buyer proof
- not energy, prosody, audio, visual, comment, engagement, or creator-level scoring
- not a consolidated hard30-plus-remaining70 adjudicated 100-row label artifact
- diagnostic note fields are not repeatable closed labels
- full transcript bodies are not stored in this artifact

Machine-readable labels are in `docs/review-inputs/youtube_shorts_fragrance_tone_labeling_remaining70_v0.json`.
