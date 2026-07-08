# orca-harness/youtube_capture

YouTube **public-data** capture tooling (promoted from `_scratch/` 2026-06-21).

- `stealth_client.py` — the single network entry point: Chrome-impersonating HTTP client
  (`curl_cffi`: matched TLS/JA3 + HTTP/2 + client-hints), **anonymous-only** (no account),
  **no proxy** (proxy/residential rotation is a separate higher rung — CloakBrowser), with a
  loud non-stealth warning if it falls back to urllib.
- `capture_youtube_v0.py` — per-video capture: embedded `ytInitialPlayerResponse` metadata +
  `youtubei/v1/next` comments. Long-form + Shorts via one runner (`surface_type` switch).
- `shorts_scroll_capture_v0.py` — volume capture / load test (scrolls Shorts at a cadence;
  stops and records on the first wall).
- `enrich_ryd_v0.py` — adds a **labeled** Return-YouTube-Dislike *estimate* (never ground truth).
- `verify_fingerprint_v0.py` — independent TLS/JA3 check vs a neutral echo service.

**Method, conventions (code-enforced vs must-follow), residuals, ToS/legal posture:** see
`orca/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_agent_playbook_v0.md`
and `youtube_capture_recon_v0.md`.

Requires `curl_cffi` (`pip install curl_cffi`). **Captured data is gitignored — never commit it.**
Public read-only; SG-legal non-criminal use; obtain legal counsel before commercializing a
scraping-based capability (per the source-access boundary decision).
