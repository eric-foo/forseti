# Near-Half Signal-Reliability Ledger v0 (schema + discipline; closes far-half N7)

```yaml
retrieval_header_version: 1
artifact_role: PROPOSED schema + discipline contract (defines the signal-reliability ledger the near-half produces and decision-memory consumes; binds no signal, admits no source-family, populates no rows)
scope: >
  The durable definition of the signal-reliability ledger: what a signal is, the
  firewall-clean pre-commitment unit, the K-of-N report-all reliability tally,
  the product-learning cap, staleness, provenance, and how rows flow in (from
  blind backtest resolutions and the far-half) and out (to decision memory).
  Step 1 of 3 in the near-half build (signal-reliability -> architecture ->
  postmortem). Closes the far-half's pending N7 interface.
use_when:
  - Recording or reading a signal's reliability across backtest cases or live resolutions.
  - Building the near-half postmortem loop or the decision-memory query surface.
  - Checking what a reliability tally may claim and what it must not.
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md
  - docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md
input_hashes:
  docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md: <FILL_AT_PROMOTION — blob-bytes SHA256 on the landing commit>
branch_or_commit: near-half-signal-reliability-ledger-v0 off origin/main @ 96134a3
stale_if:
  - The far-half N7 interface fields change (re-reconcile the field map below).
  - The harness signal/evidence vocabulary changes in orca-harness/schemas/judgement_models.py.
  - The near-half architecture (step 2) amends the ledger's role, inflow, or outflow.
  - The evidence ladder tiers, closeout states, or the conductor firewall doctrine change.
```

## Status

`PROPOSED` — schema + discipline only, product-learning tier. Defines the ledger;
**binds no signal, admits no source-family, populates no real rows, and promotes
nothing.** The worked example is illustration (`example_not_a_real_row`). The
owner-stated build order is signal-reliability → architecture → postmortem; this
is step 1, deliberately authored before the near-half architecture so the
architecture (step 2) wraps a concrete interface rather than a hypothetical one.

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_signal_reliability (far-half architecture N7 + batch-1 ledger signal discipline + evidence ladder + harness judgement_models.py, all re-verified on origin/main @ 96134a3)
  edit_permission: docs-write
  target_scope:
    - docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md (new, this file only)
  dirty_state_checked: yes (fresh branch off origin/main; clean at start)
  blocked_if_missing: no
