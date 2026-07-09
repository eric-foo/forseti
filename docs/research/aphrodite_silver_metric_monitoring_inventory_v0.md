# Aphrodite Silver Metric Monitoring Inventory v0

```yaml
retrieval_header_version: 1
artifact_role: >
  Retrieval-only inventory for Aphrodite/Forseti capture surfaces and metric
  families. Documentation lane only; not implementation, capture authorization,
  lake-write authorization, validation, readiness, buyer proof, or product authority.
scope: >
  Point-in-time source-backed inventory of what Forseti can capture, what committed
  artifacts show has already been captured, what metric families are current,
  deferred, proposed, or forbidden, and which Aphrodite monitoring recipes must
  not be invented inside a product surface.
use_when:
  - Checking which source surfaces already have a Capture or Scanning route.
  - Distinguishing capturable route posture from committed captured evidence.
  - Deciding whether a metric family is current, deferred, proposed, or forbidden.
  - Scoping Aphrodite monitoring without fabricating moving averages, velocity,
    spike, breakout, decay, audience/person, or buyer-proof claims.
authority_boundary: retrieval_only
source_context_status: SOURCE_CONTEXT_READY_PATCH_LEVEL
source_pack: whole_repo_custom_capture_metric_inventory
open_next:
  - docs/workflows/forseti_repo_map_v0.md
  - forseti/product/spines/capture/core/source_families/README.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md
  - forseti/product/spines/creator_signal/creator_signal_product_architecture_v0.md
branch_or_commit: >
  Inventoried on branch codex/aphrodite-creator-capture-strategy @ 055ff9de.
  Recheck if source-family catalogs, committed snapshots, metric producers,
  data-lake metric-family code, or Creator Signal contracts change.
stale_if:
  - Capture or Scanning source-family catalogs change.
  - Creator metric Silver producers, snapshots, validation, or profile-current
    materialization change.
  - Share-of-voice readout code, movement-threshold contracts, or metric-family
    gates change.
  - Any monitoring recipe named here lands with a recipe/version/runner.
external_source_boundary: >
  External workflow source and unrelated project trees are not Forseti authority.
  Paths in this record use only forseti/ and forseti-harness/ repository roots.
```

## Status

`PROPOSED_DOCS_INVENTORY_V1`.

This is a retrieval-only inventory. It does not validate a product, authorize
capture, mutate the lake, create metric records, prove request-budget feasibility,
or authorize a customer-facing claim.

`SOURCE_CONTEXT_READY_PATCH_LEVEL`: loaded sources covered the Forseti repo map,
capture source-family catalog, scanning source-family docs, creator registry and
profile-current artifacts, Silver/Vault authority, Data Lake metric-family
contracts, share-of-voice implementation, committed creator metric snapshots,
committed product-learning capture receipts, and creator-metric producer/runner
code. Residual risk: two broad read-only survey lanes timed out, so treat this as
a strong patch-level inventory rather than a permanent no-omissions claim.

## Boundary Problem

A complete inventory here must keep two things separate:

1. **Capture surfaces:** what Forseti can route, and what committed artifacts show
   has already been captured.
2. **Metric families:** calculations/readouts Forseti can calculate, precompute,
   materialize, or must forbid, with status, posture, lineage, sample/history
   requirements, and source cites.

Failure modes this record attacks: omitting non-creator surfaces, calling a route
"captured" without committed evidence, treating `not_attempted` as implemented,
asserting absence without point-in-time cites, zero-filling hidden/missing values,
and making Aphrodite the metric authority.

Decision criteria: `current` means committed contract/code/artifact exists;
`deferred` means named or schema-reserved but currently non-observed; `proposed`
means desired or source-classed without an implemented metric/readout; `forbidden`
means current authority says the field/claim/output must not exist.

## Reading Rule: Posture And Value

Every metric inherits Silver posture/value coupling:

```text
observed     => numeric value, no reason
non-observed => null value, explicit reason
```

Zero is valid only as a real observed zero from a source-backed record. Missing,
hidden, blocked, out-of-window, not-applicable, and not-attempted are never zero
and must not be ranked, averaged, or displayed as low performance. Authority:
`forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md:322-365`,
`forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md:442-456`,
`forseti-harness/capture_spine/creator_profile_current/validation.py:452-475`.

