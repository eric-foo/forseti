# YouTube Behavioral Lake Metadata Bridge Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial code review prompt for PR #440 Batch 3: making the
  YouTube behavioral projection discover committed watch metadata/comment packets
  from DataLakeRoot by platform_video_id, instead of requiring a manually passed
  metadata packet.
use_when:
  - Commissioning a bounded review of the Batch 3 YT behavioral lake bridge patch.
  - Checking whether YouTube watch metadata/comments now correlate programmatically
    with transcript/extraction sources by video id without forcing shared IG/YT
    acquisition machinery.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
  - docs/workflows/youtube_first_behavioral_completion_spec_v0.md
  - docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md
```

## Prompt Preflight

```yaml
orca_start_preflight:
  agents_read: yes_supplied_in_current_task_context
  overlay_read: yes_loaded_by_dispatcher
  source_pack: custom_pr440_batch_3_code_diff
  edit_permission: read-only
  target_scope:
    implementation_targets:
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\youtube_capture\behavioral_projection.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\tests\unit\test_youtube_behavioral_projection.py
    context_only:
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\source_capture\youtube_watch_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\tests\unit\test_source_capture_youtube_watch_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\data_lake\root.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\workflows\youtube_first_behavioral_completion_spec_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\workflows\youtube_behavioral_contract_from_merged_main_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\review-outputs\youtube_behavioral_projection_post_patch_adversarial_code_recheck_v0.md
  excluded_from_review_target:
    - this prompt artifact
    - IG behavioral adapter implementation
    - shared capture-core implementation or acquisition unification
    - live YouTube or Instagram probing
    - transcript extraction quality, Cleaning, Judgment, scheduler, dashboard, production runtime, or buyer-proof claims
  dirty_state_checked: yes_by_dispatcher_before_prompt_write
  branch_or_commit_reference: >
    branch `codex/youtube-capture-spine-sync`, PR #440. Review the Batch 3 diff
    after base `5e36ba6e3e83a2a7319e094d22e5242a196b5b97`; if this prompt is
    committed in the same branch, exclude this prompt file from implementation findings.
  output_mode: file-write
  prompt_artifact_path: C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\prompts\reviews\youtube_behavioral_lake_metadata_bridge_adversarial_code_review_prompt_v0.md
  reviewer_output_mode: filesystem-output_preferred
  required_review_report_path: C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\review-outputs\youtube_behavioral_lake_metadata_bridge_advisory_code_review_v0.md
  doctrine_change_decision: no doctrine change requested; review prompt only
  isolation_decision: read-only review; do not create or switch branches/worktrees
  validation_gates:
    - inspect the Batch 3 implementation diff against YouTube behavioral projection and SourceCapturePacket lake semantics
    - optionally rerun the focused pytest command if repo execution is available
  blocked_if_missing:
    - reviewer cannot open the pinned repo/worktree, branch, or PR diff
    - reviewer cannot distinguish behavior/correlation parity from shared acquisition machinery
    - reviewer cannot inspect DataLakeRoot and the YouTube watch packet writer while evaluating the bridge
```

## Commission

Run a read-only adversarial code review of the Batch 3 YT behavioral lake metadata bridge patch on PR #440.

This prompt is routed from fused implementation closeout plus the carried delegated-review discipline. The target is a multi-file implementation/code diff, so this is a read-only `workflow-code-review` commission with adversarial posture. No patch execution, patch queue, formal verdict, readiness claim, runtime model recommendation, or no-new-seam claim is authorized.

De-correlation is a who-constraint, not a runtime model recommendation. The author/home family is OpenAI/Codex. The operator should route this to a different upstream vendor/model-lineage reviewer if claiming `cross_vendor_discovery`; otherwise record the lower bar actually used in the output provenance fields. Unknown or undisclosed reviewer lineage cannot satisfy cross-vendor de-correlation.

Fitness reference:

- Goal: after the watch metadata/comment runner writes SourceCapturePackets to the lake, `project_youtube_behavioral_item_from_lake(...)` should resolve the latest matching watch metadata/comment packet by `platform_video_id` without a manually supplied `metadata_packet`.
- Non-goal: do not make YouTube use IG acquisition machinery, do not introduce a shared scheduler/framework, and do not claim live capture readiness.
- Done looks like: the review identifies whether the patch creates deterministic lake-backed metadata/comment correlation, keeps transcript/extraction behavior intact, avoids false success or hidden failure, and preserves the projection/acquisition boundary.

## Method Order

REFERENCE-LOAD these methods first. Do not APPLY them yet:

- `workflow-deep-thinking`
- `workflow-code-review`

Then SOURCE-LOAD the target files and context-only files listed in preflight. Declare either `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources and material gaps. Only after that declaration, APPLY `workflow-deep-thinking` to frame failure modes, then APPLY `workflow-code-review` for findings-first review.

If `workflow-code-review` is unavailable, unresolved, or cannot be applied, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` with the reason and do not emit strict review claims.

## Review Axes To Attack

Focus on blocker/major correctness and review-confidence failures:

- Whether `metadata_packet_for_video(...)` discovers only committed `youtube_watch_metadata_comments` packets and ignores transcript/audio packets without false matches.
- Whether the latest-packet selection is deterministic and source-backed (`capture_timestamp`, then packet id), and whether ties or missing timestamps create surprising behavior.
- Whether malformed/corrupt packet reads stay fail-visible through existing lake discovery behavior rather than being silently converted to success.
- Whether `_watch_metadata_packet(...)` reconstructs the nested watch capture payload without laundering route receipts or dropping platform/video identity.
- Whether `project_youtube_behavioral_item_from_lake(...)` still respects an explicit `metadata_packet` override and does not rebuild availability unless explicitly requested.
- Whether transcript-source discovery, extraction-result matching, canonical-source selection, and no-runtime-acquisition boundaries remain intact.
- Whether the new tests prove the real behavior using an actual `write_youtube_watch_packet(..., data_root=...)` commit, not a synthetic manual metadata dict only.
- Whether any shared-core, IG parity, live-capture, Cleaning, Judgment, production-runtime, scheduler, dashboard, or buyer-proof claim is implied without authority.

## Validation Evidence To Inspect

Dispatcher-observed focused validation after the Batch 3 patch:

```powershell
cd C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider tests/unit/test_youtube_behavioral_projection.py tests/contract/test_youtube_behavioral_projection_no_runtime_imports.py tests/unit/test_source_capture_youtube_watch_packet.py tests/unit/test_youtube_watch_runner_output_mode.py tests/unit/test_youtube_caption_runner_output_mode.py
```

Observed result in this implementation turn: `28 passed in 1.53s`.

Treat this as evidence to inspect, not as a formal validation claim. If you have repo execution access, rerun the focused pytest command and report the observed result. If you cannot run it, report `validation_not_run` and review from source.

## Output Contract

Preferred reviewer output is a durable report at:

`C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\review-outputs\youtube_behavioral_lake_metadata_bridge_advisory_code_review_v0.md`

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