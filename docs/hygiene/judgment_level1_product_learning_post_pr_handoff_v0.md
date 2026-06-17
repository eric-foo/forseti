# Judgment Level 1 Product-Learning Post-PR Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet (workflow-handoff output; continuation artifact, not readiness evidence)
scope: >
  Transfers the Judgment Level 1 product-learning lane after PR #233 was updated
  to reflect the backtesting-first MGT/SCV propagation. Routes the next fresh
  lane toward prompt-orchestrated commission-gate and Level 1 judgment prompt
  artifacts, then the remaining source/outcome/forecast/action/log/evaluation
  docs-only scaffolding.
use_when:
  - Relaunching the Judgment Level 1 product-learning lane from PR #233.
  - Checking what remains after the backtesting-first core-minimum propagation.
  - Preventing a fresh lane from reusing the consumed pre-propagation handoff.
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine/judgment_level1_product_learning_core_minimum_v0.md
  - docs/product/judgment_spine/judgment_current_state_and_decomposition_v0.md
  - docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md
  - docs/workflows/orca_repo_map_v0.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
stale_if:
  - PR #233 changes head, base, title, or body after this packet without a refresh.
  - PR #230 or PR #233 lands, closes, rebases, or retargets.
  - The Level 1 core-minimum doc changes its MGT/SCV contract, default mode, next docs-only moves, or DCP receipt.
  - A commission-gate or Level 1 judgment prompt artifact lands after this packet.
  - A source registry, outcome-label sheet, forecast record, decision log, benchmark policy, or evaluation sheet lands after this packet.
```

## Load Contract

- packet_version: handoff_v0
- mode: max
- created_at: 2026-06-17
- created_by_lane: Codex lane `codex/judgment-level1-core-minimum`
- workspace: `C:/Users/vmon7/Desktop/projects/orca/.codex/worktrees/judgment-level1-core-minimum`
- handoff_path: `docs/hygiene/judgment_level1_product_learning_post_pr_handoff_v0.md`
- expected_branch: `codex/judgment-level1-core-minimum`
- expected_pr: `https://github.com/eric-foo/orca/pull/233`
- expected_base: `codex/judgement-lane` at `dec37f13cd63a8e683aafeca7851f700e1f0c064` when PR metadata was checked
- expected_pr_head_before_this_handoff_file: `2a125c578cf09a7947b54429de6d3fac511ae3be`
- expected_dirty_state_including_handoff_file: clean before writing this handoff file; this file is newly added by the handoff refresh and must be committed/pushed if it is to travel with PR #233
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority

## Goal Handoff

`goal_handoff` was not supplied as a structured frame in this turn. Output-fit
checking must use the active objective and drift guard below, not an inferred
goal frame.

## Open Decision / Fork

- decision: whether the receiving lane continues from unmerged PR #233 or waits
  until PR #230 and PR #233 land.
- options:
  - Continue from PR #233 head for dependent docs-only continuation work.
  - Wait until PR #230 and PR #233 are merged before starting a fresh lane off
    `main`.
- already constrained / off the table:
  - Do not start this continuation from current `main` and assume the Level 1
    core minimum is present there.
  - Do not hand-edit durable prompt artifacts; use `workflow-prompt-orchestrator`.
  - Do not run cases, capture sources, score, claim readiness, or claim
    judgment-quality evidence from these setup docs.
- trade-offs:
  - Continuing from PR #233 preserves momentum but keeps the lane dependent on
    PR #230 and PR #233.
  - Waiting for merges reduces branch dependency but delays the next docs-only
    scaffolding.
- owner of the call: repository owner / current user.
- recommendation: continue from PR #233 only if the owner intentionally wants a
  dependent lane; otherwise wait for the prerequisite PR stack to land.

## Drift Guard

- invariant, non-goal, or scope boundary: Level 1 is backtesting-first
  product-learning setup.
  - why it matters: it keeps the uploaded MGT/SCV target from inflating into
    live/client readiness, scoring, buyer proof, or judgment-quality claims.
  - what violating it would break: claim discipline in the evidence ladder and
    conductor/gate ownership boundaries.
