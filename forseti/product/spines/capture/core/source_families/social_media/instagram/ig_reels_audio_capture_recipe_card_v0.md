```yaml
retrieval_header_version: 1
artifact_role: Capture recipe card (IG Reels audio, probe-authored)
scope: >
  The banked recipe card for anonymous Instagram-Reel audio capture, authored by the 2026-06-25
  audio-acquisition probe under the capture-investigation playbook. Records the working route,
  access posture, request-rate ceiling, and known false-diagnoses so steady-state fetches go direct
  to the pinned route instead of re-walking the catalog.
use_when:
  - Capturing IG Reel audio for the transcript→product lane.
  - Checking whether an IG-audio "blocked"/skip call was made honestly.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_reels_transcript_product_extraction_spec_v0.md
non_claims:
  - not validation, not readiness, not capture authorization (per-operation network approval still required)
  - the anti-bot/at-scale envelope is unmeasured; this card is a single-Reel human-rate probe result
```

# Recipe Card — Instagram Reel audio (anonymous)

| Field | Value |
|---|---|
| **source** | Instagram Reels (public `/reel/<shortcode>/` or `/p/<shortcode>/`) |
| **substrate** | Reel media (audio track) served from IG fbcdn (`*.fna.fbcdn.net`); discovered + fetched by yt-dlp's Instagram extractor |
| **route that worked** | `python -m yt_dlp -f ba/b -o <tmpl> https://www.instagram.com/reel/<shortcode>/` — anonymous (no cookies, no proxy). Returns an `.m4a` bestaudio asset |
| **triggers / when to use** | Need a Reel's spoken content as ms-timed cues; no caption API exists for Reels, so ASR on this audio is the only transcript route |
| **content-anchor** | bestaudio bytes (sha256), fed to faster-whisper (`small`, `vad_filter=True`) → `{start_ms,end_ms,text}` cues |
| **candidate adapter shape** | `download_ig_reel_audio(shortcode) -> IgAudioFetch{status, audio_bytes, audio_ext, detail}` in `source_capture/transcript/ig_reels_audio_packet.py` |
| **access posture** | public-only; **audience-restricted / login-walled = `access_gated` typed skip** (never defeat the gate). Step-0 access-control gate governs |
| **request-rate ceiling** | human-rate, one Reel per call, attended; no batch crawl, no at-scale enumeration |
| **known false-diagnoses** | HTTP 200 on the bare page ≠ public (IG serves a logged-out app-shell with title "Instagram" and no media URL — the real signal is whether yt-dlp's extractor resolves a media URL, not the page status) |

## Probe receipts (2026-06-25, diagnostic — not entered as evidence; temp-only, deleted)

- **`DZWSHBTOjPa` → NO-GO (target-specific).** yt-dlp: *"This content isn't available to everyone:
  It can't be seen by certain audiences."* → `access_gated`. Anonymous page GET returned the
  app-shell (title "Instagram", no media hint). Audience-restricted; not a general IG NO-GO.
- **`DaALKgOsWn0` → GO (acquisition), PARTIAL (ASR).** Anonymous m4a (32.5s, Jeremy Fragrance).
  faster-whisper `base`: 1 cue, a **song lyric** ("let's go to the mall"), p=0.315 — a music-led
  Reel; VAD correctly gated the rest. Pipeline works; this Reel carries no product speech.
- **`DZ69knlsDb1` → GO (acquisition + ASR).** Anonymous m4a (56s, Jeremy Fragrance). faster-whisper
  `small`: **14 cues, p=0.979, ~55s speech**, clean fragrance commentary naming Louis Vuitton, Dior,
  Chanel with stated rankings — exactly the product-mention signal the lane consumes.

## Honest envelope / known gaps

- **Yield is per-Reel and content-dependent.** Anonymous viewability varies Reel-to-Reel; product
  signal depends on the Reel being *talking* commentary, not a music montage.
- **Anti-bot at scale is unmeasured.** This is a single-Reel, human-rate result. The anti-detect /
  proxy / JS-challenge envelope is a separately-gated (third-tranche) question, not proven here.
- **Re-probe trigger:** the pinned route failing, or output degrading (e.g. yt-dlp extractor breakage,
  a public Reel returning the app-shell) — then it is a fresh symptom under playbook Guardrail 4.
