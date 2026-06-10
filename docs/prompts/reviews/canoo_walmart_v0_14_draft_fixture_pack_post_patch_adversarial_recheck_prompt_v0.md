# Canoo/Walmart v0.14 Draft Fixture Pack Post-Patch Adversarial Recheck Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Narrow read-only adversarial recheck prompt for the Canoo/Walmart v0.14 draft fixture pack after the DFP-01 through DFP-05 patch.
use_when:
  - Checking whether the owner-authorized fixture patch closed DFP-01 through DFP-05.
  - Looking only for patch-caused or newly visible blocker/major regressions inside the touched patch scope.
  - Deciding whether the draft pack can proceed to the next non-scoring fixture decision.
authority_boundary: retrieval_only
open_next:
  - docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_v0_14_draft_fixture_pack_adversarial_review_v0.md
  - docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/fixture_authoring_receipt_v0.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - .agents/workflow-overlay/review-lanes.md
input_hashes:
  prior_review_report: 016BD1DF23F0ABDCB0146109E51379D1DA27E77773F8DEFA29790D118161D73F
  fixture_authoring_receipt_v0.md: 2880145A4274BB3C09DDDECD6B607968970BFF6CE2CF68C741CA257326977AF4
  participant_packet_draft_v0.md: 24BA78BB6D3EDAE37222B282C9151CCA140D136894399D45B0F4120135A9E4AE
  evidence_registry_draft_v0.md: 5F8BB241981D7FDB79F78E18BE07E7E52E68B447C51CFDAC688E234B09FC4078
  facilitator_ledger_draft_v0.md: B10C4B7A282CDB72D9320AB7E55FB9ECE7751CC10124A4415856115BE1D6AAC6
  blind_judgement_adapter_note_v0.md: B16206BB5859B61CF20C16112EF9AFE59972F0E4A6E73840241B9BFD6E45EB78
  adversarial_artifact_review_v0.md: 17188D11F4C151103CC746328D02F0DFC94FCF3AAD3F39714A510CEDBA5A60AA
```

- Status: PROPOSED_PROMPT
- Artifact type: Post-patch adversarial recheck prompt
- Template kind: `rerun` / adversarial patch recheck
- Template source: `docs/prompts/templates/review/adversarial_artifact_review_v0.md` plus `.agents/workflow-overlay/prompt-orchestration.md` rerun economy rules
- Prompt artifact path: `docs/prompts/reviews/canoo_walmart_v0_14_draft_fixture_pack_post_patch_adversarial_recheck_prompt_v0.md`
- Required review report path: `docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_v0_14_draft_fixture_pack_post_patch_adversarial_recheck_v0.md`
- Output mode: `review-report`
- Reviewer edit permission: read-only, except writing the required review report
- Patch queue authorized: no
- Full fresh fixture review authorized: no
- Implementation, runtime, package, test, automation, commit, push, PR, model run, memorization-probe execution, scoring execution, proof-run, product-proof, validation execution, fixture admission, case-report creation, or lesson-promotion authorized: no

## Prompt Author Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus prompt/review overlay, prior review report, patched fixture files, and current target hashes
  edit_permission: docs-write
  target_scope: Create a narrow post-patch adversarial recheck prompt for DFP-01 through DFP-05 closure and patch-caused blocker/major regressions.
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
  reason: This prompt applies existing Orca review, rerun, and prompt-orchestration policy without changing it.
```

## Prompt

You are performing a narrow read-only adversarial post-patch recheck for Orca.

Your target is the owner-authorized patch to the Canoo/Walmart v0.14 draft fixture pack after the prior adversarial review `canoo_walmart_v0_14_draft_fixture_pack_adversarial_review_v0.md`.

This is a patch-closure recheck lane, not a full fresh artifact review, not a patch lane, not a fixture-authoring lane, not a harness implementation lane, not an implementation-scoping lane, not a probe-execution lane, not a model-run lane, not a scoring lane, not a validation lane, not a case-continuation lane, not a fresh blind-judgment lane, not a lesson-promotion lane, not a proof-run lane, and not a product-proof lane.

Do not recommend, prescribe, rank, or imply a runtime model for this review lane. Model-family language is allowed only when reviewing the artifact's memorization-probe and quarantine logic.

## Workspace

- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Expected branch: `main`
- Expected HEAD observed by prompt author: `a2aebdd`
- Dirty-state allowance: dirty and untracked Orca docs may exist. The reviewed draft fixture pack, prompt, review report, case index, harness index, and manifest files may be untracked. Treat dirty or untracked sources as working artifacts unless an accepted Orca source makes them controlling authority.
- Prompt artifact path: `docs/prompts/reviews/canoo_walmart_v0_14_draft_fixture_pack_post_patch_adversarial_recheck_prompt_v0.md`
- Output mode: `review-report`
- Required durable report path: `docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_v0_14_draft_fixture_pack_post_patch_adversarial_recheck_v0.md`
- Chat closeout after successful report write: compact `review_summary` YAML from `.agents/workflow-overlay/communication-style.md`

