# YouTube Watch Source Capture Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial code review prompt for PR #440's YouTube watch-page
  metadata/comments SourceCapturePacket sync: extractor availability states,
  metric receipts, packet writer, runner, projection carry-through, Shorts
  posture alignment, and focused tests.
use_when:
  - Commissioning a bounded review of PR #440 before owner merge.
  - Checking whether YouTube watch metadata/comments are on source_capture rails without zero-filled absent metrics, fake comments-disabled states, or transcript/Cleaning/Judgment overclaims.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```yaml
orca_start_preflight:
  agents_read: yes_supplied_in_current_task_context
  overlay_read: yes_loaded_by_dispatcher
  source_pack: custom_S0_plus_capture_method_plus_pr440_code_diff
  repo_map_decision: targeted_route_checked
  repo_map_reason: PR #440 added new source_capture writer/runner entries and repo-map route; dispatcher verified the map route during the implementation lane.
  edit_permission: read-only
  target_scope:
    implementation_targets:
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\source_capture\youtube_watch_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\runners\run_source_capture_youtube_watch_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\youtube_capture\capture_youtube_v0.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\youtube_capture\shorts_scroll_capture_v0.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\youtube_capture\behavioral_projection.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\tests\unit\test_source_capture_youtube_watch_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\tests\unit\test_youtube_capture_view_count.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\tests\unit\test_youtube_behavioral_projection.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\tests\contract\test_capture_runner_lake_seam_coverage.py
    context_only:
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\source_capture\models.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\source_capture\writer.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\source_capture\transcript\caption_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\source_capture\transcript\asr_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\workflows\orca_repo_map_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca\product\spines\capture\core\source_capture_toolbox\source_capture_playbook_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca\product\spines\capture\core\source_capture_toolbox\capture_recon_index_v0.md
  excluded_from_review_target:
    - this prompt artifact
    - unrelated IG capture implementation
    - shared IG/YT capture-core architecture
    - live YouTube probing or source-system access
    - transcript, Cleaning, Judgment, scheduler, dashboard, or production-runtime claims
  dirty_state_checked: yes_by_dispatcher
  branch_or_commit_reference: PR #440, branch codex/youtube-capture-spine-sync, implementation commit 0ad8b3478460f981ff12be8438007a3da55c4629; if the branch later advances only to add this prompt, review the implementation target diff and exclude this prompt file
  controlling_source_state: dispatcher observed clean worktree at implementation commit before this prompt artifact was filed; strict readiness and formal pass claims are not authorized by this prompt
  output_mode: file-write
  prompt_artifact_path: C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\prompts\reviews\youtube_watch_source_capture_adversarial_code_review_prompt_v0.md
  delivery_copy: paste-ready-chat copy may be used after this filed prompt artifact exists
  reviewer_output_mode: filesystem-output_preferred
  required_review_report_path: C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\review-outputs\youtube_watch_source_capture_advisory_code_review_v0.md
  doctrine_change_decision: no doctrine change requested; review prompt only
  isolation_decision: read-only review; do not create or switch branches/worktrees
  validation_gates:
    - inspect PR #440 implementation diff against source_capture packet semantics and YouTube extractor behavior
    - optionally rerun the focused pytest command if repo execution is available
  blocked_if_missing:
    - reviewer cannot open the pinned repo/worktree or PR diff
    - reviewer cannot distinguish source-capture packet semantics from transcript, Cleaning, Judgment, or production-runtime behavior
    - reviewer cannot inspect `SourceCapturePacket` models/writer while evaluating the new writer
```

## Commission

Run a read-only adversarial code review of PR #440's YouTube watch metadata/comments Source Capture sync. The review target is the implementation code plus tests listed above, not this prompt, not a live YouTube probe, not a shared IG/YT capture core, and not any transcript/Cleaning/Judgment downstream lane.

This prompt was routed from an explicit `workflow-delegated-review-patch` request, but Orca's delegated-review-patch overlay marks multi-file implementation/code diffs as non-eligible for the provisional bounded patch convention unless separate patch execution is bound. Therefore this is a read-only `workflow-code-review` commission with adversarial posture. No patch execution, patch queue, formal verdict, readiness claim, runtime model recommendation, or no-new-seam claim is authorized.

