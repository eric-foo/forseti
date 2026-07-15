# Forseti Beauty US Neutral Company Longlist Scan v0

```yaml
retrieval_header_version: 1
artifact_role: CSB-first Scanning receipt
scope: Bounded public-source discovery of neutral US consumer-beauty Brand pointers for GTM eligibility.
use_when:
  - Auditing how the 60-row machine-readable longlist was sourced.
authority_boundary: research_receipt_only
```

```yaml
commission_id: CSB-BEAUTY-US-NEUTRAL-POOL-V0
scan_date: 2026-07-16
mode: forward
subject: neutral US consumer-beauty Brand discovery set
source_context_status: SOURCE_CONTEXT_READY
run_caps:
  max_screening_moves_total: 24
  max_exact_queries_total: 12
screening_moves_used: 18
exact_queries_used: 8
closeout_state: no_candidate_after_discovery
screening_move_ids: [M01, M02, M03, M04, M05, M06, M07, M08, M09, M10, M11, M12, M13, M14, M15, M16, M17, M18]
```

## Broad Scout And Source-Cap Accounting

The broad scout opened all four commissioned source frames before exact-query work. It produced 60 distinct Brand pointers. Frame totals count the primary discovery assignment of each deduplicated Brand; cross-frame corroboration does not create another pointer.

The scout frontier covered all four commissioned frames. Venue evaluation happened before exact queries. Hidden venue pointers were limited to official identity, stockist, store-locator, and portfolio routes. Negative and access note work checked duplicates, unavailable surfaces, and regional ambiguity. Recency/current-state checks used the run-date observation boundary. The recommended main deepening is not another broad scan: it is the later one-company decision-pressure pass after the Company Surface-compatible proving slice clears.

| frame | primary distinct pointers | cap | live seed | outcome |
|---|---:|---:|---|---|
| broad US beauty retail | 24 | 30 | Sephora and Ulta | cap respected |
| emerging-brand programmes | 15 | 30 | Sephora Accelerate and official Ulta programme surfaces | cap respected |
| established portfolios | 11 | 30 | official parent and Brand directories | cap respected |
| fragrance retail | 10 | 30 | Luckyscent, Ministry of Scent, Sephora, and Ulta | cap respected |
| **combined deduplicated** | **60** | **120** | normalized consumer Brand identity | cap respected |

csb_rows_consumed: [SBR-001, SBR-002, SBR-003, SBR-004, SBR-005, SBR-006]

CSB row accounting: SBR-001 through SBR-004 were used for discovery; SBR-005 and SBR-006 were used for mandatory counterevidence and limitation checks. No commissioned row was dropped.

| move_id | move | CSB rows | result |
|---|---|---|---|
| M01-M04 | open and screen the four seed-frame families | SBR-001-SBR-004 | all frames accessible; Brands nominated |
| M05-M08 | follow official Brand identity and US shopping routes | SBR-001-SBR-004 | first-party pointers retained |
| M09-M12 | inspect retailer, specialist, and programme corroboration | SBR-001, SBR-002, SBR-004 | independent source-family pointers retained |
| M13-M15 | inspect official parent/portfolio routes | SBR-003, SBR-005 | parent pointers resolved or limited visibly |
| M16-M18 | duplicate, access, and low-trigger coverage pass | SBR-005, SBR-006 | no duplicate row promoted; comparator candidates preserved without inference |

## Exact Query Discovery Ledger

| query_id | bounded purpose | outcome |
|---|---|---|
| EQ-001 | exact Brand + official US site | first-party identity routes checked |
| EQ-002 | exact Brand + Sephora | specialty-retail pointers checked |
| EQ-003 | exact Brand + Ulta | specialty-retail pointers checked |
| EQ-004 | exact Brand + US retailer/store locator | US/channel gaps checked |
| EQ-005 | exact Brand + official parent | ownership pointers checked without forcing resolution |
| EQ-006 | exact fragrance Brand + Luckyscent | specialist-fragrance availability checked |
| EQ-007 | exact fragrance Brand + Ministry of Scent | specialist-fragrance availability checked |
| EQ-008 | exact Brand + current official activity | dated-observation and access gaps checked |

Four allowed exact-query slots remained unused because all quota cells were fillable.

## Venue Evaluation

| venue | value for this commission | limitation |
|---|---|---|
| Sephora brand discovery and search | broad US specialty availability and emerging-program routes | merchandising is not performance evidence |
| Ulta A-Z and search | broad specialty availability across price and category | presence alone does not establish tier |
| Sephora Accelerate and official Ulta programmes | emerging Brand identity candidates | cohorts may be historical |
| official Brand and parent directories | identity, owned-channel, and parent pointers | ownership does not establish operating shape |
| Luckyscent and Ministry of Scent | independent and specialist fragrance alternatives | specialist presence is not national distribution |

## Hidden Venue Pointers

