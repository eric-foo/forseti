# TikTok Bounded Pointer Action Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed cross-recipient prompt for a read-only adversarial code review of the
  TikTok bounded pointer-action implementation: typed browser pointer action,
  TikTok live-probe wiring, and capped comment-list admission.
use_when:
  - Commissioning a de-correlated reviewer after the bounded pointer-action PR is opened.
  - Checking whether the implementation is deterministic, observable, sanitized, and stop-on-challenge compatible.
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/validation-gates.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
  - orca-harness/source_capture/adapters/browser_snapshot.py
  - orca-harness/source_capture/tiktok/live_batch_probe.py
  - orca-harness/tests/unit/test_source_capture_browser_snapshot.py
  - orca-harness/tests/unit/test_tiktok_live_batch_probe.py
  - orca-harness/source_capture/tiktok/batch_packet.py
  - orca-harness/source_capture/tiktok/admission.py
authoring_branch: codex/tiktok-bounded-pointer-action
authoring_base_observed: origin/main @ 82613874bb45fcb7fd4209de6eaf2501d21729eb
stale_if:
  - The reviewer cannot identify the PR/branch head being reviewed.
  - Any target source/test file differs from the PR/branch head under review.
  - The implementation diff includes files outside the declared target scope, except this prompt artifact.
authority_boundary: retrieval_only
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

- output_mode: `review-report`
- prompt_artifact_path: `docs/prompts/reviews/tiktok_bounded_pointer_action_adversarial_code_review_prompt_v0.md`
- review_report_destination: `docs/review-outputs/tiktok_bounded_pointer_action_adversarial_code_review_v0.md`
- template_kind: `review`; Orca has no bound repo-code-review template, so this prompt uses the overlay review contract directly.
- authorization_basis: owner requested `assumption gate fused (delegate prompt after)` for the bounded pointer-action plan.
- edit_permission: `read-only`; reviewer may write only the review report at the destination above.
- expected_worktree: repo-backed checkout or worktree for branch `codex/tiktok-bounded-pointer-action`.
- expected_branch: `codex/tiktok-bounded-pointer-action` unless the dispatcher supplies a PR checkout that resolves to the same branch head.
- expected_head: derive from `git rev-parse HEAD` at dispatch; do not trust this prompt for the final head SHA.
- expected_pr: `https://github.com/eric-foo/orca/pull/575` (draft at prompt update).
- dirty_state_allowance: prompt/report docs may be dirty or untracked. Target source/test files must be clean relative to the reviewed head.
- target_files_or_dirs:
  - `orca-harness/source_capture/adapters/browser_snapshot.py`
  - `orca-harness/source_capture/tiktok/live_batch_probe.py`
  - `orca-harness/tests/unit/test_source_capture_browser_snapshot.py`
  - `orca-harness/tests/unit/test_tiktok_live_batch_probe.py`
  - Read-only compatibility context: `orca-harness/source_capture/tiktok/batch_packet.py`, `orca-harness/source_capture/tiktok/admission.py`.
- validation_gates:
  - Verify branch, HEAD, target diff, and dirty state before strict findings.
  - Run only offline tests/compilation/checks unless blocked by local tooling.
  - Do not run live TikTok, browser capture against TikTok, network capture, auth-state refresh, or creator micro-batches.
  - Do not print cookies, tokens, proxy values, storage-state contents, raw TikTok CDN URLs, raw query secrets, or raw pointer coordinates.
- doctrine_change_decision: no doctrine change requested. Return `NEEDS_ARCHITECTURE_PASS` for doctrine-level concerns; do not edit doctrine.
- isolation_decision: reviewer uses existing PR/worktree; no new writing branch required for read-only review.

## Commission

You are the de-correlated controller for a read-only adversarial code review. The reviewed patch was authored by an OpenAI/GPT-family Codex agent. To satisfy the discovery bar, your controller vendor/model lineage must be different from OpenAI/GPT-family. This is a who-constraint, not a runtime model recommendation.

If you are OpenAI/GPT-family, same-vendor, self-reviewing, or your lineage is unknown, stop and return:

```text
BLOCKED_CONTROLLER_NOT_DECORRELATED
```

If you do not have filesystem access to the expected repo/worktree, stop and request a repo-backed source capsule or no-repo handoff. Do not review from this prompt summary alone.

Your task is to decide whether the bounded pointer-action implementation is safe, scoped, and truthfully claimed before merge. Findings are decision input only; they are not approval, validation, mandatory remediation, merge authority, or patch authority.

## Required Method Sequence

