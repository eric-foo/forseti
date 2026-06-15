# Judgment-Spine Demand-Read Core Architecture v0 (PROPOSED — the demand-read core the two shells wrap)

```yaml
retrieval_header_version: 1
artifact_role: Product architecture object (PROPOSED target architecture — pending owner adjudication)
scope: >
  Target architecture for Orca's demand-read judgment CORE ("object C"): the
  market-agnostic procedure that turns an ALLOWED demand signal into a verdict +
  action ceiling (allow → weight → verdict+ceiling → counterfactual). The two
  mode-shells that wrap it — backtest learning and the live decision loop — and
  the per-source weighting store ALREADY EXIST in this lane as PROPOSED
  architectures; this object supplies the core-shaped hole none of them specify
  and reconciles to them by pointer. Design only; no scoring engine, no conductor
  edit, no implementation.
use_when:
  - Designing, reviewing, or implementing the demand-read judgment procedure (the steps that produce a verdict + action ceiling).
  - Deciding how a demand read plugs into the existing near-half (backtest) / far-half (live) loops and the signal-reliability ledger.
  - Placing a demand-read piece on the core-Judgment-doctrine vs beauty-satellite boundary.
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md   # the LIVE shell (far half): decision-object, shadow/assisted, seal-before-disclose, decision memory
  - docs/product/judgment_spine/near_half_backtest_learning_architecture_v0.md        # the BACKTEST shell (near half): adversarial postmortem + validated-lesson cell + promotion gate
  - docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md             # the per-source weighting store (firewall-clean K-of-N report-all)
  - docs/product/judgment_spine/conductor_construction_integrity_probe_addendum_v1.md # current contamination doctrine (JSG-08 tell-audit; active recall dropped)
  - docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md      # the FROZEN backtest conductor (core enters through the JSG-06 sealed judgment surface; never edit it)
stale_if:
  - The conductor's No-Authority Invariant A or Route-Don't-Restate Invariant B changes.
  - The buyer-proof no-scoring boundary is lifted or the Demand-Substrate Hard Gate is re-derived.
  - The near-half/far-half/ledger architectures amend their loop, gate, or store shape (re-reconcile this core's plug points).
  - The conductor construction-integrity addendum's contamination model (JSG-08 tell-audit; active recall dropped) is amended.
  - The owner adjudicates this proposal (adopt / amend / reject).
```

## Status

`PROPOSED_PENDING_OWNER_ADJUDICATION` — authored 2026-06-13, hardened 2026-06-14
by the Judgment-Spine read-machinery architecture lane (worktree
`judgment-spine-read-machinery-architecture-v0` off `origin/main`), picking up
the cold handoff
`docs/prompts/handoffs/judgment_spine_read_machinery_architecture_handoff_v0.md`.

This is a target-architecture **recommendation**, not accepted doctrine. It was
authored under the architecture-planning standard profile with one directional
local pass and two owner-authorized subagent lanes (adversarial, grounding); the
adversarial lane caught that the handoff's "two shells + deck" design **reinvents
an existing three-part PROPOSED program in this same lane** (near-half backtest
learning, far-half prospective loop, signal-reliability ledger). This object was
rewritten to keep only its genuinely new contribution — the demand-read judgment
**core** — and reuse the existing program by pointer.

It was then hardened by a **cross-vendor (OpenAI/GPT-5 family) delegated
review-and-patch** pass (de-correlated from the Claude author per
`.agents/workflow-overlay/delegated-review-patch.md`): findings DRP-01 (isolate
only the sealed C3/C4 surface as the JSG-06 contestant, not the whole core),
DRP-02 (C2 admits only citation-disjoint `judgment_domain` lessons), and DRP-03
(no separate satellite card-set claim) were CA-adjudicated and **accepted**
2026-06-14. This repo-mode cross-vendor discovery pass discharges the R6
pre-freeze leakage independent-review requirement at `product_learning` tier
(residual: the delegate's own edited lines are covered by its class-sweep, not an
independent pass). The CONSUME direction below is independently corroborated by
the retiring near-half lane's own cold handoff
(`docs/prompts/handoffs/near_half_reconciliation_handoff_to_read_machinery_lane_v0.md`,
near-half artifacts verified on `origin/main`: architecture `5faf1728f8389870`,
ledger `388352b83bac9860`).