## Review Target

Prior review to recheck:

- `docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_v0_14_draft_fixture_pack_adversarial_review_v0.md`

Patched fixture files:

- `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/fixture_authoring_receipt_v0.md`
- `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/participant_packet_draft_v0.md`
- `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/evidence_registry_draft_v0.md`
- `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/facilitator_ledger_draft_v0.md`
- `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/blind_judgement_adapter_note_v0.md`

Relevant spec controls:

- `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md`
- `docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md`
- `docs/research/judgment-spine/harness/v0_14/blind_judgement_schema_and_harness_protocol.md`
- `docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md`

Prompt-author observed SHA256 values:

```yaml
input_hashes:
  prior_review_report: 016BD1DF23F0ABDCB0146109E51379D1DA27E77773F8DEFA29790D118161D73F
  fixture_authoring_receipt_v0.md: 2880145A4274BB3C09DDDECD6B607968970BFF6CE2CF68C741CA257326977AF4
  participant_packet_draft_v0.md: 24BA78BB6D3EDAE37222B282C9151CCA140D136894399D45B0F4120135A9E4AE
  evidence_registry_draft_v0.md: 5F8BB241981D7FDB79F78E18BE07E7E52E68B447C51CFDAC688E234B09FC4078
  facilitator_ledger_draft_v0.md: B10C4B7A282CDB72D9320AB7E55FB9ECE7751CC10124A4415856115BE1D6AAC6
  blind_judgement_adapter_note_v0.md: B16206BB5859B61CF20C16112EF9AFE59972F0E4A6E73840241B9BFD6E45EB78
  adversarial_artifact_review_v0.md: 17188D11F4C151103CC746328D02F0DFC94FCF3AAD3F39714A510CEDBA5A60AA
```

Prompt-author observed git status for reviewed targets:

```yaml
observed_git_status:
  docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/: untracked
  docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_v0_14_draft_fixture_pack_adversarial_review_v0.md: untracked
```

If hashes differ, do not fail automatically. Record the mismatch in the report and decide whether the changed file is still reviewable under the dirty-state allowance. Block only if the mismatch prevents a source-backed recheck of the commissioned target.

## Recheck Purpose

Adversarially recheck only whether the patch closed the prior findings and whether the patch caused any new blocker/major regression inside the touched scope.

Use the prior review's findings as the frozen unresolved delta:

```yaml
prior_findings_to_recheck:
  DFP-01:
    prior_priority: major
    issue: case_id canoo_walmart_2022_v0_14 contained company names in participant packet frontmatter.
    closure_question: Does the participant-visible case_id/frontmatter now avoid company identity leakage while preserving an explicit internal fixture ID boundary?
  DFP-02:
    prior_priority: major
    issue: compound source IDs on CW-E02/CW-E04/CW-E05/CW-E06 were not defined in v0.14 EvidenceUnit schema.
    closure_question: Are draft EvidenceUnits now single-source, and are downstream ledger/adapter evidence references remapped without stale old IDs?
  DFP-03:
    prior_priority: minor
    issue: committed_at NOT_COMMITTED was not valid ISO-8601 UTC.
    closure_question: Is NOT_COMMITTED removed from the draft schema instance, with committed_at clearly freeze-required rather than fake-filled?
  DFP-04:
    prior_priority: minor
    issue: protocol/Pydantic discrepancies were not surfaced as implementation blockers.
    closure_question: Does the draft now name the protocol/Pydantic reconciliation blocker clearly enough for implementation/freeze lanes?
  DFP-05:
    prior_priority: minor
    issue: underreach_observability rationale lacked evidence-unit citations.
    closure_question: Does the underreach rationale now cite candidate evidence unit IDs and preserve draft-only status?
```

Patch-caused regression scan:

- Check only the touched patch scope.
- Look for blocker/major regressions, not minor/nit issues.
- Newly visible means the patch changed or exposed evidence inside the touched scope enough that the issue could invalidate closure or create serious downstream risk.
- Exclude unrelated structural review, full-artifact review, new broad v0.14 critique, product-proof critique, and pre-existing issues outside the touched scope.

## Required Source Hierarchy

Use this source hierarchy:

1. Current user instruction for the recheck run.
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

