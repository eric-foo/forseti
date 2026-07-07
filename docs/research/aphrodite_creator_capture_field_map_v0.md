# Aphrodite Creator Capture — Trackable Data & Stats Field Map v0

```yaml
retrieval_header_version: 1
artifact_role: >
  Research reference map (creator-channel capture + derived-stat field inventory;
  retrieval-only). Field-level companion to the Aphrodite Silver metric monitoring
  inventory.
scope: >
  Field-level map of what data and stats Forseti can track or harvest for one
  creator channel, organized by capture layer — grid heartbeat, deep per-reel
  capture, and derived computations — each tagged live / built-gated / deferred /
  proposed, with a source pointer to drill into.
use_when:
  - "What data or stats can we track / harvest for a creator?" — this doc is the answer.
  - Checking what the grid layer vs deep capture vs the derived layer each yields, field by field.
  - Checking whether a given creator stat is built, deferred, or proposed, and where its source lives.
authority_boundary: retrieval_only
open_next:
  - docs/research/aphrodite_silver_metric_monitoring_inventory_v0.md              # broader capture-surface + metric-family inventory (same lane)
  - docs/research/aphrodite_creator_capture_strategy_v0.md                        # the grid-heartbeat + deep-capture + promotion strategy
  - docs/workflows/aphrodite_proposed_creator_stats_design_handoff_v0.md          # nonresolving: external-worktree packet, never committed; the design lane it opened is discharged by the design spec on PR #787
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_creator_ideal_audience_inference_spec_v0.md
  - forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md
branch_or_commit: >
  Field statuses read against current main-line source specs + forseti-harness
  (2026-07), on branch codex/aphrodite-creator-capture-strategy. Recheck the cited
  source if a producer, spec, or contract changes.
stale_if:
  - Any cited grid / deep / derived spec, producer, or fusion module changes.
  - A proposed stat here lands with a recipe/version/runner (update its status).
  - The Aphrodite inventory or strategy is superseded.
```

## Status

`REFERENCE_MAP_V0`. Retrieval-only. Not validation, readiness, buyer proof, capture
authorization, or product authority. This is a where-to-find map, not a claim that
any stat is production-ready. Statuses are point-in-time; the cited source is the
truth.

## How to read this map

**Status tags:** **LIVE** = code runs today · **BUILT·gated** = code exists, a live
wire (LLM key / auth loop) is owner-gated · **DEFERRED** = declared/reserved, not
populated · **PROPOSED** = design/idea, no code.

**Posture rule (applies to every field):** a stat carries a **value AND a typed
availability posture** — `observed / unavailable_with_reason / out_of_capture_window
/ not_attempted / not_applicable` — coupled so a number exists only when posture is
`observed`. **Missing is never `0`**; a non-observed field is never ranked or averaged
as zero. Authority: `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`.

## Layer 1 — Grid capture (cheap, broad heartbeat over the whole profile)

Owning spec: `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md`.
Typed value+posture contract (**proposed**, not yet built): `.../instagram/ig_capture_shape_contract_spec_v0.md`.

**Per grid item (reel / post):**

| Field | Reliability | Source |
| --- | --- | --- |
| `view_count` | reliably visible on clean rows; sometimes hidden (typed, not `0`) | grid DOM view text |
| `like_count` / `comment_count` | **SOFT** — inferred from unlabeled DOM hidden leaves (positional heuristic); can be `ambiguous_hidden_numeric` | grid DOM hidden leaves |
| `shortcode` / permalink / `kind` (reel·post) | reliably observed (identity) | grid DOM |
| caption text | **conditional** — passive-JSON join by shortcode; else null | `edge_media_to_caption` JSON |
| publication date (`taken_at`) | **conditional** — passive-JSON join; else honest null (never guessed from grid order) | passive JSON |
| `product_type` / `is_video` / `__typename` | JSON candidate | passive JSON |
| paid-partnership / affiliate / sponsor | **CANDIDATE only** ("false" ≠ "not an ad") | passive JSON |
| pinned (clips-tab / timeline) | JSON only (no DOM marker) | `/clips/user`, `web_profile_info` |
| `view_count` on static / carousel posts | `not_applicable` (distinct from `0` / missing) | — |

