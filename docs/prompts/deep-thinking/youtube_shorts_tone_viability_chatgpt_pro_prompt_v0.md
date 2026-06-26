# YouTube Shorts Tone Viability ChatGPT Pro Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Deep-thinking prompt
scope: Prompt for stress-testing whether a YouTube Shorts tone-measurement lane is viable before building it.
use_when:
  - Asking ChatGPT Pro or another external reasoning model to decide whether YouTube Shorts tone measurement is worth building.
  - Stress-testing the split between transcript/rhetorical tone, source-context consistency, and audio/prosody energy.
authority_boundary: retrieval_only
open_next:
  - orca-harness/source_capture/transcript/youtube_captions.py
  - orca-harness/source_capture/transcript/caption_packet.py
  - orca-harness/source_capture/transcript/audio_asr.py
  - orca-harness/source_capture/transcript/asr_packet.py
  - orca-harness/signal_content/models.py
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_transcript_product_extraction_spec_v0.md
  - docs/review-inputs/youtube_shorts_tone_viability_source_pack_manifest_v0.md
branch_or_commit: codex/youtube-shorts-tone-viability-prompt; source-read base main @ 077efda1
```

## Orca Prompt Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S0 + target transcript/source-boundary files
  edit_permission: docs-write for this prompt only; receiver is read-only
  target_scope: viability stress test for a possible YouTube Shorts tone derived-record lane
  dirty_state_checked: yes; authored in clean worktree off main because root checkout was dirty
  blocked_if_missing: none for advisory viability; implementation remains unauthorized
output_mode: file-write plus paste-ready-chat copy
prompt_artifact_path: docs/prompts/deep-thinking/youtube_shorts_tone_viability_chatgpt_pro_prompt_v0.md
template_kind: deep-thinking
template_source: no bound project-local deep-thinking template used; prompt follows Orca prompt-orchestration preflight directly
edit_permission: read-only for the receiver
target_workspace: C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-shorts-tone-viability-prompt
target_branch: codex/youtube-shorts-tone-viability-prompt
source_read_base_commit: 077efda1
dirty_state_allowance: none required for repo-capable review; if no repo access, use the attached source zip plus embedded source capsule
no_repo_source_pack: docs/review-inputs/youtube_shorts_tone_viability_source_pack_v0.zip
doctrine_change: none; request is advisory viability only
receiver: ChatGPT Pro or another external reasoning reviewer
```

## Paste-Ready Prompt

You are stress-testing a proposed Orca capability before we build it.

Question: is a YouTube Shorts-specific tone-measurement lane actually viable, given that Orca already has YouTube caption acquisition, audio download, and ASR fallback?

Be adversarial. If the idea is weak, say so. Do not produce a polite roadmap for a bad metric. The intended output is a viability decision and a smallest credible v0 shape, not implementation code.

If you received `youtube_shorts_tone_viability_source_pack_v0.zip`, treat it as the source pack. Open `README.md` first, then inspect only the included files needed to answer this question. If you have no repo access and no zip is attached, use the source capsule below and mark repo verification gaps explicitly.

### Context

Orca already has a YouTube transcript stack on `main`:

- `youtube_captions.py` fetches original-language YouTube captions through yt-dlp and returns raw json3 caption bytes plus a non-authoritative flat-text view.
- `caption_packet.py` writes raw caption json3 plus metadata into a SourceCapturePacket. It explicitly says flat text is non-authoritative and Cleaning-style normalization is downstream.
- `audio_asr.py` downloads bestaudio through yt-dlp and transcribes with faster-whisper using built-in Silero VAD. It can return `transcribed`, `no_speech`, or `failed`.
- `asr_packet.py` preserves raw audio as a SourceCapturePacket and writes the ASR transcript as a derived record under `derived/<audio_packet_id>/transcript_asr/<record_id>`. ASR text is not laundered into source capture.
- `youtube_transcript_product_extraction_spec_v0.md` treats transcript extraction as downstream enrichment over already captured transcripts, not a new capture surface.
- `signal_content/models.py` keeps aggregate sentiment/reaction and Judgment-like scoring out of source-side records. Cross-source aggregate sentiment is Judgment-owned.

This proposed tone lane should therefore consume existing transcript/audio records. It should not rebuild capture, audio download, or transcription.

### The Specific Risk

The word "tone" is overloaded. Split it before judging viability:

1. `rhetorical_tone_v0`: what the transcript says and how it is framed in words.
   Examples: educational, promotional/direct-response, urgent/scarcity, contrarian/hot-take, confessional, testimonial/review, authority/expert, comedic/entertainment, fear/warning, neutral/demo.

2. `source_context_consistency_v0`: cheap checks against source framing.
   Examples: title/description/hashtags/caption kind/transcript source/video metadata contradict or reinforce the transcript-derived reading. This is a consistency/audit layer, not a second independent verdict.

3. `delivery_energy_v0`: audio/prosody only.
   This is the catch: "energy" is mostly pace, loudness, pitch movement, pauses, excitement, and vocal delivery. ASR preserves words and throws most acoustics away. A text-derived energy score is mostly a guess. If energy matters, it must be measured from the audio that is already fetched for ASR, not inferred from transcript words.

