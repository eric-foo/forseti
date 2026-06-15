# Handoff Packet — Data Capture Spine (Whole-Spine State + Coordination)

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet (whole Data Capture Spine state + coordination; continuation artifact, not readiness evidence)
scope: Transfer Chief-Architect coordination of the WHOLE Data Capture Spine to a fresh CA thread — anchored on the existing consolidation submap (navigation), adding current live state + next moves + invariants.
authority_boundary: retrieval_only
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-15
- created_by_lane: capture-spine Chief-Architect coordinating thread (provenance only; not authority)
- workspace: C:\Users\vmon7\Desktop\projects\orca
- handoff_path: docs/prompts/handoffs/capture_spine_state_handoff_v0.md
- expected_branch: fresh worktree/branch off `origin/main` for any repo-changing follow-up (NOT the hot home branch `ecr-sp3-timing-deriver-slice1`)
- expected_head: `origin/main` was `421b4a11` at handoff; it moves fast (owner merges aggressively) — re-fetch.
- expected_dirty_state_including_handoff_file: this packet is newly created under tracked `docs/prompts/handoffs/` → untracked until committed on its lane.
- load_rule: **confirm-don't-trust** — re-verify every load-bearing fact (the consolidation map's currency, each lane's PR/branch state, main HEAD) before acting. The owner merges and renames aggressively; this map and several lane snapshots are dated and may lag live state.

## Goal Handoff

- long_term_goal: Orca's Data Capture Spine reliably captures source-faithful, commissioned, gate-honest evidence — **observed facts and their limits, never weights/scores/verdicts (INV-1)** — that downstream ECR / Cleaning / Judgment and the demand-read consume.
- anchor_goal: **pick up Chief-Architect coordination of the WHOLE Data Capture Spine** — drive its in-flight lanes to their next state — *without re-deriving the spine*: the consolidation submap (below) is the navigation authority; this packet adds current state + next moves.
- success_signal: a fresh CA can, from this packet **plus the consolidation map**, see each spine lane's current state, the spine-wide invariants, and the next move per lane, and act on any one lane under confirm-don't-trust without this thread.

## Open Decision / Fork

