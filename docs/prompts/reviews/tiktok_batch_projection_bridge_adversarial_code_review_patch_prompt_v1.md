# TikTok Batch Projection Bridge Adversarial Code Review Patch Prompt v1

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  De-correlated implementation/code review-and-patch prompt for PR #547, the
  TikTok admitted-batch projection bridge.
use_when:
  - Commissioning a different-family controller to review PR #547.
  - Allowing bounded patching only inside the PR-changed implementation files.
  - Preparing a couriered review result for home-model adjudication.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
branch_or_commit: PR #547 head 0734bb0d96ddc66f865d8d63406c4e310a9d20e6
stale_if:
  - PR #547 head SHA changes.
  - PR #547 merges, closes, or is rebased.
  - The reviewed branch has uncommitted local edits before the controller starts.
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_repo_code_review_pack
  edit_permission: patch-only
  target_scope: PR #547 changed files only
  dirty_state_checked: required_by_receiver
  blocked_if_missing: repo access, PR #547 head pin, clean target worktree, de-correlated controller family

prompt_contract:
  output_mode: file-write artifact plus paste-ready controller prompt
  template_kind: review + patch
  authorization_basis: current owner request for delegated review patch prompt
  objective: de-correlated review of PR #547 and bounded patching of material defects
  intended_decision: whether PR #547 is clean enough to merge after home-model adjudication
  dirty_state_allowance: target worktree must be clean before review; controller-created diff is allowed and must be reported uncommitted
  branch_or_commit_reference: codex/tiktok-source-projection-bridge at 0734bb0d96ddc66f865d8d63406c4e310a9d20e6
  doctrine_change_decision: no doctrine change intended; flag any needed doctrine/projection-contract change as off-scope
  isolation_decision: receiver should use a clean worktree for PR #547; do not edit the prompt-artifact worktree
  validation_gates:
    - focused pytest listed in this prompt, when dependencies/environment are available
    - git diff --check after any patch
    - optional real Funmi packet readback when F: data lake is available
  thread_operating_target_continuity: omitted; no visible active thread_operating_target supplied
```

## Controller Prompt

You are the de-correlated controller for a bounded implementation/code review-and-patch pass.

This is a who-constraint, not a model recommendation. The reviewed change was authored by an OpenAI/GPT-family Codex agent. You may proceed as controller only if your upstream model family/vendor differs from OpenAI/GPT. If your family/vendor is OpenAI/GPT, or your lineage is unknown, stop with `BLOCKED_CONTROLLER_NOT_DECORRELATED`.

Actor receipt to complete before review:

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI/GPT-family Codex
  controller_model_family: <fill your actual family/vendor>
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: satisfied | blocked
```

Do not launch another reviewer subagent to satisfy de-correlation. If you are the controller and the receipt is satisfied, proceed. If not, block.

## Review Target

Repository: `C:\Users\vmon7\Desktop\projects\orca`

PR: `https://github.com/eric-foo/orca/pull/547`

Target branch: `codex/tiktok-source-projection-bridge`

Expected head SHA: `0734bb0d96ddc66f865d8d63406c4e310a9d20e6`

Base: `main`

PR title: `Add TikTok batch projection bridge`

Fresh verification already observed by the dispatcher:

```yaml
pr_state:
  state: OPEN
  isDraft: false
  mergeStateStatus: CLEAN
  ci:
    orca-harness-tests: SUCCESS
    completedAt: 2026-07-01T13:04:57Z
```

Do not trust this receipt. Verify the PR branch, head SHA, clean worktree state, and diff yourself before review. If you cannot access the repo/PR branch directly, return `BLOCKED_REPO_ACCESS_UNAVAILABLE` and request a no-repo review bundle. Do not review from this prompt, a summary, or recreated source as a substitute.

## Bounded Patch Scope

You may patch only these PR-changed files:

- `[projection-core]` `orca-harness/source_capture/tiktok/batch_projection.py`
- `[projection-cli]` `orca-harness/runners/run_tiktok_batch_projection.py`
- `[projection-export]` `orca-harness/source_capture/tiktok/__init__.py`
- `[projection-tests]` `orca-harness/tests/unit/test_tiktok_batch_projection.py`
- `[repo-map]` `docs/workflows/orca_repo_map_v0.md`

Everything else is read-only. You may inspect adjacent source for evidence, but if the correct fix requires changing any other file, flag it as off-scope instead of editing it. Do not commit, push, merge, open or update a PR, or modify protected/global/user/plugin skill source.

Patch only blocker or major material defects that are directly inside the bounded files. Report minor findings without patching unless they are necessary to make a blocker/major patch coherent.

If you find a design-level problem, return `NEEDS_ARCHITECTURE_PASS`, revert any partial local diff, and provide findings only.

## Required Method Sequence

1. REFERENCE-LOAD method instructions:
   - `workflow-deep-thinking`
   - `workflow-code-review`
   - `.agents/workflow-overlay/review-lanes.md`
   - `.agents/workflow-overlay/delegated-review-patch.md`
   - `.agents/workflow-overlay/prompt-orchestration.md`
2. Do not APPLY those methods yet.
3. SOURCE-LOAD the task sources below.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
5. Only after source readiness, APPLY `workflow-deep-thinking` to identify the highest-risk failure modes, then APPLY `workflow-code-review`.

If `workflow-code-review` is unavailable in your runtime, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not patch.

## Task Sources To Read

