# Delegated adversarial code review-and-patch commission: TikTok persistent onboarding navigation and progress


```yaml
retrieval_header_version: 1
artifact_role: delegated adversarial code review-and-patch commission
scope: >
  Different-vendor review and bounded patch pass for persistent TikTok creator
  onboarding navigation, progress visibility, and Chrome auth-root alignment.
use_when:
  - Reviewing branch codex/chrome-cdp-auth-root-fix before merge.
authority_boundary: retrieval_only
```

## Forseti Prompt Preflight

- Goal: adversarially review the complete PR diff that keeps TikTok creator onboarding on one retained Chrome CDP page, makes direct selected-video navigation explicit, and removes redundant cold-agent orchestration latency through flushed progress/blocker events.
- Mode: repository code review with bounded patch authority.
- Target worktree: `C:\tmp\forseti-persistent-onboarding-review`
- Target branch: `codex/review-tiktok-persistent-onboarding`
- Target revision: `ccc77aaa28cb7a6494de45dc2f7dfa4773ceb61f`
- Base merge point: `dae46bbe8b98d6c3967648491da15244bd26fea5`
- Source range: `origin/main...HEAD`
- Isolation: use the named clean worktree only; do not create or switch branches.
- Controller requirement: use a model family/vendor different from OpenAI Codex/GPT-5 for finding discovery.
- Patch authority: patch only confirmed defects inside the eight named files; leave edits uncommitted.
- Lifecycle boundary: no live browser, TikTok, OAuth, CAPTCHA, data-lake admission, commit, push, merge, or PR mutation.
- Output: write the durable report named below and return a courier summary for Chief Architect adjudication.
- If branch, revision, cleanliness, or any committed blob ID differs, stop and
  report the mismatch.

## Confirm-don't-trust source load

Before strict claims, read `AGENTS.md`, `.agents/workflow-overlay/README.md`,
`.agents/workflow-overlay/delegated-review-patch.md`, and the complete diff plus
all named files. Apply `workflow-deep-thinking` before
`workflow-code-review`. Declare `SOURCE_CONTEXT_READY` only after this load.

Pinned committed Git blobs at the target revision (verify each with
`git rev-parse ccc77aaa28cb7a6494de45dc2f7dfa4773ceb61f:<path>`; do not hash
checkout bytes because Windows line-ending normalization is worktree-dependent):

- `3908ddc1f26c1535cceed886bb03532cd5246b10  forseti-harness/docs/source_capture_agent_runbook.md`
- `04d0f06b6608afb1538b11614c2a21a4f0f045e9  forseti-harness/runners/run_source_capture_chrome_cdp_session.py`
- `a7e66213f8d8d92b33c26bb7562bbcbce63fe416  forseti-harness/runners/run_source_capture_tiktok_creator_onboarding.py`
- `5c223f8c71fde27bc49c63dc8544369e3fc0e4b4  forseti-harness/source_capture/tiktok/creator_onboarding.py`
- `5f409f1b84441d50fd8bddada898805f3637fec2  forseti-harness/source_capture/tiktok/live_batch_probe.py`
- `dc268bcea4581a1e39887c5e34134dca8d33ba47  forseti-harness/tests/unit/test_source_capture_chrome_cdp_session.py`
- `683085b73fc371fefbabd531aa9c3d6bcb28ee9a  forseti-harness/tests/unit/test_tiktok_creator_onboarding.py`
- `5f662e859ad7c75e0ef954f631274a2ef0d9ab84  forseti-harness/tests/unit/test_tiktok_live_batch_probe.py`

## Fitness contract

The accepted behavior is:

1. A warm onboarding run is one CLI invocation. It owns Registry preflight and
   session-alias resolution; agents do not need separate preamble probes unless
   the runner emits a blocker.
2. The retained operator Chrome remains the browser authority. CDP uses one
   runner page sequentially and detaches without closing the operator browser.
3. Selected videos are navigated by their validated direct TikTok URLs in
   selection order on that one page. There is no return to grid between videos.
   The final selected video remains visible after detach.
4. Do not add address-bar typing simulation, referrer spoofing, browser-chrome
   pointer ceremony, fake clicks, OS-level pointer control, or CAPTCHA solving.
   Pointer movement remains limited to meaningful in-page actions already
   required by capture.
5. Progress lines are flushed, machine-readable, non-secret, and useful for
   distinguishing preflight, grid, selection, deep capture, close, admission,
   and fail-loud blocker states.
6. Existing capture artifacts, selection order, challenge handoff, cadence,
   first-comment behavior, auth-state safety, and failure visibility remain
   intact.
7. The Chrome bootstrap default auth-state root remains aligned with logical
   session-profile resolution.

## Adversarial focus

Probe at least:

- whether the claimed one-page/final-video policy matches actual engine
  ownership and close semantics rather than receipt prose alone;
- whether direct navigation can accidentally open new pages, return to grid, or
  reorder selected videos;
- whether progress events are mislabeled, late, buffered, secret-bearing, or
  capable of raising and breaking capture;
- whether the runbook's direct-command instruction hides a necessary preflight
  or weakens a real failure gate;
- whether blocker codes preserve useful failure visibility;
- whether the prior auth-root correction and the new progress work compose;
- API/test compatibility for callers using custom engines or deep-capture
  functions.

Do not manufacture anti-detection features. Review correctness and truthful
contracts, not speculative evasion.

## Patch and validation

Patch only confirmed defects with practical regression proof. Do not broaden the
architecture or alter live-capture policy. Run at minimum:

```powershell
cd C:\tmp\forseti-persistent-onboarding-review\forseti-harness
$env:PYTHONDONTWRITEBYTECODE=1
python -m pytest -p no:cacheprovider -q tests/unit/test_source_capture_chrome_cdp_session.py tests/unit/test_tiktok_creator_onboarding.py tests/unit/test_tiktok_live_batch_probe.py tests/contract
cd ..
python .agents/hooks/check_review_routing.py --strict
git diff --check
```
Output mode: `review-report`.


Write:
`docs/review-outputs/tiktok_persistent_onboarding_navigation_progress_delegated_adversarial_code_review_v0.md`

The report must include provenance, source-readiness, findings ordered by
severity, considered-and-defended hypotheses, exact patch diff if any,
validation evidence, verdict, residual risks, and a courier block. Leave all
review edits and the report uncommitted for owner adjudication.

