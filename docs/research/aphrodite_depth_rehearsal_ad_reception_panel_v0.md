# Aphrodite Depth Rehearsal — Sponsorship Load + Ad Reception Panel v0 (jeremyfragrance, IG)

```yaml
retrieval_header_version: 1
artifact_role: Research record (rehearsal panel rendering — evidence lane; NOT a customer surface, NOT decision-grade)
scope: >
  The rehearsal rendering of charter Section 4 panel 2 (sponsorship load + ad
  reception) for one creator, built exclusively from the frozen corpus's
  derived claim objects. Every shown fact cites a claim_id; the core
  sponsored-vs-organic comparison is honestly downgraded because zero
  third-party sponsored items exist in the corpus. Exists to be graded.
use_when:
  - Grading the depth rehearsal (see the grade doc).
  - Seeing which ad-reception components the current capture substrate can and cannot power.
authority_boundary: retrieval_only
open_next:
  - docs/research/aphrodite_depth_rehearsal_derived_claims_v0.json
  - docs/research/aphrodite_depth_rehearsal_grade_v0.md
stale_if:
  - The derived-claims JSON or frozen corpus is superseded.
```

Creator: **jeremyfragrance (Instagram)** · Corpus: 12 reels, 2026-06-27→29 ·
Claims bound to `aphrodite_derived_claim_provenance_contract_v0.md`; drill back
via `claim_id`.

## 1. Sponsorship detection (per reel) — SHOWN

12 per-reel classifications emitted (`claims: ad.detection.<shortcode>.v0`),
each with confidence and verbatim receipt:

| Reel | Classification | Confidence | State |
|---|---|---|---|
| DaGUhsKsYL9 | gifted_invite_candidate + self_brand_commerce | 0.7 / 0.9 | show |
| DaH3L1Isdrc | self_brand_commerce (in editorial top-10) | 0.85 | show |
| DaINMZCCb6N | gifted_invite_candidate (brand-voiced acknowledgement) | 0.5 | downgrade |
| DaIr5aRsp8p | self_brand_commerce | 0.9 | show |
| DaK3uKxBlKy | gifted_invite_candidate + self_brand_commerce | 0.75 / 0.9 | show |
| DaKd8E9skt8 | gifted_invite_candidate + self_brand_commerce | 0.75 / 0.9 | show |
| DaKeXcVM0sx | self_brand_commerce (discount code) | 0.95 | show |
| DaKkwCiB_2B | self_brand_commerce (discount code) | 0.95 | show |
| DaKkXGQBE9i | gifted_invite_candidate + self_brand + ambiguous third-party promo dialog | 0.6 | downgrade |
| DaLBhRbskFa | self_brand_commerce | 0.9 | show |
| DaLBRQiMJhQ | organic | 0.8 | show |
| DaLK8b9s9z9 | gifted_invite_candidate + self_brand + host cross-promotion | 0.75 | show |

Platform signals: `is_paid_partnership` false/null on all 12; `sponsor_users`
and `ad_term_candidates` empty on all 12.

## 2. Sponsorship load — SHOWN

**Commercial density very high but self-directed: 11/12 reels carry a
commercial marker; 0/12 platform-labeled paid partnerships; one candidate
gifting relationship (Nike Schroeder / Forte Village, 5 reels). Disclosure
hygiene: the hosted-trip cluster has no #ad/#sponsored/platform label — only
informal caption thanks.** `claim: ad.load.v0` · confidence medium-high.

## 3. Ad reception (sponsored vs organic) — DOWNGRADED

**Directional only: hosted-trip reels underperform the rest on median plays
(3,153 vs 4,981) and likes (110 vs 141) — confounded, tiny n, one snapshot.**
`claim: ad.reception.v0` · confidence low.

The charter-defined comparison (third-party sponsored vs matched organic pairs,
including comment texture) is **not possible on this corpus**: zero third-party
sponsored items exist. That absence is the panel's principal finding, not a gap
to be papered over.

## Panel limitations (named, per contract)

- Gifted-candidate labels are inferred from captions/speech/comments, not
  platform-verified; gifting ambiguity is carried per the charter's named
  limitation.
- Play/like counts are one observed snapshot at capture time (2026-06-29),
  ~0.3–2 days after posting; late-arriving engagement is invisible.
- Small n per class (5 vs 7); same-week posting; persona-content confound
  (one 156K-play dance reel dominates the non-cluster median).
- Comment-texture comparison between classes not emitted: per-class non-empty
  comment counts (~30 vs ~34) are too small to separate honestly.

## Non-claims

Not decision-grade, not a customer surface, not validation, not proof of
sponsorship or of ad underperformance; `product_learning`-capped.