```

## Why This Exists (the improving-judgment job)

The backtest harness today *scores* blind calls; it does not *learn* from them in
a carried way. The single most reusable thing to carry forward is **which signals
actually predict** — generalized from batch-1, which proved this for one signal
(org-motion) on one batch ("org-motion moved the call in K of N pre-committed
cases"). The signal-reliability ledger makes that a standing record: every signal
a judgment leans on accrues a reliability history, so the next blind call can
weight it on evidence instead of intuition. This is counterparty-free and runs on
the backtest cases that already exist.

## What A Signal Is (and is not)

A **signal** is a *named, reusable* evidence-family or indicator a judgment can
lean on across cases — e.g., org-motion / hiring composition, review-venue
candidate yield, embedded price-payload movement. It has a stable `signal_id` and
a reliability history worth tracking.

A signal is **not** a one-off claim or a single evidence unit. The harness
`EvidenceUsed` row (`claim_id`, `claim_text`, `claim_role`, `evidence_unit_ids`)
records *a* use of evidence in *one* judgment; the signal is the reusable family
that use belongs to. One signal spans many `EvidenceUsed` rows across many cases.
A signal whose reliability is tracked here is **still not an admitted/bound
source-family** — JSG-01 stays frozen; promotion to a bound source-family is a
separate, stronger gate (see Caps), not a consequence of a good tally.

## The Firewall-Clean Pre-Commitment Unit (the load-bearing rule)

The unit of reliability is one **pre-committed use**: a `(signal_id, case_id)`
pair whose **predicted direction was recorded inside the blind pre-reveal call**,
before the outcome was knowable. This anchors the tally to the firewall:

- the signal's predicted direction lives in the **blind judgment** (the only
  judgment score; the conductor firewall) — it is pre-reveal evidence;
- the reliability tally (did it point the right way) is computed **post-reveal**,
  which is lower-tier by construction (it uses the revealed outcome);
- a signal direction asserted *after* reveal ("org-motion clearly predicted
  this") is a **confirmed tell**, not a pre-committed use — it is excluded and,
  if it contaminated the call, routes to the contaminated branch.

This is the live/backtest generalization of batch-1's rule: *record the blind
signal prediction before the reveal.*

## The K-of-N Report-All Tally (the cherry-pick guard)

A signal's reliability is **K correct of N pre-committed uses**, under two
non-negotiable rules carried from batch-1:

1. **Pre-commit before reveal.** A signal can only be added to a case's
   pre-committed set before that case's outcome is examined for favorable
   alignment. You cannot add a signal to a case after seeing it would have
   helped.
2. **Report all.** Every pre-committed `(signal, case)` use is tallied —
   correct, wrong, not-applicable, and unscoreable alike. Dropping the misses
   voids the property. The honest claim is "signal S pointed the right way in K
   of N pre-committed uses," never "here is a case where S worked."

Per use, the outcome is exactly one of: `correct_direction` | `wrong_direction`
| `not_applicable` (signal didn't bear on this case) | `unscoreable`
(outcome criterion couldn't be applied). Only `correct`/`wrong` count toward K/N;
the others are reported but excluded from the ratio.

## Ledger Schema v0

```yaml
signal_reliability_ledger_v0:
  signals:
    - signal_id:                 # stable key; the N7 identity field
      description:               # what the signal is, in one line
      applicable_decision_families: []   # the N7 decision_family scope; a signal is reliable WITHIN families, not globally
      reliability:               # the N7 "reliability evidence"
        pre_committed_uses: []   # one entry per (signal, case) pre-committed use:
          # - case_id:
          #   predicted_direction:        # recorded in the blind call (pre-reveal)
          #   blind_call_ref:             # provenance: the sealed pre-reveal judgment that carries the prediction
          #   outcome: correct_direction | wrong_direction | not_applicable | unscoreable
          #   resolution_ref:             # provenance: where the post-reveal score was computed
        tally:
          k_correct:             # count of correct_direction
          n_scoreable:           # correct + wrong (the denominator)
          excluded:              # not_applicable + unscoreable counts, reported
      validation_status:         # the N7 "validation status": product_learning (default) | <stronger only via a named gate>
      staleness:                 # the N7 "staleness marker"
        stale_if: []             # e.g., underlying source changed; decision-family drift; N too small; tally older than <window>
        last_reviewed:
      provenance:                # the N7 "provenance": where rows came from
        row_sources: []          # backtest postmortem | far-half resolution emit
  non_claims:
    - a tally is product-learning evidence about signal usefulness, not judgment-quality
    - a high K/N does not admit or bind the signal's source-family (JSG-01 frozen)
    - a tally proves selection discipline + post-reveal correlation, not causation
```

### N7 field reconciliation (closes the far-half pending interface)

| Far-half N7 field (architecture) | Ledger field here |
| --- | --- |
| stable `signal_id` | `signals[].signal_id` |
| applicable `decision_family` | `signals[].applicable_decision_families` |
| reliability evidence with provenance | `signals[].reliability` + `signals[].provenance` |
| validation status | `signals[].validation_status` |
| staleness marker | `signals[].staleness` |

The fields match the architecture's named N7 interface, so this ledger **closes
N7 with no architecture edit** — the far-half's `signals_used` emit
(`signal_reliability_rows` at resolution) lands as `reliability.pre_committed_uses`
entries here.

## Inflow / Outflow

- **In (two sources, same shape):** (a) **backtest postmortems** — the near-half
  step-3 loop reads a scored blind case and appends one pre-committed-use entry
  per signal the blind call carried; (b) **far-half resolutions** — when the
  live loop exists, `signal_reliability_rows` emitted at resolution append the
  same entry shape. The ledger does not care which half produced a row; both are
  firewall-clean pre-committed uses.
- **Out (read-only):** **decision memory** queries the ledger by
  `decision_family` to weight a signal at the next blind call. Reading the ledger
  is advisory input to a judgment; it never overrides the blind call or promotes
  a source-family.

## Caps (what a tally may and may not claim)

- **Product-learning by default.** A reliability tally is product-learning
  evidence per the evidence ladder. It does not become buyer-proof or
  judgment-quality without that tier's own gate.
- **No source-family promotion.** A good tally does not admit, bind, or unfreeze
  a source-family. Batch-1 explicitly kept org-motion *not promoted to a standing
  source-family*; this ledger tracks reliability without changing that. Promotion
  is a separate owner-gated decision.
- **Correlation, not causation.** A post-reveal tally shows the signal pointed
  the right way K of N times under pre-commitment; it does not prove the signal
  *caused* the outcome or will hold out-of-sample.
- **Small-N honesty.** K/N at small N is weak; the tally is reported with N, and
  staleness/N caveats travel with any use of it.

## Worked Example (`example_not_a_real_row` — illustrative)

```yaml
signal_id: org-motion-hiring-composition
description: direction of public ATS hiring composition (expansion vs contraction by function) ahead of a demand decision
applicable_decision_families: [beauty-consumer-demand, launch-expand]
reliability:
  pre_committed_uses:
    - case_id: beautypie_repricing_2023_v0
      predicted_direction: expansion -> supports demand-positive call
      blind_call_ref: <the sealed blind judgment carrying the org-motion prediction>
      outcome: correct_direction
      resolution_ref: <where the post-reveal score was computed>
  tally: { k_correct: 1, n_scoreable: 1, excluded: 0 }
