---
retrieval_header_version: 1
artifact_role: Capture-side source-provenance record (capture-spine deliverable; NOT a fixture, band input, or contestant-visible packet)
scope: >
  Per-evidence-unit provenance for the pre-cutoff Wayback capture set of case
  joahbeauty_cvs_kill_2024_v0: a homepage trajectory plus a set of
  decision-relevant pre-cutoff pages, captured via the archive_org adapter.
  Records the selected snapshots, body hashes, and honest coverage limits. This
  is a capture-spine evidence set, not a backtest fixture: no participant
  packets, facilitator ledger, sealed outcome, or evaluation exist for this
  case yet.
use_when:
  - Auditing what the Joah Beauty CVS-kill case is archive-sourced from so far.
  - Deciding what a later judgment-spine fixture for this case would still need.
authority_boundary: retrieval_only
open_next:
  - docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md   # roster row this case came from (candidate #1)
  - forseti/product/case_families/product_learning/other_verticals/forseti_backtest_specimen_unity_runtime_fee_source_packet_v0.md   # the backtest specimen shape a later fixture would mirror
---

# Source Provenance Notes — joahbeauty_cvs_kill_2024_v0 (v0)

Capture-side record. This is the **capture-spine deliverable** for the Joah
Beauty CVS-exclusive K-beauty line-kill backtest case: bounded pre-cutoff
Wayback captures produced by the `archive_org` adapter
(`run_source_capture_archive_packet.py`, `select_snapshot <= cutoff`). Every
unit below is `cutoff_posture: pre_cutoff`, body-verified (served body equals
the selected snapshot), `warnings: []`, `limitations: []`. It is **not** a
backtest fixture and asserts no judgment.

## Case context (roster-stated; not independently verified here)

