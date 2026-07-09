# Capture Runner v4.1 Blocker Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed cross-recipient prompt for a read-only adversarial artifact review of the
  Capture Spine runner v4.1 blocker addendum and its underlying source evidence.
use_when:
  - Commissioning a delegated review of whether Capture Spine runners really are blocked from v4.1 lake writes.
  - Checking whether the v4.1 addendum's blocker and patch sequence are source-backed.
open_next:
  - docs/review-outputs/capture_spine_runner_data_lake_v4_1_addendum_v0.md
  - docs/review-outputs/capture_spine_runner_data_lake_dump_audit_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md
  - forseti-harness/data_lake/root.py
  - forseti-harness/runners/
  - forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
branch_or_commit: codex/ig-reels-capture-spine @ f95c33ae4162464354a33cd07be557d2eedc6c89
stale_if:
  - The v4.1 addendum, v4.1 contract, DataLakeRoot, runner CLIs, or seam tests change.
  - The current dirty/untracked state is cleaned, committed, or materially changed.
  - A v4.1 implementation patch lands before this review is run.
authority_boundary: retrieval_only
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

- output_mode: `review-report`
- prompt_artifact_path: `docs/prompts/reviews/capture_runner_v4_1_blocker_adversarial_review_prompt_v0.md`
- review_report_destination: `docs/review-outputs/adversarial-artifact-reviews/capture_runner_v4_1_blocker_adversarial_review_v0.md`
- template_kind: `adversarial-artifact-review`
- template_source: `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
- authorization_basis: current owner request to prompt a delegated review of the v4.1 blocker finding.
- edit_permission: `read-only`; reviewer may write only the review report at the destination above.
- target_files_or_dirs:
  - `docs/review-outputs/capture_spine_runner_data_lake_v4_1_addendum_v0.md`
  - `docs/review-outputs/capture_spine_runner_data_lake_dump_audit_v0.md`
  - `docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md`
  - `orca-harness/data_lake/root.py`
  - `orca-harness/source_capture/writer.py`
  - `orca-harness/source_capture/packet_assembly.py`
  - `orca-harness/runners/`
  - `orca-harness/tests/`
- source_pack: custom v4.1 runner-blocker review pack named in this prompt; expand only when a missing source could change the blocker verdict.
- dirty_state_allowance: dirty worktree is allowed as review context only. Modified/untracked controlling sources must be named in the review and must not be overclaimed as landed/mainline truth.
- expected_branch: `codex/ig-reels-capture-spine`
- expected_head_at_prompt_authoring: `f95c33ae4162464354a33cd07be557d2eedc6c89`
- controlling_source_state_at_prompt_authoring:
  - branch tracks `origin/codex/ig-reels-capture-spine`
  - `core_spine_v0_data_lake_physicality_location_contract_v0.md` is modified
  - `core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md` is untracked
  - several unrelated untracked docs/worktrees exist; ignore unless they affect target evidence
- isolation_decision: neither branch nor worktree creation; this is read-only review plus a report write.
- doctrine_change_decision: no doctrine change requested by the reviewer. If the reviewer concludes doctrine must change, report it as a finding or blocker; do not edit doctrine.
- validation_gates:
  - Required source reads and file:line evidence for load-bearing claims.
  - No live capture, no live runner execution, no external data-root writes.
  - Read-only live-root inspection is optional and must be explicitly reported if used.
  - If tests are run, clear or guard `ORCA_DATA_ROOT` first; otherwise mark tests `not_run`.
- thread_operating_target_continuity: no visible active `thread_operating_target`; omitted.

## Review Commission

You are performing a read-only adversarial artifact review for Orca.

Review target:
`docs/review-outputs/capture_spine_runner_data_lake_v4_1_addendum_v0.md`

Related context target:
`docs/review-outputs/capture_spine_runner_data_lake_dump_audit_v0.md`

Review purpose:
Attack the addendum's blocker claim:

> Current Capture Spine runners do not yet drop data into a v4.1 Orca data lake. Three runners expose a legacy lake seam, nine direct packet writers are local-output only, and the shared `DataLakeRoot` still writes v0/unsharded refs rather than v4.1 root/epoch/sharded refs.

Your job is to decide whether that blocker claim is source-backed, overstated, understated, stale, or wrong, and whether the proposed patch sequence is the smallest complete path before implementation.

Fitness reference:
The work is successful if a Chief Architect can decide whether to authorize implementation from a source-backed review that answers:

- Can all current Source Capture packet writers write into a v4.1 data lake today?
- If not, what is the exact blocker set?
- Is the addendum's patch sequence the smallest complete route, or does it miss a higher-priority blocker?

This fitness reference is an alignment axis to attack, not a pass bar.

## Required Authority Sources

Read these before strict findings:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-of-truth.md`
4. `.agents/workflow-overlay/source-loading.md`
5. `.agents/workflow-overlay/artifact-roles.md`
6. `.agents/workflow-overlay/review-lanes.md`
7. `.agents/workflow-overlay/prompt-orchestration.md`
8. `.agents/workflow-overlay/validation-gates.md`
9. `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`

