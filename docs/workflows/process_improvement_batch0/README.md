# Process Improvement Batch 0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Active evidence pilot for review economics, deep-thinking decisions, resident-rule firing, and worktree lifecycle.
use_when:
  - Closing a material adversarial review during the Batch 0 sample.
  - Recording or checking one of the four Batch 0 probes.
  - Checking whether the tenth-review owner notification should have fired.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/review-lanes.md
  - docs/workflows/process_improvement_batch0/review_receipts/README.md
```

## Operating state

- `pilot_status`: `active`
- `review_sample_target`: `10`
- `review_completion_unit`: one valid CA-adjudicated receipt for one material adversarial review
- `owner_notification`: one deduplicated GitHub issue, assigned to and mentioning the repository owner, after the valid receipt count first reaches at least 10 on `main`
- `non_claim`: starting or completing this pilot does not prove that a process improves decisions

This is a measurement batch, not a new review layer. It measures observed process
value and failure modes before later doctrine, automation, or skill changes are
considered.

## Probe 1 — adversarial-review economics

After the Chief Architect finishes adjudicating a material adversarial review,
write one JSON receipt under `review_receipts/`. The receipt records net-new
accepted material findings, decision change, closure state, provenance, evidence,
and a small cost proxy. A report, prompt, patch, or unadjudicated review is not a
completion unit.

The validator is `.github/scripts/batch0_process_tracker.py`. The dedicated
GitHub workflow rejects malformed or duplicated receipts on pull requests. The
notification workflow is `.github/workflows/batch0-owner-notify.yml`.

Stop or pivot if receipt production becomes manual ceremony that does not affect
review selection, adjudication, or closure. Prefer automatic derivation from the
CA closeout if that happens.

## Probe 2 — deep-thinking retrospective

Use `deep_thinking_benchmark_v0.md` to examine 8–12 closed decisions. Compare
strong, weak, absent, and unknown deep-thinking use without claiming causality.
Keep `unknown` when the original decision input, invocation state, or observed
outcome cannot be reconstructed.

Stop or pivot if fewer than six cases are comparable. In that case, run only a
decision-delta/conformance audit.

## Probe 3 — resident-rule firing

Use `resident_rule_firing_audit_v0.md` for ten varied work units. Record only
applicable rules, whether they fired, and the observed consequence. Checklist
completion without a concrete consequence is not evidence.

Stop or pivot to incident-triggered sampling if 20 varied units show no
consequential miss or the audit costs more than ten minutes per unit.

## Probe 4 — worktree lifecycle

Use `worktree_lifecycle_audit_v0.md` for the intake baseline and lifecycle failure
classification. This probe is read-only: it never removes a worktree or branch.
Any cleanup or enforcement change is a separate guarded work unit.

## Batch closeout

After the owner notification fires, the next agent should summarize the four
probes for the owner, distinguish method defects from adoption or enforcement
defects, and recommend keep/change/stop decisions. It must not promote a lesson,
change doctrine, or begin Batch 1 without separate authority.
