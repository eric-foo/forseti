# Aphrodite Silver Metric Monitoring Docs Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow handoff packet (documentation lane; not implementation authorization)
scope: >
  Fresh-lane handoff for updating Forseti Silver/Vault, creator registry, and
  runner-facing documentation so Aphrodite Signals can see which creator metrics
  are currently captured, which are currently monitorable, and which monitoring
  recipes are proposed but not yet implemented.
authority_boundary: retrieval_only
owner_request: >
  Update the lake/vault/runner documentation for the stats Aphrodite can capture
  or monitor, especially moving averages, EMA, and creator-registry monitoring
  metrics.
open_first:
  - docs/research/aphrodite_creator_capture_strategy_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_native_record_mapping_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_ledger_operational_evolution_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_monitoring_policy_architecture_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_momentum_pipeline_architecture_v0.md
  - forseti-harness/capture_spine/creator_profile_current/
  - forseti-harness/runners/
stale_if:
  - Creator metric Silver contracts, profile-current contracts, or runner entrypoints change.
  - Aphrodite capture strategy is superseded.
  - Moving-average, EMA, velocity, or breakout-state recipes are implemented before this handoff is consumed.
```

## Objective

Produce a documentation update, not a runtime change.

The receiver should inventory what Forseti already captures and can safely
monitor for creator accounts, then document the gap between:

- currently emitted source metric observations;
- currently emitted rollups;
- current freshness and revalidation checks;
- candidate Aphrodite monitoring recipes;
- forbidden, unsupported, or source-hidden stats.

This matters because Aphrodite Signals is tied directly to both Silver/Vault and
the creator registry. The product surface should not invent moving averages,
EMA, velocity, spike state, or breakout state inside Aphrodite. Those recipes
belong in Silver/MetricRollupObservation with lineage and posture, then can be
copied into creator_profile_current only after the recipe is accepted.

## Current Facts To Preserve

- Use `forseti/` and `forseti-harness/` paths.
- The creator registry and profile-current contracts are present in current
  main-line source.
- `creator_profile_current` already exposes average views, median views,
  average like count, average comment count, engagement rate, posting cadence,
  and recent velocity fields.
- `posting_cadence` and `recent_velocity` remain declared-deferred until
  compatible Silver history exists.
- `creator_metric_silver_record_contract_v0.md` owns source-visible
  MetricObservation and MetricRollupObservation records, with posture/value
  coupling and missingness discipline.
- A grep/source read is not proof that moving average or EMA already exists. If
  no implemented recipe is found, mark it proposed/deferred.

## Source Inventory

Inspect these before deciding where the docs change belongs:

- `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md`
- `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_ledger_operational_evolution_contract_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_native_record_mapping_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_monitoring_policy_architecture_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_momentum_pipeline_architecture_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_metric_silver_record_contract_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/instagram_reels_creator_metric_rollup_snapshot_v0.json`

Inspect these runner/code entrypoints for what is actually emitted today:

- `forseti-harness/capture_spine/creator_profile_current/instagram_metric_seed.py`
- `forseti-harness/capture_spine/creator_profile_current/youtube_metric_seed.py`
- `forseti-harness/capture_spine/creator_profile_current/youtube_watch_packet_metric_document.py`
- `forseti-harness/capture_spine/creator_profile_current/tiktok_metric_seed.py`
- `forseti-harness/capture_spine/creator_profile_current/silver_metric_producer.py`
- `forseti-harness/capture_spine/creator_profile_current/youtube_silver_metric_producer.py`
- `forseti-harness/capture_spine/creator_profile_current/tiktok_silver_metric_producer.py`
- `forseti-harness/capture_spine/creator_profile_current/silver_metric_reader.py`
- `forseti-harness/capture_spine/creator_profile_current/silver_metric_snapshot.py`
- `forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py`
- `forseti-harness/capture_spine/creator_profile_current/materialize.py`
- `forseti-harness/capture_spine/creator_profile_current/validation.py`
- `forseti-harness/capture_spine/creator_profile_current/live_lake_freshness_gate.py`
- `forseti-harness/runners/run_creator_metric_rollup_producer.py`
- `forseti-harness/runners/run_creator_metric_rollup_snapshot.py`
- `forseti-harness/runners/run_creator_rollup_formula_revalidation.py`
- `forseti-harness/runners/run_creator_profile_current_materialize.py`
- `forseti-harness/runners/run_live_lake_freshness_gate.py`
- `forseti-harness/runners/run_instagram_reels_creator_metric_seed_materialize.py`
- `forseti-harness/runners/run_youtube_creator_metric_rollup_producer.py`
- `forseti-harness/runners/run_youtube_watch_packet_metric_rollup_producer.py`
- `forseti-harness/runners/run_tiktok_batch_metric_rollup_producer.py`

## Recommended Documentation Shape

Add or update the nearest owning doc after source loading. The output should
include a compact table with these sections:

- platform and source surface;
- source-visible raw metric facts currently observed;
- current Silver rollup fields;
- current freshness, revalidation, and materialization runner;
- proposed Aphrodite monitoring recipe;
- required history window and sample support;
- posture/missingness behavior;
- recipe version and lineage owner;
- whether the stat is current, deferred, proposed, or forbidden.

Candidate Aphrodite monitoring recipes to document as proposed unless source
inspection proves they already exist:

- simple moving average over compatible recent observations;
- exponential moving average (EMA);
- compatible-window velocity;
- capture-window delta when publication timing is unavailable;
- spike score against creator baseline or platform/content-kind norm;
- breakout state;
- decay or plateau state;
- active-watch expiry state.

Do not document these as product-ready claims unless the implementation and
recipe source exist.

## Boundaries

- Do not implement moving average, EMA, velocity, spike score, or scheduler
  behavior in this lane.
- Do not run live capture, mutate the lake, or create new metric records.
- Do not hide derived metrics inside `creator_profile_current`.
- Do not turn Aphrodite Signals into the metric authority.
- Do not claim request-budget readiness or daily monitoring feasibility from
  this docs pass alone.

## Validation

For docs-only output, run:

```powershell
rg -n "orca[/\\]product|orca[-]harness" <touched-docs>
python .agents/hooks/check_placement.py --strict
git diff --check
```

If code changes are made despite this handoff's intended scope, run the nearest
runner or unit tests for the touched code and explain why code was necessary.