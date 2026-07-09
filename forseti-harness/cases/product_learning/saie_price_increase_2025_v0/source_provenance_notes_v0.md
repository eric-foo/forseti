---
retrieval_header_version: 1
artifact_role: Capture-side source-provenance record (capture-spine deliverable; NOT a fixture, band input, or contestant-visible packet)
scope: >
  Per-evidence-unit provenance for the pre-cutoff Wayback capture set of case
  saie_price_increase_2025_v0. Records what is archive-captured (a homepage
  trajectory plus a set of decision-relevant product/collection pages showing
  pre-increase prices), the selected snapshots and body hashes, and the honest
  limits. This is a capture-spine starter set, not a backtest fixture: no
  participant packets, no facilitator ledger, no sealed outcome, no evaluation
  exist for this case yet.
use_when:
  - Auditing what the Saie price-increase case is archive-sourced from so far.
  - Deciding what a later judgment-spine fixture for this case would still need.
authority_boundary: retrieval_only
open_next:
  - docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md   # roster row this case came from (candidate C2)
  - docs/decisions/beauty_subtle_decision_screen3_ledger_v0.md             # screen-3 ledger receipt for the Saie decision + outcome
---

# Source Provenance Notes — saie_price_increase_2025_v0 (v0)

Capture-side record. This is the **capture-spine deliverable** for the Saie
price-increase backtest case: a bounded set of pre-cutoff Wayback captures,
produced by the `archive_org` adapter (`run_source_capture_archive_packet.py`,
`select_snapshot <= cutoff`). Each capture is `cutoff_posture: pre_cutoff`,
body-verified (served body equals the selected snapshot; no availability≠body
redirect), `warnings: []`, `limitations: []`. It is **not** a backtest fixture
and asserts no judgment.

## Case context (roster-stated; not independently verified here)

From the consumer-demand candidate pool (candidate C2):

