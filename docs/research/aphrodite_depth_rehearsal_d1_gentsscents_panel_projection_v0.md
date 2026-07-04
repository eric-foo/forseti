# Aphrodite Depth Rehearsal - D-1 GentsScents Panel Projection v0

```yaml
retrieval_header_version: 1
artifact_role: Research record (five-panel D-1 projection for GentsScents; evidence posture, not score or readiness)
scope: >
  Renders the D-1 GentsScents claim record into the Aphrodite five-panel depth
  layer for a synthetic skeptical dupe-first buyer, preserving show/downgrade/
  withhold states and explicit non-claims.
use_when:
  - Reading the D-1 GentsScents panel output without parsing the JSON claim record first.
  - Reviewing whether the panel layer preserves provenance and abstentions.
authority_boundary: retrieval_only
open_next:
  - docs/research/aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json
  - docs/research/aphrodite_depth_rehearsal_d1_gentsscents_grade_v0.md
  - docs/review-inputs/aphrodite_depth_rehearsal_d1_gentsscents_adversarial_review_input_v0.md
stale_if:
  - The claim record is amended.
  - A cross-vendor adversarial review requires patching this projection.
```

## Status

`D1_PANEL_PROJECTION_V0_POST_REVIEW_PATCH` - product-learning evidence posture only. This artifact has no score and does not fire D-1. It incorporates the home-lane response to review findings AR-01 through AR-06 from `docs/review-outputs/adversarial-artifact-reviews/aphrodite_depth_rehearsal_d1_gentsscents_adversarial_artifact_review_v0.md`.

Reading order for the locked buyer profile: fit and dupe posture first, then brand adjacency, purchase intent, ad reception, and momentum.

## Buyer Frame

The buyer is synthetic but skeptical: a dupe-first or clone-house operator who cares about whether GentsScents can reveal demand around Dior Sauvage, Creed Aventus, and adjacent clone/original shopping behavior. The buyer is not assumed to buy because direct originals appear; the projection must preserve what is missing.

Candidate-set intake is now structured in the claim record: the buyer segment, house tier, target originals, note-family targets, occasion targets, and target tier position all carry `intake_source_state` or an explicit withheld state. This is still synthetic intake, not market proof.

## Panel 1 - Fit and Dupe Posture

| Fit element | State | Projection |
|---|---|---|
| Corpus topicality | `show` | 15/15 selected videos are fragrance topical inside the bounded GentsScents window. |
| Product segment presence | `downgrade` | Round-2 SoV shows 417 raw product mentions, 415 deduped mentions, 340 distinct products, and a 55-mention low-confidence tail. It is useful but still rehearsal-grade. |
| Presence x attention x stance | `downgrade` | Direct-original attention exists for both buyer anchors: Creed Aventus (5 videos, 183,116 attention views, 1.2%) and Dior Sauvage (5 videos, 167,049 attention views, 1.1%). Stance remains operator-coded rehearsal evidence. |
| Note-family overlap | `downgrade` | All 10 buyer target note families are rendered explicitly as chips in the claim record. None are silently dropped. Each is marked aggregate-receipt-only because the branch still lacks committed per-mention transcript receipts behind the SoV aggregates. |
| Tier alignment | `downgrade` | The row is narrowed to a top-8 resolved-product tier view plus buyer-anchor tier comparison. Top-8 attention is 85.7% designer and 14.3% niche; this is not the ratified full 340-product six-tier distribution. |
| Direct-original attention | `downgrade` | The buyer's originals are present in aggregate SoV rows, but per-mention transcript receipts are not committed in this branch. |
| Clone-tail or dupe-space roll-up | `withhold` | Dupe-space roll-up withheld: the ontology contains no citable dupe relationships for this capture/version. Direct original mentions are shown where available. This is not evidence of zero clone demand. |
| Comparable baseline | `downgrade` | Mainstream comparable products such as YSL Y EDP, Bleu de Chanel, Coach for Men, Invictus Parfum, and Versace Pour Homme appear, but only as same-window affiliate-heavy evidence. |
| Attention concentration | `downgrade` | The corpus appears diffuse from aggregate SoV rows: 340 distinct products, 85% appearing in only one video, with the top single product at 1.3% attention share. This remains aggregate-table supported. |
| Niche trajectory | `withhold` | Single capture cycle. |
| Unresolved product tail | `downgrade` | 55/417 low-confidence mentions, mostly clone/niche tail, are disclosed instead of silently disappearing. |

