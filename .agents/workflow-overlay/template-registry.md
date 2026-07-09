# Template Registry

```yaml
retrieval_header_version: 1
artifact_role: Orca overlay authority
scope: Forseti-owned prompt template registry for project-local templates.
use_when:
  - Resolving which Orca prompt template should be used.
  - Checking whether prompt-orchestrator template fallback is allowed.
authority_boundary: retrieval_only
```

This registry binds Forseti-local prompt templates. Reusable prompt-orchestrator
mechanics may use the registry for template discovery, but Orca owns the
template paths, template targets, output modes, artifact roles, and non-claim
boundaries.

Model-target templates (`_generic/`) were retired 2026-06-13 (unused; owner decision). Only model-neutral templates remain registered.

## Registry Rules

- Check this registry before using any generic prompt-orchestration fallback template.
- Template files live under `docs/prompts/templates/`.
- Do not copy `jb` prompt templates, GAP/CV Engine paths, lifecycle mechanics,
  product policy, validation habits, or handoff rules.
- Generic layout ideas from external templates are allowed only after binding to
  Orca paths, roles, output modes, validation gates, and non-claims.
- Template targets are prompt-shaping labels only. They do not recommend,
  require, rank, or route runtime model choice.
- Implementation templates are unbound by default. Use them only when the
  current turn or an accepted Orca decision explicitly authorizes a bounded
  implementation scope and binds the target files, output mode, and non-claims.

## Registered Templates

| Template kind | Primary path | Template target | Output mode | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| `shared-behavior-contract` | `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md` | model-neutral | template include | active | Common behavior clauses for Orca prompt templates. |
| `shared-preflight-defaults` | `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` | model-neutral | template include | active | Repo-constant preflight field bindings; required per-prompt deltas must still be stated. |
| `research-evidence-lane-o3` | `docs/prompts/templates/research/o3_evidence_only_research_lane_v0.md` | o3 / o3-deep-research prompt posture | paste-ready-chat | active | Evidence-only public research lane template. |
| `research-synthesis-gpt55` | `docs/prompts/templates/research/gpt_5_5_evidence_synthesis_v0.md` | GPT-5.5 prompt posture | paste-ready-chat | active | Synthesis from prior evidence-only lane outputs. |
| `adversarial-artifact-review` | `docs/prompts/templates/review/adversarial_artifact_review_v0.md` | model-neutral | review-report or paste-ready-chat | active | Read-only non-code artifact review prompt template. |
| `thin-wrapper` | `docs/prompts/templates/wrappers/thin_wrapper_v0.md` | model-neutral | paste-ready-chat or file-write | active | Wrapper around an existing prompt or source artifact. |
| `portable-adversarial-artifact-review-method` | `docs/prompts/templates/portable/adversarial_artifact_review_portable_method_v0.md` | model-neutral | paste-ready-chat | active | Self-contained, model-agnostic review METHOD for repo-agnostic / cross-family reviewers with no skill/overlay access; ship the delimited PORTABLE METHOD block as review-package component (c). Derived from `adversarial-artifact-review` template + review-lanes doctrine; re-derive on source-hash change. |

## Unbound Template Kinds

- `direct-implementation`: unbound by default; available only when a current
  turn or accepted Orca decision explicitly authorizes bounded implementation.
- `repo-code-review`: unbound unless implementation or code review is explicitly authorized.
- `automation-runtime`: forbidden until a later explicit implementation turn or
  accepted Orca decision names that runtime scope.
