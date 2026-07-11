```yaml
retrieval_header_version: 1
artifact_role: capture recon finding + capture-path behavior spec (non-authorizing)
scope: >
  Instagram `/reels/` grid DOM engagement plus passive page-load JSON capture contract for
  low-interaction creator monitoring. Records the current no-hover DOM finding, `/clips/user`
  source-surface finding, viewport/zoom boundaries, creator snapshot implications, and
  code-enforceable capture-path rules. Projection, scoring, classification, and storage policy
  are explicitly deferred.
use_when:
  - Scoping IG-only creator monitoring from public `/reels/` grids.
  - Deciding which fields the capture runner may emit before projection.
  - Checking what code can enforce for low-footprint capture and visible failure handling.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_capture_findings_consolidated_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_reel_viewcount_capture_feasibility_recon_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
stale_if:
  - IG `/reels/` media anchors stop carrying no-hover numeric leaf text for visible reels.
  - A fresh logged-out/proxy probe contradicts the 2026-06-22 `/reels/` route observations.
  - A fresh probe contradicts the 2026-06-22 `/api/v1/clips/user/` source-surface observations.
  - A runner implementation supersedes this capture-path contract and its source-surface labels.
status: RECON_GO_NO_HOVER_REELS_DOM__REELS_CLIPS_JSON_DIRECTIONAL__OPTIMIZED_RUNNER_WIRED__OLD_CALLS_RUNNER_LEGACY__STATIC_COMPARISON_POLICY_DEFERRED__PROJECTION_DEFERRED
```

# IG Profile-Grid DOM Engagement Recon And Spec (v0)

This is a capture-spine source-family spec, not a runner implementation, projection contract,
classification policy, validation record, legal opinion, stealth guidance, or readiness claim.
It is limited to public Instagram `/reels/` grid observations and safe route metadata.

## Runner Binding

`forseti-harness/runners/run_source_capture_ig_reels_grid_packet.py` is the optimized default
Source Capture Armory runner for public IG creator monitoring. It supersedes
`forseti-harness/runners/run_source_capture_ig_calls_packet.py` for steady-state monitoring because it
uses one `/reels/` page load, no hover/click/item-page fan-out, no OCR, and passive JSON capture
joined by shortcode. The old calls runner remains a legacy calibration or fallback route when
item-page OG metadata is explicitly needed.

The optimized runner supports `--output` for scratch packets and `--data-root` /
`FORSETI_DATA_ROOT` (legacy `ORCA_DATA_ROOT` accepted as fallback) for data-lake
raw packet admission. As of the current implementation, the grid runner still exposes
heavy-asset blocking as an implementation behavior. Current daily-heartbeat operating policy is
owned by `ig_daily_heartbeat_operating_policy_v0.md`, which prefers ordinary browser asset loading
for supervised daily heartbeat and treats heavy-asset blocking as an explicit bandwidth mode. Do not
claim code alignment with that policy until a runner patch changes and verifies the default.

## Static Comparison Policy

IG creator monitoring is not reels-only. The high-cadence public monitoring route is `/reels/`
because reels expose views plus likes/comments and usually carry the clearest public traction signal.
Static image/carousel capture is a lower-cadence companion surface for onboarding, periodic refresh,
and escalation because static posts can carry captions, tags, paid-partnership/product hints, likes,
and comments. They lack view count and must not be mixed into the reels traction series.

Daily steady-state heartbeat is separate from onboarding. The daily heartbeat policy governs
registered-creator first-visible-grid monitoring only; onboarding top-band or static/profile-grid
intake rules stay in their own lane.

Static capture must remain a separate thin source surface, not an expansion of the reels runner. Policy:

- high-cadence monitoring: reels traction series
- lower-cadence companion: one static/profile-grid comparison pass during creator onboarding
- periodic refresh: static weekly or every 2-4 monitoring cycles
- escalation: static pass when reels signal is ambiguous or sponsor detection matters

