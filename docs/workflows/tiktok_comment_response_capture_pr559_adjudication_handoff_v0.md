# TikTok Comment Response Capture PR #559 Adjudication Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: >
  Cold-lane handoff after adjudicating the de-correlated adversarial review of
  PR #559, TikTok live comment-response capture hardening.
use_when:
  - Resuming the PR #559 merge/readiness lane from a fresh thread.
  - Continuing to the next owner-gated TikTok live probe step after PR #559 is merged.
open_next:
  - docs/review-outputs/tiktok_comment_response_capture_adversarial_code_review_v0.md
  - docs/prompts/reviews/tiktok_comment_response_capture_adversarial_code_review_prompt_v0.md
  - orca-harness/source_capture/tiktok/live_batch_probe.py
  - orca-harness/source_capture/adapters/browser_snapshot.py
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/review-lanes.md
branch_or_commit: codex/tiktok-comment-body-capture-probe @ f8a30acccaa61b18c144872d8fe28191cfeaa84b
stale_if:
  - PR #559 head commit, state, or checks change.
  - The review report changes.
  - Any target implementation/test file changes after f8a30acccaa61b18c144872d8fe28191cfeaa84b.
  - A newer TikTok live probe artifact supersedes the two control artifacts named here.
authority_boundary: retrieval_only
```

## Load Contract

- packet_version: `v0`
- mode: `max`
- created_at: `2026-07-02T15:01:02+08:00`
- created_by_lane: OpenAI/GPT-family Codex, adjudication and handoff authoring lane; provenance only, not authority.
- workspace: `C:\tmp\orca-tiktok-live-smoke-main`
- handoff_path: `C:\tmp\orca-tiktok-live-smoke-main\docs\workflows\tiktok_comment_response_capture_pr559_adjudication_handoff_v0.md`
- expected_branch: `codex/tiktok-comment-body-capture-probe`
- expected_head: `f8a30acccaa61b18c144872d8fe28191cfeaa84b`
- expected_dirty_state_including_handoff_file:
  - `?? docs/prompts/reviews/tiktok_comment_response_capture_adversarial_code_review_prompt_v0.md`
  - `?? docs/review-outputs/tiktok_comment_response_capture_adversarial_code_review_v0.md`
  - `?? docs/workflows/tiktok_comment_response_capture_pr559_adjudication_handoff_v0.md`
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

`goal_handoff`: not supplied.

Output-fit warning: no upstream `goal_handoff` block was supplied in the current context. The receiver should use the Active Objective and Drift Guard below, then rebind any broader goal from current owner instruction before expanding scope.

## Open Decision / Fork

- decision: whether to merge PR #559 as-is after final green checks, or patch minor advisories first.
  - options:
    - Merge after final green checks, preserving the narrow claim that this proves plumbing/filtering and not live comment capture.
    - Patch one or more minor hardening items before merge.
  - already constrained / off the table:
    - Do not claim live comment capture works from the current evidence.
    - Do not run a 3-5 creator live batch before a single-video non-challenge gate succeeds.
    - Do not inspect, print, or alter cookies, tokens, auth-state contents, or proxy secrets.
  - trade-offs:
    - Merging now unblocks the next real live probe while keeping the patch narrow and reviewed.
    - Patching minor items first adds delay and risk of churn, with no critical/major defect found.
  - owner of the call: Orca owner / Chief Architect, plus repository protected-action guard for merge mechanics.
  - recommendation and why: merge PR #559 after final check remains green; treat the three review findings as accepted residuals or later hardening, not merge blockers.

## Drift Guard

- invariant, non-goal, or scope boundary: PR #559 is a plumbing and hardening patch, not proof that real TikTok comment capture works.
  - why it matters: the only live control completion had `response_count=0` and `matched_comment_response_count=0`.
  - what violating it would break: it would turn zero-response admission compatibility into a false product/capture claim.
- invariant, non-goal, or scope boundary: stop-on-challenge governs the next live step.
  - why it matters: the wait-variant live run stopped on `platform_challenge_observed`.
  - what violating it would break: running a broad 3-5 creator batch into a challenge would violate the lane's account-safety posture.
- invariant, non-goal, or scope boundary: source files are reviewed read-only in this handoff; no patch is authorized by this packet.
  - why it matters: the review found no critical/major issues and this packet only transfers state.
  - what violating it would break: it would bypass owner/CA adjudication and create unreviewed post-review changes.
- invariant, non-goal, or scope boundary: product mentions, product value, Judgment extraction, cross-creator proof, and buyer-proof claims stay out of this lane.
  - why it matters: owner explicitly deferred product mentions earlier; current evidence is capture-mechanics only.
  - what violating it would break: it would blur capture plumbing with downstream product or Judgment claims.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- targets to enter the ladder:
  - PR #559 branch/head/checks.
  - `docs/review-outputs/tiktok_comment_response_capture_adversarial_code_review_v0.md`
  - `orca-harness/source_capture/tiktok/live_batch_probe.py`
  - `orca-harness/source_capture/adapters/browser_snapshot.py`
  - optional live control artifacts under `C:\tmp\orca-tiktok-live-smoke-output\`.
- already loaded (weak orientation, freshness-marked; not authority):
  - Attached delegated review return from `C:\Users\vmon7\.codex\attachments\9e1355f4-e48e-4413-95a1-5db2540d157e\pasted-text.txt`, read 2026-07-02.
  - Durable review report, prompt file, target code line windows, live control JSON artifacts, PR metadata, and PR checks were read by this lane before writing this packet.
- must load first (before strict or actionable steps):
  - `AGENTS.md`
  - `.agents/workflow-overlay/README.md`
  - `.agents/workflow-overlay/source-loading.md`
  - this handoff packet
  - the review report
  - current `git status --short --branch`, `git rev-parse HEAD`, and PR #559 state/checks.
- load rule: receiver re-runs progressive source loading per overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- decision, framing, profile, or convention: delegated review output is decision input, not approval, validation, or merge authority.
  - decided in: `.agents/workflow-overlay/review-lanes.md`
  - compare target: reread-required.
  - verify before: treating any review verdict as binding.
- decision, framing, profile, or convention: PR #559 review was read-only adversarial code review, not patch execution.
  - decided in: `docs/prompts/reviews/tiktok_comment_response_capture_adversarial_code_review_prompt_v0.md`
  - compare target: SHA256 `D97CA1BCF2237F836C07D20682345497910015276B6D7D9180CCA59AA2A95E8F`.
  - verify before: asking a reviewer or continuation lane to edit code.
- decision, framing, profile, or convention: TikTok live capture must stop on challenge/auth-wall/empty-shell class.
  - decided in: `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md`
  - compare target: reread-required.
  - verify before: running any live TikTok probe.

## Active Objective

Carry PR #559 from de-correlated review adjudication to owner merge/readiness, then prepare the next lane for a bounded post-merge live probe that proves or falsifies real page-owned comment-list capture without violating stop-on-challenge.

## Exact Next Authorized Action

1. Fresh-read PR #559: confirm head remains `f8a30acccaa61b18c144872d8fe28191cfeaa84b`, checks remain green, and no target files changed.
2. If the owner/merge guard authorizes merge, merge PR #559 as-is. If merge is not authorized, report it as adjudicated merge-compatible but unmerged.
3. After PR #559 lands on main, create a clean continuation worktree or branch from current main for the next live probe lane.
4. Run exactly one owner-gated live retry first, not a 3-5 creator batch. The retry must use bounded session mode, stop on any challenge/auth-wall/empty-shell, and produce sanitized staging JSON plus offline admission if completed.
5. Expand to 3-5 creators only if the first retry has `challenge_count=0`, no empty/stripped shell, and either captures at least one real page-owned `/api/comment/list` response or records a deliberate owner decision that zero-response routing is the next diagnosis target.

## Authority And Source Ledger

- Repository instructions:
  - `AGENTS.md`
    - Role: Orca project behavior kernel.
    - Load-bearing: yes.
    - Compare target: supplied in current conversation and must be reread from repo before strict continuation.
    - Last checked: current conversation plus repo overlay use, 2026-07-02.
    - Reuse rule: reread-required before merge or source-changing work.
- Overlay or equivalent authority:
  - `.agents/workflow-overlay/README.md`
    - Role: Orca overlay entrypoint.
    - Load-bearing: yes.
    - Compare target: read from repo 2026-07-02.
    - Last checked: 2026-07-02.
    - Reuse rule: reread if overlay changed.
  - `.agents/workflow-overlay/source-loading.md`
    - Role: source-loading and start-preflight authority.
    - Load-bearing: yes.
    - Compare target: read from repo 2026-07-02.
    - Last checked: 2026-07-02.
    - Reuse rule: reread before strict/actionable claims.
  - `.agents/workflow-overlay/review-lanes.md`
    - Role: review-use and de-correlation boundary.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: earlier prompt-authoring turn and current report source.
    - Reuse rule: reread before treating review output as binding.
- User constraints:
  - Current request: "adjudicate, then handoff."
    - Role: current owner instruction.
    - Load-bearing: yes.
    - Compare target: current message.
    - Last checked: 2026-07-02.
    - Reuse rule: current-turn authority only; newer owner instruction overrides.
  - Prior owner constraint: product mentions deferred; next live work owner-gated; check on one before broader 3-5 expansion.
    - Role: scope and drift guard.
    - Load-bearing: yes.
    - Compare target: current conversation history; reread or owner-confirm if unavailable.
    - Last checked: current context summary.
    - Reuse rule: use as orientation unless superseded by current owner instruction.
- Source-read ledger:
  - `docs/review-outputs/tiktok_comment_response_capture_adversarial_code_review_v0.md`
    - Role: de-correlated adversarial review output.
    - Load-bearing: yes.
    - Compare target: SHA256 `FF0A045A4EFB6487638999AA4EEF2931ACE4FECFA35142D41DA69DAC9BFCDD52`.
    - Last checked: 2026-07-02.
    - Reuse rule: rehash and reread before relying on findings.
  - `docs/prompts/reviews/tiktok_comment_response_capture_adversarial_code_review_prompt_v0.md`
    - Role: review commission prompt.
    - Load-bearing: yes.
    - Compare target: SHA256 `D97CA1BCF2237F836C07D20682345497910015276B6D7D9180CCA59AA2A95E8F`.
    - Last checked: 2026-07-02.
    - Reuse rule: rehash and reread if report/commission scope matters.
  - `orca-harness/source_capture/adapters/browser_snapshot.py`
    - Role: implementation target.
    - Load-bearing: yes.
    - Compare target: SHA256 `331CF7B803B3E19ED43D4689A687181C2E3ABB7E14E85AA7F3A2B55564E820DC`.
    - Last checked: 2026-07-02.
    - Reuse rule: rehash/reread before code claims.
  - `orca-harness/source_capture/tiktok/live_batch_probe.py`
    - Role: implementation target.
    - Load-bearing: yes.
    - Compare target: SHA256 `DA5DDE46B77E053DEDFF2E7AC5AF9E5E6A4B19375AD098620A7EADA06F4CC6BF`.
    - Last checked: 2026-07-02.
    - Reuse rule: rehash/reread before code claims or live run.
  - `orca-harness/tests/unit/test_source_capture_browser_snapshot.py`
    - Role: test target.
    - Load-bearing: yes.
    - Compare target: SHA256 `45D714F6CD3D9F30822E3D7F64BE33F9E6631B3D82EF9C8AFBAFC4327C44E430`.
    - Last checked: 2026-07-02.
    - Reuse rule: rehash/reread before test-coverage claims.
  - `orca-harness/tests/unit/test_tiktok_live_batch_probe.py`
    - Role: test target.
    - Load-bearing: yes.
    - Compare target: SHA256 `DA5E101CDD30D8F1133F4E74384C59DB11FD4F77280939A5050E411D7D3EF2A9`.
    - Last checked: 2026-07-02.
    - Reuse rule: rehash/reread before test-coverage claims.
  - `C:\tmp\orca-tiktok-live-smoke-output\tiktok_control_patch_probe_20260702T000000Z\tiktok_live_cadence_result.json`
    - Role: live control completion artifact.
    - Load-bearing: yes.
    - Compare target: SHA256 `83D1C522584B7ACD31B1E5C139E87C392D758410BBD04DE02FDC361B1709C676`.
    - Last checked: 2026-07-02.
    - Reuse rule: rehash/reread before live-evidence claims.
  - `C:\tmp\orca-tiktok-live-smoke-output\tiktok_control_patch_probe_wait_20260702T000000Z\tiktok_live_cadence_result.json`
    - Role: live challenge-stop artifact.
    - Load-bearing: yes.
    - Compare target: SHA256 `CB375FFB115ABF1F820F970729FD54E38DEB1742CBA8B52F320CB374139F606F`.
    - Last checked: 2026-07-02.
    - Reuse rule: rehash/reread before challenge-stop claims.
- Source gaps:
  - This handoff did not rerun the 70-test pytest slice; it relies on the review report for that validation evidence and on fresh `gh pr checks 559`.
  - This handoff did not run live TikTok capture.
- Strict-only blockers:
  - PR #559 readiness for merge is not proven if head, checks, or target files drift.
  - Live comment capture remains not proven until a real page-owned comment-list response is captured under owner-gated live conditions.
- Not-proven boundaries:
  - Not product proof.
  - Not cross-creator ceiling proof.
  - Not Judgment extraction.
  - Not account-safety-at-scale evidence.
  - Not merge authority.

## Current Task State

- Completed:
  - PR #559 implementation was authored, committed, pushed, and opened as draft before this handoff.
  - De-correlated adversarial review was run and wrote `docs/review-outputs/tiktok_comment_response_capture_adversarial_code_review_v0.md`.
  - Review found no critical or major findings and recommended `merge_after_green`.
  - This adjudication accepts the review result: no source patch is required before merge.
- Partially completed:
  - Review prompt and report are untracked in the PR worktree. They are useful workflow artifacts but not committed.
  - PR #559 remains draft at the time of this handoff.
- Broken or uncertain:
  - Real live comment capture is unproven.
  - Last wait-variant live run hit `platform_challenge_observed`.

## Workspace State

- Branch: `codex/tiktok-comment-body-capture-probe`
- Head: `f8a30acccaa61b18c144872d8fe28191cfeaa84b`
- PR state observed 2026-07-02:
  - PR: `https://github.com/eric-foo/orca/pull/559`
  - title: `Harden TikTok live comment response capture`
  - state: `OPEN`
  - draft: `true`
  - base: `main`
  - head branch: `codex/tiktok-comment-body-capture-probe`
  - head OID: `f8a30acccaa61b18c144872d8fe28191cfeaa84b`
