# Creator Signal Multi-Creator Library - Client Projection v0

```yaml
retrieval_header_version: 1
artifact_role: product_signal_client_projection
scope: >
  Client-readable static projection of the Creator Signal Library over the
  reviewed 33-row multi-creator static projection, with audit detail kept
  reachable but not shown as the default scan experience.
use_when:
  - Creating or reviewing a client-facing Creator Signal Library preview.
  - Checking how to progressively disclose limitations, non-claims, and source drill-back from the static projection.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/creator_signal/creator_signal_multi_creator_library_static_projection_v0.md
  - forseti/product/spines/creator_signal/creator_signal_multi_creator_library_surface_v0.md
stale_if:
  - creator_signal_multi_creator_library_static_projection_v0.md row counts, platform mix, metric postures, or row order change.
  - A later accepted contract authorizes cross-platform rollups, populated ideal-audience rows, outreach use, or populated posting_cadence/recent_velocity.
```

## Boundary

This is the client-readable version of the reviewed static projection. It is still a static source-backed view, not a dashboard, API, CRM list, source of truth, buyer proof, product proof, selection engine, or outreach authorization.

The default view is intentionally lighter than the audit projection: rows show the scan metrics and trust posture a client needs to interpret the table, while full limitations, non-claims, calculation lineage, and source drill-back stay one click away through each row's audit link.

## What This Shows

- 33 currently committed creator-profile rows: 30 YouTube, 3 Instagram.
- Platform-separated library sections. There is no combined YouTube+Instagram ordering.
- Table order is `average_views` descending within each platform only.
- `average_views` and engagement are admitted-pool metrics, not channel-wide creator averages.
- `posting_cadence` and `recent_velocity` are not yet available for every row.

## What This Does Not Prove

This library does not prove buyer readiness, audience fit, creator quality, cross-platform identity, representative channel-wide performance, or outreach priority. Use the audit links when a row needs explanation beyond the compact trust cue shown in the table.

## YouTube Library View

