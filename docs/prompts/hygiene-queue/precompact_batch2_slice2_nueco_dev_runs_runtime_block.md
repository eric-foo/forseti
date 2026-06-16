# Pre-Compact Checkpoint

## Current objective

Continue only the Batch 2 Slice 2 lane from `docs/prompts/handoffs/batch2_slice2_nueco_gap_close_and_dev_runs_handoff_v0.md`: close the nueco anti-cherry-pick gap, then run the dev arm (`cocokind`, `saie`) using the ledger-pinned Claude Sonnet-class arm.

## Current state

- What has been completed:
  - Orca project instructions and overlay entrypoint were read.
  - The handoff packet was loaded from refreshed `origin/main`; PR #174 is on `origin/main`.
  - A clean isolated Codex worktree/branch was created: `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\batch2-slice2-nueco-dev-runs`, branch `codex/batch2-slice2-nueco-dev-runs`, HEAD `f5002a7b`.
  - Confirm-don't-trust checklist returned `REUSE`.
  - Authority blob targets verified against HEAD:
    - ledger `482d8169`
    - conductor addendum v1 `ede29148`
    - gate-ownership map `0135ad5a`
    - commission handoff `075183c0`
    - `orca-harness/runners/run_case.py` `4f1c55c9`
  - Pinned scoring key verified against Git blob bytes:
    - `orca-harness/scoring/band_scorer.py` SHA-256 `D54DCD2CB34A8158232E1A428F70A1F3F182052529D7BC8E5293D5F21A67E1E3`
    - `orca-harness/scoring/mapping_table.py` SHA-256 `8BFD4830A2E3C8FEFEE631B4CE69AF6241BDBDDE585AFAAB09A7791A356AC9E9`
  - Case footprints verified:
    - `nueco_fragrance_pivot_v0`: 7 capture dirs, 21 preserved files, byte-faithful, no packet/run/findings/report artifacts.
    - `cocokind_holdprice_2025_v0`: existing packet/evidence/facilitator ledger/packet receipt, 10 capture dirs, 30 preserved files, byte-faithful, no run/findings/report.
    - `saie_price_increase_2025_v0`: existing packet/evidence/facilitator ledger/packet receipt, 10 capture dirs, 30 preserved files, byte-faithful, no run/findings/report.
    - `joahbeauty_cvs_kill_2024_v0`: full slice-1 exemplar shape present, including run and report.
  - Runtime blocker verified:
    - `Get-Command claude` returned no command.
    - `Get-Command anthropic` returned no command.
    - Codex multi-agent tool exposes GPT-family model overrides only, not Claude/Sonnet.
- What is partially completed:
  - Codex performed reusable verification prep only.
  - No slice-2 packet, run, findings, report, score, commit, push, or PR was produced by Codex.
  - The Codex worktree exists and is clean; it is not a valid executor for the Claude Sonnet-class contestant arm.
- What is currently broken or uncertain:
  - Structural blocker: this Codex/GPT runtime cannot produce a Claude Sonnet-class contestant judgment.
  - Next execution must happen in a Claude Code / Claude Sonnet-capable runtime, or Codex may only do downstream file work from externally recorded Sonnet judgments.

## Important files and symbols

- `AGENTS.md`
  - Relevant functions/classes/components: Orca project instructions.
  - Current role in the task: Global behavior, isolation, smallest complete intervention, verification before durable claims.
  - Important changes or observations: Requires overlay README before project work; implementation/runtime work requires explicit bounded authorization or accepted handoff.
- `.agents/workflow-overlay/README.md`
  - Relevant functions/classes/components: Overlay entrypoint.
  - Current role in the task: Project authority routing.
  - Important changes or observations: Overlay wins over generic or external workflow source for Orca facts.
- `.agents/workflow-overlay/decision-routing.md`
  - Relevant functions/classes/components: Cynefin routing layer.
  - Current role in the task: Used because this is cross-thread, messy-worktree, execution-affecting work.
  - Important changes or observations: Allowed next move was source verification and isolated worktree; disallowed move was building/running in dirty current checkout or substituting runtime.
- `docs/prompts/handoffs/batch2_slice2_nueco_gap_close_and_dev_runs_handoff_v0.md`
  - Relevant functions/classes/components: Goal Handoff, Active Objective, Drift Guard, Confirm-Don't-Trust Load Checklist.
  - Current role in the task: Current lane packet.
  - Important changes or observations: Present on `origin/main` as blob `0d0a057e`; active objective is nueco full pipeline first, then dev runs.
