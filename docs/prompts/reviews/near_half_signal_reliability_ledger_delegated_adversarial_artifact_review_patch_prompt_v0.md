# Delegated Adversarial Artifact Review + Bounded Patch — Near-Half Signal-Reliability Ledger v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (review family; delegated review-and-patch commission under the provisional convention)
scope: >
  Controller prompt for a de-correlated, cross-vendor adversarial artifact
  review WITH bounded patch authority on the signal-reliability ledger schema +
  discipline contract — its firewall-clean pre-committed-use unit, the K-of-N
  report-all cherry-pick guard, the N7 field map, and the product-learning /
  no-source-family-promotion caps — returning a durable findings report, an
  uncommitted working-tree diff, neutral per-change citations, a verdict, and a
  residual-risk note for home-model adjudication.
use_when:
  - Executing this commissioned controller pass in a non-Anthropic-vendor lane with repo access.
  - Adjudicating the returned diff and report (home model recalls the commission bounds).
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - forseti/product/spines/judgment/learning_loops/near_half/near_half_signal_reliability_ledger_v0.md
input_hashes:
  docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md: 388352b83bac9860c3b9959d93af3d04d0c9ccfb69198cd9382f2fbe0a498102 (SHA256 over git blob bytes at 3fe878c, per the bound hash convention; not CRLF working-tree bytes)
