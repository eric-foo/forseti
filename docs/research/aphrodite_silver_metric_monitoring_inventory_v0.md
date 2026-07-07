# Aphrodite Silver Metric Monitoring Inventory v0

```yaml
retrieval_header_version: 1
artifact_role: >
  Research inventory record (Aphrodite creator-metric capture/monitoring
  inventory; documentation lane, not implementation authorization)
scope: >
  Source-backed inventory of which creator metrics Forseti currently captures and
  rolls up in Silver, which freshness/revalidation checks exist, and which
  Aphrodite monitoring recipes (moving average, EMA, velocity, spike, breakout,
  decay, active-watch expiry) are proposed-but-not-implemented. Documents the gap
  so Aphrodite Signals reads it, and does not invent it.
use_when:
  - Deciding which creator stat is safe to surface as observed vs. deferred vs. proposed.
  - Preparing the later Aphrodite roster-size / request-budget calculation.
  - Scoping the first Silver metric recipe (which of SMA/EMA/velocity/spike/breakout to document first).
authority_boundary: retrieval_only
open_next:
  - docs/research/aphrodite_creator_capture_strategy_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
branch_or_commit: >
  Harness/contract state inventoried on branch
  codex/aphrodite-creator-capture-strategy @ b41b669f (creator-metric harness is
  main-line, branched from 0af842e5). Recheck if the producers or contracts change.
stale_if:
  - Creator metric Silver contracts, profile-current contracts, or runner entrypoints change.
  - Aphrodite capture strategy is superseded.
  - Moving-average, EMA, velocity, spike, or breakout-state recipes are implemented (this inventory then understates what exists).
```

## Status

`PROPOSED_DOCS_INVENTORY_V0`.

Documentation-only. This is not validation, readiness, capture authorization, live
monitoring approval, lake-write approval, request-budget feasibility, buyer proof,
or product readiness. It reports the contract and harness-code state as read on the
Aphrodite lane at the commit above; recheck the primary sources before relying on
any absence claim below.

Consumes the handoff `docs/workflows/aphrodite_silver_metric_monitoring_docs_handoff_v0.md`.

## Why This Exists

Aphrodite Signals sits directly on top of Silver/Vault and the creator registry. The
product surface must **not** invent moving averages, EMA, velocity, spike state, or
breakout state inside `creator_profile_current`. Those recipes belong in Silver
`MetricObservation` / `MetricRollupObservation` with a named recipe version, lineage,
and posture — then the registry read model copies only the accepted, lineage-backed
field.

This inventory separates five things the strategy asks Aphrodite to keep distinct:

1. currently emitted source metric observations;
2. currently emitted rollups;
3. current freshness and revalidation checks;
4. candidate Aphrodite monitoring recipes (proposed, not built);
5. forbidden, unsupported, or source-hidden stats.

## Reading Rule (Posture / Value Coupling)

Every metric obeys the Silver Vault coupling and it is load-bearing for every table below:

```text
observed      -> numeric value, no reason
non-observed  -> null value, a reason (unavailable_with_reason / out_of_window / not_attempted / not_applicable)
```

`metric_value = 0` is valid **only** as a real observed zero from the source. Missing,
hidden, blocked, not-attempted, and not-applicable are never zero and must never be
ranked, averaged, or shown as poor performance. Silver owns the recipe-backed rollups;
`creator_profile_current` stores and presents the latest accepted rollup — it does not
compute global longitudinal stats.

## Table A — Capture Surfaces Currently Emitting Silver Metrics

| Platform / source surface | Source-visible raw facts observed | Freshness / revalidation / materialization | `calculation_recipe_version` + lineage owner | Status |
| --- | --- | --- | --- | --- |
| **Instagram** reels-grid projection | per-content `view_count`, `like_count`, `comment_count`; per-account `follower_count` (observation only, not yet a rollup field) | freshness gate + formula revalidation + materialize (shared, see Table C-freshness) | `creator_metric_rollup_instagram_reels_grid_engagement_v0` — `forseti-harness/capture_spine/creator_profile_current/instagram_metric_seed.py` → `silver_metric_producer.py` | current |
| **YouTube Shorts** — genesis seed (checked-in review-input pool) | per-Short `view_count` only | same shared checks | `creator_metric_rollup_admitted_youtube_shorts_average_v0` — `youtube_metric_seed.py` → `youtube_silver_metric_producer.py` | current (view-only) |
| **YouTube Shorts** — live watch-packet (committed `youtube_watch_metadata_comments` lake packets) | per-Short `view_count`, `like_count`, `total_comment_count` | same shared checks | `creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0` — `youtube_watch_packet_metric_document.py` → `youtube_silver_metric_producer.py` | current |
| **TikTok** batch-admission packets | per-video `view_count` (`playCount`), `like_count` (`diggCount`), `total_comment_count` (`commentCount`); `shareCount`/`collectCount` preserved but **not** rollup inputs | same shared checks | `creator_metric_rollup_tiktok_profile_grid_engagement_v0` — `tiktok_metric_seed.py` → `tiktok_silver_metric_producer.py` | current |

