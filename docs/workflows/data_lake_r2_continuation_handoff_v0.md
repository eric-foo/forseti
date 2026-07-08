# Handoff Packet

## Load Contract

- packet_version: workflow-handoff max v0
- mode: max
- created_at: 2026-06-20 16:48:32 +08:00
- created_by_lane: Codex data-lake structure adjudication lane; provenance only, not authority.
- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- handoff_path: `C:\Users\vmon7\Desktop\projects\orca\docs\workflows\data_lake_r2_continuation_handoff_v0.md`
- expected_branch: `main`
- expected_head: `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`
- expected_remote_head_observed: `origin/main` at `5bb52bad208c618b7363a6de7a03a6c1cb5cf3dc`
- expected_dirty_state_including_handoff_file: post-write verification observed local `main` behind `origin/main` by 6 commits; dirty state included `M docs/hygiene/ig_creator_momentum_lane_handoff_v0.md`; untracked files existed under `.codex/hooks/`, `_scratch/`, `docs/hygiene/cleaning_spine_lane_handoff_v0.md`, `docs/hygiene/commission_signal_board_lane_handoff_v0.md`, `docs/prompts/product-planning/orca_spine_first_target_structure_controller_prompt_v0.md`, and this handoff file. The hygiene handoff changes appeared during this turn and were not created by this lane.
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: Keep Orca's data-lake foundation boring, durable, and IG-agnostic: it stores captured data and keyed state facts while Capture, Projection, ECR, Signal Statement, Cleaning, Judgment, and future consumers remain separate lanes.
- anchor_goal: Continue the Data Lake R2 continuation lane from current `main` after spine-first migration, bloat cuts, ontology tagging, and Data Lake R2 landing; decide and patch only the remaining deferred Data Lake placement issue if the current user authorizes it.
- success_signal: The receiver re-verifies current repo state, keeps Data Lake as a shared-foundation spine, does not reopen physical backend selection or smart-lake orchestration, and either records the two deferred planning docs as intentionally staying in `docs/migration/` or applies an owner-authorized placement patch with checks.

## Open Decision / Fork

- decision:
  - options:
    - Keep `docs/migration/data_lake_spine_first_migration_plan_v0.md` and `docs/migration/data_lake_spine_first_migration_inventory_v0.md` in `docs/migration/` as repo-structure migration records.
    - Move those two records into `orca/product/spines/data_lake/migrations/` as founding Data Lake spine history.
  - already constrained / off the table:
    - Do not move the Data Lake contracts or mechanics map again without a later accepted decision.
    - Do not put repo-controller logs into Data Lake product authority.
    - Do not use or recreate `orca/product/shared/data_lake_mechanics/` as a live target; it is retired by Data Lake R2.
  - trade-offs:
    - `docs/migration/` matches the overlay rule for migration/import planning records and keeps repo logs global.
    - `data_lake/migrations/` preserves a literal founding history inside the spine but conflicts with the bound grammar that says it is for lake-specific schema/data migration plans, not repo migration logs.
  - owner of the call: current user / owner.
  - recommendation and why:
    - Keep both #239 planning docs in `docs/migration/`. Current Data Lake README and binding say `data_lake/migrations/` is for lake-specific schema/data migration plans, not repo migration logs. The R2 harvest script and moved-path index already live under `docs/migration/repo_structure_data_lake_r2_v0/`, matching the same class.

## Drift Guard

- invariant, non-goal, or scope boundary:
  - Data Lake is a shared-foundation spine at `orca/product/spines/data_lake/`, not `orca/product/shared/data_lake_mechanics/`.
  - why it matters: Data Lake owns hard cross-layer storage contracts and needs an owner workspace.
  - what violating it would break: It would hide the contract owner and reintroduce the retired shared mechanics folder.
- invariant, non-goal, or scope boundary:
  - The lake stores and exposes keyed state; it does not call, orchestrate, clean, project, derive, judge, queue, retry, or schedule lanes.
  - why it matters: This keeps Capture, Projection, ECR, Signal Statement, Cleaning, and Judgment boundaries intact.
  - what violating it would break: It would turn the lake into a smart orchestrator and collapse ownership boundaries.
- invariant, non-goal, or scope boundary:
  - Do not choose a physical backend, storage engine, queue, database, warehouse, object store, or lakehouse technology in this lane.
  - why it matters: The current artifacts are storage contracts and repo-structure placement, not physicalization.
  - what violating it would break: It would create premature implementation lock-in.
