# Social Capture Browser Calibration Lane Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet (durable continuation artifact; NOT validation/readiness/governance)
scope: >
  Transfers the social capture browser-behavior calibration lane after the
  Capture core migration planning/execution loop, so a fresh lane can reverify
  current repo state, port the existing calibration prompt to the landed
  capture/core structure, and continue only the planning/architecture work.
use_when:
  - Resuming the IG-first social browser-behavior calibration prompt after Capture core migration.
  - Reconstructing why the existing calibration prompt is stale against current Capture placement.
  - Starting a fresh worktree to port and then run the calibration commission.
authority_boundary: retrieval_only
```

## Load Contract

- packet_version: `workflow-handoff/max/v0`
- mode: max
- created_at: `2026-06-21T15:03:41.4798408+08:00`
- created_by_lane: Codex current thread; provenance only, not authority.
- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- handoff_path: `docs/hygiene/social_capture_browser_calibration_lane_handoff_v0.md`
- expected_branch: local root worktree observed on `main`
- expected_head: local root worktree observed at `35066b15`
- expected_dirty_state_including_handoff_file: after write, expect the pre-existing unrelated dirty state plus `?? docs/hygiene/social_capture_browser_calibration_lane_handoff_v0.md`.
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting. Sender claims are hypotheses, not authority.

## Current Supersession Addendum - IG Reels DOM Timestamp Join (2026-06-22)

Current owner direction supersedes this packet's older prompt-port-only active objective for this
lane. Treat the older objective as provenance and re-confirm every claim below against current
sources before implementing.

### Superseded Active Objective

The next lane is no longer "port the existing browser-behavior calibration prompt, then run a
planning-only architecture commission" by default. The current lane is an IG-only continuation of
the profile-grid engagement route:

- default surface: public Instagram creator `/reels/` grid, not the profile main grid;
- default extraction: no-hover media-anchor DOM records keyed by `shortcode` or permalink path;
- default engagement fields: rendered views text plus hidden no-hover like/comment text when present;
- default timestamp source: profile-feed JSON joined by `shortcode`, not grid DOM date text;
- default posture: diagnostic/scoping until a later explicit runner build is authorized.

### Timestamp Contract

Do not assume grid DOM carries reliable post dates. The current no-hover grid finding only supports
engagement extraction from media-anchor DOM. Dates should come from profile-feed JSON:

- `web_profile_info` first page and grid cursor JSON can expose media nodes keyed by `shortcode`;
- existing harness code already parses `taken_at_timestamp` from media JSON nodes;
- join DOM engagement observations to JSON metadata by `shortcode` or permalink-derived shortcode;
- if JSON timestamps are unavailable, clicking latest / 5th / 10th items may calibrate approximate
  visible-grid coverage, but must not assign exact dates to all grid rows or extrapolate a 30-day
  window from grid index.

Minimum output extension for the grid observation shape:

```yaml
media_observation:
  shortcode:
  permalink_path:
  views_text:
  likes_text:
  comments_text:
  taken_at_timestamp: null        # fill only from JSON/profile-feed or item-page evidence
  timestamp_source: none | profile_feed_json | item_page | unknown
  timestamp_join_status: joined_by_shortcode | missing_json | missing_shortcode | ambiguous | not_attempted
