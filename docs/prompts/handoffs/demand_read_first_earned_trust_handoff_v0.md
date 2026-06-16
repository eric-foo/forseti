# Handoff Packet — Demand-Read Lane: next horizon (first earned trust)

```yaml
retrieval_header_version: 1
artifact_role: >
  Handoff packet (cold cross-lane state transfer; workflow-handoff output) —
  transfers the Orca demand-read judgment lane to a fresh lane after the C2 Rule 3
  reground + C1 Admit→Allow rename + durable-vs-hollow→two-axis propagation landed
  on main. The receiver advances the lane toward its next horizon (first earned
  trust), gated on the owner's design-tier-vs-build-tier decision.
scope: >
  Cold-reader self-contained. The demand-read *method* is now coherent and on
  main, but PROPOSED/product_learning and entirely unbuilt/unvalidated. This packet
  carries the goal frame, the open horizon decision, the drift guards, and the
  source-read ledger (compare targets on origin/main) the next lane needs.
authority_boundary: retrieval_only
applied_contract: authored via workflow-handoff; courier prompt deferred to workflow-prompt-orchestrator.
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-15
- created_by_lane: Orca demand-read spine CA thread (Claude Opus-class) operating from the primary repo on stale `ecr-sp3-timing-deriver-slice1`; provenance only, not authority
- workspace: C:\Users\vmon7\Desktop\projects\orca
- handoff_path: docs/prompts/handoffs/demand_read_first_earned_trust_handoff_v0.md
- expected_branch (sender primary): ecr-sp3-timing-deriver-slice1 — STALE scratch; the receiver spins its OWN worktree off `origin/main`, NOT this branch
- expected_head (sender primary): 0fc58cfe; **`origin/main` is at e0b939a2** (the demand-read work landed here)
- expected_dirty_state_including_handoff_file: ~25 untracked on the sender's `ecr-sp3` working tree; this handoff file is newly untracked there. It will NOT travel to a worktree off `main` — read it by the absolute path above while it exists, or have it couriered/committed into the new lane.
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority

## Goal Handoff

- long_term_goal: >
    Orca's durable-vs-transient demand calls become trustworthy enough that a
    decision owner allocates (and eventually pays) against them on a manipulable
    public substrate — trust earned by method, not asserted.
- anchor_goal: >
    The demand-read judge moves past coherent-but-unbuilt to its first earned
    trust — the durable/transient/manufactured call backed by a ratified+completed
    method or a first honestly-graded real read, not more doctrine.
- success_signal:
    core_success:
      owner_observable: >
        Something that visibly advances the method past "proposed-and-unbuilt" — a
        ratified grammar + C0/C1/C3/C4 specified to C2's depth, or Orca's first
        by-hand demand read on real data with an honest grade — not a 4th design doc.
      output_fit: >
        Makes the durable/transient/manufactured call more trustworthy (closes a
        named method gap or yields first real evidence) and states plainly what it
        does and does not prove.
      boundary: >
        More design docs, PR merges, or tool runs are not success; no
        validation/decision-grade/buyer-proof claim counts unless earned via its gate.
      drift_cue: >
        Polishing/multiplying doctrine while the method stays unbuilt/untested, or
        restating product_learning design as validation/readiness.
    secondary_success_signals:
      - INV-1 (no scoring engine) and the G1/G2 gate stay intact as the method advances.
      - Claims stay honestly tiered (product_learning until a gate earns more).
- status: user_stated (owner goal, framed via workflow-goal-framing 2026-06-15)

## Open Decision / Fork

- decision: **Which horizon should the next demand-read lane optimize for?**
  - options:
    - **(a) Close the design tier** — owner-adjudicate/ratify the read-grammar (taxonomy is still `PROPOSED_PENDING_OWNER_ADJUDICATION`), specify C0 Frame / C1 Allow / C3 Verdict+Ceiling / C4 Counterfactual to the depth C2 already has, and finish the open distillation re-run. Lower risk; no build gate; produces a *complete* method.
    - **(b) Cross to the build/proof tier** — populate the signal-reliability ledger with real rows and run the first by-hand C2 demand read on real data, honestly graded. This is what first produces *evidence* rather than doctrine — but it is **owner-gated** (build/run authorization + the conductor run-gate) and depends on the ledger being populatable.
  - already constrained / off the table: the two-axis demand-state model is settled (#78) and Rule 3 is folded (#124) — do not re-litigate either. INV-1 (no scoring engine) holds. The ratified G1/G2 / Demand-Substrate Hard Gate is consumed, not reopened.
  - trade-offs: (a) risks producing more correct-but-unbuilt doctrine (the drift_cue); (b) is higher-value toward the long-term goal but needs an owner build-gate lift and real data, and a premature read could overclaim.
  - owner of the call: **owner (Eric)**. The receiver proposes; the owner picks the horizon.
  - recommendation (sender, soft — owner decides): the highest-compounding move toward "trust earned by method" is **(b)** — one by-hand C2 read against a populated ledger is the first thing that yields evidence instead of doctrine. But take (b) only once the owner lifts the build gate and the ledger is populatable; otherwise close the *smallest* (a)-tier gaps that block a read (a specified C3 verdict + a minimally-populatable ledger), then cross.

## Drift Guard

- **Work off `origin/main` (@ e0b939a2 or later), in a FRESH worktree.** The sender's primary repo is on the STALE `ecr-sp3-timing-deriver-slice1`; do not work there.
- **The reground/rename/propagation is ALREADY ON MAIN — do not re-do or re-merge it.** PRs #124/#125/#126/#130 are MERGED (squash SHAs in Commands section). C1 is `Allow`, Rule 3 is folded, "durable-vs-hollow" is retired on the live docs.
- **Build/run is owner-gated.** No real ledger rows, no by-hand C2 read, no population/run without an explicit bounded owner authorization in the current turn. Design/docs is the default; the build crossing (option b) needs the owner's word.
- **INV-1 — no scoring engine, no numbers, no formula.** Weighting stays qualitative (classification + reason).
- **Consume, don't reopen:** the ratified G1/G2 / Demand-Substrate Hard Gate (admissibility) and the settled two-axis model.
- **Latent regression to NOT propagate from:** the 3 PROPOSED `*_consumer_demand_revision_v0` variants (buyer-proof, offer, charter) still carry "durable-vs-hollow"; if adopted as-is they re-introduce the retired frame. Re-ground them before/at adoption — do not treat them as the current frame.
- **Claims stay `product_learning`.** Nothing here is validated, decision-grade, or buyer-proven; no buyer has paid.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (read `AGENTS.md` + `.agents/workflow-overlay/README.md` first). Judgment-Spine read pack + the demand-read taxonomy are the entry.
- targets to enter the ladder (on `origin/main`): `docs/product/product_lead/orca_demand_read_taxonomy_v0.md`; `docs/product/judgment_spine/judgment_spine_demand_read_machinery_architecture_v0.md`; `docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md`; `docs/product/judgment_spine/demand_read_core_adoption_and_ledger_first_direction_v0.md`; `docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md`; `docs/product/product_lead/orca_buyer_proof_packet_v0.md` (the gate).
- already loaded (weak orientation; NOT authority): the sender authored/landed the reground+rename+propagation this session and read all of the above on their lane branches before merge; re-read fresh on `origin/main`.
- must load first (before any strict/actionable step): `AGENTS.md` + overlay README; then the taxonomy + C2 read-contract + core architecture on `origin/main`.
- load rule: re-run progressive source loading per the overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- **Two-axis demand-state model** (durable/transient persistence + real/manufactured integrity; "hollow" retired). Decided via PR #78 (`c36e09c2`). Verify: `git merge-base --is-ancestor c36e09c2 origin/main` exits 0; reread the taxonomy. reread-required.
- **The demand-read core C0–C4** ("one core, two shells": C0 Frame → C1 **Allow** (gate) → C2 Weight → C3 Verdict+Ceiling → C4 Counterfactual). Owner-ADOPTED (Decisions B + D) per the adoption note. Verify: `demand_read_core_adoption_and_ledger_first_direction_v0.md` + the core architecture on `origin/main`. reread-required.
- **C2 read-contract rules 1–3** (1: direction + two-sided tolerance; 2: ambiguity caveat classification; **3: risk-state weighting — cap on the MANUFACTURED axis, transient→C3, NOT a cap**). Verify: `judgment_spine_c2_ledger_read_contract_v0.md` on `origin/main`. reread-required.
- **INV-1 (no scoring engine)** and **the ratified G1/G2 Demand-Substrate Hard Gate**. Verify: the core architecture's Invariants + the buyer-proof packet on `origin/main`. reread-required.

## Active Objective

Advance the demand-read judge from coherent-but-unbuilt (its current on-main state) toward its first earned trust (the anchor goal), by resolving the design-tier-vs-build-tier horizon (Open Decision) with the owner and producing the bounded next routing object that fits the chosen horizon — without building/running anything absent explicit owner authorization.

## Exact Next Authorized Action

1. Spin a **fresh worktree off `origin/main`** (AGENTS isolation; do NOT use `ecr-sp3`). Run the Orca start preflight (AGENTS + overlay README).
2. Re-read on `origin/main`, verifying compare targets: the taxonomy; the C2 read-contract (rules 1–3); the core architecture (C0–C4); the adoption note (Decisions B/D); the signal-reliability ledger (#54); the buyer-proof gate.
3. **Resolve the Open Decision with the owner** (design-tier (a) vs build-tier (b)). Propose from evidence; the owner picks.
4. Produce the bounded next routing object for the chosen horizon — e.g. (a) ratify the grammar / specify C3+C4 / close the distill re-run; or (b) scope the first by-hand C2 read (build/run only after explicit owner authorization).
5. Stop condition: a chosen horizon + the smallest complete next routing object. No scoring engine, no numbers, no build/run without explicit owner authorization, no G1/G2 reopen; claims stay `product_learning`.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` (+ `CLAUDE.md` shim) — reread-required.
- Overlay authority: `.agents/workflow-overlay/` (README, source-loading, source-of-truth, decision-routing, validation-gates) — reread-required.
- User constraints: build/run owner-gated; INV-1 no scoring; G1/G2 consumed not reopened; design vs build/proof tiers kept distinct; no buyer outreach (no-contact-before-MVP gate stays closed); claims stay product_learning.
- Source-read ledger (all on `origin/main` @ e0b939a2 unless noted):
  - `docs/product/product_lead/orca_demand_read_taxonomy_v0.md`
    - Role: the read-grammar (two-axis model + calling sequence). Load-bearing: yes.
    - Compare target: status line `PROPOSED_PENDING_OWNER_ADJUDICATION`; two-axis amendment present (#78 `c36e09c2` ancestor of `origin/main`). reread-required.
    - Reuse rule: read fresh; it is NOT yet owner-adjudicated as operative grammar (that is option-(a) work).
  - `docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md`
    - Role: how C2 weights signals via the ledger; rules 1–3 (Rule 3 folded). Load-bearing: yes.
    - Compare target: contains `## Rule 3 — Risk-State Weighting Across Evidentiary States (folded 2026-06-15)`; landed via #124 (squash `3ccc86ef`). reread-required.
    - Reuse rule: read fresh; PROPOSED/product_learning; distill re-run still open (Mutable Questions).
  - `docs/product/judgment_spine/judgment_spine_demand_read_machinery_architecture_v0.md`
    - Role: C0–C4 core. Load-bearing: yes.
    - Compare target: `C1 — Allow` + C3 two-axis verdict present; landed via #125 (squash `2b45001b`). reread-required.
    - Reuse rule: read fresh; C0/C1/C3/C4 not contract-specified to C2's depth (option-(a) gap).
  - `docs/product/judgment_spine/demand_read_core_adoption_and_ledger_first_direction_v0.md`
    - Role: owner adoption (Decisions B + D) + ledger-first direction. Load-bearing: yes. Compare target: on `origin/main` (#125). reread-required.
  - `docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md`
    - Role: the signal-reliability ledger C2 reads (the build-tier substrate for option b). Load-bearing: yes.
    - Compare target: sha256[:16] `388352b83bac9860` on `origin/main` (#54, verified 2026-06-15). reread-required; re-check whether PR #64 hardening landed.
    - Reuse rule: holds NO real rows yet; populating it is owner-gated build work.
  - `docs/product/product_lead/orca_buyer_proof_packet_v0.md`
    - Role: the ratified Demand-Substrate Hard Gate (G1/G2 admissibility) + Orca Promise + no-scoring boundary. Load-bearing: yes. Compare target: on `origin/main` (re-grounded by #130). reread-required.
    - Reuse rule: consume the gate, do not reopen.
  - `docs/product/judgment_spine/judgment_spine_c2_rule3_reground_phase_a_classification_finding_v0.md`
    - Role: the PATCH classification + axis mapping record for Rule 3. Load-bearing: no (orientation). Compare target: on `origin/main` (#126). Reuse rule: orientation only.
- Source gaps: the ontology-backbone commission (`derived_from`/`diverges_from` link semantics that C2's de-correlate/diverge sub-steps depend on) is a dispatched, branch-only commission — "confirm on adoption"; not on `origin/main`.
- Strict-only blockers: any build/population/by-hand-run is BLOCKED pending explicit bounded owner authorization + the conductor run-gate.
- Not-proven boundaries: everything is `product_learning`/design — not validated, decision-grade, buyer-proven, or ready. The decay-curve / transient-timing capability does not exist (transient reads are built-to, not proven-at). Wind-caller calibration is unproven.

## Current Task State

- Completed (this session, landed on `origin/main`): C2 Rule 3 re-grounded onto the two-axis model (#124); C1 `Admit`→`Allow` rename + C3 `hollow`→two-axis verdict (#125); Phase-A PATCH classification finding (#126); `durable-vs-hollow`→two-axis propagation across 8 live product-lead + capture-spine docs (#130).
- Partially completed: the demand-read *method* is coherent and on main, but PROPOSED/product_learning — not ratified, not fully specified (C0/C1/C3/C4), not built, not validated.
- Broken or uncertain: nothing broken. The next horizon (design-tier completion vs build-tier crossing) is unresolved — the Open Decision.

## Workspace State

- Branch (sender primary): ecr-sp3-timing-deriver-slice1 @ 0fc58cfe — STALE; receiver must NOT continue here.
- Head: `origin/main` @ e0b939a2 (carries all four merged PRs).
- Dirty/untracked before handoff (sender primary): ~25 untracked on ecr-sp3.
- Dirty/untracked after writing this handoff file: this file newly untracked on ecr-sp3.
- Target files/artifacts: none yet for the receiver (off `main`); the demand-read spine docs above.
- Related worktrees/branches: the four lane branches (ledger-c2-read-contract-v0, judgment-spine-read-machinery-architecture-v0, c2-risk-state-weighting-reground-v0, hollow-retire-two-axis-propagation-v0) are MERGED + deleted on origin; local copies/worktrees may linger and are safe to prune.

## Changed / Inspected / Tested Files

- (All landed on `origin/main` via the four merged PRs — see Source Ledger for paths + compare targets. No uncommitted implementation deltas carry to the receiver.)

## Frozen Decisions

- Two-axis demand-state model (durable/transient + real/manufactured; hollow retired) is settled (#78). Do not reopen. Evidence: `c36e09c2` ancestor of `origin/main`. Consequence: the operative frame.
- C1 step verb is **Allow** (was Admit); "admitted signal" → "allowed signal"; gate "admissibility" + source-family "admission" unchanged. Evidence: #125 on main. Consequence: use "Allow"/"allowed signal".
- Rule 3 (risk-state weighting): cap on the **manufactured** axis; persistence-axis patterns are **transient** (routed to C3), NOT caps. Evidence: #124 on main. Consequence: do not re-litigate; do not cap transient.
- INV-1 (no scoring engine); advisory-not-control; G1/G2 not reopened. Consequence: weighting stays qualitative.

## Mutable Questions

- The Open Decision horizon (design-tier vs build-tier) — resolves by owner decision.
- The **distillation re-run** (route a de-correlation lesson to the overlay-governance / review-patch binding, NOT judgment-spine) — open from the ledger-c2 lane; resolves by running it correctly.
- Whether PR #64 changed the signal-reliability ledger schema — resolves by a fresh hash check vs `388352b83bac9860`.
- The ontology-backbone `derived_from`/`diverges_from` semantics — resolves on that commission's adoption.

## Superseded / Dangerous-To-Reuse Context

- **"durable vs hollow" framing** — RETIRED by the two-axis model. Replacement: durable/transient (persistence) + real/manufactured (integrity). Do not reintroduce.
- **The 3 PROPOSED `*_consumer_demand_revision_v0` variants still carry "durable-vs-hollow"** — DANGEROUS to adopt as-is (re-introduces the retired frame over #130's fix). Replacement: re-ground them before/at adoption; treat the base docs (re-grounded by #130) as the current frame.
- **The sender branch `ecr-sp3-timing-deriver-slice1`** — stale scratch; additive-untracked only. Replacement: a fresh worktree off `origin/main`.
- **"PRs pending merge" status from earlier in the sender thread** — SUPERSEDED: all four merged 2026-06-15. Replacement: read the work on `origin/main`.

## Commands And Verification Evidence

- Confirm the work is on main + two-axis ancestry (run 2026-06-15, sender):
  ```bash
  git merge-base --is-ancestor c36e09c2 origin/main   # exit 0 → two-axis model on main (#78)
  git grep -q "C1 — Allow" origin/main -- docs/product/judgment_spine/judgment_spine_demand_read_machinery_architecture_v0.md   # present
  git grep -q "Rule 3 — Risk-State Weighting" origin/main -- docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md   # present
  ```
  Result: all confirmed on `origin/main` @ e0b939a2.
- Merged PR squash commits (re-run target: `gh pr view <n> --repo eric-foo/orca --json state,mergeCommit`):
  - #124 → `3ccc86ef` (C2 Rule 3 fold)
  - #125 → `2b45001b` (C1 Allow + C3 two-axis)
  - #126 → `3067fb41` (Phase-A finding)
  - #130 → `03b47bfde` (hollow→two-axis propagation)
- Signal-reliability ledger hash (re-verify before relying on row shape): `388352b83bac9860` (#54 on `origin/main`); re-check #64.

## Blockers And Risks

- Build/run is owner-gated (no real rows, no by-hand read without explicit authorization). Evidence: drift guard + INV-1 + conductor run-gate. Next action: design/docs until the owner lifts the gate (option b).
- The signal-reliability ledger holds no real rows. Evidence: the C2 spec's Claim Classification ("the ledger holds no real rows"). Next action: populating it is owner-gated build work.
- Method incompleteness (C0/C1/C3/C4 not specified to C2's depth; taxonomy unratified). Evidence: only C2 has a read-contract. Next action: option-(a) work if the owner chooses it.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: (1) you are on a FRESH worktree off `origin/main`, not `ecr-sp3`; (2) `origin/main` carries the four merged PRs (C1 Allow + Rule 3 + hollow-retire present); (3) the taxonomy's `PROPOSED_PENDING_OWNER_ADJUDICATION` status; (4) the ledger #54 hash `388352b83bac9860` (and whether #64 landed); (5) the ratified G1/G2 gate on main.
- Compare targets: `c36e09c2` ancestry of `origin/main`; the grep markers above; ledger sha256[:16]; merged PR squash SHAs.
- Load outcomes: `REUSE` only if `origin/main` carries the merged work and you are off `main`; `STALE_REREAD_REQUIRED` if `origin/main` advanced past e0b939a2 or #64 changed the ledger; `BLOCKED_UNVERIFIABLE` if the spine docs can't be read.
- Sources to reread if drift: the taxonomy + C2 read-contract + core architecture on `origin/main` (they bound the whole lane).

## Do Not Forget

- **The method is on main but UNBUILT and UNVALIDATED** — the gap to the goal is evidence, not more doctrine. Don't substitute a 4th design doc for first earned trust.
- **Build/run is owner-gated** — the build-tier crossing (option b) needs the owner's explicit word.
- **Resolve the horizon Open Decision with the owner before producing the next routing object** — design-tier (a) vs build-tier (b).
- **Don't re-introduce "hollow"** — and re-ground the 3 PROPOSED revision variants before they're adopted.
```text
This is a continuation artifact, not validation, readiness, or acceptance evidence.
```
