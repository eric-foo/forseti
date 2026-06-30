# TikTok Public Route Live Diagnostic Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Live diagnostic receipt
scope: >
  Narrow public-route diagnostic for the pinned TikTok first-slice fixture after
  the TikTok behavior-sync handoff. Records what the current public browser route
  exposed before the run hit a TikTok slider challenge.
use_when:
  - Checking whether the pinned TikTok video-detail route still exposes
    page-embedded metadata in a public browser render.
  - Distinguishing public-route diagnostics from the sessioned warm-probe plan.
  - Preserving the stop-on-challenge outcome from the 2026-06-30 live run.
stale_if:
  - A later TikTok live probe updates the public route, access posture, comment
    route, challenge posture, or data contract.
  - `tiktok_capture_lane_spec_v0.md`, `tiktok_first_slice_probe_recon_v0.md`,
    `tiktok_sessioned_capture_warm_probe_plan_v0.md`, or the capture playbook
    changes materially.
```

## Verdict

`PARTIAL / public-route challenge-gated`.

The pinned TikTok video page still rendered and exposed the page-owned
`#__UNIVERSAL_DATA_FOR_REHYDRATION__` metadata blob for the fixture video. The
same visible page state also showed a TikTok slider challenge: "Drag the slider
to fit the puzzle." The run stopped there. No login was attempted, no modal was
closed, no CAPTCHA was solved, no comments were opened or harvested, and no
sessioned ceiling was measured.

This is not a sessioned warm-probe result.

## Target

- URL: `https://www.tiktok.com/@tiktok/video/7642770753292635422`
- Source-family fixture: pinned from
  `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_first_slice_probe_recon_v0.md`
- Run posture: Chrome extension-controlled real browser, public route diagnostic,
  no credential entry, no session setup, no account label
- Browser session label: `TikTok public diagnostic`
- Date: 2026-06-30

## Observed Page State

- Final URL remained:
  `https://www.tiktok.com/@tiktok/video/7642770753292635422`
- Page title:
  `Midnight Sun: Zara Larsson-Inspired Remix Night | TikTok`
- Visible route signals included:
  - `Comments`
  - `You may like`
  - `Log in`
  - `Drag the slider to fit the puzzle`
- A visible `Close` control existed on the challenge/modal surface, but it was
  not pressed because the visible state was a slider challenge, not merely a
  login gate.

## Embedded Metadata Blob

`document.getElementById("__UNIVERSAL_DATA_FOR_REHYDRATION__")` was present and
parsed.

Observed `webapp.video-detail.itemInfo.itemStruct` summary:

```json
{
  "id": "7642770753292635422",
  "authorUniqueId": "tiktok",
  "authorId": "107955",
  "createTime": "1779471253",
  "desc": "Shout out all the iconic @Zara Larsson stans who helped inspire Midnight Sun: Girls Trip",
  "textExtraCount": 1,
  "commentsInlineCount": 0,
  "stats": {
    "collectCount": "966",
    "commentCount": 1256,
    "diggCount": 10500,
    "playCount": 295000,
    "shareCount": 908
  },
  "statsV2": {
    "collectCount": "966",
    "commentCount": "1256",
    "diggCount": "10500",
    "playCount": "295000",
    "repostCount": "0",
    "shareCount": "908"
  }
}
```

The description above omits a trailing emoji from the visible/source text for
ASCII receipt hygiene.

## Interpretation

- Public video-detail metadata remains route-visible in a real browser render.
- The public route is not reliable enough to treat as a sustained capture route:
  the diagnostic immediately encountered a visible TikTok slider challenge.
- Comments were not proven in this run. The page displayed a comment count and a
  `Comments` surface, but the comment-list response was not captured or parsed.
- The result is consistent with the current lane direction: logged-out/public
  TikTok is brittle; the sessioned/cookied dedicated-account warm-probe remains
  the measurement route for per-account ceiling and comment-route survivability.

## Non-Claims

- Not a sessioned warm-probe.
- Not account-ceiling evidence.
- Not scale reliability evidence.
- Not comment-route validation for this run.
- Not transcript, ASR, source-native caption, durable audio, or durable video
  evidence.
- Not source-access approval beyond this bounded public diagnostic.
- Not legal advice.
- Not implementation readiness.

## Next Decision

The next compounding move remains the sessioned warm-probe only after the
dedicated-account prerequisites are real:

- dedicated non-personal TikTok account
- human-performed login
- warmed session
- account-ban risk acceptance for that account
- public content only
- no credential, cookie, storage-state, token, proxy endpoint, or exit-IP
  persistence
- stop on challenge

Until then, public-route diagnostics can only report partial public visibility
and challenge posture; they should not be promoted into a capture readiness
claim.