Static `view_count` must be recorded as `not_applicable`, not as missing data.
Implementation note: the optimized reels runner filters `/p/` rows out of the reels traction series and records a limitation when such rows are observed on the reels route. The pure grid normalizer also marks static `/p/` rows with static view-count non-applicability so a separate static comparison surface cannot accidentally promote a visible number into `view_count`.

## Lane Wrap-Up: Code Enforcement And Behavioral Refresh Boundary

The optimized `/reels/` capture lane has two kinds of rules. Code should enforce deterministic packet honesty and privacy boundaries. Behavioral probes should refresh assumptions about Instagram's changing UI, response payloads, and block behavior. Do not move behavioral assumptions into hard correctness claims.

Code-enforceable in this lane:

- Exactly one output target: scratch `--output` or data-lake `--data-root` / `FORSETI_DATA_ROOT` (legacy `ORCA_DATA_ROOT` fallback); an ambient data-root env var must not silently override an explicit `--output`.
- One optimized `/reels/` page-load path for the high-cadence runner; no hover, click, OCR, comment-text capture, media-byte preservation, or item-page fan-out in that runner.
- Response preservation is limited to known passive JSON source surfaces with response-size caps.
- Cookie / `set-cookie` headers, proxy endpoint, proxy credentials, proxy exit IP, proxy store path, and stored browser state are not serialized into packets.
- Source slices carry typed metric observations: observed values only when present; non-observed metrics use typed posture + reason; static/non-video `view_count` is `not_applicable`.
- Missing capture timestamps on source slices remain `unknown_with_reason`; metric coverage windows are omitted rather than filled with prose.
- Row-level limitations roll up to capture-level limitations so packet honesty validation cannot pass only because an unrelated limitation happened to be present.
- Data-lake admission uses lake-owned staging and write-once raw packet publication with availability index readback.
- Projection may carry source-visible metric rows, captions, timestamps, and mechanical surface-mention counts; it must not emit ad, sponsorship, credibility, demand, integrity, or action-ceiling conclusions.

Code-enforceable candidates for the next implementation slice:

- Add an IG creator-grid projection adapter that handles high-cadence reels and lower-cadence static/profile-grid comparison rows while emitting caption text anchors, surface mention candidates, caption-template repetition, and per-capture `caption_surface_mention_frequency` as mechanical projection features.
- Add per-row selected-source audit fields (`join_status`, chosen `source_surface`, selection policy, and selection limitations) if downstream consumers need row-level selection provenance instead of reading the preserved candidates.
- Preserve like/comment count candidate disagreements with the same symmetry already used for view/play count candidates.
- Finish the separate static/profile-grid comparison source surface for onboarding, periodic refresh, or escalation; do not expand the high-cadence reels runner into mixed static capture.

Behavioral refresh required; not code-enforceable as truth:

- Whether Instagram's DOM hidden numeric order still maps to likes then comments for no-hover rows.
- Whether `/clips/user`, `web_profile_info`, or profile-feed JSON continue to appear during ordinary public page load, and which field names carry views/plays, likes, comments, captions, timestamps, paid labels, affiliate flags, and sponsor users.
- Whether a viewport/zoom/browser bucket changes visible row count or passive JSON depth.
- Whether high-frequency creator switching, proxy use, logged-out access, or sessioned access triggers access blocks or automated-behavior warnings at unacceptable rates.
- Whether `is_paid_partnership=false`, empty sponsor users, or missing affiliate flags actually mean "not an ad". They do not; ad/promotional meaning stays Judgment-owned.
- Whether repeated brand/product mentions are paid sponsorship, organic product discussion, campaign behavior, or content-farm cadence. Projection may count mentions; Cleaning may normalize entities; Judgment decides meaning.
- Whether static/carousel posts add enough signal to justify their capture cost for a given monitoring phase.

## Current Finding

A logged-out proxy diagnostic against `https://www.instagram.com/vanzzcoser/reels/` on
2026-06-22 parsed 12 of 12 visible media anchors at both `768x1024` and `1080x1920` without
hover, click, OCR, item-page visits, profile main-grid visits, or scroll. The same high-viewport
attempt at `5204x4728` redirected to a login URL and produced zero anchors, so larger launch
viewports are not treated as better by default.

