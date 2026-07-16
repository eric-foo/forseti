# Ontology object card — `brand:beautypie` (v0)

```yaml
retrieval_header_version: 1
artifact_role: Ontology object card (instance hint — Brand)
scope: >
  Object card for the adopted Orca ontology backbone — a dated instance hint for one
  Brand. The §2.2 roster in forseti_ontology_backbone_architecture_v0.md is the naming
  authority; this card is an instance hint, not authority, and restates no owner-lane
  content (it points).
authority_boundary: retrieval_only
status: DATED_HINT_2026-06-15
review_by: 2027-01-05   # R0 card-convention conformance 2026-07-05
naming_authority: forseti/product/spines/foundation/ontology/forseti_ontology_backbone_architecture_v0.md  # §2.2 (type Brand) + §2.1 (ID grammar)
```

> Dated instance hint, fail-soft — **not** a current-state claim, **not** authority.
> Org is adopted, but this card still omits an ownership edge because the backing
> pointer does not establish a source-backed owner Org for this instance.

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
  - `brand:beautypie —owned_by→ org:…` — **OMITTED / unresolved:** the relationship
    vocabulary is active, but this dated backing pointer does not identify and
    support the owner Org; adoption never fabricates an instance edge.
- **backing artifact** (pointer — NOT restated): `forseti/product/case_families/product_learning/fragrance/consumer_demand_candidate_pool_handoff_v0.md`
  (candidate-pool handoff).

## Non-Claims

Dated hint only. Points to the candidate-pool handoff; restates none of it. The
`—owned_by→ Org` link is intentionally absent for lack of relationship-specific
evidence. Not validation, not readiness.
