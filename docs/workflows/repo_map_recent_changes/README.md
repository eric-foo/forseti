# Repo Map Recent Changes

```yaml
retrieval_header_version: 1
artifact_role: Workflow navigation note index
scope: Low-conflict notes for repo-map-affecting changes that should not be appended to the main repo-map header.
use_when:
  - Recording optional recent-change context after a repo-map-affecting edit.
  - Investigating recent repo-map churn or PR conflicts.
  - Deciding whether a change needs a map route, a submap route, or only retrieval context.
open_next:
  - docs/workflows/forseti_repo_map_v0.md
  - .agents/hooks/check_repo_map_freshness.py
downstream_consumers:
  - repo-map maintainers
  - prompt authors
  - review authors
  - branch owners diagnosing repo-map conflicts
stale_if:
  - docs/workflows/forseti_repo_map_v0.md changes repo-map freshness policy or map metadata rules.
  - .agents/hooks/check_repo_map_freshness.py changes structural trigger behavior.
  - .agents/workflow-overlay/retrieval-metadata.md changes retrieval-header requirements for durable workflow artifacts.
authority_boundary: retrieval_only
```

This folder is the low-conflict place for optional recent-change notes when a
repo-map-affecting change needs durable context but does not need to append a
rolling chronology to `docs/workflows/forseti_repo_map_v0.md`.

Use one small file per change when the context is useful. Do not use this folder
as a substitute for updating the actual map route or delegated submap when
navigation changes. Keep the main repo map's top metadata stable; do not append
rolling `Prior:` chronology there.

```yaml
direction_change_propagation:
  doctrine_changed: >
    Repo-map recent-change chronology moved out of the main map header into
    `docs/workflows/repo_map_recent_changes/`, and the freshness checker now
    gates new direct `orca-harness/` areas instead of every runner/adapter
    basename under already mapped harness folders.
  trigger: workflow_authority
  related_triggers:
    - validation_philosophy
  controlling_sources_updated:
    - docs/workflows/orca_repo_map_v0.md
    - docs/workflows/repo_map_recent_changes/README.md
    - .agents/hooks/check_repo_map_freshness.py
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/source-of-truth.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        AGENTS.md already routes Orca workflow authority and validation mechanics
        through the overlay and repo map; adding this low-level conflict-reduction
        rule there would duplicate map-local policy.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The enforcement-placement principle is unchanged; only one checker's
        high-precision trigger changed from file-level harness units to area-level
        harness navigation.
  stale_language_search: >
    rg -n "Refreshed:.*Prior:|Latest focused addition|PR #542 branch addition|new harness unit|HARNESS_UNIT_GLOBS|new_harness_unit|orca-harness/` runner|or every runner|rolling `Prior:`" docs/workflows/orca_repo_map_v0.md .agents/hooks/check_repo_map_freshness.py docs/workflows/repo_map_recent_changes/README.md .agents/workflow-overlay AGENTS.md
  stale_language_search_result: "No matches."
  non_claims:
    - not validation
    - not readiness
    - not source-of-truth promotion
    - not proof that the repo map is complete
```
