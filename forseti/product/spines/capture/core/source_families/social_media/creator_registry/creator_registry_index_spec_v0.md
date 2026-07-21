# Creator Registry Index Spec v0

```yaml
retrieval_header_version: 1
artifact_role: source_capture_family_registry_index
scope: >
  Small creator-registry dedupe/index contract for known public platform accounts
  and linked creator records. Defines what Discovery and Capture may check before
  opening duplicate exploration or capture work. This is not metric authority,
  not raw capture storage, not a dashboard, not SQLite adoption, and not a public
  person identity service.
use_when:
  - Checking whether a discovered public account is already known.
  - Designing Discovery or Capture preflight against known creator/platform accounts.
  - Explaining why handle/account identity belongs near the ledger while metrics remain in Silver/Capture records.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_v0.json
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_native_record_mapping_v0.md
stale_if:
  - Discovery or Capture adopts a different known-account preflight contract.
  - The linkage ledger moves to SQLite or a lake-native generated registry envelope.
  - Platform-account identity keys or promoted-link states are superseded.
```

## Status

`SMALL_DEDUPE_INDEX_CONTRACT_V0`.

The index answers one question before Discovery or Capture opens work:

```text
Have we already seen this public platform account or linked creator record?
```

It does not answer whether the creator is influential, currently fresh, a good
fit, reachable, or cross-platform linked. Those facts come from sibling records
and the profile-current view.

It also records whether an account has completed initial content onboarding.
That is a narrow operational fact, not a freshness or quality judgment.

## Stable Keys

Use platform-account identity first, handles second:

1. `platform_account_id`: Orca-local stable row id.
2. `platform_public_account_id_or_none`: platform-native public account id when known.
3. `public_profile_url`: canonical public URL observed from source evidence.
4. `normalized_public_handle`: handle label normalized for lookup, but mutable and never enough by itself for final cross-platform identity.

## Index Row Shape

Each `platform_accounts` row carries:

- `platform_account_id`
- `platform`
- `platform_public_account_id_or_none`
- `public_handle`
- `normalized_public_handle`
- `public_profile_url`
- `creator_record_id_or_none`
- `identity_state`
- `discovery_state`
- `capture_state`
- `onboarding`
- `linkage_state`
- `routing_decision`
- `freshness`
- `lookup_keys`
- `source_pointers`
- `non_claims`

The current v0 index is a deterministic materialized JSON projection. Tests
must prove that its identity rows mirror the linkage ledger and that its
onboarding rows derive from verified committed Bronze. A later lake-native or
SQLite implementation should generate the same logical shape rather than teach
Discovery/Capture a different one.

## Dedupe State Semantics

`discovery_state` is routing state, not profile truth:

- `known_account`: Discovery found an account already admitted to the registry.
- future `candidate_new_account`: a not-yet-admitted candidate from Discovery.
- future `known_seen_again`: a repeat observation event should attach to the existing row.

`capture_state` is freshness/routing state, not metric truth:

- `identity_observed_metric_seed_available`: identity exists and at least one
  source-backed metric seed/profile row currently points to this account.
- `identity_observed_profile_packet_available`: identity exists from a
  source-backed public profile packet, but no source-backed metric rollup is
  currently joined for this account.
- `never_captured`: identity exists, but no official content capture has yet
  qualified under the onboarding policy.
- future `capture_stale`, `capture_blocked`, or `capture_fresh` require a named
  Capture/Silver freshness producer.

`onboarding` is separate from freshness and routing state:

- `not_onboarded`: no publicly available qualifying official committed Bronze
  content packet can be exactly attributed to the platform account. Its
  evidence fields are null.
- `onboarded`: at least one publicly available qualifying packet is hash/size
  verified and exactly attributable. The row carries the earliest qualifying
  available capture time, packet id, source family, source surface, and policy
  version.
- Qualifying v0 surfaces are Instagram Reels grid packets, TikTok grid or
  admitted video/comment/subtitle packets, and YouTube watch metadata/comments
  packets. YouTube RSS, TikTok logged-out discovery snapshots, suggested-account
  discovery packets, scratch/staging artifacts, failed attempts, and partial
  uncommitted captures do not qualify.
- The state is account-scoped and monotonic over publicly available immutable
  committed Bronze. Owner-directed public-consumption tombstones remove
  superseded packets from eligibility without deleting audit bytes. Recency,
  paused monitoring, and stale metrics remain separate fields.

The live successor is governed by
`creator_registry_lake_authority_contract_v1.md`. The checked-in v0 index is a
frozen migration input. After cutover, `creator_registry_index_v1` is rebuilt
from the one baseline plus append-only admissions and published under the lake
`CURRENT` generation. Bronze capture alone does not flip state; validated
Judgment completion performs the admission and exact-once readback.

`linkage_state` is inherited from the public-handle linkage ledger:

- `single_platform_observed`: no linked creator record exists.
- future `candidate_needs_review`, `probable_public_account_link`,
  `declared_public_account_link`, or `rejected_public_account_link` may appear
  only when the linkage ledger carries the corresponding evidence.

## Boundaries

- The registry index may be source of truth for Orca-known platform-account rows
  and observed handle history.
- It is not source of truth for metrics, audiences, creator fit, contactability,
  buyer proof, or real-world person identity.
- Handles are mutable. Discovery/Capture must prefer platform-native account ids
  when they are available.
- Repeat discovery of a known account should be preserved as evidence or signal,
  not discarded; the dedupe behavior is to avoid duplicate rows and duplicate
  work queues.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "Creator onboarding is now an account-scoped, Bronze-evidenced materialized state in the Creator Registry, distinct from freshness and mirrored into creator_profile_current."
  trigger: lifecycle_boundary
  related_triggers: [architecture_doctrine, output_authority]
  controlling_sources_updated:
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_spec_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_ledger_operational_evolution_contract_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/validation-gates.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md
    - docs/workflows/forseti_repo_map_v0.md
    - forseti-harness/capture_spine/creator_profile_current/materialize.py
    - forseti-harness/capture_spine/creator_profile_current/validation.py
  intentionally_not_updated:
    - {path: individual platform capture runners, reason: "Onboarding is derived centrally from committed Bronze so every runner need not maintain registry state."}
    - {path: data-lake packet schemas, reason: "Existing committed packet identity and lineage fields are sufficient; no Bronze schema change is required."}
    - {path: Creator Signal ranking surfaces, reason: "Onboarding is operational eligibility, not a ranking, fit, quality, or influence score."}
  stale_language_search: 'rg -n "never_captured|onboarded|not_onboarded|capture_state|creator_profile_current" forseti/product/spines/capture/core/source_families/social_media/creator_registry forseti-harness/capture_spine/creator_profile_current forseti-harness/runners'
  non_claims: [not validation, not readiness, not live capture authorization, not creator quality, not freshness]
```
