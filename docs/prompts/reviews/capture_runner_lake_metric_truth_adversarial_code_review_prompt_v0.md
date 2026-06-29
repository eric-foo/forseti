# Capture Runner Lake + Metric Truth Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial code review prompt for the Batch 1 + Batch 2 capture
  enforcement patch on PR #440: packet-runner lake seam/output-mode contracts,
  YouTube caption runner output-mode behavior, and YouTube watch metric receipt
  truth/no-zero-fill enforcement.
use_when:
  - Commissioning a bounded review of the Batch 1 + Batch 2 patch before owner merge.
  - Checking whether capture runner storage contracts and YouTube watch metric truth contracts are enforced by code without forcing shared IG/YT acquisition mechanics.
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
  source_pack: custom_S0_plus_pr440_batch_1_2_code_diff
  repo_map_decision: targeted_route_checked
  repo_map_reason: `docs/prompts/reviews/`, `docs/review-outputs/`, `orca-harness/runners/`, `orca-harness/source_capture/`, and `orca-harness/tests/` are already map-reachable for this prompt and patch scope.
  edit_permission: read-only
  target_scope:
    implementation_targets:
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\tests\contract\test_capture_runner_lake_seam_coverage.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\runners\run_source_capture_youtube_caption_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\source_capture\youtube_watch_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\tests\unit\test_source_capture_youtube_watch_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\tests\unit\test_youtube_caption_runner_output_mode.py
    context_only:
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\runners\run_source_capture_youtube_watch_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\source_capture\models.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\source_capture\packet_assembly.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\source_capture\transcript\caption_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness\youtube_capture\capture_youtube_v0.py
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\prompts\reviews\youtube_watch_source_capture_adversarial_code_review_prompt_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\review-outputs\youtube_watch_source_capture_advisory_code_review_v0.md
  excluded_from_review_target:
    - this prompt artifact
    - unrelated IG acquisition route changes
    - shared IG/YT capture-core architecture or route unification
    - live YouTube or Instagram probing
    - transcript extraction quality, Cleaning, Judgment, scheduler, dashboard, production runtime, or buyer-proof claims
  dirty_state_checked: yes_by_dispatcher_before_prompt_write
  branch_or_commit_reference: branch `codex/youtube-capture-spine-sync`, PR #440, review the Batch 1 + Batch 2 diff after base `03cefbe4bc4a8ad4934458c07a8aab1522af30a0`; if this prompt is committed on the same branch, exclude this prompt file from implementation findings.
  controlling_source_state: dispatcher observed the implementation patch in the named worktree; strict readiness, approval, and formal pass claims are not authorized by this prompt.
  output_mode: file-write
  prompt_artifact_path: C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\prompts\reviews\capture_runner_lake_metric_truth_adversarial_code_review_prompt_v0.md
  delivery_copy: paste-ready-chat copy may be used after this filed prompt artifact exists
  reviewer_output_mode: filesystem-output_preferred
  required_review_report_path: C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\review-outputs\capture_runner_lake_metric_truth_advisory_code_review_v0.md
  doctrine_change_decision: no doctrine change requested; review prompt only
  isolation_decision: read-only review; do not create or switch branches/worktrees
  validation_gates:
    - inspect the Batch 1 + Batch 2 implementation diff against source_capture packet semantics and runner storage behavior
    - optionally rerun the focused pytest command if repo execution is available
  blocked_if_missing:
    - reviewer cannot open the pinned repo/worktree, branch, or PR diff
    - reviewer cannot distinguish source-capture packet/runner contracts from platform acquisition methods
    - reviewer cannot inspect SourceCapturePacket models and packet_assembly while evaluating the writer/contract tests
