# Company Surface To Silver Mapping Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract (Company Surface physical mapping)
scope: >
  Thin mapping from the four accepted Company Surface logical record families
  into producer-owned Silver Vault payloads, plus deterministic non-authoritative
  current, historical-restated, and historical-as-known read models.
use_when:
  - Serializing Company Surface logical records into Silver Vault.
  - Building or reviewing Company Surface temporal views.
  - Checking that Company Surface physicalization preserves Capture and Data Lake ownership.
authority_boundary: retrieval_only
open_next:
  - forseti/product/information/company_surface/company_logical_record_and_view_contract_v0.md
  - forseti/product/information/company_surface/company_identity_boundary_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - forseti-harness/data_lake/company_surface.py
stale_if:
  - The Company Surface logical families, assertion states, or temporal-view semantics change.
  - Silver changes its common envelope, closed record kinds, correction edges, or generated-view manifest contract.
  - Foundation changes Brand, Org, owned_by, or subsidiary_of semantics.
```

## Status And Authority

`COMPANY_SURFACE_SILVER_MAPPING_V0`, owner-authorized 2026-07-15.

This is the physical mapping contract the accepted logical contract deliberately
left as its next decision. It chooses producer-owned payloads over changes to the
generic Silver envelope. Company Surface remains semantic owner, Capture remains
source-observation owner, and Data Lake remains physical authority. Generated
views are rebuildable caches and never a second authority.

## Common Mapping

Every Company Surface logical record becomes one append-only
`silver_vault_record_v0` record in the `company_surface_silver` producer lane.
The existing common header is unchanged:

- `record_kind` remains closed to `entity | relationship | observation`;
- `payload_kind` distinguishes Company Surface payloads;
- `producer_row_kind` preserves the logical record family;
- `raw_refs` preserve packet/source hashes and `derived_refs` preserve record
  lineage;
- effective/observation time remains distinct from `captured_at` and the
  Company Surface `recorded_at`; and
- the existing Silver content hash and validating write front door remain
  mandatory.

Company Surface emits no mutable company row and no new entity record merely to
hold time-varying facts. Brand and Org anchors use the adopted `brand:<slug>` and
`org:<slug>` grammar, but the mapping neither mints nor resolves them.

## Four-Family Mapping

| Logical family | Silver `record_kind` | `payload_kind` | Physical meaning |
| --- | --- | --- | --- |
| Subject assertion | `observation` | `CompanySubjectAssertion` | Time/state/provenance-bearing assertion that a raw identifier concerns one Brand or Org. |
| Relationship assertion | `relationship` | `CompanyRelationshipAssertion` | Evidence-backed `owned_by` or `subsidiary_of` assertion without identity merge. |
| Company-activity link | `relationship` | `CompanyActivityLink` | Link from an upstream observation/receipt to the Brand or Org it concerns. |
| Coverage or failure marker | `observation` | `CompanyCoverageMarker` | Explicit available, partial, failed, excluded, or not-covered posture; never a negative fact. |

The producer payload preserves the logical stable reference, subject anchors,
assertion state where applicable, evidence refs, effective interval and
precision, recorded time, capture posture, limitations, alternatives, and the
family-specific body.

## Correction, Supersession, And Conflict

A logical record that corrects, supersedes, or conflicts with another record
emits a companion append-only Silver `RelationshipEdge` with the existing
`corrects_record`, `supersedes_record`, or `conflicts_with_record` edge type.
The prior record is never rewritten or deleted. A correction or supersession
affects a view only when the edge itself is known by that view's knowledge
cutoff. Conflict stays visible and does not silently choose a winner.

## Temporal Views

Every query supplies an anchor subject, effective boundary, knowledge cutoff,
and one mode:

- `current` — present boundary under the declared current cutoff;
- `historical_restated` — historical boundary under a later cutoff; or
- `historical_as_known` — historical boundary under the historical cutoff.

The selection policy admits only records known by the cutoff and applicable at
the effective boundary. Resolved subject/relationship assertions enter the
resolved roll-up only when their interval is determinate under declared
precision. Provisional, ambiguous, unresolved, or temporally indeterminate
records remain visible residuals. Coverage/failure markers remain visible and
never become zero or a resolved negative.

Each generated view has a manifest containing generation id/time, source record
ids, source high-watermark, selection-policy version, exact query, view hash,
and stale/drift condition. The generation stamp is injectable and recorded so
identical committed inputs plus the same stamp reproduce identical bytes.

## Public Implementation Path

`forseti-harness/data_lake/company_surface.py` is the one public implementation
path for:

1. validating and mapping logical records;
2. translating a validated company-aggregate Capture observation into a
   Company-activity logical record;
3. writing mapped records through `append_silver_record`;
4. reading the producer lane; and
5. rebuilding or proving the three generated view modes.

The bounded Topicals holdout uses that same path. Test fixtures may restate only
the minimum frozen facts and provenance necessary to exercise it.

## Non-Goals

This contract adds no source adapter, live capture, scheduler, matcher,
registry, canonical identity resolver, ECR schema, generalized store, graph or
vector database, SQL surface, UI, API, dashboard, feed, broad corpus, pain
score, recommendation, pitch, contact authority, or intervention.

## Acceptance Conditions

1. All four logical families preserve their signed semantic distinctions.
2. The generic Silver envelope and closed record kinds remain unchanged.
3. Missing/failed coverage cannot become numeric zero or a negative fact.
4. Brand and Org stay distinct and unsupported relations stay visible.
5. Later correction/supersession changes restated history without rewriting
   as-known history.
6. Identical committed inputs and generation stamp reproduce view and manifest bytes.
7. Views expose query boundaries, included records, exclusions, conflicts,
   limitations, source high-watermark, and selection-policy version.
8. The Topicals holdout remains `product_learning` only and enters through the
   same public producer/mapping/view path.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Company Surface gains its first physical mapping: producer-owned payloads
    inside the existing Silver envelope and deterministic manifest-backed read
    models for current, historical-restated, and historical-as-known queries.
  trigger: architecture_doctrine
  controlling_sources_updated:
    - forseti/product/information/company_surface/company_surface_silver_mapping_contract_v0.md
  downstream_surfaces_checked:
    - forseti/product/information/company_surface/README.md
    - forseti/product/information/company_surface/purpose_contract_v0.md
    - forseti/product/information/company_surface/company_identity_boundary_v0.md
    - forseti/product/information/company_surface/company_logical_record_and_view_contract_v0.md
    - forseti/product/spines/foundation/ontology/ontology.yaml
    - forseti/product/spines/foundation/ontology/forseti_ontology_backbone_architecture_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
    - forseti-harness/data_lake/lane_registry.py
  intentionally_not_updated:
    - path: Silver common record contract and validator
      reason: Producer-owned payloads fit the existing envelope and closed record kinds without weakening generic authority.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: The existing Company Surface front door remains the T1 route; a per-contract row would be inventory bloat.
    - path: source adapters, ECR, matcher/registry, API/UI, and broad corpus
      reason: Explicitly outside the owner-authorized vertical slice.
  stale_language_search: >
    rg -n -i "Data Lake representation.*deferred|first physical mapping.*remain|Company Surface runtime.*deferred"
    forseti/product/information/company_surface
  non_claims:
    - not validation or readiness
    - not source completeness or buyer proof
    - not a second authority
    - not identity resolution, source access, GTM, contact, or intervention authorization
```