- PR checks observed 2026-07-02:
  - `orca-harness-tests`: pass, `1m32s`, `https://github.com/eric-foo/orca/actions/runs/28547983189/job/84638010812`
- Dirty or untracked state before handoff:
  - `?? docs/prompts/reviews/tiktok_comment_response_capture_adversarial_code_review_prompt_v0.md`
  - `?? docs/review-outputs/tiktok_comment_response_capture_adversarial_code_review_v0.md`
- Dirty or untracked state after writing the handoff file:
  - `?? docs/prompts/reviews/tiktok_comment_response_capture_adversarial_code_review_prompt_v0.md`
  - `?? docs/review-outputs/tiktok_comment_response_capture_adversarial_code_review_v0.md`
  - `?? docs/workflows/tiktok_comment_response_capture_pr559_adjudication_handoff_v0.md`
- Target files or artifacts:
  - PR target files: `browser_snapshot.py`, `live_batch_probe.py`, `test_source_capture_browser_snapshot.py`, `test_tiktok_live_batch_probe.py`
  - Review artifacts: prompt, report, this handoff packet.
- Related worktrees or branches:
  - `C:\tmp\orca-tiktok-live-smoke-main`, branch `codex/tiktok-comment-body-capture-probe`.

## Changed / Inspected / Tested Files

