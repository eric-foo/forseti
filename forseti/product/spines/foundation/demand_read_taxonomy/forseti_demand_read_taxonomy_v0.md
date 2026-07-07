# Forseti Demand-Read Taxonomy v0 (PROPOSED)

```yaml
retrieval_header_version: 1
artifact_role: Product artifact (PROPOSED read grammar — pending owner adjudication)
scope: >
  Fleshes out the owner's 2026-06-12 sketch of Forseti's main function: the
  signal layers, read types, wind-caller machinery, and pricing refinement
  that the scanning lane hunts for, the cleaning layer labels, and judgment
  acts on. Buy-side primary, supply-side supplement (owner word). PROPOSED:
  becomes operative read grammar only on owner adjudication; on adoption the
  thesis owes a dated pointer via the propagation contract.
use_when:
  - Specifying or reviewing the scanning lane's hunting grammar.
  - Checking what counts as a demand read, a wind caller, or an anti-trigger.
  - Adjudicating the pricing-signal refinement (complaint volume vs rerouting vs pricing events).
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_product_thesis_consumer_demand_v0.md          # controlling thesis (costly-behavior primitive, action ceilings)
  - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md         # wedge (beauty operator first door)
  - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md           # Demand-Substrate Hard Gate
  - forseti/product/satellites/beauty/beauty_venue_card_set_v0.md               # venue discovery layer; card 11 = wind-caller exemplar
  - forseti/product/spines/scanning/scan_core/forseti_demand_scan_core_spec_v0.md   # consumes this grammar for authorized scans
  - forseti/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md  # consumes this grammar for verdict/action-ceiling judgment
stale_if:
  - The owner adjudicates (adopt / amend / reject) — fold the word in as a dated amendment.
  - The thesis or wedge is amended (re-derive against the amended text).
```

## Status

`PROPOSED_PENDING_OWNER_ADJUDICATION` — fleshed 2026-06-12 by the ICP /
product-direction lane from the owner's in-thread sketch ("help me flesh this
out please — this would be the main function of orca"). Owner words anchored:
buy-side primary with *some* supply side to supplement (org motion);
influencers as wind callers of their own — "maybe the main wind callers
actually"; convergence and divergence examples (peptides trend; promoted-but-
low-engagement; Reddit-vs-TikTok-vs-IG splits); movement over availability.

Text-consistency fix (2026-06-14, owner-authorized in-thread): the
wind-caller-calibration read-type and Non-Claims lines below were reconciled to
match Signal Layer 2 and the live carve-out
(`docs/decisions/wind_caller_calibration_carveout_v0.md`), completing that
carve-out's propagation (its receipt amended Layer 2 but missed these two
lines). No policy change. The channel-vs-person boundary itself remains an
owner-confirmation item — see the adjudication-prep companion
(`forseti_demand_read_taxonomy_adjudication_v0.md`, Q3).

Demand-state model amendment (2026-06-14, owner-authorized in-thread; clarified
2026-06-23): the central axis changes from **durable vs hollow** to **two
independent axes** — **durable vs transient** (persistence horizon) and **real vs
manufactured** (integrity). "Hollow" is retired: it conflated *transient*
(strong real demand in the current window whose durability is not called, or
whose evidence supports decay) with *manufactured* (fake / amplified). Three
actionable states result — **durable** (real strong demand with a named
evidence basis for projected persistence over the decision horizon; commit,
then scale as earned), **transient** (real strong current-window demand; probe /
commit in-window, time-boxed to the decay window), **manufactured** (avoid) —
and the action ceiling is matched to the demand's lifespan. Transient gets
**equal billing** with durable as a read (owner call: spikes are still
capital-allocation decisions and occur more often than durable shifts). The
durability problem is governed by the calling sequence (new section below): open
current-window transient when no durability basis is present; call durable only
when the read names the evidence-supported persistence projection; monitor to
strengthen, revise, scale, or reduce. The recurring monitoring is
**decision-linked retainer billing**, never a feed. The layers and read types
below are restructured to this model; the controlling thesis is amended by dated
pointer (see the propagation receipt at the end).

## The Function In One Sentence

For a vertical and sub-niche, Orca reads where demand is actually going **and how
long it is supportably expected to stay strong** — sorting **durable** demand
(real strong demand with a named persistence-projection basis) from
**transient** demand (real strong current-window demand whose durability is not
called, or whose evidence supports decay) and from **manufactured** demand (fake
/ amplified) — by fusing buy-side movement with supply-side org motion under
integrity labels, identifies who calls the wind in that niche, and packages the
evidence so judgment can set the action ceiling **matched to the demand's
lifespan** (monitor, probe, commit, hold, scale, avoid, reduce).

