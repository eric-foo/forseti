# Core Spine v0 Data Lake Bronze Full-GT Gate ADR Batch Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Data Lake workflow/decision-request record
scope: >
  Post-PR-557 batch plan for the Bronze full-GT physicalization lane: one
  review-efficient work unit that authors the Gate 1 ADR and the Gate 2
  explicit-posture ADR together, plus the parallel delegated review of the
  landed physicalization decision brief.
use_when:
  - Continuing the Bronze full-GT lane after PR #557 with the owner's Gate-1-first call.
  - Sizing or dispatching the Gate ADR authoring lane and its single delegated review-patch pass.
  - Checking what is batched now versus deferred until owner ratification of both gates.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md
  - docs/prompts/reviews/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_delegated_adversarial_review_patch_prompt_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - .agents/workflow-overlay/delegated-review-patch.md
stale_if:
  - Gate 1 and Gate 2 are both ratified or explicitly deferred by accepted authority.
  - The brief's delegated review returns NEEDS_ARCHITECTURE_PASS.
  - The owner declares lawful erasure a hard current requirement (re-orders to Gate-2-first).
  - The Storage, Attachment Record, or Physicality Location contract changes the physicalization boundary.
```

## Status

`GATE_ADR_BATCH_PLAN_RECORDED_V0; BATCH_COMPLETE_BOTH_GATES_RATIFIED_2026_07_02`.

Both gates were ratified by the owner on 2026-07-02 (recorded in each ADR's
Owner Ratification block). The batch is complete and this plan is now a
historical record. Post-ratification continuation lives in
`docs/hygiene/bronze_full_gt_post_ratification_handoff_v0.md` (contract
fold-in with DCP receipts, then implementation scoping). The brief's
cross-vendor discovery residual remains open: the owner has not yet accepted
it or commissioned a non-OpenAI-family pass.

B2 and B3 were authored 2026-07-02:
`core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md`
(packet-member default; sidecar reserved; G1-D locked behind Gate 2 plus a
backend/physicalization ADR) and
`core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md`
(explicit deferral with the full accepted-residual record). B5 executed
2026-07-02 (GPT-5 controller: cross_vendor_discovery for both ADRs,
same_vendor_sanity for the brief recheck; `[gate1-adr]` patched for AR-01
stale raw-path grammar and AR-02 G1-D under-gating, both CA-adjudicated and
kept; `[gate2-adr]` and `[brief-recheck]` no-patch). Report:
`docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_lake_bronze_full_gt_gate_adr_batch_delegated_adversarial_review_patch_v0.md`.
The only remaining batch step is owner ratification of both gates. The brief's
cross-vendor discovery bar remains open (two same-vendor passes so far); the
owner may accept it as a residual at ratification or commission a
non-OpenAI-family pass.

This is a planning and sequencing record. It is not implementation
authorization, gate ratification, backend/layout/retention selection,
validation, readiness, review-lane authority, or a Bronze full-GT claim.

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom data_lake physicalization S3 (brief + overlay delegated-review/prompt contracts)
  edit_permission: docs-write
  target_scope: >
    Bronze full-GT physicalization lane batching after PR #557; no runtime
    implementation, backend selection, third proof, or full-GT claim.
  dirty_state_checked: yes
  blocked_if_missing: >
    Re-read the brief and the storage / Attachment Record / physicality
    contracts before authoring either Gate ADR.
```

## Owner Decisions Recorded (2026-07-02)

