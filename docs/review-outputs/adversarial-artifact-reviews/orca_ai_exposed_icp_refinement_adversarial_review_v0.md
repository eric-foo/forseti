# Orca AI-Exposed ICP Refinement Adversarial Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Adversarial review of the proposed AI-exposed refinement to Orca's first proof wedge against the current Product Lead first ICP wedge decision and product-proof overlay.
use_when:
  - Deciding whether to patch the first ICP wedge decision artifact with the AI-exposed refinement.
  - Checking whether AI market emphasis creates hype drift or improves first-proof discipline.
  - Preparing patch implications for the first ICP wedge decision artifact, buyer-proof packet, and product proof lead charter.
authority_boundary: retrieval_only
open_next:
  - docs/product/orca_product_lead_first_icp_wedge_decision_v0.md
  - docs/product/orca_offer_hypothesis_v0.md
  - docs/product/orca_buyer_proof_packet_v0.md
  - docs/product/orca_product_proof_lead_charter_v0.md
  - .agents/workflow-overlay/product-proof.md
input_hashes:
  - path: docs/prompts/reviews/orca_ai_exposed_icp_refinement_adversarial_review_prompt_v0.md
    sha256: 5B61D61C9EB2FB4628671069169116D09F05196FE7FE9DB1202EDBD8440E09B0
  - path: docs/product/orca_product_lead_first_icp_wedge_decision_v0.md
    sha256: 67608F4E8DD0011E416C3F1619EEB4F2ACAAB1D062C46C0A4EA3527C756705A7
  - path: docs/product/orca_offer_hypothesis_v0.md
    sha256: AC3943A03864DF79918B9DC12B808E1AF39884F832592F5A71DC62FE03F76F64
  - path: docs/product/orca_buyer_proof_packet_v0.md
    sha256: B7B4B1699D6918422DCDDB243E6E33C2130AA619C750003DE12C0FE7041C1F18
  - path: docs/product/orca_product_proof_lead_charter_v0.md
    sha256: BFA1685D21C318A65CE890D305B237366D7423D0BB9688B1634865813F800889
  - path: docs/product/orca_discovery_batch_0_candidate_context_scan_v0.md
    sha256: 52A7F5E823A31562EAFDAE389AB51188BCAA021BF3E6B4478F8045435684FE28
  - path: docs/product/orca_discovery_batch_0_qualification_prep_sentry_clerk_v0.md
    sha256: EA47275CEF6F98872BDE9A00F6488BEE5ED044C4A4BE4482532D2ADDB8CB74F3
  - path: .agents/workflow-overlay/product-proof.md
    sha256: 0EB8A11DAA2A2BE1FC7F610AAA48004D97200A18D11679F9C8D45731EED61F21
branch_or_commit: main@a873c9c3ed3b289a65f9c472c63e0aadf880a127
downstream_consumers:
  - Owner or Product Lead decision to patch, defer, or reject the AI-exposed refinement.
  - Future Discovery Batch 0 qualification prep ordering.
  - Future patch route for the first ICP wedge decision artifact.
stale_if:
  - The first ICP wedge decision artifact is patched, replaced, or superseded.
  - Product-proof trust or non-claim semantics change in `.agents/workflow-overlay/product-proof.md`.
  - Owner accepts or rejects the AI-exposed refinement.
  - A separate ICP Chief Architect run replaces the current first proof wedge.
