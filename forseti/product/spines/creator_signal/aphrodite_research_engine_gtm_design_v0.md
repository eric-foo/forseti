# Aphrodite Research-Engine GTM Design v0

```yaml
retrieval_header_version: 1
artifact_role: Design lane artifact (Forseti OWN-growth GTM using the CSB→capture→creator_signal engine) — applies ratified doctrine; not itself ratified doctrine
scope: >
  How Forseti points its OWN outside-in research/CI engine (the
  CSB → capture → creator_signal chain) at its OWN go-to-market: (A) sourcing +
  scaling the B2B outreach motion's inputs at depth, (B) SEO authority content
  that genuinely earns rankings, (C) AEO earned answer-engine citations, (D)
  CreatorIQ/peer outside-in competitive intelligence, and (E, optional) inbound
  feeding the charter §7 waitlist accelerator. Public-info-only, earn-don't-
  fabricate, Phase-0 designed-not-executed. Applies existing doctrine; changes
  none.
use_when:
  - Designing or sequencing Forseti's own-growth use of the research engine (outreach inputs, SEO, AEO, competitive CI).
  - Checking how the engine sources the outreach motion's inputs at depth without redoing the motion.
  - Checking the AEO-as-channel vs AEO-as-product-demand-evidence seam before any AEO work.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md   # ratified spine — §3 moat / §4 offer / §5 lanes / §7 gates
  - forseti/product/spines/creator_signal/aphrodite_b2b_outreach_motion_design_v0.md   # the already-designed outreach MOTION (branch claude/aphrodite-b2b-outreach-handoff-fafbe6, PR #802) — referenced, not redone
  - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md   # the engine's signal-structuring instrument (source-family map, Search-Surface MGT route card, AEO-visibility rule)
  - .agents/hooks/check_commission_signal_board_output.py   # the validator that mechanically enforces the AEO-not-demand-evidence refusal
  - forseti/product/spines/creator_signal/aphrodite_growth_strategy_map_v0.md   # EXPLORATORY parent index (§A two-company split, §B buyer ladder, §D capture scope, §F lane index)
stale_if:
  - The charter amends the offer (§4), lead lane (§5), moat protectors (§3), or the foundation exit gate / probe trigger (§7).
  - The CSB prompt/validator changes the source-family map, the AEO-visibility posture, or the Search-Surface MGT route card.
  - product-proof.md or the buyer-proof packet changes the trust/pull/kill/graduation or claim-tier grammar this design consumes.
  - The owner ratifies any part of this GTM design (promote it via a dated charter amendment; then this becomes the applied record).
```

## Status and non-claims

`DESIGN — PHASE-0 (designed, not executed)`. This is a GTM **plan**, not a run.
It **applies** ratified doctrine (charter §3/§4/§5/§7; the parent thesis A1
carve; the CSB evidence/signals-only boundary; product-proof and the buyer-proof
grammar) and **changes none of it**, so it carries **no
`direction_change_propagation` receipt** — the handoff test: a plan applying
existing doctrine carries no receipt; only minting durable own-marketing doctrine
would (flagged in §7, not self-authorized).

Every claim here is capped at `product_learning` tier. This design is not
validation, willingness-to-pay evidence, buyer proof, or judgment-quality
evidence, and it authorizes **nothing executed**: no content published, no
messages sent, no lists uploaded to any tool, no live capture, no scans. Only the
ratified holding page + waitlist are live. Each play's execution keeps its own
gate (§7).

## 0. What this is — and the one line it must never cross

**This is Forseti's OWN growth GTM: Forseti finding and winning its own buyers
and building its own authority — dogfooding the outside-in CI engine on its own
funnel. It is NOT the product surface sold to brands.** The mechanism is one
move repeated four ways: **point our own engine at ourselves** — at our buyers,
at the market's questions, at the answer-engine surface, and at the incumbent.

### Settled anchors (route to these; do not re-derive)

- **Own-growth use is legitimate and distinct from the product's forbidden set.**
  The charter §3 forbidden set (no outreach / contact enrichment / lead-list
  export / person-level directory) governs what the *product* does with
  creator/brand data. It does not restrict Forseti using its own engine for its
  own marketing and CI. The parent thesis A1 carve
  (`docs/decisions/forseti_product_thesis_consumer_demand_v0.md`) already makes
  Aphrodite a bounded *sold* creator-level surface; own-marketing sits further
  inside that carve.
