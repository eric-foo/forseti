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
- `linkage_state`
- `routing_decision`
- `freshness`
- `lookup_keys`
- `source_pointers`
- `non_claims`

The current v0 index may be static JSON as long as tests prove it mirrors the
identity ledger. A later lake-native or SQLite implementation should generate
the same logical shape rather than teach Discovery/Capture a different one.

## Dedupe State Semantics

`discovery_state` is routing state, not profile truth:

- `known_account`: Discovery found an account already admitted to the registry.
- future `candidate_new_account`: a not-yet-admitted candidate from Discovery.
- future `known_seen_again`: a repeat observation event should attach to the existing row.

`capture_state` is freshness/routing state, not metric truth:

- `identity_observed_metric_seed_available`: identity exists and at least one
  source-backed metric seed/profile row currently points to this account.
- future `never_captured`, `capture_stale`, `capture_blocked`, or `capture_fresh`
  require a named Capture/Silver freshness producer.

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