validation_status: product_learning
staleness:
  stale_if: [Greenhouse board schema changes, beauty-family drift, N < 3]
  last_reviewed: <date>
provenance: { row_sources: [backtest postmortem] }
```
Illustrative only: it shows the firewall-clean shape (direction in the blind
call, score post-reveal), N=1 honesty, the product-learning cap, and no
source-family promotion. It is not a real row and creates no reliability claim.

## Claim Classification

```yaml
judgment_spine_claim_classification:
  evaluated_claim_surface: signal-reliability ledger (schema + discipline contract)
  source_quality_state: design/control artifacts only (far-half N7 + batch-1 + ladder + harness, re-verified on main); no real rows
  execution_quality_state: no signal tracked, no tally computed, no row populated
  closeout_state: no_durable_evidence
  claim_cap: design input / product-learning context only
  weakest_missing_or_failed_gate: no real pre-committed uses recorded; near-half postmortem (step 3) not yet built
  receipt_artifact_or_gap: first real rows come from the step-3 backtest postmortem loop
  non_claims:
    - not validation unless separately proven
    - not readiness unless separately proven
    - not buyer proof unless the buyer-proof receipt is complete
    - not judgment-quality evidence unless the judgment-quality receipt is complete
```

## Non-Claims

- Schema + discipline only; binds no signal, admits no source-family, promotes
  nothing, populates no real rows.
- Mints no evidence-ladder vocabulary; reuses `signal_id`/`decision_family` from
  the architecture and the K-of-N/report-all discipline from batch-1.
- Closes the far-half N7 interface by matching its named fields; it does not edit
  the architecture or change the far-half's claims.
- A reliability tally is product-learning evidence about signal usefulness — never
  judgment-quality, never a source-family admission, never causation.
- The worked example is illustration and can never be cited as a reliability row.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The near-half signal-reliability ledger is now a durable PROPOSED schema +
    discipline contract: a firewall-clean pre-committed-use unit, a K-of-N
    report-all tally, a product-learning cap, and the N7 field map. This is the
    first near-half artifact (step 1 of 3) and makes the far-half's pending N7
    interface concrete.
  trigger: architecture_doctrine
  controlling_sources_updated:
    - docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md (new; this file only)
  downstream_surfaces_checked:
    - docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md  # N7 fields MATCH this ledger; no edit needed — the architecture's stale_if ("near-half ledger lands") is satisfied by reconciliation, recorded in the N7 field-map table above
    - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md  # K-of-N/report-all/org-motion-not-promoted discipline reused, not amended
    - docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md  # product-learning cap consumed, no tier minted
    - docs/product/judgment_spine/prospective_decision_loop_phase0_semantics_spec_v0.md  # signals_used shape consistent; the ledger is the destination its rows flow to
  intentionally_not_updated:
    - path: docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md
      reason: N7 was authored as a pending interface with exactly these fields; this ledger fills it by matching them, so no architecture text changes. If a reviewer finds a field mismatch, that is a finding to reconcile, not a silent edit.
    - path: docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md
      reason: batch-1 remains the historical exemplar; its org-motion pre-commitment is generalized here, not rewritten.
  stale_language_search: >
    rg -n "signal-reliability|signal_reliability|signal_id|K of N|report-all|pre-committed"
    docs/product/judgment_spine docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md
  non_claims:
    - not validation
    - not readiness
    - not a source-family admission or JSG-01 unfreeze
    - not implementation authorization
```
