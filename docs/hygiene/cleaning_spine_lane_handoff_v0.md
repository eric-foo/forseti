# Cleaning Spine Lane Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet
scope: >
  Recoverable handoff for continuing the Cleaning Spine lane after the spine-first
  repo migration, bloat cut, ontology pass, and folder-structure changes.
use_when:
  - Starting a fresh thread or agent lane for Cleaning Spine continuation.
  - Reorienting after the old Cleaning migration-inventory worktree or PR context is stale.
  - Checking which Cleaning sources must be re-read before strict or actionable claims.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-of-truth.md
  - .agents/workflow-overlay/source-loading.md
  - docs/workflows/orca_repo_map_v0.md
  - orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md
stale_if:
  - This handoff file is consumed by a new lane.
  - Local main is fetched, rebased, reset, or materially updated.
  - Cleaning contracts, repo-map routes, or spine-first migration records change.
  - The user redirects the next lane away from Cleaning Spine continuation.
```

## Load Contract

- packet_version: `workflow-handoff/max/v0`
- mode: max
- created_at: 2026-06-20T16:50:22+08:00
- created_by_lane: Codex current thread; provenance only, not authority
- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- handoff_path: `docs/hygiene/cleaning_spine_lane_handoff_v0.md`
- expected_branch: `main` local checkout, behind local `origin/main` by 6 at post-write verification time
- expected_head: `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`
- expected_dirty_state_including_handoff_file:
  ```text
  ## main...origin/main [behind 6]
   M docs/hygiene/ig_creator_momentum_lane_handoff_v0.md
  ?? .codex/hooks/run_orca_guard.py
  ?? _scratch/
  ?? docs/hygiene/cleaning_spine_lane_handoff_v0.md
  ?? docs/hygiene/commission_signal_board_lane_handoff_v0.md
  ?? docs/prompts/product-planning/orca_spine_first_target_structure_controller_prompt_v0.md
  ?? docs/workflows/data_lake_r2_continuation_handoff_v0.md
  warning: could not open directory 'orca-harness/.pytest_tmp/': Permission denied
  ```
- source_loading_mode: repo-overlay-bound
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

goal_handoff: not supplied

Output-fit warning: no verbatim `workflow-goal-framing` goal frame was visible during packet creation, so the receiver cannot use a carried `success_signal` as an authority. The receiver should derive a fresh goal frame from the current user instruction after loading the packet.

## Open Decision / Fork

- decision: What should the next Cleaning lane do after reorientation?
  - options:
    - Reorient from current `main`, reload moved Cleaning sources, and produce the next scoped Cleaning-lane plan.
    - If the owner asks for implementation, run a fresh assumption/implementation gate against current `orca/product/spines/cleaning/contracts/` and current harness state.
    - If the owner asks for migration cleanup, classify stale Cleaning branches/PRs and only then decide whether to retire or harvest them.
  - already constrained / off the table:
    - Do not resume the old closed PR #245 as current authority.
    - Do not resume the removed old inventory worktree path.
    - Do not move files, rewrite repo structure, or merge to `main` unless explicitly redirected by the current user.
    - Do not treat this packet, any old branch, or a migration proposal as validation, readiness, implementation authorization, or product proof.
  - trade-offs:
    - Current `main` contains the migrated Cleaning contracts and is the closest live source, but it is locally behind `origin/main` and dirty with unrelated modified/untracked files.
    - Current Cleaning-specific worktrees exist, but observed ones are stale: `codex/w3b-cleaning` is clean but 73 behind `origin/main`; `codex/ontology-tag-cleaning` has upstream gone.
  - owner of the call: current user / next-thread operator.
  - recommendation and why: Start by re-verifying current `main` or a fresh worktree from updated `origin/main`; use the moved Cleaning contracts as the source anchors and treat old PR #245 only as historical provenance because GitHub reports it closed and unmerged.

## Drift Guard

- invariant, non-goal, or scope boundary: Cleaning is distinct from Capture, Evidence Candidate Record / Signal Content Record, and Judgment.
  - why it matters: Current Cleaning contracts place Cleaning after Capture/projection/ECR and before Judgment; blurring layers would corrupt ownership of traceability, credibility, exclusion, and decision-use effects.
  - what violating it would break: Cleaning could start deciding credibility, independence, Signal Integrity, Signal Use, Decision Strength, or Action Ceiling, which the current contracts assign to Judgment.
- invariant, non-goal, or scope boundary: Raw remains canonical; projection and Cleaning are working views.
  - why it matters: Cleaning may consume projection references but must preserve raw anchors and raw-pull triggers.
  - what violating it would break: Downstream Judgment would lose the ability to inspect source meaning and provenance.
- invariant, non-goal, or scope boundary: Do not reuse old `docs/product/` paths as live homes.
  - why it matters: spine-first Wave C/E moved product artifacts under `orca/product/`; historical references resolve through moved-path indexes.
  - what violating it would break: The receiver would read stale paths or recreate retired structure.
- invariant, non-goal, or scope boundary: Do not treat this handoff as authority.
  - why it matters: Orca source-of-truth says checkpoints are non-authoritative convenience copies.
  - what violating it would break: The receiver could act on stale branch, validation, or file-state claims without re-checking them.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- targets to enter the ladder:
  - `AGENTS.md`
  - `.agents/workflow-overlay/README.md`
  - `.agents/workflow-overlay/source-of-truth.md`
  - `.agents/workflow-overlay/source-loading.md`
  - `.agents/workflow-overlay/artifact-folders.md`
  - `docs/workflows/orca_repo_map_v0.md`
  - `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md`
  - `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
  - `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
  - `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`
  - `orca/product/spines/cleaning/contracts/core_spine_v0_corroboration_vs_amplification_discipline_v0.md`
  - `docs/migration/phase2_proposals/cleaning_w3a_proposal_v0.md`
- already loaded (weak orientation, freshness-marked; not authority): the targets above were read or targeted-read from local `main` at HEAD `c449b0f97906b4be1ccfee7ef734ba54f5b55df1` on 2026-06-20; `docs/workflows/orca_repo_map_v0.md` was searched for Cleaning-related lines rather than fully used as authority.
- must load first before strict or actionable steps: `AGENTS.md`, overlay README, source-of-truth, source-loading, artifact-folders, current git status/head, repo map Cleaning routes, and the Cleaning README/foundation contracts.
- load rule: receiver re-runs progressive source loading per overlay; this packet's loaded set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- decision, framing, profile, or convention: Cleaning is now housed as a spine under `orca/product/spines/cleaning/`, with contracts under `contracts/`.
  - decided in: `.agents/workflow-overlay/artifact-folders.md` and `docs/STRUCTURE.md`
  - compare target: HEAD `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`; blobs `e4011ed4a89a9ed95c9e62568e4e4c92634d3252` and `b60c27933f40d786012dbbb3a3f1e533fe3ef844`
  - verify before: any placement, move, source-path, or repo-structure claim.
- decision, framing, profile, or convention: Cleaning's load-bearing product anchor is the moved Cleaning README and foundation, not the old migration inventory PR.
  - decided in: `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md` and `core_spine_v0_cleaning_spine_foundation_v0.md`
  - compare target: HEAD `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`; blobs `ade7ba2e206ae77e8e2eb97ddcbd2054b7fc13ea` and `f4679e98792412526432859c07005e1935e6b2b9`
  - verify before: any strict Cleaning scope, implementation boundary, or next-action claim.
- decision, framing, profile, or convention: Mechanical projection is Data-Capture-owned and raw remains canonical; Cleaning consumes handles keyed to raw.
  - decided in: `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md` and `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
  - compare target: HEAD `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`; blobs `da93c5c9c1c41b0651d618ec1e4b931f8d7f3e89` and `2f17cf89e6e85f32a7a831f84f27bd25fdf0ada9`
  - verify before: any Cleaning-vs-Capture, projection, ECR/SCR, or Judgment boundary claim.
