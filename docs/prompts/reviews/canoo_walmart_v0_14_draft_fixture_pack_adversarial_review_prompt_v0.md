# Canoo/Walmart v0.14 Draft Fixture Pack Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial artifact review prompt for the Canoo/Walmart v0.14 draft fixture pack and bounded discovery pointers.
use_when:
  - Reviewing the Canoo/Walmart v0.14 draft fixture pack before any fixture patch, implementation scoping, probe execution, model run, scoring, validation, or proof claim.
  - Checking participant-packet leakage, EvidenceUnit field correctness, facilitator-ledger schema mapping, and blind-judgment adapter boundaries.
  - Deciding whether the draft fixture pack can proceed to owner-authorized patching or remains blocked by artifact defects.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/fixture_authoring_receipt_v0.md
  - docs/research/judgment-spine/cases/canoo-walmart/case_index.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - .agents/workflow-overlay/review-lanes.md
input_hashes:
  docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/fixture_authoring_receipt_v0.md: 8D83BE764BE5BE34127C53FEB94FFF4191CE936524023C1A17EAFB7ED29ACF40
  docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/participant_packet_draft_v0.md: 66A24DF645E1D6592C4F95B30395AAECBAF1B4F126BB6B6E0A7B776B6ECCD997
  docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/evidence_registry_draft_v0.md: 79C22D86FEC835E9FB72682E57FB8F8FB99C382998D5596C0C76BF545478B093
  docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/facilitator_ledger_draft_v0.md: 10E42DEE1B97F11874919E2F59FCD86D9E3ECF6D82100E6CE25D7BF9D5EFD313
  docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/blind_judgement_adapter_note_v0.md: 2B7E0C6438F528736AC634C5ABDCD4C442383F896814A669009898A0CC36660B
  docs/research/judgment-spine/harness/v0_14/index.md: 3453D75546286B7755726076489C8550CB9AD60B53D02AADD1D5B57BE78BE769
  docs/research/judgment-spine/manifest_v0.md: 78B6821DDB9A38382199AEB218E4E68FABB434FDC631B0BA8C1CEC0D635E05F5
  docs/research/judgment-spine/cases/canoo-walmart/case_index.md: 989D3764DB3965E7867B9B3B66F0D5AAB10FBEBA942865D5F6B5449476D0E13E
  docs/prompts/templates/review/adversarial_artifact_review_v0.md: 17188D11F4C151103CC746328D02F0DFC94FCF3AAD3F39714A510CEDBA5A60AA
```

- Status: PROPOSED_PROMPT
- Artifact type: Adversarial artifact review prompt
- Template kind: `adversarial-artifact-review`
- Template source: `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
- Prompt artifact path: `docs/prompts/reviews/canoo_walmart_v0_14_draft_fixture_pack_adversarial_review_prompt_v0.md`
- Required review report path: `docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_v0_14_draft_fixture_pack_adversarial_review_v0.md`
- Output mode: `review-report`
- Reviewer edit permission: read-only, except writing the required review report
- Patch queue authorized: no
- Implementation, runtime, package, test, automation, commit, push, PR, model run, memorization-probe execution, scoring execution, proof-run, product-proof, validation execution, fixture admission, case-report creation, or lesson-promotion authorized: no

## Prompt Author Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus prompt template, review-lane overlay, current Canoo/Walmart draft fixture pack, and current target hashes
  edit_permission: docs-write
  target_scope: Create a read-only adversarial artifact review prompt for the Canoo/Walmart v0.14 draft fixture pack and bounded discovery pointers.
  dirty_state_checked: yes
  blocked_if_missing: no
control_plane_source_state:
  branch: main
  head: a2aebdd
  overlay_sources_modified_or_untracked: yes
  reviewed_targets_untracked: yes
  strict_pass_or_readiness_claimed: no
doctrine_change:
  changes_doctrine: no
  reason: This prompt applies existing Orca review and prompt-orchestration policy without changing it.
