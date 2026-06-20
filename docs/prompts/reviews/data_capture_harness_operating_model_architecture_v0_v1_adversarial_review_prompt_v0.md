# Data Capture Harness Operating Model Architecture v0/v1 Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: Read-only adversarial artifact review prompt comparing the v0 and v1 proposed Data Capture Harness operating-model architecture artifacts, with v1 treated as the presumptive candidate but not accepted.
use_when:
  - Commissioning an adversarial review before owner acceptance of a Data Capture Harness operating-model architecture.
  - Comparing v0 plain-model-fallback architecture output against v1 delegated-three-subagent architecture output.
  - Stress-testing CPOE-ARC for review-theater, Judgment leakage, operator authority creep, excessive operating-model weight, and boundary drift.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v1.md
  - orca/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v0.md
  - orca/product/spines/capture/core/operating_model/data_capture_obligation_baseline_decision_v0.md
  - orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - orca/product/spines/capture/core/operating_model/data_capture_harness_product_goal_direction_signal_decision_v0.md
stale_if:
  - Either v0 or v1 architecture artifact is materially revised or superseded.
  - The Data Capture obligation baseline decision is amended, rejected, or superseded.
  - The Data Capture obligation contract is materially revised or superseded.
  - A later owner decision accepts, rejects, patches, or hybridizes v0/v1.
```

- Prompt target: model-neutral Orca adversarial artifact review lane.
- Output mode: `review-report`.
- Review report path: `docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_v0.md`.
- Prompt artifact path: `docs/prompts/reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_prompt_v0.md`.
- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Expected branch: `main`
- Expected HEAD: `b7627d3`
- Target v0 path: `docs/product/data_capture_harness_operating_model_architecture_v0.md`
- Target v0 SHA256: `F43238167562437D26FCC5FCCFCE9152B83C8FD383AE750B9A21990089F5E3A2`
- Target v1 path: `docs/product/data_capture_harness_operating_model_architecture_v1.md`
- Target v1 SHA256: `BCC62DAC605ADA7BC5AA5A79482E0FBBEECC47322339DEC83E0CF234678BC8CF`
- Reviewer edit permission: read-only; may write only the review report.
- Patch execution authorized: no.
- Architecture acceptance authorized: no.
- Implementation/runtime/ECR/Cleaning/Judgment work authorized: no.
- Source-of-truth promotion claimed: no.

## Paste-Ready Prompt

```text
<role>
You are performing a read-only adversarial artifact review for Orca.
</role>

<commission>
Review target:
- `docs/product/data_capture_harness_operating_model_architecture_v0.md`
- `docs/product/data_capture_harness_operating_model_architecture_v1.md`

Review purpose:
Compare the two proposed Data Capture Harness operating-model architecture
artifacts before owner acceptance. Treat v1 as the presumptive candidate because
it was produced under `delegated_three_subagents` and names CPOE-ARC, but do not
accept it. Attack whether v1 should be accepted, patched, hybridized with v0,
sent back for another architecture pass, or rejected.

Primary adversarial target:
`Contract-Pinned Operating Envelope with Adversarial Reviewer Checkpoint
(CPOE-ARC)` in v1.

This review must specifically test whether CPOE-ARC accidentally creates:
- review theater;
- Judgment leakage;
- ECR/Cleaning leakage;
- operator authority creep;
- reviewer refusal authority that becomes hidden Judgment;
- too-heavy operating-model overhead;
- false confidence from delegated subagent agreement;
- fake success through obligation-state completeness;
- manual-harness ossification;
- source-family satellite drift into core;
- runtime/tooling gravity through deferred implementation implications.
</commission>

<workspace_preflight>
Worktree: `C:\Users\vmon7\Desktop\projects\orca`
Expected branch: `main`
Expected HEAD: `b7627d3`

Required target hashes:
- v0 SHA256: `F43238167562437D26FCC5FCCFCE9152B83C8FD383AE750B9A21990089F5E3A2`
- v1 SHA256: `BCC62DAC605ADA7BC5AA5A79482E0FBBEECC47322339DEC83E0CF234678BC8CF`

Dirty-state allowance:
- Dirty and untracked Orca prompt/product/overlay sources are allowed for this
  advisory review only if named in the source-read ledger.
- Do not claim strict readiness, validation, acceptance, source-of-truth
  promotion, proof, or PASS status from dirty/untracked source state alone.

Required output mode:
- `review-report`
- Write the durable report to:
  `docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_v0.md`

If the report cannot be written, return `FAILED_REVIEW_OUTPUT_WRITE` and do not
treat chat output as the durable review artifact.
</workspace_preflight>

<required_method_sequence>
1. REFERENCE-LOAD `workflow-deep-thinking`.
2. REFERENCE-LOAD `workflow-adversarial-artifact-review`.
3. Do not APPLY either method yet. Before source readiness, use them only to
   prepare neutral source-reading questions.
4. SOURCE-LOAD the required Orca sources below.
5. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
6. Only after source readiness, APPLY `workflow-deep-thinking` to frame the
   boundary problem, hidden assumptions, comparison criteria, and failure modes.
7. Then APPLY `workflow-adversarial-artifact-review` to v0 and v1 under this
   commission.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot
be applied after `SOURCE_CONTEXT_READY`, return a blocked or advisory-only
result. Do not emit formal verdicts, readiness claims, validation claims,
mandatory remediation, patch queues, executor-ready handoffs, or
alignment-complete claims.
</required_method_sequence>

<required_sources>
Control and overlay sources:
- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/communication-style.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/product-proof.md`

Review targets:
- `docs/product/data_capture_harness_operating_model_architecture_v0.md`
- `docs/product/data_capture_harness_operating_model_architecture_v1.md`

Controlling product-method sources:
- `docs/product/data_capture_obligation_baseline_decision_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md`
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`

Conditional expansion only if a concrete finding depends on provenance,
prompt-contract compliance, or source conflict:
- `docs/prompts/product-planning/data_capture_harness_operating_model_architecture_prompt_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_prompt_adversarial_review_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_manual_harness_bt204_dry_run_adversarial_review_v0.md`

Default exclusions:
- Do not read `docs/_inbox/`.
- Do not bulk-load all product, prompt, review, research, workflow, proof-run,
  or method-validation replay files.
- Do not read implementation folders or create implementation scope.
</required_sources>

<review_questions>
Answer these questions adversarially:

1. Is v1 actually stronger than v0, or does delegated-subagent evidence create
   false confidence?
2. Does CPOE-ARC preserve Capture/Judgment/ECR/Cleaning boundaries, especially
   around the adversarial reviewer checkpoint and refusal authority?
3. Does the reviewer checkpoint create review theater: a visible adversarial
   gate that looks rigorous but does not improve capture obligation discharge?
4. Does v1 add too much operating-model weight before 3-5 real commissioned
   pressure tests?
5. Does v1's "adversarial reviewer" role make hidden credibility, exclusion,
   discounting, signal-use, Decision Strength, or Action Ceiling decisions?
6. Does v1 avoid schema/runtime drift while still making obligation-discharge
   visible enough for downstream ECR handoff?
7. Does v1 preserve source-family satellite discipline, or does it create a
   pathway for source-family mechanics to become core through reviewer behavior?
8. Does v1's next authorized step overreach by moving too quickly into
   operator-roster and pressure-test commissioning, or is that the correct next
   planning object after owner acceptance?
9. Does v0 contain a simpler, safer architecture surface that should be kept or
   hybridized into v1?
10. Are there internal contradictions, version/status mismatches, retrieval
    metadata issues, stale-if gaps, non-claim leaks, or source-readiness
    overclaims in either artifact?
</review_questions>

<finding_contract>
Report findings first, ordered by materiality.

For each finding include:
- finding id;
- phase: `correctness` or `friction`;
- severity: `critical`, `major`, or `minor` as finding-priority labels only;
- target: `v0`, `v1`, `v0_vs_v1`, or `source_context`;
- location or stable search key;
- issue;
- evidence;
- impact on owner acceptance, boundary control, architecture usefulness, or
  downstream routing;
- minimum_closure_condition;
- next_authorized_action.

Do not include `patch_queue_entry`. This is read-only review.
</finding_contract>

<recommendation_contract>
Use exactly one advisory recommendation:
- `accept_v1_as_candidate`: no blocking or major issue prevents owner acceptance
  of v1 as the operating-model architecture, subject to non-claims.
- `patch_v1_before_acceptance`: v1 is the right base, but bounded artifact
  patching is needed before owner acceptance.
- `hybridize_v0_v1_before_acceptance`: v1 contains the stronger target, but v0
  contains safer/simpler architecture surface that should be merged before
  acceptance.
- `prefer_v0_before_acceptance`: v0 is safer or more faithful than v1.
- `reject_both_reopen_architecture`: neither v0 nor v1 is fit as the owner
  acceptance base.
- `needs_source_context`: required source context is missing or conflicted.

These recommendation labels are advisory review outputs only. They are not
approval, validation, readiness, owner acceptance, mandatory remediation,
patch authority, architecture execution, or implementation authority.
</recommendation_contract>

<output_contract>
Write the full review report to:
`docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_v0.md`

The report must include:
- source-readiness declaration;
- source-read ledger;
- dirty/untracked source caveats;
- review boundary and excluded scope;
- comparison frame;
- findings;
- non-findings that matter;
- v0 strengths worth preserving;
- v1 strengths worth preserving;
- not-proven boundaries;
- advisory recommendation;
- smallest next authorized step.

After writing the report, return a compact human summary plus courier YAML:

review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_v0.md
  recommendation: accept_v1_as_candidate | patch_v1_before_acceptance | hybridize_v0_v1_before_acceptance | prefer_v0_before_acceptance | reject_both_reopen_architecture | needs_source_context
  summary: "..."
  findings_count: N
  blocking_findings: [...]
  advisory_findings: [...]
  next_action: "..."
</output_contract>

<review_use_boundary>
This is a read-only adversarial artifact review. Findings are decision input
for the owner. They are not acceptance, validation, readiness, source-of-truth
promotion, mandatory remediation, patch authority, architecture execution,
implementation authority, or runtime/tooling authorization.
</review_use_boundary>
```
