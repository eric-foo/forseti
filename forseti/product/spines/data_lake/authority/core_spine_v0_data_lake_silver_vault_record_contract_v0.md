# Core Spine v0 Data Lake Silver Vault Record Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract
scope: >
  Forward v4.1 record-schema contract for Silver Vault records and the generated
  Creator Vault read layer. Locks the smallest complete schema invariants needed
  before implementation scoping: generic derived pathing, record header fields,
  entity/relationship/observation payload boundaries, metric posture/value
  coupling, coverage windows, correction/conflict edges, read-model manifests,
  and Creator Vault non-dossier guardrails.
use_when:
  - Scoping Silver Vault record producers or read-model builders.
  - Checking whether Creator Vault remains a generated Silver read layer.
  - Checking metric observation, correction, conflict, or envelope schema shape.
  - Preventing SQL/query tables from treating missing evidence as zero or truth.
open_next:
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
  - forseti-harness/source_capture/models.py
  - forseti-harness/source_capture/ig_reels_grid_projection.py
downstream_consumers:
  - Silver Vault record producer scoping
  - Creator Vault read-model/envelope builder scoping
  - SQL/query-table scoping
  - IG creator/content proving-slice scoping
stale_if:
  - The v4.1 forward-epoch folder grammar or derived-record addressing grammar changes.
  - MetricObservation, MetricPosture, CoverageWindow, or IG selection-policy fields change.
  - The owner authorizes persistent actor profiles, cross-platform person identity, or Creator Vault Gold/Judgment outputs.
  - A later accepted Silver Vault contract supersedes this candidate.
authority_boundary: retrieval_only
```

## Status

`SILVER_VAULT_V4_1_FORWARD_RECORD_CONTRACT_SELECTED_V0`.

Owner direction recorded 2026-06-28: v4.1 is a clean forward epoch, not a
compatibility migration of the small current lake. Silver Vault uses canonical lake folders with v4.1 record semantics. This is not implementation
authority, validation, readiness, backend selection, graph/vector engine
selection, client launch approval, or Judgment authorization.

## Decision In One Screen

```text
Silver Vault authority lives in append-only derived records:

derived/<anchor_shard>/<raw_anchor>/<lane_namespace>/<record_id>.json

The path stays generic. Meaning lives inside the record.

Generated read models live under:

indexes/derived_retrieval/silver_vault/...

