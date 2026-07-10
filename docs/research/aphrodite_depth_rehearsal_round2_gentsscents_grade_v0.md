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
  - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
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
| Comments engagement-ranked w/ per-comment likes | partial | **yes** (top-sort + `like_count`/`reply_count` per comment) |
| Total comments available | ~300 across corpus | **3,231** |
| Purchase-intent comments | **0** | **47** (~8% of sampled) |
| Dupe/clone-discourse comments | **0** | **46** (~8% of sampled) |
| Monetization signal in captured description | n/a | **85 affiliate links, 15/15 videos** |
| Views (corpus total) | — | 552,859 (per-video 20K–65K) |

Transcript substrate is **~90× larger**; the audience-signal categories that
were flatly *absent* for Jeremy (purchase intent, dupe-seeking) are present at
~8% each for GentsScents. The round-1 caps were **substrate-bound, not
method-bound** — confirmed.

Purchase-intent examples (verbatim, from captured comment samples):
- "I purchased Raees Luxury edition the day I saw this video and it was in stock and shipped already." (q0oiKqeghks)
- "Reflection man is on my list to eventually get. One day!" (eH93HPAWucE)
- "I bought Coral Fantasy last year and have no complains!" (eH93HPAWucE)

**Comments arrive engagement-ranked** (YouTube `youtubei/next` default Top-sort)
with per-comment `like_count` and `reply_count` captured — so a comment's weight
relative to the others is directly available (e.g. a 27-like "you can't go wrong
recommending Versace Pour Homme" vs a 1-like reply). High-value texture signal,
already in the capture, no extra work to obtain.

**Monetization signal is already captured, correcting an earlier error in this
doc's first draft.** The watch packet DOES capture the video description
(`packet.metadata.short_description`); the first draft checked the wrong field
and wrongly concluded the description was uncaptured. In fact all 15 descriptions
carry affiliate links (`gentsscents.me/...`, `go.magik.ly/ml/...`) — 85 links
total — and the raw watch HTML carries affiliate/sponsorship markers. The
formal YouTube paid-promotion flag (`paidContentOverlay`) is 0 across the
corpus, i.e. this creator monetizes via **affiliate**, not declared paid
partnerships — and that entire signal is already on disk. **Ad-reception is an
extraction task over captured metadata, not a capture gap** (owner-confirmed).

## Grading rubric (owner-set, 2026-07-04)

The time axis is removed from the grade ceiling. Because no second capture cycle
exists yet, components that *require* longitudinal data (proven adjacency,
niche-share trajectory, momentum) must not cap the grade — grading a
single-cycle rehearsal down for lacking time it structurally cannot have "bans
ourselves for no reason." So:

- **A** = the best a panel can be **from a single capture cycle** (all
  non-time components decision-grade).
- **S** = A **plus** the longitudinal components, once ≥2 cycles exist
  (separate, later).

Grades below are against **A** (time-excluded). Time-axis components are marked
`deferred-to-S`, not counted against the grade.

## Re-grade against identical charter Section 4 criteria

**Fit panel: A- (was D+; time-excluded rubric).** With long-form transcripts:
- *Segment share* — clean: 15/15 are structured fragrance-review content
  (rankings, clone guides, seasonal lineups), not persona content.
- *Product-tier distribution* — rich: each video names 10–25 products across
  designer/niche/clone tiers; a real distribution is derivable. The one thing
  keeping this off full A: tiers/notes are still *operator-labeled* without a
  fragrance ontology (the round-1 ontology gap — a build task, not capture).
- *Audience taste* — strong and decision-relevant: collector + dupe-seeker +
  purchase-intent discourse all present, quantifiable, and now **weightable by
  per-comment likes** (top-ranked comments carry the loudest signal). Sample-
  capped at ~40/video but that is a sampling knob, not a wall.
- *Proven adjacency*, *niche-share trajectory* — `deferred-to-S` (need ≥2
  cycles); not counted against the grade.

A- not A only because product tiers/notes need the ontology to be *derived*
rather than operator-asserted.

**Ad-reception panel: A- (was C-; time-excluded rubric).** The substrate is all
captured: dense transcripts, per-video engagement (20K–65K views, 1.1K–4.7K
likes, 100–703 comments), engagement-ranked comments, and — corrected from the
first draft — the full description with **85 affiliate links across 15/15
videos** plus the `paidContentOverlay` paid-promotion flag (0 = affiliate model,
not declared partnership). Detection, load (monetization density), and
reception (engagement of monetized vs less-monetized content) are all buildable
**now, from captured data**. A- not A only because (a) the sponsored-vs-organic
contrast is mild for this creator — nearly every video carries affiliate links,
a creator property, not a capture gap — and (b) the extraction pass itself has
not been run yet (see below). No capture gap remains.

## What round 2 changes about the build picture

1. **The method is not worthless — the round-1 subject was.** Under the
   time-excluded rubric a typical reviewer clears both panels to A-. The product
   is real; round 1 was starved of substrate.
2. **The #1 round-1 shopping-list item is validated.** "YouTube long-form
   transcripts at roster scale" was the top gap; one creator-week of it lifted
   fit from D+ to A-. This is the highest-leverage capture to scale.
3. **What actually remains to reach A (single cycle) is extraction + ontology,
   not capture:**
   - **Run the extraction passes over the captured substrate** — product
     mentions (for fit + share-of-voice) and monetization/ad signal (for
     ad-reception). Both inputs are already on disk; the passes have not been
     run in this environment (see caveats). This is the immediate next move.
   - **Fragrance ontology with tier/note reference data** — so product-tier and
     note-family distributions are *derived*, not operator-asserted. Build task.
     *(Update 2026-07-10: since built —
     `forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml`.)*
4. **Corrected from the first draft:** the earlier "add description capture to
   the watch-packet schema" shopping item was **wrong** — the description is
   already captured (`packet.metadata.short_description`, 85 affiliate links
   across 15 videos). No schema change is needed; ad-reception is extraction.
5. **To reach S:** the time axis (≥2–3 capture cycles) for adjacency,
   trajectory, momentum — the grid clock running over weeks. Out of scope for a
   single-cycle grade by the owner rubric above.

## Product-mention / share-of-voice status (not yet run)

> **Update (2026-07-10): since run.** The round-2 share-of-voice extraction
> landed as `docs/research/aphrodite_depth_rehearsal_round2_share_of_voice_v0.md`,
> and the fragrance reference graph consumed its output (see the "round-2 SoV
> extraction" note in `fragrance_reference_v0.yaml`). The section below records
> the historical pre-run state.

The `silver__cleaning__product_mentions` lane (the share-of-voice input) is
**not populated for GentsScents**. Only the two capture runners
(caption + watch) were run; the product-mention extractor
(`orca-harness/runners/run_transcript_product_extract.py`) is a no-LLM,
transport-injected daemon runner and this environment has no `ANTHROPIC_API_KEY`
/ wired transport, so it could not be run here. It IS wired to consume
`youtube_captions` packets (its `_transcripts_for_packet` handles the
`youtube_captions` surface directly), so once a transport/key is available it
will pick up all 15 GentsScents caption packets idempotently and emit the
mentions record-sets that feed share-of-voice. This is the concrete blocker on
the fit panel's product-tier component and the recommended next action.

## Creator registry status

GentsScents was **already a registered account** in the Creator Registry
(`acct_yt_fragrance_010`, matched by public handle) — the capture preflight
resolved `existing_match` / `allowed`, which is exactly why the capture was
permitted without a new-candidate admission. This run **did not mutate the
registry**: capture writes raw packets only; the preflight is explicitly "not
registry mutation," and no metric-rollup/current-view update was run. So there
was no new creator to add, and the captured metrics are not yet reflected in
any registry current-view (that is a separate projection step, not run here).

## D-1 advisory (owner-routed, not decided here)

Round 2 strengthens the round-1 recommendation for a **practice-run** D-1 gate
over numeric targets. Under the owner's time-excluded rubric a suggested gate
shape is "a single-creator fit + ad-reception panel reaches A- or better on a
*representative* reviewer from captured substrate." GentsScents meets that on
one cycle **pending the extraction passes**; the remaining exit conditions are
run-the-extraction and build-the-ontology (both non-capture). Owner decision;
nothing here fires the gate.

## Honesty caveats

- **First-draft correction:** this doc's first committed draft claimed the
  video description was uncaptured and proposed a watch-packet schema change.
  That was a false read (wrong JSON field checked); the description is captured
  and the ad-reception grade/shopping-list are corrected above. Recorded rather
  than silently overwritten.
- **Duplicate packets:** the first dispatched capture worker stalled after
  reporting, but had already captured 12 of the 15 videos in a background
  shell; the recovery loop re-captured them. 12 of 15 videos therefore have 2
  caption + 2 watch packets in the lake. Harmless (append-only,
  content-addressed; reads dedupe), but it is clutter and the headline counts
  above are computed newest-packet-per-video, dedup'd. Prunable on request.
- Comment sentiment/intent coding is a single model pass over sampled comments,
  not a validated classifier; the intent/dupe rates are directional.
- Product-mention and monetization extraction have **not** been run here; grades
  reflect substrate readiness, and the panels are not themselves built yet.
- Single capture cycle; sample-limited comments; grades are the authoring
  model's honest self-assessment and the natural target for delegated
  adversarial review.

## Non-claims

- Not validation, readiness, buyer proof, or willingness-to-pay evidence;
  `product_learning`-capped.
- Authorizes no roster-scale capture, no ontology build, no schema change; each
  is its own gated lane. FLAG 1 remains open.