Hidden-venue following was limited to official About, stockist/store-locator, Terms, parent portfolio, and retailer Brand-result pages linked or discoverable from the seeded surfaces. No social account, contact database, paywalled source, private community, or generic research agent was used.

## Screen-Light Observations

```yaml
observation_id: OBS-BEAUTY-001
source_move_id: M01-M04
url: https://www.sephora.com/beauty/find-products
retrieval_date: 2026-07-16
short_quote_or_summary: Current Sephora discovery surface supplied cross-category US Brand pointers.
signal_stage: venue_value
claim_it_might_support: neutral Brand discovery and US specialty-retail pointer
gate_role: none
independence_hypothesis: retailer-owned surface independent from Brand first-party sites
uncertainty_or_limits: Merchandising and availability can change; presence is not a company-performance signal.
```

```yaml
observation_id: OBS-BEAUTY-002
source_move_id: M01-M04
url: https://www.ulta.com/brand/all
retrieval_date: 2026-07-16
short_quote_or_summary: Current Ulta A-Z surface supplied broad US Brand and category pointers.
signal_stage: venue_value
claim_it_might_support: neutral Brand discovery and US specialty-retail pointer
gate_role: none
independence_hypothesis: retailer-owned surface independent from Brand first-party sites
uncertainty_or_limits: A-Z inclusion is not distribution breadth or business-need evidence.
```

```yaml
observation_id: OBS-BEAUTY-003
source_move_id: M09-M12
url: https://accelerate.sephora.com/alumni/
retrieval_date: 2026-07-16
short_quote_or_summary: Official programme alumni surface supplied emerging Brand identity pointers.
signal_stage: precursor
claim_it_might_support: bounded emerging-candidate discovery
gate_role: none
independence_hypothesis: programme surface is independently operated from participating Brand sites
uncertainty_or_limits: Alumni status can be historical and does not prove current distribution.
```

```yaml
observation_id: OBS-BEAUTY-004
source_move_id: M01-M04
url: https://www.luckyscent.com/brands
retrieval_date: 2026-07-16
short_quote_or_summary: Specialist US fragrance directory supplied independent fragrance alternatives.
signal_stage: venue_value
claim_it_might_support: fragrance Brand discovery and specialist-US availability pointer
gate_role: none
independence_hypothesis: specialist retailer surface independent from Brand first-party sites
uncertainty_or_limits: Specialist availability is not national distribution.
```

```yaml
observation_id: OBS-BEAUTY-005
source_move_id: M01-M04
url: https://ministryofscent.com/collections/all-brands-1
retrieval_date: 2026-07-16
short_quote_or_summary: Specialist US fragrance collection supplied a second fragrance discovery venue.
signal_stage: venue_value
claim_it_might_support: fragrance alternatives and cross-venue corroboration
gate_role: none
independence_hypothesis: retailer-owned surface independent from Brand and Luckyscent sites
uncertainty_or_limits: Collection membership can change and is not evidence of company pressure.
```

```yaml
observation_id: OBS-BEAUTY-006
source_move_id: M16-M18
url: https://github.com/eric-foo/forseti
retrieval_date: 2026-07-16
short_quote_or_summary: Deduplicated pointer sidecar preserves 60 Brand identities, sources, limitations, eligibility fields, and administrative selection metadata.
signal_stage: candidate_support
claim_it_might_support: GTM eligibility-pool construction only
gate_role: none
independence_hypothesis: not an independent evidence source; this is the receiving research companion
uncertainty_or_limits: Pool membership and classifications are GTM metadata, not company evidence.
```

## Negatives And Access Notes

- No commissioned source required bypassing login, paywall, robots restriction, or access control.
- Retail search routes may render dynamically or vary by region; the first-party pointer remains the identity anchor.
- Parent resolution was not forced when the bounded scan did not establish it.
- Current availability observed on 2026-07-16 does not establish the effective date of an underlying launch or distribution event.
- No company-pressure candidate was minted. That is an intentional boundary result, not a failed discovery run.

## Capture Triage

```yaml
capture_requests: []
triage_result: no_capture_request
reason: >
  This commission ends at neutral public pointers and GTM eligibility metadata.
  Substantive company evidence capture waits for the minimal Company Surface-compatible proving slice and a one-company decision-pressure commission.
```

## Candidate Decision

Decision: `NO_COMPANY_PRESSURE_CANDIDATE_MINTED`.

All 60 neutral Brand pointers route to the GTM eligibility companion. Scanning does not choose the final 20 and does not interpret any pointer as company pain, demand, buyer relevance, priority, outreach suitability, or wedge evidence.

## Closeout

```yaml
closeout_state: no_candidate_after_discovery
discovery_result: 60_deduplicated_brand_pointers_routed_to_gtm
source_caps_respected: true
missing_quota_cells: []
next_artifact: docs/research/forseti_beauty_us_company_selection_v0.json
reopen_rule: Reopen only for a named failed eligibility, stratum, fragrance-replacement, identity, access, duplication, or source-coverage cell.
```
