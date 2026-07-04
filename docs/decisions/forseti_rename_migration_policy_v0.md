# Forseti Rename Migration Policy v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Canonical rename policy for the project formerly named Orca.
use_when:
  - Deciding whether a live Orca reference should be renamed to Forseti.
  - Planning compatibility, path, package, skill, hook, or prompt-template rename batches.
  - Auditing remaining Orca references after the authority rename.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/project-authority.md
  - .agents/workflow-overlay/source-of-truth.md
  - .agents/workflow-overlay/source-loading.md
  - docs/workflows/orca_repo_map_v0.md
```

## Decision

The canonical project and product name is **Forseti**. **Orca** is the legacy
pre-rename name.

Live authority, doctrine, current source-loading, validation, review, safety,
artifact-role, and repo-navigation prose should use Forseti. Legacy lowercase
paths, package names, filenames, skill IDs, hook names, and historical artifacts
remain valid until a later compatibility batch explicitly renames or retires
them.

## Rename Classes

| Class | Examples | Rule |
| --- | --- | --- |
| Live authority/doctrine | `AGENTS.md`, `.agents/workflow-overlay/*.md`, current repo-map prose | Rename to Forseti now. Use "formerly Orca" only where transition clarity matters. |
| Current route/index surfaces | `docs/workflows/orca_repo_map_v0.md`, active submaps, current source packs | Rename human-facing prose to Forseti while preserving legacy paths until compatibility migration. |
| Current product/architecture sources | product thesis, active spine contracts, current proof/claim/read-pack docs | Rename in the next product-spine batch unless the file is historical-only. |
| Compatibility names | `orca/product/`, `orca-harness/`, `orca-product-lead`, lowercase `orca_*` filenames, import/package names | Do not rename blindly. Migrate with moved-path indexes, validation, and rollback notes. |
| Historical provenance | old prompts, review outputs, DCP receipts, dated migration notes, prior workstream records | Preserve by default. Add a supersession or alias note only when the artifact remains a live route. |
| Scratch/inbox material | `docs/_inbox/`, unpromoted drafts, contaminated replays | Do not rename by default. Triage only when promoted or used as source. |

## Field And Alias Policy

The forward canonical start-preflight label is `forseti_start_preflight`.
`orca_start_preflight` remains an accepted legacy alias during the compatibility
migration because existing prompts, hooks, and prior artifacts may still emit or
expect it. New live authority should prefer `forseti_start_preflight` and may
name the alias only where compatibility matters.

The file path `docs/workflows/orca_repo_map_v0.md` remains the live repo map
until a later compatibility batch creates and validates a renamed successor.
References to that path are compatibility references, not proof that Orca is
still the project name.

## Batch Plan

1. Authority/doctrine batch: rename live authority prose and add this policy.
2. Product-spine batch: rename current product and architecture source prose
   while preserving historical records.
3. Compatibility/path batch: migrate lowercase paths, packages, filenames,
   skill IDs, hooks, and moved-path indexes with validation and rollback notes.
4. Runtime/tooling batch: repair imports, hook messages, CI, tests, and local
   deployment copies after compatibility renames.
5. Stale-reference audit: classify every remaining `Orca` hit as historical
   provenance, explicit legacy alias, transitional compatibility, or defect.

## Audit Rule

A remaining `Orca` reference is valid only when one of these is true:

- it names historical provenance from before the rename;
- it appears in an explicit "formerly Orca" or legacy-alias statement;
- it is a lowercase compatibility path, package, filename, skill ID, hook name,
  or external identifier not yet migrated;
- it is inside scratch or unpromoted inbox material that is not authority.

Anything else is stale language and should be patched or queued with an owner.

## Non-Claims

- This policy is not validation, readiness, product proof, implementation
  authorization, or source promotion.
- This policy does not rename paths, packages, hooks, skills, or runtime code.
- This policy does not make old historical artifacts incorrect merely because
  they say Orca.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The canonical project/product name is now Forseti; Orca becomes a legacy
    alias. Live authority/doctrine should use Forseti, while historical
    provenance and lowercase compatibility names remain until explicit migration
    batches rename or retire them.
  trigger: workflow_authority
  related_triggers:
    - product_doctrine
    - architecture_doctrine
    - output_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/forseti_rename_migration_policy_v0.md
    - AGENTS.md
    - README.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/project-authority.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/artifact-roles.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - .agents/workflow-overlay/template-registry.md
    - .agents/workflow-overlay/product-proof.md
    - .agents/workflow-overlay/communication-style.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/workflow-overlay/skill-adoption.md
    - docs/workflows/orca_repo_map_v0.md
    - repo-structure.yaml
  downstream_surfaces_checked:
    - CLAUDE.md
    - docs/workflows/orca_repo_map_v0.md
    - repo-structure.yaml
  intentionally_not_updated:
    - path: historical DCP receipt bodies
      reason: >
        Dated receipts are point-in-time provenance and should not be rewritten
        as if the name existed then.
    - path: legacy lowercase compatibility paths and filenames
      reason: >
        Paths such as orca/product/ and docs/workflows/orca_repo_map_v0.md need
        a validated compatibility migration rather than a text-only rename.
    - path: docs/prompts/** and docs/review-outputs/**
      reason: >
        Prompt and review artifacts are historical by default unless a specific
        prompt or review remains a live route surface.
  stale_language_search: >
    rg -in "\bOrca\b|\bORCA\b|orca_start_preflight" AGENTS.md README.md
    .agents/workflow-overlay docs/workflows/orca_repo_map_v0.md
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not implementation authorization
    - not a path/package/runtime rename
```
