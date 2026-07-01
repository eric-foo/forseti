# TikTok Sessioned DOM Hydration Profile Comments Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Live probe receipt
authority_boundary: retrieval_only
scope: >
  Sessioned TikTok DOM/hydration harvest for the locked @tiktok source-family
  fixture. Records profile-grid depth, video-detail hydration, and visible
  top-level comment DOM captured from one human-logged-in Chrome session without
  reading, exporting, or writing session secrets.
use_when:
  - Recovering the largest current sessioned DOM/profile/comment evidence batch
    before attempting packet-grade page-response capture.
  - Selecting a low-cost 5-video rung from observed @tiktok grid anchors.
  - Distinguishing DOM/hydration availability from packet-grade /api/comment/list
    response-body availability.
stale_if:
  - A later TikTok live probe changes route, challenge posture, selector shape,
    comment-list response capture, grid depth, or per-account ceiling.
  - `tiktok_capture_lane_spec_v0.md`, `tiktok_first_slice_probe_recon_v0.md`, or
    `tiktok_sessioned_capture_warm_probe_plan_v0.md` changes materially.
```

## Verdict

`PARTIAL_GO / sessioned DOM + hydration harvest expanded; packet-grade comments still unproven`.

The same sessioned Chrome/TikTok tab loaded both the pinned video fixture and the
`@tiktok` profile without visible login, slider challenge, or verification
markers. The profile route exposed `webapp.user-detail`, stable profile selectors,
and 94 unique visible grid video anchors after bounded scrolling. The pinned
video route exposed `webapp.video-detail`, exact video `createTime`, raw stats,
music metadata, mention metadata, and 20 visible top-level comment DOM rows.

This is still not packet-grade comment capture. The Chrome surface used here did
not expose `/api/comment/list` response bodies, so `cid`, `uid`, exact comment
`create_time`, cursor, and `has_more` remain unproven under the sessioned route.

## Authorization And Secret Boundary

- Current owner authorization: live sessioned DOM/hydration run authorized in
  this lane after the dedicated TikTok login was completed by the owner.
- Browser posture: one existing TikTok Chrome tab reused; no duplicate TikTok tab
  was created.
- Login: human-performed; the agent did not enter credentials.
- Secrets: no cookies, storage state, credentials, tokens, proxy endpoints, exit
  IPs, or storage snapshots were read, copied, exported, written, or included.
- Content boundary: public `@tiktok` profile and public pinned video fixture.
- Stop rule: stop on challenge; no CAPTCHA solving.

## Targets

- Profile: `https://www.tiktok.com/@tiktok`
- Pinned video: `https://www.tiktok.com/@tiktok/video/7642770753292635422`
- Date: 2026-06-30
- Structured payload:
  `docs/workflows/tiktok_sessioned_dom_hydration_profile_comments_payload_v0.json`

## Profile Observation

Observed after returning to the profile in the same tab and performing bounded
profile-grid scrolls:

```json
{
  "url": "https://www.tiktok.com/@tiktok",
  "title": "TikTok (@tiktok) | TikTok",
  "challengeMarkers": {
    "hasLoginText": false,
    "hasSliderChallenge": false,
    "hasVerifyText": false
  },
  "selectorCounts": {
    "userTitle": 1,
    "userSubtitle": 1,
    "userBio": 1,
    "userLink": 1,
    "userPostItem": 95,
    "videoViews": 95
  },
  "grid": {
    "uniqueAnchorCount": 94,
    "firstVideoId": "7655821093684448542",
    "lastVideoId": "7595247839345741086"
  }
}
```

`#__UNIVERSAL_DATA_FOR_REHYDRATION__` was present with `webapp.user-detail`.
Observed profile fields:

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

Visible DOM values:

| Selector | Observed text |
| --- | --- |
| `data-e2e="user-title"` | `TikTok` |
| `data-e2e="user-subtitle"` | `tiktok` |
| `data-e2e="user-bio"` | `One TikTok can make a big impact` |
| `data-e2e="user-link"` | `linktr.ee/tiktok` |

The full 94-row grid anchor payload is in
`tiktok_sessioned_dom_hydration_profile_comments_payload_v0.json`.

## Video Observation

The pinned video route exposed `#__UNIVERSAL_DATA_FOR_REHYDRATION__` with
`webapp.video-detail`.

```json
{
  "id": "7642770753292635422",
  "createTime": "1779471253",
  "author": {
    "id": "107955",
    "uniqueId": "tiktok",
    "nickname": "TikTok",
    "verified": true,
    "privateAccount": false
  },
  "stats": {
    "collectCount": "967",
    "commentCount": 1256,
    "diggCount": 10500,
    "playCount": 295100,
    "shareCount": 908
  },
  "statsV2": {
    "collectCount": "967",
    "commentCount": "1256",
    "diggCount": "10500",
    "playCount": "295100",
    "repostCount": "0",
    "shareCount": "908"
  },
  "music": {
    "id": "7642770792052280095",
    "title": "original sound",
    "authorName": "TikTok",
    "original": true,
    "duration": 54
  },
  "textExtra": [
    {
      "type": 0,
      "userId": "205879097384816641",
      "userUniqueId": "zaralarsson"
    }
  ]
}
```

