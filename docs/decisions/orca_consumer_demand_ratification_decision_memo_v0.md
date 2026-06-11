# Owner Decision Memo — Consumer-Demand Thesis Asks 1-4 (PROPOSED)

```yaml
retrieval_header_version: 1
artifact_role: Decision record (owner decision outcomes for thesis asks 1-4, 2026-06-12; lane recommendation retained as history)
scope: >
  The ICP / product-direction lane's recommendation on the consumer-demand
  thesis's four owner sign-off asks, with the cheapest-test framing and the
  exact consequence boundary of each ask. The owner's word decides; this memo
  only prepares it.
use_when:
  - The owner sits down to decide thesis asks 1-4.
  - Checking what each ask does and does not authorize before signing.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_product_thesis_consumer_demand_v0.md       # ask 1 target
  - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md      # ask 2 target
  - docs/product/product_lead/orca_icp_ratification_readiness_report_v0.md   # the consistency sweep behind this memo
  - docs/product/product_lead/orca_ratification_day_runbook_v0.md  # what executes after the word
input_hashes:
  docs/decisions/orca_product_thesis_consumer_demand_v0.md: 5FEA48AE8B0C0E22D24CE2194F1F17617C5C94D2C75A204AAD5CD8CC149B2B0E
  docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md: C878ABEBBFFC119A032E0290E093A9EBB973BC15052B4B21FA59D285AB83C07B
branch_or_commit: ecr-sp3-timing-deriver-slice1 @ 48c00ca
stale_if:
  - The owner amends any recorded decision (dated amendment to the Owner Decision Record; no silent rewrites).
```

## Status

`DECIDED_2026-06-12` — the owner decided all four asks in-thread 2026-06-12;
the Owner Decision Record below is the recorded outcome and governs. The
recommendation sections below it are retained as history (prepared
2026-06-11 as `PROPOSED_LANE_RECOMMENDATION`). Every claim in this memo is
capped at `product_learning` tier or below per the evidence ladder; closeout
state for any proof-shaped reading: `no_durable_evidence`.

## Owner Decision Record (2026-06-12, verbatim words and effects)

- **Ask 1 — thesis: ratified AS AMENDED.** Owner words: "no for 1 - it does
  not depend on no live ToS violating source. we accept the risks for ToS
  just not at an absurd level (e.g. Brightdata)". Recorded effect: the
  thesis is ratified with its Product Boundary capture bullet amended to the
  measured-ToS-risk posture — measured platform-terms risk accepted;
  absurd-level approaches (the owner's example: Bright-Data-style industrial
  scraping) rejected; the "does not depend on any live ToS-violating source"
  premise retired. Per-venue route bindings remain capture-lane-owned and are
  revisited there under this posture (TikTok live: ratified GO the same day —
  see the addendum below). Thesis status: `OWNER_LOCKED` (dated
  amendment in the thesis record). Interpretation note: "no for 1" is read
  as rejecting the named premise, not the thesis — asks 2-4 presuppose the
  direction; if this misreads the intent, the correction is a dated
  amendment + status revert, and the cascade reverses by banner removal.
- **Ask 2 — wedge: co-ratified.** Owner words: "co-ratify ok". Effect: the
  consumer-demand wedge record is `OWNER_LOCKED_DIRECTION`; pricing-first is
  superseded as first proof (retained as engine application + method
  anchors; its re-entry candidacy was withdrawn by the same-day addendum
  below).
- **Ask 3 — probe gate: authorized.** Owner words: "yes thats okay" (to the
  recommendation as framed: Stage-1 feasibility now; Stage 2 held until
  Stage 1 reports). Effect: the durability probe's Stage-1 feasibility gate
  is owner-authorized; execution belongs to the `consumer-demand-probe`
  lane, which must consume this record and run under its own spec-v2 gates
  and authorization record. No execution happened in this lane.
