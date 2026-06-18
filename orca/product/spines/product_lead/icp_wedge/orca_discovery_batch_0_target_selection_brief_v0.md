# Orca Discovery Batch 0 Target-Selection Brief v0

> **SUPERSEDED / OFF-TARGET (2026-06-12)**
> This brief predates the consumer-demand re-scope and remains hard-gated to
> the superseded pricing wedge (pricing-first propagation AR-01 had already
> flagged it as a misrouting live instrument). The live target-selection
> instrument is now
> `orca/product/spines/product_lead/icp_wedge/orca_discovery_consumer_demand_target_selection_brief_v0.md`.
> Current wedge authority:
> `docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md` (owner
> co-ratified 2026-06-12). Retained as history; do not use this brief as a
> live qualification instrument.

```yaml
retrieval_header_version: 1
artifact_role: Product artifact (superseded discovery instrument — historical)
scope: Discovery Batch 0 target-selection brief for the first Orca Product Proof Lead customer-discovery pass.
use_when:
  - Selecting blank Discovery Batch 0 target slots before outreach or web research.
  - Checking first-contact qualification objectives before memo production.
  - Preserving Product Proof Lead stop rules and non-claims.
authority_boundary: retrieval_only
superseded_by: orca/product/spines/product_lead/icp_wedge/orca_discovery_consumer_demand_target_selection_brief_v0.md
open_next:
  - .agents/workflow-overlay/product-proof.md
  - docs/decisions/orca_icp_wedge_pricing_first_v0.md  # superseded wedge record (historical)
  - orca/product/spines/product_lead/icp_wedge/orca_product_lead_first_icp_wedge_decision_v0.md # superseded by above; reread-required
  - orca/product/spines/product_lead/proof_charter/orca_product_proof_lead_charter_v0.md
  - orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
  - docs/prompts/product-planning/orca_product_proof_lead_customer_discovery_prompt_v0.md
input_hashes:
  - path: docs/product/orca_product_lead_first_icp_wedge_decision_v0.md
    sha256: B570672CD7F31B2D78F9DC5E851C3AEDA7030A56ECF2CDC6733E0191ED3DDC23
  - path: docs/product/orca_product_proof_lead_charter_v0.md
    sha256: 731E4349AA931613D393DFC64B05F410E098D40F86D1C26A11BD31A1E2852322
  - path: docs/product/orca_buyer_proof_packet_v0.md
    sha256: ECDCD4BFC626295D486189F063CA8429EA2F324BD71151C9D28A52683927A224
  - path: docs/prompts/product-planning/orca_product_proof_lead_customer_discovery_prompt_v0.md
    sha256: 7576C10F94B2A454F2619226DD7F4AD8DE2B6E0F37FF9CD92A455B9CAAA63841
  - path: docs/review-outputs/adversarial-artifact-reviews/orca_product_proof_lead_customer_discovery_prompt_v0_adversarial_review.md
    sha256: 18B623503A03CD6D3820C44EF980FAD465E8C6F6CD3250A832F54C2BEBA79E09
```

## Status

Discovery Batch: `0`.

Purpose: target selection for the first Product Proof Lead customer-discovery pass.

Output boundary: docs-first target-selection brief only. This brief does not authorize buyer outreach, public web research, memo production, executive deck production, product-bet planning, feature planning, implementation planning, commercial-readiness work, source systems, dashboards, source maps, data-spine design, CRM workflows, packages, tests, staging, commits, pushes, or PRs.

## Pricing-First Refinement (2026-06-08)

This brief's first-proof framing is REFINED by the owner-locked pricing-first
direction. Controlling wedge authority:
`docs/decisions/orca_icp_wedge_pricing_first_v0.md` (the pinned source hashes
below are superseded by it — reread-required; a hash-mismatch / BLOCKED_ROLE_DRIFT
stop does NOT fire for this intentional refinement). Deltas:

- Engine/spine = outside-in COMPETITIVE & market intelligence; pricing is its
  first application.
- First-proof BEACHHEAD re-scoped: from "developer-facing SaaS" (a stale,
  convenience-derived inheritance) to the AI-MONETIZATION SLICE — B2B SaaS making
  a first-time AI-monetization or competitor-triggered repricing/repackaging
  decision, where the competitor-pricing substrate is publicly rich and the firm
  is flying blind. Dev-facing SaaS is a strong sub-instance, not the defining
  qualifier; the wedge frame is cross-sector-open. Decision family
  (pricing/packaging/API/billing/usage/add-on/monetization) is UNCHANGED.
- Beachhead RATIONALE (test instrument, not arbitrary filter): the
  first-time/flying-blind qualifiers exist because that is where public signal can
  plausibly DECIDE the repricing move rather than merely CONFIRM it — no internal
  AI-pricing history. Caveat the proof must test: in a first-time wave the
  competitor-price substrate is itself new/sparse, so "publicly rich" is not yet
  "clean/decision-grade."
