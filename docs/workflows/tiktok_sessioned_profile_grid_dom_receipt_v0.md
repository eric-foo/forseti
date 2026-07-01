# TikTok Sessioned Profile Grid DOM Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Live probe receipt
authority_boundary: retrieval_only
scope: >
  Narrow sessioned TikTok creator/profile grid DOM receipt for the locked @tiktok
  source-family fixture. Records profile hydration fields, stable DOM selectors,
  grid permalink IDs, and challenge/login posture without reading cookies,
  storage state, credentials, or tokens.
use_when:
  - Checking whether the TikTok profile/listing grid route works under the
    current dedicated session.
  - Recovering the DOM selectors and grid identity anchors already named by the
    TikTok first-slice lane.
  - Distinguishing sessioned profile-grid visibility from full warm-probe
    ceiling or packet-grade comment capture.
stale_if:
  - A later TikTok live probe updates profile/grid selector behavior, challenge
    posture, grid depth, profile fields, or permalink identity anchors.
  - `tiktok_first_slice_probe_recon_v0.md`, `tiktok_capture_lane_spec_v0.md`,
    `tiktok_sessioned_capture_warm_probe_plan_v0.md`, or the capture playbook
    changes materially.
```

## Verdict

`GO / sessioned N=1 profile-grid DOM route clean; depth and scale unmeasured`.

The existing human-logged-in TikTok session loaded `https://www.tiktok.com/@tiktok`
without a visible login wall, slider challenge, or verify prompt. The profile page
exposed `#__UNIVERSAL_DATA_FOR_REHYDRATION__` with `webapp.user-detail`, stable
profile DOM selectors, and visible grid item anchors.

This is not a full warm-probe ladder and not comment packet validation.

## Source Basis

The lane already specified this route:

- `tiktok_first_slice_probe_recon_v0.md` says Profile page Route 1 is GO via
  `data-e2e` selectors: `user-title`, `user-bio`, `user-link`, `user-post-item`,
  and `video-views`, with video permalinks carrying real numeric IDs.
- `tiktok_logged_out_first_slice_probe_plan_v0.md` locks the subject as
  `https://www.tiktok.com/@tiktok` and treats one profile plus one video/comments
  first slice as the bounded route-existence check.
- `tiktok_behavioral_gap_ledger_from_ig_youtube_v0.md` kept sessioned profile
  grid behavior as a live residual; this receipt closes the N=1 sessioned DOM
  route check, not the scale/depth residual.

## Authorization And Secret Boundary

- Current owner authorization: sessioned live run authorized.
- Login: human-performed before the probe.
- Account premise: dedicated non-personal account.
- Secrets: no cookies, storage state, credentials, tokens, proxy endpoints, or
  exit IPs were read, copied, exported, written, or included in this receipt.
- Content boundary: public TikTok creator profile only.
- Stop rule: stop on challenge; no CAPTCHA solving.

## Target And Session

- URL: `https://www.tiktok.com/@tiktok`
- Browser session label: `TikTok sessioned grid`
- Date: 2026-06-30
- Batch size: one profile page, no scrolling beyond settled loaded state

## Visible Route Signals

```json
{
  "url": "https://www.tiktok.com/@tiktok",
  "title": "TikTok (@tiktok) | TikTok",
  "visibleSignals": {
    "hasLoginText": false,
    "hasSliderChallenge": false,
    "hasVerifyText": false,
    "hasUserTitle": true,
    "hasUserBio": true,
    "hasUserLink": true,
    "hasPostItems": true
  }
}
```

## Hydration Profile Fields

`document.getElementById("__UNIVERSAL_DATA_FOR_REHYDRATION__")` was present and
parsed. The profile data lived under `webapp.user-detail`.

Observed profile summary:

```json
{
  "id": "107955",
  "uniqueId": "tiktok",
  "nickname": "TikTok",
  "verified": true,
  "privateAccount": false,
  "signatureLength": 32,
  "stats": {
    "diggCount": 0,
    "followerCount": 94600000,
    "followingCount": 3,
    "friendCount": 1,
    "heart": 461000000,
    "heartCount": 461000000,
    "videoCount": 1463
  }
}
```

## DOM Selector Evidence

Observed selector counts:

```json
{
  "userTitle": 1,
  "userBio": 1,
  "userLink": 1,
  "userPostItem": 31,
  "videoViews": 31,
  "videoAnchorsStructuredSample": 24
}
```

Observed profile DOM values:

| Selector | Observed text |
| --- | --- |
| `data-e2e="user-title"` | `TikTok` |
| `data-e2e="user-subtitle"` | `tiktok` |
| `data-e2e="user-bio"` | `One TikTok can make a big impact` |
| `data-e2e="user-link"` | `linktr.ee/tiktok` |

The browser DOM snapshot excerpt also contained `@tiktok/video/` URLs for the
same visible grid. This receipt records structured grid anchors below instead of
copying a full DOM snapshot.

## Structured Grid Sample

The structured sample captured the first 24 unique visible `@tiktok/video/`
anchors and their visible grid view text.

| # | video_id | view_text |
| --- | --- | --- |
| 1 | `7655821093684448542` | `122.3K` |
| 2 | `7655739740422950174` | `87K` |
| 3 | `7655732127413112095` | `28M` |
| 4 | `7655021741516885279` | `79.3K` |
| 5 | `7654716883307990302` | `472.1K` |
| 6 | `7654341587425692942` | `32.1M` |
| 7 | `7653150706425138446` | `153.2K` |
| 8 | `7652870361331043614` | `282.6K` |
| 9 | `7651659857640033566` | `177.4K` |
| 10 | `7650608519288245534` | `168.7K` |
| 11 | `7650573331304860958` | `27.4M` |
| 12 | `7650547481587109150` | `5.6M` |
| 13 | `7650300237860424990` | `6.4M` |
| 14 | `7649091368656194847` | `182.3K` |
| 15 | `7647963131938901278` | `13.2M` |
| 16 | `7646496890783010078` | `191.6K` |
| 17 | `7645395404045028639` | `46.7M` |
| 18 | `7645356725259865375` | `7.2M` |
| 19 | `7644982860780260639` | `50.3M` |
| 20 | `7644644020869811486` | `156.9K` |
| 21 | `7644289514600451358` | `12.6M` |
| 22 | `7642770753292635422` | `295.1K` |
| 23 | `7642540102207524126` | `151.3K` |
| 24 | `7642519488302222622` | `143.6K` |

The DOM snapshot evidence excerpt showed additional `@tiktok/video/` URLs beyond
this 24-row structured sample, but this receipt keeps the sample bounded.

## Interpretation

- Sessioned profile-grid DOM route is live-clean for the locked `@tiktok` fixture.
- The profile page carries both embedded profile stats and visible DOM selectors.
- Grid identity should use video permalink IDs, not visible position.
- Visible grid view text is source-visible but abbreviated; exact numeric view
  count availability for grid items is not proven by this receipt.
- This receipt closes the narrow missing sessioned profile-grid/DOM check. It
  does not close sessioned packet-grade comments, grid pagination/depth, field
  drift, or per-account ceiling.

## Non-Claims

- Not a full TikTok warm-probe ladder.
- Not packet-grade comment capture.
- Not exact grid-view-count normalization.
- Not profile-grid pagination/deep-history proof.
- Not scale reliability evidence.
- Not transcript, ASR, source-native caption, durable audio, or durable video
  evidence.
- Not legal advice.
- Not implementation readiness.

## Next Compounding Step

Use this receipt as the profile/listing-grid half of the sessioned first slice.
The remaining packet-grade bottleneck is still page-owned `/api/comment/list`
response capture for the pinned video, with exact comment fields and no secret
persistence.
