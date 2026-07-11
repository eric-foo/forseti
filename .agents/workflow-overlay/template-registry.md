# Template Registry

```yaml
retrieval_header_version: 1
artifact_role: Forseti overlay authority
scope: Forseti-owned prompt template registry for project-local templates.
use_when:
  - Resolving which Forseti prompt template should be used.
  - Checking whether prompt-orchestrator template fallback is allowed.
authority_boundary: retrieval_only
```

This registry binds Forseti-local prompt templates. Reusable prompt-orchestrator
mechanics may use the registry for template discovery, but Forseti owns the
template paths, template targets, output modes, artifact roles, and non-claim
boundaries.

Model-target templates (`_generic/`) were retired 2026-06-13 (unused; owner decision). Only model-neutral templates remain registered.

## Registry Rules

- Check this registry before using any generic prompt-orchestration fallback template.
- Template files live under `docs/prompts/templates/`.
- Do not copy `jb` prompt templates, GAP/CV Engine paths, lifecycle mechanics,
  product policy, validation habits, or handoff rules.
- Generic layout ideas from external templates are allowed only after binding to
  Forseti paths, roles, output modes, validation gates, and non-claims.
- Template targets are prompt-shaping labels only. They do not recommend,
  require, rank, or route runtime model choice.
- Implementation templates are unbound by default. Use them only when the
  current turn or an accepted Forseti decision explicitly authorizes a bounded
  implementation scope and binds the target files, output mode, and non-claims.

## Registered Templates

| Template kind | Primary path | Template target | Output mode | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| `shared-behavior-contract` | `docs/prompts/templates/shared/forseti_prompt_behavior_contract_v0.md` | model-neutral | template include | active | Common behavior clauses for Forseti prompt templates. |
| `shared-preflight-defaults` | `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md` | model-neutral | template include | active | Repo-constant preflight field bindings; required per-prompt deltas must still be stated. |
| `research-evidence-lane-o3` | `docs/prompts/templates/research/o3_evidence_only_research_lane_v0.md` | o3 / o3-deep-research prompt posture | paste-ready-chat | active | Evidence-only public research lane template. |
| `research-synthesis-gpt55` | `docs/prompts/templates/research/gpt_5_5_evidence_synthesis_v0.md` | GPT-5.5 prompt posture | paste-ready-chat | active | Synthesis from prior evidence-only lane outputs. |
| `adversarial-artifact-review` | `docs/prompts/templates/review/adversarial_artifact_review_v0.md` | model-neutral | review-report or paste-ready-chat | active | Read-only non-code artifact review prompt template. |
| `thin-wrapper` | `docs/prompts/templates/wrappers/thin_wrapper_v0.md` | model-neutral | paste-ready-chat or file-write | active | Wrapper around an existing prompt or source artifact. |
| `delegated-review-return-adjudication` | `docs/prompts/templates/review/delegated_review_return_adjudication_v0.md` | model-neutral | chat-only or file-write | active | Chief Architect adjudication template for delegated review-and-patch returns; adjudicates findings/diff/verdict as claims, batches admin into one land step, and derives material moves only from a visible active goal. |
| `portable-adversarial-artifact-review-method` | `docs/prompts/templates/portable/adversarial_artifact_review_portable_method_v0.md` | model-neutral | paste-ready-chat | active | Self-contained, model-agnostic review METHOD only for no_repo reviewers without repository, skill, or overlay access; cross-vendor/external/couriered status alone does not select it. Ship the delimited PORTABLE METHOD block as review-package component (c). Derived from `adversarial-artifact-review` template + review-lanes doctrine; re-derive on source-hash change. |

## Unbound Template Kinds

- `direct-implementation`: unbound by default; available only when a current
  turn or accepted Forseti decision explicitly authorizes bounded implementation.
- `repo-code-review`: unbound unless implementation or code review is explicitly authorized.
- `automation-runtime`: forbidden until a later explicit implementation turn or
  accepted Forseti decision names that runtime scope.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Shared prompt-template identity now uses Forseti-named primary paths for the
    preflight defaults and behavior contract; the old Orca-named paths are
    compatibility pointers for historical prompts and source packs only.
  trigger: workflow_authority
  related_triggers:
    - output_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - .agents/workflow-overlay/template-registry.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/source-loading.md
    - docs/prompts/templates/shared/forseti_preflight_defaults_v0.md
    - docs/prompts/templates/shared/forseti_prompt_behavior_contract_v0.md
    - docs/prompts/templates/shared/orca_preflight_defaults_v0.md
    - docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/prompts/templates/review/adversarial_artifact_review_v0.md
    - docs/prompts/templates/research/o3_evidence_only_research_lane_v0.md
    - docs/prompts/templates/research/gpt_5_5_evidence_synthesis_v0.md
    - docs/prompts/templates/wrappers/thin_wrapper_v0.md
    - docs/prompts/templates/README.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
  intentionally_not_updated:
    - path: historical prompts, review inputs, review outputs, and DCP archive entries
      reason: >
        Those files preserve provenance or source-pack hashes and resolve through
        the compatibility pointers; rewriting them would fabricate history.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Its old shared-behavior-contract path appears inside a historical DCP
        receipt and remains accurate as provenance through the compatibility
        pointer.
  stale_language_search: >
    rg -n "orca_preflight_defaults_v0.md|orca_prompt_behavior_contract_v0.md|orca_start_preflight|projects\\orca"
    .agents/workflow-overlay docs/prompts/templates docs/workflows/forseti_repo_map_v0.md docs/workflows/forseti_post_harness_migration_status_v0.md
  stale_language_search_result: >
    Active overlay and template surfaces now point to Forseti-named shared
    template paths; remaining old shared-template path hits in the checked
    live-authority set are compatibility pointers or historical DCP provenance.
    `orca_start_preflight` remains documented only as a legacy compatibility
    alias, and old `projects/orca` workspace paths remain only in historical or
    legacy-workspace status text.
  non_claims:
    - not validation
    - not readiness
    - not prompt execution
    - not historical prompt rewrite
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
