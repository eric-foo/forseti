# IG Browser Behavior Calibration Note v0

```yaml
retrieval_header_version: 1
artifact_role: Non-authorizing IG calibration recommendation
scope: >
  IG-only browser-behavior calibration note for social capture. Records the
  completed IG docs patch boundary and prepares a bounded logged-out probe around
  session shape, stop/cooldown, viewport/fallback, stable egress lanes, and
  receipt evidence.
use_when:
  - Checking the active IG browser-behavior calibration boundary.
  - Preparing the bounded IG logged-out sustainability probe after the docs patch.
  - Preventing this lane from drifting into runtime work, proxy/session fallback,
    non-IG source work, media-byte capture, or full comment-thread capture.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_at_scale_operating_envelope_v0.md
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_logged_out_sustainability_probe_plan_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - orca/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md
branch_or_commit: codex/social-capture-browser-calibration-core-port working tree from origin/main @ 2988c82f; later lane commits refine this artifact
stale_if:
  - IG sustained cadence, cooldown, viewport, route, or lane-isolation evidence changes.
  - A non-IG social platform enters scope.
  - The Source Capture playbook, source-access boundary, wind-caller carve-out, or anti-block ladder changes.
  - Browser-behavior controls are implemented in runtime code.
```

## Status And Boundary

Status: `NON_AUTHORIZING_IG_RECOMMENDATION`.

Primary label: `IG_DOC_PATCH_DONE__STAGE_1_PROBE_PREP_NEXT`.

This note does not by itself authorize live IG capture, runtime edits, browser
automation installation, proxy/session setup, anti-detect tooling, scheduler
work, account flows, credentials, production workers, source-access boundary
changes, validation, readiness, legal sufficiency, or commercial use.

## Active Scope Lock - IG Only

Keep in this lane:

- IG session-shape profile and anti-bot cadence discipline.
- Stop-on-wall and fully quiet cooldown discipline.
- Viewport/fallback interpretation before false `NO-GO`.
- Stable egress-lane language and no per-request rotation.
- Receipt evidence for anti-bot and data-integrity analysis.

Cut from this lane:

- non-IG social platform recon;
- cross-platform abstraction artifacts;
- full comment-thread/body capture, commenter identity capture, comment graph
  expansion, or comment timestamp capture;
- media/video-byte capture claims;
- runtime/code changes;
- proxy/session/account fallback;
- live probe execution from this docs patch.

In the current IG receipt patch, `comments` means source-visible `comment_count`
only.

## Source Readiness

`SOURCE_CONTEXT_READY` for a non-authorizing IG-only recommendation.

Loaded local sources:

- Orca authority and prompt rules: `AGENTS.md`, `.agents/workflow-overlay/README.md`,
  `.agents/workflow-overlay/decision-routing.md`, `.agents/workflow-overlay/source-loading.md`,
  `.agents/workflow-overlay/source-of-truth.md`, `.agents/workflow-overlay/artifact-folders.md`,
  `.agents/workflow-overlay/prompt-orchestration.md`, `.agents/workflow-overlay/validation-gates.md`,
  `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`, and
  `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`.
- Capture method and access boundary:
  `docs/workflows/data_capture_spine_consolidation_map_v0.md`,
  `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`,
  `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`,
  `orca/product/spines/capture/core/source_capture_toolbox/source_capture_anti_block_ladder_usage_guide_v0.md`,
  `orca/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md`,
  and `docs/decisions/wind_caller_calibration_carveout_v0.md`.
- IG current spine:
  `orca/product/spines/capture/core/source_families/social_media/instagram/ig_capture_findings_consolidated_v0.md`,
  `ig_r_probe_results_v0.md`, `ig_capture_rate_findings_report_v0.md`,
  `ig_at_scale_operating_envelope_v0.md`,
  `ig_logged_out_sustainability_probe_plan_v0.md`,
  `ig_sustained_cadence_r_probe_design_v0.md`,
  `ig_capture_shape_contract_spec_v0.md`,
  `ig_wind_caller_calls_capture_build_architecture_v0.md`, and
  `orca-harness/runners/run_source_capture_ig_calls_packet.py`.

Material IG gaps:

- IG at-pace daily-volume ceiling, exact pace threshold, exact cooldown decay,
  lane-2 isolation, and durable viewport behavior remain unproven.
- Media/video byte capture is out of scope and unprobed for IG.
- Full comment-thread/body capture and comment timestamp capture are out of
  scope for this lane.

## Current IG Behavior Model

