# Unity v0.14 Draft Fixture Pack Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial artifact review prompt for the Unity Runtime Fee v0.14 draft fixture pack and bounded discovery pointers.
use_when:
  - Reviewing the Unity v0.14 draft fixture pack before any fixture patch, implementation scoping, probe execution, model run, scoring, validation, or proof claim.
  - Checking participant-packet leakage, EvidenceUnit field correctness, facilitator-ledger schema mapping, and sealed-memo adapter boundaries.
  - Deciding whether the draft fixture pack can proceed to owner-authorized patching or remains blocked by artifact defects.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/fixture_authoring_receipt_v0.md
  - docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - .agents/workflow-overlay/review-lanes.md
input_hashes:
  docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/fixture_authoring_receipt_v0.md: 580290C23AA8B3AF9DB12173BC1E5E5B939D55814CE039B1959AE8842CF842B2
  docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/participant_packet_draft_v0.md: D48825BEA5F619DB8A16CC04064D19ABE3ABF17E55B7E05E1A3F97157D1D215F
  docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/evidence_registry_draft_v0.md: 35A92BCA9134CEE22AD5FA2CD37122BA8AC5C6E5BF91D1BA956F4C8C95FE6E15
  docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/facilitator_ledger_draft_v0.md: 8A92156CF312E8E254378E213F98C4B2D72C6EDB40258E8FDFB70C79A493C3C1
  docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/sealed_memo_adapter_note_v0.md: C97272BF6BCAED5DBE3731F40BF3D49F71EC8C1AA20C23E4F69BB67C085D7FD6
  docs/research/judgment-spine/harness/v0_14/index.md: 59194297235C65E099C356D5141C6B2D64C4E21AECD5A1F13CD364BAD37F7163
  docs/research/judgment-spine/manifest_v0.md: E79CC2FDF22F58059A71BC12116F51DB411689304AE4228C9DB21F92CACEC644
```

- Status: PROPOSED_PROMPT
- Artifact type: Adversarial artifact review prompt
- Template kind: `adversarial-artifact-review`
- Template source: `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
- Prompt artifact path: `docs/prompts/reviews/unity_v0_14_draft_fixture_pack_adversarial_review_prompt_v0.md`
- Required review report path: `docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_draft_fixture_pack_adversarial_review_v0.md`
- Output mode: `review-report`
- Reviewer edit permission: read-only, except writing the required review report
- Patch queue authorized: no
- Implementation, runtime, package, test, automation, commit, push, PR, model run, memorization-probe execution, scoring execution, proof-run, product-proof, validation execution, fixture admission, case-report creation, or lesson-promotion authorized: no

## Prompt Author Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus adversarial review template, draft fixture pack, fixture-authoring prompt, extraction plan, discovery pointers, and current target hashes
  edit_permission: docs-write
  target_scope: Create a read-only adversarial artifact review prompt for the Unity v0.14 draft fixture pack and bounded discovery pointers.
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

Your target is the Unity Runtime Fee v0.14 draft fixture pack and its bounded discovery pointers. This is an artifact review lane, not a patch lane, not a fixture-authoring lane, not a harness implementation lane, not an implementation-scoping lane, not a probe-execution lane, not a model-run lane, not a scoring lane, not a validation lane, not a case-continuation lane, not a fresh blind-judgment lane, not a lesson-promotion lane, not a proof-run lane, and not a product-proof lane.

Do not recommend, prescribe, rank, or imply a model for this review lane. Model-family language is allowed only when reviewing the artifact's memorization-probe and quarantine logic.

## Workspace

- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Expected branch: `main`
- Expected HEAD observed by prompt author: `b7627d3`
- Dirty-state allowance: dirty and untracked Orca docs may exist. The reviewed draft fixture pack, fixture-authoring prompt, extraction plan, harness index, and manifest files may be untracked. Treat dirty or untracked sources as working artifacts unless an accepted Orca source makes them controlling authority.
- Prompt artifact path: `docs/prompts/reviews/unity_v0_14_draft_fixture_pack_adversarial_review_prompt_v0.md`
- Output mode: `review-report`
- Required durable report path: `docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_draft_fixture_pack_adversarial_review_v0.md`
- Chat closeout after successful report write: compact `review_summary` YAML from `.agents/workflow-overlay/communication-style.md`

