# Handoff Packet

```yaml
retrieval_header_version: 1
artifact_role: Handoff packet
scope: Creator registry folder move handoff preserving PR conflict and stale open_next remediation context.
use_when:
  - Resuming or auditing the creator registry folder move handoff packet.
  - Diagnosing PR conflict or stale retrieval-link fallout from the creator registry folder move.
  - Checking why creator-registry follow-up work should continue from the main-compatible branch.
authority_boundary: retrieval_only
```

## Load Contract

- packet_version: workflow-handoff max v0
- mode: max
- created_at: 2026-06-29T23:35:08.6742136+08:00
- created_by_lane: Codex desktop thread in `C:\Users\vmon7\Desktop\projects\orca`; provenance only, not authority.
- workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-registry-folder-main`
- handoff_path: `C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-registry-folder-main\docs\hygiene\creator_registry_folder_handoff_v0.md`
- expected_branch: `codex/creator-registry-folder-main`
- expected_head: `217b46ca4a38393080679d3fd1e73d4f796707a9`
- expected_dirty_state_including_handoff_file: before writing this packet, `git status --short --branch` in the handoff workspace was clean against `origin/codex/creator-registry-folder-main`; after writing, expect this handoff file to be untracked unless a sender later commits it.
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: "Build Orca's creator intelligence layer as a one-stop creator profile surface over identity, platform accounts, target audience, discovery/capture status, and aggregate influence metrics."
- anchor_goal: "Make the creator ledger/registry source-backed and lake-aware: ledger owns identity/handle graph, metrics derive from Silver/data-lake records, and capture/discovery can check/update creator status without duplicate discovery."
- success_signal:
  - core_success:
    - owner_observable: "A creator-facing registry/profile surface shows who the creator is, active platforms, evidence pointers, freshness/discovery state, and aggregate influence."
    - output_fit: "Future outputs make the ledger more automatically maintained from capture/lake data rather than manually stale."
    - boundary: "Not one giant ledger doc, not SQLite/dashboard for its own sake, and not treating derived profile metrics as raw source truth."
    - drift_cue: "Work is drifting if it optimizes IG projection/capture plumbing without improving creator-profile usefulness."
  - secondary_success_signals:
    - "Discovery checks the creator graph before proposing creators."
    - "Capture freshness/status is visible per platform account."
    - "Aggregate metrics update as more reels/shorts land."

## Open Decision / Fork

- decision: How should the receiver finish PR #469 after the creator registry folder move caused CI retrieval-link failures?
  - options:
    - Patch the 15 stale `open_next` paths reported by `check_map_links --strict` to point at `.../social_media/creator_registry/...`. This is the recommended path.
    - Annotate some historical `open_next` entries as `# nonresolving:` if the receiver proves they are intentionally point-in-time and should not resolve. Use sparingly; `open_next` is normally live retrieval metadata.
    - Revert the folder move to restore old flat paths. Downgraded: it loses the user-requested real folder placement and leaves the ledger shape ambiguous.
  - already constrained / off the table:
    - Do not merge or mark PR #469 ready while CI is red.
    - Do not bypass link checks or treat the handoff packet as validation evidence.
    - Do not move platform metric seeds into `creator_registry/`; metric seeds stay in `youtube/` and `instagram/` as platform metric/rollup inputs.
    - Do not introduce SQLite, dashboard code, live capture, or cross-platform creator identity promotion in this lane.
  - trade-offs:
    - Updating stale `open_next` paths is more mechanical but resolves CI and keeps retrieval metadata live.
    - Annotating nonresolving can preserve historical context but risks normalizing dead retrieval paths if overused.
    - Reverting avoids link churn but breaks the owner-approved placement direction.
  - owner of the call: current user / Orca owner for any scope expansion; receiver may execute the smallest complete CI fix on PR #469 without asking again.
  - recommendation and why: patch the 15 stale `open_next` path failures, rerun strict link check and focused tests, commit, and push to PR #469.

## Drift Guard

- invariant, non-goal, or scope boundary: The creator registry is source of truth for known public platform accounts, handles, and linkage states, not for metrics, audience facts, contactability, buyer proof, or raw capture.
  - why it matters: collapsing facts into the registry would recreate the "one giant ledger" shape the owner rejected.
  - what violating it would break: metric/source truth would become ambiguous and future Silver/data-lake derivation would be harder.
