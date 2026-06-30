# YouTube Leading-Dash Residual - Delegated Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt (delegated adversarial code review)
scope: >
  Commissions a de-correlated, repo-bound, read-only adversarial code review of
  PR #511's YouTube leading-dash video-id residual fix and its evidence receipts.
use_when:
  - Dispatching an independent reviewer to inspect the PR #511 implementation diff before adjudication or merge.
  - Checking whether the YouTube leading-dash residual fix weakens CLI error visibility or overclaims IG/YT behavioral completeness.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - docs/workflows/youtube_behavioral_measurement_corpus_receipt_v0.md
branch_or_commit: codex/ig-youtube-residual-burndown @ 6b82343d3852566cfad076183b0060a0c9af8a22
```

## Prompt Preflight Record

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  repo_map_decision: loaded
  repo_map_reason: target diff updates the repo map and runner navigation; the review needs the changed map row only, not a broad map sweep.
  workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\ig-youtube-residual-burndown
  branch: codex/ig-youtube-residual-burndown
  base_commit: 760fa28d05b740d128686d16f0cee6312267d346
  implementation_commit_under_review: 6b82343d3852566cfad076183b0060a0c9af8a22
  dirty_state_allowance: clean working tree; this prompt file may be present but is outside the implementation review target.
  edit_permission: read-only
  output_mode: review-report
  prompt_artifact: docs/prompts/reviews/youtube_leading_dash_residual_adversarial_code_review_prompt_v0.md
  review_report_destination: docs/review-outputs/youtube_leading_dash_residual_adversarial_code_review_v0.md
  template_kind: review
  template_source: workflow-prompt-orchestrator custom body; Orca registry has no bound repo-code-review template.
  doctrine_change: no
  external_source_boundary: jb and external workflow source are not Orca authority; installed/plugin skills are read-only.
```

## Lane Binding

- Review purpose: adversarial implementation/code review of PR #511's leading-dash YouTube video-id residual fix.
- Review lane: `workflow-code-review` after `workflow-deep-thinking`.
- Delegated-review-patch status: route-out from the provisional convention. This is a multi-file implementation/code diff, so do not stretch it into the single-target delegated review-and-patch lane.
- Patch authority: none. Do not edit files, do not emit `patch_queue_entry`, and do not apply fixes. Findings may include advisory remediation direction and must name `next_authorized_action`.
- De-correlation: who-constraint, not a runtime model recommendation.

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI/GPT-family Codex current thread; exact runtime version unrecorded
  controller_model_family: operator_to_fill
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier or independent review lane
  de_correlation_status: operator_to_fill
  de_correlation_bar: operator_to_fill  # cross_vendor_discovery | same_vendor_sanity | self_fallback
```

If the controller is not de-correlated from the author/home family, still return useful findings if the owner asks, but record the limitation and do not claim the cross-vendor discovery/no-new-seam bar. Do not recommend, rank, or select a runtime model.

## What This Is For

Goal: verify that PR #511 actually closes the YouTube leading-dash video-id residual without weakening ordinary argparse failure visibility, runner data-lake semantics, or the IG/YT behavioral-completeness claim boundary.

Done looks like: the reviewer either finds no material blocker/major issue in the pinned implementation diff, or returns findings with source citations, closure conditions, and the next authorized action needed before the PR should be treated as reviewed input.

This is an alignment axis to attack, not a pass-if-matches bar.

## Source-Gated Method Contract

REFERENCE-LOAD the following method instructions first. Do not APPLY them yet; use them only to prepare a neutral source-reading lens.

1. `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.87\skills\workflow-deep-thinking\SKILL.md`
2. `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.87\skills\workflow-code-review\SKILL.md`

SOURCE-LOAD the task sources below, then declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, source gaps, excluded sources, and conflicts. Only after that declaration may you APPLY `workflow-deep-thinking` and then `workflow-code-review`.

## Required Source Pack

Read the repo/worktree directly. Do not substitute this prompt, a summary, an alternate checkout, or recreated source for the pinned worktree. If you cannot open the worktree or see the expected commit, return the nearest blocker instead of reviewing.

Authority and routing sources:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/safety-rules.md`

Implementation target: review the branch's implementation diff against current `origin/main`; inspect implementation commit `6b82343d3852566cfad076183b0060a0c9af8a22` directly for author intent.

Use:

```powershell
git show --stat --oneline 6b82343d3852566cfad076183b0060a0c9af8a22
git show --name-status --oneline 6b82343d3852566cfad076183b0060a0c9af8a22
git diff origin/main...HEAD -- <target files>
```

Target files:

- `orca-harness/runners/_youtube_cli.py`
- `orca-harness/runners/run_source_capture_youtube_watch_packet.py`
- `orca-harness/runners/run_source_capture_youtube_caption_packet.py`
- `orca-harness/runners/run_source_capture_youtube_asr_packet.py`
- `orca-harness/tests/unit/test_youtube_watch_runner_output_mode.py`
- `orca-harness/tests/unit/test_youtube_caption_runner_output_mode.py`
- `orca-harness/tests/unit/test_youtube_asr_runner_cli.py`
- `docs/workflows/youtube_behavioral_measurement_corpus_receipt_v0.md`
- `docs/workflows/ig_youtube_behavioral_e2e_closeout_receipt_v0.md`
- `docs/workflows/orca_repo_map_v0.md`