```

## Deep-Thinking Frame

Real decision under review:

Is the proposed AI-exposed refinement a *better first proof wedge* than the currently selected one, or does it weaken proof discipline by adding hype-driven buyer-attribute filters on top of a decision-family lane that already accommodates AI-triggered pricing and packaging decisions?

Strongest failure modes framed before findings:

- Hype drift: AI funding and VC density rationale could be read as buyer-proof signal when it is hypothesis material about market potential.
- Forbidden upgrades: long-term market potential, urgency, and capital density claims could leak into willingness-to-pay or commercial-readiness territory.
- Survivorship/availability bias: the candidate-context scan already concentrated on AI-adjacent contexts (Sentry Seer, Vercel AI Cloud, Pinecone, Algolia AI Search); using that scan to justify the refinement risks circular evidence.
- Wedge widening under a narrowing label: the refinement adds "trust" and "competitive-positioning" decision families and "agent workflows" / "AI cost structure" triggers that exceed the current pricing/packaging/API/billing/monetization decision lane.
- Buyer-attribute filtering vs decision-family sharpening: "venture-backed AI-native or AI-adjacent" is a buyer-attribute filter, not a decision-family sharpener; the existing wedge already permits AI add-on triggers without that filter.
- Generic AI strategy consulting drift: when "AI cost structure" or "agent workflows" frames the decision, the conversation can slide from action-ceiling discipline into AI strategy advisory.
- Public-signal noise: AI-exposed public conversation is louder but also more hype-driven, model-driven, and anecdotal; higher volume is not higher signal quality.

Criteria that should decide the review:

- Does the refinement add a sharper, more disqualifying ICP filter without creating hype drift or generic strategy consulting risk?
- Does it preserve all current product-proof non-claims?
- Does it preserve the distinction between offer boundary, first proof wedge, and later expansion path?
- Does it sharpen the decision family or only the buyer attribute set?
- Is whatever the refinement adds already accommodated by the current wedge plus the candidate-context scan?

Deep thinking does not widen scope, authorize patching, or convert this review into product planning. The output remains a review report with findings, non-findings, not-proven boundaries, and the next authorized step.

## Preflight

- Workspace: `C:\Users\vmon7\Desktop\projects\orca`.
- Branch verified: `main`.
- HEAD verified: `a873c9c3ed3b289a65f9c472c63e0aadf880a127`.
- Source hash check: all pinned input hashes match the prompt's input_hashes.
- Dirty state: allowed by prompt. Relied-on dirty or untracked sources include the overlay files, the first ICP wedge decision artifact, the offer hypothesis, the buyer-proof packet, the product proof lead charter, the candidate-context scan, the Sentry/Clerk qualification prep, and the product-proof overlay.
- Review lane: Orca adversarial artifact review (read-only).
- Reviewer write permission: this report only, under `docs/review-outputs/adversarial-artifact-reviews/`.
- Patch execution: not authorized.
- No public web research was run. The review used only Orca overlay and accepted Orca docs.

## 1. Verdict

Verdict: `ACCEPT_WITH_CAVEATS`.

One-sentence reason: the refinement is directionally useful as a trigger-language sharpening of the existing wedge, but it should not replace the current wedge wholesale because as written it widens the decision-family scope, adds buyer-attribute filters that exceed available evidence, and risks hype-driven proof drift.

## 2. Best Case For The Refinement

The strongest argument the refinement has going for it:

- The current candidate-context scan and the owner-selected Discovery Batch 0 priorities are already concentrated in AI-triggered pricing and packaging contexts. Sentry Seer is explicitly an "AI debugging add-on" pricing transition. Vercel's Fluid compute and AI Cloud surfaces are framed around AI workload economics. Pinecone, Algolia AI Search, and Clerk's beta Billing all sit close to AI-adjacent monetization questions.
- Naming the AI exposure makes a real concentration of decision urgency more legible. AI add-on pricing, AI cost structure, agent workflow billing, and AI-native competitor moves do plausibly create 30-90 day budget-adjacent decisions with visible public surfaces.
- A buyer who explicitly sees an AI-driven trigger may be more willing to evaluate public-signal evidence because the AI environment itself is changing fast enough that internal data is more obviously incomplete.
- Funding density and capital concentration around AI-native companies is, hypothetically, correlated with budget-adjacent decision behavior. That correlation is not buyer validation, but it is plausible context for the candidate-context scan's existing ordering.
- The refinement does explicitly reject "anything with AI in the name" as hype drift, which is the right disclaimer.

This best case supports a narrow conceptual sharpening of trigger language inside the existing wedge. It does not support a full replacement.

## 3. Strongest Objections

Listed by importance.

### O-1. The current wedge already accommodates AI-triggered pricing and packaging decisions

The Product Lead first ICP wedge decision already names "AI add-on monetization shift," "AI/add-on monetization," and "developer-facing usage, AI add-on, billing, packaging, API, and monetization transitions" inside the urgency triggers and the first-wedge sharpening (`orca_product_lead_first_icp_wedge_decision_v0.md` lines 158-166, 264-266). The Sentry Seer and Vercel AI Cloud contexts in the candidate-context scan are already inside the current wedge.

So the refinement's marginal sharpening over the current wedge is mostly:

- adding "venture-backed AI-native or AI-adjacent" as a buyer-attribute filter;
- adding "trust" and "competitive-positioning" to the decision-family list;
- adding "agent workflows" and "AI cost structure" to the trigger list;
- substituting "AI-native competitors" for "competitor or adjacent platform move."

None of those four additions is required to keep Sentry Seer, Clerk Billing, Vercel AI Cloud, Pinecone, or Algolia in scope. They are already in scope.

### O-2. The refinement widens the decision-family scope under a narrowing label

The current first proof lane is bounded to "pricing, packaging, API, billing, usage-based monetization, AI add-on monetization, package migration, beta-to-paid transition, bundle versus add-on framing, grandfathering, segment exemptions, or developer/customer communication around those changes" (`orca_product_lead_first_icp_wedge_decision_v0.md` lines 155-159).

The refinement adds "trust" and "competitive-positioning" as live decision triggers. "Trust" is broader than billing/packaging and easily collapses into brand, narrative, or messaging consulting. "Competitive-positioning" was explicitly downgraded in the Product Lead candidate-wedge comparison (see the "post-revenue product or strategy leader facing competitor-triggered positioning, pricing, packaging, or roadmap allocation decision" row, lines 128-129): "too broad if it includes all positioning and roadmap allocation at once." The refinement reintroduces what the existing decision artifact already rejected as too broad, but tagged with "AI" to make it sound narrow.

### O-3. Capital density and long-term market potential are hypothesis material, not proof inputs

The proposed core claim says the AI refinement "preserves proofability while increasing long-term market potential, urgency, capital density, public-signal density, and strategic upside." Four of those five (long-term market potential, capital density, public-signal density, strategic upside) are TAM-flavored claims about a market.

The product-proof non-claims (`.agents/workflow-overlay/product-proof.md` lines 141-156; `orca_buyer_proof_packet_v0.md` lines 338-355) explicitly forbid treating capital availability, market enthusiasm, or single strong-signal density as buyer validation, willingness-to-pay proof, repeatability proof, or commercial readiness.

The refinement's rationale, as stated, leans on those market claims. As long as that rationale only orders the candidate-context scan, it is allowed. If it justifies a wedge replacement or future graduation argument, it crosses into forbidden upgrades.

### O-4. "Venture-backed AI-native or AI-adjacent" is a buyer-attribute filter that exceeds available evidence

No accepted Orca doc supports either of the following claims:

- venture-backed companies are more likely to convert to paid-decision-sprint-level pull on a public-signal decision artifact than non-venture-backed companies;
- AI-native companies are more likely to have decision owners with public-signal openness (`trust_open` or `trust_objection`) than non-AI-native companies.

Both are plausible. Neither is qualified. Treating either as an ICP filter elevates an unqualified hypothesis to ICP discipline level. The buyer-proof packet (`orca_buyer_proof_packet_v0.md` lines 58-83) and product proof lead charter (`orca_product_proof_lead_charter_v0.md` lines 83-98) are already deliberately silent on funding stage and AI-nativity because there is no buyer evidence to justify those filters yet.

The "AI-adjacent" half also dissolves in practice. Stripe, Shopify, Vercel, Sentry, Cloudflare, Algolia, Twilio, and most B2B SaaS companies are arguably AI-adjacent today. If "AI-adjacent" covers most current developer-platform candidates, it does not disqualify, and therefore does not sharpen the wedge.

### O-5. The candidate-context scan does not prove AI-exposed concentration is a population fact

The candidate-context scan used 8 search queries and opened 18 pages, of which 16 supported usable evidence (`orca_discovery_batch_0_candidate_context_scan_v0.md` lines 33-38). The scan deliberately concentrated on developer-platform pricing pages where AI add-ons were visible. Several non-AI contexts (Datadog/New Relic observability packaging, Netlify, OpenAI/Anthropic API pricing, Cursor coding subscription) were deferred or excluded specifically to preserve scan caps.

That sample is a candidate-context source ledger, not a market population study. Concluding from it that AI-exposed contexts are the densest first-wedge population would be a survivorship inference. The scan was not designed to disqualify non-AI contexts.

### O-6. Forbidden overconfidence from "VC money is flowing into AI"

The proposed refinement core claim names capital density as part of the rationale. This is exactly the failure mode the prompt asked to test for. Capital density does not produce decision-owner authority, budget-adjacent behavior on this specific decision, public-signal surface, `trust_open` or `trust_objection` posture, paid-first commercial willingness, or repeatability. It correlates with budget existence, not with public-signal decision-artifact willingness to pay.

If the refinement is read as "AI companies have money so the proof loop will close faster," the proof discipline is broken. The buyer-proof packet's Grade D and kill criteria depend on `trust_refusal` and decision-use, not on the buyer's funding (`orca_buyer_proof_packet_v0.md` lines 208-214, 275-286).

### O-7. AI-native context risks generic AI strategy consulting drift

The Product Lead artifact already flags "risk of generic strategy consulting" for the pre-revenue founder wedge and "risk of bespoke advisory work" for the investor/operator wedge (`orca_product_lead_first_icp_wedge_decision_v0.md` lines 128, 130, 220-228, 240-243). The same risk applies to AI-native contexts when the buyer wants help with "AI strategy," "AI cost structure," or "agent workflow design" rather than a specific pricing/packaging action ceiling.

The Product Lead charter and buyer-proof packet have specific disqualifiers for this kind of drift: "buyer wants generic research, source volume, dashboard access, market monitoring, or deck polish instead of allocation-risk reduction" and "the opportunity only works as bespoke consulting and does not repeat around a decision family" (`orca_product_lead_first_icp_wedge_decision_v0.md` lines 203-216). The refinement does not strengthen those disqualifiers and may weaken them by introducing decision-family language ("trust," "competitive-positioning," "agent workflows") that is easier to bend into AI strategy advisory.

### O-8. AI-exposed public conversation is noisier, not necessarily higher-quality

Public-signal density is one of the refinement's named benefits. Public AI commentary is high-volume but disproportionately hype, model-comparison anecdotes, X/Reddit takes, and analyst speculation. The buyer-proof packet's signal-quality rubric (`orca_buyer_proof_packet_v0.md` lines 134-146) treats source cleanliness, audience fit, uncertainty framing, and artificial-amplification risk as proof criteria. AI-native public commentary will normally score worse than developer pricing-page reactions, changelog comments, or formal community feedback for the kinds of decisions Orca targets. More signal does not mean better deck substrate.

### O-9. AI-driven decisions move fast in ways that complicate repeatability

A 30-90 day AI add-on pricing decision today may not generalize to the same decision six months later because the underlying AI cost stack is moving. Repeatability around a "decision family caused by AI adoption" is harder to demonstrate than repeatability around pricing/packaging/API/monetization regardless of AI exposure. Orca's graduation criteria require two independent qualified decision owners in the same buyer segment and decision family producing Grade A or Grade B results without reusing the same buyer or same internal decision (`orca_buyer_proof_packet_v0.md` lines 289-300). A faster-moving substrate makes that bar harder to clear, not easier.

### O-10. Offer-boundary leakage risk

The offer hypothesis is intentionally broader than the first proof wedge (`orca_offer_hypothesis_v0.md` lines 91-110, 158-204). The Product Lead artifact restates this distinction (`orca_product_lead_first_icp_wedge_decision_v0.md` lines 82-90, 264-271). Replacing the current wedge with "AI-exposed" risks narrowing the offer boundary by precedent: if the first wedge is AI-only, future agents may assume Orca's offer is AI-only. That collapses Orca's later-expansion path into AI-adjacent companies and weakens the foundational/hyper-competitive decision framing the offer hypothesis is built around.

## 4. Failure Modes If Accepted

If the refinement is accepted wholesale, plausible downstream failure modes:

- Future agents cite the refined wedge to deprioritize non-AI developer-platform contexts (Clerk Billing's non-AI pieces, Supabase's general usage-based billing, PostHog's usage-based product-suite pricing, Neon's serverless Postgres economics) even when those contexts have stronger live decisions and stronger public-signal surface than an available AI-adjacent context.
- Discovery Batch 0 ordering subtly shifts from "candidate context with the strongest visible decision and public-signal surface" to "candidate context most legible as AI-exposed." The two are not equivalent.
- "Capital density" and "venture-backed" framing seeps into outreach posture and commercial-frame inputs, treating AI VC funding as a signal that buyers will pay before Orca has proof.
- "Trust" and "competitive-positioning" decision families pull discovery into AI brand and narrative work, away from pricing/packaging/billing/monetization action ceilings.
- "AI cost structure" or "agent workflows" framing converts qualified pricing decisions into AI strategy consulting requests, which the existing kill criteria flag as consulting-risk.
- The buyer-proof packet's repeatability requirement gets harder to satisfy because two independent AI-adjacent buyers facing the same AI cost decision are rarer than two independent developer-platform buyers facing the same pricing/packaging decision.
- The offer boundary narrows by precedent. If the first proof wedge is AI-only, Orca's positioning drifts toward "AI strategic intelligence" rather than "public-signal decision intelligence."
- A future patch-route reviewer may treat the refinement's market-size rationale (capital density, public-signal density, long-term market potential) as accepted background, and use it to justify outreach scale or unpaid bespoke work that the buyer-proof packet disallows.
- The kill criteria become harder to apply cleanly. Trust refusal in a "competitive-positioning" or "trust" decision frame is harder to classify than in a pricing/packaging frame because "trust" is itself the topic.

## 5. What Should Change In The Decision Artifact

Patch execution is not authorized in this review. The conceptual patch units below are advisory only.

### Recommended conceptual patch units

P-1. Patch trigger language, not the buyer attribute set, in the first ICP wedge decision artifact.

Conceptual delta: in the "Urgency trigger" section and in the "Why This Wedge Wins" preface, name AI add-on monetization, AI cost-structure-driven repricing, AI-native competitor packaging moves, and AI feature bundling as explicit examples of the already-named live triggers. Do not introduce "AI-native or AI-adjacent" as a buyer filter. Do not add "venture-backed" as a buyer filter.

P-2. Add a short non-supersession guard on the AI rationale.

Conceptual delta: state in the Product Lead artifact that AI exposure is a candidate-context ordering hypothesis for Discovery Batch 0, not a wedge replacement, not buyer validation, not willingness-to-pay proof, not market-size proof, and not capital-density proof. Map it back to the existing offer-boundary vs first-wedge distinction.

P-3. Reject the "trust" and "competitive-positioning" decision families as wedge additions.

Conceptual delta: do not patch the decision family beyond pricing, packaging, API, billing, usage-based monetization, AI add-on monetization, package migration, beta-to-paid transition, bundle versus add-on framing, grandfathering, segment exemptions, or developer/customer communication around those changes. If competitive-positioning is needed later, route it through a separate ICP Chief Architect run.

P-4. Reject "agent workflows" and "AI cost structure" as standalone triggers.

Conceptual delta: an "agent workflows" decision only counts inside the first wedge when it presents as pricing, packaging, API, billing, or monetization. "AI cost structure" only counts when it presents as the same. Otherwise it is candidate-context only.

P-5. Reaffirm the disqualifier set without softening it.

Conceptual delta: re-state that buyer attribute filters such as venture-backed, AI-native, or AI-adjacent are not disqualifiers and are not qualifiers. Disqualifiers stay grounded in named decision owner, live 30-90 day decision, public-signal surface, paid-first plausibility, `trust_refusal` test, and consulting-risk test (`orca_product_lead_first_icp_wedge_decision_v0.md` lines 197-216).

P-6. Preserve the offer-boundary / first-wedge / later-expansion distinction explicitly.

Conceptual delta: add or reinforce a sentence that this trigger-language sharpening does not narrow Orca's offer boundary, does not supersede the offer hypothesis, and does not foreclose non-AI-adjacent expansion later.

P-7. Preserve all existing non-claims verbatim.

Conceptual delta: no change required. The Product Lead artifact's non-claims block (lines 339-355) is correct and must not be weakened.

### Not recommended

- Replacing the current wedge text with the proposed AI-exposed wedge sentence.
- Introducing "venture-backed" or "AI-native or AI-adjacent" as a binding ICP attribute.
- Introducing "trust" or "competitive-positioning" as live decision families inside the first proof wedge.
- Treating the refinement's market-size, capital-density, public-signal-density, or strategic-upside rationale as accepted product fact.

## 6. What Must Not Change

- Product-proof non-claims listed in `.agents/workflow-overlay/product-proof.md`, `orca_buyer_proof_packet_v0.md`, `orca_product_proof_lead_charter_v0.md`, and the first ICP wedge decision artifact.
- The `trust_objection` versus `trust_refusal` distinction. Initial buyer skepticism about AI hype, AI vendor proliferation, or AI cost noise is `trust_objection`, not `trust_refusal`. Disqualification still requires categorical refusal.
- The manual decision memo plus evidence appendix as the minimum proof artifact and proof gate. The executive deck remains derived from that substrate.
- The paid-first commercial boundary. AI funding density does not waive the paid-first deck condition. Budget-adjacent behavior remains pull evidence; AI capital availability does not.
- The kill criteria around consulting-risk drift, private-data dependence, generic research demand, and missing decision ownership.
- The graduation criteria around two independent qualified decision owners in the same buyer segment and decision family producing Grade A or Grade B results without reusing the same buyer or same internal decision.
- The distinction between offer boundary, first proof wedge, and later expansion path.
- Docs-first boundaries. The refinement does not authorize software, automation, dashboards, source maps, data-spine designs, source systems, packages, tests, commits, pushes, PRs, or feature plans.
- Source hierarchy. The Orca overlay wins over reusable workflow guidance for Orca facts.

## 7. Evidence Gaps / Not Proven

This review is source-bounded to Orca overlay and accepted Orca docs. The following are explicitly not proven by this review:

- That AI-exposed companies have more decision-owner-level public-signal openness than non-AI-exposed developer-platform companies.
- That venture-backed AI-native companies convert to fixed-scope paid-decision-sprint-level pull faster, more reliably, or at higher rates than non-venture-backed or non-AI-native developer-platform companies.
- That AI-exposed pricing or packaging decisions have higher repeatability across independent buyers than non-AI-exposed pricing or packaging decisions.
- That AI-driven public-signal volume translates to higher-quality decision evidence rather than higher noise.
- That capital density in AI markets reduces the time, work, or cost required to qualify a buyer, produce a memo, or close a paid-decision sprint.
- That the Discovery Batch 0 candidate-context scan, with 8 search queries and 18 opened pages, is population-representative of where the first wedge's strongest contexts live.
- That the "AI-adjacent" half of the proposed filter is well-defined enough to disqualify or qualify a buyer in practice.
- That "trust" or "competitive-positioning" decisions caused by AI exhibit the same decision-owner, budget-adjacency, public-signal-surface, and action-ceiling properties as pricing/packaging/API/billing/monetization decisions.
- That AI-adjacent buyers are less prone to generic strategy consulting drift than non-AI-adjacent buyers.

## 8. Recommendation

Exact next authorized step:

Prepare a docs-only patch route for `docs/product/orca_product_lead_first_icp_wedge_decision_v0.md` that incorporates patch units P-1 through P-7 above without changing any non-claim, proof gate, disqualifier, offer-boundary distinction, or implementation boundary. The patch route should be a separate authorized turn, not implemented from this review.

That patch route should:

- sharpen trigger language to make AI add-on monetization, AI cost-structure-driven repricing, AI-native competitor packaging moves, and AI feature bundling explicit examples of the already-named triggers;
- not introduce "venture-backed," "AI-native," or "AI-adjacent" as buyer-attribute filters;
- not extend the first-wedge decision family to include "trust" or "competitive-positioning";
- not extend the first-wedge trigger set to include standalone "agent workflows" or "AI cost structure" decisions outside pricing/packaging/API/billing/monetization;
- restate the offer-boundary / first-wedge / later-expansion distinction;
- preserve all current non-claims, kill criteria, graduation criteria, and disqualifiers.

No outreach, public web research, memo production, executive deck production, commercial-frame decision, feature planning, implementation, automation, source-system design, dashboard work, skill creation, commits, pushes, or PRs is authorized by this review.

Discovery Batch 0 ordering may informally consider AI exposure as candidate-context interest, but only as a candidate-context hypothesis. It must not be elevated to a qualification gate, disqualifier, or paid-first signal.

Review-use boundary: these findings are decision input. They are not mandatory remediation, approval, validation, or executor-ready patch authority unless a separate authorized Orca patch or decision lane accepts them.

## 9. Non-Claims

This review does not claim:

- buyer validation;
- willingness to pay;
- paid pilot conversion;
- repeatability;
- ROI;
- product readiness;
- feature readiness;
- implementation readiness;
- commercial readiness;
- Core Spine v0 validation;
- target-company qualification;
- AI-market sizing correctness;
- AI capital-density relevance to Orca's first proof;
- outreach authorization;
- memo production authorization;
- executive deck production authorization;
- proof-lane graduation;
- that the refinement, as written, is accepted, approved, locked, or buyer-proven;
- that the Discovery Batch 0 candidate-context scan, qualification prep, or ordering is validated.
