# Judgment-Spine C3 Verdict + Action-Ceiling Contract v0 (PROPOSED — how the demand-read core's C3 turns weighted signals into a verdict + action ceiling)

```yaml
retrieval_header_version: 1
artifact_role: Implementation-facing behavior/contract spec (PROPOSED binding-side interface — what must be true when the demand-read core's C3 emits the demand-state verdict + action ceiling; binds no row, builds nothing, runs nothing)
scope: >
  The binding-side contract for one owner-ADOPTED-but-unspecified step: how the
  demand-read core's C3 (Verdict + Action Ceiling) turns the C2-weighted allowed
  signals into a two-axis demand-state verdict (durable / transient, given real)
  and an action ceiling (one verb from monitor / probe / commit / hold / scale / avoid /
  reduce; horizon accretes via monitoring) matched to the
  demand's lifespan, filling the far-half decision-object sealed_call. Specifies
  C3 to the depth the C2 ledger read-contract already has. Qualitative,
  LLM-in-session, explained — never a number (INV-1). Consumes the C1 gate and
  the C2 weighting + Rule 3 routing by pointer; edits neither.
use_when:
  - Scoping or running the demand-read core's C3 (emitting a verdict + action ceiling).
  - Reviewing whether a C3 reasoning trace stays within INV-1 (no scoring engine) and the buyer-proof ceiling-cap rule.
  - Checking that a verdict obeys the calling sequence (durable requires a named persistence-projection basis; transient is strong current-window demand) and the two-axis model.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md  # the demand-read core whose C3 this specifies (C3 step shape; owner-ADOPTED Decision B)
  - forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md             # the C2 step C3 consumes (weighted signals; Rule 3 routes persistence patterns here)
  - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md                              # the action-ceiling cap rule (floor vs ceiling; >=2 converging origins; engagement/resonance-only caps)
  - forseti/product/spines/judgment/learning_loops/far_half/prospective_decision_loop_target_architecture_v0.md      # the sealed_call output surface C3 fills (recommendation / confidence_band / signals_used / reasoning_trace)
  - forseti/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md                            # the read grammar (two-axis model + calling sequence + read types) C3 verdicts in
stale_if:
  - The core architecture amends C3's step shape, the two-axis verdict, or the calling sequence.
  - The buyer-proof action-ceiling cap rule (floor/ceiling, >=2 converging origins, engagement/resonance-only cap) is re-derived.
  - The far-half decision-object sealed_call slot shape or the contestant confidence-band vocabulary changes.
  - The owner lifts the no-scoring boundary (INV-1); a numeric/ordinal ceiling mapping then becomes admissible and the INV-1 disqualifiers below relax.
  - The taxonomy/read-grammar is owner-adjudicated and amends the read types or the durable/transient/manufactured states.
```

## Status

`PROPOSED` — binding-side behavior/contract spec, `product_learning` tier. It
**stabilizes what must be true** when C3 emits the verdict + action ceiling; it
**binds no real row, runs no case, and edits neither the C1 gate, the C2
contract, the FROZEN conductor, nor the far-half loop.** It fills the binding
half of a step the core architecture names and the owner ADOPTED (Decision B,
2026-06-14: "C3 Verdict+Action-Ceiling") but does not specify to contract depth —
only C2 had a read-contract. Authored 2026-06-15 in the demand-read first-earned-trust
lane (worktree `demand-read-first-earned-trust-slice1` off `origin/main`), under an
owner build-gate lift bounded to the first by-hand read work unit. C3 is the
step whose output the first read's whole claim rests on; specifying it to C2's
depth is what lets a read be run without inventing the verdict+ceiling intent.

## Amendment — 2026-06-20 (owner-directed): Action-Ceiling Vocabulary Replaced (Flat Verb Set; Horizon Via Monitoring); Bayesian Reasoning Accepted

Owner-directed in-thread. This **replaces the action-ceiling vocabulary**; it does
**NOT delete this contract.** The verb×horizon model named below — verbs
`{act, phase, narrow, hold, defend}` × horizon `{commit, move}` — is superseded by a
single **flat verb set**, and horizon stops being a declared output. The two-axis
verdict, the floor/ceiling cap rule, INV-1, and the consume-don't-reopen boundary
are **unchanged**. The former observed-only transient-default / earned-durable
wording is superseded by the 2026-06-23 durable-demand projection clarification.
Sections below that name the old verbs or the `horizon` field are read through
this amendment (dated; originals preserved).

**New action ceiling — exactly one verb from:**