- **Ask 4 — outreach gate: stays closed.** Owner words: "yes close for now".
  Effect: the no-buyer-contact-before-full-spine-MVP gate is unchanged and
  closed; no opening condition named; it re-opens only by the owner's
  explicit word.

Cascade executed 2026-06-12 per
`docs/product/product_lead/orca_ratification_day_runbook_v0.md`; the
executed `direction_change_propagation` receipt lives in
`docs/decisions/orca_product_thesis_consumer_demand_v0.md`.

## Owner Decision Record — Addendum (2026-06-12, post-cascade corrections)

Two further owner words landed after the cascade ran; both applied as dated
amendments the same day:

- **TikTok live capture: GO.** Owner words: "oh tiktok live was ratified to
  be a GO - change it." Effect: the thesis no longer lists TikTok live as a
  NO-GO example (Product Boundary bullet + evidence-table TikTok row carry
  the dated correction). Verification note (recorded, not silent): no record
  on this branch shows the prior GO ratification — the capture recon index
  still calls TikTok/IG recon speculative and the probe-lane status quoted
  at thesis prep was live-NO-GO — so the GO is recorded here on the owner's
  current word, and the owning capture-lane records (probe lane,
  recon index) owe their own dated alignment in their lanes. Consistent
  with the ask-1 measured-ToS-risk posture. The owner re-confirmed the GO
  after this flag was raised ("2 - go", 2026-06-12).
- **Pricing-first re-entry candidacy: withdrawn.** Owner words: "do NOT do
  poricing - first actually. that's too... we cant call any wind for that.
  we need to hit the harder ones / profitable ones". Effect: pricing-first
  is no longer the default re-entry candidate on a beauty-wedge kill — the
  wedge offers too weak a wind-calling demonstration. It stays only as
  historical method anchors (two RETRO SaaS cases) and a shelved engine
  application. On kill, re-entry re-forms toward the harder /
  more-profitable end of the buyer ladder (fund screen, PE/family-office
  diligence path), decided by the owner at kill time. Amended in the wedge
  record, the buyer-proof packet, and the pricing-first banner.
- **Geography: US-first baked into the thesis.** Owner words: "got it. bake
  that into thesis" (accepting the lane's US-first recommendation;
  consistent with the same-day US-default direction already recorded in the
  discovery lane's candidate-pool handoff: "US brands/ecosystem default;
  consuming batch routes inclusion to the owner or defers the row"). Effect:
  the thesis carries a Vertical And Geography Doctrine bullet (US-market
  first proof; EU/UK a later widening decision; substrate-not-passport
  exception gate), and the wedge first door, buyer-proof packet segment,
  charter segment, offer-hypothesis wedge statement, and the live discovery
  brief carry the US-market qualifier.

## Readiness In One Line

The consistency sweep found **nothing that blocks asks 1-2**: no subordinate
artifact or lane record contradicts the thesis center or the wedge ordering;
the one stale line inside the thesis (claim-defense doctrine described as
pending; it was signed 2026-06-11) is folded into the ratification edit, and
the cascade is a prepared one-pass runbook. You can decide all four asks in
one sitting.

## Ask 1 — Ratify the thesis (consumer-demand decision intelligence, beauty first)

**Recommendation: ratify.**

Grounds (all product-learning tier or below, statuses verbatim from the
records):

- The four-lane exploration sweep found no lane that contradicts the center;
  the binding constraints found (claim-tier discipline; capture-entitlement
  walls) are encoded inside the thesis, not hidden.
- The proof engine has already materially committed to this substrate: batch
  1 is owner-signed and active with 4 of 6 cases beauty consumer-demand.
  Doctrine should either follow the engine or consciously re-aim it — the
  thesis follows it.
- The thesis depends on no live ToS-violating source, names its falsifiers
  (probe Stage-2 fail; batch-1 confirm-only; substrate walls generalizing),
  and carries its own prepared supersession of turn_08.