The video description and full comment rows are preserved in the structured
payload with non-ASCII source text escaped as JSON.

## Comment DOM Observation

The comments control opened in the same sessioned tab. A bounded comment-panel
scroll did not expand the visible sample beyond the first 20 top-level rows.

```json
{
  "challengeMarkers": {
    "hasLoginText": false,
    "hasSliderChallenge": false,
    "hasVerifyText": false
  },
  "selectorCounts": {
    "comments": 1,
    "commentLevel1": 20,
    "commentUsername1": 20,
    "commentReply1": 20,
    "commentInput": 1,
    "commentPost": 1,
    "commentText": 1,
    "commentCount": 2,
    "commentIcon": 2
  },
  "comments": {
    "topLevelCount": 20,
    "uniqueProfileHrefCount": 20
  }
}
```

The visible DOM fields per row are: display username, profile handle from public
profile link, public comment text, visible date string, visible like text, and
visible reply-expansion count when present. The date strings are DOM-visible
display strings, not exact timestamps.

## API Capture Boundary

`/api/comment/list` is not a public API route to call directly. It is TikTok's
page-owned web endpoint: the browser page issues a signed request after the
comments surface opens. The lane target is the response body from that
page-owned request, not a forged direct request.

The live Chrome control surface did not provide response-body access for
page-owned XHR/fetch traffic. The available Chrome tab capability exposed page
assets, not XHR bodies, and the page-scope resource check did not yield
packet-grade `/api/comment/list` bodies.

### Existing Chrome Follow-Up Diagnostic

A later same-day follow-up reused the already-running user Chrome session
instead of launching a new Playwright browser. The pinned video tab was clean:
no visible login gate, no visible slider/captcha/verify marker, and comments
rendered after clicking `Read or add comments 1256 comments`.

Observed through the supported Chrome extension surface:

- `pageAssets` was the only extra tab capability; it inventoried scripts,
  images, stylesheets, fonts, and video assets, not XHR/fetch response bodies.
- After comments opened, `pageAssets` showed the comment sidebar script but no
  comment-list response body surface.
- The read-only page evaluation scope did not expose `performance` or resource
  timing entries, so a page-generated `/api/comment/list` URL could not be
  recovered there.
- A bounded DOM/React-object scan found visible comment handles/text/date strings
  but no hidden `cid`, commenter `uid`, exact `create_time`, cursor, or
  `has_more`.
- No raw signed URL, cookies, storage state, tokens, headers, or raw response
  body were printed or written.

Therefore this receipt does not claim any of:

- comment `cid`
- commenter `uid`
- exact comment `create_time`
- `cursor`
- `has_more`
- raw `/api/comment/list` response bytes/hash

## Interpretation

- The sessioned route is clean for public profile DOM, profile hydration, video
  hydration, and first-page visible comment DOM on this locked fixture.
- Existing user Chrome is a good manual/session surface for TikTok rendering,
  but the current Chrome-extension automation surface is not a packet-grade
  response-body capture surface.
- The profile-grid route has enough observed anchors to seed a low-cost 5-video
  rung without extra discovery.
- Visible grid view counts are abbreviated display text and should not be treated
  as exact numeric views.
- Visible comment dates are lower fidelity than the spec target; exact comment
  timestamps still depend on `/api/comment/list` response bodies.
- More DOM probing is no longer the highest-value next step. The remaining
  bottleneck is response-body capture from the page-owned comment request.

## Non-Claims

- Not packet-grade comment capture.
- Not proof of `cid`, `uid`, exact comment `create_time`, cursor, or `has_more`.
- Not a per-account ceiling or scale run.
- Not a full profile-grid pagination/deep-history proof.
- Not exact grid-view normalization.
- Not transcript, ASR, source-native caption, durable media, or durable audio
  evidence.
- Not TikTok implementation readiness.
- Not legal advice.

## Next Material Batch

1. Run the pinned fixture through the harness path that can observe page-owned
   responses: `fetch_browser_page_observation_capture` with the post-load
   comment-panel action and a `/api/comment/list` response predicate.
2. Require one preserved response body with exact comment packet fields before
   any broader ladder: `cid`, `text`, `create_time`, `digg_count`,
   `reply_comment_total`, `user.uid`, `user.unique_id`, `user.nickname`,
   `cursor`, and `has_more`.
3. If the pinned packet run succeeds, use the profile payload's grid anchors for
   the 5-video rung at human cadence, stop on the first challenge, and update the
   ceiling ledger.
4. Do not repeat DOM-only Chrome-extension probing for packet proof; use a
   supported response-body capture surface or stop with the body-access blocker.
