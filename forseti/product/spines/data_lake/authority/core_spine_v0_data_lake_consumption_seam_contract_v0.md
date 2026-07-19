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
Views    = rebuildable Silver Retrieval query tables under
           indexes/derived_retrieval/silver_vault/core/query_tables/, paired
           with manifests/ rows; built by the rebuild runner; never consulted
           by pickup.
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
- Shared implementation: `forseti-harness/data_lake/consumption.py`
  (`pickup`, `append_ack`, `retract_ack`, `is_acknowledged`, `find_acks`).
  A lane may reimplement pickup only if it passes the same conformance
  obligations below, unchanged.

### Cadence snapshot boundary

- A cadence run first reads the exact committed packet-id set directly from
  by-key raw without reading, purging, or rebuilding shared availability.
- Every driven lane receives that same immutable set for both execution
  cycles, ASR skip checks, and the final pending proof. Scoped reconcile
  refreshes only selected anchors and never purges the global availability
  index.
- A selected anchor that becomes missing, corrupt, tombstoned, or unreadable
  fails loudly. A packet committed after the snapshot is next-run work: it may
  be reported, but cannot invalidate or silently join the current completion
  claim.
- Standalone consumer calls remain live and unscoped by default. The boundary
  is explicit input, not process-global state or an implicit root wrapper.
- The cadence-tail Creator Vault rebuild is an ordinary live rebuild after
  snapshot completion. It scans the full creator-profile metric observation
  lane, may include newer committed material, and is never an exact
  historical-snapshot claim. Generic `by_creator`, `by_mention`, and `undone`
  views remain explicit owner-rebuildable caches; normal cadence no longer
  rescans them merely to refresh current creator metrics.
- A fresh root may still use one explicit cadence
  `--bootstrap-active-product-mention-policy` run to build the generic map with
  the checkout's exact active policy; bootstrap reports and stores the version
  plus fingerprint and refuses an existing `by_mention` manifest. Later
  generic-map rebuilds use stored pins. Normal Creator Vault cadence does not
  read or require product-mention policy pins, and `--check` never mutates.
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
8. **Scoped isolation** — reconciling or picking up a named packet set does
   not delete, rewrite, or process availability outside that set.
9. **Late-arrival separation** — a packet committed between cadence cycles
   remains pending for the next snapshot and does not create current-cycle
   work.
10. **Selected-anchor failure visibility** — loss or corruption of a packet
    in the start set makes the current cadence fail; it cannot become a
    successful empty pickup.

The shared suite lives at `forseti-harness/tests/test_data_lake_consumption.py`.

## Rebuild Command Binding

The command shape is pinned by the derived-layout contract
(`lake indexes rebuild --root <FORSETI_DATA_ROOT> --target
availability|creator_vault|derived_retrieval|all --prove-rebuildability`). The v0 entry
point is `forseti-harness/runners/run_data_lake_indexes_rebuild.py` (argparse,
runner convention); the semantics, not the binary packaging, are the
contract.

For a rebuild containing derived_retrieval, the caller must additionally
provide --product-mention-policy-version <VERSION> and
--product-mention-policy-fingerprint-sha256 <LOWERCASE_64_HEX>. A fresh root
may instead use `--bootstrap-active-product-mention-policy` exactly once. That
flag binds the exact active product-extraction policy from the checked-out
code, reports and persists the version plus fingerprint in generated-view
manifests, and refuses to run when a `by_mention` manifest already exists.
Later cadence and owner-operated rebuilds use
`--use-stored-product-mention-policy` from that manifest. Proof mode
regenerates from the exact policy stored in each view manifest and does not
accept an implicit current/latest policy.

- `--target availability` delegates to `DataLakeRoot.rebuild_availability`.
- `--target creator_vault` scans only the complete
  `creator_metric_silver` observation-lane history, filters to current
  source-backed `tiktok_creator_profile_metric` rows, and replaces the
  per-account envelopes under
  `indexes/derived_retrieval/silver_vault/creator_vault/`. A Silver account id
  is used when present. Handle-only monitoring observations bind to the stable
  creator-profile registry by exact platform plus public handle; any direct-
  Silver/registry disagreement fails closed into an unfiled residual. It does
  not require product-mention policy pins and does not rewrite the core lake-map
  views. Unfileable captured accounts are persisted as named generated residuals;
  missing envelopes therefore remain distinguishable from captured-but-
  unfileable evidence. Account manifests expose a source-ref-set fingerprint,
  generation time, selection policy, and explicit stale condition.
