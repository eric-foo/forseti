# Handoff Packet — Tiered Retail Capture for Company Understanding

```yaml
retrieval_header_version: 1
artifact_role: completed_implementation_batch_record_and_cold_handoff
scope: >
  Records the landed Steps 1-5 capability and explicitly deferred Step 6 proof.
  No live capture, new implementation, data-lake write, monitoring activation,
  or Understanding rerun is authorized or claimed here.
use_when:
  - Recovering the landed architecture or commissioning the deferred proof step.
  - Recovering the accepted decisions after context loss.
stale_if:
  - A successor changes the direction or batch order.
  - Company-Understanding or Retail/PDP authority materially changes.
authority_boundary: retrieval_only
status: STEPS_1_TO_5_LANDED_STEP_6_DEFERRED
```

## Load Contract

- `mode`: max
- `created_at`: 2026-07-21 Asia/Singapore
- `created_by_lane`: `codex/understanding-tiered-retail-plan`
- `base_revision_at_intake`: `2e2ede165fa1efde2b6dc48b75d934061133bc0f`
- `source_revision_at_plan_close`: `de2e60a8a52bdfe9360a5aa2de2f0606bee299a8`
- `handoff_path`: `docs/workflows/forseti_understanding_tiered_retail_capture_batch_plan_handoff_v0.md`
- `expected_receiver_state`: fresh branch/worktree from current `origin/main`; no dirty target or authority files.
- `load_rule`: **confirm-don't-trust**. Re-read `AGENTS.md`, `.agents/workflow-overlay/README.md`, the active batch's named sources and current Git state before strict or actionable claims. If repo access is unavailable, stop and request a pasted source capsule or no-repo handoff.
- `current_turn_authorization`: retrieval only; no live capture or deferred proof authorization.

## Goal Handoff / Active Objective

Complete company **Understanding** with enough public evidence to explain portfolio shape, customer/use-case coverage, retail expression, relative product traction, strong and weak links, strategic motion, and material dependencies with decision-useful confidence—without pretending retail evidence proves internal economics.

The landed implementation provides a tiered-depth US retail layer that:

1. binds canonical owned identity, uses qualified retailer grids for discovery, and reconciles the union back to owned evidence before selecting heroes;
2. uses Sephora as guarded default retail primary when authorized, US-admissible, and materially complete;
3. shallowly onboards every exact parent listing across each qualified member of the US beauty ladder—Sephora, Ulta, Target, and Amazon;
4. preserves retailer-specific signals without paying four times for syndicated reviews;
5. deepens reviews/Q&A only for evidence-selected products.

Retailer-local longitudinal proof remains explicitly deferred until identity and baseline are stable.

### Success signals

A real company run can produce:

- owned franchise/parent denominator plus typed gaps;
- a grid/assortment outcome for every qualified retailer, including exact absence or failure;
- one full-raw PDP baseline for every exact parent listing found at each qualified retailer;
- Sephora-rich standardized facts and lean retailer-specific comparison facts elsewhere;
- products selected for depth after breadth, not from fame;
- native and deduplicated review counts that remain separate and traceable;
- retailer-local changes over time, with a gap never reported as no change; and
- a concise, confident report whose major numeric, causal, comparative, and action-changing claims resolve to admitted evidence.

## Frozen Decisions

