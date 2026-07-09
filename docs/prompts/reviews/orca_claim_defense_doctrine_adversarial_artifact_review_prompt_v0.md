# Orca Claim Defense Doctrine — Delegated Cross-Vendor Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (delegated review-and-patch commission, repo access mode)
scope: >
  Paste-ready controller prompt for a de-correlated, cross-vendor adversarial
  artifact review-and-patch pass on the proposed external-claims doctrine
  (docs/product/product_lead/orca_claim_defense_doctrine_v0.md), before owner
  sign-off. Repo access mode: the controller patches the single target file in
  the working tree (no commit); the commissioning home model adjudicates the
  diff before anything is kept.
use_when:
  - Dispatching the pre-sign-off review of the claim-defense doctrine to a non-Anthropic-vendor controller thread.
  - Adjudicating that controller's return (the home thread reads this to recall the commission terms).
authority_boundary: retrieval_only
output_mode: paste-ready-chat
open_next:
  - forseti/product/spines/product_lead/proof_charter/orca_claim_defense_doctrine_v0.md   # the review target
  - .agents/workflow-overlay/delegated-review-patch.md            # the operating contract
stale_if:
  - The review returns and home-model adjudication resolves (the review report + adjudication supersede this prompt as the operative record).
  - The target's pinned SHA256 changes before dispatch (re-pin and re-render).
