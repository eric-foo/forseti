# Aphrodite Carveout Charter v0

```yaml
retrieval_header_version: 1
artifact_role: Product charter (carveout identity stitch + strategy register — owner-ratified direction)
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
  - forseti/product/spines/creator_signal/creator_signal_product_architecture_v0.md
  - docs/decisions/forseti_creator_signal_spine_promotion_binding_v0.md
  - forseti/product/spines/creator_signal/creator_signal_market_sizing_v0.md
  - .agents/workflow-overlay/product-proof.md
  - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md
stale_if:
  - The owner amends or supersedes this charter (dated amendments only; no silent rewrites).
  - A controlling record this charter routes to is superseded.
  - The Aphrodite working name changes (D7 posture keeps a pre-launch rename cheap by design).
```

## Status

`OWNER_RATIFIED_DIRECTION` — ratified by the owner in-thread on 2026-07-04
(owner word: "ratified."), after the delegated cross-vendor adversarial
review-and-patch return (`reviewed_by: gpt-5-codex`; report at
`docs/review-outputs/adversarial-artifact-reviews/aphrodite_carveout_charter_v0_delegated_adversarial_artifact_review_v0.md`)
was adjudicated by the commissioning CA with all four findings accepted and
their patches kept (commit `3e56eb25`). This locks a direction, not a result:
it asserts no validation, willingness-to-pay evidence, buyer proof, or
readiness, and it authorizes no build, capture expansion, outreach, or
publishing.

The individual decisions recorded below as `DECIDE (ratified)` were
owner-ratified in-thread on 2026-07-04 (owner words cited per item); this
charter is the durable record of those decisions and of the strategy synthesis
around them.

Provenance of the synthesis: a cross-vendor (ChatGPT Pro) strategy commission
over a 13-source pack, adjudicated by the home model under the Mini God Tier
lens (`docs/decisions/forseti_mini_god_tier_doctrine_v0.md`) and Smallest Complete
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
  home (`forseti/product/spines/creator_signal/`, bound by
  `docs/decisions/forseti_creator_signal_spine_promotion_binding_v0.md`).