- decision, framing, profile, or convention: Phase-2 W3a Cleaning proposal found the Cleaning area lean: three docs, zero deletion candidates, three ontology/doc-term findings.
  - decided in: `docs/migration/phase2_proposals/cleaning_w3a_proposal_v0.md`
  - compare target: HEAD `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`; blob `a37196057d46e0bbd162d6f876b963cc1ecff52b`
  - verify before: any claim that Cleaning bloat has been assessed or that no Cleaning contract file should be deleted.
- decision, framing, profile, or convention: PR #245 for `docs/migration/cleaning_spine_first_migration_inventory_v0.md` is closed and unmerged, so it is historical provenance only.
  - decided in: GitHub PR metadata for `eric-foo/orca#245`
  - compare target: observed via GitHub connector on 2026-06-20: state `closed`, merged `false`, head SHA `c7962162549d2ad287677be11151dfa433390775`
  - verify before: using the old migration inventory as anything more than provenance.

## Active Objective

Create a cold-reader handoff for the Cleaning Spine lane after repository migration and structure drift, so another thread can re-verify current sources and continue only the Cleaning lane without relying on stale branch/worktree memory.

## Exact Next Authorized Action

1. In the next thread, open this packet and run the confirm-don't-trust checklist below.
2. Re-check repo state from `C:\Users\vmon7\Desktop\projects\orca`: branch, HEAD, `origin/main`, dirty/untracked files, and whether a fresh worktree is needed before any docs or implementation edits.
3. Load the current Cleaning source pack: AGENTS/overlay, source-of-truth, source-loading, artifact-folders, repo map Cleaning routes, Cleaning README, Cleaning foundation, boundary note, projection doctrine, corroboration/amplification note, and Cleaning W3a proposal.
4. Ask or infer from the current user instruction whether the next lane is planning, implementation scoping, review, migration cleanup, or source refresh. Stop if the user asks to move files, merge structure, or claim readiness without a new explicit authorization.