- **monitor** — observe; no position taken (was `watch`). Keep reading the signal.
- **probe** — a small, reversible action taken to learn; not a real commitment.
- **commit** — take a real position; the **default verb for moving in**, reversible by default.
- **hold** — maintain the current stance: hold an existing position (neither scale up nor
  reduce), or hold off before committing. Low-commitment — does not require the material
  ≥2-origin bar.
- **scale** — increase an existing commitment; **earned** via monitored persistence, or
  taken on an exceptional initial outburst **only when the manufactured axis is cleared**
  (bigger outburst ⇒ higher integrity bar).
- **avoid** — do not enter / discount (manufactured demand, or not worth entering).
- **reduce** — wind down an existing position as real demand decays.

The removed verbs fold into this set: a defensive or scope-narrowed position is a
`commit` (or `scale` to deepen it); "wait / take no position" is `monitor` or `probe`;
staged entry is just a reversible `commit`. There is no separate `defend`, `narrow`,
`phase`, or `move`.

**Horizon is not declared.** The `horizon: commit | move` output is removed. The verb
carries the commitment; **monitoring** then earns `scale` (the long horizon) or triggers
`reduce` (decay) — horizon accretes from observation, never an upfront call. This makes the
calling sequence native: open with a reversible `commit` (or `monitor` / `probe` if
under-supported, `avoid` if manufactured); `scale` or `reduce` as persistence is observed.

**Demand-state → verb:** manufactured → **avoid**; real, entering → **commit** (reversible);
real, steady (maintain a committed position) → **hold**; real, persistence earned →
**scale**; real, decaying → **reduce**; pre-decision / under-supported → **monitor** or
**probe**.

**Cap rule (remapped; the floor/ceiling rule is otherwise unchanged).** **commit** and
**scale** are the material/committing verbs — each requires **≥2 independent converging
origins** plus gradeable costly behavior; a single independent origin, or
engagement/attention/resonance-only evidence, caps **below commit** (at `monitor` / `probe` / `hold`).
**avoid** and **reduce** *lessen* exposure, so they carry a **lower** evidence bar (you may
avoid or reduce on weaker evidence than you would commit or scale on). INV-1 holds: the verb
is a qualitative classification with reasons, never a computed or score-derived output.

**Bayesian reasoning — accepted as the read's grammar (qualitative).** The demand-state read
is a qualitative Bayesian update: a prior (category base rate / momentum) updated by
**discriminating** evidence, each signal weighed by *how much more it is expected under one
demand-state than another*. A discipline, not a numeric engine (INV-1, no numbers): the
`reasoning_trace` must state, per signal, **which demand-state the evidence favors and why** —
non-discriminating evidence (predicted equally by real and manufactured, or durable and
transient) must not move the verdict.

```yaml
direction_change_propagation:
  doctrine_changed: >
    The demand-read C3 action-ceiling vocabulary is replaced: the verb×horizon model
    {act,phase,narrow,hold,defend}×{commit,move} is superseded by a flat verb set
    {monitor, probe, commit, scale, avoid, reduce}, with horizon no longer declared (it
    accretes via monitoring — scale earns the long horizon, reduce handles decay). The cap
    rule remaps so commit and scale are the material verbs (>=2 converging origins + costly
    behavior) and avoid/reduce lessen exposure at a lower bar. INV-1, the two-axis verdict,
    floor/ceiling cap rule, and consume-don't-reopen are unchanged. The later 2026-06-23
    clarification supersedes the observed-only transient-default / earned-durable wording by
    requiring a named durability projection basis. Bayesian qualitative reasoning remains
    accepted as the read's grammar (prior x discriminating-likelihood, stated per-signal in
    the reasoning_trace; no numbers). The C3 contract document is retained, not deleted.
  trigger: product_doctrine
  related_triggers:
    - validation_philosophy
  controlling_sources_updated:
    - forseti/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md
    - docs/decisions/forseti_product_thesis_consumer_demand_v0.md
    - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md
    - forseti/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md
    - forseti/product/satellites/fragrance/judgment_level1/satellite_skeleton/fragrance_level1_product_learning_satellite_skeleton_v0.md
    - forseti/product/spines/foundation/ontology/forseti_ontology_backbone_architecture_v0.md
    - forseti/product/spines/product_lead/offer/forseti_offer_hypothesis_v0.md
    - forseti/product/spines/product_lead/proof_charter/forseti_product_proof_lead_charter_v0.md
    - forseti/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
    - docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md
  intentionally_not_updated:
    - path: ALL TEN DOWNSTREAM SURFACES ABOVE
      reason: >
        SEQUENCED REALIGNMENT, NOT SILENTLY FORKED. A repo-wide grep on
        2026-06-20 identified these ten surfaces as carrying the old action
        vocabulary ({act,phase,narrow,hold,defend} / {commit,move} /
        long/short-horizon). This amendment updates the OWNER (this C3 contract)
        only; the ten restating/referencing surfaces are named here for a
        sequenced realignment pass (depth varies and is not yet individually
        inspected — the foundation ontology and the owner-locked thesis Central
        Read #4 in particular need their own careful edits). The new verb set is
        controlling from this amendment; the old verbs in those surfaces are stale
        pending realignment, not a competing live vocabulary.
  stale_language_search: >
    rg -i "phase \| narrow|narrow, hold|long-horizon|short-horizon|Move → Commit|Excluded → Watch|act \| phase" (repo-wide)
  stale_language_search_result: >
    Executed 2026-06-20. Eleven files carry the old action vocabulary: this C3
    contract (owner — amended here), the demand-read taxonomy, the owner-locked
    product thesis (Central Read #4 + the 2026-06-14 durable→commit/transient→move
    mapping), the buyer-proof packet (cap rule — verb-name remap only; cap logic
    unchanged), the demand-read core (C0–C4 step shape), the fragrance satellite
    skeleton (verb lists), the foundation ontology backbone + its commission
    prompt, the offer hypothesis, the proof charter, and the scan core spec. Owner
    updated; the other ten are named above for sequenced realignment.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not judgment-quality evidence
    - INV-1 unchanged; verbs are qualitative classifications, no numeric/scored ceiling
    - C3 contract retained, not deleted; downstream realignment is sequenced, not complete
```

