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
  - orca-harness/source_capture/adapters/browser_snapshot.py
  - orca-harness/source_capture/tiktok/live_batch_probe.py
  - orca-harness/source_capture/tiktok/blocker_triage.py
  - orca-harness/source_capture/tiktok/batch_packet.py
  - orca-harness/source_capture/tiktok/admission.py
  - orca-harness/runners/run_source_capture_tiktok_live_batch_probe.py
  - orca-harness/runners/run_source_capture_tiktok_batch_packet.py
branch_or_commit: f58eccc8fff5a81939c9677d8cad8a4ad70bcbb7
input_hashes:
  AGENTS.md: c28077faf75c83b80800beda7508ae7a6d95a411
  .agents/workflow-overlay/README.md: 57cbc892dcd79d4d57686db465900ad042769174
  .agents/workflow-overlay/source-loading.md: 29c8c3211299aff22837ef9981e5865f3c15c222
  orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md: 9bbec5e63e8d8845a3b6c24ff58acbc8bf039ba6
  orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_sessioned_capture_warm_probe_plan_v0.md: 0814b9f9aaa8e925c03d2cb5ae81c876a33073aa
  orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_first_slice_probe_recon_v0.md: 8ae31ac55067f2ec175f6baa6867939704cf7078
  docs/workflows/tiktok_public_route_live_diagnostic_receipt_v0.md: a0ca160b4a984a2d6e2f0d191a2deea8d6844a2b
  docs/workflows/tiktok_behavioral_sync_fresh_lane_handoff_v0.md: 0fcda55434efb97791c495e112e7682f9cc1b42d
  docs/workflows/tiktok_comment_response_capture_pr559_adjudication_handoff_v0.md: 5a814dad39d79222ea78631e395ff382d4fc7396
  docs/workflows/tiktok_funmi_n30_comment_subtitle_cadence_analysis_v0.md: 8385e43615e76a2503e9f36468dbdcd7c92268a3
  orca-harness/source_capture/adapters/browser_snapshot.py: 626200271254fbec54185226c9be220c19f80b9a
  orca-harness/source_capture/tiktok/live_batch_probe.py: dc2989412d8e355453283abaff935a449ddd0af5
  orca-harness/source_capture/tiktok/blocker_triage.py: 19816ad967bc57c53aa750dfc9cf59902e5455cd
  orca-harness/source_capture/tiktok/batch_packet.py: b6758d7615a96804e48714283f1925577c7dc22c
  orca-harness/source_capture/tiktok/admission.py: 45a86b554772a58300b23be077a48b32f8dcd8de
  orca-harness/runners/run_source_capture_tiktok_live_batch_probe.py: a541072ee177f46892b9f8d697376376383750e6
  orca-harness/runners/run_source_capture_tiktok_batch_packet.py: 856b76df0be96b47040486260b52a427444072d9
stale_if:
  - PR #583 is reverted or the TikTok blocker-triage/live-probe stop behavior is superseded.
  - `browser_snapshot.py`, `live_batch_probe.py`, `blocker_triage.py`, `batch_packet.py`, or `admission.py` changes materially.
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
  Make the TikTok source-capture lane produce sanitized, admissible, page-owned
  live staging data under real sessioned conditions without violating
  stop-on-challenge or account-safety boundaries.
anchor_goal: >
  Repair the live micro-batch gate so one known public video must prove a real
  page-owned `/api/comment/list` response before any cross-creator batch spends
  more account/session budget.
success_signal: >
  For the first attempted creator/video, produce a run receipt with attempted,
  completed, challenge, and failure counts; at least one admitted page-owned
  comment-list response; captured comment count; subtitle metadata yield;
  admission path if completed; and explicit no-secret/no-raw-URL/no-cookie
  confirmation. If comment-list yield is zero, stop as a diagnosis result and
  do not expand. No product-value or scale claim.
