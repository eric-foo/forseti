# Source Of Truth

## Current Source Hierarchy

1. Explicit user instruction for the current turn.
2. Orca `AGENTS.md`.
3. This overlay under `.agents/workflow-overlay/`.
4. Orca docs under `docs/`, when they do not conflict with the overlay.
5. Future accepted `agent-workflow` reusable workflow-kernel source for generic mechanics only.

## Conflict Rules

- Orca overlay wins for Orca project facts.
- Future `agent-workflow` source may own reusable workflow mechanics, not Orca facts.
- Installed global/user/plugin skills are runtime copies or external tools, not Orca project authority.
- If a required source is missing, report a visible failure and name the missing file or decision.

## Doctrine Change Propagation Contract

Doctrine-changing work is any source-changing edit that changes a durable rule
future agents may follow for product doctrine, architecture doctrine, workflow
authority, validation philosophy, review authority, output authority, or a
lifecycle boundary.

Use these trigger values:

- `product_doctrine`
- `architecture_doctrine`
- `workflow_authority`
- `validation_philosophy`
- `review_authority`
- `output_authority`
- `lifecycle_boundary`

Before claiming completion for doctrine-changing work, update the controlling
source and check the downstream source-loaded surfaces that could continue to
route agents by stale doctrine. At minimum, consider:

- top-level agent instructions such as `AGENTS.md` and `CLAUDE.md`;
- the controlling overlay file under `.agents/workflow-overlay/`;
- start-route and source-loading surfaces such as
  `.agents/workflow-overlay/source-loading.md` and
  `docs/workflows/orca_repo_map_v0.md`;
- executor, prompt, validation, review, and closeout surfaces when the doctrine
  affects them.

Store the propagation evidence inline in the changed artifact, prompt, handoff,
or final closeout. Do not create a standalone receipt file, new skill,
registry, broad template sweep, or automation for this loop unless a later turn
explicitly authorizes that expansion.

Use this receipt shape:

```yaml
direction_change_propagation:
  doctrine_changed: "<one sentence>"
  trigger: product_doctrine | architecture_doctrine | workflow_authority | validation_philosophy | review_authority | output_authority | lifecycle_boundary
  controlling_sources_updated:
    - "<path>"
  downstream_surfaces_checked:
    - "<path>"
  intentionally_not_updated:
    - path: "<path>"
      reason: "<why unchanged>"
  stale_language_search: "<query or not_run + why>"
  non_claims:
    - "not validation"
    - "not readiness"
```

If propagation cannot be completed, return an explicit blocker instead of a
completion claim:

```yaml
direction_change_propagation_blocker:
  doctrine_changed: "<one sentence>"
  trigger: product_doctrine | architecture_doctrine | workflow_authority | validation_philosophy | review_authority | output_authority | lifecycle_boundary
  blocking_surface: "<missing, conflicting, or unchecked path/source>"
  attempted_check: "<what was attempted>"
  allowed_next_step: "<narrow action that would unblock propagation>"
  non_claims:
    - "not validation"
    - "not readiness"
```

The receipt or blocker is propagation evidence only. It is not validation,
readiness, approval, acceptance, proof, implementation authorization, or source
promotion.

## Known Source Documents

- `README.md`: workspace entrypoint.
- `AGENTS.md`: agent operating instructions.
- `CLAUDE.md`: Claude-specific instruction shim; subordinate to `AGENTS.md` and the Orca overlay for Orca project authority.
- `.agents/workflow-overlay/README.md`: overlay entrypoint.
- `.agents/workflow-overlay/artifact-roles.md`: Orca artifact role bindings for reusable workflow methods.
- `.agents/workflow-overlay/prompt-orchestration.md`: Orca prompt artifact, wrapper, preflight, output mode, validation, and rerun bindings.
- `.agents/workflow-overlay/communication-style.md`: Orca response style for Chief Architect sequencing, review closeouts, and prompt handoffs.
- `docs/STRUCTURE.md`: docs-folder usage guide for future agents; subordinate to this overlay if conflicts appear.
- `docs/workflows/orca_bootstrap_record.md`: Turn 6 bootstrap record.
- `docs/migration/import_queue.md`: read-only import queue state.
- `docs/decisions/turn_08_product_thesis_v0.md`: current Orca product thesis and value proposition.
- `docs/workflows/turn_08_workflow_bedrock_maximization.md`: docs-first maximization plan for `workflow-deep-thinking`, future `workflow-product-ultraplan`, and future `workflow-feature-ultraplan`.
