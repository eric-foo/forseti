# Tower 28 Beauty Company Decision-Pressure Commission Signal Board v0

```yaml
retrieval_header_version: 1
artifact_role: source-family commission for one-company public decision-pressure discovery
scope: Bounded forward Commission Signal Board for Tower 28 Beauty (USBEAUTY-019) before one-company CSB-first Scanning.
use_when:
  - Executing or auditing the first Tower 28 public decision-pressure scan.
  - Checking commissioned source families, counterevidence paths, and the public-evidence ceiling.
  - Separating retrieval routes from later GTM interpretation.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/scanning/README.md
  - docs/workflows/forseti_beauty_tower28_company_decision_pressure_handoff_v0.md
stale_if:
  - The governing Beauty US GTM contract changes its one-company research boundary.
  - Tower 28 is no longer the deterministically selected USBEAUTY-019 Brand.
```

### 1. Commission Intake Receipt

```yaml
commission_id: BEAUTY-TOWER28-DP-001
mode: forward
candidate_or_subject: Tower 28 Beauty (USBEAUTY-019)
decision_context: discover public observations that could nominate or disconfirm Tower 28 decision-pressure hypotheses for later GTM adjudication
market_or_geography: United States
time_window: prioritize current state and the most recent 24 months; use older evidence only for chronology or contradiction
evidence_cutoff_at: not_applicable
input_status: complete
missing_required_inputs: []
cutoff_rule: not_applicable_forward_run
non_goals_preserved:
  - no generic Deep Research
  - no Company Surface write, mapping, ingestion, schema fit, compatibility, or readiness claim
  - no pain, buyer intent, urgency, willingness-to-pay, priority, or wedge confirmation
  - no outreach, runtime, crawler, monitor, registry, capture runner, or private-system work
  - no replacement of Tower 28 because another Brand appears more interesting
boundedness:
  subject_count: exactly_one_brand
  monetary_or_token_budget: none_imposed
  operational_bounds: named source families, lawful public access, 24-month priority window, and declared saturation stop
saturation_stop: >
  Stop when every material problem hypothesis has an independent corroboration
  path or is downgraded to single-source/unknown; every commissioned source family
  is checked or blocked; all mandatory counterevidence paths are checked; and two
  consecutive frontier rounds yield no new material hypothesis or contradiction.
starting_pointer_notice: >
  The official brand site, Sephora catalog, and Revolve catalog are screen-light
  starting routes observed on 2026-07-16. Observation time proves neither an
  underlying event date nor company pressure.
```

### 2. Boundary Statement

This is an evidence/signals-only source-family commission. It is not a pain or demand verdict, buyer or priority claim, graph artifact, forecast, proof claim, judgment, Company Surface record, or client output. Public observations may nominate or weaken later GTM hypotheses only after the scan is sealed.

### 3. Source-Family Coverage Plan

| Source family | Subfamily / surface | Capture posture | Why check it | Expected observable | Evidence status | Surface cutoff status | Cutoff status | Notes |
|---|---|---|---|---|---|---|---|---|
| owned_channels | official brand site and public brand pages | available_now | establish owned chronology, assortment, claims, and distribution framing | dated or current first-party statements | source_backed | not_applicable | not_applicable | High chronology value, low independence. |
| retail_pdp | Sephora catalog | available_now | corroborate current US retail presence and route to assortment/review detail | catalog, PDP, price, availability, reviews | source_backed | not_applicable | not_applicable | Listing is not sell-through. |
| retail_pdp | Revolve catalog | available_now | second retailer route and channel-state corroboration | catalog, PDP, price, availability, discounts | source_backed | not_applicable | not_applicable | Listing is not demand. |
| news_editorial_trade | trade press, interviews, funding and distribution reports | available_now | test independent chronology and company-motion claims | dated reporting and attributable statements | to_retrieve | not_applicable | not_applicable | Syndicated copies must not count as independent. |
| professional_org_motion | ATS/careers, leadership pages, public org announcements | available_now | test priority and capability-building clues | roles, leadership changes, team remit | to_retrieve | not_applicable | not_applicable | Prefer ATS/careers; LinkedIn is no-live/planning-only. |
| reviews | retailer reviews and complaint patterns | available_now | identify repeated product experiences and contradictions | dated review language, helpfulness context, retailer responses | to_retrieve | not_applicable | not_applicable | Complaints are not company pain. |
| forums_community | independent public community discussion | manual_only | surface consumer language, comparisons, objections, and rebuttals | dated public threads and independent participant language | to_retrieve | not_applicable | not_applicable | Public, repeatable, bounded slices only. |
| creator_social_video | disclosed creator and campaign activity | manual_only | test campaign concentration versus broader response | dated public posts/videos, disclosure, campaign overlap | to_retrieve | not_applicable | not_applicable | No comment scraping, follower graph, or dossier. |
| search_discovery | search_surface_mgt and exact-query discovery | manual_only | find hidden venues, comparisons, negatives, and current-state changes | query-led route pointers, negatives, access notes | to_retrieve | not_applicable | not_applicable | Query count or rank is not demand proof. |
| other | official regulatory, trademark, recall, litigation, or corporate records | available_now | check decision-relevant official contradiction or risk | dated official record | to_retrieve | not_applicable | not_applicable | Use only when relevant; absence is not absence of pressure. |