```

### Route Defaults And Stops

- Prefer `/reels/` over the main profile grid while static-post behavior remains unverified.
- Known-good diagnostic viewport is `768x1024`; test `1080x1920` portrait next. Treat
  `1920x1080`, `1280x1200`, and `1440x2200` as calibration variants, not proof that larger
  viewports are better.
- Wait for a media-anchor selector before extracting. Zero anchors is a route/access/layout failure
  or variant to report, not a successful empty capture.
- Record route context honestly: existing Chrome diagnostic, headed logged-out browser, logged-out
  proxy, runner packet, or sessioned route must not be collapsed into one generic label.
- Stop on visible login redirect, interstitial/block shell, suspicious-behavior notice, repeated
  zero-anchor parse, or hidden-number ambiguity that prevents mapping likes/comments.

### Packet Use

Keep using a packet only as a recoverable handoff/source-quality control. Diagnostic `_test_runs`
outputs are evidence, not Source Capture Packets or validation records. Refresh this handoff in
place if needed; do not accumulate `_v2` copies. A later runner implementation or reviewed capture
spec should supersede this addendum.

### Explicit Non-Goals

- No anti-detect, stealth, browser-fingerprint bypass, CAPTCHA/password automation, cookie export,
  raw storage-state handling, raw proxy secrets, or exit-IP recording.
- No claim that this route lowers detection risk; it only removes unnecessary hover/click/OCR work.
- No comment text capture, bot/paid-comment classification, TikTok/YouTube expansion, or static-post
  assumption without a separate static grid probe.

## Goal Handoff

- long_term_goal: Durable, source-bounded social capture planning that improves IG capture run shape without hiding block/culling evidence or generalizing to TikTok/YouTube without source evidence.
- anchor_goal: Port the existing social browser-behavior calibration prompt to the Capture core structure and then run the architecture/calibration commission from a clean, current worktree.
- success_signal: A fresh lane can verify the merged `capture/core/` layout, update the prompt paths and output destinations, and produce or commission exactly one non-authorizing recommendation artifact without runtime edits or live social-platform capture.

## Open Decision / Fork

- decision: How to continue the stale prompt after the Capture core migration.
  - options:
    - Refresh/fetch current `main`, create a clean worktree, and port the existing prompt onto the merged `capture/core/` layout.
    - Reuse the existing `codex/social-capture-browser-calibration-prompt` worktree after rebasing/merging current `main`.
    - Do not port yet; first reverify whether PR #316 and `capture/core/` are actually present in the receiver's current local repo.
  - already constrained / off the table:
    - Do not edit the dirty root worktree for this lane.
    - Do not run live IG, TikTok, or YouTube capture.
    - Do not implement runtime browser automation, anti-detect tooling, proxies, scraper APIs, credential flows, or stealth recipes.
    - Do not treat TikTok or YouTube as equivalent to IG without current Orca source evidence.
  - trade-offs:
    - Fresh worktree off fetched current `main` avoids carrying old branch assumptions and unrelated root dirt.
    - Reusing the existing prompt branch preserves prompt history but starts from a stale path model and must be rebased/merged before edits.
    - Blocking until fetch/reverify costs a small step but prevents writing a prompt against a locally absent `capture/core/` tree.
  - owner of the call: receiving Chief Architect/operator, after local source refresh. The owner can redirect.
  - recommendation and why: use a fresh clean worktree off fetched current `main`; keep the old prompt branch as source material only. This is the least ambiguous continuation because local root currently lacks the migration merge while the calibration prompt branch is pre-migration.

## Drift Guard

- invariant, non-goal, or scope boundary: This handoff is a checkpoint artifact under `docs/hygiene/`, not source authority.
  - why it matters: Orca overlay says checkpoint artifacts are convenience copies and single-consumption.
  - what violating it would break: A receiver could treat stale local or prior-thread claims as authoritative instead of re-reading current sources.
- invariant, non-goal, or scope boundary: The next work is prompt/docs planning only.
  - why it matters: Orca default allowed work covers docs, decisions, prompts, reviews, migration notes, and overlay maintenance; implementation/runtime work needs explicit bounded authorization.
  - what violating it would break: It would turn a planning lane into source access/runtime automation without owner authorization.
- invariant, non-goal, or scope boundary: Browser-behavior calibration must preserve visible failure and block/culling evidence.
  - why it matters: The existing prompt requires no fake success and no hiding empty payloads, redirects, culling, or blocks.
  - what violating it would break: It would compromise downstream evidence and source-access boundaries.
- invariant, non-goal, or scope boundary: Do not generalize IG thresholds or routes to TikTok/YouTube without Orca source-family recon.
  - why it matters: The existing prompt treats cross-platform sharing as a hypothesis only.
  - what violating it would break: It would erase platform-specific evidence gates and create unsupported source-access assumptions.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`; load it fresh before strict/actionable source claims.