- decision: **which spine lane to advance next** (the spine has several in-flight; pick by owner priority).
  - options: (A) **demand-durability indicators** — dispatch the *authorized* build phase (step-2 writer → step-3 scheduler; handoffs #114/#115; sub-coordination #120); (B) **#94 publisher-history PH fix** — long-open; closes the PH-01/02 fake-success holes from the #89-merged-ahead saga; (C) **#112 standing-capture-corpus-intake contract**; (D) the map's other lanes (Reddit Candidate URL Intake / Graph Frontier, anti-block ladder, CloakBrowser, LinkedIn, source-quality) — each has an owner doc in the map.
  - already constrained / off the table: build authorization is **bounded to demand-durability steps 2+3 only** — other lanes' builds need their own authorization; landing to `main` is owner-gated; the source-access boundary + commissioning gate bind every lane.
  - trade-offs: (A) has authorization + momentum; (B) is hygiene-critical (PH holes have lingered since the start of this arc); (C)/(D) are owner-priority calls.
  - owner of the call: the owner + the fresh CA.
  - recommendation: **(A) dispatch the demand-durability build** (authorized, gated, ready) **and resolve (B) #94** (long-open correctness debt). Triage (C)/(D) by owner priority via the map.

## Drift Guard

- **INV-1** (spine-wide): capture records observed facts + limits, never weights, scores, ranks, or verdicts. Bounds every lane.
- **Commissioned capture only** (obligation contract Ob.1): captures are bounded + tied to a Decision Frame. **No broad/standing/opportunistic crawling**, no site-wide walking, no production monitoring.
- **No-gate-defeat**: anti-bot (honest/anti-blocking UA, CloakBrowser per the accepted source-access posture) is OK; **STOP at any auth / CAPTCHA / Cloudflare *challenge***, record it, escalate honestly via the cost-ordered anti-block ladder (block_shell honest-success guard). Never defeat a gate.
- **Source-access boundary**: discoverable-or-entitled + disclosable standard; CloakBrowser is the selected primary anti-blocking backend; hard stops per `data_capture_source_access_boundary_decision_v0.md`. Build authority is bounded per `data_capture_spine_source_access_tooling_build_authorization_v0.md`.
- **Additive-optional schema** (the demand-durability hardening): durability fields default unset, no `SOURCE_CAPTURE_MANIFEST_VERSION` bump; never break packet back-compat.
- **Series-diff (Element 3) deferred**; **bounded authorization = demand-durability steps 2+3 only** (NOT a spine-wide build grant).
- **The consolidation map is navigation, not authority** — on any conflict the pointed-to owner doc wins; and the map is dated (~2026-06-05, predates the demand-durability work) so **re-verify lane state before acting**.
- **Confirm-don't-trust / cross-lane drift**: the owner merges + renames aggressively. This spine was bitten twice — **#89/#93** (merged ahead of an in-flight fix) and **#106/#116** (files renamed mid-flow → dangling refs). Re-verify PR states + current filenames before any actionable claim.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (read `.agents/workflow-overlay/README.md` first, per AGENTS.md).
- **primary entrypoint** (load this first): `docs/workflows/data_capture_spine_consolidation_map_v0.md` — the spine's repo submap; routes to every lane's owner doc + a "Fast Route" table + a (dated) reality snapshot. Treat as navigation, re-verify currency.
- other targets to enter the ladder: `docs/product/source_capture_toolbox/README.md` (Source Capture Armory index); `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md` (obligations + forbidden outputs + Ob.17); `docs/product/data_capture_spine/data_capture_source_access_boundary_decision_v0.md` + `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md` (access boundary + build authority); the demand-durability artifacts (below); `orca-harness/source_capture/` + `orca-harness/runners/` + `orca-harness/capture_spine/` (implemented adapters/runners — check code, docs may lead runners).
- already loaded (weak orientation, freshness-marked; not authority): this packet's state claims (sender verified at `origin/main 421b4a11`).
- must load first: the consolidation map, before coordinating any lane.
- load rule: receiver re-runs progressive source loading per overlay; the packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- **Spine structure + accepted architecture** (operating-model v2, source-access boundary, build authority, Candidate URL Intake / Graph Frontier / LinkedIn lane architectures, anti-block ladder, packet lifecycle): all indexed by the consolidation map. Decided in: the per-area owner docs the map lists. Verify: open the map's "Areas" + the owner doc per lane. Verify before: coordinating that lane.
- **Demand-durability indicators rollout** (the most recent capture-spine work; this map predates it): designed → live-pilot-proven → distilled → hardened → handed-off → authorized, **all merged**. Detail: pilot `docs/product/data_capture_spine/demand_durability_capture_pilot_v0.md`; build handoffs `docs/prompts/handoffs/demand_durability_series_writer_step2_handoff_v0.md` (+ `..._cadence_runner_step3_...`); sub-coordination `docs/prompts/handoffs/demand_durability_capture_spine_ca_coordination_handoff_v0.md` (PR #120); distill A1c `docs/decisions/distillation_binding_data_capture_v0.md`; schema `orca-harness/source_capture/models.py` + Ob.17. Verify: `git ls-tree origin/main docs/product/data_capture_spine/ | grep demand_durability_indicator`.
- **INV-1, commissioning (Ob.1), source-access boundary, no-gate-defeat**: the spine-wide invariants. Decided in: the obligation contract + the source-access boundary decision + the buyer-proof packet (INV-1). Verify before: any lane action.

## Active Objective

Coordinate the whole Data Capture Spine — advance its in-flight lanes (demand-durability build phase; #94 PH fix; #112 standing-capture; and the map's other lanes by owner priority) to their next state — anchored on the consolidation map, under the spine-wide invariants, from a green `main`.

## Exact Next Authorized Action

1. **Confirm-don't-trust**: `git fetch origin main`; open the consolidation map; re-verify `main` green (`check_map_links --strict` OK) and the open capture lanes' states (#94, #112, #120, plus any new).
2. Pick the next lane to advance (Open Decision; recommend demand-durability build + #94).
3. **Demand-durability**: dispatch the step-2 writer build (`demand_durability_series_writer_step2_handoff_v0.md`, carries bounded auth) → step-3 (`..._cadence_runner_step3_...`) → first real commissioned series.
4. **#94 PH fix**: re-verify state; drive to merge (closes the PH-01/02 holes).
5. **Other lanes**: route via the consolidation map's owner doc per lane; re-verify state (map is dated). Each lane's build needs its own authorization.

This coordinating thread dispatches + adjudicates; it does not itself build.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` + `.agents/workflow-overlay/` (read overlay `README.md` first).
- Overlay authority: source-loading; dev-workflow / per-lane PR; safety / no-gate-defeat; delegated-review-patch + review-lanes (for review steps).
- User constraints: token-conscious; wants real steps; confirm-don't-trust; owner merges/renames fast; demand-durability build authorized (steps 2+3); series-diff deferred.
- Source-read ledger (all on `origin/main 421b4a11`):
  - `docs/workflows/data_capture_spine_consolidation_map_v0.md` — Role: **THE spine navigation entry** (routes to every lane owner doc). Load-bearing: **yes**. Compare: `reread-required` (verify currency; dated ~2026-06-05). Reuse: navigation, not authority.
  - `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md` — Role: obligations + forbidden outputs + Ob.17. Load-bearing: **yes**. Compare: `reread-required`.
  - `docs/product/data_capture_spine/data_capture_source_access_boundary_decision_v0.md` + `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md` — Role: access boundary + bounded build authority (CloakBrowser primary). Load-bearing: **yes**. Compare: `reread-required`.
  - demand-durability artifacts (pilot, build handoffs, #120, distill binding, models.py) — Role: the in-flight demand-durability lane. Load-bearing: **yes** for that lane. Compare: `reread-required`.
  - open PRs **#94** (publisher-history PH fix) + **#112** (standing-capture intake) — Role: in-flight capture lanes. Load-bearing: **yes**. Compare: `gh pr view` (re-verify state).
  - `docs/product/source_capture_toolbox/README.md` — Role: Armory component index/gaps. Load-bearing: no (orientation). Compare: `reread-required`.
- Source gaps: per-lane live state beyond demand-durability is map-snapshot-dated — re-verify before acting.
- Strict-only blockers: none on `main` (green); each non-demand-durability build needs its own bounded authorization.
- Not-proven boundaries: only the demand-durability lane's current state was freshly verified this thread; other lanes are carried from the (dated) map + the open-PR list — re-verify.

## Current Task State

- Completed / merged: the **demand-durability indicators rollout** (spec → pilot → distill A1c → hardening Elements 1/2/4 + Ob.17 → build handoffs #114/#115 → stale-ref fixes #116/#117); the spine's accepted architecture + consolidation map + Armory + anti-block rung-1 + CloakBrowser anonymous v0 + Reddit Candidate URL Intake / Graph Frontier local support (per the map — re-verify dates/merge-state).
- Partially completed: demand-durability **build phase** (steps 2→3 authorized, unbuilt); **#94** PH fix (open); **#112** standing-capture intake (open); the map's other lanes at various accepted-but-unbuilt states.
- Broken or uncertain: the consolidation map is dated ~2026-06-05 (predates demand-durability; the anti-block rung-1 was on `feat/anti-block-http-ladder` "confirm merge state") → **re-verify per lane**; #94's PH holes lingered open since early in this arc.

## Workspace State

- Branch: receiver creates a fresh worktree/branch off `origin/main` for any repo-changing follow-up.
- Head: `origin/main 421b4a11` at handoff (moves; re-fetch).
- Dirty/untracked before handoff: home thread (`ecr-sp3-timing-deriver-slice1`) carries unrelated untracked files; do not work there. Many stale worktrees exist under `.claude/worktrees/` + `orca-worktrees/` (owner hygiene).
- Dirty/untracked after writing this handoff file: + this file (untracked under `docs/prompts/handoffs/` until committed on its lane).
- Target files/artifacts: coordination only here; lane work happens in fresh authorized lanes.

## Frozen Decisions

- The spine's accepted architecture (operating-model v2, source-access boundary, build authority, lane architectures) — owner-accepted per the map's owner docs. Consequence: coordinate within it; don't re-litigate.
- Demand-durability hardening additive-optional + Ob.17; series-diff Element 3 deferred; bounded auth = steps 2+3. Consequence: that lane's build is gated + ready.
- INV-1 + commissioning (Ob.1) + source-access boundary + no-gate-defeat. Consequence: spine-wide invariants, non-negotiable.

## Mutable Questions

- Which lane to advance next (Open Decision).
- #94 / #112 disposition + the map's other lanes' priority.
- #120's fate — it is the **narrower demand-durability sub-coordination handoff** (this whole-spine handoff supersedes its scope); keep it as the demand-durability detail, or close/fold it. (Owner's call; recommend close to avoid two coordination handoffs, since this packet + #114/#115 + the pilot spec cover the demand-durability lane.)
- Whether to refresh the consolidation map itself (it predates demand-durability + several lanes).

## Superseded / Dangerous-To-Reuse Context

- **The map's "Current Reality Snapshot"** is dated ~2026-06-05 — re-verify each lane's live state (e.g., "confirm merge state in git" for the anti-block branch). Don't treat the snapshot as current.
- **`demand_proxy_*` filenames** — renamed → `demand_durability_indicator_*` (#106). Use the new names.
- **PR #120** — the narrower demand-durability-rollout coordination handoff (created earlier this thread as a scope misread of "capture spine"); this whole-spine handoff is the broader, intended one. #120 stands as the demand-durability detail unless the owner closes it.

## Commands And Verification Evidence

- Orient + verify:
  ```bash
  git fetch origin main && git rev-parse --short origin/main
  # open docs/workflows/data_capture_spine_consolidation_map_v0.md  (navigation)
  gh pr list --state open --json number,headRefName   # re-confirm open capture lanes (#94, #112, ...)
  ```
  Result at handoff: `origin/main 421b4a11`; open capture lanes #94, #112, #120; main green (`check_map_links --strict: OK` verified earlier this thread).
- Offline suite (the green gate for any build):
  ```bash
  cd orca-harness && .venv/Scripts/python.exe -m pytest -q
  ```
  Baseline at the demand-durability hardening: 861 passed, 2 skipped.

## Blockers And Risks

- Blocker: none on `main` (green). Non-demand-durability lane builds need their own bounded authorization.
- Risk: acting on the dated consolidation snapshot without re-verifying a lane's live state. Mitigation: re-verify per lane (confirm-don't-trust).
- Risk: cross-lane drift (owner merges/renames fast) — the #89/#93 + #106/#116 lessons.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: (1) the consolidation map is current-enough for the target lane (re-verify that lane's owner doc + code); (2) open lanes #94/#112/#120 states; (3) `origin/main` HEAD (≥ `421b4a11`) + main green; (4) the spine-wide invariants still hold; (5) for demand-durability, the bounded build authorization in #114/#115.
- Load outcomes: `REUSE` after re-verify; `STALE_REREAD_REQUIRED` if `main` moved or a lane's state drifted (expected — refresh + re-read the owner doc); `BLOCKED_DRIFT` if a claimed-merged item isn't, or main is red.
- Reread on drift: the consolidation map + the target lane's owner doc + `git`/`gh` state.

## Do Not Forget

- **The consolidation map (`docs/workflows/data_capture_spine_consolidation_map_v0.md`) is THE navigation entry** — don't re-derive the spine; route through it, and re-verify its dated snapshot per lane.
- **Owner merges/renames aggressively** — re-verify PR states + current filenames before every actionable claim (#89/#93 + #106/#116 lessons).
- **Spine-wide invariants are non-negotiable**: INV-1, commissioned-only (Ob.1), no-gate-defeat, the source-access boundary. Build authorization is **bounded** (demand-durability steps 2+3 only — not spine-wide).