Only after `SOURCE_CONTEXT_READY`, APPLY `workflow-deep-thinking` to frame patch-closure failure modes, then APPLY `workflow-adversarial-artifact-review` to produce the recheck.

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
11. `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
12. `docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_v0_14_draft_fixture_pack_adversarial_review_v0.md`
13. `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/fixture_authoring_receipt_v0.md`
14. `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/participant_packet_draft_v0.md`
15. `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/evidence_registry_draft_v0.md`
16. `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/facilitator_ledger_draft_v0.md`
17. `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/blind_judgement_adapter_note_v0.md`
18. `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md`
19. `docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md`
20. `docs/research/judgment-spine/harness/v0_14/blind_judgement_schema_and_harness_protocol.md`
21. `docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md`

Optional targeted reads, only if they can materially change a closure decision:

- `docs/research/judgment-spine/cases/canoo-walmart/source_packet_v0.md`
- `docs/research/judgment-spine/cases/canoo-walmart/participant_packet_v0.md`
- `docs/research/judgment-spine/cases/canoo-walmart/blind_judgments_v0.md`
- `docs/research/judgment-spine/cases/canoo-walmart/facilitator_ledger_v0.md`

Do not bulk-read all prompts, all cases, all review outputs, method-validation replays, proof-run packets, `docs/_inbox/`, the full product directory, implementation code, tests, packages, configs, runners, or runtime files by default. If one of those appears necessary, state the exact source gap first and keep the read targeted.

## In Scope

- DFP-01 through DFP-05 closure status.
- Patch-caused or newly visible blocker/major regressions inside the five patched fixture files.
- Participant-visible frontmatter and participant-facing packet leakage after the alias patch.
- Internal fixture ID versus participant-visible case ID boundary.
- EvidenceUnit single-source shape and stale old evidence ID references.
- Ledger schema-instance placeholder cleanup for `committed_at`.
- Protocol/Pydantic blocker visibility for future implementation/freeze lanes.
- Underreach evidence-unit citation and draft-only status.
- Receipt accuracy about review hash, patch authorization, patched findings, and blocked-before-scoring status.

## Out Of Scope

- Full fresh review of the fixture pack.
- New unrelated critique of v0.14 harness design.
- Minor or nit findings unless they invalidate DFP closure.
- Patch execution or patch queue.
- Implementation, probe execution, model calls, scoring, tests, validation, proof-runs, or runtime workflows.
- Collecting new evidence or producing source packets.
- Running or requesting a new blind judgment.
- Product proof, buyer proof, commercial positioning, or lesson promotion.
- Source collection, scraping, runtime design, schemas as code, packages, tests, automation, deployment, commits, pushes, or PRs.

## Recheck Output Contract

The report must list findings first only if there are unresolved findings or patch-caused blocker/major regressions.

For each unresolved finding or regression include:

- finding id;
- priority: `critical`, `major`, or `minor`;
- phase: `closure` or `regression`;
- location;
- issue;
- evidence;
- impact;
- minimum_closure_condition;
- next_authorized_action;
- recommended correction or advisory remediation direction.

Do not include `patch_queue_entry`. Patch queues are not authorized.

If all prior findings are closed and no patch-caused blocker/major regressions are found, say so directly and list residual not-proven boundaries.

Include a closure table:

| Finding | Closure status | Evidence | Residual risk |
| --- | --- | --- | --- |
| DFP-01 | closed / partially_closed / not_closed / regression | ... | ... |
| DFP-02 | closed / partially_closed / not_closed / regression | ... | ... |
| DFP-03 | closed / partially_closed / not_closed / regression | ... | ... |
| DFP-04 | closed / partially_closed / not_closed / regression | ... | ... |
| DFP-05 | closed / partially_closed / not_closed / regression | ... | ... |

## Report Output

Write the full review report to:

```text
docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_v0_14_draft_fixture_pack_post_patch_adversarial_recheck_v0.md
```

The report must include:

1. Recheck target and purpose.
2. Source context status.
3. Deep-thinking and adversarial-review invocation status.
4. Source-read ledger, including dirty/untracked caveats.
5. Closure table for DFP-01 through DFP-05.
6. Findings-first output only for unresolved closure failures or patch-caused blocker/major regressions.
7. Non-findings or residual risks.
8. Strict-only blockers and not-proven boundaries.
9. Review-use boundary.
10. Next authorized step.

After successfully writing the report, return only a compact chat summary using this YAML shape:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_v0_14_draft_fixture_pack_post_patch_adversarial_recheck_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  summary: "One sentence describing the recheck result."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated:
    - DFP-01
    - DFP-02
  next_action: "One concrete next step"
```

If the required report cannot be written, do not use `report_path`. Return:

```yaml
review_summary:
  status: failed
  review_location: chat_only_current_thread
  recommendation: blocked
  summary: "Failed to write required report to docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_v0_14_draft_fixture_pack_post_patch_adversarial_recheck_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Resolve the report write failure, then rerun the recheck prompt."
```

## Review-Use Boundary

This is a read-only recheck. Findings, non-findings, closure statuses, and recommendations are decision input only. They are not approval, validation, product proof, mandatory remediation, source-of-truth promotion, fixture admission, probe pass, score-readiness, implementation authorization, lesson promotion, or executor-ready instructions unless a separate authorized Orca decision, patch, validation, or implementation lane accepts them.

Required boundary: plumbing works only; not judgment quality.
