# Unity v0.14 Fixture Extraction Plan Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial artifact review prompt for the Unity Runtime Fee v0.14 fixture extraction plan and bounded discovery pointers.
use_when:
  - Reviewing the Unity v0.14 fixture extraction plan before patching, implementation scoping, probe execution, scoring, or fixture creation.
  - Checking whether the plan stays plan-only and preserves participant/facilitator/parent/excluded material boundaries.
  - Checking whether Unity probe risk, sealed-memo contamination, leakage audit mapping, required v0.14 fields, and Daimler fallback are source-supported and bounded.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - .agents/workflow-overlay/review-lanes.md
```

- Status: PROPOSED_PROMPT
- Artifact type: Adversarial artifact review prompt
- Template kind: `adversarial-artifact-review`
- Template source: `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
- Prompt artifact path: `docs/prompts/reviews/unity_v0_14_fixture_extraction_plan_adversarial_review_prompt_v0.md`
- Required review report path: `docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_fixture_extraction_plan_adversarial_review_v0.md`
- Output mode: `review-report`
- Reviewer edit permission: read-only, except writing the required review report
- Patch queue authorized: no
- Implementation, runtime, package, test, automation, commit, push, PR, model run, memorization-probe execution, scoring execution, proof-run, product-proof, validation execution, fixture creation, participant-packet creation, evidence-registry creation, facilitator-ledger creation, blind-judgment creation, failure-log creation, or lesson-promotion authorized: no

## Prompt Author Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus adversarial review template, Unity extraction plan target, discovery pointers, commissioning prompt, and current target hashes
  edit_permission: docs-write
  target_scope: Create a read-only adversarial artifact review prompt for the Unity v0.14 fixture extraction plan and bounded discovery pointers.
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

Your target is the Unity Runtime Fee v0.14 fixture extraction plan and its bounded discovery pointers. This is an artifact review lane, not a patch lane, not a harness implementation lane, not an implementation-scoping lane, not a fixture-creation lane, not a probe-execution lane, not a scoring lane, not a case-continuation lane, not a fresh blind-judgment lane, not a lesson-promotion lane, not a proof-run lane, and not a product-proof lane.

Do not recommend, prescribe, rank, or imply a model for this review lane. Model-family language is allowed only when reviewing the artifact's memorization-probe and quarantine logic.

## Workspace

- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Expected branch: `main`
- Expected HEAD observed by prompt author: `b7627d3`
- Dirty-state allowance: dirty and untracked Orca docs may exist. The reviewed extraction plan, commissioning prompt, harness index, and manifest files may be untracked. Treat dirty or untracked sources as working artifacts unless an accepted Orca source makes them controlling authority.
- Prompt artifact path: `docs/prompts/reviews/unity_v0_14_fixture_extraction_plan_adversarial_review_prompt_v0.md`
- Output mode: `review-report`
- Required durable report path: `docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_fixture_extraction_plan_adversarial_review_v0.md`
- Chat closeout after successful report write: compact `review_summary` YAML from `.agents/workflow-overlay/communication-style.md`

## Review Target

Primary target:

- `docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md`

Bounded discovery-pointer targets:

- `docs/research/judgment-spine/harness/v0_14/index.md`
- `docs/research/judgment-spine/manifest_v0.md`

Commissioning prompt source:

- `docs/prompts/deep-thinking/judgment_spine_unity_v0_14_fixture_extraction_plan_ca_prompt_v0.md`

Prompt-author observed SHA256 values:

```yaml
input_hashes:
  docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md: F0DA91385F918F855F7DB6BA84AAA3C020AA4F711BD75450D681F829EC016D0F
  docs/research/judgment-spine/harness/v0_14/index.md: 4DB97DB3D561368CF5E780E4CF3F8A6E9053F591C23BDA918302CD2A996C6351
  docs/research/judgment-spine/manifest_v0.md: 4228C88FC32A33F2E1C5123997DB3A301E4A7000D82043CAB1BB3ADBB796766E
  docs/prompts/deep-thinking/judgment_spine_unity_v0_14_fixture_extraction_plan_ca_prompt_v0.md: 05140F3FDBF89BD97377610CA8C9A6CDD15D602BFAB41B2CA19C40181D8C37F9
```

Prompt-author observed git status for reviewed targets:

```yaml
observed_git_status:
  docs/prompts/deep-thinking/judgment_spine_unity_v0_14_fixture_extraction_plan_ca_prompt_v0.md: untracked
  docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md: untracked
  docs/research/judgment-spine/harness/v0_14/index.md: untracked
  docs/research/judgment-spine/manifest_v0.md: untracked
```

If hashes differ, do not fail automatically. Record the mismatch in the report and decide whether the changed file is still reviewable under the dirty-state allowance. Block only if the mismatch prevents a source-backed review of the commissioned target.

