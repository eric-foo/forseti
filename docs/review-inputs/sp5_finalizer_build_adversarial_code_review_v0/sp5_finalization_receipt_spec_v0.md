# SP-5 FinalizationReceipt — Behavior Spec v0

```yaml
retrieval_header_version: 1
artifact_role: Spec
scope: >
  Behavior contract (what-must-be-true) for the SP-5 finalization of evidence
  pre_decision_status: a separate FinalizationReceipt record indexed by evidence_id,
  finalized cross-family from the judge, provenance-bound, validated by a
  block-don't-repair consumer. Docs/spec only — not the build, not a harness
  finalizer, not a JSG-01 unfreeze. Product-learning grade (operator-recorded
  family attestation, not model self-cert).
use_when:
  - Scoping or authorizing the SP-5 finalizer mechanism (what the receipt must carry, who may finalize).
  - Checking what JSG-01's finalization-provenance subpredicate reads as its owner field.
  - Reviewing whether a finalization receipt is valid (cross-family, bound, complete).
authority_boundary: retrieval_only
open_next:
  - docs/decisions/ar_01_pre_decision_status_finalizer_staffing_v0.md
  - docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - docs/research/judgment-spine/judgment_spine_machinery_build_state_gap_map_v0.md
stale_if:
  - AR-01, decision B (finalizer kind), or the PreDecisionStatus enum changes.
  - The conductor's JSG-01 finalization-provenance subpredicate changes its owner-field contract.
  - An SP-5 finalizer mechanism is built (then this spec moves from contract to as-built).
```

## Status

**Spec status:** SPEC_COMPLETE_READY_FOR_SCOPING. Docs/spec only; authorizes no build.

