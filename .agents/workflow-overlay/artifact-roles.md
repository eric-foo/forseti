# Artifact Roles

```yaml
retrieval_header_version: 1
artifact_role: Forseti overlay authority
scope: Forseti artifact role bindings, permissions, freshness markers, and paired artifacts.
use_when:
  - Binding an artifact role for Forseti work.
  - Checking artifact permissions or protected roles.
authority_boundary: retrieval_only
```

This file binds reusable artifact-role mechanics to Forseti-owned paths. Generic workflow methods may request these roles, but Forseti owns the concrete permissions, destinations, freshness checks, and validation evidence.

## Role Bindings

| Role | Authoritative source or destination | Read / write permission | Freshness marker | Paired artifacts | Validation evidence |
| --- | --- | --- | --- | --- | --- |
| Forseti overlay authority | `.agents/workflow-overlay/` | Read for all Forseti work; write only for explicit overlay maintenance | File contents plus git status | `AGENTS.md` | Source list and changed overlay files |
| Product thesis authority | `docs/decisions/forseti_product_thesis_evidence_adjudication_v0.md` (supersedes the consumer-demand thesis and beauty-first wedge as current direction, 2026-07-12) | Read for planning; write only when explicitly updating the thesis | Decision ID, status, date, and hash when pinned | Product and feature planning prompts | Source list and decision status |
| Full prompt artifact | `docs/prompts/` or a typed child folder under it | Read/write docs-only prompt drafts | File path, version suffix, source list, and optional hash | Thin wrapper, review input, rerun prompt | Prompt validation gate result |
| Prompt template | `docs/prompts/templates/` | Read/write docs-only Forseti-local prompt templates | Template ID, version suffix, template target if applicable, and registry entry | Template registry, full prompt artifact, thin wrapper | Registry lookup and leakage check |
| Thin wrapper prompt | `docs/prompts/wrappers/` | Read/write docs-only wrapper drafts | Referenced full prompt path and hash or revision | Full prompt artifact | Wrapper-delta check |
| Planning handoff prompt | `docs/prompts/handoffs/` | Read/write docs-only handoff prompts | Work unit ID, target source revision, and output mode | Feature plan, implementation handoff, review input | Preflight check and validation plan |
| Review prompt | `docs/prompts/reviews/` or `docs/review-inputs/` | Read/write review requests; reviewers are read-only unless explicitly assigned patch execution | Source paths, hashes or revisions, and review lane | Review report | Review-lane and source-hash check |
| Rerun or patch prompt | `docs/prompts/reruns/` or `docs/prompts/patches/` | Read/write docs-only retry or patch prompts | Prior artifact path, prior hash or revision, frozen fields, mutable fields | Prior artifact, patch queue, review report | Rerun economy check |
| Review report | `docs/review-outputs/` or a typed child folder under it | Read/write reviewer findings reports; overlay-bound verdicts only when the review lane or prompt binds them | Reviewed artifact path and revision | Review prompt, patch queue | Findings list, review-use boundary, and overlay-bound verdict only when requested |
| Patch queue | `docs/review-inputs/` or `docs/workflows/` | Read/write ordered patch candidates; source changes require separate execution authority | Stable unit IDs and target files | Rerun prompt, review report, implementation handoff | Residual-work and validation-gate mapping |
| Workflow record | `docs/workflows/` | Read/write Forseti workflow records | Date, source list, and hashes when material | Prompt artifacts, decisions, validation notes | Gate evidence and residuals |
| Product artifact | `docs/product/` | Read/write docs-only product contracts, product proof plans, evidence standards, source maps, satellite notes, decision artifacts, memo substrates, evidence appendices, and executive-deck shape drafts | File path, version suffix, source list, and decision status when applicable | Product planning prompts, feature planning prompts, decision records | Product artifact impact classification and source list |
| Research artifact | `docs/research/` | Read/write docs-only public/source research artifacts, evidence-only lane outputs, candidate screens, synthesis reports, backtestability notes, and reject-pattern maps | File path, version suffix, source list, query list, and date boundary when applicable | Product artifacts, decision records, prompt artifacts, backtest-prep notes | Evidence/source list, missing-field labels, synthesis boundary, and non-claims |
| Hygiene queue | `docs/hygiene/` | Read/write docs-only triage queues and cleanup notes | Queue item ID, status, and target destination | Inbox material, prompt artifacts, product artifacts, workflow records | Triage status and promotion or disposal note |
| Inbox scratch | `docs/_inbox/` | Read/write temporary docs-only scratch; not authoritative | Creation note or queue item ID when retained | Hygiene queue | Promotion, archive, deletion, or `not authority` note |

## Protected Roles

- External workflow source outside this workspace is read-only from Forseti work unless a later turn explicitly authorizes external source changes.
- Installed global, user-level, plugin, and project-local skills are deployment copies or tools, not Forseti project authority.
- `jb` project rules, paths, handoffs, GAP/CV Engine policy, lifecycle mechanics, and repo-local skills are not Forseti artifact roles.
- Material in `docs/_inbox/` is not Forseti authority until promoted into an accepted docs folder or overlay file.

## Retrieval Metadata

Durable human-authored workflow artifacts follow the retrieval-header contract
in `.agents/workflow-overlay/retrieval-metadata.md` (which owns applicability
and exclusions). It changes no role binding, permission, freshness marker,
paired artifact, validation evidence, source-of-truth status, or authority
boundary in this file.

## Failure States

- `BLOCKED_UNBOUND_ARTIFACT_ROLE`: a prompt or workflow references a role not listed here or in another accepted Forseti overlay file.
- `BLOCKED_ROLE_PERMISSION`: requested work exceeds the role permission.
- `BLOCKED_ROLE_DRIFT`: a role points to stale, missing, or conflicting evidence.
