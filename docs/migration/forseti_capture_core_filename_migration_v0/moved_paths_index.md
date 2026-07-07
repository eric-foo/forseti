# Forseti Capture Core Filename Migration Moved-Paths Index v0

```yaml
retrieval_header_version: 1
artifact_role: Moved-path index
scope: Retrieval-only compatibility index for the Capture-core filename migration.
use_when:
  - Resolving historical references to the old Capture-core architecture filenames.
  - Auditing remaining lowercase filename families after the bounded migration.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_capture_core_filename_migration_decision_v0.md
```

This index is retrieval-only. It does not rewrite historical prompts, review
outputs, research snapshots, old migration evidence, archived DCP receipt
bodies, source-pin rows, source-hash rows, or older DCP receipt bodies.

For historical `orca/product/...` or `docs/product/...` paths, first resolve
through the relevant product-root and repo-structure migration indexes, then
apply the successor below when applicable.

| Old path | New path |
| --- | --- |
| `forseti/product/spines/capture/core/operating_model/orca_capture_projection_storage_spine_architecture_v0.md` | `forseti/product/spines/capture/core/operating_model/forseti_capture_projection_storage_spine_architecture_v0.md` |
| `forseti/product/spines/capture/core/source_families/social_media/instagram/orca_creator_momentum_pipeline_architecture_v0.md` | `forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_momentum_pipeline_architecture_v0.md` |
| `forseti/product/spines/capture/core/source_families/social_media/instagram/orca_creator_monitoring_policy_architecture_v0.md` | `forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_monitoring_policy_architecture_v0.md` |
