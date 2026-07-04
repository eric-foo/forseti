# Creator Signal — Market Sizing (Rough Internal Estimate, v0)

```yaml
retrieval_header_version: 1
artifact_role: market_sizing_estimate_internal
scope: >
  Rough TAM/SAM/SOM for the Creator Signal carve-out (vertical creator-intelligence,
  fragrance -> beauty). Supporting evidence for the product-architecture proposal
  (creator_signal_product_architecture_v0.md). This is a SIZING exercise to frame
  go/no-go — NOT demand validation, NOT buyer proof, NOT a revenue forecast.
use_when:
  - Framing whether the opportunity is venture-scale / small-business / too-small.
  - Reasoning about the fragrance wedge vs the beauty destination.
  - Identifying the competitor to design against (CreatorIQ / Tribe Dynamics).
open_next:
  - forseti/product/spines/creator_signal/creator_signal_product_architecture_v0.md
stale_if:
  - Cited market figures (2024-25) age past ~2 years.
  - A demand/WTP probe returns real evidence (replace estimates with observations).
authority_boundary: retrieval_only
```

## Status & honesty boundary

Internal research pass, 2026-07-01. Numbers are **order-of-magnitude estimates
triangulated from published market reports + competitor pricing**, with explicit
assumptions and confidence flags. **This sizes the *prize*; it does not validate
that anyone will pay** — the willingness-to-pay premium is the hinge and is
UNVALIDATED (see §Hinge). Buyer counts carry ±50%. Not a forecast, not readiness,
not buyer proof.

## One-line verdict

Fragrance *alone* is a **small-business / niche-SaaS** market (~$0.3–1.5M ARR SOM) —
**not venture-scale.** The **beauty (incl. skincare) expansion** is what makes it a
**credible Series-A-scale vertical SaaS** (~$5M ARR base at Year 3, range $2–12M):
venture-*plausible*, not venture-*obvious*. **Fragrance = the wedge; beauty = the
destination.** Plan around the beauty market, not fragrance.

## TAM / SAM / SOM

