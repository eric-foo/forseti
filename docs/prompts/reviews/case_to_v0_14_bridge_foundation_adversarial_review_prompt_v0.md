# Case To v0.14 Bridge Foundation Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial artifact review prompt for the Judgment Spine case-to-v0.14 bridge foundation and bounded discovery pointers.
use_when:
  - Reviewing the case-to-v0.14 bridge foundation before a Unity fixture extraction plan, implementation scoping prompt, or harness construction lane.
  - Checking whether the bridge foundation satisfies the consumed goal and success signal without smuggling readiness, validation, implementation, or lesson-promotion claims.
  - Checking whether the Unity recommendation, minimum harness-entry shape, and navigation patches are source-supported and bounded.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - .agents/workflow-overlay/review-lanes.md
```

- Status: PROPOSED_PROMPT
- Artifact type: Adversarial artifact review prompt
- Template kind: `adversarial-artifact-review`
- Template source: `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
- Prompt artifact path: `docs/prompts/reviews/case_to_v0_14_bridge_foundation_adversarial_review_prompt_v0.md`
- Required review report path: `docs/review-outputs/adversarial-artifact-reviews/case_to_v0_14_bridge_foundation_adversarial_review_v0.md`
- Output mode: `review-report`
- Reviewer edit permission: read-only, except writing the required review report
- Patch queue authorized: no
- Implementation, runtime, package, test, automation, commit, push, PR, proof-run, product-proof, or validation execution authorized: no

## Prompt Author Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus adversarial review template, bridge foundation target, navigation pointers, commissioning prompt, and current target hashes
  edit_permission: docs-write
  target_scope: Create a read-only adversarial artifact review prompt for the case-to-v0.14 bridge foundation and bounded discovery pointers.
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

Your target is the Judgment Spine case-to-v0.14 bridge foundation and its bounded discovery pointers. This is an artifact review lane, not a patch lane, not a harness implementation lane, not an implementation scoping lane, not a case-continuation lane, not a lesson-promotion lane, and not a product-proof lane.

## Workspace

- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Expected branch: `main`
- Expected HEAD observed by prompt author: `b7627d3`
- Dirty-state allowance: dirty and untracked Orca docs may exist. The reviewed bridge, prompt, harness index, and manifest files may be untracked. Treat dirty or untracked sources as working artifacts unless an accepted Orca source makes them controlling authority.
- Prompt artifact path: `docs/prompts/reviews/case_to_v0_14_bridge_foundation_adversarial_review_prompt_v0.md`
- Output mode: `review-report`
- Required durable report path: `docs/review-outputs/adversarial-artifact-reviews/case_to_v0_14_bridge_foundation_adversarial_review_v0.md`
- Chat closeout after successful report write: compact `review_summary` YAML from `.agents/workflow-overlay/communication-style.md`

## Review Target

Primary target:

- `docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md`

Bounded discovery-pointer targets:

- `docs/research/judgment-spine/harness/v0_14/index.md`
- `docs/research/judgment-spine/manifest_v0.md`

Commissioning prompt source:

- `docs/prompts/deep-thinking/judgment_spine_case_to_v0_14_bridge_ca_prompt_v0.md`

Prompt-author observed SHA256 values:

```yaml
input_hashes:
  docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md: 730983118F4280EC6015872F6CD17D77BB3E18DF37BFD14F4DDC60CE1C8DED79
  docs/research/judgment-spine/harness/v0_14/index.md: 5178403E30E89884ED2C7D206105FB403F516FC7AC5479AB5452D36FF161CCE6
  docs/research/judgment-spine/manifest_v0.md: C5C0A3E0E1CDE39F14546961D12C325FEFB01C7D2E5C2DCB5C183409F91EF1D3
  docs/prompts/deep-thinking/judgment_spine_case_to_v0_14_bridge_ca_prompt_v0.md: 6484400332D128D69AFEE7852837A0F7E7DF53F333497E2C5592199099314294
```

