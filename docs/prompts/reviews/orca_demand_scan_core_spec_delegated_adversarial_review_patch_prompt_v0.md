# Delegated Adversarial Review-and-Patch — Orca Demand Scan-Core Spec v0 (Controller Prompt)

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (review family — delegated review-and-patch commission, base-subagent, repo mode)
scope: >
  Commission one de-correlated (non-Anthropic) controller to run an adversarial
  artifact review of docs/product/foundation/orca_demand_scan_core_spec_v0.md
  via the portable review method, then apply a bounded working-tree patch to
  that single file, returning a unified diff + per-change neutral citations +
  advisory verdict + residual-risk note for home-model (CA) adjudication.
  Convention: .agents/workflow-overlay/delegated-review-patch.md (provisional,
  opt-in; this prompt is the explicit CA commission).
use_when:
  - Dispatching the delegated hardening pass on the demand scan-core spec (operator couriers this prompt to a non-Anthropic-vendor agent with access to the pinned worktree).
authority_boundary: retrieval_only
branch_or_commit: demand-scan-core-spec-v0 worktree @ 64c442a (tracking origin/main)
stale_if:
  - The target file's pinned hash no longer matches (the spec was edited after commissioning — re-render this prompt).
  - The delegated-review-patch convention or the portable method is amended.
