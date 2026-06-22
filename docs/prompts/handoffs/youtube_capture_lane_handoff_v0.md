# Handoff Packet — YouTube Capture Lane

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet (durable continuation artifact; NOT validation/readiness/authorization)
scope: >
  Transfers the YouTube public-data capture lane to a fresh lane/agent/thread that holds none of the
  sender's context. The lane covers: capturing YouTube PUBLIC data (video/creator/comment metadata +
  a labeled Return-YouTube-Dislike estimate) at volume via HTTP-level stealth tooling, and the lane's
  open build items (the Renovate curl_cffi freshness PR, the GATED rung-2 curl_cffi shared adapter,
  and orphan-branch cleanup). Instagram / crawling work is a SEPARATE lane (a different thread) and
  is explicitly OUT OF SCOPE here.
use_when:
  - Picking up the YouTube capture lane cold; running captures; or finishing the lane's open PRs / build items.
authority_boundary: retrieval_only
stale_if:
  - origin/main advances past the compare targets below (it moves fast — fetch fresh first).
  - PR #344 (Renovate curl_cffi freshness) merges — its files move from branch-only to main.
  - The owner gives the curl_cffi optional-dependency go (unblocks the rung-2 adapter build).
  - The orphan branch claude/xenodochial-greider-ec61aa is deleted.
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-22 (date stamp from session context; verify via `git log` of this file — the author's clock API was unavailable)
- created_by_lane: the `claude/ig-rung2-finding` worktree (provenance only — NOT an authority claim)
- workspace: the Orca repo. This packet was written from the worktree at `C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\xenodochial-greider-ec61aa`. **The YouTube receiver should work in its OWN fresh worktree/branch off `origin/main`**, not in that worktree (it stays the Instagram lane).
- handoff_path: `docs/prompts/handoffs/youtube_capture_lane_handoff_v0.md`
- this_packet_lane_branch: `claude/youtube-capture-lane-handoff` (created off `origin/main`)
- expected_head (origin/main at handoff time): `b3072a0b` — **fast-moving; fetch fresh before trusting**
- expected_dirty_state: this handoff file is newly created → untracked, then committed on `claude/youtube-capture-lane-handoff` (see Workspace State)
- load_rule: **confirm-don't-trust** — re-verify every load-bearing fact against its compare target before acting; the sender's claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: Orca capture spine — durable, public-data capture of creator-momentum / anti-bot-integrity signals across social platforms, feeding the judgment / projection spine.
- anchor_goal: Continue the YouTube lane — **PRIMARILY capturing YouTube public data** (video / creator / comment metadata + dislike estimate) at volume using the existing stealth tooling; SECONDARILY closing the lane's open build items.
- success_signal: YouTube public data captured into lean **gitignored** packets usable for analysis, with the stealth transport kept current (fingerprint freshness), the open PR(s) resolved, and the rung-2 build decision actioned per owner go.

(Derived from the user's handoff instruction "continuing YT lane (mostly for capturing information)" plus the YT recon/playbook; no formal `workflow-goal-framing` frame was supplied → treat `success_signal` as advisory.)

## Open Decision / Fork

- **decision 1 — build the shared rung-2 `curl_cffi` adapter now, or keep capturing on the existing YT-local client?**
  - options: (a) build `orca-harness/source_capture/adapters/curl_cffi_http.py` (stateless, **NO proxy**, **NO urllib fallback** / fail-loud-and-closed, `block_shell`-wired, conforming to `orca-harness/docs/adapter_author_contract.md`) + tests + the `[impersonate]` extra in `orca-harness/pyproject.toml` — architecture-DECIDED; (b) defer it and keep capturing with the proven YT-local `orca-harness/youtube_capture/stealth_client.py`.
  - already constrained / off the table: the rung-2 build is **GATED on the owner's explicit `curl_cffi` optional-dependency go** (not yet given) — do NOT build without it. The cross-source stealth **default-flip is REJECTED**. The YouTube **re-port onto the adapter is DEFERRED**.
  - trade-offs: the shared adapter generalizes the transport (other sources could consume it) but adds a `curl_cffi` runtime-dependency surface; deferring keeps capture moving on the working local client.
  - owner of the call: the human owner (the `curl_cffi`-dependency go).
  - recommendation: **capture can proceed NOW** on `stealth_client.py` without the adapter; only start the rung-2 `/fused` build **after** the owner's go.
- **decision 2 — merge PR #344 (Renovate `curl_cffi` freshness):** owner-gated. **After merge, the Renovate GitHub App must be installed on the repo** for the config to do anything (the `renovate.json` is inert without the app).

## Drift Guard

- **Public-data ONLY; anonymous-only (NO account login, NO `po_token`); SG-legal non-criminal use.** Violating this breaks the entire legal/ToS footing the lane rests on.
- **NEVER commit captured data** — it is gitignored: `orca-harness/youtube_capture/{packets/,shorts_scroll_runs/,route_guard.json}`. Committing scraped data is a posture + hygiene breach.
- **NO proxy in the default transport** — proxy / residential rotation is a SEPARATE higher rung (CloakBrowser). The owner explicitly vetoed proxy-as-default.
- **probe-then-pin / cheapest-first:** pin the cheapest working rung per source, logged in the recon index; **NO blanket stealth default.** The owner explicitly vetoed "make the heavy rung the default."
- **Do NOT bypass harness guards:** the pre-push guard (`.githooks/pre-push` blocks branch-deletion pushes), the self-modification guard (on `.claude/settings*`), and the detection-evasion classifier. Use `gh api` / owner action for gated ops; never `--no-verify` without explicit owner go.
- **This is the YOUTUBE lane.** Do NOT do Instagram / crawling work — that is a separate lane in its own thread. Lane separation is the whole point of this handoff.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/README.md` (read the Orca overlay before project work, per `AGENTS.md`). This is overlay-bound, NOT zero-config.
- targets to enter the ladder:
  - `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_recon_v0.md` — the YT recon (GO; unified long-form + Shorts; dislikes routes; po_token; route-health).
  - `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_agent_playbook_v0.md` — CODE-ENFORCED vs MUST-FOLLOW conventions for agents.
  - `orca-harness/youtube_capture/` — the tooling (see Changed/Inspected Files).
  - `orca/product/spines/capture/core/source_capture_toolbox/weapon_anti_block_http_ladder_v0.md` — the rung ladder (rung-2 `curl_cffi` gated/unbuilt; proxy/cloakbrowser separate higher rungs).
  - `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md` — the cross-source pin-log.
- already loaded (weak orientation, freshness-marked; NOT authority): the author read all of the above on `origin/main @ b3072a0b` (2026-06-22).
- must load first (before strict/actionable steps): the recon doc + playbook + the anti-block ladder, re-read fresh from current `origin/main`.
- load rule: the receiver re-runs progressive source loading per the overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- **YT unified long-form + Shorts** (one substrate / paths / route; `surface_type` discriminator = serving-surface, NOT duration alone — Shorts run up to ~180s). Decided in: `youtube_capture_recon_v0.md`. Verify before: any surface-split assumption.
- **probe-then-pin / cheapest-first ladder**; rung-0 `direct_http` honest baseline; **rung-2 = `curl_cffi` (GATED / UNBUILT)**. Decided in: `weapon_anti_block_http_ladder_v0.md`. Verify before: any rung/transport claim.
- **Dislikes = Return-YouTube-Dislike (RYD) labeled ESTIMATE**, never YouTube ground truth (~±15-25% post-2021-cutoff). Implemented in: `orca-harness/youtube_capture/enrich_ryd_v0.py`. Verify before: treating dislikes as truth.
- **Fingerprint freshness = Renovate auto-PR of `curl_cffi` + a MANUAL freshness check (Option 1; no live CI gate)** — `verify_fingerprint_v0.py` hits a third-party TLS echo, so it cannot be a clean deterministic CI gate. In: PR #344. Verify before: changing the freshness approach.
- **IG vs YT distinction (IG-lane context, included ONLY so the YT receiver does not pull IG into scope):** Instagram is pinned at rung-3 logged-out `browser_snapshot` (NOT cloak); the rung-2 `curl_cffi` costume was never probed for IG and was DEFERRED (IG's binding constraint is per-IP *pace*, not fingerprint). Decided in: `orca/product/spines/capture/core/source_families/social_media/instagram/ig_capture_findings_consolidated_v0.md` (the rung-2 finding — note: that bullet is on PR #346's branch `claude/ig-rung2-finding`, NOT yet on main). Verify before: assuming YT and IG share a transport.

## Active Objective

Continue the YouTube public-data capture lane: primarily **run captures** with the existing stealth tooling (`orca-harness/youtube_capture/`), and resolve the lane's open items (merge #344 + install the Renovate app; build the rung-2 `curl_cffi` adapter once the owner gives the dependency go; clean the now-unblocked orphan branch).

## Exact Next Authorized Action

1. In a **FRESH worktree/branch off `origin/main`** (NOT the Instagram worktree): `git fetch origin` and confirm main contains #342 + #343 (compare targets below).
2. **To CAPTURE:** run `orca-harness/youtube_capture/capture_youtube_v0.py` (per-video) and `shorts_scroll_capture_v0.py` (volume). Requires `curl_cffi` installed (`pip install curl_cffi`). Captured data is **gitignored — never commit it.**
3. **PR #344** (Renovate `curl_cffi`): owner-gated merge; **AFTER merge, install the Renovate GitHub App** on the repo (config is inert otherwise).
4. **rung-2 adapter:** ONLY after the owner's `curl_cffi`-dependency go → run `/fused` for it (smallest-complete: adapter + tests + `[impersonate]` extra; NO runner / doctrine-flip / YT-re-port).
5. **Orphan cleanup (now unblocked — #343 is merged):** delete `claude/xenodochial-greider-ec61aa` (local + remote). The remote delete is owner-gated (the pre-push guard blocks branch-deletion pushes) → use `gh api -X DELETE repos/eric-foo/orca/git/refs/heads/claude/xenodochial-greider-ec61aa` or the GitHub Branches UI.
6. **Stop condition:** do NOT start Instagram / crawling work (separate lane).

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` + `CLAUDE.md` (shim) at repo root; the overlay at `.agents/workflow-overlay/README.md`.
- Overlay authority: `.agents/workflow-overlay/` (source loading, validation gates, prompt orchestration, decision routing).
- User constraints: public-data only; anonymous-only; SG-legal non-criminal; no proxy default; never commit captured data; do not bypass harness guards; this lane = YouTube only.
- Source-read ledger:
  - `orca-harness/youtube_capture/{README,capture_youtube_v0,enrich_ryd_v0,shorts_scroll_capture_v0,stealth_client,verify_fingerprint_v0}.py`
    - Role: the YT capture tooling (entry points + transport + dislike enrich + fingerprint check).
    - Load-bearing: yes.
    - Compare target: `git ls-tree -r --name-only origin/main -- orca-harness/youtube_capture/` returns these 6 files; re-read each before strict use.
    - Last checked: 2026-06-22 @ origin/main `b3072a0b`.
    - Reuse rule: orient only; re-read fresh before editing/running.
  - `orca/product/spines/capture/core/source_families/social_media/youtube/{youtube_capture_recon_v0,youtube_capture_agent_playbook_v0}.md`
    - Role: recon (GO/route/dislikes/po_token) + agent playbook (conventions).
    - Load-bearing: yes.
    - Compare target: present on `origin/main`; re-read before acting.
    - Last checked: 2026-06-22 @ `b3072a0b`.
    - Reuse rule: re-read fresh.
  - `orca/product/spines/capture/core/source_capture_toolbox/weapon_anti_block_http_ladder_v0.md`
    - Role: the rung ladder (cheapest-first; rung-2 curl_cffi gated; proxy/cloak separate higher rungs).
    - Load-bearing: yes.
    - Compare target: line ~20-21 states the rung order + "rung-2 curl_cffi gated/unbuilt".
    - Reuse rule: re-read fresh.
  - `orca-harness/pyproject.toml`
    - Role: dependency declarations. The `[impersonate] = curl_cffi>=0.15.0,<0.16` extra is **in PR #344 ONLY, NOT on main**.
    - Load-bearing: yes.
    - Compare target: `git show origin/main:orca-harness/pyproject.toml` has NO `impersonate` extra; `git show origin/claude/renovate-curl-cffi-freshness:orca-harness/pyproject.toml` has it.
    - Reuse rule: confirm which branch before relying on the extra.
- Source gaps: the YT at-pace **daily-volume ceiling** is less characterized than IG's (capture at gentle pace; lean on the recon's route-health signals).
- Strict-only blockers: the rung-2 build needs the owner's `curl_cffi`-dependency go.
- Not-proven boundaries: "not blocked != undetected" (cannot see YouTube's actual classifier); fingerprint is Chrome-class, not proven byte-identical to a live Chrome build.

## Current Task State

- Completed: **PR #342 MERGED** (squash `3ecc2ee6`) — YT recon + stealth tooling + playbook + recon card. **PR #343 MERGED** (head `28e091d8`) — stale-docstring fixes + proxy strip from the default transport + README proxy-line fix.
- Partially completed: **PR #344 OPEN** (head `a4c0fc17`, mergeable) — Renovate `curl_cffi` freshness (renovate.json + `[impersonate]` extra + `verify_fingerprint` freshness block + repo-structure.yaml declaration). Awaiting owner merge + Renovate app install.
- Broken or uncertain: none known. The rung-2 adapter is NOT built (gated). YT daily-volume ceiling uncharacterized.

## Workspace State

- This packet's lane branch: `claude/youtube-capture-lane-handoff` (off `origin/main` `b3072a0b`).
- origin/main: `b3072a0b` (fast-moving — fetch fresh).
- Open YT PR: #344 `claude/renovate-curl-cffi-freshness` @ `a4c0fc17`.
- Orphan: `claude/xenodochial-greider-ec61aa` (local + remote @ `a3576bee`) — superseded by #343 (its commits were cherry-picked into #343, now merged); **now deletable**.
- This handoff file: newly created → untracked, then committed on this lane branch (records its own dirty-state impact).
- NOTE: the sender's other worktree (`claude/ig-rung2-finding` @ `b2c3f389`, PR #346) is the SEPARATE Instagram lane — not part of this handoff.

## Changed / Inspected / Tested Files

- `orca-harness/youtube_capture/stealth_client.py`
  - Status: on main (via #342, hardened by #343).
  - Role: the single network entry point — Chrome-impersonating HTTP client (`curl_cffi` TLS/JA3 + HTTP/2 + client-hints), anonymous-only, **NO proxy**, loud non-stealth warning if it falls back to urllib.
- `orca-harness/youtube_capture/capture_youtube_v0.py` — per-video capture (embedded `ytInitialPlayerResponse` + `youtubei/v1/next` comments; `surface_type` switch for long-form/Shorts).
- `orca-harness/youtube_capture/shorts_scroll_capture_v0.py` — volume capture / load test (stops + records on first wall).
- `orca-harness/youtube_capture/enrich_ryd_v0.py` — adds a LABELED Return-YouTube-Dislike estimate (never ground truth).
- `orca-harness/youtube_capture/verify_fingerprint_v0.py` — independent TLS/JA3 check vs a neutral third-party echo; owner-run (the live JA3-echo is operator-run, not agent-run). PR #344 adds a plain-English FRESHNESS block.
- `orca-harness/youtube_capture/README.md` — orientation; post-#343 says "no proxy"; PR #344 adds a "Keeping the Chrome costume fresh" section.

## Frozen Decisions

- YT unified long-form + Shorts (one substrate). Evidence: `youtube_capture_recon_v0.md`. Consequence: one runner, `surface_type` discriminator.
- probe-then-pin / cheapest-first; no blanket stealth default; no proxy default. Evidence: owner course-corrections this lane + the ladder doc. Consequence: pin the cheapest working rung per source; proxy only at the highest rungs.
- Dislikes = RYD labeled estimate. Evidence: `enrich_ryd_v0.py`. Consequence: never a hard authenticity threshold.
- Renovate Option 1 (auto-PR + manual freshness check; no live CI gate). Evidence: PR #344. Consequence: a human runs `verify_fingerprint_v0.py` at bump-review.
- rung-2 adapter shape DECIDED (stateless, no proxy, no fallback, block_shell-wired) but build PENDING owner `curl_cffi`-dependency go. Consequence: do not build without the go.

## Mutable Questions

- The owner's `curl_cffi` optional-dependency go (gates the rung-2 build). Resolved by: an explicit owner instruction.
- Whether to re-port YouTube onto the rung-2 adapter (currently DEFERRED). Resolved by: owner decision after the adapter exists.
- The YT at-pace daily-volume ceiling. Resolved by: a bounded capture measurement, if scaling demands it.

## Superseded / Dangerous-To-Reuse Context

- **Orphan branch `claude/xenodochial-greider-ec61aa` (`a3576bee`):** superseded by #343's cherry-pick (now merged). Do NOT open a PR from it; delete it (see Next Action #5).
- **"Make rung-2 the default" / "blanket stealth default":** REJECTED — probe-then-pin / cheapest-first instead.
- **Precompact pointer `docs/hygiene/precompact_youtube_capture_stealth_2026-06-22.md`:** disposable scratch (gitignored); superseded by THIS handoff for cross-lane purposes.
- **"Stale proxy-from-env-only README line":** FIXED (merged in #343); no longer a pending item.

## Commands And Verification Evidence

- `gh -R eric-foo/orca pr view 342 --json state` → MERGED (squash `3ecc2ee6`).
- `gh -R eric-foo/orca pr view 343 --json state,headRefOid` → MERGED, head `28e091d8`.
- `gh -R eric-foo/orca pr view 344 --json state,headRefOid,mergeable` → OPEN, `a4c0fc17`, MERGEABLE.
- `git ls-tree -r --name-only origin/main -- orca-harness/source_capture/adapters/ | grep curl_cffi` → empty (rung-2 adapter absent on main).
- `git show origin/main:orca-harness/youtube_capture/README.md | grep -i proxy` → "no proxy ... separate higher rung" (confirms #343 landed).
- `verify_fingerprint_v0.py` → **owner-run** (live third-party JA3 echo; not agent-run). Prior owner run (2026-06-21) confirmed curl_cffi(chrome) JA3/JA4 distinct from stdlib urllib.

## Blockers And Risks

- rung-2 adapter build BLOCKED on the owner's `curl_cffi`-dependency go.
- PR #344's effect BLOCKED on the Renovate GitHub App install (after merge).
- Remote branch deletion BLOCKED by the pre-push guard → use `gh api` / GitHub UI (owner action).
- Risk: YT at-pace daily-volume ceiling uncharacterized → capture at gentle pace; watch the recon's route-health signals; the tooling stops + records on the first wall.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: `origin/main` head; #342/#343 MERGED, #344 OPEN; rung-2 adapter ABSENT on main; orphan SHA `a3576bee`; the 6 YT tooling files present.
- Compare targets: the `gh pr view` + `git ls-tree`/`git show` commands above.
- Sources to reread if drift detected: the recon doc, the playbook, the anti-block ladder, `pyproject.toml` (extra is branch-only).
- Load outcomes: `REUSE` (all load-bearing facts re-verified) / `PARTIAL_REUSE` / `STALE_REREAD_REQUIRED` (main moved — re-derive) / `BLOCKED_DRIFT` / `BLOCKED_MISSING_PACKET` / `BLOCKED_UNVERIFIABLE`.

## Do Not Forget

- Captured data is **gitignored — NEVER commit it.**
- This is the **YouTube lane only**; Instagram / crawling is a separate lane in its own thread.
- The rung-2 build is **gated**; capture does not need it — proceed on `stealth_client.py`.
