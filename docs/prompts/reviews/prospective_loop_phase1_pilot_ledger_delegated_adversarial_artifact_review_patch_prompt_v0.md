# Delegated Adversarial Artifact Review + Bounded Patch — Phase-1 Pilot Ledger Doctrine v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (review family; delegated review-and-patch commission under the provisional convention)
scope: >
  Controller prompt for a de-correlated, cross-vendor adversarial artifact
  review WITH bounded patch authority on the DOCTRINE of the Phase-1 dogfood
  pilot ledger DRAFT — its authorization basis, selection criteria, run-shape
  fidelity, firewall preservation, and claim caps — returning a durable
  findings report, an uncommitted working-tree diff, neutral per-change
  citations, a verdict-as-decision-input, and a residual-risk note for
  home-model adjudication. The OWNER-FILL decision-list slots are out of scope.
use_when:
  - Executing this commissioned controller pass in a non-Anthropic-vendor lane with repo access.
  - Adjudicating the returned diff and report (home model recalls the commission bounds).
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - docs/decisions/prospective_decision_loop_phase1_dogfood_pilot_ledger_v0.md
input_hashes:
  docs/decisions/prospective_decision_loop_phase1_dogfood_pilot_ledger_v0.md: 01fbb24ae96625462f0c9816c5bbfd642965cc9ad84ced6cc4791499ca2ec97e (SHA256 over git blob bytes at f53c8c0, per the bound hash convention; not CRLF working-tree bytes)
