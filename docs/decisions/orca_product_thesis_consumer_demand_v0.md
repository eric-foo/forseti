# Orca Product Thesis v1 — Consumer-Demand Decision Intelligence (Proposal)

```yaml
retrieval_header_version: 1
artifact_role: Decision record (controlling product thesis — owner-ratified)
scope: >
  V1 product thesis re-centering Orca on consumer-demand decision
  intelligence (durable / transient / manufactured demand discrimination), beauty/personal-care
  as the first vertical (Vertical), on the existing outside-in engine and frozen Core
  Spine foundation. Prepared 2026-06-11 after a cross-branch exploration
  sweep; ratified by the owner 2026-06-12 with the ask-1 capture-risk
  amendment folded in (see Status). Supersedes
  docs/decisions/turn_08_product_thesis_v0.md as the controlling product
  thesis.
supersedes:
  - docs/decisions/turn_08_product_thesis_v0.md
use_when:
  - Owner sign-off on the consumer-demand product thesis.
  - Anchoring product, capture, judgment, or proof lanes to the product center.
  - Checking whether a proposed product claim, artifact, or lane fits the thesis.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/turn_08_product_thesis_v0.md
  - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md
  - forseti/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md
stale_if:
  - The owner amends this record (dated amendments only; no silent rewrites).
  - The consumer-demand durability probe's Stage-2 stop/go gate fails decide-grade.
  - Batch-1 distillation lands a contrary decide-vs-confirm read on the demand substrate.
```

## Status

