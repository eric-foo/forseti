# Moved Paths Index - Data Lake R2 convergence (generated/curated)

```yaml
retrieval_header_version: 1
artifact_role: Orca migration index (Data Lake R2 path-resolution artifact)
scope: >
  Old-path -> new-path lookup for the Data Lake R2 convergence: the 3 lake
  contracts + the canonical mechanics map harvested from the in-flight contract
  lane into orca/product/spines/data_lake/, plus the retired
  orca/product/shared/data_lake_mechanics/ copy. Resolves historical references.
use_when:
  - Resolving an old docs/product or shared/ data-lake path to its data_lake spine home.
  - Auditing the Data Lake R2 convergence.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_data_lake_spine_promotion_binding_v0.md
  - orca/product/spines/data_lake/README.md
stale_if:
  - A later accepted decision relocates the data_lake spine contents.
```

Historical + cross-lane records reference these old paths by design; resolve them here.

| Old path | New path |
| --- | --- |
| `docs/product/core_spine/core_spine_v0_data_lake_core_contract_v0.md` | `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md` |
| `docs/product/core_spine/core_spine_v0_data_lake_storage_contract_v0.md` | `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md` |
| `docs/product/core_spine/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md` | `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md` |
| `docs/product/core_spine/core_spine_v0_data_lake_mechanics_map_v0.md` | `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md` |
| `orca/product/shared/data_lake_mechanics/core_spine_v0_data_lake_mechanics_map_v0.md` | `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md` |

Provenance: contracts + mechanics harvested 2026-06-18 from `codex/data-lake-core-contract` (#232); the mechanics-map content was confirmed canonical via a 3-way reconciliation (vs `origin/main` shared/ copy and the `codex/data-lake-mechanics-map` lane). The 2 `#239` repo-structure planning docs (`data_lake_spine_first_migration_{plan,inventory}_v0.md`) are deferred pending the data-lake placement decision (`docs/migration/` vs `migrations/`).
