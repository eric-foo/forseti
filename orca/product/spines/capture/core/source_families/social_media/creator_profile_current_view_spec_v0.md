# Creator Profile Current View Spec v0

```yaml
retrieval_header_version: 1
artifact_role: source_capture_family_architecture_contract
scope: >
  Owner-directed architecture contract for the current creator profile view: a
  one-stop operator/dashboard surface that joins public-handle identity linkage,
  per-content metric observations, aggregate metric rollups, and ideal-audience
  profile snapshots without turning the identity ledger into one giant ledger.
  This is not runtime storage, not SQLite adoption, not a live dashboard, not
  capture execution, and not a public person-level product surface.
use_when:
  - Designing the one-stop creator profile surface for internal creator intelligence.
  - Deciding where average views, engagement rate, and other aggregate creator metrics belong.
  - Checking the boundary between the public-handle identity ledger, metric observations, metric rollups, ideal-audience enrichment, and future SQLite/data-lake storage.
open_next:
  - orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_v0.json
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_ideal_audience_inference_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
  - orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
stale_if:
  - The creator public-handle linkage ledger moves to SQLite or another database schema.
  - A later accepted artifact defines a different creator profile view, dashboard contract, or creator-intelligence surface without explicitly reconciling with this spec and the Creator Signal surface.
  - Metric rollup storage, ideal-audience schema home, or Data Lake physicalization is adopted in a way that supersedes this view contract.
  - The wind-caller carve-out changes public stats, aggregate audience, or person-level surface boundaries.
authority_boundary: retrieval_only
```

## Status

`OWNER_DIRECTED_TARGET_VIEW_CONTRACT_V0`.

The owner accepted the split: not one giant ledger; individual reels/videos and
their metrics belong in metric observation records; average/aggregate influence
belongs in rollups; the operator needs a one-stop current profile that can later
become a dashboard.

This document records the target view and placement. It does not add real
creator rows, choose SQLite, create runtime tables, authorize live capture,
start a data-lake job, or claim validation/readiness.

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: true
  overlay_read: true
  cynefin_route: complicated
  source_pack: custom_creator_profile_current_view
  edit_permission: docs_write
  isolation: existing clean worktree codex/creator-ledger-static-fixture
  target_scope:
    - orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md
    - orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md
    - orca/product/spines/capture/core/source_capture_toolbox/README.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/workflows/orca_repo_map_v0.md
  blocked_if_missing:
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/decisions/wind_caller_calibration_carveout_v0.md
    - orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md
    - orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_ideal_audience_inference_spec_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
```

## Placement Decision

The one-stop creator profile contract lives at the social-media source-family
level:

`orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md`

Why this home:

- The current profile joins Instagram, TikTok, YouTube, and later social creator
  inputs, so it does not belong inside the IG-only folder.
- It is a product/source-family contract, so it belongs under `orca/product/`,
  not `docs/hygiene/` or `docs/workflows/`.
- It is not runtime storage, so it does not belong in `orca-harness/`.
- It references Data Lake storage and future SQLite physicalization, but those
  are implementation/storage homes; they are not the source of truth for this
  product view contract.

The public-handle identity ledger remains at:

`orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_v0.json`

A future static/manual creator-profile artifact, if needed before SQLite, should
live beside this spec, for example:

`orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_v0.json`

That future artifact should be derived from source-backed identity, metric, and
audience records. It should not be manually edited as a second source of truth
once a data-lake/SQLite physicalization exists.

## Architecture Result

Use a **view over siblings**, not one giant ledger.

```text
creator_public_handle_linkage_ledger
  -> stable public creator/account cluster ids
  -> platform accounts and link evidence

creator_metric_observations
  -> individual reels/videos/profile metric facts
  -> value + posture + source pointer + content/account key

creator_metric_rollups
  -> average views, engagement rate, velocity, cadence
  -> computed over windows from metric observations

creator_ideal_audience_profile_snapshots
  -> ideal/content-fit audience fields and evidence pointers
  -> actual audience remains not_estimated unless separately authorized

creator_profile_current
  -> current one-stop joined view for operator/dashboard use
