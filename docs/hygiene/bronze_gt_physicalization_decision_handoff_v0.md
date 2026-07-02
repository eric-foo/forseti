# Handoff Packet

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-thread handoff checkpoint
scope: >
  Same-lane continuation packet for the Bronze full-GT physicalization decision
  brief patch after PR #555, carrying goal frame, open decision, drift guard,
  dirty worktree state, verification evidence, and confirm-don't-trust load targets.
use_when:
  - Continuing the Bronze full-GT physicalization lane in a fresh thread.
  - Re-establishing context for the docs-only patch before review, commit, or next ADR work.
  - Checking why the next-material-decisions packet was superseded as the active continuation anchor.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_next_material_decisions_v0.md
  - .agents/workflow-overlay/source-loading.md
stale_if:
  - The handoff file is consumed by a fresh thread and live state is re-established.
  - The worktree branch, head, dirty state, or changed file hashes differ from the Load Contract compare targets.
  - The user redirects away from the Bronze full-GT physicalization lane.
```

## Load Contract

- packet_version: workflow-handoff max v0
- mode: max
- source-loading mode: repo-overlay-bound
- created_at: 2026-07-02T04:37:31.9626684+08:00
- created_by_lane: OpenAI/GPT-family Codex, current Orca thread; provenance only, not authority
- workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-gt-physicalization-handoff`
- handoff_path: `C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-gt-physicalization-handoff\docs\hygiene\bronze_gt_physicalization_decision_handoff_v0.md`
- expected_branch: `codex/bronze-gt-physicalization-handoff`
- expected_head: `0b17593a9cdd8c1b06344d3041d8bc81f1135e8d`
- expected_dirty_state_including_handoff_file:
  - `M docs/workflows/orca_repo_map_v0.md`
  - `M orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_next_material_decisions_v0.md`
  - `?? docs/hygiene/bronze_gt_physicalization_decision_handoff_v0.md`
  - `?? orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md`
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: Get the Data Lake Bronze lane from Mini God Tier typed raw-truth retrievability toward defensible full God Tier without weakening raw authority, hiding residuals, or letting storage convenience choose architecture.
- anchor_goal: Continue the post-PR-555 Bronze full-GT physicalization lane by using the new physicalization decision brief to adjudicate Gate 1 (Attachment Record body layout/backend relationship) and Gate 2 (retention/lawful-erasure/backend lock-in) before any runtime implementation, backend selection, or third-proof expansion.
- success_signal:
  - core_success:
    - owner_observable: The owner can see the patched physicalization decision brief, the superseded next-decision anchor, and a fresh-thread handoff that identifies the live open decision and exact next safe action.
    - output_fit: The next output must make the physicalization choice safer and more decision-useful by selecting, deferring, or requesting owner input on Gate 1/Gate 2 without overclaiming full GT.
    - boundary: Artifact creation, review, tests, or a green CI-style check do not count as full GT, backend selection, retention policy, lawful-erasure sufficiency, implementation authorization, or third-proof authority.
    - drift_cue: The lane is drifting if it starts storage code, a third consumer proof, repo-wide cleanup, or a backend-first choice before the two physicalization gates are decided or consciously deferred.
  - secondary_success_signals:
    - A fresh reader can verify the patch from file hashes and repo state before acting.
    - The older next-material-decisions packet is no longer treated as active PR/admin guidance.

## Open Decision / Fork

- decision: Which physicalization route should the next thread prepare or adjudicate?
  - options:
    1. Defer physicalization and keep the current MGT posture.
    2. Proceed with Gate 1 ADR: decide packet-member versus hash-pinned sidecar versus explicit deferral while keeping backend unselected until Gate 2.
    3. Proceed with Gate 2 ADR first if lawful erasure or retention policy is load-bearing now.
    4. Proceed with a combined physicalization ADR only if the owner wants an explicit backend call now.
  - already constrained / off the table:
    - No runtime storage implementation in this handoff.
    - No backend selection by convenience.
    - No third-proof expansion as a substitute for physicalization.
    - No Bronze full-GT claim from PR #555, the new brief, or this packet.
  - trade-offs:
    - Gate 1 first is lowest-lock-in if lawful erasure is not a hard current requirement.
    - Gate 2 first is necessary if erasure/retention policy is load-bearing.
    - Combined ADR is heavier but may be justified if the owner wants a backend decision now.
  - owner of the call: Owner / Chief Architect.
  - recommendation and why: Proceed with Gate 1 ADR unless the owner states lawful erasure is a hard current requirement; then Gate 2 comes first. This keeps backend convenience from selecting architecture.

