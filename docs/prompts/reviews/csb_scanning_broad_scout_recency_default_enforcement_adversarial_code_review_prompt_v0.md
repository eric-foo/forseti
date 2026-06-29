# CSB Scanning Broad-Scout Recency Default Enforcement Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed route-out prompt for adversarial mixed code/docs review of the CSB
  recency/current-state row-shape enforcement patch that supports scanning's
  default broad-scout and recency-attention doctrine.
use_when:
  - Commissioning an independent review of the CSB validator enforcement patch.
  - Checking whether the prompt pinned the correct implementation scope and output contract.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/validation-gates.md
  - .agents/workflow-overlay/source-loading.md
implementation_under_review: 28d896c79100db1159c5b0cdf9d897e4734397f0
prompt_carrier_note: >
  This prompt may be committed after the implementation commit. The implementation
  target under review is commit 28d896c79100db1159c5b0cdf9d897e4734397f0; prompt-only
  carrier commits do not change the implementation target unless they modify the
  named target files.
stale_if:
  - Any named implementation target file changes after 28d896c79100db1159c5b0cdf9d897e4734397f0 and before review.
  - The review-output destination already exists and the operator has not authorized a new version.
  - The receiving actor claims cross_vendor_discovery without a different vendor/model-lineage from the author/home family.
```

## Orca Prompt Preflight

- Output mode: file-write review prompt; receiver output mode is `review-report` to `docs/review-outputs/csb_scanning_broad_scout_recency_default_enforcement_adversarial_code_review_v0.md`.
- Template kind: review. Orca-local `repo-code-review` template is unbound; this prompt uses the generic prompt-orchestrator review frame plus Orca overlay bindings.
- Edit permission, targets, branch: reviewer is read-only. Target worktree is `C:\Users\vmon7\Desktop\projects\orca\worktrees\scanning-broad-scout-recency-default`, branch `codex/scanning-broad-scout-recency-default`, implementation commit `28d896c79100db1159c5b0cdf9d897e4734397f0`. Dirty state is allowed only for this prompt artifact or later prompt-carrier commits that do not touch target files.
- Reviews: findings-first. This is advisory mixed implementation/code plus artifact/doctrine review unless a later Orca binding grants formal implementation-review authority. Do not emit formal PASS, readiness, mandatory remediation, or patch queue.
- Doctrine change: none intended by this prompt. It routes review of an already-authored CSB enforcement patch; it does not alter CSB, scanning, Capture, Judgment, review, prompt, validation, or output doctrine.
- Destinations: this prompt is the input artifact; the receiver writes the full report to `docs/review-outputs/csb_scanning_broad_scout_recency_default_enforcement_adversarial_code_review_v0.md`.
- Fitness reference: make the mechanical CSB checker carry stable row-shape obligations so future agents do not have to remember them, while preserving the attention-only boundary. Done looks like: required Section 4 fields and enum values are mechanically rejected when absent or invalid, docs accurately state checker-pass semantics, and no recency/currentness wording leaks into proof, scoring, graph weight, Capture route binding, or demand classification.
- Thread operating target continuity: no active thread-local `thread_operating_target` was visible when this prompt was filed; no target carried forward.

## Commission

Run an adversarial mixed code/docs review of the CSB recency row-shape enforcement patch at commit `28d896c79100db1159c5b0cdf9d897e4734397f0`.

This prompt was produced from a `workflow-delegated-review-patch` route-out, but the target is a multi-file implementation/code plus doctrine-doc change packet. Per Orca `.agents/workflow-overlay/delegated-review-patch.md`, do not force this into the single-artifact delegated review-and-patch convention. Route it through read-only mixed review: `workflow-code-review` for checker/tests/fixtures and `workflow-adversarial-artifact-review` for the CSB/scanning/Capture/Judgment doctrine-language surfaces. The reviewer must not patch source files.

Review purpose:

1. Attack whether the checker actually removes LLM memory burden for the mechanical CSB obligations it claims to enforce.
2. Attack whether the patch overclaims: checker pass must mean row-shape and enum compliance only, never evidence truth, demand proof, classifier correctness, graph weight, Capture route binding, or readiness.
3. Attack whether docs, tests, fixtures, and stale-language sweeps are complete enough to keep scanning's default broad-scout and recency-attention doctrine aligned with CSB output shape.

## Actor And De-Correlation Receipt

- author_home_model_family: OpenAI / GPT-family Codex, recorded from the authoring lane.
- controller_model_family: `operator_to_fill`; to claim `cross_vendor_discovery`, the receiving reviewer must be a different vendor/model-lineage from OpenAI / GPT-family.
- current_receiving_actor_role: controller.
- dispatch_mode: external-controller-courier.
- de_correlation_status: set `cross_vendor_discovery` only if the reviewer is genuinely different-vendor/model-lineage from the author/home family; otherwise set `same_vendor_sanity` or `self_fallback` and do not claim no-new-seam.
- no runtime model recommendation is made by this prompt.

## Source-Gated Method Contract

1. REFERENCE-LOAD `workflow-deep-thinking`, `workflow-code-review`, and `workflow-adversarial-artifact-review` if available in your environment. Do not APPLY them yet.
2. Read the required Orca authority and target sources below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, conflicts, unavailable tools, and any target-file drift.
4. Only after source readiness, APPLY deep-thinking to frame material failure modes.
5. APPLY `workflow-code-review` to checker, tests, and fixture changes.
6. APPLY `workflow-adversarial-artifact-review` to prompt/playbook/adjudication and cross-spine doctrine-language claims.
7. If either review skill is unavailable, mark that slice advisory-only or blocked. Do not silently emulate strict review authority.

## Required Reads

Read these authority and boundary files first:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/safety-rules.md`
- `docs/decisions/overlay_enforcement_placement_classification_v0.md`