The no-hover DOM shape for clean rows was:

```yaml
visible_numeric_texts:
  - views_text
hidden_leaf_numeric_texts:
  - likes_text
  - comments_text
  - views_text
hidden_engagement_candidates:
  - likes_text
  - comments_text
```

For this observed shape, `hidden_engagement_candidates[0]` is likes and
`hidden_engagement_candidates[1]` is comments. Code must still preserve the raw leaf list and mark
ambiguous rows instead of silently trusting the order when the shape changes.

## Metadata / Aboutness Boundary

The grid DOM does not tell what the video is about beyond visible reel engagement and permalink
identity. It does not reliably expose caption text, hashtags, audio, topic, sponsor status, or
publish date.

Profile-feed JSON can expose metadata for rows it contains, including `taken_at_timestamp`,
`product_type`, `__typename`, `is_video`, thumbnail-related fields, and `edge_media_to_caption`.
Existing harness code already parses `edge_media_to_caption` into `caption` for profile-feed media
nodes. That caption can provide a weak "what is this about" source when present, but it is not
available for every visible `/reels/` grid row and must not be treated as a complete video-topic
classification.

The 2026-06-22 probes observed multiple JSON source surfaces with different coverage and count
semantics:

- `web_profile_info` / profile-feed style JSON can expose timestamps, captions, product type,
  like/comment counts, and video/play count, but it may only overlap a subset of currently rendered
  `/reels/` grid rows and can carry lower video/play counts than the grid-visible reel view number.
- `/api/v1/clips/user/` page-load JSON returned all 12 target `vanzzcoser` visible-grid shortcodes in
  one 1080x1920 run, including exact timestamps, captions when present, product type, like/comment
  counts, video/play counts, and ad-signal-capable fields.
- In the `jeremyfragrance` CloakBrowser 1920x4000 run, both `/api/v1/users/web_profile_info/` and
  `/api/v1/clips/user/` were observed. For sampled rows, `/api/v1/clips/user/` video/play counts
  matched the DOM-visible view text while `web_profile_info` carried lower video/play counts for the
  same shortcode. Example: `DZ4Stb5MVPB` had DOM `2,984`, `web_profile_info` count `655`, and
  `/clips/user` count `2,984`.

This finding is directional, not a production stability claim. The capture contract must preserve
source provenance and raw candidate values instead of silently choosing a single unqualified
"view" field.

Therefore capture must distinguish:

- `dom_grid_engagement`: visible `/reels/` grid facts from the media-anchor DOM.
- `passive_page_json_metadata`: metadata observed in JSON responses returned by the same page load.
- `clips_user_json_metadata`: metadata observed from `/api/v1/clips/user/` during the page load.
- `web_profile_info_json_metadata`: metadata observed from `/api/v1/users/web_profile_info/` during
  the page load.
- `profile_feed_json_metadata`: metadata from explicit profile-feed JSON fetches, if a later runner
  enables that extra request class.
- `item_page_metadata`: caption/date/comment text from item pages; out of default scope for this
  low-interaction route.

## Required Capture Behavior

Given an explicit public IG handle or `/reels/` URL, the capture route should load the public
`/<handle>/reels/` grid and extract no-hover media-anchor observations. It should optionally capture
page-load JSON responses passively and join metadata by shortcode when available. It should not use
hover loops, item-page fan-out, OCR, search navigation, main-profile grid checks, or scrolling by
default.

Minimum creator profile snapshot fields for the capture path, when visible in DOM or passive JSON:

```yaml
creator_profile_snapshot:
  platform: instagram
  source_profile:
  numeric_id:                  # when observed
  capture_timestamp_utc:
  capture_context_label:
  profile_grid_url:
  final_url:
  display_name:
  bio:
  external_url:
  bio_links:                   # list of {title, url} public link-in-bio destinations (not just a count)
  follower_count:
  following_count:
  post_or_media_count:
  raw_profile_text_excerpt:
  source_surfaces:
  parse_status:
  limitations:
```

