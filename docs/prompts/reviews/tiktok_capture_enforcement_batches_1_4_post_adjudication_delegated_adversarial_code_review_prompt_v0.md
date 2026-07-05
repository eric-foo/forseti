# TikTok Capture Enforcement Batches 1-4 Post-Adjudication Delegated Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed cross-recipient prompt for a de-correlated delegated adversarial
  code review-and-patch pass on the TikTok cold-agent capture enforcement
  BATCH-01 through BATCH-04 implementation, including the post-review
  adjudication patch for human challenge handoff routing and interrupted
  warmup provenance binding.
use_when:
  - Commissioning an independent controller to review and optionally patch PR #709 after the post-adjudication implementation commit.
  - Checking whether a cold agent can use the sanctioned TikTok capture path without rediscovering known blocker, provenance, admission, transcript, and receipt rules.
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/decision-routing.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/validation-gates.md
  - .agents/workflow-overlay/safety-rules.md
  - docs/workflows/tiktok_cold_agent_capture_enforcement_goal_v0.md
  - docs/decisions/tiktok_auth_state_provenance_sidecar_architecture_v0.md
  - docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
  - orca-harness/runners/run_source_capture_tiktok_live_batch_probe.py
  - orca-harness/runners/run_source_capture_cloakbrowser_profile_warmup.py
  - orca-harness/runners/run_source_capture_browser_user_data_export.py
  - orca-harness/source_capture/source_access_provenance.py
  - orca-harness/source_capture/auth_state.py
  - orca-harness/source_capture/browser_user_data.py
  - orca-harness/source_capture/adapters/browser_snapshot.py
  - orca-harness/source_capture/tiktok/live_batch_probe.py
  - orca-harness/source_capture/tiktok/blocker_triage.py
  - orca-harness/source_capture/tiktok/batch_packet.py
  - orca-harness/source_capture/tiktok/admission.py
  - orca-harness/tests/unit/test_tiktok_live_batch_probe.py
  - orca-harness/tests/unit/test_tiktok_blocker_triage.py
  - orca-harness/tests/unit/test_tiktok_batch_admission.py
  - orca-harness/tests/unit/test_source_capture_authenticated_browser_snapshot.py
authoring_branch: codex/tiktok-session-provenance-implementation
authoring_base_observed: origin/main @ e8ca2093ce7fad5d3d8b96b030c874f81655824a
implementation_target_head: fb078dd08539c1392002dc0ca145a41a02656ddc
stale_if:
  - The reviewer cannot inspect implementation_target_head in the target repository/worktree.
  - The reviewed target diff is not `origin/main...fb078dd08539c1392002dc0ca145a41a02656ddc` or an explicitly owner-supplied rebased equivalent.
  - Target source or test files have uncommitted local changes not owned by the reviewer.
  - The receiving actor cannot establish the de-correlation receipt required below.
authority_boundary: retrieval_only
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

