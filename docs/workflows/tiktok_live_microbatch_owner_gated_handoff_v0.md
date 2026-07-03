# TikTok Live Microbatch Owner-Gated Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow handoff
scope: >
  Cold-lane handoff for the owner-gated TikTok live smoke/micro-batch after the
  bounded pointer-action and blocker-triage patches landed on main.
use_when:
  - Transferring the next TikTok live micro-batch run to a fresh agent or lane.
  - Verifying prerequisites before running the headed/sessioned TikTok live probe.
  - Preserving stop-on-challenge, no-CAPTCHA-solving, and sanitized-admission boundaries.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_sessioned_capture_warm_probe_plan_v0.md
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_first_slice_probe_recon_v0.md
  - docs/workflows/tiktok_public_route_live_diagnostic_receipt_v0.md
  - docs/workflows/tiktok_behavioral_sync_fresh_lane_handoff_v0.md
  - docs/workflows/tiktok_comment_response_capture_pr559_adjudication_handoff_v0.md
  - docs/workflows/tiktok_funmi_n30_comment_subtitle_cadence_analysis_v0.md
  - docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md
  - orca-harness/source_capture/adapters/browser_snapshot.py
  - orca-harness/source_capture/tiktok/live_batch_probe.py
  - orca-harness/source_capture/tiktok/blocker_triage.py
  - orca-harness/source_capture/tiktok/batch_packet.py
  - orca-harness/source_capture/tiktok/admission.py
  - orca-harness/runners/run_source_capture_tiktok_live_batch_probe.py
  - orca-harness/runners/run_source_capture_tiktok_batch_packet.py
branch_or_commit: codex/tiktok-live-microbatch-gate-repair
input_hashes:
  AGENTS.md: c28077faf75c83b80800beda7508ae7a6d95a411
  .agents/workflow-overlay/README.md: 57cbc892dcd79d4d57686db465900ad042769174
  .agents/workflow-overlay/source-loading.md: 29c8c3211299aff22837ef9981e5865f3c15c222
  orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md: f7f5819a3b7091458438b7b84b820445174196f3
  orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_sessioned_capture_warm_probe_plan_v0.md: 977628f964461970a41c8aa243503acce16db048
  orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_first_slice_probe_recon_v0.md: 8ae31ac55067f2ec175f6baa6867939704cf7078
  docs/workflows/tiktok_public_route_live_diagnostic_receipt_v0.md: a0ca160b4a984a2d6e2f0d191a2deea8d6844a2b
  docs/workflows/tiktok_behavioral_sync_fresh_lane_handoff_v0.md: 0fcda55434efb97791c495e112e7682f9cc1b42d
  docs/workflows/tiktok_comment_response_capture_pr559_adjudication_handoff_v0.md: 5a814dad39d79222ea78631e395ff382d4fc7396
  docs/workflows/tiktok_funmi_n30_comment_subtitle_cadence_analysis_v0.md: 8385e43615e76a2503e9f36468dbdcd7c92268a3
  docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md: c9c7f561c1d121bf4a2cb259f4fb4ac5971d81db
  orca-harness/source_capture/adapters/browser_snapshot.py: c69014f5fb4eb21901c3770b6eb8a058ebd1b65c
  orca-harness/source_capture/tiktok/live_batch_probe.py: 15fb5239c33da41ee4946d6b4e5d1c9b126a0c9e
  orca-harness/source_capture/tiktok/blocker_triage.py: 19816ad967bc57c53aa750dfc9cf59902e5455cd
  orca-harness/source_capture/tiktok/batch_packet.py: 97e3db09f1f895a2a758ea6b9f58fbe1b0580053
  orca-harness/source_capture/tiktok/admission.py: 45a86b554772a58300b23be077a48b32f8dcd8de
  orca-harness/runners/run_source_capture_tiktok_live_batch_probe.py: 9551ced836e3c2699b68bc7356d05b8b8b569093
  orca-harness/runners/run_source_capture_tiktok_batch_packet.py: 856b76df0be96b47040486260b52a427444072d9
