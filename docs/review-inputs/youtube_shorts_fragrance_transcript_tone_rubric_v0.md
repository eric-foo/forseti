# YouTube Shorts fragrance transcript tone rubric v0

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

Automatic non-claims:
- No energy score.
- No prosody score.
- No final tone benchmark claim.
- No creator-level generalization from this fixture.
- No inter-rater reliability or label-agreement claim.
- No validation, benchmark-readiness, or buyer-proof / commercial-decision-support claim.
- No claim of repeatable labels for any field without a closed enum (see Field stability).
