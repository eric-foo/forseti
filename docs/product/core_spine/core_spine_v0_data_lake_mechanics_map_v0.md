# Core Spine v0 Data Lake Mechanics Map v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture map
scope: >
  Minimal logical map for how Orca source data moves from raw capture through
  projection, ECR/SCR, Cleaning, and Judgment while raw capture remains the
  source of truth.
use_when:
  - Planning capture-to-derived-layer data flow.
  - Checking whether a downstream layer may copy, mutate, or replace source truth.
  - Deciding whether a storage/schema/projection/Cleaning lane is still blocked.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/source_capture_tenant_payload_attachment_boundary_v0.md
  - docs/product/data_capture_spine/source_capture_core_payload_split_explainer_v0.md
  - docs/product/data_capture_spine/retail_pdp_typed_envelope_probe_v0.md
  - docs/workflows/ecr_spine_submap_v0.md
  - docs/product/core_spine_v0_projection_doctrine_v0.md
  - docs/product/core_spine/core_spine_v0_cleaning_spine_foundation_v0.md
branch_or_commit:
  - Based on codex/source-capture-tenant-payload-boundary at d5dcf1a4; verify landing status before relying on this boundary from another base.
stale_if:
  - The payload-boundary lane is rejected or materially changed.
  - The Retail/PDP typed-envelope probe is rejected or materially changed.
  - A later accepted storage/manifest/sidecar/projection-cache decision supersedes this logical map.
  - A non-IG envelope probe disproves or changes the packet/slice-keyed boundary.
  - ECR, SCR, Cleaning, or Judgment ownership changes in a later accepted source.
```

## Status

`TARGET_RECOMMENDED_LOGICAL_MECHANICS_MAP_V0`.

Mini god tier lens: keep the high-value map, drop the pork. This artifact
answers one question: **what may each layer read and write without turning a
derived view into source truth?**

It is not storage selection, implementation, validation, readiness, or schema
migration authority.

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (payload boundary + source_capture models + ECR/SCR + projection + Cleaning)
  edit_permission: docs-write
  target_scope:
    - docs/product/core_spine/core_spine_v0_data_lake_mechanics_map_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/workflows/ecr_spine_submap_v0.md
  dirty_state_checked: yes
  isolation: clean worktree branch codex/data-lake-mechanics-map based on codex/source-capture-tenant-payload-boundary @ d5dcf1a4
external_source_boundary: delegated passes were advisory only; Orca authority remains AGENTS.md, the overlay, and accepted Orca docs.
doctrine_propagation_expected: architecture_doctrine
```

## Decision

Adopt the logical by-key mechanics map:

```text
Source Capture writes raw packet truth.
Everything downstream reads raw by key.
Everything downstream writes a derived view, receipt, record, or ledger.
Nothing downstream replaces raw.
Physical storage remains open.
```

Shared handle family:

- `packet_id`
- `slice_id` when slice-scoped
- preserved file refs plus `sha256` and `hash_basis`
- sibling derived-record refs only as refs, never as raw-truth substitutes

## Hard Rules

1. Raw `SourceCapturePacket` is canonical.
2. Reference, never merge.
3. Re-derive, never migrate.
4. Carry supplied facts or residualize; do not author from prose.
5. Absence is a posture, not observed zero.
6. One derived record per epistemic kind.
7. Projection and Cleaning own mechanics only.
8. Judgment owns credibility, salience, exclusion, Signal Integrity, Signal Use,
   Decision Strength, and Action Ceiling.
9. New source-family payloads default to packet/slice-keyed typed envelopes,
   not new direct `SourceCaptureSlice` fields.
10. Storage, manifest changes, projection cache, and runtime schema are not
    selected here.

## Layer Contract

| Layer | Reads | Writes | Must not do |
| --- | --- | --- | --- |
| Source Capture | Source surface + capture method context | Immutable `SourceCapturePacket` bundle | Decide downstream meaning or use |
| Core slice frame | Packet/slice capture facts | Stable shared facts; incumbent fields stay readable | Treat every new source detail as a core field |
| Typed envelope | Source-family payload tied to packet/slice | Logical typed payload: family, kind, schema version, pins, body, absence/residual posture | Pick physical storage or become mutable side truth |
| Projection | Raw + core facts + envelopes | Re-derived row view, loss ledger, receipt | Persist as source truth or decide salience |
| ECR | Raw packet/slice/file facts | Integrity postures SP-1/2/3/6 | Depend on Cleaning/projection or bind final Evidence Unit schema |
| SCR | Raw body material + provenance/ECR refs | Per-slice content record by key | Become a second capture-payload home |
| Cleaning | One raw-keyed input handle + optional sibling refs | Transform ledger, cleaned working view, warnings, raw-pull triggers | Decide credibility, independence, similarity effect, exclusion, or strength |
| Judgment | Raw + derived chain + raw pull-in | Verdicts and decision-use outputs | Rewrite raw capture truth |

