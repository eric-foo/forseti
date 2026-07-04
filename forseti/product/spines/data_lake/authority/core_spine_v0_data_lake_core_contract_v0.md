# Core Spine v0 Data Lake Core Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract
scope: >
  Core responsibility contract for Orca's data lake: what the lake owns, what
  it must not own, how capture material becomes available by key, and how
  downstream derived lanes attach results without replacing raw truth.
use_when:
  - Deciding whether a lake, capture, projection, ECR, SCR, or Cleaning change crosses the lake boundary.
  - Preparing the Data Lake Storage Contract v0 after the logical data-lake mechanics map.
  - Checking whether a fragrance or other source-family consumer belongs in lake core or satellite payloads.
open_next:
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
  - forseti/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_typed_envelope_probe_v0.md
  - forseti/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
  - docs/workflows/ecr_spine_submap_v0.md
downstream_consumers:
  - data lake storage contract lane
  - capture packet schema/evolution lane
  - ECR/SCR source-side derived-record lanes
  - Cleaning spine foundation lane
stale_if:
  - A later accepted storage, manifest, sidecar, queue, or Attachment Record serialization decision supersedes this contract.
  - The payload-boundary lane is rejected or materially changed.
  - Projection, ECR, SCR, Cleaning, or Judgment ownership changes in a later accepted source.
  - A later owner decision makes the lake an orchestrator rather than a by-key store.
