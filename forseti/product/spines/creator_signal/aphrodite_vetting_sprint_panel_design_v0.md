# Aphrodite Vetting Sprint — Five-Panel Design v0 (Mini God Tier)

```yaml
retrieval_header_version: 1
artifact_role: Product design record (adjudicated display design for the five sprint evidence panels; owner-invoked Mini God Tier lens)
scope: >
  The adjudicated display design for the five Vetting Sprint evidence panels
  (fit, ad-reception, purchase-intent, brand adjacency, momentum), with the fit
  panel specified in depth: the fit matrix, the dupe-space roll-up rule,
  buyer-segment lead variants, and gameability countermeasures. Elaborates the
  charter §4 panel definitions into a buildable display target for the
  depth-layer build and the D-1 dress rehearsal. Mini God Tier design: accepted
  residuals are named below; this record asserts no validation or readiness.
use_when:
  - Building or scoping the depth-layer extractor's display output (what the panels must render).
  - Preparing or grading the D-1 dress-rehearsal sprint report.
  - Checking what a panel may show, downgrade, or must withhold.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md            # §4 panels, §5 buyer lanes (owns strategy; this record elaborates display)
  - forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md  # the claim-object discipline every row obeys
  - forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml            # the ontology substrate fit resolves against
  - docs/prompts/handoffs/aphrodite_depth_layer_build_handoff_v1.md                   # the build this record gives a display target to (v1 supersedes v0)
stale_if:
  - Charter §4/§5 or the provenance contract is amended in a way that changes a panel's obligations.
  - The D-1 gate decision adopts different rehearsal criteria than this design assumes.
  - A later accepted design record supersedes this one.
```

## Status and provenance

`ADJUDICATED_DESIGN_2026-07-05` — cross-vendor enrichment proposal (OpenAI
ChatGPT Pro, commissioned over a 6-file source pack: charter, two panel
rehearsals, round-2 share-of-voice record, fragrance reference data, provenance
contract; delivered in-chat 2026-07-05) adjudicated by the home lane under
Smallest Complete Intervention and the owner-invoked Mini God Tier lens
(`docs/decisions/forseti_mini_god_tier_doctrine_v0.md`). All proposal elements were
accepted or accepted-with-modification; none rejected structurally; the two
modifications and all accepted residuals are recorded below. Design record
only: not validation, not readiness, `product_learning`-capped; authorizes no
build (the depth-layer build stays gated on its own handoff + D-1).

## 1. Panel-wide rules (all five panels)

- **Panels, never scores.** No composite/vanity number anywhere; every panel is
  a set of independently-evidenced rows.
- **Every row is a claim object** per the derived-claim provenance contract
  (pointer, not restated here): source refs, extraction provenance, receipt,
  confidence-or-abstention, and a per-row posture of `show | downgrade |
  withhold`. Missing evidence displays as named missingness, never zero.
- **Coverage is not endorsement:** stance mix is always displayed separately
  from presence and attention.
- **Freshness is displayed, not implied:** capture dates and window state on
  every panel; single-window reads that claim trend behavior downgrade.

## 2. Fit panel (the lead panel for every buyer segment)

**Form: a fit matrix.** Independent evidence rows for the buyer's product or
demand-space — each resolving to show/downgrade/withhold on its own:

| Row | What it shows |
| --- | --- |
| Presence × attention × stance | The per-product/demand-space triple (the round-2 SoV finding): videos, deduped product×video mentions, captured views, attention share, stance mix. Never a single ranked SoV number. |
| Note-family overlap | Buyer note families as individual chips: `observed with receipts` / `observed only via adjacent products` / `withheld — not observed in captured corpus`. |
| Tier alignment | Creator's attention-weighted and editorial coverage distribution across the ontology tier vocabulary, displayed separately from note overlap. |
| Dupe-space adjacency | Direct-original evidence and clone-tail evidence as SEPARATE sub-blocks (rule in §3). |
| Comparable-brand baseline | Buyer-comparable content performance vs the creator's OWN baseline (never vs other creators); withheld when no comparable content or baseline history exists. |

**Buyer-segment lead variants** (reading order for the whole report in §6):