## Authority And Source Ledger

- Repository instructions:
  - `AGENTS.md`
    - Role: Orca agent behavior kernel and project-entry rules.
    - Load-bearing: yes
    - Compare target: HEAD `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`, blob `8715ece8c18d14fc6b498639ea24ed8b1d8de1c2`
    - Last checked: 2026-06-20
    - Reuse rule: reread before any strict/actionable continuation.
- Overlay or equivalent authority:
  - `.agents/workflow-overlay/README.md`
    - Role: overlay entrypoint.
    - Load-bearing: yes
    - Compare target: HEAD `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`, blob `57cbc892dcd79d4d57686db465900ad042769174`
    - Last checked: 2026-06-20
    - Reuse rule: reread before strict/actionable continuation.
  - `.agents/workflow-overlay/source-of-truth.md`
    - Role: source hierarchy and checkpoint lifecycle; states handoff packets are non-authoritative convenience copies under `docs/hygiene/`.
    - Load-bearing: yes
    - Compare target: HEAD `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`, blob `fd42a38eb206327ff474fa83a2a5c90165c12a59`
    - Last checked: 2026-06-20
    - Reuse rule: reread before treating this handoff or any checkpoint as usable.
  - `.agents/workflow-overlay/source-loading.md`
    - Role: source-loading budgets and start preflight.
    - Load-bearing: yes
    - Compare target: HEAD `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`, blob `17eb55585e8d26ed8bf91a0a70bca987b88ed4ce`
    - Last checked: 2026-06-20
    - Reuse rule: reread before choosing source pack or making strict claims.
  - `.agents/workflow-overlay/artifact-folders.md`
    - Role: accepted folders and spine-first product tree placement.
    - Load-bearing: yes
    - Compare target: HEAD `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`, blob `e4011ed4a89a9ed95c9e62568e4e4c92634d3252`
    - Last checked: 2026-06-20
    - Reuse rule: reread before placement or artifact-location claims.
