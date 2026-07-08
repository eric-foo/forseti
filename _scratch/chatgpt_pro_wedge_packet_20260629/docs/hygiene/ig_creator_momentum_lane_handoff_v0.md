# Handoff Packet - IG Creator-Momentum Lane

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet (durable continuation artifact; NOT validation/readiness/governance)
scope: >
  Transfers the IG creator-momentum lane to a fresh thread after the spine-first
  migration, bloat cut, ontology work, and folder restructure. This packet
  replaces the older 2026-06-15 hygiene handoff and re-anchors the lane to the
  current `orca/product/` structure.
use_when:
  - Continuing the IG creator-momentum / beauty-creator lane cold after the spine-first migration.
  - Re-establishing the creator-momentum source pack before deciding between docs stabilization, roster work, or the next bounded build.
  - Checking which old lane claims are stale after typed metric observations and the new product tree landed.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-loading.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - orca/product/spines/capture/source_families/instagram/orca_creator_momentum_pipeline_architecture_v0.md
  - orca/product/spines/capture/source_families/instagram/ig_creator_discovery_spec_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
stale_if:
  - `main` is updated past local `origin/main` or the receiver is not on the recorded HEAD/ref.
  - The creator-momentum architecture, discovery spec, roster ledger, wind-caller carve-out, `models.py`, or IG projection helper changes.
  - The remaining IG satellite producer / packet-level coverage contract lands.
  - The owner redirects the next lane from creator-momentum to controller-wide migration work.
