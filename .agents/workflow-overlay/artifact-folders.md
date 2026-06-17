# Artifact Folders

```yaml
retrieval_header_version: 1
artifact_role: Orca overlay authority
scope: Accepted Orca artifact folders and folder rules.
use_when:
  - Deciding where Orca artifacts belong.
  - Checking whether a folder is authoritative, scratch, or forbidden.
authority_boundary: retrieval_only
```

## Accepted Folders

- `docs/decisions/`: Orca decision records.
- `docs/prompts/`: Orca prompt artifacts.
- `docs/prompts/product-planning/`: product planning prompt drafts.
- `docs/prompts/feature-planning/`: feature planning prompt drafts.
- `docs/prompts/deep-thinking/`: deep reasoning prompt drafts.
- `docs/prompts/handoffs/`: implementation handoff prompt drafts.
- `docs/prompts/reviews/`: review prompt drafts.
- `docs/prompts/reruns/`: rerun prompt drafts.
- `docs/prompts/patches/`: patch prompt drafts.
- `docs/prompts/wrappers/`: thin wrapper prompts that reference full prompt artifacts.
- `docs/prompts/templates/`: Orca-local prompt templates and template README files, subordinate to `.agents/workflow-overlay/template-registry.md`.
- `docs/review-inputs/`: artifacts prepared for review.
- `docs/review-outputs/`: reviewer findings reports and overlay-bound verdicts.
- `docs/review-outputs/adversarial-artifact-reviews/`: adversarial artifact review reports.
- `docs/workflows/`: workflow records, repo maps, validation notes, and operational records owned by Orca.
- `docs/migration/`: migration and import queue records.
- `docs/product/`: product contracts, product proof plans, Foundation Layer notes, satellite notes, evidence standards, source maps, decision artifacts, memo substrates, evidence appendices, and executive-deck shape drafts.
- `docs/product/source_capture_toolbox/`: product-facing Source Capture Armory design notes, scoped specs, and gap notes. Existing controlling Data Capture source-access decisions, method plans, and obligation contracts remain at their historical paths unless a later migration decision moves them.
- `docs/product/search/`: Orca's demand-signal intelligence (search-led) lane - search / answer-engine surfaces (web search / SERP, AI Overviews and other answer engines, zero-click, AEO/GEO, search-interest) PLUS the demand-signal discovery method (scan core, read taxonomy, demand gates) they feed, bound by `docs/decisions/orca_search_product_lane_binding_v0.md`. Membership is set by that record's inclusion test; topic-primacy wins over spine placement for those docs. The method docs are search-led but venue-spanning (consumed across judgment, capture, and Foundation Layer work).
- `docs/product/` lane subfolders (`foundation/`, `data_capture_spine/`, `judgment_spine/`, `signal_content/`, `ecr/`, `product_lead/`, `search/`): the bound second-level axis for product artifacts per `docs/decisions/orca_repo_structure_binding_v0.md` (and, for the `search/` topic lane, `docs/decisions/orca_search_product_lane_binding_v0.md`). New product artifacts use the matching lane; files matching no lane may stay at `docs/product/` root. Existing flat files move only via a migration package, not ad hoc.
- `repo-structure.yaml` (repo root): the machine structure map - router only, consumed by `.agents/hooks/check_placement.py` and agents for navigation. It declares homes and never states rules; this overlay file remains the placement authority and wins on conflict.
- `docs/research/`: public/source research artifacts, evidence-only lane outputs, synthesis reports, candidate screens, and reject-pattern maps that support Orca product or proof work without becoming product authority by default.
- `docs/research/judgment-spine/harness/v0_14/smoke_tests/`: Judgment Harness v0.14 no-case smoke-test receipts and operator provenance records. Artifacts in this folder are plumbing evidence only and do not become real-case probe, validation, fixture-admission, product-proof, or judgment-quality evidence by location.
- `docs/hygiene/`: triage queues and cleanup notes for Orca artifacts.
- `docs/_inbox/`: non-authoritative temporary holding area for scratch prompts, notes, imports, and untriaged material.
- `.agents/skills/`: Orca-local accepted/candidate workflow skill source (for example, `orca-product-lead`), governed by `.agents/workflow-overlay/skill-adoption.md`. Orca-local only; this is NOT plugin, user-level, installed, or external skill source, and living here does not deploy, activate, or make a skill resolver-visible.

