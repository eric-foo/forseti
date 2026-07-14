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

status: implemented contract for the product-mention and TikTok audience-evidence lanes

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

The source-less legacy capture lanes `silver__capture__audience_comments`,
`silver__capture__reel_transcript`, and
`silver__capture__reel_deep_capture__set` are also
`retired_silver_lineage`. Existing bytes remain audit-readable by explicit
lane/path lookup, but cannot establish Silver authority. The old deep-capture
writer fails visibly with `eligible_bronze_required`; this decision does not
invent or authorize a replacement Bronze producer.

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
  resolves and verifies, with hash/basis coupling;
- closed record kind, payload kind, and no Cleaning transform ledger in the fact;
- Text/Metric observation posture, row counts, row identity, inline-text hashes, and
  policy fingerprints;
- every Silver member of a detectable record set before any member is written.

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

- Historical bytes in the three retired source-less capture lanes are preserved
  for explicit audit lookup; they are not migrated, recaptured, or promoted to
  authority.
- Rejected LLM rows remain processing telemetry and are not copied into Silver
  facts. Historical grammar-B records retain their old rejection detail.
- Profile synthesis remains operator-run/provider-invoked at the existing cadence;
  this change does not make owner-gated LLM work automatic.
- No live data-lake migration is performed by this implementation. Existing
  committed packets re-derive only when the normal runner is invoked.

## Success signals

- no active product/audience producer writes grammar B;
- every newly written authority record passes common-header, hash, lineage, and
  payload validation before persistence;
- current readers select only the new envelope lane and fail closed on malformed
  records;
- old records remain audit-readable but cannot become current authority by fallback;
- audience profiles cite exact Silver evidence while remaining explicitly outside
  Silver Authority;
- a completed rerun has zero second-cycle provider work under the same obligation.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Silver authority now requires the current envelope plus physical
    verification of every exact claimed source at both write and read gates.
    The three remaining source-less silver__capture lanes are retired for
    authority, their historical bytes remain available for explicit audit, and
    the old writer now fails visibly with eligible_bronze_required instead of
    creating another source-less Silver record.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/silver_vault_legacy_record_convergence_v0.md
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
  intentionally_not_updated:
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
      reason: It already requires every claimed source to be resolvable and hash-verifiable; this work makes that existing contract executable at every authority gate.
  non_claims:
    - not a live-lake migration, recapture, or reprocessing authorization
    - not recovery of unavailable records
    - not a replacement Bronze producer
    - not validation or production readiness
```