1. Read this prompt.
2. REFERENCE-LOAD `workflow-deep-thinking`. Do not APPLY it yet.
3. REFERENCE-LOAD `workflow-code-review`. Do not APPLY it yet.
4. SOURCE-LOAD the authority and task sources below.
5. Declare `SOURCE_CONTEXT_READY` with a compact source-read ledger, or `SOURCE_CONTEXT_INCOMPLETE` with missing sources and blocked claims.
6. Only after source readiness, APPLY `workflow-deep-thinking` to frame the highest-risk failure modes.
7. Then APPLY `workflow-code-review` to review the implementation and tests.
8. Write findings first. Do not patch.

If either method is unavailable, name that fact. You may still provide advisory-only critique, but do not emit strict review claims, readiness claims, validation claims, mandatory remediation, or merge recommendations as if the method contract was satisfied.

## Confirm-Do-Not-Trust Load Contract

Do not trust any implementation facts in this prompt until you verify them from the repo and files.

Before strict or actionable claims:

1. Run `git rev-parse HEAD` and record the reviewed target commit.
2. Run `git status --short --branch` and confirm the reviewed branch/head and that target source/test files are clean relative to that head. Prompt/report docs may be dirty only if you explicitly exclude them from source findings.
3. Run `git diff --name-only origin/main...HEAD` or the PR base equivalent and confirm the implementation target diff is limited to:
   - `orca-harness/source_capture/adapters/browser_snapshot.py`
   - `orca-harness/source_capture/tiktok/live_batch_probe.py`
   - `orca-harness/tests/unit/test_source_capture_browser_snapshot.py`
   - `orca-harness/tests/unit/test_tiktok_live_batch_probe.py`
   - this prompt artifact, if included in the branch.
4. Read the target files and required context below. Do not make source-backed claims from commit messages, PR text, prior thread summaries, or this prompt alone.

If the branch, HEAD, target scope, or disallowed dirty state does not match, return `BLOCKED_TARGET_MISMATCH` with observed values.

## Required Authority Sources