- output_mode: `review-report`
- prompt_artifact_path: `docs/prompts/reviews/tiktok_capture_enforcement_batches_1_4_post_adjudication_delegated_adversarial_code_review_prompt_v0.md`
- review_report_destination: `docs/review-outputs/tiktok_capture_enforcement_batches_1_4_post_adjudication_delegated_adversarial_code_review_v0.md`
- template_kind: `review`; Orca has no bound repo-code-review template, so this prompt uses the overlay review and delegated-review-patch contracts directly.
- authorization_basis: owner requested adjudication of the duplicated delegated review return, completion of the remaining batches, and a delegated review prompt.
- objective / intended_decision: decide whether the completed TikTok BATCH-01 through BATCH-04 enforcement implementation is safe, truthful, fail-closed, and usable by a cold agent before merge, and patch bounded defects if found.
- fitness_reference: `docs/workflows/tiktok_cold_agent_capture_enforcement_goal_v0.md`; success means a cold agent can follow the sanctioned TikTok runner path without rediscovering known blockers, provenance/session posture, local admission, caption/transcript, owner-challenge handoff, or receipt-summary rules.
- edit_permission: `patch-only`; the controller may patch only the files in `bounded_patch_scope` below and may write the review report at `review_report_destination`. Do not commit, push, merge, open a PR, edit secrets, or edit off-scope files.
- expected_worktree: `C:\Users\vmon7\Desktop\projects\orca\worktrees\tiktok-session-provenance-implementation` or another repo-backed checkout of PR #709.
- expected_branch: `codex/tiktok-session-provenance-implementation` unless the dispatcher supplies a detached checkout of `implementation_target_head`.
- expected_pr: `https://github.com/eric-foo/orca/pull/709`
- implementation_target_head: `fb078dd08539c1392002dc0ca145a41a02656ddc`
- base_comparison: `origin/main...fb078dd08539c1392002dc0ca145a41a02656ddc`
- dirty_state_allowance: clean target files, except reviewer-owned uncommitted patch output and the known unrelated untracked superseded `docs/workflows/tiktok_session_provenance_pr689_handoff_v0.md`. If reviewing from the prompt-file commit that descends from `implementation_target_head`, review the implementation diff pinned above and treat the prompt-only descendant as dispatcher context, not implementation scope.
- isolation_decision: use the existing PR worktree/branch; this is a review-and-patch pass, not a new implementation lane.
- doctrine_change_decision: no new doctrine change requested. If the correct fix requires changing workflow, validation, review, safety, architecture, or prompt doctrine, return `NEEDS_ARCHITECTURE_PASS` or an off-scope finding instead of editing doctrine.
- thread_operating_target_continuity:
  - carried_forward: yes
  - reason: same_workstream
  - lifecycle_status: active_thread_local
  - target: make TikTok capture seamless enough for a cold agent to access and capture via sanctioned harness paths, with low-latency known blocker handling and enforceable receipts.

## De-Correlation And Role Contract

You are the de-correlated controller for a delegated adversarial code review-and-patch pass. The implementation was authored and adjudicated by OpenAI/GPT-family Codex/GPT-5. To satisfy the discovery bar, your controller vendor/model lineage must differ from OpenAI/GPT-family. This is a who-constraint, not a runtime model recommendation.

Before reviewing, record:

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI/GPT-family Codex/GPT-5
  controller_model_family: <operator/tooling supplied>
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_bar: cross_vendor_discovery
  de_correlation_status: satisfied | blocked
```

If the receipt is missing, same-vendor, unknown, or inconsistent, return `BLOCKED_CONTROLLER_NOT_DECORRELATED` before reviewing. Do not ask the authoring model to self-review. Do not launch recursive or unrelated subagents. Findings and any patch are claims for home-model adjudication, not kept truth.

## Source-Gated Method Sequence

1. Read the authority and operating sources named in `open_next` that apply to the review.
2. REFERENCE-LOAD `workflow-deep-thinking`, `workflow-code-review`, and `workflow-adversarial-artifact-review`. Do not APPLY them yet.
3. SOURCE-LOAD the task-specific source pack below.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`. If incomplete, name missing sources and whether strict findings are blocked.
5. After source readiness, APPLY `workflow-deep-thinking` to frame failure modes, APPLY `workflow-code-review` to code/tests, and APPLY `workflow-adversarial-artifact-review` to prompt/docs/doctrine surfaces in the target diff.

## Required Task Source Pack

Run or inspect:

```powershell
git rev-parse HEAD
git status --short --branch
git show --stat --oneline fb078dd08539c1392002dc0ca145a41a02656ddc
git diff origin/main...fb078dd08539c1392002dc0ca145a41a02656ddc
```

Read these files as source, not summaries:

- `docs/workflows/tiktok_cold_agent_capture_enforcement_goal_v0.md`
- `docs/decisions/tiktok_auth_state_provenance_sidecar_architecture_v0.md`
- `docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md`
- `orca-harness/README.md`
- `orca-harness/docs/source_capture_agent_runbook.md`
- `orca-harness/runners/run_source_capture_tiktok_live_batch_probe.py`
- `orca-harness/runners/run_source_capture_cloakbrowser_profile_warmup.py`
- `orca-harness/runners/run_source_capture_browser_user_data_export.py`
- `orca-harness/source_capture/source_access_provenance.py`
- `orca-harness/source_capture/auth_state.py`
- `orca-harness/source_capture/browser_user_data.py`
- `orca-harness/source_capture/adapters/browser_snapshot.py`
- `orca-harness/source_capture/tiktok/live_batch_probe.py`
- `orca-harness/source_capture/tiktok/blocker_triage.py`
- `orca-harness/source_capture/tiktok/batch_packet.py`
- `orca-harness/source_capture/tiktok/admission.py`
- `orca-harness/tests/unit/test_tiktok_live_batch_probe.py`
- `orca-harness/tests/unit/test_tiktok_blocker_triage.py`
- `orca-harness/tests/unit/test_tiktok_batch_admission.py`
- `orca-harness/tests/unit/test_source_capture_authenticated_browser_snapshot.py`

Do not inspect cookies, auth-state contents, storage-state contents, proxy credentials, raw proxy endpoints, raw exit IPs, raw signed subtitle URLs, device IDs, tokens, or live account secrets. Category-only metadata, code, tests, docs, and sanitized receipts are in scope. Do not run a live TikTok probe unless the owner explicitly authorizes that separately.

## Bounded Patch Scope

The controller may patch only these files:

- `orca-harness/runners/run_source_capture_tiktok_live_batch_probe.py`
- `orca-harness/runners/run_source_capture_cloakbrowser_profile_warmup.py`
- `orca-harness/runners/run_source_capture_browser_user_data_export.py`
- `orca-harness/source_capture/source_access_provenance.py`
- `orca-harness/source_capture/auth_state.py`
- `orca-harness/source_capture/browser_user_data.py`
- `orca-harness/source_capture/tiktok/live_batch_probe.py`
- `orca-harness/source_capture/tiktok/blocker_triage.py`
- `orca-harness/source_capture/tiktok/batch_packet.py`
- `orca-harness/source_capture/tiktok/admission.py`
- `orca-harness/tests/unit/test_tiktok_live_batch_probe.py`
- `orca-harness/tests/unit/test_tiktok_blocker_triage.py`
- `orca-harness/tests/unit/test_tiktok_batch_admission.py`
- `orca-harness/tests/unit/test_source_capture_authenticated_browser_snapshot.py`
- `orca-harness/README.md`
- `orca-harness/docs/source_capture_agent_runbook.md`
- `docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md`

Everything else is read-only and flag-only, including overlay files, decisions, lane specs, repo maps, generated artifacts, auth-state files, proxy profile files, browser user-data directories, and unrelated untracked files. If the right fix is outside patch scope, return a finding with `minimum_closure_condition` and `next_authorized_action`; do not edit it.

## Review Focus

Attack these claims first:

1. BATCH-01 provenance: packet-grade TikTok runner posture is enforced by code and owner-produced sidecars, not by label strings. Browser user-data warmup, export, auth-state metadata, and live runner `--require-harness-proxy-posture` fail closed on missing/mismatched evidence and preserve secret-safe category-only metadata.
2. Post-adjudication residual closure: writing browser user-data provenance before external CloakBrowser warmup actually prevents interrupted profile reuse under a changed proxy posture; the regression test catches the failure and does not create a brittle false positive.
3. BATCH-02 blocker handling: known TikTok UI blockers are typed and routed correctly. Intro/teaching overlays use owner-approved OK handling, retry prompts press retry, comments can be reached by the You-may-like/comments route, and X-able slider/platform challenges attempt only allowed X/Close followthrough. `platform_challenge_observed` must retain challenge kind detail instead of collapsing all cases into one terminal blocker.
4. BATCH-03 transcript/admission: captions/transcripts are captured or represented by sanitized reason/length/hash only; no raw subtitle URLs or secrets persist. Batch admission rejects owner-attention-as-clean-capture, agent CAPTCHA/challenge solving, and source-access interventions that should not count as clean capture.
5. Owner challenge handoff: when scripted X/Close followthrough does not clear a slider/captcha and `--human-challenge-handoff` is enabled, receipts route to owner attention without letting the agent solve the challenge and without admitting the result as clean capture. The accepted delegated test must pin the route and the non-clean-capture semantics.
6. BATCH-04 cold-agent command and receipts: runner help and docs expose a copyable sessioned CloakBrowser command using `--require-harness-proxy-posture no_proxy_profile_loaded`, `--allow-challenge-close-followthrough`, `--human-challenge-handoff`, and local `--admit-output`; bronze `--data-root` is explicit, not ambient. Summary receipt lines distinguish staging, local admission, bronze admission, owner attention, and fail-closed outcomes without printing secrets.
7. Failure visibility: no swallowed admission failure, fake success, partial packet write after gate failure, challenge count hidden as success, or secret-bearing receipt is introduced.
8. Test placement: tests pin behavior at deterministic code boundaries and do not imply live TikTok success, account safety, no-proxy network proof, CAPTCHA bypass, scale readiness, or merge readiness.

## Validation To Run

If you patch, run the smallest complete validation relevant to your changes. At minimum for this scope, run:

```powershell
python -m py_compile orca-harness\runners\run_source_capture_tiktok_live_batch_probe.py orca-harness\runners\run_source_capture_cloakbrowser_profile_warmup.py orca-harness\tests\unit\test_tiktok_live_batch_probe.py orca-harness\tests\unit\test_source_capture_authenticated_browser_snapshot.py
python -m pytest orca-harness\tests\unit\test_tiktok_live_batch_probe.py orca-harness\tests\unit\test_tiktok_blocker_triage.py orca-harness\tests\unit\test_tiktok_batch_admission.py orca-harness\tests\unit\test_source_capture_authenticated_browser_snapshot.py -q
python orca-harness\runners\run_source_capture_tiktok_live_batch_probe.py --help
python .agents\hooks\check_dcp_receipt.py --strict
python .agents\hooks\check_handoff_pointers.py --strict
git diff --check
```

If a command is not run, state why. Do not run live TikTok, launch browsers, refresh auth-state, open proxy profiles, or inspect secrets unless the owner explicitly authorizes that in a separate current turn.

## Return Contract

Return findings first, ordered by severity. For every finding include:

- severity: `critical`, `major`, or `minor`
- confidence: `high`, `medium`, or `low`
- file and line citation
- why it matters for the cold-agent TikTok capture goal
- `minimum_closure_condition`
- `next_authorized_action`

If you patch, leave changes uncommitted and return:

- files changed
- concise diff summary
- validation commands and observed results
- residual risks
- off-scope flags

If a design-level problem prevents safe patching, return `NEEDS_ARCHITECTURE_PASS`, revert any partial patch, and return findings only.

Close with:

```yaml
review_summary:
  reviewed_by: <operator/tooling supplied model+version or unrecorded>
  authored_by: OpenAI/GPT-family Codex/GPT-5
  de_correlation_bar: cross_vendor_discovery
  de_correlation_status: satisfied | blocked
  target_commit: fb078dd08539c1392002dc0ca145a41a02656ddc
  recommendation: keep | keep_with_patch | needs_architecture_pass | block
  patches_applied: <count>
  validation: <observed summary or not_run_with_reason>
  next_action: <one land step or none>
```

Review findings and patches are decision input only. They are not approval, validation, mandatory remediation, merge authority, account safety, no-proxy network proof, CAPTCHA bypass, live TikTok success, scale readiness, or readiness to merge until the home model adjudicates them and required gates pass.