## Review Purpose

Adversarially review whether the Unity extraction plan and bounded discovery pointers:

1. Satisfy the commissioning prompt's goal, selected next move, and required output shape.
2. Stay a docs-only extraction plan rather than becoming a participant packet, evidence registry, facilitator ledger, blind judgment, memorization probe artifact, scoring result, failure log, case report, proof artifact, or implementation scope.
3. Correctly classify Unity material as participant-facing candidate, facilitator-only, parent-only, or excluded.
4. Keep revealed, outcome, owner-read, sealed-memo conclusion, calibration, lesson, post-cutoff, and product-proof material out of participant-facing surfaces.
5. Map EU-01 through EU-08 toward v0.14 EvidenceUnit fields without inventing hashes, timestamps, retrieval timestamps, pre-decision status, or source authority.
6. Correctly identify facilitator-ledger work that must be operator-authored later, including frozen band inputs, second-label audit, must-address items, underreach observability, leakage audit, `decision_shape`, freeze hash, and committed timestamp.
7. Map leakage and spoiler controls into v0.14 facilitator-ledger fields without inventing a standalone v0.14 leakage artifact.
8. Make the memorization-probe gate hard enough for pass, fail, and ambiguous outcomes, including contestant/model-family quarantine.
9. Treat the sealed Unity memo as advisory, baseline-like, or legacy existing judgment material unless comparability and required BlindJudgement fields are proven.
10. Preserve the failure-log versus lesson-promotion boundary and avoid promoted rules or memory claims.
11. Define Daimler fallback criteria without accepting Daimler into manifest inventory, proving Daimler probe safety, or turning the review into a Daimler case lane.
12. Avoid strict-claim leakage around acceptance, readiness, validation, implementation authorization, source-of-truth promotion, fixture admission, probe pass, score-readiness, harness superiority, buyer proof, product proof, proof-run status, or lesson transfer.
13. Keep the `index.md` and `manifest_v0.md` discovery pointers narrow and non-authorizing.

## Goal Context To Check

Use this goal context only as review orientation. It is not source authority, validation evidence, readiness, approval, sequencing authority, or edit permission.

```yaml
goal_handoff:
  long_term_goal: Develop Judgment Spine into a durable judgment-improvement layer where real cases can become repeatable, scored, failure-logged learning material without losing spoiler safety, layer boundaries, or non-claims.
  anchor_goal: Define a case-to-v0.14 bridge CA lane that maps existing Judgment Spine case material into the v0.14 Judgment Harness foundation before any harness implementation.
  success_signal: A CA can determine the minimum harness-entry shape for one real case, identify which v0.14 spec files control it, expose missing or unsafe inputs, and name the smallest later implementation scope without authorizing code.
  status: user_stated
selected_next_move:
  source: incremental-planning
  move: Create a docs-only Unity v0.14 fixture extraction plan with a hard memorization-probe gate and explicit Daimler fallback decision.
  output_fit_check: The plan maps Unity's source packet into participant-packet extraction boundaries, evidence-registry conversion, facilitator-ledger work queue, leakage-audit fields, required decision_shape, sealed-memo contamination handling, parent-only exclusions, and a Daimler fallback trigger without authorizing implementation or scoring.
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: goal_handoff.anchor_goal
  current_output_target: selected_next_move.move
  output_fit_check: selected_next_move.output_fit_check
  target_delta_from_prior:
    status: narrowed
    changed_fields: [current_output_target, output_fit_check]
    summary: Shifted from bridge foundation completion to a concrete Unity fixture extraction plan before implementation.
  drift_guard: Do not let Unity fixture extraction planning become harness implementation, actual fixture creation, blind judgment execution, scoring, product proof, or lesson promotion.
  conflict_behavior: call_out_conflict_before_proceeding
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: yes
  lifecycle_status: active_thread_local
  if_changed_reason: The owner accepted the incremental next move after the bridge foundation patch.
```

Before producing findings, state in working notes whether the reviewed artifacts still fit the `anchor_goal`, `success_signal`, and `selected_next_move.output_fit_check`. If they do not, report a blocking finding.

## Required Source Hierarchy

Use this source hierarchy:

1. Current user instruction for the review run.
2. Orca `AGENTS.md`.
3. `.agents/workflow-overlay/`.
4. Orca docs under `docs/`, when they do not conflict with the overlay.
5. Reusable `agent-workflow` skills as mechanics only.

Do not import `jb` rules, paths, handoffs, lifecycle mechanics, product policy, validation habits, model routing, or templates as Orca authority.

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

