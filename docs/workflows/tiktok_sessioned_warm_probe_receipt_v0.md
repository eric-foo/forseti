# TikTok Sessioned Warm Probe Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Live probe receipt
authority_boundary: retrieval_only
scope: >
  Narrow N=1 sessioned TikTok warm-probe receipt for the pinned first-slice
  fixture. Records visible browser/session behavior, embedded metadata parsing,
  and comment-surface availability without inspecting cookies, storage state, or
  credentials.
use_when:
  - Checking whether the dedicated-session TikTok route clears the public-route
    slider/login blocker for the pinned fixture.
  - Distinguishing sessioned UI/DOM availability from the exact page-XHR packet
    contract and per-account ceiling measurement.
  - Deciding the next sessioned batch: response-capture harness, 5-video ladder,
    or blocker.
stale_if:
  - A later TikTok live probe updates sessioned route, challenge posture,
    comment-response capture, packet fields, or per-account ceiling.
  - `tiktok_sessioned_capture_warm_probe_plan_v0.md`,
    `tiktok_capture_lane_spec_v0.md`, `tiktok_first_slice_probe_recon_v0.md`,
    or the capture playbook changes materially.
```

## Verdict

`PARTIAL_GO / sessioned N=1 UI route clean; exact packet contract unproven`.

The human-logged-in browser session loaded the pinned TikTok fixture without a
visible login wall, slider challenge, or verify prompt. The page-owned
`#__UNIVERSAL_DATA_FOR_REHYDRATION__` video-detail blob parsed successfully.
After clicking the visible comments control, the comment surface rendered visible
comment DOM nodes.

The run did not capture `/api/comment/list` response bodies and therefore did
not prove `cid`, `uid`, exact `create_time`, cursor, or `has_more` fields in this
sessioned run. It also did not measure a per-account ceiling beyond one clean
fixture.

## Authorization And Secret Boundary

- Current owner authorization: sessioned run authorized after the public route
  hit a strong no-login/challenge posture.
- Login: human-performed in Chrome before the probe.
- Account premise: dedicated non-personal account, per owner-ready signal.
- Secrets: no cookies, storage state, credentials, tokens, proxy endpoints, or
  exit IPs were read, copied, exported, written, or included in this receipt.
- Content boundary: public TikTok video only.
- Stop rule: stop on challenge; no CAPTCHA solving.

## Target

- URL: `https://www.tiktok.com/@tiktok/video/7642770753292635422`
- Fixture source:
  `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_first_slice_probe_recon_v0.md`
- Browser session label: `TikTok sessioned probe`
- Date: 2026-06-30
- Batch size: `1`

## Pre-Target Session Signal

Visible logged-in session behavior was checked without cookie/storage reads.

Observed sanitized signals before navigating to the fixture:

```json
{
  "url": "https://www.tiktok.com/foryou?lang=en",
  "title": "Watch trending videos for you | TikTok",
  "signals": {
    "loginPage": false,
    "hasLoginText": false,
    "hasForYou": true,
    "hasFollowing": true,
    "hasUpload": true,
    "hasSliderChallenge": false
  }
}
```

## Video Metadata Observation

On the pinned fixture, the page-owned embedded metadata blob was present and
parsed.

Observed summary:

```json
{
  "id": "7642770753292635422",
  "authorUniqueId": "tiktok",
  "authorId": "107955",
  "createTime": "1779471253",
  "descLength": 91,
  "textExtraCount": 1,
  "commentsInlineCount": 0,
  "stats": {
    "collectCount": "966",
    "commentCount": 1256,
    "diggCount": 10500,
    "playCount": 295100,
    "shareCount": 908
  },
  "statsV2": {
    "collectCount": "966",
    "commentCount": "1256",
    "diggCount": "10500",
    "playCount": "295100",
    "repostCount": "0",
    "shareCount": "908"
  }
}
```

No slider challenge, verify text, or login text was visible after target load.

## Comment Surface Observation

The visible comment control was uniquely resolved by accessible name:

`Read or add comments\n1256 comments`

After clicking it, the page still showed no slider challenge, verify text, or
login text. The comment surface rendered visible DOM nodes including:

- a `1256 comments` header
- visible first-page comment containers
- `data-e2e="comment-username-1"` nodes
- `data-e2e="comment-level-1"` nodes
- `data-e2e="comment-reply-1"` nodes
- an add-comment placeholder/surface

The DOM surface carries public comment text and relative dates, but it does not
provide the exact packet-grade fields required by the spec. This receipt
therefore records comment-surface availability, not comment-packet completion.

## Interpretation

- Sessioned browser state cleared the immediate public-route blocker for this
  pinned fixture.
- Metadata remains available from the page-owned embedded video-detail blob.
- Comment UI availability is better under the sessioned route than the 2026-06-30
  public diagnostic, which stopped on a visible slider challenge before comment
  capture.
- Exact comment packet capture is still the next technical bottleneck because
  this browser-control pass did not preserve `/api/comment/list` responses.
- Per-account ceiling remains unmeasured beyond `N=1`.

## Non-Claims

- Not a full warm-probe ladder.
- Not a measured per-account ceiling.
- Not sessioned packet-contract validation.
- Not proof of `cid`, `uid`, exact `create_time`, cursor, or `has_more` fields
  for this sessioned run.
- Not scale reliability evidence.
- Not transcript, ASR, source-native caption, durable audio, or durable video
  evidence.
- Not legal advice.
- Not implementation readiness.

## Next Compounding Step

Run the smallest packet-grade sessioned batch:

1. Use the same dedicated-session boundary, without exposing or storing secrets.
2. Capture page-owned `/api/comment/list` responses through the existing browser
   response-capture primitive or a bounded harness wrapper.
3. Re-run the pinned fixture and require exact metadata plus at least first-page
   comment packet fields (`cid`, `text`, `create_time`, `user.uid`,
   `user.unique_id`, `digg_count`, `reply_comment_total`, `cursor`, `has_more`).
4. Stop on any challenge.
5. Only after packet fields are proven should the lane advance to a 5-video
   ceiling rung.
