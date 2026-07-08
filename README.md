# Forseti

Forseti is the canonical project identity for this workspace. The workspace was
formerly named Orca; live `orca/` and `orca-harness/` paths are legacy
compatibility roots until a separate physical-root migration moves their
contents.

Forseti is separate from `jb` and does not inherit `jb` project assumptions,
lifecycle rules, validation rules, product policy, or artifact authority.

Project-specific facts belong in `.agents/workflow-overlay/`. If a fact is not
declared there or in a Forseti-owned source document, treat it as
`UNKNOWN - requires owner input`.

Explicitly invoked or resolver-loaded skills may provide task-local mechanics
only; they are not Forseti project authority.

## Current Authority

- Project overlay: `.agents/workflow-overlay/`
- Docs workspace: `docs/`
- Repo route card: `docs/workflows/forseti_repo_map_v0.md`
- Product front door: `forseti/product/README.md`
- Legacy detailed map: `docs/workflows/orca_repo_map_v0.md`
- Legacy product corpus: `orca/product/`
- Legacy runtime harness: `orca-harness/`
- Bootstrap record: `docs/workflows/orca_bootstrap_record.md`
- Migration import queue: `docs/migration/import_queue.md`

## Current Unknowns

- Forseti implementation migration from legacy physical roots: UNKNOWN - requires owner input
- Forseti runtime or automation stack beyond the legacy `orca-harness/` compatibility root: UNKNOWN - requires owner input
- Forseti external integrations: UNKNOWN - requires owner input
