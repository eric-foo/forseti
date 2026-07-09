# Core Spine v0 Data Lake Derived Layout + Index Rebuild Decision Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture decision contract
scope: >
  Resolves the Data Lake derived-side foundation layout: the append-only addressing
  grammar for derived records, acknowledgements, and decision-evidence assembly
  receipts; the supersession model; the index-rebuild guarantee (indexes/availability
  rebuilds from committed raw + attachment keys/hashes; all of indexes/ is disposable);
  and the on-demand-analysis extensibility that keeps cross-object analysis derivable
  without pre-building it. The derived_retrieval population stays governance-gated.
use_when:
  - Scoping where derived records, acks, and assembly receipts physically live and how they are addressed.
  - Scoping the index rebuild command or checking the rebuildability guarantee.
  - Checking whether a cross-object or on-demand analysis has a home without new lake structure.
open_next:
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
downstream_consumers:
  - physical data-lake storage/implementation lane
  - availability index rebuild lane
  - projection/ECR/SCR/Cleaning/Judgment derived-record lanes
  - decision-evidence assembly lane
stale_if:
  - A later accepted serialization, manifest, or backend decision changes the derived addressing or rebuild semantics.
  - The Data Lake Core, Storage, or Physicality contract changes the derived-attachment or index boundary.
  - A later owner decision makes any index authoritative or non-rebuildable.
