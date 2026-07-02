# Handoff Packet: IG Lane Orchestrator And Operator Extraction

```yaml
retrieval_header_version: 1
artifact_role: durable cold-lane handoff packet
scope: Repo-visible rehandoff for the merged IG lane orchestrator/operator extraction work from PR #463.
use_when:
  - A fresh lane needs the IG orchestrator/operator extraction context after PR #463.
  - A receiver was told to find docs/hygiene/ig_lane_orchestrator_operator_extraction_handoff_v0.md and could not because the first packet was never committed.
  - Continuing capture/data-lake propagation work from the merged IG baseline.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - docs/workflows/orca_repo_map_v0.md
branch_or_commit: origin/main @ 83f19bb2f56f4bb1a921d4ee2b28fe4b4952afd7
stale_if:
  - origin/main does not contain PR #463 merge commit 83f19bb2f56f4bb1a921d4ee2b28fe4b4952afd7.
  - Any load-bearing file named in this packet has changed and the receiver has not reread it.
  - A newer handoff supersedes this packet.
```

## Load Contract

- packet_version: handoff_v0_reissued
- mode: max
- source_loading_mode: repo-overlay-bound
- created_at: 2026-06-29
- created_by_lane: Codex current thread, sender only; not an authority claim
- handoff_path: `docs/hygiene/ig_lane_orchestrator_operator_extraction_handoff_v0.md`
- transport_branch: `codex/ig-lane-orchestrator-rehandoff`
- expected_main_anchor: `origin/main` contains PR #463 merge commit `83f19bb2f56f4bb1a921d4ee2b28fe4b4952afd7`
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting. Sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: Keep Instagram, YouTube, and later TikTok capture/data-lake behavior coherent around bronze/silver outputs, transcript/product extraction, route receipts, and honest completion states, without forcing identical platform acquisition methods.
- anchor_goal: Use the merged IG lane orchestrator/operator extraction work as the current IG baseline, and continue only from freshly verified `origin/main` state rather than from the missing uncommitted packet.
- success_signal: A fresh lane can fetch this handoff branch or read the merged implementation files from `origin/main`, verifies PR #463 is merged, and does not reimplement the already-merged IG orchestrator/operator extraction slice unless explicitly redirected.

## Open Decision / Fork

- decision: None open for PR #463 itself; it is merged. The next fork is what lane the owner wants after this context transfer.
  - options: continue downstream capture/data-lake propagation doctrine; start a new platform lane such as YouTube follow-up or future TikTok; run live IG validation if runtime confidence is needed.
  - already constrained / off the table: do not search for the old uncommitted packet as if it existed in git history before this reissue; do not treat this packet as validation, readiness, or approval; do not force identical acquisition mechanics across IG, YT, and TT.
  - owner of the call: current user / owner.
  - recommendation and why: Verify the merged implementation files on `origin/main`, then follow the current user directive for the next lane. There is no PR #463 implementation blocker left to solve.

## Drift Guard

- The previous handoff packet was never committed. A fresh lane could not find it because it did not exist in git history.
- PR #463 implementation is merged. Do not treat it as open conflict work unless fresh drift proves otherwise.
- This packet is context transfer only. It is not a test result, live capture receipt, owner approval, or readiness proof.
- Shared capture behavior does not mean identical acquisition method. The accepted direction is shared receipts/lake/product behavior with platform-specific adapters.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- targets to enter the ladder:
  - `docs/workflows/orca_repo_map_v0.md`
  - `orca-harness/runners/run_ig_reels_lane_orchestrator.py`
  - `orca-harness/runners/run_ig_reels_operator_product_extract.py`
  - `orca-harness/source_capture/lane_orchestration.py`
  - `orca-harness/cleaning/transcript_product_lake.py`
  - `orca-harness/tests/unit/test_ig_reels_lane_orchestrator.py`
  - `orca-harness/tests/unit/test_ig_reels_operator_product_extract.py`
  - `orca-harness/tests/unit/test_transcript_product_lake.py`
- already loaded (weak orientation, freshness-marked; not authority): current-thread memory, current `gh pr view 463`, current `git ls-tree origin/main`, and current `git show origin/main:docs/workflows/orca_repo_map_v0.md` excerpts.
- must load first before strict or actionable steps: `AGENTS.md`, overlay README, source-loading overlay, and the concrete implementation files on the fetched ref the receiver will use.
- load rule: receiver re-runs progressive source loading per overlay; the packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors

- PR #463 landed the IG lane orchestrator/operator extraction slice.
  - verify pointer: `gh pr view 463 --json state,mergedAt,mergeCommit,headRefOid` and `git show --stat 83f19bb2f56f4bb1a921d4ee2b28fe4b4952afd7`.
- The missing packet problem was a handoff persistence error, not an implementation merge failure.
  - verify pointer: before this reissue, `git log --all -- docs/hygiene/ig_lane_orchestrator_operator_extraction_handoff_v0.md` returned no output, while `git ls-tree origin/main` showed the implementation files.