- `docs/decisions/judgment_spine_backtest_batch2_ledger_declaration_v0.md`
  - Relevant functions/classes/components: Batch 2 set/split/key/panel/discipline.
  - Current role in the task: Governing authority.
  - Important changes or observations: Blob `482d8169`; confirms 7 holdouts including `nueco`, 2 dev cases (`cocokind`, `saie`), Claude Sonnet-class arm, frozen key, product-learning cap, no live API, no scoring-key change.
- `docs/product/judgment_spine/conductor_construction_integrity_probe_addendum_v1.md`
  - Relevant functions/classes/components: R2 outcome-blind construction, R4 reasoning trace, tell-audit.
  - Current role in the task: Packet construction integrity authority.
  - Important changes or observations: Blob `ede29148`; nueco packet must be built by an outcome-blind subagent with outcome material withheld and receipt evidence.
- `docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md`
  - Relevant functions/classes/components: JSG-01..JSG-10 ownership, JSG-02 packet freeze, JSG-04 isolation, JSG-06 blind judgment, JSG-07 scoring, JSG-08 reveal/calibration.
  - Current role in the task: Gate ownership and non-claims boundary.
  - Important changes or observations: Blob `0135ad5a`.
- `docs/prompts/handoffs/batch2_outcome_blind_packet_construction_commission_handoff_v0.md`
  - Relevant functions/classes/components: Construction-run-score discipline and layer map.
  - Current role in the task: Execution discipline source.
  - Important changes or observations: Blob `075183c0`; says construction delegated to outcome-blind subagent, runs blind/isolated, score via `run_case.py`, report all results.
- `orca-harness/runners/run_case.py`
  - Relevant functions/classes/components: Deterministic scoring runner.
  - Current role in the task: Only permitted scoring path.
  - Important changes or observations: Blob `4f1c55c9`; do not edit for this lane.
- `orca-harness/scoring/band_scorer.py`
  - Relevant functions/classes/components: Frozen scoring key.
  - Current role in the task: Pinned key input.
  - Important changes or observations: Working-tree SHA can differ because of line endings; Git blob SHA-256 matches ledger pin `D54DCD2C...`.
- `orca-harness/scoring/mapping_table.py`
  - Relevant functions/classes/components: Frozen mapping table.
  - Current role in the task: Pinned key input.
  - Important changes or observations: Git blob SHA-256 matches ledger pin `8BFD4830...`.
- `orca-harness/cases/product_learning/nueco_fragrance_pivot_v0/`
  - Relevant functions/classes/components: `source_captures/`, `source_provenance_notes_v0.md`.
  - Current role in the task: Missing 7th holdout that must be run or documented-excluded.
  - Important changes or observations: Captures present and byte-faithful; no concrete feasibility blocker found; no execution artifacts present. Dir name leaks outcome, so neutralize ID for blind builder.
- `orca-harness/cases/product_learning/cocokind_holdprice_2025_v0/`
  - Relevant functions/classes/components: existing `participant_packet.md`, `evidence/`, `facilitator_ledger.yaml`, `packet_construction_receipt_v0.md`.
  - Current role in the task: Dev case with packet built but blind Sonnet run not done.
  - Important changes or observations: Receipt says outcome was withheld; no run/findings/report.
- `orca-harness/cases/product_learning/saie_price_increase_2025_v0/`
  - Relevant functions/classes/components: existing `participant_packet.md`, `evidence/`, `facilitator_ledger.yaml`, `packet_construction_receipt_v0.md`.
  - Current role in the task: Dev case with packet built but blind Sonnet run not done.
  - Important changes or observations: Receipt says outcome was withheld; no run/findings/report.
- `orca-harness/cases/product_learning/joahbeauty_cvs_kill_2024_v0/`
  - Relevant functions/classes/components: slice-1 packet, run, findings, report.
  - Current role in the task: Artifact-shape exemplar to mirror.
  - Important changes or observations: Full footprint present.

## Decisions made

- Decision: Do not execute Claude arm from Codex/GPT runtime.
  - Reason: Ledger pins Claude arm to Sonnet-class; Codex subagents are GPT-family only and no Claude CLI/runtime is available.
  - Consequence: No off-panel run artifacts were written. Continuing execution must use a Claude Sonnet-capable environment.
