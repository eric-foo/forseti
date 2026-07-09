# Source Capture Tenant Payload Attachment Boundary v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract
scope: >
  Defines the accepted logical attachment boundary for tenant/source-family typed
  payloads on Source Capture packets: current slice-attached fields are
  transitional/incumbent, while new payload families target packet/slice-keyed
  extension envelopes. Physical storage, migration, runner work, and projection
  cache implementation are out of scope.
use_when:
  - Deciding whether a new source-family payload may add fields directly to SourceCaptureSlice.
  - Designing capture, projection, ECR, Signal Content, or Cleaning inputs that need tenant payloads.
  - Classifying current metric_observations or demand pins against the long-term lake boundary.
authority_boundary: retrieval_only
open_next:
  - forseti-harness/source_capture/models.py
  - forseti/product/spines/capture/core/packet_schema/source_capture_packet_schema_evolution_architecture_v0.md
  - forseti/product/spines/capture/core/operating_model/orca_capture_projection_storage_spine_architecture_v0.md
  - forseti/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
stale_if:
  - SourceCaptureSlice adds, removes, or reclassifies tenant/source-family payload fields.
  - A later accepted packet-bundle, sidecar, manifest, or storage decision physicalizes extension envelopes.
  - A later accepted source proves a genuinely shared typed-payload schema across multiple non-overlapping source families.
```

## Status

`OWNER_ACCEPTED_TARGET_BOUNDARY_V0`.

This is a docs-only architecture contract. It records the accepted target
boundary for future source-family payloads after the whole-lake pass and the
narrowed payload-attachment pass. It does not authorize implementation, packet
mutation, manifest migration, storage-engine work, runner work, projection-cache
work, or validation/readiness claims.

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (tenant payload attachment boundary)
  edit_permission: docs-write
  target_scope:
    - forseti/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - forseti/product/spines/capture/core/operating_model/orca_capture_projection_storage_spine_architecture_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_capture_shape_contract_spec_v0.md
  dirty_state_checked: yes
  isolation: clean worktree branch codex/source-capture-tenant-payload-boundary off origin/main @ ada92695
  blocked_if_missing: no (all target sources present)
external_source_boundary: workflow skills are task-local mechanics only; Forseti authority remains AGENTS.md, the overlay, and accepted Orca docs.
doctrine_propagation_expected: architecture_doctrine
```

## Source Readiness

`SOURCE_CONTEXT_READY` for this boundary artifact.

Loaded source basis:

- `forseti-harness/source_capture/models.py`: current `MetricObservation`,
  `MetricPosture`, and `SourceCaptureSlice` fields.
- `forseti/product/spines/capture/core/operating_model/orca_capture_projection_storage_spine_architecture_v0.md`:
  proposed storage-spine core/satellite boundary and projection store/cache
  language.
- `forseti/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`: Mechanical Source
  Projection / Projected Unit view-contract non-claims.
- `forseti/product/spines/capture/core/packet_schema/source_capture_packet_schema_evolution_architecture_v0.md`:
  write-once/hash-pin and replay-not-mutate discipline.
- `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_capture_shape_contract_spec_v0.md`:
  typed value/posture coupling, IG metric vocabulary, and version-pin contract.
- The owner-adjudicated narrowed pass: extension envelopes accepted as target
  logical boundary, current slice fields classified transitional/incumbent.

## Decision

New tenant/source-family typed payloads target a **logical extension envelope**
keyed to `packet_id` and, when the payload belongs to a slice, `slice_id`.

Current slice-attached payload fields remain valid incumbent reality:

- `SourceCaptureSlice.metric_observations`
- `SourceCaptureSlice.session_visibility_pin`
- `SourceCaptureSlice.locale_pin`
- `SourceCaptureSlice.currency_pin`
- `SourceCaptureSlice.variant_pin`

Those fields are transitional/incumbent. They are not the long-term universal
lake schema and are not precedent for adding more bespoke source-family fields
to `SourceCaptureSlice` by default.

Direct `SourceCaptureSlice` field additions for future source-family payloads
require a separate owner decision showing that the field is truly core across
families, not merely convenient for the next tenant.

## Target Boundary

