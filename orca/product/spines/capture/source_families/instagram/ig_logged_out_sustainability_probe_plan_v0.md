# IG Logged-Out Sustainability Probe Plan (v0)

```yaml
retrieval_header_version: 1
artifact_role: Product artifact - IG logged-out sustainability probe plan (non-authorizing)
scope: >
  Defines the next bounded measurement plan for testing whether the current IG
  serious-v0 operating posture can remain fully logged-out under repeated,
  compliant, two-lane monitoring pressure. It is a plan for owner-authorized
  future measurement only; it does not authorize live IG reads, proxy/session
  setup, scheduler/runtime work, or implementation.
use_when:
  - Deciding how to test whether logged-out IG monitoring remains viable before building fallback machinery.
  - Preparing an owner authorization request for a bounded IG sustainability probe.
  - Interpreting a future logged-out sustainability result without overclaiming readiness.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/source_families/instagram/ig_at_scale_operating_envelope_v0.md
  - orca/product/spines/capture/source_families/instagram/ig_r_probe_results_v0.md
  - orca/product/spines/capture/source_families/instagram/ig_capture_rate_findings_report_v0.md
  - orca/product/spines/capture/source_families/instagram/ig_sustained_cadence_r_probe_design_v0.md
  - orca/product/spines/capture/source_families/instagram/ig_capture_findings_consolidated_v0.md
  - orca/product/spines/capture/source_capture_toolbox/source_capture_playbook_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
stale_if:
  - A future probe pins the at-pace daily-volume ceiling, exact pace threshold, throttle decay, or two-lane additivity.
  - IG moves the required public signal behind auth or changes the logged-out read substrate.
  - IG changes the profile DOM responsive variant such that `768x1024` no longer exposes the
    measured profile-grid permalink links.
  - The wind-caller carve-out is amended to authorize sessions, standing scheduling, commercial scale, or a different account/egress posture.
  - The IG runner's read model, block detector, response-body support, or metric-observation behavior materially changes.
```

## Status

`PROBE_PLAN_V0 - owner-gated, non-authorizing, logged-out-first.`

This artifact exists because the current evidence supports logged-out IG reachability and a first
pace-bound R reading, but it does **not** prove that fully logged-out monitoring will remain durable
for repeated 1,000-creator serious-v0 operating windows. The next test should measure that
sustainability directly before Orca builds sessions, proxies, scheduler/runtime machinery, or
account-based fallback paths.

This is a documentation/product-method plan only. It is not a live-run instruction, not validation,
not readiness, not buyer proof, not commercial authorization, not proxy/session approval, not network
setup approval, and not implementation authorization.

