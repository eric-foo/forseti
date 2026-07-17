# Creator Registry

```yaml
retrieval_header_version: 1
artifact_role: source_capture_family_registry_index
scope: >
  Folder front door for Orca creator-ledger artifacts: the known public account
  registry, public-handle linkage ledger, creator-profile current view, and the
  lake-native mapping that keeps Capture, Discovery, and Creator Signal aligned
  without turning creator intelligence into one giant document.
use_when:
  - Finding the current list of known creator/platform accounts.
  - Checking whether Discovery or Capture should treat an observed account as already known.
  - Explaining the split between creator registry, public-handle linkage, metric rollups, and the profile-current dashboard view.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_v0.json
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_gt_roadmap_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_ledger_operational_evolution_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/ak_fragrances1_creator_audience_triangulation_snapshot_v1.json
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/ak_fragrances1_creator_audience_judgment_outcome_v1.json
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_native_record_mapping_v0.md
  - forseti/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
stale_if:
  - Creator registry ownership moves out of Capture/social-media source family.
  - Discovery or Capture adopts a different known-account preflight index.
  - Creator Signal adopts a successor profile surface without reconciling this folder.
```

## Purpose

This folder is the creator-ledger home for social-media creator accounts.

It is intentionally a folder, not one huge document. The parts update at
different speeds and carry different authority:

- `creator_registry_index_v0.json` is the current check-before-work list for
  known public platform accounts and linked creator records, plus the
  deterministic account-level onboarding projection from committed Bronze.
- `creator_public_handle_linkage_ledger_v0.json` is the identity/linkage ledger:
  public platform accounts, handle evidence, soft links, promoted links, and
  rejected links.
- `creator_profile_current_view_v0.json` is the current one-stop profile export:
  identity plus joined rollups and source drill-back for operator/dashboard use.
- `ak_fragrances1_creator_audience_triangulation_snapshot_v1.json` is the exact
  checked-in export of AK Fragrances' validated v1 transcript/comment audience
  snapshot for reproducible profile-current materialization.
- `ak_fragrances1_creator_audience_judgment_outcome_v1.json` is its exact paired
  successful Judgment outcome; the persisted lake record `cajo_ee7c184a02dfee07534e`
  remains the producer record, while this copy is the clean-checkout verification input.
- `creator_profile_current_record_contract_v0.md` pins the per-profile visible
  field surface, consumer interpretation promise, and declared-deferred global
  metric recipes for `posting_cadence` and `recent_velocity`.
- `creator_ledger_operational_evolution_contract_v0.md` pins the
  migration-stable additive-evolution rule, capability routing matrix, and
  upgrade-intake shape: future
  capability should add fields, sibling records, resolvers, or views without
  rewriting existing source truth, and God Tier progress is judged by operational
  efficacy before audit completeness.
- `creator_registry_gt_roadmap_v0.md` records what to optimize for after the
  Mini God Tier slice, including bounded scanning, account/evidence graphing,
  public-link exploration, and the road toward fuller God Tier efficacy.
- Metric observations, rollups, capture receipts, and audience snapshots remain
  in their owning Capture/Silver producer records. Checked-in producer exports
  may support deterministic current-view rebuilds, but they are not copied into
  the registry index as raw truth.

Run `forseti-harness/runners/run_creator_registry_onboarding_refresh.py` after
official captures to refresh `not_onboarded` / `onboarded` from exact committed
packet evidence. The runner reads the lake but never writes it. Then run the
profile-current materializer, which mirrors the same state for consumers.

## Placement

The folder stays under:

`forseti/product/spines/capture/core/source_families/social_media/creator_registry/`

That is the low-level social-media source-family contract home. The higher-level
consumer-facing surface is still the Creator Signal spine:

`forseti/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md`

In plain terms: Capture owns the registry and evidence boundaries; Creator Signal
owns how the buyer/operator sees the resulting profile.

## Dedupe Rule

Discovery should still observe known creators again. A repeat observation is
useful signal. The registry index only prevents duplicate rows and duplicate work:

```text
Discovery observes a handle or URL
-> normalize platform/account/handle
-> check creator_registry_index_v0.json
-> exact known account: attach discovery evidence through the owning source-family observation or capture-refresh handoff, keyed to the stable account/subject ids
-> possible same creator: create or refresh a candidate link review item
-> unknown account: create a new candidate stub through the owning source lane
```

When the next capability is not exact preflight, use the capability routing
matrix in `creator_ledger_operational_evolution_contract_v0.md` before changing
record shape. Repeat observations, metric facts, rollups, linkage review, and
Creator Signal interpretation each have different owning layers.

## Non-Claims

- not a raw capture store
- not metric authority
- not audience authority
- not public person identity proof
- not a social follower graph
- not SQLite or dashboard implementation
- not buyer proof

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Creator-ledger artifacts are now grouped under the Capture-owned social-media
    creator_registry folder: creator_registry_index_v0.json is the known-account
    preflight/dedupe list for Discovery and Capture, while public-handle linkage
    and profile-current remain separate sibling artifacts instead of one giant
    ledger document.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
    - product_doctrine
  controlling_sources_updated:
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_spec_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_v0.json
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_native_record_mapping_v0.md
  downstream_surfaces_checked:
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - forseti/product/spines/capture/core/source_capture_toolbox/README.md
    - forseti/product/spines/creator_signal/README.md
    - forseti/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
    - orca-harness/capture_spine/creator_profile_current/materialize.py
    - orca-harness/capture_spine/creator_profile_current/instagram_metric_seed.py
    - orca-harness/runners/run_creator_profile_current_materialize.py
    - orca-harness/runners/run_instagram_reels_creator_metric_seed_materialize.py
    - orca-harness/tests/unit/test_creator_registry_index.py
    - orca-harness/tests/unit/test_creator_profile_current_static_view.py
    - orca-harness/tests/unit/test_creator_public_handle_linkage.py
    - orca-harness/tests/unit/test_instagram_reels_creator_metric_seed.py
    - orca-harness/tests/unit/test_youtube_creator_metric_seed.py
  intentionally_not_updated:
    - path: docs/prompts/, docs/review-inputs/, and docs/review-outputs/ historical prompt/review body prose
      reason: Historical commission/review artifacts keep point-in-time source paths in their body narrative by design; their open_next retrieval headers were repointed to the new creator_registry/ paths so the strict retrieval link gate stays green, and active product, map, code, and test surfaces were updated.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not SQLite adoption
    - not live capture execution
    - not dashboard implementation
```
