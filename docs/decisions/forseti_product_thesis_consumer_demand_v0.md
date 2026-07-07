# Forseti Product Thesis v1 — Evidence-Backed Consumer-Market Decision Intelligence

```yaml
retrieval_header_version: 1
artifact_role: Decision record (controlling product thesis — owner-ratified)
scope: >
  V1 product thesis re-centering Forseti on evidence-backed strategic
  decisions for consumer-market leaders, with consumer-demand integrity and
  durability as the first reads, beauty/personal-care as the first vertical
  (Vertical), and the existing outside-in engine and frozen Core Spine
  foundation as the substrate. Prepared 2026-06-11 after a cross-branch
  exploration sweep; ratified by the owner 2026-06-12 with later owner
  directions through 2026-06-20 folded into the active body (see Status).
  Supersedes
supersedes:
  - docs/decisions/turn_08_product_thesis_v0.md
use_when:
  - Owner sign-off on or review of the current product thesis.
  - Anchoring product, capture, judgment, or proof lanes to the product center.
  - Checking whether a proposed product claim, artifact, or lane fits the thesis.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/turn_08_product_thesis_v0.md
  - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md
  - orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md
stale_if:
  - The owner changes this active body again or a successor thesis supersedes it.
  - The consumer-demand durability probe's Stage-2 stop/go gate fails decide-grade.
  - Batch-1 distillation lands a contrary decide-vs-confirm read on the demand substrate.
```

## Status

`OWNER_LOCKED` — ratified by the owner 2026-06-12, in-thread. The owner then
authorized a 2026-06-20 active-body integration: the decision-led,
evidence-backed headline value proposition and action vocabulary are operative
inside this thesis body, not as separate override notes.

The 2026-06-12 ratification receipt remains (ask 1 ratified AS AMENDED;
verbatim words and effects recorded in the Owner Decision Record of
`docs/decisions/orca_consumer_demand_ratification_decision_memo_v0.md`):

- Ask 1 — owner words: "no for 1 - it does not depend on no live ToS
  violating source. we accept the risks for ToS just not at an absurd level
  (e.g. Brightdata)". Effect: the Product Boundary capture bullet is restated
  under the measured-ToS-risk posture (dated amendment 2026-06-12 below);
  the prior "does not depend on any live ToS-violating source" premise is
  retired.
- Ask 2 — "co-ratify ok": the wedge record
  (`docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md`) is
  co-ratified as the wedge direction lock.
- Ask 3 — "yes thats okay": durability probe Stage-1 feasibility gate
  authorized per the decision memo's recommendation (Stage 2 held until
  Stage 1 reports); execution belongs to the `consumer-demand-probe` lane
  under its own authorization record.
- Ask 4 — "yes close for now": the outreach gate stays closed; no opening
  condition named.

Historical: proposed as `PROPOSED_PENDING_OWNER_SIGNOFF` by the product-lead
lane 2026-06-11. Owner direction recorded in-thread that day: the
consumer-demand/beauty direction "feels more possible than b2b pricing";
formal wedge sign-off deferred until a thesis exists; this record was that
thesis, proposed.

