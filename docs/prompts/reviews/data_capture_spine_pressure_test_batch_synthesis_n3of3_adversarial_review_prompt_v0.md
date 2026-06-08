# Data Capture Spine Pressure-Test Batch Synthesis N3 of 3 Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial artifact review prompt for the completed N=3 Data Capture pressure-test batch synthesis.
use_when:
  - Commissioning adversarial review of `docs/research/data_capture_spine_pressure_test_batch_synthesis_n3of3_v0.md`.
  - Checking whether the synthesis is safe to use as commissioner decision input.
  - Attacking overclaims, stale partial-draft language, source-trace gaps, and boundary drift before commissioner classification.
authority_boundary: retrieval_only
open_next:
  - docs/research/data_capture_spine_pressure_test_batch_synthesis_n3of3_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_pressure_test_batch_synthesis_n3of3_adversarial_review_v0.md
stale_if:
  - `docs/research/data_capture_spine_pressure_test_batch_synthesis_n3of3_v0.md` changes materially.
  - Any Slot 1, Slot 2, or Slot 3 source artifact changes materially.
  - A commissioner verdict supersedes the evidence-only synthesis.
  - A later adversarial review prompt supersedes this one.
```

## Paste-Ready Prompt

You are performing a **read-only adversarial artifact review** for Orca.

Review target:

```text
docs/research/data_capture_spine_pressure_test_batch_synthesis_n3of3_v0.md
```

Review purpose:

```text
Determine whether the completed N=3 Data Capture pressure-test batch synthesis is safe to use as commissioner decision input, or whether it needs revision before commissioner classification.
```

This is not a commissioner decision, not a patch lane, not source-access planning, not validation, not readiness, not product proof, and not implementation authorization.

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
| `docs/research/data_capture_spine_pressure_test_batch_synthesis_n3of3_v0.md` | `467DC46B94A932D18E029831913FEDF31FE2BF8FBC5264C4A06821520C85F1FD` |

Dirty-state allowance:

- The worktree is expected to be dirty with modified and untracked Orca docs.
- Dirty or untracked state may support advisory review only.
- Dirty or untracked state does not support validation, readiness, source-of-truth promotion, buyer proof, implementation authority, or owner acceptance claims.
- If the target artifact hash mismatches, return `SOURCE_CONTEXT_INCOMPLETE_TARGET_CHANGED` unless the current launch instruction explicitly authorizes reviewing the changed target.

Output mode:

```text
review-report
```

Required report path:

```text
docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_pressure_test_batch_synthesis_n3of3_adversarial_review_v0.md
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

- `docs/research/data_capture_spine_pressure_test_batch_synthesis_n3of3_v0.md`

Primary pressure-test inputs:

- `slot1_mi_CAPTURE_operator_workfile.md`
- `slot2_teal_CAPTURE_operator_workfile.md`
- `docs/product/data_capture_spine_pressure_test_slot3_combined_handoff_v0.md`
- `docs/product/data_capture_spine_pressure_test_slot3_reddit_capture_session_v0.md`
- `docs/product/data_capture_spine_pressure_test_slot3_wso_capture_session_v0.md`

Controlling support:

- `docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md`
- `docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `docs/product/data_capture_source_access_boundary_decision_v0.md`
- `docs/product/data_capture_spine_intake_surface_consolidation_v0.md`

Historical support, only where decision-relevant:

- `docs/research/data_capture_spine_pressure_test_batch_synthesis_n2of3_v0.md`
- `docs/prompts/handoffs/orca_data_capture_pressure_test_ca_handoff_prompt_v0.md`

Excluded by default:

- broad `docs/review-outputs/`
- broad `docs/prompts/`
- broad `docs/product/`
- `docs/_inbox/`
- raw Reddit JSON or screenshots unless the target artifact makes a claim that cannot be checked from the Slot 3 handoff/session artifacts
- implementation/runtime folders
- external web research

Expand only if a missing source could materially change a finding. If expansion would exceed a bounded review source pack, report `SOURCE_CONTEXT_INCOMPLETE` with the exact missing source and why it matters.

## Review Questions

Attack the synthesis against these questions:

1. Does the synthesis preserve its evidence-only boundary, or does any language quietly become a commissioner verdict, patchable/architecture-threatening classification, contract amendment, source-access implementation authorization, validation, readiness, buyer proof, or product authority?
2. Are all material claims traceable to Slot 1, Slot 2, Slot 3, the commissioning/authorization docs, or the obligation/boundary docs?
3. Does any stale partial-draft routing language remain, especially references to pending steps, incomplete sections, or historical Slot 3 fork state?
4. Does the synthesis treat source-access/fetcher requirements as planning inputs only, without authorizing runtime, scrapers, APIs, storage, dashboards, tools, tests, packages, or deployment?
5. Does it correctly distinguish source fidelity failures from capture-boundary drift?
6. Does it overstate what "held" across the batch, especially given Slot 1 paraphrase, Slot 2 zero source observable, and Slot 3 WSO pointer-level limits?
7. Does it understate any architecture-threatening signal by hiding it inside "method requirement" language?
8. Does it overpromote Mechanical Source Projection from one Reddit data point into doctrine, or does it keep MSP as a narrow candidate helper?
9. Does the checker interpretation fairly account for Slot 3's weaker WSO checker equivalence and pass-2's not-yet-adopted status?
10. Does the commissioner decision queue contain actual decisions rather than recommendations disguised as decisions?
11. Does the validation-readback section avoid making a validation claim while still pointing to authoring checks?
12. Does the retrieval header help future source loading without creating authority, approval, readiness, or lifecycle status?

## Required Finding Severity

Use these priority labels only:

- `critical`: using the synthesis as commissioner input would likely create a false verdict, validation/readiness claim, implementation authorization, or doctrine change.
- `major`: using the synthesis as commissioner input would materially distort the commissioner decision because of overclaim, source-trace failure, stale routing language, missing material limitation, or boundary drift.
- `minor`: wording, retrieval, routing, or friction issue that should be patched but does not materially distort commissioner use if explicitly carried.

These labels are finding priority only. They do not create approval, rejection, readiness, validation, mandatory remediation, or patch authority.

## Recommendation Vocabulary

Use exactly one:

- `use_as_commissioner_input_as_written`
- `use_as_commissioner_input_after_minor_patch`
- `revise_before_commissioner_input`
- `blocked_source_context`
- `advisory_only_skill_unavailable`

Do not use generic `pass`, `fail`, `approved`, `ready`, or `validated`.

## Output Report Requirements

Write the full durable report to:

```text
docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_pressure_test_batch_synthesis_n3of3_adversarial_review_v0.md
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
  report_path: docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_pressure_test_batch_synthesis_n3of3_adversarial_review_v0.md
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
  summary: "Failed to write required report to docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_pressure_test_batch_synthesis_n3of3_adversarial_review_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  next_action: "Resolve report write failure, then rerun the review-report prompt."
```

## Hard Boundaries

Do not:

- patch the synthesis;
- patch source artifacts;
- patch the obligation contract, commissioning plan, execution authorization, or overlay;
- make the commissioner classification;
- authorize source-access planning or implementation;
- design ECR, Cleaning, Judgment, source systems, runtime, schemas, tools, dashboards, scrapers, APIs, automation, tests, packages, deployment, commits, pushes, or PRs;
- claim validation, hardening, readiness, buyer proof, product readiness, source-of-truth promotion, implementation authority, or commercial readiness.

Review findings are decision input only. Owner acceptance, commissioner classification, patch authorization, source-access planning, and any implementation/runtime work require separate explicit authorization.
