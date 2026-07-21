# Beauty Operator Pain Universe Map v0

```yaml
retrieval_header_version: 1
artifact_role: Research synthesis for owner adjudication (pain-universe map; not product authority, not a taxonomy edit)
scope: >
  The problem universe of US beauty brands at $10M-$150M revenue with DTC +
  retail distribution, enumerated from what operators actually face and then
  classified by public observability: new observable detection candidates
  (five-gated), enrichments to already-adjudicated classes, the corroborable
  proxy layer, and the explicit invisible list. Executes
  docs/workflows/forseti_beauty_operator_pain_universe_handoff_v0.md.
use_when:
  - Adjudicating new candidate detection classes into the silent-pain taxonomy.
  - Choosing sell-to-learn conversation material from the invisible list.
  - Scoping a paid-source follow-up pass (see the paywalled-source receipt).
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/product_lead/gtm/forseti_gtm_silent_pain_taxonomy_v0.md
  - forseti/product/spines/product_lead/gtm/forseti_beauty_us_problem_discovery_to_wedge_contract_v0.md
stale_if:
  - The owner re-adjudicates or re-tiers a candidate inherited by the taxonomy; use the taxonomy for current class authority.
  - The owner re-tiers the taxonomy in a way that changes the prior art below.
```

Currentness note: the observable candidates were adjudicated into the taxonomy
linked above. Use that taxonomy for current class authority; this map remains
research provenance, the corroborable/invisible boundary, and the paid-source receipt.

## Provenance and method

