# Distillation — Held Lessons from the Beauty Pie #3 Pilot (prepare-only)

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: >
  Foundation capture of two recorded outcomes from the org-motion Beauty Pie #3
  judgement pilot (case beautypie_repricing_2023_v0) — L1 (scope-against-charter)
  and L2 (capture-success is not claim-support) — held as candidate distillation
  analysis. Records the outcomes durably so they survive compaction; it does NOT
  install cells, name final decision nodes, build any substrate, or pick the
  distillation folder/deck shape. Those are the deferred architecture pass.
authority_boundary: retrieval_only
use_when:
  - Running the distillation architecture pass that decides L2's decision node,
    enforcement placement, and the lessons-vs-method deck split.
  - Checking what the Beauty Pie pilot session recorded as distill-worthy and why
    it is not yet a binding cell.
open_next:
  - docs/decisions/distillation_doctrine_orca_spine_bindings_v0.md
  - docs/decisions/distillation_binding_data_capture_v0.md
  - .agents/workflow-overlay/validation-gates.md
stale_if:
  - The architecture pass settles L2's decision node / placement (this record is
    then superseded by that decision; set superseded_by).
  - L1 is recorded against the upstream incremental-planning skill (its held state
    here is then discharged).
```

## Status

**PREPARE-ONLY — HELD ANALYSIS (candidate).** This record captures two recorded
session outcomes so they are not lost. It is **not** a binding, not an installed
cell, not bound into any always-on overlay, and **names no final decision node**.
Per the Distillation §0 core, a lesson whose decision node is unsettled is *held
as analysis and re-entered when a node is named* — that is exactly this record's
state for L2; L1 has no Orca decision node at all and is held for upstream routing.

Edits no overlay rule, no doctrine, no binding, no harness. Same boundary as the
distillation index (`distillation_doctrine_orca_spine_bindings_v0.md`): a
prepare-only classification of *already-recorded* outcomes, so **no
`direction_change_propagation` receipt is owed**. No validation, readiness,
acceptance, or proof claim is made by this record.

> **UPDATE — L2 OPERATIONALIZED (this lane).** L2 is now a code-enforced cell:
> `GUARD claim-support-span-in-body` at `node:evidence-claim-binding` in
> `distillation_binding_judgment_spine_v0.md`, enforced by
> `orca-harness/evidence_binding/verifier.py` (+ `tests/unit/test_claim_support_verifier.py`).
> The L2 held analysis below is **superseded by that cell**. L1 remains held
> (upstream routing to the incremental-planning skill is still pending); this
> record stays alive for L1 until that is discharged.

## Why this exists (foundation, not paving)

The owner directive was "clear the foundation before paving": record L1 and L2
durably *now* (cheap, reversible, pre-commits no architecture), and defer the
node/placement/encode/deck decisions to a routed architecture pass. This file is
the foundation. It is the intake the architecture pass consumes.

## L1 — Scope a work-unit against its own charter before recommending

```yaml
held_lesson:
  id: L1-scope-against-charter
  outcome_class: wrong-recommendation (a scope call made before reading the
    work-unit's own governing charter)
  recorded_outcome: >
    During the pilot, an incremental-planning recommendation called the archived
    ATS / Greenhouse org-motion capture "overbuild" — before reading the case's
    own feasibility doc and batch ledger declaration, which MANDATED that capture
    (owner-signed). The recommendation was wrong; the owner caught it.
  causal_miss: missing trigger — "read the work-unit's governing charter
    (feasibility doc / ledger declaration / owning lane)" must fire BEFORE a
    scope/overbuild recommendation, not after.
  candidate_intervention: a pre-recommendation read of the unit's own charter;
    actor-carried (judgment at planning time — no deterministic boundary).
  decision_node: NONE IN ORCA. The miss happens at the planning/recommendation
    step. Orca's spine bindings carry only run-time judgment gates; none owns a
    "scoping/recommendation" node. Therefore, by NO DECISION NODE NO LESSON, this
    does not distill into an Orca binding.
  disposition: route UPSTREAM to the incremental-planning workflow-kernel skill
    (outside Orca's binding system). Honest limit: upstream may only record it,
    not enforce it.
  provenance: case beautypie_repricing_2023_v0 — feasibility doc
    (docs/research/orgmotion_beautypie_capture_feasibility_v0.md) +
    judgment_spine_backtest_batch1_ledger_declaration_v0.md mandated the ATS
    capture; the "overbuild" call preceded reading them. tier: recorded session
    outcome. date 2026-06.
  owner: owner (upstream-routing decision already made: yes, flow upstream).
  retirement_test: retire if the incremental-planning skill carries a
    charter-read trigger that fires before scope recommendations.
```

## L2 — A successful capture is not evidence until the body is verified to back the claim

```yaml
held_lesson:
  id: L2-capture-success-not-claim-support
  outcome_class: silent-wrong-input (a capture that succeeds mechanically is
    treated as evidence for a claim its body does not actually contain)
  recorded_outcome: >
    The beautypie.com/how-it-works capture succeeded cleanly (right page,
    pre-cutoff snapshot, body hash verified) but its body did NOT contain the
    membership-pricing facts the case premise leaned on (the £5 tier, £59 Plus,
    and spending-limit wording were absent from that page and the other
    captures). A clean capture was nearly read as backing a claim it did not make;
    the premise had to be reclassified as a case-stated premise instead.
  causal_miss: missing distinction — "capture succeeded" (got the bytes,
    pre-cutoff, hash-anchored) is NOT "the body backs claim X". Two different
    questions; the second was skipped.
  candidate_intervention (ENCODE-FIRST): require every source-to-claim binding to
    cite the exact body span that supports the claim, and a deterministic checker
    that confirms that quoted span is present in the captured (hash-anchored)
    body. This is mechanically checkable, so per ENFORCEMENT PLACEMENT /
    CLASSIFY-SUBSTRATE-FIRST it belongs in a substrate (fixture schema + checker),
    not (only) a resident model instruction.
  decision_node: the CLAIM-BINDING step (not the grab). Verified site (this
    session): the owner-ratified evidence_binding layer — Jsg01EvidenceBinding in
    orca-harness/evidence_binding/models.py, where an EvidenceUnit is bound to the
    slice whose preserved bytes carry its content. NOT data-capture
    node:capture-packet-emit (a clean grab of a non-supporting page passes there).
    Exact node id (e.g. node:evidence-claim-binding) is the architecture pass's to
    name.
  placement_candidate: by EFFICIENCY RANK this is a silent/catastrophic-loss
    class; substrate-first prefers a deterministic code check over resident budget.
    CORRECTION (verified this session, supersedes this record's first draft): the
    encode does NOT land in case_models.py. Its home is the evidence_binding layer.
    Jsg01EvidenceBinding is owner-ratified "reference-never-merge: three keys, no
    content/derived value stored on it (do not relax without owner auth)", so the
    quoted supporting span must be a SEPARATE keyed claim-support assertion +
    deterministic checker, NOT a field on the binding. No verifier exists yet.
    Because this is the evidence_binding layer (a different file), L2's encode is
    DECOUPLED from the FacilitatorLedger drift in case_models.py.
  verification_pair: under-case (a source bound to a claim whose facts are absent
    from the body) -> check FAILS / binding blocked; over-edge (claim facts
    present as a quoted span in the body) -> passes.
  provenance: case beautypie_repricing_2023_v0 —
    source_provenance_notes_v0.md (E2 reclassified to case-stated premise; only
    the £10/mo wording was archive-sourced). tier: recorded session outcome.
    date 2026-06.
  owner: owner (placement is owner-gated; owner has signalled "top level" +
    "encode/auto if possible").
  retirement_test: retire if the fixture schema enforces span-in-body for every
    source-to-claim binding and the checker is shown to fire.
  operationalized: >
    SUPERSEDED by GUARD claim-support-span-in-body at node:evidence-claim-binding in
    distillation_binding_judgment_spine_v0.md, enforced by
    orca-harness/evidence_binding/verifier.py (Jsg01ClaimSupportAssertion +
    verify_claim_support) with contract test tests/unit/test_claim_support_verifier.py.
    Page-grain, atomic-claims-only, additive/optional (frozen fixtures unaffected).
```

## Deferred to the architecture pass (not decided here)

- L2's final **decision node** (capture-emit vs a fixture-construction node) and
  its **enforcement placement** (cell vs core vs code-substrate).
- The **lessons-vs-method deck split**: L1/L2 are distillation (lessons-from-loss);
  the owner's other wanted decks — "weighting evidence" and "what evidence would
  shift the decision materially" (value-of-information) — are **judgment-method**,
  a different artifact class that may already have a home (the judgment-quality
  operating-model surface). The pass decides homes; this record does not.
- The **distillation folder scope** (cross-spine home vs judgment-lane sub-area).
- The **harness-model reconciliation** (FacilitatorLedger in case_models.py): a
  SEPARATE lane (a different file from L2's evidence_binding home) — Phase-6, NOT
  coupled to L2's encode (corrected from this record's first draft).

## Other session observations (noted, NOT distilled here)

The pilot also surfaced a provenance taxonomy (captured-source / case-stated-premise
/ general-base-rate), a construction-vs-runtime schema drift, and the
firewalled-freeze recipe. They are noted for the architecture pass's intake but
are deliberately **out of scope** for this foundation capture, which the owner
scoped to L1 and L2.

## Non-claims

Prepare-only held analysis. Not a binding, not an installed cell, not bound, no
substrate built, no decision node finalized, no folder/deck created. Not
validation, readiness, acceptance, firing evidence, or proof. Placement is not
authority.
