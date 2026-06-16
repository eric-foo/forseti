# Handoff — Batch 2 External Arms: START the GPT-5.5 + Grok 4 runs

```yaml
retrieval_header_version: 1
artifact_role: Implementation handoff prompt (docs/prompts/handoffs/)
scope: >
  Cold cross-runtime "run it" handoff: gives a fresh operator/lane everything to
  START and complete the Batch 2 external contestant runs for GPT-5.5 and Grok 4
  (Gemini deferred) on all 9 product-learning cases, score them on the frozen key,
  and report all results. Sits on top of the merged external-arm commission
  (#178) and the merged paste-and-score helper (#180); both are on origin/main.
use_when:
  - Running the GPT-5.5 and/or Grok 4 contestant arm for Batch 2 and reporting results.
authority_boundary: retrieval_only
authored_by: judgment-spine batch-2 coordination lane (Opus 4.8), 2026-06-16
supersedes: none
```

## Authoring Route (prompt-orchestration compliance)

```yaml
authoring_route:
  authored_via: workflow-handoff (cold cross-lane state-packet mechanics)
  contract_applied: .agents/workflow-overlay/prompt-orchestration.md (Implementation handoff family; docs/prompts/handoffs/; file-write; header_index.py --strict + check_map_links.py --strict gates; confirm-don't-trust load contract)
  composes_with: the merged external-arm commission handoff (docs/prompts/handoffs/batch2_external_arms_run_commission_handoff_v0.md) — that doc owns the per-arm run mechanics; this packet is the cold START state for it.
  not_a_claim: not validation, not readiness, not a new execution authorization beyond the signed Batch 2 ledger + band ratification.
```

## Load Contract