- `orca-harness/source_capture/adapters/browser_snapshot.py`
  - Status: committed in PR #559, inspected.
  - Role: implementation target.
  - Important observations: optional request metadata extraction returns HTTP method/resource type only; defensive failures return `None`.
  - Symbols or sections: `_response_request_metadata`, `_read_observed_page_responses`.
- `orca-harness/source_capture/tiktok/live_batch_probe.py`
  - Status: committed in PR #559, inspected.
  - Role: implementation target.
  - Important observations: post-load script clicks a comment-like control and waits 2500 ms; page-owned comment-list filter requires TikTok `/api/comment/list` and rejects non-GET/non-fetch/xhr when metadata exists.
  - Symbols or sections: `TIKTOK_OPEN_COMMENTS_POST_LOAD_SCRIPT`, `_cadence_row_from_capture`, `_is_page_owned_comment_list_response`.
- `orca-harness/tests/unit/test_source_capture_browser_snapshot.py`
  - Status: committed in PR #559, inspected.
  - Role: test target.
  - Important observations: happy-path request metadata preservation is tested; metadata failure branches are not.
- `orca-harness/tests/unit/test_tiktok_live_batch_probe.py`
  - Status: committed in PR #559, inspected.
  - Role: test target.
  - Important observations: fake-engine test proves non-GET response is filtered and GET/fetch response is retained.
