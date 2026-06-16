# Cold Handoff — Capture Spine: Reddit Screening-Read Service

> Disposable cold-handoff packet (burn after consume). Orientation, **not** authority.
> Confirm every load-bearing claim against the cited durable source before acting.
> Source hierarchy: `AGENTS.md` > `.agents/workflow-overlay/` > `docs/`. Verify branch/HEAD on entry — hot shared tree, many lanes.

## Goal
Give screening agents a **bounded, entitlement-gated, screen-light** way to read public Reddit (WebFetch tool-blocks `reddit.com` for screening agents). The read must **never** become a capture packet / enter ECR — "screening read, not a capture run."

## State — done + home-CA-verified against source
- **Service built + cross-vendor-reviewed + verified.**
  - Worktree `C:\Users\vmon7\Desktop\projects\orca-capture-spine-reddit-wt`, branch `capture-spine-reddit-screening-v0`, HEAD `4f1ac65` (harden) over `0b02b1f` (build). Clean; **NOT pushed**.
  - `orca-harness/source_capture/screening_reddit_read.py` → `reddit_screening_read(url, timeout_seconds=20, max_bytes=2_000_000) -> RedditScreenLight | RedditScreeningReadRefused`.
  - Verified by source read: wires **only** the adapter `fetch_direct_http_capture` (no packet/ECR — sole forbidden-symbol occurrence is the line-5 boundary *comment*); pre-fetch gate (https + old/www.reddit.com + `/r/` + dot-segment refusal, no network); post-fetch login refusal; bounded screen-light output. Cross-vendor review (gpt-5-codex) found+patched scheme/dot-segment/body-login gaps.
  - NOT independently re-verified: the "25 passed" suite (no pytest in home env; 17 test fns + parametrization ≈ 25, code-consistent) and the live receipt (advisory).
- **Durable artifacts (the lane spine — confirm, don't trust):**
  - `docs/decisions/screening_reddit_read_route_decision_v0.md` — route + contract (adapter-not-runner; has 1 dirty correction this session → owner to commit).
  - `docs/product/source_capture_toolbox/source_capture_playbook_v0.md` — capture method (Step 0 entitlement, risk posture).
  - `docs/product/source_capture_toolbox/capture_recon_index_v0.md` — Reddit-discovery read shape.

## Open / next moves
1. **Owner is taking the MERGE** of `capture-spine-reddit-screening-v0`. Before merge:
   - Re-run the **live integration receipt** (`tests/integration/test_reddit_screening_read_live.py`, skip-marked) for FRESH raw output — the one real pre-merge gate.
   - (optional) guard the `byte_count` KeyError at `screening_reddit_read.py:109` (`.get` fallback). Low-risk.
2. **At merge (not before):** add a repo-map row in `docs/workflows/orca_repo_map_v0.md` for `screening_reddit_read.py` (file only on the unmerged branch now → a row before merge dangles). Repo map is shared/auto-deny → owner commits.
3. Dirty on `ecr-sp3` this session for the owner's merge sweep: the decision-doc correction.

## Frozen — do not relitigate
- **Adapter `fetch_direct_http_capture`, NEVER `run_source_capture_http_packet`** (it writes packet→ECR).
- Screen-light only; per-screen-bounded; orchestrator-invoked; no standing service; entitlement gate first; logged-out public only.
- Capture moat = **judgment + cleaning**, not data/farm (buy commodity; self-capture only the moat-signal modestly). Live product direction = the **creator-momentum wedge** (`docs/research/creator_momentum_data_landscape_v0.md`; `docs/hygiene/precompact_creator_momentum_wedge_v0.md`).

## Drift guards
- Hot shared branch `ecr-sp3-timing-deriver-slice1` (NOT ours) — additive only; HEAD drifts; home-CA commits auto-deny (owner commits); build work goes in worktrees.
- Before any further build: verify worktree HEAD `4f1ac65` + the decision doc's adapter-not-runner wording.

## First move for the fresh thread
Confirm the merge status of `capture-spine-reddit-screening-v0`. Unmerged → drive the pending items above. Merged → add the repo-map row + delete this handoff. Either way, reread the cited artifacts before acting; do not inherit this packet's claims.
