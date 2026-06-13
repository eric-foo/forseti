# Near-Half Backtest-Learning Architecture v0 (the improving-judgment loop)

```yaml
retrieval_header_version: 1
artifact_role: PROPOSED target architecture (planning artifact; occupies the slot the far-half already cut for the near half; binds nothing, builds nothing, validates no lesson)
scope: >
  The near-half architecture: the counterparty-free loop that turns scored blind
  backtest calls into carried, validated lessons that improve the next call.
  Deliberately LEAN — it reuses batch-1 (case substrate), the step-1
  signal-reliability ledger (signal sink), and the far-half decision-memory
  (read surface), and adds exactly the two cells the far half names but does not
  own: the adversarial-postmortem protocol and the validated-lesson cell +
  promotion gate. Step 2 of 3 (signal-reliability -> architecture -> postmortem).
use_when:
  - Deciding whether to adopt, amend, or reject the near-half (backtest-learning) target.
  - Building the postmortem protocol (step 3) or the lesson-promotion gate.
  - Checking what a lesson may claim and the firewall/cherry-pick guards on carrying it.
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md
  - docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md
branch_or_commit: near-half-architecture-v0 off origin/main @ ea2c79b
depends_on:
  - The step-1 signal-reliability ledger lands on main (PR #54). This architecture references it by pointer and pins it at promotion; no first lesson/row before it is on main.
stale_if:
  - The step-1 signal-reliability ledger schema changes (re-reconcile the emit boundary).
  - The far-half decision-memory / learning-loop sections are amended (re-reconcile the read surface + emit/consume boundary).
  - batch-1's K-of-N / report-all / pre-commitment discipline changes.
  - The conductor firewall doctrine or the evidence-ladder caps change.
```

## Status

