# Core Spine v0 Data Lake Storage Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract
scope: >
  Non-selecting storage contract for Orca's data lake: dumb record-kind slots,
  write/read disciplines, success signals, and physicalization blockers.
use_when:
  - Preparing data-lake storage, manifest, index, or derived-result work after the logical lake contract.
  - Checking whether a lake change accidentally selects a physical engine, queue, serialization, or schema.
  - Explaining where Capture, Projection, ECR/SCR, Cleaning, and Judgment attach without replacing raw truth.
open_next:
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
  - orca/product/spines/capture/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
  - orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
  - docs/workflows/ecr_spine_submap_v0.md
downstream_consumers:
  - physical data-lake storage lane
  - capture packet schema/evolution lane
  - ECR/SCR source-side derived-record lanes
  - Cleaning spine foundation lane
  - future queue or scheduler lane
stale_if:
  - A later accepted storage, manifest, sidecar, queue, serialization, or schema decision supersedes this contract.
  - The Data Lake Core Contract v0 changes the lake-owned boundary.
  - Projection, ECR, SCR, Cleaning, or Judgment ownership changes in a later accepted source.
  - A later owner decision makes the lake an orchestrator rather than a by-key store.
authority_boundary: retrieval_only
```

## Status

`TARGET_STORAGE_CONTRACT_RECORDED_V0; BLOCKER_1_DIRECTION_RECORDED_V0; BLOCKER_1_IMPLEMENTATION_CONTRACT_RECORDED_V0; BLOCKER_2_DIRECTION_RECORDED_V0`.

This is a planning and architecture contract. It is not implementation
authority, validation, readiness, physical storage selection, queue design,
schema finalization, migration authority, or storage-engine selection.

## Goal

Define the smallest complete storage contract that lets later lanes know where
data lands and how derived work attaches, without making the data lake smart.

## Success Signals

This goal is successful when all of the following are true:

1. A future lane can say exactly what the lake stores: raw packet (CapturePacket) truth, stable
   handles, source-family attachment records, passive availability facts, and
   append-only derived/ack references.
2. A future lane can say exactly what the lake does not do: clean, normalize,
   dedupe, identify, score, judge, schedule, retry, route, or call downstream
   lanes.
3. The five dumb record kinds are named consistently: Raw Packet Store,
   Attachment Record, Availability Index, Derived Result Store, and
   Acknowledgement Log.
4. By-key discovery remains the authority before any queue: downstream lanes
   can find committed work by key even if an event message is missed.
5. Physical choices remain visibly deferred: no storage engine, manifest v2,
   sidecar contract, serialization, projection cache, queue runtime, schema,
   migration, or validation/readiness claim is selected here.
6. Historical "typed extension envelope" wording does not become the target
   storage name. In this lane, use Attachment Record; cite envelope language
   only as prior logical-boundary terminology.

## Contract In One Screen

```text
Capture writes raw SourceCapturePacket (CapturePacket) truth.
The Raw Packet Store preserves raw truth and stable handles.
Attachment Records carry source-family payloads by packet/slice/file key.
The Availability Index exposes only committed-by-key facts.
Projection, ECR, SCR, Cleaning, and Judgment read raw or derived refs by key.
Those lanes write append-only Derived Result Store or Acknowledgement Log facts.
Nothing derived replaces raw truth.
```

## Record-Kind Slots

| Slot | Lake-side responsibility | Must not become | Physical status |
| --- | --- | --- | --- |
| Raw Packet Store | Preserve raw `SourceCapturePacket` bundles, stable packet/slice/file handles, `sha256`, and `hash_basis`. | Cleaned source truth, canonical identity, or mutable packet history. | Deferred. |
| Attachment Record | Carry source-family payload body plus packet identity (`packet_id`), slice identity (`slice_id` when applicable), family, kind, schema version, replay pins, and absence/refusal/residual posture. | Cleaned value, dedupe decision, credibility label, Judgment label, or downstream-use strength. | Direction recorded: manifest-indexed immutable attachment bodies; exact serialization, sidecar/member layout, manifest version, backend, and migration remain deferred. Historical docs call this the logical typed-envelope boundary. |
| Availability Index | Record only that packet/slice/file material is committed and readable by stable keys with checkable refs. | Event bus, scheduler, lane router, retry gate, priority system, or success tracker. | Deferred; by-key scan/query must work before any queue. |
| Derived Result Store | Hold append-only lane-owned derived records keyed to raw: projection receipts, ECR integrity records, SCR content records, Cleaning ledgers, and Judgment outputs. | Second raw source of truth, merged cross-kind blob, or rewritten or deleted derived history. | Deferred with derived-record physical-home blocker. |
| Acknowledgement Log | Hold append-only lane-owned completion or acknowledgement facts keyed to raw. | Lake-consumed control flow for scheduling, gating, retrying, or calling another lane. | Deferred with derived-record physical-home blocker. |

## Write And Read Discipline

- Capture writes raw material once. The lake preserves raw bytes, hashes,
  manifests, packet identity, and source-visible payload material.
- The lake may expose committed-by-key availability, but the fact is passive.
- Downstream lanes scan or query by committed packet/slice/file keys. A queue
  may later optimize notification, but it is not the source of truth.
- Derived records reference raw packet/slice/file handles and sibling derived
  records. They do not copy raw payload bodies into a second source of truth.
- Each epistemic kind remains separate. Projection receipts, ECR integrity
  records, SCR content records, Cleaning ledgers, Judgment outputs, and
  acknowledgements are siblings, not one merged object.
- When a derived taxonomy changes, re-derive rather than mutate raw or rewrite
  prior derived records in place.

## Physicalization Gate

Do not implement storage, manifest changes, Attachment Record serialization,
projection cache, queue runtime, derived-record persistence, or acknowledgement
persistence from this contract until these blockers close:

Blocker 1 now has a direction and an implementation-facing contract, not a
runtime implementation closeout. The accepted direction is manifest-indexed
immutable Attachment Records: compact manifest/index entries point to immutable
hash-checkable attachment bodies. Use
`orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
before scoping storage code. Exact layout, serialization, manifest version,
backend, and migration remain deferred.

