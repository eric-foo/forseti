# Core Spine v0 Data Lake Attachment Record Implementation Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract
scope: >
  Implementation-facing contract for the Data Lake Storage Contract blocker-1
  direction: manifest-indexed immutable Attachment Record bodies.
use_when:
  - Scoping future Attachment Record storage, manifest, packet-index, or packet-bundle work.
  - Checking whether a proposed storage implementation preserves the no-smart-lake boundary.
  - Reviewing whether source-family payload bodies are traceable, retrievable, and hash-checkable without becoming lake-core fields.
open_next:
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
  - orca/product/spines/capture/core/packet_schema/source_capture_packet_schema_evolution_architecture_v0.md
stale_if:
  - Data Lake Storage Contract v0 reopens or supersedes the blocker-1 direction.
  - Source Capture packet manifest/read-write mechanics change attachment or preserved-file reference semantics.
  - A later accepted Manifest v2, sidecar/member layout, backend, migration, or lawful-erasure decision supersedes this contract.
authority_boundary: retrieval_only
```

## Status

`BLOCKER_1_IMPLEMENTATION_CONTRACT_RECORDED_V0`.

This artifact converts the accepted blocker-1 direction into an
implementation-facing contract. It is not code, implementation authority,
validation, readiness, Manifest v2 selection, packet serialization, sidecar
selection, migration authority, queue design, or engine/backend selection by
this artifact. Engine/backend choice is delegated to the Storage Contract
physicalization boundary.

## Contract Summary

An Attachment Record is represented as two linked pieces:

1. A compact manifest or manifest-equivalent packet index entry.
2. An immutable, hash-checkable attachment body that carries the source-family
   payload.

The entry makes the record traceable and retrievable by key. The body preserves
the source-family payload without turning it into a new lake-core field. The
lake stores and exposes the keyed fact; it does not interpret, clean, score,
route, retry, or call downstream lanes.

## Required Shape

1. The manifest/index entry must carry enough keying to find the body without
   source-family interpretation: `packet_id`, `slice_id` when applicable, a
   packet-scoped attachment or file key when needed, source family, payload
   kind, payload schema version, replay/version pins, attachment reference,
   hash, `hash_basis`, and absence/refusal/residual posture summary.
2. The attachment body carries the source-family payload body. It may later be a
   packet member, sidecar, hash-pinned bundle member, or equivalent immutable
   packet material, but this contract does not choose among those layouts.
3. The body must be immutable and checkable from the entry. The hash basis must
   say what bytes are covered, following the current `PreservedFile` pattern as
   evidence of a viable ref/hash/hash-basis discipline, not as a final
   Attachment Record schema.
4. The Availability Index must be rebuildable from committed packet,
   Attachment Record, key, reference, hash, and `hash_basis` material. It is a
   passive findability surface, not an event bus, scheduler, router, retry
   engine, or success tracker.
5. Replacing, correcting, or replaying an Attachment Record writes a new record
   or new packet material. Existing packet material is not rewritten in place.
6. Attachment Records may carry relationship or supersession references, but
   the lake must not choose which record is current for a downstream purpose.
   Reader lanes own use-time selection under their own contracts.
7. Attachment Records must not carry cleaned values, canonical entity
   decisions, dedupe decisions, credibility labels, Judgment labels, or
   downstream-use strength.

## Accepted Implementation Shapes

These shapes remain acceptable for a future physicalization lane if they satisfy
the required shape above:

- compact manifest entry plus packet-bundle member body;
- compact manifest entry plus immutable/hash-pinned sidecar body;
- compact manifest-equivalent packet index entry plus equivalent immutable,
  hash-checkable packet material.

The common requirement is the relationship: a compact keyed entry points to an
immutable/checkable body. The exact layout remains open.

## Rejected Implementation Shapes

Future storage implementation must not:

- stuff arbitrary source-family payload bodies into new lake-core manifest
  fields;
- create loose sidecars that are not packet-keyed, indexed, and hash-checkable;
- make a mutable database row the only canonical raw payload body;
- make the Availability Index call ECR, SCR, Cleaning, Projection, Judgment, or
  any queue/scheduler;
- treat "table of contents" as architecture terminology for this contract.
  The source term remains manifest/index entry.

## Current Source Evidence

- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md`
  records the accepted blocker-1 direction as manifest-indexed immutable
  Attachment Record bodies and keeps layout, serialization, backend, and
  migration deferred.
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md`
  defines Attachment Records as the target term for new source-family payloads
  and forbids treating them as cleaned values or downstream-use strength.
- `orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md`
  preserves the older logical typed-envelope boundary while explicitly
  deferring physical storage choice.
- `orca/product/spines/capture/core/packet_schema/source_capture_packet_schema_evolution_architecture_v0.md`
  preserves write-once/hash-pin discipline: future currentness is replay into
  new packet material, not in-place packet mutation.
- `orca-harness/source_capture/models.py` and
  `orca-harness/source_capture/writer.py` show the current preserved-file
  ref/hash/hash-basis pattern: packet-relative paths, `sha256`, and
  `hash_basis="raw_stored_bytes"` for copied raw files.

## Future Implementation Acceptance Checks

A future implementation lane is not complete unless it can prove, with code and
tests appropriate to that lane, that:

1. Given a packet, a reader can enumerate Attachment Record entries without
   source-family interpretation.
2. Given an Attachment Record entry, a reader can resolve the body reference and
   verify the body hash under the recorded `hash_basis`.
3. Given packet/slice/file or attachment keys, a reader can discover the
   committed Attachment Record material without a queue message.
4. The Availability Index can be rebuilt from committed packet material rather
   than maintained as a hidden source of truth.
5. Correction, replacement, replay, or migration paths append new material and
   do not mutate pinned historical packet material in place.
6. No lake-core model grows a new direct source-family payload field merely
   because one source family needs it.
7. No lake write/read path calls ECR, SCR, Cleaning, Projection, Judgment, a
   scheduler, or a retry engine as part of storing or exposing the keyed
   Attachment Record fact.

## Deferred Decisions

This contract deliberately leaves the following decisions open:

- exact packet member versus sidecar versus equivalent layout;
- exact manifest/index serialization;
- Manifest v2 or other versioning mechanics;
- selected physical backend/engine, including database, object store,
  warehouse/lakehouse, DuckDB or another SQL-capable embedded engine, or queue;
- migration or replay plan for incumbent direct fields;
- SCR `FamilyDetailBase` governance;
- lawful erasure, retention, WORM, or crypto-shredding mechanics;
- enforcement placement for no-new-core-field pressure and append-only derived
  records.

## Non-Goals

This artifact does not authorize runtime implementation, engine/backend
selection, packet mutation, manifest migration, source-family schema design,
derived-record persistence, queue runtime, validation, approval, readiness, or
architecture completion.
