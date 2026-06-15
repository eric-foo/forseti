---
retrieval_header_version: 1
artifact_role: Capture-side source-provenance record (capture-spine deliverable; NOT a fixture, band input, or contestant-visible packet)
scope: >
  Per-evidence-unit provenance for the pre-cutoff Wayback capture set of case
  kinderbeauty_box_pivot_2023_v0. Records what is archive-captured (a homepage
  trajectory), the selected snapshots and body hashes, and the honest limits.
  This is a capture-spine starter set, not a backtest fixture: no participant
  packets, no facilitator ledger, no sealed outcome, no evaluation exist for
  this case yet.
use_when:
  - Auditing what the Kinder Beauty box-pivot case is archive-sourced from so far.
  - Deciding what a later judgment-spine fixture for this case would still need.
authority_boundary: retrieval_only
open_next:
  - docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md   # roster row this case came from (candidate #4)
  - docs/product/core_spine/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md   # the backtest specimen shape a later fixture would mirror
---

# Source Provenance Notes — kinderbeauty_box_pivot_2023_v0 (v0)

Capture-side record. This is the **capture-spine deliverable** for the Kinder
Beauty box-economics-pivot backtest case: a bounded set of pre-cutoff Wayback
homepage captures, produced by the `archive_org` adapter
(`run_source_capture_archive_packet.py`, `select_snapshot <= cutoff`). Each
capture is `cutoff_posture: pre_cutoff`, body-verified (served body equals the
selected snapshot), `warnings: []`, `limitations: []`. It is **not** a backtest
fixture and asserts no judgment.

## Case context (roster-stated; not independently verified here)

From the consumer-demand candidate pool (candidate #4):

- **Decision being backtested:** Kinder Beauty's beauty-box economics pivot (~March 2023).
- **Cutoff:** 2023-03-01 (captures select the latest snapshot at or before each declared cutoff).
- **Known later outcome:** shutdown January 2024; pre-announcement decay reported by r/BeautyBoxes.

The outcome above is roster-stated context, **not** an independently sealed or
verified outcome record for this case (Beauty Pie has one; this case does not yet).

## Captured evidence (real Source Capture packets, body-verified, pre-cutoff)

| E | what it sources | declared cutoff | selected snapshot | body bytes | sha256 (body) | packet |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | kinderbeauty.com homepage, cutoff-proximate | 2023-03-01 | 2023-02-27 | 290723 | `45309ab7…a7439bbf` | `source_captures/e1_homepage/` |
| E2 | kinderbeauty.com homepage, mid-window trajectory point | 2022-09-01 | 2022-08-31 | 272523 | `46eb60f2…5198c44e` | `source_captures/e2_homepage/` |
| E3 | kinderbeauty.com homepage, ~1y-before trajectory point | 2022-03-01 | 2022-02-27 | 240983 | `31a8498b…39f2edd0` | `source_captures/e3_homepage/` |

The three points form a ~1-year pre-cutoff homepage trajectory (Feb 2022 →
Aug 2022 → Feb 2023). Body size grew across the window; **the change is recorded
as a fact, not interpreted** — what the offer/pricing actually was at each point
is not asserted here (the raw HTML body is preserved for a later parser/judgment
step; this capture does not parse or extract page meaning).

## Honest limitations

- **Homepage-only.** Only the homepage URL is captured. Distinct page paths
  (pricing/plans, how-it-works, products) were not captured: a `/pages/how-it-works`
  probe 404'd on Wayback and a broader CDX page-path sweep was flaky. Additional
  page-type and macro/context evidence units are deferred, not done.
- **No fixture.** No participant packets, facilitator ledger, sealed outcome,
  paired-packet design, or evaluation exist for this case. Those are judgment-spine
  work (cf. the near-half backtest-learning lane / the Beauty Pie fixture), not
  built by this capture run.
- **Content not parsed.** Per INV-1, capture records observed facts + limits and
  introduces no weights, scores, ranks, or verdicts.

## Non-claims

Not validation, not readiness, not a backtest fixture, not a band input, not a
sealed outcome, not contestant-visible, not Cleaning/ECR/Judgment, not buyer
proof. Product-learning tier, capture-only, N=3 homepage snapshots.