Design-only. No implementation, scoring engine, runner, schema, conductor edit,
or gate reopening. Carries no validation/readiness/buyer claim; caps at
`product_learning`.

## The Architecture Question

The lane already has a backtest-learning loop (near half), a live decision loop
(far half), and a signal-reliability ledger. What **none** of them specifies is
the demand-read judgment procedure itself — the steps that turn an *allowed* demand
signal into a verdict + action ceiling. The far-half decision-object has a
`sealed_call` slot (`recommendation`, `confidence_band`, `signals_used`,
`reasoning_trace`); it does not say how a demand read *fills* it. The taxonomy
names this exact gap (pipeline steps 5–6: cleaning, evidence-packaging for
judgment, "DEVELOPING"); the buyer-proof memo shape only implies it as prose.

**What is the market-agnostic core procedure for a demand read, and how does it
plug into the existing two shells and the signal store without reinventing them
or violating the conductor's invariants?**

## Target Architecture: One Core, Two (already-existing) Shells

**Decision: `TARGET_RECOMMENDED`.** One market-agnostic, mode-agnostic demand-read
judgment **core**. The two mode-shells that wrap it are **not new** — they are the
PROPOSED near-half (backtest) and far-half (live) loops already in this lane. The
core is the piece they both presuppose and neither specifies.

```text
   BACKTEST shell = near_half_backtest_learning_architecture_v0    LIVE shell = prospective_decision_loop_target_architecture_v0
   (sealed core call through JSG-06; scored vs known                (core fills the decision-object sealed_call; shadow/assisted;
    outcome; adversarial postmortem mints validated lessons)         seal-before-disclose; outcome lands later → resolution)
                         \                                          /
                          \------------------ THE CORE (this object) ------------------/
                            C0 Frame → C1 Allow(gate) → C2 Weight(de-correlate·diverge·ledger)
                            → C3 Verdict + Action Ceiling → C4 Counterfactual  (+ required reasoning trace)
                                              |
                          weighting store + lessons: near_half_signal_reliability_ledger_v0
                          + the validated-lesson library (decision memory) — NOT a new "deck"
```

### The Core (steps C0–C4) — the new contribution

Market-agnostic and mode-agnostic at the architecture level: both shells use the
C0-C4 procedure, but each shell owns which acts are pre-seal input assembly,
which are inside an isolated judgment, and which occur after resolution. In
backtest mode, only the JSG-06 sealed judgment surface is isolated; the C1 allow step
and any C2(c) ledger / lesson lookup complete before the child run and are not
live-read by it. Every run must emit a **reasoning trace** (the JSG-06 /
decision-object `reasoning_trace` analog, required per conductor addendum v1 R4)
so contamination can be tell-audited and lessons extracted.

- **C0 — Frame.** A demand read runs only inside a Decision Frame (spine
  boundary: "Decision Frame remains the required starting point") — made explicit
  here, consistent with the buyer-proof memo opening (decision question + live
  trigger) and the far-half decision-object `frame`.
- **C1 — Allow.** Apply the **Demand-Substrate Hard Gate** (≥2 independent venue
  families; costly-behavior anchor; integrity labels per venue). Fail →
  disqualify/hold. The core **routes to** the gate (owned by the buyer-proof
  packet); it does not restate it, and does not reopen the ratified gate
  decisions.
- **C2 — Weight.** Over allowed signals: **(a) de-correlate** shared-origin
  signals via `derived_from` (independence is the truth-amount, not volume);
  **(b) map divergence** via `diverges_from` (cross-venue disagreement is signal);
  **(c) weight per decision-family** by reading the **signal-reliability ledger**
  (a signal is reliable *within* a `decision_family`, K-of-N report-all) and the
  validated-lesson library. Only citation-disjoint `judgment_domain` lessons may
  enter the judgment read path; `loop_mechanics` lessons and lessons whose
  evidentiary set overlaps the case / same-family neighbors stay out. Weighting
  is **qualitative, LLM-in-session, explained** — see INV-1.
  *(`derived_from`/`diverges_from` semantics are owned by the dispatched
  ontology-backbone commission, currently branch-only — confirm on adoption.)*