- Commissioned by `docs/workflows/forseti_beauty_operator_pain_universe_handoff_v0.md` (carried in this same change per the handoff-pointer merge rule).
- Executed 2026-07-18 as six parallel research lanes: retail/wholesale operations; regulatory & compliance; supply chain, manufacturing & tariffs; finance & capital; demand, marketing & channel; organization, talent & internal systems. Sources swept: trade press (Glossy, Beauty Independent, BeautyMatter, WWD, BoF, CosmeticsDesign, Cosmetics Business, Happi), law-firm client alerts, FDA/Federal Register/state primary sources, CFO-advisory and deduction/3PL/EDI/ERP vendor content (vendors document the pain they sell against), founder communities and confessionals, recruiter and job-posting surfaces, M&A/deal coverage.
- The taxonomy prior art was reread from the binding record (confirm-don't-trust), not from the handoff packet summary.
- **Paid-source disclosure:** the owner sanctioned paid sources for this pass (2026-07-18). This lane held no paid memberships, so paywalled sources were recorded (name, URL/date, what the headline or abstract shows) but not read. The consolidated receipt is in "Paywalled sources encountered, not read" below. Silent pains under-appear on free surfaces; the paywalled set is the named residual, not a claimed coverage.
- Claim discipline (binding, from the taxonomy): three layers always — dated observation → bounded operational implication → unproven hypothesis. Every candidate carries its hard limit. Nothing here characterizes legality, compliance, or fault of any named company. No pain-rate or "costs them $X" claim without a stated public basis; third-party aggregate figures are attributed to their (often vendor) source and are not per-brand claims.

## How to read this map

Every enumerated pain is classified into exactly one of:

- **observable** — a public surface shows it directly; a five-gated detection sketch is supplied (Section A), or it enriches an already-adjudicated class (Section B);
- **corroborable** — public surfaces show a proxy or second teller, not the pain itself (Section C);
- **invisible** — no public falsifier exists; recorded as the honest boundary of the product and as sell-to-learn conversation material (Section D).

The five gates (from the taxonomy, all required for admission as observable): identifiable internal owner; recurring expensive decision; sub-hour manual public test; public falsifier; stated hard limit. Candidates failing any gate were pushed down to corroborable or invisible, not admitted weakened. Per the taxonomy's verification rule, no candidate below is verified until its first real run; gate verdicts here are design-time assessments.

The known law held everywhere in this pass: pains leak into public view to the degree they touch public commerce, legal/regulatory, and hiring surfaces. The richest new candidates sit exactly there. The interior of the business — cash, margins, contracts, systems, psychology — stays dark, and Section D says so rather than inventing signatures.

---

## Section A — New observable candidates (five-gated, for owner adjudication)

### A1. Public legal-targeting record (Prop 65 registry + claims-litigation dockets)

- **Pain in plain words:** claims and labeling language the brand chose for positioning ("clean," "natural," "non-toxic"; TiO2-bearing powders sold into CA) makes it a target for private Prop 65 plaintiffs and consumer class actions. Defense cost dwarfs settlements; founders in trade press describe closures driven by serial suits ("A lawsuit is the real reason we closed" — Glossy, 2023-10-25). The pain is legal-defense burden and the recurring warn-vs-risk / substantiate-vs-strip decision, not any question of merit.
- **Internal owner:** GC/outside counsel; Founder/CEO; Regulatory; Marketing (claims language).
- **Forced decision:** apply Prop 65 warnings (hurting "clean"/premium positioning and retailer standards) vs. omit and risk a notice; substantiate or strip each green/clean claim before it ships; settle vs. defend when targeted.
- **Signature (sub-hour test):** search the CA OAG Prop 65 60-day-notice and settlement registry (oag.ca.gov/prop65) for the brand and its legal entity; search federal dockets (CourtListener/PACER) for consumer class actions naming the brand. Record dated notices/filings, plaintiff, listed chemical or challenged claim, and disposition where public.
- **Falsifier:** notices are frequently withdrawn, settled as boilerplate, or mooted — check disposition; the 2025-08-12 E.D. Cal. permanent injunction bars new Prop 65 TiO2-cancer-warning suits in cosmetics, so forward TiO2 risk differs from the historical record; a single stale notice with no follow-on is a weak signal.
- **Hard limit:** the registry and dockets prove the brand was *targeted* and carries the defense burden — never that it violated anything. No legality or fault characterization travels with a finding, ever. Settlement amounts, defense costs, and insurance are invisible.
- **Five-gate verdict:** passes all five at design time (registry and docket search are sub-hour; disposition is the falsifier). First-run verification required before any prospect use.
- **Evidence:** Glossy 2023-10-25 (founder closures over Prop 65 suits); Loeb & Loeb 2025 (TiO2 injunction); K&L Gates 2024-04-02 (clean/natural class actions); CA OAG public registry.

### A2. UCC-1 financing fingerprint (working-capital strain via lien records)

- **Pain in plain words:** the inventory-ahead-of-PO cash gap (deposit out months before net-60/90 payment back) forces brands into a financing waterfall — ABL, inventory/PO financing, factoring, revenue-based financing, MCA — whose cost eats margin. Operators name this as the defining squeeze of the bracket ("you're either not getting paid or getting paid 60 days later than you planned" — Crystal Wood, BeautyMatter 2026-03-05).
- **Internal owner:** CFO / fractional CFO; Founder/CEO.
- **Forced decision:** which financing source to tap each reorder cycle, and whether the effective cost still leaves the reorder profitable; whether to sign personal guarantees to secure it.
- **Signature (sub-hour test):** state Secretary-of-State UCC search on the brand's legal entity (entity resolution first — ties into the adjudicated Tier B entity/IP checks). Read the *lender type* and pattern: a factoring company, MCA funder, RBF platform, or inventory-finance specialist as secured party is a fingerprint of expensive working capital; recent stacking of filings and absence of terminations sharpen it.
- **Falsifier:** an ordinary bank blanket lien is normal-course and proves little; terminated/lapsed filings must be excluded; a lien can secure an unused facility. The strong form is a non-bank expensive-capital lender with a recent filing, not any UCC hit.
- **Hard limit:** liens never show amounts drawn, rates, covenants, or health. Borrowing is not distress; the finding is "this brand is paying for working capital of type X since date Y," nothing more.
- **Five-gate verdict:** passes all five at design time. Sub-hour test depends on resolving the correct legal entity and on the state's search UI; verify on first run. Some states charge small fees — flag if that matters to the read-only rule.
- **Evidence:** BeautyMatter 2026-03-05 (Saks fallout operator quotes: net-60 squeeze, personal guarantees, unpaid POs); Eightx working-capital advisories (financing waterfall, effective-APR math, vendor-sourced); finance lane cross-cutting note (UCC as the one cheap public proxy touching four distinct finance pains).

### A3. Retailer-bankruptcy creditor exposure (event-triggered)

- **Pain in plain words:** when a carried retailer files Chapter 11 (Saks Global, 2025-26 cycle), the brand's unpaid POs become at-risk receivables. Operators describe deciding "whether [they were] okay never being paid for that order" (Leilah Mundt, BeautyMatter 2026-03-05); founders with personal capital in the business are hit hardest.
- **Internal owner:** CFO; Founder/CEO; VP Sales (whether to keep shipping).
- **Forced decision:** keep shipping a wobbly retailer on open terms vs. cut off (and lose the account); insure/factor receivables at a recurring cost vs. run naked.
- **Signature (sub-hour test):** when a retailer the subject is carried by files, search the public claims register (Kroll/Stretto/PACER creditor matrix and schedules) for the brand; the filing lists the brand as creditor with a claim amount — a dated, quantified public statement of exposure.
- **Falsifier:** claims may be paid under first-day/critical-vendor orders, insured, sold, or disputed; check docket disposition before reading exposure as loss.
- **Hard limit:** exposure at filing date only; never recovery outcome, never the brand's overall AR health. Event-triggered: fires only when a carried retailer files — this is a conditional check, not a standing scan (no monitoring proposal; point-in-time per event).
- **Five-gate verdict:** passes all five when the trigger event exists; without an event there is nothing to run. Companion to Tier A class 6 (wholesale concentration): concentration is the standing read; this quantifies the downside when it fires.
- **Evidence:** BeautyMatter 2026-03-05 (Saks Global fallout, three named operator voices); BeautyMatter bankruptcy tracker 2025 (22 brand failures 2025 / 25 in 2024 / 28 in 2023, vendor-tracked).

### A4. Off-price / liquidation-channel appearance (overstock disposition fingerprint)

- **Pain in plain words:** MOQ overbuys, faded virality, discontinued shades, and packaging refreshes strand perishable inventory; brands quietly move it through off-price (TJX family) and liquidation marketplaces at a fraction of retail. The shelf announces the write-off decision the brand never talks about.
- **Internal owner:** Demand planning / Supply chain; CFO; Merchandising.
- **Forced decision:** the recurring markdown/liquidate/donate/hold call on aging stock — and upstream, how much to over-commit against MOQs in the first place.
- **Signature (sub-hour test):** search off-price surfaces (TJMaxx/Marshalls online, off-price beauty e-tailers, liquidation marketplaces such as beauty-overstock platforms) for the brand's SKUs; record price vs. MSRP, pack version (old vs. current — cross-check class 5), and seller identity (cross-check class 10's authorized list).
- **Falsifier:** some brands run a deliberate, sanctioned off-price channel; gray-market diversion (class 10) and legacy-pack sell-through (class 5) produce the same shelf state. The strong form is current-pack product, below MSRP, at scale, from sellers absent from the authorized list, while DTC holds full price.
- **Hard limit:** cannot show whether the disposition was sanctioned, its volume, terms, or the size of any write-off. Overlaps classes 5 and 10 and must name which reading it is asserting per finding.
- **Five-gate verdict:** passes all five at design time; adjudication question for the owner is whether this stands alone or folds into class 10 as its liquidation-lot sub-case. Recommendation: stand-alone, because the internal owner and forced decision differ (inventory disposition vs. channel control).
- **Evidence:** BeautyMatter (Highstock overstock-recovery coverage, 2025); efulfillment/liquidation guides 2025-26 (10-30%-of-retail liquidation, expiry loss, vendor-sourced); Eightx 168-day inventory problem (public-brand median inventory days, disclosed-financials basis).

