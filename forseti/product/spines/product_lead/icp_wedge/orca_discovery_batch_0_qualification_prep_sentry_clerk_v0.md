# Orca Discovery Batch 0 Qualification Prep - Sentry Seer and Clerk v0

> **SUPERSEDED / OFF-TARGET (2026-06-08)**
> This prep predates the pricing-first re-scope. Sentry/Clerk-style developer-tool discovery prep is no longer the first-proof beachhead. The first-proof beachhead is now the AI-monetization slice (B2B SaaS making a first-time AI-monetization or competitor-triggered repricing/repackaging decision; developer-facing SaaS is a sub-instance, not the defining qualifier). Current authority: `docs/decisions/forseti_icp_wedge_pricing_first_v0.md`. The prior ICP wedge record (`docs/product/orca_product_lead_first_icp_wedge_decision_v0.md`) is superseded by that record. Content below is retained as history; do not use it as a live qualification instrument without re-reading `docs/decisions/forseti_icp_wedge_pricing_first_v0.md` first.

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Discovery Batch 0 qualification prep for two owner-selected candidate contexts: Sentry Seer and Clerk Billing / B2B Authentication.
use_when:
  - Preparing later owner-authorized qualification intake for the selected candidate contexts.
  - Checking whether Sentry Seer or Clerk should move from candidate context to manual qualification.
  - Preserving no-outreach, no-memo, no-deck, and non-client boundaries before Product Proof Lead discovery.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/product-proof.md
  - forseti/product/spines/product_lead/icp_wedge/orca_product_lead_first_icp_wedge_decision_v0.md
  - forseti/product/spines/product_lead/proof_charter/forseti_product_proof_lead_charter_v0.md
  - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md
  - forseti/product/spines/product_lead/icp_wedge/orca_discovery_batch_0_candidate_context_scan_v0.md
  - forseti/product/spines/product_lead/icp_wedge/orca_discovery_batch_0_target_selection_brief_v0.md
  - docs/prompts/product-planning/orca_product_proof_lead_customer_discovery_prompt_v0.md
input_hashes:
  - path: docs/product/orca_product_lead_first_icp_wedge_decision_v0.md
    sha256: B570672CD7F31B2D78F9DC5E851C3AEDA7030A56ECF2CDC6733E0191ED3DDC23
  - path: docs/product/orca_product_proof_lead_charter_v0.md
    sha256: 731E4349AA931613D393DFC64B05F410E098D40F86D1C26A11BD31A1E2852322
  - path: docs/product/orca_buyer_proof_packet_v0.md
    sha256: ECDCD4BFC626295D486189F063CA8429EA2F324BD71151C9D28A52683927A224
  - path: docs/product/orca_discovery_batch_0_candidate_context_scan_v0.md
    sha256: 52A7F5E823A31562EAFDAE389AB51188BCAA021BF3E6B4478F8045435684FE28
  - path: docs/product/orca_discovery_batch_0_target_selection_brief_v0.md
    sha256: 3F50789618E4DC9881A753CC57F786F6763B0A17891F498238E1A1331907856E
  - path: docs/prompts/product-planning/orca_product_proof_lead_customer_discovery_prompt_v0.md
    sha256: 7576C10F94B2A454F2619226DD7F4AD8DE2B6E0F37FF9CD92A455B9CAAA63841
  - path: .agents/workflow-overlay/product-proof.md
    sha256: 0EB8A11DAA2A2BE1FC7F610AAA48004D97200A18D11679F9C8D45731EED61F21
