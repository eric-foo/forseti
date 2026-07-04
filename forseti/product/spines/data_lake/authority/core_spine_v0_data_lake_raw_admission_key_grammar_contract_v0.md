# Core Spine v0 Data Lake Raw Admission + Key Grammar Decision Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture decision contract
scope: >
  Resolves the gating Data Lake raw-addressing blocker: structural packet-admission
  criteria and the lake key grammar (packet/slice/file/attachment addressing
  handles), the packet-depth raw path, and identity invariants. Keys are addressing
  handles only, never canonical identity; admission is structural, never semantic.
use_when:
  - Scoping raw packet admission, the raw path container, or lake key usage.
  - Checking whether a proposed key or admission rule leaks canonical identity, dedupe, or payload interpretation.
open_next:
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
downstream_consumers:
  - physical data-lake storage/implementation lane
  - availability index + derived-record keying lanes
  - capture packet schema/evolution lane
stale_if:
  - A later accepted serialization, manifest, or backend decision changes the key family or raw path semantics.
  - The Data Lake Core or Storage contract changes the lake-owned handle family or admission boundary.
  - A later owner decision admits content-derived IDs, canonical identity, or dedupe into the lake.
authority_boundary: retrieval_only
```

## Status

`RAW_ADMISSION_KEY_GRAMMAR_DECISION_RECORDED_V0`. Resolves Physicality Location
Contract blocker 1 (packet-admission + key rules).

Owner-adopted 2026-06-21 (owner "proceed" after adjudication of the raw-admission
blocker-resolution lane report). This is an architecture decision contract. It is
not implementation authority, validation, readiness, serialization, manifest
selection, backend selection, canonical identity, or dedupe.

## Decision In One Screen

```text
Lake keys are addressing handles, not identities.
Raw admission is structural and hash-checkable, never semantic.
The raw container is sharded for physical fanout: raw/<packet_shard>/<packet_id>/ (shard = sha256(packet_id)[:3]); by-key reads recompute the shard.
Inner layout, serialization, canonical identity, and dedupe stay deferred/out-of-scope.
```

## Admission Criteria

A captured packet is admitted/committed to the Raw Packet Store only when:

- its manifest is present, parseable, and accepted by the current admission
  schema/version policy;
- its `packet_id` matches the locked grammar and its write-once target
  `raw/<packet_id>/` is absent/free (no overwrite);
- every preserved file carries a stable file handle, packet-relative path,
  `sha256`, `hash_basis`, and size, and every recorded hash verifies under its
  recorded `hash_basis`;
- file handles are unique, every slice/file reference resolves, and no preserved
  body is orphaned;
- any Attachment Record entry resolves an immutable/hash-checkable body by
  key/ref/hash/`hash_basis` without source-family interpretation;
- admission does not interpret payload meaning (meaning belongs to
  Projection/ECR/SCR/Cleaning/Judgment, not lake admission).

Hold/quarantine (not commit): hash-consistent but off-policy/historical manifest
versions; incomplete staging not yet atomically publishable; packets needing an
owner/lane decision before replay.

Refuse: missing manifest/body, hash mismatch, absent/unsupported `hash_basis`, path
escape, duplicate `packet_id`, duplicate file handles, unresolved references, a
mutable store as the only canonical raw body, a semantic/canonical-identity
requirement, or an existing target (collision, never overwrite).

## Key Grammar

Lake keys are an addressing family only:

- `packet_id` — an opaque, capture/admit-assigned handle, **incumbent-compatible**
  with the current capture generator's ULID-style 26-character Crockford handle. It
  is not a content hash, source URL, or canonical product/entity/creator identity.
  The exact format is incumbent-pinned, not newly frozen by this contract.
- `slice_id` — a packet-scoped stable token; not globally unique outside its packet.
- `file_id` — a packet-scoped stable token that maps through the manifest/index to a
  packet-relative stored body path; it is not itself a path.
- `attachment_key` — a packet-scoped stable token when needed, carried with separate
  source family, payload kind, schema version, body reference, hash, `hash_basis`,
  and posture fields.
- `object_key` / `event_key` — **not** lake-owned at raw admission. If a derived lane
  needs object/event rows, it owns lane-namespaced derived-record keys keyed back to
  raw anchors. Availability events, if later added, are runtime notifications over
  committed keys, never source of truth.

## Raw Path Grammar

Locked at packet depth, under an opaque physical shard prefix:

```text
raw/<packet_shard>/<packet_id>/
```

`<packet_id>` must equal the manifest `packet_id` and remains the authoritative raw
by-key handle. `<packet_shard>` is a fixed-width lowercase-hex shard derived SOLELY
from `<packet_id>` for physical fanout (incumbent: the first 3 hex chars of
`sha256(packet_id)`, 4096 buckets), so no single directory accumulates an unbounded
packet count at scale. It carries no source-family, date, source URL, canonical
entity/product/creator, content-hash, or dedupe meaning, and is never lake authority;
the primary raw path must not encode any of those meanings. **By-key lookup MUST
recompute the shard from `packet_id`; it MUST NOT require an Availability Index,
locator, queue, scan, or runtime event to find committed raw.** A duplicate
`packet_id` or an existing sharded target is a collision/refusal path, never an
overwrite or dedupe. Inner packet layout (how material is organized within the
packet container), manifest/index serialization, the exact shard width, and backend
remain deferred to physicalization; the AR-body member-vs-sidecar fork is ratified
(packet-member default per the Gate 1 body-layout ADR, 2026-07-02); incumbent
packet-relative body paths inside the container remain acceptable. (Shard prefix adopted 2026-06-25; a future shard-width change is a
separate owner-gated migration.)

## Identity Invariants

- Lake keys are addresses, not canonical identities.
- Hash equality proves byte equality under a named `hash_basis`, not
  product/entity/creator sameness.
- Re-capture of the same source object gets a new `packet_id`; supplement /
  supersede / conflict relationships are append-only metadata, never a lake-owned merge.
- A duplicate `packet_id` or existing `raw/<packet_id>/` is a collision/refusal path,
  never overwrite or dedupe.
- Derived records reference raw handles and never mutate raw bytes, hashes,
  manifests, packet identity, or Attachment Records.

## Accepted Residuals

- Inner raw sublayout left open (avoid premature backend/serialization lock-in);
  upgrade trigger: physicalization lane starts or two consumers need the same
  concrete member layout.
- Manifest version / Attachment Record serialization left open (relationship locked,
  wire shape not); trigger: storage-code implementation scoping.
- Admission version-dispatch policy for historical packets left at hold/replay/refuse
  posture; trigger: a named consumer needs off-version packets.
- Semantic object/event keys intentionally not lake-owned; trigger: a derived lane
  needs a durable derived-row contract.

## Deferred / Out Of Scope

Storage engine/backend (object store, database, SQL-capable embedded engine,
or equivalent), manifest version, attachment serialization, queue/event runtime,
derived-record physical home, migration/replay tooling, canonical identity,
cross-packet dedupe, semantic object/event identity, validation suite, and
implementation route. (AR-body member-vs-sidecar layout, formerly deferred here,
was ratified 2026-07-02 by the Gate 1 body-layout ADR: packet-member default.)

## Non-Claims

Not validation, readiness, approval, or implementation authorization. Not
serialization, manifest, or engine/backend selection by this artifact. Not canonical
identity or dedupe. Not ECR/SCR/Cleaning/Judgment design. Records an addressing +
admission decision only.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Raw Admission + Key Grammar Decision Contract v0 resolves the gating raw-
    addressing blocker: lake keys are addressing handles (opaque incumbent-
    compatible packet_id; packet-scoped slice_id/file_id/attachment_key; no lake-
    owned object/event identity), admission is structural and hash-checkable, the raw
    container path is locked at packet depth raw/<packet_id>/, and canonical
    identity/dedupe/serialization stay out of scope or deferred.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
    - forseti/product/spines/data_lake/README.md
  downstream_surfaces_checked:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not serialization or backend selection
    - not canonical identity or dedupe
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Amended 2026-06-25: the raw container path gains an opaque deterministic
    physical shard prefix -- raw/<packet_shard>/<packet_id>/ -- with
    <packet_shard> = sha256(packet_id)[:3] (4096 buckets), physical fanout ONLY
    (no family/date/identity/content/dedupe meaning, never authority). <packet_id>
    stays the authoritative by-key handle; by-key lookup recomputes the shard and
    needs no index/locator. A duplicate packet_id or an existing sharded target
    stays a collision/refusal. Exact shard width and backend remain deferred; a
    future width change is a separate owner-gated migration.
  trigger: architecture_doctrine
  owner_directive: >
    Owner adopted raw + derived/ack directory sharding to prevent a future
    flat-directory reorg (standing principle: long-term structure overrides
    ratified authority); a de-correlated different-family review (Codex) verified
    by-key preservation, the relocate migration, and collision/rebuild handling.
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
  implementation_landed:
    - orca-harness/data_lake/root.py
  downstream_surfaces_checked:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  non_claims:
    - not validation
    - not readiness
    - not a storage-engine/backend selection
    - not a shard-width finalization (incumbent 3-hex; a change is an owner-gated migration)
```
