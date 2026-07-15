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

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Forseti adds `information/` as the fifth accepted second-level product
    axis, with `company_surface/` as its first current domain; the axis owns
    reusable decision-agnostic information contracts while operational work
    remains spine-owned and actual records remain Data Lake-stored.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
    - output_authority
  controlling_sources_updated:
    - docs/decisions/forseti_spine_first_target_structure_binding_v0.md
    - .agents/workflow-overlay/artifact-folders.md
    - forseti/product/README.md
    - forseti/product/information/README.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - docs/STRUCTURE.md
    - docs/workflows/forseti_repo_map_v0.md
    - repo-structure.yaml
    - forseti/product/spines/capture/README.md
    - forseti/product/spines/data_lake/README.md
    - forseti/product/spines/commission_signal_board/README.md
  intentionally_not_updated:
    - path: repo-structure.yaml
      reason: >
        The machine map declares the `forseti/` root and explicitly leaves
        per-product-area structure to the spine-first binding; no machine-map
        field enumerates the second-level product axes.
    - path: forseti/product/shared/
      reason: >
        Its two current registry/doctrine homes remain transitional; Company
        Surface is not placed there and this change does not re-home them.
    - path: Capture, Data Lake, and Commission Signal Board spine content
      reason: >
        Their existing operational and storage ownership is unchanged; only the
        new information-domain relationship is routed.
    - path: forseti-harness/ and stored company data
      reason: >
        Folder authority only; no runtime, schema, migration, capture, or data
        write is authorized.
    - path: historical migration prose, receipts, review-input snapshots, and forseti/product/.gitkeep
      reason: >
        Point-in-time or bootstrap evidence retains the pre-amendment axis list;
        none is a live placement or retrieval router.
  stale_language_search: >
    rg -n "Second-level axis|second-level axis|spines/satellites/case_families/shared|spines / satellites /|spines\\|satellites\\|case_families\\|shared"
    AGENTS.md .agents docs forseti repo-structure.yaml
  stale_language_search_result: >
    Executed 2026-07-15 after the edit. The live product router and
    artifact-folder authority include `information/`; remaining pre-amendment
    axis hits are historical migration prose/receipts, review-input snapshots,
    the bootstrap .gitkeep, or sources that point to the controlling placement
    authority without enumerating the axis. No checked live router omits the
    new axis.
  non_claims:
    - not validation
    - not readiness
    - not Company Surface content or schema acceptance
    - not runtime, storage, capture, CSB, or data-migration authorization
```