- User constraints:
  - Current user asked for `workflow-handoff` so work can continue in another thread for this lane.
    - Role: current-turn scope.
    - Load-bearing: yes
    - Compare target: current chat instruction, no repo compare target; reread-required from thread.
    - Last checked: 2026-06-20
    - Reuse rule: current user instruction wins over this packet if redirected.
- Source-read ledger:
  - `docs/workflows/orca_repo_map_v0.md`
    - Role: current navigation map; targeted Cleaning route search.
    - Load-bearing: yes for route existence, no for full-state truth.
    - Compare target: HEAD blob `efb1b91e01e563257da6d3618a60e9f4eec6237e`; local `origin/main` blob observed as `d52840047dab4e011ffd2dc4a6e587452551ac21`, so re-read after updating.
    - Last checked: 2026-06-20
    - Reuse rule: reread after fetch/rebase before relying on map routes.
  - `repo-structure.yaml`
    - Role: machine map router only.
    - Load-bearing: yes for current known top-level routing, no for authority.
    - Compare target: HEAD blob `11e3428d722d81258b5c0b348f4d89c725254a45`
    - Last checked: 2026-06-20
    - Reuse rule: reread if running placement checks or asserting top-level structure.
  - `docs/STRUCTURE.md`
    - Role: navigation guide.
    - Load-bearing: no unless used for route support.
    - Compare target: HEAD blob `b60c27933f40d786012dbbb3a3f1e533fe3ef844`
    - Last checked: 2026-06-20
    - Reuse rule: advisory; overlay wins.
  - `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md`
    - Role: Cleaning entrypoint and build boundary.
    - Load-bearing: yes
    - Compare target: HEAD blob `ade7ba2e206ae77e8e2eb97ddcbd2054b7fc13ea`
    - Last checked: 2026-06-20
    - Reuse rule: reread before any Cleaning lane continuation.
  - `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
    - Role: Cleaning layer contract and OD-1/OD-4/OD-7 state.
    - Load-bearing: yes
    - Compare target: HEAD blob `f4679e98792412526432859c07005e1935e6b2b9`
    - Last checked: 2026-06-20
    - Reuse rule: reread before any scope, architecture, or implementation claim.
  - `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
    - Role: Capture / ECR / Cleaning / Judgment boundary.
    - Load-bearing: yes
    - Compare target: HEAD blob `2f17cf89e6e85f32a7a831f84f27bd25fdf0ada9`
    - Last checked: 2026-06-20
    - Reuse rule: reread before layer-boundary claims.
  - `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`
    - Role: projection as raw-keyed Data-Capture-owned view, not Cleaning or Judgment.
    - Load-bearing: yes
    - Compare target: HEAD blob `da93c5c9c1c41b0651d618ec1e4b931f8d7f3e89`
    - Last checked: 2026-06-20
    - Reuse rule: reread before projection/Cleaning interface claims.
  - `orca/product/spines/cleaning/contracts/core_spine_v0_corroboration_vs_amplification_discipline_v0.md`
    - Role: Cleaning/Judgment split for dedupe, corroboration, and amplification.
    - Load-bearing: yes for dedupe boundary claims.
    - Compare target: HEAD blob `b82501b52d8114a1660164a00e8c6851c4c4577a`
    - Last checked: 2026-06-20
    - Reuse rule: reread before dedupe/clustering/independence claims.
  - `docs/migration/phase2_proposals/cleaning_w3a_proposal_v0.md`
    - Role: current migration/bloat/ontology proposal for Cleaning area.
    - Load-bearing: yes for migration-cleanup claims only.
    - Compare target: HEAD blob `a37196057d46e0bbd162d6f876b963cc1ecff52b`
    - Last checked: 2026-06-20
    - Reuse rule: reread before claiming Cleaning W3a outcome.
