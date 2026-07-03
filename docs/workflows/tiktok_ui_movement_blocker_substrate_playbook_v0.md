# TikTok UI Movement Blocker Substrate Playbook v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow playbook
scope: >
  Cold-agent map for using Orca's bounded browser pointer-action substrate on
  TikTok logged-out and live-run UI blockers without converting challenge
  interaction into capture success.
use_when:
  - A TikTok logged-out limit-mapping lane needs to dismiss benign overlays
    while measuring public creator/video/comment access limits.
  - A TikTok live/sessioned lane hits benign overlays, comment-surface routing
    misses, slider/captcha close diagnostics, or visually present controls that
    are not exposed as DOM buttons.
  - A cold agent needs to know which UI movement action is allowed for each
    blocker class before running or patching the live probe.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/safety-rules.md
  - docs/workflows/tiktok_live_microbatch_owner_gated_handoff_v0.md
  - orca-harness/source_capture/adapters/browser_snapshot.py
  - orca-harness/source_capture/tiktok/live_batch_probe.py
  - orca-harness/source_capture/tiktok/blocker_triage.py
  - orca-harness/tests/unit/test_source_capture_browser_snapshot.py
  - orca-harness/tests/unit/test_tiktok_live_batch_probe.py
stale_if:
  - `BrowserPagePointerAction`, `_run_pointer_action`, or the visual-X fallback changes materially.
  - `live_batch_probe.py` action names, ordering, stop semantics, or CLI flags change materially.
  - TikTok blocker-triage challenge/auth-wall policy changes materially.
