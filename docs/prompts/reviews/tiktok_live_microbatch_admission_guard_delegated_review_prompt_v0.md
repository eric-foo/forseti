# TikTok Live Microbatch Admission Guard Delegated Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Repo-bound delegated adversarial code review-and-patch prompt for PR #608's
  TikTok live microbatch blocker-routing, visual-X diagnostic, and batch-admission guards.
use_when:
  - An independent receiving lane is asked to review the TikTok live microbatch gate repair branch.
  - A de-correlated or explicitly bounded same-vendor sanity reviewer needs the exact target files and return contract.
  - The reviewer may patch only the named target files and must not run live TikTok actions.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - docs/workflows/tiktok_live_microbatch_owner_gated_handoff_v0.md
  - docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md
  - orca-harness/source_capture/tiktok/live_batch_probe.py
  - orca-harness/source_capture/tiktok/batch_packet.py
  - orca-harness/tests/unit/test_tiktok_live_batch_probe.py
  - orca-harness/tests/unit/test_tiktok_batch_admission.py
branch_or_commit: >
  codex/tiktok-live-microbatch-gate-repair target patch head
  7979edc55b87513253b7fc5f2c21ff332ad54751; a prompt-only commit may sit on top.
stale_if:
  - Any target file listed in this prompt changes after 7979edc55b87513253b7fc5f2c21ff332ad54751.
  - PR #608 branch head changes after this prompt is committed for reasons other than prompt/report artifacts.
  - The owner changes the no-CAPTCHA-solving, no-auth-inspection, or challenge-close-is-stop policy.
```

## Prompt Preflight

- prompt_artifact_path: `docs/prompts/reviews/tiktok_live_microbatch_admission_guard_delegated_review_prompt_v0.md`
- output_mode: review-report
- review_report_destination: `docs/review-outputs/adversarial-artifact-reviews/tiktok_live_microbatch_admission_guard_delegated_review_v0.md` unless the operator names another Orca-owned path.
- template_kind: repo-bound adversarial code review with bounded patch option.
- template_source: prompt-orchestrator contract plus Orca review-lanes/delegated-review-patch overlay; no runtime model recommendation is made.
- edit_permission: patch-only inside the target files below, and only after the receiving actor records its role and de-correlation bar. Otherwise read-only.
- workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\tiktok-bounded-pointer-action`
- expected_branch: `codex/tiktok-live-microbatch-gate-repair`
- target_patch_head: `7979edc55b87513253b7fc5f2c21ff332ad54751`
- branch_head_note: a prompt-only commit may exist on top; if any target file differs from `7979edc55b87513253b7fc5f2c21ff332ad54751`, stop and refresh this prompt.
- dirty_state_allowance: `_scratch/` may be untracked. The prompt file itself may be present. Any dirty target file at start is a blocker unless it is the reviewer's own patch.
- live_run_permission: none. Do not run TikTok, open browser sessions, inspect auth state, print cookies/storage, or solve/close CAPTCHA except by reviewing existing code/tests.

## Actor / De-Correlation Receipt

Fill before review:

```yaml
actor_model_family_receipt:
  authored_by_family: OpenAI/GPT-family Codex lane
  controller_family: operator_to_fill
  current_receiving_actor_role: controller | patch-executor | home-dispatcher
  dispatch_mode: external-controller-courier
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback
  de_correlation_status: satisfied | bounded_sanity_only | blocked
  same_vendor_rationale: operator_to_fill_when_same_vendor
```

If the receiving controller is not different-family from the author, do not claim cross-vendor discovery or no-new-seam review. A same-family reviewer may run only bounded sanity if the operator accepts that limitation. A self-review fallback is not delegated review.

## Target Scope

Review the current branch/PR #608 diff with emphasis on commits:

- `2f55eb6a Gate TikTok visual close diagnostic on challenge text`
- `7979edc5 Reject TikTok diagnostic cadence in batch admission`

Patch scope is limited to these files:

- `docs/workflows/tiktok_live_microbatch_owner_gated_handoff_v0.md`
- `docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_sessioned_capture_warm_probe_plan_v0.md`
- `orca-harness/source_capture/tiktok/live_batch_probe.py`
- `orca-harness/source_capture/tiktok/batch_packet.py`
- `orca-harness/tests/unit/test_tiktok_live_batch_probe.py`
- `orca-harness/tests/unit/test_tiktok_batch_admission.py`

Everything else is read-only / flag-only. Do not commit or push. Leave `_scratch/` untracked and do not depend on it except as optional existing diagnostic evidence.

## Required Method Sequence

1. REFERENCE-LOAD `workflow-code-review` if available. Do not APPLY it before source readiness.
2. SOURCE-LOAD the files in `open_next`, the target files, current `git status --short --branch`, and the branch diff against the appropriate base.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources.
4. APPLY code-review judgment after source readiness.
5. If patching is authorized and a blocker/major issue is found inside target scope, patch the smallest complete fix. If the correct fix is outside scope, do not edit; return `NEEDS_ARCHITECTURE_PASS` or an off-scope finding.
6. Run validation that can fail; at minimum:
   - `python -m py_compile orca-harness\source_capture\tiktok\live_batch_probe.py orca-harness\source_capture\tiktok\batch_packet.py orca-harness\tests\unit\test_tiktok_live_batch_probe.py orca-harness\tests\unit\test_tiktok_batch_admission.py`
   - `$env:PYTHONPATH='orca-harness'; python -m pytest -q orca-harness\tests\unit\test_source_capture_browser_snapshot.py orca-harness\tests\unit\test_tiktok_blocker_triage.py orca-harness\tests\unit\test_tiktok_live_batch_probe.py orca-harness\tests\unit\test_tiktok_batch_admission.py`
   - `git diff --check`

## Review Questions

Find blocker or major issues in these claims:

- The visual-X diagnostic can run only when `--allow-challenge-close-diagnostic` is set and visible challenge/security text matches.
- The visual-X diagnostic is not a generic upper-right clicker and cannot close unrelated non-challenge UI.
- Any clicked challenge-close diagnostic forces stop semantics and cannot create a completed row, success claim, batch expansion, or product extraction.
- Batch admission rejects non-clean live cadence before producing a packet: nonzero `challenge_count`, non-empty `failures`, `first_failure_reason`, `captcha_solving=true`, `challenge_close_counts_as_success=true`, and `challenge_close_diagnostic_allowed=true`.
- The tests cover the live recurrence class where a diagnostic click is followed by page-owned comment-list traffic but remains diagnostic-only.
- The docs and handoff do not overclaim clean capture, validation, readiness, product extraction, scale, or challenge resolution.
- No code path inspects, prints, commits, or persists auth cookies/storage beyond normal ignored auth-state loading.

Minor style findings are optional. Do not generate a broad refactor list.

## Return Contract

Return findings first. Use this exact summary block before details:

```yaml
review_summary:
  source_context: SOURCE_CONTEXT_READY | SOURCE_CONTEXT_INCOMPLETE
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback
  de_correlation_status: satisfied | bounded_sanity_only | blocked
  verdict: no_blocker_or_major_found | patched_blocker_or_major | blocker_or_major_found_unpatched | needs_architecture_pass | blocked
  patch_applied: yes | no
  changed_files:
    - path: ...
      reason: ...
  validation:
    py_compile: pass | fail | not_run
    targeted_pytest: pass | fail | not_run
    diff_check: pass | fail | not_run
  residual_risk: ...
```

For each finding, include:

- severity: blocker | major | minor
- file and line reference
- evidence
- impact
- minimum_closure_condition
- next_authorized_action

If a patch is applied, include a concise diff summary and validation output. Do not claim approval, readiness, merge safety, or validation beyond observed command results. The review is decision input for the home/CA lane, not automatic acceptance.
