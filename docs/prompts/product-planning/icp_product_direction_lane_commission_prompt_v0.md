# ICP / Product-Direction Lane — Commission Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Product-planning lane prompt (lane commission)
scope: >
  Commissions the standing ICP / product-direction lane: carry the
  consumer-demand product thesis and the consumer-demand-first ICP wedge to
  ratification-readiness, refresh the subordinate product-lead artifacts as
  PROPOSED drafts consistent with them, and prepare the ratification-day
  cascade — prep-only until the owner ratifies thesis asks 1-2. Anchored on a
  branch-exploration synthesis verified against primary sources 2026-06-11.
use_when:
  - Spinning up (or resuming) the ICP / product-direction lane in a fresh session.
  - Checking what that lane may produce before thesis ratification.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_product_thesis_consumer_demand_v0.md      # anchor 1: the thesis (PROPOSED; 4 owner asks)
  - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md     # anchor 2: the wedge (PROPOSED)
  - forseti/product/spines/product_lead/proof_charter/orca_claim_defense_doctrine_v0.md   # OWNER_SIGNED_OPERATIVE; binds all external wording
  - forseti/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md  # claim caps
input_hashes:
  docs/decisions/orca_product_thesis_consumer_demand_v0.md: 5FEA48AE8B0C0E22D24CE2194F1F17617C5C94D2C75A204AAD5CD8CC149B2B0E
  docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md: C878ABEBBFFC119A032E0290E093A9EBB973BC15052B4B21FA59D285AB83C07B
branch_or_commit: ecr-sp3-timing-deriver-slice1 @ 48c00ca (concurrent lanes commit freely; verify pins on intake)
stale_if:
  - The owner ratifies or amends the thesis or wedge (the lane re-anchors; ratification day runs the prepared cascade instead of this prep commission).
  - The claim-defense doctrine is amended (re-check Row-1 wording before any externally-shaped draft).
```

## Thread Operating Target

`Stand up the ICP / product-direction lane: bring the consumer-demand thesis +
wedge to ratification-readiness with every subordinate product-lead artifact
consistent, and have the ratification-day cascade prepared so the owner's
sign-off is one pass.`

```yaml
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target   # new lane; the commissioning thread was a courier/cleaning thread
  changed_from_input: no
  lifecycle_status: active_from_this_commission
```

Fitness reference (pointer-preferred, per
`docs/decisions/work_unit_fitness_reference_v0.md`): **goal** = a
ratification-ready ICP/product-direction package; **observable success
signal** = the owner can ratify thesis asks 1-2 in one sitting because every
subordinate artifact is consistent (or has its needed amendment named), with
all claims capped per the evidence ladder and claim-defense Row 1.

## Cynefin Routing

Per `.agents/workflow-overlay/decision-routing.md` (run at commissioning,
2026-06-11): regime **Complicated**; layer-based decomposition (anchors →
charter → prep deliverables); bottleneck = owner ratification of asks 1-2;
stop/pivot = owner amends the thesis center, then re-anchor before any
subordinate refresh. Disallowed: self-ratification, probe execution, outreach.
Re-run the router on intake if the trigger conditions have changed.

## Preflight

```text
orca_start_preflight:
  agents_read: required on intake (read fresh; AGENTS.md carries the Mini God Tier trigger since 5fb65db)
  overlay_read: required on intake (.agents/workflow-overlay/README.md)
  source_pack: S2 product anchor + the targeted reads below
  edit_permission: docs-write (docs/product/product_lead/ + docs/decisions/ PROPOSED drafts only)
  target_scope: ICP/product-direction prep package (deliverables 1-4 below)
  dirty_state_checked: required on intake (concurrent lanes share the branch; verify input_hashes; on mismatch reread the anchor before relying on it)
  blocked_if_missing: anchors unreadable, or hash drift the lane cannot re-verify
repo_map_decision: loaded
repo_map_reason: the Product Anchor Files table routes this lane's homes (offer hypothesis, buyer-proof packet, wedge, proof charter, claim-defense doctrine)
doctrine_change: none in this prep commission. Ratification day IS doctrine-changing
  (trigger: product_doctrine) — the thesis carries its own prepared propagation map
  ("Doctrine-Change Propagation — Prepared Map"); the receipt is owed by the
  ratifying turn, not by this lane's prep work.
