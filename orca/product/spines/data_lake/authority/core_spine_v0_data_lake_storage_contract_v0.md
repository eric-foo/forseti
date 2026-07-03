# Core Spine v0 Data Lake Storage Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract
scope: >
  Storage contract for Orca's data lake: dumb record-kind slots, write/read
  disciplines, success signals, physicalization blockers, and the boundary for
  deliberate engine/backend selection.
use_when:
  - Preparing data-lake storage, manifest, index, or derived-result work after the logical lake contract.
  - Checking whether a lake change deliberately selects a physical engine/backend under the physicalization gate, or accidentally bypasses that gate.
  - Explaining where Capture, Projection, ECR/SCR, Cleaning, and Judgment attach without replacing raw truth.
open_next:
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
  - orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
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

`TARGET_STORAGE_CONTRACT_RECORDED_V0; BLOCKER_1_DIRECTION_RECORDED_V0; BLOCKER_1_IMPLEMENTATION_CONTRACT_RECORDED_V0; BLOCKER_2_DIRECTION_RECORDED_V0; GATE1_BODY_LAYOUT_FOLDED_IN_V0; GATE2_ERASURE_DEFERRAL_POINTED_V0`.

This is a planning and architecture contract. It is not implementation
authority, validation, readiness, physical storage selection, queue design,
schema finalization, migration authority, or storage-engine selection. It does
not itself choose the engine/backend. Engine/backend selection is now permitted
only as a separately scoped physicalization or implementation decision that
preserves the lake invariants below.

## Goal

Define the smallest complete storage contract that lets later lanes know where
data lands and how derived work attaches, without making the data lake smart,
while allowing a later bounded lane to choose the concrete physical engine.

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
5. Physical choices are not selected in this contract: storage engine/backend
   (including filesystem-only, SQL-capable embedded engines such as DuckDB,
   databases, object stores, warehouses/lakehouses, or hybrids), manifest v2,
   sidecar contract, serialization, projection cache, queue runtime, schema,
   migration, or validation/readiness claim.
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
| Attachment Record | Carry source-family payload body plus packet identity (`packet_id`), slice identity (`slice_id` when applicable), family, kind, schema version, replay pins, and absence/refusal/residual posture. | Cleaned value, dedupe decision, credibility label, Judgment label, or downstream-use strength. | Direction recorded: manifest-indexed immutable attachment bodies. Body layout ratified (Gate 1 body-layout ADR, 2026-07-02): packet-member default, `attachments/` sidecar reserved behind its reopen trigger, external bodies locked behind Gate 2 plus a backend ADR. Entry serialization ratified (A2 ADR, 2026-07-03): manifest-equivalent packet index with the versioned entry schema plus deterministic derivation rule as the canonical object; materialized rows stay generated and non-authoritative. Backend and incumbent-field migration remain deferred. Historical docs call this the logical typed-envelope boundary. |
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
before scoping storage code. The body layout is now ratified: packet-member
default per the Gate 1 body-layout ADR
(`orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md`,
2026-07-02), with the `attachments/` sidecar reserved behind its reopen
trigger. Entry serialization is now ratified: manifest-equivalent packet index
per the A2 entry-serialization ADR
(`orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_a2_attachment_record_entry_serialization_adr_v0.md`,
2026-07-03) — the versioned entry schema plus deterministic derivation rule is
the canonical object; materialized rows stay generated and non-authoritative;
Manifest v2 stays reserved behind that ADR's revisit triggers. Backend and
incumbent-field migration remain deferred.

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

## Engine Selection Boundary

The earlier blanket **no storage engine** posture is retired. This contract
still selects no engine by itself, but engine/backend choice is now an allowed
downstream physicalization decision.

Valid candidates may include the incumbent filesystem-only layout, a concrete
SQL-capable embedded engine such as DuckDB, a conventional database, an object
store, a warehouse/lakehouse, or a hybrid. Treat "SQL" as a query/interface
property unless the lane names a concrete engine.

A selection is acceptable only if the lane proves these invariants:

- raw packet material remains immutable/create-only and hash-checkable;
- derived records and acknowledgements remain append-only;
- `indexes/` remains rebuildable and non-authoritative;
- by-key discovery works without relying on a queue/event message as truth;
- the Availability Index stays content-free and passive;
- source-family payloads stay out of lake-core fields unless a later owner
  decision cites a cross-family promotion rule;
- the lake does not clean, dedupe, score, judge, schedule, retry, route, or call
  downstream lanes;
- operational data stays outside the Git repo, or the physicality-location
  contract is explicitly superseded for a different external backend model;
- retention semantics stay inert per the ratified Gate 2 deferral ADR: no
  backend lifecycle, expiry, versioning-cleanup, or WORM mode may carry
  retention policy while the deferral stands, and drafting any backend/engine
  selection ADR fires that ADR's revisit trigger T3 (re-ratify the deferral
  against the candidate backend's semantics, or produce the full
  retention/erasure ADR first);
