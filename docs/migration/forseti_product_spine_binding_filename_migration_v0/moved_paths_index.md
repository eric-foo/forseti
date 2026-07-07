# Forseti Product-Spine Binding Filename Migration Moved-Paths Index v0

```yaml
retrieval_header_version: 1
artifact_role: Moved-path index
scope: Retrieval-only compatibility index for the product/spine binding filename migration.
use_when:
  - Resolving historical references to the old search product-lane binding filename.
  - Resolving historical references to the old Data Lake spine-promotion binding filename.
  - Resolving historical references to the old Creator Signal spine-promotion binding filename.
  - Auditing remaining lowercase filename families after the bounded migration.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_product_spine_binding_filename_migration_decision_v0.md
```

This index is retrieval-only. It does not rewrite historical prompts, review
outputs, research snapshots, old migration evidence, archived DCP receipt
bodies, source-pin rows, source-hash rows, or unrelated product strategy records.

| Old path | New path |
| --- | --- |
| `docs/decisions/orca_search_product_lane_binding_v0.md` | `docs/decisions/forseti_search_product_lane_binding_v0.md` |
| `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md` | `docs/decisions/forseti_data_lake_spine_promotion_binding_v0.md` |
| `docs/decisions/orca_creator_signal_spine_promotion_binding_v0.md` | `docs/decisions/forseti_creator_signal_spine_promotion_binding_v0.md` |