- **Dogfooding doubles as a credibility demo, capped at `product_learning`.** "We
  run our own outside-in CI engine on our own funnel and on our own competitor"
  is a strong story and internal method-learning. It is **not** buyer proof and
  **not** judgment-quality evidence (internal method validation explicitly does
  not count as pull — buyer-proof packet). Tiered honestly, it is a demo asset,
  not a proof claim.
- **The engine is the parent thesis's "outside-in market & competitive
  intelligence"** (buyer-proof packet framing); Aphrodite is its first
  application. Productizing it ("research/CI as a service") is a parent-level,
  **owner-gated** direction — flagged in §7, not designed here.

### The one guardrail: earn, don't fabricate

Research-informed authority content that genuinely earns rankings and citations
is the whole point, and **aggressive, confident copy is wanted.** The single hard
line is **fabricating signal into the public pool**: no astroturfed reviews, no
bought or bot engagement, no sockpuppets, no fake citations or citation rings, no
manufactured social proof. Forseti *detects and discounts* those in the product
(thesis Product Boundary); it never produces them for its own growth. SEO and AEO
**as channels** are legitimate. Everything below earns.

### The AEO seam (load-bearing — keep these two lanes apart, always)

The same AEO / answer-engine surface appears in two completely different roles.
They must never be conflated:

| Lane | What it is | Status |
| --- | --- | --- |
| **AEO-as-product-demand-evidence** | Using "brand X shows up in AI Overviews / is cited by an LLM" as evidence that brand X has real consumer *demand* for a buyer's allocation decision | **REFUSED.** The CSB validator fails any AEO row (`source_family: aeo_answer_engines` or `signal_role: aeo_visibility`) that enters the demand-classifier handoff (`handoff_row_aeo_visibility`). AEO is "visibility annotation only; never an independent demand-origin surface." Changing this needs a Forseti owner decision, not a per-run override. **This refusal stands, untouched.** |
| **AEO-as-own-growth-channel** | Forseti *earning* answer-engine citations to build its own authority and inbound (Play C) | **Legitimate and pursued.** A marketing channel, measured as a marketing KPI. |

Play C lives entirely in the second lane. Even when the engine is pointed at
CreatorIQ's AEO footprint for competitive CI (Play D), those AEO reads inform
*our own positioning* — they are never fed as product demand evidence into any
buyer's demand-classifier handoff. Same discipline, cleanly separated.

## 1. The engine, as a reusable own-growth input machine

The product engine is a three-link chain:

```text
CSB  →  Capture  →  creator_signal
(structure the      (retrieve public   (derive claim-object
 signal request)     bytes, ToS-gated)   reads / panels)
```

For **own-growth**, the reusable core is the front of that chain used as a
**structured public-signal retrieval scaffold** — deliberately *without* the
product-surface tail:

- **CSB gives the structure**: the source-family / subfamily map (forums-community,
  reviews, creator-social-video, retail-PDP, search-discovery, AEO-visibility,
  news-editorial-trade, professional-org-motion, owned-channels), signal rows,
  mandatory counterevidence paths, campaign/duplication-risk checks, the
  graph-light retrieval brief, the Search-Surface MGT route card, cutoff
  discipline, and provenance labels. CSB is signals-only and authorizes **no
  retrieval** — it structures the request.
- **Capture retrieves** the public bytes, through the Source Capture Armory Runner
  Ladder (safety-rules), ToS-gated, at the charter's measured-risk posture. This
  design assumes only *public* retrieval and authorizes none; any scale-up beyond
  charter §6 media-light scope carries the growth-map §D flag (§6 amendment + ToS
  re-gate).
- **creator_signal derives** the claim-object reads — the same
  provenance-stamped, missingness-honest derivation the product uses (the five
  panels; the fragrance ontology of houses / notes / accords / dupe-relationships
  / scene vocabulary).

**The seam that keeps own-growth clean of the product surface:** the CSB
**Section 8 demand-classifier handoff is NOT invoked for own-growth
commissions.** That handoff exists to package a *buyer's* demand decision — a
product-surface object. Own-growth research has no buyer demand decision, so the
board runs in *collection* mode (`board_status: COLLECTION_BOARD_ONLY` /
`READY_FOR_RETRIEVAL_HANDOFF`) and its Section-8 tail is N/A. We consume the
board's coverage plan, signal rows, counterevidence, and graph-retrieval brief as
a **research/retrieval scaffold**. This is *why* the AEO-not-demand-evidence
refusal never even has to fire in own-growth work: there is no demand-classifier
handoff to protect — and we still honor the underlying principle (AEO is
visibility, never demand-origin).

