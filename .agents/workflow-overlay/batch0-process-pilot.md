# Batch 0 Process Pilot

```yaml
retrieval_header_version: 1
artifact_role: Forseti overlay authority
scope: Retired binding and final disposition for the four-probe Batch 0 process-improvement evidence pilot.
use_when:
  - Interpreting preserved Batch 0 evidence or its keep/stop decisions.
  - Confirming that the temporary receipt and notification machinery are retired.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/process_improvement_batch0/README.md
  - .agents/workflow-overlay/review-lanes.md
```

## Retired pilot record

The owner activated Batch 0 on 2026-07-11. During the pilot, a material
adversarial review counted only when its Chief Architect adjudication was
followed by one valid review-economics receipt under
`docs/workflows/process_improvement_batch0/review_receipts/`.

A completion unit is one unique, schema-valid receipt for one material review
whose Chief Architect adjudication is complete. A review prompt, report, patch,
reviewer verdict, or unadjudicated finding set does not count. Invalid or
duplicated receipts fail visibly and never increment the sample.

The receipt is process-measurement evidence only. It does not change the review
verdict, finding authority, remediation requirement, patch authority, approval,
validation, readiness, model routing, or the Chief Architect's adjudication
ownership.

The other three probes used the ledgers linked from the workflow front door:
deep-thinking retrospective, resident-rule firing, and worktree lifecycle. They
preserved `unknown` rather than inventing outcomes. The worktree probe was
read-only and authorized no cleanup.

## Historical threshold and notification

The threshold was reached and the one-time owner notification was delivered as
GitHub issue #1012. A final pre-retirement tracker run against `main` observed
13 valid receipts and no schema errors.

Threshold completion does not authorize Batch 1, doctrine promotion, lesson
installation, process retention, or cleanup. Those remain separate owner
decisions after the synthesis.

## Final disposition

- **Keep:** the existing selective adversarial-review practice and the read-only
  lifecycle classifier in `.github/scripts/lane-health-check.ps1`.
- **Stop:** the per-review receipt obligation, tracker, CI validation, owner
  notifier, unfinished deep-thinking retrospective, and standing resident-rule
  sample.
- **Preserve:** all receipts, reports, ledgers, and historical prompts.

`retired` on 2026-07-17. No replacement measurement, review layer, sampling
rule, automatic cleanup, lesson promotion, or later batch is authorized.

## Direction Change Propagation

### Activation record (historical)

```yaml
direction_change_propagation:
  doctrine_changed: >
    A temporary four-probe process-improvement pilot is active. The next ten
    material adversarial reviews count only through unique, valid,
    CA-adjudicated economics receipts; the tenth valid receipt on main triggers
    one deduplicated owner-assigned GitHub issue. The other probes start as
    evidence ledgers with honest unknowns. Threshold completion authorizes only
    owner synthesis, not later process changes.
  trigger: workflow_authority
  related_triggers:
    - review_authority
    - output_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - .agents/workflow-overlay/batch0-process-pilot.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/review-lanes.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/process_improvement_batch0/README.md
    - .github/scripts/batch0_process_tracker.py
    - .github/workflows/batch0-owner-notify.yml
    - .github/workflows/ci.yml
    - docs/prompts/reviews/batch0_process_pilot_implementation_adversarial_review_prompt_v0.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/validation-gates.md
      reason: The dedicated workflow validates the temporary receipt schema; no permanent universal validation gate is added.
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: The receipt is written by CA adjudication closeout, not by the reviewer prompt or report.
    - path: .agents/workflow-overlay/source-loading.md
      reason: The overlay README and workflow front door provide the bounded route; no global source pack changes.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: No new top-level area or product/harness organization; a one-file recent-change note records the temporary route.
  stale_language_search: >
    rg -n -i "Batch 0|review-economics receipt|process-economics receipt|ten valid|tenth"
    .agents docs .github --glob '*.md' --glob '*.py' --glob '*.yml' --glob '*.json'
  stale_language_search_result: >
    Executed 2026-07-11. Live hits are the new pilot owner, its review-lanes
    pointer, workflow records, validator, and notification workflow. Other
    "Batch 0" hits are historical product/rebrand records with different scope.
  non_claims:
    - not validation or readiness
    - not a review verdict or approval
    - not runtime model routing
    - not proof that any measured process improves outcomes
    - not worktree cleanup authority
```

### Retirement record

```yaml
direction_change_propagation:
  doctrine_changed: >
    Batch 0 is retired after 13 valid receipts and owner synthesis: the existing
    review practice and read-only lifecycle classifier remain, while every
    temporary receipt, notification, and unfinished sampling obligation ends.
  trigger: workflow_authority
  related_triggers:
    - review_authority
    - validation_philosophy
    - lifecycle_boundary
  controlling_sources_updated:
    - .agents/workflow-overlay/batch0-process-pilot.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/review-lanes.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/repo_map_recent_changes/batch0_process_pilot_v0.md
    - docs/workflows/process_improvement_batch0/README.md
    - docs/workflows/process_improvement_batch0/deep_thinking_benchmark_v0.md
    - docs/workflows/process_improvement_batch0/resident_rule_firing_audit_v0.md
    - docs/workflows/process_improvement_batch0/worktree_lifecycle_audit_v0.md
    - docs/workflows/process_improvement_batch0/review_receipts/README.md
    - .github/workflows/ci.yml
    - docs/prompts/reviews/batch0_process_pilot_implementation_adversarial_review_prompt_v0.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/validation-gates.md
      reason: Temporary CI steps are removed; no standing validation rule changes.
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: Pilot retirement changes no prompt contract.
    - path: .agents/workflow-overlay/source-loading.md
      reason: Existing historical retrieval routes remain sufficient.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: No top-level area or active route changed.
    - path: docs/prompts/reviews/batch0_process_pilot_implementation_adversarial_review_prompt_v0.md
      reason: Historical commissioning input remains preserved verbatim.
  stale_language_search: >
    rg -n -i "Batch 0|review-economics receipt|process-economics receipt|ten valid|tenth"
    .agents docs .github --glob "*.md" --glob "*.py" --glob "*.yml" --glob "*.json"
  stale_language_search_result: >
    Executed 2026-07-17. Remaining hits are retired authority, preserved
    evidence, or historical records; no live obligation or notifier remains.
  non_claims:
    - not validation or readiness
    - not proof of review causality or quantified return on effort
    - not a conclusion about deep-thinking method value
    - not worktree cleanup authority
    - not authorization for replacement behavior or a later batch
```
