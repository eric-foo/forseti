# Orca Pricing-First — Method-Validation Handoff (Banked) v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Banks the two decide-vs-confirm method-validation cases (and the substrate-newness risk) for the METHOD-VALIDATION lane. Non-authoritative handoff; the product-lead lane does not execute these.
use_when:
  - The method-validation lane is selecting/locking new cases.
  - Checking the open question the pricing-first wedge depends on.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_icp_wedge_pricing_first_v0.md
  - orca/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_case_locks_v0.md
```

## Status

BANKED handoff for the method-validation lane. The product-lead lane locked
pricing-first (`docs/decisions/orca_icp_wedge_pricing_first_v0.md`); the two
cases below resolve its one open question. They are NOT executed in this lane.
No buyer contact (clears the MVP gate); market-context only; not validation/WTP/
readiness.

## The open question

Does public competitor-PRICE signal DECIDE a repricing move, or merely CONFIRM
one the firm would make anyway? The pricing-first wedge's whole bet rides on the
former; the evidence so far supports only the latter (competitor price is a USED
input, not shown to be decisive).

## The two cases to add to the method-validation portfolio

1. **Pricing-repricing decide-vs-confirm case** — a competitor-/AI-triggered
   repricing decision; at a fair cutoff, test whether public competitor-price/
   packaging signal would have DECIDED (not merely confirmed) the move.
2. **Clean-substrate competitor-displacement case** (the break-in escape-hatch) —
   test whether a clean NON-review public substrate (filings, hiring, changelogs,
   earnings, ecosystem migration) + judgment can carry the "why are customers
   leaving competitor X" read WITHOUT the biased/FTC-polluted review substrate.

Both scored on decide-vs-confirm semantics.

## Substrate-newness risk to test (soundness review AR-S2)

In a first-time AI-monetization wave the competitor-price substrate is itself
new/sparse — "publicly rich" is NOT yet "clean/decision-grade/stable." Case 1
must test whether the substrate is decision-grade for newly-set prices, or narrow
the requirement to cases with at least one observable pricing iteration/anchor.

## Boundary

Owned by the method-validation lane and its locked-case machinery
(`docs/product/core_spine_v0_method_validation_case_locks_v0.md` etc.). Adding or
locking cases is that lane's authorization, not the product-lead lane's. This
note only banks the work; it does not authorize execution, and asserts no
validation, readiness, or buyer-proof.
