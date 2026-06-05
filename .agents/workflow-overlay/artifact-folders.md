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
- `docs/product/`: product contracts, product proof plans, core-spine notes, satellite notes, evidence standards, source maps, decision artifacts, memo substrates, evidence appendices, and executive-deck shape drafts.
- `docs/product/source_capture_toolbox/`: product-facing Source Capture Armory design notes, scoped specs, and gap notes. Existing controlling Data Capture source-access decisions, method plans, and obligation contracts remain at their historical paths unless a later migration decision moves them.
- `docs/research/`: public/source research artifacts, evidence-only lane outputs, synthesis reports, candidate screens, and reject-pattern maps that support Orca product or proof work without becoming product authority by default.
- `docs/research/judgment-spine/harness/v0_14/smoke_tests/`: Judgment Harness v0.14 no-case smoke-test receipts and operator provenance records. Artifacts in this folder are plumbing evidence only and do not become real-case probe, validation, fixture-admission, product-proof, or judgment-quality evidence by location.
- `docs/hygiene/`: triage queues and cleanup notes for Orca artifacts.
- `docs/_inbox/`: non-authoritative temporary holding area for scratch prompts, notes, imports, and untriaged material.

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
- Do not copy or move material from external reference folders unless a later turn explicitly authorizes the import.

## Direction Change Propagation - Source Capture Armory Product Folder

```yaml
direction_change_propagation:
  doctrine_changed: "The Source Capture Armory product-doc folder convention is now bound in the overlay folder authority while existing controlling Data Capture source-access documents remain at their historical paths."
  trigger: output_authority
  controlling_sources_updated:
    - ".agents/workflow-overlay/artifact-folders.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "docs/product/README.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
  intentionally_not_updated:
    - path: ".agents/workflow-overlay/artifact-roles.md"
      reason: "The existing Product artifact role covers Source Capture Armory design notes and scoped specs; this patch binds folder routing, not a new artifact role."
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "Source-access boundary permission and hard stops did not change."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Data Capture obligations did not change."
  stale_language_search: "rg -n \"source_capture_toolbox|Source Capture Armory\" .agents/workflow-overlay/artifact-folders.md docs/product/README.md docs/product/source_capture_toolbox/README.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md docs/product/data_capture_source_access_method_plan_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not implementation authorization"
    - "not source-access boundary amendment"
    - "not ECR, Cleaning, or Judgment design"
```

## Direction Change Propagation - No-Case Smoke Tests Folder

```yaml
direction_change_propagation:
  doctrine_changed: >
    The Judgment Harness v0.14 now has a narrow accepted folder for no-case
    smoke-test receipts and operator provenance records, with a permanent
    plumbing-only/non-gate-clearing boundary.
  trigger: output_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/artifact-folders.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
    - docs/decisions/no_case_smoke_test_authorization_pending_parameters_v0.md
    - docs/review-outputs/adversarial-artifact-reviews/no_case_smoke_test_authorization_pending_parameters_adversarial_artifact_review_v0.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/artifact-roles.md
      reason: >
        Existing Research artifact and Workflow record roles already cover the
        receipt/provenance distinction; this patch only binds a narrower folder.
    - path: docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
      reason: >
        The checklist already requires exact receipt/provenance paths and keeps
        smoke artifacts non-gate-clearing; no semantic update is required.
  stale_language_search: >
    rg -n "smoke_tests|no-case smoke|SMOKE_NOCASE_|gate-clearing|fixture admission|judgment-quality"
    .agents/workflow-overlay/artifact-folders.md
    docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
    docs/decisions/no_case_smoke_test_authorization_pending_parameters_v0.md
  non_claims:
    - not validation
    - not readiness
    - not live-call authorization
    - not fixture admission
    - not judgment-quality proof
```