- **Decision being backtested:** Saie's price increase of **+$1–4** on its clean-makeup line (~June 2025).
- **Cutoff:** 2025-06-01 (14-digit `20250601000000`; captures select the latest snapshot at or before each declared cutoff). The ledgers state the decision month as "June 2025" with no tighter date, so the cutoff is pinned just before the increase at ~2025-06-01.
- **Domain:** `saiehello.com` is the archived Saie storefront (dense pre-cutoff Wayback coverage, monthly homepage snapshots through 2025-05; the `saie.com` alternative was not needed — `saiehello.com` is conclusively the archived store).
- **Known later outcome:** the increase **PERSISTED into 2026** (BeautyMatter's 2026 tariff piece lists Saie among brands that raised; brand IG/FB community tariff-update posts are the action receipts — recorded as pointers, not followed).

The outcome above is roster-stated context (screen-3 ledger / candidate pool),
**not** an independently sealed or verified outcome record for this case
(Beauty Pie / Topicals have sealed records; this case does not yet).

## Captured evidence (real Source Capture packets, body-verified, pre-cutoff)

### Homepage trajectory (~10 months approaching the cutoff)

| E | what it sources | declared cutoff | selected snapshot | body bytes | sha256 (body) | packet |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | saiehello.com homepage, cutoff-proximate | 2025-06-01 | 2025-05-23 | 1828786 | `3730750c…e93ad5f3` | `source_captures/e1_homepage/` |
| E2 | saiehello.com homepage, mid-window trajectory point | 2024-12-01 | 2024-11-26 | 3418345 | `c8bf892a…170d9f29` | `source_captures/e2_homepage/` |
| E3 | saiehello.com homepage, ~10mo-before trajectory point | 2024-07-15 | 2024-07-14 | 2490346 | `29afbef3…95c922fc` | `source_captures/e3_homepage/` |

### Decision-relevant pages (pre-increase price surfaces; all cutoff 2025-06-01)

| E | page | selected snapshot | body bytes | sha256 (body) | packet |
| --- | --- | --- | --- | --- | --- |
| E4 | `/collections/all` — full catalog grid | 2025-04-28 | 4125876 | `a47a3a80…e18f5223` | `source_captures/e4_collections_all/` |
| E5 | `/collections/bestsellers` — hero-product grid | 2025-05-22 | 3524557 | `b2db2d0c…98e2d6f3` | `source_captures/e5_bestsellers/` |
| E6 | `/products/dew-blush` — hero blush PDP | 2025-05-14 | 1230136 | `34835379…896d21af` | `source_captures/e6_dew_blush/` |
| E7 | `/products/clean-mascara-101` — Mascara 101 PDP | 2025-04-28 | 1092995 | `e088d95c…733bb001` | `source_captures/e7_clean_mascara_101/` |
| E8 | `/products/airset` — setting-spray PDP | 2025-04-28 | 1005173 | `ddce3c3b…56d24b0f` | `source_captures/e8_airset/` |
| E9 | `/products/blush-n-glow` — Blush & Glow PDP | 2025-03-20 | 1225000 | `52cbbedf…e9946e87` | `source_captures/e9_blush_n_glow/` |
| E10 | `/products/complexion-boost` — Complexion Boost PDP | 2025-04-28 | 974906 | `e82a4c16…5fdf9143` | `source_captures/e10_complexion_boost/` |

10 body-verified units. The three homepage points form a ~10-month pre-cutoff
trajectory (Jul 2024 → Nov 2024 → May 2025); the seven decision-relevant pages
are the catalog grid, the bestsellers grid, and five hero-product PDPs, captured
cutoff-proximate (Mar–May 2025) — i.e. the **pre-increase price surfaces** for a
price-increase decision. Page content is **recorded, not interpreted**: the raw
HTML body of each snapshot **preserves the old (pre-increase) prices** in-bytes,
but those prices are **not parsed, extracted, or asserted here** and **no price
delta is computed** (capture preserves bytes + provenance only; a later
parser/judgment step would read the bodies).

## Honest limitations

- **Prices preserved, not parsed (INV-1).** Each product/collection body contains
  price tokens, but this capture asserts no price value and computes no `+$1–4`
  delta against any later snapshot. The increase magnitude and persistence are
  roster-stated outcome context, not derived here.
- **Outcome receipts not captured.** The persistence evidence named by the roster —
  the BeautyMatter 2026 raiser list and the brand IG/FB tariff-update posts — is
  **not** in this set. The IG/FB posts are login-gated social surfaces (pointers
  recorded, not followed, per screen policy); a 2026 BeautyMatter capture is
  post-cutoff outcome material, out of scope for a pre-cutoff evidence set.
- **Snapshot clustering.** E4/E7/E8/E10 each selected the 2025-04-28 snapshot day
  (the densest archive day before the cutoff); E5 (2025-05-22), E6 (2025-05-14),
  and E9 (2025-03-20) differ. All are the latest pre-cutoff snapshot for their URL.
- **Bounded set, no exhaustive crawl.** Hero PDPs were chosen from CDX-confirmed
  clean base-slug coverage; product **variant/query-string** snapshot URLs and the
  full PDP catalog were not swept. Several flagship slugs probed (e.g.
  `/products/glowy-super-gel`, `/products/slip-tint`) had no clean base-slug
  pre-cutoff snapshot and were not chased.
- **No fixture.** No participant packets, facilitator ledger, sealed outcome,
  paired-packet design, or evaluation exist for this case. Those are judgment-spine
  work, not built by this capture run.
- **Content not parsed.** Per INV-1, capture records observed facts + limits and
  introduces no weights, scores, ranks, or verdicts.
- **Line endings.** Capture raw files commit under repo-wide `autocrlf=true` with no
  `.gitattributes` (matching the existing Beauty Pie / Topicals / Kinder Beauty
  precedent). The committed blobs are byte-faithful (blob sha256 = the manifest
  sha256 above); a Windows working-copy checkout shows CRLF-inflated sizes.
  Marking `source_captures/** -text` repo-wide is the correct fix but would re-touch
  the frozen fixtures, so it is left as an owner-gated hygiene call.

## Non-claims

Not validation, not readiness, not a backtest fixture, not a band input, not a
sealed outcome, not contestant-visible, not Cleaning/ECR/Judgment, not buyer
proof. No price value, price delta, or persistence is asserted or computed here.
Product-learning tier, capture-only, N=10 pre-cutoff snapshots.