## Source-loading receipt

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S0 + Source Capture Method + IG operating-envelope sources
  edit_permission: docs-write
  target_scope: new non-authorizing IG logged-out sustainability probe plan
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md, overlay README, source-loading, artifact folders, retrieval metadata, source capture playbook, carve-out, current IG R/envelope docs
```

Key source reads for this plan:

- `AGENTS.md` and `.agents/workflow-overlay/README.md`: project boundary and docs/runtime authorization split.
- `.agents/workflow-overlay/source-loading.md`: capture-spine activity starts with the source-capture playbook.
- `.agents/workflow-overlay/artifact-folders.md` and `.agents/workflow-overlay/retrieval-metadata.md`: product-doc placement and header contract.
- `orca/product/spines/capture/source_capture_toolbox/source_capture_playbook_v0.md`: access-control gate, blocked-as-hypothesis rule, receipt/verdict discipline.
- `docs/decisions/wind_caller_calibration_carveout_v0.md`: internal-only, pre-commercial, human-initiated, time-bounded, self-terminating passive-monitoring boundary.
- `orca/product/spines/capture/source_families/instagram/ig_capture_findings_consolidated_v0.md`: logged-out reachability and session-lane retirement for current IG signal.
- `orca/product/spines/capture/source_families/instagram/ig_r_probe_results_v0.md`: first measured pace-bound R evidence and open residuals.
- `orca/product/spines/capture/source_families/instagram/ig_capture_rate_findings_report_v0.md`: preliminary operating guidance and pending at-pace daily ceiling.
- `orca/product/spines/capture/source_families/instagram/ig_at_scale_operating_envelope_v0.md`: two-lane serious-v0 operating posture for 1,000 creators.
- `orca/product/spines/capture/source_families/instagram/ig_sustained_cadence_r_probe_design_v0.md`: prior R-probe design, purity boundary, and owner-gated run posture.

## Assumption gate result

The accepted direction is to write a non-authorizing probe plan before any live probe or runtime
work. The load-bearing assumptions checked before this artifact:

| Assumption | Verdict | Evidence |
| --- | --- | --- |
| A docs-only probe plan is authorized; live/network/runtime action is not. | Verified real | `AGENTS.md` permits documentation work by default and requires explicit bounded authorization for implementation/runtime work; the source-capture playbook grants no live-run authority. |
| Logged-out IG is reachable enough to plan a sustainability test, but not proven durable at serious-v0 pressure. | Verified real | Consolidated IG findings record logged-out reachability; R results record only first measured pace-bound evidence with open at-pace ceiling and decay residuals. |
| Future measurement must use capture-method guardrails and receipt discipline. | Verified real | Source-capture playbook requires Step 0 access classification, honest GO/PARTIAL/NO-GO/CATALOG_GAP receipts, and treats blocked as a hypothesis. |

The gate clears this artifact only. It does not clear the future live run.

## The Decision This Probe Must Answer

```text
Can the 1,000-creator serious-v0 IG monitoring posture remain fully logged-out,
using stable paced egress lanes and bounded self-terminating sessions, without
sessions, proxies, standing schedulers, or account-based fallback machinery?
```

The test is not meant to prove commercial readiness. It is meant to prevent Orca from building the
wrong fallback too early. The failure mode to avoid is assuming "logged-out works" from reachability
and one clean paced run, then discovering during implementation that repeated compliant windows
accumulate sticky throttling.

## Current Evidence Boundary

What is currently supported:

- IG public calls, profile stats, and reel/view-count substrate are recorded as logged-out reachable
  in the consolidated IG findings.
- The first R reading found a pace wall, not an ordinary session-volume wall: a clean run sustained
  about 176 modeled requests over 37 minutes, while sub-2s behavior tripped an IP-wide soft
  login redirect.
- Owner-adopted operating pace is about 2.5-4s between reads, never sub-2s.
- Neither proxies nor sessions are currently warranted for realistic monitoring/burst cadences.
- The serious-v0 operating envelope uses two stable logged-out egress lanes for the 1,000-creator
  plan, not per-request rotation and not multiple logged-in accounts.
- The 2026-06-17 successor probes add two route facts: current local egress can be logged-out
  soft-walled, while alternate residential egress worked logged-out; owner-created session state on
  current egress also worked for `web_profile_info`, but sustained account/session cadence remains
  unmeasured and outside this logged-out-first plan.
- Profile item enumeration is viewport-sensitive. In a bounded `@hyram` proxy route, `768x1024` and
  `1280x1200` exposed 12 DOM permalinks, while `1280x720`, `820x1180`, and `1024x1366` exposed none.
  JSON profile-feed enumeration still returned shortcodes when the DOM grid was empty.

What remains not proven:

- At-pace daily-volume ceiling.
- Exact pace threshold.
- Throttle decay time after a wall.
- Whether repeated compliant windows accumulate throttle state.
- Whether two distinct egress lanes behave additively under bounded IG reads.
- Whether the second-laptop/mobile-data lane has been isolated and then tested in this repo lane.
- Whether the logged-out current local egress recovers after a fully quiet cooldown.

## Probe Posture

The successor probe should be **logged-out-first and compliant-pace-first**.

Do not start by deliberately driving sub-2s to find the wall again. The previous R-probe already found
that failure mode. The current risk is different: whether compliant, repeated, bounded windows remain
usable. A wall-finding ramp is a contingency only if compliant testing gives a confusing result that
cannot be interpreted without measuring the threshold.

Use the measured profile-enumeration route deliberately: prefer `768x1024` for profile reads, and do
not interpret an empty DOM grid at `1280x720` as a source NO-GO. If DOM links are absent, record the
viewport and use `web_profile_info` / profile-feed JSON shortcodes as the fallback enumerator before
classifying the failure.

### Hard boundaries

- Publicly-viewable IG material only; no private accounts, DMs, paywalls, or access-control bypass.
- Logged-out baseline only; no cookies, sessions, stored auth state, or login automation.
- No paid proxy, anti-detect setup, or per-request IP rotation in the baseline. A phone-tether/mobile
  lane is an alternate logged-out egress lane, not request rotation. A residential proxy route is a
  separate fallback diagnostic, not the baseline sustainability proof.
- No standing crawler, daemon, unattended scheduler, or auto-retry loop.
- No discovery during passive monitoring windows; subject handles are locked before the run.
- No typed `metric_observations`; this measures read sustainability, not producer/projection acceptance.
- Abort on login redirect, 429-like interstitial, network-security block, unexpected auth wall, or
  operator concern.
- After any wall, stop and use a fully quiet cooldown; do not keep probing periodically as if that
  were neutral.

## Subject Set

Use a small locked set of already-flagged, US-first public beauty creators. The set should be chosen
before the run and recorded in the receipt.

Minimum viable set:

- 8-12 public creator handles.
- Mix of A/B/C-like monitoring roles if available: rising/high-signal, established/slower, and long-tail/dormant.
- No private/auth-gated handles.
- No live discovery, related-account snowballing, or new-roster expansion during the probe.

The subject set is not an assertion that the roster is complete or representative. It is only enough
to exercise repeated multi-creator monitoring windows without expanding the lane into discovery.

## Probe Stages

### Stage 0 - Non-IG Lane Isolation

Purpose: confirm two distinct egress paths before any two-lane IG interpretation.

Checks:

1. Compare public IP/provider on the main laptop/home fibre lane and second laptop/mobile-data lane.
2. Confirm the second laptop loses internet when phone tether/mobile upstream is disconnected.
3. Confirm the second laptop does not silently rejoin home Wi-Fi.
4. Confirm the phone is on mobile data, not home Wi-Fi.

Output: network-separation receipt only. Passing this stage proves network separation, not IG safety.

### Stage 1 - Single-Lane Clean Baseline

Purpose: verify the current logged-out substrate is still reachable at compliant pace before any
larger repeated-window test.

Shape:

- One egress lane.
- 4-6 locked public handles.
- Profile-enumeration viewport: start at `768x1024`; record any fallback to JSON shortcode
  enumeration.
- Pace: 2.5-4s minimum spacing with longer natural gaps; never sub-2s.
- Size: about 80-120 modeled IG-request equivalents.
- Stop on first block marker or unexpected auth wall.

Interpretation:

- Clean baseline: proceed to Stage 2.
- Any block at compliant pace: stop, record receipt, run a fully quiet cooldown, and do not expand
  until the failure is classified.
- Missing signal but HTTP/page access clean: first check viewport and JSON fallback. If access remains
  clean, classify as content-shape/fidelity issue, not a rate wall.

### Stage 2 - Repeated Single-Lane Sustainability Windows

Purpose: test whether compliant logged-out reads remain usable across repeated sessions, instead of
only within one clean run.

Shape:

- Same egress lane as Stage 1.
- 8-12 locked handles.
- 3 windows over 2-3 days, owner-initiated each time.
- Each window is time-bounded and self-terminating.
- Target window size starts below the serious-v0 per-lane daily load, then steps up only if prior
  windows are clean.

Suggested progression:

| Window | Target | Approximate modeled requests | Purpose |
| --- | --- | ---: | --- |
| W1 | small operating window | 150-250 | Checks repeatability after Stage 1. |
| W2 | medium operating window | 350-600 | Looks for accumulation under normal compliant pace. |
| W3 | stress-but-compliant window | 700-1,000 | Approaches serious-v0 per-lane pressure without deliberately crossing the pace wall. |

Spacing:

- Read spacing remains 2.5-4s minimum with natural gaps.
- Insert cluster gaps after small groups of creator/item reads.
- Leave a fully quiet gap between windows; do not run background probes in between.

Interpretation:

- Three clean windows: logged-out single-lane sustainability is provisionally supported for this
  bounded profile, but not validated or commercially ready.
- Block in W1/W2/W3: classify the failure by pace, elapsed time, cumulative modeled requests,
  page/block type, and recovery behavior.
- Sticky block after quiet cooldown: this becomes the gating evidence for fallback analysis.

### Stage 3 - Two-Lane Additivity Check

Purpose: test whether the two stable egress lanes behave independently enough to support the
serious-v0 window.

Prerequisite:

- Stage 0 network separation has passed.
- Stage 1 and at least one Stage 2 window are clean on Lane 1.
- Owner explicitly authorizes the two-lane IG read test.

Shape:

- Lane 1 and Lane 2 run separate locked handle subsets.
- No per-request rotation.
- No same-handle tight loops across both lanes.
- Each lane stays within compliant pace.
- Start with small simultaneous windows; increase only after clean receipts.

Interpretation:

- Both lanes clean: supports the two-lane operating-envelope assumption.
- One lane blocks and the other stays clean: suggests egress-specific capacity or environment issue.
- Both lanes block under compliant pace: suggests the logged-out operating assumption is weaker than
  the current envelope, and fallback analysis should reopen.

### Stage 4 - Optional Recovery Characterization

Purpose: characterize recovery only after a block has already occurred.

Do not run periodic probes every few minutes. The previous endurance attempts suggest gentle periodic
probing may sustain the throttle state. Use fully quiet cooldowns instead.

Minimum recovery sequence:

- Stop immediately at wall.
- Fully quiet cooldown: start with at least 60 minutes.
- One low-density recovery read.
- If still blocked, stop again and extend the quiet interval; do not keep probing.

Interpretation:

- Recovery after quiet cooldown: preserve logged-out posture but add cooldown/abort rules.
- No recovery after extended quiet: treat as a serious sustainability failure and route to fallback
  decision, not implementation.

## Measurement Ledger

Every run must produce an append-only receipt. Minimum fields:

| Field | Required note |
| --- | --- |
| run_id | Stable identifier for the window. |
| lane_id | Lane 1 / Lane 2; include egress type without exposing secrets or exit IP in durable docs. |
| access_classification | Publicly-viewable, publicly-viewable-but-ToS-restricted, access-controlled, operator-supplied/manual-only, or unknown. |
| subject_handle | Locked before run; no discovery during run. |
| capture_kind | profile, item, post permalink, profile-feed, or other. |
| modeled_request_count | State modeling assumptions; do not pretend exact network requests were counted unless instrumented. |
| cadence_min_max | Observed/read-configured spacing range. |
| page_result | captured, no_signal, access_blocked, redirected_to_login, rate_limited_429_interstitial, network_security_block, capture_failed. |
| block_reason | If any. |
| stop_reason | normal_ceiling, operator_abort, block_onset, auth_wall, unexpected_error. |
| quiet_cooldown | If recovery was attempted. |
| viewport | Profile-enumeration viewport; required for any DOM-grid success or failure interpretation. |
| enumeration_route | DOM grid, profile-feed JSON, or mixed fallback. |
| verdict | GO, PARTIAL, NO-GO, or CATALOG_GAP as defined by the source-capture playbook. |

No receipt means no strict interpretation. Chat summaries or operator memory are not enough.

## Decision Tree

```text
IF Stage 1 fails at compliant pace:
  classify as substrate/auth/block issue; do not expand.

