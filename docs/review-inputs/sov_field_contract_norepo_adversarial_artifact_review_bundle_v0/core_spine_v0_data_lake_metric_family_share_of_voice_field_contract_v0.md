# Core Spine v0 Data Lake Metric Family Field Contract — Source-Backed Brand/Line Share of Voice (v0)

```yaml
retrieval_header_version: 1
artifact_role: Product architecture decision contract
scope: >
  The field-level posture/reason/coverage contract for the owner-named metric
  family source_backed_brand_line_share_of_voice — the binding the consumption
  seam contract's field-level gate requires before any view of this family may
  be built. Binds readout identity, grouping, numerator/denominator and
  coverage fields, window basis, posture semantics, and the fields that may
  never exist. Field contract only: it authorizes no view build, no capture,
  and no engine.
use_when:
  - Building or reviewing any share-of-voice computation or view over lake evidence.
  - Checking whether a SoV readout's fields are honest (coverage, posture, denominator basis).
  - Deciding whether the family's view-build gate is satisfied.
open_next:
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
stale_if:
  - The Silver Vault metric posture vocabulary or coupling rules change.
  - A Cleaning-owned brand/line canonicalization decision lands (fires the grouping upgrade trigger).
  - A later owner decision renames or retires the family or changes the seam contract's metrics policy.
authority_boundary: retrieval_only
```

## Status

