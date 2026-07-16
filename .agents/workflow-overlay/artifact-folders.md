# Artifact Folders

```yaml
retrieval_header_version: 1
artifact_role: Forseti overlay authority
scope: Accepted Forseti artifact folders and folder rules.
use_when:
  - Deciding where Forseti artifacts belong.
  - Checking whether a folder is authoritative, scratch, or forbidden.
authority_boundary: retrieval_only
```

## Accepted Folders

- `docs/decisions/`: Forseti decision records.
- `docs/prompts/`: Forseti prompt artifacts.
- `docs/prompts/product-planning/`: product planning prompt drafts.
- `docs/prompts/feature-planning/`: feature planning prompt drafts.
- `docs/prompts/deep-thinking/`: deep reasoning prompt drafts.
- `docs/prompts/handoffs/`: implementation handoff prompt drafts.
- `docs/prompts/reviews/`: review prompt drafts.
- `docs/prompts/reruns/`: rerun prompt drafts.
- `docs/prompts/patches/`: patch prompt drafts.
- `docs/prompts/wrappers/`: thin wrapper prompts that reference full prompt artifacts.
- `docs/prompts/templates/`: Forseti-local prompt templates and template README files, subordinate to `.agents/workflow-overlay/template-registry.md`.
- `docs/review-inputs/`: artifacts prepared for review.
- `docs/review-outputs/`: reviewer findings reports and overlay-bound verdicts.
- `docs/review-outputs/adversarial-artifact-reviews/`: adversarial artifact review reports.
- `docs/workflows/`: workflow records, repo maps, validation notes, and operational records owned by Forseti.
- `docs/migration/`: migration and import queue records.
- `forseti/product/` (repo root): the **spine-first product tree** for product contracts, product proof plans, core-spine notes, satellite notes, evidence standards, source maps, decision artifacts, memo substrates, evidence appendices, executive-deck shape drafts, Source Capture Toolbox design notes, and demand-signal method/surface docs. The tree is bound by `docs/decisions/forseti_spine_first_target_structure_binding_v0.md` and authorized by `docs/decisions/forseti_spine_first_blocker_authorization_v0.md` (#254). Second-level axis: `spines/` (`foundation/`, `commission_signal_board/`, `scanning/`, `capture/`, `creator_signal/`, `ecr/`, `cleaning/`, `judgment/`, `product_lead/`, `data_lake/`), `satellites/`, `case_families/`, `information/` (`company_surface/`), and `shared/`. `information/` holds reusable, decision-agnostic product-information contracts only: actual records remain in Data Lake-owned storage and operational work remains in the owning spine. `creator_signal/` is a product-signal spine promotion-bound 2026-06-28 by `docs/decisions/forseti_creator_signal_spine_promotion_binding_v0.md` for product-facing creator intelligence surfaces over Capture-owned creator records. `data_lake/` is a shared-foundation spine promotion-bound 2026-06-18 by `docs/decisions/forseti_data_lake_spine_promotion_binding_v0.md` (R2 landed the contracts + mechanics into authority/+workflows/ and retired shared/data_lake_mechanics/; the 2 #239 repo-structure planning docs stay in `docs/migration/` as migration records). Per-product-area structure is owned by the spine-first binding, not the machine map; `check_placement.py` treats `forseti/` as a declared top-level area via `repo-structure.yaml`. Historical `docs/product/` references resolve through `docs/migration/repo_structure_spine_first_v0/moved_paths_index.md` by design. `docs/doctrine/` is intentionally NOT created by this migration (owner B3: index/router-only, seeded later).
- `repo-structure.yaml` (repo root): the machine structure map - router only, consumed by `.agents/hooks/check_placement.py` and agents for navigation. It declares homes and never states rules; this overlay file remains the placement authority and wins on conflict.
- `docs/research/`: public/source research artifacts, evidence-only lane outputs, synthesis reports, candidate screens, and reject-pattern maps that support Forseti product or proof work without becoming product authority by default.
- `docs/research/judgment-spine/harness/v0_14/smoke_tests/`: Judgment Harness v0.14 no-case smoke-test receipts and operator provenance records. Artifacts in this folder are plumbing evidence only and do not become real-case probe, validation, fixture-admission, product-proof, or judgment-quality evidence by location.
- `docs/hygiene/`: triage queues and cleanup notes for Forseti artifacts.
- `docs/_inbox/`: non-authoritative temporary holding area for scratch prompts, notes, imports, and untriaged material.
- `.agents/skills/`: Forseti-local accepted/candidate workflow skill source (for example, `forseti-product-lead`; legacy wrappers such as `orca-product-lead` only when bound by skill-adoption.md), governed by `.agents/workflow-overlay/skill-adoption.md`. Forseti-local only; this is NOT plugin, user-level, installed, or external skill source, and living here does not deploy, activate, or make a skill resolver-visible.
- `.agents/tools/`: small repository-owned utilities operated directly by agents; each tool must stay bounded to its named workflow failure, fail visibly, and expose its own usage and focused self-test. This is not a hook, daemon, plugin, runtime service, or general automation home.

## Rules

- Keep durable Forseti artifacts under `docs/` unless a later Forseti decision creates a narrower folder.
- Full prompt artifacts and thin wrappers must follow `.agents/workflow-overlay/prompt-orchestration.md`.
- New or materially touched durable human-authored workflow artifacts must
  follow `.agents/workflow-overlay/retrieval-metadata.md` unless that contract
  excludes the artifact class.
- Treat `docs/_inbox/` as scratch only. Nothing in `_inbox` is Forseti authority until promoted into an accepted docs folder or overlay file.
- Track parked or temporary material through `docs/hygiene/queue.md` when it may need promotion, review, archiving, or deletion.
- Keep product artifacts in `forseti/product/` unless they are accepted decision records, prompt artifacts, workflow records, review artifacts, or migration records.
- Keep research artifacts in `docs/research/` when the primary purpose is source discovery, corpus qualification, evidence gathering, candidate screening, or rejected-source mapping. Promote research conclusions into `forseti/product/` or `docs/decisions/` only through a later accepted product or decision artifact.
- Do not create implementation folders such as `src`, `app`, `packages`, `tests`, or automation runtimes until explicitly authorized.
- Forseti-local workflow skills live only under `.agents/skills/` and are governed by `.agents/workflow-overlay/skill-adoption.md`; acceptance there is a local freeze, not deployment, and must not edit plugin, user-level, installed, or external skill source.
- Do not copy or move material from external reference folders unless a later turn explicitly authorizes the import.
- Placement is checked at the write boundary by `.agents/hooks/check_placement.py` (EP-04, advisory; `--strict` commit/CI mode available), which reads `repo-structure.yaml` as its only rule source. A passing check is placement shape only - never validation, readiness, or authority. Parameters and invariants: `docs/decisions/forseti_repo_structure_binding_v0.md`.
