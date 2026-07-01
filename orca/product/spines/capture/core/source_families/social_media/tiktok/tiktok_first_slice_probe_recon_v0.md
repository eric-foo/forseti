# TikTok First-Slice Probe Recon v0

```yaml
retrieval_header_version: 1
artifact_role: Capture recon
scope: First live logged-out TikTok capture probe (subject @tiktok) — route-existence recon for creator profile, video, and comments, across the harness runner ladder AND a real cookied browser. First TikTok technical recon in the repo.
use_when:
  - Authoring or updating the TikTok capture recipe card.
  - Deciding how (and whether) to scale TikTok creator-momentum + comment-integrity capture.
authority_boundary: retrieval_only
probe_date: 2026-06-21
subject: "https://www.tiktok.com/@tiktok and video 7642770753292635422 (official, public, non-personal)"
authorization: owner-authorized bounded first-slice live probe (chat, 2026-06-21); per-operation network approvals granted at runtime
evidence_location: orca-harness/_test_runs/tiktok_first_slice_probe/ (gitignored scratch; HTTP + headless/cloak browser packets) + live real-browser (Chrome extension) DOM/blob/XHR inspection captured inline
plan_ref: orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_logged_out_first_slice_probe_plan_v0.md
correction_note: This v0 supersedes an earlier in-session conclusion that comments were login-NO-GO. That conclusion was a HEADLESS bot-detection artifact and is corrected below.
non_claims: probe/recon only; one subject; survivability-at-scale NOT proven; no build authority; not validation/readiness; not legal advice
```

## Bottom line (corrected)

Logged-out, in a **real cookied browser**, TikTok exposes **both** halves the lane wanted:

- **Creator-momentum (profile + video metadata): GO.** Raw integers + exact post time, served in the page's embedded data blob.
- **Comment-integrity (comments + commenter ids + exact timestamps): GO** via the page's own `/api/comment/list` XHR (memo **Route 4**), `user_is_login=false`.
- **30/60-minute comment window: now SOLVABLE** — exact video post time + exact comment `create_time`.

The **blocker is not authentication.** Anti-bot survivability *at volume* is the open question, but it is **unproven in either direction** — the one 403 observed was an extension/proxy transient (`[BLOCKED: JWT token]`), **not** TikTok, and the page reloaded cleanly immediately after (see "Detection finding (corrected)").

## Why the headless harness said NO-GO (corrected)

The harness rungs (`run_source_capture_http_packet`, `…browser_packet`, `…cloakbrowser_packet`) were **bot-detected and served a stripped page**: HTTP 200 but ~11 KB shell with no `__UNIVERSAL_DATA__` blob, and a comment area showing "Log in to see." That produced a **false** comment-NO-GO. The same URLs in a **real Chrome (human fingerprint + `ttwid` device cookies)** return the full page. **Lesson: the capture tool must be a real/non-headless cookied browser context, not the headless harness mode.**

## What is reachable logged-out, in a real browser

**1. Embedded metadata blob (memo Route 2) — GO.** `document.getElementById('__UNIVERSAL_DATA_FOR_REHYDRATION__')` → `__DEFAULT_SCOPE__['webapp.video-detail'].itemInfo.itemStruct`. Observed for video `7642770753292635422` (raw integers):
- `stats`: diggCount 10100, shareCount 822, commentCount 1289, playCount 289000, collectCount 946
- `createTime` 1779471253 → **2026-05-22T17:34:13Z** (exact post time, raw field)
- `author`: id 107955, uniqueId `tiktok`, nickname, verified, privateAccount false
- `authorStats` (embedded on EVERY video page): followerCount 94,500,000, followingCount 3, heart 460,500,000, videoCount 1456
- `music`, `textExtra` (mentions/hashtags)

**1b. Profile page (Route 1) — GO.** Stable `data-e2e` selectors (`user-title`, `user-bio`, `user-link`, `user-post-item` ×16, `video-views` ×16); raw follower integer `94502299`; 16 video permalinks with real numeric IDs.

**2. Video post time — two independent exact sources.** (a) blob `createTime`; (b) the video ID is Snowflake-style: `unix_seconds = video_id >> 32` (decoded all 16 grid IDs to the second). Either gives exact post time; the page only *renders* relative ("1d ago" / "5-23").

**3. Comments (memo Route 4) — GO.** The page's own request:
`GET https://www.tiktok.com/api/comment/list/?aweme_id=<id>&count=20&cursor=<n>&…&user_is_login=false` (HTTP 200, logged-out), signed with `msToken`, `X-Bogus`, `X-Gnarly`, `verifyFp`, `device_id`, `odinId`. Response per comment:
```
cid, text, create_time (raw unix — EXACT), digg_count, reply_comment_total,
user:{ uid, unique_id, nickname }      ; envelope: total, has_more, cursor (paginates 20/page)
```
Observed sample (logged-out): `easy_glowe` (uid 7596762827626857492) "Tiktok posting on TikTok" → **2026-05-22T18:36:54Z**, 8 likes; `md.jinnat.065` → 2026-05-22T22:21:56Z. Total field = 1289, has_more=1, cursor stepped 20→40→60.