**Per account (profile header):** handle + `numeric_id` observed; `follower_count`,
`bio`, `external_url`, `bio_links`, following/post counts are **schema targets whose
reliability the probe did not confirm** — named, not proven.

**View-count endpoint reconciliation (decided):** the grid DOM view text and
`/api/v1/clips/user/` **agree** and are authoritative for the *current* view;
`web_profile_info` under-reports current view but is the **deep-history** source
(the only surface that paginates back years logged-out). Example reel `DZ4Stb5MVPB`
(@jeremyfragrance): DOM/clips **2,984** vs web_profile_info **655**. **Never merge** —
tag every number by `source_surface`; record disagreements. Open confirm-probe and
the formal rule live in the proposed-stats design lane / the grid capture-shape
contract. Deep-history route source: `.../instagram/ig_reel_viewcount_capture_feasibility_recon_v0.md`.

## Layer 2 — Deep capture (earned depth; selected / promoted items only)

| Signal | Status | Source |
| --- | --- | --- |
| **Transcript (ASR)** — timed cues + per-segment confidence | **LIVE (offline)** | `.../instagram/ig_reels_transcript_product_extraction_spec_v0.md` (Reels have no caption API → audio→whisper) |
| **Product / brand / category mentions** — transcript → `ProductMention` → `silver__cleaning__product_mentions` | **LIVE (offline)** | same spec; core inherited from `.../youtube/youtube_transcript_product_extraction_spec_v0.md` |
| **No-product reel** → `ProductMention: []` but an extraction record with `mention_count: 0` (typed absence, not silence) | **LIVE** | youtube spec D5 ("return `[]` when no product named"); `forseti-harness/cleaning/transcript_product_lake.py` |
| Caption / hashtags / comment post-text | **separate seam** (`audience_extractor` / `audience_post_packet`), not the transcript path | `.../instagram/README.md` route map |
| Audio bytes (`.m4a` + sha256, for ASR) | **LIVE** | `.../instagram/ig_reels_audio_capture_recipe_card_v0.md` (no IG sound-object id/artist) |
| Top comments (text/count) | lane exists | `.../instagram/README.md` deep-capture row |

Honest edges: a **sung** brand name can become a false mention (speech/music split
deferred); login-walled reels are a typed skip (`access_gated`); **one reel per call,
attended — no at-scale crawl**.

## Layer 3 — Derived computations (on top of grid + deep)

