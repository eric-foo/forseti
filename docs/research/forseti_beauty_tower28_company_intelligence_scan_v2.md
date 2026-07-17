# Tower 28 Beauty — v2 Rerun Supplement Scan Receipt (Delta Declaration)

```yaml
retrieval_header_version: 1
artifact_role: Research artifact (v2 rerun supplement scan/run receipt with comparison delta declaration)
scope: >
  Records the B+ supplement acquisitions executed for the Tower 28 v2 rerun:
  which contract version the run used, the evidence base and enumerated
  supplements, the retailer surface set versus v1, the capture receipts landed
  in the canonical lake, the typed access outcomes, and the honest deltas the
  external comparison needs to separate contract-shape gains from
  evidence-breadth gains.
use_when:
  - Reading the v2 bundle for the owner's same-lens external comparison.
  - Auditing which v2 observations are reused-from-v1 versus freshly acquired.
authority_boundary: retrieval_only
open_next:
  - docs/research/forseti_beauty_tower28_company_intelligence_report_v2.md
  - docs/research/forseti_beauty_tower28_company_intelligence_csb_v2.md
  - docs/workflows/forseti_beauty_tower28_rerun_commission_handoff_v0.md
stale_if:
  - The external comparison is adjudicated (bundle consumed).
  - A recorded packet is unavailable or fails its preserved-file hash check.
```

## Run Receipt And Delta Declaration

For honest comparison attribution, this run declares its deltas against v1.

```yaml
run_receipt:
  commission_id: tower28_ci_v2_rerun_2026_07_18
  contract_version_run_under: >
    Upgraded CSB company_competitive_intelligence contract at
    forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
    (synthesis layer: Executive Intelligence Brief, per-hero choice-mechanism
    chain cards, five-way review classification with held_background default and
    graduation triggers, stated-sample proportionality, visible-concentration
    language, invalidation conditions, preservation trigger, and the
    review_classification_rows block).
  contract_version_v1_ran_under: >
    Pre-upgrade company_competitive_intelligence contract (citation-only Section
    5-8 summaries, no Executive Intelligence Brief, no chain cards, no
    review_classification_rows).
  mode: forward
  time_posture: recency_first
  as_of_date: "2026-07-18"
  evidence_cutoff_at: not_applicable
  evidence_base: B+ (reuse + targeted supplement)
  reused_from_v1:
    observation_rows: OBS-001 through OBS-029 (verbatim, original observation dates 2026-07-16/17)
    coverage_rows: COV-001 through COV-020 (earned v1 statuses)
    blindness_maintained: >
      This lane loaded the upgraded contract files and raw evidence only. It did
      NOT load v1's report synthesis (Sections 5-8 narrative, Section 9
      candidates, the Executive-brief-equivalent conclusions), the external
      assessments of v1, or the adjudication ledger. The v1 raw observation and
      coverage rows were read as evidence; the v1 report's synthesis sections
      were not.
  supplements_acquired_2026_07_17:
    - id: COV-021
      class: substantive_review_text_sampling
      why: upgraded contract's Section 7 six-field classification rows and per-hero chain cards require per-review text v1 never collected (closes v1 GAP-008)
      surface: Sephora hero and sub-4.0 PDPs (Swipe, SOS Daily Rescue spray, ShineOn, SunnyDays, MakeWaves)
      landed_observations: [OBS-030, OBS-031, OBS-032, OBS-033, OBS-034]
    - id: COV-022
      class: amazon_us_seller_state_and_diversion_read
      why: fulfills v1 REQ-003/CR-003 (v1 could read Amazon only from a Singapore vantage); resolves the Amazon channel-listing-vs-operation contradiction and the add-on diversion task
      surface: Amazon US search plus two hero PDPs with declared US delivery ZIP 10001
      landed_observations: [OBS-035, OBS-036, OBS-037]
    - id: COV-023
      class: certification_directory_verification
      why: certifier-side verification of the brand's three-organization seal claims (add-on task); checkable counter-evidence to a load-bearing versioned claim
      surface: NEA, NRS, NPF public seal/product directories
      landed_observations: [OBS-041, OBS-042, OBS-043]
    - id: COV-024
      class: preservation_captures_and_price_ladder
      why: preserve conclusion-bearing, disputable, likely-to-disappear pages (CR mechanism); price-ladder add-on raw material
      surface: tower28beauty.com stores, ingredients, collections/all pages
      landed_observations: [OBS-038, OBS-039, OBS-040]
  retailer_surface_set_vs_v1:
    v1: Sephora-deep (brand page, PDPs, aggregate ratings); Revolve selection-run + first-party listing; Amazon International (Singapore vantage only); Ulta bounded no-carriage-observed.
    v2_added: Sephora per-review text sampling on five heroes; Amazon US storefront with confirmed US delivery pin (seller-of-record + diversion read); NEA/NRS/NPF certifier directories; brand-page preservation captures.
    v2_not_re_run: Revolve, Ulta, Mecca, Credo, TikTok/Instagram live, AEO (reused or held as typed gaps).
  dates:
    supplement_capture_date: "2026-07-17"
    report_as_of: "2026-07-18"
  validator_status: PASS (report and sealed commission board both pass check_commission_signal_board_output.py)
  comparison_neutrality: >
    "Beat v1" was not a synthesis instruction. The lane ran the upgraded
    contract against the B+ evidence base; the report stays decision-neutral.
```

