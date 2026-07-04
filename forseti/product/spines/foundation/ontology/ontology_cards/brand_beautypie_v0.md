# Ontology object card — `brand:beautypie` (v0)

```yaml
retrieval_header_version: 1
artifact_role: Ontology object card (instance hint — Brand)
scope: >
  Object card for the adopted Orca ontology backbone — a dated instance hint for one
  Brand. The §2.2 roster in orca_ontology_backbone_architecture_v0.md is the naming
  authority; this card is an instance hint, not authority, and restates no owner-lane
  content (it points).
authority_boundary: retrieval_only
status: DATED_HINT_2026-06-15
naming_authority: forseti/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md  # §2.2 (type Brand) + §2.1 (ID grammar)
```

> Dated instance hint, fail-soft — **not** a current-state claim, **not** authority. Reserved
> types (`Org`) get no card; a link to a reserved type is omitted/provisional.

- **id:** `brand:beautypie` (§2.1 grammar)
- **type:** `Brand` — §2.2 row 2 ("a consumer brand; consumer-facing label")
- **instance:** Beauty Pie — UK beauty membership/subscription brand (subject of the 2023 repricing).
- **key states / dimensions:** none — §2.2 row 2 promotes none for `Brand`.
- **links** (drawn from §2.3, not invented):
  - `brand:beautypie —in→ vertical:beauty`
  - `decision:beautypie.repricing-2023 —concerns→ brand:beautypie`
  - `brand:beautypie —can_act_as→ WindCaller` — **guarded:** a Brand's own moves are
    `self_originated` for its own Product/DecisionEvent and **excluded from the G1
    independent-origin count** (§2.3 self-origin guard; pointer, not restated).
  - `brand:beautypie —owned_by→ org:…` — **OMITTED / provisional:** `Org` is RESERVED
    (not adopted), so parent-resolution is deferred until `Org` graduates (§6.1).
- **backing artifact** (pointer — NOT restated): `forseti/product/case_families/product_learning/fragrance/consumer_demand_candidate_pool_handoff_v0.md`
  (candidate-pool handoff).

## Non-Claims

Dated hint only. Points to the candidate-pool handoff; restates none of it. The `—owned_by→ Org`
link is intentionally absent (reserved type). Not validation, not readiness.
