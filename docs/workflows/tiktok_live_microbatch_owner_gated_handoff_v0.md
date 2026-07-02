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
  - orca-harness/source_capture/tiktok/live_batch_probe.py
  - orca-harness/source_capture/tiktok/blocker_triage.py
  - orca-harness/source_capture/tiktok/batch_packet.py
  - orca-harness/source_capture/tiktok/admission.py
  - orca-harness/runners/run_source_capture_tiktok_live_batch_probe.py
  - orca-harness/runners/run_source_capture_tiktok_batch_packet.py
branch_or_commit: 1dfbb2d09819696b93a2d0c0b3c5f11b05b5d81d
input_hashes:
  AGENTS.md: c28077faf75c83b80800beda7508ae7a6d95a411
  .agents/workflow-overlay/README.md: 57cbc892dcd79d4d57686db465900ad042769174
  .agents/workflow-overlay/source-loading.md: 29c8c3211299aff22837ef9981e5865f3c15c222
  orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md: 9bbec5e63e8d8845a3b6c24ff58acbc8bf039ba6
  orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_sessioned_capture_warm_probe_plan_v0.md: 0814b9f9aaa8e925c03d2cb5ae81c876a33073aa
  orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_first_slice_probe_recon_v0.md: 8ae31ac55067f2ec175f6baa6867939704cf7078
  docs/workflows/tiktok_public_route_live_diagnostic_receipt_v0.md: a0ca160b4a984a2d6e2f0d191a2deea8d6844a2b
  orca-harness/source_capture/tiktok/live_batch_probe.py: b9bacfadca51acaa575e41762a1689e6c7488e62
  orca-harness/source_capture/tiktok/blocker_triage.py: b0c7d320dc09ee4f65c59d1014deebf2b03d0d80
  orca-harness/source_capture/tiktok/batch_packet.py: b6758d7615a96804e48714283f1925577c7dc22c
  orca-harness/source_capture/tiktok/admission.py: 45a86b554772a58300b23be077a48b32f8dcd8de
  orca-harness/runners/run_source_capture_tiktok_live_batch_probe.py: a541072ee177f46892b9f8d697376376383750e6
  orca-harness/runners/run_source_capture_tiktok_batch_packet.py: 856b76df0be96b47040486260b52a427444072d9
stale_if:
  - PR #583 is reverted or the TikTok blocker-triage/live-probe stop behavior is superseded.
  - `live_batch_probe.py`, `blocker_triage.py`, `batch_packet.py`, or `admission.py` changes materially.
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
  Run the owner-gated 3-5 creator TikTok live micro-batch, checkpoint after the
  first creator/result, and prove that sanitized staging JSON plus network-free
  batch admission can consume real TikTok conditions.
success_signal: >
  For each attempted creator/video, produce a run receipt with attempted,
  completed, and challenge counts; comment-list response yield; subtitle metadata
  yield; admission success/failure path; stop reason if stopped; and explicit
  no-secret/no-raw-URL/no-cookie confirmation. No product-value or scale claim.