```

## Commission

Run a read-only adversarial code review of the Batch 1 + Batch 2 capture enforcement patch on PR #440.

This prompt was routed from an explicit `workflow-delegated-review-patch` request, but Orca's delegated-review-patch overlay marks multi-file implementation/code diffs as non-eligible for the provisional bounded patch convention unless separate patch execution is bound. Therefore this is a read-only `workflow-code-review` commission with adversarial posture. No patch execution, patch queue, formal verdict, readiness claim, runtime model recommendation, or no-new-seam claim is authorized.

De-correlation is a who-constraint, not a runtime model recommendation. The author/home family is OpenAI/Codex. The operator should route this to a different upstream vendor/model-lineage reviewer if claiming `cross_vendor_discovery`; otherwise record the lower bar actually used in the output provenance fields. Unknown or undisclosed reviewer lineage cannot satisfy cross-vendor de-correlation.

Fitness reference:

- Goal: enforce the valuable Batch 1 + Batch 2 capture contracts by code while avoiding shared acquisition-method lock-in across IG and YT.
- Batch 1: storage/runner contract - packet-producing runners expose a data-lake seam, forward `data_root`, and keep `--output` local mode mutually exclusive with `--data-root`/`ORCA_DATA_ROOT` lake mode.
- Batch 2: metric truth contract - YT watch metric observations must come from complete metric receipts; missing/hidden metrics must be explicit unavailable postures, never fallback observed values or zero-looking rollups.
- Done looks like: the review identifies whether the patch actually enforces those contracts, whether it overconstrains platform acquisition, and whether the tests catch the failure modes without false confidence.

## Method Order

REFERENCE-LOAD these methods first. Do not APPLY them yet:

- `C:\Users\vmon7\.codex\skills\workflow-deep-thinking\SKILL.md` or the resolver-visible `workflow-deep-thinking` skill
- `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.87\skills\workflow-code-review\SKILL.md` or the resolver-visible `workflow-code-review` skill

Then SOURCE-LOAD the target files and context-only files listed in preflight. Declare either `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources and material gaps. Only after that declaration, APPLY `workflow-deep-thinking` to frame failure modes, then APPLY `workflow-code-review` for findings-first review.

If `workflow-code-review` is unavailable, unresolved, or cannot be applied, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` with the reason and do not emit strict review claims.

## Review Axes To Attack

Focus on blocker/major correctness and review-confidence failures:

- Whether `test_capture_runner_lake_seam_coverage.py` now detects thin source-capture packet writer wrappers such as `write_youtube_watch_packet` and `write_caption_packet` without accidentally classifying non-packet derived-record runners or internal helper calls.
- Whether the widened lake-seam detector still protects every packet-producing runner from missing `--data-root`, missing `ORCA_DATA_ROOT`, missing `DataLakeRoot.resolve`, or missing `data_root=` forwarding.
- Whether the new output-mode exclusivity check catches both explicit `--output + --data-root` ambiguity and env fallback overriding explicit `--output`, without requiring unrelated stdout-only or data-lake-only runners to grow fake local-output modes.
- Whether `run_source_capture_youtube_caption_packet.py` now rejects explicit dual mode and correctly ignores `ORCA_DATA_ROOT` when `--output` is explicit, without changing acquisition behavior or caption packet semantics.
- Whether `youtube_watch_packet.py` rejects observed metric values without complete receipts (`source_route`, `source_path`, `artifact`) and rejects unavailable receipts without reason/routes checked.
- Whether the writer correctly rejects stale/mismatched metric receipt values rather than silently using `engagement` fallbacks.
- Whether missing like/comment totals remain `unavailable_with_reason` with no zero-filled value, and whether visible mode changes no longer look like metric-value zero-fills.
- Whether preserving route receipts in `youtube_watch_capture.json` remains platform-specific and does not force shared IG/YT acquisition machinery.
- Whether the new tests prove the load-bearing behaviors and fail for the old failure modes.
- Whether any transcript quality, Cleaning, Judgment, production-runtime, scheduler, dashboard, broad crawling, or shared-core claim is implied without authority.

## Validation Evidence To Inspect

Dispatcher-observed focused validation after the Batch 1 + Batch 2 patch:

```powershell
cd C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\orca-harness
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider tests/contract/test_capture_runner_lake_seam_coverage.py tests/unit/test_source_capture_youtube_watch_packet.py tests/unit/test_youtube_caption_runner_output_mode.py tests/unit/test_youtube_capture_metadata_helpers.py tests/unit/test_youtube_capture_view_count.py tests/unit/test_youtube_behavioral_projection.py
```

Observed result in this implementation turn: `33 passed in 1.70s`.

Additional dispatcher-observed checks before this prompt was written:

```powershell
python -c "from pathlib import Path; files=['orca-harness/source_capture/youtube_watch_packet.py','orca-harness/runners/run_source_capture_youtube_caption_packet.py','orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py','orca-harness/tests/unit/test_source_capture_youtube_watch_packet.py']; [compile(Path(p).read_text(encoding='utf-8'), p, 'exec') for p in files]; print('compile ok')"
git diff --check
```

Observed result: `compile ok`; `git diff --check` exited 0 and printed only a line-ending warning for the contract test working copy.

Treat these as evidence to inspect, not as a formal validation claim. If you have repo execution access, rerun the focused pytest command and report the observed result. If you cannot run it, report `validation_not_run` and review from source.

## Output Contract

Preferred reviewer output is a durable report at:

`C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-capture-spine-sync\docs\review-outputs\capture_runner_lake_metric_truth_advisory_code_review_v0.md`

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
