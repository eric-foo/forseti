# Moved Paths Index - Forseti ontology filename migration v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti migration index
scope: >
  Old-path -> new-path lookup for the bounded ontology filename migration that
  retired two live lowercase `orca_*` filenames in the ontology foundation family.
use_when:
  - Resolving old ontology backbone or ontology GT ladder paths after this filename migration.
  - Auditing remaining lowercase `orca_*` filenames by family.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_ontology_filename_migration_decision_v0.md
  - docs/migration/forseti_ontology_filename_migration_v0/moves_manifest.csv
stale_if:
  - The ontology filename migration manifest changes and this index is not updated.
```

Historical records may retain the old filenames as provenance. For older
`orca/product/...` paths, first resolve through
`docs/migration/forseti_product_root_migration_v0/moved_paths_index.md`, then
apply the filename successor row below where applicable.

| Old path | New path |
| --- | --- |
| `docs/decisions/orca_ontology_gt_foundation_ladder_v0.md` | `docs/decisions/forseti_ontology_gt_foundation_ladder_v0.md` |
| `forseti/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md` | `forseti/product/spines/foundation/ontology/forseti_ontology_backbone_architecture_v0.md` |