- `--target derived_retrieval` builds the gate-opened object-level views as
  `indexes/derived_retrieval/silver_vault/core/query_tables/<view>.json`, with
  the paired manifest at
  `indexes/derived_retrieval/silver_vault/core/manifests/<view>.json` carrying
  the Silver Vault read-model obligations (generation id, source record ids,
  source high-watermark, selection policy versions, generated_at, stale/drift
  detection fields).
- Core built views in v0: `by_creator`, `by_mention`, and `undone`. The
  separately addressed Creator Vault account-envelope family is also a
  generated, non-authoritative read model and is covered by rebuildability
  proof. All public generated read models exclude tombstoned raw anchors while
  retaining the underlying append-only lake bytes.
  `by_creator`
  was deferred at gate opening behind the audience-silver lake wiring; that
  wiring has since landed (registered creator-metric, grid, and
  comment-attention Silver lanes, census-reconciled), so the view is built
  (owner-commissioned 2026-07-17). No SQL engine: the query-lens stays
  scan/query-latency-gated.
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
  `transcript_product_mentions_silver` records mapped to record refs. The
  caller binds one exact `{policy_version, policy_fingerprint_sha256}` and
  the view selects at most one record per transcript evidence subject under
  that policy. Policy mismatches and other non-selected records are named
  residuals; distinct same-policy siblings fail closed. Only records passing
  the read-side Silver lineage gate
  (`silver_record_source_backed_status == complete`) enter the evidence
  mapping; all others appear solely under a `residuals` section (ids +
  counts, explicitly non-evidence). Exact strings are preserved — grouping
  normalization is Cleaning's job, never the lake's. Owner-widened
  2026-07-17: the view additionally carries a `native_product_pages` section
  routing a brand/line entity to its own committed product-page capture
  anchor (identity from the view-only projection product snapshot, labeled
  routing, never Silver authority) with the anchor's classified Silver
  record counts, so product entities resolve to native product-page
  evidence, not only creator-content mentions. Product-identity sources are
  a closed in-code registry (`NATIVE_PRODUCT_PAGE_SOURCES`; Fragrantica is
  the sole entry) — a new identity source is a deliberate registry entry
  with its own extractor, never a loop rewrite. A projection row missing
  brand or line is residual-only; one native `(anchor, source site, site id
  or canonical URL)` identity cannot silently bind to conflicting brand/line
  or URL values.
