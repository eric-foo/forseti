# Beauty Minimum-Complete Retailer Corpus Research Commission Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Research commission prompt (product-planning family)
scope: >
  Commissions a US-first, cross-company study to identify the smallest retailer
  capture capability set that maximizes distinct decision-relevant assortment,
  product, review, and purchase-context evidence while minimizing redundant
  retailer coverage. It also derives the smaller retailer subset to activate
  for one company. It does not commission route implementation, volume capture,
  data-lake writes, or a claim about the percentage of unique customers reached.
use_when:
  - Deciding which three or four beauty-retailer routes Forseti should prioritize for deep capture support.
  - Designing a per-company primary, contrast, and exception retailer selection rule.
  - Testing whether Amazon, Target, Ulta, Walmart, or a department-store route adds material evidence beyond Sephora.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md
  - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
  - docs/research/forseti_beauty_retailer_surface_probe_results_v0.md
stale_if:
  - A later accepted study supersedes the retailer capability set or per-company activation rule.
  - Retailer access, review providers, storefronts, or Forseti capture profiles materially change.
  - The owner changes the initial decision market from US beauty retail.
```

## Forseti Prompt Preflight

```yaml
preflight_defaults: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md v0 - constants bound; deltas stated inline.
output_mode: file-write
template_kind: full-prompt
template_source: project-local research commission plus retail-PDP and CSB source contracts
prompt_artifact_path: docs/prompts/product-planning/beauty_minimum_complete_retailer_corpus_research_commission_prompt_v0.md
downstream_output_artifact_path: docs/research/forseti_beauty_minimum_complete_retailer_corpus_research_v0.md
workspace_binding: receiver records the exact isolated Forseti worktree, branch, HEAD, and prompt blob before research
receiver_binding: one repo-capable research lane with current public-web access
source_pack: named in Required Source Load; receiver records exact paths and blobs for repository sources
dirty_state_allowance: clean isolated worktree except the single commissioned research report
controlling_source_state: confirm from current bytes; do not trust this prompt's summaries
edit_permission: docs-write
doctrine_change_decision: no doctrine change authorized
implementation_authority: none
reviews: findings-first if separately commissioned
validation_gates: prompt output-mode check, retrieval header, map links, repo-map freshness, placement, diff check
```

## Goal Handoff / Active Objective

Answer this bound question:

> What is the smallest retailer **capability set** Forseti should support deeply,
> and the smallest retailer **runtime subset** it should activate for one beauty
> company, to maximize distinct decision-relevant purchase-context and customer-
> evidence coverage while minimizing duplicated assortment and syndicated review
> capture—without claiming population reach the available evidence cannot observe?

The owner expects that three or four deeply supported retailers may be enough at
platform level. Treat `3–4` as a hypothesis to test, not a quota to satisfy. A
smaller set may win if it preserves the material evidence jobs; a larger set may
be recommended only if the study identifies a named, decision-relevant blind
spot that no smaller set covers.

This is a general beauty-company design question. Summer Fridays may be one
representative case, but it must not determine the answer by itself.

## Decision This Research Must Enable

The report must let an owner decide:

1. which retailer routes deserve the next data-lake/capture investment;
2. which one retailer normally anchors a company Understanding pass;
3. when a second retailer adds a genuinely different evidence world rather than
   a duplicate listing and duplicate reviews;
4. the narrow condition under which a third per-company retailer is justified;
5. whether Amazon belongs in the platform core, is conditional, or is a poor
   trade relative to another retailer; and
6. which non-retailer evidence is required to address retailer avoidance or
   non-purchasers that retailer pages cannot observe.

The platform capability set and the per-company runtime subset are separate
answers. Do not recommend capturing every supported retailer for every company.

## Terms And Claim Boundary

Use these definitions consistently:

- **Retailer capability set**: the small set of retailer routes Forseti chooses
  to support reliably at platform level.
- **Runtime subset**: the retailer sources activated for a particular company or
  franchise after owned portfolio architecture is known.
- **Primary retailer**: the authorized retailer providing the strongest combined
  assortment, product-metadata, and customer-evidence surface for that company.
- **Contrast retailer**: a second retailer admitted only because it adds a named
  non-duplicative purchase context, assortment segment, review population, or
  metadata surface.
- **Exception retailer**: a third retailer admitted only to resolve a remaining
  material contradiction or blind spot.
- **Observed retailer audience**: purchasers or reviewers visible at that
  retailer. It is not the company's full customer population.
- **Coverage**: coverage of specified evidence jobs and observed purchase
  contexts. Do not silently redefine it as percentage of unique customers.

Do not claim that a retailer set reaches “most customers,” “all buyer types,” or
a measured percentage of unique people unless a representative, deduplicated
consumer panel or first-party dataset directly supports that claim. Retailer
pages cannot observe people who considered but rejected the retailer, abstained
from the category, bought offline without leaving evidence, or avoided a
retailer for ethical, political, geographic, membership, price, trust, or access
reasons.

A large review sample does not repair that boundary. For example, 1,000 observed
reviews can make estimates within that observed review population statistically
precise, but cannot remove self-selection, missingness, retailer selection,
review syndication, incentive, survivorship, or purchaser-only bias. Report
sample size, denominator, missingness, and selection mechanism separately.

## Confirm-Don't-Trust Load Contract

Before making strict or actionable claims:

1. Record the absolute workspace, branch, `HEAD`, dirty state, prompt blob, and
   each named repository source blob.
2. Re-read the named load-bearing sources from their current bytes. Do not rely
   on summaries in this prompt, prior chat, handoff prose, or filenames.
3. Classify the load:
   - `REUSE`: named sources exist and their current contracts support this commission;
   - `REFRESH`: source contracts remain usable but volatile retailer facts require fresh observation;
   - `BLOCKED`: a controlling source is absent, contradictory, or cannot be read.
4. State `SOURCE_CONTEXT_READY` only after the load succeeds. If repository
   access is unavailable, stop and request a pasted source capsule or a no-repo
   handoff. If a controlling source is blocked, write no research conclusion.
5. Treat historical packet reports and handoffs as route evidence only to the
   degree their current bytes and named primary receipts support. Freshly verify
   all current retailer, access, assortment, and policy claims on the public web.

## Required Source Load

Read completely:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-of-truth.md`
4. `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md`
5. `forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md`
6. `docs/workflows/forseti_bazaarvoice_retailer_compatibility_implementation_handoff_v0.md`
7. `docs/research/retail_pdp_review_record_capture_recon_v0.md`
8. `docs/research/forseti_sephora_brand_grid_capture_live_proof_v0.md`

