# Creator Registry Scan Handoff Enforcement Delegated Adversarial Code Review Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Delegated adversarial code review and bounded patch prompt for PR #660's
  Creator Registry scan/capture handoff enforcement work unit.
use_when:
  - Reviewing PR #660 before merge after the CSB scanning artifact checker was
    extended to require Creator Registry match-preflight receipt fields on
    capture_request records.
  - Hardening the scan-to-capture duplicate-prevention bridge without widening
    into registry identity writes, capture execution, or live data collection.
authority_boundary: retrieval_only
```

## Prompt Preflight

- Output mode: `review-report`; write the durable review report to `docs/review-outputs/adversarial-artifact-reviews/creator_registry_scan_handoff_enforcement_delegated_adversarial_code_review_patch_v0.md`.
- Template kind: `none` for the concrete prompt body; this is the provisional `delegated_code_review_and_patch` sibling mode in `.agents/workflow-overlay/delegated-review-patch.md`, using the code review lane as the review method. The registered adversarial-artifact template is source guidance only for non-code artifact surfaces.
- Edit permission: bounded patch-only inside the named PR #660 target set below. Do not commit, push, merge, open/close PRs, run capture, write the external data lake, or edit the identity ledger.
- Target workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-registry-receipt-handoffs`.
- Target branch: `codex/creator-registry-receipt-handoffs`.
- Base: `origin/main`.
- PR: `https://github.com/eric-foo/orca/pull/660`.
- Worktree state expected at reviewer start: clean after the commissioning CA pushes this prompt and the enforcement patch. If dirty, report the dirty files and stop unless the dirty files are exactly your own permitted patch output.
- Prompt source: this file.
- Thread operating target continuity:

```yaml
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: prompt_for_same_pr_review_after_owner_redirect
  if_changed_reason: null
```

## Commission

Perform an adversarial implementation/code review of the whole PR #660 work unit, then apply only smallest-complete patches for confirmed defects inside the bounded target set. The work unit's intended outcome is narrow:

- scan/capture handoffs for a new social creator/account capture must carry the Creator Registry exact-match preflight receipt fields;
- downstream agents must not infer `new_capture` permission from `decision: new_candidate` or `action_status: allowed` alone;
- the CSB-first scanning artifact checker must mechanically fail closed on missing or contradictory handoff metadata;
- non-social capture requests must carry the explicit `not_applicable` boundary rather than omit the seam;
- this remains a shape/receipt enforcement gate only, not registry truth, capture authorization, buyer proof, fuzzy identity, route binding, or live capture.

## Source-Gated Method Contract

REFERENCE-LOAD the following method instructions first. Do not APPLY them yet; use them only to prepare a neutral source-reading lens.

- `workflow-deep-thinking`
- `workflow-code-review`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/prompt-orchestration.md` Source-Gated Method Contract and Review Prompt Defaults

Then SOURCE-LOAD the authority and task sources below. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before producing findings, recommendations, or patches. Only after that declaration, APPLY `workflow-deep-thinking` to frame material failure modes, then APPLY `workflow-code-review` to review the diff. Use prompt/artifact review checks only as supporting lenses for the changed docs/prompts; do not relabel this as an artifact-only review.

If `workflow-code-review` is unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` in the report rather than silently claiming it ran. If repository access is unavailable, return `BLOCKED_REPO_ACCESS_REQUIRED`; this commission is repo-mode.

## Required Source Reads

Authority and operating rules:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `docs/workflows/creator_registry_record_contract_handoff_v0.md` only for lane boundaries: no identity-ledger writes, no capture, no lake writes, posture/value honesty.

Contract and changed-task sources:

- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md`
- `orca-harness/docs/source_capture_agent_runbook.md`
- `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md`
- `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`
- `.agents/hooks/check_csb_scanning_artifact.py`
- `.agents/hooks/README.md`
- `docs/workflows/orca_repo_map_v0.md`
- `orca-harness/tests/unit/test_csb_scanning_artifact_validator.py`
- `orca-harness/tests/fixtures/csb_scanning_artifacts/valid_csb_first_scan.md`
- `orca-harness/tests/fixtures/csb_scanning_artifacts/bad_engagement_overclaim.md`

Baseline/context sources when needed to adjudicate behavior:

- `.github/workflows/ci.yml`
- `orca-harness/capture_spine/creator_profile_current/registry_match_preflight.py`
- `orca-harness/runners/run_creator_registry_match_preflight.py`
- `orca-harness/tests/unit/test_creator_registry_match_preflight.py`

Before reviewing, record in the report:

- current branch and observed HEAD SHA;
- dirty state;
- diff target used (`origin/main...HEAD` and any uncommitted changes if present);
- whether every named source exists;
- any source gap, and whether it blocks strict findings.

## Bounded Patch Scope

You may patch only these files:

- `.agents/hooks/check_csb_scanning_artifact.py`
- `.agents/hooks/README.md`
- `docs/workflows/orca_repo_map_v0.md`
- `orca-harness/tests/unit/test_csb_scanning_artifact_validator.py`
- `orca-harness/tests/fixtures/csb_scanning_artifacts/valid_csb_first_scan.md`
- `orca-harness/tests/fixtures/csb_scanning_artifacts/bad_engagement_overclaim.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md`
- `orca-harness/docs/source_capture_agent_runbook.md`
- `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md`
- `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`

Everything outside that set is read-only. Flag out-of-scope defects in the report with `next_authorized_action: CA decision or separate lane`; do not edit them.

Return `NEEDS_ARCHITECTURE_PASS` and stop patching if the smallest correct fix requires a broader capture-runner schema change, identity resolver redesign, fuzzy matching, route-binding authority, registry schema change, external data lake work, live capture, or CI architecture change outside the named target set.

## Adversarial Review Focus

Attack these failure modes first:

1. A scan artifact can still request a new social creator/account capture without a preserved Creator Registry preflight receipt.
2. A `classify` or `update_existing` receipt can be made to look like `new_capture` clearance.
3. `decision: new_candidate` plus `action_status: allowed` clears new capture when `can_start_new_capture` is missing, false, malformed, or from the wrong intended action.
4. `required_when: not_applicable` can be used as an escape hatch while still carrying `new_capture` or `can_start_new_capture: true` metadata.
5. The checker accepts placeholders such as `null_or_path`, `unknown`, or empty receipt paths for new social creator/account capture.
6. The checker overreaches into route authorization, registry truth, buyer proof, scan quality, fuzzy identity, or capture policy beyond mechanical handoff shape.
7. The docs and runbook describe a stricter/looser contract than the checker actually enforces.
8. The tests prove only happy paths and miss the dangerous bypasses above.
9. The CI hook path or repo-map note claims enforcement that CI does not actually run.
10. Prompt/review-routing mechanics are satisfied only cosmetically and would fail `check_review_routing.py` or prompt validation.

## Validation Obligations

After any patch, run the tight gates and record observed results:

```powershell
python -m py_compile .agents\hooks\check_csb_scanning_artifact.py
python -m pytest -q orca-harness\tests\unit\test_csb_scanning_artifact_validator.py
python .agents\hooks\check_csb_scanning_artifact.py --selftest
python .agents\hooks\check_csb_scanning_artifact.py --diff origin/main --strict
python .agents\hooks\check_retrieval_header.py --changed --strict
python .agents\hooks\header_index.py --strict --base origin/main
python .agents\hooks\check_handoff_pointers.py --strict --base origin/main
python .agents\hooks\check_dcp_receipt.py --strict --base origin/main
python .agents\hooks\check_review_routing.py --strict --base origin/main
python .agents\hooks\check_map_links.py --strict
python .agents\hooks\check_full_gt_claims.py --changed --strict
git diff --check
```

If a command is not run, record `not_run` with the reason. Do not claim validation, readiness, approval, or merge safety from these checks; they are observed gate results only.

For the delegated review report itself, after the final report write run:

```powershell
python .agents\hooks\check_review_output_provenance.py --strict docs\review-outputs\adversarial-artifact-reviews\creator_registry_scan_handoff_enforcement_delegated_adversarial_code_review_patch_v0.md
```

If the report changes after that command, rerun it before closeout.

## Output Contract

Write the durable report to `docs/review-outputs/adversarial-artifact-reviews/creator_registry_scan_handoff_enforcement_delegated_adversarial_code_review_patch_v0.md`.

The report must include:

- `review_summary` YAML with `status`, `report_path`, `recommendation`, `reviewed_by`, `authored_by`, `de_correlation_bar`, `same_vendor_rationale` when applicable, `findings_count`, `blocking_findings`, `advisory_findings`, and `next_action`.
- Source-read ledger with one line per required source and any source gaps.
- Findings first, ordered by severity, each with `minimum_closure_condition` and `next_authorized_action`.
- Patch summary and unified diff for any changes you applied.
- Validation evidence with exact commands and observed pass/fail/not-run results.
- Residual risks and non-claims.

Chat closeout after the report write should return only the compact courier YAML plus a short findings summary. The delegate's diff, findings, and verdict are decision input only; the commissioning CA adjudicates what to keep.