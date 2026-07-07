# Forseti Spine-First Structure Filename Migration Moved-Paths Index v0

```yaml
retrieval_header_version: 1
artifact_role: Moved-path index
scope: Retrieval-only compatibility index for the spine-first structure filename migration.
use_when:
  - Resolving historical references to the old spine-first target-structure binding filename.
  - Resolving historical references to the old spine-first blocker-authorization filename.
  - Auditing remaining lowercase filename families after the bounded migration.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_spine_first_structure_filename_migration_decision_v0.md
```

This index is retrieval-only. It does not rewrite historical prompts, review
outputs, research snapshots, old migration evidence, archived DCP receipt
bodies, source-pin rows, source-hash rows, or historical product-root body
references.

| Old path | New path |
| --- | --- |
| `docs/decisions/orca_spine_first_target_structure_binding_v0.md` | `docs/decisions/forseti_spine_first_target_structure_binding_v0.md` |
| `docs/decisions/orca_spine_first_blocker_authorization_v0.md` | `docs/decisions/forseti_spine_first_blocker_authorization_v0.md` |