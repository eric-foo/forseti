# TikTok Cold-Agent Capture Enforcement Goal v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow goal and implementation batching record
scope: >
  Reference goal, code-enforcement batches, and doctrine split for making cold
  agents able to run TikTok capture with low-latency blocker handling, source-access
  provenance, no raw secrets, and honest admission boundaries.
use_when:
  - Planning or implementing TikTok cold-agent capture hardening.
  - Deciding whether a TikTok blocker rule belongs in code or doctrine.
  - Preparing fused implementation batches for the TikTok live runner and admission path.
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/decision-routing.md
  - docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md
  - docs/decisions/tiktok_auth_state_provenance_sidecar_architecture_v0.md
  - docs/workflows/tiktok_session_provenance_pr689_handoff_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/tiktok/tiktok_sessioned_capture_warm_probe_plan_v0.md
  - orca-harness/runners/run_source_capture_tiktok_live_batch_probe.py
  - orca-harness/source_capture/tiktok/live_batch_probe.py
  - orca-harness/source_capture/tiktok/blocker_triage.py
  - orca-harness/source_capture/source_access_provenance.py
branch_or_commit: codex/tiktok-session-provenance-implementation @ af8a12fba6409958feed1fe0d5329da17ab8e301
stale_if:
  - PR #689 is merged, closed, rebased, or has a head different from af8a12fba6409958feed1fe0d5329da17ab8e301.
  - The TikTok live runner, blocker triage, admission gate, or source-access provenance schema changes.
  - The owner changes no-secret, no-solve, owner-attention, or bronze-write policy.
  - A later TikTok probe proves a different browser/backend route is the packet-grade path.
authority_boundary: retrieval_only
```

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write now; implementation-authorized only for later fused batches after their gates clear
  target_scope: workflow_authority plus validation_philosophy for TikTok cold-agent capture hardening
  dirty_state_checked: yes
  blocked_if_missing: blocker playbook, provenance ADR, TikTok lane spec, live runner, blocker triage, source-access provenance source
```

## Goal Establishing

Long-term goal: cold agents should be able to access and capture public TikTok creator/video/comment/subtitle evidence through the sanctioned Orca harness route without re-diagnosing known blockers, leaking secrets, or overclaiming source-access posture.

Anchor goal: convert the known TikTok cold-agent failure modes into deterministic runner/admission behavior where the machine can decide setup action, owner-attention, admissible capture, or fail-closed stop from flags and sanitized receipts.

Success signal:

- Core success:
  - Owner-observable: a cold agent can load one goal/playbook surface, run the sanctioned TikTok runner with a warmed dedicated session, and see a clear proceed/setup-click/owner-attention/admit/fail-closed outcome.
  - Output fit: future implementation batches should make fewer decisions depend on model memory; code should own mechanically checkable route, blocker, provenance, and admission gates.
  - Boundary: success is not a live capture guarantee, scale proof, account-safety proof, full-network no-proxy proof, CAPTCHA-solving authorization, or creator-registry promotion.
  - Drift cue: the work is drifting if it adds more prose reminders without moving a mechanically checkable blocker or admission rule into code.
- Secondary success signals:
  - The first controlled sessioned probe can run with `cloakbrowser`, `client_provided_session`, `--require-harness-proxy-posture no_proxy_profile_loaded`, named blocker actions, and local `--admit-output` before any bronze write.
  - A failed close, unsupported subtitle host, missing provenance sidecar, or owner-attention condition stops with a typed reason that future agents can act on.