The accepted target is **packet/slice-keyed typed extension envelopes**.

At the architecture-boundary level, an extension envelope must preserve:

- packet identity: the `packet_id` the payload belongs to;
- slice identity when applicable: the `slice_id` the payload belongs to;
- source-family identity: for example IG, Reddit, Retail/PDP, demand-durability,
  or a later family;
- payload kind: the tenant-owned shape being carried;
- payload schema version;
- registry, identity, conflict-policy, or posture-policy version pins when the
  family needs them for replay;
- the tenant-owned payload body;
- limitations, warnings, absence/refusal posture, or residual state when the
  payload was expected but not observed.

This is a **logical attachment boundary**, not a physical storage decision. The
later physical design may embed envelopes in the packet manifest, store them as
packet-bundle sidecars, or choose another immutable/hash-pinned representation.
That physical choice remains open and must not be inferred from this document.

## Core vs Satellite

Core owns:

- raw packet/slice/file identity and provenance;
- the rule that tenant payloads attach by stable packet/slice key;
- payload schema-version pinning and immutable rebuild inputs;
- the typed value/posture coupling discipline for observed values;
- the rule that absence, blocked access, out-of-window, not-attempted, and
  not-applicable states are never stored as observed zeroes;
- the rule that projection, ECR, Signal Content, Cleaning, and Judgment must
  reference back to raw packet/slice/file handles instead of copying payloads
  into a second source of truth.

Tenant/source-family satellites own:

- IG metric vocabulary, value constraints, identity anchors, and coverage
  meaning;
- Retail/PDP product, variant, price, currency, availability, review substrate,
  target-binding, and residual meanings;
- Reddit thread/comment structure, parent/depth relationships, body text
  posture, and raw HTML provenance pointers;
- demand-durability series semantics, comparability pins, cadence, cold-start,
  temporal-regime, and diff meanings;
- any family-specific payload schema, registry, or posture-reason vocabulary.

Therefore the **value/posture discipline can be core**, but IG
`MetricObservation` cannot become the universal lake schema.

## Incumbent Field Treatment

Current slice-attached payload fields are kept as incumbent fields because they
already exist on current main and may be referenced by existing readers,
fixtures, or docs.

They are classified as:

- **allowed to remain readable** for current and historical packets;
- **not a reason to add more tenant fields** to `SourceCaptureSlice`;
- **eligible for future dual-read or replay migration** only under a later
  separately authorized implementation lane;
- **not eligible for in-place packet mutation**. If old material must become
  current under a new representation, the schema-evolution discipline points to
  replay into a new packet rather than editing the pinned original.

## Projection Terminology Guardrail

Use two names:

1. **Mechanical Source Projection / Projected Unit view contract.**
   This is the non-authoritative, re-derivable row view over raw. It is not a
   new spine layer, not the source of truth, and not a standing persisted object.

2. **Projection store/cache/plane.**
   This is the rebuildable query/index surface described by the storage-spine
   proposal. It may be persisted later only under the store/cache contract and
   remains non-authoritative.

This payload-boundary decision touches the **inputs** to Mechanical Source
Projection: a projection reader must know whether tenant payloads are present
as current slice fields or target extension envelopes. It does not decide a
projection cache engine, storage plane, materialization strategy, or runtime.

## Flow

```text
Capture writes immutable SourceCapturePacket (CapturePacket) bundle
  -> packet has SourceCaptureSlice records
  -> current fields may still appear on slices as transitional/incumbent
  -> new tenant payloads attach as logical extension envelopes keyed to packet/slice
  -> projection reads raw packet + current fields/envelopes and emits a derived view
  -> ECR / Signal Content / series derivations read raw-keyed inputs and write receipts
  -> Cleaning consumes one raw-keyed handle with optional projection/ECR/SCR refs
  -> Judgment later reads the traceable chain; it does not rewrite capture truth
```

Nothing in this flow makes projection, ECR, Cleaning, or Judgment a replacement
for the raw packet bundle.

## Option Disposition

