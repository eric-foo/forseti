# Batch 0 Process Pilot

```yaml
retrieval_header_version: 1
artifact_role: Forseti overlay authority
scope: Temporary binding for the four-probe Batch 0 process-improvement evidence pilot and tenth-review owner notification.
use_when:
  - Closing a material adversarial review while the Batch 0 sample is active.
  - Recording or interpreting a Batch 0 probe.
  - Checking the threshold notification and pilot retirement boundary.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/process_improvement_batch0/README.md
  - .agents/workflow-overlay/review-lanes.md
```

## Active pilot rule

The owner activated Batch 0 on 2026-07-11. Until ten valid completion receipts
have landed on `main`, the Chief Architect closing each material adversarial
review must write one review-economics receipt under
`docs/workflows/process_improvement_batch0/review_receipts/` after adjudication.

A completion unit is one unique, schema-valid receipt for one material review
whose Chief Architect adjudication is complete. A review prompt, report, patch,
reviewer verdict, or unadjudicated finding set does not count. Invalid or
duplicated receipts fail visibly and never increment the sample.

The receipt is process-measurement evidence only. It does not change the review
verdict, finding authority, remediation requirement, patch authority, approval,
validation, readiness, model routing, or the Chief Architect's adjudication
ownership.

The other three probes use the ledgers linked from the workflow front door:
deep-thinking retrospective, resident-rule firing, and worktree lifecycle. They
must preserve `unknown` rather than invent outcomes. The worktree probe is
read-only and authorizes no cleanup.

## Threshold and notification

At ten or more valid receipts on `main`, the Batch 0 workflow creates one
deduplicated GitHub issue assigned to and mentioning the repository owner. The
issue asks an agent to synthesize all four probes and inform the owner. A prior
exact-title issue is the durable notification marker; later pushes must not ping
again.

Threshold completion does not authorize Batch 1, doctrine promotion, lesson
installation, process retention, or cleanup. Those remain separate owner
decisions after the synthesis.

## Retirement

After the owner receives the synthesis and decides keep/change/stop, retire this
temporary pilot through a doctrine-change propagation pass. Do not leave the
receipt obligation resident indefinitely.

## Direction Change Propagation

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
