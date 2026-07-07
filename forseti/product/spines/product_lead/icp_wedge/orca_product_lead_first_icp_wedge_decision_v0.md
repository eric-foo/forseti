# Orca Product Lead First ICP Wedge Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Product Lead decision artifact selecting Orca's first proofable ICP and wedge.
use_when:
  - Checking the selected first Orca ICP and wedge before product-proof patches.
  - Preparing commercial-frame inputs for the first paid decision-artifact path.
  - Deciding whether later proof work may replace the current first proof lane.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/product-proof.md
  - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md
  - forseti/product/spines/product_lead/proof_charter/forseti_product_proof_lead_charter_v0.md
  - forseti/product/spines/product_lead/offer/forseti_offer_hypothesis_v0.md
input_hashes:
  - path: docs/product/orca_offer_hypothesis_v0.md
    sha256: AC3943A03864DF79918B9DC12B808E1AF39884F832592F5A71DC62FE03F76F64
  - path: docs/review-outputs/adversarial-artifact-reviews/orca_offer_hypothesis_v0_narrow_adversarial_review.md
    sha256: 26CC2DC631AD550234BDB6904640616109F76CC3F5DAC90F490ED76B524D40A6
  - path: docs/decisions/turn_08_product_thesis_v0.md
    sha256: 822653A241CF84675A3F07F695BA0ED3BFACC230F7F13AA47A4649B5DB2CD7E6
  - path: docs/product/core_spine_v0_product_contract.md
    sha256: 6D1876BE75E3ACAD349479E2CD584E869EB7A9B1C1C40F98E8C9234005EAB17E
  - path: docs/product/core_spine_v0_information_production_foundation_v0.md
    sha256: 8C0A784F80C577D725CE4D71BDED7F15B502F61B545DF5158B18352C351F7767
  - path: docs/product/orca_buyer_proof_packet_v0.md
    sha256: B7B4B1699D6918422DCDDB243E6E33C2130AA619C750003DE12C0FE7041C1F18
  - path: docs/product/orca_product_proof_lead_charter_v0.md
    sha256: BFA1685D21C318A65CE890D305B237366D7423D0BB9688B1634865813F800889
  - path: .agents/workflow-overlay/product-proof.md
    sha256: 0EB8A11DAA2A2BE1FC7F610AAA48004D97200A18D11679F9C8D45731EED61F21
  - path: docs/review-outputs/adversarial-artifact-reviews/orca_ai_exposed_icp_refinement_adversarial_review_v0.md
    sha256: 648864959A13143F9C0C4DF5A8553D5F4BD0D7608FF09ADE6632938D748CADBA
branch_or_commit: main@a873c9c3ed3b289a65f9c472c63e0aadf880a127
downstream_consumers:
  - Orca product-proof packet patch pass.
  - Orca commercial-frame Chief Architect pass.
  - Future Product Lead candidate-skill extraction review.
stale_if:
  - The offer hypothesis, buyer-proof packet, proof lead charter, or product-proof overlay changes.
  - Owner accepts a different ICP, buyer segment, decision family, or paid-first boundary.
  - External customer discovery produces contrary qualified buyer evidence.
