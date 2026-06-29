# Creator Profile Current Materializer Delegated Adversarial Code Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca delegated review-and-patch prompt
scope: >
  Commission a de-correlated repo-mode adversarial code review-and-patch pass
  for PR #452, the creator-profile-current materializer that derives the checked-in
  creator profile view from sibling account-linkage and metric-seed ledgers.
use_when:
  - Couriering PR #452 for independent review before the materializer is treated as settled.
  - Checking whether creator-profile-current can be regenerated as source ledgers grow without fake freshness, stale checked-in output, or source-backedness overclaims.
authority_boundary: retrieval_only
branch_or_commit: codex/creator-ledger-real-seed @ d8edd7862d9471ccc0b101266387f337d7bba967
pr: https://github.com/eric-foo/orca/pull/452
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/decision-routing.md
  - docs/prompts/templates/shared/orca_preflight_defaults_v0.md
  - orca-harness/capture_spine/creator_profile_current/materialize.py
  - orca-harness/runners/run_creator_profile_current_materialize.py
  - orca-harness/tests/unit/test_creator_profile_current_static_view.py
  - orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_v0.json
  - orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_v0.json
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_seed_v0.json
input_hashes:
  docs/workflows/orca_repo_map_v0.md: ECA433CF1DEC346339B4F6DEA2B1941C9FC1A92CD0A16F2E03FA4A5717F8606E
  orca-harness/capture_spine/creator_profile_current/__init__.py: FAC68FF1EBFC327A73915D4769EF26D9F83EF55ED1F747CE794FD62310104AB9
  orca-harness/capture_spine/creator_profile_current/materialize.py: 840885253F3E9B16AA7D56D44A823F3D7BB2B1EC0D0789B99F68FA84A104FF7C
  orca-harness/runners/run_creator_profile_current_materialize.py: A869E73A53DDA1DEF21F1D7DAFA3367C759171EC086221D86E7970F044FA8F63
  orca-harness/tests/unit/test_creator_profile_current_static_view.py: 55878AC676A6CC5801B8E552EE6786D471522066C95ECE755A36796B0824EC31
stale_if:
  - PR #452 is retargeted away from main.
  - Base commit 2d08b747c720ed6dc0b1031ea5828b01663286b6 is no longer the PR base when review starts.
  - Any target file listed in this prompt changes after d8edd7862d9471ccc0b101266387f337d7bba967 before review, other than this prompt artifact being added in a later commit.
  - Orca delegated-review-patch, review-lanes, prompt-orchestration, or source-loading overlay authority changes before review.
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0, constants bound; deltas stated here.

- output_mode: `file-write` for this prompt artifact, plus `paste-ready-chat` copy for couriering.
- prompt_artifact_path: `docs/prompts/reviews/creator_profile_current_materializer_delegated_adversarial_code_review_patch_prompt_v0.md`.
- template_kind: `review` plus delegated review-and-patch commission semantics from `.agents/workflow-overlay/delegated-review-patch.md`.
- authorization_basis: current owner invocation of `workflow-delegated-review-patch` after PR #452 was opened for the creator-ledger materializer implementation.
- edit_permission_for_receiver: `patch-only` inside the named target files below; all other paths are read-only / flag-only.
- workspace_path: `C:\Users\vmon7\Desktop\projects\orca`.
- expected_worktree_path: `C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-ledger-real-seed`.
- branch_or_commit_reference: `codex/creator-ledger-real-seed @ d8edd7862d9471ccc0b101266387f337d7bba967`.
- reviewed_diff: `2d08b747c720ed6dc0b1031ea5828b01663286b6..d8edd7862d9471ccc0b101266387f337d7bba967`.
- target_files_or_dirs:
  - `orca-harness/capture_spine/creator_profile_current/__init__.py`
  - `orca-harness/capture_spine/creator_profile_current/materialize.py`
  - `orca-harness/runners/run_creator_profile_current_materialize.py`
  - `orca-harness/tests/unit/test_creator_profile_current_static_view.py`
  - `docs/workflows/orca_repo_map_v0.md`
