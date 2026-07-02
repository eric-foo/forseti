# YouTube Shorts Grid-Tier Assessment v0

```yaml
retrieval_header_version: 1
artifact_role: live_probe_assessment_receipt
scope: >
  Assessment (not implementation) of the YouTube Shorts channel grid as the
  cheap DAILY capture tier under the owner's 2026-07-02 two-tier daily-cadence
  direction, with a code/artifact comparison against the IG /reels/ grid and
  TikTok profile-grid capture surfaces. Records observed per-tile fields, route
  viability logged-out, per-video view-capture proof, gaps, and a grid-tier
  shape recommendation feeding the owner fork. Commissioned by
  docs/workflows/yt_shorts_grid_tier_assessment_handoff_v0.md.
use_when:
  - Deciding the per-platform shape of the daily grid capture tier
    (views-only vs engagement-bearing vs unusable).
  - Checking what the YT Shorts grid exposed per tile logged-out on the probe
    date, and how that compares to IG/TT grid surfaces in existing capture code.
stale_if:
  - A later YT grid probe observes different tile fields, tile depth, access
    posture, or wall behavior.
  - The IG reels-grid or TikTok capture modules materially change what their
    grid surfaces expose.
  - The owner revisits the two-tier daily-cadence direction.
authority_boundary: retrieval_only
```

## Recommendation (feeds the owner fork; does not resolve it)

**Option (a): the YT grid tier is views-only and spike-triggers deep
watch-packet capture.** The logged-out YT Shorts channel grid works today and
exposes per-video views (rounded display text) but no likes, no comments, and
no publish date per tile. That matches the owner's stated YT spike rule ("view
spike for yt shorts") exactly. IG and TT grid surfaces ARE engagement-bearing
in our existing capture paths (views + likes + comments per item), so their
richer view/like/comment spike rule is feasible from grid tier alone.

Spike thresholds, rounded-count spike semantics, and daily-cadence scheduling
remain owner decisions and are not resolved here.

## Probe Method And Authorization

- Authorization: owner direction 2026-07-02 authorizes assessment probes
  (verbatim quote carried in the handoff packet, verified before probing).
- Probe vehicle: adapted the enumeration/wall-detection/pacing posture of
  `orca-harness/youtube_capture/shorts_scroll_capture_v0.py` (blob `a80bf567`
  @ `origin/main cf43db5f`, re-verified) into a scratch read-only probe script;
  no repo code changed, no producer built.
- Wire posture: the harness's own `stealth_client.http_get`
  (backend observed: `curl_cffi:chrome`), logged-out, no cookies or session.
- Bound: 3 admitted roster channels (from the read-only linkage ledger, blob
  `e8d35b5c` re-verified), channel-id URLs (`/channel/<UC…>/shorts` — ledger
  handles are capture labels, not guaranteed-current handles), 5 HTTP requests
  total (3 grid + 2 watch), ~12 s pacing, stop-on-first-wall.
- Wall outcome: **no wall signals** — all requests HTTP 200, no
  `consent.youtube.com` redirect, no "Sign in to confirm you" interstitial.
- Two runs, same bound (5 requests each). Run 1 (targeted extraction,
  scratch-only): 2026-07-02T16:19:27Z–16:20:17Z. Run 2 (full-fidelity,
  owner-requested, committed to the lake): 2026-07-02T16:36:10Z–16:36:59Z.
  See "Run 2: Full-Fidelity Evidence Commit" below for the durable raw
  evidence; the load-bearing observations are inlined throughout.

## Observed: YT Shorts channel grid, logged-out

| Channel (roster id) | Channel ID | HTTP | Tiles in initial HTML | Renderer | Continuation markers |
|---|---|---|---|---|---|
| JeremyFragrance (acct_yt_fragrance_011) | UCzKrJ5NSA9o7RHYRG12kHZw | 200 | 48 | `shortsLockupViewModel` | present |
| GentsScents (acct_yt_fragrance_010) | UC9IImcLkUdmURWtQhxu8VwQ | 200 | 13 | `shortsLockupViewModel` | present |
| Redolessence (acct_yt_fragrance_018) | UCuSy0Z5UwvkMQ7lXRbUdOnQ | 200 | 48 | `shortsLockupViewModel` | present |

Per-tile fields actually observed (tile = `richGridRenderer.contents[].
richItemRenderer.content.shortsLockupViewModel`; top-level keys:
`accessibilityText, entityId, indexInCollection, inlinePopStateEntityKey,
loggingDirectives, menuOnTap, menuOnTapA11yLabel, onTap, overlayMetadata,
stackedFrameData, thumbnailViewModel, titleTruncationStyle`):