```

## Status And Decision

Status: `PRODUCT_LEAD_FIRST_ICP_WEDGE_DECISION_V0` — **SUPERSEDED 2026-06-08 by
`docs/decisions/orca_icp_wedge_pricing_first_v0.md`**. The ICP redo replaced this
dev-facing-pricing wedge with the pricing-first / AI-monetization-beachhead
direction on the outside-in competitive-intelligence engine. This record is
HISTORICAL; read the pricing-first record for the current wedge.

Verdict: `KEEP_CURRENT_PROOF_LANE` (historical).

Selected wedge: post-revenue developer-facing B2B SaaS, platform, API, or
data-product companies with a live 30-90 day pricing, packaging, API, or
monetization decision where public customer, developer, buyer, competitor, or
ecosystem signals can change an executive decision deck and decision matrix.

Pinned source hash check (HISTORICAL — 2026-06-08): SUPERSEDED. This record is no
longer the controlling wedge source (see the pricing-first record); its pinned
`input_hashes` are stale and the original "pass" no longer holds. Do not rely on
this line.

This keeps the current proof lane, but sharpens the first wedge toward
developer-facing usage, AI add-on, billing, or packaging transitions like the
Sentry Seer and Clerk Billing / B2B Authentication candidate contexts. It does
not hard-lock Orca's broader offer boundary. AI exposure is trigger and
candidate-context ordering context only; it is not a buyer filter, not a wedge
replacement, not buyer validation, not willingness-to-pay proof, and not
market-size or capital-density proof.

## Product State Synthesis

Current phase:

Orca is docs-first and pre-validation. The offer hypothesis is provisionally
locked, not hard-locked. Core Spine v0 and the information-production
foundation define manual decision-evidence mechanics, not product readiness or
implementation authority.

Value proposition:

Orca turns messy, noisy, and contradictory public market signals into
executive-grade decision decks for high-stakes product, pricing, positioning,
growth, and competitive moves. The buyer-facing artifact is a strategic
decision deck and matrix. The internal substrate remains a memo-like reasoning
artifact (Memo) plus evidence appendix so the deck cannot outrun source-backed
judgment.

Current offer:

The offer is broad enough for foundational strategic and hyper-competitive
decisions, including pre-revenue and post-revenue contexts when the decision
is real, consequential, public signals are visible, and the buyer is willing to
pay before custom deck work. That breadth is offer surface, not first-wedge
permission.

What must become more true:

Orca must show that a real decision owner will use a public-signal decision
artifact to reduce allocation risk before committing budget, and that the
value comes from signal-quality judgment, action-ceiling discipline, and
decision accountability rather than bespoke research labor or deck polish.

Active uncertainty:

The first external buyer, commercial frame, price, duration, procurement path,
and willingness-to-pay remain unknown. Buyer validation, repeatability, and
commercial readiness are not proven.

## ICP Definition For Orca

ICP (Buyer) means the specific customer segment most likely to urgently need,
understand, buy, and successfully use Orca's public-signal decision artifact.

For Orca, an ICP must bind:

- buyer or sponsor type;
- company or organization stage;
- decision owner or decision context;
- decision family;
- urgency trigger;
- consequence if wrong;
- public or external signal availability requirement;
- willingness-to-pay or paid-first condition;
- disqualifiers.

The ICP should not be "any leader with a strategic decision." That is not a
wedge; it is an invitation to generic consulting.

## Candidate Wedges Compared

| Candidate wedge | Fit to offer and urgency | Owner, budget, and paid-first plausibility | Signal and deck proofability | Repeatability and risk | Decision |
| --- | --- | --- | --- | --- | --- |
| Current first proof lane: post-revenue B2B SaaS/platform/API/data-product pricing, packaging, API, or monetization decisions (DecisionEvent) | Strong fit. Pricing and package changes create immediate allocation risk, backlash risk, churn risk, sales-enablement cost, and competitive-response pressure. | Strongest visible owner map: VP Product, GM, pricing/packaging lead, growth/strategy lead, PMM, or founder/operator. Paid-first is plausible because the decision is budget-adjacent. | Strong. Existing candidate-context scan found visible pricing/docs surfaces for Sentry, Clerk, Vercel, Supabase, Neon, PostHog, Pinecone, and Algolia. A deck can compare options, risks, action ceilings, and signal limits. | Strongest near-term repeatability. Risk is private usage data dependence, but the proof lane already disqualifies private-data-first cases. | Keep as first wedge, sharpen around developer-facing usage, AI add-on, billing, or package-transition decisions. |
| Pre-revenue founder or founding team facing positioning, category, launch, or fundraising-narrative decision | Good offer fit in theory because runway and launch focus matter before internal data exists. | Weak-to-medium. Founder urgency can be high, but budget and paid-first behavior are less certain and can slide into fundraising narrative coaching. | Medium. Public signals may exist, but many pre-revenue decisions depend on private founder intent, investor feedback, early customer calls, or unobservable strategy. | Repeatability unproven. High risk of generic strategy consulting or pitch-deck work. | Defer. Keep in broader offer boundary, not first proof wedge. |
| Post-revenue product or strategy leader facing competitor-triggered positioning, pricing, packaging, or roadmap allocation decision | Strong fit and strong urgency, especially when competitor narrative, AI packaging, or category movement forces a response. | Strong if the owner controls roadmap, packaging, revenue, retention, or competitive-response budget. | Strong when public competitor, buyer, developer, community, and ecosystem signals are visible. The method-validation replays support action-ceiling discipline for competitive and monetization decisions. | Strong, but too broad if it includes all positioning and roadmap allocation at once. | Treat as the umbrella rationale for the selected wedge; do not broaden beyond pricing/packaging/API/monetization for first proof. |
| Investor, operator, or portfolio context | Plausible offer fit for allocation and diligence decisions where public evidence can change a decision. | Medium. Sponsor may have budget, but the decision owner and artifact user can split across investor, operator, and company team. | Medium-to-weak from current sources. Visible signals may help, but portfolio decisions often require private diligence, company data, or investment mandate context. | Risk of bespoke advisory work and unclear buyer/user boundary. Source support is not strong enough for first proof. | Defer until a concrete paid portfolio decision and public-signal surface are supplied. |
| Stop or defer all wedge selection pending external research | Conservative option, but too cautious given current sources. | Not applicable. | Not applicable. | It delays market contact despite an already bounded proof lane and candidate-context scan. | Reject. The current lane is proofable enough for docs-first qualification prep. |

## Selected First ICP / Wedge

Buyer / sponsor type:

Post-revenue B2B SaaS, developer-platform, API, infrastructure, or
data-product company where the sponsor is a VP Product, GM, pricing or
packaging lead, growth or strategy lead, product marketing lead, or
founder/operator directly accountable for the decision.

Company or organization stage:

Post-revenue is in for the first proof wedge. Pre-revenue is out for this
first wedge, even though it remains inside the broader provisional offer
boundary for later testing.

Decision owner or decision context:

A named decision owner or budget-accountable decision lead with authority over
a pricing, packaging, API, billing, usage, add-on, monetization, or related
market-response decision.

Decision family:

Pricing, packaging, API, billing, usage-based monetization, AI add-on
monetization, package migration, beta-to-paid transition, bundle versus add-on
framing, grandfathering, segment exemptions, or developer/customer
communication around those changes.

Trust, competitive-positioning, agent-workflow, and AI-cost-structure questions
are not standalone first-wedge decision families. They count inside this first
wedge only when they present as a pricing, packaging, API, billing, usage,
add-on, monetization, package-migration, or developer/customer communication
decision.

Urgency trigger:

A live 30-90 day decision caused by a planned pricing or packaging change, a
competitor or adjacent platform move, an AI/add-on monetization shift, public
developer or customer reaction, a beta or migration deadline, a board/budget
deadline, or a GTM launch deadline. AI-triggered examples include AI feature
bundling, AI add-on monetization, AI cost-structure-driven repricing, and an
AI-native competitor packaging move, but only when the trigger resolves into
the first-wedge decision families above.

Consequence if wrong:

Customer backlash, churn, delayed revenue capture, positioning damage, wasted
launch spend, support or sales-enablement cost, developer trust loss,
competitive-response misfire, or overcommitting to a broad package change when
the evidence supports only a narrower action ceiling.

Public or external signal requirement:

The target must have visible public or external signal enough to build an
inspectable memo and deck substrate: pricing pages, product docs, changelog or
help-center updates, developer/community reaction, customer or buyer
discussion, competitor packaging moves, ecosystem feedback, review-site
signals, partner commentary, or source-backed objection patterns. Official
pages alone are not enough for a strong deck unless they are paired with
relevant external signal or a clearly bounded decision-owner readback.

Paid-first condition:

No bespoke executive deck work before the buyer agrees to a paid fixed-scope
decision artifact, paid decision sprint, or another owner-approved paid-first
commercial container. Budget-adjacent behavior can count as pull evidence; it
does not waive the paid-first deck condition. For the proof loop, memo and
evidence-appendix production still requires all qualification gates, a named
decision owner, sufficient public-signal surface, and a readback agreement. The
Commercial Frame CA must later decide exact price, scope, duration, payment
terms, and whether the paid container is called a decision sprint, deck,
advisory package, or something else.

Disqualifiers:

- No named decision owner or budget-accountable decision lead.
- No live 30-90 day pricing, packaging, API, billing, usage, add-on, or
  monetization decision.
- No concrete consequence if wrong.
- No meaningful public or external signal surface.
- Buyer wants generic research, source volume, dashboard access, market
  monitoring, or deck polish instead of allocation-risk reduction.
- Buyer requires private/internal data, source systems, dashboards, automation,
  source maps, or data-spine design before public-signal evidence can matter.
- Categorical `trust_refusal`: buyer says public-signal evidence cannot affect
  this decision regardless of evidence quality, explanation, examples,
  numbers, mechanism, case logic, proof memo, or decision artifact.
- Buyer refuses readback or cannot involve the decision owner / budget-accountable
  lead before memo or deck production.
- The opportunity only works as bespoke consulting and does not repeat around a
  decision family.

Buyer attributes such as `venture-backed`, `AI-native`, or `AI-adjacent` are
neither qualifiers nor disqualifiers. They may be recorded as context, but they
cannot replace a named decision owner, live 30-90 day decision, concrete
consequence, public-signal surface, paid-first condition, trust-refusal test,
or consulting-risk test.

## Why This Wedge Wins

This wedge compounds product learning most because it is narrow enough to test
the manual Core Spine mechanics while still sitting in the provisionally
broader offer. It has a named buyer type, a recognizable budget-adjacent
decision, visible public-signal surfaces, existing candidate contexts, and
clear action ceilings such as hold, narrow, phase, exempt, grandfather, test,
message, defend, or reframe.

The pre-revenue founder wedge is tempting, but it is weaker as first proof.
Runway pressure is real, yet the work can collapse into pitch strategy,
positioning taste, or investor-narrative consulting before Orca proves that
public-signal evidence changes a paid decision.

The broader post-revenue competitor-triggered positioning wedge is strong, but
too wide for the first proof if it includes all roadmap and positioning
allocation. The selected pricing/package/API/monetization lane preserves the
best of that candidate while avoiding vague "strategy deck" drift.

AI exposure should sharpen Discovery Batch 0 candidate-context ordering only
when it makes the same pricing, packaging, API, billing, usage, add-on, or
monetization decision more urgent or more visible. It does not supersede the
selected wedge, narrow Orca's broader offer boundary, foreclose non-AI
developer-platform contexts, or convert AI funding, capital density,
market-size, public-signal volume, or strategic upside into proof of buyer
need, willingness to pay, repeatability, or commercial readiness.

The investor/operator/portfolio wedge may become valuable later, but current
sources do not show enough concrete decision-owner, paid-first, and public
signal conditions to make it the first proof wedge.

The stop/defer option is overcautious. Existing docs already name a bounded
lane and the candidate-context scan has plausible contexts for qualification
prep. Delaying all wedge selection would postpone the first real proof without
buying meaningful source clarity.

What would change the answer:

- Qualified buyers in this lane consistently require private data, dashboards,
  source systems, or generic monitoring before public-signal evidence can
  matter.
- Decision owners show `trust_refusal` rather than `trust_objection`.
- The strongest interest is unpaid deck or source-volume demand, not
  budget-adjacent decision use.
- A pre-revenue, investor, or broader strategy context supplies a named paid
  decision owner, urgent deadline, clear public-signal surface, and a sharper
  first proof path than this lane.

## Proof-Lane Implications

The current buyer-proof packet and Product Proof Lead charter should stay as
the controlling first proof-lane sources for now.

They should be patched later, not in this run, to record this Product Lead
decision:

- keep the post-revenue B2B SaaS/platform/API/data-product first proof lane;
- sharpen the first wedge toward developer-facing usage, AI add-on, billing,
  packaging, API, and monetization transitions, including AI feature bundling,
  AI cost-structure-driven repricing, and AI-native competitor packaging moves
  only when they resolve into those first-wedge decision families;
- preserve the distinction between broad offer boundary and first proof lane;
- make the buyer-facing executive deck / internal memo-substrate split
  explicit where older memo-first language may create friction;
- preserve `trust_objection` versus `trust_refusal` semantics;
- preserve all product-proof non-claims and docs-first boundaries.

No existing product docs are patched by this artifact.

## Commercial Frame Inputs

The later Commercial Frame CA should inherit these inputs:

- First commercial hypothesis remains a fixed-scope paid decision artifact or
  paid decision sprint around one qualified live decision.
- The buyer-facing artifact is the executive decision deck and matrix, derived
  from the memo and evidence appendix.
- No free bespoke executive deck production.
- Budget-adjacent behavior is pull evidence, not permission to skip the
  paid-first deck condition.
- No free source expansion after a buyer asks for "more sources."
- Memo production requires a named qualified decision owner, a live trigger,
  sufficient public signal, and readback agreement.
- Executive deck production requires memo and evidence-appendix gates plus
  internal decision-circulation use.
- Commercial pull must be budget-adjacent behavior, not praise, curiosity, or
  generic deck interest.

Unknowns that must remain unresolved here:

- Price.
- Duration.
- Scope limits.
- Payment timing.
- Refund or guarantee terms.
- Procurement path.
- Whether the paid container is called a sprint, deck, decision artifact,
  advisory package, or another format.
- Whether any unpaid qualification or sample step is allowed before paid work.
- How to handle source-expansion requests inside a paid scope.

## Product Lead Candidate Skill Notes

Repeatable mechanics observed in this CA pass:

- Load Orca overlay authority before product synthesis.
- Verify pinned hashes before treating source-heavy artifacts as stable.
- Separate offer boundary from first proof lane.
- Compare candidate wedges by buyer, stage, decision owner, urgency,
  consequence, public-signal availability, paid-first plausibility, and
  disqualifiers.
- Treat `trust_objection` as proof material and `trust_refusal` as a
  disqualifier.
- Preserve deck-first buyer framing without weakening memo and evidence
  appendix discipline.
- State patch implications without applying patches.
- Preserve product-proof non-claims in every decision artifact.

What should not become skill behavior yet:

- Auto-selecting SaaS/API/data-product pricing as Orca's permanent ICP.
- Treating candidate-context scans as qualified buyers.
- Turning deck-first framing into deck production.
- Running outreach, public research, skill creation, implementation planning,
  or commercial-frame decisions from a Product Lead synthesis pass.
- Upgrading paid-first plausibility into willingness-to-pay proof.

A future `orca-product-lead` candidate skill is justified later, not now. The
mechanics are becoming repeatable, but Orca has no accepted local candidate
skills and this run is explicitly not a skill-creation lane.

## Non-Claims

This artifact does not claim:

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
- outreach authorization;
- memo production authorization;
- executive deck production authorization;
- proof-lane graduation.

## Exact Next Authorized Step

Immediate next move:

Prepare a docs-only patch route for `docs/product/orca_buyer_proof_packet_v0.md`
and `docs/product/orca_product_proof_lead_charter_v0.md` that incorporates
this decision without changing non-claims, proof gates, or implementation
boundaries.

Conditional next-step preview:

After those patches are accepted, Discovery Batch 0 qualification prep can
continue from the Sentry Seer and Clerk Billing / B2B Authentication candidate
contexts. Outreach, public research refresh, memo production, executive deck
production, commercial-frame decisions, feature planning, and implementation
each require separate later authorization.
