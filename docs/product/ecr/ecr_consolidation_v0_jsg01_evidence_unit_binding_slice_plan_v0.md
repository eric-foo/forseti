# ECR Consolidation v0 — JSG-01-Scoped EvidenceUnit Binding Slice Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: >
  Bounded slice plan for the minimal composition object that binds, by key
  (reference-never-merge), exactly what the JSG-01 predicate reads — the four
  derived source-side postures (SP-1/2/3/6) and the current FinalizationReceipt
  read — onto one case-packet evidence unit. Advisory design; recommends but
  ratifies nothing; build gated behind owner ratification.
status: PROPOSED_ARCHITECTURE_ROUTING_OBJECT — advisory, non-executing, POST delegated cross-vendor review-and-patch (adjudicated 2026-06-12: all reviewer changes kept), PRE owner ratification.
use_when:
  - Preparing the owner ratification of the JSG-01-scoped EvidenceUnit binding slice.
  - Checking what the binding composition decides vs what stays reserved (full EU architecture, canonical name).
authority_boundary: retrieval_only
gate_posture: JSG-01 stays FROZEN. This plan does not bind, ratify, build, or unfreeze anything.
relates_to:
  conductor_predicate: docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md  # JSG-01 row (:209) — read, never edit
  ratified_field_schema: docs/product/foundation/core_spine_v0_data_and_cleaning_spine_boundary_v0.md  # SP-1/2/3/6 ratification + decisions B/C; reserved decisions
  ecr_frame: docs/product/ecr/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md  # INV-1..5, three-mode binding rule (inherited verbatim)
  sp5_contract: docs/research/judgment-spine/sp5_finalization_receipt_spec_v0.md  # the receipt + validate-only consumer contract
  spine_submap: docs/workflows/ecr_spine_submap_v0.md  # cross-kind invariants 1-5 (orientation)
built_inputs: >
  ECR derivers: orca-harness/ecr/deriver.py (SP-1/2/3/6, pure, bind no EvidenceUnit).
  SP-5 model + validate-only consumer: orca-harness/schemas/finalization_models.py (committed a37f896).
  SP-5 producer (acting half): orca-harness/runners/run_finalization_receipt.py (built under the same
  commission; review/adjudication state must be checked in that lane, not inferred here).
  EvidenceUnit: orca-harness/schemas/case_models.py:53-73 (UNCHANGED by this slice).
branch_or_commit: ecr-sp3-timing-deriver-slice1 (re-verify citations at ratification time).
stale_if:
  - The conductor's JSG-01 row, the ratified SP-1/2/3/6 schema, decision B/C, or the SP-5 contract changes.
  - The owner ratifies, amends, or declines this binding slice (then this plan is consumed or superseded).
  - The owner settles the reserved full ECR/Evidence Unit field architecture or canonical object name.
