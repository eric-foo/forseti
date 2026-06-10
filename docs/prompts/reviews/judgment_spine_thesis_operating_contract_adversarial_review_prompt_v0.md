# Judgment Spine Thesis Operating Contract Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial artifact review prompt for the Judgment Spine thesis operating contract and bounded navigation patches.
use_when:
  - Asking a reviewer to adversarially inspect the thesis operating contract before owner acceptance or further thesis-lane work.
  - Checking whether the contract preserves the Judgment Spine thesis goal, source authority, non-claims, and layer boundaries.
  - Checking whether the thesis, README, and manifest navigation patches are narrow and non-authorizing.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - .agents/workflow-overlay/review-lanes.md
```

- Status: PROPOSED_PROMPT
- Artifact type: Adversarial artifact review prompt
- Template kind: `adversarial-artifact-review`
- Template source: `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
- Prompt artifact path: `docs/prompts/reviews/judgment_spine_thesis_operating_contract_adversarial_review_prompt_v0.md`
- Required review report path: `docs/review-outputs/adversarial-artifact-reviews/judgment_spine_thesis_operating_contract_adversarial_review_v0.md`
- Output mode: `review-report`
- Reviewer edit permission: read-only, except writing the required review report
- Patch queue authorized: no
- Implementation, runtime, package, test, automation, commit, push, or PR authorized: no

## Prompt Author Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus adversarial review prompt template and Judgment Spine review targets
  edit_permission: docs-write
  target_scope: Create a read-only adversarial artifact review prompt for the Judgment Spine thesis operating contract and bounded navigation patches.
  dirty_state_checked: yes
  blocked_if_missing: no
control_plane_source_state:
  branch: main
  head: b7627d3
  overlay_sources_modified_or_untracked: yes
  reviewed_targets_untracked: yes
  strict_pass_or_readiness_claimed: no
```

## Prompt

You are performing a read-only adversarial artifact review for Orca.

Your target is the Judgment Spine thesis operating contract and its bounded navigation/thesis patches. This is an artifact review lane, not a patch lane, not a Judgment Harness implementation lane, not a broad architecture-planning lane, and not a product-proof lane.

## Workspace

- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Expected branch: `main`
- Expected HEAD observed by prompt author: `b7627d3`
- Dirty-state allowance: dirty and untracked Orca docs may exist. The reviewed Judgment Spine files may be untracked. Treat dirty or untracked sources as working artifacts unless an accepted Orca source makes them controlling authority.
- Prompt artifact path: `docs/prompts/reviews/judgment_spine_thesis_operating_contract_adversarial_review_prompt_v0.md`
- Output mode: `review-report`
- Required durable report path: `docs/review-outputs/adversarial-artifact-reviews/judgment_spine_thesis_operating_contract_adversarial_review_v0.md`
- Chat closeout after successful report write: compact `review_summary` YAML from `.agents/workflow-overlay/communication-style.md`

## Review Target

Primary target:

- `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md`

Bounded patch targets:

- `docs/research/judgment-spine/judgment_spine_thesis_v0.md`
- `docs/research/judgment-spine/README.md`
- `docs/research/judgment-spine/manifest_v0.md`

Prompt source that authorized the target work:

- `docs/prompts/deep-thinking/judgment_spine_thesis_operating_contract_ca_prompt_v0.md`

Prompt-author observed SHA256 values:

```yaml
input_hashes:
  docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md: 6DBFFE3ABD281193A54EA4781AF6D4E75FB0D646575C98987B7B1B6C327E7442
  docs/research/judgment-spine/judgment_spine_thesis_v0.md: 8F198443BA99B292B8F9C4F370E4CB441C9DFE4418023DBE358286DA26C31DED
  docs/research/judgment-spine/README.md: 3584FDEF4C672D78DFBF14BBDA9D06DAAD7FF3C7382F31E929E184E2960454DD
  docs/research/judgment-spine/manifest_v0.md: 15F91CB0C0FDE9E87462CE328C70E1F5C3403EFCD449C0D2DD22CFC6A1F25D17
