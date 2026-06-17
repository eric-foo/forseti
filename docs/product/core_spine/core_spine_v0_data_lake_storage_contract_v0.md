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
  - docs/product/core_spine/core_spine_v0_data_lake_core_contract_v0.md
  - docs/product/core_spine/core_spine_v0_data_lake_mechanics_map_v0.md
  - docs/product/data_capture_spine/source_capture_tenant_payload_attachment_boundary_v0.md
  - docs/product/core_spine_v0_projection_doctrine_v0.md
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

`TARGET_STORAGE_CONTRACT_RECORDED_V0`.

This is a planning and architecture contract. It is not implementation
authority, validation, readiness, physical storage selection, queue design,
schema finalization, migration authority, or storage-engine selection.

## Goal

Define the smallest complete storage contract that lets later lanes know where
data lands and how derived work attaches, without making the data lake smart.

## Success Signals

This goal is successful when all of the following are true:

1. A future lane can say exactly what the lake stores: raw packet truth, stable
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
Capture writes raw SourceCapturePacket truth.
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
| Attachment Record | Carry source-family payload body plus scope, family, kind, schema version, replay pins, and absence/refusal/residual posture. | Cleaned value, dedupe decision, credibility label, Judgment label, or downstream-use strength. | Deferred; historical docs call this the logical typed-envelope boundary. |
| Availability Index | Record only that packet/slice/file material is committed and readable by stable keys with checkable refs. | Event bus, scheduler, lane router, retry gate, priority system, or success tracker. | Deferred; by-key scan/query must work before any queue. |
| Derived Result Store | Hold append-only lane-owned derived records keyed to raw: projection receipts, ECR integrity records, SCR content records, Cleaning ledgers, and Judgment outputs. | Second raw source of truth, merged cross-kind blob, or rewritten derived history. | Deferred with derived-record physical-home blocker. |
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

1. Choose the Attachment Record physical representation: manifest child,
   immutable sidecar, hash-pinned bundle member, or another immutable/checkable
   form.
2. Decide the fate of incumbent direct fields at slice and packet level.
3. Govern SCR `FamilyDetailBase` so it cannot become a competing raw
   source-family payload home.
4. Assign enforcement for write-once raw, no-cleaning-in-lake, append-only
   derived results, and no-new-core-field pressure to deterministic write or
   tool boundaries where possible.
5. Choose the physical home and write boundary for projection receipts, ECR
   records, SCR records, Cleaning ledgers, Judgment outputs, and downstream
   completion/acknowledgement facts.
6. Preserve by-key discovery as authority before any runtime event or queue
   engine is built.

## Non-Goals

This contract does not:

- select a storage engine;
- select Manifest v2;
- select sidecars;
- select Attachment Record serialization;
- define a projection cache;
- define a runtime queue or scheduler;
- define ECR, SCR, Cleaning, Judgment, or Evidence Unit schemas;
- define fragrance ontology or any domain ontology;
- migrate incumbent fields;
- authorize implementation;
- claim validation, readiness, approval, or acceptance.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Data Lake Storage Contract v0 records the non-selecting storage contract:
    five dumb record-kind slots, passive by-key availability, append-only
    derived/ack attachment, Attachment Record target terminology, and the six
    physicalization blockers, while selecting no storage engine, manifest,
    sidecar, serialization, queue, schema, migration, validation, or readiness.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - docs/product/core_spine/core_spine_v0_data_lake_storage_contract_v0.md
    - docs/product/core_spine/core_spine_v0_data_lake_core_contract_v0.md
    - docs/product/core_spine/core_spine_v0_data_lake_mechanics_map_v0.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/workflows/ecr_spine_submap_v0.md
  intentionally_not_updated:
    - path: docs/product/data_capture_spine/source_capture_tenant_payload_attachment_boundary_v0.md
      reason: >
        It remains the accepted logical source-family payload boundary and uses
        historical typed-envelope terminology deliberately; this storage contract
        translates that boundary to Attachment Record target terminology only for
        the lake storage lane.
    - path: docs/product/data_capture_spine/retail_pdp_typed_envelope_probe_v0.md
      reason: >
        It remains a historical non-IG logical fit probe for the typed-envelope
        boundary and is not the target storage contract.
  stale_language_search: >
    rg -n "physical envelope|storage envelope|envelope serialization|Envelope serialization|Source Payload Envelope|Typed envelope|typed envelopes|payload envelopes|source-family payload envelopes|packet/slice envelopes|Raw \+ core facts \+ envelopes"
    docs/product/core_spine/core_spine_v0_data_lake_core_contract_v0.md
    docs/product/core_spine/core_spine_v0_data_lake_mechanics_map_v0.md
    docs/product/core_spine/core_spine_v0_data_lake_storage_contract_v0.md
    docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-06-17 after edits. No target-surface hits; after recording
    this receipt, the exact query appears only in this stale_language_search
    field. A broader "envelope|Envelope" scan still finds only historical
    logical-boundary/probe references, file names, explicit "not the target
    storage name" language, and unrelated run-envelope text outside the storage
    target surface.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not physical storage selection
```