### A5. Hero-SKU stockout during a visible demand spike

- **Pain in plain words:** virality whiplash — a creator or celebrity moment 10x's demand in hours while replenishment runs 8-16 weeks. Phlur's fragrance sold out in five hours with a 200,000+ waitlist for months (BeautyMatter, 2025); Fazit's Taylor Swift moment spiked sales +3,500% in 48 hours (Inc., 2024-10). The brand eats the loss or over-orders into A4's overstock trap on the way down.
- **Internal owner:** Supply chain / demand planning; Founder/CEO; Ecommerce.
- **Forced decision:** how much buffer to pre-build on hero SKUs (cash and expiry risk) vs. run lean and lose the moment; whether to pay 2-3x expedite/air premiums mid-spike.
- **Signature (sub-hour test):** for a subject with a visible viral moment (public view counts, press), check hero-SKU stock states across DTC + carried retailers: sold-out PDPs, waitlist/"notify me" modules, purchase limits. Point-in-time: "on date D, N of M surfaces out of stock while demand signal visible."
- **Falsifier:** deliberate drop/scarcity models, planned discontinuation or transition (class 5), seasonal phase-outs, and site errors all mimic it; the strong form is simultaneous multi-surface stockout of a current hero SKU with waitlist capture live.
- **Hard limit:** cannot see inventory position, lost sales, or cause; restock-or-not and time-to-restock is longitudinal and goes to the co-movement seed list (Section F), same as the class 3 owner note.
- **Five-gate verdict:** passes all five at design time. GTM note: this is a *door-opener with a clock* — the finding is most valuable during or immediately after the spike.
- **Evidence:** BeautyMatter viral-brands feature (Phlur; member-gated body, headline facts visible); Inc. 2024-10 (Fazit +3,500%/48h); TikTok Shop inventory analyses 2025 (30/day to 800/day in six hours, vendor-sourced).