- Servability HARD GATE: the differentiated read must sit on a CLEAN,
  decision-grade public substrate — competitor PRICE/packaging signal (pricing
  pages, changelogs, filings, earnings), NOT user reviews (biased / FTC-polluted /
  interview-gated). Read "public-signal surface" below as that clean substrate;
  reviews are confirmatory-only.

```yaml
direction_change_propagation:
  doctrine_changed: First-proof framing refined to pricing-first / AI-monetization beachhead / competitive-intelligence engine / clean-substrate hard gate.
  trigger: product_doctrine
  controlling_sources_updated:
    - this artifact
  controlling_decision: docs/decisions/orca_icp_wedge_pricing_first_v0.md
  non_claims:
    - not validation
    - not willingness-to-pay
    - not readiness
    - not ICP proven
```

The body below is SURGICALLY ALIGNED to this refinement; the stop rules,
disqualifiers, blank target slots, intake objective, and non-claims are unchanged.

## Current Prep State

The customer-discovery prompt has been refreshed for the sealed Orca ICP and product-proof boundary. It treats the memo plus evidence appendix as the minimum artifact and an executive deck as the premium buyer-facing layer derived from that substrate.

The prior adversarial review recommendation was `accept_with_friction` for the pre-refresh prompt. It remains useful caution context, but this brief does not claim a new adversarial review of the refreshed prompt.

The remaining advisory friction findings are non-blocking. They should travel as caution notes, not as blockers to target-selection prep.

Reviewed prompt:
`docs/prompts/product-planning/orca_product_proof_lead_customer_discovery_prompt_v0.md`

Current prompt SHA256:
`7576C10F94B2A454F2619226DD7F4AD8DE2B6E0F37FF9CD92A455B9CAAA63841`

Adversarial review report:
`docs/review-outputs/adversarial-artifact-reviews/orca_product_proof_lead_customer_discovery_prompt_v0_adversarial_review.md`

## Selected First Lane

First lane: the AI-monetization slice — B2B SaaS making a first-time AI-monetization or competitor-triggered repricing/repackaging decision, where the competitor-pricing substrate is publicly rich and the firm is flying blind. Developer-facing SaaS is a strong sub-instance, not the defining qualifier; the wedge frame is cross-sector-open.

The target must have a visible or plausibly discoverable live 30-90 day pricing, packaging, API, billing, usage, add-on, or monetization decision. The decision must have a concrete allocation consequence, such as launch spend, pricing risk, package migration, API monetization, billing-model risk, usage-limit backlash, add-on monetization risk, churn risk, customer backlash, positioning damage, sales enablement cost, delayed capture of opportunity, or competitive response cost.

AI exposure may prioritize candidate context only when it creates urgency around the first-wedge decision family. It is not a buyer filter. `venture-backed`, `AI-native`, and `AI-adjacent` are neither qualifiers nor disqualifiers. Standalone trust, competitive-positioning, agent-workflow, or AI cost-structure questions qualify only when they resolve into pricing, packaging, API, billing, usage, add-on, or monetization.

This lane is selected for discovery qualification only. No companies are selected in this brief.

## Target Qualification Filters

A target may proceed beyond first qualification only if all hard gates pass:

- Company is in the AI-monetization slice — making a first-time AI-monetization or competitor-triggered repricing/repackaging decision (B2B SaaS as the strong sub-instance; cross-sector-open; dev-facing not required).
- A named decision owner or budget-accountable decision lead exists.
- A live pricing, packaging, API, billing, usage, add-on, or monetization decision is pending in the next 30-90 days.
- The specific decision, timing, and allocation consequence can be stated.
- A CLEAN, decision-grade public substrate exists or is plausibly discoverable — competitor price/packaging signal (pricing pages, changelogs, filings, earnings); user reviews are confirmatory-only and flagged (biased/FTC-polluted/interview-gated), not the basis of the read.
- Public-signal trust posture is `trust_open` or `trust_objection`, not `trust_refusal`.
- The buyer is seeking allocation-risk reduction, not generic market research.
- Readback agreement is secured before memo production, and executive deck use is tied to internal circulation for a qualified live decision before any deck production.

Trust rule: `trust_objection` is proof material, not disqualification. Only `trust_refusal` disqualifies on public-signal trust grounds.

Buyer-pull rule: buyer pull means observable decision or budget-adjacent behavior, not approval language, praise, curiosity, or generic research interest.

## Disqualifiers

Disqualify or hold before memo production if any condition applies:

- No named decision owner.
- No budget-accountable decision lead.
- No live 30-90 day pricing, packaging, API, billing, usage, add-on, or monetization decision.
- Decision is outside pricing, packaging, API, billing, usage, add-on, or monetization.
- AI exposure, `venture-backed`, `AI-native`, or `AI-adjacent` status is the only qualification basis.
- Standalone trust, competitive-positioning, agent-workflow, or AI cost-structure question does not resolve into a first-wedge decision family.
- Specific decision, timing, or allocation consequence cannot be stated.
- No clean, decision-grade competitor price/packaging substrate (pricing pages, changelogs, filings, earnings) exists or can be plausibly verified; user reviews alone do not satisfy this gate (biased / FTC-polluted / interview-gated; confirmatory-only).
- Categorical public-signal refusal: buyer says public-signal evidence cannot affect this decision regardless of evidence quality, explanation, examples, numbers, mechanism, case logic, or proof experience.
- Requires private data, dashboards, source systems, automation, source maps, or data-spine design before any decision use.
- Wants generic market research, market monitoring, source volume, deck polish, or dashboard access rather than a decision-risk artifact.
- Seeks manipulative, deceptive, or person-level dossier work.
- Declines decision-artifact readback or cannot include the decision owner / budget-accountable decision lead in the memo step.

## Blank Target Slots

No public web research or researched company selection has been authorized for this run. Leave companies blank until the owner authorizes public research or supplies candidate names.

| Slot | Company | Suspected decision family | Suspected trigger | Likely decision owner role | Public-signal surface to verify | Qualification status | Next intake question |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TBD | TBD | TBD | TBD | TBD | not_screened | What live 30-90 day pricing, packaging, API, billing, usage, add-on, or monetization decision is pending? |
| 2 | TBD | TBD | TBD | TBD | TBD | not_screened | Who owns the decision and the budget or business consequence? |
| 3 | TBD | TBD | TBD | TBD | TBD | not_screened | What allocation risk would be costly to get wrong? |
| 4 | TBD | TBD | TBD | TBD | TBD | not_screened | What clean competitor price/packaging signal exists (pricing pages, changelogs, filings, earnings)? Are user reviews the only available substrate (biased/FTC-polluted/interview-gated; confirmatory-only)? |
| 5 | TBD | TBD | TBD | TBD | TBD | not_screened | What would make public-signal evidence trustworthy or untrustworthy for this decision? |
| 6 | TBD | TBD | TBD | TBD | TBD | not_screened | Would the decision owner agree to decision-artifact readback before any memo or deck is produced? |
| 7 | TBD | TBD | TBD | TBD | TBD | not_screened | What specific action should the decision artifact help avoid, narrow, reframe, sequence, or defend? |
| 8 | TBD | TBD | TBD | TBD | TBD | not_screened | What deadline, launch, board, renewal, budget, competitor, or GTM event is driving urgency? |

## Intake Objective

The objective of first contact is to qualify whether a target is eligible for decision artifact production, not to sell or produce the memo, evidence appendix, or executive deck.

First contact should:

- Qualify the live decision.
- Identify the named decision owner or budget-accountable decision lead.
- Confirm stakes, timing, and allocation consequence.
- Classify public-signal trust posture as `trust_open`, `trust_objection`, or `trust_refusal`.
- Secure readback agreement before memo production.
- Decide whether memo and executive deck production are allowed, blocked, not needed, or still need clarification.

## Stop Rules

Stop before outreach unless outreach is explicitly authorized in a later owner turn.

Stop before public web research unless public research is explicitly authorized in a later owner turn.

Stop before memo production unless all memo-production gates pass:

- Named qualified buyer.
- Named decision owner or budget-accountable decision lead.
- Live 30-90 day pricing, packaging, API, billing, usage, add-on, or monetization decision trigger.
- Sufficient clean, decision-grade competitor price/packaging substrate (pricing pages, changelogs, filings, earnings); user reviews are confirmatory-only and do not satisfy this gate alone.
- Public-signal trust posture is `trust_open` or `trust_objection`.
- Clear memo question.
- Concrete decision stakes and consequence of being wrong.
- Buyer agrees to decision-artifact readback.

Stop before executive deck production unless the memo and evidence appendix pass these gates and the deck is tied to internal decision circulation for the qualified live decision.

Stop before product-bet planning, feature planning, implementation planning, source-system design, dashboards, source maps, data-spine design, automation, CRM workflows, commercial-readiness work, or readiness claims.

## Current Blockers

Before outreach:

- Outreach has not been explicitly authorized.
- No target companies have been owner-supplied or authorized for public research.
- No first-contact script has been authorized for use with buyers in this run.

Before memo production:

- No named qualified buyer exists.
- No named decision owner or budget-accountable decision lead has been confirmed.
- No live 30-90 day pricing, packaging, API, billing, usage, add-on, or monetization decision trigger has been qualified.
- No public-signal surface has been verified.
- No public-signal trust posture has been classified.
- No memo question, stakes, timing, or allocation consequence has been confirmed.
- No decision-artifact readback agreement exists.
- No executive deck use tied to internal decision circulation has been established.

## Non-Claims

This brief does not prove:

- Buyer validation.
- Willingness-to-pay proof.
- Repeatability proof.
- Product readiness.
- Feature readiness.
- Implementation readiness.
- Commercial readiness.
- Core Spine v0 validation.

This brief also does not claim buyer outreach occurred, public web research occurred, target companies were selected, a memo was produced, an executive deck was produced, a readback occurred, buyer pull was observed, or any product-proof graduation criteria were met.
