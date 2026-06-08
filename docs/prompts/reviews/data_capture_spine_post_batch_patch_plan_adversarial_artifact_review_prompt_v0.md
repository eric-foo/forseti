# Data Capture Spine Post-Batch Patch Plan Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial artifact review prompt for the Data Capture Spine post-batch patch plan.
use_when:
  - Commissioning adversarial review of `docs/product/data_capture_spine_post_batch_patch_plan_v0.md`.
  - Checking whether the patch plan can safely proceed to owner acceptance, narrowing, or revision.
  - Attacking overclaims, hidden contract hardening, source-access implementation drift, MSP overpromotion, checker-validation leakage, and propagation/routing defects.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine_post_batch_patch_plan_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_post_batch_patch_plan_adversarial_artifact_review_v0.md
stale_if:
  - `docs/product/data_capture_spine_post_batch_patch_plan_v0.md` changes materially.
  - The first N=3 batch classification decision is superseded.
  - The obligation contract, source-access method plan, Data Capture/Cleaning boundary, or source-loading overlay is materially amended.
  - A later adversarial artifact review prompt supersedes this one.
```

## Paste-Ready Prompt

You are performing a **read-only adversarial artifact review** for Orca.

Review target:

```text
docs/product/data_capture_spine_post_batch_patch_plan_v0.md
```

Review purpose:

```text
Determine whether the Data Capture Spine post-batch patch plan is safe to use as owner-gate input for later obligation-contract and source-access method patch drafts, or whether it needs revision before owner acceptance/narrowing/rejection.
```

This is not owner acceptance, not a patch lane, not a contract amendment, not source-access implementation, not validation, not readiness, not product proof, and not runtime authorization.

## Workspace And Preflight

Workspace:

```text
C:\Users\vmon7\Desktop\projects\orca
```

Expected branch and revision at prompt authoring:

```text
branch: main
HEAD: a2aebdd
```

Target artifact hash at prompt authoring:

| Source | SHA256 |
| --- | --- |
| `docs/product/data_capture_spine_post_batch_patch_plan_v0.md` | `CB71FDFA3CF7B54DDA17B2510CC7E651F9C5978967B395EFE112D1C959286D64` |

Dirty-state allowance:

- The worktree is expected to be dirty with modified and untracked Orca docs.
- The review target is expected to be untracked at prompt authoring.
- `.agents/workflow-overlay/source-loading.md` and `docs/workflows/orca_repo_map_v0.md` are expected to be modified because they were updated for navigation to the target artifact.
- Dirty or untracked state may support advisory review only.
- Dirty or untracked state does not support validation, readiness, source-of-truth promotion, buyer proof, implementation authority, or owner acceptance claims.
- If the target artifact hash mismatches, return `SOURCE_CONTEXT_INCOMPLETE_TARGET_CHANGED` unless the current launch instruction explicitly authorizes reviewing the changed target.

Output mode:

```text
review-report
```

Required report path:

```text
docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_post_batch_patch_plan_adversarial_artifact_review_v0.md
```

Edit permission:

```text
read-only review; write only the required review report path above
```

If you cannot access the repo/worktree files, return `BLOCKED_REPO_ACCESS_UNAVAILABLE`. Do not review from summaries, chat memory, or this prompt alone.

## Required Method Sequence

REFERENCE-LOAD these method instructions first. Do not APPLY them yet:

- `workflow-deep-thinking`
- `workflow-adversarial-artifact-review`

Before `SOURCE_CONTEXT_READY`, you may prepare only neutral source-reading lenses. Do not produce findings, verdicts, rankings, recommendations, or architecture conclusions before source readiness.

Then SOURCE-LOAD the required Orca sources below.

After declaring `SOURCE_CONTEXT_READY`, APPLY `workflow-deep-thinking` to frame the boundary problem, likely failure modes, and decision criteria.

Then APPLY `workflow-adversarial-artifact-review` to produce the findings-first review report.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot be applied after `SOURCE_CONTEXT_READY`, return a blocked or advisory-only result. Do not emit formal verdicts, severity authority, readiness claims, validation claims, mandatory remediation, patch queues, executor-ready handoffs, or alignment-complete claims.

## Required Sources

Authority and review-lane sources:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/communication-style.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/retrieval-metadata.md`

Review target:

- `docs/product/data_capture_spine_post_batch_patch_plan_v0.md`

Primary source basis:

- `docs/decisions/data_capture_spine_pressure_test_batch_classification_decision_v0.md`
- `docs/research/data_capture_spine_pressure_test_batch_synthesis_n3of3_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_pressure_test_batch_synthesis_n3of3_adversarial_review_v0.md`

Controlling support:

- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/data_capture_source_access_method_plan_v0.md`
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `docs/product/data_capture_spine_intake_surface_consolidation_v0.md`
- `docs/product/data_capture_harness_operating_model_architecture_v2.md`

Navigation/propagation support:

- `docs/workflows/orca_repo_map_v0.md`

Excluded by default:

- broad `docs/review-outputs/`
- broad `docs/prompts/`
- broad `docs/product/`
- broad `docs/research/`
- `docs/_inbox/`
- raw Reddit JSON or screenshots
- implementation/runtime folders
- external web research

Expand only if a missing source could materially change a finding. If expansion would exceed a bounded review source pack, report `SOURCE_CONTEXT_INCOMPLETE` with the exact missing source and why it matters.

## Review Questions

Attack the patch plan against these questions:

1. Does it preserve the patch-planning boundary, or does any section quietly apply an obligation-contract patch, source-access method patch, or new durable rule?
2. Are all contract patch candidates traceable to the classification decision and N=3 synthesis, especially `cannot_assess` / `indeterminate`, `insufficient` / `assessed_not_met`, tool-origin block vs boundary `blocked`, Obligation #16, and Obligation #6?
3. Does any candidate language accidentally become accepted contract language rather than a planned question?
4. Does the source-access section stay at method-planning level, or does it authorize builds, scrapers, APIs, dashboards, storage, schemas, tests, packages, deployment, runtime work, or source-system implementation?
5. Does the source-access section faithfully preserve the current discoverable-or-entitled + disclosable boundary and hard-stop exclusions without adding new restraint or widening beyond accepted limits?
6. Does the MSP section keep MSP as a narrow helper over preserved raw, or does it overpromote one Reddit data point into final contract doctrine?
7. Does the checker section avoid turning pass-2 checking, checker tokens, model agreement, or invocation equivalence into validation, readiness, approval, proof, or source adequacy?
8. Does the owner gate correctly keep the artifact as review target and planning input, not patch authority?
9. Are deferred items complete enough to prevent accidental contract hardening, source-access implementation, new pressure-test execution, or ECR/Cleaning/Judgment design?
10. Are navigation updates in `.agents/workflow-overlay/source-loading.md` and `docs/workflows/orca_repo_map_v0.md` appropriately narrow, or do they create authority beyond retrieval/routing?
11. Is the direction-change propagation receipt proportionate and accurate, including trigger choice, controlled sources, intentionally-not-updated surfaces, and stale-language search?
12. Does the retrieval header help future source loading without creating authority, approval, readiness, lifecycle status, edit permission, or validation proof?
13. Does the artifact contain stale partial-draft language, readiness language, validation language, or owner-acceptance leakage?
14. Does the artifact need revision before owner-gate use, or is it safe to put before the owner after review?

## Required Finding Severity

Use these priority labels only:

- `critical`: using the patch plan as owner-gate input would likely create false contract hardening, implementation authorization, validation/readiness, or doctrine/lifecycle authority.
- `major`: using the patch plan as owner-gate input would materially distort the owner's decision because of overclaim, source-trace failure, stale language, missing material limitation, or boundary drift.
- `minor`: wording, retrieval, routing, or friction issue that should be patched but does not materially distort owner-gate use if explicitly carried.

These labels are finding priority only. They do not create approval, rejection, readiness, validation, mandatory remediation, or patch authority.

## Recommendation Vocabulary

Use exactly one:

- `use_as_owner_gate_input_as_written`
- `use_as_owner_gate_input_after_minor_patch`
- `revise_before_owner_gate`
- `blocked_source_context`
- `advisory_only_skill_unavailable`

Do not use generic `pass`, `fail`, `approved`, `ready`, or `validated`.

## Output Report Requirements

Write the full durable report to:

```text
docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_post_batch_patch_plan_adversarial_artifact_review_v0.md
```

The report must include:

- retrieval header;
- `review_summary` YAML at the top;
- source readiness declaration;
- source-read ledger with dirty/untracked notes;
- review boundary and excluded scope;
- decision criteria;
- findings first, ordered by severity;
- non-findings that matter;
- not-proven boundaries;
- final recommendation from the allowed vocabulary;
- review-use boundary.

For each finding include:

- finding id;
- severity;
- phase: `correctness` or `friction`;
- target location or stable search key;
- issue;
- source evidence;
- impact;
- minimum_closure_condition;
- next_authorized_action;
- advisory remediation direction, not a patch queue.

Do not emit `patch_queue_entry`. This is read-only review.

## Chat Closeout

After successfully writing the durable report, return only a compact human sentence plus this courier YAML:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_post_batch_patch_plan_adversarial_artifact_review_v0.md
  recommendation: <one recommendation from the allowed vocabulary>
  summary: "<one sentence>"
  findings_count: <number>
  blocking_findings: []
  advisory_findings: []
  next_action: "<one concrete next step>"
```

If report writing fails after `review-report` is selected, do not use `report_path`. Return:

```yaml
review_summary:
  status: failed
  review_location: chat_only_current_thread
  recommendation: blocked_source_context
  summary: "Failed to write required report to docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_post_batch_patch_plan_adversarial_artifact_review_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  next_action: "Resolve report write failure, then rerun the review-report prompt."
```

## Hard Boundaries

Do not:

- patch the patch plan;
- patch source artifacts;
- patch the obligation contract, source-access method plan, boundary docs, source-loading overlay, or repo map;
- make the owner decision;
- apply any contract or method patch;
- authorize source-access planning beyond the existing docs-only planning scope;
- authorize source-access implementation;
- design ECR, Cleaning, Judgment, source systems, runtime, schemas, tools, dashboards, scrapers, APIs, automation, tests, packages, deployment, commits, pushes, or PRs;
- claim validation, hardening, readiness, buyer proof, product readiness, source-of-truth promotion, implementation authority, or commercial readiness.

Review findings are decision input only. Owner acceptance, patch authorization, source-access implementation, and any runtime work require separate explicit authorization.