Required controlling sources:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`

Required implementation sources:

- PR #547 diff against `main`
- `orca-harness/source_capture/tiktok/batch_projection.py`
- `orca-harness/runners/run_tiktok_batch_projection.py`
- `orca-harness/source_capture/tiktok/__init__.py`
- `orca-harness/tests/unit/test_tiktok_batch_projection.py`

Required adjacent context:

- `orca-harness/source_capture/tiktok/batch_coverage.py`
- `orca-harness/source_capture/tiktok/batch_packet.py`
- `orca-harness/source_capture/tiktok/admission.py`
- `orca-harness/cleaning/projection.py`
- `orca-harness/cleaning/models.py`
- `orca-harness/source_capture/ig_projection.py`
- `orca-harness/tests/unit/test_tiktok_batch_coverage.py`
- `orca-harness/tests/unit/test_cleaning_projection_integration.py`

Optional real-packet source, only if available on your machine:

- `F:\orca-data-lake\raw\97c\01KWCYZ9P72W4SJD7NDPRQT0DB`

If `F:` is unavailable, mark the real-packet readback as `not_run_environment_unavailable`; do not block review solely for that.

## Review Axis

Attack the implementation for material defects in:

- projection-doctrine compliance: projection is a re-derived view over raw, not Cleaning, ECR, Judgment, product extraction, or a new persisted lane;
- raw anchoring: each row must be keyed to the preserved raw batch JSON and stable JSON pointer, not to the derived coverage view alone;
- sanitizer safety: no raw TikTok signed URLs, cookies, query secrets, raw comments, transcript text, cue text, hashtags, or source mentions should enter projection output;
- Cleaning handle compatibility: rows must preserve `raw_ref.packet_id/slice_id` and preserved-file `raw_anchor` shape accepted by `cleaning.projection`;
- loss ledger integrity: omitted text counts, row counts, residual counts, and structure-preserved claims must be computed from source evidence and fail visibly when inconsistent;
- CLI behavior: packet directory and data-lake packet-id modes must preserve the same boundaries and not introduce network/browser/proxy/model dependencies;
- tests: tests should pin the safety and anchor contract without creating fake success paths;
- repo-map change: navigation update should be truthful and not overclaim validation/readiness.

Explicit non-goals:

- no product mention extraction;
- no live capture or browser automation;
- no direct TikTok API call;
- no data-lake derived append or persisted projection lane;
- no Cleaning transform, ECR record, Judgment, buyer proof, or cross-creator generalization claim;
- no unrelated refactor or style-only cleanup.

## Suggested Verification Commands

Run what your environment supports and report exact results.

From `orca-harness`:

```powershell
python -m pytest -p no:cacheprovider --no-header --no-summary --basetemp pytest_tiktok_projection_tmp tests/unit/test_tiktok_batch_admission.py tests/unit/test_tiktok_video_admission.py tests/unit/test_tiktok_batch_coverage.py tests/unit/test_tiktok_batch_projection.py tests/unit/test_cleaning_projection_integration.py -q
```

From repo root:

```powershell
git diff --check
python .agents\hooks\header_index.py --strict --base origin/main
python .agents\hooks\check_map_links.py --strict
python .agents\hooks\check_repo_map_freshness.py --changed --strict
```

Optional real packet readback, from `orca-harness`, if `F:` is available:

```powershell
python -c "from pathlib import Path; import json; from collections import Counter; from source_capture.tiktok.batch_projection import build_tiktok_batch_projection_from_packet_directory; p=build_tiktok_batch_projection_from_packet_directory(Path(r'F:\orca-data-lake\raw\97c\01KWCYZ9P72W4SJD7NDPRQT0DB')); out={'projection_method':p.projection_method,'projection_version':p.projection_version,'certification':p.certification,'packet_id':p.packet_id,'creator_handle':p.creator_handle,'row_count':len(p.rows),'loss_ledger':p.loss_ledger.model_dump(mode='json'),'first_anchor':p.rows[0].raw_anchor.model_dump(mode='json'),'last_anchor':p.rows[-1].raw_anchor.model_dump(mode='json'),'row_residual_counts':dict(sorted(Counter(r for row in p.rows for r in row.residuals).items())),'non_claims':p.non_claims}; print(json.dumps(out, indent=2, sort_keys=True))"
```

## Return Contract

Return findings first. If there are no blocker/major findings, say that clearly and include residual risk.

Required return shape:

```yaml
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL:
  reviewed_by: <your actual model/family/version, or unrecorded>
  authored_by: OpenAI/GPT-family Codex
  de_correlation_bar: cross_vendor_discovery | blocked
  target_pr: https://github.com/eric-foo/orca/pull/547
  target_head: <observed SHA>
  source_context: SOURCE_CONTEXT_READY | SOURCE_CONTEXT_INCOMPLETE
  worktree_preflight:
    branch: <observed branch>
    head: <observed SHA>
    dirty_before_review: yes | no
  verdict: findings | no_blocker_or_major_findings | NEEDS_ARCHITECTURE_PASS | blocked
  patched: yes | no
  changed_files: []
  validation:
    pytest: run | not_run | failed
    diff_check: run | not_run | failed
    header_index: run | not_run | failed
    map_links: run | not_run | failed
    repo_map_freshness: run | not_run | failed
    real_packet_readback: run | not_run_environment_unavailable | failed
  residual_risks: []
```

For each finding include:

- `severity`: blocker, major, or minor;
- label tag from the bounded patch scope;
- file and line/anchor;
- evidence from source;
- impact;
- minimum closure condition;
- next authorized action;
- whether you patched it.

If you patch:

- leave changes uncommitted;
- provide a unified diff;
- cite the source basis for each change;
- state exactly which validation was rerun after the patch;
- do not present your diff as kept. It is decision input for home-model adjudication.

The home model / Chief Architect will adjudicate your findings and diff. Your verdict, citations, and patch are claims to adjudicate, not premises to inherit.