Preparation basis: a four-lane read-only exploration sweep across the current
branch and the `consumer-demand-probe`, `capture-demand-projection`,
`capture-probe-tiktok-demand`, `capture-cloak-scroll`,
`capture-archive-snapshot-timing`, and `capture-archive-cdx-bound` lanes (full
source ledger in the preparing thread's closeout). No explored lane contradicts
this center; the binding constraints found are claim-tier discipline and
capture-entitlement walls, both encoded below.

This thesis states a DIRECTION and a center of gravity. It is not validation,
buyer proof, willingness-to-pay, judgment-quality evidence, or readiness.

## Active Reading

Owner-ratified directions through 2026-06-20 are folded into the active thesis
body below. Historical ratification receipts remain in the propagation section;
the operative product wording is this body, not a stack of override notes.

## Thesis (the bet)

Forseti helps consumer-market leaders make **evidence-backed strategic decisions**
before internal data is conclusive: whether to monitor, probe, commit, hold,
scale, avoid, or reduce, and at what scale the evidence supports.

Today's sharpest engine is productized outside-in consumer-demand intelligence.
It turns messy, contradictory public demand signals — reviews, forums, search
interest, retail presence, social chatter — fused with org-motion corroboration
(hiring composition and headcount at brand (Brand) and parent level (Org)) into
clean, evidence-backed, calibrated decision evidence that discriminates
**real durable demand, real transient demand, and manufactured demand**.

Demand integrity and durability are the first reads, not the ceiling; the product
can add further evidence-backed reads as the decision spine expands. It serves
the people who must allocate against that distinction: operators committing
inventory, retail, launch, or pricing budget first; investors underwriting
consumer demand later. Beauty/personal-care is the first vertical; the engine,
spine, and method are vertical-portable by design.

## Value Proposition

For a decision owner (Buyer) facing a live consumer-demand allocation decision
(DecisionEvent) before internal data is conclusive, Forseti delivers the decided
answer — "this demand is real-and-durable / real-but-transient / manufactured;
monitor, probe, commit, hold, scale, avoid, or reduce; here is what would change
the answer and when" — as a **calibrated decision with an action ceiling, never
a feed**, built from an inspectable memo (Memo) + evidence appendix substrate,
never a dashboard or source dump.

The differentiated mechanism is judgment discipline over a hostile substrate,
not access to data: provenance-verified capture, integrity labels
(artificial-amplification risk, incentive distortion, copied/coordinated),
costly-behavior demand classification, entity-resolved brand→parent rollups,
explicit action ceilings, and published backtest receipts that show the method
called at cutoff against what actually happened — misses included.

## The Central Read (what the product decides)

1. **Real first, then durable-or-transient.** Two questions, in order: is the
   demand *real* (costly behavior) or *manufactured* (fake/amplified →
   avoid)? If real, is the strong current-window demand expected to stay strong
   over the relevant decision horizon (**durable**) or is it strong only in the
   current window / expected to decay (**transient**)? Durable is a
   forward-looking demand call with a named evidence basis for projected
   persistence, not a retrospective label that demand already stayed strong.
   Observed persistence can be one basis; repeated costly behavior, analogue
   history, post-trigger follow-through, and org-motion corroboration can also
   support or contest the projection. Weak, attention-only, resonance-only, or
   manufactured signals are not transient demand. Horizon accretes through monitoring;
   `scale` earns the long horizon, and `reduce` handles decay. The persistence
   half is what the consumer-demand durability probe spec is designed to test
   blind against momentum and category-prior baselines
   (`consumer_demand_durability_probe_spec_v2.md`, lane `consumer-demand-probe`,
   status `PROPOSED_PROBE_SPEC_V2 — KEEP-CLEARED`; review state, not execution
   authority).
2. **Demand means costly behavior.** Per the frozen Core Spine rule, demand is
   evidenced by payment, switching, workarounds, churn, durable buyer
   pressure — never engagement/resonance volume alone. Engagement should be
   interpreted as qualitative resonance weight, and still cannot carry a Commit. This single rule is the
   structural separation from social-listening and trend dashboards.
3. **Divergence reads are the premium element.** Demand and org-motion are
   read together: demand↑ + staffing↑ (durable conviction), demand↑ +
   staffing-flat (flash or capital-constrained), staffing↑ + demand-flat
   (betting ahead of the market). Org-motion is corroboration inside the
   artifact — never a standalone product, never person-level.
4. **Every read carries an action ceiling.** Outputs bind to the active flat
   action vocabulary — monitor, probe, commit, hold, scale, avoid, reduce — and
   the recommendation verb may not exceed what signal integrity supports. The
   cap logic is unchanged: engagement/resonance-only caps below material commitment, and
   any material or irreversible commitment requires enough effectively
   independent origins for that commitment.
5. **Manufactured-vs-organic is scoped honestly.** Backtests can test
   persistence discrimination; they cannot recover historical paid-proxy
   spend. Manufactured-demand separation is a forward/live capability with
   cross-signal consistency as a partial flag — claimed only at that strength.

## Strategic Center (what compounds)

- Clean, provenance-verified public evidence earns trust (capture armory +
  ECR integrity postures).
- Costly-behavior demand classification plus integrity judgment prevents
  overreaction to manufactured noise — the failure mode the substrate invites.
- The entity-resolution join (brand → parent hierarchy, load-bearing in
  beauty) makes signals roll up and down ownership trees; built narrow for
  the wedge's entities, designed to widen.
- Outcome memory is the moat: pre-declared, anti-cherry-picked backtest
  ledgers and calibration receipts compound into evidence no copywriter can
  fake.
- Differentiation floor and moat: the mechanical layers (costly-behavior
  classification, org-motion fusion, entity resolution) genuinely beat a social
  listener's inputs but are *replicable features* — a survivable fallback
  business, not a moat. The uncopyable, category-defining differentiator is the
  calibrated **judgment + outcome memory**; don't sell the plumbing, sell the
  calibrated decision. (Positioning hypothesis, not a validated claim.)
- Standard ownership is the commercial posture (claim-defense doctrine,
  owner-signed 2026-06-11): Forseti owns and publishes the judgment-evidence standard
  it grades itself against — "built to" ships now; "proven at" only with the
  receipted rung.

## Product Boundary

Carried from thesis v0 and sharpened for the demand substrate:

- Not a social-listening dashboard, trend feed, monitoring service, data
  broker, scraping commodity, or report factory. No person-level dossiers in any
  sold or externally published surface, and no outreach lists at all; org-level
  signals only. (Internal
  wind-caller calibration is the bounded exception per
  `docs/decisions/wind_caller_calibration_carveout_v0.md` — named public-figure
  calibration, non-permanent, internal-use only; the cap applies to our own
  operating/capture accounts (≤10, starting ≤5); the subject-creator roster is
  uncapped (all-in-vertical); active capture = attended/human-initiated; passive
  monitoring = human-initiated, time-bounded, self-terminating runs (carve-out
  2026-06-15 amendment);
  the external/product boundary here is unchanged.)
  [Amended 2026-07-05 (owner-approved in-thread): a second bounded exception —
  the **Aphrodite** productized Creator Signal surface may sell
  creator/channel-level reads within its own forbidden set (no
  contact/outreach/lead-lists/person-identity-proof; aggregate-only audience
  signals), per
  `forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md`. It
  is a *sold* creator-level surface, so it is a deliberate, bounded carve to
  "org-level signals only," scoped to the Aphrodite creator-intelligence
  product; the org-level-only default still governs every other sold or
  published surface.]
- **Recurring decisions, not a feed.** Where a read is monitored over time
  (transient → earn-durable), every output stays a calibrated decision with an
  action ceiling — never a monitoring feed or stream. This keeps Forseti off the
  buyer-proof "monitoring-only pull" kill and out of the social-listening
  category (the never-a-feed invariant; owned in the buyer-proof packet).
- No fake reviews, botting, astroturf, manipulation, or deceptive competitive
  tactics — Forseti detects and discounts these; it never produces them.
- Capture risk posture (owner-amended at ratification, 2026-06-12): Forseti
  accepts measured platform-terms (ToS) risk in capture; it rejects
  absurd-level risk approaches (the owner's example: Bright-Data-style
  industrial scraping). The thesis is NOT premised on avoiding every live
  ToS-violating source. Per-venue route bindings stay capture-lane-owned and
  are revisited there under this posture (LinkedIn live NO-GO today; TikTok
  live ratified GO by owner word 2026-06-12 — the owning capture-lane
  records still carry the pre-ratification NO-GO and owe their own dated
  alignment; TikTok archive's closed 2019–2023 window is a coverage fact,
  unchanged). No standing monitor, broad crawler, or production pipeline is
  implied.
- Raw signals are inputs, not evidence. Nothing reaches a buyer artifact
  without provenance, integrity labels, classification, and constraint.

## Internal Product Shape (the spine, with build-state labels)

One engine, layered per the frozen boundary contracts (Capture ≠ ECR ≠
Cleaning ≠ Judgment ≠ Artifact ≠ Outcome Memory; reference, never merge):

1. **Source Capture Armory** — bounded, provenance-hashed capture of public
   surfaces (CloakBrowser route, archive adapters with typed snapshot time and
   cutoff-bounded CDX, review surfaces via incremental scroll). Built and
   probe-verified on beauty venues (Sephora reviews GO; Ulta embedded state
   GO; Reddit bounded GO).
2. **Demand projection** — deterministic, no-LLM extraction of dated
   `demand_observation` time-series (search_interest, review_event_or_velocity,
   retail_presence) from captured bytes via declared-semantic anchors;
   live-validated (Ulta, 43 observations); genericity proven across three
   surface shapes. Its F6/R6 design currently carries
   `NEEDS_ARCHITECTURE_PASS` (result-algebra, snapshot-time ownership,
   coordinate identity) — a bounded settlement, not a thesis blocker.
3. **ECR integrity postures** (SP-1/2/3/6 built; JSG-01 conductor FROZEN) and
   **Cleaning** — receipts and non-destructive transformation, owning no
   credibility judgment.
4. **Entity-resolution spine** — the canonical join (LinkedIn/ATS slugs,
   retailer spellings, brand vs parent) signals roll up through. Direction
   agreed; narrow-now-widen; not yet built — its own gated lane.
5. **Judgment spine** — decide-vs-confirm grading, integrity-affected decision
   strength, action ceilings, zero-spoiler blind execution, memorization-
   resistant case selection (finder frame, pending sign-off; web-search-off
   discipline).
6. **Outcome memory / calibration** — pre-declared batch ledgers, all-results
   reporting, recognition checks, distillation records (batch 1 active and
   owner-signed).

Satellites adapt the spine to vertical, venue set, decision family, and
buyer language (beauty is the first satellite); the core stays
market-agnostic per the Core Spine satellite contract.

## Vertical And Geography Doctrine (beauty first, US first, narrow-then-widen)

- Beauty/personal-care is the proof vertical: substrate-rich (reviews,
  Reddit/forums, trackers, trade press), entity hierarchies tractable, and
  the proof engine already runs there. "Good proof vertical" and "durable
  market" stay separate questions; widening is a later owner decision.
- Geography doctrine (owner-adopted 2026-06-12, "bake that into thesis";
  consistent with the same-day US-default direction already recorded in the
  discovery lane's candidate-pool handoff): the first proof runs US-market —
  the probe-verified venue set, the compounding screen knowledge,
  English-language receipts, and the FTC-calibrated integrity flags all sit
  there. US brands/ecosystem is the default; non-US candidates route to the
  owner or defer. The engine is geography-portable by design — EU/UK is a
  later widening decision (bringing its own claims/integrity doctrine row,
  e.g. Omnibus/DSA, and a stricter org-motion privacy posture), not part of
  the first proof. The exception gate is the substrate, not the passport: a
  qualified non-US buyer whose decision sits on capturable venues is routed
  to the owner, not refused outright.
- Venue knowledge compounds by Shape C only: the owner-adopted thin
  exploration procedure plus append-only Screen/Venue Provenance blocks — no
  registry, atlas, or standing source map (owner-rejected 2026-06-11;
  independently supported by the source-registry research: registries rot
  fastest exactly where they are honor-maintained). Beauty has been screened
  twice; the next beauty screen fires the promote-on-reuse card-set trigger,
  owner-routed.
- The higher-value case class is **subtle decisions** — price nudges, quiet
  reformulations, silent SKU kills, unannounced channel shifts — which live at
  the origination layer (community boards, trackers) before any trade-press
  laundering, and which the memorization-resistant finder frame prefers.
- Influence observations ("wind-callers": testers, community hubs whose calls
  move the market) are recorded as dated provenance and feed signal
  attribution — history, never a maintained current-state asset.

## Buyer Ladder And First Application

The first-proof application is decided in the subordinate wedge record
(`docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md`, pending the same
sign-off): indie/DTC beauty operator first door (live demand-allocation
decision), consumer seed/VC fund screen as the second door, PE/family-office
diligence as the destination — ordered by reachability under the owner's
no-warm-leads constraint, with backtest-as-public-proof as the primary
door-opener.

The thesis binds the ladder's shape (operator decisions first, screen-tier
second, diligence-tier destination); the wedge record owns the first-proof
specifics and their kill/reframe conditions.

## Proof Doctrine

- The evidence ladder governs every claim: `product_learning` →
  `buyer_proof` → `judgment_quality`, weakest-cleared-gate caps, one-way
  promotion, closeout states named inline. All evidence behind this thesis
  today is product-learning tier or below (discovery/feasibility) — stated
  plainly, here and externally.
- Public proof motion: publish zero-spoiler backtest receipts (pre-declared
  ledgers, all results including misses) under the claim-defense doctrine's
  wording discipline ("built to" vs "proven at"; tier label on every external
  sentence; concession-as-demo). The running engines are batch 1
  (owner-signed, active) and — if the owner authorizes execution — the
  consumer-demand durability probe (spec keep-cleared; execution not yet
  authorized).
- Buyer proof starts only at a qualified live decision + memo + readback under
  the buyer-proof packet's unchanged gates (trust ladder, pull-vs-praise,
  kill/graduation, paid-first). The standing no-buyer-contact-before-
  full-spine-MVP gate is untouched by this thesis; opening it is a separate
  owner decision.