```yaml
goal_handoff:
  long_term_goal: Cold agents should be able to access and capture public TikTok creator/video/comment/subtitle evidence through the sanctioned Orca harness route without re-diagnosing known blockers, leaking secrets, or overclaiming source-access posture.
  anchor_goal: Convert the known TikTok cold-agent failure modes into deterministic runner/admission behavior where the machine can decide setup action, owner-attention, admissible capture, or fail-closed stop from flags and sanitized receipts.
  success_signal:
    core_success:
      owner_observable: A cold agent can load one goal/playbook surface, run the sanctioned TikTok runner with a warmed dedicated session, and see a clear proceed/setup-click/owner-attention/admit/fail-closed outcome.
      output_fit: Future implementation batches should make fewer decisions depend on model memory; code should own mechanically checkable route, blocker, provenance, and admission gates.
      boundary: Not live capture guarantee, scale proof, account-safety proof, full-network no-proxy proof, CAPTCHA-solving authorization, or creator-registry promotion.
      drift_cue: The work is drifting if it adds more prose reminders without moving a mechanically checkable blocker or admission rule into code.
    secondary_success_signals:
      - First controlled sessioned probe can run with cloakbrowser, client_provided_session, required harness proxy posture, named blocker actions, and local admit-output before bronze.
      - Failed close, unsupported subtitle host, missing provenance sidecar, or owner-attention condition stops with a typed reason future agents can act on.
  status: user_stated
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: goal_handoff.anchor_goal
  output_fit_check: goal_handoff.success_signal.core_success.output_fit
  target_delta_from_prior:
    status: changed
    changed_fields: [anchor_goal, success_signal]
    summary: The active target now emphasizes code-enforced cold-agent behavior before more handoff/probe work.
  drift_guard: Do not substitute another prose-only handoff for deterministic TikTok runner/admission enforcement where the rule is mechanically checkable.
  conflict_behavior: call_out_conflict_before_proceeding
```

## Code-Enforced Findings

These belong in deterministic runner, blocker-triage, provenance, receipt, test, or admission code. A cold agent should not need to remember them.

1. **Packet-grade TikTok route posture.** The sanctioned packet-grade route should be explicit and hard to misuse: `--browser-backend cloakbrowser` for TikTok live capture unless a diagnostic path is deliberately selected. `--browser-channel` must remain incompatible with CloakBrowser.
2. **Session provenance gate.** A sessioned run that requests posture must validate local auth-state sidecar provenance before browser launch. A label containing `noproxy` never clears the gate by itself.
3. **Harness proxy-posture vocabulary.** Code may require `no_proxy_profile_loaded` or `proxy_profile_loaded`; it must not expose that as full-network no-proxy proof.
4. **Secret scan.** Sidecars, packets, staging, receipts, docs, and admission payloads must reject raw cookies, storage-state contents, tokens, proxy endpoints, exit IPs, profile paths, device identifiers, and raw signed URLs.
5. **Benign overlay setup.** TikTok onboarding, teaching, `OK`, `Got it`, app, cookie, or continue-in-browser prompts without challenge/security markers are setup actions through named pointer actions, not terminal blockers.
6. **Visible retry setup.** `Retry`, `Retry again`, `Try again`, or `Reload` controls should be clicked once through a named pointer action before classifying failure.
7. **Comment route zero-yield.** `no_challenge_but_no_comments` is not terminal until the full comments -> `You may like` / `More like this` -> comments route has run, including the bounded second route pass when configured.
8. **Challenge breakdown.** `platform_challenge_observed` must break down into marker, kind, and receipt fields. Slider/captcha/security/auth-wall should not collapse into one undifferentiated stop string.
9. **X-able challenge follow-through.** When follow-through is authorized, code clicks only the modal X/Close through the named pointer-action substrate. It never drags or solves a puzzle.
10. **Close acceptance gate.** `clicked=true` means pointer delivery only. Admission requires close acceptance plus no final challenge/security triage marker. Failed close means zero admission even if comment traffic appears.
11. **Owner-attention state.** If a slider/captcha remains and manual solve is the only possible continuation, the runner should produce an owner-attention state or prompt when possible. If owner-attention/prompting is not available, it must fail closed with a typed reason rather than solving or pretending capture success.
12. **Human handoff receipt boundary.** Any owner/manual intervention is source-access intervention in receipts. It is not clean capture and must not silently satisfy clean-route assertions.
13. **Admission chaining.** Cold agents should use runner-owned `--admit-output` or explicit `--data-root` only. Hand-copying staging JSON into packets should remain out of the path.
14. **Admission fail-closed contract.** Nonzero challenge count, failures, first-failure reason, diagnostic close, challenge-close-as-success, captcha-solving markers, forbidden secret material, or missing source provenance when required must reject before packet/lake write.
15. **Subtitle/transcript capture.** Source-native captions should be captured only through explicit allowlisted subtitle hosts and sanitized WebVTT/cue payloads. Unsupported hosts should stop or mark a typed non-capture reason; raw signed subtitle URLs/bodies must not persist.
16. **Receipt inspectability.** The runner should preserve enough sanitized fields for a cold agent to classify: blocker class, matched marker, challenge kind, retry/benign/comment action chronology, close attempts, close accepted/not accepted, owner-attention state, admitted response count, DOM fallback count, subtitle status, provenance requirement status.

