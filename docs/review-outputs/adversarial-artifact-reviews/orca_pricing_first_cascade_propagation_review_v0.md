# Orca Pricing-First Cascade — Propagation & Coherence Adversarial Review (advisory) v0

```yaml
retrieval_header_version: 1
artifact_role: Adversarial artifact review output (advisory, findings-only)
review_lane: adversarial-artifact-review (UNBOUND, RECOMMENDED) — advisory critique, no binding verdict
review_direction: propagation_and_coherence
read_only: true
commission:
  target:
    - docs/product/orca_offer_hypothesis_v0.md
    - docs/product/orca_buyer_proof_packet_v0.md
    - docs/product/orca_product_proof_lead_charter_v0.md
  purpose: >
    Did the 3 Sonnet rewrites fully and cleanly align the bodies to the
    owner-locked pricing-first direction? Hunt stale dev-facing / "enough public
    signal" text, banner-vs-body incoherence, broken DCP receipts, accidental
    decision-family wording change, and downstream surfaces that should have been
    aligned but were not (or were wrongly touched).
controlling_direction: docs/decisions/orca_icp_wedge_pricing_first_v0.md
agreed_deltas: docs/workflows/orca_pricing_first_doc_cascade_proposal_v0.md
fitness_reference:
  goal: >
    The product-doc cascade REFINES (not replaces) the already-pricing-centric
    corpus to the pricing-first / AI-monetization-beachhead / outside-in
    competitive-intelligence-engine / clean-substrate-servability-hard-gate
    framing, while preserving decision family, proof gates, rubric,
    kill/graduation criteria, and all non-claims unchanged.
  success_signal: >
    Per the cascade proposal "Do NOT change" columns + the controlling decision's
    direction_change_propagation_blocker: every live downstream surface that
    consumes the beachhead/servability framing is either aligned or correctly
    recorded as intentionally_not_updated; no surface still asserts the demoted
    dev-facing-default beachhead or the un-sharpened "enough public signal" gate
    as if current; decision-family wording is byte-stable.
  source: >
    Pointer-bound. docs/decisions/orca_icp_wedge_pricing_first_v0.md (Decision +
    direction_change_propagation_blocker) and
    docs/workflows/orca_pricing_first_doc_cascade_proposal_v0.md (Part 2 table,
    Part 3 propagation map, Part 4 beachhead).
non_claims:
  - advisory findings only; not a binding accept/reject verdict
  - not validation, not WTP, not readiness, not buyer proof, not ICP proven
  - findings are decision input; not mandatory remediation or executor-ready
    patch authority until separately accepted/authorized
use_when:
  - Inspecting propagation and coherence findings for the pricing-first cascade.
  - Tracing cascade corrections to this advisory review.
authority_boundary: retrieval_only
reviewed_by: unrecorded
authored_by: unrecorded
review_use_boundary: Findings are decision input, not approval, validation, mandatory remediation, or patch authority.
```

## Review-Use Boundary

This is an UNBOUND, RECOMMENDED review lane. Findings below are advisory decision
input for the owner / Chief Architect only. The `verdict` field is advisory, not
a binding gate. Nothing here approves, validates, or authorizes remediation,
patches, commits, or readiness. Only a separately authorized patch/acceptance
lane can make any remediation mandatory or executor-ready.

## Source-Read Ledger

| Source | Why read | Status |
| --- | --- | --- |
| `docs/decisions/orca_icp_wedge_pricing_first_v0.md` | Controlling owner-locked direction + DCP blocker (fitness reference). | untracked on ECR branch; treated as the controlling direction per prompt. |
| `docs/workflows/orca_pricing_first_doc_cascade_proposal_v0.md` | Agreed deltas: per-doc "Do NOT change", propagation map, beachhead. | untracked; treated as agreed-delta reference per prompt. |
| `docs/product/orca_offer_hypothesis_v0.md` (target) | Reviewed for alignment + coherence. | untracked (`??`); no committed baseline to diff. |
| `docs/product/orca_buyer_proof_packet_v0.md` (target) | Reviewed for alignment + coherence. | untracked (`??`); no committed baseline to diff. |
| `docs/product/orca_product_proof_lead_charter_v0.md` (target) | Reviewed for alignment + coherence. | untracked (`??`); no committed baseline to diff. |
| `docs/product/orca_product_lead_first_icp_wedge_decision_v0.md` | Cascade item 1 (supersede-marker target); SHA-receipt holder. | untracked (`??`). |
| `docs/product/orca_discovery_batch_0_target_selection_brief_v0.md` | Live downstream qualification instrument that consumes the beachhead. | untracked (`??`). |
| `docs/prompts/product-planning/orca_product_proof_lead_customer_discovery_prompt_v0.md` | Active discovery instrument referenced by the brief. | tracked; checked line 149. |
| `docs/decisions/turn_08_product_thesis_v0.md` | DCP receipts claim it is "consistent; no change". | tracked; verified consistent. |
| `.agents/workflow-overlay/{review-lanes,product-proof}.md` | Review machinery + product-proof semantics. | review-lanes clean; product-proof `M` (modified for an unrelated Judgment-Spine reason). |

