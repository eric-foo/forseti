# JSG-01 Binding Assembly Proof Case Packet v0 (slice C of the bounded unfreeze build)

```yaml
retrieval_header_version: 1
artifact_role: Case packet (product_learning; machinery assembly proof — NOT a judged case)
scope: >
  The first real case packet carrying everything the frozen JSG-01 predicate
  reads: one evidence unit bound (per the ratified JSG-01-scoped EvidenceUnit
  binding contract) to a real pre-cutoff archive SourceCapturePacket, plus the
  case-carried finalization receipt stream. Proves machinery assembly only;
  this is not a judged case, mints no claim tier, and does not unfreeze JSG-01.
use_when:
  - Checking which packet carried the slice-C assembly proof (commission fallback).
  - Preparing the slice-D unfreeze memo's determinate-evaluability evidence.
authority_boundary: retrieval_only
stale_if:
  - The Beauty Pie case #3 org-motion archive packet lands (then swap it in per
    the commission and re-run the assembly; this README records the swap).
```

## Which packet carried the proof (commission fallback record)

The commissioned default (Beauty Pie case #3 org-motion archive packet, Phase-4
capture) had **not landed** at assembly time — no org-motion/Greenhouse packet
exists in the tree. Per the commission's named fallback, the proof runs on an
existing **real pre-cutoff archive SourceCapturePacket**:

- packet: `orca-harness/reports/source_capture/g4_archive_validation_3/`
- packet_id: `01KTM9QS8RJJAYJVD3A3C784HW`
- captured: 2026-06-08T19:00:49Z (archive_org adapter; Direct HTTP; anti-leakage
  `select_snapshot <= cutoff`; snapshot `20241225121950` of
  `https://en.wikipedia.org/wiki/Canoo`)
- capture purpose (the packet's own `requested_decision_context`): "G4
  foundation validation: observe archive_only on a real pre-cutoff archive
  packet (lighter-CDX URL)"

When the Beauty Pie packet lands, swap it in: author its evidence unit +
binding the same way, re-run the composition, and update this record.

## Contents

- `evidence/e001.yaml` — the proof EvidenceUnit (Packing-proposed
  `pre_decision_status`; the unit's hash anchors to the packet's preserved
  archive-body file by reference).
- `evidence/jsg01_binding_E1.yaml` — the ratified three-key binding declaration
  (`evidence_id` / `packet_id` / `evidence_slice_id`): an assembly-authored key
  assertion that the `archive_snapshot_body` slice's preserved bytes carry this
  unit's content.
- `evidence/finalization_receipts.yaml` — the case-carried append-only SP-5
  receipt stream (written by `runners/run_finalization_receipt.py`; absent
  until the operator's out-of-band finalization act per AR-01).
- `evidence/jsg01_evidence_record_E1.yaml` — materialized composed-record
  snapshot (convenience only; **authority is re-derivation** via
  `evidence_binding.compose_jsg01_evidence_record` — re-derive, never migrate).

## Non-claims

Machinery assembly proof at product-learning grade. Not a judged case, not a
contestant-facing packet, not JSG-01 clearance, not judgment-quality evidence,
not the unfreeze (the owner's dated act), and not the Beauty Pie case packet
(swap pending). Zero-spoiler note: this proof case contains pre-cutoff archive
material only and references no sealed outcome artifact.