- invariant, non-goal, or scope boundary:
  - Do not treat R2 placement/link hygiene as validation, readiness, product proof, runtime authorization, or proof that the data lake is built.
  - why it matters: The moved contracts and mechanics are source-backed doctrine; they are not implementation evidence.
  - what violating it would break: It would overclaim architecture docs as runtime success.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- targets to enter the ladder:
  - `AGENTS.md`
  - `.agents/workflow-overlay/README.md`
  - `.agents/workflow-overlay/source-loading.md`
  - `.agents/workflow-overlay/artifact-folders.md`
  - `orca/product/spines/data_lake/README.md`
  - `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md`
  - `docs/migration/repo_structure_data_lake_r2_v0/moved_paths_index.md`
  - `docs/migration/data_lake_spine_first_migration_plan_v0.md`
  - `docs/migration/data_lake_spine_first_migration_inventory_v0.md`
  - `docs/workflows/orca_repo_map_v0.md`
- already loaded (weak orientation, freshness-marked; not authority):
  - Handoff skill source `C:\Users\vmon7\.codex\skills\workflow-handoff\SKILL.md` loaded fully 2026-06-20.
  - Overlay README, decision routing, artifact folders, source loading, docs structure, Data Lake README, promotion binding, R2 moved-path index, and #239 Data Lake plan/inventory read 2026-06-20 from local `main` at `c449b0f9`.
- must load first (before strict or actionable steps):
  - Re-run `git status --short --branch`, `git rev-parse HEAD`, and compare `origin/main`.
  - Re-read `orca/product/spines/data_lake/README.md`, `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md`, and `.agents/workflow-overlay/artifact-folders.md` because the repo is moving quickly.
- load rule: receiver re-runs progressive source loading per overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- decision, framing, profile, or convention: Data Lake is an accepted `shared_foundation` spine under `orca/product/spines/data_lake/`.
  - decided in: `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md`
  - compare target: `reread-required`; file was read at HEAD `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`.
  - verify before: moving, patching, or making authority claims about Data Lake placement.
- decision, framing, profile, or convention: Data Lake R2 landed the three contracts into `authority/` and canonical mechanics map into `workflows/`; `shared/data_lake_mechanics/` is retired.
  - decided in: `.agents/workflow-overlay/artifact-folders.md` Data Lake R2 receipt and `docs/migration/repo_structure_data_lake_r2_v0/moved_paths_index.md`
  - compare target: `git ls-tree HEAD` showed tree ids `4123f21260f2b576415063145a2e1e74b3a692b3` for `orca/product/spines/data_lake/authority` and `806c082a2643156e50e73245554cf4e8f7e43453` for `orca/product/spines/data_lake/workflows`.
  - verify before: relying on R2 completion or old-path resolution.
- decision, framing, profile, or convention: Data Lake `migrations/` is for lake-specific schema/data migration plans, not repo migration logs.
  - decided in: `orca/product/spines/data_lake/README.md` and `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md`
  - compare target: `reread-required`; the exact wording was present at read time in the README subfolder grammar and binding bound subfolder grammar.
  - verify before: deciding the two #239 planning docs' final location.
- decision, framing, profile, or convention: `docs/migration/` is the accepted home for migration and import queue/planning records.
  - decided in: `.agents/workflow-overlay/artifact-folders.md` and `docs/STRUCTURE.md`
  - compare target: `reread-required`; both files were read at HEAD `c449b0f9`.
  - verify before: creating or moving migration records.

## Active Objective

Prepare a fresh thread to continue this lane after repo-wide structure migration and Data Lake R2 convergence. The receiver's first substantive task is to verify current state, then resolve or apply the remaining placement decision for the two #239 Data Lake migration planning docs without reopening the landed Data Lake contracts or mechanics map.

## Exact Next Authorized Action

1. In the new thread, re-run the confirm-don't-trust load checklist below against current `main` and `origin/main`.
2. Ask or confirm whether the current user accepts the recommendation: keep `data_lake_spine_first_migration_plan_v0.md` and `data_lake_spine_first_migration_inventory_v0.md` in `docs/migration/`.
3. If accepted and patching is authorized in that turn, patch only the surfaces that still say the two planning docs are deferred pending placement; do not move the docs unless the owner explicitly chooses that.
4. Run relevant doc checks after any patch: at minimum `git diff --check`; run map/header/placement checks only if touched files require them, and report exact observed output.

