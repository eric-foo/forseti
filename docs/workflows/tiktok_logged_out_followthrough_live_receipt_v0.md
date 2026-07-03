# TikTok Logged-Out Follow-Through Live Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow receipt
scope: >
  Sanitized receipt for the 2026-07-03 logged-out TikTok Funmi Monet follow-through
  live probe after the source-access/admission doctrine changed to allow
  owner-authorized X/Close follow-through.
use_when:
  - Checking whether the TikTok X/Close follow-through path was actually run.
  - Deciding whether logged-out TikTok comment capture can expand past the Funmi
    fixture.
  - Preventing future lanes from re-diagnosing closeability instead of using the
    follow-through playbook.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md
  - docs/workflows/tiktok_live_microbatch_owner_gated_handoff_v0.md
  - orca-harness/source_capture/tiktok/live_batch_probe.py
  - orca-harness/source_capture/tiktok/batch_packet.py
stale_if:
  - The live scratch receipt path is deleted or superseded by a later live run.
  - TikTok changes the logged-out challenge/comment UI.
  - The source-access boundary or TikTok follow-through doctrine changes again.
```

## Receipt

- run_type: `logged_out_public_tiktok_followthrough_live_probe`
- target_creator: `funmimonet`
- target_profile_url: `https://www.tiktok.com/@funmimonet`
- target_video_url: `https://www.tiktok.com/@funmimonet/video/7629774409762442526`
- output_dir: `orca-harness\_scratch\tiktok_followthrough_20260703_04\funmimonet_7629774409762442526`
- cadence_receipt: `orca-harness\_scratch\tiktok_followthrough_20260703_04\funmimonet_7629774409762442526\tiktok_live_cadence_result.json`
- grid_receipt: `orca-harness\_scratch\tiktok_followthrough_20260703_04\funmimonet_7629774409762442526\tiktok_live_grid_result.json`
- observed_utc: `2026-07-03T09:55:09Z`
- run_complete_utc: `2026-07-03T09:55:30Z`

The runner used `--logged-out`, `--allow-challenge-close-followthrough`,
`--wait-until networkidle`, `--settle-seconds 8`, and no auth storage state.

Observed outcome:

- `attempted_count=1`
- `completed_count=0`
- `challenge_count=1`
- `challenge_close_followthrough_allowed=true`
- `challenge_close_counts_as_success=false`
- `reason=platform_challenge_observed_after_close_followthrough`
- no row was admitted and `response_items=[]`

The X/Close follow-through did run. The sanitized action receipt recorded:

- `action_name=tiktok_challenge_modal_visual_close_followthrough_pointer_v0`
- `target_kind=visual_x`
- `target_found=true`
- `clicked=true`
- `selection_strategy=top_right_visual_x`
- `visual_fallback_confidence=0.933`
- `visual_fallback_candidate_count=3`
- `visual_fallback_screenshot_sha256=e234672a86f921786f5bc9fafd1cbc6abbbb2271386bd08be8546fafd90b02fa`
- `visual_fallback_crop_box={"x":576,"y":0,"width":704,"height":251}`

Receipt limitation: this historical run was recorded before the pointer-action
receipt retained `target_box` and `click_point`, so it proves the visual-X
substrate path reported a page-level click but does not preserve the exact
viewport coordinate. Current runner receipts now retain those sanitized geometry
fields for future audits, without retaining screenshot bodies or raw DOM.

The blocker remained after the click:

- `blocker_class=challenge_or_security`
- `matched_marker=drag the slider`
- `hydration_present=true`
- `challenge_close_followthrough=true`

## Interpretation

This is not another closeability diagnostic: the script clicked the visual X.
The logged-out limit on this Funmi target is that the challenge marker remained
after the owner-authorized close follow-through, so the admission gate correctly
stopped before comment capture or creator expansion.

No raw comment bodies, raw endpoint URLs, cookies/tokens, auth state, raw DOM
body, or screenshot image were persisted by this receipt. DOM-derived sanitized
metadata was preserved: hydration presence, matched challenge marker, and the
bounded pointer-action receipt.

