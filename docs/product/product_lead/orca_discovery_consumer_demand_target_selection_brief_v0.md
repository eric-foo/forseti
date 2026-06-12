# Orca Discovery — Consumer-Demand Target-Selection Brief v0 (PROPOSED)

```yaml
retrieval_header_version: 1
artifact_role: Product artifact (live discovery instrument — adopted 2026-06-12)
scope: >
  Target-selection instrument for the consumer-demand/beauty first proof:
  blank target slots, qualification objectives, and stop rules derived from
  the ratified thesis + wedge (2026-06-12). Replaces the pricing-gated
  orca_discovery_batch_0_target_selection_brief_v0.md, which pricing-first
  propagation AR-01 already flagged as a misrouting live instrument. Slots
  are intentionally blank: no candidate scan is authorized yet, and the
  standing no-buyer-contact gate is closed (owner ask 4, 2026-06-12).
supersedes:
  - docs/product/product_lead/orca_discovery_batch_0_target_selection_brief_v0.md
use_when:
  - Selecting blank consumer-demand discovery target slots after the wedge is ratified and a candidate-scan lane is authorized.
  - Checking first-contact qualification objectives for the beauty operator door before memo production.
authority_boundary: retrieval_only
open_next:
  - docs/product/product_lead/orca_buyer_proof_packet_consumer_demand_revision_v0.md  # owns the substrate gate + disqualifiers
  - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
  - .agents/workflow-overlay/product-proof.md
input_hashes:
  docs/decisions/orca_product_thesis_consumer_demand_v0.md: 5FEA48AE8B0C0E22D24CE2194F1F17617C5C94D2C75A204AAD5CD8CC149B2B0E
  docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md: C878ABEBBFFC119A032E0290E093A9EBB973BC15052B4B21FA59D285AB83C07B
branch_or_commit: ecr-sp3-timing-deriver-slice1 @ 48c00ca
stale_if:
  - The owner amends the thesis or wedge (re-derive against the amended text).
  - The buyer-proof packet revision's Demand-Substrate Hard Gate changes (gates below re-derive from it).
  - The no-buyer-contact gate is reopened or changed (re-read before any use).
```

## Status

`ADOPTED_LIVE_INSTRUMENT` — adopted 2026-06-12 by the ratification cascade
(owner ratified thesis asks 1-2; runbook step 6). Supersedes the batch-0
target-selection brief as the live instrument. Prepared 2026-06-11 by the
ICP / product-direction lane. The companion instrument —
`docs/prompts/product-planning/orca_product_proof_lead_customer_discovery_prompt_v0.md`
— is OUTSIDE the product lane's write scope (prompt artifact). Corrected
2026-06-12 (gap DB-5): ORCA-HYGIENE-018 was resolved by RETIRING that prompt
outright (RETIRED / OFF-TARGET banner, 2026-06-12), not by realigning it. No
live discovery operating prompt exists; when the owner opens outreach, a
consumer-demand successor must be commissioned through prompt orchestration
before any discovery runs.

Dated note (2026-06-12, owner ask-1 amendment): the capture risk posture is
measured ToS risk accepted / absurd-level rejected (the owner's example:
Bright-Data-style industrial scraping); per-venue route bindings stay
capture-lane-owned. The stop rules below are stated under that posture.

## Output Boundary (carried unchanged from batch 0)

Docs-first target-selection instrument only. It does not authorize buyer
outreach (standing gate: no buyer contact before full-spine MVP —
`docs/decisions/advisory_proof_slice_definition_v0.md` — closed unless the
owner names an opening condition under thesis ask 4), public web research,
candidate scanning, memo or deck production, product-bet or feature planning,
implementation, source systems, dashboards, source maps, data-spine design,
CRM workflows, commits, pushes, or PRs. Filling the blank slots below requires
a separately authorized candidate-scan lane.

## Target Slots (blank by design)

| Slot | Candidate context (brand + live decision) | Decision family | Venue families visible (≥2 required) | Costly-behavior evidence visible | Org-motion route available (capture-lane-bound routes) | Named decision owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | `UNFILLED - requires authorized candidate scan` | — | — | — | — | — | empty |
| T2 | `UNFILLED - requires authorized candidate scan` | — | — | — | — | — | empty |
| T3 | `UNFILLED - requires authorized candidate scan` | — | — | — | — | — | empty |
| T4 | `UNFILLED - requires authorized candidate scan` | — | — | — | — | — | empty |
| T5 | `UNFILLED - requires authorized candidate scan` | — | — | — | — | — | empty |
| T6 | `UNFILLED - requires authorized candidate scan` | — | — | — | — | — | empty |

Slot-fill rule: a slot may be filled only from a dated, provenance-noted
candidate scan produced by an authorized lane; no slot is filled from memory,
from another lane's unverified summary, or from this lane. Slots default
US-market per the thesis geography doctrine (2026-06-12); non-US candidates
route to the owner or defer (mirroring the candidate-pool handoff
obligations). Candidate companies are not buyers, leads, prospects, or
clients; trust posture is `unknown` until qualification.

## Qualification Objectives (first contact, when outreach is ever opened)

Derived from the wedge and the buyer-proof packet revision; the packet's
Demand-Substrate Hard Gate and disqualifiers control on any conflict.

1. Confirm a live 30-90 day consumer-demand allocation decision in the
   wedge's families (tier/price; retail/channel expansion;
   launch/moratorium/reposition; taste-shift pivot; defend/hold).
2. Confirm a named decision owner (founder, head of brand / insights /
   growth / strategy) and a concrete allocation consequence.
3. Confirm the Demand-Substrate Hard Gate is satisfiable for this decision:
   at least two independent venue families visible, costly-behavior evidence
   present, integrity labels applicable, no route outside the capture lane's
   current bindings required (and no absurd-risk route at any time).
4. Classify public-signal trust state (`trust_open` / `trust_objection` /
   `trust_refusal`) per `.agents/workflow-overlay/product-proof.md`; only
   categorical `trust_refusal` disqualifies.
5. Test paid-first willingness before any custom artifact work.
6. Record pull versus praise per the packet; praise, curiosity, and generic
   deck interest are not pull.

## Stop Rules (carried unchanged)

- Stop at any disqualifier in the buyer-proof packet revision (B3).
- Stop if qualification would require outreach while the no-buyer-contact
  gate is closed.
- Stop if signal coverage would require a route outside the capture lane's
  current bindings or an absurd-risk approach (owner posture 2026-06-12:
  measured ToS risk accepted; Bright-Data-style industrial scraping
  rejected). Route expansion is a capture-lane decision, not a
  discovery-time stretch.
- Do not stretch the wedge around a near-miss candidate; record the gap and
  hold or disqualify.

## Claim-Tier Classification

Design / product-learning-tier instrument; no proof, readiness, validation,
or judgment-quality claim; closeout state for any such claim:
`no_durable_evidence`.

## Non-Claims

Live instrument only — not candidate selection, not buyer validation, not
outreach authority, not a research authorization, not proof of anything.
Blank slots are a deliberate boundary, not an omission. Mints no
evidence-ladder vocabulary; redefines no overlay-owned semantics.