Read these bounded sections from the current bytes:

9. `forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md` — portfolio-first source order, retailer limit, review-signal limits, and evidence-selected franchise rules.
10. `forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md` — owned architecture, primary/secondary/tertiary retailer rules, and reviewer-demographic boundaries.
11. `forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md` — portfolio-first sequence, typed acquisition failure, escalation, and Deliver blocking rules.
12. `docs/research/forseti_beauty_retailer_surface_probe_results_v0.md` — execution status; Sephora, Target, Amazon, Ulta, Walmart, Nordstrom, and Kohl's route/market-pin findings; Bazaarvoice compatibility; and non-claims.
13. `forseti-harness/source_capture/retail_capture_profiles.py` — current profile inventory and retailer-specific sufficiency requirements only.

If a section heading has moved, locate the equivalent current section and record
the new heading. Do not expand into unrelated implementation sources unless a
specific route claim cannot otherwise be resolved.

## Research Boundary And Starting Hypotheses

Initial market: US beauty retail. Note international transfer risks, but do not
turn this into a global retailer study.

Start with, but do not automatically select, these candidate retailer families:

- prestige specialty: Sephora;
- mass-plus-prestige beauty specialty: Ulta;
- marketplace/convenience: Amazon;
- mass generalist/value and household trip: Target and Walmart;
- department-store/luxury/service: Nordstrom and one evidence-supported peer if needed;
- shop-in-shop or access-extension: Sephora at Kohl's;
- selective fashion/lifestyle or cross-border specialist only if the sampled
  companies reveal a material gap;