- invariant, non-goal, or scope boundary: Continue on the lane named here: PR #469 / `codex/creator-registry-folder-main`.
  - why it matters: root workspace `C:\Users\vmon7\Desktop\projects\orca` is still on stale branch `codex/ig-reels-capture-spine` at `63694997`; it is not the correct edit base.
  - what violating it would break: edits could land on the obsolete #464 branch or mix with unrelated root untracked files.
- invariant, non-goal, or scope boundary: Do not reuse the older local branch `codex/creator-registry-folder` as active truth.
  - why it matters: it was stale and would drag unrelated deletions/data-lake changes over current `main`.
  - what violating it would break: PR #469's clean one-commit shape and current main compatibility.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- targets to enter the ladder:
  - `AGENTS.md`
  - `.agents/workflow-overlay/README.md`
  - `.agents/workflow-overlay/artifact-folders.md`
  - `.agents/workflow-overlay/source-loading.md`
  - PR #469 state on GitHub
  - branch/worktree state for `C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-registry-folder-main`
  - `python .agents/hooks/check_map_links.py --strict`
- already loaded (weak orientation, freshness-marked; not authority):
  - `workflow-handoff` skill from `C:\Users\vmon7\.codex\skills\workflow-handoff\SKILL.md`, read 2026-06-29T23:35+08.
  - Orca overlay artifact and source-loading rules, read 2026-06-29T23:35+08.
  - PR #469 and CI state, read 2026-06-29T23:35+08.
- must load first (before strict or actionable steps):
  - `AGENTS.md` and `.agents/workflow-overlay/README.md` if not already loaded in the fresh lane.
  - This packet.
  - Current `git status --short --branch`, `git rev-parse HEAD`, and PR #469 status.
  - The strict link-check failure list from a fresh local run or GitHub log.
- load rule: receiver re-runs progressive source loading per overlay; the packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- decision, framing, profile, or convention: Goal frame says registry/profile work should optimize for one-stop creator intelligence while keeping raw facts in source-backed capture/lake records.
  - decided in: visible prior goal frame in this thread; verify by reading this packet's Goal Handoff and current user message if available.
  - compare target: `goal_handoff` text in this packet.
  - verify before: expanding scope beyond PR #469 CI fix or adding new sync-contract artifacts.
- decision, framing, profile, or convention: Creator registry belongs under Capture/social-media source family; Creator Signal owns the buyer/operator surface over it.
  - decided in: PR #469 diff, especially `orca/product/spines/capture/core/source_families/social_media/creator_registry/README.md`.
  - compare target: file hash `ab91d277ee32969307e5fa3658662c28f580714d7f101b29bb41d2f4d25f455e` at HEAD `217b46ca`.
  - verify before: changing placement or source ownership.
- decision, framing, profile, or convention: #468 replaced #464 and is merged; do not continue #464 as the active branch.
  - decided in: GitHub PR #468, merged into `main` at merge commit `f75c63426edd10dbeae2e732940ab13d52265cce` by `eric-foo` on 2026-06-29T15:16:50Z.
  - compare target: `gh pr view 468 --json state,mergedAt,mergeCommit`.
  - verify before: touching any IG projection branch or root worktree state.

## Active Objective

Finish the creator registry folder placement lane on PR #469. The immediate blocker is red CI from stale retrieval metadata paths after moving creator profile/linkage files into `creator_registry/`.

## Exact Next Authorized Action

1. In `C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-registry-folder-main`, re-run `python .agents\hooks\check_map_links.py --strict` and confirm the 15 C2 stale `open_next` failures.
2. Patch the stale `open_next` paths to the new `creator_registry/` locations. Target the files named by the checker; do not mass-edit body prose unless needed by a checker or active retrieval path.
3. Re-run:
   - `python .agents\hooks\check_map_links.py --strict`
   - `python -m pytest -q -p no:cacheprovider orca-harness\tests\unit\test_creator_registry_index.py orca-harness\tests\unit\test_creator_public_handle_linkage.py orca-harness\tests\unit\test_creator_profile_current_static_view.py orca-harness\tests\unit\test_instagram_reels_creator_metric_seed.py orca-harness\tests\unit\test_youtube_creator_metric_seed.py`
   - `python orca-harness\runners\run_creator_profile_current_materialize.py --check`
   - `git diff --check origin/main..HEAD`
