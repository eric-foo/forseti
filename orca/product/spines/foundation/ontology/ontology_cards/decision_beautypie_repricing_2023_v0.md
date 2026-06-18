# Ontology object card — `decision:beautypie.repricing-2023` (v0)

```yaml
retrieval_header_version: 1
artifact_role: Ontology object card (instance hint — DecisionEvent)
scope: >
  Object card for the adopted Orca ontology backbone — a dated instance hint for one
  DecisionEvent. The §2.2 roster in orca_ontology_backbone_architecture_v0.md is the
  naming authority; this card is an instance hint, not authority, and restates no
  owner-lane content (it points).
authority_boundary: retrieval_only
status: DATED_HINT_2026-06-15
naming_authority: orca/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md  # §2.2 (type DecisionEvent) + §2.1 (ID grammar)
```

> Dated instance hint, fail-soft — **not** a current-state claim, **not** authority. Reserved types get no card.

- **id:** `decision:beautypie.repricing-2023` (§2.1 grammar)
- **type:** `DecisionEvent` — §2.2 row 9 ("the live brand-decision event the Read action serves")
- **instance:** Beauty Pie's 2023 repricing decision (£5/month entry-tier elimination, minimum
  doubled) — the brand decision the backtest case is built around.
- **key states / dimensions** (per §2.2 row 9):
  - `trigger status:` historical (the 2023 repricing already occurred)
  - `discovery_status:` n/a — **historical backtest** decision, not a live discovery-scan candidate
    (this card implies no live scan)
- **links** (drawn from §2.3):
  - `decision:beautypie.repricing-2023 —concerns→ brand:beautypie`
  - inbound: `case:beautypie.repricing-2023 —backtests→ decision:beautypie.repricing-2023`
- **backing artifact** (pointer — NOT restated): `orca/product/case_families/product_learning/fragrance/consumer_demand_candidate_pool_handoff_v0.md`
  (candidate-pool handoff).

## Non-Claims

Dated hint only. Points to the candidate-pool handoff; restates none of it. `discovery_status` is
n/a (historical, not a live candidate). Not validation, not readiness.