- **video_id**: present per tile (48/48, 13/13, 48/48 tiles carried one).
- **title**: present (overlay metadata + accessibility text).
- **view count**: present per tile as ROUNDED display text only — observed
  values like `834 views`, `1.5K views`, `5.2K views`, `241K views`. Below ~1K
  the display text is unit-precise (`834 views`); at K/M scale it is
  quantized to 2 significant figures.
- **likes**: ABSENT — no like field or like-bearing string in any tile.
- **comments**: ABSENT — no comment field or comment-bearing string in any tile.
- **publish date / recency**: ABSENT — no date, "ago", or recency string in
  any tile. Grid order is the only recency signal on this surface; first-seen
  tracking or the deep tier must supply publish timing.
- **thumbnail**: present (`thumbnailViewModel`), not evaluated further.

Tile-count note: regex short-id extraction and tile-renderer count agreed
exactly per channel (48/13/48), so the tile payload is the same population the
existing enumeration route sees. Whether GentsScents' 13 tiles is that
channel's full Shorts count or an initial-page cap was not determined (out of
probe bounds); continuation requests exist for deeper history and were
deliberately not exercised.

## Per-Video View Capture Proof (grid vs deep tier, same videos)

| Video | Grid display text (tile) | Watch-page exact count | Watch-page source path |
|---|---|---|---|
| iG92pxnu7J4 | `1.5K views` | 1,597 | `ytInitialPlayerResponse.videoDetails.viewCount` |
| vwT__IK7XGU | `5.2K views` | 5,263 | `ytInitialPlayerResponse.videoDetails.viewCount` |

Per-video view capture from the grid is proven, with the exactness caveat:
grid views are display-rounded; the deep (watch-packet) tier remains the
exact-count source. Any YT view-spike rule computed on grid values operates on
quantized numbers (e.g. a 1.5K→1.6K step is the smallest observable move at
that scale). Whether that quantization is acceptable for the spike trigger is
an owner product-parameter decision, surfaced here and not resolved.

## Run 2: Full-Fidelity Evidence Commit (owner-requested)

Everything capturable from the probe surfaces is persisted raw in the lake as
one SourceCapturePacket (probe-scoped surface; every existing YouTube consumer
filters on `source_surface` and skips it, verified in
`youtube_watch_packet_metric_document.py` / `behavioral_projection.py`):

- Lake packet: `raw/f16/01KWHV1Q2E48SS4A9QXGRR90B5` (`ORCA_DATA_ROOT` =
  `F:\orca-data-lake`), `source_family: youtube`,
  `source_surface: yt_shorts_channel_grid_probe_v0`.
- Contents (12 staged artifacts + writer manifest/receipt): per channel the
  raw served grid HTML, the FULL parsed `ytInitialData`, and the COMPLETE
  tile renderer JSON; per comparison video the raw watch-page HTML; plus the
  probe manifest with per-request status, final URL, byte size, sha256,
  timestamps.
- Raw sha256 anchors: grid JeremyFragrance `f19e5bf8…`, grid GentsScents
  `202f7dc8…`, grid Redolessence `676da6b8…`, watch iG92pxnu7J4 `94f60d39…`,
  watch vwT__IK7XGU `cd89d15a…` (full hashes in the packet's
  `probe_manifest.json`).
- Run 2 reproduced Run 1: same tile counts (48/13/48), zero wall signals,
  views-only tile fields. Date-absence strengthened: a key scan over the
  three COMPLETE persisted tile payloads (all 109 tiles) found zero
  date-bearing keys (`publishedTimeText`/`publishDate`/`dateText`/
  `uploadDate`) — publish timing is definitively not on this surface.
- Deep-tier date proof: both watch pages expose exact `publishDate`
  (iG92pxnu7J4: `2026-07-02T02:00:05-07:00`; vwT__IK7XGU:
  `2026-07-02T01:57:35-07:00`) — publish timing is a deep-tier field.
- Incidental spike-relevant observation: between runs (~17 min), exact watch
  views moved 1,597 → 1,658 and 5,263 → 5,940 on these same-day-published
  Shorts; the grid's rounded text ("1.5K"/"5.2K" at Run 1) is the coarse
  signal a grid-tier spike rule would see.

## Comparison: IG /reels/ grid (code + committed-artifact read; not probed)

Basis: `orca-harness/source_capture/ig_reels_grid_capture.py` (blob `51f18fab`),
`orca-harness/runners/run_source_capture_ig_reels_grid_packet.py` (blob
`339f18d8`), `orca-harness/source_capture/ig_reels_grid.py`, all re-verified at
`origin/main cf43db5f`.