- IG operator-assisted product extraction writes into the same silver product-mentions lane as provider-backed extraction, with honest backend/provenance.
  - verify pointer: reread `run_ig_reels_operator_product_extract.py`, `run_ig_reels_product_extract.py`, and `transcript_product_lake.py` from current `origin/main`.
- The lane orchestrator sequences requested IG lanes and exposes shared lane receipts; it does not standardize acquisition method across platforms.
  - verify pointer: reread `source_capture/lane_orchestration.py` and `run_ig_reels_lane_orchestrator.py` from current `origin/main`.

## Active Objective

This packet does not reopen implementation. It restores repo-visible context for the merged IG lane orchestrator/operator extraction work and tells a cold reader how to verify the merged baseline before continuing to the owner's next lane.

## Exact Next Authorized Action

1. Fetch the repo and verify PR #463 state: `git fetch origin` and `gh pr view 463 --json state,mergedAt,mergeCommit,headRefOid,url,title`.
2. Verify the implementation files exist on the chosen ref: `git ls-tree -r --name-only origin/main | rg "run_ig_reels_lane_orchestrator.py|run_ig_reels_operator_product_extract.py|source_capture/lane_orchestration.py"`.
3. Read `docs/workflows/orca_repo_map_v0.md` and the three implementation files named above before making strict behavior claims.
4. Continue only with the next owner-directed lane. Do not patch PR #463 unless new drift is freshly observed.

## Authority And Source Ledger

- `AGENTS.md`: project rules, SCI/MGT, git/worktree lifecycle, verification requirements. Load-bearing: yes. Compare target: reread from repo before strict/actionable use. Reuse rule: orientation until reread.
- `.agents/workflow-overlay/README.md`: Orca overlay binding rule. Load-bearing: yes. Compare target: reread from repo before strict/actionable use. Reuse rule: re-read in fresh lane.
- PR #463: merged implementation PR. Load-bearing: yes. Compare target: `gh pr view 463 --json number,state,mergedAt,baseRefName,headRefName,headRefOid,mergeCommit,url,title`. Last checked: observed `state:"MERGED"`, `mergedAt:"2026-06-29T15:23:06Z"`, `mergeCommit.oid:"83f19bb2f56f4bb1a921d4ee2b28fe4b4952afd7"`.
- Merged implementation files on `origin/main`: actual source baseline. Load-bearing: yes. Compare target: `git ls-tree -r --name-only origin/main | rg "run_ig_reels_lane_orchestrator.py|run_ig_reels_operator_product_extract.py|source_capture/lane_orchestration.py"`. Last checked: observed all three paths.
- Repo map route: `docs/workflows/orca_repo_map_v0.md`. Load-bearing: yes for navigation, no for validation/readiness. Compare target: `git show origin/main:docs/workflows/orca_repo_map_v0.md | Select-String "IG lane orchestrator|run_ig_reels_operator_product_extract.py|lane_orchestration.py"`.
- Old packet absence: before this reissue, `git log --all -- docs/hygiene/ig_lane_orchestrator_operator_extraction_handoff_v0.md` returned no output. Load-bearing: yes for explaining why the receiver could not find it. Reuse rule: after this branch/PR, distinguish pre-reissue absence from post-reissue branch presence.

## Current Task State

- Completed:
  - PR #463 merged to `main` at merge commit `83f19bb2f56f4bb1a921d4ee2b28fe4b4952afd7`.
  - Merged implementation files are visible on `origin/main`.
  - Repo map on `origin/main` routes to the IG orchestrator/operator extraction files.
  - This packet reissues the previously missing handoff path as a repo-visible artifact on branch `codex/ig-lane-orchestrator-rehandoff`.
- Partially completed:
  - This packet is not on `main` until its handoff branch/PR is merged.
- Broken or uncertain:
  - No live end-to-end IG orchestrator run is claimed by this packet.
  - No next implementation lane is selected by this packet.

## Workspace State

- Sender root checkout: `C:\Users\vmon7\Desktop\projects\orca`
- Sender rehandoff worktree: `C:\tmp\orca-ig-lane-orchestrator-rehandoff`
- Rehandoff branch: `codex/ig-lane-orchestrator-rehandoff`
- Base: `origin/main` at `83f19bb2f56f4bb1a921d4ee2b28fe4b4952afd7`
- Expected dirty state before committing this packet: only `docs/hygiene/ig_lane_orchestrator_operator_extraction_handoff_v0.md` is new.
- Related PR: #463, already merged.

## Changed / Inspected / Tested Files

- `docs/hygiene/ig_lane_orchestrator_operator_extraction_handoff_v0.md`
  - Status: added by this rehandoff branch.
  - Role: durable cold-lane packet replacing the missing uncommitted handoff.
  - Important observations: The filename intentionally matches the missing packet name so the original path becomes findable after this branch is fetched or merged.
- `orca-harness/runners/run_ig_reels_lane_orchestrator.py`
  - Status: merged by PR #463.
  - Role: sequences requested IG grid, deep-capture, product extraction, and projection lanes with shared receipts.
