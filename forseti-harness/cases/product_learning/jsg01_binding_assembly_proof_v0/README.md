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

- packet: `forseti-harness/reports/source_capture/g4_archive_validation_3/`
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
  receipt stream (written by `runners/run_finalization_receipt.py`). The
  finalization act was recorded 2026-06-12: receipt
  `01KTW48P5PW4JJQG7NBG6G6DBP`, finalizer `operator:eric_band_labeling_operator`
  (proxy-recorded by the ECR CA lane per the owner's in-thread word),
  `finalizer_model_family: human_operator`. `judge_model_family` is the
  EXPLICIT placeholder `unassigned_pending_run_authorization` — no judge model
  lane is assigned for this case yet (owner-couriered); when a run is
  authorized, record a correction receipt (`--supersedes
  01KTW48P5PW4JJQG7NBG6G6DBP`) carrying the real judge family before
  evaluation. A human finalizer is structurally cross-family from any model
  judge (AR-01 guardrail a).
- `evidence/jsg01_evidence_record_E1.yaml` — materialized composed-record
  snapshot (convenience only; **authority is re-derivation** via
  `evidence_binding.compose_jsg01_evidence_record` — re-derive, never migrate).

## Composition observed (2026-06-12; authority = re-derivation)

All five JSG-01 reads evaluated determinately over this packet via
`evidence_binding.compose_jsg01_evidence_record`: SP-1 `resolved` (clears),
SP-6 `archive_only` (clears), SP-3 bound `pre_cutoff` (clears), SP-2 bound
`inspectable_verifiable` (clears), SP-5 finalization CLEARED (single current
cross-family binding-consistent receipt, final `verified_pre_decision`) when
evaluated at the recorded judge family. Determinate evaluation is a machinery
fact, not a JSG-01 clearance: the conductor stays FROZEN and clears no case.

## Non-claims

Machinery assembly proof at product-learning grade. Not a judged case, not a
contestant-facing packet, not JSG-01 clearance, not judgment-quality evidence,
not the unfreeze (the owner's dated act), and not the Beauty Pie case packet
(swap pending). Zero-spoiler note: this proof case contains pre-cutoff archive
material only and references no sealed outcome artifact.
