# Delegated Adversarial Artifact Review + Bounded Patch — Prospective Decision Loop Target Architecture v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (review family; delegated review-and-patch commission under the provisional convention)
scope: >
  Controller prompt for a de-correlated, cross-vendor adversarial artifact
  review WITH bounded patch authority on the single named target
  (prospective_decision_loop_target_architecture_v0.md), returning a durable
  findings report, an uncommitted working-tree diff, neutral per-change
  citations, a verdict-as-decision-input, and a residual-risk note for
  home-model adjudication.
use_when:
  - Executing this commissioned controller pass in a non-Anthropic-vendor lane with repo access.
  - Adjudicating the returned diff and report (home model reads this to recall the commission bounds).
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md
input_hashes:
  docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md: 64A4274EBA1950264629940C5B06B3749FFF0B1CA12B71E8CE1CE1D2D3FE17CD
branch_or_commit: prospective-decision-loop-architecture-v0; target-bearing commit 9de7561 (PR #34)
stale_if:
  - The target file hash changes before the run starts (re-issue the prompt with a fresh pin).
  - The home-model adjudication for this commission completes (this prompt becomes historical).
```

## Commission

This is an explicit Chief Architect commission under the **provisional**
Delegated Review-and-Patch convention. Your operating contract is
`.agents/workflow-overlay/delegated-review-patch.md` — read it first and treat
it as binding for this run. Access mode: `repo` (you read and patch in the
pinned worktree). Mode: base-subagent (you are the single controller; no
executor split).

Why source-read-only review is insufficient: the target is a high-stakes
authored doctrine artifact whose author (the home model) encodes the very
guardrails under review — firewall translation, evidence-ladder caps,
dependency sequencing — and can reintroduce exactly the failure modes those
guardrails exist to prevent. A de-correlated combined review-and-patch pass
catches and fixes correlated blind spots before the owner ratifies.

## Actor / Model-Family Receipt (verify before any work)

```yaml
actor_model_family_receipt:
  author_home_model_family: Anthropic / Claude (authored_by claude-fable-5[1m]; the home model also adjudicates)
  controller_model_family: REQUIRED non-Anthropic vendor lineage; operator records the concrete model+version at run start
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: verify_at_run_start
```

This is a **who-constraint of the commission, not a model recommendation or
ranking**. Vendor = upstream model developer, not hosting platform or wrapper.
If your vendor lineage is Anthropic, or unknown/undisclosed, STOP and return
`BLOCKED_CONTROLLER_NOT_DECORRELATED` — do not review. Do not delegate this
review to subagents (no tester/testee shortcut); you are the controller and you
do not dispatch a replacement.

## Worktree Preflight (fail loud; never review a substitute checkout)

- Workspace: `C:\Users\vmon7\Desktop\projects\orca-worktrees\orca-prospective-loop-wt`
- Branch: `prospective-decision-loop-architecture-v0` (PR #34). `git log` must
  show commit `9de7561` in history.
- Target (the ONLY file you may patch):
  `docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md`
- Target SHA256 (working-tree bytes, CRLF): `64A4274EBA1950264629940C5B06B3749FFF0B1CA12B71E8CE1CE1D2D3FE17CD`
- Dirty-state allowance: the working tree must be clean at start (untracked
  files out of scope). Your only permitted writes: (a) the target file, (b) the
  new durable report file named below. **No commit, no push, no staging, no
  branch operations** — the diff stays in the working tree for adjudication.
- On any precondition failure (wrong worktree, branch, missing commit, hash
  mismatch, dirty start, inaccessible path): return a blocked result naming the
  failed check. Do not proceed, do not clone, do not switch.

Record at run start (orca_start_preflight): agents_read, overlay_read,
source_pack (custom, listed below), edit_permission `patch-only (single named
target) + report file-write`, target_scope, dirty_state_checked,
repo_map_decision: `not_needed` (all sources are named explicitly here),
external-source boundary: external workflow source is read-only; `jb` is not
Orca authority.

## Source-Gated Method Contract (sequence is binding)

1. **Authority reads:** `AGENTS.md`; `.agents/workflow-overlay/README.md`;
   `.agents/workflow-overlay/source-of-truth.md`;
   `.agents/workflow-overlay/source-loading.md`;
   `.agents/workflow-overlay/review-lanes.md`;
   `.agents/workflow-overlay/prompt-orchestration.md`;
   `.agents/workflow-overlay/validation-gates.md`;
   `.agents/workflow-overlay/delegated-review-patch.md` (your contract).
2. **REFERENCE-LOAD the review method** (do not APPLY yet):
   `docs/prompts/templates/review/adversarial_artifact_review_v0.md` plus
   `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`.
   Method note: the Orca review skills (`workflow-deep-thinking`,
   `workflow-adversarial-artifact-review`) are not invocable in your runtime.
   Therefore (a) your result is **advisory-only decision input** — findings
   plus recommendation; no formal verdict authority, no blocked/ready status,
   no validation or readiness claims — state this bound explicitly in your
   report; (b) the deep-thinking step is replaced by a mandatory
   **reasoning-before-findings pass**: enumerate the target's load-bearing
   claims, boundary/decision criteria, and likely failure modes before listing
   any finding. (Provenance note recorded by the commissioning lane: the
   portable distilled method was NOT shipped — its freshness gate failed, both
   `derived_from` pins predate 2026-06-12 changes to the live sources; you have
   repo access, so the live sources above govern.)
3. **SOURCE-LOAD** (bounded; do not bulk-load beyond this list):
   - the target file (full read);
   - its three `open_next` doctrine sources:
     `docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md`,
     `docs/product/judgment_spine/conductor_construction_integrity_probe_addendum_v1.md`,
     `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md`;
   - `.agents/workflow-overlay/product-proof.md` (the target maps assisted-mode
     evidence onto buyer-proof semantics; verify against the owner).
   Default exclusions: research corpus, harness code, review outputs, other
   prompts, `_inbox`. Note for your authority check: the target asserts the
   near-half plan (signal-reliability ledger) has NO durable repo artifact —
   verify that absence claim cheaply (search), since the target's
   decision-memory interface depends on it.
4. Declare **`SOURCE_CONTEXT_READY`** (or `SOURCE_CONTEXT_INCOMPLETE` with the
   named gaps; if incomplete, findings may proceed advisory-only with the gaps
   labeled).
5. Only then **APPLY**: the reasoning-before-findings pass, then the method's
   adversarial review checks, then findings, then the bounded patch.

## Fitness Reference And Thread Operating Target

Fitness reference (intent-bearing target — attack the goal and signal
themselves; never treat as a pass-if-matches bar): the target artifact must let
the owner make a ratify/amend/reject decision on a counterparty-safe operational
decision loop. Observable signal: each section survives adversarial probing on
(1) firewall integrity into shadow/assisted mode, (2) evidence-ladder cap
compliance with zero minted vocabulary, (3) dependency-map correctness (nothing
counterparty-blocked misfiled as now-buildable, and vice versa), (4)
core/satellite boundary clarity — while remaining PROPOSED at product-learning
tier with its non-claims intact.

```yaml
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: goal_handoff.anchor_goal
  output_fit_check: goal_handoff.success_signal.core_success.output_fit
  target_delta_from_prior:
    status: prior_target_not_supplied
    changed_fields: []
    summary: First explicit goal frame in this thread; the earlier commission's deliverable (authoring + PR) is complete, so this target governs the hardening pass.
  drift_guard: "Do not let the hardening pass become a second architecture-authoring pass or an implementation start; harden the existing artifact only."
  conflict_behavior: call_out_conflict_before_proceeding
goal_handoff:
  long_term_goal: Doctrine-consistent operational decision loop, built in counterparty-safe order, firewall and ladder caps intact.
  anchor_goal: PR #34's target-architecture artifact hardened via de-correlated different-family review with home-model adjudication, so the owner ratifies/amends/rejects a stress-tested version.
  success_signal:
    core_success:
      owner_observable: Review findings + kept/rejected adjudication + bounded patch (or reasoned no-patch) visible on the lane/PR.
      output_fit: Kept findings improve firewall integrity, ladder-cap compliance, dependency-map correctness, or core/satellite boundary clarity — not length or hedging.
      boundary: Ceremony completion, claim inflation, firewall weakening, or implied acceptance do not count; artifact remains PROPOSED at product-learning tier.
      drift_cue: Redesign-from-scratch, edits beyond the one artifact, building loop components, or unadjudicated delegate verdicts.
    secondary_success_signals:
      - Generalizable defects captured, not silently patched.
      - Lane CI green after any patch commit.
  status: user_stated
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
```

## Review Purpose (commission-bound; be maximally adversarial within it)

Attack the target as the doctrine artifact the owner will ratify:

- **Firewall integrity:** does seal-before-disclose actually close the three
  named risk relocations (disclosure, resolution, post-hoc editing)? Can any
  path in the schema or protocols let post-disclosure or post-outcome material
  acquire forecast standing? Does the mode pre-declaration really close the
  cherry-pick channel?
- **Evidence-ladder cap compliance:** does any section mint tier/closeout
  vocabulary, imply a cleared gate, or let assisted-mode adoption evidence
  masquerade as judgment evidence? Is the buyer-proof mapping faithful to
  `product-proof.md` and the ladder's promotion rules?
- **Dependency-map correctness:** is every "now-specifiable" item truly
  counterparty-independent? Is anything counterparty-blocked actually
  pre-specifiable (or vice versa)? Is the dogfood pilot (N8) honestly bounded?
- **Core/satellite boundary:** leakage either way; anything counterparty-bound
  hardened into core.
- Plus the method's standard checks: authority/hierarchy conformance, internal
  consistency, missing inputs/unbound roles, downstream executability (can a
  Phase-0 spec author and a Phase-1 pilot operator act on this?), overclaims,
  scope discipline (overreach AND underfix), `jb`/external leakage.

Do not retarget, widen, or redesign. A design-level defect routes to
escalation, not to a rewrite.

## Bounded Patch Scope

- You may patch **only** the single named target file, in the working tree,
  uncommitted. Smallest complete fix per kept finding; no redesign; no
  restructuring for taste.
- The patch must not weaken: the PROPOSED status, the non-claims, the
  product-learning cap, the firewall invariants, or the routed-out boundary
  (changes the artifact routes to owners stay routed, not enacted).
- Everything else is **read-only / flag-only**: all other Orca sources,
  overlay files, `AGENTS.md`/`CLAUDE.md`, decisions, templates, and every
  safety-rules-forbidden path. A finding whose fix lies outside the target is
  returned as a flagged finding, never an edit.
- **Escalation valve:** on a design-level problem, return
  `NEEDS_ARCHITECTURE_PASS`, stop patching, revert any partial diff, and
  return findings only.

## Output Contract

Output mode: `review-report` (durable report) plus the working-tree patch.

1. Write the durable report to
   `docs/review-outputs/adversarial-artifact-reviews/prospective_decision_loop_architecture_delegated_adversarial_artifact_review_v0.md`
   BEFORE returning your chat summary. If the write fails, return
   `FAILED_REVIEW_OUTPUT_WRITE` with `review_location: chat_only_current_thread`
   and no `report_path`.
2. The report must contain:
   - a compact `review_summary` block (status, one-line recommendation,
     findings_count, blocking_findings, advisory_findings, summary);
   - the explicit advisory-only bound (formal Orca review tooling not available
     in your runtime);
   - the reasoning-before-findings pass (load-bearing claims, decision
     criteria, failure modes);
   - findings ordered critical → major → minor, each with: severity, location,
     issue, evidence (cite the target section AND the conflicting authority
     excerpt), impact, `minimum_closure_condition` (required end state, not
     implementation), `next_authorized_action`, advisory remediation direction;
   - the **unified diff** of your working-tree patch (or `no patch` /
     `NEEDS_ARCHITECTURE_PASS` with reverted state);
   - **per-change neutral citations** — factual source evidence per hunk, no
     advocacy; decision-sufficient so the adjudicator's veto is informed;
   - a **verdict-as-decision-input** and a **residual-risk note** (your
     argument lives here, not in the citations);
   - provenance fields: `authored_by: claude-fable-5[1m]`;
     `reviewed_by: <operator-supplied model+version, or unrecorded>` — never
     fabricated;
   - non-claims: advisory decision input only; not validation, readiness,
     acceptance, formal verdict authority, or mandatory remediation; the
     convention is provisional; nothing is kept until home-model adjudication.
3. Chat return after a successful report write: compact courier summary only
   (report path, findings count, patch/no-patch/escalation state, residual
   one-liner). The durable report carries the review value.
4. Leave the worktree with exactly two changes: the patched target (if any
   patch) and the new report file. The home model adjudicates the diff
   hunk-by-hunk against your citations before anything is kept; rejected hunks
   are reverted by the home lane.

## Non-Claims

This run is advisory decision input for the commissioning Chief Architect. It
creates no validation, readiness, acceptance, buyer-proof, judgment-quality, or
formal review-lane claim; it does not ratify the target; the target remains
PROPOSED at product-learning tier regardless of verdict. The de-correlation
constraint is commission provenance, not runtime model routing.
