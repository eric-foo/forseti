# Orca Workflow Overlay

This overlay is the project authority for Orca. Reusable workflow methods may provide mechanics, but Orca-specific facts and constraints must come from this folder or another Orca-owned source named here.

## Overlay Sections

- `project-authority.md`: project identity, boundary, and unknown facts.
- `source-of-truth.md`: Orca source hierarchy, conflict rules, and doctrine-change propagation contract.
- `artifact-folders.md`: accepted docs-first artifact locations.
- `artifact-roles.md`: role bindings, permissions, freshness markers, and paired artifacts.
- `prompt-orchestration.md`: lightweight Orca prompt artifact, wrapper, preflight, output mode, and rerun rules.
- `communication-style.md`: Orca response style for Chief Architect sequencing, review closeouts, and prompt handoffs.
- `validation-gates.md`: checks required before claiming completion.
- `review-lanes.md`: read-only and executor lane rules.
- `safety-rules.md`: project-specific safety and forbidden drift.
- `skill-adoption.md`: skill source, shadow, and adoption status.

## Binding Rule

If reusable workflow guidance conflicts with this overlay for Orca project facts, this overlay wins unless a later accepted Orca decision supersedes it.

Missing required project facts are `UNKNOWN - requires owner input`; do not fill them from `jb` or generic defaults.
