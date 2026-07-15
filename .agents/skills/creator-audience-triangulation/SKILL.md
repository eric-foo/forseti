---
name: creator-audience-triangulation
description: "Run Forseti's creator-isolated transcript-plus-comment audience triangulation during a full TikTok creator onboarding, or when the user explicitly asks to generate or refresh one creator's ideal audience / audience triangulation. Do not trigger for comparing existing profiles, copy critique, presentation review, comment analysis, Silver maintenance, capture debugging, or general creator research."
---

# creator-audience-triangulation (Forseti-local source)

## Status and authority

Forseti-local source for the onboarding firing point. It is not a product or
data authority and does not relax capture, lake, Judgment, registry, or review
rules. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`, then follow
the sources below. This source does not authorize live capture on its own.

Required product sources:

- `forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md`
- `forseti/product/spines/creator_signal/creator_commercial_projection_calibration_deck_v0.md`

Required runtime contracts:

- `forseti-harness/runners/run_tiktok_comment_attention_producer.py`
- `forseti-harness/runners/run_tiktok_grid_observation_producer.py`
- `forseti-harness/runners/run_tiktok_creator_audience_triangulation.py`
- `forseti-harness/runners/run_creator_profile_current_materialize.py`

## Trigger boundary

Use this skill only for:

1. the later stage of a user-authorized **full TikTok creator onboarding** after
   the deep-capture batch has been admitted to Bronze; or
2. an explicit request to **generate or refresh** one creator's ideal audience
   or creator-audience triangulation from existing captured evidence.

Do not use it for comparing two existing audience profiles, explaining or
critiquing copy, reviewing a creator panel, generic comment inspection, routine
Silver production, capture troubleshooting, or browsing creators. Those tasks
must not silently create or refresh a Judgment snapshot.

## Smallest complete run

Work on exactly one creator and one admitted TikTok batch packet.

1. **Choose the packet.**
   - Full onboarding: use the packet admitted by that onboarding run.
   - On demand: use the explicit packet requested; otherwise choose the latest
     admitted packet for that creator that already contains both transcript
     cues and captured top-level comments. Do not recapture merely to refresh.
2. **Produce only the packet-scoped Silver prerequisites.** Run both producers
   with the same `--data-root` and repeatable `--packet-id <packet>` selector:
   - `run_tiktok_grid_observation_producer.py`
   - `run_tiktok_comment_attention_producer.py`
   Do not drain or recompute unrelated packets.
3. **Prepare the Judgment handoff.** Run
   `run_tiktok_creator_audience_triangulation.py prepare` with the packet,
   creator ID, Creator Registry platform-account subject ID, evidence cutoff,
   a commercially useful question, and new scratch paths for the bundle and
   prompt. The expected terminal status is
   `SUBSCRIPTION_JUDGMENT_REQUIRED`; `model_api_calls` must be `0`.
4. **Run one cold subscription-agent context.** Give that agent only the
   prepared prompt. Do not put another creator in the context, do not use a
   model API, and do not add chat memory or examples as creator evidence. Save
   its JSON-only response to a new scratch file. If the host cannot create a
   cold subscription-agent context, stop at the explicit prepared status and
   surface the prompt path; never substitute an API call or a warm mixed-
   creator context.
5. **Validate before projection.** Run
   `run_tiktok_creator_audience_triangulation.py validate` with the exact bundle
   and response. Malformed JSON, unknown evidence IDs, creator mismatch,
   unsupported majority language, unsupported effect scope, or missing
   persisted-Silver support must fail visibly. Do not hand-edit around failure.
6. **Join the validated snapshot.** Materialize Creator Registry with
   `run_creator_profile_current_materialize.py --audience-triangulation-snapshot
   <snapshot> --write` plus any normally required registry inputs/preflight.
   Confirm by fresh read that the matching profile contains the exact
   `snapshot_id` under `audience_triangulation`.

## Hard gates

- Both transcript cues and captured top-level comments are mandatory. Missing
  either means `INCOMPLETE_AUDIENCE_EVIDENCE`; create no partial snapshot and
  do not write an audience triangulation to Creator Registry.
- The evidence bundle consumes persisted Silver mechanics. It must not
  recompute comment attention from Bronze inside the Judgment handoff.
- Engagement changes salience, not truth. Comment engagement does not by itself
  prove purchase, audience prevalence, demographics, or conversion.
- One creator per model context. API-level transport batching is irrelevant:
  model-context batching across creators is forbidden.
- Scratch bundle, prompt, and response files are transient. The durable derived
  lake artifact is the assembly receipt; the validated Judgment snapshot joins
  Creator Registry. Do not write the bundle or model response into Bronze or
  Silver.
- “Ideal audience” is the buyer-facing label. The internal registry field is
  `audience_triangulation`; do not recreate `ideal_audience_profile`.

## Completion receipt

Report: creator ID, platform-account subject ID, packet ID, bundle ID/hash,
snapshot ID, Silver prerequisite status, exact registry field joined, capture
limitations, and `model_api_calls: 0`. If incomplete, report the failing gate
and confirm that no Judgment/registry write occurred.

## Adoption metadata

- Source boundary: Forseti-local `.agents` source only; not user-global,
  plugin, installed-cache, or external source.
- Trigger examples: full TikTok creator onboarding; “generate/refresh this
  creator's ideal audience from the captured transcripts and comments.”
- Negative examples: “compare our two Funmi profiles”; “make this paragraph
  more commercial”; “inspect comment likes”; “run Silver catch-up.”
- Collision status: no same-name repo-local, project Claude, user Codex,
  user Agents, user Claude, or installed-plugin skill directory observed on
  2026-07-15 before creation.
- Rollback: remove this source and its skill-adoption record; do not alter
  plugin, installed, user-level, or external skill source.