```

## Scope

This artifact prepares manual qualification for two owner-selected candidate contexts:

1. Sentry Seer pricing and AI debugging add-on packaging.
2. Clerk Billing / B2B Authentication packaging.

This artifact does not authorize outreach, buyer contact, contact enrichment, person-level dossiers, CRM construction, memo production, executive deck production, product-bet planning, feature planning, implementation planning, dashboards, source systems, source maps, data-spine design, automation, commits, pushes, PRs, product readiness claims, or commercial readiness claims.

Sentry and Clerk are candidate contexts only. They are not clients, leads, prospects, customers, accounts, sales opportunities, or qualified buyers.

No new public web research was run for this prep artifact. It uses the prior candidate-context scan and its compact source ledger.

The prior candidate-context scan is historical evidence context. Current qualification boundaries come from the sealed ICP decision, proof lead charter, buyer proof packet, customer-discovery prompt, and target-selection brief hashes above.

## Qualification Objective

The next possible discovery step is not to pitch Orca. It is to determine whether either candidate context contains a real, current decision that is narrow enough for a manual public-signal decision artifact.

Qualification must establish:

- a named decision owner or budget-accountable decision lead;
- a live 30-90 day pricing, packaging, API, billing, usage, add-on, or monetization decision (DecisionEvent);
- a concrete allocation consequence;
- sufficient public-signal surface for a manual memo (Memo) plus evidence appendix;
- `trust_open` or `trust_objection`, not `trust_refusal`;
- a clear memo question;
- readback agreement before memo production, and executive deck use tied to internal decision circulation before any deck production.

AI exposure may prioritize context only when it creates urgency around the first-wedge decision family. It is not a buyer filter, proof claim, or standalone decision family. `venture-backed`, `AI-native`, and `AI-adjacent` are neither qualifiers nor disqualifiers. Standalone trust, competitive-positioning, agent-workflow, or AI cost-structure questions qualify only when they resolve into pricing, packaging, API, billing, usage, add-on, or monetization.

If any of these are missing, memo and deck production remain blocked.

## Source Basis

| Candidate context | Sources already used in scan | Source role in this prep |
| --- | --- | --- |
| Sentry Seer | `https://sentry.io/pricing/`; `https://docs.sentry.io/pricing/`; `https://sentry.zendesk.com/hc/en-us/articles/45551407771931-What-is-the-pricing-for-Seer-January-21-2026` | Establishes visible pricing, telemetry quota, pay-as-you-go, Seer, active-contributor, and legacy-pricing transition surfaces to verify if intake is later authorized. |
| Clerk Billing / B2B Authentication | `https://clerk.com/pricing`; `https://clerk.com/docs/guides/billing/overview` | Establishes visible MRU pricing, B2B Authentication add-on, Billing add-on, seats, enterprise tiering, and beta/experimental Billing API surfaces to verify if intake is later authorized. |

## Candidate 1 - Sentry Seer

Qualification status: `qualification_prep_only`.

Trust posture: `unknown`; no buyer has been contacted.

Suspected decision family: pricing, packaging, billing, usage, add-on, monetization.

Candidate-context hypothesis:

Sentry may have a narrow decision context around Seer pricing, AI debugging monetization, contributor-based pricing, legacy add-on transition, and whether Seer should be bundled, separately priced, phased, grandfathered, or defended in packaging. The prior scan found visible public pricing and help-center surfaces that could support later qualification.

Likely decision-owner role type:

- AI product owner.
- Monetization or pricing owner.
- Observability platform product lead.
- Packaging / growth product owner.

Do not identify or collect named people in this phase.

Public-signal surfaces to verify later, only if authorized:

- official pricing page and pricing documentation;
- Seer pricing and active-contributor billing explanation;
- developer or customer reaction to Seer pricing and AI debugging value;
- developer reaction to telemetry quotas, overages, and pay-as-you-go behavior;
- public discussion of legacy pricing transition or add-on packaging;
- competitor or adjacent observability AI packaging signals.

Potential qualification questions if later contact is authorized:

- Is there a live 30-90 day decision around Seer pricing, packaging, bundling, contributor metrics, migration, or customer communication?
- Who owns the final decision and who owns the budget, revenue, retention, launch, or positioning consequence?
- What decision would be costly to get wrong: broad commit, narrow phase, migration message, grandfathering, bundle/add-on framing, or usage metric design?
- What public evidence would be credible enough to affect this decision?
- What public evidence would be discounted or considered too noisy?
- If skeptical, what mechanism, examples, numbers, case logic, or proof experience would be needed before public signals could affect the decision?
- Would the decision owner agree to read back a short memo plus evidence appendix before any memo is produced?
- If the memo and evidence appendix are useful, would an executive deck help internal decision circulation for this live decision?

Possible decision-artifact question shape, not authorized for production:

Should Sentry narrow, phase, bundle, defend, or reframe Seer pricing and migration messaging based on public customer/developer signal and comparable AI add-on packaging risk?

This memo question is a placeholder for qualification only. It is not a production memo or executive deck assignment.

Likely reasons this context may pass qualification:

- pricing and Seer-related public surfaces are visible;
- AI add-on packaging is concrete enough to avoid generic market research;
- active-contributor pricing and migration mechanics create a plausible allocation-risk decision;
- public developer/customer reaction may matter to communication, phasing, and packaging.

Likely reasons this context may fail qualification:

- decision is already locked or not live in the next 30-90 days;
- internal usage, attach-rate, retention, or support data dominates the decision;
- no decision owner is reachable;
- public signal is considered insufficient after explanation;
- the need turns into dashboard/source-system monitoring rather than a decision artifact;
- the question becomes broad AI observability strategy instead of pricing/package risk.

Hard stop before memo production:

Do not produce a Sentry memo, evidence appendix, or executive deck unless a named qualified buyer confirms the live decision, stakes, timing, memo question, public-signal trust posture, and readback agreement. Do not produce an executive deck unless it is tied to internal decision circulation for that qualified live decision.

## Candidate 2 - Clerk Billing / B2B Authentication

Qualification status: `qualification_prep_only`.

Trust posture: `unknown`; no buyer has been contacted.

Suspected decision family: pricing, packaging, API, billing, usage, add-on, monetization.

Candidate-context hypothesis:

Clerk may have a narrow decision context around B2B Authentication packaging, Billing add-on packaging, MRU/MRO pricing, seat-based expansion, organization-level monetization, and beta Billing API positioning. The prior scan found visible pricing and docs surfaces that could support later qualification.

Likely decision-owner role type:

- B2B product owner.
- Billing product owner.
- Pricing or packaging owner.
- Developer-platform product lead.
- Growth / monetization product owner.

Do not identify or collect named people in this phase.

Public-signal surfaces to verify later, only if authorized:

- pricing page and add-on structure;
- Billing docs and beta/experimental API status;
- B2B Authentication add-on and organization/seat surfaces;
- developer feedback on Billing, Stripe integration, MRU/MRO pricing, and seat models;
- customer or developer confusion around package boundaries;
- comparable developer-platform billing and B2B-auth packaging signals.

Potential qualification questions if later contact is authorized:

- Is there a live 30-90 day decision around Billing, B2B Authentication, MRU/MRO pricing, seats, add-on boundaries, beta positioning, or enterprise packaging?
- Who owns the decision and who owns the budget, revenue, retention, launch, or developer-adoption consequence?
- What allocation risk is most important: underpricing, overcomplicating packaging, confusing buyer roles, slowing adoption, or triggering support/developer trust issues?
- What public customer, developer, ecosystem, competitor, pricing, or docs evidence would matter?
- What evidence would be dismissed as too noisy or not comparable?
- If skeptical, what examples, numbers, mechanism, case logic, or proof experience would make public signals usable?
- Would the decision owner agree to read back a short memo plus evidence appendix before any memo is produced?
- If the memo and evidence appendix are useful, would an executive deck help internal decision circulation for this live decision?

Possible decision-artifact question shape, not authorized for production:

Should Clerk narrow, phase, reframe, bundle, or defend Billing and B2B Authentication packaging based on public developer/buyer signal around add-on boundaries, seat/MRU economics, and beta API trust?

This memo question is a placeholder for qualification only. It is not a production memo or executive deck assignment.

Likely reasons this context may pass qualification:

- packaging surfaces are visible and bounded;
- B2B Authentication and Billing connect directly to pricing, packaging, API, billing, usage, add-on, and monetization;
- beta/experimental status creates a plausible trust and adoption-risk question;
- public developer evidence may matter to package clarity and launch/rollout messaging.

Likely reasons this context may fail qualification:

- decision is not live or is too roadmap-dependent;
- internal Stripe, usage, beta-customer, or conversion data dominates the decision;
- no budget-accountable decision lead is reachable;
- public evidence is considered insufficient after explanation;
- need becomes custom implementation advice instead of decision-risk reduction;
- the question becomes broad developer-platform strategy rather than a concrete package/API decision.