### A6. Dupe-pressure fingerprint (moat erosion on hero SKUs)

- **Pain in plain words:** the moment a hero product works, commercial dupers (MCoBeauty-style named dupes, retailer private label) and TikTok "dupe" culture capture the demand the brand created, forcing price defense, faster innovation cadence, or IP action. The dupe market is sized ~$4.1B in 2025 (BeautyMatter Future50, vendor/analyst-sourced); prestige brands now run explicit anti-dupe campaigns (Charlotte Tilbury "Legendary. For a Reason").
- **Internal owner:** Founder/CEO; CMO/Brand; Product/Innovation; Legal (IP).
- **Forced decision:** defend price vs. cut; accelerate innovation vs. harvest; pursue IP action vs. absorb — re-litigated per hero SKU as dupes appear.
- **Signature (sub-hour test):** for each hero SKU, search "[product] dupe" across TikTok/Google/dupe-finder sites and retailer sites; enumerate *commercially marketed* dupes (named comparisons, "dupe of X" merchandising), each with price gap and seller. Count and price-gap are the finding.
- **Falsifier:** organic chatter without a commercial product is noise; claimed dupes with dissimilar INCI are superficial (check ingredient similarity); a dupe of a discontinued SKU is stale. The strong form is a currently-merchandised named dupe at a large price gap on a current hero SKU.
- **Hard limit:** dupe existence never shows revenue impact, nor whether the brand cares, nor anything about the duper's legality (explicitly out of bounds). It is pressure evidence, not damage evidence.
- **Five-gate verdict:** passes all five at design time. Cleanly complements the complaint-world authority layer: this is competitor-side pressure the subject's customers never complain about.
- **Evidence:** Cosmetics Business (Charlotte Tilbury anti-dupe campaign); Hollywood Reporter (MCoBeauty model, dupes at Sephora); BeautyMatter Future50 2025 ("Innovation vs. Imitation").

### A7. State EPR producer-registry presence (verification-gated — held at corroborable until gate 3 verified)

