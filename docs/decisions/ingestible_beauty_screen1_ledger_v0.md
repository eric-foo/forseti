# Ingestible Beauty Screen 1 Ledger v0 (guide generalization run)

```yaml
retrieval_header_version: 1
artifact_role: Decision record (screen ledger; batch provenance home)
scope: >
  Ledger for the vertical exploration guide's first run on a second vertical (Vertical)
  (ingestible beauty / nutricosmetics, 2026-06-12): half-budget cold walk, one
  agent, guide as written. Records candidates, influence observations
  (including two new wind-caller (WindCaller) types), the stop contract's first clean
  in-walk firing, the WebFetch/Reddit tooling discovery, and generalization
  findings. Promote-on-reuse counter for this vertical: 1 of 3.
use_when:
  - Step 0 prior-provenance reads for any future ingestible-beauty/wellness screen.
  - Assessing whether the guide generalizes beyond beauty (this is the first evidence).
  - Routing Reddit access for screening agents (see the tooling discovery).
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md      # the guide this run proved
  - orca/product/satellites/beauty/beauty_venue_card_set_v0.md                # adjacent vertical's promoted deck (shared hub observed)
  - docs/decisions/beauty_subtle_decision_screen3_ledger_v0.md         # prior screen (rules this run inherited)
stale_if:
  - A backtest batch admits or rejects these candidates.
  - The promote-on-reuse trigger fires for this vertical (3rd screen).
```

## Status And Authorization

Owner-authorized in-thread 2026-06-11 ("let's do that", with direction
guidance: beauty stays the focus; pick adjacent lanes within consumer demand).
Executed 2026-06-12 by the pre-capture discovery CA lane: ONE cold Sonnet-class
web-research agent, guide as written, half budget. First run of the guide on a
vertical that is not beauty; first deployment of the hard per-move stop
self-check (the screen-3 breach fix); first live test of venue-dry counting.

## Batch Plan (bound before the run)

- Direction: ingestible beauty / nutricosmetics (collagen, skin/hair/nail
  supplements, beauty gummies) x consumer-demand decisions, any family.
  Beauty-adjacent per owner direction; on-wedge (consumer demand).
- Candidate target: 3. Influence target: hub read + >=2 wind-callers with
  receipts. Budget: 1 agent, <=10 moves, stops = 3 candidates / two
  consecutive VENUE-DRY moves / cap. Access failures = access notes (count
  toward cap, not toward the dry stop) — the venue-dry amendment, live.
- Ride-along: old.reddit search-surface receipt GET (capture-lane residual).
- Step 0 state (honest): no prior provenance for this vertical; beauty trail
  adjacency noted but cold hub-finding required.

## Result Against Targets

- Candidate target EXCEEDED: 4 against a target of 3 (stop fired at move 6 of
  <=10).
- Influence target MET: 3 hub observations + 2 wind-caller observations with
  receipts — including two NEW wind-caller types (regulator; retail
  gatekeeper).
- STOP CONTRACT: first clean in-walk firing across all screens — the per-move
  self-check ran visibly in the move log (stop_check column) and the walk
  halted at condition (a) without orchestrator intervention. The screen-3
  breach fix is validated in its first deployment.
- VENUE-DRY STOP: still never fired — the vertical proved yield-rich through
  the shared brand-story hub. The dry rule remains untested; honest gap.
- Receipt ride-along: NOT COMPLETED — see the tooling discovery below.

## Candidates (screen output — admitted to NO batch)

| # | Brand | Decision (DecisionEvent) | Date | Note |
| --- | --- | --- | --- | --- |
| 1 | Sundaily (ex-Sundots) | Full pivot: UV-protectant ingestible repositioned to skin-health gummy brand; Goop distribution followed | 2018–2019 | moderately obscure; clean arc |
| 2 | Manifesto (UK eco-luxe) | Regulatory-forced reformulation: titanium dioxide removed (France E171 ban), 6-month delay accepted for EU access; Cult Beauty entry followed | ~2021 | CLEANEST: hard dated forcing function, visible tradeoff, revealed outcome; quite obscure |
| 3 | The Nue Co. | Pivot OUT of supplements toward fragrance (fragrance 20%→65% of revenue; CAC halved; Ulta exclusive) | 2019–2024 | boundary ruled IN: exit decisions BY ingestible brands are consumer-demand decisions par excellence |
| 4 | Kalumi BEAUTYfood | Pandemic reformulation + downward repricing (MCT added while price cut — margin-for-volume tradeoff) | ~2021 | WEAK flag: snippet-grade action receipt; needs source-depth check before any batch use |

Receipts: beautyindependent.com articles (Sundaily/Goop; Manifesto eco-luxe;
The Nue Co. functional fragrance; Kalumi 2017 profile), pitchbook.com (Nue Co),
amazon.com ASIN (Kalumi reformulated listing).

## Screen Provenance (batch record — NOT a standing source map)

- Screen run 2026-06-12 by one cold web-research agent; every candidate
  URL-backed; no capture.