- targets to enter the ladder:
  - `AGENTS.md`
  - `.agents/workflow-overlay/README.md`
  - `.agents/workflow-overlay/source-of-truth.md`
  - `.agents/workflow-overlay/artifact-folders.md`
  - `.agents/workflow-overlay/prompt-orchestration.md`
  - `.codex/worktrees/social-capture-browser-calibration-prompt/docs/prompts/architecture/social_capture_browser_behavior_calibration_prompt_v0.md`
  - `.codex/worktrees/capture-spine-core-migration-plan/docs/decisions/orca_spine_first_target_structure_binding_v0.md`
  - `.codex/worktrees/capture-spine-core-migration-plan/docs/review-outputs/adversarial-artifact-reviews/capture_spine_core_migration_adversarial_artifact_review_v0.md`
  - current repo `orca/product/spines/capture/` on the receiver's local branch after fetch/update.
- already loaded (weak orientation, freshness-marked; not authority):
  - `workflow-handoff` skill loaded from `C:\Users\vmon7\.codex\skills\workflow-handoff\SKILL.md` during this turn.
  - Orca overlay entrypoint and checkpoint rule loaded from `.agents/workflow-overlay/README.md` and `.agents/workflow-overlay/source-of-truth.md`.
  - Existing social calibration prompt loaded from the old prompt worktree at `3b4fa17e`.
  - Capture migration worktree checked at `5419e956`.
- must load first (before strict or actionable steps):
  - Refresh current local repo state and verify whether the receiver's `main` contains the Capture core migration.
  - Re-read the prompt to be ported from the chosen worktree/branch after it is created or updated.
  - Re-read the Capture core placement authority from the receiver's current branch, not from this handoff.
- load rule: receiver re-runs progressive source loading per overlay; the packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- decision, framing, profile, or convention: Capture current files are intended to live under `orca/product/spines/capture/core/`, with IG under `core/source_families/social_media/instagram/`.
  - decided in: `.codex/worktrees/capture-spine-core-migration-plan/docs/decisions/orca_spine_first_target_structure_binding_v0.md`
  - compare target: SHA256 `0F6C3AF13FD892EA4136F7BA088EB6F009A7E6E9A2391B5CA996E57FEBAD2B60`; excerpt lines 79-86 in that file name the `capture/core/` re-home and state that TikTok, YouTube, web-search capture, source-quality extraction, cadence/missingness folders, harness/runtime work, and source-access authorization were not created.
  - verify before: any prompt path rewrite or placement claim.
- decision, framing, profile, or convention: The existing browser calibration prompt is an IG-first architecture/calibration commission, not a live-run or implementation authorization.
  - decided in: `.codex/worktrees/social-capture-browser-calibration-prompt/docs/prompts/architecture/social_capture_browser_behavior_calibration_prompt_v0.md`
  - compare target: SHA256 `7E6F4672AF83FB6893C48980B4A82C0D43E95810B81A897EFB55A9C9D1B22390`; prompt lines 156-177 list planning-only boundaries and prohibited runtime/source-access actions.
  - verify before: executing or editing the prompt.
- decision, framing, profile, or convention: Cold handoff packets are non-authoritative, single-consumption checkpoint artifacts.
  - decided in: `.agents/workflow-overlay/source-of-truth.md`
  - compare target: SHA256 `04DAF7979FDA605A2E7CF334DBC7ECADB02F8C1F1B40A432E14B4F3503235D0C`; lines 30-55 bind checkpoint artifact lifecycle and distinguish them from handoff prompts.
  - verify before: treating this packet as usable.

## Active Objective

Transfer enough state for a fresh lane to continue the social capture browser-behavior calibration work after the Capture core migration, without trusting stale branch paths or prior-thread memory. The next concrete work is to port the existing prompt from old Capture paths to the current `capture/core/` structure, then run or commission the planning-only architecture/calibration analysis.

## Exact Next Authorized Action

1. Refresh/fetch current repo state, then verify whether `main` or `origin/main` contains the Capture core migration. Re-run `git status --short --branch`, `git rev-parse --short HEAD`, and path checks for `orca/product/spines/capture/core/source_families/social_media/instagram/README.md` and `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`.
2. Create a clean worktree/branch off the verified current `main` for the prompt port. Do not edit the dirty root worktree.
3. Port the existing prompt at `docs/prompts/architecture/social_capture_browser_behavior_calibration_prompt_v0.md` by changing old Capture paths to the current core layout:
   - IG required reads and IG-only output: `orca/product/spines/capture/core/source_families/social_media/instagram/...`
   - shared toolbox reads and shared/recon-first outputs: `orca/product/spines/capture/core/source_capture_toolbox/...`
   - source-access boundary: `orca/product/spines/capture/core/contracts/source_access_boundary/...`
   - target dirs/preflight/open_next/stale_if/branch_or_commit references: refresh to the new branch and current source state.
