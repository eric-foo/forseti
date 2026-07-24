# Summer Fridays Understanding p07 — Acquisition Seal

```yaml
retrieval_header_version: 1
artifact_role: evidence-layer acquisition seal
scope: Manual adjudication of the p06 control plus the bounded p07 REVOLVE and TSG completion evidence.
use_when:
  - Checking whether Summer Fridays Understanding may proceed from Phase A acquisition into Turn B.
  - Resuming the one remaining primary-retailer evidence gap.
authority_boundary: retrieval_only
open_next:
  - docs/research/summer_fridays_understanding_dogfood_20260725_p07/evidence_layer_completion.md
  - docs/research/summer_fridays_understanding_dogfood_20260724_p06/coordinated/turn_a_acquisition_record.md
stale_if:
  - The p06 control, p07 completion receipt, or TSG capture changes.
  - Sephora review-corpus onboarding is added or re-adjudicated.
```

```yaml
subject: Summer Fridays
cycle_id: sf_understanding_20260725_p07_evidence_completion
seal_owner: current_home_actor
adjudication_mode: manual_after_fresh_read
state: BLOCKED_ACQUISITION_INCOMPLETE
gate: fail
deliver_allowed: false
phase_a_complete: false
phase_b_started: false
turn_b_started: false
company_report_exists: false
```

## Decision

The p07 bounded completion passed for REVOLVE and the TSG transaction event, but
the complete Phase A acquisition does not yet pass.

Closed since the p06 control:

1. All 37 admitted REVOLVE listings now resolve to a completed bounded Yotpo
   review collection or source-declared zero-row outcome. The 607 captured
   occurrences deduplicate to 576 native review IDs and 35 observed overlap
   components.
2. The official TSG Consumer announcement is durably captured and can bear the
   dated 2024 transaction, retained-founder-stake, continued-founder-leadership,
   and Prelude-exit claims.
3. Sunlit Vanilla is no longer an acquisition blocker.

One material gap remains: Sephora is the officially named primary retailer, but
its review-corpus onboarding is absent. The REVOLVE board adds substantial
skincare, body, makeup, and set coverage but cannot substitute for Sephora's
distinct customer corpus or close fragrance depth when REVOLVE has no admitted
fragrance listing.

## Smallest unblock

Complete the bounded Sephora review-corpus board using its existing
source-specific onboarding roles—Helpful plus statistics, Recent, and Q&A—then
re-adjudicate only that job and this seal.

Do not rerun completed p06 identity or retailer work, add another retailer,
retry Reddit, capture Sunlit Vanilla, start Turn B, or author the company report
for this unblock.

