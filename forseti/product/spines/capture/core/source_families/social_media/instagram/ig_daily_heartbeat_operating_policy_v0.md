# IG Daily Heartbeat Operating Policy (v0)

```yaml
retrieval_header_version: 1
artifact_role: Product artifact - IG daily heartbeat operating policy (non-authorizing)
scope: >
  Current owner direction for steady-state Instagram creator grid heartbeat:
  daily first-visible-grid monitoring for registered creators, read-only source
  access, breakout-only deep capture eligibility, owner-attention challenge
  handling, and the 2-egress posture for the 2.5k/day target. This excludes
  onboarding capture.
use_when:
  - Scoping steady-state IG creator monitoring cadence or runner posture.
  - Checking whether old A/B/C sparse cadence docs are current for IG daily heartbeat.
  - Separating daily heartbeat monitoring from creator onboarding capture.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_at_scale_operating_envelope_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_monitoring_policy_architecture_v0.md
stale_if:
  - A later owner decision reintroduces tiered sparse cadence for registered IG creators.
  - Runner telemetry proves the 2-egress 2.5k/day posture is too tight or unnecessarily conservative.
  - The IG grid runner is patched and verified to a different asset, challenge, pagination, or deep-capture policy.
```

## Status

`OWNER_DIRECTION_RECORDED_V0`. This is a policy artifact, not runner
implementation, validation, account-safety proof, live-capture authorization,
or platform permission. It records the current steady-state operating direction
for IG daily heartbeat and names where current code may still lag the target
policy.

## Current Direction

For now, registered IG creators are monitored with one daily first-visible-grid
heartbeat. Do not use A/B/C sparse cadence as the current operating default for
registered IG creators. Tiering, promotion, demotion, and future sparse Tier-C
cadence remain deferred capacity tools, not current daily-heartbeat behavior.

The target roster posture is:

```text
steady_state_registered_roster = daily heartbeat
2.5k/day serious posture = 2 distinct egress lanes
third_egress = only after telemetry shows two lanes cannot fit cleanly
```

Use stable lane assignment rather than rotating every request. For the expected
2-egress posture, lane 1 may be the main machine on home Ethernet/fibre and
lane 2 may be a separate phone-tether/mobile-data route. Verify lane separation
with non-IG public-IP/provider checks before treating the lanes as distinct.
Do not store exact public IPs in durable docs unless debugging requires it.

The normal-grid target is `10-15s` end-to-end per creator. Owner-attention
pauses, CAPTCHA/challenge waits, network outages, and manual intervention time
must be recorded separately and excluded from the normal E2E average.

## Daily Heartbeat Scope

The daily heartbeat is additive time-series capture, not destructive refresh.
Each run adds another observation point for the creator/grid/post metrics.

Default heartbeat scope:

- one registered creator;
- one `/reels/` grid surface;
- first visible grid only;
- no pagination by default;
- no scroll expansion by default;
- no item-page fan-out by default;
- no comment-thread/body capture by default;
- no platform write actions.

DOM parsing is local, but source access is still visible to the platform as
browser/resource behavior. Do not claim DOM reading is invisible, low-risk, or
equivalent to official API access.

## Asset Posture

Target policy: ordinary browser asset loading is preferred for supervised daily
heartbeat. Heavy asset blocking is an explicit bandwidth mode, not the target
default and not a stealth, human-likeness, or safety claim.

Current implementation note: the existing grid runner may still default to
heavy-asset blocking until a later runner patch changes and verifies it. This
policy does not claim code alignment.

## Challenge / CAPTCHA Handling

On a CAPTCHA, challenge route, login redirect, suspicious-activity notice, or
similar owner-resolvable interstitial:

- pause the affected run or lane;
- notify/ping the owner/operator;
- keep the supervised browser/session open when that runner owns the lifecycle;
- wait for manual owner resolution only within a bounded operator window;
- do not auto-solve, route around, retry harder, or write a fake-success packet.

If the owner-attention window expires or the run is not a supervised browser
session, record the timepoint as an explicit access gap with the observed
reason. Missing activity is missingness, not zero.

## Read-Only Boundary

The runner remains read-only. It must not auto-like, comment, follow, save,
DM, vote, or perform any other platform write action.

This is not because one like materially contaminates a high-volume metric. The
risk is that write actions create account-action footprint, public side
effects, creator notifications, and retry/duplicate failure modes. Aphrodite
workflow memory should use internal tags, queue states, and notes instead of
platform interactions. Manual owner behavior during supervision is out of band
and must not become runner state.

## Deep Capture Boundary

Daily heartbeat and onboarding are separate lanes.

Steady-state heartbeat may queue deep capture only for posts already tagged by
monitoring as one of:

- `spike_candidate`;
- `fresh_breakout_candidate`;
- `active_breakout_candidate`;
- `durable_breakout_candidate`.

If no tagged candidate exists for a creator, the steady-state daily heartbeat
does not deep-capture that creator. Do not run random `0-2 per creator` deep
captures as part of daily heartbeat.

Onboarding may still have its own initial grid plus top-band/intake deep
capture policy, but that is not governed by this document. Do not import
onboarding top-band rules into daily heartbeat without a separate owner
decision.

## Future Runner Metadata

A later runner patch should make packets or run receipts expose the policy
posture without implying validation:

```yaml
behavior_policy_version: ig_daily_heartbeat_operating_policy_v0
heartbeat_mode: daily_registered_creator_grid
grid_scope: first_visible_grid_only
pagination_attempted: false
scroll_expansion_attempted: false
platform_write_actions_attempted: false
asset_policy: browser_default_assets | heavy_assets_blocked_bandwidth_mode
owner_attention_status: not_needed | needed | resolved | expired
normal_e2e_ms:
owner_attention_wait_ms:
egress_lane_id:
deep_capture_selection: no_candidate | breakout_candidate_selected | not_applicable
```

These fields are a future implementation target. This policy does not assert
they exist in current packets.

## Deferred

- 2.5k/day live test. Wait until runner telemetry can measure normal E2E,
  owner-attention rate, access gaps, and lane split cleanly.
- Tiering, promotion, demotion, and sparse Tier-C cadence. All registered IG
  creators are daily for now.
- Pagination and history backfill.
- Platform write-action experiments.
- Proxy or third-egress setup beyond the two-egress serious posture.
- Onboarding capture policy.

## Non-Claims

- not live capture authorization
- not validation or readiness
- not account-safety proof
- not platform permission
- not anti-detection, stealth, or evasion guidance
- not runner implementation alignment
- not onboarding policy
- not deep media preservation proof
- not a buyer, demand, credibility, or Judgment claim
