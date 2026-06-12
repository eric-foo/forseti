# Prospective Decision Loop Architecture - Delegated Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (adversarial artifact review; delegated review-and-patch return)
scope: >
  Advisory-only delegated adversarial artifact review and bounded patch report for
  docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md.
use_when:
  - Adjudicating the delegated working-tree diff for PR #34.
  - Checking which findings were patched, what citations support each hunk, and what residual risk remains.
authority_boundary: retrieval_only
reviewed_target:
  path: docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md
  pre_run_sha256: 64A4274EBA1950264629940C5B06B3749FFF0B1CA12B71E8CE1CE1D2D3FE17CD
commission_prompt:
  path: docs/prompts/reviews/prospective_decision_loop_architecture_delegated_adversarial_artifact_review_patch_prompt_v0.md
  sha256: 97095796CD85711333E2D5BE6D337B579ABEFCFD9DCF455627BA02EB68D9193C
branch_or_commit: prospective-decision-loop-architecture-v0 @ 3feeaf8
stale_if:
  - Home-model adjudication accepts, modifies, or rejects the working-tree diff.
  - The target file changes after this report without an adjudication note.
  - The near-half plan lands as a durable artifact and changes the decision-memory interface.
```

## Review Summary

```yaml
review_summary:
  status: completed
  recommendation: home_model_adjudicate_patch
  findings_count: 3
  blocking_findings: 0
  advisory_findings: 3
  patch_state: working_tree_patch_left_uncommitted
  summary: >
    No design-level NEEDS_ARCHITECTURE_PASS defect found. The bounded patch
    tightens buyer-proof receipt language, post-resolution shadow disclosure
    semantics, and mid-flight re-seal firewall semantics.