1. **Tiered depth.** All exact parent listings get one baseline at qualified retailers; expensive review/Q&A depth is selected, not universal.
2. **Owned identity, grid discovery, owned closure.** Owned evidence binds canonical identity. Qualified grids expand the candidate set; deterministic reconciliation returns to owned evidence to close the denominator. Retailers remain channel-local expression, not identity authority.
3. **Guarded Sephora primary.** Sephora is default where qualified; override only for a material omission, failed market pin/route, or named non-duplicative job.
4. **Qualified ladder, not quota.** Test Sephora, Ulta, Target, Amazon. Preserve `NOT_LISTED`, `ROUTE_BLOCKED`, `MARKET_UNPINNED`, `SURFACE_NOT_EXPOSED`, or current equivalent. Do not invent listings or completion credit.
5. **Common lean floor.** Exact identity and parent/variant/listing relation, price/promo, availability, aggregate rating/review state, assortment/exclusive cues, timestamp, and residuals. Preserve full source bytes.
6. **Retailer-native extensions.** Keep merchandising, badges, fulfillment, seller/authenticity, related products, Q&A availability, review provider, and native metadata. Amazon adds ASIN/seller/fulfillment/bought-band/rank only when source-visible and admissible.
7. **Sephora-rich layer.** Use standardized taxonomy, suitability attributes, variants, review controls, and captured-corpus demographics. Reviewer self-report is a subset, never a buyer census.
8. **Evidence-selected depth.** Triggers include established prominence, age-adjusted velocity, founding/strategic centrality, recent investment/adjacency, complaint concentration, plausible weak link, contradiction, or incident. No fixed product count.
9. **Deterministic review overlap.** Preserve every occurrence. Match by provider/origin ID and explicit syndication first, then normalized rating/date/author/title/body fingerprint. LLM may flag ambiguous near-matches; it never canonicalizes, deletes, or auto-merges.
10. **Traction, not sales.** Keep retailer series separate, age-normalize when possible, and require another retail behavior before directional portfolio roles.
11. **Grid-first monitoring.** Grid/brand surface is the low-cost detector; light PDP refresh fills missing metrics; material change triggers full recapture; deep reviews refresh only for selected products/jobs.
12. **US first.** Record encountered international facts, but no global map without a named job.
13. **Report voice.** Declarative, confident, characterful. Evidence-bind big claims; keep detailed provenance underneath rather than clutter every sentence.

## Resolved Capability State

All four ladder retailers now have admitted grid projections. Sephora, Ulta, and
Target project retailer-specific brand or assortment grids. Amazon projects a
query-bound ranked-search window complete only for its declared query and
reachable result window, never a guaranteed complete or authorized-only brand
catalog. Capability does not prove route admission; each run still records the
US market pin, reachability, surface boundary, and typed failure.

## Drift Guard

- Steps 1-5 landed and were independently verified. Keep Step 6 as a separately commissioned real-world proof.
- No all-retailer census, source-count completion rule, or universal deep review capture.
- No summing retailer counts without justified corpus identity/deduplication.
- No sales claims from review totals; no demand claim from one stockout.
- Reuse CapturePacket, Cleaning, Silver, and retailer-local extensions; no parallel lake or retailer-specific Silver lane.
- No LLM-owned identity or destructive dedupe.
- No universal cadence. Every series names decision, fact, baseline, trigger/threshold, cadence, route, and action.
- No international buildout, supply investigation, competitor Understanding, archive history, creator/ads, or legal/trademark deepening. Those remain named jobs.
- Do not rewrite historical Clinique/Summer Fridays receipts or research prompts.
- Code/docs existence does not complete Understanding; the deferred Step 6 proof remains required for a company-run completion claim.

## Why Six Batches

| Batch | Why separate | Failure isolated |
| --- | --- | --- |
| 1. Contract | Current authority permits one primary, one conditional secondary, exception-only tertiary. | Runtime implementing behavior the active contract forbids. |
| 2. Baseline capability | Retailer routes are heterogeneous; at plan time grid projection named Walmart, Target, Sephora, not Ulta/Amazon. | A four-retailer promise backed by missing or unequal surfaces. |
| 3. Portfolio onboarding | Company orchestration must reconcile parents, listings, variants, and failures before selection. | Hero bias and partial lists masquerading as architecture. |
| 4. Depth + overlap | Review depth and cross-retailer identity are distinct from listing capture. | Syndicated reviews faking independent support; destructive merges. |
| 5. Understanding integration | Capture capability must become a first-class report contract. | A complete substrate that the report neither exposes nor interprets. |
| 6. Understanding proof | Capture machinery can still yield weak intelligence. | A substrate that does not change or strengthen decisions. |

## Batch Route

### STEP-1 — Align the Understanding contract

**Outcome:** replace current secondary/tertiary cardinality with the qualified-ladder plus tiered-depth rule while retaining named-job discipline, typed failure, and non-claims.

**Must change**