## Signal Layers

1. **Trend vector (TrendVector)** — the object of the read: demand moving toward or away
   from an ingredient, category, format, or claim (owner example: peptides).
   A trend vector carries direction, velocity, **and expected lifespan** — the
   durable-vs-transient question is not a yes/no flag but "what horizon should
   you act on?"; it is never reported as bare momentum. A durability projection
   must cite its basis; computing the exact decay curve is a forward capability,
   likely earned from historical analogues — see the decay-timing confidence note
   in the Transient-spike read.
2. **Wind callers (WindCaller)** — the leading indicators: per vertical × sub-niche, the
   specific accounts, communities, or detectors whose early public calls (Call)
   precede the move. The owner flags influencers as possibly the main wind
   callers. The repo already holds a worked exemplar: INCIDecoder (venue card
   11, "root-receipt detector / wind-caller exemplar" — its commissioned SPF
   tests became the root receipt the entire Purito chain cites).
   **Primacy (owner-adjudicated 2026-06-14, Q2; clarified 2026-06-23):** wind
   callers are **primary at the trigger** — their early call can open the
   current-window transient read (the in-window action) — while **buy-side costly
   behavior is primary for any durable projection**. A wind-caller's standalone
   trigger-weight is **calibration-gated**: a proven precede-the-move record
   earns more weight; until that evidence exists the **conservative default
   holds** — the Demand-Substrate Hard Gate (origin de-correlation + gradeable
   costly behavior) applies even to a transient move, so a wind-caller call
   alone never fires one. *Evidence to prove (open, owner-flagged):* that
   beauty wind-callers actually precede the move reliably — what the calibration
   ledger must demonstrate before trigger-weight shifts toward wind-callers.
   **Boundary (owner-adjudicated 2026-06-14, Q3; cap redefined 2026-06-15):** named public-figure
   wind-caller calibration from public outputs is **broadly allowed and
   non-permanent** (time-bounded, never a permanent dossier); the cap applies to
   our own **operating/capture accounts (≤10, starting ≤5)** — the subject-creator
   roster is **uncapped (all-in-vertical)**; active capture = attended/human-initiated;
   passive monitoring = human-initiated, time-bounded, self-terminating runs
   (carve-out 2026-06-15 amendment) — not a blanket creator cap.
   Internal judgment/calibration use only; **person-level dossiers in any sold or
   external surface remain forbidden** and the external/product boundary is
   unchanged. Audience / follower-graph analytics stay **deferred-gated**
   (`forseti/product/spines/capture/core/operating_model/data_capture_spine_future_exploration_lanes_v0.md`).
3. **Buy-side corroboration (primary, owner word)** — costly behavior:
   sellouts, waitlists, restock pressure, review velocity and content shifts,
   pain-point convergence, dupe-seeking and switching behavior, effortful
   UGC. Attention volume never stands alone (thesis costly-behavior
   primitive).
4. **Supply-side org motion (supplement, owner word)** — operators' revealed
   bets: ad launches, hiring direction, product-pipeline and launch signals,
   retail placements. Org motion is an insider demand forecast expressed in
   spend; it corroborates or contradicts the buy-side read, it does not lead
   it.
5. **Integrity layer** — manufactured-versus-organic labels: paid-promotion
   flags, engagement anomalies, astroturf and bot marks, dupe-wave
   distortion. This layer **owns the real-vs-manufactured axis** — it answers
   "is this demand real?", independently of whether real demand is durable or
   transient. Identifying manufactured demand is decision-critical in its own
   right (owner, 2026-06-14): it is the contamination check that protects both
   real reads. Cross-venue disagreement is itself signal (surfaced by the
   divergence *technique*, below), never noise to be averaged away.
   Manufactured separation is a forward/live capability; backtests cannot
   recover historical paid-proxy spend.

## Read Types

The reads (Reading) sort into the demand-state model: two independent axes —
**durable vs transient** (what persistence horizon can the evidence support?) and
**real vs manufactured** (is there costly behavior, or is it amplified/fake?) —
yielding three actionable states. The action ceiling is matched to the demand's
lifespan: committing beyond the supported horizon strands inventory; monitoring
a durable shift leaves the compounding play on the table.

