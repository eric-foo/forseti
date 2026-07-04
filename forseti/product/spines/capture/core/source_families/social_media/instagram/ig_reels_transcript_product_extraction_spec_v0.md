```yaml
retrieval_header_version: 1
artifact_role: Source-family spec (IG Reels transcript→product extraction, v0 delta)
scope: >
  The Instagram-Reels delta over the YouTube transcript→product extraction spec. IG adopts the
  YouTube contract elements CE1-CE10 and Decisions D1-D10 by reference; this file records ONLY the
  IG-specific deltas (ASR-only transcript path, anonymous yt-dlp capture, source_family/surface,
  audience-restricted skip, the deferred speech/music upgrade) and the reuse boundary.
use_when:
  - Building, reviewing, or extending the IG Reels transcript→product extraction lane.
  - Deciding what of the YouTube transcript lane IG reuses vs. what is IG-specific.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_transcript_product_extraction_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_reels_audio_capture_recipe_card_v0.md
status: V0_IMPLEMENTED_OFFLINE
non_claims:
  - not validation, not readiness, not buyer proof
  - not live-extraction authorization (the LLM caller stays owner-gated/deferred)
  - not a new lake layer (IG reuses the ratified, source-family-agnostic lake)
```

# IG Reels Transcript→Product Extraction (v0 delta)

## What this is

Instagram Reels capture → anonymous bestaudio → VAD-gated faster-whisper ASR → `transcript_asr`
derived record → LLM product-mention extraction → `silver__cleaning__product_mentions`. IG is its
own `source_family`; it reuses the YouTube lane's **patterns**, not its files.

The **core extraction contract is source-agnostic** and is inherited verbatim from the YouTube
spec: **CE1–CE10** (identity-from-input, source-pointer-required, closed enums, LLM-emits-evidence-
not-verdict, cue-timing-from-transcript, append-only/write-once, no-LLM-zone, disobedient-output-
rejected, quote-must-be-a-real-substring, stated-rating-is-evidence-only) and **Decisions D1–D10**.
Read the YouTube spec (`open_next`) for those; they are NOT restated here.

## IG deltas (the only IG-specific facts)

1. **ASR is the ONLY transcript path.** IG Reels expose no caption API, so the YouTube caption-first
   path (`youtube_captions.py` / `caption_packet.py`, `cues_from_json3`) does NOT transfer. Every IG
   transcript is ASR.
2. **Capture route = anonymous `yt-dlp` bestaudio** on a public Reel (`/reel/<shortcode>/` or
   `/p/<shortcode>/`). No login, no `po_token`, no proxy by default. Proven by the 2026-06-25
   audio-acquisition probe (acquisition GO; ASR-on-speech GO on a talking fragrance Reel).
3. **`source_family = instagram_creator`** (the same family as the existing IG Reels grid capture),
   **`source_surface = ig_reels_audio`**. The audio packet is a new *surface* under the existing
   family — not a new family — mirroring YouTube's one-family/multiple-surfaces taxonomy. Discovery
   keys on the family and filters to the `ig_reels_audio` surface (grid-metadata packets in the same
   family carry no audio and are skipped).
4. **Audience-restricted Reels are a TYPED SKIP, not a failure.** A Reel that "can't be seen by
   certain audiences" / requires login is out of anonymous scope (access-control gate); capture
   records `access_gated` and skips it, never defeating the gate.
5. **`video_id` carries the IG shortcode.** The `ProductMention` schema is reused with NO change;
   the shortcode rides the existing (non-empty-validated) `video_id` field and `transcript_source`
   is `asr`. A schema rename to a generic id is the high-lock-in path and is explicitly NOT taken.
6. **Extraction prompt is reused unchanged for v0** (YouTube spec D-Open-Decision-1, option a:
   reuse, measure, escalate). An IG-tuned prompt (e.g. a defined `creator_authored` rule) is a
   deferred refinement, not v0.

## Reuse boundary (verified against source, 2026-06-25)

- **Reused as-is (source-agnostic):** the ratified data lake (`data_lake/root.py`, by-key API, not
  sharded on main); `source_capture/models.py` packet/slice/metric models; `audio_asr.transcribe_audio`
  (VAD-gated faster-whisper); `cleaning/transcript_product_lake.py`
  (`extract_products_into_lake`, `cues_from_asr_record`, `mentions_record_id`);
  `cleaning/transcript_product_extractor.py` core (`locate_quote`, `parse_mentions`);
  `schemas/product_mention_models.py` (`ProductMention`, verdict-free).
- **IG-specific (net-new modules; YouTube files untouched):**
  - `source_capture/transcript/ig_reels_audio_packet.py` — anonymous IG audio fetch + the IG
    audio/`transcript_asr` writer (the YouTube `asr_packet.write_asr_transcript` is YouTube-coupled,
    so IG gets its own writer composed from the agnostic primitives).
  - `runners/run_source_capture_ig_reels_audio_packet.py` — IG capture CLI (with the `access_gated`
    typed skip).
  - `runners/run_ig_reels_product_extract.py` — IG daemon-ready extraction runner (the YouTube runner
    hardcodes `source_family="youtube"`, so IG gets its own).

## Deferred (named upgrades, not v0)

- **Speech/music segmentation (inaSpeechSegmenter / pyannote).** `vad_filter` gates voice-vs-silence,
  not sung-vs-spoken, so a sung brand name in a music Reel could become a false, creator-attributed
  mention. **Trigger to graduate:** real captures showing lyric brand-drops producing false mentions.
  Cheaper mitigations first: a prompt rule defining `creator_authored`, and whisper's per-segment
  `no_speech_prob` / `avg_logprob`. Owner-accepted deferral, 2026-06-25.
- **Live LLM extraction caller.** The Transport is injected; the live (subscription- or API-routed)
  caller stays owner-gated/deferred (YouTube spec D5). v0 is offline-testable with a fake transport.
- **Pass-2 verdict fusion** — now BUILT 2026-06-26 (was: deferred for IG exactly as for YouTube, CE4 / D2): the source-agnostic `scoring/product_fusion.py` serves IG + YouTube (deterministic, LLM-free; eric-foo/orca#394).

## Standing constraints (bind every line)

Public data only; anonymous (no login / no `po_token` / no proxy by default); SG-legal pre-commercial;
**never commit captured or derived data** (the data root is external + gitignored); AI confined to
`cleaning/` (no `openai`/`anthropic`/`litellm`/`langchain` in scoring/reports/runners/schemas).