Dirty/unanchored sources affecting confidence: the three targets are **untracked**
(no committed baseline), so pre/post-rewrite diffing is by-inspection against the
proposal's "Do NOT change" columns, not by `git diff`. `product-proof.md` is
`M` for a reason unrelated to pricing (its own Judgment-Spine DCP block).

## Method & Discipline

- `workflow-deep-thinking`: invoked.
- `workflow-adversarial-artifact-review`: invoked.
- Two-phase: Phase 1 (propagation correctness) before Phase 2 (coherence/friction).
- SHA receipts independently recomputed with `hashlib.sha256` (see AR-02).

## What Propagated CLEANLY (credited, so findings are calibrated)

- **Cascade item 1 supersede marker landed correctly.** `orca_product_lead_first_icp_wedge_decision_v0.md` status now reads `SUPERSEDED 2026-06-08 by docs/decisions/orca_icp_wedge_pricing_first_v0.md ... This record is HISTORICAL; read the pricing-first record for the current wedge.` This matches proposal item 1 (supersede marker, no new v1) and preserves the historical candidate-wedge comparison.
- **Decision-family wording is UNCHANGED (the must-not-change constraint holds).** The family list `pricing, packaging, API, billing, usage, add-on, monetization` is identical across all three targets, the wedge-decision doc, and the discovery brief. The "decision-family wording accidentally changed" hunt is **clean** — no violation found.
- **`turn_08_product_thesis_v0.md` is genuinely consistent.** It frames pricing within its decision families and carries no dev-facing beachhead and no "enough public signal" servability gate, so the DCP receipt line `consistent; no change (pricing within scope)` is accurate (not a hollow receipt).
- **In-target body alignment is substantively complete.** The beachhead re-scope (AI-monetization slice; dev-facing demoted to "strong sub-instance, not the defining qualifier"; cross-sector-open) and the clean-substrate hard gate (competitor price/packaging clean; reviews confirmatory-only, biased/FTC-polluted/interview-gated) are carried through each target's live surfaces — offer hypothesis Core Offer / Buyer-Facing Draft / ICP Status / Qualifying conditions / Fit Diagnostic gates; packet Proof Standard / Target Buyer / Promise; charter Role Purpose / First Proof Lane. No residual literal "developer-facing"-as-default-beachhead survives **inside the three commissioned targets**.
- **Proof gates / rubric / kill / graduation / non-claims preserved.** Spot-checked against the proposal "Do NOT change" columns: intact in substance in all three.

## Phase 1 — Propagation Correctness Findings

### AR-01 (major) — DCP receipts under-enumerate the live downstream surface set; two active discovery instruments still hard-gate to the demoted dev-facing-default beachhead

- phase: correctness
- artifact role: product artifacts (targets) + downstream qualification instruments
- location:
  - receipts: identical `direction_change_propagation` blocks in
    `orca_offer_hypothesis_v0.md` (~L80-94), `orca_buyer_proof_packet_v0.md`
    (~L64-78), `orca_product_proof_lead_charter_v0.md` (~L65-79), each with
    `downstream_surfaces_checked: [turn_08…, product-proof.md]` only.
  - stale live surface 1: `orca_discovery_batch_0_target_selection_brief_v0.md`
    L58 "First lane: post-revenue **developer-facing** B2B SaaS, platform, API,
    infrastructure, or data-product companies." and L70 (hard gate) "Company type
    is post-revenue **developer-facing** B2B SaaS, platform, API, infrastructure,
    or data-product."
  - stale live surface 2: `docs/prompts/product-planning/orca_product_proof_lead_customer_discovery_prompt_v0.md`
    L149 "Company type: post-revenue **developer-facing** B2B SaaS, platform, API,
    infrastructure, or data-product company."
