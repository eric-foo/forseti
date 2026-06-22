# Social Browser Behavior Recon-First Calibration Note v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture recommendation - social browser-behavior calibration (non-authorizing)
scope: >
  Recommends an IG-first browser-behavior calibration change set while gating
  TikTok and YouTube inheritance on source-family recon and recipe cards.
use_when:
  - Deciding whether to patch IG browser-behavior docs before implementation scoping.
  - Checking which browser-behavior primitives are only candidate-shared until each social surface has recon.
  - Deciding whether TikTok or YouTube can inherit IG-derived capture thresholds.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/source_families/instagram/ig_at_scale_operating_envelope_v0.md
  - orca/product/spines/capture/source_families/instagram/ig_logged_out_sustainability_probe_plan_v0.md
  - orca/product/spines/capture/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/source_capture_toolbox/capture_recon_index_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
branch_or_commit: codex/social-capture-browser-calibration-prompt @ c103355c
stale_if:
  - IG sustained-cadence, cooldown, viewport, route, or two-lane additivity evidence changes.
  - TikTok or YouTube receive source-family recon, recipe cards, or access-posture decisions.
  - The source-access boundary, wind-caller carve-out, capture playbook, or IG runner receipt shape changes.
```

## Status And Boundary

Status: `RECOMMEND_RECON_FIRST_FOR_TIKTOK_YOUTUBE`; secondary label
`IG_PATCH_NOW__TT_YT_RECON_FIRST`.

This is a planning recommendation only. It does not authorize live IG, TikTok,
or YouTube reads; runtime changes; browser automation setup; session/cookie use;
proxy purchase; anti-detect tooling; CAPTCHA handling; scheduler work; or
platform-policy claims.

## Source Readiness

`SOURCE_CONTEXT_INCOMPLETE`, but sufficient for the recommendation.

Ready:

- IG browser-behavior evidence is source-loaded enough for an IG-first change
  set. The IG sources already bind logged-out-first capture, a pace-bound R
  reading, viewport sensitivity, stable egress lanes, abort-on-wall posture, and
  a non-authorizing sustainability probe plan.
- The source-access and source-capture method sources are loaded enough to keep
  access gates, receipt discipline, and honest `GO` / `PARTIAL` / `NO-GO` /
  `CATALOG_GAP` semantics visible.
- Three advisory subagents were used after source loading: IG spine mapper,
  generalization skeptic, and harness/receipt mapper. Their outputs were
  advisory inputs only, not verdicts or readiness evidence.

Incomplete:

- No durable TikTok or YouTube capture source-family recon or recipe card was
  found under `orca/product/spines/capture/source_families/`; current source
  family folders are `instagram` and `retail_pdp`.
- Repository search found TikTok and YouTube mostly as planned, deferred, or
  adjacent product/research seams, not as capture recipe cards.
- Current TikTok and YouTube platform-policy posture was not externally
  verified in this pass. Treat it as `UNKNOWN - requires source check`.

## Cynefin Routing Result

Smallest complete outcome: write one non-authorizing recommendation artifact
that decides the browser-behavior architecture direction and names the next
authorized step.

Regime: complicated with a complex edge.

Why: IG behavior is reasoned from current source-backed evidence, but
TikTok/YouTube generalization depends on missing platform-specific recon.

Decomposition: layer-based for IG; risk-first recon gate for TikTok/YouTube.

Current bottleneck: absence of TikTok/YouTube capture recon and recipe cards.

Riskiest assumption: that IG's logged-out pace, viewport, cooldown, and egress
behavior transfer to TikTok or YouTube.

Stop or pivot condition: a durable TikTok or YouTube source-family recon proves
shared thresholds, route shape, or access posture, or proves a different
substrate/control model.

Allowed next move: patch IG docs / prepare implementation scoping for IG
receipt and session-shape controls; commission TikTok/YouTube recon separately.

Disallowed next move: implement or document one shared social timing model with
IG-derived thresholds for TikTok/YouTube.

## Current IG Behavior Model

The IG model is already mostly directionally correct:

- Logged-out-first capture remains the default for current IG calls/stats and
  reel view-count evidence. Session/account runtime is a fallback/probe lane,
  not the default.
- The measured constraint is pace, not ordinary volume: clean reads occurred at
  `>=~2s`; sub-2s burst behavior tripped a sticky login redirect. The working
  operating target is 2.5-4s minimum spacing with longer natural gaps.
- `bounded_jitter` is necessary but too thin by itself. The envelope already
  says to shape whole sessions: warm-up, bounded due-list batches, cluster
  gaps, item caps, no discovery during passive monitoring, visible stop
  reasons, and full quiet after a wall.
- Profile enumeration is viewport-sensitive. `768x1024` is the current
  candidate, and profile-feed JSON shortcodes must be fallback evidence before
  an empty DOM grid becomes a source `NO-GO`.
- Stable distinct egress lanes matter. Per-request rotation and multiple
  accounts on one public egress must not be counted as throughput.

## Failure Modes Not Covered Well Enough

1. Session shape is split across docs and runner defaults rather than named as a
   single IG browser-behavior profile.
2. Cooldown language says fully quiet but does not pin a minimum default beyond
   the sustainability plan's future probe recommendation.
3. The runner can still fail on empty DOM permalinks before using profile-feed
   JSON shortcode fallback.
4. Receipts preserve many slice-level states, but run-level fields are weak:
   access classification, modeled request count, stop reason, quiet-cooldown
   status, lane identity, capture kind, and enumeration route.
5. Block taxonomy is partly implemented but not yet expressed as one reusable
   receipt contract that separates login redirect, 429-like wait page, network
   security block, missing signal, no signal, partial signal, empty DOM grid,
   and viewport/content-shape failure.
6. TikTok/YouTube have no source-backed route, substrate, threshold, viewport,
   or receipt expectations to inherit from IG.
7. Browser fingerprint and interaction-shape variables are not yet carried as
   explicit recon dimensions: TLS/JA4/HTTP2/header parity, direct-HTTP client
   choice, headed/headless/browser-context differences, mouse/scroll/click
   shape, item-open ratio, dwell-time distribution, and silent empty-response
   detection.

## Proposed Change Set

| Change | Target surface | Source-backed rationale | Expected benefit | Risk / tradeoff | Evidence needed | Owner gate |
| --- | --- | --- | --- | --- | --- | --- |
| 1. Name an `IG logged-out browser-behavior profile` | Patch `ig_at_scale_operating_envelope_v0.md`; reflect in `ig_logged_out_sustainability_probe_plan_v0.md` | The envelope already says `bounded_jitter` is too thin and names session posture, cluster gaps, warm-up, no sub-2s, and stop-on-wall behavior. | Makes session shape auditable and harder to reduce to item sleeps. | Could be mistaken for runtime authorization unless kept non-authorizing. | Clean Stage 1/2 sustainability receipts under the named profile. | Docs patch only; any run still separately authorized. |
| 2. Tighten cooldown / abort semantics | Patch IG envelope and sustainability plan | R-probe evidence says gentle periodic probing may sustain the throttle; sustainability plan already recommends fully quiet cooldowns. | Reduces accidental throttle extension and preserves block visibility. | A default like 60 minutes is still a probe default, not proven recovery law. | Future recovery characterization: one low-density read after fully quiet intervals. | Owner authorizes any live recovery probe. |
| 3. Add viewport and JSON-fallback route profile | Patch IG envelope and future implementation-scoping prompt; later runner scoping may implement fallback | Current evidence shows DOM profile links are viewport-sensitive; JSON shortcodes should be checked before `NO-GO`. | Avoids false empty-grid failures from responsive layout. | JSON fallback may require new harness behavior and response-body handling. | Bounded receipt showing DOM-empty/JSON-present cases and route outcome. | Runtime patch requires separate implementation authorization. |
| 4. Promote run-level receipt fields | Patch sustainability plan Measurement Ledger and future scoping notes | Harness lane found slice-level states exist, but run-level access classification, modeled request count, stop reason, cooldown, lane, capture kind, and route are weak. | Makes durability evidence inspectable without hiding culling or blocks. | Too much schema too early could lock in noisy fields. | One append-only per-read/run receipt that explains all stop states. | Schema/runtime changes separately authorized. |
| 5. Consolidate block taxonomy | Patch IG docs; optionally later generalize as source-capture receipt vocabulary after more sources | Runner already detects `redirected_to_login`, `rate_limited_429_interstitial`, and `network_security_block`; the shape contract requires distinct non-observed reasons. | Prevents login redirect, rate limit, auth gate, missing signal, and viewport failure from collapsing into generic failure. | Shared vocabulary could overreach if treated as platform-equivalent thresholds. | IG receipts that map each observed failure to one token without fake success. | Docs patch now; shared taxonomy later only after recon. |
| 6. Keep stable-lane discipline explicit | Patch IG envelope / sustainability plan only | Current envelope says two stable egress lanes, no per-request rotation, and no multiple accounts on one egress as throughput. | Reduces bot-like run shape and false capacity assumptions. | May slow capture; that is acceptable because durability is the point. | Two-lane isolation + additivity receipts. | Owner authorizes Stage 0/3 live lane checks. |
| 7. Recon-first TikTok/YouTube gate | Patch this note into future routing; do not patch platform thresholds | Capture playbook says recipe cards are authored by probes; recon index says TikTok has no technical recon and social cards are speculative until probed. | Blocks the dangerous shared-controller overclaim while preserving candidate reusable primitives. | Slower cross-platform expansion. | TikTok/YouTube probe-authored recipe cards or recon-index entries with a `GO` / `PARTIAL` / `NO-GO` / `CATALOG_GAP` verdict, source-native evidence, substrate, route, access posture, request-rate ceiling, stop taxonomy, and receipts. | Separate recon commission per platform. |
| 8. Add fingerprint and interaction-shape recon dimensions | Patch future IG docs/scoping and TT/YT recon prompts as variables to measure, not defaults to run | Direct HTTP, browser-context XHR, headed/headless browser posture, and human interaction shape can change whether browser-behavior reads return source-native content or silent empty responses. | Prevents false NO-GO/empty-grid diagnoses and keeps burn-risk controls visible without hard-coding evasion behavior. | Can drift into anti-detect mimicry if turned into blanket defaults like fixed dwell percentages or TLS impersonation everywhere. | Tiny canary receipts comparing relevant route/client shapes, including TLS/HTTP client family, browser/runtime context, interaction shape, item-open ratio, dwell distribution, request count, and silent-empty outcome. | Docs/prompt variable only; any live probe or runtime change remains separately authorized. |

## Platform Generalization

Recommended architecture:

- Candidate shared core concept: browser-behavior controller as a
  non-authorizing planning hypothesis with substrate-agnostic primitives only:
  bounded/self-terminating sessions, human-shaped pacing, due-bucket batching,
  cluster gaps, stop-on-wall, full quiet cooldown, and honest receipt outcomes
  with opaque stop reasons.
- Platform profile: every threshold, viewport, enumeration route,
  block-token taxonomy, egress/lane model, access posture, HTTP/TLS client
  shape, browser/runtime context, interaction/dwell behavior, and
  route-specific receipt field lives in a platform profile. IG may fill initial
  values from current evidence. TikTok/YouTube profiles remain unfilled until
  recon.
- Do not create a shared controller implementation or universal thresholds now.

| Field | IG | TikTok | YouTube |
| --- | --- | --- | --- |
| Capture source-family recon | `known`: IG has current capture findings and operating envelope. | `unknown`: no durable capture recipe card found in this worktree. | `unknown`: no durable capture recipe card found in this worktree. |
| Access posture | `known`: logged-out-first for current public IG signals, with own-session/proxy as fallback/probe only. | `UNKNOWN - requires source check`; do not infer from IG. | `UNKNOWN - requires source check`; do not infer from IG. |
| Timing threshold | `known`: avoid sub-2s; target 2.5-4s minimum plus natural gaps. | `do_not_generalize`: no TT threshold source. | `do_not_generalize`: no YT threshold source. |
| Viewport / route behavior | `known`: IG DOM grid is viewport-sensitive; JSON fallback matters. | `do_not_generalize`: substrate unknown. | `do_not_generalize`: substrate unknown. |
| Cooldown | `known`: fully quiet after wall; exact decay unpinned. | `unknown`: recon required. | `unknown`: recon required. |
| Receipts | `known`: must preserve blocks, partials, no-signal, request model, stop reason, and route evidence. | `known primitive only`: receipts required; fields must be source-specific after recon. | `known primitive only`: receipts required; fields must be source-specific after recon. |
| Fingerprint / interaction shape | `unmeasured`: treat TLS/HTTP client shape, browser runtime, mouse/scroll/click shape, item-open ratio, dwell distribution, and silent-empty behavior as canary variables, not defaults. | `do_not_generalize`: no TT source. | `do_not_generalize`: no YT source. |
| Shared controller eligibility | IG can seed primitives and IG profile. | Recon-first only. | Recon-first only. |

## Required Propagation Surfaces If Accepted

Patch now, docs-only:

- `orca/product/spines/capture/source_families/instagram/ig_at_scale_operating_envelope_v0.md`
- `orca/product/spines/capture/source_families/instagram/ig_logged_out_sustainability_probe_plan_v0.md`

Prepare for later implementation scoping, not now:

- `orca-harness/runners/run_source_capture_ig_calls_packet.py`
- Source Capture Packet / receipt schema surfaces if run-level fields become
  persisted packet fields.
- Any future IG implementation-scoping prompt for JSON fallback, per-run receipt
  ledger, session-shape controls, or fingerprint/interaction-shape canaries.

Do not patch now:

- TikTok/YouTube thresholds, profile values, route defaults, access posture,
  HTTP/TLS client defaults, or interaction/dwell defaults.
- Source-access boundary, wind-caller carve-out, anti-block ladder, or capture
  playbook doctrine. This recommendation consumes those sources; it does not
  amend them.

## Open Owner Questions

1. Should the next docs patch be IG-only, or should it also add a short
   source-capture-toolbox note that defines the platform-profile gate?
2. For the IG cooldown default, should docs name the sustainability plan's
   `at least 60 minutes` future-probe default, or keep it as `fully quiet until
   owner-authorized recovery check`?
3. Should the next TikTok recon target be public web profile/video pages,
   official/commercial data routes, or a narrow source-access posture decision
   before any technical probe?
4. Should YouTube be handled as creator-momentum data via public pages/API/vendor
   route first, rather than browser-behavior calibration first?

## Next Authorized Step

Write an IG-only docs patch that:

1. names the IG logged-out browser-behavior profile;
2. tightens cooldown / abort semantics;
3. names viewport and JSON-fallback route discipline;
4. adds run-level receipt fields to the sustainability-plan ledger;
5. repeats the explicit non-generalization gate for TikTok/YouTube;
6. records browser fingerprint and interaction-shape variables as canary
   dimensions, not default behavior.

After that, commission separate TikTok and YouTube recon prompts before filling
any platform profile values.

## Non-Claims

This artifact is not validation, readiness, legal advice, platform permission,
source-access boundary amendment, implementation authorization, live-run
authorization, proxy/session approval, anti-detect approval, scraper API
approval, production runtime, scheduler authorization, ECR, Cleaning, Judgment,
buyer proof, commercial evidence, or proof that IG behavior transfers to
TikTok or YouTube.
