# Creator Registry Folder PR #457 Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed cross-recipient prompt for a read-only adversarial code/change review of
  PR #457's creator registry folder, dedupe index, materializer wiring, and
  placement decision.
use_when:
  - Commissioning an independent review of PR #457 before merge.
  - Checking whether the creator registry is an actual durable placement or only a risky pointer.
  - Checking whether the registry correctly stays handle/identity authority, not fact or metric authority.
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/artifact-folders.md
  - .agents/workflow-overlay/source-of-truth.md
  - docs/prompts/templates/shared/orca_preflight_defaults_v0.md
branch_or_commit:
  branch: codex/creator-registry-folder
  pr: https://github.com/eric-foo/orca/pull/457
  review_base: 32e2d888f07ce345abadd521dca0dff9db93e264
  review_head: 9834a6b0b0c1e09a3ae623cbe00dae2a5b7c14ea
stale_if:
  - PR #457 review head changes and the reviewer does not explicitly re-pin the diff.
  - The creator registry placement moves, is superseded, or gains capture/discovery sync code before review.
  - Orca placement, prompt, source-loading, or review-lane authority changes before review.
authority_boundary: retrieval_only
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

- output_mode: `review-report`
- prompt_artifact_path: `docs/prompts/reviews/creator_registry_folder_pr457_adversarial_code_review_prompt_v0.md`
- review_report_destination: `docs/review-outputs/adversarial-artifact-reviews/creator_registry_folder_pr457_adversarial_code_review_v0.md`
- template_kind: `repo-code-review` route-out from `workflow-delegated-review-patch`; no runtime model routing.
- template_source: custom Orca review prompt using `.agents/workflow-overlay/prompt-orchestration.md`, `.agents/workflow-overlay/review-lanes.md`, and `workflow-code-review`; the bound adversarial artifact template is not used as the primary template because PR #457 is a mixed code/docs/data diff.
- authorization_basis: current owner request invoked `workflow-delegated-review-patch` and raised a placement risk: "if you just made a pointer i feel its extremly risky for long term. we should decide actual placement."
- edit_permission: `read-only`; reviewer may write only the durable review report at the destination above.
- target_files_or_dirs: the pinned diff `32e2d888f07ce345abadd521dca0dff9db93e264..9834a6b0b0c1e09a3ae623cbe00dae2a5b7c14ea`, excluding this prompt artifact and any later prompt-only commits.
- source_pack: custom S1 plus PR #457 diff, creator registry folder files, materializer/test changes, and placement authorities named in this prompt.
- dirty_state_allowance: read the pinned diff, not mutable branch HEAD. If the worktree has later commits or uncommitted prompt/report files, treat them as out of scope unless they materially affect access to the pinned diff.
- expected_branch: `codex/creator-registry-folder`
- expected_review_base: `32e2d888f07ce345abadd521dca0dff9db93e264`
- expected_review_head: `9834a6b0b0c1e09a3ae623cbe00dae2a5b7c14ea`
- isolation_decision: no new worktree required for read-only review; use a clean checkout/worktree if available.
- doctrine_change_decision: no doctrine edit is authorized. If placement is architecture-level rather than patch-level, return `NEEDS_ARCHITECTURE_PASS`; do not invent a new product spine or move files.
- validation_gates:
  - Source-load the pinned diff and cite `file:line` or stable diff anchors for load-bearing claims.
  - Do not run live capture, live discovery, public web collection, browser capture, or data-lake writes.
  - Tests are optional review evidence, not mandatory. If rerun, report exact commands and outcomes. If not run, report `not_run`.
  - Do not treat a green placement check as source authority; placement shape and long-term authority are separate claims.
- thread_operating_target_continuity: no visible active `thread_operating_target`; omitted.

## Review Commission

You are performing a read-only adversarial code/change review for Orca.

This prompt is a route-out from `workflow-delegated-review-patch` because the target is a multi-file PR diff, not a single high-stakes authored artifact. Do not treat this as a repo-mode delegated patch commission. Do not patch, stage, commit, push, merge, or open a PR.

Review target:

- PR #457: `https://github.com/eric-foo/orca/pull/457`
- Pinned diff: `32e2d888f07ce345abadd521dca0dff9db93e264..9834a6b0b0c1e09a3ae623cbe00dae2a5b7c14ea`
- Branch at prompt creation: `codex/creator-registry-folder`

Review purpose:

Attack whether PR #457 creates the correct durable home for the creator ledger/registry. The key risk is that the change may have created a pointer or capture-local parking spot while the actual long-term ledger belongs at a higher Creator Signal / product surface. Also attack whether the implementation creates a second source of truth for facts or metrics, breaks source-backed profile materialization, or leaves capture/discovery sync semantics misleading.

Fitness reference:

Goal: Orca has one clear creator registry folder that future capture, discovery, Creator Signal, and buyer-facing profile work can safely point at.

