# Moved Paths Index - Forseti harness runtime migration

```yaml
retrieval_header_version: 1
artifact_role: Forseti migration index (path-resolution artifact)
scope: >
  Old-path -> new-path lookup for the runtime/tooling migration from
  orca-harness/ to forseti-harness/. Preserves historical and residual records
  that intentionally keep point-in-time Orca harness paths.
use_when:
  - Resolving a historical or residual orca-harness path to its Forseti successor.
  - Auditing or re-running the Forseti harness runtime migration.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_harness_identity_migration_plan_v0.md
  - docs/workflows/forseti_repo_map_v0.md
stale_if:
  - The harness runtime root is relocated again.
  - A later accepted migration changes the harness path-resolution boundary.
```

Historical and residual records may reference old `orca-harness/` paths by
design; resolve them here.

| Old path | New path |
| --- | --- |
| `orca-harness/` | `forseti-harness/` |
