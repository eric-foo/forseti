# TikTok Comment Response Capture Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed cross-recipient prompt for a read-only adversarial code review of PR #559,
  TikTok live comment response capture hardening.
use_when:
  - Commissioning a de-correlated reviewer to attack PR #559 before merge.
  - Checking whether the live probe comment-response hardening is safe, scoped, and honestly claimed.
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
  - orca-harness/source_capture/adapters/browser_snapshot.py
  - orca-harness/source_capture/tiktok/live_batch_probe.py
  - orca-harness/source_capture/tiktok/batch_packet.py
  - orca-harness/source_capture/tiktok/admission.py
branch_or_commit: codex/tiktok-comment-body-capture-probe @ f8a30acccaa61b18c144872d8fe28191cfeaa84b
stale_if:
  - PR #559 head commit changes.
  - Any target source/test file changes after f8a30acccaa61b18c144872d8fe28191cfeaa84b.
  - A later live TikTok run supersedes the cited control artifacts.
authority_boundary: retrieval_only
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

- output_mode: `review-report`
- prompt_artifact_path: `docs/prompts/reviews/tiktok_comment_response_capture_adversarial_code_review_prompt_v0.md`
- review_report_destination: `docs/review-outputs/tiktok_comment_response_capture_adversarial_code_review_v0.md`
- template_kind: `review`; Orca has no bound `repo-code-review` template, so this prompt uses the overlay review contract directly rather than inventing a template.
- template_source: `.agents/workflow-overlay/prompt-orchestration.md` plus `.agents/workflow-overlay/review-lanes.md`; no runtime model routing is implied.
- authorization_basis: owner request for a delegated adversarial review prompt after PR #559 was opened.
- edit_permission: `read-only`; reviewer may write only the review report at the destination above.
- target_files_or_dirs:
  - `orca-harness/source_capture/adapters/browser_snapshot.py`
  - `orca-harness/source_capture/tiktok/live_batch_probe.py`
  - `orca-harness/tests/unit/test_source_capture_browser_snapshot.py`
  - `orca-harness/tests/unit/test_tiktok_live_batch_probe.py`
  - Read-only compatibility context: `orca-harness/source_capture/tiktok/batch_packet.py`, `orca-harness/source_capture/tiktok/admission.py`
  - Read-only live/offline evidence paths named below, if present.
- source_pack: custom TikTok live-comment capture review pack named in this prompt; expand only when a missing source could change a material finding.
- dirty_state_allowance: prompt/report docs may be dirty or untracked. The four target implementation/test files must match the expected head unless the reviewer explicitly reports the mismatch and blocks strict review.
- expected_worktree: `C:\tmp\orca-tiktok-live-smoke-main`
- expected_branch: `codex/tiktok-comment-body-capture-probe`
- expected_head_at_prompt_authoring: `f8a30acccaa61b18c144872d8fe28191cfeaa84b`
- expected_pr: `https://github.com/eric-foo/orca/pull/559`
- expected_pr_state_at_prompt_authoring: open draft PR, base `main`, head branch `codex/tiktok-comment-body-capture-probe`, head OID `f8a30acccaa61b18c144872d8fe28191cfeaa84b`; `orca-harness-tests` observed passing.
- doctrine_change_decision: no doctrine change requested. If review finds a doctrine-level issue, return it as `NEEDS_ARCHITECTURE_PASS`; do not edit doctrine.
- isolation_decision: neither branch nor worktree creation for the reviewer; this is read-only review plus report write.
- validation_gates:
  - Verify branch, HEAD, target diff, and dirty state before strict findings.
  - Run only offline tests/compilation/checks unless blocked by local tooling.
  - Do not run live TikTok, browser capture, Playwright, network capture, auth-state refresh, or any 3-5 creator micro-batch.
  - Do not print cookies, tokens, proxy values, storage-state contents, raw TikTok CDN URLs, or raw query secrets.
- thread_operating_target_continuity: no visible active `thread_operating_target` is supplied in this prompt; omitted.

## Commission

You are the de-correlated controller for a read-only adversarial code review. The reviewed patch was authored by an OpenAI/GPT-family Codex agent. To satisfy the discovery bar, your controller vendor/model lineage must be different from OpenAI/GPT-family. This is a who-constraint, not a runtime model recommendation.