- `docs/prompts/reviews/tiktok_comment_response_capture_adversarial_code_review_prompt_v0.md`
  - Status: untracked, inspected and hashed.
  - Role: review prompt.
  - Important observations: read-only, de-correlated, no live-run, no patch authority.
- `docs/review-outputs/tiktok_comment_response_capture_adversarial_code_review_v0.md`
  - Status: untracked, inspected and hashed.
  - Role: review output.
  - Important observations: no critical/major findings; three minor advisories; recommendation `merge_after_green`.
- `docs/workflows/tiktok_comment_response_capture_pr559_adjudication_handoff_v0.md`
  - Status: newly written by this lane.
  - Role: workflow handoff.
  - Important observations: continuation packet only, not authority or validation.

## Frozen Decisions

- Decision: accept the de-correlated review's no-critical/no-major result.
  - Evidence: durable report SHA256 `FF0A045A4EFB6487638999AA4EEF2931ACE4FECFA35142D41DA69DAC9BFCDD52`; local code spot-checks corroborated the three minor advisories.
  - Consequence: no patch is required before merge.
- Decision: preserve the narrow claim scope.
  - Evidence: live control completion had zero responses; wait-variant stopped on challenge.
  - Consequence: merge/readiness can be framed as code/plumbing readiness only, not live comment capture proof.
