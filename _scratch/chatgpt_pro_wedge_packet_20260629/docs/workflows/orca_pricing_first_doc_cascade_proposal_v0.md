# Orca Pricing-First — Findings Consolidation + Doc-Cascade Proposal v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Consolidates this session's agreed findings (ICP redo -> pricing-first) and proposes the smallest-complete document-change cascade to propagate the direction, per the Orca direction_change_propagation contract. Non-authoritative PROPOSAL for owner agreement; the cascade executes later in the product lane.
use_when:
  - Reviewing/agreeing the pricing-first doc cascade before it runs.
  - Executing the cascade in the product lane.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_icp_wedge_pricing_first_v0.md
  - docs/research/orca_icp_redo_evidence_targets_v0.md
  - docs/research/orca_wedge_alternatives_register_v0.md
stale_if:
  - Owner agrees and the cascade runs (then this proposal is consumed).
  - The first-proof direction changes.
```

## Status

Non-authoritative PROPOSAL for owner agreement. Consolidates the session's agreed
findings and proposes the doc-change cascade. Not a freeze, not validation, not
WTP, not readiness. Authoritative direction:
`docs/decisions/orca_icp_wedge_pricing_first_v0.md`.

## Part 1 — Consolidated findings (session + owner agreed)

1. **Engine / core (the spine): outside-in competitive & market intelligence.**
   Competition is the spine; the applications (pricing, positioning, break-in,
   etc.) are satellites on it.
2. **First-proof wedge: PRICING, outside-in slice** — competitor-/
   AI-monetization-/backlash-triggered repricing & repackaging, framed as a
   decision INPUT (NOT a monitoring feed, NOT a private-margin elasticity number).
   AI-monetization = sharpest live instance. Wedge frame is cross-sector-open;
   first-proof BEACHHEAD = the AI-monetization slice (re-derived from the
   findings; see Part 4) — NOT the inherited dev-facing-SaaS default.
3. **The decisive refinement — a servability HARD GATE.** Orca's differentiated
   read must sit on a CLEAN, decision-moving public substrate, not merely
   available signal. Pricing's competitor-PRICE substrate (pricing pages,
   changelogs, filings, earnings) is clean, FTC-exempt, and causally used (44%,
   Hinterhuber-Liozu, peer-reviewed INDEPENDENT). The competitor-CUSTOMER read
   (break-in) has only a REVIEW substrate — biased (J-curve self-selection) +
   polluted (FTC 16 CFR 465) + interview-gated. The gate applies to specific
   DECISIONS, not families.
4. **Monitoring-vs-decision boundary reaffirmed.** Public-signal products exist
   as MONITORING; Orca's differentiation is the DECISION artifact + judgment.
5. **Break-in / competitor-customer: demoted** to (a) a cheap clean-substrate
   TEST and (b) a retainer horizon — not the first proof.
6. **Retainer map:** pricing density = near-term retainer; positioning =
   retainer anchor; PE / commercial-diligence = high-value end-state requiring a
   later interview/first-party method evolution (the logged Palantir-esque
   private-data horizon).
7. **The crux test:** does public signal DECIDE the decision or merely CONFIRM
   it? Resolve via two method-validation cases (no buyer contact -> clears the
   MVP gate).
8. **Two de-correlated verification runs corroborated** the disconfirming
   findings; the in-house-vs-bought buy-rate has no independent denominator and is
   the resolvable unknown.

## Part 2 — Doc-change cascade (smallest-complete)

KEY FRAMING: the corpus was ALREADY pricing-centric — every product doc's first
decision family is pricing/packaging/monetization, and the packet/charter already
carry the monitoring-vs-decision boundary, the judgment differentiation, and the
non-claims. So this is REFINEMENT, not replacement: light patches, one supersede
marker, one method-validation addition, and ZERO thesis change.

| # | Doc | Change type | Proposed delta | Do NOT change |
| --- | --- | --- | --- | --- |
| 1 | `docs/product/orca_product_lead_first_icp_wedge_decision_v0.md` | **Supersede marker** (no new v1) | Add a top pointer: superseded by `orca_icp_wedge_pricing_first_v0.md`, which is the current wedge authority. | The historical candidate-wedge comparison — leave as history. |
| 2 | `docs/product/orca_offer_hypothesis_v0.md` | **Patch** (not v1) | (a) Sector note: dev-facing = first-proof BEACHHEAD, wedge frame = cross-sector-open. (b) Add engine framing (competition = spine; pricing = first application). (c) Sharpen servability to the HARD GATE: the differentiated read rests on competitor-PRICE/packaging signal (clean); reviews are biased/polluted/interview-gated -> confirmatory-only, flagged. (d) Add the decide-vs-confirm crux as the open question. (e) Repoint `input_hashes` from the ICP-wedge-v0 to the pricing-first record. | The broad offer, value prop, executive-deck framing, commercial-frame-deferred, all non-claims. |
| 3 | `docs/product/orca_buyer_proof_packet_v0.md` | **Patch** | (a) RE-SCOPE the beachhead: dev-facing SaaS -> the AI-monetization slice (first-time AI-monetization / competitor-triggered repricing in public-pricing-rich SaaS; decision family unchanged; frame stays cross-sector-open). (b) Sharpen "enough public signal" -> "clean, decision-grade public substrate," with the review-substrate caveat (biased/polluted/interview-gated; the differentiated read uses competitor-price/packaging signal). (c) Repoint `input_hashes` -> pricing-first record. (d) Optional: note the decide-vs-confirm method-validation precondition. | Proof standard, rubric, kill/graduation criteria, manual/docs-first boundary, all non-claims — intact. |
| 4 | `docs/product/orca_product_proof_lead_charter_v0.md` | **Patch** | Same deltas as the packet (RE-SCOPE beachhead to the AI-monetization slice; hard-gate sharpening; repoint hashes). | Role/ownership/exclusions/non-claims — intact. |
| 5 | `docs/product/core_spine_v0_method_validation_case_locks_v0.md` (or a new method-validation pass record) | **Addition** | Propose two cases scored on DECIDE-vs-CONFIRM: (a) a competitor-triggered pricing-repricing case; (b) a clean-substrate competitor-displacement case (the break-in escape-hatch — non-review signal only). No buyer contact (clears the MVP gate). | The existing 5 locked cases + rubric. |
| 6 | `docs/decisions/turn_08_product_thesis_v0.md` | **No change** | Pricing is within the thesis's decision families; the hard-gate substrate refinement is a sharpening of "signal-quality judgment," not a thesis change. Record as intentionally_not_updated. | Everything. |
| 7 | `.agents/skills/orca-product-lead/SKILL.md` (candidate) | **Defer** | Refresh references to pricing-first ONLY if the candidate is accepted. Do NOT clobber `skill-adoption.md` (another lane modifies it). | n/a (unaccepted). |

## Part 3 — Propagation map (direction_change_propagation)

- Trigger: `product_doctrine` (the wedge framing). Each change in items 1-5
  carries its own DCP receipt when executed.
- Controlling sources updated (the cascade): items 1-5 above.
- Downstream surfaces checked, NO change needed:
  - `turn_08_product_thesis_v0.md` — consistent (pricing within scope).
  - `.agents/workflow-overlay/product-proof.md` — buyer-proof + trust-objection
    semantics unchanged; the packet/charter still reference it correctly.
  - `AGENTS.md` / `CLAUDE.md` — carry no product-wedge content.
  - `source-loading.md` / `orca_repo_map_v0.md` — the wedge is not a routing
    surface.
  - candidate skill — unaccepted.
- Order: supersede the ICP-wedge-v0 FIRST (so the others repoint correctly), then
  offer hypothesis -> packet -> charter -> method-validation cases. The patches are
  otherwise independent.
- Authority / branch: execute in the PRODUCT LANE on `main` with owner
  authorization. The lane docs are untracked on the ECR branch; this proposal does
  NOT fork doctrine edits onto ECR.
- Blocker: the propagation-incomplete state is already recorded in
  `orca_icp_wedge_pricing_first_v0.md` (the DCP blocker). It clears when the
  cascade lands.

## Part 4 — First-proof beachhead (owner-agreed, 2026-06-08)

The dev-facing-SaaS beachhead inherited from the OLD wedge was convenience-derived
(a candidate-context scan: Sentry/Clerk/Vercel), NOT derived from this session's
evidence — stale. Re-derived from the findings, the beachhead is:

> **B2B SaaS making a FIRST-TIME AI-monetization (or competitor-triggered)
> repricing/repackaging decision, where the competitor-pricing substrate is
> publicly rich (pricing pages + changelogs + loud public reaction) and the firm
> is flying blind (no internal AI-pricing history).**

Why this, not dev-facing-SaaS: AI-monetization is the single place the wedge's core
bet — public signal DECIDES a repricing move, not merely CONFIRMS it — is most
likely TRUE, because the firm has no internal history to fall back on. It is also
live now (time-boxed), greenfield (no incumbent playbook -> most
newcomer-winnable), and public-loud. It points the first proof AND the
decide-vs-confirm method-validation test at the same target. Dev-facing SaaS is a
strong sub-instance (loudest public communities, heaviest AI-pricing activity) —
but the DEFINING qualifier is "AI-monetizing / competitor-triggered +
public-substrate-rich," not "dev-facing." Still a hypothesis; the decide-vs-confirm
test is what would confirm it.

Consequence for the cascade: the packet/charter delta grows from "add a sector
note" to "RE-SCOPE the beachhead to the AI-monetization slice" (decision family
unchanged; frame stays cross-sector-open).

## Non-claims

Market-context and direction only — NOT validation, WTP, readiness, buyer-proof,
or ICP-proven. Pricing-first is the CHOSEN direction with the decide-vs-confirm
test still pending; the in-house-vs-bought buy-rate is unmeasured. The patches must
NOT upgrade pricing-first to "validated." No execution, runtime, or commit is
authorized by this proposal.