- invariant, non-goal, or scope boundary: prompt artifacts are
  prompt-orchestrator-owned.
  - why it matters: the core-minimum DCP intentionally left stale prompt
    handoffs unedited because durable prompts must be authored through
    `workflow-prompt-orchestrator`.
  - what violating it would break: Orca prompt source-loading and preflight
    discipline.
- invariant, non-goal, or scope boundary: the consumed pre-propagation handoff
  must not be relaunched as current.
  - why it matters: it predated the backtesting-first propagation and was deleted
    by the first core-minimum commit.
  - what violating it would break: the next lane would re-enter with stale
    assumptions about missing MGT/SCV propagation.

## Inherited Context

### Source-loading state to re-establish

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- project entry authority: `AGENTS.md` and `.agents/workflow-overlay/README.md`
- targets to enter the ladder:
  - `docs/product/judgment_spine/judgment_level1_product_learning_core_minimum_v0.md`
  - `docs/product/judgment_spine/judgment_current_state_and_decomposition_v0.md`
  - `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md`
  - `docs/workflows/orca_repo_map_v0.md`
  - `.agents/workflow-overlay/prompt-orchestration.md`
- already loaded: prior sender read the overlay entrypoint, GitHub PR state,
  the Level 1 core-minimum propagation diff, and subagent audit outputs. Treat
  all of that as weak orientation.
- must load first before strict or actionable steps:
  1. `AGENTS.md`
  2. `.agents/workflow-overlay/README.md`
  3. `.agents/workflow-overlay/source-of-truth.md`
  4. `.agents/workflow-overlay/source-loading.md`
  5. `.agents/workflow-overlay/prompt-orchestration.md`
  6. the Level 1 core-minimum doc and the Judgment consolidation map
- load rule: receiver re-runs progressive source loading per overlay; this
  packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors

- decision, framing, profile, or convention: Level 1 core-plus-satellite work is
  backtesting-first by default; `live_internal` and `client_facing` are later
  gated modes.
  - decided in: `docs/product/judgment_spine/judgment_level1_product_learning_core_minimum_v0.md`
  - compare target: blob `c54578630e5a7bf7989be2206bc036876463e575` at
    `2a125c578cf09a7947b54429de6d3fac511ae3be`
  - verify before: any Level 1 continuation, prompt artifact, or case admission
- decision, framing, profile, or convention: fragrance remains the first
  satellite; core owns the reusable mode, gate, evidence, forecast/action/log,
  evaluation, and readiness boundaries.
  - decided in: `docs/product/judgment_spine/fragrance_level1_product_learning_satellite_skeleton_v0.md`
  - compare target: blob `31c6acc4a14743052a220f284880148371edaf08` at
    `2a125c578cf09a7947b54429de6d3fac511ae3be`
  - verify before: any fragrance-specific artifact or prompt
- decision, framing, profile, or convention: the 25-case fragrance casebook is
  a first-success learning pack, not a readiness screen.
  - decided in: `docs/product/judgment_spine/fragrance_level1_casebook_admission_frame_v0.md`
  - compare target: blob `d4c3dce1d03cc15f6110abf9abe97e322201ae00` at
    `2a125c578cf09a7947b54429de6d3fac511ae3be`
  - verify before: named-case admission or casebook row work

## Active Objective

Prepare the next Judgment Level 1 product-learning lane after PR #233. The next
lane should not redo the propagation; it should continue into the missing
docs-only artifacts that make the backtesting-first loop runnable later without
claiming run authority.

## Exact Next Authorized Action

1. Confirm PR #233 is still open, based on `codex/judgment-level1-core-minimum`,
   and includes the latest handoff commit if this file has been committed.
2. Use `workflow-prompt-orchestrator` to author durable commission-gate and
   Level 1 judgment prompt artifacts, or block if the current user does not want
   prompt artifacts next.
3. After prompt artifacts are bounded, create or point to the source registry,
   outcome-label sheet, forecast record, utility/action record, decision log,
   benchmark policy, and evaluation sheet named by the core-minimum doc.
4. Stop before named-case admission unless the owner explicitly chooses the
   first case and accepts the remaining source-boundary blockers.

## Authority And Source Ledger

- Repository instructions:
  - `AGENTS.md`
    - Role: project instruction authority.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: 2026-06-17 in this lane.
    - Reuse rule: reread before any actionable continuation.