- Decision: Treat Codex's `REUSE` verification as reusable prep, not execution completion.
  - Reason: Source verification is runtime-agnostic; contestant judgment is model-panel-specific.
  - Consequence: A fresh Claude lane may reuse the observed facts but must still honor confirm-don't-trust before strict/actionable claims.
- Decision: Recommended continuation route is `A`: run construction and judgments in Claude Code / Claude Sonnet environment.
  - Reason: It mirrors slice 1, keeps construction and blind runs in one Sonnet-capable runtime, and avoids panel-integrity drift.
  - Consequence: Codex should not be the lane executor; it may support scoring/file-work only after real Sonnet judgments exist.
- Decision: Do not change key, case set, runtime panel, or route raw captures to L3/L4.
  - Reason: Drift Guard and signed ledger.
  - Consequence: Any need for these changes is owner-gated and stops the lane.

## Superseded / Ignore

- Prior instruction, idea, artifact, or finding: Slice-1 framing that "6 holdout" coverage completed the holdout arm.
  - Why superseded: Signed Batch 2 ledger has 7 holdouts and includes `nueco`.
  - Current replacement: Run/report `nueco` or document-exclude with real owner-signed reason; silent drop voids anti-cherry-pick.
- Prior instruction, idea, artifact, or finding: Using Codex/GPT subagent as the Claude Sonnet contestant.
  - Why superseded: Wrong runtime would corrupt the panel.
  - Current replacement: Use Claude Sonnet-class runtime only for the Claude arm.
- Prior instruction, idea, artifact, or finding: Treating absence of `claude` CLI as a bug in the repo.
  - Why superseded: It is structural/runtime capability mismatch, not repository failure.
  - Current replacement: Route execution to a Sonnet-capable environment.
- Prior instruction, idea, artifact, or finding: Building nueco packet manually in outcome-aware Codex context.
  - Why superseded: Conductor R2 requires outcome-blind construction evidence.
  - Current replacement: Outcome-blind builder receives neutralized case ID plus stripped pre-cutoff evidence only.

## Commands and results

- Command:
  ```bash
  git fetch origin
  ```
  Result:
  - Passed/failed/not run: first failed in sandbox with `.git/FETCH_HEAD` permission denied; rerun with approved escalation passed.
  - Important output: refreshed `origin/main` to `f5002a7be0ab81aa301979c9fd66ffc4e64ba637`, which includes #174.
