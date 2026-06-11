# ICP / Product-Direction Ratification-Readiness Report v0

```yaml
retrieval_header_version: 1
artifact_role: Product-planning lane report (consistency sweep; advisory)
scope: >
  Ratification-readiness consistency sweep of the consumer-demand product
  thesis and ICP wedge against every subordinate product-lead artifact and
  named lane record: what blocks owner asks 1-2, what merely needs the
  prepared ratification-day cascade, and what is out of cascade scope.
use_when:
  - Deciding whether thesis asks 1-2 can be ratified in one sitting.
  - Checking which inconsistency is a blocker versus prepared-cascade work.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_consumer_demand_ratification_decision_memo_v0.md
  - docs/product/product_lead/orca_ratification_day_runbook_v0.md
  - docs/decisions/orca_product_thesis_consumer_demand_v0.md
  - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
input_hashes:
  docs/decisions/orca_product_thesis_consumer_demand_v0.md: 5FEA48AE8B0C0E22D24CE2194F1F17617C5C94D2C75A204AAD5CD8CC149B2B0E
  docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md: C878ABEBBFFC119A032E0290E093A9EBB973BC15052B4B21FA59D285AB83C07B
branch_or_commit: ecr-sp3-timing-deriver-slice1 @ 48c00ca
stale_if:
  - The owner ratifies or amends the thesis or wedge (the runbook and signed records govern from then on).
  - Any swept artifact is materially edited after 2026-06-11.
```

## Status

`PREP_LANE_REPORT_ADVISORY` — produced by the ICP / product-direction lane
2026-06-11 under the lane commission
(`docs/prompts/product-planning/icp_product_direction_lane_commission_prompt_v0.md`).
Advisory consistency findings from repo-visible evidence; no verdict authority,
no ratification, no patch execution.

## Intake Receipt

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: S2 product anchor + commission-targeted reads (custom)
  edit_permission: docs-write (docs/product/product_lead/ + docs/decisions/ PROPOSED drafts only)
  target_scope: ICP/product-direction prep package (commission deliverables 1-4)
  dirty_state_checked: yes
  blocked_if_missing: anchors unreadable or unverifiable hash drift - none observed
