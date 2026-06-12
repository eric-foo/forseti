# Judgment Spine Harness — Product-First Proof-Relevance Handoff Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: Fresh-thread handoff that commissions a docs-only product-first assessment of whether the Judgment Spine v0.14 harness's deterministic judgment-scoring output would produce buyer/decision-relevant signal, measured against Orca's already-decided ICP and buyer-proof standard.
use_when:
  - Starting the product-first frontier check after the Packing -> Harness interface work paused (v3 reached).
  - Deciding whether to keep investing in the Judgment Spine harness or test its proof-relevance first.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/turn_08_product_thesis_v0.md
  - docs/product/product_lead/orca_product_lead_first_icp_wedge_decision_v0.md
  - docs/product/product_lead/orca_buyer_proof_packet_v0.md
  - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md
branch_or_commit: main @ b7627d3 at authoring time (dirty; product and harness sources untracked — recheck at run time)
stale_if:
  - The ICP/wedge decision or buyer-proof standard is materially changed.
  - The Judgment Spine harness output contract (v0.14 report meaning / Phase-1 claim discipline) changes.
  - A later owner decision re-selects the frontier (e.g., back to harness-infra-first).
```

- Status: SAVED_HANDOFF_V0
- Output mode of THIS artifact: file-write (durable handoff prompt)
- Output mode the handoff COMMISSIONS: chat-only (a sequencing decision, not a durable artifact unless separately authorized)
- Implementation, runtime, schemas, probe execution, model runs, scoring runs, proof runs, automation, commits/pushes: not authorized
- Strict product-proof, buyer-validation, willingness-to-pay, readiness, or harness-superiority claims: not proven / forbidden in the output

## How To Use

Open or paste this prompt into a fresh thread (recommended: the current thread is long and harness-biased). The receiver reads the named product and harness documents and returns a product-first sequencing decision. It must not build or extend the harness and must not claim product proof.

## Goal Handoff (carry forward verbatim)

```yaml
goal_handoff:
  long_term_goal: "Build the Judgment Spine into a trustworthy harness for improving frontier-LLM judgment via clean inputs, bounded blind judgments, deterministic scoring, and failure logs, without fake validation or product-proof claims."
  anchor_goal: "Establish whether the harness's deterministic judgment-scoring would produce buyer/decision-relevant signal, before building more harness."
  success_signal: "A grounded read on whether Orca's already-decided ICP/buyer finds deterministic judgment-scoring decision-relevant enough to act on or pay for, tied to the existing buyer-proof standard and/or a real buyer signal, with no fake proof."
  status: owner_accepted
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: yes
  lifecycle_status: active
  if_changed_reason: "Prior anchor (define the Packing->Harness interface) is ACHIEVED at v3; owner re-anchored to product-first proof-relevance."