Hard stop before memo production:

Do not produce a Clerk memo, evidence appendix, or executive deck unless a named qualified buyer confirms the live decision, stakes, timing, memo question, public-signal trust posture, and readback agreement. Do not produce an executive deck unless it is tied to internal decision circulation for that qualified live decision.

## Context Comparison

| Criterion | Sentry Seer | Clerk Billing / B2B Authentication |
| --- | --- | --- |
| Suspected decision narrowness | Strong: Seer pricing, contributor metric, add-on/migration framing. | Strong: Billing and B2B Authentication add-on/package boundaries. |
| Public-signal surface | Pricing, docs, help-center, developer/customer reaction surfaces likely relevant. | Pricing, docs, beta/experimental Billing API, developer/customer reaction surfaces likely relevant. |
| Risk of private-data dependency | Medium: internal Seer usage, attach rate, retention, support data may dominate. | Medium-high: internal Stripe/Billing beta, conversion, beta-customer, and usage data may dominate. |
| Risk of becoming generic market research | Medium if framed as broad AI observability strategy. | Medium if framed as broad developer-platform monetization strategy. |
| First-intake clarity | High if focused on Seer pricing and migration/packaging risk. | High if focused on Billing/B2B add-on boundaries and beta trust. |
| Initial recommended priority | 1 | 2 |

Recommended first ordering:

1. Sentry Seer, because the suspected decision surface is narrower and visibly tied to an AI add-on pricing transition.
2. Clerk Billing / B2B Authentication, because the packaging surface is strong but may depend more heavily on private beta and billing data.

This ordering is for qualification prep only. It is not a buyer ranking, sales ranking, client priority, or product-readiness signal.

## Later First-Contact Boundary If Authorized

If outreach is later authorized, first contact should qualify context, not pitch a product.

Use open-ended qualification language:

```text
I am testing whether a short public-signal decision artifact can help with live pricing, packaging, API, billing, usage, add-on, or monetization decisions. I am not pitching software. Is there a current 30-90 day decision where public customer/developer/buyer signal could help reduce allocation risk?
```

Do not use this language for outreach unless the owner separately authorizes outreach.

Do not ask leading commercial-pull questions before a decision artifact exists.

## Decision Artifact Production Gate

Memo production remains blocked for both contexts until all are true:

- named qualified buyer;
- named decision owner or budget-accountable decision lead;
- live 30-90 day pricing, packaging, API, billing, usage, add-on, or monetization decision;
- sufficient public-signal surface for the specific decision;
- `trust_open` or `trust_objection`, not `trust_refusal`;
- clear memo question;
- concrete stakes and consequence of being wrong;
- readback agreement.

If the buyer shows `trust_objection`, continue only if they are willing to evaluate evidence quality, examples, numbers, mechanism, case logic, or proof experience. If the buyer shows `trust_refusal`, stop.

Executive deck production remains blocked unless the memo and evidence appendix pass these gates and the deck is tied to internal decision circulation for the qualified live decision.

## Stop Rules

Stop before outreach unless outreach is explicitly authorized in a later owner turn.

Stop before collecting names, emails, phone numbers, LinkedIn profiles, or person-level dossiers.

Stop before memo production unless all memo-production gates pass.

Stop before executive deck production unless the memo and evidence appendix pass all gates and the deck has qualified live-decision circulation use.

Stop if either context requires private data, dashboards, source systems, automation, source maps, data-spine design, CRM workflows, or broad market monitoring before a decision artifact could matter.

Stop if either context becomes generic research, broad strategy, or source-volume collection rather than decision-risk reduction.

## Non-Claims

This qualification prep does not claim:

- buyer validation;
- willingness-to-pay proof;
- repeatability proof;
- product readiness;
- feature readiness;
- implementation readiness;
- commercial readiness;
- Core Spine v0 validation;
- client/prospect/customer relationship;
- outreach occurred;
- a buyer was contacted;
- a decision owner was qualified;
- a memo was produced;
- an executive deck was produced;
- memo usefulness;
- buyer pull;
- paid-decision-sprint-level pull.
