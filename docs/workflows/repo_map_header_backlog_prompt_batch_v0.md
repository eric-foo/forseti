# Repo Map Header Backlog Prompt Batch v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow retrieval hardening record
scope: First targeted reduction of the remaining repo-map retrieval-header backlog after PR #554.
use_when:
  - Auditing the first post-PR-554 missing-header backlog reduction batch.
  - Deciding why prompt artifacts were patched before old review outputs or generated migration records.
  - Continuing the remaining retrieval-header backlog without broad backfill.
open_next:
  - docs/decisions/orca_repo_map_architecture_mgt_v0.md
  - docs/workflows/repo_map_retrieval_batches_3_5_v0.md
  - .agents/workflow-overlay/retrieval-metadata.md
authority_boundary: retrieval_only
```

## Batch Scope

Commission trace: owner instruction to work on the 61 remaining missing retrieval headers after PR #554 merged.

Starting health:

- `header_index.py --health --verbose`: 61 missing headers, 0 orphans.
- Backlog split: 20 prompt artifacts, 34 review outputs, 3 hygiene packets, 4 generated migration index/inventory files.

Accepted first slice:

- Add or normalize compact retrieval headers for the 20 missing `docs/prompts/` artifacts.
- Use the prompt title and folder role as the source of the header scope; four files already had older `prompt_only` boundaries and were normalized to `retrieval_only`.
- Keep headers retrieval-only: no readiness, validation, approval, source-of-truth, or execution claims.

Rationale:

- Prompt artifacts are durable human-authored workflow artifacts under `.agents/workflow-overlay/retrieval-metadata.md`.
- They are high retrieval value because future agents need to find the right prompt, review prompt, rerun prompt, or handoff quickly.
- This is a separately commissioned, category-bounded retrieval slice, not a repo-wide default backfill.

Deferred:

- Historical review outputs remain for later batches; many are large and should be grouped by review family or current retrieval demand.
- Hygiene packets remain deferred until their live routing value is confirmed.
- Generated migration moved-path indexes and inventories remain deferred because generated outputs are header-excluded unless later promoted into a durable Forseti artifact role.

Observed post-patch residual:

- This batch reduced advisory health from 61 missing headers to 41 missing headers, with 0 orphans.
- The remaining backlog is still advisory, not validation failure or readiness evidence.

## Non-Claims

- Not validation, readiness, approval, or proof that repo-map retrieval health is clean.
- Not a full historical backfill.
- Not authorization for a standing gardener or broad header sweep.
- Not a map or submap change; these prompt files live under already mapped prompt folders.