```

If hashes differ, do not fail automatically. Record the mismatch in the report and decide whether the changed file is still reviewable under the dirty-state allowance. Block only if the mismatch prevents a source-backed review of the commissioned target.

## Review Purpose

Adversarially review whether the operating contract and bounded patches:

1. Satisfy the CA prompt's goal of turning the Judgment Spine thesis into a practical operating contract for future lanes.
2. Preserve the parent Judgment Spine thesis without becoming broad architecture planning or harness implementation.
3. Correctly distinguish parent Judgment Spine, v0.14 Judgment Harness, case-learning artifacts, failure logs, promoted lessons, Data Capture, Evidence Candidate Record, Cleaning, and implementation authorization.
4. Preserve non-claims around validation, readiness, product proof, buyer proof, superiority, implementation, runtime, automation, tests, commits, pushes, and PRs.
5. Avoid creating new authority, source-of-truth promotion, approval, readiness, validation, or mandatory remediation claims.
6. Keep the navigation/thesis patches narrow and discoverability-oriented.
7. Keep the artifact compact enough to open before future Judgment Spine work without becoming a second architecture manual.

## Goal Context To Check

Use this goal context only as review orientation. It is not source authority, validation evidence, readiness, approval, sequencing authority, or edit permission.

```yaml
goal_handoff:
  long_term_goal: Develop Judgment Spine into Orca's durable judgment-improvement layer for right-sized action under bounded approved evidence.
  anchor_goal: Define a Thesis Operating Contract for how future lanes should consume, protect, and apply the Judgment Spine thesis.
  success_signal: Future agents can use the thesis to judge fit, prevent drift, and preserve non-claims without re-litigating the long-term goal.
  status: inferred_thread_local
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: goal_handoff.anchor_goal
  output_fit_check: goal_handoff.success_signal
  target_delta_from_prior:
    status: changed
    changed_fields: [anchor_goal]
    summary: Shifted from general Judgment Spine CA setup to a thesis-specific lane goal.
  drift_guard: Do not let the thesis lane become harness implementation planning or broad Judgment Spine architecture work.
  conflict_behavior: call_out_conflict_before_proceeding
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
  if_changed_reason: none
```

Before producing findings, state in working notes whether the reviewed artifacts still fit the `anchor_goal` and `success_signal`. If they do not, report a blocking finding.

## Required Source Hierarchy

Use this source hierarchy:

1. Current user instruction for the review run.
2. Orca `AGENTS.md`.
3. `.agents/workflow-overlay/`.
4. Orca docs under `docs/`, when they do not conflict with the overlay.
5. Reusable `agent-workflow` skills as mechanics only.

Do not import `jb` rules, paths, handoffs, lifecycle mechanics, product policy, validation habits, or templates as Orca authority.

## Method Sequencing

REFERENCE-LOAD `workflow-deep-thinking`. Do not APPLY it yet.

REFERENCE-LOAD `workflow-adversarial-artifact-review`. Do not APPLY it yet.

Then source-load the required Orca files below. Only after the required source context is loaded, declare either:

```yaml
source_context_status: SOURCE_CONTEXT_READY
```

or:

```yaml
source_context_status: SOURCE_CONTEXT_INCOMPLETE
missing_sources:
source_gaps:
why_it_matters:
```

Only after `SOURCE_CONTEXT_READY`, APPLY `workflow-deep-thinking` to frame the boundary problem, failure modes, and decision criteria, then APPLY `workflow-adversarial-artifact-review` to produce findings.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot be applied after `SOURCE_CONTEXT_READY`, return a blocked or advisory-only result. Do not emit formal verdicts, severity authority, blocked/ready status, validation claims, readiness claims, mandatory remediation, patch queues, executor-ready handoffs, or alignment-complete claims.

## Required Reads

Read these first:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-of-truth.md`
4. `.agents/workflow-overlay/source-loading.md`
5. `.agents/workflow-overlay/artifact-roles.md`
6. `.agents/workflow-overlay/review-lanes.md`
7. `.agents/workflow-overlay/prompt-orchestration.md`
8. `.agents/workflow-overlay/communication-style.md`
9. `.agents/workflow-overlay/validation-gates.md`
10. `.agents/workflow-overlay/retrieval-metadata.md`
11. `.agents/workflow-overlay/template-registry.md`
12. `docs/prompts/deep-thinking/judgment_spine_thesis_operating_contract_ca_prompt_v0.md`
13. `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md`
14. `docs/research/judgment-spine/judgment_spine_thesis_v0.md`
15. `docs/research/judgment-spine/README.md`
16. `docs/research/judgment-spine/manifest_v0.md`
17. `docs/research/judgment-spine/harness/v0_14/index.md`
18. `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`

