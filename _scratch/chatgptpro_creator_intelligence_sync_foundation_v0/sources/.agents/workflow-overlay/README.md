# Orca Workflow Overlay

```yaml
retrieval_header_version: 1
artifact_role: Orca overlay authority
scope: Overlay entrypoint and binding rule for Orca project work.
use_when:
  - Starting Orca project work.
  - Resolving which overlay section owns a project rule.
authority_boundary: retrieval_only
```

This overlay is the project authority for Orca. Skills may provide task-local mechanics, but Orca-specific facts and constraints must come from this folder or another Orca-owned source named here.

## Overlay Sections

- `project-authority.md`: project identity, boundary, and unknown facts.
- `source-of-truth.md`: Orca source hierarchy, conflict rules, and doctrine-change propagation contract.
- `source-loading.md`: source-loading budgets, read packs, and context-bloat controls.
- `decision-routing.md`: Cynefin Routing Layer for non-trivial, ambiguous, cross-thread, delegated, doctrine-bearing, or messy-worktree work.
- `artifact-folders.md`: accepted Orca artifact locations.
- `artifact-roles.md`: role bindings, permissions, freshness markers, and paired artifacts.
- `retrieval-metadata.md`: lightweight retrieval-header contract for durable human-authored workflow artifacts.
- `prompt-orchestration.md`: lightweight Orca prompt artifact, wrapper, preflight, output mode, and rerun rules.
- `template-registry.md`: Orca-owned prompt template registry for project-local templates.
- `product-proof.md`: buyer-proof semantics, trust-objection handling, pull signals, zero-spoiler backtest behavior, and product-proof non-claims.
- `communication-style.md`: Orca response style for Chief Architect sequencing, review closeouts, and prompt handoffs.
- `validation-gates.md`: checks required before claiming completion.
- `review-lanes.md`: read-only review lanes, patch/integration execution boundaries, and template retrieval rules.
- `delegated-review-patch.md`: provisional, opt-in Delegated Review-and-Patch convention for high-stakes authored artifacts, and the overlay-interface fields a future skill implementation may read. Not a bound review lane.
- `safety-rules.md`: project-specific safety and forbidden drift.
- `skill-adoption.md`: skill source, shadow, and adoption status.

## Binding Rule

If external workflow guidance or skill mechanics conflict with this overlay for Orca project facts, this overlay wins unless a later accepted Orca decision supersedes it.

Missing required project facts are `UNKNOWN - requires owner input`; do not fill them from `jb` or generic defaults.