## Drift Guard

- invariant, non-goal, or scope boundary: Do not treat the new brief as validation, full-GT evidence, or implementation authorization.
  - why it matters: The brief is a decision-request artifact; the Data Lake contracts still defer layout/backend/retention implementation.
  - what violating it would break: It would recreate the exact lock-in risk the lane exists to prevent.
- invariant, non-goal, or scope boundary: Do not start third-proof work before Gate 1/Gate 2 are decided or explicitly deferred.
  - why it matters: More source-family proof does not answer physicalization.
  - what violating it would break: It would make proof count substitute for architecture.
- invariant, non-goal, or scope boundary: Do not reuse the old next-material-decisions packet's PR/admin steps as active guidance.
  - why it matters: That packet is superseded as the active continuation anchor after PR #555 and this patch.
  - what violating it would break: It would reopen a stale review/admin loop instead of continuing to the physicalization decision.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`; source hierarchy: `.agents/workflow-overlay/source-of-truth.md`.
- targets to enter the ladder:
  - `AGENTS.md`
  - `.agents/workflow-overlay/README.md`
  - `.agents/workflow-overlay/source-loading.md`
  - `.agents/workflow-overlay/artifact-folders.md`
  - `.agents/workflow-overlay/retrieval-metadata.md`
  - `.agents/workflow-overlay/decision-routing.md`
  - `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md`
  - `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_next_material_decisions_v0.md`
  - the Data Lake contracts named in the brief's `open_next`.
- already loaded (weak orientation, freshness-marked; not authority): AGENTS instructions supplied in current thread; overlay README/source-loading/source-of-truth/artifact-folders/retrieval-metadata/decision-routing/validation-gates; Data Lake storage, Attachment Record, physicality-location, write-boundary, raw-admission, derived-layout contracts; current changed files.
- must load first (before strict or actionable steps): AGENTS, overlay README, source-loading, current git status/head, the new brief, and the two target files it patched.
- load rule: receiver re-runs progressive source loading per overlay; the packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- decision, framing, profile, or convention: PR #555 hardened the Bronze full-GT inventory/AR threshold gates; it did not select physicalization or declare full GT.
  - decided in: Git history / PR #555; verify via `git log --oneline -8` and, if strict PR metadata matters, `gh pr view 555`.
  - compare target: current worktree `git log --oneline -8` should include `bc08586b Harden Bronze full-GT inventory and AR threshold gates (#555)` below `3455533e Add Bronze full-GT next decision packet (#551)` and current HEAD `0b17593a...`.
  - verify before: strict merge-state or PR-history claims.
- decision, framing, profile, or convention: Data Lake Storage Contract permits a later bounded engine/backend choice but selects none itself.
  - decided in: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md`.
  - compare target: reread-required.
  - verify before: backend/engine claims.
- decision, framing, profile, or convention: Attachment Record contract binds compact keyed entry plus immutable hash-checkable body; exact layout/backend remain deferred.
  - decided in: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`.
  - compare target: reread-required.
  - verify before: AR body/layout claims.
- decision, framing, profile, or convention: Physicality contract keeps operational data under an external `ORCA_DATA_ROOT` and names logical slots `raw/ attachments/ derived/ acknowledgements/ indexes/` without selecting engine/backend.
  - decided in: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md`.
  - compare target: reread-required.
  - verify before: storage-location or Git-boundary claims.

## Active Objective

Continue the same Bronze full-GT physicalization lane in a fresh thread. The immediate objective is to verify the docs-only patch, then adjudicate whether the next material artifact should be Gate 1 ADR, Gate 2 ADR, combined ADR, or explicit deferral.

## Exact Next Authorized Action

1. Re-verify branch, head, dirty state, and the three patched artifact hashes in this packet.
2. Re-read the new physicalization decision brief and the patched next-material-decisions packet before making any actionable claim.
3. Ask or decide, based on current owner direction, which of the four decision-request options to take. Recommended default is Gate 1 ADR unless lawful erasure is a hard current requirement.
4. Do not commit, push, open PR, start delegated review, or write runtime code until the fresh thread confirms whether it should close the docs patch first or continue authoring the ADR in the same dirty worktree.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` supplied in current context; Load-bearing: yes; Compare target: reread-required; Last checked: 2026-07-02; Reuse rule: reread before strict or actionable claims.
- Overlay or equivalent authority:
  - `.agents/workflow-overlay/README.md`; Role: overlay entrypoint; Load-bearing: yes; Compare target: reread-required; Last checked: 2026-07-02; Reuse rule: reread first.
  - `.agents/workflow-overlay/source-loading.md`; Role: source-loading/start-preflight owner; Load-bearing: yes; Compare target: reread-required; Last checked: 2026-07-02; Reuse rule: reread before source claims or handoff use.
  - `.agents/workflow-overlay/source-of-truth.md`; Role: source hierarchy/checkpoint lifecycle owner; Load-bearing: yes; Compare target: reread-required; Last checked: 2026-07-02; Reuse rule: reread before checkpoint lifecycle or authority claims.
  - `.agents/workflow-overlay/artifact-folders.md`; Role: accepted folders; Load-bearing: yes; Compare target: reread-required; Last checked: 2026-07-02; Reuse rule: reread before destination claims.
  - `.agents/workflow-overlay/retrieval-metadata.md`; Role: retrieval header contract; Load-bearing: yes; Compare target: reread-required; Last checked: 2026-07-02; Reuse rule: reread before header claims.
- User constraints:
  - Patch it, goal frame, then handoff; continue same lane in different thread. Load-bearing: yes; Compare target: current user message; Last checked: 2026-07-02; Reuse rule: do not broaden beyond this lane without explicit redirect.
- Source-read ledger:
  - `docs/workflows/orca_repo_map_v0.md`
    - Role: repo-map route patched to include the new brief.
    - Load-bearing: yes
    - Compare target: SHA256 `60a8256630a0a4fac52e48e77686752f0676f472b67e85735efdf5c7df913bdd`
    - Last checked: 2026-07-02
    - Reuse rule: rehash before relying on map-route claims.
  - `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_next_material_decisions_v0.md`
    - Role: older next-decision packet patched with supersession note.
    - Load-bearing: yes
    - Compare target: SHA256 `f80f10e48dd8bc5cf7760dad0f4bcd636424f84eadc6fd77125c4e7b13c0a027`
    - Last checked: 2026-07-02
    - Reuse rule: rehash before relying on supersession claims.
  - `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md`
    - Role: new active continuation artifact.
    - Load-bearing: yes
    - Compare target: SHA256 `403b0b0a7f19471b754b96c7562c80223f2fea3657f6779cb0591e074f70decf`
    - Last checked: 2026-07-02
    - Reuse rule: rehash and reread before any next-step decision.
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md`
    - Role: backend/engine selection boundary.
    - Load-bearing: yes
    - Compare target: reread-required
    - Last checked: 2026-07-02
    - Reuse rule: reread before backend claims.
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
    - Role: AR compact-entry/body relationship contract.
    - Load-bearing: yes
    - Compare target: reread-required
    - Last checked: 2026-07-02
    - Reuse rule: reread before AR layout claims.
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md`
    - Role: external data-root and location contract.
    - Load-bearing: yes
    - Compare target: reread-required
    - Last checked: 2026-07-02
    - Reuse rule: reread before location/root claims.
- Source gaps: No delegated review-patch was run for the new brief in this thread; no full test suite was run; header_index/check_dcp strict wrappers did not effectively see uncommitted docs in their diff scope, so targeted header checks are the relevant local evidence.
- Strict-only blockers: No backend/engine/layout/retention/lawful-erasure/full-GT claim may be made from this packet.
- Not-proven boundaries: no validation, readiness, implementation authorization, full GT, PR creation, push, or commit.

## Current Task State

- Completed:
  - Created a fresh worktree branch `codex/bronze-gt-physicalization-handoff` from refreshed `origin/main` at `0b17593a`.
  - Added `core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md`.
  - Patched `core_spine_v0_data_lake_bronze_full_gt_next_material_decisions_v0.md` with `superseded_by`, an `open_next` pointer, a post-merge supersession note, and updated next material steps.
  - Patched `docs/workflows/orca_repo_map_v0.md` so the new brief is reachable.
  - Ran whitespace and targeted retrieval-header checks.
- Partially completed:
  - Goal frame is carried in this packet and will be rendered in chat final.
  - The new brief has not received delegated review-patch.
- Broken or uncertain:
  - None known in the patch itself. The next architecture decision remains owner-owned.

## Workspace State

- Branch: `codex/bronze-gt-physicalization-handoff`
- Head: `0b17593a9cdd8c1b06344d3041d8bc81f1135e8d`
- Dirty or untracked state before handoff file:
  - `M docs/workflows/orca_repo_map_v0.md`
  - `M orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_next_material_decisions_v0.md`
  - `?? orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md`
- Dirty or untracked state after writing the handoff file:
  - expected to add `?? docs/hygiene/bronze_gt_physicalization_decision_handoff_v0.md`; receiver must verify with `git status --short --branch`.
- Target files or artifacts:
  - `docs/workflows/orca_repo_map_v0.md`
  - `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_next_material_decisions_v0.md`
  - `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md`
  - `docs/hygiene/bronze_gt_physicalization_decision_handoff_v0.md`
- Related worktrees or branches: root checkout remains separately dirty on `codex/ig-reels-capture-spine`; do not work there for this lane.

## Changed / Inspected / Tested Files

- `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md`
  - Status: new, untracked before handoff.
  - Role: active physicalization decision brief.
  - Important observations: names Gate 1, Gate 2, backend discipline, decision request, proof/CI boundary, full-GT distance, non-claims.
  - Symbols or sections: `Decision In One Screen`, `Gate 1`, `Gate 2`, `Decision Request`.
- `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_next_material_decisions_v0.md`
  - Status: modified.
  - Role: superseded historical next-decision packet.
  - Important observations: active next steps now route to the physicalization brief.
  - Symbols or sections: `Post-Merge Supersession Note`, `Next Material Steps`.
- `docs/workflows/orca_repo_map_v0.md`
  - Status: modified.
  - Role: source-loading route updated.
  - Important observations: new brief is map-reachable.
  - Symbols or sections: Data Lake rows around the `orca/product/spines/data_lake/workflows/` entries.

## Frozen Decisions

- Decision: The old next-material-decisions packet is not the active continuation anchor.
  - Evidence: patched `superseded_by` header and `Post-Merge Supersession Note`; repo map row added for the new brief.
  - Consequence: New thread should continue from the physicalization brief.
- Decision: No backend/engine/layout/retention/erasure is selected by this patch.
  - Evidence: new brief `Status` and `Non-Claims` sections.
  - Consequence: Any next implementation or ADR must explicitly decide or defer the gates first.

## Mutable Questions

- Question: Is lawful erasure a hard current requirement or an accepted residual for this lane?
  - Why still mutable: Owner has not decided a legal/retention posture in this thread.
  - What would resolve it: Owner says Gate 2 first, or accepts Gate 1 first with retention as a residual.
- Question: Does the owner want an ADR artifact next, or should this branch first be reviewed/committed as a planning closeout?
  - Why still mutable: Current instruction requested patch + handoff, not commit/push/PR.
  - What would resolve it: Fresh-thread owner instruction or explicit decision to continue authoring in the same worktree.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: The old next-material-decisions packet's `Next Material Steps` that said to land a stacked PR and delegated review-patch that artifact.
  - Why stale or dangerous: PR #555 and the new physicalization brief have moved the lane beyond that admin state.
  - Current replacement: Continue from `core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md`.
- Stale instruction, idea, artifact, or finding: Treating #555 green tests as full-GT closeness or physicalization selection.
  - Why stale or dangerous: #555 hardened gates; it did not select AR layout/backend or retention policy.
  - Current replacement: Gate 1/Gate 2 decision brief.

## Commands And Verification Evidence

- Command:
  ```powershell
  git fetch origin main
  ```
  Result:
  - Passed after escalation due initial `.git/FETCH_HEAD` permission denial.
  - Important output: `From https://github.com/eric-foo/orca * branch main -> FETCH_HEAD`.
  - Re-run target so the receiver can confirm rather than trust: `git fetch origin main` if network is allowed.
- Command:
  ```powershell
  git worktree add -b codex/bronze-gt-physicalization-handoff worktrees/bronze-gt-physicalization-handoff origin/main
  ```
  Result:
  - Passed.
  - Important output: branch set up to track `origin/main`; HEAD at `0b17593a Add TikTok live batch probe runner (#553)`.
  - Re-run target: `git status --short --branch` and `git rev-parse HEAD` in the worktree.
- Command:
  ```powershell
  git diff --check
  ```
  Result:
  - Passed exit 0.
  - Important output: only line-ending warnings for two modified files; no whitespace errors.
  - Re-run target: same command.
- Command:
  ```powershell
  python .agents\hooks\check_retrieval_header.py --strict docs\workflows\orca_repo_map_v0.md orca\product\spines\data_lake\workflows\core_spine_v0_data_lake_bronze_full_gt_next_material_decisions_v0.md orca\product\spines\data_lake\workflows\core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md
  ```
  Result:
  - Passed exit 0.
  - Important output: no output.
  - Re-run target: same command.
- Command:
  ```powershell
  python .agents\hooks\check_retrieval_header.py --changed --strict
  ```
  Result:
  - Passed exit 0.
  - Important output: no output.
  - Re-run target: same command.
- Command:
  ```powershell
  python .agents\hooks\header_index.py --strict --base origin/main
  ```
  Result:
  - Exit 0 but not useful for this uncommitted patch; output said `no changed .md files in this diff -- OK`.
  - Re-run target: use targeted `check_retrieval_header.py` until files are staged/committed.
- Command:
  ```powershell
  python .agents\hooks\check_dcp_receipt.py --strict
  ```
  Result:
  - Exit 0 but not useful for this uncommitted patch; output said no changed `.md` files.
  - Re-run target: no DCP receipt expected because this is a workflow decision-request artifact, not a doctrine-changing authority contract.

## Blockers And Risks

- Blocker or risk: Handoff file itself changes dirty state after this packet is written.
  - Evidence: handoff contract requires recording the handoff file; current packet is written after the earlier status snapshot.
  - Likely next action: Fresh thread verifies actual status before acting.
- Blocker or risk: New brief has not had delegated adversarial review-patch.
  - Evidence: no review prompt or report was created in this turn.
  - Likely next action: If the owner wants to rely on the brief as an ADR input, run delegated review-patch or a source-backed review before ratification.
- Blocker or risk: Lawful-erasure requirement is owner/legal-sensitive.
  - Evidence: Gate 2 is explicitly open.
  - Likely next action: Ask owner if erasure is a hard current requirement before selecting backend.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - Branch/head = `codex/bronze-gt-physicalization-handoff` / `0b17593a9cdd8c1b06344d3041d8bc81f1135e8d`.
  - Dirty state includes the three patch files plus this handoff file.
  - File hashes for the three patch files match the ledger above.
  - The new physicalization brief exists and contains Gate 1/Gate 2.
  - The old next-material-decisions packet points to the new brief as active continuation.
  - The repo map includes the new brief path.
- Compare target for each:
  - `git rev-parse HEAD`
  - `git status --short --branch`
  - `Get-FileHash -Algorithm SHA256 <three patch files>`
  - targeted `rg` for `PHYSICALIZATION_DECISION_BRIEF_RECORDED`, `Post-Merge Supersession Note`, and the new path in repo map.
- Load outcomes and what each means:
  - `REUSE`: all required facts re-verified; continue from Exact Next Authorized Action.
  - `PARTIAL_REUSE`: optional context drifted, but patch files and branch/head match; continue after rereading changed sources.
  - `STALE_REREAD_REQUIRED`: branch/head, dirty state, or file hashes drifted but can be re-derived safely.
  - `BLOCKED_DRIFT`: unknown edits conflict with the target files or user constraints.
  - `BLOCKED_MISSING_PACKET`: this handoff path is absent or unreadable.
  - `BLOCKED_UNVERIFIABLE`: a load-bearing claim cannot be re-derived from repo state.
- Sources that must be reread if drift is detected:
  - This handoff packet.
  - The three patch files.
  - Data Lake storage, Attachment Record, physicality-location, write-boundary, raw-admission, and derived-layout contracts.

## Do Not Forget

The next material question is architectural, not evidentiary: Gate 1/Gate 2 must be decided or explicitly deferred before storage code or third-proof work.