- **Pain in plain words:** seven+ state packaging-EPR laws make every brand a "producer" owing PRO membership (Circular Action Alliance), per-material reporting, and eco-modulated fees — "CPG Brands, Meet Your New P&L Line Item" (Venable, 2026-03). Beauty's mixed-material packaging is a worst case. CO required PRO membership by 2025-07-01; CA's first common reporting deadline is 2026-05-31.
- **Internal owner:** Ops/Supply chain; Finance; Sustainability/Packaging; Regulatory.
- **Forced decision:** redesign packaging toward mono-material (capex, aesthetic cost) vs. pay rising fees; per-state registration workload.
- **Candidate signature:** check whether the brand appears in PRO/state producer registries where its distribution says it must. Absence-where-expected would be the finding (structure mirrors adjudicated class 9, certification directory check).
- **Why held back:** gate 3 (sub-hour public test) is unverified — whether the CAA/state producer lists are publicly searchable at brand grain is not established from free surfaces. Do not admit until a first run proves the registry surface exists and resolves brands. Until then this sits in Section C as a corroborable exposure read (packaging-heavy brand + covered-state distribution = obligation exists).
- **Evidence:** Venable 2026-03; Beauty Packaging 2026 EPR guide (deadlines); BeautyMatter EPR pieces (partially gated).

---

## Section B — Enrichments to already-adjudicated classes (new operator-side evidence only; no re-derivation)

