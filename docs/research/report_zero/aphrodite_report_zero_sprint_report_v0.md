# Aphrodite Report Zero — Rehearsal Vetting Sprint Report (GentsScents)

```yaml
retrieval_header_version: 1
artifact_role: Research record (D-1 dress-rehearsal sprint report — the five-panel projection over the frozen GentsScents corpus for a SYNTHETIC buyer; product_learning-capped)
scope: >
  Report #0: the full five-panel Vetting Sprint report rendered from the
  Report Zero derived claims (recipe v1, model-in-session, no API key) for the
  synthetic dupe-first clone-house buyer. This is the rehearsal deliverable the
  D-1 gate grades — a real report shape over real captured data for a buyer who
  is explicitly synthetic. Display rules per the panel design record; claim
  discipline per the derived-claim provenance contract.
use_when:
  - Grading the D-1 dress rehearsal (charter section 7 gate 3).
  - Reviewing what a Vetting Sprint report looks like when produced end-to-end.
authority_boundary: retrieval_only
open_next:
  - docs/research/report_zero/aphrodite_report_zero_derived_claims_v1.json
  - docs/research/aphrodite_report_zero_corpus_v0.md
  - docs/research/aphrodite_depth_rehearsal_extraction_recipe_v1.md
stale_if:
  - A later capture cycle supersedes this corpus for rehearsal use.
  - The panel design record or provenance contract is amended.
```

**BUYER IS SYNTHETIC.** This report exercises the candidate-set intake with the
adjudicated synthetic dupe-first clone-house profile
(`aphrodite_report_zero_buyer_intake_v0.yaml`, sha256 `3adf664b…`): a
clone-house whose target originals are `product:creed.aventus` and
`product:dior.sauvage`, required note families citrus/woody/fresh/spicy,
occasions versatile/daily/office. No real buyer was contacted. Every number
below is a claim object in
`aphrodite_report_zero_derived_claims_v1.json` (corpus hash `0362007e…`,
recipe `aphrodite-rehearsal-extraction-v1`, model `claude-fable-5`,
2026-07-10); receipts drill back to
`docs/research/report_zero/<video_id>.coded.json` and, transitively, the
canonical lake packets.

**Subject:** GentsScents — YouTube long-form fragrance reviewer
(`UC9IImcLkUdmURWtQhxu8VwQ`, registry `acct_yt_fragrance_010`).
**Corpus:** 15 most-recent videos, 2026-06-19 → 07-02 (daily cadence),
552,859 views at capture, 53,749 transcript words, 600 page-1 comments.
**Reading order:** dupe-first buyer variant — fit → brand adjacency →
purchase-intent → ad-reception → momentum (panel design §6).

---

## Panel 1 — Fit (the lead panel)

| Row | Posture | Read |
| --- | --- | --- |
| Segment share | **show** | 15/15 recent videos are fragrance-topical (8 rankings, 3 reviews, 2 clone-guides, 1 counterfeit-exposure, 1 release-intel). This is a fragrance-only channel, not a general-beauty drive-by. |
| Presence × attention × stance — **your target originals** | **show** | `creed.aventus`: attention in 5/15 videos (171K captured views) — but **zero dedicated review segments**; it appears exclusively as the clone economy's reference point ("the archetype most-cloned"; "when you want that Aventus vibe for cheap, Explorer's the one" — 8QpC36Q_eeM@181040). `dior.sauvage`: 7/15 videos (284K views, 51% of corpus attention), with **direct positive review segments** (S-tier ctcEju1AvGw@1161520; "one of the best ones ever made" sw34VzzWlvA@777120) *plus* clone-target attention. |
| Note-family overlap | **show** | All 8 of your intake families observed with receipts. The channel's dominant "blue/fresh" discourse sits squarely on your required citrus/woody/fresh/spicy. Chips: citrus ✓ woody ✓ fresh ✓ spicy ✓ · fruity ✓ sweet ✓ amber ✓ aromatic ✓ (each backed by resolved products' reference coordinates, attention-weighted). |
| Tier alignment | **show** (M1: rubric-classified, provenance visible) | Resolved mentions skew designer (9/11 observed products); niche = Aventus/Aventus-Absolu (comparative-only); luxury = LV Imagination. **Honest inversion:** the *unresolved* tail is overwhelmingly clone-house — reference v0 carries no clone-house products, so your own tier's discourse (which dominates this channel) is excluded from resolved rollups. Resolved coverage: 11/16 reference products; <10% of all distinct products mentioned. |
| Dupe-space adjacency | see Panel 2 block below | Direct-original evidence **show**; clone-tail roll-up **withhold** (empty graph). |
| Comparable-brand baseline (within-window, M4a) | **show** (medium) | Your category's content (clone-primary videos, 5-6/15) runs ~0.84× the channel's mean views but carries the **highest purchase-intent density** (up to ~45% intent-bearing comments on a single-product clone review vs ~0 on a giveaway ranking). On this channel, your category trades reach for conversion-shaped engagement. |
| Attention concentration (gameability check) | **show** | Top video = 11.7% of corpus views; top-3 = 30.7%. Broadly supported; not one-viral-video inflated. |
| Niche-share trajectory | **withhold** | Single capture cycle — no trend claim. Missing: a second capture window. |
| Unresolved mentions (coverage honesty) | **show** | ~150+ distinct products mentioned; the clone-house tail (Rasasi/Hawas, Armaf, Lattafa, Afnan, Maison Alhambra, French Avenue, Nusuk, Zimaya…) is deliberately excluded-pending-source in reference v0. Tier/note rollups above are computed over resolved mentions only. |