## Amendment Addendum — 2026-06-20 (post-adversarial-review AR-03 / AR-04; + the `hold` verb)

- **Seventh verb `hold` added** (owner-directed, post-review). The action set is now
  **monitor · probe · commit · hold · scale · avoid · reduce**. `hold` = maintain the
  current stance (hold a position without scaling or reducing, or hold off before
  committing); low-commitment (joins `monitor` / `probe`, not a material verb). This
  resolves the headline/vocabulary contradiction (the thesis headline "commit, hold, or
  avoid") and the maintain-an-existing-position gap.
- **AR-04 (receipt honesty — correction).** The propagation receipt above states it updates
  "the OWNER (this C3 contract) only" and lists the ten downstream surfaces for "sequenced
  realignment." **That is corrected:** the downstream surfaces WERE updated in the same
  session's cascade (and the follow-up `hold` pass). Read `controlling_sources_updated` as
  also including: the demand-read taxonomy + adjudication, demand-read core +
  first-demand-read-scope, buyer-proof packet, scan core, commission criteria, gate-closures
  proposal, offer hypothesis, proof charter, fragrance satellite, the foundation ontology,
  the product thesis, and the wedge — all carrying the new 7-verb set. **Genuinely not
  updated** (named, not forked): the ontology commission prompt and the c2-read-contract
  handoff (historical prompt artifacts), the B2B method-validation case-frames (a separate
  verb set / context), and the offer's venue-family substrate gate (AR-06 — pre-existing,
  separate patch). A repo-wide stale-search after this pass finds no live demand-read
  surface on the old `{act,phase,narrow,hold,defend}` / horizon vocabulary except the
  thesis Central Read #4 / 2026-06-14 mapping (superseded-original under their
  amendments); the C3 body below was reconciled to the 7-verb set (AR-03).