Frozen input basis (settled; not re-opened here): A1 = Option 2 (separate record
indexed by (not uniquely keyed by) `evidence_id`); A3 = operator family-attestation; decision B (distinct,
cross-family, provenance-bound, out-of-band act; no same-family self-finalization);
AR-01 option C (band-labeling operator finalizes for now, under guardrails);
reuse the existing `PreDecisionStatus` enum; the harness role is a validate-only
gate (block-don't-repair).

## Required behavior

- For an evidence unit's **JSG-01 finalization-provenance subpredicate** to read
  as cleared, a **FinalizationReceipt** must exist that finalizes that unit's
  `pre_decision_status` to an allowed value, **carrying both the proposed and the
  final value and bound to** the Packing-*proposed* value (the final value MAY
  confirm or change the proposed value).
- Finalization is a **distinct, out-of-band act**: the receipt's
  `finalizer_model_family` must **differ** from the `judge_model_family`
  (cross-family; no same-family self-finalization / no testee-tester).
- A consumer of the receipt must treat a **missing or invalid** receipt as
  **not-cleared (block)**, and must **never author, default, repair, or infer**
  the final value. Finalization is performed out-of-band; the consumer validates only.
- The receipt must carry provenance sufficient to audit *who* finalized, *when*,
  *over what*, and *that the cross-family constraint held*.
- **Corrections are append-only.** A finalized value is never edited in place; a
  correction is recorded as a **new receipt**, the prior is **retained for audit**,
  and **exactly one receipt per `evidence_id` is the current finalization** (the
  consumer reads the current; zero or more-than-one ⇒ block). The mechanism that
  links a correction to its prior and designates the current receipt is **deferred
  to scoping** — until then this current-selection check is `indeterminate_until_authored`
  (like `binding_hash`).

## Non-goals

- **Not** an in-harness finalizer — no code that authors/computes the final value.
- **Not** a JSG-01 unfreeze — one prerequisite among others (still needs a case
  packet carrying the derived fields), not the unfreeze itself.
- **Not** the SP-5 build/implementation — needs separate implementation authorization.
- **Not** an `EvidenceUnit`-schema change — the receipt is a separate record; the
  unit's `pre_decision_status` / `pre_decision_basis` stay as the Packing-proposed inputs.
- **Not** a conductor change, and **not itself an advance of JSG-01** — the
  conductor already reads this subpredicate; this spec **defines the contract**
  for the owner field it reads. The subpredicate stays `indeterminate_until_authored`
  until the SP-5 mechanism is **built** and a case packet **carries** a valid
  `FinalizationReceipt`; authoring this spec does not advance JSG-01.
- **Not** a claim-tier mint — family attestation is operator-recorded
  (**product-learning** grade), not model self-cert and not judgment-quality identity provenance.

## Interfaces / contracts

`FinalizationReceipt` — a **separate record indexed by `evidence_id`** (A1 = Option 2; not a field on `EvidenceUnit`). Under append-only corrections **several receipts may exist for one `evidence_id`** over time (original + corrections), exactly one current — so `evidence_id` is the association/index, **not a uniqueness key**:

| Field | Type | Contract |
| --- | --- | --- |
| `evidence_id` | str | association/index (**not** a uniqueness key); the `EvidenceUnit` finalized |
| `finalized_over` | { `proposed_pre_decision_status`: PreDecisionStatus, `proposed_pre_decision_basis`: str } | the Packing-proposed inputs being finalized over |
| `final_pre_decision_status` | PreDecisionStatus | Judgment-owned final value (reuse existing enum) |
| `finalizer_identity` | str | decision-B provenance: who performed the act |
| `judge_model_family` | str | operator-recorded |
| `finalizer_model_family` | str | operator-recorded; **must ≠ `judge_model_family`** |
| `finalized_at` | str (UTC) | timestamp of the act |
| `binding_hash` | str | a **deterministic, reproducible** hash over a canonical serialization of (`evidence_id` + `finalized_over` proposed status & basis); exact algorithm + canonicalization fixed at scoping |

Invariants:
- receipts are **append-only / immutable** (a finalized value is never edited in place); a correction is a **new receipt**, the prior is **retained for audit**, and **exactly one receipt per `evidence_id` is current** (zero, or more than one, ⇒ the consumer blocks); the correction-linking, current-designation, and per-receipt-identity mechanism is **deferred to scoping** (like `binding_hash`), so the one-current check is `indeterminate_until_authored` until then;
- both `judge_model_family` and `finalizer_model_family` are **present**, and `finalizer_model_family != judge_model_family`;
- `final_pre_decision_status ∈ PreDecisionStatus`;
- the validating consumer is **read-only** over the record (block-don't-repair).

## Acceptance criteria (testable in principle)

- Valid **current** receipt (present and current for the unit's `evidence_id`; final status ∈ enum;
  `judge ≠ finalizer` family; `binding_hash` matches; `finalized_at` present) ⇒
  the finalization-provenance subpredicate reads cleared (subject to the other
  JSG-01 subpredicates).
- Missing receipt ⇒ block (not-cleared); nothing authored.
- `judge_model_family == finalizer_model_family`, or either absent ⇒ invalid ⇒ block.
- `binding_hash` mismatch against (`evidence_id` + proposed status/basis) ⇒ invalid ⇒ block.
- The `EvidenceUnit` record is unchanged by finalization; its proposed
  `pre_decision_status` / `pre_decision_basis` remain readable as proposed inputs.
- No code path authors/defaults/repairs `final_pre_decision_status`.
- The **current** receipt for an `evidence_id` clears (subject to the other JSG-01
  subpredicates); a non-current/superseded receipt does not; **zero or more than one**
  current receipt for an `evidence_id` ⇒ block. Prior receipts are retained (not
  deleted/overwritten). Until the current-designation mechanism is fixed at scoping,
  the current-selection check is `indeterminate_until_authored` (like `binding_hash`).

## Open questions (deferred to scoping)

- The receipt's persistence/home and serialization (the spec requires only "a
  separate record indexed by `evidence_id`").
- The exact `binding_hash` algorithm + canonicalization. Until fixed, the
  `binding_hash`-match acceptance criterion is `indeterminate_until_authored` —
  the contract requires only that the hash be **deterministic and reproducible**
  from the bound inputs; the exact form is a scoping decision.
- The correction mechanism for re-finalization (per-receipt identity, how a
  correction links to its prior, how the current receipt is designated, and where
  one-current is enforced) — the immutable + supersede + audit-retain **principle**
  is decided; the mechanism is a scoping decision.
- Whether a later refinement links the receipt to a *specific judge run id*
  rather than only `judge_model_family` — additive and non-breaking; the contract
  is family-level per A3 / decision B.

## Non-Claims

- Not validation, readiness, buyer-proof, or judgment-quality evidence; product-learning grade.
- Authorizes no build, no model run, no live execution, no JSG-01 unfreeze.
- A behavior contract; the owning sources (AR-01, core-spine boundary decision B,
  the PreDecisionStatus enum) win on any conflict.
