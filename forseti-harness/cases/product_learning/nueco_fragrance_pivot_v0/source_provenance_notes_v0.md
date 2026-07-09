---
retrieval_header_version: 1
artifact_role: Capture-side source-provenance record (capture-spine deliverable; NOT a fixture, band input, or contestant-visible packet)
scope: >
  Per-evidence-unit provenance for the pre-cutoff Wayback capture set of case
  nueco_fragrance_pivot_v0. Records what is archive-captured (a homepage
  trajectory plus supplement-catalog and about pages), the selected snapshots
  and body hashes, and the honest limits including the soft pivot-date
  uncertainty. This is a capture-spine starter set, not a backtest fixture:
  no participant packets, no facilitator ledger, no sealed outcome, no
  evaluation exist for this case yet.
use_when:
  - Auditing what The Nue Co. fragrance-pivot case is archive-sourced from so far.
  - Deciding what a later judgment-spine fixture for this case would still need.
authority_boundary: retrieval_only
open_next:
  - docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md   # roster row this case came from (candidate #13)
  - docs/decisions/judgment_spine_backtest_batch2_candidate_routing_v0.md   # batch-2 routing record for this candidate (priority 2 / BORDER)
  - docs/product/core_spine/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md   # the backtest specimen shape a later fixture would mirror
---

# Source Provenance Notes — nueco_fragrance_pivot_v0 (v0)

Capture-side record. This is the **capture-spine deliverable** for The Nue
Co. fragrance-pivot backtest case: a bounded set of pre-cutoff Wayback
captures produced by the `archive_org` adapter
(`run_source_capture_archive_packet.py`, `select_snapshot <= cutoff`). Every
unit below is `cutoff_posture: pre_cutoff`, body-verified (served body
successfully fetched from Wayback), `limitations: []`. It is **not** a
backtest fixture and asserts no judgment.

## Case context (roster-stated; not independently verified here)