- **Dupe-first / clone house:** lead with original demand-space fit — direct
  original attention + clone-tail attention + stance toward each + mapped clone
  count + attention concentration. Answers "does this creator already create
  exposure around the original's demand-space."
- **Creator-owned DTC founder (pre-launch):** lead with buyer-supplied product
  coordinates (note families / occasions / tier of the planned scent) overlapped
  against the creator footprint; the concept displays as provisional
  coordinates, never as an observed market fact; absent coordinates → rows
  withheld, not guessed.
- **Niche / pre-designer indie house:** lead with tier + note-family alignment,
  then comparable-brand baseline; designer-head attention must not mask weak
  niche evidence.
- **Agency (conditional lane, client decision-owner present per charter §5):**
  same fit matrix framed on the client's product coordinates.

## 3. Dupe-space roll-up rule

For original product `O`: demand-space `D(O) = {O} + every product P whose
dupe_of contains O` (product-level only — the ontology defines `dupe_of` on
products, directional dupe→original; brand-level imitation claims are never
inferred from product edges).

- Mention resolves to `O` → **direct original evidence**.
- Mention resolves to `P` with a citable `P.dupe_of → O` edge → **clone-tail
  demand-space evidence** — never presented as direct original endorsement.
- Low-confidence resolution → excluded from roll-up; displayed only as
  unresolved/withheld when the receipt itself is claimable.
- Edge without citable provenance → excluded; the edge is withheld.
- Multiple `D(O)` products in one video → product rows stay separate; the
  video's views count ONCE toward demand-space reach.
- Display: adjacent **Direct Original** and **Clone Tail** blocks, each with
  videos, deduped mentions, unique-video attention, product-level attention,
  stance mix, top receipts, provenance state.
- Empty graph → the honest-absence text: *"Dupe-space roll-up withheld: the
  ontology contains no citable dupe relationships for this capture/version.
  Direct original mentions are shown where available. This is not evidence of
  zero clone demand."*

## 4. Gameability countermeasures (display behaviors, not new infrastructure)

| Failure mode | Countermeasure |
| --- | --- |
| Stale capture | Capture dates + freshness state displayed; single-window trend reads downgrade. |
| ASR/resolution noise in the clone tail | Per-product resolution confidence displayed; low-confidence mentions never roll up; unresolved candidate count shown as withheld. |
| One viral video dominating attention | Attention concentration displayed: top-video share + supporting-video count + editorial presence beside attention. |
| Coverage read as endorsement | Stance mix always separate; negative/unclear mentions count as coverage only. |
| Missing read as zero | Explicit withhold states with named missingness, everywhere. |

## 5. The other four panels (design targets, one enrichment each)

- **Ad-reception:** matched sponsored-vs-organic comparison grid by disclosure
  class (`paid` / `gifted-PR-candidate` / `affiliate-or-self-brand` /
  `organic`), each vs matched organic pairs and the creator's own baseline; no
  third-party sponsored items → downgrade/withhold. Known risk: hidden gifting
  understates commercial load — displayed as a named limitation.
- **Purchase-intent:** intent by product/demand-space, aggregate-only (never
  person-level), separating bought-because-of-you / where-to-buy / dupe-request
  / price-objection / comparison-shopping language, with the page-1 visible
  comment limitation displayed. Intent resolves to a product only when comment
  context supports it; otherwise it stays aggregate texture. (The intent
  categories are extractor labels for the depth-layer build — NOT new ontology
  vocabulary.)
- **Brand adjacency:** organic adjacency matrix — buyer-like brands/products
  already discussed unpaid, with tier/note-family similarity, attention, and
  stance. Never a contact list or generic brand leaderboard.
- **Momentum:** baseline-relative only (moving averages, follower deltas per
  cycle, breakout frequency vs the creator's own baseline, fit-relevant-video
  participation) — never raw popularity. Requires ≥2 capture cycles for `show`
  (see residual R3).

## 6. Reading order per buyer segment

Fit leads for every segment. Follow-on: dupe-first/clone house → adjacency →
purchase-intent → ad-reception → momentum; DTC founder → purchase-intent →
ad-reception → momentum → adjacency; niche/indie → adjacency → ad-reception →
purchase-intent → momentum; agency → ad-reception → adjacency →
purchase-intent → momentum.

