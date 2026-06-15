# Ontology Backbone Architecture — Delegated Adversarial Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt (delegated review-and-patch commission — provisional convention)
scope: >
  Commission one de-correlated (cross-vendor) adversarial artifact review — and, in
  repo mode, a bounded patch — of the PROPOSED Orca ontology backbone architecture.
  The commissioning home model (Claude/Opus) adjudicates what is kept.
use_when:
  - Dispatching the delegated hardening pass on the ontology backbone deliverable to a
    cross-vendor reviewer.
authority_boundary: retrieval_only
status: AUTHORED_2026-06-15_AWAITING_CROSS_VENDOR_DISPATCH
operating_contract: .agents/workflow-overlay/delegated-review-patch.md (provisional_opt_in)
```

## Applied-Contract Record (prompt-orchestration)

Authored under the owner's current-turn instruction to "send for
`/workflow-delegated-review-patch`". The delegated-review-patch kernel routes strict prompt
rendering to `workflow-prompt-orchestrator`, with the fallback to "apply this file's
prompt-orchestration contract in full and record that" — applied here: review-prompt defaults
(deep-thinking before the review method, source-gated REFERENCE-LOAD→SOURCE_CONTEXT_READY→APPLY,
findings-first, `severity`/`minimum_closure_condition`/`next_authorized_action`,
`reviewed_by`/`authored_by` provenance, `review-report` destination), the delegated-review-patch
overlay interface (de-correlation who-constraint, access modes, bounded target, CA adjudication,
`NEEDS_ARCHITECTURE_PASS`), and the model-neutrality boundary are all carried. No doctrine
changes, so no `direction_change_propagation` of its own.

## Commission

Adversarially review the PROPOSED ontology backbone architecture for material,
decision-relevant failure modes, and (in `repo` mode only) patch the single target
file within the bounded scope. This is a high-stakes authored artifact (a HIGH-lock-in
repo backbone) whose author encodes its own guardrails and can re-introduce the exact
failure modes those guardrails exist to prevent — which is why source-read-only
self-review is insufficient and a de-correlated pass is commissioned.

## De-Correlation Receipt (who-constraint, NOT a model recommendation)

```yaml
actor_model_family_receipt:
  author_home_model_vendor: Anthropic (Claude / Opus)   # authored the deliverable AND adjudicates
  controller_vendor: REQUIRED != Anthropic              # cross-vendor = the DISCOVERY bar (no-new-seam)
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: satisfied_only_if_controller_is_non_anthropic
```

- The DISCOVERY (survives-adversarial-review, no-new-seam) bar requires a **non-Anthropic
  vendor** (e.g. GPT / Gemini). A same-vendor Claude reviewer is the **sanity tier only**
  and must NOT claim the no-new-seam standard; a self pass never qualifies.
- Record `reviewed_by` (the reviewing model + version) and `authored_by`
  (`Anthropic Claude Opus 4.x`) on the durable report; operator/CA-supplied, `unrecorded`
  if unknown, never fabricated.
- This names model *vendors* only to express the difference constraint. It is not runtime
  model routing and must not appear as model-selection advice anywhere in the output.

## Access Mode

- **`repo`** (controller has the branch / PR #110): run the loop — review, then patch the
  target file directly in the working tree (do not commit), return a unified diff + per-change
  neutral citations + verdict + residual-risk note. Everything off the target is read-only.
- **`no_repo`** (repo-blind cross-vendor reviewer — the expected dispatch): advisory **findings
  only, no diff**. The deliverable is supplied as a **verbatim file attachment** pinned to the
  sha below; the CA (home model) applies accepted changes, then runs a **bounded same-vendor
  post-patch recheck** (closure-of-findings + any new blocker/major in the touched delta) before
  keep. `no_repo` is strictly weaker than `repo` (de-correlated review preserved, de-correlated
  patch authorship lost).

## Target (the only editable scope; everything else is flag-only)

- `docs/product/core_spine/orca_ontology_backbone_architecture_v0.md`
- sha256 (pin; verify before review): `8e80e65441c316b466ab027c651fae0b5470de719a1d50186c7998ee001d0187`
- bounded_patch_scope (repo mode): that file only. All other Orca sources, the overlay,
  canonical / frozen / hash-pinned decisions, `AGENTS.md`/`CLAUDE.md`, and every safety-rules
  forbidden path are **read-only — flag, do not patch** (`.agents/workflow-overlay/safety-rules.md`).

## Method (source-gated — REFERENCE-LOAD, do not APPLY until SOURCE_CONTEXT_READY)

1. `workflow-deep-thinking` — frame the boundary problem, failure modes, and decision criteria
   before listing findings (does not widen scope or authorize patching beyond the commission).
2. `workflow-adversarial-artifact-review` — run the formal adversarial artifact review after
   source readiness. If unavailable/unapplied, return advisory-only and emit no formal verdicts.

SOURCE-LOAD the deliverable plus the sources it cites (the demand-gate closures, the read
taxonomy + adjudication, the buyer-proof packet, the batch-1 ledger declaration, the evidence
ladder + gate-ownership map, the venue card set, `repo-structure.yaml` + `artifact-folders.md`,
and `source-of-truth.md`). For a repo-blind reviewer, the relevant excerpts are bundled in the
courier package. Declare `SOURCE_CONTEXT_READY` / `SOURCE_CONTEXT_INCOMPLETE` before applying
either method.

## Seed findings — VERIFY and EXTEND; do NOT anchor

A prior 3-perspective architecture pass surfaced these four. Treat them as candidates to
**independently verify against source AND to push past** — your job is to confirm/refute each
*and* hunt new seams the prior pass missed. Do not stop at these four.

1. **`Case` forks Layer-2.** §2.2 models `split: dev|holdout, entry_basis` as standing
   dimensions, but the batch-1 ledger declares dev/holdout *batch-local* ("mints no ladder
   vocabulary"); `claim_tier` is a *receipt-gated run state*, not a type-intrinsic field. Verify
   against the ledger + evidence ladder.
2. **The two load-bearing links are under-specified where they break.** `diverges_from` (§2.3)
   carries no `layer` attribute, yet the G2 floor-defeater fires only "same coordinated layer";
   `derived_from` has no cycle / multi-parent-collapse semantics. Verify against the gate-closures
   (AR-01/AR-03) and the read-machinery handoff.
3. **Roster over-scoped for a v0 adjudication.** 17 adopted types vs a ~5-type buildable v0 (§9);
   `Buyer`/`Org` have weak/no landed backing. Is "adopt ~5 + reserve the rest as names" sounder?
4. **Cap under-justified + `Brand —can_act_as→ WindCaller` self-laundering.** The 18-cap is
   borrowed from a 12-*instance* venue cap and flipped 15→18 same-day; and a brand's own call
   could count as an independent origin for its *own* product's demand (no guard in §2.3/§2.5).

## Output Contract

- Output mode `review-report`; write the durable report to
  `docs/review-outputs/adversarial-artifact-reviews/ontology_backbone_architecture_review_v0.md`
  (repo mode) or courier the findings for the CA to file (no_repo). Findings-first.
- Per actionable finding: `severity` ∈ {critical, major, minor} (priority only),
  `minimum_closure_condition` (required end state, not how-to), and `next_authorized_action`.
- Record `reviewed_by` / `authored_by`. Preserve the not-proven boundaries and a residual-risk note.
- Escalation valve: if the artifact's problem is **design-level** (not patch-level), return
  `NEEDS_ARCHITECTURE_PASS`, stop patching, quarantine any partial diff (keep nothing), findings only.

## CA Adjudication (home model — Claude/Opus)

The returned diff, citations, and verdict are **claims to adjudicate, not premises to inherit**.
The CA accepts / modifies / rejects each change against the citations and the artifact's intent
(reverting rejected hunks), holds final veto authority even over individually-defensible changes,
and — in `no_repo` — applies accepted changes itself, then runs the bounded same-vendor recheck
before keep.

## Non-Claims

Provisional convention (`.agents/workflow-overlay/delegated-review-patch.md`). Not validation,
not readiness, not formal review authority, not a bound/mandatory/machine-routable review lane,
not patch authorization beyond this bounded commission, and not runtime model routing. The
deliverable stays PROPOSED until owner word.
