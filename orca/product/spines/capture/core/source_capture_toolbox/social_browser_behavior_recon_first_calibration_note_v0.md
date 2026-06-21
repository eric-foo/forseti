# Social Browser Behavior Recon-First Calibration Note v0

```yaml
retrieval_header_version: 1
artifact_role: Non-authorizing architecture recommendation
scope: >
  IG-first browser-behavior calibration recommendation for social capture.
  Recommends bounded IG doc patches and a shared conceptual controller shape,
  while requiring TikTok/YouTube recon before any platform-specific settings,
  thresholds, route choices, or source-access posture are inherited from IG.
use_when:
  - Deciding whether the IG browser-behavior model should be patched now.
  - Deciding whether TikTok or YouTube may inherit IG-derived capture behavior.
  - Preparing a later owner-gated implementation-scoping prompt.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_at_scale_operating_envelope_v0.md
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_logged_out_sustainability_probe_plan_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - orca/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md
branch_or_commit: codex/social-capture-browser-calibration-core-port working tree from origin/main @ 2988c82f
stale_if:
  - IG sustained cadence, cooldown, viewport, route, or lane-isolation evidence changes.
  - TikTok or YouTube receive durable Capture recipe cards, source-family recon, or source-access decisions.
  - The Source Capture playbook, source-access boundary, wind-caller carve-out, or anti-block ladder changes.
  - Browser-behavior controls are implemented in runtime code.
```

## Status And Boundary

Status: `NON_AUTHORIZING_RECOMMENDATION`.

Primary recommendation label: `RECOMMEND_RECON_FIRST_FOR_TIKTOK_YOUTUBE`.

Secondary label: `IG_PATCH_NOW__TT_YT_RECON_FIRST`.

This note recommends documentation/architecture changes only. It does not
authorize live IG/TikTok/YouTube capture, runtime edits, browser automation
installation, proxy/session setup, anti-detect tooling, scheduler work, account
flows, credentials, production workers, source-access boundary changes,
validation, readiness, legal sufficiency, or commercial use.

## Source Readiness

`SOURCE_CONTEXT_READY` for a non-authorizing IG-first recommendation, with
explicit TikTok/YouTube source gaps.

Loaded local sources:

- Orca authority and prompt rules: `AGENTS.md`, `.agents/workflow-overlay/README.md`,
  `.agents/workflow-overlay/decision-routing.md`,
  `.agents/workflow-overlay/source-loading.md`,
  `.agents/workflow-overlay/source-of-truth.md`,
  `.agents/workflow-overlay/artifact-folders.md`,
  `.agents/workflow-overlay/prompt-orchestration.md`,
  `.agents/workflow-overlay/validation-gates.md`,
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
  `orca_creator_monitoring_policy_architecture_v0.md`, and
  `orca-harness/runners/run_source_capture_ig_calls_packet.py`.

Material gaps:

- No durable TikTok or YouTube Capture recipe card was found under
  `orca/product/spines/capture/`; current hits are deferred/seam references or
  future reserved homes, not source-family recon.
- No current official TikTok or YouTube policy/source-access check was run in
  this lane. Their policy posture remains `UNKNOWN - requires source check`.
- IG at-pace daily-volume ceiling, exact pace threshold, exact cooldown decay,
  lane-2 isolation, and durable viewport behavior remain unproven.
- Media/video byte capture is out of scope and unprobed for IG.

## Cynefin Routing Result

Smallest complete outcome: produce one non-authorizing recommendation artifact
that preserves visible IG failure evidence and blocks TikTok/YouTube
generalization until source-family recon exists.

Regime: `Complicated`, with `Complex` evidence gaps around sustained social
platform behavior.

Why: IG has source-backed route, pace, viewport, and receipt evidence, but
TikTok/YouTube have no loaded recipe cards and platform behavior cannot be
inferred from IG.

Allowed next move: patch IG planning docs or commission owner-gated
implementation scoping after owner acceptance.

