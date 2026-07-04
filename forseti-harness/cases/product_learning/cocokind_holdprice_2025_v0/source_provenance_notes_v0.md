---
retrieval_header_version: 1
artifact_role: Capture-side source-provenance record (capture-spine deliverable; NOT a fixture, band input, or contestant-visible packet)
scope: >
  Per-evidence-unit provenance for the pre-cutoff Wayback capture set of case
  cocokind_holdprice_2025_v0: a homepage trajectory plus a set of
  decision-relevant pre-cutoff price-evidence pages (collections and specific
  product pages), captured via the archive_org adapter. Records the selected
  snapshots, body hashes, and honest coverage limits. This is a capture-spine
  evidence set, not a backtest fixture: no participant packets, facilitator
  ledger, sealed outcome, or evaluation exist for this case yet.
use_when:
  - Auditing what the cocokind tariff hold-price case is archive-sourced from so far.
  - Deciding what a later judgment-spine fixture for this case would still need.
authority_boundary: retrieval_only
open_next:
  - docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md   # roster row this case came from (completion C1)
  - docs/product/core_spine/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md   # the backtest specimen shape a later fixture would mirror
---

# Source Provenance Notes — cocokind_holdprice_2025_v0 (v0)

Capture-side record. This is the **capture-spine deliverable** for the cocokind
tariff hold-price backtest case: bounded pre-cutoff Wayback captures produced by
the `archive_org` adapter (`run_source_capture_archive_packet.py`,
`select_snapshot <= cutoff`). Every unit below is `cutoff_posture: pre_cutoff`,
body-verified (served body equals the selected snapshot), `warnings: []`,
`limitations: []`. It is **not** a backtest fixture and asserts no judgment.

## Case context (roster-stated; not independently verified here)

From the consumer-demand candidate pool (completion C1; screen-3 ledger):

- **Decision being backtested:** cocokind's tariff-driven hold-price decision (~June 2025) —
  cocokind chose **not** to raise prices despite tariff cost pressure.
- **Cutoff:** 2025-06-01 (cutoff-timestamp `20250601000000`; every unit selects the latest
  snapshot at or before this cutoff). The Glossy statement carrying founder Priscilla Tsai's
  hold-price position is dated **June 2025**, so the cutoff is pinned just before it; the
  screen-3 ledger gives no tighter day-level decision date, so the month boundary is used.
