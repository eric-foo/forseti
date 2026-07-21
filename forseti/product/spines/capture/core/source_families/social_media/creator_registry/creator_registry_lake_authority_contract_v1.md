# Creator Registry Lake Authority Contract v1

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract
scope: >
  Operational Creator Registry authority, migration, admission, generated-current
  view, monitoring-eligibility, and client-safe projection boundaries after the
  Git-to-Data-Lake cutover.
use_when:
  - Deciding whether a creator is already onboarded.
  - Adding a newly validated creator without a data-only pull request.
  - Reading monitoring-eligible accounts or a client-safe creator profile.
  - Migrating or rebuilding Creator Registry state.
open_next:
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
authority_boundary: retrieval_only
```

## Decision

Live Creator Registry state is operational data and belongs in the configured
Forseti Data Lake. Git retains code, contracts, schemas, tests, fixtures, and the
frozen legacy migration inputs. A creator onboarding must not modify a tracked
registry, profile, Judgment export, or metric snapshot merely to become current.

The authority and read-model split is:

```text
derived/.../creator_registry_baseline/<record-id>          authority, one migration
derived/.../creator_registry_account_admission/<record-id> authority, append-only
derived/.../creator_audience_judgment_outcome/<record-id>  Judgment authority

indexes/derived_retrieval/creator_registry/
  CURRENT
  generations/<generation-id>/
    query_tables/creator_registry_index_v1.json            internal current view
    profiles/creator_profile_public_v1.json                 client-safe current view
    manifests/creator_registry_generation_v1.json           hashes and authority inventory
```

The generated files under `indexes/` carry no authority. A reader verifies the
complete generation, file hashes, and the current append-only authority inventory.
An authority record newer than `CURRENT`, a missing member, or a hash mismatch
fails closed and requires a rebuild.

## Baseline and admission

The one-time baseline migration preserves the exact legacy linkage-ledger,
registry-index, and profile-current bytes in a Source Capture packet, then writes
one normalized `creator_registry_baseline_v1` record. A dry run must prove the
account and profile sets before the first authority write. An identical rerun is
`already_current`; different baseline hashes are a blocker.

`creator_registry_account_admission_v1` is the first live admission contract.
Its v1 writer supports TikTok and requires:

- stable TikTok numeric account id, handle, display name, and observation time
  verified from the admitted grid-window bytes;
- the qualifying committed Bronze packet and its source surface;
- an authoritative lake `creator_audience_judgment_outcome_v1` with
  `status=validated` and an embedded snapshot bound to the same creator and
  platform-account subject;
- one conflict-free platform account mapping; and
- `monitoring_eligible=true`.

The admission record id is content-derived. Repeating the same admission is
byte-idempotent. Conflicting account id, native id, handle, outcome, or snapshot
bindings fail closed. A previously validated outcome keeps its already-bound
profile subject id when no current account exists; otherwise new TikTok subjects
use a deterministic opaque id derived from platform plus numeric native id.

Bronze capture does not promote the registry. Promotion occurs only after
successful Judgment validation, when the coordinator appends the admission,
publishes one complete generation, and freshly reads back exactly one internal
account and one public profile.

## Consumers

`creator_registry_index_v1` is the internal exact-match and operational view. It
contains onboarding and monitoring eligibility. `onboarded` means one validated
admission backed by qualifying Bronze and Judgment; it does not mean fresh,
representative, influential, or scheduled.

Monitoring semantics are deliberately narrow:

```text
onboarded -> monitoring eligible
monitoring eligible != scheduled
```

No cadence, queue, or scheduler is created by this contract.

`creator_profile_public_v1` is an allowlisted, future-delivery-ready full profile:
public platform accounts, metric rollups, audience triangulation, freshness,
limitations, and non-claims. It excludes onboarding controls, monitoring state,
routing/preflight state, source drill-back, raw response bytes, and machine-local
absolute paths. Creator Vault is not its authority because the profile includes
validated Judgment material rather than Silver public evidence alone.

Runtime preflight and monitoring readers use the lake `CURRENT` generation.
Repository JSON may be supplied only as explicit test dependency injection. The
Instagram and YouTube account state migrates into the baseline and remains
readable; new admission writers for those platforms are deferred.

## Lifecycle and rollback

The code/contract cutover is one PR. Production migration is additive: the old
code can continue reading Git until the new code lands, while the lake baseline
and generation are unused. Once the cutover lands, operational readers do not
fall back to Git.

The checked-in registry JSON remains frozen and non-authoritative for rollback
and audit during the first cutover. Remove it only in a later work unit after an
independent live onboarding proves the lake route. Closing an older data-only
onboarding PR requires semantic parity and exact-once readback through this path.

## Accepted residuals and non-claims

- Cross-platform linkage mutations and Instagram/YouTube admission writers are
  deferred.
- The public projection is a file read model, not hosted delivery, API,
  authentication, or replication.
- A generation publication failure after an append leaves detectable stale
  current state; it is not reported as successful promotion.
- This contract creates no database, general event framework, scheduler, or
  standing timing system.
- Not buyer proof, contact authorization, legal-name identity proof, or guaranteed
  campaign performance.
