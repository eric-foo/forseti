---
retrieval_header_version: 1
artifact_role: Capture-side source-provenance record (capture-spine deliverable; NOT a fixture, band input, or contestant-visible packet)
scope: >
  Per-evidence-unit provenance for the pre-cutoff Wayback capture set of case
  selflessbyhyram_target_entry_2023_v0. Records what is archive-captured (a
  homepage trajectory + product collection + about page), the selected snapshots
  and body hashes, and the honest limits. This is a capture-spine starter set,
  not a backtest fixture: no participant packets, no facilitator ledger, no sealed
  outcome, no evaluation exist for this case yet.
use_when:
  - Auditing what the Selfless by Hyram Target-entry case is archive-sourced from so far.
  - Deciding what a later judgment-spine fixture for this case would still need.
authority_boundary: retrieval_only
open_next:
  - docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md   # roster row this case came from (candidate #7)
  - docs/decisions/judgment_spine_backtest_batch2_candidate_routing_v0.md   # batch-2 routing note referencing this brand (row 7, FAME-founder flag)
---

# Source Provenance Notes — selflessbyhyram_target_entry_2023_v0 (v0)

Capture-side record. This is the **capture-spine deliverable** for the Selfless
by Hyram Target-repricing-entry backtest case: a bounded set of pre-cutoff
Wayback captures across homepage trajectory, product collection, and about pages,
produced by the `archive_org` adapter (`run_source_capture_archive_packet.py`,
`select_snapshot <= cutoff`). Each capture is `cutoff_posture: pre_cutoff`,
body-verified (served body equals the selected snapshot), `warnings: []`,
`limitations: []`. It is **not** a backtest fixture and asserts no judgment.

## Domain note

The primary registered domain `selflessbyhyram.com` redirects (HTTP 301) to
`us.selflessbyhyram.com/`. All Wayback coverage of the US-storefront is indexed
under `us.selflessbyhyram.com`. The root domain has only 301-redirect captures
pre-cutoff; no 200-OK HTML snapshots exist there. All captures in this set use
the actual storefront domain `us.selflessbyhyram.com`. Domain verified live
(`curl -sI https://selflessbyhyram.com/ → location: https://us.selflessbyhyram.com/`)
and confirmed against CDX prior to capture.

## Case context (roster-stated; not independently verified here)

From the consumer-demand candidate pool (candidate #7):

- **Decision being backtested:** Selfless by Hyram's Target repricing entry (~Feb 2023).
- **Cutoff:** 2023-02-01 (captures select the latest snapshot at or before declared cutoff per evidence unit).
- **Known later outcome:** Target exit April 2025; the mass-retail strategy did not hold.

Channel saga (roster-stated): Sephora exit → Target repricing entry (Feb 2023)
→ founder buyback → Target exit (Apr 2025).

The outcome above is roster-stated context, **not** an independently sealed or
verified outcome record for this case. Batch-2 routing notes flag this brand as
FAME (founder Hyram Yarbro) — that is a downstream blind-fixture concern; it
does not affect capture.

## Cutoff rationale

The instructed cutoff is 2023-02-01 (14-digit: `20230201000000`). This pins the
state just before the Feb 2023 Target repricing entry — the cleanest single
decision point. CDX coverage under `us.selflessbyhyram.com` shows an unbroken
monthly-or-better homepage series through Jan 2023 (`20230111170448` is the
latest pre-cutoff homepage snapshot). Per-evidence cutoffs were tightened to the
nearest clearly pre-event month for trajectory units (E2: Oct 2022, E3: Apr 2022)
to achieve a spread; those are still pre-cutoff relative to Feb 2023.

## Captured evidence (real Source Capture packets, body-verified, pre-cutoff)

| E | what it sources | declared cutoff | selected snapshot | body bytes | sha256 (body) | packet |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | us.selflessbyhyram.com homepage, cutoff-proximate | 2023-02-01 | 2023-01-27 | 251307 | `42a754db…63c4d77` | `source_captures/e1_homepage_20230111/` |
| E2 | us.selflessbyhyram.com homepage, mid-window trajectory point | 2022-10-31 | 2022-10-06 | 255222 | `f54f94f1…516d5d2` | `source_captures/e2_homepage_20221002/` |
| E3 | us.selflessbyhyram.com homepage, ~1y-before trajectory point | 2022-04-01 | 2022-03-31 | 247298 | `9bf9a700…4f5aebf` | `source_captures/e3_homepage_20220301/` |
| E4 | us.selflessbyhyram.com/collections/all, product assortment pre-entry | 2023-02-01 | 2022-11-29 | 276085 | `06bf53dd…3ff3b8c2` | `source_captures/e4_collections_all_20221129/` |
| E5 | us.selflessbyhyram.com/pages/about-us, brand positioning pre-entry | 2023-02-01 | 2023-01-27 | 191661 | `eacedc47…99914dbe2` | `source_captures/e5_about_20230127/` |
| E6 | us.selflessbyhyram.com/collections/eddies-routine, DTC routine curvature pre-entry | 2023-02-01 | 2023-01-27 | 208107 | `88fbe0c5…71f15892` | `source_captures/e6_eddies_routine_20230127/` |

The three homepage points form a ~10-month pre-cutoff trajectory (Mar 2022 →
Oct 2022 → Jan 2023). Body size variation across the window is recorded as a
fact, not interpreted — what the offer/pricing/channel language actually was at
each point is not asserted here (the raw HTML body is preserved for a later
parser/judgment step; this capture does not parse or extract page meaning).

E4 (`collections/all`) preserves the product assortment page. E5 (`about-us`)
preserves brand-positioning copy. E6 (`collections/eddies-routine`) preserves a
founder-routine curated collection, a DTC-channel-facing artifact; `evelyns-routine`
was present on CDX but not captured (bounded to 6 units per instructions).

## Honest limitations

- **No channel/retailer page.** No dedicated where-to-buy, stockist, or retailer
  page was found in CDX under `us.selflessbyhyram.com/pages/` pre-cutoff (probed
  `where-to-buy`, `retail*`, `sephora*` — all returned empty). The Sephora-era
  channel signal, if present, must be inferred from homepage/collection body if at
  all; that inference is deferred to the judgment spine.
- **No evelyns-routine capture.** CDX shows `collections/evelyns-routine` with
  `20230127104709` coverage; not captured (bounded scope). Deferred, not done.
- **E4 is Nov 2022, not Jan 2023.** The `collections/all` Wayback snapshot
  nearest to cutoff is `20221129190852`; no later 200-OK snapshot exists pre-cutoff
  for that path. This is the real snapshot selected; gap noted.
- **No fixture.** No participant packets, facilitator ledger, sealed outcome,
  paired-packet design, or evaluation exist for this case. Those are judgment-spine
  work, not built by this capture run.
- **Content not parsed.** Per INV-1, capture records observed facts + limits and
  introduces no weights, scores, ranks, or verdicts.
- **FAME flag.** Batch-2 routing marks this brand FAME (founder Hyram Yarbro).
  That is a downstream blind-fixture concern (isolation screen required before any
  judgment); it has no bearing on this capture-spine deliverable.

## Non-claims

Not validation, not readiness, not a backtest fixture, not a band input, not a
sealed outcome, not contestant-visible, not Cleaning/ECR/Judgment, not buyer
proof. Product-learning tier, capture-only, N=6 snapshots across homepage
trajectory + product collection + about page.