Each play below is one or more CSB commissions in this collection mode, with the
`decision_context` re-pointed from "a buyer's allocation decision" to "a Forseti
own-growth decision." The input illustrations are **design**, not runs.

## 2. Play A — Engine → B2B outreach inputs, at depth

**The outreach MOTION is already designed** in
`aphrodite_b2b_outreach_motion_design_v0.md` (branch
`claude/aphrodite-b2b-outreach-handoff-fafbe6`, PR #802): who to approach first
(creator-native indie/clone DTC houses), the demonstrating public-info-only
first-touch (a miniature company-personalized fit-read — "medium is the moat"),
the qualify/kill bar, and the Phase-0 "designed, not sent" boundary. **This play
does not redo it.** It designs how the ENGINE sources and scales that motion's two
input layers at depth.

### A1. Target discovery — the engine finds who to approach

A CSB commission **per candidate sub-niche**, in collection mode:

```yaml
candidate_or_subject: <target sub-niche, e.g. "clone/dupe fragrance houses in the [note-family] segment">
decision_context: >
  Own-growth outreach targeting — surface indie/DTC/clone-house brands with
  (a) live creator-spend / launch / which-original-to-chase decision pressure,
  (b) visible creator-seeding budget-adjacency, (c) a publicly reachable founder /
  decision owner, (d) registry corpus-depth sufficient for a non-embarrassing fit-read.
mode: forward
# source families that carry the four target-pick signals:
#   creator_social_video + forums_community  -> rising dupe/review content = live decision pressure ("the niche is hot")
#   creator_social_video (disclosure markers) -> affiliate codes / gifted-PR = budget-adjacency + likely trust_open
#   professional_org_motion + owned_channels  -> founder public posts = reachability
#   search_discovery                          -> category heat (source-route scout, NOT rank-as-proof)
#   retail_pdp + owned_channels               -> the brand exists / assortment / is real
# Section 8 demand-classifier handoff: N/A (own-growth collection board)
```

The board's coverage plan + signal rows become the **qualification scaffold** for
motion §1's target-pick signals; the mandatory counterevidence rows guard against
a false "hot niche" read (creator-cluster / affiliate-campaign concentration
masquerading as organic demand — CSB campaign-and-duplication-risk section). The
output is a screened target batch, not a lead list.

### A2. Demonstration content — the engine fills the first-touch at depth

The motion's first-touch **is** a public-info-only mini fit-read (Panel 1 Fit +
a sliver of Panel 5 Momentum), every element a claim object with provenance
receipt + freshness + named missingness. `creator_signal` derivation **fills that
spec's slots from the registry** — segment share of recent content, audience
taste from comment language (collector vs dupe-seeker), proven adjacency vs the
creator's own baseline, niche-share momentum — each receipt-stamped, with at least
one honest withhold actually displayed.

**Where the engine's depth is the differentiator:** because the registry is
niche-complete and ontology-deep, the target batch is *exhaustive-within-niche*
(not a shallow keyword scrape) and every demo read is receipt-stamped and
missingness-honest — a quality no generic prospecting tool matches. **The engine
scales input DEPTH, not outreach volume.** That is exactly what preserves "medium
is the moat": each first-touch stays hand-made and singular (batch → grade →
graduate/park; no mail-merge, no CRM, no list uploaded), while the engine makes
each one's slots fillable at a depth a template can't mass-produce. A non-marketer
fills a repeatable spec; the persuasion lives in the artifact.

