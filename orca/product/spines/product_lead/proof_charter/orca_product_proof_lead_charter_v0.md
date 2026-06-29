# Orca Product Proof Lead Charter v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Bounded charter for the Orca Product Proof Lead and first buyer-proof lane.
use_when:
  - Setting up Orca buyer-proof work before feature planning.
  - Checking Product Proof Lead ownership, exclusions, and graduation rules.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/product-proof.md
  - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md     # current wedge authority (supersedes pricing-first)
  - orca/product/spines/product_lead/icp_wedge/orca_product_lead_first_icp_wedge_decision_v0.md  # superseded — historical (path updated 2026-06-12; phase-2 migration)
  - orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md  # path updated 2026-06-12 (phase-2 migration); owns the Demand-Substrate Hard Gate
  - docs/decisions/orca_product_thesis_consumer_demand_v0.md      # controlling thesis (supersedes turn_08; ratified 2026-06-12)
input_hashes:
  - path: docs/decisions/turn_08_product_thesis_v0.md
    sha256: 822653A241CF84675A3F07F695BA0ED3BFACC230F7F13AA47A4649B5DB2CD7E6
  - path: docs/product/core_spine_v0_method_validation_replay_packet_v0.md
    sha256: 8CB2D592D49C1C10DD5DD91A070D2800AF61DFDFC67D7C56A404A75F2EEA2161
  - path: docs/product/orca_product_lead_first_icp_wedge_decision_v0.md
    sha256: B570672CD7F31B2D78F9DC5E851C3AEDA7030A56ECF2CDC6733E0191ED3DDC23  # superseded by orca_icp_wedge_pricing_first_v0.md; hash preserved, reread-required
  - path: docs/review-outputs/adversarial-artifact-reviews/orca_ai_exposed_icp_refinement_adversarial_review_v0.md
    sha256: 648864959A13143F9C0C4DF5A8553D5F4BD0D7608FF09ADE6632938D748CADBA
```

## Status And Boundary

Status: `PROPOSED_PRODUCT_PROOF_CHARTER_V0`

Product planning verdict: `NEEDS_CUSTOMER_DISCOVERY`.

Readiness verdict: `ready for product-fit testing`; not buyer-validated, not feature-ready, not implementation-ready, and not commercially ready.

This charter defines a bounded Orca Product Proof Lead. It is not a full Product Lead role. It does not own roadmap, feature planning, implementation, product readiness, commercial readiness, or validation claims.

This artifact is docs-first only. It does not authorize software implementation, automation, packages, tests, dashboards, source maps, data-spine designs, commits, pushes, PRs, collection pipelines, or feature planning.

## Consumer-Demand Refinement (2026-06-12, ratified cascade)

This charter's first-proof framing is RE-TARGETED by the owner-ratified
consumer-demand direction. Controlling authority:
`docs/decisions/orca_product_thesis_consumer_demand_v0.md` (thesis,
`OWNER_LOCKED` 2026-06-12) and
`docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md` (wedge,
`OWNER_LOCKED_DIRECTION` 2026-06-12), which supersede
`docs/decisions/orca_icp_wedge_pricing_first_v0.md` as first-proof authority
(pricing retained as engine application + re-entry candidate). Earlier pinned
`input_hashes` / wedge references are superseded — reread-required.

The engine is unchanged — outside-in market & competitive intelligence; its
first application is now beauty consumer-demand allocation. The substrate
hard gate is the Demand-Substrate Hard Gate in
`orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md` (fusion across
venue families + costly-behavior anchoring + integrity labels; reviews
admissible as one flagged venue; org-motion corroboration through
capture-lane-bound routes under the owner's measured-ToS-risk posture, ask-1
amendment 2026-06-12). Role boundaries, pull standard, kill/graduation
criteria, and every not-proven boundary are unchanged.

The executed `direction_change_propagation` receipt for this ratification
event lives in `docs/decisions/orca_product_thesis_consumer_demand_v0.md`
("Doctrine-Change Propagation — Executed"). Applied here by the ratification
cascade; the live text reflects the applied deviations.

```yaml
direction_change_propagation:
  note: >
    This file is a downstream surface of the carve-out 2026-06-15
    cap-redefinition propagation. "What Remains Outside The Role" updated:
    the cap now refers to our own operating/capture accounts (≤10, starting ≤5);
    subject-creator roster uncapped (all-in-vertical); active = attended; passive
    = bounded self-terminating runs. The "pre-commercial, internal only;
    external/product person-level boundary unchanged" clause is preserved verbatim
    and unchanged. The Product Proof Lead's authorized external activity scope is
    NOT expanded by this change.
  authority: docs/decisions/wind_caller_calibration_carveout_v0.md (2026-06-15 amendment)
  date: 2026-06-15