- Source gaps:
  - Local main is behind local `origin/main` by 6 at post-write verification; no fetch was run by this handoff pass.
  - `git status` emitted a permission warning for `orca-harness/.pytest_tmp/`.
  - Old `docs/migration/cleaning_spine_first_migration_inventory_v0.md` is not present in the current working tree; it exists only on `origin/codex/cleaning-spine-first-migration-inventory` at observed commit `c7962162549d2ad287677be11151dfa433390775`.
- Strict-only blockers:
  - Do not claim current latest `origin/main` state until fetch/verify runs.
  - Do not claim validation, readiness, implementation authorization, or migration completion from this handoff.
- Not-proven boundaries:
  - Cleaning is not owner-ratified or implementation-ready by this packet.
  - The old inventory PR being closed/unmerged does not prove its contents wrong; it only means it is not current main authority.

## Current Task State

- Completed:
  - Fresh live state located the current Orca repo at `C:\Users\vmon7\Desktop\projects\orca`.
  - Old configured Codex worktree path `C:\Users\vmon7\.codex\worktrees\33ea\orca` was invalid for shell execution in this session.
  - Old Cleaning inventory PR #245 was checked through GitHub: closed, unmerged, draft, head SHA `c7962162549d2ad287677be11151dfa433390775`.
  - Current Cleaning contracts were found under `orca/product/spines/cleaning/contracts/`.
  - Current migration proposal for Cleaning W3a was found under `docs/migration/phase2_proposals/cleaning_w3a_proposal_v0.md`.
- Partially completed:
  - Reorientation is not complete for the next work lane; this packet only records how to reload and what to avoid trusting.
- Broken or uncertain:
  - Local main is behind local `origin/main` by 6 at post-write verification and was not updated.
  - Main has unrelated modified/untracked files and a status warning.
  - `codex/w3b-cleaning` is clean but 73 behind `origin/main`.
  - `codex/ontology-tag-cleaning` has upstream gone.

## Workspace State

- Branch: `main`
- Head: `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`
- Local `origin/main`: `5bb52bad208c618b7363a6de7a03a6c1cb5cf3dc`
- Dirty or untracked state before handoff:
  ```text
  ## main...origin/main [behind 6]
   M docs/hygiene/ig_creator_momentum_lane_handoff_v0.md
  ?? .codex/hooks/run_orca_guard.py
  ?? _scratch/
  ?? docs/hygiene/commission_signal_board_lane_handoff_v0.md
  ?? docs/prompts/product-planning/orca_spine_first_target_structure_controller_prompt_v0.md
  ?? docs/workflows/data_lake_r2_continuation_handoff_v0.md
  warning: could not open directory 'orca-harness/.pytest_tmp/': Permission denied
  ```
- Dirty or untracked state after writing the handoff file:
  ```text
  ## main...origin/main [behind 6]
   M docs/hygiene/ig_creator_momentum_lane_handoff_v0.md
  ?? .codex/hooks/run_orca_guard.py
  ?? _scratch/
  ?? docs/hygiene/cleaning_spine_lane_handoff_v0.md
  ?? docs/hygiene/commission_signal_board_lane_handoff_v0.md
  ?? docs/prompts/product-planning/orca_spine_first_target_structure_controller_prompt_v0.md
  ?? docs/workflows/data_lake_r2_continuation_handoff_v0.md
  warning: could not open directory 'orca-harness/.pytest_tmp/': Permission denied
  ```
