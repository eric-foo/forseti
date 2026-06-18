# Decision: AR-01 — `pre_decision_status` Finalizer Staffing (Distinct Act, Operator-for-Now)

```yaml
retrieval_header_version: 1
artifact_role: Decision record
scope: >
  Resolves the open owner decision AR-01 — who staffs the Judgment-authority
  finalization of evidence `pre_decision_status`. Adopts the "distinct act,
  role-deferred" reframe: the finalization is a distinct, provenance-bound act
  (per the already-settled decision B); the role defaults to the band-labeling
  operator for now, with explicit triggers to promote it to a dedicated role.
use_when:
  - Designing or authorizing the SP-5 finalizer mechanism (who holds the finalization credential).
  - Checking whether AR-01 is still open (it is RESOLVED here; the packing interface and core-spine boundary docs still carry stale "undecided/reserved" entries pending propagation).
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
```

**Status:** LOCKED (owner, decided 2026-06-09).

## What AR-01 was

Recorded open in `packing_to_harness_foundation_interface_architecture_v3.md`
("What Is Intentionally Undecided", item 1): *whether the band-labeling operator
is the Judgment authority that finalizes evidence `pre_decision_status`, or
whether finalization is a distinct Judgment step (possibly a fourth named role).*
v3 bound the **authority** (Judgment) but not the **staffing**.

## Decision (owner, option C — the reframe)

The binary "operator vs 4th role" is not forced now. Separate the **act** from the
**role**:

1. **The act is fixed (per decision B, unchanged):** finalization of
   `pre_decision_status` is a **distinct, cross-family (different model family
   than the judge), provenance-bound, out-of-band act** with **no same-family
   self-finalization** (no testee-tester). This decision restates decision B by
   reference; it does not alter it.
2. **The role defaults to the band-labeling operator — for now — conditioned on:**
   - (a) the operator is provably **cross-family from the judge**; and
   - (b) finalization is performed as its **own provenance-stamped act**, not a
     rubber-stamp of the operator's own band labels.
3. **Promotion to a dedicated finalization role ("4th role") is deferred,**
   bound to the SP-5 finalizer build-design, and triggered earlier by any of:
   - the operator cannot be guaranteed cross-family from the judge for a case;
   - an observed labeling↔finalization separation-of-concerns conflict;
   - an owner policy that integrity-admission must always be its own gate.

## Why (low-lock-in)

Decision B requires a distinct **act**, not a standing distinct **role**. The
SP-5 mechanism is role-agnostic (it records an identity/time/inputs regardless of
which role performed the act), it is not being built yet, and no case packet
carries the fields yet — so forcing a new standing role now is premature
lock-in with no current payoff. Defaulting to the operator (under the two
guardrails) is the reversible starting posture; the dedicated role is created
only when a trigger above makes it necessary.

## Scope and non-claims

- Does **not** unfreeze JSG-01 — that still requires the SP-5 finalizer mechanism
  built **and** a case packet carrying the derived fields (ECR slice-2).
- Does **not** authorize building the SP-5 mechanism (deferred; needs explicit
  implementation authorization).
- Resolves the AR-01 **staffing** question only; decision B (the act constraints)
  is unchanged and referenced, not modified.
- Does **not** touch D2 (non-blocking) or any deriver (already built).
- Not validation, readiness, or judgment-quality evidence.

## direction_change_propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    AR-01 (pre_decision_status finalizer staffing) is RESOLVED via option C: the
    finalization is a distinct, cross-family, provenance-bound act (decision B,
    unchanged); the role defaults to the band-labeling operator for now under two
    guardrails (operator cross-family from the judge; finalization a separately
    provenance-stamped act), with promotion to a dedicated 4th role deferred to
    the SP-5 build-design or earlier separation-of-concerns / cross-family
    triggers. No standing 4th role is created. Owner-decided 2026-06-09.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/ar_01_pre_decision_status_finalizer_staffing_v0.md  # this record (authoritative home)
  downstream_surfaces_propagation_pending:
    - path: docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md
      what: '"What Is Intentionally Undecided" item 1 [AR-01] and the inline [AR-01] reference should be marked resolved, pointing to this record.'
      owner: harness/v0_14 (packing) lane
      status: >
        NOT done by the judgment lane. This file is currently UNTRACKED, in-flight
        concurrent-lane work; editing or committing it would disturb that lane.
        The packing lane should propagate when it next touches the file. This
        decision record is authoritative in the meantime.
  downstream_surfaces_checked:
    - docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md  # NO edit needed — decision B (the finalizer KIND) is unchanged and accurate, and the boundary does not pose AR-01 staffing as an open question
  non_claims:
    - not JSG-01 unfreeze
    - not SP-5 mechanism build authorization
    - no standing 4th role created
    - decision B unchanged (referenced, not modified)
    - not validation, readiness, or judgment-quality evidence
```