If you are OpenAI/GPT-family, same-vendor, self-reviewing, or your lineage is unknown, stop and return:

```text
BLOCKED_CONTROLLER_NOT_DECORRELATED
```

If you do not have filesystem access to the expected worktree, stop and request a repo-backed source capsule or no-repo handoff. Do not review from this prompt summary alone.

Your task is to decide whether PR #559 is safe, scoped, and truthfully claimed before merge. Findings are decision input only; they are not approval, validation, mandatory remediation, merge authority, or patch authority.

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

1. Run `git rev-parse HEAD` in `C:\tmp\orca-tiktok-live-smoke-main` and confirm it is `f8a30acccaa61b18c144872d8fe28191cfeaa84b`.
2. Run `git status --short --branch` and confirm the branch is `codex/tiktok-comment-body-capture-probe`; prompt/report docs may be dirty, but target source/test files must be unchanged unless you block and report the mismatch.
3. Run `git diff --name-only 0b17593a9cdd8c1b06344d3041d8bc81f1135e8d..HEAD` and confirm the implementation diff is exactly:
   - `orca-harness/source_capture/adapters/browser_snapshot.py`
   - `orca-harness/source_capture/tiktok/live_batch_probe.py`
   - `orca-harness/tests/unit/test_source_capture_browser_snapshot.py`
   - `orca-harness/tests/unit/test_tiktok_live_batch_probe.py`
4. Read the target files and required context below. Do not make source-backed claims from commit messages, PR text, prior thread summaries, or this prompt alone.

If the branch, HEAD, target scope, or disallowed dirty state does not match, return `BLOCKED_TARGET_MISMATCH` with the observed values.

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

Optional read-only evidence, if present:

1. `C:\tmp\orca-tiktok-live-smoke-output\tiktok_control_patch_probe_20260702T000000Z\tiktok_live_cadence_result.json`
2. `C:\tmp\orca-tiktok-live-smoke-output\tiktok_control_patch_probe_packet_20260702T000000Z`
3. `C:\tmp\orca-tiktok-live-smoke-output\tiktok_control_patch_probe_wait_20260702T000000Z\tiktok_live_cadence_result.json`

If optional evidence is absent, mark it `not_available`; do not recreate it with live capture.

## Observed Patch Intent To Verify

Treat this as orientation only until source-verified:

- `BrowserPageResponse` now carries optional `request_method` and `resource_type`, derived from Playwright response request metadata, while preserving existing header sanitization.
- TikTok live probe post-load behavior attempts to open the comments UI, records only sanitized `comment_action` telemetry, waits briefly, and then harvests observed page responses.
- TikTok comment-list matching now targets page-owned `/api/comment/list` responses and rejects non-GET or non-fetch/xhr responses when method/type metadata is available.
- Comment response receipts preserve method/type metadata when present.
- Tests cover response request metadata preservation and a non-GET comment-list filtering regression.

## Observed Validation And Runtime Evidence To Verify

Prompt-author observed validation:

```powershell
python -m compileall -q orca-harness\source_capture\adapters\browser_snapshot.py orca-harness\source_capture\tiktok\live_batch_probe.py orca-harness\tests\unit\test_source_capture_browser_snapshot.py orca-harness\tests\unit\test_tiktok_live_batch_probe.py
```

Observed result: pass.

```powershell
python -m pytest -q orca-harness\tests\unit\test_tiktok_batch_admission.py orca-harness\tests\unit\test_tiktok_batch_coverage.py orca-harness\tests\unit\test_tiktok_batch_projection.py orca-harness\tests\unit\test_tiktok_video_admission.py orca-harness\tests\unit\test_tiktok_live_batch_probe.py orca-harness\tests\unit\test_source_capture_browser_snapshot.py
```

Observed result: `70 passed`.

```powershell
git diff --check
```

Observed result: exit 0, with only LF-to-CRLF warnings on touched files.

Prompt-author observed live/offline evidence:

- Pre-async control run wrote sanitized staging JSON for one known TikTok video, with `attempted_count=1`, `completed_count=1`, `challenge_count=0`, `response_count=0`, and `matched_comment_response_count=0`.
- Offline batch admission consumed that staging JSON and wrote a packet with `video_count=1`, `completed_count=1`, `comment_response_success_count=0`, and no captured comments.
- Post-async control run stopped on `platform_challenge_observed` with `attempted_count=1`, `completed_count=0`, `challenge_count=1`, and no result rows.
- No 3-5 creator micro-batch was run because stop-on-challenge was triggered.
- Sensitive-marker scan over new live/admission outputs found no matches for `msToken|X-Bogus|verifyFp|ttwid=|sessionid=|sid_guard|odin_tt|passport_csrf_token|tiktokcdn|byteoversea|tos-useast`.

