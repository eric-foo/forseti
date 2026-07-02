# Repo Map Retrieval Batches 3-5

```yaml
retrieval_header_version: 1
artifact_role: Workflow retrieval hardening record
scope: Batch 3-5 repo-map retrieval hardening: missing-header triage, recent-change promotion check, and guardrail decision.
use_when:
  - Auditing the repo-map god-tier architecture follow-up after Batch 2.
  - Deciding whether to promote repo-map recent-change notes.
  - Deciding whether to tighten retrieval guardrails after the Windows header-index fix.
open_next:
  - docs/decisions/orca_repo_map_architecture_mgt_v0.md
  - docs/workflows/repo_map_retrieval_probe_batch_2_v0.md
  - docs/workflows/repo_map_recent_changes/README.md
  - .agents/hooks/header_index.py
  - .agents/workflow-overlay/retrieval-metadata.md
authority_boundary: retrieval_only
```

## Source Context

- Worktree: `.codex/worktrees/repo-map-god-tier-architecture-prompt`
- Starting branch state: `codex/repo-map-god-tier-architecture-prompt` clean against `origin/codex/repo-map-god-tier-architecture-prompt`.
- Commission trace: owner instruction in the repo-map PR lane to do Batch 3, Batch 4, Batch 5, then one mega adversarial delegated review; this record is the durable trace for this batch, not independent authorization for future sweeps.
- Batch 2 baseline: `docs/workflows/repo_map_retrieval_probe_batch_2_v0.md` recorded 66 missing headers, 0 orphans, and the Windows `header_index.py --index` encoding defect that was fixed in `.agents/hooks/header_index.py`.
- Governing source: `.agents/workflow-overlay/retrieval-metadata.md` requires headers for new or materially touched durable human-authored workflow artifacts, but explicitly says not to backfill every existing file by default.

## Batch 3 - Missing Header Triage

Observed backlog before this batch:

- `header_index.py --health --verbose`: 66 missing headers, 0 orphans.
- Folder concentration: 34 `docs/review-outputs/`, 20 `docs/prompts/`, 5 `docs/migration/`, 3 `docs/hygiene/`, 2 `docs/workflows/`, 1 `docs/decisions/`, 1 `docs/review-inputs/`.

Patch accepted:

- Add retrieval headers to `docs/workflows/orca_bootstrap_record.md` and `docs/workflows/turn_08_workflow_bedrock_maximization.md` because they are foundational workflow records with future source-loading value.
- Add a retrieval header to `docs/migration/import_queue.md` because it is the bootstrap import boundary record and is directly opened by the bootstrap record.
- Add a retrieval header to `docs/review-inputs/repo_structure_binding_v0_delegated_review_v0/MANIFEST.md` because it is the canonical manifest for a delegated review input bundle.
- Fix `docs/decisions/consultant_loop/milwaukee_initial_judgement.md` from `authority_boundary: non_authoritative` to `authority_boundary: retrieval_only`; the body now carries the explicit non-authority boundary, and the header uses the controlled retrieval boundary.

Deferred by design:

- Historical prompt and review-output backfill remains on-touch unless a separate proof slice authorizes a targeted retrieval sweep.
- Generated migration inventories and moved-path indexes are not promoted by this batch. Under `.agents/workflow-overlay/retrieval-metadata.md`, generated outputs remain header-excluded unless later promoted into a durable Orca artifact role; mere authorization to exist as a generated output is not a header trigger.
- Hygiene packets stay deferred unless they are still live routing queues. In particular, old single-consumption checkpoint or cross-repo handoff material should not be made more prominent without confirming it is still current.

Accepted residual:

- Post-patch `header_index.py --health --oneline`: `retrieval health: 61 missing headers, 0 orphans`.
- The missing-header backlog is not zero. That is intentional: `--health` remains an advisory backlog report, while `--strict` is the forward-only gate for changed durable docs.

## Batch 4 - Recent-Change Promotion Check

Observed state:

- `docs/workflows/repo_map_recent_changes/` contains only `README.md`.
- No one-file recent-change notes were present to promote into the main repo map, a dense submap, or a retrieval header.

Decision:

- No map or submap promotion is needed in this batch.
- Keep the recent-change satellite as a low-conflict optional lane. Future notes should be promoted only when they describe a durable navigation route, not merely because time has passed.

## Batch 5 - Guardrail Decision

Decision:

- Do not add a standing gardener or stricter broad backfill gate in this batch.

Rationale:

- Batch 2 found one concrete guardrail defect: Windows report output could fail on non-ASCII. That was fixed in `header_index.py`.
- The current checker already exposes the residual backlog (`--health`) and gates changed durable docs (`--strict`).
- A standing gardener would add recurring churn and conflict pressure without evidence of repeated missed promotions or stale recent-change notes.

Reconsider this decision if any of these are observed:

- `header_index.py --strict` accepts a materially touched durable doc with no valid retrieval header.
- The recent-change satellite accumulates notes that should have become map routes or dense submap routes.
- A future probe cannot find a high-value artifact within the source-loading budget because it lacks a retrieval header.

## Non-Claims

- This is not validation, readiness, approval, or proof that the repo map is complete.
- This is not a full historical backfill.
- This is not authorization for a standing gardener.
- A passing retrieval/header gate is routing hygiene only.