```

## Advisory-Only Bound

This report is advisory decision input for the commissioning Chief Architect.
The commission text expected formal Orca review tooling to be unavailable in the
controller runtime; this Codex runtime could read the relevant skill instructions,
but the output remains advisory-only under the commission. It is not a formal
Orca review verdict, validation, readiness, acceptance, buyer proof,
judgment-quality evidence, or mandatory remediation. Nothing is kept until
home-model adjudication accepts, modifies, or rejects each hunk.

Provenance:

```yaml
authored_by: claude-fable-5[1m]
reviewed_by: codex-gpt-5
controller_model_family: OpenAI / GPT-5
author_home_model_family: Anthropic / Claude
de_correlation_status: satisfied_cross_vendor
```

## Source-Read Ledger

| Source | Why read | Claim supported |
| --- | --- | --- |
| `AGENTS.md` | Supplied in current task context | Project instructions, smallest complete intervention, bounded patch scope |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint | Orca overlay authority |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy and doctrine propagation | Overlay/docs precedence and non-claim boundaries |
| `.agents/workflow-overlay/source-loading.md` | Source pack and preflight | Required `orca_start_preflight` and bounded source loading |
| `.agents/workflow-overlay/review-lanes.md` | Review lane doctrine | Findings-first, advisory boundaries, buyer-proof/judgment route separation |
| `.agents/workflow-overlay/prompt-orchestration.md` | Prompt/review output contract | Durable review report behavior and method sequencing |
| `.agents/workflow-overlay/validation-gates.md` | Strict claim gates | No validation/readiness/acceptance without evidence |
| `.agents/workflow-overlay/delegated-review-patch.md` | Commission contract | Bounded single-target patch, CA adjudication, citation burden |
| `.agents/workflow-overlay/product-proof.md` | Buyer-proof semantics | Buyer-proof receipt and pull/trust requirements |
| `docs/prompts/templates/review/adversarial_artifact_review_v0.md` | Review method reference | Reasoning-before-findings and finding shape |
| `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md` | Shared prompt behavior | Source-gated method and non-claim discipline |
| `docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md` | Review target | Architecture claims and patch target |
| `docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md` | Claim-tier authority | Buyer-proof receipt, product-learning cap, weakest-cleared-gate rule |
| `docs/product/judgment_spine/conductor_construction_integrity_probe_addendum_v1.md` | Firewall translation authority | Seal/disclose/resolve, tell-audit, by-hand residuals |
| `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md` | Ledger discipline source | Pre-declared ledger, report-all, dated amendment discipline |

Near-half absence check: exact search for `signal-reliability ledger`,
`signal_reliability`, `validated-lesson-library`, `validated lesson library`,
`adversarial-postmortem`, `adversarial postmortem`, `lesson-library`, and
`lesson library`, excluding the target file, found only the commissioning prompt.
The target's "no durable repo artifact" premise is supported for this run.

## Reasoning Before Findings

Load-bearing claims in the target:

- The operational loop preserves live-decision firewall integrity through
  seal-before-disclose, mechanical pre-specified resolution, and append-only
  sealed entries.
- One decision-object spine can support two evidence routes as long as mode is
  pre-declared and shadow/assisted evidence is never merged.
- Shadow evidence remains prospective judgment-track evidence capped at
  product-learning until a future gate family is authored and cleared.
- Assisted evidence belongs to the product/buyer route and must not be reused as
  clean prospective judgment evidence.
- Decision memory consumes validated near-half lessons and reliability rows; it
  does not own the near-half ledger or validate its own lessons.
- Every now-item is docs or by-hand operation; code, storage, UX, integrations,
  and domain memory population are counterparty-blocked or separately authorized.

Decision criteria applied:

- Firewall integrity: no post-disclosure or post-outcome material may gain
  original forecast standing.
- Evidence-ladder cap compliance: no buyer-proof, judgment-quality, validation,
  readiness, or new tier vocabulary may be implied without the existing receipts.
- Dependency-map correctness: no counterparty-dependent build item may be filed
  as now-buildable.
- Core/satellite boundary: core may own protocol vocabulary, while real
  counterparty workflow, domain metrics, and decision-memory content remain
  satellite.

Likely failure modes checked:

- Assisted-mode adoption being treated as buyer proof without the complete
  buyer-proof receipt.
- Post-resolution presentation of shadow records being misread as assisted-mode
  disclosure for the original decision.
- Mid-flight updates weakening the append-only seal by replacing an earlier
  scoreable call or allowing post-outcome material into forecast standing.
- Dogfood or public-event phases being overstated as stronger evidence than
  product-learning protocol falsification.
- Near-half pending interface being treated as a real ledger.

## Findings

### AR-01 - Major - Buyer-proof route could be read as sufficient without the complete receipt

Location: `Assisted mode (the adoption-evidence route)` and
`Evidence-ladder integration`.

Issue: The original target said a qualified decision owner using a recommendation
with readback is "literally" the ladder's `buyer_proof` typical surface. It also
said assisted adoption evidence classifies under `buyer_proof` receipts and
product-proof gates when the owner is a qualified external buyer in a live
allocation decision. That was close but too loose: a typical surface is not the
same as a complete buyer-proof receipt.

Evidence:

- Target, original assisted-mode text: qualified owner use plus readback was
  described as the `buyer_proof` typical surface and routed through existing
  gates.
- Evidence ladder, `Buyer-Proof Receipt`: buyer proof requires `buyer_or_decision_owner`,
  `live_decision_context`, `memo_artifact`, `evidence_appendix_artifact`,
  `readback_or_use_signal`, `trust_state`, `pull_grade`, and
  `commercial_next_step_signal`.
- Product-proof overlay: pull means observable decision or budget-adjacent
  behavior, and trust objections/refusals must be classified.

Impact: A future reader could treat assisted-mode usage and readback as already
buyer-proof-shaped, laundering adoption evidence into a stronger claim before
memo/evidence appendix, trust, pull, and commercial-next-step receipts are
present.

Minimum closure condition: The target must state that assisted evidence only
reaches buyer proof when the complete buyer-proof receipt and product-proof
gates are satisfied; otherwise it stays product-learning.

Next authorized action: Patched in target; home model should adjudicate whether
the added receipt language is kept as-is.

Advisory remediation direction: Keep the one-spine/two-route architecture, but
make "typical surface" subordinate to the complete receipt.

### AR-02 - Minor - Resolved shadow record disclosure could blur shadow versus assisted mode

Location: `Sequenced Roadmap`, Phase 3.

Issue: The original Phase 3 wording said the shadow record is "the disclosure
artifact." In context it meant a trust-building post-resolution presentation, but
the schema reserves `disclosure` for assisted mode and the architecture makes
pre-declared mode a firewall control.

Evidence:

- Target schema: `disclosure` is assisted mode only and structurally empty in
  shadow.
- Target architecture: mode is a pre-declared per-decision property, not assigned
  after the fact.
- Target firewall risk statement: disclosure burns the comparator.

Impact: A later operator could misread post-resolution presentation of a shadow
record as assisted-mode disclosure for the original decision, creating ambiguity
about evidence route and buyer-proof classification.

Minimum closure condition: The target must distinguish post-resolution
presentation of resolved shadow records from assisted-mode disclosure fields and
state that presentation cannot retroactively reclassify evidence.

Next authorized action: Patched in target; home model should adjudicate whether
the clarification is kept.

Advisory remediation direction: Preserve Phase 3 sequencing, but reserve
assisted-mode `disclosure` for decisions declared assisted before seal.

### AR-03 - Minor - Mid-flight re-seals needed an explicit non-replacement and pre-outcome guard

Location: `decision_object_v0.updates`.

Issue: The original `updates` field said optional mid-flight re-seals are each
their own sealed call and never an edit. That was directionally right, but it did
not explicitly say updates happen before the relevant outcome/resolution signal
is known, or that they cannot replace an earlier scoreable call.

Evidence:

- Target firewall risk statement: a recommendation revised after outcome
  information starts arriving is not a forecast.
- Target governance: append-only seal registry, amendments are new sealed
  entries, never edits.
- Target schema: the sealed call is the only scoreable forecast for the
  decision, and updates are separately sealed.

Impact: Without the explicit pre-outcome and non-replacement guard, a future spec
could allow late updates to soften a bad original call or collapse an amendment
into a replacement.

Minimum closure condition: The update field must state that re-seals occur
before the relevant outcome/resolution signal is known and do not replace
earlier scoreable calls.

Next authorized action: Patched in target; home model should adjudicate whether
the exact language is kept.

Advisory remediation direction: Keep updates, but score them as separate later
forecasts against their own information set.

## Unified Diff

```diff
diff --git a/docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md b/docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md
index b94e7e5..db5a926 100644
--- a/docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md
+++ b/docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md
@@ -153,7 +153,7 @@ decision_object_v0:
     org_decision:
     org_decision_timestamp:
     divergence_from_recommendation:
-  updates: []                  # optional mid-flight re-seals; each is its own sealed call scored against its own information_set_ref; never an edit
+  updates: []                  # optional mid-flight re-seals before the relevant outcome/resolution signal is known; each is its own sealed call scored against its own information_set_ref; never an edit or replacement of an earlier scoreable call
   resolution:
     outcome_record:            # what happened, recorded against resolution_criteria
     score:                     # mechanical application of the pre-specified criteria
@@ -228,12 +228,15 @@ How the firewall survives a human and an outcome in the loop:
   call, not the contestant using the outcome, but the same rule applies: the
   evidence is quarantined *as judgment evidence* while remaining fully valid
   *as adoption evidence*.
-- **Adoption evidence is the existing buyer-proof surface.** A qualified
-  decision owner using an Orca recommendation in a live allocation decision,
-  with readback, is literally the ladder's `buyer_proof` typical surface. No
-  new promotion path is needed: assisted-mode evidence promotes through the
-  existing product-proof gates (`.agents/workflow-overlay/product-proof.md`),
-  with pull-versus-praise and trust-objection classification unchanged.
+- **Adoption evidence routes through the existing buyer-proof surface.** A
+  qualified decision owner using an Orca recommendation in a live allocation
+  decision, with readback, is a `buyer_proof` typical surface, but it is not
+  buyer proof until the complete buyer-proof receipt is satisfied. No new
+  promotion path is needed: assisted-mode evidence promotes only through the
+  existing product-proof gates (`.agents/workflow-overlay/product-proof.md`) and
+  the ladder's buyer-proof receipt, including the memo/evidence appendix,
+  readback or use signal, trust state, pull-versus-praise classification, and
+  commercial-next-step signal where claimed.
 - **Mode is declared at intake, not after.** Post-hoc mode assignment would be
   a cherry-pick channel (disclose-and-count only the calls that look good).
   The pre-declared decision ledger and report-all rule close it.