## Comment-window status (memo AR-02) — now solvable

Video posted 2026-05-22T17:34:13Z; `easy_glowe` commented 2026-05-22T18:36:54Z → **+62.7 min** after post, provable to the second. With exact video time (blob/ID) + exact comment `create_time` (API), the 30/60-minute post-relative window is **defensible** — but **only** from the API `create_time`, **not** the rendered DOM (which shows relative/date-only strings).

## DOM vs API (answering "can we just DOM the comments?")

- Comments are **not** in the SSR blob (`commentInBlob: false`) and **not** in the DOM until the Comments tab opens (`comment-level-1: 0` before click). They are **not preloaded-hidden** — they lazy-fetch on open.
- **After opening**, the DOM has comments (`comment-level-1`/`comment-username-1`/`comment-reply-1` ×20) but **low fidelity**: relative time only, no `cid`, no `uid`.
- **The API response is the capture target** (exact `create_time`, `cid`, `uid`, full text, replies). Do not forge signatures — let the page issue its own signed request and **intercept the response** (hook `fetch`/`XHR`, scroll to paginate).

## Detection finding (corrected)

An earlier read of this probe attributed an HTTP 403 (`chrome-error://` page, title `[BLOCKED: JWT token]`, "Access denied") to TikTok anti-bot. **That was a misattribution.** The `JWT token` block came from the **automation/extension transport layer, not TikTok**: TikTok signs with `msToken`/`X-Bogus`/`X-Gnarly` (not JWTs) and serves its own error HTML rather than a `chrome-error` page. It was **transient** — re-navigating the same browser immediately returned the full page (blob + `commentCount` 1289, `is403:false`), and the owner's manual visit to the same browser was never blocked.

**Conclusion: there is NO evidence TikTok detected or blocked us.** The N=1 logged-out capture (metadata + comments + cursor pagination) ran clean. Therefore the **detection ceiling at volume is untested — unknown, not "shown low."** The scaling constraint that *does* hold on first principles is request volume, not a measured block: full comments cost ~1 request per 20 comments (≈65 sequential XHRs for this 1,289-comment video) versus ~1 page load for metadata. More requests = more exposure, but where the actual ceiling sits is unmeasured.

## Detection addendum (2026-06-22) — real captcha (confounded) + pivot to sessioned

A second attempt to measure the logged-out ceiling hit a **genuine TikTok slider captcha** ("Drag the slider to fit the puzzle") on **first load** of a logged-out video page, in a separate browser profile on the **same IP** as the owner's main browser. The captcha was **not solved** (completing a CAPTCHA/bot-check is forbidden); the probe stopped.

**Likely confound, not a clean measurement:** that browser already had a TikTok tab open and a second/duplicate session was opened concurrently — a known challenge trigger. So this does **not** cleanly measure cold logged-out detection. Combined with the three divergent logged-out sessions on record (earlier: clean full capture, no captcha; owner's main browser: captcha after ~10 scrolls; this profile: captcha on load), the honest read is that **logged-out detection is highly session-trust-dependent and unstable**, not a fixed ceiling.

**Owner decision (2026-06-22): logged-out is judged too brittle for reliable sustained capture; the lane pivots to sessioned/cookied (authenticated) capture** via a dedicated account. Recorded tradeoff: sessioning shifts the failure mode from captcha/throttle (recoverable) to **account ban** (loses the account and its accumulated trust), so it requires a **dedicated, non-personal account**, **human-performed login** (agent never enters credentials), strict no-creds-in-packets hygiene, and labeling provenance as entitled-session. See the capture spec direction update.

## Capture recipe (draft, for the recipe card)

1. **Real/non-headless cookied browser context** (persistent profile with warmed `ttwid` device cookies) — NOT headless. Human-rate.
2. **Metadata:** read `__UNIVERSAL_DATA_FOR_REHYDRATION__` → `webapp.video-detail` for raw stats + `createTime` + author + `authorStats`.
3. **Comments:** open the Comments tab (or trigger its fetch), **intercept `/api/comment/list` responses**, paginate via cursor. Capture `cid`/`create_time`/`uid`/`text`/`digg_count`/`reply_comment_total`.
4. **Timestamps:** prefer API `create_time`; video post time also via `id >> 32`.
5. **Stop conditions:** HTTP 403 / "[BLOCKED]" / captcha → stop, cool down, do not hammer.
6. **Harness fit:** the packet-grade harness seam is `browser_snapshot.py::fetch_browser_page_observation_capture` with a response predicate for `/api/comment/list` and a bounded post-load action that opens comments. `fetch_browser_context_responses` is an explicit-fetch helper, so it must not be used as the TikTok signed-request route.

## Non-claims

One subject, one session, one day, at N=1. Selectors, gates, signature params, and field shapes drift. Comment capture rides the page's own signed requests (no signature forging, no auth defeat — `user_is_login=false`). This recon authorizes no build and no scale run; **survivability at volume is untested** (the one 403 observed was an extension/proxy transient, not TikTok — see Detection finding (corrected)). Commenter handles/uids are public comment metadata captured for aggregate integrity analysis, not individual dossiers. Not legal advice. Raw evidence in gitignored scratch.