4. Commit the CI fix onto `codex/creator-registry-folder-main` and push to PR #469.
5. Stop if fixing stale links reveals substantive artifact-authority conflicts rather than simple moved-path metadata.

## Authority And Source Ledger

- Repository instructions:
  - `AGENTS.md` supplied in current conversation; load-bearing for Orca behavior and protected-action boundaries. Compare target for receiver: reread `AGENTS.md` in workspace.
- Overlay or equivalent authority:
  - `.agents/workflow-overlay/README.md`
    - Role: overlay entrypoint.
    - Load-bearing: yes.
    - Compare target: sha256 `7a30709d6011bd3f6458e926570b7164b91c7f3bf8bae7dbd5a612a08de81fda`, size 2550, checked 2026-06-29T23:35+08.
    - Reuse rule: reread before strict/actionable repo claims.
  - `.agents/workflow-overlay/artifact-folders.md`
    - Role: durable destination and accepted folder authority.
    - Load-bearing: yes.
    - Compare target: sha256 `aac40739565a55b100b32bbf14d82b15302ef6ab06284f2c63244f15acd476e7`, size 27988, checked 2026-06-29T23:35+08.
    - Reuse rule: reread before moving handoff or registry artifacts.
  - `.agents/workflow-overlay/source-loading.md`
    - Role: confirm-don't-trust / source-loading policy pointer.
    - Load-bearing: yes.
    - Compare target: sha256 `26f01f5eccad38b327ac8d54b6e8059d8e9ab6eea9f4621960e99856e4cd0385`, size 32062, checked 2026-06-29T23:35+08.
    - Reuse rule: reread before strict/actionable source-loading decisions.
- User constraints:
  - User said `1 done`, asked to `do 2` and `explain 3`; step 2 became PR #469, step 3 explanation was chat-only.
  - User invoked `workflow-handoff` to continue in a fresh lane.
- Source-read ledger:
  - `C:\Users\vmon7\.codex\skills\workflow-handoff\SKILL.md`
    - Role: handoff packet contract.
    - Load-bearing: yes.
    - Compare target: sha256 `3ce84d0ac22fd8c24c7c99bdf8707de7f55e6981d005624acb6d6e71f9f81a34`, size 34709.
    - Last checked: 2026-06-29T23:35+08.
    - Reuse rule: reread only if modifying packet shape or validating handoff behavior.
  - `orca/product/spines/capture/core/source_families/social_media/creator_registry/README.md`
    - Role: folder front door and placement rationale.
    - Load-bearing: yes.
    - Compare target: sha256 `ab91d277ee32969307e5fa3658662c28f580714d7f101b29bb41d2f4d25f455e`, size 6956, at HEAD `217b46ca`.
    - Last checked: 2026-06-29T23:35+08.
    - Reuse rule: reread before editing registry placement.
  - `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_v0.json`
    - Role: static known-account registry index.
    - Load-bearing: yes.
    - Compare target: sha256 `1b050a205c92ef14d56988617b5f35da61a0ab5ae2fbc14a2051c9a555df83a3`, size 61279, at HEAD `217b46ca`.
    - Last checked: 2026-06-29T23:35+08.
    - Reuse rule: reread before changing index or dedupe behavior.
  - `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_spec_v0.md`
    - Role: registry index contract.
    - Load-bearing: yes.
    - Compare target: sha256 `b59fb3c1f825cb6d93ac695f9801d7d289e31421458f4303014e690fc2ce87ae`, size 4827, at HEAD `217b46ca`.
    - Last checked: 2026-06-29T23:35+08.
    - Reuse rule: reread before changing sync/dedupe semantics.
  - `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json`
    - Role: identity/linkage ledger moved under registry.
    - Load-bearing: yes.
    - Compare target: sha256 `620a1e87a7ecd31df3f06905b1ca2b4317a13c509180585a8ccd7824e3f1afad`, size 27639, at HEAD `217b46ca`.
    - Last checked: 2026-06-29T23:35+08.
    - Reuse rule: reread before any identity/linkage claim.
  - `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json`
    - Role: current one-stop profile export moved under registry.
    - Load-bearing: yes.
    - Compare target: sha256 `43eeeb992b9b68ba5fd379f7acbbb01ba92cfbe1b24bf29c42178904d5fb340c`, size 308958, at HEAD `217b46ca`.
    - Last checked: 2026-06-29T23:35+08.
    - Reuse rule: reread or regenerate before profile-current claims.
  - PR #469 GitHub state
    - Role: lifecycle and CI state.
    - Load-bearing: yes.
    - Compare target: `gh pr view 469 --json number,url,isDraft,state,mergeable,mergeStateStatus,headRefName,baseRefName,headRefOid,baseRefOid,statusCheckRollup`.
    - Last checked: 2026-06-29T23:35+08.
    - Observed: PR open draft, `MERGEABLE`, `UNSTABLE`, head `217b46ca4a38393080679d3fd1e73d4f796707a9`, CI `orca-harness-tests` failure.
    - Reuse rule: reread before push/merge/ready claims.