From the consumer-demand candidate pool (candidate #1; screen-2 ledger):

- **Decision being backtested:** Joah Beauty (Kiss Products) wound down its
  CVS-exclusive (~4,000 doors) K-beauty line — socials wiped after June 2024.
- **Cutoff:** 2024-06-01 (every unit selects the latest snapshot at or before
  this cutoff; see cutoff rationale below).
- **Known later outcome:** April 2025 closure + 50%-off liquidation; the silent
  wind-down was detected by r/BeautyGuruChatter and laundered into the trade
  record by Beauty Independent (April 2025).

The outcome above is roster-stated context (screen-2 beauty ledger,
`docs/decisions/venue_procedure_proving_screen_beauty_ledger_v0.md`), **not** an
independently sealed or verified outcome record for this case (Beauty Pie /
Topicals have sealed records; this case does not yet).

### Cutoff rationale + uncertainty

The decision being backtested is the **kill / wind-down**, whose first public
signal (per the roster) is the social-media wipe that occurred **after June
2024**. The cutoff is therefore pinned at **2024-06-01** (14-digit cutoff
timestamp `20240601000000`): the latest moment that is unambiguously **before**
the wind-down signal, so the captured site state reflects the live, pre-kill
brand. Wayback has a homepage snapshot at `20240601011941` (June 1, 01:19 UTC),
which falls just *after* the `20240601000000` cutoff instant and is therefore
excluded by `select_snapshot <= cutoff`; the homepage units instead resolve to
the latest at-or-before-cutoff snapshots (2024-05-20 and earlier). **Uncertainty:**
the exact line-kill *decision* date is not in the public record — only the
~June-2024 socials wipe and the April 2025 closure are dated — so 2024-06-01 is a
conservative pre-signal cutoff, not a pinned decision date. The CVS-exclusive
relationship is an offline retail channel; the captured site is the DTC Shopify
storefront and does not itself date the CVS deal.

## Captured evidence (real Source Capture packets, body-verified, pre-cutoff)

Primary domain: **joahbeauty.com** (verified archived on Wayback CDX; the live
storefront resolves on `www.joahbeauty.com`, a Shopify store). Confirmed dense
pre-cutoff homepage coverage 2018–2024.

### Homepage trajectory (~1 year approaching the cutoff)

| E | source | selected snapshot | body bytes | sha256 (body) | packet |
| --- | --- | --- | --- | --- | --- |
| E1 | www.joahbeauty.com homepage, cutoff-proximate | 2024-05-20 | 421060 | `ae32bab2…118954f6` | `source_captures/e1_homepage/` |
| E2 | www.joahbeauty.com homepage, mid-window | 2023-12-14 | 400329 | `90736cf8…f2c49211` | `source_captures/e2_homepage/` |
| E3 | www.joahbeauty.com homepage, ~1y before | 2023-04-07 | 947203 | `45b936db…9f4cb1d5` | `source_captures/e3_homepage/` |

### Decision-relevant pages (brand / catalog / retail-channel surfaces)

| E | page | selected snapshot | body bytes | sha256 (body) | packet |
| --- | --- | --- | --- | --- | --- |
| E4 | `/pages/about` — brand / our-story | 2024-05-20 | 169869 | `039b9dbd…9c9ce3dd` | `source_captures/e4_about/` |
| E5 | `/collections/all` — full product catalog | 2024-05-20 | 806417 | `d8e7ec4e…632f7bd9` | `source_captures/e5_collections_all/` |
| E6 | `/collections` — collections index | 2024-05-20 | 339494 | `49336b38…20b6c6ae` | `source_captures/e6_collections/` |
| E7 | `/pages/joah-la-pop-up` — retail / pop-up presence | 2024-04-15 | 158160 | `c8d4d294…56cb4489` | `source_captures/e7_joah_la_pop_up/` |
| E8 | `/pages/bundles` — bundle / offer construction | 2024-04-15 | 172136 | `9d1f1027…b236438c` | `source_captures/e8_bundles/` |
| E9 | `/pages/contact` — contact / support surface | 2024-05-20 | 156834 | `31f2dbed…058792fb` | `source_captures/e9_contact/` |
| E10 | `/blogs/news` — brand news / announcements | 2024-03-03 | 152545 | `a055417e…4a95b115` | `source_captures/e10_blogs_news/` |
| E11 | `/pages/affiliate-program` — affiliate / acquisition channel | 2024-04-15 | 363983 | `be0e8d61…0eed55ba` | `source_captures/e11_affiliate_program/` |

11 body-verified units. Page content is **recorded, not interpreted** — the raw
HTML body is preserved for a later parser/judgment step; what the
catalog/offer/brand copy actually said is not asserted here (capture preserves
bytes + provenance only).

## Honest coverage limits

- **E7 / E8 / E10 each failed body retrieval once before succeeding.** On the
  first batch pass the archive.org snapshot-serving host transiently refused the
  body fetch (`WinError 10061` / connection refused) for `/pages/joah-la-pop-up`,
  `/pages/bundles`, and `/blogs/news` — the CDX availability succeeded (snapshot
  selected, HTTP 200) but no body was preserved. Each failed attempt directory
  was deleted (not committed as an empty `NO_BODY` packet) and recaptured
  sequentially with a wait; all three then preserved a real body. The same
  transient refusal also hit two homepage/catalog attempts (E3 homepage, E5
  `/collections/all`) on the availability fetch before they were retried clean.
  No empty attempt was committed.
- **No dedicated "where to buy" / CVS stockist page captured.** The
  CVS-exclusive (~4,000 doors) relationship that defines this decision is an
  offline retail channel; the archived site is the DTC Shopify storefront and
  exposes no store-locator/stockist page in the pre-cutoff bounded discovery
  sweep. `/pages/joah-la-pop-up` (E7) is the closest archived retail-presence
  surface. The CVS relationship itself is therefore **not** evidenced by these
  captures and would need a separate (likely press/trade) source.
- **Not captured by design** (bounded, commissioned to this one case): per-SKU
  product-detail pages (the catalog is represented by `/collections/all` and
  `/collections`), the social accounts whose wipe is the decision signal (not on
  this domain), and **press/news/Reddit** coverage of the wind-down (the
  r/BeautyGuruChatter detection and the Beauty Independent April-2025 closure
  story live off-domain and were not sourced here).
- **Content not parsed** (INV-1): capture records observed facts + limits and
  introduces no weights, scores, ranks, or judgment.
- **Line endings:** capture raw files commit under repo-wide `autocrlf=true`
  with no `.gitattributes` (matching the existing Beauty Pie / Topicals / Kinder
  Beauty precedent). The committed blobs are byte-faithful (blob sha256 = the
  manifest sha256 above; verified by re-hashing each preserved body); a Windows
  working-copy checkout shows CRLF-inflated sizes. Marking `source_captures/**
  -text` repo-wide is the correct fix but would re-touch the frozen Beauty Pie /
  Topicals / Kinder fixtures, so it is left as an owner-gated hygiene call.

## Non-claims

Not validation, not readiness, not a backtest fixture, not a band input, not a
sealed outcome, not contestant-visible, not Cleaning/ECR/Judgment, not buyer
proof. Product-learning tier, capture-only, N=11 pre-cutoff snapshots.