Prompt-author observed git status for reviewed targets:

```yaml
observed_git_status:
  docs/prompts/deep-thinking/judgment_spine_case_to_v0_14_bridge_ca_prompt_v0.md: untracked
  docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md: untracked
  docs/research/judgment-spine/harness/v0_14/index.md: untracked
  docs/research/judgment-spine/manifest_v0.md: untracked
```

If hashes differ, do not fail automatically. Record the mismatch in the report and decide whether the changed file is still reviewable under the dirty-state allowance. Block only if the mismatch prevents a source-backed review of the commissioned target.

## Review Purpose

Adversarially review whether the bridge foundation and bounded discovery pointers:

1. Satisfy the consumed goal and success signal from the commissioning prompt.
2. Correctly turn the operating-contract and v0.14 spec context into a non-implementation bridge foundation, not a direct harness-build route.
3. Justify `Unity Runtime Fee` as the recommended first bridge candidate against Milwaukee and Daimler for the right reasons, not merely because Unity has the most complete prose.
4. Define the minimum harness-entry shape consistently with the v0.14 specs for participant packets, evidence units, facilitator ledgers, frozen band labels, blind judgments, memorization probes, scoring results, and failure events.
5. Preserve the parent Judgment Spine versus v0.14 harness boundary, including case-learning artifacts, revealed calibration material, reusable lessons, and parent-only context.
6. Preserve spoiler, reveal, leakage, and contamination boundaries, especially for Unity's revealed source-to-memo-to-calibration chain.
7. Separate failure logging from lesson promotion without creating memory rules, doctrine, or reusable lessons by review implication.
8. Expose missing, unsafe, contaminated, unindexed, or not-proven inputs instead of treating them as hidden readiness.
9. Avoid strict-claim leakage around acceptance, readiness, validation, implementation authorization, source-of-truth promotion, harness superiority, buyer proof, product proof, or proof-run status.
10. Keep the `index.md` and `manifest_v0.md` discovery pointers narrow and non-authorizing.

## Goal Context To Check

Use this goal context only as review orientation. It is not source authority, validation evidence, readiness, approval, sequencing authority, or edit permission.