Only after `SOURCE_CONTEXT_READY`, APPLY `workflow-deep-thinking` to frame the plan-versus-fixture boundary problem, failure modes, and decision criteria, then APPLY `workflow-adversarial-artifact-review` to produce findings.

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
12. `docs/prompts/deep-thinking/judgment_spine_unity_v0_14_fixture_extraction_plan_ca_prompt_v0.md`
13. `docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md`
14. `docs/research/judgment-spine/harness/v0_14/index.md`
15. `docs/research/judgment-spine/manifest_v0.md`
16. `docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md`
17. `docs/review-outputs/adversarial-artifact-reviews/case_to_v0_14_bridge_foundation_adversarial_review_v0.md`
18. `docs/research/judgment-spine/judgment_spine_thesis_v0.md`
19. `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md`
20. `docs/research/judgment-spine/README.md`
21. `docs/workflows/orca_repo_map_v0.md`
22. `docs/research/judgment-spine/cases/unity-runtime-fee/case_index.md`
23. `docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md`
24. `docs/product/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md`
25. `docs/product/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md`
26. `docs/research/judgment-spine/cases/unity-runtime-fee/reveal_readout_v0.md`
27. `docs/research/judgment-spine/harness/v0_14/judgement_spine_thesis.md`
28. `docs/research/judgment-spine/harness/v0_14/judgement_harness_strategy.md`
29. `docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md`
30. `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md`
31. `docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md`
32. `docs/research/judgment-spine/harness/v0_14/action_band_mapping_table_numbers.md`
33. `docs/research/judgment-spine/harness/v0_14/action_band_mapping_executable_spec.md`
34. `docs/research/judgment-spine/harness/v0_14/scorer_formula_spec.md`
35. `docs/research/judgment-spine/harness/v0_14/blind_judgement_schema_and_harness_protocol.md`
36. `docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md`
37. `docs/research/judgment-spine/harness/v0_14/failure_event_log_spec.md`
38. `docs/research/judgment-spine/harness/v0_14/proof_and_memory_plan.md`

Then check whether these Daimler fallback files exist and read them if present:

39. `docs/research/judgment-spine/cases/daimler-carve-out/case_02_preflight_v0.md`
40. `docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md`
41. `docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md`

Optional targeted reads, only if they can materially change a finding:

- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `docs/research/judgment-spine/harness/v0_14/phase_1_infrastructure_architecture.md`
- `docs/research/judgment-spine/harness/v0_14/changelog.md`
- `docs/product/core_spine_v0_method_validation_mv04_unity_runtime_fee_replay_v0.md`

Do not bulk-read all prompts, all cases, all review outputs, method-validation replays, proof-run packets, `docs/_inbox/`, the full product directory, implementation code, tests, packages, configs, runners, or runtime files by default. If one of those appears necessary, state the exact source gap first and keep the read targeted.

## Review Scope

In scope:

- correctness of the extraction plan against its CA prompt;
- source-support and internal consistency;
- consumed-goal fit against the anchor goal, success signal, and selected next move;
- plan-only boundary versus actual fixture creation;
- participant-facing, facilitator-only, parent-only, and excluded material classification;
- Unity spoiler, reveal, leakage, contamination, source-packet, sealed-memo, and outcome-calibration boundaries;
- EvidenceUnit conversion plan for EU-01 through EU-08;
- facilitator-ledger work queue and required v0.14 fields;
- leakage-audit field mapping;
- memorization-probe gate and model-family quarantine handling;
- sealed memo comparability and contamination handling;
- Daimler fallback criteria;
- failure logging versus lesson promotion;
- non-claims and strict-claim hygiene;
- reviewability and future implementation-scoping safety;
- narrowness of `index.md` and `manifest_v0.md` discovery pointers;
- retrieval-header and durable artifact hygiene.

Out of scope:

- implementing the Judgment Harness;
- implementation scoping except to check whether the plan overclaims later implementation implications;
- creating or editing participant packets, safety receipts, evidence registries, facilitator ledgers, blind judgments, memorization probe artifacts, scoring results, failure logs, or case reports;
- running probes, model calls, scoring, tests, validation, proof-runs, or runtime workflows;
- collecting new evidence or producing source packets;
- continuing Unity or Daimler as a case-writing lane;
- running or requesting a new blind judgment;
- product proof, buyer proof, commercial positioning, or lesson promotion;
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
docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_fixture_extraction_plan_adversarial_review_v0.md
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
  report_path: docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_fixture_extraction_plan_adversarial_review_v0.md
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
  summary: "Failed to write required report to docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_fixture_extraction_plan_adversarial_review_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Resolve the report write failure, then rerun the review-report prompt."
```

## Review-Use Boundary

This is a read-only review. Findings and non-findings are decision input only. They are not approval, validation, product proof, mandatory remediation, source-of-truth promotion, fixture admission, probe pass, score-readiness, implementation authorization, lesson promotion, or executor-ready instructions unless a separate authorized Orca decision, patch, validation, or implementation lane accepts them.
