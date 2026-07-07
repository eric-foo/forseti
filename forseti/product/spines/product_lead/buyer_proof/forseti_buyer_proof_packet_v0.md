# Forseti Buyer Proof Packet v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: First buyer-proof packet for testing Forseti's public-signal decision artifact promise.
use_when:
  - Running customer discovery for Forseti buyer proof.
  - Deciding whether first memo production, executive deck production, proof kill, or proof graduation may proceed.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/product-proof.md
  - docs/decisions/forseti_icp_wedge_consumer_demand_first_v0.md     # current wedge authority (supersedes pricing-first)
  - forseti/product/spines/product_lead/proof_charter/forseti_product_proof_lead_charter_v0.md
  - docs/decisions/forseti_product_thesis_consumer_demand_v0.md      # controlling thesis (supersedes turn_08; ratified 2026-06-12)
input_hashes:
  - path: docs/decisions/turn_08_product_thesis_v0.md
    sha256: 822653A241CF84675A3F07F695BA0ED3BFACC230F7F13AA47A4649B5DB2CD7E6
  - path: docs/product/core_spine_v0_method_validation_replay_packet_v0.md
    sha256: 8CB2D592D49C1C10DD5DD91A070D2800AF61DFDFC67D7C56A404A75F2EEA2161
  - path: docs/product/orca_product_lead_first_icp_wedge_decision_v0.md
    sha256: B570672CD7F31B2D78F9DC5E851C3AEDA7030A56ECF2CDC6733E0191ED3DDC23
    note: SUPERSEDED as wedge authority by docs/decisions/forseti_icp_wedge_pricing_first_v0.md (reread-required)
  - path: docs/decisions/forseti_icp_wedge_pricing_first_v0.md
    sha256: REREAD_REQUIRED
  - path: docs/review-outputs/adversarial-artifact-reviews/orca_ai_exposed_icp_refinement_adversarial_review_v0.md
    sha256: 648864959A13143F9C0C4DF5A8553D5F4BD0D7608FF09ADE6632938D748CADBA