- Decision: next live continuation must use a single-video gate before broadening.
  - Evidence: challenge-stop artifact with `challenge_count=1`, `completed_count=0`.
  - Consequence: 3-5 creator run is disallowed until the single-video retry passes the drift guard.

## Mutable Questions

- Question: Should MINOR-1 be patched later with an explicit admitted-response cap?
  - Why still mutable: current review treats it as non-blocking; owner may choose hardening after merge.
  - What would resolve it: owner decision or a follow-up patch limiting admitted comment-list responses per video to the intended C3 footprint.
- Question: Should `_response_request_metadata` failure branches get a dedicated test?
  - Why still mutable: current code is correct by inspection but untested for failure branches.
  - What would resolve it: a small unit test in a later hardening PR.
- Question: Is 2500 ms sufficient for live comment-list capture?
  - Why still mutable: no live response was captured.
  - What would resolve it: owner-gated live retry producing at least one real page-owned comment-list response, or a diagnosis showing the UI/action/wait path is insufficient.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: "go 3-5 right off the bat" as an immediate next run.
  - Why stale or dangerous: the wait-variant control run hit `platform_challenge_observed`.
  - Current replacement: one-video live gate first; expand only after no challenge/empty-shell and a clear capture signal or owner-approved zero-response diagnosis.
- Stale instruction, idea, artifact, or finding: treating PR #559's live control as proof that real comments are captured.
  - Why stale or dangerous: control completion had `response_count=0`, `matched_comment_response_count=0`, and `comment_responses=[]`.
  - Current replacement: claim only sanitized staging/admission plumbing plus challenge-stop behavior.
- Stale instruction, idea, artifact, or finding: product mention extraction as near-term scope.
  - Why stale or dangerous: owner deferred product mentions; current lane is capture plumbing.
  - Current replacement: keep next work in TikTok capture mechanics.

## Commands And Verification Evidence

- Command:
  ```powershell
  git rev-parse HEAD
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: `f8a30acccaa61b18c144872d8fe28191cfeaa84b`
  - Re-run target so the receiver can confirm rather than trust: run in `C:\tmp\orca-tiktok-live-smoke-main`.
- Command:
  ```powershell
  git status --short --branch
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output before handoff write: branch `codex/tiktok-comment-body-capture-probe`, two untracked prompt/report docs.
  - Re-run target so the receiver can confirm rather than trust: expect three untracked docs after this handoff file exists.
- Command:
  ```powershell
  git diff --name-only 0b17593a9cdd8c1b06344d3041d8bc81f1135e8d..HEAD
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: exactly four target files.
  - Re-run target so the receiver can confirm rather than trust: same command.
- Command:
  ```powershell
  gh pr view 559 --json number,url,title,state,isDraft,headRefName,baseRefName,headRefOid
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: PR #559 open draft, base `main`, head branch `codex/tiktok-comment-body-capture-probe`, head OID `f8a30acccaa61b18c144872d8fe28191cfeaa84b`.
  - Re-run target so the receiver can confirm rather than trust: same command.
