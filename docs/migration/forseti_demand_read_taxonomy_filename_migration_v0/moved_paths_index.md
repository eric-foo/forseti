# Forseti Demand-Read Taxonomy Filename Migration Moved-Paths Index v0

```yaml
retrieval_header_version: 1
artifact_role: Moved-path index
scope: Retrieval-only compatibility index for the demand-read taxonomy filename migration.
use_when:
  - Resolving historical references to the old demand-read taxonomy filenames.
  - Auditing remaining lowercase filename families after the bounded migration.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_demand_read_taxonomy_filename_migration_decision_v0.md
```

This index is retrieval-only. It does not rewrite historical prompts, review
outputs, research snapshots, old migration evidence, source-pin rows, source-hash
rows, or older DCP receipt bodies.

For historical `orca/product/...` paths, first resolve through
`docs/migration/forseti_product_root_migration_v0/moved_paths_index.md`, then
apply the successor below when applicable.

| Old path | New path |
| --- | --- |
| `forseti/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md` | `forseti/product/spines/foundation/demand_read_taxonomy/forseti_demand_read_taxonomy_v0.md` |
| `forseti/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_adjudication_v0.md` | `forseti/product/spines/foundation/demand_read_taxonomy/forseti_demand_read_taxonomy_adjudication_v0.md` |
