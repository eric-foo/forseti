# Ontology object card — `vertical:beauty` (v0)

```yaml
retrieval_header_version: 1
artifact_role: Ontology object card (instance hint — Vertical)
scope: >
  Object card for the adopted Orca ontology backbone — a dated instance hint for the
  beauty Vertical and its fragrance sub-niche. The §2.2 roster in
  orca_ontology_backbone_architecture_v0.md is the naming authority; this card is an
  instance hint, not authority, and restates no owner-lane content (it points).
authority_boundary: retrieval_only
status: DATED_HINT_2026-06-15
naming_authority: forseti/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md  # §2.2 (type Vertical) + §2.1 (ID grammar)
```

> Dated instance hint, fail-soft — **not** a current-state claim, **not** authority; restates
> no thesis/wedge content (it points). Reserved types get no card.

- **id:** `vertical:beauty` (§2.1 grammar; canonical dotted form)
- **type:** `Vertical` — §2.2 row 1 ("a demand domain at a level; sub-niches nest via self-parent")
- **instance:** Beauty — Orca's wedge demand domain (consumer beauty & personal care).
- **key states / dimensions** (per §2.2 row 1):
  - `level:` `vertical`
- **sub-niche** (nests via §2.3 `Vertical —narrows_to→ Vertical`):
  - `vertical:beauty —narrows_to→ vertical:beauty.fragrance` (`level: sub_niche`) — the fragrance
    sub-class (the subtle-class home of `venue:basenotes`).
- **links** (drawn from §2.3; resolves inbound references from already-carded instances):
  - `brand:beautypie —in→ vertical:beauty`
  - `venue:basenotes —in→ vertical:beauty.fragrance`
- **backing artifacts** (pointers — NOT restated):
  - thesis → `docs/decisions/orca_product_thesis_consumer_demand_v0.md`
  - wedge → `docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md`

## Non-Claims

Dated hint only. Points to the thesis + wedge; restates neither. Not validation, not readiness.