- Overlay authority:
  - `.agents/workflow-overlay/README.md`
    - Role: overlay entrypoint.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: 2026-06-17 in this lane.
    - Reuse rule: reread before any actionable continuation.
  - `.agents/workflow-overlay/prompt-orchestration.md`
    - Role: owner for durable prompt artifact authoring.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: earlier lane source-loading; not reread in full for this
      handoff refresh.
    - Reuse rule: reread before writing or editing prompt artifacts.
- PR surface:
  - `https://github.com/eric-foo/orca/pull/233`
    - Role: current review surface for this dependent lane.
    - Load-bearing: yes.
    - Compare target: PR #233 title `docs: propagate judgment Level 1 backtest
      core`, head `2a125c578cf09a7947b54429de6d3fac511ae3be` before this
      handoff file, base `codex/judgement-lane`.
    - Last checked: 2026-06-17 after PR body update.
    - Reuse rule: re-run `gh pr view 233 --json number,title,body,url,isDraft,state,headRefName,baseRefName` before relying on it.
- Core docs:
  - `docs/product/judgment_spine/judgment_level1_product_learning_core_minimum_v0.md`
    - Role: controlling Level 1 backtesting-first MGT/SCV route.
    - Load-bearing: yes.
    - Compare target: blob `c54578630e5a7bf7989be2206bc036876463e575`.
    - Last checked: 2026-06-17.
    - Reuse rule: reread before any strict Level 1 continuation.
  - `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md`
    - Role: Judgment Spine entry submap.
    - Load-bearing: yes.
    - Compare target: blob `7e11c6996d632ee6ec3dab0bcc1465c0fa18f83e`.
    - Last checked: 2026-06-17.
    - Reuse rule: reread before route claims.
  - `docs/workflows/orca_repo_map_v0.md`
    - Role: top-level repo map.
    - Load-bearing: yes.
    - Compare target: blob `7bd7e11621398f31da05ed421fde57cef1652983`.
    - Last checked: 2026-06-17.
    - Reuse rule: reread before repo-map claims.

Source gaps:

- The uploaded temp docs are not durable Orca authority by themselves. The
  durable propagated route is the repo doc set in PR #233.
- No durable commission-gate or Level 1 judgment prompt artifact exists yet by
  this packet.
- No source registry, outcome-label sheet, forecast record, decision log,
  benchmark policy, or evaluation sheet exists yet by this packet.

Strict-only blockers:

- If PR #233 head drifts after this packet, reread the changed files before
  continuing.
- If the next task is prompt artifact authoring, load
  `.agents/workflow-overlay/prompt-orchestration.md` and use
  `workflow-prompt-orchestrator`; do not hand-draft prompts.

Not-proven boundaries:

- Not validation.
- Not readiness.
- Not buyer proof.
- Not source-capture authority.
- Not run authorization.
- Not scoring authorization.
- Not `live_internal` or `client_facing` readiness.
- Not judgment-quality evidence.

## Current Task State

Completed:

- PR #233 exists as a draft PR against `codex/judgement-lane`.
- PR title and body were updated to describe the backtesting-first MGT/SCV
  propagation and validation caveats.
- Commit `2a125c578cf09a7947b54429de6d3fac511ae3be` propagated the uploaded
  2026-06-17 MGT/SCV target into the Level 1 core-minimum route, current-state
  decomposition, fragrance docs, the Judgment consolidation map, and the repo
  map.
- PR checks observed after body update: `orca-harness-tests` passed and `route`
  passed.

Partially completed:

- Prompt handoff artifacts were checked for stale route risk but intentionally
  not edited. They require a prompt-orchestrator pass.

Broken or uncertain:

- `python .agents/hooks/check_placement.py --staged --strict` fails on
  pre-existing whole-repo placement debt such as `.github`, `.githooks`,
  `.gitattributes`, and legacy harness inventory. Changed-file placement checks
  passed.

## Workspace State

- Branch: `codex/judgment-level1-core-minimum`
- Head before writing this handoff file:
  `2a125c578cf09a7947b54429de6d3fac511ae3be`
- Dirty or untracked state before writing this handoff file:
  `git status --short --branch` returned
  `## codex/judgment-level1-core-minimum...origin/codex/judgment-level1-core-minimum`
