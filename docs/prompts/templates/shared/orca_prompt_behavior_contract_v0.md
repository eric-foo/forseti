# Legacy Orca Prompt Behavior Contract Pointer v0

```yaml
retrieval_header_version: 1
artifact_role: Compatibility pointer
scope: Legacy retrieval path for the renamed Forseti prompt behavior contract template.
use_when:
  - Resolving older prompts or source packs that cite the Orca-named shared behavior contract path.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/templates/shared/forseti_prompt_behavior_contract_v0.md
```

This file is a compatibility pointer. The live shared behavior contract source
for new or materially touched Forseti prompt templates is:

`docs/prompts/templates/shared/forseti_prompt_behavior_contract_v0.md`

Do not copy the old path into new prompt templates. Historical prompts, review
inputs, review outputs, DCP receipts, and source-pack manifests may keep the old
path as provenance.