## Capture Surface Inventory

| Surface / family | Capturable route | Already captured / committed evidence | Metric posture | Status | Cites |
| --- | --- | --- | --- | --- | --- |
| Fragrance native database: Fragrantica, Parfumo, Basenotes | Targeted current-window source-native capture, projection, and Cleaning/Silver seams. | Route contracts exist; this pass did not verify a complete committed corpus. | No creator metric family; source-visible review/community text can feed downstream Cleaning/Silver only under its lane. | current route; captured corpus unknown | `forseti/product/spines/capture/core/source_families/README.md:51`; `forseti/product/spines/capture/core/source_families/fragrance_native_database/README.md:42-46`; `forseti/product/spines/capture/core/source_families/fragrance_native_database/README.md:48-58` |
| Retail/PDP purchase-review storefronts | Rendered/embedded-state Retail/PDP packets and projections over product, offer, review-substrate, embedded JSON, and module rows. | Committed product-learning case receipts preserve archived storefront/PDP snapshots. | No price truth, demand proof, ECR/Judgment, or full review corpus by default. | current route; committed archive packets exist | `forseti/product/spines/capture/core/source_families/README.md:52`; `forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_playbook_v0.md:75-116`; `forseti-harness/cases/product_learning/cocokind_holdprice_2025_v0/source_captures/e10_chagaglo_highlighter/receipt.md:3-44` |
| Vendor pricing page | Narrow SPA/JS-payload route for public vendor pricing pages. | Route/runner contract exists; no committed vendor-pricing packet was verified in this pass. | No universal price checker, standing scheduler, rendered retail price truth, or Judgment. | current route; captured material unknown | `forseti/product/spines/capture/core/source_families/README.md:53`; `forseti/product/spines/capture/core/source_families/vendor_pricing_page/README.md:27-36`; `forseti/product/spines/capture/core/source_families/vendor_pricing_page/README.md:58-63` |
| Instagram public creator/reels | Grid/creator packet routes, deep capture/transcript routes, audience post-text seam, product-extraction handoff. | Committed IG creator metric seed/snapshot files exist; profile-current joins IG metric rows. | Current creator metrics for view/like/comment and engagement rollups; product mentions are downstream Cleaning/Silver. | current | `forseti/product/spines/capture/core/source_families/README.md:54`; `forseti/product/spines/capture/core/source_families/social_media/instagram/README.md:35-40`; `forseti/product/spines/capture/core/source_families/social_media/instagram/instagram_reels_creator_metric_rollup_snapshot_v0.json:3-9` |
| TikTok public/sessioned creator capture | Sessioned/live staging, raw packet admission, coverage/projection, and source-specific batch evidence. | Funmi N30 source-family evidence exists; current creator registry rows are identity/profile-only and no TikTok metric rollup is admitted in profile-current. | TikTok metric seed code exists in harness; committed profile-current TikTok rollups were not found. | current route; profile metric captured-current absent | `forseti/product/spines/capture/core/source_families/README.md:55`; `forseti/product/spines/capture/core/source_families/social_media/tiktok/README.md:37-54`; `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_v0.json:1333-1338` |
| YouTube public watch/Shorts/transcript | Watch metadata/comments packets, captions/ASR packets, creator observations, metric rollups, audience post-text, transcript product extraction. | Committed YouTube metric seed/snapshot files exist; profile-current joins YouTube metric rollups and source drill-back pointers. | Current creator metrics for view-only genesis and watch-packet engagement; transcript/product mentions can feed Cleaning/Silver and SoV when source-backed. | current | `forseti/product/spines/capture/core/source_families/README.md:56`; `forseti/product/spines/capture/core/source_families/social_media/youtube/README.md:34-42`; `forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json:3-9`; `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json:180-205` |
| Reddit bounded candidate/intake/capture | Candidate URL intake, graph/frontier selection, exact old Reddit thread capture, consolidation, archive fallback, one-URL browser fallback when needed. | Route and runner boundaries exist; no current committed Reddit packet corpus was verified in this pass. | Not source-wide monitoring or metrics; candidate rows do not auto-promote to capture. | current route; captured corpus unknown | `forseti/product/spines/capture/core/source_families/README.md:57`; `forseti/product/spines/capture/core/source_families/social_media/reddit/README.md:26-35`; `forseti/product/spines/capture/core/source_families/social_media/reddit/README.md:50-57` |
| Creator registry / public-handle linkage | Static known-account dedupe, linkage ledger, and profile-current materializer; not source access. | Registry/profile-current has 36 profiles, 33 with metric rollups, 31 with observed engagement_rate. | Current read model copies accepted platform-account rollups and freshness/source pointers; no cross-platform creator rollup. | current | `forseti/product/spines/capture/core/source_families/README.md:58`; `forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md:41-50`; `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json:14-22` |
| Cross-archive historical capture | Cross-source archive/history packet route, not a source-family identity. | At least 88 committed product-learning source-capture receipts exist under case folders; examples preserve archive availability metadata and snapshot bodies. | Captured facts only; not archive completeness, source-state truth, Cleaning, Judgment, or buyer proof. | current route; committed packets exist | `forseti/product/spines/capture/core/source_families/README.md:59`; `forseti-harness/cases/product_learning/beautypie_repricing_2023_v0/source_captures/e1_homepage_20230225/receipt.md:3-44`; `forseti-harness/cases/product_learning/beautypie_repricing_2023_v0/source_captures/e1_homepage_20230225/receipt.md:54-68` |
| LinkedIn scanning lane | Bounded discovery/candidate-frontier lane; downstream capture/outreach are separate authorization gates. Harness has no-live adapter/runtime gates and attended live-run skeletons behind explicit owner authorization. | Built harness slices exist, but the lane index says no-live planning discovery by default. | Visible influence/trajectory may corroborate a public-actor basis, never replace it; no follower/connection graph, contact harvesting, profile body, or content capture. | current scanning lane; live capture gated; watch deferred | `docs/workflows/forseti_repo_map_v0.md:67`; `forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_lane_index_v0.md:21-36`; `forseti-harness/capture_spine/linkedin_live_runtime/runtime.py:1-18`; `forseti-harness/capture_spine/linkedin_live_runtime/runtime.py:79-89` |
| Search-interest / answer-engine visibility | Proposed source-class/gate-read delta. Search-interest can become observation only under approved source placement; AEO needs schema amendment and routes to Capture only as a capture request. | No committed AEO historical corpus or gate-recordable AEO schema was found in loaded evidence. | Search-interest is attention-only; AEO is non-origin visibility corroboration, not demand proof or query-volume truth. | proposed | `forseti/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md:5-17`; `forseti/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md:173-190`; `forseti/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md:286-301` |

