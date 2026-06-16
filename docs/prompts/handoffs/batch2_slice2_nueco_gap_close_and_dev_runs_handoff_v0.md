# Handoff — Batch 2 Slice 2: close the nueco anti-cherry-pick gap + run the dev arm (Claude-Sonnet)

```yaml
retrieval_header_version: 1
artifact_role: Implementation handoff prompt (docs/prompts/handoffs/)
scope: >
  Cold cross-lane handoff for Batch 2 execution SLICE 2. Slice 1 (#172) ran the
  Claude-Sonnet contestant arm for 6 of the 7 pre-committed holdout cases and
  built (but did not blind-run) the 2 dev-case packets. The 7th holdout — nueco
  (The Nue Co., owner-included border US/UK case) — was SILENTLY DROPPED: no
  packet, no run, no findings, no recorded exclusion. Slice 2 closes that
  anti-cherry-pick gap (nueco full pipeline, reported) and completes the dev
  arm (cocokind + saie blind Sonnet runs), mirroring slice-1 artifact shape,
  under the signed Batch 2 ledger and the conductor outcome-blind discipline.
use_when:
  - Closing the nueco run-on-all gap and finishing the Claude-Sonnet arm for Batch 2.
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
- handoff_path: docs/prompts/handoffs/batch2_slice2_nueco_gap_close_and_dev_runs_handoff_v0.md
- expected_branch: a receiving lane spins up its OWN worktree/branch off `origin/main`.
- expected_head: `origin/main` at/after `431b6dcc` (slice-1 PR #172); re-fetch (main moves fast).
- expected_dirty_state_including_handoff_file: clean off main on the receiving worktree except this lane's files; this handoff file is newly created/untracked on the authoring lane until committed.
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Authoring Route (prompt-orchestration compliance)

```yaml
authoring_route:
  authored_via: workflow-handoff (cold state-packet mechanics)
  contract_applied: .agents/workflow-overlay/prompt-orchestration.md (Implementation handoff family; docs/prompts/handoffs/; file-write; header_index.py --strict + check_map_links.py --strict gates; confirm-don't-trust load contract)
  courier: the paste-ready routing prompt that points a fresh lane at this packet is produced via workflow-prompt-orchestrator (composes with this state packet)
  not_a_claim: not validation, not readiness, not a new execution authorization beyond the signed Batch 2 ledger, not source promotion
```

## Goal Handoff

Carried verbatim from the 2026-06-15 goal frame (orientation only, not authority):

- long_term_goal: Orca demand calls become trustworthy enough that an owner allocates/pays against them — trust earned by method.
- anchor_goal: Admit + run the 9 captured pre-cutoff cases as backtests under batch-ledger anti-cherry-pick discipline, results feeding L3.
- success_signal: a findings record per case with ALL results reported; output fit = run-on-all + report-all with no selective construction/reporting; NOT success = a pre-committed case left silently un-run.

```yaml
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
  if_changed_reason: "Same anchor goal; sub-step = finish the Claude-Sonnet arm (nueco gap + dev runs) so all 9 cases are covered for this arm."
```

## Open Decision / Fork

- decision: **How to close the nueco gap** (the owner-included 7th holdout dropped from slice 1).
  - options: (i) **run nueco like the other 6 holdouts** — full pipeline (outcome-blind packet → blind Sonnet run → findings → case_report), report whatever it scores; (ii) **only if a real feasibility/capture blocker is found**, record a **documented exclusion** (explicit reason, owner-noted) — a *documented* exclusion preserves anti-cherry-pick; a *silent* drop does not.
  - already constrained / off the table: leaving nueco silently un-run and un-reported (voids the batch's anti-cherry-pick property); admitting a *replacement* for nueco without a dated owner-signed ledger amendment.
  - trade-offs: nueco has captures present (7 units), so option (i) should be feasible; the border US/UK flag is an inclusion/owner-routing note, not a capture blocker. Option (ii) applies only if the receiver finds a concrete blocker (e.g., a corrupt/empty capture or a cutoff problem).
  - owner of the call: the **judgment-spine batch owner**. The receiver runs nueco by default; escalate to the owner only if it finds a real blocker that would force option (ii).
  - recommendation and why: **option (i) — run nueco.** It is the pre-committed 7th holdout; running + reporting it (whatever the score) is what restores run-on-all. Do it FIRST (it is the discipline gap), then the dev runs.
- secondary fork (dev arm): cocokind + saie packets already exist (JSG-02 freeze done in #172) but were **not blind-run**. Run the blind Sonnet arm + findings for both; dev cases run **once**. No real owner decision here — sequencing only (after nueco).

## Drift Guard

- **Close the nueco gap — do not let it stay dropped (load-bearing).** The signed ledger pre-commits 7 holdouts incl. nueco; slice 1 covered 6. The slice-1 commit's "6 holdout" framing is WRONG vs the ledger. nueco must be run + reported (or documented-excluded with a real reason), or the anti-cherry-pick property is void.
- **Claude contestant pinned to Sonnet-class — NOT Opus.** The ledger panel is "Claude Sonnet-class"; running the Claude arm on Opus is off-panel and would need recording as a deviation/re-run. (Slice 1 correctly used Sonnet.)
- **Outcome-blind construction (conductor v1 R2).** Build packets via an **outcome-blind subagent** (outcome-excluded prompt/transcript = receipt; actor + input separation; hash-bound; not-proven default if missing). The orchestrator may be outcome-aware but must NOT build the packet itself or leak the outcome to the subagent. nueco's dir name (`..._fragrance_pivot_...`) hints the outcome → give the blind builder a neutralized case-ID + stripped pre-cutoff evidence only.
- **Anti-cherry-pick / report-all.** Report nueco's and the dev cases' results whatever they are (in-band / over / under / failure / quarantine). No selective reporting.
- **Blind runs.** Fresh isolated session, web-off (`isolation_result == proven`), non-inducing isolation screen, reasoning trace required (JSG-06), JSG-08 tell-audit (outcome-USE → contaminated/quarantine = recorded-as-data).
- **Dev/holdout.** nueco is a **holdout** → run once under the pinned key, only reported, no method/key iteration conditioned on it. cocokind/saie are **dev** → may inform method, run once.
- **INV-1 captures** (never edit to add scores/verdicts); **frozen key** (score only via `run_case.py`; a key change stops the batch); **product-learning cap** (not validation/readiness/buyer-proof); **do NOT route raw captures to #66 / read-machinery (L3/L4)**.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: read `.agents/workflow-overlay/README.md` first, then follow the Orca overlay; `AGENTS.md` is triggers + global behavior.
- targets to enter the ladder: the **signed Batch 2 ledger** (governs); **conductor addendum v1** (R2 construction integrity); **gate-ownership map** (JSG gates); the **slice-1 commission handoff** (the construction/run discipline + the layer map); a **slice-1 exemplar case** (e.g. `joahbeauty_cvs_kill_2024_v0`) for artifact shape; `run_case.py` + the pinned key; the nueco + dev case dirs.
- already loaded (weak orientation; not authority): only this packet.
- must load first (before any strict step): `AGENTS.md` + overlay README; then the signed Batch 2 ledger + the commission handoff.
- load rule: receiver re-runs progressive source loading per the overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- **The batch is owner-signed + anti-cherry-pick (7 holdouts + 2 dev = 9, run-on-all + report-all).**
  - decided in: `docs/decisions/judgment_spine_backtest_batch2_ledger_declaration_v0.md` (compare target: blob `482d8169` on origin/main). verify before: any run/score/report step.
- **Outcome-blind packet construction is delegated to a blind subagent (R2 by-hand norm).**
  - decided in: `docs/product/judgment_spine/conductor_construction_integrity_probe_addendum_v1.md` (compare target: blob `ede29148`). verify before: building any packet.
- **The full slice construction→run→score discipline + layer map.**
  - decided in: `docs/prompts/handoffs/batch2_outcome_blind_packet_construction_commission_handoff_v0.md` (compare target: blob `075183c0`). verify before: any actionable step.
- **Slice-1 per-case artifact shape to MIRROR (so slice-2 artifacts are consistent):** per case dir under `orca-harness/cases/product_learning/<case>/` — `participant_packet.md`, `evidence/e0NN.yaml`, `facilitator_ledger.yaml` (carries `decision_shape`, band, `ledger_freeze_hash`), `packet_construction_receipt_v0.md` (records the R2 chain: blind subagent + orchestrator fixes), `runs/claude_sonnet_isolated_subagent_v0/run_001/blind_judgement.yaml`, `cross_vendor_blind_run_findings_v0.md`; plus a report at `orca-harness/reports/product_learning/<case>/case_report.yaml`. Scores are **gitignored** (`.gitignore:35`).
  - decided in: the merged slice-1 tree (compare target: present on origin/main `431b6dcc`; inspect `joahbeauty_cvs_kill_2024_v0` as the worked example). verify before: building nueco's packet (match the shape).

## Active Objective

Finish the Claude-Sonnet contestant arm for all 9 Batch 2 cases: (1) close the nueco gap — build its outcome-blind packet, blind-run it on Sonnet-class, write its findings record + case_report, report the result; (2) complete the dev arm — blind-run cocokind + saie on Sonnet-class against their already-built packets, write findings + case_reports. Mirror slice-1 artifact shape. Report all results. Land via per-lane PR (human-gated).

## Exact Next Authorized Action

1. Spin up your own worktree/branch off `origin/main`; re-fetch; re-verify the Load Checklist compare targets (ledger `482d8169`, conductor `ede29148`, gate-map `0135ad5a`, commission handoff `075183c0`, `run_case.py` `4f1c55c9`, pinned key SHA-256 `d54dcd2c`/`8bfd4830`, nueco captures present, slice-1 exemplar artifacts present). Return one load outcome.
2. Investigate the nueco skip: confirm nueco's `source_captures/` are present + byte-faithful and there is **no** real feasibility/capture blocker. If a concrete blocker exists, STOP and surface a **documented exclusion** for owner sign-off (option ii). Otherwise proceed (option i).
3. **nueco full pipeline:** outcome-blind packet via a blind subagent (mirror slice-1 shape: `participant_packet.md` + `evidence/` + `facilitator_ledger.yaml` + `packet_construction_receipt_v0.md`) → blind **Sonnet-class** run (web-off, isolation screen, reasoning trace) → JSG-08 tell-audit → `cross_vendor_blind_run_findings_v0.md` + `reports/product_learning/nueco_fragrance_pivot_v0/case_report.yaml`. Report the result whatever it is.
4. **Dev arm (cocokind, saie):** verify their existing packets were built outcome-blind (per their `packet_construction_receipt_v0.md`); blind-run each **once** on Sonnet-class → findings record + case_report. Score via `run_case.py` against the pinned key.
5. Stop conditions: Sonnet-class not Opus; no scoring-key change; no live-API; no new case admission; no L3/L4 routing of raw captures; product-learning cap. Land via per-lane PR (human-gated). Do not claim validation/readiness.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` + `.agents/workflow-overlay/` (read overlay `README.md` first). Reread-required.
- Governing authority: the **signed Batch 2 ledger** owns set/split/key/panel/discipline; per-lane PR + human-gated merge (`docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`).
- User constraints: confirm-don't-trust; owner merges fast; product-learning cap; JSG-01 frozen; no scoring-key change; no live-API without its own authorization; Claude arm = Sonnet-class.
- Source-read ledger:
  - `docs/decisions/judgment_spine_backtest_batch2_ledger_declaration_v0.md` — Role: Batch 2 governance (7 holdouts incl. nueco + 2 dev; anti-cherry-pick; pinned key; panel). Load-bearing: yes. Compare target: blob `482d8169` on origin/main. Last checked: 2026-06-16. Reuse rule: re-read before any run; amend only by dated owner-signed note.
  - `docs/product/judgment_spine/conductor_construction_integrity_probe_addendum_v1.md` — Role: outcome-blind R2 mechanism. Load-bearing: yes. Compare target: blob `ede29148`. Last checked: 2026-06-16.
  - `docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md` — Role: JSG gates (freeze/provenance/isolation/trace/tell-audit). Load-bearing: yes. Compare target: blob `0135ad5a`. Last checked: 2026-06-16.
  - `docs/prompts/handoffs/batch2_outcome_blind_packet_construction_commission_handoff_v0.md` — Role: full slice construction/run discipline + layer map. Load-bearing: yes. Compare target: blob `075183c0`. Last checked: 2026-06-16.
  - `orca-harness/runners/run_case.py` — Role: deterministic scoring vs pinned key. Load-bearing: yes (scoring). Compare target: blob `4f1c55c9`. Reuse rule: pinned key only; a key change stops the batch.
  - `orca-harness/scoring/band_scorer.py` + `mapping_table.py` — Role: frozen pinned key (ledger `input_hashes`). Load-bearing: yes (scoring). Compare target: SHA-256 `d54dcd2c…` / `8bfd4830…`.
  - `orca-harness/cases/product_learning/nueco_fragrance_pivot_v0/` — Role: the un-run holdout (captures present; **no execution artifacts** as of `431b6dcc`). Load-bearing: yes. Compare target: only `source_provenance_notes_v0.md` + `source_captures/` present on origin/main; no packet/run/findings. Reuse rule: read captures; never edit (INV-1); neutralize the dir-name outcome hint for the blind builder.
  - `orca-harness/cases/product_learning/cocokind_holdprice_2025_v0/` + `saie_price_increase_2025_v0/` — Role: dev cases; packets BUILT, blind run NOT done. Load-bearing: yes. Compare target: `participant_packet.md` + `evidence/` + `facilitator_ledger.yaml` + `packet_construction_receipt_v0.md` present; **no `runs/.../blind_judgement.yaml`**. Reuse rule: run once; verify packet was built outcome-blind before running.
  - `orca-harness/cases/product_learning/joahbeauty_cvs_kill_2024_v0/` — Role: slice-1 exemplar (full run footprint to mirror). Load-bearing: no (template). Compare target: present on origin/main `431b6dcc`.
- Source gaps: the exact reason nueco was skipped in slice 1 is **not recorded anywhere** (checked: no execution-deferral note for nueco outside its case dir). Treat as a silent oversight to be closed, not a decision.
- Strict-only blockers: scoring-key change, live-API, fixture admission, JSG-01 unfreeze, new case admission — owner-gated; landing to main human-gated.
- Not-proven boundaries: results are product-learning learning signal — NOT validation/readiness/buyer-proof. Slice-1 results are one arm (Sonnet) of a multi-model panel; the external arms (GPT/Grok/Gemini) are owner-executed and not in this lane.

## Current Task State

- Completed: 6 holdouts (`kinderbeauty`, `joahbeauty`, `privatepacks`, `selflessbyhyram`, `sundaily`, `imaginaryauthors`) fully packet-built + blind-Sonnet-run + findings + case_report (slice 1, PR #172, `431b6dcc`). Dev packets (`cocokind`, `saie`) built (JSG-02 freeze).
- Partially completed: dev cases (`cocokind`, `saie`) have packets but **no blind run / no findings**.
- Broken or uncertain: **`nueco` is entirely un-started** (captures only; no packet/run/findings/exclusion) — the anti-cherry-pick gap this lane closes. The *cause* of the skip is unrecorded.

## Workspace State

- Branch: receiving lane spins up its own off `origin/main`.
- Head: `origin/main` `431b6dcc` (re-fetch).
- Dirty/untracked before handoff: clean off main except this lane's files.
- Dirty/untracked after writing the handoff file: + this handoff file.
- Target files or artifacts: `nueco_fragrance_pivot_v0/` (new packet+run+findings), `cocokind_*` + `saie_*` (new runs+findings), `orca-harness/reports/product_learning/<case>/case_report.yaml`.
- Related worktrees/branches: slice-1 branch `batch2-backtest-execution-slice1` (merged via #172).

## Frozen Decisions

- Batch 2 admitted set (9), split (7 holdout incl. nueco / 2 dev), frozen key, and panel (Claude Sonnet-class + GPT-5.5 + Grok 4 + Gemini) are owner-signed; amend only by dated owner-signed note.
  - Evidence: `judgment_spine_backtest_batch2_ledger_declaration_v0.md` (blob `482d8169`).
  - Consequence: nueco is in-set; it cannot be dropped — only run, or documented-excluded with owner sign-off.
- INV-1 on captures; outcome-blind construction (R2); Claude arm = Sonnet-class.

## Mutable Questions

- Did nueco have a real feasibility/capture blocker, or was it a pure oversight? — resolves by inspecting nueco's captures + provenance notes; default assumption is oversight (captures present).
- Were the cocokind/saie packets built cleanly outcome-blind? — resolves by reading their `packet_construction_receipt_v0.md` before running.

## Superseded / Dangerous-To-Reuse Context

- The slice-1 commit (#172) framing of **"6 holdout cases"** as the holdout set.
  - Why dangerous: the signed ledger's holdout set is **7** (incl. nueco). Treating "6 holdouts" as complete coverage perpetuates the silent drop and voids anti-cherry-pick.
  - Current replacement: 7 holdouts; nueco is the missing one this lane closes.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts to re-verify before acting: (1) signed ledger (blob `482d8169`) + the 7-holdout set incl. nueco; (2) conductor v1 (blob `ede29148`) R2; (3) gate-ownership map (blob `0135ad5a`); (4) commission handoff (blob `075183c0`); (5) `run_case.py` (blob `4f1c55c9`) + pinned key SHA-256; (6) nueco un-run (captures only) + dev packets built-not-run + slice-1 exemplar shape.
- Load outcomes: `REUSE` (all verified — proceed to nueco); `STALE_REREAD_REQUIRED` (main moved / a blob changed — re-read); `BLOCKED_DRIFT` (ledger/key changed — stop); `BLOCKED_UNVERIFIABLE` (a load-bearing source missing — stop); `BLOCKED_MISSING_PACKET` (this file unreadable).
- Sources to reread if drift: the signed ledger + the commission handoff + the affected case dir.

## Do Not Forget

- nueco (owner-included 7th holdout) was silently dropped — closing it (run + report, or documented-exclude) is the PRIMARY job; a silent drop voids anti-cherry-pick.
- Claude arm = Sonnet-class, not Opus.
- Orchestrator is outcome-aware → delegate packet construction to an outcome-blind subagent; never build the packet yourself or leak the outcome.
- Holdout (nueco) runs once under the pinned key, only reported; dev (cocokind/saie) run once. Mirror slice-1 artifact shape.
- Results are product-learning signal — not validation/readiness/buyer-proof; do not route raw captures to #66/read-machinery.