- `docs/decisions/forseti_company_intelligence_information_architecture_v0.md`
- `forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md`
- `forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md`
- `forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md`

**Inspect only; change if cardinality/output is encoded**

- `forseti-harness/tests/unit/test_commission_signal_board_output_validator.py`
- `forseti-harness/tests/fixtures/commission_signal_board_outputs/valid_company_competitive_intelligence_output.txt`

**Acceptance:** all four active docs agree on owned census -> qualified grids -> all exact-parent baseline PDPs -> selected depth; old cardinality is absent; no source quota or new ledger field unless an existing field truly cannot express the rule; CSB gates pass; historical dogfood remains untouched. **Stop after the docs-only patch.**

### STEP-2 — Make the shallow four-retailer baseline executable

**Outcome:** each named retailer produces either a US-admitted grid/PDP shallow baseline or a typed packet-backed failure, without forcing Sephora's shape onto other retailers.

**Documents changed when behavior changes**

- Retail/PDP `README.md`
- `retailer_information_extraction_standard_v0.md`
- `retail_storefront_pin_registry_v0.md`
- `retail_pdp_content_cleaning_contract_v0.md`
- `retail_pdp_silver_producer_contract_v0.md`

All are under `forseti/product/spines/capture/core/source_families/retail_pdp/`.

**Runtime to inspect/patch only where missing**

- `forseti-harness/source_capture/retail_capture_profiles.py`
- `retail_grid_projection.py`, `retail_pdp_content.py`, `retail_pdp_silver.py`
- `forseti-harness/cleaning/retail_pdp.py`
- Sephora/Ulta/Target/Amazon onboarding modules and corresponding runners.

**Focused tests:** `test_retail_capture_profiles.py`, `test_retail_grid_projection.py`, `test_retail_pdp_content_cleaning_silver.py`, four onboarding tests, and retailer pin tests.

**Acceptance:** exact product and US/storefront binding fail closed; raw is authoritative; retailer-native fields survive; success/absence/unpinned/blocked/ambiguous/missing-field paths are tested. Target canonical content v1 is now landed; Amazon remains `raw_unflipped` at plan close with its canonical-content phase startable but unfinished. The common floor may consume admitted canonical content or preserved raw plus a sufficient lean projection, but it must never hide route maturity.

### STEP-3 — Compose complete portfolio onboarding

**Outcome:** owned source-parent census -> every qualified grid outcome -> parent/listing reconciliation -> one full-raw PDP baseline for every exact parent listing -> evidence-backed normalized-family/non-family dispositions with typed unresolved parents -> coverage residuals, all before depth selection.

**Likely docs:** Retail/PDP `README.md`, extraction standard, and only missing operator detail in the CSB playbook.

**Likely runtime:** grid projection; existing retailer onboarding runners; packet/manifest and Cleaning/Silver consumers; one thin company-onboarding compositor only if existing runners cannot enforce parent coverage and retailer outcome accounting. Prefer composition, not new architecture.

**Acceptance:** a multi-retailer fixture yields deterministic coverage and stable retailer-native parent/listing identity; context-only URL parameters do not break identity, while a changed host, non-HTTPS route, or commissioned retailer-variant mismatch fails closed. Retailer-variant binding is accepted only when the route exposes a stable selected-ID extractor. Source parents, normalized families, variant-as-parent objects, bundles/sets, non-products, and unresolved parents remain distinct; no name/category heuristic or partial denominator inflates a complete family count. Rerun does not overwrite raw; acquisition assigns no hero/growth/weak-link label.

### STEP-4 — Add evidence-selected depth and review-overlap linkage

**Outcome:** deepen only evidence-selected products and expose both native occurrences and a deterministically linked unique-review view.

**Must read/likely change**

- `forseti/product/spines/capture/source_families/retail_pdp/retail_pdp_review_capture_spec_v0.md`
- Retailer extraction standard
- `fragrance_purchase_review_row_contract_v0.md` as candidate-key precedent only
- CI architecture only if role inference needs a pointer to the new derived record.

**Runtime:** retailer companion onboarding for selected products; a derived linkage producer in the existing post-Capture seam; Cleaning/ECR ownership chosen after fresh inspection. Raw Capture must not own canonical dedupe decisions.