authority_boundary: retrieval_only
```

## Status

`DERIVED_LAYOUT_INDEX_REBUILD_DECISION_RECORDED_V0`. Resolves Physicality Location
Contract blocker 4 (derived/ack/receipt physical home + write boundary) and blocker 5
(index rebuild command + rebuildability guarantee; availability now, derived_retrieval
rebuild governance-gated/build-deferred).

Owner-adopted 2026-06-21 (owner "lets adopt that" after adjudication of the derived-
layout blocker-resolution lane report, FULL_REPO_READ). Architecture decision contract
only: not implementation authority, validation, readiness, serialization, backend, or
per-lane schema selection.

## Decision In One Screen

```text
Derived records, acknowledgements, and assembly receipts are append-only,
one-record-per-file, keyed first to a raw anchor, then a lane-owned namespace,
then a unique record id. Corrections are new records, never rewrites.
All of indexes/ is rebuildable from committed material, or it is not an index.
Cross-object / on-demand analysis lives as rebuildable derived_retrieval views or
assembly receipts referencing a set of refs -- not as new lake structure.
```

## Derived Record Addressing

Lock the relationship (not serialization):

```text
derived/<raw-anchor>/<lane-namespace>/<record-id>
```

- `<raw-anchor>` includes `packet_id` and may narrow to `slice_id`, `file_id`, or
  `attachment_key`.
- `<lane-namespace>` is lane-owned and collision-safe, but the contract must not
  enumerate or freeze the lane taxonomy into the lake path.
- `<record-id>` is create-only, one-record-per-file (not a mutable append log); the
  record body repeats the raw anchors and hashes needed for verification.

Each epistemic kind stays a sibling (projection receipt / ECR / SCR / Cleaning ledger /
Judgment output), never a merged cross-kind blob.

## On-Demand Analysis And Extensibility

This grammar addresses **per-object** derived records. Cross-object, aggregate,
cross-time, or otherwise on-demand "powerful analysis" is a first-class supported
capability and has a home **without new lake structure**:

- It lives as a rebuildable `indexes/derived_retrieval/` view (non-authoritative,
  rebuilt from committed `derived/` + raw refs) or as a decision-evidence assembly
  view/receipt that references a **set** of raw + derived refs.
- It is never forced into the single-anchor `derived/` grammar and never becomes lake
  authority.
- The foundation preserves on-demand derivability by design: raw is immutable and
  complete, derived is append-only and re-derivable (re-derive, never migrate), and
  indexes are rebuildable. New analysis types are added as new derived records or
  rebuildable views; they do not require migration of existing material.
- The real limiting factor on future analysis is capture completeness, not lake
  structure: what was not captured cannot be derived. Coverage limits, residuals, and
  raw-pull flags must travel with derived/assembly outputs.
- Guardrails that hold as analysis grows: on-demand analysis stays non-authoritative
  and rebuildable, stays non-Judgment (it assembles evidence, it does not decide), and
  stays object-level — cross-comparison is of source objects, never a person dossier;
  the actor slice remains governed by the adopted actor-retrieval governance decision.

## Acknowledgement Addressing

```text
acknowledgements/<raw-anchor>/<ack-namespace>/<ack-record-id>
```

Acknowledgements are lane-owned facts keyed to raw, one create-only record per fact;
correction is a new ack record. The lake must not consume acks as control flow for
scheduling, gating, retry, or downstream calls.

## Receipt Home

`DecisionEvidenceAssemblyReceipt` lives under `derived/` (not `acknowledgements/`, not
`indexes/`). It carries `judgment_status: not_evaluated` or an equivalent non-Judgment
marker, the assembly profile/version used, raw + derived refs, and
residuals/omissions/raw-pull flags. The transient assembly view is computed on demand
and may be cached rebuildably under `indexes/derived_retrieval/`.

## Supersession Model

Corrections, invalidation, supersession, conflict, and ignore-prior relations are
expressed only by new append-only records that reference the prior record id and raw
anchor. Prior derived, ack, attachment, or raw material is never rewritten or deleted
in place.

## Index Rebuild Contract

Command shape (non-executable here):

```text
lake indexes rebuild --root <ORCA_DATA_ROOT> --target availability|derived_retrieval|all --prove-rebuildability
```

- `availability` rebuilds only from committed raw packet + attachment key/ref/hash/
  hash_basis material and stays content-free and passive.
- `derived_retrieval` rebuilds only from committed `derived/` + raw refs and remains
  non-authoritative, governance-gated, and build-deferred.
- The prove-rebuildability check fails if any `indexes/` entry cannot be regenerated
  from committed raw/attachment/derived material, or if `availability` contains
  routing, priority, success, actor-history, dossier, or analytic content. Any
  `indexes/` content that cannot be regenerated from committed material is not an
  index.

## Accepted Residuals

- Serialization and exact segment encoding open (relationship locked); trigger:
  manifest/record-writer implementation scoping.
- Lane namespaces not globally enumerated (avoid taxonomy lock-in); trigger: the first
  lane needs a durable namespace-registration rule.
- No backend/queue/scheduler/engine (by-key discovery is authority); trigger: scan/query
  latency proves insufficient.
- `derived_retrieval` population deferred (rebuildable, non-authoritative,
  governance-gated); trigger: a governed consumer needs a reverse lookup.
- No per-lane record schemas (only the physical relationship is locked); trigger: each
  lane's own record contract.

## Deferred / Out Of Scope

Exact serialization, manifest/version shape, sidecar/member layout, backend,
queue/scheduler, per-lane record schemas, the `derived_retrieval` builder/population,
validation suite, and implementation route.

## Non-Claims

Not validation, readiness, approval, or implementation authorization. Not serialization,
manifest, backend, or per-lane schema selection. No queue/engine. No `derived_retrieval`
population. No Judgment/gold semantics in receipts. No actor-retrieval design. Records a
derived-layout + index-rebuild decision only.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Derived Layout + Index Rebuild Decision Contract v0 resolves the derived-side
    foundation layout: derived records, acknowledgements, and assembly receipts are
    append-only one-record-per-file, keyed raw-anchor -> lane-namespace -> record-id
    (taxonomy not frozen into paths); corrections are new records; receipts are
    non-Judgment under derived/; all of indexes/ is rebuildable-or-not-an-index with a
    prove-rebuildability check (availability from raw+attachment; derived_retrieval from
    derived, governance-gated); and cross-object/on-demand analysis lives as rebuildable
    derived_retrieval views or assembly receipts referencing a set of refs, preserving
    on-demand derivability without new lake structure.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
    - forseti/product/spines/data_lake/README.md
  downstream_surfaces_checked:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not serialization, backend, or per-lane schema selection
    - not derived_retrieval population
```
