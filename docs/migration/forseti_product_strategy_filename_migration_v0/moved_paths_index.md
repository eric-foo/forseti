# Forseti Product-Strategy Filename Migration Moved-Paths Index v0

```yaml
retrieval_header_version: 1
artifact_role: Moved-path index
scope: Retrieval-only compatibility index for the product-strategy filename migration.
use_when:
  - Resolving historical references to old consumer-demand, ICP/wedge, moat proof-path, or venue-registry decision filenames.
  - Auditing remaining lowercase filename families after the bounded migration.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_product_strategy_filename_migration_decision_v0.md
```

This index is retrieval-only. It does not rewrite historical prompts, review
outputs, research snapshots, old migration evidence, archived DCP receipt
bodies, source-pin rows, source-hash rows, or unrelated product-tree filenames.

| Old path | New path |
| --- | --- |
| `docs/decisions/orca_consumer_demand_ratification_decision_memo_v0.md` | `docs/decisions/forseti_consumer_demand_ratification_decision_memo_v0.md` |
| `docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md` | `docs/decisions/forseti_icp_wedge_consumer_demand_first_v0.md` |
| `docs/decisions/orca_icp_wedge_convergence_break_in_first_v0.md` | `docs/decisions/forseti_icp_wedge_convergence_break_in_first_v0.md` |
| `docs/decisions/orca_icp_wedge_pricing_first_v0.md` | `docs/decisions/forseti_icp_wedge_pricing_first_v0.md` |
| `docs/decisions/orca_moat_judgment_quality_proof_path_decision_chain_v0.md` | `docs/decisions/forseti_moat_judgment_quality_proof_path_decision_chain_v0.md` |
| `docs/decisions/orca_venue_registry_rejection_decision_v0.md` | `docs/decisions/forseti_venue_registry_rejection_decision_v0.md` |