## Authority And Source Ledger

- Repository instructions:
  - `AGENTS.md` was supplied in the current task context. Load-bearing: yes. Compare target: reread from workspace before strict/actionable work. Last checked: supplied context 2026-06-20. Reuse rule: orientation only until reread.
- Overlay or equivalent authority:
  - `.agents/workflow-overlay/README.md`
    - Role: overlay entrypoint and Orca authority routing.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: 2026-06-20.
    - Reuse rule: verify before any patch or claim.
  - `.agents/workflow-overlay/artifact-folders.md`
    - Role: accepted artifact folders and Data Lake R2 direction-change receipt.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: 2026-06-20.
    - Reuse rule: verify before placement decisions.
  - `.agents/workflow-overlay/source-loading.md`
    - Role: source-loading and handoff source-pack policy.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: 2026-06-20.
    - Reuse rule: verify before strict/actionable source-loading claims.
- User constraints:
  - Continue the Data Lake lane in a new thread; repo ground shifted substantially; use `workflow-handoff`.
  - Do not reopen physical backend choice, smart-lake orchestration, or the old full architecture debate unless current user redirects.
- Source-read ledger:
  - `orca/product/spines/data_lake/README.md`
    - Role: current Data Lake spine front door.
    - Load-bearing: yes.
    - Compare target: reread-required; observed at HEAD `c449b0f9`.
    - Last checked: 2026-06-20.
    - Reuse rule: verify before any Data Lake placement claim.
  - `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md`
    - Role: binding for Data Lake shared-foundation spine and subfolder grammar.
    - Load-bearing: yes.
    - Compare target: reread-required; observed at HEAD `c449b0f9`.
    - Last checked: 2026-06-20.
    - Reuse rule: verify before strict authority claims.
  - `docs/migration/repo_structure_data_lake_r2_v0/moved_paths_index.md`
    - Role: old-to-new path index for R2 convergence.
    - Load-bearing: yes.
    - Compare target: reread-required; observed at HEAD `c449b0f9`.
    - Last checked: 2026-06-20.
    - Reuse rule: verify before old-path resolution or stale-reference claims.
  - `docs/migration/data_lake_spine_first_migration_plan_v0.md`
    - Role: #239 Data Lake planning doc; current deferred placement target.
    - Load-bearing: yes.
    - Compare target: blob `b6528d4e97173d7c3d4badf0ecfe80739bd0953a` from `git ls-tree HEAD`.
    - Last checked: 2026-06-20.
    - Reuse rule: verify before moving, retaining, or editing.
  - `docs/migration/data_lake_spine_first_migration_inventory_v0.md`
    - Role: #239 Data Lake companion inventory; current deferred placement target.
    - Load-bearing: yes.
    - Compare target: blob `8487bf4014467e2b6e7f2f804e4f9aa6cac1a853` from `git ls-tree HEAD`.
    - Last checked: 2026-06-20.
    - Reuse rule: verify before moving, retaining, or editing.
  - `docs/workflows/orca_repo_map_v0.md`
    - Role: repo navigation map; confirms Data Lake spine entries.
    - Load-bearing: no for the placement decision, yes if map is patched.
    - Compare target: reread-required.
    - Last checked: targeted `rg` 2026-06-20.
    - Reuse rule: reread touched sections before editing.
- Source gaps:
  - Local `main` is behind `origin/main` by 6 commits; receiver must compare current refs before acting.
  - `git status --porcelain=v1 -uall` reported many `_scratch/` untracked files and a warning opening `orca-harness/.pytest_tmp/`.
- Strict-only blockers:
  - Do not claim repo clean, validation, readiness, or migration completion; current dirty state and behind status block such claims without fresh reconciliation.
- Not-proven boundaries:
  - No runtime Data Lake implementation, physical storage, backend, queue, harness move, or test move is proven or authorized by this handoff.

## Current Task State

- Completed:
  - Data Lake spine is live as a shared-foundation spine in current local sources.
  - Data Lake R2 moved the 3 contracts into `orca/product/spines/data_lake/authority/`.
  - Data Lake R2 moved the canonical mechanics map into `orca/product/spines/data_lake/workflows/`.
  - `orca/product/shared/data_lake_mechanics/` is retired by current R2 sources.
  - R2 moved-path index exists under `docs/migration/repo_structure_data_lake_r2_v0/`.
