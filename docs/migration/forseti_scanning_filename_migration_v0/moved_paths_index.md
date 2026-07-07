# Forseti Scanning Filename Migration Moved-Paths Index v0

```yaml
retrieval_header_version: 1
artifact_role: Moved-path index
scope: Retrieval-only compatibility index for the scanning core and admissibility/checkability filename migration.
use_when:
  - Resolving historical references to the old scanning core and admissibility/checkability filenames.
  - Auditing remaining lowercase filename families after the bounded migration.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_scanning_filename_migration_decision_v0.md
```

This index is retrieval-only. It does not rewrite historical prompts, review
outputs, research snapshots, old migration evidence, archived DCP receipt
bodies, source-pin rows, source-hash rows, or older DCP receipt bodies.

For historical `orca/product/...` or `docs/product/...` paths, first resolve
through the relevant product-root and repo-structure migration indexes, then
apply the successor below when applicable.

| Old path | New path |
| --- | --- |
| `forseti/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md` | `forseti/product/spines/scanning/scan_core/forseti_demand_scan_core_spec_v0.md` |
| `forseti/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md` | `forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md` |
| `forseti/product/spines/scanning/admissibility_checkability/orca_demand_gate_definition_closures_proposal_v0.md` | `forseti/product/spines/scanning/admissibility_checkability/forseti_demand_gate_definition_closures_proposal_v0.md` |
| `forseti/product/spines/scanning/admissibility_checkability/orca_demand_scan_gate_adjudication_packet_v0.md` | `forseti/product/spines/scanning/admissibility_checkability/forseti_demand_scan_gate_adjudication_packet_v0.md` |