```

## Prompt

You are performing a read-only adversarial artifact review for Orca.

Your target is the Canoo/Walmart v0.14 draft fixture pack and its bounded discovery pointers. This is an artifact review lane, not a patch lane, not a fixture-authoring lane, not a harness implementation lane, not an implementation-scoping lane, not a probe-execution lane, not a model-run lane, not a scoring lane, not a validation lane, not a case-continuation lane, not a fresh blind-judgment lane, not a lesson-promotion lane, not a proof-run lane, and not a product-proof lane.

Do not recommend, prescribe, rank, or imply a runtime model for this review lane. Model-family language is allowed only when reviewing the artifact's memorization-probe and quarantine logic.

## Workspace

- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Expected branch: `main`
- Expected HEAD observed by prompt author: `a2aebdd`
- Dirty-state allowance: dirty and untracked Orca docs may exist. The reviewed draft fixture pack, case index, harness index, and manifest files may be untracked. Treat dirty or untracked sources as working artifacts unless an accepted Orca source makes them controlling authority.
- Prompt artifact path: `docs/prompts/reviews/canoo_walmart_v0_14_draft_fixture_pack_adversarial_review_prompt_v0.md`
- Output mode: `review-report`
- Required durable report path: `docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_v0_14_draft_fixture_pack_adversarial_review_v0.md`
- Chat closeout after successful report write: compact `review_summary` YAML from `.agents/workflow-overlay/communication-style.md`

## Review Target

Primary draft fixture pack:

- `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/fixture_authoring_receipt_v0.md`
- `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/participant_packet_draft_v0.md`
- `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/evidence_registry_draft_v0.md`
- `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/facilitator_ledger_draft_v0.md`
- `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/blind_judgement_adapter_note_v0.md`

Bounded discovery-pointer targets:

- `docs/research/judgment-spine/cases/canoo-walmart/case_index.md`
- `docs/research/judgment-spine/harness/v0_14/index.md`
- `docs/research/judgment-spine/manifest_v0.md`

Pre-authoring review source:

- `docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_fixture_admission_scoring_readiness_adversarial_artifact_review_v0.md`

Prompt-author observed SHA256 values:

```yaml
input_hashes:
  fixture_authoring_receipt_v0.md: 8D83BE764BE5BE34127C53FEB94FFF4191CE936524023C1A17EAFB7ED29ACF40
  participant_packet_draft_v0.md: 66A24DF645E1D6592C4F95B30395AAECBAF1B4F126BB6B6E0A7B776B6ECCD997
  evidence_registry_draft_v0.md: 79C22D86FEC835E9FB72682E57FB8F8FB99C382998D5596C0C76BF545478B093
  facilitator_ledger_draft_v0.md: 10E42DEE1B97F11874919E2F59FCD86D9E3ECF6D82100E6CE25D7BF9D5EFD313
  blind_judgement_adapter_note_v0.md: 2B7E0C6438F528736AC634C5ABDCD4C442383F896814A669009898A0CC36660B
  docs/research/judgment-spine/harness/v0_14/index.md: 3453D75546286B7755726076489C8550CB9AD60B53D02AADD1D5B57BE78BE769
  docs/research/judgment-spine/manifest_v0.md: 78B6821DDB9A38382199AEB218E4E68FABB434FDC631B0BA8C1CEC0D635E05F5
  docs/research/judgment-spine/cases/canoo-walmart/case_index.md: 989D3764DB3965E7867B9B3B66F0D5AAB10FBEBA942865D5F6B5449476D0E13E
  docs/prompts/templates/review/adversarial_artifact_review_v0.md: 17188D11F4C151103CC746328D02F0DFC94FCF3AAD3F39714A510CEDBA5A60AA
```

Prompt-author observed git status for reviewed targets:

```yaml
observed_git_status:
  docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/: untracked
  docs/research/judgment-spine/harness/v0_14/index.md: untracked
  docs/research/judgment-spine/manifest_v0.md: untracked
  docs/research/judgment-spine/cases/canoo-walmart/case_index.md: untracked
