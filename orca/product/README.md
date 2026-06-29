# Orca Product

Product substance for Orca lives here, organized **spine-first**. This is the
product-facing tree; runtime stays in `orca-harness/`.

## Structure

Second-level axis: `spines/` (by function) plus `satellites/`, `case_families/`,
and `shared/`.

- `spines/`
  - `foundation/` — product contract, ontology, evidence standard, demand-read taxonomy, vertical exploration, shared primitives
  - `commission_signal_board/` — commission contract, signal board, dispatch rules, work orders
  - `scanning/` — scan core, admissibility/checkability, source families (discovery-side)
  - `capture/` — capture contracts, operating model, packet schema, source-capture toolbox, demand-durability indicators, source families (acquisition-side)
  - `creator_signal/` — product-facing creator intelligence surfaces: profile IA, aggregate influence display, ideal-audience/content-fit display, freshness, limitations, and source drill-back over Capture-owned creator records
  - `ecr/` — Evidence Candidate Record + Signal Content Record
  - `cleaning/` — cleaning contracts, transformations, integrity labels, normalization
  - `judgment/` — conductor, claim ladder, source-side receipts, demand-read, product-learning machinery, learning loops, toolkit gaps
  - `product_lead/` — offer, buyer proof, ICP wedge, proof charter
  - `data_lake/` — **shared-foundation spine**: cross-layer storage contracts (raw-packet preservation, keyed retrievability, Attachment Record, passive Availability Index) consumed by projection/ECR/cleaning/judgment. Authority and workflow content landed in the R2 move pass.
- `satellites/` — domain-specific context (e.g. `beauty/`, `fragrance/`)
- `case_families/` — corpora, runs, and case docs (e.g. `product_learning/`)
- `shared/` — cross-spine registries: `engagement_registry/`, `projection_doctrine/` (both transitional, pending their own re-home decisions)

## Authority

- Tree bound by `docs/decisions/orca_spine_first_target_structure_binding_v0.md`
  (+ `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md` for the
  `data_lake/` spine and
  `docs/decisions/orca_creator_signal_spine_promotion_binding_v0.md` for the
  `creator_signal/` spine).
- Placement enforced by `.agents/workflow-overlay/artifact-folders.md` +
  `repo-structure.yaml`.
- Route card: `docs/workflows/orca_repo_map_v0.md`.
- Historical pre-migration `docs/product/...` references resolve through
  `docs/migration/repo_structure_spine_first_v0/moved_paths_index.md`.

## Core vs Satellite

Keep the split explicit:

- **Core** (foundation): market-agnostic evidence mechanics.
- **Satellites**: decision-specific and domain-specific context.

## Conventions

- New product artifacts go in the matching spine folder (forward-only).
- Decisions, prompts, reviews, research, and migration records stay under `docs/`,
  not here.
- Runtime code and tests stay in `orca-harness/`.
- Do not treat Client 0 `jb` material as core product authority unless a product
  artifact explicitly promotes the concept as generalizable.
