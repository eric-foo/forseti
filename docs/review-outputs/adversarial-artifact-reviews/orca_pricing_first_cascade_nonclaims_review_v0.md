# Orca Pricing-First Cascade — Adversarial Review (Direction: Non-Claims & Overclaim Integrity) v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (adversarial artifact review)
review_lane: adversarial-artifact-review
review_mode: UNBOUND / RECOMMENDED lane -> ADVISORY findings-only (verdict advisory, NOT binding)
read_only: true
direction_key: nonclaims
direction: NON-CLAIMS & OVERCLAIM INTEGRITY (Orca product-proof discipline)
scope:
  - docs/product/orca_offer_hypothesis_v0.md
  - docs/product/orca_buyer_proof_packet_v0.md
  - docs/product/orca_product_proof_lead_charter_v0.md
fitness_reference:
  - docs/decisions/orca_icp_wedge_pricing_first_v0.md           # owner-locked controlling direction
  - docs/workflows/orca_pricing_first_doc_cascade_proposal_v0.md # agreed deltas + "do NOT change" lists
governing_overlay:
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/product-proof.md
skill_applied: workflow-adversarial-artifact-review (invoked); deep-thinking discipline applied in-source (workflow-deep-thinking not separately invoked — single-shot reviewer; noted per skill contract)
verdict: accept_with_friction   # ADVISORY ONLY — not an accept/reject gate
use_when:
  - Inspecting non-claim and overclaim-integrity findings for the pricing-first cascade.
  - Tracing cascade corrections to this advisory review.