**Match order:** provider + native/origin ID -> explicit syndication -> normalized exact fingerprint -> ambiguous queue. Preserve occurrences, raw refs, match basis, algorithm version, ambiguity, native total, unique total, overlap rate.

**Acceptance:** deterministic replay; conflicting near-matches remain ambiguous; no raw loss; native totals never change; one fixture selects a non-prominence product and proves fame is not automatic selection.

### STEP-5 — Install Portfolio and Retail Architecture in Understanding

**Outcome:** make the breadth-first owned portfolio, four-retailer corpus,
evidence-selected depth set, and outside-in interpretation a first-class,
validated completed-report section. Longitudinal monitoring is explicitly
deferred until a later owner commission.

**Must read/change**

- CI information architecture
- CSB authority rules, prompt, and playbook
- CSB output validator, company fixtures, and focused tests

**Runtime/tests:** no Capture or monitoring runtime change. Update the company
report validator and its focused fixtures/tests only.

**Acceptance:** canonical Section 5 is `Portfolio And Retail Architecture`; its
six ordered subsections expose the owned denominator, product/claim/price
architecture, qualified retailer corpus, evidence-selected depth, outside-in
interpretation, and strategic positioning/markets/channels; the completion
ledger carries the new lens; validator fixtures prove the section, subsection
order, and lens are mandatory; headings never substitute for evidence-ledger
truth.

### STEP-6 — Prove decision-useful Understanding

**Outcome:** when separately authorized, run a clean-room Summer Fridays acquisition/report under STEP-5 without using the previous run as evidence or selection input. Cross-retailer evidence must materially strengthen, weaken, or change the Understanding; longitudinal evidence is not required.

**Likely surfaces:** CSB prompt/rules/playbook and CI architecture only for observed defects; CSB validator fixture/test if output changes; a new commissioned company seal/report, never a rewrite of historical receipts.

**Report acceptance:** decisive active-verb positioning; calibrated public roles (established leader, growth investment, entry/trial, flagship anchor, experiment/adjacency, plausible weak link, attachment/cross-sell, actively supported, mature); concentration, gaps, overlaps, channel dependencies; observed/inferred/unknown distinction without citation clutter; major claims traceable; duplicated reviews not independent corroboration; at least one conclusion materially changes or gains confidence.

## Cross-Batch Change Map

| Surface | B1 | B2 | B3 | B4 | B5 | B6 |
| --- | --- | --- | --- | --- | --- | --- |
| CI architecture | must | — | — | pointer if needed | must | defect only |
| CSB rules/prompt/playbook | must | — | detail only | — | must | proof defects |
| Retail/PDP docs | — | must | composition | depth | monitoring pointer | — |
| Storefront registry | — | route truth | — | — | — | proof use |
| Grid projection | — | capability | compose | — | — | proof use |
| PDP Cleaning/Silver | — | lean floor | compose | linkage consumer if owned | — | proof use |
| Retailer adapters | — | route gaps | compose | selected depth | — | proof use |
| Review linkage | — | — | — | must | — | proof use |
| Durability series | — | — | — | — | deferred | — |
| CSB fixture/validator | inspect | — | — | — | must | output proof |

## Authorization and Stop Conditions

| Unit | Readiness | Authorization |
| --- | --- | --- |
| STEP-1 | `LANDED` | complete |
| STEP-2 | `LANDED` | complete |
| STEP-3 | `LANDED` | complete |
| STEP-4 | `LANDED` | complete |
| STEP-5 | `LANDED` | complete |
| STEP-6 | `DEFERRED_BY_OWNER` | not authorized |

Every batch runs focused tests, current repo-required gates, `git diff --check`, exact diff inspection, and fresh target verification. Live route changes require live proof; fixtures cannot upgrade registry status. A typed live failure is valid evidence, not fake coverage.

Stop when authority conflicts outside scope; US/target binding fails after its one authorized recovery; raw cannot be preserved; identity ambiguity could change coverage/selection; dedupe would require destructive/unverifiable merge; a stable series key/baseline/gap cannot be preserved; an explicitly deferred domain is required; or another writer/dirty target overlaps.

