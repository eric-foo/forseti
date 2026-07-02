# Bronze / Silver Post-PR530 Goal Frame Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet
scope: >
  Transfers the Bronze/Silver/Data Lake convergence lane after PR #530 review
  adjudication, carrying the goal frame, kept delegated-review patch, and next
  material direction for a fresh thread with no sender memory.
use_when:
  - Starting a fresh thread to continue Bronze MGT / Silver intake convergence after PR #530.
  - Re-establishing what the next thread should optimize for before touching lake docs or runtime.
  - Checking which delegated PR #530 review patch was accepted by the home model.
authority_boundary: retrieval_only
stale_if:
  - PR #530 is materially rewritten, closed without merge, or superseded.
  - Bronze is later declared full God Tier by a separate accepted authority.
  - A later handoff supersedes this packet for the same Bronze/Silver convergence lane.
```

## Goal Establishing

Long-term goal:

Make Orca's lake foundation compound across capture, projection, Silver, and later
Judgment lanes by preserving raw evidence, indexing it through public Bronze
surfaces, and letting downstream records cite replayable raw truth without
guessing folder layout or smuggling unproven authority.

Anchor goal:

Carry PR #530 to a disciplined close, then continue the same direction in a fresh
thread by selecting the first Silver-facing proving slice that consumes public
Bronze packet/catalog/Attachment Record surfaces without declaring Bronze full GT
or starting unbounded runtime work.

Success signal:

- Core success:
  - Owner-observable: PR #530 has a clear adjudication and the next thread can
    open one packet that names the goal, constraints, exact next action, and
    facts to re-verify.
  - Output fit: the next thread can decide or execute the next lake-convergence
    unit without re-litigating why Bronze MGT is enough for Silver intake, and
    without mistaking MGT for full GT.
  - Boundary: a handoff file, review report, green doc hooks, or PR metadata does
    not by itself prove Bronze full GT, Silver readiness, runtime correctness, or
    permission to implement new lake infrastructure.
  - Drift cue: the work has drifted if the next thread treats generated
    `indexes/derived_retrieval/bronze_catalog/v0` files as authority, infers
    source meaning from physical folders, hides missing Attachment Record rows,
    or expands into Manifest v2/body-store/backend/retention before proving the
    next consumer slice.
- Secondary success signals:
  - The next thread can re-verify every load-bearing claim against a named source
    path, branch, PR, hash, or `reread-required` marker.
  - The next thread preserves the accepted MGT doctrine: target 90-95% leverage,
    named residuals, no false full-GT claim.

Open question:

Which first Silver-facing proving slice should follow PR #530: an existing
producer family with preserved bodies and AR coverage, or a narrow docs-only
Silver producer contract before code?

```yaml
goal_handoff:
  long_term_goal: >
    Make Orca's lake foundation compound across capture, projection, Silver, and
    later Judgment lanes by preserving raw evidence, indexing it through public
    Bronze surfaces, and letting downstream records cite replayable raw truth
    without guessing folder layout or smuggling unproven authority.
  anchor_goal: >
    Carry PR #530 to a disciplined close, then continue the same direction in a
    fresh thread by selecting the first Silver-facing proving slice that consumes
    public Bronze packet/catalog/Attachment Record surfaces without declaring
    Bronze full GT or starting unbounded runtime work.
  success_signal:
    core_success:
      owner_observable: >
        PR #530 has a clear adjudication and the next thread can open one packet
        that names the goal, constraints, exact next action, and facts to
        re-verify.
      output_fit: >
        The next thread can decide or execute the next lake-convergence unit
        without re-litigating why Bronze MGT is enough for Silver intake, and
        without mistaking MGT for full GT.
      boundary: >
        A handoff file, review report, green doc hooks, or PR metadata does not
        by itself prove Bronze full GT, Silver readiness, runtime correctness, or
        permission to implement new lake infrastructure.
      drift_cue: >
        The work has drifted if the next thread treats generated
        indexes/derived_retrieval/bronze_catalog/v0 files as authority, infers
        source meaning from physical folders, hides missing Attachment Record
        rows, or expands into Manifest v2/body-store/backend/retention before
        proving the next consumer slice.
    secondary_success_signals:
      - The next thread can re-verify every load-bearing claim against a named source path, branch, PR, hash, or reread-required marker.
      - The next thread preserves the accepted MGT doctrine: target 90-95% leverage, named residuals, no false full-GT claim.
  status: inferred_thread_local
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: goal_handoff.anchor_goal
  output_fit_check: goal_handoff.success_signal.core_success.output_fit
  target_delta_from_prior:
    status: prior_target_not_supplied
    changed_fields: []
    summary: No prior machine-readable thread target was supplied to this packet.
  drift_guard: "Do not convert PR #530's MGT/Silver-intake boundary into a full-GT, readiness, or runtime-implementation claim."
  conflict_behavior: call_out_conflict_before_proceeding