4. Validate the prompt port with at least `rg -n "orca/product/spines/capture/(source_families|source_capture_toolbox|contracts)" docs/prompts/architecture/social_capture_browser_behavior_calibration_prompt_v0.md`, `python .agents/hooks/check_retrieval_header.py --strict docs/prompts/architecture/social_capture_browser_behavior_calibration_prompt_v0.md`, and `git diff --check`.
5. Only after the prompt paths are current, run the architecture/calibration commission or hand it to a fresh CA lane with its source-loading contract intact.

## Authority And Source Ledger

- Repository instructions:
  - `AGENTS.md`
    - Role: Orca project behavior kernel and authorization boundaries.
    - Load-bearing: yes
    - Compare target: SHA256 `4296E7617D8B2675881780CD7BE0704A00DCB17ADF7758243008DE956070940B`
    - Last checked: `2026-06-21T15:03:41+08:00`
    - Reuse rule: reread before asserting authorization, dirty-worktree policy, or validation/reporting duties.
- Overlay or equivalent authority:
  - `.agents/workflow-overlay/source-of-truth.md`
    - Role: Orca source hierarchy and checkpoint lifecycle.
    - Load-bearing: yes
    - Compare target: SHA256 `04DAF7979FDA605A2E7CF334DBC7ECADB02F8C1F1B40A432E14B4F3503235D0C`
    - Last checked: `2026-06-21T15:03:41+08:00`
    - Reuse rule: reread before relying on this checkpoint or source precedence.
  - `.agents/workflow-overlay/artifact-folders.md`
    - Role: durable artifact placement.
    - Load-bearing: yes
    - Compare target: SHA256 `42D4F554DAF4BE6F0A4A9BCBE3C67FD74EEFCC063FC72B03E53E11242EDC7AE9`
    - Last checked: `2026-06-21T15:03:41+08:00`
    - Reuse rule: reread before writing a new artifact path.
  - `.agents/workflow-overlay/prompt-orchestration.md`
    - Role: prompt artifact contract and cross-lane/durable prompt rules.
    - Load-bearing: yes
    - Compare target: SHA256 `64740C756AEC4A19F5218BCF275E05328B15B82AB62F08D9D977BB89CF849EE5`
    - Last checked: `2026-06-21T15:03:41+08:00`
    - Reuse rule: reread before authoring or using a cross-lane prompt.
  - `docs/workflows/orca_repo_map_v0.md`
    - Role: repo navigation and hygiene placement context.
    - Load-bearing: no
    - Compare target: SHA256 `05C3F9E5C836806801A4BD09903FCF11501F9D0460CB034364D9C523C78B1EDD`
    - Last checked: `2026-06-21T15:03:41+08:00`
    - Reuse rule: advisory navigation only; reread when routing by repo map.
- User constraints:
  - Current user explicitly invoked `workflow-handoff`.
  - Prior user direction renamed `social_video` to `social_media`.
  - Prior user accepted the recommendation to avoid risky stealth/runtime actions and to prefer low-cost, durable, non-authorizing planning/doc controls.
  - Load-bearing: yes for current lane boundaries; compare target: current conversation plus this handoff, `reread-required` if the receiver lacks the chat context.