- brand DTC/owned assortment as a control, not as one of the retailer slots.

A retailer name is not an archetype by assertion. Establish its purchase-context
job from first-party retailer material, filings, direct public surfaces, and, if
available, credible independent consumer research.

Amazon must receive a real adjudication because it can add marketplace,
convenience, price, seller, and availability context. Do not include it merely
because it is large. Test whether its authorized-brand coverage, seller-quality
signal, review independence, public route depth, and marginal decision value
outweigh its thinner or access-constrained evidence surfaces.

## Representative Case Design

Use a bounded, evidence-led sample rather than one hero product or one company.
Select 8–12 beauty companies across at least four materially different
distribution patterns, such as:

- prestige specialty-led or exclusive;
- broad prestige omnichannel;
- masstige or mass-plus-specialty;
- marketplace-heavy or Amazon-authorized;
- DTC-led with selective retail;
- a brand whose assortment differs materially by channel.

Include at least two product categories and at least one company with meaningful
skincare depth. Record the selection rationale and known sample bias. Summer
Fridays may be included as a prestige-specialty case, not as the default model.

For each case, begin with owned portfolio architecture and canonical product/
franchise names. Then inspect only the bounded retailer grids and representative
PDP/review surfaces needed to answer retailer overlap and marginal-value
questions. Do not attempt complete volume capture.

Stop adding cases when two successive well-chosen cases add no new retailer
archetype, material evidence job, route limitation, or selection-rule change.
If saturation is not reached by 12 cases, report that uncertainty instead of
silently expanding the commission.

## Evidence Jobs To Test

Assess each retailer against the same decision-relevant jobs:

1. **Authorized assortment coverage** — which owned franchises/products are
   listed; exclusives, omissions, bundles, channel variants, sizes, shades, and
   apparent discontinued or stale listings.
2. **Portfolio reconstruction value** — ability to map brand → franchise →
   product → variant/SKU without confusing retailer listings with the owned
   complete portfolio.
3. **Commercial-presentation value** — price, promotions, availability,
   bestseller/order signals, badges, merchandising, category placement, and
   seller identity, bounded by what the surface actually exposes.
4. **Product-fit metadata** — concerns, skin type, age or life-stage labels,
   usage, ingredients, claims, routines, and other retailer-authored facets.
5. **Customer-evidence depth** — rating/review aggregates, dates, text, filters,
   reviewer attributes, helpfulness, incentives, verification, media, and Q&A.
6. **Review independence** — provider, IDs, bodies, timestamps, counts, and
   syndication markers sufficient to detect duplicate or shared review corpora.
7. **Purchase-context contrast** — the different shopping mission the retailer
   evidences, supported rather than guessed.
8. **Route fitness** — current public accessibility, storefront/market pin,
   profile maturity, reproducibility, failure visibility, capture footprint,
   and ongoing maintenance cost.
9. **Geographic and access boundary** — what the US-first route cannot represent.
10. **Marginal information gain** — what remains after Sephora or the chosen
    primary is already captured.

Review count and review velocity may support ranking within a surface, but do
not convert them into sales or market share without a separately justified
calibration model. A high review count is evidence of review activity, not a
unit-sales meter.

## Method

### 1. Current Route-Maturity Inventory

Build a receipt-backed inventory of current Forseti support. Separate:

- capture profile exists;
- grid route observed, with projection completeness and storefront admission kept separate;
- PDP route observed;
- market/storefront pin proven;
- structured review route proven;
- review-record depth and explicit losses;
- Q&A available;
- current public route rechecked;
- implementation-ready, recon-only, blocked, or unsupported.

Never turn a profile name into proof of current end-to-end capture.

### 2. Fresh External Research

Because retailer facts are volatile, use current web research. Prefer:

1. official retailer pages, policies, media kits, filings, and first-party
   statements for positioning, scale, membership, seller model, and services;
2. direct public brand grids, PDPs, review modules, and public APIs or structured
   responses reached without gate defeat;