## Doctrine-Only Findings

These remain prose because they explain intent, risk, or interpretation rather than a deterministic runtime decision.

1. **Dedicated-account risk posture.** TikTok sessioned capture uses dedicated non-personal accounts and accepts burnable-account risk for that lane. The goal doc does not repeat human-login-only mechanics; agents already must not enter credentials.
2. **No full-network no-proxy claim.** `no_proxy_profile_loaded` means the harness did not load a proxy profile. It does not prove OS, VPN, corporate, ISP, or upstream egress state.
3. **Owner-attention preference.** If manual CAPTCHA/slider action becomes the only continuation, ping/hand off to the owner when possible; if not possible, fail closed. This is not permission to automate solving.
4. **Chrome connector boundary.** Owner Chrome may help observe UI and login state, but it is not packet-grade unless it can produce the same durable sanitized response receipts and no-secret guarantees.
5. **Playwright diagnostic boundary.** Playwright/Chrome can be used for explicit diagnostics, but it should not be the default TikTok capture route while CloakBrowser is the pinned working surface.
6. **Manual intervention interpretation.** Owner/manual solve can support source-access diagnosis or a clearly labeled intervention receipt; it is not unchallenged clean capture.
7. **One probe is not scale.** One successful fixture does not prove cross-creator durability, account safety, platform stability, or promotion readiness.
8. **Transcript interpretation.** TikTok subtitles are source-native subtitle evidence when present; not owner-generated ASR and not platform-wide transcript coverage.
9. **Bronze caution.** Prefer local `--admit-output` before data-lake `--data-root` unless the owner explicitly wants immediate bronze.

## Implementation Batches

Batches are intentionally materially large enough to reduce repeated cold-agent failures, but small enough to validate and review.

### BATCH-01 - Runner Posture, Provenance Preflight, And Owner-Attention Skeleton

Purpose: make the runner hard to invoke in the wrong TikTok capture posture and make pre-browser failures explicit.

Code scope:

- `orca-harness/runners/run_source_capture_tiktok_live_batch_probe.py`
- `orca-harness/source_capture/tiktok/live_batch_probe.py`
- `orca-harness/source_capture/source_access_provenance.py` only if needed for exported helper messages
- focused tests in `orca-harness/tests/unit/test_tiktok_live_batch_probe.py` and `orca-harness/tests/unit/test_source_capture_authenticated_browser_snapshot.py`

Expected behavior:

- Add a TikTok packet-grade/cold-agent preset or equivalent CLI guard that makes `cloakbrowser` the explicit sanctioned route for non-diagnostic capture.
- Keep a diagnostic route possible, but require explicit diagnostic intent when using non-CloakBrowser backend for TikTok.
- Preflight `--require-harness-proxy-posture` before browser launch and surface a typed, cold-readable reason for missing/legacy/mismatched provenance.
- Add an `owner_attention_required` / `manual_challenge_attention_required` state shape for remaining slider/captcha when owner handoff is needed. If prompting is unavailable or not enabled, fail closed with this reason.
- Preserve current no-solve/no-drag behavior and no-secret sidecar rules.

Validation target:

- Unit tests that non-CloakBrowser packet-grade invocation is rejected or explicitly diagnostic.
- Unit tests that required harness proxy posture rejects before browser launch on legacy/missing/mismatched sidecar.
- Unit tests that owner-attention state is emitted/handled without classifying as clean capture.
- Existing provenance and live-runner tests remain green.

### BATCH-02 - Blocker State Machine And Low-Latency Setup Actions

Purpose: move the known cold-agent blocker taxonomy from memory/prose into deterministic triage and action sequencing.

Code scope:

- `orca-harness/source_capture/tiktok/blocker_triage.py`
- `orca-harness/source_capture/tiktok/live_batch_probe.py`
- pointer-action configs/tests in `orca-harness/source_capture/adapters/browser_snapshot.py` only if missing
- focused tests in `orca-harness/tests/unit/test_tiktok_live_batch_probe.py`, `orca-harness/tests/unit/test_source_capture_browser_snapshot.py`, and blocker-triage tests

Expected behavior:

- Benign onboarding/teaching/OK/Got-it overlays trigger setup action, not terminal blocker.
- Visible Retry/Try again/Reload controls trigger exactly one setup retry action before failure.
- Comment route zero-yield requires the full bounded comment-tab route and repeat before terminal classification.
- Challenge classifier emits marker and `challenge_kind` instead of only `platform_challenge_observed`.
- X-able slider challenge attempts X/Close when authorized; failed close remains typed zero-admission stop.

Validation target:

- Fixture tests for each blocker class and action sequence.
- Receipt tests proving `pointer_action_chronology` contains setup actions and `comment_action` remains filtered to comment-route actions.
- Regression tests for `challenge_close_not_accepted` with zero admission.

### BATCH-03 - Admission, Receipt, And Transcript Enforcement

Purpose: make optional packet/bronze output reliable and ensure comments/subtitles are either admitted safely or rejected with typed reasons.

Code scope:

- `orca-harness/source_capture/tiktok/batch_packet.py`
- `orca-harness/source_capture/tiktok/admission.py`
- `orca-harness/source_capture/tiktok/live_batch_probe.py`
- live runner admission chain
- tests for TikTok batch admission and live batch probe

Expected behavior:

- Admission rejects all challenge/failure/diagnostic/owner-manual-clean-claim violations before writing.
- Source-native subtitle allowlist and sanitized WebVTT/cue capture are explicit and tested.
- Unsupported subtitle host emits typed non-capture reason; raw signed URL/body never persists.
- Staging-to-packet receipts carry enough sanitized provenance to explain why a row did or did not admit.

Validation target:

- Batch admission rejection tests for every fail-closed marker.
- Subtitle allowlist tests and no-raw-url/no-raw-body tests.
- Local `--admit-output` success-path test for comment + subtitle-bearing fixture.

### BATCH-04 - Cold-Agent Command Surface And Probe Receipts

Purpose: make the operator-facing route simple enough that cold agents run the right command and stop after the right receipt.

Code/docs scope:

- runner `--help`
- `orca-harness/README.md`
- `orca-harness/docs/source_capture_agent_runbook.md`
- `docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md`
- optional new receipt template/checker if needed

Expected behavior:

- The recommended one-fixture sessioned command is copyable and uses the code-enforced defaults/gates.
- The runner prints typed result summaries that distinguish staging, local admit-output, bronze data-root, owner-attention, and fail-closed.
- Docs remove stale ambiguity but do not claim validation, scale, or full-network no-proxy.

Validation target:

- `--help` snapshot/behavior tests where practical.
- DCP/header/handoff pointer gates if docs change.
- One post-batch review prompt after BATCH-01..03 are implemented or when a bound review gate requires it.

## First Batch Assumption-Gate Target

Accepted direction for first gate: **BATCH-01 - Runner Posture, Provenance Preflight, And Owner-Attention Skeleton**.

Load-bearing assumptions to verify before implementation:

1. Current tests can exercise runner pre-browser exits without launching a real browser.
2. The live runner has a clean place to reject wrong backend/posture before calling `write_tiktok_live_batch_probe_outputs`.
3. Existing sidecar validators expose enough typed failure signals to distinguish missing/legacy/mismatch without printing secret-adjacent payloads.

If these are verified, BATCH-01 is the right first fused target. If not, route to a smaller preflight-only patch or a spec slice before implementation.

## Non-Claims

- This document is not validation, readiness, merge approval, PR acceptance, live capture success, or implementation completion.
- This document does not authorize CAPTCHA/slider solving or secret inspection.
- This document does not prove TikTok source access, account safety, subtitle coverage, bronze correctness, or scale.
- The batches are implementation targets; each still needs source reads, tests, and review routing under the Orca overlay.