stale_if:
  - PR #583 is reverted or the TikTok blocker-triage/live-probe stop behavior is superseded.
  - `browser_snapshot.py`, `live_batch_probe.py`, `blocker_triage.py`, `batch_packet.py`, `admission.py`, or the live runner CLI changes materially.
  - The TikTok behavioral-sync handoff, PR #559 handoff, or Funmi N30 receipt changes materially.
  - The TikTok capture lane spec or sessioned warm-probe plan changes materially.
  - The owner changes live-run account-risk posture, session posture, or no-CAPTCHA-solving policy.
```

## Confirm-Don't-Trust Load Contract

This packet is a handoff, not authority. If the receiver has repo/filesystem
access, open this packet and re-read the `open_next` sources before making strict
or actionable claims. At minimum, re-check the current branch/HEAD, the live
runner CLI help, the TikTok C6/C8' stop-on-challenge account posture, and the
batch-admission sanitization path. If the receiver does not have repo/filesystem
access, stop and request a pasted source capsule or a no-repo handoff before
running or recommending any live TikTok action.

Do not trust this packet's hashes after `stale_if` fires. Use them as compare
targets only.

## Goal Handoff

```yaml
long_term_goal: >
  Make the TikTok source-capture lane produce sanitized, admissible live staging
  data under real sessioned conditions without violating stop-on-challenge or
  account-safety boundaries; page-owned comment responses remain response-tier,
  while DOM-visible comments are explicitly lower-tier fallback evidence.
anchor_goal: >
  Repair the live micro-batch gate so one known public video must prove either a
  real page-owned `/api/comment/list` response or bounded DOM-visible comment
  candidates before any cross-creator batch spends more account/session budget.
success_signal: >
  For the first attempted creator/video, produce a run receipt with attempted,
  completed, challenge, and failure counts; at least one admitted page-owned
  comment-list response or DOM-visible comment candidate; captured comment count;
  subtitle metadata yield; admission path if completed; and explicit
  no-secret/no-raw-URL/no-cookie confirmation. If both comment-list and DOM
  visible-comment yield are zero, stop as a diagnosis result and do not expand.
  No product-value or scale claim.
