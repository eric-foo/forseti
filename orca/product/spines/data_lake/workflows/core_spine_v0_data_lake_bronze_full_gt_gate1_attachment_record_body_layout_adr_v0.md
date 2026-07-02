# Core Spine v0 Data Lake Bronze Full-GT Gate 1 Attachment Record Body Layout ADR v0

```yaml
retrieval_header_version: 1
artifact_role: Data Lake workflow/decision-request record
scope: >
  Gate 1 ADR for the Bronze full-GT physicalization lane: decide the physical
  relationship binding a compact Attachment Record entry to its immutable,
  hash-checkable body, producing the eight minimum Gate 1 outputs required by
  the physicalization decision brief, for owner ratification.
use_when:
  - Adjudicating or ratifying the Gate 1 body-layout decision.
  - Scoping later implementation of Attachment Record bodies after ratification.
  - Checking which body-layout shapes are selected, deferred, or rejected.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
stale_if:
  - The owner ratifies, modifies, or rejects this ADR (the ratification block below then governs).
  - The Attachment Record, Storage, or Physicality Location contract changes the body-relationship boundary.
  - A later accepted ADR supersedes the body-layout selection.
```

## Status

`GATE1_ADR_AUTHORED_AWAITING_RATIFICATION_V0`.

This is a decision-request record. It selects nothing until the owner ratifies
it. It is not implementation authorization, backend/engine selection, Manifest
v2 or serialization selection, migration authority, validation, readiness, or a
Bronze full-GT claim. On ratification, folding the decision into the authority
contracts is a separate step carrying its own `direction_change_propagation`
receipt.

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom gate1 pack (brief + AR implementation + storage + physicality contracts, read in full)
  edit_permission: docs-write
  target_scope: Gate 1 body-layout ADR authoring; no runtime or contract edits.
  dirty_state_checked: yes
  blocked_if_missing: none
