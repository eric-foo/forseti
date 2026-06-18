# Orca ICP Redo — Evidence & Stats Distillation Targets v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact (non-authoritative)
scope: Logs the decided targeting frame, the candidate decision-cores, and the per-core statistics to distill for the from-scratch ICP redo. Stages an evidence-only deep-research pass.
use_when:
  - Preparing or running the ICP-redo evidence search.
  - Synthesizing returned evidence into an ICP selection.
  - Checking which stats are already grounded vs. still needed.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/product_lead/icp_wedge/orca_product_lead_first_icp_wedge_decision_v0.md
  - orca/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md
stale_if:
  - The ICP redo selects a wedge and supersedes this note.
  - The decided frame, axes, or dial weights change.
  - Returned evidence changes a logged stat.
```

## Status

Non-authoritative research-staging note. It logs (a) the decided targeting frame
from the Product-Lead lane, (b) the candidate decision-cores to gather stats on,
(c) the stats already grounded with sources, and (d) the per-core evidence still
needed. It does not select an ICP, validate anything, or claim WTP/readiness. It
feeds an evidence-only deep-research pass; selection and synthesis stay with the
owner + Opus 4.8. Created untracked in the `ecr-sp3-timing-deriver-slice1`
worktree; to be committed with the product/research set (see persistence note in
the lane).

## Decided frame (Product-Lead lane)

- Targeting unit = a qualified decision-moment, modeled at three levels:
  hunting ground (sector/segment) -> account (retention unit) -> trigger
  (acquisition unit).
- Public-signal-affectable filter (hard gate): a decision qualifies only if
  publicly observable evidence can materially move the decision or its risk.
  Requires BOTH signal availability AND causal relevance. Private-data-gated,
  confidential, or MNPI decisions are excluded regardless of stakes.
- Scoring axes per core: recurrence/density; stakes/magnitude; servability
  (public-signal richness + affectability); reachability of the decision owner;
  newcomer-winnability (can an unproven vendor get a first yes); plus a
  public-vs-private flag.
- Weighting for the FIRST yes (LOCKED 2026-06-08):
  primary = newcomer-winnability on a live, survivable, public decision, with
  stakes shaped as consequential-but-survivable; density is the tiebreaker that
  picks which winnable core to farm. Servability is a hard gate; the trust-bar
  lifts as track record grows.
- End-game = a decision-cadence retainer (post-proof), so density/recurrence
  predicts retainer potential. Retainer is a selection criterion, not a current
  build target.
- Scan breadth (decided): truly open cross-sector for the first pass.
- Headline deliverable (decided): find the most farmable public decision-core,
  with stats.

## Candidate decision-cores to log

| Core | Why a candidate | Public / private | Status |
| --- | --- | --- | --- |
| Pricing / packaging / monetization (leading hypothesis) | Recurring, high-stakes (revenue/churn), strongly public-signal-affectable, detectable | Public | Hypothesis to beat |
| -- AI-monetization sub-core (AI add-ons, AI-cost repricing, usage/consumption repricing) | Current live wave; hottest patch | Public | Live now |
| Competitive response / positioning | Recurring in fast-moving categories; signal = competitor move + public reaction | Public | Candidate; scope-drift risk |
| Category / market entry | High-stakes; analyst/community/press signal | Public | Candidate; rarer |
| Launch / GTM timing | Public-reaction-driven; frequency varies | Public | Candidate |
| Excluded by servability gate: M&A, IPO/financing, capex, internal restructuring, any data-room/MNPI decision | Decided on private numbers; Orca cannot serve | Private | Out (log as excluded) |

## Stats already grounded (preserve with sources)

These came from a bounded web-research pass; they are market-context estimates,
not validation. Ranges, not precision; analyst estimates flagged.

- Population (dev-facing B2B SaaS/API/infra/data-product, post-revenue, public
  pricing surface): ~1,500-4,000 global (low single-thousands likely);
  ~800-2,200 US. Confidence low-med. Sources: Ascendix/Statista (~30.8k SaaS
  global / ~17k US; ~17k B2B SaaS), Specter (~550 curated dev-tools), Failory
  (33 dev-tool unicorns), Seedtable (~69 API-infra). Definition-sensitive.
- Decision frequency: ~75% of SaaS changed pricing and/or packaging in a year
  (OpenView 2023, n=700+, HIGH); market leaders on 9-month / 90-day cycles
  (Simon-Kucher, MED); ~60% of SaaS usage-based, ~78% of Developer Tools &
  Infrastructure use consumption pricing (Gartner-attributed, MED); AI repricing
  wave (Sentry Seer Jan 2026; Cursor 2025; Salesforce Agentforce; Intercom Fin);
  AI gross margin ~50-60% vs ~80-90% SaaS (Bessemer/ICONIQ). Live-decision share
  estimate ~25-45% (mid ~1/3), HIGH uncertainty.
- WTP anchor: bounded boutique pricing sprint ~$15-25k (DemandMaven, published,
  HIGH); generic fixed-fee $5-15k+; enterprise (Simon-Kucher) undisclosed
  high-5/6-figure; billing/monetization tooling 0.7-1.5% rev or $7-75k/yr
  (adjacent, not a substitute); CI/market-research programs $23-120k/yr.
  Reasoned one-off decision-artifact band ~$8-30k (center $12-20k). Dominant
  uncertainty: buyer bucketing (consulting vs report vs DIY).

## Per-core evidence still needed (distillation targets)

| Core | Stats to distill | Already grounded? |
| --- | --- | --- |
| Pricing / packaging | Recurrence rate; stakes ($ at risk); owner role + reachability; newcomer-winnability evidence | Population/frequency/WTP grounded for dev-facing only |
| AI-monetization sub-core | Size/recency of the wave; example count; stakes per decision; recurrence | Partial (examples + margin driver) |
| Competitive response / positioning | Frequency; stakes; public-signal richness; winnability | No |
| Category entry / launch timing | Frequency; stakes; servability; winnability | No |
| Cross-sector (beyond dev SaaS) | Sector-level decision-density map: which industries have the densest public, consequential, recurring decisions | No |

## Turn 1 (breadth) results + Turn 2 plan

Ran 2026-06-08 via the external deep-research model (evidence-only). Figures are
DR-model-cited with the model's own confidence tags; not independently
re-verified here. Market-context only.

Cores surfaced, with servability tag and disposition:

| Core | Recurrence (DR-cited) | Public/private | Disposition |
| --- | --- | --- | --- |
| Pricing / packaging / monetization | ~50% of firms reprice multiple times/yr (Richmond Fed); net 30% small firms raise prices in a month (NFIB) | public-signal-affectable | T2 priority (cross-sector finding) |
| Competitive-response / positioning | no survey denominator (measurement gap, not rarity) | public | T2 priority (case-based evidence) |
| Product launch / GTM timing | ~9-11%/yr product innovation (NCSES/Census ABS) | mixed | T2 secondary |
| Marketing / paid-media mix | annual budget cycle ~7.7% rev (Gartner) | mixed (ad-transparency public; first-party private) | T2 secondary (monitoring-drift risk) |
| Workforce hiring / staffing | 53% hiring; monthly JOLTS flow | mixed | pruned (operational/internal; weak winnability) |
| Credit underwriting / lending | quarterly SLOOS; ~$13.5T balances | mixed | pruned (model/regulation-driven; incumbent-locked) |
| M&A / IPO / major capex | various | private/confidential | excluded by servability gate |

Synthesis points (Opus):

- Cross-sector pricing finding: repricing is dense AND public economy-wide, not
  just dev SaaS, which strengthens pricing as the farmable public core and opens
  a cross-sector L3 expansion path.
- Measurement caveat: competitive-response / positioning / category-entry lack
  survey density because they are unsurveyed, not rare. Evidence them case-based,
  not by population denominator.
- Marketing-mix risk: rich public ad-transparency substrate (Meta Ad Library,
  Google Ads Transparency Center), but annual-cycle + incumbent-crowded +
  monitoring-drift (an Orca kill criterion). Kept secondary, not prioritized.

Turn 2 plan (depth; two concurrent evidence-only passes; winnability +
reachability + WTP held for Turn 3):

- T2-A (priority): Pricing/packaging + Competitive-response/positioning ->
  `docs/prompts/product-planning/orca_icp_dr_t2a_depth_priority_evidence_prompt_v0.md`
- T2-B (secondary): Launch/GTM timing + Marketing/paid-media mix ->
  `docs/prompts/product-planning/orca_icp_dr_t2b_depth_secondary_evidence_prompt_v0.md`
- Depth axes (both passes): precise recurrence; stakes ($ at risk / decision
  value); servability detail (which public surfaces, how rich); decision-owner
  role.

## Turn 2 (depth) results + finalist narrowing

Ran 2026-06-08 via the external deep-research model (two concurrent evidence-only
depth passes). T2-A = priority pair (pricing/packaging + competitive-response),
returned as `deep-research-report2.md`. T2-B = secondary pair (launch/GTM +
marketing-mix), returned as `deep-research-report1.md`. NOTE: the file numbering
is the reverse of the A/B labels. Figures are DR-model-cited with the model's own
confidence tags; not independently re-verified. Market-context only.

Per-core depth read (recurrence / stakes / servability / owner):

- Pricing / packaging / monetization — STRONGEST on all four axes.
  - Recurrence: 78% of SaaS changed pricing and/or packaging in 2023 (OpenView,
    n=710, HIGH; 50% changed both, 25% price only); 79% of 2,253 cross-sector
    firms raised prices last year (Simon-Kucher 2025, HIGH); within-year
    repricing in retail/CPG/services (ECB WP2853 US posted-price 39.35%/mo;
    Bils-Klenow services ~21%/mo; GAO CPG downsizing 3x upsizing 2021-24). Dense
    AND cross-sector.
  - Stakes: median +14% NDR from a pricing change (OpenView, HIGH); avg +11%
    increase but only 48% realization (Simon-Kucher); Disney DTC op-income +$850M
    YoY. Survivable→nine-figure band well covered; public list budgets $10/seat
    → $125/user/mo.
  - Servability: richest substrate — pricing pages (Notion/GitHub feature-gate +
    metering detail), changelogs/announcements (Atlassian JSM), help-center
    (Netflix), earnings (Disney ARPU/churn), review sites (G2 3.5M+). Caveat:
    negotiated enterprise + CPG-manufacturer pricing stay private.
  - Owner: dedicated senior roles exist and are named/reachable (Justworks Head
    of Pricing & Packaging PMM; Talkdesk Pricing Director + Pricing Committee;
    GitLab Lead PMM Pricing). Only 6% of SaaS hired a 3rd party for pricing —
    internal muscle (the central WTP/winnability flag for T3).
  - AI-monetization sub-wave is live: 76% launched/planned AI features, only 15%
    monetized (OpenView); AI margins ~50-60% vs ~80-90% SaaS forcing repricing.

- Competitive-response / positioning — FOLDS INTO PRICING (not a standalone
  core). No population denominator (confirmed measurement gap). All 6 documented
  cases (Zoom AI add-on, Disney, Delta fare families, Walmart+, Atlassian JSM,
  Microsoft Copilot) ARE pricing/packaging moves seen through a competitor-trigger
  lens. → Competitive-response is the sharpest PUBLIC TRIGGER for the pricing
  core, not a rival finalist. This strengthens pricing rather than competing.

- Launch / GTM timing — PARTIAL gate; weaker. Recurrence moderate/muddy (GTM
  Alliance 2-12/yr; NCSES product-innovation 10% of firms 2020-22, and innovation
  ≠ a timing decision). Stakes high when they occur (Take-Two GTA VI delay swung
  FY26 bookings ~$500M; Apple 10-K "significant"). Servability split: launch
  EVENT public (Newsroom, Product Hunt, App Store, Steam, Google Trends) but the
  TIMING DECISION inputs (readiness, QA, financing, channel inventory) are largely
  private (NVIDIA 10-K). Owner diffuse: only 10.3% have a dedicated GTM owner;
  79.6% work with 5+ stakeholders.

- Marketing / paid-media mix — DROPPED (fails the servability causal-relevance
  half of the gate). Public ad-transparency (Meta Ad Library, Google Ads
  Transparency Center, TikTok Creative Center) exposes competitor CREATIVE/
  placement, but the decision is driven by PRIVATE ROAS/attribution/incrementality
  /first-party data (Ads Data Hub, Amazon AMC). Annual budget cycle (~7.7% rev,
  Gartner) = low density. Public signal is available but NOT causally central →
  the monitoring-drift kill criterion. T1 risk confirmed.

Field collapse (servability hard gate + locked frame):

- Marketing-mix: OUT (gate fail — public signal not causally central).
- Competitive-response: FOLDED into pricing as its public trigger.
- Pricing / packaging: FINALIST 1 — densest, richest causal public substrate,
  clearest senior/reachable owners, AI sub-wave live.
- Second T3 slot — RECOMMENDED: AI-monetization repricing sub-core (Option 1,
  concentrate; two altitudes of one trunk). Rationale: under the locked
  winnability-primary dial, AI-repricing is the single best live/survivable/public
  decision in the field (forced by margin, greenfield with no incumbent playbook,
  public-signal-rich); launch-timing (diversify) is weaker on the very primary
  axis (private decision inputs, diffuse ownership) so it dilutes rather than
  de-risks; the two pricing altitudes fail for DIFFERENT reasons (mature-pricing
  low-WTP vs wave-too-early), so "both die together" is overstated — concentration
  loads onto our substrate strength, not a single kill switch. Launch/GTM timing
  PARKED as the logged fallback probe if T3 exposes a systemic pricing-wedge flaw.
  Owner sign-off = running T3. Not frozen; no ICP pick.

Held for T3 (convergence, finalists only): newcomer-winnability, decision-owner
reachability, WTP. Sharpest question: the "only 6% hire a 3rd party for pricing"
stat is the central WTP/winnability risk for the broad-pricing wedge — the AI
sub-core (no established internal playbook yet) is the greenfield hypothesis to
test against it. T3 is built to DISCRIMINATE the two altitudes on that axis.

## Convergence (pre-pass): frame + first-proof finalists

Owner-steered convergence on 2026-06-08, before spending another DR pass.
SUPERSEDES, in the Turn-2 section above, both (a) the "Second T3 slot —
RECOMMENDED: AI-monetization" recommendation and (b) the original "Turn 3 plan"
(pricing + AI-repricing). AI-monetization is NOT dropped — it folds into Finalist
1 as its sharpest instance (first-time AI monetization = unfamiliar territory).

Engine (settled): outside-in competitive & market intelligence — the reusable
core that feeds every application. Competitive intelligence IS this engine, not a
separately sold decision.

Buyer (de-niched; situational, NOT a segment): any company — incumbent OR
challenger — at a moment where the decisive input lives OUTSIDE its walls: a new
product line, a new market/segment, first-time AI monetization, or a newly
surfaced competitor. Incumbents enter this state constantly, so it is not a
headcount niche. "Challenger / entrant" posture is a winnability AMPLIFIER for
picking the first yeses (hungrier, more outside-in-dependent), not a hard filter.

Selector rule (the through-line): a decision fits Orca NOW if the buyer is
outside-in-dependent — decisive input outside the walls, no internal substitute.
It defers/fails if the decisive input is inside the walls (own usage, own ROAS,
own readiness). Gate refinement: apply this to specific DECISIONS, not whole
families — a family can hold both a public and a private decision (the marketing
split below is the lesson).

First-proof finalists (1-2 per the locked dial; carry BOTH into the pass):
- Finalist 1 — Pricing, outside-in slice (competitor-/AI-/backlash-triggered).
  Best EVIDENCED (T1+T2). Weakness: the in-house headwind survives (6% hire help;
  Orca is an input, not the only source). AI-monetization is its sharpest instance.
- Finalist 2 — Break-in / competitor-customer / win-loss intelligence (why
  prospects buy from competitors not us; what would move them). Best FIT to the
  rule — no in-house substitute (you cannot see a competitor's customers from
  inside your own CRM), so it dodges the 6% problem. Weakness: funnel-skipped
  (zero T1/T2 evidence) and consulting-sprawl risk unless bounded to a concrete
  win/loss artifact.
- Decisive contest: best-evidenced (pricing) vs best-fit-to-the-rule (break-in).
  That IS the first-yes question the pass must inform.

Engine/satellite architecture: competitive/market intelligence = engine (core);
pricing, break-in, positioning, roadmap-bets, category-entry = applications
(satellites). Pricing is one satellite, not the product.

Package / horizon (logged, not first proof):
- Outside-in applications kept for the package, deferred for first proof:
  positioning/messaging, product/roadmap-feature bets, category/market entry
  (#5 — thesis-named, never depth-tested), churn diagnosis from public signal.
- Own-client marketing optimization (private ROAS/attribution) = v2.0 (private
  data; later scale, not now).
- Launch sequencing = DROPPED (private readiness inputs; diffuse ownership).

Market sizing (TAM/SAM/SOM; context only, NOT proof):
- TAM (broadened frame): a slice of competitive-intelligence + market-research +
  strategy/pricing-consulting spend (multi-billion adjacent category). NO specific
  figure verified this session; a cited TAM is folded into the pass below.
- SAM (beachhead, grounded): dev-facing ~1,500-4,000 firms × ~25-45% live/yr ×
  ~$12-20k one-off ≈ ~$5-25M/yr beachhead decision-spend ceiling (capture
  unproven; cross-sector multiplies, unquantified). Illustrative arithmetic only.
- SOM (operating number now): first 1 → ~3-10 buyers. Dial-1 winnability optimizes
  SOM; TAM matters only for the retainer/farm end-game.

Sharpened pass (replaces the old Turn-3 plan; one evidence-only pass):
- Prompt: `docs/prompts/product-planning/orca_icp_dr_t3_convergence_evidence_prompt_v0.md`
- Job: bring Finalist 2 (break-in) up to evidence parity (recurrence/stakes/
  servability/owner) AND run the winnability/reachability/WTP discriminator on
  BOTH finalists, PLUS an outside-in-dependence probe (do firms do this in-house
  or buy it?) AND a cited TAM/market-size pull (CI + market-research + win/loss +
  pricing/strategy-consulting market sizes; challenger/entrant population proxies).
- After the pass returns: owner + Opus make the final selection (no selection
  before). Nothing frozen.

Selection (owner-locked 2026-06-08): BREAK-IN-FIRST / pricing-expansion, on one
outside-in intelligence engine. Both passes returned (owner's external DR =
verified primary; parallel Opus run = unverified cross-check — harness
verification failed, leads only). Decisive axis = in-house vs bought: pricing
decided in-house (~6% hire help) vs break-in's proven outside-buy market (~36%
third-party, established providers, ~$15-50k/yr). This research note
(non-authoritative) is SUPERSEDED as the selection home by the decision record
`docs/decisions/orca_icp_wedge_convergence_break_in_first_v0.md`, which carries
the product_doctrine propagation blocker + the downstream document-update
cascade. Caveats preserved: break-in adoption/ROI is vendor-published (discount);
not validation/WTP/buyer-proof.

UN-FLIP (owner-locked 2026-06-08): direction reversed to PRICING-FIRST. The
break-in flip rested on the in-house-vs-bought axis, which TWO de-correlated
verification runs (Opus parallel + owner external o3) confirmed has NO independent
denominator (either side); the hard gate independently favors pricing (clean
non-review competitor-price substrate vs break-in's biased/polluted review
substrate + interview-gating); the 5-champion Opus tournament converged on pricing
as least-blocked. Competition stays the ENGINE; pricing is its first application;
break-in retained as a clean-substrate test + retainer horizon. Authoritative
un-flip + retainer map + propagation: `docs/decisions/orca_icp_wedge_pricing_first_v0.md`.

## Horizon items logged (L4 — direction, not scope)

- Private-data fusion (public + private) for sharper decisions: the expansion
  ring, earned via track record. Excluded from the proof by current doctrine.
- Quantitative demand-elasticity via private usage/transaction data: the
  quantitative upgrade to the qualitative public read.
- Qualitative pricing-power / PMF read from public signal (product idea):
  relative and uncertainty-flagged; fits the action-ceiling competence; NOT a
  true elasticity number (public signal is biased and lacks transaction data).
- Palantir/Foundry differentiation: stay decision-artifact-first (outside-in
  signal + judgment + outcome memory) vs. Palantir's internal-data
  integration/lock-in. A McKinsey-style advisory moat (trust + proprietary
  method + outcome memory) is the near-term moat path; both the Palantir-lock
  and McKinsey-trust moats are later, gated by prestige/track record.

## Non-claims

Not validation, not willingness-to-pay, not readiness, not buyer pull, not an
ICP selection. All figures are market-context estimates; ranges not precision;
analyst estimates are distinguished from primary data. This note stages
evidence; it does not gather, select, or synthesize it.