Disallowed next move: run live capture, edit runtime, install browser/proxy
tooling, or apply IG thresholds/routes to TikTok/YouTube.

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

The current at-scale envelope already says whole sessions matter, not only
item-to-item sleeps. It names bounded, human-initiated/self-terminating
sessions; due-list-only passive monitoring; stable egress lanes; a hard
no-sub-2s floor; stop-on-login/429/network-security blocks; cluster gaps;
bounded scroll depth; per-run item caps; and visible block/stop receipts
(`ig_at_scale_operating_envelope_v0.md:176-200`).

IG viewport behavior is not stable enough to bury. The logged-out sustainability
plan says prefer `768x1024` for profile reads, record the viewport, and use
`web_profile_info` / profile-feed JSON shortcodes before classifying an empty
DOM grid as failure (`ig_logged_out_sustainability_probe_plan_v0.md:140-143`,
`ig_logged_out_sustainability_probe_plan_v0.md:199-203`).

## Failure Modes Not Covered Well Enough

1. The runner has `bounded_jitter`, but the operating contract is broader than
   per-item waits. It needs a named session-shape profile so future scoping
   cannot flatten warm-up, clusters, idle gaps, item caps, and stop rules into a
   single delay knob.
2. The block taxonomy exists in pieces, but the future implementation surface
   needs a single receipt vocabulary that keeps `redirected_to_login`,
   `rate_limited_429_interstitial`, `network_security_block`, `no_signal`, and
   `capture_failed` distinct.
3. Viewport-sensitive profile enumeration can look like a false empty DOM grid.
   The docs need to preserve viewport and fallback-route evidence before any
   `NO-GO`.
4. Cooldown behavior is still underpinned by limited negative evidence.
   Periodic probing may sustain the throttle; the probe plan says stop at wall,
   start with at least 60 minutes fully quiet, and extend if still blocked
   (`ig_logged_out_sustainability_probe_plan_v0.md:277-287`).
5. Lane separation can be confused with account/session count or per-request
   rotation. The at-scale envelope says do not count two devices on one home
   egress as two lanes and do not rotate per request
   (`ig_at_scale_operating_envelope_v0.md:90-99`).
6. Cross-platform sharing is currently only a conceptual seam. The monitoring
   policy supports a core scheduler with per-platform profiles, but explicitly
   leaves TikTok/YouTube fields deferred (`orca_creator_monitoring_policy_architecture_v0.md:46-58`,
   `orca_creator_monitoring_policy_architecture_v0.md:153-170`).

## Proposed Change Set

### 1. Name An IG Browser Session-Shape Profile

Target surface: `ig_at_scale_operating_envelope_v0.md`.

Change: add a compact `ig_logged_out_browser_session_shape_v0` section that
binds warm-up read, due-bucket batching, cluster gaps, natural idle windows,
per-run item caps, bounded scroll depth, and abort/quiet behavior as one profile.

Source-backed rationale: the at-scale envelope already says `bounded_jitter` is
necessary but too thin, and that whole sessions must be shaped
(`ig_at_scale_operating_envelope_v0.md:176-191`).

Expected durability benefit: later scoping is less likely to implement only a
sleep range and call that "human-shaped."

Risk/tradeoff: too much profile detail could overfit the first IG probe. Keep
thresholds marked preliminary where the source marks them preliminary.

Evidence needed: clean repeated windows under the sustainability plan.

Owner gate: doc patch only now; runtime config or scheduler behavior requires
separate owner acceptance and implementation scoping.

### 2. Make Stop/Cooldown Rules A First-Class Receipt Contract

Target surface: `ig_logged_out_sustainability_probe_plan_v0.md`, with a future
implementation-scoping note for the runner.

Change: promote the stop-on-wall and fully quiet cooldown rule into the same
place as the receipt fields: stop on login redirect, 429-like interstitial,
network-security block, unexpected auth wall, or operator concern; do not
periodically probe through a wall.