- `orca-harness/runners/run_ig_reels_operator_product_extract.py`
  - Status: merged by PR #463.
  - Role: operator-assisted strict JSON product extraction export/import path.
- `orca-harness/source_capture/lane_orchestration.py`
  - Status: merged by PR #463.
  - Role: shared receipt/summary contract.
- `docs/workflows/orca_repo_map_v0.md`
  - Status: merged by PR #463 and subsequent main updates.
  - Role: navigation map; route context only.

## Frozen Decisions

- The old packet was not committed and should not be searched for in git history before this reissue.
- PR #463 implementation is merged.
- IG lane context should be verified from source files on `origin/main`, not from thread memory.

## Mutable Questions

- What lane should continue after this rehandoff? The user has not selected the next implementation or planning lane in this request.
- Should this handoff branch be merged to `main` or used as a branch-scoped courier artifact? This depends on owner preference or PR landing.

## Superseded / Dangerous-To-Reuse Context

- Stale: `Get back context from docs/hygiene/ig_lane_orchestrator_operator_extraction_handoff_v0.md` before this reissue. Why stale: the file did not exist in git history. Replacement: this reissued packet on branch `codex/ig-lane-orchestrator-rehandoff`, plus merged implementation files on `origin/main`.
- Stale: PR #463 has a repo-map conflict. Why stale: the conflict was resolved and PR #463 merged. Replacement: verify `gh pr view 463` and current `origin/main`.
- Stale: same-turn self-review as delegated-review evidence. Why stale: it did not satisfy de-correlation. Replacement: rely on merged source and any external review only as historical orientation.

## Commands And Verification Evidence

- Command: `gh pr view 463 --json number,state,mergedAt,baseRefName,headRefName,headRefOid,mergeCommit,url,title`
  - Result: passed; observed `state:"MERGED"`, `mergedAt:"2026-06-29T15:23:06Z"`, `mergeCommit.oid:"83f19bb2f56f4bb1a921d4ee2b28fe4b4952afd7"`, `headRefOid:"c93d972ed7a42877425f3774e13ab542a0d86087"`.
- Command: `git log --all --oneline -- docs/hygiene/ig_lane_orchestrator_operator_extraction_handoff_v0.md`
  - Result: passed before this reissue; no output.
- Command: `git ls-tree -r --name-only origin/main | rg "ig_lane_orchestrator_operator_extraction_handoff_v0|run_ig_reels_lane_orchestrator.py|run_ig_reels_operator_product_extract.py|source_capture/lane_orchestration.py"`
  - Result: passed; the three implementation files were present; the handoff packet was not present on `origin/main` before this reissue.
- Command: `git show --stat --oneline 83f19bb2f56f4bb1a921d4ee2b28fe4b4952afd7 --`
  - Result: passed; merge commit for PR #463, 10 files changed, including the two runners and `lane_orchestration.py`.

## Blockers And Risks

- The handoff packet is branch-scoped until merged. Fetch the branch directly or merge the handoff PR.
- This packet can be mistaken for validation. Rerun tests or live probes if validation is needed.
- Future main updates can move repo-map lines again. Treat repo map as navigation only and verify actual source files.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - PR #463 merged state and merge commit.
  - Presence of merged implementation files on the chosen ref.
  - Repo map route entries if using the map for navigation.
  - This packet's branch/path if using it as the handoff source.
- Compare target for each:
  - `gh pr view 463 --json state,mergedAt,mergeCommit,headRefOid`
  - `git ls-tree -r --name-only origin/main | rg "run_ig_reels_lane_orchestrator.py|run_ig_reels_operator_product_extract.py|source_capture/lane_orchestration.py"`
  - `git show origin/main:docs/workflows/orca_repo_map_v0.md | Select-String "IG lane orchestrator|run_ig_reels_operator_product_extract.py|lane_orchestration.py"`
  - `git show origin/codex/ig-lane-orchestrator-rehandoff:docs/hygiene/ig_lane_orchestrator_operator_extraction_handoff_v0.md`
- Load outcomes:
  - `REUSE`: all load-bearing facts match; continue from the merged IG baseline.
  - `PARTIAL_REUSE`: optional route text drifted; use verified source files and current user instruction.
  - `STALE_REREAD_REQUIRED`: branch, PR, or source files drifted; reread before acting.
  - `BLOCKED_DRIFT`: drift conflicts with the claim that #463 is merged or files exist.
  - `BLOCKED_MISSING_PACKET`: this packet branch/path is not available; use the merged implementation files on `origin/main` as fallback orientation.
  - `BLOCKED_UNVERIFIABLE`: a load-bearing claim cannot be checked; stop rather than relying on thread memory.

## Do Not Forget

The old handoff failed because it was not committed. This rehandoff is only useful if the receiver fetches the rehandoff branch or the branch/PR is merged; otherwise use the merged #463 implementation files on `origin/main` as the source of truth.