# Core Spine v0 Data Lake Consumption Seam Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture decision contract
scope: >
  The shared derived-lane consumption seam: how every derived lane (Silver,
  ECR, cleaning, projection) picks up committed Bronze work and acknowledges
  completion the same tested way; the acknowledgement namespace rule; the
  conformance obligations any lane pickup implementation must pass; the
  derived_retrieval rebuild-command binding for the gate-opened object-level
  views; and the on-demand-first metrics policy with metric families
  operator_to_fill.
use_when:
  - Wiring a derived lane's work discovery or completion acknowledgement.
  - Implementing or reviewing a pickup path, ack write, or the indexes rebuild runner.
  - Checking the precompute-vs-on-demand posture for a metrics view.
open_next:
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_consumption_seam_scoping_route_v0.md
stale_if:
  - The storage, derived-layout, or write-boundary contract changes by-key authority, the ack grammar, or the index rebuild guarantee.
  - A later accepted decision names the first metric families or changes the on-demand-first posture.
  - A later owner decision supersedes the seam helper or conformance contract.
authority_boundary: retrieval_only
```

## Status

`CONSUMPTION_SEAM_V0_CONTRACT_RECORDED`. Authored under the accepted
consumption-seam scoping route (STEP-02) with owner-granted bounded
implementation authorization (2026-07-02). Architecture/behavior contract
only: not validation, readiness, acceptance, engine/backend/queue selection,
or metric-family selection.

This contract adds the seam layer only. Pickup authority, ack grammar,
write-once/append-only enforcement, and index rebuildability are owned by the
contracts cited in each section; this artifact binds to them and does not
restate or fork them.

## Decision In One Screen

```text
One helper, one test contract, zero lake-core changes.

Pickup   = by-key scan of committed availability, minus anchors whose current
           obligation fingerprint is already acknowledged. Always reconcile;
           never trust a view; heavy packet loading only for undone anchors.
Ack      = append-only lane-owned record in acknowledgements/, namespace =
           a lane name already declared in lane_registry.LANE_ROLES.
Views    = rebuildable caches under indexes/derived_retrieval/object_level/;
           built by the rebuild runner; never consulted by pickup.
Metrics  = computed on demand by default; precomputed only as rebuildable
           manifest-backed views; first families operator_to_fill.
