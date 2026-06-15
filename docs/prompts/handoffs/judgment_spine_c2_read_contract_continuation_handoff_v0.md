# Handoff Packet — Judgment-Spine C2 Ledger Read-Contract Continuation

```yaml
retrieval_header_version: 1
artifact_role: Handoff packet (cold cross-lane state transfer; workflow-handoff output)
scope: >
  Transfers the Judgment-Spine demand-read CORE C2 (Weight) read-contract lane to
  a fresh reader / the owner returning later. The C2 read-contract spec is
  authored with rules 1-2 landed; rule 3 (known-risk-across-evidentiary-states
  doctrine) is the open decision, routed to a dedicated thread. Cold-reader
  self-contained; confirm-don't-trust load contract.
use_when:
  - Picking up the C2 ledger read-contract after this session, or after the rule-3 doctrine thread returns.
authority_boundary: retrieval_only
applied_contract: authored via workflow-handoff (packet owner); courier prompt deferred to workflow-prompt-orchestrator.
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-14
- created_by_lane: Orca C2 read-contract lane (Claude Opus-class); provenance only, not authority
- workspace: C:\Users\vmon7\Desktop\projects\orca (worktrees under C:\Users\vmon7\Desktop\projects\orca-worktrees\)
- handoff_path: docs/prompts/handoffs/judgment_spine_c2_read_contract_continuation_handoff_v0.md (in the lane worktree below)
- expected_branch: ledger-c2-read-contract-v0 (in worktree C:\Users\vmon7\Desktop\projects\orca-worktrees\orca-ledger-c2-read-contract-wt, off origin/main)
- expected_head: 653b8e2309acffd864231361fb64fbe946317318
- expected_dirty_state_including_handoff_file: tree was clean before this file; this handoff file is newly untracked after writing.
- WARNING — wrong checkout by default: a resumed session showed the PRIMARY repo on branch `ecr-sp3-timing-deriver-slice1` @ aed85c4 (an UNRELATED lane). This lane's work is ONLY in the worktree above. Re-verify you are in the worktree before acting.
- load_rule: confirm-don't-trust — re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: Orca's durable-vs-hollow demand calls become trustworthy by method (not assertion) on an inherently manipulable public substrate.
- anchor_goal: make the signal-reliability ledger the working FIRST learning mechanism for the demand-read core; the active sub-thread is the CORE's C2 (Weight) step read-contract — how C2 consumes the ledger qualitatively.
- success_signal: a C2 read-contract spec + the doctrine that makes a qualitative (no-scoring) weight reader-consistent and owner-adoptable, at design/docs tier.

## Open Decision / Fork

- decision — **RULE 3: how C2 treats a known risk / failure-mode across its evidentiary states**, as cap (ceiling on trust) / discount (mark-down) / neutral / positive, chained consistently:
  - states: **confirmed-present** (settled = cap) → **unconfirmed-but-possible** (the contested middle) → **confirmed-absent** (seed = neutral / floor-clear, never positive).
  - already constrained: present = cap; INV-1 keeps it qualitative (a stated cap/discount/neutral + reason, never a number/formula).
  - the **monotonicity argument** (present ≤ unconfirmed ≤ absent): unconfirmed=neutral collapses "didn't check" with "checked-clear" (kills the verify incentive); unconfirmed=cap collapses "might be" with "is" (signals never earn trust). Only **discount-in-the-middle** keeps the three distinct AND rewards verifying.
  - distinct mechanism: **inherent small-N** (e.g. N=3 sample) is NOT a state-dependent risk — it caps the *ceiling* permanently; handle separately.
  - **owner-raised refinement to fold in:** absence of a *contributory confound* = neutral, BUT absence of a *dominant disqualifier* (the main way the call could be fake — e.g. manufactured demand, which the Demand-Substrate Hard Gate rules out) can lean **positive** (it redistributes probability, not just removes a downside). The thread must set the line between contributory-confound and dominant-disqualifier.
  - owner of the call: **owner (Eric)**. The genuine fork = the DEFAULT severity of the unconfirmed discount + how steeply it escalates with the action-ceiling (act/phase/narrow/hold/defend) — a read on Orca's false-positive vs false-negative asymmetry.
  - recommendation (preserve, don't force): discount-by-default escalating to cap by stakes; absent→neutral (positive only for a dominant disqualifier); present→cap; small-N→cap-the-ceiling. The owner sets severity/steepness; everything chains from it.
  - status: AUTHORIZED axis; routed to a dedicated Claude thread (a seed prompt was produced this session — see Do Not Forget). Owner will "return" with the decision.

## Drift Guard

- **Design/docs tier only.** No real ledger rows, no by-hand run, no build/population/run, no push, no PR-merge — all owner-gated.
- **INV-1 — no scoring engine.** The weight is a qualitative direction + two-sided tolerance, never a number, ordinal, formula, or deterministic apply-rule. This is the single most expensive line to cross; rule 3 must stay a stated classification + reason.
- **Don't edit the FROZEN conductor** (`judgment_quality_promotion_operating_model_v0.md`, JSG-01..10). The core rides it as the JSG-06 contestant; consume the ledger / siblings by pointer.
- **Consume the demand gate; don't reopen** the ratified P2/P3/P4.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (read `AGENTS.md` + `.agents/workflow-overlay/README.md` first).
- targets to enter the ladder: the spec + 3 probes on this branch (below); the distillation bindings on origin/main; the demand-read core architecture + adoption note (branch-only); the ledger #54.
- already loaded (weak orientation, freshness-marked; NOT authority): all of the above were read this session 2026-06-14; treat as stale pointers, re-read.
- must load first (before strict/actionable steps): AGENTS + overlay README; then the spec + the relevant binding.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- **Demand-read core ADOPTED (owner, 2026-06-14); ledger-first direction set.** C2(c) reads the ledger qualitatively. Verify: `docs/product/judgment_spine/demand_read_core_adoption_and_ledger_first_direction_v0.md` (commit 57339ea, branch `judgment-spine-read-machinery-architecture-v0`-only) + core architecture (commit e794b8f, same branch-only). reread-required.
- **C2 read-contract rules 1-2 landed (this lane).** Rule 1: direction + reasoning load-bearing; weight = two-sided ~one-band tolerance, not a precise point. Rule 2: each ambiguous caveat classified cap/discount/neutral with a reason. Verify: the spec (compare target below).
- **Probe finding F4 (this lane).** A qualitative C2 read can be non-scoring + non-vacuous yet **inconsistent** — reasoning (facts + counterfactual) is framing-stable but the weight *level* drifts ~one band; confirmed blind across 4 model brands; the discipline (rule 2) recenters it and localized the residual to rule 3. Verify: probes v1/v2 (below).

## Active Objective

Settle rule 3 (the known-risk-across-states doctrine) in the dedicated thread, fold the result into the C2 read-contract spec as rule 3, and separately re-run the distillation correctly against the real binding. Then the design tier of the C2 read-contract is complete (build remains owner-gated).

## Exact Next Authorized Action

1. Enter the worktree `C:\Users\vmon7\Desktop\projects\orca-worktrees\orca-ledger-c2-read-contract-wt` (branch `ledger-c2-read-contract-v0`); confirm head 653b8e2 + clean tree.
2. Owner runs the rule-3 doctrine thread (seed prompt produced this session). On return, author rule 3 into the spec `docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md` (qualitative; INV-1-safe), with acceptance criteria, matching the rules 1-2 style.
3. Re-run `/workflow-distill` correctly: the binding family EXISTS (see Superseded). LOCATE the de-correlation lesson on the **overlay-governance or review-patch** binding's spine (NOT judgment-spine, whose nodes are conductor gates), and CONFLICT-CHECK against existing de-correlation residents (cross-vendor-discovery; no-self-cert-clearing).
4. Stop condition: rule 3 folded in + distill re-run; NO build/population/run, NO scoring engine, NO conductor edit, NO push without explicit owner authorization.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` (+ `CLAUDE.md` shim) — reread-required.
- Overlay authority: `.agents/workflow-overlay/` (README, source-loading, source-of-truth, review-lanes, delegated-review-patch) — reread-required.
- User constraints: design/docs only; INV-1 no scoring engine; don't edit the FROZEN conductor; consume the ledger by pointer; build owner-gated.
- Source-read ledger:
  - `docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md` (this branch)
    - Role: the C2 read-contract spec (rules 1-2 landed; rule 3 to add). Load-bearing: yes.
    - Compare target: blob sha256[:16] `a62b5bfd73ba93bb` at HEAD 653b8e2. Last checked: 2026-06-14.
    - Reuse rule: read fresh; this is the artifact rule 3 lands in.
  - `docs/product/judgment_spine/judgment_spine_c2_qualitative_read_feasibility_probe_v2.md` (this branch)
    - Role: the BLIND consistency probe + cross-model addendum (the F4 + rule-3-localization evidence). Load-bearing: yes. Compare target: reread-required at HEAD 653b8e2. Reuse rule: read fresh; evidence for rule 3.
  - `docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md` (origin/main)
    - Role: the ledger C2 consumes. Load-bearing: yes. Compare target: sha256[:16] `388352b83bac9860` (#54) on origin/main, verified 2026-06-14; re-check whether PR #64 changed it. Reuse rule: consume by pointer; amend only via delegated-review-patch.
  - `docs/decisions/distillation_binding_judgment_spine_v0.md`, `..._overlay_governance_v0.md`, `..._review_patch_v0.md`, `distillation_doctrine_orca_spine_bindings_v0.md` (origin/main)
    - Role: the distillation bindings (all PREPARE-ONLY DRAFT). Load-bearing: yes for the distill re-run. Compare target: present on origin/main, verified 2026-06-14 (`git cat-file -e`). Reuse rule: read fresh; route the de-correlation lesson to overlay-governance/review-patch, not judgment-spine.
  - `docs/product/judgment_spine/demand_read_core_adoption_and_ledger_first_direction_v0.md` (57339ea) + core architecture (e794b8f)
    - Role: owner adoption + the core whose C2 this specifies. Load-bearing: yes. Compare target: commits on branch `judgment-spine-read-machinery-architecture-v0`; reread-required (branch-only, not on origin/main).
- Source gaps: the core architecture + adoption note are branch-only (sender branch `judgment-spine-read-machinery-architecture-v0`); obtain there if a strict claim about the core's shape is needed.
- Strict-only blockers: any build/population/by-hand-run is BLOCKED pending explicit bounded owner authorization.
- Not-proven boundaries: everything here is `product_learning` / design; not validated, ready, or buyer-proven. Feasibility-in-principle established; operational reliability (cross-model, multi-case, real data) NOT proven.

## Current Task State

- Completed: C2 read-contract spec authored with rules 1-2 + acceptance criteria + enforcement posture; probes v0/v1/v2; cross-model evidence (4 brands); 6 commits on the lane branch (clean tree).
- Partially completed: rule 3 (doctrine) framed + recommended + routed to a dedicated thread, NOT decided. Distill emitted advisory-only but its "no binding" reason was wrong (see Superseded) — re-run owed.
- Broken or uncertain: none broken. Rule 3 unresolved; operational reliability unproven by design.

## Workspace State

- Branch: ledger-c2-read-contract-v0 (worktree orca-ledger-c2-read-contract-wt, off origin/main).
- Head: 653b8e2309acffd864231361fb64fbe946317318.
- Dirty/untracked before handoff: clean.
- Dirty/untracked after writing this handoff file: this file newly untracked.
- Target files/artifacts: the spec (rule 3 lands here); probe v2 (evidence).
- Related worktrees/branches: sender branch `judgment-spine-read-machinery-architecture-v0` (core architecture + adoption, branch-only); PRIMARY repo is on the UNRELATED `ecr-sp3-timing-deriver-slice1`.

## Changed / Inspected / Tested Files

- `docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md` — spec; rules 1-2 + acceptance + enforcement posture; committed 2328e6d. Rule 3 to add.
- `docs/product/judgment_spine/judgment_spine_c2_qualitative_read_feasibility_probe_v0.md` / `_v1.md` / `_v2.md` — probe chain (v0 weak → v1 pre-registered → v2 blind + cross-model). Committed across dc63a23..653b8e2.

## Frozen Decisions

- **Rule 1** (owner, 2026-06-14): direction + reasoning load-bearing; weight = two-sided ~one-band tolerance, not a precise point. Evidence: spec + probe v2 cross-model. Consequence: consistency judged on direction + reasoning, not exact level.
- **Rule 2** (owner, 2026-06-14): each ambiguous caveat classified cap/discount/neutral with a reason. Evidence: spec; probe v2 showed forcing this recenters the read. Consequence: enforced by trace-audit, not code.
- **INV-1 no scoring engine** + **don't edit the FROZEN conductor** + **demand-read core adopted, ledger-first**. Evidence: spec; adoption note 57339ea. Consequence: rule 3 stays qualitative; the core rides the conductor by pointer.

## Mutable Questions

- Rule 3 (the doctrine fork) — resolves by the owner's dedicated-thread decision on unconfirmed-risk discount severity + escalation.
- Whether PR #64 changed the ledger — resolves by a fresh hash check vs `388352b83bac9860` before relying on the ledger row shape.

## Superseded / Dangerous-To-Reuse Context

- **The distill "no binding exists → advisory-only" claim (this session) is WRONG.** A full distillation-binding family IS committed on origin/main (`docs/decisions/distillation_binding_*.md` incl. judgment_spine, overlay_governance, review_patch, + doctrine index), all PREPARE-ONLY DRAFT. Replacement: re-run distill against the real binding — route the de-correlation lesson to overlay-governance/review-patch (NOT judgment-spine, whose nodes are conductor gates), CONFLICT-CHECK the de-correlation residents.
- **Probe v0/v1 self-graded "pass" results are superseded** by the v2 BLIND result (a self-/same-author consistency check can pass while false). Use v2 + the cross-model addendum as the consistency evidence, not v0/v1's self-grade.

## Commands And Verification Evidence

- Re-verify lane state:
  ```bash
  git -C C:/Users/vmon7/Desktop/projects/orca-worktrees/orca-ledger-c2-read-contract-wt rev-parse HEAD   # expect 653b8e2
  git -C <wt> status --porcelain                                                                          # expect clean
  git -C <wt> cat-file blob HEAD:docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md | sha256sum  # expect a62b5bfd73ba93bb...
  ```
- Re-verify the binding family exists (the corrected fact):
  ```bash
  git -C <wt> cat-file -e origin/main:docs/decisions/distillation_binding_judgment_spine_v0.md && echo present
  ```
  Result this session: present (+ overlay_governance, review_patch, doctrine index).

## Blockers And Risks

- Build/run is owner-gated. Evidence: drift guard + INV-1; conductor run-gate. Next action: design/docs only until explicit owner authorization.
- Rule 3 unresolved → the spec is incomplete (rules 1-2 only). Next action: run the dedicated thread, fold result in.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: you are in the WORKTREE (not the primary ecr-sp3 checkout); branch ledger-c2-read-contract-v0 @ 653b8e2 + clean tree; the spec blob hash `a62b5bfd73ba93bb`; the ledger #54 hash `388352b83bac9860` (and whether #64 landed); the binding family present on origin/main.
- Load outcomes: REUSE only if the spec + bindings re-verify; STALE_REREAD_REQUIRED if #64 changed the ledger or the branch advanced; BLOCKED_UNVERIFIABLE if the branch-only core/adoption files can't be obtained and a strict claim about the core depends on them.
- Sources to reread if drift: the spec + probe v2; the relevant distillation binding.

## Do Not Forget

- A **seed prompt for the rule-3 thread** was produced in this session's chat (frames the present/unconfirmed/absent axis + the FP/FN fork + the absence-of-dominant-disqualifier refinement). Reuse it to start the thread; if lost, reconstruct from the Open Decision block above.
- The single most expensive mistake is building a scoring engine — keep rule 3 qualitative (classification + reason) until the owner explicitly lifts INV-1.
- The distill binding correction (Superseded) must not be re-lost: the binding exists; the prior "advisory-only because none exists" was an unsearched-absence error.
```text
This is a continuation artifact, not validation, readiness, or acceptance evidence.
```
