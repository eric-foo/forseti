# Forseti Company-Intelligence Information Architecture v0

```yaml
retrieval_header_version: 1
artifact_role: Decision record (company-intelligence information architecture)
scope: >
  Owner-adjudicated architecture for deciding which company information Forseti
  should seek, how evidence access and directness affect that choice, how
  decision-neutral company facts relate to decision-specific modules, and what
  may later enter Company Surface.
use_when:
  - Designing a one-company research or competitive-intelligence commission.
  - Deciding whether a public, paid, or customer-authorized fact is worth acquiring.
  - Separating reusable company facts from decision-specific analysis, GTM, and monitoring.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_product_thesis_decision_adjudication_v0.md
  - forseti/product/satellites/beauty/beauty_decision_adjudication_product_profile_v0.md
  - forseti/product/information/company_surface/README.md
  - forseti/product/spines/commission_signal_board/README.md
stale_if:
  - The owner changes decision adjudication as the product center.
  - Company Surface takes ownership of decision-specific analysis or recommendations.
  - Forseti adopts a materially different evidence-access or rights posture.
```

## Status And Decision

`OWNER_ACCEPTED_INFORMATION_ARCHITECTURE_V0`

The owner accepted the architecture in conversation on 2026-07-16 with these
corrections:

- start from the decision and determine the information needed to make it;
- do not start from a generic report, a proprietary-data category, or a
  monitoring product;
- treat lawfully available open or paid web information as potentially
  acquirable, with purchase effort governed by how badly the decision needs the
  fact;
- use the **smallest complete** evidence world, not a universal minimum report;
- keep compound concepts split into the precise underlying facts that can
  actually be observed or inferred; and
- keep the architecture compatible with later Company Surface import without
  making Company Surface a dependency of the first proving work.

This record controls the information-requirements architecture. It does not
select the first buyer, company, beauty decision, commercial offer, or proving
case.

## Plain-Language Model

Forseti should not ask, "What information can we collect about this company?"
It should ask:

> What decision must be made, which facts could change that decision, and what
> is the strongest evidence we can lawfully obtain for each fact?

That produces this flow:

```text
named decision, owner, action, consequence, and deadline
-> claims and unknowns that could change the action
-> atomic facts needed to resolve them
-> strongest lawful evidence route for each fact
-> observed facts, explicit proxies, conflicts, and missingness
-> decision-specific analysis module
-> act, probe, sequence, hold, or avoid
```

A company report may be a useful factual view, but it is not the product center
and does not determine what matters. The decision determines what matters.

## The Core Distinctions

### 1. Information is not a source

`Customer repeat purchase`, `retailer sell-through`, `product complaints`, and
`claim substantiation` are information. Reddit, Sephora, an earnings
transcript, a paid database, and an internal sales table are sources that may
contain evidence about that information.

A source family must never be treated as though it were the fact itself.

### 2. Access is not evidence strength

A paid source may contain direct, decisive evidence or weak, duplicated
commentary. An open source may contain a direct company admission or only a
noisy proxy. Payment status therefore does not determine importance or truth.

Every required fact is assessed on four separate axes:

| Axis | Question | Working values |
| --- | --- | --- |
| Decision criticality | Could this fact change the action, action size, timing, or hold state? | controlling, material, supporting, descriptive |
| Evidence directness | How directly does the evidence establish the fact? | direct measurement, direct observation, proxy, inference |
| Access class | How can Forseti lawfully obtain it? | open web, paid/entitled web, customer-authorized internal, unavailable/prohibited |
| Rights state | What may Forseti do with what it obtains? | inspect, derive, preserve, quote, share, redistribute — each source-specific |

These axes must remain independent. In particular:

- `paid` does not mean `strong`;
- `publicly reachable` does not mean `complete`;
- `available on the web` does not automatically grant preservation,
  quotation, sharing, or redistribution rights; and
- `unavailable` does not authorize replacing a decisive fact with a proxy.

### 3. Three meanings of non-open information

The word `private` is too imprecise for this architecture. Use:

1. **Paid or entitled web evidence** — available through a lawful subscription,
   membership, purchase, or licensed interface. This is eligible evidence.
2. **Customer-authorized internal evidence** — supplied or connected by the
   company under an explicit permission boundary.
3. **Unavailable or prohibited evidence** — not lawfully obtainable for the
   commission. If it controls the action, Forseti holds.

### 4. Consequence is not predictive proof

Evidence that an outcome was economically serious proves stakes. It does not
prove that an earlier public clue reliably predicted the outcome or would have
changed the decision.

This distinction prevents hindsight from being presented as intelligence.

## Smallest Complete Evidence World

There is no universal minimum company report and no fixed ranking of company
data that applies to every decision.

