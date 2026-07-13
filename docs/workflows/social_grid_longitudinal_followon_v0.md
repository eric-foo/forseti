# Social Account-Window Longitudinal Follow-on v0

```yaml
retrieval_header_version: 1
artifact_role: workflow follow-on contract
scope: >
  Documentation-only plan for extending the TikTok packet-grain longitudinal
  metric proof to the existing Instagram Reels-grid and YouTube channel-RSS
  Bronze surfaces.
use_when:
  - TikTok packet-grain metric history has passed its scratch-only acceptance tests.
  - Planning the next Instagram or YouTube longitudinal metric adapter.
authority_boundary: retrieval_only
stale_if:
  - the named Instagram or YouTube Bronze source surface changes
  - the accepted TikTok MetricObservationSet contract or exact-policy reader changes
open_next:
  - forseti-harness/runners/run_source_capture_ig_reels_grid_packet.py
  - forseti-harness/source_capture/ig_reels_grid_projection.py
  - forseti-harness/runners/run_source_capture_youtube_rss_monitor.py
  - forseti-harness/source_capture/youtube_watch_packet.py
```

## Status And Boundary

This artifact specifies future work. It does **not** claim that Instagram or
YouTube emits the new packet-grain Silver observation set, and it authorizes no
live capture, live-lake write, scheduler change, Creator Registry mutation,
schema migration, backfill, Cleaning, ECR, or Judgment work.

The extension gate is the tested TikTok proof: one immutable Bronze
account-window packet must deterministically produce one lineage-closed,
policy-fingerprinted Silver `MetricObservationSet`; an exact-policy reader must
recover repeated observations by platform-native video ID. Do not start a
second platform until those mechanics pass in scratch.

“Grid” is not the portable abstraction. Instagram and TikTok expose profile
grids, while YouTube's cheap daily surface is an RSS enumeration. The shared
unit is an **account-window observation packet**: one account, one capture time,
and source-visible metric postures for its platform-native content objects. An
eligible observation set has at least one content row; an empty source window
is handled explicitly and does not become a fabricated Silver row.

## Confirmed Current Capture Seams

| Platform | Current Bronze seam | Stable content identity | Metrics available at the cheap account-window surface | Current downstream state |
| --- | --- | --- | --- | --- |
| Instagram | `run_source_capture_ig_reels_grid_packet.py`; `source_family=instagram_creator`; `source_surface=ig_reels_grid_dom_passive_json`; preserved `ig_reels_grid_capture.json` from one logged-out `/reels/` page load | Reel `shortcode`, joined between DOM and passive JSON; grid position is retained only as source evidence | `view_count`, `like_count`, and `comment_count`, each already represented with an explicit posture; passive JSON and DOM candidates are retained for reconciliation | `ig_reels_grid_projection.py` emits strict mechanical rows, and `silver_metric_producer.py` can emit existing per-metric Silver observations. It does not yet claim the shared packet-grain longitudinal set described here. |
| YouTube | `run_source_capture_youtube_rss_monitor.py`; `source_family=youtube`; `source_surface=youtube_channel_rss_feed`; preserved raw feed XML plus `rss_monitor_entries.json` | Source-served YouTube `video_id`; feed position is not identity | Exact `view_count`; `media:starRating count` carried as `like_count` with named provenance; `comment_count` explicitly unavailable because the feed does not expose it | The daily RSS packet has no packet-grain Silver history adapter named in this plan. The existing YouTube Silver producer is based on deeper watch-packet metric documents, a different source surface and cadence. |

YouTube's deeper `youtube_watch_metadata_comments` packet remains the
performance-triggered enrichment seam. It can carry `view_count`, `like_count`,
sampled comments, and a source-native total comment count when exposed. It must
not be silently substituted for a missing daily RSS observation or mixed into
the RSS policy fingerprint.

## Shared Silver Contract To Reuse

Each eligible Bronze account-window packet produces exactly one atomic Silver
observation-set record under that packet's raw anchor.

The set must contain:

- the platform and one platform-account subject;
- the capture time from the Bronze packet, never producer wall-clock time;
- a producer policy version and SHA-256 policy fingerprint;
- one row per captured content object, keyed by platform-native ID;
- optional source position for audit only;
- a strict metric map whose entries couple posture and value;
- exact raw-file lineage, including packet ID, file ID, stored-byte hash, and
  the platform-specific source surface.

Identity and time rules are shared:

- join history by `(platform, account_native_id, content_native_id)`, never by
  grid or feed position;
- keep every capture as an immutable timepoint;
- a day with no committed packet produces no observation;
- a content object absent from a later bounded window gets no later row; absence
  is not a zero and does not supersede its earlier history;
- an observed source value of literal `0` is `observed(value=0)`;
- a metric absent, hidden, unparseable, or unsupported on the source surface is
  non-observed with a reason and no numeric value;
- the reader requires an exact policy fingerprint and never guesses “latest”;
- equal-time distinct records for the same policy and content identity fail
  closed rather than selecting by packet order.

## Instagram Follow-on

### Bronze ownership

No new Instagram acquisition route is justified by the current evidence. The
existing Reels-grid packet already preserves the native shortcode, capture
time, the selected metric postures, and the raw DOM/passive-JSON disagreement.
The future adapter should consume the committed packet or its mechanical
projection by key; it must not revisit Instagram.

A Bronze writer change is warranted only if focused tests prove one of these
load-bearing facts is not durable in a committed packet: capture time, profile
identity, shortcode, per-metric posture/value, selection policy version, or raw
file hash. Do not redesign Bronze merely to resemble TikTok.

### Platform mapping

- account native ID: the captured Instagram public handle, with the existing
  platform-account linkage reference retained when available;
- content native ID: `shortcode`;
- `view_count`: selected Reels view/play count from the committed slice;
- `like_count`: selected source-visible like count;
- `comment_count`: selected source-visible comment count;
- per-surface candidate counts and join status: retain as provenance or row
  limitations, not as competing normalized metrics;
- static `/p/` rows: remain outside the Reels traction series; never reinterpret
  a static-post visible number as `view_count`.

The new record is a sibling physicalization for longitudinal reads. It does not
rewrite or silently supersede existing per-metric Instagram Silver records.

### Instagram success signals

1. Two scratch Bronze grid packets for the same account and shortcode at two
   capture times produce two deterministic observation sets and a two-point
   shortcode history.
2. Reordering the grid changes `source_position` but does not change the
   history key or create a second content identity.
3. Literal zero survives as observed; missing passive JSON, ambiguous DOM
   numerics, and unsupported metrics remain non-observed with reasons.
4. Every selected value can be traced to the committed packet and preserved
   capture bytes; a raw hash or packet-anchor mismatch fails the reader.
5. A rerun writes no duplicate record; acknowledgement occurs only after the
   derived record is reread and verified.
6. A policy-fingerprint mismatch returns no substitute record, and malformed
   posture/value coupling fails validation.

## YouTube Follow-on

### Bronze ownership

The daily RSS monitor already commits the minimum Bronze facts needed for a
bounded longitudinal adapter: channel identity, capture time, video ID, exact
view count when exposed, `starRating` count with provenance, and an explicit
unavailable comment count. It also preserves the served XML and normalized
entries artifact.

Therefore the first YouTube change should be a Silver consumer for
`youtube_channel_rss_feed`, not a new “grid” capture runner. A Bronze change is
needed only if focused tests show the committed source slices cannot bind an
entry's video ID, metric posture, capture time, or preserved-file hash without
guessing.

### Platform mapping

- account native ID: requested and served YouTube channel ID after the current
  fail-closed identity check; preserve the platform-account linkage reference;
- content native ID: `video_id`;
- `view_count`: RSS `media:statistics views` when parseable;
- `like_count`: RSS `media:starRating count`, with the current provenance note
  carried into policy/provenance; do not relabel it as unqualified platform
  truth;
- `comment_count`: unavailable with the exact reason that the feed schema
  carries no comment count;
- title, published time, updated time, and first-seen state: source-visible
  context/provenance, not engagement metrics;
- content kind: unknown/mixed at this tier unless source evidence supplies a
  classification; do not infer Shorts from feed position or URL shape.

Watch-packet observations remain a separate, explicitly selected policy. A
reader may later expose RSS and watch histories side by side, but must not merge
their values into one series without a separately approved reconciliation
policy.