- Backtests obey cutoff discipline, leakage controls, recognition checks, and
  the zero-spoiler lanes; contaminated arms are data, never discarded
  silently.

## Falsifiers (what would break this thesis)

- The durability probe's Stage-2 blind momentum-matched pair fails decide-grade
  — the central discrimination claim loses its support path; the product
  re-scopes toward screen-tier reads (rank-and-shortlist) pending a new
  judgment angle.
- Batch-1 distillation shows demand reads landing confirm-only or persistently
  out-of-band — same consequence; the wedge record's pivot condition fires.
- Demand-projection or capture walls prove harder than probed (e.g., archive
  coverage gaps of the TikTok field-decay kind generalize across venues) —
  the substrate thins; venue mix and vertical choice re-open.
- At buyer-proof tier: the buyer-proof packet's kill criteria (no decision
  use, monitoring-only pull, consulting-risk-only delivery) fire after a real
  proof batch.

## Carried From Thesis v0 / Changed

Carried: outside-in posture; decide-before-internal-data-is-conclusive; memo +
evidence appendix as the substrate with the executive deck as the buyer
surface; signal-quality judgment as the differentiator; outcome memory as the
moat; all v0 product boundaries; the core/satellite split.

Changed: the strategic center now leads with evidence-backed strategic decisions
for consumer-market leaders, with consumer-demand integrity and durability as
the first reads; the central read is named (real durable / real transient /
manufactured); org-motion corroboration and the entity join enter the product
shape; beauty becomes the first vertical; the buyer ladder replaces the
undifferentiated "leaders" framing; proof doctrine binds to the evidence ladder
and claim-defense wording that postdate v0.