- source authority: controlling decision's `direction_change_propagation_blocker`
  (propagation is INCOMPLETE until the cascade lands) + the rewritten beachhead,
  which demotes dev-facing to "a strong sub-instance, **not the defining
  qualifier**" and re-scopes the beachhead to the AI-monetization slice.
- evidence / impact: the three targets now define the beachhead as the
  AI-monetization slice, but the discovery brief and the discovery prompt it
  references still assert "developer-facing" as a **hard company-type gate / First
  Lane**. These are the live instruments that route the next discovery batch.
  Left as-is they would qualify/disqualify candidates on the demoted default
  rather than the current beachhead — a direct downstream contradiction of the
  re-scope. Each target's DCP receipt asserts the only downstream surfaces are
  `turn_08` + `product-proof.md`; that enumeration is incomplete for a
  beachhead/servability change.
- scope note (anti-overreach): these two surfaces were **not** in the rewriters'
  3-doc commission, and the cascade proposal itself did not enumerate them in
  Part 2 (items 1-5) or Part 3 (downstream-checked). So this is best read as a
  **cascade-scoping gap the receipts should have surfaced**, not a "rewriters
  corrupted an in-scope doc" miss. It is still material because propagation is
  explicitly INCOMPLETE and these are active instruments.
- minimum_closure_condition: either (a) the discovery brief + discovery prompt
  are realigned to the AI-monetization-slice beachhead (dev-facing as
  sub-instance, cross-sector-open) under a separate authorized patch, or (b) each
  target's `downstream_surfaces_checked` adds these two surfaces with an explicit
  `intentionally_not_updated` + reason (e.g., deferred to a discovery-lane patch),
  so the receipt no longer implies a complete downstream sweep that omits them.
- next_authorized_action: owner/CA decision on (a) vs (b); no edit authorized by
  this advisory lane.
- patch_queue_entry: not authorized (advisory lane).
- not proven: that the discovery brief/prompt were *in scope* for these rewriters
  — they were not; the finding is about receipt completeness + live contradiction.

### AR-02 (minor) — Cross-reference SHA receipts are now stale across the cascade; the supersede-marker doc still asserts "Pinned source hash check: pass"

- phase: correctness
- artifact role: product artifacts (receipt hygiene / routing authority)
- location / evidence (recomputed SHA-256, actual vs pinned):
  - `orca_offer_hypothesis_v0.md` `input_hashes` pins buyer-proof
    `ECDCD4BF…224`, charter `731E4349…322`, product-proof `0EB8A11D…F21`;
    actual buyer-proof `0615E20C…340`, charter `B9FEDDB3…DD`, product-proof
    `AD172420…C4` → all three MISMATCH.
  - `orca_product_lead_first_icp_wedge_decision_v0.md` `input_hashes` pins offer
    `AC3943A0…64`, buyer-proof `B7B4B169…18`, charter `BFA1685D…89`; actual offer
    `01156234…89`, buyer-proof `0615E20C…340`, charter `B9FEDDB3…DD` → MISMATCH;
    **and** its body L62 still states "Pinned source hash check: pass. No blocking
    source drift was found in the pinned controlling sources."
  - `orca_discovery_batch_0_target_selection_brief_v0.md` pins wedge-decision
    `B570672C…23`, charter `731E4349…322`, buyer-proof `ECDCD4BF…224` → all now
    stale.
- source authority: `.agents/workflow-overlay/review-lanes.md` (retrieval-metadata
  defects are routing/authority-hygiene issues) + the targets' own design choice
  to use prose-supersede (`reread-required` + `controlling_decision:`) instead of
  re-pinning hashes (proposal items 2-4 said "repoint input_hashes"; rewriters
  chose prose — a defensible substitution).
- impact: routing/hygiene only — a reader using `input_hashes` for anchor
  verification across these docs will see drift. Two mitigations keep this minor:
  (i) the three targets explicitly state the pins are superseded and `reread-required`;
  (ii) the wedge-decision doc is marked HISTORICAL and its banner redirects
  readers to the pricing-first record. The one genuinely incoherent residue is the
  wedge-decision body line "hash check: pass," which sits inside the same
  2026-06-08 edit that added the supersede banner and is now false on its face.