**The firewall (motion §0, enforced by the engine's own forbidden set):** the
engine delivers a *derived decision read to a brand* — never a creator contact
list or person-level data by default. A separately negotiated strategic raw
registry transaction is allowed under the charter's price/rights boundary; it
is not smuggled into an ordinary first-touch or Signals read. If a target asks
for contacts, person-level fields, or unrestricted redistribution, route that
as a distinct rights-and-commercial decision. Studio maintains its own
legitimately obtained creator relationships; it does not inherit a Signals
contact dump.

**Gate:** this document's candidate Vetting Sprint outreach remains
designed-not-sent until D-1 fires and the owner opens that buyer-contact lane
(charter §4/§7). D-1 does not gate every possible Signals shortlist, ranking,
or decision-read unit; each still needs its own commercial/contact authorization.

## 3. Play B — Engine → SEO authority content that genuinely earns

Two engine uses, in sequence.

### B1. Learn what the market actually asks and what currently ranks

A CSB commission in **market-language / content-demand** mode:

```yaml
candidate_or_subject: <a sub-niche content target, e.g. "[note-family] dupes vs originals">
decision_context: >
  Own-growth SEO topic selection — surface the questions buyers and the market
  actually ask, and what currently ranks, to select authority-content topics we
  can genuinely earn.
mode: forward
# signal-bearing families:
#   forums_community  -> Reddit/Basenotes/Fragrantica repeat questions, objections, comparisons = real demand for answers;
#                        UNANSWERED repeat questions = content gaps (the highest-value topics)
#   reviews           -> recurring complaints / pain points = problem-shaped queries
#   search_discovery / search_surface_mgt -> query language, PAA/PAS, autocomplete, hidden-venue pointers, what ranks
#   creator_social_video -> trending clusters = topical timing
#   news_editorial_trade -> industry framing / vocabulary
# Section 8: N/A (collection board)
```

The **Search-Surface MGT route card** is built precisely for this: it points to
preserved SERP packets as *routing evidence* and routes execution to
Scanning/Capture — and it **never treats query count, SERP rank, module
recurrence, or autocomplete as proof.** The seam to hold: for SEO we consume
query/question *language* as **content-demand input** (legitimate); we never
launder SERP rank into a *product-demand* proof (forbidden, and a different lane).

Topic selection is driven by, in priority order: (1) forums' **unanswered** repeat
questions (content gaps the niche is actively asking about); (2) search query
language (raw demand); (3) review complaints (problem-shaped topics); (4) creator
clusters (timing); (5) the incumbent's content gaps (Play D — where CreatorIQ is
absent on niche-deep questions).

### B2. Design the content that earns the ranking

- **Provenance-rich format = the product's epistemics, published.** Every
  fragrance fact is a claim object: value + provenance receipt (source / date) +
  freshness + sample support + **named missingness**. Depth-honesty is the
  product *and* the content differentiator. The fragrance ontology (houses, notes,
  accords, dupe-relationships, scene vocabulary) over entity-resolved,
  receipt-stamped derivation is content **no horizontal competitor can match** —
  which is *why* it earns rank: it is the best, deepest, most-verifiable answer,
  not thin SEO chum.
