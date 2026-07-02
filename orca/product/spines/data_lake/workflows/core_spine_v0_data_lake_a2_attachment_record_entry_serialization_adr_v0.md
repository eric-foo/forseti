# Core Spine v0 Data Lake A2 Attachment Record Entry Serialization ADR v0

```yaml
retrieval_header_version: 1
artifact_role: Data Lake workflow/decision-request record
scope: >
  A2 ADR for the Bronze full-GT lane: decide the durable, canonical
  serialization of the Attachment Record entry (the compact keyed card over
  each packet-member body), selecting among Manifest v2, a
  manifest-equivalent packet index, a hybrid, or a novel shape, for owner
  ratification. Consumes the A1 touchpoint inventory evidence and an
  adjudicated cross-vendor consultation.
use_when:
  - Adjudicating or ratifying the A2 entry-serialization decision.
  - Scoping a later A2 implementation lane after ratification.
  - Checking which serialization shapes are selected, rejected, or reserved, and the triggers that reopen the fork.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md
  - orca-harness/data_lake/lake_touchpoint_inventory_v0.json
stale_if:
  - The owner ratifies, modifies, or rejects this ADR (the ratification block below then governs).
  - Any revisit trigger below fires.
  - The AR implementation, storage, or raw-admission contract changes the entry/body or key boundary.
```

## Status

`A2_ADR_AWAITING_RATIFICATION_V0`.

This record is a decision request. It is not implementation authorization,
backend/engine selection (Gate 2 trigger T3 governs any backend ADR),
retention/erasure semantics (Gate 2 claim ceiling governs), Manifest v2
authoring, migration authority, validation, readiness, or a Bronze full-GT
claim. On ratification, contract fold-in is a separate step carrying its own
`direction_change_propagation` receipts, mirroring the Gate 1/Gate 2 pattern.

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom A2 pack (AR implementation + storage + raw-admission contracts, Gate 1 ADR, A1 inventory record with fork tags, catalog.py entry mechanics, adjudicated cross-vendor consultation)
  edit_permission: docs-write
  target_scope: A2 decision-request ADR authoring; no runtime or contract edits.
  dirty_state_checked: yes (fresh branch off origin/main @ 5b2e1db5)
  blocked_if_missing: none