```

## Applied Contract Record

```yaml
applied_contract_record:
  orca_start_preflight:
    agents_read: yes
    overlay_read: yes
    source_pack: custom S0/S1 plus target review and PR #530 artifacts
    edit_permission: docs-write
    target_scope: PR #530 delegated review adjudication plus cold handoff packet
    dirty_state_checked: yes
    blocked_if_missing: overlay README, artifact folder rule, retrieval metadata, delegated report
  prompt_contract:
    output_mode: file-write
    template_kind: none; handoff packet authored directly under workflow-handoff mechanics
    preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0
    target: docs/prompts/handoffs/bronze_silver_post_pr530_goal_frame_handoff_v0.md
    authorization_basis: current user instruction to adjudicate and hand off, goal frame first
    doctrine_change_decision: none; continuation/adjudication artifact only
    isolation_decision: existing PR #530 worktree/branch, because this is a continuation of that active lane
    validation_gates: retrieval-header, prompt provenance, DCP receipt hygiene, map/header/link freshness, diff check
  handoff_contract:
    mode: max
    source_loading_mode: repo-overlay-bound
    load_rule: confirm-don't-trust; this packet is orientation, not authority
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-30
- created_by_lane: OpenAI/Codex home model on the Bronze/Silver PR #530 lane
- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- active_worktree_at_write: `C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline`
- handoff_path: `docs/prompts/handoffs/bronze_silver_post_pr530_goal_frame_handoff_v0.md`
- expected_branch: `codex/bronze-silver-ar-convergence`
- expected_pr: `https://github.com/eric-foo/orca/pull/530`
- expected_head_at_handoff_authoring: `0ba9998a` before this handoff and adjudication commit; receiver must re-verify current branch head and PR state before acting.
- expected_dirty_state_before_handoff_file: two modified target docs plus one untracked delegated review report.
- expected_dirty_state_after_handoff_file: same two modified target docs, the untracked delegated review report, and this handoff file until committed.
- load_rule: confirm-don't-trust. Re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Home-Model Adjudication

Decision: keep both delegated review patches and the durable delegated review
report.

- AR-01 kept: `docs/workflows/orca_repo_map_v0.md` live harness row now says
  `post-PR-525 MGT baseline` instead of stale `post-PR-520 MGT baseline`.
  The dated changelog line that still says post-PR-520 is intentionally
  historical, not rewritten.