Client 0 (`jb`, v0's internal method client) is carried as historical method
context; the consumer-demand center does not depend on it, and the proof
center of gravity moves to the beauty backtest portfolio.

## Evidence Basis (tiered; status labels verbatim)

| Lane / artifact | Status | Contributes |
| --- | --- | --- |
| Batch-1 ledger (`judgment_spine_backtest_batch1_ledger_declaration_v0.md`) | `BATCH1_ACTIVE_OWNER_SIGNED` | Running beauty proof engine; anti-cherry-pick ledger discipline |
| Durability probe spec v2 (lane `consumer-demand-probe`) | `PROPOSED_PROBE_SPEC_V2 — KEEP-CLEARED` | Designed blind test of the central read; review state only |
| Demand projection (lane `capture-demand-projection`) | built; design review `NEEDS_ARCHITECTURE_PASS` | Deterministic demand_observation extraction; Ulta live 43 obs |
| Beauty Pie org-motion feasibility (`docs/research/`) | DISCOVERY / FEASIBILITY — Gate-0 PASS (ATS-led) | Org-motion archive-backtest viability; provenance cap noted |
| TikTok probe (lane `capture-probe-tiktok-demand`) | PARTIAL at thesis prep (archive GO-fidelity / live NO-GO legal); owner ratified TikTok live = GO 2026-06-12 in-thread — lane-record alignment pending in the capture lane | Social demand venue limits; field-presence playbook gap |
| Sephora reviews (lane `capture-cloak-scroll`) | corrected GO via incremental scroll | Beauty review substrate capturable |
| Venue procedure + beauty proving screen | `SHAPE_C_OWNER_ADOPTED`; proving run 2026-06-11 | Venue doctrine; 7 screen-grade candidates; subtle-decision class |
| Finder frame | `PROPOSED_DOCTRINE_FRAME_PENDING_SIGNOFF` | Memorization-resistant case selection |
| Claim-defense doctrine | `OWNER_SIGNED_OPERATIVE` 2026-06-11 (review-patched, then signed) | External claim wording discipline |
| Core Spine contracts / IPF / boundary / ladder / ECR submap | `PROPOSED_FREEZE` (SP-1/2/3/6 built; JSG-01 FROZEN) | The frozen foundation this thesis sits on |

Nothing above is validation, buyer proof, or judgment-quality evidence; the
weakest-cleared-gate rule caps every claim.

## Doctrine-Change Propagation — Executed (2026-06-12)

Ratification executed per
`docs/product/product_lead/orca_ratification_day_runbook_v0.md` (one pass;
this receipt also covers the co-ratified wedge record's cascade — one
ratification event, one receipt, pointed to from the wedge record).

```yaml
direction_change_propagation:
  doctrine_changed: >
    The controlling Forseti product thesis moves to consumer-demand decision
    intelligence (beauty first vertical) with the owner's measured-ToS-risk
    capture posture amendment, and the first-proof wedge moves to the beauty
    operator door, superseding turn_08 and pricing-first; subordinate
    product-lead artifacts re-targeted via the prepared consumer-demand
    revision packages (applied with recorded deviations).
  trigger: product_doctrine
  related_triggers: []
  controlling_sources_updated:
    - docs/decisions/forseti_product_thesis_consumer_demand_v0.md
    - docs/decisions/turn_08_product_thesis_v0.md
    - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
    - docs/decisions/orca_icp_wedge_pricing_first_v0.md
    - docs/decisions/orca_consumer_demand_ratification_decision_memo_v0.md
    - docs/product/product_lead/orca_offer_hypothesis_v0.md
    - docs/product/product_lead/orca_buyer_proof_packet_v0.md
    - docs/product/product_lead/orca_product_proof_lead_charter_v0.md
    - docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md
    - docs/product/product_lead/orca_discovery_batch_0_target_selection_brief_v0.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/project-authority.md
    - .agents/workflow-overlay/artifact-roles.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/hygiene/queue.md
  downstream_surfaces_checked:
    - AGENTS.md                                   # no thesis/wedge content; routes to overlay — unchanged
    - CLAUDE.md                                   # shim — unchanged
    - .agents/workflow-overlay/product-proof.md   # wedge-agnostic semantics — unchanged
    - docs/product/core_spine/core_spine_v0_product_contract.md  # senior frozen contract — unchanged
    - docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md  # senior; one-way subordination — unchanged
    - docs/product/product_lead/orca_claim_defense_doctrine_v0.md  # owner-signed wording policy — unchanged
    - docs/product/product_lead/orca_discovery_batch_0_qualification_prep_sentry_clerk_v0.md  # already superseded-bannered; resolves via chain
    - docs/product/product_lead/orca_discovery_batch_0_candidate_context_scan_v0.md  # same chain resolution
  intentionally_not_updated:
    - path: docs/prompts/product-planning/orca_product_proof_lead_customer_discovery_prompt_v0.md
      reason: >
        Prompt artifact outside the product lane's write scope; queued as
        ORCA-HYGIENE-018 for a prompt-orchestration lane. Until realigned it
        remains pricing-gated and must not drive consumer-demand discovery.
    - path: .agents/skills/orca-product-lead/SKILL.md and .claude/skills/orca-product-lead/SKILL.md
      reason: >
        Skill source is sha-pinned under skill-adoption governance; queued as
        ORCA-HYGIENE-019 for an authorized skill-edit lane.
    - path: capture-lane source-access boundary decisions (LinkedIn/TikTok walls, Reddit ordering)
      reason: >
        The ask-1 amendment sets the product-level risk posture; per-venue
        route bindings are owned by capture-lane decisions and are revisited
        there, not silently rewritten by ratification.
    - path: pre-migration flat docs/product/ paths inside product-lead docs
      reason: >
        Owned by the Phase-2 migration posture (forward-only resolve via
        moved_paths_index.md; ORCA-HYGIENE-016 owner decision).
  stale_language_search: >
    rg -in "turn_08_product_thesis|pricing.first|PROPOSED_PENDING_OWNER_SIGNOFF"
    docs/decisions docs/product/product_lead .agents/workflow-overlay
    docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-06-12 after the cascade edits. Overlay + repo-map hits for
    turn_08 are all supersedes-annotations on the new thesis path; the only
    live-routing residue is the two orca-product-lead skill copies (queued,
    ORCA-HYGIENE-019) and the customer-discovery prompt (queued,
    ORCA-HYGIENE-018). PROPOSED_PENDING_OWNER_SIGNOFF survives only in the
    two anchors' "Historical: proposed as" lines and this receipt's own
    search string. A "current wedge authority" sweep caught two stale
    Source Use / Source Basis lines still labeling pricing-first as current
    (offer hypothesis; charter) — both fixed in the same pass, dated.
    Remaining pricing-first / turn_08 mentions are superseded banners,
    historical reasoning, review records, input_hash provenance pins, and
    the prep lane's own consistency report — intended residue, none of it a
    live routing surface.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not judgment-quality evidence
    - ratification locks a direction; every gated lane keeps its own authorization boundary
```

## Owner Sign-Off Asks (decided 2026-06-12 — outcomes in Status; retained as asked)

1. **Ratify this thesis** as the controlling product center (or amend: e.g.,
   keep the v0 sector-agnostic framing with consumer-demand as first
   application only).
2. **Co-ratify the wedge record** (operator-first beauty door) or amend its
   ordering — the thesis fixes the ladder shape; the wedge record fixes the
   first door.
3. **Authorize the durability probe's next gate** (Stage 1 feasibility /
   Stage 2 blind pair execution) — the spec is keep-cleared but execution is
   explicitly not yet authorized; it is the cheapest direct test of the
   thesis's central read.