- **Cadence driven by momentum/breakout signals.** Publish depth where a sub-niche
  is heating (the same breakout detector that feeds the product's momentum panel)
  **and** the corpus is deep enough for a non-embarrassing read (the depth-honesty
  screen — never ship a shallow authority piece; a shallow demo contradicts the
  moat, motion §1).
- **Earn-don't-fabricate line:** content earns rank by being the best answer. No
  bought links, no fabricated reviews, no astroturf, no manufactured signal into
  the pool. Aggressive, confident, deep copy — earned.

Publishing is a gated lane (charter §10 keeps publishing gated). This play
**designs** the topic-selection engine and the content format; it publishes
nothing.

## 4. Play C — Engine → AEO earned citations

**Goal:** be the source answer engines cite for fragrance and creator-intelligence
questions. This is Play B's content, structured for citation and measured as a
channel.

- **Structure + provenance density = what answer engines cite.** Answer engines
  favor structured, entity-dense, directly-answering, provenance-rich content. The
  entity-resolved fragrance ontology plus claim-object provenance density *is* that
  substrate. Structure the Play-B content for citation: entity-resolved anchors,
  direct Q&A shape, receipts, explicit scope/missingness (which reads to a citing
  model as authority and caution, not weakness). Being the receipt-stamped niche
  authority on questions the incumbents cover shallowly earns the citation.
- **Earn-don't-fabricate line (sharper here):** earn citations by being genuinely
  the best-structured, most-provenance-dense source. **No fake citations, no
  citation rings, no sockpuppet authority, no astroturfed "sources."**
- **The seam (restated, because this is where it is easiest to slip):** Play C is
  strictly **AEO-as-channel** (§0 table, second lane). Earned-citation counts are
  a **marketing KPI** — "are we cited, for which queries, vs the incumbent" — and
  are **never** written back as product demand evidence, never a CSB Section-8
  handoff row, never an input to a buyer's demand read. The CSB AEO-visibility
  refusal is untouched and un-invoked (own-growth boards don't produce that
  handoff).

Phase-0 designs the structure and the KPI; it earns nothing yet (publishing
gated).

## 5. Play D — CreatorIQ (and peers) outside-in competitive intelligence

**Public information only.** No private/non-public data on CreatorIQ or anyone.

Point the engine at the incumbent — a CSB commission with the incumbent as
subject:

```yaml
candidate_or_subject: CreatorIQ  # then Traackr / peers
decision_context: >
  Own competitive positioning — where is the incumbent structurally weak
  (fragrance / niche depth), what do they rank for and get cited for, and where
  are the niche-depth gaps we can out-content and out-rank?
mode: forward
# public-surface families only:
#   owned_channels        -> their site, blog, case studies, public pricing, positioning language
#   search_discovery      -> the queries they rank for — and the niche-deep queries they DON'T
#   aeo_answer_engines    -> what answer engines cite them for — and the note-level / dupe-relationship questions they're absent from
#                            (AEO-as-channel/CI lane; never product-demand evidence)
#   news_editorial_trade  -> category positioning
#   professional_org_motion (ATS/careers) -> are they hiring for fragrance-vertical depth? (public postings only)
# Section 8: N/A (collection board)
```

**The structural-weakness thesis is already ratified (charter §3) — consumed, not
re-derived:** horizontal-breadth players index breadth shallowly; per-vertical
depth is economically irrational at horizontal scale; they will not *sustain*
per-vertical depth because it is off-core and a distraction from their core.
Forseti's niche-complete roster + ontology + stamped derivation is depth they
won't chase. The engine's public **org-motion** read is the confirmation: if
CreatorIQ's careers pages show no fragrance-vertical-depth hiring, that is public
evidence the depth is off-core for them.

**How Forseti out-contents and out-ranks:** aim Plays B + C precisely at the
niche-depth gap the CI surfaces. The incumbent ranks and is cited for generic
"influencer marketing platform / creator discovery"; Forseti wins the niche-deep
queries — *"best fragrance creators for [note family]," "who's driving the [X]
dupe wave," "is [sub-niche] already saturating"* — the exact reads the product
produces. This is a **displacement** posture on the niche they can't sustain
(growth-map §B), not a greenfield fight on their turf.

**This play IS the parent thesis's outside-in market & competitive intelligence,
run on our own positioning** — the clearest dogfood. It doubles as a credibility
demo, capped at `product_learning` (we use the engine we sell); it is not buyer
proof or judgment-quality evidence.

## 6. Play E (optional) — Inbound → the charter §7 gate accelerator

The inbound plays close a loop back onto the charter's own acceleration mechanism:

```text
Play B/C authority content  →  inbound interest  →  waitlist signups
   (SEO + earned AEO citations)                     (with role + decision-type fields, charter R-2)
        →  a QUALIFIED waitlist-inbound buyer signal  →  can pull D-1 forward
        →  the six-criteria dress rehearsal becomes the first design-partner Sprint prep (charter §7 accelerator)
        →  first paid Signals decision read (shortlist/ranking or candidate Vetting Sprint)
```

**Honest tiering (the trap to avoid):** a waitlist signup is inbound *interest* —
a pull-signal **candidate**, not pull. Per product-proof and the buyer-proof
packet, curiosity / generic interest / "send me more" is **not pull**; pull is
paid-path behavior. A signup only becomes the accelerator when it **qualifies**:
a named decision owner, a live creator-spend/launch/which-original-to-chase
decision, a real allocation consequence, not `trust_refusal`, publicly reachable
(motion §3 bar). So the inbound plays *feed the top of the accelerator's funnel*;
they do not discharge the D-1 gate — the six criteria and the owner's separate
probe-opening still hold.

## 7. Cross-cutting discipline, seams, and owner-gated flags

### Claim discipline (everything `product_learning`-capped)

- Dogfooding = internal method validation = `product_learning`; explicitly **not
  pull, not buyer proof, not judgment quality**.
- Earned rankings / citations / inbound = **marketing KPIs**, never buyer proof,
  WTP, or judgment-quality evidence.
- No new vocabulary or doctrine minted: trust classes, pull/praise, the A/B/C/D
  rubric, the graduation anchor, the source-family map, and the AEO posture are
  all consumed from source.

### Seams respected

- **CSB structures** (signals-only; no retrieval). **Capture retrieves**
  (ToS-gated armory runner ladder; public only; scale-up beyond charter §6
  media-light carries the growth-map §D §6-amendment + ToS-re-gate flag).
  **creator_signal derives.**
- **The demand-classifier handoff (CSB Section 8) is never invoked for own-growth
  commissions** — that is the product surface. Own-growth boards run in collection
  mode.
- **The AEO two-lane seam (§0) is standing law for this lane:** channel/CI use is
  pursued; product-demand-evidence use is refused, untouched.
- **Public information only** for all CI (Play D and every board).

### Phase-0 boundary

Design only. Nothing published, sent, uploaded, scanned, or captured. **Each
play's execution keeps its own gate:** outreach send (charter §4/§7: D-1 fires +
owner opens probes); publishing (charter §10 gated); live capture / any
scale-up (capture lane + growth-map §D). No runtime-model-routing recommendation
is made anywhere in this design.