external_source_boundary: external workflow source is read-only; jb is not Orca authority.
```

## Objective And Intended Decision

Objective: make the consumer-demand product direction ratifiable and the ICP
concrete enough to act on the day it is signed.

Intended decision (owner's, not the lane's): thesis asks 1-4 —
ratify/amend the thesis (1), co-ratify/amend the wedge (2), authorize the
durability probe's next gate (3), set the outreach-gate posture (4).

## Verified State Capsule (2026-06-11, checked against primary sources)

The commissioning thread verified the branch-exploration synthesis. Corrections
applied — trust this capsule over older summaries:

- `consumer-demand-probe` branch: **115 commits ahead of main** (not 138).
  Durability probe spec v2 KEEP-CLEARED; Round-3 cross-vendor (GPT-5.5)
  Stage-2 validity review + 4 patches + bounded recheck (`3247e56`); latest
  status reconciled to recheck-completed / re-kept (`038fe44`). Execution is
  explicitly NOT authorized — that is thesis ask 3, owner-gated.
- `capture-demand-projection` branch: deterministic no-LLM demand-signal
  projection; Ulta adapter live-validated with **43 real observations**
  (`93a4fd1`); three source adapters incl. Apollo embedded-cache (`bf9c316`,
  `3e42ebc`). Design review verdict NEEDS_ARCHITECTURE_PASS (result algebra,
  coordinate identity); the F6+R6 no_repo cross-vendor review + adjudication
  landed on the main working branch (`3d7096f`) as that pass's inputs.
- Doctrine on the main working branch: venue registry REJECTED, shape-C
  procedure **owner-adopted** (not pending); beauty proving screens 1-3 done —
  the **promote-on-reuse trigger fired at screen 3** (card-set decision routed
  to the owner); finder frame still PROPOSED; **claim-defense doctrine
  OWNER_SIGNED_OPERATIVE 2026-06-11** (`cebbfa2`) — Row 1 (product_learning)
  is the only live row; batch-1 backtest ledger BATCH1_ACTIVE_OWNER_SIGNED
  (`2e665de`).
- Core Spine (frozen): costly behavior is the decision-strength primitive;
  "engagement quality remains a rubric, not a primitive"
  (`docs/product/core_spine/core_spine_v0_product_contract.md`).
- Hard source limits (encoded in lane records; thesis evidence table quotes
  them verbatim): TikTok live = ToS NO-GO, archive leg only (pre-2024 window);
  LinkedIn live = policy wall (archive/entitled routes only); Beauty Pie
  org-motion = ATS-led (Greenhouse), not LinkedIn headcount. The thesis
  depends on no live ToS-violating source.

## Source Pack (read on intake; targeted, not bulk)

Full reads (3): the two anchor decisions; the claim-defense doctrine.
Targeted reads: `docs/product/product_lead/orca_offer_hypothesis_v0.md` (core
offer + fit diagnostic), `docs/product/product_lead/orca_buyer_proof_packet_v0.md`
(proof standard, pull signals, disqualifiers),
`.agents/workflow-overlay/product-proof.md` (trust-objection semantics — do
not redefine locally). Available-not-read by default: batch-1 ledger, screen
ledgers, probe/projection branch artifacts (route through the thesis evidence
table; open only when a deliverable depends on one).

Method use follows the Source-Gated Method Contract: REFERENCE-LOAD any
invoked workflow methods first; APPLY only after declaring
`SOURCE_CONTEXT_READY` over the pack above.

## Commission (prep-only deliverables)

1. **Ratification-readiness check.** Sweep thesis + wedge against every
   subordinate product-lead artifact and named lane record for
   contradictions, stale statuses, or wording that violates claim-defense
   Row 1. Output: a short consistency report — what blocks asks 1-2, what
   merely needs the prepared cascade.
2. **Subordinate refresh as PROPOSED drafts.** Where the wedge cascade names
   them (offer hypothesis, buyer-proof packet, proof charter, discovery
   instruments): draft the consumer-demand-first revisions as PROPOSED,
   claim-capped, never ratifying by reference.
3. **Ratification-day runbook.** Turn the thesis's prepared propagation map
   into an executable one-pass checklist (status flips, supersede banner on
   turn_08, overlay re-points, repo-map refresh, DCP receipt
   `trigger: product_doctrine`), so sign-off day is mechanical.
4. **Owner decision memo.** Asks 1-4 restated with the lane's recommendation
   and the cheapest-test framing (ask 3 = the durability probe gate is the
   cheapest direct test of the central read). The memo recommends; it decides
   nothing.

## Hard Constraints

- PREP-ONLY: the lane must not ratify, partially adopt, or treat this
  commission as adoption of the thesis or wedge. Sign-off is the owner's word
  on asks 1-4, nothing less.
- No durability-probe execution (ask 3), no outreach (ask 4 default closed),
  no live-source calls, no capture expansion, no entity-spine build; JSG-01
  stays frozen; batch-1 contestant work belongs to other, outcome-clean
  sessions.
- All externally-shaped wording obeys the claim-defense doctrine Row 1
  allowlist; every results sentence carries its tier label.
- Do not touch the probe/projection branches; consume their state via the
  thesis evidence table and this capsule.
- Never commit another lane's files without the owner's explicit word.

## Output Mode And Contract

`file-write` (docs-write). Deliverables land as PROPOSED artifacts in
`docs/product/product_lead/` (drafts) and, for the decision memo,
`docs/decisions/` or chat per owner preference. Chat closeout: headed human
summary first (recommendation, blockers, next authorized step), then
path/hash/status receipts. New durable artifacts carry retrieval headers per
`.agents/workflow-overlay/retrieval-metadata.md`.

## Validation Gates

- `orca_start_preflight` recorded on intake; input hashes verified (drift →
  reread, then proceed; silent reliance on a drifted anchor is a defect).
- Judgment Spine claim-tier gate for anything proof-adjacent (classify tier +
  closeout state inline; weakest-cleared-gate rule).
- Prompt gates per `.agents/workflow-overlay/prompt-orchestration.md`; this
  commission's verdict at authoring: PASS_WITH_WARNINGS (warning: anchors are
  PROPOSED decisions — strict acceptance claims stay blocked until owner
  ratification; that is by design for a prep lane).

## Assumptions, Unknowns, Blocked Conditions

- Assumes the owner wants ratification-readiness, not a re-derivation of the
  thesis; if intake finds the owner amended the center, stop and re-anchor.
- Unknown: whether ask-2's buyer ladder ordering survives discovery-instrument
  drafting; surface tensions, do not resolve them silently.
- Blocked if: anchors unreadable; claim-defense doctrine status regressed;
  owner word contradicts this commission.

## Non-Claims

Commissions preparation only. Not ratification, not validation, not buyer
proof, not readiness, not probe-execution or outreach authority; ships no
external claim; the verified capsule is orientation evidence, not a substitute
for the lane's own intake reads.
