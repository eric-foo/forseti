# Orca Demand-Read Taxonomy v0 (PROPOSED)

```yaml
retrieval_header_version: 1
artifact_role: Product artifact (PROPOSED read grammar — pending owner adjudication)
scope: >
  Fleshes out the owner's 2026-06-12 sketch of Orca's main function: the
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
  - docs/decisions/orca_product_thesis_consumer_demand_v0.md          # controlling thesis (costly-behavior primitive, action ceilings)
  - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md         # wedge (beauty operator first door)
  - docs/product/product_lead/orca_buyer_proof_packet_v0.md           # Demand-Substrate Hard Gate
  - docs/product/core_spine/beauty_venue_card_set_v0.md               # venue discovery layer; card 11 = wind-caller exemplar
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
(`orca_demand_read_taxonomy_adjudication_v0.md`, Q3).

Demand-state model amendment (2026-06-14, owner-authorized in-thread): the
central axis changes from **durable vs hollow** to **two independent axes** —
**durable vs transient** (persistence) and **real vs manufactured** (integrity).
"Hollow" is retired: it conflated *transient* (real demand that decays — still
valuable short-term) with *manufactured* (fake / amplified). Three actionable
states result — **durable** (commit, long horizon), **transient** (move, short
horizon, time-boxed to the decay window), **manufactured** (discount / avoid) —
and the action ceiling is matched to the demand's lifespan. Transient gets
**equal billing** with durable as a read (owner call: spikes are still
capital-allocation decisions and occur more often than durable shifts), but
carries an explicit **decay-timing confidence** that is currently low and caps
its ceiling until a decay-curve capability exists (lane guardrail on the owner's
equal-billing call). The layers and read types below are restructured to this
model; the controlling thesis is amended by dated pointer (see the propagation
receipt at the end).

## The Function In One Sentence

For a vertical and sub-niche, Orca reads where demand is actually going **and how
long it will last** — sorting **durable** demand (persists past its trigger) from
**transient** demand (real, but decays) and from **manufactured** demand (fake /
amplified) — by fusing buy-side movement with supply-side org motion under
integrity labels, identifies who calls the wind in that niche, and packages the
evidence so judgment can set the action ceiling **matched to the demand's
lifespan** (act, phase, narrow, hold, defend; long-horizon *commit* vs
short-horizon *move*).

## Signal Layers

1. **Trend vector** — the object of the read: demand moving toward or away
   from an ingredient, category, format, or claim (owner example: peptides).
   A trend vector carries direction, velocity, **and expected lifespan** — the
   durable-vs-transient question is not a yes/no flag but "what horizon should
   you act on?"; it is never reported as bare momentum. (Computing the decay
   curve is a forward capability, likely earned from historical analogues — see
   the decay-timing confidence note in the Transient-spike read.)
2. **Wind callers** — the leading indicators: per vertical × sub-niche, the
   specific accounts, communities, or detectors whose early public calls
   precede the move. The owner flags influencers as possibly the main wind
   callers. The repo already holds a worked exemplar: INCIDecoder (venue card
   11, "root-receipt detector / wind-caller exemplar" — its commissioned SPF
   tests became the root receipt the entire Purito chain cites). Boundary:
   wind callers are **channels AND named public-figure wind-callers under the
   bounded internal carve-out** (`docs/decisions/wind_caller_calibration_carveout_v0.md`):
   public handle + public name + public calls + public stats + call-vs-outcome
   calibration, ≤5 accounts, human pace, pre-commercial, internal only.
   Audience/follower-graph analytics: **deferred-gated** (separate authorization +
   legal gate required; reclassified from out-of-scope to sanctioned-but-deferred
   in `docs/product/data_capture_spine/data_capture_spine_future_exploration_lanes_v0.md`).
   Person-level dossiers in any sold or external surface remain **forbidden**
   (charter exclusion, unchanged).
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

The reads sort into the demand-state model: two independent axes — **durable vs
transient** (does it persist past its trigger?) and **real vs manufactured** (is
there costly behavior, or is it amplified/fake?) — yielding three actionable
states. The action ceiling is matched to the demand's lifespan: commit on a
spike strands inventory; "move" on a durable shift leaves the compounding play
on the table.

- **Durable-demand read** (real + persists → *commit*, long horizon): independent
  venue families + wind callers + org motion pointing the same way,
  costly-behavior anchored, and **persisting past the trigger**. Owner's example:
  demand trending toward peptides, evidenced by named influencer wind-callers,
  with companies launching ads and hiring in that direction, and reviews /
  pain-points honing in on the same thing. The trust anchor — the one persistence
  backtests can support.
- **Transient-spike read** (real + decays → *move*, short horizon, time-boxed):
  real costly behavior with a **short expected lifespan** — a genuine spike that
  will normalize (a viral surge, a time-limited dupe wave, a seasonal pop). It is
  **equal billing** with the durable read (owner call, 2026-06-14): it is still a
  capital-allocation decision and these occur more often than durable shifts.
  **But** its ceiling is capped by **decay-timing confidence**, currently low:
  calling a spike is two claims — *it's real* AND *it decays in ~N weeks* — and
  the decay-curve capability does not yet exist, so the read stays claim-honest
  (built-to, not proven-at) until it does. Anti-trap: a transient spike can look
  identical to durable convergence in the moment; only the lifespan assessment
  separates them.
- **Manufactured-demand read** (fake / amplified → *discount / avoid*): demand
  that is not real — promotion-engagement mismatch, astroturf, coordinated/bot
  amplification, dupe-wave distortion. Acting on someone else's manufactured
  spike commits to demand that was never yours; identifying it protects both real
  reads (owner: this ability is itself decision-critical).
- **Brand-decision event read** (the monetization unit): a specific brand's
  live allocation decision — launch / reposition; retail or channel entry;
  restock / sellout; discontinuation / moratorium; defend-versus-hype;
  event-triggered pricing. The demand-state read (durable / transient /
  manufactured), wind-caller state, and integrity labels are the context that
  makes it decide-grade, and they set the action ceiling **and its horizon**
  (long-horizon commit vs short-horizon move) — never stronger than signal
  integrity and decay-timing confidence support.
- **Wind-caller calibration** (the compounding asset): grade each niche's
  wind callers' public calls against outcomes over time — on **both** whether the
  move happened **and how long it lasted**, since a caller good at durable shifts
  and one good at spikes are different and both valuable. This is the
  outcome-memory moat applied to sources — "we know who actually calls beauty
  winds, with receipts" — and the same historical-outcome machinery is the
  likeliest path to the decay-curve capability the transient read needs.
  Calibration receipts are dated and anti-cherry-picked like every other ledger;
  channel-level by default and — under the bounded internal carve-out (Layer 2;
  `docs/decisions/wind_caller_calibration_carveout_v0.md`) — named-public-figure
  for the ≤5 internal-only calibration subjects.

**Divergence is a technique, not a verdict** (owner, 2026-06-14): signals
disagreeing — promotion-engagement mismatch (an influencer promotes X but ad
engagement runs below their own baseline), venue sentiment splits (TikTok
disagrees with IG), a quality attack where marketing is loudest (Reddit attacking
quality under a promo push) — is *evidence you use to classify* a candidate as
transient or manufactured. It is no longer synonymous with "hollow"; it is how
you tell real-but-fading from fake.

## Pricing Refinement (PROPOSED final take on the owner's question)

- **Price-complaint volume: anti-trigger.** Chronic, omnipresent,
  non-discriminating, and it almost never resolves into an event — it cannot
  be graded, so it cannot feed the moat. Never a scan trigger.
- **Price-driven rerouting: real buy-side movement.** Dupe adoption,
  trade-down, switching with stated cause — costly behavior, gradeable, and
  in beauty the dupe culture makes this one of the most legible demand
  signals there is. This IS signal, and it is price-born.
- **Pricing decision family: retained, event-triggered only.** A price move
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
propagation contract). Wind-caller tracking is channel-level public-output by
default, extended to named-public-figure calibration only under the bounded
internal carve-out (≤5 accounts, internal-only); person-level dossiers in any
sold or external surface remain forbidden. Authorizes no scan, capture,
monitoring, or outreach.

The demand-state model (durable / transient / manufactured) is PROPOSED and
amends the controlling thesis only by dated pointer on adoption. The decay-curve
capability and decay-timing calibration do not yet exist — transient-spike reads
are built-to, not proven-at — so no transient-timing claim is validated here.