`SOV_FIELD_CONTRACT_RECORDED_V0`. Authored under owner-directed disciplined
continuation (2026-07-02) of the consumption-seam lane, satisfying the seam
contract's field-level gate for `source_backed_brand_line_share_of_voice`
(family owner-named 2026-07-02, PR #580). Not validation, readiness, view-build
execution, capture authorization, or engine selection. The sibling family
`movement_threshold_crossings` remains gate-blocked (its field contract is a
separate decision).

## Decision In One Screen

```text
A share-of-voice readout is honest only if it says: over WHICH captured
evidence (platform, cohort, window, coverage counts), grouped by WHAT
(exact brand/line strings, fragmentation disclosed), out of WHAT denominator
(captured source-backed mentions only), with missing evidence as posture +
reason — never a zero, never a market-total implication, never cross-platform.
Every number must recompute from committed records cited by ref.
```

## Readout Identity Fields (required on every readout)

| Field | Semantics |
| --- | --- |
| `metric_family` | Literal `source_backed_brand_line_share_of_voice`. |
| `family_schema_version` | This contract's field-schema version (`1` for v0); any field change bumps it. |
| `platform` | Exactly one platform (`instagram` / `youtube` / `tiktok` / …). Per-platform only — a readout spanning platforms is forbidden (medallion cross-platform identity limitation). |
| `cohort` | Declared, never inferred: `{cohort_id, definition, member_basis: "captured_set", member_count}`. The definition states how members were selected; `member_basis` is always the captured set — cohort membership claims about uncaptured creators are unrepresentable. |
| `coverage_window` | `{start, end, window_basis}` with `window_basis: capture_time \| source_publication_time`. `capture_time` is universally available (every packet records it). `source_publication_time` is surface-dependent: records lacking publication evidence in the window scope must be surfaced under `coverage.publication_time_missing` (posture, not silent exclusion). |
| `selection_policy_versions` | Must include: extractor rubric version(s) of the consumed mention records, `silver_lineage_gate` (source-backed-complete), `family_schema_version`, and `brand_grouping` (see Grouping). |

## Grouping Fields

- `grouping_basis: "exact_string_v0"` — brand/line group keys are the exact
  strings from committed mention records. The lake never normalizes
  (storage-contract no-cleaning rule); no Cleaning-owned brand/line
  canonicalization exists today (verified 2026-07-02).
- `fragmentation_note` — required non-empty field stating that case/spelling
  variants of one real-world brand appear as separate rows until a
  Cleaning-owned canonicalization is adopted.
- Upgrade trigger: a Cleaning-owned canonicalization decision lands → readouts
  may group on it ONLY by citing its version in
  `selection_policy_versions.brand_grouping`; uncited normalization is a
  contract violation.
- Group keys: `{brand, line}`. `brand` may be the extractor's literal
  `"unknown"` — reported as its own row, never merged or dropped.

## Numerator / Denominator / Share Fields

- `mention_count` (numerator, per `{brand, line}` row): count of mentions in
  source-backed-complete `silver__cleaning__product_mentions` records within
  scope. Each row must carry `mention_refs`: dereferenceable committed-record
  refs (`raw_anchor`, `lane`, `record_id`, `sha256`) — every bar clicks back to
  transcript evidence.
- `denominator`: total mentions across all rows in the same scope, with
  mandatory `denominator_basis: "captured_source_backed_mentions_only"`. No
  field may ever represent a market total, uncaptured population, or
  extrapolated reach — such fields are unrepresentable in this family, not
  optional.
- `share`: derived (`mention_count / denominator`), and must recompute exactly
  from the row's own numerator and the readout's denominator — a stored share
  that cannot be recomputed from cited refs fails the family's
  rebuildability/honesty check.
- **Zero semantics:** `share: 0` (equivalently `mention_count: 0`) is valid
  ONLY as a real observed zero — the scope has a non-empty source-backed
  denominator and this brand/line genuinely has no mentions in it. An empty
  scope is a posture, never a zero (below).

## Coverage Fields (required block; prevents thin-scope readouts)

`coverage`: `{packets_in_scope, packets_with_transcripts,
mention_records_in_scope, mention_records_excluded_not_source_backed,
publication_time_missing (when window_basis is source_publication_time)}` —
the counts a reader needs to judge how much captured evidence stands behind
the shares. Excluded non-source-backed records are counted residuals (seam
contract lineage gate), never silently dropped and never evidence.

## Posture Semantics

- Posture vocabulary binds to the Silver Vault closed set
  (`observed` / `unavailable_with_reason` / `not_attempted`) with the
  contract's value/reason coupling: a non-observed posture carries a reason
  and NO numeric value.
- Readout-level posture: a scope with `denominator = 0` (no source-backed
  mentions at all) yields `readout_posture: unavailable_with_reason` (e.g.
  `no_source_backed_mentions_in_scope`) and NO share rows — never a table of
  zeros.
- Any per-object metric embedded in a SoV readout (e.g. observed view counts
  accompanying a mention ref) carries its own `MetricObservation` posture
  unchanged — a SoV view never launders a non-observed metric into a number.

## Forbidden Fields (unrepresentable, not just discouraged)

Cross-platform aggregation or identity fields; market-total / total-reach /
"social share of market" denominators; ROI, sales-lift, or EMV fields;
person-level or dossier fields; any share computed over records failing the
lineage gate. A view schema containing any of these fails this contract.

## View-Build Gate Disposition

This artifact satisfies the seam contract's field-level gate for
`source_backed_brand_line_share_of_voice`. A SoV view build is now
gate-unblocked but remains a separate bounded work unit under the seam
contract's rules: rebuildable manifest-backed cache under
`indexes/derived_retrieval/`, on-demand-first posture, prove-rebuildability
compliant, and never authoritative. `movement_threshold_crossings` remains
gate-blocked.

## Non-Claims

Not validation, readiness, acceptance, view-build execution, engine/backend
selection, capture authorization, cohort selection, or brand canonicalization.
Records the field-level contract only.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Field-level contract recorded for the owner-named metric family
    source_backed_brand_line_share_of_voice: readout identity (family/version/
    platform/declared-cohort/coverage-window with capture_time-vs-publication
    window basis), exact-string grouping with mandatory fragmentation
    disclosure and a Cleaning-canonicalization upgrade trigger, dereferenceable
    mention refs, captured-evidence-only denominator with recomputable share,
    observed-zero-only zero semantics, required coverage block, Silver Vault
    posture binding with readout-level unavailable_with_reason for empty
    scopes, and an unrepresentable-fields list (cross-platform, market-total,
    ROI/EMV, dossier). Satisfies the seam contract's field-level gate for this
    family; movement_threshold_crossings stays gate-blocked.
  trigger: architecture_doctrine
  controlling_sources_updated:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
  downstream_surfaces_checked:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
    - orca-harness/data_lake/derived_retrieval_views.py
  intentionally_not_updated:
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
      reason: >
        Its MetricObservation posture vocabulary and read-model manifest rules
        are consumed as-is; this family contract binds to them by reference.
    - path: orca-harness/data_lake/derived_retrieval_views.py
      reason: >
        No SoV view exists yet; the view build is a separate bounded work unit
        now unblocked by this gate disposition.
  non_claims:
    - not validation or readiness
    - not view-build execution
    - not brand canonicalization or cohort selection
```