- Source-read ledger:
  - `.codex/worktrees/social-capture-browser-calibration-prompt/docs/prompts/architecture/social_capture_browser_behavior_calibration_prompt_v0.md`
    - Role: existing stale prompt to port.
    - Load-bearing: yes
    - Compare target: branch `codex/social-capture-browser-calibration-prompt` at `3b4fa17e33716ff33cbf67e6b8a6080923682471`; SHA256 `7E6F4672AF83FB6893C48980B4A82C0D43E95810B81A897EFB55A9C9D1B22390`.
    - Last checked: `2026-06-21T15:03:41+08:00`
    - Reuse rule: reread after branch update; treat old paths as stale unless current branch still uses pre-core Capture.
  - `.codex/worktrees/capture-spine-core-migration-plan/docs/decisions/orca_spine_first_target_structure_binding_v0.md`
    - Role: Capture core placement authority in migration worktree.
    - Load-bearing: yes, but only after receiver verifies it is on current main/origin.
    - Compare target: worktree branch `codex/capture-spine-core-migration-plan` at `5419e9560b5731962752154a5f7075e5fe0712ca`; SHA256 `0F6C3AF13FD892EA4136F7BA088EB6F009A7E6E9A2391B5CA996E57FEBAD2B60`.
    - Last checked: `2026-06-21T15:03:41+08:00`
    - Reuse rule: use as compare target only; reverify from current `main` after fetch before acting.
  - `.codex/worktrees/capture-spine-core-migration-plan/docs/review-outputs/adversarial-artifact-reviews/capture_spine_core_migration_adversarial_artifact_review_v0.md`
    - Role: prior delegated review report for migration.
    - Load-bearing: no for prompt port; useful context for migration friction.
    - Compare target: branch `codex/capture-spine-core-migration-plan` at `5419e9560b5731962752154a5f7075e5fe0712ca`; excerpt lines 38-41 say `recommendation: accept_with_friction`, `findings_count: 3`, `blocking_findings: []`, `advisory_findings: [AR-01, AR-02, AR-03]`.
    - Last checked: `2026-06-21T15:03:41+08:00`
    - Reuse rule: reread only if review/adjudication affects the next step.
  - Local root worktree state
    - Role: current workspace state at packet creation.
    - Load-bearing: yes for dirty-state and stale-main warning.
    - Compare target: `git status --short --branch` output observed pre-write with `## main...origin/main`, one modified handoff file, six untracked paths, and warning `could not open directory 'orca-harness/.pytest_tmp/': Permission denied`; `git rev-parse --short HEAD` observed `35066b15`.
    - Last checked: `2026-06-21T15:03:41+08:00`
    - Reuse rule: rerun before any edit; drift is expected if the receiver fetches current main.
- Source gaps:
  - PR #316 merge state was reported in prior-thread evidence, but this local root cannot see merge commit `2988c82f54dc0aa1ed3ed5968d7658a563b28228`; receiver must verify via fetch or GitHub before claiming the migration is on current main.
  - This packet did not source-load TikTok or YouTube capture artifacts; the calibration commission must search/reverify them.
- Strict-only blockers:
  - Do not make a strict "migration is on local main" claim until local fetch/current-main verification confirms it.
  - Do not execute the old prompt unchanged because its paths are pre-core.
- Not-proven boundaries:
  - No live IG/TikTok/YT durability improvement is proven.
  - No source-access authorization changed.
  - No runtime implementation authorization exists.
  - No TikTok/YouTube source-family parity exists.

## Current Task State

- Completed:
  - Existing social browser-behavior calibration prompt located and read from `codex/social-capture-browser-calibration-prompt` at `3b4fa17e`.
  - Capture migration worktree at `5419e956` verified to contain `orca/product/spines/capture/core/source_families/social_media/instagram/README.md` and `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`.
  - Local root verified to still have pre-core Capture paths and no local object for merge commit `2988c82f54dc0aa1ed3ed5968d7658a563b28228`.
- Partially completed:
  - Reorientation back to the browser calibration lane is done as conversation state, but no prompt port has been written.
  - Capture core migration was previously reported merged, but current local root requires fetch/reverification before the receiver relies on it.
- Broken or uncertain:
  - Local root `main` is stale relative to the intended post-migration state.
  - Existing prompt uses old paths in `open_next`, preflight `target_files_or_dirs`, required reads, output artifacts, and `branch_or_commit`.

## Workspace State

- Branch: local root `main`
- Head: `35066b15`
- Dirty or untracked state before handoff:
  ```text
  ## main...origin/main
   M docs/hygiene/ig_creator_momentum_lane_handoff_v0.md
  ?? .codex/hooks/run_orca_guard.py
  ?? _scratch/
  ?? docs/hygiene/cleaning_spine_lane_handoff_v0.md
  ?? docs/hygiene/commission_signal_board_lane_handoff_v0.md
  ?? docs/prompts/product-planning/orca_spine_first_target_structure_controller_prompt_v0.md
  ?? docs/workflows/data_lake_r2_continuation_handoff_v0.md
  warning: could not open directory 'orca-harness/.pytest_tmp/': Permission denied
  ```