`PROPOSED` — planning artifact, product-learning tier. A **target, not a
capability claim.** Mints no claim-tier vocabulary, validates no lesson,
populates no row, promotes no signal or source-family. It occupies the slot the
far-half architecture already declared ("the adversarial step lives in the near
half"); it does not re-decide the far half.

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_near_half_architecture (step-1 ledger + far-half architecture + phase-0 spec + batch-1 + conductor firewall + evidence ladder, re-verified on origin/main; plus 3 advisory architecture-planning perspectives, owner-authorized subagents)
  edit_permission: docs-write
  target_scope:
    - docs/product/judgment_spine/near_half_backtest_learning_architecture_v0.md (new, this file only)
  dirty_state_checked: yes (fresh branch off origin/main; clean at start)
  blocked_if_missing: no
profile: standard (3 owner-authorized subagents: directional / adversarial / grounding; main planner owns synthesis)
architecture_result: TARGET_RECOMMENDED
```

## The Architecture Question

Orca has a backtest harness that *scores* blind calls but does not *learn* from
them in a carried way. The far half already named the fix and assigned it here:
"the operational loop generates learning inputs and consumes validated outputs;
it never validates its own lessons. The adversarial step lives in the near half."

**What is the smallest architecture that turns a scored blind backtest case into
a carried, validated lesson that improves the next call — without letting
hindsight launder itself into false confidence, and without reinventing what
batch-1, the step-1 ledger, and the far half already own?**

## What Already Exists (reuse; do not reinvent)

The near half is mostly *wiring three landed pieces*, not new infrastructure:

| Existing piece | What it already owns | The near half's relation |
| --- | --- | --- |
| batch-1 ledger | scored blind cases; K-of-N / report-all / pre-commitment discipline; org-motion exemplar | **case substrate** — the postmortem reads these; never re-declares cases or discipline |
| step-1 signal-reliability ledger | the firewall-clean `(signal_id, case_id)` pre-committed-use unit; the K-of-N tally; the N7 field map; product-learning cap | **signal sink** — the postmortem emits signal rows into it; never redefines the unit |
| far-half decision-memory + learning loop | the read-side projection over (lessons + reliability + resolved cases); the four learning channels; the emit/consume boundary | **read surface** — lessons flow here; never re-specs decision-memory |

So this architecture adds **exactly two cells** the far half names but does not
own: the **adversarial-postmortem protocol** and the **validated-lesson cell +
promotion gate**. Everything else is reconciliation. (This lean framing is the
grounding lane's load-bearing point, and the adversarial lane's strongest one:
"the genuinely new thing is one protocol; an architecture risks reinventing
schema three landed docs already own." Accepted — hence the pointer-heavy shape.)

## Target Architecture

### 1. The adversarial-postmortem protocol (firewall-clean by construction)

A scored blind case has two frozen halves: the sealed **pre-reveal call** (the
JSG-06 reasoning trace) and the sealed **outcome** (JSG-08 reveal). The
postmortem — run by a **de-correlated reviewer, never the call's author** —
reads both and asks one question: *what, present in the brief at seal time,
should have changed the call?*

- **Derivability bar (carried from the conductor R4/JSG-08):** a finding is
  admissible only if it traces to information **derivable from the sealed
  brief**. "The outcome shows X" is a **confirmed tell**, not a lesson — it
  routes to the conductor's `breached_quarantined` / recorded-as-data branch.
- **Lower-tier by construction:** the postmortem consumes the *revealed*
  outcome, so nothing it produces can re-score or re-rank the blind call. **The
  blind pre-reveal call stays the only judgment score** — the firewall holds.
- Output: zero or more **lesson candidates** (and signal rows; see §4).

### 2. The validated-lesson cell

```yaml
validated_lesson_cell_v0:
  lesson_id:
  decision_family:              # keys the decision-memory read; scopes applicability
  lesson_type: judgment_domain | loop_mechanics   # see §3 — only judgment_domain enters the judgment read path
  trigger_predicate:            # a FALSIFIABLE, MECHANICAL in-brief pattern (not loose prose) — "when ATS hiring in function F contracts >= X% over the cutoff window"
  prescribed_adjustment:        # what the call should have done when the predicate fires
  origin_case_ref:              # the case the candidate was born from (excluded from its own test set)
  evidentiary_case_set: []      # the pre-declared later cases it was tested on (provenance for the citation guard, §3)
  validation_status: candidate | promotion_validated   # candidate = N=0 hypothesis; promotion_validated = passed §3 gate at product-learning
  efficacy_status: unproven | scored   # forward value vs the calls that cited it; see §5 (execution data-blocked)
  staleness: { stale_if: [], last_reviewed: }
  non_claims:
    - promotion_validated means passed the gate at product-learning, never a stronger tier
    - a lesson never admits/unfreezes a source-family (JSG-01 frozen)
    - efficacy_status: unproven until forward-citation data exists; a lesson improves no call until proven
```

### 3. The promotion gate (the cherry-pick guard for lessons — stronger than for signals)

This is the architecture's crux, and the **adversarial lane's central
contribution**: a *signal* pre-commits its direction inside the blind call, so
K-of-N is enough. A *lesson* is **born post-reveal from one case** and has no
natural pre-commitment locus — so K-of-N alone is a costume (gameable on
test-case selection, loose "correct", and small-N). A candidate becomes a
**carried** lesson only when **all** hold:

1. **Falsifiable mechanical predicate** — `trigger_predicate` is a mechanical
   condition a third party could evaluate, not prose loose enough to fit any bad
   outcome. (Closes the "loose correct" axis.)
2. **Pre-declared test set, fixed before reveal** — `evidentiary_case_set` is
   fixed **before any test case's outcome is examined for favorable alignment**,
   exactly batch-1's "fix the set first." (Closes the test-case-selection axis.)
3. **Origin-excluded K-of-N report-all** — tested on the pre-declared set
   **excluding `origin_case_ref`**, reporting every applicable case (helped /
   hurt / not-applicable / unscoreable). "Would have helped on its origin case"
   is structurally worthless (fit to that case) → N=0, never carried. Honest
   claim: "lesson L improved the call in K of N pre-committed later cases."
4. **Generation/validation lane separation** — the postmortem that *generated*
   the candidate and the pass that *tests* it are not the same actor on the same
   case (the de-correlation discipline the review lanes use).

### 4. Emit into the step-1 ledger (no re-derivation)

A promoted lesson whose adjustment leans on a named signal **emits a
`pre_committed_use` row into the step-1 signal-reliability ledger in its existing
schema** (`signal_id`, `predicted_direction`, `outcome`, `blind_call_ref`,
`resolution_ref`). The postmortem is the **"backtest postmortem" inflow source
the ledger already names.** This architecture defines the *protocol that produces
those rows honestly*; it does **not** define a second reliability tally.

### 5. The firewall guard on the citation channel (the leak the adversarial lane caught)

The far-half's learning loop feeds `lessons_consulted` **forward into the next
sealed call** — and that next call **is** a judgment score. So the firewall is
not simply "scored vs unscored"; it is a one-step-delayed conveyor: an
outcome-aware lesson from case A becomes a pre-reveal input to case B. Without a
guard, that is **legalized hindsight transfer**. The guard:

- **Citation disjointness:** a lesson may be cited at a case's seal **only if its
  `evidentiary_case_set` (and `origin_case_ref`) are disjoint from the case being
  sealed and its same-family neighbors.** Decision-memory reads **carry the
  lesson's evidentiary provenance** so this is checkable at seal time. A lesson
  validated partly on B's family-neighbors may not inform B's blind call.
- **Lesson typing:** `loop_mechanics` lessons (about the loop's own machinery —
  "our resolution criteria were vague") **never enter the `decision_family`-keyed
  judgment read path.** Only `judgment_domain` lessons inform a blind call. (This
  closes the reflexivity leak; Phase-1's stated "loop-mechanics learning only"
  purpose means most *early* lessons are exactly the type that must be quarantined
  from the judgment path.)

### 6. Efficacy / demotion (specified as a core invariant; execution data-blocked)

A growing "validated lessons" library that never improves a sealed call is the
loop's most seductive **fake-success** (adversarial lane). The control is the
far-half's channel-4 meta-loop: because each call cites `lessons_consulted`, a
carried lesson is **scored against the calls that cited it**, and a lesson whose
citations correlate with *worse* calls **demotes**.

- This is a **core invariant**, not a deferred nicety: a lesson's
  `efficacy_status` is `unproven` until citation data exists, and **a lesson may
  never be claimed to improve calls while `efficacy_status: unproven`.**
- Its **execution is data-blocked** (the grounding lane's correction to the
  adversarial lane): it needs `lessons_consulted` citation data, which only
  accrues once the loop runs. So the demotion gate is **specified and required,
  but cannot run until rows exist.** "Promotion-validated, efficacy-unproven" is
  the honest standing state of every v0 lesson. This satisfies both lanes:
  the mechanism is not cut (adversarial), and we do not pretend to run it without
  data (grounding).

## Core / Satellite Boundary

**Core** (case- and domain-agnostic; stable):
- the adversarial-postmortem protocol + the derivability bar;
- the validated-lesson cell vocabulary and `lesson_type`;
- the promotion gate (mechanical predicate + pre-declared origin-excluded
  test set + K-of-N report-all + generation/validation separation);
- the citation-disjointness firewall guard and the judgment-path typing rule;
- the efficacy/demotion invariant (specified; execution data-blocked);
- the emit-into-step-1-ledger boundary; product-learning cap; JSG-01 freeze;
  quarantine-as-data.

**Satellite** (per case / per domain; never hardened into core):
- every specific case, lesson content, and decision-family prior;
- domain outcome sources; the org-motion signal as one *instance* (the core must
  not assume "signal == org-motion-shaped" — the adversarial lane's coupling
  warning).

## Dependency Map

**Now-buildable (counterparty-free, docs + by-hand):**
- N-a: the **postmortem + lesson-cell semantics spec** (the protocol, fill-rules,
  derivability bar, the promotion-gate definition, the citation guard, lesson
  typing) — pure docs/vocabulary, zero lock-in. This is step 3's first artifact.
- N-b: **one by-hand adversarial postmortem on a single already-scored batch-1
  case** — produces the step-1 ledger's first *real* row and one *candidate*
  lesson (N=0, uncarried). Falsifies the protocol.

**Blocked / deferred (named, not built):**
- B-a: **efficacy/demotion execution** — data-blocked on `lessons_consulted`
  citations that accrue only once the loop runs (§6).
- B-b: **lesson schema-as-code / store / index / query engine** — decision-memory
  is a read projection, not a store; a lesson is a docs record like a batch-1
  entry. No tooling until by-hand proves the shape.
- B-c: **far-half decision-object field reconciliation** for the lesson cell —
  marked `stale_if`, not committed (keep the cell source-agnostic like the step-1
  ledger).
- B-d: **a lesson criteria-quality rubric** beyond pass/fail promotion —
  measure-first (the batch-1 / phase-0 pattern).
- B-e: **any lesson→source-family promotion** touching JSG-01 — separate
  owner-gated decision.

## Smallest First Move (step 3)

**The postmortem + lesson-cell semantics spec (N-a), then one by-hand adversarial
postmortem on Beauty Pie #3 (N-b)** — it already carries a paired org-motion blind
prediction and a resolution, so it is the natural falsification case. That run
produces the step-1 ledger's first real row (today it has only
`example_not_a_real_row`) and one gated lesson *candidate* (explicitly N=0,
uncarried), demonstrating the firewall-clean protocol end to end before any
K-of-N promotion is attempted across cases. Cheap, counterparty-free, and it
either survives real contact with a scored case or it doesn't.

## What Would Change The Recommendation

- The step-1 ledger schema changing before this lands (re-reconcile §4).
- Evidence that lessons cannot be expressed as falsifiable mechanical predicates
  for the target families (would weaken the promotion gate to prose, which the
  adversarial lane shows is gameable — a materially weaker design).
- An owner decision to run the far-half loop first (would unblock §6 execution
  and reorder the dependency map).

## Non-Claims

- Planning only; product-learning; a target, not a capability claim.
- Reinvents nothing: batch-1, the step-1 ledger, and far-half decision-memory are
  reused by pointer, not re-specified.
- Mints no claim-tier / ladder vocabulary; "validated lesson" = passed the
  promotion gate at product-learning, never a stronger tier.
- Validates no lesson, populates no row, promotes no signal or source-family;
  JSG-01 stays frozen.
- The efficacy/demotion gate is specified and required but data-blocked; no v0
  lesson may be claimed to improve calls.
- Not validation, readiness, acceptance, buyer proof, or judgment-quality.

## Claim Classification

```yaml
judgment_spine_claim_classification:
  evaluated_claim_surface: near-half backtest-learning target architecture (planning/design artifact)
  source_quality_state: design/control artifacts only (step-1 ledger + far-half + batch-1 + conductor + ladder, re-verified on main) + 3 advisory perspectives
  execution_quality_state: no postmortem run, no lesson, no row exists
  closeout_state: no_durable_evidence
  claim_cap: design input / product-learning context only
  weakest_missing_or_failed_gate: no postmortem protocol spec yet (step 3); no real run; efficacy gate data-blocked
  receipt_artifact_or_gap: first receipts are the step-3 semantics spec + one by-hand postmortem producing the ledger's first real row
  non_claims:
    - not validation unless separately proven
    - not readiness unless separately proven
    - not buyer proof unless the buyer-proof receipt is complete
    - not judgment-quality evidence unless the judgment-quality receipt is complete
```

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The near-half (backtest-learning) target architecture is now a durable
    PROPOSED artifact: it occupies the slot the far-half cut ("the adversarial
    step lives in the near half"), adds exactly the adversarial-postmortem
    protocol + the validated-lesson cell/promotion-gate, and binds a
    citation-disjointness firewall guard, lesson typing, and a specified-but-
    data-blocked efficacy/demotion invariant. Step 2 of 3 of the near-half build.
  trigger: architecture_doctrine
  controlling_sources_updated:
    - docs/product/judgment_spine/near_half_backtest_learning_architecture_v0.md (new; this file only)
  downstream_surfaces_checked:
    - docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md  # consumed by pointer (signal sink); emit boundary matches its named backtest-postmortem inflow; no edit
    - docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md  # this fills the "near half owns lesson validation" slot it declared; the citation guard is the live-firewall analog of its disclosure-burns-comparator rule; no edit (it already routed validation here)
    - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md  # K-of-N/report-all/pre-commitment reused, not amended
    - docs/product/judgment_spine/conductor_construction_integrity_probe_addendum_v1.md  # derivability bar + quarantine-as-data + de-correlation reused, not amended
    - docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md  # product-learning cap consumed; no tier minted
  intentionally_not_updated:
    - path: docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md
      reason: the far half already declared the near half owns lesson validation and named the channels; this architecture occupies that slot without changing far-half text. A reviewer finding a genuine interface mismatch should flag it, not silently edit.
    - path: docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md
      reason: the ledger already names "backtest postmortem" as an inflow source with the exact row shape; this architecture is that source, no ledger edit needed.
  stale_language_search: >
    rg -n "near-half|near half|adversarial-postmortem|validated-lesson|lesson cell|promotion gate|lessons_consulted"
    docs/product/judgment_spine docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md
  non_claims:
    - not validation
    - not readiness
    - not a source-family admission or JSG-01 unfreeze
    - not implementation authorization
```