- Source gaps:
  - Full PR #469 CI logs beyond `--log-failed` were not read.
  - No delegated review has been run on PR #469.
  - Step 3 sync contract is explained in chat but not yet written as a durable artifact.
- Strict-only blockers:
  - PR #469 is not ready/green; CI failed.
  - This handoff is not validation, readiness, acceptance, or merge authority.
- Not-proven boundaries:
  - No claim that registry folder design is review-approved.
  - No claim that Discovery/Capture sync is implemented.
  - No claim that Silver/lake producer exists for auto-updating rollups.

## Current Task State

- Completed:
  - PR #468 replaced conflicted PR #464 and merged into `main`.
  - Clean branch `codex/creator-registry-folder-main` created from current `origin/main`.
  - PR #469 opened as draft: `https://github.com/eric-foo/orca/pull/469`.
  - PR #469 commit `217b46ca` adds real `creator_registry/` folder, moves five creator registry authority artifacts into it, adds `creator_registry_index_v0.json`, adds index spec and tests, and updates active pointers/code/tests.
  - Local focused pytest passed: 52 tests.
  - `run_creator_profile_current_materialize.py --check` passed: up to date.
  - `git diff --check origin/main..HEAD` passed before handoff.
- Partially completed:
  - Step 3 Discovery/Capture sync contract was explained in chat but not authored as a durable spec.
  - Handoff packet is being written as an untracked durable artifact for the fresh lane.
- Broken or uncertain:
  - PR #469 CI failed on strict retrieval-link check with 15 stale `open_next` paths.
  - CI failure must be fixed before #469 can be considered merge-ready.

## Workspace State

- Branch: `codex/creator-registry-folder-main`
- Head: `217b46ca4a38393080679d3fd1e73d4f796707a9`
- Dirty or untracked state before handoff: clean; `## codex/creator-registry-folder-main...origin/codex/creator-registry-folder-main`
- Dirty or untracked state after writing the handoff file: expect `?? docs/hygiene/creator_registry_folder_handoff_v0.md`.
- Target files or artifacts:
  - `orca/product/spines/capture/core/source_families/social_media/creator_registry/`
  - PR #469
  - stale `open_next` files reported by strict link checker.
- Related worktrees or branches:
  - Root workspace `C:\Users\vmon7\Desktop\projects\orca` is on stale `codex/ig-reels-capture-spine` at `63694997`; do not continue this lane there.
  - Old local branch/worktree `codex/creator-registry-folder` exists but is stale and dangerous to reuse.

## Changed / Inspected / Tested Files

- `orca/product/spines/capture/core/source_families/social_media/creator_registry/README.md`
  - Status: added in PR #469.
  - Role: registry folder front door.
  - Important observations: states folder-not-one-document, Capture vs Creator Signal split, and dedupe rule.
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_v0.json`
  - Status: added in PR #469.
  - Role: Discovery/Capture known-account index.
  - Important observations: 33 account rows; 30 YouTube, 3 Instagram; no creator records.
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_spec_v0.md`
  - Status: added in PR #469.
  - Role: index contract and dedupe-state semantics.
- `orca-harness/tests/unit/test_creator_registry_index.py`
  - Status: added in PR #469.
  - Role: proves index mirrors ledger and carries no metric/contact fields.
- `orca-harness/capture_spine/creator_profile_current/materialize.py`
  - Status: modified in PR #469.
  - Role: default source pointers now use `creator_registry/`.
- `orca-harness/runners/run_creator_profile_current_materialize.py`
  - Status: modified in PR #469.
  - Role: default output/account ledger now under `creator_registry/`.