## Supplement Capture Receipts (landed in the canonical lake)

All packets under `F:\forseti-data-lake\raw\...`. All captures: public pages,
no login, no CAPTCHA/challenge solving, human-rate, one attempt per URL except
where a bounded re-attempt is noted with its changed-flag rationale.

### COV-021 — Sephora per-review text sampling

| Product | Packet ID | Rating / reviews (source) | Verified substantive first-page sample | Notes |
| --- | --- | --- | --- | --- |
| Swipe concealer (P507142) | `01KXRKVTDPWZ32FXTPQ9MW9DXQ` | 4.34 / 3,654 | 4 verified (all 5★) | "Non-Comedogenic" current on PDP; ld+json sample carried 1★ breakout + 3★ burning reviews absent from page 1 |
| SOS Daily Rescue spray (P448852) | `01KXRM2S8VCVDC8D3DA3CCDY0K` | 4.09 / 4,855 | 2 verified (5★) | three-org recognition claim + clinical results on PDP; 5 of 6 first-page reviews incentivized; AI summary keyword tags recorded |
| ShineOn Lip Jelly (P448854) | `01KXRM5179M7HHSMASXZZQZA87` | 4.46 / 5,608 | 3 verified (5★) | positive-weighted; one unverified 4★ separation note |
| SunnyDays SPF 30 (P477829) | `01KXRM76H72A2MD7FDRASCTY8T` | 3.98 / 1,941 | 5 verified (5/4/2/1/1★) | most negatively skewed; verified "greasy/separates" review counters stated "non-greasy formula" |
| MakeWaves mascara (P502484) | `01KXRM9C363NY7N9M633YCV89E` | 3.82 / 2,954 | 3 verified (5/5/3★) | sensitive-eyes claim + clinical results; unverified "burning" review + Irritation(23) AI tag |

Sort order: the Sephora reviews sort control rendered a generic "Sort" pill with
no textually-confirmed selected option; the observed default first page was
recency-consistent (non-decreasing review age) across all five products. Star
values were derived from DOM star-width markup and cross-checked against the
embedded ld+json review array where authors overlapped (all matched). No typed
access failures.

### COV-022 — Amazon US seller state and diversion read