- Dirty or untracked state after writing the handoff file:
  ```text
  Expected addition:
  ?? docs/hygiene/social_capture_browser_calibration_lane_handoff_v0.md

  All pre-existing dirty/untracked entries above are unrelated and must not be touched by this lane.
  ```
- Target files or artifacts:
  - Prompt to port: `docs/prompts/architecture/social_capture_browser_behavior_calibration_prompt_v0.md` in the chosen fresh worktree.
  - Existing source prompt reference: `.codex/worktrees/social-capture-browser-calibration-prompt/docs/prompts/architecture/social_capture_browser_behavior_calibration_prompt_v0.md`.
  - Expected IG-only output after prompt port: `orca/product/spines/capture/core/source_families/social_media/instagram/ig_browser_behavior_calibration_change_set_v0.md`.
  - Expected shared-controller output after prompt port: `orca/product/spines/capture/core/source_capture_toolbox/social_browser_behavior_calibration_architecture_v0.md`.
  - Expected recon-first output after prompt port: `orca/product/spines/capture/core/source_capture_toolbox/social_browser_behavior_recon_first_calibration_note_v0.md`.
- Related worktrees or branches:
  - `.codex/worktrees/social-capture-browser-calibration-prompt` on `codex/social-capture-browser-calibration-prompt` at `3b4fa17e`; clean status observed.
  - `.codex/worktrees/capture-spine-core-migration-plan` on `codex/capture-spine-core-migration-plan` at `5419e956`; clean status observed.

## Changed / Inspected / Tested Files

- `docs/hygiene/social_capture_browser_calibration_lane_handoff_v0.md`
  - Status: newly created untracked checkpoint packet.
  - Role: cold-reader handoff; non-authoritative, single-consumption.
  - Important observations: records local stale-main drift and exact next action.
  - Symbols or sections: all `workflow-handoff/max/v0` sections present.
- `.codex/worktrees/social-capture-browser-calibration-prompt/docs/prompts/architecture/social_capture_browser_behavior_calibration_prompt_v0.md`
  - Status: inspected only.
  - Role: existing prompt to port.
  - Important observations: uses old `orca/product/spines/capture/source_families/instagram/` and `orca/product/spines/capture/source_capture_toolbox/` paths; output paths likewise pre-core.
  - Symbols or sections: retrieval header, Preflight, Required Reads, Boundaries, Required Output Artifact.
- `.codex/worktrees/capture-spine-core-migration-plan/docs/decisions/orca_spine_first_target_structure_binding_v0.md`
  - Status: inspected only.
  - Role: placement decision/compare target for Capture core migration.
  - Important observations: lines 79-86 and 431-436 define the current intended `capture/core/` re-home in that worktree.
  - Symbols or sections: post-execution Capture amendment and direction-change propagation.
- `.agents/workflow-overlay/source-of-truth.md`
  - Status: inspected only.
  - Role: checkpoint lifecycle and source hierarchy.
  - Important observations: lines 30-55 bind `workflow-handoff` packets as non-authoritative checkpoint artifacts.
  - Symbols or sections: Checkpoint Artifacts.

## Frozen Decisions

- Decision: Use `social_media`, not `social_video`, for the source-family grouping.
  - Evidence: user explicitly corrected the grouping before migration planning.
  - Consequence: IG belongs under `capture/core/source_families/social_media/instagram/` after the migration.
- Decision: The browser calibration lane remains planning/docs only.
  - Evidence: existing prompt lines 156-177 and current user sequence accepted recommendation against risky stealth/runtime implementation.
  - Consequence: no live capture, browser automation install, credentials, proxies, anti-detect tooling, scraper API, production worker, or code patch in this lane.
- Decision: The prompt must be ported before execution.
  - Evidence: existing prompt required reads and outputs point to old pre-core paths; local root currently lacks `capture/core/`, while migration worktree has it.
  - Consequence: executing the prompt unchanged would route a fresh CA to stale paths.

## Mutable Questions

