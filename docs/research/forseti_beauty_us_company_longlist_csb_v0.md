# Forseti Beauty US Neutral Company Discovery CSB v0

```yaml
retrieval_header_version: 1
artifact_role: commission signal board
scope: Source-family commission for constructing a neutral US consumer-beauty Brand discovery set.
use_when:
  - Running the bounded Scanning discovery that feeds the 60-Brand eligibility longlist.
authority_boundary: research_commission_only
```

### 1. Commission Intake Receipt

```yaml
commission_id: CSB-BEAUTY-US-NEUTRAL-POOL-V0
commission_date: 2026-07-16
commissioner: forseti_product_lead_gtm
subject: US consumer-beauty Brand discovery
decision_context: construct a neutral US beauty Brand discovery set
mode: forward
cutoff_date: 2026-07-16
source_context_status: SOURCE_CONTEXT_READY
governing_contract: forseti/product/spines/product_lead/gtm/forseti_beauty_us_problem_discovery_to_wedge_contract_v0.md
```

### 2. Boundary Statement

The board commissions neutral discovery pointers. It does not commission company diagnosis or final selection. Scanning may report the observed Brand name, URL, source frame, apparent category, US-market pointer, parent pointer, channel pointer, dated-activity pointer, limitations, and coverage notes.

Prohibited outputs are pain, buyer, ICP, priority, outreach, and wedge fields or rankings. No result may infer business pressure from retailer presence, accelerator participation, ownership, recency, or absence from a surface.

Caps: no more than 30 distinct Brand pointers per source frame and no more than 120 distinct Brands overall.

### 3. Source-Family Coverage Plan

| source family | live seed | role | frame cap | coverage note |
|---|---|---|---:|---|
| broad US beauty retail | [Sephora brand discovery](https://www.sephora.com/beauty/find-products) and [Ulta A-Z](https://www.ulta.com/brand/all) | category-spanning national availability pointers | 30 | Retail inclusion is a pointer, not a performance signal. |
| emerging-brand programmes | [Sephora Accelerate](https://accelerate.sephora.com/) and current official Ulta incubator surfaces | identity and emerging-cohort pointers | 30 | Cohort membership does not establish current distribution or company need. |
| established portfolios | official parent-company Brand directories found and verified during the scan | parent and portfolio pointers | 30 | Parent scale does not establish Brand tier. |
| fragrance retail | [Luckyscent Brands](https://www.luckyscent.com/brands), [Ministry of Scent Brands](https://ministryofscent.com/collections/all-brands-1), Sephora, and Ulta | broad and specialist fragrance alternatives | 30 | Specialist availability is not national distribution. |

### 4. Signal Board Rows

| row_id | source_family | signal_role | row_purpose | recency_status | recency_attention | graph_role | graph_weight_hint | evidence_status | surface_cutoff_status | cutoff_status |
|---|---|---|---|---|---|---|---|---|---|---|
| SBR-001 | retail_pdp | retail_corroboration | source_route | current_state | normal | seed | medium | source_backed | existed_by_cutoff | in_window |
| SBR-002 | other | none | source_route | current_state | normal | seed | medium | source_backed | existed_by_cutoff | in_window |
| SBR-003 | owned_channels | owned_claim | source_route | current_state | normal | node_candidate | high | source_backed | existed_by_cutoff | in_window |
| SBR-004 | retail_pdp | retail_corroboration | source_route | current_state | normal | seed | medium | source_backed | existed_by_cutoff | in_window |
| SBR-005 | search_discovery | none | contradiction | current_state | high | counterevidence_path | high | source_backed | existed_by_cutoff | in_window |
| SBR-006 | other | none | gap | current_state | high | counterevidence_path | medium | source_backed | existed_by_cutoff | in_window |

### 5. Mandatory Counterevidence Paths

- Search official About, Terms, privacy, and parent portfolio surfaces for alias or ownership conflicts.
- Check retailer and specialist directories for duplicate Brand names, regional-only availability, discontinued pages, and access failures.
- Record an unresolved parent as unresolved; do not reject an otherwise bounded Brand solely to force ownership resolution.
- Preserve Brands with ordinary current availability as possible low-observed-trigger comparators. Absence of a visible trigger is an observation limit, not evidence that no trigger exists.

### 6. Campaign And Duplication Risk

Retailer merchandising campaigns can make many Brands appear newly active at once. Accelerator cohort pages can be historical. Parent directories can collapse Brand and legal-entity identities. Fragrance retailers can list distributors or regional storefronts. Deduplicate on normalized consumer Brand identity, retain frame provenance, and never count repeated retailer listings as independent company evidence.

### 7. Graph Retrieval Brief

Retrieve the four source frames with a bounded broad scout, then use exact queries only to fill identity, US presence, dated observation, stratum, or fragrance-replacement gaps. Follow hidden-venue links only when they can supply one of those missing facts. Keep one first-party pointer and at least one independently owned source family for every row that reaches GTM eligibility.

Target graph:

`source frame -> Brand pointer -> first-party identity -> US/channel/activity pointer -> GTM eligibility row`

No edge in this graph represents pain, demand, priority, or selection.

### 8. Demand-Classifier Handoff Packet

```yaml
classifier_handoff_packet:
  candidate_or_subject: neutral US consumer-beauty Brand discovery set
  decision_context: construct a neutral US beauty Brand discovery set
  mode: forward
  cutoff_date: 2026-07-16
  signal_rows_for_handoff: [SBR-001, SBR-002, SBR-003, SBR-004]
  counterevidence_rows_for_handoff: [SBR-005, SBR-006]
  source_family_gaps: []
  provenance_gaps:
    - Parent ownership may remain unresolved when Brand identity and eligibility otherwise clear.
  cutoff_uncertainties:
    - Observation time establishes current visibility, not the effective date of the underlying event.
  classifier_mapping_status: classifier_owned
  prohibited_claims:
    - company pain or business pressure
    - buyer, ICP, priority, outreach, or wedge recommendation
    - retailer presence as traction or need
    - accelerator participation as present operating shape
```

### 9. Visible Limitations

- This is a screen-light public-source commission, not a company dossier.
- Retail availability and site access can change after the cutoff.
- The board does not prove legal entity, revenue, headcount, or decision-maker identity.
- A current observation may lack a known event effective date.
- The four frames are designed for neutral coverage, not statistical representativeness of the US beauty market.

### 10. Board Status And Run Boundary

```yaml
board_status: READY_FOR_RETRIEVAL_HANDOFF
run_boundary: CHAT_ONLY_BOARD_COMPLETE
next_artifact: docs/research/forseti_beauty_us_company_longlist_scan_v0.md
next_authorized_step: Run the bounded CSB-first neutral discovery scan; do not mint company-pressure candidates.
stop_condition: Stop when the bounded scan can either fill all 60 eligibility cells or name the exact missing stratum/fragrance cell.
```