| Capture | Packet ID | US pin | Outcome |
| --- | --- | --- | --- |
| Search "Tower 28 Beauty" (ZIP 10001) | `01KXRKN8DZYY66P44N32R2GQ6A` | confirmed | 115 results; Seller facet lists "Tower28 Beauty" and "RG Click Picks"; $12–$92; Small Business badges |
| Search (profile-less retry) | `01KXRKNT543FVHGJNRMB8X76RK` | n/a | typed access failure: Amazon `cs_503` anti-bot soft-block; not retried (search already secured) |
| SOS spray PDP B0B3S7HJ9L (ZIP 10001) | `01KXRKTXCYFRW23GVWP5JSKJDH` | confirmed | Ships from Amazon / Sold by Tower28 Beauty; Visit the Tower 28 Store; $28.00; 4.6/5,131 |
| SunnyDays PDP B0BBFWFN42, attempt 1 | `01KXRKWZJXDRM7JYESMASJESWG` | failed | Singapore/SGD geo-redirect (same class that blocked v1); typed gap |
| SunnyDays PDP B0BBFWFN42, re-attempt (`--delivery-zip-setup-timeout-seconds 75`) | `01KXRKYNNEBFN7Q375AKR4N2K9` | confirmed | Ships from Amazon / Sold by Tower28 Beauty; $32.00; 4.4/360 |

Typed tooling caveat (not an access result): the `amazon_pdp_distribution`
capture profile's hardcoded sufficiency literals reference an unrelated LANEIGE
reference product, so every profiled capture exited non-zero on
`source_detail_sufficiency_failed` while still writing full real packets;
content was read directly from the preserved raw files. The US delivery pin is
intermittent (confirmed 3 of 4). No projection JSON was emitted for the PDP
captures (runner exits before projection on the sufficiency-gate exception).

### COV-023 — Certification directory verification

| Certifier | Packet ID(s) | Tower 28 result |
| --- | --- | --- |
| NEA (Seal of Acceptance) | base `01KXRMFR7P8QSKPQM66XTVXW46`; filtered REST `01KXRMGB4WEVBF19G464PSHZNJ` | 9 distinct SOS/SunnyDays/SuperDew titles (base page-1 was a zero-yield; public WP REST endpoint surfaced them; one sampled record binds to tower28beauty.com, accepted 2026-05-11) |
| NRS (Seal of Acceptance) | `01KXRM4HZJVVRVFAGFFX6VY5DD` | 7 products "by Tower 28" via Drupal Views fulltext filter; reproduced independently by re-loading the filter URL |
| NPF (Seal of Recognition) | base `01KXRMHRKJEZ9TJYXBYFB78514` (redirect to /seal-of-recognition-program/); data feed `01KXRMJBBSE3BP9RF0PAEQ3B7H` | 7 distinct products product_company "Tower 28 Beauty" in the Gatsby page-data feed (client-side filter only; base landing was a zero-yield) |

All three directories are public, unauthenticated GET endpoints reached by
ordinary navigation. Directory listing verifies seal acceptance/recognition,
not efficacy or comedogenicity.

### COV-024 — Brand-page preservation + price ladder

| Page | Packet ID | Preserved evidence |
| --- | --- | --- |
| /pages/stores | `01KXRKNR8FF5NAZJQYY32RFZWG` | anti-diversion notice + authorized-retailer list (Amazon, Ulta absent), verbatim |
| /pages/ingredients | `01KXRKPW08AEP94X5G29YTR3EH` | claims architecture; "first and only" absent; "non-comedogenic" absent from body; NRS/NPF not named; "vegan" only in meta tags |
| /collections/all | `01KXRKRYMB537X7NJ3N7YE4CRY` | full 33-SKU catalog price ladder $12–$128 with promo labels and sold-out states |

## Non-Claims

These observations do not establish demand, velocity, revenue, sell-through,
market share, repeat purchase, retailer productivity, claim substantiation
beyond a certifier's own acceptance judgment, or monitoring readiness. They are
bounded public page-state and directory evidence only. Validator PASS means the
report and board are mechanically complete under the company contract; it is not
evidence truth, demand classification, buyer proof, readiness, or client-facing
approval.
