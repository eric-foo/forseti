# YouTube Creator Observation Ledger Spec v0

```yaml
retrieval_header_version: 1
artifact_role: source_capture_family_spec
scope: >
  YouTube-first creator/channel observation ledger contract for admitted Shorts
  pools. Defines the static source-backed observation shape used before metric
  rollups, creator profile projection, SQLite, or cross-platform linkage.
use_when:
  - Populating source-backed YouTube creator/channel observations from admitted Shorts pools.
  - Checking whether a YouTube creator/channel row may seed platform_account inputs for creator_profile_current.
  - Distinguishing one-platform creator observations from IG/TikTok/YouTube public-handle linkage.
open_next:
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_observation_ledger_v0.json
  - docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.json
  - docs/workflows/youtube_shorts_creator_index_decision_path_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_video_capture_surface_findings_v0.md
  - orca-harness/capture_spine/youtube_creator_observation/validation.py
stale_if:
  - The YouTube Shorts fragrance creator source ledger changes.
  - Data Lake raw packet layout or source-family metadata changes.
  - A later accepted social-media creator observation contract supersedes the YouTube-first shape.
  - The creator profile current view changes where metric observations or rollups belong.
authority_boundary: retrieval_only
```

## Status

`YOUTUBE_FIRST_CREATOR_OBSERVATION_CONTRACT_V0`.

This contract records a one-platform creator/channel observation ledger. It is
the correct first step for the current 200-Shorts fragrance pool because the
available evidence is strong for YouTube channel observations and not sufficient
for cross-platform identity stitching.

The seed artifact is:

`orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_observation_ledger_v0.json`

It is a full census of the current admitted pool: 200 Shorts, 31 observed
creator/channel groups, 30 non-brand creator/channel observations, and one
brand/platform account observation. It is not a sample and not a market-proof
claim.

## Boundary

This ledger is not the public-handle linkage ledger.

- Use this ledger for source-backed YouTube account/channel observations under
  a niche or sub-niche.
- Use `creator_public_handle_linkage_ledger_v0.json` only when there is public
  evidence linking accounts across Instagram, TikTok, and YouTube.
- Use `creator_profile_current_view_spec_v0.md` for the one-stop joined view
  over identity, per-content metric observations, metric rollups, and
  ideal-audience snapshots.

Do not force YouTube-only rows into `creator_records` in the linkage ledger.
Those rows require at least two platforms and account-link evidence.

A YouTube observation row may seed a `platform_account` subject for
`creator_profile_current`. Similar YouTube, Instagram, or TikTok accounts may be
soft-linked only as `candidate_public_account_link` rows in the public-handle
linkage ledger until human review promotes or rejects the link.

## Ledger Shape

The static JSON ledger uses a single wrapper:

```yaml
youtube_creator_observation_ledger:
  schema_version: youtube_creator_observation_ledger_v0
  ledger_id: stable artifact id
  ledger_mode: source_backed_static_fixture
  compiled_at_utc: compilation timestamp
  source_policy_posture: boundary summary
  authority_pointers: source contracts and workflow route
  source_inputs: source artifacts and data-lake root marker facts
  niche_scope: domain/subdomain/platform membership basis
  counts: row, video, packet, and residual counts
  metric_rollup_policy: metric absence and next-step rule
  creator_observations: row list
  accepted_residuals: source-backed caveats
  non_claims: explicit non-claims
```

Each `creator_observation` row is one observed YouTube channel/account cluster
inside the admitted source pool. Required row fields:

```yaml
creator_observation:
  creator_observation_id: stable ledger-local row id
  platform: youtube
  platform_subject_key_type: youtube_channel_id
  platform_subject_key: observed YouTube channel id
  public_profile_url: public channel URL from the channel id
  creator_handle_query: source/capture query label, not guaranteed current @handle
  creator_classification: creator_or_channel_observed or brand_or_platform_account_observed
  identity_boundary: explicit one-platform observation boundary
  niche_scope: niche/sub-niche label
  source_pool_id: admitted pool id
  admitted_video_count: count of admitted Shorts represented by the row
  observed_author_names: observed public author/display-name values with counts
  source_observed_channel_ids: original source-ledger channel-id buckets
  resolved_lake_channel_ids: channel ids resolved from data-lake packet metadata
  lake_channel_id_missing_video_count: count of row videos whose packet metadata lacks channel id
  source_artifact_counts: source artifacts contributing row videos
  pool_ids: source pool row ids
  video_ids: all video ids for the row
  sample_shorts_urls: sample public URLs only
  data_lake_packet_refs: raw packet refs for all videos
  transcript_word_count_min: observed pool word-count minimum
  transcript_word_count_max: observed pool word-count maximum
  known_label_status_counts_100_pool_only: labeling status from the earlier 100-pool subset
  unlabeled_rows_in_pool200: remaining unlabeled rows in the 200 pool
  handle_source_pointer: pointer to the source handle-query value
  display_name_source_pointer: pointer to source display-name observations
  video_membership_source_pointer: pointer to source video membership
  lake_reconciliation_status: packet reconciliation status
  limitations: row-level caveats
  non_claims: row-level non-claims
```

## Source Requirements

A row is admissible only when:

- it comes from a bounded source pool with explicit row membership;
- it has at least one stable YouTube channel id, unless the row is explicitly
  marked unresolved;
- every `video_id` resolves to a data-lake raw packet or carries an explicit
  missing-packet residual;
- transcript bodies are not copied into the ledger;
- per-video metrics are not smuggled into the creator row unless a metric
  observation contract owns them.

The current seed artifact reconciles every video id to the external lake root
UUID `01KW1E6N133JT0XCN2KCN0V5A4`.

## Metrics Boundary

The current caption/audio packets do not carry views, likes, comment counts,
average views, or engagement rate. Do not store missing metrics as zero.

Average views and engagement rate belong in later metric observation and
metric rollup records. The current YouTube surface findings show where exact
views/likes can be captured, but this ledger does not execute that capture.

## Non-Claims

This spec and its seed ledger are not:

- cross-platform identity linkage;
- public-handle stitching evidence;
- real-world identity proof;
- creator quality ranking;
- buyer proof;
- contact, outreach, or lead-list authorization;
- follower or audience graph work;
- platform authority for cross-platform identity;
- metric rollup storage;
- SQLite migration;
- live capture authorization;
- dashboard implementation.

## Direction Change Propagation

```yaml
direction_change_propagation:
  trigger: product_doctrine
  doctrine_changed: >
    Adds a YouTube-first creator/channel observation contract and seed ledger
    so the existing 200-Shorts pool can become source-backed creator
    infrastructure without overstating cross-platform identity or metric
    readiness.
  controlling_sources_updated:
    - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_observation_ledger_spec_v0.md
    - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_observation_ledger_v0.json
    - orca-harness/capture_spine/youtube_creator_observation/validation.py
    - orca-harness/tests/unit/test_youtube_creator_observation_ledger.py
  downstream_surfaces_checked:
    - docs/workflows/youtube_shorts_creator_index_decision_path_v0.md
    - orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md
    - orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md
    - orca/product/spines/capture/core/source_capture_toolbox/README.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_v0.json
      reason: Current evidence is YouTube-only observation evidence, not cross-platform account-link evidence.
  non_claims:
    - not cross-platform identity linkage
    - not metric rollup storage
    - not SQLite migration
    - not runtime capture authorization
```