```

## Active Objective

Run a bounded, owner-gated TikTok live route-yield gate using the current
`run_source_capture_tiktok_live_batch_probe.py` runner: one known public video
first, sanitized staging, no challenge solving, and no expansion unless the first
video captures at least one real page-owned `/api/comment/list` response.

The prior micro-batch packet version was corrupted for execution: it allowed
continuation on sanitized staging plus admission alone. Treat the 2026-07-02
five-creator zero-response run as a diagnostic receipt, not capture success.

## Open Decision / Fork

The only live-run fork is whether to proceed past the first creator/video:

- Continue to a 3-5 creator micro-batch only if the first video has
  `challenge_count=0`, no empty/stripped shell, no auth wall, no unresolved
  blocker stop, `completed_count=1`, and at least one admitted page-owned
  `/api/comment/list` response.
- Stop if comment-list response yield is zero. Record it as
  `comment_list_response_absent` / route-opening diagnosis, not as a completed
  capture row and not as TikTok route failure in general.
- Stop if the first creator hits a real challenge class: slider/captcha/verify,
  login/auth wall, ban/40x on the authenticated session, empty/stripped shell,
  missing video-detail hydration, or an unresolved actual dismiss/reload blocker
  that the triage classifies as stop.
- Retry once only for transport/infra noise clearly distinguished from TikTok,
  such as extension/proxy chrome-error style failures already called out by the
  TikTok recon/spec. Do not convert repeated infra failures into a TikTok ceiling.
- Ask the owner if the dedicated account/session label, known public first-video
  URL, or live-network/browser permission is missing.

## Drift Guard

- Do not solve CAPTCHA/slider/verification challenges.
- Do not click an `X` or `Close` on a visible challenge and report success. The
  public diagnostic already observed a slider challenge plus a visible `Close`;
  the lane stopped there.
- Do not use a personal TikTok account. This lane assumes a dedicated,
  burnable, warmed account with human-performed login.
- Do not enter credentials, inspect cookies/tokens, preserve storage-state paths,
  proxy endpoints, exit IPs, raw signed URLs, raw subtitle bodies, or raw response
  bodies.
- Do not run scale. This is a one-video route-yield gate first; a 3-5 creator
  micro-batch is allowed only after the first video captures at least one real
  page-owned `/api/comment/list` response.
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
- The first corrected live retry on 2026-07-03 used that sequence on the Funmi
  video and stopped with `attempted_count=1`, `completed_count=0`,
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
   the owner explicitly directs a different small-N cadence.


5. Inspect the first-video outputs before admission or expansion:

   - `tiktok_live_grid_result.json`
   - `tiktok_live_cadence_result.json`

   Required to continue: `attempted_count=1`, `completed_count=1`,
   `challenge_count=0`, no failures, capture contract clean, and
   `results[0].capture_receipt.admitted_comment_response_count >= 1`.

   If `challenge_count` is nonzero or failures contain a challenge/auth stop, stop.

   If `admitted_comment_response_count` is zero, stop and report
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
   comment-list response and admits cleanly, run the remaining 2-4 creators with
   the same small-N shape. Stop at the first real challenge class, unresolved
   blocker stop, or zero-comment-response route diagnosis.

8. Produce a receipt with:

   - commit/branch and exact commands used;
   - creator count and video count attempted;
   - per-creator attempted/completed/challenge/failure counts;
   - first stop reason if any;
   - comment-list response success count/yield and captured comment count;
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
`/api/comment/list` response under the current runner and then admits cleanly.

Current live state: the corrected 2026-07-03 one-video retry stopped on
`platform_challenge_observed` with `challenge_count=1`; no admission or
expansion is authorized from that receipt. A further live retry should start
from owner/human account-posture review, not from blind repetition.


## Changed / Inspected / Tested Files In This Handoff Lane

Changed:

- `docs/workflows/tiktok_live_microbatch_owner_gated_handoff_v0.md`
- `orca-harness/source_capture/adapters/browser_snapshot.py`
- `orca-harness/source_capture/tiktok/live_batch_probe.py`
- `orca-harness/tests/unit/test_source_capture_browser_snapshot.py`
- `orca-harness/tests/unit/test_tiktok_live_batch_probe.py`

Inspected:

- All files in `open_next` needed for this live route-yield gate and stop-state
  repair.

Validation completed:

- `PYTHONPATH=orca-harness python -m pytest -q orca-harness/tests/unit/test_source_capture_browser_snapshot.py orca-harness/tests/unit/test_tiktok_live_batch_probe.py orca-harness/tests/unit/test_tiktok_batch_admission.py`
  -> `54 passed`
- One owner-authorized live retry using auth-state label `tiktok-batch1-20260630`
  and `session_mode=client_provided_session`; result stopped on
  `platform_challenge_observed` before admission/expansion.
- Forbidden-marker scan over the latest retry scratch output returned no matches.
- Temporary copied auth-state files were removed after the run.


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
the current stop state. Do not run another live retry blindly: the latest
corrected route opener stopped on `platform_challenge_observed`. If the owner
explicitly reauthorizes after human account/session review, run only the
one-video route-yield gate first, using
`comment_surface_toggle_pointer_sequence_v0` (comments -> More like this ->
comments); require at least one admitted page-owned
`/api/comment/list` response before admission/expansion; stop on any real
challenge, unresolved blocker, or zero-comment-response route diagnosis. Do
not solve CAPTCHA/slider challenges, do not click challenge-close controls to
claim success, do not expand directly to 3-5 creators, and do not do product
extraction.
```