Creator Vault is a first-class generated Silver read layer over public
per-platform account/content evidence. It is not a second database, not a person
dossier, and not Gold/Judgment.
```

## Medallion Label Map

Physical folder names stay canonical. Medallion names are labels for docs, UI,
and operator explanation; they are not path changes.

| Physical slot | Medallion label | Meaning |
| --- | --- | --- |
| `raw/` | Bronze | Raw evidence packets and preserved source material. |
| `derived/` | Silver Authority | Append-only source-backed semantic records. |
| `indexes/derived_retrieval/silver_vault/core/` | Silver Retrieval | Generated cross-domain query tables and read models. |
| `indexes/derived_retrieval/silver_vault/creator_vault/` | Silver Retrieval / Creator Vault | Generated client-facing creator/account/content read layer. |
| Judgment outputs | Gold | Judgment-owned interpretation, recommendations, durability/manufactured-demand verdicts, and action meaning. |

Do not rename folders to `bronze/`, `silver/`, or `gold/`. The canonical v4.1 lake
slots are `raw/`, `attachments/`, `derived/`, `acknowledgements/`, and `indexes/`,
owned by the v4.1 forward-epoch and physicality-location contracts; this contract
restates them for orientation only and does not redefine the folder grammar.

## Required Behavior

Silver Vault records must let downstream builders reconstruct source-backed
entities, relationships, observations, corrections, conflicts, query tables, and
Creator Vault envelopes without inventing:

- semantic meaning from folder paths;
- numeric values for missing evidence;
- cross-platform person identity;
- source trust, credibility, salience, durability, manufactured-demand, or action
  meaning.

## Non-Goals

This contract does not authorize:

- changing raw pathing or derived pathing;
- adding a graph engine, vector engine, scheduler, queue, or backend;
- implementing SQL/query tables;
- implementing Creator Vault UI/API/client replicas;
- making Creator Vault a source of truth;
- cross-platform identity resolution by default;
- Gold/Judgment outputs in Silver or Creator Vault;
- private/profile/contact/person dossier fields.

## Derived Record Placement

Authoritative Silver Vault records attach to the v4.1 physicalized derived
grammar:

```text
derived/<anchor_shard>/<raw_anchor>/<lane_namespace>/<record_id>.json
```

Rules:

- `<raw-anchor>` is the raw anchor owned by the lake grammar.
- `<lane-namespace>` is producer-owned and must not be frozen into a global
  entity/relationship/observation taxonomy.
- `<record-id>` is create-only and one-record-per-file.
- Corrections are new records, never rewrites.
- Cross-object retrieval is generated under `indexes/derived_retrieval/`, not
  encoded as new authoritative lake structure.

## Common Record Header

Every Silver Vault record must carry this common header or an equivalent
schema-versioned envelope with the same fields.

```json
{
  "record_id": "01...",
  "raw_anchor": "packet-or-narrower-raw-anchor",
  "lane_namespace": "producer-owned-lane",
  "producer_id": "producer-or-builder-id",
  "schema_version": "silver_vault_record_v0",
  "producer_schema_version": "producer_schema_v0",
  "content_hash": "sha256:...",
  "content_hash_basis": "canonical_json_excluding_content_hash",
  "record_kind": "entity | relationship | observation",
  "payload_kind": "ProductEntity | MetricObservation | TextObservation | CorrectionEdge | ...",
  "producer_row_kind": "ig_media_metric | retail_variant_offer | ...",
  "source_surface": "source-visible-surface-token",
  "observed_at": "2026-06-28T00:00:00Z",
  "captured_at": "2026-06-28T00:00:00Z",
  "raw_refs": [],
  "derived_refs": []
}
```

Header invariants:

| Field | Contract |
| --- | --- |
| `record_kind` | Closed v0 enum: `entity`, `relationship`, `observation`. |
| `payload_kind` | Silver payload discriminator. Must not replace producer/source-family row kind. |
| `producer_row_kind` | Carries source-family subtype when present, such as IG projection `row_kind`. |
| `content_hash` | Required durable integrity hash for the canonical record content; hash basis must be explicit and must not include the `content_hash` field itself. |
| `observed_at` | Time the fact was observed at or about the source. Nullable only for internal relationship records with no source observation time. |
| `captured_at` | Time Forseti captured the source material or producer input. |
| `raw_refs` | Required for source-backed records; each ref must resolve packet/slice/file. When `sha256` is claimed, it hashes the exact preserved body bytes and its paired `hash_basis` is exactly `raw_stored_bytes`. Source-family payload refs must honor the Bronze intake boundary below. |
| `derived_refs` | Required when a record corrects, supersedes, conflicts with, or is generated from prior derived records. A claimed `sha256` pairs only with `hash_basis: derived_record_bytes` and hashes the exact saved derived-record bytes. A claimed `content_hash` pairs independently with `content_hash_basis: canonical_json_excluding_content_hash`; either pair may appear, both may coexist, and neither aliases or substitutes for the other. |

## Bronze Intake And Attachment Record Boundary

Silver source-backed records must enter raw truth through Bronze-owned surfaces,
not raw-path inference.

Allowed Bronze intake surfaces are:

- raw packet refs from CapturePacket manifests or Bronze catalog packet rows;
- source-surface rows returned by public catalog helpers;
- Attachment Record query rows and `load_attachment_record_body` for
  source-family payload bodies.

When a Silver producer derives a source-backed fact from a source-family payload
body and an Attachment Record row exists, `raw_refs` must carry an AR-backed raw
ref rather than a private packet-member path guess. The Silver record does not
copy the body as authority; it carries enough AR material to re-resolve and
verify the body: `attachment_record_id`, schema version, physicalization,
`packet_id`, packet/body ref, `body_sha256`, `hash_basis`, `source_family`,
`source_surface`, `payload_kind`, `payload_schema_version`, replay/version pins, and any
producer-owned provenance required by that producer contract.
The ref and public catalog row must agree that the body hash is over exact saved
bytes with `hash_basis: raw_stored_bytes`; altered bytes, a different basis, or a
different hash make the source physically unresolved.

If no Attachment Record row exists, a Silver producer may cite hash-checkable raw
packet refs when its contract allows that fallback, but it must make the missing
typed AR residual visible. Missing AR is not evidence that the source payload was
absent.

Silver must not declare Bronze full GT, reimplement private catalog safe-name or
path rules, or treat generated Bronze catalog files as authority over raw packet
material.

## Not Silver: Cleaning Audit Packs

A full Cleaning transformation ledger (the complete `CleaningPacket` / transform
ledger) is **processing evidence, not a Silver fact record**. It must not be
stored as a Silver Vault record under any `record_kind`: `record_kind` stays
closed to `entity | relationship | observation`, and an `observation` payload
must carry an observation object (subject/posture/value or text semantics), which
a transform ledger does not.

Instead the ledger persists as a **derived processing-audit sibling** in a
Cleaning-produced lane (for example `cleaning_fragrantica_audit`), addressed and
stored under the Data Lake's derived-record grammar. Its
`schema_version: cleaning_audit_pack_v0` is the shared derived envelope for
Cleaning audit packs — reusable by any Cleaning lane — with
`record_family: processing_audit` and a per-source `producer_schema_version`
flavor. That `record_family` / `audit_kind` are
**local descriptive fields of `cleaning_audit_pack_v0` only and carry no
Data-Lake-wide dispatch authority** unless and until a generic derived-record
envelope is separately ratified.

Post-cleaned cleaned-working-view facts (for example a review-body
`TextObservation`) may be emitted as ordinary Silver records. Because such a
record is generated from a prior derived record, its audit-pack lineage goes in
the standard `derived_refs` header (edge `derived_from_record`, carrying the
audit lane namespace, record id, and content hash) — not a producer-private
sidecar field. Silver records reference the audit pack; they do not embed the
transform ledger.

## Entity Records

Entity records define stable source-backed identity only.

```json
{
  "record_kind": "entity",
  "payload_kind": "PlatformAccountEntity",
  "entity": {
    "entity_type": "product | platform_public_account | public_content_object | retailer_listing | review | text_artifact | category | claim",
    "entity_key": {
      "namespace": "instagram",
      "kind": "platform_public_account",
      "native_id": "17841400000000000"
    },
    "identity_source": {
      "raw_refs": [],
      "derived_refs": []
    }
  }
}
```

Entity invariants:

- Entity records must not hold time-varying facts such as handle, display name,
  follower count, price, availability, review count, product copy, caption text,
  or transcript text.
- Time-varying facts are observations keyed to the entity.
- Creator Vault account entities are per-platform public account objects.
- Creator Vault v0 must not emit a default global `person_id` or cross-platform
  person identity.
- Campaign or coordination entities are not Silver Vault v0 entity types unless a
  future source-captured campaign object contract defines their source identity.
  Manufactured-demand or campaign-coordination meaning belongs to Gold/Judgment.

## Relationship Records

Relationship records connect entities or records. They also carry correction,
supersession, tombstone, and conflict semantics.

```json
{
  "record_kind": "relationship",
  "payload_kind": "RelationshipEdge",
  "relationship": {
    "edge_type": "content_mentions_product",
    "from": {
      "ref_type": "entity_key",
      "ref": {}
    },
    "to": {
      "ref_type": "entity_key",
      "ref": {}
    },
    "evidence": {
      "raw_refs": [],
      "derived_refs": [],
      "source_span": null,
      "confidence": null
    }
  }
}
```

Minimum v0 edge types:

```text
derived_from_record
content_published_by_account
content_mentions_product
text_mentions_product
text_mentions_claim
text_mentions_category
text_compares_product_to_product
comment_on_content
review_of_product
review_on_listing
listing_of_product
corrects_record
supersedes_record
tombstones_record
conflicts_with_record
```

Correction and conflict invariants:

- Correction, supersession, tombstone, and conflict are relationship records,
  not separate `record_kind` values.
- Record-changing edges must reference record ids, not only entity keys.
- A correction says a prior record was wrong in a stated way.
- A supersession says a newer record replaces a prior record for current/latest
  generated views without erasing the prior historical record.
- A conflict says two records disagree on a field, source, timestamp, posture, or
  identity relation. Silver preserves the conflict; Gold decides meaning.

## Metric Observation Records

Metric observations must mirror the live `MetricObservation` discipline:

```json
{
  "record_kind": "observation",
  "payload_kind": "MetricObservation",
  "observation": {
    "subject": {
      "ref_type": "entity_key",
      "ref": {}
    },
    "metric_name": "view_count",
    "metric_value": 12345,
    "metric_posture": {
      "kind": "observed",
      "reason_code": null,
      "reason_detail": null
    },
    "coverage_window": {
      "start": "2026-06-21T00:00:00Z",
      "end": "2026-06-28T00:00:00Z"
    },
    "source_surface": "instagram_grid",
    "source_publication_or_event": null,
    "source_surface_count_candidates": [],
    "unit": "count"
  }
}
```

Metric posture invariants:

| Condition | Required behavior |
| --- | --- |
| `metric_posture.kind = observed` | `metric_value` is present and reason fields are absent/null. |
| `metric_posture.kind != observed` | `metric_value` is null and a reason is present. |
| `metric_value = 0` | Valid only as a real observed zero from the source. Never means missing. |
| Missing, hidden, blocked, not attempted, not applicable, outside window | Must be represented by posture + reason, not by numeric value. |
| `coverage_window` | Required for time-series/durability use where the observation claims a measurement window. |
| `source_publication_or_event` | Preserve the live producer field name when the source row distinguishes publication/event timing from capture time. |
| `source_surface_count_candidates` | Preserve live source-surface candidate counts when present; candidates are evidence for generated selection policy, not Silver trust adjudication. |

Allowed v0 posture values must map to the live source-capture posture vocabulary
instead of inventing a looser free-text set.

## Text Observation Records

Text observations carry source-backed text, text refs, or explicit absence.

```json
{
  "record_kind": "observation",
  "payload_kind": "TextObservation",
  "observation": {
    "subject": {
      "ref_type": "entity_key",
      "ref": {}
    },
    "text_artifact_type": "caption | transcript | top_comment | review_body | listing_copy | search_phrase",
    "text_value": "source-backed text when stored inline",
    "text_ref": null,
    "text_hash": "sha256:...",
    "text_posture": {
      "kind": "observed",
      "reason_code": null,
      "reason_detail": null
    },
    "coverage_window": {
      "start": null,
      "end": null
    },
    "source_span": null
  }
}
```

Text invariants:

- Observed text must have either `text_value` or a resolvable `text_ref`.
- Inline observed text must carry `text_hash`.
- Non-observed text must keep `text_value` null and carry posture + reason.
- Top comments, transcripts, captions, reviews, and listing copy are evidence,
  not Judgment.

## IG Metric Selection Policy

IG v0 metric selection is a generated-read concern over source-backed metric
observations.

Required behavior:

- Grid capture is the primary v0 source for views, likes, and comments_count.
- Per-reel capture is detail evidence for audio, transcript, caption/detail, and
  top comments.
- Per-reel counts may be preserved as non-primary metric observations when seen.
- Per-reel counts must not supersede grid-primary current metric snapshots unless
  a later selection policy version explicitly changes that rule.
- Generated metric read models must expose `selection_policy_version`.
- Generated metric read models must preserve `source_surface_count_candidates`
  when present so grid-primary selection remains mechanically auditable.

Use the existing IG precedent `selection_policy_version`; do not introduce a
global `metric_policy_id` as lake authority.

## Generated Read Models

Generated read models live under:

```text
indexes/derived_retrieval/silver_vault/
  core/
    query_tables/
    manifests/
  creator_vault/
    accounts/<platform>/<account_id>/envelope.json
    content/<platform>/<content_kind>/<content_id>/envelope.json
    query_tables/
    manifests/