## Current Creator Metric Families

The current creator-metric family is account/platform-scoped. It emits
`MetricObservation` and `MetricRollupObservation` records with lineage, raw/derived
refs, posture/value coupling, sample support, freshness, limitations, and named
`calculation_recipe_version` values (`forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md:40-50`,
`forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md:71-88`).

| Surface | Current source metrics | Current rollups | Required support | Recipe/version and lineage owner | Status |
| --- | --- | --- | --- | --- | --- |
| Instagram reels-grid | Per-content `view_count`, `like_count`, `comment_count`; profile `follower_count` is observation-only and excluded from rollup math. | `average_views`, `median_views`, `engagement_rate`, `average_like_count`, `average_comment_count`; cadence/velocity `not_attempted`. | Admitted/selected grid pool; visible sample support. | `creator_metric_rollup_instagram_reels_grid_engagement_v0`; harness seed and Silver wrapper. | current (`forseti-harness/capture_spine/creator_profile_current/instagram_metric_seed.py:26-30`; `forseti-harness/capture_spine/creator_profile_current/instagram_metric_seed.py:397-415`; `forseti-harness/capture_spine/creator_profile_current/instagram_metric_seed.py:524-544`) |
| YouTube Shorts genesis seed | Per-Short `view_count` only from checked-in source artifacts. | `average_views`, `median_views`; like/comment/engagement unavailable; cadence/velocity `not_attempted`. | Admitted source pool; thin rows must be presentation-downgraded. | `creator_metric_rollup_admitted_youtube_shorts_average_v0`; static product artifact over checked-in records. | current view-only (`forseti-harness/capture_spine/creator_profile_current/youtube_metric_seed.py:15`; `forseti-harness/capture_spine/creator_profile_current/youtube_metric_seed.py:157-176`; `forseti-harness/capture_spine/creator_profile_current/youtube_metric_seed.py:615-634`) |
| YouTube watch-packet | Per-video `view_count`, `like_count`, `total_comment_count` where observed. | `average_views`, `median_views`, optional like/comment averages, `engagement_rate` over complete triples; cadence/velocity `not_attempted`. | Admitted videos with observed inputs; engagement uses complete view/like/comment triples only. | `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0`; watch-packet metric document and YouTube Silver producer. | current (`forseti-harness/capture_spine/creator_profile_current/youtube_watch_packet_metric_document.py:19-29`; `forseti-harness/capture_spine/creator_profile_current/youtube_watch_packet_metric_document.py:76-83`; `forseti-harness/capture_spine/creator_profile_current/youtube_watch_packet_metric_document.py:623-648`) |
| TikTok batch | Harness maps `playCount`, `diggCount`, `commentCount`, `shareCount`, `collectCount` to observations; only view/like/comment are engagement inputs. | `average_views`, `median_views`, `engagement_rate`, like/comment averages; cadence/velocity `not_attempted`. | Complete triples for engagement. Current profile-current rows stay identity-only unless a rollup is admitted. | `creator_metric_rollup_tiktok_profile_grid_engagement_v0`; TikTok seed/Silver producer code. | current in harness; not current in committed profile-current view (`forseti-harness/capture_spine/creator_profile_current/tiktok_metric_seed.py:10-13`; `forseti-harness/capture_spine/creator_profile_current/tiktok_metric_seed.py:47-86`; `forseti-harness/capture_spine/creator_profile_current/tiktok_metric_seed.py:612-635`; `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_v0.json:1333-1338`) |

