# Forseti Product-Lead ICP/Wedge Filename Migration Moved-Paths Index v0

```yaml
retrieval_header_version: 1
artifact_role: Moved-path index
scope: Retrieval-only compatibility index for the product-lead ICP/wedge filename migration.
use_when:
  - Resolving historical references to old product-lead ICP/wedge artifact filenames.
  - Auditing remaining lowercase filename families after the bounded migration.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_product_lead_icp_wedge_filename_migration_decision_v0.md
```

This index is retrieval-only. It does not rewrite historical prompts, review
outputs, research snapshots, old migration evidence, archived DCP receipt
bodies, source-pin rows, source-hash rows, or unrelated product-tree filenames.

| Old path | New path |
| --- | --- |
| `forseti/product/spines/product_lead/icp_wedge/orca_discovery_batch_0_candidate_context_scan_v0.md` | `forseti/product/spines/product_lead/icp_wedge/forseti_discovery_batch_0_candidate_context_scan_v0.md` |
| `forseti/product/spines/product_lead/icp_wedge/orca_discovery_batch_0_qualification_prep_sentry_clerk_v0.md` | `forseti/product/spines/product_lead/icp_wedge/forseti_discovery_batch_0_qualification_prep_sentry_clerk_v0.md` |
| `forseti/product/spines/product_lead/icp_wedge/orca_discovery_batch_0_target_selection_brief_v0.md` | `forseti/product/spines/product_lead/icp_wedge/forseti_discovery_batch_0_target_selection_brief_v0.md` |
| `forseti/product/spines/product_lead/icp_wedge/orca_discovery_consumer_demand_target_selection_brief_v0.md` | `forseti/product/spines/product_lead/icp_wedge/forseti_discovery_consumer_demand_target_selection_brief_v0.md` |
| `forseti/product/spines/product_lead/icp_wedge/orca_icp_ratification_readiness_report_v0.md` | `forseti/product/spines/product_lead/icp_wedge/forseti_icp_ratification_readiness_report_v0.md` |
| `forseti/product/spines/product_lead/icp_wedge/orca_product_lead_first_icp_wedge_decision_v0.md` | `forseti/product/spines/product_lead/icp_wedge/forseti_product_lead_first_icp_wedge_decision_v0.md` |
| `forseti/product/spines/product_lead/icp_wedge/orca_ratification_day_runbook_v0.md` | `forseti/product/spines/product_lead/icp_wedge/forseti_ratification_day_runbook_v0.md` |