```

## Decision In One Screen

```text
Selected (pending ratification): PACKET-MEMBER is the default physical body
home. An Attachment Record body lands as immutable packet material inside the
packet's raw container under the current raw-admission grammar, exactly as
preserved files land today; this selects the body relationship, not a new raw
path schema. The attachments/ sidecar slot stays RESERVED, usable only through
a future ADR when a body genuinely cannot land inside its packet. External
blob/database bodies (G1-D) stay locked behind Gate 2 plus a separate
backend/physicalization ADR that proves the storage invariants. Durable entry
serialization (Manifest v2 vs packet-index) stays deferred to the A2 fork,
which stays gated on the A1 deterministic inventory.
```

Why this wins: it ratifies the physical reality that two Silver consumer
proofs already exercise, adds zero migration, keeps one body home (one
`hash_basis` discipline, one resolution path), and spends no lock-in on
serialization or backend before the A1 inventory and Gate 2 exist.

## Option Ledger (adjudicated)

| Option | Shape | Disposition | Why |
| --- | --- | --- | --- |
| G1-A incumbent generated-AR posture | Keep generated AR entries over preserved bodies; layout formally undecided. | Subsumed | Its physical substance IS packet-member; this ADR ratifies that substance instead of leaving it incidental. |
| G1-B packet-member / bundle body | Body is immutable packet material with a compact keyed entry. | **Selected as default** | Matches current proven reality; strongest raw-authority fit; hash basis and packet identity stay local; no second body home. |
| G1-C hash-pinned sidecar under `attachments/` | Body lives beside packets, keyed and hash-pinned. | Deferred (slot reserved) | No current body needs it; a second home doubles resolution/verification paths. Reopen trigger below. |
| G1-D external blob/database row | Body in backend material with hash-checked ref. | Rejected until Gate 2 plus a backend/physicalization ADR | Highest lock-in; the storage contract's engine boundary and Gate 2 must be satisfied before an external body store is even eligible. |

Sidecar reopen trigger: a concrete body that cannot land inside its packet at
publish time - late-arriving material for a pinned packet, or media whose size
makes packet bundling operationally wrong. That future ADR must keep the
sidecar packet-keyed, indexed, and hash-checkable (loose sidecars stay
rejected per the AR contract).

## The Eight Required Gate 1 Outputs

1. **Body key.** An entry finds its body with: `packet_id`, `slice_id` when
   applicable, packet-scoped file/attachment key, `source_family`,
   `payload_kind`, `payload_schema_version`, replay/version pins, body
   reference (packet-relative path), `sha256`, `hash_basis` - the entry-key
   list already bound by the AR implementation contract, affirmed here with
   the body reference fixed as packet-relative.
2. **`hash_basis`.** `raw_stored_bytes`: the hash covers exactly the stored
   body file's bytes as published, per the existing `PreservedFile`
   discipline - promoted by this ADR from "evidence of a viable pattern" to
   the rule. A verifier re-reads the packet-relative file and re-hashes those
   bytes; nothing else (no manifest text, no metadata) is inside the basis.
3. **Physical relationship.** Packet-member: the body is immutable material
   inside the packet's raw container under the raw-admission key grammar
   (currently `raw/<packet_shard>/<packet_id>/`, with by-key lookup recomputing
   the shard), written once at staging/publish. The body reference remains
   packet-relative; this ADR does not create a second raw path contract.
   `attachments/` reserved (deferred), external bodies rejected until Gate 2
   plus a backend/physicalization ADR.
4. **Public read surface.** `source_surface_catalog_rows`,
   `load_attachment_record_body`, and their successors remain the only public
   resolution path; Silver resolves and hash-verifies through them and never
   infers private packet-member paths (AR contract acceptance check 8).
5. **Authority split.** Generated catalog rows, AR rows, and indexes remain
   rebuildable read surfaces - never raw authority and never private
   physical-layout contracts. The packet and its hashes are the only truth.
6. **Rebuild rule.** All indexes/catalog state rebuild from committed packet
   material and keys; nothing about this selection makes any index
   load-bearing.
7. **Replay/migration implication.** Zero body-home migration for the currently
   exercised preserved-body shape: existing packets already satisfy the selected
   relationship. Raw path grammar, Manifest/index serialization, dual-read, and
   replay mechanics remain separate decisions. Incumbent direct fields stay
   legacy-readable (storage contract blocker-2 direction); corrections/replays
   append new packet material; pinned packets are never mutated in place.
8. **Rejected shapes.** Everything the AR contract rejects, affirmed;
   plus, from this ADR: no second body home without a ratified ADR; no body
   bytes promoted into lake-core fields; no consumer resolution that bypasses
   the public surface; no treating entry rows as bodies.

## Named Residuals (accepted if ratified)

- **Durable entry serialization stays open.** Entries today are generated
  catalog rows, not durable manifest/index records. Deciding Manifest v2
  versus a manifest-equivalent packet index is the A2 fork, gated on the A1
  deterministic inventory. Ratifying this ADR does not shrink that fork.
- **Media-scale bodies untested.** The selected shape is proven for text-like
  bodies; a media-heavy source family may hit the sidecar reopen trigger.
- **Backend remains unselected.** Packet-member is a layout relationship, not
  a filesystem commitment; a future backend must reproduce this relationship
  and prove the storage-contract invariants. Gate 2 ratification or deferral
  alone does not unlock G1-D external bodies.

## Owner Ratification

```yaml
gate1_ratification:
  decision: ratified | modified | rejected   # owner_to_fill
  ratified_by: owner_to_fill
  date: owner_to_fill
  modifications: owner_to_fill_or_none
```

## Non-Claims

- Not implementation authorization; not backend, engine, object-store,
  database, or hybrid selection.
- Not Manifest v2, packet-index, serialization, replay-mechanics, or cutoff
  selection (A2 stays gated on A1).
- Not retention, lawful-erasure, WORM, or deletion posture (Gate 2 ADR).
- Not validation, readiness, third-proof authorization, or Bronze full GT.
