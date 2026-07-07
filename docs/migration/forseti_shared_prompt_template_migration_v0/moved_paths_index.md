# Forseti Shared Prompt Template Migration Moved-Paths Index v0

```yaml
retrieval_header_version: 1
artifact_role: Moved-path index
scope: Retrieval-only compatibility index for the shared prompt-template identity migration.
use_when:
  - Resolving historical references to Orca-named shared prompt template paths.
  - Auditing remaining Orca-named shared template references after the Forseti rename.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/template-registry.md
  - docs/prompts/templates/shared/forseti_preflight_defaults_v0.md
  - docs/prompts/templates/shared/forseti_prompt_behavior_contract_v0.md
```

This index is retrieval-only. It does not rewrite historical prompts, review
inputs, review outputs, DCP receipts, source-pack manifests, or old hashes.
The old paths remain compatibility pointers.

| Old path | New path |
| --- | --- |
| `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` | `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md` |
| `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md` | `docs/prompts/templates/shared/forseti_prompt_behavior_contract_v0.md` |