- Question: Is PR #316 now present in the receiver's local `main` or `origin/main`?
  - Why still mutable: current local root cannot see merge commit `2988c82f54dc0aa1ed3ed5968d7658a563b28228` and still has old Capture paths.
  - What would resolve it: `git fetch origin` or equivalent, then verify branch head and `capture/core/` paths.
- Question: Should the port reuse the existing prompt branch or start from a fresh branch?
  - Why still mutable: existing branch preserves prompt history but is pre-migration; fresh branch avoids stale base.
  - What would resolve it: receiver's isolation decision after fetch. Recommended default is fresh worktree off fetched current main.
- Question: If the recommendation is a shared social browser controller, should the output live under `core/source_capture_toolbox/` or a future parent `core/source_families/social_media/` index?
  - Why still mutable: original prompt placed shared controller outputs in `source_capture_toolbox`; migration created an IG family under `social_media/` but did not create a populated shared social-media parent artifact.
  - What would resolve it: bounded source-load of current placement rules. Recommended default for the prompt port is to preserve original output-home intent and only insert `core/`.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: Existing prompt path model under `orca/product/spines/capture/source_families/instagram/` and `orca/product/spines/capture/source_capture_toolbox/`.
  - Why stale or dangerous: Capture current files were re-homed under `capture/core/` in the migration worktree, and user moved to the core/satellite migration plan before returning to calibration.
  - Current replacement: `orca/product/spines/capture/core/source_families/social_media/instagram/` for IG; `orca/product/spines/capture/core/source_capture_toolbox/` for shared toolbox; verify against current main after fetch.
- Stale instruction, idea, artifact, or finding: Treating prior chat's "PR #316 merged" statement as sufficient proof in local disk.
  - Why stale or dangerous: local root cannot see the merge commit or core paths at packet creation.
  - Current replacement: fetch/reverify before strict claims.
- Stale instruction, idea, artifact, or finding: Generalizing TLS/JA4/fingerprint or behavioral stealth advice into implementation.
  - Why stale or dangerous: Orca lane is planning-only and source-access constrained; stealth recipes or anti-detect implementation are out of scope.
  - Current replacement: architecture-level, non-executing recommendation only; preserve culling/block evidence and owner gates.

## Commands And Verification Evidence

- Command:
  ```powershell
  git status --short --branch
  ```
  Result:
  - Passed/failed/not run: passed with warning.
  - Important output: local root on `main`; dirty/untracked entries listed in `Workspace State`; warning for `orca-harness/.pytest_tmp/` permission denied.
  - Re-run target so the receiver can confirm rather than trust: rerun in `C:\Users\vmon7\Desktop\projects\orca` before any edits.
- Command:
  ```powershell
  git rev-parse --short HEAD
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: `35066b15`.
  - Re-run target so the receiver can confirm rather than trust: rerun after fetch/update.
- Command:
  ```powershell
  Test-Path -LiteralPath 'orca\product\spines\capture\core\source_families\social_media\instagram\README.md'
  Test-Path -LiteralPath 'orca\product\spines\capture\source_families\instagram\ig_at_scale_operating_envelope_v0.md'
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: `False` for current local `capture/core` IG README; `True` for old pre-core IG path.
  - Re-run target so the receiver can confirm rather than trust: rerun after fetch/update.
- Command:
  ```powershell
  git -C .codex\worktrees\social-capture-browser-calibration-prompt status --short --branch
  git -C .codex\worktrees\social-capture-browser-calibration-prompt rev-parse --short HEAD
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: `## codex/social-capture-browser-calibration-prompt...origin/codex/social-capture-browser-calibration-prompt`; `3b4fa17e`.
  - Re-run target so the receiver can confirm rather than trust: rerun before using old prompt branch.
- Command:
  ```powershell
  git -C .codex\worktrees\capture-spine-core-migration-plan status --short --branch
  git -C .codex\worktrees\capture-spine-core-migration-plan rev-parse --short HEAD
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: `## codex/capture-spine-core-migration-plan...origin/codex/capture-spine-core-migration-plan`; `5419e956`.
  - Re-run target so the receiver can confirm rather than trust: rerun if using the migration worktree as compare target.