branch_or_commit: prospective-loop-phase1-pilot-ledger-v0 @ f53c8c0 (PR #48, base main @ d6d360e)
stale_if:
  - The target file hash changes before the run starts (re-issue with a fresh pin).
  - Home-model adjudication for this commission completes (historical thereafter).
  - The owner fills the decision list before this review runs (then the post-fill check is also in scope).
```

## Commission

Explicit commission under the **provisional** Delegated Review-and-Patch
convention. Operating contract: `.agents/workflow-overlay/delegated-review-patch.md`
— read first; binding for this run. Access: `repo`. Mode: base-subagent.

Why read-only review is insufficient: the target is the decision record whose
signature first authorizes a real sealed call — the threshold from paper to
operation. Its author (the home model) also authored the architecture and
semantics it consumes, so a self-consistent-but-unsafe authorization basis,
selection criterion, or run-shape detail is a correlated blind spot. A
de-correlated combined review-and-patch pass hardens the doctrine before the
owner signs.

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
  — this is the lane worktree, NOT the primary `...\projects\orca` checkout
  (that one is on a different branch with unrelated dirty work). `cd` here first.
- Branch: `prospective-loop-phase1-pilot-ledger-v0` (PR #48). `git log` must show `f53c8c0`.
- Target (the ONLY file you may patch):
  `docs/decisions/prospective_decision_loop_phase1_dogfood_pilot_ledger_v0.md`
- Target SHA256 (git blob bytes at `f53c8c0`):
  `01fbb24ae96625462f0c9816c5bbfd642965cc9ad84ced6cc4791499ca2ec97e`
  (compute via `git cat-file blob <rev>:<path>` piped to sha256 in code, NOT
  `Get-FileHash` on the CRLF working tree).
- Dirty-state: clean at start. Your only permitted writes: (a) the target file,
  (b) the new report file named below. **No commit, no push, no staging, no
  branch operations.**
- Any precondition failure → return a blocked result naming the failed check;
  do not switch, clone, or review a substitute.

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
   verdict authority, no validation/readiness claims) — state this bound
   explicitly. The deep-thinking step is replaced by a mandatory
   **reasoning-before-findings pass** (load-bearing claims, decision criteria,
   failure modes — before any finding).
3. **SOURCE-LOAD** (bounded; do not bulk-load beyond this list):
   - the target file (full read);
   - `docs/product/judgment_spine/prospective_decision_loop_phase0_semantics_spec_v0.md`
     (the book — verify the ledger's run-shape claims match its hardened entry
     mechanics and dual-hash chain; the ledger must not re-derive or contradict
     them);
   - `docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md`
     (firewall invariants, shadow-first, ladder caps — verify the ledger
     preserves them);
   - `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md`
     (the anti-cherry-pick / report-all / dated-amendment exemplar the ledger is
     modeled on — verify the modeling is faithful, not just cosmetic).
   Default exclusions: research corpus, harness code, review outputs, other
   prompts, `_inbox`.
4. Declare **`SOURCE_CONTEXT_READY`** (or `SOURCE_CONTEXT_INCOMPLETE` with
   named gaps; findings may proceed advisory-only with gaps labeled).
5. Only then **APPLY**: reasoning-before-findings, adversarial checks, findings,
   bounded patch.

## Fitness Reference (attack the bar itself too)

The ledger's job: **be safe for the owner to sign and then run a real decision
through, without inventing semantics and without enabling cherry-picking or a
premature seal.** Observable signal: the authorization basis cannot be read as
authorizing a seal before signature or above product-learning; the selection
criteria are complete enough that a filled list cannot smuggle in selection bias
or self-reference; the run shape matches the book exactly; no firewall invariant
is weakened. If the bar itself is wrong or unmeasurable, say so as a finding
rather than inventing a different bar.

```yaml
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: goal_handoff.anchor_goal
  output_fit_check: goal_handoff.success_signal.core_success.output_fit
  target_delta_from_prior:
    status: unchanged
    changed_fields: []
    summary: Same build-out target; this is the pilot-ledger slice's pre-first-seal hardening review.
  drift_guard: "Do not let the review fill the owner-owned decision list or push the ledger past product-learning; harden the doctrine only."
  conflict_behavior: call_out_conflict_before_proceeding
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
```

## Review Purpose (commission-bound; be maximally adversarial within it)

- **Authorization basis:** can any reading authorize a seal before signature, or
  above product-learning, or treat the target as ratified when it is not? Is the
  ratification-pending handling coherent (proposed-stack semantics correct)?
- **Selection-criteria completeness:** do the 5 criteria actually close
  cherry-picking (fix-before-reveal) and self-reference? Is there a gap a filled
  list could exploit — e.g., a criterion that is unobservable, or a missing
  criterion (outcome independence? owner-vs-operator separation?)? Attack the
  criteria as the anti-bias mechanism.
- **Run-shape fidelity:** does the ledger's described folder/chain shape match
  the semantics spec's adjudication-hardened mechanics (actual_path entry,
  per-seal resolution, dual-hash) exactly? Any drift is a firewall defect.
- **Firewall preservation:** shadow-only correctly bars disclosure; org-blind
  sealing norm; breach route; single-operator residual disclosed not hidden.
- **Claim caps:** product-learning cap, non-gate-clearing surface, no minted
  vocabulary, no implied readiness.
- **OWNER-FILL boundary:** the decision-list slots are intentionally empty.
  **Do not fill them.** Flag only if their emptiness is itself unsafe (e.g., the
  ledger could be signed without them). The chosen list's content is a separate
  post-fill check, out of this scope.
- Plus standard checks: authority conformance, internal consistency, downstream
  executability (could an operator sign and run from this?), overclaims, scope
  discipline (overreach AND underfix), `jb`/external leakage.

Do not retarget, widen, or redesign. Design-level defects → escalation.

## Bounded Patch Scope

- Patch **only** the named target, working tree, uncommitted. Smallest complete
  fix per kept finding.
- The patch must not weaken: the `DRAFT_PENDING_OWNER_SIGNOFF` status, the
  non-claims, the product-learning cap, any firewall invariant, the
  no-seal-before-signature boundary, or the OWNER-FILL emptiness (do not fill
  the decision list or the sign-off block).
- Everything else read-only / flag-only (architecture, semantics spec, batch-1
  ledger, overlay files, safety-rules-forbidden paths). Fixes belonging upstream
  are flagged findings, never edits.
- **Escalation valve:** design-level problem → `NEEDS_ARCHITECTURE_PASS`, stop
  patching, revert any partial diff, findings only.

## Output Contract

Output mode: `review-report` plus the working-tree patch.

1. Write the durable report to
   `docs/review-outputs/adversarial-artifact-reviews/prospective_loop_phase1_pilot_ledger_delegated_adversarial_artifact_review_v0.md`
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
   model+version, or unrecorded>`; non-claims (advisory decision input only;
   provisional convention; nothing kept until home-model adjudication).
3. Chat return after successful write: compact courier summary only.
4. Leave exactly two working-tree changes: the patched target (if any) and the
   report. The home model adjudicates hunk-by-hunk against your citations;
   rejected hunks are reverted by the home lane.

## Non-Claims

Advisory decision input for the commissioning Chief Architect. Creates no
validation, readiness, acceptance, ratification, pilot authorization, or formal
review-lane claim; the target stays a `DRAFT_PENDING_OWNER_SIGNOFF` at
product-learning tier regardless of verdict. De-correlation is commission
provenance, not runtime model routing.
