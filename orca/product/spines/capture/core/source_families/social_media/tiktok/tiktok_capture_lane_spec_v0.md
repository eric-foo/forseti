# TikTok Capture Lane Spec v0

```yaml
retrieval_header_version: 1
artifact_role: Capture spec
scope: Behavior/contract spec for the TikTok public creator-momentum + top-comment capture lane, prioritizing (1) lowest practical bot detectability and (2) horizontal scalability. Sessioned/cookied real-browser, ride-the-page's-own-requests.
use_when:
  - Implementing or reviewing the TikTok capture lane.
  - Deciding the anti-detection + scale design before any build.
authority_boundary: retrieval_only
status: spec only — no build authority; survivability-at-scale UNMEASURED (see Validation + Non-claims)
derived_from:
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_first_slice_probe_recon_v0.md   # N=1 evidence
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_logged_out_first_slice_probe_plan_v0.md
  - docs/review-outputs/tiktok_capture_calibration_architecture_review_v0.md   # routes + non-claims
  - orca-harness/source_capture/  # reuse substrate (models, cadence, writer, browser_snapshot)
priorities: [lowest_bot_detectability, scalable]
capture_mode: sessioned_cookied (owner decision 2026-06-22; supersedes the logged-out-primary posture in C8)
```

## Direction update (2026-06-22) — sessioned/cookied

Owner decision: **logged-out capture is too brittle** (highly session-trust-dependent; captchas observed, see recon addendum). The lane now captures via an **authenticated session** (cookied), which TikTok generally trusts more and challenges less. This **supersedes C8** (logged-out-only) with the account invariants in **C8'** below. Everything else (real browser, ride the page's own requests, ≤3 requests/video, cadence, identity distribution, secret hygiene) is unchanged and applies to the authenticated session. **Tradeoff accepted:** the failure mode shifts from captcha/throttle (recoverable) to **account ban** (loses the account + its accumulated trust) — mitigated by dedicated burnable accounts, conservative pacing, and human-performed login.

## Purpose

Capture public TikTok videos under a dedicated authenticated session, at human-rate, with the lowest practical detection footprint: (a) per-video/creator **momentum metadata**, and (b) a bounded set of **top/relevant comments** with commenter identity and exact timestamps — sufficient for downstream anti-bot / data-integrity analysis. The 30/60-minute comment-window requirement is **dropped** (not needed for bot detection); comments are a top/relevant *sample*, not a chronological census.

## Design spine (resolves the detectability-vs-scale tension)

**Minimize footprint per target; scale horizontally by distributing identity.** Each video is captured with ~2–3 requests by a realistic browser context; throughput comes from many paced, identity-distinct contexts — never from hammering one context.

## Capture contract (what must be true)

### C1 — Real browser context, never headless (priority-1 invariant)
Capture MUST run in a non-headless / anti-detect browser context with a genuine fingerprint and a **warmed device-cookie session** (`ttwid` etc.). Headless and bare HTTP are FORBIDDEN as capture transports — both were served a stripped/no-data page in recon. (Harness: `cloakbrowser_snapshot` / a real-browser context, NOT `direct_http` or headless `browser_snapshot`.)

### C2 — Ride the page's own signed requests; never forge signatures
The lane MUST obtain data by loading the public page and reading what the page itself produces:
- **Metadata** from the server-rendered blob `#__UNIVERSAL_DATA_FOR_REHYDRATION__` → `__DEFAULT_SCOPE__['webapp.video-detail'].itemInfo.itemStruct` (zero extra requests).
- **Comments** by letting the page issue its own signed `GET /api/comment/list` and **intercepting the response** (hook `fetch`/`XHR`).
Forging or replaying `msToken` / `X-Bogus` / `X-Gnarly` / `verifyFp` is FORBIDDEN (brittle, adversarial, higher-detection). No synthetic/cold API calls.

### C3 — Bounded request footprint per target (priority-1 invariant)
Per video: metadata = 0 extra (in the page); comments = the first page + **at most ONE** pagination. **Hard cap ≈ 3 page-emitted requests per video.** No deep pagination, no full-comment census.

### C4 — Human-rate cadence with jitter
Inter-target and inter-request timing MUST use bounded jitter (harness `cadence.build_cadence_plan(mode="bounded_jitter")`). Starting hypothesis ~2.5–4 s, never sub-2 s (carried from IG, **re-measure for TikTok**). No bursts.