From the consumer-demand candidate pool (candidate #13):

- **Decision being backtested:** The Nue Co.'s pivot OUT of supplements toward
  fragrance-first (fragrance grew from ~20% to ~65% of revenue; CAC halved;
  Ulta exclusive entered).
- **BORDER status:** US/UK hybrid brand (NY + London); treated as US-market per
  owner direction.
- **Cutoff:** 2020-01-01 — see rationale and uncertainty note below.
- **Known later outcome (roster-stated):** fragrance became the majority of
  revenue; CAC halved post-pivot; Ulta exclusive secured.

The outcome above is roster-stated context, **not** an independently sealed or
verified outcome record for this case.

## Cutoff rationale and uncertainty

**Declared cutoff: 2020-01-01.** Rationale:

- The ingestible-beauty screen ledger dates the pivot window as "2019–2024"
  (fragrance ~20% → ~65% of revenue over that span). There is no single datable
  public event marking when fragrance crossed the majority threshold.
- The functional-fragrance product first appeared in Wayback CDX records as
  early as March 2019 (`/collections/all/products/functional-fragrance`), but
  the overall product catalog through at least end-2019 remains overwhelmingly
  supplements-led (gut-health, debloat, skin, sleep, stress, immunity, focus,
  protein categories all visible pre-2020).
- A 2020-01-01 cutoff is a **defensible supplements-led-era anchor**: the CDX
  record shows the site was supplements-forward through the captured snapshots
  (Nov–Dec 2019 homepage, Nov 2019 collections catalog, Dec 2019 supplement
  product page, Feb 2019 about page), and the fragrance revenue majority is
  a later-period outcome by the roster's own framing.
- **Uncertainty is real**: the exact date when supplements fell below 50% of
  revenue is not publicly documented and was not independently verified by this
  capture run. A future judgment-spine fixture should carry this uncertainty
  explicitly and source additional evidence to pin the pre-state more precisely
  if decision-critical.

## Captured evidence (real Source Capture packets, body-verified, pre-cutoff)

### Homepage trajectory (~10 months approaching the cutoff)

| E | what it sources | declared cutoff | selected snapshot | body bytes | sha256 (body) | packet |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | www.thenueco.com homepage, cutoff-proximate | 2020-01-01 | 2019-12-21 | 153406 | `7a6204b5…129174ec` | `source_captures/e1_homepage/` |
| E2 | www.thenueco.com homepage, mid-window | 2019-07-01 | 2019-06-26 | 109559 | `872af5a2…1a3d67da` | `source_captures/e2_homepage_mid/` |
| E3 | www.thenueco.com homepage, early window | 2019-03-01 | 2019-02-27 | 107693 | `03970d2f…5e7803c9` | `source_captures/e3_homepage_early/` |

### Supplement-catalog and brand pages (supplements-led positioning)

| E | what it sources | declared cutoff | selected snapshot | body bytes | sha256 (body) | packet |
| --- | --- | --- | --- | --- | --- | --- |
| E4 | `/collections/all` — full product catalog | 2020-01-01 | 2019-11-17 | 213104 | `20c3e364…88f8240d` | `source_captures/e4_collections_all/` |
| E5 | `/collections/best-sellers` — best-seller catalog | 2020-01-01 | 2019-11-17 | 237739 | `abc8d248…8de064eb` | `source_captures/e5_best_sellers/` |
| E6 | `/pages/about` — brand about/story page | 2019-02-20 | 2019-02-19 | 108587 | `d2bdc313…d0a7dbec` | `source_captures/e6_about/` |
| E7 | `/collections/all/products/debloat-food-prebiotic-1` — core supplement product | 2020-01-01 | 2019-12-19 | 155577 | `3c6dcc77…c01a4ffd` | `source_captures/e7_debloat_product/` |

7 body-verified units. Page content is **recorded, not interpreted** — the raw
HTML body is preserved for a later parser/judgment step; what the actual
product mix, pricing, and positioning were at each snapshot is not asserted
here (INV-1: capture preserves bytes + provenance only).

### E1 warning note

E1 carries a Wayback redirect warning in the manifest (`warnings` field):
`direct_http followed redirect from https://web.archive.org/web/20191221003425/http://thenueco.com:80/ to https://web.archive.org/web/20191214045845/https://www.thenueco.com/`. This is a Wayback-internal redirect from the bare http:// variant to the canonical https://www.thenueco.com/ snapshot and is expected behavior; the body was fetched with HTTP 200 OK (153406 bytes). The redirect is noted as a fact, not a failure.

### E6 about-page cutoff note

The `/pages/about` URL was only available in Wayback with 200 status at
2019-01-22 and 2019-02-19; the next capture (2019-06-05) returned 404
(confirmed by CDX probe). E6 was therefore captured against a 2019-02-20
cutoff rather than the primary 2020-01-01 cutoff. This is earlier in the
pre-pivot window, and remains pre-cutoff for the declared case cutoff of
2020-01-01. The narrower capture window for E6 is noted.

## Honest coverage limits

- **Cutoff uncertainty (PRIMARY).** The pivot window is 2019–2024 with no
  single dated inflection; the cutoff of 2020-01-01 is a defensible supplements-led-era
  anchor, not a confirmed pre-majority-fragrance date. The supplements-majority
  to fragrance-majority crossover date is unverified.
- **BORDER brand.** The Nue Co. is a US/UK hybrid; UK product mix and pricing
  may differ from the US-market captures above. Treated as US-market per owner
  direction; UK-market specifics are not captured.
- **No sub-page sweep.** Journal/blog posts, press/news coverage, product
  ingredient pages, and the `/pages/faqs` page were not captured. The CDX
  record showed them available but they were outside the bounded 6–12 URL scope.
- **No fixture.** No participant packets, facilitator ledger, sealed outcome,
  paired-packet design, or evaluation exist for this case. Those are
  judgment-spine work, not built by this capture run.
- **Content not parsed.** Per INV-1, capture records observed facts + limits
  and introduces no weights, scores, ranks, or verdicts.
- **thenue.co domain not captured.** The alternate short domain was not found
  in the CDX record (primary domain `www.thenueco.com` had full coverage from
  2017 onward; the alternate domain probe was not executed separately but no
  CDX results surfaced for it in the incidental scan).

## Non-claims

Not validation, not readiness, not a backtest fixture, not a band input, not a
sealed outcome, not contestant-visible, not Cleaning/ECR/Judgment, not buyer
proof. Product-learning tier, capture-only, N=7 pre-cutoff snapshots.
BORDER-status noted (US/UK); cutoff-date uncertainty named above.
