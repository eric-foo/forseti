# Ontology object cards — folder convention (v0)

```yaml
retrieval_header_version: 1
artifact_role: Convention note (ontology object-card folder)
scope: >
  How object cards in this folder work. The §2.2 roster in
  orca_ontology_backbone_architecture_v0.md is the naming authority; these cards
  and this note are subordinate to it.
authority_boundary: retrieval_only
status: DATED_HINT_2026-06-15
naming_authority: orca/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md
```

Each file here is one **object card** — a dated *instance* of an adopted §2.2 object type.

Convention (all cards):

- **Thin dated hint, fail-soft** — a best-current hint with a `review_by`, not a current-state
  claim or authority. If it goes stale, re-review or retire it.
- **Pointer-not-restate** — a card gives the instance's id + values + *pointers* to where its real
  data lives; it never restates owner-lane content (the AR-01 boundary).
- **Drawn from §2.2/§2.3** — only adopted types, dimensions, and links; no new vocabulary.
- **`retrieval_only` header**, `naming_authority` → the §2.2 doc. No cards for **reserved** types
  (`Buyer`, `Org`).
- **Schema-light (the key point):** the dimensions a card lists are the type's *named* ones —
  **illustrative, not a required schema**. Instances are schema-light (property lists are
  deliberately not frozen — see §2.2 / §10), so a card fills only what's relevant and may carry
  free-form descriptive content. Only the **id, type, and load-bearing links/gates** are fixed;
  e.g. an `Outcome` has no named dimensions at all, and a live `DecisionEvent` starts loose and
  *accretes* structure through its lifecycle rather than being locked up-front.
- **Forward-only IDs** — the canonical id is the dotted form; an existing producer id (e.g. a
  harness `*_v0`) is recorded as a storage alias under it (`harness_case_id`-style), never renamed
  (§2.1 / §6.1).

Not a registry, not validation, not readiness. The cards collectively *seed* the future registry.
