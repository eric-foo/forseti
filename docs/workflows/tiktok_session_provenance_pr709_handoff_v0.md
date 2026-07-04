# TikTok Session Provenance PR709 Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow handoff
scope: >
  Cold-reader continuation packet after PR #709 implemented TikTok cold-agent
  capture enforcement batches, added doctrine pickup, and merged current main to
  resolve conflicts.
use_when:
  - Continuing PR #709 after the 2026-07-05 merge-conflict resolution.
  - Verifying the TikTok cold-agent capture route, blocker handling, source-access provenance, and no-solve admission boundary.
  - Preparing the next controlled TikTok live probe or merge-readiness decision.
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/decision-routing.md
  - docs/workflows/tiktok_cold_agent_capture_enforcement_goal_v0.md
  - docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md
  - docs/decisions/tiktok_auth_state_provenance_sidecar_architecture_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
  - orca-harness/docs/source_capture_agent_runbook.md
  - docs/review-outputs/tiktok_capture_enforcement_batches_1_4_post_adjudication_delegated_adversarial_code_review_v0.md
  - orca-harness/runners/run_source_capture_tiktok_live_batch_probe.py
  - orca-harness/runners/run_source_capture_cloakbrowser_profile_warmup.py
  - orca-harness/source_capture/source_access_provenance.py
branch_or_commit: codex/tiktok-session-provenance-implementation @ reread-required-current-PR-head
stale_if:
  - PR #709 is merged, closed, or rebased without this packet being checked against the final branch head.
  - The TikTok live runner, CloakBrowser warmup runner, blocker triage, admission gate, source-access provenance schema, or auth-state sidecar schema changes.
  - The owner changes no-secret, no-solve, owner-attention, or bronze-write policy.
  - A live TikTok probe proves a different browser/backend/session posture is the packet-grade path.
