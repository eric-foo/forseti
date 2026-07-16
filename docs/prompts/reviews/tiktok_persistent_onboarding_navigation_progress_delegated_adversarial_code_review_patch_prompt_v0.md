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

- Goal: adversarially review the complete implementation diff that keeps TikTok
  onboarding on one retained Chrome page, exposes progress, and hard-stops
  account-risk/auth-wall signals without turning a cleared CAPTCHA into a stop.
- Mode: repository code review with bounded patch authority.
- Target worktree: `C:\tmp\forseti-persistent-onboarding-review`
- Target branch: `codex/review-tiktok-persistent-onboarding`
- Target revision: `3cd83e63f6da22bc109d1f817a16802122cb4bbc`
- Base merge point: `dae46bbe8b98d6c3967648491da15244bd26fea5`
- Source range: `origin/main...HEAD`
- Isolation: use the named clean worktree only; do not create or switch branches.
- Controller requirement: use a model family/vendor different from OpenAI Codex/GPT-5 for finding discovery.
- Patch authority: patch only confirmed defects inside the ten named files; leave edits uncommitted.
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
`git rev-parse 3cd83e63f6da22bc109d1f817a16802122cb4bbc:<path>`; do not hash
checkout bytes because Windows line-ending normalization is worktree-dependent):

- `ceaffa44e6a9d80d6007693f5f333aa3a5351af1  forseti-harness/docs/source_capture_agent_runbook.md`
- `04d0f06b6608afb1538b11614c2a21a4f0f045e9  forseti-harness/runners/run_source_capture_chrome_cdp_session.py`
- `b5e54d1d8d3f11954bfff82c4e6b824e0d35e31b  forseti-harness/runners/run_source_capture_tiktok_creator_onboarding.py`
- `8ec87cc282f5cdc471cd2f55c9188d2f85d433b9  forseti-harness/source_capture/adapters/browser_snapshot.py`
- `6fed79f8c65401260f534400d0e5d721593d7757  forseti-harness/source_capture/tiktok/creator_onboarding.py`
- `e4596148ec1ee20f2cbafa938549ae724162e627  forseti-harness/source_capture/tiktok/live_batch_probe.py`
- `405c55a16873bdf6574fc86f56d42d287f8fdfd7  forseti-harness/tests/unit/test_source_capture_browser_snapshot.py`
- `dc268bcea4581a1e39887c5e34134dca8d33ba47  forseti-harness/tests/unit/test_source_capture_chrome_cdp_session.py`
- `7160f3c7a95ffc2bb8764b6a3a471b9ad710f0d4  forseti-harness/tests/unit/test_tiktok_creator_onboarding.py`
- `6b727b771ced58554e12c807304e2aa7317d3ae4  forseti-harness/tests/unit/test_tiktok_live_batch_probe.py`

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
6. A visible account-risk warning, unexpected logged-out/comment-auth wall, or
   `/login` redirect suppresses scripted actions before the next pointer action,
   stops the batch, forbids automatic retry, leaves Chrome open, and emits
   `ACCOUNT_SAFETY_STOP`. A CAPTCHA cleared by the owner may continue the batch.
7. Engine-specific lifecycle and pre-action guarantees are emitted only when
   the actual selected engine supports them; fallback contracts remain neutral.
8. Existing capture artifacts, selection order, challenge handoff, cadence,
   first-comment behavior, auth-state safety, and failure visibility remain
   intact.
9. The Chrome bootstrap default auth-state root remains aligned with logical
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
- whether account-risk/auth-wall markers suppress actions before CAPTCHA handoff,
  remain non-retriable, propagate into the onboarding receipt and CLI blocker,
  and leave the persistent browser detached rather than closed;
- whether cleared CAPTCHA behavior still continues and remains receipt-marked as
  owner source-access intervention rather than clean capture;
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
python -m pytest -p no:cacheprovider -q tests/unit/test_source_capture_browser_snapshot.py tests/unit/test_source_capture_chrome_cdp_session.py tests/unit/test_tiktok_blocker_triage.py tests/unit/test_tiktok_creator_onboarding.py tests/unit/test_tiktok_live_batch_probe.py tests/contract
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