## Panel 2 — Dupe-space & organic brand adjacency (your lead follow-on)

**Direct Original block (show):**
- **Aventus demand-space:** the richest dupe-discourse object in the corpus.
  The creator adjudicates *which-original-to-chase* decisions around it: Kaaf
  Noir graded down for picking K over Aventus ("90% K and 10% [Aventus], if
  that… if there was more Aventus than K, that would have been a more
  interesting proposal" — _FUdh1ryqWI@699640/@814800); Montblanc Explorer
  positioned as the value pick; "a boatload of clones" acknowledged; CDN-Absolu
  speculated as Absolute-Aventus. **Read for you:** Aventus demand-space
  attention is abundant and mediated through clones — precisely your market.
- **Sauvage demand-space:** strong direct original attention (positive) + clone
  coverage (Zenith Blue) + the flanker trend-analysis (Sauvage Elixir ranked #1
  and credited with creating the elixir wave — hzqxkp3OqQw@1006480).

**Clone Tail block (withhold — honest absence):**
> Dupe-space roll-up withheld: the ontology contains no citable dupe
> relationships for this capture/version. Direct original mentions are shown
> where available. **This is not evidence of zero clone demand.**

(Observed-but-unmintable: the corpus *asserts* 25+ dupe relations in creator
and audience speech — Explorer→Aventus, Apollo→Y EDP, M→BdC, Gold Digger→Ultra
Male… — citable as discourse, not as graph edges.)

**Organic adjacency (show; gifted video downgraded out):** the creator
self-funds haul-scale coverage of your exact category ("$300 blind buying a ton
of cheap clone fragrances" — tVUqAYGT3SE@7160), grades clone quality honestly
(positive Dunescape/Concordia/Gladius; negative Hawas Chrome; tiered
Pierce > Luminous Vivid > Art of Wood for one original), and performs
market-timing analysis of clone-house target selection ("coming out with
alternatives years after all the other brands… you already own 9PM… who cares"
— nySgot9sqMY@385640). Stance is graded, never promotional: presence ≠
endorsement.

## Panel 3 — Audience purchase-intent (aggregate only)

| Signal | Raw count | Liked support (separate, M2) | Posture |
| --- | --- | --- | --- |
| Bought-because-of-creator | 12 | ~35 (top 8) | **show** |
| Dupe requests | 12 | **~170** (top 63, 40, 35) | **show** |
| Future-buy / watchlist | 30 | — | **show** |
| Where-to-buy | 4 | — | **show** |
| Comparison shopping | 4 | — | **show** |
| Price objections | 3 | 21 top | **show** |
| Ownership reports | ~150 | — | **show** |

Highlights for a clone-house buyer: dupe requests are the **most-liked intent
class** — the audience petitions clone houses through this channel, twice
naming Y EDP as the wanted target. Conversion evidence is explicit and
repeated ("purchased… the day I saw this video"; "Because of this channel, I
bought [3 products]"; "collection… approaching the mighty 100 mark") and
includes **decision-gating** ("I purposely waited for you to rate it… to make
a decision" — the review is the purchase gate). Texture: collector scale
(13–100+ bottles), clone-preservation economics, decant→bottle funnels,
gift-buyer personas, and the audience running its own dupe-similarity grading
("8/10 similarity to Profumo — it's lacking some incense").

**Limitation (always shown):** page-1 top-sort only, 40/video (600 of 3,231+
available); moderation invisible; 3 videos carry giveaway prompts that direct
comment content; no platform comment_id in capture (positional refs).

## Panel 4 — Sponsorship load & ad reception

- **Disclosure classes (show):** 14/15 affiliate-or-self-brand · 1/15
  gifted-PR-candidate (retailer-supplied bottle + that retailer's own code —
  ambiguity carried) · 0 paid detected (platform paid flag `not_captured` —
  absence is not organic proof).
- **Load (downgrade — no organic contrast class exists):** 100% of videos carry
  affiliate monetization (gentsscents.me across a ~9-discounter network); ~40%
  also promote the creator's **own fragrance line** (Michael Malul: Arashi
  Reef, French Quarter, Terranova); concentration is in the creator's own
  funnel, not a third-party sponsor.
- **Hygiene (show):** verbal disclosure segments in every video; "Biased choice
  alert" before pitching his own product; **killed a partner's discount code
  on-air** over fulfilment trust; audits eBay counterfeits by buying fakes with
  his own money. Comment texture rewards it: "most genuine and trustworthy of
  the influencers in this space."
- **Reception (matched pairs withhold; within-window contrast downgraded, n=1
  per class):** no sponsored-vs-organic pair can be formed in an all-affiliate
  corpus. Format, not disclosure class, drives reach here: rankings 64.8K >
  news 53.8K > wife-collab 51.9K > clone reviews ~25–36K > counterfeit exposure
  20.7K (lowest reach, highest trust texture).

## Panel 5 — Momentum

**Show-as-withhold (single capture cycle).** Window state: videos 2026-06-19 →
07-02, captured 2026-07-04; **no second window exists yet**, so moving
averages, subscriber deltas, breakout frequency, and fit-participation trend
are all withheld rather than faked. Observed single-window facts (metrics, not
momentum): daily upload cadence; per-video views 20.7K–64.8K around a 36.9K
mean; clone-primary content 5-6/15. A second capture cycle would convert these
into momentum reads.

---

## Candidate-set intake exercise (D-1 criterion 4 — what the intake needed)

Exercised with the synthetic intake object (hashed input, `3adf664b…`).
What worked: both `dupe_target_originals` resolved against the reference
(`product:creed.aventus`, `product:dior.sauvage`) and their note families /
tiers drove the fit chips and demand-space blocks; occasion vocabulary covered
the buyer's values. **What the intake needed that did not exist:**
1. `dupe_relationships` — empty in reference v0, so the clone-tail block the
   dupe-first buyer most wants renders as honest absence (known residual R1).
2. A clone-house product tail in the reference — the buyer's *competitive set*
   (other clone houses' products) is unresolvable, so competitive-clone
   attention can only be shown as unresolved discourse.
3. A second capture cycle — the buyer's "is this lane saturating?" question is
   exactly a trajectory/momentum read; single-cycle data can only show current
   state.

## The decision read (what this report supports — and declines)

For this synthetic dupe-first buyer, the evidence supports: **this creator is a
high-fit channel for clone-house creator spend** — category-exact organic
coverage, the strongest dupe-request audience observed anywhere in the corpus,
explicit purchase conversion, and decision-gating influence — **with the named
caveats** that reach on clone content runs below the channel's own mean, the
channel monetizes via affiliate on everything (no organic baseline), and
saturation/momentum questions are unanswerable until a second capture cycle.
Per the panel design §7, this report deliberately does **not** answer "should
I pay this creator now, at what rate" — that synthesis belongs to the readback
and the buyer's own economics.

## Non-claims

`product_learning`-capped. Not validation, readiness, buyer proof, or
willingness-to-pay evidence; the buyer is synthetic; grades are the extraction
model's coded reads over captured public content; audience comments are
commenters' claims, not verified facts; no dupe edges minted; no person-level
claims (comment authors dropped at normalization); D-1 gate firing is graded
separately, not claimed here.