drift_guard: "Do not slide back into harness-infra build (ledgers, fixtures, schemas, scoring) to avoid the buyer question. Do not re-derive the product thesis/ICP; they are already decided — consume them."
```

## Context (do not re-derive)

- The Packing -> Harness Foundation interface is defined, adjudicated, two-case pressure-tested, independently reviewed, and review-corrected at `packing_to_harness_foundation_interface_architecture_v3.md`. The harness is design-complete but has produced **zero real outputs** (no frozen ledger, blind judgment, probe, or score for any case). Harness build is intentionally paused.
- Orca already has an ICP/wedge decision, a buyer-proof packet, discovery prep, and proof/method-validation machinery. This task **consumes** that; it does not re-open product direction.
- This is the **product-first frontier check**: is the harness's eventual output something the defined buyer would value, before more harness is built?

## Required Method (source-gated)

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. Read the overlay files needed for this lane: `source-loading.md`, `source-of-truth.md`, `product-proof.md`, `artifact-folders.md`, `validation-gates.md`.
3. REFERENCE-LOAD `workflow-deep-thinking` (to frame the buyer-relevance question and failure modes) and `incremental-planning` (for the next-move selection). Optionally REFERENCE-LOAD `workflow-product-ultraplan` only if, after reading, structured product exploration proves necessary. Do not APPLY any method before source readiness.
4. SOURCE-LOAD the bounded source pack below (targeted sections — do not bulk-read the ~60-file product corpus).
5. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
6. Only then APPLY the methods and produce the decision.

Record an `orca_start_preflight` receipt and workspace state (expected `main @ b7627d3`; recheck `git rev-parse HEAD` / `git status`; dirty allowed and reported). Product and harness sources are untracked working files: they support advisory product sequencing but do not establish strict acceptance, validation, readiness, or proof. Make no strict claim.

## Required Reads

Set A — product/buyer anchor (targeted sections):
- `docs/decisions/turn_08_product_thesis_v0.md` — thesis, value proposition, strategic center.
- `docs/product/orca_product_lead_first_icp_wedge_decision_v0.md` — who the buyer is (ICP/wedge) and why.
- `docs/product/orca_buyer_proof_packet_v0.md` — proof standard, target buyer, signal surface, pull-vs-praise, disqualifiers, not-build boundaries.
- `docs/product/orca_offer_hypothesis_v0.md` — offer, mechanism, fit diagnostic, non-claims.
- `docs/product/core_spine_v0_product_contract.md` — product bet, core rule, non-goals (targeted).
- `.agents/workflow-overlay/product-proof.md` — buyer-proof semantics: trust-objection vs trust-refusal, pull vs praise, zero-spoiler. Required because the task touches buyer qualification/proof.

Set B — harness output characterization (read enough to characterize what the harness produces; do NOT re-derive or build it):
- `docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md` — especially "Report Meaning And Non-Meaning" and "Deterministic Checking Boundary".
- `docs/research/judgment-spine/harness/v0_14/proof_and_memory_plan.md` — Phase-1 allowed/forbidden claims; evidence-to-claim policy.
- `docs/research/judgment-spine/harness/v0_14/judgement_harness_strategy.md` — why the harness exists; Phase-1 contestants; no-superiority boundary.

If a named file is missing or its expected section is absent, report a source gap instead of widening to full-corpus reads.

## The Decision To Make

Primary question: **Would the Judgment Spine harness's deterministic judgment-scoring output — in-band / over-band / under-band against a frozen action band, plus shallow evidence-ID and must-address checks, memorization-probe gating, and append-only failure logs (explicitly NOT semantic-quality, NOT baseline-superiority, NOT product proof) — produce signal that Orca's already-decided ICP/buyer would find decision-relevant or pay for, measured against the existing buyer-proof standard?**

Answer these to get there:
1. Who is the buyer and what decision/trigger do they have (from the ICP/wedge)?
2. What is the buyer-proof standard, and what counts as a pull signal vs. praise (from the buyer-proof packet + product-proof overlay)?
3. What does the harness actually output, and what does it explicitly NOT prove (Set B)?
4. Gap analysis: does the harness output map onto anything in the buyer-proof standard or the offer mechanism? Where exactly is the gap?
5. Decision and next move:
   - If plausibly relevant -> name the smallest market-contact or proof test that would validate buyer relevance (real external evidence), not more internal artifacts.
   - If not / unclear -> name what would have to change (sharper buyer/trigger, a different harness output, or harness is premature relative to the product) and the next move.

Then recommend the single highest-compounding next move (an action, artifact, or question first; name a downstream workflow only after the move is chosen). Preserve the cost of delaying market contact: if an internal move cannot name the exact market-facing decision it unlocks, recommend market contact or stop/defer.

## Output Contract (chat-only)

Return:
- start-preflight + workspace-state receipt; `SOURCE_CONTEXT_READY` declaration;
- a compact source-read ledger (files + targeted sections);
- the buyer-relevance assessment (A↔B gap), stated plainly;
- a clear decision: relevant / not relevant / unclear-with-named-condition;
- the single recommended next compounding move and what next decision it sharpens;
- not-proven boundaries and what would change the answer.

You MAY recommend writing a durable product-decision note (under `docs/product/` or `docs/decisions/`), but do NOT write it unless the owner separately authorizes it with a bound destination and write permission.

## Hard Boundaries / Non-Claims

- Docs-only. Do not implement, build, or extend the harness; do not run probes, models, scoring, or proof; no schemas, automation, commits, pushes, or PRs.
- Do not claim product proof, buyer validation, willingness-to-pay, product/feature/commercial readiness, or harness superiority. Those require real proof under the product-proof overlay and are out of scope here.
- Do not re-derive or re-open the product thesis, ICP/wedge, or offer; consume them as decided.
- Honor the no-fake-validation discipline: distinguish observable pull from praise; treat buyer skepticism as a trust-objection (proof material), not a kill, unless it is a true trust-refusal.
- Do not import `jb` templates, paths, lifecycle mechanics, or product-lead rules as Orca authority.

## Closeout

Return a compact human summary plus this YAML:

```yaml
product_first_relevance_summary:
  status: completed | blocked
  buyer_relevance_verdict: relevant | not_relevant | unclear_with_condition
  why: ""
  recommended_next_move: ""
  next_decision_it_sharpens: ""
  market_contact_implication: ""
  blockers: []
  not_proven:
    - product_proof
    - buyer_validation
    - readiness
    - harness_superiority
  next_authorized_step: ""
```
