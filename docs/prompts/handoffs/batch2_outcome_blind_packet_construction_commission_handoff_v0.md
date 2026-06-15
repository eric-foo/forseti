# Handoff — Batch 2 Outcome-Blind Packet Construction → Blind Runs → Scoring (owner-authorized, anti-cherry-pick)

```yaml
retrieval_header_version: 1
artifact_role: Implementation handoff prompt (docs/prompts/handoffs/)
scope: >
  Cold cross-lane handoff routing a fresh lane to execute the owner-signed
  Judgment-Spine Backtest Batch 2: build OUTCOME-BLIND zero-spoiler contestant
  packets for the 9 admitted captured cases, run them blind/isolated, score via
  run_case.py against the pinned key, and write one findings record per case —
  ALL results reported. The Batch 2 ledger (BATCH2_ACTIVE_OWNER_SIGNED) governs
  and authorizes this batch flow at product-learning tier. The commissioning
  thread is OUTCOME-AWARE and therefore does NOT build packets or run
  contestants; construction is delegated to an outcome-blind subagent per the
  conductor construction-integrity mechanism. This handoff grants no new
  authority beyond the signed ledger; it carries the execution discipline + the
  source ledger + the open execution-design forks.
use_when:
  - Executing the Batch 2 backtest flow after the ledger is signed.
  - Standing up outcome-blind packet construction → blind run → scoring for a
    pre-committed beauty-vertical consumer-demand backtest set.
authority_boundary: retrieval_only
authored_by: judgment-spine batch-2 coordination lane (Opus 4.8), 2026-06-16
supersedes: none
```

## Load Contract