- **Known later outcome:** price **HELD** through at least June 2026 (soft outcome leg:
  absence-of-increase evidence — current site prices reported in the pre-tariff range, and
  cocokind absent from BeautyMatter's 2026 tariff-raiser list).

The outcome above is roster-stated context, **not** an independently sealed or
verified outcome record for this case (Beauty Pie / Topicals have sealed records; this case does not yet).

## Captured evidence (real Source Capture packets, body-verified, pre-cutoff)

### Homepage trajectory (~1 year approaching the cutoff)

| E | source | selected snapshot | body bytes | sha256 (body) | packet |
| --- | --- | --- | --- | --- | --- |
| E1 | cocokind.com homepage, cutoff-proximate | 2025-05-30 | 883383 | `22ab4e99…3cd6420d` | `source_captures/e1_homepage/` |
| E2 | cocokind.com homepage, mid-window | 2024-11-29 | 655124 | `b55fc904…60d224e0` | `source_captures/e2_homepage/` |
| E3 | cocokind.com homepage, ~1y before | 2024-06-25 | 1039534 | `1ef64f52…de01057b` | `source_captures/e3_homepage/` |

### Decision-relevant pages (price evidence: collections + specific product pages)

| E | page | selected snapshot | body bytes | sha256 (body) | packet |
| --- | --- | --- | --- | --- | --- |
| E4 | `/collections/bestsellers` — product highlights w/ prices | 2025-05-23 | 489734 | `11bbd8fd…c846a966` | `source_captures/e4_collection_bestsellers/` |
| E5 | `/collections/all` — full catalog listing w/ prices | 2025-04-18 | 1009656 | `0a32b22d…341ab828` | `source_captures/e5_collection_all/` |
| E6 | `/products/ceramide-barrier-serum` — hero SKU product page | 2025-05-22 | 469144 | `f74b5274…19ba8a9f` | `source_captures/e6_ceramide_barrier_serum/` |
| E7 | `/products/aha-jelly-cleanser` — cleanser product page | 2025-04-18 | 380727 | `7a3e1a9e…93373d10` | `source_captures/e7_aha_jelly_cleanser/` |
| E8 | `/products/beginner-retinol-gel` — retinol product page | 2025-05-22 | 416943 | `78bb8600…3a772eb2` | `source_captures/e8_beginner_retinol_gel/` |
| E9 | `/products/ceramide-lip-blur-balm` — lip-balm product page | 2025-05-01 | 940189 | `a07288ce…23ae11bd` | `source_captures/e9_ceramide_lip_blur_balm/` |
| E10 | `/products/chagaglo-highlighter` — color/highlighter product page | 2025-04-18 | 372727 | `304d378d…767032ed` | `source_captures/e10_chagaglo_highlighter/` |

10 body-verified units. Page content is **recorded, not interpreted** — the raw
HTML body is preserved for a later parser/judgment step. The pre-cutoff product
and collection pages **do contain the on-page price strings in the raw body**
(e.g. `$NN.NN` tokens are present in the preserved HTML), but the price levels
themselves — and any pre/post comparison or delta — are **not parsed, computed,
or asserted here**. Capture preserves bytes + provenance only.

## Honest coverage limits

- **Rate-limited retries during batch capture.** The archive.org CDX / Wayback
  endpoint returned intermittent `503 Service Unavailable` / `504 Gateway Time-out`
  during the batch (E1, E2, and E6 each needed one or more retries before a clean
  body was preserved). Every unit committed here is a clean retry: a failed attempt
  was deleted and re-run rather than committed as an empty/error-body attempt. No
  unit was dropped.
- **Homepage original URL normalization.** The Wayback CDX rows for the homepage
  resolve to `https://www.cocokind.com/` (the `www` host) for the selected snapshots,
  while the product/collection requests resolve to `https://www.cocokind.com/<path>`.
  These are the same registrable domain (`cocokind.com`); the requested locator was
  the bare-host form and the adapter selected the archived `www` snapshot.
- **Not exhaustively crawled.** This is a bounded decision-relevant set (1 homepage
  trajectory + 2 collection listings + 5 specific product pages), not a full
  product-catalog or site crawl. Other product/collection pages exist in the archive
  and were not captured.
- **No independent action/outcome receipts captured here.** The hold-price *decision
  statement* (Glossy, June 2025) and the *held-through-2026* outcome signal
  (BeautyMatter 2026 raiser-list absence; current-site price observation) are
  roster-stated pointers, **not** captured into packets in this set. This set
  preserves only the pre-cutoff cocokind site state (the price level the decision
  was made against).
- **Content not parsed** (INV-1): capture records observed facts + limits and introduces
  no weights, scores, ranks, or judgment.
- **Line endings:** capture raw files commit under repo-wide `autocrlf=true` with no
  `.gitattributes` (matching the existing Beauty Pie / Topicals / Kinder Beauty precedent).
  The committed blobs are byte-faithful (blob sha256 = the manifest sha256 above); a
  Windows working-copy checkout shows CRLF-inflated sizes. Marking `source_captures/** -text`
  repo-wide is the correct fix but would re-touch the frozen prior fixtures, so it is left
  as an owner-gated hygiene call.

## Non-claims

Not validation, not readiness, not a backtest fixture, not a band input, not a
sealed outcome, not contestant-visible, not Cleaning/ECR/Judgment, not buyer
proof, not a price assertion or price-delta computation. Product-learning tier,
capture-only, N=10 pre-cutoff snapshots.
