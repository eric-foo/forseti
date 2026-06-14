# Ontology Commission Refresh — Delegated (Cross-Vendor) Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (delegated review-and-patch commission — review family)
scope: >
  Commissions ONE de-correlated, cross-vendor adversarial review-and-patch
  hardening pass on the refreshed Orca ontology backbone commission prompt, then
  routes the result to home-model (Claude/Opus) adjudication. High-stakes: the
  reviewed artifact commissions the repo's semantic backbone, so an error
  propagates everywhere.
use_when:
  - Dispatching the delegated cross-vendor hardening review of the refreshed ontology commission, before it is launched.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md   # THE TARGET
  - .agents/workflow-overlay/delegated-review-patch.md                                                 # operating contract (provisional convention)
  - .agents/workflow-overlay/prompt-orchestration.md                                                   # Review Prompt Defaults + validation gates
```

## Applied-Contract Record (prompt-orchestration)

Authored 2026-06-14 under owner instruction ("/workflow-delegated-review-patch the prompt after").
Per `.agents/workflow-overlay/prompt-orchestration.md` validation gate 1 ("apply this file's
contract in full and record that"), the contract is applied: Review Prompt Defaults
(`workflow-deep-thinking` before `workflow-adversarial-artifact-review`, source-gated);
`review-report` output mode bound to a durable destination; findings-first; `reviewed_by`/
`authored_by` provenance required; `minimum_closure_condition`/`next_authorized_action` on
actionable findings; fitness reference bound; no runtime-model routing (the cross-vendor
constraint below is a who-constraint per `delegated-review-patch.md`, not a model
recommendation). The delegated-review-patch invariants are carried verbatim from
`.agents/workflow-overlay/delegated-review-patch.md`.

## Lane Binding (delegated review-and-patch — provisional convention)

- overlay_status: `provisional_opt_in` — available by this explicit owner/CA commission; not a bound or mandatory review lane.
- operating_contract_pointer: `.agents/workflow-overlay/delegated-review-patch.md` (the controller treats this as its contract).
- review_lane: artifact → `workflow-adversarial-artifact-review` (the target is a prompt artifact, not code).
- mode: `base-subagent` (single bounded high-stakes file; judgment-coupled — not split-executor).
- access: **`no_repo` default** (ship the target verbatim; controller returns findings; CA applies + runs the required bounded same-vendor post-patch recheck) **OR `repo`** if the operator's controller has repo access (controller patches the target directly and returns a diff; the cross-vendor repo-mode discovery then needs no separate re-scan). Operator picks at dispatch and records it.

### Actor / model-family receipt (de-correlation = who-constraint, not a model recommendation)
- author_home_model_family: **Anthropic / Claude (Opus 4.8)** — authored both the original commission and this 2026-06-14 refresh, and adjudicates what is kept.
- controller_model_family: **must be a DIFFERENT vendor (non-Anthropic, e.g., OpenAI/GPT)** — operator binds the concrete model at dispatch; unknown/undisclosed lineage cannot satisfy the cross-vendor bar.
- current_receiving_actor_role: `controller`.
- dispatch_mode: `external-controller-courier` (no_repo) or `runtime-subagent` (repo).
- de_correlation_status: **satisfied only if the controller vendor ≠ Anthropic.** If only a same-vendor reviewer is available, do NOT claim the cross-vendor discovery (no-new-seam) bar — run the same-vendor sanity tier and record the limitation (`delegated-review-patch.md` De-correlation).

## Target

- **target (the single editable scope):** `docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md` — the refreshed ontology backbone architecture-pass commission (refreshed 2026-06-14 to the landed demand-state grammar; the artifact carries an Applied-Contract Record + a Refresh Note).
- **why source-read-only review is insufficient:** the artifact commissions the repo's semantic *backbone* — a wrong object carve or a stale/incorrect grammar pointer propagates into every downstream lane. The refresh was authored by the same family (Claude) that authored the grammar it points at, so author-correlated blind spots (e.g., baking a still-wrong demand-state framing into the ontology inputs, or over-/under-specifying the roster) are exactly what self-review structurally misses. A de-correlated pass that both finds AND proposes the bounded fix is the cheap guard before launch.
- **bounded_patch_scope:** the target file ONLY — its Refresh Note, candidate-roster additions, SOURCE-LOAD list, freshness gate, survey list, applied-contract record, and any internal inconsistency in the refresh. Do NOT touch the commission's already-sound v0 spine (four-commitment frame, two-layer split, kernel discipline/cap, output contract) except to flag a defect.
- **off_scope (read-only — flag, don't edit):** every other path. Especially: the grammar/decision sources the commission points at (thesis, taxonomy, adjudication companion, buyer-proof, carve-out, demand-gate closures), the overlay, `AGENTS.md`/`CLAUDE.md`, and any canonical/frozen/hash-pinned doc. The delegate flags issues there; it does not patch them. Protected-path authority: `.agents/workflow-overlay/safety-rules.md`.

## orca_start_preflight (controller fills at execution)

```yaml
orca_start_preflight:
  agents_read: <yes/no>            # AGENTS.md + .agents/workflow-overlay/README.md read fresh
  overlay_read: <yes/no>
  source_pack: custom — the target prompt + its SOURCE-LOAD set (read the CURRENT main versions)
  repo_map_decision: loaded
  repo_map_reason: locate the grammar sources + the proto-schemas the commission must reconcile
  workspace: C:\Users\vmon7\Desktop\projects\orca
  expected_branch: <controller's own lane off origin/main; repo mode only>
  dirty_state_checked: <yes/no/not_applicable>
  controlling_source_state: <clean/modified/untracked/stale> for the target + the demand-grammar sources
  edit_permission: repo → patch-only on the single target file; no_repo → read-only (advisory findings only)
  output_mode: review-report
  external_source_boundary: jb is not Orca authority; external workflow source read-only