### C5 — Identity distribution + per-context volume cap (scale invariant)
Scale by running N contexts in parallel, each with its **own** fingerprint + residential/mobile proxy + warmed cookies, each under a **per-context window volume cap**. Throughput = contexts × paced-rate. A single context MUST NOT exceed its window cap.

### C6 — Real-block detection → cooldown (and distinguish infra noise)
Detect a genuine TikTok block — its own 403 HTML, captcha/verify interstitial, `msToken` rejection, or an empty/stripped shell — and on it: stop the context, cool down, do not hammer. The lane MUST distinguish a **true TikTok signal** from **transport/infra glitches** (e.g., an extension/proxy `[BLOCKED: JWT token]` `chrome-error` page is NOT a TikTok block — retry once before treating as detection).

### C7 — Secret hygiene (G-2 contamination stop)
No cookies, storage-state, `msToken`, signature params, proxy endpoints/credentials, exit IPs, or device IDs may be written into any packet. Packets record category-only provenance. A packet containing any of these is contaminated scratch, not admissible.

### C8' — Sessioned/cookied via a dedicated account (supersedes logged-out-only; priority-1 + safety invariant)
Capture runs under an **authenticated session** whose cookies authenticate it. Required posture:
- **Dedicated, non-personal account(s) only** — never a personal/primary account. Accounts are treated as **burnable** (a ban costs that account, not the operator).
- **Human-performed login** via a headed session bootstrap; the agent **never enters credentials** (harness: `run_source_capture_browser_session_bootstrap.py` → `run_source_capture_authenticated_browser_packet.py`).
- **No credentials, cookies, storage-state, or tokens in any packet** (C7 / G-2) — even more load-bearing now that secrets exist.
- **Provenance labeled `entitled_session`**, not `public_logged_out`. The comment data is still real public comments; only the access path is authenticated.
- **Public content only** — no private/DM/access-controlled surfaces; authentication buys trust/stability, not access to non-public data.
- **Account-level stop-on-challenge** (per C6): on captcha/challenge/ban signals, stop that account, cool down, rotate; never solve a challenge.

## Data contract (fields)

**Per video/creator (from blob, raw integers):** `video_id`, `desc`, `createTime` (raw unix → exact), `stats{diggCount, shareCount, commentCount, playCount, collectCount}`, `author{id, uniqueId, nickname, verified, privateAccount}`, `authorStats{followerCount, followingCount, heart, videoCount}`, `music{id,title,authorName,original}`, `textExtra` (mentions/hashtags). Video post time also derivable independently via `video_id >> 32`.

**Per video, top/relevant comments (first page + ≤1 pagination), from `/api/comment/list`:** per comment `cid`, `text`, `create_time` (raw unix → exact), `digg_count`, `reply_comment_total`, `user{uid, unique_id, nickname}`. Envelope: `total`, `has_more`, `cursor`. Order is TikTok's default **relevance** sort (no web time-filter exists — confirmed); capture the source order verbatim, do not re-rank.

**Receipts (every capture):** source URL at runtime; persisted receipts carry URL path/hash only, retrieval timestamp, response body sha256/size, parsed public fields, captured-from posture (`entitled_session`), request count used, limitations, non-claims, and no-secret confirmation. Raw response bodies, signed URLs, cookies/tokens, and storage-state paths are excluded per C7.

**Source text / transcript boundary:** TikTok description (`desc`), hashtags/mentions (`textExtra`), music metadata, and captured public comments are source text. A later Funmi/session N=30 cadence receipt measured source-native subtitle metadata plus WebVTT body admission when `video.subtitleInfos` exists (`26/30` metadata present; `26/26` WebVTT parse success when present). Treat this as `source_native_subtitle_webvtt` evidence for that creator/session, labeled with TikTok's source field such as `ASR` when present. It is not owner-generated ASR, not durable audio/video preservation, not cross-creator subtitle coverage, and not a platform-wide transcript guarantee.


