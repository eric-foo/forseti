# Handoff Packet — Demand-Gate Live Apply + Gate-Run Commission Criteria (Task 2)

```yaml
retrieval_header_version: 1
artifact_role: Handoff packet (cold cross-lane state transfer; workflow-handoff output)
scope: >
  Transfers the demand-gate continuation (Task 2) to a fresh lane off origin/main:
  the OWNER-GATED live apply of the ratified P2/P3/P4 Demand-Substrate Hard Gate
  amendments into the live buyer-proof packet + discovery brief, then the design of
  the gate-run commission criteria (scan -> gate-run -> filled discovery slot).
  Cold-reader self-contained; confirm-don't-trust load contract. The sender lane
  (ecr-sp3-timing-deriver-slice1) is being retired.
use_when:
  - Picking up the demand-gate live apply + gate-run commission criteria in a fresh lane off origin/main.
authority_boundary: retrieval_only
applied_contract: authored via workflow-handoff (packet owner); courier prompt deferred to workflow-prompt-orchestrator.
source_loading_mode: repo-overlay-bound (.agents/workflow-overlay/ + AGENTS.md)
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-14
- created_by_lane: Orca demand-gate (sender) thread on `ecr-sp3-timing-deriver-slice1` (Claude Opus-class); provenance only, NOT authority
- workspace: C:\Users\vmon7\Desktop\projects\orca
- handoff_path: docs/prompts/handoffs/demand_gate_live_apply_and_commission_criteria_handoff_v0.md
- expected_branch: the fresh lane must create its OWN worktree/branch off `origin/main` (per AGENTS isolation) — do NOT continue on the sender's `ecr-sp3-timing-deriver-slice1` (stale, being retired).
- expected_head: `origin/main` @ `1b6660c` (as of 2026-06-14). Advance is expected and fine — rebind to current `origin/main`; the load-bearing facts below carry blob OIDs, not a head pin.
- expected_dirty_state_including_handoff_file: in the SENDER working tree this handoff file is newly UNTRACKED (and the sender lane is being retired, so this file must be landed to `main` or carried into the fresh lane to survive — see Blockers). The fresh lane starts clean off `origin/main`.
- load_rule: confirm-don't-trust — re-verify every load-bearing fact via `git rev-parse origin/main:<path>` against the recorded blob OID before acting; sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: >
    Orca's durable-vs-hollow consumer-demand calls become trustworthy enough that a
    decision owner allocates (and eventually pays) against them on an inherently
    manipulable public substrate — trust earned by method, not asserted; the
    Demand-Substrate Hard Gate is the admissibility front-door that makes it possible.
- anchor_goal: >
    The ratified P2/P3/P4 gate logic is LIVE in the real buyer-proof packet + discovery
    brief (not a PROPOSED proposal), AND a defined runnable gate-run commission shape
    (scan -> gate-run -> filled discovery slot) exists so a candidate can be taken
    through the gate.
- success_signal:
  - core_success:
    - owner_observable: live buyer-proof packet (G1/G2) + brief (qual-#3 + slot column) carry the ratified wording; a `direction_change_propagation` receipt records it; a gate-run commission-criteria artifact exists.
    - output_fit: applied text faithfully matches the ratified proposal (transcription, NOT re-authoring); the gate is enforceable (determinate admit/hold/fail + verb-tiered ceiling); the criteria make a gate-run executable.
    - boundary: NOT merely merging #74 / landing the proposal doc to main (that is prerequisite plumbing — and is now DONE); no scoring engine; no reopening P2/P3/P4.
    - drift_cue: re-debating ratified decisions instead of transcribing them; the commission-criteria design becoming an automated scoring engine; treating "#74 merged" as the win; the apply ballooning beyond G1/G2/brief.
  - secondary_success_signals:
    - taxonomy retail=org-motion confirmed (cited, likely no edit)
    - apply isolated to a fresh lane off origin/main with a clean DCP receipt
- status: user_stated

## Open Decision / Fork

- decision: **Apply scope boundary — transcribe-only vs transcribe-and-reconcile.**
  - options:
    - (a) Strictly TRANSCRIBE the ratified P2/P3/P4 amendment wording (Amendments ①/②/③ in the proposal) into the gate's G1/G2 + brief, touching nothing else.
    - (b) Transcribe AND RECONCILE adjacent live wording the amendments render inconsistent — specifically the old "at least two independent venue families" sentences elsewhere in the buyer-proof packet (around lines ~114 and ~141; quoted in the source ledger), which contradict the new G1 verb-tiered/de-correlation logic once applied.
  - already constrained / off the table: the amendment wording itself is ratified — neither option re-authors it (Drift Guard). No scoring engine in either option.
  - trade-offs: (a) smallest diff, but leaves the instrument internally contradictory (old "≥2 families" prose sitting beside the new verb-tiered G1); (b) coherent instrument, but a wider diff that touches sentences outside the three named amendment slots.
  - owner of the call: **owner** (the apply is owner-gated). The receiving lane weighs it, owner signs off.
  - recommendation: **(b) reconcile** — leaving contradictory wording in the same live instrument defeats faithful application and would mislead an operator running the gate. Flagged as an owner decision because it widens the diff beyond the three named slots.

## Drift Guard

- **No scoring engine.** Weighting stays LLM-in-session / qualitative; numeric/automated scoring is deferred until the owner explicitly lifts the boundary. The gate-run commission criteria design must not become an automated scoring/weighting pipeline.
  - why it matters: the buyer-proof packet forbids automated scoring at this stage; building one is the primary drift.
- **Do not reopen or re-litigate the ratified decisions.** P2/P3/P4 are owner-RATIFIED (2026-06-13); the cross-vendor review findings AR-01..07 are closed + same-vendor recheck-cleared. This lane APPLIES them; it does not reopen them.
  - why it matters: re-debating settled doctrine burns the lane and risks drift from the ratified wording.
- **Faithful transcription, not re-authoring.** The apply moves the ratified encoding verbatim into the live instruments; it does not improve, reword, or extend the gate logic.
- **DCP receipt required.** This is a doctrine change to a live instrument, so it carries a `direction_change_propagation` receipt (per the overlay's source-of-truth / DCP doctrine).
- **Isolation.** Fresh worktree/branch off `origin/main`; never the retiring `ecr-sp3-timing-deriver-slice1` branch.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/` (read `AGENTS.md` + `.agents/workflow-overlay/README.md` FIRST, per AGENTS; the overlay owns source precedence, the DCP contract, and artifact-folder rules).
- targets to enter the ladder (all now on `origin/main`):
  - docs/product/product_lead/orca_demand_gate_definition_closures_proposal_v0.md (the ratified amendment wording — APPLY AUTHORITY)
  - docs/product/product_lead/orca_buyer_proof_packet_v0.md (apply target — Demand-Substrate Hard Gate)
  - docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md (apply target — qual #3 + slot column)
  - docs/product/product_lead/orca_demand_read_taxonomy_v0.md (ripple — retail=org-motion)
- already loaded (weak orientation, freshness-marked; NOT authority): all of the above were read/produced in the sender thread on 2026-06-13/14; treat as stale pointers and re-read fresh.
- must load first (before any strict/actionable step): AGENTS.md + overlay README; then the proposal (wording authority) + the two apply targets.
- load rule: re-run progressive source loading per the overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- **The P2/P3/P4 amendments (what gets applied).** Gist: G1 independence = de-correlation by origination (no shared origination ancestry; laundered/coordinated siblings collapse to one family), verb-tiered by commitment (1 origin → hold/low-commitment incl. cheap defends; ≥2 independent origins → any material/irreversible commitment incl. costly defend); retail presence = G4 org-motion corroboration, EXCLUDED from the G1 demand-family count. G2 floor = ≥1 **gradeable** costly-behavior instance (attributable to buyer actions / direction+magnitude / corroborable), evidenced in ≥1 qualifying family, distinguishable from attention; manipulated sentiment admissible as input, costly behavior clears the floor, divergence caps the ceiling + a defeater clause. Brief: qual objective #3 reworded + slot-table column header.
  - decided in: docs/product/product_lead/orca_demand_gate_definition_closures_proposal_v0.md (Amendments ①G1 / ②G2 / ③brief).
  - compare target: blob OID `3237df285fd8fd1718306a8ad52381a8f2a9a1f0` on origin/main; reread-required.
  - verify before: any apply edit.
- **DLF-01 — single-instance interim floor accepted.** Gist: one gradeable costly-behavior instance is the interim G2 floor (numeric threshold deferred to "P4-B"); owner-accepted because verb-tiering bounds the risk (a single instance earns only hold/low-commitment).
  - decided in: the proposal's "Owner decision (2026-06-13): ACCEPTED" + the review report's DLF-01.
  - compare target: review report blob OID `05c7a1c538a684e9e2a2c3ae51b99124a31e34ec` on origin/main; reread-required.
  - verify before: relying on the single-instance floor in the apply.

## Active Objective

In a fresh lane off `origin/main`: perform the OWNER-GATED live apply of the ratified P2/P3/P4 Demand-Substrate Hard Gate amendments into the live buyer-proof packet + discovery brief (with a `direction_change_propagation` receipt), then DESIGN the gate-run commission criteria (scan -> gate-run -> filled discovery slot). The live instruments currently still carry the OLD pre-amendment wording — the apply has NOT happened.

## Exact Next Authorized Action

1. Create a fresh worktree/branch off `origin/main` (AGENTS isolation; NOT `ecr-sp3-timing-deriver-slice1`). Read `AGENTS.md` + `.agents/workflow-overlay/README.md`.
2. Re-verify the source ledger blob OIDs (proposal, buyer-proof packet, brief, taxonomy) via `git rev-parse origin/main:<path>` against the recorded compare targets; reread the proposal's Amendments ①/②/③ as the wording authority.
3. Resolve the Open Decision (transcribe-only vs reconcile) and obtain the owner's go (the apply is owner-gated).
4. LIVE APPLY: transcribe the ratified wording into `orca_buyer_proof_packet_v0.md` (Demand-Substrate Hard Gate G1 + G2) and `orca_discovery_consumer_demand_target_selection_brief_v0.md` (qual objective #3 + slot-table column); confirm `orca_demand_read_taxonomy_v0.md` already states retail=org-motion (cite, likely no edit); record a `direction_change_propagation` receipt per the overlay.
5. Then DESIGN the gate-run commission criteria (scan -> gate-run -> filled discovery slot), operationalizing qualification objective #3.
6. Stop condition: live instruments carry the ratified logic faithfully + DCP receipt recorded + a commission-criteria artifact exists; no scoring engine; ratified decisions not reopened. Land via the per-lane PR flow.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` (+ `CLAUDE.md` shim) — reread-required.
- Overlay authority: `.agents/workflow-overlay/` (README, source-loading, source-of-truth/DCP, decision-routing) — reread-required.
- User constraints: apply is owner-gated; no scoring engine; faithful transcription; DCP receipt; don't reopen ratified P2/P3/P4; retail=G4 not G1; isolation off origin/main.
- Source-read ledger:
  - `docs/product/product_lead/orca_demand_gate_definition_closures_proposal_v0.md`
    - Role: APPLY AUTHORITY — the ratified amendment wording (Amendments ①G1/②G2/③brief). Status DECISIONS_RATIFIED_ENCODING_RECHECK_CLEARED.
    - Load-bearing: yes
    - Compare target: blob OID `3237df285fd8fd1718306a8ad52381a8f2a9a1f0` (origin/main @ 1b6660c). Re-derive: `git rev-parse origin/main:docs/product/product_lead/orca_demand_gate_definition_closures_proposal_v0.md`.
    - Last checked: 2026-06-14
    - Reuse rule: reread; this is the wording source of truth for the apply. Now on main (was on PR #74, which has MERGED).
  - `docs/product/product_lead/orca_buyer_proof_packet_v0.md`
    - Role: APPLY TARGET 1 — Demand-Substrate Hard Gate G1 + G2. Currently OLD wording (apply not done).
    - Load-bearing: yes
    - Compare target: blob OID `89b4caef90e17b2ae1af96bc847149d53b9d19d2` (origin/main @ 1b6660c). Old-wording anchor to grep: "A qualified read requires demand signal from **AT LEAST TWO independent venue families** (review surfaces; forums/community; search interest; retail presence)" and the fused-minimum sentence "fewer than two clean-enough venue families".
    - Last checked: 2026-06-14
    - Reuse rule: reread before apply; this is the instrument to edit.
  - `docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md`
    - Role: APPLY TARGET 2 — qualification objective #3 + slot-table column. Old wording.
    - Load-bearing: yes
    - Compare target: blob OID `9ed87c8852f64ca49f5a8653e66be2bb3ef79d61` (origin/main @ 1b6660c).
    - Last checked: 2026-06-14
    - Reuse rule: reread before apply.
  - `docs/product/product_lead/orca_demand_read_taxonomy_v0.md`
    - Role: RIPPLE — retail=org-motion confirmation (cite; expected no edit).
    - Load-bearing: yes (for the cite claim)
    - Compare target: blob OID `94b34f4b3e8add3ee86bc43f54786375c43e45e3` (origin/main @ 1b6660c).
    - Last checked: 2026-06-14
    - Reuse rule: confirm against live text before claiming "already states it."
  - `docs/review-outputs/adversarial-artifact-reviews/demand_gate_definition_closures_cross_vendor_adversarial_artifact_review_v0.md`
    - Role: PROVENANCE — the cross-vendor review (GPT-5; 7 findings accepted) + adjudication + recheck + DLF-01.
    - Load-bearing: no (reference; the findings are already closed and folded into the proposal)
    - Compare target: blob OID `05c7a1c538a684e9e2a2c3ae51b99124a31e34ec` (origin/main @ 1b6660c).
    - Last checked: 2026-06-14
    - Reuse rule: reference only; do not reopen closed findings.
- Source gaps: none material — all load-bearing sources are now on `origin/main` (post #74 merge). This handoff file itself is untracked on the retiring sender lane until landed (see Blockers).
- Strict-only blockers: the live apply is a doctrine change → needs owner go + DCP receipt.
- Not-proven boundaries: nothing applied/validated yet; the proposal is PROPOSED until the live instruments carry the wording.

## Current Task State

- Completed: P2/P3/P4 ratified; cross-vendor review (gpt-5, 7 findings) all accepted + fixes applied; same-vendor recheck cleared; proposal + review LANDED to origin/main via PR #74 (MERGED).
- Partially completed: nothing started on the live apply or the commission criteria.
- Broken or uncertain: the Open Decision (transcribe vs reconcile) is unresolved; owner go for the apply not yet given.

## Workspace State

- Branch: sender on `ecr-sp3-timing-deriver-slice1` (being retired); the fresh lane should be off `origin/main`.
- Head: `origin/main` @ `1b6660c` (2026-06-14; expect advance).
- Dirty/untracked before handoff (sender tree): pre-existing multi-lane dirt + this Task-2 work; not relevant to the fresh lane.
- Dirty/untracked after writing this handoff file: this file is newly untracked in the sender tree.
- Target files/artifacts: the two apply targets above (currently unedited) + a new commission-criteria artifact (to author) + a DCP receipt.
- Related worktrees/branches: `orca-judgment-read-machinery-wt` (branch `judgment-spine-read-machinery-architecture-v0`) holds Task 1 (read-machinery architecture, DONE) — it CONSUMES this gate (INV-6), does not do this work. Do not conflate.

## Changed / Inspected / Tested Files

- `docs/product/product_lead/orca_buyer_proof_packet_v0.md` — APPLY TARGET, not yet changed (still old wording).
- `docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md` — APPLY TARGET, not yet changed.
- `docs/product/product_lead/orca_demand_gate_definition_closures_proposal_v0.md` — the wording authority (read-only here).
- Live instruments NOT yet amended (apply pending owner go).

## Frozen Decisions

- P2/P3/P4 demand-gate decisions: owner-RATIFIED 2026-06-13. Do not reopen.
  - Evidence: proposal status DECISIONS_RATIFIED_ENCODING_RECHECK_CLEARED.
  - Consequence: the apply transcribes them; it does not re-derive whether to have them.
- Review findings AR-01..07: closed + same-vendor recheck-cleared. Do not re-litigate.
- DLF-01: single-instance interim G2 floor owner-ACCEPTED (numeric deferred to P4-B).
- No scoring engine (LLM-in-session, qualitative). Retail presence = G4 org-motion, NOT a G1 demand family.

## Mutable Questions

- The Open Decision (transcribe-only vs reconcile adjacent stale wording) — resolves on owner sign-off.
- Gate-run commission criteria shape (scan -> gate-run -> filled slot) — to DESIGN after the apply.

## Superseded / Dangerous-To-Reuse Context

- "Proposal not on main / get it from PR #74 branch / merge #74 first."
  - Why stale: PR #74 has MERGED; the proposal + review are now on `origin/main`.
  - Current replacement: read the proposal/review from `origin/main` (blob OIDs in the ledger).
- Commission #1 — the demand-substrate-gate **paper-check** (`demand_substrate_gate_paper_check_commission_prompt_v0.md`, worktree `orca-gate-paper-check-wt`).
  - Why dangerous: SEPARATE, completed work unit (a paper test of the gate) — NOT this apply. Do not conflate.
  - Current replacement: this lane is the live apply + commission criteria.
- Task 1 — the one-core-two-shells read-machinery architecture (`judgment_spine_demand_read_machinery_architecture_v0.md`).
  - Why dangerous: a different, DONE lane that CONSUMES this gate; it is not this work.

## Commands And Verification Evidence

- Re-derive any source ledger compare target (receiver confirm-don't-trust):
  ```bash
  git rev-parse origin/main:docs/product/product_lead/orca_demand_gate_definition_closures_proposal_v0.md
  # expect 3237df285fd8fd1718306a8ad52381a8f2a9a1f0 (or a newer OID if the proposal was amended — reread it)
  ```
- Confirm the apply has NOT happened (live packet still old wording):
  ```bash
  git show origin/main:docs/product/product_lead/orca_buyer_proof_packet_v0.md | grep -i "at least two independent venue"
  # a hit means the OLD wording is still live; the apply is owed.
  ```
- No build/test commands — docs-only lane.

## Blockers And Risks

- The live apply is OWNER-GATED.
  - Evidence: doctrine change to the buyer-proof packet (Demand-Substrate Hard Gate).
  - Likely next action: resolve the Open Decision, get owner go, apply off origin/main with a DCP receipt.
- This handoff file is untracked on the retiring sender lane.
  - Evidence: written to the `ecr-sp3-timing-deriver-slice1` working tree as a new untracked file; that lane is being retired.
  - Likely next action: land this packet to `origin/main` (focused PR, like #74) or carry it into the fresh lane, so it survives sender-lane retirement.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: current `origin/main` head (expect ≥ 1b6660c); the four load-bearing source blob OIDs via `git rev-parse origin/main:<path>`; that the buyer-proof packet still shows old wording (else the apply may already be in progress elsewhere — reconcile).
- Compare targets: the blob OIDs in the ledger; `reread-required` entries must be re-read.
- Load outcomes: REUSE only if the proposal + apply targets re-verify and the apply is still owed; STALE_REREAD_REQUIRED if any blob OID moved (reread that file); BLOCKED_DRIFT if the live packet was already partly amended by another lane; BLOCKED_UNVERIFIABLE if a load-bearing source can't be obtained from main.
- Sources to reread if drift: the proposal (wording authority) + the two apply targets.

## Do Not Forget

- The apply transcribes RATIFIED wording — do not re-author, and do not reopen P2/P3/P4 or the closed AR findings.
- The single most expensive mistake here is building a scoring engine; keep weighting LLM-in-session / qualitative until the owner lifts the boundary.
- "#74 merged" is plumbing, not the goal — success is the LIVE instruments carrying the ratified logic + the commission criteria designed.
