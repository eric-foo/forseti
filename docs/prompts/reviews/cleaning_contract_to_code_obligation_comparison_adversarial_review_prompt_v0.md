# Cleaning Contract-To-Code Obligation Comparison Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Repo-bound adversarial artifact review prompt for checking whether the Cleaning
  contract-to-code reconciliation checklist correctly maps current Cleaning
  obligations to current orca-harness/cleaning code and focused tests.
use_when:
  - Commissioning a de-correlated adversarial reviewer to compare Cleaning contract obligations against the checklist and current code/tests.
  - Checking whether the checklist overclaims coverage, misses an obligation, or names the wrong next patch before step 2.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/cleaning_contract_to_code_reconciliation_checklist_v0.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
stale_if:
  - docs/workflows/cleaning_contract_to_code_reconciliation_checklist_v0.md changes.
  - orca/product/spines/cleaning/contracts/ changes.
  - orca-harness/cleaning/ or the focused Cleaning tests change.
  - The worktree branch, HEAD, or dirty-state allowance below changes materially.
```

## Prompt Contract

- output_mode: `review-report`
- template_kind: `adversarial-artifact-review`
- template_source: `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
- prompt_artifact_path: `docs/prompts/reviews/cleaning_contract_to_code_obligation_comparison_adversarial_review_prompt_v0.md`
- report_destination: `docs/review-outputs/adversarial-artifact-reviews/cleaning_contract_to_code_obligation_comparison_adversarial_review_v0.md`
- edit_permission: read-only for review targets; docs-write only for the review report destination above
- runtime_model_routing: unbound; operator chooses the reviewer. Do not recommend, rank, or imply a runtime model.
- de_correlation_boundary: this prompt is suitable for a de-correlated reviewer chosen by the operator. It does not itself prove de-correlation or claim a delegated review has run.

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_cleaning_obligation_comparison_review
  repo_map_decision: loaded
  repo_map_reason: prompt target and workflow-record route depend on the repo map entry for the new checklist
  workspace_path: C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\cleaning-spine-continuation
  branch_or_commit_reference: codex/cleaning-spine-continuation @ bc950cdfeeb3a02f33bf52217d71e049aa9093f2
  origin_main_reference_observed: 780091959c778562a19984596b9d45645c8c1edf
  dirty_state_allowance: >
    Allowed dirty state is limited to the current Cleaning checklist work:
    docs/workflows/cleaning_contract_to_code_reconciliation_checklist_v0.md
    (untracked), docs/workflows/orca_repo_map_v0.md (modified route), and this
    prompt artifact if present. If other dirty files appear, classify them before
    review and do not rely on them unless the current operator explicitly adds
    them to scope.
  controlling_source_state: current prompt author observed overlay sources clean enough for prompt authoring; target checklist and repo map are intentionally dirty/uncommitted review inputs
  doctrine_change_decision: no doctrine change intended; review prompt and checklist are retrieval/workflow artifacts only
  isolation_decision: existing worktree branch off origin/main; no source edits by reviewer
  target_files_or_dirs:
    - docs/workflows/cleaning_contract_to_code_reconciliation_checklist_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - orca/product/spines/cleaning/contracts/
    - orca-harness/cleaning/
    - orca-harness/tests/unit/test_cleaning_core.py
    - orca-harness/tests/unit/test_cleaning_projection_integration.py
  validation_gates:
    - read-only review; no tests required by reviewer unless they choose to confirm evidence
    - if writing the durable report, run retrieval-header/report write checks available in the repo and record not-run items honestly
  thread_operating_target_continuity:
    carried_forward: no
    reason: no_visible_active_target
    changed_from_input: no
    lifecycle_status: not_applicable
```

## Objective

You are performing a read-only adversarial artifact review for Orca.

Review target:

- Primary target: `docs/workflows/cleaning_contract_to_code_reconciliation_checklist_v0.md`
- Secondary target for retrievability only: the new route line in `docs/workflows/orca_repo_map_v0.md`

Review purpose:

Determine whether the checklist accurately and completely maps the current
Cleaning Spine obligations to the current bounded implementation and focused
tests, before the home lane uses it to pick the next patch.

Fitness reference:

- Goal: make the next Cleaning patch target real contract-to-code drift, not a false checklist gap or an overclaimed coverage row.
- Done looks like: the review either finds no critical/major defects in the obligation mapping, or names the exact obligation, source, code/test evidence, and checklist row that must be corrected before step 2.

## Required Source Order

First, read these authority and method sources:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-of-truth.md`
4. `.agents/workflow-overlay/source-loading.md`
5. `.agents/workflow-overlay/review-lanes.md`
6. `.agents/workflow-overlay/prompt-orchestration.md`
7. `.agents/workflow-overlay/validation-gates.md`
8. `docs/prompts/templates/review/adversarial_artifact_review_v0.md`