```

The first three layers keep truth and provenance separate. The last layer is the
surface the operator opens.

## Core / Satellite Boundary

Core identity spine:

- `creator_record_id` from the public-handle linkage ledger is the join key for
  creator-level views.
- `platform_account_id` is the join key for account-level metric rollups.
- Identity rows record account linkage evidence only.
- Identity rows must not absorb metric values, audience labels, follower graphs,
  contact fields, outreach fields, or person-identity claims.

Metric satellites:

- `creator_metric_observation` records individual source-visible metric facts.
- `creator_metric_rollup` records aggregate/current influence measures computed
  from observations.
- Rollups carry a calculation recipe/version, source window, freshness timestamp,
  and limitation state.
- Absence, hidden counts, blocked access, not-applicable metrics, and
  out-of-window facts must not be stored as observed zeroes.

Audience satellites:

- Ideal-audience Tier-1 fields may join into the current profile as content-fit
  enrichment.
- Tier-2-A aggregate audience demographic fields remain gated on a schema home
  and sourced base-rate/data prerequisites.
- Actual audience is not estimated by this view.

Current profile view:

- `creator_profile_current` is a derived view, materialized view, JSON export,
  dashboard query, or equivalent current snapshot.
- It may denormalize for operator convenience.
- It must preserve pointers back to the source sibling rows, versions, and
  freshness fields.
- It is not the source of truth for identity, metrics, or audience inference.

## Suggested Record Shapes

These are architecture contracts, not implemented schemas.

```yaml
creator_metric_observation:
  metric_observation_id: required stable id
  creator_record_id: required linkage-ledger id
  platform_account_id: required platform account id
  platform: required enum instagram, tiktok, youtube
  content_id_or_none: nullable platform-local content id
  content_url_or_none: nullable public content URL
  content_kind: required enum profile, reel, short, video, post, unknown
  metric_name: required enum/family-owned token
  metric_value_or_none: required when posture is observed
  metric_unit: required enum count, rate, ratio, percent, rank, other
  metric_posture: required enum observed, unavailable_with_reason, out_of_window, not_attempted, not_applicable
  posture_reason_or_none: required when posture is not observed
  source_pointer: required pointer to packet/projection/source row
  source_field: required source field or JSON pointer
  observed_at: required timestamp
  capture_window_start_or_none: nullable timestamp
  capture_window_end_or_none: nullable timestamp
  metric_registry_version: required version
  limitation_notes: optional list
```

```yaml
creator_metric_rollup:
  metric_rollup_id: required stable id
  creator_record_id: required linkage-ledger id
  platform_scope: required enum instagram, tiktok, youtube, cross_platform
  platform_account_ids: required list
  rollup_window: required enum 7d, 30d, 90d, lifetime_known, custom
  metric_rollups:
    average_views: nullable number with posture
    median_views: nullable number with posture
    engagement_rate: nullable number with posture
    average_like_count: nullable number with posture
    average_comment_count: nullable number with posture
    posting_cadence: nullable number with posture
    recent_velocity: nullable number with posture
  source_metric_observation_ids: required list
  calculation_recipe_version: required version
  computed_at: required timestamp
  freshness_state: required enum current, stale, partial, blocked
  limitations: required list
```

```yaml
creator_ideal_audience_profile_snapshot:
  audience_profile_snapshot_id: required stable id
  creator_record_id: required linkage-ledger id
  platform_scope: required enum instagram, tiktok, youtube, cross_platform
  observation_window_start: required timestamp
  observation_window_end: required timestamp
  actual_audience: required literal not_estimated
  tier_1_profile:
    segment: nullable label with support band
    audience_role: nullable label with support band
    purchase_intent: nullable label with support band
    skill_level: nullable label with support band
    price_tier: nullable label with support band
  tier_2a_profile_or_none: nullable gated aggregate-audience slice
  evidence_ids: required list
  fusion_config_version: required version
  computed_at: required timestamp
  limitations: required list
```

```yaml
creator_profile_current:
  creator_record_id: required linkage-ledger id
  link_state: required from identity ledger
  review_state: required from identity ledger
  platform_accounts: required joined public handles
  identity_evidence_summary: required short summary and pointers
  current_metric_rollups: required latest non-stale rollups by platform/window
  ideal_audience_profile: nullable latest allowed profile snapshot
  wind_calling_summary: nullable derived operator summary
  freshness:
    identity_updated_at: required timestamp
    metrics_computed_at_or_none: nullable timestamp
    audience_computed_at_or_none: nullable timestamp
    profile_view_computed_at: required timestamp
  limitations: required list
  non_claims: required list
