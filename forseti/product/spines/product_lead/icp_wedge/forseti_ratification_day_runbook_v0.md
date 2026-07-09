  Consumer-Demand Ratification-Day Runbook v0 (PROPOSED)

```yaml
retrieval_header_version: 1
artifact_role: Product-planning lane runbook (prepared one-pass cascade checklist)
scope: >
  Executable one-pass checklist for the turn in which the owner ratifies the
  consumer-demand thesis (ask 1) and co-ratifies the wedge (ask 2): status
  flips, supersession banners, subordinate-revision adoption, overlay
  re-points, repo-map refresh, and the owed direction_change_propagation
  receipt (trigger: product_doctrine). Prep-only until the owner's word
  exists; the ratifying turn executes it.
use_when:
  - The owner has just ratified thesis asks 1-2 (or ask 1 alone — see Branches).
  - Verifying post-ratification that no live surface still routes to the superseded thesis or wedge.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_product_thesis_consumer_demand_v0.md
  - docs/decisions/forseti_icp_wedge_consumer_demand_first_v0.md
  - forseti/product/spines/product_lead/icp_wedge/forseti_icp_ratification_readiness_report_v0.md     findings F-01..F-09 referenced below
input_hashes:
    Anchors (must match before executing; on mismatch STOP and re-anchor)
  docs/decisions/orca_product_thesis_consumer_demand_v0.md: 5FEA48AE8B0C0E22D24CE2194F1F17617C5C94D2C75A204AAD5CD8CC149B2B0E
  docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md: C878ABEBBFFC119A032E0290E093A9EBB973BC15052B4B21FA59D285AB83C07B
    Cascade targets as pinned at prep (2026-06-11); on mismatch reread the target, then adapt the step
  docs/decisions/turn_08_product_thesis_v0.md: 822653A241CF84675A3F07F695BA0ED3BFACC230F7F13AA47A4649B5DB2CD7E6
  docs/decisions/orca_icp_wedge_pricing_first_v0.md: F4E678315C7EB2EF1E7F823699251F358F4920CE2FE3B36C3C8F1B9C43CF7B0B
  forseti/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md: 74E7868365F73AD95FE2119C2EBFD71ED3C7BBB78996DC34058E67B951FBFF6A
  forseti/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md: 62077848E7F43F246D93009DDDF4859E274EB57754073D6F6EC66DFCD374315A
  forseti/product/spines/product_lead/proof_charter/orca_product_proof_lead_charter_v0.md: 3B52F4599635C61748F505BCDC012CCC96195F88D9B9D6CAC55BE9734F714B6E
  forseti/product/spines/product_lead/icp_wedge/orca_discovery_batch_0_target_selection_brief_v0.md: 0DF04180A94A6E2A1583B47DB14638B6CEB28759D8008E321B7C715BFD165429
branch_or_commit: ecr-sp3-timing-deriver-slice1 @ 48c00ca (concurrent lanes commit freely; re-verify pins on execution day)
stale_if:
  - The owner amends (rather than ratifies) the thesis or wedge — STOP; re-anchor; this runbook is void as written.
  - Any pinned target drifts and the drift is more than additive (reread, re-derive the affected step).
```

   Status

`EXECUTED_2026-06-12` — the owner ratified asks 1-4 in-thread 2026-06-12
(verbatim words: Owner Decision Record in
`docs/decisions/forseti_consumer_demand_ratification_decision_memo_v0.md`) and
the cascade ran the same turn. Execution deviations from the prepared text
(recorded, not silent):

- The "owner amends" branch fired for ask 1 (measured-ToS-risk capture
  posture). Per that branch, the amendment was folded inline: the thesis
  Product Boundary capture bullet was restated, and the applied subordinate
  revisions replaced their drafted "never depend on a ToS-violating source"
  absolutism with the capture-lane-bound-routes / absurd-level-rejected
  form. Re-derivation happened at application; the revision packages record
  their own deviations.
- Step 5 additionally re-targeted two offer-hypothesis sections the package
  under-scoped (handbook-audit "Specific buyer" cell; Recommendation wedge
  paragraphs) — both still carried the pricing wedge as current.
- Step 6: the successor brief was adopted and the batch-0 brief
  superseded-bannered as prepared; the customer-discovery prompt was queued
  as ORCA-HYGIENE-018.
- Step 7 also included the repo map's stale fourth product-anchor row (the
  twice-superseded `forseti_product_lead_first_icp_wedge_decision_v0.md` row)
  and the "Offer Or Buyer Proof Work" list — re-pointed to the ratified
  records.