```

## Active Objective

Run a bounded, owner-gated TikTok live route-yield gate using the current
`run_source_capture_tiktok_live_batch_probe.py` runner: one known public video
first, sanitized staging, no challenge solving, and no expansion unless the first
video captures at least one real page-owned `/api/comment/list` response or
bounded DOM-visible comment candidates.

The prior micro-batch packet version was corrupted for execution: it allowed
continuation on sanitized staging plus admission alone. Treat the 2026-07-02
five-creator zero-response run as a diagnostic receipt, not capture success.

Current owner redirect for this lane: the prior stop-only challenge-X rule is
superseded for X-able public TikTok challenge modals. Use
`--allow-challenge-close-followthrough` when the owner authorizes a route-yield
run through a visible X/Close. The runner may attempt X/Close through the named
UI movement substrate, must never drag or solve the puzzle, and may continue only
if the close is accepted by post-click receipt checks: challenge/security text is
absent and the centered visual-X is absent on the after-click screenshot. A
`clicked=true` pointer receipt is not close proof. Continue only if accepted
close follow-through is proven and either a page-owned `/api/comment/list`
response or bounded DOM-visible comment candidates are captured after the named
comments -> `More like this` -> comments route. DOM-visible comments are lower-
tier `captured_visible_dom` evidence, not page-owned response evidence. Any
admitted row must preserve the accepted close action as a
`source_access_intervention`; it is post-close follow-through, not an
unchallenged clean route.
`--allow-challenge-close-diagnostic` remains stop-only for changed-condition
checks.

## Open Decision / Fork

The only live-run fork is whether to proceed past the first creator/video:

- Continue to a 3-5 creator micro-batch only if the first video has
  `challenge_count=0`, no empty/stripped shell, no auth wall, no unresolved
  blocker stop, no clicked diagnostic challenge-close receipt,
  `completed_count=1`, and either at least one admitted page-owned
  `/api/comment/list` response or at least one bounded DOM-visible comment
  candidate. If `challenge_close_followthrough_count > 0`, the result row and
  batch packet must carry the source-access intervention.
- Stop if both comment-list response yield and DOM-visible comment candidate
  yield are zero. Record it as `comment_list_response_absent` / route-opening
  diagnosis, not as a completed capture row and not as TikTok route failure in
  general.
- Stop if the first creator hits an unresolved challenge class: slider/captcha/
  verify text that remains after follow-through, login/auth wall, ban/40x on the
  authenticated session, empty/stripped shell, missing video-detail hydration, a
  clicked diagnostic challenge-close receipt, or an unresolved actual
  dismiss/reload blocker that the triage classifies as stop.
- Retry once only for transport/infra noise clearly distinguished from TikTok,
  such as extension/proxy chrome-error style failures already called out by the
  TikTok recon/spec. Do not convert repeated infra failures into a TikTok ceiling.
- Ask the owner if the dedicated account/session label, known public first-video
  URL, or live-network/browser permission is missing.

## Drift Guard

- Do not solve CAPTCHA/slider/verification challenges; no drag/solve path is
  authorized.
- Do not report an `X` or `Close` click by itself as success. The allowed capture
  path is the explicit owner-authorized
  `--allow-challenge-close-followthrough` route: attempt X/Close through the
  named UI movement substrate, require `challenge_close_accepted=true` from
  post-click text and visual-X absence checks, require at least one page-owned
  `/api/comment/list` response or bounded DOM-visible comment candidate, and
  preserve the accepted close action as a source-access intervention. Diagnostic
  close mode remains
  stop-only and cannot admit, expand, or count as a completed capture row.
- Do not use a personal TikTok account. This lane assumes a dedicated,
  burnable, warmed account with human-performed login.
- Do not enter credentials, inspect cookies/tokens, preserve storage-state paths,
  proxy endpoints, exit IPs, raw signed URLs, raw subtitle bodies, or raw response
  bodies.
- Do not run scale. This is a one-video route-yield gate first; a 3-5 creator
  micro-batch is allowed only after the first video captures at least one real
  page-owned `/api/comment/list` response or bounded DOM-visible comment
  candidates.
- Do not add product-mention extraction or product-value analysis. The owner
  deferred that as low value for this step.
- Do not forge TikTok signatures, call TikTok APIs directly, or replace the
  page-owned response-observation route with bare HTTP.
- Do not treat this handoff, a successful local test suite, or fake-engine
  coverage as a live-run proof.

## Inherited Context

Main now contains the bounded pointer-action and blocker-triage work that this
handoff depends on:

- The live probe opens comments via a typed pointer action (`tiktok_open_comments_pointer_v0`)
  rather than a page-JS `element.click()` path. In `live_batch_probe.py`, the
  pointer action uses bounded movement steps and a target-fraction range.
- The live probe writes local staging only: `tiktok_live_grid_result.json` and
  `tiktok_live_cadence_result.json`. Batch admission is a separate network-free
  step through `run_source_capture_tiktok_batch_packet.py`.
- `live_batch_probe.py` stops on textual challenge/auth-wall markers, missing
  video-detail hydration, and post-itemStruct blocker-triage `action=stop`.
- `blocker_triage.py` is classification-only. The live probe records triage
  receipts with `action_mode=classification_only` and `action_taken=false`.
- Text-only `Close` is not enough to stop after PR #583; actual dismiss candidate
  evidence without a benign marker remains an ambiguous stop condition.
- `batch_packet.py` preserves live-probe `url_present_but_redacted` as
  `url_redacted=true` in normalized subtitle info. This is metadata fidelity, not
  a raw URL persistence path.
- The behavioral-sync and Funmi N30 receipts are more specific than this packet
  for route-yield state: Funmi N30 measured `30/30` page-owned comment-list
  responses and `26/26` WebVTT parses when `subtitleInfos` existed, but this
  does not prove cross-creator coverage or this runner interaction path.
- The 2026-07-02 five-creator live run from the corrupted gate produced no
  challenges and sanitized admission artifacts, but zero comment responses. It is
  diagnostic evidence that the live runner interaction gate can silently miss
  the comment surface, not evidence of packet-grade cross-creator capture.
- A repaired one-video Funmi route-yield retry on 2026-07-02 stopped correctly
  with `attempted_count=1`, `completed_count=0`, `challenge_count=0`, and
  `comment_list_response_absent`. The pointer action found/clicked a matched
  role button (`candidate_count=48`, `matched_count=3`) but observed zero
  page-owned comment-list responses.
- Owner correction on 2026-07-03: the named route opener is
  `comment_surface_toggle_pointer_sequence_v0`: open comments, click the
  `More like this` tab, then return to comments. The sequence is bounded
  pointer movement only; it is not product extraction and not a challenge-close
  or solve path. The runner now performs that named bounded pointer sequence
  and records each action in sanitized metadata.
- The runner now prepends `tiktok_dismiss_benign_overlay_pointer_v0` before
  the comment-surface route. It is bounded-pointer dismissal for benign TikTok
  onboarding/app prompts such as `Got it`, `Not now`, or `Continue in browser`;
  it is not challenge-close behavior and is excluded from the comment-action
  sequence count.
- The pointer-action page-text gate now uses visible `innerText` rather than
  hidden `textContent`, so hidden TikTok strings such as `captcha` cannot by
  themselves satisfy a diagnostic pointer gate.
- The owner-authorized DOM follow-through close action is named
  `tiktok_challenge_modal_close_followthrough_pointer_v0`; the visual fallback
  action is named `tiktok_challenge_modal_visual_close_followthrough_pointer_v0`.
  They run only under `--allow-challenge-close-followthrough`; the DOM close
  action stays visible-challenge-text gated, while the visual-X follow-through
  action may run when TikTok exposes the challenge marker only as hidden/residual
  DOM text. They click only X/Close style controls and may admit only post-close
  page-owned comment responses or DOM-visible comment candidates with the close
  receipt preserved.
- The diagnostic close actions remain
  `tiktok_challenge_modal_close_diagnostic_pointer_v0` and
  `tiktok_challenge_modal_visual_close_diagnostic_pointer_v0`. They run only
  under `--allow-challenge-close-diagnostic` and remain blocker-diagnosis paths:
  any click forces stop semantics and cannot produce a capture row.
- Batch admission is now code-gated against non-clean live cadence. `batch_packet.py`
  rejects nonzero `challenge_count`, non-empty `failures`, `first_failure_reason`,
  `captcha_solving=true`, `challenge_close_counts_as_success=true`, and
  `challenge_close_diagnostic_allowed=true` before producing a packet.
- The first corrected live retry on 2026-07-03 used the comment-surface sequence
  on the Funmi video and stopped with `attempted_count=1`, `completed_count=0`,
  `challenge_count=1`, `reason=platform_challenge_observed`, and zero admitted
  comment-list responses. No admission, expansion, challenge solving,
  challenge-close click, or product extraction occurred.


## Exact Next Authorized Action

1. Verify repo state:

   ```powershell
   git status --short --branch
   git rev-parse HEAD
   git log --oneline -5
   ```

   Expected corrected baseline starts from `f58eccc8fff5a81939c9677d8cad8a4ad70bcbb7`
   plus the route-yield gate patch. If HEAD differs, re-read the changed sources
   and update this plan from the current code.

2. Verify live-run preconditions before any network/browser action:

   - explicit owner authorization for the live run in the current lane;
   - dedicated, non-personal, warmed TikTok account;
   - human-performed login already bootstrapped into an auth-state label;
   - session mode value matching the auth-state metadata;
   - no concurrent or duplicate TikTok tabs in that browser context;
   - one known public first-video URL for the route-yield gate;
   - local scratch output directory and admission output/data-root target.

   If any item is missing, stop and request it. Do not substitute a public logged
   out run for the sessioned route unless the owner explicitly redirects.

3. Re-check the live runner CLI from the receiver's environment:

   ```powershell
   $env:PYTHONPATH = "orca-harness"
   python orca-harness\runners\run_source_capture_tiktok_live_batch_probe.py --help
   python orca-harness\runners\run_source_capture_tiktok_batch_packet.py --help
   ```

   The observed live CLI requires `--creator-handle`, `--creator-profile-url`,
   repeated `--video-url`, `--state-label`, `--session-mode`, and `--output-dir`.
   It does not expose `--auth-state-root`; the default auth-state root is from
   `source_capture/auth_state.py` unless the code has changed.

4. If owner/human account-posture review reauthorizes another live retry, run
   exactly one known public video first, using current CLI help as source of
   truth. The current runner performs `comment_surface_toggle_pointer_sequence_v0`
   (comments -> `More like this` -> comments) internally. Shape:

   ```powershell
   $env:PYTHONPATH = "orca-harness"
   python orca-harness\runners\run_source_capture_tiktok_live_batch_probe.py `
     --creator-handle "<handle>" `
     --creator-profile-url "https://www.tiktok.com/@<handle>" `
     --video-url "<public-video-url-1>" `
     --state-label "<existing-auth-state-label>" `
     --session-mode "<mode-from-auth-state-metadata>" `
     --output-dir "<scratch-output-dir>\creator_01" `
     --browser-channel chrome
   ```

   Do not add flags that are not present in `--help`. Keep default cadence unless
   the owner explicitly directs a different small-N cadence. For the current
   owner-authorized X-able public challenge route-yield run, add
   `--allow-challenge-close-followthrough`. Use
   `--allow-challenge-close-diagnostic` only for stop-only changed-condition
   checks, never for admission or expansion.


