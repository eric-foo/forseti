# Safety Rules

```yaml
retrieval_header_version: 1
artifact_role: Forseti overlay authority
scope: Project-specific safety rules, forbidden drift, authorization boundaries, and rollback limits for Forseti work.
use_when:
  - Checking whether an action is forbidden drift or needs explicit authorization (implementation, runtime, commit, push, external-folder, or skill edits).
  - Confirming fail-visible behavior, scope discipline, or rollback boundaries before acting.
authority_boundary: retrieval_only
```

## Project-Specific Safety

- Fail visibly when required Forseti authority is missing.
- Do not substitute `jb` paths, product facts, lifecycle rules, or validation gates.
- Do not create software implementation, runtime systems, packages, tests, deployed automation, or source-system buildout unless the current turn or an accepted Forseti decision explicitly authorizes a bounded implementation scope.
- Bounded implementation authorization is not blanket runtime authority. Stay inside the named scope, preserve the bounded third-tranche scope for anti-detect/proxy/JS-challenge work, and preserve separate gates for commercial fetch services, storage, dashboards, deployment, ECR, Cleaning, Judgment, commits, pushes, and PRs.
- Do not mutate external reference folders during import planning.
- Do not edit installed global skills, user-level skills, plugin cache files, or external workflow source unless a later turn explicitly authorizes it.
- Forseti-local candidate skill drafting or iteration may proceed only through the
  controlled lane in `.agents/workflow-overlay/skill-adoption.md`. That lane
  does not authorize global, user-level, plugin, installed, or external workflow
  source mutation.
- Do not configure remotes or perform destructive cleanup unless explicitly authorized. Commit, push, and pull-request preparation follow the work-unit completion rule in `AGENTS.md`: at the verified completion of a repo-changing work unit on the lane's own branch or worktree they proceed without a typed instruction, owner-gated by the `settings.json` permission prompts; landing to `main` stays human-gated except a guard-verified self-merge of the agent's own PR (every other state fails closed). The guard (`.agents/hooks/guard_protected_actions.py`) is the enforcement; the conditions and policy live in `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`.
- **Online/external source-data capture routes through the Source Capture Armory Runner Ladder.** Any capture of online or external source data for evidence or learning goes through the armory runners + Mini God-Tier source-quality discipline (the "Runner Ladder"), not ad-hoc web fetches; captures emit inspectable Source Capture Packets that also serve as Capture-lane data. Route via the repo map (`docs/workflows/forseti_repo_map_v0.md` -> Data Capture / Source Capture Armory submap) -> `orca-harness/docs/source_capture_agent_runbook.md` + `forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md`. Uncaptured scouting/diagnostic web reads (not entered as evidence) are exempt.

## Scope Discipline

**Smallest complete intervention** -- and the interpretation of any "smallest
complete X" phrasing (fix, patch, edit, rewrite, refactor, review, answer) -- is
defined canonically in `AGENTS.md` § "Smallest Complete Intervention". That
definition is repo-wide and all-agent; this overlay defers to it and does not
restate it. The overlay's only role here is to apply that rule to Forseti scope
discipline: bounded intervention, justified adjacency, and no speculative
extras.

## Rollback Boundary

Rollback for this bootstrap is additive: remove the newly created Forseti directory only with explicit user approval. No rollback step may edit `jb`, installed skills, user-level skills, plugin skills, or external reference folders.

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
    - "forseti/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md"
    - "forseti/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_method_plan_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
    - "forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
    - "docs/decisions/data_capture_spine_source_observability_local_support_implementation_execution_authorization_v0.md"
  intentionally_not_updated:
    - path: "AGENTS.md"
      reason: "Already states Orca is no longer globally docs-first and permits bounded implementation by current turn or accepted handoff."
    - path: ".agents/workflow-overlay/source-of-truth.md"
      reason: "Source hierarchy and propagation mechanics did not change."
    - path: "forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Capture obligations did not change; implementation still requires separate bounded authorization."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "Already supplies the bounded first-tranche Source Capture Armory implementation authority."
    - path: "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
      reason: "Already routes future Source Capture Armory work through the bounded first-tranche authorization and non-claims."
    - path: "docs/decisions/data_capture_spine_source_observability_local_support_implementation_execution_authorization_v0.md"
      reason: "That prior local-helper authorization remains accurate and bounded to its helper surface."
  stale_language_search: "rg -n \"non-implementation architecture and proof setup|Orca remains in its non-implementation phase|exit the non-implementation phase|Implementation templates remain unbound while Orca is in non-implementation|direct-implementation.*unbound while Orca remains in non-implementation|No build, no install, no runtime authorized\" .agents/workflow-overlay forseti/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md forseti/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_method_plan_v0.md docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md forseti/product/spines/capture/core/source_capture_toolbox/README.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not blanket implementation authorization"
    - "not API, commercial-scraper, anti-detect, proxy, or production-runtime authorization"
    - "not ECR, Cleaning, or Judgment design"
```

```yaml
direction_change_propagation:
  doctrine_changed: "Captures of online/external source data must route through the Source Capture Armory Runner Ladder (armory runners + Mini God-Tier source-quality discipline), not ad-hoc web fetches; emitted Source Capture Packets double as Capture-lane data. This is a behavioral routing rule that points to the existing armory owners via the repo map; the armory mechanics, source-access boundaries, and capture authorizations are unchanged. Uncaptured scouting/diagnostic web reads are exempt."
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - ".agents/workflow-overlay/safety-rules.md"
  downstream_surfaces_checked:
    - "docs/workflows/orca_repo_map_v0.md"
    - "orca-harness/docs/source_capture_agent_runbook.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
  intentionally_not_updated:
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Already routes capture/armory work to the Data Capture submap, runbook, and runner/adapter files; this rule points to that existing route rather than forking it."
    - path: "orca-harness/docs/source_capture_agent_runbook.md"
      reason: "Owns the Runner Ladder mechanics and runner selection; this rule routes to it and changes none of it."
    - path: "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
      reason: "Owns the Mini God-Tier rungs/result tokens; referenced, not changed."
  non_claims:
    - "not new capture authorization"
    - "not a source-access boundary change"
    - "not an armory mechanics change"
    - "not ECR, Cleaning, or Judgment authority"
```