Then read the review target:

- `.agents/hooks/check_commission_signal_board_output.py`
- `orca-harness/tests/unit/test_commission_signal_board_output_validator.py`
- `orca-harness/tests/fixtures/commission_signal_board_outputs/`
- `orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_structure_v0.md`
- `orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md`
- `orca/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_structure_rules_v0.md`

Read adjacent doctrine surfaces needed for leakage checks:

- `orca/product/spines/scanning/README.md`
- `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`
- `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
- `orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md`
- `docs/workflows/orca_repo_map_v0.md`

## Target Diff And Dirty-State Allowance

Implementation target commit:

```text
28d896c79100db1159c5b0cdf9d897e4734397f0 enforce CSB recency row shape
```

Observed target files in the implementation commit:

```text
M .agents/hooks/check_commission_signal_board_output.py
M orca-harness/tests/fixtures/commission_signal_board_outputs/bad_aeo_future_info_in_handoff_output.txt
M orca-harness/tests/fixtures/commission_signal_board_outputs/bad_forward_excluded_future_info_handoff_output.txt
M orca-harness/tests/fixtures/commission_signal_board_outputs/bad_missing_handoff_mode_backtest_output.txt
M orca-harness/tests/fixtures/commission_signal_board_outputs/bad_mixed_case_aeo_handoff_output.txt
M orca-harness/tests/fixtures/commission_signal_board_outputs/bad_surface_cutoff_uncertain_handoff_output.txt
M orca-harness/tests/fixtures/commission_signal_board_outputs/bad_to_retrieve_in_handoff_output.txt
M orca-harness/tests/fixtures/commission_signal_board_outputs/bad_uncertain_cutoff_in_handoff_output.txt
M orca-harness/tests/fixtures/commission_signal_board_outputs/valid_empty_backtest_output.txt
M orca-harness/tests/fixtures/commission_signal_board_outputs/valid_source_backed_backtest_output.txt
M orca-harness/tests/fixtures/commission_signal_board_outputs/valid_source_backed_forward_output.txt
M orca-harness/tests/unit/test_commission_signal_board_output_validator.py
M orca/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_structure_rules_v0.md
M orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_structure_v0.md
M orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
```

Use this diff as the implementation under review:

```powershell
git show --stat --patch --no-renames 28d896c79100db1159c5b0cdf9d897e4734397f0 -- .agents/hooks/check_commission_signal_board_output.py orca-harness/tests/unit/test_commission_signal_board_output_validator.py orca-harness/tests/fixtures/commission_signal_board_outputs orca/product/spines/commission_signal_board
```

If the branch contains later prompt-only carrier commits, verify whether the target files above still match `28d896c79100db1159c5b0cdf9d897e4734397f0`. If they changed, report `SOURCE_CONTEXT_INCOMPLETE` or review the newer target only if the operator explicitly authorizes that retarget.

## Validation Evidence To Inspect

The prompt author observed this focused checker selftest after the implementation commit:

```powershell
python -B .agents\hooks\check_commission_signal_board_output.py --selftest
```

Observed terminal tail:

```text
PASS valid_empty_backtest_output.txt
PASS valid_source_backed_backtest_output.txt
PASS valid_source_backed_forward_output.txt
SELFTEST OK
```

The prompt author also observed this unit suite from `orca-harness`:

```powershell
python -B -m pytest -q -p no:cacheprovider tests\unit\test_commission_signal_board_output_validator.py
```

Observed output:

```text
..............                                                           [100%]
```

If you independently rerun validation, use `python -B` and report exact command, cwd, exit code, and observed output. If you do not rerun validation, report validation as author-supplied and not independently revalidated.

Do not run live scanning, CSB commissions, capture, crawling, monitoring, source access, Capture route binding, Judgment scoring, demand classification, buyer-proof checks, or client-facing output.

## Review Scope

Attack these questions:

- Does the validator actually require the intended Section 4 columns: `row_id`, `source_family`, `signal_role`, `row_purpose`, `recency_status`, `recency_attention`, `graph_role`, `graph_weight_hint`, `evidence_status`, `surface_cutoff_status`, and `cutoff_status`?
- Does enum validation cover every mechanically claimed field: `row_purpose`, `recency_status`, `recency_attention`, `graph_role`, and `graph_weight_hint`?
- Are there untested enum fields or table-shape variants that could let invalid board outputs pass while docs imply they fail?
- Does the checker normalize values deliberately, or does normalization accidentally accept materially different values that should fail?
- Does the checker preserve the existing handoff-row protections: source-backed only, no excluded future information, no AEO visibility rows, valid cutoff for backtests, and known row IDs only?
- Does malformed-row handling preserve failure visibility while still validating referenced rows?
- Do fixture edits update all valid and invalid fixtures without making old negative fixtures pass for the wrong reason?
- Do tests prove missing recency columns and invalid recency values fail? If only recency values are tested, is the lack of targeted tests for `row_purpose`, `graph_role`, and `graph_weight_hint` acceptable or a material gap?
- Do prompt/playbook/adjudication docs accurately state that the checker is manual/local, not CI, pre-commit, write-hook, or universal enforcement?
- Do docs accurately state a checker pass means row-shape and enum compliance only, not evidence truth, demand classification, attention correctness, graph correctness, buyer proof, validation, readiness, or client-facing approval?
- Is the DCP complete enough for the doctrine touched here: CSB output shape, scanning broad-scout/recency attention, Capture preservation urgency, and Judgment read attention?
- Did any stale optional-recency language remain live outside receipt search strings?
- Did any recency/currentness language leak into proof, gate proof, numeric scoring, evidence weighting, classifier mapping, graph weight, Capture route binding, access authorization, or source-access permission?
- Did the implementation stay within the accepted enforcement-placement boundary: mechanically checkable shape in code, semantic truth and attention-quality judgment in doctrine/review?
- Did the patch avoid creating false confidence by making code enforcement look like it validates signal quality?

## Intended Enforcement Closure Check

Treat these enforcement goals as claims to verify, not accepted truth:

- E-01 row-shape burden reduction: future CSB full-board outputs must carry the required Section 4 recency/current-state and graph-light fields before mechanical handoff-safety can be claimed.
- E-02 enum burden reduction: invalid mechanical vocabulary for required Section 4 row-shape fields must fail deterministically.
- E-03 non-proof boundary: checker-pass language must remain strictly shape-only, with recency/currentness kept as attention/preservation/read relevance, not proof or scoring.
- E-04 scope boundary: the validator remains a manual/local checker, not CI, pre-commit, source retrieval, classifier, graph builder, Capture router, or Judgment scorer.

For each, report one of:

- `closed`: implementation and tests/docs now cover the failure mode.
- `partially_closed`: some protection exists but a material variant remains.
- `not_closed`: the original failure mode remains.
- `not_assessed`: source or environment prevented assessment.

If `partially_closed` or `not_closed`, include evidence and a minimum closure condition.

## Output Contract

Write the full review report to:

`docs/review-outputs/csb_scanning_broad_scout_recency_default_enforcement_adversarial_code_review_v0.md`

The durable report must include:

1. `reviewed_by` and `authored_by` fields; use `unrecorded` only if the operator did not supply the value.
2. `de_correlation_bar`: `cross_vendor_discovery`, `same_vendor_sanity`, or `self_fallback`, plus `same_vendor_rationale` when applicable.
3. `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
4. Findings first, ordered by severity: `critical`, `major`, then `minor`. Severity is finding priority only, not approval or mandatory remediation authority.
5. For each finding: affected file/line, evidence, impact, minimum closure condition, next authorized action, and advisory remediation direction.
6. Closure assessment for E-01 through E-04.
7. Validation commands rerun and observed output, or not-run reason.
8. Residual risk.
9. Review-use boundary.

After the report is written, return only the compact `review_summary` YAML in chat:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/csb_scanning_broad_scout_recency_default_enforcement_adversarial_code_review_v0.md
  recommendation: <accept | accept_with_friction | needs_patch | needs_architecture_pass | blocked>
  reviewed_by: <operator_supplied_or_unrecorded>
  authored_by: openai-gpt-5-codex
  summary: "<one compact paragraph>"
  findings_count: <integer>
  blocking_findings: []
  advisory_findings: []
  next_action: "<one sentence>"
```

Review-use boundary: this is a read-only review. Findings and non-findings are decision input only, not approval, validation, mandatory remediation, executor-ready patch authority, product proof, or readiness.