authority_boundary: retrieval_only
reviewed_by: unrecorded
authored_by: unrecorded
```

## Review-Use Boundary (read first)

This is an **unbound, recommended** review lane. Findings are **decision input only** for
the owner / Chief Architect. They are **not** approval, rejection, validation,
mandatory remediation, or executor-ready patch authority. No `patch_queue_entry`
is emitted (not overlay-authorized for this lane). The `verdict` field is advisory.
This review is **READ-ONLY**; no reviewed doc was edited.

## Source-Read Ledger / Dirty-Source Note

- `orca_offer_hypothesis_v0.md`, `orca_buyer_proof_packet_v0.md`,
  `orca_product_proof_lead_charter_v0.md` — the review targets (current working-tree
  state). **All three are UNTRACKED on branch `ecr-sp3-timing-deriver-slice1`**
  (`git status` = `??`) and have **no committed version on any branch/ref** (verified
  via `git log --all`). The controlling decision itself records this ("Durable home is
  the product lane on main; untracked on the ECR branch").
- `orca_icp_wedge_pricing_first_v0.md` (controlling direction, untracked on ECR),
  `orca_pricing_first_doc_cascade_proposal_v0.md` (agreed deltas), `product-proof.md`
  (canonical non-claims authority), `review-lanes.md` (lane authority),
  `orca_product_lead_first_icp_wedge_decision_v0.md` (superseded ICP wedge, read for
  context only) — read as fitness/authority context.
- **Confidence limit (material):** because there is no committed baseline of the three
  targets, "preserved verbatim / unchanged in substance" **cannot be diff-verified
  mechanically**. This review verifies non-claim integrity against (a) the canonical
  product-proof non-claims list, (b) the proposal's per-doc "do NOT change" lists, and
  (c) internal/cross-doc consistency. See AR-04.

## Scope / Excluded Scope

In scope (this direction): preservation of product-proof non-claims; any snuck-in
validation / WTP / readiness / buyer-proof / ICP-proven / commercial-readiness claim;
"chosen direction (not validated)" framing with decide-vs-confirm pending; survival of
proof standard / rubric / kill / graduation criteria. Out of scope (other reviewers'
lanes): wedge strategy correctness, beachhead derivation merit, hard-gate evidence
quality, DCP propagation completeness, prose/style.

---

## Phase 1 — Correctness Findings

### Summary of what holds (non-claims integrity — PASS)

The rewrite is, on my direction, **clean in substance**. Verified concretely:

- **Full canonical non-claim set preserved in all three docs.** The
  `product-proof.md` required list (no buyer validation; no buyer-proof evidence
  absent a complete receipt; no WTP proof; no repeatability proof; no product/feature/
  implementation/commercial readiness; no Core Spine v0 validation) is fully covered:
  offer hypothesis lines 50-52, 308-310, 562-581; packet lines 433, 444-463; charter
  lines 311-324 + 292. No canonical non-claim was dropped.
- **No snuck-in validation/WTP/readiness/proven/buyer-proof claim.** The beachhead is
  stated as "selected, not proven" (offer 252), "Still a hypothesis" (cascade framing),
  "the bounded market-facing test of the broader offer" (offer 220). Re-scope language
  re-scopes the *hypothesis*, never upgrades it.
- **The verification-run narrative was NOT imported.** The controlling decision's
  "two de-correlated verification runs / corroborated market-context / least-blocked /
  disproven" language appears in **none** of the three docs (grep: no matches). The
  rewrite did not smuggle the decision's confidence narrative in as product-doc proof.
- **Hard gate framed as a requirement, not a satisfied condition.** "Targets must have
  a clean, decision-grade public substrate" (packet 132, charter 163); reviews are
  "confirmatory-only and ... do not satisfy the hard gate" (packet 136). No doc claims
  clean substrate is *proven present* for any buyer. Market-context evidence (44% /
  Hinterhuber-Liozu) is NOT pulled in as a proof claim — only the clean/biased/polluted
  characterization is carried.
- **Pricing-first reads as CHOSEN, decide-vs-confirm PENDING — consistently.** All three
  docs carry the identical "Open question (pending, NOT validated): does public signal
  DECIDE the repricing move or merely CONFIRM it" line (offer 75-77; packet 59-61;
  charter 60-62).
- **Proof standard / rubric / kill / graduation survived intact and unweakened** in the
  packet (Proof Standard 86-108; Evaluation Rubric 289-321; Kill 382-395; Graduation
  397-410) and charter (Kill 267-280; Graduation 282-294). The packet's bounded
  `Readiness verdict: ready for product-fit testing` (line 33) is pre-existing in shape,
  explicitly bounded against product-bet/feature/implementation/commercial readiness, and
  matches the charter — not a rewrite-introduced overclaim.

The findings below are **minor**. None rises to a snuck-in validation/WTP/readiness
claim. The cascade is, for this direction, safe to treat as clean once AR-01/AR-02 are
weighed by the owner.

---

### AR-01 (correctness, MINOR) — Offer-hypothesis alignment note claims preservation of sections the doc does not contain

- **Doc / location:** `orca_offer_hypothesis_v0.md`, "Pricing-First Refinement"
  closing paragraph, lines 96-99: *"proof standard, evaluation rubric, kill/graduation
  criteria, non-claims, and all non-claim text are unchanged."*
- **Source authority:** the cascade proposal (`...proposal_v0.md`, Part 2 row 2) assigns
  the offer hypothesis deltas (a)-(e) and a "do NOT change" list of *the broad offer,
  value prop, executive-deck framing, commercial-frame-deferred, all non-claims*. It does
  **not** attribute a "proof standard / rubric / kill / graduation criteria" to the offer
  hypothesis — those are packet/charter sections.
- **Evidence:** a full-file scan of the offer hypothesis for `rubric|kill|graduation|proof
  standard` returns **only line 98 itself** (the alignment note). The doc contains no
  Evaluation Rubric, Kill Criteria, Graduation Criteria, or Proof Standard section.
- **Impact:** the boundary-preservation assertion references artifacts this doc never
  owned. It is harmless to *claims* (it over-states preservation, not under-states it),
  but it muddies which doc is the authority for those criteria and could mislead a future
  reader into auditing the offer hypothesis for rubric/kill drift. Mild authority-hygiene /
  accuracy defect, not an overclaim of validation.
- **minimum_closure_condition:** the offer-hypothesis alignment note describes only the
  boundaries this doc actually carries (broad offer, value prop, deck framing,
  commercial-frame-deferred, non-claims), or explicitly attributes proof-standard/rubric/
  kill/graduation preservation to the packet and charter rather than to itself.
- **next_authorized_action:** owner/Chief Architect decision; optional later patch in the
  product lane. No action mandated by this lane.
- **patch_queue_entry:** not authorized (advisory lane).
- **not proven:** that this wording caused any downstream misread (no evidence either way).

---

### AR-02 (correctness, MINOR) — Compact 4-item DCP non-claims could be misread as the doc's full non-claim set

- **Doc / location:** all three docs, the embedded `direction_change_propagation:` YAML
  `non_claims:` block lists exactly four items — `not validation / not willingness-to-pay /
  not readiness / not ICP proven` (offer 89-93; packet 73-77; charter 74-78).
- **Source authority:** `product-proof.md` "Product-Proof Non-Claims" enumerates nine
  required non-claims (adds buyer-proof-evidence, repeatability, product/feature/
  implementation readiness split, commercial readiness, Core Spine v0 validation). The
  controlling decision's own DCP block uses the same compact 4 — so the compact echo is
  consistent with the controlling source.
- **Evidence:** the full nine-item set **does survive** in each doc's dedicated non-claims
  section (verified — see Phase 1 summary). The 4-item list is a DCP receipt echo, not the
  doc's non-claims of record.
- **Impact:** low. Because the compact list sits inside a fenced YAML labeled
  `direction_change_propagation`, a careless reader could treat it as "the non-claims for
  this refinement" and conclude WTP/readiness are the only boundaries the pricing-first
  change must respect. The defense (full list elsewhere in-doc) is real but is not
  cross-referenced from the DCP block.
- **minimum_closure_condition:** the DCP `non_claims:` block either notes it is a compact
  echo of the doc's full non-claims section, or the owner explicitly accepts the 4-item
  DCP convention (as already used in the controlling decision) as sufficient.
- **next_authorized_action:** owner decision; this is consistent with existing Orca DCP
  convention, so "accept as-is" is a legitimate outcome. No action mandated.
- **patch_queue_entry:** not authorized.
- **not proven:** n/a.

---

### AR-03 (correctness, MINOR) — "SURGICALLY ALIGNED ... unchanged in substance" is an unverifiable self-attestation given no baseline

- **Doc / location:** all three docs assert their substantive content was "SURGICALLY
  ALIGNED" and the proof standard/rubric/kill/graduation/non-claims are "unchanged"
  (offer 96-99; packet 80-83; charter 81-85).
- **Source authority / evidence:** the three targets are **untracked**, with **no committed
  baseline on any ref** (`git log --all` returns nothing for all three). The proposal
  explicitly scopes execution to the product lane "on `main`" and says the proposal "does
  NOT fork doctrine edits onto ECR" (proposal Part 3). These edits exist only as untracked
  ECR working-tree files.
- **Impact:** the "unchanged" claim is a **self-attestation that cannot be independently
  diff-verified** by any reviewer, because there is no prior committed text to diff against.
  My direction-level conclusion (non-claims are intact) rests on the canonical-list and
  cross-doc-consistency checks, **not** on the rewrite's own "unchanged" assertion. This is
  a process/auditability gap, not a detected claim violation.
- **minimum_closure_condition:** the cascade lands in its durable home (product lane on
  `main`) with a committed baseline so the "unchanged in substance" claim becomes
  diff-auditable; OR the owner accepts the non-claim integrity on the strength of this
  review's canonical-list verification.
- **next_authorized_action:** owner/Chief Architect decision on where these edits durably
  land (the controlling decision already routes this to the product lane on main). Outside
  this review's authority to relocate.
- **patch_queue_entry:** not authorized.
- **not proven:** whether the working-tree text differs from any intended pre-edit baseline
  (no baseline exists to compare).

---

## Phase 2 — Friction Findings

### AR-04 (friction, MINOR) — Triple-restated alignment block adds maintenance surface

- **Doc / location:** the near-identical "Pricing-First Refinement (2026-06-08)" prose +
  DCP YAML block is repeated in all three docs (offer 54-99; packet 37-83; charter 39-85).
- **Impact:** this is acceptable for self-contained per-doc DCP receipts (each doc should
  carry its own propagation record). The friction is only that the four-bullet delta prose
  and the "read 'enough public signal' as 'clean, decision-grade substrate'" instruction are
  copy-pasted, so any future correction to the refinement description must be applied in
  three places or they drift. Low cost; flagged for awareness, not remediation.
- **minimum_closure_condition:** none required — per-doc DCP receipts are the Orca
  convention. Optional: a single canonical refinement description with per-doc pointers.
- **next_authorized_action:** none mandated; owner may accept the redundancy as intended.
- **patch_queue_entry:** not authorized.

---

## Strict-Only Blockers / Not-Proven Boundaries

- **Not proven (and not claimed by this review):** that the cascade is validated, WTP-
  proven, ready, buyer-proven, or ICP-proven — the docs correctly disclaim all of these, and
  this review asserts none.
- **Strict claims withheld:** no formal artifact-role pass/fail, no overlay-bound
  ready/blocked status, no validation verdict. This lane is unbound/advisory; such claims
  would require overlay binding (`review-lanes.md`).
- **Auditability gap (AR-03):** "unchanged in substance" is not independently verifiable
  without a committed baseline.

## Minimum-Closure / Next-Authorized-Action Roll-Up

| ID | Severity | Minimum closure condition | Next authorized action |
| --- | --- | --- | --- |
| AR-01 | minor | Offer-hypothesis note describes only the boundaries this doc owns, or attributes rubric/kill/graduation preservation to packet+charter | Owner decision; optional product-lane patch |
| AR-02 | minor | DCP 4-item list flagged as compact echo, or owner accepts existing DCP convention | Owner decision (accept-as-is is valid) |
| AR-03 | minor | Cascade committed to durable home so "unchanged" is diff-auditable, or owner accepts this review's canonical-list verification | Owner routing decision (already pointed to main) |
| AR-04 | minor | None required (per-doc DCP is convention); optional dedupe | None mandated |

## Advisory Verdict (NON-BINDING)

`accept_with_friction`. For the **non-claims & overclaim-integrity** direction, the rewrite
**preserves every canonical product-proof non-claim, introduces no validation / WTP /
readiness / buyer-proof / ICP-proven / commercial-readiness claim, keeps pricing-first as
the CHOSEN (not validated) direction with the decide-vs-confirm test explicitly pending, and
leaves the proof standard / rubric / kill / graduation criteria intact and unweakened.** The
four findings are minor and concern self-description accuracy (AR-01), receipt-echo clarity
(AR-02), baseline auditability (AR-03), and copy-paste maintenance (AR-04) — none is a
snuck-in claim. None blocks treating the cascade as clean on this direction.

*Findings are decision input only. They are not approval, validation, mandatory remediation,
or executor-ready patch authority unless separately accepted or authorized by an Orca lane.*
