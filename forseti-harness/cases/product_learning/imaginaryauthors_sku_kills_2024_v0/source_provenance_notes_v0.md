---
retrieval_header_version: 1
artifact_role: Capture-side source-provenance record (capture-spine deliverable; NOT a fixture, band input, or contestant-visible packet)
scope: >
  Per-evidence-unit provenance for the pre-cutoff Wayback capture set of case
  imaginaryauthors_sku_kills_2024_v0. Records what is archive-captured (two
  homepage trajectory points, the two killed-SKU product pages, and the
  full-catalog page), the selected snapshots and body hashes, and the honest
  limits. This is a capture-spine starter set, not a backtest fixture: no
  participant packets, no facilitator ledger, no sealed outcome, no evaluation
  exist for this case yet.
use_when:
  - Auditing what the Imaginary Authors SKU-kills case is archive-sourced from so far.
  - Deciding what a later judgment-spine fixture for this case would still need.
authority_boundary: retrieval_only
open_next:
  - docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md   # roster row this case came from (candidate #9)
  - docs/decisions/beauty_subtle_decision_screen3_ledger_v0.md              # screen 3 source ledger for this candidate's discovery receipt
---

# Source Provenance Notes — imaginaryauthors_sku_kills_2024_v0 (v0)

Capture-side record. This is the **capture-spine deliverable** for the Imaginary
Authors quiet-SKU-kills backtest case: a bounded set of pre-cutoff Wayback
captures produced by the `archive_org` adapter
(`run_source_capture_archive_packet.py`, `select_snapshot <= cutoff`). Each
capture is `cutoff_posture: pre_cutoff`, body-verified (served body equals the
selected snapshot), `warnings: []` or redirect-only, `limitations: []`. It is
**not** a backtest fixture and asserts no judgment.

## Case context (roster-stated; not independently verified here)

From the consumer-demand candidate pool (candidate #9), screen 3 ledger:

- **Decision being backtested:** Imaginary Authors' quiet SKU kills — Whispered Myths
  discontinued ~Aug 2024 ("allocating production funds toward better-selling
  fragrances", sales deadline Aug 18), then Telegrama; product-info page lists 8
  total quiet kills total. Low-sales rationale.
- **Cutoff:** 2024-08-01 (captures select the latest snapshot at or before each
  declared cutoff; pre-kill full catalog is the target state — both named SKUs
  still present pre-cutoff). Cutoff source: roster-stated "Aug 2024 onward" from
  screen 3 ledger row 2; "sales deadline Aug 18" pins the first kill at Aug 2024.
  2024-08-01 is therefore the correct pre-kill cutoff (one day before the kill
  window opens).
- **Domain verified:** imaginaryauthors.com — confirmed live in Wayback CDX back to
  2012 and with continuous HTML coverage through July 2024.
- **Known later outcome:** Whispered Myths and Telegrama confirmed permanently
  discontinued; final-bottle buying in Basenotes/Fragrantica comments.

The outcome above is roster-stated + screen-3-stated context, **not** an
independently sealed or verified outcome record for this case.

## Captured evidence (real Source Capture packets, body-verified, pre-cutoff)

| E | what it sources | declared cutoff | selected snapshot | body bytes | sha256 (body) | packet |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | imaginaryauthors.com homepage, cutoff-proximate | 2024-08-01 | 2024-07-17 | 228502 | `aa6992b1…ea5f52a` | `source_captures/e1_homepage_proximate/` |
| E2 | imaginaryauthors.com homepage, ~14-month-before trajectory point | 2023-06-01 | 2023-05-30 | 162646 | `eeb6e602…528d4c9` | `source_captures/e2_homepage_midwindow/` |
| E3 | imaginaryauthors.com/products/whispered-myths (killed SKU), pre-cutoff | 2024-08-01 | 2024-06-16 | 161809 | `8fc235cf…acd4d9` | `source_captures/e3_whispered_myths_product/` |
| E4 | imaginaryauthors.com/products/telegrama (killed SKU), pre-cutoff | 2024-08-01 | 2024-03-04 | 170274 | `87513690…68bd5ee` | `source_captures/e4_telegrama_product/` |
| E5 | imaginaryauthors.com/collections/all (full catalog), pre-cutoff | 2024-08-01 | 2024-03-24 | 279547 | `cc135d03…48c3657` | `source_captures/e5_collections_all/` |

E1 + E2 form a ~14-month pre-cutoff homepage trajectory (May 2023 → July 2024).
E3 and E4 are the gold units: the two named killed-SKU product pages captured
while both were still live pre-kill. E5 is the full catalog at a 2024-03-24
snapshot, which is the most recent available full-catalog pre-cutoff capture;
both killed SKUs were present on that date. Body sizes and hashes are recorded
as facts; **the change is recorded as a fact, not interpreted** — what the
pages actually say is not asserted here (the raw HTML body is preserved for a
later parser/judgment step; this capture does not parse or extract page meaning).

Note on E2: the runner followed a Wayback redirect from the declared-cutoff URL
to the nearest available snapshot (`20230530100738`); the body preserved is the
redirect-destination snapshot. This is normal Wayback behavior and the
`pre_cutoff` posture remains valid.

## Honest limitations

- **Product-info page: no Wayback coverage found.** The screen 3 ledger cited
  the brand's "official product-info page" as one of its discovery sources
  (listing 8 total kills). No URL under `/pages/product-info` or
  `/pages/discontinued` was found in the Wayback CDX for imaginaryauthors.com.
  This page is not captured; the 8-total-kills count is roster-stated, not
  observed from a captured artifact in this set.
- **About-us page: not captured.** The `/pages/about-us` page has pre-cutoff
  coverage but is not captured in this set; the brand identity (Portland, OR;
  indie) is roster-stated, not observed from a captured artifact.
- **E4 (Telegrama) snapshot is March 2024, not July 2024.** The latest
  pre-cutoff snapshot for `/products/telegrama` with a 200 HTML response in
  the CDX was 2024-03-04. No snapshot closer to the cutoff was available.
- **E5 (collections/all) snapshot is March 2024.** The latest pre-cutoff
  snapshot for the full catalog was 2024-03-24 (next entry after that is
  post-cutoff). The July 2024 catalog state is therefore not captured.
- **No fixture.** No participant packets, facilitator ledger, sealed outcome,
  paired-packet design, or evaluation exist for this case. Those are
  judgment-spine work, not built by this capture run.
- **Content not parsed.** Per INV-1, capture records observed facts + limits
  and introduces no weights, scores, ranks, or verdicts.

## Non-claims

Not validation, not readiness, not a backtest fixture, not a band input, not a
sealed outcome, not contestant-visible, not Cleaning/ECR/Judgment, not buyer
proof. Product-learning tier, capture-only, N=5 archive snapshots (2 homepage
trajectory, 2 killed-SKU product pages, 1 full-catalog).