- Stale-link target files from CI:
  - `docs/prompts/architecture/channel_neutral_creator_identity_profile_architecture_prompt_v0.md`
  - `docs/prompts/architecture/creator_profile_validator_structure_architecture_planning_prompt_v0.md`
  - `docs/prompts/reviews/creator_ledger_pr439_delegated_adversarial_artifact_review_prompt_v0.md`
  - `docs/prompts/reviews/creator_profile_current_materializer_delegated_adversarial_code_review_patch_prompt_v0.md`
  - `docs/prompts/reviews/creator_soft_link_boundary_pr431_adversarial_artifact_review_prompt_v0.md`
  - `docs/review-inputs/creator_metric_source_audit_v0.md`
  - `docs/review-inputs/creator_signal_spine_pre_ratification_review_input_v0.md`
  - `docs/review-outputs/adversarial-artifact-reviews/creator_ledger_pr439_delegated_adversarial_artifact_review_v0.md`
  - Status: not yet patched for CI.
  - Role: stale `open_next` references to old flat paths.

## Frozen Decisions

- Decision: Creator registry is a folder under `orca/product/spines/capture/core/source_families/social_media/creator_registry/`, not one giant ledger document.
  - Evidence: PR #469 README and index/spec files.
  - Consequence: identity/profile/linkage artifacts live together; metric seeds stay in platform folders.
- Decision: Registry index is dedupe/routing over known public accounts, not metric or audience authority.
  - Evidence: `creator_registry_index_spec_v0.md` and `test_creator_registry_index.py`.
  - Consequence: do not add average views, engagement rate, ideal audience, contact fields, or raw evidence into the index.
- Decision: Cross-platform creator records remain absent until public-handle linkage evidence is admitted and reviewed.
  - Evidence: moved linkage ledger has `creator_records: []`; profile-current view has `creator_record_profiles: 0`.
  - Consequence: no Jeremy cross-platform promotion in this lane.
- Decision: SQLite/dashboard remain deferred.
  - Evidence: registry README and profile-current specs include non-claims.
  - Consequence: do not add storage engine or UI work while fixing #469.

## Mutable Questions

- Question: Should the Step 3 Discovery/Capture sync contract be a new durable spec after #469 lands, or folded into the registry index spec?
  - Why still mutable: user asked for explanation, not implementation, and #469 CI must be fixed first.
  - What would resolve it: owner direction after #469 is green/merged.
- Question: Should historical prompt/review `open_next` stale links be updated to new paths or annotated as nonresolving?
  - Why still mutable: `check_map_links --strict` fails because they are `open_next`, not body prose; usually live retrieval metadata should resolve.
  - What would resolve it: patch/update them and confirm strict link check passes; annotate only if a source-specific reason exists.
- Question: Should repeat discovery events become their own append-only family?
  - Why still mutable: current registry only has routing fields, not event storage.
  - What would resolve it: later sync-contract or lake-native producer design.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: PR #464 branch `codex/ig-reels-capture-spine`.
  - Why stale or dangerous: conflicted; replaced by PR #468.
  - Current replacement: #468 merged into `main`; continue creator registry lane via PR #469.
- Stale instruction, idea, artifact, or finding: old local branch/worktree `codex/creator-registry-folder`.
  - Why stale or dangerous: it included unrelated deletions and stale data-lake state when compared to current `main`.
  - Current replacement: clean one-commit branch `codex/creator-registry-folder-main` / PR #469.
- Stale instruction, idea, artifact, or finding: old flat paths under `.../social_media/creator_profile_current_*` and `.../social_media/creator_public_handle_linkage_*`.
  - Why stale or dangerous: PR #469 moved these into `.../social_media/creator_registry/`.
  - Current replacement: new `creator_registry/` paths.
- Stale instruction, idea, artifact, or finding: "PR #469 CI is in progress."
  - Why stale or dangerous: CI is now complete and failed.
  - Current replacement: CI failed in `check_map_links --strict` with 15 C2 missing-path findings.

## Commands And Verification Evidence

- Command:
  ```powershell
  gh pr view 469 --json number,url,isDraft,state,mergeable,mergeStateStatus,headRefName,baseRefName,headRefOid,baseRefOid,statusCheckRollup
  ```
  Result:
  - Passed.
  - Important output: PR #469 open draft, `MERGEABLE`, `UNSTABLE`, head `217b46ca4a38393080679d3fd1e73d4f796707a9`, CI `orca-harness-tests` completed with `FAILURE`.
  - Re-run target so the receiver can confirm rather than trust: same command.