- **AR-03 (C3 body — RECONCILED post-review).** The **Required Behavior #4, cap rule,
  Interfaces, Acceptance Criteria, and Downstream Handoff** sections below were
  **reconciled** to this amendment's 7-verb flat set
  (`monitor, probe, commit, hold, scale, avoid, reduce`) with horizon accreting via
  monitoring — they no longer specify the superseded `{act,phase,narrow,hold,defend}` ×
  horizon `{commit,move}` interface. The body is now **consumable** and consistent with
  this amendment; its non-vocab logic (two-axis verdict, floor/ceiling cap-rule
  structure, consume-don't-reopen, INV-1) is unchanged. Its earlier observed-only
  transient-default / earned-durable phrasing is superseded by the 2026-06-23
  durable-demand projection clarification below.

## Amendment — 2026-06-23 (owner-directed): Durable Demand Is A Projection Call

Owner-directed in-thread. This **replaces the observed-only durable/transient
wording** that treated durable as demand that had already stayed strong. The
active rule is:

- **transient** = real, strong current-window demand whose durability is not
  called, or whose evidence supports decay;
- **durable** = real, strong demand with a named evidence-supported basis for
  projecting persistence over the relevant decision horizon;
- weak, attention-only, resonance-only, insufficient, or manufactured signals
  are **not** transient demand.

Observed post-trigger persistence remains valid evidence for durability, but it
is not the definition. Other admissible bases may include repeated costly
behavior, analogue history, post-trigger follow-through, org-motion corroboration,
or a monitored upgrade. C3 must state the basis in the reasoning trace; INV-1
still forbids a numeric persistence probability or computed decay curve.

```yaml
direction_change_propagation:
  doctrine_changed: >
    Durable demand is now encoded as a forward demand call — strong real demand
    with a named evidence-supported basis for projecting persistence over the
    relevant decision horizon — rather than a retrospective "stayed strong"
    observation. Transient demand is strong real current-window demand whose
    durability is not called or whose evidence supports decay; weak,
    attention-only, resonance-only, insufficient, or manufactured signals are
    not transient demand.
  trigger: product_doctrine
  related_triggers:
    - architecture_doctrine
  controlling_sources_updated:
    - docs/decisions/forseti_product_thesis_consumer_demand_v0.md
    - forseti/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md
    - forseti/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_adjudication_v0.md
    - forseti/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
    - forseti/product/spines/commission_signal_board/dispatch_rules/orca_demand_gate_run_commission_criteria_v0.md
    - forseti/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_structure_v0.md
    - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md
    - forseti/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md
    - forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md
    - forseti/product/spines/judgment/demand_read/core/judgment_spine_first_demand_read_scope_v0.md
    - forseti/product/spines/judgment/demand_read/grading/judgment_spine_demand_read_grading_rubric_v0.md
    - forseti/product/spines/judgment/demand_read/integrity/judgment_spine_manufactured_demand_detection_design_v0.md
    - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - forseti/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
    - forseti/product/satellites/fragrance/judgment_level1/satellite_skeleton/fragrance_level1_product_learning_satellite_skeleton_v0.md
  intentionally_not_updated: []
  stale_language_search: >
    rg -n "observed persistence|observed post-trigger|observed via monitoring|not predicted|cannot call durable|never asserted at t=0|durable is earned|persists past|stayed strong|transient-default|earned-durable"
    docs/decisions/forseti_product_thesis_consumer_demand_v0.md forseti/product/spines/foundation/demand_read_taxonomy forseti/product/spines/scanning/scan_core forseti/product/spines/commission_signal_board forseti/product/spines/product_lead/buyer_proof forseti/product/spines/judgment/demand_read forseti/product/spines/capture/core/contracts/obligation_contracts forseti/product/shared/projection_doctrine forseti/product/satellites
  stale_language_search_result: >
    Executed during 2026-06-23 delegated-review adjudication. The confirmed
    active stale hit outside the original spine-scoped search was the fragrance
    satellite skeleton's `transient-default` trace language; this patch updates
    that line. Remaining hits are this receipt/query, supersession history, or
    statements that observed persistence is one possible durability-projection
    basis rather than the definition.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not judgment-quality evidence
    - not implementation authorization
```


## Input Basis (accepted)

- **Owner-ADOPTED demand-read core** (Decision B, 2026-06-14): the C0–C4 core is
  the demand-read judgment procedure; **C3 emits the verdict + action ceiling.**
  This spec operationalizes that step; it does not re-derive the core.
- **Two-axis demand-state model** (settled, main #78 `c36e09c2`): durable/transient
  (persistence) + real/manufactured (integrity); "hollow" retired. C3 verdicts on
  this model.
- **Calling sequence** (taxonomy, owner 2026-06-14; clarified 2026-06-23): first
  call is **current-window transient unless a durability basis is already in the
  information set**; **durable is a named, evidence-supported projection that
  demand will stay strong over the decision horizon.**
- **C2 contract** (`SPEC_COMPLETE`, Rule 3 folded): C3 consumes C2's per-signal
  weighted reads (direction + reasoning + qualitative band + caveats) and the
  **persistence-axis discriminator findings Rule 3 routes to C3**; the
  **manufactured-axis** integrity defeaters are resolved **upstream** (C1 gate +
  C2 Rule 3), so C3 receives a **real** (or already-disqualified/held) input.
- **Action-ceiling cap rule** (buyer-proof packet, ratified): **floor** = gradeable
  costly behavior (can you act at all); **ceiling** = integrity/independence (how
  bold); material/irreversible commitment requires **≥2 independent converging
  origins**; single origin caps at hold/low-commitment; engagement/attention/resonance
  alone cannot carry Commit-grade and caps the ceiling.
- **Output surface** (far-half decision-object): C3 fills the `sealed_call`
  (`recommendation`, `confidence_band`, `signals_used`, `reasoning_trace`); the
  sealed C3/C4 + trace is the JSG-06 scoreable child.

## Required Behavior

When C3 runs over the C2-weighted allowed signals for a **real** (not
manufactured) demand under an active `decision_family` and Decision Frame (C0), it must:

1. **Emit a two-axis demand-state verdict.** State the **persistence** verdict —
   **durable** or **transient** — given the **real** integrity disposition resolved
   upstream. The verdict is on main's two-axis model; a single-axis or "hollow"
   verdict is non-compliant.
2. **Call durable only with a named persistence-projection basis.** **Durable
   requires evidence in the read's information set that supports strong demand
   persisting over the relevant decision horizon.** Observed post-trigger
   persistence is one possible basis, not the definition. A read whose information
   set contains strong current-window demand but no durability basis calls
   **transient** and acts **in-window**; weak, attention-only, or resonance-only
   input is not transient demand.
3. **Classify persistence-axis patterns here as transient, not as caps.** A
   persistence-axis pattern (resale/flip, event/one-time, scarcity/panic), carried
   in via C2 Rule 3 with its discriminator family, **reclassifies the read as
   transient** and sets a **horizon-matched, time-boxed** ceiling. It is **never**
   treated as a manufactured-axis cap (that axis is upstream). The trace must cite
   the discriminator that supports a transient classification.
4. **Emit an action ceiling — exactly one verb from** `{monitor, probe, commit, hold,
   scale, avoid, reduce}`, **matched to the demand-state**: durable → **commit** or
   **scale** as earned by the projection basis and ceiling; transient → reversible
   **commit** in-window or **reduce** on decay; manufactured → **avoid**. Horizon is
   not declared — it accretes via monitoring. The ceiling verb is the read's
   interpretation, justified per-case in the trace.
5. **Cap the ceiling by the weakest load-bearing evidence (floor/ceiling rule).**
   - A **material/irreversible** verb (**commit** or **scale**) requires **≥2 independent
     converging origins**; on a **single** independent origin the ceiling caps **below
     commit** (at **monitor / probe / hold**).
   - **Engagement / attention / resonance-only** evidence (no gradeable costly
     behavior) **cannot carry a Commit-grade** recommendation; it caps the ceiling.
   - The ceiling is **tiered by costly-behavior strength** (one gradeable instance →
     low-commitment, `monitor`/`probe`/`hold`; a corroborated pattern → higher) and is
     **never stronger than the weakest load-bearing evidence** supports.
   - A **costly or scaling position** is material and takes the ≥2-origin bar;
     `monitor` / `probe` / `hold` are the low-commitment band.
6. **Consume, don't re-adjudicate, the manufactured axis and the gate.** The
   manufactured-axis defeat (and the ratified G1/G2 Demand-Substrate Hard Gate) are
   settled upstream (C1 + C2 Rule 3). C3 receives a real-or-disqualified input and
   **does not reopen** either; if upstream disqualified/held the read, C3 emits no
   stronger verdict than that disposition allows.
7. **Fill the sealed_call output surface.** Populate `recommendation` (option +
   action shape consistent with the ceiling), `confidence_band` (a **qualitative
   band**, **reusing the contestant band-claim vocabulary — not a new one**),
   `signals_used` (each tagged with its `signal_id`), and a **required
   `reasoning_trace`** carrying the verdict, the durability-projection basis or
   transient basis, the ceiling verb, and **every cap reason** (independence
   count, costly-behavior strength, engagement/resonance-only). The sealed C3/C4 + trace is
   the JSG-06 scoreable child.
8. **Stay qualitative (INV-1).** The verdict, ceiling verb, and
   confidence_band are **qualitative classifications with reasons** — no number,
   score, formula, or deterministic table maps an independence-count, weight band,
   or signal strength to a ceiling. (The ≥2-origin bar is the ratified gate's
   **structural independence count**, consumed as a gate condition — not a computed
   weight.) `validation_status` caps at `product_learning` and travels with the read.

## Non-Goals

- **No manufactured-axis re-adjudication.** The integrity defeat and the G1/G2 gate
  are upstream (C1 + C2 Rule 3); C3 consumes their disposition, does not reopen it.
- **No numeric/ordinal ceiling or apply-rule.** No score, fraction, rank, threshold
  table, or formula mapping independence-count / weight band / signal strength → a
  ceiling verb. (INV-1; graduates only when the owner explicitly lifts no-scoring.)
- **No unsupported decay-curve prediction / transient-timing forecast.** C3 may
  state the qualitative basis for durable projection or transient decay, but it
  does not compute a decay window or persistence probability. The decay-curve
  capability does not exist.
- **No new confidence vocabulary.** `confidence_band` reuses the contestant
  band-claim shape by pointer; C3 mints none.
- **No beauty-specific verb-tiering.** Which verbs map to which ceiling in beauty
  (and the per-vertical discriminator *tells*) is **satellite** (vertical deck), not
  this core contract; C3 owns only the requirement that the mapping and the
  transient discriminator be cited in the trace.
- **No C2 re-weighting.** C3 consumes C2's weighted signals; it does not re-run the
  ledger read, the de-correlate/diverge sub-steps, or Rule 3.
- **No live-loop / monitoring behavior.** Seal-before-disclose, the monitor that
  earns or defeats the durability projection, and resolution are owned by the far-half
  shell; C3 is the single-read verdict step that fills the sealed_call.
- **No build/run beyond the authorized first by-hand read.** No row population, no
  runner, no automated scorer.

## Interfaces / Contracts

- **Inputs (read-only, by pointer):** the active `(decision_family, Decision Frame)`
  (C0); the **C2-weighted allowed signals** (each: direction, per-case reasoning,
  qualitative weight band, `signal_id`, travelled caveats); the **integrity
  disposition** (real / disqualified-or-held) from C1 + C2 Rule 3; the
  **persistence-axis discriminator findings** routed from C2 Rule 3.
- **Outputs:** the `sealed_call` slots — `recommendation`, `confidence_band`
  (qualitative band, contestant vocabulary), `signals_used` (each tagged
  `signal_id`), `reasoning_trace` (required) — plus the **demand-state verdict**
  (`durable | transient`, given `real`) and the **action ceiling** — one verb from
  (`monitor | probe | commit | hold | scale | avoid | reduce`); horizon is **not** a
  separate output, it accretes via monitoring.
- **Invariants honored:** INV-1 (qualitative, no scoring; `product_learning` cap
  travels); the **durable-projection-basis rule** (no durable without a named
  persistence basis in the information set); INV-6 (consume the ratified gate,
  don't reopen).
- **Boundary honored:** C3 fills the sealed surface only; it does not run the live
  monitor, predict decay, re-adjudicate the manufactured axis, promote a
  source-family, or lift a signal above its evidence ceiling.

## Acceptance Criteria

- **Two-axis verdict:** a read that emits a single-axis or "hollow" verdict, or omits
  the persistence (durable|transient) call, fails.
- **Durable-projection basis:** a read that calls **durable** without naming the
  evidence basis for projected persistence over the relevant decision horizon
  fails; observed persistence is one possible basis, not the definition.
- **Persistence-pattern routing:** a persistence-axis pattern (resale / event /
  scarcity) treated as a **manufactured cap** fails — it must classify the read
  **transient** with a time-boxed ceiling and **cite its discriminator**.
- **Ceiling vocabulary:** a ceiling verb outside `{monitor, probe, commit, hold, scale, avoid, reduce}`
  fails.
- **Independence cap:** a **material/irreversible** verb (`commit` or `scale`)
  emitted on a **single** independent origin fails (must cap below commit at
  `monitor`/`probe`/`hold` unless ≥2 converging independent origins).
- **Engagement/resonance-only cap:** a **Commit-grade** ceiling carried by
  engagement, attention, or resonance-only evidence (no gradeable costly
  behavior) fails.
- **Weakest-evidence cap:** a ceiling stronger than the weakest load-bearing evidence
  supports fails.
- **Sealed_call fill:** a read that omits `recommendation`, `confidence_band`,
  `signals_used` (tagged `signal_id`), or `reasoning_trace` fails; a `confidence_band`
  stated as a number or a newly-minted vocabulary fails.
- **INV-1 disqualifier:** an auditor can find **no** step where the ceiling verb or
  the confidence_band is computed from a number/formula/threshold; a computed ceiling
  fails.
- **Trace content:** the trace carries the verdict + persistence basis (or its
  absence) + ceiling + **every cap reason**; a verdict or ceiling that moves
  without a stated reason fails.
- **Consume-don't-reopen:** a read that re-adjudicates the manufactured-axis defeat
  (settled at C1/C2) or reopens the G1/G2 gate fails.

## Open Questions

- **Contestant `confidence_band` vocabulary — DEFERRED (safe).** The exact band
  levels are owned by the contestant / decision-object contract; this spec requires
  only that C3 **reuse** that vocabulary (no new one) and state a qualitative band.
  Deferring the level list cannot change C3's behavior, only which label a band
  carries.
- **Per-vertical discriminator *tells* and verb→ceiling mapping — DEFERRED (safe).**
  Satellite-owned (the beauty deck). C3 owns the *requirement* that a transient
  classification cite a discriminator and that the verb→ceiling mapping be justified;
  the specific beauty tells are not core.
- **Durability projection threshold for the transient→durable upgrade — DEFERRED
  (safe).** Owned by the far-half monitoring loop, not the single-read verdict step.
  A first read may call durable only when its information set already carries a
  named persistence-projection basis; the monitored upgrade threshold remains a
  far-half concern.

## Downstream Handoff

```yaml
spec_handoff:
  status: SPEC_COMPLETE_READY_FOR_SCOPING
  required_behavior: >
    C3 turns the C2-weighted allowed signals (for a real, not-manufactured demand)
    into a two-axis demand-state verdict (durable | transient, given real) and an
    action ceiling (one verb from monitor | probe | commit | hold | scale | avoid | reduce)
    matched to the demand-state (durable -> commit/scale as earned from a named
    persistence-projection basis; transient -> reversible commit or reduce on
    decay; manufactured -> avoid; horizon accretes via monitoring, not declared).
    It treats transient as strong current-window demand, not weak signal; durable
    requires a named basis in the information set (observed persistence is one
    basis, not the definition); classifies persistence-axis patterns (resale /
    event / scarcity, routed from C2 Rule 3 with a cited discriminator) as
    transient, not as caps; caps the ceiling by the weakest load-bearing evidence
    (>=2 independent converging origins for a material verb, commit or scale; single
    origin -> below commit at monitor/probe/hold; engagement/resonance-only cannot carry
    commit/scale-grade); consumes (does not reopen) the manufactured
    axis and the ratified G1/G2 gate; fills the sealed_call (recommendation,
    qualitative confidence_band in the contestant vocabulary, signals_used tagged
    by signal_id, required reasoning_trace carrying verdict + persistence basis +
    ceiling + every cap reason); and stays qualitative (INV-1, no number).
  non_goals:
    - manufactured-axis re-adjudication or G1/G2 reopen (upstream C1 + C2 Rule 3)
    - numeric/ordinal ceiling or deterministic apply-rule from independence-count/strength (INV-1)
    - decay-curve prediction / unsupported transient-timing forecast (durability projection basis required; exact decay timing deferred)
    - new confidence vocabulary (reuse the contestant band-claim shape)
    - beauty-specific verb-tiering and per-vertical discriminator tells (satellite)
    - C2 re-weighting (consume C2's output; do not re-run the ledger/de-correlate/diverge/Rule 3)
    - live-loop / monitoring / resolution behavior (far-half shell)
    - any build, row population, runner, or automated scorer beyond the authorized first by-hand read
  interfaces_contracts:
    - inputs_read_only: [active (decision_family, Decision Frame), C2-weighted allowed signals (direction + reasoning + qualitative band + signal_id + caveats), integrity disposition (real | disqualified/held) from C1+C2, persistence-axis discriminator findings from C2 Rule 3]
    - outputs: [demand_state_verdict (durable|transient, given real), action_ceiling (monitor|probe|commit|hold|scale|avoid|reduce; horizon accretes via monitoring, not a declared output), sealed_call{recommendation, confidence_band, signals_used, reasoning_trace}]
    - invariants: [INV-1 (qualitative, no scoring; product_learning cap travels), durable-projection-basis rule, INV-6 (consume the gate, don't reopen)]
  acceptance_criteria:
    - two-axis verdict present (no single-axis / hollow verdict)
    - durable-projection-basis rule (no durable without a named persistence basis in the information set)
    - persistence-pattern routed to transient with a cited discriminator (not a manufactured cap)
    - ceiling drawn from {monitor, probe, commit, hold, scale, avoid, reduce}
    - independence cap (material verb commit/scale needs >=2 converging origins; single origin -> below commit at monitor/probe/hold)
    - engagement/resonance-only cap (no Commit-grade on attention/resonance-only evidence)
    - weakest-load-bearing-evidence cap
    - sealed_call filled (recommendation + qualitative confidence_band + tagged signals_used + reasoning_trace)
    - INV-1 disqualifier (no number/formula-computed ceiling or band)
    - trace carries verdict + persistence basis + ceiling + every cap reason
    - consume-don't-reopen (no manufactured re-adjudication, no G1/G2 reopen)
  deferred_open_questions:
    - contestant confidence_band vocabulary (decision-object owned; consumer reuses by pointer)
    - per-vertical discriminator tells + verb->ceiling mapping (satellite / beauty deck)
    - durability projection threshold / monitored upgrade rule (far-half monitoring loop; first reads may call durable only with a named basis in their information set)
  review_timing_advisory:
    adversarial_review: recommended
    highest_value_checkpoint: after_artifact_pre_implementation
    review_target: forseti/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md
    why_this_checkpoint: >
      C3 is the step whose verdict + ceiling the first by-hand read's whole claim
      rests on, and it encodes INV-1 at a tempting crossing point — turning an
      independence-count and a costly-behavior strength into a ceiling verb. A flaw
      here would let a deterministic ceiling rule slip in under cover of
      "qualitative," or let a first read overclaim durable. Review before the
      first-read scope relies on it.
  scoping_may_rely_on: >
    the two-axis verdict contract; the durable-projection-basis rule; the
    persistence-pattern -> transient routing; the {monitor,probe,commit,hold,scale,avoid,reduce}
    ceiling vocabulary; the floor/ceiling cap rule (>=2 converging origins,
    engagement/resonance-only cap, weakest-evidence cap); the consume-don't-reopen boundary;
    the sealed_call output surface; and INV-1. Open: the contestant band vocabulary,
    the per-vertical discriminator tells, and the live-monitor persistence threshold
    (all deferred-safe, none blocking a first read).
```

## Source-Read Ledger

- `forseti/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md`
  — the core whose C3 this specifies (C3 step shape; two-axis C3 verdict; persistence
  patterns classified at C3; owner-ADOPTED Decision B). Compare target: `C1 — Allow`
  + C3 two-axis verdict present on `origin/main` (#125 squash `2b45001b`). reread-required.
- `forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md` — the C2
  step C3 consumes; Rule 3 routes persistence-axis patterns to C3. Compare target:
  `Rule 3 — Risk-State Weighting` present on `origin/main` (#124 squash `3ccc86ef`).
  reread-required.
- `forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md` — the action-ceiling cap
  rule (floor vs ceiling; ≥2 converging origins for material commitment; engagement/resonance-only
  caps the ceiling; defend not auto-low-commitment; Scoring engines on the do-not-build
  list). On `origin/main` (re-grounded #130). reread-required.
- `forseti/product/spines/judgment/learning_loops/far_half/prospective_decision_loop_target_architecture_v0.md` —
  the sealed_call output surface (recommendation / confidence_band / signals_used /
  reasoning_trace). On `origin/main`. reread-required.
- `forseti/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md` — the read grammar
  (two-axis model + calling sequence + read types) C3 verdicts in. Status
  `PROPOSED_PENDING_OWNER_ADJUDICATION` on `origin/main`. reread-required; the grammar
  is not yet owner-adjudicated as operative.

## Claim Classification

```yaml
judgment_spine_claim_classification:
  evaluated_claim_surface: C3 verdict + action-ceiling contract (binding-side behavior/contract spec)
  source_quality_state: design/control artifacts only (owner-adopted core architecture + C2 contract + ratified buyer-proof cap rule + far-half sealed_call + taxonomy, read fresh on origin/main); no real read, no run
  execution_quality_state: no C3 verdict executed, no ceiling emitted, no case run
  closeout_state: no_durable_evidence
  claim_cap: design input / product-learning context only
  weakest_missing_or_failed_gate: no C3 read exists to test against; the first by-hand read against this contract is not yet run; review of this spec not yet run
  receipt_artifact_or_gap: first real test comes from the authorized first by-hand demand read emitting a C3 verdict + ceiling against this contract
  non_claims:
    - not validation unless separately proven
    - not readiness unless separately proven
    - not buyer proof unless the buyer-proof receipt is complete
    - not judgment-quality evidence unless the judgment-quality receipt is complete
```

## Non-Claims

- Behavior/contract spec only; binds no real row, runs no case, edits neither the C1
  gate, the C2 contract, the FROZEN conductor, nor the far-half loop.
- Authorizes no scoring engine, automated scorer, runner, or storage. INV-1 holds: the
  verdict, horizon, ceiling, and confidence_band are qualitative classifications the
  read justifies, never numbers it computes.
- Mints no evidence-ladder or confidence vocabulary; reuses `decision_family` /
  `signal_id` / the two-axis states / the action-ceiling vocab / the contestant
  band-claim shape from the architecture, taxonomy, buyer-proof packet, and far-half loop.
- **Stabilizes, does not change, the adopted C3 step.** C3's shape is already
  owner-ADOPTED (Decision B); this spec specifies it to contract depth. It is PROPOSED
  and not yet owner-adopted as the operative C3 contract; on adoption it owes a dated
  pointer via the Doctrine-Change Propagation Contract
  (`.agents/workflow-overlay/source-of-truth.md`). The 2026-06-23 durable-demand
  projection clarification carries the propagation receipt above.
- A C3 verdict is `product_learning` evidence about a demand read — never validated,
  decision-grade, buyer-proven, or judgment-quality.
```text
This is advisory design input only. It is not a verdict, not implementation
authority, and not proof of readiness.
```
