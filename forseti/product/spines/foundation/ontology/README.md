# Foundation Ontology

```yaml
retrieval_header_version: 1
artifact_role: Ontology front-door
scope: Retrieval-only entry point for live Forseti ontology reference files and legacy foundation owners.
use_when:
  - Resolving fragrance ontology/reference data for Aphrodite D-1.
  - Finding the legacy foundation product-contract owners that still live under orca/product/.
  - Checking whether an ontology artifact is reference data or accepted product doctrine.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/forseti_repo_map_v0.md
  - forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml
  - orca/product/spines/foundation/product_contract/core_spine_v0_product_contract.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_information_production_foundation_v0.md
  - orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md
  - orca/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md
stale_if:
  - The legacy foundation corpus migrates from orca/product/ into forseti/product/.
  - The fragrance reference or ontology backbone is amended.
```

## Load Order

1. Open `fragrance_reference_v0.yaml` only for the D-1 fragrance reference data
   it carries.
2. Open the legacy Core Spine product contract before changing foundation
   semantics.
3. Open the Information Production Foundation when evidence-unit or IPF wording
   is load-bearing.
4. Open the vertical exploration guide for WHERE-side venue or vertical walk
   questions.
5. Open the legacy ontology backbone when the work touches ontology shape beyond
   the fragrance reference.

## Boundary

`fragrance_reference_v0.yaml` is dated reference data for the Aphrodite bundle.
It is not validation, source truth, buyer proof, or a claim that the full
foundation corpus has migrated to Forseti. Legacy foundation owners still live
under `orca/product/` until a separate migration moves them.