## Review Target

Primary draft fixture pack:

- `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/fixture_authoring_receipt_v0.md`
- `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/participant_packet_draft_v0.md`
- `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/evidence_registry_draft_v0.md`
- `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/facilitator_ledger_draft_v0.md`
- `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/sealed_memo_adapter_note_v0.md`

Bounded discovery-pointer targets:

- `docs/research/judgment-spine/harness/v0_14/index.md`
- `docs/research/judgment-spine/manifest_v0.md`

Commissioning prompt source:

- `docs/prompts/deep-thinking/judgment_spine_unity_v0_14_fixture_authoring_ca_prompt_v0.md`

Controlling plan source:

- `docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md`

Prompt-author observed SHA256 values:

```yaml
input_hashes:
  fixture_authoring_receipt_v0.md: 580290C23AA8B3AF9DB12173BC1E5E5B939D55814CE039B1959AE8842CF842B2
  participant_packet_draft_v0.md: D48825BEA5F619DB8A16CC04064D19ABE3ABF17E55B7E05E1A3F97157D1D215F
  evidence_registry_draft_v0.md: 35A92BCA9134CEE22AD5FA2CD37122BA8AC5C6E5BF91D1BA956F4C8C95FE6E15
  facilitator_ledger_draft_v0.md: 8A92156CF312E8E254378E213F98C4B2D72C6EDB40258E8FDFB70C79A493C3C1
  sealed_memo_adapter_note_v0.md: C97272BF6BCAED5DBE3731F40BF3D49F71EC8C1AA20C23E4F69BB67C085D7FD6
  docs/research/judgment-spine/harness/v0_14/index.md: 59194297235C65E099C356D5141C6B2D64C4E21AECD5A1F13CD364BAD37F7163
  docs/research/judgment-spine/manifest_v0.md: E79CC2FDF22F58059A71BC12116F51DB411689304AE4228C9DB21F92CACEC644
  docs/prompts/deep-thinking/judgment_spine_unity_v0_14_fixture_authoring_ca_prompt_v0.md: E04DC7C16F733E827709EDEC32CC5BADE6F2F273225916B5F92DC6A3B4FD0E23
  docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md: DC0C9D64312E7A2BC49FA4EE227DD581E43919FBDD93F25AF83E6DFAB9677CE7
```

Prompt-author observed git status for reviewed targets:

```yaml
observed_git_status:
  docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/: untracked
  docs/research/judgment-spine/harness/v0_14/index.md: untracked
  docs/research/judgment-spine/manifest_v0.md: untracked
  docs/prompts/deep-thinking/judgment_spine_unity_v0_14_fixture_authoring_ca_prompt_v0.md: untracked
```

If hashes differ, do not fail automatically. Record the mismatch in the report and decide whether the changed file is still reviewable under the dirty-state allowance. Block only if the mismatch prevents a source-backed review of the commissioned target.

## Review Purpose

Adversarially review whether the Unity v0.14 draft fixture pack and bounded discovery pointers:

1. Satisfy the fixture-authoring prompt's goal, selected next move, required output paths, and required artifact shapes.
2. Preserve the docs-only draft boundary and `DRAFT_FIXTURE_PACK_BLOCKED_BEFORE_SCORING` status.
3. Keep the participant packet draft free of actual outcome, post-cutoff facts, backlash, revision, cancellation, owner blind read, sealed memo recommendation, calibration verdict, reveal lessons, frozen labels, derived floor or ceiling, must-address items, probe status, and fame-risk classification.
4. Keep the participant packet draft useful as a v0.14 participant packet seed without becoming a score-ready packet or claiming a readiness hash.
5. Map EU-01 through EU-08 toward v0.14 `EvidenceUnit` fields without inventing source hashes, retrieval timestamps, pre-decision status, pre-decision basis, or source authority.
6. Handle EU-08 as an adapter/source-visibility gap rather than turning a negative lookup into proof.
7. Separate direct Pydantic `FacilitatorLedger` draft fields from protocol fixture metadata such as `case_family`, `decision_shape`, `memorization_probe_required`, and `known_fame_risk`.
8. Use valid v0.14 enum values for band inputs and `UnderreachObservability.basis`, and clearly mark candidate/unfrozen labels as not score-ready.
9. Avoid implying that second-label audit, ledger freeze, participant packet hash, probe pass, scoring result, failure event, or case report exists.
10. Treat the sealed Unity memo as advisory, baseline-like, or legacy material only unless comparability and required `BlindJudgement` fields are proven.
11. Preserve sealed-memo non-comparability against fresh contestants.
12. Preserve the failure-log versus lesson-promotion boundary and avoid promoted rules or memory claims.
13. Avoid strict-claim leakage around acceptance, readiness, validation, implementation authorization, source-of-truth promotion, fixture admission, probe pass, score-readiness, harness superiority, buyer proof, product proof, proof-run status, or lesson transfer.
14. Keep `index.md` and `manifest_v0.md` discovery pointers narrow and non-authorizing.
15. Identify any artifact shape defect that would mislead a later implementation-scoping lane or fixture patch lane.

## Goal Context To Check

Use this goal context only as review orientation. It is not source authority, validation evidence, readiness, approval, sequencing authority, or edit permission.

