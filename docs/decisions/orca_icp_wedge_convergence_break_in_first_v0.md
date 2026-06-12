# Orca ICP Wedge Convergence — Break-In-First Direction Lock v0

```yaml
retrieval_header_version: 1
artifact_role: Decision record
scope: Owner-locked convergence of the ICP redo. The first-proof wedge flips to break-in / competitor-customer intelligence, with pricing-outside-in as the expansion application, on one outside-in competitive/market intelligence engine. Carries the doctrine-change propagation blocker and the downstream document-update proposal.
use_when:
  - Checking the current first-proof wedge direction after the ICP redo.
  - Executing the downstream product-doc cascade in the product lane.
  - Preparing commercial-frame or discovery inputs for the first proof.
authority_boundary: retrieval_only
supersedes:
  - docs/product/orca_product_lead_first_icp_wedge_decision_v0.md
open_next:
  - docs/research/orca_icp_redo_evidence_targets_v0.md
  - docs/product/product_lead/orca_offer_hypothesis_v0.md
  - docs/product/product_lead/orca_product_lead_first_icp_wedge_decision_v0.md
stale_if:
  - Owner accepts a different first-proof wedge.
  - The downstream product-doc cascade lands and this record's proposal is consumed.
```

## Status

**SUPERSEDED 2026-06-08 → `docs/decisions/orca_icp_wedge_pricing_first_v0.md`** —
UN-FLIPPED to pricing-first after two de-correlated verification runs (Opus
parallel + owner external o3) disconfirmed the break-in flip. The break-in
direction in this record is HISTORICAL; break-in is retained only as a
clean-substrate test + retainer horizon. Read the pricing-first record for the
current direction.

`OWNER_LOCKED_DIRECTION` (historical) — deliberate-then-freeze; owner sign-off
received 2026-06-08.

This locks a DIRECTION, not a result. It is not buyer validation,
willingness-to-pay, readiness, buyer pull, or proof the wedge will win.
Supporting evidence is market-context, partly vendor-published and discounted
(see the ledger).

## Decision

First-proof wedge (locked):

- Engine (core): outside-in competitive & market intelligence — the reusable
  spine that feeds every application. Competitive intelligence IS this engine,
  not a separately sold decision.
- First application — the land: break-in / competitor-customer / win-loss
  intelligence — the decision to win customers from competitors or break into a
  market by understanding why prospects choose competitors and what would move
  them, served from public outside-in signal as a decision artifact.
- Expansion application: pricing — outside-in slice (competitor-/AI-/
  backlash-triggered), reached from the same engine and relationship once trust
  exists. Pricing is retained as the expansion, not the first proof.
- Buyer (situational, NOT a segment): any company — incumbent or challenger — at
  a moment where the decisive input lives outside its walls (new product line,
  new market, first-time AI monetization, newly surfaced competitor).
  "Challenger / entrant" posture is a winnability amplifier for the first yeses,
  not a hard filter.
- Differentiation lane: the public-signal decision artifact — not a monitoring
  dashboard, not interview-based win/loss.

Supersedes the v0 wedge (post-revenue dev-facing SaaS pricing/packaging,
`KEEP_CURRENT_PROOF_LANE`).

## Why (compressed; full evidence in the ledger)

- Decisive axis = in-house vs bought. Pricing is decided in-house (~6% hire
  outside help); break-in / win-loss has a PROVEN outside-buy market (~36%
  third-party and rising; an established provider category; ~$15-50k/yr programs;
  recurring subscriptions → retainer-aligned). On the locked dial-1
  (newcomer-winnability primary), an existing buying habit + budget line is the
  bigger first-yes asset than density alone.
- Land-and-expand on one engine: engine → break-in (low activation energy,
  proven demand) → pricing + positioning + roadmap (higher value, needs trust).
  Win/loss already feeds pricing decisions, so the bridge is natural.
- The de-correlated evidence pass corrected a wrong unverified lead (the
  "orphaned pricing — nobody owns it" hypothesis was NOT corroborated; pricing is
  owned by senior named roles), which is part of why pricing-first is the harder
  cold sale.