```

## Aggregate Influence Rules

Average views and engagement rate belong in `creator_metric_rollup`, not in the
identity ledger.

Minimum rollup rules:

- Always state the window: 7d, 30d, 90d, or custom.
- Always state the platform scope: one platform or cross-platform.
- Always state which observation rows fed the rollup.
- Always carry `computed_at` and `freshness_state`.
- Never treat hidden, blocked, absent, or not-applicable metrics as observed
  zeroes.
- Never mix reels/videos/posts without a recipe version that explains the
  content-kind inclusion rule.
- Never present an aggregate as current if its source window or computation is
  stale.

## Dashboard Boundary

`creator_profile_current` is the dashboard-ready surface.

Allowed dashboard use:

- show one creator with linked public accounts;
- show latest average/aggregate influence metrics;
- show the source window and freshness for each aggregate;
- show the ideal-audience/content-fit profile when available;
- show limitations and missing-data states;
- drill back to source observations and evidence.

Forbidden dashboard use:

- contact/outreach authorization;
- lead-list export;
- public person-level directory;
- legal-name or real-world identity proof;
- follower graph or individual audience-member retention;
- actual audience demographics unless a later accepted schema home and data
  gate authorize the aggregate slice;
- unstamped, sourceless, or LLM-only influence claims.

## Creator Signal Boundary

The promoted Creator Signal surface lives at:

`orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md`

This Capture spec still owns `creator_profile_current`, sibling record shapes,
join/denormalization mechanics, and capture-side dashboard allowed/forbidden use.
Creator Signal owns the product-facing interpretation and presentation of that
view: which facts matter to an Orca operator or buyer, how they are grouped, what
claims the surface may make, and which limitations must remain visible.

The Creator Signal surface must reconcile with this `Dashboard Boundary` and
inherit rather than relax its forbidden-use set.

## SQLite And Data Lake Boundary

SQLite can be a good later physical home, but it is not the next product
decision by itself.

The next correct sequence is:

1. Lock the table/view contract in product docs.
2. Test source-backed real identity rows and metric observation/rollup examples.
3. Promote to SQLite or another storage engine only after the sibling record
   shapes survive real rows and failure cases.

When physicalized, SQLite tables can map directly from the sibling shapes:

- `creator_records`
- `platform_accounts`
- `account_link_evidence`
- `creator_metric_observations`
- `creator_metric_rollups`
- `creator_ideal_audience_profile_snapshots`
- `creator_profile_current`

Data Lake owns storage/derived-result mechanics when adopted. This product
contract owns the view boundary and source-family semantics. A data-lake job may
compute the rollups later, but this document does not create that job.

## Non-Goals

This spec does not:

- create a database;
- choose SQLite;
- create a dashboard;
- add real creator rows;
- authorize live capture;
- authorize new source access;
- define the full data-lake physical schema;
- define a scoring model for wind-calling strength;
- create a public creator directory;
- authorize outreach, contact enrichment, or lead-list use;
- claim buyer proof, validation, readiness, or commercial usefulness.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca now has an owner-directed creator-profile-current target view: the
    operator/dashboard one-stop creator surface is a derived join over sibling
    identity, metric observation, metric rollup, and ideal-audience profile
    records, not one giant identity ledger; average views and engagement rate
    belong in metric rollups keyed to the creator/account spine, with SQLite or
    another storage engine deferred until real-row tests prove the sibling
    shapes.
  trigger: architecture_doctrine
  related_triggers:
    - product_doctrine
    - lifecycle_boundary
  controlling_sources_updated:
    - orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md
    - orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md
    - orca/product/spines/capture/core/source_capture_toolbox/README.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/decisions/wind_caller_calibration_carveout_v0.md
    - orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_ideal_audience_inference_spec_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
  intentionally_not_updated:
    - path: orca-harness/capture_spine/creator_public_handle_linkage/
      reason: >
        This is a docs/product target-view contract. The existing validator
        continues to validate only the identity linkage ledger and should not
        absorb metric/audience/dashboard fields.
    - path: orca-harness/source_capture/models.py
      reason: >
        This pass authorizes no runtime schema, packet mutation, metric rollup
        computation, or data-lake physicalization.
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
      reason: >
        The storage contract already defers engine/backend selection and
        physicalization; this product spec references it without changing the
        lake boundary.
  stale_language_search: >
    rg -n "creator_profile_current|creator profile current|creator_profile_current_view|one giant ledger|average views|engagement rate|creator metric rollup|ideal audience"
    orca/product docs/workflows docs/decisions orca-harness
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not SQLite adoption
    - not live capture authorization
    - not dashboard implementation
    - not public person-level product surface
```