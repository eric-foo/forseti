# Aphrodite Depth Rehearsal — Round 2 Grade: GentsScents (YouTube long-form)

```yaml
retrieval_header_version: 1
artifact_role: Research record (round-2 rehearsal grade + substrate comparison — evidence lane, product_learning-capped)
scope: >
  The round-2 depth rehearsal: a second single-creator run on GentsScents
  (YouTube long-form review channel) built to test whether the round-1 D+/C-
  grades were substrate-bound (thin IG Reels) or method-bound. Records the
  owner-authorized capture (15 recent videos, caption + watch/comments each),
  the measured substrate delta vs the Jeremy corpus, and a re-grade of the fit
  and ad-reception panels against identical charter Section 4 criteria.
use_when:
  - Deciding whether the depth-layer method is worth building at roster scale.
  - Preparing the owner decision on charter D-1 (foundation exit gate).
  - Sizing which capture gaps still cap a good-creator panel.
authority_boundary: retrieval_only
open_next:
  - docs/research/aphrodite_depth_rehearsal_grade_v0.md
  - docs/research/aphrodite_depth_rehearsal_derived_claims_v0.json
  - orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
stale_if:
  - A later rehearsal or the real depth-layer build supersedes this grading.
  - The charter's panel definitions (Section 4) are amended.
```

## Status

`ROUND2_REHEARSAL_GRADE` — capture executed 2026-07-04 under owner
build-authorization granted in-turn ("you're authorized for this run"),
extending the depth-layer rehearsal to a second creator. Evidence lane only:
not validation, not readiness, not buyer proof; `product_learning`-capped.
FLAG 1 (commercial use / data rights) remains open and is untouched here.

## Why round 2 exists

Round 1 (`aphrodite_depth_rehearsal_grade_v0.md`) graded jeremyfragrance's fit
panel D+ and ad-reception C-. The owner's challenge: those grades look
worthless, and a *normal* fragrance creator's videos/comments carry far better
signal than Jeremy's persona-driven Reels. This run tests that directly by
running the **same extraction question** over a typical long-form reviewer.

Subject: **GentsScents** ("Gents Scents", `UC9IImcLkUdmURWtQhxu8VwQ`), a
registry channel. Creator Registry match preflight passed
(`existing_match` / `allowed`, receipt in the run scratch). Capture = the
recent-window stratum: 15 most-recent uploads (2026-06-19 → 07-02), each run
through the existing `run_source_capture_youtube_caption_packet.py` and
`run_source_capture_youtube_watch_packet.py` runners. All 30 runner
invocations exited 0.

## The measured substrate delta (this is the finding)

| Metric | Round 1 — jeremyfragrance (IG Reels) | Round 2 — GentsScents (YouTube) |
| --- | --- | --- |
| Items captured | 12 reels | 15 videos |
| Transcript words (total) | 593 | **53,749** |
| Transcript words (median/item) | ~0 (9 of 12 usable, mostly <40) | **3,468** |
| Comments sampled | 85 (page-1 only) | 591 (dedup; ~40 sampled/video) |
| Total comments available | ~300 across corpus | **3,231** |
| Purchase-intent comments | **0** | **47** (~8% of sampled) |
| Dupe/clone-discourse comments | **0** | **46** (~8% of sampled) |
| Views (corpus total) | — | 552,859 |

Transcript substrate is **~90× larger**; the audience-signal categories that
were flatly *absent* for Jeremy (purchase intent, dupe-seeking) are present at
~8% each for GentsScents. The round-1 caps were **substrate-bound, not
method-bound** — confirmed.

Purchase-intent examples (verbatim, from captured comment samples):
- "I purchased Raees Luxury edition the day I saw this video and it was in stock and shipped already." (q0oiKqeghks)
- "Reflection man is on my list to eventually get. One day!" (eH93HPAWucE)
- "I bought Coral Fantasy last year and have no complains!" (eH93HPAWucE)

## Re-grade against identical charter Section 4 criteria