### Owner-gated flags (flagged, NOT decided or designed here)

1. **CI-as-a-service** — productizing the engine as "research/CI as a service" is
   a parent-level, owner-gated direction. Flagged only.
2. **Generalizing engine → own-growth GTM into a Forseti-wide own-marketing
   pattern** (beyond Aphrodite/fragrance) — this design is Aphrodite-instantiated;
   promoting the pattern org-wide is owner-gated and would carry a
   `direction_change_propagation` receipt.
3. **Promoting "earn, don't fabricate" to a Forseti-wide own-marketing
   invariant** — applied here as this lane's guardrail; elevating it to a durable
   repo-wide invariant is a doctrine change (DCP receipt, owner-gated).
4. **Publishing authorization** — actually publishing SEO/AEO content is Phase-1+
   and separately gated.
5. **Capture scope for market/CI/SEO research beyond charter §6 media-light + the
   measured-ToS posture** — capture-lane decision + §6 amendment + ToS re-gate
   (growth-map §D).

## 8. Where this sits

- **Anchor:** the ratified charter (on main). This design is an EXPLORATORY design
  lane artifact, sibling to `aphrodite_b2b_outreach_motion_design_v0.md`, applying
  ratified doctrine and minting none.
- **Index:** listed in the creator_signal spine README "Current artifacts" table
  and in the growth-map §F design-lane index.
- **Relationship to the outreach motion:** Play A references and depends on the
  motion design (PR #802, off-main at authoring); it designs the engine feed, not
  the motion.

## 9. Amendment 2026-07-10 — Cross-vendor adjudication (ChatGPT Pro return, MGT/SCI) + owner refinements

Provenance: a de-correlated ChatGPT Pro GTM return (commissioned generatively, blind
to this design) was adjudicated by the home model under the Mini God Tier + Smallest
Complete Intervention lenses, and the owner ruled on each point (2026-07-09/10). The
return independently reproduced this design's spine (engine-as-instrument, the AEO
channel-vs-demand-evidence seam, authority-via-method-not-directory,
strategic-registry boundary,
phase/gate discipline, inbound loop, the owner-gated flags). The kept deltas +
owner rulings below refine the plays above. Still Phase-0, `product_learning`-capped,
public-info-only, earn-don't-fabricate; the charter §5 wedge sharpening is *applied*
as a first-batch selector, not self-ratified.

### Play A — outreach

- **Sharper first cohort:** within the ratified lead lane, approach FIRST the
  dupe / clone / affordable / creator-commerce fragrance brands that are *visibly
  commercially creator-exposed* — TikTok Shop presence, affiliate codes, scent-
  comparison content, fast saturation. Discriminator: creator spend is close enough
  to revenue that a wrong pick hurts, AND the decision leaves public traces. (Applied
  as the first-batch selector; folding it into charter §5 is owner-gated.) Affiliate-
  code *conversion rate* is **not** publicly measurable (private backend) — show it as
  named missingness; TikTok Shop public "units sold" belongs to the TT-Shop lane.
