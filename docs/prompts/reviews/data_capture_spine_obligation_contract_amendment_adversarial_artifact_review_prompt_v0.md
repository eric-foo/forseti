# Data Capture Spine Obligation Contract Amendment Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial artifact review prompt for the amended Data Capture Spine obligation contract after PCP-01 through PCP-08 were operationalized.
use_when:
  - Commissioning adversarial review of `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` after commit `f55002d`.
  - Checking whether the amended obligation contract faithfully consumed the accepted PCP package without leaking into source-access method planning, ECR, Cleaning, Judgment, runtime, validation, readiness, or proof authority.
  - Attacking source-support, propagation, checker-vocabulary, discharge-state, Obligation #6, Obligation #16, and source-access-boundary risks in the amended controlling contract.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - docs/decisions/data_capture_spine_obligation_contract_patch_proposal_owner_decision_v0.md
  - docs/product/data_capture_spine/data_capture_spine_obligation_contract_patch_proposal_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_amendment_adversarial_artifact_review_v0.md
input_hashes:
  docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md: 85925ECB3429CF39CE4F287E959E75DE8944260596C798321D0E38186E6D45DC
stale_if:
  - `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` changes materially.
  - `docs/decisions/data_capture_spine_obligation_contract_patch_proposal_owner_decision_v0.md` is superseded.
  - `docs/product/data_capture_source_access_boundary_decision_v0.md` or `docs/product/data_capture_source_access_method_plan_v0.md` changes in a way that affects Obligation #2 or `access_failed`.
  - A later adversarial artifact review prompt supersedes this one.
```

## Prompt Authoring Preflight

```yaml
orca_start_preflight:
  agents_read: yes - AGENTS.md supplied in current task context
  overlay_read: yes
  source_pack: custom Data Capture obligation-contract amendment adversarial review prompt pack
  edit_permission: docs-write
  target_scope: saved review prompt for read-only adversarial artifact review
  dirty_state_checked: yes - worktree broadly dirty; committed review target and immediate committed amendment-trail files are clean at prompt authoring; several adjacent Data Capture sources remain untracked or modified and must be ledgered by the reviewer
  blocked_if_missing: none
```

Template source: `docs/prompts/templates/review/adversarial_artifact_review_v0.md` with Orca prompt-orchestration and review-lane overlays applied.

## Paste-Ready Prompt

You are performing a **read-only adversarial artifact review** for Orca.

Review target:

```text
docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
```

Review purpose:

```text
Determine whether the amended Data Capture Spine obligation contract correctly operationalizes PCP-01 through PCP-08 from the accepted owner decision, or whether it needs a targeted patch before being used as the operative Data Capture obligation contract for further pressure-test or capture-spine work.
```

This is not validation, not readiness, not owner acceptance, not a patch lane, not source-access method-plan amendment, not ECR design, not Cleaning implementation, not Judgment design, not product proof, and not runtime/source-system authorization.

## Workspace And Preflight

Workspace:

```text
C:\Users\vmon7\Desktop\projects\orca
```

Expected branch and revision at prompt authoring:

```text
branch: main
HEAD: f55002d
```

Target artifact hash at prompt authoring:

| Source | SHA256 |
| --- | --- |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | `85925ECB3429CF39CE4F287E959E75DE8944260596C798321D0E38186E6D45DC` |

Dirty-state allowance:

- The worktree is expected to be broadly dirty with modified and untracked Orca docs.
- The review target and these immediate amendment-trail files were committed in `f55002d` and expected clean at prompt authoring:
  - `.agents/workflow-overlay/source-loading.md`
  - `docs/workflows/orca_repo_map_v0.md`
  - `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
  - `docs/product/data_capture_spine_obligation_contract_patch_proposal_v0.md`
  - `docs/decisions/data_capture_spine_obligation_contract_patch_proposal_owner_decision_v0.md`
  - `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_patch_proposal_adversarial_artifact_review_v0.md`
- Several adjacent Data Capture sources may remain modified or untracked, including pressure-test decisions, source-access boundary, source-access method plan, and batch synthesis artifacts. Read them when required, but ledger their dirty/untracked state and avoid strict validation/readiness/source-of-truth claims from unanchored sources.
- If the target artifact hash mismatches, return `SOURCE_CONTEXT_INCOMPLETE_TARGET_CHANGED` unless the current launch instruction explicitly authorizes reviewing the changed target.

Output mode:

```text
review-report
```

Required report path:

```text
docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_amendment_adversarial_artifact_review_v0.md
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

- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`

Immediate amendment trail:

- `docs/decisions/data_capture_spine_obligation_contract_patch_proposal_owner_decision_v0.md`
- `docs/product/data_capture_spine_obligation_contract_patch_proposal_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_patch_proposal_adversarial_artifact_review_v0.md`

Controlling support:

- `docs/product/data_capture_source_access_boundary_decision_v0.md`
- `docs/product/data_capture_source_access_method_plan_v0.md`
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`
- `docs/product/core_spine_v0_data_capture_context_preservation_note_v0.md`

Patch-basis support, read only if needed to adjudicate source trace or owner authority:

- `docs/decisions/data_capture_spine_post_batch_patch_plan_owner_decision_v0.md`
- `docs/product/data_capture_spine_post_batch_patch_plan_v0.md`
- `docs/decisions/data_capture_spine_pressure_test_batch_classification_decision_v0.md`
- `docs/research/data_capture_spine_pressure_test_batch_synthesis_n3of3_v0.md`

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

Attack the amended contract against these questions:

1. Does the contract accurately consume PCP-01 through PCP-08, or does it silently add, drop, or distort an accepted PCP decision?
2. Are `cannot_assess`, `assessed_not_met`, and `access_failed` defined tightly enough to prevent skipped capture, weak capture, ordinary uncertainty, or tool failure from becoming fake sufficiency?
3. Does the narrowed `blocked` language preserve true source-boundary/project-boundary/hard-stop exclusions without overloading routine access failure?
4. Is Obligation #2 consistent with the current source-access boundary decision and source-access method plan, especially around discoverable-or-entitled access, hard stops, and `access_failed`?
5. Does Obligation #2 accidentally amend source-access method planning, legal posture, or runtime/source-system authorization?
6. Does Obligation #6 Raw Observable Fidelity preserve the smallest complete fidelity split without making Capture decide decision-materiality?
7. Does Obligation #6 avoid universal screenshot/media bloat while still preventing fact-row/paraphrase capture from masquerading as raw observable preservation?
8. Does Obligation #16 Categorical Handoff Readiness correctly separate Capture-owned readiness from actual ECR receipt?
9. Does Obligation #16 retain archive/locator/source-slice specificity from the prior contract and owner decision without defining ECR schema, keys, IDs, tables, receipt structures, storage, or file formats?
10. Does the new Checker Vocabulary And Comparability section prevent checker output, pass-2 checking, invocation count, artifact-internal self-check, or model agreement from becoming validation, readiness, approval, proof, source adequacy, or mandatory rerun authority?
11. Does the pressure-test checklist correctly recognize the new discharge states and checker limits without hardening the contract from abstract reasoning alone?
12. Do rejected patterns, forbidden outputs, and non-claims still block source maps as core architecture, runtime plans, ECR-by-stealth, Cleaning-by-stealth, and Judgment-by-stealth?
13. Is the direction-change propagation receipt accurate and complete, including trigger choice, updated surfaces, intentionally-not-updated surfaces, and stale-language search?
14. Are `source-loading.md` and `orca_repo_map_v0.md` routing updates appropriately narrow, or did they create retrieval/source-loading authority beyond this amendment?
15. Does the retrieval header and source basis help future source loading without overstating validation, readiness, approval, source-of-truth promotion, lifecycle completion, or implementation authorization?
16. Does any wording create ambiguity that would mislead the next Data Capture operator, reviewer, or pressure-test commissioner?
17. Does the amended contract need revision before further Data Capture pressure-test/capture-spine work relies on it?

## Required Finding Severity

Use these priority labels only:

- `critical`: continued use of the amended contract would likely create false implementation authorization, validation/readiness, ECR/Cleaning/Judgment leakage, source-access hard-stop bypass, or materially corrupt Data Capture obligation discharge.
- `major`: continued use would materially distort future Data Capture work because of source-trace failure, stale lifecycle language, ambiguous operative contract language, weakened archive/locator/source-slice specificity, or mis-specified PCP consumption.
- `minor`: wording, retrieval, propagation, or operator-friction issue that should be patched but does not materially distort future Data Capture work if explicitly carried.

These labels are finding priority only. They do not create approval, rejection, readiness, validation, mandatory remediation, or patch authority.

## Recommendation Vocabulary

Use exactly one:

- `continue_using_with_no_material_findings`
- `continue_using_after_minor_patch`
- `revise_before_next_data_capture_work`
- `blocked_source_context`
- `advisory_only_skill_unavailable`

Do not use generic `pass`, `fail`, `approved`, `ready`, or `validated`.

## Output Report Requirements

Write the full durable report to:

```text
docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_amendment_adversarial_artifact_review_v0.md
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
  report_path: docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_amendment_adversarial_artifact_review_v0.md
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
  summary: "Failed to write required report to docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_amendment_adversarial_artifact_review_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  next_action: "Resolve report write failure, then rerun the review-report prompt."
```

## Hard Boundaries

Do not:

- patch the amended contract;
- patch source artifacts;
- patch source-loading, repo map, source-access method plan, source-access boundary, ECR, Cleaning, or Judgment docs;
- make the owner decision;
- apply any contract or method patch;
- authorize source-access implementation;
- design ECR, Cleaning, Judgment, source systems, runtime, schemas, tools, dashboards, scrapers, APIs, automation, tests, packages, deployment, commits, pushes, or PRs;
- claim validation, hardening, readiness, buyer proof, product readiness, source-of-truth promotion, implementation authority, or commercial readiness.

Review findings are decision input only. Owner acceptance, patch authorization, source-access implementation, and any runtime work require separate explicit authorization.
