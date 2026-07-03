# Creator Signal Multi-Creator Library — Static Projection v0

```yaml
retrieval_header_version: 1
artifact_role: product_signal_static_projection
scope: >
  Static, source-backed Markdown projection of the Creator Signal Library over
  the 33 creator_profile_current rows committed at
  origin/main@0f460b01362a849e40174d11dd89e4804f5f9d19, rendered as
  platform-scoped (YouTube, Instagram) library sections per the accepted
  multi-creator display contract.
use_when:
  - Reviewing this projection during implementation review of the Step 3 static projection.
  - Scanning current creator_profile_current rows without opening the full JSON or profile view.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/creator_signal/creator_signal_multi_creator_library_surface_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json
stale_if:
  - creator_profile_current_view_v0.json profiles_total, platform mix, or any metric posture changes from the counts recorded below.
  - A later accepted contract authorizes cross-platform rollups, populated ideal-audience rows, or posting_cadence/recent_velocity population.
```

## Status And Non-Authority

This is a static, source-backed Markdown snapshot of the Creator Signal Library over the current committed `creator_profile_current` rows. It is not a dashboard, API, CRM list, capture job, data-lake write, source of truth, buyer proof, product proof, or outreach authorization. It reflects the source data at the snapshot below; it does not refresh itself.

## Source Snapshot

