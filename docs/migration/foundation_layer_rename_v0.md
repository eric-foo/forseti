# Foundation Layer Rename v0

```yaml
retrieval_header_version: 1
artifact_role: Migration record
scope: >
  Records the docs/product/core_spine/ -> docs/product/foundation/ product-lane
  rename and the terminology boundary for Foundation Layer.
use_when:
  - Resolving old Core Spine or docs/product/core_spine/ references after the Foundation Layer rename.
  - Deciding whether a core_spine_v0_* artifact ID should be renamed.
  - Checking whether Judgment demand-read core is part of this rename.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/artifact-folders.md
  - docs/decisions/orca_repo_structure_binding_v0.md
  - docs/workflows/orca_repo_map_v0.md
stale_if:
  - Any core_spine_v0_* artifact IDs are renamed.
  - A later structure binding supersedes the Foundation Layer home.
```

- Status: APPLIED_RENAME_RECORD
- Current canonical home: `docs/product/foundation/`
- Former home: `docs/product/core_spine/`
- Canonical prose label: Foundation Layer
- Implementation authorized: no

## Applied Move

```text
docs/product/core_spine/** -> docs/product/foundation/**
```

The live product lane formerly called Core Spine is now Foundation Layer. New
live references should use `docs/product/foundation/` and Foundation Layer.

## Preserved Names

Legacy `core_spine_v0_*` artifact IDs are intentionally preserved in this pass.
They remain retrieval handles, not current lane-home authority. Renaming those
IDs, legacy Core Spine v0 artifact titles, prompt titles, or replay/proof family
names would be a separate artifact-ID migration with a wider reference blast
radius.

Judgment's demand-read core is not part of this rename. It remains a
Judgment-internal concept under `docs/product/judgment_spine/`.

## Historical Records

Historical migration packages, review records, prompts, receipts, and provenance
artifacts may continue to mention `core_spine/`, `Core Spine`, or
`core_spine_v0_*` when they record prior state. Those mentions should resolve
through this record unless a later migration explicitly rewrites historical
artifact IDs.

## Non-Claims

- Not validation.
- Not readiness.
- Not product proof.
- Not artifact-ID migration.
- Not Judgment demand-read core rename.