Read these before strict findings:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-loading.md`
4. `.agents/workflow-overlay/prompt-orchestration.md`
5. `.agents/workflow-overlay/review-lanes.md`
6. `.agents/workflow-overlay/validation-gates.md`
7. `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
8. `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
9. `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md`

Then source-load the code and compatibility context:

1. `orca-harness/source_capture/adapters/browser_snapshot.py`
2. `orca-harness/source_capture/tiktok/live_batch_probe.py`
3. `orca-harness/tests/unit/test_source_capture_browser_snapshot.py`
4. `orca-harness/tests/unit/test_tiktok_live_batch_probe.py`
5. `orca-harness/source_capture/tiktok/batch_packet.py`
6. `orca-harness/source_capture/tiktok/admission.py`

## Observed Patch Intent To Verify

Treat this as orientation only until source-verified:

- Adds a typed `BrowserPagePointerAction` accepted by `fetch_browser_page_observation_capture` and the Playwright observation engine.
- Rejects simultaneous raw `post_load_action_script` and typed pointer action.
- Locates the target by selector plus text markers inside the page, but returns only sanitized target telemetry to Python.
- Moves the Playwright mouse in bounded seeded steps and clicks inside the target box; receipts must not persist raw text or raw coordinates.
- Wires TikTok live probe comment opening to `tiktok_open_comments_pointer_v0` instead of injecting a DOM `click()` script.
- Caps admitted page-owned TikTok `/api/comment/list` responses to two per video while preserving observed match/admission counts truthfully.
- Keeps stop-on-challenge behavior and existing staging-to-batch admission compatibility.

## Observed Validation To Verify

Prompt-author observed validation:

```powershell
python -m compileall -q orca-harness\source_capture\adapters\browser_snapshot.py orca-harness\source_capture\tiktok\live_batch_probe.py orca-harness\tests\unit\test_source_capture_browser_snapshot.py orca-harness\tests\unit\test_tiktok_live_batch_probe.py
```

Observed result: pass.

```powershell
python -m pytest -q orca-harness\tests\unit\test_source_capture_browser_snapshot.py orca-harness\tests\unit\test_tiktok_live_batch_probe.py orca-harness\tests\unit\test_tiktok_batch_admission.py orca-harness\tests\unit\test_tiktok_video_admission.py
```

Observed result: `60 passed`.

```powershell
git diff --check
```

Observed result: exit 0, with only LF-to-CRLF warnings on touched files.

No live TikTok/browser/network run was performed for this implementation prompt. Do not upgrade offline tests into live capture, cross-creator, account-safety, product-value, comment-yield, or subtitle-yield claims.

## Review Checks

Be adversarial inside this target. Focus on material bugs, false-success paths, overbroad capture, secret leakage, and tests that would pass without proving the intended behavior.

Answer at least:

1. Does `BrowserPagePointerAction` stay deterministic, bounded, and observable, or can invalid config create unbounded movement, retries, hidden JS behavior, or fake success?
2. Can pointer target lookup, mouse movement, or receipt serialization leak raw UI text, raw coordinates, storage paths, cookies, tokens, proxy data, auth state, raw TikTok URLs, or query secrets?
3. Does mutual exclusion with `post_load_action_script` preserve the existing script path while preventing double action execution?
4. Are lookup/click failures visible as sanitized receipt failures rather than fake clicked success or swallowed behavior?
5. Does the TikTok wiring use only the typed pointer action and avoid anti-detection/human-mimicry claims?
6. Does the seeded movement avoid cursor teleport within the narrow operational need without becoming an evasion feature or a scale/safety claim?
7. Does the comment-list cap admit only the first two page-owned GET fetch/xhr TikTok comment-list bodies while truthfully reporting total observed matches and admitted count?
8. Does batch admission remain compatible with the staged rows produced by the live probe?
9. Do tests fail under the old behavior and exercise pointer lookup, mouse move/click order, no-target handling, receipt sanitation, TikTok wiring, and response capping without live browser/network dependency?
10. Is any issue design-level enough to return `NEEDS_ARCHITECTURE_PASS` instead of a patch request?

## Drift Guard

Do not perform or request:

- live TikTok/browser/network capture;
- a 1-creator smoke or 3-5 creator micro-batch;
- auth-state refresh, cookie inspection, proxy/session changes, or storage-state reads;
- product mention extraction, product-value analysis, creator/business judgment, or scale claims;
- patching source files;
- broad repo cleanup, prompt-template changes, or overlay doctrine changes;
- merge, commit, push, or PR state changes.

## Allowed Validation

You may run offline validation from the reviewed worktree:

```powershell
python -m compileall -q orca-harness\source_capture\adapters\browser_snapshot.py orca-harness\source_capture\tiktok\live_batch_probe.py orca-harness\tests\unit\test_source_capture_browser_snapshot.py orca-harness\tests\unit\test_tiktok_live_batch_probe.py
```

```powershell
python -m pytest -q orca-harness\tests\unit\test_source_capture_browser_snapshot.py orca-harness\tests\unit\test_tiktok_live_batch_probe.py orca-harness\tests\unit\test_tiktok_batch_admission.py orca-harness\tests\unit\test_tiktok_video_admission.py
```

```powershell
git diff --check
```

`gh pr checks` is optional if GitHub access is already available. If blocked by network/proxy/tooling, report `not_run`; do not treat that as a code finding.

## Output Contract

Write the durable report to:

`docs/review-outputs/tiktok_bounded_pointer_action_adversarial_code_review_v0.md`

The report must include:

- retrieval header with `authority_boundary: retrieval_only`;
- `reviewed_by` and `authored_by` fields in the body; use `unrecorded` only if not supplied, never fabricate;
- `de_correlation_bar: cross_vendor_discovery`;
- source-read ledger with file paths and line references for load-bearing claims;
- findings first, ordered by severity: `critical`, `major`, `minor`;
- for each finding: severity, location, issue, evidence with file:line cites, impact, minimum closure condition, next authorized action, and whether a patch is requested from the authoring lane;
- explicit answers to the Review Checks above;
- validation commands and observed outputs, or `not_run` reasons;
- residual risks;
- review-use boundary.

Do not include `patch_queue_entry`. Do not edit source files.

After writing the report, return this compact chat summary:

```yaml
review_summary:
  status: completed | failed | blocked
  review_location: durable_report | chat_only_current_thread
  report_path:
  reviewed_by:
  authored_by: OpenAI/GPT-family Codex
  de_correlation_bar: cross_vendor_discovery
  target_commit: <observed git rev-parse HEAD>
  pr: <observed PR URL or not_available>
  validation_run:
    compileall: run | not_run
    pytest: run | not_run
    diff_check: run | not_run
    pr_checks: run | not_run
  top_findings:
    - severity:
      issue:
      location:
  recommendation: merge_after_green | patch_before_merge | keep_draft | needs_architecture_pass | blocked
  next_action:
```

Review-use boundary:
This review is decision input only. It is not approval, validation, readiness, mandatory remediation, implementation authorization, merge authority, or executor-ready patch authority until separately accepted or authorized by the Orca owner / Chief Architect.
