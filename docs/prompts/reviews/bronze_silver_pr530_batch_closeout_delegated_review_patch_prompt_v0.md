# Delegated Review-and-Patch Prompt - PR 530 Batch Closeout v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (review family; delegated review-and-patch commission)
scope: >
  Controller prompt for a de-correlated adversarial review of the just-completed
  Bronze/Silver PR 530 material-sequence batch closeout, with patch authority
  limited to corrected batch-closeout text or corrected next-batch instructions.
use_when:
  - Commissioning an independent controller to review the PR 530 material-sequence batch closeout before acting on its next-step conclusions.
  - Checking whether the closeout correctly names success signals, batch outcomes, stack blockers, and assumption-gate status without overclaiming Bronze, Silver, AR, or runtime readiness.
  - Adjudicating a returned replacement closeout, corrected instruction block, or no-patch result.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/source-loading.md
  - docs/prompts/handoffs/bronze_silver_post_pr530_goal_frame_handoff_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
branch_or_commit: codex/bronze-silver-ar-convergence @ 36719e561c535620026261fce64efd648eb2737d
stale_if:
  - The PR 530 branch advances before the controller starts.
  - PR 530, PR 523, PR 478, or main stack status changes before the controller starts.
  - Home-model adjudication for this batch closeout completes.
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```yaml
orca_start_preflight:
  authorization_basis: current owner clarification that delegated review-patch target is the just-completed batch
  agents_read: yes_supplied_in_current_task_context
  overlay_read: yes_loaded_by_dispatcher
  source_pack: custom_batch_closeout_plus_pr530_stack_and_ig_projection_sources
  repo_map_decision: targeted
  repo_map_reason: review target is a workflow decision artifact, not a new product authority artifact
  edit_permission: prompt artifact file-write by dispatcher; controller patch authority limited to replacement closeout text or corrected next-batch instructions
  target_scope:
    review_target:
      - inline batch-closeout transcript excerpt in this prompt
    context_only:
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\AGENTS.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\.agents\workflow-overlay\README.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\.agents\workflow-overlay\source-of-truth.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\.agents\workflow-overlay\source-loading.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\.agents\workflow-overlay\review-lanes.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\.agents\workflow-overlay\prompt-orchestration.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\.agents\workflow-overlay\delegated-review-patch.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\docs\prompts\handoffs\bronze_silver_post_pr530_goal_frame_handoff_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca-harness\data_lake\catalog.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca-harness\source_capture\ig_reels_grid_projection.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca-harness\tests\test_data_lake_catalog.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca-harness\tests\unit\test_source_capture_ig_reels_projection.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca\product\spines\data_lake\authority\core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca\product\spines\data_lake\authority\core_spine_v0_data_lake_silver_vault_record_contract_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca\product\spines\data_lake\authority\core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  excluded_from_review_target:
    - PR 530 six-file delegated review target already commissioned by a separate prompt
    - runtime code edits, tests, runners, CI, overlay doctrine, and unrelated product spines
    - commit, push, PR, merge, automerge label, or source-changing follow-on work
  dirty_state_checked: yes_by_dispatcher_before_prompt_file
  branch_or_commit_reference: local branch codex/bronze-silver-ar-convergence at 36719e561c535620026261fce64efd648eb2737d
  controlling_source_state: the batch closeout excerpt is the target; repo and GitHub facts inside it are claims to recheck, not inherited current truth
  output_mode: file-write prompt artifact plus paste-ready delivery copy
  prompt_artifact_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\docs\prompts\reviews\bronze_silver_pr530_batch_closeout_delegated_review_patch_prompt_v0.md
  reviewer_output_mode: review-report plus replacement closeout text or corrected next-batch instructions if warranted
  required_review_report_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\docs\review-outputs\adversarial-artifact-reviews\bronze_silver_pr530_batch_closeout_delegated_review_patch_v0.md
  doctrine_change_decision: none; this prompt does not change doctrine or authorize source changes
  isolation_decision: use the existing isolated PR 530 worktree; do not create or switch branches/worktrees for the review
  validation_gates:
    - recheck local branch/head and dirty state before treating branch facts as current
    - recheck GitHub PR stack facts if network and auth are available
    - rerun or inspect the targeted IG projection tests if execution is available
    - run prompt/report hygiene checks if the controller writes a report or edits an allowed prompt/report artifact
  blocked_if_missing:
    - controller cannot see the inline target excerpt
    - controller cannot prove de-correlation from the author/home model family
    - controller cannot distinguish replacement closeout text from repo source patch authority
```