Then source-load the task sources:

1. `docs/review-outputs/capture_spine_runner_data_lake_v4_1_addendum_v0.md`
2. `docs/review-outputs/capture_spine_runner_data_lake_dump_audit_v0.md`
3. `docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md`
4. `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md`
5. `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md`
6. `orca-harness/data_lake/root.py`
7. `orca-harness/source_capture/writer.py`
8. `orca-harness/source_capture/packet_assembly.py`
9. `orca-harness/runners/*.py`, targeted to packet producers and orchestrators
10. `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
11. Targeted lake/root/runner tests that mention `data_root`, `ORCA_DATA_ROOT`, `raw_path`, `packet_shard`, `contract_version`, `.orca-lake-epoch`, or v4.1

Do not bulk-load unrelated review outputs, all prompts, all research, or all product files.

## Method Sequence

REFERENCE-LOAD `workflow-deep-thinking` first. Do not APPLY it yet. Use it only to prepare a neutral source-reading lens for blocker failure modes.

SOURCE-LOAD the required sources above.

Declare either:

- `SOURCE_CONTEXT_READY`, with a compact source-read ledger; or
- `SOURCE_CONTEXT_INCOMPLETE`, with missing sources, conflicts, and what claims are blocked.

Only after source readiness, APPLY `workflow-deep-thinking` to frame the boundary problem, failure modes, and decision criteria.

Then REFERENCE-LOAD and APPLY `workflow-adversarial-artifact-review`.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot be applied after source readiness, return only a blocked or advisory-only result. Do not emit strict verdicts, readiness claims, validation claims, mandatory remediation, patch queues, or executor-ready handoffs.

## Review Checks

Findings-first. Be maximally adversarial within this commission:

1. Does the v4.1 addendum correctly distinguish legacy lake seam from v4.1 compliance?
2. Does current `DataLakeRoot` actually use v0 marker/ref behavior, or has the addendum missed current code?
3. Are the three seam-enabled runners correctly identified?
4. Are the nine local-output-only packet writers correctly identified?
5. Are the two orchestrators classified correctly, or is one already covered by the seam contract?
6. Do current tests enforce only seam presence, or do any tests already enforce v4.1 marker/epoch/sharded refs?
7. Does the addendum overclaim the untracked v4.1 contract as landed authority?
8. Is the live-root evidence used correctly as legacy evidence, not as a v4.1 validation target?
9. Is the proposed patch sequence smallest complete, or should another blocker be first?
10. Are there any missing sources whose absence blocks a strict review conclusion?

## Output Contract

Write the durable report to:

`docs/review-outputs/adversarial-artifact-reviews/capture_runner_v4_1_blocker_adversarial_review_v0.md`

The report must include:

- retrieval header with `authority_boundary: retrieval_only`;
- `reviewed_by` and `authored_by` fields in the body; use `unrecorded` only if not supplied, never fabricate;
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
  - recommended correction or advisory remediation direction;
- explicit answer to the three fitness-reference questions;
- review-use boundary.

Do not include `patch_queue_entry`. Do not edit source files. Do not run live capture. Do not write to `F:\orca-data-lake`.

After writing the report, return a compact chat summary with:

```yaml
review_summary:
  status: completed | failed | blocked
  review_location: durable_report | chat_only_current_thread
  report_path:
  top_findings:
    - severity:
      issue:
      location:
  recommendation:
  next_action:
```

Review-use boundary:
This review is decision input only. It is not approval, validation, readiness,
mandatory remediation, implementation authorization, or executor-ready patch
authority until separately accepted or authorized by Orca owner / Chief Architect.
