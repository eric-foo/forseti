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
  views; and the on-demand-first metrics policy with the first metric
  families owner-named (brand/line share of voice; movement-threshold
  crossings) behind a field-level posture/coverage gate.
use_when:
  - Wiring a derived lane's work discovery or completion acknowledgement.
  - Implementing or reviewing a pickup path, ack write, or the indexes rebuild runner.
  - Checking the precompute-vs-on-demand posture for a metrics view.
open_next:
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_consumption_seam_scoping_route_v0.md
stale_if:
  - The storage, derived-layout, or write-boundary contract changes by-key authority, the ack grammar, or the index rebuild guarantee.
  - A later accepted decision changes the named metric families, their field-level gates, or the on-demand-first posture.
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
           manifest-backed views; first families owner-named, each
           view-blocked until its field-level contract binds (share-of-voice
           bound; movement-threshold not yet).
```

## Pickup Contract

- Discovery is by-key over committed availability
  (`DataLakeRoot.list_available` / `read_availability`), per the storage
  contract's by-key authority. A queue, event, or view may never replace it.
- **An empty pickup is a "no committed work" claim, and that claim is valid
  only over a reconciled availability surface.** The shared helper reconciles
  by default (`rebuild_availability` before the scan, failing loud on error).
  A consumer may opt out of the built-in reconcile only by reconciling
  itself first or by visibly recording its staleness tolerance; a silent
  skip that lets a stale index read as "no work" is a conformance failure.
- Each consumer computes a cheap **obligation snapshot** per raw anchor: the
  canonical-JSON structure of the inputs its processing depends on (for
  growable inputs, the exact derived record ids + content hashes; immutable
  raw needs no re-hash). The snapshot's sha256 is the **obligation
  fingerprint**.
- **Minimum obligation envelope** (helper-validated): the snapshot is a
  mapping carrying at least `obligation_schema` (version) and `consumer`
  (the consuming lane's identity), plus the processing-policy tokens whose
  change must re-trigger work (e.g. a model or rubric version). Beyond the
  envelope, input enumeration is lane-owned — but every input class whose
  growth must re-surface the anchor MUST appear in the snapshot; omitting
  one is a lane defect, and each lane's own tests are expected to pin its
  declared input families.
- An anchor is picked up unless its current fingerprint is acknowledged
  (see the retraction rule below: acknowledged means more ack facts than
  retraction facts for that fingerprint). Obligation growth (new input
  records) changes the fingerprint and re-surfaces the anchor automatically.
- Pickup must never read `indexes/derived_retrieval/` (view-independence):
  results are identical whether views exist, are stale, or are absent.
- Shared implementation: `orca-harness/data_lake/consumption.py`
  (`pickup`, `append_ack`, `retract_ack`, `is_acknowledged`, `find_acks`).
  A lane may reimplement pickup only if it passes the same conformance
  obligations below, unchanged.

## Acknowledgement Contract

- Physical grammar is owned by the derived-layout contract
  (`acknowledgements/<anchor_shard>/<raw-anchor>/<ack-namespace>/<ack-record-id>`),
  written only through `DataLakeRoot.append_record` (write-boundary contract:
  atomic create-only; overwrite hard-fails).
- **Namespace rule:** an ack namespace MUST be a lane name already declared
  in `lane_registry.LANE_ROLES` **for active writers and consumers**. No new
  registry; the CI-guarded lane map is the single name authority. This is a
  write/active-consumer admissibility rule, not retroactive authority over
  history: ack records written under a later-renamed or retired namespace
  remain valid append-only completion history and are never invalidated,
  deleted, or silently dropped by registry evolution. Renaming or retiring a
  lane is a deliberate migration that must state its completion-history
  disposition (the new namespace starts unacknowledged unless deliberately
  backfilled from evidence); an active consumer using an unregistered
  namespace fails loudly at its own call.
- Ack record id is deterministic: `ack_<fingerprint[:24]>` for the first
  completion of an obligation, `ack_<fingerprint[:24]>_<k>` for the k-th
  re-completion after retractions. Writing an id that already exists collides
  on create and hard-fails visibly — a second writer must re-check
  acknowledgement instead of overwriting.
- Ack body (canonical JSON): `ack_schema_version`, `record_kind:
  "acknowledgement"`, `ack_namespace`, `raw_anchor`, `obligation_fingerprint`,
  the full `obligation` snapshot, `evidence` (refs proving completion:
  record ids / completion markers / hashes), `generated_at`. The body repeats
  the raw anchor per the derived-layout verification rule.
- **Minimum evidence shape** (helper-validated): `evidence` is a non-empty
  list of mappings, each carrying a non-empty `kind` plus either a
  dereferenceable in-lake ref (record id / completion lane / hash fields) or
  an explicit non-dereferenceable basis statement. Sufficiency beyond that
  shape is lane-owned, but syntactically-present-yet-empty evidence never
  satisfies the ack contract; a unit whose evidence cannot be produced stays
  unacknowledged.
- **Corrections when the obligation changed** are new ack records under the
  new fingerprint, never rewrites. **Corrections when the obligation is
  unchanged** (wrong or insufficient evidence recorded) use the append-only
  **retraction fact**: `record_kind: "acknowledgement_retraction"` at
  `unack_<fingerprint[:24]>_<k>`, citing the retracted fingerprint and a
  mandatory reason. A fingerprint is acknowledged iff its well-formed ack
  facts outnumber its retraction facts, so a retracted obligation re-surfaces
  in pickup and may be truthfully re-acknowledged (`ack_<fp>_<k>`) after the
  work is re-verified. All facts remain as history; nothing is rewritten.
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
6. **No fake done** — an ack is never written without completion evidence
   meeting the minimum evidence shape; failed or partial units leave the
   anchor unacknowledged and re-surfaced.
7. **Retraction cycle** — retracting an ack (mandatory reason) re-surfaces
   the anchor in pickup; a truthful re-acknowledgement is representable
   without overwrite; all facts remain as append-only history.

The shared suite lives at `orca-harness/tests/test_data_lake_consumption.py`.

## Rebuild Command Binding

The command shape is pinned by the derived-layout contract
(`lake indexes rebuild --root <FORSETI_DATA_ROOT> --target
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
  authority. **Disclosure obligation:** the view body must make zero rows
  unmistakable — it carries a `zero_rows_meaning` statement ("zero ack
  records, NOT current-obligation satisfied") and per-namespace
  `anchors_with_acks` counts, so an operator cannot read an empty listing as
  an empty backlog when stale-ack/grown-obligation work exists that only
  lane-side pickup can see.
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
- **First metric families (owner-named 2026-07-02):**
  1. `source_backed_brand_line_share_of_voice` — per platform, cohort, and
     coverage window, the share of captured product-line mentions per
     brand/line, derived from source-backed-complete
     `silver__cleaning__product_mentions` records; every figure traceable to
     transcript evidence, denominators are captured-evidence-only (never a
     "total market" implication).
  2. `movement_threshold_crossings` — declared-threshold movement/momentum
     crossings for source objects (creator accounts, content, brands/lines)
     against a declared profile/baseline/window/cohort, landing as
     `SourceObjectMovementThresholdCrossingRecord` derivations per the
     storage contract's stored-record vocabulary.
  Provenance: owner-couriered cross-vendor decision input (GPT-5.5 Pro
  ranking, dispatched via the metric-families decision-input prompt),
  adjudicated and named by the owner's continuation instruction. Naming is
  selection only — it authorizes no view build.
- **Field-level gate (before any metric-family view is built):** the owning
  decision for a named family must first bind that family's field-level
  posture, reason, and coverage contract (field names and minimal
  semantics), so posture/coverage cannot be nominally present but
  semantically empty. Gate state:
  `source_backed_brand_line_share_of_voice` — bound by
  `core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md`
  (2026-07-02; view build is a separate bounded work unit);
  `movement_threshold_crossings` — not bound; view-build-blocked.

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
engine/backend/queue selection. Metric-family NAMING is recorded here
(owner-adjudicated selection); it is not view-build authorization — the
field-level gate must land first. Not Gate ADR territory (AR body layout,
retention/erasure). Not cross-platform identity or actor retrieval. Records
the seam behavior contract only; runtime code and tests carry their own
evidence on the implementing lane branch.

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
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  intentionally_not_updated:
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
      reason: >
        Its ack grammar, rebuild-command shape, and gate-opening record are
        consumed as-is; the seam adds a consumer layer without changing the
        pinned relationships.
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
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

```yaml
direction_change_propagation:
  doctrine_changed: >
    Adjudicated amendment pass (2026-07-02) closing the accepted findings of
    the cross-vendor delegated review (GPT-5.5 Pro, no_repo discovery pass)
    plus the owner's metric-family naming: (F1) append-only retraction fact
    class (unack_<fp>_<k> / re-ack ack_<fp>_<k>; acknowledged iff ack facts
    outnumber retraction facts) so same-obligation evidence corrections are
    representable without overwrite; (F2) namespace rule scoped to
    write/active-consumer admissibility with historical ack validity stable
    across registry evolution; (F3) reconcile-before-no-work made a binding
    pickup precondition (helper reconciles by default, fail-loud; opt-out
    must be visible); (F4) minimum obligation envelope
    (obligation_schema + consumer + policy tokens, helper-validated); (F5)
    minimum evidence shape (non-empty kind + dereferenceable ref or explicit
    basis); (F6) undone-view zero-rows disclosure (zero_rows_meaning +
    per-namespace anchors_with_acks); (F7) field-level posture/reason/
    coverage gate required before any named metric-family view is built.
    First metric families owner-named: source_backed_brand_line_share_of_voice
    and movement_threshold_crossings (naming only, view-build-blocked behind
    the field-level gate).
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
  downstream_surfaces_checked:
    - orca-harness/data_lake/consumption.py
    - orca-harness/data_lake/derived_retrieval_views.py
    - orca-harness/tests/test_data_lake_consumption.py
    - docs/workflows/orca_repo_map_v0.md
  adjudication_provenance: >
    Findings from the commissioned no_repo cross-vendor discovery review
    (reviewed_by: OpenAI GPT-5.5 Pro; authored_by: Anthropic claude-fable-5;
    de_correlation_bar: cross_vendor_discovery); each finding adjudicated
    accept/modify by the home CA; durable report at
    docs/review-outputs/adversarial-artifact-reviews/data_lake_consumption_seam_contract_adversarial_artifact_review_v0.md.
  non_claims:
    - not validation or readiness
    - not view-build authorization for the named families
    - findings closure claims are bounded by the same-vendor post-patch recheck recorded in the review report
```