- Gate 1 ADR is the next physicalization route (owner selected option 2 of the
  brief's Decision Request).
- The docs-only patch lane was closed first: PR #557 merged to main at
  `23f2536238ff9753f9f925652225962b26a8a09f`.
- The owner's Gate-1-first selection signals lawful erasure is not currently a
  hard requirement. This is a routing signal only, not a ratified retention
  posture; the Gate 2 ADR below must make the posture explicit and
  owner-ratified.

## Batch Definition

One work unit, sized so a single delegated review-and-patch pass covers every
authored artifact in it. Steps B2-B4 belong to one authoring lane and one PR.

- **B1 - Brief delegated review (dispatched now, runs in parallel).**
  Courier the filed prompt
  `docs/prompts/reviews/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_delegated_adversarial_review_patch_prompt_v0.md`
  to a controller from a non-OpenAI vendor family (the brief's author family).
  The commissioning CA adjudicates the return per
  `docs/prompts/templates/review/delegated_review_return_adjudication_v0.md`
  and lands accepted patches via a lane PR. Executed 2026-07-02 at the
  same-vendor sanity tier (the operator couriered to a GPT-5 controller, the
  same vendor as the author family); both major findings were patched and
  CA-adjudicated as kept. Cross-vendor discovery for the brief remains
  unsatisfied and rides B5's `[brief-recheck]`.
- **B2 - Gate 1 ADR authoring.** Author the Attachment Record body-relationship
  ADR from the brief's Gate 1 section: carry G1-B (packet-member/bundle) versus
  G1-C (hash-pinned sidecar) as the live comparison with G1-A as the MGT
  fallback; do not select G1-D before Gate 2. The ADR must produce all eight
  minimum Gate 1 outputs (body key, hash_basis, physical relationship, public
  read surface, authority split, rebuild rule, replay/migration implication,
  rejected shapes), a recommendation, and an explicit owner-ratification block.
- **B3 - Gate 2 explicit-posture ADR.** Record the retention/lawful-erasure
  posture as a first-class decide-or-defer artifact. Default form given the
  owner signal: explicit deferral carrying the accepted-residual record the
  patched brief requires - residual scope (lawful erasure named as an accepted
  residual), an explicit claim ceiling, append-only tombstone/supersession
  (G2-B) as the working unavailability posture, forbidden backend classes or
  operations while deferred (any backend whose adoption would make the deferred
  erasure posture irreversible or would carry retention policy implicitly), and
  revisit triggers that force a retention/lawful-erasure ADR before lock-in. If
  the owner
  instead declares erasure load-bearing, this step escalates to a full Gate 2
  decision ADR and precedes B2 ratification.
- **B4 - Routing updates.** Patch the brief's `open_next` to reach both ADRs,
  add repo-map rows, and update this plan's status. No supersession of the
  brief; it remains the gate-framing source.
- **B5 - Single delegated review-patch pass over the batch.** One commission,
  multi-target with label tags (`[gate1-adr]`, `[gate2-adr]`, plus
  `[brief-recheck]` when B1 patched the brief), cross-vendor from the batch
  author, followed by CA adjudication and then owner ratification of both
  gates. Because B1 executed at same-vendor sanity, the `[brief-recheck]`
  target also carries the brief's outstanding cross-vendor discovery bar, so
  B5's controller must be non-OpenAI-family - and non-Anthropic-family for
  the ADR targets, since the batch ADRs were Claude-authored. The B5
  commission prompt is filed at
  `docs/prompts/reviews/core_spine_v0_data_lake_bronze_full_gt_gate_adr_batch_delegated_adversarial_review_patch_prompt_v0.md`. Cross-gate consistency (G1-D locked behind Gate 2; sidecar keying
  versus erasure separability; replay/migration versus tombstone semantics) is
  an explicit review axis - this interaction is why the two ADRs review as one
  pass rather than two.

## Sequencing And Stop Conditions

- B1 dispatches immediately; B2/B3 authoring may start in parallel in a fresh
  lane, but the default is to adjudicate B1 first because the ADRs cite the
  brief's gate definitions.
- Hard ordering: B1 adjudication must complete before B5 ratification; B5 must
  complete before either gate is treated as decided or deferred.
- Stop conditions: NEEDS_ARCHITECTURE_PASS from B1 stops B2/B3 until the brief
  is re-founded; an owner declaration that lawful erasure is load-bearing
  re-orders the batch to Gate-2-first.

## Deferred Until Both Gates Are Ratified Or Explicitly Deferred

Named deferrals (deliberate, not omissions):

- Implementation scoping (`workflow-implementation-scoping`) for the chosen
  body relationship, and the Batch A deterministic inventory gate (A1) as its
  first scoped step; both need bounded implementation authorization.
- Authority-contract amendments (Attachment Record, Storage) folding in the
  ratified decisions, each with its `direction_change_propagation` receipt -
  the ADRs are doctrine-changing at ratification, not at authoring.
- Manifest/equivalent fork (A2), which waits on the A1 inventory.
- Any third-proof candidate work, per the brief's Proof/CI Boundary.

## Drift Guard

- No runtime storage implementation, backend selection, retention policy,
  Manifest selection, or third-proof work inside this batch.
- The brief's review (B1) and the batch review (B5) are decision input only;
  neither ratifies a gate. Ratification is the owner's.
- PR #555/#557 remain gate-hardening and planning evidence, not full-GT
  progress claims.

## Non-Claims

- Not implementation authorization.
- Not Gate 1 or Gate 2 ratification, backend/engine/layout selection, or
  retention/lawful-erasure posture.
- Not validation, readiness, review-lane authority, or Bronze full GT.
- Not a claim that the delegated review has run; B1 is dispatched by the
  operator and adjudicated on return.