Do not accept any design that ships transcript-derived "energy" as if it were real.

### Decision To Make

Is this lane viable at all?

Return one of:

- `GO_TRANSCRIPT_TONE_ONLY`: viable if scoped to evidence-backed rhetorical tone plus source-context flags; audio energy deferred or separate.
- `GO_WITH_AUDIO_ENERGY_SPLIT`: viable only if v0 includes a separate audio/prosody feature path for energy.
- `NO_GO`: not worth building now because the labels would be too subjective, too weakly evidenced, or too easy to overclaim.
- `NEEDS_OWNER_DECISION`: one or two owner decisions materially determine viability.

### Viability Bar

The lane is viable only if it can satisfy all of these:

- Every text/rhetorical tone label has timestamped evidence spans or cue references.
- The record states whether the input was manual captions, auto captions, or ASR.
- It names confidence and residuals instead of pretending tone is source truth.
- Source metadata is used to flag mismatch or framing, not to override transcript evidence silently.
- Audience reaction, cross-video aggregation, creator intent, and commercial Judgment scores stay out of v0.
- Energy is either audio/prosody-based or not shipped.
- The offline test plan can run with canned caption json3 and fake ASR/audio fixtures. No network is required to test the tone extractor.

### Source-Context Comparison Question

Evaluate this design choice directly:

Should v0 compare transcript-derived tone to source context?

Candidate answer to stress-test:

Use source context as a bounded consistency layer. Include fields like title, description excerpt, hashtags, caption source, transcript source, capture packet ids, publication metadata if available, and comments posture if present. Use it to add flags such as "title is promotional but transcript is neutral-demo" or "ASR no_speech makes tone unavailable." Do not make it a full source-vs-tone adjudication layer in v0.

Say whether this is correct, too weak, or too heavy.

### Energy Question

Evaluate this hard line:

Do not infer `delivery_energy` from transcript text. If measuring energy matters, compute it from audio/prosody features such as speaking rate, speech/non-speech ratio, loudness dynamics, pitch/prosody proxies where feasible, and pause density. If the current audio artifacts are insufficient for durable prosody measurement, say exactly what extra derived feature extraction would be needed. If audio energy is too much for v0, recommend deferring it rather than faking it.

### Proposed Record Shape To Critique

Critique or revise this possible derived record:

```json
{
  "kind": "youtube_shorts_tone_observation_v0",
  "video_id": "<youtube video id>",
  "transcript_source": "caption_manual | caption_auto | asr",
  "transcript_anchor": "<caption packet id or audio packet id>",
  "input_posture": "available | no_speech | failed | missing",
  "rhetorical_tone": [
    {
      "label": "educational | promotional | urgent_scarcity | contrarian | confessional | testimonial | authority_expert | comedic | fear_warning | neutral_demo | other",
      "confidence": 0.0,
      "evidence": [
        {
          "cue_id": "<id if available>",
          "start_ms": 0,
          "end_ms": 0,
          "quote": "<short verbatim transcript substring>"
        }
      ],
      "residuals": ["possible_irony", "auto_caption_quality", "ambiguous_context"]
    }
  ],
  "source_context_consistency": {
    "checked": true,
    "context_refs": ["title", "description", "hashtags", "caption_kind"],
    "flags": ["promotional_title_neutral_transcript", "missing_description", "asr_only"]
  },
  "delivery_energy": {
    "status": "not_measured | measured_from_audio | deferred",
    "non_claim": "not inferred from transcript text"
  },
  "non_claims": [
    "not source truth",
    "not audience sentiment",
    "not creator intent certainty",
    "not Judgment score",
    "not cross-video aggregation"
  ]
}
```

### Required Output

Return a concise but rigorous decision memo with these sections:

1. **Verdict**
   Pick one of the four verdicts. If `NO_GO`, stop after explaining why and name the smallest salvageable alternative, if any.

2. **What Is Actually Measurable**
   Separate transcript-measurable, source-context-measurable, and audio/prosody-measurable claims.

3. **What Must Not Be Claimed**
   Be explicit about overclaims, especially transcript-derived energy, creator intent, audience sentiment, and cross-video aggregate meaning.

4. **Recommended v0 Scope**
   Name the smallest complete v0. Include what to cut.

5. **Source-Context Comparison**
   Decide whether the bounded consistency layer is worth including in v0.

6. **Energy Handling**
   Decide whether energy is deferred or requires an audio-feature path now. Do not permit text-derived energy.

7. **Record Shape**
   Critique the proposed JSON. Name required fields, fields to remove, and fields that need stricter enums or residuals.

8. **Validation Plan**
   Give an offline validation plan using canned caption/ASR fixtures. Include at least one negative test for no-speech/music and one test proving quote substrings bind to cue timestamps.

9. **Kill Criteria**
   State when Orca should abandon the lane or keep it manual.

10. **Next Step**
   Give one smallest next step if viable. It must not be "build the whole lane."

### Style

Be direct and skeptical. Prefer a narrow viable metric over a broad impressive one. If the only honest answer is "rhetorical tone yes, energy no," say that plainly.