- Step 8: the repo map was clean at execution; per the repo's write-boundary
  hook it was committed explicit-path immediately (`7be854d`, repo map only).
- Step 9: skill copies queued as ORCA-HYGIENE-019.
- Step 10: the executed receipt lives in the thesis record ("Doctrine-Change
  Propagation — Executed"); the wedge record points to it.

Prepared 2026-06-11 as `PROPOSED_PENDING_OWNER_RATIFICATION`; the checklist
below is retained as prepared (deviations above govern where they differ).

   Preconditions (all required before step 1)

1. Owner's recorded word ratifying thesis ask 1 (and ask 2 for the full
   pass), in-thread, quotable. Asks 3 (probe gate) and 4 (outreach posture)
   are recorded as given but execute in their own lanes — see Branches.
2. Fresh hash check of the two anchors against the pins above. Mismatch =
   STOP (the owner may be signing text this runbook was not prepared for).
3. Fresh `orca_start_preflight` for the ratifying turn (docs-write;
   dirty-state checked; this is doctrine-changing work — the DCP receipt in
   step 10 is owed at its closeout).
4. Repo state: note which cascade targets are dirty/untracked from other
   lanes; coordinate, do not clobber (especially `docs/workflows/orca_repo_map_v0.md`).

   One-Pass Checklist

Execute in order. Each step names the file, the edit, and its check.

**Step 1 — Thesis record** (`docs/decisions/forseti_product_thesis_consumer_demand_v0.md`)
- Status section: `PROPOSED_PENDING_OWNER_SIGNOFF` → `OWNER_LOCKED`, with the
  sign-off date and the owner's recorded words (dated amendment style, no
  silent rewrite).
- Retrieval header: add `supersedes: [docs/decisions/turn_08_product_thesis_v0.md]`;
  drop the now-consumed "Owner ratifies, amends, or rejects" stale_if line in
  favor of the live falsifier lines.
- F-01 fix (same edit): Strategic Center line ~119 "claim-defense doctrine,
  pending sign-off" → "claim-defense doctrine, owner-signed 2026-06-11".
  Do NOT touch line ~166 ("finder frame, pending sign-off") — still true
  unless the owner also signs the finder frame today.
- Check: `rg -n "PROPOSED_PENDING_OWNER_SIGNOFF|pending sign-off" docs/decisions/forseti_product_thesis_consumer_demand_v0.md`
  returns only the finder-frame line and historical Status prose if retained.

