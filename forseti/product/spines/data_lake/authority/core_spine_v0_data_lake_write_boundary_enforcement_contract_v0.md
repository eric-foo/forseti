# Core Spine v0 Data Lake Write-Boundary Enforcement Decision Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture decision contract
scope: >
  Resolves the schema-agnostic Data Lake enforcement blockers: a single
  deterministic lake-writer boundary that enforces write-once raw and append-only
  derived/ack; fail-closed ORCA_DATA_ROOT resolution with a per-root identity
  marker; by-key discovery preserved as authority before any queue; SCR
  FamilyDetailBase kept off the raw-payload path; and no-new-core-field pressure.
use_when:
  - Scoping the lake write path, data-root resolution, or availability rebuild.
  - Checking whether a write path bypasses the deterministic boundary or selects a queue/engine.
open_next:
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
downstream_consumers:
  - physical data-lake storage/implementation lane
  - data-root configuration/runtime lane
  - availability index rebuild lane
stale_if:
  - The Physicality Location Contract changes the data-root or fail-closed rule.
  - The Data Lake Storage or Core contract changes write/read discipline or by-key authority.
  - A later owner decision selects a backend/queue that changes the write boundary.
authority_boundary: retrieval_only
```

## Status

`WRITE_BOUNDARY_ENFORCEMENT_DECISION_RECORDED_V0`. Resolves Physicality Location
Contract blockers 3 (enforcement assignment), 9 (SCR FamilyDetailBase governance),
10 (by-key authority), and 11 (fail-closed + marker + test override).

Owner-adopted 2026-06-21 (owner "proceed" after adjudication of the write-boundary
blocker-resolution lane report). Architecture decision contract only: not
implementation authority, validation, readiness, backend/queue selection, or
serialization.

## Decision In One Screen

```text
All lake writes go through one deterministic lake-writer boundary.
It resolves the root fail-closed, verifies a per-root identity marker, rejects paths
outside the resolved root, refuses raw overwrite, and allows only create-only
appends for derived and acknowledgement records.
By-key discovery stays authority; availability stays passive and rebuildable.
Enforcement is mechanical at the write/byte boundary, not reliant on reviewer discipline.
```

## Enforcement Placement

Enforce at the deterministic lake-writer/tool boundary (not actor memory or
convention):

- `raw/<packet_id>/`: create-only; an existing target path/hash/manifest identity is
  a hard fail (write-once).
- `derived/` and `acknowledgements/`: append-only create; no replace, delete, or
  in-place rewrite.
- every write: canonicalize the target, reject any path outside the resolved root,
  reject traversal/symlink escape, and reject a lake write path that calls a
  downstream lane.
- no-cleaning: the lake writer accepts preserved raw, references, and derived
  metadata only; Cleaning transforms stay outside lake core.

Reviewer convention is a backstop, never the enforcement mechanism.

## Fail-Closed Contract

**Production resolution precedence:** explicit/per-run root -> `ORCA_DATA_ROOT` ->
optional config-file fallback. A test root is injected **only in test mode** as an
explicit test input; it is never a production precedence tier or runtime fallback. (A
test override placed after config would be a silent-write hazard.)

Resolution fails closed — refuse to write and surface the failure — when the root is:
unset, unresolvable, not mounted (removable media absent), inside the repo working
tree, missing its marker, marker identity mismatches the configured/expected root,
not a directory, not writable, or the canonical target escapes the root.

## Root Marker Contract

The marker is a per-root **identity**, not mere presence:

- a root-local marker file carrying a `root_uuid`, contract version, and optional label;
- the writer compares `root_uuid` against the configured/expected root identity before
  every write session;
- writes use same-directory temp write -> flush -> atomic rename into the final path
  -> parent-directory flush where supported;
- for create-only paths, the rename fails if the destination already exists.

The exact marker file format and platform flush mechanics are implementation; the
per-root-identity and atomic-create intent is contract-level.

## By-Key Authority

By-key discovery is authority and is affirmed, not changed: downstream lanes find
committed work by key even if an event is missed; a queue may optimize notification
but is never the source of truth; availability is content-free passive committed
state; the Availability Index is rebuildable from committed packet/attachment
key/ref/hash material. No lake write/read path pushes, routes, or calls a downstream
lane.

## SCR FamilyDetailBase Governance

`FamilyDetailBase` is SCR-local derived structure only — not a raw source-family
payload home. It may carry SCR-family derived detail by reference to
packet/slice/attachment keys, but must not embed source-family payload bodies that
belong in Attachment Records. (Consistent with the SCR derivation plan keeping
`family_detail` dormant/None in v0.)

## No-New-Core-Field Enforcement

A deterministic schema/tool gate rejects new direct source-family payload fields on
`SourceCapturePacket`, `SourceCaptureSlice`, or lake-core manifest/index structures
unless a later owner decision cites a cross-family promotion rule. Convenience or
first-consumer pressure is insufficient; incumbent direct fields are legacy-readable,
not precedent.

## Accepted Residuals

No storage backend, no queue/engine, no derived/ack physical home, no
manifest/version serialization, no runtime implementation, no readiness claim — each
named and accepted now (MGT). Upgrade triggers: physical-store selection;
derived-record physical-home decision; storage-code implementation scoping.

## Deferred / Out Of Scope

Storage backend, manifest version, member/sidecar layout, lawful erasure/WORM,
queue/engine, derived-record and acknowledgement physical homes, migration/replay for
incumbent fields, and runtime tests.

## Non-Claims

Not implementation authorization, validation, or readiness. Not storage-engine,
queue, or scheduler selection. Not raw key grammar (owned by the raw admission + key
grammar contract). Not schema finalization. Records an enforcement + resolution
decision only.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Write-Boundary Enforcement Decision Contract v0 resolves the schema-agnostic
    enforcement blockers: one deterministic lake-writer boundary enforces write-once
    raw and append-only derived/ack; root resolution is fail-closed with a per-root
    identity marker and atomic create-only writes; production precedence is explicit >
    ORCA_DATA_ROOT > config with a test root injected only in test mode (never a
    runtime fallback); by-key discovery stays authority; SCR FamilyDetailBase is kept
    off the raw-payload path; and no-new-core-field pressure is gated.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
    - forseti/product/spines/data_lake/README.md
  downstream_surfaces_checked:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not backend/queue/scheduler selection
    - not raw key grammar
```
