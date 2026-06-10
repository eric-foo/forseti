# Orca Source Loading Context STEP-04 Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial review prompt for Orca source-loading/context-management STEP-04 overlay and repo-map patches.
use_when:
  - Reviewing whether the STEP-04 patches fixed source-loading and context-management risks without adding authority drift.
  - Checking the source-loading, repo-map, prompt-orchestration, and validation-gate changes before STEP-05 closeout.
authority_boundary: retrieval_only
```

- Status: PROPOSED_PROMPT
- Template kind: adversarial-artifact-review
- Template source: `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
- Output mode: `review-report`
- Required report path: `docs/review-outputs/adversarial-artifact-reviews/orca_source_loading_context_step04_adversarial_review_v0.md`
- Edit permission for reviewer: read-only
- Patch execution authorized: no
- Implementation authorized: no

## Prompt

You are performing a read-only adversarial artifact review for Orca.

Use `workflow-deep-thinking` first. Then use
`workflow-adversarial-artifact-review`.

The deep-thinking step should frame the boundary problem, failure modes, and
decision criteria before findings are listed. It does not widen review scope,
authorize patching, or turn this into Data Capture Spine architecture work.

## Workspace Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus target diffs
  edit_permission: read-only
  target_scope: STEP-04 source-loading/context-management patch files only
  dirty_state_checked: yes
  blocked_if_missing: required source, wrong workspace, missing target files, unbound report path, or disallowed dirty-state substitution
```

- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Expected branch: `main`
- Expected HEAD at prompt creation: `cb3e999a59244c68575f04d1c24904bb296b1590`
- Dirty-state allowance: dirty worktree allowed. Review the named target file
  diffs in place. Broader modified or untracked files are out of scope unless
  they directly affect source hierarchy, source-loading authority,
  prompt-orchestration gates, artifact-role binding, review-lane binding, or
  report-output authority.
- Controlling-source state at prompt creation: modified control-plane sources
  are in scope for advisory review only. Strict readiness, acceptance,
  validation, proof, source-of-truth, `PASS`, or `ADEQUATE_NOW` claims are not
  proven by this review.

If you cannot access the pinned workspace, see the wrong branch or revision, or
cannot inspect the named target diffs, return a blocked review summary instead
of reviewing a substitute checkout.

## Review Target

Review the current working-tree diffs for these files:

- `.agents/workflow-overlay/source-loading.md`
- `docs/workflows/orca_repo_map_v0.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/prompt-orchestration.md`

The patch intent was:

1. Make `.agents/workflow-overlay/source-loading.md` the canonical owner of
   source-loading budgets, source-pack tiers, source-capsule rules, and Data
   Capture Spine CA read-pack limits.
2. Prevent `docs/workflows/orca_repo_map_v0.md` from forking the Data Capture Spine
   read-pack rule while preserving its navigation role.
3. Add prompt/review validation gates for modified or untracked controlling
   sources and source-capsule budget overflow.
4. Align prompt-orchestration preflight and validation gates with those rules.

## Required Reads

Read only these first:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-of-truth.md`
4. `.agents/workflow-overlay/source-loading.md`
5. `docs/workflows/orca_repo_map_v0.md`
6. `.agents/workflow-overlay/prompt-orchestration.md`
7. `.agents/workflow-overlay/validation-gates.md`
8. `.agents/workflow-overlay/review-lanes.md`
9. `.agents/workflow-overlay/artifact-roles.md`
10. `.agents/workflow-overlay/communication-style.md`
11. `.agents/workflow-overlay/template-registry.md`
12. `.agents/workflow-overlay/retrieval-metadata.md`
13. `docs/hygiene/precompact_orca_source_loading_context_step04.md`

Use targeted diff inspection for the four review-target files. Do not bulk-read
product history, Data Capture Spine product anchors, method-validation replays,
proof-run packets, review outputs, research corpus, all prompts, or
`docs/_inbox/` by default.

Useful read-only commands, if available:

```powershell
git status --short --branch -- .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md .agents/workflow-overlay/validation-gates.md .agents/workflow-overlay/prompt-orchestration.md
git diff -- .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md .agents/workflow-overlay/validation-gates.md .agents/workflow-overlay/prompt-orchestration.md
```

## Review Purpose

Adversarially assess whether the STEP-04 patches actually reduce Orca
source-loading/context-management risk before STEP-05 validation and closeout.

Focus on whether the patch:

- keeps source hierarchy separate from source loading;
- keeps the repo map navigational rather than authoritative;
- avoids duplicating or forking the Data Capture Spine CA read-pack rule;
- makes source-capsule budgets operational enough to prevent context blow-up;
- handles modified/untracked controlling sources without creating fake
  readiness, acceptance, validation, or source-of-truth claims;
- aligns prompt-orchestration and validation-gate language without
  contradiction;
- avoids importing `jb` policy, paths, lifecycle mechanics, GAP/CV Engine
  assumptions, or generic workflow-kernel authority as Orca authority;
- avoids Data Capture Spine design, Evidence Candidate Record design, Cleaning Spine
  design, runtime design, implementation planning, or automation design;
- avoids process bloat that adds ceremony without improving source selection,
  authority clarity, failure visibility, or prompt economy.

## Hard Boundaries

Do not:

- edit files;
- create patches or patch queues;
- stage, commit, push, or create pull requests;
- design Data Capture Spine, Evidence Candidate Record fields, Cleaning Spine, runtime
  systems, implementation routes, tests, packages, or automation;
- treat this review as approval, validation, readiness, acceptance,
  source-of-truth promotion, or implementation authorization;
- treat dirty or untracked files as accepted source-of-truth;
- import `jb` project policy or paths.

## Output Mode And Report Contract

Use `review-report`.

Before full review, confirm the durable report path is bound:

`docs/review-outputs/adversarial-artifact-reviews/orca_source_loading_context_step04_adversarial_review_v0.md`

Write the full human-readable review report to that path. The report should
contain:

1. Verdict: `ACCEPT_AS_ADVISORY`, `PATCH_BEFORE_STEP_05`, `REWORK_REQUIRED`,
   or `BLOCKED`.
2. Findings first, ordered by severity: critical, major, minor.
3. For each finding: severity, location, issue, evidence, impact, recommended
   correction.
4. Non-findings and residual risks.
5. Source-read ledger with dirty/untracked status where checked.
6. Not-proven boundaries.
7. Review-use boundary.

After the report is successfully written, return only this compact YAML shape
in chat:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/orca_source_loading_context_step04_adversarial_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  summary: "One sentence describing the review result."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "One concrete next step"
```

If the required report cannot be written after `review-report` is selected, do
not use `report_path`. Return:

```yaml
review_summary:
  status: failed
  review_location: chat_only_current_thread
  recommendation: blocked
  summary: "Failed to write required report to docs/review-outputs/adversarial-artifact-reviews/orca_source_loading_context_step04_adversarial_review_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Resolve the report write failure, then rerun the review-report prompt."
```

Do not add extra YAML keys.

## Review-Use Boundary

This is a read-only adversarial review. Treat findings and non-findings as
decision input only, not as approval, validation, product proof, mandatory
remediation, or executor-ready instructions. Downstream work may use the review
only after a separate authorized Orca decision, patch, validation, or
implementation lane accepts it.
