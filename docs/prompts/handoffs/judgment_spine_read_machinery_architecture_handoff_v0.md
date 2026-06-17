# Handoff Packet — Judgment-Spine Read-Machinery Architecture ("one core, two shells")

```yaml
retrieval_header_version: 1
artifact_role: Handoff packet (cold cross-lane state transfer; workflow-handoff output)
scope: >
  Transfers the not-yet-started "one judgment core, two shells" demand-read
  machinery architecture (object C) to a fresh goal-framed lane. Cold-reader
  self-contained; confirm-don't-trust load contract. The sender thread keeps the
  demand-gate definition closures.
use_when:
  - Picking up the Judgment-Spine read-machinery architecture pass in a fresh lane.
authority_boundary: retrieval_only
applied_contract: authored via workflow-handoff (packet owner); courier prompt deferred to workflow-prompt-orchestrator.
amendments:
  - 2026-06-13 owner closed Open Decision A (distillation checkpoint #3 = weighting) and revised the phased distillation tail to diagnose -> prove -> generalize -> install. Recorded into this packet from the demand-gate (sender) thread post-compact; design status unchanged (still a PROPOSED architecture for the fresh lane to re-derive, now with #3 set and the PROVE gate specified).
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-13
- created_by_lane: Orca demand-gate thread (Claude Opus-class); provenance only, not authority
- workspace: C:\Users\vmon7\Desktop\projects\orca
- handoff_path: docs/prompts/handoffs/judgment_spine_read_machinery_architecture_handoff_v0.md
- expected_branch: ecr-sp3-timing-deriver-slice1 (SENDER's branch; the fresh lane should spin up its OWN worktree/branch off `origin/main` per AGENTS isolation, NOT continue on this branch)
- expected_head: aed85c4d012bea648e601403f865595f1013b4ea
- expected_dirty_state_including_handoff_file: sender thread left these dirty/untracked — `M docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md`; `?? docs/product/product_lead/orca_demand_gate_definition_closures_proposal_v0.md`; `?? docs/review-outputs/adversarial-artifact-reviews/demand_gate_definition_closures_cross_vendor_adversarial_artifact_review_v0.md`; and this handoff file is newly untracked.
- load_rule: confirm-don't-trust — re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: Orca's durable-vs-hollow demand calls become trustworthy enough that a decision owner allocates (and eventually pays) against them, on an inherently manipulable public substrate — trust earned by method, not asserted. (Carried from the in-thread goal frame; same durable goal.)
- anchor_goal: Design Orca's **live demand-read judgment machinery** (object "C") — the procedure that turns *admitted* signal into a verdict + action ceiling — as a PROPOSED architecture object. Specifically the "one judgment core, two shells" shape (below). Design only; no implementation, no scoring engine.
- success_signal: A PROPOSED architecture object a downstream lane could implement, that (a) names the core's steps and the two shells; (b) states the phased-distillation tail + the deck and its survival kernel; (c) incorporates distillation checkpoint #3 = **weighting** (owner-set 2026-06-13) and the **diagnose -> prove -> generalize -> install** phased tail; (d) keeps the no-scoring-engine and don't-graft-onto-the-backtest-conductor guards intact; (e) places each piece on the core-Judgment-doctrine vs beauty-satellite boundary. NOT success: building a scoring engine, editing the existing conductor, or producing implementation.

## Open Decision / Fork

- decision A — **distillation checkpoint #3 — RESOLVED by owner 2026-06-13.**
  - resolution: checkpoint #3 is **weighting** — per **vertical**, what weight each source/signal should be assigned, learned from **past (backtested) cases**. (Owner verbatim: "YES WEIGHTING ... most importantly for x vertical what weight should be assigned based on past cases.") This is the deck's per-vertical calibration output, consumed by the core's weight step; it stays LLM-in-session / qualitative per the Drift Guard (no scoring engine; numeric weights only when the owner lifts that boundary).
  - already constrained: checkpoints 1 (judgment — HAVE) and 2 (counterfactual "what evidence would let us decide better") were already set; #3 now closes the set of three.
  - owner of the call: owner — **DECIDED**. No longer open; the architecture pass builds #3 = weighting in, it does not re-derive whether to have it.
- decision B — **extend the existing backtest conductor, or author a sibling "demand-read conductor"?**
  - options: (i) add the live-read machinery as a sibling operating model; (ii) leave the existing JSG-01..10 conductor untouched and have it only *route to* the new owner-source via one predicate row.
  - already off the table: grafting judgment-computing logic INTO the JSG-01..10 conductor (violates its No-Authority Invariant — see Drift Guard).
  - owner of the call: architecture-planning lane → owner sign-off.
  - recommendation: sibling surface; the existing conductor is a backtest/quality sequencer, this is a live-read machine. They share the ontology vocabulary, not the gate logic.
- decision C — **is the distillation-tail addition to the backtest path its own architecture pass?** Likely yes (it changes a Round-19-reviewed artifact's tail); treat as a scoped sub-pass.

## Drift Guard

- **No scoring engine.** The weighting/verdict is LLM-done IN-SESSION (qualitative, explained), NOT a built/automated scoring pipeline. The buyer-proof packet forbids "scoring engines / automated scoring" at this stage. Numeric/calibrated weights graduate ONLY when wind-caller calibration data exists AND the owner explicitly lifts the no-scoring boundary. Building a scoring model now is the primary drift to avoid.
- **Do not graft onto the existing conductor.** docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md has a hard No-Authority Invariant (it reads receipts, never computes judgment/weights/scores) and Route-Don't-Restate. Judgment-computing logic cannot live in it. It is Round-19 reviewed; any touch needs the same delegated/adversarial review discipline.
- **The blind/isolation wrapper is backtest-only.** The live shell deliberately drops it (no outcome to hide). Do not import the blind-exam discipline into the live path, and do not drop it from the backtest path.
- **Spine placement.** Core (independence concept, two-part weight→verdict shape, costly-behavior-as-truth-test, the phased-distillation pattern) = core Judgment doctrine. The beauty venue/costly-behavior instances + verb-tiering calibration = beauty satellite. Don't promote satellite specifics into core.
- **Do not re-litigate Task 2.** The demand-gate P2/P3/P4 decisions are owner-RATIFIED (2026-06-13) and live in the demand-gate thread. This lane CONSUMES them (the gate is the admissibility front-door that feeds this machinery); it does not reopen them.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (read AGENTS.md + `.agents/workflow-overlay/README.md` first, per AGENTS).
- targets to enter the ladder:
  - docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md — the existing backtest conductor (its invariants bound what this machinery may/may not do).
  - docs/product/foundation/core_spine_v0_data_and_cleaning_spine_boundary_v0.md — the canonical spine map (Judgment Spine owns Signal Integrity / Signal Use Classification / Decision Strength / Action Ceiling; core vs satellite).
  - docs/product/product_lead/orca_demand_read_taxonomy_v0.md — signal layers, wind callers, convergence/divergence reads, costly-behavior catalog (the proto-ontology this machinery uses).
  - docs/product/product_lead/orca_buyer_proof_packet_v0.md — the Demand-Substrate Hard Gate (the admissibility front-door) + the no-scoring/no-automated-scoring boundary this machinery must respect.
  - docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md — DISPATCHED ontology backbone; carries the `derived_from`/`diverges_from` link types this machinery's de-correlation + divergence rely on.
- already loaded (weak orientation, freshness-marked; NOT authority): all of the above were read in the sender thread on 2026-06-13; treat as stale pointers, re-read.
- must load first (before any strict/actionable step): AGENTS.md + overlay README; then the conductor + the spine boundary doc (they bound the invariants).
- load rule: re-run progressive source loading per the overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- **One core, two shells (the whole design).** Core (market-agnostic): weight sources (de-correlate via `derived_from`; map divergence via `diverges_from`) → verdict + action ceiling → counterfactual. Backtest shell = blind/isolate → core → score vs known outcome → phased distillation. Live shell = core → verdict + counterfactual → defer scoring; when the outcome lands it re-enters as a backtest case. This is core/satellite on a MODE axis, separate from the market/vertical satellite axis.
  - decided in: this sender thread (chat-only; NOT yet in any file — this packet is its first durable capture).
  - compare target: none (no prior artifact) — treat as the sender's proposal to be re-derived/validated in goal-framing, not as settled authority.
- **Phased distillation tail (owner-revised 2026-06-13).** Per checkpoint: **diagnose → prove → generalize → install-as-dated-card**, under the venue-card-set survival kernel (hard cap, review dates, fail-soft, dated amendments). The **PROVE** phase is an empirical gate inserted before a lesson earns generalization/installation: re-run the **same case** on a **fresh instance of the same model family**, armed with the candidate lesson, and check whether its answer is **materially better**. Same family is deliberate — it isolates the lesson's effect rather than confounding it with a model-capability change; the fresh instance avoids contamination from the original run's reasoning. Pass (materially better) → generalize → install as a dated card; fail → the "lesson" did not earn a card (no install). Output = a distillation DECK that feeds the core's weighting; the deck is the membrane between backtest (produces cards) and live (consumes cards); it is where the wind-caller calibration moat lives.
  - verify pointer: the survival-kernel pattern is in docs/product/foundation/beauty_venue_card_set_v0.md (compare target: sha256[:16] 65E22CDAE5EDE781 as of 2026-06-13; reread-required).
- **Three distillation checkpoints:** (1) judgment — HAVE; (2) counterfactual "what evidence would let us decide better" — the new tail; (3) **weighting** — per vertical, what weight each source/signal earns, learned from past/backtested cases (owner-set 2026-06-13; was the open slot). All three run through the diagnose → prove → generalize → install phases and feed the deck's per-vertical calibration.
- **P2/P3/P4 are owner-RATIFIED (Task 2).** This machinery consumes the gate; it does not reopen them.
  - verify pointer: docs/product/product_lead/orca_demand_gate_definition_closures_proposal_v0.md (compare target: sha256 006CD6ACE65BF45D9E3209531ED6BFC0F4206DDB688081D40F445D5D6137FEFB; reread-required). NOTE: this file is UNTRACKED on the sender branch — a fresh lane off origin/main will NOT see it; obtain it from this branch or wait for it to land.

## Active Objective

Design the live demand-read judgment machinery ("C") — the "one core, two shells" procedure — as a PROPOSED architecture object via a goal-framed architecture pass. Not started; the design above is the sender's converged proposal, to be re-derived and hardened, not inherited as settled.

## Exact Next Authorized Action

1. Spin up a fresh worktree/branch off `origin/main` (AGENTS isolation; do NOT continue on the sender's `ecr-sp3-timing-deriver-slice1` branch).
2. Read AGENTS.md + `.agents/workflow-overlay/README.md`, then the conductor + spine-boundary doc (the invariant bounds).
3. Run `workflow-goal-framing` for this architecture pass (the anchor_goal above is a proposal — re-frame it, surface tensions).
4. Then `workflow-architecture-planning`: take the "one core, two shells" + phased-distillation design as the candidate; compare options for decisions A/B/C; produce the PROPOSED architecture object; place each piece on the core/satellite + spine boundary.
5. Stop condition: a PROPOSED architecture object meeting the success_signal; no implementation, no scoring engine, no edit to the existing conductor.

## Authority And Source Ledger

- Repository instructions: AGENTS.md (+ CLAUDE.md shim) — reread-required.
- Overlay authority: `.agents/workflow-overlay/` (README, source-loading, source-of-truth, decision-routing) — reread-required.
- User constraints: design only; no scoring engine; don't graft onto the backtest conductor; hold checkpoint #3 open; don't reopen the ratified gate decisions.
- Source-read ledger:
  - `docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md`
    - Role: the existing backtest conductor; its No-Authority + Route-Don't-Restate invariants bound this machinery.
    - Load-bearing: yes
    - Compare target: reread-required (Round-19; large file; verify the invariants section + JSG gate table).
    - Reuse rule: read fresh; do not edit; treat as the boundary, not the host.
  - `docs/product/foundation/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
    - Role: canonical spine map (core vs satellite; Judgment Spine ownership of integrity/signal-use/decision-strength).
    - Load-bearing: yes
    - Compare target: reread-required.
    - Reuse rule: read fresh; cite for spine placement.
  - `docs/product/product_lead/orca_demand_read_taxonomy_v0.md`
    - Role: signal layers, wind callers, convergence/divergence, costly-behavior catalog (the proto-ontology).
    - Load-bearing: yes
    - Compare target: sha256[:16] BC478D890419B2B6 (as of 2026-06-13); reread-required.
    - Reuse rule: read fresh; PROPOSED-strength.
  - `docs/product/product_lead/orca_buyer_proof_packet_v0.md`
    - Role: the Demand-Substrate Hard Gate (admissibility front-door) + the no-scoring boundary.
    - Load-bearing: yes
    - Compare target: sha256[:16] 732C65BEBFC31DA1 (working-tree, LF, as of 2026-06-13); reread-required. NOTE the origin/main copy differs by one front-matter pointer line (PR #40) — instrument text identical.
    - Reuse rule: read fresh; the gate FEEDS this machinery.
  - `docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md`
    - Role: dispatched ontology backbone; carries `derived_from`/`diverges_from`.
    - Load-bearing: no (reference)
    - Compare target: sha256[:16] 16068397505D8C8A (as of 2026-06-13); committed on the sender branch, NOT on origin/main; reread-required.
    - Reuse rule: orientation; this machinery uses the link semantics it names.
- Source gaps: the demand-gate proposal + this thread's design are UNTRACKED on the sender branch — a fresh lane off origin/main cannot see them until they land or are couriered.
- Strict-only blockers: none for design; any implementation/scoring claim is out of scope and blocks.
- Not-proven boundaries: nothing here is validated, ready, or implementation-authorized.

## Current Task State

- Completed: the "one core, two shells" + phased-distillation + deck design converged conceptually (in chat).
- Partially completed: 3 distillation checkpoints now all set (3 = weighting, owner-set 2026-06-13); phased tail now diagnose → prove → generalize → install.
- Broken or uncertain: decisions A/B/C unresolved; the whole design is a proposal, not a goal-framed/architecture-planned object.

## Workspace State

- Branch: ecr-sp3-timing-deriver-slice1 (sender's; fresh lane should NOT use it).
- Head: aed85c4d012bea648e601403f865595f1013b4ea (advanced from session-start 46b8371 during the sender thread; observed, cause not recorded).
- Dirty/untracked before handoff: the 3 demand-gate-thread files listed in Load Contract.
- Dirty/untracked after writing this handoff file: this file is newly untracked.
- Target files/artifacts: NONE yet for Task 1 (architecture not started).
- Related worktrees/branches: a sender-created worktree `orca-gate-paper-check-wt` exists for an UNRELATED commission (the gate paper-check); not Task 1's.

## Changed / Inspected / Tested Files

- None authored for Task 1. (The demand-gate files were authored for Task 2 and are reference-only here.)

## Frozen Decisions

- The "one core, two shells" decomposition and the no-scoring-engine / don't-graft-onto-the-conductor guards are the sender's locked design intent for this lane.
  - Evidence: this packet + the drift guard; the conductor's invariants; the buyer-proof packet's no-scoring boundary.
  - Consequence: the architecture pass works within these; it may refine the core's internals but not violate the guards.
- Distillation checkpoint #3 = **weighting** (per vertical, learned from past cases). Owner-decided 2026-06-13.
  - Evidence: owner statement in the demand-gate thread post-compact ("YES WEIGHTING ... for x vertical what weight should be assigned based on past cases").
  - Consequence: the set of three checkpoints is closed; the architecture builds #3 in. It stays LLM-in-session / qualitative until the owner lifts the no-scoring boundary.
- Phased distillation tail = **diagnose → prove → generalize → install**, with PROVE = same-case re-run on a fresh same-family model armed with the lesson, kept only if materially better. Owner-decided 2026-06-13.
  - Evidence: owner statement post-compact ("phase b - prove ... run the same case on a new model same family but with that lessons, see if their answer is materially better or not").
  - Consequence: a candidate lesson cannot be generalized or installed as a card until it passes the PROVE gate; this is the empirical guard against installing unproven lessons.

## Mutable Questions

- Extend conductor vs sibling (decision B) — what would resolve it: the architecture-planning option comparison + owner sign-off.

## Superseded / Dangerous-To-Reuse Context

- The earlier "TWO conductors" framing.
  - Why superseded: refined to "one core, two shells" (one judgment core; backtest and live are mode-shells around it). Reusing "two conductors" would over-build.
  - Current replacement: the one-core-two-shells design above.
- Early ASCII/chat sketches of the architecture.
  - Why dangerous: incomplete/flattened (they omitted the distillation phasing).
  - Current replacement: this packet's Inherited Context design.

## Commands And Verification Evidence

- None material — this is a design handoff; no commands gate the next action.

## Blockers And Risks

- Referenced design + gate files are untracked/branch-only.
  - Evidence: git status (Workspace State).
  - Likely next action: the fresh lane re-derives the design from this packet (treated as a proposal) + reads the durable bounding sources (conductor, spine boundary, taxonomy, gate) fresh; obtain the untracked files from this branch if needed.
- No calibration data for weights.
  - Evidence: wind-caller calibration is a future asset (taxonomy).
  - Likely next action: keep weighting qualitative/in-session; defer numeric.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: branch/head (expect a DIFFERENT fresh branch off origin/main, not aed85c4); the four bounding sources (conductor, spine boundary, taxonomy, gate) by fresh read against their compare targets; the ontology commission's link types.
- Compare targets: the sha256[:16] values in the ledger; reread-required entries must be re-read.
- Load outcomes: REUSE only if the bounding-source invariants still hold; STALE_REREAD_REQUIRED if the conductor/spine docs moved; BLOCKED_UNVERIFIABLE if the untracked design/gate files can't be obtained and a strict claim depends on them.
- Sources to reread if drift: the conductor + spine boundary (they bound the whole design).

## Do Not Forget

- This machinery CONSUMES the demand gate (admissibility) and the ratified P2/P3/P4 — it does not reopen them.
- The single most expensive mistake here is building a scoring engine; keep it LLM-in-session and qualitative until the owner lifts the boundary.
