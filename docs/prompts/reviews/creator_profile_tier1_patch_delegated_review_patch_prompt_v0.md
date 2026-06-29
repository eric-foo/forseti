# Creator Profile Tier 1 Patch Delegated Review-And-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca delegated review-and-patch prompt
scope: >
  Commission a de-correlated repo-mode review-and-patch pass for the Tier 1
  creator-profile validator boundary patch on PR #439, pinned to commit
  da870aa5d1d0b9d5eeaa602f75a7aebeb6b669ba.
use_when:
  - Couriering the Tier 1 creator-profile validator boundary patch for independent review.
  - Checking whether the .gitattributes LF boundary, structural-only validator wording, and regression test introduce blocker or major issues.
authority_boundary: retrieval_only
branch_or_commit: codex/creator-metric-source-audit @ da870aa5d1d0b9d5eeaa602f75a7aebeb6b669ba
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/decision-routing.md
  - orca-harness/capture_spine/creator_profile_current/validation.py
  - orca-harness/tests/unit/test_creator_profile_current_static_view.py
  - .gitattributes
stale_if:
  - Target commit da870aa5d1d0b9d5eeaa602f75a7aebeb6b669ba is not reachable from the reviewed branch.
  - The target files change after da870aa5 before this delegated review runs, other than this prompt artifact itself.
  - PR #439 is retargeted away from codex/creator-metric-source-audit before review.
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0, constants bound; deltas stated here.

- output_mode: `file-write` for this prompt artifact, plus `paste-ready-chat` copy for couriering.
- prompt_artifact_path: `docs/prompts/reviews/creator_profile_tier1_patch_delegated_review_patch_prompt_v0.md`.
- template_kind: `review` plus delegated review-and-patch commission semantics from `.agents/workflow-overlay/delegated-review-patch.md`.
- authorization_basis: current owner invocation of `workflow-delegated-review-patch` after the Tier 1 patch landed on PR #439.
- edit_permission_for_receiver: patch-only inside the three target files below; all other paths are read-only / flag-only.
- workspace_path: `C:\Users\vmon7\Desktop\projects\orca`.
- expected_worktree_path: `C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-metric-source-audit`.
- branch_or_commit_reference: `codex/creator-metric-source-audit @ da870aa5d1d0b9d5eeaa602f75a7aebeb6b669ba`.
- reviewed_diff: `8cd0b6f4afbbfcf5a79f67efc85ca24987820a9b..da870aa5d1d0b9d5eeaa602f75a7aebeb6b669ba`.
- target_files_or_dirs:
  - `.gitattributes`
  - `orca-harness/capture_spine/creator_profile_current/validation.py`
  - `orca-harness/tests/unit/test_creator_profile_current_static_view.py`
- dirty_state_allowance: target worktree should be clean before the receiver starts. If this prompt file is present as a later commit, review the pinned target diff explicitly rather than reviewing unrelated prompt-file changes.
- doctrine_change_decision: no doctrine change intended; this is implementation/config/test hardening for an already accepted Tier 1 architecture decision.
- isolation_decision: existing lane worktree `worktrees/creator-metric-source-audit`; no new worktree required for a read/patch-only delegated pass.
- validation_evidence_already_observed:
  - `python -m pytest tests\unit\test_creator_profile_current_static_view.py tests\unit\test_youtube_creator_metric_seed.py -q` passed locally, 21 passed.
  - `python -m pytest` from `orca-harness` with `ORCA_DATA_ROOT` unset passed locally, 1788 passed, 4 skipped, 1 warning.
  - PR #439 `orca-harness-tests` passed on commit da870aa5, GitHub Actions run `28363216425`, job `84022633232`.
- receiver_validation_expectation: rerun focused tests for any patch, and run at least `git diff --check`; rerun full `orca-harness` pytest only if the receiver changes behavior beyond comments/tests/attributes or if focused evidence becomes ambiguous.
- thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
  if_changed_reason: not_applicable

## Delegated Review-And-Patch Commission

### Lane Binding

- overlay_status: `provisional_opt_in`, explicitly invoked by the owner for this patch.
- operating_contract_pointer: `.agents/workflow-overlay/delegated-review-patch.md`.
- review_lane: code / implementation change packet, use `workflow-code-review` after source readiness.
- mode: `base-subagent` / repo-mode controller. Do not use split-executor.
- actor_model_family_receipt:
  - author_home_model_family: OpenAI / Codex, this commissioning lane.
  - controller_model_family: `operator_to_fill`; must be a different vendor / model lineage from OpenAI to satisfy `cross_vendor_discovery`. If not different-vendor, record `same_vendor_sanity` and do not claim discovery or no-new-seam.
  - current_receiving_actor_role: controller.
  - dispatch_mode: external-controller-courier.
  - de_correlation_status: operator must fill before review; block strict cross-vendor discovery claims if unsatisfied.
- de_correlation: this is a who-constraint, not a model recommendation. Do not recommend, rank, or prescribe a runtime model.
- subagent_authority: no tester/testee shortcut. The commissioning/home model must not satisfy this by reviewing its own patch.
- prompt_rendering: this filed prompt is the orchestrated prompt. The receiver must inspect the pinned repo/worktree directly; do not substitute this prompt body, a summary, or a recreated source pack for the source tree.

### Target

