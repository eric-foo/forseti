# Judgment-Spine Demand-Read Grading Rubric v0 (PROPOSED — the grader-side standing rules for grading a by-hand C0–C4 demand read)

```yaml
retrieval_header_version: 1
artifact_role: >
  Grader-side standing-rule record — how a revealed/outcome-aware grader grades a
  by-hand demand read (Reading) against a sealed outcome (Outcome). The deductive counterpart to the
  C3 contestant-emit contract (C3 says what a read emits; this says how a grade
  reads it). Standing rules entailed by adopted doctrine, not an empirical
  distillation. Binds no row, runs nothing, edits no other live doc.
scope: >
  The standing grading rules for a single backtest demand read: which axes a grade
  uses, which axes the sealed outcome may legitimately touch, and the two-axis
  gradeability split that makes the persistence verdict evidence-basis-graded,
  not hindsight-label-graded. Derived from (not amending) the C3 verdict/ceiling
  contract and the taxonomy Calling Sequence. Backtest-scoped (owner, 2026-06-15;
  clarified 2026-06-23); the full live monitoring sequence remains out of scope.
  Also states the classifying meta-rule (deductive standing-rule vs empirical
  generalization) that decides when a graded learning needs a proof-case.
use_when:
  - Grading a by-hand C0–C4 demand read against a revealed sealed outcome.
  - Reviewing whether a grade respects the evidence-basis split (did it grade the persistence label by hindsight outcome alone — a category error).
  - Deciding whether a graded learning is a standing rule (entailed, no proof-case) or an empirical generalization (needs N≥K cases).
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md  # parent: the contestant-emit contract (durable-projection-basis rule; ceiling vocabulary + cap rule)
  - orca/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md                            # parent: the Calling Sequence (current-window transient unless durability basis -> monitor -> earn/revise durable) this rule is entailed by
  - orca/product/spines/judgment/conductor/judgment_spine_reveal_calibration_owner_contract_v0.md   # the JSG-08 reveal / tell-audit mechanics the contamination axis uses
  - orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md        # the claim-tier boundaries (product_learning vs judgment-quality) a grade may not cross on N=1
  - orca-harness/cases/product_learning/topicals_retail_expansion_2021_v0/first_demand_read_findings_v0.md  # the worked example that surfaced this rule
stale_if:
  - The Calling Sequence or the C3 durable-projection-basis criterion is amended.
  - The two-axis demand-state model (durable/transient + real/manufactured) changes.
  - The owner lifts the backtest-only scope (the persistence-verdict grade then becomes in-scope via the monitoring loop).
  - The JSG-08 reveal/calibration contract changes the contamination/tell-audit mechanics the integrity grade depends on.
```

## Status

`PROPOSED` — grader-side standing-rule record, `product_learning` tier (advisory
/ design input). It **stabilizes how a grade reads a demand read**; it binds no
row, runs no case, and **edits neither the C3 contract, the C2 contract, the
taxonomy, nor the JSG-08 reveal contract**. Authored 2026-06-15 in the demand-read
first-earned-trust lane (worktree `demand-read-first-earned-trust-slice1` off
`origin/main`), after the lane's first graded read exposed a grader category error.

These are **standing rules, not a distillation.** They were true the moment the
Calling Sequence and the C3 contract were adopted; the first graded read merely
**surfaced** where a grader had violated them. The Topicals case is the worked
example that exposed the rule, never its evidence — so the rule needs no
proof-case (see the meta-rule below).

## Input Basis (accepted)

- **Calling Sequence** (taxonomy, owner 2026-06-14; clarified 2026-06-23): a read
  opens **current-window transient unless a durability basis is already in the
  information set**; durable is a named, evidence-supported projection that demand
  will stay strong over the decision horizon.
- **C3 durable-projection-basis criterion** (C3 contract, PROPOSED): a read that
  calls **durable** without a named persistence basis fails; a read that treats
  weak/attention-only input as transient demand also fails.