- AR-02 kept: `core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
  now includes `replay/version pins` in the Silver AR carry-list, matching the
  AR-owner contract.
- Review report kept:
  `docs/review-outputs/bronze_silver_ar_convergence_pr530_delegated_adversarial_review_patch_v0.md`.

Why keep: both patches are single-line, in-scope, faithful alignments to already
controlling PR #530 sources. They do not create new doctrine, runtime authority,
validation proof, readiness, or a full-GT claim.

## Open Decision / Fork

Decision: what should the fresh thread do after PR #530 is merged or otherwise
settled?

Options:

1. First Silver-facing proving slice over an existing Bronze source family.
   Use public Bronze packet/catalog/Attachment Record surfaces to produce or
   harden a narrow Silver `raw_refs` contract/proof. This proves the new boundary
   through a real consumer.
2. More Bronze full-GT upgrade work before Silver. This means deterministic
   writer discovery, Manifest v2/migration, body-store/backend/retention,
   lake-doctor CI, multi-family proof, and de-correlated full-GT review.
3. Docs-only Silver producer contract before code. This is lower risk than code
   if the producer family is not yet obvious, but it delays proving that the
   public Bronze surfaces work as consumed interfaces.

Already constrained / off the table:

- Do not declare Bronze full GT from PR #530. It declares and documents Bronze
  MGT baseline only.
- Do not make Silver read private packet-member paths, safe-name derivations, or
  generated catalog files as authority.
- Do not implement runtime work in the fresh thread unless that thread has a
  current bounded implementation authorization or accepted handoff that grants it.

Recommendation:

Choose option 1 once PR #530 is merged or current. The point of PR #530 is that
Bronze MGT is strong enough for Silver to consume public Bronze surfaces without
waiting for full GT. A real Silver-facing proving slice will expose whether the
AR/catalog boundary actually compounds. Keep option 2 as the full-GT upgrade
path, not the immediate bottleneck.

## Drift Guard

- Bronze MGT is not Bronze full GT. A future declaration can upgrade it only
  through a separate accepted authority and evidence path.
- Generated Bronze Catalog indexes are retrieval aids, not source authority.
  Authority stays with raw packets, manifests, preserved bodies, and controlling
  contracts.
- Attachment Record rows are typed references over preserved Bronze bodies. They
  do not replace raw bodies, pick Manifest v2/backend/retention, or authorize a
  new body-copy store by themselves.
- Missing AR is a visible residual, not proof that a source payload is absent.
- Silver `raw_refs` must cite public packet/catalog/AR surfaces and enough hash
  material to re-resolve raw evidence; no folder inference.
- Future capture/projection lanes that interact with the lake should route to
  the Bronze/Silver contracts rather than continuing private one-off raw-ref
  conventions.

## Inherited Context (Does Not Flow To A New Lane)

### Source-loading state to re-establish

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- overlay entrypoint: `.agents/workflow-overlay/README.md`
- prompt/handoff policy: `.agents/workflow-overlay/prompt-orchestration.md`
- artifact placement: `.agents/workflow-overlay/artifact-folders.md`
- retrieval headers: `.agents/workflow-overlay/retrieval-metadata.md`
- route map: `docs/workflows/orca_repo_map_v0.md`
- must load first before strict or actionable steps: `AGENTS.md`, overlay
  README, source-loading policy, the PR #530 branch/PR state, and the specific
  target contracts for the next action.
- load rule: this packet only seeds the ladder. The receiver must re-run
  progressive source loading per the overlay before strict claims or edits.

### Earlier-decided concepts and behaviors

- MGT doctrine: "mini god tier" means owner-invoked 90-95% capability target
  with named residuals, not a validation/readiness tier.
  - verify pointer: `docs/decisions/orca_mini_god_tier_doctrine_v0.md`
  - compare target: reread-required before making tier claims.
- Bronze post-PR525 declaration: PR #530 docs frame Bronze as MGT baseline that
  Silver can consume through public Bronze surfaces without declaring full GT.
  - verify pointer: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md`
  - compare target: reread-required against current branch/main.
- Silver intake boundary: Silver records may cite public Bronze packet/catalog/AR
  surfaces for `raw_refs`; no private path guessing or generated-catalog authority.
  - verify pointer: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
  - compare target: SHA256 `B9572CFD38C549FF3C3802017413DDD18F4C2888508AA7D400F019BB0AA8A2AE` at handoff authoring.
- AR contract: typed Attachment Record entries over preserved bodies are the
  cross-family ref shape; runtime physicalization/backend/migration remains
  bounded by future authorization.
  - verify pointer: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
  - compare target: reread-required against current branch/main.

## Active Objective

Close PR #530 with the accepted delegated-review patch and this handoff, then
let a fresh thread continue the lake-convergence work from a clean, verified
state. The next material unit should prove Silver consumption of public Bronze
surfaces before spending more work on full Bronze GT infrastructure.

## Exact Next Authorized Action

1. In the fresh thread, load this packet and re-verify branch/PR #530 state,
   dirty state, and the source ledger below. If PR #530 is not merged, finish
   PR closeout first.
2. After PR #530 is current or merged, open a new isolated work unit off current
   `main` for the first Silver-facing proving slice. Start by choosing the
   source family and output contract; do not default to runtime implementation
   until the new thread has bounded implementation authorization.