## Decision Utility

This converts a hero-product vignette into company intelligence. Owned-plus-retailer reconciliation exposes concentration and missing channel coverage. All-parent shallow PDPs expose price ladders, variants, promos, availability, merchandising, and review-state differences. Selective depth spends money where evidence can change the conclusion. Overlap linkage stops syndicated repetition from faking support. Longitudinal observations separate accumulated fame from current momentum. Retailer-native facts expose seller, fulfillment, exclusivity, distribution, and weak-link signals Sephora alone cannot show.

It still cannot reveal exact revenue, margin, sell-through, internal intent, manufacturing contracts, complete non-retailer demand, or global supply exposure. Those are claim ceilings, not reasons to weaken Understanding.

## Confirm-Don't-Trust Source Ledger

Fresh hashes at plan-close source revision `de2e60a8a52bdfe9360a5aa2de2f0606bee299a8` (the separate intake base remains recorded above):

| SHA-256 | Source |
| --- | --- |
| `7111D6E4D8760E34B1611012A33B92691BFFB5C2EEC5C310A7F796FB830FA69C` | `docs/workflows/clinique_moisture_surge_sephora_primary_override_dogfood_20260721_v0.md` |
| `BAA3914E5A2ED23861F0E9344BF0F2579D9F732D553BD238670F761DCAD2DB5C` | `docs/decisions/forseti_company_intelligence_information_architecture_v0.md` |
| `A758B6C9DDACC2E5E6BFE7B13481D288F1031102969BC767915824296DB73B32` | CSB authority rules |
| `8E603DEACC4B9345989E994F2CA218622DB7625BAA155E92FAF002AE84FFEB83` | CSB prompt |
| `60049A0075665EEE236E57B636FB89C72901BF17D7576062DE94032A3400A1E7` | CSB playbook |
| `B2B3CD29453E6386B4459CEC3DAF67744C804746C93E0709C2DEEAB9AA3CCB65` | Retail/PDP README |
| `55B3B643C96DAF90CEC00C3A20FE6551B5F2D870457B9CC01DD4E6A761DC2BA1` | retailer extraction standard |
| `3F100F2347BC51B7C58C10586E22D11E02F5C17068525AC4505F3B811A9EF574` | storefront pin registry |
| `8F192EA1144276C59C3FCF2D8A5A37AC2624A49657F0FBE40062E0E72291FD37` | multi-retailer rendered spec |
| `704B8D4F7FE237B7C83F8BC34D3E1AA52CDB6486797EC2E33472F4713A7F582E` | content Cleaning contract |
| `9B563A6EA631B953AB28406FB674A19C94E11296ACB343E29D246CC5F95CA1F5` | Silver producer contract |
| `D418C1B8CB6AF6C4C10911866F18A23E1C44DE951E560E4C0AF17288884899A5` | review capture spec |
| `7399E3FB30E34E9F5BBD8E643DF37385DF4325BE327D5333CD47E348B273F215` | review-velocity profile |
| `41DB97F2BB55B2654F7467EAD9B331E3F1809C232870410205D31BC392D99F9D` | availability/restock profile |
| `EFA32BA8D2A9DA17E5256F1A016535FFC292F84059982369A112EC0F101087ED` | price-timeseries profile |
| `9C47DA39A56A01742E1B22E0A85660C6063EEEAEC57AC9AF70DF33B53D57A6D9` | `docs/workflows/retail_pdp_target_amazon_canonical_content_handoff_v0.md` |

Resolve shorthand paths through the Retail/PDP README and repo map; hashes are compare targets, never substitutes for re-reading current bytes.

## Route Status

- `plan_intake`: complete
- `acceptance_basis`: explicit owner acceptance of tiered depth
- `implementation_profile`: standard; STEPS 1-5 landed, STEP-6 deferred
- `implementation_start_readiness`: none active; STEP-6 needs its own owner commission
- `current_turn_authorization`: retrieval only
- `next_authorized_step`: none authorized here; the separately commissioned STEP-6 proof is the remaining unit

Recommended Implementation Model: judgment_lane — multi-domain contracts require sequencing judgment
