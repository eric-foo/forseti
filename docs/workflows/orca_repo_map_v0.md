# Orca Repo Map Compatibility Pointer v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti compatibility pointer
scope: Legacy Orca repo-map path retained so historical links resolve after the Forseti repo-map successor migration.
use_when:
  - Following an older link to docs/workflows/orca_repo_map_v0.md.
  - Checking whether the legacy repo-map path still resolves during the Forseti compatibility migration.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/forseti_repo_map_v0.md
```

The live repo map moved to `docs/workflows/forseti_repo_map_v0.md`.

Use the successor map for current source-pack selection and prompt setup. This
file is a compatibility pointer only; it does not own current repo-map content,
validation, readiness, or source authority.