```

## Method and Source Contract (source-gated — do NOT APPLY before SOURCE_CONTEXT_READY)

`REFERENCE-LOAD` (procedural guidance only; do not APPLY yet):
1. `workflow-deep-thinking` — frame the boundary problem, the refresh's failure modes, and decision criteria BEFORE listing findings (per prompt-orchestration Review Prompt Defaults). It does not widen scope or authorize patching beyond the bounded scope.
2. `workflow-adversarial-artifact-review` — the review lane. Run it after source readiness. If unavailable/unresolved, return advisory-only and emit no formal verdict (do not silently emulate the lane).

`SOURCE-LOAD` (read CURRENT `main`; the demand-grammar docs are LIVE — verify the 2026-06-14 model is present, not the retired "durable vs hollow"):
- The target prompt (the whole file).
- `docs/product/product_lead/orca_demand_read_taxonomy_v0.md` + `..._adjudication_v0.md` — the read grammar + Q0–Q3 outcomes the refresh claims to capture.
- `docs/decisions/orca_product_thesis_consumer_demand_v0.md` (the 2026-06-14 amendment) and `docs/product/product_lead/orca_buyer_proof_packet_v0.md` (Hard Gate + never-a-feed).
- `docs/product/product_lead/orca_demand_gate_definition_closures_proposal_v0.md` (G1/G2/G4) and `docs/decisions/wind_caller_calibration_carveout_v0.md` (Q3 boundary).
- `.agents/workflow-overlay/delegated-review-patch.md` and `prompt-orchestration.md` (the contracts this prompt and the target must satisfy).

Declare `SOURCE_CONTEXT_READY` (or `SOURCE_CONTEXT_INCOMPLETE` with the gap) before APPLY.

## What to attack (be maximally adversarial within the bounded target)

Material, decision-relevant failure modes of the *refresh* (not the v0 spine, unless defective):
1. **Grammar fidelity:** does the refresh describe the demand-state model, calling sequence, Q1–Q3, and the wind-caller boundary *correctly* and *completely*, or did it introduce a wrong/garbled framing, or miss a load-bearing piece (e.g., the integrity axis, the differentiation floor, the never-a-feed semantics) that the ontology must type?
2. **Cap vs completeness:** the roster additions (demand_state, Read lifecycle, Gate actions, ActionCeiling, claim_tier, never-a-feed, WindCaller boundary) — do they violate the commission's own **hard cap / naming-normative-schema-light** discipline (over-specifying property lists, smuggling in a straitjacket), or are some genuinely *missing* still (org-motion proto-schema, entity-resolution boundary, Slot state machine)?
3. **Freshness-gate weakening:** the SOURCE-LOAD switch from exact sha-pins to "content-verification" for the live docs — does this *weaken* the base-freshness guard (a real risk the commission's own gate was designed against), or is it the right call for live docs? Propose the tightest defensible form.
4. **Boundary integrity:** does the refresh preserve grammar≠ontology, architecture-only (no implementation), Layer-2-MAP-not-rebuild, and the "design FOR forward consumers" (scan-core, read-machinery) without quietly authorizing scope creep?
5. **Internal consistency:** any contradiction the refresh introduced (e.g., between the Refresh Note, the roster, the SOURCE-LOAD, and the v0 body); the applied-contract record's accuracy.
6. **Dispatch-readiness:** would a fresh cross-lane architecture-pass model, reading ONLY this prompt, build the right thing — or is there a launch-blocking ambiguity?

## Controller output contract

- Findings in the `workflow-adversarial-artifact-review` schema, severity `critical`/`major`/`minor` (priority only), each with **per-finding neutral-but-decision-sufficient source citations** (`file:line`).
- For each actionable finding: `minimum_closure_condition` (required end state) + `next_authorized_action`.
- **repo mode:** a unified working-tree diff (NOT committed) of the bounded fix on the target file only + verdict + residual-risk note.
- **no_repo mode:** findings + proposed exact edits (no diff applied) + verdict + residual; the CA applies and runs the bounded same-vendor post-patch recheck.
- **Escalation:** if the refresh's problem is design-level (the commission shouldn't be refreshed but re-architected), return `NEEDS_ARCHITECTURE_PASS`, stop patching, quarantine any partial diff (kept = none), findings only.
- **Off-scope:** flag-only; never edit beyond the single target.
- Durable report → `docs/review-outputs/adversarial-artifact-reviews/ontology_commission_refresh_delegated_review_v0.md`; record `reviewed_by` (controller model+version) and `authored_by` (Claude/Opus 4.8) — operator-supplied, `unrecorded` if absent, never fabricated.

## Fitness reference (alignment axis — attack it, don't pass-if-matches)

The refresh's intended outcome: **a current, complete, dispatch-ready commission** such that the architecture-pass lane designs the ontology against the *landed* demand-state grammar (durable/transient/manufactured + calling sequence + Q0–Q3 + gates), under the unchanged cap/architecture-only/MAP-not-rebuild discipline. Observable success signal: a fresh model reading only the prompt produces an ontology design that types the demand-state machinery without over-specifying or missing it, and without scope creep. If no checkable bar is derivable for a finding, name `no checkable success bar bound` rather than inventing one.

## Home-model (CA) adjudication contract — what happens after the review returns

The controller's findings, citations, diff, and verdict are **claims to adjudicate, not premises to inherit.** The home model (Claude/Opus) accepts/modifies/rejects each change against the citations and the refresh's intent, reverting rejected hunks; it may veto an individually-defensible change that adds no benefit or is net-negative. In `no_repo` mode the CA applies accepted edits and runs the bounded same-vendor post-patch recheck (closure-of-findings + any new blocker/major in the touched delta) before keep. Bring the controller output back to the commissioning thread for this adjudication (a `workflow-delegated-review-patch` review-return turn).

## Hard constraints / non-claims

- Review the bounded target only; everything else is flag-only. No implementation, no edits to the grammar/decision sources or the overlay.
- De-correlation is a who-constraint (cross-vendor), not a runtime-model recommendation; do not rank or select models.
- Provisional convention — not validation, readiness, formal bound-lane authority, or auto-keep. A delegated diff + verdict is decision input only; the CA decides what is kept.
- The cross-vendor discovery (no-new-seam) standard may be claimed only if the controller vendor ≠ Anthropic; otherwise record the same-vendor-sanity limitation.
```