3. If the chosen slice needs code, bind the exact files, public Bronze APIs,
   validation gates, and non-claims before editing.

## Authority And Source Ledger

- `AGENTS.md`
  - Role: project behavior kernel and authorization boundary.
  - Load-bearing: yes.
  - Compare target: supplied in current task context; receiver rereads current file before strict claims.
  - Last checked: 2026-06-30 in this thread context.
  - Reuse rule: orientation only until reread.
- `.agents/workflow-overlay/README.md`
  - Role: Orca overlay entrypoint and binding rule.
  - Load-bearing: yes.
  - Compare target: read 2026-06-30; receiver rereads.
  - Last checked: 2026-06-30.
  - Reuse rule: reread before strict/actionable steps.
- `.agents/workflow-overlay/source-loading.md`
  - Role: source-loading policy and start preflight.
  - Load-bearing: yes.
  - Compare target: read section through Prompt Source Capsules on 2026-06-30.
  - Last checked: 2026-06-30.
  - Reuse rule: reread if source pack or strict claim changes.
- `.agents/workflow-overlay/artifact-folders.md`
  - Role: accepted destination for `docs/prompts/handoffs/`.
  - Load-bearing: yes.
  - Compare target: read 2026-06-30; `docs/prompts/handoffs/` listed as accepted.
  - Last checked: 2026-06-30.
  - Reuse rule: reread if destination changes.
- `.agents/workflow-overlay/retrieval-metadata.md`
  - Role: retrieval header contract.
  - Load-bearing: yes.
  - Compare target: read 2026-06-30; core five-field header required for durable human-authored workflow artifacts.
  - Last checked: 2026-06-30.
  - Reuse rule: reread if header policy changes.
- `.agents/workflow-overlay/prompt-orchestration.md`
  - Role: prompt/handoff artifact contract and source-gated method sequencing.
  - Load-bearing: yes.
  - Compare target: read 2026-06-30 through Supported Prompt Families / Author Through Prompt Orchestrator.
  - Last checked: 2026-06-30.
  - Reuse rule: reread if generating prompts or wrappers.
- `docs/prompts/reviews/bronze_silver_ar_convergence_pr530_delegated_adversarial_review_patch_prompt_v0.md`
  - Role: delegated review commission.
  - Load-bearing: yes for what was commissioned.
  - Compare target: SHA256 `498ACF1D799A97730A93AB1EE9A55B82A3A45438EE2B297E9E94436719A728BB`.
  - Last checked: 2026-06-30.
  - Reuse rule: reread before relying on commission scope.
- `docs/review-outputs/bronze_silver_ar_convergence_pr530_delegated_adversarial_review_patch_v0.md`
  - Role: delegated review result and patch report.
  - Load-bearing: yes for adjudication.
  - Compare target: SHA256 `396013AB6DD617BF71D5EEC0229794F1E41D9A88F3772A2E135A8935D42F0AEC`.
  - Last checked: 2026-06-30.
  - Reuse rule: reread before relying on findings or validation evidence.
- `docs/workflows/orca_repo_map_v0.md`
  - Role: repo navigation surface and AR-01 patched target.
  - Load-bearing: yes.
  - Compare target: SHA256 `DBE5DD00C360D3881F9F75C1921F731E76A5591678750E70DD95A33600701A74` after AR-01 patch.
  - Last checked: 2026-06-30.
  - Reuse rule: reread current live row before route claims.
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
  - Role: Silver Vault Record contract and AR-02 patched target.
  - Load-bearing: yes.
  - Compare target: SHA256 `B9572CFD38C549FF3C3802017413DDD18F4C2888508AA7D400F019BB0AA8A2AE` after AR-02 patch.
  - Last checked: 2026-06-30.
  - Reuse rule: reread before Silver raw-ref claims.

Source gaps:

- PR #525 runner-enforcement primary sources were not re-verified in this
  adjudication; the delegated report records this as out of the six-file scope.
- Current PR #530 CI and merge state are intentionally `reread-required`; they
  move after this packet is written and pushed.

Strict-only blockers:

- Do not claim PR #530 merged, CI green, or branch pushed unless the receiving
  thread observes it.