REFERENCE-LOAD these method instructions if available in your environment:

- `workflow-deep-thinking`
- `workflow-adversarial-artifact-review`

Do not APPLY the methods yet. Use them only to prepare a neutral source-reading lens.

Then source-load the task sources:

1. `docs/workflows/cleaning_contract_to_code_reconciliation_checklist_v0.md`
2. `docs/workflows/orca_repo_map_v0.md` targeted to the checklist route line
3. `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md`
4. `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
5. `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
6. `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`
7. `orca/product/spines/cleaning/contracts/core_spine_v0_corroboration_vs_amplification_discipline_v0.md`
8. `docs/migration/phase2_proposals/cleaning_w3a_proposal_v0.md`
9. `orca-harness/cleaning/models.py`
10. `orca-harness/cleaning/core.py`
11. `orca-harness/cleaning/projection.py`
12. `orca-harness/tests/unit/test_cleaning_core.py`
13. `orca-harness/tests/unit/test_cleaning_projection_integration.py`

After source-loading, declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
Only after that declaration, APPLY `workflow-deep-thinking` and then APPLY
`workflow-adversarial-artifact-review` to the loaded source context.

If you do not have repo/filesystem access, stop and request a source capsule.
If a required source is missing, return `SOURCE_CONTEXT_INCOMPLETE` and explain
which claim cannot be reviewed.

## Review Checks

Attack the checklist for these failure modes:

1. Missing obligation: a Cleaning contract obligation exists in the source pack but has no checklist row.
2. False coverage: a checklist row says code or tests cover an obligation when the cited code/test does not actually prove that coverage.
3. Understated gap: a row says mostly/partially covered but the real gap is larger or affects code behavior, not just tests.
4. Overstated gap: the checklist names a candidate gap that is already covered by source, code, or tests.
5. Wrong authority: the checklist relies on the handoff packet, repo map, W3a proposal, or a secondary source where a contract/code source should control.
6. Boundary drift: the checklist lets Cleaning absorb ECR, Judgment, near-match dedupe, copied-language grouping, clustering, source acquisition, persistence, runners, APIs, validation, readiness, or product proof.
7. Code evidence mismatch: cited symbols, validators, tests, or files do not exist or do not behave as described.
8. Retrieval defect: the checklist or repo-map route would be hard for a cold lane to find, stale-check, or use without overclaiming authority.
9. Next-patch quality: the candidate patch queue does not follow from the evidence, is too broad, or misses the smallest complete next patch.

Do not patch files. Do not emit executor-ready `patch_queue_entry`. You may give
advisory remediation direction and exact minimum closure conditions.

## Output Contract

Write the durable review report to:

`docs/review-outputs/adversarial-artifact-reviews/cleaning_contract_to_code_obligation_comparison_adversarial_review_v0.md`

The report must include:

- retrieval header;
- `reviewed_by` and `authored_by` fields, operator/tooling-supplied; use `unrecorded` only if not supplied, never fabricated;
- source-read ledger with `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`;
- findings first, ordered `critical`, `major`, `minor`;
- for each finding: severity, location, issue, evidence, impact, minimum_closure_condition, next_authorized_action, and advisory remediation direction;
- non-findings for rows you checked and found sound;
- residual risks and not-proven boundaries;
- final recommendation using one of: `accept`, `accept_with_friction`, `patch_before_acceptance`, `reject`, `blocked`.

After a successful report write, return only this courier YAML in chat:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/cleaning_contract_to_code_obligation_comparison_adversarial_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  reviewed_by: unrecorded
  authored_by: gpt-5-codex
  summary: "One sentence describing whether the checklist can guide step 2."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "One concrete next step."
```

If the report cannot be written, return the same shape with `status: failed`,
`review_location: chat_only_current_thread`, `recommendation: blocked`, and no
`report_path`; name the write failure in `summary` or `next_action`.

## Review-Use Boundary

This is a read-only adversarial review. Findings are decision input only. They
are not approval, validation, readiness, product proof, mandatory remediation,
patch authority, or permission to keep any change. The home lane must adjudicate
findings before editing the checklist, code, tests, or repo map.
