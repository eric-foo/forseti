# Batch 0 Resident-Rule Firing Audit v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow validation note
scope: Ten-work-unit sample of whether applicable resident judgment rules fired and with what consequence.
use_when:
  - Recording a completed work unit in the Batch 0 resident-rule sample.
  - Deciding whether a resident rule needs reinforcement, relocation, or retirement.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/process_improvement_batch0/README.md
  - docs/decisions/overlay_enforcement_placement_classification_v0.md
```

## State

`active`; `WU-01` records the adjudicated delegated-review return for the Batch
0 setup PR. Nine sample slots remain open.

## Recording rule

Record only rules that were applicable. Use `fired | missed | not_applicable |
unknown`, cite the rule and observed artifact/action, and name the concrete
consequence. A checklist tick with no consequence is not evidence.

| Work unit | Source / PR | Applicable resident rule | Result | Observed consequence | Evidence | Evaluator |
| --- | --- | --- | --- | --- | --- | --- |
| WU-01 | PR #850 Batch 0 setup | delegated-review return requires independent home-model adjudication | fired | Reviewer claims were independently adjudicated; AR-01 was downgraded, three bounded hunks were accepted, and the first economics receipt was filed. | `docs/review-outputs/adversarial-artifact-reviews/batch0_process_pilot_implementation_adjudication_v0.md` | OpenAI Codex / GPT-5 |
| WU-02 | pending | pending | unknown | pending | pending | pending |
| WU-03 | pending | pending | unknown | pending | pending | pending |
| WU-04 | pending | pending | unknown | pending | pending | pending |
| WU-05 | pending | pending | unknown | pending | pending | pending |
| WU-06 | pending | pending | unknown | pending | pending | pending |
| WU-07 | pending | pending | unknown | pending | pending | pending |
| WU-08 | pending | pending | unknown | pending | pending | pending |
| WU-09 | pending | pending | unknown | pending | pending | pending |
| WU-10 | pending | pending | unknown | pending | pending | pending |
