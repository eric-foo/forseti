# Silver Vault Legacy Record Convergence v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record (Silver Vault legacy-record convergence)
scope: >
  Binds the official Silver lanes, retired historical-lineage posture, reader
  cutover, source-less capture-lane retirement, and re-derivation contract for
  product mentions and TikTok audience evidence.
use_when:
  - Resolving current authority for product-mention or TikTok audience-evidence records.
  - Checking how legacy grammar-B records remain audit-readable without reader fallback.
  - Checking the authority posture of the retired source-less capture lanes.
stale_if:
  - A later accepted decision changes these lane roles, reader selection, or re-derivation semantics.
authority_boundary: retrieval_only
```

status: implemented Silver physical-authority and immutable legacy-read compatibility contract

authority: applies the Silver Vault Record Contract and Consumption Seam Contract to
the previously registered grammar-B cleaning lanes. It does not rewrite historical
lake bytes and does not authorize live capture, Gold/Judgment output, or automatic
LLM scheduling.

## Decision

New product-mention facts write to `transcript_product_mentions_silver`; new
quote-backed TikTok audience evidence writes to `tiktok_audience_evidence_silver`.
Both are `silver_vault_record_v0` `TextObservationSet` records written through the
validating Silver front door. Their completion-marker lanes are respectively
`transcript_product_mentions_completion` and
`tiktok_audience_evidence_completion`.

The prior product-mention, TikTok audience-evidence, and TikTok audience-profile
lanes remain registered as `retired_silver_lineage`. They remain discoverable for
audit but are not current reader or writer authority. No historical file is moved,
rewritten, or deleted.

The packet-first IG deep-capture route is current Silver authority: it preserves rendered-comment substrate and audio in a SourceCapturePacket, then writes exact packet/file/hash refs through the strict Silver front door. Pre-envelope deep-capture bytes remain audit-readable and non-authoritative; no legacy byte is rewritten or promoted.

The synthesized TikTok content-fit profile is not a source-backed Silver fact. New
profiles write to `tiktok_audience_profile_analysis` with
`role_posture=non_authoritative_analysis` and exact references to the Silver
evidence records they consumed. This lane must not be presented as actual audience,
demographic measurement, buyer proof, or a creator recommendation.

## Common write contract

Before persistence, the Silver front door verifies:

- the complete common header and write-target binding (`raw_anchor`, lane, record id);
- the canonical content hash and explicit hash basis;
- at least one raw or derived reference whose exact claimed source physically
  resolves and verifies: raw and Bronze body hashes use exact saved bytes with
  `raw_stored_bytes`; derived saved-byte hashes use `derived_record_bytes`, while
  derived canonical content hashes independently use
  `canonical_json_excluding_content_hash` with no cross-pair fallback;
- closed record kind, payload kind, and no Cleaning transform ledger in the fact;
- Text/Metric observation posture, row counts, row identity, inline-text hashes, and
  policy fingerprints;
- every Silver member of a detectable record set before any member is written.

## Immutable legacy-read compatibility

Strict new writes and compatible historical reads are separate obligations. The
write front doors require canonical reference types, closed hash bases, and exact
derived addresses. Read-time compatibility is limited to the exact declared
Fragrantica and creator-metric v0 producer/schema profiles. The original envelope
and content hash validate before any in-memory address inference; the stored
record is never mutated.

Legacy Fragrantica refs may infer only the unambiguous raw-packet type and the
record's validated anchor for its declared cleaning-audit source. Legacy creator
observations and rollups resolve only through the cross-epoch creator lineage
index, including exact rollup record-id/content-hash matching. Unknown,
contradictory, ambiguous, or unresolved forms fail closed. Absence of
lineage_schema_version alone is not evidence failure; a present value must
validate.
## Reader selection

Current `by_mention` and share-of-voice readers scan only
`transcript_product_mentions_silver`. A record is countable only after both the
common-envelope validator and the source-backed lineage gate pass. The readers do
not fall back to the retired lane. Historical grammar-B records can be inspected by
explicit lane/path lookup only.

## Re-derivation and idempotency

The product and audience runner obligations include their output record-schema
versions. The envelope migration therefore changes the obligation fingerprint and
re-surfaces previously acknowledged packets without recapture. Deterministic record
ids plus completion markers preserve second-cycle-zero behavior after successful
re-derivation. Partial sets remain visible and are never acknowledged as complete.

## Accepted residuals

- The 226 declared historical creator records remain audit-readable but not current; owner: creator-metric Silver owner; upgrade trigger: source recapture or newly mounted exact cited bytes.
- The 40 historical deep-capture records and 92 retired-lane records remain audit-only; owner: Silver lane owners; upgrade trigger: separately authorized source-backed rederivation, never byte rewriting.
- Rejected LLM rows remain processing telemetry and are not copied into Silver
  facts. Historical grammar-B records retain their old rejection detail.
- Profile synthesis remains operator-run/provider-invoked at the existing cadence;
  this change does not make owner-gated LLM work automatic.
- No live data-lake migration is performed by this implementation. Existing
  committed packets re-derive only when the normal runner is invoked.
- The 196-observation YouTube unit fixture is explicitly synthetic structural
  proof of the physical verifier and does not show that private-lake seed sources
  resolve. The focused watch-HTML proof likewise uses a temporary committed packet.

## Success signals

- strict front doors reject nonexistent, tampered, non-canonical, and declared
  legacy read-only refs before any write;
- exact declared legacy Fragrantica and creator records classify without mutating
  their stored mapping, while unknown or ambiguous forms fail closed;
- census and authority readers agree on current, historical, invalid, and
  unresolved outcomes through the shared physical classifier;
- no authority reader uses structural lineage completeness as physical proof;
- packet-first IG deep capture remains current and cross-anchor substitution
  cannot inflate current totals;
- at live acceptance fingerprint
  `ef1566100296e0d53d48904e144fb6e84765f2cc886a828194683178a3c620df`:
  7,836 stored Silver records, 7,478 current-source-backed, 226 creator
  historical-compatible, and zero unexplained errors, with 40 historical deep
  capture and 92 retired-lane records excluded from current evidence;
- the +94 records since the prior 7,742-record snapshot reconcile exactly to
  TikTok comment-attention Silver: the unchanged 5,040 Fragrantica and 1,306
  creator records plus 10 social-metric observation sets leave 1,348 TikTok
  records now versus 1,254 in the prior 1,264 token-bearing pool;
- no live-lake write, migration, recapture, or immutable-record rewrite occurs;
- focused tests, full harness CI, contract/inventory gates, final read-only live
  census, and PR checks all pass at one final pushed head.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Silver authority now separates immutable envelope validation, strict canonical new writes, root-aware physical resolution, bounded declared legacy reads, and lane-specific selection. Packet-first IG deep capture remains current; historical deep-capture and retired-lane bytes remain audit-only. Structural lineage status cannot establish physical authority.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/silver_vault_legacy_record_convergence_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
    - forseti-harness/data_lake/silver_record.py
    - forseti-harness/data_lake/silver_lineage.py
    - forseti-harness/data_lake/product_mention_selection.py
    - forseti-harness/data_lake/lane_registry.py
    - forseti-harness/source_capture/ig_reels_deep_capture_lake.py
    - forseti-harness/data_lake/silver_census.py
    - forseti-harness/source_capture/ig_reels_behavioral_lake.py
    - forseti-harness/source_capture/ig_reels_behavioral_projection.py
    - forseti-harness/data_lake/inventory.py
    - forseti-harness/data_lake/lake_touchpoint_inventory_v0.json
    - forseti-harness/capture_spine/creator_profile_current/silver_metric_producer.py
    - forseti-harness/capture_spine/creator_profile_current/youtube_silver_metric_producer.py
    - forseti-harness/cleaning/basenotes_lake.py
    - forseti-harness/cleaning/fragrantica_lake.py
    - forseti-harness/cleaning/parfumo_lake.py
    - forseti-harness/tests/contract/test_policy_module_version_pins.py
    - forseti-harness/tests/test_silver_lane_registry_guard.py
    - forseti-harness/tests/test_ig_reels_deep_capture_lake.py
    - forseti-harness/tests/test_silver_census_behavior.py
  non_claims:
    - not a live-lake migration, recapture, or reprocessing authorization
    - not recovery of unavailable records
    - not a replacement Bronze producer
    - not validation or production readiness
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    The existing physical-authority rule now closes each hash claim to its exact
    byte interpretation: raw and Attachment Record sha256 claims use
    raw_stored_bytes; derived sha256 claims use derived_record_bytes; and derived
    content_hash claims independently use canonical_json_excluding_content_hash.
    The two derived pairs may coexist but never alias or satisfy one another.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - docs/decisions/silver_vault_legacy_record_convergence_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  downstream_surfaces_checked:
    - forseti-harness/data_lake/silver_record.py
    - forseti-harness/data_lake/silver_lineage.py
    - forseti-harness/capture_spine/creator_profile_current/youtube_silver_metric_producer.py
    - forseti-harness/capture_spine/creator_profile_current/silver_metric_producer.py
    - forseti-harness/tests/unit/test_silver_record.py
    - forseti-harness/tests/unit/test_silver_lineage.py
    - forseti-harness/tests/unit/test_youtube_creator_metric_silver_producer.py
  non_claims:
    - not a new Silver envelope
    - not a new source lane, registry, migration, recapture, or reprocessing
    - not proof that unavailable private-lake records have recovered
    - not validation, Mini God Tier, or production readiness
```