```

If hashes differ, do not fail automatically. Record the mismatch in the report and decide whether the changed file is still reviewable under the dirty-state allowance. Block only if the mismatch prevents a source-backed review of the commissioned target.

## Review Purpose

Adversarially review whether the Canoo/Walmart v0.14 draft fixture pack and bounded discovery pointers:

1. Satisfy the accepted post-admission authoring move: draft fixture surfaces only, blocked before scoring.
2. Correctly consume the fixture-admission findings FA-01 through FA-09 without silently converting any finding into acceptance, readiness, validation, or scoring authority.
3. Preserve `DRAFT_FIXTURE_PACK_BLOCKED_BEFORE_SCORING` and avoid implying fixture admission, clean blind-run status, memorization-probe pass, score-readiness, or model validation.
4. Keep the participant packet draft free of company names, raw source URLs, source titles, source filenames, actual agreement terms, public-action facts, post-cutoff outcomes, owner-assisted judgment content, reveal readout content, outcome calibration, candidate labels, must-address items, and scoring hints.
5. Handle the v0.14 source-manifest conflict honestly: raw source locators would leak the anonymized case, so participant-safe aliases may be a blocker or adapter need rather than a completed schema solution.
6. Map CW-E01 through CW-E06 toward v0.14 `EvidenceUnit` fields without inventing source-byte hashes, retrieval timestamps, pre-decision authority, or source completeness.
7. Treat CW-P7 as excluded or unresolved participant-facing material unless the reviewed artifacts source-authorize its use.
8. Separate direct Pydantic `FacilitatorLedger` draft fields from protocol fixture metadata such as `case_family`, `decision_shape`, `memorization_probe_required`, and `known_fame_risk`.
9. Use valid v0.14 enum values for band inputs and valid `UnderreachObservability` shape, and clearly mark candidate/unfrozen labels as not score-ready.
10. Preserve FA-05 by keeping `underreach_observability.present: false` as candidate false before any ledger freeze, while checking whether the supporting rationale is sufficiently source-bounded.
11. Avoid implying that second-label audit, ledger freeze, participant packet hash, probe pass, scoring result, failure event, or case report exists.
12. Treat the existing blind LLM answer as user-supplied qualitative material unless a clean harness-format `BlindJudgement` is produced or the owner explicitly accepts a legacy adapter path.
13. Preserve the blind-judgment adapter's ladder-level ambiguity and avoid using the adapter note as a scoreable object.
14. Keep Walmart-specific outcome gaps visible: deployment volume, accepted units, uptime, termination-right exercise, financial exposure at bankruptcy, and protective-term effectiveness remain not established.
15. Avoid strict-claim leakage around acceptance, readiness, validation, implementation authorization, source-of-truth promotion, fixture admission, probe pass, score-readiness, harness superiority, buyer proof, product proof, proof-run status, or lesson transfer.
16. Keep `case_index.md`, `index.md`, and `manifest_v0.md` discovery pointers narrow and non-authorizing.
17. Identify any artifact shape defect that would mislead a later implementation-scoping lane, fixture patch lane, or scoring-readiness route.

## Goal Context To Check

Use this goal context only as review orientation. It is not source authority, validation evidence, readiness, approval, sequencing authority, or edit permission.

```yaml
goal_handoff:
  long_term_goal: Build Orca's Judgment Spine into a disciplined signal-integrity backtest system that distinguishes real corroboration from artificial amplification without overclaiming validation.
  anchor_goal: Review the Canoo/Walmart v0.14 draft fixture pack before any patching, probe execution, model run, scoring, validation, or proof claim.
  success_signal: Reviewer verifies source state, preserves blocked-before-scoring and plumbing-vs-judgment-quality boundaries, avoids wrong-lane contamination, and returns source-backed findings plus a bounded next action.
  status: prompt_author_supplied
