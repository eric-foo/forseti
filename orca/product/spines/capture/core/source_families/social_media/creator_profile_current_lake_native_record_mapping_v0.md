# Creator Profile Current Lake-Native Record Mapping v0

```yaml
retrieval_header_version: 1
artifact_role: source_capture_family_architecture_contract
scope: >
  Maps the creator_profile_current sibling model to Data Lake v4.1 / Silver Vault
  records and generated Creator Vault read models. Clarifies that durable creator
  metric observations and rollups should be derived from append-only Silver
  records, while the current JSON seed remains a static proving artifact.
use_when:
  - Scoping a lake-native creator metric observation or rollup producer.
  - Deciding whether creator_profile_current should read from static JSON,
    Silver Vault records, SQLite, or generated Creator Vault envelopes.
  - Explaining how average views, engagement rate, comments, likes, and sample
    support should be computed without making the identity ledger one giant ledger.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_v0.json
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_seed_v0.json
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
  - orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
stale_if:
  - The Silver Vault record contract changes record_kind, payload_kind, MetricObservation, or Creator Vault envelope semantics.
  - The creator_profile_current sibling model changes identity, metric observation, metric rollup, or audience snapshot boundaries.
  - A later accepted implementation chooses a concrete creator metric producer schema that supersedes this mapping.
```

## Status

`MAPPING_CONTRACT_V0`.

This is the MGT/SCI next step after the static creator metric seed: it locks the
lake-native target shape before implementation. It does not write lake records,
choose SQLite/DuckDB/backend, create a dashboard, run live capture, migrate the
old lake, or claim readiness.

## Decision

Yes: durable creator metric observations should derive from the Data Lake v4.1
Silver lane.

The static JSON seed is a source-backed proof artifact. The durable shape is:

```text
Bronze/raw packets
  -> Silver MetricObservation records for source-visible per-content/per-account facts
  -> Silver derived MetricRollupObservation records for account/platform/window aggregates
  -> generated Creator Vault / creator_profile_current read models
```

`creator_profile_current` is the one-stop current view. It should eventually read
from generated Silver retrieval / Creator Vault envelopes, not from a hand-kept
JSON ledger. The identity ledger remains identity-only.

## Lake-Native Record Families

These are logical families over the Silver Vault record contract. They are not
new physical folders and not a global path taxonomy.

| Creator profile layer | Lake-native home | Authority posture |
| --- | --- | --- |
| Public platform account | Silver `entity`, `payload_kind: PlatformAccountEntity` | Stable per-platform public account identity only; no person dossier. |
| Public content object | Silver `entity`, e.g. Short/Reel/Post/Video content object | Stable platform content key; mutable counts stay observations. |
| Account publishes content | Silver `relationship`, `content_published_by_account` | Connects content entity to platform account entity. |
| Per-content metric fact | Silver `observation`, `payload_kind: MetricObservation` | Source-visible value or explicit posture/reason; missing is never zero. |
| Per-account/window rollup | Silver derived `observation`, producer-owned `payload_kind: MetricRollupObservation` or equivalent accepted producer schema | Computed from MetricObservation records; carries recipe, window, source ids, sample support, limitations. |
| Ideal/content-fit audience snapshot | Silver derived observation/profile record owned by the audience producer | Joined by profile view when source-backed; actual audience remains not estimated unless separately authorized. |
| Current creator profile | Generated read model under `indexes/derived_retrieval/silver_vault/creator_vault/` plus Capture `creator_profile_current` contract | Rebuildable view, not authority. |

## Metric Derivation Rule

For a subject like `creator/account X on platform Y`:

1. Read Silver `MetricObservation` records whose subject is content or account
   evidence linked to that platform account.
2. Filter by platform, content kind, metric name, source surface, window, and
   selection policy version.
3. Exclude non-observed metrics from numeric aggregations. Keep hidden, blocked,
   absent, not-attempted, and not-applicable rows as posture/reason records.
4. Compute rollups such as average views, median views, average likes, average
   comment count, engagement rate, cadence, and velocity only when numerator and
   denominator inputs are source-backed and recipe-compatible.
5. Write or generate a rollup with source record ids, calculation recipe,
   coverage window, `computed_at`, freshness, `sample_support`, limitations, and
   non-claims.
6. Generate `creator_profile_current` / Creator Vault read envelopes from the
   latest allowed rollups and sibling identity/audience records.

Engagement rate is not a special exception. It becomes available only when
source-backed like/comment/subscriber or other denominator-compatible inputs
exist with observed posture and a named recipe.

## Validator Target

A reusable validator should validate the **shape and contract boundaries** of a
creator profile current export or generated envelope. It should not prove source
truth by itself.

Minimum checks:

- identity rows do not carry metric values, audience labels, contact fields, or
  person-level claims;
- metric observations obey posture/value/reason coupling;
- rollups list source observation ids, recipe/version, window, sample support,
  freshness, and limitations;
- non-observed metrics are not numeric zeroes;
- cross-platform rollups require promoted linkage, not candidate or rejected
  links;
- `creator_profile_current` mirrors source siblings and does not become a second
  source of truth;
- generated/read-model artifacts carry source refs or manifest pointers back to
  Silver authority.

The validator is reusable because it checks these invariants independent of the
platform. YouTube, Instagram, and TikTok producers can all feed the same shape if
their source-specific metric observations obey the Silver posture/value contract.

## Accepted Residuals

- **No lake producer yet.** This mapping records the target before implementation.
  Risk: the static JSON seed remains the only concrete metric example. Upgrade
  trigger: implementation scoping for a Silver creator metric producer.
- **No concrete backend or SQLite choice.** Silver semantics are engine-neutral.
  Risk: query ergonomics remain abstract. Upgrade trigger: scan/query latency or
  producer implementation requires backend selection under the Data Lake storage
  physicalization boundary.
- **No engagement-rate data yet.** The current YouTube seed lacks source-backed
  likes/comments/subscribers. Risk: creator influence remains view-count-only.
  Upgrade trigger: a platform producer emits observed numerator/denominator
  metric observations with posture and recipe-compatible windows.
- **No cross-platform identity rollup.** Creator Vault remains per-platform until
  public-handle linkage is promoted. Risk: the one-stop profile is account-level.
  Upgrade trigger: human-reviewed probable or declared public-account linkage
  exists for two or more platforms.
- **No dashboard/API implementation.** The profile remains a contract/read-model
  target. Risk: operators still inspect files. Upgrade trigger: generated Creator
  Vault envelopes and validator pass on real Silver records.

## Non-Claims

Not validation, readiness, buyer proof, SQLite adoption, backend selection,
data-lake writer implementation, live capture authorization, dashboard
implementation, cross-platform identity resolution, engagement-rate support, or
contact/outreach authorization.
