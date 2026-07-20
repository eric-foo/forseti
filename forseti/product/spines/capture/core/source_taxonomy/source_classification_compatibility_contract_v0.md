# Capture Source Classification Compatibility Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Capture source-classification compatibility contract
scope: >
  Canonical multi-axis, re-derivable classification view over incumbent
  SourceCapturePacket source_family/source_surface strings.
use_when:
  - Interpreting a committed legacy source-family/source-surface pair.
  - Adding a source pair to the runtime classification inventory.
  - Reading source classification from the generated Bronze catalog.
authority_boundary: architecture_doctrine
open_next:
  - forseti-harness/source_capture/source_classification.py
  - forseti-harness/source_capture/models.py
  - forseti-harness/data_lake/catalog.py
  - forseti/product/spines/capture/core/source_families/README.md
  - forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
stale_if:
  - SourceCapturePacket replaces the incumbent source_family/source_surface fields.
  - The runtime registry or Bronze source-surface catalog stops deriving this view.
  - Evidence-shape classification moves to another owning contract.
  - Cleaning stops owning current canonical-content validation and source adaptation.
```

## Decision

Keep the exact incumbent `source_family` and `source_surface` strings as raw
Capture compatibility facts. Derive, rather than persist back into packets, one
closed classification view with independent axes:

1. concrete operator/platform or venue identity, when the pair proves it;
2. one or more venue/source roles;
3. venue subtype where meaningful, including `general` versus `specialist`
   community;
4. one or more evidence shapes;
5. compatibility-named projection mechanics derived only from evidence shape; and
6. access/capture overlay only when the surface proves it.

`forseti-harness/source_capture/source_classification.py` is the executable
registry and inventory. At this revision it contains 42 implemented pairs
discovered from committed runtime declarations and fixtures, plus three
classification-contract inputs for TikTok Shop listing, creator-video, and
review surfaces. Every entry cites its declaring source. Registry construction
rejects duplicate or conflicting keys.

The runtime classification schema is `source_classification_v1`. Version 1 adds
the `reference_record` evidence shape and its
`entity_attribute_snapshot` mechanic. A reference record is a source-visible,
capture-time identity-and-attribute record about an entity. It preserves the
source's labels, values, units, bindings, explicit absences, and capture
context; it does not assert that those attributes are canonical or true.

The `projection_mechanics` field name is retained for compatibility. Its values
are classification labels, not execution ownership. The former shared
Projection Doctrine and persisted Capture Projection layer were retired when
current canonical-content validation and source adaptation moved to Cleaning.
This contract does not recreate a Capture Projection writer, record, or spine.

## Binding Semantics

- Unknown exact pairs are never normalized, prefix-guessed, or silently assigned
  to a broad family. Strict packet classification raises
  `UnknownSourceClassificationError`; generated catalog rows retain the raw pair
  and carry `mapping_status="unknown"` plus `unmapped_legacy_source_pair`.
- Review is an evidence shape, not a venue role. The compatibility pair
  `fragrance_review/rendered_widget_review` therefore does not claim an operator
  or retailer/community role without actual host facts.
- The six Fragrantica, Parfumo, and Basenotes product-page pairs are specialist
  community surfaces with both `reference_record` and `review` evidence. Their
  source-visible product snapshots are not merchant offers, official claims,
  normalized entities, or reconciled product truth.
- Community subtype does not select mechanics. General and specialist community
  evidence with shape `thread` both derive `threaded_chain`.
- TikTok Shop retains `operator_identity="tiktok"` and uses both
  `social_commerce` and `marketplace` venue roles. It is neither flattened to
  ordinary `social_media` nor relabeled as a retailer.
- TikTok Shop shapes are surface-specific: listing is
  `commerce_pdp_offer`, creator video is `social_video`, and review is `review`
  only on the explicit review surface.
- Access modality never stands in for venue identity or evidence shape. Archive,
  supervised-browser, and other overlay-only legacy pairs retain an explicit
  residual when their underlying venue or evidence shape is absent.

The derived view is classification metadata only. It does not migrate Bronze
history, rewrite raw bytes, create a Packing runtime, select evidence, perform
Cleaning, or issue a Judgment/review verdict.

The outer Bronze catalog schema is unchanged. Because the catalog is generated,
`inspect_catalog` recomputes this nested view and reports pre-v1 generated
catalog files as stale until the normal catalog rebuild refreshes them. Raw
packets and their legacy source strings do not change.

## Change Rule

A new committed pair must be added once to the executable registry with its
declaring source and focused tests. If an axis is not derivable from the exact
pair, leave it empty and name the residual. Do not add a taxonomy service,
warehouse table, packet field, or second hand-maintained inventory.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The closed source-classification view now represents specialist fragrance
    product pages truthfully as both reference records and review surfaces.
    source_classification_v1 adds the reference_record evidence shape and
    entity_attribute_snapshot compatibility mechanic without reviving the
    retired Capture Projection layer or moving adaptation out of Cleaning.
  trigger: architecture_doctrine
  controlling_sources_updated:
    - forseti/product/spines/capture/core/source_taxonomy/source_classification_compatibility_contract_v0.md
    - forseti/product/spines/capture/core/source_families/fragrance_native_database/README.md
    - forseti-harness/source_capture/source_classification.py
    - forseti-harness/data_lake/catalog.py
    - forseti-harness/tests/unit/test_source_classification.py
    - forseti-harness/tests/test_data_lake_catalog.py
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - forseti/product/spines/capture/README.md
    - forseti/product/spines/capture/core/source_families/README.md
    - forseti-harness/source_capture/models.py
    - forseti-harness/source_capture/fragrantica_projection.py
    - forseti-harness/source_capture/parfumo_projection.py
    - forseti-harness/source_capture/basenotes_projection.py
    - forseti-harness/data_lake/catalog.py
    - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
    - forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md
    - forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
    - forseti/product/spines/packing/
  intentionally_not_updated:
    - path: AGENTS.md
      reason: No global agent behavior or workflow authority changed.
    - path: .agents/workflow-overlay/
      reason: No source hierarchy, loading, validation, review, or lifecycle rule changed.
    - path: docs/review-inputs/capture_spine_core_migration_adversarial_artifact_review_v0/head_files/orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md.snapshot.txt
      reason: Historical review-input snapshot of the retired Projection Doctrine; never rewritten as live authority.
    - path: forseti-harness/source_capture/models.py
      reason: Packet fields remain unchanged; the classification view is still derived lazily.
    - path: forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
      reason: Existing raw-canonical/re-derived-view layer contract already governs this additive catalog view.
    - path: forseti/product/spines/cleaning/
      reason: >
        Existing family content rows already carry the product snapshot and
        Cleaning already validates/adapts them; classification adds no transform,
        adapter, or Silver field.
    - path: forseti/product/spines/packing/
      reason: No current Packing runtime or contract consumes source_classification, evidence_shapes, or projection_mechanics.
  stale_language_search: >
    rg -n "reference_record|entity_attribute_snapshot|source_classification_v[01]|Projection Doctrine|projection_mechanics"
    forseti-harness/source_capture/source_classification.py
    forseti-harness/data_lake/catalog.py
    forseti-harness/tests/unit/test_source_classification.py
    forseti-harness/tests/test_data_lake_catalog.py
    forseti/product/spines/capture/core/source_taxonomy
    forseti/product/spines/capture/core/source_families/fragrance_native_database
  non_claims:
    - not validation
    - not readiness
```