| Creator | Platform | Subject ID | Avg views | Engagement | Sample | Freshness | Cadence / velocity | Scan caveat | Audit |
|---|---|---|---:|---:|---|---|---|---|---|
| [JusDeRose](https://www.youtube.com/channel/UCflkhyQuNBeiw3__1TUXXNg) | YouTube | `acct_yt_fragrance_012` | 160,954.29 | 3.46% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-012) |
| [GentsScents](https://www.youtube.com/channel/UC9IImcLkUdmURWtQhxu8VwQ) | YouTube | `acct_yt_fragrance_010` | 127,654.08 | 3.29% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-010) |
| [OliviaOlfactory](https://www.youtube.com/channel/UCRGkzuXpYq4hCDGKe-9P50g) | YouTube | `acct_yt_fragrance_015` | 104,980.60 | 9.90% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-015) |
| [DemiRawling](https://www.youtube.com/channel/UC88iYYngvMLb_3obJKMCI3w) | YouTube | `acct_yt_fragrance_006` | 100,543.50 | 1.71% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-006) |
| [TheScented](https://www.youtube.com/channel/UCHqrJNnjF_3yHfVDatKl-NA) | YouTube | `acct_yt_fragrance_028` | 73,836 | 4.54% | limited | 2026-07-02 (partial) | not yet available | limited sample; admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-028) |
| [CurlyScents](https://www.youtube.com/channel/UCIfiNVTfW49L7Z3lGLfIOeA) | YouTube | `acct_yt_fragrance_005` | 64,618.90 | 2.73% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-005) |
| [CurlyFragrance](https://www.youtube.com/channel/UCcwPIKNTMO5S-Vd7z-RrIhg) | YouTube | `acct_yt_fragrance_004` | 48,680 | 5.44% | thin | 2026-07-02 (partial) | not yet available | thin sample; admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-004) |
| [SchoolofScent](https://www.youtube.com/channel/UC7yWwH6peQbpfLMVKKuR-xg) | YouTube | `acct_yt_fragrance_022` | 32,946.92 | 2.51% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-022) |
| [BowTieFragranceGuy](https://www.youtube.com/channel/UCVvzGrPSok_sf8hfDhvTg7w) | YouTube | `acct_yt_fragrance_001` | 27,558.80 | 6.46% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-001) |
| [PostCologne](https://www.youtube.com/channel/UCArpB-dspQ5Ax3pJnj0Rnog) | YouTube | `acct_yt_fragrance_016` | 25,756 | 3.72% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-016) |
| [MonikaCioch](https://www.youtube.com/channel/UCi42yeT0_OLeouUQhDBVZjQ) | YouTube | `acct_yt_fragrance_014` | 24,483 | 3.22% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-014) |
| [ChaosFragrances](https://www.youtube.com/channel/UC0fOGtvT1x8irPUZOFdF2mA) | YouTube | `acct_yt_fragrance_002` | 24,352.33 | 4.17% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-002) |
| [FragranceKnowledge](https://www.youtube.com/channel/UCzH0Tal9pApj-F6KSGZHo4Q) | YouTube | `acct_yt_fragrance_007` | 18,888.71 | 2.29% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-007) |
| [Redolessence](https://www.youtube.com/channel/UCuSy0Z5UwvkMQ7lXRbUdOnQ) | YouTube | `acct_yt_fragrance_018` | 16,965.08 | 4.67% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-018) |
| [ThePerfumeGuy](https://www.youtube.com/channel/UCFarEEFsV90-pvUU0XdUdgQ) | YouTube | `acct_yt_fragrance_026` | 15,496.91 | not available | strong | 2026-07-02 (partial) | not yet available | admitted-pool only; engagement unavailable | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-026) |
| [TiffBenson](https://www.youtube.com/channel/UC4lKHUYqvm74znBF6qSnYig) | YouTube | `acct_yt_fragrance_030` | 12,634.33 | 4.89% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-030) |
| [TheFragranceApprentice](https://www.youtube.com/channel/UCMz0tE1qg5SwmrAF3Cshe0A) | YouTube | `acct_yt_fragrance_025` | 11,828.38 | 4.81% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-025) |
| [ScentedMoments](https://www.youtube.com/channel/UCd7OAY06IuwYsUoWsn3gbuQ) | YouTube | `acct_yt_fragrance_020` | 11,644.67 | 3.02% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-020) |
| [ThePerfumeNest](https://www.youtube.com/channel/UCyU1XUvAFqV2X1NVCcRqRNA) | YouTube | `acct_yt_fragrance_027` | 7,644.11 | 6.58% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-027) |
| [MilaLeBlanc](https://www.youtube.com/channel/UCta4sjQtsMUtBCkI811ocfA) | YouTube | `acct_yt_fragrance_013` | 7,349.88 | 2.63% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-013) |
| [Cubaknow](https://www.youtube.com/channel/UCzhBUw8MLmUl8cPMx63sFuw) | YouTube | `acct_yt_fragrance_003` | 6,877.67 | 6.10% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-003) |
| [TLTGReviews](https://www.youtube.com/channel/UCmYZrY_MVZy5Iiwlua029kg) | YouTube | `acct_yt_fragrance_031` | 6,293.83 | 4.98% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-031) |
| [JeremyFragrance](https://www.youtube.com/channel/UCzKrJ5NSA9o7RHYRG12kHZw) | YouTube | `acct_yt_fragrance_011` | 6,215 | 1.27% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-011) |
| [Scenteno](https://www.youtube.com/channel/UC8gjOYz9aonQqd5HwoTu2NQ) | YouTube | `acct_yt_fragrance_021` | 5,101.50 | 3.03% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-021) |
| [funmimonet](https://www.youtube.com/channel/UCULGc5bSAoCIUMc-hQpjCXw) | YouTube | `acct_yt_fragrance_009` | 4,519.38 | 2.18% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-009) |
| [FragranceView](https://www.youtube.com/channel/UC_Zj9atmpE2MQBtzTfqDFfw) | YouTube | `acct_yt_fragrance_008` | 4,088.25 | 3.83% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-008) |
| [SokiLondon](https://www.youtube.com/channel/UCtBpe765Fy-USxg_L8hGDPg) | YouTube | `acct_yt_fragrance_024` | 2,520 | 4.01% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-024) |
| [TheScentinel](https://www.youtube.com/channel/UCCyE5usoGzgd_FNuqC1pkHQ) | YouTube | `acct_yt_fragrance_029` | 1,760.25 | 7.93% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-029) |
| [SimplyPutScents](https://www.youtube.com/channel/UCwpmex-DKwi6ARQlVa3-KcA) | YouTube | `acct_yt_fragrance_023` | 829.20 | 4.70% | strong | 2026-07-02 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-023) |
| [ProfessorPerfume](https://www.youtube.com/channel/UC_1GYaGHE0luMX0j6utkeHg) | YouTube | `acct_yt_fragrance_017` | 107 | not available | thin | 2026-07-02 (partial) | not yet available | thin sample; admitted-pool only; engagement unavailable | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-yt-fragrance-017) |

## Instagram Library View

| Creator | Platform | Subject ID | Avg views | Engagement | Sample | Freshness | Cadence / velocity | Scan caveat | Audit |
|---|---|---|---:|---:|---|---|---|---|---|
| [hyram](https://www.instagram.com/hyram/) | Instagram | `acct_ig_reels_001` | 145,593.33 | 2.42% | strong | 2026-06-30 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-ig-reels-001) |
| [milanscents](https://www.instagram.com/milanscents/) | Instagram | `acct_ig_reels_004` | 70,628.33 | 3.77% | strong | 2026-06-30 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-ig-reels-004) |
| [jeremyfragrance](https://www.instagram.com/jeremyfragrance/) | Instagram | `acct_ig_reels_002` | 27,470.50 | 1.24% | strong | 2026-06-30 (partial) | not yet available | admitted-pool only | [audit](creator_signal_multi_creator_library_static_projection_v0.md#details-acct-ig-reels-002) |

## Progressive Disclosure

Default client view:

- Show the platform sections and compact row table.
- Keep table order framed as a within-platform metric sort, not creator standing.
- Keep `Sample`, `Freshness`, `Cadence / velocity`, and `Scan caveat` visible on every row.

When the client asks "why this row?" or "what does this not prove?":

- Open the row's audit link.
- Use the linked audit entry for full limitations, non-claims, calculation recipe, and source drill-back.
- Do not summarize unavailable or deferred values as zero.

## Accepted Residuals

- Every row is a single-platform account, not a cross-platform creator record.
- No ideal-audience profile is populated in the current data.
- No cross-platform rollup exists.
- `posting_cadence` and `recent_velocity` are not yet populated for any row.
- Source-pool-limited metrics are not channel-wide performance evidence and are not an outreach basis by themselves.
