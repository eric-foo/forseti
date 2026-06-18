# ECR CA — Bounded JSG-01 Unfreeze Build Handoff Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Implementation handoff prompt (docs/prompts/handoffs/; ECR CA lane commission)
scope: >
  Owner-couriered commission of the ECR CA lane to complete the bounded JSG-01
  unfreeze build in four slices: (A) the SP-5 finalizer acting half
  (FinalizationReceipt producer under AR-01's decided authority), (B) the
  EvidenceUnit binding slice bounded to exactly what the JSG-01 predicate
  reads — slice plan, cross-family review, OWNER RATIFICATION STOP, then
  build — (C) the first real case packet carrying SourceCapturePacket ->
  derived SP-1/2/3/6 fields + a valid FinalizationReceipt, and (D) the
  unfreeze decision memo. The unfreeze itself stays the owner's dated act;
  JSG-01 and its conductor stay FROZEN throughout this commission.
use_when:
  - Spinning up (or resuming) the ECR CA lane for the bounded JSG-01 unfreeze build.
  - Checking what that lane may build, what stops for owner ratification, and what stays reserved.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/ecr_spine_submap_v0.md                                    # front door; cross-kind invariants
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md  # ratification records; reserved decisions
  - orca/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md  # the FROZEN conductor; JSG-01 row (~:209) — read, never edit
  - docs/decisions/ar_01_pre_decision_status_finalizer_staffing_v0.md        # SP-5 staffing authority (decided)
input_hashes:
  docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md: 869F41BB516731D7067092C48634E5DE047FC102805F747E9FAE62DEDBB81D6F
  docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md: 28CB338F7208DA848DB70D0B59D33AFE2DC87D96D7DBFA9F2ABF654F8AB0EAC7
  docs/research/judgment-spine/judgment_spine_machinery_build_state_gap_map_v0.md: 5E05686685635AD26E0C7A283707FB380BC91DBF0504CE3976412631B4963488
  orca-harness/schemas/finalization_models.py: 280FFEFB68092FDD37BC78FE785B8ACA78CB7E4BEE86121F54D5123AC8298FCE
  docs/decisions/ar_01_pre_decision_status_finalizer_staffing_v0.md: 85F40F1EC3D6156E282C9DA234467D4FD90FCC48B84DA20BCC8508491F1884A7
branch_or_commit: ecr-sp3-timing-deriver-slice1 @ de479c1 at authoring (concurrent lanes commit freely; hash drift on intake -> reread the drifted source, then proceed)
stale_if:
  - The owner unfreezes JSG-01 (this commission is consumed; the unfreeze decision record supersedes it as the live state).
  - The owner amends the build order, scope, or the EvidenceUnit reservation (re-anchor before continuing).
```

## Authorization Basis (record, verbatim intent)

Owner, in-thread 2026-06-11, after a three-agent verification that JSG-01 is
frozen everywhere with no unfreeze recorded: "okay let's build out the sp5
finalizer, evidence unit, real case packet, then we unfreeze. prompt out for
ECR CA yes." This is the explicit bounded implementation authorization this
handoff carries (AGENTS.md: implementation requires current-turn or
accepted-handoff authorization). It covers slices A-D below and nothing else —
notably NOT the unfreeze itself, NOT the full EvidenceUnit field architecture,
NOT live LLM calls, and NOT any edit to the frozen conductor.

## Thread Operating Target

`Complete the bounded JSG-01 unfreeze build — finalizer acting half,
JSG-01-scoped EvidenceUnit binding, one real case packet carrying fields +
receipt — so the owner's unfreeze word is the only remaining step.`

```yaml
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target   # new lane; commissioned from a courier thread
  changed_from_input: no
  lifecycle_status: active_from_this_commission
```

## Cynefin Routing

Commissioning classification (2026-06-11, per
`.agents/workflow-overlay/decision-routing.md`): regime **Complicated** — the
target is reasoned through from ratified sources (field schema ratified;
staffing decided; conductor predicate explicit); layer-based decomposition in
the slice order below. Bottleneck: the owner ratification stop in slice B.
Riskiest assumption: that the JSG-01-scoped binding slice can stay cleanly
inside the reserved full-EU-architecture boundary — if slice-B planning shows
it cannot, STOP and surface to the owner rather than widening. Re-run the
router on intake.

## Preflight

```text
orca_start_preflight:
  agents_read: required on intake (fresh)
  overlay_read: required on intake (.agents/workflow-overlay/README.md; then review-lanes.md +
    delegated-review-patch.md before commissioning the slice-B cross-family review)
  source_pack: custom — open_next above + the slice plans the submap routes to + orca-harness/{schemas,ecr,signal_content,tests}
  edit_permission: implementation-authorized (bounded to slices A-D; docs-write for plans/memo)
  target_scope: orca-harness (finalizer producer, EU-binding slice, packet assembly, tests) + docs/product/ slice plans + docs/decisions/ memo
  dirty_state_checked: required on intake (multi-lane branch; verify input_hashes; drift -> reread)
  blocked_if_missing: any pinned input unreadable; AR-01 decision absent
repo_map_decision: loaded
repo_map_reason: cross-tree work (harness + product docs + decisions); the ECR submap is the working front door
doctrine_change: slice builds are implementation, not doctrine. TWO doctrine moments are
  embedded and each owes its own inline direction_change_propagation receipt
  (trigger: architecture_doctrine, related: lifecycle_boundary) by whoever performs it:
  (1) the slice-B owner RATIFICATION (boundary-doc dated amendment, same shape as the
  SP-1/2/3+SP-6 ratification records); (2) the eventual owner UNFREEZE (its own dated
  decision record; conductor row amended only then). This commission performs neither.
external_source_boundary: external workflow source read-only; jb is not Orca authority.
commits: implementation commits in the established harness pattern (feat/test/docs,
  explicit paths, cross-family review bundles landed like prior ECR slices). Never
  commit another lane's files without the owner's word.
```

## Verified State Capsule (2026-06-11; three-agent sweep, all branches + all 15 worktrees)

- **JSG-01 is FROZEN everywhere; no unfreeze exists** — no commit, decision
  file, or worktree (committed or uncommitted) carries one. The conductor's
  JSG-01 row (~:209): schema ratified; "indeterminate_until_authored in
  practice until the EvidenceUnit binding + D2 are built and a case packet
  carries the derived fields + a valid FinalizationReceipt (the SP-5 finalizer
  half is already built). JSG-01 stays FROZEN and clears no case."
- **Already done (do not redo):** SP-1/2/3/6 field schema RATIFIED (closed
  values + clear-conditions, boundary doc); all four derivers + SCR BUILT and
  tested (`orca-harness/ecr/`, `orca-harness/signal_content/`); SP-5
  `FinalizationReceipt` model + validate-only, block-don't-repair consumer
  BUILT (`orca-harness/schemas/finalization_models.py`, committed `a37f896`,
  23 tests; binding_hash via canonical_yaml_hash; per-receipt ULID +
  supersedes); AR-01 staffing RESOLVED (distinct cross-family act,
  operator-for-now, no testee-tester; mechanism was deferred — this
  commission builds it).
- **D2 is NOT required**: SP-6 evaluates determinately without it; per owner
  decision C, clears = {archive_only, not_applicable}; the corroborated tier
  stays deferred. Do not build D2 under this commission.
- **Reserved (touch nothing of it):** the full ECR/Evidence Unit field
  architecture; the canonical object name; JSG-01 unfreeze; the conductor.

## Commission — Four Slices, In Order

**Slice A — SP-5 finalizer acting half (no open decisions; build first).**
The producer that performs the finalization act and emits a valid
`FinalizationReceipt` against the existing model: binds identity / time /
inputs out-of-band per AR-01 (distinct cross-family act — the finalizer
attests `pre_decision_status`; same-model/same-family self-finalization is
structurally disallowed, so the producer must record actor/family provenance
fields the validate-only consumer checks). Operator-driven tooling, no live
LLM calls (`test_no_llm_imports` discipline holds). Tests in the harness
pattern; cross-family code review per the established slice convention before
landing.

**Slice B — EvidenceUnit binding slice (plan -> review -> OWNER STOP -> build).**
Author the bounded slice plan: the minimal composition object/carrier that
binds, by key (reference-never-merge), exactly what the JSG-01 predicate
reads — the four derived source-side postures + the FinalizationReceipt —
onto a case packet, under the ECR invariants (carry-or-residualize;
re-derive-not-migrate; one-record-per-kind; pure derivation). It must
explicitly declare what it does NOT decide: the full EU field architecture,
the canonical object name, content/SCR composition beyond what JSG-01 needs.
Then: cross-family review (delegated-review-patch convention; adversarial
naming on the review prompt; reviewed_by/authored_by provenance), adjudicate,
then **STOP for owner ratification** (dated boundary-doc amendment + DCP
receipt, same shape as the prior ECR ratifications). Build only after the
owner's word.

**Slice C — first real case packet carrying everything.**
Assemble one case packet: SourceCapturePacket -> derived SP-1/2/3/6 fields
(via the built derivers) + a valid FinalizationReceipt (via slice A) bound per
slice B. Default candidate: the Beauty Pie case #3 org-motion archive packet
from the queued Phase-4 capture (Greenhouse ATS, anti-leakage
`select_snapshot <= cutoff`, feasibility gate-0 PASS). Cross-lane dependency:
if that capture has not landed at execution time, run the assembly proof on an
existing pre-cutoff archive SourceCapturePacket and swap the Beauty Pie packet
in when it lands — record which packet carried the proof. Zero-spoiler
discipline is absolute: pre-cutoff material only; NEVER open facilitator-only
/ sealed outcome artifacts (e.g.
`docs/research/orgmotion_beautypie_sealed_outcome_facilitator_only_v0.md`);
the assembled packet must stay blind-usable.

**Slice D — unfreeze decision memo (prep the owner's act; do not perform it).**
A short memo against the conductor's JSG-01 row, line by line: which
preconditions are now satisfied (with paths/hashes/test evidence), which
subpredicates would evaluate determinately on the slice-C packet, what lands
on residuals (expected: SP-6 residual tiers absent D2 — acceptable), and the
exact dated-decision + propagation shape the unfreeze act needs (conductor row
amendment happens only inside that owner act). The memo recommends; the owner
unfreezes.

## Hard Constraints

- JSG-01 and the conductor stay FROZEN for this entire commission. Never edit
  the conductor or any frozen consumer; coordinate by re-courier (the
  boundary doc's established pattern).
- The slice-B reservation is absolute: anything beyond what the JSG-01
  predicate reads routes to the owner memo, never into the build.
- No live raw-API or LLM calls (separate per-run authorization records own
  those); no contestant runs, recognition probes, or scoring under this
  commission; batch-1 execution belongs to other, outcome-clean sessions.
- Claim discipline: building all of this proves machinery existence, never
  judgment-quality attainment — the evidence ladder + claim-defense doctrine
  cap every externally-shaped sentence (Row 1, product_learning).
- Cross-family review before every ratification ask and before landing slice-A
  code, per the established ECR slice convention.
- Smallest complete: no dashboards, runners beyond the finalizer producer,
  storage layers, or speculative fields.

## Output Mode And Contract

`file-write` (+ bounded implementation). Durable outputs: slice-B plan in
`docs/product/` (ECR lane home per the submap's owner-doc pattern), review
bundles/reports in their bound review folders, the slice-D memo in
`docs/decisions/` or chat per owner preference, code + tests in
`orca-harness/`. Chat closeouts: headed human summary first, then
path/hash/status receipts. Stop points: after slice-B review (owner
ratification), and after slice D (owner unfreeze).

## Validation Gates

- `orca_start_preflight` on intake; pinned-input hash verification (drift ->
  reread, then proceed).
- Harness tests green per slice (pytest, scratch under `_scratch/`); the
  no-LLM-imports guard untouched; every persistence claim verified by fresh
  read with shown output.
- Judgment Spine claim-tier gate on anything proof-adjacent (weakest-cleared-
  gate rule; missing evidence is not a pass).
- The two embedded doctrine moments carry their inline DCP receipts (or
  blockers) per `.agents/workflow-overlay/source-of-truth.md`.
- Prompt verdict at authoring: PASS_WITH_WARNINGS — warnings: (1) model lane
  deliberately unbound (owner couriers); (2) slice C carries a cross-lane
  dependency on the Phase-4 capture with a named fallback; (3) the
  boundary doc and conductor are tracked-clean at the pinned hashes but the
  branch is multi-lane — intake re-verifies.

## Non-Claims

Commissions a bounded build. Not the unfreeze (owner's dated act), not the
full EvidenceUnit architecture (reserved), not JSG-01 clearance for any case,
not validation, readiness, judgment-quality evidence, or any external claim.
The verified capsule is the commissioning thread's snapshot — the lane's
intake reads govern.
