# Ontology object card — `product:dior.sauvage` (v0)

```yaml
retrieval_header_version: 1
artifact_role: Ontology object card (instance hint — Product; graduation exemplar)
scope: >
  Object card for the adopted Orca ontology backbone — a dated instance hint for one
  Product, and the exemplar card for the Product type's graduation from the deferred
  card backlog (backing landed 2026-07-04: the Aphrodite fragrance sub-ontology
  reference data). The §2.2 roster in orca_ontology_backbone_architecture_v0.md is
  the naming authority; this card is an instance hint, not authority, and restates
  no owner-lane content (it points).
authority_boundary: retrieval_only
status: DATED_HINT_2026-07-04
review_by: 2027-01-05   # R0 card-convention conformance 2026-07-05
naming_authority: forseti/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md  # §2.2 (type Product) + §2.1 (ID grammar) + §6.1 amendment 2026-07-04
```

> Dated instance hint, fail-soft — **not** a current-state claim, **not** authority.

- **id:** `product:dior.sauvage` (§2.1 grammar)
- **type:** `Product` — §2.2 row 3 ("the demand target: ingredient/category/format/claim/SKU")
- **instance:** Sauvage — Dior men's fragrance line; the rehearsal corpora's most
  consistently surfaced designer product.
- **key states / dimensions:** `target_type: sku-line` (illustrative; property lists are
  deliberately unfrozen — §6).
- **links** (drawn from §2.3, not invented):
  - `brand:dior —offers→ product:dior.sauvage`
  - `brand:dior —in→ vertical:beauty.fragrance`
- **backing artifact** (pointer — NOT restated):
  `forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml`
  (note families, accords, tier, occasions, dupe edges, per-fact provenance live THERE,
  as schema-light data — this card does not restate them).

## Non-Claims

Dated hint only. Points to the fragrance reference data; restates none of it. Not
validation, not readiness, not fact-correctness; `product_learning`-capped.
