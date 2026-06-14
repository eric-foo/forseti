---
retrieval_header_version: 1
artifact_role: Cross-lane handoff packet (cold reader; durable continuation artifact, NOT validation/readiness evidence)
scope: Set up to PROVE the Orca judgment-spine method works by carrying it past N=1 (repeatability -> calibration). Hands a fresh lane the proven Beauty Pie #3 pipeline + guardrails so it can run case #2.
authority_boundary: retrieval_only
---

# Handoff Packet — Prove the Judgment-Spine Method Repeats (past N=1)

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-14 (this session)
- created_by_lane: Beauty Pie #3 pilot CA thread (provenance only; NOT an authority claim)
- workspace: C:\Users\vmon7\Desktop\projects\orca
- handoff_path: docs/hygiene/judgment_spine_prove_method_repeatability_handoff_v0.md
- expected_branch: do your work in a FRESH worktree off `main` (this packet was authored in worktree `orca-handoff-prove-wt` on branch `handoff-prove-method-repeatability-v0`; do NOT reuse that branch for case-#2 work).
- expected_head: `origin/main` = `1b6660c` at authoring (WILL move — reread).
- expected_dirty_state_including_handoff_file: this handoff file is newly created + untracked until committed on its own lane PR; the main working dir sits on an unrelated dirty legacy branch — ignore it.
- load_rule: confirm-don't-trust. Re-verify every load-bearing fact below against its compare target before acting. Sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: an Orca judgment spine that produces trustworthy, defensible, *calibrated* N=K judgment fixtures at scale.
- anchor_goal: carry the proven capture -> resolve -> firewalled-freeze pipeline PAST N=1 to show it REPRODUCES — i.e., prove repeatability (the pipeline runs cleanly on a 2nd+ case without faking evidence), en route to a calibration proof that is only meaningful at N>=K (after reveal). One frozen case proves *method*, not *judgment quality*.
- success_signal: a second case (case #2) frozen honestly via the same pipeline — both owner and agent OUTCOME-BLIND — with the L2 claim-support enforcement applied, demonstrating the method reproduces. Stretch: enough frozen cases that a reveal/calibration step (JSG-08) becomes meaningful.

## Open Decision / Fork

- decision: which case is case #2, and run it now or stage it.
  - options: (a) select the next case from the batch-1 charter and run the full pipeline; (b) stage/scope it and pause for owner go.
  - already constrained / off the table: NOT a Beauty Pie variant (Beauty Pie is the frozen N=1); NOT the FacilitatorLedger schema fix first (deferred — see Drift Guard); NOT reading any sealed outcome.
  - trade-offs: running case #2 creates the new external evidence (repeatability) the goal needs; staging delays it for owner authorization (runtime/judgment work needs explicit owner go).
  - owner of the call: the owner (case selection + run authorization).
  - recommendation: select case #2 from the batch-1 charter, then get explicit owner authorization before running (this packet sets up the lane; it does NOT authorize the run).
- decision: land PR #83 (the L2 enforcement) — see Current Task State; it needs a rebase before it can merge.
  - owner of the call: owner CLI-merges (guard EP-03); the rebase itself can be prepared by the lane and force-pushed by the owner.

## Drift Guard

- OUTCOME-BLIND, permanently: NEVER read any case's sealed outcome — not the Beauty Pie ledger's `sealed_outcome` block, not any `*sealed_outcome*` file, not case #2's once it is sealed. Why it matters: the whole method's defensibility depends on the judge never seeing the answer before reveal; reading it destroys the N as a data point. The firewalled-freeze (L5) exists to preserve this.
- Guard EP-03: agents CANNOT land-to-main. Owner CLI-merges every PR. Do not attempt a merge/push-to-main/force-push; prepare it and hand it to the owner.
- Do NOT do the FacilitatorLedger schema fix while outcome-blind unless via the shape-only path (reconcile from the ledger's *shape*, never its sealed *value*). It is the highest-lock-in, outcome-adjacent item and the owner has signalled caution. The blind-safe path is "grandfather the hash-protected frozen case + define new vocab for new cases." Defer it until the batch actually runs model-validation gates.
- Smallest-complete; worktrees off `main`; per-lane PR flow; runtime/judgment work needs explicit owner authorization in the current turn.
- This handoff is NOT authorization to run case #2. It sets up the lane.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/` — read `.agents/workflow-overlay/README.md` first (per `AGENTS.md`); then `decision-routing.md`, `artifact-folders.md`, `safety-rules.md`, `source-loading.md` as needed.
- targets to enter the ladder: the batch-1 charter (`docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md`), the feasibility doc (`docs/research/orgmotion_beautypie_capture_feasibility_v0.md`), the frozen exemplar case dir (`orca-harness/cases/product_learning/beautypie_repricing_2023_v0/` — but NOT its `sealed_outcome`), the harness schemas (`orca-harness/schemas/case_models.py`, `orca-harness/evidence_binding/`).
- already loaded (weak orientation, freshness-marked; NOT authority): this packet + the merged held-lessons note (L1-L5).
- must load first (before strict or actionable steps): the overlay README + safety-rules (for the outcome-blind + EP-03 constraints) and the batch-1 charter (for the case queue).
- load rule: re-run progressive source loading per the overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- The proven pipeline = capture -> resolve provenance -> cross-vendor second-label -> firewalled freeze.
  - decided in / exemplar: `orca-harness/cases/product_learning/beautypie_repricing_2023_v0/` (the frozen Beauty Pie #1 fixture).
  - compare target: present on `origin/main` (verified this session); reread-required (NEVER open `sealed_outcome`).
  - verify before: building case #2's pipeline.
- Provenance taxonomy (L3): captured-source / case-stated-premise (asserted-real, recorded facilitator-side, kept OFF the contestant's evidence manifest) / general-base-rate (sentinel). This is how a premise with no captured evidence is handled honestly instead of faking evidence.
  - decided in: `docs/decisions/distillation_held_lessons_beautypie_pilot_v0.md` (on main) + `.../beautypie_repricing_2023_v0/source_provenance_notes_v0.md`.
  - compare target: held note present on `origin/main` (verified); reread-required.
  - verify before: classifying any case #2 evidence.
- The L1-L5 learnings (the method's guardrails) — see Frozen Decisions.

## Active Objective

Stand up a case-#2 lane that runs the proven judgment pipeline on a second backtest case, outcome-blind, with the L2 claim-support enforcement applied — producing a second honestly-frozen fixture that demonstrates the method reproduces. This is the first step toward a calibration proof that only becomes meaningful at N>=K.

## Exact Next Authorized Action

1. Read the overlay README + safety-rules + the batch-1 charter (`docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md`); identify the next queued case (case #2). Confirm with the owner which case and get explicit authorization to run.
2. Land PR #83 first if the owner wants the L2 enforcement available for case #2: rebase branch `distill-l2-claim-support-v0` onto current `main` to drop the duplicated held-note commits (`bfbd953`, `c14756c`) that #77 already squashed, then the owner squash-merges. (Optional for case #2 to run, but it is the operationalized L2 guard.)
3. Run the pipeline on case #2 in a fresh worktree off `main`: capture (archive_org adapter, retain raw body + hash) -> resolve provenance (L3 taxonomy) -> cross-vendor second-label -> firewalled freeze (outcome-aware subagent returns ONLY the `ledger_freeze_hash`; you + owner stay blind). Apply the L2 claim-support assertions for any atomic quotable claim.
4. Stop/validation condition: a second freeze-valid fixture exists, both parties stayed outcome-blind, evidence was not faked (every captured-source claim has a body-verified span; premises classified honestly). Accept that this fixture is freeze-valid but NOT `model_valid` (deferred debt — see Mutable Questions).

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` + `CLAUDE.md` (shim) + `.agents/workflow-overlay/` (read README first).
- Overlay or equivalent authority: `.agents/workflow-overlay/` (decision-routing, safety-rules, artifact-folders, source-loading, review-lanes).
- User constraints: OUTCOME-BLIND; guard EP-03 (owner CLI-merges); don't do the schema fix while blind; smallest-complete; explicit owner authorization for runtime/judgment runs.
- Source-read ledger:
  - `origin/main`
    - Role: base for all new work. Load-bearing: yes. Compare target: HEAD ref (was `1b6660c`). Last checked: this session. Reuse rule: reread — it moves.
  - `docs/decisions/distillation_held_lessons_beautypie_pilot_v0.md`
    - Role: the L1-L5 learnings (method guardrails). Load-bearing: yes. Compare target: present on `origin/main` (#77 merged); reread-required. Last checked: this session. Reuse rule: orientation only; rebind fresh for strict use.
  - `orca-harness/cases/product_learning/beautypie_repricing_2023_v0/` (NOT `sealed_outcome`)
    - Role: the frozen exemplar pipeline. Load-bearing: yes. Compare target: present on `origin/main`; reread-required. Reuse rule: copy the pipeline shape; NEVER read `sealed_outcome`.
  - `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md` + `docs/research/orgmotion_beautypie_capture_feasibility_v0.md`
    - Role: the batch charter (case queue + the ATS-led org-motion capture mandate). Load-bearing: yes. Compare target: both present on `origin/main` (verified this session). Reuse rule: confirm the case-#2 selection here.
  - `orca-harness/evidence_binding/` (`verifier.py`, `models.py` Jsg01ClaimSupportAssertion) + `orca-harness/schemas/case_models.py`
    - Role: the L2 enforcement + the FacilitatorLedger model. Load-bearing: yes. Compare target: the L2 verifier is on branch `distill-l2-claim-support-v0` (PR #83), NOT yet on `main` (verified absent on main this session); `case_models.py` is on main. Reuse rule: reread on the #83 branch until it lands.
- Strict-only blockers: case #2 run requires explicit owner authorization. PR #83 requires a rebase before it can merge. The FacilitatorLedger schema fix is owner-gated + blind-delicate.
- Not-proven boundaries: NO calibration/judgment-quality claim exists (sealed; needs reveal at N>=K). The pipeline is "proven" only as method-repeatability-pending; this packet asserts no readiness/validation.

## Current Task State

- Completed: Beauty Pie #1 frozen on main (N=1 anchor). PR #77 merged (L1-L5 held note on main). L2 verifier built, cross-vendor reviewed (OpenAI GPT-5; F1/F2 adjudicated), same-vendor recheck CLOSURE_CONFIRMED, 28 tests pass.
- Partially completed: PR #83 (the L2 verifier) is OPEN and NOT cleanly mergeable — stacked-squash conflict (its branch carries the held-note commits `bfbd953`/`c14756c` that #77 already squashed onto main). Fix = rebase `distill-l2-claim-support-v0` onto current `main`, then owner squash-merges.
- Broken or uncertain: no case #2 selected/run yet. FacilitatorLedger schema drift (L4) unresolved — every new fixture will be freeze-valid but not `model_valid` until the deferred schema fix.

## Workspace State

- Branch: do case-#2 work in a NEW worktree off `main`. (This packet authored in `orca-handoff-prove-wt` @ branch `handoff-prove-method-repeatability-v0` — do not reuse.)
- Head: `origin/main` = `1b6660c` at authoring (reread).
- Dirty/untracked before handoff: main working dir on legacy dirty branch `ecr-sp3-timing-deriver-slice1` (ignore).
- Dirty/untracked after writing the handoff file: this file newly created + untracked until its lane PR is committed.
- Target files/artifacts: the frozen exemplar case dir; the batch-1 charter; `orca-harness/evidence_binding/` + `orca-harness/cases/`.
- Related worktrees/branches: `distill-l2-claim-support-v0` (PR #83, needs rebase). Stale pilot worktrees may exist and are cleanable.

## Frozen Decisions

- The proven pipeline shape (capture -> resolve -> second-label -> firewalled freeze). Evidence: the Beauty Pie #1 fixture. Consequence: reuse it for case #2; don't re-invent.
- L1: scope a work-unit against its own charter BEFORE recommending. Evidence: the ATS "overbuild" misjudgment, corrected. Consequence: read case #2's charter before scope calls.
- L2: a successful capture is NOT claim-support until the body is verified to contain the claim's span (page-grain, presence not semantic support). Evidence: the how-it-works capture lacked the pricing facts the premise leaned on; now code-backed in PR #83. Consequence: bind every atomic quotable claim with a body-verified span.
- L3: provenance taxonomy (captured-source / case-stated-premise / general-base-rate). Consequence: classify each case #2 fact honestly; never fake evidence for a premise.
- L4: construction-vs-runtime schema drift (FacilitatorLedger can't `model_validate` the frozen fixture). Consequence: expect + accept the same drift on case #2 (deferred debt).
- L5: firewalled-freeze recipe (outcome-aware subagent returns only the hash; owner + agent stay blind). Consequence: freeze case #2 the same way; stay blind.
- Meta: a different-vendor reviewer earns its keep on the claims you are CONFIDENT about; encode/auto if possible but classify-substrate-first and never force judgment into brittle code; verify by page, weight by source; don't do high-lock-in work while blind.

## Mutable Questions

- Which case is case #2? Resolves: owner + the batch-1 charter.
- Run case #2 before or after landing #83? Resolves: owner (the L2 enforcement is nice-to-have for case #2, not required to run).
- Fix the FacilitatorLedger schema before accumulating more unvalidatable fixtures, or keep deferring? Resolves: owner. Recommendation: keep deferring until the batch runs model-validation gates; doing it now (blind, high-lock-in) is premature. Do it shape-only when the time comes.

## Superseded / Dangerous-To-Reuse Context

- Any earlier claim that L2's encode lands in `case_models.py` / is coupled to the FacilitatorLedger fix — FALSE. L2 lives in `orca-harness/evidence_binding/` (a separate file); it is DECOUPLED from the FacilitatorLedger drift. (Corrected during the pilot.)
- "Code-enforced / auto-enforced on every assembly" for the L2 guard — over-claimed; narrowed to "code-backed + contract-tested WHEN INVOKED" (it is not yet wired into a mandatory write-time/assembly path; that wiring is a deferred follow-on). Do not re-introduce the overclaim.

## Commands And Verification Evidence

- Re-verify base + #83 state (run before acting):
  ```bash
  git fetch origin
  git rev-parse origin/main
  gh -R eric-foo/orca pr view 83 --json number,state,mergeable
  ```
  Result at authoring: origin/main = 1b6660c; #83 OPEN (mergeable UNKNOWN/conflicted). Re-run to confirm rather than trust.
- L2 tests (on the #83 branch worktree): `python -m pytest tests/unit/test_claim_support_verifier.py tests/unit/test_evidence_binding.py -q` -> 28 passed at authoring.

## Blockers And Risks

- PR #83 not cleanly mergeable (stacked-squash). Likely next action: rebase `distill-l2-claim-support-v0` onto `main`, owner squash-merges.
- RISK: reading any sealed outcome contaminates blindness. Mitigation: never open `sealed_outcome`.
- RISK: doing the FacilitatorLedger schema fix while blind. Mitigation: defer; shape-only when done.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: `origin/main` head (was `1b6660c`); held note + frozen ledger + batch-1 charter present on main; PR #83 state; the L2 verifier lives on `distill-l2-claim-support-v0` (not main).
- Load outcomes: REUSE only if all re-verify; STALE_REREAD_REQUIRED if `origin/main` moved (re-pin) — expected; BLOCKED_DRIFT if the frozen ledger changed (a frozen fixture must not change — investigate); BLOCKED_UNVERIFIABLE if a load-bearing path is missing/unreadable.
- Sources to reread if drift: the overlay README + safety-rules; the batch-1 charter; the frozen exemplar (NOT sealed_outcome); `case_models.py` + `evidence_binding/`.

## Do Not Forget

- OUTCOME-BLIND, permanently — never read any sealed outcome. This is the method's whole integrity.
- Agents cannot land-to-main (EP-03) — owner CLI-merges.
- One frozen case proves method, not judgment quality — the calibration claim needs N>=K + reveal. Don't overclaim from case #2 alone.