```yaml
goal_handoff:
  long_term_goal: Develop Judgment Spine into a durable judgment-improvement layer where real cases can become repeatable, scored, failure-logged learning material without losing spoiler safety, layer boundaries, or non-claims.
  anchor_goal: Define a case-to-v0.14 bridge CA lane that maps existing Judgment Spine case material into the v0.14 Judgment Harness foundation before any harness implementation.
  success_signal: A CA can determine the minimum harness-entry shape for one real case, identify which v0.14 spec files control it, expose missing or unsafe inputs, and name the smallest later implementation scope without authorizing code.
  status: user_stated
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: goal_handoff.anchor_goal
  output_fit_check: goal_handoff.success_signal
  target_delta_from_prior:
    status: changed
    changed_fields: [anchor_goal, success_signal]
    summary: Shifted from operating-contract completion to a case-to-v0.14 harness foundation bridge.
  drift_guard: Do not turn the bridge lane into harness implementation, broad architecture planning, or another bespoke case-note continuation.
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

Only after `SOURCE_CONTEXT_READY`, APPLY `workflow-deep-thinking` to frame the bridge-boundary problem, failure modes, and decision criteria, then APPLY `workflow-adversarial-artifact-review` to produce findings.

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
12. `docs/prompts/deep-thinking/judgment_spine_case_to_v0_14_bridge_ca_prompt_v0.md`
13. `docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md`
14. `docs/research/judgment-spine/judgment_spine_thesis_v0.md`
15. `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md`
16. `docs/research/judgment-spine/README.md`
17. `docs/research/judgment-spine/manifest_v0.md`
18. `docs/workflows/orca_repo_map_v0.md`
19. `docs/research/judgment-spine/harness/v0_14/index.md`
20. `docs/research/judgment-spine/harness/v0_14/judgement_spine_thesis.md`
21. `docs/research/judgment-spine/harness/v0_14/judgement_harness_strategy.md`
22. `docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md`
23. `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md`
24. `docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md`
25. `docs/research/judgment-spine/harness/v0_14/action_band_mapping_table_numbers.md`
26. `docs/research/judgment-spine/harness/v0_14/action_band_mapping_executable_spec.md`
27. `docs/research/judgment-spine/harness/v0_14/scorer_formula_spec.md`
28. `docs/research/judgment-spine/harness/v0_14/blind_judgement_schema_and_harness_protocol.md`
29. `docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md`
30. `docs/research/judgment-spine/harness/v0_14/failure_event_log_spec.md`
31. `docs/research/judgment-spine/harness/v0_14/proof_and_memory_plan.md`
32. `docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/case_index.md`
33. `docs/research/judgment-spine/cases/unity-runtime-fee/case_index.md`

Then check whether these Daimler candidate files exist and read them if present:

34. `docs/research/judgment-spine/cases/daimler-carve-out/case_02_preflight_v0.md`
35. `docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md`
36. `docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md`

Optional targeted reads, only if they can materially change a finding:

- `docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/reveal_readout_v0.md`
- `docs/research/judgment-spine/cases/unity-runtime-fee/reveal_readout_v0.md`
- `docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md`
- `docs/product/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md`
- `docs/product/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md`
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `docs/research/judgment-spine/harness/v0_14/phase_1_infrastructure_architecture.md`
- `docs/research/judgment-spine/harness/v0_14/changelog.md`

Do not bulk-read all prompts, all cases, all review outputs, method-validation replays, proof-run packets, `docs/_inbox/`, the full product directory, or implementation code by default. If one of those appears necessary, state the exact source gap first and keep the read targeted.

## Review Scope

In scope:

- correctness of the bridge foundation against its CA prompt;
- source-support and internal consistency;
- consumed-goal fit against the anchor goal and success signal;
- Unity versus Milwaukee versus Daimler candidate reasoning;
- minimum harness-entry shape versus v0.14 specs;
- parent Judgment Spine versus v0.14 harness separation;
- spoiler, reveal, leakage, contamination, and participant/facilitator boundary handling;
- failure logging versus lesson promotion;
- non-claims and strict-claim hygiene;
- reviewability and future fixture-extraction usability;
- narrowness of `index.md` and `manifest_v0.md` discovery pointers;
- retrieval-header and durable artifact hygiene.

Out of scope:

- implementing the Judgment Harness;
- implementation scoping except to check whether the bridge overclaims the later smallest implementation implication;
- broad Judgment Spine architecture planning;
- continuing Milwaukee, Unity, or Daimler as a case-writing lane;
- running or requesting a blind judgment;
- collecting new evidence or producing source packets;
- product proof, buyer proof, or commercial positioning;
- source collection, scraping, runtime design, schemas as code, packages, tests, automation, deployment, commits, pushes, or PRs;
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
docs/review-outputs/adversarial-artifact-reviews/case_to_v0_14_bridge_foundation_adversarial_review_v0.md
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
  report_path: docs/review-outputs/adversarial-artifact-reviews/case_to_v0_14_bridge_foundation_adversarial_review_v0.md
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
  summary: "Failed to write required report to docs/review-outputs/adversarial-artifact-reviews/case_to_v0_14_bridge_foundation_adversarial_review_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Resolve the report write failure, then rerun the review-report prompt."
```

## Review-Use Boundary

This is a read-only review. Findings and non-findings are decision input only. They are not approval, validation, product proof, mandatory remediation, source-of-truth promotion, implementation authorization, or executor-ready instructions unless a separate authorized Orca decision, patch, validation, or implementation lane accepts them.