| Computation | What it produces | Status | Source |
| --- | --- | --- | --- |
| **Metric rollups** (Silver) | `average_views`, `median_views`, `engagement_rate`, `average_like_count`, `average_comment_count` | **LIVE** (IG/YouTube; TikTok in harness, not yet in committed profile-current view) | `.../creator_registry/creator_metric_silver_record_contract_v0.md`; `forseti-harness/capture_spine/creator_profile_current/*.py` |
| ↳ `posting_cadence`, `recent_velocity` | rate / trend fields | **DEFERRED** (schema-reserved, always `not_attempted`) | `.../creator_registry/creator_profile_current_record_contract_v0.md`; `.../creator_profile_current/rollup_formula_revalidation.py` (`_NEVER_COMPUTED_METRICS`) |
| **Ideal-audience profile** (content-fit) | per pillar: `segment`, `audience_role`, `purchase_intent`, `skill_level`, `price_tier` + support bands + evidence | **BUILT·gated** (Pass-1 LLM extractor + Pass-2 deterministic fusion + snapshot + runner; live LLM wiring gated) | `.../instagram/ig_creator_ideal_audience_inference_spec_v0.md`; `forseti-harness/scoring/audience_fusion.py`; `.../creator_profile_current/ideal_audience_snapshot.py`; `forseti-harness/cleaning/audience_extractor.py` |
| ↳ audience `gender_skew` / `age_band` (Tier-2A) | demographic skew | **DEFERRED** (owner-gated behind ledger-schema home) | same spec §Tier-2-A; `forseti-harness/schemas/audience_inference_models.py` |
| ↳ **actual** audience / follower demographics | — | **never** (`actual_audience` hardcoded `not_estimated`) | `forseti-harness/schemas/audience_inference_models.py` |
| **Creator-gender lean** | one soft `gender_lean ∈ [-1,1]` + confidence; **creator-only, never per-commenter** | **BUILT** (deterministic core); cue inference DEFERRED | `forseti-harness/scoring/creator_gender_fusion.py`; `docs/decisions/ig_creator_gender_demographic_signal_lane_scope_defer_v0.md` |
| **Product-verdict fusion** | per (brand, line): verdict {positive/negative/mixed/unknown} + support/oppose scores; **no** engagement/demand meaning | **BUILT** (calibration owner-pending) | `forseti-harness/scoring/product_fusion.py`; `docs/decisions/product_verdict_fusion_calibration_surface_v0.md` |
| **Share of voice** | brand/line share of **captured mentions** (not market total) | **LIVE** (bounded readout) | `forseti-harness/data_lake/sov_readout.py`; `.../data_lake/authority/core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md` |
| **Wind-calling / momentum / breakout score** | — | **PROPOSED** (today capture-only; "momentum" code is a raw parser marked `does_not_certify_momentum`) | `.../instagram/ig_wind_caller_calls_capture_build_architecture_v0.md`; `forseti-harness/source_capture/ig_momentum_harvest.py`, `ig_projection.py` |
| **Sub-niche classifier** | topic label | **PROPOSED** (zero code; intended owner = ontology `SubNiche`, awaiting dispatch) | `.../instagram/ig_creator_discovery_spec_v0.md` |
| **Video-format stat (two-axis)** | `format_label` + `product_density` + per-product `mention_count` (emphasis) | **PROPOSED** (in the design lane) | handoff: `docs/workflows/aphrodite_proposed_creator_stats_design_handoff_v0.md` (packet never committed; lane discharged by the design spec on PR #787) |
| **Temporal / event stats** — SMA, EMA, compatible-window velocity, capture-window delta, spike, breakout, decay/plateau, active-watch expiry | — | **PROPOSED** | inventory + handoff (above) |

### The governing gate for every derived claim

`forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md`
— any derived claim must carry `source_refs`, `extraction_model`,
`extraction_recipe_version`, `input_content_hash`, `extraction_timestamp`, `receipt`,
`confidence_or_abstention`, or it **withholds** (never zero-fills). Forbidden regardless
of provenance: person-level identity/demographics, unstamped/LLM-only claims, a single
vanity score, paid/unpaid or stealth-ad verdicts.

### Where it all surfaces to a buyer/operator

`forseti/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md`
(owner-accepted) — stitches identity + aggregate influence + ideal-audience + freshness
+ limitations + drill-back; a "wind-calling / creator-fit summary" is allowed only as an
operator summary over stamped inputs (never buyer proof, outreach, or lead list).

## Two working principles to carry (they recur in every "can we track X?" question)

1. **Emphasis ≠ demand.** How often a creator names a product is the *creator's*
   behavior; demand needs *observed audience* response (views/comments/saves), never
   inferred from repetition. High emphasis + missing disclosure = a review-candidate
   *"possible undisclosed push"* flag only, never a paid/stealth-ad verdict.
2. **Format and product-density are separate axes.** A GRWM (format) is usually
   product-dense (skincare / finishing fragrance); a storytime usually isn't. Track both
   and the interaction (format × product-density × observed success, per creator).

## Related maps

- Broader capture-surface + metric-family inventory (all source families, not just creator): `docs/research/aphrodite_silver_metric_monitoring_inventory_v0.md`.
- Capture strategy (grid heartbeat, deep-capture promotion, budget): `docs/research/aphrodite_creator_capture_strategy_v0.md`.
- Proposed-stats design lane (temporal/event stats, wind-calling, sub-niche, video-format): `docs/workflows/aphrodite_proposed_creator_stats_design_handoff_v0.md` (packet never committed; lane discharged by the design spec on PR #787).
