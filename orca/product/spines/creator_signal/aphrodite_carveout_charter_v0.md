# Aphrodite Carveout Charter v0

```yaml
retrieval_header_version: 1
artifact_role: Product charter (carveout identity stitch + strategy register — DRAFT pending delegated review and owner ratification)
scope: >
  The carveout charter for Aphrodite, the productized Creator Signal spine:
  binds the brand-to-spine identity stitch, the phase strategy, the two-layer
  moat doctrine (depth-now / time-later), the first sellable unit (paid
  design-partner Vetting Sprint), the five sprint evidence panels, buyer-lane
  defaults, the stratified capture policy (hypothesis-tier), the pre-build
  gates, and the DECIDE/DEFAULT/DEFER decision register with accepted
  residuals. Routes to the ratified records; restates none of them.
use_when:
  - Entering Aphrodite / Creator Signal carveout work and needing the current strategy state.
  - Checking whether an Aphrodite question is decided, defaulted, or deferred — and what trigger reopens it.
  - Scoping capture, product-surface, or proof work against the carveout strategy.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_company_brand_architecture_v0.md
  - orca/product/spines/creator_signal/creator_signal_product_architecture_v0.md
  - docs/decisions/orca_creator_signal_spine_promotion_binding_v0.md
  - orca/product/spines/creator_signal/creator_signal_market_sizing_v0.md
  - .agents/workflow-overlay/product-proof.md
  - orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
stale_if:
  - The owner ratifies, amends, or rejects this charter (replace the DRAFT status).
  - A controlling record this charter routes to is superseded.
  - The Aphrodite working name changes (D7 posture keeps a pre-launch rename cheap by design).
```

## Status

`DRAFT — PENDING DELEGATED ADVERSARIAL REVIEW AND OWNER RATIFICATION.`

The individual decisions recorded below as `DECIDE (ratified)` were
owner-ratified in-thread on 2026-07-04 (owner words cited per item). This
charter is the durable record of those decisions and of the strategy synthesis
around them; the charter *as an artifact* is not yet reviewed or ratified, and
it asserts no validation, willingness-to-pay evidence, buyer proof, readiness,
or build authorization.

Provenance of the synthesis: a cross-vendor (ChatGPT Pro) strategy commission
over a 13-source pack, adjudicated by the home model under the Mini God Tier
lens (`docs/decisions/orca_mini_god_tier_doctrine_v0.md`) and Smallest Complete
Intervention, with owner ratification question-by-question in the same thread
(2026-07-04). Advisory input throughout; the owner ratifications are the only
decision authority claimed.

## 1. Identity stitch

**Aphrodite is the productized Creator Signal carveout.** One product, two
names by design:

- **Aphrodite** — the adopted working sub-brand name (brand ADR D7, amended):
  the buyer-facing identity, "Aphrodite by Forseti", living at
  `aphrodite.forsetihq.com` until the public-launch gate (D8).
- **`creator_signal`** — the internal, brand-independent spine name and repo
  home (`orca/product/spines/creator_signal/`, bound by
  `docs/decisions/orca_creator_signal_spine_promotion_binding_v0.md`).

Naming boundary: the repo tree stays codename-internal (the same rule that
keeps "Orca" over "Forseti", brand ADR D1). Aphrodite appears in filenames and
buyer-facing content, never as repo structure — because D7 deliberately keeps a
pre-launch rename cheap, and structure named after a rename-cheap brand would
invert that posture.

What is inside the carveout: the Creator Signal product surface, the Vetting
Sprint offer, the sprint evidence panels, and the buyer-facing claim language.
What stays outside (Capture/Orca-internal): the creator registry data
contracts, capture runners, the lake, identity linkage, metric computation —
per the spine binding's `owns / does_not_own` split, which this charter does
not move.

## 2. Strategy

**One sentence: quietly build an evidence asset that becomes hard to copy on a
useful timeline, prove one buyer will pay for a decision made from it,
productize only what repeats — and keep the whole customer line a trigger-gated
option whose downside is capped because the data asset compounds regardless.**

