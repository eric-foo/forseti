# Forseti Creator Signal Spine Promotion Binding v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: >
  Binds forseti/product/spines/creator_signal/ as an accepted product_signal spine.
  This is a spine promotion and boundary binding for the creator-intelligence
  product surface; it does not move Capture contracts, create runtime storage,
  build a dashboard, or authorize live capture/outreach.
use_when:
  - Deciding whether creator-intelligence profile, influence, and buyer/operator presentation artifacts are Creator Signal-owned.
  - Checking the boundary between Creator Signal and low-level Capture/Data Lake creator records.
  - Authoring or changing the creator intelligence profile surface.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/creator_signal/README.md
  - forseti/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
  - docs/decisions/forseti_spine_first_target_structure_binding_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
  - .agents/workflow-overlay/artifact-folders.md
supersedes: []
stale_if:
  - The owner rejects or renames the Creator Signal spine.
  - The low-level creator profile current view, identity linkage ledger, metric rollup contract, or ideal-audience home is superseded.
  - A later accepted artifact gives Creator Signal storage, capture, outreach, or public-directory ownership.
```

## Status

Owner-accepted **spine-promotion binding**, v0 (2026-06-28). The owner accepted a
high-level Creator Signal product/signal home after a delegated review-and-patch
return was adjudicated on branch `codex/creator-ledger-static-fixture`.

This binds the spine identity and first surface contract. It does **not** create
SQLite, data-lake jobs, a dashboard runtime, real creator rows, live capture,
contact enrichment, outreach, or a public creator directory.

## Decision

`forseti/product/spines/creator_signal/` is an accepted **product_signal spine** under
`orca/product/spines/`.

It earns a high-level home because the owner wants an Orca-facing and
buyer-facing creator intelligence experience: a one-stop view of creator identity
links, platform accounts, aggregate influence, ideal/content-fit audience signal,
freshness, source drill-back, and limitations. That product surface should not
turn the low-level identity ledger into one giant ledger.

### Spine identity (bound)

```yaml
name: creator_signal
spine_kind: product_signal
root: forseti/product/spines/creator_signal/
consumes:
  - capture creator_profile_current view
  - capture public-handle identity linkage
  - capture metric observation and metric rollup records
  - ideal-audience profile snapshots and ballot taxonomy
  - data_lake storage and derived-result mechanics when later physicalized
owns:
  - creator intelligence product surface contracts
  - operator/buyer information architecture for creator profiles
  - product-facing claim language for creator fit and aggregate influence
  - required freshness, limitation, and source-drill-back displays
  - product-facing non-claims for creator signal use
does_not_own:
  - public-handle identity ledger rows
  - platform account linkage evidence
  - individual reel/video metric observations
  - metric rollup computation recipes
  - ideal-audience inference schemas or label taxonomy
  - SQLite, data-lake storage, or any physical storage engine
  - raw capture, scraping, runners, schedulers, or data-lake jobs
  - dashboard runtime or application implementation
  - public person-level directories
  - contact enrichment, outreach authorization, or lead-list export
```

## Bound Shape

The first accepted shape is intentionally small:

```text
forseti/product/spines/creator_signal/
  README.md
  creator_intelligence_profile_surface_v0.md
```

No subfolders are bound yet. Future `surfaces/`, `dashboards/`, `schemas/`,
`migrations/`, `harness/`, or `tests/` folders require a later accepted decision
or route update. Decisions, prompts, reviews, research, and migration records
stay in `docs/`; runtime code and tests stay in `orca-harness/` unless separately
authorized.

## Capture Boundary

Capture keeps the derived current view and the sibling record mechanics:

- `creator_public_handle_linkage_ledger_v0.json` and its spec own stable public
  creator/account linkage rows and evidence.
- `creator_profile_current_view_spec_v0.md` owns the low-level derived view over
  identity, metric observations, metric rollups, and ideal-audience snapshots.
- Average views, engagement rate, and similar aggregate influence facts belong
  in `creator_metric_rollup`, not in identity rows.
- The ideal-audience inference spec and ballot taxonomy own the Tier-1 fields and
  label vocabulary. Creator Signal only decides how the allowed profile is shown
  and what it may claim.

Creator Signal owns the product interpretation and presentation of that view. It
must reconcile with the Capture `Dashboard Boundary` and inherit its forbidden-use
set rather than relaxing it.

## Non-claims

- Not validation, readiness, buyer proof, or product proof.
- Not a move pass for Capture contracts or Data Lake records.
- Not SQLite adoption or any storage-engine selection.
- Not a data-lake job, scheduler, runner, or runtime build.
- Not a dashboard implementation.
- Not live capture or source-access authorization.
- Not contact enrichment, outreach, lead-list export, or a public creator directory.
- Not a claim that real creator rows or real-row tests exist.

## Direction change propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Creator Signal is promoted as an accepted product_signal spine for the
    creator-intelligence product surface. It owns product/buyer interpretation,
    information architecture, claim language, and required limitation/freshness
    displays over the Capture-owned creator_profile_current view; Capture keeps
    identity linkage, metric observations, metric rollups, ideal-audience
    inference schemas, and current-view join mechanics. No storage, runtime,
    dashboard, live capture, outreach, or public-directory authority is created.
  trigger: architecture_doctrine
  related_triggers:
    - product_doctrine
    - workflow_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/forseti_creator_signal_spine_promotion_binding_v0.md
    - docs/decisions/forseti_spine_first_target_structure_binding_v0.md
    - .agents/workflow-overlay/artifact-folders.md
    - orca/product/README.md
    - forseti/product/spines/creator_signal/README.md
    - forseti/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/artifact-folders.md
    - docs/review-inputs/creator_signal_spine_pre_ratification_review_input_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_creator_ideal_audience_inference_spec_v0.md
    - docs/decisions/orca_audience_ballot_taxonomy_v0.md
  intentionally_not_updated:
    - path: repo-structure.yaml
      reason: >
        creator_signal is under orca/ (already a declared top-level area) and
        per-spine structure is owned by the spine-first binding, not the machine
        map; no machine-map change is needed.
    - path: orca-harness/
      reason: >
        This is a docs/product promotion and surface-boundary pass only. It
        authorizes no runtime schema, validator expansion, dashboard, data-lake
        job, source access, or tests.
    - path: forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md
      reason: >
        Identity linkage ownership remains unchanged. The high-level surface
        consumes identity rows but does not add metric, audience, contact, or
        public-directory fields to the linkage ledger.
  stale_language_search: >
    rg -n "creator_signal|Creator Signal|creator intelligence|creator_profile_current|Dashboard Boundary|public person-level directory|lead-list|SQLite|data-lake job"
    .agents/workflow-overlay docs/workflows docs/decisions orca/product
  stale_language_search_result: >
    Executed 2026-06-28 in branch codex/creator-ledger-static-fixture. Hits were
    the new Creator Signal binding/front-door/surface and route updates; the
    existing Capture public-handle/current-view creator specs; existing
    LinkedIn/wind-caller exclusion language for lead-list/contact boundaries; and
    an existing data-lake derived-retrieval proposal that discusses SQLite as a
    query-lens. No checked surface assigns Creator Signal storage, runtime,
    outreach, public-directory, or Capture record ownership.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not implementation authorization
    - not SQLite adoption
    - not data-lake job authorization
    - not dashboard implementation
    - not live capture authorization
    - not outreach or lead-list authorization
```