```

## Pickup Contract

- Discovery is by-key over committed availability
  (`DataLakeRoot.list_available` / `read_availability`), per the storage
  contract's by-key authority. A queue, event, or view may never replace it.
- Each consumer computes a cheap **obligation snapshot** per raw anchor: the
  canonical-JSON structure of the inputs its processing depends on (for
  growable inputs, the exact derived record ids + content hashes; immutable
  raw needs no re-hash). The snapshot's sha256 is the **obligation
  fingerprint**.
- An anchor is picked up unless an ack record with the current fingerprint
  exists. Obligation growth (new input records) changes the fingerprint and
  re-surfaces the anchor automatically.
- Pickup must never read `indexes/derived_retrieval/` (view-independence):
  results are identical whether views exist, are stale, or are absent.
- Availability rebuild (`rebuild_availability`) remains the by-key reconcile
  backstop for missed commits; consumers may run it best-effort before
  pickup.
- Shared implementation: `orca-harness/data_lake/consumption.py`
  (`pickup`, `append_ack`, `is_acknowledged`, `find_acks`). A lane may
  reimplement pickup only if it passes the same conformance obligations
  below, unchanged.

## Acknowledgement Contract

- Physical grammar is owned by the derived-layout contract
  (`acknowledgements/<anchor_shard>/<raw-anchor>/<ack-namespace>/<ack-record-id>`),
  written only through `DataLakeRoot.append_record` (write-boundary contract:
  atomic create-only; overwrite hard-fails).
- **Namespace rule:** an ack namespace MUST be a lane name already declared
  in `lane_registry.LANE_ROLES`. No new registry; the CI-guarded lane map is
  the single name authority. The helper validates membership at write and
  read time.
- Ack record id is deterministic: `ack_<fingerprint[:24]>`. Completing the
  same obligation twice collides on create and hard-fails visibly — a second
  writer must re-check acknowledgement instead of overwriting.
- Ack body (canonical JSON): `ack_schema_version`, `record_kind:
  "acknowledgement"`, `ack_namespace`, `raw_anchor`, `obligation_fingerprint`,
  the full `obligation` snapshot, `evidence` (refs proving completion:
  record ids / completion markers / hashes), `generated_at`. The body repeats
  the raw anchor per the derived-layout verification rule.
- Corrections and supersession are new ack records (new fingerprint), never
  rewrites. Old acks remain as history.
- An unreadable/corrupt ack record is treated as **absent** for pickup
  decisions — the safe direction is re-verification, never fake-done.
  Integrity diagnosis belongs to the lake doctor, not pickup.
- The lake never consumes acks as control flow (storage contract): nothing in
  lake core schedules, gates, retries, or calls a lane from ack state.
- The ack asserts the lane met its obligation **for the recorded inputs**.
  Post-ack tampering with output records is not a pickup concern; it is a
  write-boundary violation surfaced by integrity tooling.

## Conformance Contract

Any lane pickup implementation (the shared helper included) must pass tests
proving:

1. **Idempotence** — a second run over an unchanged lake performs no
   re-processing and no duplicate writes.
2. **Append-only acks** — completing an already-acknowledged obligation
   hard-fails on create; nothing overwrites an ack.
3. **Missed-event recovery** — work discoverable purely by key: after an
   availability rebuild, a committed-but-unindexed anchor is found. No
   queue/event state is consulted.
4. **Obligation-growth re-pickup** — a new input record (e.g. a
   late-arriving derived transcript) changes the fingerprint and the anchor
   is picked up again; completion appends a new ack.
5. **View-independence** — pickup results are identical with views present,
   stale, or absent.
6. **No fake done** — an ack is never written without completion evidence;
   failed or partial units leave the anchor unacknowledged and re-surfaced.

The shared suite lives at `orca-harness/tests/test_data_lake_consumption.py`.

## Rebuild Command Binding

The command shape is pinned by the derived-layout contract
(`lake indexes rebuild --root <ORCA_DATA_ROOT> --target
availability|derived_retrieval|all --prove-rebuildability`). The v0 entry
point is `orca-harness/runners/run_data_lake_indexes_rebuild.py` (argparse,
runner convention); the semantics, not the binary packaging, are the
contract.

- `--target availability` delegates to `DataLakeRoot.rebuild_availability`.
- `--target derived_retrieval` builds the gate-opened object-level views
  under `indexes/derived_retrieval/object_level/<view>/` with a per-view
  manifest carrying the Silver Vault read-model obligations (generation id,
  source record ids, source high-watermark, selection policy versions,
  generated_at, stale/drift detection fields).
- Built views in v0: `undone` and `by_mention`. `by_creator` stays deferred
  behind the audience-silver lake wiring (Slice C) per the gate-opening
  record. No SQL engine: the query-lens stays scan/query-latency-gated.
- `undone` view semantics (weaker than lane-side pickup, by design): per
  adopted ack namespace (a namespace with at least one ack record), the
  committed anchors having **zero** ack records. Lane-side obligation growth
  is not reflected; the view is a cache for inspection, never pickup
  authority.
- `by_mention` view: exact `(brand, line)` strings from committed
  `silver__cleaning__product_mentions` records mapped to record refs. Only
  records passing the read-side Silver lineage gate
  (`silver_record_source_backed_status == complete`) enter the evidence
  mapping; all others appear solely under a `residuals` section (ids +
  counts, explicitly non-evidence). Exact strings are preserved — grouping
  normalization is Cleaning's job, never the lake's.
- `--prove-rebuildability` regenerates every view from committed material
  under the generation stamps recorded in the existing manifest and
  byte-compares against the stored files; any mismatch or unreadable source
  fails. A rebuild is never compared against itself.

## On-Demand-First Metrics Policy

- The default posture for any metric over lake evidence is **computed on
  demand** from committed records (medallion posture; derived-layout
  on-demand analysis rules).
- A metric family may be precomputed ONLY as a rebuildable, manifest-backed,
  non-authoritative view under `indexes/derived_retrieval/`, subject to the
  same prove-rebuildability check as any index.
- Metric values must obey the Silver Vault `MetricObservation` posture
  invariants — missing/hidden/blocked evidence is posture + reason, never a
  numeric zero — and metric views must expose posture and coverage fields so
  no reader can treat missing evidence as zero.
- **First metric families: `operator_to_fill`.** Candidate options recorded
  by the scoping lane: creator/content view-count style families over
  IG/YouTube/TikTok; movement-threshold
  (`SourceObjectMovementThresholdCrossingRecord`) derivations. No family is
  selected by this contract; no metric-family view may be built until the
  owner names one.

## Accepted Residuals

- `undone` view carries the weaker no-ack semantics above; upgrade trigger: a
  consumer needs fingerprint-aware backlog from the view rather than
  lane-side pickup.
- Ack write collisions between concurrent completers hard-fail the loser;
  single-writer-per-namespace remains the operating assumption. Upgrade
  trigger: a lane genuinely needs concurrent completers.
- No queue/scheduler/event system anywhere in the seam; a future queue may
  only optimize notification over this contract (storage contract residual).
- `by_creator` view deferred (Slice C precondition), per the gate-opening
  record.

## Non-Claims

Not validation, readiness, acceptance, or a Bronze full-GT claim. Not
engine/backend/queue selection. Not metric-family selection. Not Gate ADR
territory (AR body layout, retention/erasure). Not cross-platform identity or
actor retrieval. Records the seam behavior contract only; runtime code and
tests carry their own evidence on the implementing lane branch.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Consumption Seam Contract v0 adds the shared derived-lane consumption
    layer over the existing lake contracts: obligation-fingerprint pickup by
    key with ack records as lane-owned completion facts; ack namespaces bound
    to lane_registry.LANE_ROLES; a six-point conformance contract every lane
    pickup implementation must pass; the rebuild-command binding to the
    runner entry point for the gate-opened undone/by_mention views with
    manifest-backed prove-rebuildability; and the on-demand-first metrics
    policy with first metric families operator_to_fill.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
  downstream_surfaces_checked:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  intentionally_not_updated:
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
      reason: >
        Its ack grammar, rebuild-command shape, and gate-opening record are
        consumed as-is; the seam adds a consumer layer without changing the
        pinned relationships.
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
      reason: >
        By-key authority and the Acknowledgement Log slot are affirmed
        unchanged; the seam is the first production consumer of that slot.
    - path: orca-harness/data_lake/lane_registry.py
      reason: >
        The namespace rule reuses the existing CI-guarded lane map by
        reference; no registry edit is needed or made.
  non_claims:
    - not validation
    - not readiness
    - not engine/backend/queue selection
    - not metric-family selection
```