| Phase | What happens | Gate to enter | Customer-facing? |
| --- | --- | --- | --- |
| **0 — Foundation (now)** | Feed the evidence asset (registry growth, depth capture, ontology); strategy on paper; stay dark | — (current state) | No. Only the ratified holding page + waitlist (with role/decision-type fields per the D8 amendment, 2026-07-04) |
| **1 — Prove payment** | One paid design-partner **Vetting Sprint** per buyer; readback; WTP evidence is the primary output | Foundation exit gate (deferred decision — register row D-1) fires Vetting v0; buyer probes separately owner-gated | Gated, design-partner only |
| **2 — Productize repeats** | Pricing/packaging/SaaS decisions; external claim schema lock | Full house graduation grammar adapted at sprint time; minimum repeat/pull anchor = ≥2 independent qualified buyers at Grade A/B + ≥1 paid-sprint-level pull | Gated |
| **3 — Public launch** | Own domain, handles, formal trademark clearance, marketing posture | Owner decision; bundle per brand ADR D8 | Yes |

Sequencing authority is unchanged: foundation-first per the product
architecture's Direction Update v0.1. Nothing in this charter pulls the
customer product forward.

## 3. Moat doctrine (two-layer)

The ratified moat object is the evidence graph
`creator × brand × product × content × time × proof` (product architecture).
This charter binds the *cashing order* of its axes:

**Layer 1 — depth-now.** Niche-complete roster + fragrance ontology (houses,
products, notes, accords, dupe-relationships, scene vocabulary) + an
entity-resolved, receipt-stamped content layer over transcripts and comments.
Structural flank: depth-per-creator is cheap at niche scale (~500–2,000
creators that matter in fragrance) and economically irrational at horizontal
scale — the incumbents index breadth shallowly and cannot justify per-vertical
depth. Raw transcripts/comments are commodity; the moat is roster judgment +
ontology + stamped derivation.

