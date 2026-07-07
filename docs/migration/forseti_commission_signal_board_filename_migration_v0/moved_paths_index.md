# Forseti Commission Signal Board Filename Migration Moved-Paths Index v0

```yaml
retrieval_header_version: 1
artifact_role: Moved-path index
scope: Retrieval-only compatibility index for the Commission Signal Board filename migration.
use_when:
  - Resolving historical references to the old Commission Signal Board filenames.
  - Auditing remaining lowercase filename families after the bounded migration.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_commission_signal_board_filename_migration_decision_v0.md
```

This index is retrieval-only. It does not rewrite historical prompts, review
outputs, research snapshots, old migration evidence, archived DCP receipt
bodies, source-pin rows, source-hash rows, or older DCP receipt bodies.

For historical `orca/product/...` or `docs/product/...` paths, first resolve
through the relevant product-root and repo-structure migration indexes, then
apply the successor below when applicable.

| Old path | New path |
| --- | --- |
| `forseti/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_structure_rules_v0.md` | `forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md` |
| `forseti/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_structure_v0.md` | `forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md` |
| `forseti/product/spines/commission_signal_board/dispatch_rules/orca_demand_gate_run_commission_criteria_v0.md` | `forseti/product/spines/commission_signal_board/dispatch_rules/forseti_demand_gate_run_commission_criteria_v0.md` |