## Commission

Run a delegated, de-correlated adversarial review-and-patch pass over the
just-completed PR 530 material-sequence batch closeout. The target is not a
repo source diff. The target is the closeout decision artifact captured below.

Patch authority is intentionally narrow:

- You may return replacement batch-closeout text.
- You may return corrected next-batch instructions.
- You may write the required review report if you have filesystem access.
- You must not edit repo source, tests, PR metadata, branch state, overlay
  doctrine, PR 530's six-file documentation patch, or runtime code.
- If the right correction requires a repo source patch, return
  `REPO_PATCH_REQUIRED_BUT_UNAUTHORIZED` with the minimum closure condition.

## Actor / Model-Family Receipt

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI / GPT (Codex based on GPT-5 authored the batch closeout and this commission)
  controller_model_family: operator_to_fill; should be non-OpenAI vendor lineage for cross-vendor discovery
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: verify_at_run_start
```

This is a who-constraint, not a model recommendation. Vendor means upstream
model developer/provider, not hosting platform, wrapper, reseller, or tier. If
your lineage is OpenAI or unknown/undisclosed, stop before review and return
`BLOCKED_CONTROLLER_NOT_DECORRELATED`. No tester/testee shortcut: you are the
controller; do not dispatch subagents or a replacement controller.

## Review Target

The batch being reviewed followed the owner's requested sequence:

- Name success signals first.
- Batch steps 1-2 together.
- Batch step 3.
- Batch step 4.
- Batch steps 5-6 together.
- Use an assumption-gate lens across the batches.

Dispatcher closeout to review:

```text
Success signals:
- A Silver-facing proving slice consumes public Bronze surfaces rather than
  private folder semantics.
- Raw/source references are hash-checkable where available, and missing AR is
  visible residual rather than inferred absence.
- The generated Bronze catalog remains retrieval-only, not authority.
- No full Bronze GT, Silver readiness, AR runtime, storage/backend, lake-doctor,
  or Manifest v2 implementation claim is introduced.

Batch 1-2:
- PR 530 was observed open, ready, clean, CI green, and without automerge label.
- PR 523 was observed open, clean, CI green, and stacked under PR 530.
- PR 478 was observed open draft to main.
- Local ancestry check returned HEAD_ON_MAIN=no.
- Conclusion: PR 530 is stacked as 530 -> 523 -> 478; starting source-changing
  follow-on work off main is blocked unless the owner explicitly redirects to a
  stack branch.

Batch 3:
- Targeted IG projection tests passed with output:
  "........ [100%]"
- Tested catalog rows exposing packet and AR query rows, current catalog
  requirement, absent-surface shape, IG reels projection from Bronze catalog,
  stable non-duplicate record IDs, skip-existing convergence, current-catalog
  requirement, and runner projection from bronze source surface.
- Local worktree remained clean at branch codex/bronze-silver-ar-convergence,
  HEAD 36719e56.

Batch 4:
- No patch was applied.
- The IG reels-grid path already showed the first proof surface:
  source_surface_catalog_rows exposes packet_rows, attachment_record_rows, and
  load_attachment_record_body; project_ig_reels_grid_from_bronze_catalog uses
  those public Bronze catalog and AR surfaces; tests cover the consumer path.

Batch 5-6:
- No commit, push, or PR action was taken because no source changed.

Assumption-gate result:
- READY_WITH_VERIFIED_LEDGER for the IG selected proof slice as the next
  evidence-backed Silver-facing target.
- BLOCKED for source-changing follow-on off main until the stack settles or the
  owner explicitly redirects the work to a stack branch.
