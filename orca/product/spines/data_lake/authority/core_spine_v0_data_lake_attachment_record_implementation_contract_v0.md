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
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
  - orca/product/spines/capture/core/packet_schema/source_capture_packet_schema_evolution_architecture_v0.md
stale_if:
  - Data Lake Storage Contract v0 reopens or supersedes the blocker-1 direction.
  - Source Capture packet manifest/read-write mechanics change attachment or preserved-file reference semantics.
  - A later accepted Manifest v2, sidecar/member layout, backend, migration, or lawful-erasure decision supersedes this contract.
  - The Silver Vault raw-ref or Bronze intake boundary changes.
authority_boundary: retrieval_only
```

## Status

`BLOCKER_1_IMPLEMENTATION_CONTRACT_RECORDED_V0; GATE1_BODY_LAYOUT_FOLDED_IN_V0`.

This artifact converts the accepted blocker-1 direction into an
implementation-facing contract. The body-layout relationship it previously left
open is now decided: the owner-ratified Gate 1 body-layout ADR (2026-07-02)
selects packet-member as the default physical relationship (see Required Shape
and Accepted Implementation Shapes below). It is not code, implementation
authority, validation, readiness, Manifest v2 selection, packet serialization,
migration authority, queue design, or engine/backend selection by this
artifact. Engine/backend choice is delegated to the Storage Contract
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
2. The attachment body carries the source-family payload body. The ratified
   Gate 1 body-layout ADR (2026-07-02) selects packet-member as the default
   physical relationship: the body lands as immutable packet material inside
   the packet's raw container under the raw-admission key grammar
   (`raw/<packet_shard>/<packet_id>/`), with a packet-relative body reference.
   The `attachments/` sidecar slot stays reserved, usable only through a future
   ADR on that ADR's named reopen trigger; external blob/database bodies (G1-D)
   stay rejected until Gate 2 plus a separate backend/physicalization ADR
   proves the storage invariants.
3. The body must be immutable and checkable from the entry. The hash basis must
   say what bytes are covered. Per the ratified Gate 1 ADR,
   `hash_basis: raw_stored_bytes` — the hash covers exactly the stored body
   file's bytes as published, per the `PreservedFile` discipline — is promoted
   from viable-pattern evidence to the rule for packet-member bodies. This is
   the hash-basis rule, not a final Attachment Record entry schema.
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

The Gate 1 body-layout ADR
(`orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md`,
owner-ratified 2026-07-02) adjudicated the previously open shapes:

- compact manifest or manifest-equivalent packet-index entry plus
  packet-member body — **selected default**;
- compact entry plus immutable/hash-pinned sidecar body under `attachments/` —
  reserved; usable only through a future ADR on the named reopen trigger (a
  body that genuinely cannot land inside its packet);
- external blob/database body — rejected until Gate 2 plus a separate
  backend/physicalization ADR proves the storage invariants.

The common requirement is unchanged: a compact keyed entry points to an
immutable/checkable body. The entry-side serialization (Manifest v2 versus a
manifest-equivalent packet index — the A2 fork) remains open and stays gated on
the A1 deterministic inventory.

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
8. A Silver producer can resolve an Attachment Record through public Bronze
   surfaces, verify the body hash, and carry the AR-backed source ref into
   Silver `raw_refs` without reading private packet-member paths.

## Silver Consumption Contract

Attachment Records are the typed raw-payload cards Silver may cite when it turns
source-family payload bodies into source-backed semantic records. The preserved
body remains Bronze raw evidence; Silver carries a ref, not a second source body.

For source-family payload bodies, the Silver-side ref should carry enough AR
entry material to re-resolve and verify the body: `attachment_record_id`,
Attachment Record schema version, physicalization, `packet_id`, packet/body ref,
`body_sha256`, `hash_basis`, `source_family`, `source_surface`, `payload_kind`,
`payload_schema_version`, replay/version pins, and producer-owned provenance
needed by the Silver producer contract.

A Silver producer that finds no Attachment Record row may fall back to
hash-checkable raw packet refs only when its own contract allows that fallback;
the missing typed AR row must remain visible as residual/posture. The fallback is
not proof that the payload was absent and does not let the producer infer folder
semantics.

This contract still does not authorize runtime AR implementation, a new storage
layout, Manifest v2, migration, or a Silver producer. It only binds the consumer
shape that a future implementation must satisfy.

## Deferred Decisions

Resolved 2026-07-02 and no longer open here: exact packet-member versus sidecar
versus equivalent layout — the Gate 1 body-layout ADR ratified packet-member as
the default, with the sidecar reserved behind its reopen trigger.

This contract deliberately leaves the following decisions open:

- exact manifest/index serialization;
- Manifest v2 or other versioning mechanics (the A2 fork, gated on the A1
  deterministic inventory);
- selected physical backend/engine, including database, object store,
  warehouse/lakehouse, DuckDB or another SQL-capable embedded engine, or queue;
- migration or replay plan for incumbent direct fields;
- SCR `FamilyDetailBase` governance;
- lawful erasure, retention, WORM, or crypto-shredding mechanics — posture now
  governed by the ratified Gate 2 deferral ADR
  (`orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md`):
  a bounded accepted residual with a claim ceiling, tombstone/supersession as
  the working unavailability posture, forbidden backend classes/operations
  while deferred, and revisit triggers T1-T4; the mechanics remain undesigned
  while that deferral stands;
- enforcement placement for no-new-core-field pressure and append-only derived
  records.

## Non-Goals

This artifact does not authorize runtime implementation, engine/backend
selection, packet mutation, manifest migration, source-family schema design,
derived-record persistence, queue runtime, validation, approval, readiness, or
architecture completion.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Fold-in of the owner-ratified Gate 1 body-layout ADR (2026-07-02): this
    contract now states packet-member as the ratified default Attachment
    Record body relationship (sidecar reserved behind its reopen trigger,
    external bodies locked behind Gate 2 plus a backend/physicalization ADR,
    hash_basis raw_stored_bytes promoted from viable-pattern evidence to the
    rule), and its lawful-erasure deferral now points at the ratified Gate 2
    deferral ADR; the A2 entry-serialization fork stays deferred, gated on the
    A1 deterministic inventory.
  trigger: architecture_doctrine
  controlling_sources_updated:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_lake_owner_explainer_v0.md
    - orca/product/spines/data_lake/README.md
  intentionally_not_updated:
    - path: orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
      reason: >
        Its only layout-deferral hit sits inside a historical DCP receipt, not
        live routing text; no live sentence claims the body layout is open.
    - path: orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_lake_owner_explainer_v0.md
      reason: >
        It explains what the gates protect and routes live state through the
        batch plan's open_next chain (synced in PR #579); the ratified
        postures do not contradict its gates section, so its stale_if does
        not fire.
    - path: orca/product/spines/data_lake/README.md
      reason: >
        Its Attachment Record mentions are ownership language with no
        layout-undecided claim.
  stale_language_search: >
    rg -n "placement deferred|physical home unfrozen|does not choose among
    those layouts|exact layout remains open|sidecar/member layout|
    member-vs-sidecar|member vs sidecar" orca/product/spines/data_lake
    docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-07-02 after edits. Remaining hits: this contract's stale_if
    (a supersession condition, not an open-layout claim), the ratification
    annotations added by this fold-in (raw-admission and derived-layout
    contracts), the storage contract's annotated non-goal, and the gate ADR /
    brief / batch-plan family (historical gate records). No live surface
    still claims the AR body layout is undecided.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not Manifest v2 or serialization selection (A2 stays gated on A1)
    - not a Bronze full-GT claim
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Attachment Record implementation doctrine now binds Silver consumption: AR
    entries are typed raw-payload refs over preserved Bronze bodies, Silver
    records carry AR-backed raw_refs when deriving facts from source-family
    payload bodies, and missing AR rows remain visible residual/posture rather
    than inferred absence.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
    - orca/product/spines/data_lake/README.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - orca-harness/data_lake/catalog.py
  intentionally_not_updated:
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
      reason: >
        Storage still owns Manifest v2, sidecar/member/body-store layout,
        backend, migration, retention, and lawful-erasure choices. This patch
        binds consumer shape without selecting those physicalization decisions.
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
      reason: >
        Core already defines Attachment Records as source-payload refs and
        forbids cleaned/Judgment meaning. This patch narrows downstream Silver
        consumption mechanics without changing the parent boundary.
    - path: orca-harness/data_lake/catalog.py
      reason: >
        Existing post-PR-525 catalog helpers expose AR rows and body hash
        verification; no runtime implementation is authorized here.
  stale_language_search: >
    rg -n "Attachment Record|raw_refs|Silver|Manifest v2|body store|full God Tier"
    orca/product/spines/data_lake orca-harness/data_lake/catalog.py docs/workflows/orca_repo_map_v0.md
  non_claims:
    - not validation
    - not readiness
    - not runtime implementation authorization
    - not Manifest v2 selection
    - not body-store layout selection
    - not Silver producer implementation
```

Older receipts are archived in `docs/decisions/dcp_receipts_archive_v0.md`.