The prompt file itself is not part of the implementation target.

## Validation Evidence To Inspect

The commissioning lane reported this focused validation before review dispatch; verify it against the branch artifacts and rerun only if needed for a finding:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider -q --basetemp '..\pytest_tmp_youtube_residual_rebased' orca-harness/tests/unit/test_youtube_watch_runner_output_mode.py orca-harness/tests/unit/test_youtube_caption_runner_output_mode.py orca-harness/tests/unit/test_youtube_asr_runner_cli.py orca-harness/tests/unit/test_source_capture_youtube_watch_packet.py orca-harness/tests/unit/test_youtube_caption_packet.py orca-harness/tests/unit/test_youtube_asr_packet.py orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py orca-harness/tests/contract/test_runner_artifacts.py orca-harness/tests/unit/test_youtube_behavioral_projection.py
```

Reported result: exit 0, progress reached `[100%]`.

Reported live canonical F-lake readback for `-V7MN2IWMpA`:

```text
WATCH_PACKET F:/orca-data-lake/raw/dca/01KWBVE0XV1E1MRY3KS538ZJE3
CAPTION_PACKET F:/orca-data-lake/raw/266/01KWBVEVSGVEE3VHY3F5RK4ZQ1
SILVER_RECORD F:/orca-data-lake/derived/266/01KWBVEVSGVEE3VHY3F5RK4ZQ1/silver__cleaning__product_mentions/mentions_codex_operator_youtube_residual_burndown_v0__8a95674a2ab08d69.json
MENTIONS 2
REJECTED 0
PROJECTION -V7MN2IWMpA status=complete sources=1 complete_sources=1 mentions=2 residuals=[]
```

Treat F-lake evidence as an observed external-state receipt, not a reason to run new live capture during this review unless the owner separately authorizes it.

## Failure Modes To Attack

Be maximally adversarial about material, decision-relevant failure modes inside the target.

- CLI normalization: `normalize_video_id_argv(...)` must only rewrite `--video-id <value>` when `<value>` is a valid 11-character YouTube id starting with `-`. It must not hide ordinary argparse errors, missing values, mistyped flags, or arbitrary negative-looking arguments.
- Runner consistency: watch, caption, and ASR runners must all parse leading-dash video ids consistently without changing their existing `--output`, `--data-root`, `ORCA_DATA_ROOT`, exception, and exit-code semantics.
- Import/runtime compatibility: the new shared helper must resolve correctly for both module-style test imports and direct runner script execution.
- Test adequacy: the tests should prove the leading-dash path reaches the runner/fetch/write layer and should not only prove a mocked happy path while missing an argparse regression.
- Evidence receipts: the workflow docs must accurately state what was live-tested, what was parser-guarded/operator-assisted, which F-lake records were written, and what remains incomplete.
- Claim boundary: the docs must not claim platform-wide YouTube behavioral completeness, ASR/no-caption fallback validation, provider-API extraction, full IG completeness, shared IG/YT core, production readiness, or validation beyond the observed tests/readbacks.
- Repo map: the new `_youtube_cli.py` navigation entry must be placed accurately without making the repo map a validation or authority claim.
- Merge-base hygiene: review the implementation commit, not any already-merged #509 overlay changes. Do not treat the prompt artifact as part of the implementation under review.

## Output Contract

Write the durable report to:

`docs/review-outputs/youtube_leading_dash_residual_adversarial_code_review_v0.md`

The report must include:

- `reviewed_by`: operator/tooling supplied model and version that performed the review, or `unrecorded`.
- `authored_by`: operator/tooling supplied model and version that authored the reviewed artifact, or `unrecorded`.
- `de_correlation_bar`: `cross_vendor_discovery`, `same_vendor_sanity`, or `self_fallback`; if `same_vendor_sanity`, include `same_vendor_rationale`.
- Findings first, ordered by severity.
- For each actionable finding: severity (`critical`, `major`, or `minor`, priority only), file/line evidence, `minimum_closure_condition`, and `next_authorized_action`.
- Non-findings and not-proven boundaries where they matter.
- Residual risk note.

If no material issues are found, say that clearly and name residual risks or test gaps. The review report is decision input only: not approval, not validation, not mandatory remediation, not readiness, and not patch authority.

After writing the report, return only a compact courier summary in chat:

```yaml
review_summary:
  status: complete | blocked
  report_path: docs/review-outputs/youtube_leading_dash_residual_adversarial_code_review_v0.md
  reviewed_by: operator_to_fill_or_unrecorded
  authored_by: operator_to_fill_or_unrecorded
  de_correlation_bar: operator_to_fill
  finding_counts:
    critical: 0
    major: 0
    minor: 0
  next_authorized_action: <one line>
```