3. credible consumer-panel or industry research for cross-shopping or channel
   use, with date, geography, denominator, and access limitations;
4. high-quality reporting for retailer avoidance, trust, boycott, access, or
   controversy signals, always separated from retailer-surface evidence.

Search results, traffic estimates, and retailer marketing language are leads,
not interchangeable measures of unique customers. Cite direct links and record
retrieval dates. If a paywalled panel headline lacks methods or denominators,
label it unusable for population coverage.

### 3. Overlap And Independence Analysis

For each representative company, compare candidate retailers using canonical
owned product/franchise identities. At minimum calculate or explicitly assess:

- owned-to-retailer assortment recall within the observed case;
- retailer-pair assortment overlap and unique listings;
- unique metadata fields or materially different values;
- review provider overlap, syndication markers, duplicate IDs/text/dates where
  observable, and review-count agreement or divergence;
- unique purchase-context evidence;
- route cost and failure risk.

Use empirical counts for the sampled cases, but do not extrapolate them to the
US customer population. Normalize at franchise/product level before SKU-level
comparison so shade, size, bundle, or URL proliferation does not fake coverage.

### 4. Smallest-Set Decision

Treat the problem as constrained set cover plus marginal information gain, not
as a popularity ranking. Produce:

- the nondominated retailer capability sets of sizes 2, 3, and 4;
- the evidence jobs and representative cases each set covers or misses;
- the incremental value and recurring route cost of each added retailer;
- sensitivity under at least three defensible priority regimes: portfolio and
  metadata depth; customer-evidence depth; purchase-context diversity;
- a recommendation for the smallest complete platform set;
- an explicit statement if no 3–4 retailer set is defensibly complete.

Do not hide judgment inside a single composite score. If weights are used, show
them, justify them, and demonstrate whether the recommendation changes under
reasonable alternatives.

### 5. Per-Company Activation Rule

Derive a rule consistent with portfolio-first Understanding:

1. reconstruct owned portfolio/franchise architecture;
2. select one authorized primary retailer for the strongest whole-company
   assortment and customer-evidence surface;
3. add one contrast retailer only for a named non-duplicative job;
4. add a third only to resolve a material remaining contradiction or blind spot;
5. otherwise stop.

Specify selection triggers and stop rules. A platform may support four retailers
while a normal company run uses only one or two.

### 6. Retailer Avoidance Blind Spot

Answer, without pretending retailer data can solve it, how Forseti should detect
material groups or contexts excluded by the chosen retailer set. Define the
smallest bounded **non-retailer** complement—such as independent community,
search-interest, consumer-panel, or current news/controversy evidence—needed to
flag avoidance, access, boycott, trust, or non-purchaser blind spots.

Do not count that complement as another retailer. Do not commission its capture
or implementation here. State what it can and cannot prove.

## Failure Visibility

For every attempted retailer/case surface, use one of:

- `OBSERVED_CURRENT`
- `OBSERVED_HISTORICAL_RECHECK_REQUIRED`
- `LISTING_ABSENT`
- `SURFACE_NOT_EXPOSED`
- `MARKET_PIN_UNVERIFIED`
- `ROUTE_BLOCKED`
- `ROUTE_UNSUPPORTED`
- `REVIEW_CORPUS_SYNDICATED_OR_NONINDEPENDENT`
- `NOT_APPLICABLE`

When an existing proven route fails during this study, make one bounded recovery
attempt allowed by its current contract. If it still fails, flag the failure and
its effect on the recommendation. Do not silently substitute search snippets,
a different market, cached claims, or an unproven route. Do not report a required
surface as acquired merely because the retailer is known to expose it.

If an unblocked owner action could recover a load-bearing required route, issue
one consolidated escalation. Otherwise continue only where the remaining
observations can still support an explicitly lower-confidence comparison.

## Required Output

Write exactly one new report:

`docs/research/forseti_beauty_minimum_complete_retailer_corpus_research_v0.md`

It must contain:

1. retrieval header and research receipt;
2. load outcome, exact repository revision/blobs, source-context status, and
   fresh-web retrieval window;