```

## Active Objective

Run a bounded, owner-gated TikTok live micro-batch using the current
`run_source_capture_tiktok_live_batch_probe.py` runner, checkpoint after the
first creator, preserve sanitized staging and batch-admission evidence, and stop
on the first real challenge class.

The owner's latest steering for this lane is: go to the 3-5 creator micro-batch
without a separate long smoke phase, but check after the first creator so the
lane can stop early if the session/challenge posture is bad.

## Open Decision / Fork

The only live-run fork is whether to proceed past the first creator:

- Continue if the first creator's staging JSON is sanitized, batch admission
  succeeds, and no real challenge, empty shell, auth wall, or unresolved blocker
  appears.
- Stop if the first creator hits a real challenge class: slider/captcha/verify,
  login/auth wall, ban/40x on the authenticated session, empty/stripped shell,
  missing video-detail hydration, or an unresolved actual dismiss/reload blocker
  that the triage classifies as stop.
- Retry once only for transport/infra noise clearly distinguished from TikTok,
  such as extension/proxy chrome-error style failures already called out by the
  TikTok recon/spec. Do not convert repeated infra failures into a TikTok ceiling.
- Ask the owner if the dedicated account/session label, creator/video list, or
  live-network/browser permission is missing.

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
- Do not run scale. This is a 3-5 creator micro-batch with small N per creator,
  checkpointed after the first creator.
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

## Exact Next Authorized Action

1. Verify repo state:

   ```powershell
   git status --short --branch
   git rev-parse HEAD
   git log --oneline -5
   ```

   Expected authoring baseline was `1dfbb2d09819696b93a2d0c0b3c5f11b05b5d81d`
   on a branch based on `origin/main`, with `Add TikTok blocker triage receipts
   (#583)` in recent history. If HEAD differs, re-read the changed sources and
   update this plan from the current code.

2. Verify live-run preconditions before any network/browser action:

   - explicit owner authorization for the live run in the current lane;
   - dedicated, non-personal, warmed TikTok account;
   - human-performed login already bootstrapped into an auth-state label;
   - session mode value matching the auth-state metadata;
   - no concurrent or duplicate TikTok tabs in that browser context;
   - 3-5 creator handles and 2-3 known public video URLs per creator;
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

4. Run the first creator only, using the current CLI help as the source of truth.
   Shape:

   ```powershell
   $env:PYTHONPATH = "orca-harness"
   python orca-harness\runners\run_source_capture_tiktok_live_batch_probe.py `
     --creator-handle "<handle>" `
     --creator-profile-url "https://www.tiktok.com/@<handle>" `
     --video-url "<public-video-url-1>" `
     --video-url "<public-video-url-2>" `
     --state-label "<existing-auth-state-label>" `
     --session-mode "<mode-from-auth-state-metadata>" `
     --output-dir "<scratch-output-dir>\creator_01" `
     --browser-channel chrome
   ```

   Do not add flags that are not present in `--help`. Keep default cadence unless
   the owner explicitly directs a different small-N cadence.

5. Inspect the first creator outputs before continuing:

   - `tiktok_live_grid_result.json`
   - `tiktok_live_cadence_result.json`

   Check `attempted_count`, `completed_count`, `challenge_count`, `failures`,
   `capture_contract`, `blocker_triage`, comment assessment posture/counts, and
   subtitle metadata fields. Also scan the output directory for obvious forbidden
   markers before admission:

   ```powershell
   rg -n "msToken|X-Bogus|verifyFp|ttwid|sessionid|sid_guard|passport_csrf|cookie|tiktokcdn|byteoversea|tos-" "<scratch-output-dir>\creator_01"
   ```

   A match is not automatically a leak, but raw secrets, raw signed URLs, raw
   media/subtitle URLs, cookies, or storage-state paths block continuation.

6. Admit the first creator's sanitized staging JSON through batch admission:

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
   live run. For a smoke/micro-batch handoff, local `--output` is the lower-risk
   default unless redirected.

7. If and only if the first creator is clean, run the remaining 2-4 creators with
   the same small-N shape. Stop at the first real challenge class or unresolved
   blocker stop.

8. Produce a receipt with:

   - commit/branch and exact commands used;
   - creator count and video count attempted;
   - per-creator attempted/completed/challenge counts;
   - first stop reason if any;
   - comment-list response success count/yield and captured comment count;
   - subtitle metadata video count/yield;
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
- `live_batch_probe.py`: local staging writer, stop hooks, pointer-action
  parameters, sensitive-material assertion, output names, and capture contract.
- `blocker_triage.py`: challenge/auth-wall stop, missing itemStruct reload
  candidate classification, ambiguous dismiss stop, and classification-only model.
- `batch_packet.py` and `admission.py`: network-free sanitized batch admission,
  summary fields, and sensitive-material enforcement.
- Runner help for both TikTok live probe and batch admission CLIs.

## Current Task State

Ready for a separate live-execution lane. This handoff does not perform the live
run. It only preserves the source-loaded route and boundaries for the agent that
will run it.

## Changed / Inspected / Tested Files In This Handoff Lane

Changed:

- `docs/workflows/tiktok_live_microbatch_owner_gated_handoff_v0.md`
- `docs/workflows/orca_repo_map_v0.md` if the companion repo-map row is present
  in the same commit/PR

Inspected:

- All files in `open_next`, plus `.agents/workflow-overlay/retrieval-metadata.md`
  and `docs/workflows/orca_repo_map_v0.md`.

Validation expected for this docs-only handoff:

- `git diff --check`
- repo-map/header checks if available in the local hook surface
- no live TikTok/browser/network run

## Dangerous To Reuse

- Do not reuse earlier logged-out public-route diagnostics as sessioned warm-probe
  success.
- Do not reuse the old idea that clicking `Close` on a slider challenge solves
  the blocker. It does not.
- Do not reuse pre-PR #583 assumptions that itemStruct-present rows can ignore a
  blocker-triage stop verdict.
- Do not reuse any command that adds non-existent live-runner flags.

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
run the TikTok live micro-batch exactly as bounded there: 3-5 creators, small N
per creator, checkpoint after the first creator, sanitized staging plus
batch-admission proof, and stop on the first real challenge class. Do not solve
CAPTCHA/slider challenges, do not click challenge-close controls to claim
success, and do not do product extraction.
```