- downstream_report_path: `docs/review-outputs/adversarial-artifact-reviews/creator_profile_current_materializer_adversarial_code_review_v0.md`.
- dirty_state_allowance: target worktree should be clean before the receiver starts. If this prompt exists as a later commit on the same branch, review the pinned target diff above and ignore the prompt-file commit except as dispatch context.
- controlling_source_state: checked before prompt creation; worktree clean on `codex/creator-ledger-real-seed`, PR #452 open/draft, head `d8edd7862d9471ccc0b101266387f337d7bba967`, base `2d08b747c720ed6dc0b1031ea5828b01663286b6`.
- doctrine_change_decision: no doctrine change intended. This is implementation/test/runner/repo-map materialization work under existing creator-profile and delegated-review-patch boundaries.
- isolation_decision: existing isolated worktree `worktrees/creator-ledger-real-seed` off `origin/main`; no new worktree required for a bounded review-and-patch pass.
- validation_evidence_already_observed:
  - `python runners\run_creator_profile_current_materialize.py --check` passed from `orca-harness`.
  - `python -m pytest tests\unit\test_creator_profile_current_static_view.py tests\unit\test_youtube_creator_metric_seed.py -q` passed, 22 tests.
  - `python .agents\hooks\check_repo_map_freshness.py --staged --strict` passed before commit.
  - `python .agents\hooks\check_map_links.py --strict` passed with 0 findings.
  - `python .agents\hooks\check_retrieval_header.py --changed --strict` passed.
  - `python .agents\hooks\header_index.py --strict` returned no changed `.md` files in diff.
  - Earlier full harness suite before the repo-map-only follow-up: `python -m pytest` passed, 1872 passed, 4 skipped, 1 existing warning.
- receiver_validation_expectation: rerun the materializer check and focused tests for any patch. Run `git diff --check`. If touching the repo-map route, run map freshness/link checks. Run full harness pytest only if behavior changes beyond the materializer/join/check surface or if focused evidence is ambiguous.
- thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
  if_changed_reason: not_applicable

## Delegated Review-And-Patch Commission

### Lane Binding

- overlay_status: `provisional_opt_in`, explicitly invoked by the owner for this PR.
- operating_contract_pointer: `.agents/workflow-overlay/delegated-review-patch.md`.
- review_lane: mixed, with `workflow-code-review` for implementation code/tests/runner behavior and `workflow-adversarial-artifact-review` only for the repo-map route text if a source-backed doc finding is needed. The code review lane is primary.
- mode: `base-subagent` / repo-mode controller. Do not use split-executor.
- actor_model_family_receipt:
  - author_home_model_family: OpenAI / Codex, this commissioning lane.
  - controller_model_family: `operator_to_fill`; must be a different vendor / model lineage from OpenAI to satisfy `cross_vendor_discovery`.
  - current_receiving_actor_role: controller.
  - dispatch_mode: external-controller-courier.
  - de_correlation_status: operator must fill before review; block strict cross-vendor discovery claims if unsatisfied.
- de_correlation: this is a who-constraint, not a model recommendation. Do not recommend, rank, or prescribe a runtime model.
- subagent_authority: no tester/testee shortcut. The commissioning/home model must not satisfy this by reviewing its own patch. If your runtime is the same author/home family and no different-family controller is actually receiving this prompt, stop before review.
- prompt_rendering: this filed prompt is the orchestrated prompt. The receiver must inspect the pinned repo/worktree directly; do not substitute this prompt body, a summary, or a recreated source pack for the source tree.

### Target

- targets:
  - label: `[creator-profile-materializer-api]`
    path: `orca-harness/capture_spine/creator_profile_current/__init__.py`
    bounded_patch_scope: only package exports/docstring needed for the creator-profile-current materializer API.
  - label: `[creator-profile-materializer-core]`
    path: `orca-harness/capture_spine/creator_profile_current/materialize.py`
    bounded_patch_scope: only deterministic materialization from the account-linkage ledger and YouTube metric seed into the creator-profile-current view, including hash/source handling and validation calls.
  - label: `[creator-profile-materializer-runner]`
    path: `orca-harness/runners/run_creator_profile_current_materialize.py`
    bounded_patch_scope: only CLI check/write behavior for materializing or staleness-checking the checked-in creator-profile-current view.
  - label: `[creator-profile-materializer-tests]`
    path: `orca-harness/tests/unit/test_creator_profile_current_static_view.py`
    bounded_patch_scope: only parity/staleness coverage proving the materializer output matches the checked-in view and source hashes stay honest.
  - label: `[repo-map-route]`
    path: `docs/workflows/orca_repo_map_v0.md`
    bounded_patch_scope: only the route-map freshness entries for the new materializer and runner.