Done looks like: A reviewer can answer, from source, whether PR #457's folder is the actual correct placement for platform-account identity and dedupe state, whether higher-level Creator Signal is only a consumer surface, and whether any placement/sync issue blocks merge or needs an architecture pass.

This fitness reference is an alignment axis to attack, not a pass bar.

## Required Authority Sources

Read these before strict findings:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-of-truth.md`
4. `.agents/workflow-overlay/source-loading.md`
5. `.agents/workflow-overlay/artifact-folders.md`
6. `.agents/workflow-overlay/review-lanes.md`
7. `.agents/workflow-overlay/prompt-orchestration.md`
8. `.agents/workflow-overlay/validation-gates.md`
9. `.agents/workflow-overlay/delegated-review-patch.md`
10. `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`

Then source-load the pinned PR diff:

```powershell
git diff --name-status 32e2d888f07ce345abadd521dca0dff9db93e264..9834a6b0b0c1e09a3ae623cbe00dae2a5b7c14ea
git diff 32e2d888f07ce345abadd521dca0dff9db93e264..9834a6b0b0c1e09a3ae623cbe00dae2a5b7c14ea -- <target-file>
```

Changed files in the pinned target:

1. `docs/workflows/data_capture_spine_consolidation_map_v0.md`
2. `orca-harness/capture_spine/creator_profile_current/materialize.py`
3. `orca-harness/runners/run_creator_profile_current_materialize.py`
4. `orca-harness/tests/fixtures/creator_public_handle_linkage/valid_synthetic_ledger.json`
5. `orca-harness/tests/unit/test_creator_profile_current_static_view.py`
6. `orca-harness/tests/unit/test_creator_public_handle_linkage.py`
7. `orca-harness/tests/unit/test_creator_registry_index.py`
8. `orca-harness/tests/unit/test_youtube_creator_metric_seed.py`
9. `orca/product/spines/capture/core/operating_model/data_capture_spine_future_exploration_lanes_v0.md`
10. `orca/product/spines/capture/core/source_capture_toolbox/README.md`
11. `orca/product/spines/capture/core/source_families/social_media/creator_registry/README.md`
12. `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_native_record_mapping_v0.md`
13. `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md`
14. `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json`
15. `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md`
16. `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json`
17. `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_spec_v0.md`
18. `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_v0.json`
19. `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md`
20. `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_observation_ledger_spec_v0.md`
21. `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_seed_v0.json`
22. `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_observation_ledger_v0.json`
23. `orca/product/spines/creator_signal/README.md`
24. `orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md`

Do not bulk-load unrelated capture, discovery, data-lake, product-lead, ECR, Cleaning, Judgment, research, inbox, or historical review-output files unless a directly material issue in the pinned diff cannot be assessed without one narrow adjacent read.

## Method Sequence

REFERENCE-LOAD:

- `workflow-delegated-review-patch` only to preserve the route-out, de-correlation, CA adjudication, and `NEEDS_ARCHITECTURE_PASS` boundaries. Do not APPLY it as a patch-authorized lane.
- `workflow-deep-thinking`
- `workflow-code-review`

Do not APPLY these methods before source readiness. SOURCE-LOAD the required sources above, then declare either:

- `SOURCE_CONTEXT_READY`, with a compact source-read ledger; or
- `SOURCE_CONTEXT_INCOMPLETE`, with missing sources, conflicts, excluded sources, and what claims are blocked.

Only after source readiness:

1. APPLY `workflow-deep-thinking` to frame the placement boundary, source-of-truth risk, duplicate-ledger risk, and sync/read-model failure modes.
2. APPLY `workflow-code-review` to produce findings against the pinned diff.

If `workflow-code-review` is unavailable, unresolved, or cannot be applied after source readiness, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` with the reason and do not emit strict review claims.

## Review Checks

Findings first. Be adversarial within this commission.

### Placement And Authority

1. Is `orca/product/spines/capture/core/source_families/social_media/creator_registry/` a defensible actual home for platform-account identity, linkage evidence, profile views, and the index, or is it only a pointer while the real ledger belongs under `orca/product/spines/creator_signal/` or another higher-level product spine?
2. Does the folder README make the core/surface split clear: Capture-owned source-family registry as identity substrate, Creator Signal as consumer/product surface?
3. Does the PR accidentally create a second authority beside the profile view, handle-linkage ledger, YouTube seed, or future Silver/lake records?
4. If placement cannot be resolved locally, return `NEEDS_ARCHITECTURE_PASS` with the exact architecture decision needed. Do not recommend a local patch as if it settles the design.

### Registry Shape And Dedupe State

