# Process Improvement Batch 0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Retired evidence record and final keep/stop disposition for the four Batch 0 probes.
use_when:
  - Interpreting the preserved Batch 0 receipts and probe ledgers.
  - Checking what ended at retirement and what remained unchanged.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/review-lanes.md
  - docs/workflows/process_improvement_batch0/review_receipts/README.md
```

## Operating state

- `pilot_status`: `retired`
- `activated`: `2026-07-11`
- `retired`: `2026-07-17`
- `review_sample_target`: `10`
- `final_valid_receipts_observed`: `13`
- `threshold_notification`: GitHub issue #1012
- `replacement_behavior_authorized`: `no`

Batch 0 was a measurement batch, not a review layer. Its records remain
available for interpretation, but no future work unit owes a Batch 0 receipt,
ledger update, counter run, or notification check.

## Probe 1 — adversarial-review economics

The final tracker run observed 13 valid receipts. The first 12 synthesized
receipts recorded 23 accepted net-new material findings and 11 decision changes.
Cost evidence was weak because 11 of 12 recorded `turn_count: unknown`, and
report length was only a rough proxy. Keep the existing selective review
practice; stop the receipt obligation, tracker, CI steps, and notifier. Make no
quantitative return-on-effort claim.

## Probe 2 — deep-thinking retrospective

Zero candidates reached completed comparable-case scoring. Stop incomplete,
preserve the ledger, and draw no conclusion about deep-thinking method value.

## Probe 3 — resident-rule firing

Three of ten planned work units were recorded: one rule fired and two
consequential misses were recovered later. Stop incomplete, preserve the
observations, and add no standing audit or replacement sampling rule.

## Probe 4 — worktree lifecycle

Keep the read-only, fail-closed classifier in
`.github/scripts/lane-health-check.ps1`. Close the probe with no cleanup
authority and no age, count, or automatic cleanup rule.

## Batch closeout

The sample supports retaining selective adversarial review. The observed misses
were primarily adoption or enforcement failures recovered by later lanes, not
evidence that more review layers or resident checklists are needed. No lesson is
promoted, no replacement behavior is installed, and no later batch begins from
this closeout. Receipts, reports, ledgers, and the historical commissioning
prompt remain preserved evidence.