### 4. Signal Board Rows

| Row ID | Source family | Subfamily | Surface | Observable | Signal role | Row purpose | Recency status | Recency attention | Graph role | Graph weight hint | Evidence status | Provenance needed | Surface cutoff status | Cutoff status | Handoff note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SBR-001 | owned_channels | official_brand_site | tower28beauty.com | current official brand surface | owned_claim | source_route | current_state | high | seed | medium | source_backed | https://www.tower28beauty.com/ observed 2026-07-16; effective date unknown | not_applicable | not_applicable | Starting route only; retrieve dated claims and chronology. |
| SBR-002 | retail_pdp | sephora_catalog | Sephora Tower 28 search/catalog | current US retailer listing | retail_corroboration | source_route | current_state | high | node_candidate | medium | source_backed | https://www.sephora.com/search?keyword=Tower+28+Beauty observed 2026-07-16; effective date unknown | not_applicable | not_applicable | Starting route only; listing is not sell-through or pressure. |
| SBR-003 | retail_pdp | revolve_catalog | Revolve Tower 28 search/catalog | current US retailer listing | retail_corroboration | source_route | current_state | high | node_candidate | medium | source_backed | https://www.revolve.com/r/Search.jsp?search=Tower+28+Beauty observed 2026-07-16; effective date unknown | not_applicable | not_applicable | Starting route only; listing is not demand or pressure. |
| SBR-004 | owned_channels | official_chronology | brand newsroom, about, launch, retailer and product pages | official launch and distribution chronology | owned_claim | chronology | current_state | high | propagation_path | low | to_retrieve | dated first-party URL and publication/effective date if available | not_applicable | not_applicable | Separate attributable claim, publication date, and inferred event date. |
| SBR-005 | news_editorial_trade | trade_interviews_reports | trade press and attributable interviews | funding, distribution, launch, and operational motion | org_motion | signal_unit | recent | high | edge_candidate | medium | to_retrieve | original publisher URL, date, author, attribution, and syndication check | not_applicable | not_applicable | Prefer original reporting and independently sourced corroboration. |
| SBR-006 | professional_org_motion | ats_careers_leadership | official ATS/careers and leadership announcements | roles, remit, hiring, leadership movement | org_motion | signal_unit | current_state | high | edge_candidate | medium | to_retrieve | official ATS/careers or company announcement URL and observation date | not_applicable | not_applicable | LinkedIn remains no-live/planning-only. |
| SBR-007 | reviews | retailer_reviews | Sephora and other lawful retailer review surfaces | repeated experiences, complaints, praise, and contradictions | review_experience | contradiction | recent | high | counterevidence_path | medium | to_retrieve | review URL, review date, visible context, source convention, and duplication limits | not_applicable | not_applicable | Do not infer company pain from complaint prevalence. |
| SBR-008 | forums_community | independent_public_discussion | public repeatable community threads | consumer language, comparisons, objections, and rebuttals | consumer_language | contradiction | recent | high | counterevidence_path | medium | to_retrieve | thread URL, post date, retrieval date, participant context, and access note | not_applicable | not_applicable | Treat absence or low yield as a bounded negative, not universal absence. |
| SBR-009 | creator_social_video | disclosed_creator_campaigns | public disclosed creator posts and videos | campaign concentration, timing, disclosure, and public response context | creator_attention | signal_unit | recent | high | campaign_overlap_check | medium | to_retrieve | public URL, post date, disclosure, retrieval date, and campaign-overlap caveat | not_applicable | not_applicable | Attention and engagement are routing context, not demand proof. |
| SBR-010 | search_discovery | search_surface_mgt | bounded exact public queries and first-pass results | hidden venues, comparison language, negatives, and access walls | search_interest | source_route | current_state | high | propagation_path | low | to_retrieve | exact query, intent, retrieval date, result class, and next-route decision | not_applicable | not_applicable | Route to Scanning exact-query/frontier work; no standing query monitor. |
| SBR-011 | retail_pdp | assortment_price_availability | lawful retailer PDP/catalog states | assortment, price, availability, discount, and channel change chronology | retail_corroboration | chronology | current_state | high | edge_candidate | medium | to_retrieve | retailer URL, observed state/date, effective date if stated, and comparison limit | not_applicable | not_applicable | State change may nominate a hypothesis; it does not establish sell-through or pressure. |