- Partially completed:
  - The two #239 Data Lake migration plan/inventory docs remain in `docs/migration/` but current source text still marks placement as deferred pending decision.
  - The sender recommended keeping them in `docs/migration/` as repo logs; verify whether the current user accepts that recommendation in the new thread.
- Broken or uncertain:
  - Local `main` is behind `origin/main` by 3 commits.
  - Worktree has untracked scratch and prompt files unrelated to this handoff.
  - `check_placement.py --check` timed out in this run after emitting known root-placement/freshness/legacy noise; do not report it as passed.

## Workspace State

- Branch: `main`
- Head: `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`
- Dirty or untracked state before handoff:
  - `?? .codex/hooks/run_orca_guard.py`
  - many untracked files under `_scratch/`, including ChatGPT Pro source packs
  - `?? docs/prompts/product-planning/orca_spine_first_target_structure_controller_prompt_v0.md`
  - status warning: could not open `orca-harness/.pytest_tmp/` due permission denied
- Dirty or untracked state after writing the handoff file:
  - same as above plus `?? docs/workflows/data_lake_r2_continuation_handoff_v0.md`
  - post-write verification also observed `M docs/hygiene/ig_creator_momentum_lane_handoff_v0.md`, `?? docs/hygiene/cleaning_spine_lane_handoff_v0.md`, and `?? docs/hygiene/commission_signal_board_lane_handoff_v0.md`, which appeared during this turn and were not created by this lane.
- Target files or artifacts:
  - `docs/migration/data_lake_spine_first_migration_plan_v0.md`
  - `docs/migration/data_lake_spine_first_migration_inventory_v0.md`
  - `orca/product/spines/data_lake/README.md`
  - `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md`
  - `.agents/workflow-overlay/artifact-folders.md`
  - `docs/migration/repo_structure_data_lake_r2_v0/moved_paths_index.md`
- Related worktrees or branches:
  - Prior context referenced `codex/commission-spine-structure`, `codex/data-lake-core-contract`, and `codex/data-lake-mechanics-map`; current local `main` sources say R2 harvested/superseded their Data Lake content.

## Changed / Inspected / Tested Files

- `docs/workflows/data_lake_r2_continuation_handoff_v0.md`
  - Status: created by this handoff; untracked until staged.
  - Role: cold continuation handoff packet.
  - Important observations: not authority; receiver must verify sources.
  - Symbols or sections: all required `workflow-handoff` max sections.
- `.agents/workflow-overlay/artifact-folders.md`
  - Status: inspected.
  - Role: placement authority and Data Lake R2 receipt holder.
  - Important observations: records `orca/product/` spine tree, Data Lake R2 landed contracts/mechanics, and two planning docs pending placement.
  - Symbols or sections: Accepted Folders; Direction Change Propagation - Data Lake Spine Promotion; Direction Change Propagation - Data Lake R2.
- `orca/product/spines/data_lake/README.md`
  - Status: inspected.
  - Role: Data Lake spine front door.
  - Important observations: states R2 populated authority/workflows; `migrations/` is lake-specific schema/data migration plans, not repo logs; two planning docs deferred.
- `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md`
  - Status: inspected.
  - Role: Data Lake shared-foundation spine binding.
  - Important observations: binds Data Lake identity and subfolder grammar; includes post-R2 note that only two planning docs remain deferred.
- `docs/migration/repo_structure_data_lake_r2_v0/moved_paths_index.md`
  - Status: inspected.
  - Role: R2 path-resolution artifact.
  - Important observations: maps old docs/product and retired shared mechanics paths to data_lake spine homes; records mechanics map canonical confirmation.
- `docs/migration/data_lake_spine_first_migration_plan_v0.md`
  - Status: inspected.
  - Role: older #239 plan; now deferred placement candidate.
  - Important observations: still carries pre-R2 language in places; do not treat its "current binding" statements as current without checking newer binding/R2 sources.
- `docs/migration/data_lake_spine_first_migration_inventory_v0.md`
  - Status: inspected.
  - Role: older #239 inventory; now deferred placement candidate.
  - Important observations: open_next already points to new Data Lake authority docs, but body still records earlier drafting context.

## Frozen Decisions

- Decision: Data Lake is `orca/product/spines/data_lake/`, a shared-foundation spine.
  - Evidence: `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md`; `orca/product/spines/data_lake/README.md`; `.agents/workflow-overlay/artifact-folders.md`.
  - Consequence: Do not put Data Lake under `orca/product/shared/data_lake_mechanics/`.
