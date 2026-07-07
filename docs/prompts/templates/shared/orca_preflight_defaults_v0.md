# Legacy Orca Preflight Defaults Pointer v0

```yaml
retrieval_header_version: 1
artifact_role: Compatibility pointer
scope: Legacy retrieval path for the renamed Forseti preflight defaults template.
use_when:
  - Resolving older prompts or source packs that cite the Orca-named preflight defaults path.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/templates/shared/forseti_preflight_defaults_v0.md
```

This file is a compatibility pointer. The live shared preflight defaults source
for new or materially touched Forseti prompt artifacts is:

`docs/prompts/templates/shared/forseti_preflight_defaults_v0.md`

Do not copy the old path into new prompt artifacts. Historical prompts, review
inputs, review outputs, DCP receipts, and source-pack manifests may keep the old
path as provenance.