Minimum media observation fields for the capture path:

```yaml
media_observation:
  platform: instagram
  source_profile:
  capture_timestamp_utc:
  capture_context_label:
  profile_grid_url:
  final_url:                  # actual page landed on; keep for redirect/block evidence
  permalink_path:
  permalink_url:              # item URL derived from final_url + permalink_path; not a navigation claim
  grid_index_observed:
  kind: reel | post | unknown
  shortcode:
  pinned_on_clips_tab: true | false | null    # reels-tab pin from /clips/user clips_tab_pinned_user_ids (passive JSON, not a DOM marker)
  pinned_on_timeline: true | false | null     # main-grid pin from timeline_pinned_user_ids / web_profile_info pinned_for_users
  rendered_anchor_text:
  visible_numeric_texts:
  hidden_leaf_numeric_texts:
  hidden_engagement_candidates:
  views_text:
  likes_text:
  comments_text:
  extraction_mode: no_hover_dom | hover_dom | item_page | ocr | unknown
  parse_status:
  route_status:
  evidence_locator:
  rect:
  source_surface_candidates:
    - source_surface: dom_grid_engagement | clips_user_json_metadata | web_profile_info_json_metadata | profile_feed_json_metadata | item_page_metadata | unknown
      capture_mode: passive_page_load | explicit_fetch | dom_extract | unknown
      join_status: joined_by_shortcode | missing_json | missing_shortcode | ambiguous | not_attempted
      taken_at_timestamp:
      taken_at_utc:
      caption_text:
      product_type:
      typename:
      is_video:
      like_count_candidate:
      comment_count_candidate:
      video_or_play_count_candidate:
      is_paid_partnership_candidate:
      is_affiliate_candidate:
      sponsor_user_candidates:
      raw_node_key_sample:
      metadata_limitations:
  selected_fields:
    views_text:
    likes_text:
    comments_text:
    taken_at_utc:
    caption_text:
    selection_policy_version:
    selection_limitations:
  limitations:
```

### v0 emit posture (derivable vs. captured)

The `media_observation` shape above is the full conceptual record. The v0 optimized runner
(`run_source_capture_ig_reels_grid_packet.py`) does **not** separately emit the typed restatement
fields below, because they are losslessly **derivable** from evidence the packet already preserves
(`dom_rows[].parse_status`, the full `joined_rows[].source_surface_candidates` list, and the
capture-level `selection_policy_version`). Deferring them keeps the shared Source Capture Packet
schema small until a downstream consumer (projection/ECR) pins its contract; the consumer derives
them, or a field is promoted then. Derivable-not-emitted in v0:

- `join_status` — derive from a row's candidate set: candidates present -> `joined_by_shortcode`,
  empty -> `missing_json`, `parse_status == ambiguous_hidden_numeric` -> `ambiguous`. The runner also
  records the missing-join case as the slice limitation `no_passive_json_join_for_shortcode`.
- `extraction_mode` — constant `no_hover_dom` for this single route.
- `route_status` — implied by the runner exit code and `capture_metadata`.
- `selected_fields` / per-row `selection_policy_version` / `selection_limitations` — the selected
  metric values are emitted as typed `metric_observations`; the selection is recomputable by
  re-running the capture-level `selection_policy_version` over the preserved candidates.

Pinned posture is captured from passive JSON, **not** the DOM. A 2026-06-25 logged-out probe of a
public `/reels/` grid found no "Pinned" text/aria marker anywhere in the rendered DOM, but the pin
posture is exposed reliably in the JSON the runner already preserves, as typed candidate fields:

- `pinned_on_clips_tab` — reels-tab pin, from `/clips/user` `clips_tab_pinned_user_ids` (non-empty
  list = pinned; empty = not pinned; null = field absent on this surface).
- `pinned_on_timeline` — main-grid / timeline pin, from `timeline_pinned_user_ids` or
  `web_profile_info` `pinned_for_users`.

