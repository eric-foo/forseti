# YouTube Capture — Agent Playbook v0 (method + stealth conventions)

```yaml
retrieval_header_version: 1
artifact_role: capture agent playbook (source-family: YouTube)
scope: >
  How an agent captures PUBLIC YouTube creator/video/comment data and the stealth conventions to
  follow. Splits what is ENFORCED BY CODE from what the agent MUST FOLLOW (not code-enforceable).
use_when:
  - About to run or build YouTube public capture.
  - Choosing a route, pacing, or deciding when to escalate to a real browser.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_recon_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - forseti/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md
stale_if:
  - YouTube changes the served-HTML embedded-state shape, the youtubei comment route, or its po_token enforcement.
  - The stealth client's impersonation target drifts materially from current Chrome.
```

## What this is

The proven, lowest-cost way to capture public YouTube data, plus the stealth posture that keeps it
viable at volume. The capture method and route decision live in `youtube_capture_recon_v0.md`; this
doc is the **operating playbook** for an agent doing the work.

**Authorized scope:** PUBLIC data only, under `ACCEPTED_SOURCE_ACCESS_BOUNDARY_DECISION_V0`
(anti-detect/fingerprint config = owner-accepted ToS/litigation risk; SG-legal non-criminal use).
It is a costume, not a lockpick: it accesses nothing gated and defeats no authentication.

## Method quick reference (proven; see recon card for evidence)

- **Metadata:** parse the embedded `ytInitialPlayerResponse` JSON in the served `/watch?v=` HTML
  (exact `viewCount`/`lengthSeconds`/absolute-ISO `publishDate`/`channelId`/`author`/description).
- **Comments:** POST the comments engagement-panel continuation token to `youtubei/v1/next`
  (anonymous, API key from the page). Same route for long-form and Shorts. `publishedTime` is
  **relative** ("2 days ago"); infer absolute time from publish-date floor + retrieval-time − offset.
- **Surfaces unified:** long-form and Shorts share substrate, field paths, and comments route ->
  one runner + `surface_type` switch. Discriminate by **serving surface** (does `/shorts/<id>` stay
  on `/shorts/` vs redirect to `/watch`), not duration alone (Shorts run up to ~180s).
- **Dislikes:** not publicly capturable. Ground truth only via **creator-OAuth** (consent-based);
  otherwise the **Return YouTube Dislike** API as a **low-weight labeled estimate** (accurate
  pre-2021-11-10, ±15-25% after); never a hard authenticity threshold.

## ENFORCED BY CODE (the implementation guarantees these)

Current implementation: `forseti-harness/_scratch/youtube_capture/` (gitignored scratch).
- **Single network entry point:** all fetches go through `stealth_client.http_get`; capture +
  shorts scripts import it. Don't call `urllib`/`requests` directly for YouTube.
- **Chrome impersonation:** `stealth_client` uses `curl_cffi` `impersonate="chrome"` (matched
  TLS/JA3 + HTTP/2 + client-hints). Verified 2026-06-21 vs a neutral echo: JA3 `bc54cda9…` / JA4
  `t13d1516h2_…` / h2, distinct from Python's `a1ebe7f9…` / `t13d1713h1_` / HTTP/1.1.
- **Anonymous only:** a persistent Session carries anonymous cookies (CONSENT/visitor_data); **no
  account login**, no auth cookies injected.
- **Proxy from env only:** `YT_PROXY`/`HTTPS_PROXY`; never hardcoded, never logged.
- **Loud non-stealth guard:** `STEALTH_OK` is false and a stderr WARNING fires if it falls back to
  urllib (detectable as Python) — never run the fallback at volume silently.
- **Route-health from receipts, not a canary:** each packet records `comments_posture`
  (`captured`/`empty`/`disabled`); a volume run records walls/429s. (A standalone canary was tried
  and dropped as redundant.)

## YOU MUST FOLLOW (not code-enforceable — judgment)

- **Public only; never defeat auth/access-control.** If a surface needs login/po_token/CAPTCHA to
  reveal *gated* content, stop — do not bypass. (Reaching *public* content despite anti-bot friction
  is in-bounds under the source-access posture; defeating access control is not.)
- **Pace, not volume, is the wall (IG lesson).** Keep per-IP spacing human-rate; back off on 429 /
  consent / "confirm you're not a bot" rather than escalating volume.
- **Hybrid escalation ladder:** raw-HTTP stealth client is the default rung; escalate a *specific*
  request to a real browser (CloakBrowser, which mints `po_token` natively) only when a wall /
  empty-continuation / po_token demand is detected. Don't browser-everything (cost) or
  auth-session for public data (no gain, account risk).
- **Trust your zeros only when stealth + control are healthy.** A run of `empty` comment-postures
  across many items = a wall (treat the batch as suspect); scattered `disabled` = normal.
- **ToS posture:** automated access violates YouTube ToS (civil/contractual, owner-accepted risk) —
  not criminal here, but **obtain legal counsel before commercializing** a scraping-based capability
  (per the source-access decision).

## Accepted residuals (named, Mini God Tier lens)

- **po_token not minted** (no JS) — currently only gates playback/media, not the comment route;
  escalate to a browser if enforcement spreads.
- **No residential proxies** (single IP) — env hook present, unused/untested.
- **Fingerprint version-drift** — Chrome-class and coherent, not proven byte-identical to the latest
  live Chrome build; re-verify with `verify_fingerprint_v0.py` periodically.
- **"Not blocked ≠ undetected"** — we cannot observe YouTube's classifier; absence of a block is not
  proof we are unprofiled.

## Where the code lives / reuse

The implementation is in **gitignored scratch** (`forseti-harness/_scratch/youtube_capture/`): usable
on this machine/worktree, but **not committed** — so it is not yet reusable across fresh clones.
Promoting it to tracked `forseti-harness/` code is a separate, higher-lock-in decision (committing
scraping/anti-detect tooling) and should be made explicitly by the owner, with the legal-counsel
caveat above in view. Until then, this playbook is the durable doctrine; the code is rebuildable
from the recon card + this doc.

## Non-claims

Not validation, readiness, or legal advice. Not authorization to capture, build tracked tooling,
schedule, or store beyond the bounded scratch work already authorized. No bot/fake classification
from comments alone — the supportable claim is "source-native public data suitable for later
corroboration, with limitations."
```