- Caveats held: break-in's adoption/ROI figures are vendor-published (discount);
  the existing market is interview-based while Orca's method is public-signal (a
  different production mode); incumbents are funded (AlphaSense, Klue, Crayon,
  Clozd); still market-context, not validation.

## Poke results + amendment (2026-06-08)

Four de-correlated Opus challenges were run against this lock (pricing-first
steelman; incumbent-winnability; alternative-wedge; entry-model). The DIRECTION
survives — none recommended a flip — but the lock's confidence and framing are
amended:

- Confidence (LOWERED): break-in was selected on thinner, more vendor-contaminated
  evidence than the runner-up (pricing had two depth passes; break-in's Core B is
  largely Clozd-published and was funnel-skipped). The decisive in-house-vs-bought
  axis is asymmetrically sourced — the "~36%" is vendor (Clozd); the "~6%" pricing
  figure is NOT in the verified external DR (which logged that rate as a gap it
  could not find). Treat the axis as PROVISIONAL and the lock as
  reversible-pending the verification below — not settled. (Note: the structural
  claim that break-in is a recognized BOUGHT category — Gartner lists 14 win/loss
  + 31 CMI providers — has independent, non-vendor support; the soft part is the
  precise buy-rates.)
- Servability caveat: break-in's public-signal servability (the HARD gate) is
  asserted-by-analogy from the pricing pass, never depth-tested. Broad "win/loss"
  leans on a largely PRIVATE/interview input; the narrow framing below is where
  public servability is plausibly strong — untested either way.
- Framing (NARROWED): the winnable form is NOT "we do win/loss." Two challengers
  converged on the same corner — re-scope the first proof to
  COMPETITOR-DISPLACEMENT / MARKET-ENTRY intelligence for a challenger with NO
  existing pipeline to interview (so funded incumbents and interview-based win/loss
  are structurally absent), bounded to a concrete artifact, positioned as a
  COMPLEMENT / pre-interview front-end — not an interview substitute. This folds
  back the category/market-entry contender the funnel had wrongly collapsed into
  "launch/GTM timing."
- Open tension (do NOT resolve yet): narrowing to market-entry likely STRENGTHENS
  the first yes but WEAKENS density/retainer (market-entry is episodic per buyer).
  The retainer end-game may need a different cadence carrier — a serial/portfolio
  buyer class, positioning, or the pricing-expansion. Flagged for verification + a
  later decision.
- Pre-proof gates (ADDED): before any paid break-in proof — (1) run ONE
  break-in/market-entry method backtest (CONFIRMED 2026-06-08: the
  method-validation portfolio is decision-DIVERSE — pricing + competitive-
  narrative + AI-disruption + M&A + fiscal + commercial-partnership +
  corporate-restructuring, NOT pricing-only — and already includes
  competitive-displacement cases MV-01 Intercom→Zendesk and MV-03 Stack
  Overflow→ChatGPT that are break-in-adjacent; the real gap is no EXACT
  market-entry artifact yet, so ADD one to the existing validation portfolio) and
  (2) write a bounded break-in artifact spec (none exists). Note: an owner-level
  "no buyer contact before full-spine MVP" gate (advisory_proof_slice_definition_v0.md)
  is upstream of any paid proof — the wedge orients the MVP, it does not gate an
  imminent sale.
- Logged omissions: commercial / market-side DILIGENCE intelligence (absent from
  the corpus; best retainer / worst first-yes — horizon, not first wedge) and
  POSITIONING/messaging as a candidate retainer anchor (more continuous than
  pricing).
- Gate to hardening: the targeted verification prompt
  `docs/prompts/product-planning/orca_break_in_verification_evidence_prompt_v0.md`
  must close the decisive-axis and the public-signal-substitution/servability
  questions BEFORE the downstream product-doc cascade runs.

These amend the lock's confidence and framing; the direction (break-in-first,
pricing-expansion) is unchanged. Still not validation/WTP/buyer-proof.

## Doctrine-change propagation