### 5. Mandatory Counterevidence Paths

| Path ID | What could disconfirm or weaken the signal | Source families to check | Why it matters | Evidence status | Cutoff rule |
|---|---|---|---|---|---|
| CE-001 | Growth, launch, funding, or distribution narrative is mistaken for decision pressure. | owned_channels; news_editorial_trade; retail_pdp | Expansion can be healthy execution rather than strain. | to_retrieve | not_applicable_forward |
| CE-002 | Campaign amplification is mistaken for underlying demand. | creator_social_video; search_discovery; reviews; forums_community | Paid or coordinated attention can repeat without independent consumer behavior. | to_retrieve | not_applicable_forward |
| CE-003 | Retailer listing is mistaken for sell-through, velocity, or channel success. | retail_pdp; reviews; news_editorial_trade | Catalog presence supplies availability context only. | to_retrieve | not_applicable_forward |
| CE-004 | Review complaints are mistaken for company pain or a decision owner priority. | reviews; forums_community; owned_channels | Product experience does not establish internal consequence, priority, or action. | to_retrieve | not_applicable_forward |
| CE-005 | Self-promotional founder or company claims are treated as independent corroboration. | owned_channels; news_editorial_trade; professional_org_motion | Attribution and independence control claim strength. | to_retrieve | not_applicable_forward |
| CE-006 | Common scaling-beauty problems are falsely labeled Tower-28-specific. | news_editorial_trade; professional_org_motion; retail_pdp; reviews | The pass must separate category-level scaling mechanics from company-specific clues. | to_retrieve | not_applicable_forward |
| CE-007 | Absence of public evidence is treated as absence of pressure. | all commissioned families | Public silence may reflect source limits, privacy, or timing. | to_retrieve | not_applicable_forward |
| CE-008 | Syndicated copies are counted as independent corroboration. | news_editorial_trade; owned_channels; search_discovery | Repetition can create false breadth. | to_retrieve | not_applicable_forward |

### 6. Campaign And Duplication Risk

| Risk ID | Possible duplication/campaign pattern | Surfaces implicated | Required check | Evidence status | Handoff note |
|---|---|---|---|---|---|
| DUP-001 | PR release repeated by trade/editorial outlets | owned_channels; news_editorial_trade | trace wording and attribution to the earliest origin | to_retrieve | Count one origin unless independent reporting adds facts. |
| DUP-002 | Creator seeding or affiliate campaign appears as independent consumer attention | creator_social_video; search_discovery | record disclosure, timing, phrasing, affiliate links, and cluster overlap | to_retrieve | Do not call manipulation without source-backed evidence. |
| DUP-003 | Brand and retailer product copy is syndicated | owned_channels; retail_pdp | compare copy and source ownership | to_retrieve | Retail corroboration is not an independent experience claim. |
| DUP-004 | Repeated review or forum language comes from copied material or one incident | reviews; forums_community | inspect dates, wording, source conventions, and original context | to_retrieve | Preserve ambiguity when identity cannot be established. |

