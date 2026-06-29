# Creator Metric Silver Record Contract v0

```yaml
retrieval_header_version: 1
artifact_role: source_capture_family_architecture_contract
scope: >
  Producer-owned Silver Vault record contract for creator metrics: the
  MetricObservation and the new MetricRollupObservation derived records emitted
  by the creator-metric Silver producer from Instagram reels-grid projections.
  Locks the rollup payload shape and the posture semantics so creator metrics
  become lake-native instead of a hand-kept static seed.
use_when:
  - Scoping or reviewing the creator-metric Silver producer.
  - Checking the MetricRollupObservation payload shape or rollup posture rules.
  - Deciding whether a computed aggregate may carry observed posture.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_native_record_mapping_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/instagram/instagram_reels_creator_metric_seed_v0.json
  - orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py
  - orca-harness/capture_spine/creator_profile_current/validation.py
stale_if:
  - The Silver Vault record contract changes the record header, MetricObservation, posture, or content_hash semantics.
  - The instagram_reels_creator_metric_seed rollup shape changes.
  - A later accepted producer schema supersedes MetricRollupObservation.
```

## Status

`CREATOR_METRIC_SILVER_RECORD_CONTRACT_V0`.

This is the producer-owned record shape named (but not defined) by the
creator-profile lake-native record mapping, whose accepted residual was: "No
lake producer yet ... Upgrade trigger: implementation scoping for a Silver
creator metric producer." Retrieval-only: not validation, readiness, backend
selection, dashboard, live capture, or cross-platform identity.

## What the producer emits

The creator-metric Silver producer
(`orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py`)
reuses the tested `instagram_reels_creator_metric_seed` computation (so metric
numbers do not drift) and re-emits, per Instagram reels-grid projection:

- one **MetricObservation** Silver Vault record per source-visible metric fact
  (per-content view/like/comment, per-account follower_count); and
- one **MetricRollupObservation** Silver Vault record per platform account
  (the account's selected-grid engagement rollup).

Both are `record_kind: observation` records carrying the Silver Vault common
header (`record_id`, `raw_anchor`, `lane_namespace`, `producer_id`,
`schema_version`, `producer_schema_version`, `content_hash` +
`content_hash_basis`, `payload_kind`, `producer_row_kind`, `source_surface`,
`observed_at`, `captured_at`, `raw_refs`, `derived_refs`) per the Silver Vault
record contract. `content_hash` uses the
`canonical_json_excluding_content_hash` basis.

### MetricObservation

Conforms to the Silver Vault record contract's MetricObservation discipline.
`payload.observation` carries `subject` (an `entity_key` ref), `metric_name`,
`metric_value`, `metric_posture` {`kind`, `reason_code`, `reason_detail`},
`coverage_window`, `source_surface`, `source_publication_or_event`,
`source_surface_count_candidates`, `unit`. Lane `creator_metric_silver`.
Anchored to its source projection's raw packet via `raw_refs`.

### MetricRollupObservation (new payload_kind)

`payload.observation` carries: `subject` (the platform-account `entity_key`),
`rollup_kind`, `platform_scope`, `platform_account_ids`, `rollup_window`,
`rollup_window_description`, `content_kind_inclusion_rule`, `metric_rollups`
(named aggregates, each `{metric_value, metric_posture, unit}`),
`observation_count`, `view_count_min`/`view_count_max`,
`calculation_recipe_version`, `computed_at`, `freshness_state`,
`sample_support`, `limitations`, `source_metric_observation_ids`. Lane
`creator_metric_rollup_silver`. The rollup's `derived_refs` carry one
`derived_from_record` edge per source MetricObservation record (lane, record_id,
content_hash) — the canonical Silver lineage, not a producer-private sidecar.

## Posture rule (the reviewable decision)

A rollup aggregate carries `metric_posture.kind: observed` with a numeric
`metric_value` ONLY when it is source-backed (numerator and denominator
observations exist). When inputs are absent or the recipe is out of scope it
carries a non-observed posture (e.g. `unavailable_with_reason`,
`not_attempted`) with `metric_value: null` and a reason. Missing is never zero.

This reuses the posture model the existing seeds and `validation.py` already
apply to the same aggregates (Instagram `average_views`/`engagement_rate:
observed`; YouTube `engagement_rate: unavailable_with_reason`). It is the
load-bearing contract choice in this v0 — applying the *observed* posture,
defined for source-visible facts, to a *computed* aggregate. It is named here
for the delegated review rather than assumed silently.

## Conformance and no-drift

- Every emitted record obeys the Silver posture/value coupling: observed ⇔
  numeric value and no reason; non-observed ⇔ null value and a reason (the
  producer fails closed on a violation rather than emitting a fake-shaped row).
- The producer does not compute metrics; rollup numbers equal the seed
  computation exactly (the producer test asserts no-drift).

## Accepted residuals (named, not hidden)

- v0 emits MetricObservation + MetricRollupObservation only. It does NOT emit
  PlatformAccountEntity / public_content_object entity records or the
  `content_published_by_account` relationship; the metric subject is carried as
  a self-describing `entity_key` reference.
- Observations carry `raw_refs` to the raw packet; the intermediate IG
  reels-grid projection is recorded in `provenance`, not a formal `derived_refs`
  edge, because the reused seed observation does not carry the projection
  record's lake address (lane/record_id/content_hash).
- The producer does not regenerate `creator_profile_current`; re-pointing the
  read model onto these records is a separate step.
- No cross-platform creator rollups; per-platform account subjects only.

## Non-Claims

- not validation
- not readiness
- not buyer proof
- not a representative creator average
- not channel-wide creator influence
- not cross-platform identity linkage
- not a follower graph or audience estimate
- not SQLite or backend selection
- not dashboard implementation
- not live capture authorization