- Command:
  ```powershell
  python .agents\hooks\check_retrieval_header.py --help
  python .agents\hooks\check_map_links.py --help
  ```
  Result:
  - Passed/failed/not run: retrieval-header help passed; map-links help returned usage with exit code 1.
  - Important output: retrieval checker supports `--strict <paths>`; map-links supports `--strict`, `--strict-inline`, `--check`, `--report-orca`, `--selftest`.
  - Re-run target so the receiver can confirm rather than trust: rerun before choosing validation commands.

## Blockers And Risks

- Blocker or risk: Local root is stale relative to the intended post-migration capture-core shape.
  - Evidence: local root head `35066b15`; `capture/core/.../instagram/README.md` absent; old IG path present; merge commit `2988c82f54dc0aa1ed3ed5968d7658a563b28228` is not a local object.
  - Likely next action: fetch/update and reverify before edits.
- Blocker or risk: Existing prompt would route a receiver to old paths.
  - Evidence: prompt lines 16-20, 74-78, 112-129, and 233-239 name old `capture/source_families`, `capture/source_capture_toolbox`, and `capture/contracts` locations.
  - Likely next action: port prompt paths before executing commission.
- Blocker or risk: Unrelated root dirty state could be overwritten or mixed into this lane.
  - Evidence: root status lists unrelated modified and untracked docs/hooks/scratch paths.
  - Likely next action: use a clean worktree off fetched current main.
- Blocker or risk: Shared-controller recommendation could exceed source evidence.
  - Evidence: existing prompt explicitly says TikTok/YouTube generalization is source-gated and recon-first if unsupported.
  - Likely next action: keep shared primitives conceptual and platform thresholds/profile routes source-specific.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - Current branch/head and dirty state of the chosen worktree.
  - Whether current `main` or `origin/main` contains the Capture core migration.
  - Existing prompt content and old-path hits.
  - Capture core placement authority and actual disk paths on the current branch.
  - Prompt-orchestration rules before writing or handing off a cross-lane prompt.
- Compare target for each:
  - Branch/head: rerun `git status --short --branch` and `git rev-parse --short HEAD`.
  - Capture core: disk path checks plus current-branch source reads, not only this packet.
  - Existing prompt: branch `3b4fa17e33716ff33cbf67e6b8a6080923682471`, SHA256 `7E6F4672AF83FB6893C48980B4A82C0D43E95810B81A897EFB55A9C9D1B22390`, or the receiver's updated prompt branch after rebase.
  - Capture migration decision: branch `5419e9560b5731962752154a5f7075e5fe0712ca`, SHA256 `0F6C3AF13FD892EA4136F7BA088EB6F009A7E6E9A2391B5CA996E57FEBAD2B60`, then reverify from current main after fetch.
  - Prompt rules: `.agents/workflow-overlay/prompt-orchestration.md` SHA256 `64740C756AEC4A19F5218BCF275E05328B15B82AB62F08D9D977BB89CF849EE5`.
- Load outcomes and what each means:
  - `REUSE`: all required facts reverified and current `capture/core/` exists on the receiver's chosen branch; continue with prompt port.
  - `PARTIAL_REUSE`: optional review context or advisory hashes drifted, but current prompt and Capture core placement reverified; continue after rereading drifted advisory sources if needed.
  - `STALE_REREAD_REQUIRED`: branch/head or core paths drifted but can be re-derived by fetch/source reads; re-read before acting.
  - `BLOCKED_DRIFT`: dirty state, source authority, or placement conflicts make the target worktree unsafe.
  - `BLOCKED_MISSING_PACKET`: this file is absent or unreadable.
  - `BLOCKED_UNVERIFIABLE`: a load-bearing claim cannot be checked from available repo/filesystem/GitHub state; stop and request source capsule or owner direction.
- Sources that must be reread if drift is detected:
  - `AGENTS.md`
  - `.agents/workflow-overlay/source-of-truth.md`
  - `.agents/workflow-overlay/prompt-orchestration.md`
  - current-branch Capture placement decision and repo map
  - current-branch social calibration prompt after port/rebase

## Do Not Forget

- The next lane is not "calibrate IG live"; it is "make the prompt current and run planning-only architecture/calibration."
- The local root currently contradicts the prior merged-migration story on disk; fetch/reverify is the first real action.
- Consume and delete or refresh this checkpoint after the receiver re-establishes live state; do not accumulate a `_v2` copy.