Fit read for the skeptical buyer: GentsScents is credible enough to inspect for original-reference adjacency around Aventus/Sauvage, but the fit panel is not drill-back complete. The current evidence does not yet prove clone-house demand capture because the dupe graph is empty, the unresolved tail sits exactly where the buyer cares most, and the SoV-derived fit rows still terminate at aggregate tables rather than per-mention transcript receipts.

## Panel 2 - Brand Adjacency

| Adjacency element | State | Projection |
|---|---|---|
| Adjacent product presence | `downgrade` | Aventus, Sauvage, Bleu de Chanel, and YSL Y EDP are present, but organic posture is not proven because the selected videos are link-bearing. |
| Similarity to buyer coordinates | `downgrade` | Tier and note-family similarity is reference-derived; clone-house similarity is withheld without `dupe_relationships`. |
| Organic attention and stance | `withhold` | No clean unpaid subset exists in the bounded corpus. |
| Comparable brand baseline | `downgrade` | Same-window comparables exist, but there is no historical creator baseline and no organic-only baseline. |

Adjacency read: the channel is adjacent to the buyer's original-reference space, but the proof is not yet the buyer's clone-house space.

## Panel 3 - Purchase Intent

| Intent element | State | Projection |
|---|---|---|
| Product-resolved counts | `downgrade` | Example product-binding receipts exist, but the run does not claim an exhaustive product-resolved intent table. |
| Engagement-weighted support | `show` | Raw counts and `sum(like_count)` are kept separate: future-buy 23/130, bought 36/264, dupe/clone 42/211, comparison shopping 15/104, price objection 9/61, where-to-buy 3/8. |
| Aggregate unresolved texture | `show` | Visible comments contain buyer-relevant buying, dupe, comparison, and price language even when not safely product-resolved. |
| Sample limitation | `show` | Current parse saw 600 visible comments; round-2 counted 591. Both are visible/top-sort samples, not full audience prevalence. |

Intent read: the comments are materially interesting for a dupe-first buyer, especially the 42 dupe/clone comments, but the product-specific path remains under-proven.

## Panel 4 - Ad Reception

| Ad element | State | Projection |
|---|---|---|
| Video disclosure class | `show` | 15/15 selected videos are link-bearing; paid-content overlay count was not observed. |
| Affiliate link inventory | `show` | Round-2 exact count is 85 affiliate links across the 15-video set. |
| Load mix | `show` | The window is affiliate-heavy. |
| Matched reception pair | `withhold` | No clean organic paired comparator exists inside the bounded corpus. |
| Reception delta | `downgrade` | The corpus has 552,859 total views and 26,305 total likes, but ad-class delta is confounded. |
| Comment texture by class | `downgrade` | Buying/dupe/price texture exists under link-bearing videos, but class-specific comparison is unavailable. |

Ad read: the channel can expose commercial-context audience behavior, but this slice cannot answer whether affiliate or sponsored posture depresses or improves reception relative to organic content.

## Panel 5 - Momentum

| Momentum element | State | Projection |
|---|---|---|
| Capture window state | `show` | 15 videos from a single publish window, captured from existing packet reads. |
| View/engagement moving average | `withhold` | Requires at least two capture cycles. |
| Follower delta | `withhold` | Follower registry/current-view projection was not run and only one observation exists. |
| Breakout frequency | `withhold` | No historical baseline or multi-cycle denominator. |
| Fit-relevant participation | `withhold` | Fit-relevant signals exist in the window but repeated participation over time is unavailable. |

Momentum read: nothing in this run should be read as trend. It only establishes that the selected corpus has enough cross-sectional content to rehearse the panel mechanics.

## D-1 Projection

This is a credible dress-rehearsal packet, not a pass. The first cross-vendor review returned `NOT_BLOCKER_MAJOR_FREE` with four major findings. This patch responds by downgrading aggregate-only fit claims, rendering note-family chips explicitly, narrowing the tier row scope, and adding structured buyer intake. Criterion 5 remains unobserved until a cross-vendor recheck or explicit home-lane adjudication accepts the patch response as blocker/major-free. Same-family review would be a fake pass.

## Non-Claims

- No panel score, rank, or readiness label.
- No buyer conversion, willingness-to-pay, or purchase proof.
- No dupe-space roll-up beyond direct-original mentions.
- No organic ad-reception delta.
- No momentum trend.