```

## Required Source Checks

Use source checks to attack the closeout. Treat all dispatcher-observed PR
facts as claims to recheck if they are material to a finding.

1. Read `AGENTS.md`, `.agents/workflow-overlay/README.md`,
   `.agents/workflow-overlay/source-of-truth.md`,
   `.agents/workflow-overlay/source-loading.md`,
   `.agents/workflow-overlay/review-lanes.md`,
   `.agents/workflow-overlay/prompt-orchestration.md`, and
   `.agents/workflow-overlay/delegated-review-patch.md`.
2. Read the handoff packet:
   `docs/prompts/handoffs/bronze_silver_post_pr530_goal_frame_handoff_v0.md`.
   Re-read its named load-bearing sources before making strict claims.
3. Verify or explicitly mark unavailable:
   - local branch/head/dirty state;
   - PR 530, PR 523, PR 478 stack status;
   - local `HEAD_ON_MAIN` ancestry check;
   - targeted IG projection tests or the relevant test/source lines.
4. Inspect only enough of the IG projection sources and tests to support or
   refute the closeout's "no patch needed" and "IG proof slice selected"
   conclusions. Expand to full reads if a targeted read could change a finding.
5. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before
   findings.

## Review Questions

Answer these adversarially:

- Did the batch name the right success signals before batching, or did it miss a
  load-bearing signal needed before acting?
- Did batch 1-2 overstate the stack blocker, understate it, or fail to name the
  next admissible lane?
- Did batch 3 prove enough for the stated IG proof-slice selection, or should it
  have been downgraded to advisory evidence only?
- Was "no patch" in batch 4 correct, or did the batch need a prompt/report/doc
  correction despite no source change?
- Was "no commit/push/PR" in batch 5-6 correct, or did the batch create a
  durable artifact requiring normal lifecycle handling?
- Is `READY_WITH_VERIFIED_LEDGER` too strong, too weak, or correctly scoped?
- Is `BLOCKED for source-changing follow-on off main` correctly scoped to
  source-changing work only, without blocking review/prompt-only work on the
  existing PR 530 lane?

## Bounded Patch Scope

If a correction is warranted, return one of these patch forms:

- `REPLACEMENT_BATCH_CLOSEOUT`: a corrected closeout that can replace the
  reviewed batch closeout.
- `CORRECTED_NEXT_BATCH_INSTRUCTIONS`: a short instruction block for the next
  operator turn.
- `REPO_PATCH_REQUIRED_BUT_UNAUTHORIZED`: no patch text; name the source file or
  PR action that would need a separate explicit commission.
- `NO_BATCH_PATCH_NEEDED`: no replacement needed.

Do not provide a working-tree diff except for the optional review report file.
Do not patch PR 530 source artifacts under this commission.

## Output Contract

Write a durable report to:

`C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\docs\review-outputs\adversarial-artifact-reviews\bronze_silver_pr530_batch_closeout_delegated_review_patch_v0.md`

If the report cannot be written, return `FAILED_REVIEW_OUTPUT_WRITE` and do not
claim a report path. If no patch is warranted, leave no target diff and state
`NO_BATCH_PATCH_NEEDED`.

Report contents:

- compact `review_summary` YAML;
- actor/model-family receipt and de-correlation status;
- source-read ledger;
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`;
- findings first, ordered by materiality, with location, issue, evidence,
  impact, `minimum_closure_condition`, `next_authorized_action`, and verification
  expectation;
- one bounded patch form from the Bounded Patch Scope section;
- validation run status or `validation_not_run` with reason;
- verdict-as-decision-input and residual-risk note;
- provenance fields:

```yaml
reviewed_by: operator_or_reviewer_to_fill_or_unrecorded
authored_by: OpenAI/Codex GPT-5
de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback | unrecorded
same_vendor_rationale: not_applicable_unless_same_vendor_sanity_is_claimed
```

Close with this courier block so the home model can adjudicate:

```text
DELEGATED_REVIEW_PATCH_RETURN_FOR_HOME_MODEL

Here is the delegated review-and-patch result for the PR 530 batch closeout.
Adjudicate it under the delegated-review-patch return contract.

Include:
- original commission and target label `[batch-closeout]`
- reviewed branch/head, PR stack facts checked, and dirty-state result
- source readiness status and reviewed files
- findings and evidence
- one bounded patch form: REPLACEMENT_BATCH_CLOSEOUT, CORRECTED_NEXT_BATCH_INSTRUCTIONS, REPO_PATCH_REQUIRED_BUT_UNAUTHORIZED, or NO_BATCH_PATCH_NEEDED
- validation evidence and not-run checks
- residual risk
- blockers, off-scope flags, and not-proven boundaries
```

The delegate's replacement text, findings, and verdict are claims to adjudicate,
not premises to inherit. This commission is not approval, validation, readiness,
mandatory remediation, source promotion, Bronze full-GT declaration, Silver
implementation authorization, AR runtime implementation authorization, runtime
model routing, or permission to edit outside the batch-closeout review target.
