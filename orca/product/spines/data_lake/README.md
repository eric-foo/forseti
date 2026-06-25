# Data Lake Spine

```yaml
retrieval_header_version: 1
artifact_role: Spine front-door (Data Lake shared-foundation spine)
scope: >
  Front-door for the data_lake shared_foundation spine: the cross-layer storage
  contracts (raw-packet preservation, keyed retrievability, Attachment Record,
  passive Availability Index, append-only derived-result/ack attachment),
  medallion/gold-readiness contract, and physicality-location contract that
  other spines depend on. R2 populated the spine with the lake contracts and
  canonical mechanics map; the medallion contract now locks the non-physical
  bronze/silver/pre-gold/gold-ready/gold semantics, and placement closeout keeps
  the two repo-structure migration planning docs in docs/migration/ as
  repo-structure migration records.
use_when:
  - Entering the data_lake spine or deciding whether an artifact is lake-owned.
  - Checking the R2-populated authority/workflow routing and placement closeout status.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_data_lake_spine_promotion_binding_v0.md
  - docs/decisions/orca_spine_first_target_structure_binding_v0.md
stale_if:
  - The Data Lake medallion/gold-readiness contract is amended.
  - The data_lake spine shape or its shared_foundation kind is amended.
  - A later accepted placement decision moves the repo-structure migration planning docs into the spine.
```

## What this spine is

`data_lake` is a **shared-foundation spine**: other spines use it, but it owns its
own home because it holds **hard storage contracts**. It is the system's raw-truth
layer.

- **Produced by:** capture.
- **Consumed by:** projection, ECR, signal_statement, cleaning, judgment.
- **Owns:** raw-packet (CapturePacket) preservation, keyed retrievability, the Attachment Record
  contract, the passive Availability Index contract, the append-only
  derived-result / acknowledgement attachment contract, the medallion /
  gold-readiness contract, and the physicality-location contract (external data
  root + directory grammar, not an engine selection).
- **Owns engine posture:** the storage contract does not select an engine today,
  but it now owns the boundary for a later filesystem/database/DuckDB/object-store/
  warehouse/lakehouse or hybrid selection.
- **Does not own:** source-capture execution, Mechanical Source Projection
  semantics, ECR derivation, Signal Statement interpretation, Cleaning
  transforms, Spike Alert implementation,
  Gold-ready evidence assembly implementation, Judgment interpretation, or
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
  implementation), the additive medallion/gold-readiness contract that
  locks bronze/silver/pre-gold/gold-ready/gold semantics, the
  physicality-location contract (external data root, directory grammar, location
  invariants, durable record names, fail-closed resolution), and the three
  blocker-resolution decision contracts (raw admission + key grammar; write-boundary
  enforcement; derived layout + index rebuild) that close the gating physicalization
  blockers — all without selecting an engine/backend, queue, runtime, or Judgment
  behavior.
- `workflows/` — the canonical mechanics map (the version co-authored with the
  contracts, confirmed canonical via a 3-way reconciliation), which **supersedes
  and retires** the transitional `orca/product/shared/data_lake_mechanics/` copy.

Placement closeout (2026-06-20): the 2 repo-structure migration planning docs
(`data_lake_spine_first_migration_{plan,inventory}_v0.md`) intentionally stay in
`docs/migration/` as repo-structure migration records. They are not
lake-specific schema/data migration plans, so they do not move into
`data_lake/migrations/`. `spine.yaml`, `harness/`, and `tests/` stay reserved
until the lake is built.

Non-claims: not validation, readiness, proof, or runtime authorization; placement
shape only.