```

## Status And Verdict

Status: `PROPOSED_BUYER_PROOF_PACKET_V0`

Product planning verdict: `NEEDS_CUSTOMER_DISCOVERY`.

Readiness verdict: `ready for product-fit testing`; not ready for product-bet planning until the graduation criteria in this packet are met and accepted.

Feature planning verdict: not ready. This packet does not route to feature planning.

## Consumer-Demand Refinement (2026-06-12, ratified cascade)

This packet's first-proof framing is RE-TARGETED by the owner-ratified
consumer-demand direction. Controlling authority:
`docs/decisions/forseti_product_thesis_consumer_demand_v0.md` (thesis,
`OWNER_LOCKED` 2026-06-12) and
`docs/decisions/forseti_icp_wedge_consumer_demand_first_v0.md` (wedge,
`OWNER_LOCKED_DIRECTION` 2026-06-12), which supersede
`docs/decisions/forseti_icp_wedge_pricing_first_v0.md` as first-proof authority
(pricing retained as engine application + re-entry candidate). Earlier pinned
`input_hashes` / wedge references are superseded — reread-required. Deltas:

- Proof subject: beauty consumer-demand allocation decisions (DecisionEvent) —
  durable / transient / manufactured demand (TrendVector) discrimination (monitor / probe /
  commit / hold / scale / avoid / reduce), per the thesis's central read.
- Substrate HARD GATE RE-DERIVED (replaces "competitor prices clean, reviews
  confirmatory-only," which was derived for a pricing read and does not
  transfer): see "Demand-Substrate Hard Gate" below.
- Capture risk posture (owner ask-1 amendment, 2026-06-12): measured ToS risk
  is accepted; absurd-level approaches (e.g., Bright-Data-style industrial
  scraping) are rejected. Per-venue route bindings stay capture-lane-owned.
- Buyer-proof remains gated exactly as before: qualified live decision +
  memo + readback; the no-buyer-contact-before-full-spine-MVP gate is
  UNTOUCHED (owner ask 4, 2026-06-12: gate stays closed); publishing
  backtest receipts is door-opening content at `product_learning` tier,
  never buyer proof.
- Named pivot condition (from the wedge record): if batch-1 distillation
  shows demand reads landing confirm-only or persistently out-of-band, the
  first proof re-forms around the lower-bar screen (fund-first and/or
  org-motion-led shortlist) and this packet's operator-first targeting is
  void pending re-derivation.

The executed `direction_change_propagation` receipt for this ratification
event lives in `docs/decisions/forseti_product_thesis_consumer_demand_v0.md`
("Doctrine-Change Propagation — Executed"). Applied here by the ratification
cascade; the live text reflects the applied deviations.

The substantive content below (rubric grades, trust handling, pull standard,
kill and graduation structure, exclusions, and all non-claims) is SURGICALLY
ALIGNED to the refinement and unchanged in substance.

## Commercial Target Selection Update (2026-06-16)

Owner direction confirms the first commercial target for this packet as
US-market tractioned indie/DTC beauty or personal-care operators with a named
decision owner and a live 30-90 day consumer-demand allocation decision.

The proof batch should bias first toward retail/channel expansion,
launch/reposition, and inventory or purchase-depth commitment because those
decisions have concrete allocation stakes, short timing, and a high likelihood
that public creator/social/review/search/retail signals remain material before
internal data is conclusive. Tier/price, taste-shift pivot, and defend/hold
against suspected transient or manufactured demand remain eligible when they
pass the same gates.

Retailer/category teams are deferred, not killed forever: their proprietary
sell-through, basket, loyalty, and vendor data often makes the public-signal
increment harder to prove in the first 2-3 month window. If the operator-first
proof fails for decision-use reasons, the fallback ladder remains the wedge
record's rule: re-form toward consumer fund screen and then PE/family-office
diligence by owner decision at kill time. Agencies and incubators may later
serve as routes to brand decision owners, but their interest is not buyer proof
unless the accountable brand decision owner enters the memo/readback loop.

Customer-provided proprietary data may later improve accuracy by letting Forseti
compare the public-signal judgment (Reading) against the buyer's internal demand
evidence. This packet does not authorize that intake. For this first proof,
requiring private/internal data, data science, dashboards, integrations, or
source-system buildout before the public memo is useful remains a disqualifier.
Public evidence relevance is treated as strong prior plausibility, not as
buyer-proof evidence by itself.

## Proof Standard

This packet tests one narrow first-proof claim:

A real decision owner at a US-market tractioned indie/DTC beauty /
personal-care brand (Brand) facing a live 30-90 day consumer-demand allocation
decision — where internal data is not conclusive — will use a Forseti decision
artifact to reduce allocation risk before committing inventory,
retail/channel, launch, or pricing budget. Forseti
creates that artifact by capturing, cleaning, integrity-labeling, classifying
(costly behavior, never engagement/resonance volume alone), and constraining messy
public demand signals — reviews, forums, search interest, retail presence —
fused with org-motion corroboration at brand and parent level (Org), into
inspectable decision evidence with an explicit action ceiling. The engine is
outside-in market & competitive intelligence; beauty consumer-demand
allocation is its first application.

Minimum viable artifact: a manual decision memo (Memo) plus evidence appendix.

Premium buyer-facing artifact: an executive-grade decision deck derived from the memo and evidence appendix.

Commercial next-step hypothesis: a fixed-scope paid decision sprint or equivalent budget-adjacent commitment. This is a hypothesis to test, not validated commercial readiness.

The proof is manual and docs-first. It does not authorize software implementation, automation, source systems, dashboards, collection pipelines, source maps, data-spine designs, packages, tests, commits, pushes, PRs, or feature planning.

## Demand-Substrate Hard Gate (re-derived 2026-06-12)

The pricing wedge's gate ("clean substrate = competitor price pages; reviews
confirmatory-only") protected a read whose differentiated half sat on one
clean venue. The demand wedge's differentiated read sits BY DESIGN on the
hostile, manipulable demand substrate, so the gate re-derives as a fusion and
integrity rule instead of a venue allowlist:

- **Independence = de-correlation by origination, not a raw venue count.** A
  qualified read requires demand signal from **effectively-independent
  demand-venue origins (Venue)**, so no single origin's bias or manipulation carries the
  answer. An "independent venue family" means traceable to a *distinct
  origination event*. Per the venue-chain (community originates → trade press
  launders → BoF/WWD terminate), signals on the same `derived_from` chain are
  **one** family; independence requires **no shared origination ancestry** —
  collapse to one family any signals that derive from each other **or** that
  trace to a common upstream origination event or a shared coordinated
  origination. Pairwise "neither derives from the other" is **insufficient** (two
  laundered siblings of one event satisfy it while violating independence).
  *(AR-01)*
- **Verb-tiered by commitment, not a hard count or verb label.** The bar is
  **enough effectively-independent origins for the commitment claimed**, tiered
  by *commitment/reversibility*, not verb name: one origin (or
  laundered/shared-origination copies of one) authorizes only **low-commitment,
  reversible responses** (monitor / probe / hold; a watchful or low-cost posture); **any
  material or irreversible commitment — commit or scale — requires ≥2 independent
  origins that converge.** This is tiered by commitment/reversibility, not verb
  name: a costly or scaling position is a material action and needs the ≥2 bar. *(AR-02)*
- **Two distinct maintained card sets.** Maintained cards split into **G1
  demand-family cards** (today only **forums/community** is sourced;
  review-surface and search-interest are **unsourced gaps**, owner-owned) and
  **G4 org-motion corroboration cards** (including **retail presence**). Retail
  presence is a **G4 corroboration card** — preserved as G4 evidence,
  **excluded from the G1 independent-origin count**; it is neither a deprecated
  label nor a sourcing gap. *(AR-04)*
- **Manipulated sentiment is admissible input; floor vs ceiling ordering.**
  Manipulable sources are admitted as *sentiment input*. **Costly behavior (G2)
  clears the FLOOR** (is there real demand at all?); **divergence constrains the
  CEILING** (how bold). Converted costly behavior can clear the floor while
  divergence caps the verb. **Defeater:** if the divergence pattern indicates the
  costly-behavior instance is itself likely manufactured/coordinated (e.g., the
  only costly signal sits inside the same coordinated layer that divergence
  flags), divergence **defeats the floor**, not merely the ceiling. Divergence
  (`diverges_from`) is preserved as signal, never averaged away. *(AR-03)*
- **Demand-state labels are not strength tiers.** The gate first asks whether the
  candidate has real, gradeable demand substrate at all. Weak, attention-only,
  engagement-only, or resonance-only input fails or holds; it is not transient
  demand. Public engagement should still be read as qualitative resonance weight
  by default; it just does not clear the costly-behavior floor. A durable label
  is a forward persistence projection carried to Judgment/C3 with a named basis;
  observed persistence is one possible basis, not the definition.
- **Costly-behavior floor (clears G2), with a "gradeable" definition.** A
  costly-behavior instance is **gradeable** when it is (a) **attributable to
  identifiable buyer actions**, not aggregate mood/attention; (b) **statable with
  a direction and rough magnitude**; (c) **corroborable/checkable**, not a single
  unverifiable rumor. Floor = **≥1 gradeable** costly-behavior instance (payment,
  switching/dupe-adoption, workaround/stockpiling/secondary-market premium,
  churn, durable buyer pressure) **evidenced in ≥1 qualifying demand-venue
  family**, distinguishable from attention volume. *(AR-05; full numeric
  sufficiency deferred — P4-B; the single-instance interim floor is an
  owner-accepted calibration risk — see DLF-01.)*
- **Floor vs ceiling; evidence vs corroboration.** The floor needs the instance
  **evidenced in ≥1 qualifying family**; a **second independent family is not
  required at the floor** but **raises the verb ceiling** (per the verb-tiering
  above). "Corroboration" = the ≥2-independent-origin step that raises the
  ceiling, **not** a floor requirement. *(AR-06)*
- **Ceiling tiering:** the strength/amount of costly behavior scales the action
  ceiling — one gradeable instance → hold/low-commitment; a corroborated pattern
  across ≥2 independent origins → material action.
- **Guard:** absence of demand ("velocity miss," "low sales," falling
  engagement) is **not** a G2 pass.
- Every venue's evidence carries integrity labels (artificial-amplification
  risk, incentive distortion, copied/coordinated) before it may enter the
  fused read. Reviews ARE admissible — as one fused venue, flagged for
  J-curve self-selection bias and FTC 16 CFR 465 pollution — never as the
  sole basis. This knowingly prices in the bias risk the pricing un-flip
  demoted reviews for; multi-venue fusion + integrity judgment + batch-1
  calibration are the mitigations, and batch-1 measures whether they hold.
- Org-motion (hiring composition + headcount, brand AND parent) is
  CORROBORATION inside the artifact — divergence reads (demand up +
  staffing up / demand up + staffing flat / staffing up + demand flat) are
  the premium element — never a standalone product, never a sold or externally
  published person-level surface (internal wind-caller (WindCaller) calibration is the sole
  bounded exception per `docs/decisions/wind_caller_calibration_carveout_v0.md`;
  that carve-out is internal-only and does not change this artifact's external boundary).
  Routes follow the owning capture decisions (official/manual/entitled/
  archive today); the owner's measured-ToS-risk posture (ask-1 amendment,
  2026-06-12) accepts measured risk and rejects absurd-level approaches
  (e.g., Bright-Data-style industrial scraping). Route-binding changes are
  capture-lane decisions, never per-proof stretches.
- **Gate outcome by tier, not a single hard count.** The candidate **FAILS the
  gate** only when the floor cannot be cleared — **no gradeable costly-behavior
  instance** in any qualifying demand-venue family (engagement/attention/resonance
  volume alone never clears it), or **no qualifying demand-venue origin at all** — in
  which case disqualify or hold, and do not run an engagement/resonance-only memo. With the
  floor cleared on **one** independent origin, the read is **admissible but
  capped at hold / low-commitment**; **≥2 converging independent origins** are
  required before any material or irreversible commitment. A single clean origin
  is therefore a **ceiling cap, not an automatic gate failure**.

## Evidence Mode And Source Boundary

Profile: `standard`.

Subagents launched: 3.

Evidence mode: delegated advisory directional, adversarial, and grounding lanes. Each lane was advisory input only; none was a verdict, implementation authority, or proof of readiness.

Source mode: local Forseti authority and repo-visible product artifacts only. No public web research was used. Archived contaminated replay outputs were not read.

## Target Buyer (Buyer)

Primary segment:

US-market tractioned indie/DTC beauty / personal-care brands facing a live
30-90 day consumer-demand allocation decision — prioritizing retail/channel
expansion or contraction, launch / moratorium / reposition, and inventory or
purchase-depth commitment — where internal data is not conclusive. Tier/price
change, pivot on a taste or preference shift, and defend/hold against
suspected transient or manufactured demand remain eligible when they satisfy the
same gates.
Geography: US-market first proof per the thesis geography doctrine
(2026-06-12); non-US candidates route to the owner or defer.

A qualified target must pass the Demand-Substrate Hard Gate above (enough
effectively-independent demand-venue origins for the commitment claimed — one
origin caps at hold/low-commitment, ≥2 converging independent origins for
material action; a gradeable costly-behavior instance clearing the floor;
integrity labels applicable) and have a named decision owner who can identify a
concrete inventory, retail-commitment, launch-budget, backlash/churn, or
delayed-capture consequence.

If results are mixed, diagnose the demand decision families separately
(retail/channel expansion vs launch/reposition vs inventory/purchase-depth vs
tier/price vs defend/hold) before treating the family as repeatable or
non-repeatable.

Primary decision owner:

Founder, head of brand / insights / growth / strategy, or operator directly
accountable for the budgeted demand-allocation decision.

Economic context:

The decision should have meaningful allocation risk: retail or channel
commitment, launch spend, inventory commitment, purchase depth, replenishment,
tier/price change, customer backlash risk, churn risk, or delayed capture of a
real opportunity.

Disqualifiers:

- No named decision owner.
- Budget-adjacent champion cannot surface a named decision owner for the memo step.
- No live 30-90 day consumer-demand allocation decision in the families above.
- No budget or allocation consequence.
- Candidate fails the Demand-Substrate Hard Gate (no gradeable costly-behavior
  instance clearing the floor — engagement/resonance-volume-only, attention-only,
  or resonance-only signal;
  no qualifying demand-venue origin at all; or signal obtainable only through a
  route outside the capture lane's current bindings or only at absurd risk level
  — route expansion is a capture-lane decision, not a per-candidate stretch). A
  single independent origin is **not** a gate failure: it is admissible but caps
  the read at hold / low-commitment (≥2 converging independent origins are
  required for material action).
- Buyer wants only generic research, source volume, dashboard access, trend
  feeds, or a market-monitoring feed.
- Buyer requires private/internal data, data science, dashboards,
  integrations, or automated collection before a manual public-signal memo can
  be useful.
- Categorical trust refusal: buyer says public-signal evidence cannot affect this decision regardless of evidence quality, explanation, examples, numbers, case logic, or proof memo.
- Buyer attributes such as funding status, trend-darling visibility, or
  creator attention are neither qualifiers nor disqualifiers. They may be
  recorded as context, but cannot replace the decision owner, live decision,
  consequence, substrate gate, paid-first condition, trust-refusal test, or
  consulting-risk test.

## Live Decision Trigger

The proof should start only when at least one of these triggers is present:

- A retail or channel window (retailer rollout, shelf reset, marketplace
  expansion) forces a commit/hold decision.
- A virality spike, creator-driven surge, or social moment raises a
  durable-vs-transient question before inventory or launch commitment.
- A taste/preference shift (ingredient, format, claim trend) puts a
  reformulation, reposition, or launch decision in play.
- A planned launch, moratorium, tier/price change, or SKU (Product) rationalization is
  being debated and internal data is inconclusive.
- Suspected manufactured or coordinated demand (the brand's own or a
  competitor's) creates a defend/hold decision.

The trigger must be real enough that the buyer can say what decision is pending, who owns it, what budget or allocation is at stake, and when the decision must be made.

Virality, creator attention, and trend coverage are trigger and
candidate-context ordering only. They are not buyer filters, not buyer
validation, and not evidence of durable demand — the fused,
costly-behavior-anchored read decides. Engagement/resonance volume alone does not become
transient demand; it should be read as qualitative resonance weight, but it caps
the action ceiling unless gradeable costly behavior and origin integrity clear
the gate.

## Forseti Promise

Forseti helps the decision owner reduce allocation risk before committing budget
by discriminating projected durable demand from strong current-window transient
demand and manufactured demand on fused, integrity-labeled public evidence.

For this first proof, the promise is not "Forseti predicts the trend." The promise is narrower:

Forseti identifies the evidence-supported action ceiling for the live demand
decision — monitor, probe, commit, hold, scale, avoid, or reduce — states what the public
signal can and cannot support, and names what would change the answer.

**Never-a-feed invariant (2026-06-14):** every output is a calibrated decision
with an action ceiling — **never a feed or stream**. This is the structural lock
that keeps Forseti off the "monitoring-only pull" kill (below) and out of the
social-listening category, including when a read is monitored over time
(transient → earn-durable): recurring engagement is sold as recurring
*decisions*, never as a monitoring feed.

## Manual Proof Artifact

Artifact name: `Public-Signal Demand-Allocation Decision Risk Memo`.

Minimum sufficient artifact:

A concise manual memo plus evidence appendix for one qualified live decision. The memo is the reasoning substrate and proof gate. It should be good enough for a buyer readback before any premium deck is produced.

Premium artifact:

An executive-grade decision deck may be produced only after the memo and evidence appendix pass the same proof gates. The deck must be derived from the memo and appendix, preserve uncertainty and action-ceiling discipline, and be suitable for internal decision circulation by the buyer.

The Product Proof Lead or designated operator produces the proof memo and, only if justified, the executive deck. The proof artifact should fit a bounded manual session under the accepted scope. If it materially exceeds that scope, classify the result as consulting-risk evidence and record it in the batch notes.

Core/satellite/bespoke boundary:

- Core is the repeatable decision spine.
- Satellites adapt the spine to buyer, industry, decision family, competitor set, and source families.
- Bespoke work is allowed only as bounded final adaptation. Overage or repeated custom work remains consulting-risk evidence unless it points to a repeatable decision family.

## Public-Signal Trust Handling

Use `.agents/workflow-overlay/product-proof.md` for trust-objection semantics.

Classify public-signal trust state as:

- `trust_open`: buyer already sees public signals as potentially relevant.
- `trust_objection`: buyer is skeptical but willing to evaluate evidence quality, examples, numbers, mechanism, case logic, proof memo, or decision artifact.
- `trust_refusal`: buyer states public signals cannot affect the decision regardless of evidence quality, examples, numbers, mechanism, case logic, or proof experience.

Only `trust_refusal` disqualifies or blocks memo production on public-signal trust grounds. `trust_objection` is proof material: capture it, test it, and read it back.

Recommended memo and evidence appendix shape:

1. Decision question and live trigger.
2. Decision owner, timing, and allocation risk.
3. Fused demand-signal synthesis across the qualifying venue families, with
   costly-behavior classification stated per signal.
4. Integrity labels and signal-quality caveats (artificial-amplification
   risk, incentive distortion, copied/coordinated, venue bias flags).
5. Org-motion corroboration at brand and parent level, and the divergence
   read where the layers disagree.
6. Competitor and category movement relevant to the decision.
7. Valid action ceiling (monitor / probe / commit / hold / scale / avoid / reduce) and the
   unsafe overclaims explicitly declined.
8. Decision options mapped to the ceiling, with what would change the answer.
9. Evidence appendix with provenance-backed citations.
10. Explicit non-claims and tier label (`product_learning` cap).

Recommended executive deck shape, if the premium layer is produced:

1. Decision question and recommendation verb.
2. Executive action ceiling: monitor, probe, commit, hold, scale, avoid, or reduce.
3. What public signals can and cannot support.
4. Source-backed signal synthesis.
5. Buyer, user, developer, partner, or ecosystem objection patterns.
6. Competitor or category movement relevant to the decision.
7. Options, risks, and decision deadline.
8. Evidence appendix pointer and explicit non-claims.

Intentionally manual:

- Source selection.
- Source reading.
- Evidence extraction.
- Signal-quality judgment.
- Memo writing.
- Buyer readback.
- Pull classification.

Deferred or excluded:

- Dashboards.
- Source systems.
- Collection pipelines.
- Source maps.
- Data-spine designs.
- Automated scoring.
- Generalized memo generation.
- CRM or sales automation.
- Feature planning.
- Implementation planning.

## Evaluation Rubric

Grade A: strong pull.

- Buyer has a named live decision with timing and allocation consequence.
- Buyer accepts the manual memo and evidence appendix as decision-relevant.
- The memo changes, narrows, delays, accelerates, defends, reframes, or de-risks the decision.
- Buyer uses or forwards the memo internally, or a qualified decision owner requests an executive deck for internal decision circulation tied to the live decision.
- Buyer asks for a fixed-scope paid decision sprint, second decision artifact, budget-owner meeting, vendor setup, LOI, procurement path, referral, or equivalent commercial next step.

Paid-decision-sprint-level pull means at least one commercial next-step signal: payment offer, fixed-scope sprint sponsorship, LOI, vendor/procurement path, budget-owner meeting, or referral to another live decision owner with stated urgency. Memo usefulness or deck interest alone is not enough.

Grade B: useful but not commercial pull.

- Buyer has a live decision and finds the memo useful.
- Memo sharpens the decision but does not produce a commercial next step.
- Buyer asks for more thinking, but not with budget-adjacent behavior.

Grade C: weak signal.

- Buyer praises the work but cannot name a decision use.
- Buyer treats the memo as market research.
- Buyer asks for more source volume, dashboards, or monitoring instead of decision-risk reduction.
- Buyer does not involve the actual decision owner.

Grade D: kill or reframe signal.

- No live decision exists.
- Buyer shows `trust_refusal`, or the proof memo fails to move a `trust_objection` enough for public-signal evidence to affect the decision.
- The memo cannot reduce allocation risk without private data or software.
- Buyer interest depends on bespoke consulting with no repeatable pattern.
- No fixed-scope paid decision sprint or equivalent commercial next step appears after useful feedback.

## Buyer Pull

Behavior that counts as pull:

- Buyer brings a real decision rather than responding to a hypothetical concept.
- Buyer gives decision context, timing, and stakes.
- Buyer requests delivery by a decision deadline.
- Buyer schedules a readback with decision or budget-adjacent stakeholders.
- Buyer uses the memo in the decision process.
- Buyer asks for a second memo, executive deck for internal decision circulation, or deeper cut on the same decision family.
- Buyer offers payment, pilot sponsorship, LOI, vendor setup, procurement path, budget-owner meeting, or a referral to another live decision owner.

Evidence of decision-judgment pull includes the buyer naming a specific action the memo helped avoid, narrow, reframe, sequence, or defend; asking for a second decision artifact in a different decision context; asking for an executive deck for internal decision circulation tied to a qualified live decision; or bringing a budget owner / decision owner into the next conversation. Requests only for more sources, deeper research, deck polish, or custom analysis on the same topic are not enough.

Behavior that does not count as pull:

- Compliments.
- Curiosity.
- Generic "send me the deck" interest detached from a qualified live decision and internal decision use.
- Requests for a dashboard before any decision use.
- Interest from someone without decision ownership or budget adjacency.
- Desire for generic research or source volume.
- Internal Client 0 method validation.

## Commercial Path Boundary

The first offer hypothesis is a fixed-scope paid decision sprint around one
qualified live decision and one bounded decision artifact. It is not proof of
willingness to pay, repeatability, or commercial readiness.

A retainer comes later only after recurring decision cadence and observable
buyer pull. Repeated ad hoc custom work without a repeatable decision family is
consulting-risk evidence, not graduation evidence.

## Suggested Proof Batch

Run a small manual proof batch before any product-bet or feature-planning claim:

1. Qualify 6-8 target decision owners, or budget-adjacent champions who can surface a named decision owner for the memo step.
2. Select up to 3 buyers with live consumer-demand allocation decisions
   (families per Target Buyer).
3. Produce one manual memo plus evidence appendix per selected buyer.
4. Produce an executive deck only when the memo and evidence appendix pass the same gates and the deck has a live decision-circulation use.
5. Run a live readback for each memo, and deck readback only if a deck is produced.
6. Record decision use, risk reduction, trust objections, commercial next step, and anti-pull.
7. Classify each result using the rubric above.

These numbers are planning defaults, not validation proof. They should be adjusted only if owner acceptance changes the proof batch.

The memo/readback stage requires a named decision owner or budget-accountable decision lead.

Suggested buyer readback questions:

- What action would this memo help you avoid, narrow, reframe, sequence, or defend?
- What would you do differently if this memo were in the decision packet?
- Would an executive deck help internal decision circulation, and if so who would use it for this live decision?
- Who owns the budget or accountability for this decision, and should they be in the readback?
- What commercial next step, if any, would be justified if another memo reached this bar?
- Which part felt like decision judgment rather than custom research labor?

## Kill Criteria

Kill or reframe the proof if any of these conditions hold after the first proof batch:

- Fewer than two qualified decision owners have live decisions in the selected segment and decision family.
- No delivered memo is used in a real allocation decision.
- Buyers consistently classify the memo as interesting research rather than decision support.
- Buyers show `trust_refusal`, or the proof memo fails to move `trust_objection` enough for the public-signal basis, source cleanliness, uncertainty framing, or action-ceiling discipline to affect the decision.
- Buyers require private/internal data, data science, dashboards, source
  systems, collection pipelines, source maps, integrations, automation, or
  data-spine design before the memo can be useful.
- The strongest buyer ask is generic market monitoring, not allocation-risk reduction.
- No buyer shows fixed-scope paid-decision-sprint-level pull or equivalent commercial next step after useful memo feedback.
- The work only succeeds as bespoke consulting and does not repeat around a decision family.
- The demand read cannot reach decision-grade within the capture lane's bound
  routes, or would require an absurd-risk capture approach (owner-rejected
  level, e.g., Bright-Data-style industrial scraping) — a boundary kill;
  route expansion is a capture-lane decision, never a per-proof stretch.

On kill, the re-entry disposition is the wedge record's rule as amended
2026-06-12: re-form toward the harder / more-profitable end of the buyer
ladder (fund screen, PE/family-office diligence path), owner-decided at kill
time; pricing-first is not a re-entry candidate.

A single strong candidate may justify a follow-up conversation, but not graduation or proof-boundary acceptance.

## Graduation Criteria

Graduate to product-bet planning only if all of the following are met and accepted:

- Repeat means: At least two independent qualified decision owners in the same buyer segment and decision family produce Grade A or Grade B results, without reusing the same buyer or same internal decision.
- At least two qualified decision owners use a manual Forseti memo in a live allocation decision.
- At least one buyer shows fixed-scope paid-decision-sprint-level pull or equivalent commercial commitment.
- The memo plus evidence appendix format is repeatable enough to test again without building software.
- Any executive deck layer is derived from the memo and appendix and does not become bespoke presentation consulting.
- The strongest buyer value is Forseti's decision judgment and action-ceiling discipline, not merely custom research labor.
- The proof does not require dashboards, source systems, collection pipelines, source maps, automation, or data-spine design.
- Non-claims remain intact.

Feature planning may be considered only after product-bet planning or equivalent owner-accepted proof evidence, plus a later explicit feature-planning authorization. This packet alone does not authorize feature planning.

## What Must Not Be Built Yet

Do not build:

- Source systems.
- Dashboards.
- Collection pipelines.
- Source maps.
- Data-spine designs.
- Scoring engines.
- Databases.
- APIs.
- Packages.
- Tests.
- Automation.
- CRM workflows.
- Generalized memo tooling.
- User interfaces.
- Feature plans.
- Implementation plans.

Do not create buyer-validation, feature-readiness, implementation-readiness, or commercial-readiness claims.

## Product Artifact Impact

Impact classification: `artifact-as-proof` and `artifact-required`.

This packet is required before first buyer proof because it binds the proof claim, target buyer, decision family, minimum memo artifact, evidence appendix, premium executive deck layer, rubric, kill criteria, graduation criteria, exclusions, and non-claims.

The later manual decision memo plus evidence appendix is the minimum artifact-as-proof. It should be produced only after a qualified buyer and live decision trigger are selected. The executive deck is buyer-facing packaging derived from that substrate, not separate proof by itself.

## Not-Proven Boundaries

This packet does not prove:

- Buyer validation.
- External willingness to pay.
- Paid pilot conversion.
- Repeatable demand.
- Procurement feasibility.
- Retention, renewal, or expansion.
- ROI.
- Product readiness.
- Feature readiness.
- Implementation readiness.
- Commercial readiness.
- Core Spine v0 validation.
- Source-system feasibility.
- Data rights.
- Runtime feasibility.

The accepted Core Spine v0 replay packet remains bounded method signal only.

## May Proceed

Customer discovery may proceed under this packet as docs-first product-fit testing after owner acceptance of the proof boundary.

First memo production may proceed only after a named qualified buyer and live decision trigger are selected. It must use a manual decision memo and evidence appendix as the minimum artifact. Executive deck production may proceed only after the memo and evidence appendix pass the same gates and the deck is tied to a qualified live decision use.

No product-bet planning, feature planning, implementation, source-system design, automation, commits, pushes, PRs, or commercial-readiness claim may proceed from this packet.

## Blockers

Authority blocker: none for writing these docs-first product artifacts under `docs/product/`.

Product fit gaps:

- No external buyer has been qualified yet.
- No live decision trigger has been selected yet.
- No manual memo has been produced or read back yet.
- No buyer pull, fixed-scope paid-decision-sprint intent, or equivalent commercial next step has been observed yet.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The Demand-Substrate Hard Gate's independence test moved from a raw "≥2
    venue families" count to de-correlation-by-origination plus verb-tiering by
    commitment (one independent origin → hold/low-commitment; ≥2 converging
    independent origins → material/irreversible commitment); retail presence is
    reclassified as G4 org-motion corroboration, excluded from the G1
    independent-origin count; and the G2 costly-behavior floor is set to ≥1
    gradeable instance evidenced in ≥1 qualifying demand-venue family, with
    floor-vs-ceiling ordering, a divergence defeater, and ceiling tiering. The
    discovery brief's qualification objective #3 and slot-table column carry the
    same reword. This is the live apply of the owner-ratified (2026-06-13)
    P2/P3/P4 amendments; the wording is transcribed from the ratified proposal,
    not re-authored.
  trigger: product_doctrine
  controlling_sources_updated:
    - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md
    - forseti/product/spines/product_lead/icp_wedge/orca_discovery_consumer_demand_target_selection_brief_v0.md
    - forseti/product/spines/scanning/admissibility_checkability/orca_demand_gate_definition_closures_proposal_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/foundation/demand_read_taxonomy/forseti_demand_read_taxonomy_v0.md
    - forseti/product/spines/product_lead/proof_charter/forseti_product_proof_lead_charter_v0.md
    - forseti/product/spines/product_lead/offer/forseti_offer_hypothesis_v0.md
    - forseti/product/spines/product_lead/offer/orca_offer_hypothesis_consumer_demand_revision_v0.md
    - forseti/product/spines/foundation/demand_read_taxonomy/forseti_demand_read_taxonomy_adjudication_v0.md
    - forseti/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_consumer_demand_revision_v0.md
    - docs/prompts/product-planning/demand_substrate_gate_paper_check_commission_prompt_v0.md
  intentionally_not_updated:
    - path: forseti/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md
      reason: >
        Already classifies retail placements as supply-side org motion
        (corroboration), consistent with the G4 reclassification (lines 104-106);
        cite, no edit — confirmed against live text.
    - path: forseti/product/spines/product_lead/proof_charter/forseti_product_proof_lead_charter_v0.md
      reason: >
        Restates the gate parenthetically as "at least two independent venue
        families" (line 140). Outside this owner-gated apply's authorized scope
        (the apply was scoped to the buyer-proof packet + discovery brief, not a
        repo-wide gate-wording sweep — the packet's "apply ballooning" drift
        cue). FLAGGED residual reconcile target for a separate owner-decided
        pass; recorded here, not silently left consistent.
    - path: forseti/product/spines/product_lead/offer/forseti_offer_hypothesis_v0.md
      reason: >
        Qualification question restates "at least two independent venue families"
        (line 496); same FLAGGED residual reconcile, outside authorized scope.
    - path: forseti/product/spines/product_lead/offer/orca_offer_hypothesis_consumer_demand_revision_v0.md
      reason: >
        Offer-hypothesis revision restates the same clause (line 167); FLAGGED
        residual reconcile, outside authorized scope.
    - path: forseti/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_adjudication_v0.md
      reason: >
        Adjudication record restating the prior gate wording (line 138);
        historical adjudication context; FLAGGED residual, outside scope.
    - path: forseti/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_consumer_demand_revision_v0.md
      reason: >
        Prior revision document feeding orca_buyer_proof_packet_v0 (lines
        124/169); not the live instrument edited here; FLAGGED residual, outside
        scope.
    - path: docs/prompts/product-planning/demand_substrate_gate_paper_check_commission_prompt_v0.md
      reason: >
        Separate completed paper-check commission (a different work unit the
        handoff flags do-not-conflate); references "≥2 independent venue
        families" walks; not the live gate instrument, not edited here.
  stale_language_search: >
    rg -ni "at least two independent venue|two independent venue families|two
    clean-enough venue|≥2 required|single-venue-only" docs
  stale_language_search_result: >
    Executed 2026-06-14 after this apply (a replacement edit, so the search is
    required — not purely additive). The two edited live instruments
    (orca_buyer_proof_packet_v0.md, orca_discovery_consumer_demand_target_selection_brief_v0.md)
    no longer match — the old "≥2 venue families / single-venue-only" wording is
    gone from both. Remaining matches are: the ratified proposal quoting the old
    qual-#3 text it amends (intentional, inside Amendment ③), and the six
    downstream surfaces listed under intentionally_not_updated (charter,
    offer-hypothesis ×2, taxonomy-adjudication, the prior revision packet, the
    paper-check prompt) — all FLAGGED residuals outside this apply's authorized
    scope. No unflagged live instrument retained the old gate count.
  non_claims:
    - not validation
    - not readiness
    - not gate clearance
    - not buyer proof
    - not a scoring engine
    - not a repo-wide gate-wording reconcile (six residual surfaces flagged above)
```