**Step 2 — turn_08 supersession banner** (`docs/decisions/turn_08_product_thesis_v0.md`)
- Add `superseded_by: docs/decisions/forseti_product_thesis_consumer_demand_v0.md`
  (header or top banner, matching the repo's existing supersession pattern)
  plus this banner directly under the H1:

  > **SUPERSEDED (date of ratification)**
  > This thesis is superseded as the controlling product thesis by
  > `docs/decisions/forseti_product_thesis_consumer_demand_v0.md`
  > (consumer-demand decision intelligence; beauty first vertical), ratified
  > by the owner. Retained as history; carried-forward elements are listed in
  > that record's "Carried From Thesis v0 / Changed" section. Do not anchor
  > new product, capture, judgment, or proof lanes here.

- Check: `rg -n "superseded_by|SUPERSEDED" docs/decisions/turn_08_product_thesis_v0.md` hits the banner.

**Step 3 — Wedge record** (`docs/decisions/forseti_icp_wedge_consumer_demand_first_v0.md`) — full pass only
- Status: `PROPOSED_PENDING_OWNER_SIGNOFF` → `OWNER_LOCKED_DIRECTION`, dated,
  owner words quoted.
- Header: add `supersedes: [docs/decisions/forseti_icp_wedge_pricing_first_v0.md]`.
- Optional fold-in (F-03, cosmetic): update the two "untracked" parentheticals
  (batch-1 ledger, capture recon index) — all three cited records are tracked
  as of 2026-06-11.
- Check: status string flipped; `supersedes` present.

**Step 4 — Pricing-first supersession banner** (`docs/decisions/forseti_icp_wedge_pricing_first_v0.md`)
- Add `superseded_by: docs/decisions/forseti_icp_wedge_consumer_demand_first_v0.md`
  and this banner under the H1 (mirrors the break-in banner pattern):

  > **SUPERSEDED AS FIRST-PROOF WEDGE (date of ratification)**
  > The first-proof wedge moves to beauty consumer-demand
  > (`docs/decisions/forseti_icp_wedge_consumer_demand_first_v0.md`, owner-ratified).
  > Pricing-first is RETAINED as (a) an engine application reachable from the
  > same spine, (b) the two RETRO SaaS dev cases as cross-vertical method
  > anchors, and (c) the default re-entry candidate if the beauty wedge kills
  > under the buyer-proof packet's criteria — re-evaluated against this
  > record's own `stale_if` (beachhead-window maturity). The SUGGESTED
  > pricing-as-sensitivity-read block below remains a non-frozen historical
  > suggestion inside a superseded record. This record's open
  > `direction_change_propagation_blocker` is closed by supersession EXCEPT
  > the two discovery instruments (AR-01), whose realignment transfers to the
  > consumer-demand cascade (runbook step 6).

- Check: banner present; no other body text rewritten (review records and
  historical reasoning are never retro-edited).

**Step 5 — Adopt the three subordinate revision packages** (full pass only)
- Completed 2026-06-12. The applied live targets are:
  - `forseti/product/spines/product_lead/offer/forseti_offer_hypothesis_v0.md`
  - `forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md`
  - `forseti/product/spines/product_lead/proof_charter/forseti_product_proof_lead_charter_v0.md`
- Applied packages are consumed prep, not live authority; after reverse-ref and
  deletion-evidence checks, they may be deleted.
- Check: each live doc's banner names the consumer-demand authorities; no
  live doc still names pricing-first as CURRENT (historical mentions stay).

**Step 6 — Discovery instruments (F-04)** (full pass only)
- Adopt `orca_discovery_consumer_demand_target_selection_brief_v0.md` as the
  live target-selection instrument (status → adopted-label, dated).
- Retire the pricing-gated brief: add a SUPERSEDED/OFF-TARGET banner to
  `orca_discovery_batch_0_target_selection_brief_v0.md` pointing to the
  successor (mirror the batch-0 qualification-prep banner pattern).
- The customer-discovery prompt
  (`docs/prompts/product-planning/orca_product_proof_lead_customer_discovery_prompt_v0.md`)
  is a prompt artifact: route its realignment to a prompt-orchestration lane
  the same day, or add a hygiene-queue row. Until realigned it must not drive
  discovery — say so in the DCP receipt's intentionally_not_updated if
  deferred.

**Step 7 — Overlay re-points (thesis pointer refresh; includes F-02 additions)**
- `.agents/workflow-overlay/source-loading.md` line ~289 (Data Capture Spine
  CA Read Pack): turn_08 path → new thesis path (keep the targeted-sections
  description; its section names map onto the new thesis).
- `.agents/workflow-overlay/project-authority.md` line ~11: "Current product
  thesis source" → new thesis path.
- `.agents/workflow-overlay/artifact-roles.md` "Product thesis authority"
  row: → new thesis path.
- `.agents/workflow-overlay/source-of-truth.md` Known Source Documents line
  ~886: → new thesis path described as current; keep or annotate the turn_08
  entry as superseded-historical.
- Check: `rg -n "turn_08_product_thesis" .agents/workflow-overlay/` returns
  only superseded-historical annotations (and the unrelated
  `turn_08_workflow_bedrock_maximization.md` entry, a name collision — leave it).

**Step 8 — Repo map refresh** (`docs/workflows/orca_repo_map_v0.md`, lines ~428 and ~649)
- Re-point the thesis rows to the new record; annotate turn_08 as superseded.
- Coordinate with any concurrent lane editing the map; if dirty, fold the
  re-point into that lane's edit rather than clobbering.
- Check: `rg -n "turn_08_product_thesis" docs/workflows/orca_repo_map_v0.md`
  shows only the superseded annotation.

**Step 9 — orca-product-lead skill copies (P2; do NOT edit inline)**
- Both `.agents/skills/orca-product-lead/SKILL.md` and
  `.claude/skills/orca-product-lead/SKILL.md` cite turn_08 + pricing-first as
  current. Skill source is governed by
  `.agents/workflow-overlay/skill-adoption.md` (sha-pinned): queue an
  authorized skill-edit lane; record the deferral in the DCP receipt.

**Step 10 — DCP receipt (owed by the ratifying turn; skeleton prepared)**

```yaml
direction_change_propagation:
  doctrine_changed: >
    The controlling Orca product thesis moves to consumer-demand decision
    intelligence (beauty first vertical) and the first-proof wedge moves to
    the beauty operator door, superseding turn_08 and pricing-first;
    subordinate product-lead artifacts re-targeted via the prepared
    consumer-demand revision packages.
  trigger: product_doctrine
  related_triggers: []
  controlling_sources_updated:
    - docs/decisions/forseti_product_thesis_consumer_demand_v0.md
    - docs/decisions/turn_08_product_thesis_v0.md
    - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
    - docs/decisions/orca_icp_wedge_pricing_first_v0.md
    - forseti/product/spines/product_lead/offer/forseti_offer_hypothesis_v0.md
    - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md
    - forseti/product/spines/product_lead/proof_charter/forseti_product_proof_lead_charter_v0.md
    - forseti/product/spines/product_lead/icp_wedge/orca_discovery_consumer_demand_target_selection_brief_v0.md
    - forseti/product/spines/product_lead/icp_wedge/orca_discovery_batch_0_target_selection_brief_v0.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/project-authority.md
    - .agents/workflow-overlay/artifact-roles.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md                                     no wedge/thesis content; routes to overlay — expect no change
    - CLAUDE.md                                     shim — expect no change
    - .agents/workflow-overlay/product-proof.md     wedge-agnostic semantics — expect no change
    - forseti/product/spines/foundation/product_contract/core_spine_v0_product_contract.md    senior frozen contract the thesis sits on — no change
    - forseti/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md    senior; subordination one-way — no change
    - forseti/product/spines/product_lead/proof_charter/forseti_claim_defense_doctrine_v0.md    owner-signed wording policy — no change
    - docs/prompts/product-planning/orca_product_proof_lead_customer_discovery_prompt_v0.md    deferred to prompt lane (step 6)
    - .agents/skills/orca-product-lead/SKILL.md     deferred to skill-edit lane (step 9)
    - .claude/skills/orca-product-lead/SKILL.md     deferred to skill-edit lane (step 9)
  intentionally_not_updated:
    - path: forseti/product/spines/product_lead/icp_wedge/orca_discovery_batch_0_qualification_prep_sentry_clerk_v0.md
      reason: already SUPERSEDED-bannered; pointer resolves via pricing-first's new banner chain (report F-05).
    - path: forseti/product/spines/product_lead/icp_wedge/orca_discovery_batch_0_candidate_context_scan_v0.md
      reason: same chain-resolution as above.
    - path: pre-migration flat paths in product-lead docs' open_next
      reason: owned by the Phase-2 repo-structure migration package (report F-06), not this cascade.
  stale_language_search: >
    rg -in "turn_08_product_thesis|pricing_first|pricing-first|PROPOSED_PENDING_OWNER_SIGNOFF"
    docs/decisions docs/product/product_lead .agents/workflow-overlay docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: "<run after the edits; expected residue: superseded banners, historical reasoning, review records, the finder-frame pending line, and the deferred skill/prompt surfaces named above>"
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not judgment-quality evidence
    - ratification locks a direction; every gated lane keeps its own authorization boundary
```

**Step 11 — Closeout**
- Hygiene-queue rows for the two deferrals (skill-edit lane; discovery-prompt
  realignment) if not executed same-day.
- Chat closeout per `.agents/workflow-overlay/communication-style.md`:
  decision first, then receipts (paths + new hashes + statuses).
- Commit only with the owner's explicit word, and never sweep other lanes'
  files (worktree is shared).

   Branches

- **Owner ratifies ask 1 only (thesis, not wedge):** run steps 1, 2, 7, 8,
  10 (receipt names only the thesis subtree), 11. The wedge stays PROPOSED;
  pricing-first stays the wedge authority; steps 3-6 and the revision
  packages stay inert (they depend on the wedge).
- **Owner ratifies ask 2 only:** invalid as written — the wedge presupposes
  the thesis's ladder shape; surface to the owner instead of executing.
- **Owner amends either anchor:** STOP. Re-anchor the lane on the amended
  text, re-derive affected packages, then re-prepare this runbook's affected
  steps. Amendments are dated; never silently rewrite the anchors.
- **Ask 3 (durability probe gate):** an authorization recorded in the
  decision memo / owner's words — execution belongs to the
  `consumer-demand-probe` lane under its own spec and authorization record;
  no step here builds or runs anything.
- **Ask 4 (outreach posture):** default stays closed; if the owner names an
  opening condition, record it as a dated note on
  `docs/decisions/advisory_proof_slice_definition_v0.md`'s owning gate in its
  own decision record — not silently inside this cascade.

   Claim-Tier Classification

Runbook artifacts are design / product-learning-tier inputs (evidence
ladder); executing this runbook produces propagation evidence only — no step
creates validation, readiness, buyer proof, or judgment-quality evidence.
Closeout state for any such claim: `no_durable_evidence`.

   Non-Claims

Prepared checklist only. Not ratification, not owner consent, not validation,
not readiness, not probe-execution or outreach authority, not a commit/push
instruction. The DCP skeleton is a template the ratifying turn must verify
against reality at execution time — its lists are prepared expectations, not
observed facts, until that turn runs the checks and fills the result fields.