**Fit panel: B (was D+).** With long-form transcripts, three of five components
move from thin/withheld to genuinely populated:
- *Segment share* — clean: 15/15 are structured fragrance-review content
  (rankings, clone guides, seasonal lineups), not persona content.
- *Product-tier distribution* — rich: each video names 10–25 products across
  designer/niche/clone tiers; a real distribution is derivable (still needs a
  tier/note ontology to be *derived* vs operator-labeled — same round-1 gap).
- *Audience taste* — strong and decision-relevant: collector + dupe-seeker +
  purchase-intent discourse all present and quantifiable (unlike Jeremy's
  persona-mocking texture). Still page-/sample-capped (~40 comments/video of
  100–700 total).
- *Proven adjacency* and *niche-share trajectory* — **still withheld**: one
  capture cycle, no time axis. Unchanged from round 1; not fixable by more
  single-cycle capture.

Caps it at B, not A: the two time-axis components stay withheld, and product
tiers still lean on operator knowledge without an ontology.

**Ad-reception panel: C+ (was C-).** Detection substrate is far better (dense
transcripts, real engagement metrics: 20K–65K views, 1.1K–4.7K likes,
100–703 comments/video), so load and reception comparisons have real body. But
a **new capture gap** caps it: the watch-packet schema captures metadata +
comments but **not the video description**, and for YouTube reviewers the
affiliate links and sponsor disclosure live in the description. Transcripts
alone show GentsScents' recent window is largely organic review (1 of 15
transcripts even mentions "sponsored", and that instance is about *retailer
listings*, not his own sponsorship). So sponsorship load/detection is
under-measured for a structural, fixable reason — not a creator reason.

## What round 2 changes about the build picture

1. **The method is not worthless — the round-1 subject was.** A typical
   reviewer clears the fit panel to roughly B on a single capture cycle. The
   product is real; it was starved of substrate.
2. **The #1 round-1 shopping-list item is validated.** "YouTube long-form
   transcripts at roster scale" was the top gap; one creator-week of it lifted
   fit a full letter-and-a-half. This is the highest-leverage capture to scale.
3. **Two hard caps remain, both already on the round-1 list:**
   - *Time axis* (≥2–3 cycles) for adjacency, trajectory, momentum — needs the
     grid clock running over weeks, not more one-shot capture.
   - *Sponsored stratum* for the ad-reception core — and now also a concrete
     sub-item: **add description capture to the watch-packet schema**, since
     that is where YouTube sponsorship disclosure lives.
4. **New shopping-list item (round 2):** watch-packet description field. Small,
   capture-lane; unblocks most of the ad-reception panel for reviewers.

## D-1 advisory (owner-routed, not decided here)

Round 2 strengthens the round-1 recommendation for a **practice-run** D-1 gate
over numeric targets: a suggested gate shape is "a single-creator fit +
ad-reception panel reaches B or better on a *representative* reviewer using
roster-scale long-form substrate." GentsScents' fit panel already meets a B on
one cycle; the remaining blockers to A (time axis, sponsored stratum +
description capture) are the concrete, named exit conditions. Owner decision;
nothing here fires the gate.

## Honesty caveats

- **Duplicate packets:** the first dispatched capture worker stalled after
  reporting, but had already captured 12 of the 15 videos in a background
  shell; the recovery loop re-captured them. 12 of 15 videos therefore have 2
  caption + 2 watch packets in the lake. Harmless (append-only,
  content-addressed; reads dedupe), but it is clutter and the headline counts
  above are computed newest-packet-per-video, dedup'd. Prunable on request.
- Comment sentiment/intent coding is a single model pass over sampled comments,
  not a validated classifier; the intent/dupe rates are directional.
- Sponsorship characterization is limited by the missing description field
  (see ad-reception grade); "largely organic" is a transcript-only inference.
- Single capture cycle; page/sample-limited comments; grades are the authoring
  model's honest self-assessment and the natural target for delegated
  adversarial review.

## Non-claims

- Not validation, readiness, buyer proof, or willingness-to-pay evidence;
  `product_learning`-capped.
- Authorizes no roster-scale capture, no ontology build, no schema change; each
  is its own gated lane. FLAG 1 remains open.