All producers **reuse tested seed numbers and never recompute** inside the Silver
wrapper; the Silver records carry the common Vault header, posture/value coupling, and
`derived_refs` lineage per
`forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md`.
Subjects are per-platform account `entity_key`s only — **no cross-platform creator rollups**.

## Table B — Rollup Field Status by Surface

The rollup field set is fixed (`_ALLOWED_METRIC_KEYS` in
`forseti-harness/capture_spine/creator_profile_current/validation.py`) and is identical
across every surface; only the posture differs by source completeness.

| Rollup field | IG reels-grid | YT genesis seed | YT watch-packet | TikTok batch |
| --- | --- | --- | --- | --- |
| `average_views` | observed | observed | observed | observed |
| `median_views` | observed | observed | observed | observed |
| `average_like_count` | observed | `unavailable_with_reason` | observed | observed |
| `average_comment_count` | observed | `unavailable_with_reason` | observed | observed |
| `engagement_rate` | observed | `unavailable_with_reason` | observed | observed |
| `posting_cadence` | `not_attempted` | `not_attempted` | `not_attempted` | `not_attempted` |
| `recent_velocity` | `not_attempted` | `not_attempted` | `not_attempted` | `not_attempted` |

Notes:

- `average_views` / `median_views` are a plain mean / median over the admitted/selected
  pool — **not** a time-windowed or rolling average.
- `engagement_rate` is computed as `(Σ likes + Σ comments) / Σ views` over **complete**
  view/like/comment trios; where like/comment inputs are absent (YouTube genesis seed) it
  is `unavailable_with_reason`, never a zero.
- Rollups also carry `view_count_min` / `view_count_max`, `observation_count`,
  `sample_support` (`thin_n_1_to_3` / `limited_n_4_to_7` / `stronger_admitted_pool_n_8_plus`),
  and `freshness_state`. `sample_support` gates **presentation** (thin samples must be
  downgraded or withheld), not computation.

## Deferred-In-Schema Fields (`posting_cadence`, `recent_velocity`)

These are contract fields, present in **every** rollup on **every** platform, always as
`not_attempted` with `value_or_none: null` and reason "recipe is out of scope for this
metric seed/document." This is a deliberate, structurally-enforced deferral, not an
oversight: `forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py`
hard-asserts (`_NEVER_COMPUTED_METRICS`) that neither field may ever carry `observed`
posture, across all four recipe versions.

Activation conditions before first observed population (from
`creator_profile_current_record_contract_v0.md` §3):

- `posting_cadence = observed_content_count / window_days` — requires source-backed
  **publication timestamps** and a declared window. If publication timing is unavailable,
  the field must stay non-observed; capture timing must not be smuggled in as posting behavior.
- `recent_velocity = (latest − prior compatible rollup value) / elapsed_days` — requires
  **≥2 compatible Silver rollups** for the same subject, compatible scope/window, observed
  base metric in both, and positive elapsed time. A single capture cycle cannot produce it.

## Table C — Candidate Aphrodite Monitoring Recipes (Proposed)

Each candidate below was checked against the creator-metric harness by reading every
producer/runner and grepping the tree. **None has implementing code** at the inventoried
commit — each is `proposed` and, per the strategy, must route through Silver
`MetricObservation` / `MetricRollupObservation` with an explicit recipe version, source
observation ids, posture/value coupling, sample support, freshness, and limitations.
Do **not** document any of these as product-ready.

| Candidate recipe | Required history / sample support | Posture / missingness behavior | Implemented-code verdict (file:line evidence) | Status |
| --- | --- | --- | --- | --- |
| Simple moving average (SMA) | ≥1 compatible Silver rollup series over a declared time window | observed only over compatible windows; else null+reason | **ABSENT** — `average_*` are plain `statistics.mean()` over a pool, not windowed (`instagram_metric_seed.py:399`, `tiktok_metric_seed.py:613`, `youtube_watch_packet_metric_document.py:625`) | proposed |
| Exponential moving average (EMA) | as SMA, plus a declared smoothing factor | observed only over compatible windows; else null+reason | **ABSENT** — no EMA/exponential-smoothing code in any metric module (only "exponential" hit is unrelated HTTP retry backoff) | proposed |
| Compatible-window velocity | ≥2 compatible rollups, positive elapsed time, observed base metric in both | non-observed with reason until compatible history exists | **ABSENT** — `recent_velocity` always `not_attempted`; hard-enforced by `rollup_formula_revalidation.py` `_NEVER_COMPUTED_METRICS` | deferred (schema field reserved) |
| Capture-window delta (when publication timing unavailable) | ≥2 grid heartbeats of the same subject; a prior snapshot | delta only where prior observation exists; label as capture-window, **not** posting cadence/age velocity | **ABSENT** — no cross-capture delta computed; snapshot machinery selects the latest rollup, it does not diff magnitudes | proposed |
| Spike score vs. creator baseline or platform/content-kind norm | compatible recent baseline for the subject/norm | observed only when baseline inputs observed; else null+reason; nulls never ranked as low | **ABSENT** — no spike scoring; the only "spike" hits are explicit non-claims in an unrelated RSS monitor | proposed |
| Breakout state (high **and** still growing) | a spike/velocity signal plus a growth check | state only from observed inputs; expiry required (below) | **ABSENT** — zero "breakout" occurrences in `forseti-harness` | proposed |
| Decay / plateau state | a tracked breakout with measured slope over rechecks | state only from observed slope; else null+reason | **ABSENT** — no decay/plateau metric ("decay" hits are IG rate-limit cooldown non-claims) | proposed |
| Active-watch expiry state | an explicit, self-expiring recheck window on a promoted item | must be explicit, source-backed, self-expiring; no hidden forever-watch | **ABSENT** — nearest is manual `operator_video_retirements`/`excluded_video_ids` (attested exclusion), not a time-based expiry state machine | proposed |

