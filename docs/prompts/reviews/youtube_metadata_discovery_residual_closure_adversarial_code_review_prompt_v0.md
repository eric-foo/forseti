# YouTube Metadata Discovery Residual Closure Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial code review prompt for PR #440 Batch 4: closing the
  delegated-review finding that loadable-but-uninterpretable YouTube watch
  metadata packets were silently downgraded to ordinary metadata absence.
use_when:
  - Commissioning a bounded review of the Batch 4 metadata-discovery residual patch.
  - Checking whether accepted delegated review findings F1/F2 from the Batch 3
    lake metadata bridge review were closed without broadening the YouTube lane.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
  - docs/review-outputs/youtube_behavioral_lake_metadata_bridge_advisory_code_review_v0.md
  - docs/workflows/youtube_first_behavioral_completion_spec_v0.md
  - docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```yaml
orca_start_preflight:
  agents_read: yes_supplied_in_current_task_context
  overlay_read: yes_loaded_by_dispatcher
  source_pack: custom_pr440_batch_4_review_closure_diff
  repo_map_decision: targeted_route_checked
  repo_map_reason: `docs/prompts/reviews/`, `docs/review-outputs/`, `orca-harness/youtube_capture/`, and `orca-harness/tests/` are already map-reachable for this prompt and patch scope.
  edit_permission: read-only
  target_scope:
    implementation_targets:
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\youtube_capture\behavioral_projection.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\tests\unit\test_youtube_behavioral_projection.py
    context_only:
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\review-outputs\youtube_behavioral_lake_metadata_bridge_advisory_code_review_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\source_capture\youtube_watch_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\data_lake\root.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\workflows\youtube_first_behavioral_completion_spec_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\workflows\youtube_behavioral_contract_from_merged_main_v0.md
  excluded_from_review_target:
    - this prompt artifact
    - review-output report artifacts
    - IG behavioral adapter implementation
    - shared capture-core implementation or acquisition unification
    - live YouTube or Instagram probing
    - transcript extraction quality, Cleaning, Judgment, scheduler, dashboard, production runtime, or buyer-proof claims
  dirty_state_checked: yes_by_dispatcher_before_prompt_write
  branch_or_commit_reference: >
    branch `codex/youtube-capture-spine-sync`, PR #440. Review the Batch 4 diff
    after base `0c56ebe23363c2e63601d16f6250c44cfb3aecbc`; if this prompt is
    committed in the same branch, exclude this prompt file and review-output files
    from implementation findings.
  controlling_source_state: >
    Dispatcher observed a dirty implementation diff in the named worktree before
    this prompt write: `orca-harness/youtube_capture/behavioral_projection.py`
    and `orca-harness/tests/unit/test_youtube_behavioral_projection.py`, plus the
    prior delegated review output as an untracked durable report.
  output_mode: file-write
  prompt_artifact_path: C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\prompts\reviews\youtube_metadata_discovery_residual_closure_adversarial_code_review_prompt_v0.md
  delivery_copy: paste-ready-chat copy may be used after this filed prompt artifact exists
  reviewer_output_mode: filesystem-output_preferred
  required_review_report_path: C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\review-outputs\youtube_metadata_discovery_residual_closure_advisory_code_review_v0.md
  doctrine_change_decision: no doctrine change requested; review prompt only
  isolation_decision: read-only review; do not create or switch branches/worktrees
  validation_gates:
    - inspect the Batch 4 implementation diff against the accepted F1/F2 closure conditions
    - optionally rerun the focused pytest commands if repo execution is available
  blocked_if_missing:
    - reviewer cannot open the pinned repo/worktree, branch, or Batch 4 diff
    - reviewer cannot inspect the prior delegated review output and its F1/F2 closure conditions
    - reviewer cannot inspect DataLakeRoot and the YouTube watch packet writer while evaluating the corruption test shape
```

## Commission

Run a read-only adversarial code review of the Batch 4 metadata-discovery residual closure patch on PR #440.

This prompt is routed from fused implementation closeout after home-model adjudication of the prior delegated review return. The target is a multi-file implementation/code diff, so this is a read-only `workflow-code-review` commission with adversarial posture. No patch execution, patch queue, formal verdict, readiness claim, runtime model recommendation, or no-new-seam claim is authorized.

De-correlation is a who-constraint, not a runtime model recommendation. The author/home family is OpenAI/Codex. The operator should route this to a different upstream vendor/model-lineage reviewer if claiming `cross_vendor_discovery`; otherwise record the lower bar actually used in the output provenance fields. Unknown or undisclosed reviewer lineage cannot satisfy cross-vendor de-correlation.

Home-model adjudication of the prior review return:

- Accepted F1: loadable-but-uninterpretable watch metadata packets must become fail-visible and must not collapse to ordinary `youtube_metadata_packet_absent` alone.
- Accepted F2: add coverage for the watch-metadata corruption/uninterpretable path using a real lake-backed watch packet.
- Deferred F3: the SHA-pinned merged-main contract record is retrieval-only and may be refreshed later; do not require it for this patch unless the implementation itself creates contradictory current-source claims.
- No action for F4: lexicographic capture timestamp ordering is latent only under non-current writer formats.
- No action for F5: double scan/load is an efficiency advisory, not required for this closure.

Fitness reference:

- Goal: a YouTube behavioral projection from the local lake should make a committed-but-uninterpretable watch metadata packet visible as a metadata-discovery residual, while preserving deterministic metadata lookup and transcript/extraction behavior.
- Non-goal: do not redesign behavioral completeness, introduce lane/global residual architecture, change YouTube acquisition, refactor shared capture core, or optimize scan performance in this closure.
- Done looks like: the review identifies whether the patch closes F1/F2, keeps the public lookup shape compatible, keeps completion semantics transcript-scoped as documented, and tests the actual loadable-but-bad watch packet subclass rather than a manifest/size/SHA load failure.

## Method Order

REFERENCE-LOAD these methods first. Do not APPLY them yet:

- `workflow-deep-thinking`
- `workflow-code-review`

Then SOURCE-LOAD the target files and context-only files listed in preflight. Declare either `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources and material gaps. Only after that declaration, APPLY `workflow-deep-thinking` to frame failure modes, then APPLY `workflow-code-review` for findings-first review.

If `workflow-code-review` is unavailable, unresolved, or cannot be applied, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` with the reason and do not emit strict review claims.

## Review Axes To Attack

Focus on blocker/major correctness and review-confidence failures:

- Whether a watch-surface packet whose `youtube_watch_capture.json` loads through `DataLakeRoot.load_raw_packet(...)` but cannot be interpreted becomes a distinct `youtube_metadata_packet_discovery_failed:<packet_id>:<reason>` residual.
- Whether the projection avoids laundering that condition into only `youtube_metadata_packet_absent` while still honestly reporting no usable `metadata_capture`.
- Whether the new residual is target-projected in the same limited sense as the existing transcript discovery residuals, and whether the prompt/code avoids claiming a new lane/global residual architecture.
- Whether `metadata_packet_for_video(...)` keeps its existing `dict | None` return shape for callers while the from-lake projection path receives discovery residuals.
- Whether healthy metadata discovery, latest-selection, explicit metadata override behavior, and transcript-source discovery are unchanged.
- Whether the corruption test keeps the manifest size/SHA coherent so it exercises the intended loadable-but-uninterpretable payload subclass rather than a `DataLakeRootError` integrity failure.
- Whether `behavioral_completeness.complete` remains governed by the documented transcript extraction rollup, and whether any final claim overstates metadata completeness.
- Whether any F3/F4/F5 advisory item was accidentally implemented, overconstrained, or claimed as solved without authority.
- Whether any shared-core, IG parity, live-capture, Cleaning, Judgment, production-runtime, scheduler, dashboard, or buyer-proof claim is implied without authority.

## Validation Evidence To Inspect

Dispatcher-observed focused validation after the Batch 4 patch:

```powershell
cd C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider tests/unit/test_youtube_behavioral_projection.py tests/contract/test_youtube_behavioral_projection_no_runtime_imports.py tests/unit/test_source_capture_youtube_watch_packet.py tests/unit/test_youtube_watch_runner_output_mode.py tests/unit/test_youtube_caption_runner_output_mode.py
```

Observed result in this implementation turn: `29 passed in 1.82s`.

Additional dispatcher-observed lane-adjacent contract check:

```powershell
cd C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider tests/contract/test_capture_runner_lake_seam_coverage.py
```

Observed result in this implementation turn: `5 passed in 0.53s`.

Treat these as evidence to inspect, not as a formal validation claim. If you have repo execution access, rerun the focused pytest commands and report the observed result. If you cannot run them, report `validation_not_run` and review from source.

## Output Contract

Preferred reviewer output is a durable report at:

`C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\review-outputs\youtube_metadata_discovery_residual_closure_advisory_code_review_v0.md`

If filesystem write is unavailable, return the same findings-first report in chat and set `review_location: chat_only_current_thread`. Do not claim chat is equivalent to a missing durable report.

Report findings first, ordered by materiality. Each finding must include:

- `finding_id`
- commissioned target and purpose
- file and line or stable structural anchor
- implementation evidence
- authority or evidence basis
- correctness, validation, runtime, or review-confidence impact
- `minimum_closure_condition`
- `next_authorized_action`
- verification expectation
- whether `patch_queue_entry` is authorized: always `no` for this prompt

Also include:

- source-read ledger
- strict-only blockers and `not proven` boundaries
- validation run status
- open questions
- residual risk
- review-use boundary: findings are decision input only; they are not approval, validation, readiness, mandatory remediation, or executor-ready patch authority until separately accepted or authorized

Use these provenance fields in the durable report or chat output:

```yaml
reviewed_by: operator_or_reviewer_to_fill_or_unrecorded
authored_by: OpenAI/Codex GPT-5
de_correlation_bar: operator_to_fill_or_unrecorded
same_vendor_rationale: not_applicable_unless_same_vendor_sanity_is_claimed
```

Do not fabricate model identity. Do not recommend, prescribe, rank, or imply runtime model choice.

Close with this courier block so the home model can adjudicate later:

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

Include:
- original commission or review target
- implementation context, diff, and reviewed files
- findings and implementation evidence
- proposed patch, diff, or exact requested edits, if authorized
- citations
- reviewer verdict
- validation evidence and not-run checks
- residual risk
- blockers, off-scope flags, and not-proven boundaries
```

For this prompt, `proposed patch`, `diff`, `exact requested edits`, formal verdict, severity authority, readiness, approval, validation pass/fail, and patch queue are `NOT_CLAIMED` unless a later owner instruction binds them.