- Command:
  ```bash
  git rev-parse origin/main
  git log --oneline -5 origin/main
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: `origin/main` = `f5002a7be0ab81aa301979c9fd66ffc4e64ba637`; recent log includes `b7998d27 docs(judgment-spine): slice-2 handoff ... (#174)`, `431b6dcc ... (#172)`.
- Command:
  ```bash
  git worktree add -b codex/batch2-slice2-nueco-dev-runs .codex\worktrees\batch2-slice2-nueco-dev-runs origin/main
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: branch set up tracking `origin/main`; worktree HEAD `f5002a7b`.
- Command:
  ```bash
  git ls-tree HEAD docs/decisions/judgment_spine_backtest_batch2_ledger_declaration_v0.md docs/product/judgment_spine/conductor_construction_integrity_probe_addendum_v1.md docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md docs/prompts/handoffs/batch2_outcome_blind_packet_construction_commission_handoff_v0.md orca-harness/runners/run_case.py
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: blob IDs matched packet compare targets: `482d8169`, `ede29148`, `0135ad5a`, `075183c0`, `4f1c55c9`.
- Command:
  ```bash
  python -c "import subprocess,hashlib; paths=['orca-harness/scoring/band_scorer.py','orca-harness/scoring/mapping_table.py']; [print(p, hashlib.sha256(subprocess.check_output(['git','show','HEAD:'+p])).hexdigest().upper()) for p in paths]"
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: Git blob bytes matched ledger pins `D54DCD2C...` and `8BFD4830...`.
- Command:
  ```bash
  python -c "import json,hashlib,pathlib; cases=['nueco_fragrance_pivot_v0','cocokind_holdprice_2025_v0','saie_price_increase_2025_v0']; ..."
  ```
  Result:
  - Passed/failed/not run: first timed out after printing success; rerun with 60000 ms passed.
  - Important output:
    - `nueco_fragrance_pivot_v0 capture_dirs 7 preserved_files 21 byte_faithful True`
    - `cocokind_holdprice_2025_v0 capture_dirs 10 preserved_files 30 byte_faithful True`
    - `saie_price_increase_2025_v0 capture_dirs 10 preserved_files 30 byte_faithful True`
- Command:
  ```bash
  Get-Command claude -ErrorAction SilentlyContinue
  Get-Command anthropic -ErrorAction SilentlyContinue
  Get-Command codex -ErrorAction SilentlyContinue
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: `claude` absent, `anthropic` absent, `codex.ps1` present.
- Command:
  ```bash
  git status --short --branch
  ```
  Result:
  - Passed/failed/not run: passed in isolated worktree.
  - Important output: `## codex/batch2-slice2-nueco-dev-runs...origin/main`, no dirty entries.

## Known issues and risks

- Issue: Claude Sonnet runtime unavailable in Codex lane.
  - Evidence: no `claude`/`anthropic` command; Codex subagent model list lacks Sonnet.
  - Likely next action: Move execution to Claude Code / Claude Sonnet-capable environment.
- Issue: Runtime substitution would silently corrupt panel integrity.
  - Evidence: ledger panel explicitly says Claude Sonnet-class; user reaffirmed Codex/GPT must not produce Claude arm.
  - Likely next action: Refuse GPT/Codex contestant output for this arm.
- Issue: `nueco` case ID leaks the outcome.
  - Evidence: directory name `nueco_fragrance_pivot_v0`; handoff explicitly calls this out.
  - Likely next action: Blind builder receives neutralized ID plus stripped pre-cutoff evidence only.
- Issue: Working-tree SHA-256 for scoring files can look mismatched due CRLF bytes.
  - Evidence: `Get-FileHash` on working files produced different hashes, but `git show HEAD:<path>` blob bytes matched ledger pins.
  - Likely next action: Verify scoring pin against Git blob bytes, not CRLF-expanded working tree bytes.
- Issue: Main workspace is dirty with unrelated untracked files.
  - Evidence: `git status --short --branch` in root shows many unrelated untracked paths.
  - Likely next action: Do not use root for lane execution; use isolated worktree or Claude lane worktree.

## Constraints and user preferences

- Constraint/preference: Push back hard on wrong or low-quality input.
  - Source or reason: `AGENTS.md` user instruction.
- Constraint/preference: Confirm-don't-trust before strict/actionable claims.
  - Source or reason: Handoff load contract and Orca project instructions.
- Constraint/preference: Continue only the packet's Goal Handoff / Active Objective.
  - Source or reason: User instruction in this thread.
- Constraint/preference: No Opus contestant, no key change, no live API, no L3/L4 routing.
  - Source or reason: Handoff Drift Guard and user instruction.
- Constraint/preference: Claude arm must be Sonnet-class, not Codex/GPT.
  - Source or reason: Signed ledger and user reaffirmation after Codex hit runtime wall.
- Constraint/preference: Product-learning cap only; do not claim validation/readiness/buyer-proof.
  - Source or reason: Ledger and handoff.
- Constraint/preference: Land via per-lane PR; merge to main is human-gated.
  - Source or reason: `AGENTS.md` and handoff.
- Constraint/preference: Do not edit source captures.
  - Source or reason: INV-1 and handoff.

## Next steps

1. In a Claude Code / Claude Sonnet-capable environment, re-open the handoff and source checklist, then re-confirm the `REUSE` facts against current main before writes.
2. Build `nueco` outcome-blind packet via blind Claude subagent using neutralized ID and stripped pre-cutoff evidence; write `participant_packet.md`, `evidence/`, `facilitator_ledger.yaml`, and `packet_construction_receipt_v0.md` mirroring slice-1 shape.
3. Run blind Sonnet once for `nueco`, then run blind Sonnet once each for existing `cocokind` and `saie` packets; record `blind_judgement.yaml`, perform JSG-08 tell-audit, score via `run_case.py`, write findings and case reports, then validate status/diffs and prepare PR.

## Do not forget

- `REUSE` was verified, but Codex is not the executor for the Claude Sonnet arm.
- `nueco` is the anti-cherry-pick gap; close it first unless a concrete capture blocker appears.
- No GPT/Codex substitution for Claude Sonnet, no Opus, no key change, no live API, no L3/L4 routing.
- Results must be reported whatever they are; no selective reporting.