3. executive answer to the bound question;
4. terminology and population-claim boundary;
5. representative-case design and bias statement;
6. current Forseti retailer route-maturity matrix;
7. retailer archetype and evidence-job matrix;
8. observed assortment-overlap and unique-listing analysis;
9. review-provider, syndication, and independence matrix;
10. retailer-pair marginal-information analysis;
11. nondominated 2-, 3-, and 4-retailer capability sets;
12. recommended smallest platform capability set, with each member's unique job;
13. per-company primary/contrast/exception activation rule and stop conditions;
14. explicit Amazon adjudication;
15. rejected or conditional retailers and the reversal condition for each;
16. retailer-avoidance blind spot and smallest non-retailer complement;
17. route failures, missing evidence, confidence by conclusion, and material
    uncertainties;
18. implementation-priority recommendation stated as planning input only; and
19. source ledger with URL/path, publisher, date, retrieval date, geography,
    denominator where relevant, evidence job, and claim supported.

Include a concise final decision record:

```yaml
retailer_corpus_decision:
  market: US beauty retail
  platform_capability_set: []
  capability_count: null
  each_retailers_unique_job: {}
  normal_per_company_runtime_count: null
  primary_selection_rule: null
  contrast_retailer_trigger: null
  third_retailer_exception_trigger: null
  amazon_status: core | conditional | reject | unresolved
  avoidance_complement: null
  confidence: high | medium | low
  decisive_gaps: []
  implementation_authorized: false
```

## Drift Guard

Do not:

- implement, patch, or enable capture profiles, adapters, APIs, runners, or data-lake schemas;
- perform volume capture, bulk scraping, login, CAPTCHA solving, proxy rotation,
  gate defeat, paid-data purchase, outreach, or account creation;
- build a universal retailer ontology, standing retailer registry, scheduler,
  monitoring system, or customer identity graph;
- deduplicate people across retailers or imply that public review identities
  permit population-level customer deduplication;
- redesign the full Understanding cycle, CSB doctrine, franchise-selection
  logic, or downstream product strategy;
- recommend attacks, whitespace moves, economics, supply-chain actions, or GTM;
- estimate sales from review volume as though review-to-sale ratios were known;
- expand into international markets except to name a material transfer risk;
- edit existing research reports, prompts, source contracts, profiles, or code;
- commit, push, open/update a PR, merge, stash, reset, clean, or run repo hygiene.

If the research reveals an adjacent need, record it as a bounded follow-up and
continue only the Active Objective above.

## Acceptance Bar

The report is acceptable only if:

- it answers both platform capability and per-company runtime questions;
- it tests rather than presupposes the 3–4 retailer hypothesis;
- every recommended retailer has a distinct, evidenced job;
- redundancy includes assortment, metadata, review-provider, and review-content
  overlap rather than retailer-name diversity alone;
- route maturity and data richness are not conflated;
- Amazon is explicitly adjudicated;
- no population/customer-reach claim exceeds its data and denominator;
- large review counts are bounded by selection and missingness;
- proven-route failures remain visible;
- the avoidance blind spot is separated from the retailer corpus;
- the answer includes stop rules that prevent capturing all supported retailers
  for every company; and
- sources are current, directly linked, and tied to claims.

## Validation And Closeout

After writing the report, run in order:

```powershell
git diff --check
python .agents\hooks\check_prompt_output_mode.py --strict
python .agents\hooks\check_retrieval_header.py --changed
python .agents\hooks\check_repo_map_freshness.py --changed
python .agents\hooks\check_map_links.py --strict
python .agents\hooks\check_placement.py --check
git status --short
```

If any focused gate fails, stop and report the exact failure; do not continue to
broader validation. Fresh-read the written report and status before claiming it
exists or is the only change.

## Completion Status

End the report with exactly one:

- `RESEARCH_COMPLETE_DECISION_READY`
- `RESEARCH_COMPLETE_WITH_MATERIAL_GAPS`
- `RESEARCH_BLOCKED`

These statuses describe the research report only. They do not authorize capture
implementation, data-lake investment, or a production/readiness claim.