4. **Outreach gate posture** — unchanged default (closed) unless you name the
   opening condition; ratifying 1–3 does not open it.

## Non-Claims

- Ratified 2026-06-12 (see Status) — a direction lock only. Still not
  validation, willingness-to-pay, buyer pull, buyer proof, judgment quality,
  readiness, or proof the direction will win.
- Asserts no build authorization: no entity-spine build, no live-source
  calls, no probe execution, no capture expansion, no dashboards, no
  automation, no outreach. Every gated lane keeps its own authorization
  boundary; JSG-01 stays frozen.
- Quotes lane findings at their recorded status; keep-cleared review states
  are not execution authority; discovery and feasibility evidence is not
  product-learning validation.
- The wedge record, probe specs, and doctrine drafts it cites remain
  separately owned and separately signable; this thesis does not ratify them
  by reference.
- Mints no evidence-ladder vocabulary and amends no overlay rule beyond the
  ratification pointer re-points; the propagation receipt is in the
  Doctrine-Change Propagation section above.

```yaml
direction_change_propagation:
  note: >
    This file is a downstream surface of the carve-out 2026-06-15
    cap-redefinition propagation. The Product Boundary parenthetical (wind-caller
    calibration exception) has been updated to reflect that the cap applies to
    our own operating/capture accounts (≤10, starting ≤5), the subject-creator
    roster is uncapped (all-in-vertical), and the active/passive method
    distinction (active = attended; passive = bounded self-terminating runs).
    The external/product boundary clause is unchanged and preserved verbatim.
  authority: docs/decisions/wind_caller_calibration_carveout_v0.md (2026-06-15 amendment)
  date: 2026-06-15
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Product Boundary amended (2026-07-05, owner-approved in-thread): the
    "no person-level dossiers in any sold/published surface; org-level signals
    only" boundary gains a second bounded exception (alongside internal
    wind-caller calibration) — the Aphrodite productized Creator Signal surface
    may sell creator/channel-level reads within its own forbidden set (no
    contact / outreach / lead-lists / person-identity-proof; aggregate-only
    audience signals). A scoped carve for the Aphrodite creator-intelligence
    product; the org-level-only default still governs all other sold/published
    surfaces.
  trigger: product_doctrine
  related_triggers: []
  controlling_sources_updated:
    - docs/decisions/forseti_product_thesis_consumer_demand_v0.md   # Product Boundary bullet
  downstream_surfaces_checked:
    - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md   # carve is bounded by the charter's own forbidden set; consistent, no charter edit needed for A1
    - forseti/product/spines/creator_signal/README.md                          # spine Dashboard Boundary already scopes creator-level display; consistent
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not outreach or publishing authorization — creator-level selling is permitted in scope; phase/outreach gates unchanged
```