- why_read_only_insufficient: this PR creates the first deterministic refresh path for the one-stop creator profile view. If the reviewer finds a fake-pass, stale-output, source-hash, or source-backedness issue, a bounded correction inside the same five files is cheaper and safer than a review-only loop.
- off_scope: read-only / flag-only for all other files, including source ledger JSON rows, creator profile fixture data, product specs, SQLite/lake physicalization, live capture, schedulers, dashboards, identity stitching, engagement-rate derivation, broad validator framework extraction, unrelated repo-map rewrites, and all workflow overlay files.

When returning findings, diffs, or citations, carry the label tag for the affected target.

### Source-Gated Method Contract

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md` first.
2. REFERENCE-LOAD `workflow-delegated-review-patch`, `workflow-deep-thinking`, `workflow-code-review`, and, only for the repo-map route text, `workflow-adversarial-artifact-review`. Do not APPLY them yet.
3. SOURCE-LOAD the target source pack below.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before producing findings.
5. Only after source readiness, APPLY `workflow-delegated-review-patch` to enforce receipt, role, scope, patch, and CA-adjudication boundaries.
6. APPLY `workflow-deep-thinking` to frame fake-pass paths and material failure modes.
7. APPLY `workflow-code-review` to the implementation, runner, and tests.
8. APPLY `workflow-adversarial-artifact-review` only if needed to review a material repo-map route-text failure.
9. If `workflow-code-review` is unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE`; do not emulate a strict code review inline. If `workflow-adversarial-artifact-review` is unavailable, do not make strict artifact-review claims about the repo-map route; flag the limitation.

### Required Source Pack