- The alternative (keep turn_08's sector-agnostic framing, treat
  consumer-demand as first application only) is the thesis's own named
  amendment option — viable, but it leaves the product's subject undeclared
  while every running proof asset is already vertical-specific.

What ratifying does NOT do: no validation, no buyer proof, no
willingness-to-pay, no build authorization (entity spine, live sources,
probes, capture expansion, dashboards, outreach all stay separately gated;
JSG-01 stays frozen).

## Ask 2 — Co-ratify the wedge (beauty operator first door)

**Recommendation: co-ratify ordering B — operator first, fund screen second,
PE/family-office destination, pricing-first superseded-with-re-entry.**

Grounds:

- Reachability is the binding constraint under your no-warm-leads constraint,
  and the only door-opening asset being produced is the beauty backtest
  portfolio — the operator door is the door that asset opens.
- The lead-with-demand assessment stands on capture-maturity evidence (demand
  venues probe-verified; org-motion's verified strength is the archived
  corroboration layer), and its honest tension (reviews bias/pollution) is
  priced in via the fusion-with-flags substrate gate rather than argued away.
- The pivot condition is pre-named and binding: if batch-1 distillation shows
  demand reads confirm-only or persistently out-of-band, the first wedge
  re-forms around the lower-bar screen (fund-first) and operator-first is
  void. You are not betting the ordering blind; the running batch tests it.
- Pricing-first is not discarded: retained as engine application, method
  anchors (two RETRO SaaS cases), and the default re-entry candidate.

What co-ratifying does NOT do: no outreach (gate untouched), no discovery
candidate scanning (needs its own authorized lane), no org-motion or
entity-spine build, no commercial frame.

## Ask 3 — Authorize the durability probe's next gate

**Recommendation: authorize Stage 1 (feasibility) now; hold Stage 2 (blind
pair execution) until Stage 1 reports.** This is the cheapest-test framing:
the probe is the cheapest direct test of the thesis's central read
(durable-vs-hollow discrimination against momentum and category-prior
baselines), its spec is already KEEP-CLEARED through review and a bounded
recheck, and its Stage-2 gate is one of the thesis's own named falsifiers —
authorizing it buys falsification pressure on the exact claim you are
ratifying, before any buyer-facing consequence exists.

Boundary: this memo cannot and does not authorize execution. The owner's
word plus the probe lane's own authorization record (on
`consumer-demand-probe`, under spec v2's gates) is the executing authority;
keep-cleared review state is not execution authority.

## Ask 4 — Outreach gate posture

**Recommendation: keep the gate closed (default), and name the candidate
opening condition now so it is a decision rather than a drift:** e.g., "after
batch-1 distillation lands decide-grade-or-better AND at least N zero-spoiler
receipts are published under Row-1 wording" (owner sets N). Ratifying asks
1-3 does not open outreach; publishing backtest receipts is door-opening
content at `product_learning` tier, not buyer contact. If you prefer not to
name a condition, the gate simply stays closed and re-opens only by your
explicit word — also fine; the recommendation is only that the condition be
named once, deliberately.

## After Your Word

The ratifying turn runs
`docs/product/product_lead/orca_ratification_day_runbook_v0.md` (one pass:
status flips, turn_08 and pricing-first banners, subordinate revision
adoption, overlay/repo-map re-points, DCP receipt `trigger:
product_doctrine`). Two items are queued rather than inline: the
orca-product-lead skill copies (authorized skill-edit lane) and the
customer-discovery prompt realignment (prompt-orchestration lane).

## Non-Claims

A recommendation, not a decision; nothing here is validation, buyer proof,
willingness-to-pay, judgment-quality evidence, readiness, or proof the
direction will win. Probe results and batch-1 outcomes are not prejudged —
both falsifier paths (re-scope to screen-tier reads; fund-first re-form) are
live and named. This memo mints no vocabulary, amends no record, and
authorizes no execution, outreach, build, commit, or push.
