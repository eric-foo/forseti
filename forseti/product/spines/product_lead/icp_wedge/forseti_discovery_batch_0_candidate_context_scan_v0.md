  Forseti Discovery Batch 0 Candidate-Context Scan v0

> **SUPERSEDED / OFF-TARGET (2026-06-08)**
> This scan was conducted against developer-tool / developer-platform candidates
> (Sentry, Clerk, Vercel, Supabase, Neon, PostHog, Pinecone, Algolia) as the
> first discovery lane. That framing is off-target under the current wedge.
> The first-proof beachhead is now the **AI-monetization slice** — B2B SaaS
> making a first-time AI-monetization or competitor-triggered repricing/
> repackaging decision, where the competitor-pricing substrate is publicly rich
> and the firm is flying blind — with developer-facing SaaS as a strong
> sub-instance only, not the defining qualifier. The wedge frame is
> cross-sector-open. Authoritative direction:
> `docs/decisions/forseti_icp_wedge_pricing_first_v0.md`.
> Retain this scan as historical record; do not use it to drive first-proof
> candidate qualification without re-screening against the AI-monetization
> beachhead criteria.

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Discovery Batch 0 candidate-context scan for possible later Forseti Product Proof Lead qualification.
use_when:
  - Reviewing lightweight public candidate-context evidence before manual qualification prep.
  - Selecting 2-3 candidate contexts for a later owner-authorized qualification step.
  - Checking Discovery Batch 0 non-claims and no-outreach boundaries.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/product-proof.md
  - .agents/workflow-overlay/validation-gates.md
  - forseti/product/spines/product_lead/icp_wedge/forseti_discovery_batch_0_target_selection_brief_v0.md