@@ -358,10 +361,11 @@ This architecture mints **no** tier, closeout state, or ladder vocabulary.
   surface, which is permanently non-gate-clearing per the pre-sale execution
   evidence-tier policy — so the cap is structural, not a formality.
 - **Assisted route:** adoption evidence classifies under the existing
-  `buyer_proof` receipts and product-proof gates when the decision owner is a
-  qualified external buyer in a live allocation decision; otherwise it is
-  product-learning. Its sealed pre-disclosure call contributes influenced-path
-  calibration at product-learning only.
+  `buyer_proof` receipts and product-proof gates only when the decision owner is
+  a qualified external buyer in a live allocation decision and the complete
+  buyer-proof receipt is satisfied; otherwise it is product-learning. Its sealed
+  pre-disclosure call contributes influenced-path calibration at
+  product-learning only.
 - **Routed-out (ladder owner enacts, nothing here clears anything):** a future
   **prospective gate family** — requirements sketch: pre-registered decision
   ledger; seal receipts with hash + timestamp + sealing-actor separation;
@@ -487,8 +491,11 @@ is constructed ahead of the thing that would tell us it is wrong.
   counterparty + owner decision to disclose. Unlocks B2/B3. Adoption evidence
   flows to the existing buyer-proof path. Sequencing rationale: disclosure is
   irreversible per decision; shadow-first preserves the clean comparator while