```

Read-model rules:

- Generated read models are not authority.
- By-key discovery over committed `derived/` records is the current retrieval
  authority. Query tables and the wider `derived_retrieval` population are
  rebuildable, non-authoritative views whose build is governance- and
  scan/query-latency-gated by the Derived Layout + Index Rebuild Contract; SQL is
  the selected query lens when that trigger fires, not an unconditional v0 path.
- Query tables must be rebuildable from committed raw + derived records.
- Query tables must expose posture and coverage fields needed to prevent SQL
  from treating missing evidence as zero.
- Every generated query table and envelope must have a manifest row.
- Every manifest row must expose generation id, source record ids, source
  high-watermark, selection policy versions used, generated_at, and stale/drift
  detection fields.

## Creator Vault Placement And Sync Clarifications

Creator Vault account and content envelopes use sibling physical homes. The
examples below are platform-specific read-model keys, not platform-specific
authority:

```text
creator_vault/
  accounts/
    instagram/<account_id>/envelope.json
    tiktok/<account_id>/envelope.json
    youtube/<channel_id>/envelope.json
  content/
    instagram/reel/<media_id>/envelope.json
    tiktok/video/<video_id>/envelope.json
    youtube/short/<video_id>/envelope.json
```

Placement rules:

- Keep `accounts/` and `content/` as sibling generated read-model homes. Do not
  nest content physically under accounts.
- Account-scoped content pages are generated views built from account keys,
  content keys, and `content_published_by_account` relationship edges. Physical
  placement is not ownership authority.
- `acknowledgements/` is lane-level append-only processing/audit receipt space
  keyed by raw anchor and acknowledgement namespace. Creator Vault envelopes may
  point to relevant acknowledgement refs or manifest ids, but acknowledgements
  are not embedded in envelopes as authority.
- A client carveout is a filtered Creator Vault replica or export generated from
  the same Silver records and read-model manifests. It must preserve manifest
  ids, source high-watermarks, raw refs, derived refs, and selection-policy
  versions so Forseti full can consume the same evidence without a special request
  path. The replica is not a duplicate capture source by default; duplicate
  capture is only needed when the carveout has independent freshness, SLA, or
  source-access constraints.

Relationship/source-ref examples:

- Instagram reel `public_content_object` `content_published_by_account`
  Instagram `platform_public_account`.
- TikTok video `public_content_object` `content_published_by_account` TikTok
  `platform_public_account`.
- YouTube short `public_content_object` `content_published_by_account` YouTube
  channel `platform_public_account`.
- `review` `review_of_product` `product`.
- `retailer_listing` `listing_of_product` `product`.
- Caption, comment, transcript, or review text `text_mentions_product` or
  `text_mentions_claim`.
- Grid metric observation `conflicts_with_record` per-reel metric observation
  when the source surface, timestamp, posture, or value disagrees. Silver
  preserves the conflict; generated selection policy may choose the read-model
  value, and Gold/Judgment decides meaning only when a downstream question asks.

## Creator Vault Envelope Guardrails

Creator Vault is a first-class generated Silver read layer. Its envelopes may
summarize public, per-platform account/content evidence.

Creator Vault envelopes must include:

```text
envelope_type
platform
account_key or content_key
latest_metric_snapshot
coverage_summary
metric_postures
coverage_windows
source_conflicts
raw_refs
derived_refs
query_table_pointers
read_model_manifest_id
judgment_boundary
per_platform_identity_only = true
cross_platform_identity_assumed = false
```

Creator Vault envelopes must not include:

```text
person_id
private_contact
outreach_status
demographics
credibility_score
fake_or_bot_label
paid_or_unpaid_verdict
manufactured_demand_verdict
durability_verdict
partnership_recommendation
investment_recommendation
action_priority
gold_score
```

Safe wording:

```text
Allowed: evidence-ranked creator candidates based on captured public signals.
Forbidden: creators we should partner with.