- Repository snapshot: `origin/main@0f460b01362a849e40174d11dd89e4804f5f9d19` (this worktree's checked commit at authoring time)
- Input view file: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json`
- View `generated_at_utc`: `2026-07-02T14:10:00Z`
- Reconfirmed data posture counts (verified by direct structural read of the committed JSON):

```text
profiles_total=33
platform_account_profiles=33 (creator_record_profiles=0, cross_platform_rollup_profiles=0)
platforms=youtube:30, instagram:3
average_views=observed:33
engagement_rate=observed:31, unavailable_with_reason:2
average_like_count=observed:32, unavailable_with_reason:1
average_comment_count=observed:32, unavailable_with_reason:1
posting_cadence=not_attempted:33
recent_velocity=not_attempted:33
sample_adequacy=stronger_admitted_pool_n_8_plus:30, limited_n_4_to_7:1, thin_n_1_to_3:2
profiles_with_ideal_audience_profiles=0
identity_state=single_platform_observed:33
link_state_or_none=null:33
review_state_or_none=null:33
```

These counts match the reconfirmation snapshot recorded in the commissioning handoff prompt exactly; no drift was found against the live committed view.

## Creator Signal Library

This is a **library** or **catalog** of currently committed creator profiles — it is not a leaderboard, ranking, lead list, priority queue, or outreach list. Table order below is a selected-metric sort within one platform, never a creator ranking or merit score.

**What this library does not prove:** it does not prove buyer readiness, creator performance, audience fit, or outreach priority. See [Non-Claims and Accepted Residuals](#non-claims-and-accepted-residuals) before treating any row as a recommendation, ranking, or lead.

The library is organized by platform. There is no combined, all-platform table and no cross-platform rank. Every row below is a `platform_account`-scoped, `single_platform_observed` profile; no `creator_record`, cross-platform rollup, or populated ideal-audience row exists in the current data.

### How to read a row

Each row shows the selected observed scan metric (`average_views`), a sample-support cue, a freshness cue, the declared-deferred `posting_cadence`/`recent_velocity` state, and a missingness/limitations cue — all visible without opening the row's Details entry. Sorting is a selected-metric sort within one platform section only. Open the linked handle to reach the row's full Details entry: limitations, non-claims, source drill-back pointers, calculation recipe version, and additional metric families.

## YouTube Section (30 rows)

Sorted by `average_views` (observed), descending, within this platform only.

| Handle | Subject ID | Avg Views (observed) | Sample Support | Freshness | Cadence / Velocity | Missingness / Limitations |
|---|---|---|---|---|---|---|
| [JusDeRose](#details-acct-yt-fragrance-012) | `acct_yt_fragrance_012` | 160,954.29 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [GentsScents](#details-acct-yt-fragrance-010) | `acct_yt_fragrance_010` | 127,654.08 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [OliviaOlfactory](#details-acct-yt-fragrance-015) | `acct_yt_fragrance_015` | 104,980.60 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [DemiRawling](#details-acct-yt-fragrance-006) | `acct_yt_fragrance_006` | 100,543.50 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [TheScented](#details-acct-yt-fragrance-028) | `acct_yt_fragrance_028` | 73,836 (observed) | limited (n 4-7) | 2026-07-02 (partial) | not yet available (both) | limited sample; admitted-pool only, not channel-wide |
| [CurlyScents](#details-acct-yt-fragrance-005) | `acct_yt_fragrance_005` | 64,618.90 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [CurlyFragrance](#details-acct-yt-fragrance-004) | `acct_yt_fragrance_004` | 48,680 (observed) | thin (n 1-3) | 2026-07-02 (partial) | not yet available (both) | thin sample; admitted-pool only, not channel-wide |
| [SchoolofScent](#details-acct-yt-fragrance-022) | `acct_yt_fragrance_022` | 32,946.92 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [BowTieFragranceGuy](#details-acct-yt-fragrance-001) | `acct_yt_fragrance_001` | 27,558.80 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [PostCologne](#details-acct-yt-fragrance-016) | `acct_yt_fragrance_016` | 25,756 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [MonikaCioch](#details-acct-yt-fragrance-014) | `acct_yt_fragrance_014` | 24,483 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [ChaosFragrances](#details-acct-yt-fragrance-002) | `acct_yt_fragrance_002` | 24,352.33 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [FragranceKnowledge](#details-acct-yt-fragrance-007) | `acct_yt_fragrance_007` | 18,888.71 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [Redolessence](#details-acct-yt-fragrance-018) | `acct_yt_fragrance_018` | 16,965.08 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [ThePerfumeGuy](#details-acct-yt-fragrance-026) | `acct_yt_fragrance_026` | 15,496.91 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | engagement rate/avg likes unavailable; admitted-pool only, not channel-wide |
| [TiffBenson](#details-acct-yt-fragrance-030) | `acct_yt_fragrance_030` | 12,634.33 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [TheFragranceApprentice](#details-acct-yt-fragrance-025) | `acct_yt_fragrance_025` | 11,828.38 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [ScentedMoments](#details-acct-yt-fragrance-020) | `acct_yt_fragrance_020` | 11,644.67 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [ThePerfumeNest](#details-acct-yt-fragrance-027) | `acct_yt_fragrance_027` | 7,644.11 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [MilaLeBlanc](#details-acct-yt-fragrance-013) | `acct_yt_fragrance_013` | 7,349.88 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [Cubaknow](#details-acct-yt-fragrance-003) | `acct_yt_fragrance_003` | 6,877.67 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [TLTGReviews](#details-acct-yt-fragrance-031) | `acct_yt_fragrance_031` | 6,293.83 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [JeremyFragrance](#details-acct-yt-fragrance-011) | `acct_yt_fragrance_011` | 6,215 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [Scenteno](#details-acct-yt-fragrance-021) | `acct_yt_fragrance_021` | 5,101.50 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [funmimonet](#details-acct-yt-fragrance-009) | `acct_yt_fragrance_009` | 4,519.38 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [FragranceView](#details-acct-yt-fragrance-008) | `acct_yt_fragrance_008` | 4,088.25 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [SokiLondon](#details-acct-yt-fragrance-024) | `acct_yt_fragrance_024` | 2,520 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [TheScentinel](#details-acct-yt-fragrance-029) | `acct_yt_fragrance_029` | 1,760.25 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [SimplyPutScents](#details-acct-yt-fragrance-023) | `acct_yt_fragrance_023` | 829.20 (observed) | strong (admitted-pool, n>=8) | 2026-07-02 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [ProfessorPerfume](#details-acct-yt-fragrance-017) | `acct_yt_fragrance_017` | 107 (observed) | thin (n 1-3) | 2026-07-02 (partial) | not yet available (both) | engagement rate/avg comments unavailable; thin sample; admitted-pool only, not channel-wide |

## Instagram Section (3 rows)

Sorted by `average_views` (observed), descending, within this platform only.

| Handle | Subject ID | Avg Views (observed) | Sample Support | Freshness | Cadence / Velocity | Missingness / Limitations |
|---|---|---|---|---|---|---|
| [hyram](#details-acct-ig-reels-001) | `acct_ig_reels_001` | 145,593.33 (observed) | strong (admitted-pool, n>=8) | 2026-06-30 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [milanscents](#details-acct-ig-reels-004) | `acct_ig_reels_004` | 70,628.33 (observed) | strong (admitted-pool, n>=8) | 2026-06-30 (partial) | not yet available (both) | admitted-pool only, not channel-wide |
| [jeremyfragrance](#details-acct-ig-reels-002) | `acct_ig_reels_002` | 27,470.50 (observed) | strong (admitted-pool, n>=8) | 2026-06-30 (partial) | not yet available (both) | admitted-pool only, not channel-wide |

## Details

Full per-row limitations, non-claims, source drill-back pointers, calculation recipe version, and additional metric families. Grouped by platform, in the same order as the tables above.

### YouTube — Details

<a id="details-acct-yt-fragrance-012"></a>
#### JusDeRose (`acct_yt_fragrance_012`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: Jus de Rose
- Public account: [JusDeRose](https://www.youtube.com/channel/UCflkhyQuNBeiw3__1TUXXNg)
- Selected sort metric: `average_views` = 160,954.29 (observed)
- Median views: 128,690 (observed)
- Engagement rate: 3.46%
- Average like count: 5,464.29
- Average comment count: 110.29
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 21 source metric observations, view range 83,320-323,449
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/11`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/11`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 21 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-010"></a>
#### GentsScents (`acct_yt_fragrance_010`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: Gents Scents
- Public account: [GentsScents](https://www.youtube.com/channel/UC9IImcLkUdmURWtQhxu8VwQ)
- Selected sort metric: `average_views` = 127,654.08 (observed)
- Median views: 96,034 (observed)
- Engagement rate: 3.29%
- Average like count: 4,133.50
- Average comment count: 66.25
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 36 source metric observations, view range 51,802-309,510
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/9`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/9`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 36 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-015"></a>
#### OliviaOlfactory (`acct_yt_fragrance_015`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: Olivia Olfactory
- Public account: [OliviaOlfactory](https://www.youtube.com/channel/UCRGkzuXpYq4hCDGKe-9P50g)
- Selected sort metric: `average_views` = 104,980.60 (observed)
- Median views: 122,629 (observed)
- Engagement rate: 9.90%
- Average like count: 10,218.80
- Average comment count: 179.40
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 15 source metric observations, view range 41,893-137,760
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/14`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/14`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 15 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-006"></a>
#### DemiRawling (`acct_yt_fragrance_006`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: Demi Rawling
- Public account: [DemiRawling](https://www.youtube.com/channel/UC88iYYngvMLb_3obJKMCI3w)
- Selected sort metric: `average_views` = 100,543.50 (observed)
- Median views: 55,782.50 (observed)
- Engagement rate: 1.71%
- Average like count: 1,677.67
- Average comment count: 44.17
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 18 source metric observations, view range 41,949-286,732
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/5`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/5`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 18 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-028"></a>
#### TheScented (`acct_yt_fragrance_028`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: The Scented
- Public account: [TheScented](https://www.youtube.com/channel/UCHqrJNnjF_3yHfVDatKl-NA)
- Selected sort metric: `average_views` = 73,836 (observed)
- Median views: 73,836 (observed)
- Engagement rate: 4.54%
- Average like count: 3,281
- Average comment count: 72
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `limited_n_4_to_7`, 6 source metric observations, view range 35,323-112,349
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/26`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/26`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 6 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-005"></a>
#### CurlyScents (`acct_yt_fragrance_005`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: Curly Scents
- Public account: [CurlyScents](https://www.youtube.com/channel/UCIfiNVTfW49L7Z3lGLfIOeA)
- Selected sort metric: `average_views` = 64,618.90 (observed)
- Median views: 52,655 (observed)
- Engagement rate: 2.73%
- Average like count: 1,727.10
- Average comment count: 38.50
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 30 source metric observations, view range 37,225-161,665
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/4`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/4`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 30 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-004"></a>
#### CurlyFragrance (`acct_yt_fragrance_004`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public account: [CurlyFragrance](https://www.youtube.com/channel/UCcwPIKNTMO5S-Vd7z-RrIhg)
- Selected sort metric: `average_views` = 48,680 (observed)
- Median views: 48,680 (observed)
- Engagement rate: 5.44%
- Average like count: 2,600
- Average comment count: 46
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `thin_n_1_to_3`, 3 source metric observations, view range 48,680-48,680
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/3`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/3`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 3 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-022"></a>
#### SchoolofScent (`acct_yt_fragrance_022`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: School of Scent
- Public account: [SchoolofScent](https://www.youtube.com/channel/UC7yWwH6peQbpfLMVKKuR-xg)
- Selected sort metric: `average_views` = 32,946.92 (observed)
- Median views: 18,428 (observed)
- Engagement rate: 2.51%
- Average like count: 801.50
- Average comment count: 25.08
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 36 source metric observations, view range 6,091-154,203
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/20`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/20`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 36 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-001"></a>
#### BowTieFragranceGuy (`acct_yt_fragrance_001`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: BowTie FragranceGuy
- Public account: [BowTieFragranceGuy](https://www.youtube.com/channel/UCVvzGrPSok_sf8hfDhvTg7w)
- Selected sort metric: `average_views` = 27,558.80 (observed)
- Median views: 16,483 (observed)
- Engagement rate: 6.46%
- Average like count: 1,742.80
- Average comment count: 38
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 15 source metric observations, view range 7,883-69,889
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/0`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/0`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 15 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-016"></a>
#### PostCologne (`acct_yt_fragrance_016`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: Post Cologne
- Public account: [PostCologne](https://www.youtube.com/channel/UCArpB-dspQ5Ax3pJnj0Rnog)
- Selected sort metric: `average_views` = 25,756 (observed)
- Median views: 29,457 (observed)
- Engagement rate: 3.72%
- Average like count: 927.40
- Average comment count: 30.20
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 15 source metric observations, view range 2,670-42,095
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/15`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/15`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 15 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-014"></a>
#### MonikaCioch (`acct_yt_fragrance_014`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: Monika Cioch
- Public account: [MonikaCioch](https://www.youtube.com/channel/UCi42yeT0_OLeouUQhDBVZjQ)
- Selected sort metric: `average_views` = 24,483 (observed)
- Median views: 20,254 (observed)
- Engagement rate: 3.22%
- Average like count: 766.60
- Average comment count: 20.60
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 15 source metric observations, view range 5,382-62,753
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/13`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/13`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 15 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-002"></a>
#### ChaosFragrances (`acct_yt_fragrance_002`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: Chaos Fragrances
- Public account: [ChaosFragrances](https://www.youtube.com/channel/UC0fOGtvT1x8irPUZOFdF2mA)
- Selected sort metric: `average_views` = 24,352.33 (observed)
- Median views: 23,205 (observed)
- Engagement rate: 4.17%
- Average like count: 987.33
- Average comment count: 27
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 27 source metric observations, view range 5,678-50,135
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/1`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/1`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 27 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-007"></a>
#### FragranceKnowledge (`acct_yt_fragrance_007`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public account: [FragranceKnowledge](https://www.youtube.com/channel/UCzH0Tal9pApj-F6KSGZHo4Q)
- Selected sort metric: `average_views` = 18,888.71 (observed)
- Median views: 9,541 (observed)
- Engagement rate: 2.29%
- Average like count: 403.14
- Average comment count: 28.86
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 21 source metric observations, view range 5,612-70,067
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/6`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/6`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 21 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-018"></a>
#### Redolessence (`acct_yt_fragrance_018`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public account: [Redolessence](https://www.youtube.com/channel/UCuSy0Z5UwvkMQ7lXRbUdOnQ)
- Selected sort metric: `average_views` = 16,965.08 (observed)
- Median views: 4,546.50 (observed)
- Engagement rate: 4.67%
- Average like count: 763.75
- Average comment count: 29.08
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 36 source metric observations, view range 2,947-67,321
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/17`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/17`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 36 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-026"></a>
#### ThePerfumeGuy (`acct_yt_fragrance_026`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: The Perfume Guy
- Public account: [ThePerfumeGuy](https://www.youtube.com/channel/UCFarEEFsV90-pvUU0XdUdgQ)
- Selected sort metric: `average_views` = 15,496.91 (observed)
- Median views: 15,567 (observed)
- Engagement rate: unavailable_with_reason (null)
- Average like count: unavailable_with_reason (null)
- Average comment count: 31.36
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 22 source metric observations, view range 6,163-38,096
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate, average likes, and average total comments are unavailable until source-backed numerator fields exist.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/24`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/24`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 22 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-030"></a>
#### TiffBenson (`acct_yt_fragrance_030`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: Tiff Benson
- Public account: [TiffBenson](https://www.youtube.com/channel/UC4lKHUYqvm74znBF6qSnYig)
- Selected sort metric: `average_views` = 12,634.33 (observed)
- Median views: 9,345 (observed)
- Engagement rate: 4.89%
- Average like count: 596.33
- Average comment count: 21
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 9 source metric observations, view range 4,542-24,016
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/28`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/28`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 9 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-025"></a>
#### TheFragranceApprentice (`acct_yt_fragrance_025`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: The Fragrance Apprentice
- Public account: [TheFragranceApprentice](https://www.youtube.com/channel/UCMz0tE1qg5SwmrAF3Cshe0A)
- Selected sort metric: `average_views` = 11,828.38 (observed)
- Median views: 9,241 (observed)
- Engagement rate: 4.81%
- Average like count: 527.88
- Average comment count: 41.50
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 24 source metric observations, view range 5,032-23,983
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/23`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/23`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 24 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-020"></a>
#### ScentedMoments (`acct_yt_fragrance_020`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: Scented Moments
- Public account: [ScentedMoments](https://www.youtube.com/channel/UCd7OAY06IuwYsUoWsn3gbuQ)
- Selected sort metric: `average_views` = 11,644.67 (observed)
- Median views: 11,639 (observed)
- Engagement rate: 3.02%
- Average like count: 335
- Average comment count: 17
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 9 source metric observations, view range 3,014-20,281
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/18`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/18`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 9 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-027"></a>
#### ThePerfumeNest (`acct_yt_fragrance_027`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: The Perfume Nest
- Public account: [ThePerfumeNest](https://www.youtube.com/channel/UCyU1XUvAFqV2X1NVCcRqRNA)
- Selected sort metric: `average_views` = 7,644.11 (observed)
- Median views: 7,765 (observed)
- Engagement rate: 6.58%
- Average like count: 462.89
- Average comment count: 40
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 27 source metric observations, view range 4,804-11,732
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/25`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/25`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 27 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-013"></a>
#### MilaLeBlanc (`acct_yt_fragrance_013`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: Mila Le Blanc
- Public account: [MilaLeBlanc](https://www.youtube.com/channel/UCta4sjQtsMUtBCkI811ocfA)
- Selected sort metric: `average_views` = 7,349.88 (observed)
- Median views: 6,823.50 (observed)
- Engagement rate: 2.63%
- Average like count: 178.50
- Average comment count: 14.62
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 24 source metric observations, view range 5,393-13,071
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/12`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/12`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 24 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-003"></a>
#### Cubaknow (`acct_yt_fragrance_003`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public account: [Cubaknow](https://www.youtube.com/channel/UCzhBUw8MLmUl8cPMx63sFuw)
- Selected sort metric: `average_views` = 6,877.67 (observed)
- Median views: 5,211 (observed)
- Engagement rate: 6.10%
- Average like count: 389
- Average comment count: 30.67
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 9 source metric observations, view range 3,984-11,438
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/2`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/2`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 9 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-031"></a>
#### TLTGReviews (`acct_yt_fragrance_031`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: TLTG Reviews
- Public account: [TLTGReviews](https://www.youtube.com/channel/UCmYZrY_MVZy5Iiwlua029kg)
- Selected sort metric: `average_views` = 6,293.83 (observed)
- Median views: 5,732 (observed)
- Engagement rate: 4.98%
- Average like count: 117
- Average comment count: 45.33
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 13 source metric observations, view range 2,589-11,769
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/29`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/29`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 13 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-011"></a>
#### JeremyFragrance (`acct_yt_fragrance_011`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: Jeremy Fragrance
- Public account: [JeremyFragrance](https://www.youtube.com/channel/UCzKrJ5NSA9o7RHYRG12kHZw)
- Selected sort metric: `average_views` = 6,215 (observed)
- Median views: 6,195.50 (observed)
- Engagement rate: 1.27%
- Average like count: 65.25
- Average comment count: 13.50
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 12 source metric observations, view range 4,282-8,187
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/10`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/10`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 12 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-021"></a>
#### Scenteno (`acct_yt_fragrance_021`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public account: [Scenteno](https://www.youtube.com/channel/UC8gjOYz9aonQqd5HwoTu2NQ)
- Selected sort metric: `average_views` = 5,101.50 (observed)
- Median views: 4,546.50 (observed)
- Engagement rate: 3.03%
- Average like count: 142.50
- Average comment count: 11.50
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 16 source metric observations, view range 1,146-12,616
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/19`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/19`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 16 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-009"></a>
#### funmimonet (`acct_yt_fragrance_009`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: Funmi Monet
- Public account: [funmimonet](https://www.youtube.com/channel/UCULGc5bSAoCIUMc-hQpjCXw)
- Selected sort metric: `average_views` = 4,519.38 (observed)
- Median views: 2,147 (observed)
- Engagement rate: 2.18%
- Average like count: 45.17
- Average comment count: 4.80
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 19 source metric observations, view range 963-22,112
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/8`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/8`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 19 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-008"></a>
#### FragranceView (`acct_yt_fragrance_008`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public account: [FragranceView](https://www.youtube.com/channel/UC_Zj9atmpE2MQBtzTfqDFfw)
- Selected sort metric: `average_views` = 4,088.25 (observed)
- Median views: 1,710.50 (observed)
- Engagement rate: 3.83%
- Average like count: 143
- Average comment count: 13.50
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 12 source metric observations, view range 1,519-11,413
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/7`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/7`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 12 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-024"></a>
#### SokiLondon (`acct_yt_fragrance_024`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: Soki London
- Public account: [SokiLondon](https://www.youtube.com/channel/UCtBpe765Fy-USxg_L8hGDPg)
- Selected sort metric: `average_views` = 2,520 (observed)
- Median views: 2,113 (observed)
- Engagement rate: 4.01%
- Average like count: 92.56
- Average comment count: 9.62
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 26 source metric observations, view range 1,253-4,800
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/22`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/22`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 26 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-029"></a>
#### TheScentinel (`acct_yt_fragrance_029`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: The Scentinel
- Public account: [TheScentinel](https://www.youtube.com/channel/UCCyE5usoGzgd_FNuqC1pkHQ)
- Selected sort metric: `average_views` = 1,760.25 (observed)
- Median views: 1,837.50 (observed)
- Engagement rate: 7.93%
- Average like count: 111.50
- Average comment count: 23.33
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 11 source metric observations, view range 1,031-2,335
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/27`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/27`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 11 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-023"></a>
#### SimplyPutScents (`acct_yt_fragrance_023`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: Simply Put Scents
- Public account: [SimplyPutScents](https://www.youtube.com/channel/UCwpmex-DKwi6ARQlVa3-KcA)
- Selected sort metric: `average_views` = 829.20 (observed)
- Median views: 856 (observed)
- Engagement rate: 4.70%
- Average like count: 34.80
- Average comment count: 4.20
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 15 source metric observations, view range 510-1,062
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/21`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/21`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 15 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-yt-fragrance-017"></a>
#### ProfessorPerfume (`acct_yt_fragrance_017`)

- Platform: youtube
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public display name: Professor Perfume
- Public account: [ProfessorPerfume](https://www.youtube.com/channel/UC_1GYaGHE0luMX0j6utkeHg)
- Selected sort metric: `average_views` = 107 (observed)
- Median views: 107 (observed)
- Engagement rate: unavailable_with_reason (null)
- Average like count: 8
- Average comment count: unavailable_with_reason (null)
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `thin_n_1_to_3`, 2 source metric observations, view range 107-107
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-07-02T18:53:18Z; identity updated 2026-06-27T18:23:26Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`
- Limitations:
  - Profile is account-scoped to one youtube platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate, average likes, and average total comments are unavailable until source-backed numerator fields exist.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/16`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/16`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 2 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

### Instagram — Details

<a id="details-acct-ig-reels-001"></a>
#### hyram (`acct_ig_reels_001`)

- Platform: instagram
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public account: [hyram](https://www.instagram.com/hyram/)
- Selected sort metric: `average_views` = 145,593.33 (observed)
- Median views: 58,963.50 (observed)
- Engagement rate: 2.42%
- Average like count: 3,455.75
- Average comment count: 66
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 36 source metric observations, view range 32,183-741,197
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-06-30T14:15:50Z; identity updated 2026-06-29T13:47:06Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_instagram_reels_grid_engagement_v0`
- Limitations:
  - Profile is account-scoped to one instagram platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/30`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/instagram/instagram_reels_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/0`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/instagram/instagram_reels_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 36 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-ig-reels-004"></a>
#### milanscents (`acct_ig_reels_004`)

- Platform: instagram
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public account: [milanscents](https://www.instagram.com/milanscents/)
- Selected sort metric: `average_views` = 70,628.33 (observed)
- Median views: 45,850.50 (observed)
- Engagement rate: 3.77%
- Average like count: 2,552.92
- Average comment count: 108.17
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 36 source metric observations, view range 5,123-246,436
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-06-30T14:15:50Z; identity updated 2026-06-30T12:33:04Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_instagram_reels_grid_engagement_v0`
- Limitations:
  - Profile is account-scoped to one instagram platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/32`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/instagram/instagram_reels_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/2`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/instagram/instagram_reels_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 36 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

<a id="details-acct-ig-reels-002"></a>
#### jeremyfragrance (`acct_ig_reels_002`)

- Platform: instagram
- Identity state: `single_platform_observed` (`link_state_or_none`: null, `review_state_or_none`: null)
- Public account: [jeremyfragrance](https://www.instagram.com/jeremyfragrance/)
- Selected sort metric: `average_views` = 27,470.50 (observed)
- Median views: 16,994 (observed)
- Engagement rate: 1.24%
- Average like count: 319.08
- Average comment count: 21
- `posting_cadence`: not_attempted (null) — declared-deferred, not yet populated
- `recent_velocity`: not_attempted (null) — declared-deferred, not yet populated
- Sample support: `stronger_admitted_pool_n_8_plus`, 36 source metric observations, view range 4,960-147,919
- Representativeness posture: `admitted_pool_only_not_representative_creator_average`
- Freshness: metrics computed 2026-06-30T14:15:50Z; identity updated 2026-06-29T13:47:50Z; profile view computed 2026-07-02T14:10:00Z; rollup freshness_state `partial`
- Calculation recipe version: `creator_metric_rollup_instagram_reels_grid_engagement_v0`
- Limitations:
  - Profile is account-scoped to one instagram platform account; it is not a linked creator_record.
  - Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.
  - Engagement rate is source-backed only for the admitted/selected source pool; it is not a platform-wide engagement benchmark.
  - Ideal/content-fit audience profile is not joined in this static view.
  - Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.
  - Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.
  - The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.
- Non-claims (this row):
  - not channel-wide creator influence
  - not platform-wide engagement rate
  - not buyer proof
  - not public person-level identity
  - not contact or outreach authorization
  - not cross-platform rollup
  - not dashboard readiness
  - not SQLite or data-lake physicalization
- Source drill-back:
  - identity_ledger_pointer: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/platform_accounts/31`
  - metric_rollup_pointer: `orca/product/spines/capture/core/source_families/social_media/instagram/instagram_reels_creator_metric_rollup_snapshot_v0.json#/creator_metric_rollup_snapshot/metric_rollups/1`
  - metric_snapshot_pointer: `orca/product/spines/capture/core/source_families/social_media/instagram/instagram_reels_creator_metric_rollup_snapshot_v0.json`
  - source_metric_observation_ids: 36 ids recorded at the metric_snapshot_pointer above (not enumerated here for length)

## Non-Claims And Accepted Residuals

This library, at every row and at the library level, is not and does not imply:

- a leaderboard, winner/loser ranking, or competitive standing;
- a lead list, outreach list, recommended-creators list, or priority queue;
- outreach or contact authorization;
- buyer proof or product proof;
- a performance guarantee or prediction;
- cross-platform identity proof or a linked `creator_record` where none exists;
- universal or channel-wide creator influence;
- dashboard readiness, API readiness, SQLite adoption, data-lake physicalization, or capture-job authorization;
- validation, readiness, or implementation authorization beyond this static Markdown artifact.

Accepted residuals:

- Every profile in this projection is `platform_account`-scoped and `single_platform_observed`; no `creator_record` (cross-platform-linked) profile exists in the current data.
- `posting_cadence` and `recent_velocity` remain declared-deferred (`not_attempted`) for all 33 rows; this projection renders that state, it does not populate it.
- The ideal/content-fit audience section of the underlying `creator_profile_current` contract is exercised only in its always-null current state (`profiles_with_ideal_audience_profiles: 0`); this projection does not render a populated ideal-audience row because none exists, and does not claim to have exercised populated-row treatment.
- All rollups are admitted-pool or selected-grid statistics (`admitted_pool_only_not_representative_creator_average`), not channel-wide or representative creator averages, for every row.
- `link_state_or_none` and `review_state_or_none` are `null` for all 33 rows in the current data; this projection does not invent or imply a candidate/rejected/promoted link state.

## Source Drill-Back

Each row's Details entry carries its `identity_ledger_pointer`, `metric_rollup_pointer`, and `metric_snapshot_pointer` as repository-relative code paths with JSON-pointer fragments (`#/...`), exactly as recorded in the source view — not converted into public URLs and not claiming a source-access capability the JSON does not carry. A row's public account link (when present) is the source-recorded `public_profile_url` field itself, not a fabricated address.

