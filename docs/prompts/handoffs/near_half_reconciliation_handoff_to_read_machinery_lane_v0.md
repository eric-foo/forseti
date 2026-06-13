# Handoff Packet — Near-Half Backtest-Learning Machinery Already Built (reconcile, don't re-derive)

```yaml
retrieval_header_version: 1
artifact_role: Handoff packet (cold cross-lane state transfer; workflow-handoff output)
scope: >
  Delivers ONE load-bearing fact the read-machinery architecture lane does not
  have: the near-half (backtest-learning) lane independently built and LANDED
  overlapping backtest-distillation + per-signal-weighting machinery. The
  read-machinery lane should reconcile its backtest-shell distillation/weighting
  design with these landed artifacts (consume, don't re-derive) and surface the
  reconciliation for owner sign-off. The near-half lane retires after this.
use_when:
  - Running the Judgment-Spine read-machinery architecture pass (object "C", "one core, two shells").
  - Specifically before designing that lane's backtest-shell distillation tail, dated-card deck, or checkpoint-3 (per-vertical weighting).
authority_boundary: retrieval_only
open_next:
  - docs/prompts/handoffs/judgment_spine_read_machinery_architecture_handoff_v0.md  # nonresolving: the receiver's own handoff; untracked on the ecr-sp3 sender branch, not yet on main
  - docs/product/judgment_spine/near_half_backtest_learning_architecture_v0.md
  - docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-13
- created_by_lane: Orca near-half / prospective-decision-loop lane (Claude); provenance only, not authority
- workspace: C:\Users\vmon7\Desktop\projects\orca (any worktree off origin/main)
- handoff_path: docs/prompts/handoffs/near_half_reconciliation_handoff_to_read_machinery_lane_v0.md
- expected_branch: the read-machinery lane spins up its OWN worktree/branch off origin/main (per AGENTS isolation); this packet was authored on near-half-reconciliation-handoff-v0 off origin/main @ 89c2973
- expected_head: origin/main at or after 89c2973 (the near-half artifacts are landed; verify by the hashes below, not by head)
- expected_dirty_state_including_handoff_file: this handoff file is newly added (its own PR); the named near-half artifacts are committed on origin/main
- load_rule: confirm-don't-trust — re-verify every load-bearing fact (the landed artifacts + their blob hashes) before acting; sender claims are hypotheses. A squash silently dropped a reviewed adjudication once in the near-half lane's history, so verify content actually on main.

## Goal Handoff

- long_term_goal: Orca's demand calls become trustworthy enough that a decision owner allocates (and eventually pays) against them — trust earned by method, not asserted. (Carried verbatim from the read-machinery lane's own handoff, `judgment_spine_read_machinery_architecture_handoff_v0.md`.)
- anchor_goal: Reconcile this lane's backtest-shell distillation/weighting design (the "phased distillation tail → dated-card deck → checkpoint-3 per-vertical weighting") with the already-LANDED near-half backtest-learning artifacts, so Orca has ONE backtest-learning subsystem, not two competing ones. Consume the landed artifacts as the substrate; do not re-derive a parallel distillation system.
- success_signal: The read-machinery architecture object treats the landed near-half signal-reliability ledger + near-half architecture as its backtest-learning substrate (cited, reused, or explicitly amended via a reviewed pass), folds the read-machinery PROVE gate into the near-half promotion gate, and surfaces the consume-vs-differentiate reconciliation for owner sign-off. NOT success: silently designing a second, vocabulary-divergent distillation deck / lesson store / weighting ledger that duplicates the landed artifacts.

## Open Decision / Fork

- decision: **Consume the landed near-half artifacts as the backtest-learning substrate, or differentiate (two distinct subsystems)?**
  - options: (i) CONSUME — the read-machinery backtest shell uses the near-half signal-reliability ledger (for per-signal/per-vertical weighting = its checkpoint #3) and the near-half architecture (adversarial-postmortem + validated-lesson cell + promotion gate = its distillation tail), grafting in the read-machinery PROVE gate + survival-kernel "dated card" framing; (ii) DIFFERENTIATE — keep two subsystems with a stated boundary.
  - already constrained / off the table: re-deriving a competing distillation system from scratch with divergent vocabulary (that is the fragmentation this handoff exists to prevent); editing the near-half artifacts without the same delegated/adversarial review discipline that built them.
  - trade-offs: CONSUME avoids judgment-spine doctrine fragmentation (two "learn from backtests" systems) and inherits four landed cross-vendor-hardening passes; it costs a reconciliation of vocabulary (dated-card vs validated-lesson-cell) and gate design (PROVE vs K-of-N). DIFFERENTIATE is faster locally but leaves the owner with two overlapping doctrines on the same spine.
  - owner of the call: the read-machinery architecture-planning lane produces the reconciliation recommendation → **owner sign-off** (the owner has both lanes).
  - recommendation and why: **CONSUME.** The near-half artifacts are landed, cross-vendor-hardened, and already occupy the "near half owns lesson validation" slot the far-half architecture cut. The read-machinery PROVE gate (re-run the same case on a fresh same-family model armed with the candidate lesson; keep only if materially better) is genuinely STRONGER than the near-half promotion gate's K-of-N alone — and the near-half adversarial review already flagged that K-of-N alone is gameable for post-reveal lessons. So the two are complementary: graft PROVE in, keep the near-half citation-disjointness firewall guard + lesson typing, and you get one hardened subsystem.

## Drift Guard

- **Do not re-derive a competing distillation/weighting system.** The near-half ledger + architecture already exist on main; treat them as the substrate to consume or amend-via-review, not a blank slate.
- **Do not edit the near-half artifacts without the same review discipline.** They were each built + cross-vendor reviewed + home-adjudicated; any amendment needs the same delegated/adversarial pass (`.agents/workflow-overlay/delegated-review-patch.md`).
- **The near-half firewall + caps are not reopenable casually.** Blind pre-reveal call = the only judgment score; post-reveal extraction = lower tier (product-learning); JSG-01 frozen (no source-family promotion from a good tally); no schema-as-code; no real rows yet. These are landed doctrine.
- **The read-machinery LIVE verdict core is genuinely YOURS and out of scope here.** This reconciliation is ONLY about the backtest-shell distillation/weighting layer. The "one core, two shells" live core (weight → verdict + action ceiling → counterfactual) and live shell are not duplicated by the near-half work; do not fold them in.
- **Do not graft onto the JSG-01..10 backtest conductor** (your own handoff's guard) — unchanged by this.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (read AGENTS.md + `.agents/workflow-overlay/README.md` first).
- targets to enter the ladder (the NEW substrate this handoff is about):
  - docs/product/judgment_spine/near_half_backtest_learning_architecture_v0.md
  - docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md
  - docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md (the far half; names the "near half owns lesson validation" boundary these fill)
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md (case substrate + K-of-N/report-all discipline both lanes inherit)
- already loaded (weak orientation; not authority): the near-half lane read all of the above on 2026-06-13; treat as stale pointers, re-read.
- must load first (before any strict step): AGENTS.md + overlay README; then the two near-half artifacts (they ARE the substrate to reconcile against).
- load rule: re-run progressive source loading per the overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- **The near half = adversarial-postmortem → validated-lesson cell + promotion gate → emits to the signal-reliability ledger + decision-memory.** A landed PROPOSED architecture; the backtest-learning loop.
  - decided in: docs/product/judgment_spine/near_half_backtest_learning_architecture_v0.md
  - compare target: blob-bytes sha256[:16] `5faf1728f8389870` on origin/main; reread-required.
  - verify before: any design decision about the read-machinery backtest shell.
- **The signal-reliability ledger = per-signal K-of-N reliability across backtest cases (= your "checkpoint #3 per-vertical weighting from past cases").** Landed; a #64 hardening PR is open (adds per-row pre-specified resolution criterion + full denominator).
  - decided in: docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md
  - compare target: blob-bytes sha256[:16] `388352b83bac9860` on origin/main (this is the #54 version; if #64 has landed, the hash will differ — re-read); reread-required.
  - verify before: any design decision about per-vertical source weighting.

## Active Objective

Hand the read-machinery architecture lane the fact that its backtest-shell distillation/weighting layer was independently built and landed by the near-half lane, and the directive to reconcile (consume, don't re-derive). The near-half lane retires after this packet.

## Exact Next Authorized Action

1. In the read-machinery architecture-planning pass, BEFORE designing the backtest-shell distillation tail / dated-card deck / checkpoint-3 weighting, read the two landed near-half artifacts (verify the hashes above).
2. Decide CONSUME vs DIFFERENTIATE (Open Decision); produce the reconciliation as part of the architecture object; fold the PROVE gate into the near-half promotion gate if consuming.
3. Surface the reconciliation recommendation for owner sign-off.
- Stop condition: do not design a second distillation/weighting subsystem before reading the landed near-half artifacts and deciding the Open Decision.

## Authority And Source Ledger

- Repository instructions: AGENTS.md (+ CLAUDE.md shim); `.agents/workflow-overlay/` — reread-required.
- Overlay or equivalent authority: Orca overlay; structure B (human lands PRs); delegated-review-patch convention governs any amendment to the near-half artifacts.
- User constraints: planning/docs tier; product-learning caps; firewall + ladder caps intact; no implementation/scoring engine (your handoff's primary drift); JSG-01 frozen.
- Source-read ledger:
  - `docs/product/judgment_spine/near_half_backtest_learning_architecture_v0.md`
    - Role: the landed near-half architecture (= your distillation tail + lesson store).
    - Load-bearing: yes
    - Compare target: blob-bytes sha256[:16] `5faf1728f8389870` on origin/main
    - Last checked: 2026-06-13
    - Reuse rule: consume as substrate; amend only via a reviewed pass.
  - `docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md`
    - Role: the landed signal-reliability ledger (= your checkpoint-3 weighting substrate).
    - Load-bearing: yes
    - Compare target: blob-bytes sha256[:16] `388352b83bac9860` on origin/main (#54 version; differs if #64 landed)
    - Last checked: 2026-06-13
    - Reuse rule: consume as substrate; the #64 hardening (pre-specified resolution criterion + full denominator) is the current best version.
  - `docs/prompts/handoffs/judgment_spine_read_machinery_architecture_handoff_v0.md`
    - Role: the read-machinery lane's OWN task context (one core, two shells; PROVE gate; checkpoint #3 weighting). Untracked on sender branch ecr-sp3.
    - Load-bearing: yes (the receiver's own goal/decisions live here)
    - Compare target: reread-required (untracked; obtain from ecr-sp3 or wherever it lands)
    - Last checked: 2026-06-13
    - Reuse rule: the receiver's primary context; this packet only adds the near-half-already-built fact.
  - `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md`
    - Role: case substrate + K-of-N/report-all/pre-commitment discipline both lanes inherit.
    - Load-bearing: no (orientation)
    - Compare target: reread-required (on main)
    - Last checked: 2026-06-13
    - Reuse rule: the shared discipline; cases #1 Inoreader / #2 Feedhaven are RETRO/resolved; #3 Beauty Pie / #4 Topicals in execution.
- Source gaps: the read-machinery lane's own handoff + its referenced design/gate files are untracked on ecr-sp3; a fresh lane off main can't see them until they land or are couriered.
- Strict-only blockers: none for planning; any implementation/scoring/seal is out of scope for both lanes.
- Not-proven boundaries: the near-half artifacts are PROPOSED / product-learning / no real rows; this handoff binds nothing and authorizes no edit to them.

## Current Task State

- Completed (near-half lane): far half landed + parked; near-half signal-reliability ledger landed (#54) + open hardening PR #64; near-half architecture landed (#55).
- Partially completed: #64 awaiting land; near-half architecture #55 has no cross-vendor review of its own.
- Broken or uncertain: the cross-lane overlap is unreconciled — the reason for this handoff.

## Workspace State

- Branch: near-half-reconciliation-handoff-v0 (this handoff's PR branch), off origin/main @ 89c2973
- Head: 89c2973
- Dirty or untracked state before handoff: clean (a disposable precompact note from the near-half lane exists untracked at docs/hygiene/precompact_prospective_loop_near_half_lane_v0.md — superseded by this handoff; ignore)
- Dirty or untracked state after writing the handoff file: this handoff file added (its own PR)
- Target files or artifacts: this handoff only.
- Related worktrees or branches: near-half lane worktree orca-prospective-loop-wt; primary worktree C:\Users\vmon7\Desktop\projects\orca on ecr-sp3 (the read-machinery sender branch).

## Changed / Inspected / Tested Files

- `docs/prompts/handoffs/near_half_reconciliation_handoff_to_read_machinery_lane_v0.md`
  - Status: this packet (new).
  - Role: cross-lane handoff.

## The Overlap Map (the load-bearing new fact)

| Read-machinery lane design (yours) | Near-half lane (LANDED) | Relation |
| --- | --- | --- |
| Distillation tail: diagnose → prove → generalize → install | adversarial-postmortem → validated-lesson + promotion gate | same function, different design — RECONCILE |
| "Dated card" / "distillation deck" (survival kernel) | "validated-lesson cell" / decision-memory | same concept, different vocabulary — RECONCILE |
| Checkpoint #3 = per-vertical source weighting from past cases | signal-reliability ledger (per-signal K-of-N from past cases) | same substrate — CONSUME the ledger |
| PROVE gate (rerun same case, fresh same-family model, keep if materially better) | promotion gate (K-of-N report-all on OTHER pre-committed cases) | complementary — FOLD PROVE INTO the near-half gate |
| Live verdict core ("weight → verdict + action ceiling → counterfactual"), live shell | (not in the near half) | GENUINELY SEPARATE — out of scope, keep yours |

## Frozen Decisions

- The near-half artifacts are landed PROPOSED doctrine; they occupy the far-half architecture's "near half owns lesson validation" slot.
  - Evidence: on origin/main (hashes above); far-half architecture's decision-memory/learning-loop sections.
  - Consequence: the read-machinery backtest shell reconciles against them, not from scratch.

## Mutable Questions

- CONSUME vs DIFFERENTIATE (the Open Decision) — resolves via the read-machinery architecture pass + owner sign-off.
- Whether to fold the near-half citation-disjointness firewall guard + lesson typing into the read-machinery design (recommended if consuming).

## Superseded / Dangerous-To-Reuse Context

- The near-half lane's precompact note (docs/hygiene/precompact_prospective_loop_near_half_lane_v0.md).
  - Why stale: written for a same-thread resume that did not happen; the near-half lane retires instead.
  - Current replacement: this handoff.
- Any assumption that the near-half backtest-learning machinery does not exist yet (your handoff's source ledger predates it).
  - Why dangerous: it does exist and is landed; designing as if it doesn't creates the duplication this handoff prevents.
  - Current replacement: the Overlap Map above.

## Commands And Verification Evidence

- Verify the landed near-half artifacts + hashes (confirm-don't-trust):
  ```bash
  git fetch origin main
  git cat-file blob origin/main:docs/product/judgment_spine/near_half_backtest_learning_architecture_v0.md | python -c "import sys,hashlib;print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest()[:16])"   # expect 5faf1728f8389870
  git cat-file blob origin/main:docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md | python -c "import sys,hashlib;print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest()[:16])"   # expect 388352b83bac9860 (or different if #64 landed)
  ```
  Result: passed at authoring (2026-06-13). Re-run target: the receiver runs these before acting.

## Blockers And Risks

- The read-machinery lane could design a duplicate distillation system unaware of the near-half work.
  - Evidence: its handoff's source ledger does not list the near-half artifacts (parallel same-day authoring).
  - Likely next action: read the near-half artifacts first; decide the Open Decision.
- #64 (ledger hardening) may land after this, changing the ledger hash.
  - Evidence: #64 OPEN at authoring.
  - Likely next action: re-read the ledger; use the latest landed version.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts to re-verify: (1) near_half_backtest_learning_architecture_v0.md on main, hash 5faf1728f8389870; (2) near_half_signal_reliability_ledger_v0.md on main, hash 388352b83bac9860 (or #64's); (3) the read-machinery lane's own handoff is the receiver's primary context.
- Compare target for each: the blob-bytes sha256[:16] above; reread-required for the untracked read-machinery handoff.
- Load outcomes: REUSE if both artifacts present at the stated hashes → proceed to the Open Decision. STALE_REREAD_REQUIRED if #64 landed (ledger hash changed) → re-read the ledger. BLOCKED_UNVERIFIABLE if the artifacts are not on main → stop; the substrate claim is unconfirmed.
- Sources to reread if drift: the two near-half artifacts; the far-half architecture's decision-memory boundary.

## Do Not Forget

- The near-half PROVE-gate cross-pollination runs BOTH ways: PROVE strengthens the near-half promotion gate; the near-half citation-disjointness guard + lesson typing strengthen the read-machinery design.
- This handoff binds nothing and authorizes no edit to the near-half artifacts; amendments need a delegated/adversarial review pass.
- The near-half lane retires after this packet — do not expect it to continue as a source of truth.