De-correlation is a who-constraint, not a runtime model recommendation. The author/home family is OpenAI/Codex. The operator should route this to a different upstream vendor/model-lineage reviewer if claiming `cross_vendor_discovery`; otherwise record the lower bar actually used in the output provenance fields. Unknown or undisclosed reviewer lineage cannot satisfy cross-vendor de-correlation.

Fitness reference:

- Goal: make YouTube watch-page metadata/comments capture trustworthy as a platform-specific source_capture packet path without forcing shared IG/YT acquisition machinery.
- Done looks like: the review identifies whether availability states, metric receipts, like/comment extraction, comment sample-vs-total separation, no-zero-fill behavior, packet staging, data-lake runner seam, behavioral projection carry-through, Shorts posture semantics, and tests are correct enough for owner review of PR #440, with concrete closure conditions for any material finding.

## Method Order

REFERENCE-LOAD these methods first. Do not APPLY them yet:

- `C:\Users\vmon7\.codex\skills\workflow-deep-thinking\SKILL.md` or the resolver-visible `workflow-deep-thinking` skill
- `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.87\skills\workflow-code-review\SKILL.md` or the resolver-visible `workflow-code-review` skill

Then SOURCE-LOAD the target files and context-only files listed in preflight. Declare either `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources and material gaps. Only after that declaration, APPLY `workflow-deep-thinking` to frame failure modes, then APPLY `workflow-code-review` for findings-first review.

If `workflow-code-review` is unavailable, unresolved, or cannot be applied, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` with the reason and do not emit strict review claims.

## Review Axes To Attack

Focus on concrete correctness or review-confidence failures. In particular, inspect:

- Whether `fetch_youtube_watch` and legacy `capture` preserve incumbent behavior while adding availability states and route receipts without changing acquisition assumptions invisibly.
- Whether `detect_video_state`, `comments_disabled_signal`, and comment-token handling distinguish removed/private/age/login/region/unknown from playable, and distinguish `comments_disabled` from `comments_not_exposed` without brittle phrase overreach.
- Whether `extract_like_count`, `parse_exact_count_text`, `player_view_count`, and metric receipt construction avoid zero-filling absent metrics and avoid converting approximate or presentation text into exact counts.
- Whether `comment_sample_count` and `total_comment_count` are separated correctly across legacy packet, source_capture packet payload, metric observations, and limitations.
- Whether `youtube_watch_packet.py` stages raw watch HTML and youtubei JSON pages correctly, preserves route receipts in the JSON payload, and emits SourceCapture slices whose semantics fit `SourceCapturePacket` models without schema lock-in.
- Whether the runner genuinely exercises the data-lake seam (`--data-root` / `ORCA_DATA_ROOT`) and remains injectable/offline-testable rather than requiring network access in tests.
- Whether behavioral projection now preserves availability/receipts without pretending to acquire data or make creator-ledger inferences itself.
- Whether Shorts posture changes improve honesty without regressing existing comment sample extraction or collapsing route non-exposure into disabled comments.
- Whether tests prove the load-bearing behavior: no zero-fill, route receipt preservation, packet validity, data-lake runner coverage, projection carry-through, and view-count helper regressions.
- Whether any source-capture, transcript, Cleaning, Judgment, production-runtime, scheduler, dashboard, broad crawling, or shared-core claim is implied without authority.

## Validation Evidence To Inspect

Dispatcher-observed focused validation from the implementation turn:

```powershell
cd C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider -q tests/unit/test_source_capture_youtube_watch_packet.py tests/unit/test_youtube_capture_view_count.py tests/unit/test_youtube_behavioral_projection.py tests/contract/test_capture_runner_lake_seam_coverage.py
```

Observed result in that turn: `19 passed`.

Additional dispatcher-observed checks after implementation:

```powershell
python .agents/hooks/check_repo_map_freshness.py --diff origin/main --strict
python .agents/hooks/check_retrieval_header.py --strict docs/workflows/orca_repo_map_v0.md
python .agents/hooks/header_index.py --strict --base origin/main
python .agents/hooks/check_map_links.py --strict
git diff --cached --check
```

Observed result: all passed; `check_map_links --strict` reported `OK (0 findings)` and annotated nonresolving debt only.

Treat these as evidence to inspect, not as a formal validation claim. If you have repo execution access, rerun the focused pytest command and report the observed result. If you cannot run it, report `validation_not_run` and review from source.

## Output Contract

Preferred reviewer output is a durable report at:

`C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\review-outputs\youtube_watch_source_capture_advisory_code_review_v0.md`

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