**Shared freshness / revalidation / materialization runners** referenced above (current, platform-agnostic):

- `forseti-harness/capture_spine/creator_profile_current/live_lake_freshness_gate.py`
  (+ runner `run_live_lake_freshness_gate.py`) — re-runs the pure snapshot generator against
  the live lake and compares content-addressed watermarks/per-account hashes to the committed
  snapshot. Binary verdict `is_fresh` / `snapshot_behind_lake`; **no time-decay staleness scoring**.
- `rollup_formula_revalidation.py` (+ `run_creator_rollup_formula_revalidation.py`) —
  independently re-derives every rollup from source observations per its recipe version;
  checks content-hash reproducibility, lineage, cardinality, posture coupling, and the
  never-computed guard. Unknown recipe = failure.
- `materialize.py` (+ `run_creator_profile_current_materialize.py`) — joins the account
  ledger with metric seeds/snapshots into `creator_profile_current_view`; copies rollup
  fields verbatim, computes nothing.
- Rollup production / snapshot: `run_creator_metric_rollup_producer.py`,
  `run_youtube_creator_metric_rollup_producer.py`, `run_youtube_watch_packet_metric_rollup_producer.py`,
  `run_tiktok_batch_metric_rollup_producer.py`, `run_creator_metric_rollup_snapshot.py`,
  `run_instagram_reels_creator_metric_seed_materialize.py`.

## Forbidden, Unsupported, or Source-Hidden Stats

- **No engagement number from view-only data.** The YouTube genesis seed exposes only
  `view_count`; `engagement_rate`, `average_like_count`, `average_comment_count` are
  `unavailable_with_reason`, never a fabricated zero.
- **No hidden derived metrics inside `creator_profile_current`.** SMA/EMA/velocity/spike/
  breakout/decay/active-watch must live in Silver with recipe + lineage, never as registry
  read-model logic.
- **No cross-platform creator rollups or person identity.** Per-platform account subjects
  only; no `person_id`, follower graph, audience estimate, demographics, or contact/outreach fields.
- **No Gold/Judgment fields** in Silver, Creator Vault, or profile-current: no credibility
  score, fake/bot label, paid/unpaid verdict, manufactured-demand or durability verdict,
  partnership/action recommendation.
- **TikTok `shareCount` / `collectCount`** are preserved as source facts but are **not**
  rollup inputs and must not be folded into `engagement_rate` without a new accepted recipe.
- **Aphrodite Signals is not the metric authority.** Silver owns recipe-backed observations
  and rollups; Aphrodite reads accepted, lineage-backed fields and their visible limitations.

## Boundaries (This Docs Pass)

- Do not implement moving average, EMA, velocity, spike score, breakout, or scheduler
  behavior in this lane.
- Do not run live capture, mutate the lake, or create new metric records.
- Do not hide derived metrics inside `creator_profile_current`.
- Do not turn Aphrodite Signals into the metric authority.
- Do not claim request-budget readiness or daily monitoring feasibility from this inventory
  alone (the strategy's "Open Decisions Before Calculation" remain open).

## Provenance and Placement

- **Placement:** `docs/research/`, sibling to `docs/research/aphrodite_creator_capture_strategy_v0.md`.
  It is a synthesis/inventory that supports the Aphrodite strategy without becoming product
  authority (per `.agents/workflow-overlay/artifact-folders.md`); it is not a contract and
  does not belong under the `creator_registry/` authority folder.
- **Absence claims** in Table C were verified by reading every creator-metric producer/runner
  under `forseti-harness/capture_spine/creator_profile_current/` and `forseti-harness/runners/`
  plus a tree grep; they are point-in-time at the inventoried commit. A grep/read is not a
  guarantee for the future — if a recipe is later implemented, this inventory becomes stale
  (see `stale_if`).
