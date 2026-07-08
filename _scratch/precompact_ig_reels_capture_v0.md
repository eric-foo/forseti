# Precompact Working Packet — IG Reels Capture Lane

## Restore Contract

- packet_version: workflow-precompact-v1
- mode: max
- created_at: 2026-06-25
- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- checkpoint_path: `_scratch/precompact_ig_reels_capture_v0.md` (gitignored scratch; disposable)
- expected_branch: worktree `claude/ig-reels-bio-links-pinned`; main checkout is on `codex/ig-reels-capture-spine` (STALE — see Superseded)
- expected_head: `d8b0c8f6` (worktree)
- expected_dirty_state_after_checkpoint: `docs/workflows/ig_reels_capture_to_projection_ecr_cleaning_handoff_v0.md` MODIFIED (uncommitted); this checkpoint file is new + gitignored
- recovery_rule: confirm-don't-trust; re-verify branch/head/dirty, PR #378 merge, and reread sources before strict claims.

## Active Objective

Deep-think how to make the IG public `/reels/` **capture** "complete" — what is lacking and why — to decide the next build (capture hardening vs handing to projection). The capture CODE is done and merged (PR #378); this is an analysis task, not a build.

## Exact Next Authorized Action

1. **Deep-think (the queued task):** across each completeness axis, name what's lacking, WHY, and whose job it is (capture vs projection/ECR/cleaning/judgment). Seed axes:
   - **History/coverage:** only ~12 most-recent reels, one page, no scroll → no full backfill.
   - **Time-series/momentum:** ONE point-in-time snapshot; momentum needs repeated captures over time (cadence/series). Capture emits single packets; series assembly is downstream/deferred.
   - **Join completeness:** rows that don't join to passive JSON get gap metrics (~2/12 unjoined in one probe).
   - **Semantics/meaning:** no ad/bot/demand/credibility verdicts (Judgment-owned, by design).
   - **Surface coverage:** static/main-grid posts excluded (separate surface, deferred); reels-tab pin positive inferred, not directly observed.
   - **Content depth:** caption only when in JSON; no comment text, no commenter identity, no media bytes (non-goals).
   - **Durability/rate:** no scaled monitoring durability/rate envelope; logged-out headless may wall.
2. Produce a prioritized "to make it complete" map = smallest-complete next steps, splitting **capture-lane** work from **downstream-lane** work; for each gap classify: *design-choice (leave)* vs *deferred (route downstream)* vs *real capture gap (fix)*.
3. Stop at analysis. No build/commit without owner authorization.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` / `CLAUDE.md` shim — reread-required.
- Overlay authority: `.agents/workflow-overlay/` (source-loading, decision-routing, artifact-folders) — reread-required.
- User constraints: deep-think the capture completeness; SCR is deprecated (skip); projection/ECR/cleaning come after; momentum focus (beauty/fragrance creators).
- Source-read ledger (all on current `main` after PR #378 merge):
  - `orca-harness/source_capture/ig_reels_grid.py` — Role: parser + `IgReelsJsonCandidate` (incl new `pinned_on_clips_tab`/`pinned_on_timeline`). Compare target: reread-required (changed by PR #378). Reuse rule: reread before strict claims.
  - `orca-harness/runners/run_source_capture_ig_reels_grid_packet.py` — Role: runner + profile snapshot (incl new `bio_links`). Compare target: reread-required. 
  - `orca-harness/source_capture/ig_reels_grid_capture.py` — Role: live capture via shared `fetch_browser_page_observation_capture` adapter. Compare target: reread-required.
  - `orca/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md` — Role: capture-path spec (incl v0-emit-posture + pinned-from-JSON note). Compare target: reread-required.
  - `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md` — Role: projection mechanical-only doctrine. Compare target: reread-required.
  - `docs/workflows/ecr_spine_submap_v0.md` — Role: ECR spine + SCR-dormant. Compare target: reread-required.
  - `docs/workflows/ig_reels_capture_to_projection_ecr_cleaning_handoff_v0.md` — Role: the downstream handoff (refreshed 2026-06-25, UNCOMMITTED). Compare target: working-tree, dirty.
- Source gaps: no capture durability/rate envelope; no multi-capture series assembler; reels-tab pin positive unobserved.
- Not-proven boundaries: no platform-stability claim; no ad/bot/demand/credibility classification; logged-out reels access not guaranteed (may wall).

## Current Task State

- Completed:
  - Adversarial review of the runner (3 issues: views-only rollup, fake-known timestamp, `--output`/env routing) — already fixed by the codex lane; verified live.
  - #4 packet-shape decision via SCI+MGT: derived per-row fields stay **derivable-not-emitted** (lean); spec aligned.
  - `bio_links` (profile multi-link) + `pinned_on_clips_tab`/`pinned_on_timeline` (JSON-sourced) implemented, tested, **and live-probe-validated** (2026-06-25).
  - **PR #378 MERGED** to `main` (43 tests green on current main at merge).
  - SCR confirmed deprecated/dormant (ECR submap; #375).
  - Downstream handoff doc refreshed (front-loaded "Refresh 2026-06-25" block).
- Partially completed:
  - Handoff-doc refresh is UNCOMMITTED on `claude/ig-reels-bio-links-pinned` — not yet in `main`.
- Broken or uncertain:
  - Reels-tab pin positive (`clips_tab_pinned_user_ids` non-empty) inferred, not directly observed.

## Workspace State

- Branch: worktree `claude/ig-reels-bio-links-pinned`; main checkout on `codex/ig-reels-capture-spine`.
- Head: `d8b0c8f6` (worktree).
- Dirty before checkpoint: handoff doc modified (uncommitted).
- Dirty after checkpoint: same + this gitignored scratch file.
- Target files: the IG capture files (now in `main`) + the handoff doc.
- Related branches: `main` (~#377, has the merged capture work); `codex/ig-reels-capture-spine` (stale).

## Changed / Inspected / Tested Files

- `docs/workflows/ig_reels_capture_to_projection_ecr_cleaning_handoff_v0.md`
  - Status: MODIFIED, uncommitted.
  - Role: capture → projection/ECR/cleaning handoff; added front-loaded "Refresh 2026-06-25" block (bio/pinned deltas, SCR-dormant, state-moved, stale-ledger flag).
  - Decision pending: land in `main` (its own doc commit) or leave on the branch.
- IG capture files (`ig_reels_grid.py`, runner, capture module, 2 tests, spec): merged via PR #378 — no longer dirty.

## Frozen Decisions

- Pinned posture comes from **passive JSON** (`clips_tab_pinned_user_ids` / `pinned_for_users`), NOT the DOM — proven by 2026-06-25 live probe (no DOM "Pinned" marker exists). Do NOT reintroduce a DOM pin selector.
- #4 lean: derived per-row fields (`join_status`, `extraction_mode`, `route_status`, `selected_fields`, per-row `selection_policy_version`) are derivable-not-emitted; downstream derives or promotes.
- SCR deprecated/dormant; default route is evidence pack → Judgment; pipeline = capture → projection → ECR → cleaning → judgment (skip SCR).
- `bio_links` captures `{title,url}` public link-in-bio destinations.

## Mutable Questions

- Should the handoff-doc refresh land in `main` (separate doc commit) now? — resolve by owner preference.
- Confirm the reels-tab pin positive directly? — needs a creator with a reel pinned to the reels tab; resolve by probe if owner wants.
- What to build next (deep-think output) — the queued task; open until the analysis runs.

## Superseded / Dangerous-To-Reuse Context

- DOM-based `detectPinnedMarker` (PR #378 commit 1's first approach): SUPERSEDED by JSON pinned (commit 2). Dangerous to reintroduce — the live probe proved the DOM has no pin marker. Current replacement: `pinned_on_clips_tab`/`pinned_on_timeline`.
- Local `codex/ig-reels-capture-spine` branch: STALE (main ~30 PRs ahead, already has the reels lane). Do NOT PR it whole. Current path: the merged PR #378 / `main`.
- Handoff's original 2026-06-22 source-ledger SHA256s: superseded → `reread-required` (IG files changed by #378; ECR submap changed by #375).
- PR #378 "OPEN" status anywhere in chat: superseded — it is **MERGED**.

## Commands And Validation Evidence

- `python -m pytest tests/unit/test_ig_reels_grid.py tests/unit/test_source_capture_ig_reels_grid_packet.py tests/unit/test_source_capture_ig_calls_packet.py tests/unit/test_run_source_capture_packet_lake.py`
  Result: passed/`43 passed` on current `main` with PR #378 applied (re-run target if continuing code work).

## Blockers And Risks

- No blockers; the next action (deep-think) is analysis only.
- Risk: the deep-think must not silently expand capture scope — classify each gap as design-choice / deferred-downstream / real-gap before recommending any build (SCI).

## Recovery Instructions

- Required checks: `git rev-parse --short HEAD` (worktree); `git status --porcelain`; `gh pr view 378 --json state` (expect MERGED); confirm handoff doc still modified; reread the source-ledger files (all reread-required).
- Recovery outcomes: `REUSE` (state matches → run the deep-think); `STALE_REREAD_REQUIRED` (sources drifted → reread then deep-think); `BLOCKED_DRIFT` (unexpected edits/branch); `BLOCKED_MISSING_PACKET` (this file gone).
- Reread if drift: the IG capture files, projection doctrine, ECR submap, the handoff doc.

## Do Not Forget

- The queued next action is the **deep-think on capture completeness** (not a build). Classify each gap as design-choice / deferred / real-gap.
- Pinned = JSON, never DOM (live-probe-proven). SCR is deprecated.
- The handoff-doc refresh is still uncommitted; everything else is merged in `main`.
