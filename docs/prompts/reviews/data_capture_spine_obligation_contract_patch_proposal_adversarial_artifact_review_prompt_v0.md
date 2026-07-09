# Data Capture Spine Obligation Contract Patch Proposal Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial artifact review prompt for the Data Capture Spine obligation-contract patch proposal.
use_when:
  - Commissioning adversarial review of `docs/product/data_capture_spine_obligation_contract_patch_proposal_v0.md`.
  - Checking whether proposed contract language is safe to put before the owner for later contract amendment decisions.
  - Attacking hidden contract hardening, source-access widening, ECR/Cleaning/Judgment leakage, checker-validation leakage, and routing/propagation defects.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md # successor for deleted proposal
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_patch_proposal_adversarial_artifact_review_v0.md
input_hashes:
  docs/product/data_capture_spine_obligation_contract_patch_proposal_v0.md: 83DB86DBDF742C11DAEED5A8E6C280CEA0C2DADA402AFAEAC31689862540F8D1
stale_if:
  - `docs/product/data_capture_spine_obligation_contract_patch_proposal_v0.md` changes materially.
  - The post-batch patch-plan owner decision is superseded.
  - The N=3 synthesis or batch classification decision is materially revised.
  - The controlling obligation contract or source-access method plan is amended before this review runs.
  - A later adversarial artifact review prompt supersedes this one.
```

## Prompt Authoring Preflight

```yaml
orca_start_preflight:
  agents_read: yes - AGENTS.md supplied in current task context
  overlay_read: yes
  source_pack: custom obligation-contract patch proposal adversarial review prompt pack
  edit_permission: docs-write
  target_scope: saved review prompt for read-only adversarial artifact review
  dirty_state_checked: yes - worktree dirty; target proposal and prompt are untracked; source-loading and repo-map modified; prompt makes no validation, readiness, approval, or implementation claim
  blocked_if_missing: none
```

Template source: `docs/prompts/templates/review/adversarial_artifact_review_v0.md` with Orca prompt-orchestration and review-lane overlays applied.

## Paste-Ready Prompt

You are performing a **read-only adversarial artifact review** for Orca.

Review target:

```text
docs/product/data_capture_spine_obligation_contract_patch_proposal_v0.md
```

Review purpose:

```text
Determine whether the Data Capture Spine obligation-contract patch proposal is safe to use as owner decision input for later obligation-contract amendment, or whether it needs revision before owner consideration.
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
HEAD: a2aebdd8e04c627c5102e79eb324b24b3de35226
```

Target artifact hash at prompt authoring:

| Source | SHA256 |
| --- | --- |
| `docs/product/data_capture_spine_obligation_contract_patch_proposal_v0.md` | `83DB86DBDF742C11DAEED5A8E6C280CEA0C2DADA402AFAEAC31689862540F8D1` |

Dirty-state allowance:

- The worktree is expected to be dirty with modified and untracked Orca docs.
- The review target is expected to be untracked at prompt authoring.
- `.agents/workflow-overlay/source-loading.md` and `docs/workflows/orca_repo_map_v0.md` are expected to be modified because they were updated for navigation to the target artifact.
- Dirty or untracked state may support advisory review only.
- Dirty or untracked state does not support validation, readiness, source-of-truth promotion, buyer proof, implementation authority, or contract acceptance claims.
- If the target artifact hash mismatches, return `SOURCE_CONTEXT_INCOMPLETE_TARGET_CHANGED` unless the current launch instruction explicitly authorizes reviewing the changed target.

Output mode:

```text
review-report
```

Required report path:

```text
docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_patch_proposal_adversarial_artifact_review_v0.md
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
- `.agents/workflow-overlay/template-registry.md`

Review target:

- `docs/product/data_capture_spine_obligation_contract_patch_proposal_v0.md`

Primary source basis:

- `docs/decisions/data_capture_spine_post_batch_patch_plan_owner_decision_v0.md`
- `docs/product/data_capture_spine_post_batch_patch_plan_v0.md`
- `docs/decisions/data_capture_spine_pressure_test_batch_classification_decision_v0.md`
- `docs/research/data_capture_spine_pressure_test_batch_synthesis_n3of3_v0.md`

Controlling support:

- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/data_capture_source_access_method_plan_v0.md`
- `docs/product/data_capture_source_access_boundary_decision_v0.md`
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`

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

Attack the proposal against these questions:

1. Does the proposal preserve the proposal boundary, or does any section quietly amend, harden, or supersede the controlling obligation contract?
2. Are PCP-01 through PCP-08 traceable to the owner decision, patch plan, batch classification decision, and N=3 synthesis?
3. Does the proposal accurately preserve the current obligation contract rather than inventing a false current-state problem?
4. Are `cannot_assess`, `assessed_not_met`, and `access_failed` defined tightly enough to prevent generic uncertainty, weak capture, or tool failure from becoming fake sufficiency?
5. Does the narrowed `blocked` language preserve the current source-access hard stops without adding over-restraint or widening beyond accepted limits?
6. Does the #16 handoff-readiness split clarify Capture-owned readiness without defining ECR schema, receipt mechanics, IDs, keys, storage, or downstream handoff implementation?
7. Does the #6 raw-observable fidelity split prevent fact-row/paraphrase capture from masquerading as raw-observable preservation without creating universal screenshot/media bloat?
8. Does checker-token language avoid turning checker output, pass-2 checking, invocation count, artifact-internal self-check, or model agreement into validation, readiness, approval, proof, source adequacy, or mandatory rerun authority?
9. Does the patch disposition queue overstate what should be carried into a future contract amendment, or does it correctly preserve review/owner decision gates?
10. Does any proposed wording create source-access method-plan obligations that belong in the separate source-access proposal instead of the obligation contract?
11. Are non-claims and deferred gates complete enough to prevent accidental contract hardening, source-access implementation, new pressure-test execution, or ECR/Cleaning/Judgment design?
12. Are navigation updates in `.agents/workflow-overlay/source-loading.md` and `docs/workflows/orca_repo_map_v0.md` appropriately narrow, or do they create authority beyond retrieval/routing?
13. Is the direction-change propagation receipt proportionate and accurate, including trigger choice, controlling sources, intentionally-not-updated surfaces, and stale-language search?
14. Does the retrieval header help future source loading without creating authority, approval, readiness, lifecycle status, edit permission, or validation proof?
15. Does the artifact need revision before owner consideration, or is it safe to put before the owner after review?

## Required Finding Severity

Use these priority labels only:

- `critical`: using the proposal as owner decision input would likely create false contract hardening, implementation authorization, validation/readiness, or doctrine/lifecycle authority.
- `major`: using the proposal as owner decision input would materially distort the owner's decision because of overclaim, source-trace failure, stale language, missing material limitation, boundary drift, or mis-specified candidate contract language.
- `minor`: wording, retrieval, routing, or friction issue that should be patched but does not materially distort owner consideration if explicitly carried.

These labels are finding priority only. They do not create approval, rejection, readiness, validation, mandatory remediation, or patch authority.

## Recommendation Vocabulary

Use exactly one:

- `safe_for_owner_consideration_as_written`
- `safe_for_owner_consideration_after_minor_patch`
- `revise_before_owner_consideration`
- `blocked_source_context`
- `advisory_only_skill_unavailable`

Do not use generic `pass`, `fail`, `approved`, `ready`, or `validated`.

## Output Report Requirements

Write the full durable report to:

```text
docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_patch_proposal_adversarial_artifact_review_v0.md
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
  report_path: docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_patch_proposal_adversarial_artifact_review_v0.md
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
  summary: "Failed to write required report to docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_patch_proposal_adversarial_artifact_review_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  next_action: "Resolve report write failure, then rerun the review-report prompt."
```

## Hard Boundaries

Do not:

- patch the proposal;
- patch source artifacts;
- patch the obligation contract, source-access method plan, boundary docs, source-loading overlay, or repo map;
- make the owner decision;
- apply any contract or method patch;
- authorize source-access implementation;
- design ECR, Cleaning, Judgment, source systems, runtime, schemas, tools, dashboards, scrapers, APIs, automation, tests, packages, deployment, commits, pushes, or PRs;
- claim validation, hardening, readiness, buyer proof, product readiness, source-of-truth promotion, implementation authority, or commercial readiness.

Review findings are decision input only. Owner acceptance, patch authorization, source-access implementation, and any runtime work require separate explicit authorization.
