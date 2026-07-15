# Forseti Workflow Efficiency

This directory is the front door for reusable Forseti workflow and tool
efficiency material: methods, fixed cases, measurements, and dogfood records.
It does not own workflow doctrine, product behavior, validation status, or a
claim that any documented result has been reproduced.

## Route by need

| Need | Open |
| --- | --- |
| Run the fixed cold-agent vendor-admission tool-calling case | `tool_calling_dogfood_case_v0.md` |
| Review the observed 2026-07-15 three-run baseline and efficiency diagnosis | `tool_calling_dogfood_run_2026_07_15_v0.md` |
| Record an observed recurring tooling or workflow failure and its corrective pointers | `../technical_difficulties_log_v0.md` |
| Follow the dated 2026-07-09 hygiene-audit checklist and its execution waves | `../../hygiene/efficiency_audit_wave_plan_v0.md` |
| Interpret the temporary Batch 1 decision-gate economics pilot | `../../../.agents/workflow-overlay/batch1-decision-gate-economics.md` |

## Ownership boundary

- **Technical Diagnostics** is the append-only record for observed recurring
  tooling or workflow failures, their impact, and corrective pointers.
- **This efficiency surface** holds reusable efficiency methods, cases,
  measurements, and dogfood records. Each child artifact owns only the case or
  method it defines.
- **The efficiency-audit wave plan** is a dated hygiene tracking checklist. It
  does not own this directory or general workflow/tool efficiency practice.
- **Batch 1 decision-gate economics** is temporary overlay authority for its
  named pilot. It is not general tool-efficiency authority.

Currentness is per child artifact. On conflict, open the linked owning source;
this README is a directory router, not independent authority. For the current
fixed case, open `tool_calling_dogfood_case_v0.md` next.