5. Inspect the first-video outputs before admission or expansion:

   - `tiktok_live_grid_result.json`
   - `tiktok_live_cadence_result.json`

   Required to continue: `attempted_count=1`, `completed_count=1`,
    `challenge_count=0`, no failures, no clicked diagnostic challenge-close
    receipt, and
    either `results[0].capture_receipt.admitted_comment_response_count >= 1` or
    `results[0].capture_receipt.dom_visible_comment_candidate_count >= 1`. If
    `challenge_close_followthrough_count > 0`, verify
    `results[0].capture_receipt.challenge_close_accepted=true` and verify the row
    and batch packet preserve the accepted close action as
    `source_access_intervention`.

    If `challenge_count` is nonzero, failures contain a challenge/auth stop, a
    challenge remains after follow-through, or a diagnostic challenge-close
    action clicked, stop. Do not run admission.

   If both `admitted_comment_response_count` and
   `dom_visible_comment_candidate_count` are zero, stop and report
   `comment_list_response_absent` with the comment-action receipt. Do not admit
   it as success and do not run more creators.

   Scan the output directory for obvious forbidden markers before admission:

   ```powershell
   rg -n "msToken|X-Bogus|verifyFp|ttwid|sessionid|sid_guard|passport_csrf|cookie|tiktokcdn|byteoversea|tos-" "<scratch-output-dir>\creator_01"
   ```

   A match is not automatically a leak, but raw secrets, raw signed URLs, raw
   media/subtitle URLs, cookies, or storage-state paths block continuation.