- **C3 — Verdict + Action Ceiling.** Emit the **demand-state verdict** on main's
  two-axis model — **durable / transient** (persistence), given **real** (not
  manufactured) — and the action ceiling **matched to the demand's lifespan**:
  **act / phase / narrow / hold / defend** (long-horizon *commit* vs short-horizon
  *move*). The ceiling is capped by the weakest load-bearing evidence — costly
  behavior can reach Commit-grade; engagement volume alone caps lower (buyer-proof
  rule). **Persistence-axis** risk patterns (resale/flip, event/one-time,
  scarcity/panic) are classified **here** as transient, not capped at C2 (their
  discriminator families arrive from C2 Rule 3); **manufactured-axis** integrity
  defeaters are handled upstream at C2 (Rule 3) + the C1 gate. ("Hollow" is retired
  per main #78: it conflated transient with manufactured.)
- **C4 — Counterfactual.** "What evidence would let us decide better — what would
  change the answer?" (the buyer-proof memo's names-what-would-change line; the
  source of `assumptions` / `kill_or_adjust_triggers` for the live shell).

### How the core plugs into the two existing shells

- **Backtest shell — reuse `near_half_backtest_learning_architecture_v0`.** The
  demand core plugs into the unchanged conductor through the JSG-06 contestant
  interface, but the scoreable child run is **not** the whole C0-C4 procedure.
  The isolated child is the sealed C3/C4 verdict + counterfactual + reasoning
  trace over the frozen participant packet; C0 frame, C1 gate routing, and any
  C2(c) ledger / lesson lookup are facilitator / packet-construction decisions
  completed before isolation and recorded only as provenance or frozen packet
  facts where the packet owner permits. The child runs with
  `external_retrieval_disabled` / `hidden_context_boundary`; live ledger cards,
  lesson cards, facilitator material, and off-packet sources may **not** be
  in-context during the isolated verdict. Learning from scored calls is
  **already owned** by the near-half adversarial-postmortem + validated-lesson
  cell + promotion gate; this object adds no parallel "distillation tail."
- **Live shell — reuse `prospective_decision_loop_target_architecture_v0`.** The
  core fills the decision-object `sealed_call`; the far half owns shadow/assisted
  modes, seal-before-disclose, the append-only registry, decision memory, and the
  four learning channels. Live drops blind because — as the far half already
  argues — a live decision gets the blind seal **for free** (no one holds the
  outcome at seal time); the firewall risk **moves** to disclosure / resolution /
  post-hoc editing, which the far half closes (this object does not re-solve it).
- **Re-entry (ADV-5 fix).** When a live case's outcome lands, it becomes
  backtest-scoreable **only through the existing firewall machinery**: the
  far-half append-only seal-before-disclose record supplies the outcome-blind
  sealed call, and the near-half **citation-disjointness** guard prevents a
  case's own live read from calibrating lessons later cited on it or its
  family-neighbors. There is **no new re-entry hook** in this object; re-entry is
  routed, not built (the conductor re-entry predicate row is decision C, below).

### Weighting store and lessons (reconciled — NOT a new "deck")

The handoff's "deck" and "checkpoint #3 = weighting" are **already owned**:

- **Per-source weighting** = `near_half_signal_reliability_ledger_v0` — the
  firewall-clean `(signal_id, case_id)` pre-committed-use unit, K-of-N report-all,
  reliability *within* a `decision_family`, product-learning cap. This is the
  owner-sanctioned home for "what weight a source/signal earns in a vertical,
  learned from past cases" (= checkpoint #3). C2(c) **reads** it.
- **Lessons** = the near-half **validated-lesson library** (read via the far-half
  decision-memory projection). C2 consults only lessons that pass the near-half
  citation-disjointness guard and `judgment_domain` typing; the near-half
  **promotion gate** validates them.
- **Survival discipline** = the ledger's `staleness` + caps and the far-half
  append-only / dated-amendment governance already provide the hard-cap /
  review-date / fail-soft / dated-amendment "survival kernel" pattern. This
  object does not add or verify a separate satellite card set.

## Decisions

- **Decision A — checkpoint #3 = weighting. RESOLVED (owner, 2026-06-13).** Built
  in at C2(c) as a **read of the signal-reliability ledger** (per `decision_family`,
  K-of-N report-all), not a new store. Stays qualitative/in-session under INV-1.
- **Decision B — extend the conductor vs sibling. RECOMMENDED: the core is a thin
  sibling; both shells already exist (owner sign-off).** The "extend vs sibling"
  tension dissolves: backtest mode is the **unchanged** conductor receiving the
  core's sealed judgment surface through JSG-06
  (`judgment_quality_promotion_operating_model_v0.md` JSG-06 + Isolation
  Topology), so nothing is grafted in (INV-2). The live mode is the existing
  far-half loop. This object adds only the **core**, by pointer to both.
