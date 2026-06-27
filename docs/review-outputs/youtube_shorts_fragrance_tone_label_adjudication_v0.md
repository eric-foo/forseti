# YouTube Shorts fragrance tone label adjudication v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Adjudicates the 8 stable-field mismatches between v0 and v1 hard-30 YouTube Shorts fragrance tone labels.
use_when:
  - Resolving label-boundary decisions before labeling the remaining 70 Shorts.
  - Checking why the transcript-tone rubric gained adjudicated boundary rules.
  - Reviewing stable-field mismatch outcomes for the hard-30 fixture.
authority_boundary: retrieval_only
open_next:
  - docs/review-outputs/youtube_shorts_fragrance_tone_label_adjudication_v0.json
  - docs/review-inputs/youtube_shorts_fragrance_transcript_tone_rubric_v0.md
  - docs/review-inputs/youtube_shorts_fragrance_tone_labeling_run_v1.json
```

Generated: `2026-06-26T18:20:47Z`

## Scope

This adjudicates only the 8 rows where v0 and v1 disagreed on at least one stable field. It does not label the additional 70 Shorts in the 100-row pool.

Stable fields adjudicated: `primary_rhetorical_mode` and `commercial_directness`. Diagnostic fields remain non-repeatable notes.

## Outcome

- Rows adjudicated: 8
- v1 stable pair retained: 6
- v0 stable pair retained: 1
- split/shared-pair resolution: 1
- remaining 70 labels: not run

Post-adjudication reference alignment over the hard-30:

- v0 primary matches adjudication: 26 / 30
- v1 primary matches adjudication: 29 / 30
- v0 commercial matches adjudication: 25 / 30
- v1 commercial matches adjudication: 30 / 30
- v0 exact stable-pair matches adjudication: 23 / 30
- v1 exact stable-pair matches adjudication: 29 / 30

These are reference-alignment counts only, not inter-rater reliability.

## Adjudicated Rows

| Fixture | Creator | Video | Adjudicated Mode | Adjudicated Commercial | Confidence | Resolution |
| --- | --- | --- | --- | --- | --- | --- |
| `ytshorts-fragrance-tone-hard30-v0-001` | `JeremyFragrance` | `as7hye0qgYc` | `scent_of_day_or_wear_diary` | `recommendation_or_review` | `low` | `mode_same; commercial_resolves_to_v1` |
| `ytshorts-fragrance-tone-hard30-v0-010` | `SchoolofScent` | `uaCSynFfPpc` | `ranked_or_segmented_recommendation` | `direct_pitch_or_cta` | `medium` | `stable_pair_resolves_to_v1` |
| `ytshorts-fragrance-tone-hard30-v0-011` | `CurlyScents` | `MN3AI-mrPWk` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `medium` | `mode_resolves_to_v1; commercial_same` |
| `ytshorts-fragrance-tone-hard30-v0-015` | `SokiLondon` | `XDscn2sgW3w` | `ranked_or_segmented_recommendation` | `recommendation_or_review` | `medium` | `mode_resolves_to_v1; commercial_same` |
| `ytshorts-fragrance-tone-hard30-v0-018` | `TLTGReviews` | `-V7MN2IWMpA` | `scent_of_day_or_wear_diary` | `soft_personal_or_experience` | `medium` | `mode_resolves_to_v0; commercial_same` |
| `ytshorts-fragrance-tone-hard30-v0-027` | `JeremyFragrance` | `DUafgG-TLms` | `single_product_review` | `recommendation_or_review` | `medium` | `stable_pair_resolves_to_v1` |
| `ytshorts-fragrance-tone-hard30-v0-028` | `CurlyScents` | `oFSnzMS8yxA` | `direct_product_pitch_or_cta` | `direct_pitch_or_cta` | `low` | `mode_same; commercial_resolves_to_v1` |
| `ytshorts-fragrance-tone-hard30-v0-030` | `SokiLondon` | `XTgiBsIaokI` | `single_product_review` | `negative_or_anti_purchase` | `high` | `mode_same; commercial_resolves_to_v1` |

## Decision Notes

### ytshorts-fragrance-tone-hard30-v0-001 - JeremyFragrance / as7hye0qgYc

- v0: `scent_of_day_or_wear_diary` / `direct_pitch_or_cta`
- v1: `scent_of_day_or_wear_diary` / `recommendation_or_review`
- adjudicated: `scent_of_day_or_wear_diary` / `recommendation_or_review`
- basis: Brief scent-of-day mention with one positive descriptor and no transcript-visible conversion language is recommendation_or_review, not direct_pitch_or_cta.
- evidence summary: The transcript names a fragrance of the day and calls it sexy, but contains no buy, link, discount, or check-out language.
- residual flags: asr_derived_text, short_transcript, near_minimum_word_count

### ytshorts-fragrance-tone-hard30-v0-010 - SchoolofScent / uaCSynFfPpc

- v0: `single_product_review` / `recommendation_or_review`
- v1: `ranked_or_segmented_recommendation` / `direct_pitch_or_cta`
- adjudicated: `ranked_or_segmented_recommendation` / `direct_pitch_or_cta`
- basis: A three-product buying guide is ranked_or_segmented_recommendation; brand-sent products plus discount-code language is direct_pitch_or_cta unless sponsorship is explicit.
- evidence summary: The transcript says the brand sent multiple products, selects three, names a number-one pick, and points to discount-code availability.
- residual flags: brand_sent_products, discount_code_cta, sponsored_ambiguity

### ytshorts-fragrance-tone-hard30-v0-011 - CurlyScents / MN3AI-mrPWk

- v0: `direct_audience_persuasion` / `recommendation_or_review`
- v1: `ranked_or_segmented_recommendation` / `recommendation_or_review`
- adjudicated: `ranked_or_segmented_recommendation` / `recommendation_or_review`
- basis: Top-10 list structure takes precedence over direct-address persuasion; audience address remains diagnostic, not the primary mode.
- evidence summary: The transcript frames a social-effect promise, then proceeds as a 10-perfume list.
- residual flags: rapid_list_sparse_detail, direct_address_secondary

### ytshorts-fragrance-tone-hard30-v0-015 - SokiLondon / XDscn2sgW3w

- v0: `single_product_review` / `recommendation_or_review`
- v1: `ranked_or_segmented_recommendation` / `recommendation_or_review`
- adjudicated: `ranked_or_segmented_recommendation` / `recommendation_or_review`
- basis: A collection comparison covering three releases is segmented recommendation/review, not a single-product review.
- evidence summary: The transcript walks through three Euphoria collection releases and compares their scent profiles.
- residual flags: multi_product_collection_review

### ytshorts-fragrance-tone-hard30-v0-018 - TLTGReviews / -V7MN2IWMpA

- v0: `scent_of_day_or_wear_diary` / `soft_personal_or_experience`
- v1: `personal_or_event_story` / `soft_personal_or_experience`
- adjudicated: `scent_of_day_or_wear_diary` / `soft_personal_or_experience`
- basis: A wear diary remains scent_of_day_or_wear_diary when the transcript explicitly frames what was worn, spraying, and occasion fit, even with surrounding personal update content.
- evidence summary: The transcript is long and personal, but it explicitly frames a scent of the day, discusses the occasion for wearing it, and includes substantive fragrance description.
- residual flags: long_personal_context, event_context

### ytshorts-fragrance-tone-hard30-v0-027 - JeremyFragrance / DUafgG-TLms

- v0: `direct_product_pitch_or_cta` / `direct_pitch_or_cta`
- v1: `single_product_review` / `recommendation_or_review`
- adjudicated: `single_product_review` / `recommendation_or_review`
- basis: Positive new-release testimonial without transcript-visible buy/check/link/discount language is single_product_review plus recommendation_or_review, not direct_product_pitch_or_cta.
- evidence summary: The transcript praises a new release and compares it to another fragrance, but does not include an explicit conversion prompt.
- residual flags: duplicate_product_context, comparison_as_support

### ytshorts-fragrance-tone-hard30-v0-028 - CurlyScents / oFSnzMS8yxA

- v0: `direct_product_pitch_or_cta` / `explicit_sponsored_or_ad`
- v1: `direct_product_pitch_or_cta` / `direct_pitch_or_cta`
- adjudicated: `direct_product_pitch_or_cta` / `direct_pitch_or_cta`
- basis: Compact product-copy language can be direct pitch, but explicit_sponsored_or_ad requires transcript-visible sponsorship/ad language; title-only #ad stays residual.
- evidence summary: The transcript is short product-copy praise; the ad marker is only in metadata, not transcript text.
- residual flags: short_transcript, title_ad_marker_non_transcript, near_minimum_word_count

### ytshorts-fragrance-tone-hard30-v0-030 - SokiLondon / XTgiBsIaokI

- v0: `single_product_review` / `recommendation_or_review`
- v1: `single_product_review` / `negative_or_anti_purchase`
- adjudicated: `single_product_review` / `negative_or_anti_purchase`
- basis: Dominant negative evaluation is negative_or_anti_purchase even when the transcript acknowledges good price.
- evidence summary: The transcript calls the perfume boring and not distinctive, while treating price as only a partial offset.

## Rubric Patch

The rubric now carries these adjudicated boundary rules:

- List/ranking/segmented structure takes precedence over direct-address persuasion for primary_rhetorical_mode.
- Multi-product collection comparison is ranked_or_segmented_recommendation, not single_product_review.
- Scent-of-day/wear diary can remain primary despite personal context when the transcript includes substantive fragrance wearing or description.
- direct_product_pitch_or_cta requires transcript-visible conversion language or strong ad-copy pitch; ordinary positive review stays recommendation_or_review.
- explicit_sponsored_or_ad requires transcript-visible sponsorship/ad/partner language; title-only #ad stays residual.
- Brand-sent plus discount-code/stock/link language is direct_pitch_or_cta with sponsor ambiguity unless explicit sponsorship is in transcript.
- Dominant negative evaluation is negative_or_anti_purchase even with partial price praise.

## Scale Decision

Do not label the remaining 70 until the patched rubric and this adjudication are accepted as the working boundary contract.

## Non-Claims

- not labels for the remaining 70 Shorts
- not blind independent labeling
- not inter-rater reliability
- not benchmark validation
- not buyer proof
- not energy, prosody, audio, visual, comment, or engagement scoring
- full transcript bodies are not stored in this artifact

Machine-readable adjudication is in `docs/review-outputs/youtube_shorts_fragrance_tone_label_adjudication_v0.json`.