```

   Scope

This artifact is a narrow candidate-context scan only.

It does not authorize outreach, contact collection, person-level dossiers, CRM construction, memo production, executive deck production, product or feature planning, implementation planning, software, automation, source systems, dashboards, source maps, data-spine design, commits, pushes, PRs, product readiness claims, or commercial readiness claims.

Candidate companies are not buyers (Buyer). They are possible real-world decision contexts that may or may not qualify later. Trust posture is `unknown` throughout because no buyer has been contacted.

Language boundary: this scan avoids treating any company as a client, lead, prospect, customer, account, or sales opportunity.

Scan counters:

| Counter | Result |
| --- | --- |
| Search queries used | 8 |
| Public pages opened | 18 |
| Usable evidence pages | 16 |
| Opened pages excluded from evidence | 2 PostHog docs URLs returned internal errors |
| Candidate contexts identified | 8 |
| No-go / deferred candidates | 4 |

   Source Ledger

| Source URL | Source type | Why opened | Candidate/context supported |
| --- | --- | --- | --- |
| https://vercel.com/pricing | Official pricing page | Checked current plan structure, AI Cloud surface, compute usage, and spend-control signals. | Vercel compute and AI Cloud packaging |
| https://vercel.com/docs/pricing | Official docs page | Checked billable metrics and pricing model documentation. | Vercel usage-based pricing and plan thresholds |
| https://supabase.com/pricing | Official pricing page | Checked plan tiers, usage allowances, overage surfaces, and enterprise packaging. | Supabase platform pricing |
| https://supabase.com/docs/guides/platform/billing-on-supabase | Official docs page | Checked organization-based billing, variable usage fees, quotas, and compute-cost framing. | Supabase billing and packaging |
| https://neon.com/pricing | Official pricing page | Checked usage-based compute/storage pricing, autoscaling, Auth MAU threshold, and cost-control framing. | Neon serverless Postgres packaging |
| https://neon.com/docs/introduction/plans | Official docs page | Checked plan limits, egress, usage metrics, branches, and restore billing. | Neon usage limits and billing surfaces |
| https://www.pinecone.io/pricing/ | Official pricing page | Checked plan tiers and read/write/storage unit pricing dimensions. | Pinecone vector database pricing |
| https://docs.pinecone.io/guides/manage-cost/understanding-cost | Official docs page | Checked serverless cost metrics, read units, write units, and storage mechanics. | Pinecone API usage monetization |
| https://sentry.io/pricing/ | Official pricing page | Checked telemetry quotas, pay-as-you-go rates, and Seer presence in pricing calculator. | Sentry usage-based observability pricing |
| https://docs.sentry.io/pricing/ | Official docs page | Checked Seer pricing, active-contributor metric, and January 2026 legacy-pricing transition. | Sentry AI debugging add-on monetization |
| https://sentry.zendesk.com/hc/en-us/articles/45551407771931-What-is-the-pricing-for-Seer-January-21-2026 | Official help-center page | Checked Seer pricing update and active-contributor billing explanation. | Sentry Seer packaging |
| https://posthog.com/pricing | Official pricing page | Checked usage-based pricing, product-level billing limits, event pricing, and free tier. | PostHog usage-based analytics packaging |
| https://clerk.com/pricing | Official pricing page | Checked MRU pricing, B2B Authentication add-on, Billing add-on, seats, and enterprise tiering. | Clerk auth and billing packaging |
| https://clerk.com/docs/guides/billing/overview | Official docs page | Checked Billing beta status, B2C/B2B billing models, and support limitations. | Clerk Billing beta context |
| https://www.algolia.com/pricing | Official pricing page | Checked request/record overages, AI-capability tiers, Elevate annual plan, and usage FAQ. | Algolia AI Search pricing |
| https://www.algolia.com/doc/guides/scaling/algolia-service-limits | Official docs page | Checked plan limits, indexing, API, connector, and generative-experience limits. | Algolia limits and API surface |

Opened but not used as evidence:

| Source URL | Result |
| --- | --- |
| https://posthog.com/docs/billing/pricing-and-billing | Internal error in page open |
| https://posthog.com/docs/billing | Internal error in page open |

   Candidate Context Table

| Company | Category | Suspected decision family (DecisionEvent) | Visible signal | Suspected trigger | Likely decision-owner role type | Public-signal surface to verify | Trust posture | Qualification status | Why it may be worth later intake | Why it may fail qualification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Vercel | platform | pricing, packaging, API | Pricing and docs expose Fluid compute, AI Cloud, many billable metrics, usage calculation, and spend-control mechanisms. | Compute and AI workload packaging, Pro-to-Enterprise thresholds, cost predictability for developer teams. | Platform GM, product monetization owner, pricing owner, enterprise packaging owner. | Pricing/docs changes, changelog, developer reactions to compute costs, plan limits, and spend controls. | unknown | candidate_context_only | Public developer signals may be strong enough to test whether a manual public-signal decision artifact can reduce allocation risk around compute and AI packaging. | May be too large, too noisy, already decided, or dependent on private usage and enterprise contract data. |
| Sentry | mixed | pricing, packaging, monetization | Pricing shows telemetry quotas and pay-as-you-go rates; Seer docs show a January 2026 AI add-on model using active contributors. | AI debugging monetization, contributor-based pricing, legacy add-on transition, bundle versus add-on packaging. | AI product owner, monetization owner, observability platform PM, pricing owner. | Pricing docs, help-center updates, developer reactions to Seer, AI code review, and telemetry overage behavior. | unknown | candidate_context_only | Fresh AI add-on pricing creates a concrete public decision surface with role-based usage mechanics and likely public reaction. | May fail if Seer pricing is already locked, if internal adoption data dominates, or if public signals cannot affect the decision. |
| Clerk | platform, API | pricing, packaging, API, monetization | Pricing exposes MRU-based plans, B2B Authentication add-on, Billing add-on, seat limits, and enterprise tiering; Billing docs mark APIs as beta/experimental. | B2B auth and billing packaging, organization usage monetization, seat and usage billing expansion. | B2B product owner, Billing product owner, pricing owner, developer-platform GM. | Pricing page, billing docs, changelog, developer feedback on beta billing, MRU/MRO pricing, and seat models. | unknown | candidate_context_only | Billing beta plus B2B add-ons make the decision context narrower and plausibly live enough for manual qualification prep. | May require private Stripe, usage, or beta-roadmap data before public evidence can matter. |
| Supabase | platform, API | pricing, packaging | Pricing and billing docs show Free/Pro/Team/Enterprise plans, organization-based billing, quotas, overages, and project compute charged separately. | Quota and compute packaging, project/organization billing, overage anxiety, Team and Enterprise packaging. | Platform product owner, billing product owner, pricing owner, developer experience owner. | Pricing/docs, developer community discussion around quotas, project limits, compute costs, and cost controls. | unknown | candidate_context_only | Strong public developer surface and transparent billing mechanics may support later qualification around packaging and usage predictability. | May be too broad without a specific 30-90 day decision, or may require internal usage and support-ticket data. |
| Neon | data-product, platform | pricing, packaging, monetization | Pricing/docs show usage-based compute and storage, autoscaling cost ceilings, egress limits, branch billing, restore billing, and Auth MAU threshold. | Serverless Postgres cost predictability, Auth monetization, Launch/Scale packaging, usage-limit communication. | Database product owner, pricing owner, platform GM, developer experience owner. | Pricing/docs, developer discussion on compute autoscaling, egress, branches, Auth limits, and serverless database comparisons. | unknown | candidate_context_only | Public docs map directly to cost predictability and package-boundary questions that a decision owner might test later. | May fail if no live packaging decision exists or if technical workload telemetry is required to evaluate options. |
| PostHog | B2B SaaS, data-product | pricing, packaging, monetization | Pricing page presents transparent usage-based pricing, product-level billing limits, event-level rates, and broad free-tier allowances. | Product-suite packaging, free-tier/overage economics, event-type pricing, usage-limit confidence. | Product analytics GM, pricing owner, growth/product owner, data platform owner. | Pricing page, changelog, public developer discussion around event billing, free tier limits, and product-suite breadth. | unknown | candidate_context_only | Transparent usage pricing and billing-limit messaging create a plausible context for testing public-signal evidence around pricing trust. | May fail if context becomes generic analytics market research or if PostHog's public pricing philosophy makes the decision non-live. |
| Pinecone | API, data-product | API, pricing, packaging | Pricing and docs show serverless read units, write units, storage, plan tiers, and Dedicated Read Nodes for certain workloads. | AI/vector workload monetization, read/write unit packaging, Standard versus Enterprise boundaries, cost predictability. | Vector database product owner, API monetization owner, pricing owner, AI infrastructure GM. | Pricing/docs, developer feedback on read/write unit bills, workload sizing, cloud marketplace, and vector database alternatives. | unknown | candidate_context_only | AI retrieval workloads have visible public cost mechanics where public developer evidence might matter. | May require private workload telemetry, benchmark data, or enterprise capacity planning rather than public-signal evidence. |
| Algolia | API, data-product | pricing, API, monetization | Pricing shows requests/records overages, Grow Plus AI features, Elevate annual AI Search, and docs expose many plan and API limits. | AI Search tiering, record/request overage design, annual-contract thresholds, connector and generative-experience limits. | Search product owner, AI Search GM, pricing owner, platform API owner. | Pricing/docs, developer docs, public reaction to AI Search limits, overages, and connector/API constraints. | unknown | candidate_context_only | Rich pricing and limit surfaces could support a focused later intake around AI Search packaging. | May be too enterprise-contract-heavy or too dependent on private renewal and usage data for first intake. |

   Ranking

Top 2-3 for first manual qualification prep:

1. Sentry Seer pricing and AI debugging add-on packaging.
2. Clerk Billing / B2B Authentication packaging.
3. Vercel Fluid compute / AI Cloud usage packaging.

Middle:

- Supabase organization-based billing, usage quotas, and compute packaging.
- Neon usage-based serverless Postgres packaging and Auth monetization.
- PostHog usage-based product-suite pricing and billing-limit messaging.

Weak / defer:

- Pinecone read/write/storage unit monetization.
- Algolia AI Search requests/records overage and enterprise-tier packaging.

   No-Go Notes

| Candidate considered | Status | Reason |
| --- | --- | --- |
| OpenAI / Anthropic model API pricing | defer | Plausible API pricing pressure, but likely too broad and prone to generic market research for this narrow batch. Not opened to preserve scan caps. |
| Cursor / AI coding subscription limits | no-go for this batch | Strong public plan-limit discussion, but mixed individual and team subscription context risks drifting away from B2B SaaS/API decision qualification. Not opened to preserve scan caps. |
| Datadog / New Relic observability packaging | defer | Visible pricing complexity, but likely enterprise-contract-heavy and may require private renewal data before public-signal evidence matters. Not opened to preserve scan caps. |
| Netlify | defer | Adjacent developer-platform context, but Vercel produced a stronger visible compute/AI packaging surface under the page cap. Not opened to preserve scan caps. |

Excluded / deferred count: 4.

   Recommended Next Step

Owner selects 2-3 contexts for manual qualification prep. Recommended selection:

1. Sentry Seer pricing and AI debugging add-on packaging.
2. Clerk Billing / B2B Authentication packaging.
3. Vercel Fluid compute / AI Cloud usage packaging.

Selection should only prepare manual qualification questions. It should not perform outreach, collect person-level details, produce a memo, produce an executive deck, or imply Orca readiness.

   Blockers

Before outreach:

- Outreach has not been explicitly authorized.
- No candidate context has been owner-selected for qualification prep.
- No specific organization-side decision owner or budget-accountable decision lead has been confirmed.
- No first-contact script has been authorized for live use.
- No consent or expectation boundary has been established for any conversation.

Before decision artifact production:

- No named qualified buyer exists.
- No named decision owner or budget-accountable decision lead has been confirmed.
- No live 30-90 day pricing, packaging, API, or monetization decision has been qualified.
- No memo question, timing, stakes, or allocation consequence has been confirmed.
- No public-signal trust posture has been classified as `trust_open` or `trust_objection`.
- No public-signal surface has been verified for a specific qualified decision.
- No decision-artifact readback agreement exists.
- No executive deck use tied to internal decision circulation has been established.

   Non-Claims

This scan does not claim:

- buyer validation;
- willingness-to-pay proof;
- repeatability proof;
- product readiness;
- feature readiness;
- implementation readiness;
- commercial readiness;
- Core Spine v0 validation;
- client/prospect relationship established;
- outreach occurred;
- a buyer was contacted;
- a decision owner was qualified;
- a memo was produced;
- an executive deck was produced;
- memo or deck usefulness;
- buyer pull;
- paid-decision-sprint-level pull.