Optional targeted reads, only if they can materially change a finding:

- `docs/research/judgment-spine/harness/v0_14/judgement_spine_thesis.md`
- `docs/product/core_spine_v0_information_production_foundation_v0.md`
- `docs/research/judgment-spine/harness/adjacent-context/README.md`

Do not bulk-read all prompts, all cases, all review outputs, method-validation replays, proof-run packets, `docs/_inbox/`, or the full v0.14 harness docset by default. If one of those appears necessary, state the exact source gap first and keep the read targeted.

## Review Scope

In scope:

- correctness of the operating contract against its CA prompt;
- source-support and internal consistency;
- parent Judgment Spine versus v0.14 harness separation;
- Data Capture / ECR / Cleaning / Judgment layer-boundary handling;
- non-claims and strict-claim hygiene;
- reviewability and future-lane usability;
- narrowness of thesis, README, and manifest patches;
- retrieval-header and durable artifact hygiene.

Out of scope:

- implementing the Judgment Harness;
- broad Judgment Spine architecture planning;
- deciding a new target architecture;
- product proof, buyer proof, or commercial positioning;
- source collection, scraping, runtime design, schemas, packages, tests, automation, deployment, commits, pushes, or PRs;
- patch execution or executor-ready patch queues.

## Findings Contract

List findings first, ordered by priority. Use `critical`, `major`, and `minor` only as finding-priority labels. They are not approval, rejection, readiness, validation, or mandatory-remediation authority.

For each finding include:

- finding id;
- priority: `critical`, `major`, or `minor`;
- phase: `correctness` or `friction`;
- location;
- issue;
- evidence;
- impact;
- minimum_closure_condition;
- next_authorized_action;
- recommended correction or advisory remediation direction.

Do not include `patch_queue_entry`. Patch queues are not authorized.

If no issues are found, say so and list residual risks or strict claims that remain not proven.

Optional hardening may be listed only when clearly labeled optional and non-required.

## Report Output

Write the full review report to:

```text
docs/review-outputs/adversarial-artifact-reviews/judgment_spine_thesis_operating_contract_adversarial_review_v0.md
```

The report must include:

1. Review target and purpose.
2. Source context status.
3. Deep-thinking and adversarial-review invocation status.
4. Source-read ledger, including dirty/untracked caveats.
5. Findings-first review output.
6. Non-findings or residual risks.
7. Strict-only blockers and not-proven boundaries.
8. Review-use boundary.
9. Next authorized step.

After successfully writing the report, return only a compact chat summary using this YAML shape:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/judgment_spine_thesis_operating_contract_adversarial_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  summary: "One sentence describing the review result."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "One concrete next step"
```

If the required report cannot be written, do not use `report_path`. Return:

```yaml
review_summary:
  status: failed
  review_location: chat_only_current_thread
  recommendation: blocked
  summary: "Failed to write required report to docs/review-outputs/adversarial-artifact-reviews/judgment_spine_thesis_operating_contract_adversarial_review_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Resolve the report write failure, then rerun the review-report prompt."
```

## Review-Use Boundary

This is a read-only review. Findings and non-findings are decision input only. They are not approval, validation, product proof, mandatory remediation, source-of-truth promotion, implementation authorization, or executor-ready instructions unless a separate authorized Orca decision, patch, validation, or implementation lane accepts them.
