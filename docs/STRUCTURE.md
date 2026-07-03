# Forseti Docs Structure

```yaml
retrieval_header_version: 1
artifact_role: Docs usage guide
scope: Docs folder usage guide for future Forseti agents.
use_when:
  - Deciding where a Forseti artifact belongs.
  - Promoting material out of docs/_inbox.
authority_boundary: retrieval_only
```

This file is a quick navigation guide for future agents. It is not a complete
file inventory and does not create folder authority. The Forseti overlay in
`.agents/workflow-overlay/` remains the authority if anything here conflicts
with it.

## Rule Of Thumb

Keep durable Forseti artifacts under `docs/` or the overlay unless a later Forseti
decision creates a narrower location. Do not create implementation folders,
runtimes, packages, tests, scrapers, or automation unless a later turn
explicitly authorizes implementation.

## Core Folders

- `docs/decisions/`: accepted or proposed decision records.
- `orca/product/`: spine-first product tree for product contracts, Core Spine notes, satellite notes, evidence standards, source maps, proof plans, decision artifacts, memo substrates, evidence appendices, executive-deck shape drafts, Source Capture Toolbox notes, and demand-signal method/surface docs. Historical `docs/product/` paths resolve via `docs/migration/repo_structure_spine_first_v0/moved_paths_index.md`.
- `docs/prompts/`: reusable prompt artifacts and typed prompt families.
- `docs/research/`: public/source research artifacts, evidence-only lane outputs, synthesis reports, candidate screens, backtestability notes, and rejected-source maps.
- `docs/review-inputs/`: artifacts prepared for review.
- `docs/review-outputs/`: reviewer reports and verdicts.
- `docs/workflows/`: workflow records, repo maps, validation notes, and operational records.
- `docs/migration/`: migration and import planning records.
- `docs/hygiene/`: triage queues and cleanup notes.
- `docs/_inbox/`: temporary holding area for untriaged prompts, notes, imports, and scratch material.

## Prompt Folders

Accepted prompt-family folders are bound by
`.agents/workflow-overlay/prompt-orchestration.md` and
`.agents/workflow-overlay/artifact-folders.md`:

- `docs/prompts/product-planning/`: product planning prompt drafts.
- `docs/prompts/feature-planning/`: feature planning prompt drafts.
- `docs/prompts/deep-thinking/`: deep reasoning prompt drafts.
- `docs/prompts/handoffs/`: implementation handoff prompt drafts.
- `docs/prompts/reviews/`: review prompt drafts.
- `docs/prompts/reruns/`: retry prompts that preserve frozen decisions.
- `docs/prompts/patches/`: patch prompt drafts; applying patches needs separate authority.
- `docs/prompts/wrappers/`: thin wrapper prompts that reference full prompt artifacts.
- `docs/prompts/templates/`: Forseti-local prompt templates, subordinate to `.agents/workflow-overlay/template-registry.md`.

Template child folders such as `_generic/`, `research/`, `review/`, `shared/`,
and `wrappers/` are navigation aids under `docs/prompts/templates/`; check the
template registry before relying on a template.

`docs/prompts/hygiene-queue/` exists in the current working tree, but it is not
listed as an accepted prompt-family folder in the overlay. Treat it as drift or
parked material until a hygiene entry or overlay-maintenance decision resolves
it.

## Review Output Folders

Use `docs/review-outputs/` for reviewer reports and verdicts. Typed child
folders are navigation aids for durable workstreams:

- `docs/review-outputs/adversarial-artifact-reviews/`: adversarial artifact review reports.
- `docs/review-outputs/method-validation/`: Core Spine method-validation reviews.
- `docs/review-outputs/proof/`: proof-prep, proof-run, and proof-packet reviews.

Other typed review-output folders must still obey the review role bindings in
`.agents/workflow-overlay/artifact-roles.md` and any local README in
`docs/review-outputs/`.

## Research Folders

Use `docs/research/` for evidence gathering, corpus qualification, candidate
screening, reject-pattern mapping, and synthesis. Research artifacts do not
become product authority by default.

The current research corpus subtree is
`docs/research/consulting-judgment-corpus/`, with child folders for
`backtestability/`, `candidate-screens/`, `lane-outputs/`, `prompts/`,
`reject-patterns/`, and `synthesis/`.

## Core And Satellite Product Work

Use `orca/product/` for the Core + Satellite model:

- Core Spine artifacts define market-agnostic evidence mechanics.
- Satellite artifacts define decision-specific and domain-specific context.
- Client 0 `jb` material is a satellite proof case, not the product center.

Do not promote `jb`-specific assumptions into core unless a product artifact explicitly argues why the concept generalizes.

## Retrieval Metadata

For new or materially touched durable human-authored workflow artifacts, follow
the retrieval-header contract in
`.agents/workflow-overlay/retrieval-metadata.md`.

The header is for source loading only. It must not create or imply authority,
validation proof, approval, readiness, lifecycle completion, deployment status,
install status, resolver status, or edit permission.

## Inbox And Hygiene

`docs/_inbox/` is not authoritative. Material placed there must be promoted, archived, deleted, or left explicitly parked through `docs/hygiene/queue.md` when it matters.

Use this promotion rule:

- product truth -> `orca/product/` or `docs/decisions/`
- research evidence, shortlist screens, and reject-pattern maps -> `docs/research/`
- prompt artifact -> `docs/prompts/`
- workflow record -> `docs/workflows/`
- review input or output -> `docs/review-inputs/` or `docs/review-outputs/`
- migration/import note -> `docs/migration/`

If an item is useful but unresolved, keep it in `_inbox/` and add a hygiene queue entry.