Allowed rollup keys are fixed in validation: `average_views`, `median_views`,
`engagement_rate`, `average_like_count`, `average_comment_count`,
`posting_cadence`, `recent_velocity` (`forseti-harness/capture_spine/creator_profile_current/validation.py:112-121`).
`sample_support.observation_count` must match `observation_count`
(`forseti-harness/capture_spine/creator_profile_current/validation.py:493-502`).

## Deferred Creator Metric Fields

| Metric | Current posture | Required support before first observed value | Owner/lineage | Status |
| --- | --- | --- | --- | --- |
| `posting_cadence` | Present in rollup schema, emitted as `not_attempted`. | Source-backed content records/history, source publication timestamps or explicit cadence basis, declared window, named recipe version, source ids, and posture/value coupling. Capture timing cannot be smuggled in as posting behavior. | Creator profile-current contract and future Silver recipe. | deferred (`forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md:302-336`; `forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py:65-70`) |
| `recent_velocity` | Present in rollup schema, emitted as `not_attempted`. | At least two compatible Silver rollups for the same subject/scope/window, observed base metric in both, positive elapsed time, and source record ids. | Creator profile-current contract and future Silver recipe. | deferred (`forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md:338-388`; `forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py:65-70`) |

`rollup_formula_revalidation.py` independently restates known recipes, fails unknown
recipe versions, and lists `posting_cadence` and `recent_velocity` under
`_NEVER_COMPUTED_METRICS` (`forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py:29-39`,
`forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py:65-70`,
`forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py:207-221`).

## Data Lake Metric Families