- **Two-axis demand-state model** (settled, main #78): **durable/transient**
  (persistence horizon, resolved at C3) and **real/manufactured** (integrity,
  resolved upstream at C1 + C2). "Hollow" retired.
- **JSG-08 reveal/tell-audit** (reveal-calibration owner contract): contamination
  is outcome-**use**, not recognition; an outcome-aware grader runs the tell-audit
  against the sealed outcome.
- **Owner scope** (2026-06-15; clarified 2026-06-23): this rubric governs
  **single backtest reads only**; it grades the information-set basis and does not
  claim the full live monitoring sequence is exercised.

## The Standing Rule (load-bearing)

**A single backtest read's persistence verdict is graded against the evidence in
its information set, not against the realized outcome label alone.** The chain is
deductive:

1. Durable is a forward-looking demand call: strong real demand with a named
   evidence-supported basis for projected persistence over the decision horizon.
2. Transient is also strong demand: real current-window demand whose durability is
   not called, or whose evidence supports decay.
3. Therefore a read that calls **durable** without naming a persistence basis
   fails, and a read that labels weak/attention-only input **transient demand**
   fails.
4. Therefore a later durable outcome does not by itself make a compliant
   transient call wrong; it may show what the absent live monitor would have
   upgraded.
5. Therefore outcome use is limited to the named driver/projection basis,
   contamination/tell-audit, and later evidence that directly bears on the read's
   stated counterfactual.

Grading `transient` against a `durable` outcome by label match alone is a
**category error**. The grader must ask whether the packet contained a durability
basis the read missed, or whether the outcome merely reflects a later monitoring
upgrade the single read did not have.

## The Two-Axis Gradeability Split

The two verdict axes have **opposite** gradeability at t=0:

| Axis | Resolved | t=0 outcome-gradeable? |
| --- | --- | --- |
| **real / manufactured** (integrity) | upstream (C1 + C2) | **Yes** — to the extent the manufactured *marks* (astroturf, engagement anomalies) are in the captured ≤cutoff evidence. A wrong "real" call is a real failure. |
| **durable / transient** (persistence horizon) | C3 | **Partly.** The verdict is graded against the information-set basis and reasoning trace, not hindsight label alone. Durable requires a named projection basis; transient is compliant when strong current-window demand lacks that basis or evidence supports decay. |

## What the Sealed Outcome May and May Not Grade

- **MAY grade (legitimate outcome use):** **C4 / driver-validation** (did the
  counterfactual name the real driver the outcome later confirmed), the named
  durability/decay basis when the read made one, and **contamination / JSG-08
  tell-audit** (did recognition leak into the call).
- **MAY NOT grade:** a transient label against a later durable outcome by hindsight
  alone, or a durable label against later decay without examining the evidence
  basis the read actually named.
- **Graded against evidence, not outcome:** **persistence-basis faithfulness**,
  **action-appropriateness** (ceiling obeys the floor/ceiling cap on the packet's
  evidence), and **evidence-defensibility** (no *in-packet* lift signal missed).

## The Five Grading Axes

| # | Axis | Graded against | Pass condition |
| --- | --- | --- | --- |
| 1 | **Persistence-basis faithfulness** | evidence only | Called **durable** only with a named persistence-projection basis in the packet; called **transient** when demand was strong current-window but no durable basis was present or evidence supported decay. Weak/attention-only input was not labeled transient demand. *Hindsight outcome-label match is not part of this axis.* |
| 2 | **Action-appropriateness** | evidence only | The action ceiling is right on the packet's evidence under the floor/ceiling cap rule (≥2 independent converging origins for a material verb; single origin → hold/low-commitment; engagement-only cannot carry Commit-grade). Correct **even if the bolder move later won**, when the read lacked the information that justified it. |
| 3 | **C4 / driver-validation** | **outcome** (legitimate) | C4 named the *real* driver the outcome later confirmed. This is where the outcome can audit foresight and whether the named durability/decay basis was directionally meaningful. |
| 4 | **Contamination-resistance (JSG-08)** | **outcome** (legitimate) | Resolved every ambiguity *against* the known outcome (anti-tells); no non-packet knowledge; honest no-contamination attestation. |
| 5 | **Evidence-defensibility** | evidence only | Handled every ≤cutoff signal correctly; no missed *in-packet* lift signal. (Did it use what it had — not whether it predicted what it could not see.) |

## Scope and Limits (backtest-only)

- Governs **single t=0 backtest reads** (owner, 2026-06-15; clarified 2026-06-23).
  The **persistence verdict is gradeable against the information-set basis, not
  against hindsight labels alone**. A single backtest can say whether the read had
  enough captured evidence to call durable, or enough reason to stay transient; it
  cannot prove the full live monitoring loop that later upgrades, scales, or reduces.
- **Consequence:** a clean backtest grade is **never** evidence that the
  *sequence* — and therefore the product's upside-capture half — works. The
  backtest can show basis discipline and false-positive control; it cannot
  exercise the monitoring loop that captures upside. That ceiling travels with
  every backtest claim.

## The Classifying Meta-Rule (when a graded learning needs a proof-case)

**Deductive consistency-repair vs empirical generalization.**

- A learning **entailed by already-adopted doctrine** is a **standing rule.** It
  needs **no proof-case**; the case that surfaced it makes us *notice* it, not
  *establish* it. Demanding empirical proof for it is incoherent.
- A **contingent claim about how the method behaves across the world** is an
  **empirical generalization.** It needs **N≥K cases**; one read cannot carry it.

**Test:** *could the learning be false even if the doctrine is internally
consistent?* **No → standing rule** (this rubric's core; entailed by the Calling
Sequence + C3). **Yes → empirical** — e.g. method accuracy across reads; whether
high-volume first-party costly behavior should count as more than gate-*floor*;
whether the integrity axis reliably fires at t=0. Those are separate,
case-requiring goals — **not** preconditions for this rubric.

This meta-rule is **domain-agnostic epistemics**, stated here as a judgment-lane
principle. Whether it should also be encoded into a workflow-kernel reasoning
skill is a **separate, deployment-gated question** outside Orca authority (the
kernel skills are user-global installs sourced outside this repo); it is
commissioned by a prompt artifact, not folded into this lane.

## Source-Read Ledger

- `orca/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md`
  — parent; the durable-projection-basis rule and the floor/ceiling cap rule
  axis 1–2 grade against. Status `PROPOSED`. Last checked: 2026-06-23. Reuse
  rule: reread before amending the rule.
- `orca/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md` — parent; the
  Calling Sequence the standing rule is entailed by. Status
  `PROPOSED_PENDING_OWNER_ADJUDICATION`. Last checked: 2026-06-23. Reuse rule:
  reread; not yet owner-adjudicated as operative.
- `orca/product/spines/judgment/conductor/judgment_spine_reveal_calibration_owner_contract_v0.md`
  — the JSG-08 reveal/tell-audit mechanics axis 4 depends on. Reread-required.
- `orca-harness/cases/product_learning/topicals_retail_expansion_2021_v0/first_demand_read_findings_v0.md`
  — the worked example that surfaced the rule; its grade table + bullets were
  corrected for consistency in the same change. Committed `6bb67d99`
  (pre-correction). Last checked: 2026-06-15. Reuse rule: worked example, not
  evidence for the rule.

## Claim Classification

```yaml
judgment_spine_claim_classification:
  evaluated_claim_surface: demand-read grading rubric (grader-side standing rules)
  source_quality_state: design/control artifacts only (entailed by the owner-adopted Calling Sequence + the PROPOSED C3 contract + the two-axis model + the JSG-08 reveal contract); one worked example (Topicals), which is not evidence for a deductive rule
  execution_quality_state: no new read executed; the rule is derived, not measured
  closeout_state: no_durable_evidence
  claim_cap: design input / product-learning context only
  weakest_missing_or_failed_gate: the rubric's *empirical* validity (does it produce good grades across many reads) is a separate N>=K goal it does not claim; only the deductive standing rule is asserted here
  receipt_artifact_or_gap: the standing rule's authority derives from its parents (Calling Sequence + C3); the empirical axes are explicitly deferred to future graded reads
  non_claims:
    - not validation unless separately proven
    - not readiness unless separately proven
    - not judgment-quality evidence (that needs N>=K + reveal/calibration)
    - not buyer proof
```

## Non-Claims

- Grader-side standing-rule record only; binds no row, runs no case, edits neither
  the C3 contract, the C2 contract, the taxonomy, nor the JSG-08 reveal contract.
- **Standing rules, not a distillation.** Their authority is **derived** (from the
  Calling Sequence + C3), not **evidential** (earned from N=1). The Topicals case
  is the worked example that surfaced them, never their proof.
- **Backtest-scoped.** The persistence-verdict grade is out of scope; a clean
  backtest grade is not evidence the calling sequence or the product's
  upside-capture works.
- `PROPOSED` and not yet owner-adopted as the operative grading rule. On adoption
  it owes a dated pointer via the Doctrine-Change Propagation Contract
  (`.agents/workflow-overlay/source-of-truth.md`). It changes no other live
  doctrine source, so no propagation receipt is owed now (the same-change
  correction to the Topicals findings is a consistency fix to a case record, not a
  doctrine-source edit).
- A demand-read grade is `product_learning` evidence about one read — never
  validated, decision-grade, buyer-proven, or judgment-quality.
```text
This is advisory design input only. It is not a verdict, not implementation
authority, and not proof of readiness.
```