- Dirty or untracked state after writing this handoff file: this file is newly
  added until committed.
- Related PRs:
  - PR #230: base prerequisite branch `codex/judgement-lane`.
  - PR #233: current dependent branch `codex/judgment-level1-core-minimum`.

## Changed / Inspected / Tested Files

- `docs/product/judgment_spine/judgment_level1_product_learning_core_minimum_v0.md`
  - Status: changed in commit `2a125c578cf09a7947b54429de6d3fac511ae3be`.
  - Role: controlling Level 1 MGT/SCV backtesting-first route.
  - Important observation: next work starts with prompt-orchestrated gate/prompt
    artifacts and docs-only registry/evaluation scaffolding, not case execution.
- `docs/product/judgment_spine/fragrance_level1_product_learning_satellite_skeleton_v0.md`
  - Status: changed in commit `2a125c578cf09a7947b54429de6d3fac511ae3be`.
  - Role: fragrance satellite organizer.
  - Important observation: default `mode: backtest`; passive monitor answers are
    disallowed.
- `docs/product/judgment_spine/fragrance_level1_casebook_admission_frame_v0.md`
  - Status: changed in commit `2a125c578cf09a7947b54429de6d3fac511ae3be`.
  - Role: 25-slot casebook organizer.
  - Important observation: 25 cases are a first-success learning pack, not a
    readiness screen.
- `docs/product/judgment_spine/fragrance_level1_named_case_candidate_screen_v0.md`
  - Status: changed in commit `2a125c578cf09a7947b54429de6d3fac511ae3be`.
  - Role: candidate ranking screen.
  - Important observation: rankings did not become admissions.
- `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md`
  - Status: changed in commit `2a125c578cf09a7947b54429de6d3fac511ae3be`.
  - Role: Judgment Spine submap.
- `docs/workflows/orca_repo_map_v0.md`
  - Status: changed in commit `2a125c578cf09a7947b54429de6d3fac511ae3be`.
  - Role: top-level route map.
- `docs/hygiene/judgment_level1_product_learning_core_minimum_handoff_v0.md`
  - Status: deleted by commit `e2adb88b` as consumed.
  - Important observation: do not relaunch it as current.

## Frozen Decisions

- Decision: Level 1 product-learning now adopts the backtesting-first MGT/SCV
  target from the 2026-06-17 uploaded docs as repo-local product doctrine.
  - Evidence: core-minimum DCP in
    `docs/product/judgment_spine/judgment_level1_product_learning_core_minimum_v0.md`.
  - Consequence: next work must consume the core-minimum route rather than
    returning to the raw temp docs.
- Decision: prompt artifacts remain unedited in this propagation patch.
  - Evidence: core-minimum DCP intentionally-not-updated entries for the two
    older prompt handoff artifacts.
  - Consequence: use `workflow-prompt-orchestrator` for the next prompt work.

## Mutable Questions

- Question: Should the next lane continue from PR #233 before PR #230 and PR
  #233 land?
  - Why still mutable: PR #233 is dependent on `codex/judgement-lane`, not
    `main`.
  - What would resolve it: owner chooses dependent continuation, or waits for
    the PR stack to merge.
- Question: Which durable prompt artifact should be authored first:
  commission-gate prompt or Level 1 judgment prompt?
  - Why still mutable: both are next in the route; prompt-orchestrator should
    bind exact source pack and output mode.
  - What would resolve it: owner chooses sequence or accepts commission-gate
    first as the gate before judgment output.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding:
  `docs/hygiene/judgment_level1_product_learning_core_minimum_handoff_v0.md`
  from commit `dec37f13`.
  - Why stale or dangerous: it predates the post-upload MGT/SCV propagation and
    was deleted as consumed by `e2adb88b`.
  - Current replacement: this packet and PR #233 at or after commit
    `2a125c578cf09a7947b54429de6d3fac511ae3be`.
- Stale instruction, idea, artifact, or finding:
  old outcome-label spellings `review_velocity_sustains_60d`,
  `creator_momentum_persists_30d`, and `search_interest_persists_60d`.
  - Why stale or dangerous: the casebook now canonicalizes the `sustained` and
    `persisted` labels.
  - Current replacement: `review_velocity_sustained_60d`,
    `creator_momentum_persisted_30d`, and `search_interest_persisted_60d`.