- `by_creator` view (schema v2): (platform namespace, asserted identity
  kind, observed public account native id) from account-bearing Silver
  subjects (`platform_public_account` subjects and `public_content_object`
  subjects naming their publishing account) mapped to committed packet +
  Silver record refs, each carrying the build-time authority status from the
  shared `classify_silver_vault_record_sources` classifier. The identity
  kind is the record-asserted kind of the account identifier (e.g.
  `youtube_channel_id`) or `unspecified` when unasserted; distinct identity
  kinds never merge into one key, so a handle-keyed and a platform-id-keyed
  record can never silently collide or conflate. Platform namespaces come
  from the closed `KNOWN_PLATFORM_NAMESPACES` vocabulary (exact lowercase
  canonical strings; extending it is a deliberate edit per new platform,
  matching the Reddit venue registry's lowercase-canonical posture); an
  unknown namespace or an unfileable account-describing subject shape
  (missing identifiers, unknown subject kind carrying account-identifier
  fields) is a named residual (`unrecognized_platform_namespace`,
  `unrecognized_account_subject_shape`) — a wiring gap is always
  distinguishable from "not captured". Per-platform object-level only — no
  cross-platform identity is unified. Exact observed strings preserved;
  absence of a key/packet/lane means not captured or not indexed, never
  zero. Conflicting aliases for the same
  `(platform namespace, identity kind, native id)` are named residuals
  rather than silently treated as consistent. The scoped read entry point is
  `runners/run_derived_retrieval_lookup.py` (`--creator` / `--mention`).
  Creator lookup resolves identity from the stable
  `creator_profile_current_view_v0` registry first, then joins the account
  envelope directly; it remains available when `by_creator` is absent or
  stale and reports unknown/conflicted registry states explicitly. Mention
  lookup continues to require the generated `by_mention` pair. Every consumed
  generated pair is hash-checked and reports generation provenance.
- `--prove-rebuildability` regenerates the requested family from committed
  material under the generation stamps recorded in existing manifests and
  byte-compares against stored files; any mismatch or unreadable source fails.
  Creator Vault proof uses the same metric-lane-only sweep as its daily build.
  A rebuild is never compared against itself.

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
     brand/line, derived from one caller-bound exact product-mention policy
     over source-backed-complete
     `transcript_product_mentions_silver` records; every figure traceable to
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
- The `by_creator` build classifies every active Silver record per rebuild
  (deterministic but whole-lake); the SQL query-lens stays behind the
  derived-layout contract's scan/query-latency trigger. Upgrade trigger:
  rebuild or lookup latency proves insufficient for a governed consumer.

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
    Exact product-mention policy identity is now a required read-model input
    (2026-07-15). Product-mention record and completion identity includes the
    policy fingerprint; by_mention, share-of-voice, and extraction-quality
    evaluation consume the same exact-policy selector; policy mismatches are
    residuals and distinct same-policy siblings fail closed. This closes the
    write-once sibling double-count/reuse class without inventing a mutable
    latest pointer.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md
  downstream_surfaces_checked:
    - forseti-harness/cleaning/transcript_product_lake.py
    - forseti-harness/data_lake/product_mention_selection.py
    - forseti-harness/data_lake/derived_retrieval_views.py
    - forseti-harness/data_lake/sov_readout.py
    - forseti-harness/runners/run_sov_extraction_quality_eval.py
  non_claims:
    - not validation or readiness
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Cadence completion is now bound to one read-only committed starting
    packet-id snapshot. Every cadence cycle and final check uses that same set;
    scoped reconcile never purges global availability; selected-anchor failures stay
    loud; later commits are next-run work. The cadence-tail lake-map rebuild
    remains live and may include newer material, so no frozen-map claim is
    introduced.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
    - docs/decisions/bronze_consumer_census_closure_record_v0.md
    - docs/decisions/forseti_lake_map_scaling_and_hygiene_plan_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
    - forseti-harness/data_lake/root.py
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_capture_propagation_classification_contract_v0.md
    - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
    - forseti/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
    - forseti/product/spines/ecr/signal_content/core_spine_v0_signal_content_record_architecture_v0.md
    - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  intentionally_not_updated:
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
      reason: Raw/by-key authority, append-only facts, and generated-view non-authority are unchanged.
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
      reason: Packet, availability, acknowledgement, and index shapes are unchanged.
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
      reason: The Bronze/Silver/Gold boundary and readiness posture are unchanged.
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
      reason: Silver record authority and generated-read-model rules are unchanged.
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
      reason: The map remains a disposable live rebuild through the existing sanctioned writer.
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_capture_propagation_classification_contract_v0.md
      reason: Capture propagation classes and downstream checks are unchanged; this work coordinates existing consumers.
    - path: forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
      reason: Layer flow and authority routing are unchanged.
    - path: forseti/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
      reason: Projection evidence and non-authority semantics are unchanged.
    - path: forseti/product/spines/ecr/signal_content/core_spine_v0_signal_content_record_architecture_v0.md
      reason: ECR derivation and evidence semantics are unchanged.
    - path: forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
      reason: Cleaning ownership and handoff boundaries are unchanged.
  non_claims:
    - not validation, readiness, or a live-lake proof
    - not a queue, scheduler, capture pause, or global lock
    - not an exact historical lake-map snapshot
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    All three gate-opened object-level views are now built (2026-07-17,
    owner-commissioned): by_creator is no longer deferred -- its
    audience-silver wiring precondition landed via the registered
    creator-metric, grid, and comment-attention Silver lanes -- and routes a
    per-platform public account to committed packet + Silver record refs with
    build-time authority statuses from the shared classifier; by_mention is
    owner-widened to carry a native_product_pages section routing a
    brand/line entity to its own committed product-page capture anchor
    (identity from the view-only Fragrantica projection, labeled routing,
    never Silver authority); and runners/run_derived_retrieval_lookup.py is
    the scoped read-only lookup entry point over the generated views, with
    exact normalized identity matching and fail-closed manifest-pair/hash
    verification. Partial or conflicting native identity rows and conflicting
    account aliases remain visible residuals rather than fabricated or
    silently collapsed keys. Owner-ratified identity hardening (2026-07-17,
    adjudicated with the delegated review): by_creator schema v2 promotes the
    record-asserted identity kind into the card key (distinct kinds never
    merge; `unspecified` when unasserted), platform namespaces are a closed
    vocabulary, unfileable account-describing shapes are named residuals
    rather than silent drops, and native product-page identity sources are a
    closed in-code registry with Fragrantica as the sole entry. The views
    stay rebuildable, non-authoritative, per-platform object-level, and
    prove-rebuildability-covered; absence in a view is never zero; by-key
    discovery stays retrieval authority; the SQL query-lens stays behind the
    scan/query-latency trigger.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
    - forseti-harness/data_lake/derived_retrieval_views.py
    - forseti-harness/runners/run_derived_retrieval_lookup.py
  downstream_surfaces_checked:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
    - forseti-harness/runners/run_data_lake_indexes_rebuild.py
    - forseti-harness/tests/test_data_lake_indexes_rebuild.py
  intentionally_not_updated:
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
      reason: >
        Its residual records the 2026-06-25 gate opening and correctly defers
        the builder to a separate bounded work unit; this receipt records that
        unit landing. The gate state and view set are unchanged.
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
      reason: >
        Its Generated Read Models rules (rebuildable, non-authoritative,
        manifest-backed, missing-evidence-never-zero) are unchanged and this
        build satisfies them; the built-view state is owned here.
  non_claims:
    - not validation, readiness, or approval
    - not engine/backend selection; SQL query-lens stays latency-gated
    - not cross-platform identity resolution or actor retrieval
    - not a change to by-key retrieval authority
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    The built by_mention and undone read models now use the Silver Vault
    contract-owned core query_tables/manifests homes instead of the
    contradictory generic object_level tree; the views remain rebuildable,
    non-authoritative, and never pickup authority.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
    - forseti-harness/data_lake/root.py
    - forseti-harness/data_lake/derived_retrieval_views.py
    - forseti-harness/tests/test_data_lake_indexes_rebuild.py
    - forseti-harness/tests/test_data_lake_rebuild_proof.py
    - forseti-harness/tests/test_data_lake_consumption.py
    - docs/workflows/forseti_repo_map_v0.md
    - .agents/workflow-overlay/source-loading.md
  intentionally_not_updated:
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
      reason: It already owns and names the canonical Silver Vault core query_tables/manifests layout.
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
      reason: It owns the generic derived_retrieval slot and gate; the Silver Vault contract owns this read-model subhome.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: Its Data Lake routes point to the owning contracts and do not pin the retired object_level physical path.
    - path: .agents/workflow-overlay/source-loading.md
      reason: Source-pack routing is unchanged and does not pin a generated read-model physical path.
  stale_language_search: 'rg -n "derived_retrieval/object_level|object_level/<view>" forseti-harness forseti/product/spines/data_lake docs/workflows/forseti_repo_map_v0.md'
  stale_language_search_result: The only remaining match is this receipt's search command.
  non_claims:
    - not validation or readiness
    - not by_creator activation
    - not a new retrieval backend or authority source
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Fresh-root lake-map maintenance now has one explicit bootstrap boundary:
    one --bootstrap-active-product-mention-policy rebuild binds the checkout's
    exact active product-extraction policy, records its version and fingerprint,
    and refuses an existing by_mention manifest. Normal cadence then reuses
    stored pins automatically. Check mode remains read-only and no scheduler is
    introduced.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
    - docs/decisions/forseti_lake_map_scaling_and_hygiene_plan_v0.md
  downstream_surfaces_checked:
    - forseti-harness/runners/run_data_lake_indexes_rebuild.py
    - forseti-harness/runners/run_seam_cadence.py
    - forseti-harness/tests/test_data_lake_indexes_rebuild.py
    - forseti-harness/tests/unit/test_seam_cadence.py
    - forseti-harness/cleaning/transcript_product_extractor.py
    - forseti-harness/cleaning/transcript_product_lake.py
  intentionally_not_updated:
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
      reason: Policy bootstrap changes no raw, Silver, acknowledgement, or index storage shape.
  non_claims:
    - not validation, readiness, or live-drive proof
    - not a scheduler or continuous-maintenance service
    - not implicit latest-policy selection or policy-authority transfer
```
