# Handoff — 9 Pre-Cutoff Captured Candidate Cases → Judgment-Spine Backtest-Batch Admission (owner-gated, anti-cherry-pick)

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt (docs/prompts/handoffs/)
scope: >
  Cold cross-lane handoff transferring a CANDIDATE POOL of 9 pre-cutoff Wayback
  Source Capture cases (~75 INV-1 units, all merged to main) from the capture
  spine to the judgment-spine backtest-batch owner. These captures are evidence
  inputs, NOT admitted backtest cases: turning them into backtests is gated by
  the batch-ledger anti-cherry-pick discipline (owner pre-declaration, dev/holdout
  split, pinned scoring key, outcome-blind zero-spoiler packets, blind/isolated
  contestant runs, all-results reporting). It carries the corpus location + the
  governing discipline + the open owner decision; it does not admit cases, build
  packets, run contestants, or score, and it grants no judgment-spine authority.
use_when:
  - The judgment-spine batch owner is deciding whether/how to admit new beauty-vertical
    consumer-demand backtest cases.
  - A fresh lane must continue from a cold start the path "captured candidate evidence
    -> backtest-batch admission -> outcome-blind packet -> blind run -> scoring."
authority_boundary: retrieval_only
authored_by: capture-spine Chief-Architect coordination lane (Opus 4.8), 2026-06-15
supersedes: docs/prompts/handoffs/nearhalf_66_consume_capture_corpus_handoff_v0.md (mis-framed: it targeted "PR #66" and free "specimen assembly"; #66 is a retired learning-machinery handoff, and admission is batch-gated -- see Superseded context)
```

## Load Contract

- packet_version: handoff_v0
- mode: max
- created_at: 2026-06-15
- created_by_lane: capture-spine Chief-Architect coordination thread (provenance only; NOT authority)
- workspace: C:\Users\vmon7\Desktop\projects\orca
- handoff_path: docs/prompts/handoffs/captured_candidate_cases_to_judgment_spine_backtest_batch_handoff_v0.md
- expected_branch: authored on worktree branch `nearhalf-66-handoff` (off `origin/main`); a receiving lane spins up its OWN worktree/branch off `origin/main`.
- expected_head: `origin/main` advancing fast (owner merges aggressively); re-fetch. Corpus + governing docs verified present on `origin/main` 2026-06-15.
- expected_dirty_state_including_handoff_file: this handoff file is newly created/untracked on the `nearhalf-66-handoff` worktree until committed.
- load_rule: confirm-don't-trust. Re-verify every load-bearing fact against its compare target before acting. Sender claims are hypotheses, not authority. This whole packet is a weak source class (a prior-thread artifact); rebind fresh source for any strict or actionable claim.

## Prompt-Orchestration Compliance (orca_start_preflight + authoring route)

```yaml
orca_start_preflight:
  agents_md_and_overlay_readme_read: yes   # AGENTS.md + .agents/workflow-overlay/README.md + prompt-orchestration.md read in task context 2026-06-15
  source_pack: bounded_custom              # batch ledger + candidate roster + near-half + read-machinery handoff + the 9 case dirs (see Authority And Source Ledger)
  repo_map_decision: not_needed
  repo_map_reason: cold handoff cites exact verified blob OIDs; no repo-map traversal needed to act
  workspace: C:\Users\vmon7\Desktop\projects\orca
  expected_branch: authored on worktree `nearhalf-66-handoff` off origin/main; receiving lane spins up its own off origin/main
  dirty_state_allowance: this handoff file is newly created + untracked on the worktree (in scope); rest of worktree clean off main
  controlling_source_state: overlay / batch-ledger / near-half / read-machinery docs read clean from a worktree off origin/main 2026-06-15; re-verify (main moves fast)
  doctrine_change: none                    # routes a candidate pool to an existing owner-gated batch process; defines no new doctrine
  target_files: this artifact; receiver targets = the batch ledger + candidate roster + the 9 case dirs + run_case.py
  source_hierarchy: AGENTS.md > .agents/workflow-overlay/ > accepted docs (the batch-1 ledger governs case admission/discipline)
  edit_permission_this_authoring: docs-write
  output_mode: file-write (this artifact) + paste-ready-chat (courier prompt)
  validation_gates: header_index.py --strict (retrieval header present); check_map_links.py --strict
  external_source_boundary: jb is NOT Orca authority; external workflow source is read-only from Orca work
authoring_route:
  authored_via: workflow-handoff (state-packet mechanics) + workflow-prompt-orchestrator (prompt-orchestration contract applied)
  contract_applied: .agents/workflow-overlay/prompt-orchestration.md applied in full (Implementation handoff family, preflight, output-mode, validation gates, leakage check)
  not_a_claim: not validation, not readiness, not implementation authorization, not source promotion
receiver_authority:
  edit_permission: docs-write WITHIN the judgment-spine batch lane; NEVER edit capture packets (INV-1); amend the batch ledger only by dated note with owner sign-off (never silent rewrite)
  output_mode: file-write under judgment-spine lane authority; land via per-lane PR (human-gated merge)
  not_authorized_by_this_handoff: judgment-spine execution authority, case admission, scoring-key change, or live-API calls -- all owner-gated; capture coordination only transfers inputs + the governing discipline + the open decision
  model_lane: unbound  # blind contestant panel / scoring lanes are owner-set in the batch ledger; no routing claimed here
```

## Goal Handoff

Sender-derived from bound context (no `workflow-goal-framing` artifact; orientation only, not authority):

- long_term_goal: Orca's demand calls become trustworthy enough that a decision owner allocates (and eventually pays) against them — trust earned by method, not asserted.
- anchor_goal: Get the 9 captured candidate cases (pre-cutoff evidence already built + merged) **admitted and run as backtests under the batch-ledger discipline** — owner pre-declaration, outcome-blind packets, blind contestant runs, pinned-key scoring — so their results can feed the judgment-spine learning machinery, **without violating the anti-cherry-pick property** (the captures were selected outcome-aware, so admission must pre-commit the set and report all results).
- success_signal: A dated, owner-signed batch-admission decision (which of the 9 enter, into a new batch or as a dated amendment to batch 1, with dev/holdout split + pinned-key confirmation), followed by outcome-blind zero-spoiler packet construction → blind runs → `run_case.py` scoring → one findings record per case, **all results reported**. NOT success: hand-assembling "specimens" that bake in the known outcome, admitting only cases where the signal looks right, or routing raw captures to the near-half / read-machinery lanes.

## Open Decision / Fork

- decision: **How to admit the 9 captured candidate cases into the backtest batch — and which ones — under the anti-cherry-pick discipline.**
  - options: (i) **new Batch 2 declaration** (pre-declare the full admitted set + dev/holdout split + pinned key before any gate-0/outcome reveal); (ii) **dated amendment to the Batch 1 ledger** admitting them (the ledger is amended by dated note, never silent rewrite); (iii) **admit a subset**, pre-committing the selection rule before reveal.
  - already constrained / off the table: post-hoc per-case admission correlated with favorability (the selection bias the ledger exists to prevent — cf. the org-motion pre-commitment amendment); editing the batch ledger without owner sign-off; changing the pinned scoring key (a key change stops/rolls the batch); promoting any source-family off a good tally; JSG-01 unfreeze.
  - trade-offs: a new Batch 2 keeps Batch 1's closed pre-commitment intact and lets the new set carry its own (possibly refined) case-quality rubric (deferred to "next batch" per the ledger); a dated amendment is lighter but must still pre-commit the full set + run-on-all to preserve anti-cherry-pick.
  - owner of the call: **the judgment-spine batch owner** (the Batch 1 ledger is `BATCH1_ACTIVE_OWNER_SIGNED`; case admission was owner-selected in-thread).
  - recommendation and why: **new Batch 2 declaration**, pre-committing the full admitted set + run-on-all + all-results reporting *before* any outcome-aware step, so the outcome-aware capture selection cannot leak into favorability. The 9 cases are beauty-vertical consumer-demand decisions (the relaxed Batch 1 family), so they fit the same rubric.

## Drift Guard

- **Anti-cherry-pick / pre-commitment (load-bearing).** Admission must be pre-declared with all results reported (in-band/over/under, failures, swaps, exclusions). The 9 captures were selected outcome-aware (their dirs/notes encode the decision + later outcome), so admission MUST pre-commit the full set + run-on-all, or the batch's anti-cherry-pick property is void.
  - what violating it breaks: the backtest measures selection skill, not judgment; results are uninterpretable.
- **Outcome-blind packet construction.** Contestant packets must be zero-spoiler, built by an actor NOT holding the sealed outcome. The capture case dirs are outcome-labelled; the contestant packet is a DERIVED, stripped artifact, not the raw case dir.
- **Blind / isolated contestant runs.** Fresh isolated sessions, web-off (structural where possible, recorded), non-inducing pre-judgment isolation screen, tell-audit for outcome-USE (contamination = recorded-as-data, not discarded). Scoring via `orca-harness/runners/run_case.py` against the pinned key.
- **INV-1 on the capture packets.** The merged capture packets are observed facts + limits only; reuse them AS source evidence, never edit them to add scores/weights/ranks/verdicts.
- **#66 / near-half / read-machinery are DOWNSTREAM of results, not consumers of raw captures.** Do NOT route the capture corpus to those lanes. The near-half learning machinery consumes backtest *results* (signal-reliability ledger, lesson distillation); the read-machinery live design consumes the learning machinery. (See the layer map in Inherited Context.)
- **Caps unchanged.** Product-learning tier, small N; JSG-01 frozen; not live-API authorization; not validation/readiness/buyer proof. Capture coordination grants no judgment-spine execution authority.

## Inherited Context (does NOT flow to a new lane)

### The layer map (the load-bearing reframe)

```text
L1  Capture corpus (THIS handoff's payload)  = pre-cutoff Wayback source evidence; a CANDIDATE POOL.
        |  owner-gated batch admission (anti-cherry-pick) -> outcome-blind packet -> blind run -> run_case.py scoring
        v
L2  Backtest batch (batch-1 ledger governs)  = admitted cases + findings records (all results reported).
        |  results feed
        v
L3  Near-half learning machinery (#66)       = signal-reliability ledger + lesson distillation/weighting.
        |  consumed by
        v
L4  Read-machinery live design ("one core, two shells") = the live demand-read judgment machine.
```

The capture corpus is **L1**. Its next step is **L2 admission** (owner-gated). #66 is **L3**; the read-machinery handoff is **L4**. They are NOT the consumer of raw captures.

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: read `.agents/workflow-overlay/README.md` first, then follow the Orca overlay; `AGENTS.md` is triggers + global behavior. (Overlay-bound, NOT zero-config.)
- targets to enter the ladder: the Batch 1 ledger; the candidate-pool roster; the 9 case dirs under `orca-harness/cases/product_learning/`; `run_case.py` (scoring); the Inoreader findings record (exemplar shape, cited by the ledger).
- already loaded (weak orientation; not authority): only this packet (a prior-thread artifact, 2026-06-15).
- must load first (before any strict step): `AGENTS.md` + overlay README; then the Batch 1 ledger (it governs admission + discipline).
- load rule: re-run progressive source loading per the overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- Batch admission is owner-pre-declared + anti-cherry-pick + dev/holdout + pinned-key + blind-run — gist above.
  - decided in: `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md` (compare target: blob `94b56233` on origin/main). verify before: any admission step.
- The org-motion amendments show the precedent for admitting a NEW signal/case-set without selection bias: pre-commit the run-on-all set + blind prediction + report-all *before* the reveal.
  - decided in: the same ledger (Amendment — Org-Motion Batch Pre-Commitment). verify before: designing the Batch 2 pre-commitment.
- #66 = a RETIRED near-half→read-machinery reconciliation handoff (learning machinery), NOT the corpus consumer.
  - decided in: `docs/prompts/handoffs/near_half_reconciliation_handoff_to_read_machinery_lane_v0.md` (on PR #66 / branch near-half-reconciliation-handoff-v0). verify before: any claim about #66's role.
- The read-machinery live design (L4) is a separate, not-yet-started architecture pass.
  - decided in: `docs/prompts/handoffs/judgment_spine_read_machinery_architecture_handoff_v0.md` (compare target: blob `db0ec52a` on origin/main). verify before: any claim about the live machine.

## Active Objective

Transfer the 9 captured candidate cases to the judgment-spine batch owner with the governing anti-cherry-pick discipline made explicit, so the owner can decide batch admission (the open decision) — after which the standard batch flow (outcome-blind packet → blind run → `run_case.py` scoring → findings record, all reported) produces results that feed the learning machinery.

## Exact Next Authorized Action

1. Load admission authority: read `judgment_spine_backtest_batch1_ledger_declaration_v0.md` (verify blob `94b56233`) and the candidate-pool roster (blob `b26fb9c1`); confirm the anti-cherry-pick + dev/holdout + pinned-key + blind-run discipline.
2. Cross-check the 9 captured cases against the candidate roster + the ledger's case-family + recognition/fame screen; flag any that fail (e.g. brand-fame recognition risk).
3. Surface the **open decision** to the owner: new Batch 2 vs dated amendment, which cases, dev/holdout split, pinned-key confirmation — pre-committing the admitted set + run-on-all + report-all BEFORE any outcome-aware step.
4. On owner sign-off only: construct outcome-blind zero-spoiler packets (by an actor not holding the outcome) → blind/isolated contestant runs → `run_case.py` scoring against the pinned key → one findings record per case.
5. Stop condition: do NOT admit cases, build packets, run contestants, score, route captures to #66/read-machinery, or claim any backtest result without owner batch-admission sign-off. Do not claim validation/readiness.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` + `.agents/workflow-overlay/` (read overlay `README.md` first). Reread-required.
- Overlay or equivalent authority: the Batch 1 ledger owns case admission + discipline; per-lane PR flow + human-gated merge (`docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`).
- User constraints: confirm-don't-trust; owner merges fast; product-learning cap; JSG-01 frozen; no scoring-key change; no live-API without its own authorization.
- Source-read ledger:
  - `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md`
    - Role: THE backtest-batch governance — case list (#1–#6), anti-cherry-pick, dev/holdout, pinned key, blind-run execution rules, org-motion pre-commitment precedent.
    - Load-bearing: yes
    - Compare target: blob `94b5623325cb2f558f5858b98efdb796312351a4` on `origin/main`
    - Last checked: 2026-06-15
    - Reuse rule: re-read before any admission step; amend only by dated owner-signed note.
  - `docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md`
    - Role: the candidate roster the 9 cases were drawn from (FAME/NON-US/WEAK flags).
    - Load-bearing: yes
    - Compare target: blob `b26fb9c17be91d8a52b1c5e9eb9824285a2f63cb` on `origin/main`
    - Last checked: 2026-06-15
    - Reuse rule: cross-check each captured case against it before admission.
  - `orca-harness/runners/run_case.py`
    - Role: deterministic scoring against the pinned key (the batch's scoring path).
    - Load-bearing: yes (only at the scoring step)
    - Compare target: blob `4f1c55c9e8188e03112446ccc22954bc0df89f3e` on `origin/main`
    - Last checked: 2026-06-15
    - Reuse rule: run against the pinned key only; a key change stops the batch.
  - `docs/prompts/handoffs/near_half_reconciliation_handoff_to_read_machinery_lane_v0.md`
    - Role: #66 — the RETIRED near-half→read-machinery handoff (L3 context; NOT the corpus consumer).
    - Load-bearing: no (context that prevents re-conflation)
    - Compare target: on PR #66 / branch `near-half-reconciliation-handoff-v0`; reread-required (not on main).
    - Last checked: 2026-06-15
    - Reuse rule: read to understand the downstream layer; do not route captures here.
  - `docs/prompts/handoffs/judgment_spine_read_machinery_architecture_handoff_v0.md`
    - Role: the L4 live read-machinery design pass (downstream of L3).
    - Load-bearing: no (context)
    - Compare target: blob `db0ec52acc94dab9b75cb425851feefe595e87f6` on `origin/main`
    - Last checked: 2026-06-15
    - Reuse rule: context only.
  - `docs/product/judgment_spine/near_half_backtest_learning_architecture_v0.md`
    - Role: L3 near-half learning machinery (consumes batch results).
    - Load-bearing: no (context)
    - Compare target: blob `138f8374c66633e936b07b3e080244984df5dfa4` on `origin/main`
    - Last checked: 2026-06-15
    - Reuse rule: context only; not a consumer of raw captures.
  - `orca-harness/cases/product_learning/<case>/` (9 cases; see Corpus Inventory)
    - Role: the captured candidate evidence (L1 payload), INV-1.
    - Load-bearing: yes
    - Compare target: present on `origin/main`; verify with `git ls-tree -r origin/main --name-only orca-harness/cases/product_learning/<case>`; body-faithfulness via body-sha vs manifest.
    - Last checked: 2026-06-15
    - Reuse rule: read per case; never edit (INV-1).
- Source gaps: the per-case recognition/fame screen results are not pre-computed here; the receiver runs them. Whether a new Batch 2 case-quality rubric exists yet is unknown (the ledger defers it to "next batch").
- Strict-only blockers: case admission, scoring-key change, live-API, fixture admission, JSG-01 unfreeze — all owner-gated; landing to `main` human-gated.
- Not-proven boundaries: the captures are pre-cutoff evidence ONLY — NOT admitted cases, NOT backtest results, NOT validation/readiness.

### Corpus Inventory (verified on `origin/main`, 2026-06-15)

75 units across 9 cases (count = `manifest.json` files per case dir):

- `kinderbeauty_box_pivot_2023_v0` — 11 · `cocokind_holdprice_2025_v0` — 10 · `joahbeauty_cvs_kill_2024_v0` — 11 · `privatepacks_retail_retreat_v0` — 9 · `sundaily_gummy_pivot_v0` — 6 (sundots.com) · `saie_price_increase_2025_v0` — 10 · `selflessbyhyram_target_entry_2023_v0` — 6 · `nueco_fragrance_pivot_v0` — 7 · `imaginaryauthors_sku_kills_2024_v0` — 5.

NOT part of this pool: `beautypie_repricing_2023_v0` + `topicals_retail_expansion_2021_v0` (FROZEN fixtures; already Batch 1 cases #3/#4); `feedhaven_repricing_2019_anon_v0` + `inoreader_repricing_2019_v0` (Batch 1 #1/#2, RETRO/resolved).

## Current Task State

- Completed: the 9-case / 75-unit capture corpus is built, byte-faithful, pre-cutoff, INV-1 clean, MERGED to `origin/main`.
- Partially completed: nothing on batch admission — the corpus has never been admitted, packetized-blind, run, or scored. This handoff initiates that path at the owner-decision step.
- Broken or uncertain: which cases pass the recognition/fame + case-family screen; whether they go to Batch 2 or a Batch 1 amendment (the open decision).

## Workspace State

- Branch: authored on worktree `nearhalf-66-handoff` (off `origin/main`). Also on this PR: it supersedes the mis-framed `nearhalf_66_consume_capture_corpus_handoff_v0.md` (removed in the same change).
- Head: `origin/main` (re-fetch; moves fast).
- Dirty/untracked before handoff: clean off main on this worktree except this lane's files.
- Dirty/untracked after writing the handoff file: + this handoff file (and the removal of the superseded file).
- Target files or artifacts: the Batch 1 ledger; candidate roster; the 9 case dirs; `run_case.py`.
- Related worktrees/branches: `orca-judgment-read-machinery-wt` (L4 read-machinery lane); `orca-prospective-loop-wt` (the retired near-half lane / #66).

## Frozen Decisions

- Backtest case admission is owner-pre-declared + anti-cherry-pick; the Batch 1 ledger is amended only by dated owner-signed note.
  - Evidence: `judgment_spine_backtest_batch1_ledger_declaration_v0.md` (blob `94b56233`).
  - Consequence: the 9 cases cannot be silently turned into backtests; admission is the gated open decision.
- INV-1 on capture packets; Beauty Pie 2023 + Topicals 2021 frozen (already Batch 1 #3/#4).
  - Consequence: do not edit captures; do not re-derive the frozen fixtures.

## Mutable Questions

- New Batch 2 vs dated amendment to Batch 1? Which of the 9? Dev/holdout split? — resolves via owner sign-off.
- Which captured cases fail the recognition/fame or case-family screen? — resolves by running the screen per case.
- Does a Batch 2 case-quality rubric exist yet (the ledger defers it to "next batch")? — verify before declaring Batch 2.

## Superseded / Dangerous-To-Reuse Context

- `docs/prompts/handoffs/nearhalf_66_consume_capture_corpus_handoff_v0.md` (this handoff's prior version, removed in the same change).
  - Why dangerous: it framed the target as "drive PR #66 / the judgment-spine near-half lane" and the method as free "consume the corpus into Unity specimens." Both wrong: #66 is a retired learning-machinery (L3) handoff, not the corpus consumer; and turning captures into backtests is batch-admission-gated (anti-cherry-pick), not free specimen authoring.
  - Current replacement: this packet (the layer map + the batch-admission discipline).
- Any assumption that the capture corpus can be hand-assembled into backtest specimens without owner batch admission.
  - Why dangerous: it bypasses the anti-cherry-pick property and produces uninterpretable, contaminated results.
  - Current replacement: the Open Decision + the batch flow (outcome-blind packet → blind run → score).

## Commands And Verification Evidence

- Command:
  ```bash
  git fetch origin main
  git ls-tree origin/main docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md   # blob 94b56233...
  for c in kinderbeauty_box_pivot_2023_v0 cocokind_holdprice_2025_v0 joahbeauty_cvs_kill_2024_v0 \
           privatepacks_retail_retreat_v0 sundaily_gummy_pivot_v0 saie_price_increase_2025_v0 \
           selflessbyhyram_target_entry_2023_v0 nueco_fragrance_pivot_v0 imaginaryauthors_sku_kills_2024_v0; do
    git ls-tree -r origin/main --name-only "orca-harness/cases/product_learning/$c" | grep -c '/manifest.json$'
  done   # 11,10,11,9,6,10,6,7,5 = 75
  ```
  Result: passed (2026-06-15). Re-run target: the receiver confirms the ledger + corpus before acting.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts to re-verify before acting: (1) the Batch 1 ledger on main (blob `94b56233`) and its anti-cherry-pick/admission rules; (2) the candidate roster (blob `b26fb9c1`); (3) the 9-case / 75-unit corpus present + byte-faithful on main; (4) `run_case.py` (blob `4f1c55c9`).
- Load outcomes: `REUSE` (all verified — proceed to the Open Decision); `STALE_REREAD_REQUIRED` (main moved / a blob changed — re-read); `BLOCKED_DRIFT` (ledger admission rules changed); `BLOCKED_UNVERIFIABLE` (a load-bearing source missing — stop); `BLOCKED_MISSING_PACKET` (this file unreadable).
- Sources to reread if drift: the Batch 1 ledger + the candidate roster + the affected case dir.

## Do Not Forget

- The captures are L1 evidence (a candidate pool), not admitted backtest cases — admission is owner-gated and anti-cherry-pick.
- The captures were selected outcome-aware; admission MUST pre-commit the set + run-on-all + report-all, or the batch's anti-cherry-pick property is void.
- #66 (near-half) and the read-machinery design are L3/L4 — downstream of backtest *results*; do NOT route raw captures to them.
- Capture coordination grants no judgment-spine execution authority; case admission, packets, runs, and scoring are the batch owner's.