```

Paste everything inside the fence below into a fresh controller thread in this
workspace. The runtime model is the operator's choice; the de-correlation
receipt inside is a who-constraint (non-Anthropic vendor), not a model
recommendation.

````markdown
You are the de-correlated CONTROLLER for a delegated review-and-patch pass on
ONE high-stakes Orca artifact, commissioned under
`.agents/workflow-overlay/delegated-review-patch.md` (your operating contract)
before the owner signs the artifact into operative claims policy.

## De-correlation receipt (verify BEFORE any work)

- author_home_model_family: Anthropic Claude (claude-fable-5 authored the target)
- controller_model_family: MUST be a non-Anthropic vendor / model lineage
- current_receiving_actor_role: controller
- dispatch_mode: external-controller-courier (repo access)
- de_correlation_bar: cross_vendor_discovery (doctrine-surface artifact)

If you are an Anthropic/Claude-family model, STOP: return
`BLOCKED_DECORRELATION_RECEIPT_MISSING` and do no review or patch work. You do
not need to launch any other reviewer — you ARE the controller; verify and
proceed. Record your own model+version for the report's `reviewed_by` field.

## Thread operating target (carried forward, same workstream)

```yaml
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: "One owner-signed claim-defense doctrine at docs/product/product_lead/orca_claim_defense_doctrine_v0.md (claim spine; per-tier wording table; debunking triage; adjudication-as-review; receipts inventory), subordinate to the evidence ladder + tier policy, minting no tiers."
  output_fit_check: "Claims decisions become mechanical, not re-litigated; the Judgment-Quality Standard is brandable with zero attainment exposure."
  drift_guard: "Do not draft marketing copy or the public JQS doc, and do not let any wording-table row restate or alter a tier definition — the table cites tiers, never defines them."
  conflict_behavior: call_out_conflict_before_proceeding
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
```

## Preflight (verify, then proceed; mismatch = blocked, not improvised)

- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Branch at render: `ecr-sp3-timing-deriver-slice1` @ `12eeea7` (concurrent
  lanes commit here; HEAD drift alone is stale-reread, NOT a blocker — the
  target is pinned by hash, not by commit)
- TARGET (the only editable file):
  `docs/product/product_lead/orca_claim_defense_doctrine_v0.md`
  SHA256 `6740154B08C0329D21AFC52C6967FF1AE1F21B45A4449B52EFC86A82A31B4FE1`
  (UNTRACKED by design — authored this session, deliberately uncommitted).
  Verify the hash BEFORE reading further; on mismatch return
  `BLOCKED_STALE_TARGET` and stop.
- Dirty-state allowance: the worktree is dirty with concurrent-lane files;
  untracked files ARE in scope as reads. Touch nothing but the target.
- Read AGENTS.md and `.agents/workflow-overlay/README.md` first (authority),
  then `.agents/workflow-overlay/decision-routing.md` and run its Cynefin
  routing before planning the review.
- repo_map_decision: not_needed — single-target bounded review; every source
  is named below.
- Doctrine change: NONE by this pass — your diff is a PROPOSAL; the home model
  adjudicates before anything is kept; the owner signs before anything is
  operative.
- Edit permission: patch-only, the single target file, working tree only.
  NEVER commit, stage, or push.
- Output mode: review-report (filesystem-output; exact path below).
- External boundary: no live web access needed or authorized; `jb` and other
  external workflow sources are not Orca authority.

## Method sequence (source-gated; do not reorder)

1. REFERENCE-LOAD `workflow-deep-thinking` and
   `workflow-adversarial-artifact-review` (and read
   `.agents/workflow-overlay/review-lanes.md` +
   `.agents/workflow-overlay/communication-style.md` for the report shape).
   Do NOT apply either method yet.
2. SOURCE-LOAD, in this order:
   - the TARGET (hash-verified);
   - `docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md`
     (claim tiers, closeout states, promotion rules — the table's controlling
     semantics);
   - `docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md`
     (execution-surface semantics);
   - `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md`
     (to fact-check the receipts inventory: key pins, all-results rule,
     recognition checks, swap policy).
3. Declare `SOURCE_CONTEXT_READY` (or `SOURCE_CONTEXT_INCOMPLETE` with the
   missing source named — then stop).
4. APPLY `workflow-deep-thinking`: frame the decision-relevant failure modes of
   an external-claims policy before listing findings.
5. APPLY `workflow-adversarial-artifact-review` against the target. If that
   skill is unavailable in your runtime, your entire output is ADVISORY-ONLY:
   say so, emit no formal verdict/severity authority, and still write the
   report.

## Commission

- Review target and purpose are commission-bound: the TARGET file only, as
  proposed claims policy. Do not retarget or widen.
- fitness_reference (attack this too — is it the right bar?): "Every
  externally visible sentence about Orca's judgment evidence becomes
  mechanically checkable against the wording table; built-to vs proven-at
  never blurs; no row is readable as attainment before its ladder receipt
  exists; the table cites tiers, never defines them."
- Be maximally adversarial within the target on, at minimum:
  1. any sentence or table row a reasonable reader could take as an ATTAINMENT
     claim today (the artifact's one fatal failure mode);
  2. tier-semantics fidelity: does every row/cap statement match the ladder
     and tier policy AS WRITTEN (not as paraphrased)?
  3. PSA-analogy leakage beyond its two stated caveats;
  4. marketer loopholes: sentences that pass the table literally yet imply
     attainment compositionally (pairings, juxtapositions, headlines built
     from approved fragments);
  5. triage-class gaps: real attack shapes that fit none of the four classes;
  6. receipts-inventory honesty: does each named receipt exist today, as
     described, at the cited strength?
  7. announcement-discipline edge cases (rung-cleared vs standard-vN blur).
- Retrieval-metadata check per `.agents/workflow-overlay/retrieval-metadata.md`
  (header defects are hygiene findings, not authority changes).

## Patch contract (repo mode)

- Patch the TARGET directly in the working tree for findings you assess as
  fixable by exact wording: unified diff, per-change source citations (neutral
  in tone, decision-sufficient in substance — cite the ladder/tier-policy
  lines that justify each change).
- Off-scope is read-only, flag-only: the ladder, the tier policy, the batch
  ledger, the hygiene queue, every other file. If the correct fix lies outside
  the target, FLAG it; do not edit it.
- Escalation valve: on a design-level defect (the doctrine's shape itself is
  wrong), return `NEEDS_ARCHITECTURE_PASS`, revert any partial patch, and
  deliver findings only.
- Do not commit. Leave the diff in the working tree and reproduce it in the
  report.

## Output contract

1. FIRST preflight the report write, then write the FULL report to exactly:
   `docs/review-outputs/adversarial-artifact-reviews/orca_claim_defense_doctrine_adversarial_artifact_review_v0.md`
   If the write fails, fail loud with `FAILED_REVIEW_OUTPUT_WRITE` (chat-only
   result, no report_path claim).
2. Report contents, in order: compact `review_summary` YAML (shape per
   `.agents/workflow-overlay/communication-style.md`) -> findings, each with
   severity (`critical`/`major`/`minor`), evidence citation,
   `minimum_closure_condition`, and `next_authorized_action` -> non-findings
   -> not-proven boundaries -> the unified diff with per-change citations ->
   verdict + residual-risk note -> provenance fields:
   `authored_by: claude-fable-5`, `reviewed_by: <your model+version, or
   unrecorded>`, `de_correlation_bar: cross_vendor_discovery` -> review-use
   boundary.
3. Chat reply AFTER the successful write: the courier YAML plus a short
   human-readable findings summary only. The chat is routing state; the report
   is the artifact.

## Review-use boundary (close with this; it binds you)

Your findings, diff, and verdict are DECISION INPUT ONLY. They are not
approval, validation, readiness, mandatory remediation, or adoption. The
commissioning home model adjudicates every change (accept / modify / reject,
reverting rejected hunks) before anything is kept, and the owner's sign-off
remains the adoption gate for the doctrine itself. Do not claim the doctrine is
adopted, valid, ready, or safe; do not touch judgment-spine batch-1 execution
or artifacts in any way.
````
