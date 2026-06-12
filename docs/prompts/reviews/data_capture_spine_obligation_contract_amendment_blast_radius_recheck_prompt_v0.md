# Data Capture Spine Obligation Contract Amendment Blast-Radius Recheck Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Narrow read-only adversarial blast-radius recheck prompt for the Data Capture Spine obligation contract amendment after AR-01 through AR-05 closure patches.
use_when:
  - Checking whether the post-review patches closed AR-01 through AR-05 from the obligation-contract amendment adversarial review.
  - Looking only for patch-caused or newly visible blocker/major regressions inside the amended contract, source-access basis, blueprint/context-note de-staling, and repo-map hash surfaces.
  - Deciding whether the amended obligation contract can be used for the next Data Capture pressure-test or capture-spine work without another source-trace patch first.
authority_boundary: retrieval_only
open_next:
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_amendment_adversarial_artifact_review_v0.md
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - docs/product/data_capture_spine/data_capture_source_access_boundary_decision_v0.md
  - docs/product/data_capture_spine/data_capture_source_access_method_plan_v0.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
input_hashes:
  core_spine_v0_data_capture_spine_obligation_contract_v0.md: B06BD6722F76D223E7A122B7F97B967431BDEEE5D4E41AD6DCCEF81903DAC8C5
  data_capture_source_access_boundary_decision_v0.md: 9F09AE169644762250DFAB05EA627503A5E09393688D490E366B9F73E5B00C89
  data_capture_source_access_method_plan_v0.md: 74E28477400AAC3F2889AF0F0933E69E372C327DF0FAF88E7734291EF0A2EA0E
  core_spine_v0_data_capture_spine_architecture_blueprint_v0.md: A9FF03A159EA4D3029F5B25E1F7802E1F147F7BA35CF91063BCFAD1AC6FED434
  core_spine_v0_data_capture_context_preservation_note_v0.md: 1CED21649EEF0776F231BBBA4DB9869AB6669944604AB70D09CE997409921A6E
  orca_repo_map_v0.md: C524CFC817ABE29828210BFF9D692B3D03D50314CDF582157FAFC618C50B63F5
  prior_review_report: 6F12384CE30F99D80C65A6623AE51ECC1AFE616F60C2E95F2AEB1B52E3C55126
  adversarial_artifact_review_template: 17188D11F4C151103CC746328D02F0DFC94FCF3AAD3F39714A510CEDBA5A60AA
stale_if:
  - Any input hash above changes materially.
  - A later owner decision accepts, rejects, or supersedes the AR-01 through AR-05 closure patches.
  - A later adversarial recheck supersedes this prompt.
```

- Status: `PROPOSED_PROMPT`
- Artifact type: Post-patch adversarial blast-radius recheck prompt
- Template kind: `review` / adversarial post-patch recheck
- Template source: `docs/prompts/templates/review/adversarial_artifact_review_v0.md` plus `.agents/workflow-overlay/prompt-orchestration.md` rerun economy rules
- Prompt artifact path: `docs/prompts/reviews/data_capture_spine_obligation_contract_amendment_blast_radius_recheck_prompt_v0.md`
- Required review report path: `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_amendment_blast_radius_recheck_v0.md`
- Output mode: `review-report`
- Reviewer edit permission: read-only, except writing the required review report
- Patch queue authorized: no
- Full fresh contract review authorized: no
- Implementation, runtime, tooling, source-access execution, ECR, Cleaning, Judgment, validation, readiness, proof, commits, pushes, PRs, or model-routing authority: no

## Prompt Author Preflight

```yaml
orca_start_preflight:
  agents_read: yes - supplied in current task context
  overlay_read: yes
  source_pack: custom Data Capture post-review blast-radius recheck pack
  edit_permission: docs-write
  target_scope: Create a narrow adversarial recheck prompt for AR-01 through AR-05 closure and patch-caused blast radius.
  dirty_state_checked: yes - broader worktree dirty; prompt target and two latest source patches may be uncommitted at authoring time
  blocked_if_missing: none
control_plane_source_state:
  branch: main
  head_observed_by_prompt_author: 4d1887c
  strict_pass_or_readiness_claimed: no
doctrine_change:
  changes_doctrine: no
  reason: This prompt applies existing Orca review/rerun policy and the contract patch adds only a trigger-chain clarification note, not a new durable rule.
