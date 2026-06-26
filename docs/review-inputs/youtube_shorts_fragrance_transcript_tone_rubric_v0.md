# YouTube Shorts fragrance transcript tone rubric v0

Purpose: label transcript-rhetorical tone for the hard-30 YouTube Shorts fragrance viability fixture.

Scope:
- Use transcript words, phrasing, and structure only.
- Do not use audio energy, pace, volume, prosody, visuals, comments, likes, or inferred creator performance.
- Use `label_confidence=low` or residual flags when transcript length, ASR, comedy/sketch context, or sponsor ambiguity weakens the label.

Top-level fields:
- `primary_rhetorical_mode`: coarse repeatable mode. Current enum: `single_product_review`, `ranked_or_segmented_recommendation`, `scent_of_day_or_wear_diary`, `direct_product_pitch_or_cta`, `sponsored_or_partner_demo`, `personal_or_event_story`, `contrarian_or_comedic_critique`, `direct_audience_persuasion`.
- `mode_detail`: more specific subtype retained for diagnosis; do not treat as a stable class until repeated across more data.
- `commercial_directness`: coarse commercial posture. Current enum: `recommendation_or_review`, `direct_pitch_or_cta`, `explicit_sponsored_or_ad`, `soft_personal_or_experience`, `negative_or_anti_purchase`, `non_commercial_update`.
- `commercial_posture`: detailed commercial subtype.
- `lexical_intensity`: strength of transcript word choice only. This is not audio energy.
- `certainty_posture`: how conclusive or qualified the speaker sounds in text.
- `affect_valence`: positive, negative, mixed, reflective, playful, or analytical stance visible in words.
- `audience_address`: whether speech is direct second-person advice, list broadcast, review explainer, diary, routine walkthrough, or call-to-action.
- `label_confidence`: confidence in the transcript-only label.
- `residual_flags`: explicit reasons a label should be treated cautiously.

Automatic non-claims:
- No energy score.
- No prosody score.
- No final tone benchmark claim.
- No creator-level generalization from this fixture.
