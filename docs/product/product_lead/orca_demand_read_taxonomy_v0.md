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

## The Function In One Sentence

For a vertical and sub-niche, Orca reads where demand is actually going —
durable versus hollow — by fusing buy-side movement with supply-side org
motion under integrity labels, identifies who calls the wind in that niche,
and packages the evidence so judgment can set the action ceiling (act, phase,
narrow, hold, defend).

## Signal Layers

1. **Trend vector** — the object of the read: demand moving toward or away
   from an ingredient, category, format, or claim (owner example: peptides).
   A trend vector carries direction, velocity, and the durability question;
   it is never reported as bare momentum.
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
   distortion. Cross-venue disagreement is itself signal (a divergence read),
   never noise to be averaged away.

## Read Types

- **Convergence read** (durable-demand candidate): independent venue families
  + wind callers + org motion pointing the same way. Owner's example: demand
  trending toward peptides, evidenced by named influencer wind-callers, with
  companies launching ads and hiring in that direction, and reviews /
  pain-points honing in on the same thing.
- **Divergence read** (hollow / manufactured-demand candidate):
  promotion-engagement mismatch (influencers actively promote X but their ad
  engagement runs below their own baseline); venue sentiment splits (TikTok
  does not agree with IG); a quality attack running where marketing is
  loudest (Reddit attacking product quality under a promo push).
- **Brand-decision event read** (the monetization unit): a specific brand's
  live allocation decision — launch / reposition; retail or channel entry;
  restock / sellout; discontinuation / moratorium; defend-versus-hype;
  event-triggered pricing. Trend vectors, wind-caller state, and integrity
  labels are the context that makes this read decide-grade.
- **Wind-caller calibration** (the compounding asset): grade each niche's
  wind callers' public calls against outcomes over time. This is the
  outcome-memory moat applied to sources — "we know who actually calls
  beauty winds, with receipts." Calibration receipts are dated and
  anti-cherry-picked like every other ledger; channel-level by default and —
  under the bounded internal carve-out (Layer 2;
  `docs/decisions/wind_caller_calibration_carveout_v0.md`) — named-public-figure
  for the ≤5 internal-only calibration subjects.

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
