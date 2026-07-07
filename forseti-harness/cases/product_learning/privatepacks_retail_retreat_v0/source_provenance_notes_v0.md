---
retrieval_header_version: 1
artifact_role: Capture-side source-provenance record (capture-spine deliverable; NOT a fixture, band input, or contestant-visible packet)
scope: >
  Per-evidence-unit provenance for the pre-cutoff Wayback capture set of case
  privatepacks_retail_retreat_v0: a homepage trajectory plus a set of
  decision-relevant pre-cutoff pages (store-locator, wholesale/retail-partner,
  product, catalog, brand, mechanics), captured via the archive_org adapter.
  Records the selected snapshots, body hashes, and honest coverage limits. This
  is a capture-spine evidence set, not a backtest fixture: no participant
  packets, facilitator ledger, sealed outcome, or evaluation exist for this
  case yet.
use_when:
  - Auditing what the Private Packs retail-retreat case is archive-sourced from so far.
  - Deciding what a later judgment-spine fixture for this case would still need.
authority_boundary: retrieval_only
open_next:
  - docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md   # roster row this case came from (candidate #3)
  - forseti/product/case_families/product_learning/other_verticals/forseti_backtest_specimen_unity_runtime_fee_source_packet_v0.md   # the backtest specimen shape a later fixture would mirror
---

# Source Provenance Notes — privatepacks_retail_retreat_v0 (v0)

Capture-side record. This is the **capture-spine deliverable** for the Private
Packs retail-retreat / DTC-pivot backtest case: bounded pre-cutoff Wayback
captures produced by the `archive_org` adapter (`run_source_capture_archive_packet.py`,
`select_snapshot <= cutoff`). Every unit below is `cutoff_posture: pre_cutoff`,
body-verified (served body equals the selected snapshot), `warnings: []`,
`limitations: []`. It is **not** a backtest fixture and asserts no judgment.

## Case context (roster-stated; not independently verified here)