selected_next_move:
  source: owner_after_canoo_walmart_draft_fixture_pack_authoring
  move: Run a read-only adversarial artifact review of the Canoo/Walmart v0.14 draft fixture pack.
  output_fit_check: The review identifies blocker or advisory defects in the fixture pack without authorizing implementation, probe execution, model runs, scoring, validation, proof, product proof, or lesson promotion.
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
  if_changed_reason: none
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
12. `.agents/workflow-overlay/product-proof.md`
13. `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
14. `docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_fixture_admission_scoring_readiness_adversarial_artifact_review_v0.md`
15. `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/fixture_authoring_receipt_v0.md`
16. `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/participant_packet_draft_v0.md`
17. `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/evidence_registry_draft_v0.md`
18. `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/facilitator_ledger_draft_v0.md`
19. `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/blind_judgement_adapter_note_v0.md`
20. `docs/research/judgment-spine/cases/canoo-walmart/case_index.md`
21. `docs/research/judgment-spine/harness/v0_14/index.md`
22. `docs/research/judgment-spine/manifest_v0.md`
23. `docs/research/judgment-spine/cases/canoo-walmart/source_packet_v0.md`
24. `docs/research/judgment-spine/cases/canoo-walmart/participant_packet_v0.md`
25. `docs/research/judgment-spine/cases/canoo-walmart/blind_judgments_v0.md`
26. `docs/research/judgment-spine/cases/canoo-walmart/facilitator_ledger_v0.md`
27. `docs/research/judgment-spine/cases/canoo-walmart/outcome_calibration_v0.md`
28. `docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md`
29. `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md`
30. `docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md`
31. `docs/research/judgment-spine/harness/v0_14/blind_judgement_schema_and_harness_protocol.md`
32. `docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md`
33. `docs/research/judgment-spine/harness/v0_14/action_band_mapping_table_numbers.md`
34. `docs/research/judgment-spine/harness/v0_14/action_band_mapping_executable_spec.md`
35. `docs/research/judgment-spine/harness/v0_14/scorer_formula_spec.md`
36. `docs/research/judgment-spine/harness/v0_14/failure_event_log_spec.md`

Optional targeted reads, only if they can materially change a finding:

- `docs/research/judgment-spine/cases/canoo-walmart/safety_receipt_v0.md`
- `docs/research/judgment-spine/cases/canoo-walmart/owner_context_judgments_v0.md`
- `docs/research/judgment-spine/cases/canoo-walmart/pre_reveal_judgment_comparison_v0.md`
- `docs/research/judgment-spine/cases/canoo-walmart/reveal_readout_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_source_packet_safety_adversarial_artifact_review_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_reveal_readout_calibration_gate_adversarial_artifact_review_v0.md`
- `docs/research/judgment-spine/harness/v0_14/proof_and_memory_plan.md`

Do not bulk-read all prompts, all cases, all review outputs, method-validation replays, proof-run packets, `docs/_inbox/`, the full product directory, implementation code, tests, packages, configs, runners, or runtime files by default. If one of those appears necessary, state the exact source gap first and keep the read targeted.

## Review Scope

In scope:

- correctness of the draft fixture pack against the fixture-admission review's next action;
- source-support and internal consistency;
- consumed-goal fit against the anchor goal, success signal, and selected next move;
- draft fixture pack boundary versus runnable fixture, implementation, probe, model run, scoring, validation, or proof;
- participant-facing leakage and zero-spoiler discipline;
- source-manifest aliasing versus raw-locator schema expectations;
- EvidenceUnit conversion, missing fields, hashes, timestamps, pre-decision labels, and CW-P7 exclusion;
- facilitator-ledger Pydantic versus protocol-field separation;
- candidate band inputs, must-address items, underreach observability, leakage notes, spoiler inventory, freeze hash, and second-label audit status;
- blind LLM adapter non-comparability and required `BlindJudgement` field gaps;
- case ID consistency across the draft pack;
- blocked-before-scoring clarity and not-proven boundaries;
- narrowness of `case_index.md`, `index.md`, and `manifest_v0.md` discovery pointers;
- retrieval-header and durable artifact hygiene.

Out of scope:

- implementing the Judgment Harness;
- implementation scoping except to check whether the draft pack overclaims later implementation implications;
- editing participant packets, evidence registries, facilitator ledgers, blind judgments, memorization probe artifacts, scoring results, failure logs, or case reports;
- running probes, model calls, scoring, tests, validation, proof-runs, or runtime workflows;
- collecting new evidence or producing source packets;
- continuing Canoo/Walmart as a case-writing lane;
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
docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_v0_14_draft_fixture_pack_adversarial_review_v0.md
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
  report_path: docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_v0_14_draft_fixture_pack_adversarial_review_v0.md
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
  summary: "Failed to write required report to docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_v0_14_draft_fixture_pack_adversarial_review_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Resolve the report write failure, then rerun the review-report prompt."
```

## Review-Use Boundary

This is a read-only review. Findings and non-findings are decision input only. They are not approval, validation, product proof, mandatory remediation, source-of-truth promotion, fixture admission, probe pass, score-readiness, implementation authorization, lesson promotion, or executor-ready instructions unless a separate authorized Orca decision, patch, validation, or implementation lane accepts them.

Required boundary: plumbing works only; not judgment quality.