- Target files or artifacts:
  - `docs/hygiene/cleaning_spine_lane_handoff_v0.md`
  - `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md`
  - `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
  - `docs/migration/phase2_proposals/cleaning_w3a_proposal_v0.md`
- Related worktrees or branches:
  - `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\w3b-cleaning`: branch `codex/w3b-cleaning`, HEAD `2cdbb723`, clean, behind `origin/main` by 73.
  - `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\ontology-tag-cleaning`: branch `codex/ontology-tag-cleaning`, HEAD `47ab2d22`, upstream gone.
  - `origin/codex/cleaning-spine-first-migration-inventory`: contains old inventory commit `c7962162549d2ad287677be11151dfa433390775`; GitHub PR #245 closed unmerged.

## Changed / Inspected / Tested Files

- `docs/hygiene/cleaning_spine_lane_handoff_v0.md`
  - Status: newly created untracked handoff checkpoint.
  - Role: cold-reader handoff; non-authoritative.
  - Important observations: records current drift, current Cleaning sources, and exact next reorientation action.
  - Symbols or sections: all handoff contract sections.
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md`
  - Status: inspected.
  - Role: Cleaning entrypoint and build boundary.
  - Important observations: Cleaning purpose is a thin source-agnostic core with traceable handles and non-destructive ledgers; not generic ETL; build boundary still needs scoping.
  - Symbols or sections: Purpose; Short Mental Model; What Is Generic; Build Boundary.
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
  - Status: inspected.
  - Role: Cleaning layer contract.
  - Important observations: status `FOUNDATION_DRAFT_FROM_PROJECTION_CANDIDATE`; bounded substrate v0 implementation authorization exists for source-invariant Pydantic models plus exact-identity deriver only; not broader Cleaning/ECR/Judgment.
  - Symbols or sections: Layer Boundary; Allowed Transform Classes; Owner Directions Installed.
- `docs/migration/phase2_proposals/cleaning_w3a_proposal_v0.md`
  - Status: inspected.
  - Role: W3a proposal for Cleaning area.
  - Important observations: 3 files scanned; 0 deletion candidates; 3 ontology/doc-term findings.
  - Symbols or sections: Summary; A. Deletion candidates; B. Ontology / doc-term findings.
- `docs/workflows/orca_repo_map_v0.md`
  - Status: targeted search inspected.
  - Role: repo map.
  - Important observations: current map routes product artifacts to `orca/product/` and lists `orca/product/spines/cleaning/` as Cleaning spine.
  - Symbols or sections: root/product route lines around Cleaning hits.

## Frozen Decisions

- Decision: For current continuation, use current `orca/product/spines/cleaning/contracts/` files as the Cleaning source anchors.
  - Evidence: artifact-folders and repo map show spine-first product tree; Cleaning README/foundation exist at moved paths.
  - Consequence: Do not open old `docs/product/...` paths except through moved-path indexes for provenance.
- Decision: Cleaning owns non-destructive transformation mechanics, not Judgment effects.
  - Evidence: Cleaning foundation Layer Boundary and boundary note Layer Rules.
  - Consequence: Any plan that lets Cleaning decide credibility, exclusion, independent corroboration, artificial amplification, Signal Integrity, Signal Use, Decision Strength, or Action Ceiling must stop or be rerouted.
- Decision: Exact-identity dedupe mechanics are the only core-v0 dedupe mechanics currently authorized in Cleaning.
  - Evidence: Cleaning foundation OD-4 and corroboration/amplification note.
  - Consequence: Near-match dedupe, copied-language grouping, and clustering remain candidate/deferred unless separately owner-authorized.
- Decision: The previous Cleaning migration inventory branch is not current main authority.
  - Evidence: PR #245 observed closed and unmerged; current working tree lacks the inventory doc.
  - Consequence: Treat that artifact as historical provenance only unless the owner reintroduces it.

## Mutable Questions

- Question: Should the next lane be implementation scoping, architecture planning, migration cleanup, or another review pass?
  - Why still mutable: The current user asked for a handoff only.
  - What would resolve it: next-thread user instruction after loading this packet.