- Decision: R2 landed Data Lake authority and workflow content.
  - Evidence: `.agents/workflow-overlay/artifact-folders.md` Data Lake R2 receipt; `docs/migration/repo_structure_data_lake_r2_v0/moved_paths_index.md`; files under `orca/product/spines/data_lake/authority/` and `workflows/`.
  - Consequence: Do not reopen the prior 3-way mechanics-map fork unless current sources drift or owner redirects.
- Decision: Data Lake is not a smart orchestrator and does not own Capture, Projection, ECR, Signal Statement, Cleaning, Judgment, or runtime backend selection.
  - Evidence: Data Lake README and promotion binding.
  - Consequence: Any future Data Lake patch must preserve producer/consumer boundaries.
- Decision: Runtime code remains in `orca-harness/` until separately authorized.
  - Evidence: Data Lake README and binding; artifact-folders `orca/product/` rule.
  - Consequence: Do not move code, tests, or harness runtime as part of this lane.

## Mutable Questions

- Question: Should the two #239 migration plan/inventory docs remain in `docs/migration/` or move into `data_lake/migrations/`?
  - Why still mutable: current source text explicitly records the placement as deferred pending decision.
  - What would resolve it: owner acceptance of the recommendation to keep them in `docs/migration/`, followed by a narrow patch to remove deferred-placement wording where appropriate.
- Question: Is local `main` still the correct base for action?
  - Why still mutable: local `main` is behind `origin/main` by 3 commits.
  - What would resolve it: compare/fetch/rebase per current user's instructions and workspace policy before any patch.
- Question: Are untracked scratch packs relevant to this lane?
  - Why still mutable: `_scratch/` includes ChatGPT Pro data-lake architecture source packs that may be historical context but not current authority.
  - What would resolve it: current user asks to consume them, or a controlling source points to them; otherwise exclude by default.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: "R2 is blocked on a 3-way mechanics-map fork."
  - Why stale or dangerous: current Data Lake R2 sources say the mechanics map was reconciled and canonical content landed.
  - Current replacement: `docs/migration/repo_structure_data_lake_r2_v0/moved_paths_index.md` and `.agents/workflow-overlay/artifact-folders.md` Data Lake R2 receipt.
- Stale instruction, idea, artifact, or finding: old Data Lake contract paths under `docs/product/core_spine/`.
  - Why stale or dangerous: R2 moved the live contracts to `orca/product/spines/data_lake/authority/`.
  - Current replacement: moved-path index under `docs/migration/repo_structure_data_lake_r2_v0/`.
- Stale instruction, idea, artifact, or finding: `orca/product/shared/data_lake_mechanics/` as a viable live Data Lake home.
  - Why stale or dangerous: current binding says this was retired by R2 and superseded by `data_lake/workflows/`.
  - Current replacement: `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md`.
- Stale instruction, idea, artifact, or finding: prior `codex/commission-spine-structure` Data Lake plan as current binding.
  - Why stale or dangerous: it was planning input and now contains pre-R2 statements; current binding lives on `main`.
  - Current replacement: Data Lake README, promotion binding, R2 moved-path index, artifact-folders receipt.

## Commands And Verification Evidence

- Command:
  ```powershell
  git status --short --branch
  ```
  Result:
  - Passed/failed/not run: ran 2026-06-20.
  - Important output: latest post-write verification showed `## main...origin/main [behind 6]`, `M docs/hygiene/ig_creator_momentum_lane_handoff_v0.md`, untracked `.codex/hooks/run_orca_guard.py`, `_scratch/`, `docs/hygiene/cleaning_spine_lane_handoff_v0.md`, `docs/hygiene/commission_signal_board_lane_handoff_v0.md`, `docs/prompts/product-planning/orca_spine_first_target_structure_controller_prompt_v0.md`, and `docs/workflows/data_lake_r2_continuation_handoff_v0.md`; permission warning for `orca-harness/.pytest_tmp/`.
  - Re-run target so the receiver can confirm rather than trust: run the same command before acting.
- Command:
  ```powershell
  git rev-parse HEAD
  ```
  Result:
  - Passed/failed/not run: ran 2026-06-20.
  - Important output: `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`.
  - Re-run target so the receiver can confirm rather than trust: run before acting.
- Command:
  ```powershell
  git rev-parse origin/main
  ```
  Result:
  - Passed/failed/not run: ran 2026-06-20.
  - Important output: latest post-write verification showed `5bb52bad208c618b7363a6de7a03a6c1cb5cf3dc`.
  - Re-run target so the receiver can confirm rather than trust: run before acting.