- **Class 1 (master-data divergence):** the internal cause is now documented from the operator side — no PIM owner below ~$150M, per-channel re-keying across Shopify/Amazon/retailer portals/EDI, "spend half your life fixing listing errors" (PIM-vendor operator framing). Strengthens the door-opener: the external grid is the fingerprint of a named internal role gap. Corroborating hire signal: e-commerce ops/PIM postings.
- **Class 2 (price-pack conflict, observation half):** add **TikTok Shop as a priced surface** — storefront list price, stacked platform vouchers, and posted creator-commission rates on the affiliate marketplace are public, and fees are charged on the discounted price, so voucher-stacked effective price is a live per-unit rung on the ladder. Operator-side confirmation of the promo-dependence pain (discount-spiral fear; "fewer, bigger, more strategic" 2025 deal calendars) reinforces the class's GTM story. Promo-share-of-days depth reading is longitudinal → Section F.
- **Class 3 (markdown/delisting):** operator-side confirmation that markdown chargebacks are "among the largest single deduction events in a given quarter" (deduction-vendor content) — the observation half's GTM story now has a named finance-side sting. Restock-timing follow-on remains co-movement (owner note stands).
- **Class 6 (wholesale concentration):** sharpener — retailer-site **exclusivity flags** ("Only at Sephora"; ~half of Sephora's assortment is exclusive per BeautyMatter) are a public, per-SKU concentration read that upgrades the door-share recipe. Companion when concentration's downside fires: candidate A3. Context: Rare Beauty's 2026 Sephora-to-Ulta move shows the switching event is public and dated.
- **Class 7 (formula-to-standard):** extend the mapped standards from retailer lists to **dated statutory ban lists** — WA formaldehyde-releaser restrictions (from 2027-01-01), CA AB 496's 26 ingredients (2027-01-01), state PFAS bans (staggered 2025-2029). Same sub-hour INCI-vs-list mechanics, but the deadline is statutory and the forced decision (reformulate-to-strictest vs. state-specific SKUs — "the one US formula is dying," IBA-voiced) is harder than a badge. Pre-effective-date findings are exposure observations, never compliance characterizations.
- **Class 8 (regulated-SKU listing):** companion surfaces — the public **FDA recall database and warning-letter index** extend the check from listing mismatch to enforcement-event record (benzene/BPO recalls 2025 are precedent). The dual-framework burden (drug-tier cGMP + Drug Facts + establishment registration on every SPF/acne/AP SKU) is the operator-side weight behind the class's door-opener.
- **Tier B orphan pages:** owner's amplified framing (stale claims/prices still live) is confirmed operator-side — the claims-substantiation wave (A1 evidence) makes a stale live claim a sharper pain than a dead link.
- **Tier B supplier import refusals:** unchanged; recall/warning-letter records (class 8 companion) are the nearer FDA surface for finished-good events.
- **ATS hiring corroborator lens (adjudicated):** upgrade from "a hire is a paid confession" to a **decode table** — posting language maps to live pain class: "must currently be working with these retailers" (VP Sales incumbency scarcity → retail-relationship pain); regulatory-affairs head (MoCRA ownership gap); demand planner/S&OP (forecasting pain); EDI/vendor-compliance coordinator (chargeback pain); NetSuite administrator/ERP partner postings (systems break point); deductions/AR analyst (deduction burden); field educator (in-store execution cost); fractional-CFO/COO engagements visible on LinkedIn (senior-seat affordability gap). Each decode is a corroborator, never a standalone finding.

---

## Section C — Corroborable layer (proxy or second teller; not the pain itself)

| Pain (domain) | Internal owner | Forced decision | Public proxy | Why not observable |
| --- | --- | --- | --- | --- |
| Retailer compliance chargeback stack: EDI/ASN/routing/labeling penalties, OTIF (retail ops) | VP Ops/Supply chain; deductions analyst | insource vs. buy compliance; dispute vs. write off | vendor-industry existence (3PL/EDI/deduction guides per retailer), hiring decode; penalty *rules* public | per-brand incidence lives in retailer portals; prior rejection of chargeback class as observable holds |
| Retail media / co-op pay-to-play (retail ops + demand) | VP Retail Marketing; CFO | budget share to retailer networks vs. owned channels | sponsored-placement presence on retailer sites shows participation | spend, minimums (JBP-committed), and ROI invisible; measurement crisis is industry-voiced only |
| In-store execution cost: field teams, education, testers (retail ops) | Head of Field/Education | headcount per door count | field-educator job postings; testers visible in-store | cost and coverage decisions internal |
| MoCRA ownership gap; AE intake; GMP-readiness (regulatory) | Regulatory (often absent); COO | hire vs. consultant vs. push to co-man | regulatory/quality hiring decode; FDA rule status public | filings/systems not publicly searchable at brand grain |
| Regulated-ingredient exposure flags: talc-in-INCI, BPO/aerosol chemistries, ethoxylates (1,4-dioxane risk) (regulatory) | Regulatory; R&D | test/reformulate vs. absorb risk | INCI shows exposure class membership | exposure ≠ pain; test results/CoAs private; forcing into a signature would fake it |
| Re-sourcing / origin shifts under tariffs (supply chain) | Procurement; COO | re-qualify supplier vs. stay on tariffed incumbent | dated "made in / sourced in" changes on pack/PDP; founder disclosures in press | the evaluated-and-abandoned switch invisible; origin-change tracking is longitudinal (Section F) |
| Reformulation churn under state patchwork (supply chain + regulatory) | R&D; Regulatory | reformulate-to-strictest vs. state SKUs | dated "new formula"/"now free-of" relaunch claims; INCI diffs vs. archive | the scramble (stability retests, requalification) invisible; snapshot mechanics already owned by classes 4/5/7 |
| Fundraising strain (finance) | CEO; CFO | bridge/flat round vs. cut to breakeven vs. alt capital | dated round/crowdfunding announcements; market-level VC data (2021 peak $3.3B → $438.8M through July 2024, Beauty Independent-sourced) | whether a round was a down round, and terms, rarely disclosed |
| Exit stall / "muddy middle" (finance) | CEO; board | hold vs. sell soft vs. restructure | market-level deal counts and multiples (67 US deals 2025 vs 108 in 2024, Capstone-sourced) | the brand quietly unable to find a buyer is invisible by construction |
| TikTok dependence (demand) | CEO; CMO | keep maximizing vs. pre-build redundancy | platform-footprint skew (follower/engagement concentration) observable | revenue share per platform undisclosed |
| Creator spend posture (demand) | Influencer lead; CMO | pay proven creators vs. UGC/affiliate shift | tagged #ad posts show who; affiliate-marketplace commission rates show terms offered; ad-creative persistence lens (adjudicated) | rates paid and measured ROI invisible |
| DTC-to-retail channel shift (demand) | CEO; Head of DTC | keep funding DTC vs. reallocate to retail | new-door announcements, retailer listings, "now at Ulta" posts | per-brand traffic/conversion decline needs analytics |
| Brand refresh / founder-transition pressure (org) | CEO; board | refresh/broaden/replace vs. protect founder equity | rebrand launches, CEO/GM appointment announcements, CMO churn | the internal pressure precedes any public signal |
| Founder-led-sales ceiling (org) | Founder; incoming VP Sales | when/how to hand off buyer relationships | VP Sales hire announcement = handoff attempt (decode table) | whether the handoff is failing is invisible |
| Bracket layoffs / quiet restructuring (org) | CEO; CFO | whom to cut; what to outsource | press-covered cuts; LinkedIn headcount decline (paid tool); WARN mostly misses sub-100-employee brands | most cuts at this size are unannounced |
| Loyalty/retention economics (demand) | Retention lead; CFO | divert acquisition budget to retention | program existence/tiers/mechanics public | retention rates and LTV fully internal |
| Packaging EPR obligation (regulatory) | Ops; Finance | redesign vs. pay fees | covered-state distribution + packaging materials imply obligation; A7 pending registry verification | registry searchability unverified |

## Section D — The invisible list (honest boundary; sell-to-learn conversation material)

No public falsifier exists for these. They are recorded because the invisible list is the honest boundary of the product and first-rate conversation material for sell-to-learn calls — each is a pain the operator knows intimately and no outsider can pretend to have measured.

| Invisible pain | Owner | The recurring decision the operator is alone with |
| --- | --- | --- |
| Inventory-ahead-of-PO cash gap magnitude; financing rates actually paid | CFO; CEO | how much inventory to fund, from which source, at what real cost (A2 shows the arrangement exists, never the terms) |
| Deduction/chargeback write-off magnitude; dispute-vs-write-off economics | Finance/AR | fight each deduction inside its window or eat it (prior rejection re-confirmed by two lanes: no new public signature) |
| Markdown-money demands and their negotiation | VP Sales; CFO | fund the retailer's markdown or risk the account |
| Fill-rate scorecards inside retailer portals | Supply chain | how much safety stock to freeze against penalty regimes |
| Retail-media minimums, JBP commitments, and incrementality | Retail marketing; CFO | committed spend that can't flex on performance |
| True CAC/contribution by channel; SKU/channel profitability blindness | CFO; Growth | where money is actually made — often unknown internally, so doubly invisible externally (upstream cause of several visible failures) |
| Email/SMS revenue-per-send decline; list health | Retention | push frequency vs. deliverability |
| Creator rates paid and measured ROI | Influencer lead | pay up vs. shift to UGC amid measurement doubt |
| TikTok Shop net contribution after fees/vouchers/returns | CFO; Marketplace lead | run it as paid acquisition or walk (posture partially visible; the net number never) |
| CM capacity/priority/MOQ strain; single-source component dependence | Ops; Procurement | over-commit to hold a slot vs. second-source vs. accept stockout risk (prior rejection re-confirmed: no new public signature) |
| Batch QC rejections caught pre-ship; expedite/air-freight decisions | Quality; Logistics | reject-and-rerun vs. rework; pay 2-3x to save a window |
| Tariff absorb-vs-pass deliberation; refund/HTS recovery at mid-size | CFO; CEO | eat margin vs. reprice vs. re-source (only the resulting price steps are visible — Section F) |
| MoCRA safety-substantiation adequacy; AE intake systems; supplier CoA gaps (1,4-dioxane) | Regulatory; QA | how much to spend against an undefined standard |
| Claims-review discipline before shipping copy | Legal; Marketing | substantiate or strip every claim (only the lawsuit that follows failure is public — A1) |
| QoE/diligence readiness; founder personal guarantees | CFO; Founder | invest in acquirability now vs. an uncertain exit; pledge the house or forgo the PO |
| Internal PIM/re-keying burden; tool sprawl and integration debt | Ecom ops | consolidate (costly migration) vs. keep paying the reconciliation tax |
| Founder burnout mid-stream; agency churn; the "dual life" | Founder | keep burning payroll and morale vs. restructure or close (visible only in closure confessionals, i.e., too late) |

## Section E — Prior-art confirmations (nothing resurrected)

- **Rejected classes stay rejected, now with independent re-confirmation:** returns/chargeback burden (two lanes searched; nothing beyond vendor-marketing aggregates like the 5-7%-of-revenue figure, which is a vendor claim, not a per-brand public datum); paid-acquisition deterioration (demand lane confirms: ad libraries show creative, never spend or performance; no new signature); CM concentration/MOQ strain (supply lane confirms: only weak sector-level proxies).
- **Parked families sighted but not resurrected:** international fragmentation surfaced repeatedly (EU RP/CPNP entry burden, EU allergen relabeling deadline 2026-07-31, US-vs-EU SPF formula divergence from the monograph lock) — all recorded here as context and left parked per the owner's deferral (moot until subjects are multi-market). Cart-interaction and search/filter leakage: nothing in this pass argues for unparking.
- **Known law re-confirmed:** every strong new candidate sits on a public commerce, legal/regulatory, or hiring surface (A1-A6); the interior stayed dark and Section D holds it honestly.

## Section F — Co-movement seeds (longitudinal only; not current point-in-time runs)

Clearly marked per the drift guard — these are future longitudinal ideas, not runnable checks in this pass:

- Restock-or-not and time-to-restock after an A5 stockout fires (extends the existing class 3 owner note).
- Tariff-driven price-step archaeology: archived-PDP price series showing dated step increases.
- Origin-shift tracking: "made in / sourced in" changes across packaging snapshots.
- Promo-depth trend: share-of-days-on-promo from newsletter archives over quarters (class 2's longitudinal shadow).
- Ad-creative persistence (already an adjudicated seed; unchanged).

## Section G — Paywalled sources encountered, not read (the receipt)

Owner sanctioned paid sources; this lane held none. Highest-value targets for a paid or authenticated pass, recorded per the commission:

- **Beauty Independent** (hard 403 on fetch throughout): MoCRA founder-impact; "How Beauty Brands Scale After The DTC Boom"; "tight-fisted investors" fundraising feature; tariff cost features; production-nightmare and CM-selection features; team-building features.
- **WWD Beauty Inc:** tariff/packaging features; TikTok Shop tariffs/ownership; Pat McGrath Chapter 11 detail; "Inside Beauty's Growing Universe of Distressed Acquirers"; markdown-money coverage (Sourcing Journal).
- **Business of Fashion:** "Beauty Testers Are Back"; indie-retailer slowdown; founder-led-era pieces; State of Fashion Beauty.
- **BeautyMatter (member-gated bodies):** "$202 Billion Tariff Problem"; "Inside Beauty's Fight to Recover Billions"; "Your brand went viral on TikTok — now what?" (seven-brand operator interviews — likely the single richest untapped operator-voice source found in this pass); Future50; EPR deep-dives; state-regulation tracker.
- **Others:** Capstone Beauty M&A updates and DC Advisory notes; thefashionlaw M&A/investment tracker (gated dataset); Fashionista SKU-reduction feature (403); Centric Software beauty-discounting whitepaper (gated); femfounded EDI reference (403; headline: "The $6K-$50K System Retailers Force You to Buy"); ACI "Litigation Landmines in Beauty" and Mintz/Citeline litigation trackers; Glossy Beauty Podcast audio (untranscribed operator interviews); retailer vendor portals (Sephora Brand Relations Handbook, Target Partners Online) — the primary penalty schedules themselves, gated per-vendor.

## Drift-guard compliance and non-claims

- Research/design pass only: no outreach occurred, no subjects were scanned, no ICP was bound, no tooling was built.
- The complaint world (clients'-clients evidence) remains the authority layer; this map covers the supplement/door-opener layer and says so.
- No standing monitoring is proposed; A3 is event-triggered point-in-time, and all longitudinal ideas sit in Section F as seeds.
- Non-claims: this map is not a taxonomy edit (candidates enter only via owner adjudication); not validation of any candidate (first-run verification rule applies to every sketch above); not company pain evidence about any named brand; not legality, compliance, or fault characterization of anyone; not demand, buyer-intent, or willingness-to-pay proof.