```

- **Status:** advisory design; **non-executing**. Recommends the binding composition
  for owner ratification. Designs the contract; the implementation (models +
  composer + tests) is post-ratification under the same bounded commission.
- **Why this slice:** for the binding surface, the conductor's JSG-01 row is
  `indeterminate_until_authored` *in practice* because the derivers, the SP-5
  model + consumer, and (now) the SP-5 producer exist, but **no composition object
  binds their outputs onto a case packet's evidence unit**, so no case packet can
  carry the derived fields + a valid `FinalizationReceipt`. This slice is that
  missing composition object — and nothing else. It is **not** the complete
  unfreeze ledger: the frozen conductor row still names **D2** as deferred, while
  the ratified boundary note says SP-6 can evaluate determinately and may
  residualize without D2. Owner ratification / unfreeze routing must reconcile
  that wording explicitly before anyone claims "only the owner's unfreeze word
  remains."
- **Frame inheritance:** uses the ratified ECR frame verbatim (INV-1..5; M1/M2/M3
  binding modes; D3 upstream-owned/carried; D4 bind-real-fields-coin-nothing) and
  the submap's cross-kind invariants (reference-never-merge; one-record-per-kind;
  carry-or-residualize; re-derive-not-migrate; frozen conductor). It instantiates
  them one level up — at the composition grain — and redesigns none of them.

---

## The scope fence: exactly what JSG-01 reads

The binding composes **five reads and no more** (conductor JSG-01 row, against the
ratified schema):

| # | Subpredicate | Source record (own kind, own grain) | JSG-01-relevant read |
| --- | --- | --- | --- |
| 1 | SP-1 source identity | `EcrIdentityPosture` (per-packet) | `state ∈ {resolved, family_only}` |
| 2 | SP-2 inspectability | `EcrInspectabilityPosture` (per-slice) | bound slice's `state == inspectable_verifiable` |
| 3 | SP-3 timing/cutoff | `EcrTimingPosture` (per-slice; M1-carried `cutoff_posture`) | bound slice's `carried_cutoff_posture == pre_cutoff` |
| 4 | SP-6 source visibility | `EcrSourceVisibilityPosture` (per-packet) | decision-C grade (`clears` on `{archive_only, not_applicable}`) |
| 5 | finalization provenance + final value | `FinalizationReceipt` stream via the validate-only consumer | single current cross-family receipt ⇒ surfaces `final_pre_decision_status` (the conductor separately polices the *value*; SP-4 is not this slice) |

Anything beyond these five reads routes to the owner memo, never into this build.
This table is the **composer contract**, not a JSG-01 unfreeze ledger. In
particular, D2 remains a reserved surface: the composer may carry an SP-6
residual caused by absent D2, but it must not decide whether that residual is
acceptable for unfreeze or silently rewrite the frozen conductor's D2 blocker.

## The binding contract (working names; canonical name reserved)

**`Jsg01EvidenceBinding` — the durable declaration (keys only; reference-never-merge):**

| Field | Meaning |
| --- | --- |
| `evidence_id` | the case-packet `EvidenceUnit` being bound (`schemas/case_models.py:54`); the unit itself is **unchanged** |
| `packet_id` | the `SourceCapturePacket` carrying the source slice (`source_capture/models.py:161`) |
| `evidence_slice_id` | the slice within that packet whose preserved bytes carry this evidence unit's content (`source_capture/models.py:118`); resolves the per-slice grain of SP-2/SP-3 |

No posture, no receipt, no content, no derived value is stored on the binding: it
is a pure reference object. `Jsg01` in the working names marks the scope honestly;
the **canonical object name stays owner-reserved** — a later rename is cheap
because everything downstream of the keys is re-derived, not migrated.

The binding declaration is an **assembly-authored key assertion**, not a selector
over the strongest posture. Assembly must bind the `evidence_slice_id` whose
preserved bytes actually carry the evidence unit content; the composer only
checks key coherence and carries the resulting reads. It must never search for a
slice that clears SP-2/SP-3, infer content membership from posture quality, or
repair a bad binding by choosing a sibling slice.

**`compose_jsg01_evidence_record(...)` — the pure composer (M2 at composition grain):**

```text
compose_jsg01_evidence_record(
    binding: Jsg01EvidenceBinding,
    packet: SourceCapturePacket,
    receipts: list[FinalizationReceipt],
    judge_model_family: str,
) -> Jsg01EvidenceRecord
```

- **Pure derivation:** no I/O, no mutation, deterministic over its frozen inputs
  (the assembly runner owns file reads — slice C).
- **Key guards (block, don't repair):** `packet.packet_id != binding.packet_id`,
  or `evidence_slice_id` naming no slice in the packet, raises a named
  `Jsg01BindingError`. A malformed binding is a visible block — never a residual,
  never silently re-keyed. A low-quality or non-clearing bound slice is still
  carried as the bound read; the composer does not promote a better sibling.
- **Posture reads (carry verbatim):** calls the four built derivers fresh
  (`ecr/deriver.py`) — *re-derive, never migrate*. Carries the per-packet SP-1 and
  SP-6 postures, and the **full per-slice SP-2/SP-3 vectors** with
  `evidence_slice_id` as the selector for the JSG-01-relevant row. Carrying the
  full vectors is the no-hide audit surface (a sibling slice's failing posture
  stays visible); the *read* stays exactly the bound row. Considered alternative —
  bound-slice-only carry — was rejected because it lets assembly-time slice
  selection silently drop a failing sibling posture from the inspectable record.
- **Finalization read (carry the consumer's verdict verbatim):** calls
  `evaluate_finalization_provenance(evidence_id, receipts, judge_model_family)`
  (`schemas/finalization_models.py`) and carries the result as a
  `Jsg01FinalizationRead` — `result` (cleared/blocked), `reason`,
  `final_pre_decision_status` (populated only on cleared; **copied, never
  authored**), `current_receipt_id`. A missing/invalid/ambiguous receipt set is
  the consumer's BLOCKED verdict carried verbatim — an honest named state, not an
  invention and not a repair. `judge_model_family` flows in from the run context;
  the composer never supplies or defaults it.
- **NO aggregate verdict.** `Jsg01EvidenceRecord` carries the five reads, each as
  its own sub-record at its own grain, keyed back to its source
  (`packet_id`/`slice_id`/`evidence_id`/`receipt_id`). Combining subpredicates
  into cleared/not-cleared is the **frozen conductor's** job; the record stores no
  source-side verdict field, mirroring the I1 composition-test discipline
  (`tests/unit/test_ecr_source_side_composition.py`).

**Module home:** a new sibling package `orca-harness/evidence_binding/`
(`models.py` + `composer.py` + tests). Deliberately **not** inside `ecr/` — every
`ecr/` docstring's "binds no `EvidenceUnit`" disclaimer stays true; the spine
layers stay linked-by-key, never collapsed.

## Case-carried layout (assembly convention — low lock-in, exercised in slice C)

- `cases/<grade>/<case_id>/evidence/finalization_receipts.yaml` — the append-only
  receipts stream (the SP-5 producer's `--receipts-file` target). **Durable**:
  receipts are real records of acts, never re-derived.
- `cases/<grade>/<case_id>/evidence/jsg01_binding_<evidence_id>.yaml` — the
  binding declaration. **Durable**: three keys, mirroring the one-file-per-unit
  `evidence/eNNN.yaml` convention.
- A materialized `Jsg01EvidenceRecord` snapshot MAY be written beside them for
  inspection, wrapped in provenance (packet manifest hash, deriver module,
  `re_derivable: true`); its **authority is always the re-derivation** — a
  taxonomy change re-derives, never migrates the snapshot.

This layout is an assembly convention, not part of the ratified contract; it can
move without re-ratification as long as the binding keys and composer contract hold.

## Invariant check

- **INV-1 (single source-side writer):** the composer writes no source fact; absent
  inputs surface as the derivers' named residuals or the consumer's BLOCKED. ✓
- **INV-2 (receipt/derive only):** keys are declared; everything else is derived or
  consumer-validated. No new capture verb, no authored value. ✓
- **INV-3 (no persisted derived field; no migration):** postures and the composed
  record are derived/re-derivable; only the binding keys and the receipts (records
  of acts) are durable. ✓
- **INV-4 (recomputation basis upstream-owned, carried):** producer integrity
  anchors stay producer-owned, and the SP-5 `binding_hash` stays receipt-owned;
  the binding record only carries keys/reference, never re-authors either. ✓
- **INV-5 (categorical handoff, not schema import):** binds real committed fields;
  defines no producer field; `EvidenceUnit` schema untouched. ✓
- **Submap invariants:** reference-never-merge (keys, one-directional composition →
  provenance/integrity/finalization); one-record-per-kind (five reads stay five
  sub-records); carry-or-residualize (verbatim carries; named blocks); re-derive-
  not-migrate (snapshot authority = re-derivation); frozen conductor (no JSG-01
  evaluation, no conductor import, no readiness claim). ✓

## Explicitly NOT decided here (the reservation fence)

- The **full ECR/Evidence Unit field architecture** — no content fields, no SCR
  composition, no corroboration kind, no materiality, no cleaning references, no
  standing-field declarations beyond the four ratified reads.
- The **canonical object name** — `Jsg01EvidenceBinding`/`Jsg01EvidenceRecord` are
  working names scoped to this gate.
- **Content/SCR composition beyond what JSG-01 reads** — the Signal Content Record
  is not bound here at all.
- **D2** / the corroborated SP-6 tier (still deferred; SP-6 may land on residuals —
  expected and acceptable per the ratified coverage note).
- **SP-4 / the final-value policing** (the conductor's separate check) and any
  conductor edit.
- The **JSG-01 unfreeze** (the owner's dated act; slice D only prepares the memo).

## Build steps (post-ratification only)

1. `evidence_binding/models.py`: `Jsg01EvidenceBinding`, `Jsg01FinalizationRead`,
   `Jsg01EvidenceRecord` (StrictModel; stored-clears-style validators where a
   stored field mirrors a derived condition; YAML round-trip under `extra="forbid"`).
2. `evidence_binding/composer.py`: `compose_jsg01_evidence_record` + `Jsg01BindingError`.
3. Tests (harness pattern): key-guard blocks; grain alignment (bound-slice selection
   over full vectors); no selector laundering (a failing bound slice remains the
   bound read even when a sibling slice clears, and a clearing bound slice does
   not hide failing siblings in the carried vector); verbatim carry (postures
   equal the derivers' direct output; finalization read equals the consumer's
   verdict); blocked-carry (no receipt ⇒ BLOCKED carried, nothing authored);
   purity/determinism; round-trip; **no aggregate verdict field exists**.
4. Cross-family code review per the established slice convention before landing.

Validation gates: full pytest suite green; `test_no_llm_imports` untouched;
persistence claims verified by fresh read.

## What the cross-family review must attack

1. **Scope-fence exactness** — does the binding read *exactly* the five JSG-01
   reads: nothing extra (a reservation breach smuggling EU architecture) and
   nothing missing (a gap leaving the conductor blind)? Check against the
   conductor-row excerpt in the bundle.
2. **Grain correctness** — is `evidence_slice_id` the right resolution of the
   per-slice SP-2/SP-3 grain, and is full-vector carry + bound-row selection sound
   for multi-slice packets (vs the rejected bound-slice-only alternative)? Can
   assembly-time slice selection hide a failing posture anywhere?
3. **Verbatim-carry honesty** — any path where the composer authors, defaults,
   repairs, or re-derives differently from the owning deriver/consumer? Any
   aggregate verdict smuggled in (a `clears_all`-shaped field)?
4. **Reservation fence** — any decision in this plan that actually belongs to the
   reserved full-EU-architecture / canonical-name / D2 / conductor surfaces?
5. **Durable-vs-derived split** — is binding-keys+receipts-durable /
   everything-else-derived the right lock-in minimum? Does the materialized
   snapshot's re-derivation authority hold?
6. **Citations resolve** — spot-check the cited models/derivers/consumer lines
   against the bundled source.
7. **Cross-family independence** — run by a different vendor than this plan's author.

## Ratification shape (the owner act this plan stops for)

After cross-family review + home-model adjudication, this slice **STOPS** for owner
ratification: a dated amendment to
`docs/product/foundation/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
(same shape as the SP-1/2/3+SP-6 ratification records — design basis with SHA256
pins, owner decisions, reserved-list restated) carrying its own inline
`direction_change_propagation` receipt (trigger: `architecture_doctrine`, related:
`lifecycle_boundary`). That owner act must also state how the D2 wording in the
frozen conductor row is consumed: either D2 remains a named blocker, or the owner
explicitly records that the existing SP-6 residual/does-not-clear behavior is
determinately evaluable for this unfreeze boundary. Build starts only after the
owner's word.

## Non-claims

Advisory architecture/design only. Not implementation, not validation, not
ratification, not a JSG-01 unfreeze, not the full ECR/Evidence Unit field
architecture, not the canonical object name, not D2, not SP-4/value policing, not
a conductor change, and not judgment-quality evidence. Building everything this
plan describes proves machinery existence only; the evidence ladder + claim-defense
doctrine cap every externally-shaped sentence.
