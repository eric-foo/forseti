# Forseti

Forseti is separate from `jb` and does not inherit `jb` project assumptions, lifecycle rules, validation rules, product policy, or artifact authority.

Project-specific facts belong in `.agents/workflow-overlay/`. If a fact is not declared there or in a Forseti-owned source document, treat it as `UNKNOWN - requires owner input`.

Explicitly invoked or resolver-loaded skills may provide task-local mechanics only; they are not Forseti project authority.

## Current Authority

- Project overlay: `.agents/workflow-overlay/`
- Docs workspace: `docs/`
- Rename policy: `docs/decisions/forseti_rename_migration_policy_v0.md`
- Bootstrap record: `docs/workflows/orca_bootstrap_record.md`
- Migration import queue: `docs/migration/import_queue.md`

## Current Facts

- Product/domain purpose: outside-in strategic intelligence for public market signals and evidence-backed allocation decisions.
- Legacy project name: Orca.
- Compatibility paths such as `orca/product/` and `orca-harness/` remain live until explicit compatibility migration; `docs/workflows/orca_repo_map_v0.md` is a legacy pointer to the live `docs/workflows/forseti_repo_map_v0.md` map.
- Implementation remains bounded by current-turn or accepted-decision authorization.