For a named decision, the **smallest complete evidence world** contains every
fact and evidence family necessary to:

- support the strongest defensible action;
- expose a counter-case that could reverse or materially resize that action;
- identify a decisive missing input;
- distinguish direct evidence from proxy and inference; and
- leave a truthful hold when the decision cannot be defended.

It excludes material that merely makes the report feel comprehensive.

`Smallest` controls irrelevant breadth. `Complete` prevents an under-researched
answer. A smallest-complete evidence world may still be large when the decision
is consequential or the evidence is conflicted.

## Architecture Layers

### Layer 1 — Decision frame

Bind:

- accountable decision owner or faithful proxy;
- action and available alternatives;
- consequence of error or delay;
- deadline and evidence cutoff;
- allowed recommendation verbs;
- known constraints;
- decisive-private-context boundary; and
- later reveal or outcome path.

No research commission should invent this frame from source availability.

### Layer 2 — Information-requirements register

Translate the decision into atomic facts. Each required fact records:

| Field | Purpose |
| --- | --- |
| `fact_id` | Stable identifier inside the commission |
| `underlying_fact` | The exact thing that must be known |
| `decision_use` | Which action, threshold, or uncertainty it may change |
| `criticality` | Controlling, material, supporting, or descriptive |
| `preferred_measurement` | What direct evidence would look like |
| `acceptable_proxy` | Explicit fallback, if one can validly inform the decision |
| `proxy_ceiling` | What the proxy cannot establish |
| `comparison_or_baseline` | Required denominator, cohort, competitor, or prior state |
| `time_requirement` | Effective period, cutoff, and freshness need |
| `counterevidence_needed` | What would challenge the leading interpretation |
| `access_options` | Open, paid/entitled, authorized internal, or unavailable |
| `rights_requirement` | Inspect, preserve, quote, share, or redistribute need |
| `missing_behavior` | Proceed, narrow, probe, or hold when absent |
| `refresh_eligibility` | Whether later change in this fact can affect a recurring decision |

Compound labels such as `demand durability`, `channel health`, or `execution
capacity` are module names, not acceptable facts. They must be decomposed.

For example, `demand durability` might require separate facts about:

- repeat purchase by a defined cohort;
- reorder interval;
- new-versus-returning customer mix;
- dependence on one launch, creator, discount, retailer, or geography;
- return or complaint reasons;
- search, review, community, or resale persistence; and
- the period and denominator behind every measure.

### Layer 3 — Evidence acquisition

Choose sources after the facts are named.

Open and paid web sources are both eligible. The decision to buy access should
be based on:

1. how critical the fact is;
2. how much stronger or more direct the paid evidence is than available
   alternatives;
3. whether it can change the action or prevent a false hold;
4. cost and acquisition latency relative to the decision deadline; and
5. whether the source's terms permit the required inspection, derivation,
   preservation, quotation, and delivery.

The practical rule is:

> Pay for access when the expected decision value of the stronger fact exceeds
> the cost, delay, and rights limitation of obtaining it.

Membership willingness removes a commercial preference against paywalls. It
does not remove source-specific legal, contractual, technical, or evidentiary
limits.

CSB may specify the information requirements and source-family coverage.
Scanning discovers valuable venues, exact queries, hidden sources, negatives,
and access walls. Capture owns lawful acquisition and preservation routes.
Downstream evidence owners preserve provenance, transformations, conflicts,
and limitations.

### Layer 4 — Observation and derivation

Every material result must separate:

- the raw or preserved evidence;
- the directly observed fact;
- any derived measure and its method;
- any proxy relationship;
- analyst inference;
- counterevidence;
- observed, published, and effective dates;
- coverage and access limitations; and
- the strongest claim the evidence may support.

A proxy must never be stored or presented as the underlying fact. For example,
review volume is not sell-through; community excitement is not repeat purchase;
job postings are not execution capacity; and an impairment is not proof that a
particular public early-warning signal worked.

### Layer 5 — Decision modules

Decision modules are reusable analytical assemblies. They are activated only
when the decision requires them, and each module must resolve into atomic facts.

Candidate modules include:

| Module | Example decisions it may inform | Illustrative atomic facts |
| --- | --- | --- |
| Customer choice and product failure | concept, positioning, claims, reformulation | stated alternatives, switching reason, use context, failure mode, complaint incidence, repeat behavior |
| Demand durability | launch, inventory, investment, competitive response | cohort repeat, reorder interval, concentration, promotion dependence, persistence |
| Retail and channel productivity | retailer entry, expansion, exit, allocation | productive doors/SKUs, sell-through, replenishment, returns, markdowns, margin and terms |
| Claims and substantiation | claim launch, packaging, regulatory response | exact claim version, evidence standard, test basis, complaint or challenge, jurisdiction |
| Launch and inventory | launch intervention, buy depth, replenishment | forecast, orders, stock, stockout duration, replenishment, cancellations, returns |
| Competitive response | price, positioning, launch timing, assortment | competitor action, affected segment, substitution, price umbrella, channel overlap |
| Execution and supply resilience | scale, delay, supplier change, contingency | capacity, lead time, defect rate, concentration, role ownership, contingency |
| Deal, financial, and concentration | acquisition, partnership, capital allocation | revenue/margin bridge, customer/channel concentration, cash need, liabilities, impairment |
| Regulatory and safety response | hold, recall, reformulate, communicate | adverse event, affected lot/version, severity, reporting duty, corrective action |

This is a candidate vocabulary, not a required checklist and not a ranking.

### Layer 6 — Decision artifact

The output follows the current Forseti product contract:

- decision and evidence-world frame;
- recommendation or explicit hold;
- strongest evidence and counter-case;
- uncertainty and action ceiling;
- decisive missing inputs;
- reversal conditions;
- inspectable evidence appendix; and
- later reveal or outcome plan.

A generic company dossier that stops at description is incomplete for a
Decision Sprint, even if its facts remain useful as substrate.

## Common Company Substrate

A decision-neutral one-company report can reduce repeated reconstruction. Its
common substrate should be limited to reusable observed company reality:

- Brand/Org identity and ownership state;
- product, SKU, variant, formula, package, and claim versions;
- price, promotion, availability, and assortment states;
- channel and distribution footprint;
- launches, discontinuations, partnerships, and official commitments;
- leadership, hiring, role ownership, and organizational changes;
- material regulatory, litigation, safety, and corporate events; and
- provenance, timing, conflicts, missingness, and coverage limitations.

This substrate is not a complete account of the company. It is the reusable
factual layer from which decision-specific requirements may start.

The current CSB one-company competitive-intelligence profile may produce this
decision-neutral substrate. It must not be mistaken for the later
decision-specific adjudication run.

## Company Surface Boundary

Company Surface is not required for the first proving run. This architecture is
storage-neutral and authorizes no Company Surface implementation or mutation.

When a later import is authorized, suitable Company Surface candidates include:

- canonical company, Brand, product, SKU, claim, channel, and event identities;
- dated factual observations and measured values;
- source and provenance links;
- explicit limitations, missingness, conflicts, corrections, and identity
  uncertainty;
- history and effective-time relationships; and
- an explicit relation stating that one observation is a proxy for another
  fact, without promoting the proxy into that fact.

These remain outside Company Surface:

- the current buyer or Decision Frame;
- research-run priority and access-purchase choice;
- pain, urgency, ICP, wedge, outreach, or GTM hypotheses;
- analyst interpretations and confidence;
- recommendation, action ceiling, and reversal conditions; and
- proof or willingness-to-pay conclusions.

Physical records continue to belong to Data Lake-owned storage. Company Surface
owns shared company meaning and history, not the raw packets or downstream
decision.

## Monitoring Eligibility

Forseti should not monitor a source merely because it is capturable or might be
interesting.

A variable becomes eligible for longitudinal refresh only when all of these are
named:

1. the atomic fact;
2. the decision it can change;
3. the baseline or prior state;
4. the material-change threshold or qualitative trigger;
5. the required cadence relative to the decision window;
6. the acquisition and rights route; and
7. what action follows from a meaningful change.

Longitudinal evidence may be needed in a point-in-time Decision Sprint.
Production monitoring is a later delivery mechanism, not the reason a fact is
important.

## Evidence Examples

### e.l.f. Bronzing Drops — direct evidence of input use

The e.l.f. example is useful because company leadership reportedly identified
Bronzing Drops as its most requested community product and the launch explicitly
positioned a $12 item against a $38 prestige inspiration.

That supports a bounded claim:

> Customer requests and an observed prestige price umbrella entered an actual
> product and positioning decision.

It does not by itself prove the product succeeded because of those inputs, that
the request represented the whole market, or that the same method transfers to
another company.

Sources to re-verify before strict use:

- [e.l.f. earnings transcript mirror](https://fintool.com/app/research/companies/ELF/documents/transcripts/q1-2025)
- [e.l.f. product announcement](https://investor.elfbeauty.com/stock-and-financial/press-releases/landing-news/2024/06-10-2024-050119999)

### Drunk Elephant impairment — direct evidence of consequence, not prediction

Shiseido's reported ¥46.8 billion impairment establishes that Drunk Elephant's
deterioration had serious economic consequences.

It does not establish that an earlier public `cohort drift` proxy:

- was observable before the deterioration became obvious;
- measured actual customer retention or repeat purchase;
- would have crossed a predeclared action threshold;
- would have caused a decision owner to act; or
- would have prevented or reduced the impairment.

To test that stronger proposition, Forseti would need a sealed backtest:
predeclare the decision and cutoff, use only evidence available by the cutoff,
state the action before reveal, and compare it with the later outcome.

Source to re-verify before strict use:

- [Shiseido 2025 results](https://corp.shiseido.com/en/ir/pdf/ir20260210_244.pdf)

In short: e.l.f. says, "we used this input to make a product decision."
Shiseido says, "the eventual outcome was costly." The latter does not prove
which earlier signal would have warned correctly.

## First Proving-Run Requirement

The next lane should not commission another broad company report immediately.
It should first choose one beauty decision family and bind:

- the company and faithful decision-owner proxy;
- action, alternatives, consequence, deadline, and cutoff;
- atomic facts most likely to control or materially change the action;
- which facts are expected on open web, paid web, authorized internal data, or
  unavailable;
- which proxies are admissible and their ceilings;
- the smallest-complete evidence world;
- the sealed backtest or later reveal path; and
- the hold condition.

Only then should it commission the Research Engine.

## Success Signals

This architecture is functioning when:

1. A cold agent can derive a smallest-complete evidence plan from a named
   decision without using a generic company-report checklist.
2. The agent can explain exactly why each requested fact may change the action.
3. Paid access is purchased because a critical fact justifies it, not because
   paid data is presumed superior.
4. Sources, facts, proxies, and inferences remain visibly separate.
5. Missing decisive evidence produces a hold rather than a generic hypothesis.
6. Reusable factual outputs can later be imported into Company Surface without
   importing GTM or decision judgment.
7. Longitudinal refresh is attached only to variables with a named decision
   trigger and action.

## Explicit Non-Claims

This record is:

- not selection of a buyer, company, first decision family, offer, price, or GTM
  route;
- not a universal company-data ranking or mandatory report schema;
- not proof that any named source is currently accessible, complete, licensed,
  or decision-sufficient;
- not proof that the e.l.f. inputs caused success or that public cohort proxies
  predicted the Drunk Elephant impairment;
- not Company Surface, Data Lake, CSB, Scanning, Capture, Cleaning, or Judgment
  implementation authority;
- not authorization to buy access, acquire private data, contact companies, or
  redistribute source content;
- not production monitoring readiness; and
- not buyer proof, willingness-to-pay proof, or same-decision validation.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    One-company intelligence now uses a decision-first information architecture:
    atomic facts and their evidence routes are selected by the named decision,
    lawful paid web access is eligible but separately governed by criticality,
    directness, cost, latency, and rights, and reusable company facts remain
    separate from decision modules, GTM, recommendations, and monitoring.
  trigger: architecture_doctrine
  related_triggers:
    - product_doctrine
  controlling_sources_updated:
    - docs/decisions/forseti_company_intelligence_information_architecture_v0.md
    - docs/workflows/forseti_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/product-proof.md
    - docs/decisions/forseti_product_thesis_decision_adjudication_v0.md
    - forseti/product/satellites/beauty/beauty_decision_adjudication_product_profile_v0.md
    - forseti/product/spines/foundation/product_contract/core_spine_v0_product_contract.md
    - forseti/product/information/README.md
    - forseti/product/information/company_surface/README.md
    - forseti/product/information/company_surface/purpose_contract_v0.md
    - forseti/product/spines/commission_signal_board/README.md
    - forseti/product/spines/scanning/README.md
    - docs/workflows/forseti_research_engine_map_v0.md
  intentionally_not_updated:
    - path: forseti/product/information/company_surface/
      reason: >
        Its current decision-agnostic facts/history boundary is compatible.
        Import mechanics, schema changes, and runtime mutation are outside this
        work unit.
    - path: forseti/product/spines/commission_signal_board/
      reason: >
        The newly landed decision-neutral one-company profile remains a factual
        substrate. Binding decision-specific information modules belongs to the
        next proving commission, not a speculative CSB rewrite.
    - path: forseti/product/spines/scanning/ and Capture/Data Lake/Cleaning/Judgment owners
      reason: >
        Their discovery, acquisition, storage, transformation, and judgment
        boundaries remain unchanged.
    - path: GTM and buyer-proof surfaces
      reason: >
        This architecture explicitly does not select a buyer, wedge, offer, or
        commercial route.
  stale_language_search: >
    rg -n -i "generic company report|minimum company report|paid data.*superior|monitor.*because|source.*is.*fact"
    docs/decisions/forseti_company_intelligence_information_architecture_v0.md
    docs/workflows/forseti_repo_map_v0.md
  non_claims:
    - not validation or readiness
    - not source-access or purchase authorization
    - not Company Surface implementation
    - not buyer proof or willingness-to-pay proof
```