Open and inspect these exact sources from the repo/worktree, not from pasted excerpts:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/decision-routing.md`
- `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`
- target diff: `git diff 2d08b747c720ed6dc0b1031ea5828b01663286b6..d8edd7862d9471ccc0b101266387f337d7bba967 -- docs/workflows/orca_repo_map_v0.md orca-harness/capture_spine/creator_profile_current/__init__.py orca-harness/capture_spine/creator_profile_current/materialize.py orca-harness/runners/run_creator_profile_current_materialize.py orca-harness/tests/unit/test_creator_profile_current_static_view.py`
- current target files at commit `d8edd7862d9471ccc0b101266387f337d7bba967`:
  - `docs/workflows/orca_repo_map_v0.md`
  - `orca-harness/capture_spine/creator_profile_current/__init__.py`
  - `orca-harness/capture_spine/creator_profile_current/materialize.py`
  - `orca-harness/runners/run_creator_profile_current_materialize.py`
  - `orca-harness/tests/unit/test_creator_profile_current_static_view.py`
- source ledgers and materialized output used by the implementation:
  - `orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_v0.json`
  - `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_seed_v0.json`
  - `orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_v0.json`
- adjacent validator/source behavior:
  - `orca-harness/capture_spine/creator_profile_current/validation.py`
  - `orca-harness/capture_spine/youtube_creator_observation/validation.py`, targeted to source hash/rebuild behavior.
  - `orca-harness/tests/unit/test_youtube_creator_metric_seed.py`, targeted to source hash checks.
- product/spec anchors for intended boundaries:
  - `orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md`, targeted to generated-view/source-of-truth/SQLite/lake boundaries.
  - `orca/product/spines/capture/core/source_families/social_media/creator_profile_current_lake_native_record_mapping_v0.md`, targeted to lake-native mapping and validator/source-backedness residuals.

Do not bulk-load unrelated review outputs, all prompt files, all product files, all data-lake directories, live capture artifacts, historical lanes, or external sources unless a specific material finding requires one narrow adjacent read.

### Review Questions

Find blocker or major issues first, especially:

- Does the materializer truly derive the checked-in creator profile view from the sibling account-linkage and metric-seed ledgers, or does it preserve hidden hand-authored fields that will silently stale?
- Does `--check` fail when either source ledger changes but the checked-in view is not refreshed?
- Does `--write` avoid timestamp churn by preserving the existing `generated_at_utc` when no explicit timestamp is supplied?
- Does the source-input hash behavior match the repository's LF-normalized source hash convention without pretending to prove source-backed metric truth?
- Does the join between platform accounts and rollups fail closed on missing or extra subjects, duplicate identities, missing metrics, or platform/account mismatches?
- Does the generated output still pass the structural/posture validator, and does the test prove exact parity with the checked-in view?
- Is the runner path-safe and repo-root-safe enough for local operator use without writing outside the intended output?
- Does the repo-map language accurately route the new materializer and runner without overclaiming live capture, SQLite adoption, person identity proof, or universal source-backed metrics?
- Does the implementation accidentally make the creator-profile view the source of truth rather than a materialized view over sibling ledgers?
- Does the patch stay inside the current PR scope, or did it smuggle scheduler, dashboard, lake, SQLite, engagement-rate, cross-platform stitching, live capture, or validator-framework commitments?

### Patch Authority

You may patch only the five target files listed above, and only to close blocker or major issues found in this review. Do not stage, commit, push, open PRs, install dependencies, run network access, run live capture, or edit source ledger data.

If the correct fix requires changing product specs, ledger JSON data, validator architecture, capture/lake producers, workflow overlay files, or a broader backend/scheduler design, do not patch it. Flag it as off-scope.

If a design-level problem is found, return `NEEDS_ARCHITECTURE_PASS`, stop patching, revert any partial diff, and report findings only. A partial patch must not survive by inertia.

### Validation Expectations

If you patch, run the narrowest relevant validation available, normally from `orca-harness`:

- `python runners\run_creator_profile_current_materialize.py --check`
- `python -m pytest tests\unit\test_creator_profile_current_static_view.py tests\unit\test_youtube_creator_metric_seed.py -q`

Also run from repo root when relevant:

- `git diff --check`
- `python .agents\hooks\check_repo_map_freshness.py --changed --strict` if the repo-map route changes.
- `python .agents\hooks\check_map_links.py --strict` if the repo-map route changes.

Run full `python -m pytest` from `orca-harness` only if your patch changes behavior beyond the materializer/join/check surface or if focused evidence becomes ambiguous. Report exact commands and results. Preserve real failures.

### Output Contract

Write the full review report to:

- `docs/review-outputs/adversarial-artifact-reviews/creator_profile_current_materializer_adversarial_code_review_v0.md`

If the report write fails, return a blocked chat result with `review_location: chat_only_current_thread`, no `report_path`, and enough detail to route.

Report structure:

1. Commission, lane binding, and actor/model-family receipt.
2. Source context status.
3. Findings first, ordered by severity: critical, major, minor.
4. For each finding: severity, target label, location, issue, evidence, impact, minimum_closure_condition, next_authorized_action, and whether patched.
5. Unified diff for any target-file changes.
6. Per-change neutral source citations that are decision-sufficient in substance.
7. Controller verdict and residual-risk note.
8. Validation run status, including exact commands run or not run.
9. Off-scope flags.
10. CA adjudication packet.
11. Review-use boundary.

After writing the report, return this compact chat YAML:

```yaml
review_summary:
  status: completed | blocked
  report_path: docs/review-outputs/adversarial-artifact-reviews/creator_profile_current_materializer_adversarial_code_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  reviewed_by: operator_to_fill
  authored_by: OpenAI Codex / GPT-5
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback | unrecorded
  same_vendor_rationale: "required if de_correlation_bar is same_vendor_sanity"
  summary: "One sentence."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  patch_status: no_patch_needed | patch_applied | patch_blocked | needs_architecture_pass
  changed_files: []
  validation_run: []
  validation_not_run: []
  residual_risk: "One sentence."
  next_action: "One concrete next step for the commissioning CA."
```

If no issues are found, say that clearly and name residual risks or test gaps. Your output is decision input only. The commissioning CA must adjudicate before any change is kept.

### Review-Use Boundary

This delegated review-and-patch result is decision input only. The controller's diff, citations, and verdict are claims to adjudicate, not premises to inherit. It is not owner acceptance, validation proof, readiness, deployment, source-capture authorization, live-lake authorization, SQLite adoption, or permission to keep any patch without Chief Architect adjudication.