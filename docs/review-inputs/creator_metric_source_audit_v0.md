# Creator Metric Source Audit v0

```yaml
retrieval_header_version: 1
artifact_role: review_input
scope: >
  Source-backed audit and import note for creator metric observations and
  aggregate view rollups feeding the Capture-owned creator_profile_current view.
use_when:
  - Checking whether Orca has enough real creator metric data to seed metric observations.
  - Reviewing the YouTube view-count seed before any SQLite, data-lake job, or dashboard work.
  - Distinguishing admitted-pool average views from full-channel creator influence or engagement rate.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_seed_v0.json
  - orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_observation_ledger_v0.json
stale_if:
  - The YouTube Shorts fragrance creator observation ledger changes.
  - Any source capture artifact listed below changes.
  - A later capture route adds source-backed like_count, total comment_count, subscriber_count, or engagement_rate rows.
```

## Result

We have enough real data for a narrow seed:

- 196 YouTube `view_count` metric observations across 30 non-brand creator/channel platform accounts.
- 30 account-scoped rollups for average and median views over the admitted fragrance Shorts pool.
- 4 Scentbird brand/platform rows preserved as exclusions, not creator rollups.

We do not yet have enough real data for engagement rate, average likes, average total comments, subscriber count, or full-channel creator influence.

## Source Capture Receipt

Access classification: `publicly-viewable-but-ToS-restricted`.

Route used: direct HTTP over public YouTube watch/Shorts served HTML. The checked-in capture artifacts already preserve `view_count` rows. A bounded live probe over 3 videos was run as a route sanity check and wrote:

`docs/review-inputs/creator_metric_source_live_probe_youtube_v0.json`

Live probe outcome:

- 3 public video targets, logged-out, human-rate.
- 2 of 3 exposed `ytInitialPlayerResponse.videoDetails.viewCount`.
- 1 of 3 returned HTTP 200 but no extracted current view count.
- like/comment count text was not captured by this route.

Verdict: GO for YouTube `view_count` observation seeding only. PARTIAL for live current refresh. NO support yet for engagement rate.

## Imported Seed

Generated artifact:

`orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_seed_v0.json`

The seed uses these source files:

| Source | Imported rows |
| --- | ---: |
| `docs/review-inputs/youtube_shorts_fragrance_retained_recapture_v0.json` | 25 |
| `docs/review-inputs/youtube_shorts_fragrance_replacement_capture_v0.json` | 5 |
| `docs/review-inputs/youtube_shorts_fragrance_tone_expansion30_capture_v0.json` | 30 |
| `docs/review-inputs/youtube_shorts_fragrance_tone_expansion100_capture_v0.json` | 40 |
| `docs/review-inputs/youtube_shorts_fragrance_tone_expansion200_capture_v0.json` | 100 |

Total source rows: 200.

Mapping result:

- 200 source rows match the YouTube creator observation ledger video IDs.
- 196 rows map to non-brand creator/channel platform accounts.
- 4 rows map to Scentbird, classified as `brand_or_platform_account_observed`, and are excluded from creator rollups.
- 30 platform accounts receive account-scoped rollups.

## Lake Audit

Fresh local read:

- `F:\orca-data-lake`: 1 raw manifest, source family/surface `fragrance_purchase_review_pdp / direct_http_pdp`, 0 non-empty `metric_observations`.
- `F:\orca-data-lake-legacy-v0-20260628T174129Z`: 262 raw manifests: 199 YouTube captions, 1 YouTube audio, 1 Instagram creator audio, 55 web pages, 6 Reddit local artifacts, 0 non-empty `metric_observations`.
- Legacy Instagram derived audience-comment files: 113 files, 113 reel shortcodes, 1,135 captured comment rows, max top-level `comment_count` 15.

The Instagram comment files are not total public comment counts. They are admissible as captured comment-sample evidence only, so they are not used for engagement rollups here.

## Boundaries

Allowed claim:

`average_views` over the admitted YouTube fragrance Shorts pool for one platform account.

Forbidden claim:

`average creator views`, `channel-wide influence`, `engagement rate`, `creator quality`, `buyer proof`, or cross-platform creator influence.

The hard pushback is important: this seed is useful, but it is not the final creator intelligence answer. It is the first source-backed metric layer under that answer.

## Profile-Current Application

This seed now supports a static `creator_profile_current` export:

`orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_v0.json`

The export should:

- show view-count rollups with `freshness_state: partial`;
- show engagement-rate fields as `unavailable_with_reason`;
- keep cross-platform rollups blocked until public-handle linkage is promoted;
- leave ideal-audience fields unavailable until source-backed audience snapshots are joined;
- require a separate metric-bearing capture probe when we want likes/comments/subscribers.