### YouTube success signals

1. Two scratch RSS packets for the same channel and video ID at two capture
   times produce two deterministic observation sets and a two-point video
   history.
2. A video moving to a different feed position remains one identity; leaving
   the 15-entry window produces no new row and no invented zero/carry-forward.
3. Missing or unparseable views and `starRating` values remain non-observed;
   literal zero remains observed; `comment_count` is always unavailable for
   this source policy.
4. Requested/served channel identity mismatch, malformed feed entry identity,
   raw hash mismatch, or missing capture time blocks derivation or reading.
5. Reprocessing is idempotent, acknowledgement follows verified persistence,
   and non-RSS YouTube packets receive an explicit non-target acknowledgement.
6. Exact RSS policy selection never returns a watch-packet record, and exact
   watch policy selection never falls back to RSS.

## Cross-platform Acceptance Gate

Before either adapter is considered complete, focused tests must show:

- one and only one observation-set record per eligible Bronze packet and policy;
- deterministic record ID and content hash;
- record row count equals the eligible native-content rows in the packet;
- exact raw-anchor lineage and stored-byte hash verification;
- missing-versus-zero posture preservation for every mapped metric;
- history retrieval for requested native IDs across at least two captures;
- idempotent rerun and explicit handling of non-target packets;
- failure visibility for malformed output, ambiguous equal-time records,
  lineage mismatch, content-hash mismatch, and policy mismatch;
- all tests and demonstrations use fixtures or an isolated scratch lake.

No live cadence claim follows from these tests. Live scheduling, throughput,
retention, and operational failure recovery need their own later authorization
and evidence.

## Accepted Residuals

- Instagram covers the bounded first-visible Reels grid, not a complete account
  history; static posts are deliberately excluded, and delayed/missing passive
  JSON can leave honest metric gaps.
- YouTube RSS carries at most the recent feed window, mixes formats, has no
  comment count, and exposes `starRating` rather than an independently named
  like-count field. The current `starRating`-as-like mapping remains a named
  source-policy assumption.
- Missing capture days and content objects outside a bounded window are sparse
  history, not negative observations.
- Existing Instagram and YouTube per-metric Silver records may coexist with the
  future packet-grain set. No migration, deletion, or backfill is part of this
  follow-on.
- No cross-platform content identity, creator identity inference, metric
  reconciliation, SQL materialization, velocity judgment, viral threshold,
  Gold claim, or buyer-proof claim is introduced.
- Scratch proof does not establish live-lake readiness, scale to 2,500 creators,
  storage retention policy, or scheduler economics.

These residuals are acceptable for the bounded objective because they preserve
source truth and still allow exact per-platform, per-video longitudinal reads.
Upgrade only when a downstream decision requires one of the excluded claims or
when scratch tests expose a load-bearing gap.

## Source-read Ledger

- `forseti-harness/runners/run_source_capture_ig_reels_grid_packet.py`: current
  Instagram packet surface, capture time, selection policy, native shortcode,
  metric slices, and raw artifact.
- `forseti-harness/source_capture/ig_reels_grid.py`: Instagram DOM/passive-JSON
  row shape and shortcode join.
- `forseti-harness/source_capture/ig_reels_grid_projection.py`: strict
  posture/value projection, raw anchors, capture time, and source-surface
  disagreement retention.
- `forseti-harness/capture_spine/creator_profile_current/silver_metric_producer.py`:
  existing Instagram per-metric Silver physicalization and its boundaries.
- `forseti-harness/runners/run_source_capture_youtube_rss_monitor.py`: current
  daily RSS Bronze packet, channel/video identity, capture timing, metric
  postures, feed-window limit, and first-seen semantics.
- `forseti-harness/source_capture/youtube_channel_rss.py`: parser honesty rules
  for missing views and `starRating` values.
- `forseti-harness/source_capture/youtube_watch_packet.py`: separate deeper
  watch metadata/comments packet and its metric postures/non-claims.
- `forseti-harness/capture_spine/creator_profile_current/youtube_silver_metric_producer.py`:
  existing watch-seed Silver path, which is not the RSS adapter specified here.
