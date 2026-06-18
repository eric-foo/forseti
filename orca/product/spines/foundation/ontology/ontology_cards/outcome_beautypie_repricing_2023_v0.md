# Ontology object card — `outcome:beautypie.repricing-2023` (v0)

```yaml
retrieval_header_version: 1
artifact_role: Ontology object card (instance hint — Outcome)
scope: >
  Object card for the adopted Orca ontology backbone — a dated instance hint for one
  Outcome. The §2.2 roster in orca_ontology_backbone_architecture_v0.md is the naming
  authority; this card is an instance hint, not authority, and restates no owner-lane
  content (it points).
authority_boundary: retrieval_only
status: DATED_HINT_2026-06-15
naming_authority: orca/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md  # §2.2 (type Outcome) + §2.1 (ID grammar)
```

> Dated instance hint, fail-soft — **not** a current-state claim, **not** authority. Reserved types get no card.

- **id:** `outcome:beautypie.repricing-2023` (§2.1 grammar)
- **type:** `Outcome` — §2.2 row 13 ("the realized result a Reading/Call/Case is graded against; calibration target")
- **instance:** The known realized result of Beauty Pie's 2023 repricing — the calibration target
  the backtest case is graded against.
- **key states / dimensions:** none — §2.2 row 13 promotes none for `Outcome`.
- **links** (drawn from §2.3):
  - inbound: `case:beautypie.repricing-2023 —graded_by→ outcome:beautypie.repricing-2023`
- **backing artifacts** (pointers — NOT restated):
  - known-outcome / calibration target → `orca-harness/cases/product_learning/beautypie_repricing_2023_v0/facilitator_ledger.yaml`
    (the case has **not** been run, so this is the *known historical* result, not a graded `case_report`)
  - `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md` (batch-1 ledger, case #3)

## Non-Claims

Dated hint only. Points to the facilitator-ledger known-outcome + the batch-1 ledger; restates
neither. Not a graded run result (the case has not been run). Not validation, not readiness.