Allowed: observed source disagreement.
Forbidden: which source is trustworthy.

Allowed: observed timing, phrases, conflicts, and coverage gaps.
Forbidden: manufactured demand verdict.
```

## Acceptance Criteria

The contract is satisfied when downstream scoping can prove, in principle, that:

1. No authoritative Silver Vault meaning is inferred from folder path beyond the
   v4.1 physicalized derived grammar.
2. Every authoritative Silver Vault record is one file under
   `derived/<anchor_shard>/<raw_anchor>/<lane_namespace>/<record_id>`.
3. Every record has `record_kind` and `payload_kind`; source-family row subtype is
   preserved separately when present.
4. Entity records contain stable identity only; mutable facts are observations.
5. Every record carries a durable `content_hash` with explicit hash basis. Raw
   and AR-backed refs pair any claimed `sha256` only with
   `hash_basis: raw_stored_bytes`; derived refs pair `sha256` only with
   `hash_basis: derived_record_bytes` and independently pair `content_hash` only
   with `content_hash_basis: canonical_json_excluding_content_hash`.
6. Metric observations obey posture/value/reason coupling and preserve
   coverage_window where time-series meaning depends on a window.
7. Missing, blocked, hidden, not-attempted, not-applicable, and outside-window
   metrics cannot be read as numeric zero.
8. Corrections, supersessions, tombstones, and conflicts are append-only
   relationship records.
9. Campaign/coordination entities or edges are excluded from Silver v0 unless a
   future source-captured campaign object contract defines them mechanically.
10. Generated read models and Creator Vault envelopes are manifest-backed,
   rebuildable, and non-authoritative.
11. Creator Vault envelopes are per-platform, public-evidence-only, and contain no
   Gold/Judgment fields.
12. IG grid-primary metrics cannot be silently overwritten by per-reel detail
    captures under the same selection policy version.
13. Creator Vault account and content envelopes keep sibling physical placement;
    account-scoped displays are generated from relationship edges, not physical
    nesting.
14. Client carveout replicas or exports are generated from Silver records and
    read-model manifests, preserve refs/high-watermarks, and are not a separate
    source of truth.
15. Source-backed Silver `raw_refs` consume public Bronze packet/catalog/AR
    surfaces rather than private raw folder semantics.
16. AR-backed source-family payload refs are body-hash-verifiable, and missing
    AR rows become visible residual/posture instead of inferred absence.
17. Derived `sha256` and `content_hash` pairs are independently optional where
    the producer contract permits them, may coexist, and cannot satisfy or fall
    back to one another during validation or physical verification.

## Mini God Tier Accepted Residuals

This contract deliberately stops short of maximal infrastructure.

Each residual names the foregone slice, why it is acceptable now, the remaining
risk, and the upgrade trigger (per `docs/decisions/forseti_mini_god_tier_doctrine_v0.md`):

- **No graph/vector engine in v0.** By-key discovery plus SQL query tables prove
  the foundation without engine/maintenance burden. Risk: relationship-heavy or
  semantic queries may scan slowly at scale. Upgrade trigger: scan/query latency
  proves insufficient, routing engine choice to the Storage Contract
  physicalization boundary (never as authority).
- **No cross-platform person identity in Creator Vault v0.** Per-platform public
  identity avoids dossier and identity-merge risk and honors the medallion
  give-up. Risk: a unified cross-platform creator view must be stitched
  downstream. Upgrade trigger: owner authorizes cross-platform person identity
  (see `stale_if`).
- **No Creator Vault recommendations or Gold/Judgment outputs.** Keeps Creator
  Vault pre-Judgment Silver and preserves the Gold boundary. Risk: client-facing
  "who to partner with" framing waits for Judgment. Upgrade trigger: Judgment
  consumes Creator Vault by reference and emits Gold separately.
- **No full review/retail/SEO implementation implied by the schema.** The generic
  record schema spans these domains without committing per-domain producers now.
  Risk: each domain still needs its own producer lane and per-lane record
  contract before capture. Upgrade trigger: a domain's first proving slice is
  scoped.
- **No universal metric arbitration; IG v0 uses grid-primary selection policy.**
  One platform's selection policy is enough to prove metric selection. Risk: each
  further platform/metric family needs its own `selection_policy_version`; no
  global arbiter exists. Upgrade trigger: a second platform/metric family needs a
  selection policy (added as a new `selection_policy_version`, never a global
  `metric_policy_id` as lake authority).
- **No guaranteed comment/transcript coverage in v0.** Partial coverage is allowed
  only when posture and coverage state make the gap visible (no fake
  completeness). Risk: time-series or sentiment consumers over comments/
  transcripts may see gaps and must read posture/coverage. Upgrade trigger: a
  consumer needs guaranteed coverage, scoping a capture-completeness obligation.
- **No client replica implementation in this contract.** It defines replica sync
  semantics only: any client carveout replica/export is generated from Silver
  records and read-model manifests, not a separate source of truth or duplicate
  capture source by default. Risk: physical replication, freshness, and SLA
  mechanics remain undefined until a replica lane is scoped. Upgrade trigger: a
  client carveout replica is commissioned, and must remain a generated,
  read-only, manifest-backed consumer.

## Downstream Handoff

Implementation scoping may rely on:

- the architecture placement in this contract;
- the three authoritative `record_kind` values;
- `payload_kind` as the Silver payload discriminator;
- `producer_row_kind` as the source-family subtype carrier;
- public Bronze catalog and Attachment Record helper consumption for
  source-backed raw refs;
- entity records as identity-only;
- correction/conflict semantics as relationship records;
- metric observations as posture/value/reason/coverage-window coupled;
- Creator Vault as generated per-platform public evidence, not authority or
  Judgment;
- Creator Vault account/content sibling placement, acknowledgement-ref boundary,
  and carveout sync semantics as generated read-layer concerns.

Deferred to scoping:

- exact serialization syntax;
- exact manifest column names;
- exact SQL table partitioning;
- concrete producer lane names;
- exact first proving-slice implementation order.

```yaml
spec_handoff:
  status: SPEC_COMPLETE_READY_FOR_SCOPING
  required_behavior: >
    Silver Vault records must preserve source-backed semantic facts under the
    v4.1 physicalized derived grammar and generate Creator Vault read models without
    path-inferred meaning, fake zeros, dossier behavior, or Gold leakage.
  non_goals:
    - graph/vector engine selection
    - SQL implementation
    - client replica implementation
    - cross-platform person identity
    - Gold/Judgment output
  interfaces_contracts:
    - derived/<anchor_shard>/<raw_anchor>/<lane_namespace>/<record_id>.json
    - indexes/derived_retrieval/silver_vault/...
    - record_kind: entity | relationship | observation
    - payload_kind as Silver payload discriminator
    - producer_row_kind as source-family subtype carrier
    - Bronze catalog / Attachment Record surfaces for source-backed raw refs
    - MetricObservation posture/value/reason/coverage-window coupling
  acceptance_criteria:
    - records are append-only one-record-per-file
    - entity records are identity-only
    - non-observed metrics carry no value and have reason
    - generated read models are manifest-backed and rebuildable
    - source-backed raw_refs use public Bronze packet/catalog/AR surfaces
    - Creator Vault envelopes contain no forbidden Judgment/dossier fields
  deferred_open_questions:
    - exact serialization syntax
    - exact manifest column names
    - exact SQL table partitioning
    - concrete producer lane names
    - exact first proving-slice implementation order
  scoping_may_rely_on: >
    The Silver Vault v0 foundation is a generic derived-record contract plus
    generated read models. Creator Vault is the first client-facing read layer,
    but remains generated, per-platform, public-evidence-only, and non-Gold.