## Rules

- Keep durable Orca artifacts under `docs/` unless a later Orca decision creates a narrower folder.
- Full prompt artifacts and thin wrappers must follow `.agents/workflow-overlay/prompt-orchestration.md`.
- New or materially touched durable human-authored workflow artifacts must
  follow `.agents/workflow-overlay/retrieval-metadata.md` unless that contract
  excludes the artifact class.
- Treat `docs/_inbox/` as scratch only. Nothing in `_inbox` is Orca authority until promoted into an accepted docs folder or overlay file.
- Track parked or temporary material through `docs/hygiene/queue.md` when it may need promotion, review, archiving, or deletion.
- Keep product artifacts in `docs/product/` unless they are accepted decision records, prompt artifacts, workflow records, review artifacts, or migration records.
- Keep research artifacts in `docs/research/` when the primary purpose is source discovery, corpus qualification, evidence gathering, candidate screening, or rejected-source mapping. Promote research conclusions into `docs/product/` or `docs/decisions/` only through a later accepted product or decision artifact.
- Do not create implementation folders such as `src`, `app`, `packages`, `tests`, or automation runtimes until explicitly authorized.
- Orca-local workflow skills live only under `.agents/skills/` and are governed by `.agents/workflow-overlay/skill-adoption.md`; acceptance there is a local freeze, not deployment, and must not edit plugin, user-level, installed, or external skill source.
- Do not copy or move material from external reference folders unless a later turn explicitly authorizes the import.
- Placement is checked at the write boundary by `.agents/hooks/check_placement.py` (EP-04, advisory; `--strict` commit/CI mode available), which reads `repo-structure.yaml` as its only rule source. A passing check is placement shape only - never validation, readiness, or authority. Parameters and invariants: `docs/decisions/orca_repo_structure_binding_v0.md`.

## Direction Change Propagation - Foundation Layer Rename v0

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca renames the top-level market-agnostic Core Spine product lane/home to
    Foundation Layer (`docs/product/foundation/`) while preserving legacy
    `core_spine_v0_*` artifact IDs for retrieval continuity; Judgment
    demand-read core and historical provenance records are not renamed.
  trigger: output_authority
  related_triggers:
    - product_doctrine
    - workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/artifact-folders.md
    - docs/decisions/orca_repo_structure_binding_v0.md
    - repo-structure.yaml
  downstream_surfaces_checked:
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/product-proof.md
    - docs/product/README.md
    - docs/STRUCTURE.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/workflows/ecr_spine_submap_v0.md
    - docs/decisions/pre_capture_discovery_spine_charter_recommendation_v0.md
    - docs/decisions/orca_search_product_lane_binding_v0.md
    - docs/migration/foundation_layer_rename_v0.md
    - live docs/prompts/research/decisions full-path sweep excluding migration, review snapshots, and hygiene logs
  intentionally_not_updated:
    - path: docs/product/foundation/core_spine_v0_* basenames
      reason: >
        Legacy artifact IDs are preserved for retrieval continuity; this pass
        renames the lane/home and canonical prose only.
    - path: legacy Core Spine v0 artifact titles, prompt titles, and replay/proof family names
      reason: >
        These labels are coupled to preserved `core_spine_v0_*` artifact IDs and
        prior method-validation/proof family history; a full title/family rename
        is a separate artifact-ID migration.
    - path: docs/product/judgment_spine/*demand_read_core*
      reason: >
        Judgment demand-read core is a distinct Judgment-internal concept and
        was intentionally not renamed.
    - path: docs/migration/repo_structure_phase2_consolidation_v0/**
      reason: >
        Historical Phase-2 migration package; original `core_spine/` source
        paths remain historical truth and resolve through
        docs/migration/foundation_layer_rename_v0.md.
    - path: docs/review-inputs/** and docs/review-outputs/**
      reason: historical review/provenance artifacts; not live navigation.
  stale_language_search: >
    rg -n "Core Spine|docs/product/core_spine/|`core_spine/`|name: core_spine"
    .agents docs repo-structure.yaml --glob "*.md" --glob "*.yaml" --glob "*.yml" --glob "*.json"
  non_claims:
    - not validation
    - not readiness
    - not artifact-ID migration
    - not Judgment demand-read core rename
```
Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
