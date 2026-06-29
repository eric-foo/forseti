# CSB Validator Batch 1 Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial code review prompt for PR #360, Batch 1 CSB output
  validator hardening: full-board section contract, Section 4 row/vocab checks,
  Section 8 handoff packet shape, Section 10 board status, passing fixtures,
  targeted regression tests, and the playbook validator description.
use_when:
  - Commissioning a bounded read-only review of PR #360 before merge or closeout acceptance.
  - Checking whether Batch 1 catches deterministic CSB output fake-pass modes without adding CI, artifact-path, or prohibited-term linter scope.
authority_boundary: retrieval_only
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```yaml
orca_start_preflight:
  agents_read: yes_supplied_in_current_task_context
  overlay_read: yes_loaded_by_dispatcher
  source_pack: custom_S0_plus_pr360_csb_validator_batch1
  authorization_basis: >
    Current-turn explicit invocation of workflow-delegated-review-patch after a
    fused implementation review checkpoint. Orca delegated-review-patch overlay
    routes multi-file implementation/code diffs to an appropriate read-only
    code review prompt unless a separate patch-execution commission is bound.
  objective: >
    Review whether PR #360 correctly hardens the Commission Signal Board output
    validator for deterministic structural/vocabulary/status failures while
    preserving existing handoff rules and avoiding deferred scope.
  intended_decision: >
    Identify any blocker or material review-confidence issue the home model
    should adjudicate before merge or further batching.
  output_mode: file-write
  delivery_copy: paste-ready-chat copy may be used after this filed prompt artifact exists
  reviewer_output_mode: filesystem-output_preferred
  required_review_report_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\csb-validator-batch1\docs\review-outputs\csb_validator_batch1_adversarial_code_review_v0.md
  edit_permission: read-only
  branch_or_commit_reference:
    worktree: C:\Users\vmon7\Desktop\projects\orca\worktrees\csb-validator-batch1
    branch: codex/csb-validator-batch1
    expected_head: 8287a0791e9239939cc3a0b2355916b73953d8da
    base_reference: origin/main
    expected_base_head: 532f01038668455b774bb70dc05aa633ad5bca0e
    dirty_state_allowance: clean_or_prompt_file_only_if_dispatcher_has_not_committed_this_prompt
  target_files_or_dirs:
    changed_files:
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\csb-validator-batch1\.agents\hooks\check_commission_signal_board_output.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\csb-validator-batch1\orca-harness\tests\unit\test_commission_signal_board_output_validator.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\csb-validator-batch1\orca-harness\tests\fixtures\commission_signal_board_outputs\valid_empty_backtest_output.txt
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\csb-validator-batch1\orca-harness\tests\fixtures\commission_signal_board_outputs\valid_source_backed_backtest_output.txt
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\csb-validator-batch1\orca-harness\tests\fixtures\commission_signal_board_outputs\valid_source_backed_forward_output.txt
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\csb-validator-batch1\orca\product\spines\commission_signal_board\workflows\commission_signal_board_playbook_v0.md
    context_only:
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\csb-validator-batch1\docs\prompts\handoffs\imaginary_authors_csb_broad_scout_deep_scan_handoff_prompt_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\csb-validator-batch1\.agents\workflow-overlay\delegated-review-patch.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\csb-validator-batch1\.agents\workflow-overlay\review-lanes.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\csb-validator-batch1\.agents\workflow-overlay\prompt-orchestration.md
  controlling_source_state: clean_branch_observed_before_prompt_write
  doctrine_change_decision: no doctrine change requested; prompt filing only
  isolation_decision: existing PR worktree/branch reused because this prompt reviews that branch state
  template_kind: review
  template_source_used: generic workflow-prompt-orchestrator review template plus existing Orca adversarial code-review prompt shape; no project repo-code-review template is registered
  workflow_sequence_status: bound_by_delegated_review_patch_non_eligible_target_boundary_to_read_only_code_review
  thread_operating_target_continuity:
    carried_forward: no
    reason: no_visible_active_target
    changed_from_input: no
    lifecycle_status: not_applicable
  validation_gates:
    - inspect branch diff against origin/main
    - inspect validator selftest behavior and targeted pytest evidence
    - optionally rerun focused validation if repo execution is available
  blocked_if_missing:
    - source-of-truth worktree is unavailable
    - HEAD or base reference differs without an explicit dispatcher update
    - reviewer cannot distinguish read-only code review from delegated patch execution
```

## Commission

Run a read-only adversarial code review of PR #360, "Harden CSB output validator structure checks."

This prompt was routed from an explicit `workflow-delegated-review-patch` invocation, but Orca's delegated-review-patch overlay marks multi-file implementation/code diffs as non-eligible for that provisional bounded patch convention unless separate patch execution is bound. Therefore this is a read-only code review commission with adversarial posture. Do not edit files. Do not emit an executor-ready patch queue. Do not claim delegated patch authority, formal approval, readiness, or validation.

Fitness reference:

- Goal: make the CSB output validator catch deterministic Commission Signal Board fake-pass modes before downstream retrieval or demand-classifier handoff.
- Done looks like: the review identifies whether Batch 1 enforces the promised structure, row identity, vocab, handoff packet, and board status checks without breaking valid fixtures or weakening existing handoff constraints, with concrete closure conditions for any material finding.

## Method Order

REFERENCE-LOAD these methods first. Do not APPLY them yet:

- `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.86\skills\workflow-deep-thinking\SKILL.md`
- `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.86\skills\workflow-code-review\SKILL.md`

Then SOURCE-LOAD the target files and context-only files listed in preflight. Declare either `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources and material gaps. Only after that declaration, APPLY `workflow-deep-thinking` to frame failure modes, then APPLY `workflow-code-review` for findings-first review.

## Source-Of-Truth Worktree And Diff

Use this existing worktree as source of truth:

```text
C:\Users\vmon7\Desktop\projects\orca\worktrees\csb-validator-batch1
```

Expected state:

```text
branch: codex/csb-validator-batch1
HEAD: 8287a0791e9239939cc3a0b2355916b73953d8da
base: origin/main @ 532f01038668455b774bb70dc05aa633ad5bca0e
PR: https://github.com/eric-foo/orca/pull/360
```

Before reviewing, confirm that `git rev-parse HEAD` and `git rev-parse origin/main` match the expected values above, or return a blocked result naming the mismatch. Inspect:

```powershell
git diff --name-only origin/main..HEAD
git diff origin/main..HEAD -- .agents/hooks/check_commission_signal_board_output.py orca-harness/tests/unit/test_commission_signal_board_output_validator.py orca-harness/tests/fixtures/commission_signal_board_outputs/valid_empty_backtest_output.txt orca-harness/tests/fixtures/commission_signal_board_outputs/valid_source_backed_backtest_output.txt orca-harness/tests/fixtures/commission_signal_board_outputs/valid_source_backed_forward_output.txt orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
```

If the filed prompt itself is present as an uncommitted or later committed change, exclude it from the PR #360 implementation review unless the dispatcher explicitly asks for prompt review too.

## Review Axes To Attack

Focus on material correctness, false-pass, and review-confidence failures:

- Whether the full-board section contract rejects missing, duplicate, out-of-order, or renamed Sections 1-10 without becoming brittle to harmless Markdown formatting.
- Whether Section 4 row parsing correctly enforces `SBR-001` style IDs, monotonic ordering, and controlled vocab/status values without accepting malformed rows or rejecting valid source-backed rows.
- Whether Section 8 handoff packet YAML requirements catch missing, wrongly typed, or non-`classifier_owned` fields and preserve the source-backed-only handoff rule.
- Whether Section 10 board status and run boundary checks prevent fake completion, ambiguous next action, or unsupported readiness claims.
- Whether existing handoff constraints still fire: no `excluded_future_info`, no AEO visibility rows, no non-source-backed handoff rows, and backtest cutoff fields must be in-window/existed-by-cutoff.
- Whether failure codes are specific enough for tests and operator debugging, without masking multiple independent failures behind one broad code.
- Whether valid fixtures are now full-board examples that actually exercise the new parser surface, rather than passing because the checker skips sections.
- Whether negative tests cover the core failure classes, including section contract, row IDs, vocab, Section 8 shape, and Section 10 status/run-boundary values.
- Whether the CSB playbook's validator description matches the implemented checker and does not overclaim CI, artifact-path, prohibited-term linter, evidence-truth, demand judgment, or retrieval readiness.
- Whether Batch 1 accidentally implements deferred Batch 2-4 scope or creates lock-in that makes those batches harder.

## Validation Evidence To Inspect

Dispatcher-observed validation on current HEAD:

```powershell
cd C:\Users\vmon7\Desktop\projects\orca\worktrees\csb-validator-batch1
python -B .agents\hooks\check_commission_signal_board_output.py --selftest
```

Observed result in dispatcher turn: fixture-level PASS lines ending with `SELFTEST OK`.

```powershell
python -m pytest -p no:cacheprovider --no-header --no-summary --basetemp C:\tmp\csb_validator_batch1_pytest_final orca-harness\tests\unit\test_commission_signal_board_output_validator.py -q
```

Observed result in dispatcher turn: `18 passed`.

```powershell
git diff --check origin/main..HEAD
```

Observed result in dispatcher turn: no output.

Treat these as evidence to inspect, not as formal validation claims. If repo execution is available, rerun the commands and report the observed result. If you cannot run them, report `validation_not_run` and review from source.

## Output Contract

Preferred reviewer output is a durable report at:

```text
C:\Users\vmon7\Desktop\projects\orca\worktrees\csb-validator-batch1\docs\review-outputs\csb_validator_batch1_adversarial_code_review_v0.md
```

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
authored_by: operator_to_fill_or_unrecorded
de_correlation_bar: operator_to_fill_or_unrecorded
same_vendor_rationale: not_applicable_unless_same_vendor_sanity_is_claimed
```

Do not fabricate model identity. Do not recommend, prescribe, rank, or imply runtime model choice.

Close with this courier block so the home model can adjudicate later:

```text
CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the read-only adversarial code review result for PR #360. Adjudicate it as findings and evidence, not as approval or patch authority.

Include:
- original commission or review target
- implementation context, diff, and reviewed files
- findings and implementation evidence
- proposed remediation direction, if any, but no patch queue
- citations
- reviewer verdict if explicitly bound; otherwise NOT_CLAIMED
- validation evidence and not-run checks
- residual risk
- blockers, off-scope flags, and not-proven boundaries
```

For this prompt, proposed patch, exact requested edits, formal verdict, severity authority, readiness, approval, validation pass/fail, and patch queue are `NOT_CLAIMED` unless a later owner instruction binds them.
