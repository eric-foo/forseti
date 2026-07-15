# Forseti Beauty US Problem Discovery-to-Wedge Contract v0

```yaml
retrieval_header_version: 1
artifact_role: accepted GTM run contract
scope: Frozen Phase A rules and Phase B entry conditions for the first US consumer-beauty problem-discovery run.
use_when:
  - Starting or explaining the US Beauty neutral-company-pool run.
  - Deciding whether a company may enter the eligibility pool or a later decision-pressure pass.
  - Separating Company Surface facts from GTM interpretation.
authority_boundary: accepted_for_this_run
```

## Status and authority

Status: `ACCEPTED_FOR_FIRST_RUN`

This contract supersedes earlier Beauty GTM working assumptions for this run. It binds the Phase A decisions needed to construct the neutral company pool. It does not establish a permanent ICP, buyer, offer, or wedge.

The company-selection companion is [forseti_beauty_us_company_selection_v0.json](../../../../../docs/research/forseti_beauty_us_company_selection_v0.json). The human adjudication is [forseti_beauty_us_company_eligibility_pool_v0.md](../../../../../docs/research/forseti_beauty_us_company_eligibility_pool_v0.md).

## Frozen run decisions

- Market: United States.
- Observed unit: a consumer-facing beauty **Brand**. A parent may be recorded, but the Brand is the company-pool row.
- Eligible longlist: exactly 60 Brands: 18 emerging, 30 scaling, and 12 established.
- Final pool: exactly 20 Brands: 6 emerging, 10 scaling, and 4 established.
- Fragrance: exactly three final Brands, one in each stratum. Each stratum must retain at least two eligible fragrance replacements.
- Low-observed-trigger comparators: exactly four final Brands: one emerging, two scaling, and one established. This label means only that the bounded eligibility scan did not surface an obvious current pressure trigger; it is not evidence of low pain or low opportunity.
- Category diversity: at least four non-fragrance categories in the final pool, with no category above five Brands.
- Parent concentration: no more than two selected Brands under one resolved parent.
- Generic Deep Research is not used. The current CSB and Scanning spine supplies bounded discovery pointers.
- Existing influencer coverage does not determine fragrance selection.

## Neutral discovery and evidence floor

Scanning discovers pointers; GTM decides eligibility and pool membership. A Brand qualifies only when the record shows:

1. current US availability or a meaningful US operation;
2. at least two source families, including one first-party Brand source;
3. lawfully accessible evidence;
4. a bounded Brand identity, while unresolved parent ownership stays explicit; and
5. observable activity no more than 180 days before the run date.

For this first run, a live official or retailer surface observed on the run date is dated activity at **observation time**. It proves that the surface was observable then; it does not prove when the underlying product, launch, distribution agreement, or company event began. Every row therefore keeps `observed_at`, `date_basis`, and the absence of a known effective date separate.

The eligibility scan is screen-light. It may support pool construction, but it may not be reused as a substantive company diagnosis.

## Operating-shape rules

- **Emerging:** observed DTC availability plus no more than one national US retailer, with no evidence of broad national multichannel distribution.
- **Scaling:** at least two observed US retail partners, or one national partner plus a documented current distribution expansion; the established rule does not clear.
- **Established:** documented broad distribution across at least three of these channel types: DTC, specialty beauty, mass/drug, department, or owned retail. Parent ownership alone never establishes the tier.

If the evidence does not support one rule, the row is ineligible. The classifier does not choose the most flattering tier.

## Deterministic final selection

Normalize each eligible Brand name by Unicode-aware case folding, collapsing internal whitespace, and trimming. Compute SHA-256 over:

`forseti-beauty-us-pool-v0|<normalized-brand-name>`

Within each stratum, select in ascending hash order while enforcing the frozen quotas. First reserve the lowest-hash fragrance row, then the required comparator rows, then fill the remaining slots in hash order. Once a stratum's exact fragrance or comparator quota is full, later rows carrying that flag are skipped. Category and resolved-parent caps apply globally. Every skip is retained, and unselected eligible rows remain in ascending-hash replacement order.

A selected Brand may be replaced only for failed eligibility, identity, access, duplication, or source coverage. Replacement re-runs the same constraints for the affected vacancy. Apparent interest, familiarity, influencer fit, or a suspected pain point is not a replacement reason.

## Company Surface / GTM boundary

Company Surface is the factual history layer. It may later hold dated, sourced observations and identity/parent/channel facts. GTM owns the temporary eligibility label, stratum classification, comparator designation, selection hash, pool membership, and later hypotheses.

This work unit does not depend on unmerged Company Surface PR #967 and does not implement a Company Surface schema, runtime, corpus, or write path. The selection JSON is a research companion, not a Company Surface logical record. Pool membership is administrative metadata and is never company evidence.

The first substantive company decision-pressure pass remains blocked until the minimal Company Surface-compatible proving slice is functional enough to preserve its factual outputs without mixing them with GTM judgment.

## Research bounds and stop conditions

- Seed four discovery frames: broad US beauty retail, emerging-brand programmes, official established portfolios, and broad plus specialist fragrance retail.
- Cap each frame at 30 distinct Brand pointers and the combined raw discovery set at 120.
- Discovery emits only Brand, URL, source frame, apparent category, US/parent/channel/activity pointers, limitations, and coverage notes.
- Discovery must not emit or rank company pain, buyer, ICP, priority, outreach, or wedge claims.
- Stop Scanning when 60 rows clear the evidence floor and all stratum/fragrance replacement cells are fillable.
- Fail loudly if a quota is not fillable. Reopen Scanning only for the named missing cell; do not weaken the evidence floor or quota.
- Stop this work unit after the contract, CSB board, scan receipt, 60-row companion, final 20 adjudication, routing update, and validations are durable.

## Gates before later company work

`HOLD` until all of the following are true:

- the pool artifacts pass their validators and invariant checks;
- a cold reader can trace every selected Brand from this contract to its source pointers and selection reason without chat history;
- the minimal Company Surface-compatible proving slice can preserve facts separately from GTM interpretation; and
- a later commission names one company at a time for a Company Decision-Pressure Pass.

This contract authorizes neither outreach nor runtime, crawler, monitor, registry, or capture-runner construction.

## Direction change propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The first US Beauty run now has a frozen Brand-level neutral-pool contract;
    Scanning supplies bounded pointers while GTM owns eligibility and deterministic selection.
  trigger: output_authority
  related_triggers: [source_truth, lifecycle_boundary]
  controlling_sources_updated:
    - forseti/product/spines/product_lead/gtm/forseti_beauty_us_problem_discovery_to_wedge_contract_v0.md
    - docs/workflows/forseti_repo_map_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/product_lead/gtm/forseti_demand_signal_gtm_design_v0.md
    - forseti/product/spines/scanning/README.md
    - forseti/product/information/company_surface/README.md
    - forseti/product/information/company_surface/purpose_contract_v0.md
  intentionally_not_updated:
    - path: forseti/product/spines/product_lead/gtm/forseti_demand_signal_gtm_design_v0.md
      reason: It remains historical context after the GTM reset; this run-specific contract supersedes it only for the current Beauty run.
    - path: forseti/product/information/company_surface/
      reason: Company Surface implementation and schema choices are explicitly outside this work unit.
  stale_language_search: >
    rg -n -i "beauty.*(24 companies|twenty-four)|scanning.*(choose|rank).*pain|company surface.*pool membership" docs forseti/product
  non_claims:
    - not a permanent ICP, buyer, offer, or wedge decision
    - not Company Surface implementation or readiness
    - not company pain evidence
    - not outreach authorization
```
