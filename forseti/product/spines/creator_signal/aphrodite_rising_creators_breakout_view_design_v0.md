# Aphrodite Rising Creators Breakout View Design v0

```yaml
retrieval_header_version: 1
artifact_role: Product design proposal (Creator Signal ranked read model)
scope: >
  Design for a deterministic, precomputed "rising creators" ranked view over
  the creator registry, including acceleration features, the rising x ad-load
  output, held-out backtest plan, and limits. It scopes a later owner-authorized
  build; it does not authorize capture, runtime, storage, ML, or outreach work.
use_when:
  - Deciding whether or how to build Aphrodite's rising-creators / breakout-precursor read.
  - Checking the difference between creator momentum, creator acceleration, and sponsorability.
  - Preparing a build handoff for a deterministic Creator Signal ranked view over Capture-owned records.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
  - forseti/product/spines/creator_signal/aphrodite_vetting_sprint_panel_design_v0.md
  - docs/decisions/forseti_ontology_gt_foundation_ladder_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
stale_if:
  - Aphrodite's five-panel design or forbidden set changes.
  - Capture owns a new implemented breakout, velocity, spike, or movement-threshold recipe.
  - The data-lake precompute policy changes from rebuildable manifest-backed views.
  - The ontology ladder triggers R4 query-surface or R7 automated identity-clustering work.
```

## Status

`DESIGN_V0 - OWNER_REVIEW_INPUT`.

This is a design artifact only. It does not authorize implementation, live
capture, a scheduler, lake mutation, runtime storage, a query service, an ML
pipeline, outreach, contact enrichment, lead-list export, or a customer-facing
score. It prepares a later build decision for the smallest complete derived
read model that can answer: which under-the-radar fragrance creators appear to
be accelerating toward a breakout, and which of them are still sponsorable?

## Start Preflight

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  cynefin_route: complicated
  source_pack: custom_s2_plus_creator_signal_rising_design
  edit_permission: docs-write
  isolation: existing clean worktree claude/aphrodite-moat-domination-sharpening
  target_scope:
    - forseti/product/spines/creator_signal/aphrodite_rising_creators_breakout_view_design_v0.md
    - forseti/product/spines/creator_signal/README.md
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - .agents/workflow-overlay/validation-gates.md
    - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
    - forseti/product/spines/creator_signal/aphrodite_vetting_sprint_panel_design_v0.md
    - docs/decisions/forseti_ontology_gt_foundation_ladder_v0.md
```

Cynefin route:

- Smallest complete outcome: a design for a deterministic precomputed ranked
  Creator Signal read model, with acceleration features, sponsorability overlay,
  held-out backtest, and honest limits.
- Regime: complicated.
- Why: the target is designable from current product, Capture, data-lake, and
  ontology sources, but ownership boundaries are easy to blur.
- Decomposition: layer-based.
- Current bottleneck: defining acceleration and sponsorability without turning
  Creator Signal into Capture, Data Lake, an ontology query surface, or an ML
  scorer.
- Riskiest assumption: that enough comparable capture cycles and per-video
  observations exist to distinguish true acceleration from one-off noise.
- Stop or pivot condition: if source inspection shows fewer than the minimum
  comparable windows for most registry creators, the first build should become a
  "history sufficiency and watchlist posture" view, not a rising-rank product.
- Allowed next move: owner may authorize a docs-bounded build handoff for a
  rebuildable derived view and backtest runner.
- Disallowed next move: building capture, a scheduler, a general query service,
  automated identity clustering, or a customer-facing vanity score from this
  design alone.

## Source Basis

Read as controlling or decision-bearing for this artifact:

| Source | What it constrains |
| --- | --- |
| `aphrodite_carveout_charter_v0.md` Sections 3, 4, and 6 | Layer 2 time/momentum product, the five-panel sprint including sponsorship load and momentum, the cheap-layer/deep-layer capture split, breakout trigger language, and the forbidden set. |
| `aphrodite_vetting_sprint_panel_design_v0.md` Section 5 | Momentum is baseline-relative only and requires capture cycles; ad-reception uses sponsored-vs-organic comparison. |
| `docs/decisions/forseti_ontology_gt_foundation_ladder_v0.md` ladder | R4 materialized query surface and R7 automated identity clustering are not triggered; keep this deterministic-first and below ontology-query infrastructure. |
| `core_spine_v0_data_lake_consumption_seam_contract_v0.md` | Metrics are on-demand by default; any precomputed metric view must be rebuildable, manifest-backed, and non-authoritative. |
| `creator_profile_current_view_spec_v0.md` and `creator_profile_current_record_contract_v0.md` | Creator profile current is a derived view over sibling records; missing is null plus reason, not zero; metric comparison requires compatible windows, sample support, and visible limitations. |
| `aphrodite_derived_claim_provenance_contract_v0.md` | Derived claims shown by Creator Signal need claim-object provenance; unstamped derived labels withhold. |
| `docs/research/aphrodite_silver_metric_monitoring_inventory_v0.md` | Current metric rollups exist, but SMA, EMA, velocity, delta, spike, breakout, decay, and active-watch recipes are proposed/deferred, not implemented. |

Available but not broadly loaded because they would add background rather than
change this design: all review outputs, all historical proof packets, all
capture runners, all research corpus files, and all prompt artifacts.

## Design Recommendation

Build target, if later authorized:

Aphrodite should have a precomputed, rebuildable ranked view:

```text
creator_registry + metric observations + rollups + ad-classification claims
  -> deterministic feature extraction
  -> rising_creator_ranked_view_v0
  -> Creator Signal report/surface cut: "rising and still sponsorable"