## Flow

```text
Source Capture
  -> SourceCapturePacket [raw authority]
       |- core facts on packet/slice
       |- incumbent slice payload fields remain readable
       |- new source payloads attach as typed envelopes
  -> Projection view
  -> ECR integrity records
  -> SCR content records
  -> Cleaning ledger/view
  -> Judgment effects, with raw pull-in when needed
```

## Gates Before Physicalization

Do not open storage/schema/manifest/projection-cache/envelope-serialization work
until these are true:

1. The payload-boundary lane is landed or explicitly accepted as the base.
2. The Retail/PDP probe, or another non-IG family probe, shows packet/slice-
   keyed envelopes work without adding new `SourceCaptureSlice` fields.
3. The owner chooses envelope physical representation: manifest, sidecar, or
   another immutable/hash-pinned form.
4. Incumbent fields have a fate: frozen, dual-read, replayed, or legacy-only.
5. SCR `FamilyDetailBase` is governed so it does not compete with capture-side
   envelopes.

Do not open Cleaning implementation until the input handle, transform ledger,
tag/write location, allowed mechanical warning vocabulary, and raw-pull trigger
shape are decided.

## Mini God Tier Limitations

Foregone on purpose:

- no storage engine;
- no manifest v2;
- no envelope serialization;
- no projection cache;
- no migration of incumbent fields;
- no direct new `SourceCaptureSlice` field;
- no ECR/Evidence Unit final schema;
- no Cleaning runtime schema;
- no Judgment run authorization;
- no validation/readiness claim.

The payoff is speed and low lock-in: Orca gets the layer contract now, while the
irreversible physical choices wait for the non-IG probe.

## Known Risks

- This map depends on the payload-boundary branch until that branch lands.
- Retail/PDP supports the logical envelope shape only; the envelope boundary is
  still unbuilt and unproven physically.
- `SourceCaptureSlice` is already a fat incumbent surface; docs do not
  mechanically block field #6.
- SCR `FamilyDetailBase` is a latent competing payload home.
- SP-6 archive-slice keying is implemented convention, not a general packet
  field contract.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca now has a minimal planning-only data-lake mechanics map: raw
    SourceCapturePacket is canonical; packet/slice/file keys and typed
    packet/slice envelopes feed projection, ECR/SCR, Cleaning, and Judgment by
    reference; derived layers write views, receipts, records, or ledgers only;
    physical storage/schema/migration remain deferred.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - docs/product/core_spine/core_spine_v0_data_lake_mechanics_map_v0.md
    - docs/product/data_capture_spine/retail_pdp_typed_envelope_probe_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/workflows/ecr_spine_submap_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/product/data_capture_spine/source_capture_tenant_payload_attachment_boundary_v0.md
    - docs/product/data_capture_spine/source_capture_core_payload_split_explainer_v0.md
    - docs/workflows/ecr_spine_submap_v0.md
    - docs/product/core_spine_v0_projection_doctrine_v0.md
    - docs/product/core_spine/core_spine_v0_cleaning_spine_foundation_v0.md
    - orca-harness/source_capture/models.py
    - orca-harness/ecr/
    - orca-harness/signal_content/
  intentionally_not_updated:
    - path: orca-harness/source_capture/models.py
      reason: Docs-only map; no code/schema migration or new slice field.
    - path: orca-harness/ecr/
      reason: Existing derivers already follow by-key pure derivation; no code work.
    - path: orca-harness/signal_content/
      reason: SCR remains by-key; FamilyDetailBase risk is recorded without code change.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: Existing Data Capture and ECR submaps route to this artifact.
  stale_language_search: >
    rg -n "data-lake mechanics|SourceCaptureSlice|extension envelope|projection cache|ECR|Signal Content|Cleaning|Judgment|FamilyDetailBase|archive-body slice"
    docs/product docs/workflows orca-harness/source_capture orca-harness/ecr orca-harness/signal_content
  stale_language_search_result: >
    Executed 2026-06-17 on branch codex/data-lake-mechanics-map. Hits were
    expected in this artifact, payload-boundary/explainer docs, projection/ECR/
    SCR/Cleaning docs, and current source_capture/ecr/signal_content code. No
    checked live surface converted this map into storage selection, manifest
    migration, projection-cache authorization, a new SourceCaptureSlice-field
    authorization, or implementation readiness.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not storage selection
    - not migration authorization
```

Older receipts, when cycled out, belong in `docs/decisions/dcp_receipts_archive_v0.md`.