IG is currently a logged-out-first capture route for the loaded signals. The
consolidated findings say public calls, profile stats, and reel/video view
counts remain capturable by headless browser on a clean public egress, while
current local egress can soft-wall and later recover after quiet time
(`ig_capture_findings_consolidated_v0.md:36-43`). Calls, profile stats, and
reel/video view counts have distinct substrates: `og:description`, profile
stats surfaces, and profile-feed JSON respectively
(`ig_capture_findings_consolidated_v0.md:51-54`).

The source-backed pace rule is IG-specific: the rate report says logged-out
reads are pace-limited, not volume-limited, with approximately 2.5-4 seconds
between reads, never sub-2s bursts; the sub-2s failure became a sticky,
IP-wide login redirect requiring a fully quiet cooldown longer than the
observed failed recovery window (`ig_capture_rate_findings_report_v0.md:29-37`,
`ig_r_probe_results_v0.md:44-48`).

The at-scale envelope already says whole sessions matter, not only item-to-item
sleeps. It names bounded, human-initiated/self-terminating sessions;
due-list-only passive monitoring; stable egress lanes; a hard no-sub-2s floor;
stop-on-login/429/network-security blocks; cluster gaps; bounded scroll depth;
per-run item caps; and visible block/stop receipts
(`ig_at_scale_operating_envelope_v0.md:176-200`).

IG viewport behavior is not stable enough to bury. The logged-out sustainability
plan says prefer `768x1024` for profile reads, record the viewport, and use
`web_profile_info` / profile-feed JSON shortcodes before classifying an empty
DOM grid as failure (`ig_logged_out_sustainability_probe_plan_v0.md:140-143`,
`ig_logged_out_sustainability_probe_plan_v0.md:199-203`).

## IG Patch State

The active IG docs patch should preserve these decisions:

1. Name the IG browser-session profile in
   `ig_at_scale_operating_envelope_v0.md` as
   `ig_logged_out_browser_session_shape_v0`.
2. Treat `bounded_jitter` as necessary but insufficient; preserve warm-up,
   due-bucket batching, cluster gaps, idle windows, per-run item caps, bounded
   scroll depth, and abort/quiet behavior as one profile.
3. Make stop/cooldown and block taxonomy receipt-bearing: `redirected_to_login`,
   `rate_limited_429_interstitial`, `network_security_block`, `no_signal`, and
   `capture_failed` must stay distinct.
4. Bind viewport and enumeration fallback as evidence: empty DOM at an unproven
   viewport is not automatically `NO-GO`.
5. Preserve stable egress lanes and reject per-request rotation.
6. Keep media/asset-byte behavior out of the patch.
7. Record `capture_time`, source item timestamp/date, item locator, visible
   `like_count`, visible `comment_count`, applicable view/play count, page
   result, stop reason, viewport, enumeration route, and verdict in probe
   receipts.

No source-access boundary amendment is recommended now.

## Probe Preparation

Current owner direction authorizes preparing for a live IG probe, but execution
still needs the run-specific bounds below in the operating thread before any
network read starts.

Default first run package:

- Stage scope: Stage 1 single-lane clean baseline first. Run Stage 0 lane
  isolation only before any two-lane interpretation.
- Lane scope: one logged-out baseline egress lane; no proxy, session, cookies,
  login automation, or anti-detect setup.
- Subject set: 4-6 owner-supplied public IG handles, locked before the run; no
  discovery during the run.
- Viewport and route: start at `768x1024`; record JSON shortcode fallback before
  classifying an empty DOM grid.
- Pace and ceiling: 2.5-4s minimum spacing with longer natural gaps; never
  sub-2s; about 80-120 modeled IG-request equivalents unless owner narrows the
  ceiling.
- Stop and cooldown: stop on first login redirect, 429-like interstitial,
  network-security block, unexpected auth wall, or operator concern; use at
  least 60 minutes fully quiet before any recovery read.
- Output: gitignored scratch for raw operational receipts; durable summary only
  after the run if separately requested.
- Comment scope: `comment_count` only; no full comment-thread/body capture,
  commenter identity capture, comment graph expansion, or comment timestamp
  capture.

## Next Authorized Step

Prepare the Stage 1 live-probe run package by binding the subject set, lane
scope, modeled-request ceiling, time ceiling, cooldown policy, and output
location. Do not execute the live probe from this note alone, and do not scope
runtime behavior from this note.

## Non-Claims

This note is not validation, readiness, source-access authorization, legal
advice, platform permission, implementation authorization, runtime scoping,
proxy/session approval, anti-detect approval, scheduler authorization, ECR,
Cleaning, Judgment, buyer proof, commercial evidence, or proof that any non-IG
platform can inherit IG's model.