`OWNER_LOCKED` — ratified by the owner 2026-06-12, in-thread, with one
amendment (ask 1 ratified AS AMENDED; verbatim words and effects recorded in
the Owner Decision Record of
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

## Amendment — 2026-06-14 (owner): Demand-State Model (durable / transient / manufactured)

Owner-authorized in-thread. The central read's framing changes from **durable vs
hollow** to **two independent axes**. This amendment governs forward; the in-body
"durable vs hollow" phrasings below (Value Proposition; Central Read #1; the named
read line) are read through it (dated amendment; original preserved, not silently
rewritten — consistent with this record's amendment rule).

- **Two axes, not one.** *Persistence:* **durable** (demand persists past its
  trigger) vs **transient** (real demand that decays). *Integrity:* **real**
  (costly behavior) vs **manufactured** (fake / amplified). "Hollow" is retired —
  it conflated *transient* (real but short-lived, still valuable short-term) with
  *manufactured* (not real).
- **Three actionable states.** Durable → *commit* (long horizon); transient →
  *move* (short horizon, time-boxed to the decay window); manufactured →
  *discount / avoid*. The action ceiling is matched to the demand's **lifespan**,
  not only its strength — binding to the frozen ladder as long-horizon **Commit**
  vs short-horizon **Move**.
- **Transient gets equal billing** with durable as a read (owner: transient
  spikes are still capital-allocation decisions and occur more often than durable
  shifts; a durable-only product serves too thin a slice).
- **Calling sequence (dissolves the decay-timing problem).** The read opens
  **transient** and acts in-window (buy or avoid); durability is then **observed
  via monitoring, not predicted**, and **earned** as an upgrade when persistence
  holds. There is no decay curve to forecast; the earlier decay-timing-confidence
  guardrail is superseded by observe-don't-predict. Durable stays claim-honest
  (built-to; proven only once monitored persistence confirms it).
- **Billing shape & the never-a-feed invariant.** Monitoring is recurring →
  **retainer / upgraded billing**, but only as **recurring decisions**; every
  output is a calibrated decision with an action ceiling, **never a feed**. (A
  feed trips the buyer-proof "monitoring-only pull" kill *and* is what would make
  Orca social listening — same activity, opposite product.) The monitored
  outcomes are also the calibration data that earns the judgment moat.
- **Differentiation floor.** The mechanical layers (costly-behavior primitive,
  org-motion fusion, entity resolution) genuinely beat a social listener's inputs
  but are *replicable features* — a survivable fallback business, not a moat. The
  durable, uncopyable differentiator is the calibrated **judgment + outcome
  memory**: don't sell the plumbing, sell the calibrated decision. This
  reinforces the Strategic Center (judgment over a hostile substrate, not access
  to data); it is a positioning hypothesis, not a validated claim.
- **Identifying manufactured demand is decision-critical in its own right**
  (owner) — the integrity axis is the contamination check that protects both real
  reads, not merely an avoid filter.
- **Falsifier note:** the durability probe's central discrimination is the
  persistence axis (durable vs transient); manufactured separation remains the
  forward/live capability it already was. No falsifier is weakened.

The operative grammar for this model is
`docs/product/product_lead/orca_demand_read_taxonomy_v0.md` (restructured
2026-06-14) and its adjudication companion
(`orca_demand_read_taxonomy_adjudication_v0.md`, Q0). This amendment is the
thesis's owed dated pointer under the Doctrine Change Propagation Contract.

```yaml
direction_change_propagation:
  doctrine_changed: >
    The thesis central read changes from binary durable-vs-hollow demand
    discrimination to a two-axis demand-state model: durable-vs-transient
    (persistence) and real-vs-manufactured (integrity), yielding three actionable
    states (durable=commit; transient=move/short-horizon; manufactured=
    discount/avoid). "Hollow" is retired as conflating transient with
    manufactured. Transient gets equal billing as a read, with the decay-timing
    problem dissolved by the calling sequence (observe persistence, not predict
    decay); identifying manufactured demand is decision-critical in its own right.
  trigger: product_doctrine
  related_triggers: []
  controlling_sources_updated:
    - docs/decisions/orca_product_thesis_consumer_demand_v0.md               # this dated amendment
    - docs/product/product_lead/orca_demand_read_taxonomy_v0.md              # restructured to the model
    - docs/product/product_lead/orca_demand_read_taxonomy_adjudication_v0.md # Q0 recorded; read types updated
  downstream_surfaces_checked:
    - path: docs/product/product_lead/orca_buyer_proof_packet_v0.md
      note: >
        carries "durable-vs-hollow demand discrimination" framing (~L53, ~L215)
        and "hollow demand" (~L234, manufactured-sense); superseded-by this
        amendment; FLAGGED for a dated wording-realignment pass — named here, not
        silently rewritten.
    - path: docs/product/product_lead/orca_offer_hypothesis_v0.md
      note: >
        carries "durable-vs-hollow" (~L70) and "hollow or manufactured" (~L219,
        ~L339); same realignment-pending status.
    - path: docs/product/product_lead/orca_product_proof_lead_charter_v0.md
      note: >
        carries "hollow demand" (~L158, ~L170, manufactured-sense); same
        realignment-pending status.
    - path: docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
      note: uses divergence reads but no "hollow" framing; consistent with the model — no change needed.
  intentionally_not_updated:
    - path: docs/decisions/orca_consumer_demand_ratification_decision_memo_v0.md
      reason: >
        dated record of the 2026-06-12 ratification; its "durable-vs-hollow" is an
        account of what was decided then — rewriting it would falsify the record.
        Forward-only.
    - path: docs/prompts/product-planning/consumer_demand_probe_stage1_feasibility_commission_prompt_v0.md
      reason: >
        mid-flight commission prompt; its persistence-discrimination wording is
        still substantively correct (durable vs transient); realign on reissue.
    - path: docs/prompts/handoffs/capture_spine_archive_snapshot_typed_timing_handoff_prompt_v0.md
      reason: handoff prompt artifact; the "persistence signal" sense is unchanged by the rename.
    - path: docs/review-inputs/demand_projection_f6_r6_norepo_adversarial_artifact_review_bundle_v0/demand_projection_f6_r6_revised_design_v0.md
      reason: review-input design artifact; historical bundle, not a live routing surface.
    - path: orca-harness/** and docs/review-outputs/** uses of "hollow"
      reason: >
        "hollow" there means "lacking substance" (hollow tests / hollow non_claims
        / hollow receipt) — unrelated to the demand axis; must NOT be renamed.
  stale_language_search: >
    rg -in "durable.?vs.?hollow|hollow demand|durable demand from hollow"
    docs/decisions docs/product/product_lead
  stale_language_search_result: >
    Executed 2026-06-14 after this amendment. Remaining demand-sense hits are the
    three ratified surfaces named above (buyer-proof, offer, charter) flagged for
    the realignment pass, plus the ratification memo (historical record). The
    taxonomy, companion, and this thesis amendment carry the new model. No
    "lacking-substance"-sense occurrence (hollow tests/non_claims/receipt) was
    touched.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not judgment-quality evidence
    - the decay-curve capability and decay-timing calibration do not yet exist (transient reads are built-to, not proven-at)
```

## Amendment — 2026-06-20 (owner-directed): Canonical Headline Value Proposition (Decision-Led)

Owner-directed in-thread; lock of the iterated headline sentence. The canonical
one-line value proposition is now:

> **Orca helps consumer-market leaders make evidence-backed (demand integrity,
> durability & more) strategic decisions — whether to commit, hold, or avoid, and
> at what scale the evidence supports — before internal data is conclusive.**

This **leads** the framing; the "Thesis (the bet)" and "Value Proposition"
sections below are read through it (dated amendment; originals preserved).

- **The decision is the identity.** The customer-facing lead is the strategic
  decision (commit / hold / avoid, at the scale the evidence supports), not the
  mechanism. This sharpens — and slightly broadens — the 2026-06-12 framing that
  named "consumer-demand" as the product's subject: the headline subject is now
  the decision, with the demand reads as its evidence.
- **Demand integrity & durability are the first (and currently sharpest) reads,
  not the ceiling.** The "& more" is deliberate: further reads will be added as
  the product expands. The engine described in "Thesis (the bet)" remains
  consumer-demand-centric *today* (demand integrity & durability are the reads it
  runs); "& more" reserves the expansion path and keeps the headline from
  hard-locking the product to demand — consistent with the offer hypothesis's
  existing broad umbrella ("foundational strategic and hyper-competitive
  decisions").
- **"At what scale the evidence supports"** is qualitative scale guidance (the
  action ceiling) — a positive claim, not a precise quantity.

Unchanged: the first-proof wedge (beauty operator demand-allocation), the
evidence ladder, the vertical/geography doctrine, all product boundaries, and
every non-claim. This is a headline framing lock, not a wedge, vertical, or proof
change.

```yaml
direction_change_propagation:
  doctrine_changed: >
    The Orca product thesis adopts a locked, decision-led canonical headline
    value proposition ("Orca helps consumer-market leaders make evidence-backed
    (demand integrity, durability & more) strategic decisions — commit / hold /
    avoid, at the scale the evidence supports — before internal data is
    conclusive"). The customer-facing subject moves from "consumer-demand" to the
    strategic decision, with demand integrity & durability as the first (not only)
    reads; "& more" reserves expansion. Engine, first-proof wedge, evidence
    ladder, vertical, and all non-claims are unchanged.
  trigger: product_doctrine
  related_triggers: []
  controlling_sources_updated:
    - docs/decisions/orca_product_thesis_consumer_demand_v0.md
  downstream_surfaces_checked:
    - orca/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md
    - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
    - orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
    - orca/product/spines/product_lead/proof_charter/orca_product_proof_lead_charter_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - .agents/skills/orca-product-lead/SKILL.md
  intentionally_not_updated:
    - path: orca/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md
      reason: >
        Already carries the broad umbrella ("foundational strategic and
        hyper-competitive decisions") with beauty demand as the first application;
        the decision-led headline aligns with it rather than contradicting it.
    - path: docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
      reason: >
        First-proof wedge unchanged (beauty operator demand-allocation); the lock
        broadens the value-prop subject, not the wedge.
    - path: orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
      reason: >
        Proof gates, trust ladder, kill/graduation unchanged; demand-first proof
        is consistent with demand being the first reads. Residual
        "consumer-demand" wording is read through this headline; light realign
        deferred and named, not silently forked.
    - path: orca/product/spines/product_lead/proof_charter/orca_product_proof_lead_charter_v0.md
      reason: Proof-lead ownership/exclusions unchanged by a headline framing lock.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: Product-anchor rows route to this thesis as controlling source; no route or anchor target changes.
    - path: .agents/skills/orca-product-lead/SKILL.md (and the .claude/ runtime copy)
      reason: >
        Sha-pinned under skill-adoption governance (ORCA-HYGIENE skill-edit lane);
        the copies route to this thesis as controlling and quote it as history —
        the headline lock changes no routing. Edit deferred to the governed lane.
    - path: docs/decisions/turn_08_product_thesis_v0.md, orca_consumer_demand_ratification_decision_memo_v0.md, orca_ratification_day_runbook_v0.md
      reason: >
        Superseded/dated historical records (the turn-08 thesis and the 2026-06-12
        ratification memo and runbook); forward-only, not rewritten.
  stale_language_search: >
    rg -i "consumer-demand decision intelligence|consumer demand.{0,15}subject" (repo-wide)
  stale_language_search_result: >
    Executed 2026-06-20. Eight files match: this thesis (amending — Thesis-the-bet
    body now read through the new headline); the orca-product-lead skill copies
    (x2, sha-pinned, routing/description — not edited); the repo map (product-anchor
    row routing to this thesis — unchanged); turn_08 (superseded historical); the
    wedge (first-proof, unchanged); and the ratification decision memo and runbook
    (dated 2026-06-12 records — forward-only). None asserts demand as the
    permanent/only subject in a way the "& more" headline forks; the engine is
    consumer-demand-centric today and the offer umbrella is already broad. In-body
    "consumer-demand" naming realignment is deferred and named.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not judgment-quality evidence
    - a headline framing lock only; wedge, vertical, proof gates, and evidence ladder unchanged
```

## Amendment — 2026-06-20 (owner-directed): Action Vocabulary (Replaces The Frozen Ladder)

Owner-directed in-thread. The action-ceiling vocabulary in **Central Read #4**
below — "the frozen vocabulary (Excluded → Watch → Probe → Test → Hold → Move →
Commit)" — and the action verbs in the 2026-06-14 amendment's demand-state mapping
("durable → commit; transient → move") are **superseded** by a single flat verb set:
**monitor · probe · commit · hold · scale · avoid · reduce**. Horizon is no longer declared —
it accretes via monitoring (`scale` earns the long horizon, `reduce` handles decay;
manufactured → `avoid`). There is no `defend` / `narrow` / `phase` / `move`
verb (they fold into `commit` / `monitor` / `probe`). The controlling definition,
cap-rule remap, and rationale live in the demand-read **C3 contract**'s 2026-06-20
amendment (`orca/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md`),
which owns this vocabulary and carries the propagation receipt; this is its faithful
restatement (read Central Read #4 and the 2026-06-14 mapping through it; originals
preserved). The cap LOGIC — ≥2 converging origins for a material commitment,
engagement-only caps below commit — is unchanged; only the verb names change.

## Thesis (the bet)

Orca is a productized outside-in **consumer-demand decision intelligence**
system. It turns messy, contradictory public demand signals — reviews, forums,
search interest, retail presence, social chatter — fused with org-motion
corroboration (hiring composition and headcount at brand (Brand) and parent level (Org)),
into clean, source-backed, calibrated decision evidence that discriminates
**durable demand from transient and manufactured demand** before internal data
is conclusive. It
serves the people who must allocate against that distinction: operators
committing inventory, retail, launch, or pricing budget first; investors
underwriting consumer demand later. Beauty/personal-care is the first
vertical; the engine, spine, and method are vertical-portable by design.

## Value Proposition

For a decision owner (Buyer) facing a live consumer-demand allocation decision (DecisionEvent) before
internal data is conclusive, Orca delivers the decided answer — "this demand is
real-and-durable / real-but-transient / manufactured — *commit*, *move
(time-boxed)*, or *discount*; here is what would change the answer and when" —
as a **calibrated decision with an action ceiling, never a feed**, built from an
inspectable memo (Memo) + evidence appendix substrate, never a dashboard or source dump.

The differentiated mechanism is judgment discipline over a hostile substrate,
not access to data: provenance-verified capture, integrity labels
(artificial-amplification risk, incentive distortion, copied/coordinated),
costly-behavior demand classification, entity-resolved brand→parent rollups,
explicit action ceilings, and published backtest receipts that show the method
called at cutoff against what actually happened — misses included.

## The Central Read (what the product decides)

1. **Real first, then durable-or-transient.** Two questions, in order: is the
   demand *real* (costly behavior) or *manufactured* (fake/amplified →
   discount/avoid)? If real, does it *persist past its trigger* (durable) or is
   it a real spike that *decays* (transient)? The product opens a **transient**
   call and acts in-window (buy or avoid), then **monitors momentum to earn the
   durable upgrade** (commit) — durable is *earned by observed persistence*, never
   asserted up front. The action ceiling is matched to the demand's lifespan
   (short-horizon *move* vs long-horizon *commit*). The persistence half is what
   the consumer-demand durability probe spec is designed to test blind against
   momentum and category-prior baselines
   (`consumer_demand_durability_probe_spec_v2.md`, lane `consumer-demand-probe`,
   status `PROPOSED_PROBE_SPEC_V2 — KEEP-CLEARED`; review state, not execution
   authority).
2. **Demand means costly behavior.** Per the frozen Core Spine rule, demand is
   evidenced by payment, switching, workarounds, churn, durable buyer
   pressure — never engagement volume alone. Engagement classifies as
   attention/resonance and cannot carry a Commit. This single rule is the
   structural separation from social-listening and trend dashboards.
3. **Divergence reads are the premium element.** Demand and org-motion are
   read together: demand↑ + staffing↑ (durable conviction), demand↑ +
   staffing-flat (flash or capital-constrained), staffing↑ + demand-flat
   (betting ahead of the market). Org-motion is corroboration inside the
   artifact — never a standalone product, never person-level.
4. **Every read carries an action ceiling.** Outputs bind to the frozen
   vocabulary (Excluded → Watch → Probe → Test → Hold → Move → Commit); the
   recommendation verb may not exceed what signal integrity supports.
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
  owner-signed 2026-06-11): Orca owns and publishes the judgment-evidence standard
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
- **Recurring decisions, not a feed.** Where a read is monitored over time
  (transient → earn-durable), every output stays a calibrated decision with an
  action ceiling — never a monitoring feed or stream. This keeps Orca off the
  buyer-proof "monitoring-only pull" kill and out of the social-listening
  category (the never-a-feed invariant; owned in the buyer-proof packet).
- No fake reviews, botting, astroturf, manipulation, or deceptive competitive
  tactics — Orca detects and discounts these; it never produces them.
- Capture risk posture (owner-amended at ratification, 2026-06-12): Orca
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

Changed: the strategic center names consumer demand as the product's subject
(v0 was decision-family-agnostic "strategic intelligence"); the central read
is named (durable / transient / manufactured, per the 2026-06-14 amendment);
org-motion corroboration and the entity join
enter the product shape; beauty becomes the first vertical; the buyer ladder
replaces the undifferentiated "leaders" framing; proof doctrine binds to the
evidence ladder and claim-defense wording that postdate v0.

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
    The controlling Orca product thesis moves to consumer-demand decision
    intelligence (beauty first vertical) with the owner's measured-ToS-risk
    capture posture amendment, and the first-proof wedge moves to the beauty
    operator door, superseding turn_08 and pricing-first; subordinate
    product-lead artifacts re-targeted via the prepared consumer-demand
    revision packages (applied with recorded deviations).
  trigger: product_doctrine
  related_triggers: []
  controlling_sources_updated:
    - docs/decisions/orca_product_thesis_consumer_demand_v0.md
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