- targets:
  - label: `[gitattributes-lf-boundary]`
    path: `.gitattributes`
    bounded_patch_scope: only the LF repo-text rules for creator profile / metric seed source-input JSON files and their interaction with the existing `**/source_captures/** -text` rule.
  - label: `[creator-profile-validator-docstring]`
    path: `orca-harness/capture_spine/creator_profile_current/validation.py`
    bounded_patch_scope: only the module-level guarantee wording that states structural/posture scope and non-claims.
  - label: `[creator-profile-static-view-tests]`
    path: `orca-harness/tests/unit/test_creator_profile_current_static_view.py`
    bounded_patch_scope: only the new git-attribute regression helper/test and directly required import/formatting.
- why_read_only_insufficient: this patch changes guardrail behavior at a cross-platform source-hash boundary. If a reviewer finds a real issue, a bounded correction inside the same three files is cheaper and safer than a review-only loop.
- off_scope: read-only / flag-only for all other files, broader validator framework extraction, shared hash utilities, source-rebuild validators, SQLite/lake work, live-lake validation, dashboard validation, engagement-rate derivation, and cross-platform identity stitching.

When returning findings, diffs, or citations, carry the label tag for the affected target.

### Source-Gated Method Contract

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md` first.
2. REFERENCE-LOAD `workflow-deep-thinking`. Do not APPLY it yet.
3. REFERENCE-LOAD `workflow-code-review`. Do not APPLY it yet.
4. SOURCE-LOAD the target source pack below.
5. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before producing findings.
6. Only after source readiness, APPLY `workflow-deep-thinking` to frame failure modes, then APPLY `workflow-code-review` to review the pinned diff and any bounded patch you produce.
7. If `workflow-code-review` is unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE`; do not emulate a strict code review inline.

### Required Source Pack

Open and inspect these exact sources from the repo/worktree, not from pasted excerpts:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/decision-routing.md`
- target diff: `git diff 8cd0b6f4afbbfcf5a79f67efc85ca24987820a9b..da870aa5d1d0b9d5eeaa602f75a7aebeb6b669ba -- .gitattributes orca-harness/capture_spine/creator_profile_current/validation.py orca-harness/tests/unit/test_creator_profile_current_static_view.py`
- current target files at commit `da870aa5d1d0b9d5eeaa602f75a7aebeb6b669ba`:
  - `.gitattributes`
  - `orca-harness/capture_spine/creator_profile_current/validation.py`
  - `orca-harness/tests/unit/test_creator_profile_current_static_view.py`
- adjacent sibling for hash/source behavior:
  - `orca-harness/capture_spine/youtube_creator_observation/validation.py`, targeted to `_validate_source_input_hashes`, `_read_source_input_bytes`, and `validate_source_rebuild`.
  - `orca-harness/tests/unit/test_youtube_creator_metric_seed.py`, targeted to `_sha256` and source hash checks.
- product/spec anchors for accepted non-goals:
  - `orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md`, targeted to `SQLite And Data Lake Boundary`.
  - `orca/product/spines/capture/core/source_families/social_media/creator_profile_current_lake_native_record_mapping_v0.md`, targeted to `Validator Target` and accepted residuals.

Do not bulk-load unrelated review outputs, all prompt files, all product files, or historical lanes unless a specific finding requires one more source.

### Review Questions

Find blocker or major issues in the Tier 1 patch, especially:

- Does the `.gitattributes` rule actually protect the source-input JSON files whose `sha256` values are LF repo-text hashes?
- Does the `.gitattributes` rule accidentally weaken `source_captures/** -text` or another byte-faithful evidence rule?
- Does the new regression test fail closed enough to catch a future removal or override of the LF boundary?
- Does the docstring truthfully state what `creator_profile_current` validation does and does not prove, without overclaiming source truth, readiness, validation, or source-rebuild coverage?
- Does the patch stay inside Tier 1, or did it accidentally create framework, SQLite/lake, live-lake, engagement-rate, or cross-platform identity commitments?
- Is there a simpler correction needed inside the three target files to avoid a fake-pass or future CI-only line-ending failure?

### Patch Authority

You may patch only the three target files listed above, and only to close blocker or major issues found in this review. Do not commit. Do not edit prompts, docs, product specs, workflow overlay files, source-capture packets, generated artifacts, or unrelated tests.

If the correct fix requires off-scope files or a design-level change, return `NEEDS_ARCHITECTURE_PASS` or an off-scope finding and leave the working tree unchanged apart from reverting any partial patch.

### Output Contract

Return a courier-ready result in this shape:

```yaml
review_summary:
  status: completed | blocked
  review_location: chat_only_current_thread
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  reviewed_by: operator_to_fill
  authored_by: OpenAI Codex / GPT-5
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback | unrecorded
  same_vendor_rationale: "required if de_correlation_bar is same_vendor_sanity"
  summary: "One sentence."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  patch_status: no_patch_needed | patch_applied | patch_blocked | needs_architecture_pass
  changed_files: []
  validation_run: []
  validation_not_run: []
  residual_risk: "One sentence."
  next_action: "One concrete next step for the commissioning CA."
```

Then provide findings first, ordered by severity. For each finding include severity, target label, location, issue, evidence with file/line citation, impact, minimum_closure_condition, and next_authorized_action.

If you patch, include:

- unified diff of the working-tree changes;
- per-change source citations, tagged with the target label;
- validation evidence or explicit not-run status;
- residual-risk note.

If no issues are found, say that clearly and list residual risks or test gaps. Your output is decision input only. The commissioning CA must adjudicate before any change is kept.