ELSE IF Stage 2 completes clean:
  logged-out single-lane sustainability is provisionally supported for the tested profile.

ELSE IF Stage 2 blocks but recovers after fully quiet cooldown:
  keep logged-out posture; add cooldown/abort envelope; do not jump to sessions.

ELSE IF Stage 2 blocks repeatedly at compliant pace after fully quiet cooldown:
  reopen fallback analysis.

IF Stage 3 two-lane additivity is clean:
  two-lane serious-v0 operating posture is provisionally supported for planning.

ELSE IF one lane fails and the other remains clean:
  treat as egress/environment-specific; fix lane or test third distinct egress only if owner authorizes.

ELSE IF both lanes fail under compliant pace:
  route to fallback decision: more egress lanes/proxies vs sessioned runtime vs roster/cadence reduction.
```

Fallback analysis is a decision lane, not an automatic build path.

## Explicit Non-Goals

- Do not test discovery snowballing.
- Do not test private/auth-gated content.
- Do not test sessions, cookies, login, or stored auth state.
- Do not test proxies, anti-detect tooling, CAPTCHA solving, or commercial-scale collection.
- Do not test standing scheduler behavior.
- Do not prove typed capture, ECR, Cleaning, Judgment, buyer proof, validation, or readiness.
- Do not use the probe as proof that media/video bytes are capturable.
- Do not use the probe as proof that TikTok, YouTube, Reddit, or other platform satellites share IG's envelope.

## Owner Authorization Needed Before Any Run

Before any live IG read, the owner should explicitly authorize:

1. Subject set: the locked public creator handles.
2. Stage scope: Stage 1 only, Stage 1+2, or Stage 1+2+3.
3. Lane scope: one lane only, or two-lane additivity after Stage 0.
4. Ceilings: modeled request ceiling per window, time ceiling per window, total windows.
5. Cooldown policy: minimum fully quiet cooldown after any block.
6. Output location: gitignored scratch for raw operational receipts; durable summary only if separately requested.

Default recommendation: authorize Stage 0 and Stage 1 first. Expand to Stage 2 only after a clean
Stage 1 receipt, and expand to Stage 3 only after at least one clean Stage 2 window plus confirmed
non-IG network separation.

## Non-Claims

This plan is not authorization to run the probe. It is not validation, readiness, product proof,
legal advice, commercial authorization, proxy-purchase approval, network-setup approval,
session/cookie authorization, anti-detect implementation, scheduler runtime, deployment, ECR,
Cleaning, Judgment, or projection acceptance.

Future clean results should be stated as bounded observations over the tested handles, lanes,
cadence, window size, and date. They must not be generalized into permanent IG safety, commercial
readiness, or platform-wide durability.