| Metric family / readout | What it can calculate or precompute | Posture and missingness | Required support | Lineage owner | Status |
| --- | --- | --- | --- | --- | --- |
| Creator source metric rollups | Platform/account pool statistics and engagement rates for named recipes. | Missing is null+reason; read model copies latest accepted rollup and does not compute global stats. | Admitted observations, sample_support, recipe version, source ids, raw/derived refs. | Creator metric Silver contract, producer code, profile-current materializer. | current (`forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md:107-126`; `forseti-harness/capture_spine/creator_profile_current/materialize.py:21-45`; `forseti-harness/capture_spine/creator_profile_current/materialize.py:220-248`) |
| Creator-profile-current view | Static profile export joining public account identity, metric rollups, source drill-back, and freshness pointers. | Not source of truth for identity/metrics/audience inference; no cross-platform rollup without promoted linkage. | Current sibling ledgers/snapshots; profile rows preserve pointers/freshness. | Creator registry/profile-current specs and materializer. | current (`forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md:7-11`; `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md:182-190`; `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json:14-22`) |
| Source-backed brand/line share of voice | Computes `source_backed_brand_line_share_of_voice` on demand from committed `silver__cleaning__product_mentions`; can optionally materialize a rebuildable, manifest-backed, non-authoritative cache. | Denominator is captured source-backed mentions only; empty scope is unavailable-with-reason; zero rows require declared comparison set. No market-total or cross-platform implication. | Source-backed complete mention records, per-mention refs, declared platform/cohort/window, window basis, comparison-set policy if zeros are emitted. | Data Lake SoV field contract and `sov_readout.py`. | current implementation, bounded readout (`forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md:41-48`; `forseti-harness/data_lake/sov_readout.py:1-35`; `forseti-harness/data_lake/sov_readout.py:421-461`; `forseti-harness/runners/run_data_lake_sov_readout.py:1-17`) |
| Movement threshold crossings | Pre-gold `SourceObjectMovementThresholdCrossingRecord` vocabulary for a source object crossing a declared profile/baseline/window/cohort/threshold. | Means only "usual-range threshold crossed"; no actor/person implication and no viral/suspicious/bot/fake/paid language. | Declared baseline/window/cohort/threshold profile; currently parked/gate-blocked. | Data Lake physicality and Gold-readiness contracts. | deferred/gate-blocked (`forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md:234-251`; `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md:174-185`; `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md:324-326`) |
| AEO/search-interest visibility | Search-interest can be a scoped attention-only read; AEO can be a visibility annotation/capture request after schema amendment. | AEO `not_shown` is an observation state, not absence of demand; AEO has no query-volume truth and is not gate-recordable today. | Owner-approved source placement, source pins, scan-schema amendment for AEO, source-specific capture minimums. | Scanning answer-engine spec and consumed search-interest capture profile. | proposed (`forseti/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md:146-179`; `forseti/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md:189-214`; `forseti/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md:286-301`) |

## Aphrodite Monitoring Recipes: Implemented Versus Absent

Current creator metric code implements pool means/medians and complete-input
engagement rates. It does not implement longitudinal monitoring recipes. Each
absence claim below is point-in-time at `055ff9de`.

| Recipe | Required support | Point-in-time verdict | Status |
| --- | --- | --- | --- |
| Simple moving average over time | Compatible rollup series and declared time window. | No implemented SMA recipe found in creator-metric producers. Existing `average_*` values are plain admitted-pool means. | proposed (`forseti-harness/capture_spine/creator_profile_current/instagram_metric_seed.py:399-407`; `forseti-harness/capture_spine/creator_profile_current/youtube_watch_packet_metric_document.py:623-643`; `forseti-harness/capture_spine/creator_profile_current/tiktok_metric_seed.py:612-623`) |
| Exponential moving average | Compatible rollup series, smoothing factor, named recipe version. | No EMA recipe/version/runner was found in loaded harness evidence. | proposed (`forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py:207-221`) |
| Compatible-window velocity | At least two compatible Silver rollups, positive elapsed time, observed base values. | Reserved as `recent_velocity`, but every current creator metric producer emits `not_attempted`, and revalidation marks it never-computed. | deferred (`forseti-harness/capture_spine/creator_profile_current/instagram_metric_seed.py:408-409`; `forseti-harness/capture_spine/creator_profile_current/youtube_metric_seed.py:627-628`; `forseti-harness/capture_spine/creator_profile_current/youtube_watch_packet_metric_document.py:644-648`; `forseti-harness/capture_spine/creator_profile_current/tiktok_metric_seed.py:624-628`) |
| Capture-window delta | At least two comparable captures and explicit capture-window labeling. | No cross-capture delta recipe found; snapshot/freshness machinery compares latest snapshots for staleness, not magnitude deltas. | proposed (`forseti-harness/capture_spine/creator_profile_current/live_lake_freshness_gate.py:1-23`; `forseti-harness/capture_spine/creator_profile_current/live_lake_freshness_gate.py:72-105`) |
| Spike / breakout | Baseline/profile/window/cohort/threshold plus source-backed recent value. | No creator-metric spike/breakout recipe found. Data Lake movement-threshold vocabulary is parked/gate-blocked and cannot be relabeled as implemented Aphrodite breakout. | proposed/deferred (`forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md:174-185`; `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md:113-119`; `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md:243-251`) |
| Decay / plateau | Repeated observations and declared slope/plateau profile. | No creator-metric decay/plateau recipe found in loaded harness evidence. | proposed (`forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py:207-221`) |
| Active-watch expiry | Explicit watch window, source-backed recheck cadence, self-expiring state. | LinkedIn has a deferred bounded-watch spec; creator metrics do not have an active-watch expiry state machine. | proposed/deferred (`forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_influence_trajectory_watch_spec_v0.md:72-90`; `forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py:207-221`) |

