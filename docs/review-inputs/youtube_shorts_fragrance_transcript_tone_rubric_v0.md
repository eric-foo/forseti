# YouTube Shorts fragrance transcript tone rubric v0

```yaml
retrieval_header_version: 1
artifact_role: Review input / transcript tone labeling rubric
scope: Transcript-only rhetorical-tone rubric for YouTube Shorts fragrance fixture labeling.
use_when:
  - Labeling or reviewing transcript-only tone fields.
  - Checking the energy/prosody exclusion and stable-field boundaries.
authority_boundary: retrieval_only
open_next:
  - docs/review-outputs/youtube_shorts_fragrance_tone_label_adjudication_v0.md
  - docs/review-inputs/youtube_shorts_fragrance_tone_labeling_run_v1.md
```

Purpose: label transcript-rhetorical tone for the hard-30 YouTube Shorts fragrance viability fixture.

Scope:
- Use transcript words, phrasing, and structure only.
- Do not use audio energy, pace, volume, prosody, visuals, comments, likes, or inferred creator performance.
- Title, description, hashtags, tags, and pinned links are channel/video metadata, not transcript. Do not derive a transcript-only label from them. When such a signal is the only basis for a posture or flag, record it as a non-transcript source in `residual_flags` and do not raise `label_confidence` on metadata alone.
- Treat YouTube auto-generated captions as machine-generated text with ASR-class error, not clean manual text. Use `label_confidence=low`, `label_status=abstain`, or a residual flag when transcript length, ASR or auto-generated (non-manual) captions, comedy or sketch context, or sponsor ambiguity weakens the label. A transcript at or near the 20-word admission floor, or comedic/sketch text that cannot be read literally, forces `label_confidence=low` or `label_status=abstain`.

Top-level fields:
- `primary_rhetorical_mode`: coarse repeatable mode. Current enum: `single_product_review`, `ranked_or_segmented_recommendation`, `scent_of_day_or_wear_diary`, `direct_product_pitch_or_cta`, `sponsored_or_partner_demo`, `personal_or_event_story`, `contrarian_or_comedic_critique`, `direct_audience_persuasion`.
- `mode_detail`: more specific subtype retained for diagnosis; do not treat as a stable class until repeated across more data.
- `commercial_directness`: coarse commercial posture. Current enum: `recommendation_or_review`, `direct_pitch_or_cta`, `explicit_sponsored_or_ad`, `soft_personal_or_experience`, `negative_or_anti_purchase`, `non_commercial_update`.
- `commercial_posture`: detailed commercial subtype.
- `lexical_intensity`: strength of transcript word choice only. This is not audio energy.
- `certainty_posture`: how conclusive or qualified the speaker sounds in text.
- `affect_valence`: positive, negative, mixed, reflective, playful, or analytical stance visible in words.
- `audience_address`: whether speech is direct second-person advice, list broadcast, review explainer, diary, routine walkthrough, or call-to-action.
- `label_status`: `labeled` or `abstain`. Use `abstain` when the transcript text cannot support a mode without guessing; an abstained row asserts no `primary_rhetorical_mode`.
- `label_confidence`: `high`, `medium`, or `low` confidence in a non-abstained transcript-only label. `abstain` is not a confidence value.
- `residual_flags`: explicit reasons a label should be treated cautiously.

Field stability:
- Closed, repeatable enums: `primary_rhetorical_mode` and `commercial_directness` only. Apply these as the stable coarse labels.
- Provisional, not yet repeatable: `mode_detail`, `commercial_posture`, `lexical_intensity`, `certainty_posture`, `affect_valence`, and `audience_address`. Their value sets are not closed; treat them as diagnostic notes, not repeatable labels, and do not measure label agreement on them until a closed enum is set for each. Closing these enums is an owner design decision, not a per-row labeler choice.

Adjudicated boundary rules:
- When a transcript is organized as a list, ranking, buying guide, multi-product collection comparison, or segmented audience recommendation, use `ranked_or_segmented_recommendation` even if the speaker uses direct second-person persuasion. Use `direct_audience_persuasion` only when persuasion is the main structure and the transcript is not primarily a list, ranking, segmented recommendation, review, or pitch.
- When a transcript centers one product or one new release with comparison as support, use `single_product_review` unless the transcript contains a transcript-visible direct purchase prompt, explicit CTA, discount-code push, link/click instruction, or ad-copy pitch strong enough to make `direct_product_pitch_or_cta` primary.
- When a transcript explicitly frames a fragrance as the speaker's scent of the day, what they wore, what they sprayed, or how the fragrance fit an occasion, use `scent_of_day_or_wear_diary` if the transcript includes substantive fragrance discussion, even when there is surrounding personal or event context. Use `personal_or_event_story` when the fragrance is incidental to a broader personal update or event story.
- For `commercial_directness`, use `explicit_sponsored_or_ad` only when sponsorship, ad, partner, or equivalent paid-placement status is explicit in the transcript. Title-only hashtags such as `#ad` are metadata; record them as residual flags and do not upgrade the stable commercial label on that basis.
- Brand-sent products, discount-code language, limited-stock language, click/link prompts, or similar transcript-visible conversion language should generally be `direct_pitch_or_cta` with residual flags for sponsor or affiliate ambiguity unless sponsorship is explicit in the transcript.
- A brief scent-of-day mention, positive descriptor, or ordinary recommendation without transcript-visible conversion language is `recommendation_or_review`, not `direct_pitch_or_cta`.
- Use `negative_or_anti_purchase` when the transcript's dominant evaluative posture is negative or discouraging, even if it acknowledges price, value, or a partial positive.

Automatic non-claims:
- No energy score.
- No prosody score.
- No final tone benchmark claim.
- No creator-level generalization from this fixture.
- No inter-rater reliability or label-agreement claim.
- No validation, benchmark-readiness, or buyer-proof / commercial-decision-support claim.
- No claim of repeatable labels for any field without a closed enum (see Field stability).