## Commands And Verification Evidence

- Command:
  ```powershell
  git status --short --branch
  ```
  Result:
  - Passed.
  - Important output before this file:
    `## codex/judgment-level1-core-minimum...origin/codex/judgment-level1-core-minimum`
  - Re-run target: receiver checks branch and dirty state before acting.
- Command:
  ```powershell
  git rev-parse HEAD
  ```
  Result:
  - Passed.
  - Important output before this file:
    `2a125c578cf09a7947b54429de6d3fac511ae3be`
  - Re-run target: receiver confirms the current PR head or changed head.
- Command:
  ```powershell
  gh pr view 233 --json number,title,body,url,isDraft,state,headRefName,baseRefName
  ```
  Result:
  - Passed after PR body update through the GitHub connector.
  - Important output: PR #233 open draft, title
    `docs: propagate judgment Level 1 backtest core`, head
    `codex/judgment-level1-core-minimum`, base `codex/judgement-lane`.
  - Re-run target: receiver confirms PR metadata before depending on it.
- Command:
  ```powershell
  gh pr checks 233 --watch=false
  ```
  Result:
  - Passed as a status read.
  - Important output after PR update: `orca-harness-tests pass`; `route pass`.
  - Re-run target: receiver checks current PR status before merging or relying
    on green CI.

Validation evidence from the propagation commit:

- `git diff --check`: passed.
- `python .agents/hooks/check_retrieval_header.py --changed --strict`: passed.
- `python .agents/hooks/check_repo_map_freshness.py --changed --strict`: passed.
- `python .agents/hooks/check_placement.py --changed`: passed.
- `python .agents/hooks/header_index.py --strict`: passed.
- staged changed-set checks passed before commit.
- `python .agents/hooks/check_placement.py --staged --strict`: failed on
  pre-existing whole-repo placement debt, not on the changed docs.

## Blockers And Risks

- Blocker or risk: PR stack dependency.
  - Evidence: PR #233 base is `codex/judgement-lane`, not `main`.
  - Likely next action: continue from PR #233 only if owner accepts dependent
    continuation; otherwise wait for PR #230 and PR #233 to land.
- Blocker or risk: prompt artifacts must use prompt-orchestrator.
  - Evidence: Orca prompt-orchestration overlay and core-minimum DCP.
  - Likely next action: invoke `workflow-prompt-orchestrator` before writing
    commission-gate or Level 1 judgment prompt artifacts.
- Blocker or risk: setup docs can be mistaken for run readiness.
  - Evidence: core-minimum and fragrance docs explicitly record non-claims.
  - Likely next action: preserve non-claims in every next artifact.

## Confirm-Don't-Trust Load Checklist

- Load-bearing fact: PR #233 head/base/body/current checks.
  - Compare target: `gh pr view 233` and `gh pr checks 233`.
- Load-bearing fact: branch and workspace state.
  - Compare target: `git status --short --branch` and `git rev-parse HEAD`.
- Load-bearing fact: core-minimum route.
  - Compare target: reread core-minimum doc; expected blob at old head
    `c54578630e5a7bf7989be2206bc036876463e575`.
- Load-bearing fact: prompt-orchestrator ownership.
  - Compare target: reread `.agents/workflow-overlay/prompt-orchestration.md`.
- Load outcomes:
  - `REUSE`: PR #233 and core docs match or only this handoff file was added.
  - `PARTIAL_REUSE`: optional PR check state changed but branch/content still
    matches.
  - `STALE_REREAD_REQUIRED`: PR #233 head, base, or core docs changed.
  - `BLOCKED_DRIFT`: PR #233 no longer depends on the expected branch stack or
    current user redirects scope.
  - `BLOCKED_MISSING_PACKET`: this file is absent or unreadable.

## Do Not Forget

- PR first is done by PR #233 metadata update; do not open a duplicate PR.
- The next useful lane is prompt-orchestrated commission gate / Level 1 judgment
  prompt scaffolding, not case running.
- The old handoff path was consumed and deleted; relaunch from this packet if it
  is committed into PR #233.