- Command:
  ```powershell
  gh run view 28383634774 --job 84092512173 --log-failed
  ```
  Result:
  - Passed.
  - Important output: `python .agents/hooks/check_map_links.py --strict` failed with 15 C2 findings for old flat creator paths.
  - Re-run target so the receiver can confirm rather than trust: same command or `python .agents\hooks\check_map_links.py --strict`.
- Command:
  ```powershell
  python .agents\hooks\check_map_links.py --strict
  ```
  Result:
  - Failed locally as expected.
  - Important output: same 15 C2 missing old-path findings; `annotated nonresolving: 33 (debt, not failures)`.
  - Re-run target so the receiver can confirm rather than trust: same command.
- Command:
  ```powershell
  python -m pytest -q -p no:cacheprovider orca-harness\tests\unit\test_creator_registry_index.py orca-harness\tests\unit\test_creator_public_handle_linkage.py orca-harness\tests\unit\test_creator_profile_current_static_view.py orca-harness\tests\unit\test_instagram_reels_creator_metric_seed.py orca-harness\tests\unit\test_youtube_creator_metric_seed.py
  ```
  Result:
  - Passed before handoff.
  - Important output: `52 passed`.
  - Re-run target so the receiver can confirm rather than trust: same command after fixing links.
- Command:
  ```powershell
  python orca-harness\runners\run_creator_profile_current_materialize.py --check
  ```
  Result:
  - Passed before handoff.
  - Important output: `up to date: ...\creator_registry\creator_profile_current_view_v0.json`.
  - Re-run target so the receiver can confirm rather than trust: same command after edits.

## Blockers And Risks

- Blocker or risk: PR #469 CI is red.
  - Evidence: GitHub CI and local `check_map_links --strict` both report 15 stale open_next paths.
  - Likely next action: patch stale open_next references to the new `creator_registry/` paths.
- Blocker or risk: Root workspace is on a stale branch.
  - Evidence: earlier status showed root branch `codex/ig-reels-capture-spine` at `63694997`.
  - Likely next action: fresh lane should work in `worktrees/creator-registry-folder-main` or a new branch from `origin/codex/creator-registry-folder-main`.
- Blocker or risk: Handoff file is not committed.
  - Evidence: expected dirty state after write is `?? docs/hygiene/creator_registry_folder_handoff_v0.md`.
  - Likely next action: receiver can read it from filesystem; do not treat it as part of PR #469 unless explicitly staged later.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - Workspace branch/head is `codex/creator-registry-folder-main` / `217b46ca4a38393080679d3fd1e73d4f796707a9`.
  - PR #469 remains open and red for the same link-check failure, or has drifted.
  - The moved registry files exist under `creator_registry/`.
  - The old flat paths are intentionally absent in PR #469.
  - Local strict link checker reproduces the 15 C2 findings before patch.
  - Focused tests and materializer still pass after patch.
- Compare target for each:
  - `git status --short --branch`
  - `git rev-parse HEAD`
  - `gh pr view 469 --json ...`
  - `python .agents\hooks\check_map_links.py --strict`
  - file hashes listed in Authority And Source Ledger
- Load outcomes and what each means:
  - `REUSE`: all required facts match; continue at Exact Next Authorized Action.
  - `PARTIAL_REUSE`: optional context drifted; rederive optional context and continue only verified steps.
  - `STALE_REREAD_REQUIRED`: PR/head/checker state drifted but can be re-read safely; reload before patching.
  - `BLOCKED_DRIFT`: branch/head or dirty state conflicts with unknown edits; stop and ask owner or isolate a new worktree.
  - `BLOCKED_MISSING_PACKET`: this file is absent/unreadable.
  - `BLOCKED_UNVERIFIABLE`: a load-bearing claim cannot be checked; do not proceed on sender memory.
- Sources that must be reread if drift is detected:
  - `.agents/workflow-overlay/source-loading.md`
  - `.agents/workflow-overlay/artifact-folders.md`
  - PR #469 state and CI logs
  - all files named by fresh `check_map_links --strict`

## Do Not Forget

- The next lane should fix PR #469 CI first. Do not start the Step 3 sync-contract implementation while the registry folder PR is red.