- Command:
  ```powershell
  gh pr checks 559
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: `orca-harness-tests pass 1m32s`.
  - Re-run target so the receiver can confirm rather than trust: same command.
- Command:
  ```powershell
  Get-FileHash -Algorithm SHA256 <prompt/report/target/live-artifact files>
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: hashes recorded in Authority And Source Ledger.
  - Re-run target so the receiver can confirm rather than trust: rehash all load-bearing sources before acting.
- Command:
  ```powershell
  python -m pytest -q orca-harness\tests\unit\test_tiktok_batch_admission.py orca-harness\tests\unit\test_tiktok_batch_coverage.py orca-harness\tests\unit\test_tiktok_batch_projection.py orca-harness\tests\unit\test_tiktok_video_admission.py orca-harness\tests\unit\test_tiktok_live_batch_probe.py orca-harness\tests\unit\test_source_capture_browser_snapshot.py
  ```
  Result:
  - Passed/failed/not run: not rerun by this adjudication lane.
  - Important output: review report records `70 passed`; CI records `orca-harness-tests pass`.
  - Re-run target so the receiver can confirm rather than trust: rerun if merge decision depends on local validation.

## Blockers And Risks

- Blocker or risk: PR still draft/unmerged.
  - Evidence: `gh pr view 559` returned `isDraft: true`, `state: OPEN`.
  - Likely next action: owner/merge actor makes final merge/ready decision after final green check.
- Blocker or risk: real comment capture unproven.
  - Evidence: live control completion has zero responses.
  - Likely next action: single-video owner-gated live retry after merge.
- Blocker or risk: platform challenge observed on wait-variant run.
  - Evidence: challenge artifact has `challenge_count=1`, `reason=platform_challenge_observed`.
  - Likely next action: do not expand; stop on challenge and diagnose route/session if repeated.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - Workspace exists at `C:\tmp\orca-tiktok-live-smoke-main`.
  - Branch/head are `codex/tiktok-comment-body-capture-probe` and `f8a30acccaa61b18c144872d8fe28191cfeaa84b`.
  - Dirty state has exactly the expected untracked workflow artifacts, unless owner has since committed/removed them.
  - PR #559 remains at the expected head and checks are green.
  - Review report hash matches `FF0A045A4EFB6487638999AA4EEF2931ACE4FECFA35142D41DA69DAC9BFCDD52`.
  - Target implementation/test file hashes match the ledger if the receiver is relying on this adjudication.
  - Live control JSON hashes match the ledger if the receiver is relying on live-evidence claims.
- Compare target for each:
  - Git branch/head: `git status --short --branch`, `git rev-parse HEAD`.
  - PR state/checks: `gh pr view 559`, `gh pr checks 559`.
  - Files: SHA256 hashes in Authority And Source Ledger.
  - Live artifacts: SHA256 hashes in Authority And Source Ledger.
- Load outcomes and what each means:
  - `REUSE`: all required load-bearing facts match; continue from Exact Next Authorized Action.
  - `PARTIAL_REUSE`: only optional/non-load-bearing facts drifted; reuse verified PR/review state and rederive the rest.
  - `STALE_REREAD_REQUIRED`: head, PR state, checks, review report, target files, or live artifacts drifted but can be reread safely.
  - `BLOCKED_DRIFT`: drift conflicts with target PR, owner constraints, dirty-state policy, or live-safety guard.
  - `BLOCKED_MISSING_PACKET`: this handoff path is absent/unreadable.
  - `BLOCKED_UNVERIFIABLE`: a load-bearing claim lacks a compare target and cannot be re-derived.
- Sources that must be reread if drift is detected:
  - Review prompt and report.
  - The four PR target files.
  - TikTok lane spec.
  - Current PR #559 metadata/checks.

## Do Not Forget

- The adjudication is: merge-compatible after final green checks, no pre-merge patch required, three minor advisories accepted as residuals.
- The live claim is narrow: sanitized staging/admission plumbing works with zero comment responses; stop-on-challenge works. Real comment capture is not proven.
- The next live run is one-video first. Do not run 3-5 creators until the one-video gate is clean.