## Non-Claims

- not successful comment capture
- not creator expansion evidence
- not cross-creator ceiling evidence
- not product/Judgment extraction
- not raw DOM preservation
- not raw comment-body preservation
- not authorization to drag or solve CAPTCHA/slider challenges

## 2026-07-03 Acceptance-Proof Rerun

A follow-up logged-out live probe was run against the same Funmi fixture after
post-click proof fields were added:

- output_dir: `orca-harness\_scratch\tiktok_x_close_acceptance_probe_20260703_01\funmimonet_7629774409762442526`
- observed_utc: `2026-07-03T12:17:37Z`
- run_complete_utc: `2026-07-03T12:17:57Z`
- flags: `--logged-out`, `--allow-challenge-close-followthrough`, `--wait-until networkidle`, `--settle-seconds 8`, `--browser-channel chrome`
- outcome: `attempted_count=1`, `completed_count=0`, `challenge_count=1`, `results=[]`
- stop_reason: `platform_challenge_observed_after_close_followthrough`

The runner did press the centered modal X:

- `action_name=tiktok_challenge_modal_visual_close_followthrough_pointer_v0`
- `target_kind=visual_x`
- `selection_strategy=center_modal_visual_x`
- `target_found=true`
- `clicked=true`
- `target_box={"x":792.32,"y":187.2,"width":23.04,"height":21.6}`
- `click_point={"x":800.706,"y":200.024}`
- `post_click_absence_verified=true`
- `post_click_visual_target_absent=true` (historical weak check; current code requires `post_click_visual_candidate_count=0`)
- `post_click_visual_candidate_count=4`

However, the final blocker triage still reported
`matched_marker=drag the slider`. That means this rerun proves pointer delivery
to the intended X, but it does not prove the modal closed or that TikTok accepted
the close. The scratch receipt itself was written before the follow-up code patches
and contains historical overclaims: `challenge_close_accepted=true` and
`post_click_visual_target_absent=true` despite remaining post-click visual-X
candidates. Current code now fails this state closed: if post-click visual-X
candidates remain or final triage still sees challenge/security text,
`challenge_close_accepted=false` and no completed capture row can be admitted.

The same receipt observed `matched_comment_response_count=1` and
`dom_visible_comment_candidate_count=1`, but those are post-challenge diagnostic
signals only because final triage still saw the slider marker. They were not
admitted as a capture row. A forbidden-marker scan over the output directory had
only the expected contract strings `cookies_or_tokens_persisted=false`; no raw
cookie/token/signed-URL marker was observed.

## 2026-07-03 Sequence-Gated Follow-Through Rerun

A later visible logged-out probe was run after the pointer-sequence gate and
receipt-label fixes:

- output_dir: `orca-harness\_scratch\tiktok_observe_one_sequence_gate_20260703_03\funmimonet_7629774409762442526`
- observed_utc: `2026-07-03T12:58:49Z`
- run_complete_utc: `2026-07-03T12:59:08Z`
- outcome: `attempted_count=1`, `completed_count=0`, `challenge_count=1`, `results=[]`
- stop_reason: `challenge_x_click_attempted_close_not_accepted`
- `challenge_close_action.action_name=tiktok_challenge_modal_visual_close_followthrough_pointer_v0`
- `challenge_close_action.clicked=true`
- `challenge_close_action.click_point={"x":800.706,"y":200.024}`
- `challenge_close_action.post_click_visual_candidate_count=3`
- `challenge_close_action.post_click_visual_target_absent=false`
- `challenge_close_accepted=false`
- `matched_comment_response_count=0`
- `admitted_comment_response_count=0`

This is the current receipt shape future runs should expect when TikTok does not
accept the X close: the visual X click is recorded, the remaining visual-X
candidates fail close acceptance, no `challenge_close_followthrough=true` field is
carried, and the stopped close action is not mislabeled as `comment_action`.