This is point-in-time (a creator pins/unpins) and not otherwise re-capturable, so it is captured now.

The packet also emits a packet-level `pinned_inference` summary that cross-checks two **independent**
reels-tab pin signals, scoped to the reels grid only (main-grid/`timeline` pins stay out of it):

- `reels_tab_explicit_pinned_shortcodes` — the authoritative `pinned_on_clips_tab` flag.
- `reels_tab_inferred_pinned_by_recency` — a corroborating heuristic: IG hoists up to 3 pinned reels
  to the top of the *visible grid* out of recency order, so a leading grid row whose `taken_at` is
  older than a later row is inferred-pinned (`infer_pinned_shortcodes_by_recency`).
- `recency_matches_explicit` — whether the two agreed this capture (informational, not a correctness
  claim; inversion is blind to a pin of the most-recent reel, which only the explicit flag catches).

The inversion runs over **grid (DOM) order, not `/clips/user` feed order**: the 2026-06-25
esthertakumi probe showed the `/clips/user` feed stays purely recency-descending and never hoists
pins, so only the visible grid carries the positional pin signal.

Probe caveat (still open): on both probed profiles the only pins observed were main-grid posts
(`pinned_for_users` / `timeline` positive — now directly observed) which do **not** appear in the
`/reels/` capture at all (a main-grid pin is not a reels-tab pin). The reels-tab positive
(`clips_tab_pinned_user_ids` non-empty, and a grid-order recency inversion) remains **inferred, not
yet directly observed** on a reels-pinned profile; both reels-tab signals correctly read empty and
agree on a profile with no reels-tab pin.

Join yield: the same probe captured 12/12 grid rows joined to passive JSON; an earlier 2/12 miss was
not reproduced and is treated as a transient race between the `/clips/user` XHR and the DOM snapshot.
The default post-load settle window was widened (`DEFAULT_IG_REELS_SETTLE_SECONDS` 2.5 -> 4.0s) to
reduce that race; a row that still misses the join is recorded as the honest
`no_passive_json_join_for_shortcode` gap, never faked.

`caption_text` is allowed only when it is directly present in joined JSON or a later explicitly
configured item-page source. If absent, it stays null. The capture runner must not infer topic,
sponsor status, content category, or creator intent from thumbnails, engagement, or grid order.

## Parse Statuses

Required statuses:

- `parsed_no_hover_grid_engagement` - views, likes, and comments parsed from no-hover DOM shape.
- `views_only_no_hidden_engagement` - visible views found but hidden like/comment leaves missing.
- `hidden_engagement_only_no_visible_views` - hidden numeric leaves found without visible views.
- `ambiguous_hidden_numeric` - hidden numeric leaves cannot be mapped to likes/comments safely.
- `static_post_contract_unverified` - static/main-grid post behavior not pinned by this route.
- `access_failed_visible_block` - visible login wall, interstitial, challenge, or suspicious notice.
- `zero_anchor_route_variant` - page rendered but no media anchors were found.
- `route_not_verified` - route context cannot support the claim being made.

## Code-Enforceable Capture Rules

These are appropriate for runner checks, assertions, or tests:

- Accept only explicit handle or Instagram `/reels/` URL input for the default route.
- Normalize and record `profile_grid_url`, `final_url`, `permalink_path`, and `permalink_url`
  separately; never replace `final_url` with an item permalink.
- Default to no hover, no click, no item-page navigation, no OCR, no search navigation, no main-grid
  capture, and no scroll unless the run explicitly enables a different mode and records it.
- Cap visible media anchors per run; report observed count and parsed count.
- Use shortcode or permalink path as identity; never use grid index as identity.
- Preserve `visible_numeric_texts`, `hidden_leaf_numeric_texts`, and
  `hidden_engagement_candidates` even when parsed fields are present.
- Parse likes/comments only when the clean observed shape is present; otherwise emit
  `ambiguous_hidden_numeric` or another partial status.
- Treat CSS class names as unstable. Select by media permalink anchors, source-visible text, leaf
  text, and route-visible semantics instead.