Source-backed rationale: the probe plan says any compliant-pace block stops,
records a receipt, and uses a fully quiet cooldown; it also warns that periodic
probing may sustain throttle (`ig_logged_out_sustainability_probe_plan_v0.md:203-208`,
`ig_logged_out_sustainability_probe_plan_v0.md:277-287`).

Expected durability benefit: culling/block evidence remains visible and failed
access does not become fake success or retry-thrash.

Risk/tradeoff: conservative cooldowns may reduce throughput. This is acceptable
because the observed issue is pace/wall discipline, not a proven volume ceiling.

Evidence needed: cooldown receipts that show recovery or persistent block after
fully quiet intervals.

Owner gate: implementation of automatic stop/cooldown behavior is runtime work
and is not authorized by this note.

### 3. Bind Viewport And Enumeration Fallback As Evidence, Not Convenience

Target surface: `ig_logged_out_sustainability_probe_plan_v0.md` and future
implementation scoping for `run_source_capture_ig_calls_packet.py`.

Change: require viewport, enumeration route, and fallback route in every
interpretation of DOM-grid success or failure. Treat empty DOM at an unproven
viewport as `PARTIAL` or `no_signal` until JSON shortcode fallback is checked.

Source-backed rationale: IG findings correct several false route readings:
`web_profile_info` 429 was header-less direct HTTP, not browser-context XHR;
reel view-count depth did not wall when following the grid cursor; and rendered
grid extraction is viewport-sensitive (`ig_capture_findings_consolidated_v0.md:90-104`).

Expected durability benefit: fewer false `NO-GO` calls from viewport/layout
artifacts.

Risk/tradeoff: fallback logic can increase complexity. Keep it as a scoped
interpretation rule until implementation scoping binds exact behavior.

Evidence needed: repeat viewport tests across locked handles and egress lanes.

Owner gate: JSON fallback implementation or response-body capture extension is
runtime work and remains separately gated.

### 4. Preserve Stable Egress Lanes And Reject Per-Request Rotation

Target surface: `ig_at_scale_operating_envelope_v0.md`.

Change: tighten the lane language around stable egress assignment: creators and
due buckets belong to stable lanes; second device on same home egress is not
lane 2; per-request rotation is not the operating model.

Source-backed rationale: the at-scale envelope names lane 1 home fibre and lane
2 mobile-data/phone tether, rejects same-home-Wi-Fi as lane 2, and says not to
rotate per request (`ig_at_scale_operating_envelope_v0.md:90-99`).

Expected durability benefit: avoids confusing "more accounts/devices" with
actual independent egress capacity.

Risk/tradeoff: stable lanes cap throughput. That is deliberate until measured
demand proves more lanes are required.

Evidence needed: lane-2 non-IG isolation checks and then bounded IG receipts.

Owner gate: paid proxy, account/session fallback, or new network setup needs
separate owner acceptance.

### 5. Add A Social Browser Controller Concept Only As A Profile Interface

Target surface: `source_capture_toolbox/` architecture note or future prompt,
not runtime code.

Change: describe a shared conceptual controller with only these reusable
fields: access classification, session start/stop boundary, pacing envelope,
cluster/idle rhythm, viewport or rendering profile, block taxonomy, receipt
fields, and platform profile parameters. Do not include IG's numeric settings
as defaults for other platforms.

Source-backed rationale: the monitoring policy already separates platform-
agnostic scheduler machinery from per-platform profile values, and it leaves
TikTok/YouTube profile values deferred (`orca_creator_monitoring_policy_architecture_v0.md:46-58`,
`orca_creator_monitoring_policy_architecture_v0.md:153-170`).

Expected durability benefit: gives future TikTok/YouTube recon a shared shape
without smuggling IG thresholds into those sources.

Risk/tradeoff: naming a controller too early may create implementation gravity.
Keep it conceptual and non-authorizing until a second platform fills a profile
from source evidence.

Evidence needed: at least one durable TikTok or YouTube recipe card or
source-family recon that fills the profile fields.

Owner gate: implementation scoping only after owner acceptance and source-family
recon.

### 6. Keep Media/Asset Capture Out Of The Current Patch