```

## Prompt

You are performing a narrow read-only adversarial blast-radius recheck for Orca.

Review target:

```text
docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
```

Review purpose:

```text
Determine whether the AR-01 through AR-05 closure patches after the Data Capture obligation-contract amendment adversarial review are sufficient, and whether those patches caused any new blocker/major regression in the source-access basis, obligation contract, blueprint/context-note de-staling, repo-map hash, or doctrine-propagation receipt surfaces.
```

This is a patch-closure and blast-radius recheck lane, not a full fresh contract review, not a patch lane, not a source-access method-plan redesign, not ECR design, not Cleaning implementation, not Judgment design, not product proof, and not runtime/source-system authorization.

Do not recommend, prescribe, rank, or imply a runtime model for this review lane.

## Workspace

- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Expected branch: `main`
- Expected HEAD observed by prompt author: `4d1887c`
- Dirty-state allowance: dirty and untracked Orca docs may exist. The reviewed target may include uncommitted working-tree changes after `4d1887c`; use the hashes above to verify the intended review target. Do not claim validation, readiness, acceptance, or source-of-truth promotion from dirty or untracked state.
- Prompt artifact path: `docs/prompts/reviews/data_capture_spine_obligation_contract_amendment_blast_radius_recheck_prompt_v0.md`
- Output mode: `review-report`
- Required durable report path: `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_amendment_blast_radius_recheck_v0.md`

If the contract hash does not match `B06BD6722F76D223E7A122B7F97B967431BDEEE5D4E41AD6DCCEF81903DAC8C5`, return `SOURCE_CONTEXT_INCOMPLETE_TARGET_CHANGED` unless the launch instruction explicitly authorizes reviewing the changed target.

## Required Method Sequence

REFERENCE-LOAD these method instructions first. Do not APPLY them yet:

- `workflow-deep-thinking`
- `workflow-adversarial-artifact-review`

Before `SOURCE_CONTEXT_READY`, prepare only neutral source-reading lenses. Do not produce findings, verdicts, recommendations, rankings, closure claims, or blast-radius conclusions before source readiness.

Then SOURCE-LOAD the required Orca sources below.

After declaring `SOURCE_CONTEXT_READY`, APPLY `workflow-deep-thinking` to frame the closure question, likely regression surfaces, and decision criteria.

Then APPLY `workflow-adversarial-artifact-review` to produce the findings-first recheck report.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot be applied after `SOURCE_CONTEXT_READY`, return a blocked or advisory-only result. Do not emit formal verdicts, severity authority, readiness claims, validation claims, mandatory remediation, patch queues, executor-ready handoffs, or alignment-complete claims.

## Required Sources

Authority and review-lane sources:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/communication-style.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/retrieval-metadata.md`

Prior review and closure target:

- `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_amendment_adversarial_artifact_review_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`

Patch-basis / blast-radius surfaces:

- `docs/product/data_capture_source_access_boundary_decision_v0.md`
- `docs/product/data_capture_source_access_method_plan_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`
- `docs/product/core_spine_v0_data_capture_context_preservation_note_v0.md`
- `docs/workflows/orca_repo_map_v0.md`
- `.agents/workflow-overlay/source-loading.md`

Immediate amendment trail, read only if needed to verify AR-05 trigger-chain context:

- `docs/product/data_capture_spine_obligation_contract_patch_proposal_v0.md`
- `docs/decisions/data_capture_spine_obligation_contract_patch_proposal_owner_decision_v0.md`

Excluded by default:

- broad `docs/review-outputs/`
- broad `docs/prompts/`
- broad `docs/product/`
- broad `docs/research/`
- `docs/_inbox/`
- raw Reddit JSON or screenshots
- implementation/runtime folders
- external web research

Expand only if a missing source could materially change a closure or blast-radius finding. If expansion would exceed a bounded recheck source pack, report `SOURCE_CONTEXT_INCOMPLETE` with the exact missing source and why it matters.

## Recheck Questions

Attack only these closure and blast-radius questions:

1. **AR-01 closure:** Is Obligation #2 / `access_failed` now anchored to committed, internally consistent source-access boundary and method-plan sources? Does the contract cross-reference `data_capture_source_access_boundary_decision_v0.md` as the controlling boundary basis? Do `open_next` and `stale_if` force reread if the boundary decision or method plan changes?
2. **AR-01 blast radius:** Did anchoring the source-access boundary or method plan introduce new stale next-step language, source-access overclaim, hard-stop weakening, runtime/tooling authorization, legal sufficiency claim, or conflict with the obligation contract?
3. **AR-02 closure:** Does the contract propagation receipt now account for the architecture blueprint and context-preservation note? Are stale blueprint/context-note phrases reconciled or explicitly accounted for? Does the recorded stale-language search cover the relevant surfaces?
4. **AR-02 blast radius:** Did the blueprint/context-note de-staling accidentally promote old design rationale into operative contract authority, weaken ECR/Cleaning/Judgment boundaries, or create a new obligation beyond the accepted PCP package?
5. **AR-03 closure:** Does Obligation #6 now avoid Capture deciding relevance/materiality by using "the Decision Frame caused Capture to seek" or equivalent wording, while preserving Judgment-owned materiality?
6. **AR-04 closure:** Does `orca_repo_map_v0.md` now carry current freshness and the current contract hash `B06BD6722F76D223E7A122B7F97B967431BDEEE5D4E41AD6DCCEF81903DAC8C5`?
7. **AR-05 closure:** Does the `trigger_chain_note` adequately explain the lifecycle-boundary owner/proposal gate versus product-doctrine operative-contract distinction without rewriting historical receipts or creating a new doctrine category?
8. **AR-05 blast radius:** Did the trigger-chain note create contradiction with `.agents/workflow-overlay/source-of-truth.md`, imply approval/readiness/validation, or create a requirement that future artifacts add trigger-chain notes by default?
9. Did any post-review patch create new blocker or major defects in retrieval metadata, source-loading, source hierarchy, propagation receipt, or non-claims?
10. Is another patch required before the amended obligation contract is used for the next Data Capture pressure-test or capture-spine work, or can remaining issues travel as minor/advisory findings?

## Severity And Recommendation

Use these severity labels only:

- `critical`: continued use would likely create false implementation authorization, validation/readiness, ECR/Cleaning/Judgment leakage, source-access hard-stop bypass, or materially corrupt Data Capture obligation discharge.
- `major`: continued use would materially distort future Data Capture work because of source-trace failure, stale lifecycle language, ambiguous operative contract language, weakened boundary specificity, or failed closure of a prior major finding.
- `minor`: wording, retrieval, propagation, or operator-friction issue that should be patched or carried but does not materially distort future Data Capture work if explicitly carried.

These labels are finding priority only. They do not create approval, rejection, readiness, validation, mandatory remediation, or patch authority.

Use exactly one recommendation:

- `closure_confirmed_no_material_regression`
- `closure_confirmed_with_minor_carry`
- `revise_before_next_data_capture_work`
- `blocked_source_context`
- `advisory_only_skill_unavailable`

## Output Report Requirements

Write the full durable report to:

```text
docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_amendment_blast_radius_recheck_v0.md
```

The report must include:

- retrieval header;
- `review_summary` YAML at the top;
- source readiness declaration;
- source-read ledger with dirty/untracked notes;
- review boundary and excluded scope;
- decision criteria;
- closure ledger for AR-01 through AR-05;
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
  report_path: docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_amendment_blast_radius_recheck_v0.md
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
  summary: "Failed to write required report to docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_amendment_blast_radius_recheck_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  next_action: "Resolve report write failure, then rerun the blast-radius recheck prompt."
```

## Hard Boundaries

Do not:

- patch the obligation contract;
- patch source artifacts;
- patch source-loading, repo map, source-access method plan, source-access boundary, ECR, Cleaning, or Judgment docs;
- make an owner decision;
- apply any contract or method patch;
- authorize source-access implementation;
- design ECR, Cleaning, Judgment, source systems, runtime, schemas, tools, dashboards, scrapers, APIs, automation, tests, packages, deployment, commits, pushes, or PRs;
- claim validation, hardening, readiness, buyer proof, product readiness, source-of-truth promotion, implementation authority, or commercial readiness.

Review findings are decision input only. Owner acceptance, patch authorization, source-access implementation, and any runtime work require separate explicit authorization.
