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

Requires `curl_cffi` — install via the extra: `pip install -e "orca-harness[impersonate]"` (or
plain `pip install curl_cffi`). **Captured data is gitignored — never commit it.**
Public read-only; SG-legal non-criminal use; obtain legal counsel before commercializing a
scraping-based capability (per the source-access boundary decision).

## Keeping the Chrome costume fresh

`curl_cffi` makes our traffic look like a *specific* Chrome version. Real Chrome keeps moving, so a
frozen version eventually becomes a **stale, detectable** fingerprint. Two pieces keep it current:

- **Renovate** (`renovate.json` at the repo root) watches `curl_cffi` and auto-opens a PR on each
  new release (newer Chrome profile inside). It is scoped to `curl_cffi` only — no other dependency
  is auto-tracked. **Prerequisite:** the Renovate GitHub App must be installed on the repo/org; the
  config file alone does nothing. Once installed, Renovate's first action is an onboarding PR.
- **Manual freshness check** — CI deliberately does *not* do this (it would need a live third-party
  TLS echo, which would let an outage red-gate merges, and the signal is shallow). Before merging a
  `curl_cffi` bump, eyeball it in ~30s:
  ```
  cd orca-harness/youtube_capture
  python verify_fingerprint_v0.py
  ```
  Confirm it prints a Chrome-class JA3/JA4 distinct from Python's, and that the curl_cffi version
  reads as current. Being 1-2 Chrome majors behind is fine; only a long-frozen version is a tell.
  Never hand-override the UA over the impersonate path — that re-creates the UA-vs-TLS mismatch the
  costume exists to kill.
