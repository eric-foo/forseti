# Missing Work Inventory PR Fanout Report Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt (delegated adversarial artifact review commission)
scope: >
  Commission an independent, read-only adversarial artifact review of PR #764's
  missing-work inventory fanout report and its supporting git/GitHub evidence.
use_when:
  - Checking whether PR #764 honestly resolves the missing-work inventory/fanout request.
  - Auditing whether Orca-to-Forseti migration fallout was handled without hiding real missing work.
  - Asking a de-correlated reviewer for compact findings before the CA decides what, if anything, to patch.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/delegated-review-patch.md
stale_if:
  - PR #764 changes head commit after 20471b9277b95d34263f7bea2ade0e5170cf3b08.
  - origin/main advances after f0ce5b14 before review starts.
  - The non-report open PR set changes before review starts.
branch_or_commit: prompt authored on codex/missing-inventory-adversarial-review-prompt @ f0ce5b14; review target PR #764 head codex/missing-work-inventory-execution-v2 @ 20471b9277b95d34263f7bea2ade0e5170cf3b08.
```

## Delegated Review Prompt

You are the independent controller for a read-only adversarial artifact review.
This is a delegated review commission, not a model recommendation. Runtime model
choice is operator/tooling-owned. If you are not from a different vendor/model
lineage than the author/home model recorded below, you may still provide bounded
sanity findings, but you must not claim cross-vendor discovery or no-new-seam
coverage.

```yaml
delegated_review_receipt:
  author_home_model_family: OpenAI-family Codex/GPT execution thread
  controller_model_family: operator_to_fill
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_bar: operator_to_fill  # cross_vendor_discovery | same_vendor_sanity | self_fallback
  de_correlation_status: >
    satisfied only if controller_model_family is a different vendor/model lineage
    from author_home_model_family; otherwise record same_vendor_sanity or self_fallback.
  access_mode: repo
  patch_authority: none
```

## Prompt Preflight

`preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below.`

```yaml
orca_start_preflight:
  agents_read: required on intake
  overlay_read: required on intake
  source_pack: custom (review prompt + target PR/report + review lane + migration policy + live git/GitHub state)
  edit_permission: read-only for source; report-write only to the bound review report path
  target_scope: >
    Review PR #764's missing-work inventory report for correctness, completeness,
    stale claims, false lifecycle claims, migration reconciliation errors, and
    unsafe suppression or duplication of PR fanout.
  dirty_state_checked: required on intake
  blocked_if_missing: AGENTS.md, overlay README, review-lanes, prompt-orchestration, target PR #764, target report file, git metadata, or GitHub PR metadata
output_mode: review-report
template_kind: review
template_source: docs/prompts/templates/review/adversarial_artifact_review_v0.md
authorization_basis: owner current-turn request to delegate an adversarial review prompt after the inventory execution produced many updates
review_prompt_artifact_path: docs/prompts/reviews/missing_work_inventory_pr_fanout_report_adversarial_artifact_review_prompt_v0.md
review_report_path: docs/review-outputs/adversarial-artifact-reviews/missing_work_inventory_pr_fanout_report_adversarial_review_v0.md
target_files_or_dirs:
  - PR #764: https://github.com/eric-foo/forseti/pull/764
  - docs/hygiene/missing_work_inventory_pr_fanout_report_v0.md on codex/missing-work-inventory-execution-v2 @ 20471b9277b95d34263f7bea2ade0e5170cf3b08
  - docs/prompts/handoffs/missing_work_inventory_pr_fanout_handoff_prompt_v0.md
  - docs/decisions/forseti_rename_migration_policy_v0.md
  - docs/migration/*forseti*_migration*/moved_paths_index.md only when needed to test a migration-sensitive finding
branch_or_commit_reference: >
  Review target is PR #764 head codex/missing-work-inventory-execution-v2 @
  20471b9277b95d34263f7bea2ade0e5170cf3b08, based on origin/main f0ce5b14.
dirty_state_allowance: >
  Source review must use the pinned target commit or a fresh PR checkout at the
  same head; unrelated dirty files are out of scope. The review output may be
  written on a separate clean review branch/worktree.