- Question: Should the next lane start from current local `main`, a fresh worktree from updated `origin/main`, or a Cleaning-specific branch?
  - Why still mutable: local main is behind and dirty; current Cleaning worktrees are stale.
  - What would resolve it: receiver fetch/status check plus current user preference.
- Question: What should happen to stale Cleaning branches after migration?
  - Why still mutable: PR #245 is closed unmerged; `codex/w3b-cleaning` and `codex/ontology-tag-cleaning` are not safe continuation bases as observed.
  - What would resolve it: explicit cleanup/migration-controller direction.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: `docs/migration/cleaning_spine_first_migration_inventory_v0.md` from PR #245 as a current source.
  - Why stale or dangerous: GitHub reports PR #245 closed and unmerged; the file is absent from current working tree.
  - Current replacement: current Cleaning contracts under `orca/product/spines/cleaning/contracts/` plus `docs/migration/phase2_proposals/cleaning_w3a_proposal_v0.md` for migration cleanup.
- Stale instruction, idea, artifact, or finding: old worktree `C:\Users\vmon7\Desktop\projects\orca\orca-worktrees\cleaning-spine-first-migration-inventory`.
  - Why stale or dangerous: `Test-Path` returned false for the path and its `.git`.
  - Current replacement: current main checkout at `C:\Users\vmon7\Desktop\projects\orca`, or a fresh worktree the receiver creates after checking dirty state.
- Stale instruction, idea, artifact, or finding: old `docs/product/` product paths as live homes.
  - Why stale or dangerous: artifact-folders and STRUCTURE route product artifacts to `orca/product/`; docs/product paths are historical after Wave E.
  - Current replacement: use moved paths under `orca/product/` and the moved-path indexes for historical references.

## Commands And Verification Evidence

- Command:
  ```powershell
  git -C C:\Users\vmon7\Desktop\projects\orca status --short --branch
  ```
  Result:
  - Passed/failed/not run: passed with warning.
  - Important output:
    ```text
    ## main...origin/main [behind 6]
     M docs/hygiene/ig_creator_momentum_lane_handoff_v0.md
    ?? .codex/hooks/run_orca_guard.py
    ?? _scratch/
    ?? docs/hygiene/cleaning_spine_lane_handoff_v0.md
    ?? docs/hygiene/commission_signal_board_lane_handoff_v0.md
    ?? docs/prompts/product-planning/orca_spine_first_target_structure_controller_prompt_v0.md
    ?? docs/workflows/data_lake_r2_continuation_handoff_v0.md
    warning: could not open directory 'orca-harness/.pytest_tmp/': Permission denied
    ```
  - Re-run target so the receiver can confirm rather than trust: run the same command after opening this packet.
- Command:
  ```powershell
  git -C C:\Users\vmon7\Desktop\projects\orca rev-parse HEAD
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: `c449b0f97906b4be1ccfee7ef734ba54f5b55df1`
  - Re-run target so the receiver can confirm rather than trust: run before acting.
- Command:
  ```powershell
  git -C C:\Users\vmon7\Desktop\projects\orca rev-parse origin/main
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: `5bb52bad208c618b7363a6de7a03a6c1cb5cf3dc`
  - Re-run target so the receiver can confirm rather than trust: run after any fetch; do not assume this local remote ref is latest.
- Command:
  ```powershell
  git -C C:\Users\vmon7\Desktop\projects\orca ls-tree HEAD <source paths>
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: source blob IDs are listed in the Authority And Source Ledger.
  - Re-run target so the receiver can confirm rather than trust: rerun for every source used in a strict claim.
- Command:
  ```powershell
  git -C C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\w3b-cleaning status --short --branch
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: `## codex/w3b-cleaning...origin/main [behind 73]`
  - Re-run target so the receiver can confirm rather than trust: only needed if considering that stale worktree.