- packet_version: handoff_v0
- mode: max
- created_at: 2026-06-16
- created_by_lane: judgment-spine batch-2 coordination thread (provenance only; NOT authority)
- workspace: C:\Users\vmon7\Desktop\projects\orca
- handoff_path: docs/prompts/handoffs/batch2_outcome_blind_packet_construction_commission_handoff_v0.md
- expected_branch: a receiving lane spins up its OWN worktree/branch off `origin/main`.
- expected_head: `origin/main` at/after `4ce549f1` (merged ledger PR #164); re-fetch (main moves fast).
- expected_dirty_state: clean off main on the receiving worktree except this lane's files.
- load_rule: confirm-don't-trust. Re-verify every load-bearing fact against its compare target before acting. Sender claims are hypotheses, not authority. This whole packet is a weak source class (a prior-thread artifact); rebind fresh source for any strict or actionable claim.

## Prompt-Orchestration Compliance (orca_start_preflight + authoring route)

```yaml
orca_start_preflight:
  agents_md_and_overlay_readme_read: yes   # AGENTS.md + overlay README + prompt-orchestration.md read in authoring context 2026-06-16
  source_pack: bounded_custom              # signed ledger + conductor addendum v1 + gate-ownership map + roster + run_case.py + scoring key + the 9 case dirs
  repo_map_decision: not_needed
  repo_map_reason: cold handoff cites exact verified blob OIDs; no repo-map traversal needed to act
  workspace: C:\Users\vmon7\Desktop\projects\orca
  expected_branch: receiving lane spins up its own worktree/branch off origin/main
  dirty_state_allowance: this handoff file is newly created on the authoring lane; receiving lane works clean off main
  controlling_source_state: overlay / ledger / conductor / gate-map read clean from a worktree off origin/main 2026-06-16; re-verify (main moves fast)
  doctrine_change: none                    # routes ledger-authorized execution; defines no new doctrine
  target_files: this artifact; receiver targets = the 9 case dirs (read, INV-1) + new packet/findings artifacts under orca-harness + run_case.py
  source_hierarchy: AGENTS.md > .agents/workflow-overlay/ > accepted docs (the signed Batch 2 ledger governs this batch)
  edit_permission_this_authoring: docs-write
  output_mode: file-write (this artifact) + paste-ready-chat (courier prompt)
  validation_gates: header_index.py --strict (retrieval header present); check_map_links.py --strict
  external_source_boundary: jb is NOT Orca authority; external workflow source is read-only from Orca work
authoring_route:
  authored_via: workflow-handoff (state-packet shape) + workflow-prompt-orchestrator (prompt-orchestration contract applied in full)
  contract_applied: .agents/workflow-overlay/prompt-orchestration.md (Implementation handoff family, preflight, output-mode, validation gates, source-gated method contract, leakage check)
  not_a_claim: not validation, not readiness, not a new execution authorization beyond the signed ledger, not source promotion
receiver_authority:
  edit_permission: docs-write + bounded harness-write WITHIN the judgment-spine batch lane, AS AUTHORIZED BY THE SIGNED LEDGER (by-hand runs + run_case.py scoring at product-learning tier); NEVER edit the capture packets (INV-1); amend the ledger only by dated owner-signed note
  output_mode: file-write under judgment-spine lane authority; land via per-lane PR (human-gated merge)
  not_authorized_by_this_handoff: scoring-key change, live raw-API calls, fixture admission, JSG-01 unfreeze, new case admission, buyer contact — all still owner-gated; this handoff routes only the ledger-authorized packet→run→score flow
  model_lane: unbound  # the blind contestant panel is owner-set in the ledger (Batch-1 panel); no runtime model routing claimed here
```

## Goal Handoff

Carried verbatim from the 2026-06-15 goal frame (orientation only, not authority):

```yaml
goal_handoff:
  long_term_goal: Orca demand calls become trustworthy enough that an owner allocates/pays against them — trust earned by method.
  anchor_goal: Admit + run the 9 captured pre-cutoff cases as backtests under batch-ledger anti-cherry-pick discipline, results feeding L3.
  success_signal:
    core_success:
      owner_observable: Dated owner-signed admission decision, then one all-results findings record per admitted case.
      output_fit: Pre-commit set + run-on-all + report-all BEFORE any outcome-aware step, auditably.
      boundary: Not corpus-built, not doc-exists, not a subset tally, not routing to L3/L4, not validation/readiness.
      drift_cue: Selective admission/reporting; INV-1 edits; outcome-aware specimen assembly; "built"=="done".
    secondary_success_signals:
      - Mirrors org-motion pre-commitment (run-on-all + blind prediction + report-all).
      - Results interpretable as judgment skill, not selection skill.
      - Findings feed L3 near-half machinery cleanly.
  status: inferred_thread_local
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
  if_changed_reason: "Admission sub-goal is now COMPLETE (ledger signed + merged); the live sub-step is the run phase (packet → blind run → score → findings). Same anchor goal."
```

## Open Decision / Fork (receiver-resolved; escalate to owner only if a real choice arises)

The owner-gated decisions are already CLOSED by the signed ledger (set, split, key pin, panel). What remains is execution-design, to be resolved by the receiving lane against the harness + conductor:

- **Pilot sequencing (recommended):** build + run a **dev** case first (`cocokind` or `saie`) to shake out packet shape and the scoring path, then the remaining 8. The ledger marks the dev pair for exactly this. Run-on-all still binds: all 9 must be built + run + reported.
- **Packet schema / freeze shape:** confirm the zero-spoiler contestant-packet structure (JSG-02/JSG-03 freezes, JSG-04 provenance) against the harness + conductor before building; do not invent a schema if one is bound.
- **Outcome-hint neutralization:** the case **dir names themselves hint the outcome** (`..._cvs_kill_...`, `..._pivot_...`, `..._price_increase_...`). The blind builder subagent must receive **neutralized case identifiers** (e.g., `case-A`) + the stripped pre-cutoff evidence only — not the outcome-laden dir name, notes, or roster outcome columns. Decide the neutralization mapping at construction time; keep the mapping with the outcome-holding orchestrator, not the blind subagent.

## Drift Guard

- **Anti-cherry-pick / run-on-all (load-bearing).** All 9 admitted cases are built, run, and reported — in-band / over / under, failures, exclusions, swaps, quarantines. Selective construction or selective reporting **voids** the batch's anti-cherry-pick property. The set is already pre-committed in the ledger; do not narrow it.
- **Outcome-blind construction (load-bearing).** Per conductor addendum v1 **R2**: construction is delegated to an **outcome-blind subagent**; the subagent's **outcome-excluded prompt/transcript IS the receipt** (actor-separation + input-separation: outcome material withheld and NAMED + hash-binding to the frozen packet/ledger; not-proven default if any of these is missing). The commissioning/orchestrating actor may be outcome-aware but **must not build the packet itself or leak the outcome into the subagent's inputs**. Single-operator memory leak = a disclosed product-learning-tier residual, not a hard gate.
- **Blind / isolated runs.** Fresh isolated sessions, web search OFF (structural where the surface allows; recorded → `isolation_result == proven`). A **non-inducing pre-judgment isolation screen** precedes any judgment; **active recall is dropped** (recognition capacity alone is NOT contamination). The blind judgment MUST include a **reasoning trace** (JSG-06). Contamination = **outcome-USE**, caught by **tell-auditing the trace at JSG-08**; a confirmed tell → hard contaminated route → **quarantine = recorded-as-data, not discarded**. `selflessbyhyram` carries a famous founder → isolation screen mandatory, first swap candidate only if isolation cannot be proven.
- **Dev/holdout discipline.** Dev (`cocokind`, `saie`) may inform method/packet critique; **holdouts (the 7 pivots) run once under the pinned key and are only reported** — no key or harness iteration may condition on them.
- **INV-1 on the capture packets.** The merged captures are observed facts + limits only; reuse them AS source evidence, **never edit** them to add scores/weights/ranks/verdicts.
- **Pinned key unchanged.** Score only via `run_case.py` against the frozen key (`band_scorer.py` + `mapping_table.py`, the ledger `input_hashes`). A key change **stops/rolls the batch**; proposed key changes belong only in the closing distillation record.
- **Caps.** Product-learning tier, small N; JSG-01 frozen; NOT live-API authorization; NOT validation/readiness/buyer-proof. **Org-motion is out of scope for Batch 2.**
- **Do NOT route raw captures to #66 / read-machinery (L3/L4).** They consume backtest *results*, not raw captures.

## Inherited Context (does NOT flow to a new lane)

### The layer map (where this lane sits)

```text
L1  Capture corpus (the 9 cases)        = pre-cutoff source evidence (INV-1).
        |  THIS LANE: outcome-blind packet -> blind run -> run_case.py score -> findings record (all reported)
        v
L2  Backtest batch (Batch 2 ledger)     = admitted cases + findings records.   <-- this lane produces the findings
        |  results feed
        v
L3  Near-half learning machinery (#66)  = signal-reliability ledger + lesson distillation.
        v
L4  Read-machinery live design          = the live demand-read judgment machine.
```

This lane is the **L2 execution** step that turns the signed admission into reported results. It does not touch L3/L4.

### The outcome-blind construction mechanism (conductor addendum v1, R2 — by-hand norm)

- Construction is **delegated to an outcome-blind subagent**. Its **outcome-excluded prompt/transcript is the receipt** a reviewer can read to confirm exclusion. This also gives actor-separation (distinct context).
- Evidence-backed outcome-blind clearance needs: (a) `constructor_session_ref` != outcome-holder; (b) the outcome material withheld and **named**; (c) hash-binding to the frozen packet/ledger; (d) **not-proven default** if any of a–c is missing.
- The blind subagent must satisfy the overlay **source-gated method contract**: give it the same source pack or a bounded source capsule (the stripped pre-cutoff evidence), not just a method + question; require its own `SOURCE_CONTEXT_READY` gate; bind a terse schema-bound return.

### Source-loading state to re-establish (overlay doctrine)

- Read `.agents/workflow-overlay/README.md` first, then follow the Orca overlay; `AGENTS.md` is triggers + global behavior.
- Targets to enter the ladder: the **signed Batch 2 ledger** (governs); the **conductor addendum v1** (construction integrity); the **gate-ownership map** (JSG gates); `run_case.py` + the **pinned key**; the **9 case dirs**; the Inoreader findings record (exemplar shape).
- already loaded (weak orientation; not authority): only this packet.
- must load first (before any strict step): `AGENTS.md` + overlay README; then the signed Batch 2 ledger.

## Active Objective

Execute the owner-signed Batch 2 batch flow at product-learning tier: for each of the 9 admitted cases, build an outcome-blind zero-spoiler contestant packet (via a blind subagent), run the Batch-1 panel blind/isolated (web-off, isolation screen, reasoning trace), tell-audit the trace at JSG-08, score via `run_case.py` against the pinned key, and write one findings record per case — **all results reported** — so the results can feed the L3 learning machinery.

## Exact Next Authorized Action

1. Re-fetch `origin/main`; re-verify the Load Checklist compare targets (ledger blob `482d8169`, conductor v1 `ede29148`, gate-map `0135ad5a`, `run_case.py` `4f1c55c9`, key SHA-256 `d54dcd2c`/`8bfd4830`, the 9 case dirs present = 75 units). Return one load outcome.
2. Read the signed ledger + conductor addendum v1 + gate-ownership map; confirm the construction-integrity mechanism (R2) and the JSG sequence (JSG-02/03 freeze → JSG-04 provenance → JSG-05 isolation → JSG-06 trace → JSG-08 tell-audit).
3. Confirm the contestant-packet schema against the harness/conductor (do not invent one if bound). Decide the outcome-hint neutralization mapping (case-IDs), held by the outcome-holding orchestrator.
4. **Pilot:** build the outcome-blind packet for one **dev** case (`cocokind` or `saie`) via a blind subagent (outcome-excluded prompt = receipt; record `constructor_session_ref`, withheld-material name, packet hash). Shake out packet shape + the scoring path.
5. Build the remaining packets (run-on-all). Per-unit re-verify **pre-cutoff** + **byte-faithfulness** (body-sha vs manifest) before any run.
6. Run the Batch-1 panel blind/isolated (web-off; isolation screen; reasoning trace required). Tell-audit each trace at JSG-08; contaminated arms = recorded-as-data.
7. Score each case via `run_case.py` against the pinned key; write one findings record per case (Inoreader record = exemplar shape); **report all** results.
8. Stop condition: do NOT change the scoring key, make live-API calls, admit new cases, route captures to #66/read-machinery, or claim validation/readiness/buyer-proof. Land via per-lane PR (human-gated).

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` + `.agents/workflow-overlay/` (read overlay `README.md` first). Reread-required.
- Governing authority: the **signed Batch 2 ledger** owns this batch's set/split/key/panel/discipline; per-lane PR + human-gated merge (`docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`).
- User constraints: confirm-don't-trust; owner merges fast; product-learning cap; JSG-01 frozen; no scoring-key change; no live-API without its own authorization.
- Source-read ledger:
  - `docs/decisions/judgment_spine_backtest_batch2_ledger_declaration_v0.md`
    - Role: THE Batch 2 governance — admitted set, dev/holdout split, pinned key, panel, anti-cherry-pick + all-results reporting, execution rules.
    - Load-bearing: yes. Compare target: blob `482d8169` on `origin/main`. Reuse rule: re-read before any build/run/score; amend only by dated owner-signed note.
  - `docs/product/judgment_spine/conductor_construction_integrity_probe_addendum_v1.md`
    - Role: the outcome-blind construction-integrity mechanism (R2 subagent-delegation; R3/R5 isolation; R4 reasoning-trace tell-audit). PROPOSED v1 — applies as by-hand discipline.
    - Load-bearing: yes. Compare target: blob `ede29148` on `origin/main`.
  - `docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md`
    - Role: JSG gate ownership (freezes, provenance, isolation screen, reasoning trace, tell-audit).
    - Load-bearing: yes. Compare target: blob `0135ad5a` on `origin/main`.
  - `docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md`
    - Role: candidate roster (case→flags). **Spoiler-bearing** (outcome columns) — keep with the outcome-holding orchestrator; withhold from the blind builder.
    - Load-bearing: yes (orchestrator only). Compare target: blob `b26fb9c1` on `origin/main`.
  - `orca-harness/runners/run_case.py`
    - Role: deterministic scoring against the pinned key.
    - Load-bearing: yes (scoring step). Compare target: blob `4f1c55c9` on `origin/main`. Reuse rule: pinned key only; a key change stops the batch.
  - `orca-harness/scoring/band_scorer.py` + `orca-harness/scoring/mapping_table.py`
    - Role: the frozen pinned key (ledger `input_hashes`).
    - Load-bearing: yes (scoring step). Compare target: SHA-256 `d54dcd2c…` / `8bfd4830…` (blobs `0456b02e` / `b8e634fd`) on `origin/main`.
  - `orca-harness/cases/product_learning/inoreader_repricing_2019_v0/cross_vendor_blind_run_findings_v0.md`
    - Role: exemplar findings-record shape.
    - Load-bearing: no (template). Compare target: present on `origin/main`.
  - `orca-harness/cases/product_learning/<case>/` (the 9 cases; see Corpus Inventory)
    - Role: the L1 captured evidence, INV-1; **outcome-labelled** (dir names/notes hint outcome).
    - Load-bearing: yes. Compare target: present on `origin/main`; verify per case + body-sha vs manifest. Reuse rule: read per case; never edit (INV-1); neutralize identifiers for the blind builder.
- Source gaps: the exact contestant-packet schema + the neutralization mapping are resolved by the receiver against the harness/conductor.
- Strict-only blockers: scoring-key change, live-API, fixture admission, JSG-01 unfreeze, new case admission — all owner-gated; landing to `main` human-gated.
- Not-proven boundaries: results are product-learning-tier learning signal — NOT validation/readiness/buyer-proof.

### Corpus Inventory (verified on `origin/main`, 2026-06-16)

75 units across 9 cases (count = `manifest.json` per case dir). `[dev]` / `[holdout]` per the ledger:

- `cocokind_holdprice_2025_v0` — 10 **[dev]** · `saie_price_increase_2025_v0` — 10 **[dev]**
- `kinderbeauty_box_pivot_2023_v0` — 11 [holdout] · `joahbeauty_cvs_kill_2024_v0` — 11 [holdout] · `privatepacks_retail_retreat_v0` — 9 [holdout] · `selflessbyhyram_target_entry_2023_v0` — 6 [holdout] · `sundaily_gummy_pivot_v0` — 6 [holdout] · `nueco_fragrance_pivot_v0` — 7 [holdout] · `imaginaryauthors_sku_kills_2024_v0` — 5 [holdout]

## Current Task State

- Completed: Batch 2 ledger DECLARED + owner-SIGNED + MERGED to `origin/main` (`BATCH2_ACTIVE_OWNER_SIGNED`, PR #164). Set/split/key/panel pre-committed.
- Partially completed: nothing on execution — no packet built, no run, no score, no findings record. This handoff initiates the run phase.
- Broken or uncertain: the contestant-packet schema + outcome-hint neutralization mapping (receiver resolves against harness/conductor).

## Frozen Decisions

- Batch 2 admitted set, dev/holdout split, frozen scoring key, and panel are owner-signed in the ledger; amend only by dated owner-signed note.
  - Evidence: `judgment_spine_backtest_batch2_ledger_declaration_v0.md` (blob `482d8169`).
  - Consequence: this lane executes the set as-pre-committed; it does not re-select, re-split, or re-key.
- INV-1 on capture packets; outcome-blind construction required (R2).
  - Consequence: never edit captures; never build a packet while holding the outcome — delegate to a blind subagent.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts to re-verify before acting: (1) signed ledger on main (blob `482d8169`) + its set/split/key/discipline; (2) conductor addendum v1 (blob `ede29148`) R2 mechanism; (3) gate-ownership map (blob `0135ad5a`); (4) `run_case.py` (blob `4f1c55c9`) + pinned key SHA-256 (`d54dcd2c`/`8bfd4830`); (5) the 9 case dirs present + 75 units + byte-faithful.
- Load outcomes: `REUSE` (all verified — proceed to the pilot); `STALE_REREAD_REQUIRED` (main moved / a blob changed — re-read); `BLOCKED_DRIFT` (ledger/key changed — stop); `BLOCKED_UNVERIFIABLE` (a load-bearing source missing — stop); `BLOCKED_MISSING_PACKET` (this file unreadable).

## Do Not Forget

- The set is pre-committed: all 9 are built + run + reported. No selective construction or reporting.
- The commissioning/orchestrating actor is outcome-aware → must NOT build packets or run contestants; delegate construction to an outcome-blind subagent (its outcome-excluded prompt/transcript is the receipt).
- Holdouts (the 7 pivots) run once under the pinned key and are only reported — no method/key iteration conditioned on them.
- Score only via `run_case.py` against the frozen key; a key change stops the batch.
- Results are product-learning learning signal — not validation/readiness/buyer-proof. Do not route raw captures to #66/read-machinery.