```

The product is not "popular creators." It is the smaller and more valuable
question: which under-the-radar creators have a positive inflection against
their own prior behavior, while recent sponsorship load is still low enough
that a brand can plausibly afford and reach them?

The ranked view should serve two use cases:

1. Buyer report cut: "rising creators you can still afford, with evidence and
   limits."
2. Internal scouting cut: "creator accounts to watch or deepen before they
   become expensive."

Both cuts use the same derived read model. Neither cut exports contacts or
turns into an outreach list.

## Ownership Boundary

Creator Signal owns this artifact because it is a product-facing read model and
claim/display design over creator intelligence. Capture and Data Lake own the
source records, capture routes, metric computation, storage, rebuild mechanics,
and any later materializer implementation.

This design must preserve:

- public-information-only posture;
- no contact fields, outreach actions, lead-list export, or public person-level
  directory;
- no cross-platform creator aggregation unless promoted linkage exists;
- no zero-filled missing metrics;
- no unstamped/LLM-only derived claims;
- no "creator score" shipped to buyers as a black-box performance guarantee;
- no R4 ontology query surface or R7 automated identity clustering as the first
  move.

## Core Distinction: Momentum Versus Acceleration

Momentum answers: is the creator moving now?

Acceleration answers: is the creator moving faster than they were moving before?

The ranked view must privilege acceleration. A large creator with consistently
high views has momentum but may not be rising. A small-base creator whose last
few videos are materially outperforming their own baseline is the breakout
precursor.

Minimum posture rule:

- With one capture point: `withhold_rising_state`.
- With two comparable capture cycles: show velocity/delta posture only; do not
  claim acceleration.
- With at least three comparable windows or enough per-video publication-time
  observations to compare slopes: acceleration may be shown, still with sample
  support and limitations.

This is stricter than ">=2 cycles for velocity" because acceleration is a rate
change. Calling a two-point delta "acceleration" would be fake precision.

## Eligibility Gates

The view should run over all registry creators, but only some are eligible for a
`rising` classification. Others stay visible with posture.

| Gate | Rule | Failure posture |
| --- | --- | --- |
| Registry subject | Public platform account or promoted creator record with source pointers. | `unsupported_subject` |
| Small-base / under-radar | Not already established by declared category-size profile. Use a versioned profile, such as current known follower/view percentile bands, not hard-coded generic celebrity thresholds. | `established_creator_excluded` |
| Comparable metric basis | At least one source-visible base metric available across compatible content/window scope. | `insufficient_metric_basis` |
| History sufficiency | Minimum two cycles for velocity; minimum three comparable windows for acceleration. | `insufficient_history` or `velocity_only` |
| Freshness | Latest input inside declared freshness window. | `stale_inputs` |
| Provenance | Every shown feature carries source refs, recipe version, computed_at, and posture. | `withhold_feature` |

The small-base gate should be profile-driven because "under-the-radar" is
relative to the fragrance niche and platform. A fixed follower count will rot.

## Feature Set

Every feature is deterministic, recipe-versioned, and posture-coupled.

| Feature | Definition | Why it matters | Show posture |
| --- | --- | --- | --- |
| Early per-content velocity lift | For recent posts/videos, normalize source-visible views or plays by elapsed time since publish/capture, then compare against the creator's trailing baseline for compatible content. | Catches a video breaking out before absolute totals catch up. | `show` only when publish/capture timing and source-visible count are compatible; otherwise `withhold`. |
| Fast/slow window crossover | Compare fast-window creator performance against a slower trailing window using compatible metrics and content kinds. | Detects a positive inflection, not just high current level. | Needs at least three comparable windows for acceleration language. |
| Self-breakout rate | Share of recent content units beating the creator's own declared breakout envelope. | A creator with repeated small breakouts is different from one lucky hit. | Show as count and share with sample support, never as channel-wide truth. |
| Follower-cycle delta | Change in observed follower count per capture cycle when source-visible. | Adds account-level adoption evidence beyond per-video performance. | Mark platform-specific and observation-only. |
| Engagement-quality shift | Change in comment/view, like/view, save/share if source-visible, plus aggregate intent-language movement when derived claims satisfy provenance. | Helps separate empty views from commercially meaningful attention. | Derived labels require the derived-claim provenance contract; absent inputs withhold. |
| Fit-relevant participation | Whether acceleration is happening in fragrance/brand-fit content, not unrelated viral content. | A creator rising because of irrelevant content is weaker for a fragrance sponsor. | Needs source-backed product/brand/topic classification or stays `unknown_fit_relevance`. |
| Consistency / noise guard | Penalize one-post-only spikes, thin samples, stale captures, incompatible windows, and platform/content-kind mismatch. | Prevents one lucky video from dominating. | Always visible as limitation/posture. |

V0 should not include EMA, ML clustering, global topic models, or a general
ontology query surface. SMA/EMA can be named as future recipes only after their
field-level contracts and source support exist.

## Sponsorship Load Overlay

The sellable cut is not "rising" alone. It is:

```text
rising_creator + low_or_moderate_recent_ad_load + sponsored_content_still_performs
```

Ad-load and ad-reception stay separate from the acceleration score so the owner
and buyer can see the tradeoff.

| Overlay field | Definition | Posture |
| --- | --- | --- |
| `recent_sponsored_content_count` | Count of recent content classified as paid/gifted/affiliate/self-brand by metadata, description, disclosure marker, or derived claim. | Confidence and receipt required; hidden gifting remains limitation. |
| `ad_density` | Sponsored/gifted/affiliate share over declared recent window. | Show denominator and window; do not infer all sponsorships are visible. |
| `sponsor_concentration` | Whether a small number of sponsors dominate recent sponsored content. | Optional v0 if sponsor extraction is source-backed; otherwise proposed. |
| `disclosure_hygiene` | How explicit and consistent sponsorship markers are. | Derived from receipts; not legal compliance advice. |
| `sponsored_vs_organic_performance` | Matched sponsored content versus matched organic content for the same creator/window/content kind. | Withhold or downgrade when matched pairs are absent or thin. |
| `sponsorable_bucket` | `prime_sponsorable`, `rising_but_saturated`, `rising_but_ad_reception_weak`, `rising_unknown_ad_load`, or `not_rising`. | Derived bucket, never contact/outreach authorization. |

The prime buyer-facing row is `prime_sponsorable`: acceleration evidence is
strong enough to inspect, recent ad-load is not saturated, and sponsored
content does not materially underperform matched organic content. This still
does not prove the creator will accept a sponsorship or produce ROI.

## Ranked View Shape

The view is a derived, rebuildable read model. It is not the source of truth.

Suggested logical name:

```text
rising_creator_ranked_view_v0
```

Minimum fields:

| Field group | Fields |
| --- | --- |
| Identity | `view_row_id`, `profile_subject_kind`, `profile_subject_id`, `platform_account_ids`, `creator_record_id_or_none`, `platform_scope`, `identity_state`. |
| Build provenance | `recipe_version`, `computed_at`, `input_manifest_id`, `registry_snapshot_ref`, `source_record_refs`, `input_coverage_summary`. |
| Eligibility | `eligibility_state`, `small_base_profile_version`, `history_sufficiency_state`, `freshness_state`, `withhold_reasons`. |
| Acceleration features | per-feature claim objects for velocity lift, fast/slow crossover, self-breakout rate, follower delta, engagement-quality shift, fit-relevant participation, and consistency/noise guard. |
| Sponsorship overlay | ad-load count, ad-density bucket, sponsor concentration posture, disclosure-hygiene posture, sponsored-vs-organic performance posture, sponsorability bucket. |
| Ranking | `internal_rank_sort_key`, `acceleration_band`, `sponsorability_band`, `rank_explanation`, `rank_inputs_visible`. |
| Display contract | `recommended_surface_bucket`, `limitations`, `non_claims`, `source_drill_back`. |

The `internal_rank_sort_key` may be numeric because a precomputed ranked table
needs deterministic ordering. The buyer-facing surface must not expose it as a
single vanity creator score. Show bands, components, receipts, and limits.

Recommended output buckets:

- `prime_sponsorable_rising`: rising evidence plus low/moderate ad-load and no
  sponsored-performance red flag.
- `rising_watch`: rising evidence but ad-load unknown, thin, or not enough
  matched sponsored evidence.
- `rising_but_saturated`: rising evidence but ad-load high or sponsor
  concentration high.
- `velocity_only_watch`: positive movement, not enough history for acceleration.
- `stable_or_established`: not a rising target under this product.
- `withheld`: provenance, freshness, or boundary failure.

## Ranking Logic

V0 ranking should be deterministic and profile-versioned:

1. Exclude or withhold rows that fail hard gates.
2. Classify acceleration evidence into `strong`, `medium`, `weak`, or
   `withheld` based on versioned thresholds.
3. Apply a noise guard: thin samples and one-post spikes cannot reach `strong`
   without repeated evidence.
4. Classify sponsorability independently.
5. Sort first by acceleration band, then by consistency/noise guard, then by
   sponsorability bucket, then by freshness and source support.

Do not fit weights on the same period used for the held-out test. If weights
are tuned, tune them on a training slice and report held-out performance
separately.

## Precompute Policy

Default product posture: precompute the ranked view nightly or per capture
cycle once the owner authorizes a build.

But the precompute is only a rebuildable cache:

- Inputs remain Capture/Data Lake-owned records and derived claim objects.
- The precomputed view carries an input manifest and recipe version.
- A rebuild from the same manifest should reproduce the same rank rows.
- Missing/blocked values remain null plus reason.
- The view may be used for product display and scouting triage, not as source
  authority.

On-demand computation remains acceptable for bespoke sprint cuts, especially
when the buyer's candidate set, product category, or brand adjacency filter is
custom.

Physical implementation should be decided in the later build handoff. The
smallest complete first build is likely a static/committed derived view over the
current registry and metric records, plus a backtest script/report. If the view
becomes a recurring lake metric family, it must obey the data-lake
manifest-backed derived-retrieval policy.

## Held-Out Backtest Plan

The signal does not ship as trusted unless it beats base rate on history.

### Setup

1. Choose one or more historical cutoffs where the registry and capture inputs
   can be reconstructed from pre-cutoff records.
2. Freeze the creator registry as of each cutoff.
3. Use only pre-cutoff observations for features.
4. Run the deterministic rising recipe exactly as it would have run then.
5. Evaluate post-cutoff outcomes over declared horizons, such as 30, 60, and
   90 days.

If historical registry snapshots are not reconstructable, the first build must
include a forward-holdout plan and may not claim historical lift.

### Outcome labels

Use public, source-backed outcomes. Candidate labels:

- future median/average view lift over the creator's own pre-cutoff baseline;
- repeated post-cutoff content units crossing the creator's own breakout
  envelope;
- follower-count lift where source-visible and capture-cycle compatible;
- movement into a higher niche/platform percentile band;
- sustained performance over multiple post-cutoff posts, not a single spike.

The primary label should be "sustained relative lift," not "went viral once."

### Baselines to beat

Compare precision and lift against:

- raw popularity rank;
- raw current momentum/velocity rank;
- recent posting cadence;
- random small-base eligible creators;
- manual "recent high view" heuristic.

Report at least:

- base breakout rate;
- precision at top K;
- lift over base rate at top K;
- recall among eventual breakouts;
- false-positive examples and why they failed;
- false-negative examples and what the recipe missed.

Minimum ship rule: if the rising view cannot beat the base rate and raw-momentum
baseline on held-out data, it does not ship as a product claim. It may remain an
internal watchlist with explicit `not_validated` status.

### Leakage controls

- No post-cutoff views, followers, sponsorships, or manual knowledge in feature
  computation.
- No creator added after cutoff unless the backtest explicitly tests discovery
  and freezes that discovery input as of cutoff.
- No manual removal of "obvious" future winners or losers.
- No tuning on the held-out period after seeing outcomes.
- No collapsing accounts unless linkage was promoted before cutoff.

### Sponsorability evaluation

Sponsorability is partly predictive and partly commercial-fit descriptive. The
first backtest should report it separately:

- How many true future risers were `prime_sponsorable` at cutoff?
- How many were already saturated?
- Did sponsored content performance remain comparable to organic?
- Were ad-load labels source-backed or often unknown?

Do not claim sponsor conversion or willingness to pay from this backtest. It can
only support "rising and not visibly ad-saturated" unless later commercial
receipts exist.

## Display Contract

Buyer/report presentation should lead with evidence, not a score:

- creator handle/account and niche fit context;
- acceleration band and why it is banded that way;
- recent examples driving the rank;
- ad-load and ad-reception state;
- source support and windows;
- material limitations;
- "why not higher/lower" explanation;
- source drill-back for shown claims.

Internal scouting can show more operational fields, but still no contact data,
no outreach authorization, and no public person-level directory behavior.

## Honest Limits

These limits must travel with the product:

- This is probabilistic lift, not prophecy.
- Exogenous virality, algorithm changes, creator controversy, and off-platform
  events can dominate the signal.
- Small-base creators are noisy; one post can distort a short window.
- Acceleration needs history. Without enough capture cycles, the correct output
  is watchlist posture, not a rising claim.
- Hidden gifting and undisclosed sponsorships make ad-load lower bounds, not
  complete truth.
- Comments are page-1 visible and may be moderated or skewed.
- Platform metrics are not directly comparable unless the recipe says how they
  were normalized.
- Backtest lift does not prove buyer willingness to pay, sponsorship ROI, or
  creator acceptance.
- The domination edge comes from whole-niche coverage plus time-series
  accumulation. A curated panel cannot reproduce that, but a funded competitor
  can still copy extraction flow; this is position rent, not magic.

## Build Authorization Shape

The smallest complete later build should include:

1. A recipe/version document for the feature thresholds and postures.
2. A rebuildable materializer for `rising_creator_ranked_view_v0`.
3. A manifest-backed output over the current registry.
4. A held-out or forward-holdout backtest report.
5. README/front-door updates only where needed for retrieval.

It should not include:

- new capture routes;
- scheduler work;
- general query service;
- customer UI;
- ML clustering;
- outreach workflows;
- contact enrichment;
- ontology R4/R7 infrastructure.

Owner decision needed before build: authorize the derived-view materializer and
backtest lane, and choose whether the first output is a static Creator Signal
artifact or a Data Lake derived-retrieval metric-family view.

## Non-Claims

This artifact is not validation, readiness, proof, buyer pull, willingness to
pay, product-market fit, implementation authorization, capture authorization,
runtime authorization, source-of-truth promotion, or a claim that current code
already computes acceleration, velocity, spike, or breakout states.
