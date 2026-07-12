# Forseti Un-Backfillable Signal Moat — Data-Layer Doctrine Capture v0

```yaml
retrieval_header_version: 1
artifact_role: Decision-prep capture (owner-directed 2026-07-10; pending owner sign-off; not ratified doctrine)
scope: >
  Captures the owner-explored data-layer moat doctrine: a public signal is
  moat-grade only if its point-in-time history CANNOT be reconstructed later
  (the archive test). Defines the reconstructability taxonomy (Class A/B/C),
  the two-clocks moat frame (un-backfillable data history + live out-of-sample
  prediction track record), and the rule of thumb "build the data moat on
  rates and point-in-time states, never on static snapshots." Data-layer
  complement to the judgment-layer moat chain
  (docs/decisions/forseti_moat_judgment_quality_proof_path_decision_chain_v0.md).
use_when:
  - Deciding which signals a capture or product lane should treat as moat-bearing.
  - Checking whether a proposed data asset is defensible or trivially backfillable.
  - Designing backtests that reconstruct historical signal (Class B) without
    overclaiming moat (Class A).
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_moat_judgment_quality_proof_path_decision_chain_v0.md   # judgment-layer sibling: track-record-of-correct-calls as the moat gate
  - docs/decisions/forseti_product_thesis_consumer_demand_v0.md                    # Strategic Center: "outcome memory is the moat"
  - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md         # §3 time-later layer — the existing Class-A instance, owned in its own lane
  - docs/workflows/forseti_demand_signal_backtest_probe_handoff_v0.md              # the probe that tests Class-B reconstruction fidelity
stale_if:
  - Owner signs off and this capture is promoted into controlling product/capture sources (separate act with its own receipt).
  - The demand-signal backtest probe falsifies the Class-B reconstruction assumptions or the taxonomy boundaries.
  - The judgment-layer moat chain or the thesis Strategic Center is superseded.
```

## Status

`DECISION_PREP_CAPTURED_PENDING_OWNER_SIGNOFF`. Captures owner-explored framings
from the 2026-07-08/10 Sleipnir product-shape re-exploration thread. Enacts no
doctrine change, amends no controlling source, and carries no
`direction_change_propagation` receipt because it enacts none; ratification is a
separate owner act. Everything here is `product_learning`-capped.

Owner direction signal (verbatim, in-thread 2026-07-10, provenance not
ratification): the live out-of-sample track record "sounds EXACTLY like what
Forseti itself should be doing… that could be Forseti's purpose"; "im feeling
its more of Forseti main function than a sleipnir spinoff… at least we have a
sharper direction for Forseti."

## The Archive Test (the core rule)

**If a later actor can reconstruct a signal's history from what remains public
— web archives (e.g., Wayback), dated items still on the page, vendor-provided
history — then capturing that signal going forward is NOT a moat.** A competitor
starting later simply backfills the same series. A signal is moat-grade only
when its point-in-time state is unrecoverable once the moment passes, so the
only way to own its history is to have been capturing it live.

Owner articulation (verbatim): "if its archive findable, its not really a moat
if we just capture it on a going forward basis. for example - aphrodite's
creator stats make sense because we cant really archive / wayback them."

## Reconstructability Taxonomy

- **Class A — un-backfillable (moat-grade).** Point-in-time STATE that no
  archive records at useful fidelity/cadence: social engagement counters at
  time T (views, likes, follower counts — only the cumulative "now" survives),
  retailer rank / bestseller position, price / availability / out-of-stock /
  promo state, dynamic JS-rendered surfaces, deleted or edited content states,
  and everything needed to compute a *rate* (velocity, momentum, acceleration)
  at historical points. The existing Forseti instance is Aphrodite's creator
  time-series (charter §3 time-later layer) — owned in its own lane; referenced
  here, not duplicated.
- **Class B — partially reconstructable (weak moat; backtest fuel).**
  Dated-item streams: reviews, comments, posts, videos that each carry a
  creation timestamp and are still retrievable. A point-in-time series can be
  *rebuilt* by filtering items to `date ≤ cutoff` — degraded by deletions,
  edits, platform truncation, and survivorship bias. Wayback-style archive
  snapshots of static HTML also sit here (sparse, irregular, popular-pages-
  biased). Class B is valuable — it bootstraps retrospective backtests cheaply
  — but it is NOT a moat: whatever we can reconstruct, a competitor can too.
- **Class C — fully backfillable (no moat; free ground truth).** SEC filings
  and earnings materials (EDGAR), press, static listing/content pages, vendor-
  provided history (e.g., Google Trends), licensed historical datasets. Class C
  is where scoring outcomes come from (free, complete, forever), never where
  the data moat lives.

**Rule of thumb: build the data moat on Class A (rates, velocities, point-in-
time states — i.e., momentum), bootstrap backtests from Class B, score against
Class C, and never claim moat on anything below Class A.**

## The Two Clocks (the moat frame)

Two assets get un-catchable with calendar time, and only these two:

1. **The Class-A data-history clock.** Every day of live capture of
   un-backfillable signal is inventory no entrant can buy retroactively. (This
   is the generalization of Aphrodite charter §3's "longitudinal series that
   cannot be backfilled" beyond creator stats.)
2. **The live out-of-sample prediction track record.** Predictions logged
   *before* the outcome, then scored against it. Cannot be spammed, backfilled,
   or bought; accrues one settled prediction at a time. Retrospective backtests
   (Class-B-fueled) are in-sample and discounted by sophisticated buyers; the
   forward record is the sellable trust asset. This is the same object the
   judgment-layer moat chain names (D1: "a calibrated track record of correct
   calls") and the thesis Strategic Center names ("outcome memory is the
   moat") — this capture adds the data-layer half and the archive test.

Corollary: a track record exists only per *specific, repeatable, scoreable
prediction* — never for "general judgment." Generality lives in the subjects
covered, not in the prediction type. Owner-explored primary indicator this
thread: demand intensity/momentum-acceleration, with authenticity
(real-vs-manufactured) as the co-primary quality gate; durability is a
monitored follow-on read, not a from-snapshot read. Indicator selection remains
owner-open.

## Open Questions (probe-gated)

- Class-B reconstruction fidelity: how completely can dated-item streams
  (comments especially) rebuild a zero-lookahead point-in-time series, and does
  the reconstructed signal predict Class-C outcomes? → commissioned as the
  demand-signal backtest probe
  (`docs/workflows/forseti_demand_signal_backtest_probe_handoff_v0.md`).
- Which Class-A signals are highest-value per the chosen indicator, per venue,
  under capture-lane ToS/armory constraints (capture-lane-owned).
- Whether and how this capture is promoted into controlling sources (owner
  sign-off; separate act, own receipt).

## Non-Claims

Not ratified doctrine, not validation, not readiness, not buyer proof, not
willingness-to-pay, not capture authorization, not a capture-route or ToS
decision, not a product-shape decision, and not a change to any Aphrodite
record (whose creator time-series stays owned in its own lane). The
"momentum/acceleration is not priced in" intuition is an untested hypothesis
the probe exists to test, not a claim.