- minimum_closure_condition: either re-pin the cross-references on the next
  authorized pass, or (lighter) neutralize the now-false "Pinned source hash
  check: pass" line in the HISTORICAL wedge-decision doc so it does not assert a
  passing check against drifted pins.
- next_authorized_action: owner/CA decision; no edit authorized here.
- patch_queue_entry: not authorized.
- not proven: that re-pinning is required at all — the prose-supersede approach is
  acceptable; this is flagged as hygiene drift, not a blocking defect.

## Phase 2 — Coherence / Friction Findings

### AR-03 (minor) — Offer-hypothesis banner reread-instruction is narrower than the packet's, leaving "enough public signal" phrasing in broad-offer prose that a fast reader could misread as the first-proof gate

- phase: friction
- artifact role: product artifact (offer hypothesis)
- location: banner L73 instructs "Read **'enough public signal' below** as
  'clean, decision-grade substrate.'" Residual broad-offer phrasings: L157-158
  "open to pre-revenue or post-revenue companies when they face a real decision
  **with enough public or external signal**"; L454 (broad Fit Diagnostic Q4) "Are
  **public or external signals visible enough** to gather, inspect, and
  constrain?"
- source authority: cascade proposal "Do NOT change: the broad offer, value prop"
  for item 2; the hard gate is a **first-proof** servability gate, not a
  broad-offer gate.
- assessment (deliberately NOT escalated): L157-158 and L454 describe the BROAD
  offer / broad fit diagnostic, which the proposal explicitly preserves. The hard
  gate correctly lives in the first-proof surfaces (ICP Status, first-proof Fit
  Diagnostic gates 1-7, Qualifying conditions), which the rewrite sharpened. So
  this is **coherent by design**, not a contradiction — I am recording it as a
  considered non-blocking friction note, not a defect. Compare the packet, whose
  banner says "Read **every** 'enough public signal' / 'meaningful public signal'
  requirement below" — stronger and self-consistent. The offer banner's narrower
  wording ("'enough public signal' below," singular) is the only reason a hurried
  reader might over-apply the reread to broad-offer prose.
- impact: low — reader friction / theoretical misread only; no live qualification
  instrument is misrouted by it.
- minimum_closure_condition: optional only — if desired, align the offer banner's
  reread scope to the packet's "every … requirement" phrasing, or add "(first-proof
  gate only)" to the broad-offer lines. Not required for correctness.
- next_authorized_action: none required; optional hardening for owner discretion.
- patch_queue_entry: not authorized.
- not proven: that this is a defect at all — flagged as optional hardening.

## Items Checked and Found CLEAN (anti-anchoring transparency)

- Decision-family wording: byte-stable across all docs (no accidental change). CLEAN.
- Banner-vs-body in the two strongest targets (packet, charter): banner reread
  instruction + actively-rewritten body gates are mutually reinforcing. CLEAN.
- "Wrongly touched" downstream surfaces: none found — `turn_08` correctly
  untouched; the two historical review prompts that quote the old wedge
  (`orca_ai_exposed_icp_refinement_adversarial_review_prompt_v0.md` L140/L148) are
  legitimately frozen historical artifacts, not stale live surfaces. CLEAN.
- `product-proof.md` semantics relied on by packet/charter: unchanged in substance
  (its `M` status is an unrelated Judgment-Spine edit). CLEAN for this cascade.
- Supersede ordering (proposal Part 3: supersede wedge-decision first): the
  supersede marker is present; ordering is satisfied. CLEAN.

## Advisory Verdict (NON-BINDING)

`changes_recommended` (advisory). The three commissioned targets are substantively
and cleanly aligned internally — beachhead re-scope, hard gate, engine framing all
landed, and the must-not-change constraints (decision family, gates, rubric,
non-claims) hold. The recommendation to make changes is driven by **propagation
completeness beyond the three docs**, not by a defect inside them: two live
discovery instruments still hard-gate to the demoted dev-facing default (AR-01),
and the cross-doc SHA receipts plus one HISTORICAL "hash check: pass" line are
stale (AR-02). AR-03 is optional hardening only.

## Must-Fix (to treat the cascade's propagation as clean)

1. AR-01 — resolve the discovery brief + discovery prompt contradiction with the
   re-scoped beachhead (align them, or record them as `intentionally_not_updated`
   in the targets' `downstream_surfaces_checked` with a reason). Until then the
   propagation receipts overstate downstream coverage and two live instruments
   misroute discovery to the demoted default.