repo_map_decision: loaded (Product Anchor Files routing)
SOURCE_CONTEXT_READY: declared after the reads below.
```

Verified at intake (fresh reads, 2026-06-11):

- Branch/commit pin matches the commission: `ecr-sp3-timing-deriver-slice1` @
  `48c00ca`. Worktree dirt is other lanes' files plus the commission prompt
  itself; none touched by this lane.
- Both anchor hashes match the commission's `input_hashes` exactly (Get-FileHash
  SHA256). No drift; no reread required.
- Claim-defense doctrine status confirmed `OWNER_SIGNED_OPERATIVE` (signed
  2026-06-11) by full read — not regressed, so the lane's block condition did
  not fire.
- Full reads: thesis, wedge, claim-defense doctrine. Targeted reads: offer
  hypothesis, buyer-proof packet, proof-lead charter, both batch-0 discovery
  artifacts (headers/banners), target-selection brief, customer-discovery
  prompt (header/banner), pricing-first wedge record (full), turn_08 thesis
  (status/header), evidence ladder (claim tiers), overlay files (README,
  source-of-truth, source-loading, decision-routing, validation-gates,
  communication-style, artifact-folders, retrieval-metadata, product-proof).
  Available-not-read (per commission): batch-1 ledger body, screen ledgers,
  probe/projection branch artifacts — statuses consumed via the thesis
  evidence table and the commission's verified capsule.

## Verdict (the one-line answer)

**Nothing found blocks asks 1-2 semantically.** No subordinate artifact or
named lane record contradicts the thesis center or the wedge ordering. One
stale status line inside the thesis itself (F-01) should be fixed in the same
edit that flips its status — prepared in the runbook. Everything else is
either already-prepared cascade work or out-of-cascade hygiene owned
elsewhere. The owner can ratify in one sitting; the runbook makes the
mechanical pass one continuous checklist.

## Findings

| ID | Finding | Class | Disposition |
| --- | --- | --- | --- |
| F-01 | Thesis line ~119 ("Strategic Center") still says the claim-defense doctrine is "pending sign-off"; it was owner-signed 2026-06-11. The doctrine's own propagation sweep refreshed the thesis's evidence-table cell but missed this prose line (its stale-language search classified the hit as the thesis's own pending status). | Stale status inside an anchor | Fix folded into runbook step 1 (the same edit that flips thesis status). Not re-patched now: the anchor is hash-pinned by the live commission; a pre-ratification edit would invalidate the pins for no decision-relevant gain. Line ~166 "finder frame, pending sign-off" is still true — do not "fix" it. |
| F-02 | The thesis's prepared propagation map misses three overlay surfaces that name turn_08 as the current thesis: `.agents/workflow-overlay/project-authority.md` (line ~11), `.agents/workflow-overlay/artifact-roles.md` (Product thesis authority row), `.agents/workflow-overlay/source-of-truth.md` (Known Source Documents, line ~886). Only `source-loading.md` and the repo map were mapped. | Prepared-map gap | Runbook step 7 adds all three re-points. Without this, post-ratification agents would still be routed to turn_08 as current by three authority surfaces. |
| F-03 | Wedge body parentheticals say the batch-1 ledger and capture recon index are "untracked"; all three cited records (batch-1 ledger, orgmotion discovery note, capture recon index) are now tracked (`git ls-files` 2026-06-11). | Stale point-in-time note | Cosmetic. Optional fold-in at the wedge's ratification edit (runbook step 3); not a blocker. |
| F-04 | Two LIVE discovery instruments remain hard-gated to the pricing wedge: `docs/product/product_lead/orca_discovery_batch_0_target_selection_brief_v0.md` and `docs/prompts/product-planning/orca_product_proof_lead_customer_discovery_prompt_v0.md`. Already flagged by pricing-first propagation AR-01 as blocking surfaces; the consumer-demand wedge makes them doubly stale. | Live instrument misroute risk | Realign-or-retire is owner-owned (wedge cascade P2). This lane drafted a successor target-selection brief (PROPOSED) and recommends RETIRE-with-banner for both at ratification. The discovery-prompt revision is outside this lane's write scope (`docs/prompts/` is not in the commissioned edit permission) — runbook routes it to a prompt-orchestration lane or hygiene queue row. |
| F-05 | Batch-0 qualification prep (Sentry/Clerk) and candidate-context scan already carry SUPERSEDED/OFF-TARGET banners pointing at pricing-first as current authority. After ratification those pointers resolve by one extra hop through pricing-first's new supersession banner. | Chain-resolved pointer | No required edit; supersession chains are the repo's existing pattern (break-in-first resolves the same way). Optional P3 pointer refresh only if the owner wants flat pointers. |
| F-06 | Product-lead docs' `open_next`/body pointers use pre-migration flat paths (`docs/product/orca_*` instead of `docs/product/product_lead/orca_*`). | Pre-existing path drift | Out of cascade scope — owned by the Phase-2 repo-structure migration package (`docs/migration/repo_structure_phase2_consolidation_v0/`). Deliberately NOT folded into ratification day (scope guard). |
| F-07 | Offer hypothesis (`PROVISIONAL_LOCK_OFFER_HYPOTHESIS_V0`), buyer-proof packet (`PROPOSED_BUYER_PROOF_PACKET_V0`), and proof-lead charter (`PROPOSED_PRODUCT_PROOF_CHARTER_V0`) are all pinned to pricing-first via 2026-06-08 refinement banners. | Expected pre-ratification state | Not a contradiction: pricing-first IS the current wedge authority until the owner signs. Covered by the wedge's prepared cascade plus this lane's PROPOSED revision drafts (see receipts in the closeout). |
| F-08 | Claim-defense Row-1 wording sweep over the thesis and wedge: externally-shaped sentences carry tier labels; "built to / proven at" used conditionally and correctly; backtest-publishing language matches the approved Row-1 sentence shape (pre-declared ledgers, misses included, retro-known disclosed); no attainment-reading phrase found; no "sealed/out-of-sample" claim found. | Compliant | No action. Any NEW externally-shaped draft (including this lane's) must re-check against Row 1 — the drafts below carry that boundary inline. |
| F-09 | Pricing-first's `direction_change_propagation_blocker` remains open by its own terms: the three product docs got their refinement banners (2026-06-08 cascade, adjudicated), but AR-01's two discovery instruments were added as blocking surfaces and remain unrealigned (F-04). | Open blocker on the outgoing lock | The consumer-demand ratification supersedes pricing-first as first proof; the runbook's supersession banner notes the blocker as closed-by-supersession EXCEPT the instrument realignment, which transfers to the new wedge's cascade (F-04 disposition). |

## What Blocks Asks 1-2 Versus What The Cascade Covers

- Blocks ratification: nothing found.
- Fix-with-ratification (same edit, no extra pass): F-01.
- Prepared-cascade work (already mapped by the anchors, now sequenced in the
  runbook): status flips, turn_08 banner, pricing-first banner, subordinate
  refresh adoption, overlay re-points (including the three F-02 additions),
  repo-map refresh, DCP receipt.
- Deferred-by-design with owner-visible routing: skill copies (P2,
  authorized skill-edit lane), discovery-prompt realignment (prompt lane),
  F-05/F-06 hygiene.

## Claim-Tier Classification (inline, per the evidence ladder)

This report and the lane's drafts are design / product-learning-tier inputs.
They make no proof, readiness, validation, scoring, fixture, blind-use, or
judgment-quality claim; for any such claim the applicable closeout state is
`no_durable_evidence`. The weakest-cleared-gate rule caps everything here at
`product_learning` or below.

## Non-Claims

Advisory sweep only. Not ratification, not acceptance, not validation, not
review-lane output, not a patch queue, not readiness. Findings are
repo-visible-evidence observations as of 2026-06-11 on the pinned commit;
they do not bind the owner, amend any artifact, or authorize execution.
