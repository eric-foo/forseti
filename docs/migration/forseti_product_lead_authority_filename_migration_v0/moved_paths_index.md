# Moved Paths Index - Forseti product-lead authority filename migration v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti migration index
scope: >
  Old-path -> new-path lookup for the bounded product-lead authority filename
  migration that retired five live lowercase `orca_*` filenames.
use_when:
  - Resolving old product thesis, offer, buyer proof, proof charter, or claim-defense paths after this filename migration.
  - Auditing remaining lowercase `orca_*` filenames by family.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_product_lead_authority_filename_migration_decision_v0.md
  - docs/migration/forseti_product_lead_authority_filename_migration_v0/moves_manifest.csv
stale_if:
  - The product-lead authority filename migration manifest changes and this index is not updated.
```

Historical records may retain the old filenames as provenance. For older
`orca/product/...` paths, first resolve through
`docs/migration/forseti_product_root_migration_v0/moved_paths_index.md`, then
apply the filename successor row below where applicable.

| Old path | New path |
| --- | --- |
| `docs/decisions/orca_product_thesis_consumer_demand_v0.md` | `docs/decisions/forseti_product_thesis_consumer_demand_v0.md` |
| `forseti/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md` | `forseti/product/spines/product_lead/offer/forseti_offer_hypothesis_v0.md` |
| `forseti/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md` | `forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md` |
| `forseti/product/spines/product_lead/proof_charter/orca_product_proof_lead_charter_v0.md` | `forseti/product/spines/product_lead/proof_charter/forseti_product_proof_lead_charter_v0.md` |
| `forseti/product/spines/product_lead/proof_charter/orca_claim_defense_doctrine_v0.md` | `forseti/product/spines/product_lead/proof_charter/forseti_claim_defense_doctrine_v0.md` |