```

## Decision In One Screen

```text
Selected (pending ratification): A2-F2 — the manifest-equivalent packet
index — with one sharpening: the durable canonical object is the VERSIONED
ENTRY SCHEMA PLUS ITS DETERMINISTIC DERIVATION RULE, never any materialized
index row. Raw packet manifests stay frozen exactly as sealed. Materialized
catalog/index bytes remain generated, rebuildable, non-authoritative read
state produced by the pinned serializer. Manifest v2 (A2-F1) is rejected for
now and reserved behind named revisit triggers. Hybrid-forever (A2-F3) is
rejected as a destination; its compatibility half already exists as the
ratified blocker-2 legacy-readable direction and stays a bridge, not a home.
A separate AR member file inside packets (novel A2-F4) is rejected for
split-brain risk. The generated attachment_record_id stays a cache/query
locator and is never promoted to canonical identity.
```

Why this wins: it ratifies the shape two Silver consumer proofs and
PROOF-05/06 already exercise, requires zero migration of write-once history,
concentrates all change in the one layer that is rebuildable by design, and
keeps every escape ramp open — the schema can later be embedded in a Manifest
v2 for new packets, or an engine can sit under the rebuildable index as an
optimization, without touching sealed packets.

## Option Ledger (adjudicated)

| Option | Shape | Disposition | Why |
| --- | --- | --- | --- |
| A2-F1 Manifest v2 | Promote the packet manifest schema to carry the entry directly. | **Rejected for now; reserved** behind revisit triggers T-A2-2/T-A2-3. | Touches all 32 writer surfaces in lockstep; the old-format pile never shrinks (write-once), forcing permanent dual-read or a warehouse-scale replay; every future entry tweak becomes another version branch inside raw truth. |
| A2-F2 Packet index (schema + derivation rule canonical) | Raw manifests frozen; durable thing = pinned entry schema + deterministic derivation rule; materialized rows stay generated/rebuildable/non-authoritative. | **Selected as default** | Matches proven reality (catalog physicalization `manifest_equivalent_entry_over_raw_packet_body_v0`); zero day-one migration; blast radius is the 8 `packet_index` call sites; scaling pain (rebuild cost) lands on the disposable layer with a doctrine-sanctioned engine ramp. |
| A2-F3 Hybrid dual-read/replay | Legacy fields + entries + replays coexist indefinitely. | Rejected as a destination | Worst scaling law: version branches accumulate at every consumer, paid by people forever. Its compatibility half already exists as the ratified blocker-2 direction and remains a bridge only. |
| A2-F4 (novel, from consultation) Separate AR member file inside new packets | Entry materialized as a packet member beside the manifest. | Rejected | Split-brain risk between manifest and AR member; near-F1 writer blast radius without F1's single-slip clarity; old packets still need derivation anyway. |

## Required Outputs (bound if ratified)

1. **Canonical object.** The durable, canonical A2 artifact is the versioned
   `AttachmentRecordEntry` schema plus its deterministic derivation rule from
   committed packet material. No materialized row, file, or index is ever the
   canonical form; every materialization is regenerable output of the pinned
   serializer.
2. **Version pins.** Every serialized entry carries
   `attachment_record_schema_version`, `entry_serialization_version`,
   `derivation_rule_version`, `attachment_record_physicalization`, plus the
   raw replay pins already bound by the AR implementation contract
   (`raw_packet_manifest_version`, obligation-contract version).
3. **Canonical bytes.** UTF-8 JSON with sorted keys, fixed separators,
   explicit absent-field policy, newline termination — no object-ordering,
   path-walk, or filesystem-order leakage (the existing byte-identical
   rebuild proof is the enforcement).
4. **Centralized dispatch.** Version branching lives in one entry
   reader/serializer, never in downstream consumers — the anti-F3 guardrail.
   Consumers request an entry schema version; the reader dispatches by
   manifest version + derivation-rule version internally.
5. **By-key derivation acceptance check (future implementation lane).** A
   public by-key reader must be able to derive the canonical entry for a
   committed packet with all indexes deleted (shard recompute -> manifest ->
   derivation rule). This is an acceptance check the A2 implementation lane
   must prove, not a claim about today's helpers (today's public surface
   requires a current generated catalog and refuses stale reads).
6. **Identity boundary.** The generated `attachment_record_id` (hash-derived)
   remains a cache/query locator only. The canonical address is
   `packet_id` + packet-scoped file/attachment key + packet-relative body ref
   + `body_sha256`/`hash_basis` — addressing handles per the raw-admission
   key grammar; no content-derived identity, no dedupe meaning.
7. **Deprecation without mutation.** Sealed packets are never rewritten. Old
   derivation rules are frozen and normalized to the current internal shape
   by the central reader; a packet that cannot be safely mapped is
   held/refused/replayed under a separate replay decision, never silently
   coerced.
8. **Day-one migration answer.** Nothing changes on ratification day:
   existing packets untouched, existing generated rows remain transitional
   materializations, and the public read surface
   (`source_surface_catalog_rows` / `load_attachment_record_body`) keeps its
   signature while its internals move under the pinned serializer during the
   later authorized implementation lane.

## Named Residuals (accepted if ratified)

- **Full rebuild stays a scaling tax.** Rebuild is O(all manifests); at
  millions of packets it becomes a first-class operational cost. Upgrade
  ramp: incremental rebuild machinery and/or an engine under the rebuildable
  index — both later, separately gated (any backend ADR fires Gate 2 T3).
- **A deterministic bug reproduces everywhere.** Byte-identical rebuilds can
  reproduce the same wrong row lake-wide; the derivation rule's tests, not
  determinism alone, carry correctness.
- **"Index is truth" erosion pressure.** As rebuilds get expensive, pressure
  to trust stale rows grows; the stale-read refusal and reads-survive-index-
  loss proofs are the standing fence and must not be weakened.
- **Version history never disappears.** Old manifest-version dispatch rules
  are maintained (frozen) or retired only via explicit replay into new packet
  material.

## Revisit Triggers (any one reopens the fork)

- **T-A2-1 rebuild cost.** Measured rebuild cost becomes operationally
  unacceptable even with shard-parallel/incremental rebuilds, while by-key
  derivation is insufficient for real consumers -> reopen toward F1 for new
  packets.
- **T-A2-2 writer-surface collapse.** The raw writer surface collapses to one
  stable packet-assembly boundary, or another accepted change already forces
  a manifest schema rev across the same writers -> F1's marginal cost drops;
  re-compare.
- **T-A2-3 independent-reader requirement.** External readers must enumerate
  entries from packet material alone without project generator code -> F1/F4
  become attractive; re-compare.

## Consultation Provenance And Adjudication

- `consulted_by: GPT-5.5 Pro` (operator-couriered, cross-vendor,
  no-repo with attached source files), 2026-07-02. Decision input only.
- Home-model adjudication (commissioning CA, Anthropic Claude Fable 5):
  ACCEPTED the F2 recommendation and its sharpening (schema + derivation rule
  as the canonical object), the `attachment_record_id`-stays-locator
  boundary, the F4 evaluation, the versioning/deprecation design, the
  day-one migration answer, the flip evidence (folded above as revisit
  triggers), and the residuals. MODIFIED one item: the zero-index by-key
  entry reader is bound as a future implementation acceptance check, not a
  present-tense capability claim. REJECTED nothing.
- The consultation return is preserved in the lane PR for audit; this ADR is
  the adjudicated record.

## Owner Ratification

```yaml
a2_ratification:
  decision: pending
  ratified_by:
  date:
  modifications:
```

## Non-Claims

- Not implementation authorization; the A2 implementation lane (pinned
  serializer, dispatch reader, by-key derivation proof) needs its own
  scoping route and owner authorization.
- Not backend, engine, object-store, database, or hybrid selection; any
  backend ADR fires Gate 2 trigger T3 first.
- Not retention, lawful-erasure, or WORM posture (Gate 2's ratified deferral
  and claim ceiling govern).
- Not Manifest v2 authoring, migration, replay execution, or schema
  finalization beyond the entry-serialization boundary above.
- Not validation, readiness, third-proof authorization, or Bronze full GT.
