# Core Spine v0 Data Lake Bronze MGT Baseline Declaration v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture declaration
scope: >
  Declares the post-PR-525 Bronze lake baseline as Mini God Tier / 90-95
  typed raw-truth retrievability, while explicitly refusing a full God Tier
  claim.
use_when:
  - Deciding whether downstream Silver lanes may consume the current Bronze catalog and Attachment Record surfaces.
  - Checking whether Bronze may be described as full God Tier.
  - Planning the next Bronze/Silver convergence unit after PR #525.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_mini_god_tier_doctrine_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - orca-harness/data_lake/catalog.py
stale_if:
  - Bronze catalog schema or Attachment Record physicalization changes.
  - Manifest v2, sidecar/member body layout, backend/engine selection, or migration/replay mechanics are accepted.
  - A later owner decision declares full Bronze God Tier or supersedes this baseline.
```

## Status

`BRONZE_MGT_BASELINE_RECORDED_V0`.

Bronze is declared Mini God Tier / 90-95 for the current typed raw-truth
retrievability slice. It is not declared full God Tier.

As of PR #525, this declaration includes the runner-enforcement pass that made
current lake-writing runners point at the Bronze seam contract or carry explicit
classification as a non-raw-packet/manual-orchestrator residual. The baseline
marker remains `bronze_mgt_baseline_recorded_v0`; the post-PR-525 change
reaffirms the declaration rather than minting a new runtime status enum.

This declaration is architecture and routing doctrine. It is not validation,
readiness, proof, implementation authorization, storage-engine selection,
Manifest v2 selection, migration authorization, or a claim that every future
source family has exercised the shape.

## What The Baseline Means

The current Bronze baseline means:

1. Raw packet manifests and preserved bytes remain authoritative.
2. The Bronze catalog is generated, rebuildable read state under
   `indexes/derived_retrieval/bronze_catalog/v0`, not authority.
3. Attachment Record entries are typed, stable, generated entries over
   preserved raw packet bodies.
4. Attachment Record bodies are resolved through raw packet references and
   hash verification, not copied into a second body store.
5. Source surfaces are discoverable by observed `(source_family,
   source_surface)` buckets with explicit non-completeness semantics.
6. Downstream lanes have a public query surface for source-surface packet rows
   and Attachment Record rows, so they do not need private safe-name or layout
   guesses.
7. Future source families can appear with universal packet/source facets before
   a source-specific extractor exists.

This is enough for Silver convergence work to depend on Bronze by contract,
as long as Silver consumes the public Bronze helpers and treats the catalog as
generated read state.

## Why This Is Not Full God Tier

Full God Tier is intentionally not claimed because material residuals remain:

| Residual | Why accepted now | Upgrade trigger |
| --- | --- | --- |
| No Manifest v2 selection | The current catalog physicalizes manifest-equivalent entries without forcing a packet-format migration. | Accepted Manifest v2 or equivalent packet-index serialization decision. |
| No copied Attachment Record body store | Bodies remain preserved raw packet members, which preserves raw authority and avoids a second source of truth. | A storage lane selects sidecar/member/body-store layout with hash-checked immutability. |
| No final backend/engine selection | The storage contract allows later bounded engine selection but does not choose one here. | A physicalization lane selects and tests the backend while preserving lake invariants. |
| No incumbent-field migration/replay | Historical direct fields remain legacy-readable and transitional. | A separately authorized dual-read or replay lane closes migration mechanics. |
| No full source-family semantic registry | Bronze records generic payload kind and universal facets; source-specific semantic extractors remain opt-in. | Multiple source families need a shared registry and the lake-core-field promotion rule is satisfied. |
| No derived-result physical home closeout | Bronze raw retrievability is stronger than before, but downstream derived-store and acknowledgement physical homes remain separately governed. | The derived layout/index rebuild and write-boundary lanes close with code/tests. |
| No live-lake coverage proof for every lane | Tests cover generic future surfaces, current IG/Reddit fixtures, and current runner seam coverage, but not every active/future capture family. | Each lake-interacting lane rebases to this baseline and proves its own consumption path. |

These residuals are accepted under the Mini God Tier doctrine because the
baseline captures most of the immediate value: typed discoverability,
hash-checkable replay, source-surface coordination, and future-family
adaptability without taking on the lock-in of full storage migration.

## Full God Tier Upgrade Path And Worth

Full Bronze God Tier is not a Silver prerequisite. Silver should now consume the
public Bronze catalog and Attachment Record surfaces; that consumer pressure is
the right way to expose which Bronze residuals are actually expensive.

To upgrade Bronze from MGT to full GT, the remaining material work is:

1. Replace manual runner/orchestrator enumeration with a deterministic discovery
   gate for all raw-packet writers and all explicitly non-raw-packet lake
   touchpoints.
2. Select Manifest v2 or an equivalent packet-index serialization and migration
   path, including dual-read/replay rules for legacy packet material.
3. Select the final Attachment Record body layout or backend posture, including
   immutable hash verification, retention/lawful-erasure posture, and migration
   mechanics.
4. Promote the catalog/availability/index rebuild checks into a lake-doctor or
   CI-owned gate over representative fixture lakes and real lane fixtures.
5. Prove at least one Silver producer consumes Bronze by catalog/AR helper, not
   raw folder semantics, and carries verified refs into Silver `raw_refs`.
6. Repeat that consumer proof across enough source families to validate the
   generic model without promoting source-family fields into lake core.
7. Run de-correlated review on the full Bronze/Silver contract and code path
   before any full GT claim.

The long-term answer is yes, full GT is likely worth it once scale, query
latency, compliance posture, or external reliability promises make the residuals
operationally expensive. It is not worth paying the full cost before Silver
convergence because MGT deliberately avoided irreversible layout/backend choices;
switching later should mostly cost migration/replay and stricter discovery
coverage, not a semantic rewrite, if downstream lanes honor the public Bronze
surfaces now.

## Silver Consumption Boundary

Silver may consume Bronze through:

- generated catalog inspection status;
- `source_surface_catalog_rows`;
- Attachment Record rows and `load_attachment_record_body`;
- stable query paths surfaced by catalog manifests and source-surface rows.

Silver must not:

- infer full Bronze GT from this declaration;
- reimplement private catalog safe-name rules when a public helper exists;
- treat generated catalog files as authority over raw;
- mutate raw packet material, preserved bodies, or Attachment Record rows;
- promote a Silver consumer finding into a Bronze declaration without a Bronze
  authority update.

If a Silver lane finds a missing Bronze invariant, the result is a Bronze
follow-up, not a Silver-owned Bronze GT declaration.

## Code Enforcement Binding

The generated Bronze catalog surfaces expose
`bronze_baseline_status = "bronze_mgt_baseline_recorded_v0"` plus semantics
that explicitly say "not full God Tier." The field is intentionally additive
and non-authoritative; it makes the baseline visible to downstream readers and
tests.

The enforcement target is narrow:

- catalog rebuild/inspect/census reports carry the baseline marker;
- generated catalog/source-surface/Attachment-Record manifests carry the marker;
- tests assert the marker and the non-GT semantics.

This does not validate the lake, prove full coverage, or close any residual in
the table above.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Data Lake Bronze now has an explicit post-PR-525 Mini God Tier / 90-95
    baseline declaration for typed raw-truth retrievability: Silver may consume
    the public Bronze catalog and Attachment Record surfaces after runner-seam
    enforcement, but Bronze is not full God Tier and keeps named residuals for
    Manifest v2, body-store layout, backend/engine selection, incumbent-field
    migration/replay, source-family semantic registry, derived-result physical
    home, deterministic all-runner discovery, and all-lane live coverage.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
    - validation_philosophy
  controlling_sources_updated:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
    - orca/product/spines/data_lake/README.md
    - docs/workflows/orca_repo_map_v0.md
    - orca-harness/data_lake/catalog.py
    - orca-harness/tests/test_data_lake_catalog.py
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/decisions/orca_mini_god_tier_doctrine_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        The root kernel already binds Mini God Tier vocabulary to the MGT
        doctrine and routes Orca project facts to the overlay; this is a
        data_lake-spine baseline, not a new global agent trigger.
    - path: .agents/workflow-overlay/README.md
      reason: >
        No overlay section owner changes. The Data Lake spine and repo map carry
        the new route.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Source-loading rules do not enumerate each data_lake baseline; the repo
        map and Data Lake README route future agents to this declaration.
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
      reason: >
        The medallion contract already defines Bronze as raw packet and
        source-visible attachment material. This declaration does not change
        layer semantics; it records the current capability baseline.
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
      reason: >
        The storage contract remains the owner of backend/engine, Manifest v2,
        sidecar/member, migration, and derived-record physical-home blockers.
        This declaration names those residuals without settling them.
  stale_language_search: >
    rg -n "Bronze.*God Tier|full God Tier|BRONZE_MGT_BASELINE|bronze_mgt_baseline|AR-MGT-90"
    AGENTS.md .agents docs/workflows/orca_repo_map_v0.md docs/decisions/orca_mini_god_tier_doctrine_v0.md
    orca/product/spines/data_lake orca-harness/data_lake orca-harness/tests/test_data_lake_catalog.py
  non_claims:
    - not validation
    - not readiness
    - not proof
    - not full God Tier
    - not implementation authorization
    - not Manifest v2 selection
    - not body-store layout selection
    - not backend or engine selection
```

Older receipts are archived in `docs/decisions/dcp_receipts_archive_v0.md`.