```

## Commission

- **Target (the editable scope):** `docs/product/foundation/orca_demand_scan_core_spec_v0.md` — PROPOSED method spec, authored 2026-06-13, untracked in the worktree below.
- **Why source-read-only review is insufficient:** the artifact is a high-stakes authored method spec whose author encodes the guardrails (mode walls, anti-triggers, boundary rules) and can reintroduce exactly the failure modes those guardrails exist to prevent; a combined de-correlated review-and-patch pass collapses the review → adjudicate → instruct → patch → re-read round-trip while keeping the CA's adjudication gate.
- **Bounded patch scope:** the single target file, working tree only, no commit. Everything else in the repository is read-only — flag, don't edit.
- **Intended decision:** the commissioning home model (CA) adjudicates your returned diff change-by-change before anything is kept; the owner signs spec adoption separately.

## Lane Binding

- `overlay_status:` provisional (`provisional_opt_in` — available only by explicit CA commission; this prompt is that commission; not a bound review lane)
- `operating_contract_pointer:` `.agents/workflow-overlay/delegated-review-patch.md` — read it in the worktree and treat it as your operating contract
- `review_lane:` artifact — via the PORTABLE METHOD block (below); Orca's formal review skills are not invocable in your runtime, so your claim level is **advisory findings only** (state this in your report)
- `mode:` base-subagent. `access:` repo.
- `actor_model_family_receipt:`
  - `author_home_model_family:` Anthropic (Claude — Fable 5, `claude-fable-5`; authored the target 2026-06-13 in this lane)
  - `controller_model_family:` who-constraint — any **non-Anthropic** upstream model vendor; the operator records the concrete identity at dispatch
  - `current_receiving_actor_role:` controller (you, on receiving this prompt)
  - `dispatch_mode:` external-controller-courier
  - `de_correlation_status:` satisfied-by-constraint — you must self-verify below before any work
- **Controller self-check gate (run first):** state your own upstream model vendor/lineage in your report. If it is Anthropic, or unknown/undisclosed, return `BLOCKED_CONTROLLER_NOT_DECORRELATED` and stop — unknown lineage cannot satisfy the cross-vendor bar. Vendor means the upstream model developer, not the hosting platform, reseller, or wrapper.
- De-correlation is a **who-constraint of this commission, not a model recommendation**; nothing here selects, ranks, or routes a runtime model.
- `subagent_authority:` you run the pass yourself. No recursive subagents, no replacement controller, no delegation of the review or the patch.

## Start Preflight (required — verify, then proceed; on any failure return the named blocker instead of proceeding)

- Read `AGENTS.md` and `.agents/workflow-overlay/README.md` fresh in the worktree (not supplied by this prompt).
- `source_pack:` bounded custom pack — the SOURCE-LOAD list below. `repo_map_decision:` not_needed — this commission supplies every path; no repo-map routing is required.
- Workspace: `C:\Users\vmon7\Desktop\projects\orca-worktrees\orca-demand-scan-spec-wt` — branch `demand-scan-core-spec-v0` @ `64c442a`. Work in this worktree in place; do not create, clone, or switch to another checkout. Wrong worktree or revision → return a blocked result naming the mismatch.
- **Target hash gate:** the target file's SHA256 over raw file bytes must be
  `1DA22088746012B474639AA8EF401ED7FCD63E65B1137D4829C6929CFA3C0856`.
  Mismatch → `BLOCKED_STALE_TARGET` (the spec changed after commissioning).
- **Hash convention for tracked-source pins:** all pins below are SHA256 over git blob bytes (LF as stored; `git cat-file blob <rev>:<path>` or CRLF→LF-normalized working-tree bytes), first 16 hex. A raw-byte mismatch on a CRLF Windows checkout is not staleness by itself — compare like-for-like. Genuine mismatch on any pinned source → `BLOCKED_STALE_BASE`.
- Dirty-state allowance (exactly this set may be dirty when you start): untracked `docs/product/foundation/orca_demand_scan_core_spec_v0.md` (the target); untracked `docs/prompts/reviews/orca_demand_scan_core_spec_delegated_adversarial_review_patch_prompt_v0.md` (this prompt); modified `docs/prompts/templates/portable/adversarial_artifact_review_portable_method_v0.md` (dated re-pin, 2026-06-13). Plus, created by you: the report file and your patch to the target. Any other dirt → blocked result naming it.
- Edit permission: **patch-only on the single target file** + **file-write for the single report file** (path below). Read-only on absolutely everything else, including the target's sources, the overlay, templates, and this prompt.
- Output mode: `review-report` (filesystem-output at the required path below) + the working-tree unified diff (never committed). Preflight write access to the report path before starting the review; if the report cannot be written at the end, return `FAILED_REVIEW_OUTPUT_WRITE` with the failed path — chat output is courier state, not a substitute artifact.
- Doctrine boundary: the target is a PROPOSED method spec. If a correct fix would require changing the thesis, wedge, buyer-proof packet, overlay, taxonomy, card set, guide, pool, brief, or any owner-locked record — that is off-scope: flag it; for design-level problems use the escalation valve below.
- External boundary: **no public web research**; the spec and this review are built from in-repo material only. `jb` is not Orca authority.

## Method And Source Contract (source-gated)

REFERENCE-LOAD first — do not APPLY before `SOURCE_CONTEXT_READY`:

- `docs/prompts/templates/portable/adversarial_artifact_review_portable_method_v0.md` — apply only the delimited PORTABLE METHOD block as your review method. Freshness gate: run by the commissioning lane 2026-06-13 (review-lanes.md pin re-pinned to `64c442a` blob bytes after a pin-only delta; the other pin verified unchanged).

SOURCE-LOAD (pins = SHA256 first-16, blob-byte convention above, at `64c442a` unless noted):

- THE TARGET: `docs/product/foundation/orca_demand_scan_core_spec_v0.md` — full hash above (untracked; raw bytes).
- FITNESS REFERENCE: `docs/prompts/product-planning/consumer_demand_scanning_lane_commission_prompt_v0.md` — `92146714330AF783` — the commission the target was authored to satisfy. Goal + success signal: the target's "Scope And Deliverable" obligations (seven required sections) and "Hard Constraints", satisfied from the pinned sources without contradiction. This is an alignment axis you must also attack — never a pass-if-matches bar.
- The target's eight pinned sources (verify, then read):
  - `docs/product/product_lead/orca_demand_read_taxonomy_v0.md` — `BC478D890419B2B6`
  - `docs/product/foundation/beauty_venue_card_set_v0.md` — `65E22CDAE5EDE781`
  - `docs/product/foundation/orca_vertical_exploration_guide_v0.md` — `EF9F5C6E716E9857`
  - `docs/product/foundation/orca_memorization_resistant_case_finder_frame_v0.md` — `C672C1678F98878F`
  - `docs/product/foundation/consumer_demand_candidate_pool_handoff_v0.md` — `19009D43A7C29858`
  - `docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md` — `48B5534E056FD42A`
  - `docs/decisions/orca_product_thesis_consumer_demand_v0.md` — `B119E24691066E47`
  - `docs/product/product_lead/orca_buyer_proof_packet_v0.md` — `25EBD39AE95C3A07`
- Authority (read-only): `AGENTS.md`; `.agents/workflow-overlay/README.md`; `.agents/workflow-overlay/delegated-review-patch.md` (your operating contract).

Declare `SOURCE_CONTEXT_READY` (or `SOURCE_CONTEXT_INCOMPLETE` with the gap list) in your report before applying the method or proposing any finding or patch.

## Review (APPLY only after SOURCE_CONTEXT_READY)

Apply the PORTABLE METHOD block — reasoning pass before findings; be maximally adversarial about material, decision-relevant failure modes within this commission's target and purpose. In addition to the method's standard checks, attack at minimum:

1. **Source support:** every rule the spec binds (triggers, anti-triggers, walk order, schema fields, mode obligations, handoff boundaries) traces to the pinned sources at their pinned content — find inventions, misreadings, and silent strengthenings/weakenings.
2. **Reconciliation correctness:** the absorb/leave boundaries against the exploration guide and the case-finder frame — find duplication, forking of owner-adopted procedure, or orphaned obligations neither document now owns.
3. **Gate checkability:** does the candidate-entry schema actually make the Demand-Substrate Hard Gate columns mechanically checkable (including the four-gate-family vs evidence-venue split), or does it smuggle judgment back in?
4. **Boundary leakage:** does the spec anywhere set capture routes, create person-level surfaces, imply standing monitoring/registries, open outreach, or exceed PROPOSED authority?
5. **Mode-wall soundness:** backward/forward separation — contamination posture, the pool-never-a-slot-source wall, the fresh-observation corollary.
6. **The two named adjudication surfaces:** the 21-day forward freshness default and the gate-family vocabulary split — are they defensible, internally consistent, and honestly labeled as open?
7. **The fitness reference itself:** is the commission's seven-section bar the right bar; name `no checkable success bar bound` for any obligation lacking one.

Severity labels (`critical`/`major`/`minor`) are finding-priority only. Findings need `severity`, `location`, `issue`, `evidence` (target section + conflicting source/authority excerpt), `impact`, `minimum_closure_condition`, `next_authorized_action`, and an advisory remediation direction.

## Bounded Patch (after the review pass)

- Patch ONLY the target file, directly in the working tree. Do not commit, stage, or push.
- Patch what your accepted-by-you findings justify — smallest complete fixes; no rewrites beyond the failure modes found, no style sweeps, no scope inflation.
- Off-scope is flag-only: if the correct fix lies in a source, the overlay, the commission, or anywhere outside the target, record it as a finding and leave the file untouched.
- **Escalation valve:** if the artifact's problem is design-level rather than patch-level, return `NEEDS_ARCHITECTURE_PASS`, stop patching, revert any partial diff (leave the target byte-identical to its pinned hash), and return findings only.
- Citations: per-change source citations, **neutral in tone, decision-sufficient in substance** — your argument lives in the verdict and residual-risk note, never in the citations. Thin citations defeat the de-correlation.

## Output Contract

1. Write the durable report to exactly:
   `docs/review-outputs/adversarial-artifact-reviews/orca_demand_scan_core_spec_delegated_adversarial_review_patch_review_v0.md`
   containing, in order: the de-correlation self-check (your vendor statement); the preflight receipts (hash gates, dirty-state check, `SOURCE_CONTEXT_READY`); `review_summary` (portable-method shape; status/recommendation are advisory); findings (`critical` → `major` → `minor`); the unified diff of your patch (or `NEEDS_ARCHITECTURE_PASS` / no-patch statement); the per-change citation map; verdict; residual-risk note; and these provenance fields:
   - `authored_by: Claude Fable 5 (claude-fable-5)` (recorded by the commissioning lane)
   - `reviewed_by: <your model + version, operator/tooling-supplied; "unrecorded" if not supplied — never fabricated>`
2. Leave the patched target (or reverted target, on escalation) in the working tree, uncommitted.
3. Return in chat a compact courier summary for the commissioning CA: status, findings count, blocking-finding one-liners, diff stat, advisory verdict, residual risk, and the report path.
4. If any gate blocks, return the precise blocker (`BLOCKED_CONTROLLER_NOT_DECORRELATED`, `BLOCKED_STALE_TARGET`, `BLOCKED_STALE_BASE`, blocked-dirty/worktree, `FAILED_REVIEW_OUTPUT_WRITE`) instead of a partial pass.

## Adjudication (not yours)

The commissioning home model (CA) adjudicates your working-tree diff before anything is kept — accept, modify, or reject per change against your citations and the artifact's intent, reverting rejected hunks, with discretionary veto over any change. Your diff, citations, and verdict are decision input only; they are not validation, readiness, approval, formal review authority, or a keep decision.

## Non-Claims

This commission runs under a provisional, opt-in convention; it creates no formal review lane, no validation, readiness, proof, or lifecycle claim. Advisory claim level throughout (the formal Orca review lane is not invocable in your runtime). No runtime model is named, recommended, ranked, or routed; de-correlation is a who-constraint recorded at dispatch. No commit, push, PR, install, or deployment authority. The target remains PROPOSED pending commissioning-lane adjudication and owner word regardless of this pass's outcome.