5. Does `creator_registry_index_v0.json` behave as the all-known-platform-account index, not one giant fact ledger?
6. Are `canonical_creator_id`, `platform_accounts`, `dedupe_state`, and evidence pointers sufficient for discovery/capture to avoid rediscovering already-known accounts?
7. Is dedupe state useful and small, or is it dead ceremony that belongs elsewhere?
8. Does the index avoid pretending there is TikTok or Instagram data that has not been seeded yet?
9. Do tests enforce uniqueness and source-pointer consistency strongly enough to catch duplicate account rows, stale paths, or profile-view drift?

### Capture, Discovery, And Future Auto-Update Semantics

10. Does the PR overclaim auto-update, live sync, data-lake derivation, discovery suppression, capture freshness, dashboard readiness, SQLite readiness, or buyer-facing completeness?
11. Is it clear that metrics such as average views and engagement rate will derive from sibling/lake records later, not be hand-maintained as fact authority in the index?
12. Does the current folder leave a coherent future path for capture/discovery to update or consult the registry without requiring a later rewrite?

### Code, Paths, And Validation

13. Did moved paths update materializer defaults, tests, source pointers, and active docs without leaving stale live references?
14. Does the materializer still rebuild `creator_profile_current_view_v0.json` from the intended source files?
15. Do the static JSON fixtures remain source-backed and non-synthetic where the PR claims real rows?
16. Are test assertions specific enough to catch structural regressions rather than just confirming the new file exists?
17. Does placement validation pass for the new registry files, and are any known placement-check failures truly pre-existing/out of scope?

## Prompt-Author Validation Evidence To Inspect, Not Trust

The author reported these checks before this review prompt was filed. Re-run if useful; otherwise treat them as claimed evidence only and inspect whether the diff makes them credible:

```powershell
python .\orca-harness\runners\run_creator_profile_current_materialize.py --check
python -m pytest -p no:cacheprovider -q .\orca-harness\tests\unit\test_creator_registry_index.py .\orca-harness\tests\unit\test_creator_public_handle_linkage.py .\orca-harness\tests\unit\test_youtube_creator_metric_seed.py .\orca-harness\tests\unit\test_creator_profile_current_static_view.py
git diff --cached --check
python .\.agents\hooks\check_placement.py --changed --strict
```

Reported outcomes:

- materializer check: up to date
- targeted pytest: `49 passed`
- diff check: clean before implementation commit
- direct placement classification for new registry files: ok
- full `check_placement.py --changed --strict`: failed because pre-existing top-level `.gitattributes`, `.githooks`, and `.github` placement debt is still in the changed-file set; no creator registry placement violation was observed by the author.

Do not trust these outcomes without either re-running, inspecting the corresponding tests/checks, or marking them `not_verified`.

## Output Contract

Write the durable report to:

`docs/review-outputs/adversarial-artifact-reviews/creator_registry_folder_pr457_adversarial_code_review_v0.md`

The report must include:

1. Retrieval header with `authority_boundary: retrieval_only`.
2. Provenance fields in the body:
   - `reviewed_by: <operator/tooling supplied, or unrecorded>`
   - `authored_by: OpenAI/Codex current lane`
   - `de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback | unrecorded`
3. Source context status and source-read ledger with `file:line` or stable diff anchors for load-bearing claims.
4. Method invocation status for `workflow-deep-thinking` and `workflow-code-review`.
5. Findings first, ordered by severity: `critical`, `major`, `minor`.
6. For each finding:
   - severity;
   - location;
   - issue;
   - evidence;
   - impact;
   - minimum_closure_condition;
   - next_authorized_action;
   - recommended correction or advisory remediation direction.
7. Explicit placement answer:
   - `placement_ok_as_actual_home`
   - `placement_is_pointer_only_risk`
   - `needs_higher_level_home`
   - `NEEDS_ARCHITECTURE_PASS`
8. Explicit answers to:
   - Is this registry the source of truth for handles/accounts only, not facts/metrics?
   - Does the PR avoid becoming one giant ledger?
   - Does the PR preserve a future capture/discovery sync path without claiming it exists now?
9. Validation status:
   - commands run or `not_run`;
   - whether author-reported validation evidence was independently verified, inspected-only, or not verified.
10. Not-proven boundaries and residual risks.
11. Review-use boundary.

Do not include `patch_queue_entry`. Do not edit source files. Do not run live capture, live discovery, browser capture, network collection, or data-lake writes.

After writing the report, return this compact chat summary:

```yaml
review_summary:
  status: completed | failed | blocked
  review_location: durable_report | chat_only_current_thread
  report_path:
  placement_answer:
  top_findings:
    - severity:
      issue:
      location:
  recommendation:
  next_action:
```

If the required report cannot be written, return `status: failed`, `review_location: chat_only_current_thread`, no `report_path`, and enough detail to route the write failure.

Review-use boundary:

This review is decision input only. It is not approval, validation, readiness, mandatory remediation, merge authorization, source-of-truth promotion, implementation authorization, or executor-ready patch authority until separately accepted or authorized by Orca owner / Chief Architect.
