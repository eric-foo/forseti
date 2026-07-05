# Aphrodite Depth Rehearsal — Fit Evidence Panel v0 (jeremyfragrance, IG)

```yaml
retrieval_header_version: 1
artifact_role: Research record (rehearsal panel rendering — evidence lane; NOT a customer surface, NOT decision-grade)
scope: >
  The rehearsal rendering of charter Section 4 panel 1 (fit evidence) for one
  creator, built exclusively from the frozen corpus's derived claim objects.
  Every shown fact cites a claim_id in the derived-claims JSON; withheld
  components are shown as withheld. Exists to be graded, not to be used.
use_when:
  - Grading the depth rehearsal (see the grade doc).
  - Seeing what a fit panel looks like when honestly rendered from thin substrate.
authority_boundary: retrieval_only
open_next:
  - docs/research/aphrodite_depth_rehearsal_derived_claims_v0.json
  - docs/research/aphrodite_depth_rehearsal_grade_v0.md
stale_if:
  - The derived-claims JSON or frozen corpus is superseded.
```

Creator: **jeremyfragrance (Instagram)** · Corpus: 12 reels, 2026-06-27→29 ·
All values below are derived claims bound to
`aphrodite_derived_claim_provenance_contract_v0.md`; drill back via `claim_id`
into `aphrodite_depth_rehearsal_derived_claims_v0.json`.

## 1. Segment share of recent content — SHOWN

**12/12 recent reels are fragrance-framed; but at least 5/12 are persona/dance-led
with fragrance as the frame, not review content.**
`claim: fit.segment_share.v0` · confidence medium-high · window: one week,
recent stratum only.

## 2. Price-tier distribution of products mentioned — SHOWN (partial)

**Self-brand dominates: 9/12 captions carry Fragrance One commerce.** Distinct
third-party products: 8 resolved (6 designer, 2 niche/luxury), concentrated in
2 of 12 reels; 2 niche candidates unresolved (abstained, not guessed).
`claim: fit.product_tier_distribution.v0` · confidence medium-high · price
tiers are operator-assigned, not derived.

**Note-family distribution — WITHHELD** (2 note terms in the whole corpus;
a distribution would be fabrication). Carried inside
`fit.product_tier_distribution.v0`.

## 3. Audience taste from comment language — SHOWN (heavy limitations)

**Page-1 texture is persona-driven and majority-critical: ~53% critical/mocking,
~27% supportive, ~20% neutral of 64 non-empty comments; collector, dupe-seeker,
and purchase-intent language absent (0 instances).**
`claim: fit.audience_taste_texture.v0` · confidence medium · aggregate only ·
severe page-1 skew (one reel: 15 of 215 comments visible).

## 4. Proven adjacency (comparable-brand performance vs own baseline) — WITHHELD

`claim: fit.proven_adjacency.v0` · insufficient evidence: no comparable-brand
content series and no performance history in a single capture cycle.

## 5. Niche-share trajectory — WITHHELD

`claim: fit.niche_share_trajectory.v0` · insufficient evidence: one capture
cycle; a trajectory needs at least two.

## Panel limitations (named, per contract)

- 2 of 5 panel components withheld; 1 shown partial. This panel is **not
  decision-grade** (see grade doc).
- IG Reels short-form only — no long-form review discourse exists in the lake
  for this creator; segment/product reads do not represent YouTube behavior.
- Single week, single capture cycle, recent-window stratum only.
- ASR quality caps entity recall (2 products unresolvable; 1 reel's transcript
  unusable).

## Non-claims

Not decision-grade, not a customer surface, not validation, not buyer proof;
`product_learning`-capped; no person-level inference anywhere.