- **"Buyer Signal Board" is core:** a CSB pointed at a brand *account* (not creators)
  to qualify a live creator-spend decision. Core job includes mapping **everything a
  brand is publicly sponsoring in-niche right now** (disclosed #ad / gifted-PR /
  affiliate codes) — delivered as a read/pattern (footprint, saturation), never a
  contactable roster; doubles as competitive intel ("your rival already locked these
  creators in your lane").
- **Contradiction-first first-touch:** lead with ONE receipt-stamped contradiction the
  founder can act on + one decision question that forces pull-vs-praise. **Hold the
  counter-case** — do not proactively surface counterevidence; if the buyer raises the
  objection, that is a qualifier and tells us what to counter. Honesty stays on the
  claims we *do* make (real, receipt-backed, missingness shown); we just don't volunteer
  the rebuttal in a teaser.
- **Sell to the growth / ecommerce owner, not the influencer-marketing seat.** The
  execution seat wants lists/workflow (and may see us as a rival or a list to extract);
  the growth/ecommerce owner owns the spend-risk — the decision-read fits their job.
  Real qualifier = who owns the spend outcome (a small-brand founder may wear both hats).
- **Batch, not blast:** a bounded first batch (~10–20 to test the wedge; hand-build
  ~3–5 first-touches), not 30–50; single-operator posture, no CRM/list-upload.

### Play D — competitive positioning

- **Complement, not attack:** position as the narrower / deeper / decision-specific
  *preflight before you brief or pay creators* — "they run broad creator programs; we
  do fragrance-specific creator-spend judgment." Never "CreatorIQ/Traackr are shallow"
  (indefensible + overclaim). Displacement is on the niche-depth *decision*; complement
  to their workflow system-of-record.
- **No standing CI board:** competitive CI here is a one-time positioning input +
  refresh-on-trigger, not a standing monthly board. A standing competitive-intelligence
  board is a *separate lane with its own revenue* (see CI-as-a-service, owner-gated) —
  out of this GTM lane.
- **External competitor/market stats are advisory until verified:** do not build
  positioning on a competitor's self-reported numbers unchecked; verify at source before
  any becomes load-bearing. TikTok-Shop-specific facts come from the TT-Shop lane.

### Play E — inbound → gate

- **Waitlist = decision-intake:** collect role / company-type / decision-type / timing /
  channel / readback-willingness. A qualified inbound (named owner + live dated decision
  + readback-willing) can pull the charter §7 foundation gate forward; a signup alone is
  a pull *candidate*, not pull.

### Cross-cutting owner rulings

- **Activation economics (optional intake):** a correct public read can still be
  commercially miscalibrated without a few private constraints (margin, inventory, creator
  rate card, TT-Shop fees, launch timing, goal). At sprint time an **optional** ~6-field
  intake (goal / channel / SKU / budget-band / inventory / brand-safety) sharpens it.
  **Boundary:** the public read must stand alone — never *require* private data before it
  is useful (that is a buyer-proof disqualifier). **Roadmap (owner north-star):**
  integrating the buyer's internal data to reach highest-EV decisions is the *goal* once
  they are a paying customer; the public read wins the door first, and the integration
  *build* stays gated.
- **Sell derived value by default; price the raw asset strategically:** the ordinary
  high-revenue products remain the *derived read / ranking* ("name the creators that
  matter for segment X") and controlled query access. A private raw-registry export is
  also allowed when an owner-approved price and rights package compensates for lost
  exclusivity, buyer reuse/redistribution, competitive leakage, and foregone recurring
  revenue. Contact/person-level fields remain separately rights-gated. Do not confuse an
  exceptional asset transaction with a cheap first-touch export.
- **Segment rankings yes, vanity score no:** "best creators for [segment/decision]" as a
  receipt-backed, missingness-honest decision read (the fit matrix) is the product. The
  forbidden things are the single context-free vanity score (Traackr-style VIT) and a
  public standing creator directory — keep rankings as buyer decision reads, not a
  published "Aphrodite Top 50."
- **Bounded depth beats scale:** buyers need bounded, in-depth information, not scale of
  data — this *is* the moat (depth over breadth) and why cheap-capture-at-scale is
  unnecessary.
- **SEO/AEO build order:** build the topic-selection *engine* + 1–2 exemplar page specs
  now; do not pre-draft a large authority backlog ahead of the (gated) publishing
  authorization.

### Ratified direction with execution still owner-gated

- **Aphrodite Studio** is an independent revenue lane over the same evidence asset; it
  does not wait for a Signals sale or repeatability. Internal design/setup may begin now.
  Creator-facing execution still requires a named creator opportunity, defined service,
  usable evidence, an operational neutrality firewall, and separate execution
  authorization. A first client additionally requires independent creator opt-in,
  explicit service/compensation, and an engagement-specific conflict check.
- **CI-as-a-service / research-for-hire:** a separate Forseti branch, after CI + Aphrodite
  prove out; owner-gated.