- Do not claim full Bronze GT without a later accepted full-GT authority source.

## Current Task State

Completed in this thread before this handoff:

- Read the delegated review return from
  `C:\Users\vmon7\.codex\attachments\b81065ea-bf53-4e6b-a023-45e036f9b203\pasted-text.txt`.
- Read the durable delegated review report.
- Adjudicated both delegated patches as kept.
- Confirmed current worktree had exactly two modified docs plus the untracked
  delegated review report before adding this handoff.
- Bound this handoff destination to `docs/prompts/handoffs/`.

Partially completed:

- Final validation and commit/push happen after this packet body is first
  written; receiver must verify final branch and PR state.

Broken or uncertain:

- None known for the two kept patches. PR/CI state is moving and must be
  rechecked.

## Workspace State

- Branch: `codex/bronze-silver-ar-convergence`.
- Head before this handoff/adjudication commit: `0ba9998a`.
- Dirty or untracked state before handoff file:
  - modified: `docs/workflows/orca_repo_map_v0.md`
  - modified: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
  - untracked: `docs/review-outputs/bronze_silver_ar_convergence_pr530_delegated_adversarial_review_patch_v0.md`
- Dirty or untracked state after writing this handoff:
  - the same two modified docs
  - the untracked review report
  - untracked: `docs/prompts/handoffs/bronze_silver_post_pr530_goal_frame_handoff_v0.md`
- Related PR: #530, `https://github.com/eric-foo/orca/pull/530`.

## Changed / Inspected / Tested Files

- `docs/workflows/orca_repo_map_v0.md`
  - Status: modified by delegated patch, kept.
  - Role: repo map route consistency.
  - Important observation: live `orca-harness/data_lake/` row now says
    `post-PR-525 MGT baseline`; dated changelog line 27 still records
    historical post-PR-520 and is intentionally not patched.
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
  - Status: modified by delegated patch, kept.
  - Role: Silver raw-ref / Bronze intake boundary.
  - Important observation: carry-list now includes `replay/version pins`.
- `docs/review-outputs/bronze_silver_ar_convergence_pr530_delegated_adversarial_review_patch_v0.md`
  - Status: new delegated review report, kept.
  - Role: review evidence and return block for adjudication.
- `docs/prompts/handoffs/bronze_silver_post_pr530_goal_frame_handoff_v0.md`
  - Status: new handoff packet.
  - Role: cold continuation artifact for the next thread.

## Frozen Decisions

- Keep the delegated AR-01 and AR-02 patches.
  - Evidence: delegated report plus direct diff read in this thread.
  - Consequence: commit should include both patches and the report.
- Treat PR #530 as Bronze MGT/Silver intake convergence, not full Bronze GT.
  - Evidence: PR #530 target docs and delegated review summary.
  - Consequence: next thread should prove Silver consumption rather than wait
    for full-GT infrastructure.
- Keep runtime implementation gated.
  - Evidence: `AGENTS.md` and source-loading boundary require explicit bounded
    implementation authorization.
  - Consequence: docs-write handoff does not authorize new runtime work.

## Mutable Questions

- Which source family should provide the first Silver-facing proving slice?
  - Why still mutable: PR #530 establishes the boundary but does not select a
    producer-family implementation unit.
  - What would resolve it: owner selection or next-thread source-loaded
    recommendation from current Bronze/Silver contracts and available preserved
    bodies.
- Should the next unit be docs-only producer contract or bounded runtime proof?
  - Why still mutable: implementation authority must be current and bounded.
  - What would resolve it: owner authorization in the new thread or an accepted
    handoff that names exact files and validation gates.

## Superseded / Dangerous-To-Reuse Context

- "Bronze is full GT now."
  - Why stale or dangerous: PR #530 is MGT baseline only; full-GT blockers remain.
  - Current replacement: Bronze MGT baseline, with full-GT upgrade path deferred.
- "Silver can just read the generated catalog files or folder layout."
  - Why stale or dangerous: generated indexes are retrieval aids, not authority;
    folder inference loses traceability.
  - Current replacement: Silver uses public packet/catalog/AR helper surfaces
    and raw hash material.
