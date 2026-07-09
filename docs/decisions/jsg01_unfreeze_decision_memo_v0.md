# JSG-01 Unfreeze Decision Memo v0 (slice D — recommends; the owner unfreezes)

```yaml
retrieval_header_version: 1
artifact_role: Decision memo (prep for the owner's dated unfreeze act; not the act)
scope: >
  Line-by-line evaluation of the frozen conductor's JSG-01 row preconditions
  against built, committed, reviewed machinery and the first real case packet,
  plus the one open wording choice (D2 consumption) and the exact dated-decision
  + propagation shape the unfreeze act needs. This memo recommends; JSG-01 stays
  FROZEN until the owner's dated act amends the conductor row inside that act.
use_when:
  - Deciding whether (and how) to perform the JSG-01 unfreeze act.
  - Checking which conductor-row preconditions are satisfied, with evidence.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md  # the FROZEN conductor; JSG-01 row — read, never edit outside the unfreeze act
  - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md  # ratifications incl. the binding contract (2026-06-12)
  - forseti-harness/cases/product_learning/jsg01_binding_assembly_proof_v0/README.md # the slice-C proof packet record
stale_if:
  - The owner performs the unfreeze (this memo is consumed; the dated decision record supersedes it).
  - The Beauty Pie org-motion packet lands and is swapped into the proof case (refresh the evidence rows).
  - D2 is built, or the conductor row is otherwise amended.
```

**Status:** RECOMMENDS_UNFREEZE (option b below). Advisory; mints nothing;
authorizes nothing. The unfreeze is the owner's dated act.

## The conductor row's "until" clause, line by line

The frozen JSG-01 row holds `indeterminate_until_authored` *in practice* "until
the `EvidenceUnit` binding + D2 are built and a case packet carries the derived
fields + a valid `FinalizationReceipt` (the SP-5 finalizer half is already
built)". Each named element:

| # | Conductor precondition | State | Evidence (paths / commits / observed output) |
| --- | --- | --- | --- |
| 1 | SP-1/2/3/6 field schema ratified | **DONE (pre-existing)** | boundary doc, "JSG-01 source-side field schema RATIFIED" + SP-6 D-source amendment |
| 2 | Field derivers built | **DONE (pre-existing)** | `orca-harness/ecr/` (pure derivers; committed; tested) |
| 3 | SP-5 finalizer | **DONE — both halves** | model + validate-only consumer `schemas/finalization_models.py` (`a37f896`, 23 tests); producer acting half `runners/run_finalization_receipt.py` (`aeedae9`, 16 tests, cross-vendor reviewed + adjudicated) |
| 4 | The `EvidenceUnit` binding | **DONE — ratified + built** | contract owner-ratified 2026-06-12 (boundary doc amendment, commit `15b2954`); code `orca-harness/evidence_binding/` (`147e9cf`+`9f4fa93`, 17 tests, cross-vendor reviewed + adjudicated `231299a`); full suite observed `712 passed, 1 skipped` |
| 5 | A case packet carrying the derived fields + a valid `FinalizationReceipt` | **DONE — first real packet** | `cases/product_learning/jsg01_binding_assembly_proof_v0/` (`c3a44b9`, `22fe279`): real pre-cutoff archive packet `01KTM9QS8RJJAYJVD3A3C784HW`; receipt `01KTW48P5PW4JJQG7NBG6G6DBP`; composition observed 2026-06-12 |
| 6 | **D2** | **NOT built (owner-reserved)** | the one remaining named element — the wording choice below |

## What the subpredicates actually did on the real packet (observed 2026-06-12)