Do not upgrade these observations into product value, scale, cross-creator, comment-yield, subtitle-yield, or account-safety claims.

## Review Checks

Be adversarial inside this target. Focus on material bugs, false-success paths, overbroad capture, secret leakage, and tests that would pass without proving the intended behavior.

Answer at least:

1. Does `BrowserPageResponse.request_method/resource_type` add only safe metadata, or can it leak headers, cookies, URLs, storage paths, proxy data, auth state, or other secrets?
2. Is `_response_request_metadata` robust to Playwright request API failure modes without masking page-response collection?
3. Does the `/api/comment/list` filter correctly select page-owned TikTok comment-list responses while excluding OPTIONS/preflight, unrelated APIs, HTML, pixels, beacons, or third-party endpoints?
4. Does the filter avoid dropping legitimate comment-list responses when method/type metadata is unavailable in tests or older adapters?
5. Is the async comment-open post-load script safe under the TikTok lane constraints: human-rate, no secret persistence, no raw UI text persistence, no hammering, and stop-on-challenge preserved?
6. Does `comment_action` telemetry stay sanitized and useful, or can it create a misleading success signal?
7. Does the live evidence support only the narrow claim that zero-response staging/admission plumbing works and challenge stop fires, rather than a claim that real comment capture works?
8. Do the tests fail under the old behavior and exercise the intended new behavior without live browser/network dependency?
9. Does the patch alter batch admission, packet schema, or downstream summaries in a way that breaks prior TikTok batch behavior?
10. Is any issue design-level enough to return `NEEDS_ARCHITECTURE_PASS` instead of a patch request?

## Drift Guard

Do not perform or request:

- live TikTok/browser/network capture;
- a 3-5 creator micro-batch;
- auth-state refresh, cookie inspection, or proxy/session changes;
- product mention extraction, product-value analysis, or creator/business judgment;
- patching source files;
- broad repo cleanup, prompt-template changes, or overlay doctrine changes;
- merge, commit, push, or PR state changes.

## Allowed Validation

You may run offline validation from `C:\tmp\orca-tiktok-live-smoke-main`:

```powershell
python -m compileall -q orca-harness\source_capture\adapters\browser_snapshot.py orca-harness\source_capture\tiktok\live_batch_probe.py orca-harness\tests\unit\test_source_capture_browser_snapshot.py orca-harness\tests\unit\test_tiktok_live_batch_probe.py
```

```powershell
python -m pytest -q orca-harness\tests\unit\test_tiktok_batch_admission.py orca-harness\tests\unit\test_tiktok_batch_coverage.py orca-harness\tests\unit\test_tiktok_batch_projection.py orca-harness\tests\unit\test_tiktok_video_admission.py orca-harness\tests\unit\test_tiktok_live_batch_probe.py orca-harness\tests\unit\test_source_capture_browser_snapshot.py
```

```powershell
git diff --check
```

`gh pr checks 559` is optional if GitHub access is already available. If blocked by network/proxy/tooling, report `not_run`; do not treat that as a code finding.

## Output Contract

Write the durable report to:

`docs/review-outputs/tiktok_comment_response_capture_adversarial_code_review_v0.md`

The report must include:

- retrieval header with `authority_boundary: retrieval_only`;
- `reviewed_by` and `authored_by` fields in the body; use `unrecorded` only if not supplied, never fabricate;
- `de_correlation_bar: cross_vendor_discovery`;
- source-read ledger with file paths and line references for load-bearing claims;
- findings first, ordered by severity: `critical`, `major`, `minor`;
- for each finding:
  - severity;
  - location;
  - issue;
  - evidence with file:line cites;
  - impact;
  - minimum_closure_condition;
  - next_authorized_action;
  - whether a patch is requested from the authoring lane;
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
  target_commit: f8a30acccaa61b18c144872d8fe28191cfeaa84b
  pr: https://github.com/eric-foo/orca/pull/559
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