```yaml
goal_handoff:
  long_term_goal: Develop Judgment Spine into a durable judgment-improvement layer where real cases can become repeatable, scored, failure-logged learning material without losing spoiler safety, layer boundaries, or non-claims.
  anchor_goal: Define a case-to-v0.14 bridge CA lane that maps existing Judgment Spine case material into the v0.14 Judgment Harness foundation before any harness implementation.
  success_signal: A CA can determine the minimum harness-entry shape for one real case, identify which v0.14 spec files control it, expose missing or unsafe inputs, and name the smallest later implementation scope without authorizing code.
  status: user_stated
selected_next_move:
  source: owner_after_fixture_extraction_review_patch
  move: Author a docs-only Unity v0.14 draft fixture pack from the patched extraction plan, still blocked before scoring.
  output_fit_check: The fixture-authoring lane writes a draft participant packet, draft evidence registry, draft facilitator ledger, sealed-memo adapter note, and fixture authoring receipt that expose exact missing fields and hard gates without authorizing implementation, probe execution, model runs, scoring, validation, proof, product proof, or lesson promotion.
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: goal_handoff.anchor_goal
  current_output_target: selected_next_move.move
  output_fit_check: selected_next_move.output_fit_check
  target_delta_from_prior:
    status: narrowed
    changed_fields: [current_output_target, output_fit_check]
    summary: Shifted from extraction-plan repair to docs-only fixture artifact drafting.
  drift_guard: Do not let draft fixture authoring become implementation, runnable case creation, probe execution, model judging, scoring, validation, product proof, lesson promotion, or harness-superiority proof.
  conflict_behavior: call_out_conflict_before_proceeding
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: yes
  lifecycle_status: active_thread_local
  if_changed_reason: The owner asked to proceed to adversarial artifact review after docs-only draft fixture pack authoring.
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

Only after `SOURCE_CONTEXT_READY`, APPLY `workflow-deep-thinking` to frame the draft-fixture boundary problem, failure modes, and decision criteria, then APPLY `workflow-adversarial-artifact-review` to produce findings.

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
12. `docs/prompts/deep-thinking/judgment_spine_unity_v0_14_fixture_authoring_ca_prompt_v0.md`
13. `docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md`
14. `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/fixture_authoring_receipt_v0.md`
15. `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/participant_packet_draft_v0.md`
16. `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/evidence_registry_draft_v0.md`
17. `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/facilitator_ledger_draft_v0.md`
18. `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/sealed_memo_adapter_note_v0.md`
19. `docs/research/judgment-spine/harness/v0_14/index.md`
20. `docs/research/judgment-spine/manifest_v0.md`
21. `docs/research/judgment-spine/judgment_spine_thesis_v0.md`
22. `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md`
23. `docs/research/judgment-spine/README.md`
24. `docs/workflows/orca_repo_map_v0.md`
25. `docs/research/judgment-spine/cases/unity-runtime-fee/case_index.md`
26. `docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md`
27. `docs/product/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md`
28. `docs/product/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md`
29. `docs/research/judgment-spine/cases/unity-runtime-fee/reveal_readout_v0.md`
30. `docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md`
31. `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md`
32. `docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md`
33. `docs/research/judgment-spine/harness/v0_14/blind_judgement_schema_and_harness_protocol.md`
34. `docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md`
35. `docs/research/judgment-spine/harness/v0_14/action_band_mapping_table_numbers.md`
36. `docs/research/judgment-spine/harness/v0_14/action_band_mapping_executable_spec.md`
37. `docs/research/judgment-spine/harness/v0_14/scorer_formula_spec.md`
38. `docs/research/judgment-spine/harness/v0_14/failure_event_log_spec.md`

Optional targeted reads, only if they can materially change a finding:

- `docs/research/judgment-spine/harness/v0_14/proof_and_memory_plan.md`
- `docs/research/judgment-spine/harness/v0_14/phase_1_infrastructure_architecture.md`
- Daimler fallback files under `docs/research/judgment-spine/cases/daimler-carve-out/`
- `docs/product/core_spine_v0_method_validation_mv04_unity_runtime_fee_replay_v0.md`

Do not bulk-read all prompts, all cases, all review outputs, method-validation replays, proof-run packets, `docs/_inbox/`, the full product directory, implementation code, tests, packages, configs, runners, or runtime files by default. If one of those appears necessary, state the exact source gap first and keep the read targeted.

## Review Scope

In scope:

- correctness of the draft fixture pack against the fixture-authoring prompt;
- source-support and internal consistency;
- consumed-goal fit against the anchor goal, success signal, and selected next move;
- draft fixture pack boundary versus runnable fixture, implementation, probe, model run, scoring, validation, or proof;
- participant-facing leakage and zero-spoiler discipline;
- EvidenceUnit conversion, missing fields, hashes, timestamps, and pre-decision labels;
- facilitator-ledger Pydantic versus protocol-field separation;
- candidate band inputs, must-address items, underreach observability, leakage notes, spoiler inventory, freeze hash, and second-label audit status;
- sealed memo adapter non-comparability and required `BlindJudgement` field gaps;
- case ID consistency across the draft pack;
- blocked-before-scoring clarity and not-proven boundaries;
- narrowness of `index.md` and `manifest_v0.md` discovery pointers;
- retrieval-header and durable artifact hygiene.

Out of scope:

- implementing the Judgment Harness;
- implementation scoping except to check whether the draft pack overclaims later implementation implications;
- editing participant packets, evidence registries, facilitator ledgers, blind judgments, memorization probe artifacts, scoring results, failure logs, or case reports;
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
docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_draft_fixture_pack_adversarial_review_v0.md
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
  report_path: docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_draft_fixture_pack_adversarial_review_v0.md
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
  summary: "Failed to write required report to docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_draft_fixture_pack_adversarial_review_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Resolve the report write failure, then rerun the review-report prompt."
```

## Review-Use Boundary

This is a read-only review. Findings and non-findings are decision input only. They are not approval, validation, product proof, mandatory remediation, source-of-truth promotion, fixture admission, probe pass, score-readiness, implementation authorization, lesson promotion, or executor-ready instructions unless a separate authorized Orca decision, patch, validation, or implementation lane accepts them.