| JSG-01 subpredicate | Evaluation | Clears? |
| --- | --- | --- |
| SP-1 `source_identity_state` | `resolved` | yes |
| SP-2 `inspectability_state` (bound slice) | `inspectable_verifiable` | yes |
| SP-3 carried `cutoff_posture` (bound slice) | `pre_cutoff` | yes |
| SP-6 `source_visibility_posture` | `archive_only` | yes (decision-C grade) |
| Finalization provenance + final value | CLEARED; `final_pre_decision_status = verified_pre_decision` | yes (provenance; the value check is the conductor's own SP-4-side read) |

Every subpredicate evaluated **determinately** — none returned
`indeterminate_until_authored`. On this packet nothing even landed on a
residual: SP-6 cleared outright because the packet is archive-only.

## What lands on residuals (the honest general statement)

Absent D2, a packet holding **both** a pre-cutoff archive **and** a current
capture lands on `RESIDUAL_COMPARISON_NOT_RECORDED` for SP-6 — determinate,
named, **does not clear**. Archive-only packets (like the proof packet, and
like the queued Beauty Pie org-motion archive capture) clear via
`archive_only`. This is exactly the ratified coverage note: core/honest now,
corroborated tier deferred behind D2.

## The one wording choice the unfreeze act must make (D2 consumption)

The frozen row's text names D2 inside its "until" clause; decision C (later)
made SP-6 determinately evaluable without it. The unfreeze act must state which
reading it consumes:

- **(a) D2 stays a named blocker** — the unfreeze waits until D2 is built.
  Cost: blocks the gate on a capability that only adds the corroborated *tier*,
  while every subpredicate already evaluates determinately today.
- **(b) Record that decision-C's determinate residual behavior is acceptable
  for this unfreeze boundary** — the unfreeze proceeds; archive+current cases
  simply cannot clear SP-6 until D2 exists (they residualize, visibly).
  **RECOMMENDED.** Rationale: the gate's mechanical contract (Seam 1) needs
  determinate owner-field evaluation, which now exists end-to-end on a real
  packet; D2 is additive coverage, not evaluability; and the failure mode of
  (b) is conservative (residuals block clearing — they never fake a pass).

## Caveats the act should carry (named, not hidden)

1. **Judge-family placeholder:** the proof receipt records
   `judge_model_family: unassigned_pending_run_authorization` (no judge lane is
   assigned; owner-couriered). The consumer therefore clears only when
   evaluated at that recorded family; the first authorized run must record a
   correction receipt (`--supersedes 01KTW48P5PW4JJQG7NBG6G6DBP`) carrying the
   real judge family. The unfreeze act does NOT need to resolve this — it is a
   per-run input, and the append-only correction path is the designed
   mechanism.
2. **The proof case is not a judged case.** It proves machinery assembly at
   product-learning grade. Unfreezing makes JSG-01 *evaluable*, it clears no
   case, authorizes no run, and lifts no claim tier (evidence ladder Row 1 +
   claim-defense doctrine cap every externally-shaped sentence).
3. **Beauty Pie swap pending:** when the Phase-4 org-motion packet lands, swap
   it into the proof case per the commission fallback record and re-derive.

## The exact shape of the unfreeze act (when the owner says the word)

A dated decision record (new file under `docs/decisions/`, e.g.
`jsg01_unfreeze_decision_v0.md`) that: (1) states the owner's dated unfreeze
decision and the D2-consumption choice (a or b); (2) amends the conductor's
JSG-01 row — the ONLY context in which that frozen row may be edited — from
"JSG-01 stays FROZEN and clears no case" to its unfrozen evaluable state,
citing this memo's evidence table; (3) carries the inline
`direction_change_propagation` receipt (trigger: `architecture_doctrine`,
related: `lifecycle_boundary`) with downstream surfaces checked (ECR submap,
gap map, boundary doc, evidence ladder routing); and (4) restates the
non-claims: not case clearance, not run authorization, not validation, not
judgment-quality evidence, claim caps unchanged.

## Non-claims

This memo recommends and prepares; it decides nothing. Not the unfreeze, not a
conductor edit, not validation, readiness, case clearance, run authorization,
or judgment-quality evidence; capped at product-learning. JSG-01 stays FROZEN
until the owner's dated act.