authority_boundary: retrieval_only
```

## Load Contract

- packet_version: v0
- mode: max
- source_loading_mode: repo-overlay-bound
- created_at: 2026-07-05T02:03:28+08:00
- created_by_lane: Codex GPT-5 PR #709 conflict-resolution and handoff lane; provenance only, not authority.
- workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\tiktok-session-provenance-implementation`
- handoff_path: `docs/workflows/tiktok_session_provenance_pr709_handoff_v0.md`
- expected_branch: `codex/tiktok-session-provenance-implementation`
- expected_head: `reread-required-current-PR-head` (a committed handoff cannot self-pin its own SHA; receiver must verify `git rev-parse HEAD` and PR #709 `headRefOid` before acting)
- merge_resolution_head_before_handoff: `15a5b31a8e6cc4682802a7a6b6d9ff3bb51fb171`
- merged_base_ref: `origin/main` at `1b40fc760c32ca9b0d4960333fe866583d202fd9`
- expected_pr: GitHub PR #709, draft/open, base `main`, head branch `codex/tiktok-session-provenance-implementation`.
- expected_dirty_state_after_handoff_commit: clean tracked tree at final head, with only the pre-existing untracked `docs/workflows/tiktok_session_provenance_pr689_handoff_v0.md` if the owner has not removed or committed it elsewhere.
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting. Sender claims are hypotheses, not authority. This packet is not validation, readiness, live TikTok success, account-safety proof, full-network no-proxy proof, CAPTCHA bypass, scale proof, or merge authority.

## Goal Handoff

- long_term_goal: Cold agents should be able to access and capture public TikTok creator/video/comment/subtitle evidence through the sanctioned Orca harness route without re-diagnosing known blockers, leaking secrets, or overclaiming source-access posture.
- anchor_goal: Convert the known TikTok cold-agent failure modes into deterministic runner/admission behavior where the machine can decide setup action, owner-attention, admissible capture, or fail-closed stop from flags and sanitized receipts.
- success_signal: A cold agent can load the goal/playbook/runbook surfaces, run the sanctioned TikTok runner with a warmed dedicated session, and see a clear setup-click, owner-attention, admit, or fail-closed outcome without relying on model memory.

## Open Decision / Fork

- decision: What should happen after PR #709 is conflict-clean and pushed?
  - options:
    - `verify_pr_then_owner_merge`: verify PR #709 is mergeable and checks are acceptable, then leave merge timing to the owner/protected-action flow.
    - `one_probe_before_merge`: run one controlled sessioned TikTok probe from PR #709 before merge, using local `--admit-output` and owner-present human handoff only if needed.
    - `defer_for_new_review`: commission another review if the conflict-resolution diff changes behavior beyond preserving reviewed PR #709 semantics.
  - already constrained / off the table: do not broaden to multiple creators, scale, registry promotion, raw-cookie inspection, proxy endpoint reporting, data-lake writes without explicit owner request, or CAPTCHA/slider automation.
  - trade-offs: `verify_pr_then_owner_merge` keeps WIP low after conflicts are resolved; `one_probe_before_merge` spends browser/account budget but gives live signal; `defer_for_new_review` is appropriate only if validation or diff review shows semantic drift.
  - owner of the call: owner / Chief Architect decides merge timing and whether to spend one live probe before merge.
  - recommendation and why: `verify_pr_then_owner_merge` unless the owner explicitly asks for the live probe. The merge conflicts were resolved without changing the reviewed enforcement contract, and targeted tests plus doc gates passed.

## Drift Guard

- invariant, non-goal, or scope boundary: `no_proxy_profile_loaded` means no harness-loaded proxy profile for the warmed label, not full-network no-proxy proof.
  - why it matters: the source-access provenance schema is category-only and intentionally not an egress attestation system.
  - what violating it would break: no-self-certification and the provenance ADR non-claim.
- invariant, non-goal, or scope boundary: slider/captcha/security prompts are never solved by the agent.
  - why it matters: the accepted path may only click named X/Close controls when `--allow-challenge-close-followthrough` is enabled; remaining challenge requires owner handoff or fail-closed stop.
  - what violating it would break: source-access intervention boundaries and admission safety.
- invariant, non-goal, or scope boundary: owner/manual action is not clean capture and does not count as admission success.
  - why it matters: the runner and batch gate reject owner-attention/manual-challenge receipts before packet/lake write.
  - what violating it would break: clean-capture, no-fake-success, and bronze admission claims.
- invariant, non-goal, or scope boundary: do not use the old PR689 handoff as the active route.
  - why it matters: PR #709 superseded it with code enforcement, doctrine pickup, and a current-main merge.
  - what violating it would break: cold-agent routing and expected-head verification.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- targets to enter the ladder: this handoff; PR #709; `docs/workflows/tiktok_cold_agent_capture_enforcement_goal_v0.md`; `docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md`; `orca-harness/docs/source_capture_agent_runbook.md`; the live runner; the CloakBrowser warmup runner; `source_access_provenance.py`; the delegated review output.
- already loaded (weak orientation, freshness-marked; not authority): AGENTS instructions, overlay README/source-loading/decision-routing/safety/validation gates, goal doc, blocker playbook, runbook, repo map, provenance ADR, TikTok lane spec, review output, conflicted source/test files, PR metadata, and targeted validation outputs through 2026-07-05T02:03+08:00.
- must load first before strict or actionable steps: current branch/head/status, PR #709 metadata, this packet, AGENTS.md, overlay README/source-loading/decision-routing, goal doc, blocker playbook, runbook, provenance ADR, TikTok lane spec, live runner help/source, and chosen auth-state sidecar metadata via the runner gate.
- load rule: receiver re-runs progressive source loading per overlay; the packet's loaded set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- decision, framing, profile, or convention: PR #709 owns code-enforced TikTok cold-agent behavior for BATCH-01 through BATCH-04.
  - decided in: `docs/workflows/tiktok_cold_agent_capture_enforcement_goal_v0.md`
  - compare target: git blob hash `915a2c761410a0d1c22e85c471454847fde4f92d`
  - verify before: any strict claim that a blocker/provenance/admission behavior is implemented.
- decision, framing, profile, or convention: the accepted blocker route uses named pointer actions for benign setup, retry, comments -> You may like / More like this -> comments, and X/Close follow-through only.
  - decided in: `docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md`
  - compare target: git blob hash `0498c628100ed0a3dc1dc47d15a6bd8b7f9ad299`
  - verify before: any UI movement or blocker interpretation.
- decision, framing, profile, or convention: cold agents should use the runbook command with CloakBrowser, dedicated auth-state, required harness proxy posture, local `--admit-output`, and owner handoff only when owner-present.
  - decided in: `orca-harness/docs/source_capture_agent_runbook.md`
  - compare target: git blob hash `c164430755f78c2046a19f340e6583ddcf82d165`
  - verify before: any live probe command.
- decision, framing, profile, or convention: interrupted CloakBrowser warmup must bind provenance before external browser action.
  - decided in: `orca-harness/runners/run_source_capture_cloakbrowser_profile_warmup.py`
  - compare target: git blob hash `f74eaa7c0e55ca35ad3b8c44a52c6ebba54c03a1`
  - verify before: any warmup/provenance ordering claim.
- decision, framing, profile, or convention: source-access provenance must validate proxy posture/category consistency and secret-safe payloads.
  - decided in: `orca-harness/source_capture/source_access_provenance.py`
  - compare target: git blob hash `18b2066f2fac8d1fa7b3c2ae48199447f4952120`
  - verify before: any sidecar/proxy-posture claim.
- decision, framing, profile, or convention: the delegated cross-vendor review recommended keep with no patches and two minor non-blocking notes.
  - decided in: `docs/review-outputs/tiktok_capture_enforcement_batches_1_4_post_adjudication_delegated_adversarial_code_review_v0.md`
  - compare target: git blob hash `cba42afcc06124778341e083d27a3c1ff9e7b886`
  - verify before: any review-outcome claim.

## Active Objective

Continue only PR #709: keep the branch conflict-clean against current `main`, preserve the reviewed TikTok enforcement behavior, update cold-agent handoff state, then verify/push the branch. Do not run a live TikTok probe unless the owner explicitly asks after the conflict-resolution push.

## Exact Next Authorized Action

1. Re-verify PR #709 after push: branch `codex/tiktok-session-provenance-implementation`, expected head `reread-required-current-PR-head`, base `main`, mergeable not `CONFLICTING`.
2. Check GitHub checks for PR #709. If no checks are reported yet, report that observed state and do not claim CI success.
3. If the owner asks for the next material TT lane step, choose between merge-readiness verification and exactly one controlled sessioned live probe using the runbook command and local `--admit-output`.
4. If running a probe, add `--human-challenge-handoff` only while the owner is present. The agent must not drag or solve a slider/captcha; remaining challenge is owner attention or fail closed.

## Authority And Source Ledger

- Repository instructions:
  - `AGENTS.md`
    - Role: project behavior kernel.
    - Load-bearing: yes.
    - Compare target: reread-required before strict/actionable continuation.
    - Last checked: 2026-07-05 in this lane.
    - Reuse rule: reread before further repo-changing work.
- Overlay or equivalent authority:
  - `.agents/workflow-overlay/README.md`
    - Role: overlay entrypoint.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: 2026-07-05 in this lane.
    - Reuse rule: reread before strict overlay claims.
  - `.agents/workflow-overlay/source-loading.md`
    - Role: source-loading doctrine.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: 2026-07-05 in this lane.
    - Reuse rule: reread before acting from this packet.
  - `.agents/workflow-overlay/decision-routing.md`
    - Role: Cynefin routing and delegated-work routing.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: 2026-07-05 in this lane.
    - Reuse rule: reread before planning/delegation/review.
- User constraints:
  - Fix PR #709 conflicts, then update the handoff.
    - Load-bearing: yes.
    - Compare target: current user request in this thread.
    - Last checked: 2026-07-05T02:03+08:00.
    - Reuse rule: complete this request only; do not infer live-probe permission.
- Source-read ledger:
  - `docs/workflows/tiktok_cold_agent_capture_enforcement_goal_v0.md`
    - Role: active TikTok cold-agent goal and operating contract.
    - Load-bearing: yes.
    - Compare target: git blob hash `915a2c761410a0d1c22e85c471454847fde4f92d` at merge-resolution head.
    - Last checked: 2026-07-05T02:03+08:00.
    - Reuse rule: reread before strict/actionable TikTok capture claims.
  - `docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md`
    - Role: blocker/UI movement doctrine.
    - Load-bearing: yes.
    - Compare target: git blob hash `0498c628100ed0a3dc1dc47d15a6bd8b7f9ad299` at merge-resolution head.
    - Last checked: 2026-07-05T02:03+08:00.
    - Reuse rule: reread before UI action or blocker classification.
  - `orca-harness/docs/source_capture_agent_runbook.md`
    - Role: copyable runner command and source-capture operator boundary.
    - Load-bearing: yes.
    - Compare target: git blob hash `c164430755f78c2046a19f340e6583ddcf82d165` at merge-resolution head.
    - Last checked: 2026-07-05T02:03+08:00.
    - Reuse rule: reread before any live probe command.
  - `orca-harness/runners/run_source_capture_tiktok_live_batch_probe.py`
    - Role: live runner CLI, summary, and admission-chain entrypoint.
    - Load-bearing: yes.
    - Compare target: git blob hash `7b6810b88cbf5922de021ba62b92d9f5efad319c` at merge-resolution head.
    - Last checked: 2026-07-05T02:03+08:00.
    - Reuse rule: reread or run `--help` before invoking.
  - `orca-harness/runners/run_source_capture_cloakbrowser_profile_warmup.py`
    - Role: CloakBrowser warmup and pre-browser provenance bind.
    - Load-bearing: yes.
    - Compare target: git blob hash `f74eaa7c0e55ca35ad3b8c44a52c6ebba54c03a1` at merge-resolution head.
    - Last checked: 2026-07-05T02:03+08:00.
    - Reuse rule: reread before warmup/provenance ordering claims.
  - `orca-harness/source_capture/source_access_provenance.py`
    - Role: source-access provenance schema and validators.
    - Load-bearing: yes.
    - Compare target: git blob hash `18b2066f2fac8d1fa7b3c2ae48199447f4952120` at merge-resolution head.
    - Last checked: 2026-07-05T02:03+08:00.
    - Reuse rule: reread before provenance/no-secret claims.
- Source gaps:
  - No live TikTok probe was run in this conflict-resolution turn.
  - No auth-state, cookie, storage-state, token, proxy endpoint, exit IP, or device ID was read or printed.
- Strict-only blockers:
  - If PR #709 remains `CONFLICTING` after push, do not proceed to live probe; fix mergeability first.
  - If checks fail after push, inspect CI before merge-readiness claims.
- Not-proven boundaries:
  - Not live capture success, account safety, scale, full-network no-proxy proof, CAPTCHA bypass, or bronze/data-lake correctness.

## Current Task State

- Completed:
  - Fetched current `origin/main` (`1b40fc760c32ca9b0d4960333fe866583d202fd9`).
  - Merged `origin/main` into PR #709 branch and resolved conflicts in seven files.
  - Preserved PR #709's reviewed semantics: pre-warmup provenance write, proxy posture/category validation, JSON summary support, and compatible tests/docs.
  - Fixed the merge-induced duplicate argparse registration for `--require-harness-proxy-posture`.
  - Targeted Python validation and doc gates passed before the handoff write.
- Partially completed:
  - Push/remote PR verification will happen after this handoff commit is finalized.
- Broken or uncertain:
  - GitHub PR #709 still showed the old remote head `00570b33e29af854c191862e122e9ae364a630c8` before push; mergeability was `UNKNOWN` because the local merge had not yet been pushed.

## Workspace State

- Branch: `codex/tiktok-session-provenance-implementation`
- Head before handoff write: `15a5b31a8e6cc4682802a7a6b6d9ff3bb51fb171`
- Expected final head after committing this handoff: `reread-required-current-PR-head`
- Dirty or untracked state before handoff write: only pre-existing untracked `docs/workflows/tiktok_session_provenance_pr689_handoff_v0.md` after merge commit.
- Dirty or untracked state after writing the handoff file: this handoff file and repo-map edit are dirty until committed; the PR689 handoff remains untracked and should not be treated as the active route.
- Target files or artifacts: PR #709 branch, this handoff, repo-map entry, TikTok goal/playbook/runbook/review report, live runner, warmup runner, provenance source.
- Related worktrees or branches: base `origin/main` at `1b40fc760c32ca9b0d4960333fe866583d202fd9`.

## Changed / Inspected / Tested Files

- `orca-harness/runners/run_source_capture_cloakbrowser_profile_warmup.py`
  - Status: conflicted, resolved, tested.
  - Role: preserve pre-browser provenance sidecar write.
  - Important observations: write remains before `warmup_engine.warm_profile(...)`; deferred duplicate write was not kept.
- `orca-harness/source_capture/source_access_provenance.py`
  - Status: conflicted add/add, resolved, tested.
  - Role: provenance schema/validators.
  - Important observations: `_validate_proxy_category_matches_posture(payload)` remains in construction and validation paths.
- `orca-harness/runners/run_source_capture_tiktok_live_batch_probe.py`
  - Status: conflicted/resolved, then patched for duplicate argparse registration.
  - Role: live runner CLI and summary output.
  - Important observations: `json` import and `TIKTOK_BROWSER_BACKEND_CLOAKBROWSER` import remain; only one `--require-harness-proxy-posture` argument exists.
- `orca-harness/tests/unit/test_source_capture_authenticated_browser_snapshot.py`
  - Status: conflicted, resolved, tested.
  - Role: warmup/provenance regression tests.
  - Important observations: both interrupted-warmup and conflicting-rewarm tests remain.
- `orca-harness/tests/unit/test_tiktok_live_batch_probe.py`
  - Status: conflicted, resolved, tested.
  - Role: runner CLI/blocker/admission tests.
  - Important observations: packet-grade default, diagnostic backend, and handoff/followthrough tests remain.
- `docs/workflows/forseti_repo_map_v0.md`
  - Status: conflicted, resolved, then updated for this handoff.
  - Role: cold retrieval/navigation.
- `orca-harness/docs/source_capture_agent_runbook.md`
  - Status: conflicted, resolved, doc-gated.
  - Role: copyable cold-agent command and no-solve boundary.

## Frozen Decisions

- Decision: Keep PR #709's pre-warmup provenance write over main's deferred write.
  - Evidence: review output Finding/attack result 2 and passing interrupted-warmup test.
  - Consequence: retry after interrupted warmup cannot silently reuse a profile under changed proxy posture.
- Decision: Keep `source_access_provenance.py` posture/category validation at construction time.
  - Evidence: PR #709 test `test_browser_user_data_provenance_rejects_none_category_as_loaded_proxy` and passing targeted suite.
  - Consequence: `proxy_category="none"` cannot self-certify a loaded-proxy posture.
- Decision: Do not use PR689 handoff as active continuation route.
  - Evidence: PR #709 goal doc and repo map now route cold agents to the PR #709 goal/playbook/runbook/review surfaces.
  - Consequence: old PR689 packet is superseded orientation only unless the owner explicitly asks to inspect it.

## Mutable Questions

- Question: Should PR #709 be merged before the first controlled live probe?
  - Why still mutable: conflict resolution and targeted tests are complete, but no live TikTok probe was run in this turn.
  - What would resolve it: owner decision after PR #709 is pushed and mergeability/checks are observed.
- Question: Should the old untracked PR689 handoff be deleted, committed as historical, or ignored?
  - Why still mutable: it is user/worktree state not created in this turn, and deleting it is not needed to fix PR #709.
  - What would resolve it: owner instruction or a separate repo-hygiene pass.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: `docs/workflows/tiktok_session_provenance_pr689_handoff_v0.md`
  - Why stale or dangerous: it pins PR #689/head `af8a12f...` and pre-PR709 next actions.
  - Current replacement: this PR #709 handoff plus `docs/workflows/tiktok_cold_agent_capture_enforcement_goal_v0.md`.
- Stale instruction, idea, artifact, or finding: treating `platform_challenge_observed` as a single terminal class.
  - Why stale or dangerous: the runner now carries `matched_marker` and `challenge_kind`, and X/Close follow-through is authorized only through named action substrate.
  - Current replacement: blocker playbook and live-runner receipts.
- Stale instruction, idea, artifact, or finding: using label text such as `noproxy` as proof.
  - Why stale or dangerous: labels are operator text and do not clear no-self-certification.
  - Current replacement: auth-state sidecar provenance validation and `--require-harness-proxy-posture` gate.

## Commands And Verification Evidence

- Command:
  ```powershell
  git fetch origin main
  ```
  Result:
  - Passed after sandbox escalation.
  - Important output: `8be03976..1b40fc76 main -> origin/main`.
  - Re-run target: `git rev-parse origin/main`.
- Command:
  ```powershell
  git merge origin/main
  ```
  Result:
  - Initially conflicted in seven files; conflicts resolved and merge commit `15a5b31a8e6cc4682802a7a6b6d9ff3bb51fb171` created.
  - Re-run target: `git log -1 --pretty=fuller --stat`.
- Command:
  ```powershell
  python -m py_compile runners\run_source_capture_cloakbrowser_profile_warmup.py runners\run_source_capture_tiktok_live_batch_probe.py source_capture\source_access_provenance.py
  ```
  Result:
  - Passed, no output.
  - Re-run target: run from `orca-harness/`.
- Command:
  ```powershell
  python -m pytest tests\unit\test_source_capture_authenticated_browser_snapshot.py tests\unit\test_tiktok_live_batch_probe.py tests\unit\test_tiktok_batch_admission.py tests\unit\test_tiktok_blocker_triage.py -q
  ```
  Result:
  - First run failed because merge resolution duplicated `--require-harness-proxy-posture` argparse registration.
  - After deleting the duplicate, passed with 106 dots and no failures (`67%` then `100%`).
  - Re-run target: run from `orca-harness/`.
- Command:
  ```powershell
  git diff --check
  ```
  Result:
  - Passed, no output after duplicate fix.
- Command:
  ```powershell
  python .agents\hooks\check_retrieval_header.py --strict
  python .agents\hooks\header_index.py --strict
  python .agents\hooks\check_dcp_receipt.py --strict
  python .agents\hooks\check_handoff_pointers.py --strict
  python .agents\hooks\check_review_routing.py --strict
  python .agents\hooks\check_map_links.py --strict
  ```
  Result:
  - Passed before this handoff write. Header index reported 6 changed durable `.md` files map-reachable; handoff pointers 0 findings in 9 changed files; review routing OK; map links OK with 34 annotated nonresolving debt.
  - Re-run target: rerun after the handoff commit/amend.

## Blockers And Risks

- Blocker or risk: PR #709 remote head still old until push.
  - Evidence: `gh pr view 709` before push showed `headRefOid=00570b33...`.
  - Likely next action: push final branch and re-query PR metadata.
- Blocker or risk: GitHub may report no checks yet immediately after push.
  - Evidence: prior PR checks sometimes returned no checks reported.
  - Likely next action: report observed check state, do not claim CI success unless a check is actually observed passing.
- Blocker or risk: live TikTok access remains unproven after this conflict-resolution turn.
  - Evidence: no browser/live probe was run.
  - Likely next action: owner decides whether to spend one controlled probe.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - Branch/head/status equals this packet's expected branch/head and dirty-state notes.
  - PR #709 remote head equals expected final head and is not `CONFLICTING`.
  - The goal doc, playbook, runbook, live runner, warmup runner, provenance source, and review report still match the recorded compare targets or have been reread.
  - Targeted tests and doc gates are either rerun or treated as historical evidence only.
  - No raw auth-state/cookie/proxy/token material is printed or inspected.
- Compare target for each: final head SHA, blob hashes listed above, explicit command re-run targets, or `reread-required` where dynamic.
- Load outcomes and what each means:
  - `REUSE`: all load-bearing facts reverified; proceed to PR verification or owner-chosen probe.
  - `PARTIAL_REUSE`: optional context drifted; reread changed optional docs before use.
  - `STALE_REREAD_REQUIRED`: head/source/test evidence drifted but can be rederived; rerun source loading and validation before acting.
  - `BLOCKED_DRIFT`: PR/head/source drift conflicts with this packet or user constraints.
  - `BLOCKED_MISSING_PACKET`: this file is absent or unreadable.
  - `BLOCKED_UNVERIFIABLE`: a load-bearing claim cannot be checked from repo/source/tool state.
- Sources that must be reread if drift is detected: goal doc, playbook, runbook, live runner, warmup runner, source-access provenance source, TikTok lane spec, and review output.

## Do Not Forget

- A slider/captcha can be closed only by the named X/Close follow-through path when enabled; otherwise owner handoff or fail closed. Never drag or solve.
- `no_proxy_profile_loaded` is harness proxy-profile posture only.
- Read `tiktok_live_probe_summary_json=` first after any probe.
