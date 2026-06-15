# Near-Half (#66) Handoff — Consume the Capture Corpus into Backtest Specimens v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt (docs/prompts/handoffs/)
scope: >
  Cold cross-lane handoff transferring the just-completed capture-spine corpus (75 pre-cutoff
  Wayback Source Capture units across 9 product-learning cases, all merged to main) to the
  judgment-spine near-half lane (PR #66, branch near-half-reconciliation-handoff-v0) so that
  lane can CONSUME those captures into Unity-shape backtest specimens (memo-at-cutoff +
  outcome-calibration). It carries inputs, the hard capture/judgment spine boundary, and the
  specimen shape only; it does not author the judgment-side specimen and does not grant
  judgment-spine execution authority.
use_when:
  - The judgment-spine near-half lane (#66) starts consuming the capture corpus.
  - A fresh agent/thread must continue near-half backtest assembly from a cold start.
authority_boundary: retrieval_only
authored_by: capture-spine Chief-Architect coordination lane (Opus 4.8), 2026-06-15
```

## Load Contract

- packet_version: handoff_v0
- mode: max
- created_at: 2026-06-15
- created_by_lane: capture-spine Chief-Architect coordination thread (provenance only; NOT an authority claim)
- workspace: C:\Users\vmon7\Desktop\projects\orca
- handoff_path: docs/prompts/handoffs/nearhalf_66_consume_capture_corpus_handoff_v0.md
- expected_branch: authored on worktree branch `nearhalf-66-handoff` (off `origin/main`). The RECEIVER's lane is PR #66, branch `near-half-reconciliation-handoff-v0` — a different, judgment-spine lane.
- expected_head: `origin/main` @ `ae4483dc` at authoring time. Re-fetch; `main` moves fast (owner merges aggressively).
- expected_dirty_state_including_handoff_file: this handoff file is newly created and untracked on the `nearhalf-66-handoff` worktree until committed; it adds one untracked file there.
- load_rule: confirm-don't-trust. Re-verify every load-bearing fact against its compare target before acting. Sender claims are hypotheses, not authority. This whole packet is a weak source class (a prior-thread artifact); rebind fresh source for any strict or actionable claim.

## Prompt-Orchestration Compliance (orca_start_preflight + authoring route)

```yaml
orca_start_preflight:
  agents_md_and_overlay_readme_read: yes   # AGENTS.md + .agents/workflow-overlay/README.md + prompt-orchestration.md read in task context 2026-06-15
  source_pack: bounded_custom              # the 6 ledger docs + 9 case dirs (see Authority And Source Ledger)
  repo_map_decision: not_needed
  repo_map_reason: cold handoff cites exact verified blob OIDs; no repo-map traversal needed to act
  workspace: C:\Users\vmon7\Desktop\projects\orca
  expected_branch: authored on worktree `nearhalf-66-handoff` off origin/main @ ae4483dc; receiver lane = PR #66 / near-half-reconciliation-handoff-v0
  dirty_state_allowance: this handoff file is newly created + untracked on the worktree (in scope); rest of worktree clean off main
  controlling_source_state: overlay / source-loading / validation / artifact-role files read clean from this worktree off origin/main @ ae4483dc; not separately checked for later modification
  doctrine_change: none                    # commissions a lane to consume existing inputs; defines no new doctrine, so no direction_change_propagation receipt is required
  target_files: this artifact (docs/prompts/handoffs/nearhalf_66_consume_capture_corpus_handoff_v0.md); receiver targets = the 9 case dirs + Unity specimen trio + near_half architecture doc (Authority And Source Ledger)
  source_hierarchy: AGENTS.md > .agents/workflow-overlay/ > accepted docs (near_half_backtest_learning_architecture_v0.md owns #66 consumption)
  edit_permission_this_authoring: docs-write
  output_mode: file-write (this artifact) + paste-ready-chat (courier prompt)
  validation_gates: header_index.py --strict (retrieval header present); check_map_links.py --strict; plus an INV-1 preservation check on any consumed capture packet
  external_source_boundary: jb is NOT Orca authority; external workflow source is read-only from Orca work
authoring_route:
  authored_via: workflow-handoff (state-packet mechanics) + workflow-prompt-orchestrator (prompt-orchestration contract applied)
  contract_applied: .agents/workflow-overlay/prompt-orchestration.md applied in full this turn (Implementation handoff family, preflight, output-mode, validation gates, leakage check)
  not_a_claim: not validation, not readiness, not implementation authorization, not source promotion
receiver_authority:
  edit_permission: docs-write WITHIN the judgment-spine near-half lane (#66) — author memo_at_cutoff + outcome_calibration specimen docs; NEVER edit capture packets (INV-1)
  output_mode: file-write under judgment-spine lane authority; land via per-lane PR (human-gated merge)
  not_authorized_by_this_handoff: judgment-spine execution authority — the receiver operates under its own lane authority; capture coordination only transfers inputs/boundary/shape
  model_lane: unbound  # judgment/review lanes choose their own runtime model; no routing claimed here
```

## Goal Handoff

Sender-derived from bound context (no `workflow-goal-framing` artifact existed; orientation only, not authority):

- long_term_goal: Orca learns whether its as-of-cutoff product-demand judgments would have been right, by backtesting them against sealed later outcomes — turning judgment quality into a measured, improvable signal.
- anchor_goal: Stand up the judgment-spine near-half backtest so it CONSUMES the 75-unit capture corpus — produce the memo-at-cutoff + outcome-calibration specimen halves for one or more of the 9 cases, in the Unity 3-doc shape, without the capture side ever emitting a verdict.
- success_signal: At least one case has a complete Unity 3-doc specimen — `source_packet` (already built, INV-1, unchanged) + `memo_at_cutoff` + `outcome_calibration` — where the memo is written ONLY from pre-cutoff captured facts and the calibration scores it against the known later outcome, with the spine boundary demonstrably preserved (no scores/weights/ranks/verdicts written into the capture packet).

## Open Decision / Fork

- decision: HOW the near-half lane consumes the captures into specimens.
  - options:
    - (a) Hand-assemble specimens per the Unity 3-doc pattern (doc-only), matching the current "no backtest code harness exists" reality.
    - (b) Build a minimal harness/scaffold that generates memo/calibration skeletons from the capture packets.
    - (c) plus: which case(s) first — the 9 vary in unit count and outcome clarity.
  - already constrained / off the table: re-deriving the frozen fixtures (Beauty Pie 2023, Topicals 2021); emitting verdicts/scores from the capture side; broad/opportunistic crawling; editing the merged capture packets.
  - trade-offs: (a) is smallest-complete and matches how the only existing Unity specimen was built (doc-assembled), but is manual per case. (b) scales but is speculative infrastructure before the consumption path is proven once — exactly the kind of build the project's "smallest complete intervention" rule warns against until justified.
  - owner of the call: judgment-spine lane owner (Eric).
  - recommendation and why: start with (a), one case with the clearest sealed outcome (a decisive pivot/kill — e.g. `joahbeauty_cvs_kill_2024_v0` or `kinderbeauty_box_pivot_2023_v0`), to validate the consumption path end-to-end before considering any harness. Rationale: no harness exists, the reference Unity specimen is doc-assembled, and proving one case first de-risks (b).

## Drift Guard

- INV-1 (capture invariant): the capture packets record observed facts + limits ONLY. Do NOT edit a capture packet to add scores, weights, ranks, or verdicts.
  - why it matters: it is the load-bearing separation that keeps captured evidence neutral.
  - what violating it breaks: the backtest becomes circular — captured "evidence" pre-contaminated with judgment is not a fair input.
- Spine boundary: the capture-spine coordination lane that produced this handoff does NOT authorize judgment-spine execution. The receiver operates under judgment-spine authority; this packet transfers inputs + boundary + shape only.
  - what violating it breaks: lane-authority confusion; work attributed to the wrong spine/owner.
- Memo discipline (backtest validity): `memo_at_cutoff` must use ONLY pre-cutoff captured facts — no hindsight from the known later outcome may leak into it.
  - what violating it breaks: the backtest measures hindsight, not foresight; the result is worthless.
- Frozen fixtures: Beauty Pie 2023 (`beautypie_repricing_2023_v0`) and Topicals 2021 (`topicals_retail_expansion_2021_v0`) are sealed — do not re-derive or add captures.
- Commissioned-bounded: consume the EXISTING corpus; do not opportunistically expand capture in this lane.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: read `.agents/workflow-overlay/README.md` first, then follow the Orca overlay; `AGENTS.md` is triggers + global behavior. (Overlay-bound, NOT zero-config.)
- targets to enter the ladder: `docs/product/judgment_spine/near_half_backtest_learning_architecture_v0.md` (the #66 lane authority); `docs/workflows/data_capture_spine_consolidation_map_v0.md` (spine navigation); the Unity specimen trio (see ledger); the 9 case dirs under `orca-harness/cases/product_learning/`.
- already loaded (weak orientation, freshness-marked; not authority): only this packet (a prior-thread artifact, dated 2026-06-15).
- must load first (before strict or actionable steps): `near_half_backtest_learning_architecture_v0.md` — confirm the current near-half consumption contract before assembling any specimen.
- load rule: re-run progressive source loading per the overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- Capture-spine vs judgment-spine boundary — gist: capture-spine emits INV-1 inputs; judgment-spine owns scoring/learning.
  - decided in: `docs/workflows/data_capture_spine_consolidation_map_v0.md` and `docs/product/judgment_spine/near_half_backtest_learning_architecture_v0.md`
  - compare target: see ledger blob OIDs.
  - verify before: any specimen assembly.
- Backtest = Half 1 (pre-cutoff evidence capture, DONE) + Half 2 (as-of-cutoff scoring/learning, THIS lane) — gist: the captures are Half 1; #66 is Half 2.
  - decided in: `near_half_backtest_learning_architecture_v0.md`. verify before: actionable use.
- Unity 3-doc specimen shape — gist: a backtest specimen is three docs: source_packet / memo_at_cutoff / outcome_calibration.
  - decided in: the Unity specimen trio (ledger). verify before: choosing doc-vs-harness.
- INV-1 invariant — gist: capture records observed facts + limits, never weights/scores/verdicts. (Drift Guard above.)
- Source Capture packet shape — gist: each unit = `manifest.json` + `raw/01_archive_availability_metadata.json` + `raw/02_archive_snapshot_body.bin` + `raw/03_archive_snapshot_body_metadata.json` + `receipt.md`; the committed blob sha256 of file_02 (body) equals `manifest.preserved_files[].sha256` (byte-faithful).
  - verify before: trusting any unit; re-derive a body sha and compare to its manifest entry.

## Active Objective

Stand up the judgment-spine near-half backtest (PR #66) to consume the just-completed 75-unit capture corpus into Unity-shape backtest specimens, preserving the capture/judgment spine boundary (INV-1 on the capture packets; memo + calibration as separate judgment-side docs).

## Exact Next Authorized Action

1. Load #66 lane authority: read `docs/product/judgment_spine/near_half_backtest_learning_architecture_v0.md` and `docs/workflows/data_capture_spine_consolidation_map_v0.md`; confirm the current near-half consumption contract for capture packets (doc-assembled specimens vs. harness).
2. Read the Unity specimen trio (ledger) to internalize the target 3-doc shape.
3. Pick one case with a clear sealed outcome (recommended: `joabeauty_cvs_kill_2024_v0` or `kinderbeauty_box_pivot_2023_v0`); read its `source_provenance_notes_v0.md` and 2-3 `source_captures/<unit>/manifest.json` to confirm pre-cutoff facts are present.
4. Assemble that case's Unity 3-doc specimen: reuse the existing capture packet AS the `source_packet` (INV-1, unchanged); author `memo_at_cutoff` (pre-cutoff facts only, no hindsight) + `outcome_calibration` (score the memo against the known later outcome) as judgment-side docs under judgment-spine authority.
5. Validation / stop condition: confirm no scores/weights/ranks/verdicts were written into any capture packet (INV-1 preserved) and that the memo cites only pre-cutoff facts. If either fails, stop and fix before proceeding to a second case.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` + `.agents/workflow-overlay/` (read overlay `README.md` first). Reread-required.
- Overlay or equivalent authority: judgment-spine lane authority owns #66 execution; per-lane PR flow in `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md` (squash-merge, human-gated landing to `main`).
- User constraints: confirm-don't-trust; owner merges fast; mechanical delegation → Sonnet `worker` / Haiku `mechanical` (Opus only for judgment), per `docs/decisions/subagent_model_tiering_doctrine_v0.md`.
- Source-read ledger:
  - `docs/product/judgment_spine/near_half_backtest_learning_architecture_v0.md`
    - Role: THE near-half (#66) lane architecture/authority — defines how Half-2 scoring/learning consumes captures.
    - Load-bearing: yes
    - Compare target: blob `138f8374c66633e936b07b3e080244984df5dfa4` on `origin/main` @ `ae4483dc`
    - Last checked: 2026-06-15
    - Reuse rule: re-read fresh before any specimen assembly; rebind if blob changed.
  - `docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md`
    - Role: near-half signal-reliability ledger (related judgment-spine artifact; orientation).
    - Load-bearing: no
    - Compare target: blob `28215ba3d0a593fd2a6029d18f5b19760077e44c` on `origin/main` @ `ae4483dc`
    - Last checked: 2026-06-15
    - Reuse rule: orientation only.
  - `docs/product/core_spine/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md`
    - Role: Unity specimen — the source_packet (capture-side) reference shape.
    - Load-bearing: yes
    - Compare target: blob `c4d814e53dc2abc2676a0cf58d80e753940c868a` on `origin/main` @ `ae4483dc`
    - Last checked: 2026-06-15
    - Reuse rule: shape reference; re-read before assembling.
  - `docs/product/core_spine/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md`
    - Role: Unity specimen — the memo-at-cutoff (judgment-side) reference shape.
    - Load-bearing: yes
    - Compare target: blob `55e0e1245babfa45cc1f93ee6bc3094dd0df5131` on `origin/main` @ `ae4483dc`
    - Last checked: 2026-06-15
    - Reuse rule: shape reference; the as-of-cutoff discipline here is the model to copy.
  - `docs/product/core_spine/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md`
    - Role: Unity specimen — the outcome-calibration (judgment-side) reference shape.
    - Load-bearing: yes
    - Compare target: blob `fbfc8285ad12431903de0455f68854c452952321` on `origin/main` @ `ae4483dc`
    - Last checked: 2026-06-15
    - Reuse rule: shape reference; re-read before assembling.
  - `docs/workflows/data_capture_spine_consolidation_map_v0.md`
    - Role: capture-spine navigation map (where the corpus + adapters live; archive.org in-bounds).
    - Load-bearing: yes
    - Compare target: blob `b4296f967615ec4062ec2266867c2408d4162780` on `origin/main` @ `ae4483dc`
    - Last checked: 2026-06-15
    - Reuse rule: navigation, not authority.
  - `orca-harness/cases/product_learning/<case>/` (9 cases; see Corpus Inventory below)
    - Role: the capture corpus — INV-1 inputs to backtest. Each case = `source_provenance_notes_v0.md` + `source_captures/<unit>/{manifest.json, raw/01-03, receipt.md}`.
    - Load-bearing: yes
    - Compare target: present on `origin/main` @ `ae4483dc`; verify with `git ls-tree -r origin/main --name-only orca-harness/cases/product_learning/<case>`. Byte-faithfulness: re-derive a body sha and compare to its manifest entry.
    - Last checked: 2026-06-15
    - Reuse rule: read per case before consuming; never edit (INV-1).
- Source gaps: the precise near-half consumption contract (doc-assembled vs. harness) is not restated here — read the architecture doc. Whether `near_half_backtest_learning_architecture_v0.md` has been revised since `ae4483dc` is unknown to the receiver; re-fetch.
- Strict-only blockers: landing to `main` is human-gated; the protected-action guard blocks an agent's `gh pr merge` (self-merge only via the verified own-PR exception); background agents cannot `gh pr create` (a main thread opens PRs).
- Not-proven boundaries: the capture corpus is pre-cutoff evidence ONLY — NOT validation, NOT a backtest result, NOT readiness. Nothing in this handoff asserts a backtest verdict.

### Corpus Inventory (verified on `origin/main` @ `ae4483dc`, 2026-06-15)

75 units across 9 cases (count = `manifest.json` files per case dir):

- `kinderbeauty_box_pivot_2023_v0` — 11 units
- `cocokind_holdprice_2025_v0` — 10 units
- `joahbeauty_cvs_kill_2024_v0` — 11 units
- `privatepacks_retail_retreat_v0` — 9 units
- `sundaily_gummy_pivot_v0` — 6 units (domain sundots.com)
- `saie_price_increase_2025_v0` — 10 units
- `selflessbyhyram_target_entry_2023_v0` — 6 units
- `nueco_fragrance_pivot_v0` — 7 units
- `imaginaryauthors_sku_kills_2024_v0` — 5 units

NOT part of this corpus (present on main but out of scope): `beautypie_repricing_2023_v0` + `topicals_retail_expansion_2021_v0` (FROZEN fixtures); `feedhaven_repricing_2019_anon_v0` + `inoreader_repricing_2019_v0` (YAML-evidence model, not archive-capture); `jsg01_binding_assembly_proof_v0` (binding proof).

## Current Task State

- Completed: the capture corpus (75 units / 9 cases) is built, byte-faithful (committed blob sha == manifest sha), pre-cutoff, INV-1 clean, and MERGED to `origin/main` (the last three landed as #139 Joah, #140 Private Packs, #141 Sundaily — all verified MERGED 2026-06-15).
- Partially completed: nothing on #66 itself — this lane is being handed off at its start.
- Broken or uncertain: whether #66 expects doc-assembled specimens or a code harness (open decision above); resolve by reading the architecture doc.

## Workspace State

- Branch: this packet authored on worktree `nearhalf-66-handoff` (off `origin/main`). Receiver's working lane: PR #66 / `near-half-reconciliation-handoff-v0`.
- Head: `origin/main` @ `ae4483dc` (re-fetch).
- Dirty or untracked state before handoff: the `nearhalf-66-handoff` worktree was clean off `main`; the home branch `ecr-sp3-timing-deriver-slice1` carries many pre-existing untracked files (out of scope for this lane).
- Dirty or untracked state after writing the handoff file: + this handoff file (untracked on the `nearhalf-66-handoff` worktree until committed).
- Target files or artifacts: the 9 case dirs under `orca-harness/cases/product_learning/`; the Unity specimen trio; the near-half architecture doc.
- Related worktrees or branches: many capture lane worktrees under `.claude/worktrees/` are now landed (hygiene-cleanup candidates).

## Changed / Inspected / Tested Files

- `docs/prompts/handoffs/nearhalf_66_consume_capture_corpus_handoff_v0.md`
  - Status: newly created (this handoff), untracked on the `nearhalf-66-handoff` worktree until committed.
  - Role: the cold handoff packet itself.
  - Important observations: carries a retrieval header to satisfy `header_index --strict`; cites blob-OID compare targets verified at `ae4483dc`.
- Source files inspected (read-only) to build this packet: the 6 ledger docs + the 9 case dirs (presence + unit counts).
  - Status: unchanged.
  - Role: load-bearing inputs / shape references.

## Frozen Decisions

- Beauty Pie 2023 + Topicals 2021 are FROZEN fixtures.
  - Evidence: prior session adjudication; both case dirs exist on main as sealed fixtures.
  - Consequence: do not re-derive or add captures into them.
- INV-1: capture packets are observed facts + limits only.
  - Evidence: capture-spine invariant; consolidation map.
  - Consequence: scoring/learning lives only in judgment-side docs.
- Unity 3-doc specimen shape is the target form.
  - Evidence: the Unity specimen trio on main.
  - Consequence: specimens = source_packet + memo_at_cutoff + outcome_calibration.

## Mutable Questions

- Doc-assembled specimens vs. a code harness?
  - Why still mutable: the architecture doc (not fully re-read by the receiver yet) owns the answer.
  - What would resolve it: reading `near_half_backtest_learning_architecture_v0.md`.
- Which case first?
  - Why mutable: outcome clarity varies; owner may have a preference.
  - What would resolve it: owner call, or pick the clearest sealed outcome.
- Has the near-half contract changed since `ae4483dc`?
  - Why mutable: `main` moves fast.
  - What would resolve it: re-fetch + re-read the architecture doc blob.

## Superseded / Dangerous-To-Reuse Context

- `_scratch/precompact_capture_spine_coordination_v0.md` (a same-thread precompact checkpoint) — do NOT rely on it as a cold reader.
  - Why dangerous: it is a warm same-thread checkpoint for the capture-spine coordination thread, not a cold handoff; some of its "next actions" (merge #139/#140/#141) are already DONE.
  - Current replacement: this handoff packet.
- The owner's earlier "all merged" / "should all be merged" beliefs — drifted twice during the capture batch while PRs were still open.
  - Why dangerous: do not assume merge state from sender say-so.
  - Current replacement: VERIFIED 2026-06-15 — #139/#140/#141 are MERGED and the full corpus is on `origin/main` @ `ae4483dc`. Still: re-verify, do not trust.

## Commands And Verification Evidence

- Command:
  ```bash
  git fetch origin main
  git rev-parse --short origin/main                       # ae4483dc
  for n in 139 140 141; do gh pr view $n --json state --jq .state; done   # all MERGED
  ```
  Result:
  - Passed: `main` @ `ae4483dc`; #139/#140/#141 MERGED.
  - Re-run target: the receiver should re-run to confirm `main` hasn't moved past the corpus.
- Command:
  ```bash
  for c in kinderbeauty_box_pivot_2023_v0 cocokind_holdprice_2025_v0 joahbeauty_cvs_kill_2024_v0 \
           privatepacks_retail_retreat_v0 sundaily_gummy_pivot_v0 saie_price_increase_2025_v0 \
           selflessbyhyram_target_entry_2023_v0 nueco_fragrance_pivot_v0 imaginaryauthors_sku_kills_2024_v0; do
    git ls-tree -r origin/main --name-only "orca-harness/cases/product_learning/$c" | grep -c '/manifest.json$'
  done                                                    # 11,10,11,9,6,10,6,7,5 = 75
  ```
  Result:
  - Passed: 75 units / 9 cases.
  - Re-run target: the receiver confirms the inventory before consuming.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - The capture corpus (75 units / 9 cases) is present on `main` and unchanged — compare target: `git ls-tree` per case @ current `origin/main`; byte-faithfulness via body-sha vs manifest.
  - `near_half_backtest_learning_architecture_v0.md` is present and current — compare target: blob `138f8374...` (rebind if changed).
  - The Unity specimen trio is present — compare targets: blobs `c4d814e5...`, `55e0e124...`, `fbfc8285...`.
- Load outcomes and what each means: `REUSE` (all verified — continue from Exact Next Authorized Action); `STALE_REREAD_REQUIRED` (main moved / a blob changed — re-read before acting); `BLOCKED_DRIFT` (corpus or architecture doc conflicts with this packet); `BLOCKED_UNVERIFIABLE` (a load-bearing source is missing and cannot be re-derived — stop, do not proceed on say-so); `BLOCKED_MISSING_PACKET` (this file unreadable).
- Sources that must be reread if drift is detected: the near-half architecture doc + the consolidation map + the affected case dir.

## Do Not Forget

- The capture packets are INPUTS, not results — reuse them AS the `source_packet`, never edit them (INV-1).
- `memo_at_cutoff` must cite ONLY pre-cutoff facts — no hindsight leakage from the known outcome; this is the backtest's validity guard.
- Capture-spine coordination (this packet's sender) does NOT authorize judgment-spine execution — the receiver works under judgment-spine authority.
