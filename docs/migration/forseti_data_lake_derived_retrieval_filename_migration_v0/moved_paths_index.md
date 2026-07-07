# Forseti Data Lake Derived-Retrieval Filename Migration Moved-Paths Index v0

```yaml
retrieval_header_version: 1
artifact_role: Moved-path index
scope: Retrieval-only compatibility index for the Data Lake derived_retrieval filename migration.
use_when:
  - Resolving historical references to the old Data Lake derived_retrieval activation proposal filename.
  - Auditing remaining lowercase filename families after the bounded migration.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_data_lake_derived_retrieval_filename_migration_decision_v0.md
```

This index is retrieval-only. It does not rewrite historical prompts, review
outputs, research snapshots, old migration evidence, archived DCP receipt
bodies, source-pin rows, source-hash rows, or unrelated product strategy
records.

| Old path | New path |
| --- | --- |
| `docs/decisions/orca_data_lake_derived_retrieval_activation_proposal_v0.md` | `docs/decisions/forseti_data_lake_derived_retrieval_activation_proposal_v0.md` |