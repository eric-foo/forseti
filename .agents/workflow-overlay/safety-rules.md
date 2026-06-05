# Safety Rules

## Project-Specific Safety

- Fail visibly when required Orca authority is missing.
- Do not substitute `jb` paths, product facts, lifecycle rules, or validation gates.
- Do not create software implementation, runtime systems, packages, tests, deployed automation, or source-system buildout unless the current turn or an accepted Orca decision explicitly authorizes a bounded implementation scope.
- Bounded implementation authorization is not blanket runtime authority. Stay inside the named scope, preserve the bounded third-tranche scope for anti-detect/proxy/JS-challenge work, and preserve separate gates for commercial fetch services, storage, dashboards, deployment, ECR, Cleaning, Judgment, commits, pushes, and PRs.
- Do not mutate external reference folders during import planning.
- Do not edit installed global skills, user-level skills, plugin cache files, or external workflow source unless a later turn explicitly authorizes it.
- Orca-local candidate skill drafting or iteration may proceed only through the
  controlled lane in `.agents/workflow-overlay/skill-adoption.md`. That lane
  does not authorize global, user-level, plugin, installed, or external workflow
  source mutation.
- Do not commit, push, configure remotes, create pull requests, or perform destructive cleanup unless explicitly authorized.

## Scope Discipline

**Smallest complete intervention** -- and the interpretation of any "smallest
complete X" phrasing (fix, patch, edit, rewrite, refactor, review, answer) -- is
defined canonically in `AGENTS.md` § "Smallest Complete Intervention". That
definition is repo-wide and all-agent; this overlay defers to it and does not
restate it. The overlay's only role here is to apply that rule to Orca scope
discipline: bounded intervention, justified adjacency, and no speculative
extras.

## Rollback Boundary

Rollback for this bootstrap is additive: remove the newly created Orca directory only with explicit user approval. No rollback step may edit `jb`, installed skills, user-level skills, plugin skills, or external reference folders.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "Orca is no longer globally in non-implementation architecture/proof setup: bounded implementation, packages, and tests may proceed when explicitly authorized by the current turn or an accepted Orca decision, while default work remains docs/decision work and separate gates remain intact."
  trigger: lifecycle_boundary
  controlling_sources_updated:
    - ".agents/workflow-overlay/project-authority.md"
    - ".agents/workflow-overlay/safety-rules.md"
    - ".agents/workflow-overlay/template-registry.md"
    - ".agents/workflow-overlay/validation-gates.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
    - "docs/decisions/data_capture_spine_source_observability_local_support_implementation_execution_authorization_v0.md"
  intentionally_not_updated:
    - path: "AGENTS.md"
      reason: "Already states Orca is no longer globally docs-first and permits bounded implementation by current turn or accepted handoff."
    - path: ".agents/workflow-overlay/source-of-truth.md"
      reason: "Source hierarchy and propagation mechanics did not change."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Capture obligations did not change; implementation still requires separate bounded authorization."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "Already supplies the bounded first-tranche Source Capture Armory implementation authority."
    - path: "docs/product/source_capture_toolbox/README.md"
      reason: "Already routes future Source Capture Armory work through the bounded first-tranche authorization and non-claims."
    - path: "docs/decisions/data_capture_spine_source_observability_local_support_implementation_execution_authorization_v0.md"
      reason: "That prior local-helper authorization remains accurate and bounded to its helper surface."
  stale_language_search: "rg -n \"non-implementation architecture and proof setup|Orca remains in its non-implementation phase|exit the non-implementation phase|Implementation templates remain unbound while Orca is in non-implementation|direct-implementation.*unbound while Orca remains in non-implementation|No build, no install, no runtime authorized\" .agents/workflow-overlay docs/product/data_capture_source_access_boundary_decision_v0.md docs/product/data_capture_source_access_method_plan_v0.md docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md docs/product/source_capture_toolbox/README.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not blanket implementation authorization"
    - "not API, commercial-scraper, anti-detect, proxy, or production-runtime authorization"
    - "not ECR, Cleaning, or Judgment design"
```