- **Durable-demand (Reading) read** (real + projected to stay strong →
  *commit / scale as earned*): effectively independent demand origins + wind
  callers + org motion pointing the same way, costly-behavior anchored, with a
  named basis for projecting persistence over the decision horizon. Owner's
  example: demand trending toward peptides, evidenced by named influencer
  wind-callers, with companies launching ads and hiring in that direction, and
  reviews / pain-points honing in on the same thing. Observed persistence is one
  support path, not the definition.
- **Transient-spike (Reading) read** (real + strong current-window demand → *probe / commit in-window*, time-boxed):
  real strong current-window costly behavior with a **short expected lifespan**
  or without enough basis to project persistence — a genuine spike that will
  normalize (a viral surge, a time-limited dupe wave, a seasonal pop). It is
  **equal billing** with the durable read (owner call, 2026-06-14): it is still a
  capital-allocation decision and these occur more often than durable shifts.
  The action is **in-window** (buy or avoid now). Anti-trap: weak,
  attention-only, or resonance-only input is not transient demand, and manufactured hype is not transient demand;
  transient demand is strong real demand whose persistence horizon is not
  supportably durable.
- **Manufactured-demand (Reading) read** (fake / amplified → *avoid*): demand
  that is not real — promotion-engagement mismatch, astroturf, coordinated/bot
  amplification, dupe-wave distortion. Acting on someone else's manufactured
  spike commits to demand that was never yours; identifying it protects both real
  reads (owner: this ability is itself decision-critical).
- **Brand-decision event (Reading) read** (the monetization unit): a specific brand (Brand)'s
  live allocation decision — launch / reposition; retail or channel entry;
  restock / sellout; discontinuation / moratorium; defend-versus-hype;
  event-triggered pricing. The demand-state read (durable / transient /
  manufactured), wind-caller state, and integrity labels are the context that
  makes it decide-grade, and they set the action ceiling (monitor / probe / commit / hold / scale / avoid / reduce), capped by signal
  integrity and decay-timing confidence.
- **Wind-caller calibration (Reading)** (the compounding asset): grade each niche's
  wind callers' public calls against outcomes (Outcome) over time — on **both** whether the
  move happened **and how long it lasted**, since a caller good at durable shifts
  and one good at spikes are different and both valuable. This is the
  outcome-memory moat applied to sources — "we know who actually calls beauty
  winds, with receipts" — and the same historical-outcome machinery is the
  likeliest path to the decay-curve capability the transient read needs.
  Calibration receipts are dated, anti-cherry-picked, and **non-permanent**
  (time-bounded); channel-level by default and — under the carve-out (Layer 2) —
  **named-public-figure broadly**, with the cap on our own operating/capture
  accounts (≤10, starting ≤5); subject-creator roster uncapped (all-in-vertical);
  active = attended; passive = bounded self-terminating runs
  (carve-out 2026-06-15 amendment).

**Divergence is a technique, not a verdict** (owner, 2026-06-14): signals
disagreeing — promotion-engagement mismatch (an influencer promotes X but ad
engagement runs below their own baseline), venue sentiment splits (TikTok
disagrees with IG), a quality attack where marketing is loudest (Reddit attacking
quality under a promo push) — is *evidence you use to classify* a candidate as
transient or manufactured. It is no longer synonymous with "hollow"; it is how
you tell real-but-fading from fake.

## Calling Sequence (2026-06-14, owner; clarified 2026-06-23)

The reads relate over time, and that sequence is the read grammar's motion:

1. **First call = current-window transient unless a durability basis is already
   in the information set.** Durable is the over-claimable label — anything can
   be *asserted* durable — so the read must name the evidence basis before it can
   call durable. Without that basis, it opens transient and **acts in-window**
   (buy: ride the spike; or avoid/reduce: a spike not worth committing to). The
   action is immediate; it does not wait on the monitor.
2. **Then monitor momentum.** Monitoring does not merely observe history; it
   builds or defeats the persistence projection. The spike either decays (exit,
   as called), consolidates into a durable read, or reveals manufactured
   contamination.
3. **Earn or revise the durable call.** When monitored evidence, repeated costly
   behavior, analogues, and corroborating org motion support the persistence
   projection, the call upgrades transient → durable (commit, scale as earned).
   Durable is the *earned* projection state — not a retrospective label and not
   an opening assertion without basis.

**Re-homed 2026-06-14** (kept here only as grammar; the commercial and
positioning consequences live where they belong): the *billing shape* (recurring
monitoring → retainer / recurring-decision packaging) is an offer concern —
offer hypothesis → Commercial Frame Status, as input to the pricing /
commercial-frame CA run; the *never-a-feed invariant* (every output is a
calibrated decision with an action ceiling, never a stream — the lock that keeps
the retainer off the "monitoring-only pull" kill and out of social listening) is
owned by the buyer-proof packet → Orca Promise; and the *judgment moat /
differentiation floor* (each monitored outcome compounds the calibration ledger)
is strategic — thesis → Strategic Center.