```

## Commercial Target Selection Update (2026-06-16)

Owner direction confirms the first commercial target for the proof loop as
US-market tractioned indie/DTC beauty or personal-care operators with a named
decision owner and a live 30-90 day consumer-demand allocation decision (DecisionEvent).

The Product Proof Lead should bias candidate qualification toward
retail/channel expansion, launch/reposition, and inventory or purchase-depth
commitment before tier/price, taste-shift pivot, or defend/hold decisions.
Those first families have the clearest timing, allocation stakes, and
public-signal relevance before internal data is conclusive.

Retailer/category teams are deferred because their proprietary sell-through,
basket, loyalty, and vendor data often makes Orca's public-signal increment
harder to prove in the first 2-3 month window. This is a sequencing constraint,
not a business-ending conclusion. If operator-first proof fails, the
owner-decided fallback ladder remains consumer fund screen and then
PE/family-office diligence. Agencies and incubators may later route to brand
decision owners, but they are not the first buyer-proof target.

Customer-provided proprietary data is a later augmentation path, not a first
proof dependency. The Product Proof Lead may later route a separate
data-spine/proof question for reconciling Orca's public-signal judgment against
internal sell-through, CRM, panel, retail, or cohort evidence. This charter's
first proof loop remains public-first and must not require proprietary-data
intake, data science, dashboards, integrations, or source-system buildout to
make the memo credible.

## Source Basis

- Current owner instruction for Orca product-proof planning.
- `AGENTS.md` and `.agents/workflow-overlay/` authority, especially product artifact write permission under `docs/product/`.
- `docs/decisions/turn_08_product_thesis_v0.md`, which frames Orca as an outside-in strategic intelligence system for public market signals and allocation decisions.
- `docs/decisions/orca_icp_wedge_pricing_first_v0.md` — wedge authority at authoring (owner-locked 2026-06-08; superseded 2026-06-12 by `docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md`); supersedes the v0 ICP wedge below.
- `docs/product/orca_product_lead_first_icp_wedge_decision_v0.md`, which selects the first proof lane and binds AI exposure as trigger/context ordering only. SUPERSEDED by `docs/decisions/orca_icp_wedge_pricing_first_v0.md`; reread-required.
- `docs/review-outputs/adversarial-artifact-reviews/orca_ai_exposed_icp_refinement_adversarial_review_v0.md`, which rejects AI buyer-attribute filters and standalone AI/trust/competitive-positioning decision-family expansion.
- `docs/product/core_spine_v0_method_validation_replay_packet_v0.md`, accepted only as bounded method signal, not validation, buyer validation, feature readiness, implementation readiness, or commercial readiness.
- Advisory `workflow-product-ultraplan` standard lanes: directional, adversarial, and grounding. These were advisory inputs only, not verdicts or readiness proof.

No public web research was used. Archived contaminated replay outputs were not read.

## Role Purpose

The Orca Product Proof Lead owns the buyer-proof loop for one narrow question:

Can a real decision owner at an indie/DTC beauty / personal-care brand (Brand) facing
a live consumer-demand allocation decision — where internal data is not
conclusive — use an Orca decision artifact to reduce allocation risk before
committing inventory, retail/channel, launch, or pricing budget, after Orca
captures, cleans, integrity-labels, classifies (costly behavior, never
engagement/resonance volume alone), and constrains messy public demand signals, fused
with org-level (Org) org-motion corroboration, into inspectable decision evidence
with an explicit action ceiling?

The engine for this work is outside-in market and competitive intelligence;
beauty consumer-demand allocation is its first application per the ratified
thesis and wedge (2026-06-12).

The minimum viable artifact is a manual decision memo (Memo) plus evidence appendix. The premium buyer-facing artifact is an executive-grade decision deck derived from that memo and appendix. The first commercial next-step hypothesis is a fixed-scope paid decision sprint, not validated commercial readiness.

The role exists to convert bounded method signal into buyer-proof learning without prematurely turning Orca into a product organization, software system, dashboard, deck shop, research factory, or implementation program.

## What The Product Proof Lead Owns

1. Buyer-proof design for the first external proof loop.
2. Selection of one target buyer segment (Buyer) and one live decision family for the proof.
3. Qualification of live decision triggers before memo production.
4. The manual Orca decision memo, evidence appendix, and optional executive deck shape used in the proof.
5. The proof evaluation rubric, including pull, weak signal, kill, and graduation criteria.
6. Source cleanliness, uncertainty framing, action-ceiling discipline, and explicit non-claims inside proof artifacts.
7. Buyer readback questions that test decision use, risk reduction, trust, and commercial next step.
8. Proof notes that distinguish buyer behavior from praise.
9. Recommendations to kill, reframe, continue discovery, or graduate the proof.
10. Boundary enforcement against roadmap, feature, implementation, validation, and commercial-readiness leakage.

## What Remains Outside The Role

The Product Proof Lead does not own:

- Orca roadmap.
- Product readiness.
- Feature planning or feature readiness.
- Implementation planning or implementation readiness.
- Software architecture, runtimes, packages, tests, dashboards, source maps, data-spine designs, source systems, collection pipelines, automations, scoring engines, or generalized tooling.
- Commercial readiness, sales operations, final pricing, packaging, procurement operations, or revenue ownership.
- Claims that Core Spine v0 is validated, accepted, predictive, buyer-validated, feature-ready, implementation-ready, or commercially ready.
- Broad AI strategy, standalone trust work, standalone competitive-positioning
  work, agent-workflow design, or AI cost-structure analysis unless it
  presents as a qualified consumer-demand allocation decision in the first
  proof lane's families.
- Broad market research, generic social listening, person-level dossiers (exception: internal wind-caller (WindCaller) calibration per `docs/decisions/wind_caller_calibration_carveout_v0.md` — bounded to ≤10 own operating/capture accounts (starting ≤5); subject-creator roster uncapped (all-in-vertical); active = attended; passive = bounded self-terminating runs (carve-out 2026-06-15 amendment); pre-commercial, internal only; external/product person-level boundary unchanged), outreach lists, data-broker activity, manipulation, fake reviews, botting, or deceptive competitive tactics.
- Revalidation of the accepted method replay packet or use of archived contaminated replay outputs.

## First Proof Lane

Recommended first buyer segment:

US-market tractioned indie/DTC beauty / personal-care brand decision owners
(founder, head of brand / insights / growth / strategy, or equivalent
operator) with a live 30-90 day demand-allocation decision and a concrete
allocation consequence, passing the buyer-proof packet's Demand-Substrate Hard
Gate (at least two independent venue families (Venue); costly-behavior anchoring;
integrity labels applicable; org-motion corroboration through
capture-lane-bound routes).

If results are mixed, diagnose the demand decision families separately
(retail/channel expansion vs launch/reposition vs inventory/purchase-depth vs
tier/price vs defend/hold) before treating the decision family as repeatable
or non-repeatable.

Recommended decision owner:

Founder, head of brand / insights / growth / strategy, or operator directly
accountable for the budgeted demand-allocation decision.

Recommended first decision family:

Retail or channel expansion; launch / moratorium / reposition; inventory or
purchase-depth commitment. Tier/price change, pivot on a taste or preference
shift, and defend/hold against suspected manufactured or transient demand remain
eligible when they pass the same gates — where a false broad commit could
waste inventory or launch budget, misfire a retail window, create backlash or
churn, or surrender a real opportunity to noise.

Virality, creator attention, and trend coverage are trigger and
candidate-context ordering only; they count when they resolve into the first
decision family above. Buyer attributes such as funding status or
trend-darling visibility are neither qualifiers nor disqualifiers.

Selected product promise:

Orca reduces allocation risk before budget is committed by discriminating
durable from transient and manufactured demand on fused, integrity-labeled public evidence and
naming the evidence-supported action ceiling — monitor, probe, commit, hold, scale, avoid, or
reduce — plus what would change the answer.

Manual proof artifact:

A concise public-signal demand-allocation decision risk memo plus evidence
appendix (the buyer-proof packet's
`Public-Signal Demand-Allocation Decision Risk Memo`), produced manually for
one qualified live decision. The memo is the reasoning substrate and minimum
proof artifact; it must not depend on a dashboard, source system, collection
pipeline, source map, automation, or generalized data spine.

Premium artifact:

An executive-grade decision deck may be produced only after the memo and evidence appendix pass the same gates. The deck must be derived from the memo and appendix, preserve uncertainty and action-ceiling discipline, and serve qualified internal decision circulation rather than generic presentation interest.

The Product Proof Lead or designated operator produces the proof memo and, only if justified, the executive deck. The proof artifact should fit a bounded manual session under the accepted scope. If it materially exceeds that scope, classify the result as consulting-risk evidence and record it in the batch notes.

Proof-record home (bound 2026-06-12, gap DB-4, owner word): batch notes —
including readback records, near-misses, disqualifications, and
consulting-risk classifications — live at `docs/product/product_lead/` as
`orca_proof_batch_<n>_notes_v0.md` (one file per proof batch;
product_learning tier; retrieval-headered). Candidate-scan outputs are
research artifacts in `docs/research/` per the discovery brief's slot-fill
rule; they are inputs to slot selection, never proof records.

Core/satellite/bespoke boundary:

- Core is the repeatable decision spine.
- Satellites adapt the spine to buyer, industry, decision family, competitor set, and source families.
- Bespoke work is allowed only as bounded final adaptation. Overage or repeated custom work remains consulting-risk evidence unless tied to a repeatable decision family.

## Public-Signal Trust Handling

Use `.agents/workflow-overlay/product-proof.md` for trust-objection semantics.

Classify public-signal trust state as:

- `trust_open`: buyer already sees public signals as potentially relevant.
- `trust_objection`: buyer is skeptical but willing to evaluate evidence quality, examples, numbers, mechanism, case logic, proof memo, or decision artifact.
- `trust_refusal`: buyer states public signals cannot affect the decision regardless of evidence quality, examples, numbers, mechanism, case logic, or proof experience.

Only `trust_refusal` disqualifies or blocks memo production on public-signal trust grounds. `trust_objection` is proof material: capture it, test it, and read it back.

## Pull Standard

Buyer pull means observable budget-adjacent behavior, not approval language.

Strong pull includes one or more of:

- A real decision owner brings a live decision with timing, stakes, and budget consequence.
- The buyer gives context and asks for a memo by a decision deadline.
- The buyer schedules a readback with the decision owner or budget-adjacent stakeholders.
- The memo changes, narrows, delays, accelerates, or de-risks the allocation decision.
- The buyer circulates or uses the memo in an internal decision process.
- A qualified decision owner requests an executive deck for internal decision circulation tied to the live decision.
- The buyer asks for a second decision artifact, deeper cut, fixed-scope paid decision sprint, vendor setup, LOI, budget-owner meeting, procurement path, referral to another decision owner, or equivalent commercial next step.

Paid-decision-sprint-level pull means at least one commercial next-step signal: payment offer, fixed-scope sprint sponsorship, LOI, vendor/procurement path, budget-owner meeting, or referral to another live decision owner with stated urgency. Memo usefulness or deck interest alone is not enough.

Evidence of decision-judgment pull includes the buyer naming a specific action the memo helped avoid, narrow, reframe, sequence, or defend; asking for a second decision artifact in a different decision context; asking for an executive deck for internal decision circulation tied to a qualified live decision; or bringing a budget owner / decision owner into the next conversation. Requests only for more sources, deeper research, deck polish, or custom analysis on the same topic are not enough.

Weak or non-pull includes:

- Praise, curiosity, or "interesting" feedback without a live decision.
- Requests for a generic report, dashboard, data feed, or source volume rather than decision-risk reduction.
- Generic deck interest detached from a qualified live decision and internal decision use.
- A desire for free advice without internal decision use.
- Interest that cannot name a decision owner, timing, allocation risk, or commercial next step.

## Commercial Path Boundary

The first offer hypothesis is a fixed-scope paid decision sprint around one
qualified live decision and one bounded decision artifact. It is not proof of
willingness to pay, repeatability, or commercial readiness.

A retainer comes later only after recurring decision cadence and observable
buyer pull. Repeated ad hoc custom work without a repeatable decision family is
consulting-risk evidence, not graduation evidence.

## Kill Criteria

Kill or materially reframe the proof if the first qualified proof batch shows any of the following:

- Fewer than two qualified decision owners have live decisions in the selected segment and decision family.
- Buyers treat the memo as generic research rather than decision-risk reduction.
- No delivered memo changes or sharpens a real allocation decision.
- Buyers will not use or circulate the memo in the decision process.
- Buyers show `trust_refusal`, or the proof memo fails to move a `trust_objection` enough for public-signal evidence, source cleanliness, and uncertainty boundaries to affect the decision.
- Value depends on bespoke consulting labor with no repeatable decision pattern.
- No buyer requests a fixed-scope paid decision sprint or equivalent commercial next step after useful memo feedback.
- The memo requires software, dashboards, collection pipelines, source maps,
  automation, data science, integrations, or private/internal data to be
  credible.

A single strong candidate may justify a follow-up conversation, but not graduation or proof-boundary acceptance.

## Graduation Criteria

Graduate to product-bet planning only if the proof produces all of the following:

- Repeat means: At least two independent qualified decision owners in the same buyer segment and decision family produce Grade A or Grade B results, without reusing the same buyer or same internal decision.
- At least two qualified decision owners use a manual Orca memo in a live allocation decision.
- At least one buyer shows fixed-scope paid-decision-sprint-level pull or equivalent commercial commitment.
- The memo plus evidence appendix format remains sufficient without software, dashboards, source systems, source maps, or automation.
- Any executive deck layer is derived from the memo and appendix and does not become bespoke presentation consulting.
- The buyer values Orca's decision judgment and action-ceiling discipline, not merely custom research labor.
- The non-claims remain intact: no buyer validation, feature readiness, implementation readiness, or commercial readiness is asserted.

Feature planning remains later than product-bet planning. It may be considered only after accepted product proof evidence, explicit owner authorization, and a bounded feature-planning turn. This charter does not route to feature planning.

## Next Docs-First Product Work

Customer discovery may proceed as docs-first product-fit testing under this charter after owner acceptance of the proof boundary.

First memo production may proceed only for a named qualified buyer with a live
30-90 day consumer-demand allocation trigger (families per the first proof
lane), using the manual proof artifact in
`orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md` (path updated
2026-06-12). Executive deck production may
proceed only after the memo and evidence appendix pass the same gates and the
deck is tied to a qualified live decision use.

No implementation, automation, source-system design, data-spine design, dashboard design, source-map design, commits, pushes, PRs, or feature planning may proceed from this charter.

## Not-Proven Boundaries

This charter does not prove:

- Buyer validation.
- External willingness to pay.
- Repeatable demand.
- Procurement feasibility.
- ROI.
- Retention, renewal, or expansion.
- Product readiness.
- Feature readiness.
- Implementation readiness.
- Commercial readiness.
- Core Spine v0 validation.
- Source-system feasibility, data rights, or runtime feasibility.