- Stop and emit a visible route status on login redirect, interstitial, suspicious notice, challenge,
  repeated zero anchors, or parse ambiguity.
- Do not record raw proxy endpoints, exit IPs, cookies, storage-state JSON, raw browser profile paths,
  passwords, CAPTCHA artifacts, or raw media bytes.
- Do not record `video_url`, fetch media bytes, or treat thumbnail/display URLs as proof of content
  topic by default.
- Join JSON metadata only by shortcode. If a shortcode is absent from JSON, leave date/caption fields
  null and surface the missing join (v0 runner: the slice limitation `no_passive_json_join_for_shortcode`,
  from which `join_status: missing_json` is derivable); do not extrapolate exact dates from grid order.
- Record `source_surface` for every numeric/count candidate. Do not collapse DOM views,
  `/clips/user` play/view counts, and `web_profile_info` video/play counts into one unqualified value.
- Preserve all count candidates when source surfaces disagree; selection/reconciliation is a versioned
  policy decision and must remain visible in emitted limitations.
- Passive page-load JSON capture is lower footprint than explicit JSON fetches; if explicit JSON
  fetches are enabled later, code must label the request class separately.
- Treat ad-related fields such as `is_paid_partnership`, `is_affiliate`, sponsor users, brand/product
  mentions, and caption ad terms as candidate signals only; do not classify ads in this capture route.

Not enforceable by code alone:

- Claims that the route is undetectable, human-like, legally sufficient, or immune from future walls.
- Semantic correctness of "what the video is about" beyond directly captured caption text.
- Whether a creator's likes/comments are paid, botted, sponsored, or commercially meaningful.
- Future stability of IG's DOM, JSON endpoints, or rate behavior.

## Non-Goals

- Projection, scoring, momentum classification, bot/paid-comment classification, or storage policy.
- Capturing comment text or commenter identities.
- Private/auth-gated profile access, login automation, CAPTCHA solving, cookie export, raw storage
  handling, anti-detection bypass, or browser-fingerprint spoofing.
- Treating static posts or main-grid behavior as equivalent to the `/reels/` grid.
- TikTok, YouTube, or cross-platform generalization.

## Sanitized Evidence Appendix (2026-06-22)

This appendix makes the source context portable across clean worktrees. It is a summarized diagnostic
evidence excerpt, not validation, readiness, endpoint-stability proof, ad classification, or a source
capture packet. It intentionally excludes raw response bodies, proxy endpoints, exit IPs, cookies,
storage-state files, browser profile paths, screenshots, and media bytes.

vanzzcoser /api/v1/clips/user/ metadata probe, 1080x1920, page-load JSON source surface:

| shortcode | taken_at_utc | video_or_play_count | like_count | comment_count |
|---|---:|---:|---:|---:|
| C7dGMB_hY3n | 2024-05-27T02:10:12Z | 1477637 | 73554 | 536 |
| DZz48C2hkI5 | 2026-06-20T14:19:02Z | 80290 | 11812 | 23 |
| DZx0y8jBw-q | 2026-06-19T19:05:19Z | 30034 | 5810 | 18 |
| DZq4VgUBZHY | 2026-06-17T02:20:24Z | 5988 | 1726 | 3 |
| DZq4QFfB0zC | 2026-06-17T02:19:46Z | 1860 | 822 | 4 |
| DZewzx8BjVK | 2026-06-12T09:23:53Z | 11810 | 1098 | 3 |
| DZcuy9Ahrsf | 2026-06-11T14:27:49Z | 17191 | 2126 | 4 |
| DZcan8vhyx1 | 2026-06-11T11:31:30Z | 10242 | 951 | 2 |
| DZcaj_DBD3H | 2026-06-11T11:30:59Z | 17548 | 1983 | 1 |
| DZcYXi_hVP9 | 2026-06-11T11:11:52Z | 26860 | 2787 | 13 |
| DZX1Tm3Bss2 | 2026-06-09T16:48:33Z | 24605 | 2189 | 2 |
| DZXDTz5BuIW | 2026-06-09T09:31:46Z | 16702 | 1384 | 1 |

