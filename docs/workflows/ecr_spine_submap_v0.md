# ECR Source-Side Spine Repo Submap v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow navigation artifact (ECR source-side spine repo submap)
scope: Single repo submap that orients a reader across the ECR source-side derived-record spine — the integrity postures (ECR SP-1/2/3/6) and the sibling content layer (Signal Content Record), the deriver discipline they share, and the frozen boundary to the JSG-01 conductor. Map only; not source-of-truth.
use_when:
  - Orienting to the ECR source-side spine (integrity postures or Signal Content Record) before reading or extending any derived-record code or plan.
  - Finding which owner doc owns an ECR posture, the SCR content layer, the shared deriver discipline, or a deferred surface.
  - Checking what is built vs declared-but-dormant vs frozen, without bulk-loading every ECR/SCR artifact.
authority_boundary: retrieval_only
open_next:
  - docs/product/signal_content/core_spine_v0_signal_content_record_architecture_v0.md
  - docs/product/ecr/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md
  - orca-harness/ecr/__init__.py
downstream_consumers:
  - JSG-01 conductor (UNFROZEN 2026-06-12 by the owner's dated act, docs/decisions/jsg01_unfreeze_decision_v0.md; evaluable, clears no case until an authorized run) — the reader of the records this spine produces; nothing under this map authorizes runs or clears cases.
stale_if:
  - A new derived-record kind is added beside the ECR integrity postures and the Signal Content Record.
  - The shared M1/M2/M3 carry-or-residualize discipline or the per-kind grain invariant changes in an owner doc.
  - The authored-interpretation lane (signal_family + event-core) is built (activates the dormant SCR M2 seam).
  - The owner settles the reserved final Evidence Unit field architecture, or a JSG-01 run is authorized (the unfreeze itself happened 2026-06-12).
```

> **What this is.** A retrieval-only repo submap. It tells a cold reader which owner
> source to open for an ECR source-side / Signal Content Record question, and states
> the few cross-kind invariants that have no single other home. It is the map, not
> the authority: on any conflict, the pointed-to owner source wins.
>
> **Do not use** this map as validation, readiness, ratification, a JSG-01 unfreeze,
> Evidence-Unit binding authority, the reserved final Evidence Unit field
> architecture, Cleaning, Judgment, or buyer proof.

## The Spine In One Screen

Three stacked layers over one captured source slice — **linked by key, never collapsed:**

- **Provenance** — *that a capture happened* + how to trust the bytes. `SourceCapturePacket` (`orca-harness/source_capture/`).
- **Integrity** — *can I trust the saying.* ECR postures: SP-1 identity / SP-2 inspectability / SP-3 timing-cutoff / SP-6 source-visibility (`orca-harness/ecr/`).
- **Content** — *what the signal says.* The Signal Content Record (`orca-harness/signal_content/`).

The cross-kind invariants the spine runs on (stated here for orientation only — the owner doc holds the authority):

1. **Reference, never merge.** Content references provenance (`packet_id`/`slice_id`) and integrity (ECR posture keys) **by key**, one-directional content → provenance. Linked, never collapsed: content is "what's said," integrity is "can I trust the saying." → *SCR direction brief.*
2. **One derived record per epistemic kind, composed by the Evidence Unit, never merged.** The integrity postures and the content row are siblings at their own grain; future kinds (e.g. corroboration) follow the same shape rather than sprawling. → *SCR direction brief.*
3. **Carry-supplied-or-residualize; never author from prose.** Every source-side deriver is a pure function of its frozen inputs (the packet plus caller-supplied bodies / posture-keys / authored-interpretation). Each field is carried from an input or emitted as a **named residual**; an absent input → honest residual. No deriver classifies, selects, or infers an interpretive value from packet prose (the shared M1-carry / M2-derive / M3-residual discipline). → *SCR deriver plan (Amendment v0.1); ECR frame plan.*
4. **Derived / re-derivable — re-derive, never migrate.** These are M2-style derived reads over the still-frozen raw observable, not persisted-at-capture columns; a taxonomy change is a re-derive, not a stored-column migration (inherits the capture-packet schema-evolution doctrine verbatim: read-checked `_vN`, additive enum growth, lenient-read/strict-admit). → *schema-evolution doctrine.*
5. **Foundation only — the conductor owns evaluation.** Everything here is source-side derivation feeding JSG-01 evaluation. JSG-01 was unfrozen by the owner's dated act (2026-06-12, `docs/decisions/jsg01_unfreeze_decision_v0.md`) and clears no case until a separately authorized run; the final Evidence Unit field architecture stays owner-reserved; nothing under this map authorizes runs or widens the reserved architecture. → *data/cleaning boundary doc; `.agents/workflow-overlay/safety-rules.md`.*

## Fast Route

| I need to... | Open |
| --- | --- |
| Understand the content layer's locked direction + invariants | `docs/product/signal_content/core_spine_v0_signal_content_record_architecture_v0.md` |
| Build/review the SCR deriver (carry-or-residualize, per-slice grain, the D2 event-time amendment) | `docs/product/signal_content/signal_content_record_deriver_architecture_plan_v0.md` (see **Amendment v0.1**) |
| Understand the ECR frame (the M1/M2/M3 binding rule + INV-1..5) and the SP-6 source-visibility slice | `docs/product/ecr/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md` |
| Bind SP-1 identity / SP-2 inspectability / SP-3 timing-cutoff to committed producer fields | `docs/product/ecr/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md` |
| Decide SP-6 derivation ownership + mechanical rule shape | `docs/product/judgment_spine/jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md`, `..._routing_v0.md` |
| See where the source-side fields + closed allowed-values came from (interim translator) | `docs/product/judgment_spine/jsg01_source_side_receipt_translator_v0.md` |
| Check the schema-evolution doctrine the spine inherits | `docs/product/data_capture_spine/source_capture_packet_schema_evolution_architecture_v0.md` |
| Inspect the built ECR integrity derivers (SP-1/2/3/6) + models | `orca-harness/ecr/` |
| Inspect the built Signal Content Record deriver + model | `orca-harness/signal_content/` |
| Record an out-of-band SP-5 finalization act (`FinalizationReceipt` producer) | `orca-harness/runners/run_finalization_receipt.py` (model + validate-only consumer: `orca-harness/schemas/finalization_models.py`) |
| Bind what JSG-01 reads onto one case-packet evidence unit (three-key binding + composer) | `orca-harness/evidence_binding/` (ratified contract: boundary doc → "JSG-01-scoped EvidenceUnit binding contract RATIFIED") |
| Inspect the tests | `orca-harness/tests/unit/test_ecr_*`, `orca-harness/tests/unit/test_signal_content_*`, `orca-harness/tests/unit/test_finalization_models.py`, `orca-harness/tests/unit/test_run_finalization_receipt.py` |
| Reach the upstream provenance layer (the packet this all keys to) | `docs/workflows/data_capture_spine_consolidation_map_v0.md` (capture submap) |

## Current Reality Snapshot

- **Built + committed (clean working tree; unit tests under `orca-harness/tests/unit/`):** the four ECR integrity postures — SP-1 identity, SP-2 inspectability, SP-3 timing-cutoff, SP-6 source-visibility — in `orca-harness/ecr/`, and the Signal Content Record deriver in `orca-harness/signal_content/`. Each at its own true grain; pure; binds no Evidence Unit. *Implementation reality is the code — check it there; plan docs may run ahead of or behind it. Review history lives in the owning plan docs and the commit log.*
- **Declared-but-dormant:** the SCR **authored-interpretation lane** (`signal_family` + event-core). The deriver residualizes that core today (the default) because no authored-classification input / SP-5-style finalizer exists in source. A named, typed seam — not built (the SP-6 precedent).
- **Built (SP-5 finalization, judgment-lane sibling):** the `FinalizationReceipt` model + validate-only consumer (`orca-harness/schemas/finalization_models.py`, committed `a37f896`) and the operator-driven producer recording the out-of-band act (`orca-harness/runners/run_finalization_receipt.py`; cross-vendor reviewed + adjudicated). Binds no Evidence Unit; clears no case.
- **Ratified + built (JSG-01-scoped composition layer):** the **JSG-01-scoped EvidenceUnit binding** (three-key `Jsg01EvidenceBinding` + pure no-aggregate-verdict composer; owner-ratified 2026-06-12 at the boundary doc; code in `orca-harness/evidence_binding/`, cross-vendor reviewed + adjudicated). Scoped to exactly what the JSG-01 predicate reads; the full field-by-field Evidence Unit schema stays reserved.
- **Deferred / reserved (named, not owned here):** the field-by-field Evidence Unit schema; D2; Cleaning; Judgment; run authorization. Each separately gated. (The JSG-01 unfreeze was performed by the owner's dated act, 2026-06-12.)

## Owners By Layer

- **Provenance (capture):** `docs/workflows/data_capture_spine_consolidation_map_v0.md` → `orca-harness/source_capture/`.
- **Integrity (ECR postures):** frame + SP-6 slice — `docs/product/ecr/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md`; SP-1/2/3 — `docs/product/ecr/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md`; SP-6 derivation ownership/rule — `docs/product/judgment_spine/jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md` (+ `..._routing_v0.md`); origin of the closed values — `docs/product/judgment_spine/jsg01_source_side_receipt_translator_v0.md`. Code: `orca-harness/ecr/`.
- **Content (SCR):** direction + invariants — `docs/product/signal_content/core_spine_v0_signal_content_record_architecture_v0.md`; deriver contract — `docs/product/signal_content/signal_content_record_deriver_architecture_plan_v0.md`. Code: `orca-harness/signal_content/`.
- **Shared discipline:** schema evolution — `docs/product/data_capture_spine/source_capture_packet_schema_evolution_architecture_v0.md`; data/cleaning boundary — `core_spine_v0_data_and_cleaning_spine_boundary_v0.md`.
- **Downstream consumer:** the JSG-01 conductor (unfrozen 2026-06-12; evaluable, clears no case until an authorized run) — the final Evidence Unit field architecture stays owner-reserved; boundary in `.agents/workflow-overlay/safety-rules.md`.

## Non-Claims

This map is not validation, readiness, ratification, a JSG-01 unfreeze, the reserved
final Evidence Unit field architecture, Evidence-Unit binding authority, schema
authority, Cleaning, Judgment design, buyer proof, or implementation authorization.
It restates no authority; every invariant above is owned and already recorded in the
pointed-to source.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The ECR source-side spine (integrity postures SP-1/2/3/6 plus the sibling Signal
    Content Record) now has a thin retrieval-only workflow submap as its front door:
    it states the cross-kind invariants (reference-never-merge, one-record-per-kind,
    carry-or-residualize/never-author-from-prose, re-derive-not-migrate,
    frozen-conductor) and routes each area to its owner doc.
  trigger: workflow_authority
  status: map_written_routing_entry_flagged_for_coordinator
  controlling_sources_updated:
    - docs/workflows/ecr_spine_submap_v0.md
  flagged_for_coordinator_not_edited:
    - path: docs/workflows/orca_repo_map_v0.md
      reason: "The front-door routing entry (ECR detail routes through this submap, read map first) is coordinator-owned/protected; flagged for the coordinator, not edited here."
    - path: .agents/workflow-overlay/source-loading.md
      reason: "Source-loading routing order is coordinator-owned/protected; flagged for the coordinator, not edited here."
  downstream_surfaces_checked:
    - path: docs/workflows/data_capture_spine_consolidation_map_v0.md
      note: "Sibling capture submap; this submap points to it for the provenance layer and mirrors its style. No edit required."
  non_claims:
    - "not validation"
    - "not readiness"
    - "not ratification"
    - "not a JSG-01 unfreeze"
    - "not Evidence-Unit binding or the reserved final Evidence Unit field architecture"
    - "not Cleaning or Judgment design"
    - "not implementation authorization"
```