- Command:
  ```text
  GitHub connector _get_pr_info(repository_full_name="eric-foo/orca", pr_number=245)
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: PR #245 URL `https://github.com/eric-foo/orca/pull/245`, state `closed`, merged `false`, draft `true`, head SHA `c7962162549d2ad287677be11151dfa433390775`.
  - Re-run target so the receiver can confirm rather than trust: re-check PR #245 only if deciding whether to reuse or retire old inventory provenance.

## Blockers And Risks

- Blocker or risk: current local main is behind local `origin/main` by 6 at post-write verification and no fetch was run by this handoff pass.
  - Evidence: status and `rev-parse` outputs above.
  - Likely next action: receiver should fetch/recheck or create a fresh worktree before edits.
- Blocker or risk: unrelated modified/untracked files are present.
  - Evidence: `docs/hygiene/ig_creator_momentum_lane_handoff_v0.md`, `.codex/hooks/run_orca_guard.py`, `_scratch/`, `docs/hygiene/commission_signal_board_lane_handoff_v0.md`, `docs/prompts/product-planning/orca_spine_first_target_structure_controller_prompt_v0.md`, and `docs/workflows/data_lake_r2_continuation_handoff_v0.md` appear in post-write status alongside this handoff file.
  - Likely next action: leave them untouched unless the current user redirects; use a fresh worktree for new source-changing work.
- Blocker or risk: `orca-harness/.pytest_tmp/` permission warning prevents a fully clean status read.
  - Evidence: status warning.
  - Likely next action: avoid strict whole-tree cleanliness claims until that warning is resolved or scoped out.
- Blocker or risk: old Cleaning inventory PR is closed unmerged.
  - Evidence: GitHub PR #245 metadata.
  - Likely next action: do not treat PR #245 as current source; harvest only if owner asks.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - Current repo path is readable and branch/head match or drift is understood.
  - Dirty state matches or drift is classified.
  - Product artifacts live under `orca/product/`, not `docs/product/`.
  - Cleaning contracts exist at the moved paths.
  - Cleaning README/foundation still carry the same build boundary and OD-1/OD-4/OD-7 posture.
  - Boundary note and projection doctrine still keep Projection Data-Capture-owned and raw canonical.
  - PR #245 remains closed/unmerged if it is being considered.
  - Current user instruction still wants Cleaning lane continuation.
- Compare target for each:
  - Git branch/head/status commands above.
  - `git ls-tree HEAD <path>` blob IDs above.
  - GitHub PR #245 metadata above.
  - Current chat instruction for lane scope.
- Load outcomes and what each means:
  - `REUSE`: all required load-bearing facts re-verified; continue with Exact Next Authorized Action.
  - `PARTIAL_REUSE`: only optional or non-load-bearing facts drifted; reuse verified anchors and re-derive the rest.
  - `STALE_REREAD_REQUIRED`: local head, repo map, Cleaning contracts, or dirty state drifted but can be safely reloaded.
  - `BLOCKED_DRIFT`: drift conflicts with user constraints, dirty-state policy, or source authority.
  - `BLOCKED_MISSING_PACKET`: this file is absent or unreadable.
  - `BLOCKED_UNVERIFIABLE`: a load-bearing claim cannot be re-derived from repo or GitHub state.
- Sources that must be reread if drift is detected:
  - `AGENTS.md`
  - `.agents/workflow-overlay/README.md`
  - `.agents/workflow-overlay/source-of-truth.md`
  - `.agents/workflow-overlay/source-loading.md`
  - `.agents/workflow-overlay/artifact-folders.md`
  - `docs/workflows/orca_repo_map_v0.md`
  - `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md`
  - `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
  - `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
  - `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`
  - `docs/migration/phase2_proposals/cleaning_w3a_proposal_v0.md`

## Do Not Forget

- This packet is a checkpoint artifact, not source of truth.
- The next lane should start by re-verifying current source files and status, not by trusting this packet.
- Continue only Cleaning Spine work unless the current user redirects.
- Do not move files, merge, rewrite repo structure, or claim readiness from this handoff.
