# Handoff Packet — Capture Spine Continuation

```yaml
retrieval_header_version: 1
artifact_role: Cold handoff packet
scope: Capture-spine continuation state for a fresh lane resuming after the CloakBrowser (PR #50) + subagent-return-contract (PR #53) session.
use_when:
  - A fresh lane, agent, or thread resumes capture-spine work with none of the sender's context.
  - Reconciling the in-flight capture PRs or driving the Reddit screening-read service to merge.
authority_boundary: retrieval_only
```

> Durable cold-handoff packet. Orientation, **not** authority. Confirm every load-bearing
> claim against its cited compare target before acting. Source hierarchy: `AGENTS.md` >
> `.agents/workflow-overlay/` > `docs/`.

## STATUS UPDATE — 2026-06-13 (post-reconciliation; READ FIRST, supersedes stale body below)

Verified against `origin/main` this session. **The body below is partially STALE.**

- **origin/main = `e32f18a`** (was `72d32e7` at original write). PRs **#50 (CloakBrowser), #53 (subagent contract), #54 (judgment-spine ledger) are all MERGED.** Option C (reconcile the open PRs) is **DONE**.
- **Orphaned cloak worktrees/branches (geo `#22`, scroll `#23`) PRUNED**; no stale worktree records remain.
- **Reddit screening service (Option A) — rebuilt clean, validated, pushed, NOT yet merged:**
  - The original branch sat on a **stale 173-commit non-main base** (824 files). The naive "push branch + open PR" in the body below would have produced an 824-file PR — **DO NOT do that.**
  - Recovered by rebasing onto fresh `origin/main` keeping only the 2 feature commits → **3 files / 667 insertions**. Branch `capture-spine-reddit-screening-v0` pushed to origin @ **`e889da2`** (clean; 1 behind / 2 ahead of `e32f18a`; mergeable).
  - Validated in-home-env (closes the body's "never re-run"): **25/25 unit tests pass**; **live receipt GREEN** — one logged-out GET → HTTP 200, 115 784 bytes, 75 `/comments/` markers, returned `RedditScreenLight` (adapter-not-runner holds at runtime). The `byte_count` guard at `:109` is **unnecessary** (adapter sets the key unconditionally). pytest **is** available at `orca-harness/.venv`.
  - **ONLY remaining action:** open a PR for `capture-spine-reddit-screening-v0` → squash-merge → then (at merge) add the repo-map row for `screening_reddit_read.py` and delete the burn-after-consume sub-handoff. **As of this write no PR exists yet.**
- **Option B (IG/TikTok demand probe):** branch `capture-probe-tiktok-demand` is an **empty placeholder (0 commits)** — no work exists. Demand existence is not the question; if ever pursued it is a capture-feasibility/signal-quality recon (per `orca_demand_read_taxonomy_v0.md`), lower priority than the demand-read *reliability* gap that batch-1 backtests score.

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-13 (session; capture-spine CA)
- created_by_lane: capture-spine CA (main thread, the lane that isolated CloakBrowser PR #50 + landed doctrine PR #53). Provenance only, not authority.
- workspace: C:\Users\vmon7\Desktop\projects\orca
- handoff_path: C:\Users\vmon7\Desktop\projects\orca\docs\hygiene\handoff_capture_spine_continuation_v0.md
- expected_branch: ecr-sp3-timing-deriver-slice1 (a HOT SHARED branch, NOT a capture lane — see Drift Guard)
- expected_head: aed85c4
- expected_dirty_state_including_handoff_file: 2 modified (`docs/decisions/screening_reddit_read_route_decision_v0.md`, `docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md`) + ~10 untracked, plus THIS new file (untracked under tracked `docs/hygiene/`).
- load_rule: confirm-don't-trust. Re-verify every load-bearing fact against its compare target before acting. Sender claims are hypotheses, not authority. **The single most load-bearing check: `git fetch origin main` FIRST** — local `main` and PR readiness were both stale this session (caused the closed PR #45).

## Goal Handoff

- long_term_goal: Orca's capture moat is **judgment + cleaning, not data volume / not a data farm** — buy commodity data; self-capture only the modest moat-signal. Live product direction = the **creator-momentum wedge**. (Verify: `docs/research/creator_momentum_data_landscape_v0.md`; restated in `docs/hygiene/handoff_capture_spine_reddit_screening_v0.md` §Frozen.)
- anchor_goal: As capture-spine CA, advance source-capture capability via **smallest-complete** moves landed through the per-lane PR flow — first reconcile the in-flight capture work to merge, then pick the next frontier.
- success_signal: each capture-spine deliverable lands on `main` cleanly via PR (CI green), with no false-success path, and each change traces to the moat (judgment/cleaning), not bulk data capture.

(Note: no `workflow-goal-framing` frame was supplied; `long_term_goal` is carried from the cited capture-spine sources, not invented. Treat as orientation; re-verify before strict use.)

## Open Decision / Fork

- decision: **Which capture-spine lane to drive next?** The user said "continue our capture spine activities (whatever that was before)."
  - options:
    - **A — Finish the Reddit Screening-Read Service merge** (this IS "what was before": the CA-handoff that named the CA role). Pending: re-run the skip-marked live integration receipt for a fresh raw output; optional `byte_count` KeyError guard at `screening_reddit_read.py:109`; confirm/push branch + open PR → main; at merge add the repo-map row. Source: `docs/hygiene/handoff_capture_spine_reddit_screening_v0.md` §Open/next moves.
    - **B — Start the IG/TikTok demand probe** (user floated "perhaps next move would be to tackle IG/TikTok"). A worktree already exists: `orca-worktrees/orca-tiktok-probe-wt` @ `f15de94` [capture-probe-tiktok-demand]. Scope unread — verify its state before assuming progress.
    - **C — Reconcile the two open in-flight PRs first** (#50 CloakBrowser, #53 doctrine) + prune the orphaned/merged worktrees, before opening a new frontier.
  - already constrained / off the table: spawning a NEW build lane while ~12 capture worktrees are already open and 2 PRs are unmerged (WIP sprawl + stale-base risk). Reddit screening must stay adapter-not-runner / screen-light (see Drift Guard) — not a scope to reopen.
  - trade-offs: A closes the explicit owed item and is low-risk (built + reviewed, only a live receipt re-run gates it). B is the user-floated frontier but is greenfield (more risk, unread worktree). C is pure housekeeping the command sheet below already covers.
  - owner of the call: the owner (user) / capture-spine CA.
  - recommendation: do **C** (mechanical, fast — command sheet ready), then **A** (the literal "before"; finish the owed merge), then surface **B** (IG/TikTok) as the next frontier once WIP is reconciled. Rationale: finish-before-start cuts the stale-base risk that bit this session, and A is the item the CA role was handed off to complete.

## Drift Guard

- **FETCH `origin/main` FIRST** before basing any branch or asserting any PR/merge readiness. Local `main` was 23 PRs stale this session; a `git rev-list --left-right main...origin/main` on un-fetched refs falsely read "current" and produced the closed PR #45. Highest-consequence guardrail here.
- **Reddit screening: adapter `fetch_direct_http_capture` ONLY, NEVER `run_source_capture_http_packet`** (the runner writes a packet → ECR; a screening read must never become a capture run). Screen-light, per-screen-bounded, entitlement-gated, logged-out public only, orchestrator-invoked, no standing service.
- **`ecr-sp3-timing-deriver-slice1` is a HOT SHARED branch, NOT a capture lane.** It is the current working tree's branch but belongs to other (ecr/product-lead) work; HEAD drifts (was 46b8371 → now aed85c4 this session). Additive only; home-CA commits to shared/config files auto-deny (owner commits). Do all capture build work in worktrees off fresh `main`.
- **Capture moat = judgment + cleaning, not data volume.** Do not expand any lane into bulk/farm data capture.
- ~12 capture worktrees already exist (see Workspace State). Do not spawn more without reconciling existing ones.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (+ read `.agents/workflow-overlay/README.md` before project work, per `AGENTS.md`).
- capture-spine entry map (enter the ladder here): `docs/workflows/data_capture_spine_consolidation_map_v0.md` (retrieval-only routing map for Data Capture Spine + Source Capture Armory).
- targets to enter the ladder: the consolidation map above; `docs/hygiene/handoff_capture_spine_reddit_screening_v0.md` (the live sub-handoff for the Reddit service); `orca-harness/source_capture/` adapters.
- already loaded (weak orientation, freshness-marked 2026-06-13; NOT authority): this packet's cited reads.
- must load first (before any strict/actionable capture claim): `AGENTS.md`, the overlay `README.md`, and the consolidation map.
- load rule: receiver re-runs progressive source loading per overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- Capture moat = judgment+cleaning, creator-momentum wedge — decided in `docs/research/creator_momentum_data_landscape_v0.md`; compare target: reread-required. Verify before strict product-direction use.
- Reddit screening = adapter-not-runner, screen-light, entitlement-gated — decided in `docs/decisions/screening_reddit_read_route_decision_v0.md` (NOTE: 1 uncommitted correction in the working tree this session — dirty). Verify before touching the screening service.
- Fetch-first discipline — decided this session (PR #45 postmortem) + `AGENTS.md` verification rule ("Absence and build-state are claims… confirm against the primary source"). Compare target: AGENTS.md §Agent Behavior Kernel.
- Subagent return contract (just landed as PR #53, unmerged): orientation/research subagents whose output an agent consumes must return a terse **schema-bound** verdict (named fields, one-line, `file:line` cite, `unknown` for absent), not a prose dump — decided in `.agents/workflow-overlay/prompt-orchestration.md`. Relevant if you dispatch capture-orientation subagents.

## Active Objective

As capture-spine CA, reconcile the in-flight capture work (PRs #50, #53; the Reddit screening service merge) and then advance the next capture-spine frontier — completing the Reddit screening service (the owed item), with the IG/TikTok demand probe as the user-floated next move — each landed via the per-lane PR flow off fresh `main`.

## Exact Next Authorized Action

1. `git fetch origin main`; then `gh pr list --state open` and confirm whether PR #50 (CloakBrowser) and #53 (doctrine) merged, and whether `capture-spine-reddit-screening-v0` is pushed/PR'd/merged (it was local-worktree-only + unpushed at handoff; `screening_reddit_read.py` was ABSENT from `origin/main`).
2. If #50/#53 still open: run the cleanup/merge command sheet (in chat this session — squash-merge #50/#53, prune the `orca-cloak-deeprender`, `subagent-return-contract`, `orca-cloak-geo`, `orca-cloak-scroll` worktrees/branches). Do not merge without reviewing #53's receipt-relocation (it touches 4 files, incl. `dcp_receipts_archive_v0.md`).
3. Reddit screening service (Option A): enter worktree `C:\Users\vmon7\Desktop\projects\orca-capture-spine-reddit-wt` (branch `capture-spine-reddit-screening-v0`, HEAD `4f1ac65`); verify HEAD + the decision-doc's adapter-not-runner wording; re-run `tests/integration/test_reddit_screening_read_live.py` (skip-marked) for a fresh live receipt; optionally add `.get` fallback for `byte_count` at `screening_reddit_read.py:109`; push + open PR → `main`; at merge add a repo-map row for `screening_reddit_read.py` in `docs/workflows/orca_repo_map_v0.md`.
4. Then resolve the Open Decision (A done → surface B, IG/TikTok).
- Stop condition: if any base is stale, any PR conflicts, or a "superseded" claim can't be verified against `origin/main`, STOP and fetch-first / report — do not improvise (this is exactly what produced PR #45).

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` (+ `CLAUDE.md` shim) — overlay-bound; build in worktrees off main; per-lane PR flow; surface ambiguity before acting.
- Overlay or equivalent authority: `.agents/workflow-overlay/` (read `README.md` first).
- User constraints: capture-spine CA role accepted; acutely token-burn-conscious (a Stop-hook `check_token_burn.py` now warns repo-wide — landed via PR #29); wants real next steps done, not deferred; chose to continue capture-spine work; floated IG/TikTok as next.
- Source-read ledger:
  - `origin/main`
    - Role: merge base / compare target for every new capture PR.
    - Load-bearing: yes. Compare target: HEAD — was `72d32e7` at handoff; **reread-required** (moves often; multiple lanes merging).
    - Last checked: 2026-06-13. Reuse rule: ALWAYS re-fetch before basing/asserting. Never trust local `main`.
  - `docs/hygiene/handoff_capture_spine_reddit_screening_v0.md`
    - Role: the live sub-handoff for Option A (Reddit screening service). Compare target: untracked working-tree file; quoted facts: branch `capture-spine-reddit-screening-v0` @ `4f1ac65`, adapter-not-runner, "25 passed" NOT re-verified, live receipt is the real pre-merge gate. Load-bearing: yes. Last checked: 2026-06-13. Reuse rule: reread in full before driving the merge; it says "burn after consume."
  - `orca-capture-spine-reddit-wt` (worktree) / branch `capture-spine-reddit-screening-v0`
    - Role: the Reddit screening service build. Compare target: HEAD `4f1ac65` — reread-required (confirm not pushed/merged). Load-bearing: yes. Reuse rule: verify HEAD before editing.
  - PRs #50 / #53
    - Role: in-flight capture (#50 CloakBrowser deep-render+proxy-geo) + capture-adjacent doctrine (#53 subagent return contract). Compare target: both OPEN/MERGEABLE at handoff — reread via `gh pr view`. Load-bearing: yes (gate step 2).
  - `docs/workflows/data_capture_spine_consolidation_map_v0.md`
    - Role: capture-spine navigation entry map. Compare target: tracked; reread-required. Load-bearing: no (orientation).
- Source gaps: the IG/TikTok probe worktree (`orca-tiktok-probe-wt` @ `f15de94`) state is UNREAD — scope before assuming progress. The Reddit service "25 passed" + push/PR status are unverified.
- Strict-only blockers: none bound; delegated-review convention is provisional only.
- Not-proven boundaries: the Reddit service's "25 passed" suite was never re-run in the home env; the live integration receipt is the only real pre-merge gate and has not been re-run on current code.

## Current Task State

- Completed (this session): CloakBrowser deltas isolated → PR #50 (geo+settle+scroll, 786 tests passed on fresh main, supersession of #22/#23 verified, both closed); subagent return contract rebased+landed → PR #53; token-burn hook confirmed already on main via #29 (identical blob `ab4e330`, nothing to commit).
- Partially completed: PRs #50, #53 OPEN — awaiting your review/squash-merge (you squashed #50's branch to `d3aa658`). Reddit screening service still unmerged/unpushed.
- Broken or uncertain: `origin/main` moved to `72d32e7` (other lanes) — re-fetch. ~12 capture worktrees open; some orphaned (geo/scroll from closed #22/#23) pending prune.

## Workspace State

- Branch: ecr-sp3-timing-deriver-slice1
- Head: aed85c4
- Dirty/untracked before handoff: 2 modified (decision-doc correction for Reddit screening; ontology backbone prompt) + ~10 untracked (incl. `check_token_burn.py` [already on main, untracked here only because branch predates #29], `_scratch/`, the reddit-screening handoff doc, beautypie/conductor review docs from other lanes).
- Dirty/untracked after writing this file: + `docs/hygiene/handoff_capture_spine_continuation_v0.md` (untracked).
- Target files/artifacts: `orca-harness/source_capture/screening_reddit_read.py`; `orca-harness/source_capture/adapters/cloakbrowser_snapshot.py`; the touched tests.
- Related worktrees (capture lanes): `orca-capture-spine-reddit-wt` @ 4f1ac65 [capture-spine-reddit-screening-v0] (Option A); `orca-worktrees/orca-tiktok-probe-wt` @ f15de94 [capture-probe-tiktok-demand] (Option B); `orca-worktrees/orca-cloak-deeprender-wt` @ d3aa658 [capture-cloak-deeprender-v0] (PR #50); `orca-subagent-return-contract-wt` @ (PR #53 branch). Orphaned (prune): `orca-cloak-geo-wt` @ ffacded, `orca-cloak-scroll-wt` @ 0faf262. Other capture lanes (triage later): archive-timing, capture-archive-cdx-bound, capture-spine-bounds, consumer-demand-probe, demand-projection, demand-scan-spec, rung15-openai-payload, capture-wt (detached @ f15de94).

## Changed / Inspected / Tested Files

- `orca-harness/source_capture/adapters/cloakbrowser_snapshot.py`
  - Status: PR #50 (unmerged) adds geo timezone/locale + settle_seconds + scroll_step_px on top of main's #25 core. ABSENT from `origin/main` still.
  - Role: CloakBrowser source-capture adapter. Observations: net diff +1311/−9, 786 tests pass on fresh main.
- `orca-harness/source_capture/screening_reddit_read.py`
  - Status: only on unmerged worktree branch `capture-spine-reddit-screening-v0`. NOT on main.
  - Role: Reddit screening-read service (Option A). Observations: wires adapter `fetch_direct_http_capture` only; pre/post-fetch refusal gates; `byte_count` KeyError risk at :109 (optional `.get` guard).
- `docs/decisions/screening_reddit_read_route_decision_v0.md`
  - Status: tracked, 1 uncommitted correction in working tree (owner to commit in merge sweep). Role: Reddit screening route + adapter-not-runner contract.

## Frozen Decisions

- Reddit screening is adapter-not-runner, screen-light, entitlement-gated, logged-out-public only. Evidence: `docs/decisions/screening_reddit_read_route_decision_v0.md`; reddit handoff §Frozen. Consequence: never wire the packet/ECR runner.
- Capture moat = judgment + cleaning; product direction = creator-momentum wedge. Evidence: `docs/research/creator_momentum_data_landscape_v0.md`. Consequence: no bulk-data-farm expansion.
- Fetch-first before basing/asserting. Evidence: PR #45 postmortem (this session). Consequence: re-fetch origin/main every time.

## Mutable Questions

- A, B, or C next (see Open Decision)? Resolves by owner choice + reconciling the open PRs.
- Does the IG/TikTok probe worktree already hold partial work? Resolves by reading `orca-tiktok-probe-wt` before starting B.
- Has the Reddit service been pushed/PR'd since the reddit handoff was written? Resolves by `gh pr list` + checking `origin/capture-spine-reddit-screening-v0`.

## Superseded / Dangerous-To-Reuse Context

- PR #45 + branch `capture-cloakbrowser`: CLOSED + DELETED. Do NOT recreate. Replacement: PR #50 (`capture-cloak-deeprender-v0`).
- PRs #22 / #23: CLOSED (superseded by #50). Their branches `capture-cloak-proxy-geo` / `capture-cloak-scroll` + worktrees are orphaned — prune, don't reuse.
- Local `main` and any `git rev-list main...origin/main` on un-fetched refs: STALE/MEANINGLESS. Replacement: `git fetch origin main` first.
- The Reddit service "25 passed, 1 skipped": never re-run in home env — NOT a validation. Replacement: the live integration receipt re-run is the real pre-merge gate.
- `check_token_burn.py` showing untracked in this working tree: NOT a missing commit — it is identical (`ab4e330`) to the copy already on `origin/main` (landed via #29). Do not re-commit it.

## Commands And Verification Evidence

- Fetch-first + PR-state check (run first):
  ```bash
  git fetch origin main && git rev-parse origin/main
  gh pr list --state open
  ```
  Result: not run by receiver yet (reread-required). At handoff: origin/main `72d32e7`; #50 + #53 OPEN; reddit service not on main.
- Reddit service live receipt (Option A pre-merge gate), from `orca-capture-spine-reddit-wt`:
  ```bash
  orca-harness/.venv/Scripts/python.exe -m pytest tests/integration/test_reddit_screening_read_live.py
  ```
  Result: not run this session (skip-marked; needs fresh raw output before merge).
- Full offline harness suite (used to validate #50): `orca-harness/.venv/Scripts/python.exe -m pytest` → 786 passed, 1 skipped on the #50 branch. Re-run target for any new capture branch.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: (1) `origin/main` HEAD via fetch; (2) PR #50/#53 state via `gh pr view`; (3) Reddit branch `capture-spine-reddit-screening-v0` HEAD `4f1ac65` + push/merge status; (4) the decision-doc adapter-not-runner wording; (5) the IG/TikTok worktree state before starting B.
- Compare targets: fetched origin/main ref; `gh pr view` JSON; worktree `git rev-parse HEAD`; quoted decision-doc text; worktree file listing.
- Load outcomes: `REUSE` only after all five re-verified; `STALE_REREAD_REQUIRED` if origin/main moved or PRs changed (expected — refresh then proceed); `BLOCKED_DRIFT` if a "superseded" claim can't be confirmed against origin/main; `BLOCKED_MISSING_PACKET` if this file is unreadable.
- Sources to reread on drift: origin/main; the two PRs; the reddit handoff doc; the consolidation map.

## Do Not Forget

- **FETCH `origin/main` FIRST.** The load-bearing guard; skipping it caused PR #45.
- Reddit screening = adapter `fetch_direct_http_capture`, NEVER the packet/ECR runner.
- The literal "what was before" = the **Reddit Screening-Read Service merge** (`docs/hygiene/handoff_capture_spine_reddit_screening_v0.md`); IG/TikTok is the floated next frontier, not the owed item.
- Two PRs (#50, #53) are open + mergeable; the cleanup/merge command sheet is in this session's chat.