- tests or equivalent deterministic checks prove write-once, append-only,
  read-by-key, hash verification, and index-rebuild behavior for the selected
  engine.

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
- The body lands as packet-member material by default (ratified Gate 1
  body-layout ADR, 2026-07-02): immutable packet material inside the packet's
  raw container under the raw-admission key grammar, with a packet-relative
  body reference. The `attachments/` sidecar stays reserved behind that ADR's
  reopen trigger; external bodies stay rejected until Gate 2 plus a separate
  backend/physicalization ADR.
- Availability indexes must be rebuildable from committed packet/attachment
  keys and hashes.
- Replacing or correcting an Attachment Record writes a new record; old records
  are not rewritten in place.
- Retention and lawful-erasure posture is recorded in the ratified Gate 2
  deferral ADR
  (`orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md`,
  2026-07-02): lawful erasure is a bounded accepted residual with a written
  claim ceiling; append-only tombstone/supersession records are the working
  unavailability posture; backend-native lifecycle/retention/WORM semantics
  must stay inert while the deferral stands. This direction still selects no
  WORM behavior, crypto-shredding, or storage engine.

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

- select a storage engine inside this artifact; engine/backend selection is now
  a permitted downstream physicalization decision, not a forbidden doctrine
  change;
- select Manifest v2 (reserved behind the A2 ADR's revisit triggers, not by
  this contract);
- select sidecars;
- select exact packet-member vs sidecar layout (now ratified by the Gate 1
  body-layout ADR, not by this contract);
- select Attachment Record serialization (now ratified by the A2
  entry-serialization ADR, not by this contract);
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
    Fold-in of the owner-ratified A2 entry-serialization ADR (2026-07-03): the
    Attachment Record slot row and blocker-1 direction now state the ratified
    manifest-equivalent packet index (versioned entry schema plus deterministic
    derivation rule canonical; materialized rows generated and
    non-authoritative), and the non-goals annotate Manifest v2 and entry
    serialization as ADR-owned decisions, not contract selections.
  trigger: architecture_doctrine
  controlling_sources_updated:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  downstream_surfaces_checked:
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_a2_attachment_record_entry_serialization_adr_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
  intentionally_not_updated:
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
      reason: >
        Its deferred list already carries the 2026-07-02 annotation pointing
        layout decisions at the gate ADRs; its "exact serialization" deferral
        concerns per-lane derived-record wire shapes it owns, not the AR entry
        serialization the A2 ADR decided.
  stale_language_search: >
    rg -n "serialization.*remain deferred|remain deferred.*serialization|select
    Attachment Record serialization" orca/product/spines/data_lake/authority
  stale_language_search_result: >
    Executed 2026-07-03 after edits. Remaining hits are the annotated non-goal
    lines in this contract (ADR-ownership annotations added by this fold-in),
    the derived-layout contract's per-lane wire-shape deferral (out of A2
    scope), and historical receipt text. No live surface still defers the AR
    entry serialization.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization by this contract
    - not engine/backend selection
    - not a Bronze full-GT claim
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Fold-in of the two owner-ratified physicalization gates (2026-07-02): the
    blocker-1 direction and the Attachment Record slot row now state the
    ratified packet-member default body layout (sidecar reserved behind its
    reopen trigger, external bodies locked behind Gate 2 plus a backend ADR),
    and the retention/lawful-erasure constraint now points at the ratified
    Gate 2 deferral ADR — including a new engine-selection invariant that
    backend-native retention semantics stay inert while the deferral stands
    and that drafting any backend/engine ADR fires Gate 2 revisit trigger T3.
  trigger: architecture_doctrine
  controlling_sources_updated:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  downstream_surfaces_checked:
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
      reason: >
        Its "physical representation remain deferred" line concerns record
        field schemas, not the AR body-layout fork; it carries no Gate 1 or
        Gate 2 stale language.
  stale_language_search: >
    rg -n "remain later physicalization constraints|remain deferred|sidecar/member layout"
    orca/product/spines/data_lake/authority
  stale_language_search_result: >
    Executed 2026-07-02 after edits. "remain later physicalization
    constraints" has zero hits (the retention sentence now points at the
    ratified Gate 2 deferral ADR). Remaining "remain deferred" hits concern
    serialization, manifest version, backend, migration, shard width, config
    mechanics, or field schemas — all genuinely still open. The only
    sidecar/member-layout hits are supersession conditions and the
    ratification annotations added by this fold-in.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not engine/backend selection
    - not erasure capability (the Gate 2 claim ceiling governs deletion language)
    - not a Bronze full-GT claim
```

Older receipts are archived in `docs/decisions/dcp_receipts_archive_v0.md`.
