# YouTube Per-Video Capture — Surface & Field Findings v0 (long-form, with Short comparison)

```yaml
retrieval_header_version: 1
artifact_role: capture findings (source-family: YouTube; recon-grade, NOT packet-grade / not build authorization)
scope: >
  Empirical results from one live capture session on the per-video and creator-level YouTube public
  surfaces: which surface yields which fields, the request cost of each, two honest gaps (comment
  totals, caption text), and a long-form-vs-Short validation of the unified-route decision. Worked
  on a long-form video; cross-checked against a genuine Short. Single-session, small-n.
use_when:
  - Deciding which surface to hit for a given YouTube field at minimum request cost.
  - Confirming the long-form / Shorts unified-route claim with field-level evidence.
authority_boundary: retrieval_only
stale_if:
  - YouTube changes the served-HTML embedded-state shape, the RSS feed schema, or po_token enforcement.
  - The channel-grid renderer changes again (it already moved videoRenderer -> lockupViewModel).
open_next:
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_recon_v0.md
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_agent_playbook_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/weapon_anti_block_http_ladder_v0.md
```

## What this is

Field-level capture findings gathered live on 2026-06-22 through the tracked stealth client
(`curl_cffi` impersonate `chrome`, anonymous, **no proxy**), no browser unless noted. It answers a
practical question the recon left open: **for each YouTube data field, what is the cheapest public
surface that yields it, and what can't be gotten cheaply at all?** Recon/findings-grade, small-n
(long-form n=1 deep + Short n=1 deep + channel/RSS probes); **not** packet-grade, **not** a capture
contract, **not** build authorization. All cited values were observed from real captures this
session (data persisted to the gitignored `orca-harness/youtube_capture/packets/`).

## Posture (unchanged from the playbook)

Public data only; anonymous-only (no login, no po_token); SG-legal non-criminal; no proxy default;
**captured data is gitignored — never committed**. Automated access is a YouTube-ToS (civil) matter,
owner-accepted; obtain legal counsel before commercializing. "Not blocked ≠ undetected."

## Surface → field matrix (the core finding)

| Field | Channel `/videos` (1 req; full catalog via continuation) | **RSS feed** (1 req; latest ~15 only) | `/watch` per-video (1 req; +1 for comments) |
|---|---|---|---|
| video id, watch url | ✅ | ✅ | ✅ |
| title | ✅ (truncated ~49ch when hashtag-heavy) | ✅ | ✅ (full, og:title) |
| view count | ⚠️ abbreviated ("15K") | ✅ **exact** | ✅ **exact** |
| publish date | ⚠️ relative ("2 days ago") | ✅ **absolute ISO** | ✅ **absolute ISO** |
| like count | ❌ | ✅ **exact** (`media:starRating count`) | ✅ **exact** (`"likeCount"`) |
| full description | ❌ | ✅ (when author wrote one) | ✅ |
| tags / category | ❌ | ❌ | ✅ |
| comment **content** | ❌ | ❌ | ✅ (`youtubei/v1/next`) |
| comment **total count** | ❌ | ❌ | ❌ *(see gaps)* |
| caption **track list** | ❌ | ❌ | ✅ |
| caption **text (transcript)** | ❌ | ❌ | ⚠️ po_token-gated → browser rung |
| thumbnail (any resolution) | ✅ (construct from id) | ✅ (from id) | ✅ (from id) |

Rendered DOM (browser rung) is a **strict subset** of the channel `/videos` JSON — it adds no field
for catalog capture and costs orders of magnitude more requests; reserve it for blocks / po_token
surfaces. (See the DOM-vs-JSON comparison run this session.)

## The surfaces in detail

1. **Channel `/videos` listing** — one GET returns channel identity + the recent-uploads grid;
   continuation token (`/youtubei/v1/browse`) pages the full catalog ~30/req. Values are
   **abbreviated/relative**. Grid renderer is now **`lockupViewModel`** (`contentId` = video id) —
   see Recon correction below.
2. **RSS feed** `https://www.youtube.com/feeds/videos.xml?channel_id=<ID>` — one GET, **latest ~15
   videos**, with **exact views, exact likes (`media:starRating count`), absolute publish dates, and
   full descriptions**. No pagination, no comments, no captions. This is the best minimal-request
   source for **recent** exact stats — 1 request replaces 15 `/watch` fetches.
3. **`/watch?v=<id>`** — one GET of the served HTML carries `ytInitialPlayerResponse`: **exact
   `viewCount` (source path can vary by surface/serving variant), absolute `publishDate`, full
   `shortDescription`, `keywords`, `category`, `lengthSeconds`, channel identity**, plus the **exact like count** (`"likeCount"` field /
   accessibility "N likes") and the caption **track list**. Comments need one more POST to
   `youtubei/v1/next`. The same `/watch?v=<id>` URL serves long-form **and** Shorts.

