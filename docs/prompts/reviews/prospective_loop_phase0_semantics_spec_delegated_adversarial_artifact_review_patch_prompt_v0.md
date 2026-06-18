# Delegated Adversarial Artifact Review + Bounded Patch — Phase-0 Semantics Spec v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (review family; delegated review-and-patch commission under the provisional convention; fused post-implementation handoff)
scope: >
  Controller prompt for a de-correlated, cross-vendor adversarial artifact
  review WITH bounded patch authority on the single named target
  (prospective_decision_loop_phase0_semantics_spec_v0.md), returning a durable
  findings report, an uncommitted working-tree diff, neutral per-change
  citations, a verdict-as-decision-input, and a residual-risk note for
  home-model adjudication.
use_when:
  - Executing this commissioned controller pass in a non-Anthropic-vendor lane with repo access.
  - Adjudicating the returned diff and report (home model recalls the commission bounds).
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - orca/product/spines/judgment/learning_loops/far_half/prospective_decision_loop_phase0_semantics_spec_v0.md
input_hashes:
  docs/product/judgment_spine/prospective_decision_loop_phase0_semantics_spec_v0.md: 0eb599c15a99182f2d2c8870bbd786bfcd8592837e513d50d0ab116ea30f7e10 (SHA256 over git blob bytes at a3ddd6d, per the bound hash convention; not CRLF working-tree bytes)