```

## Load Contract

- packet_version: v1
- mode: max
- created_at: 2026-06-20T16:49:16+08:00
- created_by_lane: Codex current-thread handoff for the IG creator-momentum lane; provenance only, not authority.
- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- handoff_path: `docs/hygiene/ig_creator_momentum_lane_handoff_v0.md`
- expected_branch: `main`
- expected_head: `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`
- expected_remote_head_observed: `origin/main` at `5bb52bad208c618b7363a6de7a03a6c1cb5cf3dc`
- expected_dirty_state_including_handoff_file: after writing this packet, `docs/hygiene/ig_creator_momentum_lane_handoff_v0.md` is modified; pre-existing untracked items remain under `.codex/hooks/run_orca_guard.py`, `_scratch/**`, and `docs/prompts/product-planning/orca_spine_first_target_structure_controller_prompt_v0.md`.
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting. This packet is orientation, not authority.
- source_loading_mode: repo-overlay-bound.

## Routing Preflight

- smallest_complete_outcome: durable cold-reader handoff only; no moves, no structure rewrite, no commit/push.
- cynefin_route: mixed/chaotic edge because the repo shifted while this lane was paused; stabilize by rereading current sources before choosing the next creator-lane move.
- current_bottleneck: stale path/build-state claims after spine-first migration and typed metric-observation landing.
- allowed_next_move: verify source pack, then choose a narrow creator-momentum action.
- disallowed_next_move: controller-wide migration, IG lane file moves, live capture, scheduler, readiness claims, or unrelated scratch cleanup.

## Goal Handoff

- long_term_goal: Build the Orca creator-momentum product: read creator momentum across a consumer vertical, beauty first and Instagram first, using follower trajectory, reel/video view-count curves, tier band jumps, and creator roster movement as demand / wind-caller signals.
- anchor_goal: Continue the creator-momentum lane in the new spine-first structure without reviving stale `docs/product/` paths or rebuilding already-landed typed metric-observation substrate.
- success_signal: A fresh thread can re-open the current source pack, identify the remaining creator-momentum gap precisely, and choose the next owner-approved lane action without moving files, rewriting repo structure, or trusting the old 2026-06-15 packet.

## Open Decision / Fork

- decision: What should the next creator-momentum lane do after the repo restructure?
  - options:
    1. Docs stabilization first: update stale body prose in the architecture/handoff family that still says `docs/product/...` or "typed metric field missing."
    2. Bounded implementation/scoping next: wire the IG satellite producer to emit `metric_observations` plus packet-level coverage/identity/conflict metadata.
    3. Roster/discovery next: continue toward the 250 -> 500 -> 1,000 creator roster/frontier workflow.
  - already constrained / off the table: no file moves, no repo-structure rewrite, no main merge, no live IG capture, no scheduler/standing crawler, no broad IG lane migration, no rebuild of the `MetricObservation` core substrate unless drift proves it absent.
  - trade-offs: docs stabilization is lowest risk and prevents a fresh lane from acting on stale path/build claims; implementation moves product closer but must confirm current authorization; roster work aligns with the likely "1000 creator thing" but depends on current discovery/ontology posture.
  - owner of the call: owner decides the next lane; receiver should present the verified fork if not explicitly redirected.
  - recommendation: run the confirm-don't-trust load first, then do docs stabilization if stale claims remain; after that choose between IG satellite producer scoping/build and roster/frontier workflow.

## Drift Guard

- spine-first paths are current: product-owned capture files now live under `orca/product/spines/capture/...`; old `docs/product/...` body prose is historical/stale unless the moved-path index says otherwise.
- the old creator migration inventory `docs/migration/capture_spine_ig_creator_migration_inventory_v0.md` is absent on current `main`; do not make it the lane's active source.
- `MetricObservation`, `MetricPosture`, `CoverageWindow`, and `SourceCaptureSlice.metric_observations` exist in `orca-harness/source_capture/models.py`; do not tell the receiver the typed metric field is missing without re-checking.
- still not authorized by this packet: live IG capture, commercial-scale collection, scheduler/standing crawler, production store, ECR/Cleaning/Judgment binding, validation/readiness claims, or repo-structure edits.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- targets to enter the ladder:
  - `docs/workflows/data_capture_spine_consolidation_map_v0.md`
  - `orca/product/spines/capture/source_families/instagram/orca_creator_momentum_pipeline_architecture_v0.md`
  - `orca/product/spines/capture/source_families/instagram/ig_creator_discovery_spec_v0.md`
  - `orca/product/spines/capture/source_families/instagram/ig_creator_roster_frontier_ledger_spec_v0.md`
  - `docs/decisions/wind_caller_calibration_carveout_v0.md`
  - `orca-harness/source_capture/models.py`
  - `orca-harness/source_capture/ig_projection.py`
- already loaded: AGENTS, overlay README/source-of-truth/source-loading/artifact-folders/decision-routing/retrieval-metadata, repo map, Data Capture submap, old hygiene handoff, current IG architecture/discovery/carve-out/model/projection/test surfaces. Weak orientation only.
- must load first before strict or actionable work: AGENTS, overlay README, source-loading, current git status, Data Capture submap, architecture doc, wind-caller carve-out, `models.py`, and whichever target file the receiver proposes to edit.

### Earlier-decided concepts and behaviors

- creator-momentum pipeline is discover -> deep-capture -> per-call curves, IG first; verify in `orca/product/spines/capture/source_families/instagram/orca_creator_momentum_pipeline_architecture_v0.md` blob `093d185d26febb0d96cd801a21b430d530d0c29c`.
- discovery roster is beauty sub-niche + follower band and covers both established and rising creators; verify in `orca/product/spines/capture/source_families/instagram/ig_creator_discovery_spec_v0.md` blob `5c6b8f3c915793ddf7150d5470e5be1bf07514cd`.
- subject-creator roster is uncapped/all-in-vertical; <=10 is Orca's own operating/capture account ceiling, not a tracked-creator cap; verify in `docs/decisions/wind_caller_calibration_carveout_v0.md` blob `d02a284f95831934e0cb370db78c5f692d5e15bf`.
- current serious-v0 roster gates are 250 -> 500 -> 1,000; verify in `orca/product/spines/capture/source_families/instagram/ig_creator_roster_frontier_ledger_spec_v0.md` blob `9f660a8f02bbfc8081d608791ed65f392ed38c6f`.
- typed metric-observation core exists but per-platform satellite producer and packet-level coverage claim are deferred/need verification; verify in `orca-harness/source_capture/models.py` blob `121c3dcc8126467ac7f02a6d267209e948cf0083` and `orca-harness/source_capture/ig_projection.py` blob `63876d7a97a42819efcb8394bf474b24a208afb0`.

## Active Objective

Re-orient the IG creator-momentum lane on the current spine-first repo shape and pick the next narrow lane action from verified current sources. The next receiver should not assume the 2026-06-15 packet is current; it must verify the current product files and code first.

## Exact Next Authorized Action

1. Run `git status --short --branch --untracked-files=all` and compare branch/head/dirty state against this packet.
2. If the receiver needs latest remote state, update or switch to a clean current worktree before editing; local `main` was observed behind `origin/main` by 6; the selected lane-path diff in `HEAD..origin/main` only reported `docs/workflows/orca_repo_map_v0.md`.
3. Re-read the source pack named above and return a load outcome: `REUSE`, `PARTIAL_REUSE`, `STALE_REREAD_REQUIRED`, `BLOCKED_DRIFT`, `BLOCKED_MISSING_PACKET`, or `BLOCKED_UNVERIFIABLE`.
4. If continuing this lane, first resolve the fork: docs stabilization, IG satellite producer scoping/build, or roster/frontier workflow. Do not move files or rewrite repo structure.
5. If editing, use a new isolated branch/worktree as required by AGENTS; do not edit on dirty `main` unless explicitly directed.

## Authority And Source Ledger

- `AGENTS.md` - project instruction kernel; load-bearing yes; blob `8715ece8c18d14fc6b498639ea24ed8b1d8de1c2`; checked 2026-06-20.
- `.agents/workflow-overlay/README.md` - overlay entrypoint; load-bearing yes; blob `57cbc892dcd79d4d57686db465900ad042769174`.
- `.agents/workflow-overlay/source-of-truth.md` - source hierarchy and checkpoint lifecycle; load-bearing yes; blob `fd42a38eb206327ff474fa83a2a5c90165c12a59`.
- `.agents/workflow-overlay/source-loading.md` - current source-loading and capture read-pack rules; load-bearing yes; blob `17eb55585e8d26ed8bf91a0a70bca987b88ed4ce`.
- `.agents/workflow-overlay/artifact-folders.md` - current `orca/product/` placement authority; load-bearing yes; blob `e4011ed4a89a9ed95c9e62568e4e4c92634d3252`.
- `.agents/workflow-overlay/decision-routing.md` - routing messy/cross-thread work; load-bearing yes; blob `666bc1da35b9f6376d9dbabf5f7e966107dc0df0`.
- `.agents/workflow-overlay/retrieval-metadata.md` - durable artifact header contract; load-bearing yes; blob `f675c5dd9357d4c53000ff8beb040839b3e06343`.
- `docs/workflows/orca_repo_map_v0.md` - navigation and Wave E product path shape; load-bearing yes; blob `efb1b91e01e563257da6d3618a60e9f4eec6237e`.
- `docs/workflows/data_capture_spine_consolidation_map_v0.md` - Capture/Armory front door and IG projection helper route; load-bearing yes; blob `495f652a0965892e6e8053351261084c3148f860`.
- `orca/product/spines/capture/source_families/instagram/orca_creator_momentum_pipeline_architecture_v0.md` - proposed creator architecture; load-bearing yes; blob `093d185d26febb0d96cd801a21b430d530d0c29c`.
- `orca/product/spines/capture/source_families/instagram/ig_creator_discovery_spec_v0.md` - discovery spec; load-bearing yes; blob `5c6b8f3c915793ddf7150d5470e5be1bf07514cd`.
- `orca/product/spines/capture/source_families/instagram/ig_creator_roster_frontier_ledger_spec_v0.md` - roster/frontier gates; load-bearing yes; blob `9f660a8f02bbfc8081d608791ed65f392ed38c6f`.
- `docs/decisions/wind_caller_calibration_carveout_v0.md` - owner-signed cap/posture authority; load-bearing yes; blob `d02a284f95831934e0cb370db78c5f692d5e15bf`.
- `orca-harness/source_capture/models.py` - current packet model with metric observations; load-bearing yes; blob `121c3dcc8126467ac7f02a6d267209e948cf0083`.
- `orca-harness/source_capture/ig_projection.py` - IG creator-momentum view-only projection; load-bearing yes for projection-current claims; blob `63876d7a97a42819efcb8394bf474b24a208afb0`.
- `docs/research/creator_momentum_data_landscape_v0.md` - optional data-landscape context; load-bearing no for immediate next action; blob `746607b7a5e4f163a3cb012e442311afbc90092e`.

## Current Task State

- Completed: refreshed the stable hygiene handoff in place for the current spine-first repo shape; confirmed old creator migration inventory is absent on current local `main`; confirmed current product files and typed metric substrate exist.
- Partially completed: the architecture doc still has stale body prose under "Placement" naming old `docs/product/...` homes; it also still implies the capture-shape contract is entirely next-build even though the core typed metric substrate exists.
- Broken or uncertain: local `main` behind `origin/main` by 3; untracked scratch/controller files are present; next lane choice is owner-directed.

## Workspace State

- Branch: `main`
- Head: `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`
- Remote ref observed: `origin/main` at `76c39f726f137dd1a4dc43b62049b4273515b308`
- Dirty/untracked before handoff: `## main...origin/main [behind 3]`; untracked `.codex/hooks/run_orca_guard.py`; untracked `_scratch/**`; untracked `docs/prompts/product-planning/orca_spine_first_target_structure_controller_prompt_v0.md`; status emitted warning for `orca-harness/.pytest_tmp/` permission denied.
- Dirty/untracked after writing this packet: expected `M docs/hygiene/ig_creator_momentum_lane_handoff_v0.md` plus the same pre-existing untracked items; receiver must re-run status for exact state.
- Old worktree `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\commission-spine-structure` was checked and absent.

## Changed / Inspected / Tested Files

- `docs/hygiene/ig_creator_momentum_lane_handoff_v0.md` - overwritten by this packet; stable cold-lane checkpoint.
- `orca/product/spines/capture/source_families/instagram/orca_creator_momentum_pipeline_architecture_v0.md` - inspected; proposed architecture; body placement prose still stale.
- `orca/product/spines/capture/source_families/instagram/ig_creator_discovery_spec_v0.md` - inspected; discovery spec with subject roster uncapped and active/passive posture resolved.
- `orca/product/spines/capture/source_families/instagram/ig_creator_roster_frontier_ledger_spec_v0.md` - inspected/search-read; 250 -> 500 -> 1,000 gates.
- `orca-harness/source_capture/models.py` - inspected targeted lines 128-227; typed metric observation exists.
- `orca-harness/tests/unit/test_source_capture_metric_observation.py` - inspected targeted lines 1-184; tests encode observed-zero vs absence invariant and back-compat default empty list.
- `docs/decisions/wind_caller_calibration_carveout_v0.md` - inspected; cap and posture authority.
- Tests: not run in this handoff turn.

## Frozen Decisions

- Checkpoint packets are non-authoritative, single-consumption lane-state artifacts refreshed in place.
- Product-owned capture files now live under `orca/product/`.
- Wind-caller cap referent: <=10 counts Orca operating/capture accounts, not subject creators.
- Typed metric observation core substrate exists.

## Mutable Questions

- Should the next lane fix stale architecture body prose first? Owner or receiver should decide after load.
- Should next work be IG satellite producer implementation/scoping? Requires explicit bounded authorization.
- Should next work be roster/frontier toward 1,000 creators? Depends on owner direction and staged gate scope.
- Should local `main` be updated before editing? Receiver should decide; current local main is behind remote.

## Superseded / Dangerous-To-Reuse Context

- Old handoff claim: `models.py` has no typed metric field. Stale; current model has metric observations.
- Old placement/body prose: IG capture satellite -> `docs/product/source_capture_toolbox/`; derivation spec -> `docs/product/data_capture_spine/`. Stale after spine-first migration; current product files are under `orca/product/`.
- Old migration inventory `docs/migration/capture_spine_ig_creator_migration_inventory_v0.md`. Absent on current local `main`; use current product files and maps instead.
- Old architecture assumption: flat file/no engine justified by a small tracked roster. Re-check against current roster gates and all-in-vertical posture before using.

## Commands And Verification Evidence

- `git status --short --branch --untracked-files=all`: observed local main behind 3, untracked scratch/controller files, and `.pytest_tmp` permission warning.
- `git rev-parse --abbrev-ref HEAD; git rev-parse HEAD; git rev-parse origin/main`: observed `main`, `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`, `76c39f726f137dd1a4dc43b62049b4273515b308`.
- `git diff --name-status HEAD..origin/main -- <selected lane paths>`: no selected lane-path diffs printed.
- `git diff --name-status HEAD..origin/main --`: observed remote-only changes to `docs/hygiene/queue.md` and `docs/workflows/orca_repo_map_v0.md`.
- `rg --files | rg -i "capture.*ig.*creator|ig_creator.*migration|creator_momentum|ig_creator|creator_roster|creator_discovery|wind_caller|spine_first.*creator"`: found current product files and old hygiene handoff; did not find old creator migration inventory.
- Validation: no tests or strict validation gates were run in this handoff turn.

## Blockers And Risks

- local `main` is behind `origin/main` by 3; use a fresh worktree/current ref before source-changing work if strict freshness matters.
- untracked scratch/controller files are present; leave them uncommitted unless a later lane owns them.
- architecture body has stale placement and next-object language; docs stabilization may be the lowest-risk first action.
- implementation authorization is not granted by this packet.

## Confirm-Don't-Trust Load Checklist

- Re-verify branch/head/dirty state against `main` at `c449b0f97906b4be1ccfee7ef734ba54f5b55df1` and `origin/main` at `76c39f726f137dd1a4dc43b62049b4273515b308`.
- Re-verify product path structure against artifact-folders blob `e4011ed4a89a9ed95c9e62568e4e4c92634d3252` and repo map blob `efb1b91e01e563257da6d3618a60e9f4eec6237e`.
- Re-verify typed metric substrate against `models.py` blob `121c3dcc8126467ac7f02a6d267209e948cf0083` and tests blob `5f64c6742021b86bd926c7e4087295b82e224819`.
- Re-verify lane source pack against architecture/discovery/roster/carve-out blobs recorded above.
- Return one load outcome: `REUSE`, `PARTIAL_REUSE`, `STALE_REREAD_REQUIRED`, `BLOCKED_DRIFT`, `BLOCKED_MISSING_PACKET`, or `BLOCKED_UNVERIFIABLE`.

## Do Not Forget

The next receiver should not continue from the old 2026-06-15 assumptions. The current repo already landed the core typed metric-observation substrate and moved product files under `orca/product/`; remaining work starts from that reality.
