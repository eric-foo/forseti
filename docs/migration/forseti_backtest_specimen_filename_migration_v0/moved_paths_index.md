# Forseti Backtest Specimen Filename Migration Moved-Paths Index v0

```yaml
retrieval_header_version: 1
artifact_role: Moved-path index
scope: Retrieval-only compatibility index for the Unity runtime-fee backtest specimen filename migration.
use_when:
  - Resolving historical references to old Unity backtest specimen filenames.
  - Auditing remaining lowercase filename families after the bounded migration.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_backtest_specimen_filename_migration_decision_v0.md
```

This index is retrieval-only. It does not rewrite sealed specimen body text,
source-pin rows, source-hash rows, historical prompts, review outputs, research
snapshots, old migration evidence, or unrelated product-tree filenames.

| Old path | New path |
| --- | --- |
| `forseti/product/case_families/product_learning/other_verticals/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md` | `forseti/product/case_families/product_learning/other_verticals/forseti_backtest_specimen_unity_runtime_fee_source_packet_v0.md` |
| `forseti/product/case_families/product_learning/other_verticals/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md` | `forseti/product/case_families/product_learning/other_verticals/forseti_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md` |
| `forseti/product/case_families/product_learning/other_verticals/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md` | `forseti/product/case_families/product_learning/other_verticals/forseti_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md` |