From the consumer-demand candidate pool (candidate #3):

- **Decision being backtested:** Private Packs' retail retreat from ~1,000 CVS + ~250 Target doors on a velocity miss (category expected ~4–6 units/wk; ~$100K retail infrastructure written off) → DTC pivot.
- **Cutoff:** 2025-05-01 (every unit selects the latest snapshot at or before this cutoff; see cutoff rationale below).
- **Known later outcome:** retail retreat from the CVS + Target footprint; ~$100K retail infra written off; pivot back to DTC. Reported (per the screen-2 source ledger) by Beauty Independent, "Private Packs founder walked away from retail distribution."

The outcome above is roster-stated context, **not** an independently sealed or
verified outcome record for this case (Beauty Pie / Topicals have sealed records; this case does not yet).

### Cutoff rationale and uncertainty

The screen-2 source ledger
(`docs/decisions/judgment_spine_backtest_batch2_candidate_routing_v0.md`) dates the
retail-retreat / DTC-pivot decision as **"by June 2025"** — i.e., the retreat was
public by June 2025 — but does **not** pin a day-level public-announcement date.
**2025-05-01** is selected as a defensible pre-decision cutoff: it sits clearly
before the June 2025 public marker, captures the full retail-era trajectory, and
leaves the next-later homepage snapshot (2025-05-16, outside the window) as a
margin. The exact in-window decision day is uncertain; if a later source pins a
specific announcement date, this cutoff should be re-checked against it. The
cutoff is a capture boundary, not a claim about when the decision was made.

## Captured evidence (real Source Capture packets, body-verified, pre-cutoff)

### Homepage trajectory (~1 year approaching the cutoff)

| E | source | selected snapshot | body bytes | sha256 (body) | packet |
| --- | --- | --- | --- | --- | --- |
| E1 | privatepacks.com homepage, cutoff-proximate | 2025-04-28 | 263306 | `f12b7541…bd0947b1` | `source_captures/e1_homepage/` |
| E2 | privatepacks.com homepage, mid-window | 2024-08-16 | 363904 | `a5c3fb52…e0d580cf` | `source_captures/e2_homepage/` |
| E3 | privatepacks.com homepage, ~1y before | 2024-05-22 | 358264 | `53f37f7d…2fd581aa` | `source_captures/e3_homepage/` |

### Decision-relevant pages (retail-vs-DTC surfaces)

| E | page | selected snapshot | body bytes | sha256 (body) | packet |
| --- | --- | --- | --- | --- | --- |
| E4 | `/pages/store-locator` — retail-door footprint (retail-presence surface) | 2025-04-28 | 254248 | `3386964f…3991acd5` | `source_captures/e4_store_locator/` |
| E5 | `/pages/wholesale` — wholesale / retail-partner program | 2025-02-19 | 237178 | `36bf14b2…7831e03f` | `source_captures/e5_wholesale/` |
| E6 | `/products/private-packs` — core product page (the velocity-miss unit) | 2025-03-16 | 417872 | `2597a991…0c3033fd` | `source_captures/e6_product/` |
| E7 | `/collections/all` — full catalog | 2025-02-19 | 260578 | `0bd2893d…76364847` | `source_captures/e7_collections_all/` |
| E8 | `/pages/our-story-2023` — brand / about | 2025-02-19 | 243114 | `644b2fa1…f0e7410f` | `source_captures/e8_our_story/` |
| E9 | `/pages/how-it-works-2023` — product mechanics | 2025-04-28 | 276320 | `e5df8ca7…5745f859` | `source_captures/e9_how_it_works/` |

9 body-verified units. Page content is **recorded, not interpreted** — the raw
HTML body is preserved for a later parser/judgment step; what the retail
footprint / product / wholesale terms actually were is not asserted here
(capture preserves bytes + provenance only).

## Honest coverage limits

- **E9 (`/pages/how-it-works-2023`) required a retry.** The first attempt's CDX
  availability query returned `HTTP 504 Gateway Time-out` with an unparseable body
  (rate-limited during batch capture), producing `selected_snapshot: None` /
  `archive_history_posture: attempt_failed`; that failed packet was deleted and
  re-run, and the retry preserved a real pre-cutoff snapshot body. The committed
  E9 packet is the clean retry.
- **`/apps/store-locator/` not captured.** That store-locator *app* surface has no
  pre-cutoff `text/html 200` snapshot on Wayback CDX (it is a JS app endpoint, not
  an archived HTML page); the canonical retail surface `/pages/store-locator` (E4)
  is captured instead. No empty attempt is committed for it.
- **`/pages/about-us` not used.** The empty `/pages/about-us` path has no pre-cutoff
  HTML snapshots; the live brand/about surface in the cutoff window is
  `/pages/our-story-2023` (E8), which is what was captured.
- **Not captured / out of bounded scope** (commissioned to this one case; no
  exhaustive crawl): per-retailer detail beyond the store-locator page, press/news
  coverage of the retreat (the decision marker itself), the blog channel
  (`/blogs/whats-up-down-there`, including retail-collab posts), and the
  internationalized locale paths (`/en-ca`, `/en-gb`).
- **Content not parsed** (INV-1): capture records observed facts + limits and introduces
  no weights, scores, ranks, or judgment.
- **Line endings:** capture raw files commit under repo-wide `autocrlf=true` with no
  `.gitattributes` (matching the existing Beauty Pie / Topicals / Kinder Beauty
  precedent). The committed body blobs are byte-faithful (working-copy `02_*.bin`
  sha256 = the manifest sha256 above; the `.bin` bodies are binary, so autocrlf does
  not rewrite them). Marking `source_captures/** -text` repo-wide is the correct fix
  but would re-touch the frozen prior fixtures, so it is left as an owner-gated
  hygiene call.

## Non-claims

Not validation, not readiness, not a backtest fixture, not a band input, not a
sealed outcome, not contestant-visible, not Cleaning/ECR/Judgment, not buyer
proof. Product-learning tier, capture-only, N=9 pre-cutoff snapshots.
