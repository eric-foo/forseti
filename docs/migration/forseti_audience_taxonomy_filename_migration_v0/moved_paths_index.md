# Forseti Audience Taxonomy Filename Migration Moved-Paths Index v0

```yaml
retrieval_header_version: 1
artifact_role: Moved-path index
scope: Retrieval-only compatibility index for the audience taxonomy filename migration.
use_when:
  - Resolving historical references to the old audience-inference ballot taxonomy filename.
  - Resolving historical references to the old Tier-2-A base-rate prior table filename.
  - Auditing remaining lowercase filename families after the bounded migration.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_audience_taxonomy_filename_migration_decision_v0.md
```

This index is retrieval-only. It does not rewrite historical prompts, review
outputs, research snapshots, old migration evidence, archived DCP receipt
bodies, source-pin rows, source-hash rows, or unrelated product strategy
records.

| Old path | New path |
| --- | --- |
| `docs/decisions/orca_audience_ballot_taxonomy_v0.md` | `docs/decisions/forseti_audience_ballot_taxonomy_v0.md` |
| `docs/decisions/orca_audience_tier2a_base_rate_prior_table_v0.md` | `docs/decisions/forseti_audience_tier2a_base_rate_prior_table_v0.md` |