## 7. Explicit non-goal (adjudicated as out of scope, kept visible)

The panels deliberately do NOT answer *"given my product economics,
creator rate, terms, timing, and legal tolerance, should I buy this placement
now?"* That final synthesis belongs to the readback conversation and the
buyer's own judgment; imitation-legality screening stays a per-engagement owner
call (charter §5); pricing/commercial framing is deferred (register row D-2).
Setting this expectation with the buyer up front is part of the sprint offer,
not a gap to quietly fill with a score.

## 8. Accepted residuals (Mini God Tier — the price, named)

| # | Left undone | Why acceptable now | Remaining risk | Upgrade trigger |
| --- | --- | --- | --- | --- |
| R1 | Dupe graph is empty; dupe-space roll-up ships as honest withhold | The honest-absence display is designed and doctrinally correct | Clone-house buyers see their core row withheld in early sprints | Capture-lane run (post capture↔lake sync) lands citable `dupe_of` edges from the source's similar-perfumes data |
| R2 | Stance extraction is operator-assisted, not a validated extractor | `product_learning` cap + per-row confidence display | Stance mix could misread sarcasm/context | Depth-layer build validates the extractor per its own handoff |
| R3 | Momentum has one capture window today | Time-axis accrues passively; panel opens as downgrade/withhold honestly | Momentum panel thin in first sprints | ≥2 capture cycles per roster creator via the registry/silver lanes (owner-deferred timeline) |
| R4 | Clone/niche-tail mentions (~13%, low-confidence ASR) excluded from roll-ups | Prevents provenance laundering; bias is downward (honest direction) | Undercounts clone-tail attention for exactly the widened-lane buyers | Tail re-verification against the bound fragrance reference |
| R5 | Pre-launch DTC fit depends on buyer-supplied coordinates | Withhold-not-guess is the doctrine | Thin report if the buyer can't articulate coordinates | Coordinate-intake step at sprint prep (owned by sprint ops, not this record) |
| R6 | Comparable-brand baseline needs history in the captured corpus | Withheld honestly when absent | Row frequently withheld at current roster depth | Roster depth capture at scale |
| R7 | The §7 "buy now?" synthesis is out of scope | Readback + owner per-engagement calls own it; D-2 deferred | Buyer expectation mismatch if unstated | D-2 commercial-frame decision |

## Non-claims

Design record only — not validation, not readiness, not buyer proof, not build
authorization; `product_learning`-capped. The Mini God Tier label is a
capability-target calibration, not a measured claim.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The five sprint evidence panels gain an adjudicated display design: fit as
    a per-row show/downgrade/withhold matrix (no composite), the dupe-space
    roll-up rule, buyer-segment lead variants, gameability countermeasures as
    display behaviors, one design target per remaining panel, an explicit
    out-of-scope synthesis question, and a Mini God Tier accepted-residuals
    list. Elaborates charter §4; amends no charter decision.
  trigger: product_doctrine
  related_triggers: []
  controlling_sources_updated:
    - forseti/product/spines/creator_signal/aphrodite_vetting_sprint_panel_design_v0.md
    - forseti/product/spines/creator_signal/README.md   # index row
  downstream_surfaces_checked:
    - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md   # §4 defines the panels; this record elaborates display, consistent, not amended
    - forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md   # consumed as the per-row discipline; not amended
    - forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml   # consumed (dupe_of semantics, tier vocabulary); no schema or vocabulary change
    - docs/prompts/handoffs/aphrodite_depth_layer_build_handoff_v0.md   # gains a display target; the handoff itself is not edited — its receiver loads this record via the spine README
  intentionally_not_updated:
    - path: forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
      reason: >
        Charter §4 stays the strategy-level panel definition; duplicating
        display rules there would fork the owner. This record is the routed
        elaboration.
  stale_language_search: >
    rg -in "fit score|composite score|single score|fit panel" forseti/product/spines/creator_signal docs/research
  stale_language_search_result: >
    Executed 2026-07-05. No live surface proposes a composite fit score (the
    charter's forbidden set already bans a single vanity score); the rehearsal
    fit-panel record remains a dated research record consistent with this
    design. No conflicts.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not build authorization
```