Target surface: none now, except non-claims in the IG docs.

Change: do not add asset/media-byte behavior to the calibration patch. Preserve
the source gap.

Source-backed rationale: IG findings say media/video bytes are out of scope and
unprobed (`ig_capture_findings_consolidated_v0.md:51-54`,
`ig_capture_findings_consolidated_v0.md:148-151`); the sustainability plan says
it must not be used as proof that media/video bytes are capturable
(`ig_logged_out_sustainability_probe_plan_v0.md:349-354`).

Expected durability benefit: prevents a browser-behavior recommendation from
claiming fidelity it did not source-load.

Risk/tradeoff: leaves asset policy unresolved. That is correct until a separate
media/source-fidelity lane exists.

Evidence needed: a bounded media-byte/source-fidelity recon.

Owner gate: separate source-access/runtime authorization.

## IG / TikTok / YouTube Comparison

| Dimension | IG | TikTok | YouTube |
| --- | --- | --- | --- |
| Source-family recon | `known`: IG route, pace, viewport, and receipt evidence exists. | `unknown`: no durable Capture recipe card loaded. | `unknown`: no durable Capture recipe card loaded. |
| Access posture | `known`: logged-out-first for loaded signals; own-session only future fallback/probe. | `unknown`: public surfaces may be in scope, login-walled surfaces remain gated. | `unknown`: public surfaces may be in scope, login-walled surfaces remain gated. |
| Pacing | `known`: 2.5-4s minimum spacing; never sub-2s; exact threshold unpinned. | `do_not_generalize`: no TikTok threshold from IG. | `do_not_generalize`: no YouTube threshold from IG. |
| Cooldown | `known`: fully quiet cooldown, at least 60 minutes in the current plan; exact decay unpinned. | `do_not_generalize`: cooldown behavior must be probed. | `do_not_generalize`: cooldown behavior must be probed. |
| Viewport/route | `known`: `768x1024` candidate, JSON fallback before false `NO-GO`. | `do_not_generalize`: route and viewport unknown. | `do_not_generalize`: route and viewport unknown. |
| Shared primitive | `known`: access gate, session boundary, pacing envelope, stop/receipt discipline can be a conceptual interface. | `known`: may use the same interface after recon fills values. | `known`: may use the same interface after recon fills values. |

## Required Propagation Surfaces If Accepted

If the owner accepts the recommendation, the first patch should be docs-only and
small:

- `ig_at_scale_operating_envelope_v0.md`: add or tighten the named IG browser
  session-shape profile, egress-lane discipline, and per-request rotation
  prohibition.
- `ig_logged_out_sustainability_probe_plan_v0.md`: align receipt fields,
  viewport/fallback interpretation, and cooldown/stop rules.
- Future implementation-scoping prompt: bind exact changes to
  `run_source_capture_ig_calls_packet.py` only after owner acceptance.
- Optional later architecture note under `source_capture_toolbox/`: define the
  shared conceptual profile interface only after the owner accepts that the
  abstraction is useful.

No source-access boundary amendment is recommended now.

## Open Owner Questions

- Should the next patch be IG-only doc tightening, or should it also add a
  non-authorizing shared profile-interface note?
- Is the owner willing to accept the throughput cost of a fully quiet cooldown
  default before exact decay is pinned?
- Should TikTok or YouTube be the first social-platform recon card after IG?
- Should current official TikTok/YouTube policy posture be checked before any
  recon prompt is drafted?

## Next Authorized Step

Patch the two IG planning docs named above, or commission a bounded docs-only
patch prompt for them. Do not run live capture or scope runtime behavior until
the owner accepts this recommendation and separately authorizes the next lane.

## Non-Claims

This note is not validation, readiness, source-access authorization, legal
advice, platform permission, implementation authorization, runtime scoping,
proxy/session approval, anti-detect approval, scheduler authorization, ECR,
Cleaning, Judgment, buyer proof, commercial evidence, or proof that TikTok or
YouTube can inherit IG's model.
