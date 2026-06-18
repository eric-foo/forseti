# Data Lake Spine

```yaml
retrieval_header_version: 1
artifact_role: Spine front-door (Data Lake shared-foundation spine)
scope: >
  Front-door for the data_lake shared_foundation spine: the cross-layer storage
  contracts (raw-packet preservation, keyed retrievability, Attachment Record,
  passive Availability Index, append-only derived-result/ack attachment) that
  other spines depend on. PROMOTION binding only — no content has moved in yet;
  the R2 move pass lands the contracts and the mechanics map.
use_when:
  - Entering the data_lake spine or deciding whether an artifact is lake-owned.
  - Authoring or gating the R2 Data Lake content move.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_data_lake_spine_promotion_binding_v0.md
  - docs/decisions/orca_spine_first_target_structure_binding_v0.md
stale_if:
  - The data_lake spine shape or its shared_foundation kind is amended.
  - The R2 move pass populates the spine (update this front-door then).
```

## What this spine is

`data_lake` is a **shared-foundation spine**: other spines use it, but it owns its
own home because it holds **hard storage contracts**. It is the system's raw-truth
layer.

- **Produced by:** capture.
- **Consumed by:** projection, ECR, signal_statement, cleaning, judgment.
- **Owns:** raw-packet preservation, keyed retrievability, the Attachment Record
  contract, the passive Availability Index contract, and the append-only
  derived-result / acknowledgement attachment contract.
- **Does not own:** the physical backend or storage engine, source-capture
  execution, Mechanical Source Projection semantics, ECR derivation, Signal
  Statement interpretation, Cleaning transforms, Judgment interpretation, or
  queue / retry / scheduling / lane orchestration.

The binding authority is
`docs/decisions/orca_data_lake_spine_promotion_binding_v0.md`.

## Subfolder grammar

| Folder | Holds |
| --- | --- |
| `authority/` | lake contracts, invariants, source-truth rules |
| `workflows/` | operational / read-flow docs (mechanics maps, route cards) |
| `migrations/` | lake-specific schema/data migration plans (not repo migration logs) |
| `harness/` | docs / pointers / specs for harness integration (not runtime code) |
| `tests/` | test strategy / fixtures / spec docs (actual test code stays in `orca-harness/` for now) |

## Status — populated by R2 (2026-06-18)

R2 landed the lake's authority + workflow substance:

- `authority/` — the 3 lake contracts (core, storage, Attachment-Record
  implementation), harvested from the `codex/data-lake-core-contract` lane with
  refs repointed to `orca/product/` paths.
- `workflows/` — the canonical mechanics map (the version co-authored with the
  contracts, confirmed canonical via a 3-way reconciliation), which **supersedes
  and retires** the transitional `orca/product/shared/data_lake_mechanics/` copy.

Deferred: the 2 repo-structure migration planning docs
(`data_lake_spine_first_migration_{plan,inventory}_v0.md`) pending a placement
decision (`docs/migration/` vs `migrations/`). `spine.yaml`, `harness/`, and
`tests/` stay reserved until the lake is built.

Non-claims: not validation, readiness, proof, or runtime authorization; placement
shape only.