## Pricing Refinement (owner-ratified 2026-06-14)

- **Price-complaint volume: anti-trigger.** Chronic, omnipresent,
  non-discriminating, and it almost never resolves into an event — it cannot
  be graded, so it cannot feed the moat. Never a scan trigger.
- **Price-driven rerouting: real buy-side movement.** Dupe adoption,
  trade-down, switching with stated cause — costly behavior, gradeable, and
  in beauty the dupe culture makes this one of the most legible demand
  signals there is. This IS signal, and it is price-born.
- **Pricing decision family (DecisionEvent): retained, event-triggered only.** A price move
  that happened or is visibly imminent (batch-1's Beauty Pie 2023 repricing
  is exactly this) stays a valid decision family. Complaint chatter alone
  never triggers it.
- **Horizon (2026-06-14):** price-driven rerouting is usually a **transient**
  signal (a dupe wave surges then normalizes) but is **durable** when a price
  move drives permanent defection to a cheaper brand. The read must classify
  which; rerouting inherits the durable/transient tag and its decay-timing
  confidence like every other read. Q1's substance is unchanged.

## Pipeline Fit (owner's six-step structure, 2026-06-12)

1. **Vertical / venue discovery** — EXISTS: the beauty venue card set (12
   cards, NEWSY/SUBTLE chain) + three screens' ledgers + the vertical
   exploration guide.
2. **Scanning / candidate finding** — THE GAP this taxonomy feeds; the
   scanning lane hunts the read types above across the card venues
   (commission: `docs/prompts/product-planning/consumer_demand_scanning_lane_commission_prompt_v0.md`).
3. **Capture** — EXISTS: capture lane / Armory; per-venue route bindings stay
   capture-lane-owned; measured-ToS posture (owner ask-1 amendment).
4. **Candidate recording** — EXISTS in backward mode (candidate-pool handoff
   shape); forward mode lands in the discovery brief's slots.
5. **Cleaning / integrity processing** — DEVELOPING: dedup, entity
   normalization, brand-to-parent resolution, distortion labels,
   attention-versus-costly separation.
6. **Evidence packaging for judgment** — DEVELOPING: memo / evidence-appendix
   substrate; judgment sets the action ceiling.

## Non-Claims

PROPOSED only — no validation, readiness, buyer proof, or judgment-quality
claim; closeout state for any such claim: `no_durable_evidence`. Mints no
evidence-ladder vocabulary and redefines no overlay-owned semantics. Does not
amend the thesis (on adoption, the thesis gains a dated pointer through the
propagation contract). Wind-caller tracking is channel-level public-output plus
**non-permanent** named-public-figure calibration under the carve-out (the cap
applies to our own operating/capture accounts — ≤10, starting ≤5; subject-creator
roster uncapped, all-in-vertical; active = attended; passive = bounded
self-terminating runs; carve-out 2026-06-15 amendment); person-level dossiers in any sold or external
surface remain forbidden and the external/product boundary is unchanged. Authorizes no scan, capture,
monitoring, or outreach.

The demand-state model (durable / transient / manufactured) is PROPOSED and
amends the controlling thesis only by dated pointer on adoption. The decay-curve
capability and decay-timing calibration do not yet exist — transient-spike reads
are built-to, not proven-at — so no transient-timing claim is validated here.
This artifact is the read **grammar**; defining the ontology and proving reads
decision-grade is a separate, separately-commissioned pass — the taxonomy asserts
no ontology or decision-grade claim.

```yaml
direction_change_propagation:
  note: >
    This file is a downstream surface of the carve-out 2026-06-15
    cap-redefinition propagation. Three sites updated (Layer-2 wind-caller
    boundary, Read-Types calibration, Non-Claims): the cap is redefined to our
    own operating/capture accounts (≤10, starting ≤5); subject-creator roster
    uncapped (all-in-vertical); active = attended; passive = bounded
    self-terminating runs. The "person-level dossiers in any sold or external
    surface remain forbidden and the external/product boundary is unchanged"
    clause (Non-Claims site) is preserved verbatim and unchanged.
  authority: docs/decisions/wind_caller_calibration_carveout_v0.md (2026-06-15 amendment)
  date: 2026-06-15
```
