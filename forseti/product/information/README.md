# Product Information

```yaml
retrieval_header_version: 1
artifact_role: Product information front-door index
scope: >
  Retrieval-only entry point for Forseti's reusable, decision-agnostic
  information domains. Defines the information-axis placement boundary and
  routes to its current domains; it does not define their record schemas or
  store runtime data.
use_when:
  - Deciding whether a product artifact is reusable information or operational spine material.
  - Starting work on a product information domain.
  - Finding the current Company Surface front door.
authority_boundary: retrieval_only
open_next:
  - forseti/product/information/company_surface/README.md
stale_if:
  - The information axis is renamed, retired, or merged into another product axis.
  - The Company Surface front door moves or another information domain is accepted.
```

This axis holds contracts for reusable information that operational spines can
consume without making one of those spines its owner. It is not a generic
document bucket.

## Boundary

- Actual records and captured evidence live through Data Lake-owned storage,
  not in this product-document folder.
- Operational instructions, queues, decisions, and interventions stay with the
  owning spine.
- Decision records, research, prompts, and reviews stay in their accepted
  `docs/` homes.
- A new information domain requires an accepted product-structure decision; do
  not add speculative holding folders here.

## Current Domains

| Domain | Role | Open |
| --- | --- | --- |
| Company Surface | Decision-agnostic home for the future contract governing externally observable company history. | `forseti/product/information/company_surface/README.md` |

This placement does not claim a Company Surface schema, implementation, stored
company corpus, entity resolver, CSB integration, validation, or readiness.