## Freshness, Revalidation, And Materialization

- `live_lake_freshness_gate.py` compares committed snapshot versus fresh live-lake
  selection using content-addressed watermarks and per-account hashes; it writes
  nothing and returns fresh versus `snapshot_behind_lake`
  (`forseti-harness/capture_spine/creator_profile_current/live_lake_freshness_gate.py:1-23`,
  `forseti-harness/capture_spine/creator_profile_current/live_lake_freshness_gate.py:72-105`).
- `rollup_formula_revalidation.py` independently recomputes known recipes and
  fails on unknown recipe versions
  (`forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py:29-39`,
  `forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py:207-221`).
- `materialize.py` builds profile-current from account ledger and metric
  seed/snapshot inputs, carrying source pointers and roles; it does not compute
  deferred metric recipes (`forseti-harness/capture_spine/creator_profile_current/materialize.py:21-45`,
  `forseti-harness/capture_spine/creator_profile_current/materialize.py:220-248`).

These are checks/materializers, not time-decay scores, monitoring schedulers, or
request-budget proof.

## Forbidden Or Unsupported Outputs

- Cross-platform person identity, default `person_id`, private contact, outreach,
  demographics, follower/connection/commenter graph capture, and audience estimate
  claims are forbidden in current Creator Vault/profile surfaces
  (`forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md:512-553`; `forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_lane_index_v0.md:61-72`).
- Gold/Judgment fields in Silver or Creator Vault are forbidden: no credibility,
  durability, manufactured-demand, fake/bot/paid verdict, partner/action
  recommendation, or product ranking
  (`forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md:568-605`; `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md:618-626`).
- A YouTube view-only seed cannot produce engagement, average likes, or average
  comments; those stay `unavailable_with_reason`
  (`forseti-harness/capture_spine/creator_profile_current/youtube_metric_seed.py:157-176`; `forseti-harness/capture_spine/creator_profile_current/youtube_metric_seed.py:615-628`).
- TikTok `shareCount` and `collectCount` are preserved as observations in the
  harness builder but are not rollup inputs
  (`forseti-harness/capture_spine/creator_profile_current/tiktok_metric_seed.py:10-13`; `forseti-harness/capture_spine/creator_profile_current/tiktok_metric_seed.py:47-86`).
- AEO is not query-volume truth, not independence proof, not floor clearance, and
  not gate-recordable without schema hardening
  (`forseti/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md:286-301`).

## Product-Surface Implication For Aphrodite

Aphrodite can read accepted, lineage-backed fields and display limitations,
freshness, sample support, and missingness. It must not become the metric authority
or silently compute hidden recipes inside `creator_profile_current`.

Safe now: show observed platform/account rollups; show `unavailable_with_reason`
and `not_attempted`; downgrade or withhold thin admitted-pool rows; show source
drill-back and freshness; keep platforms separate unless future linkage authority
and a downstream surface contract authorize more.

Unsafe now: sorting by non-observed metrics; showing null as zero; fabricating
YouTube engagement from view-only data; labeling admitted-pool means as moving
averages, trends, velocity, spikes, breakouts, decay, or active watch; using SoV as
market total/cross-platform share/buyer proof; treating LinkedIn/AEO observations
as independent demand proof or outreach basis.

## Successor Recommendation

This doc is broad enough for Aphrodite scoping, but it now carries two catalogs at
once: capture-surface routing and metric-family/readout posture. If ongoing
maintenance is desired, split it into:

1. `forseti_capture_surface_inventory_v0.md`: route/capturable/captured evidence by
   source family and scanning family.
2. `forseti_metric_family_inventory_v0.md`: current/deferred/proposed/forbidden
   metrics/readouts with recipe versions, posture, lineage, and implementation
   evidence.

Do not mint that split from this commission without new bounded authorization.