-  trust is being earned, and the shadow record is itself the disclosure
-  artifact ("here is what we sealed before you decided, and how it resolved").
+  trust is being earned, and the resolved shadow record is a post-resolution
+  trust artifact ("here is what we sealed before you decided, and how it
+  resolved"). That presentation does not populate the original shadow decision's
+  assisted-mode `disclosure` fields, retroactively reclassify its evidence, or
+  turn it into a buyer-proof receipt.
 - **Phase 4 — Integration/writeback (out of scope).** Separate authorization,
   separate governance; named here only so its exclusion is visible.
 
@@ -559,6 +566,8 @@ batch-1 ledger (pre-declared list, report-all, dated-amendment-only).
   addendum (applied here as by-hand discipline per its PROPOSED status).
 - Does not create the near-half plan, the signal-reliability ledger, or the
   lesson library; N7 is a pending interface, not a binding.
+- Post-resolution presentation of shadow records does not retroactively convert
+  shadow evidence into assisted evidence or buyer proof.
 - Not validation, readiness, acceptance, buyer proof, or judgment-quality
   evidence; this artifact's own evidence state is classified below.
```

## Per-Change Neutral Citations

```yaml
change_citations:
  H1_updates_reseal_guard:
    target_hunk: decision_object_v0.updates
    citations:
      - target: "The target names post-hoc editing as a firewall risk and says a recommendation revised after outcome information starts arriving is not a forecast."
      - target: "The governance section requires append-only sealed entries and amendments as new entries, never edits."
    reason_for_change: >
      The hunk makes the existing append-only/re-seal rule explicit at the schema
      field where a future spec author would otherwise consume it.
  H2_H3_buyer_proof_receipt_guard:
    target_hunks:
      - assisted mode adoption-evidence bullet
      - evidence-ladder assisted-route bullet
    citations:
      - evidence_ladder: "Buyer-proof receipt fields include buyer/decision owner, live decision context, memo artifact, evidence appendix artifact, readback or use signal, trust state, pull grade, and commercial next-step signal."
      - product_proof: "Product proof distinguishes trust objection/refusal and pull versus praise; praise or generic interest is not pull."
      - target: "The target already says assisted-mode evidence promotes through existing product-proof gates and that the sealed pre-disclosure call is product-learning influenced-path calibration only."
    reason_for_change: >
      The hunk preserves the route but prevents typical-surface language from
      being read as a completed buyer-proof claim.
  H4_H5_shadow_record_presentation_guard:
    target_hunks:
      - Phase 3 roadmap
      - Non-Claims
    citations:
      - target: "The schema marks disclosure as assisted mode only and structurally empty in shadow."
      - target: "The architecture says mode is pre-declared per decision and post-hoc mode assignment is a cherry-pick channel."
      - target: "The firewall section says disclosure burns the independent comparator."
    reason_for_change: >
      The hunk distinguishes post-resolution trust presentation from assisted-mode
      disclosure and prevents retroactive route reclassification.
```

## Verdict As Decision Input

Recommendation: keep the patch, subject to home-model hunk adjudication. The
architecture's core route is strong enough to ratify or amend without a new
architecture pass: the biggest risks are not wrong target architecture, but
future misuse of close-enough wording at the evidence-route boundaries. The
patch addresses those risks without widening scope, adding a new gate, or
changing the one-spine/two-mode recommendation.

## Residual Risk

The target still depends on a future near-half artifact that does not yet exist.
This report verified the absence premise cheaply, but it cannot validate the
eventual `signal_id`, lesson-library, or reliability-ledger interface. Reconcile
N7 when that durable source lands.

## Non-Claims

- Advisory decision input only.
- Not validation, readiness, acceptance, buyer proof, judgment-quality evidence,
  formal review verdict authority, or mandatory remediation.
- The delegated review-and-patch convention remains provisional.
- The working-tree patch is not kept until home-model adjudication accepts it.

## Home-Model Adjudication (2026-06-13, appended by the commissioning lane)

```yaml
home_model_adjudication:
  adjudicator: claude-fable-5[1m] (author/home model; correlation with the authored target disclosed — adjudication was checked against the cited controlling sources directly, not against the controller's verdict)
  diff_verified: actual working-tree diff matched the report's Unified Diff byte-for-byte (5 hunks, index b94e7e5..db5a926) before adjudication
  per_hunk:
    - hunk: decision_object_v0.updates re-seal guard (AR-03)
      decision: accepted
      basis: target's own firewall risk 3 + append-only governance; guard excludes post-outcome re-seals from forecast standing without banning indicator-driven updates
    - hunk: assisted-mode adoption-evidence bullet (AR-01)
      decision: accepted
      basis: evidence ladder Buyer-Proof Receipt fields re-checked directly; original "literally the typical surface" wording could launder adoption evidence past the complete receipt
    - hunk: evidence-ladder assisted-route bullet (AR-01)
      decision: accepted
      basis: same receipt check; "only when ... complete buyer-proof receipt is satisfied" matches the ladder's promotion-gate row
    - hunk: Phase 3 post-resolution presentation (AR-02)
      decision: accepted
      basis: schema reserves `disclosure` for assisted mode; original wording created a retroactive-reclassification ambiguity
    - hunk: Non-Claims addition (AR-02)
      decision: accepted
      basis: durable non-claims home for the presentation rule
  vetoes: none
  modifications: none
  kept_state: all 5 hunks kept and committed on the lane branch (PR #34)
  non_claims:
    - adjudication is a keep-decision only; not validation, readiness, ratification, or acceptance of the architecture
    - the target remains PROPOSED at product-learning tier; owner ratify/amend/reject decision still pending
```