**Layer 2 — time-later.** The longitudinal graph accrues passively under
Layer 1 (the capture clock is already running). Its first product is
**momentum** (weeks-scale: moving averages, follower deltas, breakout frequency
vs the creator's own baseline — derivable from grid capture already flowing);
rising-star and history products mature later.

**Moat protectors** (all pre-existing doctrine, inherited verbatim): the
forbidden set (no outreach, contact enrichment, lead-list export, public
person-level directory, demographics without gates, single vanity score,
unstamped/LLM-only claims, zero-filled metrics) and honesty-as-product
(explicit missingness, per-number provenance).

**Honest boundary:** a funded competitor who chose to could replicate the
corpus in months — LLMs commoditize extraction for everyone. The claim is a
*defensible head start in a niche the incumbents are structurally blind to*,
hardening into a real barrier as the time axis accrues. Layer 1 is the bridge
that makes Layer 2's years survivable.

## 4. First sellable unit — the Vetting Sprint

`DECIDE (ratified 2026-07-04)`: the first sellable unit is a **paid,
fixed-scope design-partner Vetting Sprint** — a report for one live
creator-spend decision, plus a gated evidence view and a readback with the
decision owner. Not SaaS, not library access, not software. Its primary output
is willingness-to-pay evidence; revenue is secondary. Sellable only after the
foundation exit gate fires (register row D-1) and the owner separately opens
buyer probes.

The sprint report is built from five evidence panels — panels, never scores;
every shown fact is a claim object with provenance, freshness, sample support,
and named missingness:

1. **Fit evidence** (`ratified: "all these sub points are spectacular. we need
   this for sure"`) — segment share of recent content; price-tier and
   note-family distribution of products mentioned; audience taste from comment
   language (collector vs dupe-seeker); proven adjacency (how the creator's
   videos on comparable brands performed against their own baseline);
   niche-share trajectory.
2. **Sponsorship load + ad reception** (`ratified, same turn`) — detection
   from metadata/description/disclosure markers on all captured videos
   (organic / gifted-PR / affiliate / paid, each with confidence + receipt
   quote); load = density, gifted/paid mix, sponsor concentration, disclosure
   hygiene; reception = within-creator sponsored-vs-organic comparison on
   views/likes/comment texture. Named limitations travel with the panel
   (small per-creator n, gifted ambiguity, invisible comment moderation).
3. **Audience purchase-intent evidence** — aggregate intent language from
   visible comments ("bought it because of you", "where do I get this", dupe
   requests); always aggregate, never per-commenter (person-level boundary).
4. **Organic brand adjacency** — which candidate creators already discuss
   brands like the buyer's, unpaid; bounded inside the paid report; never
   exportable, never a contact list.
5. **Momentum** (`owner-added 2026-07-04`) — engagement/view moving averages,
   follower-count deltas per capture cycle, breakout frequency, all relative
   to the creator's own baseline, shown with windows and receipts.

Candidate-set shape, `DECIDE (ratified — hybrid)`: Aphrodite builds and
rehearses the capability to assemble a bounded candidate set from the registry
("we must have enough information to bring to them"); the bring-vs-assemble
mix for a real engagement is decided at the first sprint. Assembled sets carry
no contact info and never leave the report.

## 5. Buyer lanes and proof gates

`DEFAULT` (working assumption per the product architecture, sharpened here):

- **Lead lane: indie/DTC fragrance brands** — they own the exact decision the
  sprint serves.
- **Agencies: conditional** — admitted only when the accountable client
  decision owner joins the readback (house rule inherited from the parent
  proof doctrine; agency interest alone is not proof).
- **Non-marketer evidence buyers (investor/retail/procurement): deferred** —
  trigger: inbound evidence-buyer pull, or the first bounded brand/agency
  batch produces zero paid path.

Proof semantics are consumed, not redefined, from
`.agents/workflow-overlay/product-proof.md` and the graduation/kill grammar of
`orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md`
(adapted to this product at sprint time — the parent's demand-substrate gate
does not transfer; the pull/praise, trust-objection/refusal, kill-discipline,
and graduation grammar do): pull is paid-path behavior, never praise. The
≥2 independent qualified decision owners at Grade A/B plus ≥1
paid-sprint-level pull threshold is the minimum repeat/pull anchor, not the
full graduation gate; at sprint adaptation the packet's repeatability,
no-dashboard/no-source-system, no-bespoke-value, and non-claim criteria still
have to hold. Park on majority forbidden-feature pull, repeated trust refusal,
or a dry bounded batch. Every claim in this charter's scope is capped at
`product_learning` tier until receipts exist.

## 6. Capture policy (hypothesis-tier; numbers are capture-lane calibration, not commitments)

`DECIDE (ratified via the consolidated plan, 2026-07-04)` — the shape;
`hypothesis` — every number.

- **Cheap layer, all videos** (existing grid capture): metadata, titles,
  descriptions, view/like/comment counts, disclosure markers. Sponsorship
  *detection*, much of brand-mention recall, and all momentum inputs live
  here at near-zero marginal cost.
- **Deep layer (transcript + page-1 visible comments), stratified — not
  top-sliced:** (a) recent window, last ~10–15 videos per roster creator
  regardless of performance (representativeness anchor); (b) top-K all-time
  by views (audience-defining content); (c) breakout triggers — daily grid
  analysis flags a video outperforming the creator's own baseline → probe
  (the trigger doubles as the momentum detector); (d) pull-on-decision —
  sponsored videos + matched organic pairs for any creator entering a sprint.
- **Rejected: top-25%-only / performance-triggered-only capture.**
  Performance selection biases exactly the fit panel (hits misrepresent
  segment share) and the ad-reception panel (sponsored videos underperform on
  average and would be systematically excluded). Stratified ≈ 90–95% of
  decision value at roughly 20–30% of full-corpus capture cost; full
  transcripts are not required — the only full-recall consumer (niche demand
  analytics) is view-weighted, and sprint-specific needs are pulled on
  demand.
- **Comments:** page-1 visible only (engagement-ranked; carries the reception
  and intent signal). Superfan/early-commenter skew, comment drift after
  capture, and moderation invisibility are named limitations, not silently
  absorbed.

## 7. Pre-build gates

1. **Extraction provenance** — before any derived (LLM-extracted) label ships
   to any surface, the claim-object discipline extends to derivation: every
   derived claim carries extraction model, version, prompt/recipe version, and
   source hash, with the receipt quote/timestamp. Without this, derived labels
   are the unstamped claims the doctrine forbids. Contract design is a later
   bounded work unit; this charter only gates on its existence.
2. **ToS-risk sanity check** — a capture-lane pass confirming comment and
   transcript capture at niche scale stays inside the owner's measured-risk
   posture, before the deep layer is committed at roster scale.
3. **Foundation exit gate** — deferred decision (register row D-1); it gates
   the Vetting v0 build, not foundation work itself.

## 8. Decision register

| # | Item | Tag | Basis / trigger |
| --- | --- | --- | --- |
| R-1 | First sellable unit = paid design-partner Vetting Sprint | `DECIDE (ratified 2026-07-04)` | Owner selection: "Ratify the Vetting Sprint" |
| R-2 | Waitlist collects two optional fields (role, decision type) | `DECIDE (ratified 2026-07-04)` | Owner selection: "Add the two fields"; applied as the D8 amendment (2026-07-04) in the brand ADR |
| R-3 | Candidate-set hybrid: assembly capability built + rehearsed; mix decided at first sprint | `DECIDE (ratified 2026-07-04)` | Owner: "deciding at first sprint, but we must have enough information to bring to them so hybrid" |
| R-4 | Sprint panels: fit, sponsorship/ad-reception, purchase-intent, brand adjacency, momentum | `DECIDE (ratified 2026-07-04)` | Owner: "we need this for sure"; momentum owner-added same day |
| R-5 | Two-layer moat doctrine + stratified capture shape | `DECIDE (ratified 2026-07-04)` | Owner "proceed" on the consolidated findings; capture numbers stay hypothesis-tier |
| D-1 | Foundation exit gate definition (practice-run report vs numeric thresholds vs both) | `DEFER (owner-parked)` | Recorded recommendation: practice-run gate + numbers as non-binding capture targets. Trigger: foundation nears completion |
| D-2 | Commercial frame (pricing bands, tiers, terms) | `DEFER` | Per-decision pricing *posture* is `DEFAULT`; the frame decision is a separate owner-gated pass. Trigger: first real paid conversation or repeat pull |
| D-3 | External customer claim-object schema lock | `DEFER` | Ratified in Direction Update v0.1. Trigger: repeated paid use reveals stable claim fields |
| D-4 | SaaS / gated library packaging | `DEFER` | Trigger: repeated paid buyers ask to reuse the evidence surface |
| D-5 | Non-marketer evidence-buyer lane | `DEFER` | Trigger: inbound evidence-buyer pull, or dry first bounded batch |
| D-6 | Public launch bundle (domain, handles, trademark), entity split | `DEFER` | Owned by the brand ADR (D3, D7-amendment, D8); not re-decided here |
| F-1 | Buyer lanes: brands lead; agencies conditional on client decision owner in readback | `DEFAULT` | Inherited parent rule; reopened only by D-5's trigger |
| F-2 | Repo home = `creator_signal` spine; Aphrodite in filenames, never tree | `DEFAULT` | Section 1 naming boundary |
| F-3 | Proof grammar = house grammar; `product_learning` cap | `DEFAULT` | Section 5 |

## 9. Accepted residuals (Mini God Tier discipline)

Named, bounded, consciously accepted; each with remaining risk and an upgrade
trigger. Without this table the MGT label would be hype.

| Residual | Why acceptable now | Remaining risk | Upgrade trigger |
| --- | --- | --- | --- |
| Single lead buyer lane (brands) instead of a parallel 3-lane probe | Cheapest discriminating path; probes are owner-gated anyway | Lead lane could be wrong | First bounded batch runs dry → open next lane (D-5) |
| No numeric foundation gate pre-committed | Numbers would be unvalidated guesses; the practice-run rehearsal is the real test either way | Capture lane lacks a hard numeric finish line | First rehearsal failure mints evidence-based numbers (D-1) |
| Stratified (not full) transcript corpus | Hypothesis-tier estimate: ~90–95% of decision value at ~20–30% of capture cost; analytics are view-weighted | Organic mentions in unsampled median videos missed | Metadata scan on all videos mitigates; sprint-specific needs pulled on demand |
| Page-1 comments only | Engagement-ranked page carries the decision signal | Superfan skew; drift; moderation invisible | Named-limitation display; re-probe on trigger |
| No pricing menu / tiers | One unit must sell before a ladder exists | Cannot quote beyond the sprint | First paid conversation → commercial-frame pass (D-2) |
| No freshness SLA | Single-operator manual posture is the verified state | Staleness at readback | Refresh-before-readback rule now; SLA only when a customer requires one |
| Working brand name without formal clearance | D7 amendment posture: light check before spend, formal clearance at first public commercial use, rename cheap pre-launch | Late collision forces rename | Public-launch gate bundles clearance (D-6) |

## 10. Non-claims

- Not validation, willingness-to-pay evidence, buyer proof, judgment quality,
  or readiness of any kind; every claim here is `product_learning`-capped.
- Authorizes no implementation, capture expansion, ontology build, outreach,
  publishing, buyer contact, website build, or purchase — every gated lane
  keeps its own authorization boundary.
- Moves no Capture/Creator Signal ownership boundary and mints no
  evidence-ladder vocabulary.
- The charter itself is DRAFT: not reviewed, not ratified; the in-thread
  ratifications it records (register rows R-1…R-5) stand on the owner's words,
  not on this artifact's status.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Adds the Aphrodite carveout charter as the strategy register above the
    product architecture: the brand-to-spine identity stitch and naming
    boundary; the phase strategy with gates; the two-layer moat doctrine
    (depth-now content/ontology layer, time-later longitudinal layer) as the
    cashing order of the ratified evidence-graph moat; the ratified first
    sellable unit (paid design-partner Vetting Sprint) with five evidence
    panels; buyer-lane defaults; the stratified capture policy shape
    (hypothesis-tier numbers); extraction-provenance and ToS-check pre-build
    gates; and the DECIDE/DEFAULT/DEFER register with MGT accepted residuals.
    Sequencing (foundation-first) and all ownership boundaries unchanged.
  trigger: product_doctrine
  related_triggers: []
  controlling_sources_updated:
    - orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
    - docs/decisions/forseti_company_brand_architecture_v0.md   # D8 amendment (waitlist role fields), same lane
    - orca/product/spines/creator_signal/README.md               # index row for this charter
  downstream_surfaces_checked:
    - orca/product/spines/creator_signal/creator_signal_product_architecture_v0.md  # foundation-first sequencing and Vetting v0 shape consistent; this charter sits above it and pulls nothing forward
    - docs/decisions/orca_creator_signal_spine_promotion_binding_v0.md              # owns/does_not_own split untouched; charter routes to it
    - .agents/workflow-overlay/product-proof.md                                     # proof semantics consumed, not redefined
    - orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md    # grammar reused; parent demand-substrate gate explicitly not transferred
    - docs/workflows/orca_repo_map_v0.md                                            # decision/product records not exhaustively indexed (existing precedent); the spine README row carries the route
    - AGENTS.md                                                                     # no naming/brand/product content; routes to overlay — unchanged
  intentionally_not_updated:
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Existing precedent (spine binding DCP): per-spine artifacts route via
        the spine front door, which this lane updates; no repo-map row added.
    - path: orca/product/spines/creator_signal/creator_signal_product_architecture_v0.md
      reason: >
        Its Direction Update v0.1 remains the sequencing authority; this
        charter routes to it rather than editing it. Its older Vetting v0
        detail sections already carry the v0.1 supersession note.
  stale_language_search: >
    rg -in "aphrodite" --glob "!docs/_inbox/**" --glob "!orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md" .
  stale_language_search_result: >
    Executed 2026-07-04 in the lane worktree with all three edits staged, before
    commit. Hits in exactly four files, all expected: the brand ADR (the naming
    authority plus this lane's D8 amendment), the web-foundation design-lane
    handoff (a committed point-in-time packet whose stale_if routes receivers to
    the ADR), one captured-evidence datapoint (the "Soki London Aphrodite"
    fragrance product title in docs/review-inputs/youtube_shorts_fragrance_
    tone_expansion200_capture_v0.json — evidence data, not routing), and the
    spine README (this lane's new index row). No repo surface carries stale or
    conflicting Aphrodite routing.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not willingness-to-pay evidence
    - not implementation, capture, outreach, or publishing authorization
    - charter is DRAFT pending delegated review and owner ratification
```