### 7. Graph Retrieval Brief

```yaml
graph_retrieval_brief:
  seed_entities:
    - Tower 28 Beauty (USBEAUTY-019)
  adjacent_entities_to_check:
    - named products, retailers, launches, partners, executives, roles, and campaigns encountered within the bounded walk
  creator_slices:
    - disclosed public campaign posts or videos encountered through bounded exact-query/frontier work
  source_families:
    - owned_channels
    - retail_pdp
    - news_editorial_trade
    - professional_org_motion
    - reviews
    - forums_community
    - creator_social_video
    - search_discovery
    - other_official_records_when_relevant
  mandatory_counterevidence_paths: [CE-001, CE-002, CE-003, CE-004, CE-005, CE-006, CE-007, CE-008]
  node_types_to_retrieve: [Brand, Product, Retailer, Person, Role, Campaign, OfficialRecord]
  edge_types_to_retrieve: [launched, listed_by, partnered_with, hired_for, led_by, promoted_in, discussed_in, contradicted_by]
  campaign_overlap_checks: [shared wording, disclosure, affiliate links, timing clusters, common PR origin, retailer-brand syndication]
  graph_weight_notes: relation utility only; never signal strength, demand confidence, pressure, or proof
  surface_cutoff_notes: forward mode; record publication, event/effective, and retrieval dates separately
  forecast_targets_supported_without_probabilities: [assortment change, availability change, discounting, review-pattern change, creator-attention decay, org-motion change]
  backtest_cutoff_date: not_applicable
  future_info_exclusion_rule: not_applicable_forward_run
```

### 8. Demand-Classifier Handoff Packet

```yaml
classifier_handoff_packet:
  candidate_or_subject: Tower 28 Beauty (USBEAUTY-019)
  decision_context: discover public observations that could nominate or disconfirm Tower 28 decision-pressure hypotheses for later GTM adjudication
  mode: forward
  cutoff_date: not_applicable
  signal_rows_for_handoff: [SBR-001, SBR-002, SBR-003]
  counterevidence_rows_for_handoff: []
  source_family_gaps:
    - SBR-004 through SBR-011 remain unretrieved routes or gaps
  provenance_gaps:
    - starting-pointer observation dates do not establish underlying event dates
    - no sourced company-pressure observation has yet been retrieved
  cutoff_uncertainties: []
  durability_projection_evidence_or_gap: gap; no durability inference is commissioned at board stage
  decay_lifespan_evidence_or_gap: gap; no decay-lifespan inference is commissioned at board stage
  manufactured_hype_dedup_risk: open; creator, PR, retailer-copy, and syndication overlap require retrieval
  classifier_mapping_status: classifier_owned
  prohibited_claims:
    - no demand verdict
    - no buyer-proof claim
    - no validation or readiness claim
    - no graph score
    - no forecast probability
    - no company pain, buyer intent, urgency, willingness-to-pay, priority, or wedge claim
```

### 9. Visible Limitations

- Starting pointers are screen-light current-availability routes observed on 2026-07-16, not event dates or evidence of pressure.
- Public evidence cannot establish internal priorities, consequences, urgency, budget, buyer intent, willingness to pay, or a wedge.
- The 24-month priority window may miss older chronology; older evidence is admitted only when it changes chronology or contradiction.
- No standing monitoring, exhaustive web coverage, private source, authenticated surface, paywall bypass, LinkedIn live access, comment scraping, creator dossier, graph construction, classifier mapping, or Capture route is authorized.
- Inaccessible, undated, syndicated, stale, ambiguous, or dependent sources must remain visibly labeled.
- Candidate factual observations are not imported into Company Surface and make no eventual-schema compatibility claim.

### 10. Board Status And Run Boundary

```yaml
board_status: READY_FOR_RETRIEVAL_HANDOFF
run_boundary: CHAT_ONLY_BOARD_COMPLETE
next_authorized_step: one-company CSB-first Scanning, not pain classification
```
