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

Answer-engine/search/AEO shortcut for legacy cold starts: current work routes
through `forseti/product/spines/scanning/README.md`, then
`forseti/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md`,
then research evidence under `docs/research/answer_engine/`. Do not route
current execution through stale `docs/product/search/` or search-lane history.