| Option | Disposition | Why |
| --- | --- | --- |
| Keep adding direct `SourceCaptureSlice` fields | Rejected as the default target | Fits incumbent code, but turns each new tenant into lake-core field pressure. |
| Sidecar payload records | Deferred physical option | Acceptable only if governed as immutable/hash-pinned packet-bundle material, not mutable external truth. |
| Extension envelopes | Accepted target logical boundary | Stable keying and version pins remain core while family payload meaning stays satellite. |
| Transitional incumbent fields + target boundary | Accepted transition stance | Preserves current fields without blessing them as the future universal schema. |

## Non-Goals

This artifact does not:

- authorize code changes;
- authorize adding, removing, or migrating any `SourceCaptureSlice` field;
- choose embedded-manifest vs sidecar physical storage;
- choose envelope serialization;
- choose projection cache engine or materialization;
- design ECR, Signal Content, Cleaning, Evidence Binding, or Judgment schema;
- admit fixtures, validate packets, prove source-family coverage, or claim
  readiness;
- decide whether existing IG or demand fields should be frozen, dual-written,
  replayed, or migrated.

## Open Decisions

Still owner-owned or separately scoped:

- Whether extension envelopes are eventually embedded in the packet manifest,
  stored as packet-bundle sidecars, or represented another way.
- Whether current `metric_observations` remain IG-only for future captures or
  are frozen as legacy/transitional.
- Whether demand pins remain core capture facts, transitional fields, or later
  move into demand-family envelopes.
- Exact allowed envelope scopes beyond packet and slice, such as preserved file,
  series, or observation.
- Whether one core posture enum is sufficient or families may use their own
  posture vocabularies while satisfying the common coupling discipline.
- Whether any non-IG family proves a genuinely shared typed-observation schema.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Source Capture tenant/source-family typed payloads now have an accepted
    target logical attachment boundary: current SourceCaptureSlice payload
    fields are transitional/incumbent, while new tenant payload families target
    packet/slice-keyed extension envelopes; core preserves the value/posture
    discipline, and physical storage/migration remain deferred.
  trigger: architecture_doctrine
  controlling_sources_updated:
    - forseti/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - forseti/product/spines/capture/core/operating_model/orca_capture_projection_storage_spine_architecture_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_capture_shape_contract_spec_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/artifact-roles.md
    - .agents/workflow-overlay/validation-gates.md
    - forseti/product/spines/capture/core/packet_schema/source_capture_packet_schema_evolution_architecture_v0.md
    - forseti/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
    - forseti-harness/source_capture/models.py
  intentionally_not_updated:
    - path: forseti-harness/source_capture/models.py
      reason: >
        This artifact classifies current fields as incumbent/transitional and
        authorizes no code or schema migration.
    - path: forseti/product/spines/capture/core/packet_schema/source_capture_packet_schema_evolution_architecture_v0.md
      reason: >
        Its write-once/hash-pin and replay-not-mutate discipline is reused as
        controlling source; no changed schema-evolution rule is introduced.
    - path: forseti/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
      reason: >
        Projection doctrine remains correct; this artifact only clarifies what
        payload attachment source a projection reader consumes.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Source-loading already routes Data Capture Spine work through the
        consolidation map; the map now points to this artifact.
  stale_language_search: >
    rg -n "SourceCaptureSlice|metric_observations|typed Observation fields|extension envelope|extension envelopes|payload attachment|tenant payload|typed observation attaches|new sub-model|sidecar"
    docs/product/data_capture_spine docs/product/source_capture_toolbox
    docs/workflows/data_capture_spine_consolidation_map_v0.md
    forseti-harness/source_capture/models.py
  stale_language_search_result: >
    Executed 2026-06-17 in branch codex/source-capture-tenant-payload-boundary.
    Expected live hits remain in models.py for incumbent SourceCaptureSlice fields,
    this artifact, and the Data Capture submap pointer. The PROPOSED storage spine
    still contains historical "typed Observation fields" language, but now carries
    an open_next/stale_if pointer and a Relationship note saying this accepted
    attachment boundary supersedes it for payload attachment location. The IG
    capture-shape spec's former attachment-location open question is replaced
    with a later-boundary update. Other sidecar hits refer to session or Retail/PDP
    projection sidecars and do not assert the tenant-payload attachment target.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not migration authorization
    - not projection-cache or storage-engine selection
```