branch_or_commit: phase0-semantics-spec-v0 @ a3ddd6d (PR #46, base main @ 64c442a)
stale_if:
  - The target file hash changes before the run starts (re-issue with a fresh pin).
  - Home-model adjudication for this commission completes (historical thereafter).
```

## Commission

Explicit commission under the **provisional** Delegated Review-and-Patch
convention, triggered as the fused turn's post-implementation handoff
(`adversarial_review: recommended`, checkpoint `after_all_steps_pre_closeout`).
Operating contract: `.agents/workflow-overlay/delegated-review-patch.md` — read
first; binding for this run. Access: `repo`. Mode: base-subagent.

Why read-only review is insufficient: the target is the hand-runnable semantics
contract for the prospective decision loop — the artifact a Phase-1 operator
will execute literally. Its author (the home model) also authored the
architecture it operationalizes, so ambiguity and self-consistent-but-wrong
fill-rules are correlated blind spots; a de-correlated combined review-and-patch
pass fixes them before the owner signs anything that depends on this spec.

## Actor / Model-Family Receipt (verify before any work)

```yaml
actor_model_family_receipt:
  author_home_model_family: Anthropic / Claude (authored_by claude-fable-5[1m]; also adjudicates)
  controller_model_family: REQUIRED non-Anthropic vendor lineage; operator records concrete model+version at run start
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: verify_at_run_start
```

Who-constraint, not a model recommendation. Vendor = upstream model developer.
If your lineage is Anthropic or unknown/undisclosed: STOP, return
`BLOCKED_CONTROLLER_NOT_DECORRELATED`. No tester/testee shortcut; you are the
controller — do not dispatch subagents or a replacement controller.

## Worktree Preflight (fail loud; never review a substitute checkout)

- Workspace: `C:\Users\vmon7\Desktop\projects\orca-worktrees\orca-prospective-loop-wt`
- Branch: `phase0-semantics-spec-v0` (PR #46). `git log` must show `a3ddd6d`.
- Target (the ONLY file you may patch):
  `docs/product/judgment_spine/prospective_decision_loop_phase0_semantics_spec_v0.md`
- Target SHA256 (git blob bytes at `a3ddd6d`, per the convention recorded in
  the target itself and in the portable-method header):
  `0eb599c15a99182f2d2c8870bbd786bfcd8592837e513d50d0ab116ea30f7e10`
- Dirty-state: clean at start (the commissioning prompt file itself, committed,
  is expected in history). Your only permitted writes: (a) the target file,
  (b) the new report file named below. **No commit, no push, no staging, no
  branch operations** — the diff stays in the working tree for adjudication.
- Any precondition failure → return a blocked result naming the failed check.

Record at run start (orca_start_preflight): agents_read, overlay_read,
source_pack (listed below), edit_permission `patch-only (single named target) +
report file-write`, target_scope, dirty_state_checked, repo_map_decision:
`not_needed` (sources named explicitly), external-source boundary (`jb` is not
Orca authority).

## Source-Gated Method Contract (sequence is binding)

1. **Authority reads:** `AGENTS.md`; `.agents/workflow-overlay/README.md`;
   `.agents/workflow-overlay/source-of-truth.md`;
   `.agents/workflow-overlay/source-loading.md`;
   `.agents/workflow-overlay/review-lanes.md`;
   `.agents/workflow-overlay/prompt-orchestration.md`;
   `.agents/workflow-overlay/validation-gates.md`;
   `.agents/workflow-overlay/delegated-review-patch.md` (your contract).
2. **REFERENCE-LOAD the review method** (do not APPLY yet):
   `docs/prompts/templates/review/adversarial_artifact_review_v0.md` +
   `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`.
   The Orca review skills are not invocable in your runtime → your result is
   **advisory-only decision input** (findings + recommendation; no formal
   verdict authority, no validation/readiness claims) — state this bound
   explicitly. The deep-thinking step is replaced by a mandatory
   **reasoning-before-findings pass** (load-bearing claims, decision criteria,
   failure modes — before any finding).
3. **SOURCE-LOAD** (bounded; do not bulk-load beyond this list):
   - the target file (full read);
   - `docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md`
     (the landed adjudicated architecture the spec operationalizes — check
     fill-rules against its invariants and adjudicated AR-01/02/03 rules);
   - `orca-harness/schemas/judgement_models.py` (verify the vocabulary trace
     table claims field-for-field — this is a load-bearing check);
   - `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md`
     (targeted: Screen Provenance section, which the worked example cites).
   Default exclusions: research corpus, other harness code, review outputs,
   other prompts, `_inbox`.
4. Declare **`SOURCE_CONTEXT_READY`** (or `SOURCE_CONTEXT_INCOMPLETE` with
   named gaps; findings may proceed advisory-only with gaps labeled).
5. Only then **APPLY**: reasoning-before-findings, adversarial checks,
   findings, bounded patch.

## Fitness Reference (attack the bar itself too)

The spec's own completeness test: **a by-hand operator can run a real decision
through intake → seal → (disclose) → resolve using only this document, with
zero invented semantics.** Observable signal: every field has a fill-rule
(filled-by / when / from-what / filled-means) concrete enough to execute; the
worked example is consistent with every fill-rule it exercises; the chain/hash
mechanics are operable exactly as written. If the bar itself is wrong or
unmeasurable, say so as a finding rather than inventing a different bar.

```yaml
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: goal_handoff.anchor_goal
  output_fit_check: goal_handoff.success_signal.core_success.output_fit
  target_delta_from_prior:
    status: changed
    changed_fields: [anchor_goal, success_signal]
    summary: Prior target (hardening pass on PR #34) achieved; owner activated the build-out target ("this lane will be building it out").
  drift_guard: "Do not substitute 'more architecture' or 'any code' for hand-runnable Phase-0 specs; consume the target, build only the N-column, and stop at every owner gate (PR landing, pilot-ledger signature)."
  conflict_behavior: call_out_conflict_before_proceeding
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
```

## Review Purpose (commission-bound; be maximally adversarial within it)

- **Hand-runnability:** attack every fill-rule an operator could not execute
  without inventing semantics — ambiguous filled-means, missing filled-by,
  judgment smuggled into "mechanical" resolution criteria.
- **Vocabulary-trace fidelity:** verify the trace table against
  `judgement_models.py` field-for-field; flag any silent rename, range drift
  (0–8), or unmapped name. The action-vocabulary decision (ladder=scale,
  labels=satellite) must be internally coherent with band-claim reuse.
- **Firewall/cap compliance of the fill-rules:** do the entry mechanics, chain
  rule, breach routes, update semantics, and disclosure rules preserve the
  landed architecture's invariants (seal-before-disclose; pre-outcome re-seals
  only, never replacement; presentation ≠ disclosure; quarantine-as-data)? Can
  any fill-rule path let post-outcome or post-disclosure material gain forecast
  standing?
- **Example completeness:** every schema field exercised; every example value
  consistent with its own fill-rule; the `example_not_a_sealed_decision` label
  effective against future evidence-citation.
- **Claim discipline:** proposed-home worded as proposal; no implied pilot
  authorization, ratification, or evidence tier anywhere.
- Plus the method's standard checks: authority conformance, internal
  consistency, downstream executability, overclaims, scope discipline
  (overreach AND underfix), `jb`/external leakage.

Do not retarget, widen, or redesign. Design-level defects → escalation.

## Bounded Patch Scope

- Patch **only** the named target, working tree, uncommitted. Smallest complete
  fix per kept finding; no restructuring for taste.
- The patch must not weaken: PROPOSED status, the non-claims, the
  product-learning cap, any firewall invariant, the proposal-not-binding
  wording of the ledger home, or the example's non-evidence label.
- Everything else read-only / flag-only (all other Orca sources, overlay files,
  the architecture, harness code, safety-rules-forbidden paths). Fixes that
  belong in the architecture are flagged findings, never edits.
- **Escalation valve:** design-level problem → `NEEDS_ARCHITECTURE_PASS`, stop
  patching, revert any partial diff, findings only.

## Output Contract

Output mode: `review-report` plus the working-tree patch.

1. Write the durable report to
   `docs/review-outputs/adversarial-artifact-reviews/prospective_loop_phase0_semantics_spec_delegated_adversarial_artifact_review_v0.md`
   BEFORE the chat summary. Write failure → `FAILED_REVIEW_OUTPUT_WRITE`,
   `review_location: chat_only_current_thread`, no `report_path`.
2. Report contents: compact `review_summary`; the explicit advisory-only bound;
   the reasoning-before-findings pass; findings (critical → major → minor; each
   with severity, location, issue, evidence citing target section AND
   conflicting authority excerpt, impact, `minimum_closure_condition`,
   `next_authorized_action`, advisory remediation); the **unified diff** (or
   `no patch` / `NEEDS_ARCHITECTURE_PASS` with reverted state); **per-change
   neutral citations** (decision-sufficient, no advocacy);
   verdict-as-decision-input; residual-risk note; provenance
   `authored_by: claude-fable-5[1m]`, `reviewed_by: <operator-supplied
   model+version, or unrecorded>`; non-claims (advisory decision input only;
   provisional convention; nothing kept until home-model adjudication).
3. Chat return after successful write: compact courier summary only.
4. Leave exactly two working-tree changes: the patched target (if any) and the
   report. The home model adjudicates hunk-by-hunk against your citations;
   rejected hunks are reverted by the home lane.

## Non-Claims

Advisory decision input for the commissioning Chief Architect. Creates no
validation, readiness, acceptance, ratification, pilot authorization, or formal
review-lane claim; the target stays PROPOSED at product-learning tier
regardless of verdict. De-correlation is commission provenance, not runtime
model routing.