```

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Silver v0 hash bases are closed physical claims. Raw-packet and Bronze
    Attachment Record sha256 values hash exact preserved body bytes and pair only
    with raw_stored_bytes. Derived sha256 values hash exact saved derived-record
    bytes and pair only with derived_record_bytes. A derived content_hash is a
    separate canonical-record claim paired only with
    canonical_json_excluding_content_hash; either derived pair may appear, both
    may coexist, and neither aliases or falls back to the other.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
    - docs/decisions/silver_vault_legacy_record_convergence_v0.md
  downstream_surfaces_checked:
    - forseti-harness/data_lake/silver_record.py
    - forseti-harness/data_lake/silver_lineage.py
    - forseti-harness/capture_spine/creator_profile_current/youtube_silver_metric_producer.py
    - forseti-harness/tests/unit/test_silver_record.py
    - forseti-harness/tests/unit/test_silver_lineage.py
    - forseti-harness/tests/unit/test_youtube_creator_metric_silver_producer.py
  intentionally_not_updated:
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
      reason: >
        Its raw_stored_bytes rule already owns Attachment Record body hashing;
        this clarification closes the Silver ref-side interpretation and catalog
        agreement check without changing the Bronze envelope.
    - path: forseti-harness/capture_spine/creator_profile_current/silver_metric_producer.py
      reason: >
        Its emitted source-ref hash meaning was already exact raw stored bytes and
        required no producer-schema change.
  stale_language_search: >
    rg -n "raw_stored_bytes|derived_record_bytes|canonical_json_excluding_content_hash|source_evidence_hash_basis"
    forseti-harness/data_lake forseti-harness/capture_spine/creator_profile_current
    forseti-harness/tests/unit
  non_claims:
    - not a Silver envelope version change
    - not a hash-basis registry or normalization framework
    - not live-lake migration, recapture, or reprocessing
    - not proof that private-lake seed sources resolve
    - not validation or production readiness
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Silver Vault now binds source-backed raw intake to public Bronze packet,
    catalog, and Attachment Record surfaces: Silver raw_refs must not infer
    meaning from raw folder layout, must carry AR-backed refs for source-family
    payload bodies when AR rows exist, and must make missing typed AR rows a
    visible residual instead of inferred absence.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
    - forseti/product/spines/data_lake/README.md
    - docs/workflows/forseti_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
    - forseti-harness/data_lake/catalog.py
  intentionally_not_updated:
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
      reason: >
        The core contract already owns the raw packet / Attachment Record logical
        boundary. This patch binds Silver consumption mechanics without changing
        the parent no-smart-lake boundary.
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
      reason: >
        Medallion semantics are unchanged: Bronze remains raw evidence and Silver
        remains source-backed semantic records. This patch only names the public
        Bronze surfaces Silver must use.
    - path: forseti-harness/data_lake/catalog.py
      reason: >
        The required public Bronze helpers and AR body loader already exist in
        the post-PR-525 baseline; this patch does not authorize new runtime code.
  stale_language_search: >
    rg -n "Silver.*Bronze|raw_refs|Attachment Record|full God Tier|bronze_mgt"
    forseti/product/spines/data_lake docs/workflows/forseti_repo_map_v0.md forseti-harness/data_lake/catalog.py
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not full Bronze God Tier
    - not Silver producer implementation
```
Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
