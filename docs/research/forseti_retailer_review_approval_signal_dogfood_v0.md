# Retailer Review Approval Signal Dogfood v0

## Status and use

- Status: `BOUNDED_SAMPLE_MECHANICAL_DOGFOOD_PASSED`
- Observed on: `2026-07-19`
- Use: implementation evidence for the optional Commission Signal Board
  retailer-review approval signal
- Not established: full-corpus validity, representative customer approval,
  demand, market consensus, causal incentive distortion, or cross-retailer
  comparability

This record tests whether the proposed derivation preserves incentive
disclosures, denominator boundaries, arithmetic, and permitted language on a
real preserved review slice. It does not promote the slice into a population
claim.

## Preserved source

- Source surface: Credo/Yotpo, Tower 28 SOS Daily Rescue Facial Spray
- Source-visible review count: `648`
- Capture packet: `01KXX5M6BGQ6CM9XJ1752F7N2Y`
- Projection: `01KXX6RCN8C2XTH3JZF055RMSJ`
- Projection SHA-256:
  `778266c9af8b9dd526a83083768fe78d632756049f3258632b4afe3cded4c0fd`
- Corpus basis: `reproducible_bounded_sample`
- Sample selection: first ten rows from the preserved date-sorted widget
  response
- Limitation: this is a recent, non-random slice of ten rows, not the
  648-review corpus

The source projection preserves ten ratings and the source-visible Yotpo
`is_incentivized` field per row. A false flag is treated only as `not marked
incentivized`; it is not treated as confirmed organic or explicitly
non-incentivized.

## Derived result

```yaml
retailer_review_approval_signal:
  corpus_basis: reproducible_bounded_sample
  source_visible_total: 648
  captured_total: 10
  sample_selection: first ten rows from the preserved date-sorted widget response
  incentive_disclosure_basis: source-visible Yotpo is_incentivized boolean
  excluded_explicit_incentivized: 5
  excluded_unknown_or_conflicting: 0
  excluded_other: 0
  excluded_other_reason: none
  eligible_explicit_non_incentivized: 0
  eligible_not_marked_incentivized: 5
  eligible_total: 5
  eligible_positive_4_5: 5
  eligible_below_positive_1_3: 0
  approval_rate_pct: 100.0
  below_positive_rate_pct: 0.0
```

Permitted reading:

> In the preserved latest-ten review slice, all five reviews not marked
> incentivized were four or five stars; five source-flagged incentivized
> reviews were excluded from this derived view.

Prohibited reading:

> Tower 28 has 100% organic customer approval.

The prohibited version changes `not marked incentivized` into `organic`, drops
the denominator and selection boundary, and generalizes five eligible rows to
the retailer-wide corpus.

## Result

The real slice exercises the intended behavior:

- all ten rows remain in the source packet;
- the five source-flagged incentivized rows are excluded only from the derived
  primary view;
- the eligible denominator and excluded count are visible;
- the output stays bounded to the latest-ten sample; and
- no strict explicit-non-incentivized sensitivity is emitted because this
  surface does not explicitly certify those five rows as non-incentivized.

The dogfood is sufficient to validate the mechanical and language boundary.
It is intentionally insufficient to validate the metric on a full retailer
corpus or to claim that incentive filtering changes the substantive conclusion.
A later full-corpus run is the upgrade trigger for those stronger claims.