doctrine_change_decision: none authorized; flag doctrine issues but do not patch doctrine
isolation_decision: review-only lane; no source edits outside the review report path
validation_gates:
  - Verify PR #764 metadata and head commit before reviewing.
  - Verify origin/main and the non-report open PR set before relying on the report's freshness claims.
  - Run retrieval/header and map/link checks only if you write the durable review report.
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: new_review_commission
```

## Required Method Sequence

1. `REFERENCE-LOAD` `workflow-deep-thinking`. Do not apply it yet; use it only
   to prepare a neutral failure-mode lens.
2. `REFERENCE-LOAD` `workflow-adversarial-artifact-review`. Do not apply it yet.
3. `SOURCE-LOAD` the required sources below.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
5. Only after source readiness, APPLY `workflow-deep-thinking` to frame the
   boundary problem, failure modes, and decision criteria.
6. Then APPLY `workflow-adversarial-artifact-review` to produce findings.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot
be applied after source readiness, return a blocked or advisory-only result. Do
not emit strict review claims, readiness, validation, mandatory remediation,
patch queues, or executor-ready handoffs.

## Required Sources

Read these before findings:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/review-lanes.md`
4. `.agents/workflow-overlay/prompt-orchestration.md`
5. `.agents/workflow-overlay/source-loading.md`
6. `.agents/workflow-overlay/validation-gates.md`
7. `.agents/workflow-overlay/retrieval-metadata.md`
8. `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
9. `docs/prompts/handoffs/missing_work_inventory_pr_fanout_handoff_prompt_v0.md`
10. `docs/decisions/forseti_rename_migration_policy_v0.md`
11. `docs/hygiene/missing_work_inventory_pr_fanout_report_v0.md` from PR #764 head commit `20471b9277b95d34263f7bea2ade0e5170cf3b08`
12. Fresh git/GitHub observations:
    - `git fetch --prune --all`
    - `git rev-parse --short origin/main`
    - `gh pr view 764 --json number,title,state,isDraft,headRefName,baseRefName,url,commits`
    - `gh pr list --state open --limit 200 --json number,title,state,headRefName,baseRefName,updatedAt,url`

Do not bulk-load every branch diff. Sample branch/ref classifications only when
needed to test a material report claim or a suspected false negative.

## Fitness Reference

Goal: the report should let the CA decide what local work still needs action
after the Orca-to-Forseti migration without creating duplicate, stale, unsafe,
or unclassified PRs.

Observable success signal: a fresh reviewer can trace each major disposition in
PR #764 to observed git/GitHub state, migration policy, or a clearly named
source gap, and can see why zero non-report work PRs were opened without relying
on chat narration.

Attack both the goal and the signal. If you think this is the wrong success bar,
make that a finding.

## Review Questions

Findings should prioritize material failure modes:

- Did PR #764 accurately update for `origin/main` `f0ce5b14`, PR #763 merged state, and zero non-report open PRs at generation time?
- Does the report hide or understate any unit that should have been `ready_for_pr` rather than `needs_owner_decision`, `needs_source_reconciliation`, `unsafe_or_protected`, or already covered by main?
- Did the report correctly treat Orca-to-Forseti rename/path migration fallout as a reconciliation gate rather than a reason to bulk PR stale work?
- Are lifecycle claims about fetch, commit, push, branch, PR, validation, and CI stated only where freshly observed?
- Does the report's root-untracked grouping avoid promoting `_scratch/`, `.tmp*`, `.codex/hooks/**`, or `worktrees/**` while still preserving enough signal for owner action?
- Are unresolved handoff-looking paths properly marked as inventory-only `nonresolving:` observations rather than actionable cold-lane pointers?
- Does the report overfit to the author's noisy execution trail instead of giving the CA a compact, decision-useful inventory?
- Does the report create any false sense of validation, readiness, approval, or source-of-truth promotion?

## Output Contract

Write exactly one durable review report:

`docs/review-outputs/adversarial-artifact-reviews/missing_work_inventory_pr_fanout_report_adversarial_review_v0.md`

The report must include a retrieval header and these body fields near the top:

```yaml
reviewed_by: operator_to_fill_or_unrecorded
authored_by: OpenAI-family Codex/GPT execution thread
de_correlation_bar: operator_to_fill
same_vendor_rationale: required_if_same_vendor_sanity_else_omit
review_target: PR #764 / docs/hygiene/missing_work_inventory_pr_fanout_report_v0.md @ 20471b9277b95d34263f7bea2ade0e5170cf3b08
review_use_boundary: decision_input_only_not_validation_not_approval_not_patch_authority
```

Findings first, ordered by severity: `critical`, `major`, `minor`.

For each finding include:

- severity
- location
- issue
- evidence
- impact
- minimum_closure_condition
- next_authorized_action
- advisory remediation direction

Keep the review compact. Do not produce a process diary. If there are no
critical or major findings, say that plainly and list residual risks or sampling
limits.

Do not include `patch_queue_entry`. Do not edit PR #764, the report, this
prompt, or any source artifact. The only write permitted by this prompt is the
review report above.

After writing the report, return a short chat courier with:

```yaml
review_summary:
  status: completed | blocked | failed
  report_path:
  recommendation:
  critical_count:
  major_count:
  minor_count:
  next_action:
```

Review findings are decision input only. They are not approval, validation,
mandatory remediation, readiness, merge authority, or patch authority until the
CA separately accepts or authorizes a follow-up.
