---
name: creator-audience-triangulation
description: "Run Forseti's creator-isolated transcript-plus-comment audience triangulation during supported creator onboarding, or when the user explicitly asks to generate or refresh one creator's ideal audience / audience triangulation. Do not trigger for comparing existing profiles, copy critique, presentation review, comment analysis, Silver maintenance, capture debugging, or general creator research."
---

# creator-audience-triangulation (Forseti-local source)

## Status and authority

Forseti-local source for the onboarding firing point. It is not product or data
authority and does not authorize capture on its own.

Required product sources:

- `forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md`
- `forseti/product/spines/creator_signal/creator_ideal_audience_distillation_deck_v0.md`

Required runtime contracts:

- `forseti-harness/judgment/creator_audience.py`
- `forseti-harness/runners/run_tiktok_creator_onboarding_coordinator.py`
- `forseti-harness/runners/run_tiktok_creator_audience_triangulation.py`
- `forseti-harness/runners/run_instagram_creator_audience_triangulation.py`
- `forseti-harness/runners/run_creator_profile_current_materialize.py`

## Trigger boundary

Use only for the later stage of a supported, user-authorized creator onboarding
after evidence admission, or an explicit request to generate/refresh exactly one
platform account's ideal audience from existing evidence. Do not trigger for
comparisons, copy review, generic comment inspection, Silver maintenance,
capture troubleshooting, or browsing creators.

## Smallest complete run

1. **Choose one complete evidence set.** Work on exactly one platform account.
   Reuse explicit or latest complete admitted evidence; do not recapture merely
   to refresh.
2. **Prepare through the platform adapter.** TikTok uses its onboarding
   coordinator and packet-scoped Silver prerequisites. Instagram uses
   `run_instagram_creator_audience_triangulation.py prepare` with explicit,
   already-admitted Reel audience-comment and transcript Silver records. The
   expected status is `SUBSCRIPTION_JUDGMENT_REQUIRED`; `model_api_calls` is `0`.
3. **Run one cold subscription context.** Give it only the emitted prompt. The
   prompt embeds the exact method deck and compact lossless evidence view; it
   excludes named calibration examples, another creator, chat memory, and model
   API transport.
4. **Submit exact response bytes.** The response supplies semantic claims,
   evidence aliases, and buyer-facing projection choices only. The shared
   compiler derives durable claim/evidence IDs, source-item closure, modality,
   support scope, summaries, method hash, and snapshot identity. It never fuzzy-
   corrects an unknown alias or grants unavailable engagement salience.
5. **Complete verified materialization.** Only a validated
   `creator_audience_triangulation_snapshot_v1` paired with its exact successful
   `creator_audience_judgment_outcome_v1` may join `audience_triangulation`.
   Existing v0 snapshot/outcome documents remain readable; new writes are v1.

## Hard gates

- Both content/transcript evidence and captured top-level comments are mandatory.
- One platform account per context; no cross-creator or cross-platform fusion.
- Engagement changes salience, not truth. TikTok elevation requires its persisted
  same-observation Silver capability. Instagram comment likes remain visible but
  are not elevation-eligible without an equivalent admitted capability.
- Full audit bundles, assembly receipts, and exact response bytes preserve
  reproducibility; the model sees the compact view, not the audit envelope.
- `ideal audience` is buyer-facing language; the registry field remains
  `audience_triangulation`.
- YouTube is outside the supported adapter set for this version.

## Completion receipt

Report creator ID, platform-account ID, platform, evidence anchor(s), bundle
ID/hash, method-deck hash, response hash, Judgment outcome path, snapshot ID,
Silver prerequisite status, registry field, capture limitations, compatibility
residuals, and `model_api_calls: 0`. If blocked, report every validation defect,
confirm no snapshot/registry write, and state whether recapture is required.

## Adoption metadata

- Source boundary: Forseti-local `.agents` source only.
- Positive triggers: full supported creator onboarding; explicit ideal-audience
  generate/refresh from admitted transcripts/content and comments.
- Negative triggers: comparing profiles, copy edits, comment-like inspection,
  Silver catch-up, or capture debugging.
- Rollback: restore the prior firing-point source; do not alter user/global or
  plugin skill sources.