| Layer | Estimate | Notes |
|---|---|---|
| **TAM** — influencer-marketing *tooling + services* market | **~$15B** (range $10–20B); software-only ~$9–10B; ~20% CAGR | Corroborated across 5+ firms (Straits $9.4B, SkyQuest $10.6B, MarkNtel $15B, Data Bridge $17.1B, Fortune $20.2B). MEDIUM confidence. Layer above it — total influencer *industry* incl. creator payouts — is ~$32.55B (IAB puts US creator ad spend ~$37B 2025, +26% YoY); too broad to be addressable. |
| **SAM** — beauty+fragrance vertical tooling+services | headline **~$2B**, but **reachable ICP slice ~$100M** | The $2B top-down **includes enterprise beauty** (L'Oréal etc. on CreatorIQ at $30–60k/yr) that is NOT our ICP. Bottom-up (indie/DTC brands + specialist agencies × ARPU) = **~$100M** — the real near-term serviceable market. **Do not anchor on $2B.** Fragrance-only category ≈ $100–160M. LOW–MEDIUM confidence. |
| **SOM** — 3-yr obtainable | fragrance-only **~$0.3–1.5M** ARR; **+ beauty ~$2–12M (base ~$5M)** | Base math: ~11,200 addressable brands × ~6% × ~$5k + ~250 agencies × ~15% × ~$18k ≈ $5M by Yr3. LOW confidence — penetration + ARPU are assumptions, not observations. |

## Competitor benchmark (2025)

| Player | Sells | Rough pricing | Fragrance/beauty vertical depth? |
|---|---|---|---|
| CreatorIQ (+ Tribe Dynamics) | Enterprise creator-mktg OS; Tribe = beauty/fashion **earned-media** analytics | **~$30–60k/yr**, enterprise, sales-led | **Closest.** Tribe's metric is **EMV (Earned Media Value)**. Real beauty/fashion depth, but coverage is a *curated creator panel* refreshed ~semiannually (not niche-complete); freshness/provenance is marketing-grade, not auditor-grade |
| Traackr | Beauty-heavy influencer-performance platform; Brand Vitality Score (VIT) | enterprise | **Closest *after* CreatorIQ for beauty** — watch on the beauty/skincare expansion |
| Launchmetrics | **MIV (Media Impact Value)** — fashion/lifestyle/**beauty** media measurement | enterprise | The metric earlier mis-attributed to Tribe; it is *Launchmetrics'*. Luxury/PR/press-heavy |
| Sprout Social / Tagger | Social-mgmt suite + influencer (Tagger, acq. ~$140M 2023) | mid-market/enterprise | No — horizontal |
| Meltwater / Klear | Media-intelligence suite + influencer | enterprise | No — PR/comms-oriented |
| HypeAuditor | Discovery + audience/fraud analytics (200M+) | $399–$1,799/mo | No — beauty is a filter |
| Modash | Discovery (350M+) + tracking | $199–$499/mo, $14.7k/yr ent. | No |
| Upfluence | Discovery + outreach + e-comm | ~$478–$2,000/mo | No |
| GRIN | DTC creator-mgmt (CRM-style) | ~$999–$2,500/mo | No — DTC-general |
| Aspire | Campaign workflow + marketplace | ~$2,000–$2,300/mo | No |

**Key structural finding: no incumbent owns fragrance/beauty as a vertical *data
product*.** The closest — and the one to design against — is **CreatorIQ / Tribe
Dynamics** (Tribe's metric is **EMV — Earned Media Value**; **MIV — Media Impact
Value — is *Launchmetrics'* separate metric**, do not conflate them). Everyone else
treats beauty as a search filter, not a domain. This both **validates the category
is buyable** and **narrows the "white space."**

**Competitive posture (from the cross-vendor teardown, 2026-07-01):**
- **They are strong, not fragile** — enterprise workflow + governance + a familiar
  EMV benchmark. Do **not** attack head-on (workflow, payments, big-brand
  reporting, Fortune-500 procurement deals).
- **Their structural gaps are our openings:** coverage is a *curated, ~semiannually-
  refreshed panel* — not niche-complete (misses fragrance micro-reviewers, decant/
  collector communities that matter early); EMV is a proprietary engagement proxy
  (assigns full value to *each* brand in a multi-brand post; Stories are
  model-predicted; it is not revenue/incrementality); freshness/provenance is
  *marketing-grade, not auditor-grade* (a new creator gets only a limited historical
  scan).
- **The moat is not "better software" — it is a proprietary, longitudinal, vertical
  *evidence graph*** (creator × brand × product × content × time × proof). They can
  copy screens faster than *capture history* — which only accrues if we start
  capturing the niche **now**.
- **The play is win-the-flank → coexist → possibly be-acquired, NOT displace.** Serve
  indie/DTC brands, specialist agencies, and **non-marketer evidence buyers**
  (investors / retail / procurement / legal). Tribe already has a financial-institutions
  page, so that demand is real — but their packaging is high-level EMV, not
  diligence-grade evidence, which is the opening. CreatorIQ acquired Tribe for exactly
  this category authority, so an acquisition path is credible.

## The hinge (biggest uncertainty)

Every dollar above assumes buyers pay a **premium** for "every meaningful creator
in the niche, fresh + provenance-backed" over a horizontal tool's beauty *filter*.
Whether that premium is **durable** (vs. replicable-as-a-filter by CreatorIQ/Tribe,
HypeAuditor, Modash) is a **demand question sizing cannot answer** — it is the
single hinge the entire case turns on, and it is unvalidated.

## Plausible ARPU (benchmarked, unvalidated for our product)

Brands **$3–12k/yr** (base $5k; above Modash entry, at/below GRIN/Aspire).
Agencies **$10–40k/yr** (base $18k; multi-seat, multi-client).

## Assumptions ledger

1. Beauty ≈ 15% of influencer-tooling TAM (from ~21.6% fashion+beauty). *Softest SAM link.*
2. Fragrance ≈ 5–8% of beauty by revenue (niche fragrance $5–8.6B vs ~$677B beauty). *Well-grounded.*
3. ARPU brands $5k / agencies $18k base. *Benchmarked to competitors; unvalidated for us.*
4. 3-yr penetration 5–8% of ICP pool. *Assumption.*
5. Buyer counts (~10k beauty / ~1.2k fragrance brands / ~250 specialist agencies). *±50%; no clean census exists.*

## Data-quality flags

No figures stale (all 2024–25). Platform-market sizes vary ~2x — treated as a range,
not a point. Private-company revenue/installed-base not publicly reported (pricing
confirmed, base estimated). Grand View's $34.2B (2025) figure is a broad-scope
outlier, not load-bearing.

## Provenance

Internal research pass (web-triangulated), 2026-07-01. Sources: Influencer
Marketing Hub Benchmark 2025, IAB 2025 Creator Economy report, MarkNtel / Fortune
Business Insights / Data Bridge / Grand View platform-market reports, competitor
pricing pages (Modash, HypeAuditor, GRIN), niche-fragrance + beauty market reports.
Rough estimate for go/no-go framing only.
