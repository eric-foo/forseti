# Forseti Vertical Exploration Filename Migration Moved-Paths Index v0

```yaml
retrieval_header_version: 1
artifact_role: Moved-path index
scope: Retrieval-only compatibility index for the vertical-exploration filename migration.
use_when:
  - Resolving historical references to the old vertical-exploration filenames.
  - Auditing remaining lowercase filename families after the bounded migration.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_vertical_exploration_filename_migration_decision_v0.md
```

This index is retrieval-only. It does not rewrite historical prompts, review
outputs, research snapshots, old migration evidence, source-pin rows, source-hash
rows, or older DCP receipt bodies.

For historical `orca/product/...` or `docs/product/core_spine/...` paths, first
resolve through the relevant product-root and repo-structure migration indexes,
then apply the successor below when applicable.

| Old path | New path |
| --- | --- |
| `forseti/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md` | `forseti/product/spines/foundation/vertical_exploration/forseti_vertical_exploration_guide_v0.md` |
| `forseti/product/spines/foundation/vertical_exploration/orca_memorization_resistant_case_finder_frame_v0.md` | `forseti/product/spines/foundation/vertical_exploration/forseti_memorization_resistant_case_finder_frame_v0.md` |