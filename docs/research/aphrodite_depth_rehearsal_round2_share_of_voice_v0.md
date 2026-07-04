# Aphrodite Depth Rehearsal — Round 2 Share-of-Voice (GentsScents)

```yaml
retrieval_header_version: 1
artifact_role: Research record (share-of-voice rehearsal over captured transcripts — evidence lane, product_learning-capped; NOT a silver-lane record)
scope: >
  A share-of-voice (SoV) rehearsal over the 15 captured GentsScents YouTube
  transcripts: an operator-assisted product-mention extraction, then two SoV
  computations — unweighted editorial SoV and view-weighted attention SoV —
  plus the gap between them. Built to answer the owner's methodology question
  (is SoV accurate if you only take top performers?) and to demonstrate the
  fit-panel product-tier / share-of-voice value on real captured substrate.
  This is a rehearsal artifact in docs/research; it is NOT written into the
  silver__cleaning__product_mentions lake lane.
use_when:
  - Deciding how to compute SoV (editorial vs attention-weighted) and what to capture.
  - Seeing the fit-panel product/SoV component built on real captured substrate.
authority_boundary: retrieval_only
open_next:
  - docs/research/aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md
  - orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
stale_if:
  - A real silver-lane product-mention extraction supersedes this rehearsal.
  - The captured GentsScents corpus is superseded.
```

## Status

`SOV_REHEARSAL` — 2026-07-04, under the same owner build-authorization as the
round-2 capture. Product mentions were extracted by an **operator-assisted**
pass (delegated Sonnet worker; `extraction_model: claude-sonnet-4-5-20250929`),
matching the lake's existing `operator_codex_assisted` precedent, because the
daemon extractor needs an LLM transport/API key not present in this environment
and the subscription transport is unwired (spec Accepted Residual #6). Evidence
lane only: not validation, readiness, or buyer proof; `product_learning`-capped.

## Inputs

- 15 GentsScents transcripts (53,749 words) + per-video view counts, from the
  captured caption + watch packets (see the round-2 grade doc).
- Extraction: 417 raw product mentions (415 after intra-video dedup), each with
  brand, product, verbatim receipt, stance, resolution confidence.

## The two SoV metrics (the owner's question, resolved)

**The question:** is SoV accurate if you only take, say, the top 25% of videos?
And is "SoV of high-attention products" more valuable?

**The resolution:** don't top-slice at *capture* (that biases the denominator —
products living in median/flop videos vanish). Capture a representative set,
then compute two things at *analysis*:

- **Editorial SoV** — share of mentions, unweighted. "What the creator talks
  about." Feeds segment-share / fit.
- **Attention-weighted SoV** — each product weighted by the views of the videos
  it appears in (impressions ≈ views × mention). "What the audience is actually
  exposed to." The buyer-relevant headline.

Both are computed here from the *same* representative corpus; the view weights
came free from the captured watch metadata.

## Results — top products by attention-weighted SoV

| Product | Videos | Attention (Σ views) | Attention SoV | Editorial SoV | Gap |
| --- | --- | --- | --- | --- | --- |
| YSL Y Eau de Parfum | 5 | 199,244 | 1.3% | 1.2% | +0.1 |
| Creed Aventus | 5 | 183,116 | 1.2% | 1.2% | −0.0 |
| Chanel Bleu de Chanel | 5 | 167,049 | 1.1% | 1.2% | −0.1 |
| Dior Sauvage | 5 | 167,049 | 1.1% | 1.2% | −0.1 |
| Coach for Men | 3 | 149,248 | 0.9% | 0.7% | +0.2 |
| JPG Ultra Male | 4 | 141,980 | 0.9% | 1.0% | −0.1 |
| Paco Rabanne Invictus Parfum | 3 | 141,852 | 0.9% | 0.7% | +0.2 |
| Versace Pour Homme | 3 | 130,085 | 0.8% | 0.7% | +0.1 |

## The finding the rehearsal actually produced

1. **Over this corpus, editorial SoV ≈ attention SoV (gaps all within ±0.3pp).**
   That is *because* the 15 videos are a recent-window slice with a narrow view
   spread (20K–65K). When every video draws similar attention, weighting by
   attention barely moves the ranking. This is the empirical answer to the
   owner's question: **the "high-attention SoV" only diverges from editorial
   SoV when the corpus has real view spread** — i.e. when it mixes viral hits
   with median/flop videos. So the value of attention-weighting is *unlocked by
   capturing across the performance range* (representative window **plus** top-K
   all-time), exactly the charter's stratified capture — and is *destroyed* by
   top-25%-only capture, which flattens the spread. Top-slice at capture and you
   lose the very signal you wanted.
2. **The distribution is a long tail, not a leaderboard.** 340 distinct products
   from 415 mentions; **85% appear in only one video**. A single headline "SoV %"
   is diffuse for a broad list-reviewer (the top product is ~1.3%). The useful
   buyer unit is the **per-product triple — presence × attention × stance —**
   not a ranked SoV table: "does this creator cover MY product, in videos people
   watch, and how does he talk about it." Stance mix across the corpus: 211
   positive / 138 neutral / 20 negative / 48 unclear.
3. **This is the fit-panel product-tier component, built for real.** The round-2
   grade rated it A- pending extraction; this run *is* that extraction on real
   captured substrate, and it works.

## Honesty caveats

- **Rehearsal, not silver lane.** These mentions are NOT written into
  `silver__cleaning__product_mentions`; they live only in this rehearsal's
  scratch + this doc. Feeding the real SoV tooling needs the daemon runner (API
  key) or a YouTube operator runner (small build) — a separate owner-gated step.
- **ASR + resolution noise.** 55 of 417 mentions (~13%) are low-confidence,
  mostly Arabic/clone-house ASR garbles (Lattafa, Afnan, Ahmed Al Maghribi
  lines). The 340 distinct-product key count is inflated by unnormalized
  near-duplicate clone-name strings; the designer head (YSL, Creed, Chanel,
  Dior…) is clean and stable, the clone/niche tail is noisier.
- **Single extraction pass**, one delegated model; not a validated extractor.
  One self-caught miss during extraction (a "fake fragrances" video first
  returned 0 mentions, corrected to 16 against the transcript before inclusion).
- Views are one capture-time snapshot; attention weights shift as videos age.

## Non-claims

- Not validation, readiness, buyer proof, or willingness-to-pay evidence;
  `product_learning`-capped.
- Not a silver-lane record and not a registry/current-view update; authorizes
  no lake write, ontology build, or roster capture. FLAG 1 remains open.