6. Admit the first video's sanitized staging JSON through batch admission only if
   the route-yield gate passed:

   ```powershell
   $env:PYTHONPATH = "orca-harness"
   python orca-harness\runners\run_source_capture_tiktok_batch_packet.py `
     --creator-handle "<handle>" `
     --creator-profile-url "https://www.tiktok.com/@<handle>" `
     --grid-result-json "<scratch-output-dir>\creator_01\tiktok_live_grid_result.json" `
     --cadence-result-json "<scratch-output-dir>\creator_01\tiktok_live_cadence_result.json" `
     --output "<scratch-output-dir>\creator_01_admitted"
   ```

   Use `--data-root` only if the owner explicitly wants a data-lake write for the
   live run. Local `--output` is the lower-risk default unless redirected.

7. If and only if the first video captures at least one admitted page-owned
   comment-list response or DOM-visible comment candidate and admits cleanly, run
   the remaining 2-4 creators with the same small-N shape. Stop at the first real
   challenge class, unresolved blocker stop, or zero-comment/zero-DOM route
   diagnosis.

8. Produce a receipt with:

   - commit/branch and exact commands used;
   - creator count and video count attempted;
   - per-creator attempted/completed/challenge/failure counts;
   - first stop reason if any;
   - comment-list response success count/yield, DOM-visible comment candidate yield, and captured comment count;
   - subtitle metadata video count/yield, explicitly noting that this live runner
     defers subtitle body/WebVTT fetch;
   - admission success/failure path for each admitted output;
   - no-secret/no-raw-URL scan result;
   - non-claims: no scale proof, no account-safety-at-volume proof, no final
     product extraction, no Cleaning/ECR/Judgment.
## Source Ledger

Fresh-read sources used while writing this handoff:

- `AGENTS.md` supplied in-thread and compared at HEAD object
  `c28077faf75c83b80800beda7508ae7a6d95a411`.
- `.agents/workflow-overlay/README.md`: overlay front door and source ownership.
- `.agents/workflow-overlay/source-loading.md`: handoff and capture-spine
  source-loading rules, source capsules, and new-thread handoff triggers.
- `.agents/workflow-overlay/retrieval-metadata.md`: retrieval header field shape.
- `.agents/workflow-overlay/prompt-orchestration.md`: durable prompt/handoff
  preflight obligations.
- `tiktok_capture_lane_spec_v0.md`: C6 stop/cooldown, C8' sessioned account
  posture, implementation note for live probe/batch admission, and non-claims.
- `tiktok_sessioned_capture_warm_probe_plan_v0.md`: dedicated account,
  human login, no concurrent TikTok tabs, batch ladder concept, stop conditions,
  and per-run receipt requirements.
- `tiktok_first_slice_probe_recon_v0.md`: public/headless brittleness, real
  browser/session lesson, and no-CAPTCHA-solving boundary.
- `tiktok_public_route_live_diagnostic_receipt_v0.md`: public route hit slider
  challenge with visible `Close`; challenge was not solved or closed.
- `tiktok_behavioral_sync_fresh_lane_handoff_v0.md`: response-body route state,
  proven Funmi controls, and one-response proof before broader rung.
- `tiktok_comment_response_capture_pr559_adjudication_handoff_v0.md`: explicit
  one-video gate before any 3-5 creator expansion, and zero-response routing as
  a diagnosis target rather than success.
- `tiktok_funmi_n30_comment_subtitle_cadence_analysis_v0.md`: measured
  Funmi/session N30 result with `30/30` comment responses, 596 parsed comments,
  and `26/26` WebVTT success when subtitle metadata existed.
- `tiktok_ui_movement_blocker_substrate_playbook_v0.md`: cold-agent map from
  blocker class to allowed bounded pointer-action substrate, including benign
  overlays, comment-surface routing, DOM close diagnosis, visual-X diagnosis,
  and no-solve/no-success stop semantics.
- `browser_snapshot.py`: shared page-response observer, bounded pointer target script,
  and multi-action pointer-sequence metadata.
- `live_batch_probe.py`: local staging writer, stop hooks, TikTok
  comments/More-like-this/comments pointer-action sequence, zero-response stop,
  output names, and capture contract.
- `blocker_triage.py`: challenge/auth-wall stop, allow-list `matched_marker`
  receipts, missing itemStruct reload candidate classification, ambiguous dismiss
  stop, and classification-only model.
- `batch_packet.py` and `admission.py`: network-free sanitized batch admission,
  summary fields, and sensitive-material enforcement.
- Runner help for both TikTok live probe and batch admission CLIs.

## Current Task State

Corrected after the 2026-07-02 zero-response micro-batch diagnostic, the
one-video Funmi zero-yield retries, and the 2026-07-03 owner correction that
the route opener must use `comment_surface_toggle_pointer_sequence_v0`
(comments -> `More like this` -> comments). This handoff is not reusable as a
direct 3-5 creator execution packet until a
one-video route-yield gate captures at least one admitted page-owned
`/api/comment/list` response or bounded DOM-visible comment candidate under the
current runner and then admits cleanly.

Current live state after the visual-X diagnostic patch and two recurrence
probes: the latest 2026-07-03 one-video Funmi retries stopped as
`challenge_close_diagnostic_only`, each with `attempted_count=1`,
`completed_count=0`, `challenge_count=1`, empty `results`, no batch-admission
claim, and no expansion. In both recurrence probes, the selected diagnostic
receipt was `tiktok_challenge_modal_visual_close_diagnostic_pointer_v0` with
`target_found=true`, `clicked=true`, `target_kind=visual_x`,
`page_text_gate_matched=true`, `visual_fallback_candidate_count=1`,
`visual_fallback_confidence=0.721`, and crop
`{x:576,y:0,width:704,height:251}`. The screenshot hashes differed
(`9a466df6...` then `efdb3ebd...`), so this is recurring behavior rather than a
single cached receipt. Any page-owned comment-list response observed after the
challenge-close diagnostic click remains diagnostic only and cannot satisfy the
clean route-yield/admission gate. This proves a visual-X target can be found and
a pointer click can be delivered under the challenge-text gate; it does not prove
that TikTok accepted the close, because accepted close now requires post-click
text and visual-X absence proof.


## Changed / Inspected / Tested Files In This Handoff Lane

Changed:

- `docs/workflows/tiktok_live_microbatch_owner_gated_handoff_v0.md`
- `docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_sessioned_capture_warm_probe_plan_v0.md`
- `orca-harness/source_capture/adapters/browser_snapshot.py`
- `orca-harness/source_capture/tiktok/live_batch_probe.py`
- `orca-harness/source_capture/tiktok/batch_packet.py`
- `orca-harness/runners/run_source_capture_tiktok_live_batch_probe.py`
- `orca-harness/tests/unit/test_source_capture_browser_snapshot.py`
- `orca-harness/tests/unit/test_tiktok_live_batch_probe.py`

Inspected:

- All files in `open_next` needed for this live route-yield gate and stop-state
  repair.

Validation completed:

- `PYTHONPATH=orca-harness python -m pytest -q orca-harness/tests/unit/test_source_capture_browser_snapshot.py orca-harness/tests/unit/test_tiktok_blocker_triage.py orca-harness/tests/unit/test_tiktok_live_batch_probe.py orca-harness/tests/unit/test_tiktok_batch_admission.py`
  -> exit 0 with 70 targeted tests passing.
- Three owner-authorized diagnostic live retries after the visual-X patch using
  auth-state label `tiktok-batch1-20260630` and
  `session_mode=client_provided_session`; the last two were explicit recurrence
  probes and both stopped on `challenge_close_diagnostic_only` with visual
  diagnostic `target_found=true`, `clicked=true`, `target_kind=visual_x`,
  `page_text_gate_matched=true`, empty `results`, no batch-admission claim, and
  no expansion.
- Forbidden-marker scans over the recurrence scratch outputs returned no
  matches.
- Temporary copied auth-state files were removed after each run and verified
  absent.


## Dangerous To Reuse

- Do not reuse earlier logged-out public-route diagnostics as sessioned warm-probe
  success.
- Do not reuse the old idea that clicking `Close` on a slider challenge solves
  the blocker. It does not.
- Do not reuse pre-PR #583 assumptions that itemStruct-present rows can ignore a
  blocker-triage stop verdict.
- Do not reuse any command that adds non-existent live-runner flags.
- Do not repeat live retries blindly after `platform_challenge_observed`; require
  owner/human account-posture review before another live browser action.
- Do not reuse the old continuation gate that allowed a 3-5 creator run after
  sanitized staging plus admission alone. Zero comment-list response yield is a
  stop/diagnosis class, not a completed capture row.

## Final Courier Prompt

Paste this to the execution lane after the packet is merged or otherwise
available:

```text
Open and follow:
docs/workflows/tiktok_live_microbatch_owner_gated_handoff_v0.md