```

## Core Rule

Use the shared pointer-action substrate for TikTok UI movement. Do not hand-roll
ad hoc Playwright clicks in a live lane unless the substrate itself is missing a
needed bounded capability and the patch adds tests plus a receipt.

Known-closeability diagnostics are not useful work once pinned. The 2026-07-03
TikTok slider/challenge X was already proven repeatedly closeable by the
visual-X substrate; future lanes must not spend run budget re-proving that fact
unless a material condition changed, such as account/session posture, browser
context, route opener, target video/creator, or TikTok UI state. A closeable
slider/captcha X is still a challenge/security blocker for admissible capture:
do not use the close click to manufacture a completed row, admission, expansion,
or success claim.

The substrate is:

- `BrowserPagePointerAction` in `orca-harness/source_capture/adapters/browser_snapshot.py`.
- `_run_pointer_action(...)` in the same file.
- Movement execution via `page.mouse.move(..., steps=...)` followed by
  `page.mouse.click(...)`, with randomized bounded target fractions and step
  counts from the action config.
- Sanitized receipts under `metadata.post_load_pointer_actions`; receipts must
  not include raw cookie/storage contents, raw endpoint URLs, or raw response
  bodies.

## Blocker Map

| Blocker / UI state | Action substrate | Allowed in clean run? | Success semantics |
| --- | --- | --- | --- |
| Benign TikTok onboarding/app prompt such as `Got it`, `Not now`, `Continue in browser` | `tiktok_dismiss_benign_overlay_pointer_v0` | Yes | Setup action only; excluded from comment-action count. |
| Logged-out login upsell modal with a dismiss/close control and no challenge/security text | `tiktok_dismiss_benign_overlay_pointer_v0` or a named logged-out dismiss action if added later | Yes for logged-out limit mapping only | Setup action only; record the receipt and continue measuring public access. Do not enter credentials. |
| Comment surface does not load comments until tab shuffle | `comment_surface_toggle_pointer_sequence_v0`: `tiktok_open_comments_pointer_v0` -> `tiktok_open_more_like_this_pointer_v0` -> `tiktok_reopen_comments_pointer_v0` | Yes | Clean only if at least one page-owned `/api/comment/list` response is admitted. Zero response is stop/diagnosis. |
| DOM-exposed slider/captcha close control | `tiktok_challenge_modal_close_diagnostic_pointer_v0` | No for admissible capture; only with `--allow-challenge-close-diagnostic` | Diagnostic only. Closeability is already pinned; do not re-run only to prove it. If clicked, force stop as challenge-close diagnosis. |
| Screenshot-visible but DOM-invisible slider/captcha X | `tiktok_challenge_modal_visual_close_diagnostic_pointer_v0` | No for admissible capture; only with `--allow-challenge-close-diagnostic` and visible challenge text | Diagnostic only. Closeability is already pinned; do not re-run only to prove it. If clicked, force stop as challenge-close diagnosis. |
| Slider/captcha puzzle itself | None | Never | Do not drag, solve, or attempt puzzle interaction. |
| Login/auth wall redirect, credential prompt, or account risk wall | None unless separately mapped as benign logged-out upsell | Never by default | Stop and report blocker. Do not enter credentials or manipulate account state. |
| Unknown dismiss/reload blocker | None until mapped | No | Stop or patch a named substrate action with tests; do not generic-click around blockers. |

## Logged-Out Limit-Mapping Mode

Logged-out runs are allowed to measure TikTok's public creator/video/comment
surface limits before any sessioned retry. They must use the same pointer-action
substrate and receipts.

Allowed logged-out movement:

- dismiss benign onboarding, app, cookie, continue-in-browser, and login-upsell
  overlays when they expose a close/dismiss control and no challenge/security
  marker;
- open comments through the named comment-surface route action;
- capture public stats and comment bodies only through the armory runner/output
  path chosen for the lane, without pagination unless the current owner
  explicitly authorizes it.

Not allowed in logged-out capture:

- dragging, solving, or interacting with slider/captcha puzzles;
- treating a slider/captcha X click as capture success;
- entering credentials, preserving auth state, or upgrading to a sessioned run
  without a fresh owner gate;
- repeating closeability diagnostics after the same challenge/security X has
  already been pinned.

If a logged-out run hits a closeable login upsell, dismiss once and continue. If
it hits a slider/captcha/security challenge, stop and record the pinned blocker
state; do not run a close diagnostic unless the lane objective is explicitly to
check a changed blocker condition.

## Cold-Agent Procedure

1. Load the active handoff and this playbook. Re-read the current
   `browser_snapshot.py`, `live_batch_probe.py`, and `blocker_triage.py` before
   making strict claims.
2. Select mode before browser action:
   - logged-out limit mapping: no auth state, no credential entry, benign
     dismissals allowed, challenge/security stops;
   - live/sessioned gate: dedicated non-personal warmed account,
     human-performed login, authorized auth-state label/session mode, no
     duplicate TikTok tabs, and owner authorization for the live run.
3. For a clean route-yield gate, run without `--allow-challenge-close-diagnostic`.
   The runner may dismiss benign overlays and perform the comments -> More like
   this -> comments sequence.
4. Continue only if the first video has `completed_count=1`, `challenge_count=0`,
   no failures, and `admitted_comment_response_count >= 1`.
5. If the owner explicitly authorizes challenge-close diagnosis, run with
   `--allow-challenge-close-diagnostic`. A DOM close click or visual-X close click
   must stop the run and must not admit, expand, or claim capture success.
   The visual-X diagnostic is challenge-text gated; it is not a generic
   upper-right screenshot clicker.
6. Scan outputs for forbidden markers before any admission claim. Auth-state files
   copied for a live run must be removed and verified absent after the run.
   Batch admission is code-gated to reject challenge/diagnostic cadence: nonzero
   `challenge_count`, non-empty `failures`, `first_failure_reason`,
   `captcha_solving=true`, `challenge_close_counts_as_success=true`, or
   `challenge_close_diagnostic_allowed=true` cannot be admitted.

## Receipt Fields To Inspect

For benign overlay:

- `capture_receipt.benign_overlay_action.action_name`
- `target_found`, `clicked`, `candidate_count`, `matched_count`, `wait_ms`

For comment routing:

- `capture_receipt.comment_action.sequence_name`
- `action_count`
- `action_sequence[*].action_name`
- `clicked_all_targets`
- `admitted_comment_response_count`

For challenge-close diagnostics:

- `blocker_triage.challenge_close_diagnostic.action_name`
- `target_found`, `clicked`, `target_kind`, `selection_strategy`
- visual-only fields: `visual_fallback_attempted`,
  `visual_fallback_target_found`, `visual_fallback_candidate_count`,
  `visual_fallback_confidence`, `visual_fallback_crop_box`,
  `visual_fallback_screenshot_sha256`

A clicked challenge-close diagnostic receipt is evidence that the close control
was reachable. It is not evidence that TikTok capture succeeded. For the current
TikTok slider/challenge X, closeability is already proven and should be treated
as a pinned blocker fact, not a default next action.

## Patch Rule For New Blockers

If a new blocker needs UI movement:

1. Add a named `BrowserPagePointerAction` config, not an inline click.
2. Gate it by visible page text or by an explicit diagnostic flag when it touches
   challenge/auth-risk UI.
3. Preserve sanitized receipt fields that explain what was attempted and why.
4. Add unit tests in `test_source_capture_browser_snapshot.py` for substrate
   behavior and `test_tiktok_live_batch_probe.py` for TikTok ordering/stop
   semantics.
5. Update this playbook and the active handoff.

Never add a path where closing or dismissing a challenge can produce a completed
capture row, admission, batch expansion, product extraction, or success claim.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    TikTok lanes must stop repeating already-pinned slider/challenge X
    closeability diagnostics, while logged-out limit-mapping runs may dismiss
    benign overlays and login upsells that expose a close control and no
    challenge/security marker.
  trigger: workflow_authority
  controlling_sources_updated:
    - docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md
  downstream_surfaces_checked:
    - docs/workflows/tiktok_live_microbatch_owner_gated_handoff_v0.md
    - docs/workflows/tiktok_live_microbatch_gate_repair_fresh_thread_handoff_v0.md
    - .agents/workflow-overlay/safety-rules.md
  intentionally_not_updated:
    - path: docs/workflows/tiktok_live_microbatch_owner_gated_handoff_v0.md
      reason: >
        Already states the visual-X closeability recurrence and diagnostic-only
        semantics; the new logged-out limit-mapping mode belongs in this
        substrate playbook.
    - path: docs/workflows/tiktok_live_microbatch_gate_repair_fresh_thread_handoff_v0.md
      reason: >
        It is a completed PR #608 landing handoff and already says
        challenge-close diagnostics are never capture success.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        The external source-data capture rule already routes captures through
        the Source Capture Armory Runner Ladder; this playbook only narrows
        TikTok UI movement behavior.
  stale_language_search: >
    rg -n "challenge-close|visual-X|allow-challenge-close-diagnostic|logged-out|login upsell|closeability"
    docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md
    docs/workflows/tiktok_live_microbatch_owner_gated_handoff_v0.md
    docs/workflows/tiktok_live_microbatch_gate_repair_fresh_thread_handoff_v0.md
  non_claims:
    - not validation
    - not readiness
    - not capture success
    - not authorization to solve or bypass CAPTCHA/slider challenges
```

Older receipts for this file live verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