- "Missing AR means missing source payload."
  - Why stale or dangerous: AR generation is not complete enough to prove absence.
  - Current replacement: missing AR is visible residual; fallback raw refs must
    be producer-contract-bound and hash-checkable.

## Commands And Verification Evidence

- Command:
  ```powershell
  git status --short --branch
  ```
  Result:
  - Observed before handoff write: branch `codex/bronze-silver-ar-convergence`
    tracking origin, two modified docs, one untracked review report.
  - Re-run target: receiver reruns in the active worktree.
- Command:
  ```powershell
  git diff -- docs/workflows/orca_repo_map_v0.md orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  ```
  Result:
  - Observed: exactly two single-line delegated patches, AR-01 and AR-02.
  - Re-run target: receiver reruns against current branch if adjudication is in doubt.
- Command:
  ```powershell
  Get-FileHash -Algorithm SHA256 -LiteralPath <patched docs and review artifacts>
  ```
  Result:
  - Observed hashes are recorded in Authority And Source Ledger.
  - Re-run target: receiver recomputes if using this packet as a load seed.

Final validation status:

- Observed after initial packet write on 2026-06-30:
  - `git diff --check`: passed, no output.
  - `check_retrieval_header.py --changed --strict`: passed, no output.
  - `check_dcp_receipt.py --strict --base codex/bronze-mgt-baseline`: passed,
    reported every real receipt in changed `.md` files shape-valid.
  - `check_dcp_receipt_hygiene.py --changed --strict`: passed, no output.
  - `header_index.py --strict --base codex/bronze-mgt-baseline`: passed,
    reported changed durable `.md` files have headers and are map-reachable.
  - `check_map_links.py --strict`: passed, 0 findings, 33 annotated
    nonresolving debt.
  - `check_repo_map_freshness.py --strict`: passed, no output.
  - `check_prompt_provenance.py --changed --strict`: command returned 0, but
    this hook has no real changed-file strict mode; treat prompt-preflight
    compliance as recorded in the Applied Contract Record, not as a checker
    proof.
  - `check_placement.py --strict`: failed on pre-existing repo-wide placement
    debt (`.github`, `.githooks`, `.gitattributes`, legacy harness files, and
    related map/tree freshness), not on this handoff path. Treat as known
    placement debt, not a completion blocker for this docs-only handoff.

## Blockers And Risks

- Risk: next thread treats MGT as enough for all future work.
  - Evidence: user wants "god tier" lake; PR #530 deliberately stops at MGT.
  - Likely next action: keep the full-GT upgrade path visible but do not let it
    block the first Silver proof unless a source-loaded reason says Silver will
    misbehave.
- Risk: next thread begins implementation from generated catalog semantics.
  - Evidence: PR #530 explicitly says generated catalog is retrieval-only.
  - Likely next action: bind public helper APIs and raw packet/manifest authority
    before code.

## Confirm-Don't-Trust Load Checklist

Load-bearing facts the receiver must re-verify before acting:

- Current branch and PR #530 state.
- The two kept delegated patches still exist or have been superseded.
- The durable delegated review report exists and matches or supersedes the hash
  recorded above.
- The Bronze MGT declaration still says MGT/not full GT.
- The Silver contract still binds `raw_refs` to public Bronze packet/catalog/AR
  surfaces.
- Current implementation authorization, if any, in the new thread.

Load outcomes:

- `REUSE`: all required load-bearing facts match or have current-source
  successors; continue from Exact Next Authorized Action.
- `PARTIAL_REUSE`: only optional context drifted; re-derive optional context and
  continue from verified facts.
- `STALE_REREAD_REQUIRED`: branch, PR, or target docs moved; reread current
  sources before deciding.
- `BLOCKED_DRIFT`: current source conflicts with this handoff's goal,
  authorization, or drift guard.
- `BLOCKED_MISSING_PACKET`: this handoff path is missing or unreadable.
- `BLOCKED_UNVERIFIABLE`: a load-bearing claim cannot be re-derived.

## Do Not Forget

The next compounding move is not "make Bronze bigger." It is to prove that
Silver can consume the public Bronze surfaces cleanly. If that proof exposes a
Bronze blocker, then promote that blocker into the full-GT path with evidence.
