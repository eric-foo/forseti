# Forseti Mini God Tier Doctrine Filename Migration Moved-Paths Index v0

```yaml
retrieval_header_version: 1
artifact_role: Moved-path index
scope: Retrieval-only compatibility index for the Mini God Tier doctrine filename migration.
use_when:
  - Resolving historical references to the old Mini God Tier doctrine filename.
  - Auditing remaining lowercase filename families after the bounded migration.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_mini_god_tier_doctrine_filename_migration_decision_v0.md
```

This index is retrieval-only. It does not rewrite historical prompts, review
outputs, research snapshots, old migration evidence, archived DCP receipt
bodies, source-pin rows, source-hash rows, or older DCP receipt bodies.

| Old path | New path |
| --- | --- |
| `docs/decisions/orca_mini_god_tier_doctrine_v0.md` | `docs/decisions/forseti_mini_god_tier_doctrine_v0.md` |