- Command:
  ```powershell
  git diff --check
  ```
  Result:
  - Passed/failed/not run: ran 2026-06-20.
  - Important output: no output observed.
  - Re-run target so the receiver can confirm rather than trust: run after any patch.
- Command:
  ```powershell
  python .agents\hooks\check_map_links.py --strict
  ```
  Result:
  - Passed/failed/not run: ran 2026-06-20.
  - Important output: `check_map_links --strict: OK (0 findings)` and `annotated nonresolving: 30 (debt, not failures)`.
  - Re-run target so the receiver can confirm rather than trust: run if repo-map or retrieval links are patched.
- Command:
  ```powershell
  python .agents\hooks\check_placement.py --check
  ```
  Result:
  - Passed/failed/not run: timed out after about 23 seconds.
  - Important output: emitted 11 violations, 4 freshness warnings, many legacy-tolerated entries, and advisory authority text before timeout. Do not claim pass.
  - Re-run target so the receiver can confirm rather than trust: rerun with an appropriate timeout or targeted scope if placement-sensitive files are patched.

## Blockers And Risks

- Blocker or risk: local `main` is behind `origin/main`.
  - Evidence: `git status --short --branch` and `git rev-parse origin/main`.
  - Likely next action: receiver re-verifies current refs before patching.
- Blocker or risk: broad untracked `_scratch/` source packs and local prompt file are present.
  - Evidence: `git status --porcelain=v1 -uall`.
  - Likely next action: ignore unless current user explicitly includes them; do not stage or delete.
- Blocker or risk: current Data Lake plan/inventory are pre-R2 planning records and can mislead if read as current binding.
  - Evidence: body text says current binding remains `docs/` plus `orca-harness/`, while newer Data Lake README and R2 receipt say the spine is populated.
  - Likely next action: if patch authorized, update deferred-placement and stale pre-R2 wording without changing historical provenance.
- Blocker or risk: placement checker did not pass in this run.
  - Evidence: timeout and emitted known/freshness noise.
  - Likely next action: do not claim validation; rerun after targeted patch if necessary.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - Workspace branch/head/dirty state.
  - Whether `origin/main` is still ahead and whether current thread should update first.
  - Data Lake spine README current contents.
  - Data Lake promotion binding current contents.
  - R2 moved-path index current contents.
  - Whether the two #239 planning docs are still present in `docs/migration/`.
  - Whether newer owner instruction accepted or rejected the recommendation to keep those docs in `docs/migration/`.
- Compare target for each:
  - Branch/head: `git status --short --branch`; `git rev-parse HEAD`; `git rev-parse origin/main`.
  - Plan doc: blob `b6528d4e97173d7c3d4badf0ecfe80739bd0953a` at sender read time.
  - Inventory doc: blob `8487bf4014467e2b6e7f2f804e4f9aa6cac1a853` at sender read time.
  - Other source docs: `reread-required` because the repo is actively moving.
- Load outcomes and what each means:
  - `REUSE`: branch/head/dirty state and load-bearing sources match or are safely re-verified; continue from Exact Next Authorized Action.
  - `PARTIAL_REUSE`: non-load-bearing source drifted; use verified Data Lake sources and re-derive skipped context.
  - `STALE_REREAD_REQUIRED`: branch, head, dirty state, Data Lake README, promotion binding, moved-path index, or planning docs drifted but can be safely reread.
  - `BLOCKED_DRIFT`: drift conflicts with the Data Lake spine identity, old-path resolution, owner constraints, or dirty-state policy.
  - `BLOCKED_MISSING_PACKET`: this handoff file is absent or unreadable.
  - `BLOCKED_UNVERIFIABLE`: a load-bearing claim cannot be re-derived from available sources.
- Sources that must be reread if drift is detected:
  - `orca/product/spines/data_lake/README.md`
  - `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md`
  - `.agents/workflow-overlay/artifact-folders.md`
  - `docs/migration/repo_structure_data_lake_r2_v0/moved_paths_index.md`
  - `docs/migration/data_lake_spine_first_migration_plan_v0.md`
  - `docs/migration/data_lake_spine_first_migration_inventory_v0.md`

## Do Not Forget

- This packet is not authority. The next thread must verify because the repo is behind `origin/main` and active migration work is still landing.