Naming boundary: Forseti is the canonical project name at the authority layer
(rename policy, PR #646), while `orca/` roots and lowercase `orca_*`
identifiers are preserved compatibility paths — path renames are high-lock-in
migrations, never text cleanups
(`docs/decisions/forseti_compatibility_migration_boundary_v0.md`). Aphrodite
follows the same discipline with one extra reason: it appears in filenames and
buyer-facing content, never as repo structure, because D7 deliberately keeps a
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
| **1 — Prove payment** | One paid design-partner **Vetting Sprint** per buyer; readback; WTP evidence is the primary output | Foundation exit gate (register row D-1, ratified 2026-07-05) fires Vetting v0; buyer probes separately owner-gated | Gated, design-partner only |
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

**Honest boundary (moat strength — amended 2026-07-05):** LLMs commoditize
*extraction* for everyone, so extraction-only depth is not the moat and a funded
competitor who *chose* to could replicate the corpus in months — that residual is
kept, not waved away. But replication is strategically unattractive and off-core
for the incumbents (horizontal-breadth players will not *sustain* per-vertical
depth — it is a distraction from their core), and a fresh entrant takes the same
capture/ToS risk *before* proving the business, so risk-adjusted it is a worse bet
for them than for us. Both layers compound against a late entrant: the *depth*
layer via roster judgment + ontology + stamped derivation + scene relationships
(not the commodity extraction), and the *time* layer via a longitudinal series
that cannot be backfilled. The durable claim stands: a defensible head start in a
niche the incumbents are structurally blind to, hardening into a real barrier as
the time axis accrues. Layer 1 is the bridge that makes Layer 2's years
survivable.

**Moat object, sharpened (2026-07-08, owner-approved in-thread):** The
load-bearing distinction is *extraction vs domination*. Extraction — pulling and
labeling transcripts / comments / metadata — is a commodity *flow*: any
competitor with the same LLM can run it, so it earns no rent (this is the
residual kept above). What is *not* a commodity is **domination of the niche** —
a *position*, not a dataset: niche-*complete* coverage (every creator that
matters, not a curated sample), a longitudinal series that cannot be backfilled,
the roster judgment + ontology + scene relationships, and — as the position
matures — the creator relationships, buyer trust, and being *the* source in the
niche. A funded competitor with the same extraction can copy the *flow* but
cannot instantly *occupy the position*. So the premium Aphrodite commands is a
**position rent, not a data-quality rent** — the asset is "we own the niche," and
data is a commodity input to it. This is also why *small* is the strategy, not a
limitation: domination is achievable only in a niche small enough to fully
capture, and defensible only in one too small for a horizontal incumbent to
contest. Framing sharpened; the extraction residual above is unchanged and still
kept.

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
  - *Lead-lane sharpening (owner-directed 2026-07-05, non-negotiable inclusion):*
    the lead lane **explicitly includes dupe-first / clone houses,
    creator-owned DTC, and pre-designer specialty/indie houses** — the
    graduation cohort (dupe-first → originals → mainstream retail; the
    Lattafa / Armaf / Dossier-into-Sephora arc). Rationale: this cohort's
    recurring decision — *which proven original to chase next, and whether that
    niche is already saturated* — is the exact decision the sprint and the fit
    read serve; the dupe-relationship graph plus attention-weighted SoV is
    buyer-core for them, not enrichment. The ontology tier vocabulary
    (`clone-house`, `creator-owned-dtc` in
    `forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml`)
    already carries the classification. Brand-safety / imitation-legality
    screening stays a per-engagement owner call, never a lane exclusion.
- **Agencies: conditional** — admitted only when the accountable client
  decision owner joins the readback (house rule inherited from the parent
  proof doctrine; agency interest alone is not proof).
- **Non-marketer evidence buyers (investor/retail/procurement): deferred** —
  trigger: inbound evidence-buyer pull, or the first bounded brand/agency
  batch produces zero paid path.

Proof semantics are consumed, not redefined, from
`.agents/workflow-overlay/product-proof.md` and the graduation/kill grammar of
`forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md`
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
3. **Foundation exit gate** — ratified 2026-07-05 (register row D-1); it gates
   the Vetting v0 build, not foundation work itself. Definition: the
   foundation phase exits when one full dress rehearsal — display target
   `aphrodite_vetting_sprint_panel_design_v0.md` — produces all six:
   1. All five panels rendered via the operator-runner transport (no API
      key) against a real captured creator.
   2. Fit panel fully DERIVED: every fit element resolves against
      `fragrance_reference_v0.yaml` coordinates; no operator-asserted fit
      facts.
   3. Provenance behavior demonstrated end-to-end, including at least one
      honest withhold actually displayed (missing ≠ zero in practice, not
      just on paper).
   4. Candidate-set assembly rehearsed (register row R-3): the buyer-side
      product-coordinate intake actually exercised, not stubbed.
   5. Cross-vendor adversarial review of the rehearsal output returns
      blocker/major-free, per the delegated-review lane.
   6. Bounded-effort receipt: the rehearsal records what it cost
      (reads/steps/time), proving repeatability rather than a heroic
      one-off.

   **Accelerator:** a waitlist-inbound buyer signal may pull the gate
   forward — the rehearsal becomes the first design-partner Sprint prep
   instead of a synthetic cycle. **FLAG-1 rider:** the commercial-use/
   data-rights flag carries into Phase 1 unresolved and must appear in the
   first Sprint's scope conversation; the gate does not silently discharge
   it. **Excluded:** numeric roster thresholds (owner roster-decoupling
   decision); numbers remain non-binding capture targets.

**Gate status (2026-07-05):** gate 1 is discharged (existence) by
`aphrodite_derived_claim_provenance_contract_v0.md`; gate 2 is discharged by
`aphrodite_depth_capture_tos_risk_sanity_check_v0.md` (PASS for
foundation-stage capture, with the commercial-use/data-rights flag carried to
Phase 1). Gate 3 is defined (ratified 2026-07-05, D-1) and has not yet
fired — the rehearsal has not run. The depth-layer build itself is
packaged in `docs/prompts/handoffs/aphrodite_depth_layer_build_handoff_v0.md`
and stays gated on explicit owner build-authorization.

## 8. Decision register

| # | Item | Tag | Basis / trigger |
| --- | --- | --- | --- |
| R-1 | First sellable unit = paid design-partner Vetting Sprint | `DECIDE (ratified 2026-07-04)` | Owner selection: "Ratify the Vetting Sprint" |
| R-2 | Waitlist collects two optional fields (role, decision type) | `DECIDE (ratified 2026-07-04)` | Owner selection: "Add the two fields"; applied as the D8 amendment (2026-07-04) in the brand ADR |
| R-3 | Candidate-set hybrid: assembly capability built + rehearsed; mix decided at first sprint | `DECIDE (ratified 2026-07-04)` | Owner: "deciding at first sprint, but we must have enough information to bring to them so hybrid" |
| R-4 | Sprint panels: fit, sponsorship/ad-reception, purchase-intent, brand adjacency, momentum | `DECIDE (ratified 2026-07-04)` | Owner: "we need this for sure"; momentum owner-added same day |
| R-5 | Two-layer moat doctrine + stratified capture shape | `DECIDE (ratified 2026-07-04)` | Owner "proceed" on the consolidated findings; capture numbers stay hypothesis-tier |
| D-1 | Foundation exit gate = six-criteria practice-run dress rehearsal + waitlist accelerator + FLAG-1 rider; numeric thresholds excluded | `DECIDE (ratified 2026-07-05)` | Owner selection: "Ratify as proposed" on the six-criteria proposal; definition in §7 gate 3. Numbers stay non-binding capture targets (roster-decoupling) |
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
- Ratification locks a direction only; the in-thread ratifications recorded in
  register rows R-1…R-5 stand on the owner's words. Every gated lane keeps its
  own authorization boundary.

## Direction Change Propagation

Older receipts for this file are archived verbatim in
`docs/decisions/dcp_receipts_archive_v0.md` (charter-creation receipt,
2026-07-04, moved 2026-07-05 under the two-inline-receipt rule).

```yaml
direction_change_propagation:
  doctrine_changed: >
    Durable propagation of the owner-directed lead-lane sharpening landed in
    §5 by commit d1bbfb2f (PR #710, merged): the Aphrodite lead buyer lane
    (indie/DTC fragrance brands) explicitly includes the dupe-first/clone-house,
    creator-owned-DTC, and pre-designer specialty/indie cohort (the
    Lattafa/Armaf/Dossier graduation arc) as buyer-core, not an enrichment
    add-on; brand-safety/imitation-legality screening stays per-engagement,
    never a lane exclusion. That commit's message-body receipt was compact and
    did not carry the full downstream sweep this record completes. This receipt
    adds no new doctrine — it is the propagation completion for the
    already-landed §5 text quoted above.
  trigger: product_doctrine
  related_triggers: []
  controlling_sources_updated:
    - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md   # §5 sharpening already landed by d1bbfb2f; this receipt completes propagation
    - forseti/product/spines/creator_signal/creator_signal_market_sizing_v0.md   # added a dated routing note (2026-07-05): buyer counts/SAM predate the cohort sharpening and are not re-derived here; resizing is its own later unit
  downstream_surfaces_checked:
    - forseti/product/spines/creator_signal/creator_signal_product_architecture_v0.md   # ICP framing ("niche/indie/challenger/DTC fragrance brands", lines 26/95-99) is the broader superset the charter narrows within; consistent, not contradicted — charter's own text says the DEFAULT is "sharpened here," so no edit
    - forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml   # clone-house / creator-owned-dtc tier vocabulary already exists (lines 96,116,120,129); consistent, confirms the sharpening has a classification substrate
    - forseti/product/spines/creator_signal/README.md   # index rows for the charter and the market-sizing doc still accurately describe each artifact's role after the sizing-note addition; no row text change needed
    - forseti/product/spines/product_lead/proof_charter/forseti_product_proof_lead_charter_v0.md   # describes the separate parent-level indie/DTC beauty/personal-care ICP wedge (a different product lane, not Aphrodite); charter §5 already states proof semantics are "consumed, not redefined" from this lane — consistent, out of scope
    - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md   # same parent buyer-proof grammar; charter explicitly reuses grammar without transferring the demand-substrate gate — consistent, out of scope per task bound (buyer-proof grammar owned elsewhere)
    - forseti/product/spines/product_lead/icp_wedge/*   # parent ICP-wedge decision chain (pricing-first / consumer-demand-first lineage) is a distinct, superseded-in-place lane unrelated to the Aphrodite carveout lead lane; no lane-naming or vocabulary collision found
    - docs/workflows/orca_repo_map_v0.md   # no Aphrodite/creator_signal lead-lane enumeration to update; existing precedent routes per-spine artifacts via the spine front door (per the charter's own prior receipt)
  intentionally_not_updated:
    - path: forseti/product/spines/creator_signal/creator_signal_product_architecture_v0.md
      reason: >
        The charter's §5 header already states the DEFAULT is "per the product
        architecture, sharpened here" — the architecture doc keeps the broader
        ICP statement (niche/indie/challenger/DTC) and the sharpening
        deliberately lives only in the charter, per the charter's own existing
        (pre-this-receipt) intentionally_not_updated note for this same file.
    - path: forseti/product/spines/creator_signal/README.md
      reason: >
        Both affected artifacts' index-row descriptions remain accurate after
        this lane's edits (the charter row already names it as the strategy
        register; the market-sizing row already flags it as a non-validating
        estimate) — no row text is stale.
    - path: forseti/product/spines/product_lead/*
      reason: >
        Owns a distinct, parent-level ICP/buyer-proof lane and grammar the
        charter explicitly borrows without redefining (§5); task scope
        excludes widening into product-proof semantics or buyer-proof grammar.
        Checked for lane-naming collision only — none found.
  stale_language_search: >
    rg -in "lead lane|buyer lane|\bICP\b|indie/DTC|indie-DTC|\bclone\b|\bdupe\b|dupe-cohort|dupe cohort" forseti/product/spines/creator_signal forseti/product/spines/product_lead docs/decisions docs/workflows
  stale_language_search_result: >
    Executed 2026-07-05 on branch claude/aphrodite-icp-dcp-propagation (base
    origin/main e1969efb). ~146 hits. Creator Signal spine hits are the
    already-landed §5 sharpening (charter), the broader ICP superset statement
    (product architecture, consistent per above), and the ontology tier
    vocabulary (consistent, pre-existing substrate). product_lead and
    docs/decisions hits are exclusively the separate parent ICP-wedge/buyer-proof
    lane (pricing-first / consumer-demand-first lineage, and the general
    US-market indie/DTC beauty/personal-care wedge) — a different product line
    from the Aphrodite carveout, already explicitly decoupled by charter §5's
    "consumed, not redefined" language; no conflicting or stale routing found
    requiring edits there. No hit found requiring a change beyond the
    market-sizing routing note added by this receipt.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not willingness-to-pay evidence
    - not implementation, capture, outreach, or publishing authorization
    - not a resizing of the market-sizing estimate (routing note only)
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Register row D-1 (foundation exit gate definition) flips DEFER
    (owner-parked) to DECIDE (ratified 2026-07-05): the foundation phase exits
    on a six-criteria practice-run dress rehearsal (five panels rendered via
    the operator-runner transport; fit panel fully DERIVED against
    fragrance_reference_v0.yaml; provenance behavior end-to-end including at
    least one honest withhold displayed; candidate-set assembly rehearsed per
    register row R-3; cross-vendor adversarial review blocker/major-free;
    bounded-effort receipt), plus a waitlist-inbound accelerator and the
    FLAG-1 commercial-use/data-rights rider carried into Phase 1. Numeric
    roster thresholds are excluded per the owner's roster-decoupling decision;
    numbers remain non-binding capture targets. The definition lives in §7
    gate 3; no other register row, phase boundary, or ownership boundary
    changes. Defining the gate does not fire it: the rehearsal has not run,
    and the depth-layer build keeps its own owner authorization.
  trigger: product_doctrine
  related_triggers: []
  controlling_sources_updated:
    - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md   # §2 phase-table gate cell, §7 gate 3 definition + gate status, §8 row D-1
  downstream_surfaces_checked:
    - forseti/product/spines/creator_signal/aphrodite_vetting_sprint_panel_design_v0.md   # (lands via PR #717, open at receipt time) names itself the display target for the D-1 dress rehearsal; its stale_if trigger "D-1 adopts different rehearsal criteria than this design assumes" does not fire — the ratified criteria adopt that design as the rehearsal target
    - docs/prompts/handoffs/aphrodite_depth_layer_build_handoff_v0.md   # marks D-1 "OPEN (parked)" at lines 90/128; committed point-in-time packet whose load contract requires re-verifying the charter register before execution; its own text already states D-1 does not block the rehearsal
    - forseti/product/spines/creator_signal/creator_signal_product_architecture_v0.md   # sequencing authority (foundation-first, Direction Update v0.1) untouched; the gate definition pulls no customer product forward
    - forseti/product/spines/creator_signal/README.md   # charter index row already names it the decision register; no row text stale
  intentionally_not_updated:
    - path: docs/prompts/handoffs/aphrodite_depth_layer_build_handoff_v0.md
      reason: >
        Committed point-in-time handoff packet; per existing DCP precedent
        (web-foundation handoff, charter-creation receipt) sealed packets are
        not edited — their confirm-don't-trust load contract routes receivers
        to re-read the charter register, which now carries the DECIDE row.
    - path: forseti/product/spines/creator_signal/aphrodite_vetting_sprint_panel_design_v0.md
      reason: >
        Not on main at receipt time (PR #717 open); its stale_if for D-1 does
        not fire because the ratified criteria match the design it assumes.
  stale_language_search: >
    rg -in "D-1|foundation exit gate" forseti/product/spines/creator_signal
    docs/prompts/handoffs docs/decisions docs/workflows
  stale_language_search_result: >
    Executed 2026-07-05 on branch claude/d1-gate-ratification (base
    origin/main e8ca2093) with all edits in the working tree, before commit.
    Hits: this charter (controlling source), the depth-layer build handoff
    (sealed point-in-time packet, handled above), and cleaning/judgment-spine
    files whose matches are the unrelated "OD-1" token and a different lane's
    "foundation" vocabulary — no Aphrodite surface carries stale
    deferred-gate routing.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof or willingness-to-pay evidence
    - not rehearsal completion — the gate is defined, not fired
    - not build authorization: depth-layer build and Vetting v0 keep their own owner gates
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    §3 "Honest boundary" strengthened (2026-07-05, owner-approved in-thread): the
    moat claim now names why replication is strategically unattractive and
    off-core for incumbents (unsustained per-vertical depth) and risk-asymmetric
    for a fresh entrant, and that both the depth layer (judgment / ontology /
    stamped derivation / scene relationships) and the time layer (un-backfillable
    longitudinal series) compound against a late entrant — while explicitly
    KEEPING the honest residual that LLM-commoditized extraction is replicable.
    Framing strengthened; no phase, gate, offer, or ownership boundary changes.
  trigger: product_doctrine
  related_triggers: []
  controlling_sources_updated:
    - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md   # §3 Honest boundary
  downstream_surfaces_checked:
    - forseti/product/spines/creator_signal/creator_signal_market_sizing_v0.md   # moat/premium reasoning consumed as-is; sizing not re-derived
    - docs/decisions/forseti_product_thesis_consumer_demand_v0.md                    # parent moat language (outcome memory) consistent; not amended
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - framing strengthened; not a new moat claim tier; extraction residual kept
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    §3 "Honest boundary" sharpened further (2026-07-08, owner-approved
    in-thread) with the extraction-vs-domination distinction: extraction is a
    commodity flow (earns no rent), whereas domination of the niche is a
    position (niche-complete coverage + un-backfillable longitudinal series +
    roster judgment / ontology / scene relationships + maturing creator
    relationships and buyer trust) that a same-LLM competitor cannot instantly
    occupy. The premium is named a POSITION rent, not a data-quality rent, and
    "small is the strategy" is stated as a consequence (domination is achievable
    only in a niche small enough to fully capture and defensible only in one too
    small for a horizontal incumbent to contest). Framing sharpened; the
    extraction residual is explicitly unchanged and still kept; no phase, gate,
    offer, ownership, or claim-tier boundary changes.
  trigger: product_doctrine
  related_triggers: []
  controlling_sources_updated:
    - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md   # §3 Honest boundary — "Moat object, sharpened" paragraph added
  downstream_surfaces_checked:
    - forseti/product/spines/creator_signal/creator_signal_market_sizing_v0.md   # "the hinge" (premium durability) reasoning consumed as-is; sizing not re-derived; consistent with position-rent framing
    - docs/decisions/forseti_product_thesis_consumer_demand_v0.md                    # parent moat language (outcome memory / de-correlated demand) consistent; not amended
    - forseti/product/spines/creator_signal/creator_signal_product_architecture_v0.md   # moat object (evidence graph) unchanged; this sharpens its defensibility framing, not the object
  stale_language_search: >
    rg -in "extraction|commodity|domination|position rent|\bmoat\b" forseti/product/spines/creator_signal docs/decisions/forseti_product_thesis_consumer_demand_v0.md
  stale_language_search_result: >
    Executed 2026-07-08 after the edits. Creator Signal spine hits: this charter
    (controlling source, edited); creator_signal_product_architecture_v0.md
    (defines the evidence-graph moat OBJECT — unchanged; this sharpens its
    defensibility framing, not the object); creator_signal_market_sizing_v0.md
    ("the hinge" premium-durability + the competitor teardown "they can copy
    screens faster than capture history" — already consistent with position-rent
    framing); and mechanics files (vetting panel design, derived-claim provenance
    contract, ToS-risk check, README) that carry no moat-framing claim. Parent
    thesis hits (forseti_product_thesis_consumer_demand_v0.md lines 169-188) are
    its OWN moat object — "outcome memory is the moat", "scraping commodity" — a
    distinct, consistent framing for the parent lane, not a conflict with
    Aphrodite's niche-domination position. No surface carries a moat framing this
    sharpening contradicts; no edit required beyond the charter.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - framing sharpened; not a new moat claim tier; extraction residual kept
```