- Venues (Venue) that produced candidates or evidence: Beauty Independent (the
  brand-story hub — ALL four candidates trace through it; its ingestibles
  category page is the vertical's richest screen surface), BeautyMatter
  (corporate events: Care/of shutdown), PitchBook (funding context), Amazon
  listings (reformulation evidence).
- VENUE-DRY (walked, yielded nothing for brand decisions): cosmeticsdesign.com,
  happi.com, nutraceuticalbusinessreview.com, nutritioninsight.com — all are
  ingredient/market-size trade press, not brand-decision press.
- Rejected negative set: Care/of (Bayer $225M — too prominent; shutdown June
  2024 noted), AG1/Ritual/Olly/Goop/Vital Proteins/SugarBearHair/Hims (excluded
  famous), Moon Juice + Seed (flagged, not walked), Lux Beauty Club Botanicals
  (single-mention source depth — insufficient), Aubrey Organics (not
  ingestible), Clarisonic (device), Neutrogena Skinstacks (too prominent).
- Access notes: old.reddit.com AND www.reddit.com BLOCKED at the agent-tool
  level (see tooling discovery); site:reddit.com search operator returned
  zero results; podfoods.co login-gated; pointer-only socials skipped per
  policy.
- Boundary: batch provenance only; no standing source map, inventory, monitor,
  or crawler.

### Influence Observations (dated 2026-06-12; history, never current-state claims)

Hubs:

- Beauty Independent is the brand-story hub for THIS vertical too — the same
  outlet that anchors the beauty card-set. Cross-vertical hub observation:
  adjacent consumer-demand verticals appear to share the brand-story trade
  layer. Its /brands-products/ingestibles-supplements category page is the
  vertical's Dish-equivalent surface.
- BeautyMatter covers the corporate-events layer (closures, funding) the
  brand-story layer misses.
- Ingredient/market trade press (cosmeticsdesign, happi, nutritioninsight) is
  a DISTINCT non-producing layer: market sizing and launches, never brand
  decisions. See Generalization Findings.

Wind-callers — two NEW types observed:

- REGULATOR-AS-WIND-CALLER (WindCaller): France's ANSES E171 (titanium dioxide) ban, then
  the EU-wide ban — a hard, dated forcing function the vertical visibly
  responded to (Manifesto's forced reformulation + delay). Regulatory events
  are clean wind-callers: dated, documented, and they move every exposed brand
  at once.
- RETAIL-GATEKEEPER-AS-VALIDATOR (WindCaller): Goop's stocking decisions function as demand
  validation that moves brand narratives and retail access (Sundaily's pivot
  outcome was evidenced BY its Goop listing).
- Both fit the guide's existing wind-caller definition ("actors whose words or
  actions the vertical visibly responds to") — vocabulary examples, not a rule
  change.

## Tooling Discovery (reframes the Reddit residual)

The agent could not reach old.reddit.com OR www.reddit.com: the WebFetch tool
itself refuses the domain ("Claude Code is unable to fetch from
old.reddit.com"). This is an AGENT-TOOLING constraint, not a Reddit-side block:
the capture lane's HTTP runners fetch these surfaces fine (their receipts
exist). Consequence for screening:

- The capture lane's GO read shape is GO for capture-harness runners, but
  UNUSABLE by WebFetch-based screening agents.
- The search-surface receipt residual is therefore not closable by a screening
  agent at all; it needs one bounded GET from the capture lane's runner, OR
  screening walks route their Reddit reads through that runner as a
  screening-read service (a cross-lane wiring question, owner/capture-lane
  gated).
- Until then: Reddit origination reads in screens = search snippets only.
- The beauty card-set cards 4–6 carry this caveat as of this screen (dated
  update applied same turn).

## Generalization Findings (what this run proved about the guide)

- Cold hub-finding WORKS on a new vertical: the agent found the vertical's own
  hub structure and 4 candidates in 6 moves with no inherited trail.
- The stop contract WORKS as a hard per-move self-check (first clean firing;
  executor honored it without intervention).
- Venue-dry counting ran live (ingredient-press moves correctly classified
  VENUE-DRY; reddit blocks correctly classified ACCESS-NOTE, not dry) — but
  the two-consecutive-dry STOP never fired; still untested.
- PROPOSED-NOT-APPLIED (owner-gated; twice-observed, beauty + here): subdivide
  Step 2 move 1 "vertical trade press" into (a) brand-story/founder-narrative
  press (yields decisions: Beauty Independent, BeautyMatter) vs (b)
  ingredient/market-size press (yields market context, never decisions). Walks
  should weight (a). One dated clause if accepted.
- Obscurity gradient note: this vertical clusters bimodal (very famous vs
  thinly documented); the middle tier (Nue Co., Sundaily) is the richest zone
  for reconstructable decisions — consistent with the finder frame's
  not-too-prominent operative bar.
- Promote-on-reuse counter: ingestible beauty = screen 1 of 3.

## Wedge Relevance (product-learning raw material, NOT ICP validation)

The screen evidences that the consumer-demand signal substrate exists in an
adjacent vertical: demand-forced decisions (DecisionEvent) (pivots, forced reformulations,
repricing) are reconstructable outside-in, with influence structure including
regulatory and retail-gatekeeper movers. This is substrate-breadth evidence
the wedge-ratification work may consume as input. It is not validation,
willingness-to-pay, or buyer proof.

## Non-Claims

Not validation, readiness, buyer proof, or judgment-quality evidence.
Candidates admitted to no batch; recognition checks not run; Kalumi flagged
for source depth. No capture performed or authorized; the Reddit wiring
question routes to owner/capture lane. Creates no registry, atlas, or monitor.
The proposed trade-press subdivision changes nothing until owner-accepted.

## Lane Note

Executed by the pre-capture discovery CA lane under owner in-thread
authorization. Uncommitted at close (no commit instruction this turn).
