# Fragrantica Projection Adapter Adversarial Implementation Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact
scope: >
  Read-only adversarial implementation/code review prompt for the Fragrantica
  current-window projection adapter change on branch
  codex/fragrantica-projection-adapter-clean.
use_when:
  - Commissioning an independent reviewer to inspect the Fragrantica projection adapter diff.
  - Checking whether the implementation preserves capture/projection/data-lake boundaries without overclaiming review archive completeness.
  - Routing the prior delegated-review-patch request to a code-review prompt because the target is a multi-file implementation diff.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md
  - orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md
branch_or_commit: codex/fragrantica-projection-adapter-clean @ 1c203173788bbbe0628e2c77c1cc3c97baf82bf5
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus Fragrantica projection target sources
  edit_permission: read-only for the receiving reviewer; docs-write was used only to file this prompt
  target_scope: current branch diff for the Fragrantica current-window projection adapter
  dirty_state_checked: yes, local worktree reported clean on branch `codex/fragrantica-projection-adapter-clean`
  blocked_if_missing: source-of-truth worktree, expected revision, target files, or output destination

Prompt contract:
- output_mode: `review-report`
- prompt_delivery: filed prompt under `docs/prompts/reviews/`; paste-ready-chat may carry a copy of this filed body.
- template_kind: `review`
- template_source: `workflow-prompt-orchestrator` bundled `review.md` template adapted to Orca overlay. Orca template registry was checked; no project-local repo-code-review template is bound.
- authorization_basis: current user invoked `workflow-delegated-review-patch`; Orca delegated-review-patch overlay routes multi-file implementation/code diffs to the appropriate review prompt instead of stretching the provisional single-artifact patch convention.
- objective: inspect the Fragrantica projection adapter diff for correctness, boundary discipline, false success paths, missing tests, and data-lake/projection contract violations.
- intended_decision: whether the Fragrantica projection adapter PR needs changes before CA adjudication or merge consideration.
- target_files_or_dirs:
  - `docs/workflows/orca_repo_map_v0.md`
  - `orca-harness/runners/run_fragrantica_projection.py`
  - `orca-harness/source_capture/__init__.py`
  - `orca-harness/source_capture/fragrantica_projection.py`
  - `orca-harness/tests/test_fragrantica_projection_lake_pilot.py`
  - `orca-harness/tests/unit/test_fragrantica_cleaning_projection_integration.py`
  - `orca-harness/tests/unit/test_fragrantica_projection.py`
- branch_or_commit_reference: `codex/fragrantica-projection-adapter-clean` at `1c203173788bbbe0628e2c77c1cc3c97baf82bf5`; compare against `origin/main`.
- dirty_state_allowance: no local source edits allowed before review; if the worktree is dirty, report `BLOCKED_DIRTY_STATE` unless the dirty files are this review report only.
- controlling_source_state: prompt-authoring sources were read in the commissioning lane; receiver must fresh-read in its own lane before findings.
- doctrine_change_decision: this review prompt changes no doctrine; no direction-change propagation receipt is claimed.
- isolation_decision: neither new implementation branch nor patch work; this is read-only review of the existing implementation branch.
- validation_gates: review must be findings-first; no approval, readiness, validation, mandatory remediation, or patch authority is created by the report.
- thread_operating_target_continuity: no visible active `thread_operating_target` block was present; the Fragrantica projection lane context is carried through the objective and target files instead.

## Source-Of-Truth Worktree

Use this source directly:

```text
C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrance-native-live-probe
```

Expected git state before review:

```text
branch: codex/fragrantica-projection-adapter-clean
head: 1c203173788bbbe0628e2c77c1cc3c97baf82bf5
base: origin/main
dirty allowance: clean source tree
changed files vs origin/main:
- docs/workflows/orca_repo_map_v0.md
- orca-harness/runners/run_fragrantica_projection.py
- orca-harness/source_capture/__init__.py
- orca-harness/source_capture/fragrantica_projection.py
- orca-harness/tests/test_fragrantica_projection_lake_pilot.py
- orca-harness/tests/unit/test_fragrantica_cleaning_projection_integration.py
- orca-harness/tests/unit/test_fragrantica_projection.py
```

If the path is unavailable, the branch/head differs, or disallowed dirty source files are present, return a blocked result instead of reviewing a substitute checkout, pasted summary, alternate branch, or recreated source pack.

## Required Reads

REFERENCE-LOAD these method/operating sources first. Do not APPLY review methods yet:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `workflow-deep-thinking` skill instructions, if available in the receiving runtime
- `workflow-code-review` skill instructions, if available in the receiving runtime

Then SOURCE-LOAD the task sources:

- `docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md`
- `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md`
- `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- existing adjacent projection implementations as needed:
  - `orca-harness/source_capture/reddit_projection.py`
  - `orca-harness/source_capture/ig_projection.py`
  - `orca-harness/source_capture/retail_pdp_projection.py`
  - `orca-harness/data_lake/root.py`
- the seven changed files listed in the preflight.

Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with material gaps before producing findings. After source readiness, APPLY `workflow-deep-thinking` to frame likely failure modes, then APPLY `workflow-code-review` to produce findings. If either skill is unavailable, name the unavailable skill and continue only as advisory code review; do not claim a strict delegated review ran.

## Review Commission

Run a read-only adversarial implementation/code review of the Fragrantica current-window projection adapter. Do not edit files. Do not produce a patch queue. Do not treat this as a valid `workflow-delegated-review-patch` execution, because the target is a multi-file implementation diff, not a single high-stakes authored artifact with a bounded patch scope.

Review the implementation against these decision criteria:

- Fragrantica remains `fragrance_native_database`, not `retail_pdp`.
- Projection stays a mechanical view over committed raw capture, not Cleaning, ECR, Judgment, product proof, demand proof, or readiness.
- Direct HTTP review cards are treated as a current-window substrate only. The adapter must not claim full review archive capture.
- Residuals and loss ledger entries must make missing or gated surfaces explicit: archive expansion, login-gated reviews, non-rendered performance components, linked media, attached photos, and absent search-review rows.
- Data-lake writes must use the verified raw packet load path and append-only derived record semantics.
- Re-derive should create sibling derived records; fixed record-id reuse should fail closed.
- Source-family/source-surface guards should reject the wrong packet type instead of creating plausible but invalid projection output.
- Projection rows and bindings should preserve enough raw anchors for downstream Cleaning handles without claiming cleaned or normalized meaning.
- Runner behavior should be local/no-network projection only.
- Tests should cover parser shape, wrong-source rejection, lake append behavior, re-derive behavior, runner behavior, and Cleaning-handle integration.
- Repo-map update should be limited to navigation for the new helper and runner.

Validation evidence available to inspect:

```text
Prior author closeout reported these commands as passing:
- focused Fragrantica projection tests: 9 passed
- broader adjacent projection/Cleaning/lake suite: 46 passed
- clean branch rerun: 46 passed

Treat those as author-supplied evidence to verify or challenge, not as proof.
If rerunning locally, prefer a no-network command such as:
python -m pytest -p no:cacheprovider --no-header --no-summary --basetemp pytest_projection_review_tmp `
  tests/unit/test_fragrantica_projection.py `
  tests/unit/test_fragrantica_cleaning_projection_integration.py `
  tests/test_fragrantica_projection_lake_pilot.py `
  tests/unit/test_cleaning_projection_integration.py `
  tests/unit/test_reddit_projection.py `
  tests/unit/test_retail_pdp_projection.py `
  tests/unit/test_source_capture_ig_projection.py `
  tests/test_ig_projection_lake_pilot.py
```

If validation is not run, report `validation_not_run` with the reason. Do not infer validation from the existence of tests.

## Output Binding

Write the durable review report here:

```text
docs/review-outputs/fragrantica_projection_adapter_adversarial_implementation_review_v0.md
```

The report must include:

- `reviewed_by`: operator/tooling-supplied model+version, or `unrecorded`.
- `authored_by`: operator/tooling-supplied model+version for the implementation author, or `unrecorded`.
- `de_correlation_bar`: `cross_vendor_discovery`, `same_vendor_sanity`, `self_fallback`, or `unrecorded`.
- `same_vendor_rationale`: required when `de_correlation_bar` is `same_vendor_sanity`.
- source context status: `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
- validation status: command(s) run and observed result, or `validation_not_run`.
- findings first, ordered by materiality, each with file/line references where possible.
- for each actionable finding: `minimum_closure_condition` and `next_authorized_action`.
- open questions and residual risk.
- review-use boundary: findings are decision input only, not approval, validation, readiness, mandatory remediation, or patch authority.

After successfully writing the report, return only a compact human summary and this courier YAML:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/fragrantica_projection_adapter_adversarial_implementation_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  reviewed_by: unrecorded
  authored_by: unrecorded
  de_correlation_bar: unrecorded
  summary: "<one sentence>"
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "<one concrete next step>"
```

If the report cannot be written, return `status: failed`, `review_location: chat_only_current_thread`, `recommendation: blocked`, and explain the write failure. Do not claim chat is equivalent to the missing durable report.

## Non-Claims

- This prompt does not run the review.
- This prompt does not authorize patch execution.
- This prompt does not claim the delegated-review-patch provisional convention ran.
- This prompt does not recommend, rank, or prescribe a runtime model.
- This prompt does not claim validation, readiness, approval, merge safety, product proof, demand proof, ECR completion, Cleaning completion, or Judgment readiness.