Blocker 2 now has a direction, not a migration or code closeout. Existing
direct packet/slice fields remain legacy-readable and transitional; they are
not precedent for future direct source-family fields, not promoted to universal
lake core, and not mutated in pinned packets. Future lanes may dual-read them
with Attachment Records or replay them into new packet material under separate
authorization.

Remaining blockers before storage implementation:

1. Govern SCR `FamilyDetailBase` so it cannot become a competing raw
   source-family payload home.
2. Assign enforcement for write-once raw, no-cleaning-in-lake, append-only
   derived results, and no-new-core-field pressure to deterministic write or
   tool boundaries where possible.
3. Choose the physical home and write boundary for projection receipts, ECR
   records, SCR records, Cleaning ledgers, Judgment outputs, and downstream
   completion/acknowledgement facts.
4. Preserve by-key discovery as authority before any runtime event or queue
   engine is built.

## Blocker 1 Direction

The accepted direction for Attachment Record representation is
**manifest-indexed immutable attachment bodies**.

This chooses the relationship, not the storage backend or final wire shape:

Implementation-facing details are recorded in
`orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`;
this section remains the directional summary.

- A compact manifest or manifest-equivalent packet index entry carries
  packet/slice/file keys, family, kind, schema version, replay pins,
  attachment ref, hash, `hash_basis`, and posture summary.
- The source-family payload body stays in an immutable/checkable attachment
  body outside the core manifest payload body.
- The body may later be encoded as a packet member, sidecar, or equivalent
  immutable/hash-pinned packet material.
- Availability indexes must be rebuildable from committed packet/attachment
  keys and hashes.
- Replacing or correcting an Attachment Record writes a new record; old records
  are not rewritten in place.
- Retention and lawful-erasure policy remain later physicalization constraints.
  This direction does not select WORM behavior, crypto-shredding, or any storage
  engine.

## Blocker 2 Direction

The accepted direction for incumbent direct fields is
**legacy-readable transitional fields with future dual-read or replay only**.

This settles the fate question without migrating or implementing storage code:

- Existing direct fields at packet and slice level remain readable for current
  and historical packets.
- They are not precedent for adding new source-family payload fields directly
  to `SourceCaptureSlice` or `SourceCapturePacket`.
- They are not promoted as the future universal lake-core schema.
- New source-family payloads target Attachment Records.
- Future implementation may dual-read incumbent fields and Attachment Records
  or replay old material into new packet material, but only under a separately
  authorized implementation lane.
- Pinned historical packets are never mutated in place to fit the new
  representation.
- Exact dual-read behavior, replay triggers, migration tooling, and cutoff
  timing remain later implementation decisions.

## Non-Goals

This contract does not:

- select a storage engine;
- select Manifest v2;
- select sidecars;
- select exact packet-member vs sidecar layout;
- select Attachment Record serialization;
- define a projection cache;
- define a runtime queue or scheduler;
- define ECR, SCR, Cleaning, Judgment, or Evidence Unit (EvidenceUnit) schemas;
- define fragrance ontology or any domain ontology;
- migrate incumbent fields;
- promote incumbent direct fields as future universal lake core;
- authorize implementation;
- claim validation, readiness, approval, or acceptance.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Data Lake Storage Contract v0 now records the blocker-2 incumbent-field
    direction: existing direct packet/slice fields remain legacy-readable and
    transitional, are not precedent for new direct source-family fields, are not
    promoted to universal lake core, and may only move through future dual-read
    or replay under separate authorization; pinned packets are not mutated.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
    - orca/product/spines/capture/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/decisions/dcp_receipts_archive_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/validation-gates.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
    - orca/product/spines/capture/packet_schema/source_capture_packet_schema_evolution_architecture_v0.md
    - orca-harness/source_capture/models.py
    - orca-harness/source_capture/writer.py
    - orca-harness/source_capture/ig_projection.py
    - orca-harness/source_capture/retail_pdp_projection.py
  intentionally_not_updated:
    - path: orca-harness/source_capture/models.py and writer/projection code
      reason: >
        This patch records architecture direction only. Existing fields and
        readers remain live and readable; no runtime migration, dual-read
        implementation, replay implementation, or schema mutation is authorized.
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
      reason: >
        It already defers the migration/replay plan for incumbent direct fields.
        This patch settles the high-level fate in the storage/core/boundary
        sources without choosing dual-read mechanics or replay triggers.
  stale_language_search: >
    rg -n "Decide the fate of incumbent direct fields|Before physicalization, the incumbent field fate must be decided|Whether current `metric_observations` remain|Whether demand pins remain|migrate incumbent fields|legacy-readable transitional|future dual-read or replay"
    orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
    orca/product/spines/capture/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
    orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
    docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-06-18 after edits. No live target text still says incumbent
    direct-field fate must be decided, nor that current metric observations or
    demand pins have an open high-level fate. Hits are expected: the storage,
    core, mechanics map, attachment-boundary, and repo-map text now state the
    accepted legacy-readable / future-dual-read-or-replay direction; the storage
    contract keeps "migrate incumbent fields" only as a non-goal; this receipt
    contains the query. No hit authorizes migration, schema finalization,
    runtime implementation, validation, readiness, or storage-engine selection.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not migration authorization
    - not schema finalization
    - not storage-engine selection
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Data Lake Storage Contract v0 now records the blocker-1 implementation-facing
    Attachment Record contract: compact manifest/index entries link to immutable,
    hash-checkable attachment bodies, while exact sidecar/member layout,
    serialization, manifest version, backend, migration, validation, readiness,
    and runtime implementation remain deferred.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/decisions/dcp_receipts_archive_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/review-lanes.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
    - orca/product/spines/capture/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
    - orca/product/spines/capture/packet_schema/source_capture_packet_schema_evolution_architecture_v0.md
    - orca-harness/source_capture/models.py
    - orca-harness/source_capture/writer.py
  intentionally_not_updated:
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
      reason: >
        It remains the parent logical contract and already defers exact field
        names and physical representation; the storage contract plus new
        implementation contract own the narrower blocker-1 physicalization
        direction without reopening core boundaries.
    - path: orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
      reason: >
        It remains a planning-only mechanics map. Its broader physicalization
        gate stays stale-if-superseded by later storage/manifest/sidecar
        decisions, and this patch does not select those physical choices.
    - path: orca/product/spines/capture/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
      reason: >
        It remains the accepted logical typed-envelope boundary and explicitly
        defers physical storage. This patch records the storage-lane
        implementation contract without globally renaming historical envelope
        terminology.
  stale_language_search: >
    rg -n "table of contents|storage engine selected|sidecar selected|Manifest v2 selected|call ECR|call SCR|call Cleaning|call Projection|call Judgment|implementation readiness|runtime implementation closeout"
    orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
    orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
    orca/product/spines/capture/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
    docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-06-18 after edits. Hits are expected guardrails only: the
    new implementation contract rejects "table of contents" as architecture
    terminology and forbids the Availability Index from calling ECR, SCR,
    Cleaning, Projection, or Judgment; the storage contract states blocker 1 is
    not a runtime implementation closeout and contains the query in this
    receipt; the mechanics map hit is an older receipt non-claim against
    implementation readiness. No hit selects a backend, sidecar, Manifest v2,
    runtime implementation, validation, or readiness.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not Manifest v2 selection
    - not sidecar selection
    - not storage-engine selection
```

Older receipts are archived in `docs/decisions/dcp_receipts_archive_v0.md`.