authority_boundary: retrieval_only
```

## Purpose

This contract turns the accepted data-lake direction into a narrow boundary that
future implementation and architecture lanes can rely on without making the lake
too smart.

The lake is the warehouse and filing system for captured source material. It
preserves raw packets (CapturePacket), stable IDs, hashes, manifests, and by-key availability.
It does not clean, normalize, identify entities, decide source value, or run
downstream lanes.

## Status

`TARGET_CONTRACT_RECORDED_V0`.

This is a planning and architecture contract. It is not implementation
authority, validation, readiness, physical storage selection, queue design,
schema finalization, or engine/backend selection by this contract. Engine/backend
choice is delegated to the Storage Contract physicalization boundary.

## Source Basis

- The data-lake mechanics map records the by-key flow: Source Capture writes
  raw packet truth; downstream lanes read raw by key and write derived outputs;
  nothing downstream replaces raw.
- The tenant payload boundary accepts packet/slice-keyed source-family payload
  envelopes as the target logical attachment boundary, while current direct
  fields remain incumbent/transitional.
- The Retail/PDP probe clears one non-IG logical fit check for keyed payload
  envelopes, but explicitly does not clear physical storage, manifest, sidecar,
  migration, ECR, Cleaning, or Judgment implementation.
- Projection doctrine keeps Mechanical Source Projection as a re-derivable
  Data-Capture-owned view over raw, not a new spine layer and not Cleaning.
- The ECR/SCR spine map carries the reference-never-merge, one-record-per-kind,
  carry-or-residualize, and re-derive-not-migrate disciplines.

## Contract In One Screen

```text
Capture writes raw SourceCapturePacket (CapturePacket) truth.
The lake preserves raw truth and makes it findable by stable keys.
The lake may record that a packet is available by key.
Projection, ECR, SCR, and Cleaning discover/read by key.
Those lanes write append-only derived results keyed back to raw.
Raw bytes, hashes, and packet identity are never rewritten by derived lanes.
```

The lake is allowed to be strict about storage mechanics. It is not allowed to
be smart about meaning.

## Core Lake Owns

- Raw `SourceCapturePacket` bundle preservation.
- Stable handle family: `packet_id`, `slice_id` when slice-scoped, preserved
  file IDs, `sha256`, and `hash_basis`.
- Manifest and reference rules needed to know which raw files and payloads
  belong to a packet.
- By-key findability: the ability to locate committed packets, slices, files,
  and attached payload references by stable handles.
- Source-family payload attachment rules at the core boundary: keyed scope,
  payload kind, payload schema version, immutable replay inputs, and
  structural value/posture coupling. The lake may require that an observed,
  absent, refused, blocked, or residual value travels with an explicit posture;
  it must not interpret what that posture means for ECR, SCR, Cleaning, or
  Judgment.
- Logical attachment points for downstream derived results keyed to packet,
  slice, or file references.
- A content-free availability fact after raw commit: "this packet/slice/file
  material is committed and readable by these keys."

## Lake Must Not Own

- ECR semantic or integrity derivation.
- SCR content interpretation.
- Cleaning transforms, normalization, translation, summarization, dedupe, or
  clustering mechanics.
- Judgment, including credibility, salience, exclusion, Signal Integrity,
  Signal Use, Decision Strength, Action Ceiling, or source value.
- Canonical entity identity, product (Product) identity, brand (Brand) identity, creator identity,
  or cross-packet dedupe.
- Fragrance, beauty, retail, social, forum, or other domain ontology as lake
  core.
- Downstream scheduling, retry, completion gating, or direct calls into ECR,
  Projection, SCR, Cleaning, or Judgment.

## Availability Signal Contract

The lake may expose a work-availability signal only as a content-free fact:

```text
raw material committed at packet/slice/file keys, with hash/checkable refs
```

The signal must not name which downstream lane should act, what processing is
required, what priority a lane should assign, or whether previous downstream
work succeeded.

By-key discovery is the contract authority. The lake-owned availability surface
is passive committed state: a downstream lane must be able to find work by
scanning or querying committed packet keys even if an event/queue message is
missed. Any event or queue engine is a separate runtime optimization over
committed raw state, not the source of truth, and must not become a lake-owned
push, route, or call into a downstream lane.

Downstream completion or acknowledgement may be written as an append-only
lane-owned fact keyed to raw. The lake must not consume that acknowledgement as
control flow to gate, retry, or schedule another lane. Its physical write path
is deferred with the derived-record physical home; until that lane closes, this
is a logical attachment allowance, not an implementation instruction.

## Result Attachment Contract

Downstream outputs attach as logical append-only derived records keyed to raw.
The physical home is deferred, but the logical rule is fixed:

- Derived records point to `packet_id`, `slice_id`, preserved file refs, and
  sibling derived-record refs only as references.
- Derived records do not copy raw payload bodies into a second source of truth.
- Derived records never mutate raw bytes, raw hashes, raw manifests, packet
  identity, or source-family Attachment Records.
- Each epistemic kind stays separate: projection receipt, ECR integrity record,
  SCR content record, Cleaning transform ledger, and Judgment output are
  siblings, not one merged blob.
- Re-derive, never migrate, when a derived taxonomy changes. Corrections,
  supersession, invalidation, or ignore-prior relationships must be modeled as
  lane-owned append-only derived metadata keyed back to raw, not by mutating raw
  truth or rewriting prior derived records in place.

Do not infer physical separation from this section. Attachment Record and
derived-record storage lane still must choose the actual manifest, sidecar,
bundle, store, or other representation.

## Projection Boundary

Do not collapse lake findability and Mechanical Source Projection.

Lake findability means:

- committed packet lookup;
- stable handle lookup;
- manifest/reference traversal;
- source payload reference discovery. The lake may know a reference's structural
  family/kind/schema-version keys; it must not understand or validate the
  payload body's source-family semantics.

Projection means:

- a re-derivable row view over raw;
- raw anchors;
- a loss ledger;
- a projection receipt;
- no Cleaning, no ECR, no Judgment, and no salience decision.

The lake owns "findable." Projection owns "legible as rows." Cleaning owns
mechanical transforms. Judgment owns interpretation and decision use.

## Source Payload Attachment Boundary

New source-family payloads default to packet/slice-keyed source payload
Attachment Records, not new direct `SourceCaptureSlice` fields. The prior
logical-boundary docs call this the typed-envelope boundary; this storage lane
uses Attachment Record as the target term.

At the lake boundary, the Attachment Record carries:

- packet identity;
- slice identity when applicable;
- source-family identity;
- payload kind;
- payload schema version;
- replay/version pins when needed;
- source-visible payload body;
- limitations, warnings, absence/refusal posture, or residual state.

The Attachment Record must not carry cleaned values, canonical entity decisions,
dedupe decisions, credibility labels, Judgment labels, or downstream-use
strength.

Exact field names and physical representation remain open. Do not freeze names
such as `extension_envelopes` from this contract alone.

## Fragrance Consumer Boundary

Fragrance is allowed to be the first consumer pressure test. It is not allowed
to become lake core by convenience.

Fragrance-specific facts such as notes, accords, concentration, longevity,
retailer SKU details, review substrate, or source-specific residuals belong in
source-family Attachment Records or downstream derived records keyed to raw.
They do not become lake-core fields unless a later owner decision proves a
cross-family core need under a cited source-family promotion rule or explicitly
accepted one-off invariant. Convenience, first-consumer pressure, or one source
family is not enough.

## Incumbent Direct Fields

Current source-capture source has direct incumbent payload fields that predate
this target boundary. They include slice-level tenant fields such as demand
pins and metric observations, plus packet-level demand-series fields.

This contract classifies them as incumbent/transitional. They remain readable
for current and historical packets, but they are not precedent for adding the
next source-family field directly to `SourceCaptureSlice` or
`SourceCapturePacket`.

The accepted storage-lane fate is: keep them legacy-readable and
transitional, do not treat them as precedent for future direct source-family
fields, and move only by future dual-read or replay under a separately
authorized lane. They are not promoted as universal lake core.

No path may mutate pinned historical packets in place.

## Physicalization Gate

Do not implement storage, manifest changes, Attachment Record serialization, projection
cache, queue runtime, or derived-record persistence from this contract until
the physicalization lane closes these blockers:

1. Choose the Attachment Record physical representation: manifest child, immutable
   sidecar, hash-pinned bundle member, or another immutable/checkable form.
2. Follow the accepted incumbent-field fate: legacy-readable transitional
   fields, future dual-read or replay only, and no in-place packet mutation.
3. Govern SCR `FamilyDetailBase` so it cannot become a competing raw
   source-family payload home.
4. Assign enforcement for write-once raw, no-cleaning-in-lake, append-only
   derived results, and no-new-core-field pressure to deterministic write or
   tool boundaries where possible.
5. Choose the physical home and write boundary for projection receipts, ECR
   records, SCR records, Cleaning ledgers, Judgment outputs, and downstream
   completion/acknowledgement facts.
6. Preserve by-key discovery as authority before any runtime event/queue engine
   is built.

## What This Does Not Select

- Storage engine inside this contract; engine/backend choice is delegated to
  the Storage Contract physicalization boundary.
- Manifest v2.
- Attachment Record serialization.
- Sidecar contract.
- Projection cache.
- Runtime queue or scheduler.
- ECR, SCR, Cleaning, Judgment, or Evidence Unit (EvidenceUnit) schema.
- Fragrance ontology.
- Migration mechanics for incumbent fields.
- Validation/readiness claim.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Data Lake Core Contract v0 records the lake-owned responsibility boundary:
    raw packet preservation, stable by-key findability, content-free
    availability facts, source-payload Attachment Record rules, and logical
    append-only downstream result attachment, while excluding Cleaning, ECR,
    SCR interpretation, Judgment, orchestration, queue authority, physical
    storage selection, and fragrance/domain ontology from lake core. Post-review
    hardening keeps that boundary and clarifies passive availability, structural
    value/posture coupling, re-derive-never-migrate, promotion-rule citation,
    and derived-record/acknowledgement physical-home blockers.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/workflows/ecr_spine_submap_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        Root instructions already route Orca project facts and doctrine-changing
        work to the overlay and docs; this contract is product architecture, not
        a new agent-behavior kernel rule.
    - path: .agents/workflow-overlay/README.md
      reason: >
        No overlay section changed; the contract lives under the already
        accepted docs/product/core_spine folder.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Existing Data Capture and ECR read packs already route through the
        consolidation maps; those maps gain the new contract pointer instead of
        duplicating read-pack rules.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Source hierarchy and known-source mechanics are unchanged; this new
        product architecture contract is reachable through repo maps and lane
        maps rather than being added to the overlay known-source list.
  stale_language_search: >
    rg -n "Data Lake Core Contract|core_spine_v0_data_lake_core_contract_v0|data-lake mechanics|lake-owned|availability signal|physical storage|orchestration"
    docs/product/core_spine docs/product/data_capture_spine docs/workflows/data_capture_spine_consolidation_map_v0.md docs/workflows/ecr_spine_submap_v0.md docs/workflows/orca_repo_map_v0.md
    (run 2026-06-17 in worktree codex/data-lake-core-contract)
  stale_language_search_result: >
    Executed 2026-06-17 after delegated-review hardening. Expected hits observed
    in this contract, the data-lake mechanics map pointer,
    data_capture_spine_consolidation_map_v0.md, ecr_spine_submap_v0.md, and
    orca_repo_map_v0.md. Additional non-contradictory hits are substring hits on
    prompt-orchestration paths and existing payload, Retail/PDP,
    demand-durability, storage/projection, Cleaning, and ontology artifacts that
    preserve deferred physical-storage or source-family boundaries. No checked
    live routing surface contradicts the new lake boundary. The search does not
    validate implementation or physical storage.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not physical storage selection
    - not queue/runtime design
    - not ECR, SCR, Cleaning, Judgment, or fragrance ontology design
```

Older receipts are archived in `docs/decisions/dcp_receipts_archive_v0.md`.
