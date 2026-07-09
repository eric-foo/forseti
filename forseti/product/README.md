# Forseti Product

```yaml
retrieval_header_version: 1
artifact_role: Product tree front door
scope: Canonical Forseti product-tree entrypoint during identity convergence.
use_when:
  - Starting product-surface work in Forseti.
  - Finding the accepted Aphrodite / Creator Signal product records.
  - Checking which Orca-named roots are still legacy compatibility paths.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/forseti_repo_map_v0.md
  - forseti/product/spines/creator_signal/README.md
  - forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md
  - forseti/product/spines/creator_signal/aphrodite_vetting_sprint_panel_design_v0.md
  - forseti/product/spines/foundation/ontology/README.md
  - forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml
stale_if:
  - The physical product corpus under orca/product/ is migrated into forseti/product/.
  - A later accepted product-tree binding supersedes the legacy compatibility posture.
```

## Canonical Route

Forseti is the canonical project and product identity. New product entrypoints
and newly accepted product artifacts route through `forseti/product/` unless the
work is a narrow update to an existing legacy owner that still physically lives
under `orca/product/`.

## Current Live Forseti Product Areas

- `forseti/product/spines/creator_signal/`: Creator Signal / Aphrodite product
  records restored for the D-1 bundle. Start at
  `forseti/product/spines/creator_signal/README.md`.
- `forseti/product/spines/foundation/ontology/`: Forseti ontology reference data
  needed by the Aphrodite D-1 rehearsal. Start at
  `forseti/product/spines/foundation/ontology/README.md`.

## Legacy Compatibility Roots

- `orca/product/`: legacy product corpus. Most pre-Forseti product and spine
  owners still physically live there; do not mass-move them in a writing lane
  unless a separate migration explicitly authorizes it.
- `orca-harness/`: legacy runtime harness root. No `forseti-harness/` directory
  exists in this workspace yet; use the legacy harness path when a live harness
  file is required.

## Aphrodite D-1 Fast Route

Open these live files for the D-1 bundle:

- `docs/research/aphrodite_depth_rehearsal_extraction_recipe_v1.md`
- `docs/research/aphrodite_recipe_v1_second_opinion_adjudication_v0.md`
- `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_corpus_v0.md`
- `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json`
- `forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md`
- `forseti/product/spines/creator_signal/aphrodite_vetting_sprint_panel_design_v0.md`
- `forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml`

## Non-Claims

This README is navigation only. It is not validation, readiness, buyer proof,
source promotion, build authorization, runtime authorization, or evidence that
the legacy physical-root migration is complete.