Follow the packet's confirm-don't-trust load contract. If you have repo/filesystem
access, open the packet and re-read its named load-bearing sources before making
strict or actionable claims. If you do not have repo/filesystem access, stop and
request a pasted source capsule or no-repo handoff.

Continue only the lane named in the packet's Goal Handoff / Active Objective. Do
not perform work excluded by the packet's Drift Guard unless explicitly redirected
by the current user.

First task after getting your bearings: verify owner/live-run preconditions and
the current stop state. Load
`docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md` before any
browser action. Do not run another live retry blindly: the latest visual-X
diagnostic stopped as `challenge_close_diagnostic_only`. If the owner explicitly
reauthorizes after human account/session review, run only the
one-video route-yield gate first. The current runner first attempts bounded
benign-overlay dismissal, then uses
`comment_surface_toggle_pointer_sequence_v0` (comments -> More like this ->
comments); require at least one admitted page-owned
`/api/comment/list` response or DOM-visible comment candidate before
admission/expansion; stop on unresolved challenge text after follow-through,
unresolved blocker, or zero-comment/zero-DOM route diagnosis. Do not solve
CAPTCHA/slider challenges,
do not treat a close click alone as success, do not expand directly to 3-5
creators, and do not do product extraction. If the current owner explicitly
authorizes `--allow-challenge-close-followthrough`, the runner may close an
X-able public challenge and then attempt the page-owned/DOM-visible comment
route; any admitted result must preserve the close action as a source-access
intervention.
Use `--allow-challenge-close-diagnostic` only for stop-only changed-condition
checks.
```