**Implementation note (2026-07-01):** Network-free parsed-batch admission now exists for the Funmi N30 staging shape via `orca-harness/source_capture/tiktok/batch_packet.py` and `orca-harness/runners/run_source_capture_tiktok_batch_packet.py`, with focused tests in `orca-harness/tests/unit/test_tiktok_batch_admission.py`. The verified data-lake packet is `F:\orca-data-lake\raw\97c\01KWCYZ9P72W4SJD7NDPRQT0DB` (`tiktok_creator_batch_comment_subtitle_admission`): 30 videos, 596 parsed comments, 26 transcript-bearing source-native WebVTT captures, 1044 cues, and deterministic typed extraction seeds. A first live staging producer now exists via `orca-harness/source_capture/tiktok/live_batch_probe.py` and `orca-harness/runners/run_source_capture_tiktok_live_batch_probe.py`, with fake-engine tests in `orca-harness/tests/unit/test_tiktok_live_batch_probe.py`; it runs one creator per invocation, uses headed/sessioned page-owned comment-list observation, writes sanitized grid/cadence staging JSON for the existing admission gate, stops on challenge, and records subtitle metadata only while deferring subtitle body fetch. The code is not itself a live run, profile-grid automation proof, cross-creator ceiling proof, durable media/video preservation, final product extraction, Cleaning, ECR, or Judgment.
## Explicitly out of scope

30/60-minute comment windows; full-comment pagination / chronological census; personal account use; agent-entered credentials; private or access-controlled content; media/video/audio bytes; owner-generated ASR unless separately authorized; source-native subtitle claims when `subtitleInfos` is absent; cross-creator subtitle coverage unless separately measured; signature forging; reply-thread expansion beyond the first-page `reply_comment_total` count.

## Validation plan

1. **Offline / no-live:** fixture tests for the blob parser and the comment-list JSON parser; receipt-assertion tests; secret-hygiene tests (C7); a no-live smoke mode. All green before any live run.
2. **Detection-ceiling measurement gate (owner-gated, BEFORE bulk):** a controlled, escalating volume probe that measures where (if anywhere) a *real* TikTok block appears under this design — distinct from infra noise (C6). Bulk scale is NOT authorized until this measures an acceptable ceiling. This spec designs for low detectability; it does not assert survivability.
3. **First-party-anchor option:** if bulk volume is later sourced from a vendor, a small self-captured set under this lane is the provenance-clean anchor to validate vendor fidelity.

## Harness fit (reuse, minimal new surface)

If a cold lane is confounded by TikTok UI movement or blocker behavior, open
`docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md` before any
browser action. It maps blocker classes to the bounded `BrowserPagePointerAction`
substrate and preserves the no-CAPTCHA-solving/no-success-from-challenge-close
boundary.

- **Reused substrate, lightly extended browser seam:** packet `models.py` (+ typed `MetricObservation` for stats), `cadence.py` (C4), `writer.py`/`packet_assembly.py`, `block_shell.py`/`rendered_access.py` (C6), `proxy_profiles.py` (C5), and `auth_state.py` / authenticated browser session bootstrap only for the C8' dedicated-account session boundary. The reusable browser response seam is `browser_snapshot.py::fetch_browser_page_observation_capture`: attach a response predicate before navigation, run headed/sessioned, execute a bounded post-load page action to open comments, then preserve only matching page-emitted `/api/comment/list` responses. `fetch_browser_context_responses` is not the TikTok C2 mechanism because it performs explicit in-page `fetch(url)` calls.
- **New (TikTok satellite):** `source_capture/tiktok/admission.py` (network-free parsers/sanitizers), `video_packet.py`, `batch_packet.py`, `batch_coverage.py`, `batch_projection.py`, and `live_batch_probe.py` plus `run_source_capture_tiktok_live_batch_probe.py` for one-creator live staging (C1-C3, C6: headed/sessioned, request cap, comment-panel post-load action, comment/list response predicate, sanitized staging only). The required change vs the failed recon runs is **running the existing browser observation seam non-headless/sessioned with assets allowed**, not forged request logic.

## Open decisions (owner-owned) / Non-claims

- **Volume + provenance target** (how many creators/videos/comments, freshness, first-party-required?) is unset and **flips the scale design** (self-capture vs vendor-for-bulk + first-party-anchor).
- **Proxy strategy** (residential vs mobile, pool size) is a cost-vs-detectability owner decision.
- **Detection ceiling is PARTIALLY MEASURED, not settled** - one Funmi/session cadence run completed N=30 with zero challenges and clean page-owned comment/subtitle capture. Cross-creator coverage, higher-volume survivability, longer-run account safety, and selector/signature/field drift remain unmeasured.
- This is a spec only: no build authority, no validation/readiness, no deployment. **Authenticated (sessioned) public capture via a dedicated burnable account** under the owner Risk posture; carries **account-ban and ToS exposure the owner has explicitly accepted** for this lane. Commenter handles/uids are public comment metadata for aggregate integrity analysis, not individual dossiers. Not legal advice.
```