branch_or_commit: signal-reliability-ledger-hardening-v0 off origin/main @ 700c1ba (re-pinned 2026-06-13 after #54 landed; the ledger content is unchanged — blob hash still 388352b8 — only the now-merged #54 branch pin was stale). This review is a FOLLOW-UP hardening pass on the LANDED ledger.
stale_if:
  - The target file hash changes before the run starts (re-issue with a fresh pin).
  - Home-model adjudication for this commission completes (historical thereafter).
```

## Commission

Explicit commission under the **provisional** Delegated Review-and-Patch
convention. Operating contract: `.agents/workflow-overlay/delegated-review-patch.md`
— read first; binding for this run. Access: `repo`. Mode: base-subagent.

Why read-only review is insufficient: this ledger is the **shared interface both
halves of the judgment loop depend on** — the far-half emits to it, the near-half
postmortem (step 3) populates it, and decision-memory consumes it. Its author
(the home model) also authored the far-half it reconciles (N7) and the batch-1
discipline it generalizes, so a self-consistent-but-wrong firewall unit,
cherry-pick guard, or cap is a correlated blind spot. A de-correlated combined
review-and-patch pass hardens it before the architecture (step 2) and postmortem
(step 3) build on it.

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
  — the lane worktree, NOT the primary `...\projects\orca` checkout (different
  branch, unrelated dirty work). `cd` here first.
- Branch: `signal-reliability-ledger-hardening-v0` (off `origin/main @ 700c1ba`; #54 already landed, so this is a follow-up hardening pass and its result is a NEW patch PR). The ledger file must be present on this branch (it is, from main).
- Target (the ONLY file you may patch):
  `docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md`
- Target SHA256 (git blob bytes at `3fe878c`):
  `388352b83bac9860c3b9959d93af3d04d0c9ccfb69198cd9382f2fbe0a498102`
  (compute via `git cat-file blob <rev>:<path>` piped to sha256 in code, NOT
  `Get-FileHash` on the CRLF working tree).
- Dirty-state: clean at start. Your only permitted writes: (a) the target file,
  (b) the new report file named below. **No commit, no push, no staging, no
  branch operations.**
- Any precondition failure → return a blocked result naming the failed check.

Record at run start (orca_start_preflight): agents_read, overlay_read,
source_pack (below), edit_permission `patch-only (single named target) + report
file-write`, target_scope, dirty_state_checked, repo_map_decision: `not_needed`,
external-source boundary (`jb` is not Orca authority).

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
   verdict authority, no validation/readiness claims) — state this explicitly.
   The deep-thinking step is replaced by a mandatory **reasoning-before-findings
   pass** (load-bearing claims, decision criteria, failure modes — first).
3. **SOURCE-LOAD** (bounded; do not bulk-load beyond this list):
   - the target file (full read);
   - `docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md`
     — verify the N7 field map matches the architecture's named interface
     field-for-field (this is the load-bearing reconciliation claim);
   - `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md`
     — verify the K-of-N / report-all / org-motion-not-promoted discipline is
     faithfully generalized, not distorted;
   - `docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md`
     — verify the product-learning cap and that no tier/ladder vocabulary is
     minted;
   - `orca-harness/schemas/judgement_models.py` — verify the `EvidenceUsed` /
     signal vocabulary claims (claim_text, claim_role, evidence_unit_ids).
   Default exclusions: research corpus, other harness code, review outputs,
   other prompts, `_inbox`.
4. Declare **`SOURCE_CONTEXT_READY`** (or `SOURCE_CONTEXT_INCOMPLETE` with named
   gaps; findings may proceed advisory-only with gaps labeled).
5. Only then **APPLY**: reasoning-before-findings, adversarial checks, findings,
   bounded patch.

## Fitness Reference (attack the bar itself too)

The ledger's job: **define a signal-reliability record that cannot launder
hindsight into a "validated" signal and cannot be cited above product-learning.**
Observable signal: the pre-committed-use unit genuinely anchors the predicted
direction in the blind pre-reveal call (no post-reveal direction can count); the
K-of-N report-all rule actually closes the cherry-pick channel; the caps bar
source-family promotion (JSG-01 frozen); and the N7 field map matches the
architecture exactly. If the bar itself is wrong or gameable, say so as a finding.

```yaml
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: goal_handoff.anchor_goal
  output_fit_check: goal_handoff.success_signal.core_success.output_fit
  target_delta_from_prior:
    status: changed
    changed_fields: [anchor_goal]
    summary: Owner redirected the build to the near-half (backtest-learning) foundation; far-half is parked infrastructure. This is step 1 of 3 (signal-reliability ledger).
  drift_guard: "Do not let the review promote a signal, populate real rows, mint ladder vocabulary, or push the ledger past product-learning; harden the schema + discipline only."
  conflict_behavior: call_out_conflict_before_proceeding
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
```

## Review Purpose (commission-bound; be maximally adversarial within it)

- **Firewall integrity of the unit:** can any reading let a signal's predicted
  direction be recorded or counted *post-reveal*? Does the pre-committed-use
  definition actually anchor the direction in the blind call? Is the
  "confirmed tell → excluded" rule airtight?
- **Cherry-pick guard completeness:** is K-of-N report-all genuinely
  un-gameable here, or is there a seam (defining "correct_direction" loosely,
  choosing which cases pre-commit a signal, small-N presented as strong,
  not_applicable/unscoreable used as an escape hatch)?
- **Cap integrity:** does anything let a good tally promote/admit a
  source-family (JSG-01), or be cited as buyer-proof / judgment-quality? Is
  "product-learning" the genuine ceiling everywhere?
- **N7 reconciliation correctness:** does the field map actually match the
  far-half architecture's named N7 interface field-for-field? A mismatch is a
  real defect (it would mean N7 is NOT closed).
- **Vocabulary fidelity:** are `signal_id` / `decision_family` / the harness
  evidence fields used consistently with their owning sources (no silent
  rename — this exact defect occurred on a prior slice)?
- Plus standard checks: authority conformance, internal consistency, downstream
  executability (could the step-3 postmortem and decision-memory actually
  consume this?), overclaims, scope discipline (overreach AND underfix),
  `jb`/external leakage.

Do not retarget, widen, or redesign. Design-level defects → escalation.

## Bounded Patch Scope

- Patch **only** the named target, working tree, uncommitted. Smallest complete
  fix per kept finding.
- The patch must not weaken: PROPOSED status, the non-claims, the
  product-learning cap, the no-source-family-promotion / JSG-01-frozen boundary,
  the firewall-clean unit, or the report-all rule.
- Everything else read-only / flag-only (architecture, batch-1, ladder, harness,
  overlay files, safety-rules-forbidden paths). Fixes belonging in those sources
  are flagged findings, never edits. A genuine N7 field mismatch is a flagged
  finding (it would require an architecture reconciliation), not a silent ledger
  edit that hides the mismatch.
- **Escalation valve:** design-level problem → `NEEDS_ARCHITECTURE_PASS`, stop
  patching, revert any partial diff, findings only.

## Output Contract

Output mode: `review-report` plus the working-tree patch.

1. Write the durable report to
   `docs/review-outputs/adversarial-artifact-reviews/near_half_signal_reliability_ledger_delegated_adversarial_artifact_review_v0.md`
   BEFORE the chat summary. Write failure → `FAILED_REVIEW_OUTPUT_WRITE`,
   `review_location: chat_only_current_thread`, no `report_path`.
2. Report contents: compact `review_summary`; the explicit advisory-only bound;
   the reasoning-before-findings pass; findings (critical → major → minor; each
   with severity, location, issue, evidence citing target section AND
   conflicting authority excerpt, impact, `minimum_closure_condition`,
   `next_authorized_action`, advisory remediation); the **unified diff** (or
   `no patch` / `NEEDS_ARCHITECTURE_PASS` with reverted state); **per-change
   neutral citations**; verdict-as-decision-input; residual-risk note;
   provenance `authored_by: claude-fable-5[1m]`, `reviewed_by: <operator-supplied
   model+version, or unrecorded>`; non-claims.
3. Chat return after successful write: compact courier summary only.
4. Leave exactly two working-tree changes: the patched target (if any) and the
   report. The home model adjudicates hunk-by-hunk against your citations;
   rejected hunks are reverted by the home lane.

## Non-Claims

Advisory decision input for the commissioning Chief Architect. Creates no
validation, readiness, acceptance, source-family admission, or formal
review-lane claim; the target stays PROPOSED at product-learning tier regardless
of verdict. De-correlation is commission provenance, not runtime model routing.