- **Decision C — distillation-tail / re-entry predicate onto the backtest path =
  its own scoped sub-pass. DEFERRED.** It touches the Round-19-reviewed conductor's
  surroundings and the near-half/far-half emit-consume boundary; run it as a
  separate pass under the same delegated/adversarial review discipline.
- **Decision D — NEW, owner-bound: reconcile the owner-set PROVE gate with the
  near-half promotion gate.** The handoff records an owner decision (2026-06-13)
  for a distillation tail diagnose→**PROVE**→generalize→install, where PROVE =
  re-run the **same case** on a fresh same-family instance armed with the lesson,
  keep if materially better. The near-half architecture (PROPOSED) already defines
  a **stronger** promotion gate — falsifiable mechanical predicate + pre-declared
  origin-excluded **K-of-N report-all** + generation/validation lane separation —
  and explicitly classifies "would have helped on its origin case" as
  **structurally worthless → N=0, never carried**
  (`near_half_backtest_learning_architecture_v0.md` §3). The retiring near-half
  lane's reconciliation handoff recommends CONSUME and folding PROVE in, calling
  PROVE "genuinely stronger" than K-of-N. **Recommendation (with a correction to
  that framing):** PROVE and K-of-N measure **different axes and both run** — PROVE
  is a same-family **reproducibility / contamination pre-check on the origin case**
  (does the lesson leak the outcome; does a fresh instance reproduce the gain),
  while the near-half origin-excluded **K-of-N report-all is the generalization
  gate**. PROVE is **not** "stronger" and **cannot** substitute or dominate K-of-N:
  it acts on the origin case, which the near-half doc itself classifies as
  *structurally worthless for generalization (N=0)*. So PROVE **precedes and
  complements** the generalization gate; it does not replace it. The owner
  reconciles the exact gate wording; this object does not silently drop PROVE nor
  override the near-half gate, and CONSUME (this object's direction) is now
  corroborated by the near-half lane's own handoff.

## Spine Placement (core/satellite)

The lane's **MODE** axis is already realized by the near-half (backtest) and
far-half (live) shells; this object adds only the **core** on that axis. The
**MARKET** axis is where this object does its placement work:

| Core Judgment doctrine (market-agnostic) | Beauty satellite (bounded adaptation) |
| --- | --- |
| The C0–C4 core procedure shape | The specific venue families + costly-behavior instances (sellouts, dupe-switching, restock pressure) |
| Independence/de-correlation (`derived_from`) + divergence (`diverges_from`) | Verb-tiering calibration (which verbs map to which ceiling in beauty) |
| Two-part weight → verdict → action-ceiling shape | Per-vertical wind-caller **identities** (who calls beauty winds, e.g. INCIDecoder) |
| Costly-behavior-as-truth-test; the counterfactual step | Beauty-specific ledger rows + lesson content |

**Ownership (spine boundary):** the core sits in **Judgment Spine** (Signal-Use
Classification, Decision Strength, Action Ceiling). The signal-reliability ledger
and validated-lesson library are **Outcome Memory** (production + storage); the
core only **consumes** them at C2 — Judgment Spine "must not own … deck
production." The C1 allow step routes to the buyer-proof gate.

## Invariants Later Work Must Preserve

- **INV-1 — No scoring engine (operational discriminator).** Weighting and verdict
  are qualitative, LLM-in-session, explained. **No card/row may carry a numeric or
  ordinal weight or a deterministic apply-rule**; the signal-reliability ledger
  records a graded *track record* (K-of-N) the in-session read interprets. Numeric/
  calibrated weighting graduates only when the owner explicitly lifts the
  no-scoring boundary. (Buyer-proof do-not-build list: "Scoring engines",
  "Automated scoring".)
- **INV-2 — Don't graft onto / don't edit the conductor.** In backtest mode, the
  core enters the conductor only through the JSG-06 sealed judgment surface; it
  never becomes logic inside the conductor. Conductor stays FROZEN and
  No-Authority.
- **INV-3 — Contamination is outcome-USE, not outcome-visibility (per addendum
  v1).** Backtest contamination is caught by the **JSG-08 tell-audit on the
  reasoning trace** (a call that asserts the outcome or cites non-brief knowledge
  with no derivation is a confirmed tell → contaminated/quarantined-as-data);
  active recall is dropped, JSG-05 is a non-inducing screen only. The live shell
  needs no blind wrapper (blind seal for free). Do not re-import the superseded
  "memorization-probe / must-not-see-the-outcome" framing.
- **INV-4 — Learning crosses backtest→live only through the sanctioned channels.**
  The signal-reliability ledger (per-source) and the validated-lesson library (via
  decision memory) are the sanctioned durable channels, each firewall-guarded
  (K-of-N report-all; citation disjointness). **Named residual (not a clean single
  membrane):** same-model-family tacit transfer and the re-entry path are
  controlled by the far-half blind re-entry + near-half disjointness guards, not
  eliminated.
- **INV-5 — Live caps at `product_learning`** and carries Live-Outcome-Memory
  attribution degradation / influenced-path-calibration limits (far half). A live
  verdict is never a scored/validated/buyer claim.
- **INV-6 — Consume, don't reopen.** The Demand-Substrate Hard Gate and the
  ratified demand-gate P2/P3/P4 are admission inputs this machinery consumes.

## Deferred Implementation Implications (non-executable)

- All store/loop implementation (ledger, lesson library, decision-object,
  seal registry, postmortem) is **owned by the near-half/far-half/ledger
  architectures** and deferred there; this object adds none.
- **Numeric weighting** — deferred behind INV-1 + an explicit owner lift.
- The **conductor re-entry predicate row** — decision C sub-pass.
- The **`derived_from` / `diverges_from`** link types — owned by the dispatched
  ontology-backbone commission; consume, do not redefine.
- The **PROVE-vs-promotion-gate reconciliation** — decision D, owner-bound.

## What Would Change The Recommendation

- The near-half/far-half/ledger architectures changing their loop/gate/store shape
  (re-reconcile the plug points).
- The buyer-proof no-scoring boundary being lifted (numeric weighting then
  admissible at C2 / the ledger).
- The conductor's No-Authority/Route-Don't-Restate invariant changing (the JSG-06
  sealed-judgment-surface reconciliation depends on it).
- Owner reconciliation of decision D landing against (not for) a same-family
  pre-check (PROVE would then need a different home or retirement).

## Source-Read Ledger

Bounding sources read fresh from the worktree off `origin/main`; the three
same-lane sibling architectures and the conductor addendum were read **after** the
adversarial subagent lane flagged them (correcting an initial scoping miss — the
first draft cited only the four handoff-named sources and wrongly claimed the
lane held no overlapping architecture).

- `docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md`
  — FROZEN backtest conductor; Invariant A/B; JSG-06 contestant blind judgment +
  Isolation Topology; deterministic scorer JSG-07; by-hand → `product_learning`.
- `docs/product/judgment_spine/near_half_backtest_learning_architecture_v0.md` —
  the backtest shell: adversarial postmortem + validated-lesson cell + promotion
  gate (origin-excluded K-of-N report-all); citation disjointness; lesson typing.
- `docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md`
  — the live shell: decision-object, shadow/assisted, seal-before-disclose,
  decision memory, four learning channels, governance.
- `docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md` — the
  per-source weighting store (firewall-clean K-of-N report-all, product-learning
  cap, decision-family scoping).
- `docs/product/judgment_spine/conductor_construction_integrity_probe_addendum_v1.md`
  — current contamination doctrine (active recall dropped; JSG-08 tell-audit on
  the reasoning trace; outcome-USE not recognition).
- `docs/prompts/handoffs/near_half_reconciliation_handoff_to_read_machinery_lane_v0.md`
  — cross-lane provenance (inherited): the retiring near-half lane's directive to
  CONSUME the landed near-half artifacts, not re-derive. Near-half substrate
  hashes verified on `origin/main`: architecture `5faf1728f8389870`, ledger
  `388352b83bac9860` (#64 not landed; ledger is the current #54 version).
- `docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
  — Judgment-Spine ownership; scoring engines deferred; Outcome Memory
  Backtest/Live split; Decision Frame required.
- `docs/product/product_lead/orca_buyer_proof_packet_v0.md` — Demand-Substrate
  Hard Gate; action-ceiling vocab; no-scoring boundary; `product_learning` cap.
- `docs/product/product_lead/orca_demand_read_taxonomy_v0.md` — signal layers,
  read types, wind-caller calibration; pipeline gap (steps 5–6).
- **Source gaps (non-blocking for design):** the ontology-backbone commission
  prompt (`derived_from`/`diverges_from`) is branch-only, not on `origin/main` —
  link semantics used per the handoff, confirm on adoption; the demand-gate
  closures proposal (P2/P3/P4) is untracked/branch-only — consumed, not reopened.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Demand-read CORE C1 step renamed Admit -> Allow (and its derived object
    "admitted signal" -> "allowed signal") to remove the confess/concede ambiguity;
    the C1 admissibility GATE concept (Demand-Substrate Hard Gate, ratified G1/G2)
    is unchanged. C3 verdict re-grounded onto main's two-axis model (durable /
    transient + real / manufactured): "durable-vs-hollow" retired (main #78);
    persistence-axis risk patterns are classified transient at C3 (not capped at
    C2), receiving discriminator families from C2 Rule 3.
  trigger: architecture_doctrine
  related_triggers:
    - product_doctrine
  controlling_sources_updated:
    - docs/product/judgment_spine/judgment_spine_demand_read_machinery_architecture_v0.md
    - docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md
  downstream_surfaces_checked:
    - docs/product/product_lead/orca_demand_read_taxonomy_v0.md   # already two-axis; "hollow" hits are the retirement explanation, kept
  intentionally_not_updated:
    - path: "C2 admits ... lessons" (DRP-02 line), "admission inputs" (ratified gate), "admissible at C2" (permissible)
      reason: lesson-admission and gate-admissibility are distinct from the C1 demand-signal step; the rename targets the C1 step verb + its "admitted signal" object only.
  stale_language_search: >
    rg -i "admit|admitt|admiss|hollow" on the two edited docs (2026-06-15): no "C1
    Admit", no "admitted signal", no live "durable-vs-hollow"; residuals are all
    intended-keep (lesson-admission, gate-admissibility, retirement explanation).
  non_claims:
    - not validation
    - not readiness
    - not a live fold to origin/main (per-lane PR pending)
```

## Non-Claims

- Not validation, readiness, buyer proof, judgment-quality evidence, or
  commercial readiness; closeout state for any such claim: `no_durable_evidence`.
- Authorizes no implementation, scoring engine, automated scoring, runner,
  schemas, storage, conductor edit, or reopening of the demand gate.
- Reinvents nothing: the two shells and the weighting store are reused by pointer,
  not re-specified.
- Mints no evidence-ladder vocabulary and redefines no overlay-owned semantics.
- PROPOSED only. On owner adoption, this object owes a dated pointer via the
  Doctrine-Change Propagation Contract
  (`.agents/workflow-overlay/source-of-truth.md`); the conductor row stays FROZEN
  unless changed inside an owner-dated act.

## Claim Classification

```yaml
judgment_spine_claim_classification:
  evaluated_claim_surface: demand-read judgment core target architecture (planning/design artifact)
  source_quality_state: design/control artifacts only (conductor + spine boundary + buyer-proof + taxonomy + the three same-lane shell/ledger architectures + conductor addendum, read fresh) + 1 directional local pass + 2 owner-authorized subagent lanes (adversarial, grounding)
  execution_quality_state: no demand read run, no lesson, no row, no sealed call exists
  closeout_state: no_durable_evidence
  claim_cap: design input / product-learning context only
  weakest_missing_or_failed_gate: no run exists; decision B/D owner-unsigned; decision C deferred
  non_claims:
    - not validation unless separately proven
    - not readiness unless separately proven
    - not buyer proof unless the buyer-proof receipt is complete
    - not judgment-quality evidence unless the judgment-quality receipt is complete
```

## Architecture Result

`TARGET_RECOMMENDED` — the demand-read core (C0–C4) wrapped by the two
already-existing shells, with the signal-reliability ledger + validated-lesson
library as the weighting/learning store. Decision A built in (as a ledger read);
decision B recommended (thin core sibling; shells already exist) pending owner
sign-off; decision C deferred; **decision D (PROVE vs the near-half promotion
gate) newly surfaced and owner-bound.** Smallest complete next routing object:
**owner review of this object + decisions B and D**; then (if accepted) the
decision-C sub-pass and, behind explicit authorization, implementation scoping
owned by the near-half/far-half/ledger lanes.
```text
This is advisory architecture input only. It is not a verdict, not implementation
authority, and not proof of readiness.
```