This is a `product_doctrine` change. The downstream product corpus still routes
by the v0 pricing-first wedge, so propagation is INCOMPLETE — recorded as a
blocker, not a completion claim, per
`.agents/workflow-overlay/source-of-truth.md`:

```yaml
direction_change_propagation_blocker:
  doctrine_changed: >
    First-proof wedge flips from dev-facing SaaS pricing/packaging (v0) to
    break-in / competitor-customer intelligence first, with pricing-outside-in as
    the expansion application, on one outside-in competitive/market intelligence
    engine.
  trigger: product_doctrine
  related_triggers: []
  blocking_surface: >
    Downstream product-doctrine sources still carry the v0 pricing-first wedge:
    docs/product/orca_offer_hypothesis_v0.md,
    docs/product/orca_product_lead_first_icp_wedge_decision_v0.md,
    docs/product/orca_buyer_proof_packet_v0.md,
    docs/product/orca_product_proof_lead_charter_v0.md. Their durable home is the
    product lane on main; they are untracked on the ECR branch.
  attempted_check: >
    Read the product corpus and overlay (source-of-truth, artifact-roles,
    artifact-folders); locked the direction in this decision record and pointed
    the research ledger to it; identified the full downstream cascade (below). Did
    NOT edit the downstream product docs from this lane/branch without
    owner-authorized product-lane execution.
  allowed_next_step: >
    Owner-authorized product-lane patch cascade (preferably on main), in order:
    (1) ICP wedge v1, (2) offer hypothesis v1, (3) buyer-proof packet + proof-lead
    charter patches, (4) candidate skill refresh — each carrying its own
    direction_change_propagation receipt.
  non_claims:
    - not validation
    - not readiness
    - not willingness-to-pay
    - not buyer proof
    - not ICP proven
```

## Document-update proposal (the cascade)

| Document | Proposed change | Priority | Authority / branch |
| --- | --- | --- | --- |
| `docs/product/orca_product_lead_first_icp_wedge_decision_v0.md` → v1 | Flip selected wedge to break-in-first / pricing-expansion; engine + situational buyer; `supersedes` v0; refresh `input_hashes`; carry DCP receipt | P0 (controlling source) | Product lane, main — do not fork on ECR |
| `docs/product/orca_offer_hypothesis_v0.md` → v1 | First-proof offer layer flips from dev-facing pricing to break-in / competitor-customer intelligence; pricing → expansion; keep the broad offer boundary; revise buyer/decision-family/qualifying-conditions/pull-signals; carry DCP receipt | P0 | Product lane, main |
| `docs/product/orca_buyer_proof_packet_v0.md` | Patch first-proof wedge, pull signals, and disqualifiers to break-in | P1 | Product lane, main |
| `docs/product/orca_product_proof_lead_charter_v0.md` | Patch the first-proof lane to break-in | P1 | Product lane, main |
| `.agents/skills/orca-product-lead/SKILL.md` (candidate) | Refresh references/examples to the new wedge IF the candidate is accepted; do NOT clobber `skill-adoption.md` (another lane modifies it) | P2 (candidate, unaccepted) | This lane |
| `docs/decisions/turn_08_product_thesis_v0.md` | No change — break-in sits within the thesis's positioning/competitive/growth families; recorded as consistent | none | Read-only |
| `docs/research/orca_icp_redo_evidence_targets_v0.md` | Point to this decision record as the selection home | done this turn | This lane |

Downstream routing surfaces checked, no change needed: `product-proof.md` (owns
buyer-proof semantics, not the specific wedge); `source-loading.md` /
`orca_repo_map_v0.md` (the wedge is not a routing surface); `AGENTS.md` /
`CLAUDE.md` (carry no product-wedge content).

## Non-claims

Not validation, willingness-to-pay, paid-pilot conversion, repeatability, ROI,
product/feature/implementation/commercial readiness, buyer proof, target-company
qualification, outreach authorization, or proof the wedge will win. This record
locks an owner-chosen direction and proposes its propagation; it does not
authorize implementation, runtime work, or commits.