- Access posture: logged-out headless-browser page load of
  `instagram.com/<handle>/reels/`; one page load, no item fan-out; passive
  page-load JSON preserved (`clips/user`, `web_profile_info`, profile feed).
- Per-item fields (joined by shortcode from passive JSON):
  **view/play count** (`video_or_play_count` from
  `play_count`/`video_view_count`/`view_count`/`ig_play_count` keys),
  **like_count**, **comment_count**, taken-at timestamp, pinned flags.
  DOM tiles additionally carry per-tile numeric display text.
- Profile-level: follower_count and profile metadata from `web_profile_info`.
- Registry state: IG metrics are already grid-fed via this path (grid →
  projection → producer); honest per-row gap postures (`no_passive_json_join_
  for_shortcode` etc.) are recorded rather than zero-filled.
- Consequence: the owner's IG spike rule (view / like / comment) is satisfiable
  from the existing grid tier alone.

## Comparison: TikTok profile grid (code + committed-artifact read; not probed)

Basis: `orca-harness/runners/run_source_capture_tiktok_video_packet.py` (blob
`e0c10ad7`, re-verified), `orca-harness/source_capture/tiktok/admission.py`,
`batch_packet.py`, `live_batch_probe.py`, and the committed receipt
`docs/workflows/tiktok_sessioned_profile_grid_dom_receipt_v0.md`.

- Access posture: SESSIONED (dedicated non-personal account, human login) per
  the committed N=1 receipt; the lean runner consumes page-owned artifacts
  rather than automating TikTok. This differs from YT/IG's logged-out posture.
- Per-item fields (profile grid feed `/api/post/item_list/`, `stats`/`statsV2`):
  **playCount**, **diggCount** (likes), **commentCount**, **shareCount**,
  **collectCount**, plus createTime. Fully engagement-bearing per item.
- Registry state: zero TT accounts in the roster (none added by this lane);
  grid depth/scale beyond N=1 remains an open residual per the receipt.
- Consequence: the owner's TT spike rule (view / like / comment) is
  satisfiable from the grid surface the existing code already parses, subject
  to the sessioned posture and unmeasured depth/scale.

## Cross-Platform Grid-Tier Summary

| Surface | Access posture | Views/tile | Likes/tile | Comments/tile | Publish timing/tile | Evidence basis |
|---|---|---|---|---|---|---|
| YT `@channel/shorts` grid | logged-out HTTP | Yes (rounded text) | No | No | No (grid order only) | live probe (this doc) |
| IG `/reels/` grid | logged-out browser + passive JSON | Yes (numeric) | Yes | Yes | Yes (taken_at) | code + committed captures |
| TT profile grid | sessioned | Yes (numeric) | Yes (digg) | Yes | Yes (createTime) | code + committed receipt |

## Cost Shape (arithmetic projection, not a validated claim)

One logged-out HTTP GET per channel per day covers that channel's most-recent
Shorts tiles (up to 48 observed) with per-video views — versus one watch-page
fetch PER VIDEO on the deep tier. For the current 30-channel YT roster at the
probe's 12–15 s pacing, a daily grid sweep is ~30 requests over ~6–8 minutes.
This is arithmetic from the probe's per-request observations; a full-roster
sweep was NOT run (out of this lane's bounds) and no operating-envelope claim
is made.

## Gaps, Risks, And Honest Limits

- **Rounded grid views**: K/M-scale quantization bounds the smallest
  observable view delta; spike semantics on rounded values are an owner call.
  Never precision-inflate grid values into exact counts.
- **No per-tile publish date on YT**: new-content detection must rely on grid
  order + first-seen diffing against prior captures, or defer timing to the
  deep tier.
- **Tile depth**: 48 tiles max observed per initial fetch; older history needs
  continuation requests (existence recorded; deliberately not exercised or
  built).
- **N=3 probe**: route viability is proven on 3 roster channels on one day
  under `curl_cffi:chrome`; logged-out posture can change on YouTube's side at
  any time. The existing stop-on-first-wall discipline should carry into any
  future producer.
- **Handle currency**: probing by channel-id URL avoided the ledger's
  handles-are-labels caveat; a producer should do the same.
- **TT posture asymmetry**: TT grid richness is real but sits behind a
  sessioned route with unmeasured depth/scale; do not treat the three
  platforms' grid tiers as posture-equivalent.

## Non-Claims

- Not an implementation, producer, Silver lane, registry change, or scheduler.
- Not a spike-threshold decision or spike-rule design.
- Not validation, readiness, acceptance, or an operating-envelope claim.
- Not proof the YT grid route will keep working logged-out.
- Not a full-roster sweep, not IG/TT live probes, not TT roster admission.
- The linkage ledger and observation ledger were read-only inputs; no ledger
  edits.