- packet_version: handoff_v0
- mode: max
- created_at: 2026-06-16
- created_by_lane: judgment-spine batch-2 coordination thread (provenance only; NOT authority)
- workspace: C:\Users\vmon7\Desktop\projects\orca
- handoff_path: docs/prompts/handoffs/batch2_external_arms_run_start_handoff_v0.md
- expected_branch: receiving lane spins up its OWN worktree/branch off `origin/main`.
- expected_head: `origin/main` at/after `c5d03455` (helper PR #180 merge); re-fetch (main moves fast).
- expected_dirty_state_including_handoff_file: clean off main except this lane's files; this handoff file is newly created/untracked on the authoring lane until committed.
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

Carried verbatim (orientation only, not authority):

- long_term_goal: Orca demand calls become trustworthy enough that an owner allocates/pays against them — trust earned by method.
- anchor_goal: Admit + run the 9 captured pre-cutoff cases as backtests under batch-ledger anti-cherry-pick discipline, results feeding L3.
- success_signal: a findings/score record per case PER ARM with ALL results reported; output fit = run-on-all + report-all with no selective construction/reporting.

```yaml
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
  if_changed_reason: "Same anchor goal; sub-step = run the GPT-5.5 + Grok 4 contestant arms so 2 of the 3 remaining panel arms are covered."
```

## Open Decision / Fork

- decision: **Where/how each external arm is run isolated, and what to do if a runtime cannot isolate the model.**
  - options: (i) run each model in a runtime where it IS the contestant and can be isolated (fresh session, web/tools OFF, no outside/post-cutoff knowledge, target `tool_uses=0`) — e.g. a GPT runtime for GPT-5.5, an xAI runtime for Grok 4; (ii) if a given runtime cannot run the named model isolated, record a **documented block** for that (arm, case) and move on.
  - already constrained / off the table: substituting a different model for the named contestant; fabricating a contestant answer; iterating method on holdouts to chase a score; running with web/tools on.
  - trade-offs: option (i) gives a clean blind run; option (ii) preserves honesty when isolation is impossible. Never (iii) fake a run to fill the matrix.
  - owner of the call: the operator running each arm (sequencing only — no owner sign-off needed to proceed; the set/split/key/panel are already owner-signed).
  - recommendation and why: run GPT-5.5 first across all 9, then Grok 4 across all 9 (batching by model keeps one isolated session context per arm). Use `--dry-run` once per case to sanity-check the parse before the real score.

## Drift Guard

- **Contestant must BE the named external model, isolated.** The operator may be outcome-aware; the contestant is blind — it sees ONLY the exam (packet + must-address items + ladder + schema), never the band, `frozen_band_inputs`, or `spoiler_inventory`.
- **Frozen key + owner-ratified bands.** Pinned key SHA-256 `d54dcd2c…` / `8bfd4830…` is unchanged; bands are owner-ratified (band ratification record, #178). Score ONLY via `run_case.py` / the helper. A key or band change stops/rolls the batch.
- **Anti-cherry-pick / report-all.** Run all 9 per arm; report EVERY result (in-band / over / under / escalate / failure / quarantine). No selective reporting; no quietly dropping a bad result. Holdouts run once (report-only, no method iteration); dev cases (cocokind, saie) run once.
- **JSG-08 tell-audit.** Capture the contestant's recognition self-report. Contamination = demonstrated outcome-USE → quarantine (recorded-as-data); recognition alone is NOT contamination. Watch the **saie** pattern the Claude arm flagged: recognition + recommendation-aligns-with-actual-outcome → flag and record as data, don't silently treat as clean.
- **Load-bearing citation.** Every `load_bearing` claim must cite ≥1 evidence id or the scorer logs a blocking `evidence_id_missing` event (this bit both Claude dev runs). The exam already reminds the contestant; if you re-assemble an exam, keep that reminder.
- **nueco neutralization.** nueco's contestant-facing case_id is `b2_holdout_h7_v0`. Never surface the real dir name (`nueco_fragrance_pivot_v0`) or its capture `manifest.json`/`receipt.md` (which state the post-cutoff outcome) to the contestant. Its committed packet already carries the neutral id.
- **INV-1 captures** (never edit to add scores/verdicts); **product-learning cap**; **do NOT route raw captures to #66 / read-machinery (L3/L4)**.
- **Helper is ingest-only.** `score_external_run.py` only wraps a reply you provide; it never invents a contestant answer.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: read `.agents/workflow-overlay/README.md` first, then follow the Orca overlay; `AGENTS.md` is triggers + global behavior.
- targets to enter the ladder: the merged **external-arm commission handoff** (run mechanics), the **band ratification** record, the **signed Batch 2 ledger**, `score_external_run.py` + `run_case.py` + the pinned key, and any case dir under `orca-harness/cases/product_learning/`.
- already loaded (weak orientation; not authority): only this packet.
- must load first (before any strict step): `AGENTS.md` + overlay README; then the commission handoff + the signed ledger.
- load rule: receiver re-runs progressive source loading per the overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- **The batch is owner-signed + anti-cherry-pick (7 holdouts + 2 dev = 9; run-on-all + report-all).**
  - decided in: `docs/decisions/judgment_spine_backtest_batch2_ledger_declaration_v0.md` (compare target: blob `482d8169` on origin/main). verify before: any run/score/report step.
- **The bands are owner-ratified (the scoring key the contestant is graded against).**
  - decided in: `docs/decisions/judgment_spine_backtest_batch2_band_ratification_v0.md` (compare target: blob `746d23cd`). verify before: relying on any band.
- **The per-arm run mechanics (assemble exam → isolated run → write → score → findings).**
  - decided in: `docs/prompts/handoffs/batch2_external_arms_run_commission_handoff_v0.md` (compare target: blob `da693bed`). verify before: any actionable step.
- **The Claude-Sonnet arm is already complete for all 9 cases (slice 1 #172 + slice 2 #177).** Each case dir holds a `runs/claude_sonnet_isolated_subagent_v0/run_001/blind_judgement.yaml` + `cross_vendor_blind_run_findings_v0.md` to MIRROR for shape. nueco's findings flag the in-band-but-opposite-to-hindsight result; saie's flag the recognition/alignment caveat.
  - compare target: present on origin/main `c5d03455`; inspect any case dir.

## Active Objective

Run GPT-5.5 (`gpt55_isolated_v0`) and Grok 4 (`grok4_isolated_v0`) as blind contestants on all 9 Batch 2 cases (18 runs), score each on the frozen key via the helper, append each arm's result to the case's findings, and report ALL results. This covers 2 of the 3 remaining panel arms (Gemini deferred).

## Exact Next Authorized Action

1. Spin up your own worktree/branch off `origin/main`; re-fetch; run the Confirm-Don't-Trust Load Checklist below. Return one load outcome.
2. Obtain the 9 exams. They live at `_scratch/batch2_external_exams/<case>__EXAM.txt` on the coordinator machine (gitignored — NOT in the repo). If you do not have them, **re-assemble** each from the case's committed `participant_packet.md` (verbatim) + its `facilitator_ledger.yaml` `must_address_items`, wrapped in the exam template documented in the commission handoff + that folder's `README.md`. Exact exam text need not be byte-identical (the helper's `prompt_hash` is an audit field, not a correctness gate) — but it MUST contain only the packet + must-address + ladder + schema, never the band.
3. For each model M ∈ {`gpt55`, `grok4`} and each of the 9 cases: open the exam → paste into a FRESH M session (web/tools OFF, no outside/post-cutoff knowledge) → save the whole reply (the ```yaml block + the `RECOGNITION SELF-REPORT:` line) to a file → run:
   `python orca-harness/runners/score_external_run.py --model M --case <alias> --reply <file>`
   (add `--dry-run` first to preview band/verdict/recognition without writing). The helper wraps the blind_judgement metadata, validates, writes `runs/<contestant_id>/run_001/blind_judgement.yaml`, and scores on the pinned key.
4. Append the arm's row to the case's `cross_vendor_blind_run_findings_v0.md` (call vs band, recognition self-report, isolation basis, any failure events). Report whatever it scores.
5. Stop conditions: contestant not the named model; web/tools on; scoring-key or band change; new case admission; L3/L4 routing of raw captures. If a runtime can't isolate the model, record a documented block — do NOT fake a run. Land via per-lane PR (human-gated). Do not claim validation/readiness.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` + `.agents/workflow-overlay/` (read overlay `README.md` first). Reread-required.
- Governing authority: the signed Batch 2 ledger owns set/split/key/panel/discipline; the band ratification owns the accepted answer key; the commission handoff owns the per-arm run mechanics; per-lane PR + human-gated merge.
- User constraints: confirm-don't-trust; product-learning cap; no scoring-key/band change; Claude arm done; external arms owner-run; scope THIS handoff to GPT-5.5 + Grok 4 (Gemini deferred).
- Source-read ledger:
  - `docs/prompts/handoffs/batch2_external_arms_run_commission_handoff_v0.md` — Role: per-arm run mechanics. Load-bearing: yes. Compare target: blob `da693bed` on origin/main. Last checked: 2026-06-16. Reuse rule: re-read before any run.
  - `docs/decisions/judgment_spine_backtest_batch2_band_ratification_v0.md` — Role: owner-accepted bands. Load-bearing: yes. Compare target: blob `746d23cd`. Last checked: 2026-06-16.
  - `docs/decisions/judgment_spine_backtest_batch2_ledger_declaration_v0.md` — Role: batch governance. Load-bearing: yes. Compare target: blob `482d8169`. Last checked: 2026-06-16.
  - `orca-harness/runners/score_external_run.py` — Role: paste-and-score helper. Load-bearing: yes. Compare target: blob `63f3db1c`. Last checked: 2026-06-16. Reuse rule: ingest-only; run from a checkout (project root inferred as `orca-harness/`).
  - `orca-harness/runners/run_case.py` — Role: deterministic scoring vs pinned key. Load-bearing: yes. Compare target: blob `4f1c55c9`.
  - `orca-harness/scoring/band_scorer.py` + `mapping_table.py` — Role: frozen pinned key. Load-bearing: yes (scoring). Compare target: SHA-256 `d54dcd2c…` / `8bfd4830…`. Reuse rule: a key change stops the batch.
  - `_scratch/batch2_external_exams/` — Role: 9 pre-assembled exams + README (operator convenience). Load-bearing: no (regenerable from packets+ledgers). Compare target: `reread-required` (gitignored local scratch; not in the repo; may be absent on a fresh machine).
- Source gaps: the assembled exams are NOT committed (local scratch); a fresh-machine operator regenerates them from the committed packets+ledgers.
- Strict-only blockers: scoring-key change, band change, live-API beyond a contestant run, new case admission, L3/L4 routing — owner-gated; landing to main human-gated.
- Not-proven boundaries: results are product-learning learning signal — NOT validation/readiness/buyer-proof. The full-panel verdict still needs all arms; this handoff covers 2 of 3 external arms.

## Current Task State

- Completed: Claude-Sonnet arm for all 9 cases (merged #172, #177). Band ratification + external-arm commission merged (#178). Paste-and-score helper merged (#180). 9 exams assembled (local scratch).
- Partially completed: external panel — GPT-5.5 + Grok 4 + Gemini all un-run.
- Broken or uncertain: none known; the only open item is executing the external runs in runtimes that have those models.

## Workspace State

- Branch: receiving lane spins up its own off `origin/main`.
- Head: `origin/main` `c5d03455` (re-fetch).
- Dirty/untracked before handoff: clean off main except this lane's files.
- Dirty/untracked after writing the handoff file: + this handoff file (newly untracked).
- Target files or artifacts (created by the runs): per case, `runs/gpt55_isolated_v0/run_001/blind_judgement.yaml` + `runs/grok4_isolated_v0/run_001/blind_judgement.yaml`; updated `cross_vendor_blind_run_findings_v0.md`; regenerated `reports/product_learning/<case_id>/case_report.yaml` (scores under `scores/` are gitignored).
- Related worktrees/branches: none required; spin up fresh.

## The 9 cases (aliases, contestant ids, bands — bands are OPERATOR-ONLY, never shown to the contestant)

- Models: `gpt55` → contestant_id `gpt55_isolated_v0` (model_id `gpt-5.5`, family `openai_gpt`); `grok4` → `grok4_isolated_v0` (model_id `grok-4`, family `xai_grok`).
- Cases (alias → dir | role | band):
  - `kinderbeauty` → kinderbeauty_box_pivot_2023_v0 | holdout | [3,4]
  - `joahbeauty` → joahbeauty_cvs_kill_2024_v0 | holdout | [6,6]
  - `privatepacks` → privatepacks_retail_retreat_v0 | holdout | [6,6]
  - `selfless` → selflessbyhyram_target_entry_2023_v0 | holdout | [3,4]
  - `sundaily` → sundaily_gummy_pivot_v0 | holdout | [6,6]
  - `imaginaryauthors` → imaginaryauthors_sku_kills_2024_v0 | holdout | [3,5]
  - `nueco` → nueco_fragrance_pivot_v0 (contestant-facing id b2_holdout_h7_v0) | holdout | [3,5]
  - `cocokind` → cocokind_holdprice_2025_v0 | dev | [1,4]
  - `saie` → saie_price_increase_2025_v0 | dev | [3,4]

## Frozen Decisions

- Batch 2 admitted set (9), split (7 holdout incl. nueco / 2 dev), frozen key, panel, and the owner-ratified bands are owner-signed; amend only by dated owner-signed note.
  - Evidence: `judgment_spine_backtest_batch2_ledger_declaration_v0.md` (blob `482d8169`) + `…batch2_band_ratification_v0.md` (blob `746d23cd`).
  - Consequence: contestants are graded against these exact bands; do not change them.
- Claude arm = Sonnet; external arms = GPT-5.5 / Grok 4 / Gemini, each isolated, each its own `contestant_id`.

## Mutable Questions

- Does each available runtime run its model truly isolated (web off, tool_uses=0)? — resolves at run time; if not, documented-block that (arm, case).
- Will the external contestants reproduce the load-bearing-citation miss the Claude dev runs showed? — resolves by observing the scorer's failure events; report either way.

## Superseded / Dangerous-To-Reuse Context

- Any earlier note that #180 (the helper) is "OPEN" or "not yet on main."
  - Why dangerous: it is now MERGED (origin/main `c5d03455`, blob `63f3db1c`); waiting on it would stall.
  - Current replacement: the helper is on `main`; pull and use it.

## Commands And Verification Evidence

- Verify the load-bearing blobs (re-run to confirm, don't trust):
  ```bash
  git fetch origin
  git rev-parse --short origin/main:docs/prompts/handoffs/batch2_external_arms_run_commission_handoff_v0.md  # expect da693bed
  git rev-parse --short origin/main:docs/decisions/judgment_spine_backtest_batch2_band_ratification_v0.md      # expect 746d23cd
  git rev-parse --short origin/main:orca-harness/runners/score_external_run.py                                 # expect 63f3db1c
  git show origin/main:orca-harness/scoring/band_scorer.py   | sha256sum   # expect d54dcd2c…
  git show origin/main:orca-harness/scoring/mapping_table.py | sha256sum   # expect 8bfd4830…
  ```
  Result: passed at authoring time (2026-06-16, origin/main c5d03455).
- Score one run (after pasting a model reply to `reply.txt`):
  ```bash
  python orca-harness/runners/score_external_run.py --model gpt55 --case nueco --reply reply.txt --dry-run
  python orca-harness/runners/score_external_run.py --model gpt55 --case nueco --reply reply.txt
  ```
  Result: helper dry-run validated at authoring time; real scoring uses the proven `run_case.run_fixed_case`.

## Blockers And Risks

- Risk: a runtime lacks an isolated mode for the named model → record a documented block for that (arm, case); do not fake. Evidence: the Claude lane could not run GPT/Grok contestants at all, which is why this is owner-run. Likely next action: run that arm where the model is available isolated.
- Risk: regenerated exam leaks the band/outcome → keep exams to packet + must-address + ladder + schema only; nueco stays neutralized. Likely next action: re-verify the exam contains no band/spoiler before pasting.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts to re-verify before acting: (1) commission handoff blob `da693bed`; (2) band ratification blob `746d23cd`; (3) signed ledger blob `482d8169`; (4) `score_external_run.py` blob `63f3db1c` + `run_case.py` `4f1c55c9`; (5) pinned key SHA-256 `d54dcd2c`/`8bfd4830`; (6) the 9 case dirs present with `participant_packet.md` + `facilitator_ledger.yaml` on origin/main.
- Load outcomes: `REUSE` (all verified — proceed to the runs); `STALE_REREAD_REQUIRED` (main moved / a blob changed — re-read); `BLOCKED_DRIFT` (key/band changed — stop); `BLOCKED_UNVERIFIABLE` (a load-bearing source missing — stop); `BLOCKED_MISSING_PACKET` (this file unreadable).
- Sources to reread if drift: the commission handoff + the band ratification + the affected case dir.

## Do Not Forget

- Contestant is the external model, isolated; the operator holds the bands; the contestant never sees them.
- Run all 9 per arm and report EVERY result; holdouts once + report-only; dev cases once.
- nueco stays neutralized (`b2_holdout_h7_v0`); never leak its dir name or capture manifest/receipt.
- The helper is ingest-only — never fabricate a contestant answer; if isolation is impossible, documented-block.
- Results are product-learning signal — not validation/readiness/buyer-proof; the full-panel verdict still needs all arms (Gemini still deferred).
