# Product-Verdict Calibration — Labeling Protocol v0

```yaml
retrieval_header_version: 1
artifact_role: calibration labeling procedure (operational record; not a data run, not validation)
scope: >
  How the owner builds the labeled corpus that real calibration of the deterministic Pass-2
  product-verdict fusion needs: capture real reels, extract mentions, and label a blind gold
  verdict per (creator, product), then how those labels feed a Phase C re-fit.
use_when:
  - Preparing to run the Phase B calibration corpus (capture + label).
  - Defining what a gold product verdict means so labels stay consistent.
  - Feeding owner labels into a Phase C constant re-fit.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/product_verdict_fusion_calibration_surface_v0.md   # the knobs + findings this corpus calibrates
  - orca-harness/runners/run_source_capture_ig_reels_creator_deep_capture.py  # the capture path
  - orca-harness/scoring/product_fusion_sensitivity.py               # the harness Phase C runs over the corpus
stale_if:
  - The capture path or Pass-1 extraction seam is replaced (update the steps that name them).
  - The owner adopts a different gold-label vocabulary than positive/mixed/negative/unknown.
```

## Status

`PROCEDURE — NO DATA RUN EXECUTED`. This is the method only; it captures nothing and labels
nothing by itself. Running it is owner-gated (needs per-operation network approval for live
capture). It is not validation, readiness, buyer proof, or a calibrated-threshold claim.

## Purpose and scope

Real calibration of `scoring/product_fusion.py` needs ground truth: the owner's own verdict on
real mentions, against which the constants are tuned. This protocol produces that corpus.

In scope: the **creator product verdict** only (positive / mixed / negative / unknown about a
product, from one creator across their reels). **Out of scope:** engagement / resonance
weighting, audience-comment ranking, demand, and cross-creator aggregation — those are the
deferred Judgment brain, not this fusion.

## Constraints (carry verbatim)

- **Real public data only.** Anonymous, subscription-not-API, human-pace capture. No synthetic
  mentions — calibrating on synthetic data re-encodes our priors and is worthless for this.
- **Per-operation network approval** for every live capture.
- **Spread creators.** Several real fragrance creators spanning styles (sincere reviewer, hype
  style, deadpan / ironic). Do **not** farm jeremyfragrance — he is over-sampled already.
- **The owner produces the labels.** A gold verdict is owner-authored ground truth, never an
  agent-asserted or system-derived value.

## Step 1 — Select and capture

Pick several creators (target >= 5 spanning the styles above). For each, capture their
top-engagement reels via `runners/run_source_capture_ig_reels_creator_deep_capture.py` (grid ->
rank -> top-N deep-capture), persisting comments + transcript to the lake. Engagement-thresholded
capture keeps interaction low; scale later.

## Step 2 — Extract mentions

Run the Pass-1 agent-in-the-loop extraction over each captured transcript to produce
`ProductMention` records (the `parse_mentions(model_text, transcript)` seam; spec:
`ig_reels_transcript_product_extraction_spec_v0.md`). These are the evidence the gold label will
be set against, and the exact input the fusion will later score. Persist them per creator.

## Step 3 — Label the gold verdict (BLIND)

This is the load-bearing step. For each `(creator, brand, line)` product the owner assigns one
gold verdict, **reading the evidence (the located quotes / transcript spans), NOT the system's
verdict.** Labeling against the system output makes the labels correlate with the system and the
calibration circular — the gold label must be an independent judgment.

Gold-verdict rubric (one per product, across all that creator's captured reels):

- **positive** — the creator is, on balance, clearly favorable about the product.
- **negative** — the creator is, on balance, clearly unfavorable.
- **mixed** — genuinely divided: real praise and real criticism, not noise.
- **unknown** — too little to tell: a passing or purely factual mention, or contested noise with
  no resolvable stance. Abstaining is a valid, expected answer; do not force a call.

One label record per product, owner-authored:

```yaml
creator_id: <handle>
brand: <brand>
line: <line>
gold_verdict: positive | mixed | negative | unknown
labeler: owner
evidence_pointer: <mention_ids or reel shortcodes the judgment rests on>
note: <one line of why, optional>
```

Label every product the extractor surfaced for the creator, including the ones you judge
`unknown` — the abstention cases are exactly what calibrates the `material_min` risk dial.

## Step 4 — Feed Phase C (re-fit + sign-off)

With the corpus in hand:

1. Run the fusion over each creator's mentions and compare the **emitted** verdict to the
   **gold** label (the harness `scoring/product_fusion_sensitivity.py` sweeps constants; extend
   it to score agreement against labels).
2. Weight the **confident-wrong** error class hardest: the system emitting positive/negative when
   gold says `unknown` or the opposite polarity is worse than an over-abstention. A false-confident
   verdict misleads Judgment; an abstention merely withholds. This asymmetry is why `material_min`
   is a risk dial the owner sets, not a fitted value.
3. Settle the constants that maximize agreement under that weighting; the **owner signs off** the
   risk dial. Then bump `FUSION_CONFIG_VERSION`, re-derive the pinned sensitivity tests, and
   resolve the shared-vs-independent question with `audience_fusion`.

## Corpus sizing and honesty

Target a few dozen labeled `(creator, product)` units across >= 5 creators for a directional v1.
Be explicit: this is **not** enough to statistically fit six constants — Phase C is "principled
defaults nudged toward owner labels + sign-off", not optimization. More creators and reels
sharpen it; they do not turn it into a trained classifier.

## What this protocol does not cover

Engagement / resonance weighting, audience-comment ranking, demand and affiliate-discount, and
cross-creator aggregation. Those belong to the owner-deferred Judgment brain
(`orca/product/shared/engagement_registry/engagement_logic_registry_v0.md`), not to product-verdict
fusion calibration.