## Worked example — long-form (Max Forti, `wXbST6WGQ4M`)

- surface: `long_form` (stayed on `/watch`). EXACT views **15,726**; length **561 s**; publish
  **2026-06-20T05:27:49−07:00**; category **Entertainment**; description **1,905 chars**; **10**
  keywords; **exact likes 1,103**; comments captured (sample); caption tracks **1** (`en/asr`).
- **RSS cross-check (same video):** `media:statistics views="15726"` == watch 15,726 ✅;
  `media:starRating count="1103"` == watch `"likeCount":"1103"` ✅; RSS `published` == watch publish
  (same instant) ✅. → **`media:starRating count` IS the exact like count.**

## Two honest gaps

- **Comment total count — not exposed anonymously.** Absent from RSS, the channel page, and the
  watch HTML; the `youtubei/v1/next` comments response returned a `commentsHeaderRenderer` **with no
  count field** (no `countText`, no `commentCount`, no "N comments" string in a 273 KB response).
  Comment **content** is available; a **total** requires paginating every comment (expensive) and may
  only A/B-appear. Treat "comment count" as not reliably capturable cheaply.
- **Caption text — po_token-gated.** The track list is free from `/watch`, but fetching the
  `timedtext` transcript returned **HTTP 200 / 0 bytes** (empty/gated) — consistent with the recon's
  po_token watch. Transcript text needs the **browser rung** (CloakBrowser mints po_token). Creator
  surfaces never carry captions at all.

## Long-form vs Short — unified route validated

| | Long-form (Max Forti `wXbST6WGQ4M`) | Short (Jeremy `CeFQ023_ZJo`) |
|---|---|---|
| serving surface | `long_form` (→ `/watch`) | `shorts` (stays on `/shorts/`) |
| capture route | `/watch` `ytInitialPlayerResponse` | **same** (`/watch?v=<id>` works) |
| exact views | 15,726 | 708 |
| length | 561 s | 13 s |
| absolute publish | 2026-06-20T05:27:49−07:00 | 2026-06-22T05:52:08−07:00 |
| exact likes | 1,103 | 12 |
| RSS like cross-check | 1,103 == 1,103 ✅ | 12 == 12 ✅ |
| full description | 1,905 chars | 0 (empty) |
| tags / category | 10 / Entertainment | 0 / Howto & Style |
| comments | captured; no total | captured; no total |
| caption tracks | 1 (`en/asr`); text gated | 0 (fresh 13 s Short — none yet) |

**Conclusion:** route and field semantics are unified for long-form and Shorts, but individual JSON
field paths are not a stable contract. Use one runner + `surface_type` switch, with path-tolerant
extraction that records the observed source path. The only domain differences are **content**
(Shorts often have empty descriptions, no tags, and a fresh/short Short may have no caption track
yet) and the **surface discriminator**. Discriminate by **serving surface**, not duration: a
1:57 (117 s) Jeremy upload (`Qu5rbwa5iNg`) **redirected to `/watch` = `long_form`**, so duration
alone is not a Short signal.

## Request economy (which surface for which need)

- **Recent exact stats (last ~15 uploads):** RSS — **1 request** for exact views + likes + absolute
  dates + descriptions.
- **Full-catalog breadth (ids/titles, all 707):** channel `/videos` + continuation — ~1 req / 30.
- **Deep per-video (comments, tags, caption list, exact stats on *older* videos beyond RSS's window):**
  `/watch` — 1 req (+1 for comments).
- **Browser rung:** only on a detected block, or for **caption text** (po_token). Never for routine
  catalog/metadata — it yields no extra field and costs far more.

## Recon correction / drift flagged

- **Channel enumeration renderer:** recon P3 enumerated via `videoRenderer`; YouTube has since
  migrated the channel grid to **`lockupViewModel`** (`contentId` = video id). The recon's
  enumeration *example* is stale; its route *conclusion* is unaffected.
- **View-count field path (2026-06-27):** a fresh Shorts re-probe returned exact `viewCount` at
  `microformat.playerMicroformatRenderer.viewCount` while `videoDetails.viewCount` was absent. The
  one-runner conclusion stands, but extraction must be path-tolerant and record the observed path.
- **Playbook implementation location:** the agent playbook has been updated from the old scratch-code
  note to the tracked `orca-harness/youtube_capture/` implementation; captured outputs remain
  gitignored.

## Non-claims

Recon/findings-grade, single-session, small-n (deep n=1 long-form + n=1 Short; RSS→likes mapping
cross-checked n=2: 1,103 and 12). Not packet-grade, not validation/readiness, not a capture-shape
contract, not build/runtime authorization, not legal advice. The `media:starRating count` → exact
likes mapping is evidence-backed but should be re-verified if YouTube changes the feed. Comment-total
absence observed this session; YouTube A/B-tests count visibility. Captured data remains gitignored.
