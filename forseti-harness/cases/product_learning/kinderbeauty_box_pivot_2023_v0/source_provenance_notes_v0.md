---
retrieval_header_version: 1
artifact_role: Capture-side source-provenance record (capture-spine deliverable; NOT a fixture, band input, or contestant-visible packet)
scope: >
  Per-evidence-unit provenance for the pre-cutoff Wayback capture set of case
  kinderbeauty_box_pivot_2023_v0: a homepage trajectory plus a set of
  decision-relevant pre-cutoff pages, captured via the archive_org adapter.
  Records the selected snapshots, body hashes, and honest coverage limits. This
  is a capture-spine evidence set, not a backtest fixture: no participant
  packets, facilitator ledger, sealed outcome, or evaluation exist for this
  case yet.
use_when:
  - Auditing what the Kinder Beauty box-pivot case is archive-sourced from so far.
  - Deciding what a later judgment-spine fixture for this case would still need.
authority_boundary: retrieval_only
open_next:
  - docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md   # roster row this case came from (candidate #4)
  - forseti/product/case_families/product_learning/other_verticals/forseti_backtest_specimen_unity_runtime_fee_source_packet_v0.md   # the backtest specimen shape a later fixture would mirror
---

# Source Provenance Notes — kinderbeauty_box_pivot_2023_v0 (v0)

Capture-side record. This is the **capture-spine deliverable** for the Kinder
Beauty box-economics-pivot backtest case: bounded pre-cutoff Wayback captures
produced by the `archive_org` adapter (`run_source_capture_archive_packet.py`,
`select_snapshot <= cutoff`). Every unit below is `cutoff_posture: pre_cutoff`,
body-verified (served body equals the selected snapshot), `warnings: []`,
`limitations: []`. It is **not** a backtest fixture and asserts no judgment.

## Case context (roster-stated; not independently verified here)

From the consumer-demand candidate pool (candidate #4):

- **Decision being backtested:** Kinder Beauty's beauty-box economics pivot (~March 2023).
- **Cutoff:** 2023-03-01 (every unit selects the latest snapshot at or before this cutoff).
- **Known later outcome:** shutdown January 2024; pre-announcement decay reported by r/BeautyBoxes.

The outcome above is roster-stated context, **not** an independently sealed or
verified outcome record for this case (Beauty Pie / Topicals have sealed records; this case does not yet).

## Captured evidence (real Source Capture packets, body-verified, pre-cutoff)

### Homepage trajectory (~1 year approaching the cutoff)

| E | source | selected snapshot | body bytes | sha256 (body) | packet |
| --- | --- | --- | --- | --- | --- |
| E1 | kinderbeauty.com homepage, cutoff-proximate | 2023-02-27 | 290723 | `45309ab7…a7439bbf` | `source_captures/e1_homepage/` |
| E2 | kinderbeauty.com homepage, mid-window | 2022-08-31 | 272523 | `46eb60f2…5198c44e` | `source_captures/e2_homepage/` |
| E3 | kinderbeauty.com homepage, ~1y before | 2022-02-27 | 240983 | `31a8498b…39f2edd0` | `source_captures/e3_homepage/` |

### Decision-relevant pages (box economics / subscription mechanics)

| E | page | selected snapshot | body bytes | sha256 (body) | packet |
| --- | --- | --- | --- | --- | --- |
| E4 | `/pages/bundler` — box bundling / checkout mechanism | 2023-02-06 | 229510 | `3b51d570…da830236` | `source_captures/e4_bundler/` |
| E5 | `/pages/choose-your-box` — box / subscription selection | 2023-02-05 | 243704 | `4297195b…043f65ef` | `source_captures/e5_choose_your_box/` |
| E6 | `/pages/how-to-cancel` — cancellation policy (churn surface) | 2023-02-05 | 233134 | `fbc3d7f6…130be3dc` | `source_captures/e6_how_to_cancel/` |
| E7 | `/pages/16-first-box` — first-box acquisition offer | 2022-12-08 | 384978 | `ac2be6af…9daad394` | `source_captures/e7_first_box/` |
| E8 | `/pages/customer-help` — FAQ / support | 2023-02-05 | 292457 | `d47c932e…96df883d` | `source_captures/e8_customer_help/` |
| E10 | `/collections/bestsellers` — product highlights | 2023-02-05 | 480775 | `832d3c09…6769e03a` | `source_captures/e10_bestsellers/` |
| E11 | `/pages/brands` — featured-brand curation | 2022-11-30 | 282640 | `9a301008…eb19b5f1` | `source_captures/e11_brands/` |
| E12 | `/pages/april-2022-box` — an example monthly box | 2023-02-01 | 238534 | `b33c015f…ae78ce8e` | `source_captures/e12_april_2022_box/` |

11 body-verified units. Page content is **recorded, not interpreted** — the raw
HTML body is preserved for a later parser/judgment step; what the offer/pricing/
box contents actually were is not asserted here (capture preserves bytes + provenance only).

## Honest coverage limits

- **E9 (`/collections/all`) not captured.** The archive.org CDX endpoint returned
  repeated `503 Service Unavailable` for that URL across two attempts (rate-limited
  during batch capture); it is dropped rather than committed as an empty attempt.
  Other product/collection pages (E10 bestsellers) captured fine.
- **Not archived / not findable on Wayback** (per a bounded discovery sweep):
  pre-cutoff **r/BeautyBoxes thread-level** discussion (the subreddit home is archived,
  but specific Kinder Beauty threads are sparse), **press/news** coverage, a **careers /
  Greenhouse/Lever** board (none found — so no hiring trajectory like Beauty Pie's), and
  an **about/our-story** page.
- **Content not parsed** (INV-1): capture records observed facts + limits and introduces
  no weights, scores, ranks, or judgment.
- **Line endings:** capture raw files commit under repo-wide `autocrlf=true` with no
  `.gitattributes` (matching the existing Beauty Pie / Topicals precedent). The committed
  blobs are byte-faithful (blob sha256 = the manifest sha256 above); a Windows working-copy
  checkout shows CRLF-inflated sizes. Marking `source_captures/** -text` repo-wide is the
  correct fix but would re-touch the frozen Beauty Pie / Topicals fixtures, so it is left as
  an owner-gated hygiene call.

## Non-claims

Not validation, not readiness, not a backtest fixture, not a band input, not a
sealed outcome, not contestant-visible, not Cleaning/ECR/Judgment, not buyer
proof. Product-learning tier, capture-only, N=11 pre-cutoff snapshots.