jeremyfragrance 1920x4000 source-surface conflict sample. DOM views and /clips/user counts
matched for these sampled visible rows; web_profile_info was lower or absent for the same shortcode
in the sanitized sample:

| shortcode | dom_views | web_profile_info_count | clips_user_count | dom_likes | dom_comments |
|---|---:|---:|---:|---:|---:|
| DZ4Stb5MVPB | 2,984 | 655 | 2984 | 30 | 4 |
| DZ4SvBvs6PB | 2,854 | 653 | 2854 | 13 | 0 |
| DZ4SxgfMfu6 | 5,493 |  | 5493 | 65 | 1 |
| DZ4Sq-8MLZq | 1,876 |  | 1876 | 9 | 0 |
| DZ4SnhHMx8m | 1,630 |  | 1630 | 9 | 0 |

Viewport and zoom diagnostics summarized:

- vanzzcoser 768x1024 and 1080x1920: 12 DOM anchors and 12 parsed no-hover rows.
- vanzzcoser 5204x4728: login redirect and zero anchors.
- jeremyfragrance CloakBrowser 1080x1920: 12 DOM anchors, 12 parsed rows, 12 network media records, 10 joined metadata rows.
- jeremyfragrance CloakBrowser 1920x4000: 12 DOM anchors, 12 parsed rows, 30 network media records, 12 joined metadata rows.
- Zoom matrix: Playwright/CDP zoom did not produce a clean zoom-out route; several zoom-out attempts redirected to login, and no DOM rows were joined. Zoom remains excluded from steady-state.

## Evidence Pointers

- DOM probe, `768x1024`: `orca-harness/_test_runs/ig_vanzz_reels_dom_probe_768x1024_20260622_1/`.
- DOM probe, `1080x1920`: `orca-harness/_test_runs/ig_vanzz_reels_dom_probe_1080x1920_20260622_1/`.
- High-viewport failure: `orca-harness/_test_runs/ig_vanzz_reels_dom_probe_5204x4728_20260622_1/`.
- Passive network sniff: `orca-harness/_test_runs/ig_vanzz_reels_network_sniff_20260622_1/`.
- `/clips/user` metadata probe: `orca-harness/_test_runs/ig_vanzz_reels_json_ad_metadata_20260622_1/summary.json`.
- CloakBrowser viewport/source-surface probe: `orca-harness/_test_runs/ig_cloakbrowser_jeremyfragrance_reels_20260622_1/summary.json` and `1920x4000/joined_rows.json`.
- Zoom matrix diagnostic: `orca-harness/_test_runs/ig_jeremyfragrance_reels_zoom_matrix_20260622_1/summary.json`.
- Existing caption parser: `orca-harness/source_capture/ig_momentum_harvest.py` parses
  `edge_media_to_caption` into `caption` for joined profile-feed JSON records.

## Downstream Handoff

```yaml
spec_handoff:
  status: CAPTURE_SPEC_READY_FOR_SCOPING
  current_path: forseti/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md
  required_behavior:
    - Extract public IG `/reels/` grid engagement from no-hover media-anchor DOM.
    - Preserve raw numeric leaf evidence plus parsed views/likes/comments when clean.
    - Join passive page-load JSON metadata by shortcode when available.
    - Preserve per-field source-surface provenance for DOM, `/clips/user`, and `web_profile_info` candidates.
    - Keep date/caption null with explicit limitations when JSON does not contain the shortcode.
  deferred:
    - projection and typed metric promotion
    - scoring and monitoring policy
    - static/main-grid post comparison arm, limited to onboarding, periodic refresh, or escalation
    - item-page fallback for full caption/date coverage
    - runner persistence surface
  review_timing_advisory:
    adversarial_review: not_needed_for_this_capture-spine_note
    why: This patch records a bounded capture-path contract and code-enforceable rules only; first runner implementation should be reviewed separately.
```
